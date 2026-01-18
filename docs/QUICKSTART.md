# 🚀 Quick Start Guide

## Running the Dashboard

```powershell
uv run dashboard
```

Dashboard opens at: **http://localhost:8501**

## First Time Setup

```powershell
# Install dependencies
uv sync

# Convert data to Parquet (recommended for speed)
uv run python utils/data_converter.py
```

## Using the Dashboard

### Home Page
- View regional analysis
- See top banks
- Check data summary

### Compare Page
1. **Select Period** - Choose time period from dropdown
2. **Choose Banks** - Use region filters or search
3. **Pick Metrics** - Search or browse categories
4. **View Charts** - All metrics shown at once

### Quick Actions
- **🎯 Presets** - Pre-configured selections
- **⚙️ Settings** - Toggle features (stats, sorting, period change)
- **▲ Hide** - Collapse selectors for more space

### Tips
- Use **Select All** / **Clear** for quick selection
- Click **ℹ️** on charts for metric details
- Enable **Show period change** to see trends
- Sort by value to find top/bottom banks

## Performance

Convert CSV to Parquet for 3-5x faster loading:
```powershell
uv run python utils/data_converter.py
```

## Stopping

Press `Ctrl+C` in the terminal to stop the server.
uv venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -e .
```

## Troubleshooting

### Error: "No module named 'streamlit'"
Run: `uv pip install -e .`

### Error: "Data file not found"
Ensure `data/tr_cre.csv` exists in the project directory

### Port already in use
Add `--server.port 8502` to use a different port:
```powershell
streamlit run app.py --server.port 8502
```

## Features Overview

### Main Page
- Overview of all data
- Key statistics
- Quick access to all features

### Overview Page (📊)
- Summary statistics
- Top banks visualization
- Time series trends
- Data quality metrics

### Compare Page (🔍)
- Smart bank selector (regional grouping)
- Smart metric selector (category grouping)
- Multiple comparison modes:
  - Compare banks on single metric
  - Compare metrics for single bank
  - Heatmap visualization
- Automated insights
- Download filtered data

### Analytics Page (📈)
- Regional comparison analysis
- Top performers ranking
- Correlation analysis
- Trend analysis
- Custom data queries

## Tips

- 💡 Use the sidebar to navigate between pages
- 💡 Start with the Overview page to understand your data
- 💡 Use regional grouping to quickly select multiple banks
- 💡 Export your filtered data for offline analysis
- 💡 Check the automated insights for interesting findings

## Performance Notes

- First load may take 10-30 seconds (loading 648k+ rows)
- Data is cached after first load for better performance
- Filtering and visualization are near-instantaneous after initial load

## Support

For issues or questions, check the main README.md file or contact your administrator.
