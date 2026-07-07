#!/usr/bin/env python3
"""Archive GitHub repository traffic snapshots and update a weekly scorecard."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO = os.getenv("GITHUB_REPOSITORY", "bbbuilt/fragment-stars-api")
TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / ".github-seo-data"
SCORECARD = ROOT / "GITHUB-WEEKLY-SCORECARD.md"


def github_get(path: str) -> object:
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN or GH_TOKEN is required for traffic endpoints")

    request = Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "fragment-stars-api-traffic-archiver",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def safe_get(path: str) -> object:
    try:
        return github_get(path)
    except HTTPError as exc:
        return {"error": f"HTTP {exc.code}", "path": path}
    except URLError as exc:
        return {"error": str(exc.reason), "path": path}


def load_recent_snapshots(limit: int = 7) -> list[dict]:
    snapshots: list[dict] = []
    for path in sorted(DATA_DIR.glob("*.json"), reverse=True)[:limit]:
        try:
            snapshots.append(json.loads(path.read_text()))
        except json.JSONDecodeError:
            continue
    return snapshots


def sum_count(payload: object, key: str) -> int:
    if isinstance(payload, dict) and isinstance(payload.get(key), int):
        return int(payload[key])
    return 0


def top_items(items: object, name_key: str, count_key: str, limit: int = 5) -> list[tuple[str, int]]:
    if not isinstance(items, list):
        return []
    result = []
    for item in items[:limit]:
        if isinstance(item, dict):
            result.append((str(item.get(name_key, "unknown")), int(item.get(count_key, 0) or 0)))
    return result


def write_scorecard(snapshots: list[dict]) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    latest = snapshots[0] if snapshots else {}
    weekly_views = sum(sum_count(s.get("views"), "count") for s in snapshots)
    weekly_unique_views = sum(sum_count(s.get("views"), "uniques") for s in snapshots)
    weekly_clones = sum(sum_count(s.get("clones"), "count") for s in snapshots)
    weekly_unique_clones = sum(sum_count(s.get("clones"), "uniques") for s in snapshots)
    stars = latest.get("repo", {}).get("stargazers_count", "unknown") if isinstance(latest.get("repo"), dict) else "unknown"

    referrers = top_items(latest.get("referrers"), "referrer", "count")
    paths = top_items(latest.get("popular_paths"), "path", "count")

    lines = [
        "# GitHub Weekly Scorecard",
        "",
        "Automated GitHub traffic snapshot for `bbbuilt/fragment-stars-api`.",
        "",
        f"Last updated: `{generated_at}`",
        "",
        "## Last 7 Archived Snapshots",
        "",
        f"- Stars: `{stars}`",
        f"- Views: `{weekly_views}` total / `{weekly_unique_views}` unique",
        f"- Clones: `{weekly_clones}` total / `{weekly_unique_clones}` unique",
        "",
        "## Latest Top Referrers",
        "",
    ]

    if referrers:
        lines.extend(f"- `{name}`: `{count}`" for name, count in referrers)
    else:
        lines.append("- No referrer data archived yet.")

    lines.extend(["", "## Latest Popular Paths", ""])
    if paths:
        lines.extend(f"- `{name}`: `{count}`" for name, count in paths)
    else:
        lines.append("- No path data archived yet.")

    lines.extend([
        "",
        "## Conversion Hypotheses to Review",
        "",
        "- If README views grow but clones/stars do not, improve first-screen CTA and examples.",
        "- If `docs/rest-api.md` gets traffic, add more non-Python examples.",
        "- If GitHub search/referrers are weak, tune topics, description, and README opening keywords.",
        "",
    ])

    SCORECARD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    DATA_DIR.mkdir(exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snapshot = {
        "date_utc": today,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": safe_get(f"/repos/{REPO}"),
        "views": safe_get(f"/repos/{REPO}/traffic/views"),
        "clones": safe_get(f"/repos/{REPO}/traffic/clones"),
        "referrers": safe_get(f"/repos/{REPO}/traffic/popular/referrers"),
        "popular_paths": safe_get(f"/repos/{REPO}/traffic/popular/paths"),
    }
    (DATA_DIR / f"{today}.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")
    write_scorecard(load_recent_snapshots())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"traffic archive failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
