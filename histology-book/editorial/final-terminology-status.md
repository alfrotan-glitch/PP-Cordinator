# Final Terminology Status — post-reconciliation

**Date:** 2026-09-21 · **Status: TERMINOLOGY GATE = FINAL / CLOSED**
Verified against the actual repository, not carried over from earlier reports.

---

## 1. Actual current numbers

All figures below were read from `glossary/terminology-glossary.csv` and re-run this session.

| Measure | Value (book-end run, 23/23 chapters) |
|---|---|
| **Glossary entries** | **691** |
| **AFGHAN STANDARD** | **292** |
| **COMMON AFGHAN TRANSLITERATION** | **375** |
| **ENGLISH RETAINED** | **23** |
| **VERIFY FURTHER** | **1** |
| **Unresolved terminology** | **1 — آنتی‌ژن** |
| **Distinct forbidden forms (CSV)** | **115** — of which **79 Iranian-Persian** and the rest non-canonical/constructed |
| Accepted variants (distinct) | 41 |
| Confidence split | 145 HIGH · 524 MEDIUM · 21 LOW · 1 UNRESOLVED |
| Rows carrying a Latin term / an abbreviation | 99 / 32 |
| Rows with no source note at all | 0 — every row states its evidence basis or declares that no Afghan document was located |
| `[VERIFY TERMINOLOGY]` markers | 2 (both in the front-matter note describing آنتی‌ژن) |
| `[VERIFY AGAINST JUNQUEIRA 17e]` markers | **415** in the book text — 413 in the 23 chapters + 2 in the front matter (418 including README's 3) |

**Scanner:** `python3 scripts/qa_scan.py` → **`RESULT: 0 findings`**, exit 0 (whole book, Ch 1–23).
**Self-test:** `python3 scripts/selftest_terminology.py` → **`SELFTEST: ALL PASS`** (all 115 forbidden
forms caught on injection; all 691 canonical forms clean; no form is both canonical and prohibited;
every locked decision asserted).

*Note on one apparent discrepancy:* the scanner's summary line prints `English-retained registry … 49`.
That figure is **23 glossary rows + 26 hardcoded symbols and abbreviations** (GAG, ECM, IHC, LM, TEM,
H&E, DNA, ATP, CD, MHC …) that live in `ENGLISH_RETAINED_FALLBACK`. The glossary-column count of
ENGLISH RETAINED is **23**; both figures are correct and measure different things.

---

## 2. Locked decisions — verified in place

| # | Locked decision | Repository state |
|---|---|---|
| 1 | Carbohydrate → **کاربوهایدریت** canonical; no `[VERIFY TERMINOLOGY]`; not کربوهیدرات / قندها | ✅ canonical row HIGH; کربوهیدرات + 4 variants forbidden; no flag; not in the unresolved list; 16 Dari uses in the text |
| 2 | Chemotherapy → **کیموتراپی** canonical; کیمیا تداوی / کیمیا درمانی prohibited | ✅ canonical; all three constructed forms enforced as prohibited |
| 3 | Tight Junction → **Tight junction / Zonula Occludens** canonical; مضبوط اتصال gloss only | ✅ `ENGLISH RETAINED` HIGH; «مضبوط اتصال» **not** prohibited, used once as a gloss in Ch4 |
| 4 | Adherens Junction → **Adherens junction / Zonula Adherens** canonical; no Dari term | ✅ `ENGLISH RETAINED` HIGH; the Dari calque is non-canonical and enforced; nothing invented |
| 5 | Gap Junction → **Gap junction** canonical | ✅ `ENGLISH RETAINED` HIGH; the Dari calque is non-canonical and enforced; nothing invented |
| 6 | Organelle → **ارگانل** canonical; **اندامک = ACCEPTED AFGHAN VARIANT**, never Iranian-only or prohibited | ✅ ارگانل `AFGHAN STANDARD` (MoE Grade-7); اندامک is in `accepted_variants`, and **no row anywhere prohibits it** |

---

## 3. What reconciliation actually changed

The locked decisions were already applied last session. This pass found and fixed **four artifacts
that still contradicted them** — the minimum needed to make the repository self-consistent:

| Artifact | Contradiction found | Fix |
|---|---|---|
| `scripts/apply_terminology_correction.py` | Its `WORD_RULES` still mapped **کاربوهایدریت → کربوهیدرات**. Re-running it would have **silently reintroduced a forbidden form and broken the gate** | The 5 carbohydrate rules removed; a header note records that the mapping is superseded |
| same file | Docstring called اندامک "the Iranian form" and called کاربوهایدریت "INVENTED. No Afghan source uses it" | Both claims corrected in place, with the actual Afghan source quoted for each |
| `editorial/terminology-correction-report.md` | Table rows still read "اندامک → ارگانل — Iranian form corrected" and "کاربوهایدریت → کربوهیدرات — invented compound withdrawn"; scope line said 207 entries | Both rows carry explicit **CORRECTED CLAIM / REVERSED — DO NOT REUSE** notes; counts marked historical |
| `editorial/final-terminology-lock.md`, `final-terminology-evidence-gate.md`, `change-log.md` | Outdated counts (208 / 207 entries) presented as current | Updated to 228, or explicitly marked as the count at that date; the change log now opens with the authoritative current state |

*Historical note:* the "228" those rows were updated to was correct at that date and is itself now
superseded — §1 and §6 carry the book-end figures (691 rows).

**Checked and found already correct:** `build_glossary.py` (no stale claims, no forbidden form in any
blacklist), `qa_scan.py` (no hardcoded stale decision), `selftest_terminology.py`, README §4.2 policy,
`00-front-matter.md`, all six chapters, and all three apply-scripts (verified mechanically: **no rule in
any script maps to a forbidden form**).

**Not done, deliberately:** no other terminology changed, no new term created, no research redone,
no legitimate Afghan variant removed — including اندامک, which also happens to be used in Iran but is
retained as an accepted Afghan variant per decision 6.

---

## 4. Source honesty

No new institutional claim was made in this pass. The one evidence claim re-stated is the
Carbohydrate row, whose source remains the document actually examined:

> TolAfghan (tolafghan.com/posts/30498), «فزیولوژی حجره», محمدشفیق محمدی —
> «… و سایر لیپیدها ۴ فیصد و **کاربوهایدریت‌ها** ۳ فیصد.»

The previously reported claim that no Afghan source uses کاربوهایدریت is withdrawn and no longer
appears as a live statement anywhere in the repository.

---

## 5. Gate result

```
python3 scripts/qa_scan.py              → RESULT: 0 findings     (exit 0)
python3 scripts/selftest_terminology.py → SELFTEST: ALL PASS     (exit 0)
```

The repository matches the locked decisions, and both gates pass.

**TERMINOLOGY GATE = FINAL / CLOSED.**

**Chapter 6 — Adipose Tissue** was written under these locked decisions
(`chapters/06-adipose-tissue.md`, 5 topics × 13 sections, 14 verification markers). Its 20
new terms were registered before first use, none was constructed, and no genuinely disputed new term
arose — so the gate was **not** reopened.

---

## 6. Book-end harmonisation pass (Chapters 7–23)

Chapters 7–23 were added under the closed policy. Each chapter's genuinely new terms were registered
in `scripts/build_glossary.py` **before** first use, the whole-book scanner was run before and after
each insertion, and no chapter reopened a settled decision. Two classes of bookkeeping drift were
found and fixed in this pass — **nothing scientific and nothing in the locked set was touched**:

### 6a. Duplicate English-term rows removed (12)

Because later chapters re-introduced terms already registered earlier, twelve English terms existed
twice. Each pair was reviewed and merged into one row; where the two rows used different Dari forms,
the surviving row records the other form so no reader loses a spelling that appears in the text.

| English term | Rows found | Resolution |
|---|---|---|
| Endothelium | Ch4 + Ch12 | kept Ch4 row («اندوتلیوم», variant «آندوتلیوم») |
| Submucosa | Ch4 + Ch15 | kept «تحت مخاط»; «زیرمخاطی» / «لایهٔ زیرمخاطی» recorded as its variants |
| Plasma cell | Ch5 + Ch13 | kept «پلاسماسل» (variant «پلاسموسیت») |
| Adipocyte | Ch5 + Ch6 | dropped the unused «آدیپوسایت»; the book writes «ادیپوسیت» |
| Chondroitin sulfate | Ch5 + Ch7 | kept the Ch5 row; sulfate spelling normalised in the text |
| Keratan sulfate | Ch5 + Ch7 | kept the Ch5 row; sulfate spelling normalised in the text |
| Fibrin | Ch5 + Ch9 | identical rows; kept Ch5 |
| Capillary | Ch1 + Ch12 | kept «موی‌رگ» as the single primary form |
| Insulin | Ch6 + Ch16 | identical rows; kept Ch6 |
| Bone marrow | Ch5/8 + Ch13 | kept «مغز استخوان»; the kasre spelling normalised in the text |
| Lymphocyte | Ch9 + Ch13 | kept «لنفوسیت»; «لیمفوسیت» recorded as its variant and the text unified |
| Leukemia | Ch9 + Ch13 | identical rows; kept Ch9 |

Result: **0 duplicate English-term rows remain** (checked with `Counter(english_term)`).

*One deliberate asymmetry, recorded so it is not mistaken for drift:* the surviving Submucosa row keeps
the label «تحت مخاط» (the form the gate registered) and carries «زیرمخاطی» / «لایهٔ زیرمخاطی» as recorded
variants; the three chapters that discuss the layer (Ch14, Ch15, Ch17) use the variant form «زیرمخاطی»
consistently, and no chapter mixes the two. Changing the chapters to the label form would have meant
touching audited clinical text for no reader benefit, so the registry was left to hold both.

### 6b. Variant spellings harmonised across chapters (4)

| Drift | Chapters affected | Direction of the fix |
|---|---|---|
| «مغزِ استخوان» vs «مغز استخوان» | Ch8, Ch12, Ch13, Ch18 | unified on «مغز استخوان» (27 edits) |
| «سلفات» vs «سولفات» | Ch7, Ch9 | unified on the «سولفات» spelling used by the register (10 edits) |
| «پلاسموسیت» vs «پلاسماسل» | Ch13, Ch14, Ch15 | unified on «پلاسماسل» (24 edits) |
| «لیمفوسیت» vs «لنفوسیت» | Ch13 | unified on «لنفوسیت» (43 edits) plus one garbled line repaired |

Two further repairs in the same pass: the Ch12 terminology note was rewritten so it no longer quotes
a form the glossary has retired, and a corrupted line in Ch13 («لنفوسیت‌آهن‌دانه») was rewritten as the
question it was meant to be. The whole-book scanner returned **0 findings** after the pass, and the
self-test returned **ALL PASS**.

### 6b-bis. Count reconciliations (book end)

| Item | What was wrong | Resolution |
|---|---|---|
| Ch23 terminology note | said the chapter registered «۳۵ ردیف» while the CH23 block actually registered **36** rows (667 → 703) | note corrected to «۳۶ ردیف»; the earlier commit message for Ch23 («35 new terms») is kept as a dated record and is documented here rather than rewritten |
| Ch13 self-assessment line | read «لیمفوسیت‌آهن‌دانه (لنفوسیت)» — a corrupted compound that the scanner could not see | line rewritten as the question it was meant to be («لنفوسیت‌ها از راهِ کدام ورید وارد عقدە می‌شوند؟»); the same pass unified the chapter on «لنفوسیت» |
| Marker counts | earlier reports quoted 20 / 25 / 39 markers from the Ch 1–5 era | book-end figures verified by machine: **413** markers in the 23 chapters, **415** in the book text (2 more in the front matter), 418 including README; **207** of them are written up as backlog items |
| Legacy «سلول» hits | 7 occurrences remain in the book | all inside registered Latin-derived compounds — «هپاتوسلولار» (Ch16) and «پُرسلول» (Ch21, Ch23) — never as the prohibited standalone form |

### 6c. New LOW-confidence transliterations (Ch 19–23)

Twenty-one glossary rows are labelled `LOW`, all of them international terms rendered as
transliterations where no Afghan document was located during this run — e.g. لوله‌های منیفروس،
واز دفرنس، وسیکولِ سیمینال (Ch21); سکلرا، کوروئید، یوویا، هیومورِ آکوئوس، فووآ سنترالیس (Ch23).
They are **not** claimed as settled Afghan terminology; they are flagged here so a human reviewer can
confirm or replace them. No compound was invented to fill any of these slots.
