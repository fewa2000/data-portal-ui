"""
Drilldown Page
Allows drilling down into data by different dimensions.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services import api

st.set_page_config(page_title="Drilldown", page_icon="🔍", layout="wide")
st.title("Drilldown")

# Fetch available dimensions
dimensions = api.get_dimensions()

# Dimension selector
selected_dimension = st.selectbox("Select Dimension", dimensions, format_func=str.title)

# Fetch and display drilldown data
data = api.get_drilldown_data(selected_dimension)

if not data.empty:
    st.subheader(f"Breakdown by {selected_dimension.title()}")

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(data.set_index(selected_dimension)["revenue"])
    with col2:
        st.dataframe(data, use_container_width=True, hide_index=True)
else:
    st.warning("No data available for this dimension.")
