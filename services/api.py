"""
Database-backed API service layer.
All data fetching goes through this module.

The database is the SINGLE SOURCE OF TRUTH.
All filtering happens via SQL.
The UI only collects filter parameters - it NEVER filters data itself.
"""

from typing import Any

from sqlalchemy import text, bindparam

from services.db import get_connection, execute_query


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
            {"column": "visitor_id", "type": "VARCHAR", "description": "Visitor identifier"},
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
            {"column": "requested_delivery_date", "type": "DATE", "description": "Requested delivery date"},
            {"column": "actual_delivery_date", "type": "DATE", "description": "Actual delivery date"},
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
            {"column": "account_type", "type": "VARCHAR", "description": "Account type (revenue/expense)"},
            {"column": "amount", "type": "DECIMAL", "description": "Posting amount"},
        ],
    },
}

# Column mappings for filter options queries
FILTER_COLUMNS = {
    "sales": {
        "regions": "region",
        "product_categories": "product_category",
        "channels": "channel",
    },
    "procurement": {
        "suppliers": "supplier",
        "material_groups": "material_group",
        "plants": "plant",
    },
    "finance": {
        "company_codes": "company_code",
        "cost_centers": "cost_center",
        "accounts": "account",
        "periods": "posting_period",
    },
}


def get_domain_table_info(domain: str) -> dict:
    """
    Get table information for a domain including schema and sample rows.
    This is for TRANSPARENCY - showing users what data source is used.
    """
    info = DOMAIN_TABLES.get(domain, {})
    if not info:
        return {}

    result = {
        "table": info["table"],
        "description": info["description"],
        "schema": info["schema"],
        "sample_rows": [],
    }

    # Fetch sample rows from database
    table = info["table"]
    try:
        sample_rows = execute_query(f"SELECT * FROM {table} LIMIT 5")
        result["sample_rows"] = sample_rows
    except Exception:
        # Return empty sample_rows if DB unavailable
        pass

    return result


def get_filter_options(domain: str) -> dict:
    """
    Get available filter options for a domain from the database.
    Returns distinct values for each filter column.
    """
    columns = FILTER_COLUMNS.get(domain)
    if not columns:
        return {}

    table_info = DOMAIN_TABLES.get(domain)
    if not table_info:
        return {}

    table = table_info["table"]
    result = {}

    for filter_name, column_name in columns.items():
        try:
            sql = f"SELECT DISTINCT {column_name} FROM {table} WHERE {column_name} IS NOT NULL ORDER BY {column_name}"
            rows = execute_query(sql)
            result[filter_name] = [row[column_name] for row in rows]
        except Exception:
            result[filter_name] = []

    return result


# =============================================================================
# SQL Generation
# =============================================================================

def _build_sales_where_clause(filters: dict) -> tuple[str, dict]:
    """Build WHERE clause and params for sales queries."""
    conditions = []
    params = {}

    if filters.get("date_from"):
        conditions.append("order_date >= :date_from")
        params["date_from"] = filters["date_from"]
    if filters.get("date_to"):
        conditions.append("order_date <= :date_to")
        params["date_to"] = filters["date_to"]
    if filters.get("regions"):
        conditions.append("region IN :regions")
        params["regions"] = tuple(filters["regions"])
    if filters.get("product_categories"):
        conditions.append("product_category IN :product_categories")
        params["product_categories"] = tuple(filters["product_categories"])
    if filters.get("channels"):
        conditions.append("channel IN :channels")
        params["channels"] = tuple(filters["channels"])

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    return where_clause, params


def _build_procurement_where_clause(filters: dict) -> tuple[str, dict]:
    """Build WHERE clause and params for procurement queries."""
    conditions = []
    params = {}

    if filters.get("date_from"):
        conditions.append("purchase_date >= :date_from")
        params["date_from"] = filters["date_from"]
    if filters.get("date_to"):
        conditions.append("purchase_date <= :date_to")
        params["date_to"] = filters["date_to"]
    if filters.get("suppliers"):
        conditions.append("supplier IN :suppliers")
        params["suppliers"] = tuple(filters["suppliers"])
    if filters.get("material_groups"):
        conditions.append("material_group IN :material_groups")
        params["material_groups"] = tuple(filters["material_groups"])
    if filters.get("plants"):
        conditions.append("plant IN :plants")
        params["plants"] = tuple(filters["plants"])

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    return where_clause, params


def _build_finance_where_clause(filters: dict) -> tuple[str, dict]:
    """Build WHERE clause and params for finance queries."""
    conditions = []
    params = {}

    if filters.get("period_from"):
        conditions.append("posting_period >= :period_from")
        params["period_from"] = filters["period_from"]
    if filters.get("period_to"):
        conditions.append("posting_period <= :period_to")
        params["period_to"] = filters["period_to"]
    if filters.get("company_codes"):
        conditions.append("company_code IN :company_codes")
        params["company_codes"] = tuple(filters["company_codes"])
    if filters.get("cost_centers"):
        conditions.append("cost_center IN :cost_centers")
        params["cost_centers"] = tuple(filters["cost_centers"])
    if filters.get("accounts"):
        conditions.append("account IN :accounts")
        params["accounts"] = tuple(filters["accounts"])

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    return where_clause, params


def _generate_sales_sql(filters: dict) -> str:
    """Generate SQL preview for sales domain."""
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
    COUNT(DISTINCT visitor_id) as unique_visitors
FROM mart.sales_orders_fact
WHERE {where_clause}"""


def _generate_procurement_sql(filters: dict) -> str:
    """Generate SQL preview for procurement domain."""
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
    """Generate SQL preview for finance domain."""
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
# Run Execution
# =============================================================================

def _execute_with_expanding_params(sql: str, params: dict) -> list[dict]:
    """Execute query with expanding IN clause parameters."""
    with get_connection() as conn:
        # Build the statement with expanding bindparams for tuple values
        stmt = text(sql)
        for key, value in params.items():
            if isinstance(value, tuple):
                stmt = stmt.bindparams(bindparam(key, expanding=True))

        result = conn.execute(stmt, params)
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]


def _execute_scalar_with_expanding_params(sql: str, params: dict):
    """Execute query and return single scalar with expanding IN clause support."""
    rows = _execute_with_expanding_params(sql, params)
    if rows:
        first_row = rows[0]
        first_key = list(first_row.keys())[0]
        return first_row[first_key]
    return None


def execute_run(domain: str, filters: dict) -> tuple[dict[str, Any], str]:
    """
    Execute a run and return results.

    The filters are translated to SQL WHERE clauses.
    KPI calculations happen in the database, NOT in the UI.

    Args:
        domain: The domain (sales, procurement, finance)
        filters: Filter parameters from the UI

    Returns:
        Tuple of (results dict, SQL preview string)
    """
    sql_preview = generate_sql_preview(domain, filters)

    if domain == "sales":
        results = _execute_sales_run(filters)
    elif domain == "procurement":
        results = _execute_procurement_run(filters)
    elif domain == "finance":
        results = _execute_finance_run(filters)
    else:
        results = {}

    return results, sql_preview


def _execute_sales_run(filters: dict) -> dict:
    """Execute sales run with real SQL queries."""
    where_clause, params = _build_sales_where_clause(filters)

    # KPIs query
    kpi_sql = f"""
        SELECT
            COALESCE(SUM(revenue), 0) as total_revenue,
            COUNT(*) as total_orders,
            COALESCE(AVG(revenue), 0) as avg_order_value,
            COUNT(DISTINCT visitor_id) as unique_visitors
        FROM mart.sales_orders_fact
        WHERE {where_clause}
    """
    kpi_rows = _execute_with_expanding_params(kpi_sql, params)
    kpi_row = kpi_rows[0] if kpi_rows else {}

    total_orders = int(kpi_row.get("total_orders", 0))
    unique_visitors = int(kpi_row.get("unique_visitors", 0))
    conversion_rate = (total_orders / unique_visitors * 100) if unique_visitors > 0 else 0.0

    kpis = {
        "total_revenue": int(kpi_row.get("total_revenue", 0)),
        "total_orders": total_orders,
        "avg_order_value": round(float(kpi_row.get("avg_order_value", 0)), 2),
        "conversion_rate": round(conversion_rate, 1),
    }

    # Trends query - group by month
    trends_sql = f"""
        SELECT
            TO_CHAR(order_date, 'Mon') as month,
            EXTRACT(MONTH FROM order_date) as month_num,
            COALESCE(SUM(revenue), 0) as revenue,
            COUNT(*) as orders
        FROM mart.sales_orders_fact
        WHERE {where_clause}
        GROUP BY TO_CHAR(order_date, 'Mon'), EXTRACT(MONTH FROM order_date)
        ORDER BY month_num
    """
    trend_rows = _execute_with_expanding_params(trends_sql, params)

    trends = {
        "months": [row["month"] for row in trend_rows],
        "revenue": [int(row["revenue"]) for row in trend_rows],
        "orders": [int(row["orders"]) for row in trend_rows],
    }

    # Breakdown by region
    breakdown_sql = f"""
        SELECT
            region,
            COALESCE(SUM(revenue), 0) as value
        FROM mart.sales_orders_fact
        WHERE {where_clause}
        GROUP BY region
        ORDER BY value DESC
        LIMIT 10
    """
    breakdown_rows = _execute_with_expanding_params(breakdown_sql, params)

    breakdown = {
        "dimension": "region",
        "labels": [row["region"] for row in breakdown_rows],
        "values": [int(row["value"]) for row in breakdown_rows],
    }

    return {
        "kpis": kpis,
        "trends": trends,
        "breakdown": breakdown,
    }


def _execute_procurement_run(filters: dict) -> dict:
    """Execute procurement run with real SQL queries."""
    where_clause, params = _build_procurement_where_clause(filters)

    # KPIs query
    kpi_sql = f"""
        SELECT
            COALESCE(SUM(spend), 0) as total_spend,
            COUNT(*) as purchase_orders,
            COALESCE(AVG(spend), 0) as avg_po_value,
            COUNT(CASE WHEN actual_delivery_date <= requested_delivery_date THEN 1 END) as on_time_count,
            COUNT(CASE WHEN actual_delivery_date IS NOT NULL AND requested_delivery_date IS NOT NULL THEN 1 END) as delivery_count
        FROM mart.procurement_orders_fact
        WHERE {where_clause}
    """
    kpi_rows = _execute_with_expanding_params(kpi_sql, params)
    kpi_row = kpi_rows[0] if kpi_rows else {}

    on_time_count = int(kpi_row.get("on_time_count", 0))
    delivery_count = int(kpi_row.get("delivery_count", 0))
    on_time_delivery = (on_time_count / delivery_count * 100) if delivery_count > 0 else 0.0

    kpis = {
        "total_spend": int(kpi_row.get("total_spend", 0)),
        "purchase_orders": int(kpi_row.get("purchase_orders", 0)),
        "avg_po_value": round(float(kpi_row.get("avg_po_value", 0)), 2),
        "on_time_delivery": round(on_time_delivery, 1),
    }

    # Trends query - group by month
    trends_sql = f"""
        SELECT
            TO_CHAR(purchase_date, 'Mon') as month,
            EXTRACT(MONTH FROM purchase_date) as month_num,
            COALESCE(SUM(spend), 0) as spend,
            COUNT(*) as orders
        FROM mart.procurement_orders_fact
        WHERE {where_clause}
        GROUP BY TO_CHAR(purchase_date, 'Mon'), EXTRACT(MONTH FROM purchase_date)
        ORDER BY month_num
    """
    trend_rows = _execute_with_expanding_params(trends_sql, params)

    trends = {
        "months": [row["month"] for row in trend_rows],
        "spend": [int(row["spend"]) for row in trend_rows],
        "orders": [int(row["orders"]) for row in trend_rows],
    }

    # Breakdown by material_group
    breakdown_sql = f"""
        SELECT
            material_group,
            COALESCE(SUM(spend), 0) as value
        FROM mart.procurement_orders_fact
        WHERE {where_clause}
        GROUP BY material_group
        ORDER BY value DESC
        LIMIT 10
    """
    breakdown_rows = _execute_with_expanding_params(breakdown_sql, params)

    breakdown = {
        "dimension": "material_group",
        "labels": [row["material_group"] for row in breakdown_rows],
        "values": [int(row["value"]) for row in breakdown_rows],
    }

    return {
        "kpis": kpis,
        "trends": trends,
        "breakdown": breakdown,
    }


def _execute_finance_run(filters: dict) -> dict:
    """Execute finance run with real SQL queries."""
    where_clause, params = _build_finance_where_clause(filters)

    # KPIs query - use account_type to distinguish income vs expenses
    kpi_sql = f"""
        SELECT
            COALESCE(SUM(CASE WHEN account_type = 'revenue' THEN amount ELSE 0 END), 0) as total_income,
            COALESCE(SUM(CASE WHEN account_type = 'expense' THEN ABS(amount) ELSE 0 END), 0) as total_expenses,
            COALESCE(SUM(amount), 0) as net_income,
            COUNT(*) as posting_count
        FROM mart.gl_postings_fact
        WHERE {where_clause}
    """
    kpi_rows = _execute_with_expanding_params(kpi_sql, params)
    kpi_row = kpi_rows[0] if kpi_rows else {}

    total_income = float(kpi_row.get("total_income", 0))
    total_expenses = float(kpi_row.get("total_expenses", 0))
    operating_margin = (total_income - total_expenses) / total_income * 100 if total_income > 0 else 0.0

    kpis = {
        "net_income": int(kpi_row.get("net_income", 0)),
        "operating_margin": round(operating_margin, 1),
        "total_expenses": int(total_expenses),
        "posting_count": int(kpi_row.get("posting_count", 0)),
    }

    # Trends query - group by posting_period (already YYYY-MM format)
    trends_sql = f"""
        SELECT
            posting_period,
            COALESCE(SUM(CASE WHEN account_type = 'revenue' THEN amount ELSE 0 END), 0) as income,
            COALESCE(SUM(CASE WHEN account_type = 'expense' THEN ABS(amount) ELSE 0 END), 0) as expenses
        FROM mart.gl_postings_fact
        WHERE {where_clause}
        GROUP BY posting_period
        ORDER BY posting_period
    """
    trend_rows = _execute_with_expanding_params(trends_sql, params)

    # Convert YYYY-MM to month abbreviation
    month_abbrevs = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }

    months = []
    for row in trend_rows:
        period = row["posting_period"]
        if period and len(period) >= 7:
            month_num = period[5:7]
            months.append(month_abbrevs.get(month_num, period))
        else:
            months.append(str(period))

    trends = {
        "months": months,
        "income": [int(row["income"]) for row in trend_rows],
        "expenses": [int(row["expenses"]) for row in trend_rows],
    }

    # Breakdown by cost_center
    breakdown_sql = f"""
        SELECT
            cost_center,
            COALESCE(SUM(ABS(amount)), 0) as value
        FROM mart.gl_postings_fact
        WHERE {where_clause}
        GROUP BY cost_center
        ORDER BY value DESC
        LIMIT 10
    """
    breakdown_rows = _execute_with_expanding_params(breakdown_sql, params)

    breakdown = {
        "dimension": "cost_center",
        "labels": [row["cost_center"] for row in breakdown_rows],
        "values": [int(row["value"]) for row in breakdown_rows],
    }

    return {
        "kpis": kpis,
        "trends": trends,
        "breakdown": breakdown,
    }
