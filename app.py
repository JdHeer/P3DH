"""Main Streamlit application for European Banking Transparency Dashboard."""
import streamlit as st

import config
from src import data_loader

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    .feature-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown(f'<div class="main-header">{config.APP_ICON} {config.APP_TITLE}</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Comprehensive Analysis Tool for European Banking Transparency Data</div>', unsafe_allow_html=True)

# Load data to check availability
df = data_loader.load_data()

if df is None:
    st.error("⚠️ **Data Loading Error**")
    st.error(f"Failed to load data from: `{config.DATA_PATH}`")
    st.info("Please ensure the data file exists and is properly formatted.")
    st.stop()

# Welcome section
st.success("✅ Data loaded successfully!")

# Data summary
summary = data_loader.get_data_summary(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Records", f"{summary['total_rows']:,}")

with col2:
    st.metric("🏦 Banks Covered", summary['unique_banks'])

with col3:
    st.metric("📅 Time Periods", summary['unique_periods'])

with col4:
    st.metric("📈 Metrics", summary['unique_metrics'])

st.caption(f"**Data Range:** {summary['date_range']}")

st.markdown("---")

# Features overview
st.header("🎯 Dashboard Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.subheader("📊 Overview")
    st.write("Quick insights and key statistics across all banks and metrics")
    st.markdown("• Summary statistics")
    st.markdown("• Recent trends")
    st.markdown("• Data quality indicators")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.subheader("🔍 Compare")
    st.write("Deep dive into bank and metric comparisons")
    st.markdown("• Multi-bank comparison")
    st.markdown("• Multi-metric analysis")
    st.markdown("• Interactive heatmaps")
    st.markdown("• Automated insights")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.subheader("📈 Analytics")
    st.write("Advanced analytical tools and custom queries")
    st.markdown("• Regional comparisons")
    st.markdown("• Top performers analysis")
    st.markdown("• Correlation analysis")
    st.markdown("• Trend analysis")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Quick start guide
st.header("🚀 Quick Start Guide")

with st.expander("📖 How to use this dashboard"):
    st.markdown("""
    ### Getting Started

    1. **Navigation**: Use the sidebar on the left to navigate between different pages
    2. **Overview Page**: Start here to get a quick overview of the data
    3. **Compare Page**: Use smart selectors to:
       - Select banks by region or individually
       - Choose metrics by category or search
       - Select time periods
       - Generate visualizations and comparisons
    4. **Analytics Page**: Perform advanced analyses:
       - Regional comparisons
       - Top performer rankings
       - Correlation analysis
       - Custom data queries

    ### Smart Features

    - **Regional Grouping**: Banks are automatically grouped by geographic region
    - **Metric Categories**: Metrics are organized by type (Credit Risk, NPE, Collateral, etc.)
    - **Quick Presets**: Use preset buttons for common selections
    - **Automated Insights**: Get AI-generated insights about your data
    - **Export Options**: Download filtered data in Excel or CSV format

    ### Tips

    - 💡 Use the search function to quickly find specific banks or metrics
    - 💡 Start with fewer selections and expand as needed
    - 💡 Use the "Compare Banks" button for quick multi-bank analysis
    - 💡 Check the automated insights section for interesting findings
    - 💡 Export your filtered data for further analysis in Excel
    """)

# Data source info
st.markdown("---")
st.header("ℹ️ About the Data")

with st.expander("📋 Data Information"):
    st.markdown(f"""
    **Data Source:** European Banking Transparency Data

    **File:** `{config.DATA_PATH}`

    **Coverage:**
    - **{summary['unique_banks']}** European banks/countries
    - **{summary['unique_metrics']}** different metrics
    - **{summary['unique_periods']}** time periods
    - **{summary['total_rows']:,}** total data points

    **Time Range:** {summary['date_range']}

    **Categories:**
    - Credit Risk (Standard & IRB approaches)
    - Non-Performing Exposures (NPE)
    - Forborne Exposures
    - Collateral
    - NACE Sector Analysis

    **Last Updated:** {df['Period'].max().strftime('%B %Y')}
    """)

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | European Banking Transparency Dashboard v1.0")

# Sidebar information
with st.sidebar:
    st.header("📌 Navigation")
    st.info("""
    Use the pages above to:
    - 📊 **Overview**: View summary statistics
    - 🔍 **Compare**: Compare banks & metrics
    - 📈 **Analytics**: Advanced analysis tools
    """)

    st.markdown("---")

    st.header("❓ Help")
    st.markdown("""
    **Need help?**

    Check the Quick Start Guide on the main page for detailed instructions.

    **Common Tasks:**
    - Compare multiple banks on a single metric
    - Analyze trends over time
    - Export filtered data
    - View regional comparisons
    """)
