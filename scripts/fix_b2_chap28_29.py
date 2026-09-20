# -*- coding: utf-8 -*-
with open('manuscript/health_management_master.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace duplicate ## فصل بیست‌وهشتم
# First occurrence: 30 Cases (Keep as ## فصل بیست‌وهشتم)
# Second occurrence (around MCQ bank): Make it ### بانک جامع ۲۷۰ سوالی
# Third occurrence (around toolkits): Make it ## فصل بیست‌ونهم: جعبه‌ابزار جامع مدیر صحی و ضمایم مسلکی

parts = text.split('## فصل بیست‌وهشتم:')
print(f"Occurrences of '## فصل بیست‌وهشتم:': {len(parts)-1}")

if len(parts) >= 4:
    fixed = parts[0] + '## فصل بیست‌وهشتم:' + parts[1] + '### بانک جامع آزمون‌های استخدامی مدیریت صحی\n' + parts[2] + '## فصل بیست‌ونهم: جعبه‌ابزار جامع مدیر صحی و ضمایم مسلکی\n' + parts[3]
    with open('manuscript/health_management_master.md', 'w', encoding='utf-8') as f:
        f.write(fixed)
    print("Fixed Book 2 chapters 28 and 29 successfully!")
