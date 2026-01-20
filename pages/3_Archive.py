"""
Archive Section Page.
Provides access to previously executed runs.

Archived runs are:
- Clickable
- Re-openable
- Read-only

Uses the same result rendering logic as Dashboards.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services import state
from models.run import RunStatus
from components.result_charts import render_run_results

# Page configuration
st.set_page_config(
    page_title="Archive | Data Portal",
    page_icon="📁",
    layout="wide",
)

# Initialize state
state.init_state()

# =============================================================================
# Sidebar - Business Case Selector (consistent across all pages)
# =============================================================================

with st.sidebar:
    st.header("Business Case")

    business_cases = state.get_business_cases()
    current_bc = state.get_business_case()

    selected_bc = st.radio(
        "Select Business Case",
        business_cases,
        format_func=str.title,
        index=business_cases.index(current_bc),
        label_visibility="collapsed",
    )

    if selected_bc != current_bc:
        state.set_business_case(selected_bc)
        # Clear selected archive run when switching business case
        if "archive_run_id" in st.session_state:
            del st.session_state.archive_run_id
        st.rerun()

    st.divider()

    selected_inputs = state.get_selected_inputs()
    st.caption(f"Selected inputs: {len(selected_inputs)}")

    run_count = state.get_run_count()
    st.caption(f"Total runs: {run_count}")

    # Filter option
    st.divider()
    st.subheader("Filter")
    show_all = st.checkbox("Show all business cases", value=False)

# =============================================================================
# Main Content
# =============================================================================

st.title("Archive")

# Display current business case
business_case = state.get_business_case()
bc_display = business_case.title()

if show_all:
    st.markdown("**Showing runs from all business cases**")
else:
    st.markdown(f"**Business Case:** {bc_display}")

st.markdown("---")

# Get completed runs
if show_all:
    completed_runs = state.get_completed_runs()
else:
    completed_runs = state.get_completed_runs(business_case)

# =============================================================================
# Run List
# =============================================================================

if not completed_runs:
    st.info("No archived runs available. Execute runs in the Dashboards section to see them here.")
    st.page_link("pages/2_Dashboards.py", label="Go to Dashboards", icon="📈")
else:
    st.subheader(f"Completed Runs ({len(completed_runs)})")

    # Create a table-like view of runs
    for run in completed_runs:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        with col1:
            st.markdown(f"**{run.display_name}**")

        with col2:
            st.caption(f"Business Case: {run.business_case.title()}")

        with col3:
            st.caption(f"Executed: {run.executed_at_formatted}")

        with col4:
            if st.button("View", key=f"view_{run.id}"):
                st.session_state.archive_run_id = run.id
                st.rerun()

        st.divider()

# =============================================================================
# Display Selected Run Results
# =============================================================================

if "archive_run_id" in st.session_state:
    selected_run = state.get_run_by_id(st.session_state.archive_run_id)

    if selected_run:
        st.markdown("---")
        st.subheader(f"Results: {selected_run.display_name}")

        # Run metadata
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Business Case:** {selected_run.business_case.title()}")
        with col2:
            st.markdown(f"**Period:** {selected_run.parameters.period}")
        with col3:
            st.markdown(f"**Scenario:** {selected_run.parameters.scenario.title()}")

        st.caption(f"Executed at: {selected_run.executed_at_formatted}")
        st.caption(f"Run ID: {selected_run.id}")

        st.divider()

        # Render results using shared component
        render_run_results(selected_run.results, selected_run.business_case)

        # Close button
        if st.button("Close Results", type="secondary"):
            del st.session_state.archive_run_id
            st.rerun()
