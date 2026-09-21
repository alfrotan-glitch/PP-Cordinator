# -*- coding: utf-8 -*-
"""
pdf.py — the print/digital PDF production engine.

Pipeline
--------
1. build the book units (title, copyright, content, appendices) from the document model
2. place them page by page with MuPDF's story engine and mirrored A4 margins
3. measure what actually landed on every page (block positions) and repair layout
   defects by re-breaking: orphan headings/leads are moved to the next page, and
   tables/self-assessment blocks are kept whole
4. converge: the table of contents gets the real page numbers, the index is generated
   from the finished text layer, and the layout is re-checked until stable
5. dress the pages: running heads, folio, chapter opener band, internal links,
   bookmarks, metadata/XMP
6. repair the text layer: MuPDF writes Arabic presentation forms and mis-numbered
   CIDs into ToUnicode; every CID is re-mapped from the embedded font itself
7. subset the embedded fonts and write the final file
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import time
import unicodedata

import pymupdf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bookmodel as bm
import design
import render_html as rh
import units as U
from fonts import ZWNJ, ZWNJ_RENDER

BODY_W = design.PAGE_W - design.M_INNER - design.M_OUTER
BODY_H = design.BODY_BOTTOM - design.BODY_TOP

ANCHOR_RE = re.compile(r"^(?:ch-\d+|tp-\d+-\d+|bk-[a-z]+)$")
MAX_ITERATIONS = 8
MAX_CONVERGE = 4
ORPHAN_ZONE = 40.0          # pt from the bottom of the text block

GLOSSARY_ROWS_PER_CHUNK = 26


# ----------------------------------------------------------------- geometry

def page_rect(page_no: int) -> pymupdf.Rect:
    """Text block of a page. Odd pages sit on the left of an RTL spread (gutter right)."""
    if page_no % 2 == 1:
        left, right = design.M_OUTER, design.PAGE_W - design.M_INNER
    else:
        left, right = design.M_INNER, design.PAGE_W - design.M_OUTER
    return pymupdf.Rect(left, design.BODY_TOP, right, design.BODY_BOTTOM)


def band_rect(page_no: int, band: str) -> pymupdf.Rect:
    r = page_rect(page_no)
    if band == "header":
        return pymupdf.Rect(r.x0, design.M_TOP, r.x1, design.BODY_TOP - 8)
    return pymupdf.Rect(r.x0, design.BODY_BOTTOM + 16, r.x1, design.PAGE_H - design.M_BOTTOM + 8)


# ----------------------------------------------------------------- units

def build_units(doc, page_map: dict, index_entries=None, chapters=None,
                glossary_rows: int | None = None) -> list[U.Unit]:
    back_entries = [
        ("پیوستِ الف — پرسش‌های مروریِ فصل‌ها", "bk-sa"),
        ("پیوستِ ب — ممیزیِ انطباق با مرجع", "bk-audit"),
        ("پیوستِ ج — واژه‌نامهٔ اصطلاح‌ها", "bk-glossary"),
        ("پیوستِ د — نمایهٔ اصطلاح‌ها", "bk-index"),
    ]
    units = [U.title_unit(), U.copyright_unit(), U.toc_unit(page_map, back_entries, doc),
             U.preface_unit(doc)]
    seen_ids: set[str] = set()
    for u in units:
        for bid, _html in u.chunks:
            assert bid not in seen_ids, f"duplicate block id {bid} in unit {u.key}"
            seen_ids.add(bid)
    units += [U.chapter_unit(ch) for ch in (chapters if chapters is not None else doc.chapters)]
    units.append(U.appendix_a_unit(doc))
    units.append(U.appendix_b_unit(doc))
    units.append(U.glossary_unit(row_limit=glossary_rows or GLOSSARY_ROWS_PER_CHUNK,
                                 max_rows=glossary_rows))
    units.append(U.index_unit(index_entries or []))
    return units


def is_heading_html(html: str) -> bool:
    return bool(re.match(r"\s*<h[1-6][\s>]", html))


def is_lead_html(html: str) -> bool:
    return 'class="lead"' in html[:120] or "apx-chapter-label" in html[:160]


# ----------------------------------------------------------------- pagination

def run_pages(units, out_path, break_before: set, css: str, arch, dress: bool = True) -> list[dict]:
    """Place every unit page by page, draw it (with furniture), and record what landed where."""
    writer = pymupdf.DocumentWriter(out_path)
    pages: list[dict] = []
    page_no = 0
    for unit in units:
        segments = split_segments(unit, break_before)
        if unit.meta.get("fixed"):
            segments = [(None, unit.head)] if unit.head.strip() else []
        for mark_id, html in segments:
            if not html.strip():
                continue
            story = pymupdf.Story(html=html.replace(ZWNJ, ZWNJ_RENDER),
                                  user_css=css, archive=arch)
            first_page_of_unit = True
            while True:
                page_no += 1
                rect = page_rect(page_no)
                dev = writer.begin_page(pymupdf.Rect(0, 0, design.PAGE_W, design.PAGE_H))
                more, filled = story.place(rect)
                rec = dict(no=page_no, unit=unit.key, meta=unit.meta,
                           filled=filled[3] - rect.y0, rect=rect,
                           first_in_unit=first_page_of_unit, elements=[],
                           mark=mark_id)
                els = rec["elements"]

                def cb(pos):
                    r = pos.rect
                    if r is None:
                        return
                    y0 = rect.y0 + r[1]
                    if not (getattr(pos, "open_close", 1) & 1):
                        return                      # close report of the same element
                    els.append(dict(id=getattr(pos, "id", None),
                                    heading=getattr(pos, "heading", 0),
                                    x0=rect.x0 + r[0], y0=y0,
                                    x1=rect.x0 + r[2], y1=rect.y0 + r[3],
                                    on_page=y0 <= rect.y1 + 6))
                story.element_positions(cb)
                story.draw(dev)
                if dress:
                    draw_furniture(dev, rec, els, pages)
                writer.end_page()
                pages.append(rec)
                if not more or unit.meta.get("fixed"):
                    break
                first_page_of_unit = False
    writer.close()
    return pages


def split_segments(unit, break_before: set) -> list[tuple[str | None, str]]:
    """Split a unit into page-starting segments; each carries the mark that caused it."""
    segments: list[tuple[str | None, str]] = []
    cur: list[str] = [unit.head] if unit.head.strip() else []
    mark: str | None = None
    for bid, html in unit.chunks:
        if bid in break_before and cur and "".join(cur).strip():
            segments.append((mark, "".join(cur)))
            cur, mark = [], bid
        cur.append(html)
    if cur and "".join(cur).strip():
        segments.append((mark, "".join(cur)))
    return segments


def block_positions(pages: list[dict], units) -> dict:
    """Deduplicate raw element reports into {id: (page, y0, y1, heading)}."""
    out: dict[str, tuple] = {}
    for rec in pages:
        for e in rec["elements"]:
            if not e["id"] or not e.get("on_page", True):
                continue
            prev = out.get(e["id"])
            if prev is None or e["y0"] < prev[1]:
                out[e["id"]] = (rec["no"], e["y0"], e["y1"], e["heading"])
    return out


def waste_prune(pages: list[dict], threshold: float = 0.72) -> set[str]:
    """Marks whose segment fills less than `threshold` of the page (a wasted page)."""
    body_h = design.BODY_BOTTOM - design.BODY_TOP
    keep: set[str] = set()
    total: dict[str, float] = {}
    for rec in pages:
        if rec["mark"]:
            total[rec["mark"]] = total.get(rec["mark"], 0.0) + rec["filled"]
    return {m for m, h in total.items() if h < threshold * body_h}


def segment_waste(pages: list[dict]) -> float:
    """Mean fraction of a page left empty at the end of every layout segment."""
    body_h = design.BODY_BOTTOM - design.BODY_TOP
    fills = [p["filled"] / body_h for p in pages if not p["first_in_unit"]]
    if not fills:
        return 0.0
    return sum(1 - min(1.0, f) for f in fills) / len(fills)


def detect_last_orphans(pages: list[dict], unit_block_ids: dict[str, dict], units) -> set[str]:
    """The unacceptable case only: a heading with *nothing* after it on its page."""
    marks: set[str] = set()
    first_chunk: dict[str, str] = {}
    for unit in units:
        if unit.chunks:
            first_chunk[unit.key] = unit.chunks[0][0]
    for rec in pages:
        html_by_id = unit_block_ids.get(rec["unit"], {})
        seq, seen = [], set()
        for e in rec["elements"]:
            bid = e["id"]
            if not bid or not e.get("on_page", True) or bid not in html_by_id or bid in seen:
                continue
            seen.add(bid)
            seq.append((e["y0"], bid))
        seq.sort()
        if not seq:
            continue
        bid = seq[-1][1]
        html = html_by_id[bid]
        if not (is_heading_html(html) or is_lead_html(html)):
            continue
        if first_chunk.get(rec["unit"]) == bid and rec["first_in_unit"]:
            continue
        marks.add(bid)
    return marks


def detect_orphans(pages: list[dict], unit_block_ids: dict[str, dict], units) -> set[str]:
    """Block ids that would be stranded at the foot of their page."""
    marks: set[str] = set()
    first_chunk: dict[str, str] = {}
    for unit in units:
        if unit.chunks:
            first_chunk[unit.key] = unit.chunks[0][0]
    for rec in pages:
        html_by_id = unit_block_ids.get(rec["unit"], {})
        seq: list[tuple[float, str]] = []
        seen = set()
        for e in rec["elements"]:
            bid = e["id"]
            if not bid or not e.get("on_page", True) or bid not in html_by_id or bid in seen:
                continue
            seen.add(bid)
            seq.append((e["y0"], bid))
        seq.sort()
        if not seq:
            continue
        for i, (y0, bid) in enumerate(seq):
            html = html_by_id[bid]
            head_like = is_heading_html(html) or is_lead_html(html)
            if not head_like:
                continue
            if first_chunk.get(rec["unit"]) == bid and rec["first_in_unit"]:
                continue
            if i == len(seq) - 1 or (i + 1 < len(seq)
                                     and seq[i + 1][0] > design.BODY_BOTTOM - ORPHAN_ZONE):
                marks.add(bid)      # heading ends the page, or under two lines follow it
    return marks


# ----------------------------------------------------------------- index

def index_entries_from_text(doc, terms, first_page: int, last_page: int, max_refs: int = 5):
    """Build the index from the finished text layer (page references of each term)."""
    pages_text = []
    for i, page in enumerate(doc):
        if not (first_page <= i + 1 <= last_page):
            pages_text.append("")
            continue
        t = page.get_text()
        t = unicodedata.normalize("NFKC", t)
        t = t.replace("\u200c", "").replace("\u200f", "").replace("\u200e", "")
        pages_text.append(re.sub(r"\s+", " ", t))

    entries: dict[str, list[int]] = {}
    low = [(t, t.lower()) for t in terms]
    for i, txt in enumerate(pages_text):
        if not txt:
            continue
        lowtxt = txt.lower()
        for term, term_low in low:
            if term_low and term_low in lowtxt:
                entries.setdefault(term, []).append(i + 1)

    def fmt(pages: list[int]) -> str:
        pages = pages[:max_refs]
        out, i = [], 0
        while i < len(pages):
            j = i
            while j + 1 < len(pages) and pages[j + 1] == pages[j] + 1:
                j += 1
            if j - i >= 2:
                out.append(f"{U.fa_num(pages[i])}–{U.fa_num(pages[j])}")
            else:
                out.extend(U.fa_num(p) for p in pages[i:j + 1])
            i = j + 1
        return "، ".join(out)

    grouped: dict[str, list[tuple[str, str]]] = {}
    for term in sorted(entries, key=lambda t: t):
        refs = entries[term]
        letter = term[0] if term else "?"
        grouped.setdefault(letter, []).append((term, fmt(refs)))
    order = sorted(grouped.keys(), key=lambda c: (c < "\u0600", c))
    return [(letter, grouped[letter]) for letter in order], entries


# ----------------------------------------------------------------- furniture

HEAD_CSS = ("@font-face{font-family:V;src:url(Vazirmatn-Regular.ttf);}"
            "body{font-family:V;font-size:7.4pt;color:%s;margin:0;direction:rtl;line-height:1.2}"
            "p{margin:0}" % design.GREY)
FOLIO_CSS = ("@font-face{font-family:V;src:url(Vazirmatn-Regular.ttf);}"
             "body{font-family:V;font-size:9pt;font-weight:700;color:%s;margin:0;"
             "text-align:center;direction:rtl}" % design.ACCENT)


def running_head_text(rec: dict, topic_state: dict) -> str:
    meta = rec["meta"]
    key = rec["unit"]
    if key.startswith("ch-"):
        if rec["first_in_unit"]:
            return ""
        ch = U.fa_num(meta.get("chapter", ""))
        topic = topic_state.get(rec["no"])
        if topic and meta.get("chapter"):
            return f"مبحث {topic} · فصل {ch} — {meta.get('chapter_title','')}"
        return f"فصل {ch} — {meta.get('chapter_title','')}"
    if meta.get("running_text"):
        return meta["running_text"]
    if meta.get("running") == "toc":
        return "فهرست مطالب — Contents"
    if meta.get("running") == "front":
        return "پیشگفتار و راهنمای مطالعه — Preface"
    return design.RUNNING_TITLE


TOPIC_ID_RE = re.compile(r"^tp-\d+-\d+$")


def topic_of_page(rec: dict, anchors: dict) -> str:
    """Last topic opener that starts on this page (if any)."""
    best = None
    for e in rec["elements"]:
        bid = e["id"] or ""
        if TOPIC_ID_RE.match(bid):
            best = bid
    return best


BAND_CSS = ("@font-face{font-family:V;src:url(Vazirmatn-Regular.ttf);}"
            "body{font-family:V;margin:0;direction:rtl}"
            "p.running{font-size:7.4pt;color:%s;margin:0;line-height:1.2}"
            "div.band{background:%s;height:3.4pt;width:34%%;margin-right:0;margin-left:auto;"
            "margin-top:12pt}"
            "div.band.gold{background:%s;width:100%%;height:2.6pt;margin-top:14pt}"
            % (design.GREY, design.ACCENT, design.WARM_RULE))


def draw_furniture(dev, rec: dict, els: list, pages: list) -> None:
    """Running head, hairline rule, folio and the opener band, drawn on the page device."""
    meta = rec["meta"]
    if not meta.get("furniture", True):
        return
    x0, x1 = rec["rect"].x0, rec["rect"].x1
    outer_left = rec["no"] % 2 == 1              # odd pages sit left of an RTL spread
    opener = bool(rec["first_in_unit"])
    header_parts = []
    if meta.get("chapter") and opener:
        header_parts.append('<div class="band"></div>')
    elif meta.get("running") in ("appendix-a", "appendix-b", "appendix-c", "appendix-d") \
            and opener:
        header_parts.append('<div class="band gold"></div>')
    else:
        topics = [e["id"] for e in els if TOPIC_ID_RE.match(e["id"] or "")]
        if topics and meta.get("chapter"):
            last = topics[-1].replace("tp-", "").replace("-", ".")
            head = f"مبحث {last} · فصل {U.fa_num(meta['chapter'])} — {meta.get('chapter_title','')}"
        elif meta.get("chapter"):
            head = f"فصل {U.fa_num(meta.get('chapter',''))} — {meta.get('chapter_title','')}"
        else:
            head = {("toc"): "فهرست مطالب — Contents",
                    ("front"): "پیشگفتار و راهنمای مطالعه — Preface"}.get(
                        meta.get("running"), meta.get("running_text", design.RUNNING_TITLE))
        align = "left" if outer_left else "right"
        header_parts.append(f'<p class="running" style="text-align:{align}">{head}</p>'
                            f'<div style="border-top:0.4pt solid {design.RULE_SOFT};'
                            f'margin-top:4pt"></div>')
    if header_parts:
        story = pymupdf.Story(html="".join(header_parts), user_css=BAND_CSS,
                              archive=rh.build_archive())
        story.place(band_rect(rec["no"], "header"))
        story.draw(dev)
    folio = pymupdf.Story(html=f'<p style="font-size:9pt;font-weight:700;color:{design.ACCENT};'
                               f'text-align:center;margin:0">{U.fa_num(rec["no"])}</p>',
                          user_css=BAND_CSS, archive=rh.build_archive())
    folio.place(band_rect(rec["no"], "footer"))
    folio.draw(dev)


def add_links(doc, pages: list[dict], anchors: dict, arch) -> dict:
    """Internal links: table of contents rows -> their target pages."""
    links = 0
    seen: set = set()
    for rec in pages:
        page = doc[rec["no"] - 1]
        if rec["unit"] != "toc":
            continue
        for e in rec["elements"]:
            bid = e["id"] or ""
            if not bid.startswith("toc-") or bid == "toc-head":
                continue
            target_id = bid[4:]
            target = anchors.get(target_id)
            if not target:
                continue
            key = (bid, round(e["y0"]), round(e["y1"]))
            if key in seen:
                continue
            seen.add(key)
            r = pymupdf.Rect(e["x0"], e["y0"], e["x1"], e["y1"])
            page.insert_link({"kind": pymupdf.LINK_GOTO, "from": r,
                              "page": target[0] - 1,
                              "to": pymupdf.Point(rec["rect"].x1, target[1])})
            links += 1
    return dict(links=links)


# ----------------------------------------------------------------- text layer

_SHAPING_CACHE: dict[str, dict] = {}
_SHAPING_TEXTS: list[str] = []


def _design_font_paths() -> list[str]:
    paths = []
    for files in design.FONTS.values():
        paths += files
    return [p for p in paths if os.path.exists(p) and p.endswith(".ttf")]


def shaping_map(font_path: str, texts: list[str]) -> dict:
    """gid -> text, derived by re-shaping the book's own text with the same font."""
    if font_path in _SHAPING_CACHE:
        return _SHAPING_CACHE[font_path]
    import uharfbuzz as hb
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    font = hb.Font(face)
    out: dict[int, str] = {}
    for text in texts:
        if not text or not text.strip():
            continue
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, {"kern": True, "liga": True, "clig": True, "calt": True})
        starts = sorted({i.cluster for i in buf.glyph_infos})
        n = len(text)
        for info in buf.glyph_infos:
            gid = info.codepoint
            if gid == 0:
                continue
            c = info.cluster
            nxt = next((s for s in starts if s > c), n)
            sub = text[c:nxt] if nxt > c else text[c:c + 1]
            sub = unicodedata.normalize("NFKC", sub).replace("\ue000", "\u200c")
            if not sub:
                continue
            prev = out.get(gid)
            if prev is None or len(sub) < len(prev):
                out[gid] = sub
    _SHAPING_CACHE[font_path] = out
    return out


def all_model_texts() -> list[str]:
    doc = bm.load_document()
    texts: list[str] = []
    for blk in doc.front:
        texts += list(bm.iter_texts(blk))
    for ch in doc.chapters:
        texts += [ch.fa_title, ch.en_title]
        for blk in list(ch.blocks) + list(ch.tail):
            texts += list(bm.iter_texts(blk))
        for top in ch.topics:
            texts += [top.fa_title, top.en_title]
            for blk in top.blocks:
                texts += list(bm.iter_texts(blk))
    return [x for x in texts if x]


def _font_name_key(name: str) -> str:
    """Normalise a PDF font name: drop the subset tag, case, spaces and punctuation."""
    name = re.sub(r"^[A-Z]{6}\+", "", (name or ""))
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _layer_text(text: str) -> str:
    """Canonicalise a glyph's Unicode for the text layer.

    Two book-specific spellings are restored so that the text layer reads exactly like the
    frozen manuscript: the ZWNJ stand-in becomes U+200C again, and the precomposed
    ``heh with yeh above`` (U+06C0) — which HarfBuzz selects for the Persian ezafe — is
    written as the manuscript's ``heh + hamza above`` pair (U+0647 U+0654).
    """
    text = unicodedata.normalize("NFKC", text).replace(ZWNJ_RENDER, ZWNJ)
    return text.replace("\u06c0", "\u0647\u0654")


def _utf16be(text: str) -> str:
    """Hex for a ToUnicode target: UTF-16BE, so astral characters need a surrogate pair.

    A five-hex-digit value such as ``1F50D`` is not valid UTF-16BE and makes extractors
    read the wrong character (``1F50`` + a stray nibble), which is why the magnifier
    emoji used to vanish from the text layer.
    """
    out = []
    for ch in text:
        cp = ord(ch)
        if cp <= 0xFFFF:
            out.append(f"{cp:04X}")
        else:
            v = cp - 0x10000
            out.append(f"{0xD800 + (v >> 10):04X}{0xDC00 + (v & 0x3FF):04X}")
    return "".join(out)


def _name_text(gname: str) -> str:
    """Unicode text of an Adobe-style glyph name, or '' when the name carries none.

    Contextual/positional forms are not in the font's cmap, so their Unicode value has to
    come from somewhere else.  Vazirmatn names them after the character they draw:
    ``uni0646.medi`` (a final/medial nun), ``uniFB58.long1`` (a stretched peh),
    ``uni064E0651`` (fatha + shadda on one glyph).  Reading the name is exact; the
    fallback below (re-shaping the book's own text) can only give a cluster window and
    would, for instance, label a damma with the letter it happens to sit on.
    """
    if not gname:
        return ""
    base = gname.split(".")[0]
    if base.startswith("uni") and re.fullmatch(r"[0-9A-Fa-f]{4,}", base[3:] or "") \
            and len(base[3:]) % 4 == 0:
        cps = [int(base[3 + i:7 + i], 16) for i in range(0, len(base) - 3, 4)]
    elif re.fullmatch(r"u[0-9A-Fa-f]{4,6}", base):
        cps = [int(base[1:], 16)]
    else:
        return ""
    try:
        text = "".join(chr(c) for c in cps)
    except ValueError:
        return ""
    text = _layer_text(text)
    return "" if not text or "\ufffd" in text else text


def repair_tounicode(doc, use_shaping: bool = True) -> dict:
    """
    Rebuild every font's ToUnicode CMap from the embedded font itself.

    MuPDF writes Arabic presentation forms (U+FE70–FEFF) and leaves some CIDs
    unmapped — extractors then print raw CID values (Cyrillic look-alikes).  Here each
    CID (Identity encoding ⇒ CID = glyph id) is mapped to the font's own Unicode value,
    normalised to base characters with NFKC.
    """
    from fontTools.ttLib import TTFont

    stats = dict(fonts=0, entries=0, unmapped=0)
    for xref in range(1, doc.xref_length()):
        if doc.xref_get_key(xref, "Type")[1] != "/Font":
            continue
        if doc.xref_get_key(xref, "Subtype")[1] != "/Type0":
            continue
        desc = doc.xref_get_key(xref, "DescendantFonts")
        if desc[0] != "array":
            continue
        df_xref = int(desc[1].strip("[]").split()[0])
        fd = doc.xref_get_key(df_xref, "FontDescriptor")
        if fd[0] != "xref":
            continue
        fd_xref = int(fd[1].split()[0])
        stream = None
        for key in ("FontFile2", "FontFile3", "FontFile"):
            v = doc.xref_get_key(fd_xref, key)
            if v[0] == "xref":
                stream = doc.xref_stream(int(v[1].split()[0]))
                break
        if not stream:
            continue
        try:
            font = TTFont(io.BytesIO(stream), lazy=False)
            cmap = font.getBestCmap()
        except Exception:
            continue
        glyph_names = font.getGlyphOrder()
        order = {name: i for i, name in enumerate(glyph_names)}
        gid2uni: dict[int, str] = {}
        gid_score: dict[int, tuple] = {}
        for cp, gname in cmap.items():
            gid = order.get(gname)
            if gid is None or gid == 0:
                continue
            norm = _layer_text(chr(cp))
            if not norm or "\ufffd" in norm:
                continue
            presentation = 0xFE70 <= cp <= 0xFEFF
            score = (1 if presentation else 0, -len(norm))
            if gid not in gid2uni or score < gid_score[gid]:
                gid2uni[gid] = norm
                gid_score[gid] = score
        # glyphs produced by shaping (contextual forms, ligatures, our ZWNJ stand-in) are not
        # in the cmap: take their Unicode from the glyph name, else from re-shaping the
        # book's own text with the matching design file.  A cmap entry is authoritative and
        # is never replaced — the cluster window of a diacritic mark contains the letter it
        # sits on and must not leak into the text layer.
        if use_shaping:
            base = _font_name_key(doc.xref_get_key(df_xref, "BaseFont")[1] or "")
            for path in _design_font_paths():
                if _font_name_key(os.path.basename(path)) not in base and \
                        _font_name_key(os.path.splitext(os.path.basename(path))[0]) not in base:
                    continue
                smap = shaping_map(path, _SHAPING_TEXTS)
                for gid, text in smap.items():
                    if gid in gid2uni:
                        continue
                    named = _name_text(glyph_names[gid]) if gid < len(glyph_names) else ""
                    gid2uni[gid] = named or text
                break
        for gid in range(len(glyph_names)):
            if gid not in gid2uni and gid:                      # unnamed remnants, if any
                named = _name_text(glyph_names[gid])
                if named:
                    gid2uni[gid] = named
        # write the CMap
        entries = []
        num_glyphs = font["maxp"].numGlyphs if "maxp" in font else max(gid2uni) + 1
        for gid in range(num_glyphs):
            uni = gid2uni.get(gid)
            if not uni:
                stats["unmapped"] += 1
                continue
            hexes = _utf16be(uni)[:512]
            entries.append((gid, hexes))
        if not entries:
            continue
        body = ["/CIDInit /ProcSet findresource begin",
                "12 dict begin",
                "begincmap",
                "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def",
                "/CMapName /Adobe-Identity-UCS def",
                "/CMapType 2 def",
                "1 begincodespacerange",
                "<0000> <FFFF>",
                "endcodespacerange"]
        for i in range(0, len(entries), 100):
            chunk = entries[i:i + 100]
            body.append(f"{len(chunk)} beginbfchar")
            body += [f"<{gid:04X}> <{uni}>" for gid, uni in chunk]
            body.append("endbfchar")
        body += ["endcmap", "CMapName currentdict /CMap defineresource pop", "end", "end"]
        data = ("\n".join(body) + "\n").encode("latin-1")

        tu = doc.xref_get_key(xref, "ToUnicode")
        if tu[0] == "xref":
            tu_xref = int(tu[1].split()[0])
            doc.update_stream(tu_xref, data, compress=1)
        else:
            tu_xref = doc.get_new_xref()
            doc.update_object(tu_xref, "<<>>")
            doc.update_stream(tu_xref, data, compress=1)
            doc.xref_set_key(xref, "ToUnicode", f"{tu_xref} 0 R")
        stats["fonts"] += 1
        stats["entries"] += len(entries)
    return stats


def set_metadata(doc) -> None:
    doc.set_metadata({
        "title": f"{design.TITLE_FA} — {design.TITLE_EN}",
        "author": design.AUTHOR,
        "subject": "دوزبانه (دری + English) — مرورِ امتحان‌محورِ هستولوژی بر پایهٔ "
                   "Junqueira's Basic Histology, 17th ed.",
        "keywords": "هیستولوژی, Histology, دری, Dari, English, Junqueira, هستولوژی بنیادی, "
                    "medical textbook, bilingual",
        "creator": f"PP-Cordinator production pipeline (PyMuPDF {pymupdf.__version__})",
        "producer": f"PyMuPDF {pymupdf.__version__} — MuPDF story engine",
    })
    xmp = f"""<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:pdf="http://ns.adobe.com/pdf/1.3/" xmlns:xmp="http://ns.adobe.com/xap/1.0/">
   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{design.TITLE_FA} — {design.TITLE_EN}</rdf:li></rdf:Alt></dc:title>
   <dc:creator><rdf:Seq><rdf:li>{design.AUTHOR}</rdf:li></rdf:Seq></dc:creator>
   <dc:description><rdf:Alt><rdf:li xml:lang="x-default">Bilingual (Afghan Dari + English) high-yield histology review</rdf:li></rdf:Alt></dc:description>
   <dc:language><rdf:Bag><rdf:li>fa-AF</rdf:li><rdf:li>en</rdf:li></rdf:Bag></dc:language>
   <pdf:Producer>PyMuPDF {pymupdf.__version__}</pdf:Producer>
   <xmp:CreatorTool>PP-Cordinator production pipeline</xmp:CreatorTool>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""
    doc.set_xml_metadata(xmp)


def set_outline(doc, anchors: dict, doc_pages: list) -> int:
    toc = []
    for ch in doc_pages:
        n = ch.number
        a = anchors.get(U.ch_id(n))
        if a:
            toc.append([1, f"فصل {U.fa_num(n)} — {ch.fa_title}", a[0]])
        for t in ch.topics:
            ta = anchors.get(U.tp_id(t.number))
            if ta:
                toc.append([2, f"{t.number} {t.fa_title}", ta[0]])
    for label, key in (("پیوستِ الف — پرسش‌های مروریِ فصل‌ها", "bk-sa"),
                       ("پیوستِ ب — ممیزیِ انطباق با مرجع", "bk-audit"),
                       ("پیوستِ ج — واژه‌نامهٔ اصطلاح‌ها", "bk-glossary"),
                       ("پیوستِ د — نمایهٔ اصطلاح‌ها", "bk-index")):
        a = anchors.get(key)
        if a:
            toc.append([1, label, a[0]])
    doc.set_toc(toc)
    return len(toc)


# ----------------------------------------------------------------- orchestration

def build(out_path: str, tmp_dir: str | None = None, verbose: bool = True,
          subset: int | None = None) -> dict:
    t0 = time.time()
    doc_model = bm.load_document()
    chapters = doc_model.chapters if not subset else doc_model.chapters[:subset]
    css = rh.css_for_measure()
    arch = rh.build_archive()
    tmp_dir = tmp_dir or os.path.dirname(os.path.abspath(out_path))
    work = os.path.join(tmp_dir, "_pdfwork.pdf")

    grow = U.glossary_rows()
    if subset:
        grow = grow[:60]
    terms = [t[0] for t in grow]
    terms += [t[1] for t in grow if t[1] and t[1] != t[0]]

    page_map: dict[str, str] = {}
    break_before: set[str] = set()
    index_entries = None
    history = []
    index_stable = False

    best = None            # (score, marks, page_map, index_entries) of the best layout seen
    pages = []
    for it in range(1, MAX_ITERATIONS + 1):
        units = build_units(doc_model, page_map, index_entries, chapters=chapters,
                            glossary_rows=60 if subset else None)
        pages = run_pages(units, work, break_before, css, arch, dress=False)
        positions = block_positions(pages, units)
        anchors = {k: (v[0], v[1]) for k, v in positions.items() if ANCHOR_RE.match(k)}
        new_map = {k: U.fa_num(v[0]) for k, v in anchors.items()}
        need = detect_last_orphans(pages, {u.key: {b: h for b, h in u.chunks} for u in units}, units)
        need -= waste_prune(pages)
        waste = segment_waste(pages)
        score = (len(need), round(waste, 2), len(pages))
        if best is None or score < best[0]:
            best = (score, set(break_before), dict(page_map), index_entries)
        # the index is generated from the text layer of the body pages
        try:
            d = pymupdf.open(work)
            first = max(1, anchors.get(U.ch_id(1), (1, 0))[0])
            idx, _raw = index_entries_from_text(d, terms, first, d.page_count)
            d.close()
            index_stable = (index_entries == idx)
            index_entries = idx
        except Exception as exc:                      # pragma: no cover
            if verbose:
                print("   index generation failed:", exc)
            index_entries = index_entries or []
        history.append(dict(iteration=it, pages=len(pages), orphans=len(need),
                            waste=round(waste, 3), toc_entries=len(new_map),
                            marks=len(break_before),
                            stable=bool(new_map == page_map and not need and index_stable)))
        if verbose:
            print(f"  iter {it}: pages={len(pages)} marks={len(break_before)} "
                  f"orphans={len(need)} waste={waste:.2f} toc={len(new_map)}")
        page_map = new_map
        break_before = break_before | need      # monotone: a mark is never dropped again
        if not need and index_stable:
            break
    # final content pass with the winning break set, page map and index
    _score, break_before, page_map, index_entries = best
    if verbose:
        print(f"  chosen layout: orphans={_score[0]} waste={_score[1]} breaks={len(break_before)}")

    # converge the page map (table of contents numbers) for the chosen break set
    anchors = {}
    for conv in range(1, MAX_CONVERGE + 1):
        units = build_units(doc_model, page_map, index_entries, chapters=chapters,
                            glossary_rows=60 if subset else None)
        pages = run_pages(units, work, break_before, css, arch, dress=False)
        positions = block_positions(pages, units)
        anchors = {k: (v[0], v[1]) for k, v in positions.items() if ANCHOR_RE.match(k)}
        new_map = {k: U.fa_num(v[0]) for k, v in anchors.items()}
        if verbose:
            print(f"  converge {conv}: pages={len(pages)} map_changed={new_map != page_map}")
        if new_map == page_map:
            break
        page_map = new_map

    # final dressed pass
    units = build_units(doc_model, page_map, index_entries, chapters=chapters,
                        glossary_rows=60 if subset else None)
    pages = run_pages(units, work, break_before, css, arch)
    positions = block_positions(pages, units)
    anchors = {k: (v[0], v[1]) for k, v in positions.items() if ANCHOR_RE.match(k)}
    final_map = {k: U.fa_num(v[0]) for k, v in anchors.items()}
    if final_map != page_map:
        if verbose:
            print("  note: final pass shifted the page map; re-running once with the new map")
        page_map = final_map
        units = build_units(doc_model, page_map, index_entries, chapters=chapters,
                            glossary_rows=60 if subset else None)
        pages = run_pages(units, work, break_before, css, arch)
        positions = block_positions(pages, units)
        anchors = {k: (v[0], v[1]) for k, v in positions.items() if ANCHOR_RE.match(k)}

    doc = pymupdf.open(work)
    furnish = add_links(doc, pages, anchors, arch)
    n_outline = set_outline(doc, anchors, chapters)
    set_metadata(doc)
    global _SHAPING_TEXTS
    _SHAPING_TEXTS = [t.replace(ZWNJ, ZWNJ_RENDER) for t in all_model_texts()]
    textlayer = repair_tounicode(doc)
    # Fonts are embedded in full: the derived ZWNJ glyph mapping must stay valid, and
    # MuPDF's own subsetter renumbers CIDs, which would invalidate the repaired ToUnicode.
    doc.save(out_path, garbage=4, deflate=True, clean=True)
    doc.close()

    # verification pass on the finished file
    check = pymupdf.open(out_path)
    report = dict(
        file=os.path.basename(out_path),
        path=os.path.abspath(out_path),
        bytes=os.path.getsize(out_path),
        pages=check.page_count,
        outline=n_outline,
        links=furnish["links"],
        running_heads=sum(1 for p in pages if p["meta"].get("furniture", True) and not
                          p["first_in_unit"]),
        textlayer=textlayer,
        iterations=history,
        chosen=dict(orphans=best[0][0], waste=best[0][1], pages=len(pages)),
        seconds=round(time.time() - t0, 1),
        page_map=page_map,
        breaks=len(break_before),
        index_terms=sum(len(v) for _l, v in (index_entries or [])),
    )
    check.close()
    if os.path.exists(work):
        os.remove(work)
    return report


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(design.BOOK_DIR, "dist",
                                                             "histology-dari-en.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    rep = build(out)
    print(json.dumps(rep, ensure_ascii=False, indent=2)[:3000])
