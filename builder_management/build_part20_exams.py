# -*- coding: utf-8 -*-
"""
Part 20: Comprehensive Practice & Exam Bank
Combines all MCQs, scenarios, short-answers, exercises, interviews, and mock exams.
"""
from builder_management.build_part20_mcqs_1_50 import get_mcqs_1_50
from builder_management.build_part20_mcqs_51_100 import get_mcqs_51_100
from builder_management.build_part20_mcqs_101_150 import get_mcqs_101_150
from builder_management.build_part20_scenarios_short import get_scenarios_and_short_answers
from builder_management.build_part20_exercises import get_exercises_text
from builder_management.build_part20_interviews_mocks import get_interviews_and_mocks

def get_part20_text():
    intro = r"""
# بخش بیستم: بانک جامع تمرینات و آزمون‌های مدیریتی
## فصل بیستم: ارزشیابی، سنجش مهارت و آمادگی برای میدان عمل
### Comprehensive Practice and Assessment Bank: MCQs, Scenarios, Exercises & Mock Exams

این بخش به عنوان گسترده‌ترین و جامع‌ترین بانک آزمون و تمرین مدیریتی در افغانستان طراحی شده است. هیچ مدیری بدون آزمودن دانسته‌های خود در بوته آزمایش‌های سنجش مهارت به کمال نمی‌رسد. بخش بیستم شامل اجزای زیر است:
1. **۱۵۰ سوال چهارجوابی تخصصی (MCQs)** همراه با پاسخ‌های تشریحی و تحلیل مسلکی
2. **۳۰ سناریوی واقعی مدیریتی** با تحلیل تفصیلی اقدامات
3. **۳۰ پرسش پاسخ کوتاه مفهومی** با پاسخ‌های الگو
4. **۳۰ تمرین عملی و کارگاهی**
5. **۲۰ تمرین دوراهی تصمیم‌گیری**
6. **۲۰ تمرین رهبری و نفوذ تیمی**
7. **۲۰ تمرین ارتباطات حرفه‌ای سازمانی**
8. **۲۰ پرسش تخصصی مصاحبه استخدامی** با روباریک نمره‌دهی
9. **۳ آزمون جامع شبیه‌سازی‌شده (Mock Exams)**
"""
    return (
        intro + "\n\n" +
        get_mcqs_1_50() + "\n\n" +
        get_mcqs_51_100() + "\n\n" +
        get_mcqs_101_150() + "\n\n" +
        get_scenarios_and_short_answers() + "\n\n" +
        get_exercises_text() + "\n\n" +
        get_interviews_and_mocks()
    )

if __name__ == "__main__":
    t = get_part20_text()
    print("Part 20 Total Characters:", len(t))
