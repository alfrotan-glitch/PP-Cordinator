# Reference Alignment Audit — canonical template
# الگوی استانداردِ ممیزیِ انطباق با مرجع

**Purpose:** this file is the single source of truth for the 12 canonical audit questions.
`scripts/qa_scan.py` reads them from here and verifies that every chapter answers all 12.
Do not reword these lines when copying them into a chapter — the scanner matches them literally.

**Usage:** copy the 12 lines below into the audit table at the end of every chapter, replacing
`- [ ]` with the result (✅ / ⚠️ / ❌) and adding a note column.

---

## The 12 checks / دوازده بررسی

- [ ] آیا تمام مفاهیم اصلی Chapter پوشش داده شده‌اند؟
- [ ] آیا تعریف‌ها علمی و دقیق هستند؟
- [ ] آیا Classification درست است؟
- [ ] آیا Structure درست است؟
- [ ] آیا Function درست است؟
- [ ] آیا Structure–Function relationship درست است؟
- [ ] آیا ویژگی‌های Histological Identification حفظ شده‌اند؟
- [ ] آیا نکات مهم امتحانی حذف نشده‌اند؟
- [ ] آیا اصطلاحات مهم تغییر نیستند؟
- [ ] آیا چیزی برخلاف Reference اضافه نشده است؟
- [ ] آیا کوتاه‌سازی باعث از بین رفتن یک مفهوم مهم نشده است؟
- [ ] آیا متن تولیدشده یک متن مستقل و آموزشی است و بازتولید متن کتاب اصلی نیست؟

---

## Scoring legend / راهنمای نمره‌گذاری

| علامت | معنا |
|---|---|
| ✅ | بررسی با موفقیت انجام شده — passed |
| ⚠️ | نکته‌ای نیاز به توجه یا گسترش دارد — passed with a note |
| ❌ | مشکل مسدودکننده — blocking issue, chapter is not release-ready |

## Rule

If any check is ❌, the chapter status is not "done" regardless of how much of it is written.
Record ❌ items in `editorial/change-log.md` as open issues.
