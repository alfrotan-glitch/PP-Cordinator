# Final Terminology Status — post-reconciliation

**Date:** 2026-09-21 · **Status: TERMINOLOGY GATE = FINAL / CLOSED**
Verified against the actual repository, not carried over from earlier reports.

---

## 1. Actual current numbers

All figures below were read from `glossary/terminology-glossary.csv` and re-run this session.

| Measure | Value |
|---|---|
| **Glossary entries** | **228** |
| **AFGHAN STANDARD** | **97** |
| **COMMON AFGHAN TRANSLITERATION** | **110** |
| **ENGLISH RETAINED** | **20** |
| **VERIFY FURTHER** | **1** |
| **Unresolved terminology** | **1 — آنتی‌ژن** |
| **Distinct forbidden forms** | **102** — of which **79 Iranian-Persian** and **23 non-canonical/constructed** |
| Accepted variants | 39 |
| Confidence split | 145 HIGH · 82 MEDIUM · 1 UNRESOLVED |
| `[VERIFY TERMINOLOGY]` markers | 2 (both in the front-matter note describing آنتی‌ژن) |
| `[VERIFY AGAINST JUNQUEIRA 17e]` markers | 39 |

**Scanner:** `python3 scripts/qa_scan.py` → **`RESULT: 0 findings`**, exit 0.
**Self-test:** `python3 scripts/selftest_terminology.py` → **`SELFTEST: ALL PASS`** (all 102 forbidden
forms caught on injection; all 228 canonical forms clean; no form is both canonical and prohibited;
every locked decision asserted).

*Note on one apparent discrepancy:* the scanner's summary line prints `English-retained registry … 45`.
That figure is **20 glossary rows + 25 hardcoded symbols and abbreviations** (GAG, ECM, IHC, LM, TEM,
H&E, DNA, ATP, CD, MHC …) that live in `ENGLISH_RETAINED_FALLBACK`. The glossary-column count of
ENGLISH RETAINED is **20**; both figures are correct and measure different things.

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

**Chapter 6 — Adipose Tissue** was already written and committed under these locked decisions
(`chapters/06-adipose-tissue.md`, 914 lines, 5 topics × 13 sections, 14 verification markers). Its 20
new terms were registered before first use, none was constructed, and no genuinely disputed new term
arose — so the gate is **not** reopened.
