# -*- coding: utf-8 -*-
"""
human_quality_editor.py
Performs targeted, senior-level editorial, terminological, and authority repairs
across both manuscripts (Book 1 and Book 2).
"""

import re

def polish_manuscript(text, is_book2=False):
    # 1. Authority fixes
    # Fix unilateral contract cancellation
    text = text.replace(
        "فسخ فوری قرارداد با رستورانت تامین‌کننده غذا، ابطال فکتور و درج تخلف در لیست سیاه تدارکات.",
        "توقف فوری توزیع غذا و ارسال راپور مستند به همراه فکتور به کمیته تدارکات دفتر مرکزی با پیشنهاد فسخ قرارداد طبق پالیسی تدارکات."
    )
    text = text.replace(
        "تعلیق فوری داکتر از وظیفه و ارجاع پرونده به آمریت حقوقی و HR در کابل جهت اخراج قطعی.",
        "منع فوری داکتر از ورود به اتاق عملیات جهت حفظ مصئونیت مریض، اخذ تست‌های لازم، تنظیم داکتر جراح بدیل، و ارجاع عاجل دوسیه مستند به آمریت منابع بشری و کمیته انضباطی دفتر مرکزی طبق پالیسی HR."
    )
    text = text.replace(
        "تذکر اینکه در صورت تکرار، قرارداد راننده فوراً فسخ خواهد شد.",
        "تذکر مکتوب اینکه در صورت تکرار غفلت، دوسیه جهت فسخ قرارداد طبق پالیسی HR و قانون کار به دفتر مرکزی ارجاع خواهد شد."
    )
    text = text.replace(
        "تدوین شیفت‌بندی مکتوب و الزامی برای تمام رانندگان کلینیک با جریمه‌های انضباطی مشخص.",
        "تدوین شیفت‌بندی مکتوب و الزامی برای تمام رانندگان کلینیک با اقدامات انضباطی مشخص طبق پالیسی منابع بشری سازمان."
    )
    text = text.replace(
        "توبیخ راننده به دلیل عدم راپور نقص فنی بخاری و استعلام از مسئول ترانسپورت ولایت.",
        "اخذ استعلام کتبی از راننده، ثبت در دوسیه و ارجاع راپور به مسئول ترانسپورت و آمریت اداری ولایت جهت پیگیری انضباطی طبق پالیسی سازمان."
    )
    text = text.replace(
        "استرداد مبالغ اخذشده به مردم و ارسال راپور مستند به دفتر مرکزی جهت فسخ قرارداد آمر متخلف.",
        "استرداد مبالغ اخذشده به مراجعین و ارسال راپور مستند به دفتر مرکزی با پیشنهاد فسخ قرارداد آمر متخلف به کمیته انضباطی سازمان."
    )
    text = text.replace(
        "تعلیق موقت واکسیناتور از امور تزریقات و ارجاع پرونده به آمریت HR جهت مجازات انضباطی.",
        "تغییر موقت وظیفه واکسیناتور از امور تزریقات (جهت حفظ مصئونیت مریضان) و ارجاع دوسیه به آمریت HR جهت اقدامات انضباطی طبق پالیسی سازمان."
    )
    text = text.replace(
        "عدم ارائه دلیل موجه: اخطار اول کتبی و کسر معاش روزهای غیرحاضر.",
        "عدم ارائه دلیل موجه: صدور استعلام کتبی، اخطار اول و پیشنهاد کسر معاش ایام غیرحاضری به آمریت منابع بشری دفتر مرکزی طبق پالیسی HR سازمان."
    )
    text = text.replace(
        "عدم ارائه عذر موجه: کسر معاش ایام غیبت و صدور اخطار کتبی درجه یک از طریق منابع بشری.",
        "عدم ارائه عذر موجه: صدور اخطار کتبی و پیشنهاد کسر معاش ایام غیبت به آمریت منابع بشری دفتر مرکزی طبق پالیسی HR سازمان."
    )
    text = text.replace(
        "Authority Boundary: توبیخ اداری در صلاحیت هماهنگ‌کننده است اما کسر معاش باید توسط HR کابل منظور شود.",
        "Authority Boundary: مدیر کلینیک صلاحیت کسر مستقیم معاش یا اخراج را ندارد؛ ثبت تخلف و صدور اخطار کتبی مطابق طرزالعمل انجام شده و کسر معاش یا فسخ قرارداد منوط به تأیید آمر مالی و HR دفتر مرکزی طبق پالیسی قابل تطبیق سازمان است."
    )

    # 2. Marketing claims removal
    text = text.replace("بالاترین نمره شایستگی را از داوران کسب کند.", "نمره شایستگی لازم را از داوران کسب کند.")
    text = text.replace("با بالاترین کیفیت ممکن و مناسب‌ترین قیمت", "با کیفیت مطلوب و معیاری و مناسب‌ترین قیمت")
    text = text.replace("کیفیت تضمین‌شده و بالاترین اثر بخشی", "کیفیت تضمین‌شده و اثربخشی اثبات‌شده")

    # 3. Afghan Dari Terminology replacements
    # زایشگاه -> اتاق ولادت / شعبه ولادی
    text = text.replace("کتاب‌های راجستر زایشگاه", "کتاب‌های راجستر اتاق ولادت")
    text = text.replace("کتاب راجستر زایشگاه", "کتاب راجستر اتاق ولادت")
    text = text.replace("تری عاجل زایشگاه", "تری عاجل اتاق ولادت")
    text = text.replace("زایشگاه و اتاق ولادت فعال", "اتاق ولادت و شعبه ولادی فعال")
    text = text.replace("مراکز صحی دارای زایشگاه", "مراکز صحی دارای اتاق ولادت")
    text = text.replace("بازدید از زایشگاه CHC", "بازدید از اتاق ولادت CHC")
    text = text.replace("بخش‌های عاجل و زایشگاه", "بخش‌های عاجل و اتاق ولادت")
    text = text.replace("بخش عاجل و زایشگاه", "بخش عاجل و اتاق ولادت")
    text = text.replace("تجهیز تمام زایشگاه‌ها", "تجهیز تمام شعبات ولادی")
    text = text.replace("عدم توقف زایشگاه", "عدم توقف خدمات ولادی")
    text = text.replace("مراجعه به زایشگاه", "مراجعه به اتاق ولادت کلینیک")

    # اورژانس -> عاجل
    text = text.replace("جراحی اورژانسی", "عملیات عاجل جراحی")
    text = text.replace("سزارین اورژانسی", "سزارین عاجل (Emergency Cesarean)")

    # بهداشت -> حفظ‌الصحه / صحت
    text = text.replace("پروتکل بهداشت دست (Hand Hygiene)", "رهنمود حفظ‌الصحه دست‌ها (Hand Hygiene)")
    text = text.replace("بهداشت دست (Hand Hygiene)", "حفظ‌الصحه دست‌ها (Hand Hygiene)")
    text = text.replace("بهداشت دست", "حفظ‌الصحه دست‌ها")
    text = text.replace("دفن بهداشتی، بدون بو و مصئون جفت", "دفن مصئون، بدون بو و صحی جفت")
    text = text.replace("دفن بهداشتی", "دفن مصئون و صحی")
    text = text.replace("امحای بهداشتی جفت", "امحای مصئون و صحی جفت")
    text = text.replace("کدام بسته بهداشتی است", "کدام بسته خدمات صحی است")
    text = text.replace("حریم بهداشتی کلینیک", "محیط صحی کلینیک")
    text = text.replace("بخش بهداشت شفاخانه", "بخش حفظ‌الصحه و نظافت شفاخانه")
    text = text.replace("بهبود بهداشت", "بهبود حفظ‌الصحه")
    text = text.replace("رعایت بهداشت فردی", "رعایت حفظ‌الصحه فردی")

    # پرونده -> دوسیه
    text = text.replace("پرونده عملکرد", "دوسیه عملکرد")
    text = text.replace("پرونده ولادت", "دوسیه ولادت")
    text = text.replace("پرونده بهداشتی", "دوسیه صحی")
    text = text.replace("پرونده کارمند", "دوسیه کارمند")
    text = text.replace("پرونده انضباطی", "دوسیه انضباطی")
    text = text.replace("ارسال پرونده به HR", "ارسال دوسیه به HR")
    text = text.replace("ارجاع پرونده به آمریت", "ارجاع دوسیه به آمریت")
    text = text.replace("پرونده را فوراً به کمیته", "دوسیه را فوراً به کمیته")
    text = text.replace("پرونده تقلب", "دوسیه تقلب")
    text = text.replace("پرونده بیماری", "دوسیه مریضی")
    text = text.replace("پرونده تمام ولادت‌ها", "دوسیه تمام ولادت‌ها")
    text = text.replace("پرونده را به تفتیش", "دوسیه را به تفتیش")
    text = text.replace("بستن پرونده", "بستن دوسیه")

    # دستورالعمل -> طرزالعمل / رهنمود
    text = text.replace("دستورالعمل گام‌به‌گام", "طرزالعمل گام‌به‌گام")
    text = text.replace("دستورالعمل‌ها با ادبیات", "رهنمودها با ادبیات")
    text = text.replace("دستورالعمل‌های مشخص", "طرزالعمل‌های مشخص")
    text = text.replace("دستورالعمل ملی", "رهنمود ملی")
    text = text.replace("دستورالعمل رسمی صیانت", "پالیسی رسمی صیانت")

    # انبار -> گدام / دیپو
    text = text.replace("دمای انبار", "دمای گدام")
    text = text.replace("فضای انبار", "فضای گدام")
    text = text.replace("وارد انبار می‌شود", "وارد گدام می‌شود")
    text = text.replace("انبار کردن ادویه", "ذخیره کردن ادویه در دیپو")
    text = text.replace("انباشت مازاد", "ذخیره مازاد")
    text = text.replace("نم کشیدن انبار", "نم کشیدن گدام")

    # دارو -> دوا / ادویه
    text = text.replace("طبقه‌بندی داروها", "طبقه‌بندی ادویه")
    text = text.replace("داروخانه فروش", "دواخانه فروش")
    text = text.replace("شرکت‌های دارویی", "کمپنی‌های ادویه")
    text = text.replace("تزریق داروی بی‌اثر", "تزریق دوای بی‌اثر")
    text = text.replace("زرق داروی انقباض رحم", "زرق دوای انقباض رحم")
    text = text.replace("هر دارویی که به معاینه‌خانه", "هر دوایی که به معاینه‌خانه")
    text = text.replace("ضایع شدن داروهای", "ضایع شدن ادویه")

    # کادر درمان -> پرسنل صحی
    text = text.replace("کادر درمان و مدیران صحی", "کادر صحی و مدیران مراکز صحی")
    text = text.replace("کادر درمان", "کادر صحی")

    # بیمار -> مریض
    text = text.replace("ایمنی بیمار", "مصئونیت مریض (Patient Safety)")
    text = text.replace("مصئونیت بیمار", "مصئونیت مریض")
    text = text.replace("حقوق بیمار", "حقوق مریض")
    text = text.replace("جریان حرکت بیمار", "جریان حرکت مراجعین و مریضان")
    text = text.replace("ارتباط حسنه با بیمار", "برخورد نیک و محترمانه با مریض")
    text = text.replace("رنج بیماران", "رنج مریضان")
    text = text.replace("شکایت بیماران", "شکایت مریضان")
    text = text.replace("بیماران شاکی", "مریضان شاکی")
    text = text.replace("به بیماران", "به مریضان")
    text = text.replace("از بیماران", "از مریضان")
    text = text.replace("با بیماران", "با مریضان")
    text = text.replace("برای بیماران", "برای مریضان")
    text = text.replace("وضعیت بیماران", "وضعیت مریضان")
    text = text.replace("جان بیمار", "جان مریض")
    text = text.replace("پرونده بیمار", "دوسیه مریض")
    text = text.replace("دیتای بیمار", "دیتای مریض")
    text = text.replace("اقامت بیمار", "اقامت مریض")
    text = text.replace("سلامت بیمار", "صحت مریض")
    text = text.replace("آسیب به بیمار", "آسیب به مریض")

    # درمان -> تداوی (in clinical contexts)
    text = text.replace("خدمات درمانی و وقایوی", "خدمات وقایوی و تداوی")
    text = text.replace("خدمات درمانی", "خدمات تداوی")
    text = text.replace("استندردهای درمانی", "استندردهای تداوی")
    text = text.replace("مداخله درمانی", "مداخله تداوی")
    text = text.replace("نیازهای درمانی", "نیازهای تداوی")
    text = text.replace("شاخص درمان توبرکلوز", "شاخص تداوی توبرکلوز (TB Cure Rate)")

    # 4. Book 1 specific fix for lines 103-105: un-nest formula from blockquote
    if not is_book2:
        old_block = """> ### 🔑 فرمول بنیادین و قطب‌نمای طلایی کتاب:
> $$\\mathbf{UNDERSTAND \\rightarrow PRIORITIZE \\rightarrow COORDINATE \\rightarrow VERIFY \\rightarrow ACT \\rightarrow DOCUMENT \\rightarrow REPORT \\rightarrow FOLLOW\\ UP}$$
> «بفهم $\\rightarrow$ اولویت\u200cبندی کن $\\rightarrow$ هماهنگ بساز $\\rightarrow$ تصدیق کن $\\rightarrow$ اقدام کن $\\rightarrow$ مستند بساز $\\rightarrow$ راپور بده $\\rightarrow$ پیگیری کن»"""
        
        new_block = """### 🔑 فرمول بنیادین و قطب‌نمای طلایی کتاب:
$$\\mathbf{UNDERSTAND \\rightarrow PRIORITIZE \\rightarrow COORDINATE \\rightarrow VERIFY \\rightarrow ACT \\rightarrow DOCUMENT \\rightarrow REPORT \\rightarrow FOLLOW\\ UP}$$

> «بفهم $\\rightarrow$ اولویت\u200cبندی کن $\\rightarrow$ هماهنگ بساز $\\rightarrow$ تصدیق کن $\\rightarrow$ اقدام کن $\\rightarrow$ مستند بساز $\\rightarrow$ راپور بده $\\rightarrow$ پیگیری کن»"""
        text = text.replace(old_block, new_block)

    return text

# Apply to Book 1
with open('manuscript/master.md', 'r', encoding='utf-8') as f:
    c1 = f.read()
new_c1 = polish_manuscript(c1, is_book2=False)
with open('manuscript/master.md', 'w', encoding='utf-8') as f:
    f.write(new_c1)
print(f"Book 1 updated. Chars: {len(c1)} -> {len(new_c1)}")

# Apply to Book 2
with open('manuscript/health_management_master.md', 'r', encoding='utf-8') as f:
    c2 = f.read()
new_c2 = polish_manuscript(c2, is_book2=True)
with open('manuscript/health_management_master.md', 'w', encoding='utf-8') as f:
    f.write(new_c2)
print(f"Book 2 updated. Chars: {len(c2)} -> {len(new_c2)}")
