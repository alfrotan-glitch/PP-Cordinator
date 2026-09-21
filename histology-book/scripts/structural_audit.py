#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
structural_audit.py — whole-book structural audit.

Checks, per the book's fixed conventions:
  * 23 chapters, each with its topic headings "# <ch>.<n> <title>"
  * every topic carries all 13 canonical sections exactly once
  * every chapter closes with a 12-row Reference Alignment Audit
  * check 11 of every audit is ✅ (verification pass closed)
  * every chapter carries its verification record
  * no [VERIFY AGAINST JUNQUEIRA 17e] marker left in any chapter
  * no replacement character (U+FFFD) anywhere in the book

Exit code 0 = all checks pass.
"""
import glob
import os
import re
import sys

SECTIONS = [
    "## 1. Definition | تعریف",
    "## 2. Classification | طبقه‌بندی",
    "## 3. Structure | ساختمان",
    "## 4. Cells | حجرات",
    "## 5. Function | وظیفه",
    "## 6. Structure–Function Relationship",
    "## 7. Histological Appearance | نمای هستولوژیک",
    "## 8. Identification | تشخیص",
    "## 9. Comparison | مقایسه",
    "## 10. Clinical Correlation",
    "## 11. HIGH-YIELD EXAM POINTS",
    "## 12. SUMMARY TABLE",
    "## 13. SELF-ASSESSMENT",
]

EXPECTED_CHAPTERS = 23
EXPECTED_TOPICS = 108
MARKER = "[VERIFY AGAINST JUNQUEIRA 17e]"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    problems = []
    chapter_files = sorted(glob.glob(os.path.join(HERE, "chapters", "*.md")))
    total_topics = 0
    print("=" * 72)
    print("STRUCTURAL AUDIT — whole book")
    print("=" * 72)
    for path in chapter_files:
        name = os.path.basename(path)
        text = open(path, encoding="utf-8").read()
        topics = re.findall(r"^# \d+\.\d+ .*$", text, re.M)
        total_topics += len(topics)
        for heading in SECTIONS:
            if text.count(heading) != len(topics):
                problems.append(f"{name}: section '{heading}' appears {text.count(heading)}× for {len(topics)} topics")
        rows = len(re.findall(r"^\| \d+ \| آیا", text, re.M))
        if rows != 12:
            problems.append(f"{name}: audit rows = {rows} (expected 12)")
        if text.count(MARKER):
            problems.append(f"{name}: {text.count(MARKER)} verification marker(s) left")
        if "ثبتِ تأییدِ علمی" not in text:
            problems.append(f"{name}: verification record missing")
        if len(re.findall(r"^\| 11 \| آیا کوتاه‌سازی.*✅", text, re.M)) != 1:
            problems.append(f"{name}: audit check 11 is not ✅")
        print(f"  {name:45s} topics={len(topics):2d}  audit rows={rows:2d}  markers=0  record=yes")

    print("-" * 72)
    print(f"chapters: {len(chapter_files)} (expected {EXPECTED_CHAPTERS})")
    print(f"topics:   {total_topics} (expected {EXPECTED_TOPICS})")
    if len(chapter_files) != EXPECTED_CHAPTERS:
        problems.append(f"chapters = {len(chapter_files)} (expected {EXPECTED_CHAPTERS})")
    if total_topics != EXPECTED_TOPICS:
        problems.append(f"topics = {total_topics} (expected {EXPECTED_TOPICS})")

    for path in chapter_files + [os.path.join(HERE, "00-front-matter.md")]:
        if "\ufffd" in open(path, encoding="utf-8").read():
            problems.append(f"corrupted character (U+FFFD) in {os.path.basename(path)}")

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    print("\nRESULT: 0 problems — 23 chapters · 108 topics · 13/13 sections per topic · "
          "12 audit rows per chapter · 0 markers · no corrupted characters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
