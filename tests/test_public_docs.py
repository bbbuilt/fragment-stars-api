"""Offline checks for the public integration entry points."""

import re
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_readme_starts_with_a_read_only_request_before_purchase_examples() -> None:
    for name in ("README.md", "README.ru.md"):
        text = (ROOT / name).read_text()
        assert len(re.findall(r"^# ", text, re.M)) == 1
        assert "Telegram Stars" in text.splitlines()[0]
        assert text.index("curl https://api.fragment-api.space/api/v1/prices") < text.index(
            "client.buy_stars("
        )
        assert "2.1.6" in text
        assert "0.25%" in text or "0,25%" in text
        assert "[SECURITY.md](SECURITY.md)" in text


def test_integration_guides_exist_and_use_the_canonical_endpoint() -> None:
    for name in ("python.md", "nodejs.md", "telegram-premium-api.md"):
        text = (ROOT / "docs" / name).read_text()
        assert "https://api.fragment-api.space" in text
        assert "@telegram_user" in text
        assert "../SECURITY.md" in text


def test_issue_forms_have_a_description() -> None:
    for path in ROOT.joinpath(".github/ISSUE_TEMPLATE").glob("*.yml"):
        text = path.read_text()
        assert re.search(r"^description: .+", text, re.M), path.name
        assert not re.search(r"^about:", text, re.M), path.name


def test_security_document_explains_the_hosted_signing_boundary() -> None:
    text = (ROOT / "SECURITY.md").read_text()
    assert "send your wallet seed to the API service" in text
    assert "Base64 is encoding, not encryption" in text
    assert "dedicated operating wallet" in text


def test_public_markdown_relative_file_links_exist() -> None:
    paths = [*ROOT.glob("*.md"), *ROOT.joinpath("docs").glob("*.md")]
    for path in paths:
        text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
        links = re.findall(r"\]\(([^)\s]+)\)", text)
        links += re.findall(r'(?:href|src)="([^"]+)"', text)
        for link in links:
            if ":" in link or link.startswith("#"):
                continue
            destination = link.split("#", 1)[0].split("?", 1)[0]
            assert (path.parent / destination).exists(), f"{path.name}: {link}"
