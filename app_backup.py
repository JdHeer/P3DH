"""Bank Comparison Dashboard - Landing Page"""
import streamlit as st
import plotly.graph_objects as go
from src import data_loader, metric_catalog
import config

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Load data
df = data_loader.load_data()
if df is None:
    st.error("⚠️ Failed to load data")
    st.stop()

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
    import plotly.colors as pc
    n_banks = len(all_banks)
    st.session_state.bank_colors = {
        bank: pc.sample_colorscale("Viridis", [i/(n_banks-1) if n_banks > 1 else 0.5])[0]
        for i, bank in enumerate(all_banks)
    }
if 'selectors_collapsed' not in st.session_state:
    st.session_state.selectors_collapsed = False

# Top bar
top_cols = st.columns([2, 2, 1, 1])

with top_cols[0]:
    selected_period = st.selectbox(
        "Period",
        all_periods,
        index=all_periods.index(st.session_state.selected_period),
        format_func=lambda x: x.strftime('%b %Y')
    )
    st.session_state.selected_period = selected_period

with top_cols[1]:
    with st.popover("📋 Presets"):
        if st.button("Nordic Banks - NPE", width='stretch'):
            st.session_state.selected_banks = [b for b in ['DK', 'FI', 'SE'] if b in all_banks]
            st.session_state.selected_metrics = [m for m in all_metrics if 'non-performing' in m.lower()][:3]
            st.rerun()
        if st.button("Top 5 - Credit Risk", width='stretch'):
            st.session_state.selected_banks = all_banks[:5]
            st.session_state.selected_metrics = [m for m in all_metrics if 'credit' in m.lower() or 'risk' in m.lower()][:3]
            st.rerun()

with top_cols[2]:
    sort_by_value = st.checkbox("Sort by value", value=True)

with top_cols[3]:
    show_data = st.checkbox("Show data", value=False)

# Selectors (collapsible)
if not st.session_state.selectors_collapsed:
    st.markdown("##### 🏦 Banks")
    bank_cols = st.columns([2, 1, 1, 1, 1])

    with bank_cols[0]:
        region_filter = st.selectbox("Region", ["All"] + list(config.BANK_REGIONS.keys()), label_visibility="collapsed")

    with bank_cols[1]:
        available_banks = config.BANK_REGIONS.get(region_filter, all_banks) if region_filter and region_filter != "All" else all_banks

        selected_banks = st.multiselect(
            "Banks",
            available_banks,
            default=[b for b in st.session_state.selected_banks if b in available_banks] if st.session_state.selected_banks else available_banks[:5],
            max_selections=15,
            label_visibility="collapsed"
        )
        st.session_state.selected_banks = selected_banks

    with bank_cols[2]:
        if st.button("Select All", width='stretch'):
            st.session_state.selected_banks = available_banks[:15]
            st.rerun()

    with bank_cols[3]:
        if st.button("Clear", width='stretch'):
            st.session_state.selected_banks = []
            st.rerun()

    with bank_cols[4]:
        if st.button("Reset", width='stretch'):
            st.session_state.selected_banks = all_banks[:5]
            st.rerun()

    st.markdown("##### 📊 Metrics")
    metric_cols = st.columns([2, 1, 1, 1])

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
            max_selections=10,
            label_visibility="collapsed"
        )
        st.session_state.selected_metrics = selected_metrics

    with metric_cols[1]:
        if st.button("Select All ", width='stretch'):
            st.session_state.selected_metrics = filtered_metrics[:10]
            st.rerun()

    with metric_cols[2]:
        if st.button("Clear ", width='stretch'):
            st.session_state.selected_metrics = []
            st.rerun()

    with metric_cols[3]:
        if st.button("Reset ", width='stretch'):
            st.session_state.selected_metrics = all_metrics[:3]
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
    
    st.markdown("**Quick Start Presets:**")
    preset_cols = st.columns(3)
    with preset_cols[0]:
        if st.button("Nordic Banks - NPE Metrics"):
            st.session_state.selected_banks = [b for b in ['DK', 'FI', 'SE'] if b in all_banks]
            st.session_state.selected_metrics = [m for m in all_metrics if 'non-performing' in m.lower()][:3]
            st.rerun()
    with preset_cols[1]:
        if st.button("Top 5 Banks - Credit Risk"):
            st.session_state.selected_banks = all_banks[:5]
            st.session_state.selected_metrics = [m for m in all_metrics if 'credit' in m.lower()][:3]
            st.rerun()
    with preset_cols[2]:
        if st.button("All Regions - Core Metrics"):
            st.session_state.selected_banks = all_banks[:10]
            st.session_state.selected_metrics = all_metrics[:3]
            st.rerun()
    st.stop()

# Filter data
filtered_df = df[
    (df['NSA'].isin(selected_banks)) &
    (df['Label'].isin(selected_metrics)) &
    (df['Period'] == selected_period)
]

# Chart rendering
def format_number(val):
    if val >= 1000:
        return f'{val/1000:.0f}k'
    return f'{val:.0f}'

# Determine layout: 1 or 2 columns based on number of banks
num_banks = len(selected_banks)
use_two_columns = num_banks <= 8  # Use 2 columns if 8 or fewer banks

chart_idx = 0
for metric in selected_metrics:
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
                col = cols[0]
            else:
                col = cols[1]
        else:
            col = st

        with col:
            st.markdown(f"**{metric_catalog.get_metric_short_name(metric)}**")

            # Map colors
            bank_values['Color'] = bank_values['Bank'].map(st.session_state.bank_colors).astype(object).fillna('#808080')

            # Calculate dynamic height
            chart_height = max(200, min(400, num_banks * 30 + 80))

            # Chart with average line
            fig = go.Figure()
            
            # Add bars
            fig.add_trace(go.Bar(
                x=bank_values['Bank'],
                y=bank_values['Amount'],
                marker_color=bank_values['Color'],
                text=[format_number(v) for v in bank_values['Amount']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>%{y:,.0f}<extra></extra>',
                showlegend=False
            ))
            
            # Add average line
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
                yaxis={'rangemode': 'tozero'},
                font={'size': 10},
                margin={'t': 10, 'b': 30, 'l': 40, 'r': 10}
            )

            st.plotly_chart(fig, width='stretch', key=f"chart_{chart_idx}")

            # Data table toggle
            with st.expander("📊 View Data"):
                table_df = bank_values[['Bank', 'Amount']].copy()
                table_df['Amount'] = table_df['Amount'].apply(lambda x: f"{x:,.0f}")
                st.dataframe(table_df, hide_index=True, width='stretch')

        chart_idx += 1

# Full data table
if show_data:
    st.divider()
    display_df = filtered_df[['NSA', 'Label', 'Amount']].copy()
    display_df['Label'] = display_df['Label'].apply(metric_catalog.get_metric_short_name)
    st.dataframe(display_df, width='stretch', height=300)
