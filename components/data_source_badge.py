"""
Data Source Badge Component.
Shows data source attribution for any data display.
"""

import streamlit as st


def render_source_badge(
    table: str | None = None,
    query_type: str | None = None,
    row_count: int | None = None,
    column: str | None = None,
) -> None:
    """
    Render a compact data source badge.

    Args:
        table: Source table name (e.g., "mart.sales_orders_fact")
        query_type: Type of query (e.g., "SELECT DISTINCT", "LIMIT 5", "Aggregation")
        row_count: Number of rows returned (optional)
        column: Column name for filter queries (optional)
    """
    parts = []

    if table:
        parts.append(f"Source: `{table}`")
    if column:
        parts.append(f"Column: `{column}`")
    if query_type:
        parts.append(f"Query: {query_type}")
    if row_count is not None:
        parts.append(f"Rows: {row_count}")

    if parts:
        st.caption(" | ".join(parts))


def render_schema_source(schema_name: str, table_name: str) -> None:
    """Render source badge for schema information."""
    st.caption(f"Source: `information_schema.columns` WHERE table_schema='{schema_name}' AND table_name='{table_name}'")


def render_sample_source(table: str, limit: int, row_count: int | None = None) -> None:
    """Render source badge for sample data."""
    if row_count is not None:
        st.caption(f"Source: `SELECT * FROM {table} LIMIT {limit}` | Rows: {row_count}")
    else:
        st.caption(f"Source: `SELECT * FROM {table} LIMIT {limit}`")


def render_filter_source(table: str, column: str, count: int | None = None) -> None:
    """Render source badge for filter options."""
    if count is not None:
        st.caption(f"Source: `SELECT DISTINCT {column} FROM {table}` | {count} values")
    else:
        st.caption(f"Source: `SELECT DISTINCT {column} FROM {table}`")


def render_date_range_source(table: str, column: str) -> None:
    """Render source badge for date range."""
    st.caption(f"Range from: `SELECT MIN({column}), MAX({column}) FROM {table}`")


def render_results_source(table: str, query_type: str = "Aggregation") -> None:
    """Render source badge for results section."""
    st.caption(f"Source: `{table}` | Query type: {query_type}")
