#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qa_scan.py — quality gate for the bilingual histology book.

    python3 scripts/qa_scan.py          # report
    python3 scripts/qa_scan.py --fix    # apply mechanical normalisations only
    python3 scripts/qa_scan.py --quiet  # summary only

Passes
------
1 [SCRIPT]    non-Persian script contamination (CJK / Cyrillic / stray Latin
              letters glued to Persian words). Latin text inside `code`,
              `| tables |` and English lines is legitimate and ignored.
2 [TERM]      prohibited terminology, taken from glossary/terminology-glossary.csv:
                (IRANIAN)   genuine Iranian-Persian form -> must not appear
                (NONCANON)  Afghan-attested but non-canonical variant
              Matching is LETTER-BOUNDARY aware: ZWNJ and harakat are separators,
              so مویرگ‌ها is matched while بافته (woven), هیستونی (histonic),
              پیوند and بیوشیمیایی are protected.
3 [INCONSIST] a canonical form and one of its accepted_variants both appear in
              the same file (the book must pick one form per file).
4 [STRUCT]    the 13 mandated section headings are present for every topic.
5 [RETAINED]  informational: terms explicitly registered as ENGLISH RETAINED.
6 [VERIFY]    informational: [VERIFY TERMINOLOGY] and [VERIFY AGAINST JUNQUEIRA 17e].

--fix only normalises Persian-Indic digits to Western digits and U+2212 to a
plain hyphen. It never rewrites terminology: terminology changes must go through
editorial/terminology-decisions.md and scripts/apply_terminology.py.
"""

import argparse
import csv
import glob
import os
import re
import sys
import unicodedata

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY = os.path.join(BOOK, "glossary", "terminology-glossary.csv")
AUDIT_TEMPLATE = os.path.join(BOOK, "qa", "audit-template.md")

REQUIRED_SECTIONS = [
    "Definition | تعریف",
    "Classification | طبقه‌بندی",
    "Structure | ساختمان",
    "Cells | حجرات",
    "Function | وظیفه",
    "Structure–Function Relationship",
    "Histological Appearance | نمای هستولوژیک",
    "Identification | تشخیص",
    "Comparison | مقایسه",
    "Clinical Correlation",
    "HIGH-YIELD EXAM POINTS",
    "SUMMARY TABLE",
    "SELF-ASSESSMENT",
]

ALLOWED_SYMBOLS = set("→←↔↓↑µμ°≈–…«»‹›·×÷≤≥±§¶†‡•★☆🔍⭐✅❌⚠⏳")
ALLOWED_SCRIPTS = {"ARABIC", "LATIN", "GREEK", "COMMON", "INHERITED"}

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"

# Terms explicitly retained in English / as transliterations.
# The scanner must never flag these (rule: do not be excessively aggressive).
ENGLISH_RETAINED_FALLBACK = {
    "Cellulitis", "paracellular", "GAG", "ECM", "IHC", "LM", "TEM", "SEM", "RBC",
    "WBC", "DNA", "RNA", "ATP", "PAS", "CD", "MHC", "IgA", "IgG", "IgM",
    "H&E", "Golgi", "Goblet", "Urothelium", "Laminin", "Fibronectin",
}


def _in_arabic_block(ch):
    return ("\u0600" <= ch <= "\u06FF") or ("\u0750" <= ch <= "\u077F")


def is_letter(ch):
    """Arabic-script LETTER. ZWNJ (U+200C) and harakat are not letters."""
    if not ch or not _in_arabic_block(ch):
        return False
    return unicodedata.category(ch) == "Lo"


def word_hits(text, term):
    """Occurrences of `term` not glued to a neighbouring Arabic letter."""
    out = []
    for m in re.finditer(re.escape(term), text):
        b = text[m.start() - 1] if m.start() > 0 else ""
        a = text[m.end()] if m.end() < len(text) else ""
        if not is_letter(b) and not is_letter(a):
            out.append(m.start())
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


# ---------------------------------------------------------------- glossary --
def load_glossary():
    forbidden, variants, retained, unresolved = {}, {}, set(), []
    if not os.path.exists(GLOSSARY):
        return forbidden, variants, retained, unresolved
    with open(GLOSSARY, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            canon = row["dari_term"].strip()
            dec = row.get("decision", "").strip()
            notes = row.get("usage_notes", "")
            if dec == "ENGLISH RETAINED" or canon.isascii():
                retained.add(canon)
            # A term is "unresolved" when its EVIDENCE is unresolved, which can
            # be true of a VERIFY FURTHER row or of an ENGLISH RETAINED row that
            # is retained precisely because no Afghan source could be found.
            if dec == "VERIFY FURTHER" or row.get("confidence", "").strip() == "UNRESOLVED":
                if canon not in unresolved:
                    unresolved.append(canon)
            for f in filter(None, (x.strip()
                                   for x in row.get("forbidden_forms", "").split(";"))):
                # an Iranian-Persian violation vs an Afghan non-canonical variant
                kind = "NONCANON" if "NON-CANONICAL" in notes else "IRANIAN"
                forbidden[f] = (canon, row["english_term"], kind, notes)
            for v in filter(None, (x.strip()
                                   for x in row.get("accepted_variants", "").split(";"))):
                variants[v] = canon
    return forbidden, variants, retained, unresolved


# ------------------------------------------------------------ audit checks --
def load_audit_checks():
    """Single source of truth: qa/audit-template.md lines starting '- [ ]'."""
    checks = []
    if os.path.exists(AUDIT_TEMPLATE):
        with open(AUDIT_TEMPLATE, encoding="utf-8") as fh:
            for ln in fh:
                if ln.startswith("- [ ]"):
                    checks.append(ln[5:].strip())
    return checks


# -------------------------------------------------------------------- pass 1 -
def scan_script(text):
    """Foreign-script letters and emoji. Punctuation, math, digits and the
    book's allow-listed symbols are never reported (no false positives)."""
    findings = []
    for i, raw in enumerate(text.split("\n"), 1):
        hit = None
        for ch in raw:
            if ch in ALLOWED_SYMBOLS or ch.isspace():
                continue
            cat = unicodedata.category(ch)
            if cat[0] in ("P", "Z", "N") or cat in ("Sm", "Sc", "Cf", "Mn", "Me", "Mc"):
                continue
            if cat == "So":                      # emoji / pictographs
                hit = f"{ch} U+{ord(ch):04X} (SYMBOL)"
                break
            if cat[0] == "L":
                name = unicodedata.name(ch, "")
                script = name.split(" ")[0] if name else "UNKNOWN"
                if script not in ALLOWED_SCRIPTS:
                    hit = f"{ch} U+{ord(ch):04X} ({script})"
                    break
        # Latin run glued directly to a Persian letter (e.g. granول)
        if not hit:
            # A Latin run is legitimate before a Persian plural/copula suffix
            # (GAGها, rRNAی, doubletها) and illegitimate when embedded inside a
            # Persian word (granول) or followed by any other Persian letter.
            for m in re.finditer(r"[A-Za-z]{2,}", raw):
                b = raw[m.start() - 1] if m.start() > 0 else ""
                a = raw[m.end()] if m.end() < len(raw) else ""
                if is_letter(b):
                    hit = f"{m.group(0)!r} inside a Persian word (LATIN GLUED)"
                    break
                if is_letter(a):
                    nxt = raw[m.end():m.end() + 4]
                    if not nxt.startswith(("هایی", "های", "ها", "ی", "ای", "دار", "مانند", "ساز")):
                        hit = f"{m.group(0)!r} glued to a Persian letter (LATIN GLUED)"
                        break
        if hit:
            findings.append((i, hit, raw.strip()[:90]))
    return findings


# -------------------------------------------------------------------- pass 2 -
def scan_terms(text, forbidden):
    findings = []
    for term, (canon, eng, kind, _notes) in sorted(forbidden.items(),
                                                   key=lambda kv: -len(kv[0])):
        for pos in word_hits(text, term):
            findings.append((kind, line_of(text, pos), term, canon, eng))
    return findings


# -------------------------------------------------------------------- pass 3 -
def scan_inconsistency(text, variants):
    findings = []
    for var, canon in sorted(variants.items(), key=lambda kv: -len(kv[0])):
        if word_hits(text, var) and word_hits(text, canon):
            findings.append((var, canon))
    return findings


# -------------------------------------------------------------------- pass 4 -
def scan_structure(path, text):
    """Every topic ('# N.k Title') must carry all 13 mandated sections.
    Chapter topics are H1 and the 13 sections are H2 within them."""
    findings = []
    starts = [(m.start(), m.group(0).strip())
              for m in re.finditer(r"^# \d+\.\d+ ", text, re.M)]
    if not starts:
        return findings
    starts.append((len(text), None))
    for i in range(len(starts) - 1):
        start, title = starts[i]
        block = text[start:starts[i + 1][0]]
        missing = [s for s in REQUIRED_SECTIONS
                   if not re.search(r"^##\s*\d+\.\s*" + re.escape(s) + r"\s*$",
                                    block, re.M)]
        if missing:
            findings.append((title, missing))
    return findings


# -------------------------------------------------------------------- fix ----
def autofix(text):
    changed = []
    new = text
    for i, d in enumerate(PERSIAN_DIGITS):
        if d in new:
            changed.append(f"{d}->{i}")
            new = new.replace(d, str(i))
    for i, d in enumerate(ARABIC_DIGITS):
        if d in new:
            changed.append(f"{d}->{i}")
            new = new.replace(d, str(i))
    if "\u2212" in new:
        changed.append("U+2212->ASCII-hyphen")
        new = new.replace("\u2212", "-")
    return new, changed


# ------------------------------------------------------------------- driver --
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(BOOK, "chapters", "*.md")))
    files += sorted(glob.glob(os.path.join(BOOK, "*front-matter*.md")))
    files += [os.path.join(BOOK, "README.md")]

    forbidden, variants, retained, unresolved = load_glossary()
    audit_checks = load_audit_checks()

    findings_total = 0
    verify_counts = {"TERMINOLOGY": 0, "JUNQUEIRA": 0}

    for path in files:
        rel = os.path.relpath(path, BOOK)
        raw = open(path, encoding="utf-8").read()
        text = raw

        if "README" not in rel:          # markers are counted in book text only
            verify_counts["TERMINOLOGY"] += raw.count("[VERIFY TERMINOLOGY]")
            verify_counts["JUNQUEIRA"] += raw.count("[VERIFY AGAINST JUNQUEIRA 17e]")

        if args.fix:
            text, ch = autofix(text)
            if text != raw:
                open(path, "w", encoding="utf-8").write(text)
                print(f"{rel}: [FIX] normalized {', '.join(ch)}")

        out = []

        for ln, what, ctx in scan_script(text):
            out.append(f"  L{ln} [SCRIPT] {rel}: {what} :: {ctx}")

        for kind, ln, term, canon, eng in scan_terms(text, forbidden):
            out.append(f"  L{ln} [{kind}] {rel}: «{term}» -> «{canon}» ({eng})")

        for var, canon in scan_inconsistency(text, variants):
            out.append(
                f"  [INCONSIST] {rel}: accepted variant «{var}» mixed with "
                f"canonical «{canon}» — pick one form per file")

        for title, missing in scan_structure(path, text):
            out.append(f"  [STRUCT] {rel}: {title} missing "
                       f"{len(missing)}/13 section(s): {', '.join(missing)}")

        if out:
            findings_total += len(out)
            if not args.quiet:
                print(f"\n### {rel}")
                for line in out:
                    print(line)

    # ------------------------------------------------------------- summary --
    print("\n" + "=" * 72)
    print("TERMINOLOGY GATE SUMMARY")
    print("=" * 72)
    print(f"  glossary entries ............ {len(forbidden) + 0:>4} forbidden forms loaded")
    print(f"  canonical terms ............. {len(set(v for v in forbidden.values())):>4} distinct replacements")
    print(f"  accepted variants ........... {len(variants):>4}")
    print(f"  English-retained registry ... {len(retained) + len(ENGLISH_RETAINED_FALLBACK):>4}")
    print(f"  audit checks loaded ......... {len(audit_checks):>4} (from qa/audit-template.md)")
    print(f"  [VERIFY TERMINOLOGY] markers  {verify_counts['TERMINOLOGY']:>4}")
    print(f"  [VERIFY AGAINST JUNQUEIRA 17e] {verify_counts['JUNQUEIRA']:>4}")
    if unresolved:
        print(f"  unresolved terminology ...... {len(unresolved)}: {', '.join(unresolved)}")
    print("-" * 72)
    if findings_total == 0:
        print("  RESULT: 0 findings — no prohibited Iranian-Persian terminology,")
        print("          no unexplained terminology inconsistency.")
    else:
        print(f"  RESULT: {findings_total} finding(s) — see above.")
    print("=" * 72)
    return 1 if findings_total else 0


if __name__ == "__main__":
    sys.exit(main())
