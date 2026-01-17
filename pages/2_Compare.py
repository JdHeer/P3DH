"""Bank and metric comparison page."""
import streamlit as st

import config
from components import charts, downloads, insights, selectors
from src import data_loader, data_processor

st.set_page_config(
    page_title=f"{config.APP_TITLE} - Compare",
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT
)

st.title("🔍 Compare Banks & Metrics")
st.markdown("---")

# Load data
df = data_loader.load_data()

if df is None:
    st.error("Failed to load data. Please check the data file path.")
    st.stop()

# Sidebar filters
with st.sidebar:
    st.header("🎛️ Filters & Selection")

    # Period selector
    selected_periods = selectors.render_period_selector("compare")

    st.markdown("---")

    # Bank selector
    selected_banks = selectors.render_bank_selector("compare")

    st.markdown("---")

    # Metric selector
    selected_metrics = selectors.render_metric_selector("compare")

    st.markdown("---")

    # Action buttons
    selectors.render_action_buttons(selected_banks, selected_metrics, selected_periods)

# Main content area
if not selected_banks:
    st.warning("⚠️ Please select at least one bank from the sidebar")
    st.stop()

if not selected_metrics:
    st.warning("⚠️ Please select at least one metric from the sidebar")
    st.stop()

if not selected_periods:
    st.warning("⚠️ Please select at least one time period from the sidebar")
    st.stop()

# Filter data
filtered_df = data_loader.filter_data(
    df,
    banks=selected_banks,
    periods=selected_periods,
    metrics=selected_metrics
)

if filtered_df is None or filtered_df.empty:
    st.warning("No data available for the selected filters")
    st.stop()

# Show compact selection summary
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Banks", len(selected_banks))
with col2:
    st.metric("Metrics", len(selected_metrics))
with col3:
    st.metric("Periods", len(selected_periods))

st.divider()

# Comparison type - more compact
st.subheader("📊 Visualization")

comparison_type = st.radio(
    "Select comparison type:",
    ["Compare Banks (Single Metric)", "Compare Metrics (Single Bank)", "Heatmap (Banks × Metrics)"],
    horizontal=True
)

if comparison_type == "Compare Banks (Single Metric)":
    # Single metric, multiple banks comparison
    if len(selected_metrics) > 1:
        selected_metric = st.selectbox(
            "Select metric:",
            options=selected_metrics,
            index=0
        )
    else:
        selected_metric = selected_metrics[0]

    # Prepare data
    comparison_data = data_processor.prepare_comparison_data(
        filtered_df,
        banks=selected_banks,
        metric=selected_metric,
        periods=selected_periods
    )

    if comparison_data is not None and not comparison_data.empty:
        # Format index for display
        comparison_data.index = comparison_data.index.strftime('%b %Y')

        # Main chart - much larger
        if len(selected_periods) > 1:
            st.subheader(f"{selected_metric}")
            charts.render_line_chart(
                comparison_data,
                title="Bank Comparison Over Time",
                height=600
            )
        else:
            # Bar chart for single period
            latest_period = selected_periods[-1]
            latest_data = filtered_df[
                (filtered_df['Period'] == latest_period) &
                (filtered_df['Label'] == selected_metric)
            ]

            bank_values = latest_data.groupby('NSA')['Amount'].sum().reset_index()
            bank_values.columns = ['Bank', 'Amount']

            st.subheader(f"{selected_metric} - {latest_period.strftime('%b %Y')}")
            charts.render_bar_chart(
                bank_values,
                title="Bank Comparison",
                x_col='Bank',
                y_col='Amount',
                orientation='v',
                height=600
            )

        # Compact statistics below
        with st.expander("📊 View Statistics & Data Table"):
            latest_period = selected_periods[-1]
            stats = data_processor.calculate_statistics(
                filtered_df,
                banks=selected_banks,
                metric=selected_metric,
                period=latest_period
            )
            charts.render_statistics_card(stats, f"Stats for {latest_period.strftime('%b %Y')}")
            st.divider()
            charts.render_comparison_table(comparison_data, "Data Table")

elif comparison_type == "Compare Metrics (Single Bank)":
    # Single bank, multiple metrics comparison
    if len(selected_banks) > 1:
        selected_bank = st.selectbox(
            "Select bank to analyze:",
            options=selected_banks,
            index=0
        )
    else:
        selected_bank = selected_banks[0]

    st.subheader(f"📊 {selected_bank}")

    # Use latest period for metric comparison
    analysis_period = selected_periods[-1]

    metric_data = data_processor.prepare_metric_comparison_data(
        filtered_df,
        bank=selected_bank,
        metrics=selected_metrics,
        period=analysis_period
    )

    if metric_data is not None and not metric_data.empty:
        charts.render_bar_chart(
            metric_data,
            title=f"Metric Comparison - {selected_bank} ({analysis_period.strftime('%b %Y')})",
            x_col='Amoun:",
            options=selected_banks,
            index=0
        )
    else:
        selected_bank = selected_banks[0]

    # Use latest period for metric comparison
    analysis_period = selected_periods[-1]

    metric_data = data_processor.prepare_metric_comparison_data(
    # Use latest period
    analysis_period = selected_periods[-1]

    heatmap_data = data_processor.prepare_heatmap_data(
        filtered_df,
        banks=selected_banks,
        metrics=selected_metrics,
        period=analysis_period
    )

    if heatmap_data is not None and not heatmap_data.empty:
        st.subheader(f"Banks × Metrics - {analysis_period.strftime('%b %Y')}")

        # Normalization option
        normalize = st.checkbox("Normalize values", value=False)

        if normalize:
            heatmap_data = data_processor.normalize_data(heatmap_data, method='minmax')

        charts.render_heatmap(
            heatmap_data,
            title="Heatmap Comparison",
            height=max(600, len(selected_metrics) * 30)
        )

        # Data table in expander
        with st.expander("📋 View Data Table"):
            charts.render_comparison_table(heatmap_data, "Detailed Data")

# Compact sections in expanders
with st.expander("💡 View Insights & Suggestions"):
    insights.render_insights_section(
        filtered_df,
        banks=selected_banks,
        metrics=selected_metrics,
        period=selected_periods[-1] if selected_periods else None
    )

with st.expander("📥 Download Data"):
    downloads.render_download_section(df, filtered_df