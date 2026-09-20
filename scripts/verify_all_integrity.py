# -*- coding: utf-8 -*-
"""
Exhaustive Structural Integrity & Content Verification Test
"""
import re
import sys

with open('manuscript/master.md', 'r', encoding='utf-8') as f:
    text = f.read()

errors = []

# 1. 20 Parts
parts = re.findall(r'^# PART ([^\n:]+):?([^\n]*)', text, re.MULTILINE)
print(f"1. Parts Count: {len(parts)} (Target: 20)")
if len(parts) != 20:
    errors.append(f"Expected 20 parts, found {len(parts)}")

# 2. 62 Chapters
ordinals = [
    'اول', 'دوم', 'سوم', 'چهارم', 'پنجم', 'ششم', 'هفتم', 'هشتم', 'نهم', 'دهم',
    'یازدهم', 'دوازدهم', 'سیزدهم', 'چهاردهم', 'پانزدهم', 'شانزدهم', 'هفدهم', 'هجدهم', 'نوزدهم', 'بیستم',
    'بیست‌ویکم', 'بیست‌ودوم', 'بیست‌وسوم', 'بیست‌وچهارم', 'بیست‌وپنجم', 'بیست‌وششم', 'بیست‌وهفتم', 'بیست‌وهشتم', 'بیست‌ونهم', 'سی‌ام',
    'سی‌ویکم', 'سی‌ودوم', 'سی‌وسوم', 'سی‌وچهارم', 'سی‌وپنجم', 'سی‌وششم', 'سی‌وهفتم', 'سی‌وهشتم', 'سی‌ونهم', 'چهلم',
    'چهل‌ویکم', 'چهل‌ودوم', 'چهل‌وسوم', 'چهل‌وچهارم', 'چهل‌وپنجم', 'چهل‌وششم', 'چهل‌وهفتم', 'چهل‌وهشتم', 'چهل‌ونهم', 'پنجاهم',
    'پنجاه‌ویکم', 'پنجاه‌ودوم', 'پنجاه‌وسوم', 'پنجاه‌وچهارم', 'پنجاه‌وپنجم', 'پنجاه‌وششم', 'پنجاه‌وهفتم', 'پنجاه‌وهشتم', 'پنجاه‌ونهم', 'شصتم',
    'شصت‌ویکم', 'شصت‌ودوم'
]
chapters_found = []
for idx, name in enumerate(ordinals):
    pattern = rf'(?:##|###) فصل {name}[:\s]'
    if re.search(pattern, text):
        chapters_found.append(idx+1)
    else:
        errors.append(f"Missing Chapter {idx+1} (فصل {name})")
print(f"2. Chapters Verified: {len(chapters_found)} / 62")
if len(chapters_found) != 62:
    errors.append(f"Expected 62 chapters, found {len(chapters_found)}")

# 3. 13 Appendices
appendix_names = ['الف', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ی', 'ک', 'ل', 'م']
appendices_found = []
for idx, name in enumerate(appendix_names):
    pattern = rf'(?:##|###) ضمیمه {name}[:\s]'
    if re.search(pattern, text):
        appendices_found.append(idx+1)
    else:
        errors.append(f"Missing Appendix {idx+1} (ضمیمه {name})")
print(f"3. Appendices Verified: {len(appendices_found)} / 13")
if len(appendices_found) != 13:
    errors.append(f"Expected 13 appendices, found {len(appendices_found)}")

# 4. 180 Questions & A1-A180
c32 = re.search(r'## فصل سی‌ودوم.*?(?=## فصل سی‌وسوم)', text, re.DOTALL)
if not c32:
    errors.append("Chapter 32 not found!")
else:
    t32 = c32.group(0)
    q_matches = list(re.finditer(r'^(\d+)\.\s+\*\*(.+?)(?=\n\d+\.|\n###|\n---|\Z)', t32, re.MULTILINE | re.DOTALL))
    print(f"4. Chapter 32 Questions Found: {len(q_matches)} (Target: 180)")
    if len(q_matches) != 180:
        errors.append(f"Expected 180 questions in Chapter 32, found {len(q_matches)}")
    
    # Check numbering 1 to 180 and corresponding answer keys A1 to A180
    q_nums = [int(m.group(1)) for m in q_matches]
    if q_nums != list(range(1, 181)):
        errors.append("Questions in Chapter 32 are not strictly numbered 1 to 180 sequentially")
    
    missing_keys = []
    for m in q_matches:
        num = int(m.group(1))
        body = m.group(0)
        if not re.search(rf'A{num}\b', body):
            missing_keys.append(num)
    if missing_keys:
        errors.append(f"Questions missing exact A{missing_keys} key: {missing_keys}")
    else:
        print(f"   -> 100% of questions 1-180 have verified matching A1-A180 answer keys!")

# 5. 3 Mock Exams
c33 = re.search(r'## فصل سی‌وسوم.*?(?=## فصل سی‌وچهارم)', text, re.DOTALL)
c34 = re.search(r'## فصل سی‌وچهارم.*?(?=## فصل سی‌وپنجم)', text, re.DOTALL)
c35 = re.search(r'## فصل سی‌وپنجم.*?(?=# PART XIV)', text, re.DOTALL)
mock_ok = c33 and c34 and c35
print(f"5. Mock Exams Verified: {3 if mock_ok else 0} / 3")
if not mock_ok:
    errors.append("Mock exams 1, 2, or 3 missing or boundary broken")

# 6. 20 Interview Questions in Chapter 37
c37 = re.search(r'## فصل سی‌وهفتم.*?(?=## فصل سی‌وهشتم)', text, re.DOTALL)
if not c37:
    errors.append("Chapter 37 not found")
else:
    q_iv = re.findall(r'#### س[ؤو]ال (\d+):', c37.group(0))
    print(f"6. Interview Questions Found: {len(q_iv)} / 20")
    if len(q_iv) != 20:
        errors.append(f"Expected 20 interview questions, found {len(q_iv)}")

# 7. 20 Case Responses in Chapter 55
c55 = re.search(r'## فصل پنجاه‌وپنجم.*?(?=## فصل پنجاه‌وششم)', text, re.DOTALL)
if not c55:
    errors.append("Chapter 55 not found")
else:
    cases55 = re.findall(r'^\d+\.\s+\*\*', c55.group(0), re.MULTILINE)
    print(f"7. Chapter 55 Case Responses Found: {len(cases55)} / 20")
    if len(cases55) != 20:
        errors.append(f"Expected 20 case responses in Ch 55, found {len(cases55)}")

# 8. 20 Interview Answers in Chapter 56
c56 = re.search(r'## فصل پنجاه‌وششم.*?(?=## فصل پنجاه‌وهفتم)', text, re.DOTALL)
if not c56:
    errors.append("Chapter 56 not found")
else:
    iv56 = re.findall(r'^\d+\.\s+\*\*', c56.group(0), re.MULTILINE)
    print(f"8. Chapter 56 Interview Answers Found: {len(iv56)} / 20")
    if len(iv56) != 20:
        errors.append(f"Expected 20 interview answers in Ch 56, found {len(iv56)}")

# 9. 10 Integrated Master Cases in Part XVII (Chapters 42-51)
p17 = re.search(r'# PART XVII.*?(?=# PART XVIII)', text, re.DOTALL)
if not p17:
    errors.append("Part XVII not found")
else:
    m_cases = re.findall(r'### فصل (?:چهل|پنجاه)[^\n]+:\s*قضیه جامع (\d+):', p17.group(0))
    print(f"9. Integrated Master Cases Found: {len(m_cases)} / 10")
    if len(m_cases) != 10:
        errors.append(f"Expected 10 master cases in Part XVII, found {len(m_cases)}")

# 10. Duplicate Question Check across all 180 questions
if c32:
    stems = []
    for m in q_matches:
        line1 = m.group(0).splitlines()[0]
        # extract stem after **label:**
        stem = re.sub(r'^\d+\.\s+\*\*[^\*]+\*\*:\s*', '', line1).strip()
        stems.append((m.group(1), stem))
    stem_map = {}
    duplicates = []
    for q_id, s in stems:
        if s in stem_map:
            duplicates.append((stem_map[s], q_id, s))
        else:
            stem_map[s] = q_id
    print(f"10. Duplicate Question Stems: {len(duplicates)}")
    if duplicates:
        errors.append(f"Found duplicate question stems: {duplicates}")

if errors:
    print("\nFAILURES DETECTED:")
    for err in errors:
        print("  -", err)
    sys.exit(1)
else:
    print("\nALL 10 STRUCTURAL INTEGRITY VERIFICATIONS PASSED WITH 100% SUCCESS!")
    sys.exit(0)
