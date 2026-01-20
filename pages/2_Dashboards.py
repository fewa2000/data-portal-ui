"""
Dashboards Section Page.
Define, execute, and view analytical runs.

A RUN is a concrete analytical scenario defined by:
- Business case (Sales / Procurement / Finance)
- Parameters (period, scenario, etc.)
- Execution timestamp
- Results (KPIs, charts)
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services import api, state
from models.run import Run, RunParameters, RunStatus
from components.run_form import render_run_form
from components.result_charts import render_run_results

# Page configuration
st.set_page_config(
    page_title="Dashboards | Data Portal",
    page_icon="📈",
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
        # Clear current run results when switching business case
        if "current_run_id" in st.session_state:
            del st.session_state.current_run_id
        st.rerun()

    st.divider()

    selected_inputs = state.get_selected_inputs()
    st.caption(f"Selected inputs: {len(selected_inputs)}")

    run_count = state.get_run_count()
    st.caption(f"Total runs: {run_count}")

# =============================================================================
# Main Content
# =============================================================================

st.title("Dashboards")

# Display current business case
business_case = state.get_business_case()
bc_display = business_case.title()
st.markdown(f"**Business Case:** {bc_display}")

st.markdown("---")

# Check if inputs are selected
selected_inputs = state.get_selected_inputs()
if not selected_inputs:
    st.warning("No inputs selected. Please select inputs in the Input section first.")
    st.page_link("pages/1_Input.py", label="Go to Input", icon="📥")
    st.stop()

# =============================================================================
# Run Configuration Form
# =============================================================================

parameters = render_run_form(business_case)

# =============================================================================
# Run Execution
# =============================================================================

if parameters:
    # Create a new run
    run = Run(
        business_case=business_case,
        parameters=RunParameters(
            period=parameters["period"],
            scenario=parameters["scenario"],
        ),
        status=RunStatus.RUNNING,
    )

    # Execute the run via mock API
    # TODO: Replace with actual API call when backend is available
    with st.spinner(f"Executing run: {run.display_name}..."):
        results = api.execute_run(business_case, parameters)

    # Update run with results
    run.status = RunStatus.COMPLETED
    run.results = results

    # Store run in state
    state.add_run(run)

    # Store current run ID for display
    st.session_state.current_run_id = run.id

    st.success(f"Run completed: **{run.display_name}**")
    st.rerun()

# =============================================================================
# Display Current Run Results
# =============================================================================

if "current_run_id" in st.session_state:
    current_run = state.get_run_by_id(st.session_state.current_run_id)

    if current_run and current_run.status == RunStatus.COMPLETED:
        st.divider()
        st.subheader(f"Results: {current_run.display_name}")
        st.caption(f"Executed at: {current_run.executed_at_formatted}")

        render_run_results(current_run.results, current_run.business_case)

        # Option to clear current results
        if st.button("Clear Results", type="secondary"):
            del st.session_state.current_run_id
            st.rerun()
else:
    # Show recent runs for this business case
    recent_runs = state.get_completed_runs(business_case)

    if recent_runs:
        st.divider()
        st.subheader("Recent Runs")
        st.caption("Click on a run to view its results.")

        for run in recent_runs[:5]:  # Show last 5 runs
            with st.expander(f"{run.display_name} - {run.executed_at_formatted}"):
                if st.button("View Results", key=f"view_{run.id}"):
                    st.session_state.current_run_id = run.id
                    st.rerun()
    else:
        st.info("No runs executed yet for this business case. Configure a run above and click 'Start Run'.")
