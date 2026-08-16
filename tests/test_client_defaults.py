import pytest

from fragment_api import DEFAULT_API_URL, FragmentAPIClient, __version__
from fragment_api.exceptions import RateLimitError, ValidationError, raise_for_error_response


def test_client_uses_public_https_endpoint_by_default() -> None:
    client = FragmentAPIClient()

    assert DEFAULT_API_URL == "https://api.fragment-api.space"
    assert client.base_url == DEFAULT_API_URL
    assert __version__ == "2.1.5"


def test_client_still_accepts_custom_endpoint() -> None:
    client = FragmentAPIClient("https://example.com/")

    assert client.base_url == "https://example.com"


def test_buy_stars_rejects_less_than_50_without_network(monkeypatch: pytest.MonkeyPatch) -> None:
    client = FragmentAPIClient()
    monkeypatch.setattr(client, "_request", lambda *args, **kwargs: pytest.fail("network called"))

    with pytest.raises(ValueError, match="at least 50"):
        client.buy_stars("@telegram_user", 49, seed="c2VlZA==")


def test_buy_stars_rejects_base64_cookies_without_json(monkeypatch: pytest.MonkeyPatch) -> None:
    client = FragmentAPIClient()
    monkeypatch.setattr(client, "_request", lambda *args, **kwargs: pytest.fail("network called"))

    with pytest.raises(ValueError, match="Base64-encoded JSON"):
        client.buy_stars(
            "@telegram_user",
            50,
            seed="c2VlZA==",
            cookies="bm90LWpzb24=",
        )


@pytest.mark.parametrize(
    "error_code",
    ["INVALID_FRAGMENT_COOKIES", "INVALID_FRAGMENT_LOCAL_STORAGE"],
)
def test_session_payload_errors_are_validation_errors(error_code: str) -> None:
    with pytest.raises(ValidationError):
        raise_for_error_response({
            "success": False,
            "error": {"code": 422, "error_code": error_code, "message": "invalid"},
        })


def test_api_busy_is_a_rate_limit_error() -> None:
    with pytest.raises(RateLimitError):
        raise_for_error_response({
            "success": False,
            "error": {"code": 429, "error_code": "API_BUSY", "message": "busy"},
        })
