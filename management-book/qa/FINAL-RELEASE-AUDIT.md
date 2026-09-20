# Final release audit — report

**Book:** «مدیریت؛ مبانی و مهارت‌های اساسی مدیریت» — Management: The Essentials, Afghan Dari Professional Edition
**Scope:** final release audit only. No rewriting, no expansion, no redesign. Content was touched once, to correct a single verified spelling defect (see §6, D‑5).
**Machine‑readable evidence:** `qa/final-release-integrity.json` (this audit), `qa/qa-report.md` (67/67), `qa/mcq-verification.json`, `qa/language-audit.json`, `qa/final-verification.json`, `qa/epubcheck` output (0/0/0/0), screenshots and JSON in `/tmp/audit_out/`.
**Final status:** **READY** — see §9 for what that word does and does not cover.

---

## 1. What was actually inspected, and with what

There is no Word, no LibreOffice, no Java, no browser and no EPUB reader shipped in this sandbox. They were obtained for this audit:

| Tool | How it was obtained | Used for |
|---|---|---|
| Chromium 153.0.8010.0 (headless, CDP) | npm `@sparticuz/chromium` (Chromium + lib set unpacked to `/tmp/chrom`) | rendering HTML, EPUB XHTML and DOCX |
| docx-preview 0.4.0 + JSZip 3.10.2 | npm | rendering the DOCX in Chromium (real OOXML → HTML), served from a local server |
| EPUBCheck 5.3.0 + Temurin JDK 25 | pip `epubcheck`, `jdk4py` | conformance validation of the EPUB package |
| PyMuPDF 1.28.2 | pip | print/PDF text and margin analysis |
| The book's own fonts (Vazir, Samim, BookSymbols) | registered as system fonts (`/tmp/sysfonts`) so the renderers use the real typefaces, not a fallback | all three renderers |

Everything below was reproduced on the **final** build of 20 Sep 2026 (DOCX 3,215,104 B · EPUB 716,552 B · HTML 1,095,543 B · master 64,825 words).

---

## 2. Area 1 — DOCX

**Method:** rendered with docx-preview in Chromium (page-break mode, headers and footers on, 64 rendered sections, 14 of them landscape), plus direct XML inspection with `lxml`/`python-docx`. Platform font of body paragraphs read through CDP `CSS.getPlatformFontsForNode`: **`('Vazir', 38 glyphs)`** — the book's own font, no fallback.

| Required check | Result | Evidence |
|---|---|---|
| TOC displays, populated | **Yes, entries populate** — 264 `BKToc` paragraphs, 264 bookmarks, 264 `PAGEREF` fields, dot-leader tab stops; the TOC page renders 7,748 characters of entry text | field numbers themselves have empty cached results; `<w:updateFields w:val="true"/>` is set, so Word refreshes them on open (see §8.1) |
| 14 landscape sections readable | **Yes** — 14 sections at 11.69 × 8.27 in, margins 0.59 in; the widest landscape table renders 1009 px wide inside a 1009 px text column, nothing clipped | `docx_landscape.png` (visual), geometry dump |
| Wide tables not clipped / overflowing | **Yes** — all 159 top-level tables occupy ≤ 100.0 % of their own section's text column (portrait 12240 − 2×1304 twips; landscape 16838 − 2×850); renderer reports 0 tables with `scrollWidth > clientWidth` | table-grid audit, corrected section pairing |
| RTL / Dari text, headings | **Yes** — 64/64 rendered sections `direction: rtl`; 5,898 bidi paragraphs, 7,412 RTL runs; headings render in Samim (DariDisplay) at BKPart/BKChapter sizes | render + XML |
| Headers / footers | **Yes** — every section carries the running header «مدیریت؛ مبانی و مهارت‌های اساسی مدیریت» and the footer «صفحه » + `PAGE` field; every section has a different (suppressed) first page | XML + render |
| Page breaks | **Yes** — 35 explicit page breaks; each of the 7 parts starts on a new page; no chapter starts mid-page | XML |
| Proof spacing | **Yes** — body 10.5 pt (`sz` 21) at 336 twips line spacing, justified, 120 twips after; list and callout styles consistent; no run-boundary word collisions | style table + render |
| No production metadata visible | **Yes** — `core.xml`: title, subject, creator/«نشر سرچشمه», category, keywords, `fa-AF`, 2026‑09‑20; `app.xml`: no `Application`, no Microsoft claim, no stale statistics, no builder name. String scan of every package part: no «PP-Cordinator», no python-docx/ebooklib/PIL trace | package scan |

## 3. Area 2 — EPUB

**Method:** package unpacked, all 40 XHTML documents rendered in Chromium at 800 / 480 / 360 px and in dark scheme, plus XML/OPF/nav inspection. EPUBCheck run separately (§4).

| Required check | Result | Evidence |
|---|---|---|
| 7 part-divider titles | **Yes** — 7 real `partpage` documents («بخش یکم» … «بخش هفتم») with their chapter lists: 3, 3, 4, 4, 3, 1, 2 chapter links | render |
| TOC / navigation | **Yes** — `toc.xhtml` 266 links, `nav.xhtml` 270 links (3 levels: part → chapter → section), 0 dead links, colophon/licence entries present | render + link check |
| MCQ options as proper lists | **Yes** — 150 question blocks, each exactly one ordered list of four lettered choices (الف/ب/ج/د); 0 malformed | render |
| RTL / LTR mixed text | **Yes** — `dir="rtl"` + `lang="fa-AF"` on html and body of all 40 documents; Latin fragments (names, «Management: The Essentials») stay LTR; extracted text shows correct bidi ordering | render + text extraction |
| Fonts load | **Yes** — Vazir (regular), Samim (bold/display) and BookSymbols embedded in the package and reported `loaded` in all sampled documents; 0 documents with font errors | render |
| Tables readable | **Yes** — 83 tables; none overflows its column at 800 px; `t-xwide` key tables use 0.68 em with `overflow-wrap`; the six 52-column workshop tables in ch 20 need horizontal scrolling below ≈ 810 px (no clipping, but the reader scrolls) — see §8.5 | render |
| Dark mode / high contrast / mobile | **Yes** — dark scheme swaps to `#14161a` paper / `#e8e6e1` ink and accents; `@media (prefers-contrast: more)` present; at 360 and 480 px `documentElement.scrollWidth == clientWidth` (no page-level horizontal overflow) | render |

## 4. Area 3 — EPUBCheck

EPUBCheck **was run** (5.3.0, EPUB 3.3 rules) on the final package:

```
Validating using EPUB version 3.3 rules.
No errors or warnings detected.
Messages: 0 fatals / 0 errors / 0 warnings / 0 infos
```

`scripts/qa.py` now resolves the jar and the JDK itself (`epubcheck` + `jdk4py`), so the check that previously reported «اجرا نشد» now runs and passes: **QA 67 checks · 67 pass · 0 blocking**.

## 5. Area 4 — final HTML

**Method:** the single self-contained file rendered in Chromium at 1440 / 1024 / 820 / 390 / 320 px, in light and dark scheme, with contrast sampling and a real print pass (Chromium A4 PDF, analysed with PyMuPDF).

| Required check | Result | Evidence |
|---|---|---|
| Two-level nav | **Yes** — 34 sidebar links: 7 parts (level 1) + 27 chapters (level 2); 0 dead anchors | render |
| RTL text / layout | **Yes** — `lang="fa-AF" dir="rtl"`, 18.5 px body at 2.02 line height, justified with `text-justify: inter-word`, DariBook first in the stack and `document.fonts.check('16px DariBook') === true` | render |
| Tables | **Yes** — 83 tables, none wider than its container on desktop/tablet; on phones 26–38 tables scroll horizontally inside their own container; no page-level overflow | render |
| MCQs | **Yes** — 150 blocks, each one 4-item list with lettered options; 0 h4; headings semantic | render |
| Responsive / mobile | **Yes** — 390 px and 320 px: `scrollWidth == clientWidth` (no sideways page scroll); sidebar collapses above the text | render |
| Dark mode | **Yes** — 5,679 text samples, minimum contrast 8.49 : 1; light scheme minimum 7.65 : 1 (both above WCAG AA 4.5) | render |
| Print layout | **Yes** — A4, 201 pages, sidebar and progress bar hidden, `.layout` unwrapped, cover on page 1, headings page-break-before, boxes/tables/rows kept inside a page; text stays within margins | Chromium PDF |

---

## 6. Defects found by this audit and corrected

The audit was allowed to fix concrete release-blocking defects. Five were found; all five are cheap, mechanical and verified after rebuilding:

| # | Where | Defect | Fix |
|---|---|---|---|
| D‑1 | packaged EPUB (all 40 documents) | **No document linked the stylesheet.** ebooklib rebuilds every `<head>` from its own template, so the `<link>` written into the content was dropped — a real reading system would have opened an unstyled book | `scripts/build_epub.py:598-602` registers `style/main.css` on every document item; rebuilt; 40/40 documents now link it |
| D‑2 | `scripts/build_html.py:169` | the mobile media query used `grid-template-columns: 1fr`, so the 21 rem sidebar column survived on phones (page 366 px wide at a 390 px viewport; tables began 30–136 px off-screen) | `minmax(0, 1fr)`; rebuilt; 390/320 px now have no page-level overflow |
| D‑3 | `scripts/build_docx.py:30` | the DOCX declared `Vazirmatn`, a family that is **not** the shipped font (assets ship Vazir) → Word substitutes an arbitrary face | `FONT = 'Vazir'`; rebuilt; `document.xml` and `styles.xml` now reference only Vazir, and the renderer resolves the real font |
| D‑4 | `scripts/build_docx.py:474-478` | `docProps/app.xml` carried `<Application>PP-Cordinator DOCX builder</Application>` — a build-tool trace visible in Word's document properties | removed; rebuilt; the string «PP-Cordinator» is now absent from the whole package |
| D‑5 | `manuscript/parts/10_part1.md:10` | one «مسوول» against 200+ correctly spelled «مسئول» — the required spelling-consistency check failed | corrected; `scripts/assemble.py` re-run; master now has مسوول 0 / مسؤول 0 |

After these fixes the master was re-assembled and **all three editions were rebuilt** (DOCX 3,215,104 B · EPUB 716,552 B · HTML 1,095,543 B), the nine proof pages re-rendered, and every audit in §2–§5 repeated on the new files.

---

## 7. Final automated integrity check

`qa/final-release-integrity.json` — one run, on the final artefacts:

| Required item | Result |
|---|---|
| P0 defects zero | **Pass** — `scripts/qa.py`: 67 checks, 67 pass, 0 notes/fail, **0 blocking** |
| MCQ keys 24 / 24 / 24 / 28 | **Pass** — الف 24.0 %, ب 24.0 %, ج 24.0 %, د 28.0 % (was الف 12.7 / ب 72.0 / ج 14.7 / د 0.7 before the correction pass) |
| No > 5-character answer-length cue | **Pass** — items whose keyed option is longer than the runner-up by more than 5 characters: **0** (max gap 5, median −1) |
| Forbidden Iranian forms zero | **Pass** — پرونده 0, استعلاجی 0, نظرسنجی 0, توسعهٔ شغلی 0, تیلفون 0, فرم 0, گزارش 0, مسؤول 0; preferred Afghan forms present (دوسیه 12, مرخصی مرضی 5, سروی 30, انکشاف شغلی 2, تلیفون 11, فورم 48, راپور 126) |
| مسئول / مسئولیت spelling consistent | **Pass** — the two wrong spellings are absent: «مسوول» 0, «مسؤول» 0. Correct forms present: «مسئول» 201 (the language audit's word count), «مسئولیت» 139, «مسئولیت‌ها» 17 |
| Outputs correspond to the corrected manuscript | **Pass** — 6 sample passages traced from `master.md` into DOCX, EPUB and HTML with 0 misses; DOCX paragraph text identical before/after the rebuild; 264 bookmarks = 264 PAGEREF = 264 TOC entries; EPUB 7 parts / 230 TOC sections / 150 MCQs; HTML 7 parts / 27 chapters / 150 MCQs |
| No unintended files or unrelated changes | **Pass** — `git status --porcelain` shows exactly one entry, `?? management-book/`; nothing committed, nothing pushed; no `.tmp`/`.bak`/stray artefacts (only Python's own `scripts/__pycache__`, a bytecode cache) |

Deliverable fingerprints (SHA‑256, first 16 hex): master `4f7b8796b65bdb6c` · DOCX `c031527148af4533` · EPUB `ff3f5ef625ae9016` · HTML `07cd5f328fa6bf3e`.

---

## 8. Limitations — what this audit did **not** verify

1. **No word processor.** The DOCX pagination itself (where the 35 page breaks fall, how the 14 landscape sections split across sheets) was verified geometrically and in a non‑paginating renderer, **not** in Word/LibreOffice. The 264 TOC page numbers are `PAGEREF` fields whose cached results are empty; Word fills them on open because the file sets `<w:updateFields w:val="true"/>`. That behaviour is standard but was not observed here.
2. **DOCX fonts are not embedded.** The file names the shipped family (Vazir); a machine without Vazir installed substitutes a fallback face. The EPUB *does* embed all three fonts and is self‑contained.
3. **No real EPUB reading system** (Apple Books, Calibre, Thorium, Adobe DE). The EPUB was validated by EPUBCheck 5.3.0 and rendered as XHTML in Chromium; reader-specific behaviour (two‑column landscape, hyphenation engines, older RMSDK engines) was not observed.
4. **No print engine for the DOCX.** The print check was done on the HTML edition (Chromium A4 PDF): 201 pages, cover page first, no blank pages, text inside the margins.
5. **Chapter 20's six workshop key tables have 52 columns.** They are readable at desktop and tablet widths; below ≈ 810 px they require horizontal scrolling. This is a deliberate design of the wide “answer key” grid, not a clipping defect, but it is a real reading cost on phones.
6. **The proofs in `qa/proof/` are rendered by the book's own engine** (`scripts/build_proofs.py`), not by a word processor or a reading system; they illustrate the design, they do not replace items 1–3.
7. Nothing in this report is a claim of perfection. The verdict below says the four audit areas were inspected and passed; it does not say that no defect can exist outside what these tools can see.

---

## 9. Final publication status

**READY.**

All four required areas were actually inspected on the final build, not merely assumed:

* **DOCX** — rendered in Chromium (64 sections, real Vazir font, headers/footers, 14 landscape pages) and checked in XML: populated TOC (264 entries/bookmarks/PAGEREFs), no clipped or overflowing table (159 tables ≤ 100 % of their column), correct RTL/Dari typography, clean publication metadata with no build trace.
* **EPUB** — rendered document by document with its embedded fonts: 7 part dividers, 266/270 navigation links with 0 dead, 150 MCQ blocks as proper lists, 83 readable tables, dark mode and high contrast, no overflow on 360/480 px.
* **EPUBCheck** — installed and run on the final package: **0 fatals / 0 errors / 0 warnings / 0 infos** (EPUB 3.3 rules). The audit found and fixed the reason the book would have shipped unstyled (D‑1) before validating.
* **HTML** — rendered at five widths in light and dark, with contrast measured and a real A4 print pass: two-level navigation, RTL layout, readable tables, MCQs, dark mode and clean print.

Then the final automated integrity check passed all seven required items (zero P0 defects, keys 24/24/24/28, no answer-length cue, no forbidden Iranian form، consistent «مسئول»، outputs matching the corrected manuscript, no unrelated files or changes).

The residual uncertainty is exactly §8: verification used the best renderers this environment can run — Chromium, docx-preview, EPUBCheck, PyMuPDF — not Microsoft Word, a commercial EPUB reading system and a print shop. A reviewer with those tools should confirm the two items that depend on them: how the 264 TOC page numbers resolve when Word refreshes its fields, and how the 14 landscape sections paginate on paper. Everything else in this report was observed directly.
