"""Bank Comparison Dashboard - Landing Page"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import config, data_loader, metric_catalog

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Header
st.title("Compare")

# Load data with spinner
with st.spinner('Loading data...'):
    df = data_loader.load_data()
    if df is None:
        st.error("⚠️ Failed to load data")
        st.stop()

# Small data summary
st.caption(f"{len(df):,} records · {df['NSA'].nunique()} banks · {df['Label'].nunique()} metrics")

# Get available options
all_banks = data_loader.get_banks()
all_metrics = data_loader.get_metrics()
all_periods = data_loader.get_periods()

# Initialize session state
if 'selected_banks' not in st.session_state:
    st.session_state.selected_banks = all_banks[:5]
if 'selected_metrics' not in st.session_state:
    st.session_state.selected_metrics = all_metrics[:3]
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = all_periods[-1]
if 'bank_colors' not in st.session_state:
    # Custom color palette
    colors = ['#002E2E', '#87E0B0', '#C3A8BA', '#295757', '#B0FFD9', '#DBCC9A',
              '#001414', '#5EB887', '#A2874C', '#485154', '#1C0D0F', '#000000']
    st.session_state.bank_colors = {
        bank: colors[i % len(colors)]
        for i, bank in enumerate(all_banks)
    }
if 'selectors_collapsed' not in st.session_state:
    st.session_state.selectors_collapsed = False

st.divider()

# Top bar - more compact
top_cols = st.columns([3, 2, 2])

with top_cols[0]:
    selected_period = st.selectbox(
        "📅 Period",
        all_periods,
        index=all_periods.index(st.session_state.selected_period) if st.session_state.selected_period in all_periods else len(all_periods)-1,
        format_func=lambda x: x.strftime('%b %Y') if pd.notna(x) else 'Unknown'
    )
    st.session_state.selected_period = selected_period

with top_cols[1]:
    sort_by_value = st.checkbox("📊 Sort by value", value=True)

with top_cols[2]:
    show_data = st.checkbox("📋 Show data table", value=False)

# Selectors (collapsible)
if not st.session_state.selectors_collapsed:
    st.markdown("##### 🏦 Banks")
    bank_cols = st.columns([1, 4, 1, 1])

    with bank_cols[0]:
        region_filter = st.selectbox("Region", ["All"] + list(config.BANK_REGIONS.keys()), label_visibility="collapsed")

    available_banks = config.BANK_REGIONS.get(region_filter, all_banks) if region_filter and region_filter != "All" else all_banks

    with bank_cols[1]:
        selected_banks = st.multiselect(
            "Banks",
            available_banks,
            default=[b for b in st.session_state.selected_banks if b in available_banks] if st.session_state.selected_banks else available_banks[:5],
            label_visibility="collapsed"
        )
        st.session_state.selected_banks = selected_banks

    with bank_cols[2]:
        if st.button("All", width="stretch"):
            st.session_state.selected_banks = available_banks
            st.rerun()

    with bank_cols[3]:
        if st.button("Clear", width="stretch"):
            st.session_state.selected_banks = []
            st.rerun()

    st.markdown("##### 📊 Metrics")
    metric_cols = st.columns([4, 1, 1])

    with metric_cols[0]:
        metric_search = st.text_input(
            "Search metrics",
            placeholder="Type to search...",
            label_visibility="collapsed"
        )

        filtered_metrics = metric_catalog.search_metrics(all_metrics, metric_search) if metric_search else all_metrics

        selected_metrics = st.multiselect(
            "Metrics",
            filtered_metrics,
            default=[m for m in st.session_state.selected_metrics if m in filtered_metrics] if st.session_state.selected_metrics else filtered_metrics[:3],
            format_func=metric_catalog.get_metric_short_name,
            label_visibility="collapsed"
        )
        st.session_state.selected_metrics = selected_metrics

    with metric_cols[1]:
        if st.button("All ", width="stretch"):
            st.session_state.selected_metrics = filtered_metrics
            st.rerun()

    with metric_cols[2]:
        if st.button("Clear ", width="stretch"):
            st.session_state.selected_metrics = []
            st.rerun()

# Collapse toggle
collapse_col1, collapse_col2 = st.columns([1, 3])
with collapse_col1:
    if st.button("▲ Hide" if not st.session_state.selectors_collapsed else "▼ Show"):
        st.session_state.selectors_collapsed = not st.session_state.selectors_collapsed
        st.rerun()

with collapse_col2:
    if st.session_state.selectors_collapsed:
        st.caption(f"📊 {len(selected_metrics)} metrics × 🏦 {len(selected_banks)} banks")

st.divider()

# Validation
if not selected_banks or not selected_metrics:
    st.info("👈 Select banks and metrics to compare")
    st.stop()

# Filter data efficiently using query where possible
filtered_df = df[
    (df['NSA'].isin(selected_banks)) &
    (df['Label'].isin(selected_metrics)) &
    (df['Period'] == selected_period)
].copy()  # Create copy to avoid SettingWithCopyWarning

st.divider()

# Chart rendering
def format_number(val):
    if val >= 1000000:
        return f'{val/1000000:.1f}M'
    elif val >= 1000:
        return f'{val/1000:.0f}k'
    return f'{val:.0f}'

# Determine layout: 1 or 2 columns based on number of banks
num_banks = len(selected_banks)
use_two_columns = num_banks <= 8  # Use 2 columns if 8 or fewer banks

chart_idx = 0
cols = None

# Render charts with progress
progress_bar = st.progress(0)
total_metrics = len(selected_metrics)

for metric_idx, metric in enumerate(selected_metrics):
    metric_data = filtered_df[filtered_df['Label'] == metric]

    if metric_data.empty:
        continue

    bank_values = metric_data.groupby('NSA', observed=True)['Amount'].sum().reset_index()
    bank_values = bank_values.rename(columns={'NSA': 'Bank'})

    if not bank_values.empty:
        if sort_by_value:
            bank_values = bank_values.sort_values('Amount', ascending=False)
        else:
            bank_values = bank_values.sort_values('Bank')

        # Calculate average for reference line
        avg_value = bank_values['Amount'].mean()

        # Determine column placement
        if use_two_columns:
            if chart_idx % 2 == 0:
                cols = st.columns(2)
            col = cols[chart_idx % 2]
        else:
            col = st.container()

        with col:
            # Compact metric header
            st.markdown(f"##### {metric_catalog.get_metric_short_name(metric)}")

            # Map colors
            bank_values['Color'] = bank_values['Bank'].map(st.session_state.bank_colors).astype(object).fillna('#808080')

            # Calculate dynamic height - more compact
            chart_height = max(180, min(350, num_banks * 25 + 60))

            # Chart with average line
            fig = go.Figure()

            # Add bars with improved styling
            fig.add_trace(go.Bar(
                x=bank_values['Bank'],
                y=bank_values['Amount'],
                marker_color=bank_values['Color'],
                marker_line_width=0,
                text=[format_number(v) for v in bank_values['Amount']],
                textposition='outside',
                textfont={'size': 10},
                hovertemplate='<b>%{x}</b><br>%{y:,.0f}<extra></extra>',
                showlegend=False
            ))

            # Add average line - more subtle
            fig.add_trace(go.Scatter(
                x=bank_values['Bank'],
                y=[avg_value] * len(bank_values),
                mode='lines',
                line={'color': 'rgba(150,150,150,0.5)', 'width': 1, 'dash': 'dash'},
                name='Average',
                hovertemplate=f'Avg: {format_number(avg_value)}<extra></extra>',
                showlegend=False
            ))

            fig.update_layout(
                height=chart_height,
                xaxis_title="",
                yaxis_title="",
                yaxis={'rangemode': 'tozero', 'gridcolor': 'rgba(200,200,200,0.2)'},
                plot_bgcolor='rgba(0,0,0,0)',
                font={'size': 10},
                margin={'t': 5, 'b': 25, 'l': 35, 'r': 5},
                hoverlabel={'bgcolor': 'white', 'font_size': 12}
            )

            st.plotly_chart(fig, width="stretch", key=f"chart_{chart_idx}")

            # Data table toggle - more compact
            with st.expander("📊 Data Table"):
                table_df = bank_values[['Bank', 'Amount']].copy()
                table_df['Amount'] = table_df['Amount'].apply(lambda x: f"{x:,.0f}")
                st.dataframe(table_df, hide_index=True, width="stretch", height=200)

        chart_idx += 1

        # Update progress
        progress_bar.progress((metric_idx + 1) / total_metrics)

# Clear progress bar
progress_bar.empty()

# Full data table
if show_data:
    st.divider()
    display_df = filtered_df[['NSA', 'Label', 'Amount']].copy()
    display_df['Label'] = display_df['Label'].apply(metric_catalog.get_metric_short_name)
    st.dataframe(display_df, width='stretch', height=300)
