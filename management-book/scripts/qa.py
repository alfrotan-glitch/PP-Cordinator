#!/usr/bin/env python3
"""
Quality assurance for the whole book.

Runs in one pass:
  1. structure  - parts, chapters, sections, callouts, tables, required counts
  2. language   - Afghan Dari usage, Iranian-Persian contamination, officialese,
                  ZWNJ, punctuation, numerals, mixed-script typos
  3. formats    - DOCX style/TOC/RTL, EPUB structure + EPUBCheck, HTML integrity
  4. output     - qa/qa-report.md (what was checked, what was found, what was fixed)

Exit code is non-zero when a blocking check fails, so the build can gate on it.
"""
from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import unicodedata
import zipfile
from collections import Counter
from pathlib import Path

import mgmtgen
from mgmtgen import ROOT

QA = ROOT / 'qa'
DOCX = ROOT / 'output' / 'مدیریت_مبانی_و_مهارت‌ها.docx'
EPUB = ROOT / 'output' / 'مدیریت_مبانی_و_مهارت‌ها.epub'
HTMLF = ROOT / 'output' / 'مدیریت_نسخهٔ_وب.html'

results = []          # (category, check, ok, detail, blocking)


def add(cat, check, ok, detail='', blocking=False):
    results.append((cat, check, bool(ok), detail, blocking))


# --------------------------------------------------------------- language -----

# Words and forms that are standard in Iran but not used in Afghan Dari, with the
# Afghan equivalent the book must use instead.
IRANIAN = {
    r'\bدانش‌?آموز(ان)?\b': 'شاگرد/شاگردان',
    r'\bدانشجویی?\b': 'محصل (در متن این کتاب کاربرد ندارد)',
    r'\bپزشک(ان)?\b': 'داکتر',
    r'\bبیمار(ان|ها)?\b': 'مریض/مریضان',
    r'\bبیمارستان(‌ها)?\b': 'شفاخانه',
    r'\bمدرسه(‌ها)?\b': 'مکتب',
    r'\bکلاس(‌ها|ی)?\b': 'صنف',
    r'\bگزارش(‌ها|ی|ات)?\b': 'راپور',
    r'\bدرصد\b': 'فیصد',
    r'\bاتومبیل\b': 'موتر',
    r'\bخودرو\b': 'موتر',
    r'\bحقوق\b(?=.{0,12}(کارمند|ماهانه|پرداخت))': 'معاش',
    r'\bویزیت\b': 'مراجعه/معاینه',
    r'\bزنگ زدن\b': 'تماس گرفتن',
    r'\bتلفن\b': 'تلیفون',
    r'\bمحیط زیست\b': 'محیط',
    r'\bواکسیناسیون\b': 'واکسین',
    r'\bمبارزه با بیماری\b': 'کنترول بیماری',
    r'\bهمایش\b': 'نشست/کنفرانس',
    r'\bسازمان‌های مردم نهاد\b': 'نهادهای غیردولتی',
    r'\bتیم‌بندی\b': 'گروه‌بندی',
    r'\bسبک زندگی\b': 'شیوهٔ زندگی',
    r'\bدانشکده\b': 'پوهنځی',
    r'\bفوق‌لیسانس\b': 'ماستری',
    r'\bکارشناسی ارشد\b': 'ماستری',
    r'\bآزمایشگاه\b': 'لابراتوار',
    r'\bخیابان\b': 'سرک',
    r'\bفارغ‌التحصیل\b': 'فارغ',
    r'\bپلیس\b': 'پولیس',
    r'\bدورهٔ متوسطه\b': 'دورهٔ ثانوی',
    r'\bملت\b': 'ملت/مردم (در متن این کتاب: مردم)',
}

# Heavy administrative style that hides the meaning or the responsible person.
OFFICIALESE = {
    r'\bمی\u200cباشد\b': 'است',
    r'(?:انجام|صورت|تهیه|اجرا|ارسال|ثبت|پرداخت|دریافت|بررسی)\s+می\u200cگردد': 'می‌شود',
    r'(?:انجام|صورت|تهیه|اجرا|ارسال|ثبت|پرداخت|دریافت|بررسی)\s+گردید': 'شد',
    r'\bنمودن\b': 'کردن',
    r'\bجهت\s+(?:انجام|اطلاع|اجرا|هماهنگی|شرکت|مشارکت|ورود|دریافت|ارسال|بررسی|رفع|تأمین|پرداخت|تهیه)': 'برای',
    r'\bراجع به\b': 'دربارهٔ',
    r'\bمبادرت\b': 'اقدام',
    r'\bفلذا\b': 'پس',
    r'\bعلیهذ?ا\b': 'بنابراین',
    r'\bبدین\u200cوسیله\b': 'حذف شود',
    r'\bبه استحضار می\u200cرساند\b': 'حذف شود (به‌جای آن: موضوع روشن و درخواست مشخص)',
    r'\bاقدامات مقتضی\b': 'حذف شود (جای آن: چه کسی، چه کار، تا چه زمانی)',
    r'\bدر اسرع وقت\b': 'تا تاریخ مشخص',
    r'\bبا عنایت به\b': 'با توجه به',
    r'\bذیلاً\b': 'در زیر',
    r'\bمرقوم\b': 'نوشته‌شده',
}

# Typographic and orthographic traps in mixed Dari/Latin text.
ARABIC_KAF = '\u0643'          # ك
ARABIC_YEH = '\u064a'          # ي
ARABIC_HEH = '\u06c0'
INDIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'


def scan_language(text: str, lines):
    findings = []
    for pattern, replacement in IRANIAN.items():
        for m in re.finditer(pattern, text):
            findings.append(('واژه‌های ناافغانی', m.group(0), replacement,
                             line_of(lines, m.start())))
    prose = re.sub(r'«[^»]*»', '«…»', text)
    prose = re.sub(r'برمی\u200c?گردد|برگردید', '—', prose)          # to return, not officialese
    prose = re.sub(r'جهت(?=\u200c?(ده|گیری|نما|دهی))|در جهت|جهت\s*دهی', '—', prose)
    for pattern, replacement in OFFICIALESE.items():
        for m in re.finditer(pattern, prose):
            findings.append(('زبان اداری سنگین', m.group(0), replacement,
                             line_of(lines, m.start())))
    return findings


def line_of(lines, pos):
    total = 0
    for n, ln in enumerate(lines, 1):
        total += len(ln) + 1
        if total > pos:
            return n
    return len(lines)


def main():
    master = mgmtgen.MASTER.read_text(encoding='utf-8')
    lines = master.split('\n')
    blocks = mgmtgen.parse(mgmtgen.MASTER)
    docs = mgmtgen.split_documents(blocks)

    # ---------------------------------------------------------- structure ----
    parts = [d for d in docs if d['kind'] == 'part']
    chapters = [d for d in docs if d['kind'] == 'chapter']
    appendices = [d for d in docs if d['kind'] == 'appendix']
    add('ساختار', 'بخش‌های اصلی کتاب', len(parts) == 7, f'{len(parts)} بخش', True)
    add('ساختار', 'فصل‌ها', len(chapters) == 20, f'{len(chapters)} فصل', True)
    add('ساختار', 'پیوست‌ها', len(appendices) >= 4, f'{len(appendices)} پیوست', True)

    counts = Counter(b.kind for b in blocks)
    add('ساختار', 'جعبه‌ها (داستان/کیس/ابزار/هشدار/…)', counts['callout'] >= 90,
        f"{counts['callout']} جعبه", True)
    add('ساختار', 'جدول‌ها', counts['table'] >= 60, f"{counts['table']} جدول", True)
    bad_calls = [b.ctype for b in blocks if b.kind == 'callout'
                 and b.ctype not in mgmtgen.CALLOUTS]
    add('ساختار', 'انواع جعبه‌ها در فهرست مجاز', not bad_calls,
        str(set(bad_calls)) if bad_calls else 'همه مجاز', True)

    # table shape: every row of a table must have the same number of cells
    ragged = 0
    for i, b in enumerate(blocks):
        if b.kind == 'table' and b.items:
            widths = {len(r) for r in b.items}
            if len(widths) > 1:
                ragged += 1
    add('ساختار', 'هم‌شکلی ستون‌های جدول‌ها', ragged == 0, f'{ragged} جدول ناهم‌شکل', True)

    # case laboratory
    case_titles = re.findall(r'^## کیس (\d+) — ', master, re.M)
    add('ساختار', 'شمار کیس‌های مدیریتی', len(case_titles) >= 30,
        f'{len(case_titles)} کیس (مورد نیاز: 30)', True)
    case_steps = len(re.findall(r'\*\*کارگاه', master))
    add('ساختار', 'کارگاه تحلیلی برای هر کیس', case_steps >= 30,
        f'{case_steps} کارگاه', True)

    # exercise inventory
    mcq = len(re.findall(r'^\d+\.\s', master, re.M)) and len(
        re.findall(r'^\d{1,3}\.\s', master, re.M))
    n_scen = master.count('*راهنمای پاسخ*')
    add('کارگاه', 'پرسش سناریویی با راهنمای پاسخ', n_scen >= 30, f'{n_scen} پرسش', True)
    def section_items(start_marker, stop_markers):
        i = master.find(start_marker)
        if i < 0:
            return -1
        j = min([master.find(x, i + 1) for x in stop_markers if master.find(x, i + 1) > 0]
                or [len(master)])
        part = master[i:j]
        nums = [int(n) for n in re.findall(r'^(?:\*\*)?(\d+)\.', part, re.M)]
        return len({n for n in nums if n})

    mcq = section_items('## بخش یکم — 150 پرسش چند گزینه‌ای', ['## بخش دویم'])
    add('کارگاه', 'پرسش چند گزینه‌ای', mcq >= 150, f'{mcq} پرسش', True)
    scen = section_items('## بخش دویم — 30 پرسش سناریویی', ['## بخش سوم'])
    add('کارگاه', 'پرسش سناریویی', scen >= 30, f'{scen} پرسش', True)
    short = section_items('## بخش سوم — 30 پرسش پاسخ کوتاه', ['## بخش چهارم'])
    add('کارگاه', 'پرسش پاسخ کوتاه', short >= 30, f'{short} پرسش', True)
    mini = section_items('## بخش چهارم — 30 کیس کوتاه', ['## بخش پنجم'])
    add('کارگاه', 'کیس کوتاه', mini >= 30, f'{mini} کیس', True)
    dec = section_items('## بخش پنجم — 20 تمرین تصمیم‌گیری', ['## بخش ششم'])
    add('کارگاه', 'تمرین تصمیم‌گیری', dec >= 20, f'{dec} تمرین', True)
    lead = section_items('## بخش ششم — 20 تمرین رهبری', ['## بخش هفتم'])
    add('کارگاه', 'تمرین رهبری', lead >= 20, f'{lead} تمرین', True)
    comm = section_items('## بخش هفتم — 20 تمرین ارتباط', ['## بخش هشتم'])
    add('کارگاه', 'تمرین ارتباط', comm >= 20, f'{comm} تمرین', True)
    inter = section_items('## بخش هشتم — 20 پرسش مصاحبهٔ کاری', ['## بخش نهم'])
    add('کارگاه', 'پرسش مصاحبهٔ کاری', inter >= 20, f'{inter} پرسش', True)
    mocks = len(re.findall(r'^\*\*امتحان آزمایشی', master, re.M))
    add('کارگاه', 'امتحان‌های آزمایشی', mocks == 3, f'{mocks} امتحان', True)
    keys = sum(1 for b in blocks if b.kind == 'table' and b.items
               and b.items[0] and b.items[0][0] == 'پرسش')
    add('کارگاه', 'جدول‌های کلید پاسخ', keys >= 6, f'{keys} کلید (هر 25 پرسش، یک جدول)', True)
    tools = len(re.findall(r'^## ابزار \d+ —', master, re.M))
    add('ابزارها', 'ابزارهای عملی مدیریت', tools == 14, f'{tools} ابزار', True)
    gi = master.find('پیوست 1 — واژه‌نامهٔ اصطلاحات')
    glossary_rows = len(re.findall(r'^\| ', master[gi:master.find('## پیوست 2')], re.M)) \
        if gi > 0 else 0
    add('واژه‌نامه', 'ردیف‌های واژه‌نامه در پیوست', glossary_rows >= 80,
        f'{glossary_rows} اصطلاح', True)

    # ethics coverage: the concepts the book promises must exist with a framework
    ETH = {'صداقت (Integrity)': 'صداقت', 'محرمانگی (Confidentiality)': 'محرمانگی',
           'تضاد منافع (Conflict of Interest)': 'تضاد منافع',
           'سوءاستفاده از صلاحیت (Abuse of Authority)': 'سوءاستفاده از صلاحیت',
           'رفتار حرفه‌ای (Professional Conduct)': 'رفتار حرفه‌ای',
           'تصمیم اخلاقی (Ethical Decision)': 'تصمیم اخلاقی'}
    missing = [k for k, v in ETH.items() if v not in master]
    add('اخلاق', 'شش مفهوم اخلاقی در متن', not missing, f'کامل؛ نبود: {missing}' if missing
        else 'هر شش مفهوم موجود', True)
    add('اخلاق', 'آزمون اخلاقی و مسیر اعلام',
        'آزمون اخلاقی' in master and 'Reporting Channel' in master,
        'آزمون پنج‌پرسشی و مسیر اعلام موجود', True)
    add('اخلاق', 'جعبهٔ اخلاقی در متن', counts['callout'] and ':::ethics' in master,
        'جعبهٔ اخلاقی موجود', False)

    # ----------------------------------------------------------- language ----
    lang = scan_language(master, lines)
    iranian = [f for f in lang if f[0] == 'واژه‌های ناافغانی']
    official = [f for f in lang if f[0] == 'زبان اداری سنگین']
    add('زبان', 'واژه‌های ناافغانی (فارسی ایران)', not iranian,
        '؛ '.join(f'{f[1]} → {f[2]} (خط {f[3]})' for f in iranian[:8]) or 'یافت نشد',
        True)
    add('زبان', 'زبان اداری سنگین (بیرون از نمونه‌های آموزشی)', not official,
        '؛ '.join(f'{f[1]} → {f[2]} (خط {f[3]})' for f in official[:8]) or 'یافت نشد',
        False)

    arabic_chars = [c for c in (ARABIC_KAF, ARABIC_YEH, ARABIC_HEH) if c in master]
    add('زبان', 'حروف عربی (ك، ي) به‌جای ک و ی', not arabic_chars,
        f'یافت شد: {arabic_chars}' if arabic_chars else 'یافت نشد', True)

    stray_letters = {f'U+{ord(c):04X}': c for c in ('\u06d5', '\u0643', '\u064a', '\u0629', '\u0649')
                     if c in master}
    add('زبان', 'حروف ناهمخوان (ە، ك، ي، ة، ى)', not stray_letters,
        f'یافت شد: {stray_letters}' if stray_letters else 'یافت نشد', True)

    REDUPLICATED = ('آرام', 'کم', 'رفته', 'دسته')      # طبیعی در زبان: آرام‌آرام، کم‌کم
    doubled = [m2.group(1) for m2 in re.finditer(r'\b([آ-ی]{3,})[ \u200c]+\1\b', master)
               if '\n' not in master[m2.start():m2.end()] and m2.group(1) not in REDUPLICATED]
    add('زبان', 'واژهٔ تکراری درون یک سطر', not doubled,
        f'{doubled[:5]}' if doubled else 'یافت نشد', True)

    glued = re.findall(r'(?<!\w)یک\u200cاستعاد[آ-ی]*', master)
    add('زبان', 'چسبیدن «یک» به واژهٔ بعدی (خطای دیده‌شده)', not glued,
        f'نمونه: {glued[:5]}' if glued else 'یافت نشد', True)

    wrong_refs = []
    for m2 in re.finditer(r'پیوست\s*(\d)', master):
        n = int(m2.group(1))
        head = re.search(r'# پیوست ' + str(n) + r' — ([^\n]+)', master)
        if head and 'واژه‌نامه' not in head.group(1) and 'پیوست' in master[max(0, m2.start() - 60):m2.start()]:
            wrong_refs.append(m2.group(0))
    add('ارجاع', 'ارجاع به پیوست‌ها', not wrong_refs,
        f'مبهم: {wrong_refs[:5]}' if wrong_refs else 'ارجاع‌ها بررسی شد', False)

    indian = [c for c in INDIAN_DIGITS if c in master]
    add('زبان', 'ارقام یک‌سان (لاتین)', not indian,
        f'ارقام هندی-فارسی: {indian}' if indian else 'همهٔ ارقام لاتین', True)

    # ZWNJ for the "می" prefix
    mi_ok = len(re.findall(r'(?<![آ-ی‌])می\u200c', master))
    SAFE = ('میزان', 'میدان', 'میله', 'میگو', 'میهن', 'میراث', 'میکرب', 'میخانه',
            'میان', 'میانه', 'میلی', 'میکا', 'میرزا', 'میدانی', 'میانگین', 'میز', 'میل')
    mi_bad = [m.group(0) for m in re.finditer(
        r'(?<![آ-ی‌])می(?=[آ-ی])[آ-ی]*', master)
        if not m.group(0).startswith(SAFE)]
    add('زبان', 'نیم‌فاصله پس از «می»', not mi_bad,
        f'{mi_ok} مورد درست؛ نمونه‌های نادرست: {mi_bad[:6]}' if mi_bad
        else f'{mi_ok} مورد با نیم‌فاصله', True)

    # ZWNJ for the plural "ها" after a non-joining letter
    PLAIN_HA = ('تنها', 'آنها', 'بعدها', 'انتها', 'بارها', 'رها', 'ره‌ها')
    ha_bad = [w for w in re.findall(r'[\u0600-\u06FF\u200c]{3,}ها(?=[،.:\s(]|$)', master)
              if '\u200c' not in w and w not in PLAIN_HA]
    add('زبان', 'نیم‌فاصله پیش از «ها»', not ha_bad,
        f'{list(dict.fromkeys(ha_bad))[:8]}' if ha_bad else 'همه با نیم‌فاصله', True)

    add('زبان', 'جهت فلش‌ها با خواندن راست‌به‌چپ',
        '→' not in master and master.count('←') >= 50,
        f"{master.count('←')} فلش چپ‌رو؛ فلش راست‌رو: {master.count('→')}", True)

    double_space = len(re.findall(r'[^\n] {2,}[^\n]', master))
    add('زبان', 'فاصله‌های تکراری درون خط', double_space == 0, f'{double_space} مورد', False)

    prose = '\n'.join(l for l in lines if not l.startswith('@part'))
    space_punct = re.findall(r' [،؛؟!:]', prose)
    add('زبان', 'فاصله پیش از نشانه‌های نقطه‌گذاری', not space_punct,
        f'{len(space_punct)} مورد' if space_punct else 'یافت نشد', False)

    # mixed-script typos: a Dari word with a stray Latin letter inside
    mixed = re.findall(r'[آ-ی]{2}[A-Za-z][آ-ی]', master)
    add('زبان', 'واژه‌های با حروف درهم (دری + لاتین)', not mixed,
        f'{list(dict.fromkeys(mixed))[:5]}' if mixed else 'یافت نشد', True)

    # non-Dari scripts that would be a copy/paste error
    stray = [c for c in set(master)
             if unicodedata.category(c).startswith('L')
             and not re.match(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF'
                              r'\uFE70-\uFEFFA-Za-z]', c)]
    add('زبان', 'حروف از الفبای دیگر', not stray, f'{stray[:10]}' if stray else 'یافت نشد',
        True)

    # ------------------------------------------------------------ formats ----
    add('فرمت', 'DOCX ساخته شده', DOCX.exists(), f'{DOCX.name}', True)
    if DOCX.exists():
        from docx import Document
        d = Document(str(DOCX))
        styles = {p.style.name for p in d.paragraphs}
        need = {'BK Chapter', 'BK Section', 'BK Body', 'BK Part', 'BK List'}
        add('فرمت', 'DOCX از سبک‌های واقعی Word استفاده می‌کند', need <= styles,
            f'{len(styles)} سبک در سند', True)
        body_xml = d.element.body.xml
        toc = 'TOC \\o' in body_xml
        add('فرمت', 'DOCX فهرست خودکار دارد', toc, 'میدان TOC موجود', True)
        rtl = d.element.body.xml.count('w:bidi')
        add('فرمت', 'DOCX راست‌به‌چپ', rtl > 1000, f'{rtl} پاراگراف RTL', True)
        add('فرمت', 'DOCX جدول‌ها', len(d.tables) >= 150, f'{len(d.tables)} جدول', False)

    add('فرمت', 'EPUB ساخته شده', EPUB.exists(), EPUB.name, True)
    check_ok, check_detail = False, 'اجرا نشد'
    if EPUB.exists():
        check_ok, check_detail = run_epubcheck(EPUB)
        add('فرمت', 'EPUBCheck', check_ok, check_detail, True)
        with zipfile.ZipFile(EPUB) as z:
            names = z.namelist()
            opf = next(n for n in names if n.endswith('.opf'))
            opf_text = z.read(opf).decode('utf-8')
            add('فرمت', 'mimetype در ابتدای بسته و بدون فشرده‌سازی',
                names[0] == 'mimetype'
                and z.getinfo('mimetype').compress_type == zipfile.ZIP_STORED,
                'درست', True)
            add('فرمت', 'جهت راست‌به‌چپ در OPF',
                'page-progression-direction="rtl"' in opf_text, 'درست', True)
            nav_text = z.read('EPUB/nav.xhtml').decode('utf-8')
            add('فرمت', 'ناوبری چندسطحی (بخش/فصل/عنوان)',
                nav_text.count('<ol') >= 2 and nav_text.count('<a ') >= 200,
                f'{nav_text.count("<a ")} پیوند ناوبری در {nav_text.count("<ol")} سطح', False)
            add('فرمت', 'حالت شبانه در شیوه‌نامه',
                'prefers-color-scheme' in z.read('EPUB/style/main.css').decode('utf-8'),
                'موجود', True)
            add('فرمت', 'متادیتای دسترس‌پذیری',
                'schema:accessMode' in opf_text and 'accessibilitySummary' in opf_text,
                'موجود', True)
            add('فرمت', 'قلم‌های جاسازی‌شده',
                sum(1 for n in names if n.endswith('.woff2')) == 3,
                f'{sum(1 for n in names if n.endswith(".woff2"))} قلم', True)
            add('فرمت', 'اجازه‌نامهٔ قلم‌ها همراه بسته',
                any('licence' in n for n in names), 'موجود', True)
            ltr_marks = 0
            for n in names:
                if n.endswith('.xhtml'):
                    ltr_marks += z.read(n).decode('utf-8').count('lang="en"')
            add('فرمت', 'نشانه‌گذاری متن لاتین (lang="en")', ltr_marks > 500,
                f'{ltr_marks} مورد', False)

    # every choice line of every exercise must survive into the built editions
    src_options = master.count('الف)')
    if DOCX.exists():
        from docx import Document as _D
        d2 = _D(str(DOCX))
        docx_text = '\n'.join(p.text for p in d2.paragraphs) + '\n' + '\n'.join(
            c.text for t in d2.tables for r in t.rows for c in r.cells)
        add('فرمت', 'گزینه‌های پرسش‌ها در DOCX', docx_text.count('الف)') >= src_options,
            f'{docx_text.count("الف)")} از {src_options} گزینه', True)
        add('فرمت', 'شمارهٔ پیوستهٔ پرسش‌ها در DOCX', '150. ' in docx_text,
            'پرسش 150 موجود' if '150. ' in docx_text else 'شماره‌ها شکسته‌اند', True)
    if EPUB.exists():
        with zipfile.ZipFile(EPUB) as z:
            epub_text = ' '.join(z.read(n).decode('utf-8') for n in z.namelist()
                                 if n.endswith('.xhtml'))
        add('فرمت', 'گزینه‌های پرسش‌ها در EPUB',
            epub_text.count('الف)') >= src_options and 'value="150"' in epub_text,
            f'{epub_text.count("الف)")} از {src_options} گزینه · شمارهٔ 150: '
            f'{"موجود" if chr(118) + "alue=" + chr(34) + "150" + chr(34) in epub_text else "نیست"}',
            True)

    add('فرمت', 'نسخهٔ وب ساخته شده', HTMLF.exists(), HTMLF.name, True)
    if HTMLF.exists():
        doc = HTMLF.read_text(encoding='utf-8')
        add('فرمت', 'HTML یک‌فایل و خودبسنده',
            'data:font/woff2;base64' in doc and 'dir="rtl"' in doc,
            f'{HTMLF.stat().st_size / 1024:.0f} KB', True)
        add('فرمت', 'HTML ساختار معنایی', doc.count('<h1') >= 30 and doc.count('<table') >= 60,
            f'{doc.count("<h1")} عنوان سطح یک، {doc.count("<table")} جدول', False)
        add('فرمت', 'گزینه‌ها و شمارهٔ پرسش‌ها در HTML',
            doc.count('الف)') >= src_options and 'value="150"' in doc,
            f'{doc.count("الف)")} از {src_options} گزینه · شمارهٔ 150: '
            f'{"موجود" if chr(118) + "alue=" + chr(34) + "150" + chr(34) in doc else "نیست"}', True)

    # ------------------------------------------------ reader-visible text ---
    BANNED = ['prompt', 'agent', 'github', 'repository', 'branch', 'commit', 'qa',
              'editorial', 'internal note', 'user request', 'build instruction',
              'development note', 'پرامپت', 'یادداشت داخلی', 'دستورالعمل ساخت',
              'هوش مصنوعی', 'تحریریه', 'مصنوعی', 'نسخهٔ آزمایشی', 'یادداشت تولید']
    visible = master.lower()
    hits = [b for b in BANNED if b in visible]
    add('متن نهایی', 'واژه‌های ممنوع در متن کتاب', not hits, f'یافت شد: {hits}' if hits
        else 'یافت نشد', True)
    if HTMLF.exists():
        doc = HTMLF.read_text(encoding='utf-8')
        stripped = re.sub(r'data:[\w./+-]+;base64,[A-Za-z0-9+/=]+', ' ', doc).lower()
        h2 = [b for b in BANNED if b in stripped]
        add('متن نهایی', 'واژه‌های ممنوع در نسخهٔ وب', not h2, f'یافت شد: {h2}' if h2
            else 'یافت نشد', True)
    if EPUB.exists():
        with zipfile.ZipFile(EPUB) as z2:
            text2 = ' '.join(z2.read(n).decode('utf-8', 'ignore') for n in z2.namelist()
                             if n.endswith('.xhtml')).lower()
        h3 = [b for b in BANNED if b in text2]
        add('متن نهایی', 'واژه‌های ممنوع در EPUB', not h3, f'یافت شد: {h3}' if h3
            else 'یافت نشد', True)
    if DOCX.exists():
        from docx import Document as _Doc
        dd = _Doc(str(DOCX))
        text3 = ('\n'.join(p.text for p in dd.paragraphs) + '\n' + '\n'.join(
            c.text for t in dd.tables for r in t.rows for c in r.cells)).lower()
        h4 = [b for b in BANNED if b in text3]
        add('متن نهایی', 'واژه‌های ممنوع در DOCX', not h4, f'یافت شد: {h4}' if h4
            else 'یافت نشد', True)

    # ---------------------------------------------------------- vocabulary ---
    glossary = ROOT / 'glossary' / 'terminology-glossary.csv'
    add('واژه‌نامه', 'فایل واژه‌نامهٔ اصطلاحات موجود', glossary.exists(),
        glossary.name if glossary.exists() else 'نیست', False)

    writing()
    return 0 if all(ok for _, _, ok, _, blocking in results if blocking) else 1


def run_epubcheck(path: Path):
    import epubcheck
    import jdk4py
    jar = Path(epubcheck.__file__).parent / 'epubcheck.jar'
    java = Path(jdk4py.JAVA_HOME) / 'bin' / 'java'
    proc = subprocess.run([str(java), '-jar', str(jar), str(path)],
                          capture_output=True, text=True, timeout=900)
    out = proc.stdout or ''
    errs = [l for l in out.splitlines() if l.startswith(('ERROR', 'FATAL'))]
    warns = [l for l in out.splitlines() if l.startswith('WARNING')]
    summary = next((l.strip() for l in out.splitlines() if l.startswith('Messages:')), '')
    return (not errs and 'No errors' in out), f'{summary or "بدون خطا"}' + \
        (f' — اولی: {errs[0][:110]}' if errs else '') + \
        (f' — اخطار: {warns[0][:90]}' if warns else '')


def writing():
    QA.mkdir(exist_ok=True)
    (QA / 'preview').mkdir(exist_ok=True)
    blocking_fail = [r for r in results if r[4] and not r[2]]
    lines = ['# گزارش بررسی کیفیت', '',
             'این گزارش، نتیجهٔ بررسی خودکار کتاب است: ساختار، زبان، و سه فایل خروجی.',
             '']
    lines.append(f"- بررسی‌ها: **{len(results)}** · قبول: **{sum(1 for r in results if r[2])}**"
                 f" · رد: **{sum(1 for r in results if not r[2])}**"
                 f" · ردهای بازدارنده: **{len(blocking_fail)}**")
    lines.append('')
    cat = None
    for c, check, ok, detail, blocking in results:
        if c != cat:
            lines.append(f'## {c}')
            lines.append('')
            lines.append('| بررسی | نتیجه | جزئیات |')
            lines.append('|---|---|---|')
            cat = c
        mark = 'قبول' if ok else ('رد (بازدارنده)' if blocking else 'یادداشت')
        lines.append(f'| {check} | {mark} | {detail} |')
        if ok and c == 'زبان':
            pass
    lines.append('')
    lines.append('## وضعیت نهایی')
    lines.append('')
    if blocking_fail:
        lines.append('**NOT READY FOR PUBLICATION** — موارد بازدارنده:')
        lines.extend(f'- {c}: {chk} — {det}' for c, chk, ok, det, bl in blocking_fail)
    else:
        lines.append('**READY FOR PUBLICATION** — همهٔ بررسی‌های بازدارنده قبول شده‌اند؛ '
                     'یادداشت‌های غیربازدارنده در جدول‌های بالا آمده است.')
    (QA / 'qa-report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')

    # console summary
    print(f'QA: {len(results)} checks · '
          f'{sum(1 for r in results if r[2])} pass · '
          f'{sum(1 for r in results if not r[2])} notes/fail · '
          f'{len(blocking_fail)} blocking')
    for c, chk, ok, det, bl in results:
        if not ok:
            print(f'   [{"BLOCK" if bl else "note "}] {c} :: {chk} :: {det[:140]}')
    print(f'   report -> {QA / "qa-report.md"}')


if __name__ == '__main__':
    sys.exit(main())
