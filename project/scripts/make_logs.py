#!/usr/bin/env python3
"""
Phase 8 — produce the editorial change log, the scientific correction log and the
publication readiness report from the same tables the edits were made from, so the
logs cannot drift out of sync with the manuscript.
"""
import csv
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / 'project/logs'
MASTER = ROOT / 'project/manuscript/master.md'

spec = importlib.util.spec_from_file_location('patch_curated',
                                              ROOT / 'project/scripts/patch_curated.py')
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)


def load_automated():
    rows = []
    with (LOGS / 'automated-change-log.csv').open(encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def short(s, n=150):
    s = re.sub(r'\s+', ' ', s)
    return (s[:n] + '…') if len(s) > n else s


def main():
    master = MASTER.read_text(encoding='utf-8')
    auto = load_automated()

    # ---------------- editorial change log --------------------------
    lines = ['# لاگ تغییرات ویرایشی — Editorial Change Log', '',
             '**کتاب:** قانون زبان — راهنمای جامع و عملی Provincial Coordinator · '
             '**نسخه:** دوم (۱۴۰۵) · **زبان:** دری افغانی', '',
             'کلاس‌بندی‌ها مطابق `references/editorial-workflow.md`: '
             'Editorial · Terminological · Scientific correction · Clinical correction · '
             'Updated evidence · Structural · Formatting · Publication/prepress.', '',
             '## ۱. تغییرات ساختاری این نسخه (Structural)', '',
             '| # | تغییر | شرح |', '|---|---|---|',
             '| S0 | صفحه جلد | جلد تایپوگرافیک با همان فونت متن (Vazir) برای DOCX/PDF/EPUB ساخته شد. |',
             '| S1 | پیشگفتار، «درباره این کتاب»، «چگونه از این کتاب استفاده کنیم» و «نقشه راه ده فصل» | بخش‌های آغازین که در نسخه قبلی نبود، نوشته شد. |',
             '| S2 | «فهرست اختصارات» (۲۹ اصطلاح) | به آغاز کتاب اضافه شد. |',
             '| S3 | «اهداف این فصل» | به شروع هر ده فصل اضافه شد (OBJ). |',
             '| S4 | «فهرست مطالب» | در DOCX به فیلد خودکار Word (با به‌روزرسانی خودکار در زمان باز شدن)، در PDF با شماره صفحه، در EPUB با nav تبدیل شد؛ دستور «کلیک راست ← Update Field» از متن حذف شد. |',
             '| S5 | بخش ۳.۸ «نظام صحی افغانستان امروز (۱۴۰۵)» | بخش جدید افزوده شد (S01). |',
             '| S6 | پیوست‌های ۱ تا ۵ | واژه‌نامه، قالب‌های کاری، پلان ۹۰ روزه، راهنمای امتحان/مصاحبه، منابع. |',
             '| S7 | «درباره این نسخه» | صفحه اطلاعات نسخه، سلسله نسخه‌ها و روش ویرایش. |',
             '']

    sci = [x for x in pc.EDITS if x[1] in ('Scientific correction', 'Clinical correction',
                                           'Updated evidence')]
    lines += ['## ۲. تصحیحات علمی و کلینیکی (Scientific / Clinical / Updated evidence)', '',
              'در هر مورد، **متن اصلی** نگه‌داری شده است تا نویسنده بتواند تصحیح را بازبینی کند.',
              '']
    for cid, cls, reason, old, new, expect in sci:
        lines += [f'### {cid} — {cls}', '',
                  f'**دلیل:** {reason}', '',
                  '**متن اصلی:**', '', f'> {short(old, 700)}', '',
                  '**متن اصلاح‌شده:**', '', f'> {short(new, 700)}', '']
    for cid, cls, reason, anchor, payload in pc.NEW_SECTIONS:
        lines += [f'### {cid} — {cls}', '', f'**دلیل:** {reason}', '',
                  f'**بخش جدید:** {anchor.replace("###", "").strip()}', '']

    lines += ['## ۳. تصحیحات اصطلاحی (Terminological)', '',
              '| قاعده | تغییر | تعداد |', '|---|---|---|']
    for r in auto:
        if r['classification'] == 'Terminological':
            lines.append(f"| {r['rule']} | {r['description']} | {r['hits']} |")
    lines += ['', 'این قواعد در `project/scripts/normalize.py` تعریف شده‌اند و روی کل '
              'متن اجرا می‌شوند؛ جدول کامل در `automated-change-log.csv` است.', '',
              '## ۴. ویرایش زبانی و صفحه‌آرایی (Editorial / Formatting)', '',
              '| قاعده | تغییر | تعداد |', '|---|---|---|']
    for r in auto:
        if r['classification'] in ('Editorial', 'Formatting'):
            lines.append(f"| {r['rule']} | {r['description']} | {r['hits']} |")
    lines += ['', '## ۵. ویرایش‌های موردی (Curated edits)', '',
              '| # | کلاس‌بندی | شرح |', '|---|---|---|']
    for cid, cls, reason, *rest in pc.EDITS:
        lines.append(f'| {cid} | {cls} | {short(reason, 160)} |')
    for key in pc.OBJECTIVES:
        lines.append(f'| OBJ | Structural | «اهداف این فصل» برای {key} |')
    lines += ['', '## ۶. تضمین کیفیت خروجی (Publication/prepress)', '',
              '| # | تغییر | شرح |', '|---|---|---|',
              '| P1 | ایموجی → نشانه تایپوگرافیک | ⭐→★، 🔴→●، ✅→✓، ❌→✗ — فونت‌های متن گلیف ایموجی ندارند و کتاب چاپی نباید ایموجی رنگی داشته باشد. |',
              '| P2 | فونت نمادین | فلش‌ها (← → ↓) با فونت DejaVuSans در PDF چاپ می‌شوند تا هیچ کاراکتری به شکل مربع خالی چاپ نشود. |',
              '| P3 | RTL در EPUB | `dir="rtl"` روی همه اسناد XHTML و `page-progression-direction="rtl"` در OPF تثبیت شد. |',
              '| P4 | فاصله‌گذاری اعداد | اعداد متن دری به ارقام فارسی-هندی (۰–۹) یکدست شد؛ اعداد انگلیسی داخل جواب‌های نمونه انگلیسی به شکل اصلی ماند. |',
              '| P5 | حاشیه آینه‌ای | برای PDF چاپی و DOCX حاشیه آینه‌ای (mirror margins) تنظیم شد. |',
              '']
    (LOGS / 'editorial-change-log.md').write_text('\n'.join(lines), encoding='utf-8')

    # ---------------- scientific correction log ---------------------
    sl = ['# لاگ تصحیحات علمی و کلینیکی — Scientific Correction Log', '',
          'این فایل همان مدخل‌های Scientific correction / Clinical correction / '
          'Updated evidence از لاگ تغییرات ویرایشی است، جداگانه برای بازبینی نویسنده.', '',
          '| # | کلاس‌بندی | مورد | متن اصلی (خلاصه) | تصحیح | منبع تصحیح |', '|---|---|---|---|---|---|']
    sources = {
        'C04': 'تاریخچه رسمی Shuhada Organization', 'C05': 'moph.gov.af — General Directories',
        'C06': 'MoPH, BPHS 2010 (معیار جمعیت مراکز صحی)', 'C07': 'همان (C06)',
        'C08': 'همان (C06)', 'C09': 'MoPH HMIS Procedures Manual (مهلت هفتم ماه)',
        'C10': 'همان (C09)', 'C11': 'MoPH HMIS Procedures Manual (راپور ربعوار)',
        'C12': 'IASC Six Core Principles (PSEA)', 'C13': 'تاریخچه رسمی Shuhada Organization',
        'C14': 'همان (C13)', 'C15': 'همان (C13)', 'C16': 'منابع منتشرشده SO',
        'C17': 'همان (C16)', 'S01': 'UNICEF HER/NFA evaluation؛ WHO EMRO؛ گزارش‌های ۲۰۲۵',
    }
    for cid, cls, reason, old, new, expect in sci:
        sl.append(f'| {cid} | {cls} | {short(reason, 90)} | {short(old, 120)} | '
                  f'{short(new, 120)} | {sources.get(cid, "—")} |')
    sl += ['', '**یادداشت:** هیچ تغییر علمی بدون ثبت متن اصلی انجام نشده است. جایی که '
           'معلومات قابل تأیید نبود (مثلاً شمار کارمندان MoPH)، عدد حذف شد نه اینکه با '
           'عدد تقریبی جایگزین شود.', '']
    (LOGS / 'scientific-correction-log.md').write_text('\n'.join(sl), encoding='utf-8')

    # ---------------- publication readiness -------------------------
    qa = (LOGS / 'qa-report.md').read_text(encoding='utf-8')
    m = re.search(r'\*\*خلاصه:\*\* ([^\n]+)', qa)
    summary = m.group(1) if m else ''
    flags = [
        ('بنیان‌گذار شفاهی/دیگر SO',
         'در متن اصلی «داکتر سیما سمر و عبدالرؤف نوید» آمده بود. متن به «داکتر سیما سمر» '
         'تغییر کرد تا با تاریخچه منتشرشده سازمان بخواند. اگر سازمان سهم بنیان‌گذاران دیگر را '
         'تأیید می‌کند، همان نام‌ها باید بازگردانده شود.'),
        ('ارقام دستاوردهای SO (۵.۸ میلیون مستفید صحی و …)',
         'این ارقام از نسخه قبلی کتاب گرفته شده‌اند. قبل از چاپ باید با گزارش رسمی سازمان '
         'مقایسه شوند.'),
        ('مبالغ پروژه‌های دایکندی (۳۵,۰۰۰ / ۲۵,۰۰۰ / ۴۰,۰۰۰ دالر)',
         'نام مراکز (چچن، کورگا، شیلان کورگا) و مبالغ باید با اسناد مالی/پروژه‌ای SO تأیید شوند.'),
        ('فهرست ولسوالی‌های دایکندی',
         'در متن چهار ولسوالی (نیلی، اشترلی، شهرستان، کیتی) نام برده شده؛ تعداد ولسوالی‌ها در '
         'منابع متفاوت است (۸ تا ۹ — بعضی منابع پتو/کجران و بعضی گیزیب را متفاوت می‌شمارند). '
         'برای «فهرست کامل» باید از PPHD دایکندی تأیید گرفته شود.'),
        ('DHIS2 در MoPH',
         'کاربرد DHIS2 در ثبت معلومات HMIS افغانستان در این نسخه به شکل عمومی گفته شده است؛ '
         'نسخه/روند فعلی را با MoPH/PPHD تأیید کنید.'),
        ('نام بخش‌ها در وزارت صحت عامه امروز',
         'ساختار چهار معینیت از صفحه رسمی وزارت گرفته شده؛ نام‌های فعلی ممکن است تغییر کرده باشد.'),
        ('مشخصات نشر',
         'شماره ISBN، ناشر رسمی، قطع نهایی چاپ و الزامات چاپ‌خانه تعیین نشده است — خارج از '
         'حوزه این ویرایش، اما برای نشر نیاز است.'),
    ]
    rl = ['# گزارش آمادگی نشر — Publication Readiness Report', '',
          '**وضعیت:** READY FOR PUBLICATION WITH AUTHOR CONFIRMATIONS (آماده نشر با '
          'تأییدهای نویسنده) — هیچ مانع فنی باقی نمانده، اما موارد جدول زیر باید پیش از '
          'چاپ توسط نویسنده/سازمان تأیید شوند.', '',
          f'**خلاصه QA:** {summary}', '',
          '**خروجی‌های تولیدشده:**', '',
          '| فایل | توضیح |', '|---|---|',
          '| `output/…DOCX_نسخه_نهایی.docx` | نسخه قابل ویرایش Word با استایل‌های واقعی و فهرست خودکار |',
          '| `output/…چاپی_17x24.pdf` | PDF آماده چاپ (قطع ۱۷×۲۴ سانتی‌متر، حاشیه آینه‌ای) |',
          '| `output/…دیجیتال_A4.pdf` | PDF دیجیتال (A4، لینک‌های داخلی) |',
          '| `output/….epub` | EPUB3 با فونت دری تعبیه‌شده و راست‌به‌چپ |',
          '| `project/glossary/terminology-glossary.csv` | واژه‌نامه اصطلاحات (۷۴ مدخل) |',
          '| `project/logs/editorial-change-log.md` | لاگ تغییرات |',
          '| `project/logs/scientific-correction-log.md` | لاگ تصحیحات علمی |',
          '| `project/logs/qa-report.md` | گزارش QA با ۳۹ بررسی |',
          '', '## مواردی که تأیید انسان لازم دارد (Human review gate)', '',
          '| مورد | چه چیزی باید تأیید شود |', '|---|---|']
    for a, b in flags:
        rl.append(f'| {a} | {b} |')
    rl += ['', '## کارهای باقی‌مانده فنی', '',
           '1. **epubcheck**: در این محیط (بدون Java) قابل اجرا نبود؛ اعتبارسنجی ساختاری '
           'جایگزین انجام شد. قبل از توزیع، `epubcheck` روی فایل EPUB اجرا شود.',
           '2. **بازبینی چشمی چاپ**: PDF چاپی باید پیش از رفتن به چاپ‌خانه یک بار به‌صورت '
           'چشمی بررسی شود (شکستن جدول‌ها، صفحه‌های خالی، شروع فصل‌ها).',
           '3. **متن PDF و کاپی کردن**: متن PDF با گلیف‌های شکل‌یافته ذخیره شده است (برای '
           'نمایش درست دری). برای متن قابل کپی کامل، از DOCX یا EPUB استفاده شود.',
           '']
    (LOGS / 'publication-readiness.md').write_text('\n'.join(rl), encoding='utf-8')

    print('logs written:')
    for f in ('editorial-change-log.md', 'scientific-correction-log.md',
              'publication-readiness.md'):
        p = LOGS / f
        print(f'  {p.name}  {p.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
