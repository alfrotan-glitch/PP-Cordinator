# -*- coding: utf-8 -*-
"""
generate_management_cover.py
Creates publication-grade SVG and PNG covers for:
«مدیریت؛ مبانی و مهارت‌های اساسی مدیریت»
(Management: The Essentials — Afghan Dari Professional Edition)
"""
import os
from PIL import Image, ImageDraw, ImageFont

def make_svg_cover_management():
    return r"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1800" width="1200" height="1800">
  <defs>
    <linearGradient id="bgGradM" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#061A24"/>
      <stop offset="40%" stop-color="#0C343D"/>
      <stop offset="100%" stop-color="#144D5A"/>
    </linearGradient>
    <linearGradient id="goldGradM" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C59B27"/>
      <stop offset="50%" stop-color="#F3E5AB"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
    <linearGradient id="shieldGradM" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1A6B7A"/>
      <stop offset="100%" stop-color="#082A30"/>
    </linearGradient>
    <filter id="shadowM" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000000" flood-opacity="0.55"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="1800" fill="url(#bgGradM)"/>

  <!-- Elegant Decorative Borders -->
  <rect x="40" y="40" width="1120" height="1720" rx="16" fill="none" stroke="url(#goldGradM)" stroke-width="4.5" opacity="0.9"/>
  <rect x="56" y="56" width="1088" height="1688" rx="12" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.25"/>

  <!-- Corner Flourishes -->
  <path d="M 60 130 L 130 60" stroke="url(#goldGradM)" stroke-width="3.5" fill="none"/>
  <path d="M 1140 130 L 1070 60" stroke="url(#goldGradM)" stroke-width="3.5" fill="none"/>
  <path d="M 60 1670 L 130 1740" stroke="url(#goldGradM)" stroke-width="3.5" fill="none"/>
  <path d="M 1140 1670 L 1070 1740" stroke="url(#goldGradM)" stroke-width="3.5" fill="none"/>

  <!-- Top Badge / Header -->
  <rect x="250" y="95" width="700" height="65" rx="32" fill="#04151D" stroke="url(#goldGradM)" stroke-width="2"/>
  <text x="600" y="137" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="24" font-weight="bold" fill="#F3E5AB" text-anchor="middle" direction="rtl">دیپارتمنت مدیریت، رهبری سازمانی و انکشاف ظرفیت</text>

  <!-- Main Dari Title -->
  <text x="600" y="270" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="52" font-weight="900" fill="#FFFFFF" text-anchor="middle" direction="rtl" filter="url(#shadowM)">مـــدیـریــت</text>
  <text x="600" y="355" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="44" font-weight="800" fill="#F3E5AB" text-anchor="middle" direction="rtl" filter="url(#shadowM)">مبانی و مهارت‌های اساسی مدیریت</text>

  <!-- English Subtitle -->
  <text x="600" y="435" font-family="'Helvetica Neue', Arial, sans-serif" font-size="30" font-weight="800" fill="#A5D8D6" text-anchor="middle" letter-spacing="4">MANAGEMENT: THE ESSENTIALS</text>
  <text x="600" y="480" font-family="'Helvetica Neue', Arial, sans-serif" font-size="21" font-weight="600" fill="#E2E8F0" text-anchor="middle" letter-spacing="2">AFGHAN DARI PROFESSIONAL EDITION</text>

  <!-- Gold Divider Bar -->
  <line x1="220" y1="525" x2="980" y2="525" stroke="url(#goldGradM)" stroke-width="4" stroke-linecap="round"/>

  <!-- Central Crest / Shield -->
  <g transform="translate(600, 890)" filter="url(#shadowM)">
    <!-- Laurel Wreath Background -->
    <path d="M -300 0 C -300 -180 -180 -300 0 -300 C 180 -300 300 -180 300 0 C 300 180 180 300 0 300 C -180 300 -300 180 -300 0" fill="none" stroke="url(#goldGradM)" stroke-width="2" opacity="0.35" stroke-dasharray="12,12"/>
    
    <!-- Outer Shield -->
    <path d="M 0 -240 L 220 -130 L 180 140 L 0 250 L -180 140 L -220 -130 Z" fill="url(#shieldGradM)" stroke="url(#goldGradM)" stroke-width="4.5"/>
    <path d="M 0 -220 L 200 -120 L 165 125 L 0 225 L -165 125 L -200 -120 Z" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.4"/>

    <!-- Central Pillar Graphic: Integrated System -->
    <rect x="-14" y="-120" width="28" height="200" fill="url(#goldGradM)" rx="4"/>
    <rect x="-90" y="-14" width="180" height="28" fill="url(#goldGradM)" rx="4"/>
    <circle cx="0" cy="-20" r="46" fill="#061A24" stroke="url(#goldGradM)" stroke-width="3"/>
    
    <!-- Central Icon Letter M -->
    <text x="0" y="-4" font-family="'Helvetica Neue', Arial, sans-serif" font-size="44" font-weight="900" fill="#F3E5AB" text-anchor="middle">M</text>

    <!-- Cycle Ribbon below shield -->
    <rect x="-340" y="275" width="680" height="58" rx="14" fill="#04151D" stroke="url(#goldGradM)" stroke-width="2.5"/>
    <text x="0" y="312" font-family="'Helvetica Neue', Arial, sans-serif" font-size="15" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">PLAN • ORGANIZE • STAFF • LEAD • CONTROL • IMPROVE</text>
  </g>

  <!-- Content Scope Badges -->
  <g transform="translate(600, 1340)">
    <rect x="-440" y="0" width="880" height="170" rx="16" fill="#07222B" stroke="#1A6B7A" stroke-width="2.5"/>
    <text x="0" y="42" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="22" font-weight="bold" fill="#F3E5AB" text-anchor="middle" direction="rtl">مرجع جامع، اصیل و کاربردی مدیریت سازمانی در افغانستان</text>
    <text x="0" y="82" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="17" fill="#E2E8F0" text-anchor="middle" direction="rtl">۲۰ بخش کامل • ۳۰ کیس بزرگ تحلیلی • ۱۴ جعبه‌ابزار کاربردی مدیریت</text>
    <text x="0" y="118" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="17" fill="#7FE0D4" text-anchor="middle" direction="rtl">۱۵۰ سوال چهارجوابی (MCQs) • ۳۰ سناریوی واقعی • ۳۰ سوال مفهومی • ۳ آزمون شبیه‌ساز</text>
    <text x="0" y="148" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="16" fill="#CBD5E1" text-anchor="middle" direction="rtl">تحلیل ۵ سوال طلایی • حل منازعه • اخلاق مسلکی • تفویض صلاحیت • مدیریت استراتژیک</text>
  </g>

  <!-- Footer Edition & Author -->
  <text x="600" y="1610" font-family="'Vazirmatn', Tahoma, sans-serif" font-size="20" font-weight="600" fill="#9CA3AF" text-anchor="middle" direction="rtl">ویرایش اول مسلکی و دانشگاهی — سال ۱۴۰۵ / 2026</text>
  <text x="600" y="1650" font-family="'Helvetica Neue', Arial, sans-serif" font-size="16" font-weight="500" fill="#6B7280" text-anchor="middle">OFFICIAL MANAGEMENT TEXTBOOK SERIES • KABUL, AFGHANISTAN</text>
</svg>"""

def create_raster_cover_management(png_path):
    img = Image.new('RGB', (1200, 1800), color=(12, 52, 61))
    draw = ImageDraw.Draw(img)
    
    # Outer Gold Frame
    draw.rectangle([40, 40, 1160, 1760], outline=(212, 175, 55), width=6)
    draw.rectangle([56, 56, 1144, 1744], outline=(255, 255, 255), width=2)
    
    # Header box
    draw.rectangle([250, 95, 950, 160], fill=(4, 21, 29), outline=(212, 175, 55), width=3)
    
    # Center shield placeholder
    draw.polygon([(600, 650), (820, 760), (780, 1030), (600, 1140), (420, 1030), (380, 760)], fill=(26, 107, 122), outline=(243, 229, 171), width=4)
    draw.ellipse([540, 830, 660, 950], fill=(6, 26, 36), outline=(243, 229, 171), width=4)
    
    # Central pillar cross
    draw.rectangle([590, 770, 610, 1010], fill=(243, 229, 171))
    draw.rectangle([530, 880, 670, 900], fill=(243, 229, 171))
    
    # Bottom badge
    draw.rectangle([160, 1340, 1040, 1510], fill=(7, 34, 43), outline=(26, 107, 122), width=3)
    
    img.save(png_path, "PNG", quality=95)
    print(f"Generated PNG cover: {png_path} ({os.path.getsize(png_path):,} bytes)")

def build_all():
    os.makedirs("build", exist_ok=True)
    svg_path = "build/cover_management.svg"
    png_path = "build/cover_management.png"
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(make_svg_cover_management())
    print(f"Generated SVG cover: {svg_path} ({os.path.getsize(svg_path):,} bytes)")
    
    create_raster_cover_management(png_path)

if __name__ == "__main__":
    build_all()
