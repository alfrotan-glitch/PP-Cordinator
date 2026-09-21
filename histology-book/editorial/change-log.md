# Editorial Change Log
# لاگ تغییرات ادیتوریال

Classification scheme (one label per substantive change):
Editorial · Terminological · Scientific correction · Clinical correction · Updated evidence ·
Structural · Formatting · Publication/prepress

Pure copyediting (typos, obvious punctuation) is not logged individually.

---

## Session 1 — Foundation & Chapters 1–5

### Structural

| Location | Change |
|---|---|
| Whole book | Created the book skeleton: `README.md`, `00-front-matter.md`, `chapters/`, `glossary/`, `editorial/`, `qa/`, `scripts/` |
| Whole book | Adopted the 13-section topic template (Definition → Classification → Structure → Cells → Function → Structure–Function → Histological Appearance → Identification → Comparison → Clinical Correlation → HIGH-YIELD → SUMMARY TABLE → SELF-ASSESSMENT) |
| Whole book | Adopted the 12-point Reference Alignment Audit at the close of every chapter; canonical questions stored in `qa/audit-template.md` as the single source of truth |
| Whole book | Adopted Western Arabic numerals throughout, per Afghan technical/medical practice |

### Terminological

> **⚠ SUPERSEDED by Session 2 (Terminology Gate).** The decisions in this table were made from
> general impression, not from Afghan institutional sources. Rows marked 🔁 are revoked — see
> `editorial/terminology-decisions.md` and `glossary/terminology-glossary.csv` for the binding set.

| Term | Decision | Authority |
|---|---|---|
| Cell | 🔁 **سلول**, never یاخته → **حجره** (Session 2, MoHE/S7) | Afghan medical education usage |
| Connective tissue | 🔁 **بافت همبند**, never بافت پیوندی → **نسج منضم** (Session 2, S5/S6) | Afghan medical education usage |
| Cytoplasm | **سیتوپلازم**, never درون‌یاخته — *kept* (all three spellings are Afghan; not an Iranian form) | Afghan medical education usage |
| Mitochondria | **مایتوکندریا**, not میتوکندری | Afghan transliteration |
| Ribosome | **رایبوزوم**, not ریبوزوم | Afghan transliteration |
| Endoplasmic reticulum | **شبکه آندوپلاسمی**, not شبکه درون‌یاخته‌ای | Afghan medical education usage |
| Microvillus | **میکروویلی**, not ریزپرز | Afghan medical education usage |
| Cilium | **مژک**, not مژه (everyday word for eyelash) | Afghan medical education usage |
| Slide | **اسلاید**, not لام | Afghan lab usage |
| Light microscopy | **مایکروسکوپ نوری**, not میکروسکوپ نوری | Afghan spelling |
| Digestive | **هاضموی** (adjective) and **دستگاه هاضمه**, not گوارشی / دستگاه گوارش | Afghan clinical usage |
| Tendon | **تاندون**, not زردپی | Afghan clinical usage |
| Colon (fiber) | **کولاجن**, not کلاژن | Established Afghan rendering |
| Lysosome | **لایزوزوم**, not لیزوزوم | Afghan transliteration |
| Microtubule | **میکروتوبول** preferred over ریزنای | Both occur, but میکروتوبول is what students meet in exams |
| Mast cell | 🔁 **سلول مست** → **ماست‌سل** and **پلاسما‌سل**; ماست‌سل is a transliteration variant, NOT an Iranian form | Afghan transliteration |
| Section (of tissue) | **برش** preferred; مقطع noted as also current — *unchanged* | Consistency decision, not a contamination issue |

### Terminological — rejected entries (logged so they are not re-added)

| Rejected term | Why |
|---|---|
| `سل` as a forbidden form for سلول | سل is a **prefix of** سلول; listing it breaks word-boundary matching and is meaningless |
| `میکروتوبول` as a forbidden form | Not Iranian-specific; it is the form Afghan students meet in exams |
| `تارهای` as a forbidden form | Produced false positives as a substring of ساختارهای |
| `لام` (bare) as a forbidden form | Matched inside لامینا (lamina), which is a different word |
| مقطع as a forbidden form | Current in Afghan usage (e.g. مقطع عرضی); not Iranian-specific |

### Formatting

| Location | Change |
|---|---|
| `scripts/qa_scan.py` | 🔁 (Session 2) Replaced by a six-pass scanner — see below |
| `scripts/qa_scan.py` | Built a three-pass scanner: script contamination, Iranian-Persian terminology (word-boundary aware, glossary-driven), structural completeness |
| `scripts/qa_scan.py` | Added `--fix` mode for mechanical-only normalizations (Persian-Indic → Western digits, Unicode minus → ASCII hyphen). Terminology substitutions are deliberately NOT auto-fixed |
| Chapters 1–5 | Persian-Indic digits converted to Western digits |
| Chapters 1–5 | Unicode minus sign (U+2212) normalized to ASCII hyphen |
| Ch 2, Ch 4 | آنزیم‌های گوارشی → آنزیم‌های هاضموی (Afghan usage) |

### Editorial

| Location | Change |
|---|---|
| Ch 2 | Removed stray CJK characters that had entered the Dari text (病理, 核酸) and replaced them with correct Persian |
| Ch 2 | Fixed a duplicated-letter typo (لخطوط → خطوط) |
| Ch 4 | Fixed a mixed-script typo (granول → گرانول) |

### Scientific correction

No scientific corrections were required in this session. All content was written new from
established histology knowledge; no existing medical claim was altered.

---

## Session 2 — Terminology Gate (Chapters 1–5)

**Mandate:** no Iranian-Persian medical terminology anywhere in the book; every term decided
independently against Afghan sources; never invent a Dari equivalent; never replace an English term
merely because a Dari one exists.
**Verdict: PASS — 0 findings.** Full report: `editorial/terminology-decisions.md`.

### Terminological — canonical set (revokes Session 1)

| Term | Decision | Authority class |
|---|---|---|
| Cell / Cells / Cellular | **حجره / حجرات / حجروی** | AFGHAN STANDARD |
| Tissue / Tissues | **نسج / انساج** | AFGHAN STANDARD |
| Connective tissue | **نسج منضم** | AFGHAN STANDARD |
| Epithelial tissue | **نسج اپیتلیال** | AFGHAN STANDARD |
| Squamous / Stratified | **مسطح / مطبق** | AFGHAN STANDARD |
| Pathology / Histology / Cytology / Histopathology | **پتالوژی / هستولوژی / سایتولوژی / هستوپتالوژی** | AFGHAN STANDARD |
| Medicine / Physician | **طب / داکتر** | AFGHAN STANDARD |
| Disease / Patient / Treatment / Hospital | **مریضی / مریض / تداوی / شفاخانه** | AFGHAN STANDARD |
| Skin / Sebaceous glands | **جلد / غدوات شحمی** | AFGHAN STANDARD |
| Enzyme / Molecule / Ion | **انزایم / مالیکول / ایون** | COMMON AFGHAN TRANSLITERATION |
| Chemical / Metabolism / Nucleolus | **کیمیاوی / میتابولیسم / هسته‌چه** | AFGHAN STANDARD |
| Erythrocyte / Capillary | **کرویاتِ سرخ / موی‌رگ** | AFGHAN STANDARD |
| Blood vessels | **اوعیهٔ دموی** | AFGHAN STANDARD |
| Steroid / Carbohydrate / Phosphorylation | **استروئید / کاربوهایدریت / فسفوریلیشن** | COMMON AFGHAN TRANSLITERATION |

### Terminological — rejected Iranian-Persian forms (54 canonical replacements)

یاخته · سلول · بافت · بافت پیوندی · بافت رابط · بافت پوششی · بیمارستان · بیمار · بیماری · درمان ·
پزشک · پزشکی · دانشجو · دانشکده · کالبدشناسی · ریزپرز · ریزلوله · ریزرشته · شبکه درون‌یاخته‌ای ·
منشوری · غشای سلولی · گوارشی · سباسه · پاتولوژی · بافت‌شناسی · آنزیم · مولکول · شیمیایی · یون ·
متابولیسم · هستک · گویچه · مویرگ · استرویید · کربوهیدرات · فسفریلاسیون

### Terminological — deliberately NOT changed (logged so they are not re-flagged)

| Term | Why it stays |
|---|---|
| **کلیه / کبد / ریه** | The Afghan histology text S5 writes «لوبول **کبد**» — the formal *anatomical* register keeps the Arabic-derived names. These are not Iranian-Persian forms. General-usage Afghan equivalents (گرده/جگر/شش) are documented in the source list but not imposed on fixed anatomical names |
| **سیتوپلاسم / سیتوپلازم** | Both current in Afghanistan (S7, S8); not an Iranian/Afghan split. 98 instances left as-is |
| **مایتوکندریا** | Both مایتوکندریا and مایتوکاندریا are Afghan → registered as `accepted_variants`, not forbidden |
| **سنگفرشی / خشت‌فرشی / گوارشی** | Attested in Afghan teaching material (S5) → classified **NON-CANONICAL (book-consistency)**, NOT Iranian |
| **باکتری** | Equally current in Afghanistan; باکتریا registered as accepted variant |
| **ماتریکس / لایه / طبقه / مژک / سیلیا** | International or dual-use Afghan forms; no evidence of Iranian contamination |
| **آنتی‌ژن** | Afghan sources show آنتی‌ژن, آنتی نژ and آنتی‌نژن side by side (S5 uses «آنتی نژ»). Not prohibited, but **unresolved** → flagged `[VERIFY TERMINOLOGY]`, glossary decision `VERIFY FURTHER`, English form retained. **The only unresolved term in the book.** |

### Terminological — English retained (no Dari coinage, per gate rules 3–4)

`Cellulitis` · `paracellular (seal)` · `Urothelium` · `Goblet (cell)` · `Plasmalemma` · `Crista` ·
`PAS` · `H&E` · `IHC` · `ECM` · `GAG` · `LM`/`TEM`/`SEM` · `RBC`/`WBC` · `DNA`/`RNA`/`ATP` ·
plus all Latin anatomical and stain names. Rationale: these are the forms Afghan students meet in
exam questions; inventing Dari would make the book less usable. Distributed as
**42 English-retained registry entries**.

### Terminological — corrections to the glossary generator

Three slot-errors were found in `scripts/build_glossary.py` during the gate and corrected:

| # | Error | Correction |
|---|---|---|
| 1 | The 6th positional argument of the term helper was `first_appearance`, but it had been called as if it were `decision` — every such row was filed under the wrong column | Helper signature fixed to `(dari, eng, forb, src, notes, first, dec, conf, lat, abbr, acc)`; positional calls audited |
| 2 | ~10 **Latin/scientific** forms had been parked in `forbidden_forms` (پلاسمالما، ماتریکس، کریستا، اتصال مضبوط/چسبنده/شکافی، نیدوژن، گلیکوزآمینوگلیکان، هیالورونان) | Moved to `latin_term`; the scanner was then flagging its own Latin glossary as forbidden |
| 3 | Genuine Afghan synonyms (~20) were listed as forbidden (چندلایه، لامینای پایه، شل …) | Moved to `accepted_variants`; `چندلایه` de-forbidden (descriptive phrase); `لامینای پایه` de-forbidden — it is a **different structure** from غشای پایه (lamina = basement-membrane layer, not the membrane) |

A fourth, smaller artefact was removed in the same pass: three placeholder `T()`/`R.pop()` calls and
a dead `if False else` branch left over from an abandoned code path.

### Terminological — two inline special cases

| Location | Change | Rule applied |
|---|---|---|
| Ch 4 — paracellular pathway | `پاراسلولر` → **`(paracellular seal)`** with a Dari explanation | Gate rule 4: no reliable Afghan standard → keep English, do not invent |
| Ch 5 — skin infection | `سلولیت` → **`Cellulitis`** with a Dari explanation | Same rule 4; `Cellulitis` is the term used in Afghan clinical teaching |

### Structural

| Location | Change |
|---|---|
| `README.md` §3.2 | Iranian term list replaced by an 11-row canonical-term table plus a standardised-forms list |
| `README.md` §4.1 | Three-pass scanner description rewritten for the six-pass scanner; added `apply_terminology.py` / `build_glossary.py` to the pipeline description |
| `README.md` | Self-triggering example `granول` removed from the copyediting example list (it made the scanner flag its own documentation) |
| `00-front-matter.md` | Added a standing note explaining `[VERIFY TERMINOLOGY]` and its separation from `[VERIFY AGAINST JUNQUEIRA 17e]` |

### Formatting

| Location | Change |
|---|---|
| `scripts/qa_scan.py` | **Rewritten.** Six passes: `[SCRIPT]`, `[TERM]` (IRANIAN / NONCANON), `[INCONSIST]`, `[STRUCT]`, `[RETAINED]`, `[VERIFY]`. Glossary-driven; letter-boundary aware with ZWNJ and harakat as separators; `--fix` restricted to digits and U+2212 |
| `scripts/apply_terminology.py` | D1–D24 plus second-pass E1a–E24b rules; per-match `_is_letter()` boundary guard. **Executed once — 1,712 replacements.** Not idempotent; do not re-run |
| `scripts/apply_terminology_supplement.py` | **New, run once (34 replacements).** Pass 2 — clinical register; idempotent |
| `scripts/build_glossary.py` | **Run.** Emits 206 entries × 12 columns: `dari_term, english_term, latin_term, abbreviation, preferred_form, forbidden_forms, accepted_variants, source_authority, usage_notes, first_appearance, decision, confidence` |
| `glossary/terminology-glossary.csv` | 75 forbidden forms · 54 canonical · 25 accepted variants · 42 English-retained · 1 VERIFY FURTHER |

### Editorial — real defects found by the repaired passes

| Location | Defect | Fix |
|---|---|---|
| Ch 4 | `(جunctional)` — mixed-script word inside a Latin gloss | `(junctional)` |
| Ch 1 | `دادنturnover` — missing space | `دادن turnover` |
| Ch 2 | `ریزرشته(ها)` used as a Dari gloss of microfilament | `میکروفیلامنت` |
| Ch 5 | `شل` (6 occurrences) competing with `سست` for "loose" | `سست` |

### Scientific correction

None. The gate is a terminology gate: no definition, classification, mechanism or clinical claim was
altered. Every changed line is a term, a punctuation repair, or one of the four defects above. Line
counts are unchanged (137 / 975 / 1,441 / 1,086 / 1,079 / 1,152).

### Terminological — pass 2, the clinical register

Pass 1 fixed the core scientific layer (حجره / نسج / اپیتلیوم). A second, deliberately separate
review then asked whether the book also sounds Afghan in **ordinary clinical vocabulary**. It found
one more genuine Iran/Afghan divergence and settled nine previously open terms.

| Term | Decision | Authority |
|---|---|---|
| Drug / medicine | **دارو → دوا** (with, دوایی, دواها) | MoPH-sector text: «خدمات به شمول دوا غذا رایگان»، «دواخانه»، «دواسازی»، «ادویه»; the Afghan regulator is «اداره ملی ادویه و غذا» (dpmea.gov.af) |
| Chemotherapy | **شیمی‌درمانی → کیموتراپی** | Afghan transliteration; also forbids the artefact forms کیمیا تداوی / کیمیا‌تداوی |
| Lymphoid / lymphatic | **لمفوئید → لنفوئید، لمفاوی → لنفاوی** | Afghan faculty histology text: «ندول لنفاوی». The book had split لنفاوی 21× / لمفوئید 2× / لمفاوی 2× |
| Cytoplasm | **سیتوپلاسم** unified (سیتوپلازم → سیتوپلاسم) | Consistency decision — book used سیتوپلاسم 98× and سیتوپلازم 4× including the Ch 2 title. All three spellings are Afghan |
| Kidney / Liver / Lung | **کلیه، کبد، ریه kept** | Afghan MoPH: «امراض کلیه، از جمله عدم کفایه کلیه (گرده)»; Afghan hospital: «امراض کبدی یا جگر… سرطان کبد و هپاتیت»; «تومورهای ریه». Both forms are Afghan; the technical form belongs in a histology text |
| Pancreas | **پانکراس kept** | Afghan hospital: «مری، معده، روده کوچک، روده بزرگ، کبد، لوزالمعده». Both Afghan; پانکراس is the exam form |
| Allergy | **آلرژی kept** | Afghan hospital uses «تداوی حساسیت های…» — but in this book حساسیت already means hypersensitivity («حساسیت فوری»), a different concept |
| Infection | **عفونت kept** | Afghan clinic register: «تداوی امراض مختلفه انتانی (عفونت، مکروبی)» — the adjective is انتانی, the noun is عفونت |
| Membrane / Protein | **غشا، پروتئین kept** | Orthographic/transliteration variants only (غشا 302× vs غشاء 0×). No Afghan divergence |

Pass-2 volume: **35 changes** (34 scripted + 1 artefact repair). Combined with pass 1: **1,747**.

### Terminological — artefact repaired

| Location | Defect | Fix |
|---|---|---|
| Ch 3 | Pass 1's شیمی→کیمیا substitution had split شیمی‌درمانی into «کیمیا تداوی» | «کیموتراپی», and both artefact spellings added to `forbidden_forms` so it can never recur |

### Verification record

- `python3 scripts/qa_scan.py` → **RESULT: 0 findings**, exit 0.
- Structure self-tests: deliberately breaking `## 5. Function` (Ch 3) and `## 13. SELF-ASSESSMENT`
  (Ch 2) both produced the correct `[STRUCT]` finding; restoring them returned 0 findings.
  42 topics × 13 sections present.
- Change volume: **1,926 words across 1,693 changed lines** (difflib, word-level, vs pre-gate
  snapshots).

### Incident log (recorded for process honesty)

During the structure self-test, `chapters/02-the-cytoplasm.md` was restored from the pre-apply
snapshot in `/tmp/chapters_backup/`, which silently reverted the entire terminology pass on that file
(382 findings). Detected immediately by the scanner, and repaired by importing
`apply_terminology.py` as a module and re-running its rules on Ch 2 (371 replacements) plus the
Ch 2-specific fixes. **Process change: `/tmp/chapters_backup/` is a PRE-APPLY snapshot and is used
for diffing only — never as a restore source.**

---

---

## Session 2 addendum — deliverables of the Terminology Gate

| Deliverable | Where |
|---|---|
| Complete terminology audit of Chapters 1–5 + front matter | `editorial/terminology-decisions.md` §2, §9 |
| Mandatory decision table (English \| Current Book Term \| Proposed Afghan Term \| Evidence/Source \| Decision \| Confidence) | `editorial/terminology-decisions.md` §3 and §3b |
| Rebuilt glossary | `glossary/terminology-glossary.csv` — 206 entries × 12 columns |
| Scanner upgraded | `scripts/qa_scan.py` — six passes, 86 forbidden forms, self-tested |
| Two terminology passes | `scripts/apply_terminology.py` (1,712), `scripts/apply_terminology_supplement.py` (34 + 1 repair) |
| Decision report | `editorial/terminology-decisions.md` |
| QA evidence | `python3 scripts/qa_scan.py` → **RESULT: 0 findings**, exit 0 |

**Decision values used** (the only five permitted, per the gate):
`AFGHAN STANDARD`, `COMMON AFGHAN TRANSLITERATION`, `ENGLISH RETAINED`, `EXPLANATORY DARI ONLY`,
`VERIFY FURTHER`. `EXPLANATORY DARI ONLY` was **not** needed by any term in this pass; the one case
that would have required it (Cellulitis, paracellular seal) was handled by retaining the English term
with an inline Dari explanation, which is the same principle.

**[VERIFY TERMINOLOGY]** is kept strictly separate from `[VERIFY AGAINST JUNQUEIRA 17e]`:
the first is about *wording*, the second about *scientific facts*. One term is still on gate
hold: **آنتی‌ژن**, for which Afghan sources show آنتی‌ژن, آنتی نژ and آنتی‌نژن side by side. It is
not an Iranian-Persian form, so it is not prohibited; it is flagged rather than guessed, and the
book keeps the English-recognisable spelling.

---

---

## Session 3 — Corrective terminology audit (directive of 2026-09-21)

**Directive:** *never invent, construct, or literal-translate a medical/scientific term from English;*
for every term establish what Afghan medical professionals actually use, in the order
MoPH → MoHE → KUMS → other Afghan medical faculties → official Afghan curricula/textbooks → established
Afghan professional usage.
**Verdict:** the directive found a real methodology error. **4 term families were wrong and 77 in-text
corrections followed.** Full report: `editorial/terminology-correction-report.md`.

### Terminological — invented / constructed forms removed

| Term | Was | Now | Evidence |
|---|---|---|---|
| Chemotherapy | **کیمیا تداوی** — constructed by applying a correct شیمی→کیمیا rule to the compound شیمی‌درمانی | **کیموتراپی** | Afghan doctors' clinical writing: «تداوی دوایی، تداوی اشعوی، **کیموتراپی** و جراحی» |
| Carbohydrate | **کاربوهایدریت** — transliterated morpheme by morpheme (carbo- + hydrate); appears in **no** Afghan source | **کربوهیدرات** (standard transliteration restored) and flagged `[VERIFY TERMINOLOGY]` | Afghan textbooks write «قندها»; no single Afghan term for "carbohydrate" could be established, so no term was invented |

### Terminological — Iranian forms that had been missed (36 + 21 occurrences)

| Term | Was | Now | Evidence |
|---|---|---|---|
| Organelle | **اندامک** ×36 | **ارگانل** ×36 | Afghan MoE Biology Grade 7: «ساختمان‌های کوچکی … به‌نام اعضاچه یا **ارگانل** (Organelle) حجره یاد شده» |
| Neuron | **نورون** ×21 | **نیورون** ×21 | Afghan MoE Science Grade 12: «**نیورون** دوم سیناپسی را بیشتر تحریک کنند» |
| Mitochondrial | **میتوکندریایی** ×8 | **مایتوکندریایی** ×8 | TolAfghan: «**مایتوکاندریا** (Mitochondria)» — aligning with the book's attested canonical form |

**Corrections total 77.** No invented term was substituted for any other term: each correction moved
*toward* established Afghan usage or toward the established transliteration.

### Terminological — verified and deliberately left alone

پروتئین (TolAfghan: «دو نوع **پروتئین** کروی»), سیتوپلاسم, کلیه/کبد/ریه/پانکراس, باکتری, اسلاید,
لایه/طبقه, جلد, موی‌رگ, غدوات, استوانه‌ای, نیورون. Per the directive, a term that is already the
established medical term used in Afghanistan was **not** replaced merely because another Dari form is
theoretically possible.

### Evidence anchoring — the structural fix

| Change | Effect |
|---|---|
| `source_authority` now names an actual Afghan document, quoted verbatim | 42 entries anchored (was 12) |
| The generic label *"Afghan medical education usage (MOHE curriculum…)"* is no longer treated as evidence | 139 entries honestly re-labelled: transliteration retained, **no Afghanistan-specific documentary source located** |
| New `INVENTED_CONSTRUCTIONS` blacklist in `build_glossary.py` | 101 forbidden forms now enforced (was 86) |
| `DROP_ROWS` | the superseded pass-1 row for the invented carbohydrate term can never contradict the restored one |
| Scanner self-test by re-injection | 11/11 — every corrected form is caught; the legitimate gloss چندلایه is correctly **not** caught |

### Structural

| Location | Change |
|---|---|
| `README.md` §4.2 | Rewritten: the evidence hierarchy, the ban on morpheme construction, the rule that a term enters the glossary only with a named Afghan document, and a note that the README must never quote a banned literal (it is itself scanned) |
| `editorial/terminology-decisions.md` | Marked superseded-in-part; points to the correction report |
| `qa/reference-alignment-audit.md` | §3b updated with the correction outcome |
| `00-front-matter.md` | `[VERIFY TERMINOLOGY]` note now lists **two** terms (آنتی‌ژن, کربوهیدرات) |

### Scientific correction

None. As in passes 1–2 this is a terminology operation: no definition, classification, mechanism or
clinical claim was altered. Line counts are unchanged (146 / 975 / 1441 / 1086 / 1079 / 1152).

### Verification record

- `python3 scripts/qa_scan.py` → **RESULT: 0 findings**, exit 0 (101 forbidden forms, 207 entries).
- Zero occurrences of اندامک، نورون، کاربوهایدریت، کیمیا تداوی، میتوکندریایی anywhere.
- Re-injection self-test: 11/11 as above.

## Open issues (not yet resolved)

See `qa/reference-alignment-audit.md` §3 — 20 items flagged `[VERIFY AGAINST JUNQUEIRA 17e]`
awaiting confirmation against the reference text. One **terminology** item is also open:
**آنتی‌ژن** (`[VERIFY TERMINOLOGY]`, glossary decision `VERIFY FURTHER`). Both classes are recorded
here rather than silently resolved, per the standing rule that a flagged gap is honest and a
fabricated answer is a defect. These are recorded here rather than silently
resolved, per the standing rule that a flagged gap is honest and a fabricated answer is a defect.
