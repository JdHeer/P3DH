# European Banking Transparency Dashboard

Interactive Streamlit dashboard for analyzing European banking transparency data.

## Features

- 📊 **Overview**: Regional analysis and top banks at a glance
- 🔍 **Compare**: Multi-bank/metric comparison with advanced filtering
- 💾 **Export**: Download data in Excel/CSV
- 📈 **Analytics**: Consistent colors, period-over-period changes, outlier detection
- ⚡ **Performance**: Parquet support for 3-5x faster loading

## Quick Start

```bash
# Install dependencies
uv sync

# Convert data to Parquet (optional, recommended for speed)
uv run python utils/data_converter.py

# Run dashboard
uv run dashboard
```

Dashboard opens at http://localhost:8501

## Project Structure

```
P3DH/
├── app.py                  # Home page with regional analytics
├── dashboard.py            # CLI entry point
├── config.py               # Configuration
├── pages/
│   └── Compare.py          # Main comparison page
├── components/             # Reusable UI components
│   ├── charts.py           # Chart rendering
│   ├── downloads.py        # Data export
│   └── insights.py         # Automated insights
├── src/                    # Core logic
│   ├── data_loader.py      # Data loading (CSV/Parquet)
│   ├── data_processor.py   # Data transformations
│   ├── bank_catalog.py     # Bank information
│   └── metric_catalog.py   # Metric categorization
├── utils/
│   └── data_converter.py   # CSV to Parquet converter
└── data/                   # Data files
```

## Key Features

### Selection
- Region-based bank filtering (Nordic, Western Europe, etc.)
- Metric search and categorization
- Quick presets (Top 5, Nordic Banks, etc.)
- Select All / Clear / Reset buttons
- Collapsible selectors

### Visualization
- All metrics displayed simultaneously
- Consistent bank colors across charts
- Dynamic chart sizing
- Period-over-period % change
- Outlier detection (>2x average)
- Sortable by value or alphabetically

### Performance
- Parquet format: 3-5x faster loading
- 50-70% smaller file size
- Cached data loading
- Optimized data types

## Requirements

- Python 3.11+
- Streamlit 1.30+
- Pandas 2.0+
- Plotly 5.18+
- PyArrow 14.0+ (for Parquet)

## Data Format

Place your data file in `data/tr_cre.csv`. Required columns:
- LEI_Code, NSA, Period, Item, Label
- Portfolio, Country, Amount, Sheet

Convert to Parquet for better performance:
```bash
uv run python utils/data_converter.py
```
├── config.py                   # Configuration settings
├── pyproject.toml             # Project dependencies
├── data/                       # Data files
│   ├── tr_cre.csv
│   └── TR_Metadata.xlsx
├── src/                        # Core processing modules
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── bank_catalog.py
│   └── metric_catalog.py
├── components/                 # UI components
│   ├── selectors.py
│   ├── charts.py
│   ├── downloads.py
│   └── insights.py
└── pages/                      # Dashboard pages
    ├── 1_📊_Overview.py
    ├── 2_🔍_Compare.py
    └── 3_📈_Analytics.py
```

## Data Requirements

Place your data files in the `data/` directory:
- `tr_cre.csv`: Main transparency data (648,951 rows)
- `TR_Metadata.xlsx`: Metadata file (optional)

## Dashboard Pages

### 1. Overview
- Summary statistics across all banks and metrics
- Recent trends visualization
- Data quality indicators

### 2. Compare
- Smart bank selector with regional grouping
- Metric selector with category organization
- Multiple comparison modes:
  - Compare Banks (single metric)
  - Compare Metrics (single bank)
  - Heatmap (banks × metrics)
- Automated insights
- Data export functionality

### 3. Analytics
- Regional comparison analysis
- Top performers ranking
- Correlation analysis between metrics
- Trend analysis over time
- Custom data queries

## Key Features

### Smart Selection
- **Regional Grouping**: Nordic, Western Europe, Southern Europe, Eastern Europe, Baltic
- **Metric Categories**: Credit Risk, NPE, Forborne Exposures, Collateral, NACE
- **Quick Presets**: Top 10 banks, All exposure metrics, All risk metrics

### Visualizations
- Interactive line charts for time series
- Bar charts for cross-sectional comparison
- Heatmaps for multi-dimensional analysis
- Period-over-period change charts
- Statistical summaries

### Insights & Suggestions
- Automated data analysis
- Trend detection
- Outlier identification
- Comparative insights
- Analysis suggestions

## Technical Details

- **Framework**: Streamlit 1.30+
- **Data Processing**: Pandas 2.0+
- **Visualization**: Plotly 5.18+
- **Python**: 3.11+

## Development

Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

## License

Internal use only - Zanders BV

## Version

1.0.0 - January 2026
