"""
Mock API service layer.
All data fetching goes through this module.

The database is the SINGLE SOURCE OF TRUTH.
All filtering happens via SQL (mocked for now).
The UI only collects filter parameters - it NEVER filters data itself.

TODO: Replace with actual FastAPI client when backend is available.
"""

from typing import Any
import random

# TODO: Replace with actual FastAPI client
# BASE_URL = "http://localhost:8000/api/v1"


# =============================================================================
# Domain Configuration (Gold Tables)
# =============================================================================
# These are the source tables for each domain.
# Tables are NOT user-selected - they are defined by the domain.

DOMAIN_TABLES = {
    "sales": {
        "table": "mart.sales_orders_fact",
        "description": "Aggregated sales order data",
        "schema": [
            {"column": "order_date", "type": "DATE", "description": "Order date"},
            {"column": "region", "type": "VARCHAR", "description": "Sales region"},
            {"column": "product_category", "type": "VARCHAR", "description": "Product category"},
            {"column": "channel", "type": "VARCHAR", "description": "Sales channel"},
            {"column": "revenue", "type": "DECIMAL", "description": "Order revenue"},
            {"column": "quantity", "type": "INTEGER", "description": "Order quantity"},
        ],
        "sample_rows": [
            {"order_date": "2025-01-15", "region": "DACH", "product_category": "Electronics", "channel": "Online", "revenue": 1250.00, "quantity": 5},
            {"order_date": "2025-01-16", "region": "Nordics", "product_category": "Home", "channel": "Retail", "revenue": 890.50, "quantity": 3},
            {"order_date": "2025-01-17", "region": "UK", "product_category": "Sports", "channel": "Wholesale", "revenue": 2100.00, "quantity": 10},
        ],
    },
    "procurement": {
        "table": "mart.procurement_orders_fact",
        "description": "Aggregated procurement order data",
        "schema": [
            {"column": "purchase_date", "type": "DATE", "description": "Purchase date"},
            {"column": "supplier", "type": "VARCHAR", "description": "Supplier name"},
            {"column": "material_group", "type": "VARCHAR", "description": "Material group"},
            {"column": "plant", "type": "VARCHAR", "description": "Plant code"},
            {"column": "spend", "type": "DECIMAL", "description": "Purchase spend"},
            {"column": "quantity", "type": "INTEGER", "description": "Purchase quantity"},
        ],
        "sample_rows": [
            {"purchase_date": "2025-01-10", "supplier": "Supplier A", "material_group": "Raw Materials", "plant": "P100", "spend": 45000.00, "quantity": 500},
            {"purchase_date": "2025-01-12", "supplier": "Supplier B", "material_group": "Components", "plant": "P200", "spend": 32000.00, "quantity": 200},
            {"purchase_date": "2025-01-14", "supplier": "Supplier C", "material_group": "Services", "plant": "P100", "spend": 15000.00, "quantity": 1},
        ],
    },
    "finance": {
        "table": "mart.gl_postings_fact",
        "description": "Aggregated general ledger posting data",
        "schema": [
            {"column": "posting_period", "type": "VARCHAR", "description": "Posting period (YYYY-MM)"},
            {"column": "company_code", "type": "VARCHAR", "description": "Company code"},
            {"column": "cost_center", "type": "VARCHAR", "description": "Cost center"},
            {"column": "account", "type": "VARCHAR", "description": "GL account"},
            {"column": "amount", "type": "DECIMAL", "description": "Posting amount"},
            {"column": "currency", "type": "VARCHAR", "description": "Currency code"},
        ],
        "sample_rows": [
            {"posting_period": "2025-01", "company_code": "1000", "cost_center": "CC100", "account": "400000", "amount": 125000.00, "currency": "EUR"},
            {"posting_period": "2025-01", "company_code": "2000", "cost_center": "CC200", "account": "500000", "amount": 85000.00, "currency": "EUR"},
            {"posting_period": "2025-02", "company_code": "1000", "cost_center": "CC100", "account": "600000", "amount": 45000.00, "currency": "EUR"},
        ],
    },
}


def get_domain_table_info(domain: str) -> dict:
    """
    Get table information for a domain.
    This is for TRANSPARENCY - showing users what data source is used.
    """
    return DOMAIN_TABLES.get(domain, {})


# =============================================================================
# Domain Filter Options (Categorical Values)
# =============================================================================
# These are the available options for multi-select filters.
# In production, these would come from database queries.

FILTER_OPTIONS = {
    "sales": {
        "regions": ["DACH", "Nordics", "UK", "France", "Benelux", "Southern Europe"],
        "product_categories": ["Electronics", "Home", "Sports", "Fashion", "Food"],
        "channels": ["Online", "Retail", "Wholesale", "Partner"],
    },
    "procurement": {
        "suppliers": ["Supplier A", "Supplier B", "Supplier C", "Supplier D", "Supplier E"],
        "material_groups": ["Raw Materials", "Components", "Services", "Equipment", "MRO"],
        "plants": ["P100", "P200", "P300", "P400"],
    },
    "finance": {
        "company_codes": ["1000", "2000", "3000", "4000"],
        "cost_centers": ["CC100", "CC200", "CC300", "CC400", "CC500"],
        "accounts": ["400000", "500000", "600000", "700000", "800000"],
        "periods": [f"2025-{m:02d}" for m in range(1, 13)],
    },
}


def get_filter_options(domain: str) -> dict:
    """
    Get available filter options for a domain.
    TODO: Replace with requests.get(f"{BASE_URL}/domains/{domain}/filters")
    """
    return FILTER_OPTIONS.get(domain, {})


# =============================================================================
# SQL Generation (Mock)
# =============================================================================
# These functions generate SQL templates for transparency.
# The SQL is conceptually correct but mocked - no actual execution.

def _generate_sales_sql(filters: dict) -> str:
    """Generate SQL for sales domain."""
    where_clauses = []

    if filters.get("date_from"):
        where_clauses.append(f"order_date >= '{filters['date_from']}'")
    if filters.get("date_to"):
        where_clauses.append(f"order_date <= '{filters['date_to']}'")
    if filters.get("regions"):
        regions_str = ", ".join(f"'{r}'" for r in filters["regions"])
        where_clauses.append(f"region IN ({regions_str})")
    if filters.get("product_categories"):
        cats_str = ", ".join(f"'{c}'" for c in filters["product_categories"])
        where_clauses.append(f"product_category IN ({cats_str})")
    if filters.get("channels"):
        channels_str = ", ".join(f"'{c}'" for c in filters["channels"])
        where_clauses.append(f"channel IN ({channels_str})")

    where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

    return f"""SELECT
    SUM(revenue) as total_revenue,
    COUNT(*) as total_orders,
    AVG(revenue) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM mart.sales_orders_fact
WHERE {where_clause}"""


def _generate_procurement_sql(filters: dict) -> str:
    """Generate SQL for procurement domain."""
    where_clauses = []

    if filters.get("date_from"):
        where_clauses.append(f"purchase_date >= '{filters['date_from']}'")
    if filters.get("date_to"):
        where_clauses.append(f"purchase_date <= '{filters['date_to']}'")
    if filters.get("suppliers"):
        suppliers_str = ", ".join(f"'{s}'" for s in filters["suppliers"])
        where_clauses.append(f"supplier IN ({suppliers_str})")
    if filters.get("material_groups"):
        mats_str = ", ".join(f"'{m}'" for m in filters["material_groups"])
        where_clauses.append(f"material_group IN ({mats_str})")
    if filters.get("plants"):
        plants_str = ", ".join(f"'{p}'" for p in filters["plants"])
        where_clauses.append(f"plant IN ({plants_str})")

    where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

    return f"""SELECT
    SUM(spend) as total_spend,
    COUNT(*) as purchase_orders,
    AVG(spend) as avg_po_value,
    COUNT(DISTINCT supplier) as unique_suppliers
FROM mart.procurement_orders_fact
WHERE {where_clause}"""


def _generate_finance_sql(filters: dict) -> str:
    """Generate SQL for finance domain."""
    where_clauses = []

    if filters.get("period_from"):
        where_clauses.append(f"posting_period >= '{filters['period_from']}'")
    if filters.get("period_to"):
        where_clauses.append(f"posting_period <= '{filters['period_to']}'")
    if filters.get("company_codes"):
        codes_str = ", ".join(f"'{c}'" for c in filters["company_codes"])
        where_clauses.append(f"company_code IN ({codes_str})")
    if filters.get("cost_centers"):
        ccs_str = ", ".join(f"'{c}'" for c in filters["cost_centers"])
        where_clauses.append(f"cost_center IN ({ccs_str})")
    if filters.get("accounts"):
        accts_str = ", ".join(f"'{a}'" for a in filters["accounts"])
        where_clauses.append(f"account IN ({accts_str})")

    where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

    return f"""SELECT
    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_income,
    SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as total_expenses,
    SUM(amount) as net_income,
    COUNT(*) as posting_count
FROM mart.gl_postings_fact
WHERE {where_clause}"""


def generate_sql_preview(domain: str, filters: dict) -> str:
    """
    Generate SQL preview for a domain with given filters.
    This is for TRANSPARENCY - showing users what query would be executed.
    """
    if domain == "sales":
        return _generate_sales_sql(filters)
    elif domain == "procurement":
        return _generate_procurement_sql(filters)
    elif domain == "finance":
        return _generate_finance_sql(filters)
    else:
        return "-- Unknown domain"


# =============================================================================
# Run Execution (Mock)
# =============================================================================

def execute_run(domain: str, filters: dict) -> tuple[dict[str, Any], str]:
    """
    Execute a run and return results.
    This is a mock implementation that simulates database query execution.

    The filters are translated to SQL WHERE clauses (conceptually).
    KPI calculations happen in the database, NOT in the UI.

    TODO: Replace with requests.post(f"{BASE_URL}/runs", json={...})

    Args:
        domain: The domain (sales, procurement, finance)
        filters: Filter parameters from the UI

    Returns:
        Tuple of (results dict, SQL preview string)
    """
    # Generate SQL preview for transparency
    sql_preview = generate_sql_preview(domain, filters)

    # Calculate a multiplier based on filter selections to simulate filtered data
    # More filters = potentially smaller dataset
    filter_count = sum(1 for v in filters.values() if v)
    base_multiplier = max(0.3, 1.0 - (filter_count * 0.1))

    # Add randomness
    variance = random.uniform(0.9, 1.1)
    multiplier = base_multiplier * variance

    if domain == "sales":
        results = _generate_sales_results(multiplier, filters)
    elif domain == "procurement":
        results = _generate_procurement_results(multiplier, filters)
    elif domain == "finance":
        results = _generate_finance_results(multiplier, filters)
    else:
        results = {}

    return results, sql_preview


def _generate_sales_results(multiplier: float, filters: dict) -> dict:
    """Generate mock sales results based on filters."""
    # Use selected regions for breakdown, or default
    regions = filters.get("regions") or ["DACH", "Nordics", "UK", "France"]

    return {
        "kpis": {
            "total_revenue": int(1_250_000 * multiplier),
            "total_orders": int(8_420 * multiplier),
            "avg_order_value": round(148.46 * multiplier, 2),
            "conversion_rate": round(3.2 * (0.9 + multiplier * 0.2), 1),
        },
        "trends": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "revenue": [int(v * multiplier) for v in [180_000, 195_000, 210_000, 205_000, 225_000, 235_000]],
            "orders": [int(v * multiplier) for v in [1_200, 1_350, 1_420, 1_380, 1_510, 1_560]],
        },
        "breakdown": {
            "dimension": "region",
            "labels": regions[:4],
            "values": [int(random.randint(200_000, 400_000) * multiplier) for _ in regions[:4]],
        },
    }


def _generate_procurement_results(multiplier: float, filters: dict) -> dict:
    """Generate mock procurement results based on filters."""
    # Use selected material groups for breakdown, or default
    materials = filters.get("material_groups") or ["Raw Materials", "Components", "Services", "Equipment"]

    return {
        "kpis": {
            "total_spend": int(850_000 * multiplier),
            "purchase_orders": int(2_340 * multiplier),
            "avg_po_value": round(363.25 * multiplier, 2),
            "on_time_delivery": round(94.5 * (0.95 + multiplier * 0.05), 1),
        },
        "trends": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "spend": [int(v * multiplier) for v in [120_000, 135_000, 145_000, 140_000, 155_000, 155_000]],
            "orders": [int(v * multiplier) for v in [350, 380, 410, 395, 420, 385]],
        },
        "breakdown": {
            "dimension": "material_group",
            "labels": materials[:4],
            "values": [int(random.randint(100_000, 350_000) * multiplier) for _ in materials[:4]],
        },
    }


def _generate_finance_results(multiplier: float, filters: dict) -> dict:
    """Generate mock finance results based on filters."""
    # Use selected cost centers for breakdown, or default
    cost_centers = filters.get("cost_centers") or ["CC100", "CC200", "CC300", "CC400"]

    return {
        "kpis": {
            "net_income": int(320_000 * multiplier),
            "operating_margin": round(12.5 * multiplier, 1),
            "total_expenses": int(460_000 * multiplier),
            "posting_count": int(12_500 * multiplier),
        },
        "trends": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "income": [int(v * multiplier) for v in [85_000, 92_000, 98_000, 95_000, 102_000, 108_000]],
            "expenses": [int(v * multiplier) for v in [68_000, 72_000, 75_000, 74_000, 78_000, 80_000]],
        },
        "breakdown": {
            "dimension": "cost_center",
            "labels": cost_centers[:4],
            "values": [int(random.randint(80_000, 200_000) * multiplier) for _ in cost_centers[:4]],
        },
    }
