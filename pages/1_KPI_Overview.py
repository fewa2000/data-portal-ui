"""
KPI Overview Page
Displays high-level KPIs and trends.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services import api

st.set_page_config(page_title="KPI Overview", page_icon="📈", layout="wide")
st.title("KPI Overview")

# Fetch KPIs from API
kpis = api.get_kpis()

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${kpis['total_revenue']:,.0f}")
col2.metric("Total Orders", f"{kpis['total_orders']:,}")
col3.metric("Avg Order Value", f"${kpis['avg_order_value']:.2f}")
col4.metric("Active Customers", f"{kpis['active_customers']:,}")

st.divider()

# Fetch and display trends
st.subheader("Monthly Trends")
trends = api.get_kpi_trends()

col1, col2 = st.columns(2)
with col1:
    st.line_chart(trends.set_index("month")["revenue"], y_label="Revenue ($)")
with col2:
    st.line_chart(trends.set_index("month")["orders"], y_label="Orders")
