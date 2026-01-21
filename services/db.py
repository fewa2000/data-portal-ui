"""
Database connection helper using SQLAlchemy 2.0.

Reads connection string from DATABASE_URL environment variable.
"""

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection


# Read connection string from environment variable
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/dataportal"
)

# Create engine with connection pooling
_engine: Engine | None = None


def get_engine() -> Engine:
    """Get or create the SQLAlchemy engine."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    return _engine


@contextmanager
def get_connection() -> Generator[Connection, None, None]:
    """
    Context manager for database connections.

    Usage:
        with get_connection() as conn:
            result = conn.execute(text("SELECT ..."))
    """
    engine = get_engine()
    with engine.connect() as conn:
        yield conn


def execute_query(sql: str, params: dict | None = None) -> list[dict]:
    """
    Execute a query and return results as list of dicts.

    Args:
        sql: SQL query string (use :param_name for parameters)
        params: Dictionary of parameter values

    Returns:
        List of row dictionaries
    """
    with get_connection() as conn:
        result = conn.execute(text(sql), params or {})
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]


def execute_scalar(sql: str, params: dict | None = None):
    """
    Execute a query and return a single scalar value.

    Args:
        sql: SQL query string
        params: Dictionary of parameter values

    Returns:
        Single value from first column of first row
    """
    with get_connection() as conn:
        result = conn.execute(text(sql), params or {})
        row = result.fetchone()
        return row[0] if row else None
