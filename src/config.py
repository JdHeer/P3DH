"""Configuration settings for the Transparency Dashboard."""

# File paths
DATA_PATH = "data/tr_cre.csv"
METADATA_PATH = "data/TR_Metadata.xlsx"

# App settings
APP_TITLE = "European Banking Transparency Dashboard"
APP_ICON = "🏦"
PAGE_LAYOUT = "wide"

# Chart settings
DEFAULT_CHART_HEIGHT = 500
DEFAULT_COLOR_SCHEME = "Plotly"

# Data caching
CACHE_TTL = 3600  # 1 hour

# Bank groupings
BANK_REGIONS = {
    "Nordic": ["DK", "FI", "NO", "SE"],
    "Western Europe": ["AT", "BE", "DE", "FR", "LU", "NL"],
    "Southern Europe": ["ES", "GR", "IT", "PT", "CY", "MT"],
    "Eastern Europe": ["HU", "PL", "RO", "SI"],
    "Baltic": ["EE", "LT", "LV"],
    "Other": ["LI", "IE", "OT"]
}

# Metric categories based on sheet names
METRIC_CATEGORIES = {
    "Credit Risk - Standard Approach": "Credit Risk_STA",
    "Credit Risk - IRB Approach": "Credit Risk_IRB",
    "Non-Performing Exposures": "NPE",
    "Forborne Exposures": "Forborne exposures",
    "Collateral": "Collateral",
    "NACE Sectors": "NACE",
}

# Display formats
AMOUNT_FORMAT = "{:,.0f}"
PERCENTAGE_FORMAT = "{:.2f}%"
DECIMAL_FORMAT = "{:.2f}"

# Colors for charts
CHART_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]
