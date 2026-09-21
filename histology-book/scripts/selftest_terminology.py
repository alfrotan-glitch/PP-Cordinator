#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest_terminology.py — proves the terminology gate actually works.

Three kinds of check, all against the live glossary and the live scanner:

  1. INJECTION   every forbidden form, injected into sample text, must be caught.
  2. CLEAN       every canonical form and every accepted variant, injected on its
                 own, must NOT be caught.
  3. LOCKED      the specific decisions recorded in editorial/final-terminology-lock.md
                 must hold in the built glossary (carbohydrate, junctions, organelle,
                 chemotherapy, and the non-canonical junction calques).

Run it after changing anything in build_glossary.py:

    python3 scripts/build_glossary.py
    python3 scripts/selftest_terminology.py     # must print ALL PASS
    python3 scripts/qa_scan.py                  # must print RESULT: 0 findings
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_scan  # noqa: E402

FAILURES = []


def check(ok, label):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        FAILURES.append(label)


def main():
    forbidden, variants, retained, unresolved = qa_scan.load_glossary()
    if not forbidden:
        print("glossary empty — nothing to test")
        return 1

    # ------------------------------------------------------------ 1. injection --
    print("\n[1] injection — every forbidden form must be detected")
    missed = [f for f in forbidden if not qa_scan.scan_terms(f"د متن {f} د متن", forbidden)]
    check(not missed, f"all {len(forbidden)} forbidden forms are caught"
                      + (f" — MISSED: {missed}" if missed else ""))

    # ---------------------------------------------------------------- 2. clean --
    print("\n[2] clean — canonical forms and accepted variants must not be flagged")
    import csv as _csv
    with open(qa_scan.GLOSSARY, encoding="utf-8") as fh:
        canon = sorted({row["dari_term"].strip() for row in _csv.DictReader(fh)})
    dirty = [c for c in canon if qa_scan.scan_terms(f"د متن {c} د متن", forbidden)]
    check(not dirty, f"all {len(canon)} canonical forms are clean"
                     + (f" — FLAGGED: {dirty}" if dirty else ""))
    badvar = [v for v in variants if v in forbidden]
    check(not badvar, f"no accepted variant is also a forbidden form"
                      + (f" — CONFLICT: {badvar}" if badvar else ""))

    # --------------------------------------------------------------- 3. locked --
    print("\n[3] locked decisions (editorial/final-terminology-lock.md)")
    dec = {c: (e, k) for c, e, k, _n in forbidden.values()}

    def canon_is(dari_exact, label):
        check(dari_exact in set(canon), f"{label}: canonical form «{dari_exact}» is in the glossary")

    def forbidden_is(form, label):
        check(form in forbidden, f"{label}: «{form}» is enforced as prohibited")

    def not_forbidden(form, label):
        check(form not in forbidden, f"{label}: «{form}» is NOT prohibited")

    def variant_of(form, canon, label):
        check(variants.get(form) == canon, f"{label}: «{form}» is an accepted variant of «{canon}»")

    canon_is("کاربوهایدریت", "Carbohydrate")
    for f in ("کربوهیدرات", "کاربوهیدرات"):
        forbidden_is(f, "Carbohydrate (Persian spelling / misspelling)")
    canon_is("کیموتراپی", "Chemotherapy")
    for f in ("کیمیا تداوی", "کیمیا‌تداوی", "کیمیا درمانی", "شیمی‌درمانی"):
        forbidden_is(f, "Chemotherapy (constructed form)")
    canon_is("Tight junction", "Tight junction")
    canon_is("Adherens junction", "Adherens junction")
    canon_is("Gap junction", "Gap junction")
    for f in ("اتصال چسبنده", "اتصال شکافی"):
        forbidden_is(f, "junction (non-canonical Dari calque)")
    not_forbidden("اتصال مضبوط", "Tight junction (permitted Afghan Dari gloss)")
    canon_is("ارگانل", "Organelle")
    variant_of("اندامک", "ارگانل", "Organelle (accepted Afghan variant)")
    for f in ("کیمیا تداوی", "نورون", "ریزرشته", "ریزپرز", "ریزلوله", "میتوکندریایی"):
        forbidden_is(f, "constructed/non-canonical form")
    # The retained-English registry must carry the three junction terms.
    for t in ("Tight junction", "Adherens junction", "Gap junction"):
        check(t in retained, f"English-retained registry carries «{t}»")
    # Only genuinely unresolved evidence may remain flagged.
    check(unresolved == ["آنتی‌ژن"],
          f"unresolved terminology is exactly [آنتی‌ژن] — got {unresolved}")

    print()
    if FAILURES:
        print(f"SELFTEST: {len(FAILURES)} FAILURE(S)")
        for f in FAILURES:
            print("   -", f)
        return 1
    print("SELFTEST: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
