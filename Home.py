"""
Data Portal UI - Main Entry Point

This is the home page with navigation and business case selection.
"""

import streamlit as st
from services import state

# Page configuration
st.set_page_config(
    page_title="Data Portal",
    page_icon="📊",
    layout="wide",
)

# Initialize state
state.init_state()

# =============================================================================
# Sidebar - Business Case Selector
# =============================================================================

with st.sidebar:
    st.header("Business Case")

    # Get available business cases
    business_cases = state.get_business_cases()
    current_bc = state.get_business_case()

    # Radio buttons for business case selection
    selected_bc = st.radio(
        "Select Business Case",
        business_cases,
        format_func=str.title,
        index=business_cases.index(current_bc),
        label_visibility="collapsed",
    )

    # Update state if changed
    if selected_bc != current_bc:
        state.set_business_case(selected_bc)
        st.rerun()

    st.divider()

    # Show selected inputs count
    selected_inputs = state.get_selected_inputs()
    st.caption(f"Selected inputs: {len(selected_inputs)}")

    # Show runs count
    run_count = state.get_run_count()
    st.caption(f"Total runs: {run_count}")

# =============================================================================
# Main Content
# =============================================================================

st.title("Data Portal")

# Display current business case prominently
bc_display = state.get_business_case().title()
st.markdown(f"### Current Business Case: **{bc_display}**")

st.markdown("---")

st.markdown("""
Welcome to the Data Portal. This application allows you to:

1. **Input** - Select and configure input data sources
2. **Dashboards** - Create and execute analytical runs
3. **Archive** - View historical run results

Use the **sidebar** to:
- Select your business case (Sales, Procurement, Finance)
- Navigate between sections using the page links
""")

# Navigation cards
st.markdown("### Quick Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Input")
    st.markdown("Select data sources for your next run.")
    st.page_link("pages/1_Input.py", label="Go to Input", icon="📥")

with col2:
    st.markdown("#### Dashboards")
    st.markdown("Configure and execute analytical runs.")
    st.page_link("pages/2_Dashboards.py", label="Go to Dashboards", icon="📈")

with col3:
    st.markdown("#### Archive")
    st.markdown("View historical run results.")
    st.page_link("pages/3_Archive.py", label="Go to Archive", icon="📁")
