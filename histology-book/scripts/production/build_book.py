# -*- coding: utf-8 -*-
"""
build_book.py — one command that produces every deliverable.

    python3 scripts/production/build_book.py                 # full book
    python3 scripts/production/build_book.py --subset        # one chapter (fast smoke test)
    python3 scripts/production/build_book.py --skip-pdf      # re-render DOCX/EPUB only

Outputs (in histology-book/dist/):
    histology-dari-en.pdf    print + screen edition (embedded fonts, bookmarks, links)
    histology-dari-en.docx   editable Word edition (automatic TOC, running heads, folios)
    histology-dari-en.epub   reflowable digital edition (RTL spine, nav, cover)
    production-report.json   the machine-readable build report
    production-report.md     the human-readable build report

The manuscript is never modified here; every renderer works from the frozen Markdown.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import design   # noqa: E402
import fonts    # noqa: E402

DIST = os.path.join(design.BOOK_DIR, "dist")
PDF_NAME = "histology-dari-en.pdf"
DOCX_NAME = "histology-dari-en.docx"
EPUB_NAME = "histology-dari-en.epub"


def environment() -> dict:
    import pymupdf
    import docx
    import fontTools
    import uharfbuzz

    return dict(
        python=platform.python_version(),
        pymupdf=pymupdf.__version__,
        python_docx=getattr(docx, "__version__", "?"),
        fonttools=fontTools.version,
        harfbuzz=getattr(uharfbuzz, "version_string", lambda: "?")() if hasattr(uharfbuzz, "version_string") else "?",
        platform=platform.platform(),
        date=time.strftime("%Y-%m-%d %H:%M"),
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subset", action="store_true", help="build a one-chapter sample")
    ap.add_argument("--skip-pdf", action="store_true")
    ap.add_argument("--skip-docx", action="store_true")
    ap.add_argument("--skip-epub", action="store_true")
    ap.add_argument("--no-qa", action="store_true")
    ap.add_argument("--outdir", default=DIST)
    args = ap.parse_args(argv)

    os.makedirs(args.outdir, exist_ok=True)
    fonts.configure(verbose=True)

    report: dict = dict(environment=environment(),
                        manuscript=os.path.join(design.BOOK_DIR, "README.md"),
                        outputs={})
    t_start = time.time()
    pdf_path = os.path.join(args.outdir, PDF_NAME)
    docx_path = os.path.join(args.outdir, DOCX_NAME)
    epub_path = os.path.join(args.outdir, EPUB_NAME)

    if args.subset:
        import pdf as pdfmod
        work = os.path.join(args.outdir, "_subset.pdf")
        rep = pdfmod.build(work, verbose=True, subset=1)
        rep.pop("page_map", None)
        report["outputs"]["pdf_subset"] = rep
        print("\nsubset build done:", rep["pages"], "pages")
        return 0

    if not args.skip_pdf:
        import pdf as pdfmod
        print("\n== PDF ==")
        rep = pdfmod.build(pdf_path, verbose=True)
        rep.pop("page_map", None)
        report["outputs"]["pdf"] = rep

    if not args.skip_docx:
        import word
        print("\n== DOCX ==")
        report["outputs"]["docx"] = word.build(docx_path, verbose=True)

    if not args.skip_epub:
        import epub
        print("\n== EPUB ==")
        report["outputs"]["epub"] = epub.build(epub_path, pdf_path, verbose=True)

    if not args.no_qa:
        import prod_qa
        print("\n== QA ==")
        prod_qa.RESULTS.clear()
        paths = [p for p in (pdf_path, docx_path, epub_path) if os.path.exists(p)]
        rc = prod_qa.main(["prod_qa"] + paths)
        report["qa"] = dict(results=prod_qa.RESULTS, returncode=rc)

    report["seconds"] = round(time.time() - t_start, 1)
    with open(os.path.join(args.outdir, "production-report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    write_markdown_report(report, os.path.join(args.outdir, "production-report.md"))
    print(f"\ntotal build time: {report['seconds']} s")
    return 0


def write_markdown_report(report: dict, path: str) -> None:
    lines = ["# گزارش تولید — Production report", ""]
    env = report.get("environment", {})
    lines += [f"- تاریخ: {env.get('date','')}", f"- پایتون: {env.get('python','')}",
              f"- PyMuPDF: {env.get('pymupdf','')}", f"- fontTools: {env.get('fonttools','')}",
              ""]
    for key, val in report.get("outputs", {}).items():
        lines.append(f"## {key}")
        lines.append("")
        for k2, v2 in val.items():
            if isinstance(v2, (dict, list)):
                lines.append(f"- {k2}: `{json.dumps(v2, ensure_ascii=False)}`")
            else:
                lines.append(f"- {k2}: {v2}")
        lines.append("")
    qa = report.get("qa")
    if qa:
        lines.append("## QA")
        lines.append("")
        for area, name, detail in qa.get("results", []):
            lines.append(f"- **[{area}] {name}** — {detail}")
        lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
