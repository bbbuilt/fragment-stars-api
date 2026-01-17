"""
Data models for Fragment API responses.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class OrderStatus(str, Enum):
    """Order status values."""
    CREATED = "created"
    QUEUED = "queued"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    EXPIRED = "expired"


class QueueStatus(str, Enum):
    """Queue request status values."""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ErrorDetail:
    """Validation error detail."""
    field: str
    message: str


@dataclass
class ErrorResponse:
    """API error response."""
    code: int
    message: str
    error_code: str
    details: list[ErrorDetail] = field(default_factory=list)


@dataclass
class QueuedRequest:
    """Queued request data model."""
    id: str
    status: QueueStatus
    position: Optional[int] = None
    estimated_wait_seconds: Optional[int] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    type: Optional[str] = None
    api_key_id: Optional[str] = None
    wallet_address: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QueuedRequest":
        """Create QueuedRequest from API response dict."""
        request_id = data.get("request_id") or data.get("id", "")
        
        return cls(
            id=request_id,
            status=QueueStatus(data["status"]),
            position=data.get("position"),
            estimated_wait_seconds=data.get("estimated_wait_seconds"),
            created_at=_parse_datetime(data["created_at"]) if data.get("created_at") else None,
            started_at=_parse_datetime(data["started_at"]) if data.get("started_at") else None,
            completed_at=_parse_datetime(data["completed_at"]) if data.get("completed_at") else None,
            result=data.get("result"),
            error=data.get("error"),
            type=data.get("type"),
            api_key_id=data.get("api_key_id"),
            wallet_address=data.get("wallet_address"),
        )


@dataclass
class BuyStarsResponse:
    """Response from buy stars endpoint (queued)."""
    request_id: str
    position: int
    estimated_wait_seconds: int
    message: str


@dataclass
class PurchaseResult:
    """Final result of a completed purchase."""
    success: bool
    transaction_id: Optional[str] = None
    transaction_hash: Optional[str] = None
    amount: Optional[int] = None
    cost_ton: Optional[str] = None
    commission_ton: Optional[str] = None
    commission_rate: Optional[float] = None
    mode: Optional[str] = None  # 'kyc' or 'no_kyc'
    error: Optional[str] = None


@dataclass
class CommissionRatesResponse:
    """Commission rates response."""
    rate_no_kyc: float           # Percentage (e.g., 5 for 5%)
    rate_with_kyc: float         # Percentage (e.g., 1.5 for 1.5%)
    rate_no_kyc_decimal: float   # Decimal (e.g., 0.05)
    rate_with_kyc_decimal: float # Decimal (e.g., 0.015)
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CommissionRatesResponse":
        """Create from API response dict."""
        return cls(
            rate_no_kyc=data["rate_no_kyc"],
            rate_with_kyc=data["rate_with_kyc"],
            rate_no_kyc_decimal=data["rate_no_kyc_decimal"],
            rate_with_kyc_decimal=data["rate_with_kyc_decimal"],
            updated_at=_parse_datetime(data["updated_at"]),
        )


def _parse_datetime(value: Any) -> datetime:
    """Parse datetime from various formats."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        value = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.fromisoformat(value.split("+")[0].split("Z")[0])
    raise ValueError(f"Cannot parse datetime from {value}")
