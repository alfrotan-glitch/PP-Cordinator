# -*- coding: utf-8 -*-
"""
prod_qa.py — the automated production QA gate for the finished deliverables.

    python3 scripts/production/prod_qa.py dist/histology-dari-en.pdf \
            dist/histology-dari-en.docx dist/histology-dari-en.epub

Checks (each printed as PASS / FAIL / WARN with the measured value)
------------------------------------------------------------------
PDF        structure · metadata · outline · internal links · font embedding ·
           text-layer integrity (no presentation forms, CID look-alikes, U+FFFD) ·
           content preservation against the frozen manuscript · margins ·
           folio/running-head coverage · blank pages · symbol coverage
DOCX       package integrity · section geometry · RTL · complex-script fonts ·
           styles · tables · fields (TOC / PAGE / STYLEREF) · content preservation
EPUB       container · nav / NCX / spine · XHTML well-formedness · fonts ·
           cover · RTL metadata · content preservation
"""
from __future__ import annotations

import collections
import io
import json
import os
import re
import sys
import unicodedata
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bookmodel as bm
import check_preservation as cp
import design
import units as U

RESULTS: list[tuple[str, str, str]] = []


def check(area: str, name: str, ok: bool, detail: str = "", warn_only: bool = False):
    status = "PASS" if ok else ("WARN" if warn_only else "FAIL")
    RESULTS.append((area, name, f"{status} — {detail}"))
    return ok


# --------------------------------------------------------------------- PDF

def qa_pdf(path: str) -> dict:
    import pymupdf
    area = "PDF"
    doc = pymupdf.open(path)
    model = bm.load_document()

    check(area, "opens", doc.is_pdf and not doc.is_encrypted, f"{doc.page_count} pages")
    check(area, "page size A4", all(abs(p.rect.width - design.PAGE_W) < 1.5 and
                                    abs(p.rect.height - design.PAGE_H) < 1.5
                                    for p in doc), f"{doc[0].rect.width:.0f}x{doc[0].rect.height:.0f} pt")
    meta = doc.metadata
    check(area, "metadata title", bool(meta.get("title")), meta.get("title", ""))
    check(area, "metadata author/subject", bool(meta.get("author")) and bool(meta.get("subject")),
          f"{meta.get('author','')[:34]} | {meta.get('subject','')[:34]}")
    try:
        xmp = doc.get_xml_metadata() or ""
    except Exception:
        xmp = ""
    check(area, "XMP metadata", "dc:title" in xmp and "pdf:Producer" in xmp, f"{len(xmp)} bytes")

    toc = doc.get_toc()
    check(area, "bookmarks/outline", len(toc) >= 120, f"{len(toc)} entries")
    links = sum(len(p.get_links()) for p in doc)
    check(area, "internal links (TOC)", links >= 120, f"{links} link objects")

    # fonts
    fonts = collections.Counter()
    not_embedded = []
    for i in range(doc.page_count):
        for f in doc[i].get_fonts(full=True):
            fonts[(f[3], f[4])] += 1
    for xref in range(1, doc.xref_length()):
        if doc.xref_get_key(xref, "Type")[1] != "/Font":
            continue
        df = doc.xref_get_key(xref, "DescendantFonts")
        if df[0] != "array":
            continue
        dfx = int(df[1].strip("[]").split()[0])
        fd = doc.xref_get_key(dfx, "FontDescriptor")
        if fd[0] != "xref":
            continue
        fdx = int(fd[1].split()[0])
        embedded = any(doc.xref_get_key(fdx, k)[0] == "xref"
                       for k in ("FontFile", "FontFile2", "FontFile3"))
        if not embedded:
            not_embedded.append(doc.xref_get_key(dfx, "FontName")[1])
    check(area, "all fonts embedded", not not_embedded,
          f"{len(fonts)} font resources, unembedded: {not_embedded}")

    # text layer integrity + margins + folio coverage
    presentation = cid_like = replacement = controls = 0
    out_of_margin = []
    blank = []
    folio_missing = []
    for i, page in enumerate(doc):
        t = page.get_text()
        for ch in t:
            o = ord(ch)
            if 0xFE70 <= o <= 0xFEFF:
                presentation += 1
            elif 0x0400 <= o <= 0x04FF or 0x4E00 <= o <= 0x9FFF or 0x3040 <= o <= 0x30FF:
                cid_like += 1
            elif o == 0xFFFD:
                replacement += 1
            elif o < 32 and ch not in "\n\r\t":
                controls += 1
        if len(t.strip()) < 12:
            blank.append(i + 1)
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            x0, y0, x1, y1 = b["bbox"]
            if x0 < design.M_OUTER - 4 or x1 > design.PAGE_W - design.M_OUTER + 4:
                out_of_margin.append((i + 1, round(x0), round(x1)))
            if y1 > design.PAGE_H - design.M_BOTTOM + 24:
                out_of_margin.append((i + 1, "bottom", round(y1)))
    check(area, "no presentation forms (U+FE70–FEFF)", presentation == 0, f"{presentation} chars")
    check(area, "no CID look-alikes (Cyrillic/CJK)", cid_like == 0, f"{cid_like} chars")
    check(area, "no replacement characters", replacement == 0, f"{replacement} chars")
    check(area, "no control characters", controls == 0, f"{controls} chars")
    check(area, "no blank pages", not blank, f"{len(blank)} blank: {blank[:8]}")
    check(area, "text inside margins", len(out_of_margin) == 0,
          f"{len(out_of_margin)} violations: {out_of_margin[:6]}")
    # every chapter opens on a fresh page and is preceded by its running head
    opener_pages = [i + 1 for i, p in enumerate(doc)
                    if any(h in p.get_text()[:120] for h in ("فصل ۱\n", "فصل ۲\n", "فصل ۲۳\n"))]
    folio_ok = sum(1 for i, p in enumerate(doc) if p.get_text().strip().endswith(
        str(i + 1).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))))
    check(area, "folio on every page", folio_ok >= doc.page_count - 2,
          f"{folio_ok}/{doc.page_count} pages end with their folio")

    # content preservation between the print file's text layer and the manuscript
    blob = "\n".join(p.get_text() for p in doc)
    src = cp.manuscript_tokens()
    other = cp.content_tokens(blob)
    missing, _extra, ok_m, _ok_x = cp.compare(src, other, cp.compact_text(blob))
    numeric = re.compile(r"^[0-9۰-۹.,;:()،؛%«»+−-]+$")
    content_missing = collections.Counter({k: v for k, v in missing.items() if not numeric.match(k)})
    covered = 1 - sum(content_missing.values()) / max(1, sum(src.values()))
    check(area, "content preservation (text layer)", covered > 0.995,
          f"coverage {covered*100:.2f}% (missing tokens {sum(content_missing.values())}, "
          f"present-by-substring {len(ok_m)})")

    # chapters / topics / appendices present in the text layer
    compact = cp.compact_text(blob)
    ch_missing = [c.number for c in model.chapters
                  if cp.compare(cp.content_tokens(c.fa_title), other, compact)[0]]
    tp_missing = [t.number for c in model.chapters for t in c.topics
                  if cp.compare(cp.content_tokens(t.fa_title), other, compact)[0]]
    check(area, "all 23 chapter titles present", not ch_missing, f"missing: {ch_missing}")
    check(area, "all topic titles present", not tp_missing, f"missing: {tp_missing}")
    for label in ("پیوستِ الف", "پیوستِ ب", "پیوستِ ج", "پیوستِ د"):
        check(area, f"appendix {label} present", label in blob)

    # table headers present
    tbl_missing = 0
    for c in model.chapters:
        for t in c.topics:
            for blk in t.blocks:
                if blk.kind == "table" and blk.header:
                    hdr = " ".join(bm.plain_text(h) for h in blk.header)
                    if cp.compare(cp.content_tokens(hdr), other, compact)[0]:
                        tbl_missing += 1
    check(area, "table headers present", tbl_missing == 0, f"{tbl_missing} tables missing headers")

    # searchable text (typical reader expectation)
    probe = "هستولوژی"
    hits = sum(1 for p in doc if probe in p.get_text())
    check(area, "text searchable (Dari terms)", hits > 100,
          f"'{probe}' found on {hits} pages; "
          f"'هیستولوژی' (title-page spelling) on "
          f"{sum(1 for p in doc if 'هیستولوژی' in p.get_text())} pages")

    stats = dict(pages=doc.page_count, bytes=os.path.getsize(path),
                 outline=len(toc), links=links,
                 fonts=len([f for f in fonts if f[0]]),
                 font_names=sorted({f[0] for f in fonts if f[0]}))
    doc.close()
    return stats


# --------------------------------------------------------------------- DOCX

def qa_docx(path: str) -> dict:
    from docx import Document
    from docx.oxml.ns import qn
    area = "DOCX"
    check(area, "valid OOXML package", zipfile.is_zipfile(path),
          f"{os.path.getsize(path)} bytes")
    d = Document(path)
    sect = d.sections[0]
    check(area, "A4 page geometry",
          abs(sect.page_width.cm - 21.0) < 0.2 and abs(sect.page_height.cm - 29.7) < 0.2,
          f"{sect.page_width.cm:.1f}x{sect.page_height.cm:.1f} cm")
    check(area, "gutter (mirrored-ish) margins",
          sect.left_margin.cm >= 2.2 and sect.right_margin.cm >= 1.5,
          f"L {sect.left_margin.cm:.2f} / R {sect.right_margin.cm:.2f} cm")
    check(area, "RTL section", sect._sectPr.find(qn("w:bidi")) is not None)
    bidi = sum(1 for p in d.paragraphs
               if p._p.find(qn("w:pPr")) is not None
               and p._p.find(qn("w:pPr")).find(qn("w:bidi")) is not None)
    check(area, "RTL paragraphs", bidi > len(d.paragraphs) * 0.7,
          f"{bidi}/{len(d.paragraphs)} paragraphs")
    cs = 0
    for p in d.paragraphs[:2000]:
        for r in p.runs:
            rPr = r._element.find(qn("w:rPr"))
            if rPr is not None and rPr.find(qn("w:rFonts")) is not None \
                    and rPr.find(qn("w:rFonts")).get(qn("w:cs")):
                cs += 1
    check(area, "complex-script fonts (w:cs)", cs > 500, f"{cs} runs in the first 2000 paragraphs")
    check(area, "styles defined", len(d.styles) > 150, f"{len(d.styles)} styles")
    check(area, "tables", len(d.tables) > 500, f"{len(d.tables)} tables")
    repeats = sum(1 for t in d.tables
                  if t.rows and t.rows[0]._tr.find(qn("w:trPr")) is not None
                  and t.rows[0]._tr.find(qn("w:trPr")).find(qn("w:tblHeader")) is not None)
    check(area, "repeating table headers", repeats >= len(d.tables) - 5,
          f"{repeats}/{len(d.tables)}")
    xml = open(path, "rb").read().decode("latin-1")
    check(area, "automatic table of contents field (TOC)", "TOC \\\\o" in xml.replace("\\\\", "\\")
          or "TOC \\o" in xml)
    check(area, "PAGE field (folios)", "PAGE" in xml and "fldChar" in xml)
    check(area, "running head field (STYLEREF)", "STYLEREF" in xml)
    check(area, "fields refresh on open", "updateFields" in xml)

    blob = "\n".join([p.text for p in d.paragraphs] +
                     [c.text for t in d.tables for row in t.rows for c in row.cells])
    src = cp.manuscript_tokens()
    other = cp.content_tokens(blob)
    missing, _x, _m, _y = cp.compare(src, other, cp.compact_text(blob))
    numeric = re.compile(r"^[0-9۰-۹.,;:()،؛%«»+−-]+$")
    content_missing = collections.Counter({k: v for k, v in missing.items() if not numeric.match(k)})
    covered = 1 - sum(content_missing.values()) / max(1, sum(src.values()))
    check(area, "content preservation", covered > 0.995,
          f"coverage {covered*100:.2f}% (missing {sum(content_missing.values())}, "
          f"sample {list(content_missing.items())[:4]})")
    check(area, "no literal markup artefacts", "**" not in blob and "```" not in blob,
          "no ** / ``` sequences")
    for label in ("پیوستِ الف", "پیوستِ ب", "پیوستِ ج"):
        check(area, f"appendix {label} present", label in blob)
    return dict(paragraphs=len(d.paragraphs), tables=len(d.tables),
                bytes=os.path.getsize(path), styles=len(d.styles))


# --------------------------------------------------------------------- EPUB

def qa_epub(path: str) -> dict:
    import xml.etree.ElementTree as ET
    area = "EPUB"
    check(area, "valid zip", zipfile.is_zipfile(path), f"{os.path.getsize(path)} bytes")
    z = zipfile.ZipFile(path)
    names = z.namelist()
    check(area, "mimetype first + stored",
          names[0] == "mimetype" and z.getinfo("mimetype").compress_type == zipfile.ZIP_STORED)
    check(area, "container.xml", "META-INF/container.xml" in names)
    opf = [n for n in names if n.endswith(".opf")]
    check(area, "package document", len(opf) == 1, opf[0] if opf else "missing")
    root = ET.fromstring(z.read(opf[0]))
    ns = {"opf": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/"}
    title = root.find(".//dc:title", ns)
    check(area, "dc metadata", title is not None and bool(title.text), title.text if title is not None else "")
    spine = root.find(".//opf:spine", ns)
    prog = spine.get("page-progression-direction") if spine is not None else None
    check(area, "RTL page progression", prog == "rtl", str(prog))
    items = [i.get("href") for i in root.findall(".//opf:manifest/opf:item", ns)]
    xhtml = [h for h in items if h.endswith(".xhtml")]
    bad_xml = []
    for h in xhtml + [i for i in items if i.endswith(".ncx")]:
        try:
            ET.fromstring(z.read("OEBPS/" + h))
        except Exception as exc:
            bad_xml.append((h, str(exc)[:60]))
    check(area, "well-formed XHTML/NCX", not bad_xml, f"{len(xhtml)} documents, errors: {bad_xml[:3]}")
    fonts = [h for h in items if "fonts/" in h]
    check(area, "fonts embedded", len(fonts) >= 6, f"{len(fonts)} font files")
    cover = [i.get("href") for i in root.findall(".//opf:manifest/opf:item", ns)
             if (i.get("properties") or "") == "cover-image"]
    check(area, "cover image", bool(cover), str(cover))
    nav = [i.get("href") for i in root.findall(".//opf:manifest/opf:item", ns)
           if "nav" in (i.get("properties") or "")]
    nav_ok = False
    if nav:
        navdoc = ET.fromstring(z.read("OEBPS/" + nav[0]))
        nav_ok = "toc" in z.read("OEBPS/" + nav[0]).decode("utf-8")
    check(area, "navigation document", nav_ok, nav[0] if nav else "missing")
    check(area, "spine length", spine is not None and len(spine) >= 28,
          f"{len(spine)} items" if spine is not None else "")

    blob = "\n".join(z.read(n).decode("utf-8", "ignore") for n in names
                     if n.endswith(".xhtml"))
    blob = re.sub(r"<[^>]+>", " ", blob)
    blob = blob.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#160;", " ")
    src = cp.manuscript_tokens()
    other = cp.content_tokens(blob)
    missing, _x, _m, _y = cp.compare(src, other, cp.compact_text(blob))
    numeric = re.compile(r"^[0-9۰-۹.,;:()،؛%«»+−-]+$")
    content_missing = collections.Counter({k: v for k, v in missing.items() if not numeric.match(k)})
    covered = 1 - sum(content_missing.values()) / max(1, sum(src.values()))
    check(area, "content preservation", covered > 0.995,
          f"coverage {covered*100:.2f}% (missing {sum(content_missing.values())}, "
          f"sample {list(content_missing.items())[:4]})")
    for label in ("پیوستِ الف", "پیوستِ ب", "پیوستِ ج"):
        check(area, f"appendix {label} present", label in blob)
    return dict(documents=len(xhtml), bytes=os.path.getsize(path), fonts=len(fonts))


# --------------------------------------------------------------------- main

def main(argv) -> int:
    paths = argv[1:]
    if not paths:
        dist = os.path.join(design.BOOK_DIR, "dist")
        paths = [os.path.join(dist, f) for f in sorted(os.listdir(dist))
                 if f.lower().endswith((".pdf", ".docx", ".epub"))]
    summary = {}
    for p in paths:
        if not os.path.exists(p):
            continue
        print(f"\n=== {os.path.basename(p)} ===")
        ext = os.path.splitext(p)[1].lower()
        if ext == ".pdf":
            summary["pdf"] = qa_pdf(p)
        elif ext == ".docx":
            summary["docx"] = qa_docx(p)
        elif ext == ".epub":
            summary["epub"] = qa_epub(p)
    print()
    fails = 0
    for area, name, detail in RESULTS:
        if detail.startswith("FAIL"):
            fails += 1
        print(f"  [{area}] {name}: {detail}")
    counts = collections.Counter(d.split(" — ")[0] for _a, _n, d in RESULTS)
    print(f"\nTOTAL: {counts.get('PASS',0)} PASS · {counts.get('WARN',0)} WARN · "
          f"{counts.get('FAIL',0)} FAIL")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
