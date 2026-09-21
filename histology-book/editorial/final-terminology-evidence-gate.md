# Final Terminology Evidence Gate — Report

> **SUPERSEDED IN PART — see `editorial/final-terminology-lock.md`.** Three of this report's conclusions were revised by the owner and by later evidence:
> (1) the junction terms are settled as international, per the targeted check in
> `editorial/junction-terminology-check.md`; (2) **Carbohydrate is canonical as کاربوهایدریت** —
> the claim that no Afghan source uses that form was wrong (TolAfghan, «فزیولوژی حجره»);
> (3) **اندامک is an accepted Afghan variant**, not a prohibited form, and (4) the KUMS evidence
> gap is closed — 5 entries now cite a KUMS document.

**Gate:** the mandatory check before Chapter 6.
**Policy locked:** `README.md` §4.2 (canonical rule, source hierarchy, no-construction rule, no-overclaim rule).
**Result: PASS — scanner 0 findings, exit 0.**
**Glossary: 208 entries.**

---

## 0. Policy as locked

> **Use the established medical terminology actually used in Afghanistan.**
> **If an established Afghan Dari term exists, use it.**
> **If Afghan medical education uses an English-derived/transliterated term, retain that established
> form.**
> **If no reliable Afghan terminology can be established, DO NOT invent a translation. Retain the
> English term or the established international transliteration and mark it `[VERIFY TERMINOLOGY]`
> where appropriate.**

Source hierarchy now enforced: **MoPH → MoHE → KUMS → official Afghan curricula and textbooks →
other recognised Afghan medical universities → other credible Afghan medical educational sources.**
Iranian sources, generic Persian dictionaries and general Persian websites are explicitly **not**
evidence. `README.md` §4.2 also states the no-construction rule, the no-overclaim rule, and the rule
that a generic label such as *"Afghan medical education usage"* must never appear in `source_authority`.

**This gate made no stylistic rewrite.** Three changes were made, all of them corrections:
`Carbohydrate` → English-retained; 31 overclaimed source labels replaced with real ones or an honest
declaration; two self-triggering README examples removed.

---

## 1. Terms with direct Afghan institutional evidence — **54 entries**

Every one of these names an actual document that was fetched and read, with the quoted text.

| Source document | Entries anchored |
|---|---:|
| **Afghan MoE textbook, Biology Grade 7** (moe.gov.af, Kabul 1398) | 21 |
| **Afghan MoPH official recruitment register** (moph.gov.af) | 9 |
| **Afghan faculty histology text** — خاتم النبیین University, «هستولوژی تئوری ۲» (muslimuniversity.edu.af) | 9 |
| **TolAfghan** (tolafghan.com), «فزیولوژی حجره» | 9 |
| Afghan medical-curriculum course lists (kateb.edu.af) | 3 |
| Afghan MoHE Biology curriculum (logu.edu.af) | 2 |
| **Afghan doctors' clinical writing** (afghan-doctors.com) | 2 |
| Afghan hospital clinical text (mehrabanhospital.af) | 2 |
| **Afghan MoHE** academic-post announcement (mohe.gov.af) | 1 |
| AfghanVet biology text (afghanvet.blogspot.com) | 1 |
| **Afghan national medicines regulator** (dpmea.gov.af) | 1 |
| Afghan clinical directory entry (Kabul infectious-disease practice) | 1 |

Representative anchored terms: حجره · حجرات · حجروی · نسج · انساج · مایکروسکوپ · ارگانل ·
سایتوپلازم · غشای حجروی · مایتوکندریا · انزایم · کیمیاوی · میتابولیسم · فسفوریلیشن · پروتئین ·
شبکه آندوپلاسمی · استوانهای · نیورون · جلد · غدوات · مویرگ · مریض · امراض · داکتر · وقایه ·
پتالوژی · هستولوژی · سایتولوژی · هستوپتالوژی · مالیکولی · دوا · کلیه · کبد · تداوی · کیموتراپی.

---

## 2. Established Afghan transliterations — **149 entries, confidence MEDIUM**

Direct English-derived transliterations that must not be replaced by a Dari translation. Each is
labelled in `source_authority` as *"Established English-derived transliteration retained as the term
Afghan readers recognise; no Afghanistan-specific documentary source located in this audit."*

Examples: هپارین · هیستامین · ترپتاز · دسموزوم · همیدسموزوم · گرانول · ایسکمی · نکروز · آپوپتوز ·
کندرویتین سولفات · کراتان سولفات · درماتان سولفات · رایبوزوم · لایزوزوم · پراکسیزوم · گابلت ·
ماستسل · پلاسماسل · آدیپوسایت · میواپیتلیال · کارسینوم درجا · تولوئیدینبلو · لامینا پروپریا ·
اپیژنتیک.

**None of these is a constructed compound.** They are phonetic borrowings, and the policy's rule for
them is precisely "retain the established form". They are MEDIUM confidence rather than HIGH because
no Afghanistan-specific document was located — that is stated, not hidden.

---

## 3. English-retained terms — **16 entries**

`Cellulitis` · `paracellular (seal)` · `Urothelium` · `Goblet (cell)` · `Plasmalemma` · `Crista` ·
**`Carbohydrate`** · `PAS` · `H&E` · `IHC` · `ECM` · `GAG` · `LM`/`TEM`/`SEM` · `RBC`/`WBC` ·
`DNA`/`RNA`/`ATP` — plus every Latin anatomical and stain name.

**`Carbohydrate` (new in this gate).** Previously the book used an invented form, then a standard
transliteration. Neither could be anchored to an Afghan medical source. Per the policy it is now
**retained in English** and flagged:

| | |
|---|---|
| Book text | `Carbohydrate` (12 occurrences; the invented form and the transliteration are both forbidden) |
| Glossary | dari_term `Carbohydrate`, decision **ENGLISH RETAINED**, confidence **UNRESOLVED** |
| Status | `[VERIFY TERMINOLOGY]`, listed as unresolved |

**`قندها` was NOT adopted as the canonical term.** Afghan MoE biology books write «قندها» for *sugars*
— a general biological expression, not a medical terminology standard for *Carbohydrate*. It is
recorded in `usage_notes` as a related-but-different concept.

---

## 4. Unresolved terms — **2**

| Term | Form in book | Why unresolved |
|---|---|---|
| **آنتیژن** | آنتیژن | Afghan sources show آنتیژن / آنتی نژ / آنتینژن side by side; no institution settles the spelling. Not an Iranian form, so not prohibited |
| **Carbohydrate** | `Carbohydrate` | No Afghan medical source using any Dari form could be identified. English retained |

Both carry `[VERIFY TERMINOLOGY]`. The scanner now reports unresolved terms by **confidence**, not only
by decision, so an English-retained term that is unverified stays visible in the summary.

The scientific-verification marker remains separate: **25** `[VERIFY AGAINST JUNQUEIRA 17e]` markers
(20 distinct backlog items).

---

## 5. Constructed terms still present — **0 of the prohibited kind; 30 compositional forms reported for your decision**

**No morpheme-by-morpheme invention remains.** The blacklist is enforced and self-tested.

However, honest reporting requires a second list: **30 multi-word Dari forms in the glossary are
compositional** — built from attested elements rather than being independently attested as units. They
are *not* the chemotherapy/carbohydrate failure mode (no invented root, no semantic calque of an
English compound word), but they are also not each backed by their own Afghan citation. You asked to
see them, so here they are in full:

| Category | Terms |
|---|---|
| **Derived from an attested root** (حجروی ← ME7, اپیتلیوم ← S5) | بینحجروی · خارجحجروی · درونحجروی · نسج اپیتلیال · شبه مطبق · میواپیتلیال |
| **Built on an attested head noun** (نسج ← ME7; غدوات ← ME12; دستگاه ← ME7) | نسج منضم سست · نسج منضم متراکم · نسج گرانولاسیون · غدوات شحمی · دستگاه گلژی · مادهٔ زمینهای · رشتهٔ رتیکولار · رشتهٔ الاستیک · تحت مخاط |
| **Calques of English junction/structural names** — the closest thing to the prohibited pattern on this list | اتصال مضبوط · اتصال چسبنده · اتصال شکافی |
| **Standard international or laboratory forms, transliterated** | تولوئیدینبلو · لامینا پروپریا · همیدسموزوم · اپیکنیک→اپیژنتیک · کارسینوم درجا · ماستسل · پلاسماسل · کندرویتین سولفات · کراتان سولفات · درماتان سولفات · آنتیژن · لامینای پایه · غشای پایه · غشای هستوی · منفذ هستوی · فیلامنت میانی · رگ زایی |

**My recommendation, for your decision — not applied:** the three junction names are the only entries
I would actively reconsider. Histology exams test them as *tight junction / zonula occludens*,
*adherens junction / zonula adherens* and *gap junction / nexus*, and the international names are what
an Afghan student meets. If you agree, the fix is to make the English/international form canonical
with the Dari as parenthetical explanation — **the reverse of a translation**. I have deliberately
**not** made that change, because it is a judgment call about exam familiarity, not something the
sources settle, and it would be a broad text change.

---

## 6. Iranian-specific terminology still present — **0 occurrences**

A candidate list of 33 Iranian-Persian forms was tested against the full text, including the ones this
project has already had to fix (یاخته · سلول · بافت · اندامک · نورون · میتوکندری · هستک · گویچه ·
مویرگ · سباسه · گوارشی · پاتولوژی · آنزیم · مولکول · یون · شیمیایی · کاربوهایدریت · ریزپرز · منشوری ·
لمفوئید …).

**Result: zero occurrences**, with one documented exception:

| Form | Count | Status |
|---|---:|---|
| چندلایه | 1 | **Deliberately permitted.** It appears once in Chapter 4 as a parenthetical Dari *gloss* of شبه مطبق. It is attested Afghan descriptive usage (the Afghan histology text writes «چند طبقه»), and it is a gloss, not a competing standard. Forbidding it would make the scanner flag legitimate explanatory Dari |

Also verified: **no Iranian source, Persian dictionary or general Persian website is cited anywhere in
`source_authority`.** Two earlier citations to Iranian-platform material were removed in this gate.

---

## 7. Source-coverage honesty

| | |
|---|---|
| Entries naming an Afghan institution/source | 57 |
| …of those, **failing to identify an actual document** | **0** |
| Generic labels such as *"Afghan medical education usage"* remaining | **0** |
| Entries declaring an owner-mandated decision (explicitly *not* an evidence claim) | 4 |
| Iranian or generic-Persian sources cited as evidence | **0** |

**A gap I will not paper over: KUMS anchors 0 entries.** The directive ranks Kabul University of
Medical Sciences third, but KUMS histology syllabi and lecture material are not published as
retrievable full text, so **no KUMS-sourced terminology claim is made anywhere in the glossary.**
Where a Kabul medical-faculty source was reachable (the MoHE announcement about پوهنحی طب, and the
course lists), it is cited as such. KUMS-specific vocabulary — lamina, desmosome, glycocalyx and
similar — remains unverified at that tier and is carried at MEDIUM confidence.

---

## 8. Final scanner result and glossary count

```
$ python3 scripts/qa_scan.py
========================================================================
TERMINOLOGY GATE SUMMARY
========================================================================
  glossary entries ............  106 forbidden forms loaded
  canonical terms .............   60 distinct replacements
  accepted variants ...........   35
  English-retained registry ...   41
  audit checks loaded .........   12 (from qa/audit-template.md)
  [VERIFY TERMINOLOGY] markers     2
  [VERIFY AGAINST JUNQUEIRA 17e]   25
  unresolved terminology ......    2: آنتی‌ژن, Carbohydrate
------------------------------------------------------------------------
  RESULT: 0 findings — no prohibited Iranian-Persian terminology,
          no unexplained terminology inconsistency.
========================================================================
```

| | |
|---|---|
| **Final glossary count** | **208 entries** (12 columns) |
| Decisions | 94 AFGHAN STANDARD · 97 COMMON AFGHAN TRANSLITERATION · 16 ENGLISH RETAINED · 1 VERIFY FURTHER |
| Confidence | 143 HIGH · 63 MEDIUM · 2 UNRESOLVED |
| Forbidden forms enforced | 106 |
| Scanner | **0 findings**, exit 0 |
| Scientific content changed | **none** — line counts unchanged (146 / 975 / 1441 / 1086 / 1079 / 1152) |

**GATE STATUS: PASSED.** All eight requested items are reported above, including the two categories
you asked about specifically (constructed terms, Iranian terminology). Chapter 6 may proceed once you
accept this pass and decide on the three junction names in §5.
