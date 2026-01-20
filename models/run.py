"""
Run data model for the Data Portal.
Represents a single analytical run with parameters and results.

This is UI state ONLY.
TODO: Replace with backend persistence when available.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
import uuid


class RunStatus(Enum):
    """Status of a run."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class RunParameters:
    """Parameters defining a run configuration."""
    period: str  # e.g., "2025-12"
    scenario: str  # e.g., "default", "optimistic", "pessimistic"

    def to_dict(self) -> dict:
        return {
            "period": self.period,
            "scenario": self.scenario,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RunParameters":
        return cls(
            period=data.get("period", ""),
            scenario=data.get("scenario", "default"),
        )


@dataclass
class Run:
    """
    A single analytical run.

    Represents a concrete analytical scenario defined by:
    - Business case (Sales / Procurement / Finance)
    - Parameters (period, scenario, etc.)
    - Execution timestamp
    - Results (KPIs, charts data)
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    business_case: str = ""  # "sales", "procurement", "finance"
    parameters: RunParameters = field(default_factory=lambda: RunParameters("", "default"))
    executed_at: str = ""  # ISO timestamp
    status: RunStatus = RunStatus.PENDING
    results: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.executed_at:
            self.executed_at = datetime.now().isoformat()

    @property
    def display_name(self) -> str:
        """Human-readable name for the run."""
        bc = self.business_case.title() if self.business_case else "Unknown"
        period = self.parameters.period if self.parameters.period else "No Period"
        scenario = self.parameters.scenario.title() if self.parameters.scenario else "Default"
        return f"{bc} - {period} - {scenario}"

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
            "business_case": self.business_case,
            "parameters": self.parameters.to_dict(),
            "executed_at": self.executed_at,
            "status": self.status.value,
            "results": self.results,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Run":
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            business_case=data.get("business_case", ""),
            parameters=RunParameters.from_dict(data.get("parameters", {})),
            executed_at=data.get("executed_at", ""),
            status=RunStatus(data.get("status", "pending")),
            results=data.get("results", {}),
        )
