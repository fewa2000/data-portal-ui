"""
KPI Cards Component.
Displays key performance indicators in a card layout.
"""

import streamlit as st
from typing import Any


# KPI display configuration per business case
_KPI_CONFIG = {
    "sales": {
        "total_revenue": {"label": "Total Revenue", "format": "${:,.0f}"},
        "total_orders": {"label": "Total Orders", "format": "{:,}"},
        "avg_order_value": {"label": "Avg Order Value", "format": "${:.2f}"},
        "conversion_rate": {"label": "Conversion Rate", "format": "{:.1f}%"},
    },
    "procurement": {
        "total_spend": {"label": "Total Spend", "format": "${:,.0f}"},
        "purchase_orders": {"label": "Purchase Orders", "format": "{:,}"},
        "avg_po_value": {"label": "Avg PO Value", "format": "${:.2f}"},
        "on_time_delivery": {"label": "On-Time Delivery", "format": "{:.1f}%"},
    },
    "finance": {
        "net_income": {"label": "Net Income", "format": "${:,.0f}"},
        "operating_margin": {"label": "Operating Margin", "format": "{:.1f}%"},
        "cash_flow": {"label": "Cash Flow", "format": "${:,.0f}"},
        "debt_ratio": {"label": "Debt Ratio", "format": "{:.2f}"},
    },
}


def render_kpi_cards(kpis: dict[str, Any], business_case: str) -> None:
    """
    Render KPI cards for the given business case.

    Args:
        kpis: Dictionary of KPI name -> value
        business_case: The business case for formatting configuration
    """
    if not kpis:
        st.warning("No KPI data available.")
        return

    config = _KPI_CONFIG.get(business_case, {})

    # Create columns for KPIs
    cols = st.columns(len(kpis))

    for col, (key, value) in zip(cols, kpis.items()):
        kpi_config = config.get(key, {"label": key.replace("_", " ").title(), "format": "{}"})
        label = kpi_config["label"]
        formatted_value = kpi_config["format"].format(value)
        col.metric(label, formatted_value)


def render_kpi_cards_generic(kpis: dict[str, Any]) -> None:
    """
    Render KPI cards without business case specific formatting.
    Useful for displaying arbitrary KPIs.

    Args:
        kpis: Dictionary of KPI name -> value
    """
    if not kpis:
        st.warning("No KPI data available.")
        return

    cols = st.columns(len(kpis))

    for col, (key, value) in zip(cols, kpis.items()):
        label = key.replace("_", " ").title()
        if isinstance(value, float):
            formatted = f"{value:,.2f}"
        elif isinstance(value, int):
            formatted = f"{value:,}"
        else:
            formatted = str(value)
        col.metric(label, formatted)
