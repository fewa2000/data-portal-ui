"""
Input Section Page.
Allows users to see and select available input data sources.

Inputs are NOT executed here - they are selected for use in Dashboards.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services import api, state

# Page configuration
st.set_page_config(
    page_title="Input | Data Portal",
    page_icon="📥",
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
        st.rerun()

    st.divider()

    selected_inputs = state.get_selected_inputs()
    st.caption(f"Selected inputs: {len(selected_inputs)}")

    run_count = state.get_run_count()
    st.caption(f"Total runs: {run_count}")

# =============================================================================
# Main Content
# =============================================================================

st.title("Input")

# Display current business case
bc_display = state.get_business_case().title()
st.markdown(f"**Business Case:** {bc_display}")

st.markdown("---")

st.markdown("""
Select the input data sources for your next analytical run.
These inputs will be used when you execute a run in the Dashboards section.
""")

st.info("These inputs will be used for the next run.")

# Get available inputs for current business case
business_case = state.get_business_case()
available_inputs = api.get_inputs(business_case)
selected_input_ids = state.get_selected_inputs()

# Group inputs by type
file_inputs = [i for i in available_inputs if i["type"] == "file"]
database_inputs = [i for i in available_inputs if i["type"] == "database"]

# =============================================================================
# File Inputs
# =============================================================================

st.subheader("File Inputs")
st.caption("Uploaded CSV and Excel files")

if file_inputs:
    for input_item in file_inputs:
        input_id = input_item["id"]
        is_selected = input_id in selected_input_ids

        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            checked = st.checkbox(
                label=input_item["name"],
                value=is_selected,
                key=f"input_{input_id}",
                label_visibility="collapsed",
            )
        with col2:
            st.markdown(f"**{input_item['name']}**")
            st.caption(input_item["description"])

        # Update state based on checkbox
        if checked and input_id not in selected_input_ids:
            state.add_selected_input(input_id)
            st.rerun()
        elif not checked and input_id in selected_input_ids:
            state.remove_selected_input(input_id)
            st.rerun()
else:
    st.caption("No file inputs available for this business case.")

st.divider()

# =============================================================================
# Database Inputs
# =============================================================================

st.subheader("Database Tables")
st.caption("Available database tables")

if database_inputs:
    for input_item in database_inputs:
        input_id = input_item["id"]
        is_selected = input_id in selected_input_ids

        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            checked = st.checkbox(
                label=input_item["name"],
                value=is_selected,
                key=f"input_{input_id}",
                label_visibility="collapsed",
            )
        with col2:
            st.markdown(f"**{input_item['name']}**")
            st.caption(input_item["description"])

        # Update state based on checkbox
        if checked and input_id not in selected_input_ids:
            state.add_selected_input(input_id)
            st.rerun()
        elif not checked and input_id in selected_input_ids:
            state.remove_selected_input(input_id)
            st.rerun()
else:
    st.caption("No database inputs available for this business case.")

st.divider()

# =============================================================================
# Selection Summary
# =============================================================================

st.subheader("Selection Summary")

selected_input_ids = state.get_selected_inputs()  # Refresh after any changes
selected_names = [i["name"] for i in available_inputs if i["id"] in selected_input_ids]

if selected_names:
    st.success(f"**{len(selected_names)} input(s) selected:**")
    for name in selected_names:
        st.markdown(f"- {name}")
else:
    st.warning("No inputs selected. Please select at least one input source.")

# Navigation hint
st.markdown("---")
st.markdown("Ready to run? Go to **Dashboards** to configure and execute your analysis.")
st.page_link("pages/2_Dashboards.py", label="Go to Dashboards", icon="📈")
