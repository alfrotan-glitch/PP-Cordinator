#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_terminology_supplement.py — supplementary pass of the Terminology Gate.

RUN ORDER:  scripts/apply_terminology.py --apply  ->  THIS SCRIPT  ->  qa_scan.py

Why this exists
---------------
`apply_terminology.py` applied the canonical map (سلول -> حجره, بافت -> نسج, ...).
A later, source-anchored review of the **clinical register** found one more genuine
Iranian/Afghan divergence that pass 1 did not cover:

    دارو / دارویی / داروها   (Iranian-Persian)
    دوا  / دوایی  / دواها    (Afghan)

Evidence (Afghan, institutional first):
  * Ministry of Public Health / Afghanistan health report:
      «تمامی خدمات به شمول **دوا** غذا رایگان است»
      «بررسی ... کیفیت **دوا**های در حال فروش»  «بیش از ۹۰۰۰ **دواخانه**»
      «**دواسازی**»  «مصارف **ادویه** دولتی»  «**دوا** خانه»
  * Afghanistan National Medicine & Food Administration (dpmea.gov.af) — the
    ministry is literally named «اداره ملی **ادویه** و غذا»; its own text:
      «محصولات **دوایی**»  «قاچاق **دوا** ها»  «ذخیره **ادویه**»  «توزیع به مریض»
  * Afghan private hospitals: «با استفاده از روش‌های تداوی مختلفی از جمله
    **دوا**های مرتبط»  «با گرفتن **دوا**»  «**دوا** دریافت کرده»
  * Afghan clinical register: «**دواخانه**» (pharmacy) is the universal Afghan form.

  دارو does still appear in Afghan journalistic prose, so this is a *register*
  decision, not a hard ban: Afghan official/clinical writing standardises on
  دوا / دوایی / ادویه / دواخانه, and the book is a clinical teaching text.
  Confidence: MEDIUM-HIGH.

Every rule below is letter-boundary guarded by the same `_is_letter()` test used in
pass 1, so دارو inside a hypothetical compound is never touched.

IDEMPOTENT: every rule maps an Iranian form to an Afghan form; no source form is a
substring of its own target, so running this script twice changes nothing the
second time.
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from apply_terminology import _is_letter          # noqa: E402  (shared guard)

TARGETS = ([os.path.join(ROOT, "00-front-matter.md")] +
           sorted(glob.glob(os.path.join(ROOT, "chapters", "*.md"))))

# Longest source first so that داروهایی is not eaten by دارو.
WORD_RULES = [
    # --- clinical register: drug ------------------------------------------
    ("دارویی‌اند", "دوایی‌اند"),
    ("داروهایی",   "دواهایی"),
    ("داروهای",    "دواهای"),
    ("داروهایش",   "دواهایش"),
    ("داروها",     "دواها"),
    ("دارویی",     "دوایی"),
    ("داروی",      "دوای"),
    ("دارو",       "دوا"),

    # --- internal consistency (book uses one form 20-25x more often) ------
    # The book's dominant Afghan form is سیتوپلاسم (98 uses); سیتوپلازم appeared
    # only 4 times, including the Ch 2 chapter title. Both spellings are current
    # in Afghanistan, so this is a consistency decision, NOT a contamination one.
    ("سیتوپلازم",  "سیتوپلاسم"),

    # Lymphatic family. Afghan histology teaching uses لنفاوی (S5, an Afghan
    # faculty histology text: «ندول لنفاوی»). The book already used لنفاوی 21x
    # but لمفوئید 2x and لمفاوی 2x — an internal split, not a second standard.
    ("لمفوئیدی",   "لنفوئیدی"),
    ("لمفوئید",    "لنفوئید"),
    ("لمفاوی",     "لنفاوی"),
]


def apply_supplement(text):
    """Apply the supplement rules; return (new_text, hit_count)."""
    hits = 0
    for src, dst in sorted(WORD_RULES, key=lambda kv: -len(kv[0])):
        out, last = [], 0
        for m in re.finditer(re.escape(src), text):
            s, e = m.span()
            before = text[s - 1] if s > 0 else ""
            after = text[e] if e < len(text) else ""
            if _is_letter(before) or _is_letter(after):
                continue                      # part of a longer word
            out.append(text[last:s])
            out.append(dst)
            last = e
            hits += 1
        if out:
            out.append(text[last:])
            text = "".join(out)
    return text, hits


def main():
    apply = "--apply" in sys.argv
    total = 0
    for path in TARGETS:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        new, hits = apply_supplement(text)
        total += hits
        name = os.path.relpath(path, ROOT)
        if hits:
            print(f"{name:56s} {hits:4d} replacements"
                  + ("  [written]" if apply else "  (dry run)"))
            if apply:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
        else:
            print(f"{name:56s}    0")
    print(f"\nTOTAL: {total} replacements" + ("" if apply else "  — dry run, nothing written"))
    if not apply:
        print("Re-run with --apply to write.")


if __name__ == "__main__":
    main()
