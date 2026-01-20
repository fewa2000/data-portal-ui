"""
Session state management for the Data Portal.
Centralizes all state access and initialization.

This module provides a clean interface for managing:
- Selected domain (Sales / Procurement / Finance)
- Executed runs

The portal is DOMAIN-DRIVEN:
- Domains define what is possible
- Tables are NOT user-selected
- Filters are domain-specific

TODO: When backend is available, runs should be persisted via API.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from models.run import Run, RunStatus


# Domain constants
DOMAINS = ["sales", "procurement", "finance"]
DEFAULT_DOMAIN = "sales"


def init_state() -> None:
    """
    Initialize all session state variables.
    Call this at the start of each page.
    """
    if "selected_domain" not in st.session_state:
        st.session_state.selected_domain = DEFAULT_DOMAIN

    if "runs" not in st.session_state:
        # List of Run objects
        st.session_state.runs = []

    if "current_run_id" not in st.session_state:
        st.session_state.current_run_id = None


# Domain Management

def get_domain() -> str:
    """Get the currently selected domain."""
    init_state()
    return st.session_state.selected_domain


def set_domain(domain: str) -> None:
    """Set the selected domain."""
    if domain in DOMAINS:
        st.session_state.selected_domain = domain


def get_domains() -> list[str]:
    """Get all available domains."""
    return DOMAINS.copy()


# Run Management

def get_runs(domain: str | None = None) -> list[Run]:
    """
    Get all runs, optionally filtered by domain.
    Returns runs sorted by execution time (newest first).
    """
    init_state()
    runs = st.session_state.runs

    if domain:
        runs = [r for r in runs if r.domain == domain]

    # Sort by executed_at descending
    runs = sorted(runs, key=lambda r: r.executed_at, reverse=True)
    return runs


def get_completed_runs(domain: str | None = None) -> list[Run]:
    """Get only completed runs."""
    runs = get_runs(domain)
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


# Current Run Management

def get_current_run_id() -> str | None:
    """Get the ID of the currently displayed run."""
    init_state()
    return st.session_state.current_run_id


def set_current_run_id(run_id: str | None) -> None:
    """Set the ID of the currently displayed run."""
    init_state()
    st.session_state.current_run_id = run_id


def clear_current_run() -> None:
    """Clear the current run display."""
    init_state()
    st.session_state.current_run_id = None


# Utility Functions

def clear_runs() -> None:
    """Clear all runs. Use with caution."""
    init_state()
    st.session_state.runs = []
    st.session_state.current_run_id = None


def get_run_count(domain: str | None = None) -> int:
    """Get the count of runs."""
    return len(get_runs(domain))
