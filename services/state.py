"""
Session state management for the Data Portal.
Centralizes all state access and initialization.

This module provides a clean interface for managing:
- Selected business case
- Selected inputs per business case
- Executed runs

TODO: When backend is available, runs should be persisted via API.
"""

import streamlit as st
from typing import Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from models.run import Run, RunStatus


# Business case constants
BUSINESS_CASES = ["sales", "procurement", "finance"]
DEFAULT_BUSINESS_CASE = "sales"


def init_state() -> None:
    """
    Initialize all session state variables.
    Call this at the start of each page.
    """
    if "selected_business_case" not in st.session_state:
        st.session_state.selected_business_case = DEFAULT_BUSINESS_CASE

    if "selected_inputs" not in st.session_state:
        # Dict mapping business_case -> list of selected input IDs
        st.session_state.selected_inputs = {bc: [] for bc in BUSINESS_CASES}

    if "runs" not in st.session_state:
        # List of Run objects
        st.session_state.runs = []


# Business Case Management

def get_business_case() -> str:
    """Get the currently selected business case."""
    init_state()
    return st.session_state.selected_business_case


def set_business_case(business_case: str) -> None:
    """Set the selected business case."""
    if business_case in BUSINESS_CASES:
        st.session_state.selected_business_case = business_case


def get_business_cases() -> list[str]:
    """Get all available business cases."""
    return BUSINESS_CASES.copy()


# Input Selection Management

def get_selected_inputs(business_case: str | None = None) -> list[str]:
    """
    Get selected inputs for a business case.
    Uses current business case if not specified.
    """
    init_state()
    bc = business_case or get_business_case()
    return st.session_state.selected_inputs.get(bc, [])


def set_selected_inputs(inputs: list[str], business_case: str | None = None) -> None:
    """
    Set selected inputs for a business case.
    Uses current business case if not specified.
    """
    init_state()
    bc = business_case or get_business_case()
    st.session_state.selected_inputs[bc] = inputs


def add_selected_input(input_id: str, business_case: str | None = None) -> None:
    """Add an input to the selected inputs."""
    init_state()
    bc = business_case or get_business_case()
    if input_id not in st.session_state.selected_inputs[bc]:
        st.session_state.selected_inputs[bc].append(input_id)


def remove_selected_input(input_id: str, business_case: str | None = None) -> None:
    """Remove an input from the selected inputs."""
    init_state()
    bc = business_case or get_business_case()
    if input_id in st.session_state.selected_inputs[bc]:
        st.session_state.selected_inputs[bc].remove(input_id)


# Run Management

def get_runs(business_case: str | None = None) -> list[Run]:
    """
    Get all runs, optionally filtered by business case.
    Returns runs sorted by execution time (newest first).
    """
    init_state()
    runs = st.session_state.runs

    if business_case:
        runs = [r for r in runs if r.business_case == business_case]

    # Sort by executed_at descending
    runs = sorted(runs, key=lambda r: r.executed_at, reverse=True)
    return runs


def get_completed_runs(business_case: str | None = None) -> list[Run]:
    """Get only completed runs."""
    runs = get_runs(business_case)
    return [r for r in runs if r.status == RunStatus.COMPLETED]


def add_run(run: Run) -> None:
    """Add a run to the state."""
    init_state()
    st.session_state.runs.append(run)


def get_run_by_id(run_id: str) -> Run | None:
    """Get a specific run by ID."""
    init_state()
    for run in st.session_state.runs:
        if run.id == run_id:
            return run
    return None


def update_run(run: Run) -> None:
    """Update an existing run in state."""
    init_state()
    for i, r in enumerate(st.session_state.runs):
        if r.id == run.id:
            st.session_state.runs[i] = run
            return


# Utility Functions

def clear_runs() -> None:
    """Clear all runs. Use with caution."""
    init_state()
    st.session_state.runs = []


def get_run_count(business_case: str | None = None) -> int:
    """Get the count of runs."""
    return len(get_runs(business_case))
