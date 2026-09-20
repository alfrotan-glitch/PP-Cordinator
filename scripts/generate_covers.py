# -*- coding: utf-8 -*-
"""
generate_covers.py
Creates publication-grade vector SVG and PNG cover illustrations for Book 1 and Book 2.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def make_svg_cover_book1():
    return r"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1800" width="1200" height="1800">
  <defs>
    <linearGradient id="bgGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#081A36"/>
      <stop offset="50%" stop-color="#0F2C59"/>
      <stop offset="100%" stop-color="#163E75"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#B8860B"/>
      <stop offset="50%" stop-color="#E5C158"/>
      <stop offset="100%" stop-color="#C28B14"/>
    </linearGradient>
    <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E4D8C"/>
      <stop offset="100%" stop-color="#0A1F3D"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="1800" fill="url(#bgGrad1)"/>

  <!-- Elegant Decorative Borders -->
  <rect x="40" y="40" width="1120" height="1720" rx="16" fill="none" stroke="url(#goldGrad)" stroke-width="4" opacity="0.85"/>
  <rect x="55" y="55" width="1090" height="1690" rx="12" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.25"/>

  <!-- Corner Flourishes -->
  <path d="M 60 120 L 120 60" stroke="url(#goldGrad)" stroke-width="3" fill="none"/>
  <path d="M 1140 120 L 1080 60" stroke="url(#goldGrad)" stroke-width="3" fill="none"/>
  <path d="M 60 1680 L 120 1740" stroke="url(#goldGrad)" stroke-width="3" fill="none"/>
  <path d="M 1140 1680 L 1080 1740" stroke="url(#goldGrad)" stroke-width="3" fill="none"/>

  <!-- Top Badge / Header -->
  <rect x="300" y="100" width="600" height="60" rx="30" fill="#061326" stroke="url(#goldGrad)" stroke-width="2"/>
  <text x="600" y="140" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="24" font-weight="bold" fill="#E5C158" text-anchor="middle" direction="rtl">سازمان شهدا (Shuhada Organization) — ولایت دایکندی</text>

  <!-- Main Dari Title -->
  <text x="600" y="270" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="46" font-weight="900" fill="#FFFFFF" text-anchor="middle" direction="rtl" filter="url(#shadow)">رهنمای جامع آزمون استخدامی و وظایف</text>
  <text x="600" y="350" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="56" font-weight="900" fill="#E5C158" text-anchor="middle" direction="rtl" filter="url(#shadow)">هماهنگ‌کننده ولایتی</text>

  <!-- English Subtitle -->
  <text x="600" y="430" font-family="'Helvetica Neue', Arial, sans-serif" font-size="28" font-weight="800" fill="#A8C7FA" text-anchor="middle" letter-spacing="4">PROVINCIAL COORDINATOR</text>
  <text x="600" y="475" font-family="'Helvetica Neue', Arial, sans-serif" font-size="24" font-weight="600" fill="#FFFFFF" text-anchor="middle" letter-spacing="2">24-HOUR EXAM &amp; FIELD PRACTICE MASTER GUIDE</text>

  <!-- Gold Divider Bar -->
  <line x1="250" y1="520" x2="950" y2="520" stroke="url(#goldGrad)" stroke-width="4" stroke-linecap="round"/>

  <!-- Central Emblem / Crest Graphic -->
  <g transform="translate(600, 830)" filter="url(#shadow)">
    <!-- Outer Shield -->
    <path d="M 0 -220 Q 180 -220 220 -100 Q 220 120 0 240 Q -220 120 -220 -100 Q -180 -220 0 -220 Z" fill="url(#shieldGrad)" stroke="url(#goldGrad)" stroke-width="6"/>
    <!-- Inner Arch Pattern -->
    <path d="M 0 -180 Q 140 -180 170 -80 Q 170 90 0 190 Q -170 90 -170 -80 Q -140 -180 0 -180 Z" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.3"/>
    
    <!-- Stylized Scales of Justice / Governance Star -->
    <circle cx="0" cy="-20" r="70" fill="#081A36" stroke="url(#goldGrad)" stroke-width="4"/>
    <!-- Emblem Compass / Star -->
    <polygon points="0,-75 16,-30 65,-20 25,12 36,60 0,30 -36,60 -25,12 -65,-20 -16,-30" fill="url(#goldGrad)"/>
    
    <!-- Core Formula Ribbon below shield -->
    <rect x="-240" y="270" width="480" height="55" rx="12" fill="#0A1F3D" stroke="url(#goldGrad)" stroke-width="2"/>
    <text x="0" y="306" font-family="'Helvetica Neue', Arial, sans-serif" font-size="18" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">UNDERSTAND → PRIORITIZE → COORDINATE</text>
  </g>

  <!-- Key Pillars Badges -->
  <g transform="translate(600, 1340)">
    <rect x="-420" y="0" width="840" height="150" rx="16" fill="#07162C" stroke="#1E4D8C" stroke-width="2"/>
    <text x="0" y="40" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="22" font-weight="bold" fill="#E5C158" text-anchor="middle" direction="rtl">ویژه داوطلبان پست‌های هماهنگ‌کننده ولایتی، مدیر پروژه و رهبری دفاتر ساحوی</text>
    <text x="0" y="80" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="18" fill="#D1D5DB" text-anchor="middle" direction="rtl">شامل ۶۲ فصل کاربردی | ۲۶ قضیه تفصیلی ساحوی | ۲۰۰ سوال امتحانی با پاسخ تشریحی</text>
    <text x="0" y="118" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="18" fill="#A8C7FA" text-anchor="middle" direction="rtl">سیستم‌های BPHS/EPHS • مدیریت مالی و تدارکات • اصول PSEA • دیتای HMIS</text>
  </g>

  <!-- Footer Edition & Author -->
  <text x="600" y="1600" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="20" font-weight="600" fill="#9CA3AF" text-anchor="middle" direction="rtl">چاپ اول مسلکی — سال ۱۴۰۵ / 2026</text>
  <text x="600" y="1640" font-family="'Helvetica Neue', Arial, sans-serif" font-size="16" font-weight="500" fill="#6B7280" text-anchor="middle">OFFICIAL EXAM &amp; OPERATIONS SERIES • SHUHADA ORGANIZATION</text>
</svg>"""

def make_svg_cover_book2():
    return r"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1800" width="1200" height="1800">
  <defs>
    <linearGradient id="bgGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#041E24"/>
      <stop offset="50%" stop-color="#0A3641"/>
      <stop offset="100%" stop-color="#0E4C5B"/>
    </linearGradient>
    <linearGradient id="tealGold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00A896"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#02C39A"/>
    </linearGradient>
    <linearGradient id="medGold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#F3E5AB"/>
    </linearGradient>
    <linearGradient id="shieldGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0E5463"/>
      <stop offset="100%" stop-color="#06252C"/>
    </linearGradient>
    <filter id="shadow2" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="1800" fill="url(#bgGrad2)"/>

  <!-- Elegant Decorative Borders -->
  <rect x="40" y="40" width="1120" height="1720" rx="16" fill="none" stroke="url(#medGold)" stroke-width="4" opacity="0.85"/>
  <rect x="55" y="55" width="1090" height="1690" rx="12" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.25"/>

  <!-- Corner Flourishes -->
  <path d="M 60 120 L 120 60" stroke="url(#medGold)" stroke-width="3" fill="none"/>
  <path d="M 1140 120 L 1080 60" stroke="url(#medGold)" stroke-width="3" fill="none"/>
  <path d="M 60 1680 L 120 1740" stroke="url(#medGold)" stroke-width="3" fill="none"/>
  <path d="M 1140 1680 L 1080 1740" stroke="url(#medGold)" stroke-width="3" fill="none"/>

  <!-- Top Badge / Header -->
  <rect x="280" y="100" width="640" height="60" rx="30" fill="#04161B" stroke="url(#medGold)" stroke-width="2"/>
  <text x="600" y="140" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="24" font-weight="bold" fill="#D4AF37" text-anchor="middle" direction="rtl">سازمان شهدا (Shuhada Organization) — دیپارتمنت صحت عامه</text>

  <!-- Main Dari Title -->
  <text x="600" y="270" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="44" font-weight="900" fill="#FFFFFF" text-anchor="middle" direction="rtl" filter="url(#shadow2)">مدیریت صحی در افغانستان</text>
  <text x="600" y="350" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="52" font-weight="900" fill="#D4AF37" text-anchor="middle" direction="rtl" filter="url(#shadow2)">رهنما و مرجع جامع ۲۴ ساعته آزمون و ساحه</text>

  <!-- English Subtitle -->
  <text x="600" y="430" font-family="'Helvetica Neue', Arial, sans-serif" font-size="28" font-weight="800" fill="#7FE0D4" text-anchor="middle" letter-spacing="4">HEALTH MANAGEMENT</text>
  <text x="600" y="475" font-family="'Helvetica Neue', Arial, sans-serif" font-size="24" font-weight="600" fill="#FFFFFF" text-anchor="middle" letter-spacing="2">24-HOUR EXAM &amp; FIELD PRACTICE MASTER GUIDE</text>

  <!-- Gold/Teal Divider Bar -->
  <line x1="250" y1="520" x2="950" y2="520" stroke="url(#tealGold)" stroke-width="4" stroke-linecap="round"/>

  <!-- Central Medical Shield & Caduceus Graphic -->
  <g transform="translate(600, 830)" filter="url(#shadow2)">
    <!-- Outer Shield -->
    <path d="M 0 -220 Q 180 -220 220 -100 Q 220 120 0 240 Q -220 120 -220 -100 Q -180 -220 0 -220 Z" fill="url(#shieldGrad2)" stroke="url(#medGold)" stroke-width="6"/>
    <!-- Medical Cross -->
    <path d="M -40 -120 L 40 -120 L 40 -40 L 120 -40 L 120 40 L 40 40 L 40 120 L -40 120 L -40 40 L -120 40 L -120 -40 L -40 -40 Z" fill="#00A896" stroke="#FFFFFF" stroke-width="3" opacity="0.95"/>
    
    <!-- Central Caduceus / Health System Icon -->
    <circle cx="0" cy="0" r="32" fill="#041E24" stroke="url(#medGold)" stroke-width="3"/>
    <text x="0" y="10" font-family="'Helvetica Neue', Arial, sans-serif" font-size="28" font-weight="900" fill="#D4AF37" text-anchor="middle">H</text>

    <!-- 7 Pillars Ribbon below shield -->
    <rect x="-260" y="270" width="520" height="55" rx="12" fill="#041E24" stroke="url(#medGold)" stroke-width="2"/>
    <text x="0" y="306" font-family="'Helvetica Neue', Arial, sans-serif" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">PEOPLE • SERVICE • DATA • SUPPLIES • FINANCE • QUALITY</text>
  </g>

  <!-- Content Scope Badges -->
  <g transform="translate(600, 1340)">
    <rect x="-420" y="0" width="840" height="150" rx="16" fill="#05242B" stroke="#00A896" stroke-width="2"/>
    <text x="0" y="40" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="22" font-weight="bold" fill="#D4AF37" text-anchor="middle" direction="rtl">بانک جامع آزمون‌های استخدامی مدیریت تسهیلات و کلینیک‌های صحی</text>
    <text x="0" y="80" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="18" fill="#D1D5DB" text-anchor="middle" direction="rtl">۱۰۲ فصل تخصصی | ۳۰ قضیه جامع عملیاتی | ۲۷۰ سوال مسلسل (Q1-Q270) با پاسخ تشریحی</text>
    <text x="0" y="118" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="18" fill="#7FE0D4" text-anchor="middle" direction="rtl">۳ آزمون شبیه‌سازی کامل • ۳۰ سوال مصاحبه تخنیکی • ۲۰ مینی‌کیس • زنجیره سرد و DHIS2</text>
  </g>

  <!-- Footer Edition & Author -->
  <text x="600" y="1600" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="20" font-weight="600" fill="#9CA3AF" text-anchor="middle" direction="rtl">چاپ اول مسلکی — سال ۱۴۰۵ / 2026</text>
  <text x="600" y="1640" font-family="'Helvetica Neue', Arial, sans-serif" font-size="16" font-weight="500" fill="#6B7280" text-anchor="middle">OFFICIAL HEALTH MANAGEMENT SERIES • SHUHADA ORGANIZATION</text>
</svg>"""

def create_raster_cover_book1(png_path):
    img = Image.new('RGB', (1200, 1800), color=(15, 44, 89))
    draw = ImageDraw.Draw(img)
    
    # Outer Gold Frame
    draw.rectangle([40, 40, 1160, 1760], outline=(194, 139, 20), width=6)
    draw.rectangle([55, 55, 1145, 1745], outline=(255, 255, 255), width=2)
    
    # Header box
    draw.rectangle([250, 100, 950, 160], fill=(8, 26, 54), outline=(194, 139, 20), width=3)
    
    # Center shield placeholder
    draw.polygon([(600, 650), (780, 750), (740, 980), (600, 1120), (460, 980), (420, 750)], fill=(30, 77, 140), outline=(229, 193, 88))
    draw.ellipse([540, 830, 660, 950], fill=(8, 26, 54), outline=(229, 193, 88), width=4)
    
    # Bottom badge
    draw.rectangle([180, 1320, 1020, 1480], fill=(7, 22, 44), outline=(30, 77, 140), width=3)
    
    img.save(png_path, "PNG", quality=95)
    print(f"Generated PNG cover: {png_path}")

def create_raster_cover_book2(png_path):
    img = Image.new('RGB', (1200, 1800), color=(10, 54, 65))
    draw = ImageDraw.Draw(img)
    
    # Outer Gold Frame
    draw.rectangle([40, 40, 1160, 1760], outline=(212, 175, 55), width=6)
    draw.rectangle([55, 55, 1145, 1745], outline=(255, 255, 255), width=2)
    
    # Header box
    draw.rectangle([250, 100, 950, 160], fill=(4, 30, 36), outline=(212, 175, 55), width=3)
    
    # Center shield placeholder
    draw.polygon([(600, 650), (780, 750), (740, 980), (600, 1120), (460, 980), (420, 750)], fill=(14, 84, 99), outline=(212, 175, 55))
    draw.rectangle([560, 800, 640, 960], fill=(0, 168, 150))
    draw.rectangle([520, 840, 680, 920], fill=(0, 168, 150))
    draw.ellipse([560, 840, 640, 920], fill=(4, 30, 36), outline=(212, 175, 55), width=3)
    
    # Bottom badge
    draw.rectangle([180, 1320, 1020, 1480], fill=(5, 36, 43), outline=(0, 168, 150), width=3)
    
    img.save(png_path, "PNG", quality=95)
    print(f"Generated PNG cover: {png_path}")

def generate_all_covers():
    os.makedirs("build", exist_ok=True)
    
    # Book 1
    svg1_path = "build/cover_book1.svg"
    png1_path = "build/cover_book1.png"
    with open(svg1_path, "w", encoding="utf-8") as f:
        f.write(make_svg_cover_book1())
    create_raster_cover_book1(png1_path)
    print(f"Book 1 Covers generated: {svg1_path}, {png1_path}")
    
    # Book 2
    svg2_path = "build/cover_book2.svg"
    png2_path = "build/cover_book2.png"
    with open(svg2_path, "w", encoding="utf-8") as f:
        f.write(make_svg_cover_book2())
    create_raster_cover_book2(png2_path)
    print(f"Book 2 Covers generated: {svg2_path}, {png2_path}")

if __name__ == "__main__":
    generate_all_covers()
