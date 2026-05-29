#!/usr/bin/env python3
"""Overlay current site metrics onto the resume PDF.

The repository only stores the final PDF, not the original design source. This
script keeps the visible PDF metrics aligned with index.html by covering the
known metric areas and drawing the current values back on top.
"""

from __future__ import annotations

import re
import tempfile
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"
PDF_PATH = ROOT / "Ardianto's Resume.pdf"

PAGE_WIDTH = 594.95996
PAGE_HEIGHT = 841.91998

PAPER = "#f5f4ed"
ACCENT = "#1b365d"
INK = "#141413"
MUTED = "#504e49"
SOFT_BLUE = "#eef2f7"


def metric(key: str) -> str:
    html = INDEX_PATH.read_text(encoding="utf-8")
    match = re.search(rf'<b data-metric="{re.escape(key)}">([\d,]+)</b>', html)
    if not match:
        raise ValueError(f"Metric {key!r} not found in index.html")
    return match.group(1)


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width: float, size: float, leading: float, color: str = MUTED) -> None:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if c.stringWidth(candidate, "Times-Roman", size) <= width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    c.setFont("Times-Roman", size)
    c.setFillColor(color)
    for offset, line in enumerate(lines):
        c.drawString(x, y - offset * leading, line)


def draw_metric(c: canvas.Canvas, x: float, y: float, value: str, suffix: str, label: str, label_width: float) -> None:
    c.setFillColor(ACCENT)
    c.setFont("Times-Roman", 17.4)
    c.drawString(x, y, value)
    if suffix:
        c.setFont("Times-Roman", 10.4)
        c.drawString(x + c.stringWidth(value, "Times-Roman", 17.4) + 2.0, y + 1.0, suffix)
    draw_wrapped(c, label, x, y - 13.0, label_width, 9.3, 10.4)


def page_one_overlay(metrics: dict[str, str]) -> PdfReader:
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    c.setFillColor(PAPER)
    c.rect(28, 705, 542, 66, stroke=0, fill=1)
    c.rect(82, 407, 470, 30, stroke=0, fill=1)

    draw_metric(c, 36, 750, "10", "yrs", "translation track since 2016", 75)
    draw_metric(c, 150, 750, metrics["orcid-works"], "works", "ORCID-listed works", 80)
    draw_metric(c, 270, 750, metrics["researchgate-reads"], "", "ResearchGate reads", 82)
    draw_metric(c, 390, 750, metrics["researchgate-citations"], "", "ResearchGate citations", 70)
    draw_metric(c, 486, 750, metrics["google-scholar-citations"], "", "Google Scholar citations", 68)

    c.setFont("Times-Roman", 9.6)
    c.setFillColor(INK)
    c.drawString(83, 425, f"Public research profile lists 16 ResearchGate publications, {metrics['researchgate-reads']} reads,")
    c.drawString(83, 412, f"{metrics['researchgate-citations']} ResearchGate citations, and {metrics['google-scholar-citations']} Google Scholar citations.")

    c.save()
    packet.seek(0)
    return PdfReader(packet)


def page_two_overlay(metrics: dict[str, str]) -> PdfReader:
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    c.setFillColor(PAPER)
    c.rect(34, 730, 528, 62, stroke=0, fill=1)

    c.setFont("Times-Roman", 9.8)
    c.setFillColor(ACCENT)
    c.drawString(36, 782, "Publication record centered on language in use.")
    c.setFillColor(INK)
    c.drawString(230, 782, "Selected work covers translation style, contextual configuration,")
    c.drawString(36, 768, "sociolinguistics, discourse, code-switching, and English teaching materials. Public profile:")
    c.drawString(
        36,
        754,
        f"{metrics['orcid-works']} ORCID works · 16 ResearchGate publications · "
        f"{metrics['researchgate-citations']} ResearchGate citations · "
        f"{metrics['google-scholar-citations']} Google Scholar citations.",
    )

    c.save()
    packet.seek(0)
    return PdfReader(packet)


def main() -> int:
    metrics = {
        "orcid-works": metric("orcid-works"),
        "researchgate-reads": metric("researchgate-reads"),
        "researchgate-citations": metric("researchgate-citations"),
        "google-scholar-citations": metric("google-scholar-citations"),
    }

    base = PdfReader(str(PDF_PATH))
    overlays = [page_one_overlay(metrics), page_two_overlay(metrics)]
    writer = PdfWriter()
    for index, page in enumerate(base.pages):
        page.merge_page(overlays[index].pages[0])
        writer.add_page(page)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        writer.write(tmp)
        temp_path = Path(tmp.name)

    temp_path.replace(PDF_PATH)
    print("Updated resume PDF metrics:")
    for key, value in metrics.items():
        print(f"- {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
