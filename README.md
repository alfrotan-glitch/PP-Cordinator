# کتاب قانون زبان — Provincial Coordinator Handbook (second edition)

Editorial + production repository for **«کتاب قانون زبان — راهنمای جامع و عملی
Provincial Coordinator»** (Shuhada Organization — Daikundi, 1405 / 2026), produced with
the `medical-dari-publishing` skill: a single Markdown master manuscript, edited in
distinct phase-controlled passes, and built into DOCX + print PDF + digital PDF + EPUB3.

---

## 1. Deliverables (ready to hand over)

| File | What it is |
|---|---|
| `output/…DOCX_نسخه_نهایی.docx` | Editable Word edition. Real Word styles (Chapter/Section/Body/Note/Key Point…), RTL paragraphs and runs, mirrored margins, cover page, and an **automatic table of contents** (updates itself on open — no "click Update Field" step). |
| `output/…چاپی_17x24.pdf` | Print-ready PDF, 17×24 cm trim, mirrored (gutter) margins, embedded Vazir + Samim. |
| `output/…دیجیتال_A4.pdf` | Digital PDF, A4, embedded fonts, generated TOC with real page numbers. |
| `output/….epub` | EPUB 3 (fa-AF, RTL): one document per chapter, **two-level navigation** (chapter → section, 90 section anchors) in nav + NCX, a visible table-of-contents page, landmarks, SVG cover, three embedded fonts (Vazir text, Samim bold, BookSymbols fallback) with their licence notices inside the package, accessibility metadata, and a colophon page. Validated with EPUBCheck 5.3.0: **0 errors, 0 warnings**. |
| `project/glossary/terminology-glossary.csv` | Terminology glossary (74 entries) — the single source of truth for terms. |
| `project/logs/editorial-change-log.md` | Every substantive change, classified, with the **original wording preserved** for scientific/clinical corrections. |
| `project/logs/scientific-correction-log.md` | The scientific/clinical corrections as their own review view. |
| `project/logs/qa-report.md` | QA results (39 checks) across content, medical, language, terminology, typography, layout, DOCX, PDF, EPUB, references. |
| `project/logs/publication-readiness.md` | Release gate: what passed, and the short list of items needing the author's confirmation. |

The original manuscript (`کتاب_Provincial_Coordinator_نسخه_ویرایش‌شده.docx`) is **untouched**
and kept in the repository root as the version-1 reference.

## 2. What the second edition changed (summary)

* **Structure** — new preface, "about this book", how-to-use guide, 10-chapter roadmap,
  acronym list, learning objectives at the head of every chapter, five annexes (glossary,
  work templates, first-90-days plan, exam/interview guide, sources), edition page.
* **Scientific/clinical accuracy** — BPHS catchment standards corrected (health post
  1,000–1,500; BHC 15,000–30,000; CHC 30,000–60,000; district hospital 100,000–300,000;
  provincial hospital 200,000–500,000), an unverifiable MoPH staff figure removed, HMIS
  reporting deadlines stated unambiguously (aggregated report before the 7th of each month;
  quarterly report before the end of the first month of the new quarter), PSEA restated
  against the IASC Six Core Principles, SO founder/history and province list aligned with
  the organisation's published record, and a new section **§3.8 "Afghanistan's health
  system today (1405)"** describing how BPHS/EPHS is financed and delivered now.
* **Language** — Afghan Dari terminology enforced throughout (مریض، شفاخانه، داکتر، قریه،
  طفل، فیصد، ولایت، کارمندان), Iranian-Persian contamination audited, ZWNJ/نیم‌فاصله,
  punctuation, percent signs and Persian-Indic numerals made consistent, register
  professionalised (زنگ زدن → تماس گرفتن).
* **Production** — real Word styles, RTL everywhere, print-safe typographic marks instead of
  emoji, embedded fonts, cover, and a single-source build for all four formats.

## 3. Repository layout

```
├── medical-dari-publishing.skill          # the skill used (untouched)
├── کتاب_..._نسخه_ویرایش‌شده.docx            # original manuscript (v1, untouched)
├── output/                                # DOCX · print PDF · digital PDF · EPUB
└── project/
    ├── manuscript/
    │   ├── parts/                         # 00 extracted · 10 body · 20 glossary ·
    │   │                                  # 30 annexes · 40 back matter
    │   └── master.md                      # SINGLE SOURCE for all outputs
    ├── scripts/                           # the pipeline (see §4)
    ├── assets/                            # fonts (Vazir, Samim — OFL) + cover
    ├── glossary/terminology-glossary.csv
    └── logs/                              # change log · QA · readiness · audit CSVs
```

## 4. Rebuilding everything

```bash
cd /home/user/PP-Cordinator
bash project/scripts/build_all.sh
```

The pipeline, in phase order:

| Script | Phase | What it does |
|---|---|---|
| `extract_docx.py` | 0–1 | Faithful extraction of the original DOCX (structure, tables, callouts) — never edits the source. |
| `normalize.py` | 3–5 | Structure typing + language rule table + Afghan terminology table; writes the automated change log and a token-diff QA file. |
| `patch_curated.py` | 2–4 | The curated scientific/clinical corrections and structural additions (exact-match, asserted). |
| `assemble.py` | 5 | Concatenates the parts into `master.md`. |
| `make_cover.py` | 5 | Typographic cover (same embedded font). |
| `make_webfonts.py` | 5 | Web fonts for the EPUB: Vazir/Samim → woff2 and a small DejaVu symbol subset (renamed `BookSymbols`), plus the embedded licence notices. |
| `preview_epub.py` | 7 | Browser preview of the packaged EPUB (`project/preview/index.html`) for review without an e-reader. |
| `build_docx.py` / `build_pdf.py` / `build_epub.py` | 6 | The three production formats. |
| `qa.py` | 7 | Whole-book QA → `logs/qa-report.md`. |
| `make_logs.py` | 8 | Change log, scientific correction log, publication readiness report. |

Verified environment: Python 3.11 with `python-docx`, `reportlab`, `arabic-reshaper`,
`python-bidi`, `ebooklib`, `pillow`, `fonttools`, `brotli`, `pypdf` and `epubcheck`+`jdk4py`
(all installed from PyPI). No system TeX/pandoc is required — the pipeline is self-contained.

To look at the EPUB in a browser without an e-reader:

```bash
python3 project/scripts/preview_epub.py
python3 -m http.server 8000 --bind 0.0.0.0 --directory project/preview
```

## 5. Publication status

`project/logs/publication-readiness.md` → **READY FOR PUBLICATION WITH AUTHOR
CONFIRMATIONS**: 45 QA checks pass, 0 fail, 3 non-blocking warnings (ZWNJ on proper nouns
like میزان/میانگین; emoji→typographic mapping; non-preferred forms intentionally listed in
the glossary). The EPUB edition passes EPUBCheck 5.3.0 with no errors and no warnings —
`qa.py` runs EPUBCheck itself (Java ships in the `jdk4py` pip package), so the check is part
of every build. The items awaiting the author's
confirmation — SO founder attribution, SO beneficiary figures, Daikundi project amounts and
district list, DHIS2 currency, MoPH directorate names, ISBN/print vendor spec — are listed
there rather than hidden.
