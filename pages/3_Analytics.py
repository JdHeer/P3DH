"""Advanced analytics page."""
import pandas as pd
import streamlit as st

import config
from components import charts, downloads
from src import bank_catalog, data_loader, data_processor, metric_catalog

st.set_page_config(
    page_title=f"{config.APP_TITLE} - Analytics",
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT
)

st.title("📈 Advanced Analytics")
st.markdown("---")

# Load data
df = data_loader.load_data()

if df is None:
    st.error("Failed to load data. Please check the data file path.")
    st.stop()

# Analysis type selector
st.header("🎯 Select Analysis Type")

analysis_type = st.selectbox(
    "Choose analysis:",
    [
        "Regional Comparison",
        "Top Performers Analysis",
        "Correlation Analysis",
        "Trend Analysis",
        "Custom Query"
    ]
)

st.markdown("---")

if analysis_type == "Regional Comparison":
    st.subheader("🌍 Regional Comparison")

    # Select metric
    metrics = data_loader.get_metrics()
    selected_metric = st.selectbox("Select metric:", options=metrics, index=0)

    # Select period
    periods = data_loader.get_periods()
    selected_period = st.selectbox(
        "Select period:",
        options=periods,
        format_func=lambda x: x.strftime('%b %Y'),
        index=len(periods) - 1
    )

    # Calculate regional totals
    regional_data = {}

    for region, banks in config.BANK_REGIONS.items():
        region_total = df[
            (df['NSA'].isin(banks)) &
            (df['Label'] == selected_metric) &
            (df['Period'] == selected_period)
        ]['Amount'].sum()

        regional_data[region] = region_total

    # Create dataframe
    regional_df = pd.DataFrame(list(regional_data.items()), columns=['Region', 'Amount'])
    regional_df = regional_df.sort_values('Amount', ascending=False)

    # Chart
    charts.render_bar_chart(
        regional_df,
        title=f"{selected_metric} by Region - {selected_period.strftime('%b %Y')}",
        x_col='Region',
        y_col='Amount',
        orientation='v'
    )

    # Details table
    st.markdown("---")
    st.subheader("📋 Regional Details")

    # Expand to show banks in each region
    for region in regional_df['Region']:
        with st.expander(f"{region} - {regional_data[region]:,.0f}"):
            region_banks = config.BANK_REGIONS[region]

            bank_data = df[
                (df['NSA'].isin(region_banks)) &
                (df['Label'] == selected_metric) &
                (df['Period'] == selected_period)
            ].groupby('NSA')['Amount'].sum().reset_index()

            bank_data.columns = ['Bank', 'Amount']
            bank_data = bank_data.sort_values('Amount', ascending=False)

            if not bank_data.empty:
                st.dataframe(bank_data, use_container_width=True)

elif analysis_type == "Top Performers Analysis":
    st.subheader("🏆 Top Performers")

    # Configuration
    col1, col2 = st.columns(2)

    with col1:
        metrics = data_loader.get_metrics()
        selected_metric = st.selectbox("Select metric:", options=metrics, index=0)

    with col2:
        periods = data_loader.get_periods()
        selected_period = st.selectbox(
            "Select period:",
            options=periods,
            format_func=lambda x: x.strftime('%b %Y'),
            index=len(periods) - 1
        )

    n_top = st.slider("Number of top banks to show:", min_value=5, max_value=20, value=10)

    # Get top banks
    top_banks = data_processor.get_top_banks(df, selected_metric, selected_period, n=n_top)

    if top_banks:
        # Get data for top banks
        top_data = df[
            (df['NSA'].isin(top_banks)) &
            (df['Label'] == selected_metric) &
            (df['Period'] == selected_period)
        ].groupby('NSA')['Amount'].sum().sort_values(ascending=False).reset_index()

        top_data.columns = ['Bank', 'Amount']
        top_data['Bank_Name'] = top_data['Bank'].apply(bank_catalog.get_bank_display_name)
        top_data['Region'] = top_data['Bank'].apply(bank_catalog.get_region_for_bank)

        # Chart
        charts.render_bar_chart(
            top_data,
            title=f"Top {n_top} Banks - {selected_metric} ({selected_period.strftime('%b %Y')})",
            x_col='Bank_Name',
            y_col='Amount',
            orientation='h',
            height=max(400, n_top * 30)
        )

        # Table with additional info
        st.markdown("---")
        st.subheader("📊 Detailed Rankings")

        display_data = top_data[['Bank', 'Bank_Name', 'Region', 'Amount']].copy()
        display_data['Rank'] = range(1, len(display_data) + 1)
        display_data = display_data[['Rank', 'Bank', 'Bank_Name', 'Region', 'Amount']]

        st.dataframe(display_data, use_container_width=True, hide_index=True)

elif analysis_type == "Correlation Analysis":
    st.subheader("🔗 Metric Correlation Analysis")

    st.info("💡 This analysis shows how different metrics relate to each other across banks")

    # Select metrics for correlation
    all_metrics = data_loader.get_metrics()

    # Select period
    periods = data_loader.get_periods()
    selected_period = st.selectbox(
        "Select period:",
        options=periods,
        format_func=lambda x: x.strftime('%b %Y'),
        index=len(periods) - 1
    )

    selected_metrics = st.multiselect(
        "Select metrics to analyze (2-10 recommended):",
        options=all_metrics,
        default=all_metrics[:5] if len(all_metrics) >= 5 else all_metrics,
        format_func=metric_catalog.get_metric_short_name
    )

    if len(selected_metrics) < 2:
        st.warning("Please select at least 2 metrics for correlation analysis")
    else:
        # Prepare data for correlation
        correlation_data = df[
            (df['Label'].isin(selected_metrics)) &
            (df['Period'] == selected_period)
        ].pivot_table(
            index='NSA',
            columns='Label',
            values='Amount',
            aggfunc='sum'
        )

        if not correlation_data.empty:
            # Calculate correlation
            corr_matrix = correlation_data.corr()

            # Heatmap
            charts.render_heatmap(
                corr_matrix,
                title=f"Metric Correlation Matrix - {selected_period.strftime('%b %Y')}",
                height=max(500, len(selected_metrics) * 40)
            )

            # Correlation table
            st.markdown("---")
            st.subheader("📊 Correlation Matrix")
            st.dataframe(corr_matrix.style.background_gradient(cmap='RdYlGn', vmin=-1, vmax=1), use_container_width=True)

elif analysis_type == "Trend Analysis":
    st.subheader("📈 Trend Analysis Over Time")

    st.info("💡 Analyze how metrics evolve over time for selected banks")

    # Select banks
    all_banks = data_loader.get_banks()
    selected_banks = st.multiselect(
        "Select banks (1-5 recommended):",
        options=all_banks,
        default=all_banks[:3],
        format_func=lambda x: f"{x} - {bank_catalog.get_bank_display_name(x)}"
    )

    # Select metric
    metrics = data_loader.get_metrics()
    selected_metric = st.selectbox("Select metric:", options=metrics, index=0)

    if not selected_banks:
        st.warning("Please select at least one bank")
    else:
        # Get all periods
        periods = data_loader.get_periods()

        # Prepare trend data
        trend_data = data_processor.prepare_comparison_data(
            df,
            banks=selected_banks,
            metric=selected_metric,
            periods=periods
        )

        if trend_data is not None and not trend_data.empty:
            # Format index
            trend_data.index = trend_data.index.strftime('%b %Y')

            # Line chart
            charts.render_line_chart(
                trend_data,
                title=f"Trend Analysis: {selected_metric}"
            )

            # Period-over-period change
            st.markdown("---")
            st.subheader("📊 Period-over-Period Change (%)")

            pct_change = data_processor.calculate_period_change(
                df,
                banks=selected_banks,
                metric=selected_metric
            )

            if pct_change is not None and not pct_change.empty:
                pct_change.index = pct_change.index.strftime('%b %Y')
                charts.render_period_change_chart(
                    pct_change,
                    title=f"Growth Rate: {selected_metric}"
                )

                # Statistics
                st.markdown("---")
                st.subheader("📈 Trend Statistics")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Average Growth", f"{pct_change.mean().mean():.2f}%")

                with col2:
                    st.metric("Highest Growth", f"{pct_change.max().max():.2f}%")

                with col3:
                    st.metric("Lowest Growth", f"{pct_change.min().min():.2f}%")

else:  # Custom Query
    st.subheader("🔍 Custom Data Query")

    st.info("💡 Build your own custom query to explore the data")

    col1, col2 = st.columns(2)

    with col1:
        # Banks
        all_banks = data_loader.get_banks()
        selected_banks = st.multiselect(
            "Select banks:",
            options=all_banks,
            format_func=lambda x: f"{x} - {bank_catalog.get_bank_display_name(x)}"
        )

    with col2:
        # Periods
        periods = data_loader.get_periods()
        selected_periods = st.multiselect(
            "Select periods:",
            options=periods,
            format_func=lambda x: x.strftime('%b %Y')
        )

    # Metrics
    all_metrics = data_loader.get_metrics()
    selected_metrics = st.multiselect(
        "Select metrics:",
        options=all_metrics,
        format_func=metric_catalog.get_metric_short_name
    )

    # Sheets
    sheets = data_loader.get_sheets()
    selected_sheets = st.multiselect(
        "Filter by category (optional):",
        options=sheets
    )

    if st.button("🔍 Run Query", type="primary"):
        # Filter data
        filtered_df = data_loader.filter_data(
            df,
            banks=selected_banks if selected_banks else None,
            periods=selected_periods if selected_periods else None,
            metrics=selected_metrics if selected_metrics else None,
            sheets=selected_sheets if selected_sheets else None
        )

        if filtered_df is None or filtered_df.empty:
            st.warning("No data matches your query")
        else:
            st.success(f"Found {len(filtered_df):,} records")

            # Summary stats
            st.markdown("---")
            st.subheader("📊 Query Results")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Records", f"{len(filtered_df):,}")

            with col2:
                st.metric("Total Amount", f"{filtered_df['Amount'].sum():,.0f}")

            with col3:
                st.metric("Average Amount", f"{filtered_df['Amount'].mean():,.0f}")

            with col4:
                st.metric("Unique Banks", filtered_df['NSA'].nunique())

            # Data preview
            st.markdown("---")
            st.subheader("📋 Data Preview")
            st.dataframe(filtered_df.head(100), use_container_width=True)

            # Download
            st.markdown("---")
            downloads.render_download_section(df, filtered_df)
