# European Banking Transparency Dashboard

An interactive Streamlit dashboard for analyzing European banking transparency data with comprehensive comparison and analysis tools.

## Features

- 📊 **Overview Dashboard**: Quick insights and key statistics
- 🔍 **Comparison Tools**: Compare banks and metrics with interactive visualizations
- 📈 **Advanced Analytics**: Regional comparisons, trend analysis, and correlation studies
- 💾 **Data Export**: Download filtered data in Excel or CSV format
- 💡 **Automated Insights**: AI-generated insights and suggestions
- 🎯 **Smart Selectors**: Regional grouping and category-based metric selection

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
pip install uv

# Install dependencies
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Usage

Run the dashboard:

```bash
# Recommended: Using uv
uv run dashboard

# Alternative: Direct streamlit command
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Project Structure

```
P3DH/
├── app.py                      # Main Streamlit application
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
