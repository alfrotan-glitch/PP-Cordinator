# -*- coding: utf-8 -*-
"""
builder_rebuild_b1.py
Master Rebuilder for Book 1:
Provincial Coordinator — Field Management, Operations Leadership & Exam Readiness
Merges fragmented sections into 24 substantive, deeply written, narrative-driven chapters.
"""

import os
import re

def rebuild_book1():
    print("=== REBUILDING BOOK 1: PROVINCIAL COORDINATOR ===")
    
    # Read parts 1-3, 4-6, 7-8 from book1_modules
    import scripts.book1_modules.part1_3 as p1_3
    import scripts.book1_modules.part4_6 as p4_6
    import scripts.book1_modules.part7_8 as p7_8
    
    t1 = p1_3.get_content().strip()
    t2 = p4_6.get_content().strip()
    t3 = p7_8.get_content().strip()
    
    # Read the rich master cases from builder/build_master_cases.py
    import sys
    sys.path.insert(0, 'builder')
    import build_master_cases
    cases_raw = build_master_cases.get_master_cases_text()
    
    # Read the rich 180 questions from builder/build_part13_exams.py
    import build_part13_exams
    exams_raw = build_part13_exams.get_part13_exams_text()
    
    # Read interviews from builder/build_part14_15.py
    import build_part14_15
    interviews_raw = build_part14_15.get_part14_15_text()
    
    # Read appendices from builder/build_appendices.py
    import build_appendices
    appendices_raw = build_appendices.get_appendices_text()
    
    # Clean up and normalize cases
    cases_clean = cases_raw
    cases_clean = re.sub(r'^#\s+PART[^\n]*\n', '', cases_clean)
    cases_clean = re.sub(r'^##\s+فصل[^\n]*\n', '', cases_clean)
    
    # Clean up and normalize exams
    exams_clean = exams_raw
    exams_clean = re.sub(r'^#\s+PART[^\n]*\n', '', exams_clean)
    exams_clean = re.sub(r'^##\s+فصل[^\n]*\n', '', exams_clean)
    
    # Clean up interviews
    interviews_clean = interviews_raw
    interviews_clean = re.sub(r'^#\s+PART[^\n]*\n', '', interviews_clean)
    interviews_clean = re.sub(r'^##\s+فصل[^\n]*\n', '', interviews_clean)
    
    # Clean up appendices
    appendices_clean = appendices_raw
    appendices_clean = re.sub(r'^#\s+APPENDICES[^\n]*\n', '', appendices_clean)
    
    # Assemble Part VIII with comprehensive content
    part8 = f"""
# بخش هشتم: لابراتوار قضایای جامع، بانک آزمون و مصاحبه تخصصی
## فصل بیست‌ویکم: ده قضیه ترکیبی جامع ساحوی با راهکار گام‌به‌گام
### 10 Integrated Master Field Cases with Detailed Problem-Solving Rubrics

در این فصل، ده سناریوی چندوجهی و واقعی از دشوارترین چالش‌های عملیاتی ولایت دایکندی ارائه شده است. در هر سناریو، هماهنگ‌کننده ولایتی همزمان با چالش‌های بالینی، مالی، تدارکاتی، امنیتی، دیتایی و روابط محلی مواجه است:

{cases_clean.strip()}

---

## فصل بیست‌ودوم: بانک جامع آزمون تحریری استخدامی: ۱۰۰ پرسش سناریومحور با تحلیل و کلید مدل
### 100 Scenario-Based Written Examination Questions with Comprehensive Answer Keys

این مجموعه، بانک جامع پرسش‌های استاندارد شبیه‌سازی‌شده برای بست هماهنگ‌کننده ولایتی است که حوزه‌های مدیریت، نظارت حمایوی، HMIS، تدارکات ادویه، بودجه، منابع بشری و صیانت را پوشش می‌دهد:

{exams_clean.strip()}

---

## فصل بیست‌وسوم: راهنمای کامل مصاحبه تخصصی: ۳۰ سؤال کلیدی با متدولوژی STAR
### 30 Technical Interview Questions & High-Impact Behavioral Responses

مصاحبه استخدامی هماهنگ‌کننده ولایتی، آزمون سنجش خونسردی، تفکر نقادانه و پایبندی به اصول مدیریتی در شرایط بحرانی است:

{interviews_clean.strip()}

---

## فصل بیست‌وچهارم: جعبه‌ابزار ساحوی هماهنگ‌کننده ولایتی و لغت‌نامه دوزبانه
### Provincial Coordinator Field Toolkit, SOPs & Bilingual Glossary

این جعبه‌ابزار شامل چک‌لیست‌های کاربردی نظارت حمایوی، فورم پلان اقدامات اصلاحی (CAP)، جدول ماتریس اولویت‌بندی، و لغت‌نامه جامع دوزبانه انگلیسی-دری اصطلاحات سکتور صحت است:

{appendices_clean.strip()}
"""

    full_text = f"{t1}\n\n{t2}\n\n{t3.split('# بخش هشتم')[0].strip()}\n\n{part8.strip()}"
    
    # Apply editorial terminological cleanup to ensure 100% natural Afghan Dari
    import scripts.human_quality_editor as editor
    full_text = editor.polish_manuscript(full_text, is_book2=False)
    
    # Clean any internal meta phrases
    full_text = re.sub(r'# PART [IVXLCDM]+\s*—[^\n]*\n', '', full_text)
    
    os.makedirs('manuscript', exist_ok=True)
    with open('manuscript/master.md', 'w', encoding='utf-8') as f:
        f.write(full_text)
        
    print(f"Book 1 successfully compiled: {len(full_text):,} characters, {len(full_text.split())} words.")

if __name__ == '__main__':
    rebuild_book1()
