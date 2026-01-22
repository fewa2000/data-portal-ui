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
from services import api, state
from models.run import RunStatus
from components.result_charts import render_run_results
from components.db_status import render_db_status
from components.data_source_badge import render_results_source

# Page configuration
st.set_page_config(
    page_title="Archive | Data Portal",
    page_icon="📁",
    layout="wide",
)

# Initialize state
state.init_state()

# =============================================================================
# Sidebar - Domain Selector (consistent across all pages)
# =============================================================================

with st.sidebar:
    st.header("Domain")

    domains = state.get_domains()
    current_domain = state.get_domain()

    selected_domain = st.radio(
        "Select Domain",
        domains,
        format_func=str.title,
        index=domains.index(current_domain),
        label_visibility="collapsed",
    )

    if selected_domain != current_domain:
        state.set_domain(selected_domain)
        # Clear selected archive run when switching domain
        if "archive_run_id" in st.session_state:
            del st.session_state.archive_run_id
        st.rerun()

    st.divider()

    run_count = state.get_run_count()
    st.caption(f"Total runs: {run_count}")

    # Filter option
    st.divider()
    st.subheader("Filter")
    show_all = st.checkbox("Show all domains", value=False)

    st.divider()
    render_db_status()

# =============================================================================
# Main Content
# =============================================================================

st.title("Archive")

# Display current domain
domain = state.get_domain()
domain_display = domain.title()

if show_all:
    st.markdown("**Showing runs from all domains**")
else:
    st.markdown(f"**Domain:** {domain_display}")

st.markdown("---")

# Get completed runs
if show_all:
    completed_runs = state.get_completed_runs()
else:
    completed_runs = state.get_completed_runs(domain)

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
            st.markdown(f"**{run.domain.title()}**")
            st.caption(run.get_filter_summary())

        with col2:
            st.caption(f"Domain: {run.domain.title()}")

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

        # Get table info for source badge
        run_table_info = api.DOMAIN_TABLES.get(selected_run.domain, {})
        run_table_name = run_table_info.get("table", "unknown")

        # Run header with clear identification
        st.subheader(f"Results: {selected_run.domain.title()}")
        render_results_source(run_table_name, "Aggregation with GROUP BY")

        # Run metadata
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Domain:** {selected_run.domain.title()}")
        with col2:
            st.markdown(f"**Executed:** {selected_run.executed_at_formatted}")

        st.markdown(f"**Filters:** {selected_run.get_filter_summary()}")
        st.caption(f"Run ID: {selected_run.id}")

        # SQL Preview
        if selected_run.sql_preview:
            with st.expander("SQL Query (for transparency)", expanded=False):
                st.code(selected_run.sql_preview, language="sql")

        st.divider()

        # Render results using shared component
        render_run_results(selected_run.results, selected_run.domain)

        # Close button
        if st.button("Close Results", type="secondary"):
            del st.session_state.archive_run_id
            st.rerun()
