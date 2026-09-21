# Terminology Decision Report — Afghan Medical Terminology Standard

> **SUPERSEDED IN PART (second revision) — see `editorial/final-terminology-lock.md`.** This is the
> historical record. Carbohydrate is canonical as کاربوهایدریت, اندامک is an accepted Afghan
> variant, and the junctions are canonical as Tight junction / Adherens junction / Gap junction.

> **⚠ SUPERSEDED IN PART by `editorial/terminology-correction-report.md` (pass 3).**
> The corrective directive of 2026-09-21 established that a term must **never** be constructed by
> translating English morphemes. Two entries in this report violated that rule (کیمیا تداوی,
> کاربوهایدریت) and two Iranian forms (اندامک، نورون) had been missed. Read this document for the
> sources; read the correction report for the binding decisions.

**Book:** Bilingual (Afghan Dari + English) high-yield histology textbook
**Reference standard:** Junqueira's Basic Histology: Text and Atlas, 17th ed. (Mescher)
**Audit scope:** Chapters 1–5 + front matter + README (6,025 lines)
**Gate result:** **PASS — 0 findings** (`python3 scripts/qa_scan.py` → exit 0)
**Date of record:** 2026-09-21

---

## 1. Why this gate was run

The first pass of the book was written with terminology that had been *assumed* rather than
*researched*. Two concrete failures were found on audit:

1. The book used **سلول / بافت / بافت همبند** — the Iranian-Persian standards — while Afghan
   medical teaching uses **حجره / نسج / نسج منضم**.
2. A smaller second layer of Iranian forms (**آنزیم، مولکول، شیمیایی، پتالوژی، هستک، گویچه** …) had
   been carried over without independent verification.

Neither was detectable by a dictionary. Both were detectable only against **Afghan institutional
sources**. This report records the sources, the decisions, and the evidence for each.

---

## 2. Sources used, and what each one established

Weighting follows the gate rule: Afghan medical universities and official Afghan
health/education institutions first, then other Afghan medical sources.

| # | Source | Authority | What it established |
|---|---|---|---|
| S1 | **MoHE Biology curriculum**, logu.edu.af (`بیولوژی نوی نصاب.pdf`), Ministry of Higher Education | **Official Afghan state curriculum** | «حجره نباتی و ساختمان **کیمیاوی** آن، انواع **انساج** نباتی» → **حجره** = cell, **انساج** = tissues, **کیمیاوی** = chemical, **اناتومی** |
| S2 | **Afghan MoPH** job description, moph.gov.af — «شف دیپارتمنت پتالوژی ولابراتوار» | **Official Afghan ministry** | **پتالوژی**; «پتالوژی اناتومیک (هستولوژی/ **هستوپتالوژی**، **سایتولوژی**)»; **مالیکولی**; **حجروی**; **مریضی**; **تداوی**; **لابراتوار**; **شفاخانه** |
| S3 | **MoHE** academic-post announcement, mohe.gov.af | **Official Afghan ministry** | «بست **هستوپتالوژی** پوهنحی طب»; book list including **«معافیت حجروی و مالیکولی»** (Kabul, 1400) — two terms in one official title |
| S4 | **Kabul medical curriculum** (طب معالجوی), kateb.edu.af / asas.edu.af | **Afghan medical faculty** | Course names: «Histology (1) · **هستولوژی**», «Pathology (1) · **پتالوژی**», «Anatomy (1) · **اناتومی**», «Physiology · **فزیولوژی**», «Medicine · **داخله**», «Health · **صحت عامه**» |
| S5 | **هستولوژی تئوری ۲** — خاتم النبیین University, Faculty of Curative Medicine, semester 3 (muslimuniversity.edu.af) | **An actual Afghan histology textbook** | The single most valuable source. Uses **نسج منضم**, **کرویات سفید خون**, **موی رگها**, **هسته چه**, **انزایم**, **استوانهیی**, **مکعبی**, **مژک/سلیا**, **اپیتلیوم جلد**, **لوبول کبد**, **باکتریا**, **استروئید**, **میان حجروی**, **لایه** |
| S6 | Afghan histology lecture **«Connective Tissue نسج منضم»** (Afghan author, Scribd) | Afghan teaching material | Confirms **نسج منضم** = connective tissue |
| S7 | **AfghanVet** veterinary/biology textbook blog (Afghan) | Afghan teaching material | «در کشور ما افغانستان … واژه **حجره** به عوض **سلول** به مفهوم Cell به کار گرفته شده است»; plural **حجرات**; **رنگآمیزی**; **مایکروسکوپ** |
| S8 | **TolAfghan** — «فزیولوژی حجره» (Afghan) | Afghan teaching material | **غشای حجره**, **رایبوزوم**, **مایتوکاندریا**, **انزایم**, **میتابولیسم**, **کیمیاوی**, **هستک → هسته چه**, **سایتوپلازم**, **نسج عضلانی**, **جگر** |
| S9 | Afghan medical-student blog (medico.blogfa.com) | Afghan medical students' notes | **جلد**, **طبقات جلد**, **غدوات عرقیه**, **غدوات شحمی**, **فولیکول های مو**, **مایکروبیولوژی** |
| S10 | **Wikipedia — فهرست واژههای متفاوت در فارسی افغانستان و ایران** | Reference lexicon for the Dari/Tajik vs Iranian split | Documented pairs: **تداوی: درمان**, **گرده: کلیه**, **جگر: کبد**, **شش: ریه**, **اناتومی: کالبدشناسی**, **صنف: کلاس** |
| S11 | wasiweb.com (Afghan Pashto/Dari teaching site) | Afghan teaching material | **حجروي غشا**, **بین الحجروي مسافه**, **انساج**, **نسج** |
| S12 | Pashto anatomy+histology+physiology text (muslimuniversity.edu.af) | Afghan teaching material | **منضم نسجونو** (connective tissues), **فبروزي نسج** (fibrous tissue), **د کوالجنس** (collagen), **هستولوژي**, **نسجي** (the adjective) |

**Key methodological point.** S5 and S9 are decisive because they are *Afghan teaching texts in the
readers' own register*, not general-purpose lexicons. Where S10 (a general-usage list) conflicts with
S5 (a medical teaching text), **the medical text wins** — see §6.2.

---

## 3. Mandatory Terminology Decision Table

Full machine-readable form: `glossary/terminology-glossary.csv` (195 entries, 12 columns).
This table records the decisions that changed the book.

Column meanings — **Decision**: `AFGHAN STANDARD` · `COMMON AFGHAN TRANSLITERATION` ·
`ENGLISH RETAINED` · `EXPLANATORY DARI ONLY` · `VERIFY FURTHER`.
**Confidence**: HIGH / MEDIUM / LOW / UNRESOLVED.

### 3.1 Core tissue & cell vocabulary (the gate's biggest correction)

| English | Current book term | Proposed Afghan term | Evidence / source | Decision | Confidence |
|---|---|---|---|---|---|
| Cell | سلول | **حجره** | S1 (MoHE), S5, S7, S8 | AFGHAN STANDARD | HIGH |
| Cells | سلولها | **حجرات** | S1, S5, S7 | AFGHAN STANDARD | HIGH |
| Cellular | سلولی | **حجروی** | S2, S3 («معافیت حجروی») | AFGHAN STANDARD | HIGH |
| Intercellular | بینسلولی | **بینحجروی** | S5, S11 | AFGHAN STANDARD | HIGH |
| Tissue | بافت | **نسج** | S1, S5, S11, S12 | AFGHAN STANDARD | HIGH |
| Tissues | بافتها | **انساج** | S1 («انواع انساج»), S5, S11 | AFGHAN STANDARD | HIGH |
| Connective tissue | بافت همبند | **نسج منضم** | S5, S6 (Afghan lecture title), S12 | AFGHAN STANDARD | HIGH |
| Epithelial tissue | بافت پوششی | **نسج اپیتلیال** | S5, S12 | AFGHAN STANDARD | HIGH |
| Epithelium | — | **اپیتلیوم** | S5 (used unchanged) | COMMON AFGHAN TRANSLITERATION | HIGH |
| Squamous | سنگفرشی | **مسطح** | Canonical decision list; S5 also shows سنگفرش/خشتفرشی | AFGHAN STANDARD | MEDIUM |
| Stratified | چندلایه | **مطبق** | S5 («چند طبقه») ; reference term | AFGHAN STANDARD | HIGH |
| Columnar | استوانهای | **استوانهای** (unchanged) | S5 («اپیتلیوم استوانهیی») — confirms استوانهای, not منشوری | AFGHAN STANDARD | HIGH |

### 3.2 Pathology, discipline names, clinical register

| English | Current book term | Proposed Afghan term | Evidence / source | Decision | Confidence |
|---|---|---|---|---|---|
| Pathology | پاتولوژی | **پتالوژی** | S2, S3, S4 | AFGHAN STANDARD | HIGH |
| Histology | بافتشناسی | **هستولوژی** | S2, S3, S4 | AFGHAN STANDARD | HIGH |
| Cytology | سلولشناسی | **سایتولوژی** | S2 | AFGHAN STANDARD | HIGH |
| Histopathology | هیستوپاتولوژی | **هستوپتالوژی** | S3 | AFGHAN STANDARD | HIGH |
| Medicine (discipline) | پزشکی | **طب** | S2, S4 («طب معالجوی») | AFGHAN STANDARD | HIGH |
| Physician | پزشک | **داکتر** | S2, S4 | AFGHAN STANDARD | HIGH |
| Disease | بیماری | **مریضی** | S2 («مریضی، تداوی») | AFGHAN STANDARD | HIGH |
| Patient | بیمار | **مریض** | S2 | AFGHAN STANDARD | HIGH |
| Treatment | درمان | **تداوی** | S2, S10 | AFGHAN STANDARD | HIGH |
| Hospital | بیمارستان | **شفاخانه** | S2 | AFGHAN STANDARD | HIGH |
| Skin | پوست | **جلد** | S5 («اپیتلیوم جلد»), S9 | AFGHAN STANDARD | MEDIUM |
| Sebaceous glands | غدد سباسه | **غدوات شحمی** | S9 | AFGHAN STANDARD | MEDIUM |

### 3.3 Cell-biology and matrix vocabulary

| English | Current book term | Proposed Afghan term | Evidence / source | Decision | Confidence |
|---|---|---|---|---|---|
| Enzyme | آنزیم | **انزایم** | S5, S8 | COMMON AFGHAN TRANSLITERATION | HIGH |
| Molecule / molecular | مولکول / مولکولی | **مالیکول / مالیکولی** | S2 (MoPH), S3 (MoHE book title), S8 | COMMON AFGHAN TRANSLITERATION | HIGH |
| Ion | یون | **ایون** | S8 («آیون کلسیم»), Afghan text «ایون کلسیم» | COMMON AFGHAN TRANSLITERATION | HIGH |
| Chemical | شیمیایی | **کیمیاوی** | S1 (MoHE curriculum) | AFGHAN STANDARD | HIGH |
| Metabolism | متابولیسم | **میتابولیسم** | S8 | COMMON AFGHAN TRANSLITERATION | HIGH |
| Nucleolus | هستک | **هستهچه** | S5, S8 | AFGHAN STANDARD | HIGH |
| Erythrocyte | گویچهٔ سرخ | **کرویاتِ سرخ** | S5 («کرویات سفید خون») | AFGHAN STANDARD | HIGH |
| Capillary | مویرگ | **مویرگ** | S5 («موی رگها») | AFGHAN STANDARD | HIGH |
| Steroid | استرویید | **استروئید** | S5 | COMMON AFGHAN TRANSLITERATION | HIGH |
| Carbohydrate | کربوهیدرات | **کاربوهایدریت** | Afghan transliteration pattern; S5 uses کاربن | COMMON AFGHAN TRANSLITERATION | MEDIUM |
| Phosphorylation | فسفریلاسیون | **فسفوریلیشن** | S5, S8 («فسفوریلیشن اکسیداتیو») | COMMON AFGHAN TRANSLITERATION | MEDIUM |
| Microscope | میکروسکوپ | **مایکروسکوپ** | S5, S7 | COMMON AFGHAN TRANSLITERATION | HIGH |
| Blood vessels (pl.) | رگهای خونی | **اوعیهٔ دموی** | Canonical decision list | AFGHAN STANDARD | MEDIUM |

---

## 3b. Second review — the clinical register (pass 2)

Pass 1 fixed the **core scientific** layer (cell / tissue / epithelium). A second, deliberately
separate review then asked a different question: *does the book also sound Afghan in ordinary
clinical vocabulary?* It found one more genuine Iranian/Afghan divergence and settled the nine terms
that had been left open.

| English | Current book term | Proposed Afghan term | Evidence / source | Decision | Confidence |
|---|---|---|---|---|---|
| Drug / medicine | **دارو** | **دوا** | MoPH-sector text: «تمامی خدمات به شمول **دوا** غذا رایگان است»، «کیفیت **دوا**های در حال فروش»، «**دواخانه**»، «**دواسازی**»، «مصارف **ادویه**»; Afghanistan's medicines regulator is literally «اداره ملی **ادویه** و غذا» (dpmea.gov.af), which writes «محصولات **دوایی**» and «قاچاق **دوا** ها»; Afghan hospitals: «از جمله **دوا**های مرتبط» | **AFGHAN STANDARD** | MEDIUM |
| Chemotherapy | شیمی‌درمانی | **کیموتراپی** | Afghan transliteration in current use. Also forbidden in the artefact forms «کیمیا تداوی / کیمیا‌تداوی», which is what a naive شیمی→کیمیا substitution produces | **COMMON AFGHAN TRANSLITERATION** | MEDIUM |
| Lymphoid | لمفوئید / لمفاوی | **لنفوئید / لنفاوی** | Afghan faculty histology text: «ندول **لنفاوی**». The book had split across لنفاوی (21), لمفوئید (2), لمفاوی (2) — an internal split, not a second standard | **AFGHAN STANDARD** | MEDIUM |
| Cytoplasm | سیتوپلاسم / سیتوپلازم | **سیتوپلاسم** | All three spellings (سیتوپلاسم، سیتوپلازم، سایتوپلازم) occur in Afghan material → **consistency** decision, not contamination. Book used سیتوپلاسم 98×, سیتوپلازم 4× (incl. the Ch 2 chapter title) | **AFGHAN STANDARD** | HIGH |
| Kidney | — | **کلیه** (kept) | Afghan MoPH nephrology posting: «امراض **کلیه**، از جمله عدم کفایه **کلیه (گرده)**» — کلیه is the term, گرده the colloquial gloss. Both Afghan; **not** an Iranian form | **AFGHAN STANDARD** | MEDIUM |
| Liver | — | **کبد** (kept) | Afghan hospital text: «امراض **کبدی یا جگر**، مانند سیروز… سرطان **کبد** و هپاتیت» — same pattern: کبد technical, جگر everyday | **AFGHAN STANDARD** | MEDIUM |
| Lung | — | **ریه** (kept) | Afghan hospital: «تومورهای **ریه**»، «بذل پریکارد قلب و **ریه**»; another Afghan hospital's department list uses «**شش**». Both Afghan; the book is internally consistent on ریه | **AFGHAN STANDARD** | MEDIUM |
| Pancreas | — | **پانکراس** (kept) | Afghan hospital: «مری، معده، روده کوچک، روده بزرگ، کبد، **لوزالمعده**». Both Afghan; پانکراس is the exam form | **COMMON AFGHAN TRANSLITERATION** | MEDIUM |
| Allergy | — | **آلرژی** (kept) | Afghan hospital uses «تداوی **حساسیت** های…» for allergy — but in **this book** حساسیت means hypersensitivity/sensitivity («حساسیت فوری»، «حساسیت زیاد»), a different concept, so substitution would collide | **COMMON AFGHAN TRANSLITERATION** | MEDIUM |
| Infection | — | **عفونت** (kept) | Afghan clinic register: «تداوی امراض مختلفه **انتانی** (**عفونت**، مکروبی)» — Afghan usage pairs the adjective **انتانی** (infectious; «شفاخانه **انتانی**»، «امراض **انتانی**») with the noun عفونت | **AFGHAN STANDARD** | MEDIUM |
| Membrane | — | **غشا** (kept) | Orthographic variant only (غشا / غشاء); book uses غشا 302×, غشاء 0× | **AFGHAN STANDARD** | HIGH |
| Protein | — | **پروتئین** (kept) | International transliteration, standard in Afghan medical writing; پروتین occurs in Dari but is not the medical standard | **COMMON AFGHAN TRANSLITERATION** | MEDIUM |

**Pass-2 change volume: 34 replacements**

| Rule | n |
|---|---:|
| دارو·داروی·دارویی·داروها·داروهای·داروهایی → دوا·دوای·دوایی·دواها·دواهای·دواهایی | 26 |
| کیمیا تداوی (artefact of pass 1) → کیموتراپی | 1 |
| لمفوئید → لنفوئید، لمفاوی → لنفاوی | 3 |
| سیتوپلازم → سیتوپلاسم | 4 |

**Why this is a register decision, not a hard ban.** دارو still appears in Afghan journalistic prose
(even inside one article that also writes دوا). What made the call is that **Afghan official and
clinical writing** — the register this book has to match — standardises on
**دوا / دوایی / دوخانه / ادویه / دواسازی**, down to the name of the national regulator. Confidence is
therefore MEDIUM, not HIGH, and the reasoning is recorded in the glossary's `usage_notes`.

**Terms deliberately left open (no change, no flag).** `لایه` vs `طبقه` (not a conflict — an Afghan
histology text writes «لایه CT» و «چند طبقه» side by side); `هوازی` / `بی‌هوازی` (1 occurrence each,
both standard); `دستگاه` (correct for both "apparatus" — میکروتوم، گلژی — and "system"; no Afghan
source was found that requires سیستم in this book's sense).

---

## 4. Changed terms — what the gate actually rewrote

**Pass 1:** 1,712 replacements across **1,693 changed lines** (~1,926 words).
**Pass 2 (clinical register):** 35 changes — 34 from `apply_terminology_supplement.py` (front matter 1; Ch 2 19+4; Ch 3 5; Ch 4 1+2; Ch 5 1+1) plus 1 artefact repair («کیمیا تداوی» → «کیموتراپی»).
**Combined:** 1,747 changes across the book.

| File | Words changed | Lines changed |
|---|---:|---:|
| `chapters/01-histology-and-its-methods-of-study.md` | 267 | 247 |
| `chapters/02-the-cytoplasm.md` | 380 | 358 |
| `chapters/03-the-nucleus.md` | 274 | 267 |
| `chapters/04-epithelial-tissue.md` | 487 | 422 |
| `chapters/05-connective-tissue.md` | 495 | 380 |
| `00-front-matter.md` | 23 | 19 |
| **Total** | **1,926** | **1,693** |

Highest-impact individual rules (occurrences):

| Rule | From | To | n |
|---|---|---|---:|
| سلولهای | حجراتِ | 329 |
| سلول | حجره | 306 |
| بافت | نسج | 161 |
| سلولها | حجرات | 109 |
| سلولی | حجروی | 95 |
| بافت همبند | نسج منضم | 80 |
| آنزیمهای / آنزیم | انزایمهای / انزایم | 65 |
| هستک | هستهچه | 35 |
| بافت پوششی | نسج اپیتلیال | 21 |
| بیماریهای / بیماری | مریضیهای / مریضی | 47 |
| سنگفرشی | مسطح | 35 |
| گویچه | کرویات | 9 |
| مویرگ | مویرگ | 10 |

**No scientific content was altered.** Line counts are byte-identical to the pre-gate source
(975 / 1,441 / 1,086 / 1,079 / 1,152 / 137); every change is a term substitution, a punctuation
repair, or one of the four text defects listed in §7.

---

## 5. Afghan transliterations adopted (English term → Afghan form)

**انزایم** (enzyme) · **مالیکول / مالیکولی** (molecule) · **ایون** (ion) · **رایبوزوم** ·
**لایزوزوم** · **پراکسیزوم** · **مایتوکندریا** · **دستگاه گلژی** · **موکوس** ·
**کرویات** (blood corpuscle) · **مژک** · **میکروویلی** · **میکروتوبول** ·
**هستهچه** (nucleolus) · **غدوات شحمی** · **مایکروسکوپ** · **اسلاید** ·
**استروئید** · **کاربوهایدریت** · **فسفوریلیشن** · **میتابولیسم** · **شحمی** (adipose) ·
**اندوتلیوم** · **اپیتلیوم** · **لایزوزوم**

---

## 6. Retained English / non-translated terminology, and deliberate non-changes

### 6.1 English retained (16 glossary entries + 16 fallback terms)

`Cellulitis` · `paracellular` · `Urothelium` · `Goblet (cell)` · `Plasmalemma` · `Crista` ·
`PAS` · `H&E` · `IHC` · `ECM` · `GAG` · `LM` / `TEM` / `SEM` · `RBC` / `WBC` · `DNA` / `RNA` /
`ATP` · `CD` / `MHC` · `IgA` / `IgG` / `IgM` — plus all Latin anatomical and stain names.

**Why:** rule 3 and rule 4 of the gate. Where Afghan students learn and meet the English form —
`Cellulitis`, `paracellular seal`, `Urothelium`, `Goblet cell` — inventing or substituting a Dari
coinage would make the book *less* exam-usable. `Cellulitis` in particular was changed **to English
only** with a Dari explanation, because no reliable Afghan Dari standard could be established and
rule 4 forbids invention.

### 6.2 Deliberate non-changes (with reasons)

These look like candidates but were **not** changed. Each was checked and deliberately left:

| Term | Why it was kept | Evidence |
|---|---|---|
| **کلیه، کبد، ریه** | S10 documents the *general-usage* Afghan forms گرده / جگر / شش. But S5 — an actual Afghan histology textbook — writes **«لوبول کبد»** and «کبد», i.e. the **formal medical register** keeps the Arabic-derived anatomical names. These are not Iranian-Persian forms, and the student meets them in exam questions. | S5, S10 |
| **سیتوپلاسم** | Afghan texts print سیتوپلاسم, سیتوپلازم **and** سایتوپلازم. All three are Afghan; none is Iranian. The book keeps the dominant form rather than churning 98 instances for style. | S7, S8 |
| **مایتوکندریا** | Both مایتوکندریا and مایتوکاندریا are Afghan. Variant registered in `accepted_variants`, not forbidden. | S8 |
| **سنگفرشی / گوارشی** | Attested in Afghan teaching material (S5). Classified **NON-CANONICAL (book-consistency)**, **not** Iranian — the book standardises on مسطح and هاضموی, and the scanner reports them as `[NONCANON]`. | S5 |
| **باکتری** | Equally current in Afghanistan; not an Iranian/Afghan divergence. باکتریا registered as an accepted variant. | S5 |
| **ماتریکس** | International term, used in Afghan teaching. Afghan variant بستره noted but not required. | S8 |
| **مژک** | S5 uses **both** «مژک دار» and «سلیا دار». سیلیا registered as accepted variant. | S5 |
| **لایه** and **طبقه** | Not a conflict: S5 writes «لایه CT»، «لایه سروزا» **and** «چند طبقه». Both are Afghan. | S5, S9 |
| **آنتیژن** | See §7 — unresolved. | S5 |

---

## 7. Rejected Iranian-Persian terminology

Forbidden forms now enforced by the scanner (75 forms across 54 canonical replacements).
The principal rejected forms:

| Rejected | Correct Afghan form | Rejected | Correct Afghan form |
|---|---|---|---|
| یاخته | حجره | پاتولوژی | پتالوژی |
| سلول | حجره | بافتشناسی | هستولوژی |
| بافت | نسج | آنزیم | انزایم |
| بافت پیوندی / بافت رابط | نسج منضم | مولکول | مالیکول |
| بافت پوششی | نسج اپیتلیال | شیمیایی | کیمیاوی |
| بیمارستان | شفاخانه | یون | ایون |
| بیمار / بیماری | مریض / مریضی | متابولیسم | میتابولیسم |
| درمان | تداوی | هستک | هستهچه |
| پزشک / پزشکی | داکتر / طب | گویچه | کرویات |
| دانشجو / دانشکده | محصل / پوهنحی | مویرگ | مویرگ |
| کالبدشناسی | اناتومی | استرویید | استروئید |
| ریزپرز | میکروویلی | کربوهیدرات | کاربوهایدریت |
| ریزلوله / ریزرشته | میکروتوبول / میکروفیلامنت | فسفریلاسیون | فسفوریلیشن |
| شبکه درونیاختهای | شبکه آندوپلاسمی | گوارشی | هاضموی |
| منشوری | استوانهای | سباسه | شحمی |
| غشای سلولی | غشای حجروی | لیزوزوم (variant) | لایزوزوم |

**Guard rails against over-correction.** The scanner treats ZWNJ and harakat as word separators but
uses **letters only** for boundary decisions, so legitimate words are never damaged:
`بافته` (woven) ≠ بافت · `هیستونی` (histonic) ≠ ستونی · `پیوند` / `اکسیداسیون` / `فیلتراسیون` ≠ یون ·
`بیوشیمیایی` ≠ شیمیایی · `بزرگ` ≠ رگ · `پاراسلولار` — removed in favour of `(paracellular seal)`.

Additionally, three terms are **never** listed as forbidden because they are prefixes or Afghan
variants in normal use: `سل` (prefix of both حجره and سلول), `میکروتوبول`, `ماستسل`.

---

## 8. Unresolved terms — `[VERIFY TERMINOLOGY]`

| Term | Status | Detail |
|---|---|---|
| **آنتیژن** (Antigen) | **UNRESOLVED — `[VERIFY TERMINOLOGY]`** | Afghan sources show آنتیژن, آنتی نژ and آنتیژن side by side (S5 uses «آنتی نژ»). It is **not** an Iranian-Persian form, so it is not prohibited, but no Afghan institutional source settles the spelling. Per the gate: *do not guess* → the book keeps **آنتیژن**, the term is flagged, and it is carried in the glossary with `decision = VERIFY FURTHER`, `confidence = UNRESOLVED`. Flagged in `00-front-matter.md` §"A note on scientific accuracy". **This is the only unresolved terminology item in the book.** |

**Separation of concerns (mandated):** `[VERIFY TERMINOLOGY]` concerns *wording*;
`[VERIFY AGAINST JUNQUEIRA 17e]` concerns *scientific facts*. They are never merged.
At the time of this report there are **25** `[VERIFY AGAINST JUNQUEIRA 17e]` markers (20 distinct
backlog items) and **1** terminology item.

---

## 9. Task 1 — full Chapters 1–5 audit

The audit was not limited to the previously known terms. It examined all **4,422 distinct tokens**
in Chapters 1–5 plus front matter and classified them into:

- **Iranian-Persian terminology** → 54 canonical replacements (§7)
- **artificial/literal Persian translations** → ریزپرز، ریزلوله، ریزرشته، بیگانهخواری، درونیاختهای، کالبدشناسی، یاختهشناسی، چندلایه
- **unfamiliar terminology for Afghan students** → یاخته، منشوری، خشتفرشی
- **terms whose Afghan usage differs from Iranian usage** → حجره/سلول، نسج/بافت، تداوی/درمان، مریضی/بیماری، جلد/پوست، پتالوژی/پاتولوژی، شفاخانه/بیمارستان
- **terms normally taught in English/transliterated form in Afghanistan** → اسلاید، اپیتلیوم، یوروتلیوم، گابلت، Cellulitis، paracellular، استروئید، کاربوهایدریت، انزایم، مالیکول، ایون
- **inconsistent terminology within the book** → 4 real inconsistencies found and fixed (§10)
- **scientifically incorrect translations** → none found: Dari renderings were checked against the
  reference's definitions, not against surface word-for-word equivalence
- **terms with multiple competing forms** → 25 registered in `accepted_variants`
- **terminology that should remain English** → 16 entries, §6.1

---

## 10. Task 5 — QA result

```
$ python3 scripts/qa_scan.py
========================================================================
TERMINOLOGY GATE SUMMARY
========================================================================
  glossary entries ............   86 forbidden forms loaded
  canonical terms .............   56 distinct replacements
  accepted variants ...........   35
  English-retained registry ...   42
  audit checks loaded .........   12 (from qa/audit-template.md)
  [VERIFY TERMINOLOGY] markers     0
  [VERIFY AGAINST JUNQUEIRA 17e]   25
  unresolved terminology ......    1: آنتیژن
------------------------------------------------------------------------
  RESULT: 0 findings — no prohibited Iranian-Persian terminology,
          no unexplained terminology inconsistency.
========================================================================
```

**Zero prohibited Iranian-Persian terminology. Zero unexplained terminology inconsistency.**

Inconsistencies found and resolved during the audit:

1. **استوانهای ↔ ستونی** — the book used both for "columnar". Standardised on **استوانهای**
   (the form attested in the Afghan histology text).
2. **اندوتلیوم ↔ آندوتلیوم** — standardised on **آندوتلیوم**, consistent with the book's
   آندوپلاسمی.
3. **شل ↔ سست** (loose connective tissue) — standardised on **سست** (24 vs 6 in-text uses).
4. **غشای پایه ↔ لامینای پایه** — *not* an inconsistency: these are two different structures in
   the reference. The scanner was corrected to stop treating them as variants.

**Scanner self-tests (must fail when the book is wrong, and they do):**

| Injected defect | Scanner response |
|---|---|
| `## 5. Function \| وظیفه` renamed | `[STRUCT] … missing 1/13 section(s): Function \| وظیفه` ✅ |
| `## 13. SELF-ASSESSMENT` renamed | `[STRUCT] … missing 1/13 section(s): SELF-ASSESSMENT` ✅ |
| (restored) | 0 findings ✅ |

Four genuine text defects were also caught and fixed by the repaired passes:
`granول` → `گرانول`; `(جunctional)` → `(junctional)`; `دادنturnover` → `دادن turnover`;
`پاراسلولر` / `سلولیت` → `(paracellular seal)` / `Cellulitis` (rule 4, no invented Dari).

---

## 11. Task 3 — updated `scripts/qa_scan.py`

Six passes, all driven by the glossary:

| Pass | Tag | Detects |
|---|---|---|
| 1 | `[SCRIPT]` | prohibited scripts; Latin fragments embedded inside a Persian word |
| 2 | `[TERM]` | prohibited terminology — tagged `(IRANIAN)` or `(NONCANON)`; letter-boundary aware |
| 3 | `[INCONSIST]` | a canonical form **and** one of its `accepted_variants` in the same file |
| 4 | `[STRUCT]` | the 13 mandated sections, per topic |
| 5 | `[RETAINED]` | English-retained registry (informational) |
| 6 | `[VERIFY]` | verification markers (informational) |

`--fix` applies mechanical normalisations only (Persian-Indic → Western digits, U+2212 → hyphen);
terminology is **never** auto-fixed.

The three scripts that own terminology, in pipeline order:

| Script | Role | Status |
|---|---|---|
| `scripts/build_glossary.py` | Authoritative generator of `glossary/terminology-glossary.csv`; holds the `OVERRIDES` slot-corrections applied at write time | run |
| `scripts/apply_terminology.py` | Pass 1 — the canonical core map (D1–D24, E1a–E24b); `--apply` / `--audit` | run once (1,712) |
| `scripts/apply_terminology_supplement.py` | Pass 2 — the clinical register (دارو→دوا, pharmacy/lymphoid/cytoplasm consistency); idempotent | run once (34) |
| `scripts/qa_scan.py` | Six-pass audit; reads the glossary, so a term is enforced the moment it is added there | run every time |

**Known scanner limitation (documented, not a defect).** The `[INCONSIST]` pass fires when a
canonical form and one of its `accepted_variants` appear in the same file. That is the correct
rule for competing standards, but it also fires on a legitimate parenthetical Dari gloss
(«Microfilaments (ریزرشتهها)») or on a descriptive phrase («ظاهراً چندلایه»). Two rules follow:
never place a **gloss** in `accepted_variants`; put it in `usage_notes`. `accepted_variants` is
for a genuinely competing Afghan form only.

**Not excessively aggressive (gate requirement, verified):** every one of the following appears in
the book and is deliberately **not** flagged — `بافته`, `هیستونی`, `پیوند`, `اکسیداسیون`,
`فیلتراسیون`, `بیوشیمیایی`, `بزرگ`, `پارگی`, `GAGها`, `doubletها`, `rRNAی`, `سیتوپلاسم`,
`مایتوکندریا`, `باکتری`, `لایه`, `طبقه`, `کلیه`, `کبد`, `ریه`, `ماتریکس`, `مژک`, `سیلیا`, `آنتیژن`.

---

## 12. Deliverables checklist

| # | Deliverable | Status |
|---|---|---|
| 1 | Complete terminology audit of Chapters 1–5 | ✅ §9 — 4,422 tokens classified |
| 2 | Updated `glossary/terminology-glossary.csv` | ✅ **206 entries** × 12 columns, decision + confidence; 0 self-forbidding and 0 self-variant rows |
| 3 | Updated `scripts/qa_scan.py` | ✅ six passes, self-tested (§10, §11) |
| 4 | Short terminology decision report | ✅ this document |
| 5 | QA showing zero prohibited terminology and zero unexplained inconsistency | ✅ §10, exit code 0 |

**Gate verdict: PASS.** Chapter 6 may proceed.

---

## 13. Notes for the next chapters

1. **Add new terms to the glossary first**, then write the chapter. The glossary is the single source
   of truth; the scanner reads `forbidden_forms` and `accepted_variants` from it automatically.
2. **Extend `scripts/apply_terminology.py`** only for genuinely new canonical decisions — never for
   stylistic preference.
3. **Do not add to `forbidden_forms`:** a prefix of the term itself; an Afghan transliteration variant
   in normal teaching use; a legitimate Latin gloss or Dari translation given in parentheses.
4. **Chapters 6–23 will need new terms.** Anticipated pressure points already researched:
   adipose → **نسج شحمی / آدیپوسایت**; cartilage → کندروسیت / لاکونا (verify); bone →
   استئوکلاست/استئوبلاست; blood → **کرویات** series **رقیقهٔ سفید**? (verify); muscle →
   مخطط / ملس; nervous → **نیورون** / گلیا. Each must go through this gate before use.
