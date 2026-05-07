"""
Fragment API Client

Simple client for purchasing Telegram Stars and Premium.
"""

import base64
import json
import time
from typing import Any, Optional, Union

import requests

from .exceptions import (
    InvalidResponseError,
    QueueTimeoutError,
    raise_for_error_response,
)
from .models import (
    BuyStarsResponse,
    CommissionRatesResponse,
    PurchaseResult,
    QueuedRequest,
    QueueStatus,
)

__version__ = "2.0.2"


class FragmentAPIClient:
    """
    Client for Fragment API.
    
    Example:
        >>> from fragment_api import FragmentAPIClient
        >>> client = FragmentAPIClient("https://your-server.com:8443")
        >>> 
        >>> # Buy stars (no KYC - uses owner cookies)
        >>> result = client.buy_stars("username", 50, seed="your_seed_base64")
        >>> 
        >>> # Buy stars with KYC (lower commission)
        >>> result = client.buy_stars("username", 50, seed="...", cookies="cookies_base64")
        >>> 
        >>> # Buy premium
        >>> result = client.buy_premium("username", 3, seed="...")  # 3 months
    """
    
    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        poll_timeout: float = 300.0,
    ):
        """
        Initialize client.
        
        Args:
            base_url: API server URL (required)
            timeout: Request timeout in seconds
            poll_timeout: Max time to wait for queue result
        """
        if not base_url:
            raise ValueError("base_url is required")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.poll_timeout = poll_timeout
        self._session = requests.Session()
        self._session.headers["Content-Type"] = "application/json"

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
        raise_on_error: bool = True,
    ) -> dict:
        """Make API request."""
        url = f"{self.base_url}{path}"
        response = self._session.request(method, url, json=data, timeout=self.timeout)
        try:
            result = response.json()
        except ValueError as exc:
            body_preview = response.text[:300] if response.text else "<empty response>"
            raise InvalidResponseError(
                f"API returned non-JSON response: {body_preview}",
                response.status_code,
                "INVALID_RESPONSE",
            ) from exc
        
        if raise_on_error and not result.get("success", False):
            raise_for_error_response(result)
        
        return result
    
    def buy_stars(
        self,
        username: str,
        amount: int,
        seed: str,
        cookies: Optional[str] = None,
        local_storage: Optional[Union[str, dict]] = None,
        wait: bool = True,
    ) -> Union[BuyStarsResponse, PurchaseResult]:
        """
        Buy Telegram Stars.
        
        Args:
            username: Telegram username
            amount: Number of stars
            seed: Wallet seed (base64)
            cookies: Fragment cookies (base64) - optional, for KYC mode
            local_storage: Fragment localStorage (base64 or dict) - optional
            wait: Wait for result (default: True)
            
        Returns:
            PurchaseResult if wait=True, else BuyStarsResponse
        """
        data: dict[str, Any] = {
            "username": username,
            "amount": amount,
            "seed": seed,
        }
        
        if cookies:
            data["fragment_cookies"] = self._normalize_cookies(cookies)
        if local_storage:
            data["fragment_local_storage"] = self._normalize_json_blob(local_storage)
        
        result = self._request("POST", "/api/v1/stars/buy", data)
        response = BuyStarsResponse(
            request_id=result["data"]["request_id"],
            position=result["data"]["position"],
            estimated_wait_seconds=result["data"]["estimated_wait_seconds"],
            message=result["data"].get("message", ""),
        )
        
        if not wait:
            return response
        
        return self._poll_result(response.request_id)

    def buy_premium(
        self,
        username: str,
        duration: int,
        seed: str,
        cookies: Optional[str] = None,
        local_storage: Optional[Union[str, dict]] = None,
        wait: bool = True,
    ) -> Union[BuyStarsResponse, PurchaseResult]:
        """
        Buy Telegram Premium.
        
        Args:
            username: Telegram username
            duration: Months (3, 6, or 12)
            seed: Wallet seed (base64)
            cookies: Fragment cookies (base64) - optional, for KYC mode
            local_storage: Fragment localStorage (base64 or dict) - optional
            wait: Kept for backward compatibility. Premium returns final result directly.
            
        Returns:
            PurchaseResult for the current API, or BuyStarsResponse for legacy queued APIs
        """
        data: dict[str, Any] = {
            "username": username,
            "duration": duration,
            "seed": seed,
        }
        
        if cookies:
            data["fragment_cookies"] = self._normalize_cookies(cookies)
        if local_storage:
            data["fragment_local_storage"] = self._normalize_json_blob(local_storage)
        
        result = self._request("POST", "/api/v1/premium/buy", data)
        data_result = result.get("data")

        # Backward compatibility with older queued Premium API responses.
        if isinstance(data_result, dict) and "request_id" in data_result:
            response = BuyStarsResponse(
                request_id=data_result["request_id"],
                position=data_result["position"],
                estimated_wait_seconds=data_result["estimated_wait_seconds"],
                message=data_result.get("message", ""),
            )
            if not wait:
                return response
            return self._poll_result(response.request_id)

        return self._purchase_result_from_dict(result)

    def get_rates(self) -> CommissionRatesResponse:
        """
        Get commission rates.
        
        Returns:
            CommissionRatesResponse with rate_no_kyc and rate_with_kyc
        """
        result = self._request("GET", "/api/v1/commission/rates")
        return CommissionRatesResponse.from_dict(result["data"])
    
    def get_queue_status(self) -> dict:
        """
        Get queue status information.
        
        Returns:
            dict with queue_length and estimated_wait_seconds
        """
        result = self._request("GET", "/api/v1/queue/status")
        return result["data"]
    
    def check_premium_eligibility(self, username: str) -> dict:
        """
        Check if user is eligible for Premium purchase.
        
        Args:
            username: Telegram username
            
        Returns:
            dict with eligibility status and reason
        """
        data = {"username": username}
        result = self._request(
            "POST",
            "/api/v1/premium/check-eligibility",
            data,
            raise_on_error=False,
        )
        payload = result.get("data") if isinstance(result.get("data"), dict) else result
        normalized = {
            "eligible": bool(payload.get("eligible", False)),
            "username": payload.get("username"),
        }
        error = payload.get("error") or {}
        if error:
            normalized["reason"] = error.get("message", "Unknown error")
            normalized["error_code"] = error.get("error_code") or error.get("code")
        elif payload.get("reason"):
            normalized["reason"] = payload["reason"]
        return normalized
    
    def get_status(self, request_id: str) -> QueuedRequest:
        """
        Get request status.
        
        Args:
            request_id: Request ID
            
        Returns:
            QueuedRequest with status
        """
        result = self._request("GET", f"/api/v1/queue/{request_id}")
        return QueuedRequest.from_dict(result["data"])
    
    def _poll_result(self, request_id: str) -> PurchaseResult:
        """Poll until request completes."""
        start = time.time()
        
        while time.time() - start < self.poll_timeout:
            status = self.get_status(request_id)
            
            if status.status == QueueStatus.COMPLETED:
                r = status.result or {}
                return self._purchase_result_from_dict(r)
            
            if status.status == QueueStatus.FAILED:
                return PurchaseResult(success=False, error=status.error or "Unknown error")
            
            if status.status == QueueStatus.TIMEOUT:
                raise QueueTimeoutError(f"Request timed out: {request_id}", 408, "TIMEOUT")
            
            time.sleep(2)
        
        raise QueueTimeoutError(f"Polling timed out after {self.poll_timeout}s", 408, "TIMEOUT")

    def _purchase_result_from_dict(self, data: dict[str, Any]) -> PurchaseResult:
        """Convert direct or queued purchase response data to PurchaseResult."""
        payload = data.get("data") if isinstance(data.get("data"), dict) else data
        return PurchaseResult(
            success=bool(payload.get("success", data.get("success", True))),
            transaction_id=payload.get("transaction_id"),
            transaction_hash=payload.get("transaction_hash") or payload.get("tx_hash"),
            invoice_id=payload.get("invoice_id") or payload.get("fragment_invoice_id"),
            username=payload.get("username"),
            amount=payload.get("stars_amount") or payload.get("amount"),
            duration_months=payload.get("duration_months"),
            cost_ton=payload.get("cost_ton"),
            commission_ton=payload.get("commission_ton"),
            commission_rate=payload.get("commission_rate"),
            mode=payload.get("mode"),
            commission_balance_ton=payload.get("commission_balance_ton"),
            expires_at=payload.get("expires_at"),
            timestamp=payload.get("timestamp"),
            payment_required=payload.get("payment_required"),
            payment_invoice=payload.get("payment_invoice"),
        )

    def _normalize_cookies(self, cookies: Union[str, list, dict]) -> str:
        """Convert cookies to base64 string."""
        if isinstance(cookies, str):
            return cookies
        
        if isinstance(cookies, dict):
            cookies = [
                {"name": k, "value": v, "domain": ".fragment.com", "path": "/"}
                for k, v in cookies.items()
            ]
        
        return self._normalize_json_blob(cookies)

    def _normalize_json_blob(self, value: Union[str, list, dict]) -> str:
        """Return base64 JSON for dict/list values, or pass through strings."""
        if isinstance(value, str):
            return value
        return base64.b64encode(json.dumps(value).encode()).decode()
    
    def close(self):
        """Close session."""
        self._session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
