# -*- coding: utf-8 -*-
"""
generate_epub.py
Generates an EPUB3 book from manuscript/master.md using ebooklib
"""

import os
import re
import html
from ebooklib import epub

def create_epub(md_path, epub_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    book = epub.EpubBook()
    book.set_identifier('shuhada-daikundi-provincial-coordinator-2026')
    book.set_title('MASTER BLUEPRINT — PROVINCIAL COORDINATOR: 24-HOUR EXAM MASTER GUIDE')
    book.set_language('fa')
    book.add_author('Shuhada Organization — Daikundi Operations')
    
    # CSS
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: sans-serif;
        direction: rtl;
        text-align: right;
        line-height: 1.6;
        padding: 5%;
    }
    h1 { color: #1B365D; border-bottom: 2px solid #005A9C; }
    h2 { color: #005A9C; }
    h3 { color: #2D3748; }
    .callout {
        border-right: 4px solid #005A9C;
        background-color: #F0F4F8;
        padding: 10px;
        margin: 15px 0;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    th, td {
        border: 1px solid #CBD5E0;
        padding: 8px;
        text-align: right;
    }
    th {
        background-color: #1B365D;
        color: white;
    }
    '''
    default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
    book.add_item(default_css)

    # Split into sections by '# '
    sections = re.split(r'\n(?=# )', md)
    chapters = []
    
    for idx, sec in enumerate(sections):
        sec = sec.strip()
        if not sec:
            continue
        first_line = sec.split('\n')[0].replace('#', '').strip()
        c_title = first_line[:50] if first_line else f"Section {idx+1}"
        
        # Simple HTML conversion for each section
        sec_lines = sec.split('\n')
        sec_html = []
        for l in sec_lines:
            sl = l.strip()
            if sl.startswith('# '):
                sec_html.append(f'<h1>{html.escape(sl[2:])}</h1>')
            elif sl.startswith('## '):
                sec_html.append(f'<h2>{html.escape(sl[3:])}</h2>')
            elif sl.startswith('### '):
                sec_html.append(f'<h3>{html.escape(sl[4:])}</h3>')
            elif sl.startswith('>'):
                sec_html.append(f'<div class="callout">{html.escape(sl.lstrip(">").strip())}</div>')
            elif sl.startswith('* ') or sl.startswith('- '):
                sec_html.append(f'<li>{html.escape(sl[2:])}</li>')
            elif sl:
                sec_html.append(f'<p>{html.escape(sl)}</p>')
                
        c_item = epub.EpubHtml(title=c_title, file_name=f'chap_{idx:02d}.xhtml', lang='fa')
        c_item.content = f'<html><head><link rel="stylesheet" href="style/default.css"/></head><body dir="rtl">{"".join(sec_html)}</body></html>'
        c_item.add_item(default_css)
        book.add_item(c_item)
        chapters.append(c_item)

    book.toc = chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters

    os.makedirs(os.path.dirname(epub_path), exist_ok=True)
    epub.write_epub(epub_path, book)
    print(f"Generated EPUB saved at: {epub_path}")
    print(f"File size: {os.path.getsize(epub_path):,} bytes")

if __name__ == "__main__":
    create_epub("manuscript/master.md", "build/Provincial_Coordinator_24Hour_Exam_Master_Guide.epub")
