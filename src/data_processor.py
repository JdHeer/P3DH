"""Data processing and transformation utilities."""
import streamlit as st


def calculate_bank_sizes(df):
    """Calculate total exposure for each bank to determine size categories."""
    if df is None or df.empty:
        return {}

    # Calculate total amounts by bank
    bank_totals = df.groupby('NSA')['Amount'].sum().sort_values(ascending=False)

    # Categorize by quantiles
    quantiles = bank_totals.quantile([0.33, 0.67])

    size_dict = {}
    for bank, total in bank_totals.items():
        if total >= quantiles.iloc[1]:
            size_dict[bank] = 'Large'
        elif total >= quantiles.iloc[0]:
            size_dict[bank] = 'Medium'
        else:
            size_dict[bank] = 'Small'

    return size_dict


@st.cache_data
def get_metrics_by_category(df):
    """Group metrics by their sheet categories."""
    if df is None or df.empty:
        return {}

    metrics_by_sheet = {}
    for sheet in df['Sheet'].unique():
        sheet_metrics = df[df['Sheet'] == sheet]['Label'].unique().tolist()
        metrics_by_sheet[sheet] = sorted(sheet_metrics)

    return metrics_by_sheet


def prepare_comparison_data(df, banks, metric, periods=None):
    """Prepare data for bank comparison on a single metric."""
    if df is None or df.empty:
        return None

    filtered_df = df[
        (df['NSA'].isin(banks)) &
        (df['Label'] == metric)
    ]

    if periods:
        filtered_df = filtered_df[filtered_df['Period'].isin(periods)]

    # Pivot to get banks as columns, periods as rows
    pivot_df = filtered_df.pivot_table(
        index='Period',
        columns='NSA',
        values='Amount',
        aggfunc='sum'
    )

    return pivot_df


def prepare_metric_comparison_data(df, bank, metrics, period=None):
    """Prepare data for metric comparison for a single bank."""
    if df is None or df.empty:
        return None

    filtered_df = df[
        (df['NSA'] == bank) &
        (df['Label'].isin(metrics))
    ]

    if period:
        filtered_df = filtered_df[filtered_df['Period'] == period]

    # Group by metric and sum amounts
    summary_df = filtered_df.groupby('Label')['Amount'].sum().reset_index()
    summary_df.columns = ['Metric', 'Amount']

    return summary_df.sort_values('Amount', ascending=False)


def calculate_period_change(df, banks, metric):
    """Calculate period-over-period changes for selected banks and metric."""
    if df is None or df.empty:
        return None

    filtered_df = df[
        (df['NSA'].isin(banks)) &
        (df['Label'] == metric)
    ]

    # Pivot and calculate changes
    pivot_df = filtered_df.pivot_table(
        index='Period',
        columns='NSA',
        values='Amount',
        aggfunc='sum'
    ).sort_index()

    # Calculate percentage change
    pct_change_df = pivot_df.pct_change() * 100

    return pct_change_df


def get_top_banks(df, metric, period, n=10):
    """Get top N banks for a specific metric and period."""
    if df is None or df.empty:
        return []

    filtered_df = df[
        (df['Label'] == metric) &
        (df['Period'] == period)
    ]

    bank_totals = filtered_df.groupby('NSA')['Amount'].sum().sort_values(ascending=False)

    return bank_totals.head(n).index.tolist()


def calculate_statistics(df, banks, metric, period):
    """Calculate statistical summary for selected banks and metric."""
    if df is None or df.empty:
        return {}

    filtered_df = df[
        (df['NSA'].isin(banks)) &
        (df['Label'] == metric) &
        (df['Period'] == period)
    ]

    amounts = filtered_df.groupby('NSA')['Amount'].sum()

    return {
        'mean': amounts.mean(),
        'median': amounts.median(),
        'std': amounts.std(),
        'min': amounts.min(),
        'max': amounts.max(),
        'total': amounts.sum(),
        'count': len(amounts)
    }


def prepare_heatmap_data(df, banks, metrics, period):
    """Prepare data for heatmap visualization (banks x metrics)."""
    if df is None or df.empty:
        return None

    filtered_df = df[
        (df['NSA'].isin(banks)) &
        (df['Label'].isin(metrics)) &
        (df['Period'] == period)
    ]

    # Pivot to create matrix
    heatmap_df = filtered_df.pivot_table(
        index='Label',
        columns='NSA',
        values='Amount',
        aggfunc='sum',
        fill_value=0
    )

    return heatmap_df


def normalize_data(df, method='minmax'):
    """Normalize data for comparison."""
    if df is None or df.empty:
        return None

    df_normalized = df.copy()

    if method == 'minmax':
        # Min-max normalization to 0-1 range
        df_normalized = (df - df.min()) / (df.max() - df.min())
    elif method == 'zscore':
        # Z-score normalization
        df_normalized = (df - df.mean()) / df.std()
    elif method == 'percentage':
        # Percentage of total
        df_normalized = df / df.sum() * 100

    return df_normalized
