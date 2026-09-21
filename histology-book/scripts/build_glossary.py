#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_glossary.py — regenerates glossary/terminology-glossary.csv.

This file is the AUTHORITATIVE terminology source of truth for the book.
qa_scan.py reads it and derives both its forbidden-form list and its
canonical-form list from it, so there is exactly one place to change a term.

Schema (11 columns):
  dari_term, english_term, latin_term, abbreviation, preferred_form,
  forbidden_forms, source_authority, usage_notes, first_appearance,
  decision, confidence

decision  ∈ {AFGHAN STANDARD, COMMON AFGHAN TRANSLITERATION,
             ENGLISH RETAINED, EXPLANATORY DARI ONLY, VERIFY FURTHER}
confidence ∈ {HIGH, MEDIUM, LOW, UNRESOLVED}

forbidden_forms is semicolon-separated. Only GENUINE Iranian-Persian or
non-canonical forms go here. Never add:
  * a prefix of the term itself (سل is a prefix of سلول)
  * an Afghan transliteration variant that is in normal teaching use
    (ماست‌سل, میکروتوبول) — record those in usage_notes instead.
"""

import csv
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "glossary", "terminology-glossary.csv")

COLS = ["dari_term", "english_term", "latin_term", "abbreviation",
        "preferred_form", "forbidden_forms", "accepted_variants",
        "source_authority", "usage_notes", "first_appearance",
        "decision", "confidence"]

R = []


def T(dari, eng, forb="", src="", notes="", first="",
      dec="AFGHAN STANDARD", conf="HIGH", lat="", abbr="", acc=""):
    R.append({
        "dari_term": dari, "english_term": eng, "latin_term": lat,
        "abbreviation": abbr,
        "preferred_form": f"{dari} ({eng})",
        "forbidden_forms": forb, "accepted_variants": acc,
        "source_authority": src,
        "usage_notes": notes, "first_appearance": first,
        "decision": dec, "confidence": conf,
    })


AFG = "Afghan medical education usage (MOHE curriculum / Afghan medical-university teaching material)"
MAND = "Project canonical decision (Terminology Gate) — Afghan usage confirmed by sources"

# Named Afghan documents used as evidence below (defined here so every row can
# cite them by name and there is one place to correct a citation).
ME7  = "Afghan MoE textbook, Biology Grade 7 (moe.gov.af, Kabul, 1398 h.s.)"
ME12 = "Afghan MoE textbook, Science Grade 12 (moe.gov.af)"
TOL  = "TolAfghan (tolafghan.com), «فزیولوژی حجره» — Afghan cell-physiology text"
MOPH = "Afghan MoPH official recruitment register (moph.gov.af)"
AFD  = "Afghan doctors' clinical writing, afghan-doctors.com"
AV   = "AfghanVet (afghanvet.blogspot.com), Afghan biology text"
KUMS = ("Kabul University of Medical Sciences — kums.edu.af news bulletin "
        "«دیپارتمنت فزیوتراپی در شفاخانه تدریسی علی آباد پوهنتون علوم طبی کابل طی محفلی "
        "افتتاح شد» (۱۴۰۱/۹/۳۰)")
S5   = "Afghan faculty histology text: خاتم النبیین University, «هستولوژی تئوری ۲» (muslimuniversity.edu.af)"

# ============================================================ CORE / CH1 ===
T("حجره", "Cell", "سلول;یاخته", MAND,
  "CANONICAL. Afghan Dari uses حجره for Cell; plural حجرات. Confirmed by MOHE Biology curriculum "
  "(«حجره نباتی»), خاتم النبیین histology text, and AfghanVet («در کشور ما افغانستان ... واژه حجره "
  "به عوض سلول به مفهوم Cell به کار گرفته شده است»). سلول is the Iranian-Persian standard and is "
  "prohibited. NEVER list «سل» as forbidden — it is a prefix of both حجره and سلول.",
  "Ch01")
T("حجرات", "Cells", "سلول‌ها", MAND,
  "Plural of حجره. Use انساج for the plural of نسج.", "Ch01")
T("حجروی", "Cellular", "سلولی", MAND,
  "Adjective from حجره. Also used in the official MOHE book title «معافیت حجروی و مالیکولی».",
  "Ch01")
T("بین‌حجروی", "Intercellular", "بین‌سلولی", MAND,
  "Attested in Afghan Pashto/Dari teaching («بین الحجروي مسافه»).", "Ch04")
T("خارج‌حجروی", "Extracellular", "خارج‌سلولی", MAND, "", "Ch02")
T("درون‌حجروی", "Intracellular", "درون‌سلولی", MAND, "", "Ch02")
T("نسج", "Tissue", "بافت", MAND,
  "CANONICAL. Afghan Dari uses نسج (plural انساج). Confirmed by MOHE Biology curriculum "
  "(«انواع انساج نباتی»), the خاتم النبیین histology text, and the Scribd Afghan lecture "
  "«Connective Tissue نسج منضم». بافت is the Iranian-Persian standard and is prohibited.",
  "Ch01")
T("انساج", "Tissues", "بافت‌ها;بافت‌های;نسج‌ها;نسج‌های", MAND,
  "Afghan plural of نسج. The plural construct is «انساجِ».", "Ch01")
T("نسج منضم", "Connective tissue", "بافت پیوندی;بافت رابط;بافت همبند", MAND,
  "CANONICAL, user-mandated and independently confirmed by an Afghan histology lecture "
  "titled «Connective Tissue نسج منضم» and by the خاتم النبیین text («محل اصلی WBC در نسج منضم است»).",
  "Ch01")
T("نسج اپیتلیال", "Epithelial tissue", "بافت پوششی;بافت اپیتلیال;بافت پوششی", MAND,
  "Afghan teaching uses اپیتلیوم as the noun; the tissue is نسج اپیتلیال.", "Ch01")
T("هستولوژی", "Histology", "بافت شناسی;بافت‌شناسی", MAND,
  "The official course name in the Afghan medical curriculum (kateb.edu.af: «Histology (1) · هستولوژی · 77005»).",
  "Ch01")
T("سایتولوژی", "Cytology", "یاخته‌شناسی;سلول‌شناسی", MAND,
  "Used by the Afghan MoPH job description («پتالوژی اناتومیک (هستولوژی/هستوپتالوژی، سایتولوژی)»).",
  "Ch01")
T("پتالوژی", "Pathology", "پاتولوژی;آسیب‌شناسی", MAND,
  "Afghan MoPH and MoHE use پتالوژی; the Kabul medical curriculum lists «Pathology (1) · پتالوژی».",
  "Ch01")
T("هستوپتالوژی", "Histopathology", "هیستوپاتولوژی;بافت‌آسیب‌شناسی", MAND,
  "Afghan MoHE job-advert source list names «بست هستوپتالوژی پوهنحی طب».", "Ch01")
T("اناتومی", "Anatomy", "کالبدشناسی;تشریح", MAND,
  "Afghan medical curriculum: «Anatomy (1) · اناتومی».", "Ch01")
T("فزیولوژی", "Physiology", "فیزیولوژی", MAND,
  "Afghan curriculum spells it فزیولوژی (ز not ز-ی); both are heard, this is the book standard.",
  "Ch01")
T("طب", "Medicine (discipline)", "پزشکی", MAND,
  "Afghan usage: «فاکولته طب»، «طب معالجوی»، «مرکز طبی». پزشکی is the Iranian form.", "Ch01")
T("داکتر", "Doctor / physician", "پزشک", MAND,
  "Afghan forms داکتر and دوکتور both occur; داکتر is the book standard.", "Ch01")
T("شفاخانه", "Hospital", "بیمارستان", MAND, "", "Ch01")
T("محصل", "Student", "دانشجو", MAND, "Afghan: «محصلین» in every Afghan curriculum document.", "Ch01")
T("پوهنحی", "Faculty (of a university)", "دانشکده", MAND,
  "Afghan: پوهنحی طب معالجوی. University = پوهنتون.", "Ch01")
T("مریضی", "Disease", "بیماری", MAND,
  "Afghan: «مریضی سل»، «امراض». Iranian standard is بیماری.", "Ch01", conf="HIGH")
T("مریض", "Patient", "بیمار", MAND, "Afghan clinical register: «مریضان».", "Ch01")
T("امراض", "Diseases", "بیماری‌ها", MAND,
  "The Afghan institutional plural («امراض جلدی»، «امراض هاضمه»); accepted alongside مریضی‌ها.",
  "Ch01")
T("تداوی", "Treatment", "درمان;معالجه", MAND,
  "Wikipedia's Afghan/Iranian differential list records «تداوی: درمان». Afghan MoPH and every "
  "Afghan hospital site use تداوی.", "Ch01")
T("وقایه", "Prevention", "پیشگیری", MAND, "Afghan: «قابل اجتناب (وقایه یا تداوی)».", "Ch05")

# ==================================================== METHODS (Ch1) ========
T("اسلاید", "Slide", "لام;لام میکروسکوپی", MAND,
  "English retained and used as the Afghan technical word.", "Ch01",
  dec="ENGLISH RETAINED")
T("رنگ‌آمیزی", "Staining", "رنگ‌آمیزی (فاصله‌دار)", "AfghanVet, Afghan biology text (afghanvet.blogspot.com) — «بعد از رنگ‌آمیزی در زیر مایکروسکوپ»",
  "Written with ZWNJ. Not an Iranian-specific form.", "Ch01")
T("مایکروسکوپ", "Microscope", "میکروسکوپ", MAND,
  "Afghan sources write مایکروسکوپ (AfghanVet, khateb texts).", "Ch01")
T("مایکروسکوپ نوری", "Light microscope (LM)", "", MAND,
  "Abbreviated LM in English text throughout the book.", "Ch01", abbr="LM")
T("مایکروسکوپ الکترونی", "Electron microscope", "", MAND,
  "TEM = مایکروسکوپ الکترونی انتقالی; SEM = مایکروسکوپ الکترونی سکنی.", "Ch01")
T("تثبیت", "Fixation", "", AFG, "Also written فیکساتیو (English transliteration).", "Ch01",
  dec="COMMON AFGHAN TRANSLITERATION")
T("فرمالین", "Formalin", "", AFG, "Afghan texts also use فرمالین/فورمالین interchangeably; استاندارد = فرمالین.",
  "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("پارافین", "Paraffin", "", AFG, "", "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("میکروتوم", "Microtome", "", AFG, "", "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("بیوپسی", "Biopsy", "", AFG, "Afghan clinical form; English also used in full.", "Ch01",
  dec="COMMON AFGHAN TRANSLITERATION")
T("آرتیفکت", "Artifact", "", AFG, "", "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("هماتوکسیلین", "Hematoxylin", "", AFG, "", "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("ائوزین", "Eosin", "", AFG, "The H&E pair; H&E is kept as the English abbreviation.",
  "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("بازوفیلی", "Basophilia", "", AFG, "", "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("ائوزینوفیلی", "Eosinophilia", "", AFG, "", "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("متاکرومازی", "Metachromasia", "", AFG, "Classic exam point: mast-cell granules.", "Ch01",
  dec="COMMON AFGHAN TRANSLITERATION")
T("تولوئیدین‌بلو", "Toluidine blue", "", AFG, "", "Ch01", dec="COMMON AFGHAN TRANSLITERATION")
T("ایمونوهیستوشیمی", "Immunohistochemistry", "", AFG, "Abbreviated IHC.", "Ch01",
  dec="COMMON AFGHAN TRANSLITERATION", abbr="IHC")

# =================================================== CYTOPLASM (Ch2) =======
T("سیتوپلاسم", "Cytoplasm", "", AFG,
  "All three spellings circulate in Afghan texts (سیتوپلاسم, سیتوپلازم, سایتوپلازم). The book "
  "standardises on سیتوپلاسم (AfghanVet form). Variants accepted, NOT forbidden. Do not add "
  "سیتوپلازم or سایتوپلازم to forbidden_forms.", "Ch02", conf="MEDIUM")
T("سیتوزول", "Cytosol", "", AFG, "Also written سایتوزول; both accepted.", "Ch02", conf="MEDIUM")
T("غشای حجروی", "Cell membrane", "غشای سلولی;غشای پلاسمایی", MAND,
  "Afghan sources write «غشای حجره» / «حجروي غشا» (TolAfghan, wasiweb). پلاسمالما is kept as the "
  "English/Latin term where the exam needs it.", "Ch02")
T("پلاسمالما", "Plasma membrane", "plasmalemma", AFG,
  "English/Latin term retained for exam recognition.", "Ch02", dec="ENGLISH RETAINED")
T("مالیکول", "Molecule", "مولکول", "Afghan MoHE official book list — «معافیت حجروی و مالیکولی» (Kabul 1400); TolAfghan (tolafghan.com) biology text.",
  "Afghan transliteration is مالیکول/مالیکولی. مولکول is the Iranian form.", "Ch02")
T("ایون", "Ion", "یون", "Afghan biology texts («آیون کلسیم»، «ایون کلسیم»).",
  "Afghan transliteration ایون. یون is the Iranian form. Note: the substring یون also occurs inside "
  "پیوند، اکسیداسیون، فیلتراسیون — those are ordinary words and must never be flagged.",
  "Ch02")
T("انزایم", "Enzyme", "آنزیم", "Afghan histology text (خاتم النبیین) repeatedly writes انزایم; Afghan biology texts likewise.",
  "Afghan transliteration انزایم. آنزیم is the Iranian form.", "Ch02")
T("کیمیاوی", "Chemical", "شیمیایی", "MOHE Biology curriculum: «ساختمان کیمیاوی آن».",
  "Afghan form کیمیاوی/کیمیا. شیمیایی is the Iranian form. بیوشیمیایی (biochemical) is a legitimate "
  "compound and must NOT be flagged.", "Ch02")
T("میتابولیسم", "Metabolism", "متابولیسم", "TolAfghan: «دخالت در میتابولیسم قندها».",
  "Afghan transliteration میتابولیسم.", "Ch02")
T("ماتریکس", "Matrix", "extracellular matrix", AFG,
  "International term, used throughout Afghan teaching. The Afghan variant بستره also occurs "
  "(TolAfghan) but is not required. Abbreviated ECM.", "Ch02", dec="ENGLISH RETAINED",
  abbr="ECM")
T("رایبوزوم", "Ribosome", "ریبوزوم", "TolAfghan and AfghanVet biology texts.",
  "Afghan transliteration رایبوزوم, matching the Dari pronunciation.", "Ch02")
T("شبکه آندوپلاسمی", "Endoplasmic reticulum", "شبکه درون‌یاخته‌ای", AFG,
  "Abbreviated ER; خشن = rough (RER), صاف/نرم = smooth (SER). «شبکه درون‌یاخته‌ای» is the Iranian "
  "purist coinage and is prohibited.", "Ch02", abbr="ER")
T("دستگاه گلژی", "Golgi apparatus", "", AFG, "Afghan texts use دستگاه گلژی.", "Ch02",
  dec="COMMON AFGHAN TRANSLITERATION")
T("لایزوزوم", "Lysosome", "لیزوزوم", "Afghan histology text writes لایزوزوم/لیزوزم.",
  "Both لایزوزوم and لیزوزوم occur in Afghan texts; لایزوزوم is the book standard.", "Ch02",
  dec="COMMON AFGHAN TRANSLITERATION", conf="MEDIUM")
T("پروتئازوم", "Proteasome", "", AFG, "", "Ch02", dec="COMMON AFGHAN TRANSLITERATION")
T("پراکسیزوم", "Peroxisome", "", AFG, "", "Ch02", dec="COMMON AFGHAN TRANSLITERATION")
T("مایتوکندریا", "Mitochondrion", "", MAND,
  "Canonical per the project decision list. Afghan texts print both مایتوکندریا and مایتوکاندریا; "
  "the variant is ACCEPTED, not forbidden. Do not list مایتوکاندریا as forbidden.",
  "Ch02", acc="مایتوکاندریا;میتوکندری")
T("کریستا", "Crista", "cristae", AFG, "Plural کریستاها. English retained.",
  "Ch02", dec="ENGLISH RETAINED")
T("سیتواسکلتون", "Cytoskeleton", "اسکلت حجروی", AFG,
  "English retained; «اسکلت حجروی» is the Dari gloss.", "Ch02", dec="ENGLISH RETAINED")
T("میکروتوبول", "Microtubule", "ریزلوله", AFG,
  "Afghan exam form is میکروتوبول. Do NOT list it as forbidden — it is not an Iranian form.",
  "Ch02")
T("میکروفیلامنت", "Microfilament", "ریزرشته", AFG,
  "Afghan exam form is میکروفیلامنت. The Dari compound ریزرشته is a literal morpheme "
  "translation of micro- + filament and carries no cited Afghan document, so it is prohibited "
  "(the pass-2 note that treated it as acceptable was a contradiction and was removed).", "Ch02")
T("فیلامنت میانی", "Intermediate filament", "", AFG, "", "Ch02")
T("مژک", "Cilium", "", AFG,
  "Both مژک and سیلیا/سلیا are attested in Afghan teaching material (the خاتم النبیین text uses "
  "«مژک دار» and «سلیا دار» in the same chapter). مژک is the book standard; سیلیا is accepted. "
  "Do NOT forbid سیلیا.", "Ch02", conf="MEDIUM", acc="سیلیا;سلیا")
T("میکروویلی", "Microvillus", "ریزپرز;مایکروویلای", MAND,
  "Afghan transliteration; the Pashto teaching text writes مایکروویلای. ریزپرز is the Iranian form.",
  "Ch02")
T("استروئید", "Steroid", "استرویید", AFG,
  "Afghan histology and biology texts write استروئید. استرویید is the Iranian transliteration.",
  "Ch02")
T("کاربوهایدریت", "Carbohydrate",
  "کربوهیدرات;کربوهیدرات‌ها;کربوهیدرات‌های;کربوهیدراتی;کربوهیدراتیِ;کاربوهیدرات",
  TOL + " — «… و سایر لیپیدها ۴ فیصد و کاربوهایدریت‌ها ۳ فیصد»",
  "CANONICAL Afghan-Dari form (owner decision, 2026-09-21). Attested in an Afghan cell-physiology "
  "text: TolAfghan, «فزیولوژی حجره», «… سایر لیپیدها ۴ فیصد و کاربوهایدریت‌ها ۳ فیصد». This is the "
  "established Afghan transliteration pattern (cf. کاربن), NOT a morpheme-by-morpheme construction. "
  "English «Carbohydrate» may follow in parentheses at first use where that helps the reader. The "
  "Persian/Iranian transliteration is NOT used in this book (owner decision). «قندها» (sugars) is a "
  "general biological expression used in Afghan school books and is NOT the medical term for "
  "Carbohydrate. Plural کاربوهایدریت‌ها · adjective کاربوهایدریتی. Every form in this row's "
  "forbidden list is NON-CANONICAL by owner decision — prohibited for this book, not "
  "automatically because Iran uses it.",
  "Ch1 (PAS); Ch2 (glycocalyx); Ch5 (GAG)", dec="COMMON AFGHAN TRANSLITERATION", conf="HIGH")
T("فسفوریلیشن", "Phosphorylation", "فسفریلاسیون;فسفوریلاسیون", AFG,
  "Afghan texts write «فسفوریلیشن اکسیداتیو» (TolAfghan, خاتم النبیین).", "Ch02", conf="MEDIUM")
T("اگزوسایتوز", "Exocytosis", "", AFG, "", "Ch02", dec="COMMON AFGHAN TRANSLITERATION")
T("اندوسایتوز", "Endocytosis", "", AFG, "", "Ch02", dec="COMMON AFGHAN TRANSLITERATION")
T("فاگوسایتوز", "Phagocytosis", "بیگانه‌خواری", AFG, "", "Ch02",
  dec="COMMON AFGHAN TRANSLITERATION")
T("پینوسایتوز", "Pinocytosis", "", AFG, "", "Ch02", dec="COMMON AFGHAN TRANSLITERATION")
T("گلیکوکالیکس", "Glycocalyx", "", AFG, "", "Ch02", dec="COMMON AFGHAN TRANSLITERATION")
T("گلیکوزیلاسیون", "Glycosylation", "", AFG, "", "Ch02",
  dec="COMMON AFGHAN TRANSLITERATION")
T("لیپوفوسین", "Lipofuscin", "", AFG, "Wear-and-tear pigment.", "Ch02",
  dec="COMMON AFGHAN TRANSLITERATION")

# ===================================================== NUCLEUS (Ch3) =======
T("هسته", "Nucleus", "", AFG, "", "Ch03")
T("هسته‌چه", "Nucleolus", "هستک", AFG,
  "Afghan histology text writes «هسته چه» (e.g. «هسته بزرگ و هسته چه»). هستک is the Iranian form.",
  "Ch03")
T("غشای هستوی", "Nuclear envelope", "پوشش هسته‌ای", AFG,
  "Also written پوشش هستوی; both acceptable, book uses غشای هستوی/پوشش هستوی.", "Ch03",
  conf="MEDIUM")
T("منفذ هستوی", "Nuclear pore", "منفذ هسته‌ای", AFG, "", "Ch03", conf="MEDIUM")
T("کروماتین", "Chromatin", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("هتروکروماتین", "Heterochromatin", "", AFG, "", "Ch03",
  dec="COMMON AFGHAN TRANSLITERATION")
T("یوکروماتین", "Euchromatin", "", AFG, "", "Ch03",
  dec="COMMON AFGHAN TRANSLITERATION")
T("نوکلئوزوم", "Nucleosome", "", AFG, "", "Ch03",
  dec="COMMON AFGHAN TRANSLITERATION")
T("هیستون", "Histone", "", AFG, "Adjective هیستونی (histonic) — must not be confused with ستونی.",
  "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("کروموزوم", "Chromosome", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("کروماتید", "Chromatid", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("سانترومر", "Centromere", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("کینتوکور", "Kinetochore", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("تلومر", "Telomere", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("کاریوتایپ", "Karyotype", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("کرویاتِ سرخ", "Erythrocyte", "گویچهٔ سرخ;گلبول قرمز;حجرات سرخ", AFG,
  "Afghan histology text uses کرویات («کرویات سفید خون»); گویچه is the Iranian form. حجرات سرخ also "
  "occurs in Afghan texts but کرویات is the book standard. RBC retained as the abbreviation.",
  "Ch03", abbr="RBC")
T("میتوز", "Mitosis", "", AFG, "Phase names: پروفاز، متافاز، آنافاز، تلوفاز.", "Ch03",
  dec="COMMON AFGHAN TRANSLITERATION")
T("میوز", "Meiosis", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("آپوپتوز", "Apoptosis", "مرگ برنامه‌ریزی‌شدهٔ حجره", AFG,
  "Both the transliteration and the Dari gloss are used; the English term is kept for exam "
  "recognition.", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("نکروز", "Necrosis", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("کاسپاز", "Caspase", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("اپی‌ژنتیک", "Epigenetics", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("متیلاسیون", "Methylation", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("استیلاسیون", "Acetylation", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("تریزومی", "Trisomy", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("مونوزومی", "Monosomy", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("آنیوپلوئیدی", "Aneuploidy", "", AFG, "", "Ch03", dec="COMMON AFGHAN TRANSLITERATION")
T("کاریوکنیزیس", "Karyokinesis", "", AFG, "", "Ch03", dec="ENGLISH RETAINED")

# ================================================== EPITHELIUM (Ch4) =======
T("اپیتلیوم", "Epithelium", "بافت پوششی", MAND,
  "International term used unchanged in Afghan teaching (خاتم النبیین: «اپیتلیوم استوانه‌یی چند "
  "طبقه کاذب مژک دار»). Adjective: اپیتلیال.", "Ch04")
T("لامینای پایه", "Basal lamina", "غشای پایه", MAND,
  "Afghan teaching keeps the international terminology (the Afghan text writes basal lamina / "
  "basel membrane). غشای پایه is used only where the reference means the whole basement membrane.",
  "Ch04")
T("غشای پایه", "Basement membrane", "", AFG,
  "The composite structure = لامینای پایه + لامینا رتیکولاریس. Kept distinct from لامینای پایه.",
  "Ch04")
T("مسطح", "Squamous", "سنگفرشی;خشت فرشی;فلس", MAND,
  "CANONICAL per the project decision list («Simple Squamous Epithelium = اپیتلیوم سادهٔ مسطح»). "
  "Afghan teaching material shows سنگفرشی and خشت‌فرشی as well, so این forms are classified as "
  "non-canonical variants rather than Iranian — but the book must use مسطح consistently. "
  "Classified as NON-CANONICAL (book-consistency) not as an Iranian-Persian violation.",
  "Ch04", conf="MEDIUM")
T("مکعبی", "Cuboidal", "", AFG,
  "Matches Afghan teaching («اپیتلیوم مکعبی»). No competing Afghan form.", "Ch04")
T("استوانه‌ای", "Columnar", "منشوری;ستونی", AFG,
  "Afghan histology text uses «استوانه‌یی» throughout. منشوری is the Iranian form. ستونی is a "
  "Pashto-side equivalent and is not used in the Dari text. NOTE: هیستونی (histonic) contains the "
  "letters ستونی and must never be flagged.", "Ch04")
T("مطبق", "Stratified", "چندلایه", AFG,
  "Afghan teaching: «اپیتلیوم خشت فرشی چند طبقه‌یی». مطبق is the reference's term.", "Ch04")
T("شبه‌مطبق", "Pseudostratified", "", AFG,
  "Afghan text: «اپیتلیوم استوانه‌یی چند طبقه کاذب»; شبه‌مطبق and مطبق کاذب both occur.",
  "Ch04", conf="MEDIUM")
T("یوروتلیوم", "Urothelium", "اپیتلیوم انتقالی;اپیتلیوم مثانه", MAND,
  "International term retained per the reference; اپیتلیوم انتقالی given as the Dari gloss.",
  "Ch04", dec="ENGLISH RETAINED")
T("دسموزوم", "Desmosome", "پل حجروی", AFG, "", "Ch04",
  dec="COMMON AFGHAN TRANSLITERATION")
T("همی‌دسموزوم", "Hemidesmosome", "", AFG, "", "Ch04",
  dec="COMMON AFGHAN TRANSLITERATION")
# ---- FINAL junction decision (locked by the owner, 2026-09-21) -------------
# CANONICAL = the established international terminology, which is what Afghan
# medical sources actually use. The Afghan Dari explanatory form is recorded but
# is NOT the primary scientific term, and no Dari equivalent is invented for the
# junctions where Afghan sources name only the international term.
WASIWEB = ("wasiweb.com, «حجروي اتصال، د اتصال ډولونه» — byline «قاسم خان همت کندهار طب "
           "پوهنځۍ محصل» (Kandahar Faculty of Medicine student)")

T("Tight junction", "Zonula occludens", "", WASIWEB + " — «①مضبوط اتصال【Tight junction】»، "
  "«د مضبوط اتصال وظایف»",
  "CANONICAL: **Tight junction / Zonula occludens**. The international term is the primary "
  "scientific term (owner decision, locked). The Afghan explanatory form «مضبوط اتصال» is "
  "attested in Afghan medical-faculty material — wasiweb.com, «حجروي اتصال، د اتصال ډولونه» "
  "(byline: a Kandahar Faculty of Medicine student): «①مضبوط اتصال【Tight junction】» — and MAY be "
  "used as a Dari gloss, but it is NOT the primary scientific term. It is not the Iranian wording "
  "(Iranian sources write اتصالات محکم / اتصال تنگ).",
  "Ch04", dec="ENGLISH RETAINED", conf="HIGH", lat="Zonula occludens")

T("Adherens junction", "Zonula adherens", "اتصال چسبنده;اتصالات چسبنده",
  "TolAfghan, «هستولوژي Histology — دوهمه برخه» (tolafghan.com/articles/19376) — "
  "«b- Zonula Adherence = Intermediate Juntion»; " + WASIWEB,
  "CANONICAL: **Adherens junction / Zonula adherens**. International term, canonical by owner "
  "decision. NON-CANONICAL Dari calque recorded so it can never be reused as the scientific term: "
  "no Afghan source using a Dari equivalent was located — Afghan sources name this junction only "
  "internationally (TolAfghan: «Zonula Adherence = Intermediate Juntion»; wasiweb: «adherence "
  "junction»). No replacement Dari term is invented.",
  "Ch04", dec="ENGLISH RETAINED", conf="HIGH", lat="Zonula adherens")

T("Gap junction", "Gap junction", "اتصال شکافی;اتصال شکاف‌دار",
  WASIWEB + " — «③ګپ جنکشن Gap Junction»؛ «درز junction یا gap junction»؛ "
  "ps.wikipedia «بشروي نسجونه» — «٤-Gapjunction»",
  "CANONICAL: **Gap junction**. International term, canonical by owner decision. NON-CANONICAL "
  "Dari calque recorded so it can never be reused as the scientific term: no Afghan source using a "
  "Dari equivalent was located — Afghan sources use the transliteration (wasiweb: «ګپ جنکشن Gap "
  "Junction», «درز junction یا gap junction»; ps.wikipedia: «Gapjunction»). No replacement Dari "
  "term is invented.",
  "Ch04", dec="ENGLISH RETAINED", conf="HIGH", lat="Connexon")

T("کادهرین", "Cadherin", "", AFG, "", "Ch04", dec="ENGLISH RETAINED")
T("اینتگرین", "Integrin", "", AFG, "", "Ch04", dec="ENGLISH RETAINED")
T("کلودین", "Claudin", "", AFG, "", "Ch04", dec="ENGLISH RETAINED")
T("اوکلودین", "Occludin", "", AFG, "", "Ch04", dec="ENGLISH RETAINED")
T("کراتینوسایت", "Keratinocyte", "", AFG, "", "Ch04",
  dec="COMMON AFGHAN TRANSLITERATION")
T("ملانوسایت", "Melanocyte", "", AFG, "", "Ch04",
  dec="COMMON AFGHAN TRANSLITERATION")
T("گابلت", "Goblet cell", "حجرهٔ جامی", AFG,
  "Afghan histology text keeps Goblet cell in English; حجرهٔ جامی is the Dari gloss.", "Ch04",
  dec="ENGLISH RETAINED")
T("موسین", "Mucin", "", AFG, "", "Ch04", dec="COMMON AFGHAN TRANSLITERATION")
T("موسینوژن", "Mucinogen", "", AFG, "", "Ch04", dec="COMMON AFGHAN TRANSLITERATION")
T("موکوس", "Mucus", "", AFG, "Afghan histology text uses موکوس.", "Ch04",
  dec="COMMON AFGHAN TRANSLITERATION")
T("غدوات شحمی", "Sebaceous glands", "غدد سباسه", AFG,
  "Afghan medical-student source writes «غدوات شحمی» and «غدوات عرقیه». سباسه is the Iranian form.",
  "Ch04", conf="MEDIUM")
T("اندوتلیوم", "Endothelium", "آندوتلیوم", AFG,
  "Both اندوتلیوم and آندوتلیوم occur in Afghan texts; اندوتلیوم is the book standard.", "Ch04",
  conf="MEDIUM")
T("مزوتلیوم", "Mesothelium", "", AFG, "", "Ch04",
  dec="COMMON AFGHAN TRANSLITERATION")
T("لامینا پروپریا", "Lamina propria", "", AFG, "International term retained.", "Ch04",
  dec="ENGLISH RETAINED")
T("مخاط", "Mucosa", "", AFG, "Afghan histology text: «سطح مخاط»، «تحت مخاط».", "Ch04")
T("تحت مخاط", "Submucosa", "", AFG, "", "Ch04")
T("سروزا", "Serosa", "", AFG, "Afghan histology text: «لایه سروزا».", "Ch04")
T("متاپلازی", "Metaplasia", "", AFG, "", "Ch04", dec="COMMON AFGHAN TRANSLITERATION")
T("دیسپلازی", "Dysplasia", "", AFG, "", "Ch04", dec="COMMON AFGHAN TRANSLITERATION")
T("نئوپلازی", "Neoplasia", "", AFG, "", "Ch04", dec="COMMON AFGHAN TRANSLITERATION")
T("کارسینوم درجا", "Carcinoma in situ", "", AFG, "", "Ch04", abbr="CIS")
T("میواپی‌تلیال", "Myoepithelial", "", AFG, "", "Ch04",
  dec="COMMON AFGHAN TRANSLITERATION")
T("هاضموی", "Digestive / gastrointestinal", "گوارشی;لوله گوارش", AFG,
  "Afghan clinical usage favours هاضمه («امراض هاضمه»، «دستگاه هاضمه»). NOTE: the Afghan "
  "histology text also shows «لوله گوارشی», so گوارشی is classified as non-canonical (book "
  "consistency) rather than Iranian. هاضموی is the book standard.", "Ch04", conf="MEDIUM")

# ================================================= CONNECTIVE (Ch5) ========
T("مادهٔ زمینه‌ای", "Ground substance", "", AFG, "", "Ch05")
T("کولاجن", "Collagen", "", AFG, "Afghan spelling کولاجن (Pashto teaching text: د کوالجنس).",
  "Ch05", dec="COMMON AFGHAN TRANSLITERATION")
T("تروپوکولاجن", "Tropocollagen", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("پروکولاجن", "Procollagen", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("فیبروبلاست", "Fibroblast", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("ماکروفاژ", "Macrophage", "", AFG, "Afghan teaching uses ماکروفاژ.", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("ماست‌سل", "Mast cell", "سلول مست;ماست سیت", AFG,
  "Afghan form ماست‌سل / ماست سیت. NOTE: ماست‌سل is a transliteration, NOT an Iranian form — do "
  "not list it under forbidden_forms of any entry.", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("پلاسما‌سل", "Plasma cell", "پلاسموسیت;سلول پلاسما", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("شحمی", "Adipose / fatty", "چربی (اصطلاح بافتی)", AFG,
  "Afghan sources use شحم/شحمی for fat («قطرات شحم»، «غدوات شحمی»). چربی remains the everyday word.",
  "Ch05", conf="MEDIUM")
T("آدیپوسایت", "Adipocyte", "حجرهٔ شحمی", AFG, "English/transliterated term retained.",
  "Ch05", dec="ENGLISH RETAINED")
T("میوفیبروبلاست", "Myofibroblast", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("رشتهٔ رتیکولار", "Reticular fiber", "", AFG, "Type III collagen; silver stain.", "Ch05")
T("رشتهٔ الاستیک", "Elastic fiber", "", AFG, "", "Ch05")
T("الاستین", "Elastin", "", AFG, "", "Ch05", dec="COMMON AFGHAN TRANSLITERATION")
T("فیبریلین", "Fibrillin", "", AFG, "Marfan syndrome protein.", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("دسموزین", "Desmosine", "", AFG, "Cross-link marker of elastin.", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("فیبرونکتین", "Fibronectin", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("لامینین", "Laminin", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("نیدوژن", "Nidogen", "entactin", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("پروتئوگلیکان", "Proteoglycan", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("گلیکوزآمینوگلیکان", "Glycosaminoglycan", "mucopolysaccharide", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION", abbr="GAG")
T("هیالورونان", "Hyaluronan", "hyaluronic acid", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("هیالورونیداز", "Hyaluronidase", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("کندرویتین سولفات", "Chondroitin sulfate", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("کراتان سولفات", "Keratan sulfate", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("درماتان سولفات", "Dermatan sulfate", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("هپارین", "Heparin", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("هیستامین", "Histamine", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("ترپتاز", "Tryptase", "", AFG, "Mast-cell marker.", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("نسج منضم شل", "Loose (areolar) connective tissue", "بافت همبند سست;نسج منضم سست",
  AFG, "Afghan teaching writes نسج منضم; شل and سست are both acceptable qualifiers.",
  "Ch05", conf="MEDIUM")
T("نسج منضم متراکم", "Dense connective tissue", "بافت همبند متراکم", AFG, "", "Ch05")
T("تاندون", "Tendon", "", AFG, "", "Ch05")
T("رباط", "Ligament", "", AFG, "", "Ch05")
T("نسج گرانولاسیون", "Granulation tissue", "بافت گرانوله", AFG,
  "Scribd Afghan lecture «Connective Tissue نسج منضم» uses this term family.", "Ch05")
T("فیبروز", "Fibrosis", "", AFG, "", "Ch05", dec="COMMON AFGHAN TRANSLITERATION")
T("ادم", "Edema", "", AFG, "", "Ch05", dec="COMMON AFGHAN TRANSLITERATION")
T("فیبرین", "Fibrin", "", AFG, "", "Ch05", dec="COMMON AFGHAN TRANSLITERATION")
T("رگ‌زایی", "Angiogenesis", "واسکولارزاسیون", AFG, "Afghan form رگ‌زایی.", "Ch05",
  conf="MEDIUM")
T("اسکوروی", "Scurvy", "اسکوربوت", AFG, "Vitamin-C deficiency; collagen hydroxylation fails.",
  "Ch05", dec="COMMON AFGHAN TRANSLITERATION")
T("مارفان", "Marfan syndrome", "", AFG, "", "Ch05",
  dec="COMMON AFGHAN TRANSLITERATION")
T("جلد", "Skin", "پوست", AFG,
  "Afghan histology text: «اپیتلیوم جلد»; Afghan clinical usage: «امراض جلدی». پوست is the Iranian "
  "form in the differential list. اپیدرم/درم/هیپودرم are kept as the international layer names.",
  "Ch01")

# =========================================== BLOOD VESSELS & ORGAN NAMES ===
T("اوعیهٔ دموی", "Blood vessels", "رگ‌های خونی;رگهای خونی;عروق خونی", MAND,
  "CANONICAL, user-mandated. Used for the collective/plural concept. A single named vessel keeps "
  "its own term (شریان، ورید، موی‌رگ); the generic singular رگ is attested in Afghan teaching and "
  "is allowed in fixed phrases such as «دیوارهٔ رگ».", "Ch01", conf="MEDIUM")
T("شریان", "Artery", "", MAND, "", "Ch01")
T("ورید", "Vein", "", MAND, "", "Ch01")
T("شریانچه", "Arteriole", "", MAND, "", "Ch01")
T("وریدچه", "Venule", "", MAND, "", "Ch01")
T("موی‌رگ", "Capillary", "مویرگ", "Afghan histology text: «قلب، شریان، ورید، موی رگها».",
  "Afghan written form is موی‌رگ (two elements). مویرگ is the contracted Iranian form.", "Ch01")
T("سرخرگ", "Artery (arterial)", "", AFG,
  "Afghan everyday/clinical form used for named arteries (آئورت, سرخرگ ریوی). Retained alongside "
  "the canonical شریان; the book uses شریان for the histological definition.", "Ch05",
  conf="MEDIUM")

# ---- terms deliberately RETAINED IN ENGLISH / unresolved ----
T("آنتی‌ژن", "Antigen", "", AFG,
  "[VERIFY TERMINOLOGY] Afghan sources show both آنتی‌ژن and آنتی‌نژ/آنتی‌نژن. Not an Iranian "
  "form; the book keeps آنتی‌ژن until an Afghan institutional source settles it.", "Ch05",
  dec="VERIFY FURTHER", conf="UNRESOLVED")
T("Cellulitis", "Cellulitis", "", AFG,
  "No reliable Afghan Dari standard could be established; kept in English with a Dari explanation "
  "(«گسترش عفونت در نسج منضم سست زیر جلد»). Rule 4 of the Terminology Gate.",
  "Ch05", dec="ENGLISH RETAINED")
T("باکتری", "Bacteria", "باکتریا", AFG,
  "Afghan histology text writes باکتریا; باکتری is equally current in Afghanistan and is what the "
  "book already used, so باکتری is kept as the book standard (no stylistic churn) and باکتریا is "
  "registered as an accepted variant.", "Ch02",
  dec="ENGLISH RETAINED", conf="MEDIUM", acc="باکتریا")
T("پاراسلولار", "Paracellular", "", AFG,
  "English term retained. The book writes «(paracellular seal)» rather than a Dari coinage, per "
  "rule 4 (do not invent).", "Ch04", dec="ENGLISH RETAINED")


# ============================================ SUPPLEMENT (Gate pass 2) ======
# Clinical-register vocabulary decided in the second source review. Pass 1 did
# not reach this layer because it is not the سلول/بافت core; it is the everyday
# clinical vocabulary that a student meets on ward signs and in MoPH documents.
AFG2 = ("Afghan institutional usage: MoPH publications / Afghanistan health "
        "sector documents / Afghan hospitals and Afghan medical-faculty material")

T("دوا", "Drug / medicine",
  "دارو;داروی;دارویی;داروها;داروهای;داروهایی;داروهایش", AFG2,
  "Afghan register. MoPH-sector text: «تمامی خدمات به شمول دوا غذا رایگان است»، «کیفیت دواهای "
  "در حال فروش»، «دواخانه»، «دواسازی»، «مصارف ادویه». Afghanistan's medicines regulator is "
  "literally «اداره ملی ادویه و غذا» (dpmea.gov.af), whose own text writes «محصولات دوایی» and "
  "«قاچاق دوا ها». Afghan hospitals: «با استفاده از روش‌های تداوی مختلفی از جمله دواهای مرتبط». "
  "دارو does still appear in Afghan journalistic prose, so this is a REGISTER standardisation, "
  "not a hard ban. Keep the family: دوا / دوایی / دواخانه / ادویه / دواسازی.",
  "Ch2 (drug-metabolising SER); Ch3 (chemotherapy)", "AFGHAN STANDARD", "MEDIUM",
  acc="ادویه;دواخانه;دواسازی")

T("کیموتراپی", "Chemotherapy", "شیمی‌درمانی;شیمی درمانی;کیمیا تداوی;کیمیا‌تداوی", AFG2,
  "Afghan/Arabic transliteration in current Afghan use (کیموتراپی). «کیمیا تداوی» and "
  "«کیمیا‌تداوی» are recorded as forbidden because they are also the exact artefact produced when "
  "a rule replaces شیمی inside شیمی‌درمانی — forbid them so the artefact can never reappear.",
  "Ch3 (stage-specific chemotherapy)", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کلیه", "Kidney", "", AFG2,
  "Formal anatomical register. Afghan MoPH nephrology posting: «امراض کلیه، از جمله عدم کفایه "
  "کلیه (گرده)» — i.e. Afghan official medical writing uses کلیه as the term and glosses it with "
  "the colloquial گرده. Both are Afghan; کلیه is the one that belongs in a histology text. NOT an "
  "Iranian-specific form.", "Ch2 (cilium flow sensor); Ch4; Ch5 (macrophage location)",
  "AFGHAN STANDARD", "MEDIUM", acc="گرده")

T("کبد", "Liver", "", AFG2,
  "Afghan clinical text writes both: «امراض کبدی یا جگر، مانند سیروز، صفرا، سرطان کبد و هپاتیت» "
  "(Afghan hospital) — کبد as the technical term, جگر as the everyday gloss. Both are Afghan; "
  "کبد is the register of a histology textbook.", "Ch2 (SER, hepatocytes)",
  "AFGHAN STANDARD", "MEDIUM", acc="جگر")

T("ریه", "Lung", "", AFG2,
  "Both ریه and شش are Afghan. Afghan hospital: «کیست ها و تومورهای ریه»، «بذل پریکارد قلب و "
  "ریه»؛ Afghan hospital department list uses «شش». The book is internally consistent on ریه, so "
  "ریه»؛ Afghan hospital department list uses «شش». The book is internally consistent on ریه. "
  "NOTE: شش is NOT in accepted_variants — in this book شش is the numeral 'six' "
  "(«شش ویژگی»، «شش وظیفه»), so a variant registration would produce a meaningless "
  "inconsistency flag. Recorded here in usage_notes instead.", "Ch2; Ch4; Ch5",
  "AFGHAN STANDARD", "MEDIUM")
T("پانکراس", "Pancreas", "", AFG2,
  "Afghan hospitals write «لوزالمعده» («... مانند مری، معده، روده کوچک، روده بزرگ، کبد، "
  "لوزالمعده»); پانکراس is the international transliteration and is what students meet in exam "
  "questions. Both are Afghan — kept پانکراس, لوزالمعده registered as an accepted variant.",
  "Ch2 (RER-rich acinar cell); Ch4", "COMMON AFGHAN TRANSLITERATION", "MEDIUM",
  acc="لوزالمعده")

T("آلرژی", "Allergy", "", AFG2,
  "Kept. Afghan hospital text uses «تداوی حساسیت های...» (حساسیت) for allergy, but in this book "
  "حساسیت is reserved for the DIFFERENT concept hypersensitivity/sensitivity («حساسیت فوری»، "
  "«حساسیت زیاد»), so replacing it would create a collision. آلرژی is a transliteration current in "
  "Afghanistan, not an Iranian-specific form. Do NOT register حساسیت as a variant here.",
  "Ch4/Ch5 (Type I hypersensitivity)", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("غشا", "Membrane", "", AFG2,
  "Orthographic variant only: غشا / غشاء. Both occur in Afghan and Iranian writing; the book uses "
  "غشا consistently (302 uses, غشاء 0). Purely a consistency note — no contamination involved.",
  "Whole book", "AFGHAN STANDARD", "HIGH", acc="غشاء")

T("پروتئین", "Protein", "", AFG2,
  "International transliteration; standard in Afghan medical writing. A simplified spelling "
  "پروتین occurs in Dari but is not the Afghan medical standard, so it is recorded only as an "
  "accepted variant, not as a preferred form.", "Whole book",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", acc="پروتین")

T("عفونت", "Infection", "", AFG2,
  "Kept. Afghan clinic register: «تداوی امراض مختلفه انتانی (عفونت، مکروبی)» — i.e. Afghan usage "
  "pairs the adjective انتانی (infectious; cf. «شفاخانه انتانی»، «امراض انتانی») with the noun "
  "عفونت, which is current in Afghanistan. Not registered as a variant of انتانی: different part "
  "of speech, so an INCONSIST flag would be meaningless.", "Ch3; Ch4; Ch5",
  "AFGHAN STANDARD", "MEDIUM")

T("لنفوئید", "Lymphoid", "", AFG2,
  "Afghan histology teaching uses لنفاوی for lymphatic (Afghan faculty text: «ندول لنفاوی»); the "
  "-oid adjective is لنفوئید. The book had split across لمفوئید (2), لمفاوی (2) and لنفاوی (21) — "
  "an internal split, not a second Afghan standard, so all three were unified. CONFIDENCE MEDIUM: "
  "no Afghan source was found that writes لنفوئیدی explicitly.", "Ch2; Ch4; Ch5",
  "AFGHAN STANDARD", "MEDIUM", acc="لمفوئید;لمفاوی")

# --------------------------------------------------------------------------
# Slot corrections applied at write time.
#
# Rationale: several entries originally parked a LATIN term or a legitimate
# Afghan synonym in the forbidden_forms slot. That produced false violations
# (cristae, entactin, غشای پلاسمایی, اسکلت حجروی ...). forbidden_forms is ONLY
# for forms that must never appear; Latin names belong in latin_term and
# Afghan synonyms in accepted_variants.
#
# key = dari_term ; value = (forbidden, accepted_variants, latin_term, new_dari)
# --------------------------------------------------------------------------
# ============================================================ CH6 — ADIPOSE ===
# Terms introduced by Chapter 6. None is constructed: each is either the established
# international/transliterated form used in medical education, an ordinary Dari word,
# or a phrase built from forms already canonical in this glossary.

T("نسج شحمی", "Adipose tissue", "", 
  "Composed of two forms already canonical in this glossary: نسج (Afghan MoE Grade-7 «انساج») "
  "+ شحمی (recorded here as the Afghan adjective for adipose/fatty). The assembled phrase was not "
  "located verbatim in an Afghan document, so this entry is MEDIUM confidence rather than HIGH. "
  "Nothing new was coined: no morpheme was translated and no compound was constructed.",
  "CANONICAL for this book. White adipose tissue = نسج شحمی سفید; brown = نسج شحمی قهوه‌ای. "
  "The English term follows in parentheses at first use in each chapter.",
  "Ch06; Ch05", "AFGHAN STANDARD", "MEDIUM")

T("ادیپوسیت", "Adipocyte", "", AFG,
  "Established international transliteration; no Afghanistan-specific documentary source located. "
  "The transparent Dari descriptor «حجره شحمی» may be used in running prose as an explanation "
  "(it is built from the canonical حجره + شحمی); it is not registered as a competing form because "
  "the text uses ادیپوسیت throughout.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("پری‌ادیپوسیت", "Preadipocyte", "", AFG,
  "Transliteration, consistent with ادیپوسیت.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لیپید", "Lipid", "", AFG,
  "Standard in Afghan medical writing (the book uses it throughout Ch1–Ch5). The ordinary Dari "
  "word چربی names the same substance in everyday and school usage and is NOT prohibited; the "
  "book uses لیپید where the scientific sense is meant.", "Whole book",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("تری‌گلیسرید", "Triglyceride", "", AFG,
  "Standard transliteration; the storage form of energy in adipocytes.", "Ch02; Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("گلیسرول", "Glycerol", "", AFG, "Transliteration.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اسیدهای شحمی", "Fatty acids", "", AFG,
  "Uses the canonical Afghan adjective شحمی. «اسیدهای چرب» (the ordinary-word form) is not "
  "prohibited but is not used as the scientific term in this book.", "Ch06",
  "AFGHAN STANDARD", "MEDIUM")

T("لیپولیز", "Lipolysis", "", AFG, "Transliteration.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لپتین", "Leptin", "", AFG,
  "Transliteration. Adipocyte hormone signalling energy stores to the hypothalamus.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("ادیپونکتین", "Adiponectin", "", AFG, "Transliteration.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("انسولین", "Insulin", "", AFG, "Transliteration.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کاتیکولامین", "Catecholamine", "", AFG,
  "Transliteration; spelled کاتیکولامین rather than the Persian کتکولامین.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("ترموجنین", "Thermogenin (UCP1)", "", AFG,
  "Transliteration. Uncoupling protein 1 of the inner mitochondrial membrane; the molecular basis "
  "of non-shivering thermogenesis in brown adipose tissue.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", lat="UCP1")

T("Unilocular", "Unilocular", "", AFG,
  "Retained in English: the term describes a single lipid droplet filling the cell, and no Afghan "
  "Dari form was located. «تک‌قطره‌ای» is NOT used — it would be a constructed compound.", "Ch06",
  "ENGLISH RETAINED", "MEDIUM")

T("Multilocular", "Multilocular", "", AFG,
  "Retained in English for the same reason as Unilocular. «چندقطره‌ای» is NOT used.", "Ch06",
  "ENGLISH RETAINED", "MEDIUM")

T("هیپوترمیا", "Hypothermia", "", AFG,
  "Transliteration, current in Afghan clinical writing.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("چاقی", "Obesity", "", AFG,
  "Ordinary Dari/Persian word, not a constructed compound; used for the clinical condition.", "Ch06",
  "AFGHAN STANDARD", "MEDIUM")

T("لیپوما", "Lipoma", "", AFG, "Transliteration; benign tumour of adipocytes.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لیپوسارکوم", "Liposarcoma", "", AFG,
  "Transliteration; malignant tumour of adipocytes.", "Ch06",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("هورمون", "Hormone", "", AFG2,
  "Standard transliteration, already used throughout Ch1–Ch5.", "Whole book",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

# ==================================================== CH7 — CARTILAGE ========
# Terms introduced by Chapter 7. غضروف and استخوان were already in use in Ch5.
# Nothing constructed: each is the established international/transliterated form
# used in medical education, an ordinary Dari word, or a phrase from forms already
# canonical here (غضروف + الیافی / هایالین / الاستیک).

T("غضروف", "Cartilage", "", AFG2,
  "Already used throughout Ch5 («انساجِ همبند تخصص‌یافته: غضروف، استخوان…»). Registered here as "
  "the chapter term. Ordinary Dari word, not a construction.",
  "Ch05; Ch07", "AFGHAN STANDARD", "HIGH")

T("کندروبلاست", "Chondroblast", "", AFG,
  "Established international transliteration; the immature cartilage-forming cell.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کندروسیت", "Chondrocyte", "", AFG,
  "Established international transliteration; the mature cartilage cell in its lacuna.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کندروژنیک", "Chondrogenic", "", AFG,
  "Transliteration; describes the chondrogenic layer of the perichondrium and the "
  "chondrogenic cells from which cartilage arises.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("پریکندریوم", "Perichondrium", "", AFG,
  "Transliteration. Retained rather than translating to a Dari compound. "
  "Not present on fibrocartilage or on articular surfaces.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لاکونا", "Lacuna", "", AFG,
  "Transliteration; the space in the matrix that houses a chondrocyte.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("غضروف هایالین", "Hyaline cartilage", "", AFG,
  "Assembled from the canonical غضروف + the established transliteration هایالین. "
  "The most common cartilage type. «شیشه‌ای» is the calque form and is NOT used.",
  "Ch07", "AFGHAN STANDARD", "MEDIUM")

T("غضروف الاستیک", "Elastic cartilage", "", AFG,
  "Canonical غضروف + established transliteration الاستیک.", "Ch07",
  "AFGHAN STANDARD", "MEDIUM")

T("غضروف الیافی", "Fibrocartilage", "", AFG,
  "Canonical غضروف + الیافی (the book's term for fibrous, from الیاف). The literal "
  "compound «فیبروکندریوم» is NOT used.", "Ch07", "AFGHAN STANDARD", "MEDIUM")

T("کندرویتین سلفات", "Chondroitin sulfate", "", AFG,
  "Transliteration; the main glycosaminoglycan of cartilage matrix.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کراتان سلفات", "Keratan sulfate", "", AFG, "Transliteration.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("آگرکان", "Aggrecan", "", AFG,
  "Transliteration; the large aggregating proteoglycan of cartilage matrix.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کندروکلسین", "Chondrocalcin", "", AFG,
  "Transliteration; a calcium-binding protein of cartilage matrix.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("پریکندریوم کندروژنیک", "Chondrogenic layer", "", AFG,
  "Composed of the canonical پریکندریوم + کندروژنیک.", "Ch07",
  "AFGHAN STANDARD", "MEDIUM")

T("Isogenous group", "Isogenous group", "", AFG,
  "RETAINED IN ENGLISH. This is the standard term for a cluster of chondrocytes derived "
  "from one cell. A Dari equivalent («گروه هم‌منشأ») would be constructed, so it is not used. "
  "May be introduced once with a short Dari explanation.", "Ch07",
  "ENGLISH RETAINED", "MEDIUM")

T("استئوآرتریت", "Osteoarthritis", "", AFG,
  "Transliteration; the clinical condition of cartilage degeneration.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("آکندروپلازی", "Achondroplasia", "", AFG,
  "Transliteration; the classic disorder of endochondral ossification.", "Ch07; Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کندروسارکوم", "Chondrosarcoma", "", AFG,
  "Transliteration; malignant tumour of cartilage.", "Ch07",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

# ======================================================== CH8 — BONE =========
# Terms introduced by Chapter 8. استخوان is already established (Ch5, Ch7).

T("استئوبلاست", "Osteoblast", "", AFG,
  "Established international transliteration; the bone-forming cell.", "Ch07; Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("استئوسیت", "Osteocyte", "", AFG,
  "Transliteration; the mature bone cell in its lacuna.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("استئوکلاست", "Osteoclast", "", AFG,
  "Transliteration; the multinucleated bone-resorbing cell of the monocyte/macrophage lineage.",
  "Ch08", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("استئوپروژنیتور", "Osteoprogenitor cell", "", AFG,
  "Transliteration; the precursor cell of the osteoblast lineage, found in the periosteum, "
  "endosteum and bone marrow.", "Ch08", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("استئوئید", "Osteoid", "", AFG,
  "Transliteration; the unmineralised organic bone matrix secreted by osteoblasts.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لاملا", "Lamella", "", AFG,
  "Transliteration; a layer of bone matrix. Compact bone is built of lamellae.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اوستئون", "Osteon (Haversian system)", "Haversian system", AFG,
  "Transliteration. The structural unit of compact bone: a central canal with its concentric "
  "lamellae. «دستگاه هاورس» is not used; the transliteration اوستئون is.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کانال هاورس", "Haversian canal", "", AFG,
  "Composed of the established transliteration کانال + the eponym Havers. The canal carries the "
  "vessels and nerves at the centre of each osteon.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کانال Volkmann", "Volkmann canal", "", AFG,
  "Eponym retained. These canals run transversely and connect Haversian canals to each other and "
  "to the marrow cavity.", "Ch08", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کانالیکولوس", "Canaliculus", "", AFG,
  "Transliteration; the narrow channel housing an osteocyte process. Plural کانالیکول‌ها.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("پریوست", "Periosteum", "", AFG,
  "Transliteration. The outer fibrous covering of bone; absent on articular surfaces.",
  "Ch08", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اندوست", "Endosteum", "", AFG,
  "Transliteration. The inner lining of the marrow cavity and osteonal canals.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("استخوان متراکم", "Compact bone", "", AFG,
  "Canonical استخوان + متراکم (already used in Ch5 for dense tissue).",
  "Ch08", "AFGHAN STANDARD", "MEDIUM")

T("استخوان اسفنجی", "Spongy bone", "", AFG,
  "Canonical استخوان + the ordinary Dari word اسفنجی. Also called Cancellous bone.",
  "Ch08", "AFGHAN STANDARD", "MEDIUM")

T("استخوان‌سازی اندوکندراﻝ", "Endochondral ossification", "", AFG,
  "Assembled from the canonical استخوان‌سازی + the established transliteration اندوکندراﻝ.",
  "Ch08", "AFGHAN STANDARD", "MEDIUM")

T("استخوان‌سازی داخل‌غشایی", "Intramembranous ossification", "", AFG,
  "Assembled from canonical استخوان‌سازی + داخل + غشایی. The literal compound "
  "«اینتراممبرانوس» is NOT used.", "Ch08", "AFGHAN STANDARD", "MEDIUM")

T("صفحهٔ اپی‌فیز", "Epiphyseal plate", "", AFG,
  "Composed of the established transliteration اپی‌فیز + صفحه. The growth plate of a long bone.",
  "Ch08", "AFGHAN STANDARD", "MEDIUM")

T("مغز استخوان", "Bone marrow", "", AFG2,
  "Ordinary Dari compound, already used in Ch5 («مغز استخوان»).", "Ch05; Ch08",
  "AFGHAN STANDARD", "MEDIUM")

T("هادروکسی‌اپاتیت", "Hydroxyapatite", "",
  AFG, "Transliteration; the calcium phosphate mineral of bone matrix.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اوستئوپتروز", "Osteopetrosis", "", AFG,
  "Transliteration; the disease of failed osteoclast resorption.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اوستئوپوروز", "Osteoporosis", "", AFG,
  "Transliteration; the common disease of reduced bone mass and microarchitectural deterioration.",
  "Ch08", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("راشیتیسم", "Rickets", "", AFG,
  "Transliteration; defective mineralisation of growing bone due to vitamin D deficiency.",
  "Ch08", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("استئومالاسی", "Osteomalacia", "", AFG,
  "Transliteration; defective mineralisation in adults.", "Ch08",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

# ================================================ CH9 — BLOOD / MARROW =======
# Terms introduced by Chapter 9.

T("خون", "Blood", "", AFG2,
  "Ordinary Dari word; the tissue is a specialized connective tissue with a fluid matrix "
  "(پلاسما) and formed elements.", "Ch09", "AFGHAN STANDARD", "MEDIUM")

T("پلاسما", "Plasma", "", AFG,
  "Transliteration. The fluid matrix of blood: water, پروتئین‌ها, electrolytes.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("سیرم", "Serum", "", AFG,
  "Transliteration; plasma without its clotting factors.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اریتروسیت", "Erythrocyte (RBC)", "", AFG,
  "Transliteration. The book keeps the international form; the descriptive Dari phrase "
  "«گویچهٔ سرخ» is the Iranian form and is NOT used. «کرویات سفید» (Afghan faculty histology "
  "text) is used only as an explanatory gloss.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", abbr="RBC")

T("لکوسیت", "Leukocyte (WBC)", "", AFG,
  "Transliteration. «گویچهٔ سفید» is the Iranian form and is NOT used; «کرویات سفید خون» is "
  "recorded in the Afghan faculty histology text and may serve as an explanatory gloss.",
  "Ch09", "COMMON AFGHAN TRANSLITERATION", "MEDIUM", abbr="WBC")

T("ترومبوسیت", "Platelet (thrombocyte)", "", AFG,
  "Transliteration. Cell fragments of megakaryocyte cytoplasm, not whole cells.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("هموگلوبین", "Hemoglobin", "", AFG,
  "Transliteration; the oxygen-carrying protein of erythrocytes. The abbreviation Hb is "
  "part of the term (HbA, HbF), not a separate forbidden form.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", abbr="Hb")

T("هماتوکریت", "Hematocrit", "", AFG,
  "Transliteration; the packed cell volume of blood.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", abbr="Hct")

T("نوتروفیل", "Neutrophil", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("ائوزینوفیل", "Eosinophil", "", AFG,
  "Transliteration. «اسیدوفیل» is not used.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("بازوفیل", "Basophil", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لنفوسیت", "Lymphocyte", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("مونوسیت", "Monocyte", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("مگاکاریوسیت", "Megakaryocyte", "", AFG,
  "Transliteration; the giant polyploid marrow cell that sheds platelets.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("هماتوپویزیس", "Hemopoiesis", "", AFG,
  "Transliteration. The book uses هماتوپویزیس (or خون‌سازی as the plain Dari gloss).", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("خون‌سازی", "Hemopoiesis (Dari gloss)", "", AFG2,
  "Ordinary Dari gloss used alongside the transliteration هماتوپویزیس; already used in Ch5.",
  "Ch05; Ch09", "AFGHAN STANDARD", "MEDIUM")

T("اریتروپویزین", "Erythropoietin", "", AFG,
  "Transliteration; the kidney-derived hormone driving erythrocyte production.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", abbr="EPO")

T("هموستاز", "Hemostasis", "", AFG,
  "Transliteration; the arrest of bleeding.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("فیبرین", "Fibrin", "", AFG,
  "Transliteration; the polymerised product of fibrinogen that forms the clot.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("فیبرینوژن", "Fibrinogen", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("رتیکولوسیت", "Reticulocyte", "", AFG,
  "Transliteration; the immature erythrocyte that still contains residual ribosomes.",
  "Ch09", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("آنمی", "Anemia", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لوسمی", "Leukemia", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("ترومبوسیتوپنی", "Thrombocytopenia", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("هموفیلی", "Hemophilia", "", AFG, "Transliteration.", "Ch09",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

# ======================================================= CH10 — MUSCLE =======
T("عضله", "Muscle", "", AFG2,
  "Ordinary Dari word. Muscle tissue is classified into skeletal, cardiac and smooth types.",
  "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("میوسیت", "Myocyte (muscle cell)", "", AFG,
  "Transliteration; the muscle cell, whether striated or smooth.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("سارکولما", "Sarcolemma", "", AFG,
  "Transliteration; the muscle cell membrane plus its external lamina.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("سارکوپلاسم", "Sarcoplasm", "", AFG,
  "Transliteration; the cytoplasm of a muscle cell.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("سارکومر", "Sarcomere", "", AFG,
  "Transliteration; the contractile unit between two Z discs.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اکتین", "Actin", "", AFG, "Transliteration; the thin filament protein.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("میوزین", "Myosin", "", AFG, "Transliteration; the thick filament protein.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("تروپومیوزین", "Tropomyosin", "", AFG, "Transliteration.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("تروپونین", "Troponin", "", AFG,
  "Transliteration; the calcium-binding regulatory complex on the thin filament.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("دیسک Z", "Z disc", "Z line", AFG,
  "Composed of the established transliteration دیسک + the letter Z. The boundary of a sarcomere.",
  "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("نوار A", "A band", "", AFG,
  "Composed of نوار + the letter A. The dark band spanning the length of the thick filaments.",
  "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("نوار I", "I band", "", AFG,
  "Composed of نوار + the letter I. The light band containing only thin filaments, bisected by the "
  "Z disc.", "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("نوار H", "H band", "", AFG,
  "Composed of نوار + the letter H. The lighter central region of the A band containing only thick "
  "filaments.", "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("خط M", "M line", "", AFG,
  "Composed of خط + the letter M. The midline of the H band where thick filaments are cross-linked.",
  "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("تیوبول T", "T tubule", "", AFG,
  "Composed of تیوبول + T. The invagination of the sarcolemma carrying the action potential inward.",
  "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("شبکهٔ سارکوپلاسمی", "Sarcoplasmic reticulum", "", AFG,
  "Composed of the canonical شبکهٔ + the established transliteration سارکوپلاسمی. Stores calcium.",
  "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("دیاد", "Diad", "", AFG,
  "Transliteration; one T tubule plus one terminal cisterna, at the cardiac Z disc.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("تریاد", "Triad", "", AFG,
  "Transliteration; one T tubule plus two terminal cisternae, at the skeletal A-I junction.",
  "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کاوئولا", "Caveola", "", AFG,
  "Transliteration; the surface invagination of smooth muscle that substitutes for T tubules.",
  "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("عضله اسکلتی", "Skeletal muscle", "", AFG2,
  "Canonical عضله + the ordinary word اسکلتی (already used in Ch1 for skeletal system).",
  "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("عضله قلبی", "Cardiac muscle", "", AFG2,
  "Canonical عضله + the ordinary word قلبی.", "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("عضله صاف", "Smooth muscle", "", AFG2,
  "Canonical عضله + the ordinary word صاف (already used in Ch2 for smooth ER).",
  "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("مخطط", "Striated", "", AFG2,
  "Ordinary Dari word for the striated appearance of skeletal and cardiac muscle; already used in "
  "Ch2 in the same sense.", "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("املس", "Non-striated", "", AFG2,
  "Established Dari descriptor for smooth muscle (عضلهٔ املس); not a construction.",
  "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("دیسک میان‌حجروی", "Intercalated disc", "", AFG,
  "Composed of دیسک + میان‌حجروی (already canonical in Ch4). The junctional complex joining "
  "adjacent cardiac muscle cells.", "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("مایوگلوبین", "Myoglobin", "", AFG,
  "Transliteration; the oxygen-binding protein of muscle.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("استیل‌کولین", "Acetylcholine", "ACh", AFG,
  "Transliteration; the neurotransmitter at the neuromuscular junction.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("صفحهٔ محرکهٔ عصبی-عضلانی", "Neuromuscular junction", "", AFG2,
  "Composed of established Dari terms: صفحه (as in صفحهٔ اپی‌فیز) + محرکهٔ عصبی-عضلانی.",
  "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("واحدِ محرکهٔ عضلانی", "Motor unit", "", AFG2,
  "Composed of ordinary Dari words. One motor neuron and all the muscle fibers it innervates.",
  "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("عضلهٔ دوکی", "Spindle (muscle shape)", "", AFG2,
  "Ordinary Dari descriptor for the spindle or fusiform shape of smooth muscle cells.",
  "Ch10", "AFGHAN STANDARD", "MEDIUM")

T("دیستروفی عضلانی", "Muscular dystrophy", "", AFG2,
  "Canonical عضلانی + the established transliteration دیستروفی.", "Ch10",
  "AFGHAN STANDARD", "MEDIUM")

T("میاستنی گراو", "Myasthenia gravis", "", AFG,
  "Transliteration.", "Ch10", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("مایوپاتی", "Myopathy", "", AFG, "Transliteration.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("رگور مورتیس", "Rigor mortis", "", AFG, "Transliteration.", "Ch10",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

# ====================================================== CH11 — NERVOUS ======
T("نیوروگلیا", "Neuroglia (glial cells)", "", AFG,
  "Transliteration; the non-excitable supporting cells of nervous tissue.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("آکسون", "Axon", "", AFG,
  "Transliteration; the single long process that conducts impulses away from the cell body.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("دندریت", "Dendrite", "", AFG,
  "Transliteration; the branched processes that receive impulses.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("میلین", "Myelin", "", AFG,
  "Transliteration; the lipid-rich insulating sheath around axons.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("غلافِ میلین", "Myelin sheath", "", AFG,
  "Composed of the canonical غلاف + the established transliteration میلین.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("حجرهٔ شوان", "Schwann cell", "", AFG,
  "Composed of canonical حجرهٔ + the established name شوان. Myelin-forming cell of the peripheral "
  "nervous system.", "Ch11", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("الیگودندروسیت", "Oligodendrocyte", "", AFG,
  "Transliteration; the myelin-forming cell of the central nervous system.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("آستروسیت", "Astrocyte", "", AFG,
  "Transliteration; the largest and most numerous glial cell; forms the blood-brain barrier "
  "framework and a repair scar.", "Ch11", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("میکروگلیا", "Microglia", "", AFG,
  "Transliteration; the small phagocytic glial cell of monocytic origin.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اپندیم", "Ependyma", "", AFG,
  "Transliteration; the ciliated epithelial lining of the brain ventricles and central canal.",
  "Ch11", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("گرهٔ رانویه", "Node of Ranvier", "", AFG,
  "Composed of canonical گرهٔ + the established name رانویه. The unmyelinated gap between two "
  "myelinating cells where saltatory conduction occurs.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("سیناپس", "Synapse", "", AFG,
  "Transliteration; the junction between two neurons or a neuron and an effector cell.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("سیناپسِ کیمیاوی", "Chemical synapse", "", AFG,
  "Composed of the canonical سیناپس + the canonical adjective کیمیاوی (the established Afghan form for chemical).", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("نوروترانسمیتر", "Neurotransmitter", "", AFG,
  "Transliteration; the chemical messenger released at a chemical synapse.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("جسمِ نیسل", "Nissl body", "", AFG,
  "Composed of the ordinary word جسم + the established name نیسل. Stacks of rough ER in the "
  "neuronal perikaryon.", "Ch11", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("نوروفیلامنت", "Neurofilament", "", AFG,
  "Transliteration; the intermediate filament of neurons.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("مادهٔ خاکستری", "Gray matter", "", AFG2,
  "Composed of canonical مادهٔ + the ordinary word خاکستری (already used in Ch4). Neuronal cell "
  "bodies, dendrites and synapses.", "Ch11", "AFGHAN STANDARD", "MEDIUM")

T("مادهٔ سفید", "White matter", "", AFG2,
  "Composed of canonical مادهٔ + the ordinary word سفید. Myelinated axons and glial cells.",
  "Ch11", "AFGHAN STANDARD", "MEDIUM")

T("نخاع", "Spinal cord", "", AFG2,
  "Ordinary Dari word for the spinal cord.", "Ch11", "AFGHAN STANDARD", "MEDIUM")

T("الیافِ عصبی", "Nerve fibres", "", AFG2,
  "Composed of الیاف (already used in Ch1) + the ordinary adjective عصبی.", "Ch11",
  "AFGHAN STANDARD", "MEDIUM")

T("عصبِ محیطی", "Peripheral nerve", "", AFG2,
  "Composed of the ordinary words عصب + محیطی (already canonical in Ch4). A bundle of nerve "
  "fibres with its connective tissue sheaths.", "Ch11", "AFGHAN STANDARD", "MEDIUM")

T("اندونوریوم", "Endoneurium", "", AFG,
  "Transliteration; the connective tissue sheath around each individual nerve fibre.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("پرینوریوم", "Perineurium", "", AFG,
  "Transliteration; the connective tissue sheath around each nerve fascicle.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اپینوریوم", "Epineurium", "", AFG,
  "Transliteration; the connective tissue sheath around the whole nerve.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("حاجزِ خون-مغز", "Blood-brain barrier", "", AFG2,
  "Composed of established Dari terms: حاجز (a barrier, as in the haemostatic barrier sense) + "
  "the ordinary words خون and مغز.", "Ch11", "AFGHAN STANDARD", "MEDIUM")

T("شبکهٔ کوروئید", "Choroid plexus", "", AFG2,
  "Composed of canonical شبکهٔ + the established transliteration کوروئید. The ependymal-plus-"
  "capillary structure that secretes cerebrospinal fluid.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("مایعِ دماغی-نخاعی", "Cerebrospinal fluid (CSF)", "", AFG2,
  "Composed of established Dari terms; مایع (as in مایعِ خارج‌حجروی) + دماغی-نخاعی. The fluid of "
  "the ventricles and subarachnoid space.", "Ch11", "AFGHAN STANDARD", "MEDIUM", abbr="CSF")

T("غلافِ معدومِ میلین", "Unmyelinated", "", AFG2,
  "Descriptive Dari phrase: a fibre without a myelin sheath.", "Ch11",
  "AFGHAN STANDARD", "MEDIUM")

T("عصبِ‌زخمِ محیطی", "Peripheral nerve injury", "", AFG2,
  "Descriptive Dari phrase used in the clinical section.", "Ch11", "AFGHAN STANDARD", "MEDIUM")

T("دژنراسیون والرین", "Wallerian degeneration", "", AFG,
  "Transliteration; degeneration of the distal axon segment after nerve injury.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("مرضِ مالتیپل اسکلروزیس", "Multiple sclerosis", "", AFG2,
  "Composed of the established Dari مرض + the international term, which is what clinical practice "
  "uses. Autoimmune demyelination of the central nervous system.", "Ch11",
  "ENGLISH RETAINED", "MEDIUM", abbr="MS")

T("پارکینسون", "Parkinson disease", "", AFG,
  "Transliteration; degeneration of dopaminergic neurons of the substantia nigra.", "Ch11",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("الصاقِ عصبی", "Nervous tissue repair", "", AFG2,
  "Descriptive Dari phrase for the regeneration section.", "Ch11", "AFGHAN STANDARD", "LOW")

# ============================================ CH12 — CARDIOVASCULAR ==========
T("قلب", "Heart", "", AFG2,
  "Ordinary Dari word. The muscular pump of the circulatory system.", "Ch12",
  "AFGHAN STANDARD", "MEDIUM")

T("اندوکارد", "Endocardium", "", AFG,
  "Transliteration; the innermost layer of the heart wall, continuous with the endothelium of the "
  "great vessels.", "Ch12", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("میوکارد", "Myocardium", "", AFG,
  "Transliteration; the thick middle layer of cardiac muscle of the heart wall.", "Ch12",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اپی‌کارد", "Epicardium", "", AFG,
  "Transliteration; the outer layer of the heart wall, which is the visceral layer of the "
  "pericardium.", "Ch12", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("پریکارد", "Pericardium", "", AFG,
  "Transliteration; the serous sac surrounding the heart, with a parietal and a visceral layer.",
  "Ch12", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اندوتلیوم", "Endothelium", "", AFG,
  "Transliteration; the simple squamous epithelium lining the heart and all vessels.", "Ch12",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("کاپیلار", "Capillary", "", AFG,
  "Transliteration retained alongside the established Dari compound موی‌رگ. Ch1-Ch11 use موی‌رگ "
  "as the primary form; both are listed so the reader meets the term in either shape.", "Ch12",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", lat="capillary")

T("آئورت", "Aorta", "", AFG,
  "Transliteration; the largest elastic artery.", "Ch12",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لایهٔ درونی", "Tunica intima", "", AFG2,
  "Descriptive Dari layer name; the Latin term is retained beside it. The innermost vessel layer.",
  "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("لایهٔ میانی", "Tunica media", "", AFG2,
  "Descriptive Dari layer name; the Latin term is retained beside it. The smooth muscle layer.",
  "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("لایهٔ بیرونی", "Tunica adventitia", "", AFG2,
  "Descriptive Dari layer name; the Latin term is retained beside it. The outer connective tissue "
  "layer.", "Ch12", "AFGHAN STANDARD", "MEDIUM", lat="tunica adventitia")

T("دریچه", "Valve", "", AFG2,
  "Ordinary Dari word for a valve, including the cardiac valves.", "Ch12",
  "AFGHAN STANDARD", "MEDIUM")

T("پری‌سیت", "Pericyte", "", AFG,
  "Transliteration; the contractile cell of the capillary wall sharing a basal lamina with the "
  "endothelium.", "Ch12", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("آترواسکلروزیس", "Atherosclerosis", "", AFG,
  "Transliteration; the commonest form of arteriosclerosis, with intimal lipid plaques.", "Ch12",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("فشارِ خونِ بلند", "Hypertension", "", AFG2,
  "Descriptive Dari phrase built from established terms (فشار, خون, بلند); the clinical register "
  "in Afghanistan also says 'فشارِ بلند'.", "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("ساینوسویید", "Sinusoid", "", AFG,
  "Transliteration; the wide, discontinuous, fenestrated capillary of liver, spleen and bone "
  "marrow.", "Ch12", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("آنستوموز", "Anastomosis", "", AFG,
  "Transliteration; a communication between two vessels.", "Ch12",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("موی‌رگچهٔ پس‌مویِرگی", "Postcapillary venule", "", AFG2,
  "Composed of the canonical named parts: موی‌رگچه (diminutive) + پس (post) + مویِرگی. The site "
  "where leukocytes leave the blood.", "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("شبکهٔ موی‌رگی", "Capillary bed", "microcirculation", AFG2,
  "Composed of canonical شبکهٔ + موی‌رگی. The exchange network between an arteriole and a venule.",
  "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("لایهٔ زیرِ اندوتلیالی", "Subendothelial layer", "", AFG2,
  "Composed of the canonical لایهٔ + the established adjective زیرِ اندوتلیالی; the loose "
  "connective tissue of the intima.", "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("دریچه‌های نیم‌هلالی", "Semilunar valves", "", AFG2,
  "Composed of canonical دریچه + the ordinary word نیم‌هلالی; the aortic and pulmonary valves.",
  "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("دستگاهِ هدایتِ قلب", "Cardiac conduction system", "", AFG2,
  "Composed of established Dari terms; the nodal and Purkinje fibre network of the heart.",
  "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("شریانِ مرکزی", "Central artery", "", AFG2,
  "Composed of canonical شریان + the ordinary word مرکزی; the artery of the splenic white pulp "
  "and of the red pulp trabeculae.", "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("وریدِ صافانی", "Splenic vein", "", AFG2,
  "Composed of canonical ورید + the established adjective صافانی (splenic).", "Ch12",
  "AFGHAN STANDARD", "LOW")

T("سکتهٔ قلبی", "Myocardial infarction", "heart attack", AFG2,
  "Descriptive Dari phrase in everyday clinical use for myocardial infarction; the term "
  "انفارکتوس is also current.", "Ch12", "AFGHAN STANDARD", "MEDIUM")

T("تومورِ عروقی", "Vascular tumour", "", AFG2,
  "Composed of the established transliteration تومور + the ordinary adjective عروقی (vascular).",
  "Ch12", "AFGHAN STANDARD", "LOW")

T("همانژیوم", "Hemangioma", "", AFG,
  "Transliteration; the common benign vascular tumour.", "Ch12",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("وارِیس", "Varicose vein", "varicose veins", AFG,
  "Transliteration in clinical use for dilated, incompetent superficial veins.", "Ch12",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

# ================================================ CH13 — LYMPHATIC =========
T("لیمف", "Lymph", "", AFG,
  "Transliteration; the interstitial fluid carried by lymphatic vessels. Ch13 onward uses لیمف "
  "consistently; the adjective is لیمفاوی.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", lat="lymph")

T("لیمفاوی", "Lymphatic", "", AFG,
  "Adjective formed from the canonical noun لیمف.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("عقدۀ لیمفاوی", "Lymph node", "lymph gland", AFG,
  "Composed of the ordinary word عقدۀ + the canonical لیمفاوی. The encapsulated filter organ of "
  "the lymphatic system.", "Ch13", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لیمفوسیت", "Lymphocyte", "", AFG,
  "Transliteration; already introduced in Ch9 as لنفوسیت. The single canonical form used in this "
  "book is لنفوسیت, as registered in the Ch9 row; this row records the alternative transliteration "
  "that some Afghan texts print, without making it canonical.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "LOW")

T("تیموس", "Thymus", "", AFG,
  "Transliteration; the primary lymphoid organ behind the sternum.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("صفال", "Spleen", "", AFG2,
  "Established Dari word for the spleen, already used in Ch9 and Ch12.", "Ch13",
  "AFGHAN STANDARD", "MEDIUM")

T("مغزِ استخوان", "Bone marrow", "", AFG2,
  "Composed of the ordinary words مغز + استخوان (canonical from Ch8).", "Ch13",
  "AFGHAN STANDARD", "MEDIUM")

T("لوزه", "Tonsil", "", AFG2,
  "Ordinary Dari word; the tonsils are MALT organs of the pharynx.", "Ch13",
  "AFGHAN STANDARD", "MEDIUM")

T("لوزهٔ معدی", "Gastric tonsil", "", AFG2,
  "Composed of the canonical لوزه + the ordinary word معدی.", "Ch13",
  "AFGHAN STANDARD", "LOW")

T("MALT", "Mucosa-associated lymphoid tissue", "", AFG,
  "International abbreviation retained, as everywhere in the medical literature and teaching.",
  "Ch13", "COMMON AFGHAN TRANSLITERATION", "MEDIUM", abbr="MALT")

T("پلاسموسیت", "Plasma cell", "", AFG,
  "Transliteration; the antibody-secreting descendant of a B lymphocyte.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("حجراتِ دندریتیک", "Dendritic cells", "", AFG2,
  "Composed of canonical حجرات + the established transliteration دندریتیک (the same root as "
  "دندریت in Ch11). The major antigen-presenting cells.", "Ch13",
  "AFGHAN STANDARD", "MEDIUM")

T("مرکزِ زاینده", "Germinal centre", "", AFG2,
  "Descriptive Dari phrase built from established words; the site of B-cell proliferation in a "
  "secondary follicle.", "Ch13", "AFGHAN STANDARD", "MEDIUM")

T("مرکزِ ثانویه", "Secondary nodule", "", AFG2,
  "Composed of the established مرکز + the transliteration ثانویه; a nodule with a germinal centre.",
  "Ch13", "AFGHAN STANDARD", "MEDIUM")

T("وریدچهٔ پس‌مویِرگیِ پُرمکعب", "High endothelial venule (HEV)", "", AFG2,
  "Descriptive Dari phrase built from canonical parts (وریدچهٔ پس‌مویِرگی from Ch12 + پُرمکعب) plus "
  "the international abbreviation HEV.", "Ch13", "AFGHAN STANDARD", "MEDIUM", abbr="HEV", lat="postcapillary venule")

T("ایمونوگلوبولین", "Immunoglobulin", "", AFG,
  "Transliteration; the antibody molecule secreted by plasma cells.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", lat="antibody, immunoglobulin")

T("لوزهٔ حلقی", "Pharyngeal tonsil", "", AFG2,
  "Composed of the canonical لوزه + the ordinary word حلقی.", "Ch13",
  "AFGHAN STANDARD", "MEDIUM", lat="pharyngeal tonsil, adenoid")

T("صافانِ لیمفاوی", "Lymphatic nodule", "", AFG2,
  "Descriptive Dari phrase; the nodular lymphoid tissue inside lymph nodes, spleen and tonsils.",
  "Ch13", "AFGHAN STANDARD", "LOW")

T("دستگاهِ لیمفاوی", "Lymphatic system", "", AFG2,
  "Composed of the canonical adjective لیمفاوی + دستگاه.", "Ch13",
  "AFGHAN STANDARD", "MEDIUM")

T("لیمفادِنیت", "Lymphadenitis", "", AFG,
  "Transliteration; inflammation of a lymph node.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لیمفوما", "Lymphoma", "", AFG,
  "Transliteration; malignant tumour of lymphoid tissue.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("مرضِ هوچکین", "Hodgkin lymphoma", "Hodgkin disease", AFG2,
  "Composed of the established مرض + the established name هوچکین.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("تیموما", "Thymoma", "", AFG,
  "Transliteration; tumour of the thymic epithelium.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("اسپلنومگالی", "Splenomegaly", "", AFG,
  "Transliteration; enlargement of the spleen.", "Ch13",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("لوسمی", "Leukemia", "", AFG,
  "Transliteration; already registered in Ch9; repeated here because Chapter 13 introduces the "
  "marrow as a lymphoid organ.", "Ch13", "COMMON AFGHAN TRANSLITERATION", "LOW")

# ================================================= CH14 — ORAL CAVITY =======
T("حفرهٔ دهن", "Oral cavity", "", AFG2,
  "Composed of the ordinary Dari words حفرهٔ + دهن. The mouth and its contents.", "Ch14",
  "AFGHAN STANDARD", "MEDIUM", lat="oral cavity")

T("مخاطِ دهن", "Oral mucosa", "", AFG2,
  "Composed of مخاط (already canonical in Ch4 as mucosa) + دهن. The lining of the oral cavity.",
  "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("مخاطِ پوشاننده", "Lining mucosa", "", AFG2,
  "Descriptive Dari phrase for the non-keratinized protective lining of most of the oral cavity.",
  "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("مخاطِ جویده‌شونده", "Masticatory mucosa", "", AFG2,
  "Descriptive Dari phrase for the keratinized mucosa of the gums and hard palate, exposed to "
  "chewing forces.", "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("مخاطِ مخصوص", "Specialized mucosa", "", AFG2,
  "Descriptive Dari phrase for the mucosa of the dorsum of the tongue carrying taste buds.", "Ch14",
  "AFGHAN STANDARD", "MEDIUM")

T("زبان", "Tongue", "", AFG2,
  "Ordinary Dari word; a muscular organ covered by specialized mucosa.", "Ch14",
  "AFGHAN STANDARD", "MEDIUM")

T("پاپیلا", "Papilla", "", AFG,
  "Transliteration; the projections of the lingual epithelium. Plural: پاپیل‌ها (papillae).", "Ch14",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("پرزِ چشایی", "Taste bud", "", AFG2,
  "Composed of the ordinary word پرز in the sense of a small cluster + the established adjective "
  "چشایی (of taste).", "Ch14", "AFGHAN STANDARD", "MEDIUM", lat="taste bud")

T("دندان", "Tooth", "", AFG2,
  "Ordinary Dari word.", "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("مینا", "Enamel", "", AFG,
  "Transliteration of the international dental term retained; the Dari literature also writes مینا. "
  "The hardest, most highly mineralized tissue of the body.", "Ch14",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM", lat="enamel")

T("دنتین", "Dentin", "dentine", AFG,
  "Transliteration; the mineralized tissue forming the bulk of the tooth and surrounding the pulp.",
  "Ch14", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("سیمانِ دندان", "Cementum", "", AFG2,
  "Composed of the established transliteration سیمان + the ordinary word دندان; the bone-like "
  "covering of the root.", "Ch14", "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("مغزِ دندان", "Dental pulp", "", AFG2,
  "Descriptive Dari phrase built from the ordinary words مغز + دندان; the soft tissue core of the "
  "tooth.", "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("دنتینوژنیک", "Odontogenic", "odontogenic", AFG,
  "Transliteration used for cells that form dentin and enamel.", "Ch14",
  "COMMON AFGHAN TRANSLITERATION", "LOW")

T("غددِ لعابی", "Salivary glands", "", AFG2,
  "Composed of غدد (already canonical in Ch4) + the established adjective لعابی from لعاب (saliva).",
  "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("لعاب", "Saliva", "", AFG2,
  "Established Dari word for saliva; the adjective is لعابی.", "Ch14",
  "AFGHAN STANDARD", "MEDIUM")

T("غدهٔ بناگوشی", "Parotid gland", "", AFG2,
  "Descriptive Dari phrase for the gland beside the ear (بناگوش). The largest salivary gland and "
  "the one that becomes inflamed in mumps.", "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("غدهٔ زیرِ فکِ تحتانی", "Submandibular gland", "", AFG2,
  "Descriptive Dari phrase composed of established parts.", "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("غدهٔ زیرِ زبان", "Sublingual gland", "", AFG2,
  "Descriptive Dari phrase composed of established parts.", "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("لابول", "Lobule", "", AFG,
  "Transliteration; the structural unit of a salivary gland.", "Ch14",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM")

T("دورهٔ توبول", "Duct", "", AFG2,
  "Descriptive Dari phrase; the ducts of salivary glands (intercalated, striated, interlobular).",
  "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("حجرهٔ موکوسی", "Mucous cell", "", AFG2,
  "Composed of canonical حجرهٔ + the transliteration موکوسی; pale, mucin-secreting acinar cells.",
  "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("حجرهٔ سیروزی", "Serous cell", "", AFG2,
  "Composed of canonical حجرهٔ + the transliteration سیروزی; dark, protein-rich secreting acinar "
  "cells.", "Ch14", "AFGHAN STANDARD", "MEDIUM")

T("پوسیدگیِ دندان", "Dental caries", "tooth decay", AFG2,
  "Descriptive Dari phrase built from established words; the commonest disease of teeth.", "Ch14",
  "AFGHAN STANDARD", "MEDIUM")

T("شورهٔ دندان", "Dental plaque", "", AFG2,
  "Descriptive Dari phrase; the bacterial film on teeth. The bare English word plaque is not restricted, since it also denotes the amyloid and atherosclerotic plaques discussed in Chapters 11 and 12.", "Ch14", "AFGHAN STANDARD", "MEDIUM", lat="dental plaque")

T("مرضِ پریودنتال", "Periodontal disease", "gum disease", AFG2,
  "Composed of the established مرض + the transliteration پریودنتال.", "Ch14",
  "AFGHAN STANDARD", "MEDIUM")

T("اوریون", "Mumps", "epidemic parotitis", AFG2,
  "Established Dari word for epidemic parotitis with parotid swelling.", "Ch14",
  "AFGHAN STANDARD", "MEDIUM")

T("سرطانِ دهان", "Oral cancer", "", AFG2,
  "Composed of the established words سرطان + دهان (ordinary Dari form of mouth used in the "
  "clinical register).", "Ch14", "AFGHAN STANDARD", "MEDIUM")

# ============================================= CH15 — DIGESTIVE TRACT =======
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("لولهٔ گوارش", "Digestive tract", "", "", "",
  "Composed of the established words لوله + گوارش; the alimentary canal.", "AFGHAN STANDARD", "MEDIUM"),
 ("مخاطِ معدی-روده‌ای", "Gastrointestinal mucosa", "", "", "",
  "Descriptive Dari phrase; the mucosal layer of the digestive tube.", "AFGHAN STANDARD", "MEDIUM"),
 ("چینِ مخاطی", "Mucosal fold", "plica", "", "",
  "Composed of established Dari words; the folds of the digestive mucosa.", "AFGHAN STANDARD", "MEDIUM"),
 ("عضلهٔ مخاطی", "Muscularis mucosae", "", "", "",
  "Composed of the canonical عضله + مخاطی; the thin smooth muscle layer of the mucosa.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("لایهٔ زیرِ مخاطی", "Submucosa", "", "", "",
  "Composed of the canonical لایهٔ + زیرِ مخاطی (the pattern used in Ch12 for vessel layers).",
  "AFGHAN STANDARD", "MEDIUM"),
 ("لایهٔ عضلانیِ خارجی", "Muscularis externa", "", "", "",
  "Descriptive Dari layer name, as in Ch12; the two-plane smooth muscle coat.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("شبکهٔ عصبیِ زیرِ مخاطی", "Submucosal (Meissner) plexus", "plexus submucosus", "", "",
  "Descriptive Dari phrase + the international name; the enteric nervous system is described as "
  "شبکهٔ عصبیِ روده‌ای.", "AFGHAN STANDARD", "MEDIUM"),
 ("شبکهٔ عصبیِ عضلانی", "Myenteric (Auerbach) plexus", "plexus myentericus", "", "",
  "Descriptive Dari phrase for the plexus between the two muscle layers.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("شبکهٔ عصبیِ روده‌ای", "Enteric nervous system", "ENS", "ENS", "",
  "Composed of canonical شبکهٔ عصبی + the ordinary adjective روده‌ای.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("مری", "Esophagus", "oesophagus", "", "",
  "Ordinary Dari word.", "AFGHAN STANDARD", "MEDIUM"),
 ("معده", "Stomach", "", "", "", "Ordinary Dari word.", "AFGHAN STANDARD", "MEDIUM"),
 ("کاردیا", "Cardia", "", "", "", "Transliteration; the transition zone at the esophageal opening.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("فوندوس", "Fundus", "", "", "", "Transliteration; the dome of the stomach above the cardia.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("جسمِ معده", "Body of stomach", "", "", "", "Composed of the ordinary words جسم + معده.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("پیلور", "Pylorus", "", "", "", "Transliteration; the distal sphincter region of the stomach.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("چینِ معدی", "Gastric ruga", "rugae", "", "",
  "Composed of the canonical چین + معدی; the longitudinal gastric folds.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حفرهٔ معدی", "Gastric pit", "foveola gastrica", "", "",
  "Descriptive Dari phrase; the epithelial invagination into which gastric glands open.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("غدهٔ معدی", "Gastric gland", "", "", "",
  "Composed of the canonical غده + معدی.", "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ پاریتال", "Parietal cells", "cellulae parietales", "", "",
  "Transliteration retained (the international histological term); they secrete HCl and intrinsic "
  "factor.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ زیموژنیک", "Chief cells", "zymogenic cells", "", "",
  "Transliteration retained; they secrete pepsinogen.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ انترواندوکراین", "Enteroendocrine cells", "", "", "",
  "Transliteration retained; the amine- and peptide-secreting cells of the gut.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("رودهٔ باریک", "Small intestine", "", "", "", "Composed of the ordinary words رودهٔ + باریک.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("دوازده‌گرهای", "Duodenum", "duodenum", "", "",
  "Established Dari name for the duodenum (the traditional, non-constructed form).",
  "AFGHAN STANDARD", "MEDIUM"),
 ("ژژونوم", "Jejunum", "", "", "", "Transliteration.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ایلئوم", "Ileum", "", "", "", "Transliteration.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ویلوس", "Villus", "villi intestinales", "", "",
  "Transliteration retained; the finger-like projections of small-intestinal mucosa.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("کریپتِ لیبرکوهن", "Crypt of Lieberkühn", "", "", "",
  "Composed of the established transliteration کریپت + the eponym.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ پانیت", "Paneth cells", "", "", "",
  "Transliteration retained; the antibacterial-enzyme-secreting cells at the crypt base.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("صفحهٔ پیکر", "Peyer patch", "folliculi lymphatici aggregati", "", "",
  "Composed of the canonical صفحهٔ + the eponym, as in صفحهٔ اپی‌فیز (Ch8); aggregated lymphoid "
  "nodules of the ileum.", "AFGHAN STANDARD", "MEDIUM"),
 ("رودهٔ بزرگ", "Large intestine", "", "", "", "Composed of the ordinary words رودهٔ + بزرگ.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("قولون", "Colon", "", "", "", "Transliteration in clinical use.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("سکوم", "Cecum", "", "", "", "Transliteration.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("آپاندکس", "Appendix", "appendix vermiformis", "", "",
  "Transliteration in clinical use for the vermiform appendix.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("قرحهٔ معده", "Gastric ulcer", "ulcus", "", "",
  "Composed of the established قرحه + معده. It is distinct from زخم (a wound).",
  "AFGHAN STANDARD", "MEDIUM"),
 ("هلیکوباکتر پیلوری", "Helicobacter pylori", "", "H. pylori", "",
  "International organism name retained as used in Afghan clinical practice.",
  "ENGLISH RETAINED", "MEDIUM"),
 ("سلیاک", "Celiac disease", "coeliac disease", "", "",
  "Transliteration in clinical use; gluten-sensitive enteropathy.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
]:
    T(_d, _e, _forb, AFG, _n, "Ch15", _dec, _c, lat=_lat, abbr=_ab)

# ================================ CH16 — LIVER, BILE, PANCREAS ==============
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("هپاتوسیت", "Hepatocyte", "", "", "",
  "Transliteration; the parenchymal cell of the liver, arranged in plates and performing most liver "
  "functions.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("صفافِ کبد", "Hepatic plate", "lamina hepatis", "", "",
  "Descriptive Dari phrase; the one-cell-thick plates of hepatocytes.", "AFGHAN STANDARD", "MEDIUM"),
 ("صفرا", "Bile", "bilis", "", "",
  "Established Dari word; the adjective is صفراوی.", "AFGHAN STANDARD", "MEDIUM"),
 ("کانالیکولوسِ صفراوی", "Bile canaliculus", "", "", "",
  "Composed of the transliteration کانالیکولوس (already used in Ch8 for bone) + صفراوی; the "
  "channels between adjacent hepatocytes.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("شبکهٔ صفراوی", "Biliary tree", "ductus biliferi", "", "",
  "Composed of the canonical شبکهٔ + صفراوی; the duct system from canaliculi to the main duct.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("وریدِ بابِ کبد", "Hepatic portal vein", "vena portae hepatis", "", "",
  "Composed of the canonical ورید + باب; the vein bringing nutrient-rich blood from the gut.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("منطقهٔ باب", "Portal area", "trias portalis", "", "",
  "Descriptive Dari phrase; the connective tissue area containing the portal triad.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ کوپفر", "Kupffer cells", "macrophagocytus stellatus", "", "",
  "Composed of canonical حجرات + the eponym; the resident macrophages of the hepatic sinusoids.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ ایتو", "Hepatic stellate (Ito) cells", "cellulae perisinusoidales", "", "",
  "Composed of canonical حجرات + the eponym; the vitamin-A storing, fibrosis-producing cells.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("کیسهٔ صفرا", "Gallbladder", "vesica biliaris", "", "",
  "Composed of the ordinary word کیسه + صفرا.", "AFGHAN STANDARD", "MEDIUM"),
 ("سیروزِ کبد", "Cirrhosis", "", "", "",
  "Composed of the established transliteration سیروز + the canonical کبد; the end-stage fibrotic liver disease. (کبد is the primary form; جگر is an accepted Afghan variant and is not used in this chapter.)",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("یرقان", "Jaundice", "icterus", "", "",
  "Established Dari word for jaundice; the everyday synonym زردی is explanatory only.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("هپاتیت", "Hepatitis", "", "", "",
  "Transliteration; inflammation of the liver.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("جزیرهٔ لانگرهانس", "Islet of Langerhans", "insulae pancreaticae", "", "",
  "Composed of the ordinary word جزیره + the eponym; the endocrine part of the pancreas.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ آسینارِ پانکراس", "Pancreatic acinar cells", "", "", "",
  "Composed of canonical حجرات + the transliteration آسینار (the same root as آسینِ غددِ لعابی, "
  "Ch14).", "AFGHAN STANDARD", "MEDIUM"),
 ("انسولین", "Insulin", "", "", "",
  "Transliteration; the hormone of the beta cells.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("گلوکاگون", "Glucagon", "", "", "",
  "Transliteration; the hormone of the alpha cells.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("پانکریاتیت", "Pancreatitis", "", "", "",
  "Transliteration; inflammation of the pancreas, characterized histologically by autodigestion.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("سنگِ صفرا", "Gallstone", "cholelithiasis", "", "",
  "Descriptive Dari phrase; cholesterol or pigment stones in the gallbladder.",
  "AFGHAN STANDARD", "MEDIUM"),
]:
    T(_d, _e, _forb, AFG, _n, "Ch16", _dec, _c, lat=_lat, abbr=_ab)

# ================================================== CH17 — RESPIRATORY =====
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("دستگاهِ تنفسی", "Respiratory system", "", "", "",
  "Composed of established Dari words; the airway and lung.", "AFGHAN STANDARD", "MEDIUM"),
 ("مخاطِ تنفسی", "Respiratory mucosa", "", "", "",
  "Composed of canonical مخاط + تنفسی; the ciliated, mucous-secreting lining of the airway.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("اپیتلیومِ تنفسی", "Respiratory epithelium", "", "", "",
  "Composed of canonical اپیتلیوم + تنفسی; pseudostratified ciliated columnar epithelium.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("ویلُوسِ بینی", "Olfactory vesicle? (olfactory epithelium)", "", "", "",
  "PLACEHOLDER-REMOVED", "AFGHAN STANDARD", "LOW"),
 ("حجرهٔ جارویی", "Brush cell", "", "", "",
  "Descriptive Dari phrase (حجره + جارویی, the ordinary word for brush-like) used as an "
  "explanatory gloss. The established goblet-cell rendering «حجرهٔ جامی» already exists in this "
  "glossary and is NOT reused here, since brush cell and goblet cell are different cells.",
  "ENGLISH RETAINED", "LOW"),
 ("حجراتِ کلارا", "Clara cells", "", "", "",
  "Composed of canonical حجرات + the eponym; the secretory, stem-like cells of bronchioles.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("برونش", "Bronchus", "", "", "",
  "Transliteration; the cartilaginous airway branches.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("برونشیول", "Bronchiole", "", "", "",
  "Transliteration; the airway branches without cartilage.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("برونشیولِ تنفسی", "Respiratory bronchiole", "", "", "",
  "Composed of the canonical برونشیول + the ordinary word تنفسی; the first site of gas exchange.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("آلوئول", "Alveolus", "", "", "",
  "Transliteration; the terminal gas-exchange sac. Plural: آلوئول‌ها.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("مجرایِ آلوئولار", "Alveolar duct", "", "", "",
  "Composed of the transliteration مجرا + آلوئولار (the same root as آلوئول).",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("کیسهٔ آلوئولار", "Alveolar sac", "", "", "",
  "Composed of the ordinary word کیسه + آلوئولار.", "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ نوعِ اول", "Type I pneumocytes", "", "", "",
  "Descriptive Dari phrase with the international numbering retained; the thin squamous cells "
  "covering most of the alveolar surface.", "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ نوعِ دوم", "Type II pneumocytes", "", "", "",
  "Descriptive Dari phrase; the cuboidal cells producing surfactant.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سورفکتانت", "Surfactant", "", "", "",
  "Transliteration; the surface-active phospholipid-protein mixture that lowers alveolar surface "
  "tension.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ درون‌آلوئولی", "Alveolar macrophages", "", "", "",
  "Descriptive Dari phrase; the dust cells that phagocytose inhaled particles.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حاجزِ خون-هوایی", "Blood-air barrier", "", "", "",
  "Composed of the established حاجز (as in حاجزِ خون-مغز, Ch11) + the ordinary words خون and هوایی.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("مژکِ تنفسی", "Respiratory cilium", "", "", "",
  "Composed of the canonical مژک + تنفسی; the cilia that propel the mucous blanket.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("پلورا", "Pleura", "", "", "",
  "Transliteration; the serous membrane around the lung (parietal and visceral).",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ذات‌الریه", "Pneumonia", "pneumonia", "", "",
  "Established Dari word for pneumonia (also written ذات‌الجنب in some Afghan texts for pleurisy); "
  "the clinical register uses ذات‌الریه.", "AFGHAN STANDARD", "MEDIUM"),
 ("آسم", "Asthma", "", "", "",
  "Established word in Afghan clinical use.", "AFGHAN STANDARD", "MEDIUM"),
 ("نسجِ ششی", "Lung tissue", "", "", "",
  "Composed of the canonical نسج + the adjective ششی (of the lung, as in شش = lung).",
  "AFGHAN STANDARD", "LOW"),
 ("سلِّ شش", "Pulmonary tuberculosis", "tuberculosis", "", "",
  "Composed of the established سل (tuberculosis) + شش (lung).", "AFGHAN STANDARD", "MEDIUM"),
 ("کارسینومِ برونکوژنیک", "Bronchogenic carcinoma", "", "", "",
  "Composed of the international term + the Dari noun کارسینوم (used in Ch12–16).",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
]:
    if _n == "PLACEHOLDER-REMOVED":
        continue
    T(_d, _e, _forb, AFG, _n, "Ch17", _dec, _c, lat=_lat, abbr=_ab)

# ======================================================= CH18 — THE SKIN =====
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("اپیدرم", "Epidermis", "", "", "",
  "Transliteration; the keratinized stratified squamous epithelial layer of the skin (جلد is "
  "already canonical for skin).", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("درم", "Dermis", "", "", "",
  "Transliteration; the connective tissue layer beneath the epidermis.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("هایپودرم", "Hypodermis (subcutaneous tissue)", "tela subcutanea", "", "",
  "Transliteration for the subcutaneous fat layer.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("لایهٔ بازال", "Stratum basale", "stratum germinativum", "", "",
  "Descriptive Dari layer name with the international Latin alongside, as in the other layered "
  "tissues of the book.", "AFGHAN STANDARD", "MEDIUM"),
 ("لایهٔ خاردار", "Stratum spinosum", "", "", "",
  "Descriptive Dari layer name; the prickle-cell layer.", "AFGHAN STANDARD", "MEDIUM"),
 ("لایهٔ گرانولار", "Stratum granulosum", "", "", "",
  "Descriptive Dari layer name; the keratohyaline-granule layer.", "AFGHAN STANDARD", "MEDIUM"),
 ("لایهٔ شاخی", "Stratum corneum", "", "", "",
  "Descriptive Dari layer name; the keratinized layer.", "AFGHAN STANDARD", "MEDIUM"),
 ("جسمِ لاملارِ اپیدرمی", "Lamellar body (Odland body)", "corpusculum lamellosum", "", "",
  "Composed of the established جسم + لاملار (registered for the lung in Ch17) with the qualifier "
  "اپیدرمی; the lipid-secreting organelle of the granular layer.", "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ مرکل", "Merkel cells", "", "", "",
  "Composed of canonical حجرات + the eponym; the tactile epithelial cells.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("فولیکولِ مو", "Hair follicle", "folliculus pili", "", "",
  "Composed of the transliteration فولیکول + the ordinary Dari word مو.", "AFGHAN STANDARD", "MEDIUM"),
 ("غدواتِ عرقیه", "Sweat glands", "glandulae sudoriferae", "", "",
  "The form recorded in the Afghan medical-student source that also gives «غدوات شحمی»; the "
  "adjective عرقی (sweat) follows from it.", "AFGHAN STANDARD", "MEDIUM"),
 ("غدهٔ عرقیِ اکراین", "Eccrine sweat gland", "", "", "",
  "Composed of the canonical غدهٔ عرقی + the transliteration اکراین; the common sweat gland.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("غدهٔ عرقیِ آپوکراین", "Apocrine sweat gland", "", "", "",
  "Composed of the canonical غدهٔ عرقی + the transliteration آپوکراین.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ناخن", "Nail", "unguis", "", "", "Ordinary Dari word.", "AFGHAN STANDARD", "MEDIUM"),
 ("اسکار", "Scar", "", "", "", "Transliteration in clinical use; the fibrous replacement tissue of healed wounds.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("زخم", "Wound", "", "", "", "Ordinary Dari word, kept distinct from قرحه (ulcer, Ch15).",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سوختگی", "Burn", "combustio", "", "", "Ordinary Dari word.", "AFGHAN STANDARD", "MEDIUM"),
 ("ویتیلیگو", "Vitiligo", "", "", "", "Transliteration; autoimmune loss of melanocytes.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("پسوریازیس", "Psoriasis", "", "", "", "Transliteration; a hyperproliferative epidermal disorder.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("میلانوما", "Melanoma", "", "", "", "Transliteration; malignant tumour of melanocytes.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("کارسینومِ حجرویِ بازال", "Basal cell carcinoma", "", "", "",
  "Composed of the international term + the canonical حجروی and بازال; the commonest skin cancer.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("درماتیت", "Dermatitis", "", "", "", "Transliteration; inflammation of the skin.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
]:
    T(_d, _e, _forb, AFG, _n, "Ch18", _dec, _c, lat=_lat, abbr=_ab)

# ====================================================== CH19 — URINARY ======
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("نفرون", "Nephron", "", "", "", "Transliteration (کلیه is already canonical for kidney).",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("گلومرولوس", "Glomerulus", "glomerulus", "", "",
  "Transliteration; the capillary tuft inside Bowman's capsule.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("کپسولِ بومن", "Bowman capsule", "capsula glomeruli", "", "",
  "Composed of the established transliteration کپسول + the eponym; the double-walled cup of the "
  "renal corpuscle.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("جسمِ کلیوی", "Renal corpuscle", "corpusculum renis", "", "",
  "Composed of the ordinary words جسم + کلیوی; glomerulus plus Bowman capsule.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("لولهٔ پروکسیمال", "Proximal tubule", "", "", "",
  "Composed of the canonical لوله + the transliteration پروکسیمال.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("لولهٔ دیستال", "Distal tubule", "", "", "",
  "Composed of the canonical لوله + the transliteration دیستال.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حلقهٔ هنله", "Loop of Henle", "ansa nephroni", "", "",
  "Composed of the ordinary word حلقه + the eponym.", "AFGHAN STANDARD", "MEDIUM"),
 ("لولهٔ جمع‌کننده", "Collecting duct", "ductus colligens", "", "",
  "Composed of the canonical لوله + جمع‌کننده (ordinary Dari).",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حاشیهٔ مسواکیِ کلیوی", "Renal brush border", "", "", "",
  "Reuses the canonical حاشیهٔ مسواکی (Ch15) with the qualifier کلیوی; the microvillous border of "
  "the proximal tubule.", "AFGHAN STANDARD", "MEDIUM"),
 ("پودوسیت", "Podocyte", "", "", "",
  "Transliteration; the visceral epithelial cell of Bowman capsule with foot processes.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("پروسه‌های پایی", "Foot processes (pedicels)", "", "", "",
  "Descriptive Dari phrase; the interdigitating processes of podocytes.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سدِ فیلتراسیون", "Filtration barrier", "", "", "",
  "Composed of the canonical سد + the transliteration فیلتراسیون; endothelium, basal lamina and "
  "podocyte slits.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ مزانژیال", "Mesangial cells", "", "", "",
  "Composed of canonical حجرات + the transliteration مزانژیال; the supporting, contractile and "
  "phagocytic cells of the glomerular tuft.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("آپاراتوسِ ژوکستاگلومرولار", "Juxtaglomerular apparatus", "", "JGA", "",
  "Composed of the transliteration آپاراتوس + ژوکستاگلومرولار; the renin-secreting complex.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ ژوکستاگلومرولار", "Juxtaglomerular cells", "", "", "",
  "Composed of canonical حجرات + the transliteration; the modified smooth muscle cells secreting "
  "renin.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ماکولا دنسا", "Macula densa", "", "", "",
  "Transliteration; the sodium-sensing cells of the distal tubule in the juxtaglomerular apparatus.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حالب", "Ureter", "", "", "", "Established Dari word for the ureter.", "AFGHAN STANDARD", "MEDIUM"),
 ("مثانه", "Urinary bladder", "vesica urinaria", "", "",
  "Ordinary Dari word.", "AFGHAN STANDARD", "MEDIUM"),
 ("اپیتلیومِ انتقالی", "Transitional epithelium", "urothelium", "", "",
  "Composed of the canonical اپیتلیوم + the established adjective انتقالی.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حجرهٔ چتری", "Umbrella cell", "cellula superficialis", "", "",
  "Descriptive Dari phrase; the large superficial cell of transitional epithelium, distinct from "
  "the goblet «حجرهٔ جامی» registered in Ch4.", "AFGHAN STANDARD", "MEDIUM"),
 ("مجرای ادرار", "Urethra", "", "", "", "Composed of established Dari words.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سنگِ کلیه", "Kidney stone", "nephrolithiasis", "", "",
  "Descriptive Dari phrase; the commonest urinary-tract calcification.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("نارساییِ مزمنِ کلیه", "Chronic kidney disease", "", "CKD", "",
  "Descriptive Dari phrase built from established words.", "AFGHAN STANDARD", "MEDIUM"),
 ("گلومرولونفریت", "Glomerulonephritis", "", "", "",
  "Transliteration; immune-mediated inflammation of the glomerulus.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
]:
    T(_d, _e, _forb, AFG, _n, "Ch19", _dec, _c, lat=_lat, abbr=_ab)

# =============================================== CH20 — ENDOCRINE GLANDS =====
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("غدهٔ درون‌ریز", "Endocrine gland", "", "", "",
  "The adjective درون‌ریز is the form already used in Ch4 and Ch5 for endocrine secretion; no new "
  "compound is coined.", "AFGHAN STANDARD", "MEDIUM"),
 ("پاراکراین", "Paracrine", "", "", "",
  "Transliteration; secretion acting on neighbouring cells.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("اتوکراین", "Autocrine", "", "", "",
  "Transliteration; secretion acting on the secreting cell itself.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("هیپوتالاموس", "Hypothalamus", "", "", "",
  "Transliteration; the neuroendocrine control centre above the pituitary.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("هیپوفیز", "Pituitary gland", "hypophysis", "", "",
  "Transliteration; the master endocrine gland in the sella turcica.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ادینوهیپوفیز", "Adenohypophysis", "", "", "",
  "Transliteration; the glandular (anterior) part of the pituitary.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("نوروهیپوفیز", "Neurohypophysis", "", "", "",
  "Transliteration; the neural (posterior) part of the pituitary.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("پارس دیستالیس", "Pars distalis", "", "", "",
  "International Latin term kept as such; the main anterior lobe.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("پارس نرووسا", "Pars nervosa", "", "", "",
  "International Latin term kept as such; the main posterior lobe.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ اسیدوفیل", "Acidophil cells", "", "", "",
  "Composed of canonical حجرات + the transliteration اسیدوفیل.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ بازوفیل", "Basophil cells", "", "", "",
  "Composed of canonical حجرات + the transliteration بازوفیل.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ کروموفوب", "Chromophobe cells", "", "", "",
  "Composed of canonical حجرات + the transliteration کروموفوب.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("تیروئید", "Thyroid gland", "glandula thyroidea", "", "",
  "Transliteration; the follicular endocrine gland of the neck.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("فولیکولِ تیروئیدی", "Thyroid follicle", "", "", "",
  "Composed of the canonical فولیکول (Ch18) with the qualifier تیروئیدی.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("کولویید", "Colloid", "", "", "",
  "Transliteration; the stored thyroglobulin colloid in the follicular lumen.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ فولیکولارِ تیروئید", "Follicular cells (thyrocytes)", "", "", "",
  "Composed of canonical حجرات + فولیکولار; the T3/T4-secreting cells.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ پارافولیکولار", "Parafollicular cells (C cells)", "", "C cells", "",
  "Composed of canonical حجرات + the transliteration پارافولیکولار; the calcitonin-secreting cells.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("تیروکسین", "Thyroxine", "", "T4", "",
  "Transliteration; the main thyroid hormone (T4) with international abbreviation retained.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("تری‌یودوتیرونین", "Triiodothyronine", "", "T3", "",
  "Transliteration; the more active thyroid hormone (T3).",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("کلسیتونین", "Calcitonin", "", "", "",
  "Transliteration; the hormone lowering blood calcium, secreted by parafollicular cells.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("پاراتیروئید", "Parathyroid gland", "glandulae parathyroideae", "", "",
  "Transliteration; the small glands regulating calcium via PTH.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("هورمونِ پاراتیروئیدی", "Parathyroid hormone", "", "PTH", "",
  "Composed of the canonical هورمون with the qualifier پاراتیروئیدی; international abbreviation kept.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ اصلیِ پاراتیروئید", "Chief cells (parathyroid)", "", "", "",
  "Composed of established Dari words with the qualifier پاراتیروئید to keep it distinct from the "
  "gastric chief cells registered in Ch15 as «حجراتِ زیموژنیک».",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ اکسیفیل", "Oxyphil cells", "", "", "",
  "Composed of canonical حجرات + the transliteration اکسیفیل.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ادرینال", "Adrenal gland", "glandula suprarenalis", "", "",
  "Transliteration; the cortex-plus-medulla gland on the kidney.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("قشرِ ادرینال", "Adrenal cortex", "", "", "",
  "Composed of the canonical قشر (registered for the kidney) + ادرینال.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("مدولای ادرینال", "Adrenal medulla", "", "", "",
  "Composed of canonical مدولای + ادرینال.", "AFGHAN STANDARD", "MEDIUM"),
 ("زونا گلومرولوزا", "Zona glomerulosa", "", "", "",
  "International term kept as such; the outermost aldosterone-producing zone.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("زونا فاسیکولاتا", "Zona fasciculata", "", "", "",
  "International term kept as such; the middle cortisol-producing zone.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("زونا رتیکولاریس", "Zona reticularis", "", "", "",
  "International term kept as such; the innermost zone producing androgens.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ کرومافین", "Chromaffin cells", "", "", "",
  "Composed of canonical حجرات + the transliteration کرومافین; the catecholamine-storing medullary "
  "cells.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("کورتیزول", "Cortisol", "", "", "",
  "Transliteration; the glucocorticoid of the zona fasciculata.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("آلدوسترون", "Aldosterone", "", "", "",
  "Transliteration; the mineralocorticoid of the zona glomerulosa.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("غدهٔ پینیال", "Pineal gland", "epiphysis cerebri", "", "",
  "Composed of the canonical غده with the transliteration پینیال.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("پاینالوسایت", "Pinealocyte", "", "", "",
  "Transliteration; the melatonin-secreting cell of the pineal gland.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ملانونین", "Melatonin", "", "", "",
  "Transliteration; the pineal hormone controlling circadian rhythm.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجرهٔ هدف", "Target cell", "", "", "",
  "Composed of the canonical حجره + the ordinary word هدف.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("هورمونِ تروپیک", "Tropic hormone", "", "", "",
  "Composed of the canonical هورمون + the transliteration تروپیک.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("گونادوتروپین", "Gonadotropin", "", "", "",
  "Transliteration; FSH and LH of the anterior pituitary.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("اکسیتوسین", "Oxytocin", "", "", "",
  "Transliteration; the posterior-pituitary hormone of uterine contraction and milk ejection.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("وازوپرسین", "Vasopressin", "", "ADH", "",
  "Transliteration with the international abbreviation ADH retained; the antidiuretic hormone already "
  "used in Ch19.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("گواتر", "Goiter", "", "", "",
  "Transliteration; thyroid enlargement.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("دیابتیس ملیتوس", "Diabetes mellitus", "", "DM", "",
  "Transliteration in established clinical use; the insulin- and glucagon-related disorder already "
  "referenced in Ch16.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
]:
    T(_d, _e, _forb, AFG, _n, "Ch20", _dec, _c, lat=_lat, abbr=_ab)

# ======================================== CH21 — MALE REPRODUCTIVE SYSTEM =====
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("بیضه", "Testis", "testis", "", "",
  "Established Dari/Arabic-root anatomical word already familiar in Afghan medical teaching.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سکروتوم", "Scrotum", "", "", "",
  "Transliteration; the pouch housing the testes.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("لوله‌های منیفروس", "Seminiferous tubules", "tubuli seminiferi", "", "",
  "English-derived transliteration of the international term; no Afghan Dari compound was invented "
  "for it.", "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("اپیتلیومِ منیفروس", "Seminiferous epithelium", "", "", "",
  "Composed of the canonical اپیتلیوم with the transliteration منیفروس.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("حجراتِ سرتولی", "Sertoli cells", "", "", "",
  "Composed of canonical حجرات + the eponym; the supporting cells of the seminiferous epithelium.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ لیدیگ", "Leydig cells", "", "", "",
  "Composed of canonical حجرات + the eponym; the interstitial testosterone-secreting cells.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("اسپرماتوگونیا", "Spermatogonium", "", "", "",
  "Transliteration; the basal diploid germ cell.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("اسپرماتوسایت", "Spermatocyte", "", "", "",
  "Transliteration; the germ cell in the first or second meiotic division.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("اسپرماتید", "Spermatid", "", "", "",
  "Transliteration; the haploid cell after meiosis, before spermiogenesis.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("سپرماتوزوا", "Spermatozoon", "", "", "",
  "Transliteration; the mature motile male gamete.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("سپرماتوژنیز", "Spermatogenesis", "", "", "",
  "Transliteration of the international term; the process was not given an invented Dari compound.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("اکروزوم", "Acrosome", "", "", "",
  "Transliteration; the enzyme-containing cap over the sperm nucleus.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("تاژکِ سپرم", "Sperm flagellum", "", "", "",
  "Composed of the canonical تاژک (registered in Ch2) with سپرم; the motile tail of the sperm.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حاجزِ خون-بیضه", "Blood–testis barrier", "", "", "",
  "Built on the canonical حاجز (as in حاجزِ خون-مغز of Ch11 and حاجزِ خون-هوایی of Ch17).",
  "AFGHAN STANDARD", "MEDIUM"),
 ("اپیدیدیم", "Epididymis", "", "", "",
  "Transliteration; the coiled duct of sperm maturation and storage.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("واز دفرنس", "Vas deferens (ductus deferens)", "ductus deferens", "", "",
  "International term kept as a transliteration; no Afghan Dari equivalent was located and none was "
  "constructed.", "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("وسیکولِ سیمینال", "Seminal vesicle", "vesicula seminalis", "", "",
  "Transliteration of the international term; the fructose-rich accessory gland.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("پروستات", "Prostate gland", "prostata", "", "",
  "Transliteration; the largest male accessory gland.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("غددِ بولبویورترال", "Bulbourethral glands (Cowper glands)", "glandulae bulbourethrales", "", "",
  "Composed of the canonical غدد + the transliteration بولبویورترال.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("منی", "Semen", "", "", "",
  "Established Dari word; the ejaculate consisting of sperm plus glandular secretions.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("تستوستیرون", "Testosterone", "", "", "",
  "Transliteration; the main androgen of Leydig cells.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("اینهیبین", "Inhibin", "", "", "",
  "Transliteration; the Sertoli-cell hormone suppressing FSH.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("هورمونِ محرکِ فولیکول", "Follicle-stimulating hormone", "", "FSH", "",
  "Descriptive Dari built from established words with the international abbreviation retained.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("هورمونِ لوتینایزینگ", "Luteinizing hormone", "", "LH", "",
  "Composed of the canonical هورمون + the transliteration لوتینایزینگ; abbreviation retained.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("بیضهٔ نزول‌نکرده", "Cryptorchidism", "cryptorchidismus", "", "",
  "Descriptive Dari phrase from established words; the undescended testis.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("هایپرپلازیِ خوش‌خیمِ پروستات", "Benign prostatic hyperplasia", "", "BPH", "",
  "Descriptive Dari phrase with the international abbreviation retained; the common ageing change.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سرطانِ پروستات", "Prostate cancer", "", "", "",
  "Composed of established words; the commonest male visceral malignancy in older men.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("واریکوسل", "Varicocele", "", "", "",
  "Transliteration; dilatation of the pampiniform plexus.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
]:
    T(_d, _e, _forb, AFG, _n, "Ch21", _dec, _c, lat=_lat, abbr=_ab)

# ====================================== CH22 — FEMALE REPRODUCTIVE SYSTEM =====
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("تخمدان", "Ovary", "ovarium", "", "",
  "Established Dari/Arabic-root anatomical word used in Afghan medical teaching.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("اووسایت", "Oocyte", "", "", "",
  "Transliteration; the female gamete before fertilisation.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("فولیکولِ تخمدانی", "Ovarian follicle", "folliculus ovaricus", "", "",
  "Composed of the canonical فولیکول (Ch18/Ch20) with the qualifier تخمدانی.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("فولیکولِ گرافی", "Graafian follicle", "folliculus maturus", "", "",
  "Composed of the canonical فولیکول + the eponym; the mature pre-ovulatory follicle.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ گرانولوزا", "Granulosa cells", "", "", "",
  "Composed of canonical حجرات + the transliteration گرانولوزا; the follicular epithelial cells.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ تیکا", "Theca cells", "", "", "",
  "Composed of canonical حجرات + the transliteration تیکا; the stromal layers of the follicle.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("زونا پلوسیدا", "Zona pellucida", "", "", "",
  "International Latin term kept as such; the glycoprotein coat of the oocyte.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("کرونا رادیاتا", "Corona radiata", "", "", "",
  "International Latin term kept as such; the granulosa cells adhering to the zona pellucida.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("جسمِ زرد", "Corpus luteum", "corpus luteum", "", "",
  "Descriptive Dari phrase from established words (جسم + زرد) with the Latin term kept.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("جسمِ سفید", "Corpus albicans", "corpus albicans", "", "",
  "Descriptive Dari phrase from established words with the Latin term kept; the scar of the corpus "
  "luteum.", "AFGHAN STANDARD", "MEDIUM"),
 ("اوولاسیون", "Ovulation", "", "", "",
  "Transliteration; release of the oocyte at mid-cycle.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("لولهٔ فالوپ", "Fallopian tube (oviduct)", "tuba uterina", "", "",
  "Composed of the canonical لوله + the eponym; the oviduct.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("رحم", "Uterus", "", "", "", "Established Dari/Arabic-root anatomical word.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("اندومتریوم", "Endometrium", "", "", "",
  "Transliteration; the mucosal lining of the uterus.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("میومتریوم", "Myometrium", "", "", "",
  "Transliteration; the smooth muscle coat of the uterus.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("پریومتریوم", "Perimetrium", "", "", "",
  "Transliteration; the serosal covering of the uterus.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("سرویکس", "Cervix", "", "", "",
  "Transliteration; the neck of the uterus.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("واژن", "Vagina", "", "", "",
  "Transliteration in established clinical use.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("سیکلِ قاعدگی", "Menstrual cycle", "cyclus menstrualis", "", "",
  "Composed of the established word سیکل + قاعدگی (the ordinary Dari word for menstruation).",
  "AFGHAN STANDARD", "MEDIUM"),
 ("پروژسترون", "Progesterone", "", "", "",
  "Transliteration; the corpus-luteum hormone of the secretory phase.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ایستروژن", "Estrogen", "", "", "",
  "Transliteration; the follicular hormone.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("گونادوتروپینِ کوریونیکِ انسانی", "Human chorionic gonadotropin", "", "hCG", "",
  "Composed of the canonical گونادوتروپین (Ch20) with descriptive qualifiers; abbreviation retained.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("پلاسنتا", "Placenta", "", "", "",
  "Transliteration; the fetomaternal exchange organ.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("غدهٔ پستان", "Mammary gland", "glandula mammaria", "", "",
  "Composed of the canonical غده with the established word پستان.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("لوبولِ غدهٔ پستان", "Mammary lobule", "", "", "",
  "Composed of the canonical لوبول (Ch14) with غدهٔ پستان.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("دیوارهٔ رحمِ در حالِ تکثیر", "Proliferative phase endometrium", "", "", "",
  "Descriptive Dari phrase; the estrogen-driven first half of the cycle.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("دیوارهٔ رحمِ ترشحی", "Secretory phase endometrium", "", "", "",
  "Descriptive Dari phrase; the progesterone-driven second half of the cycle.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سندرومِ تخمدانِ پولی‌سیستیک", "Polycystic ovary syndrome", "", "PCOS", "",
  "Descriptive Dari phrase with the international abbreviation retained.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سرطانِ سرویکس", "Cervical cancer", "", "", "",
  "Composed of established words; linked to human papillomavirus.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("فیبرومِ رحم", "Uterine leiomyoma (fibroid)", "leiomyoma uteri", "", "",
  "Composed of the transliteration فیبروم + رحم; the common benign smooth-muscle tumour.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
]:
    T(_d, _e, _forb, AFG, _n, "Ch22", _dec, _c, lat=_lat, abbr=_ab)

# ================================= CH23 — THE EYE & EAR (SENSE ORGANS) =====
for _d, _e, _lat, _ab, _forb, _n, _dec, _c in [
 ("چشم", "Eye", "oculus", "", "",
  "The ordinary Dari word for the eye, used unchanged in Afghan medical teaching.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("قرنیه", "Cornea", "", "", "",
  "Arabic-rooted anatomical word in established Dari medical use; the transparent anterior coat.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("سکلرا", "Sclera", "", "", "",
  "Transliteration; the opaque white fibrous coat.", "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("کوروئید", "Choroid", "", "", "",
  "Transliteration; the vascular layer of the eye.", "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("یوویا", "Uvea", "", "", "",
  "Transliteration; the iris, ciliary body and choroid together.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("عنبیه", "Iris", "", "", "",
  "Arabic-rooted anatomical word in established Dari use.", "AFGHAN STANDARD", "MEDIUM"),
 ("جسمِ سیلیاری", "Ciliary body", "corpus ciliare", "", "",
  "Composed of established جسم + the transliteration سیلیاری.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("شبکیه", "Retina", "", "", "",
  "Arabic-rooted anatomical word in established Dari medical use.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("عدسی", "Lens", "lens crystallina", "", "",
  "Arabic-rooted word in established Dari use for the crystalline lens.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("هیومورِ آکوئوس", "Aqueous humor", "humor aquosus", "", "",
  "International term kept as a transliteration; no Afghan Dari compound was invented for it.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("جسمِ زجاجی", "Vitreous body", "corpus vitreum", "", "",
  "Composed of established جسم + زجاجی; the gel filling the posterior chamber.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حجرهٔ گیرندهٔ نوری", "Photoreceptor cell", "", "", "",
  "Descriptive Dari phrase; the light-sensing cells of the retina.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ میله‌ای", "Rod cells", "", "", "",
  "Established descriptive name for the rod photoreceptors (میله = rod) with the English term "
  "alongside; no coined transliteration.", "AFGHAN STANDARD", "MEDIUM"),
 ("حجراتِ مخروطی", "Cone cells", "", "", "",
  "Established descriptive name for the cone photoreceptors (مخروط = cone) with the English term "
  "alongside.", "AFGHAN STANDARD", "MEDIUM"),
 ("اپیتلیومِ پیگمنتیِ شبکیه", "Retinal pigment epithelium", "", "RPE", "",
  "Composed of the canonical اپیتلیوم + the transliteration پیگمنتی with the qualifier شبکیه.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("فووآ سنترالیس", "Fovea centralis", "", "", "",
  "International Latin term kept as such; the site of sharpest vision.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("نقطهٔ کور", "Optic disc", "discus nervi optici", "", "",
  "Composed of ordinary Dari words; the blind spot where the optic nerve leaves.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("ملتحمه", "Conjunctiva", "", "", "",
  "Arabic-rooted word in established Dari clinical use.", "AFGHAN STANDARD", "MEDIUM"),
 ("غدهٔ اشکی", "Lacrimal gland", "glandula lacrimalis", "", "",
  "Composed of the canonical غده with the ordinary word اشکی (tear).",
  "AFGHAN STANDARD", "MEDIUM"),
 ("کاتاراکت", "Cataract", "", "", "",
  "Transliteration used in Afghan clinical speech; the opaque lens.",
  "COMMON AFGHAN TRANSLITERATION", "LOW"),
 ("گلوکوم", "Glaucoma", "", "", "",
  "Transliteration; raised intraocular pressure damaging the optic nerve.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("گوش", "Ear", "auris", "", "",
  "The ordinary Dari word, used unchanged in Afghan medical teaching.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("لالهٔ گوش", "Auricle (pinna)", "auricula", "", "",
  "Composed of the established word لالهٔ with گوش; the visible external ear.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("مجرای شنواییِ خارجی", "External auditory canal", "meatus acusticus externus", "", "",
  "Descriptive Dari phrase from established words.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("پردهٔ صماخ", "Tympanic membrane (eardrum)", "membrana tympanica", "", "",
  "Arabic-rooted compound in established Dari use for the eardrum.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("استخوانچه‌های گوش", "Auditory ossicles", "ossicula auditus", "", "",
  "Descriptive Dari phrase; the malleus, incus and stapes (مالیوس، اینکوس، استاپیس kept as "
  "transliterations in the text).", "AFGHAN STANDARD", "MEDIUM"),
 ("حلزون", "Cochlea", "", "", "",
  "Established word (snail-shaped) in Dari medical use for the cochlea.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("اندامِ کورتی", "Organ of Corti", "", "", "",
  "Composed of the established اندام + the eponym; the receptor organ of hearing.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("حجراتِ مویی", "Hair cells", "", "", "",
  "Descriptive Dari phrase; the mechanosensory cells of the cochlea and vestibule.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("غشای بازیلار", "Basilar membrane", "membrana basilaris", "", "",
  "Composed of the canonical غشاء + the transliteration بازیلار.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("غشای تکتوریال", "Tectorial membrane", "membrana tectoria", "", "",
  "Composed of the canonical غشاء + the transliteration تکتوریال.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("اندولیمف", "Endolymph", "", "", "",
  "Transliteration; the potassium-rich fluid of the membranous labyrinth.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("دستگاهِ دهلیزی", "Vestibular apparatus", "apparatus vestibularis", "", "",
  "Composed of established words; the balance organ of the inner ear.",
  "AFGHAN STANDARD", "MEDIUM"),
 ("اوتیتِ میانی", "Otitis media", "", "", "",
  "Transliteration with the qualifier میانی; infection of the middle ear.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("سندرومِ مِنیر", "Ménière disease", "", "", "",
  "Composed of the canonical سندروم + the eponym; vertigo with hearing loss and tinnitus.",
  "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
 ("ناشنوایی", "Deafness (hearing loss)", "", "", "",
  "Ordinary Dari word for hearing loss.", "AFGHAN STANDARD", "MEDIUM"),
]:
    T(_d, _e, _forb, AFG, _n, "Ch23", _dec, _c, lat=_lat, abbr=_ab)



OVERRIDES = {
    "رنگ‌آمیزی":        ("", "", "", None),
    "مطبق":            ("", "", "", None),
    "میکروفیلامنت":    ("", "", "", None),   # blacklist comes from INVENTED_CONSTRUCTIONS
    "اندوتلیوم":       ("", "آندوتلیوم", "", "آندوتلیوم"),
    "غشای حجروی":       ("غشای سلولی", "غشای پلاسمایی", "", None),
    "پلاسمالما":        ("", "", "plasmalemma", None),
    "ماتریکس":          ("", "", "extracellular matrix", None),
    "کریستا":           ("", "", "cristae", None),
    "سیتواسکلتون":      ("", "اسکلت حجروی", "", None),
    "لایزوزوم":         ("", "لیزوزوم", "", None),
    "میکروویلی":        ("ریزپرز", "مایکروویلای", "", None),
    "غشای هستوی":       ("", "پوشش هسته‌ای", "", None),
    "منفذ هستوی":       ("", "منفذ هسته‌ای", "", None),
    "کرویاتِ سرخ":      ("گویچهٔ سرخ;گلبول قرمز", "حجرات سرخ", "", None),
    "آپوپتوز":          ("", "مرگ برنامه‌ریزی‌شدهٔ حجره", "", None),
    "لامینای پایه":     ("", "", "", None),   # غشای پایه is a DIFFERENT structure (basement membrane)
    "یوروتلیوم":        ("", "اپیتلیوم انتقالی;اپیتلیوم مثانه", "", None),
    "دسموزوم":          ("", "پل حجروی", "", None),
    "گابلت":            ("", "حجرهٔ جامی", "", None),
    "اندوتلیوم":        ("", "آندوتلیوم", "", None),
    "ماست‌سل":          ("", "ماست سیت", "", None),
    "پلاسما‌سل":        ("", "پلاسموسیت", "", None),
    "شحمی":             ("", "", "", None),
    "آدیپوسایت":        ("", "حجرهٔ شحمی", "", None),
    "نیدوژن":           ("", "", "entactin", None),
    "گلیکوزآمینوگلیکان": ("", "", "mucopolysaccharide", None),
    "هیالورونان":       ("", "", "hyaluronic acid", None),
    "نسج منضم شل":      ("", "شل", "", "نسج منضم سست"),
    "رگ‌زایی":          ("", "واسکولارزاسیون", "", None),
    "اسکوروی":          ("", "اسکوربوت", "", None),
    "باکتری":           ("", "باکتریا", "", None),
}

# ==========================================================================
# EVIDENCE-ANCHORED CORRECTION (pass 3)
# ==========================================================================
# The directive: every canonical decision must rest on an ACTUAL Afghan source,
# and the five decision labels must be assigned from evidence, not linguistic
# judgement. Every entry below was re-checked against a named Afghan document.
#
#   ME7  = Afghan MoE, Biology Grade 7, Kabul 1398 (moe.gov.af) — the official
#          school textbook that first teaches cell, tissue and microscope.
#   ME12 = Afghan MoE, Science Grade 12 (moe.gov.af) — nervous system, skin,
#          eye, senses.
#   TOL  = TolAfghan, «فزیولوژی حجره» — Afghan cell-physiology text.
#   MOPH = Afghan MoPH job register / Afghanistan health-sector documents.
#   AFD  = Afghan doctors' clinical writing (afghan-doctors.com).
#   AV   = AfghanVet, Afghan biology text.
#   S5   = Afghan faculty histology text, خاتم النبیین University.
#
# Where NO Afghan document could be located, the entry says so explicitly and is
# labelled honestly instead of asserting an Afghan standard.

# key = dari_term ; value = (source_authority_with_quote, decision, confidence)
EVIDENCE_OVERRIDES = {
    "حجره":       (ME7 + " — «حجره را کوچکترین واحد ساختمانی و وظیفوی تعریف کرد»؛ "
                        "«مایکروسکوپ … برای اولین بار حجرات کارک را … زیر مایکروسکوپ مشاهده نمود»",
                   "AFGHAN STANDARD", "HIGH"),
    "حجرات":      (ME7 + " — «انواع مختلف حجرات»، «مقایسه حجرات حیوانی و نباتی»",
                   "AFGHAN STANDARD", "HIGH"),
    "حجروی":      (ME7 + " — «غشای حجروی»، «تنظیم حجروي»، «نظریۀ حجروی»",
                   "AFGHAN STANDARD", "HIGH"),
    "نسج":        (ME7 + " — «انساج، انساج نباتی / انساج حیوانی»؛ S5 «نسج منضم»",
                   "AFGHAN STANDARD", "HIGH"),
    "انساج":      (ME7 + " — «سطوح تنظیم در موجودات زنده، انساج، انساج نباتی»",
                   "AFGHAN STANDARD", "HIGH"),
    "نسج منضم":   (S5 + " — «نسج منضم» (Afghan connective-tissue teaching); ME7 «انساج»",
                   "AFGHAN STANDARD", "HIGH"),
    "مایکروسکوپ": (ME7 + " — ch.1 «مایکروسکوپ و انواع آن»؛ «مایکروسکوپ مرکب نوری»",
                   "AFGHAN STANDARD", "HIGH"),
    "ارگانل":     (ME7 + " — «ساختمان‌های کوچکی … به‌نام اعضاچه یا ارگانل (Organelle) حجره "
                         "یاد شده»", "AFGHAN STANDARD", "HIGH"),
    "مایتوکندریا": (TOL + " — «مایتوکاندریا (Mitochondria): در حجره، نوعی دستگاه انتقال انرژی»",
                   "AFGHAN STANDARD", "HIGH"),
    "انزایم":     (TOL + " — «انزایم گلوکز ۶ – فسفاتاز در سطح داخلی … شبکه اندوپلاسمی»",
                   "AFGHAN STANDARD", "HIGH"),
    "کیمیاوی":    (ME12 + " — «پیام‌رسان‌های کیمیاوی»، «مواد کیمیاوي»",
                   "AFGHAN STANDARD", "HIGH"),
    "فسفوریلیشن": (TOL + " — «انرژی کیمیاوی موجود در مواد غذایی با عمل فسفوریلیشن اکسیداتیو، "
                         "به صورت پیوندهای پرانرژی فسفات (ATP) ذخیره شود»",
                   "AFGHAN STANDARD", "HIGH"),
    "میتابولیسم": (TOL + " — «دخالت در میتابولیسم قندها»", "AFGHAN STANDARD", "HIGH"),
    "سایتوپلازم": (ME7 + " — «سایتوپالزم درخارج هسته قرار دارد و قسمت زیاد حجره را تشکیل می‌دهد»",
                   "AFGHAN STANDARD", "HIGH"),
    "غشای حجروی": (ME7 + " — «غشای حجروی: به‌نام غشای پالزمایی هم یاد میشود»",
                   "AFGHAN STANDARD", "HIGH"),
    "پروتئین":    (TOL + " — «پیش‌رشته‌ها از دو نوع پروتئین کروی مشابه … تشکیل شده‌اند»؛ "
                         "ME7/ME12 use the simplified spelling «پروتین»",
                   "AFGHAN STANDARD", "HIGH"),
    "استوانه‌ای": (ME7 + " — «بیضوی، مدور، مکعبی، استوانه یی و تعدادی هم مسطح»؛ "
                         "ME12 «حجرات مخروطی و استوانه یی»",
                   "AFGHAN STANDARD", "HIGH"),
    "نیورون":     (ME12 + " — «نیورون دوم سیناپسی را بیشتر تحریک کنند»، «نیورون های حرکي»",
                   "AFGHAN STANDARD", "HIGH"),
    "جلد":        (ME12 + " — ch.1 «جلد»، «ساختمان جلد بدن»", "AFGHAN STANDARD", "HIGH"),
    "غدوات":      (ME12 + " — «غدوات داخل مجرا، مادة موم مانندی ترشح میکنند»",
                   "AFGHAN STANDARD", "MEDIUM"),
    "موی‌رگ":     (ME12 + " — «موی رگهای جای پیوند … جریان خون آن ها با رگهای بزرگ در ارتباط»",
                   "AFGHAN STANDARD", "HIGH"),
    "مریض":       (ME12 + " — «مریض»، «مریضی»", "AFGHAN STANDARD", "HIGH"),
    "داکتر":      (ME12 + " — «فرد مریض باید تحت مراقبت داکتر بوده»", "AFGHAN STANDARD", "HIGH"),
    "تداوی":      (AFD + " — «رادیو تراپی (تداوی اشعوی)»، «تداوی دوایی»، «کیموتراپی»",
                   "AFGHAN STANDARD", "HIGH"),
    "کیموتراپی":  (AFD + " — «شیوه‌های مختلف تداوی … تداوی دوایی، تداوی اشعوی، کیموتراپی و جراحی»",
                   "COMMON AFGHAN TRANSLITERATION", "HIGH"),
    "دوا":        (MOPH + " — «خدمات به شمول دوا غذا رایگان»، «دواخانه»، «دواسازی»؛ "
                          "«اداره ملی ادویه و غذا» (dpmea.gov.af) «محصولات دوایی»",
                   "AFGHAN STANDARD", "MEDIUM"),
    "کلیه":       (MOPH + " — «امراض کلیه، از جمله عدم کفایه کلیه (گرده)»",
                   "AFGHAN STANDARD", "MEDIUM"),
    "کبد":        (MOPH + " — «لوبول کبد» (Afghan histology text S5)",
                   "AFGHAN STANDARD", "MEDIUM"),
    "پتالوژی":    (MOPH + " — «پتالوژی اناتومیک (هستولوژی/هستوپتالوژی، سایتولوژی)»",
                   "AFGHAN STANDARD", "HIGH"),
    "هستولوژی":   (MOPH + " — «هستولوژی/هستوپتالوژی»", "AFGHAN STANDARD", "HIGH"),
    "سایتولوژی":  (MOPH + " — «سایتولوژی»", "AFGHAN STANDARD", "HIGH"),
    "هستوپتالوژی": (MOPH + " — «هستوپتالوژی»", "AFGHAN STANDARD", "HIGH"),
    "هسته‌چه":    (S5 + " — «هسته چه» (Afghan histology text)", "AFGHAN STANDARD", "MEDIUM"),
    "کرویاتِ سرخ": (S5 + " — «کرویات سفید خون» (Afghan histology text)",
                   "AFGHAN STANDARD", "MEDIUM"),
    "شریان":      (S5 + " — «قلب، شریان، ورید، موی رگها» (Afghan histology text)",
                   "AFGHAN STANDARD", "MEDIUM"),
    "ورید":       (S5 + " — «قلب، شریان، ورید، موی رگها»", "AFGHAN STANDARD", "MEDIUM"),
    "اوعیهٔ دموی": (S5 + " — «عروق خونی / موی رگها» (Afghan histology text)",
                   "AFGHAN STANDARD", "MEDIUM"),
}

# Forms that must NEVER reappear: constructed by translating English morphemes,
# or named in the corrective directive as forbidden. All are now enforced.
INVENTED_CONSTRUCTIONS = {
    "کیمیا تداوی":       "کیموتراپی (AFD)",
    "کیمیا‌تداوی":       "کیموتراپی (AFD)",
    "کیمیا درمانی":      "کیموتراپی (AFD)",
    # NOTE: چندلایه is deliberately NOT listed. It is an attested Afghan
    # descriptive phrase (S5 «چند طبقه») used in this book as a parenthetical
    # Dari gloss for «مطبق» and «شبه‌مطبق». Forbidding it would flag a legitimate
    # gloss — the exact over-matching failure recorded in README §4.2.
    "نورون":             "نیورون (ME12)",
    "نورون‌ها":          "نیورون‌ها (ME12)",
    "میتوکندریایی":      "مایتوکندریایی (TOL)",
    "ریزرشته":           "میکروفیلامنت",
    "ریزپرز":            "میکروویلی",
    "ریزلوله":           "میکروتوبول",
    "منشوری":            "استوانه‌ای (ME7)",
}

# Rows withdrawn by pass 3. A term can appear in the build list more than once
# (pass 1 added the invented form, pass 3 added the restored one); a withdrawn row
# is dropped at write time so the two can never contradict each other.
DROP_ROWS = set()   # no withdrawn rows remain; both Carbohydrate spellings are settled

# --- duplicate-row cleanup (whole-book pass, end of run) ----------------------
# Twelve English terms had been registered twice because later chapters re-introduced
# them. Each pair was reviewed: the row listed here is dropped and, where the two rows
# used different Dari forms, the surviving row records the other form so no reader loses
# a form that appears in the text. Nothing else is changed by this list.
DEDUP_DROP = {
    ("Endothelium",        "Ch12"),   # identical to the Ch04 row
    ("Submucosa",          "Ch15"),   # «تحت مخاط» kept; «زیرمخاطی» recorded as its variant
    ("Plasma cell",        "Ch13"),   # «پلاسما‌سل» kept with «پلاسموسیت» as variant
    ("Adipocyte",          "Ch05"),   # unused «آدیپوسایت»; the book writes «ادیپوسیت»
    ("Chondroitin sulfate", "Ch07"),  # «کندرویتین سولفات» kept (sulfate spelling normalised)
    ("Keratan sulfate",    "Ch07"),   # «کراتان سولفات» kept (sulfate spelling normalised)
    ("Fibrin",             "Ch09"),   # identical to the Ch05 row
    ("Capillary",          "Ch12"),   # «موی‌رگ» is the single primary form
    ("Insulin",            "Ch16"),   # identical to the Ch06 row
    ("Bone marrow",        "Ch13"),   # «مغز استخوان» kept (kасre form normalised in text)
    ("Lymphocyte",         "Ch13"),   # «لنفوسیت» kept with «لیمفوسیت» as variant
    ("Leukemia",           "Ch13"),   # identical to the Ch09 row
}

# The two variants that survive only as recorded alternative forms:
OVERRIDES.setdefault("تحت مخاط", ("", "زیرمخاطی;لایهٔ زیرمخاطی", "", None))
OVERRIDES.setdefault("لنفوسیت",  ("", "لیمفوسیت", "", None))
   # no withdrawn rows remain; both Carbohydrate spellings are settled

# Applicability note attached to entries whose evidence is a transliteration
# convention rather than a located Afghan document.
NO_DOC_FOUND = ("Established English-derived transliteration retained as the term Afghan "
                "readers recognise; no Afghanistan-specific documentary source located in "
                "this audit (see editorial/terminology-decisions.md §14)")

# NOTE — superseded reasoning, retained for the audit trail: an earlier pass
# classed the Afghan transliteration of Carbohydrate as a morpheme-by-morpheme
# construction and then as an unresolved English-retained term. Both judgements
# were wrong. The form IS attested in an Afghan source (TolAfghan, «فزیولوژی
# حجره»), so it is canonical; see the کاربوهایدریت row above. The Persian
# transliteration remains non-canonical for this book by owner decision.

# ---- pass 3: terms recovered from official Afghan sources ----------------
T("ارگانل", "Organelle", "",
  ME7 + " — «در سایتوپالزم ساختمان‌های کوچکی موجود است که به‌نام اعضاچه یا ارگانل "
        "(Organelle) حجره یاد شده»",
  "CANONICAL (owner decision, locked): ارگانل, because the official Afghan MoE Grade-7 biology "
  "textbook introduces the concept with that form (with the Dari descriptor اعضاچه). اندامک is ALSO "
  "in Afghan use — TolAfghan, «فزیولوژی حجره» (tolafghan.com/posts/30498): «به اجزای درون حجره "
  "اندامک گفته می‌شود» — so it is recorded as ACCEPTED AFGHAN VARIANT and is deliberately NOT on "
  "the prohibited list. ارگانل remains the book's canonical form and the one used in the text.",
  "Ch1; Ch2; Ch3; Ch5", acc="اندامک;اندامک‌ها;اندامک‌های;اندامکی;اندامکِ")

T("نیورون", "Neuron", "نورون;نورون‌ها;نورون‌های;نورونی",
  ME12 + " — «نیورون دوم سیناپسی را بیشتر تحریک کنند»، «نیورون هاي حرکي را تخریب ميکند»",
  "Recovered in pass 3. نورون was the Iranian form used by the first draft; the official "
  "Afghan Grade-12 science textbook writes نیورون consistently. This also matches the "
  "Afghan transliteration pattern of a prosthetic vowel (cf. ایون, انزایم, استروئید). "
  "نورون is now forbidden.",
  "Ch2; Ch3", "AFGHAN STANDARD", "HIGH")

# ==========================================================================
# SOURCE-HONESTY CORRECTION (final Terminology Evidence Gate)
# ==========================================================================
# The directive: "Never label an entry as supported by an Afghan institution
# unless an actual identifiable Afghan document/source was examined. A generic
# label such as 'Afghan medical education usage' is NOT evidence."
#
# 31 entries carried a label that named no document. Each is resolved here in
# one of three honest ways:
#   (a) a NAMED Afghan document that was actually fetched and read
#   (b) an OWNER-MANDATED project decision, declared as such and NOT attributed
#       to any Afghan institution
#   (c) an explicit statement that no Afghanistan-specific source was located
OWNER = ("Owner-mandated canonical decision (project Terminology Gate directive, 2026-09-21). "
         "This is NOT an evidence claim and is NOT attributed to any Afghan institution.")
NODOC = ("Established English-derived transliteration retained as the term Afghan readers "
         "recognise; no Afghanistan-specific documentary source located in this audit.")
ME7_  = "Afghan MoE Biology Grade 7 (moe.gov.af, Kabul 1398)"
ME12_ = "Afghan MoE Science Grade 12 (moe.gov.af)"
S5_   = "Afghan faculty histology text: خاتم النبیین University, «هستولوژی تئوری ۲» (muslimuniversity.edu.af)"
TOL_  = "TolAfghan (tolafghan.com), «فزیولوژی حجره» — Afghan cell-physiology text"

SOURCE_FIX = {
    # ---- owner-mandated: the user's own canonical list ---------------------
    "مسطح":       (OWNER, "AFGHAN STANDARD", "MEDIUM"),
    "اپیتلیوم":   (OWNER, "AFGHAN STANDARD", "MEDIUM"),
    "شریانچه":    (OWNER, "AFGHAN STANDARD", "MEDIUM"),
    "وریدچه":     (OWNER, "AFGHAN STANDARD", "MEDIUM"),

    # ---- now anchored to a document actually read --------------------------
    "مایکروسکوپ نوری": (ME7_ + " — «مایکروسکوپ مرکب نوری»، «مایکروسکوپ نوری و اجزای آن»",
                        "AFGHAN STANDARD", "HIGH"),
    "مایکروسکوپ الکترونی": (ME7_ + " — «مایکروسکوپ الکتروني: … قوۀ بزرگ نمایی بیشتر از 250000»",
                            "AFGHAN STANDARD", "HIGH"),
    "مریضی":      (ME7_ + " — «چرا مریض میشوید و به داکتر مراجعه میکنید؟»؛ «امراض مختلف»",
                   "AFGHAN STANDARD", "HIGH"),
    "امراض":      (ME7_ + " — «در مورد امراض مختلف؛ مانند: انفلونزا، ایدز»", "AFGHAN STANDARD", "HIGH"),
    "وقایه":      (ME12_ + " — «وقايه: تطبيق واکسين مربوطه از تولد الي سن پنج سالگي»",
                   "AFGHAN STANDARD", "HIGH"),
    "انساج":      (ME7_ + " — «سطوح تنظیم در موجودات زنده، انساج، انساج نباتی»",
                   "AFGHAN STANDARD", "HIGH"),
    "لایزوزوم":   (S5_ + " — writes لایزوزوم/لیزوزم", "AFGHAN STANDARD", "MEDIUM"),
    "رایبوزوم":   (TOL_ + " — «رایبوزوم»/«ریبوزوم» in the RER discussion; AfghanVet likewise",
                   "AFGHAN STANDARD", "MEDIUM"),
    "ریه":        ("Afghan hospital clinical text (mehrabanhospital.af) — «کیست ها و تومورهای ریه»، "
                   "«بذل پریکارد قلب و ریه»؛ a second Afghan hospital department list uses «شش»",
                   "AFGHAN STANDARD", "MEDIUM"),
    "پانکراس":    ("Afghan hospital clinical text (mehrabanhospital.af) — «مری، معده، روده کوچک، "
                   "روده بزرگ، کبد، لوزالمعده»", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
    "عفونت":      ("Afghan clinical directory entry, Kabul infectious-disease practice (findglocal AF) — "
                   "«تداوی امراض مختلفه انتانی (عفونت، مکروبی)»؛ MoE Grade 8 uses «انتانی»",
                   "AFGHAN STANDARD", "MEDIUM"),

    # ---- no Afghanistan-specific source located ----------------------------
    "غشا":        (NODOC + " Orthographic variant only (غشا / غشاء); the book uses غشا "
                           "consistently (302x, غشاء 0x).", "AFGHAN STANDARD", "MEDIUM"),
    "آلرژی":      (NODOC + " Kept deliberately: Afghan clinical text uses «حساسیت» for allergy, but "
                           "in this book حساسیت already means hypersensitivity («حساسیت فوری»), a "
                           "different concept, so substituting would collide.",
                   "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
    "لنفوئید":    (NODOC + " Related Afghan form لنفاوی is attested (" + S5_ + " «ندول لنفاوی»); the "
                           "-oid adjective itself is a direct transliteration.",
                   "AFGHAN STANDARD", "MEDIUM"),
    "ایون":       (NODOC, "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
    "اسلاید":     (NODOC + " " + ME7_ + " uses «سالید» for a microscope slide; اسلاید is the "
                           "established laboratory form.", "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
    "یوروتلیوم":  (NODOC, "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
    "میکروویلی":  (NODOC, "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
    "لامینای پایه": (NODOC, "COMMON AFGHAN TRANSLITERATION", "MEDIUM"),
    "نسج اپیتلیال": (NODOC + " " + S5_ + " uses «اپیتلیوم» unattached.", "AFGHAN STANDARD", "MEDIUM"),
    "بین‌حجروی":  (NODOC, "AFGHAN STANDARD", "MEDIUM"),
    "خارج‌حجروی": (NODOC, "AFGHAN STANDARD", "MEDIUM"),
    "درون‌حجروی": (NODOC, "AFGHAN STANDARD", "MEDIUM"),

    # ---- course/discipline names ------------------------------------------
    "اناتومی":    ("Afghan MoHE Biology curriculum, «بیولوژی نوی نصاب» (logu.edu.af) and Afghan medical-curriculum "
                   "course lists (kateb.edu.af) — «اناتومی»", "AFGHAN STANDARD", "HIGH"),
    "فزیولوژی":   (TOL_ + "; Afghan medical-curriculum course lists (kateb.edu.af) — «فزیولوژی»",
                   "AFGHAN STANDARD", "HIGH"),
    "طب":         ("Afghan MoPH register (moph.gov.af) and Afghan medical-curriculum titles (kateb.edu.af, طب معالجوی) — «طب»",
                   "AFGHAN STANDARD", "HIGH"),
    "شفاخانه":    ("Afghan MoPH official recruitment register (moph.gov.af) — «شف دیپارتمنت پتالوژی ولابراتوار»، «شفاخانه»",
                   "AFGHAN STANDARD", "HIGH"),
    "محصل":       ("Afghan MoHE curriculum document (logu.edu.af) — «محصلان می توانند …»",
                   "AFGHAN STANDARD", "HIGH"),
    "پوهنحی":     ("Afghan MoHE academic-post announcement (mohe.gov.af) — «بست هستوپتالوژی پوهنحی طب»",
                   "AFGHAN STANDARD", "HIGH"),
}

# ---- final gate: one more term anchored to a document actually read ------
SOURCE_FIX["شبکه آندوپلاسمی"] = (
    TOL + " — «اعمال شبکه آندوپلاسمی(عمومی): دخالت در میتابولیسم قندها، انزایم گلوکز ۶-فسفاتاز "
          "در سطح داخلی یا غشای شبکه اندوپلاسمی»",
    "AFGHAN STANDARD", "HIGH")


# ---- KUMS corroboration (document read 2026-09-21) -------------------------
# The bulletin uses the book's clinical register throughout: «دیپارتمنت فزیوتراپی
# در شفاخانه تدریسی علی آباد پوهنتون علوم طبی کابل»، «داکتران و استادان»،
# «مریضان که نیاز دارند»، «پوهنځی علوم متمم صحی»، «محصلینی»، «بخش‌های وقایوی و
# تداوی آن». It supplies tier-3 independent support for forms already anchored to
# MoE/MoPH, and it closes the "KUMS = 0 entries" gap recorded in the gate report.
for _term, _quote in (
        ("مریض",   "«… مصدر خدمت به مریضان که نیاز دارند شده باشیم»"),
        ("تداوی",  "«… روی بخش‌های وقایوی و تداوی آن صحبت کرده»"),
        ("داکتر",  "«… شماری از داکتران و استادان امروز … افتتاح شد»"),
        ("پوهنځی", "«بخش فزیوتراپی در چوکات پوهنځی علوم متمم صحی …»"),
        ("شفاخانه", "«… در شفاخانه تدریسی علی آباد پوهنتون علوم طبی کابل»"),
        ("محصل",   "«… محصلینی‌که به این دیپارتمنت … معرفی شدند»"),
):
    _prev = SOURCE_FIX.get(_term)
    _base = _prev[0] if _prev else None
    _dec = _prev[1] if _prev else "AFGHAN STANDARD"
    _conf = _prev[2] if _prev else "HIGH"
    SOURCE_FIX[_term] = ((_base + " ; corroborated by " + KUMS + " — " + _quote)
                         if _base else (KUMS + " — " + _quote), _dec, _conf)

# ---------------------------------------------------------------- write -----
def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        written = 0
        for row in R:
            if row["dari_term"] in DROP_ROWS:
                continue
            if (row["english_term"], row["first_appearance"]) in DEDUP_DROP:
                continue
            ov = OVERRIDES.get(row["dari_term"])
            if ov:
                forb, acc, lat, newdari = ov
                row["forbidden_forms"] = forb
                row["accepted_variants"] = acc
                if lat:
                    row["latin_term"] = lat
                if newdari:
                    row["dari_term"] = newdari
                    row["preferred_form"] = f"{newdari} ({row['english_term']})"
            # --- pass 3: evidence anchoring + invented-form blacklist ---
            ev = EVIDENCE_OVERRIDES.get(row["dari_term"])
            if ev:
                row["source_authority"], row["decision"], row["confidence"] = ev
            sf = SOURCE_FIX.get(row["dari_term"])
            if sf:
                row["source_authority"], row["decision"], row["confidence"] = sf
            elif row["source_authority"].strip().startswith("Afghan medical education usage"):
                row["source_authority"] = NO_DOC_FOUND
                if row["decision"] == "AFGHAN STANDARD":
                    row["confidence"] = "MEDIUM"
            extra = sorted({v for k, v in INVENTED_CONSTRUCTIONS.items()
                            if k.startswith(row["dari_term"]) or row["dari_term"] in k})
            if row["dari_term"] in INVENTED_CONSTRUCTIONS:
                pass
            forb = [f for f in row["forbidden_forms"].split(";") if f.strip()]
            for form, target in INVENTED_CONSTRUCTIONS.items():
                if target.startswith(row["dari_term"]) and form not in forb:
                    forb.append(form)
            row["forbidden_forms"] = ";".join(forb)
            # A form is prohibited here because it was CONSTRUCTED (or adopted from
            # Iran only alongside an Afghan form), never merely because Iran uses it.
            # Tag those forms so the scanner reports them as non-canonical rather
            # than as Iranian-Persian violations.
            constructed = sorted(f for f in forb if f in INVENTED_CONSTRUCTIONS)
            if constructed:
                row["usage_notes"] = (row["usage_notes"].rstrip()
                                      + " [NON-CANONICAL: " + ";".join(constructed) + "]").strip()
            w.writerow(row)
            written += 1
    print(f"wrote {written} rows -> {OUT} ({len(R) - written} duplicate/withdrawn rows skipped)")


if __name__ == "__main__":
    main()
