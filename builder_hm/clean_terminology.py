# -*- coding: utf-8 -*-
"""
Clean non-preferred Iranian loanwords across all builder_hm modules
and replace them with official Afghan Dari terminology according to assets/terminology-glossary.csv.
"""
import glob
import os

replacements = [
    ("بیمارستان", "شفاخانه"),
    ("گزارش‌دهی", "راپوردهی"),
    ("گزارش", "راپور"),
    ("پزشکان", "داکتران"),
    ("پزشک", "داکتر"),
    ("مامایی", "قابلگی"),
    ("ماماها", "قابله‌ها"),
    ("ماما", "قابله"),
    ("مرخصی", "رخصتی"),
    ("هزینه‌ها", "مصارف"),
    ("هزینه", "مصرف"),
    ("انبارداری", "گدام‌داری"),
    ("زایمان‌های", "ولادت‌های"),
    ("زایمان‌ها", "ولادت‌ها"),
    ("زایمان", "ولادت"),
]

builder_files = glob.glob("builder_hm/*.py")

for filepath in builder_files:
    if os.path.basename(filepath) in ["clean_terminology.py"]:
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = content
    for old, new in replacements:
        modified = modified.replace(old, new)
        
    if modified != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(modified)
        print(f"Updated {filepath}")

print("Terminology cleaned in builder files. Re-assembling manuscript...")
