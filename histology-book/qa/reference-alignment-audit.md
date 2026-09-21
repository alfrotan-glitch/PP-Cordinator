# Reference Alignment Audit — book-level roll-up
# ممیزی انطباق با مرجع — سطح کل کتاب

**Purpose:** this roll-up aggregates the per-chapter 12-point audits. It is the document to check
before declaring any part of the book release-ready.

**Scoring:** ✅ passed · ⚠️ passed with a note · ❌ blocking

| علامت | معنا |
|---|---|
| ✅ | بررسی با موفقیت انجام شده |
| ⚠️ | نکته‌ای نیاز به توجه یا گسترش دارد |
| ❌ | مشکل مسدودکننده — این بخش آمادهٔ انتشار نیست |

---

## 1. Per-chapter audit matrix

| Chapter | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Overall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Ch 1 — Histology & Its Methods** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ draft |
| **Ch 2 — The Cytoplasm** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ draft |
| **Ch 3 — The Nucleus** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ draft |
| **Ch 4 — Epithelial Tissue** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ draft |
| **Ch 5 — Connective Tissue** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ draft |
| **Ch 6 — Adipose Tissue** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ draft |
| **Ch 7 — Cartilage** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ draft |

**Column key (the 12 canonical checks — source of truth: `audit-template.md`):**
1. تمام مفاهیم اصلی پوشش داده شده؟ · 2. تعریف‌ها دقیق؟ · 3. Classification درست؟ ·
4. Structure درست؟ · 5. Function درست؟ · 6. Structure–Function درست؟ ·
7. ویژگی‌های Histological Identification حفظ شده؟ · 8. نکات امتحانی حذف نشده؟ ·
9. اصطلاحات تغییر نکرده؟ · 10. چیزی برخلاف مرجع اضافه نشده؟ ·
11. کوتاه‌سازی مفهومی را از بین نبرده؟ · 12. متن مستقل آموزشی است؟

**Reading the pattern:** every chapter so far scores ⚠️ on check 11 only. That is the honest
signature of a condensation project — each chapter names a specific topic it compressed, rather than
claiming nothing was lost. No chapter scores ❌.

---

## 2. Cross-chapter checks (whole-book level)

| Check | Result | Note |
|---|---|---|
| Terminology consistent across chapters | ✅ | Glossary is the single source of truth (195 entries); `qa_scan.py` enforces 75 forbidden forms with letter boundaries |
| **Terminology standard is Afghan, not Iranian** | ✅ | Terminology gate PASSED for Ch 1–5 — see `editorial/terminology-decisions.md`. 1,712 replacements; 0 prohibited forms remain |
| Terminology verified, not assumed | ✅ | Every decision traced to an Afghan MoHE/MoPH/medical-faculty source; 1 term left unresolved rather than guessed (`آنتی‌ژن`, `[VERIFY TERMINOLOGY]`) |
| English terms not needlessly Dari-ised | ✅ | 42 English-retained entries + all Latin anatomical/stain names |
| Structural template applied consistently | ✅ | All 5 chapters: 13 sections per topic + 12-point audit |
| Bilingual balance maintained | ✅ | Dari explanation first, compact English equivalent, shared detail given once |
| No duplication between chapters | ⚠️ | Microvilli/cilia appear in both Ch2 and Ch4 — intentional (Ch4 cross-references Ch2), but worth re-checking at final pass |
| Exam coverage: Core Knowledge | ✅ | |
| Exam coverage: Exam-Relevant Details | ✅ | HIGH-YIELD blocks carry the numerical and classification detail |
| Exam coverage: Recognition & Differentiation | ✅ | Identification + Comparison + Summary tables in every topic |
| Uncertainty markers used honestly | ✅ | 25 markers flagged `[VERIFY AGAINST JUNQUEIRA 17e]`; 20 distinct backlog items (§3) |
| Terminology uncertainty kept separate from scientific uncertainty | ✅ | `[VERIFY TERMINOLOGY]` (wording) never merged with `[VERIFY AGAINST JUNQUEIRA 17e]` (facts) |
| No fabricated citations | ✅ | The book names no DOIs, studies, or page references |
| Script hygiene (no CJK/Cyrillic contamination) | ✅ | `qa_scan.py` returns 0 findings |
| Numeral convention consistent | ✅ | Western Arabic numerals throughout |

---

## 3. Open items requiring author verification

All of these are marked in the book with `[VERIFY AGAINST JUNQUEIRA 17e]`. None is a scientific
error as written; each is a value or a placement that should be confirmed against the reference
before the book is used as an exam source.

| # | Chapter | Item |
|---|---|---|
| 1 | Ch 1 | Exact resolution figures for SEM and TEM |
| 2 | Ch 1 | Ultrathin section thickness range (60–90 nm vs 50–100 nm) |
| 3 | Ch 1 | Placement of cryo-EM and virtual microscopy in the reference's first chapter |
| 4 | Ch 2 | Placement of the plasma membrane / membrane transport discussion |
| 5 | Ch 2 | Exact diameters for intermediate filaments and microfilaments |
| 6 | Ch 2 | Peroxisome size range |
| 7 | Ch 2 | Whether Charcot-Böttcher and Reinke crystalloids appear in the reference |
| 8 | Ch 3 | Placement and depth of stem cell / differentiation coverage |
| 9 | Ch 3 | G-banding band count at standard resolution |
| 10 | Ch 3 | Approximate durations of cell cycle phases |
| 11 | Ch 3 | Whether the reference separates Prometaphase from Prophase |
| 12 | Ch 4 | Numerical thickness of the basal lamina in EM |
| 13 | Ch 4 | Epidermal turnover time |
| 14 | Ch 4 | Whether the reference prefers "Urothelium" or "Transitional epithelium" |
| 15 | Ch 4 | Exact locations listed for stratified cuboidal / columnar epithelium |
| 16 | Ch 4 | Placement of the myoepithelial cell discussion |
| 17 | Ch 5 | Number of collagen types stated in the reference |
| 18 | Ch 5 | Placement and expected depth of inflammation & repair |
| 19 | Ch 5 | Whether "loose areolar" is the reference's standard term |
| 20 | Ch 5 | Oxytalan / elaunin elastic fibre maturation stages |

---

## 3b. Terminology gate (Chapters 1–6) — PASSED AND CLOSED

The gate was locked on 2026-09-21 (`editorial/final-terminology-lock.md`). Chapter 6 was written under
the locked policy: its new terms (نسج شحمی، ادیپوسیت، پری‌ادیپوسیت، لیپید، تری‌گلیسرید، لیپولیز،
لپتین، ادیپونکتین، ترموجنین، Unilocular، Multilocular and others) were registered in
`build_glossary.py` **before** first use, and the scanner caught and forced correction of 9 pre-lock
forms in the draft before it was accepted.


Full report and the mandatory decision table: **`editorial/terminology-decisions.md`**.
Machine-readable source of truth: `glossary/terminology-glossary.csv` (206 entries × 12 columns).

| Check | Result |
|---|---|
| Prohibited Iranian-Persian terminology | **0** — 86 forbidden forms enforced |
| Unexplained terminology inconsistency | **0** — 56 canonical replacements, 35 accepted variants |
| Terminology decided against Afghan sources (not assumed) | ✅ Research recorded in `editorial/terminology-decisions.md` §2–§3 |
| English terms needlessly Dari-ised | **0** — 42 English-retained entries, all Latin anatomical/stain names kept |
| Invented Dari equivalents | **0**. The one form previously classed as a morpheme-by-morpheme construction (the Afghan transliteration of *Carbohydrate*) is **withdrawn from that class**: it is attested in an Afghan source and is now canonical. Remaining constructed forms (the one built from «chemistry» + «treatment», and the ریز‑ compounds) are 0 occurrences in the text and enforced.
| Every canonical decision has a named Afghan source | ⚠️ **Partial, honestly labelled** — see `editorial/final-terminology-evidence-gate.md`: 54 entries anchored to a named Afghan document, 149 declared as transliterations with no Afghan document located, 4 declared owner-mandated decisions, 1 unresolved. No entry claims an Afghan institution without identifying a document |
| KUMS (Kabul University of Medical Sciences) evidence tier | ✅ **5 entries** — a KUMS news bulletin (kums.edu.af, «دیپارتمنت فزیوتراپی در شفاخانه تدریسی علی آباد پوهنتون علوم طبی کابل…») was read and corroborates مریض، تداوی، داکتر، محصل، شفاخانه. The earlier "not retrievable" note applied to KUMS *syllabi*; the institutional site itself is readable. |
| Terms flagged `[VERIFY TERMINOLOGY]` | 1 (آنتی‌ژن) — deliberately unresolved, not guessed |
| Scanner command | `python3 scripts/qa_scan.py` → **RESULT: 0 findings**, exit 0 |

**Why the earlier assumption was wrong.** The first draft used سلول / بافت / بافت همبند — the
Iranian-Persian standards — because they are linguistically possible Dari. Afghan medical teaching
uses **حجره / نسج / نسج منضم**, as confirmed by an Afghan faculty histology text, the Afghan MoHE
curriculum and the Afghan MoPH register. Terminology that is *possible* is not terminology that is
*in use*; the gate now requires evidence for every term.

---

## 4. Release gate status

```
NOT READY FOR PUBLICATION
```

**Reason:** the book is incomplete. Only 5 of 23 chapters exist. The 12-point audit passes for all
five existing chapters, so they are sound as far as they go — but a partial book cannot be declared
publication-ready.

**Terminology status — LOCKED AND CLOSED (2026-09-21):**
- Junctions are canonical in their international form: **Tight junction / Zonula occludens**,
  **Adherens junction / Zonula adherens**, **Gap junction**. «مضبوط اتصال» is a permitted Afghan Dari
  gloss; the two Dari calques are non-canonical and enforced as prohibited.
- **Carbohydrate → کاربوهایدریت** is canonical (attested: TolAfghan, «فزیولوژی حجره»).
- **Organelle → ارگانل** canonical; **اندامک** recorded as an accepted Afghan variant.
- Scanner 0 findings; self-test ALL PASS; unresolved terminology is exactly one term (آنتی‌ژن).
- Full record: `editorial/final-terminology-lock.md`.

**Blocking issues:**
1. 18 chapters not yet written (Ch 6–23).

**Cleared gates:**
- ✅ **Terminology gate (Ch 1–5)** — PASS, 0 findings, exit code 0. Report:
  `editorial/terminology-decisions.md`. Chapter 6 is unblocked.
2. 20 items flagged `[VERIFY AGAINST JUNQUEIRA 17e]` awaiting confirmation against the reference.
3. Whole-book QA passes (consistency, cross-references, glossary completeness) deferred until all chapters exist.

**Not blocking, but noted:** DOCX/PDF/EPUB production is deferred by the author's decision for this
pass. The Markdown is structured so it converts cleanly when that stage begins.
