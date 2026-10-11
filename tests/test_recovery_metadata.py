"""Recovery must preserve an existing order, never submit another purchase."""

from datetime import datetime, timezone
from email.utils import format_datetime
from unittest.mock import Mock

import pytest
import requests

from fragment_api import FragmentAPIClient, QueueStatus, QueuedRequest
from fragment_api.exceptions import FragmentAPIError, QueueTimeoutError, RateLimitError


def test_local_poll_timeout_preserves_request_id(monkeypatch: pytest.MonkeyPatch) -> None:
    client = FragmentAPIClient(poll_timeout=0)
    request = Mock(side_effect=AssertionError("must not submit anything"))
    monkeypatch.setattr(client, "_request", request)
    with pytest.raises(QueueTimeoutError) as caught:
        client._poll_result("existing-request")
    assert caught.value.request_id == "existing-request"
    assert "existing-request" in caught.value.message
    assert caught.value.error_code == "TIMEOUT"
    request.assert_not_called()


def test_server_timeout_preserves_request_id(monkeypatch: pytest.MonkeyPatch) -> None:
    client = FragmentAPIClient()
    get_status = Mock(return_value=QueuedRequest(id="existing-request", status=QueueStatus.TIMEOUT))
    monkeypatch.setattr(client, "get_status", get_status)
    with pytest.raises(QueueTimeoutError) as caught:
        client._poll_result("existing-request")
    assert caught.value.request_id == "existing-request"
    get_status.assert_called_once_with("existing-request")


@pytest.mark.parametrize("retry_after", ["30", "0", " 60 "])
def test_retry_after_seconds_exposed_without_retry(retry_after: str) -> None:
    client = FragmentAPIClient()
    response = Mock(status_code=429, headers={"Retry-After": retry_after})
    response.json.return_value = {
        "success": False,
        "error": {"code": 429, "error_code": "API_BUSY", "message": "busy"},
    }
    client._session.request = Mock(return_value=response)
    with pytest.raises(RateLimitError) as caught:
        client._request("POST", "/api/v1/premium/buy", {"seed": "synthetic"})
    assert caught.value.retry_after == int(retry_after)
    client._session.request.assert_called_once()


def test_retry_after_date_is_supported(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("fragment_api.client.time.time", lambda: 1_000_000)
    date = format_datetime(datetime.fromtimestamp(1_000_030, tz=timezone.utc), usegmt=True)
    client = FragmentAPIClient()
    response = Mock(status_code=429, headers={"Retry-After": date})
    response.json.return_value = {
        "success": False,
        "error": {"code": 429, "error_code": "RATE_LIMIT_EXCEEDED", "message": "wait"},
    }
    client._session.request = Mock(return_value=response)
    with pytest.raises(RateLimitError) as caught:
        client.get_prices()
    assert caught.value.retry_after == 30
    client._session.request.assert_called_once()


@pytest.mark.parametrize("retry_after", [None, "-1", "invalid", "1.5", "NaN"])
def test_invalid_retry_after_does_not_replace_the_api_error(retry_after: str | None) -> None:
    client = FragmentAPIClient()
    response = Mock(status_code=429, headers={"Retry-After": retry_after})
    response.json.return_value = {
        "success": False,
        "error": {"code": 429, "error_code": "API_BUSY", "message": "busy"},
    }
    client._session.request = Mock(return_value=response)
    with pytest.raises(RateLimitError) as caught:
        client.get_prices()
    assert caught.value.retry_after is None
    assert caught.value.error_code == "API_BUSY"


@pytest.mark.parametrize("error", [requests.Timeout("read timed out"), FragmentAPIError("bad", 502, "FRAGMENT_ERROR")])
def test_poll_failure_preserves_original_exception_and_request_id(
    monkeypatch: pytest.MonkeyPatch, error: Exception
) -> None:
    client = FragmentAPIClient()
    get_status = Mock(side_effect=error)
    monkeypatch.setattr(client, "get_status", get_status)
    with pytest.raises(type(error)) as caught:
        client._poll_result("existing-request")
    assert caught.value is error
    assert caught.value.request_id == "existing-request"
    get_status.assert_called_once()


def test_queue_timeout_error_legacy_constructor_still_works() -> None:
    error = QueueTimeoutError("timeout", 408, "TIMEOUT", [])
    assert error.request_id is None
    assert error.code == 408


def test_buy_stars_poll_timeout_never_submits_twice() -> None:
    client = FragmentAPIClient()
    accepted = Mock(status_code=202, headers={})
    accepted.json.return_value = {
        "success": True,
        "data": {"request_id": "saved-id", "position": 1, "estimated_wait_seconds": 1},
    }
    client._session.request = Mock(side_effect=[accepted, requests.Timeout("poll timeout")])
    with pytest.raises(requests.Timeout) as caught:
        client.buy_stars("@telegram_user", 50, seed="synthetic")
    assert caught.value.request_id == "saved-id"
    assert [call.args[0] for call in client._session.request.call_args_list] == ["POST", "GET"]


def test_initial_submission_failure_does_not_invent_request_id() -> None:
    client = FragmentAPIClient()
    client._session.request = Mock(side_effect=requests.Timeout("submission timeout"))
    with pytest.raises(requests.Timeout) as caught:
        client.buy_stars("@telegram_user", 50, seed="synthetic")
    assert getattr(caught.value, "request_id", None) is None
    client._session.request.assert_called_once()
