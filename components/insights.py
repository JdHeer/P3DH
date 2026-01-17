"""Automated insights and suggestions."""
import streamlit as st

from src import bank_catalog, metric_catalog


def generate_insights(df, banks=None, metrics=None, period=None):
    """Generate automated insights from the data."""
    if df is None or df.empty:
        return []

    insights = []

    # Filter data if specified
    filtered_df = df.copy()
    if banks:
        filtered_df = filtered_df[filtered_df['NSA'].isin(banks)]
    if metrics:
        filtered_df = filtered_df[filtered_df['Label'].isin(metrics)]
    if period:
        filtered_df = filtered_df[filtered_df['Period'] == period]

    # Insight 1: Highest exposure bank
    if not filtered_df.empty and 'Amount' in filtered_df.columns:
        bank_totals = filtered_df.groupby('NSA')['Amount'].sum().sort_values(ascending=False)
        if len(bank_totals) > 0:
            top_bank = bank_totals.index[0]
            top_amount = bank_totals.iloc[0]
            insights.append({
                'type': 'info',
                'title': '🏆 Highest Exposure',
                'message': f"{bank_catalog.get_bank_display_name(top_bank)} ({top_bank}) has the highest total exposure: {top_amount:,.0f}"
            })

    # Insight 2: Period-over-period trends
    if 'Period' in filtered_df.columns and filtered_df['Period'].nunique() > 1:
        periods_sorted = sorted(filtered_df['Period'].unique())
        if len(periods_sorted) >= 2:
            latest = periods_sorted[-1]
            previous = periods_sorted[-2]

            latest_total = filtered_df[filtered_df['Period'] == latest]['Amount'].sum()
            previous_total = filtered_df[filtered_df['Period'] == previous]['Amount'].sum()

            if previous_total != 0:
                change_pct = ((latest_total - previous_total) / previous_total) * 100
                direction = "increased" if change_pct > 0 else "decreased"

                insights.append({
                    'type': 'success' if change_pct > 0 else 'warning',
                    'title': '📈 Period Trend',
                    'message': f"Total exposure {direction} by {abs(change_pct):.2f}% from {previous.strftime('%b %Y')} to {latest.strftime('%b %Y')}"
                })

    # Insight 3: Regional comparison
    if banks and len(banks) > 1:
        regional_data = {}
        for bank in banks:
            region = bank_catalog.get_region_for_bank(bank)
            bank_total = filtered_df[filtered_df['NSA'] == bank]['Amount'].sum()

            if region not in regional_data:
                regional_data[region] = 0
            regional_data[region] += bank_total

        if regional_data:
            top_region = max(regional_data, key=regional_data.get)
            insights.append({
                'type': 'info',
                'title': '🌍 Regional Leader',
                'message': f"{top_region} region shows the highest total exposure among selected banks"
            })

    # Insight 4: Data quality
    null_counts = filtered_df['Amount'].isna().sum()
    if null_counts > 0:
        insights.append({
            'type': 'warning',
            'title': '⚠️ Data Quality',
            'message': f"Found {null_counts} missing values in selected data ({(null_counts/len(filtered_df)*100):.1f}%)"
        })

    # Insight 5: Outlier detection
    if 'Amount' in filtered_df.columns and len(filtered_df) > 10:
        q1 = filtered_df['Amount'].quantile(0.25)
        q3 = filtered_df['Amount'].quantile(0.75)
        iqr = q3 - q1
        outliers = filtered_df[
            (filtered_df['Amount'] < q1 - 1.5 * iqr) |
            (filtered_df['Amount'] > q3 + 1.5 * iqr)
        ]

        if len(outliers) > 0:
            insights.append({
                'type': 'info',
                'title': '🔍 Outliers Detected',
                'message': f"Found {len(outliers)} outlier values ({(len(outliers)/len(filtered_df)*100):.1f}% of data)"
            })

    return insights


def render_insights_section(df, banks=None, metrics=None, period=None):
    """Render insights section."""
    st.subheader("💡 Automated Insights")

    with st.spinner("Generating insights..."):
        insights = generate_insights(df, banks, metrics, period)

    if not insights:
        st.info("No specific insights available for current selection. Try selecting different banks or metrics.")
        return

    for insight in insights:
        insight_type = insight['type']
        title = insight['title']
        message = insight['message']

        if insight_type == 'success':
            st.success(f"**{title}**\n\n{message}")
        elif insight_type == 'warning':
            st.warning(f"**{title}**\n\n{message}")
        elif insight_type == 'error':
            st.error(f"**{title}**\n\n{message}")
        else:
            st.info(f"**{title}**\n\n{message}")


def render_suggestions_panel(df, banks, metrics):
    """Render suggestions for analysis."""
    st.subheader("🎯 Suggested Analyses")

    suggestions = []

    # Suggestion 1: Time series analysis
    if df is not None and 'Period' in df.columns and df['Period'].nunique() > 1:
        suggestions.append({
            'title': 'Time Series Analysis',
            'description': 'Analyze trends over time for selected banks and metrics',
            'action': 'View time trends'
        })

    # Suggestion 2: Peer comparison
    if banks and len(banks) == 1:
        bank = banks[0]
        region = bank_catalog.get_region_for_bank(bank)
        peer_banks = [b for b in bank_catalog.get_banks_by_region(region) if b != bank]

        suggestions.append({
            'title': 'Peer Group Comparison',
            'description': f'Compare {bank_catalog.get_bank_display_name(bank)} with other {region} banks: {", ".join(peer_banks[:3])}',
            'action': 'Compare with peers'
        })

    # Suggestion 3: Correlation analysis
    if metrics and len(metrics) > 1:
        suggestions.append({
            'title': 'Metric Correlation',
            'description': f'Analyze correlation between {len(metrics)} selected metrics',
            'action': 'View correlations'
        })

    # Suggestion 4: Risk metrics focus
    risk_metrics = [m for m in metrics if metric_catalog.is_risk_metric(m)] if metrics else []
    if not risk_metrics and metrics:
        suggestions.append({
            'title': 'Add Risk Metrics',
            'description': 'Consider adding risk-related metrics like NPE or defaulted exposures for better risk assessment',
            'action': 'Browse risk metrics'
        })

    # Render suggestions
    for idx, suggestion in enumerate(suggestions):
        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"**{suggestion['title']}**")
                st.caption(suggestion['description'])

            with col2:
                if st.button("→", key=f"suggestion_{idx}", use_container_width=True):
                    st.session_state[f"suggestion_{idx}"] = True
                    st.info(f"Action: {suggestion['action']}")

            st.divider()
