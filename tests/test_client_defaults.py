from pathlib import Path

import pytest

from fragment_api import DEFAULT_API_URL, FragmentAPIClient, WalletResolution, __version__
from fragment_api.exceptions import RateLimitError, ValidationError, raise_for_error_response


def test_client_uses_public_https_endpoint_by_default() -> None:
    client = FragmentAPIClient()

    assert DEFAULT_API_URL == "https://api.fragment-api.space"
    assert client.base_url == DEFAULT_API_URL
    assert __version__ == "2.1.6"


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
    ("wallet_address", "account_index", "expected"),
    [
        (None, None, {}),
        (None, 7, {"account_index": 7}),
        ("UQ_SELECTED", None, {"wallet_address": "UQ_SELECTED"}),
        ("UQ_SELECTED", 7, {"wallet_address": "UQ_SELECTED", "account_index": 7}),
    ],
)
def test_buy_stars_sends_wallet_selection(
    monkeypatch: pytest.MonkeyPatch,
    wallet_address: str | None,
    account_index: int | None,
    expected: dict[str, object],
) -> None:
    client = FragmentAPIClient()
    captured: dict[str, object] = {}

    def fake_request(method: str, path: str, data: dict) -> dict:
        captured.update(data)
        return {
            "success": True,
            "data": {
                "request_id": "req-1",
                "position": 1,
                "estimated_wait_seconds": 1,
            },
        }

    monkeypatch.setattr(client, "_request", fake_request)
    client.buy_stars(
        "@telegram_user",
        50,
        seed="c2VlZA==",
        wait=False,
        wallet_address=wallet_address,
        account_index=account_index,
    )

    selection = {
        key: captured[key] for key in ("wallet_address", "account_index") if key in captured
    }
    assert selection == expected


def test_buy_premium_sends_wallet_selection(monkeypatch: pytest.MonkeyPatch) -> None:
    client = FragmentAPIClient()
    captured: dict[str, object] = {}

    def fake_request(method: str, path: str, data: dict) -> dict:
        captured.update(data)
        return {"success": True, "data": {"success": True}}

    monkeypatch.setattr(client, "_request", fake_request)
    client.buy_premium(
        "@telegram_user",
        3,
        seed="c2VlZA==",
        wallet_address="UQ_SELECTED",
        account_index=9,
    )

    assert captured["wallet_address"] == "UQ_SELECTED"
    assert captured["account_index"] == 9


@pytest.mark.parametrize(
    ("wallet_address", "account_index"),
    [("UQ_SELECTED", None), (None, 3), ("UQ_SELECTED", 3)],
)
def test_resolve_wallet(
    monkeypatch: pytest.MonkeyPatch,
    wallet_address: str | None,
    account_index: int | None,
) -> None:
    client = FragmentAPIClient()
    captured: dict[str, object] = {}

    def fake_request(method: str, path: str, data: dict) -> dict:
        assert method == "POST"
        assert path == "/api/v1/wallet/resolve"
        captured.update(data)
        return {
            "success": True,
            "data": {
                "wallet_address": "UQ_RESOLVED",
                "wallet_version": "v5r1",
                "seed_format": "bip39-12",
                "account_index": 3,
            },
        }

    monkeypatch.setattr(client, "_request", fake_request)
    result = client.resolve_wallet(
        "c2VlZA==",
        wallet_address=wallet_address,
        account_index=account_index,
    )

    assert isinstance(result, WalletResolution)
    assert result.wallet_address == "UQ_RESOLVED"
    assert captured == {
        "seed": "c2VlZA==",
        **({"wallet_address": wallet_address} if wallet_address else {}),
        **({"account_index": account_index} if account_index is not None else {}),
    }


def test_resolve_wallet_requires_selector() -> None:
    with pytest.raises(ValueError, match="wallet_address or account_index"):
        FragmentAPIClient().resolve_wallet("c2VlZA==")


@pytest.mark.parametrize("account_index", [-1, 1.5, True, 2147483648])
def test_wallet_account_index_validation(account_index: object) -> None:
    with pytest.raises(ValueError, match="account_index"):
        FragmentAPIClient().resolve_wallet("c2VlZA==", account_index=account_index)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "error_code",
    ["INVALID_FRAGMENT_COOKIES", "INVALID_FRAGMENT_LOCAL_STORAGE"],
)
def test_session_payload_errors_are_validation_errors(error_code: str) -> None:
    with pytest.raises(ValidationError):
        raise_for_error_response(
            {
                "success": False,
                "error": {"code": 422, "error_code": error_code, "message": "invalid"},
            }
        )


@pytest.mark.parametrize(
    "error_code",
    ["INVALID_WALLET_ADDRESS", "WALLET_ADDRESS_MISMATCH", "ACCOUNT_INDEX_NOT_FOUND"],
)
def test_wallet_selection_errors_are_validation_errors(error_code: str) -> None:
    with pytest.raises(ValidationError) as captured:
        raise_for_error_response(
            {
                "success": False,
                "error": {"code": 422, "error_code": error_code, "message": "invalid"},
            }
        )

    assert captured.value.error_code == error_code


def test_api_busy_is_a_rate_limit_error() -> None:
    with pytest.raises(RateLimitError):
        raise_for_error_response(
            {
                "success": False,
                "error": {"code": 429, "error_code": "API_BUSY", "message": "busy"},
            }
        )


def test_public_examples_match_current_production_contract() -> None:
    root = Path(__file__).parents[1]
    public_files = [
        *root.joinpath("examples").glob("*.py"),
        root / "COOKIES_GUIDE.md",
        root / "COOKIES_GUIDE.ru.md",
    ]
    combined = "\n".join(path.read_text() for path in public_files)

    assert "your-api-server.com:8443" not in combined
    assert "your-server.com:8443" not in combined
    assert 'username="telegram_username"' not in combined
    assert 'username="telegram_user"' not in combined
    assert 'username="user"' not in combined
    assert "QueueStatus.TIMEOUT" in (root / "examples/async_mode.py").read_text()
    assert "300" in (root / "README.md").read_text()
    assert "RATE_LIMIT_EXCEEDED" in (root / "docs/errors.md").read_text()


def test_readmes_show_current_sdk_version() -> None:
    root = Path(__file__).parents[1]
    expected = f"Current SDK: `v{__version__}`"
    expected_badge = f"badge/PyPI-v{__version__}-38BDF8"

    for readme in (root / "README.md", root / "README.ru.md"):
        content = readme.read_text()
        assert expected in content
        assert expected_badge in content
