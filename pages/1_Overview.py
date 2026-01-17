"""Overview dashboard page."""
import streamlit as st

import config
from components import charts
from src import bank_catalog, data_loader, data_processor

st.set_page_config(
    page_title=f"{config.APP_TITLE} - Overview",
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT
)

st.title("📊 Dashboard Overview")
st.markdown("---")

# Load data
df = data_loader.load_data()

if df is None:
    st.error("Failed to load data. Please check the data file path.")
    st.stop()

# Summary statistics
st.header("📈 Key Statistics")

summary = data_loader.get_data_summary(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", f"{summary['total_rows']:,}")

with col2:
    st.metric("Banks Covered", summary['unique_banks'])

with col3:
    st.metric("Time Periods", summary['unique_periods'])

with col4:
    st.metric("Unique Metrics", summary['unique_metrics'])

st.caption(f"📅 Data Range: {summary['date_range']}")

st.markdown("---")

# Recent trends
st.header("📊 Recent Trends")

col1, col2 = st.columns(2)

with col1:
    # Total exposure by bank (latest period)
    latest_period = df['Period'].max()
    latest_data = df[df['Period'] == latest_period]

    bank_totals = latest_data.groupby('NSA')['Amount'].sum().sort_values(ascending=False).head(10)

    if not bank_totals.empty:
        df_chart = bank_totals.reset_index()
        df_chart.columns = ['Bank', 'Amount']
        df_chart['Bank_Name'] = df_chart['Bank'].apply(bank_catalog.get_bank_display_name)

        charts.render_bar_chart(
            df_chart,
            title=f"Top 10 Banks by Total Exposure ({latest_period.strftime('%b %Y')})",
            x_col='Bank_Name',
            y_col='Amount',
            orientation='h',
            height=400
        )

with col2:
    # Distribution by sheet category
    sheet_totals = latest_data.groupby('Sheet')['Amount'].sum().sort_values(ascending=False)

    if not sheet_totals.empty:
        df_chart = sheet_totals.reset_index()
        df_chart.columns = ['Category', 'Amount']

        charts.render_bar_chart(
            df_chart,
            title=f"Exposure by Category ({latest_period.strftime('%b %Y')})",
            x_col='Category',
            y_col='Amount',
            orientation='h',
            height=400
        )

st.markdown("---")

# Time series overview
st.header("📈 Time Series Overview")

# Select a default metric for overview
default_metrics = [
    'Original Exposure (SA_and_IRB)',
    'Exposure value (SA_and_IRB)',
    'Risk exposure amount (SA_and_IRB)'
]

available_metrics = [m for m in default_metrics if m in df['Label'].unique()]

if available_metrics:
    selected_metric = st.selectbox(
        "Select metric to visualize:",
        options=available_metrics,
        index=0
    )

    # Top 5 banks for this metric
    top_banks = data_processor.get_top_banks(df, selected_metric, latest_period, n=5)

    if top_banks:
        comparison_data = data_processor.prepare_comparison_data(
            df,
            banks=top_banks,
            metric=selected_metric
        )

        if comparison_data is not None and not comparison_data.empty:
            # Format period labels
            comparison_data.index = comparison_data.index.strftime('%b %Y')

            charts.render_line_chart(
                comparison_data,
                title=f"{selected_metric} - Top 5 Banks Over Time",
                x_col='Period',
                height=500
            )

st.markdown("---")

# Data quality indicators
st.header("✅ Data Quality")

col1, col2, col3 = st.columns(3)

with col1:
    missing_amounts = df['Amount'].isna().sum()
    missing_pct = (missing_amounts / len(df)) * 100
    st.metric("Missing Values", f"{missing_pct:.2f}%", delta=None)

with col2:
    zero_amounts = (df['Amount'] == 0).sum()
    zero_pct = (zero_amounts / len(df)) * 100
    st.metric("Zero Values", f"{zero_pct:.2f}%", delta=None)

with col3:
    negative_amounts = (df['Amount'] < 0).sum()
    negative_pct = (negative_amounts / len(df)) * 100
    st.metric("Negative Values", f"{negative_pct:.2f}%", delta=None)

st.markdown("---")

# Navigation
st.info("💡 **Next Steps:** Use the sidebar to navigate to **Compare** page for detailed analysis!")
