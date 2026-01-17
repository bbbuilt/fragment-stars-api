"""
Fragment API Python SDK

Purchase Telegram Stars and Premium via Fragment API.
"""

from .client import FragmentAPIClient, __version__
from .models import (
    BuyStarsResponse,
    PurchaseResult,
    QueuedRequest,
    QueueStatus,
    CommissionRatesResponse,
)
from .exceptions import (
    FragmentAPIError,
    QueueTimeoutError,
)

__all__ = [
    # Client
    "FragmentAPIClient",
    "__version__",
    # Models
    "BuyStarsResponse",
    "PurchaseResult",
    "QueuedRequest",
    "QueueStatus",
    "CommissionRatesResponse",
    # Exceptions
    "FragmentAPIError",
    "QueueTimeoutError",
]
