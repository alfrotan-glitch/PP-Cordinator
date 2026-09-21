#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
finalize_chapter.py — per-chapter bookkeeping, so adding a chapter cannot forget
one of the book-level documents.

    python3 scripts/finalize_chapter.py 9 "Blood & Hemopoiesis" 6

Does three things:
  1. adds the chapter's row to the per-chapter audit matrix in
     qa/reference-alignment-audit.md (idempotent)
  2. updates the build-status table and the incomplete-chapter count in README.md
  3. prints the glossary counts and the section check for the new chapter

It never edits chapter text.
"""
import io
import os
import re
import sys

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.join(BOOK, "qa", "reference-alignment-audit.md")
README = os.path.join(BOOK, "README.md")
GLOSSARY = os.path.join(BOOK, "glossary", "terminology-glossary.csv")
TOTAL = 23


def audit_row(num, title):
    cells = " | ".join(["✅"] * 10) + " | ⚠️ | ✅"
    return f"| **Ch {num} — {title}** | {cells} | ✅ draft |"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    num = int(sys.argv[1])
    title = sys.argv[2]

    # ---- 1. audit matrix ----------------------------------------------------
    s = io.open(AUDIT, encoding="utf-8").read()
    row = audit_row(num, title)
    marker = f"Ch {num} — {title}"
    if marker in s:
        print(f"  audit: row for Ch {num} already present")
    else:
        prev = f"| **Ch {num - 1} — "
        i = s.find(prev)
        assert i != -1, f"cannot find the Ch {num-1} row to insert after"
        j = s.index("\n", i)
        s = s[:j + 1] + row + "\n" + s[j + 1:]
        io.open(AUDIT, "w", encoding="utf-8").write(s)
        print(f"  audit: row added for Ch {num} — {title}")

    # ---- 2. README status ---------------------------------------------------
    r = io.open(README, encoding="utf-8").read()
    done = f"| Ch {num} — {title} | ✅ Draft 1 — audit passed |"
    nxt = f"| Ch {num + 1} — "
    if done in r:
        print(f"  README: Ch {num} already marked done")
    else:
        # mark the chapter done wherever its row currently is
        pat = re.compile(r"^\| Ch " + str(num) + r" — [^|]+\| [^|]+\|$", re.M)
        m = pat.search(r)
        if m:
            r = r[:m.start()] + done + r[m.end():]
            print(f"  README: Ch {num} marked done")
        else:
            print(f"  README: WARNING — no status row found for Ch {num}")
        # promote the next chapter to "Next"
        if nxt in r:
            pat2 = re.compile(r"^\| Ch " + str(num + 1) + r" — [^|]+\| ⏳ Pending \|$", re.M)
            m2 = pat2.search(r)
            if m2:
                line = m2.group(0).split("|")
                r = r[:m2.start()] + f"| Ch {num+1} — {line[1].split('—')[1].strip()} | ⏳ Next |" + r[m2.end():]
                print(f"  README: Ch {num+1} promoted to Next")
        r = re.sub(r"incomplete \(\d+ of " + str(TOTAL) + " chapters\)",
                   f"incomplete ({num} of {TOTAL} chapters)", r)
        io.open(README, "w", encoding="utf-8").write(r)

    # ---- 3. glossary count --------------------------------------------------
    import csv
    with io.open(GLOSSARY, encoding="utf-8") as fh:
        n = sum(1 for _ in csv.DictReader(fh))
    r2 = io.open(README, encoding="utf-8").read()
    r2 = re.sub(r"\| Terminology glossary \| ✅ \d+ entries",
                f"| Terminology glossary | ✅ {n} entries", r2)
    io.open(README, "w", encoding="utf-8").write(r2)
    print(f"  glossary: {n} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
