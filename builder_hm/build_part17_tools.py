# -*- coding: utf-8 -*-
"""
Builder for Part XVII: Practical Toolkits, Checklists & Afghan Health Acronym Directory
Includes 9 operational tools and complete field templates.
"""

def get_part17_tools_text():
    return r"""
# PART XVII — جعبه‌ابزار کاربردی، چک‌لیست‌ها و ضمایم مسلکی (Practical Toolkits & Appendices)

---

## جعبه‌ابزار ۱: چک‌لیست جلسه هماهنگی صبحگاهی (Daily Morning Huddle Checklist)

این چک‌لیست هر روز رأس ساعت ۰۸:۰۰ صبح توسط سرپرست مرکز صحی (Clinic In-Charge) بازبینی و امضا می‌شود:

| ردیف | مؤلفه مورد بررسی | وضعیت (تایید / نقص) | اقدام اصلاحی فوری در صورت نقص |
| :---: | :--- | :---: | :--- |
| **۱** | درجه حرارت یخچال واکسین (بین +2°C تا +8°C) | [  ] بلی  [  ] نخیر | بررسی جریان برق سولر و آیس‌پک‌ها |
| **۲** | موجودیت ادویه نجات‌بخش در تری عاجل زایشگاه | [  ] بلی  [  ] نخیر | اکمال فوری اکسی‌توسین و سرم رینگر |
| **۳** | حضور کامل پرسونل شیفت روز و قابله آن‌کال | [  ] بلی  [  ] نخیر | ثبت غیبت و فعال‌سازی کادر چرخشی |
| **۴** | فشار کپسول‌های اکسیجن در اتاق عاجل | [  ] بلی  [  ] نخیر | تعویض فوری سیلندر خالی با پر |
| **۵** | برقراری آب لوله‌کشی و صابون مایع در دستشویی‌ها | [  ] بلی  [  ] نخیر | پر کردن تانکر ذخیره آب و توزیع صابون |
| **۶** | موجودیت Safety Box در اتاق تزریقات و واکسین | [  ] بلی  [  ] نخیر | قرار دادن جعبه نو و بستن جعبه‌های پر |
| **۷** | بررسی باک تیل و آمادگی تخنیکی امبولانس | [  ] بلی  [  ] نخیر | تیل‌گیری فوری و رفع نقص ترمز موتر |

---

## جعبه‌ابزار ۲: فورم تفتیش کیفیت دیتای صحی (Monthly DQA Sheet)

این فورم در پایان هر ماه جهت ممیزی تطابق کتاب‌های راجستر با فورم‌های ماهوار MIAR تکمیل می‌گردد:

| شاخص کلیدی کلینیکی | تعداد در راجستر فزیکی (Recount) | تعداد در راپور ماهوار (Reported) | ضریب اعتبارسنجی (VF) | وضعیت تطابق (تایید / مغایرت) |
| :--- | :---: | :---: | :---: | :---: |
| **ویزیت‌های سراپا (Total OPD)** |  |  | $VF = \text{Recount} / \text{Reported}$ |  |
| **مراقبت اول بارداری (ANC-1)** |  |  |  |  |
| **مراقبت چهارم بارداری (ANC-4)** |  |  |  |  |
| **ولادت‌های داخل مرکز (IDR)** |  |  |  |  |
| **واکسین پنتاولنت دوز ۳ (Penta-3)** |  |  |  |  |
| **واکسین سرخکان دوز ۱ (Measles-1)** |  |  |  |  |
| **بهبود سوءتغذیه حاد (SAM Cure)** |  |  |  |  |

* **قاعده ارزیابی تفتیش:**
  * ضریب بین ۰.۹۵ تا ۱.۰۵ (مغایرت کمتر از ۵٪): **کیفیت عالی (تایید بدون قید و شرط)**.
  * ضریب بین ۰.۹۰ تا ۰.۹۴: **خطای جزیی (نیازمند بازآموزی کاتب)**.
  * ضریب کمتر از ۰.۹۰ یا بیشتر از ۱.۱۰: **مغایرت شدید (رد راپور، استعلام کتبی و تفتیش مجدد)**.

---

## جعبه‌ابزار ۳: ماتریس ۱۰۰ امتیازی نظارت حمایتی تسهیلات (100-Point Supervisory Matrix)

| حوزه ارزیابی | شاخص‌های کلیدی | حداکثر نمره | نمره کسب‌شده |
| :--- | :--- | :---: | :---: |
| **۱. منابع بشری و اداری** | حاضری منظم، ToR مکتوب، تفکیک وظایف، جو تیمی محترمانه | ۱۵ نمره |  |
| **۲. خدمات عاجل و تریاژ** | تریاژ فعال، تری عاجل کامل، امبولانس آماده، پروتکول احیا | ۱۵ نمره |  |
| **۳. صحت مادر و نوزاد** | تکمیل پاروتوگراف، خدمات ۲۴ ساعته BEmONC، مراقبت محترمانه | ۲۰ نمره |  |
| **۴. معافیت کتلوی و سردخانه** | ثبات دمای +2 تا +8، لاگ‌بوک منظم، VVM سالم، سیشن سیار | ۱۵ نمره |  |
| **۵. مدیریت ادویه و دیپو** | استاک‌کارت روزآمد، چیدمان پالت FEFO، عدم وجود داروی منقضی | ۱۵ نمره |  |
| **۶. وقایه از انتان (IPC)** | بهداشت دست، محلول کلورین ۰.۵٪، تفکیک زباله، چاهک پلاسنتا | ۱۰ نمره |  |
| **۷. ارقام و HMIS** | تطابق راجستر با راپور ماهوار (ACCT)، نمایش نمودارهای روند | ۱۰ نمره |  |
| **مجموع کل نمرات** | **حداقل نمره قبولی استاندارد: ۸۰ امتیاز** | **۱۰۰ نمره** |  |

---

## جعبه‌ابزار ۴: فلوچارت پاسخ اضطراری به طغیان وبایی (AWD/Cholera Outbreak Flowchart)

```
[ ورود موارد مشکوک اسهال حاد آبکی شدید ]
                    ↓
[ راپوردهی فوری ظرف ۱۲ ساعت به NDSR ریاست صحت عامه ]
                    ↓
[ برپایی خیمه تریاژ و مرکز تداوی موقت اسهالات (CTU) در بیرون کلینیک ]
                    ↓
        +-----------------------------------------------+
        |                                               |
[ پلان A (کم‌آبی خفیف) ]          [ پلان B (کم‌آبی متوسط) ]         [ پلان C (کم‌آبی شدید / شوک) ]
  - محلول ORS در خانه             - خوراندن ORS در کلینیک         - سرم رینگرلاکتات فوری وریدی
  - تابلیت زنک به مدت ۱۴ روز       - ارزیابی مجدد بعد از ۴ ساعت      - ۱۰۰ میلی‌لیتر/کیلوگرم ظرف ۳ تا ۶ ساعت
        |                                               |
        +-----------------------------------------------+
                    ↓
[ اعزام تیم صحت محیطی جهت کلوریناسیون عاجل منابع آب قریه و توزیع صابون ]
```

---

## جعبه‌ابزار ۵: فرهنگ جامع اختصارات و اصطلاحات صحت عامه افغانستان (100+ Health Acronyms)

این دایرکتوری مرجع استاندارد تمام واژگان اختصاری به کار رفته در آزمون‌های استخدامی و راپورهای تخنیکی است:

* **ACT:** Artemisinin-based Combination Therapy (تداوی ترکیبی ملاریا بر پایه آرتمیزینین)
* **AD Syringe:** Auto-Disable Syringe (سرنگ خودتخریب‌گر یک‌بارمصرف)
* **AEFI:** Adverse Events Following Immunization (رویدادهای ناگوار پس از واکسیناسیون)
* **AFP:** Acute Flaccid Paralysis (فلج حاد شل / مشکوک به پولیو)
* **ALOS:** Average Length of Stay (میانگین طول اقامت بیمار در بستر)
* **AMC:** Average Monthly Consumption (میانگین مصرف ماهوار ادویه)
* **AMTSL:** Active Management of the Third Stage of Labor (مدیریت فعال مرحله سوم ولادت)
* **ANC:** Antenatal Care (مراقبت‌های دوران بارداری قبل از ولادت)
* **BCG:** Bacillus Calmette-Guérin (واکسین توبرکلوز بدو تولد)
* **BEmONC:** Basic Emergency Obstetric and Newborn Care (مراقبت‌های عاجل ولادی و نوزادی پایه)
* **BHC:** Basic Health Center (مرکز صحی اساسی)
* **bOPV:** Bivalent Oral Polio Vaccine (قطره خوراکی دوظرفیتی پولیو)
* **BOR:** Bed Occupancy Rate (درصد اشغال تخت‌های بستر)
* **BPHS:** Basic Package of Health Services (بسته اساسی خدمات صحی)
* **CBA:** Comparative Bid Analysis (جدول مقایسه پیشنهادات تدارکاتی)
* **CBHC:** Community-Based Health Care (مراقبت‌های صحی مبتنی بر جامعه)
* **CEmONC:** Comprehensive Emergency Obstetric and Newborn Care (مراقبت‌های عاجل ولادی جامع)
* **CFR:** Case Fatality Rate (نرخ کشندگی بیماری)
* **CHC:** Comprehensive Health Center (مرکز صحی جامع)
* **CHS:** Community Health Supervisor (سوپروایزر صحی جامعه)
* **CHW:** Community Health Worker (کارمند صحی جامعه)
* **CPR:** Cardiopulmonary Resuscitation (احیای قلبی-ریوی)
* **CTU:** Cholera Treatment Unit (واحد موقت تداوی کولرا)
* **CYP:** Couple-Years of Protection (سال-زوج تحت پوشش تنظیم خانواده)
* **DEWS:** Disease Early Warning System (سیستم هشدار زودهنگام بیماری‌ها)
* **DH:** District Hospital (شفاخانه ولسوالی)
* **DHIS2:** District Health Information Software 2 (نرم‌افزار ملی معلومات صحی)
* **DIP:** Detailed Implementation Plan (پلان تفصیلی تطبیق پروژه)
* **DOTS:** Directly Observed Treatment, Short-course (تداوی تحت نظارت مستقیم توبرکلوز)
* **DQA:** Data Quality Audit (تفتیش و ممیزی کیفیت دیتا)
* **EBF:** Exclusive Breastfeeding (تغذیه انحصاری با شیر مادر تا ۶ ماهگی)
* **EML:** Essential Medicines List (لست ادویه اساسی)
* **EOC:** Emergency Operations Center (اتاق عملیات بحران)
* **EPHS:** Essential Package of Hospital Services (بسته خدمات اساسی شفاخانه‌ای)
* **EPI:** Expanded Programme on Immunization (برنامه توسعه‌یافته معافیت کتلوی)
* **FEFO:** First Expired, First Out (اولین داروی منقضی‌شونده، اولین داروی خروجی)
* **FIFO:** First In, First Out (اولین داروی وارده، اولین داروی خروجی)
* **GMP:** Good Manufacturing Practice (اصول استاندارد تولید ادویه)
* **GRN:** Goods Received Note (سند تصدیق تسلیمی اجناس به گدام)
* **GSP:** Good Storage Practice (اصول استاندارد گدام‌داری ادویه)
* **HER:** Health Emergency Response Project (پروژه پاسخ اضطراری صحت)
* **HIV:** Human Immunodeficiency Virus (ویروس نقص ایمنی انسان)
* **HMIS:** Health Management Information System (سیستم معلومات مدیریت صحی)
* **IDR:** Institutional Delivery Rate (نرخ ولادت در داخل تسهیلات صحی)
* **ILR:** Ice-Lined Refrigerator (یخچال واکسین دارای جداره یخ)
* **IMAM:** Integrated Management of Acute Malnutrition (مدیریت ادغام‌یافته سوءتغذیه حاد)
* **IMNCI:** Integrated Management of Newborn and Childhood Illness (مدیریت ادغام‌یافته امراض نوزاد و طفل)
* **IPC:** Infection Prevention and Control (وقایه و کنترول انتان)
* **IPD:** Inpatient Department (بخش مریضان بستری)
* **IPV:** Inactivated Polio Vaccine (واکسین تزریقی فلج اطفال)
* **IUCD:** Intrauterine Contraceptive Device (وسیله ضدبارداری داخل رحمی / آی‌یودی)
* **KMC:** Kangaroo Mother Care (مراقبت تماس پوست به پوست مادر و نوزاد کانگورویی)
* **KPI:** Key Performance Indicator (شاخص کلیدی عملکرد)
* **LQAS:** Lot Quality Assurance Sampling (نمونه‌گیری تضمین کیفیت دسته‌ای)
* **MAM:** Moderate Acute Malnutrition (سوءتغذیه حاد متوسط)
* **MCH:** Maternal and Child Health (صحت مادر و طفل)
* **MDR-TB:** Multi-Drug Resistant Tuberculosis (توبرکلوز مقاوم به چند دارو)
* **MIAR:** Monthly Integrated Activities Report (راپور ماهوار فعالیت‌های ادغام‌یافته کلینیک)
* **MNCH:** Maternal, Newborn, and Child Health (صحت مادر، نوزاد و طفل)
* **MoPH:** Ministry of Public Health (وزارت صحت عامه افغانستان)
* **MPDSR:** Maternal and Perinatal Death Surveillance and Response (سیستم ترصد و بررسی مرگ مادر و نوزاد)
* **MTR:** Mid-Term Review (ارزیابی میان‌دوره‌ای پروژه)
* **MUAC:** Mid-Upper Arm Circumference (محیط دور بازو جهت سنجش سوءتغذیه)
* **NDSR:** National Disease Surveillance and Response (سیستم ملی مراقبت و پاسخ به امراض)
* **NEML:** National Essential Medicines List (لست ملی ادویه اساسی)
* **NMR:** Neonatal Mortality Rate (نرخ مرگ‌ومیر نوزادان زیر ۲۸ روز)
* **OPD:** Outpatient Department (بخش مریضان سراپا)
* **OPV:** Oral Polio Vaccine (واکسین خوراکی فلج اطفال)
* **ORS:** Oral Rehydration Salts (پودر نمک‌های بازجذب خوراکی)
* **PCV:** Pneumococcal Conjugate Vaccine (واکسین کونژوگه پنوموکوک سینه‌بغل)
* **PDCA / PDSA:** Plan-Do-Check/Study-Act (چرخه چهارمرحله‌ای بهبود کیفیت)
* **PEP:** Post-Exposure Prophylaxis (وقایه دارویی پس از مواجهه تصادفی با ویروس)
* **PH:** Provincial Hospital (شفاخانه ولایتی)
* **PHCC:** Provincial Health Coordination Committee (کمیته هماهنگی صحی ولایت)
* **PIP:** Performance Improvement Plan (پلان بهبود عملکرد)
* **PNC:** Postnatal Care (مراقبت‌های پس از ولادت)
* **PPE:** Personal Protective Equipment (وسایل حفاظت فردی)
* **PPH:** Postpartum Hemorrhage (خونریزی مهلک پس از ولادت)
* **PPHD:** Provincial Public Health Directorate (ریاست صحت عامه ولایت)
* **PPM:** Planned Preventive Maintenance (نگهداری وقایوی پلان‌شده تجهیزات)
* **PSEA:** Protection from Sexual Exploitation and Abuse (حفاظت در برابر استثمار و سوءاستفاده جنسی)
* **QI:** Quality Improvement (بهبود کیفیت)
* **RDT:** Rapid Diagnostic Test (کیت تست تشخیصی سریع)
* **RH:** Reproductive Health (صحت باروری)
* **RH:** Regional Hospital (شفاخانه حوزوی)
* **ROP:** Reorder Point (نقطه سفارش مجدد کالا)
* **RRT:** Rapid Response Team (تیم واکنش سریع اپیدمی)
* **RUTF:** Ready-to-Use Therapeutic Food (غذای آماده درمانی سوءتغذیه / پلمپی‌نات)
* **SAM:** Severe Acute Malnutrition (سوءتغذیه حاد شدید)
* **SDD:** Solar Direct Drive (یخچال خورشیدی بدون باطری مستقیم)
* **SHC:** Sub-Health Center (مرکز صحی فرعی)
* **SMART:** Specific, Measurable, Achievable, Relevant, Time-bound (اهداف هوشمند)
* **SOP:** Standard Operating Procedure (دستورالعمل معیاری عملیاتی)
* **TB:** Tuberculosis (مرض توبرکلوز / سل)
* **Td:** Tetanus and reduced Diphtheria toxoid (واکسین کزاز و دیفتری بزرگسالان)
* **TIN:** Tax Identification Number (نمبر تشخیصیه مالیاتی شرکت‌ها)
* **ToR:** Terms of Reference (لایحه وظایف مکتوب کارمند)
* **TPM:** Third-Party Monitoring (نظارت شخص ثالث مستقل)
* **TSR:** Treatment Success Rate (نرخ موفقیت تداوی)
* **U5MR:** Under-5 Mortality Rate (نرخ مرگ‌ومیر اطفال زیر ۵ سال)
* **VEN:** Vital, Essential, Non-essential (سیستم اولویت‌بندی دارویی حیاتی، ضروری، غیرضروری)
* **VVM:** Vaccine Vial Monitor (شاخص حرارتی حساس به گرمای ویال واکسین)
* **WBS:** Work Breakdown Structure (ساختار شکست کار در مدیریت پروژه)
* **WFP:** World Food Programme (برنامه جهانی غذا)
* **WHO:** World Health Organization (سازمان صحی جهان)
* **WISN:** Workload Indicators of Staffing Need (شاخص‌های سنجش نیاز پرسونل بر اساس بار کاری).

---
"""

if __name__ == "__main__":
    t = get_part17_tools_text()
    print("Part 17 Tools length:", len(t))
