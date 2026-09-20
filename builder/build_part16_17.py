# -*- coding: utf-8 -*-
"""
Builder for Part XVI (Chapters 40 & 41) and Part XVII (Chapters 42 to 51):
Excel/Word Skills & The 10 Integrated Master Cases
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
from build_master_cases import get_master_cases_text

def get_part16_17_text():
    part16 = r"""
# PART XVI — EXCEL & OFFICE SKILLS
## فصل چهلم: مهارت‌های اکسل در ۳۰ دقیقه برای هماهنگ‌کننده ولایتی
### Practical Excel Formulas for Health & Budget Management

اکسل قدرتمندترین ابزار کار روزمره شماست. در امتحان و کار نیازی به فرمول‌های پیچیده ماکرو ندارید؛ تسلط بر فرمول‌های زیر کافی است:

| فورمول در اکسل | کاربرد عملی در کلینیک | مثال عینی |
| :--- | :--- | :--- |
| `=SUM(B2:B20)` | جمع کل مریضان، جمع مصارف بودجه | محاسبه مجموع مصارف ورکشاپ آموزشی |
| `=AVERAGE(C2:C13)` | محاسبه میانگین مصرف ماهوار دوا (AMC) | میانگین مصرف ماهوار اموکسی‌سیلین در ۶ ماه |
| `=COUNT(A2:A50)` | شمارش تعداد سطرهای عددی | شمارش تعداد کلینیک‌هایی که راپور داده‌اند |
| `=COUNTA(A2:A50)` | شمارش خانه‌های غیرخالی (نام کارمندان) | بررسی کامل بودن لست حاضری پرسونل |
| `=(B2/C2)*100` | محاسبه فیصدی پوشش و پیشرفت هدف | فیصدی اطفال واکسین‌شده نسبت به تارگت سالانه |
| `=B2-C2` | محاسبه تفاوت بودجه (Variance) | اختلاف بودجه منظورشده از مصرف واقعی |
| `=D2-E2` | مغایرت موجودی گدام (Stock Discrepancy) | استاک در سیستم منفی شمارش فزیکی |

---

### ۴۰.۱ تمرین محاسباتی اکسل: شیت مقایسه پیشرفت کلینیک‌ها
```
کلینیک       هدف ماهوار OPD     مراجعه واقعی      فیصدی تحقق (%)        وضعیت
اشترلی             ۵۰۰               ۴۳۰               ۸۶٪              نیاز به نظارت
شهرستان            ۸۰۰               ۸۴۰              ۱۰۵٪              موفق
میرامور            ۶۰۰               ۳۶۰               ۶۰٪              بحرانی (بررسی عاجل)
```

---

## فصل چهل‌ویکم: اصول نگارش و دیزاین راپورهای اداری در Word
### Word Formatting, Version Control & Professional Emailing

1. **سلسله‌مراتب عناوین (Headings):** عنوان کتاب (Title) $\rightarrow$ فصل‌ها (Heading 1) $\rightarrow$ بخش‌ها (Heading 2) $\rightarrow$ زیربخش‌ها (Heading 3). عدم استفاده از استایل‌های استاندارد ورد مانع ایجاد فهرست خودکار (Table of Contents) می‌شود.
2. **راست‌به‌چپ (RTL) و فونت:** متن‌های دری باید دارای دایرکشن RTL بوده و اصطلاحات انگلیسی درون پرانتز بدون بهم‌ریختگی تایپ شوند. فونت وزیرمتن (Vazirmatn) یا آریال برای متن و عناوین توصیه می‌شود.
3. **نام‌گذاری معیاری فایل‌ها (File Naming Convention):** هرگز فایلی را با نام `Report_final_new2.docx` ذخیره نکنید! نام‌گذاری استاندارد:
   `SO_DKD_MonthlyReport_Hamal1405_v1.0.docx`
   (نام سازمان _ ولایت _ نوع سند _ ماه و سال _ شماره نسخه).
4. **متن ایمیل حرفه‌ای جهت ارسال راپور:**
   * *موضوع ایمیل:* `Shuhada Organization Daikundi — Monthly Progress Report (Hamal 1405) — Submission`
   * *متن:* با ادای احترام رسمی، خلاصه ۳ دستاورد عمده در ۳ بولت‌پوینت، پیوست فایل با فرمت PDF و Word، و اعلام آمادگی برای پاسخ به سوالات تخنیکی.

---
"""
    return part16.strip() + "\n\n" + get_master_cases_text().strip()

if __name__ == "__main__":
    text = get_part16_17_text()
    print("Part 16 & 17 text length:", len(text))
