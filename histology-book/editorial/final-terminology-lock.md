# Final Terminology Lock — decisions applied, gate CLOSED

**Status: FINAL AND CLOSED.** Owner's locked decisions of 2026-09-21 applied and verified.
`python3 scripts/qa_scan.py` → **RESULT: 0 findings**, exit 0. `python3 scripts/selftest_terminology.py`
→ **ALL PASS**. Chapter 6 (Adipose Tissue) is unblocked.

Scope of this pass, as instructed: the three junction terms, Carbohydrate, اندامک/ارگانل, the locked
policy, the evidence-discipline rules, and the final verification. **No other terminology decision was
reopened and no scientific content was changed.**

---

## 1. The locked policy (now written into README §4.2)

**Decision hierarchy — take the first level that exists:**

1. Established official Afghan medical terminology (ministry documents, official curricula, textbooks).
2. Established terminology used by Afghan medical universities and medical education.
3. Established Afghan transliteration of international medical terminology.
4. International English terminology, when that is the terminology actually used in medical education.
5. English or the international transliteration retained, when no reliable Afghan equivalent is established.

**Absolute prohibitions:** never invent a medical term · never build a Dari/Persian compound by
translating English word by word · never replace an established international term merely because a Dari
translation is possible.

**Evidence discipline:** no claim of "official Afghan terminology" without an actual examined Afghan
document; a generic label such as "Afghan medical education usage" is not evidence; Iranian sources,
Persian dictionaries and generic Persian websites are not evidence. **But** — added this pass at the
owner's direction — *a term is not automatically prohibited merely because it is also used in Iran*; the
test is whether it is established and appropriate in Afghan medical usage.

---

## 2. Decisions applied

### 2.1 Junction terminology — international forms canonical

| Concept | Canonical (locked) | Status of the Dari form |
|---|---|---|
| Tight junction | **Tight junction / Zonula occludens** | Afghan explanatory form **«مضبوط اتصال»** is attested (wasiweb.com, Kandahar Faculty of Medicine teaching note) and **may be used as a Dari gloss** — it is *not* the scientific term |
| Adherens junction | **Adherens junction / Zonula adherens** | No Afghan Dari equivalent exists → none is invented; the former Dari calque is recorded as **non-canonical** and is machine-enforced as prohibited |
| Gap junction | **Gap junction** | Same — no Afghan Dari equivalent exists → none is invented; the former Dari calque is **non-canonical** and prohibited |

The chapter text needed no change: Chapter 4 already used the international names. Two Dari forms are
now on the enforcement list so they can never return as the scientific term. The permitted Afghan gloss
is deliberately **not** on that list.

### 2.2 Carbohydrate → کاربوهایدریت

Canonical Afghan-Dari term: **کاربوهایدریت** (`Carbohydrate` may follow in parentheses at first use).
`[VERIFY TERMINOLOGY]` removed. The Persian transliteration and «قندها» are not used. Evidence:

> TolAfghan (tolafghan.com/posts/30498), «فزیولوژی حجره», محمدشفیق محمدی —
> «… و سایر لیپیدها ۴ فیصد و **کاربوهایدریت‌ها** ۳ فیصد.»

This is the established Afghan transliteration pattern (cf. کاربن), **not** a morpheme-by-morpheme
construction, and the earlier finding that said otherwise has been withdrawn (§5).

### 2.3 اندامک / ارگانل

**ارگانل** stays canonical — it is the form in the official Afghan MoE Grade-7 biology textbook
(«… به‌نام اعضاچه یا ارگانل (Organelle) حجره یاد شده»). **اندامک is no longer prohibited**: it is
recorded as an **ACCEPTED AFGHAN VARIANT**, with the Afghan document that uses it:

> TolAfghan (tolafghan.com/posts/30498), «فزیولوژی حجره» — «به اجزای درون حجره **اندامک** گفته می‌شود».

Both forms have Afghan usage; the official textbook decides which one the book uses.

---

## 3. What changed in the book

| File | Change |
|---|---|
| `chapters/01…` | 4 Latin *Carbohydrate* phrases → **کاربوهایدریت** (English in parentheses at first use) |
| `chapters/02…` | 5 phrases → **کاربوهایدریت** |
| `chapters/05…` | 2 phrases → **کاربوهایدریت** |
| `00-front-matter.md` | PAS table row → کاربوهایدریت; `[VERIFY TERMINOLOGY]` note rewritten — now **one** term (آنتی‌ژن) |
| `chapters/04…` | terminology note rewritten: the three international junction terms are canonical; «مضبوط اتصال» allowed as a Dari gloss; no invented equivalents |
| `README.md` §4.2 | locked hierarchy, the three absolute prohibitions, locked examples table, and the "used in Iran ≠ prohibited" rule |
| `scripts/build_glossary.py` | carbohydrate row re-anchored to a named Afghan document; artificial blacklist entries removed for the two settled forms; organelle variant registered; junctions re-keyed to the international terms |
| `scripts/qa_scan.py` | per-form Iranian vs non-canonical classification (see §6) |
| `scripts/selftest_terminology.py` | **new** — permanent self-test (injection / clean / locked decisions) |

No scientific content was altered. Verified: `گزارش` counts of Latin *Carbohydrate* in chapter prose are
now 0 except the intended parenthetical first-use.

---

## 4. Final audit — the ten confirmation items

| # | Item | Result | How it was verified |
|---|---|---|---|
| 1 | کاربوهایدریت is canonical | ✅ | glossary row, `COMMON AFGHAN TRANSLITERATION`, HIGH; Persian spelling + misspelling enforced prohibited |
| 2 | کیموتراپی is canonical | ✅ | glossary row; the constructed compound and its variants enforced prohibited |
| 3 | Tight Junction / Zonula Occludens is canonical | ✅ | glossary row (`ENGLISH RETAINED`, HIGH), latin field `Zonula occludens` |
| 4 | Adherens Junction / Zonula Adherens is canonical | ✅ | glossary row (`ENGLISH RETAINED`, HIGH) |
| 5 | Gap Junction is canonical | ✅ | glossary row (`ENGLISH RETAINED`, HIGH) |
| 6 | ارگانل is canonical | ✅ | glossary row `AFGHAN STANDARD`, source = Afghan MoE Grade-7 textbook |
| 7 | اندامک is an accepted Afghan variant, not prohibited | ✅ | `accepted_variants` of ارگانل; self-test asserts it is **not** in any forbidden list |
| 8 | No constructed medical terminology remains | ✅ | 0 occurrences in chapters/front-matter/README; all constructed forms enforced |
| 9 | No unsupported institutional claims remain | ✅ | 0 rows naming an institution without an identifiable document; 0 generic-label rows; 0 empty source fields |
| 10 | No accidental Iranian-only terminology remains | ✅ (one item flagged — see §7) | scanner now classifies per form: **79 Iranian-Persian + 23 non-canonical/constructed** |

**Glossary at the time of this lock:** 228 entries · 102 forbidden forms · 64 canonical
replacements · 39 accepted variants · 45 English-retained · 1 unresolved (آنتی‌ژن) ·
`[VERIFY TERMINOLOGY]` markers: 2 (both in the front-matter explanation, describing that single term).
*(Book-end counts, 23/23 chapters: **691 rows** — **690 after the verification pass**, see `final-terminology-status.md` §7 · 115 forbidden forms · 77 canonical replacements ·
41 accepted variants · 23 English-retained rows · same single unresolved term —
see `editorial/final-terminology-status.md` §1.)*

**Scanner:** `RESULT: 0 findings` — no prohibited terminology, no unexplained inconsistency, all 13
mandated sections present in every topic, all structural checks pass.

**Self-test:** `SELFTEST: ALL PASS` — all 102 forbidden forms detected on injection; all 228 canonical
forms clean; no form is simultaneously canonical and prohibited; the locked decisions all hold.
*(Re-run at book end, and again after the verification pass, against 115 forbidden forms and 690 canonical rows: still **ALL PASS**.)*

---

## 5. Corrections to my own earlier reports

Both are now corrected wherever they appear, and neither was allowed to remain in this final report.

| Earlier claim | Correction |
|---|---|
| «کاربوهایدریت appears in **no** Afghan source» (terminology-correction-report, final-terminology-evidence-gate) | **False.** TolAfghan «فزیولوژی حجره» writes «و سایر لیپیدها ۴ فیصد و کاربوهایدریت‌ها ۳ فیصد». The form is attested and is now canonical. |
| «اندامک is the Iranian form» (same reports) | **Half right.** An Afghan source uses it; it is now an accepted Afghan variant. The canonical choice rests on institutional precedence (official MoE textbook), not on اندامک being non-Afghan. |

A related process lesson is recorded with them: TolAfghan is an Afghan source with a **mixed register**
(the same page mixes حجره/سلول, انزایم/انزیم, مایتوکاندریا/مایتوکندریا). It evidences what an Afghan
author uses; ministry and university documents evidence what Afghan institutions standardise on, and
those keep outranking it.

---

## 6. Defects found by the new self-test, and fixed

1. **One form was both "prohibited" and "acceptable".** The Microfilament entry carried a Dari compound
   in both columns, because an earlier override re-declared acceptable what a later blacklist prohibited.
   The later (corrective) decision stands: it is prohibited, and the contradictory note was removed.
2. **Constructed forms were being reported as "Iranian-Persian".** The scanner labelled a whole entry
   from one keyword, so forms prohibited *because they were constructed* were counted as Iranian
   violations — which is precisely the confusion the owner's rule forbids. The scanner now classifies
   **per form**; the split is 79 Iranian-Persian / 23 non-canonical. No term's status changed.

---

## 7. Flagged for the owner — evidence raised, decision not taken

Per the project rule *flag human-review items rather than resolving them silently*. None of these
blocks the gate.

1. **KUMS uses مریض/شفاخانه/تداوی — and possibly also the Persian patient word.**
   The document I examined (kums.edu.af, «دیپارتمنت فزیوتراپی در شفاخانه تدریسی علی آباد پوهنتون علوم
   طبی کابل…») uses the book's register throughout: «داکتران و استادان»، «مریضان که نیاز دارند»،
   «پوهنځی علوم متمم صحی»، «محصلینی»، «بخش‌های وقایوی و تداوی آن». Search snippets from *other* KUMS
   news items show «بالای **بیمار** ۵۵ ساله…» alongside «**مریض** باشنده ولایت کابل» on a single page.
   **I did not examine those pages**, so under the project's own rule that is *not* evidence and I
   changed nothing. If the owner wants the Persian patient word admitted as an accepted Afghan variant
   (as اندامک now is), that needs its own evidence pass — the book's text uses the Afghan forms.
   This also **closes the "KUMS = 0 entries" gap**: 5 glossary rows now cite KUMS.
2. **پوهنحی vs پوهنځی — two official Afghan sources spell it differently.** The MoHE announcement writes
   «پوهنحی»; the KUMS bulletin writes «پوهنځی». The glossary row declares the MoHE spelling canonical,
   while one chapter of the book currently uses the KUMS spelling once. Recorded, not changed; owner's
   call which spelling is canonical.
3. **Accepted-variant mechanics.** A registered accepted variant may not appear in the same file as its
   canonical form (the scanner's consistency rule). In practice this means the book can *record*
   اندامک as accepted Afghan usage but cannot freely mix it with ارگانل in one chapter. If the owner
   wants both in active use, that rule needs revisiting.

---

## 8. Commands

```bash
python3 scripts/build_glossary.py          # regenerate the glossary (source of truth)
python3 scripts/selftest_terminology.py    # must print SELFTEST: ALL PASS
python3 scripts/qa_scan.py                 # must print RESULT: 0 findings
```

**From Chapter 6 onward:** a genuinely new medical term is checked against this locked policy at the
moment it is introduced — add its row to `build_glossary.py` (with a named Afghan document, or an
explicit statement that none was found), rebuild, and re-run the self-test and the scanner. The full
audit is **not** re-run per chapter unless a genuinely disputed new term appears.
