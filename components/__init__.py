"""
Reusable UI components for the Data Portal.

All components are for RENDERING only.
Data is pre-computed by the backend - the UI does NOT filter or aggregate.
"""

from components.kpi_cards import render_kpi_cards, render_kpi_cards_generic
from components.result_charts import render_run_results, render_trend_charts, render_breakdown_chart

__all__ = [
    "render_kpi_cards",
    "render_kpi_cards_generic",
    "render_run_results",
    "render_trend_charts",
    "render_breakdown_chart",
]
