#!/usr/bin/env python3
"""
Cover generator: a clean typographic cover (no generated artwork), drawn with
Pillow using the same embedded Vazir font, so DOCX / PDF / EPUB all share it.
RTL text is shaped with arabic-reshaper + python-bidi.
"""
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / 'project/assets/fonts'
OUT = ROOT / 'project/assets/cover.png'

W, H = 1600, 2400
NAVY = (31, 58, 95)
TEAL = (15, 107, 94)
CREAM = (250, 248, 244)
GREY = (90, 90, 95)
RESHAPER = arabic_reshaper.ArabicReshaper(
    configuration={'delete_harakat': False, 'support_ligatures': True})


def rtl(t):
    return get_display(RESHAPER.reshape(t))


def font(size, name='Vazir'):
    return ImageFont.truetype(str(FONTS / f'{name}.ttf'), size)


def text_center(draw, y, txt, f, fill, rtl_text=True):
    s = rtl(txt) if rtl_text else txt
    bbox = draw.textbbox((0, 0), s, font=f)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) / 2, y), s, font=f, fill=fill)
    return y + (bbox[3] - bbox[1])


def main():
    img = Image.new('RGB', (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # frame + bands
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.rectangle([0, H - 24, W, H], fill=NAVY)
    d.rectangle([80, 80, W - 80, H - 80], outline=NAVY, width=3)
    d.rectangle([120, 120, W - 120, H - 120], outline=(200, 200, 205), width=1)

    y = 300
    y = text_center(d, y, 'سازمان شهدا — ولایت دایکندی', font(52), TEAL) + 20
    y = text_center(d, y, 'Shuhada Organization — Daikundi', font(40, 'Samim'), GREY,
                    rtl_text=False) + 120

    y = text_center(d, y, 'کتاب قانون زبان', font(150), NAVY) + 40
    d.line([(W * 0.22, y + 20), (W * 0.78, y + 20)], fill=TEAL, width=4)
    y += 70

    y = text_center(d, y, 'راهنمای جامع و عملی', font(72), (40, 40, 45)) + 18
    y = text_center(d, y, 'Provincial Coordinator', font(72, 'Samim'), NAVY,
                    rtl_text=False) + 60

    y = text_center(d, y, 'در بخش صحت — با سناریوهای واقعی، تمرین و جواب مدل',
                    font(44), GREY) + 160

    # three small emblem blocks
    bx = W / 2 - 300
    for label in ('پلان', 'نظارت', 'راپور'):
        d.rounded_rectangle([bx, y, bx + 200, y + 120], radius=16, outline=TEAL, width=3)
        bbox = d.textbbox((0, 0), rtl(label), font=font(50))
        d.text((bx + (200 - (bbox[2] - bbox[0])) / 2, y + 30), rtl(label),
               font=font(50), fill=NAVY)
        bx += 200

    y += 300
    y = text_center(d, y, 'نسخه دوم — ویرایش‌شده، تصحیح‌شده و آماده نشر',
                    font(46), GREY) + 24
    y = text_center(d, y, '۱۴۰۵ خورشیدی', font(60), NAVY) + 80
    text_center(d, y, '«Working for a better tomorrow»', font(40, 'Samim'), GREY,
                rtl_text=False)

    img.save(OUT, 'PNG')
    print('cover ->', OUT, img.size)


if __name__ == '__main__':
    main()
