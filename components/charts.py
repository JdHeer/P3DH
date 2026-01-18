"""Chart rendering components."""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import config
from src import metric_catalog


def render_line_chart(df, title, x_col='Period', y_cols=None, height=None):
    """Render interactive line chart."""
    if df is None or df.empty:
        st.warning("No data available for chart")
        return

    height = height or config.DEFAULT_CHART_HEIGHT

    fig = go.Figure()

    if y_cols is None:
        y_cols = [col for col in df.columns if col != x_col]

    for idx, col in enumerate(y_cols):
        if col in df.columns:
            color = config.CHART_COLORS[idx % len(config.CHART_COLORS)]
            fig.add_trace(go.Scatter(
                x=df.index if x_col == 'Period' else df[x_col],
                y=df[col],
                mode='lines+markers',
                name=col,
                line={'color': color, 'width': 3},
                marker={'size': 10}
            ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 20}},
        xaxis_title=x_col,
        yaxis_title="Amount",
        height=height,
        hovermode='x unified',
        showlegend=True,
        legend={
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.02,
            'xanchor': "right",
            'x': 1
        },
        yaxis={'rangemode': 'tozero'},
        font={'size': 14}
    )

    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(df, title, x_col, y_col, orientation='v', height=None):
    """Render bar chart."""
    if df is None or df.empty:
        st.warning("No data available for chart")
        return

    height = height or config.DEFAULT_CHART_HEIGHT

    # Generate distinct colors for each bar
    import plotly.colors as pc
    n_bars = len(df)
    colors = pc.sample_colorscale("Viridis", [i/(n_bars-1) if n_bars > 1 else 0.5 for i in range(n_bars)])

    fig = px.bar(
        df,
        x=x_col if orientation == 'v' else y_col,
        y=y_col if orientation == 'v' else x_col,
        orientation=orientation,
        title=title,
        color=df.index,
        color_discrete_sequence=colors,
        text=y_col if orientation == 'v' else x_col
    )

    # Format numbers: show in thousands for large values
    def format_number(val):
        if val >= 1000:
            return f'{val/1000:.0f}k'
        return f'{val:.0f}'

    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        customdata=df[y_col if orientation == 'v' else x_col].apply(format_number)
    )

    # Update text to show formatted values
    for trace in fig.data:
        values = trace.y if orientation == 'v' else trace.x
        trace.text = [format_number(v) for v in values]

    fig.update_layout(
        height=height,
        showlegend=False,
        xaxis_title=x_col if orientation == 'v' else y_col,
        yaxis_title=y_col if orientation == 'v' else x_col,
        title={'text': title, 'font': {'size': 20}},
        yaxis={'rangemode': 'tozero'} if orientation == 'v' else {},
        xaxis={'rangemode': 'tozero'} if orientation == 'h' else {},
        font={'size': 14}
    )

    # Format axis labels to show thousands
    if orientation == 'v':
        fig.update_yaxes(tickformat='.0f')
    else:
        fig.update_xaxes(tickformat='.0f')

    st.plotly_chart(fig, use_container_width=True)


def render_grouped_bar_chart(df, title, height=None):
    """Render grouped bar chart for multi-bank comparison."""
    if df is None or df.empty:
        st.warning("No data available for chart")
        return

    height = height or config.DEFAULT_CHART_HEIGHT

    fig = go.Figure()

    for idx, col in enumerate(df.columns):
        color = config.CHART_COLORS[idx % len(config.CHART_COLORS)]
        fig.add_trace(go.Bar(
            name=col,
            x=df.index,
            y=df[col],
            marker_color=color
        ))

    fig.update_layout(
        title=title,
        barmode='group',
        height=height,
        xaxis_title="Period",
        yaxis_title="Amount",
        legend={
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.02,
            'xanchor': "right",
            'x': 1
        }
    )

    st.plotly_chart(fig, use_container_width=True)


def render_heatmap(df, title, height=None):
    """Render heatmap for banks x metrics comparison."""
    if df is None or df.empty:
        st.warning("No data available for heatmap")
        return

    height = height or config.DEFAULT_CHART_HEIGHT

    # Format hover text
    hover_text = []
    for i, row_label in enumerate(df.index):
        hover_row = []
        for j, col_label in enumerate(df.columns):
            value = df.iloc[i, j]
            hover_row.append(
                f"Metric: {metric_catalog.get_metric_short_name(row_label)}<br>"
                f"Bank: {col_label}<br>"
                f"Amount: {value:,.0f}"
            )
        hover_text.append(hover_row)

    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        x=df.columns,
        y=[metric_catalog.get_metric_short_name(m) for m in df.index],
        colorscale='Viridis',
        hovertemplate='%{text}<extra></extra>',
        text=hover_text,
        colorbar={'title': "Amount"}
    ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 20}},
        height=height,
        xaxis_title="Banks",
        yaxis_title="Metrics",
        font={'size': 14}
    )

    st.plotly_chart(fig, use_container_width=True)


def render_comparison_table(df, title="Data Table"):
    """Render formatted data table."""
    if df is None or df.empty:
        st.warning("No data available")
        return

    st.subheader(title)

    # Format numeric columns
    formatted_df = df.copy()
    for col in formatted_df.select_dtypes(include=['float64', 'int64']).columns:
        formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:,.2f}")

    st.dataframe(formatted_df, use_container_width=True, height=400)


def render_statistics_card(stats_dict, title="Statistics"):
    """Render statistics as a card."""
    st.subheader(title)

    cols = st.columns(len(stats_dict))

    for col, (label, value) in zip(cols, stats_dict.items(), strict=False):
        with col:
            if isinstance(value, (int, float)):
                st.metric(label.replace('_', ' ').title(), f"{value:,.2f}")
            else:
                st.metric(label.replace('_', ' ').title(), str(value))


def render_period_change_chart(df, title, height=None):
    """Render period-over-period change chart."""
    if df is None or df.empty:
        st.warning("No data available for change chart")
        return

    height = height or config.DEFAULT_CHART_HEIGHT

    fig = go.Figure()

    for idx, col in enumerate(df.columns):
        color = config.CHART_COLORS[idx % len(config.CHART_COLORS)]
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[col],
            mode='lines+markers',
            name=col,
            line={'color': color, 'width': 2},
            marker={'size': 8},
            hovertemplate='%{y:.2f}%<extra></extra>'
        ))

    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        title=title,
        xaxis_title="Period",
        yaxis_title="Change (%)",
        height=height,
        hovermode='x unified',
        showlegend=True,
        legend={
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.02,
            'xanchor': "right",
            'x': 1
        }
    )

    st.plotly_chart(fig, use_container_width=True)


def render_multi_metric_comparison(df_dict, bank_name, height=None):
    """Render multiple metrics for a single bank."""
    if not df_dict:
        st.warning("No data available")
        return

    height = height or config.DEFAULT_CHART_HEIGHT

    # Create subplots
    n_metrics = len(df_dict)
    rows = (n_metrics + 1) // 2

    fig = make_subplots(
        rows=rows,
        cols=2,
        subplot_titles=list(df_dict.keys())
    )

    for idx, (metric, df) in enumerate(df_dict.items()):
        row = idx // 2 + 1
        col = idx % 2 + 1

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.values,
                mode='lines+markers',
                name=metric,
                showlegend=False
            ),
            row=row,
            col=col
        )

    fig.update_layout(
        title=f"Multiple Metrics Comparison - {bank_name}",
        height=height * rows // 2,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
