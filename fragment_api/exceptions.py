"""
Exception classes for Fragment API errors.
"""

from typing import Optional

from .models import ErrorDetail


class FragmentAPIError(Exception):
    """Base exception for all Fragment API errors."""

    def __init__(
        self,
        message: str,
        code: int,
        error_code: str,
        details: Optional[list[ErrorDetail]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.error_code = error_code
        self.details = details or []

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


class ValidationError(FragmentAPIError):
    """Validation error (422)."""

    pass


class AuthenticationError(FragmentAPIError):
    """Authentication error (401)."""

    pass


class InsufficientBalanceError(FragmentAPIError):
    """Insufficient balance error (402)."""

    pass


class UserNotFoundError(FragmentAPIError):
    """User not found error (404)."""

    pass


class QueueTimeoutError(FragmentAPIError):
    """Queue timeout error (408)."""

    pass


class RateLimitError(FragmentAPIError):
    """Rate limit exceeded error (429)."""

    def __init__(
        self,
        message: str,
        code: int,
        error_code: str,
        details: Optional[list[ErrorDetail]] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(message, code, error_code, details)
        self.retry_after = retry_after


class FragmentServiceError(FragmentAPIError):
    """Fragment.com service error (502)."""

    pass


class InvalidResponseError(FragmentAPIError):
    """API returned an invalid or unexpected response."""

    pass


# Error code to exception class mapping
ERROR_CODE_MAP = {
    "VALIDATION_ERROR": ValidationError,
    "INVALID_USERNAME_FORMAT": ValidationError,
    "INVALID_FRAGMENT_COOKIES": ValidationError,
    "INVALID_FRAGMENT_LOCAL_STORAGE": ValidationError,
    "INVALID_WALLET_ADDRESS": ValidationError,
    "WALLET_ADDRESS_MISMATCH": ValidationError,
    "ACCOUNT_INDEX_NOT_FOUND": ValidationError,
    "UNAUTHORIZED": AuthenticationError,
    "INVALID_API_KEY": AuthenticationError,
    "INVALID_SEED": AuthenticationError,
    "INVALID_COOKIES": AuthenticationError,
    "INSUFFICIENT_BALANCE": InsufficientBalanceError,
    "USER_NOT_FOUND": UserNotFoundError,
    "QUEUE_TIMEOUT": QueueTimeoutError,
    "RATE_LIMIT_EXCEEDED": RateLimitError,
    "API_BUSY": RateLimitError,
    "FRAGMENT_ERROR": FragmentServiceError,
    "INVALID_RESPONSE": InvalidResponseError,
    "USER_HAS_PREMIUM": FragmentAPIError,
    "WALLET_CONNECTION_FAILED": FragmentServiceError,
    "SERVICE_NOT_CONFIGURED": FragmentServiceError,
    "INTERNAL_ERROR": FragmentAPIError,
}


def raise_for_error_response(response_data: dict) -> None:
    """Raise appropriate exception for error response."""
    if response_data.get("success", True):
        return

    error = response_data.get("error", {})
    raw_code = error.get("code", 500)
    code = raw_code if isinstance(raw_code, int) else 500
    message = error.get("message", "Unknown error")
    error_code = error.get("error_code")
    if not error_code and isinstance(raw_code, str):
        error_code = raw_code
    if not error_code:
        error_code = "INTERNAL_ERROR"

    details = []
    for detail in error.get("details", []):
        details.append(
            ErrorDetail(
                field=detail.get("field", ""),
                message=detail.get("message", ""),
            )
        )

    exception_class = ERROR_CODE_MAP.get(error_code, FragmentAPIError)

    if exception_class == RateLimitError:
        raise RateLimitError(message, code, error_code, details, retry_after=None)

    raise exception_class(message, code, error_code, details)
