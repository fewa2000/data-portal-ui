"""
Mock API service layer.
All data fetching goes through this module.
"""

import pandas as pd

# TODO: Replace with actual FastAPI client
# BASE_URL = "http://localhost:8000/api/v1"


def get_kpis() -> dict:
    """
    Fetch KPI summary data.
    TODO: Replace with requests.get(f"{BASE_URL}/kpis")
    """
    return {
        "total_revenue": 1_250_000,
        "total_orders": 8_420,
        "avg_order_value": 148.46,
        "active_customers": 2_150,
    }


def get_kpi_trends() -> pd.DataFrame:
    """
    Fetch KPI trend data over time.
    TODO: Replace with requests.get(f"{BASE_URL}/kpis/trends")
    """
    return pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "revenue": [180_000, 195_000, 210_000, 205_000, 225_000, 235_000],
        "orders": [1_200, 1_350, 1_420, 1_380, 1_510, 1_560],
    })


def get_drilldown_data(dimension: str) -> pd.DataFrame:
    """
    Fetch drilldown data for a given dimension.
    TODO: Replace with requests.get(f"{BASE_URL}/drilldown/{dimension}")
    """
    if dimension == "region":
        return pd.DataFrame({
            "region": ["North", "South", "East", "West"],
            "revenue": [320_000, 290_000, 380_000, 260_000],
            "orders": [2_100, 1_950, 2_520, 1_850],
        })
    elif dimension == "category":
        return pd.DataFrame({
            "category": ["Electronics", "Clothing", "Home", "Sports"],
            "revenue": [450_000, 320_000, 280_000, 200_000],
            "orders": [2_800, 2_400, 1_920, 1_300],
        })
    elif dimension == "channel":
        return pd.DataFrame({
            "channel": ["Online", "Retail", "Wholesale"],
            "revenue": [680_000, 380_000, 190_000],
            "orders": [4_500, 2_800, 1_120],
        })
    return pd.DataFrame()


def get_dimensions() -> list[str]:
    """
    Fetch available drilldown dimensions.
    TODO: Replace with requests.get(f"{BASE_URL}/dimensions")
    """
    return ["region", "category", "channel"]
