# هیستولوژی بنیادی — دری/English
## Essential Histology: A Bilingual (Afghan Dari + English) High-Yield Review

**Reference Standard:** Junqueira's Basic Histology: Text and Atlas, 17th Edition — Anthony L. Mescher
**Audience:** Medical, dental, and allied-health students; candidates preparing for specialty/histology examinations
**Priority order:** Scientific accuracy > Conceptual clarity > Brevity > Memorization

---

## 1. Purpose of this book

This is an **independent teaching text**, not a translation, paraphrase, or reproduction of the
reference book. It is written to be:

- **Shorter** than the reference — through better organization, denser sentences, and removal of
  repetition, never through removal of a concept the student needs.
- **Complete** at the level of *core knowledge + exam-relevant detail + microscopic recognition*.
- **Fully bilingual** — Afghan Dari explanation first, compact English equivalent second.

The test for every chapter is: *if a student had only this text before an exam written from
Junqueira 17e, could they read → understand → review → recognize → recall → answer?*

## 2. Status of the build

| Item | Status |
|---|---|
| Front matter + study guide | ✅ Done |
| Ch 1 — Histology & Its Methods of Study | ✅ Draft 1 — audit passed |
| Ch 2 — The Cytoplasm | ✅ Draft 1 — audit passed |
| Ch 3 — The Nucleus | ✅ Draft 1 — audit passed |
| Ch 4 — Epithelial Tissue | ✅ Draft 1 — audit passed |
| Ch 5 — Connective Tissue | ✅ Draft 1 — audit passed |
| Ch 6 — Adipose Tissue | ⏳ Next (terminology gate cleared) |
| Ch 7 — Cartilage | ⏳ Pending |
| Ch 8 — Bone | ⏳ Pending |
| Ch 9 — Blood & Hemopoiesis | ⏳ Pending |
| Ch 10 — Muscle Tissue | ⏳ Pending |
| Ch 11 — Nervous System & Neural Tissue | ⏳ Pending |
| Ch 12 — Circulatory System | ⏳ Pending |
| Ch 13 — Immune System & Lymphoid Organs | ⏳ Pending |
| Ch 14 — The Oral Cavity | ⏳ Pending |
| Ch 15 — The Digestive Tract | ⏳ Pending |
| Ch 16 — Organs Associated with the Digestive Tract | ⏳ Pending |
| Ch 17 — Respiratory System | ⏳ Pending |
| Ch 18 — The Skin | ⏳ Pending |
| Ch 19 — Urinary System | ⏳ Pending |
| Ch 20 — Endocrine Glands | ⏳ Pending |
| Ch 21 — Male Reproductive System | ⏳ Pending |
| Ch 22 — Female Reproductive System | ⏳ Pending |
| Ch 23 — The Eye & Ear: Special Sense Organs | ⏳ Pending |
| Terminology glossary | ✅ 206 entries × 12 columns (see `glossary/terminology-glossary.csv`) |
| Terminology gate (Ch 1–5) | ✅ **PASS** — 0 findings; decision table in `editorial/terminology-decisions.md` |
| Terminology decision report | ✅ `editorial/terminology-decisions.md` (mandatory table + evidence) |
| Terminology **correction** report | ✅ `editorial/terminology-correction-report.md` (pass 3 — invented-term audit) |
| QA scanner | ✅ `scripts/qa_scan.py` — six passes, 86 forbidden forms, 0 findings |
| Editorial change log | ✅ `editorial/change-log.md` |
| Book-level audit roll-up | ✅ `qa/reference-alignment-audit.md` |
| Full-book QA + release gate | ⏳ Deferred until all chapters exist |

**Release gate status: `NOT READY FOR PUBLICATION`** — the book is incomplete (5 of 23 chapters).
See `qa/reference-alignment-audit.md` §4 for the blocking list.

**Verification backlog:** 20 items are flagged `[VERIFY AGAINST JUNQUEIRA 17e]` across the five
chapters (numerical values, and placement of some topics in the reference). None is a scientific
error as written; each needs confirmation against the reference text.

> **Note on chapter order:** the sequence of *topics* follows the reference's canonical organization.
> Chapter numbering varies between printings and between editions; treat the topic sequence, not the
> number, as the thing being aligned.

## 3. Standing conventions

### 3.1 Bilingual layout
For every concept:
```
**Dari term — English term**

**دری:**
Explanation in natural, plain Afghan Dari.

**English:**
Compact scientific equivalent.
```
Shared scientific detail (bullets, tables, exam points) is given **once**, in a shared block, so the
book never doubles in length.

### 3.2 Language rules (non-negotiable)
- The Dari is **Afghan Dari**, as used in Afghan medical faculties and hospitals — not Iranian Persian.
- Where no established Afghan equivalent exists, the **international English/Latin term is kept** and
  explained in Dari. No invented Persian coinages.
- Key English terms are **never dropped** — the student must recognize them in exam questions.
- **Canonical Afghan terms used throughout this book** (the single source of truth is
  `glossary/terminology-glossary.csv`; the full decision record is
  `editorial/terminology-decisions.md`):

  | English | Afghan Dari used here |
  |---|---|
  | Cell / Cells | **حجره / حجرات** |
  | Tissue / Tissues | **نسج / انساج** |
  | Connective tissue | **نسج منضم** |
  | Epithelial tissue | **نسج اپیتلیال** (noun: اپیتلیوم) |
  | Histology / Pathology | **هستولوژی / پتالوژی** |
  | Squamous / Stratified | **مسطح / مطبق** |
  | Blood vessels | **اوعیهٔ دموی** |
  | Enzyme / Molecule / Ion | **انزایم / مالیکول / ایون** |
  | Chemical / Metabolism | **کیمیاوی / میتابولیسم** |
  | Disease / Treatment | **مریضی / تداوی** |
  | Skin | **جلد** |

  Also standardised: اسلاید, رنگ‌آمیزی, مایکروسکوپ نوری, موی‌رگ (capillary),
  هسته‌چه (nucleolus), کرویات (blood corpuscle), شبکه آندوپلاسمی, رایبوزوم,
  مایتوکندریا, لایزوزوم, پراکسیزوم, میکروویلی, مژک, اپیتلیوم, لامینای پایه.
- **Western Arabic numerals (1, 2, 3…) are used throughout**, per Afghan technical/medical practice.
- Latin anatomical terminology is preserved as-is.

### 3.3 Uncertainty marker
Anything that cannot be stated with confidence carries:

`[VERIFY AGAINST JUNQUEIRA 17e]`

This is a deliberate editorial device. An honest flag is better than a fluent guess.

### 3.4 Directory layout
```
histology-book/
  README.md                 ← this file (production plan, conventions, status)
  00-front-matter.md        ← how to use the book, study method, exam strategy
  chapters/NN-*.md          ← the chapters
  glossary/terminology-glossary.csv   ← single source of truth for terminology
  editorial/change-log.md   ← editorial + scientific change log
  qa/reference-alignment-audit.md     ← per-chapter 12-point audit
```

## 4. Chapter template (applied to every topic in every chapter)

| # | Section | Purpose |
|---|---|---|
| 1 | Definition \| تعریف | Precise, compact |
| 2 | Classification \| طبقه‌بندی | All important classifications, organized |
| 3 | Structure \| ساختمان | Key structural features |
| 4 | Cells \| حجرات | Important cells, their features and roles |
| 5 | Function \| وظیفه | Main functions |
| 6 | Structure–Function Relationship | Why *this* structure suits *this* function |
| 7 | Histological Appearance \| نمای هستولوژیک | What is seen by light microscopy; EM where important |
| 8 | Identification \| تشخیص | How to recognize it on a slide/image |
| 9 | Comparison \| مقایسه | Against similar structures |
| 10 | Clinical Correlation | Only important, short, real associations |
| 11 | HIGH-YIELD EXAM POINTS | The points questions are built from |
| 12 | SUMMARY TABLE | Where appropriate |
| 13 | SELF-ASSESSMENT | Questions with answers, drawn only from that section |

A **Reference Alignment Audit** (12 checks) closes every chapter.

### 4.1 How chapters are checked

`scripts/qa_scan.py` runs six passes over every chapter, the front matter and this README, and must
return **0 findings**:

1. **Script contamination** — flags CJK, Cyrillic, Hebrew, Hangul, Kana and any other script that
   must not appear, plus a Latin fragment embedded inside a Persian word. Latin terms in front
   of a Persian plural suffix (`GAGها`, `doubletها`) are legitimate and are never flagged.
2. **Prohibited terminology** — driven by the `forbidden_forms` column of the glossary and tagged
   `(IRANIAN)` or `(NONCANON)`. Matching is **letter-boundary aware**: ZWNJ and harakat are treated
   as separators, so `موی‌رگ‌ها` is caught while `بافته` (woven), `هیستونی` (histonic), `پیوند`
   and `بیوشیمیایی` are protected.
3. **Terminology inconsistency** — a canonical form and one of its registered `accepted_variants`
   both appearing in the same file.
4. **Structural completeness** — all 13 mandated template sections present for every topic.
5. **English-retained registry** — informational: terms deliberately kept in English.
6. **Verification markers** — informational: `[VERIFY TERMINOLOGY]` and
   `[VERIFY AGAINST JUNQUEIRA 17e]` counts.

```
python3 scripts/qa_scan.py          # report
python3 scripts/qa_scan.py --fix    # apply mechanical-only normalizations
```

Terminology substitutions are deliberately **not** auto-fixed: they need human judgment. Bulk
terminology changes are made once, reproducibly, and in this order:

```
python3 scripts/build_glossary.py                # regenerate the glossary (source of truth)
python3 scripts/apply_terminology.py --apply     # pass 1 — canonical core map (RUN ONCE)
python3 scripts/apply_terminology_supplement.py --apply   # pass 2 — clinical register (idempotent)
python3 scripts/qa_scan.py                       # must report 0 findings
```

Every decision must be recorded in `editorial/terminology-decisions.md`. `apply_terminology.py`
is **not** idempotent — it has already been run and must not be re-run.

### 4.2 Canonical terminology policy (binding)

> **Use the established medical terminology actually used in Afghanistan.**
> **If an established Afghan Dari term exists, use it.**
> **If Afghan medical education uses an English-derived/transliterated term, retain that established
> form.**
> **If no reliable Afghan terminology can be established, DO NOT invent a translation. Retain the
> English term or the established international transliteration and mark it `[VERIFY TERMINOLOGY]`
> where appropriate.**

**No constructed terminology.** Never create a medical term by translating English morphemes or by
combining Dari words. *Chemotherapy → کیموتراپی / Chemotherapy* — never a compound built from
"chemistry" + "treatment". Likewise the book does not carry an invented Dari equivalent for
*Carbohydrate* merely because the English word can be translated semantically.

**Source hierarchy** — evidence for a term, in this order:

1. Afghan Ministry of Public Health
2. Afghan Ministry of Higher Education
3. Kabul University of Medical Sciences (پوهنتون علوم طبی کابل)
4. Official Afghan medical curricula and textbooks
5. Other recognised Afghan medical universities
6. Other credible Afghan medical educational sources

Iranian sources, generic Persian dictionaries and general Persian websites are **not** evidence of
Afghan terminology.

**Never overclaim a source.** An entry may name an Afghan institution only when an actual, identifiable
document was examined, and the entry must identify it. A generic label such as *"Afghan medical
education usage"* is not evidence and must not appear in `source_authority`.

**Preserve legitimate international terminology.** Do not replace an established medical term merely
because a Dari translation is possible. The goal is **established Afghan medical terminology +
scientific precision + terminology familiar to Afghan medical students** — not maximum Dari translation.

**Mechanics for a new chapter**

- Add the term to `build_glossary.py` **before** using it. The scanner enforces whatever is in
  `forbidden_forms`, so adding a row is what makes a rule real.
- `forbidden_forms` is only for a **genuinely prohibited or non-canonical** form. Never put an Afghan
  transliteration variant there, and never put a **Dari gloss given in parentheses** there — the
  scanner would then flag a legitimate gloss. Two specific traps of each kind are recorded, with
  examples, in `editorial/terminology-correction-report.md` §1 and §6.
- `accepted_variants` is for a genuinely competing Afghan form. A form placed there is allowed, but the
  file may not then mix it with the canonical form.
- Put `NON-CANONICAL` in `usage_notes` when a forbidden form is merely non-canonical rather than
  Iranian, so the scanner tags it `[NONCANON]` instead of `[IRANIAN]`.
- *Editors: this README is itself scanned. Never quote a banned literal here — describe it instead.*

## 5. Production note

Currently **Markdown only**, by the author's decision for this pass. DOCX/PDF/EPUB generation from
this single Markdown source is deferred to a later stage. The Markdown is written so that it
converts cleanly: real heading hierarchy, pipe tables, no manual formatting.
