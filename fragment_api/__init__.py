"""
Fragment API Python SDK

Purchase Telegram Stars and Premium via Fragment API.
"""

from .client import DEFAULT_API_URL, FragmentAPIClient, __version__
from .models import (
    BuyStarsResponse,
    PurchaseResult,
    PremiumEligibilityResult,
    QueuedRequest,
    QueueStatus,
    CommissionRatesResponse,
)
from .exceptions import (
    FragmentAPIError,
    InvalidResponseError,
    QueueTimeoutError,
)

__all__ = [
    # Client
    "DEFAULT_API_URL",
    "FragmentAPIClient",
    "__version__",
    # Models
    "BuyStarsResponse",
    "PurchaseResult",
    "PremiumEligibilityResult",
    "QueuedRequest",
    "QueueStatus",
    "CommissionRatesResponse",
    # Exceptions
    "FragmentAPIError",
    "InvalidResponseError",
    "QueueTimeoutError",
]
