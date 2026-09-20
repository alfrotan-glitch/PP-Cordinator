# -*- coding: utf-8 -*-
"""
editorial_polish.py
Performs precise lexical, orthographic and editorial corrections on both manuscripts:
- manuscript/master.md (Book 1)
- manuscript/health_management_master.md (Book 2)
"""

import re
import os

def polish_manuscript(filepath, is_book1=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Fix accidental word replacements
    replacements = [
        ("ملااقابلهن", "ملاامامان"),
        ("دندانداکتری", "پرسونل طب دندان"),
        ("اخلاق زیست‌داکتری", "اخلاق طبابت و زیست‌طبی (Bioethics)"),
        ("اخلاق داکتری", "اخلاق طبابت (Medical Ethics)"),
        ("باورهای غلط داکتری", "باورهای نادرست طبی"),
        ("کادر قابلگی جایگزین", "قابله مسلکی جایگزین"),
        ("کورس‌های ارتقای ظرفیت قابلگی", "کورس‌های ارتقای ظرفیت قابله‌گی"),
        ("خدمات قابلگی به حیث ستون", "خدمات قابله‌گی به حیث ستون"),
        ("خدمات قابلگی و ولادی", "خدمات قابله‌گی و ولادی"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)

    # 2. Fix tab characters in Book 1 (\t -> proper \times or \text)
    if is_book1:
        text = re.sub(r'1\s*\t\s*imes', r'1 \\times', text)
        text = re.sub(r'3\s*\t\s*imes', r'3 \\times', text)
        text = re.sub(r'10\s*\t\s*imes', r'10 \\times', text)
        text = re.sub(r'12\s*\t\s*imes', r'12 \\times', text)
        text = re.sub(r'\$\t\s*ext\{', r'$\\text{', text)
        # Any remaining stray tabs
        text = text.replace('\t', '    ')

    # 3. Orthography & Punctuation: Nim-faseleh (ZWNJ) normalization
    # Make sure common prefixes and suffixes have ZWNJ: می, نمی, ها, های, هایش, کننده
    zwnj = '\u200c'
    text = re.sub(r'\bمی\s+([آ-ی])', rf'می{zwnj}\1', text)
    text = re.sub(r'\bنمی\s+([آ-ی])', rf'نمی{zwnj}\1', text)
    
    # 4. Remove robotic filler transitions if present
    fillers = [
        (r'نکته بسیار مهم این است که\s*', ''),
        (r'اکنون به بررسی ([^\n]+) می‌پردازیم\.?', r'\1:'),
    ]
    for pattern, repl in fillers:
        text = re.sub(pattern, repl, text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Polished {filepath}: {len(text.split()):,} words, {len(text):,} chars.")

if __name__ == "__main__":
    polish_manuscript("manuscript/master.md", is_book1=True)
    polish_manuscript("manuscript/health_management_master.md", is_book1=False)
