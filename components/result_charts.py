"""
Result Charts Component.
Renders charts and visualizations for run results.

All data displayed here is PRE-COMPUTED by the backend.
The UI does NOT perform any filtering or aggregation.
"""

import streamlit as st
import pandas as pd
from typing import Any

from components.kpi_cards import render_kpi_cards
from services import api


def render_trend_charts(trends: dict[str, Any], domain: str) -> None:
    """
    Render trend charts from run results.

    Args:
        trends: Trend data with 'months' and metric arrays (pre-computed)
        domain: The domain for labeling
    """
    if not trends or "months" not in trends:
        st.warning("No trend data available.")
        return

    months = trends["months"]

    # Determine which metrics to display based on domain
    if domain == "sales":
        metric1, metric2 = "revenue", "orders"
        label1, label2 = "Revenue ($)", "Orders"
    elif domain == "procurement":
        metric1, metric2 = "spend", "orders"
        label1, label2 = "Spend ($)", "Orders"
    elif domain == "finance":
        metric1, metric2 = "income", "expenses"
        label1, label2 = "Income ($)", "Expenses ($)"
    else:
        # Fallback: use first two keys that aren't 'months'
        metrics = [k for k in trends.keys() if k != "months"]
        if len(metrics) >= 2:
            metric1, metric2 = metrics[0], metrics[1]
            label1, label2 = metric1.title(), metric2.title()
        elif len(metrics) == 1:
            metric1 = metrics[0]
            metric2 = None
            label1 = metric1.title()
            label2 = None
        else:
            st.warning("No trend metrics found.")
            return

    col1, col2 = st.columns(2)

    with col1:
        if metric1 in trends:
            df = pd.DataFrame({"Month": months, label1: trends[metric1]})
            st.line_chart(df.set_index("Month"), y_label=label1)

    with col2:
        if metric2 and metric2 in trends:
            df = pd.DataFrame({"Month": months, label2: trends[metric2]})
            st.line_chart(df.set_index("Month"), y_label=label2)


def render_breakdown_chart(breakdown: dict[str, Any]) -> None:
    """
    Render a breakdown bar chart from run results.

    Args:
        breakdown: Breakdown data with 'dimension', 'labels', and 'values' (pre-computed)
    """
    if not breakdown or "labels" not in breakdown or "values" not in breakdown:
        st.warning("No breakdown data available.")
        return

    dimension = breakdown.get("dimension", "Category").replace("_", " ").title()
    labels = breakdown["labels"]
    values = breakdown["values"]

    df = pd.DataFrame({dimension: labels, "Value": values})

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df.set_index(dimension))
    with col2:
        st.dataframe(df, use_container_width=True, hide_index=True)


def render_run_results(results: dict[str, Any], domain: str) -> None:
    """
    Render complete run results including KPIs, trends, and breakdown.

    All data is PRE-COMPUTED by the backend. The UI only renders.

    Args:
        results: Complete run results dictionary
        domain: The domain
    """
    if not results:
        st.warning("No results available.")
        return

    # Get table name for source attribution
    table_info = api.DOMAIN_TABLES.get(domain, {})
    table_name = table_info.get("table", "unknown")

    # KPIs
    if "kpis" in results:
        st.subheader("Key Performance Indicators")
        st.caption(f"Computed from: `{table_name}` | Query: SUM, COUNT, AVG aggregations")
        render_kpi_cards(results["kpis"], domain)
        st.divider()

    # Trends
    if "trends" in results:
        st.subheader("Trends")
        st.caption(f"Computed from: `{table_name}` | Query: GROUP BY month")
        render_trend_charts(results["trends"], domain)
        st.divider()

    # Breakdown
    if "breakdown" in results:
        dimension = results["breakdown"].get("dimension", "category").replace("_", " ").title()
        st.subheader(f"Breakdown by {dimension}")
        st.caption(f"Computed from: `{table_name}` | Query: GROUP BY {results['breakdown'].get('dimension', 'category')}")
        render_breakdown_chart(results["breakdown"])
