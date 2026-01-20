"""
Run Form Component.
Form for configuring and executing analytical runs.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services import api


def render_run_form(business_case: str) -> dict | None:
    """
    Render the run configuration form.

    Args:
        business_case: The current business case

    Returns:
        Dictionary with run parameters if form is submitted, None otherwise
    """
    st.subheader("Configure Run")

    # Get available options from API
    periods = api.get_available_periods()
    scenarios = api.get_available_scenarios()

    # Form inputs
    col1, col2 = st.columns(2)

    with col1:
        # Default to most recent period
        default_period_idx = len(periods) - 1
        selected_period = st.selectbox(
            "Period",
            periods,
            index=default_period_idx,
            help="Select the time period for analysis"
        )

    with col2:
        selected_scenario = st.selectbox(
            "Scenario",
            scenarios,
            format_func=str.title,
            help="Select the scenario type"
        )

    # Display current configuration
    st.info(f"Run configuration: **{business_case.title()}** - {selected_period} - {selected_scenario.title()}")

    # Submit button
    if st.button("Start Run", type="primary", use_container_width=True):
        return {
            "period": selected_period,
            "scenario": selected_scenario,
        }

    return None
