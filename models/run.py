"""
Run data model for the Data Portal.
Represents a single analytical run with domain-specific filter parameters.

This is UI state ONLY.
TODO: Replace with backend persistence when available.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Any
import uuid


class RunStatus(Enum):
    """Status of a run."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# =============================================================================
# Domain Filter Contracts
# =============================================================================
# Each domain has a specific set of filters that translate to SQL WHERE clauses.
# The UI renders filters based on these contracts.
# Filters are NEVER applied in the UI - they are passed to the backend.

@dataclass
class SalesFilters:
    """
    Filter contract for Sales domain.
    Maps to: mart.sales_orders_fact
    """
    date_from: date | None = None
    date_to: date | None = None
    regions: list[str] = field(default_factory=list)  # multi-select
    product_categories: list[str] = field(default_factory=list)  # multi-select
    channels: list[str] = field(default_factory=list)  # multi-select

    def to_dict(self) -> dict:
        return {
            "date_from": self.date_from.isoformat() if self.date_from else None,
            "date_to": self.date_to.isoformat() if self.date_to else None,
            "regions": self.regions,
            "product_categories": self.product_categories,
            "channels": self.channels,
        }

    def to_display_string(self) -> str:
        """Human-readable filter summary."""
        parts = []
        if self.date_from and self.date_to:
            parts.append(f"{self.date_from} to {self.date_to}")
        elif self.date_from:
            parts.append(f"From {self.date_from}")
        elif self.date_to:
            parts.append(f"Until {self.date_to}")
        if self.regions:
            parts.append(f"Region: {', '.join(self.regions)}")
        if self.product_categories:
            parts.append(f"Category: {', '.join(self.product_categories)}")
        if self.channels:
            parts.append(f"Channel: {', '.join(self.channels)}")
        return " | ".join(parts) if parts else "No filters"

    @classmethod
    def from_dict(cls, data: dict) -> "SalesFilters":
        return cls(
            date_from=date.fromisoformat(data["date_from"]) if data.get("date_from") else None,
            date_to=date.fromisoformat(data["date_to"]) if data.get("date_to") else None,
            regions=data.get("regions", []),
            product_categories=data.get("product_categories", []),
            channels=data.get("channels", []),
        )


@dataclass
class ProcurementFilters:
    """
    Filter contract for Procurement domain.
    Maps to: mart.procurement_orders_fact
    """
    date_from: date | None = None
    date_to: date | None = None
    suppliers: list[str] = field(default_factory=list)  # multi-select
    material_groups: list[str] = field(default_factory=list)  # multi-select
    plants: list[str] = field(default_factory=list)  # multi-select

    def to_dict(self) -> dict:
        return {
            "date_from": self.date_from.isoformat() if self.date_from else None,
            "date_to": self.date_to.isoformat() if self.date_to else None,
            "suppliers": self.suppliers,
            "material_groups": self.material_groups,
            "plants": self.plants,
        }

    def to_display_string(self) -> str:
        """Human-readable filter summary."""
        parts = []
        if self.date_from and self.date_to:
            parts.append(f"{self.date_from} to {self.date_to}")
        elif self.date_from:
            parts.append(f"From {self.date_from}")
        elif self.date_to:
            parts.append(f"Until {self.date_to}")
        if self.suppliers:
            parts.append(f"Supplier: {', '.join(self.suppliers)}")
        if self.material_groups:
            parts.append(f"Material: {', '.join(self.material_groups)}")
        if self.plants:
            parts.append(f"Plant: {', '.join(self.plants)}")
        return " | ".join(parts) if parts else "No filters"

    @classmethod
    def from_dict(cls, data: dict) -> "ProcurementFilters":
        return cls(
            date_from=date.fromisoformat(data["date_from"]) if data.get("date_from") else None,
            date_to=date.fromisoformat(data["date_to"]) if data.get("date_to") else None,
            suppliers=data.get("suppliers", []),
            material_groups=data.get("material_groups", []),
            plants=data.get("plants", []),
        )


@dataclass
class FinanceFilters:
    """
    Filter contract for Finance domain.
    Maps to: mart.gl_postings_fact
    """
    period_from: str | None = None  # e.g., "2025-01"
    period_to: str | None = None  # e.g., "2025-12"
    company_codes: list[str] = field(default_factory=list)  # multi-select
    cost_centers: list[str] = field(default_factory=list)  # multi-select
    accounts: list[str] = field(default_factory=list)  # multi-select

    def to_dict(self) -> dict:
        return {
            "period_from": self.period_from,
            "period_to": self.period_to,
            "company_codes": self.company_codes,
            "cost_centers": self.cost_centers,
            "accounts": self.accounts,
        }

    def to_display_string(self) -> str:
        """Human-readable filter summary."""
        parts = []
        if self.period_from and self.period_to:
            parts.append(f"{self.period_from} to {self.period_to}")
        elif self.period_from:
            parts.append(f"From {self.period_from}")
        elif self.period_to:
            parts.append(f"Until {self.period_to}")
        if self.company_codes:
            parts.append(f"Company: {', '.join(self.company_codes)}")
        if self.cost_centers:
            parts.append(f"Cost Center: {', '.join(self.cost_centers)}")
        if self.accounts:
            parts.append(f"Account: {', '.join(self.accounts)}")
        return " | ".join(parts) if parts else "No filters"

    @classmethod
    def from_dict(cls, data: dict) -> "FinanceFilters":
        return cls(
            period_from=data.get("period_from"),
            period_to=data.get("period_to"),
            company_codes=data.get("company_codes", []),
            cost_centers=data.get("cost_centers", []),
            accounts=data.get("accounts", []),
        )


# Type alias for filter union
DomainFilters = SalesFilters | ProcurementFilters | FinanceFilters


def create_filters_from_dict(domain: str, data: dict) -> DomainFilters:
    """Factory function to create domain-specific filters from dictionary."""
    if domain == "sales":
        return SalesFilters.from_dict(data)
    elif domain == "procurement":
        return ProcurementFilters.from_dict(data)
    elif domain == "finance":
        return FinanceFilters.from_dict(data)
    else:
        raise ValueError(f"Unknown domain: {domain}")


# =============================================================================
# Run Model
# =============================================================================

@dataclass
class Run:
    """
    A single analytical run.

    Represents a concrete analytical scenario defined by:
    - Domain (Sales / Procurement / Finance)
    - Filter parameters (based on domain contract)
    - Execution timestamp
    - Results (KPIs, charts data)

    Filter parameters are translated to SQL WHERE clauses by the backend.
    The UI NEVER filters data itself.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    domain: str = ""  # "sales", "procurement", "finance"
    filters: dict[str, Any] = field(default_factory=dict)  # Serialized filter parameters
    executed_at: str = ""  # ISO timestamp
    status: RunStatus = RunStatus.PENDING
    results: dict[str, Any] = field(default_factory=dict)
    # SQL template generated (for transparency, not execution)
    sql_preview: str = ""

    def __post_init__(self):
        if not self.executed_at:
            self.executed_at = datetime.now().isoformat()

    @property
    def display_name(self) -> str:
        """Human-readable name for the run."""
        domain_name = self.domain.title() if self.domain else "Unknown"
        filter_summary = self.get_filter_summary()
        return f"{domain_name} - {filter_summary}"

    def get_filter_summary(self) -> str:
        """Get human-readable filter summary."""
        if not self.filters:
            return "No filters"
        try:
            filter_obj = create_filters_from_dict(self.domain, self.filters)
            return filter_obj.to_display_string()
        except (ValueError, KeyError):
            return "Invalid filters"

    @property
    def executed_at_formatted(self) -> str:
        """Formatted execution timestamp."""
        try:
            dt = datetime.fromisoformat(self.executed_at)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return self.executed_at

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "domain": self.domain,
            "filters": self.filters,
            "executed_at": self.executed_at,
            "status": self.status.value,
            "results": self.results,
            "sql_preview": self.sql_preview,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Run":
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            domain=data.get("domain", ""),
            filters=data.get("filters", {}),
            executed_at=data.get("executed_at", ""),
            status=RunStatus(data.get("status", "pending")),
            results=data.get("results", {}),
            sql_preview=data.get("sql_preview", ""),
        )
