"""
Data Portal UI - Main Entry Point

This is the home page with navigation and domain selection.
The portal is DOMAIN-DRIVEN - domains define what is possible.
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
# Sidebar - Domain Selector
# =============================================================================

with st.sidebar:
    st.header("Domain")

    # Get available domains
    domains = state.get_domains()
    current_domain = state.get_domain()

    # Radio buttons for domain selection
    selected_domain = st.radio(
        "Select Domain",
        domains,
        format_func=str.title,
        index=domains.index(current_domain),
        label_visibility="collapsed",
    )

    # Update state if changed
    if selected_domain != current_domain:
        state.set_domain(selected_domain)
        state.clear_current_run()
        st.rerun()

    st.divider()

    # Show runs count
    run_count = state.get_run_count()
    st.caption(f"Total runs: {run_count}")

# =============================================================================
# Main Content
# =============================================================================

st.title("Data Portal")

# Display current domain prominently
domain_display = state.get_domain().title()
st.markdown(f"### Current Domain: **{domain_display}**")

st.markdown("---")

st.markdown("""
Welcome to the Data Portal. This application allows you to:

1. **Input** - View domain data sources (read-only)
2. **Dashboards** - Define filters and execute analytical runs
3. **Archive** - View historical run results

Use the **sidebar** to select your domain (Sales, Procurement, Finance).
Each domain has specific filters that translate to SQL queries.
""")

# Navigation cards
st.markdown("### Quick Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Input")
    st.markdown("View domain tables and schema.")
    st.page_link("pages/1_Input.py", label="Go to Input", icon="📥")

with col2:
    st.markdown("#### Dashboards")
    st.markdown("Configure filters and execute runs.")
    st.page_link("pages/2_Dashboards.py", label="Go to Dashboards", icon="📈")

with col3:
    st.markdown("#### Archive")
    st.markdown("View historical run results.")
    st.page_link("pages/3_Archive.py", label="Go to Archive", icon="📁")
