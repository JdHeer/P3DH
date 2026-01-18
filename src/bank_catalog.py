"""Bank information and grouping utilities."""
from . import config

# Full country names for NSA codes
BANK_NAMES = {
    "AT": "Austria",
    "BE": "Belgium",
    "CY": "Cyprus",
    "DE": "Germany",
    "DK": "Denmark",
    "EE": "Estonia",
    "ES": "Spain",
    "FI": "Finland",
    "FR": "France",
    "GR": "Greece",
    "HU": "Hungary",
    "IE": "Ireland",
    "IT": "Italy",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "MT": "Malta",
    "NL": "Netherlands",
    "NO": "Norway",
    "OT": "Other",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SE": "Sweden",
    "SI": "Slovenia"
}


def get_bank_display_name(nsa_code):
    """Get full country name for NSA code."""
    return BANK_NAMES.get(nsa_code, nsa_code)


def get_banks_by_region(region=None):
    """Get list of banks in a specific region or all regions."""
    if region and region in config.BANK_REGIONS:
        return config.BANK_REGIONS[region]
    return config.BANK_REGIONS


def get_region_for_bank(nsa_code):
    """Get the region for a specific bank."""
    for region, banks in config.BANK_REGIONS.items():
        if nsa_code in banks:
            return region
    return "Other"


def format_bank_list(banks):
    """Format list of banks with full names."""
    return [f"{bank} - {get_bank_display_name(bank)}" for bank in banks]


def get_all_banks_sorted():
    """Get all banks sorted alphabetically."""
    return sorted(BANK_NAMES.keys())
