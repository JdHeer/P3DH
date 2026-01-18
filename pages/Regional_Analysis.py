"""Data & Information Page"""
import streamlit as st

import config
from components import downloads
from src import data_loader

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

st.title("Data & Info")

# Load data
df = data_loader.load_data()

if df is None:
    st.error("⚠️ Failed to load data")
    st.stop()

# Data summary
summary = data_loader.get_data_summary(df)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Banks", summary['unique_banks'])
with col2:
    st.metric("Metrics", summary['unique_metrics'])
with col3:
    st.metric("Periods", summary['unique_periods'])
with col4:
    st.metric("Records", f"{summary['total_rows']//1000}k")

st.divider()

# About
with st.expander("📖 About", expanded=False):
    st.markdown("""
    **European Banking Transparency Dashboard**

    Interactive tool for analyzing regulatory data from European banks based on EBA transparency exercise requirements.

    **Data Source:** European Banking Authority (EBA) Transparency Exercise
    **Coverage:** 26 European banks across 89 metrics over 4 reporting periods
    **Purpose:** Enable comparison and analysis of key banking metrics
    """)

st.divider()

# Download section
st.markdown("#### 📥 Download Data")

download_cols = st.columns([2, 1, 1])

with download_cols[0]:
    selected_banks = st.multiselect(
        "Select banks (leave empty for all)",
        data_loader.get_banks(),
        default=None,
        label_visibility="collapsed"
    )

with download_cols[1]:
    format_option = st.selectbox("Format", ["Excel", "CSV"], label_visibility="collapsed")

with download_cols[2]:
    st.write("")  # Spacing
    st.write("")  # Spacing

    # Filter data
    download_df = df.copy()
    if selected_banks:
        download_df = download_df[download_df['NSA'].isin(selected_banks)]

    # Download button
    if format_option == "Excel":
        downloads.download_excel(download_df, f"banking_data_{len(selected_banks) if selected_banks else 'all'}_banks")
    else:
        downloads.download_csv(download_df, f"banking_data_{len(selected_banks) if selected_banks else 'all'}_banks")

st.caption(f"💾 Download includes {len(download_df):,} records")
