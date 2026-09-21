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

---

## Session 4 — Final Terminology Evidence Gate

**Purpose:** lock the terminology policy before Chapter 6 and verify the 208 glossary entries.
**Report:** `editorial/final-terminology-evidence-gate.md`. **Result: PASS.**

### Policy (not a rewrite — this session made three corrections only)

| # | Change | Detail |
|---|---|---|
| 1 | **Canonical rule locked** in `README.md` §4.2 | "Use the established medical terminology actually used in Afghanistan…" + source hierarchy (MoPH → MoHE → KUMS → official curricula → recognised Afghan medical universities → credible Afghan medical educational sources) + the ban on constructing a term from English morphemes + the ban on overclaiming a source + the duty to preserve legitimate international terminology |
| 2 | **Carbohydrate → ENGLISH RETAINED** | The invented form is withdrawn and the transliteration is **not** adopted either. Neither could be anchored to an Afghan source, so per policy the English term is retained and flagged `[VERIFY TERMINOLOGY]`. «قندها» was **not** adopted — it is a general biological expression for sugars, not a medical terminology standard |
| 3 | **Source-honesty correction** | 31 entries carried labels that named no document ("Afghan medical education usage", "Project canonical decision — Afghan usage confirmed by sources"). Each now either names an actual Afghan document with a verbatim quote, or declares itself an owner-mandated decision that is explicitly **not** an evidence claim, or states that no Afghanistan-specific source was located |

### Verification

| Check | Result |
|---|---|
| Entries naming an Afghan institution that fail to identify a document | **0** |
| Generic labels such as "Afghan medical education usage" remaining | **0** |
| Iranian sources / Persian dictionaries cited as evidence | **0** |
| Iranian-Persian forms in the book (33-form candidate list) | **0**, with one documented permission: چندلایه ×1, a parenthetical Dari gloss of شبه‌مطبق |
| Constructed terms (morpheme-by-morpheme) remaining | **0** |
| Compositional Dari forms not independently attested | **30 — listed in full in the gate report §5, reported for the author's decision, not changed** |
| KUMS-anchored entries | **0 — stated as a gap, not claimed** |
| Scanner | **0 findings**, exit 0 |

### Structural

| Location | Change |
|---|---|
| `README.md` §4.2 | Rewritten as the binding policy; the self-triggering example removed (the README is itself scanned) |
| `scripts/qa_scan.py` | "unresolved terminology" is now keyed on **confidence**, so an English-retained but unverified term stays visible |
| `scripts/build_glossary.py` | `SOURCE_FIX` map (31 entries) + precise document identifiers in every source string |
| `00-front-matter.md` | `[VERIFY TERMINOLOGY]` note now lists آنتی‌ژن and Carbohydrate |
| Chapters 1, 2, 5 | `Carbohydrate` substituted for the Dari forms (12 occurrences) |

### Scientific correction

None. Line counts unchanged (146 / 975 / 1441 / 1086 / 1079 / 1152).

---

## Session 5 — Targeted junction terminology evidence check

**Scope:** three terms only. No other terminology changed. Report:
`editorial/junction-terminology-check.md`.

| Term | Evidence found | Outcome |
|---|---|---|
| Tight junction / Zonula occludens | **`اتصال مضبوط`** — wasiweb.com «حجروي اتصال، د اتصال ډولونه», byline «قاسم خان همت **کندهار طب پوهنځۍ** محصل» (Kandahar Faculty of Medicine student): «①مضبوط اتصال【Tight junction】»، «د مضبوط اتصال وظایف» | **PASS** — glossary decision upgraded to AFGHAN STANDARD (MEDIUM). Not the Iranian form (Iranian = اتصالات محکم / اتصال تنگ) |
| Adherens junction / Zonula adherens | No Afghan Dari form located. TolAfghan «هستولوژي Histology — دوهمه برخه»: «**Zonula Adherence = Intermediate Juntion**»; wasiweb: «**adherence junction**». The retained Dari form matches the **Iranian** «اتصالات چسبنده» | **FLAGGED** `[VERIFY TERMINOLOGY]` — retained, decision owed |
| Gap junction | No Afghan Dari form located. Afghan usage is the transliteration: «**ګپ جنکشن** Gap Junction» (wasiweb), «**درز junction** یا gap junction» (wasiweb), «٤-**Gapjunction**» (ps.wikipedia). Nearest Persian form اتصال شکاف‌دار is Iranian | **FLAGGED** `[VERIFY TERMINOLOGY]` — retained, decision owed |

### Terminological

| Location | Change |
|---|---|
| Glossary — `اتصال مضبوط` | decision `COMMON AFGHAN TRANSLITERATION` → **AFGHAN STANDARD**; source_authority replaced with the named document + verbatim quotations |
| Glossary — `اتصال چسبنده`, `اتصال شکافی` | decision → **VERIFY FURTHER**, confidence UNRESOLVED; source_authority records every Afghan document examined |
| Ch 4 §4.3 | one bilingual terminology note: international names are used because Afghan sources use them; `اتصال مضبوط` is attested for tight junction; adherens and gap junction carry `[VERIFY TERMINOLOGY]` |
| `00-front-matter.md` | `[VERIFY TERMINOLOGY]` list updated to include the two junction equivalents |

Not done, deliberately: no inversion, no new term, no new forbidden form, no other terminology change.

### Correction to my own earlier reports

Reading the sources directly for this check exposed two overstatements in
`editorial/terminology-correction-report.md` and `final-terminology-evidence-gate.md`. Both corrected in
the report; neither term changed, per instruction.

| Earlier claim | Correction |
|---|---|
| «کاربوهایدریت appears in NO Afghan source» | **Wrong.** TolAfghan «فزیولوژی حجره» (tolafghan.com/posts/30498) writes «سایر لیپیدها ۴ فیصد و **کاربوهایدریت‌ها** ۳ فیصد». The Afghan-pattern transliteration does occur in an Afghan source. `Carbohydrate` stays English-retained because no Afghan source uses `کربوهیدرات`, but the basis is weaker than reported |
| «اندامک was the Iranian form» | **Half right.** The same TolAfghan page writes «به اجزای درون حجره **اندامک** گفته می‌شود», so an Afghan author uses it. `ارگانل` still stands on **institutional precedence** (the official MoE Grade-7 curriculum writes «ارگانل (Organelle)»), not on `اندامک` being un-Afghan |

Process note recorded: TolAfghan is an Afghan source with a **mixed register** (the same page contains
حجره and سلول, انزایم and انزیم, مایتوکاندریا and مایتوکندریا). It is good evidence of what an Afghan
author uses and weaker evidence of institutional standardisation; the institutional tier must keep
outranking it.

### Verification

`python3 scripts/qa_scan.py` → **RESULT: 0 findings**, exit 0.
`[VERIFY TERMINOLOGY]` 4 · unresolved: اتصال چسبنده, اتصال شکافی, آنتی‌ژن, Carbohydrate.
Scientific content unchanged.

**Chapter 6 remains blocked** — 2 of 3 terms flagged, decisions owed.

---

## Session 6 — Final terminology lock: gate CLOSED, Chapter 6 unblocked

Report: `editorial/final-terminology-lock.md`. Scope = the owner's final decisions only; no other
terminology decision reopened, no scientific content changed.

### Decisions applied

| Item | Final state | Evidence |
|---|---|---|
| Tight junction | canonical **Tight junction / Zonula occludens**; «مضبوط اتصال» permitted as an Afghan Dari gloss, not the scientific term | wasiweb.com, «حجروي اتصال، د اتصال ډولونه» (Kandahar Faculty of Medicine student) |
| Adherens junction | canonical **Adherens junction / Zonula adherens**; no Dari equivalent invented; former calque non-canonical + enforced | TolAfghan «هستولوژي Histology — دوهمه برخه»; wasiweb «adherence junction» |
| Gap junction | canonical **Gap junction**; no Dari equivalent invented; former calque non-canonical + enforced | wasiweb «ګپ جنکشن Gap junction»; ps.wikipedia «Gapjunction» |
| Carbohydrate | canonical **کاربوهایدریت**; `[VERIFY TERMINOLOGY]` removed | TolAfghan, «فزیولوژی حجره» — «… سایر لیپیدها ۴ فیصد و کاربوهایدریت‌ها ۳ فیصد» |
| Organelle | **ارگانل** canonical (Afghan MoE Grade-7 textbook); **اندامک** = ACCEPTED AFGHAN VARIANT, no longer prohibited | TolAfghan — «به اجزای درون حجره اندامک گفته می‌شود» |
| Policy | README §4.2 rewritten: 5-level decision hierarchy, three absolute prohibitions, locked examples table, and "used in Iran ≠ prohibited" | owner directive, 2026-09-21 |

### Changes

- **Chapters:** 11 Latin *Carbohydrate* phrases → کاربوهایدریت (Ch1 ×4, Ch2 ×5, Ch5 ×2) + the
  front-matter PAS row and the flag note.
- **Ch4 §4.3 note** rewritten — international junctions canonical, no invented equivalents.
- **`00-front-matter.md`:** `[VERIFY TERMINOLOGY]` now describes exactly **one** term (آنتی‌ژن).
- **`build_glossary.py`:** carbohydrate row re-anchored to a named document; artificial blacklist
  entries for the two settled forms removed; organelle variant registered; junction rows re-keyed to
  the international terms; KUMS constant added; evidence-source constants hoisted above first use.
- **`qa_scan.py`:** per-form Iranian vs non-canonical classification (79 / 23) instead of one
  row-level keyword.
- **`scripts/selftest_terminology.py`:** NEW permanent self-test — injection (102 forbidden forms),
  clean (208 canonical forms), and the locked decisions.
- **KUMS evidence gap CLOSED:** 5 rows now cite the KUMS bulletin examined this session.

### Corrections to earlier reports

- «کاربوهایدریت appears in no Afghan source» — **withdrawn**; the form is attested and canonical.
- «اندامک is the Iranian form» — **revised**; it is an accepted Afghan variant, and ارگانل is canonical
  on institutional precedence.
- Supersession banners added to `terminology-correction-report.md`, `final-terminology-evidence-gate.md`,
  `junction-terminology-check.md`, `terminology-decisions.md`.

### Defects found by the new self-test and fixed

1. One form was listed as both prohibited and acceptable (an earlier override contradicting a later
   blacklist). The later decision stands; the contradiction was removed.
2. Constructed forms were being *reported* as Iranian-Persian violations. Classification is now
   per form. No term's status changed.

### Flagged for the owner (evidence raised, decision not taken)

1. KUMS uses the book's clinical register; search snippets from other KUMS news items also show the
   Persian patient word. Not examined → not evidence → nothing changed.
2. پوهنحی (MoHE) vs پوهنځی (KUMS) — two official Afghan spellings, one chapter uses the latter.
3. A registered accepted variant may not share a file with its canonical form.

### Verification

```
python3 scripts/qa_scan.py                -> RESULT: 0 findings, exit 0
python3 scripts/selftest_terminology.py   -> SELFTEST: ALL PASS
```

208 glossary entries · 102 forbidden · 64 canonical · 39 accepted variants · 43 English-retained ·
1 unresolved (آنتی‌ژن) · `[VERIFY TERMINOLOGY]` 2 · `[VERIFY AGAINST JUNQUEIRA 17e]` 25.

**Terminology Gate: FINAL AND CLOSED. Chapter 6 (Adipose Tissue) unblocked.**

---

## Session 7 — Chapter 6 (Adipose Tissue) written under the locked policy

**File:** `chapters/06-adipose-tissue.md` — 914 lines, 5 topics, each with all 13 mandated sections,
plus the chapter self-assessment and the 12-point reference alignment audit.

| Topic | Content |
|---|---|
| 6.1 | نسج شحمی: تعریف، منشأ و طبقه‌بندی — definition, mesenchyme origin, white/brown/beige |
| 6.2 | نسج شحمی سفید (Unilocular) — structure, signet-ring, frozen-section stains, lipoma |
| 6.3 | نسج شحمی قهوه‌ای (Multilocular) — UCP1/ترموجنین, sympathetic control, neonatal thermogenesis |
| 6.4 | تنظیمِ میتابولیک و وظیفهٔ اندوکراین — LPL/HSL/ATGL, leptin, adiponectin, insulin |
| 6.5 | منشأ، توزیع و پیوندِ بالینی — lipoblast, lipoma/liposarcoma/hibernoma, fat embolism |

### Terminology — new terms registered BEFORE first use

20 new glossary rows, all under the locked policy: none constructed, none translated word by word.
The only phrase assembled from Afghan forms is **نسج شحمی** (canonical نسج + canonical شحمی), recorded
MEDIUM with an explicit note that the assembled phrase was not found verbatim in a document.
**Unilocular / Multilocular are retained in English** precisely because a Dari equivalent would have
had to be constructed. 14 new `[VERIFY AGAINST JUNQUEIRA 17e]` markers were added (book total 39).

### Scanner as the pre-introduction check — it worked

The draft was scanned before acceptance and **9 pre-lock forms were caught and corrected**: بافت/بافت‌های ×2,
سلولی ×3, بیماری, پوست, and one garbled differential bullet. This is the first chapter written with the
locked system in place, and the check did its job — nothing was waved through.

### State

`qa_scan.py` → **RESULT: 0 findings** · `selftest_terminology.py` → **ALL PASS** ·
glossary 228 entries · per-chapter matrix in `qa/reference-alignment-audit.md` now has a Ch 6 row
(✅ draft, ⚠️ on check 11 only, like every other chapter).

**Next chapter: Chapter 7 — Cartilage.**

## Open issues (not yet resolved)

See `qa/reference-alignment-audit.md` §3 — 20 items flagged `[VERIFY AGAINST JUNQUEIRA 17e]`
awaiting confirmation against the reference text. One **terminology** item is also open:
**آنتی‌ژن** (`[VERIFY TERMINOLOGY]`, glossary decision `VERIFY FURTHER`). Both classes are recorded
here rather than silently resolved, per the standing rule that a flagged gap is honest and a
fabricated answer is a defect. These are recorded here rather than silently
resolved, per the standing rule that a flagged gap is honest and a fabricated answer is a defect.
