"""Metric information and categorization utilities."""
import config


def get_metric_category(metric_label, sheet_name):
    """Get the category for a metric based on its sheet."""
    for category, sheet_prefix in config.METRIC_CATEGORIES.items():
        if sheet_prefix in sheet_name:
            return category
    return "Other Metrics"


def get_metric_short_name(metric_label):
    """Get a shortened version of metric name for display."""
    # Remove common prefixes for cleaner display
    short_name = metric_label

    prefixes_to_remove = [
        "Original Exposure - ",
        "Exposure value - ",
        "Risk exposure amount - ",
        "Value adjustments and provisions - ",
        "Exposures with forbearance measures - ",
        "Gross carrying amount on ",
        "Accumulated impairment, accumulated changes in fair value due to credit risk and provisions on ",
        "Collaterals and financial guarantees received on non-performing exposures on "
    ]

    for prefix in prefixes_to_remove:
        if short_name.startswith(prefix):
            short_name = short_name[len(prefix):]
            break

    return short_name


def is_exposure_metric(metric_label):
    """Check if metric is an exposure-related metric."""
    exposure_keywords = ['Exposure', 'exposure']
    return any(keyword in metric_label for keyword in exposure_keywords)


def is_risk_metric(metric_label):
    """Check if metric is a risk-related metric."""
    risk_keywords = ['Risk', 'risk', 'NPE', 'Non-performing', 'Defaulted']
    return any(keyword in metric_label for keyword in risk_keywords)


def is_impairment_metric(metric_label):
    """Check if metric is an impairment/provision metric."""
    impairment_keywords = ['impairment', 'provision', 'Impairment', 'Provision']
    return any(keyword in metric_label for keyword in impairment_keywords)


def is_collateral_metric(metric_label):
    """Check if metric is a collateral-related metric."""
    collateral_keywords = ['Collateral', 'collateral', 'guarantee']
    return any(keyword in metric_label for keyword in collateral_keywords)


def get_metric_type_tags(metric_label):
    """Get type tags for a metric."""
    tags = []

    if is_exposure_metric(metric_label):
        tags.append("Exposure")
    if is_risk_metric(metric_label):
        tags.append("Risk")
    if is_impairment_metric(metric_label):
        tags.append("Impairment")
    if is_collateral_metric(metric_label):
        tags.append("Collateral")

    return tags if tags else ["General"]


def search_metrics(metrics_list, search_term):
    """Search metrics by keyword."""
    if not search_term:
        return metrics_list

    search_term_lower = search_term.lower()
    return [m for m in metrics_list if search_term_lower in m.lower()]
