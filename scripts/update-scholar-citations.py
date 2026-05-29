#!/usr/bin/env python3
"""Update the Google Scholar citation metric in index.html.

This script intentionally has no third-party dependencies so it can run in
GitHub Actions with the default Python runtime.
"""

from __future__ import annotations

import html
import re
import sys
import urllib.request
from pathlib import Path


PROFILE_URL = "https://scholar.google.com/citations?user=LATwILMAAAAJ&hl=en"
INDEX_PATH = Path(__file__).resolve().parents[1] / "index.html"


def fetch_profile() -> str:
    request = urllib.request.Request(
        PROFILE_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_citations(profile_html: str) -> int:
    meta_match = re.search(r'Cited by\s+([\d,]+)', html.unescape(profile_html))
    if meta_match:
        return int(meta_match.group(1).replace(",", ""))

    table_match = re.search(
        r"Citations</a></td><td class=\"gsc_rsb_std\">([\d,]+)</td>",
        profile_html,
    )
    if table_match:
        return int(table_match.group(1).replace(",", ""))

    raise ValueError("Could not find Google Scholar citation count in profile HTML.")


def update_index(citations: int) -> bool:
    page = INDEX_PATH.read_text(encoding="utf-8")
    next_page, replacements = re.subn(
        r'(<b data-metric="google-scholar-citations">)([\d,]+)(</b>)',
        lambda match: f"{match.group(1)}{citations:,}{match.group(3)}",
        page,
        count=1,
    )
    if replacements != 1:
        raise ValueError("Could not find Google Scholar citation metric in index.html.")

    if next_page == page:
        return False

    INDEX_PATH.write_text(next_page, encoding="utf-8")
    return True


def main() -> int:
    citations = extract_citations(fetch_profile())
    changed = update_index(citations)
    print(f"Google Scholar citations: {citations:,}")
    print("index.html updated" if changed else "index.html already current")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"update failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
