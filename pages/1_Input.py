"""
Input Section Page.
Shows domain data sources for TRANSPARENCY.

Tables are NOT user-selected - they are defined by the domain.
This section shows:
- Which gold table is used for the domain
- Schema information
- Sample data preview (mocked)

No execution happens here.
"""

import streamlit as st
import pandas as pd
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
        st.rerun()

    st.divider()

    run_count = state.get_run_count()
    st.caption(f"Total runs: {run_count}")

# =============================================================================
# Main Content
# =============================================================================

st.title("Input")

# Display current domain
domain = state.get_domain()
domain_display = domain.title()
st.markdown(f"**Domain:** {domain_display}")

st.markdown("---")

st.info(
    "This section shows the data source used for this domain. "
    "Tables are defined by the domain - they are NOT user-selectable."
)

# Get domain table information
table_info = api.get_domain_table_info(domain)

if not table_info:
    st.warning("No table information available for this domain.")
    st.stop()

# =============================================================================
# Gold Table Information
# =============================================================================

st.subheader("Gold Table")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"**Table Name:**")
    st.code(table_info["table"])

with col2:
    st.markdown(f"**Description:**")
    st.markdown(table_info["description"])

st.divider()

# =============================================================================
# Schema Information
# =============================================================================

st.subheader("Schema")

schema_data = table_info.get("schema", [])
if schema_data:
    schema_df = pd.DataFrame(schema_data)
    schema_df.columns = ["Column", "Type", "Description"]
    st.dataframe(schema_df, use_container_width=True, hide_index=True)
else:
    st.caption("No schema information available.")

st.divider()

# =============================================================================
# Sample Data Preview
# =============================================================================

st.subheader("Sample Data Preview")
st.caption("First 3 rows (mocked for demonstration)")

sample_rows = table_info.get("sample_rows", [])
if sample_rows:
    sample_df = pd.DataFrame(sample_rows)
    st.dataframe(sample_df, use_container_width=True, hide_index=True)
else:
    st.caption("No sample data available.")

# =============================================================================
# Available Filters
# =============================================================================

st.divider()
st.subheader("Available Filters")
st.caption("These filters will be available in the Dashboards section.")

filter_options = api.get_filter_options(domain)

if filter_options:
    for filter_name, options in filter_options.items():
        display_name = filter_name.replace("_", " ").title()
        st.markdown(f"**{display_name}:** {', '.join(str(o) for o in options[:5])}" +
                   (f" (+{len(options) - 5} more)" if len(options) > 5 else ""))
else:
    st.caption("No filter options available.")

# Navigation hint
st.markdown("---")
st.markdown("Ready to run? Go to **Dashboards** to configure filters and execute your analysis.")
st.page_link("pages/2_Dashboards.py", label="Go to Dashboards", icon="📈")
