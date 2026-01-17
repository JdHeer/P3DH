"""Bank and metric selector components."""
import streamlit as st

import config
from src import bank_catalog, data_loader, data_processor, metric_catalog


def render_bank_selector(key_prefix="main"):
    """Render smart bank selector with regional grouping."""
    st.subheader("🏦 Select Banks")

    # Get available banks
    all_banks = data_loader.get_banks()

    # Selection mode
    selection_mode = st.radio(
        "Selection Mode:",
        ["By Region", "Individual Selection", "Quick Presets"],
        key=f"{key_prefix}_bank_mode",
        horizontal=True
    )

    selected_banks = []

    if selection_mode == "By Region":
        st.write("**Select regions to include:**")

        cols = st.columns(3)
        selected_regions = []

        for idx, (region, banks) in enumerate(config.BANK_REGIONS.items()):
            with cols[idx % 3]:
                if st.checkbox(
                    f"{region} ({len(banks)})",
                    key=f"{key_prefix}_region_{region}"
                ):
                    selected_regions.append(region)

        # Collect all banks from selected regions
        for region in selected_regions:
            selected_banks.extend(config.BANK_REGIONS[region])

        # Show selected banks
        if selected_banks:
            st.caption(f"Selected: {', '.join(sorted(set(selected_banks)))}")

    elif selection_mode == "Individual Selection":
        # Search box
        search_term = st.text_input(
            "🔍 Search banks:",
            key=f"{key_prefix}_bank_search"
        )

        # Filter banks
        filtered_banks = all_banks
        if search_term:
            search_lower = search_term.lower()
            filtered_banks = [
                b for b in all_banks
                if search_lower in b.lower() or
                   search_lower in bank_catalog.get_bank_display_name(b).lower()
            ]

        # Multi-select
        selected_banks = st.multiselect(
            "Select individual banks:",
            options=filtered_banks,
            format_func=lambda x: f"{x} - {bank_catalog.get_bank_display_name(x)}",
            key=f"{key_prefix}_bank_multiselect"
        )

    else:  # Quick Presets
        df = data_loader.load_data()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🌍 All Banks", key=f"{key_prefix}_all_banks"):
                selected_banks = all_banks

        with col2:
            if st.button("⭐ Top 10 by Exposure", key=f"{key_prefix}_top10"):
                if df is not None:
                    bank_sizes = data_processor.calculate_bank_sizes(df)
                    selected_banks = list(bank_sizes.keys())[:10]

        with col3:
            if st.button("🔵 Nordic Banks", key=f"{key_prefix}_nordic"):
                selected_banks = config.BANK_REGIONS["Nordic"]

        # Show current selection
        if selected_banks:
            st.info(f"**Selected:** {', '.join(selected_banks)}")

            # Allow modification
            selected_banks = st.multiselect(
                "Modify selection:",
                options=all_banks,
                default=selected_banks,
                format_func=lambda x: f"{x} - {bank_catalog.get_bank_display_name(x)}",
                key=f"{key_prefix}_preset_modify"
            )

    return list(set(selected_banks))  # Remove duplicates


def render_metric_selector(key_prefix="main"):
    """Render smart metric selector with category grouping."""
    st.subheader("📊 Select Metrics")

    df = data_loader.load_data()
    if df is None:
        st.error("Cannot load data")
        return []

    # Selection mode
    selection_mode = st.radio(
        "Selection Mode:",
        ["By Category", "Search & Select", "Quick Presets"],
        key=f"{key_prefix}_metric_mode",
        horizontal=True
    )

    selected_metrics = []

    if selection_mode == "By Category":
        metrics_by_sheet = data_processor.get_metrics_by_category(df)

        st.write("**Select categories and metrics:**")

        for sheet, metrics in sorted(metrics_by_sheet.items()):
            with st.expander(f"📁 {sheet} ({len(metrics)} metrics)"):
                # Select all in category
                if st.checkbox(
                    f"Select all {len(metrics)} metrics",
                    key=f"{key_prefix}_cat_all_{sheet}"
                ):
                    selected_metrics.extend(metrics)
                else:
                    # Individual selection with search
                    search = st.text_input(
                        "Filter metrics:",
                        key=f"{key_prefix}_cat_search_{sheet}"
                    )

                    filtered = metrics
                    if search:
                        filtered = metric_catalog.search_metrics(metrics, search)

                    selected = st.multiselect(
                        f"Select from {sheet}:",
                        options=filtered,
                        format_func=metric_catalog.get_metric_short_name,
                        key=f"{key_prefix}_cat_select_{sheet}"
                    )
                    selected_metrics.extend(selected)

    elif selection_mode == "Search & Select":
        all_metrics = data_loader.get_metrics()

        # Search box
        search_term = st.text_input(
            "🔍 Search metrics:",
            placeholder="e.g., exposure, risk, NPE, collateral",
            key=f"{key_prefix}_metric_search"
        )

        # Filter metrics
        filtered_metrics = all_metrics
        if search_term:
            filtered_metrics = metric_catalog.search_metrics(all_metrics, search_term)

        st.caption(f"Showing {len(filtered_metrics)} metrics")

        # Multi-select
        selected_metrics = st.multiselect(
            "Select metrics:",
            options=filtered_metrics,
            format_func=metric_catalog.get_metric_short_name,
            key=f"{key_prefix}_metric_multiselect"
        )

    else:  # Quick Presets
        all_metrics = data_loader.get_metrics()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💰 All Exposure Metrics", key=f"{key_prefix}_exposure"):
                selected_metrics = [m for m in all_metrics if metric_catalog.is_exposure_metric(m)]

        with col2:
            if st.button("⚠️ All Risk Metrics", key=f"{key_prefix}_risk"):
                selected_metrics = [m for m in all_metrics if metric_catalog.is_risk_metric(m)]

        with col3:
            if st.button("📉 All Impairment Metrics", key=f"{key_prefix}_impairment"):
                selected_metrics = [m for m in all_metrics if metric_catalog.is_impairment_metric(m)]

        # Show current selection
        if selected_metrics:
            st.info(f"**{len(selected_metrics)} metrics selected**")

            # Show first few
            with st.expander("View selected metrics"):
                for m in selected_metrics[:20]:
                    st.text(f"• {metric_catalog.get_metric_short_name(m)}")
                if len(selected_metrics) > 20:
                    st.caption(f"... and {len(selected_metrics) - 20} more")

            # Allow modification
            if st.checkbox("Modify selection", key=f"{key_prefix}_preset_modify_check"):
                selected_metrics = st.multiselect(
                    "Modify metrics:",
                    options=all_metrics,
                    default=selected_metrics,
                    format_func=metric_catalog.get_metric_short_name,
                    key=f"{key_prefix}_preset_modify"
                )

    return list(set(selected_metrics))  # Remove duplicates


def render_period_selector(key_prefix="main"):
    """Render period selector."""
    periods = data_loader.get_periods()

    if not periods:
        return []

    # Format periods for display
    period_labels = {p: p.strftime('%b %Y') for p in periods}

    st.subheader("📅 Select Time Period(s)")

    selection_type = st.radio(
        "Select:",
        ["Single Period", "Multiple Periods", "All Periods"],
        key=f"{key_prefix}_period_type",
        horizontal=True
    )

    if selection_type == "Single Period":
        selected = st.selectbox(
            "Period:",
            options=periods,
            format_func=lambda x: period_labels[x],
            index=len(periods) - 1,  # Default to latest
            key=f"{key_prefix}_period_single"
        )
        return [selected]

    elif selection_type == "Multiple Periods":
        selected = st.multiselect(
            "Periods:",
            options=periods,
            default=[periods[-1]],  # Default to latest
            format_func=lambda x: period_labels[x],
            key=f"{key_prefix}_period_multi"
        )
        return selected

    else:  # All Periods
        return periods


def render_action_buttons(banks, metrics, periods):
    """Render smart action buttons."""
    st.divider()
    st.subheader("🎯 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Compare Banks", use_container_width=True):
            if banks and metrics:
                st.session_state['action'] = 'compare_banks'
                st.session_state['compare_banks'] = banks
                st.session_state['compare_metric'] = metrics[0] if len(metrics) == 1 else None
                st.success("Switched to comparison view!")
            else:
                st.warning("Please select banks and at least one metric")

    with col2:
        if st.button("📈 Compare Metrics", use_container_width=True):
            if len(banks) == 1 and metrics:
                st.session_state['action'] = 'compare_metrics'
                st.session_state['compare_bank'] = banks[0]
                st.session_state['compare_metrics'] = metrics
                st.success("Switched to metric comparison!")
            else:
                st.warning("Please select exactly one bank and multiple metrics")

    with col3:
        if st.button("🔥 Show Heatmap", use_container_width=True):
            if banks and metrics and periods:
                st.session_state['action'] = 'heatmap'
                st.session_state['heatmap_banks'] = banks
                st.session_state['heatmap_metrics'] = metrics
                st.session_state['heatmap_period'] = periods[0] if periods else None
                st.success("Generating heatmap!")
            else:
                st.warning("Please select banks, metrics, and at least one period")
