# -*- coding: utf-8 -*-
"""
render_html.py — turn the document model into styled HTML fragments for the PDF and
EPUB renderers.  Pure presentation: no text is added, removed or reordered.
"""
from __future__ import annotations

import html as _html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bookmodel as bm
import design

ARCHIVE = None


# --------------------------------------------------------------- font archive

def build_archive() -> "object":
    """PyMuPDF Archive that resolves the @font-face file names used in the CSS."""
    global ARCHIVE
    if ARCHIVE is not None:
        return ARCHIVE
    import pymupdf
    import fonts
    try:
        fonts.configure()
    except Exception:
        pass
    arch = pymupdf.Archive(design.FONT_DIR_PDF or design.FONT_DIR)
    ARCHIVE = arch
    return arch


def css_for_measure() -> str:
    faces = []
    for fam, files in design.FONTS.items():
        for path in files:
            style = "italic" if "Italic" in path else "normal"
            if "Bold" in path:
                weight = "700"
            elif "SemiBold" in path:
                weight = "600"
            elif "Medium" in path:
                weight = "500"
            else:
                weight = "400"
            faces.append(
                "@font-face {font-family: '%s'; font-style: %s; font-weight: %s; "
                "src: url(%s);}" % (fam, style, weight, os.path.basename(path)))
    return "\n".join(faces) + "\n" + design.css()


# ------------------------------------------------------------------- escaping

def esc(text: str) -> str:
    return _html.escape(text, quote=False)


BIDI_FIXES = [
    ("«", "\u00ab"), ("»", "\u00bb"),
]

# Comparison signs carry the Unicode Bidi_Mirrored property: inside an RTL run the
# renderer draws the mirror image, so an author's «>۳» reaches the page as «<۳» and
# states the opposite criterion.  A left-to-right mark in front of the sign resolves it
# as LTR, which keeps the glyph the manuscript wrote; the mark itself is invisible and
# is dropped again by text extraction.
_OP_CHARS = "<>"


def spans_text(text: str) -> str:
    """Escape `text`, prefixing every comparison operator with an invisible LRM."""
    if any(c in _OP_CHARS for c in text):
        text = text.replace("<", "\u200e<").replace(">", "\u200e>")
    return esc(text)


def spans_html(spans: list) -> str:
    out = []
    for s in spans:
        t = spans_text(s.text)
        if s.code:
            out.append(f"<code>{t}</code>")
            continue
        if s.bold:
            t = f"<b>{t}</b>"
        if s.italic:
            t = f"<i>{t}</i>"
        if getattr(s, "sup", False):
            t = f"<sup>{t}</sup>"
        elif getattr(s, "sub", False):
            t = f"<sub>{t}</sub>"
        out.append(t)
    return "".join(out)


def is_english(text: str) -> bool:
    return bm.lang_of(text) == "en"


def measure_height(html: str, width: float | None = None) -> float:
    """Height (pt) that `html` occupies at the book's text width."""
    import pymupdf
    width = width or (design.PAGE_W - design.M_INNER - design.M_OUTER)
    story = pymupdf.Story(html=html, user_css=css_for_measure(), archive=build_archive())
    try:
        more, filled = story.place(pymupdf.Rect(0, 0, width, 20000))
    except Exception:
        return 0.0
    return filled[3] - filled[1]


# ------------------------------------------------------------------- blocks

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def render_list(blk, bid: str = "") -> str:
    """Flat list rendering that preserves the manuscript's indentation and ordinals."""
    items = [it for it in blk.items if isinstance(it, tuple)]
    if not items:
        return ""
    base = min(i for i, _, _ in items)
    iattr = f' id="{bid}"' if bid else ""
    out = [f'<div class="listbox"{iattr}>']
    counters: dict[int, int] = {}
    for indent, kind, body in items:
        lvl = max(0, (indent - base) // 2)
        if kind == "ol":
            counters[lvl] = counters.get(lvl, 0) + 1
            marker = str(counters[lvl]).translate(FA_DIGITS) + "."
            for k in list(counters):
                if k > lvl:
                    del counters[k]
        else:
            marker = "•"
            counters.pop(lvl, None)
        txt = body[2:] if body.startswith("* ") else body
        out.append(f'<p class="li" style="margin-right:{lvl * 12}pt">'
                   f'<b class="mk">{marker}</b>&#8201;<span class="tx">'
                   f'{spans_html(bm.parse_inline(txt))}</span></p>')
    out.append("</div>")
    return "\n".join(out)


def cell_html(cell: str, is_header: bool = False) -> str:
    txt = bm.plain_text(cell)
    cls = ""
    if bm.lang_of(txt) == "en":
        cls = ' class="en" dir="ltr"'
    else:
        cls = ' class="fa"'
    return f"<td{cls}>{spans_html(bm.parse_inline(cell)) or '&nbsp;'}</td>"


def render_table(blk, css: str = "", arch=None, width: float = 0.0, first_only: bool = False,
                 bid: str = ""):
    """Return (html, header_only_html_or_None)."""
    if not blk.header and not blk.rows:
        return None
    ncols = max(len(blk.header or []), max((len(r) for r in (blk.rows or [])), default=0))
    cls = "appendix" if getattr(blk, "role", "") == "audit-table" else "data"
    widths = _column_widths(blk, ncols)
    colgroup = "<colgroup>" + "".join(f'<col style="width:{w}%">' for w in widths) + "</colgroup>"
    head_cells = []
    for i in range(ncols):
        cell = blk.header[i] if blk.header and i < len(blk.header) else ""
        txt = bm.plain_text(cell)
        c = 'class="en" dir="ltr"' if bm.lang_of(txt) == "en" else 'class="fa"'
        head_cells.append(f"<th {c}>{spans_html(bm.parse_inline(cell)) or '&nbsp;'}</th>")
    thead = f"<thead><tr>{''.join(head_cells)}</tr></thead>"
    rows = blk.rows[:1] if first_only else blk.rows
    body = []
    for row in rows:
        cells = [cell_html(row[i] if i < len(row) else "") for i in range(ncols)]
        body.append(f"<tr>{''.join(cells)}</tr>")
    tbody = f"<tbody>{''.join(body)}</tbody>"
    iattr = f' id="{bid}"' if bid else ""
    full = f'<table class="{cls}"{iattr}>{colgroup}{thead}{tbody}</table>'
    header_only = f'<table class="{cls}">{colgroup}{thead}</table>'
    return full, header_only


def _column_widths(blk, ncols: int) -> list[float]:
    """Content-aware column widths (percent)."""
    if ncols <= 1:
        return [100.0]
    if getattr(blk, "role", "") == "audit-table":
        base = [5, 34, 61] if ncols == 3 else [100.0 / ncols] * ncols
        return (base + [100.0 / ncols] * ncols)[:ncols]
    lengths = []
    for i in range(ncols):
        vals = [len(bm.plain_text(blk.header[i])) if blk.header and i < len(blk.header) else 0]
        vals += [len(bm.plain_text(r[i])) for r in blk.rows if i < len(r)]
        vals.sort()
        # 75th percentile of cell length as weight, damped with a square root
        p75 = vals[int(0.75 * (len(vals) - 1))] if vals else 1
        lengths.append(max(4.0, p75 ** 0.62))
    total = sum(lengths)
    pct = [w * 100.0 / total for w in lengths]
    lo, hi = 8.0, 62.0
    pct = [min(hi, max(lo, p)) for p in pct]
    total = sum(pct)
    return [p * 100.0 / total for p in pct]


def render_callout(blk, bid: str = "") -> str:
    """Callout box. Continuation lines that begin with (1) / (2) … become a list."""
    iattr = f' id="{bid}"' if bid else ""
    inner = ['<div class="callout-inner">']
    items = [i for i in blk.items if isinstance(i, str) and i.strip()]
    buf: list[str] = []

    def flush() -> None:
        if not buf:
            return
        inner.append("<ul class='citems'>")
        for body in buf:
            span_html = spans_html(bm.parse_inline(body))
            inner.append(f"<li class='ci'>{span_html}</li>")
        inner.append("</ul>")
        buf.clear()

    for line in items:
        if re.match(r"^\(\d+\)\s*", line.strip()):
            buf.append(line)
            continue
        flush()
        inner.append(f"<p>{spans_html(bm.parse_inline(line))}</p>")
    flush()
    inner.append("</div>")
    cls = "callout " + (getattr(blk, "role", "") or "callout")
    return f'<div class="{cls}"{iattr}>' + "".join(inner) + "</div>"


def block_html(blk, css: str = "", arch=None, width: float = 0.0, bid: str = "") -> str:
    role = getattr(blk, "role", "")
    iattr = f' id="{bid}"' if bid else ""
    if blk.kind == "heading":
        if role == "chapter-title":
            return f'<h1 class="chapter-title"{iattr}>{spans_html(blk.spans[0])}</h1>'
        if role == "chapter-title-en":
            return f'<p class="chapter-title-en"{iattr}>{spans_html(blk.spans[0])}</p>'
        if role == "topic-title":
            return f'<h1 class="topic-title"{iattr}>{spans_html(blk.spans[0])}</h1>'
        if blk.level == 2:
            head = spans_html(blk.spans[0])
            if role == "section":
                return f'<h2 class="section-head"{iattr} data-sec="{esc(blk.text)}">{head}</h2>'
            if role == "audit-head":
                return f'<h2 class="audit-head"{iattr}>{head}</h2>'
            if role == "record-head":
                return f'<h2 class="record-head"{iattr}>{head}</h2>'
            if role == "chapter-sa-head":
                return f'<h2 class="chapter-sa-head"{iattr}>{head}</h2>'
            return f"<h2{iattr}>{head}</h2>"
        return f"<h3{iattr}>{spans_html(blk.spans[0])}</h3>"
    if blk.kind == "para":
        cls = {"body-en": "en", "body-fa": "fa", "body": "", "lead": "lead",
               "record-note": "record-note"}.get(role, "")
        spans = [sp for paras in blk.spans for sp in paras]
        t = spans_html(spans) if spans else spans_text(blk.text)
        dattr = ' dir="ltr"' if cls == "en" else ""
        return f'<p class="{cls}"{iattr}{dattr}>{t}</p>' if cls else f"<p{iattr}>{t}</p>"
    if blk.kind == "list":
        return render_list(blk, bid)
    if blk.kind == "table":
        out = render_table(blk, css, arch, width, bid=bid)
        return out[0] if out else ""
    if blk.kind == "callout":
        return render_callout(blk, bid)
    if blk.kind == "diagram":
        return f'<pre class="diagram"{iattr}>{esc(blk.text)}</pre>'
    if blk.kind == "rule":
        return f'<hr{iattr}>'
    return ""
