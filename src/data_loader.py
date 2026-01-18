"""Data loading and caching module."""

from pathlib import Path

import pandas as pd
import streamlit as st

from . import config


@st.cache_data(ttl=config.CACHE_TTL, show_spinner=False)
def load_data():
    """Load the main transparency data with caching. Prefers Parquet over CSV."""
    try:
        data_path = Path(config.DATA_PATH)
        parquet_path = data_path.with_suffix('.parquet')

        # Try loading Parquet first (faster)
        if parquet_path.exists():
            df = pd.read_parquet(parquet_path)
        else:
            # Fall back to CSV
            df = pd.read_csv(config.DATA_PATH)

        # Basic data validation
        required_columns = ['LEI_Code', 'NSA', 'Period', 'Item', 'Label',
                          'Portfolio', 'Country', 'Amount', 'Sheet']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
            return None

        # Convert Period to datetime if needed (handles both integer and string formats)
        if 'Period' in df.columns and df['Period'].dtype != 'datetime64[ns]':
            df['Period'] = pd.to_datetime(df['Period'].astype(str), format='%Y%m')

        df['Period_Label'] = df['Period'].dt.strftime('%b %Y')

        return df
    except FileNotFoundError:
        st.error(f"Data file not found: {config.DATA_PATH}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


@st.cache_data(show_spinner=False)
def get_unique_values(df, column):
    """Get unique values from a column with caching."""
    if df is None or column not in df.columns:
        return []
    return sorted(df[column].unique().tolist())


@st.cache_data(show_spinner=False)
def get_banks():
    """Get list of all banks."""
    df = load_data()
    if df is None:
        return []
    # Use set for faster unique operation, then sort
    return sorted(set(df['NSA'].tolist()))


@st.cache_data(show_spinner=False)
def get_periods():
    """Get list of all time periods."""
    df = load_data()
    if df is None:
        return []
    return sorted(df['Period'].unique())


@st.cache_data(show_spinner=False)
def get_metrics():
    """Get list of all metrics."""
    df = load_data()
    if df is None:
        return []
    # Use set for faster unique operation, then sort
    return sorted(set(df['Label'].tolist()))


@st.cache_data(show_spinner=False)
def get_sheets():
    """Get list of all sheet categories."""
    df = load_data()
    if df is None:
        return []
    return sorted(df['Sheet'].unique().tolist())


def filter_data(df, banks=None, periods=None, metrics=None, sheets=None):
    """Filter dataframe based on selections."""
    if df is None:
        return None

    filtered_df = df.copy()

    if banks:
        filtered_df = filtered_df[filtered_df['NSA'].isin(banks)]

    if periods:
        filtered_df = filtered_df[filtered_df['Period'].isin(periods)]

    if metrics:
        filtered_df = filtered_df[filtered_df['Label'].isin(metrics)]

    if sheets:
        filtered_df = filtered_df[filtered_df['Sheet'].isin(sheets)]

    return filtered_df


def get_data_summary(df):
    """Get summary statistics about the data."""
    if df is None:
        return {}

    return {
        'total_rows': len(df),
        'unique_banks': df['NSA'].nunique(),
        'unique_periods': df['Period'].nunique(),
        'unique_metrics': df['Label'].nunique(),
        'date_range': f"{df['Period'].min().strftime('%b %Y')} - {df['Period'].max().strftime('%b %Y')}",
        'total_amount': df['Amount'].sum(),
        'avg_amount': df['Amount'].mean(),
    }
