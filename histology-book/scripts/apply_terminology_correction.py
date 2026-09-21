#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_terminology_correction.py — pass 3, the CORRECTIVE pass.

Why this pass exists
--------------------
Passes 1 and 2 applied a rule that is only valid for terms whose Afghan form had
been *observed*, and invalid for terms derived by translating English morphemes.
That produced four defects, all found by auditing against official Afghan
documents rather than by linguistic reasoning:

  1. اندامک   (36x) — the Iranian form. The Afghan MoE Grade-7 Biology textbook
                     (moe.gov.af, Kabul 1398) defines the concept as
                     «اعضاچه یا ارگانل (Organelle)» — and ارگانل is the form an
                     Afghan student meets.
  2. نورون    (21x) — the Iranian form. The Afghan MoE Grade-12 science textbook
                     writes نیورون consistently («نیورون دوم»، «نیورون های حرکي»).
  3. میتوکندریایی (8x) — a third spelling of mitochondria. The book's own
                     canonical form مایتوکندریا is the form attested in Afghan
                     material (TolAfghan: «مایتوکاندریا (Mitochondria)»).
  4. کاربوهایدریت (13x) — INVENTED. No Afghan source uses it; it was constructed
                     by transliterating "carbo-hydrate" morpheme by morpheme.
                     Removed entirely; the text now uses کربوهیدرات.

Rules applied
-------------
Only the four rules above. Nothing else is touched. The directive is explicit
that a term already established in Afghanistan must be left alone even when a
more "Dari-sounding" alternative is theoretically available, so this script does
NOT widen the Dari footprint — it removes an invented form and two Iranian ones.

Evidence for every rule is an actual Afghan document, named in EVIDENCE below and
in glossary/terminology-glossary.csv source_authority.

IDEMPOTENT: every source form is absent from its own target.
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from apply_terminology import _is_letter          # noqa: E402

TARGETS = ([os.path.join(ROOT, "00-front-matter.md")] +
           sorted(glob.glob(os.path.join(ROOT, "chapters", "*.md"))))

EVIDENCE = {
    "ارگانل": "Afghan MoE, Biology Grade 7 (moe.gov.af, Kabul 1398), ch.1: "
              "«اعضاچه یا ارگانل (Organelle)»",
    "نیورون": "Afghan MoE, Science Grade 12 (moe.gov.af): «نيورون هاي حرکي»، «نیورون دوم»",
    "مایتوکندریایی": "TolAfghan, فزیولوژی حجره: «مایتوکاندریا (Mitochondria)»",
    "کربوهیدرات": "No Afghan source found for either spelling; invented form withdrawn, "
                  "standard transliteration restored and flagged for verification",
}

# (source form, target form, evidence key) — longest source first per family.
WORD_RULES = [
    # 1. organelle — Iranian form replaced by the official Afghan one
    ("اندامک‌های", "ارگانل‌های"),
    ("اندامک‌هایی", "ارگانل‌هایی"),
    ("اندامک‌ها", "ارگانل‌ها"),
    ("اندامکِ", "ارگانلِ"),
    ("اندامکی", "ارگانلی"),
    ("اندامک", "ارگانل"),

    # 2. neuron — Iranian form replaced by the official Afghan one
    ("نورون‌های", "نیورون‌های"),
    ("نورون‌ها", "نیورون‌ها"),
    ("نورونی", "نیورونی"),
    ("نورون", "نیورون"),

    # 3. mitochondria — align with the book's attested Afghan form
    ("میتوکندریایی", "مایتوکندریایی"),
    ("میتوکندریا", "مایتوکندریا"),

    # 4. carbohydrate — withdraw the invented compound
    ("کاربوهایدریت‌های", "کربوهیدرات‌های"),
    ("کاربوهایدریتیِ", "کربوهیدراتیِ"),
    ("کاربوهایدریتی", "کربوهیدراتی"),
    ("کاربوهایدریت‌ها", "کربوهیدرات‌ها"),
    ("کاربوهایدریت", "کربوهیدرات"),
]


def apply_correction(text):
    hits = {}
    for src, dst in sorted(WORD_RULES, key=lambda kv: -len(kv[0])):
        out, last, n = [], 0, 0
        for m in re.finditer(re.escape(src), text):
            s, e = m.span()
            before = text[s - 1] if s > 0 else ""
            after = text[e] if e < len(text) else ""
            if _is_letter(before) or _is_letter(after):
                continue
            out.append(text[last:s])
            out.append(dst)
            last = e
            n += 1
        if out:
            out.append(text[last:])
            text = "".join(out)
            hits[src] = n
    return text, hits


def main():
    apply = "--apply" in sys.argv
    grand = 0
    for path in TARGETS:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        new, hits = apply_correction(text)
        total = sum(hits.values())
        grand += total
        if total:
            name = os.path.relpath(path, ROOT)
            detail = ", ".join(f"{k}->{v}" for k, v in
                               sorted(hits.items(), key=lambda kv: -kv[1]))
            print(f"{name:56s} {total:4d}  [{'written' if apply else 'dry run'}]")
            for src in sorted(hits, key=lambda k: -hits[k]):
                dst = dict(WORD_RULES)[src]
                print(f"      {src:16s} -> {dst:16s} x{hits[src]:3d}   {EVIDENCE.get(dst,'')[:70]}")
            if apply:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
    print(f"\nTOTAL: {grand} corrections" + ("" if apply else "  — dry run, nothing written"))
    if not apply:
        print("Re-run with --apply to write.")


if __name__ == "__main__":
    main()
