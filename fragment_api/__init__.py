"""
Fragment API Python SDK

Purchase Telegram Stars and Premium via Fragment API.
"""

from .client import DEFAULT_API_URL, FragmentAPIClient, __version__
from .exceptions import (
    FragmentAPIError,
    InvalidResponseError,
    QueueTimeoutError,
)
from .models import (
    BuyStarsResponse,
    CommissionRatesResponse,
    PremiumEligibilityResult,
    PurchaseResult,
    QueuedRequest,
    QueueStatus,
    WalletResolution,
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
    "WalletResolution",
    # Exceptions
    "FragmentAPIError",
    "InvalidResponseError",
    "QueueTimeoutError",
]
