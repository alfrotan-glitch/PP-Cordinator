# Terminology Correction Report — Pass 3

> **SUPERSEDED IN PART — see `editorial/final-terminology-lock.md`.** The finding in §1 that the Afghan transliteration of *Carbohydrate* was a morpheme-by-morpheme
> construction **is withdrawn**: the form is attested in TolAfghan, «فزیولوژی حجره»
> («… و سایر لیپیدها ۴ فیصد و کاربوهایدریت‌ها ۳ فیصد») and is now the canonical Afghan-Dari
> term. The same report's treatment of اندامک as an Iranian form is likewise revised — it is an
> accepted Afghan variant, and ارگانل is canonical on institutional precedence.

**Trigger:** corrective directive — *"NEVER invent, construct, or literal-translate a medical/scientific
term from English."*
**Scope (as of that pass):** 207 glossary entries + the completed chapters + front matter + README.
The glossary reached **228 entries** at that gate and **691 rows** by book end (23/23 chapters); these
counts are historical and are superseded by `editorial/final-terminology-status.md` §1 and §6.
**Verdict:** the directive identified a real methodology error. **4 term families were wrong; 77 in-text
corrections made; 1 invented compound withdrawn entirely.** No new Dari term was introduced to replace
any of them — every correction moves *toward* established Afghan usage, not away from it.

---

## 0. What the previous pass got wrong

The pass-1/2 rule set was valid for terms whose Afghan form had actually been **observed**. It was
silently invalid for terms derived by **translating English morphemes**. Nothing in the pipeline
distinguished the two, so one constructed compound survived as a "canonical Afghan term" and two
Iranian forms were never noticed at all.

| Failure mode | Example | Detectable by linguistics? |
|---|---|---|
| Morpheme-by-morpheme construction | کاربوهایدریت ← carbo- + hydrate | **No** — it reads as perfect Dari |
| Iranian form mistaken for neutral | اندامک، نورون | **No** — both are current in Iranian writing |
| Constructed by a *rule* applied to a compound | کیمیا تداوی ← کیمیا + تداوی (from شیمی‌درمانی) | **No** — it is an artefact of a correct rule |

All four were found only by **auditing the text against named Afghan documents**. That is now the
pipeline's first step, not its last.

---

## 1. Terms corrected because they were invented / constructed

| English | Previous book term | Status | Corrected to | Evidence | Decision | Confidence |
|---|---|---|---|---|---|---|
| Chemotherapy | **کیمیا تداوی / کیمیا‌تداوی** | ❌ **INVENTED** — produced by applying the correct شیمی→کیمیا rule to the compound شیمی‌درمانی | **کیموتراپی** | Afghan doctors' clinical writing: «شیوه‌های مختلف تداوی … تداوی دوایی، تداوی اشعوی، **کیموتراپی** و جراحی» | COMMON AFGHAN TRANSLITERATION | HIGH |
| Carbohydrate | **کاربوهایدریت** | ❌ **INVENTED** — transliterated morpheme by morpheme; **zero Afghan sources** | **کربوهیدرات** (established transliteration, restored) | No Afghan source located for either spelling. Afghan MoE textbooks write «قندها» / «پولی‌میری های طبیعی، قندها، پروتین ها» rather than one term for "carbohydrate" | **VERIFY FURTHER** | UNRESOLVED |

**77 in-text corrections** in total:

| Correction | n | Type |
|---|---:|---|
| اندامک → **ارگانل** | 36 | **CORRECTED CLAIM:** not an Iranian-only form. ارگانل became canonical because the official Afghan MoE Grade-7 textbook uses it; اندامک is an ACCEPTED AFGHAN VARIANT (TolAfghan, «فزیولوژی حجره») and is not prohibited |
| نورون → **نیورون** | 21 | Iranian form corrected |
| کاربوهایدریت → **کربوهیدرات** | 11 | **REVERSED — DO NOT REUSE.** This correction was wrong. کاربوهایدریت is attested in an Afghan source (TolAfghan, «فزیولوژی حجره») and is now the CANONICAL term; کربوهیدرات is a FORBIDDEN form. The book has been changed back |
| میتوکندریایی → **مایتوکندریایی** | 8 | third spelling unified |
| کیمیا تداوی → **کیموتراپی** | 1 | constructed compound removed (pass 2) |

**No invented term was substituted for any other term.** کیمیا تداوی needed *no* Dari replacement — it
needed the established transliteration کیموتراپی. کاربوهایدریت needed no replacement either — the
standard transliteration was restored and the term flagged as unresolved.

**Permanent defence.** All of these are now in `forbidden_forms`, and the scanner was self-tested by
re-injecting each one:

| Injected form | Scanner | Injected form | Scanner |
|---|---|---|---|
| اندامک | ✅ CAUGHT | کاربوهایدریت | ✅ CAUGHT |
| نورون | ✅ CAUGHT | کیمیا تداوی | ✅ CAUGHT |
| میتوکندریایی | ✅ CAUGHT | شیمی‌درمانی | ✅ CAUGHT |
| ریزرشته | ✅ CAUGHT | منشوری | ✅ CAUGHT |
| سلول | ✅ CAUGHT | بافت | ✅ CAUGHT |
| **چندلایه** | ✅ correctly **NOT** flagged — legitimate parenthetical Dari gloss | | |

---

## 2. Terms retained as English / transliteration

Retained because Afghan sources use the English-derived or English form — **not** because a Dari
translation was unavailable.

**English retained (17 glossary entries):** `Cellulitis` · `paracellular (seal)` · `Urothelium` ·
`Goblet (cell)` · `Plasmalemma` · `Crista` · `PAS` · `H&E` · `IHC` · `ECM` · `GAG` ·
`LM`/`TEM`/`SEM` · `RBC`/`WBC` · `DNA`/`RNA`/`ATP` — plus every Latin anatomical and stain name.

**Established transliterations retained:** کیموتراپی · هستولوژی · سایتولوژی · پتالوژی ·
هستوپتالوژی · مایکروسکوپ · انزایم · مالیکول · ایون · رایبوزوم · لایزوزوم · پراکسیزوم ·
مایتوکندریا · فسفوریلیشن · میتابولیسم · استروئید · آپوپتوز · نکروز · ایسکمی · گرانول ·
دسموزوم · هیستامین · هپارین · ترپتاز · کندرویتین سولفات · آرگانل → ارگانل · نیورون ·
سایتوپلازم.

**Deliberate non-changes (verified, not merely possible).** These were checked and left alone
*because they are established Afghan usage*:

| Term | Evidence that it is correct |
|---|---|
| **پروتئین** | TolAfghan: «دو نوع **پروتئین** کروی مشابه … تشکیل شده‌اند». (Afghan MoE school books use the simplified spelling پروتین; both are Afghan — پروتین recorded as an accepted variant.) |
| **سیتوپلاسم** | AfghanVet and TolAfghan use it; MoE uses سایتوپلازم. All three are Afghan. |
| **جلد، موی‌رگ، غدوات، استوانه‌ای، اسکلیتی، پیوند، ترشح** | Confirmed verbatim in the official MoE Grade-12 textbook |
| **کلیه، کبد، ریه، پانکراس** | Afghan MoPH writes «امراض **کلیه**، از جمله عدم کفایه کلیه (**گرده**)»; Afghan hospitals write «امراض **کبدی یا جگر**» and «تومورهای **ریه**» |
| **لایه / طبقه** | Not a conflict — an Afghan histology text writes «لایه CT» and «چند طبقه» side by side |
| **باکتری** | MoE writes بکتریا; both are Afghan — registered as variants |
| **اسلاید** | MoE school labs say سالید; اسلاید is the established medical/laboratory form |

---

## 3. Terms supported by the Afghan Ministry of Public Health (MoPH)

| Term | Evidence |
|---|---|
| **پتالوژی** | MoPH job register: «شف دیپارتمنت پتالوژی ولابراتوار» |
| **هستولوژی / هستوپتالوژی / سایتولوژی** | «پتالوژی اناتومیک (**هستولوژی**/ **هستوپتالوژی**، **سایتولوژی**)» |
| **مالیکولی** | Same register; MoHE book title «معافیت حجروی و **مالیکولی**» |
| **حجروی** | Same register |
| **مریضی / مریض / تداوی / لابراتوار / شفاخانه** | «مریض محور»، «تشخیص و مدیریت امراض … تداوی»، «لابراتوار» |
| **دوا / دوایی / دواخانه / ادویه** | «خدمات به شمول **دوا** غذا رایگان است»; the national regulator is «اداره ملی **ادویه** و غذا» (dpmea.gov.af) |
| **کلیه** | «امراض کلیه، از جمله عدم کفایه کلیه (گرده)» |
| **کاربن** (in کاربن دای اکساید) | MoE Grade-7: «مواد اضافی چون **کاربن دای اکساید** را … خارج میسازد» |

**MoPH-anchored entries: 10**

---

## 4. Terms supported by the Afghan Ministry of Higher Education (MoHE), the Ministry of Education
curriculum, and Afghan medical faculties

**MoHE (higher education):**

| Term | Evidence |
|---|---|
| **هستوپتالوژی** | «بست **هستوپتالوژی** پوهنحی طب» |
| **حجروی / مالیکولی** | Official book title «معافیت **حجروی** و **مالیکولی**» (Kabul 1400) |
| **کیمیاوی، انساج، حجرات، اپیتیلیوم، اناتومی، پوهنتون، دیپارتمنت** | MoHE Biology curriculum (logu.edu.af) |

**Ministry of Education official textbooks — the single best source for the cell/tissue layer:**

| Term | Evidence (verbatim) |
|---|---|
| **حجره / حجرات / حجروی / حجروی (unicellular)** | «حجره را کوچکترین واحد ساختمانی و وظیفوی تعریف کرد»؛ «انواع مختلف حجرات»؛ «غشای **حجروی**»؛ «موجودات زندۀ یک **حجروی** (Unicellular)» |
| **انساج** | «سطوح تنظیم در موجودات زنده، **انساج**، انساج نباتی» |
| **مایکروسکوپ** | ch.1 title «**مایکروسکوپ** و انواع آن»؛ «مایکروسکوپ مرکب نوری» |
| **ارگانل** | «ساختمان‌های کوچکی … به‌نام اعضاچه یا **ارگانل** (Organelle) حجره یاد شده» |
| **سایتوپلازم / غشای پلاسمایی** | «سایتوپالزم درخارج هسته قرار دارد»؛ «غشای حجروی: به‌نام **غشای پالزمایی** هم یاد میشود» |
| **میتوکاندریا · واکیول · کروماتین · کروموزوم · پالستید · سنتریول · دیوار حجروی** | Same chapter, organelle section |
| **استوانه‌ای** | «بیضوی، مدور، مکعبی، **استوانه یی** و تعدادی هم مسطح»; «حجرات مخروطی و **استوانه یی**» |
| **نیورون** | Grade 12: «**نیورون** دوم سیناپسی را بیشتر تحریک کنند»؛ «**نیورون** هاي حرکي را تخریب ميکند» |
| **جلد · غدوات · موی رگ · کیمیاوی · نیورون · واکسین · وقایه · عضلات · پرده** | Grade 12 science text |
| **بکتریا** | Grade 7: «مانند: **بکتریا**ها، آمیب و غیره» |

**Afghan medical-faculty material (خاتم النبیین University histology text):** نسج منضم · موی رگ ·
هسته چه · انزایم · استوانه‌یی · مکعبی · کرویات سفید خون · لوبول کبد · مژک/سلیا · عروق خونی.

**MoHE/MoE/faculty-anchored entries: 24**

---

## 5. Terms supported by KUMS / پوهنتون علوم طبی کابل

**Honest assessment: this is the weakest evidence tier in the audit, and one specific action is owed.**

| Term | What the KUMS / Kabul medical source shows |
|---|---|
| **پتالوژی** | kums.edu.af: «دیپارتمنت **پتالوژی**»، «لابراتوار **پتالوژی**» |
| **هستولوژی · هستوپتالوژی** | MoHE announcement on the medical faculty: «بست **هستوپتالوژی** پوهنحی طب» |
| **اناتومی · فزیولوژی · داخله · صحت عامه · طب معالجوی** | Afghan medical-curriculum course names (kateb.edu.af / asas.edu.af) |
| **لابراتوار** | «لابراتوار **هستومالوژی**/پتالوژی» (asas.edu.af, anis.af) |
| **حجروی** | «معاینات **حجروی**، هستوپتالوژی، باکتریولوژی، پرازیتولوژی» |

**Not achievable in this pass:** KUMS course syllabi and lecture handouts are not published as
retrievable full text, so the deeper histology vocabulary (e.g. the exact KUMS words for *lamina*,
*desmosome*, *glycocalyx*) could **not** be verified against KUMS. I have recorded that as a gap
rather than filling it with an inference.

> **Owed action:** obtain KUMS / پوهنتون علوم طبی کابل histology syllabus or lecture material and
> re-check the 139 entries that are currently marked "no Afghanistan-specific documentary source
> located". Until that is done those entries are labelled honestly as transliterations, not asserted
> as Afghan standards.

**KUMS-anchored entries: 6 (course-level terminology only)**

---

## 6. Terms requiring further verification

| Term | Form in book | Why unresolved | Label |
|---|---|---|---|
| **آنتی‌ژن** | آنتی‌ژن | Afghan sources show آنتی‌ژن, آنتی نژ, آنتی‌نژن side by side (the Afghan histology text writes «آنتی نژ»). Not an Iranian form, so not prohibited — but no Afghan institution settles the spelling | `[VERIFY TERMINOLOGY]`, decision VERIFY FURTHER |
| **کربوهیدرات** | کربوهیدرات | The invented form was withdrawn, but **neither** spelling could be anchored to an Afghan document. Afghan textbooks write «قندها» instead of a single term | `[VERIFY TERMINOLOGY]`, decision VERIFY FURTHER |

**Terminology-sourced vs science-sourced uncertainty is kept separate.** `[VERIFY TERMINOLOGY]` = wording;
`[VERIFY AGAINST JUNQUEIRA 17e]` = scientific facts. Current counts: **2** and **25**.

**139 glossary entries are marked:** *"Established English-derived transliteration retained as the term
Afghan readers recognise; no Afghanistan-specific documentary source located in this audit."* These are
direct transliterations (هپارین، هیستامین، دسموسوم، گرانول، ایسکمی …) — **none is a constructed
compound**, so none violates the directive. They are labelled MEDIUM confidence rather than HIGH, which
is the honest position.

---

## 7. Final scanner result

```
$ python3 scripts/qa_scan.py
========================================================================
TERMINOLOGY GATE SUMMARY
========================================================================
  glossary entries ............   93 forbidden forms loaded
  canonical terms .............   60 distinct replacements
  accepted variants ...........   36
  English-retained registry ...   42
  audit checks loaded .........   12 (from qa/audit-template.md)
  [VERIFY TERMINOLOGY] markers     2
  [VERIFY AGAINST JUNQUEIRA 17e]   25
  unresolved terminology ......    2: آنتی‌ژن, کربوهیدرات
------------------------------------------------------------------------
  RESULT: 0 findings — no prohibited Iranian-Persian terminology,
          no unexplained terminology inconsistency.
========================================================================
```

Exit code **0**. 207 glossary entries written at that time (228 today). Zero occurrences of اندامک، نورون،
کیمیا تداوی، میتوکندریایی or any constructed compound anywhere in the book.

---

## 8. What changed in the process, not just in the text

The directive's core point is methodological, so the pipeline changed accordingly:

| Before | Now |
|---|---|
| A term was added because it *sounded* Afghan | A term is added only with a **named Afghan document** in `source_authority`, quoted verbatim |
| A generic label ("Afghan medical education usage") counted as evidence | 139 entries carrying that label were re-labelled honestly; **42 entries now name an actual document** |
| Forbidden lists grew by linguistic judgement | An explicit **INVENTED_CONSTRUCTIONS** blacklist, self-tested by re-injection |
| Scanner could not detect a constructed compound | Scanner now catches all of them (11/11 self-tests) |

**Standing rule for Chapters 6–23, recorded in `README.md` §4.2:**

> Established Afghan medical usage first. Established English/transliterated medical terminology second.
> **Invented translation is never acceptable.** If no reliable Afghan term can be established, keep the
> English term or the established transliteration and add a short Dari explanation — do not build one.

**Chapter 6 remains held** until this correction is accepted.

---

## 9. Sources added in this pass

| Ref | Source | What it settled |
|---|---|---|
| **ME7** | Afghan MoE, **Biology Grade 7**, Kabul 1398 (moe.gov.af) | حجره، حجرات، حجروی، انساج، مایکروسکوپ، **ارگانل**، سایتوپلازم، غشای حجروی/پلاسمایی، میتوکاندریا، مکعبی، **استوانه یی**، مسطح، کاربن، بکتریا، نظریۀ حجروی |
| **ME12** | Afghan MoE, **Science Grade 12** (moe.gov.af) | **نیورون**، جلد، موی رگ، غدوات، کیمیاوی، واکسین، وقایه، اسکلیتی، پیوند، ترشح، پرده، استوانه یی |
| **TOL** | TolAfghan, **«فزیولوژی حجره»** | مایتوکاندریا، **انزایم**، **فسفوریلیشن اکسیداتیو**، میتابولیسم، **پروتئین**، شبکه اندوپلاسمی، سایتوزول |
| **AFD** | Afghan doctors' clinical writing (afghan-doctors.com) | **کیموتراپی**، تداوی دوایی، تداوی اشعوی، رادیو تراپی |
| **MOPH** | Afghan MoPH register + national medicines regulator | پتالوژی، هستولوژی، هستوپتالوژی، سایتولوژی، حجروی، مالیکولی، دوا/ادویه، کلیه |
