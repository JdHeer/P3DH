# 🚀 Quick Start Guide

## Running the Dashboard

### Option 1: Using uv (Recommended)

```powershell
uv run dashboard
```

### Option 2: Using the run scripts

**Windows PowerShell:**
```powershell
.\run.ps1
```

**Windows Command Prompt:**
```cmd
run.bat
```

### Option 3: Manual activation

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the dashboard
streamlit run app.py
```

## Accessing the Dashboard

Once started, the dashboard will be available at:
- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.x.x:8501 (for access from other devices)

Your default web browser should open automatically. If not, manually navigate to http://localhost:8501

## Stopping the Dashboard

Press `Ctrl+C` in the terminal to stop the server.

## First Time Setup

If you haven't installed dependencies yet:

```powershell
# Create virtual environment
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
