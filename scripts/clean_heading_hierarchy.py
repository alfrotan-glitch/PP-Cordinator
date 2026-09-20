# -*- coding: utf-8 -*-
import re

def clean_book1_headings(text):
    # Demote nested ## inside Part 8
    # Keep only ## فصل اول through ## فصل بیست‌وچهارم as ##
    # All other ## become ###
    lines = text.split('\n')
    out = []
    persian_ordinals = [
        "اول", "دوم", "سوم", "چهارم", "پنجم", "ششم", "هفتم", "هشتم", "نهم", "دهم",
        "یازدهم", "دوازدهم", "سیزدهم", "چهاردهم", "پانزدهم", "شانزدهم", "هفدهم", "هجدهم", "نوزدهم", "بیستم",
        "بیست‌ویکم", "بیست‌ودوم", "بیست‌وسوم", "بیست‌وچهارم"
    ]
    valid_chap_titles = [f"فصل {o}" for o in persian_ordinals]
    
    for l in lines:
        if l.startswith('## '):
            title = l[3:].strip()
            # check if it starts with one of valid_chap_titles
            is_valid = any(title.startswith(v) for v in valid_chap_titles)
            if not is_valid:
                out.append('### ' + title)
            else:
                out.append(l)
        else:
            out.append(l)
    return '\n'.join(out)

def clean_book2_headings(text):
    lines = text.split('\n')
    out = []
    persian_ordinals = [
        "اول", "دوم", "سوم", "چهارم", "پنجم", "ششم", "هفتم", "هشتم", "نهم", "دهم",
        "یازدهم", "دوازدهم", "سیزدهم", "چهاردهم", "پانزدهم", "شانزدهم", "هفدهم", "هجدهم", "نوزدهم", "بیستم",
        "بیست‌ویکم", "بیست‌ودوم", "بیست‌وسوم", "بیست‌وچهارم", "بیست‌وپنجم", "بیست‌وششم", "بیست‌وهفتم", "بیست‌وهشتم", "بیست‌ونهم"
    ]
    valid_chap_titles = [f"فصل {o}" for o in persian_ordinals]
    
    for l in lines:
        if l.startswith('## '):
            title = l[3:].strip()
            is_valid = any(title.startswith(v) for v in valid_chap_titles)
            if not is_valid:
                out.append('### ' + title)
            else:
                out.append(l)
        else:
            out.append(l)
    return '\n'.join(out)

# Clean Book 1
with open('manuscript/master.md', 'r', encoding='utf-8') as f:
    b1 = f.read()
b1_clean = clean_book1_headings(b1)
with open('manuscript/master.md', 'w', encoding='utf-8') as f:
    f.write(b1_clean)

# Clean Book 2
with open('manuscript/health_management_master.md', 'r', encoding='utf-8') as f:
    b2 = f.read()
b2_clean = clean_book2_headings(b2)
with open('manuscript/health_management_master.md', 'w', encoding='utf-8') as f:
    f.write(b2_clean)

print("Heading hierarchies cleaned successfully!")
