"""Entry point for running the dashboard via CLI."""

import sys

from streamlit.web import cli as stcli


def main():
    """Run the Streamlit dashboard."""
    sys.argv = ["streamlit", "run", "Compare.py"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
