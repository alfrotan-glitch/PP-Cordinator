import sys, os
sys.path.insert(0, os.path.abspath('.'))
# -*- coding: utf-8 -*-
"""
build_management_deliverables.py
Compiles all deliverables for:
«مدیریت؛ مبانی و مهارت‌های اساسی مدیریت»
(Management: The Essentials — Afghan Dari Professional Edition)
- EPUB3
- DOCX
- HTML
- SVG & PNG Covers
"""
import os
import sys
from scripts.generate_management_cover import build_all as generate_covers
from scripts.publish_master_epub import build_epub
from scripts.generate_docx import build_docx_from_markdown
from scripts.generate_html import markdown_to_html

def build():
    print("================================================================")
    print("  COMPILING FLAGSHIP TEXTBOOK:")
    print("  «مدیریت؛ مبانی و مهارت‌های اساسی مدیریت»")
    print("  Management: The Essentials — Afghan Dari Professional Edition")
    print("================================================================")
    
    os.makedirs("build", exist_ok=True)
    
    # 1. Covers
    print("\n--- 1. Generating Publication Covers ---")
    generate_covers()
    
    # 2. EPUB3
    print("\n--- 2. Building EPUB3 Publication Archive ---")
    epub_out = "build/Management_The_Essentials_Afghan_Edition.epub"
    build_epub(
        book_id="mgmt-essentials-afghan-dari-2026-v1",
        title="مدیریت؛ مبانی و مهارت‌های اساسی مدیریت",
        subtitle="راهنمای جامع، کاربردی و مسلکی اصول مدیریت، رهبری سازمانی و حل مسائل در بستر افغانستان",
        author="دیپارتمنت مدیریت، رهبری سازمانی و انکشاف ظرفیت",
        cover_png="build/cover_management.png",
        manuscript_path="manuscript/management_essentials.md",
        output_epub_path=epub_out
    )
    
    # 3. HTML Reader
    print("\n--- 3. Compiling Standalone HTML Reader ---")
    html_out = "build/Management_The_Essentials_Afghan_Edition.html"
    markdown_to_html("manuscript/management_essentials.md", html_out)
    
    # 4. DOCX Document
    print("\n--- 4. Building Styled DOCX Document ---")
    docx_out = "build/Management_The_Essentials_Afghan_Edition.docx"
    build_docx_from_markdown("manuscript/management_essentials.md", docx_out)
    
    print("\n================================================================")
    print("  ALL MANAGEMENT DELIVERABLES SUCCESSFULLY COMPILED!")
    print(f"  EPUB : {epub_out} ({os.path.getsize(epub_out):,} bytes)")
    print(f"  DOCX : {docx_out} ({os.path.getsize(docx_out):,} bytes)")
    print(f"  HTML : {html_out} ({os.path.getsize(html_out):,} bytes)")
    print(f"  SVG  : build/cover_management.svg ({os.path.getsize('build/cover_management.svg'):,} bytes)")
    print(f"  PNG  : build/cover_management.png ({os.path.getsize('build/cover_management.png'):,} bytes)")
    print("================================================================")

if __name__ == "__main__":
    build()
