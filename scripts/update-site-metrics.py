#!/usr/bin/env python3
"""Update public scholarly metrics in index.html.

The updater is dependency-free so it can run in GitHub Actions with the
default Python runtime. ORCID and Google Scholar are fetched directly from
public pages/APIs. ResearchGate is best-effort because the public profile can
return Cloudflare 1020 to automated requests; when that happens, the existing
ResearchGate values in index.html are preserved.
"""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


ORCID_WORKS_URL = "https://pub.orcid.org/v3.0/0000-0001-8642-5840/works"
RESEARCHGATE_URL = "https://www.researchgate.net/profile/Ardik-Ardianto"
SCHOLAR_URL = "https://scholar.google.com/citations?user=LATwILMAAAAJ&hl=en"
INDEX_PATH = Path(__file__).resolve().parents[1] / "index.html"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0 Safari/537.36"
)


def fetch_text(url: str, *, accept: str | None = None) -> str:
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_orcid_works() -> int:
    data = json.loads(fetch_text(ORCID_WORKS_URL, accept="application/json"))
    return len(data.get("group", []))


def extract_scholar_citations() -> int:
    profile_html = fetch_text(SCHOLAR_URL)
    text = html.unescape(profile_html)

    meta_match = re.search(r"Cited by\s+([\d,]+)", text)
    if meta_match:
        return int(meta_match.group(1).replace(",", ""))

    table_match = re.search(
        r"Citations</a></td><td class=\"gsc_rsb_std\">([\d,]+)</td>",
        profile_html,
    )
    if table_match:
        return int(table_match.group(1).replace(",", ""))

    raise ValueError("Could not find Google Scholar citation count.")


def parse_compact_number(value: str) -> int:
    value = value.strip().replace(",", "")
    multiplier = 1
    if value[-1:].lower() == "k":
        multiplier = 1_000
        value = value[:-1]
    elif value[-1:].lower() == "m":
        multiplier = 1_000_000
        value = value[:-1]
    return int(float(value) * multiplier)


def extract_first(patterns: list[str], text: str) -> int | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return parse_compact_number(match.group(1))
    return None


def extract_researchgate_metrics() -> tuple[int | None, int | None]:
    try:
        page = fetch_text(RESEARCHGATE_URL)
    except urllib.error.HTTPError as exc:
        print(f"ResearchGate skipped: HTTP {exc.code}", file=sys.stderr)
        return None, None
    except urllib.error.URLError as exc:
        print(f"ResearchGate skipped: {exc.reason}", file=sys.stderr)
        return None, None

    text = html.unescape(page)
    reads = extract_first(
        [
            r'"(?:readsCount|readCount|totalReads)"\s*:\s*"?([\d,.]+[km]?)"?',
            r'([\d,.]+[km]?)\s*(?:publication\s*)?reads\b',
            r'\breads\b[^0-9]{0,80}([\d,.]+[km]?)',
        ],
        text,
    )
    citations = extract_first(
        [
            r'"(?:citationsCount|citationCount|totalCitations)"\s*:\s*"?([\d,.]+[km]?)"?',
            r'([\d,.]+[km]?)\s*citations\b',
            r'\bcitations\b[^0-9]{0,80}([\d,.]+[km]?)',
        ],
        text,
    )
    if reads is None or citations is None:
        print("ResearchGate skipped: profile metrics were not found.", file=sys.stderr)
    return reads, citations


def current_metric(key: str) -> int:
    page = INDEX_PATH.read_text(encoding="utf-8")
    match = re.search(rf'<b data-metric="{re.escape(key)}">([\d,]+)</b>', page)
    if not match:
        raise ValueError(f"Could not find existing metric {key!r} in index.html.")
    return int(match.group(1).replace(",", ""))


def preserve_on_error(key: str, extractor) -> int:
    try:
        return extractor()
    except Exception as exc:
        print(f"{key} preserved: {exc}", file=sys.stderr)
        return current_metric(key)


def update_metric(page: str, key: str, value: int | None) -> tuple[str, bool]:
    if value is None:
        return page, False

    next_page, replacements = re.subn(
        rf'(<b data-metric="{re.escape(key)}">)([\d,]+)(</b>)',
        lambda match: f"{match.group(1)}{value:,}{match.group(3)}",
        page,
        count=1,
    )
    if replacements != 1:
        raise ValueError(f"Could not find metric {key!r} in index.html.")
    return next_page, next_page != page


def update_index(metrics: dict[str, int | None]) -> bool:
    page = INDEX_PATH.read_text(encoding="utf-8")
    changed = False
    for key, value in metrics.items():
        page, metric_changed = update_metric(page, key, value)
        changed = changed or metric_changed

    if changed:
        INDEX_PATH.write_text(page, encoding="utf-8")
    return changed


def main() -> int:
    researchgate_reads, researchgate_citations = extract_researchgate_metrics()
    metrics = {
        "orcid-works": preserve_on_error("orcid-works", extract_orcid_works),
        "researchgate-reads": researchgate_reads,
        "researchgate-citations": researchgate_citations,
        "google-scholar-citations": preserve_on_error(
            "google-scholar-citations",
            extract_scholar_citations,
        ),
    }
    changed = update_index(metrics)

    for key, value in metrics.items():
        shown = f"{value:,}" if value is not None else "preserved"
        print(f"{key}: {shown}")
    print("index.html updated" if changed else "index.html already current")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"update failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
