"""Download and export functionality."""
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st


def create_excel_download(df, filename_prefix="transparency_data"):
    """Create Excel file for download with multiple sheets."""
    if df is None or df.empty:
        st.warning("No data to download")
        return

    # Create Excel writer
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Main data sheet
        df.to_excel(writer, sheet_name='Data', index=False)

        # Summary statistics sheet
        summary_data = {
            'Metric': ['Total Rows', 'Unique Banks', 'Unique Periods', 'Unique Metrics'],
            'Value': [
                len(df),
                df['NSA'].nunique() if 'NSA' in df.columns else 'N/A',
                df['Period'].nunique() if 'Period' in df.columns else 'N/A',
                df['Label'].nunique() if 'Label' in df.columns else 'N/A'
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

        # Metadata sheet
        metadata = {
            'Field': ['Export Date', 'Export Time', 'Data Source', 'Total Records'],
            'Value': [
                datetime.now().strftime('%Y-%m-%d'),
                datetime.now().strftime('%H:%M:%S'),
                'European Banking Transparency Dashboard',
                len(df)
            ]
        }
        pd.DataFrame(metadata).to_excel(writer, sheet_name='Metadata', index=False)

    output.seek(0)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{filename_prefix}_{timestamp}.xlsx"

    return output, filename


def render_download_section(df, filtered_df=None):
    """Render download section with options."""
    st.subheader("📥 Download Data")

    download_option = st.radio(
        "What to download:",
        ["Filtered Data (Current Selection)", "All Data"],
        horizontal=True
    )

    df_to_download = filtered_df if download_option.startswith("Filtered") and filtered_df is not None else df

    if df_to_download is None or df_to_download.empty:
        st.warning("No data available to download")
        return

    # Show preview
    with st.expander("📊 Preview Data to Download"):
        st.write(f"**Total rows:** {len(df_to_download):,}")
        st.dataframe(df_to_download.head(10), use_container_width=True)

    # Download format options
    col1, col2 = st.columns(2)

    with col1:
        # Excel download
        excel_data, excel_filename = create_excel_download(df_to_download)
        st.download_button(
            label="📊 Download as Excel",
            data=excel_data,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col2:
        # CSV download
        csv_data = df_to_download.to_csv(index=False).encode('utf-8')
        csv_filename = f"transparency_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        st.download_button(
            label="📄 Download as CSV",
            data=csv_data,
            file_name=csv_filename,
            mime="text/csv",
            use_container_width=True
        )


def render_chart_export_button(fig, chart_name="chart"):
    """Render button to export chart as image."""
    if fig is None:
        return

    # Note: Plotly charts can be exported using the built-in modebar
    st.caption("💡 Tip: Use the camera icon in the chart to save as PNG")
