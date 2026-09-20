#!/usr/bin/env python3
"""
Hand-made (curated) corrections on project/manuscript/parts/10_body.md.

Every entry is one editorial decision, applied by exact-match replacement and
asserted, so nothing fails silently. Options:
    python3 project/scripts/patch_curated.py            # apply
    python3 project/scripts/patch_curated.py --check     # verify only

Classifications follow references/editorial-workflow.md:
    Scientific correction | Clinical correction | Updated evidence |
    Terminological | Structural | Editorial
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / 'project/manuscript/parts/10_body.md'

# ---------------------------------------------------------------------------
# exact-match replacements: (id, classification, reason, old, new, expected_hits)
# ---------------------------------------------------------------------------
EDITS = [
    # --- production / typography clean-up -------------------------------
    ('C01', 'Formatting', 'the acronym DHIS2 must stay Latin; the numeral rule had converted it',
     'DHIS۲', 'DHIS2', 10),
    ('C02', 'Editorial', 'correct Dari spelling of the exclamation',
     'انشالله', 'انشاءالله', 1),
    ('C03', 'Editorial', 'register consistency (زنگ زدن -> تماس گرفتن)',
     'زنگ می‌زنند', 'تماس می‌گیرند', 1),

    # --- chapter 1: organisation description ----------------------------
    ('C04', 'Scientific correction',
     'founder aligned with the organisation published history (1989, Quetta hospital); '
     'non-political self-description restored; province list aligned with published sources. '
     'Original wording kept in the change log.',
     'Shuhada Organization (SO) در سال ۱۹۸۹ توسط داکتر سیما سمر و عبدالرؤف نوید تأسیس شد. '
     'این سازمان غیردولتی، غیرانتفاعی و مستقل است که هدف اصلی‌اش رفاه و پیشرفت شهروندان افغان '
     'با تمرکز بر توانمندسازی زنان و اطفال است. SO در بخش‌های صحت، آموزش و توانمندسازی '
     'اقتصادی زنان فعالیت دارد و در ولایات مختلف از جمله دایکندی، بامیان، غزنی و کابل کار می‌کند.',
     'Shuhada Organization (SO) در سال ۱۹۸۹ توسط داکتر سیما سمر بنیان گذاشته شد؛ اولین مرکز آن '
     'شفاخانه‌ای برای زنان و اطفال افغان پناهنده در کویته، پاکستان بود. این سازمان غیردولتی، '
     'غیرانتفاعی، غیرسیاسی و مستقل است و هدف اصلی‌اش رفاه و پیشرفت شهروندان افغان با تمرکز بر '
     'توانمندسازی زنان و اطفال است. SO در بخش‌های صحت، آموزش، حقوق بشر و توانمندسازی اقتصادی '
     'زنان فعالیت دارد و در ولایات مرکزی افغانستان — از جمله دایکندی، بامیان و غزنی — کار می‌کند.',
     1),

    # --- chapter 3: health-system structure and standards ----------------
    ('C05', 'Scientific correction',
     'unverifiable staff figure removed; replaced with the published deputy-ministry structure '
     'of MoPH (moph.gov.af general directorates list).',
     '- High Council: بالاترین نهاد تصمیم‌گیری — وزیر صحت + ۳ معین\n\n'
     '- Executive Board: اجرائیه — وزیر، معین‌ها، مشاوران، رؤسای عمومی\n\n'
     '- MoPH حدود ۱۴,۰۰۰ کارمند دارد — در کابل و ولایات',
     '- در رأس وزارت: وزیر صحت عامه؛ در کنار او چهار معینیت — خدمات صحی، پالیسی و انکشاف، '
     'طب و غذا، و مالی و اداری.\n\n'
     '- زیر هر معینیت، ریاست‌های عمومی و تصدی‌های تخصصی کار می‌کنند — از جمله ریاست هماهنگی '
     'صحت ولایات (Provincial Health Coordination)، ریاست صحت اولیه (PHC)، ریاست صحت مادر و '
     'طفل، و ریاست پلان و هماهنگی.\n\n'
     '- شورای عالی صحت عامه و بورد اجرائیه وزارت، نهادهای مشورتی و هماهنگی برای '
     'تصمیم‌گیری‌های کلان صحی اند.',
     1),
    ('C06', 'Scientific correction',
     'BPHS catchment standards corrected: the original "one BHC per 13,000 and one hospital per '
     '210,000" does not match the national BPHS standard. Source: MoPH, Basic Package of Health '
     'Services 2010 (health post 1,000-1,500; BHC 15,000-30,000; CHC 30,000-60,000; district '
     'hospital 100,000-300,000; provincial hospital 200,000-500,000).',
     '- یک BHC برای هر ۱۳,۰۰۰ نفر • یک شفاخانه برای هر ۲۱۰,۰۰۰ نفر • در سال ۲۰۱۸، ۳,۱۳۵ مرکز '
     'صحی فعال بود و ۸۷٪ مردم در فاصله ۲ ساعته به خدمات دسترسی داشتند.',
     '- Health Post برای هر ۱,۰۰۰–۱,۵۰۰ نفر (۱۰۰–۱۵۰ خانواده) • BHC برای هر ۱۵,۰۰۰–۳۰,۰۰۰ نفر '
     '(در ساحات بسیار دور، کمتر از ۱۵,۰۰۰ نفر) • CHC برای هر ۳۰,۰۰۰–۶۰,۰۰۰ نفر • شفاخانه '
     'ولسوالی برای هر ۱۰۰,۰۰۰–۳۰۰,۰۰۰ نفر • شفاخانه ولایتی برای هر ۲۰۰,۰۰۰–۵۰۰,۰۰۰ نفر '
     '(معیارهای BPHS، وزارت صحت عامه).\n\n'
     '- در سال ۲۰۱۸ در افغانستان ۳,۱۳۵ مرکز صحی فعال ثبت شده بود و نزدیک به ۸۷٪ مردم در '
     'فاصله دو ساعته به خدمات صحی دسترسی داشتند (منبع: WHO EMRO — Health Systems, Afghanistan).',
     1),
    ('C07', 'Scientific correction',
     'catchment figures corrected in the chapter summary as well (consistency with C06).',
     '- BHC برای هر ۱۳,۰۰۰ نفر — شفاخانه برای هر ۲۱۰,۰۰۰ نفر.',
     '- BHC برای هر ۱۵,۰۰۰–۳۰,۰۰۰ نفر — شفاخانه ولسوالی برای هر ۱۰۰,۰۰۰–۳۰۰,۰۰۰ نفر.', 1),
    ('C08', 'Scientific correction',
     'exam answer key updated to the BPHS standard (consistency with C06).',
     '**جواب: برای هر ۱۳,۰۰۰ نفر.**',
     '**جواب: برای هر ۱۵,۰۰۰–۳۰,۰۰۰ نفر (در ساحات بسیار دور، کمتر از ۱۵,۰۰۰ نفر).**', 1),
    ('C09', 'Scientific correction',
     'HMIS submission deadline stated unambiguously. Source: MoPH HMIS Procedures Manual '
     '("aggregated report is sent on to the PPHO/NGO before the 7th day of each month").',
     'فرستادن به PPHD/NGO — قبل از ۷ ماه',
     'فرستادن به PPHD/سازمان — تا هفتم ماه بعد (۷ روز پس از پایان ماه)', 1),
    ('C10', 'Scientific correction', 'same deadline clarified inside the table (consistency with C09).',
     '| راپور به PPHD/NGO فرستاده می‌شود | قبل از ۷ ماه |',
     '| راپور به PPHD/سازمان فرستاده می‌شود | تا هفتم ماه بعد (۷ روز پس از پایان ماه) |', 1),
    ('C11', 'Scientific correction',
     'quarterly-report deadline clarified against the HMIS manual (quarterly reports reach the '
     'central level before the end of the first month of the new quarter).',
     'فرستادن به مرکز — پایان ماه اول ربع جدید',
     'فرستادن راپور ربعوار به مرکز — تا پایان ماه اول ربع جدید', 1),

    # --- chapter 6: PSEA wording aligned with IASC ----------------------
    ('C12', 'Clinical correction',
     'PSEA principles re-stated against the IASC Six Core Principles. The original version '
     'described principle 4 as an absolute prohibition and attributed principle 6 only to senior '
     'management; the IASC text says "strongly discouraged ... inherently unequal power dynamics" '
     'and places the obligation on humanitarian workers, with particular responsibilities for '
     'managers at all levels. Original wording preserved in the change log.',
     '- عدم تحمل مطلق (Zero Tolerance) در برابر رفتار نادرست جنسی — منجر به اخراج می‌شود.\n\n'
     '- ممنوعیت کامل هر گونه فعالیت جنسی و روابط با افراد زیر ۱۸ سال.\n\n'
     '- ممنوعیت تبادله پول، جنس/مال یا خدمات در بدل منافع یا روابط جنسی.\n\n'
     '- ممنوعیت مطلق روابط با افراد آسیب‌دیده، گروه‌های آسیب‌پذیر و شرکت‌کنندگان در '
     'برنامه‌های بشردوستانه.\n\n'
     '- گزارش الزامی هر نوع ادعا/شکایت، سوء ظن، یا خطرهای استثمار و سوء استفاده جنسی.\n\n'
     '- مسئولیت مدیریت ارشد برای ایجاد و حفظ سیستم‌های جلوگیری و پاسخگویی.',
     '**اصول شش‌گانه IASC:**\n\n'
     '۱. استثمار و سوء استفاده جنسی از سوی کارمندان بشردوستانه، تخلف سنگین کاری است و '
     'موجب اخراج از وظیفه می‌شود.\n\n'
     '۲. فعالیت جنسی با افراد زیر ۱۸ سال ممنوع است — بدون توجه به سن قانونی یا رضایت محلی. '
     'ادعای نادانی در مورد سن، عذر پذیرفته نیست.\n\n'
     '۳. تبادله پول، مال، کار یا خدمات در بدل رابطه جنسی — از جمله استفاده از کمک‌هایی که '
     'حق مستفیدان است — ممنوع است.\n\n'
     '۴. روابط جنسی میان کارمندان بشردوستانه و مستفیدان برنامه‌ها به شدت منع شده است، زیرا '
     'بر عدم توازن قدرت بنا شده و اعتبار کمک بشردوستانه را آسیب می‌زند. در عمل، اکثر سازمان‌ها '
     'این روابط را مطلقاً ممنوع کرده‌اند و استفاده نادرست از مقام و جایگاه برای آن، تخلف است.\n\n'
     '۵. اگر کارمند بشردوستانه در مورد سوء استفاده یا استثمار جنسی از سوی همکار خود — در همین '
     'سازمان یا سازمان دیگر — شک یا نگرانی داشته باشد، مکلف است آن را از راه‌های رسمی گزارش بدهد.\n\n'
     '۶. هر کارمند مکلف است محیطی را ایجاد و حفظ کند که از استثمار و سوء استفاده جنسی جلوگیری '
     'شود؛ مدیران در همه سطوح مسئولیت ویژه‌ای برای ساختن و حفظ چنین محیطی دارند.\n\n'
     '**در سازمان خودت:** کانال گزارش‌دهی PSEA، نام مسئول PSEA و خط تماس محرمانه را از قبل '
     'بشناس و به تیم خود هم معرفی کن — قبل از اینکه حادثه‌ای پیش بیاید.',
     1),

    # --- chapter 9: SO history -------------------------------------------
    ('C13', 'Scientific correction',
     'founder attribution aligned with SO published history (consistency with C04).',
     'Shuhada Organization (SO) در سال ۱۹۸۹ توسط داکتر سیما سمر و عبدالرؤف نوید در کویته، '
     'پاکستان تأسیس شد.',
     'Shuhada Organization (SO) در سال ۱۹۸۹ توسط داکتر سیما سمر در کویته، پاکستان بنیان '
     'گذاشته شد؛ اولین مرکز آن شفاخانه‌ای برای زنان و اطفال افغان پناهنده بود.', 1),
    ('C14', 'Scientific correction', 'consistency with C13 (chapter summary).',
     '- SO در ۱۹۸۹ توسط داکتر سیما سمر و عبدالرؤف نوید تأسیس شد.',
     '- SO در ۱۹۸۹ توسط داکتر سیما سمر بنیان گذاشته شد.', 1),
    ('C15', 'Scientific correction', 'consistency with C13 (answer-key table).',
     '| SO کِی تأسیس شد؟ | ۱۹۸۹ — توسط داکتر سیما سمر و عبدالرؤف نوید | ۱۹۸۹ by Dr. Sima Samar and Abdul Rauf Naveed. |',
     '| SO کِی تأسیس شد؟ | ۱۹۸۹ — توسط داکتر سیما سمر | ۱۹۸۹, founded by Dr. Sima Samar. |', 1),
    ('C16', 'Scientific correction',
     'province list aligned with published sources (Bamyan, Ghazni, Ghor, Wardak, Daykundi, '
     'and the Hazarajat region) instead of an unsourced list.',
     'SO در ولایات کابل، غزنی، بامیان، دایکندی، بغلان و چند ولایت دیگر فعالیت دارد.',
     'SO در ولایات مرکزی و همجوار افغانستان — از جمله دایکندی، بامیان، غزنی، غور، وردک و '
     'کابل — فعالیت دارد.', 1),
    ('C17', 'Scientific correction', 'consistency with C16 (answer-key table).',
     '| SO در کدام ولایات فعال است؟ | کابل، غزنی، بامیان، دایکندی | Kabul, Ghazni, Bamyan, Daikundi. |',
     '| SO در کدام ولایات فعال است؟ | دایکندی، بامیان، غزنی، غور، وردک و کابل | Daykundi, Bamyan, Ghazni, Ghor, Wardak and Kabul. |', 1),
]


# ---------------------------------------------------------------------------
# insertions: (id, classification, reason, anchor, payload, where)
#   where = 'before' | 'after'
# ---------------------------------------------------------------------------
OBJECTIVES = {
    'فصل اول': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. وظایف واقعی یک Provincial Coordinator را فهرست می‌کنی و می‌دانی کجا Coordinator است و کجا نه.
۲. می‌توانی یک پلان کاری واضح، قابل اندازه‌گیری و زمان‌بندی‌شده بنویسی.
۳. تفاوت Monitoring و Evaluation، Risk و Issue، و اولویت‌بندی کارها را توضیح می‌دهی.
۴. چرخه هفت‌مرحله‌ای کار Coordinator را در یک وضعیت واقعی به کار می‌بری.

:::""",
    'فصل دوم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. یک راپور ماهوار واقعی را با ساختار کامل (مقدمه، فعالیت‌ها، نتایج، مشکلات، درس‌ها، پلان آینده) می‌نویسی.
۲. خلاصه اجرائی نیم‌صفحه‌ای می‌نویسی که نتیجه را پیش از توضیح می‌گوید.
۳. برای هر مشکل یک پلان اقدام (مشکل، اقدام، مسئول، زمان، شاخص) می‌سازی.
۴. راپور حادثه‌ای را همان روز آماده می‌کنی.

:::""",
    'فصل سوم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. سه سطح نظام صحی افغانستان و وظیفه هر سطح را توضیح می‌دهی.
۲. تفاوت BPHS و EPHS و معیار جمعیتی هر نوع مرکز صحی را می‌دانی.
۳. زنجیره معلومات صحی (Register ← HMIS ← DHIS2 ← PPHD ← MoPH) را می‌شناسی.
۴. می‌دانی امروز خدمات اساسی از چه راه تأمین می‌شود و نقش UNICEF، WHO، MoPH و PPHD چیست.

:::""",
    'فصل چهارم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. چرخه تدارکات (نیاز ← درخواست ← تأیید ← خریداری ← تحویل ← ثبت) را توضیح می‌دهی.
۲. AMC و Reorder Point را محاسبه می‌کنی و برای موجودی تصمیم می‌گیری.
۳. Stock-out را فوراً مدیریت می‌کنی و علت ریشه‌ای آن را پیدا می‌کنی.
۴. پلان زمستانی‌سازی و حفظ زنجیره سرد را برای مراکز دورافتاده می‌نویسی.

:::""",
    'فصل پنجم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. بودجه، پلان‌شده و واقعی را با هم مقایسه می‌کنی و Variance را محاسبه می‌کنی.
۲. Advance می‌گیری و آن را با اسناد درست تصفیه می‌کنی.
۳. اسناد حمایتی هر مصرف را می‌شناسی و می‌دانی بدون سند چه می‌شود.
۴. خود را برای Audit داخلی و خارجی آماده می‌کنی.

:::""",
    'فصل ششم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. روند استخدام را مطابق ToR و پالیسی سازمان اجرا می‌کنی.
۲. حاضری، رخصتی و ارزیابی عملکرد را مدیریت می‌کنی.
۳. روند اجرایات را عادلانه و مستند پیش می‌بری.
۴. اصول PSEA را می‌دانی و می‌دانی در صورت شک یا شکایت، چطور و به کی گزارش بدهی.

:::""",
    'فصل هفتم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. Stakeholderهای ولایتی را فهرست می‌کنی و نقش هرکدام را می‌دانی.
۲. با PPHD، MoPH، دفتر مرکزی و جامعه — هر کدام با زبان و روش خودش — هماهنگ می‌کنی.
۳. تعارض را می‌شناسی و آن را با شنیدن، بررسی و پیگیری حل می‌کنی.
۴. می‌دانی چه وقت و چطور مشکل را Escalate کنی.

:::""",
    'فصل هشتم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. سی سناریوی واقعی کار Coordinator را می‌شناسی و برای هرکدام پلان اقدام داری.
۲. در هر سناریو، هفت کلمه طلایی را به کار می‌بری: بفهم ← بررسی کن ← اولویت بده ← اقدام کن ← مستند کن ← راپور بده ← پیگیری کن.
۳. جواب دری و انگلیسی هر سناریو را می‌توانی در امتحان و مصاحبه بازگو کنی.
۴. می‌دانی در بحران اول کدام کار را انجام بدهی.

:::""",
    'فصل نهم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. تاریخچه، مأموریت، ارزش‌ها و ساختار Shuhada Organization را توضیح می‌دهی.
۲. فعالیت‌های صحی SO در دایکندی را می‌شناسی.
۳. مسئولیت‌های این بست را در ساختار SO جای می‌دهی.
۴. برای پرسش‌های مصاحبه در باره SO، جواب آماده داری.

:::""",
    'فصل دهم': """::: objectives اهداف این فصل

پس از خواندن این فصل:
۱. سه آزمون آزمایشی کامل را با وقت‌گیری حل می‌کنی.
۲. جواب‌های نمونه دری و انگلیسی را با جواب‌های خودت مقایسه می‌کنی.
۳. در مصاحبه، خودت را معرفی می‌کنی و برای سؤال‌های سناریویی و PSEA آماده‌ای.
۴. نقاط ضعف خودت را می‌شناسی و همان بخش کتاب را دوباره می‌خوانی.

:::""",
}

NEW_SECTIONS = [
    ('S01', 'Updated evidence',
     'new section: current (1405) service-delivery and funding context, which a coordinator '
     'working today needs and which the manuscript did not cover. Sources: UNICEF HER/NFA '
     'evaluation, WHO EMRO emergency situation report, UK Home Office CPIN Afghanistan '
     '(Oct 2025), Tolo News reporting (July 2025).',
     '### جواب‌های طلایی فصل سوم',
     """## ۳.۸ نظام صحی افغانستان امروز (۱۴۰۵) — چیزهایی که در کار روزمره می‌بینی

::: concept

ساختار BPHS/EPHS همان است که در بخش ۳.۲ خواندی، اما روش تأمین خدمات و پول آن بعد از ۲۰۲۱ تغییر کرده است. Coordinator باید این تفاوت را بداند تا بفهمد راپورش به کی می‌رسد و تصمیم از کجا می‌آید.

:::

**چطور خدمات اساسی تأمین می‌شود؟**

- وزارت صحت عامه (MoPH) پالیسی، معیار و نظارت را دارد؛ خدمات را سازمان‌های غیردولتی (Service Providers) در هر ولایت تطبیق می‌کنند.
- بعد از ۲۰۲۱، مدیریت قرارداد‌های BPHS/EPHS به سازمان ملل منتقل شد: UNICEF مسئول خدمات صحت اولیه و WHO مسئول بخش عمده خدمات شفاخانه‌ای است؛ پول آن از طریق صندوق‌های مشترک (مثل ARTF/بانک جهانی و ADB) تأمین می‌شود.
- در دوره قبلی همین خدمات زیر پروژه «صحتمندی» (Sehatmandi) و قراردادهای مستقیم MoPH اجرا می‌شد؛ پس برنامه‌های فعلی ادامه همان مدل contracting-out است.
- PPHD در ولایت، نقش هماهنگی، نظارت و تأیید را دارد؛ سازمان تو (Shuhada Organization) یکی از Service Providerها است.

**چه چیزی در چند سال اخیر تغییر کرده؟**

- تعداد مراکز صحی فعال کاهش یافته است. در اوج (اواخر دهه ۲۰۱۰) بیش از ۳,۰۰۰ مرکز فعال بود؛ در سال‌های بعد این تعداد به صورت محسوس کم شد و در ۲۰۲۵ نیز با قطع بخشی از کمک‌ها، صدها مرکز دیگر به تعلیق رفت.
- تأمین دوا، حقوق کارمندان و بعضی برنامه‌های صحی آسیب دیده است؛ این یعنی Stock-out و ترک وظیفه کارمندان در ولایات دور، ریسک‌های روزمره است.
- کمک‌ها برای برنامه‌های صحی عامه تا پایان ۲۰۲۶ تمدید شده؛ اما شرایط مالی بی‌ثبات است.

**این برای Coordinator چه معنی دارد؟**

۱. راپور و نظارت تو، برای ادامه پول و ادامه خدمات مهم است — گزارش دقیق = دفاع از خدمات برای مردم.
۲. هر Stock-out یا ترک وظیفه را مستند کن؛ این معلومات به PPHD و UNICEF/WHO کمک می‌کند تا برای ولایت تو منابع بگیرند.
۳. انتظار تغییر داشته باش: شرکای تأمین‌کننده، پروژه‌ها و شاید سازمان تطبیق‌کننده در ولایت عوض شوند. رابطه کاری با PPHD را نگه دار و اسناد را منظم نگه دار.
۴. برای معلومات دقیق و به‌روز، راپورترین و بلندترین منبع را نخوان — با PPHD ولایت خودت و دفتر مرکزی تماس بگیر.

**چه چیزی را بازبینی کن (تابستان ۱۴۰۵):** نام پروژه فعلی، شریک مالی، و کانال گزارش‌دهی ولایت خودت — چون ممکن است تغییر کرده باشد.

""",),
]


def apply():
    text = BODY.read_text(encoding='utf-8')
    applied = []
    problems = []

    for cid, cls, reason, old, new, expect in EDITS:
        n = text.count(old)
        if n != expect:
            problems.append(f'{cid}: expected {expect} match(es), found {n}')
            continue
        text = text.replace(old, new)
        applied.append((cid, cls, reason, n))

    # objectives at the head of every chapter
    added = 0
    for key, block in OBJECTIVES.items():
        anchor = None
        for line in text.split('\n'):
            if line.startswith('# ') and key in line:
                anchor = line
                break
        if not anchor:
            problems.append(f'OBJECTIVES {key}: chapter heading not found')
            continue
        if anchor + '\n\n' + block in text:
            applied.append((f'OBJ-{key}', 'Structural', 'chapter learning objectives', 1))
            continue
        text = text.replace(anchor, anchor + '\n\n' + block + '\n', 1)
        added += 1
        applied.append((f'OBJ-{key}', 'Structural', 'chapter learning objectives added', 1))

    for cid, cls, reason, anchor, payload in NEW_SECTIONS:
        idx = text.find(anchor)
        if idx < 0:
            problems.append(f'{cid}: anchor not found: {anchor[:40]}')
            continue
        line_start = text.rfind('\n', 0, idx) + 1
        text = text[:line_start] + payload + '\n' + text[line_start:]
        applied.append((cid, cls, reason, 1))

    print(f'objective boxes inserted: {added}/{len(OBJECTIVES)}')

    if '--check' in sys.argv:
        print('CHECK MODE: no file written')
    else:
        BODY.write_text(text, encoding='utf-8')

    print(f'applied {len(applied)} curated edits')
    for a in applied:
        print('  ', a[0], '|', a[1], '| x', a[3])
    if problems:
        print('PROBLEMS:')
        for p in problems:
            print('  !', p)
        sys.exit(1)


if __name__ == '__main__':
    apply()
