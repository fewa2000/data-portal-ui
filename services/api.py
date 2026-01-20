"""
Mock API service layer.
All data fetching goes through this module.

TODO: Replace with actual FastAPI client when backend is available.
"""

import pandas as pd
from typing import Any
import random

# TODO: Replace with actual FastAPI client
# BASE_URL = "http://localhost:8000/api/v1"


# =============================================================================
# Input Sources (Mock Data)
# =============================================================================

_MOCK_INPUTS = {
    "sales": [
        {"id": "sales_orders_csv", "name": "Sales Orders (CSV)", "type": "file", "description": "Monthly sales order export"},
        {"id": "sales_forecast_xlsx", "name": "Sales Forecast (Excel)", "type": "file", "description": "Q4 forecast spreadsheet"},
        {"id": "customer_master", "name": "Customer Master", "type": "database", "description": "Customer database table"},
        {"id": "product_catalog", "name": "Product Catalog", "type": "database", "description": "Product master data"},
    ],
    "procurement": [
        {"id": "purchase_orders_csv", "name": "Purchase Orders (CSV)", "type": "file", "description": "PO export from ERP"},
        {"id": "supplier_quotes_xlsx", "name": "Supplier Quotes (Excel)", "type": "file", "description": "Latest supplier quotations"},
        {"id": "vendor_master", "name": "Vendor Master", "type": "database", "description": "Vendor database table"},
        {"id": "inventory_levels", "name": "Inventory Levels", "type": "database", "description": "Current stock levels"},
    ],
    "finance": [
        {"id": "gl_transactions_csv", "name": "GL Transactions (CSV)", "type": "file", "description": "General ledger export"},
        {"id": "budget_xlsx", "name": "Budget Plan (Excel)", "type": "file", "description": "Annual budget spreadsheet"},
        {"id": "cost_centers", "name": "Cost Centers", "type": "database", "description": "Cost center master"},
        {"id": "accounts_payable", "name": "Accounts Payable", "type": "database", "description": "AP aging data"},
    ],
}


def get_inputs(business_case: str) -> list[dict]:
    """
    Fetch available input sources for a business case.
    TODO: Replace with requests.get(f"{BASE_URL}/inputs/{business_case}")
    """
    return _MOCK_INPUTS.get(business_case, [])


# =============================================================================
# Run Parameters (Mock Data)
# =============================================================================

def get_available_periods() -> list[str]:
    """
    Get available periods for run configuration.
    TODO: Replace with requests.get(f"{BASE_URL}/periods")
    """
    return [
        "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
        "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
    ]


def get_available_scenarios() -> list[str]:
    """
    Get available scenarios for run configuration.
    TODO: Replace with requests.get(f"{BASE_URL}/scenarios")
    """
    return ["default", "optimistic", "pessimistic"]


# =============================================================================
# Run Execution (Mock Data)
# =============================================================================

def execute_run(business_case: str, parameters: dict) -> dict[str, Any]:
    """
    Execute a run and return results.
    This is a mock implementation that returns simulated data.

    TODO: Replace with requests.post(f"{BASE_URL}/runs", json={...})

    Args:
        business_case: The business case (sales, procurement, finance)
        parameters: Run parameters (period, scenario, etc.)

    Returns:
        Dictionary containing KPIs and chart data
    """
    # Simulate different results based on business case and scenario
    scenario = parameters.get("scenario", "default")
    multiplier = {
        "default": 1.0,
        "optimistic": 1.15,
        "pessimistic": 0.85,
    }.get(scenario, 1.0)

    # Add some randomness to make it feel more real
    variance = random.uniform(0.95, 1.05)
    multiplier *= variance

    if business_case == "sales":
        return _generate_sales_results(multiplier)
    elif business_case == "procurement":
        return _generate_procurement_results(multiplier)
    elif business_case == "finance":
        return _generate_finance_results(multiplier)
    else:
        return {}


def _generate_sales_results(multiplier: float) -> dict:
    """Generate mock sales results."""
    return {
        "kpis": {
            "total_revenue": int(1_250_000 * multiplier),
            "total_orders": int(8_420 * multiplier),
            "avg_order_value": round(148.46 * multiplier, 2),
            "conversion_rate": round(3.2 * multiplier, 1),
        },
        "trends": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "revenue": [int(v * multiplier) for v in [180_000, 195_000, 210_000, 205_000, 225_000, 235_000]],
            "orders": [int(v * multiplier) for v in [1_200, 1_350, 1_420, 1_380, 1_510, 1_560]],
        },
        "breakdown": {
            "dimension": "region",
            "labels": ["North", "South", "East", "West"],
            "values": [int(v * multiplier) for v in [320_000, 290_000, 380_000, 260_000]],
        },
    }


def _generate_procurement_results(multiplier: float) -> dict:
    """Generate mock procurement results."""
    return {
        "kpis": {
            "total_spend": int(850_000 * multiplier),
            "purchase_orders": int(2_340 * multiplier),
            "avg_po_value": round(363.25 * multiplier, 2),
            "on_time_delivery": round(94.5 * (1 + (multiplier - 1) * 0.1), 1),
        },
        "trends": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "spend": [int(v * multiplier) for v in [120_000, 135_000, 145_000, 140_000, 155_000, 155_000]],
            "orders": [int(v * multiplier) for v in [350, 380, 410, 395, 420, 385]],
        },
        "breakdown": {
            "dimension": "category",
            "labels": ["Raw Materials", "Components", "Services", "Equipment"],
            "values": [int(v * multiplier) for v in [340_000, 250_000, 160_000, 100_000]],
        },
    }


def _generate_finance_results(multiplier: float) -> dict:
    """Generate mock finance results."""
    return {
        "kpis": {
            "net_income": int(320_000 * multiplier),
            "operating_margin": round(12.5 * multiplier, 1),
            "cash_flow": int(180_000 * multiplier),
            "debt_ratio": round(0.35 / multiplier, 2),
        },
        "trends": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "income": [int(v * multiplier) for v in [45_000, 52_000, 58_000, 55_000, 62_000, 48_000]],
            "expenses": [int(v * multiplier) for v in [38_000, 42_000, 45_000, 44_000, 48_000, 40_000]],
        },
        "breakdown": {
            "dimension": "cost_center",
            "labels": ["Operations", "R&D", "Sales & Marketing", "Admin"],
            "values": [int(v * multiplier) for v in [180_000, 120_000, 95_000, 65_000]],
        },
    }


# =============================================================================
# Legacy Functions (Preserved for backward compatibility during transition)
# =============================================================================

def get_kpis() -> dict:
    """
    Fetch KPI summary data.
    DEPRECATED: Use execute_run() instead.
    TODO: Remove after migration is complete.
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
    DEPRECATED: Use execute_run() instead.
    TODO: Remove after migration is complete.
    """
    return pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "revenue": [180_000, 195_000, 210_000, 205_000, 225_000, 235_000],
        "orders": [1_200, 1_350, 1_420, 1_380, 1_510, 1_560],
    })


def get_drilldown_data(dimension: str) -> pd.DataFrame:
    """
    Fetch drilldown data for a given dimension.
    DEPRECATED: Use execute_run() instead.
    TODO: Remove after migration is complete.
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
    DEPRECATED: Dimensions are now included in run results.
    TODO: Remove after migration is complete.
    """
    return ["region", "category", "channel"]
