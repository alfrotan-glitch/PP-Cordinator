#!/usr/bin/env python3
"""
Cover and web artwork.

The cover is a typographic cover drawn with the same font family as the book
interior, over a low-contrast navy panel so that the title stays legible at
thumbnail size. Two images are produced:
    cover.png        - full cover (EPUB / DOCX / PDF / HTML)
    cover-thumb.png  - 600px wide version for the EPUB library grid
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import bookkit as bk

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'assets/art'
OUT = ROOT / 'assets'
W, H = 1600, 2400

NAVY = (18, 32, 58)
NAVY_DEEP = (11, 21, 40)
CREAM = (247, 245, 240)
GOLD = (201, 168, 106)
TEAL = (76, 168, 152)
GREY = (168, 176, 190)

TITLE = 'مدیریت'
SUBTITLE = 'مبانی و مهارت‌های اساسی مدیریت'
ENGLISH = 'Management: The Essentials'
EDITION = 'نسخهٔ دری افغانستان — ویرایش حرفه‌ای'
STRAP1 = 'بیست فصل  ·  سی کیس کاری  ·  بستهٔ چهارده‌گانهٔ ابزارها'
STRAP2 = 'صد و پنجاه پرسش تمرینی  ·  واژه‌نامهٔ کامل اصطلاحات'
FOOT = 'برای مدیران، سرپرستان و کوآردیناتوران سازمان‌ها و پروژه‌های افغانستان'


def base_canvas():
    art = ART / 'cover-base.png'
    if art.exists():
        img = Image.open(art).convert('RGB').resize((W, H), Image.LANCZOS)
    else:
        img = Image.new('RGB', (W, H), NAVY)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # graded panel: solid at the top, fading into the artwork lower down
    for y in range(H):
        if y < 1500:
            alpha = 205
        else:
            alpha = int(205 * max(0.0, 1 - (y - 1500) / 620))
        d.line([(0, y), (W, y)], fill=NAVY_DEEP + (alpha,))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGBA')
    return img


def main():
    img = base_canvas()
    draw = ImageDraw.Draw(img)

    margin = 140
    right = W - margin
    width = W - 2 * margin

    # top rule and publisher line
    draw.rectangle([margin, 150, right, 154], fill=TEAL)
    f_small = bk.font(34, 'body')
    bk.draw_line(img, right, 230, 'راهنمای حرفه‌ای مدیریت سازمانی', f_small, CREAM, 'rtl')
    bk.draw_line(img, margin, 232, 'Afghan Dari Professional Edition', bk.font(30, 'display'),
                 GREY, 'ltr')

    # main title
    f_title = bk.font(196, 'display')
    bk.draw_line(img, right, 640, TITLE, f_title, CREAM, 'rtl')
    draw.rectangle([right - 430, 700, right, 705], fill=GOLD)

    f_sub = bk.font(70, 'display')
    bk.draw_line(img, right, 800, SUBTITLE, f_sub, CREAM, 'rtl')

    bk.draw_line(img, right, 900, ENGLISH, bk.font(54, 'display'), TEAL, 'rtl')

    # descriptive strap in two lines
    f_body = bk.font(37, 'body')
    bk.draw_line(img, right, 1050, STRAP1, f_body, (220, 226, 236), 'rtl')
    bk.draw_line(img, right, 1108, STRAP2, f_body, (220, 226, 236), 'rtl')
    bk.draw_block(img, right, 1180, width, FOOT, f_body, GREY, 'rtl',
                  align='right', line_height=64)

    # edition seal
    seal_y = 1650
    draw.rounded_rectangle([margin + 40, seal_y, right - 40, seal_y + 190], radius=18,
                           outline=(70, 86, 116), width=2)
    bk.draw_line(img, right - 90, seal_y + 92, EDITION, bk.font(46, 'display'), CREAM, 'rtl')
    bk.draw_line(img, right - 90, seal_y + 158,
                 'بيست فصل  ·  کارگاه کیس  ·  ابزارها  ·  واژه‌نامه', f_small, TEAL, 'rtl')

    # footer band
    draw.rectangle([0, H - 26, W, H], fill=GOLD)
    draw.rectangle([0, 0, W, 14], fill=TEAL)

    out = OUT / 'cover.png'
    img.convert('RGB').save(out, 'PNG', optimize=True)
    thumb = img.convert('RGB').resize((640, 960), Image.LANCZOS)
    thumb.save(OUT / 'cover-thumb.png', 'PNG', optimize=True)
    print(f'cover -> {out} {img.size}, thumb 640x960')


if __name__ == '__main__':
    main()
