"""Bank and metric comparison page."""
import plotly.graph_objects as go
import streamlit as st

from components import downloads, insights
from src import config, data_loader, data_processor, metric_catalog

st.set_page_config(
    page_title=f"{config.APP_TITLE} - Compare",
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT
)

# Load data
df = data_loader.load_data()
if df is None:
    st.error("Failed to load data.")
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

# Compact top bar
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_period = st.selectbox(
        "Period",
        all_periods,
        index=len(all_periods) - 1,
        format_func=lambda x: x.strftime('%b %Y'),
        label_visibility="collapsed"
    )
    st.session_state.selected_period = selected_period

with col2:
    with st.popover("🎯 Presets"):
        if st.button("Nordic Banks - NPE", use_container_width=True):
            st.session_state.selected_banks = config.BANK_REGIONS["Nordic"]
            npe_metrics = [m for m in all_metrics if "Non-performing" in m or "NPE" in m]
            st.session_state.selected_metrics = npe_metrics[:3] if npe_metrics else all_metrics[:3]
            st.rerun()
        if st.button("Top 5 - Credit Risk", use_container_width=True):
            bank_sizes = data_processor.calculate_bank_sizes(df)
            st.session_state.selected_banks = list(bank_sizes.keys())[:5]
            credit_metrics = [m for m in all_metrics if "Credit" in m or "Risk" in m]
            st.session_state.selected_metrics = credit_metrics[:3] if credit_metrics else all_metrics[:3]
            st.rerun()

with col3:
    with st.popover("⚙️"):
        show_data = st.checkbox("Show data table", False)
        sort_by_value = st.checkbox("Sort by value", True)
        show_stats = st.checkbox("Show chart stats", True)
        compare_previous = st.checkbox("Show period change", False)

# Selectors
if not st.session_state.selectors_collapsed:
    st.markdown("##### 🏦 Banks")
    bank_cols = st.columns([2, 1, 1, 1])

    with bank_cols[0]:
        region_filter = st.pills(
            "Region",
            ["All"] + list(config.BANK_REGIONS.keys()),
            selection_mode="single",
            label_visibility="collapsed"
        )

        available_banks = config.BANK_REGIONS.get(region_filter, all_banks) if region_filter and region_filter != "All" else all_banks

        selected_banks = st.multiselect(
            "Banks",
            available_banks,
            default=[b for b in st.session_state.selected_banks if b in available_banks] if st.session_state.selected_banks else available_banks[:5],
            max_selections=15,
            label_visibility="collapsed"
        )
        st.session_state.selected_banks = selected_banks

    with bank_cols[1]:
        if st.button("Select All", use_container_width=True):
            st.session_state.selected_banks = available_banks[:15]
            st.rerun()

    with bank_cols[2]:
        if st.button("Clear", use_container_width=True):
            st.session_state.selected_banks = []
            st.rerun()

    with bank_cols[3]:
        if st.button("Reset", use_container_width=True):
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
        if st.button("Select All ", use_container_width=True):
            st.session_state.selected_metrics = filtered_metrics[:10]
            st.rerun()

    with metric_cols[2]:
        if st.button("Clear ", use_container_width=True):
            st.session_state.selected_metrics = []
            st.rerun()

    with metric_cols[3]:
        if st.button("Reset ", use_container_width=True):
            st.session_state.selected_metrics = all_metrics[:3]
            st.rerun()

# Collapse toggle
collapse_col1, collapse_col2 = st.columns([1, 3])
with collapse_col1:
    if st.button("▲ Hide" if not st.session_state.selectors_collapsed else "▼ Show"):
        st.session_state.selectors_collapsed = not st.session_state.selectors_collapsed
        st.rerun()

with collapse_col2:
    if selected_banks and selected_metrics:
        st.caption(f"📊 {len(selected_metrics)} chart{'s' if len(selected_metrics) > 1 else ''} × {len(selected_banks)} banks")

# Validation
if not selected_banks or not selected_metrics:
    st.info("👆 Select banks and metrics above")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔵 Nordic", use_container_width=True):
            st.session_state.selected_banks = config.BANK_REGIONS["Nordic"]
            st.session_state.selected_metrics = all_metrics[:3]
            st.rerun()
    with col2:
        if st.button("⭐ Top 5", use_container_width=True):
            bank_sizes = data_processor.calculate_bank_sizes(df)
            st.session_state.selected_banks = list(bank_sizes.keys())[:5]
            st.session_state.selected_metrics = all_metrics[:3]
            st.rerun()
    with col3:
        if st.button("🌍 All", use_container_width=True):
            st.session_state.selected_banks = all_banks[:10]
            st.session_state.selected_metrics = all_metrics[:3]
            st.rerun()
    st.stop()

# Filter data
filtered_df = data_loader.filter_data(df, banks=selected_banks, periods=[selected_period], metrics=selected_metrics)

if filtered_df is None or filtered_df.empty:
    st.warning("No data available")
    st.stop()

st.divider()

# Chart rendering
def format_number(val):
    if val >= 1000:
        return f'{val/1000:.0f}k'
    return f'{val:.0f}'

for idx, metric in enumerate(selected_metrics):
    metric_data = filtered_df[(filtered_df['Period'] == selected_period) & (filtered_df['Label'] == metric)]

    bank_values = metric_data.groupby('NSA', observed=True)['Amount'].sum().reset_index()
    bank_values = bank_values.rename(columns={'NSA': 'Bank'})  # Rename NSA to Bank

    if not bank_values.empty:
        if sort_by_value:
            bank_values = bank_values.sort_values('Amount', ascending=False)
        else:
            bank_values = bank_values.sort_values('Bank')

        # Period change
        period_change_text = ""
        if compare_previous and len(all_periods) > 1:
            period_idx = all_periods.index(selected_period)
            if period_idx > 0:
                previous_period = all_periods[period_idx - 1]
                prev_data = df[(df['Period'] == previous_period) & (df['Label'] == metric) & (df['NSA'].isin(selected_banks))]
                if not prev_data.empty:
                    current_total = bank_values['Amount'].sum()
                    previous_total = prev_data['Amount'].sum()
                    if previous_total > 0:
                        pct_change = ((current_total - previous_total) / previous_total) * 100
                        arrow = "📈" if pct_change > 0 else "📉" if pct_change < 0 else "➡️"
                        period_change_text = f" {arrow} {pct_change:+.1f}%"

        chart_height = max(250, min(450, len(selected_banks) * 35 + 100))

        # Header
        header_col1, header_col2 = st.columns([4, 1])
        with header_col1:
            st.markdown(f"**{metric_catalog.get_metric_short_name(metric)}**{period_change_text}")
        with header_col2:
            with st.popover("ℹ️"):
                st.caption(f"**{metric_catalog.get_metric_short_name(metric)}**")
                tags = metric_catalog.get_metric_type_tags(metric)
                st.write(f"Tags: {', '.join(tags)}")

        # Map colors (with fallback for missing banks)
        bank_values['Color'] = bank_values['Bank'].map(st.session_state.bank_colors).astype(object).fillna('#808080')

        # Chart
        fig = go.Figure(data=[
            go.Bar(
                x=bank_values['Bank'],
                y=bank_values['Amount'],
                marker_color=bank_values['Color'],
                text=[format_number(v) for v in bank_values['Amount']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>%{y:,.0f}<extra></extra>'
            )
        ])

        fig.update_layout(
            height=chart_height,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Amount",
            yaxis={'rangemode': 'tozero'},
            font={'size': 12},
            margin={'t': 20, 'b': 40}
        )

        st.plotly_chart(fig, width='stretch', key=f"chart_{idx}")

        # Data table toggle
        with st.expander("📊 View Data Table"):
            table_df = bank_values[['Bank', 'Amount']].copy()
            table_df['Amount'] = table_df['Amount'].apply(lambda x: f"{x:,.0f}")
            st.dataframe(table_df, hide_index=True, width='stretch')

        # Stats
        if show_stats:
            stat_cols = st.columns(5)
            with stat_cols[0]:
                st.metric("Total", f"{bank_values['Amount'].sum()/1000:.0f}k")
            with stat_cols[1]:
                st.metric("Average", f"{bank_values['Amount'].mean()/1000:.0f}k")
            with stat_cols[2]:
                st.metric("Max", f"{bank_values['Amount'].max()/1000:.0f}k")
            with stat_cols[3]:
                st.metric("Min", f"{bank_values['Amount'].min()/1000:.0f}k")
            with stat_cols[4]:
                avg = bank_values['Amount'].mean()
                outliers = bank_values[bank_values['Amount'] > avg * 2]
                st.metric("Outliers", len(outliers))

        st.divider()

# Data table
if show_data:
    st.divider()
    display_df = filtered_df[['NSA', 'Label', 'Amount']].copy()
    display_df['Label'] = display_df['Label'].apply(metric_catalog.get_metric_short_name)
    st.dataframe(display_df, width='stretch', height=300)

# Footer
st.divider()
action_cols = st.columns([1, 1, 4])

with action_cols[0]:
    with st.popover("💡 Insights"):
        insights.render_insights_section(filtered_df, banks=selected_banks, metrics=selected_metrics, period=selected_period)

with action_cols[1]:
    with st.popover("📥 Export"):
        downloads.render_download_section(df, filtered_df)
