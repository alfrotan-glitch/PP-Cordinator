# -*- coding: utf-8 -*-
"""
builder_rebuild_b2.py
Master Rebuilder for Book 2:
Health Management — Professional Learning & Field Practice
Consolidates 119 fragmented half-page chapters into 29 substantial, fully developed chapters
covering all 76 core health management topics.
"""

import os
import sys
import re

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('builder_hm'))

import assemble_master
import build_part16_domain

def rebuild_book2():
    print("=== REBUILDING BOOK 2: HEALTH MANAGEMENT ===")
    
    # 1. Assemble raw text from builder_hm including domain bank
    raw_text = assemble_master.get_meta_text() + "\n\n"
    raw_text += assemble_master.get_part1_2_text() + "\n\n"
    raw_text += assemble_master.get_part3_4_text() + "\n\n"
    raw_text += assemble_master.get_part5_6_text() + "\n\n"
    raw_text += assemble_master.get_part7_8_text() + "\n\n"
    raw_text += assemble_master.get_part9_10_text() + "\n\n"
    raw_text += assemble_master.get_part11_12_text() + "\n\n"
    raw_text += assemble_master.get_part13_14_text() + "\n\n"
    raw_text += assemble_master.get_part15_cases_text() + "\n\n"
    raw_text += assemble_master.get_mcqs_text() + "\n\n"
    raw_text += build_part16_domain.get_domain_text() + "\n\n"
    raw_text += assemble_master.get_mocks_text() + "\n\n"
    raw_text += assemble_master.get_interviews_text() + "\n\n"
    raw_text += assemble_master.get_part17_tools_text()
    
    print(f"Raw assembled text: {len(raw_text):,} chars, {len(raw_text.split()):,} words")
    
    # 2. Consolidation Strategy:
    lines = raw_text.split('\n')
    output_lines = []
    
    current_chapter_num = 0
    chapter_names_persian = [
        "اول", "دوم", "سوم", "چهارم", "پنجم", "ششم", "هفتم", "هشتم", "نهم", "دهم",
        "یازدهم", "دوازدهم", "سیزدهم", "چهاردهم", "پانزدهم", "شانزدهم", "هفدهم", "هجدهم", "نوزدهم", "بیستم",
        "بیست‌ویکم", "بیست‌ودوم", "بیست‌وسوم", "بیست‌وچهارم", "بیست‌وپنجم", "بیست‌وششم", "بیست‌وهفتم", "بیست‌وهشتم", "بیست‌ونهم"
    ]
    
    major_chapter_starts = {
        1: "ماهیت مدیریت و رهبری در نظام سلامت (Management & Leadership Foundations)",
        4: "تفویض صلاحیت، تصمیم‌گیری و اولویت‌بندی (Delegation, Decision-Making & Prioritization)",
        7: "پویایی تیم‌های صحی، ارتباطات سازمانی و مدیریت تعارض (Team Dynamics & Conflict)",
        10: "ارزیابی نیازمندی‌ها، طراحی و پلان‌گذاری پروژه صحی (Needs Assessment & Planning)",
        14: "پلان کاری تفصیلی، اهداف و فعالیت‌ها (Workplans, Objectives & Activities)",
        17: "زنجیره نتایج، شاخص‌ها و تارگت‌های عملیاتی (Results Chain & Indicators)",
        21: "سیستم تطبیق، پایش و نظارت پروژه (Project Implementation & Monitoring)",
        23: "فلسفه و متدولوژی نظارت حمایوی (Supervision & Supportive Supervision)",
        25: "هنر مربی‌گری، بازخورد سازنده و پلان اقدامات اصلاحی (Coaching, Feedback & CAP)",
        28: "عملیات کلینیک، جریان حرکت مراجعین و سیستم ارجاع (Facility Operations & Patient Flow)",
        32: "کیفیت خدمات، مصئونیت مریض و وقایه از انتان (Quality, Patient Safety & IPC)",
        35: "جریان معلومات صحی، اسناد دست‌اول و پلتفرم DHIS2 (HMIS, Registers & DHIS2)",
        39: "کیفیت دیتا، راستی‌آزمایی و استفاده در تصمیم‌گیری (Data Quality & Verification)",
        42: "استندردهای راپورنویسی پیشرفت و حوادث عاجل (Reporting Standards & Incident Reports)",
        47: "سیستم دوسیه‌بندی، بایگانی و محرمیت اسناد (Documentation & Filing Systems)",
        48: "استخدام شایسته‌سالار، شمولیت و آشناسازی کارمند (HR Recruitment & Onboarding)",
        51: "مدیریت حاضری، رخصتی‌ها، ارزیابی عملکرد و ارتقای ظرفیت (Attendance & Performance)",
        54: "انضباط اداری طبق پالیسی و موازین قانون کار (Administrative Discipline & Policy)",
        55: "پلان‌گذاری بودجه، نظارت مالی و اسناد حمایتی (Health Finance & Budget Monitoring)",
        61: "تدارکات شفاف، لوژستیک و مدیریت گدام ادویه (Procurement, Logistics & Stock)",
        65: "مدیریت دارایی‌ها، تجهیزات و نگهداری وقایوی (Medical Equipment & Maintenance)",
        66: "هماهنگی دولتی و دیپلوماسی سازمانی با ریاست صحت (Government Coordination)",
        68: "روش‌های تحلیل علت ریشه‌ای و بهبود مداوم کیفیت (Quality Improvement & RCA)",
        70: "مدیریت ریسک و آمادگی برای شرایط اضطرار و بحران (Risk & Crisis Management)",
        72: "اخلاق مسلکی، محرمیت و پاسخگویی سازمانی (Professional Ethics & Accountability)",
        75: "صیانت، پالیسی PSEA و پیشگیری از سوءاستفاده (Safeguarding & PSEA)",
        80: "روابط با جامعه، شورای صحی قریه و اعتمادسازی (Community & Shura Engagement)",
    }
    
    in_case_lab = False
    in_exam_bank = False
    
    for line in lines:
        stripped = line.strip()
        
        # Check for Part XV (Case lab)
        if "# PART XV" in stripped or "لابراتوار قضایای عملیاتی" in stripped:
            in_case_lab = True
            current_chapter_num = 28
            output_lines.append(f"# بخش دوازدهم: لابراتوار قضایای جامع و جعبه‌ابزار مسلکی مدیر صحی")
            output_lines.append(f"## فصل بیست‌وهشتم: تحلیل پیشرفته ۳۰ قضیه عملیاتی مدیریت کلینیک و پروژه‌های صحی")
            output_lines.append(f"### 30 Advanced Operational Health Management Cases with Complete 10-Part Rubrics")
            continue
            
        if "# PART XVI" in stripped or "بانک جامع آزمون" in stripped:
            in_exam_bank = True
            output_lines.append(f"### بانک جامع ۲۷۰ سوالی آزمون‌های استخدامی مدیریت صحی")
            continue
            
        if "# PART XVII" in stripped or "جعبه‌ابزار کاربردی" in stripped:
            current_chapter_num = 29
            output_lines.append(f"## فصل بیست‌ونهم: جعبه‌ابزار جامع مدیر صحی: چک‌لیست‌ها، تمپلیت‌های CAP و ماتریس‌های تصمیم‌گیری")
            output_lines.append(f"### Practical Health Management Toolkits, Checklists & Standard Forms")
            continue

        # If it's a chapter header
        m_chap = re.match(r'^##\s+فصل\s+([^\:]+)\:\s*(.*)', stripped)
        if m_chap and not in_case_lab and not in_exam_bank:
            title_text = m_chap.group(2).strip()
            
            is_major = False
            for num, m_title in major_chapter_starts.items():
                if any(k in title_text for k in m_title.split()[:2]):
                    is_major = True
                    break
            
            if is_major and current_chapter_num < 27:
                current_chapter_num += 1
                c_name = chapter_names_persian[current_chapter_num - 1]
                output_lines.append(f"## فصل {c_name}: {title_text}")
            else:
                output_lines.append(f"### {title_text}")
            continue

        if re.match(r'^#\s+PART\s+[IVXLCDM]+', stripped):
            clean_part = re.sub(r'^#\s+PART\s+[IVXLCDM]+\s*—\s*', '# بخش: ', stripped)
            output_lines.append(clean_part)
            continue
            
        output_lines.append(line)

    consolidated_text = '\n'.join(output_lines)
    
    # 3. Apply Afghan Dari polish & Authority boundary enforcement
    import scripts.human_quality_editor as editor
    consolidated_text = editor.polish_manuscript(consolidated_text, is_book2=True)
    
    # Write to manuscript/health_management_master.md
    with open('manuscript/health_management_master.md', 'w', encoding='utf-8') as f:
        f.write(consolidated_text)
        
    print(f"Book 2 successfully compiled: {len(consolidated_text):,} chars, {len(consolidated_text.split()):,} words.")

if __name__ == '__main__':
    rebuild_book2()
