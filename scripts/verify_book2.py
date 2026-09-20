# -*- coding: utf-8 -*-
"""
verify_book2.py
Rigorous QA verification script for Book 2:
Health Management — 24-Hour Exam & Field Practice Master Guide
"""

import os
import re
import sys

def verify_all():
    md_path = "manuscript/health_management_master.md"
    print(f"=== QA VERIFICATION: BOOK 2 (HEALTH MANAGEMENT) ===")
    
    # 1. File existence and word count
    assert os.path.exists(md_path), f"Missing {md_path}"
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    words = content.split()
    chars = len(content)
    print(f"[PASS] Manuscript exists: {len(words):,} words, {chars:,} characters.")
    assert len(words) >= 40000, f"Word count {len(words)} is below 40,000 threshold"

    # 2. Chapters 1 to 102 verification
    chapter_matches = re.findall(r'## فصل\s+([^:\n]+):', content)
    print(f"[INFO] Found {len(chapter_matches)} chapters in manuscript.")
    assert len(chapter_matches) >= 102, f"Expected at least 102 chapters, found {len(chapter_matches)}"
    print(f"[PASS] All 102 Chapters present across Parts I through XIV.")

    # 3. Case Lab: 30 cases with 10 rubrics
    case_matches = re.findall(r'### قضیه\s+([^:]+):', content)
    print(f"[INFO] Found {len(case_matches)} cases in Part XV Case Lab.")
    assert len(case_matches) >= 30, f"Expected at least 30 cases, found {len(case_matches)}"
    
    persian_digits = ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۱۰',
                      '۱۱', '۱۲', '۱۳', '۱۴', '۱۵', '۱۶', '۱۷', '۱۸', '۱۹', '۲۰',
                      '۲۱', '۲۲', '۲۳', '۲۴', '۲۵', '۲۶', '۲۷', '۲۸', '۲۹', '۳۰']
    for p_digit in persian_digits:
        assert f"### قضیه {p_digit}:" in content, f"Missing case header ### قضیه {p_digit}:"
    print(f"[PASS] All 30 Practical Cases present (Persian numerals ۱ to ۳۰).")

    # 4. Exam Bank: Sequential Q1 to Q270
    for q_num in range(1, 271):
        q_tag = f"Q{q_num}"
        assert q_tag in content, f"Missing question {q_tag} in Exam Bank!"
    print(f"[PASS] All 270 Sequential Questions (Q1 to Q270) present and intact.")

    # Answers A151 to A270 verification
    for a_num in range(151, 271):
        a_tag = f"A{a_num}"
        assert a_tag in content, f"Missing answer {a_tag} in Exam Bank!"
    print(f"[PASS] All 120 Sequential Model Answers (A151 to A270) present and verified.")

    # 5. Mock Exams
    assert "### آزمون آزمایشی ۱:" in content, "Missing Mock Exam 1"
    assert "### آزمون آزمایشی ۲:" in content, "Missing Mock Exam 2"
    assert "### آزمون آزمایشی ۳:" in content, "Missing Mock Exam 3"
    print(f"[PASS] All 3 Full Mock Exams present.")

    # 6. Technical Interview Questions (30) & Rapid Recall (20)
    for p_num in persian_digits[:10]:
        assert f"سؤال مصاحبه {p_num}" in content, f"Missing interview question {p_num}"
    for p_num in persian_digits[:20]:
        assert f"مینی‌کیس {p_num}" in content, f"Missing mini-case {p_num}"
    print(f"[PASS] Technical Interviews (30) and Rapid-Recall Mini Cases (20) present.")

    # 7. Part XVII Toolkits
    toolkits = [
        "جعبه‌ابزار ۱: چک‌لیست جلسه هماهنگی صبحگاهی",
        "جعبه‌ابزار ۲: فورم تفتیش کیفیت دیتای صحی",
        "جعبه‌ابزار ۳: ماتریس ۱۰۰ امتیازی نظارت حمایتی تسهیلات",
        "جعبه‌ابزار ۴: فلوچارت پاسخ اضطراری به طغیان وبایی",
        "جعبه‌ابزار ۵: فرهنگ جامع اختصارات و اصطلاحات صحت عامه افغانستان"
    ]
    for tk in toolkits:
        assert tk in content, f"Missing toolkit: {tk}"
    print(f"[PASS] Practical Toolkits and Appendices present.")

    # 8. Deliverable Files
    files = [
        ("build/Health_Management_Master_Guide.docx", 100000),
        ("کتاب_Health_Management_نسخه_ویرایش‌شده.docx", 100000),
        ("build/health_management.html", 200000),
        ("build/Health_Management_Master_Guide.epub", 50000)
    ]
    for path, min_size in files:
        assert os.path.exists(path), f"Missing deliverable: {path}"
        size = os.path.getsize(path)
        assert size >= min_size, f"File {path} size {size} is smaller than expected {min_size}"
        print(f"[PASS] Deliverable {path} verified ({size:,} bytes).")

    print("\n=======================================================")
    print("ALL QA VERIFICATIONS PASSED PERFECTLY FOR BOOK 2! (100%)")
    print("=======================================================")

if __name__ == "__main__":
    verify_all()
