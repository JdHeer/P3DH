"""Data & Information Page"""
import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime

import config
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

# Filter data
download_df = df.copy()
if selected_banks:
    download_df = download_df[download_df['NSA'].isin(selected_banks)]

with download_cols[1]:
    format_option = st.selectbox("Format", ["Excel", "CSV"], label_visibility="collapsed")

with download_cols[2]:
    if format_option == "Excel":
        # Create Excel file
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            download_df.to_excel(writer, sheet_name='Data', index=False)
        output.seek(0)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"banking_data_{len(selected_banks) if selected_banks else 'all'}_banks_{timestamp}.xlsx"
        
        st.download_button(
            label="Download",
            data=output,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    else:
        # CSV download
        csv_data = download_df.to_csv(index=False).encode('utf-8')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"banking_data_{len(selected_banks) if selected_banks else 'all'}_banks_{timestamp}.csv"
        
        st.download_button(
            label="Download",
            data=csv_data,
            file_name=filename,
            mime="text/csv",
            use_container_width=True
        )

st.caption(f"💾 Download includes {len(download_df):,} records")
