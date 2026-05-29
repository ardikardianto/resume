#!/usr/bin/env python3
"""Render the first page of the resume PDF to assets/resume-preview.png."""

from __future__ import annotations

from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "Ardianto's Resume.pdf"
PREVIEW_PATH = ROOT / "assets" / "resume-preview.png"


def main() -> int:
    doc = fitz.open(PDF_PATH)
    page = doc[0]
    zoom = 1200 / page.rect.height
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=True)
    pix.save(PREVIEW_PATH)
    print(f"Rendered {PREVIEW_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
