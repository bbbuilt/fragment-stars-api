from fragment_api import DEFAULT_API_URL, FragmentAPIClient, __version__


def test_client_uses_public_https_endpoint_by_default() -> None:
    client = FragmentAPIClient()

    assert DEFAULT_API_URL == "https://api-fragment.duckdns.org"
    assert client.base_url == DEFAULT_API_URL
    assert __version__ == "2.1.3"


def test_client_still_accepts_custom_endpoint() -> None:
    client = FragmentAPIClient("https://example.com/")

    assert client.base_url == "https://example.com"
