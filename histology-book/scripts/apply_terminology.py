#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_terminology.py — one-shot, auditable application of the Afghan
terminology standard (Terminology Gate, 2026-09) to the book text.

Design rules
------------
1. Phrase rules run BEFORE single-word rules (they need the original context).
2. Single-word rules run longest-source-first, so inflected forms
   (سلول‌های) are rewritten before their base (سلول).
3. Word-boundary guard uses *letters only* (Unicode category Lo). ZWNJ and
   Arabic diacritics (kasra, hamza above) are treated as NON-letters, so
   "بافتِ" and "مویرگ‌ها" are matched while "میلیون" is protected from "یون".
4. Every rule carries an ID and a source so the change is traceable to
   editorial/terminology-decisions.md.
5. Dry-run by default. --apply writes. --audit prints every changed line.

Never run --apply twice: rules are not idempotent for every form
(e.g. a second pass would re-see بافت only if leftovers remain — the
post-check catches that).
"""

import argparse
import glob
import os
import re
import sys
import unicodedata

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(BOOK, "chapters", "*.md"))) + [
    os.path.join(BOOK, "00-front-matter.md")
]

ZWNJ = "\u200c"


def _is_letter(ch: str) -> bool:
    """Arabic-script letter only. ZWNJ and harakat are NOT letters."""
    if ch == ZWNJ:
        return False
    if not ("\u0600" <= ch <= "\u06FF" or "\u0750" <= ch <= "\u077F"):
        return False
    return unicodedata.category(ch) == "Lo"


# ---------------------------------------------------------------- rule set ---
# (id, kind, source, target, note)
# kind: "phrase" = literal replace anywhere; "word" = letter-boundary guarded
RULES = [
    # ---- D1  Cell: سلول -> حجره (CANONICAL DECISION, MOHE/multi-source) ----
    ("D1a", "word", "سلول‌های", "حجراتِ", "Cell, plural construct"),
    ("D1b", "word", "سلول‌هایی", "حجراتی", "Cell, indefinite plural"),
    ("D1c", "word", "سلول‌هایش", "حجراتش", "Cell, 3sg possessive"),
    ("D1d", "word", "سلول‌ها", "حجرات", "Cell, plural"),
    ("D1e", "word", "سلولی", "حجروی", "cellular"),
    ("D1f", "word", "سلول‌های", "حجراتِ", "Cell, plural construct (dup guard)"),
    ("D1g", "word", "سلول", "حجره", "Cell (canonical)"),

    # ---- D2  Tissue: بافت -> نسج / انساج (CANONICAL DECISION) ----
    ("D2a", "word", "بافت‌شناسی", "هستولوژی", "Histology (canonical term)"),
    ("D2b", "phrase", "بافت همبند", "نسج منضم", "Connective tissue (canonical)"),
    ("D2c", "phrase", "بافت پیوندی", "نسج منضم", "Iranian form rejected"),
    ("D2d", "phrase", "بافت پوششی", "نسج اپیتلیال", "Epithelial tissue"),
    ("D2e", "phrase", "بافت اپیتلیال", "نسج اپیتلیال", "Epithelial tissue"),
    ("D2f", "phrase", "بافت عضلانی", "نسج عضلانی", "Muscle tissue"),
    ("D2g", "phrase", "بافت عصبی", "نسج عصبی", "Nervous tissue"),
    ("D2h", "phrase", "بافت چربی", "نسج شحمی", "Adipose tissue"),
    ("D2i", "phrase", "بافت لنفاوی", "نسج لمفوئیدی", "Lymphoid tissue"),
    ("D2j", "phrase", "بافت لنفوئیدی", "نسج لمفوئیدی", "Lymphoid tissue"),
    ("D2k", "phrase", "بافت اسکار", "نسج اسکار", "Scar tissue"),
    ("D2l", "phrase", "بافت گرانولاسیون", "نسج گرانولاسیون", "Granulation tissue"),
    ("D2m", "phrase", "بافت همبندِ", "نسج منضمِ", "Connective tissue + kasra"),
    ("D2n", "word", "بافت‌های", "انساجِ", "Tissue, plural construct"),
    ("D2o", "word", "بافت‌ها", "انساج", "Tissue, plural"),
    ("D2p", "word", "بافتی", "نسجی", "tissue (adj.)"),
    ("D2q", "word", "بافت", "نسج", "Tissue (canonical)"),

    # ---- D3  Squamous: سنگفرشی -> مسطح (CANONICAL DECISION) ----
    ("D3a", "phrase", "سنگفرشی مطبق", "مطبق مسطح", "Stratified squamous word order"),
    ("D3b", "word", "سنگفرشی", "مسطح", "Squamous (canonical)"),

    # ---- D4  Pathology (CANONICAL DECISION, MOPH/MOHE) ----
    ("D4a", "word", "پاتولوژی", "پتالوژی", "Pathology"),

    # ---- D5  Optical instrument ----
    ("D5a", "word", "میکروسکوپ", "مایکروسکوپ", "Microscope (Afghan transliteration)"),

    # ---- D6  Enzyme: MOHE biology curriculum + Afghan histology text ----
    ("D6a", "word", "آنزیم‌های", "انزایم‌های", "enzyme, plural construct"),
    ("D6b", "word", "آنزیم‌ها", "انزایم‌ها", "enzyme, plural"),
    ("D6c", "word", "آنزیمی", "انزایمی", "enzymatic"),
    ("D6d", "word", "آنزیم", "انزایم", "Enzyme"),

    # ---- D7  Chemistry: MOHE curriculum "ساختمان کیمیاوی" ----
    ("D7a", "word", "شیمیایی", "کیمیاوی", "chemical"),
    ("D7b", "word", "شیمی", "کیمیا", "chemistry"),

    # ---- D8  Molecule: MOHE "معافیت حجروی و مالیکولی" ----
    ("D8a", "word", "مولکول‌های", "مالیکول‌های", "molecule, plural construct"),
    ("D8b", "word", "مولکول‌ها", "مالیکول‌ها", "molecule, plural"),
    ("D8c", "word", "مولکولی", "مالیکولی", "molecular"),
    ("D8d", "word", "مولکول", "مالیکول", "Molecule"),

    # ---- D9  Ion (Afghan: ایون) ----
    ("D9a", "word", "یون‌های", "ایون‌های", "ion, plural construct"),
    ("D9b", "word", "یون‌ها", "ایون‌ها", "ion, plural"),
    ("D9c", "word", "یونی", "ایونی", "ionic"),
    ("D9d", "word", "یون", "ایون", "Ion"),

    # ---- D10 Metabolism ----
    ("D10a", "word", "متابولیسم", "میتابولیسم", "Metabolism"),

    # ---- D11 Skin: Afghan histology text "اپیتلیوم جلد" ----
    ("D11a", "word", "پوستی", "جلدی", "cutaneous"),
    ("D11b", "word", "پوست", "جلد", "Skin"),

    # ---- D12 Sebaceous: Afghan "غدوات شحمی" ----
    ("D12a", "phrase", "غدد سباسه", "غدوات شحمی", "sebaceous glands"),
    ("D12b", "phrase", "غدهٔ سباسه", "غدهٔ شحمی", "sebaceous gland"),
    ("D12c", "phrase", "سباسه:", "غدهٔ شحمی:", "sebaceous gland (table label)"),
    ("D12d", "word", "سباسه", "غدهٔ شحمی", "sebaceous"),

    # ---- D13 Nucleolus: Afghan histology text "هسته چه" ----
    ("D13a", "word", "هستک‌های", "هسته‌چه‌های", "nucleolus, plural construct"),
    ("D13b", "word", "هستک‌ها", "هسته‌چه‌ها", "nucleolus, plural"),
    ("D13c", "word", "هستکِ", "هسته‌چهٔ", "nucleolus + kasra"),
    ("D13d", "word", "هستک", "هسته‌چه", "Nucleolus"),

    # ---- D14 Red blood cell: Afghan histology text "کرویات سفید خون" ----
    ("D14a", "word", "گویچهٔ سرخ", "کرویاتِ سرخ", "erythrocyte"),
    ("D14b", "word", "گویچهٔ سفید", "کرویاتِ سفید", "leukocyte (guičeh form)"),
    ("D14c", "word", "گویچه‌های", "کرویاتِ", "blood cell, plural construct"),
    ("D14d", "word", "گویچه‌ها", "کرویات", "blood corpuscles"),
    ("D14e", "word", "گویچه", "کرویات", "blood corpuscle"),

    # ---- D15 Capillary: Afghan histology text "موی رگها" ----
    ("D15a", "word", "مویرگ‌های", "موی‌رگ‌های", "capillary, plural construct"),
    ("D15b", "word", "مویرگ‌ها", "موی‌رگ‌ها", "capillary, plural"),
    ("D15c", "word", "مویرگی", "موی‌رگی", "capillary (adj.)"),
    ("D15d", "word", "مویرگ", "موی‌رگ", "Capillary"),

    # ---- D16 Steroid ----
    ("D16a", "word", "استرویید", "استروئید", "steroid"),

    # ---- D17 Carbohydrate (Afghan transliteration) ----
    ("D17a", "word", "کاربوهیدرات", "کاربوهایدریت", "carbohydrate (dup guard)"),
    ("D17b", "word", "کربوهیدرات", "کاربوهایدریت", "carbohydrate"),

    # ---- D18 Oxidative phosphorylation ----
    ("D18a", "word", "فسفریلاسیون", "فسفوریلیشن", "phosphorylation"),
    ("D18b", "word", "فسفوریلاسیون", "فسفوریلیشن", "phosphorylation (dup guard)"),

    # ---- D19 Disease / patient: Afghan مریضی / مریض ----
    ("D19a", "word", "بیماری‌های", "مریضی‌های", "disease, plural construct"),
    ("D19b", "word", "بیماری‌ها", "مریضی‌ها", "disease, plural"),
    ("D19c", "word", "بیماریِ", "مریضیِ", "disease + kasra"),
    ("D19d", "word", "بیماری", "مریضی", "Disease"),
    ("D19e", "word", "بیماران", "مریضان", "patients"),
    ("D19f", "word", "بیمار", "مریض", "Patient"),

    # ---- D20 Treatment: Afghan تداوی ----
    ("D20a", "word", "پرتودرمانی", "رادیوتراپی", "radiotherapy"),
    ("D20b", "word", "درمانی", "تداوی", "therapeutic"),
    ("D20c", "word", "درمان", "تداوی", "Treatment"),

    # ---- D21 Physician / medicine: Afghan داکتر / طب ----
    ("D21a", "word", "چشم‌پزشکی", "افتالمولوژی", "ophthalmology"),
    ("D21b", "word", "پزشکی", "طب", "medicine (discipline)"),
    ("D21c", "word", "پزشک", "داکتر", "physician"),

    # ---- D22 Carbon ----
    ("D22a", "word", "کربن", "کاربن", "carbon"),

    # ---- D23 Internal consistency: columnar ----
    ("D23a", "word", "ستونی", "استوانه‌ای", "columnar (Afghan canonical form)"),

    # ---- D24 Blood vessels: CANONICAL DECISION اوعیهٔ دموی ----
    ("D24a", "phrase", "رگ‌های خونی و لنفی", "اوعیهٔ دموی و لمفاوی", "blood + lymph vessels"),
    ("D24b", "phrase", "رگهای خونی و لنفی", "اوعیهٔ دموی و لمفاوی", "blood + lymph vessels"),
    ("D24c", "phrase", "رگ‌های خونی", "اوعیهٔ دموی", "blood vessels (canonical)"),
    ("D24d", "phrase", "رگهای خونی", "اوعیهٔ دموی", "blood vessels (canonical)"),
    ("D24e", "phrase", "رگ‌های لنفاوی", "اوعیهٔ لمفاوی", "lymphatic vessels"),
    ("D24f", "phrase", "رگهای لنفاوی", "اوعیهٔ لمفاوی", "lymphatic vessels"),
]

# --------------------------------------------------------------------------
# Pass 2 — inflected / suffixed forms discovered by the post-run inventory.
# These must exist as explicit rules because the letter guard would otherwise
# reject a base form that is legally followed by a suffix letter
# (e.g. سلول + ‌هاست) or protected by a legitimate prefix (ماکرو + مولکول).
# --------------------------------------------------------------------------
RULES += [
    ("E1a", "word", "سلول‌هاست", "حجرات است", "cells + copula"),
    ("E1b", "word", "سلولِ", "حجرهٔ", "cell + kasra"),
    ("E1c", "word", "چندسلولی", "چندحجروی", "multicellular"),
    ("E2a", "word", "بافت‌هاست", "انساج است", "tissues + copula"),
    ("E2b", "word", "بافت‌هایی", "انساجی", "tissues, indefinite"),
    ("E4a", "word", "پاتولوژیک", "پتالوژیک", "pathological"),
    ("E6a", "word", "آنزیم‌هایی", "انزایم‌هایی", "enzymes, indefinite"),
    ("E8a", "word", "ماکرومولکول‌های", "ماکرومالیکول‌های", "macromolecules constr."),
    ("E8b", "word", "ماکرومولکول‌ها", "ماکرومالیکول‌ها", "macromolecules"),
    ("E8c", "word", "ماکرومولکول", "ماکرومالیکول", "macromolecule"),
    ("E8d", "word", "مولکول‌هایی", "مالیکول‌هایی", "molecules, indefinite"),
    ("E5a", "word", "میکروسکوپی", "مایکروسکوپی", "microscopic"),
    ("E11a", "word", "پوست‌های", "جلدهای", "skins, plural construct"),
    ("E16a", "word", "استروییدساز", "استروئیدساز", "steroidogenic"),
    ("E16b", "word", "استروییدهای", "استروئیدهای", "steroids constr."),
    ("E16c", "word", "استروییدها", "استروئیدها", "steroids"),
    ("E16d", "word", "استروییدی", "استروئیدی", "steroidal"),
    ("E17a", "word", "کربوهیدرات‌های", "کاربوهایدریت‌های", "carbohydrates constr."),
    ("E17b", "word", "کربوهیدرات‌ها", "کاربوهایدریت‌ها", "carbohydrates"),
    ("E17c", "word", "کربوهیدراتی", "کاربوهایدریتی", "carbohydrate (adj.)"),
    ("E19a", "word", "بیماری‌هاست", "مریضی‌ها است", "diseases + copula"),
    ("E19b", "word", "بیماری‌زا", "مریضی‌زا", "pathogenic"),
    ("E24a", "word", "رگ‌های", "اوعیهٔ دمویِ", "blood vessels, construct"),
    ("E24b", "word", "رگ‌ها", "اوعیهٔ دموی", "blood vessels (plural)"),
]

# longest source first within each kind; phrase rules first overall
PHRASE_RULES = [r for r in RULES if r[1] == "phrase"]
PHRASE_RULES.sort(key=lambda r: -len(r[2]))
WORD_RULES = [r for r in RULES if r[1] == "word"]
WORD_RULES.sort(key=lambda r: -len(r[2]))

# Forms that must not survive a run. Each entry is checked with the same
# letter-only guard, so "بافته" (woven) and "بیوشیمیایی" are NOT reported.
MALFORMED = ["نسج‌های", "نسج‌ها", "حجره‌ها", "حجره‌های",
             "بافت", "سلول", "سنگفرشی", "پاتولوژی", "پاتولوژیک",
             "آنزیم", "شیمیایی", "مولکول", "ماکرومولکول",
             "متابولیسم", "پوست", "سباسه", "هستک", "گویچه", "مویرگ",
             "استرویید", "کربوهیدرات", "فسفریلاسیون",
             "بیماری", "بیمار", "درمان", "پزشک", "میکروسکوپ", "یون"]


def apply_rules(text, audit_log=None):
    hits = {}

    def bump(rid):
        hits[rid] = hits.get(rid, 0) + 1

    for rid, _kind, src, tgt, note in PHRASE_RULES:
        if src in text:
            n = text.count(src)
            text = text.replace(src, tgt)
            hits[rid] = hits.get(rid, 0) + n
            if audit_log is not None:
                audit_log.append((rid, src, tgt, n, note))

    for rid, _kind, src, tgt, note in WORD_RULES:
        # No regex boundary: a letter-only guard is applied per match instead.
        # That lets ZWNJ compounds (بین‌سلولی -> بین‌حجروی) be rewritten while
        # still protecting true word-internal hits (سلولز, آنیون, کاتیون).
        pat = re.compile(re.escape(src))
        out, last, n = [], 0, 0
        for m in pat.finditer(text):
            s, e = m.span()
            before = text[s - 1] if s > 0 else ""
            after = text[e] if e < len(text) else ""
            if _is_letter(before) or _is_letter(after):
                continue
            out.append(text[last:s]); out.append(tgt)
            last = e; n += 1
        if n:
            out.append(text[last:])
            text = "".join(out)
            hits[rid] = hits.get(rid, 0) + n
            if audit_log is not None:
                audit_log.append((rid, src, tgt, n, note))
    return text, hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--audit", action="store_true")
    args = ap.parse_args()

    total = {}
    for path in FILES:
        raw = open(path, encoding="utf-8").read()
        log = []
        new, hits = apply_rules(raw, log)
        rel = os.path.relpath(path, BOOK)
        if raw != new:
            print(f"\n### {rel}")
            for rid, src, tgt, n, note in log:
                print(f"    [{rid}] {src} -> {tgt}   x{n}   ({note})")
                total[rid] = total.get(rid, 0) + n
        bad = []
        for m in MALFORMED:
            for mm in re.finditer(re.escape(m), new):
                b = new[mm.start() - 1] if mm.start() > 0 else ""
                a = new[mm.end()] if mm.end() < len(new) else ""
                if not _is_letter(b) and not _is_letter(a):
                    bad.append(m)
                    break
        if bad:
            print(f"  !! MALFORMED FORMS in {rel}: {sorted(set(bad))}", file=sys.stderr)
        if args.apply and raw != new:
            open(path, "w", encoding="utf-8").write(new)

    print("\n=== RULE TOTALS ===")
    for rid in sorted(total):
        print(f"  {rid}: {total[rid]}")
    print(f"  TOTAL REPLACEMENTS: {sum(total.values())}")
    if not args.apply:
        print("\n(dry run — nothing written; pass --apply to write)")


if __name__ == "__main__":
    main()
