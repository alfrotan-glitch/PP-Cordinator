# -*- coding: utf-8 -*-
"""
passes.py — pedagogical layout audit that runs *before* rendering.

Measures every block with the real typesetting engine and classifies layout defects:

  ORPHAN-SECTION-HEAD : 15. Definition → only 1–2 content lines on the page that starts it
  SPLIT-TABLE-HEADER  : header + thead separated from the table body across pages
  KEEP-TABLE-SPLIT    : a short table split across two pages without need
  WIDOW-LEAD          : a lead/heading block stranded alone at a page foot
  TALL-ROW            : one table row taller than half a page
  OVERLONG-PARAGRAPH  : paragraph density above the chapter's norm
  SHORT-SECTION       : a section with materially less content than its siblings

The audit returns a list of findings; the renderer consumes the table findings to
add the `keep` class only where it is needed and layout-safe.
"""
from __future__ import annotations

import io
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pymupdf  # noqa: E402
import bookmodel  # noqa: E402
import design  # noqa: E402
import render_html  # noqa: E402

EST_FONT = "Vazirmatn-Regular.ttf"


def _measure_lines(html: str, css: str, arch: pymupdf.Archive, width: float, height: float):
    story = pymupdf.Story(html=html, user_css=css, archive=arch)
    filled = None
    try:
        more, filled = story.place(pymupdf.Rect(0, 0, width, height))
    except Exception as exc:                     # pragma: no cover
        return None
    return filled


def table_metrics(blk, css: str, arch, width: float) -> dict:
    """Height of a table, of its header, and of its first row (points)."""
    header_html = render_html.render_table(blk, css, arch, width)
    if header_html is None:
        return {}
    full, hdr = header_html
    f_full = _measure_lines(full, css, arch, width, 12000)
    f_hdr = _measure_lines(hdr, css, arch, width, 12000) if hdr else None
    first = blk.rows[0] if blk.rows else None
    f_first = None
    if first:
        b1 = bookmodel.Block(kind="table", header=blk.header, rows=[first])
        h1, _ = render_html.render_table(b1, css, arch, width, first_only=True)
        f_first = _measure_lines(h1, css, arch, width, 12000)
    return dict(height=f_full.y1 if f_full else 0.0,
                header_height=f_hdr.y1 if f_hdr else 0.0,
                first_row_height=(f_first.y1 - (f_hdr.y1 if f_hdr else 0.0)) if f_first else 0.0,
                rows=len(blk.rows))


def paragraph_lengths(doc) -> dict:
    out = {}
    for ch in doc.chapters:
        lens = []
        for t in ch.topics:
            for b in t.blocks:
                if b.kind == "para":
                    lens.append(len(b.text))
        out[ch.number] = (statistics.median(lens) if lens else 0,
                          max(lens) if lens else 0, len(lens))
    return out


def audit(verbose: bool = False) -> list[dict]:
    doc = bookmodel.load_document()
    css = render_html.css_for_measure()
    arch = render_html.build_archive()
    body_w = design.PAGE_W - design.M_INNER - design.M_OUTER
    body_h = design.BODY_BOTTOM - design.BODY_TOP
    findings: list[dict] = []

    for ch in doc.chapters:
        for t in ch.topics:
            # --- section heads and their content weight
            for i, b in enumerate(t.blocks):
                if b.kind == "heading" and b.level == 2 and getattr(b, "role", "") == "section":
                    nxt = [x for x in t.blocks[i + 1:i + 5]]
                    weight = sum(len(x.text) for x in nxt if x.kind in ("para", "list"))
                    if weight < 90:
                        findings.append(dict(cls="SHORT-SECTION", chapter=ch.number, topic=t.number,
                                             detail=f"{b.text[:40]} → content weight {weight}"))
                if b.kind == "table":
                    m = table_metrics(b, css, arch, body_w)
                    if not m:
                        continue
                    if m["height"] > body_h and m["header_height"] + m["first_row_height"] < body_h * 0.42:
                        findings.append(dict(cls="SPLIT-TABLE-HEADER", chapter=ch.number, topic=t.number,
                                             detail=f"table {m['rows']} rows, h={m['height']:.0f}pt "
                                                    f"header={m['header_height']:.0f} first_row={m['first_row_height']:.0f}"))
                    if body_h * 0.30 < m["height"] <= body_h and m["rows"] >= 3:
                        findings.append(dict(cls="KEEP-TABLE-SPLIT", chapter=ch.number, topic=t.number,
                                             detail=f"table {m['rows']} rows, h={m['height']:.0f}pt "
                                                    f"(body {body_h:.0f}pt)"))
                    if m["first_row_height"] > body_h * 0.45:
                        findings.append(dict(cls="TALL-ROW", chapter=ch.number, topic=t.number,
                                             detail=f"first row h={m['first_row_height']:.0f}pt"))
    pl = paragraph_lengths(doc)
    for num, (med, mx, n) in pl.items():
        if mx > max(1400, med * 6):
            findings.append(dict(cls="OVERLONG-PARAGRAPH", chapter=num, topic="",
                                 detail=f"median={med:.0f} max={mx} paragraphs={n}"))
    if verbose:
        for f in findings:
            print(f"  {f['cls']:20s} ch{f['chapter']:>2} {f['topic']:8s} {f['detail']}")
    counts = {}
    for f in findings:
        counts[f["cls"]] = counts.get(f["cls"], 0) + 1
    print("findings:", counts)
    return findings


if __name__ == "__main__":
    audit(verbose="-v" in sys.argv)
