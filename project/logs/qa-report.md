# گزارش تضمین کیفیت — QA Report

کتاب: قانون زبان — راهنمای جامع و عملی Provincial Coordinator · نسخه دوم · ۱۴۰۵

این گزارش به‌صورت خودکار از فایل‌های ساخته‌شده تولید شده است (`project/scripts/qa.py`). هر ردیف یا PASS است، یا WARN (نیاز به توجه، مانع نشر نیست)، یا FAIL (مانع نشر).

| کتگوری | بررسی | نتیجه | شواهد |
|---|---|---|---|
| Content | Ten chapters present in order | PASS | 10 chapter headings: فصل اول؛ فصل دوم؛ فصل سوم؛ فصل چهارم؛ فصل پنجم؛ فصل ششم؛ فصل هفتم؛ فصل هشتم؛ فصل نهم؛ فصل دهم |
| Content | Section numbering | PASS | 90 numbered sections found (n.nn pattern) |
| Content | No empty or truncated headings | PASS | 0 empty headings |
| Content | No production placeholders left in the text | PASS | none found |
| Content | Annexes and back matter complete | PASS | پیوست ۱–۵ + «درباره این نسخه» present |
| Medical | Corrected BPHS catchment standards carried through | PASS | old "BHC per 13,000" claim removed; standard present in §3.2, summary and answer key |
| Medical | PSEA principles match the IASC text | PASS | principles 1-6 restated from IASC; principle 4 wording aligned |
| Medical | Unverifiable staff number removed | PASS | MoPH staff count deleted, structure kept |
| Medical | HMIS deadlines unambiguous | PASS | monthly deadline spelled out in prose and table |
| Medical | Cold-chain temperature retained and correct | PASS | vaccine cold chain 2-8 °C stated in §4.6 |
| Medical | No drug dose or treatment instruction in the book | PASS | book is management-oriented; no dosing tables to verify (screened for mg/milligram) |
| Language | Iranian-Persian contamination scan (Afghan Dari audit) | PASS | none found |
| Language | ZWNJ (نیم‌فاصله) after the prefix می | WARN | 20 tokens without ZWNJ (proper nouns like میزان/میانگین are expected) |
| Language | Replacement character / mojibake | PASS | 0 U+FFFD characters |
| Language | Arabic yeh/kaf contamination | PASS | no Arabic U+064A / U+0643 characters (Dari ی/ک used consistently) |
| Terminology | Glossary scanner run against the manuscript | WARN |   /home/user/PP-Cordinator/project/manuscript/master.md:3886  'برنامه عملیاتی'  ->  prefer 'پلان اقدام'  [Afghan clinical/administrative usage (see پیوست ۵)] (exit 2) |
| Typography | Numeral convention consistent (Persian-Indic in Dari text) | PASS | 1457 Persian-Indic digits; ASCII digits only in English text |
| Typography | Percent sign consistent | PASS | 40 × ٪ ; 3 × % remaining, all inside English sample answers (Latin % is correct there) |
| Typography | Quote style consistent | PASS | 101 × «» guillemets, 0 straight quotes |
| Typography | Heading hierarchy sane | PASS | 22 H1 / 90 H2 / 22 H3 / 50 H4 headings |
| Typography | Emoji replaced with print-safe symbols | WARN | emoji mapped to typographic marks (⭐→★, 🔴→●, ✅→✓, ❌→✗) — fonts carry no emoji glyphs |
| Layout | DOCX built | PASS | قانون_زبان_Provincial_Coordinator_DOCX_نسخه_نهایی.docx (240 KB) |
| Layout | PDFs built (print + screen) | PASS | قانون_زبان_Provincial_Coordinator_دیجیتال_A4.pdf (521 KB); قانون_زبان_Provincial_Coordinator_چاپی_17x24.pdf (583 KB) |
| Layout | EPUB built | PASS | قانون_زبان_Provincial_Coordinator.epub (238 KB) |
| DOCX | Real Word styles used (not manual formatting) | PASS | 176 styles defined; chapter/section/body/callout styles present |
| DOCX | RTL paragraph direction and runs | PASS | 2694 bidi paragraphs, 2729 rtl runs |
| DOCX | Table of contents field auto-updates on open | PASS | TOC field present + w:updateFields=true (no manual "Update Field" step) |
| DOCX | Mirrored margins for print binding | PASS | w:mirrorMargins enabled |
| DOCX | Tables render as real Word tables | PASS | 505 tables in document.xml |
| PDF | قانون_زبان_Provincial_Coordinator_دیجیتال_A4.pdf: Dari fonts embedded | PASS | embedded: /AAAAAA+DejaVuSans, /AAAAAA+Samim, /AAAAAA+Vazir / also referenced: /Helvetica |
| PDF | قانون_زبان_Provincial_Coordinator_دیجیتال_A4.pdf: table of contents generated with page numbers | PASS | TOC page text length 684 |
| PDF | قانون_زبان_Provincial_Coordinator_چاپی_17x24.pdf: Dari fonts embedded | PASS | embedded: /AAAAAA+DejaVuSans, /AAAAAA+Samim, /AAAAAA+Vazir / also referenced: /Helvetica |
| PDF | قانون_زبان_Provincial_Coordinator_چاپی_17x24.pdf: table of contents generated with page numbers | PASS | TOC page text length 499 |
| PDF | RTL shaping loses no characters (NFKC multiset check) | PASS | all paragraphs checked: shaped visual text is a permutation of the source text (ZWNJ removed and brackets mirrored, as bidi requires) |
| EPUB | mimetype is the first entry and uncompressed | PASS | mimetype, compress_type=0 |
| EPUB | All XHTML documents are well-formed | PASS | 24 documents parsed; no errors |
| EPUB | Manifest references resolve | PASS | all manifest hrefs present in package |
| EPUB | Navigation document + NCX present | PASS | nav.xhtml and toc.ncx generated |
| EPUB | RTL reading order declared | PASS | OPF spine + XHTML documents carry RTL direction |
| EPUB | Dari font embedded and cover present | PASS | Vazir.woff2 embedded, cover image included |
| EPUB | epubcheck executed | WARN | epubcheck (Java) is not available in this build environment — structural validation above was run instead; run epubcheck before print/distribution |
| References | Original manuscript preserved untouched | PASS | کتاب_Provincial_Coordinator_نسخه_ویرایش‌شده.docx present in the repository root, unmodified |
| References | Sources listed for the corrected claims | PASS | پیوست ۵ lists MoPH BPHS, HMIS manual, WHO EMRO, IASC PSEA, UNICEF HER/NFA |

**خلاصه:** PASS: 39 · WARN: 4

**مانع‌های نشر:** هیچ
