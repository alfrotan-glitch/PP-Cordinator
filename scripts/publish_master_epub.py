# -*- coding: utf-8 -*-
"""
publish_master_epub.py
Builds publication-quality, accessible, and elegant EPUB3 editions for:
1. Book 1: Provincial Coordinator — Field Management & Exam Readiness
2. Book 2: Health Management — Professional Learning & Field Practice

Follows strict publication standards:
- Elegant typography optimized for Afghan Dari & English long-form reading
- Responsive, mobile-first design with dark mode support
- Clean semantic XHTML, zero LaTeX/HTML leakage
- Valid EPUB3 package, manifest, spine, NCX, and NAV
"""

import os
import re
import html
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

CSS_STYLES = """@charset "utf-8";

/* ==========================================================================
   Master EPUB3 Professional Publication Stylesheet
   Dari / Pashto / English Bilingual Typography
   Focus: Readability, Restrained Elegance, Accessibility
   ========================================================================== */

@namespace "http://www.w3.org/1999/xhtml";

:root {
  --primary-color: #1e3a8a;
  --secondary-color: #0f766e;
  --text-main: #1f2937;
  --text-muted: #4b5563;
  --bg-main: #ffffff;
  --bg-subtle: #f8fafc;
  --border-light: #e2e8f0;
  --border-strong: #94a3b8;
  --table-head-bg: #1e293b;
  --callout-border: #0284c7;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Vazirmatn", "IRANSans", "Tahoma", "Arial", sans-serif;
  font-size: 1.05em;
  line-height: 1.85;
  color: var(--text-main);
  background-color: var(--bg-main);
  direction: rtl;
  text-align: justify;
  margin: 0;
  padding: 4% 5%;
  word-wrap: break-word;
}

/* Headings */
h1.part-header {
  font-size: 1.8em;
  font-weight: 800;
  color: #0f172a;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 8px;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  line-height: 1.35;
  text-align: right;
  page-break-before: always;
}

h2.chapter-header {
  font-size: 1.4em;
  font-weight: 700;
  color: var(--primary-color);
  border-right: 4px solid var(--secondary-color);
  padding-right: 10px;
  margin-top: 1.4em;
  margin-bottom: 0.6em;
  line-height: 1.4;
  text-align: right;
}

h3.section-header {
  font-size: 1.18em;
  font-weight: 700;
  color: var(--secondary-color);
  margin-top: 1.2em;
  margin-bottom: 0.5em;
  text-align: right;
}

h4.sub-header {
  font-size: 1.05em;
  font-weight: 600;
  color: #334155;
  margin-top: 1em;
  margin-bottom: 0.4em;
  text-align: right;
}

/* Paragraphs & Text */
p.para {
  margin-top: 0;
  margin-bottom: 1em;
  line-height: 1.85;
}

strong {
  font-weight: 700;
  color: #0f172a;
}

code {
  font-family: Consolas, "Courier New", monospace;
  font-size: 0.88em;
  background-color: #f1f5f9;
  padding: 2px 5px;
  border-radius: 3px;
  direction: ltr;
  display: inline-block;
}

/* Lists */
ul.bullet-list, ol.numbered-list {
  margin: 0.6em 0 1.2em 0;
  padding-right: 24px;
  padding-left: 0;
}

li.bullet-item, li.numbered-item {
  margin-bottom: 0.5em;
  line-height: 1.8;
}

/* Cards & Text Callouts (Restrained & Elegant) */
.quote-card {
  background-color: var(--bg-subtle);
  border-right: 3px solid var(--primary-color);
  padding: 10px 16px;
  margin: 1.1em 0;
  color: #334155;
  border-radius: 0 4px 4px 0;
}

.model-answer-card {
  background-color: #f0fdf4;
  border-right: 3px solid #16a34a;
  border-radius: 0 6px 6px 0;
  padding: 12px 16px;
  margin: 1.2em 0;
  color: #14532d;
}

.exam-tip-card {
  background-color: #eff6ff;
  border-right: 3px solid #2563eb;
  border-radius: 0 6px 6px 0;
  padding: 12px 16px;
  margin: 1.2em 0;
  color: #1e3a8a;
}

.warning-card {
  background-color: #fef2f2;
  border-right: 3px solid #dc2626;
  border-radius: 0 6px 6px 0;
  padding: 12px 16px;
  margin: 1.2em 0;
  color: #7f1d1d;
}

.diagram-box {
  background-color: #0f172a;
  color: #f8fafc;
  padding: 12px 16px;
  border-radius: 6px;
  margin: 1.2em 0;
  direction: ltr;
  text-align: left;
  overflow-x: auto;
}
.diagram-box pre {
  margin: 0;
  font-family: Consolas, monospace;
  font-size: 0.85em;
  line-height: 1.5;
}

/* Formulas & Math */
.inline-math {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-weight: 600;
  color: #0369a1;
  direction: ltr;
  display: inline-block;
  padding: 0 2px;
}

.math-card {
  background: var(--bg-subtle);
  border: 1px solid var(--border-light);
  border-top: 3px solid var(--secondary-color);
  border-radius: 6px;
  padding: 12px 16px;
  margin: 1.2em 0;
  text-align: center;
  direction: ltr;
  overflow-x: auto;
}

.math-equation {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 1.05em;
  font-weight: 600;
  color: #0f172a;
}

.math-frac {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  vertical-align: middle;
  padding: 0 4px;
}

.math-num {
  border-bottom: 2px solid #334155;
  padding-bottom: 2px;
  text-align: center;
  width: 100%;
}

.math-den {
  padding-top: 2px;
  text-align: center;
  width: 100%;
}

/* Flow Chains */
.flow-chain {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 6px;
  padding: 10px 14px;
  margin: 1.1em 0;
  direction: ltr;
}

.flow-step {
  background-color: #ffffff;
  border: 1px solid #86efac;
  border-radius: 4px;
  padding: 3px 8px;
  font-weight: 600;
  color: #166534;
  font-size: 0.88em;
}

.flow-arrow {
  font-weight: bold;
  color: #15803d;
  font-size: 1em;
}

/* Tables */
.table-wrap {
  width: 100%;
  overflow-x: auto;
  margin: 1.4em 0;
  -webkit-overflow-scrolling: touch;
}

table.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92em;
  direction: rtl;
  margin: 0 auto;
}

table.styled-table th {
  background-color: var(--table-head-bg);
  color: #ffffff;
  padding: 8px 10px;
  text-align: right;
  border: 1px solid #334155;
  font-weight: 700;
  word-break: normal;
}

table.styled-table td {
  padding: 8px 10px;
  border: 1px solid var(--border-light);
  text-align: right;
  vertical-align: top;
  word-break: break-word;
}

table.styled-table tr:nth-child(even) {
  background-color: var(--bg-subtle);
}

hr.chapter-divider {
  border: 0;
  height: 1px;
  background: var(--border-light);
  margin: 1.8em 0;
}

/* Cover Image Page */
.cover-container {
  text-align: center;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.cover-image {
  max-width: 100%;
  max-height: 100%;
  height: auto;
  object-fit: contain;
}

/* Title Page */
.title-page-wrap {
  text-align: center;
  padding: 30px 15px;
  direction: rtl;
}
.title-main {
  font-size: 2em;
  font-weight: 800;
  color: #0f2b48;
  margin-bottom: 10px;
  line-height: 1.35;
}
.title-sub {
  font-size: 1.2em;
  font-weight: 600;
  color: #334155;
  margin-bottom: 20px;
  line-height: 1.4;
}
.title-meta-box {
  background-color: var(--bg-subtle);
  border: 1px solid var(--border-light);
  border-radius: 6px;
  padding: 14px 18px;
  display: inline-block;
  margin-top: 25px;
  text-align: right;
  font-size: 0.92em;
  color: var(--text-muted);
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-main: #121212;
    --text-main: #e2e8f0;
    --text-muted: #94a3b8;
    --bg-subtle: #1e293b;
    --border-light: #334155;
    --border-strong: #64748b;
    --table-head-bg: #0f172a;
    --primary-color: #60a5fa;
    --secondary-color: #2dd4bf;
  }
  body {
    background-color: #121212;
    color: #e2e8f0;
  }
  h1.part-header { color: #93c5fd; border-bottom-color: #3b82f6; }
  h2.chapter-header { color: #60a5fa; border-right-color: #2dd4bf; }
  h3.section-header { color: #2dd4bf; }
  h4.sub-header { color: #cbd5e1; }
  strong { color: #f8fafc; }
  code { background-color: #1e293b; color: #38bdf8; }
  .quote-card { background-color: #1e293b; color: #cbd5e1; border-right-color: #3b82f6; }
  .model-answer-card { background-color: #064e3b; color: #ecfdf5; border-right-color: #10b981; }
  .exam-tip-card { background-color: #1e3a5f; color: #dbeafe; border-right-color: #3b82f6; }
  .warning-card { background-color: #450a0a; color: #fee2e2; border-right-color: #ef4444; }
  .math-card { background: #1e293b; border-color: #334155; border-top-color: #0284c7; }
  .math-equation { color: #f8fafc; }
  .math-num { border-bottom-color: #94a3b8; }
  .math-left, .math-right { color: #f8fafc; }
  .flow-chain { background-color: #064e3b; border-color: #047857; }
  .flow-step { background-color: #065f46; color: #ecfdf5; border-color: #10b981; }
  .title-meta-box { background-color: #1e293b; border-color: #334155; color: #94a3b8; }
}
"""

def parse_balanced_braces(s, start_idx):
    if start_idx >= len(s) or s[start_idx] != '{':
        return "", start_idx
    depth = 1
    i = start_idx + 1
    content = []
    while i < len(s) and depth > 0:
        ch = s[i]
        if ch == '{':
            depth += 1
            content.append(ch)
        elif ch == '}':
            depth -= 1
            if depth > 0:
                content.append(ch)
        else:
            content.append(ch)
        i += 1
    return "".join(content), i

def strip_latex_to_text(s):
    res = []
    i = 0
    while i < len(s):
        if s[i:i+8] == r'\mathbf{':
            inner, next_i = parse_balanced_braces(s, i+7)
            res.append(strip_latex_to_text(inner))
            i = next_i
        elif s[i:i+6] == r'\text{':
            inner, next_i = parse_balanced_braces(s, i+5)
            res.append(strip_latex_to_text(inner))
            i = next_i
        elif s[i:i+2] == r'\ ':
            res.append(' ')
            i += 2
        elif s[i:i+2] == r'\%':
            res.append('%')
            i += 2
        elif s[i:i+6] == r'\times':
            res.append(' × ')
            i += 6
        elif s[i:i+11] == r'\rightarrow':
            res.append(' → ')
            i += 11
        elif s[i:i+6] == r'\approx':
            res.append(' ≈ ')
            i += 6
        elif s[i:i+4] == r'\sum':
            res.append(' ∑ ')
            i += 4
        elif s[i:i+6] == r'\frac{':
            num_inner, after_num = parse_balanced_braces(s, i+5)
            if after_num < len(s) and s[after_num] == '{':
                den_inner, after_den = parse_balanced_braces(s, after_num)
                num = strip_latex_to_text(num_inner).strip()
                den = strip_latex_to_text(den_inner).strip()
                res.append(f"({num} / {den})")
                i = after_den
            else:
                res.append(s[i])
                i += 1
        elif s[i] == '\\' and i+1 < len(s) and s[i+1].isalpha():
            cmd_match = re.match(r'\\([a-zA-Z]+)', s[i:])
            if cmd_match:
                cmd = cmd_match.group(1)
                i += len(cmd) + 1
            else:
                res.append(s[i])
                i += 1
        else:
            res.append(s[i])
            i += 1
    return "".join(res)

def format_math_display(raw):
    raw = raw.strip()
    idx_frac = raw.find(r'\frac{')
    if idx_frac != -1:
        before = strip_latex_to_text(raw[:idx_frac]).strip()
        num_raw, idx_after_num = parse_balanced_braces(raw, idx_frac + 5)
        if idx_after_num < len(raw) and raw[idx_after_num] == '{':
            den_raw, idx_after_den = parse_balanced_braces(raw, idx_after_num)
            after = strip_latex_to_text(raw[idx_after_den:]).strip()
            num = strip_latex_to_text(num_raw).strip()
            den = strip_latex_to_text(den_raw).strip()
            return f'''<div class="math-card">
  <div class="math-equation">
    <span class="math-left">{html.escape(before)}</span>
    <span class="math-frac">
      <span class="math-num">{html.escape(num)}</span>
      <span class="math-den">{html.escape(den)}</span>
    </span>
    <span class="math-right">{html.escape(after)}</span>
  </div>
</div>'''

    clean = strip_latex_to_text(raw).strip()
    if '→' in clean or '->' in clean:
        tokens = [t.strip() for t in re.split(r'→|->', clean) if t.strip()]
        steps_html = []
        for t in tokens:
            steps_html.append(f'<span class="flow-step">{html.escape(t)}</span>')
        return '<div class="flow-chain">' + '<span class="flow-arrow"> → </span>'.join(steps_html) + '</div>'
    
    return f'<div class="math-card"><div class="math-equation">{html.escape(clean)}</div></div>'

def process_inline_markdown(line):
    # 1. Protect <br> / <br/> before HTML escaping
    line = re.sub(r'<br\s*/?>', '___BR_TOKEN___', line, flags=re.IGNORECASE)
    
    # 2. Extract math tokens ($$ first, then $)
    math_tokens = []
    def stash_math(m):
        raw = m.group(1)
        clean = strip_latex_to_text(raw).strip()
        token_html = f'<span class="inline-math">{html.escape(clean)}</span>'
        math_tokens.append(token_html)
        return f"___MATH_TOKEN_{len(math_tokens)-1}___"
    
    line = re.sub(r'\$\$(.*?)\$\$', stash_math, line)
    line = re.sub(r'\$(.*?)\$', stash_math, line)
    
    # 3. Escape HTML
    line = html.escape(line)
    
    # 4. Restore styling tokens
    line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
    line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
    line = re.sub(r'`(.*?)`', r'<code>\1</code>', line)
    
    # 5. Restore <br/>
    line = line.replace('___BR_TOKEN___', '<br/>')
    
    # 6. Restore math tokens
    for idx, token in enumerate(math_tokens):
        line = line.replace(f"___MATH_TOKEN_{idx}___", token)
        
    return line

def convert_section_to_valid_xhtml(md_text, section_title):
    lines = md_text.split('\n')
    output = []
    
    in_code = False
    code_lines = []
    table_lines = []
    quote_lines = []
    in_ul = False
    in_ol = False
    
    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            output.append('</ul>')
            in_ul = False
        if in_ol:
            output.append('</ol>')
            in_ol = False

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].rstrip('\r\n')
        stripped = line.strip()
        
        # Code block
        if stripped.startswith('```'):
            close_lists()
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                block_content = html.escape("\n".join(code_lines))
                output.append(f'<div class="diagram-box"><pre><code>{block_content}</code></pre></div>')
                code_lines = []
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Table block
        if stripped.startswith('|') and stripped.endswith('|'):
            close_lists()
            table_lines.append(stripped)
            i += 1
            continue
        else:
            if table_lines:
                rows = [r.strip().strip('|') for r in table_lines if r.strip().strip('|')]
                t_html = ['<div class="table-wrap"><table class="styled-table">']
                header_done = False
                for r in rows:
                    if re.match(r'^[\s\-\:\.\=\|]+$', r):
                        continue
                    cols = [c.strip() for c in r.split('|')]
                    if not header_done:
                        t_html.append('<thead><tr>')
                        for c in cols:
                            t_html.append(f'<th>{process_inline_markdown(c)}</th>')
                        t_html.append('</tr></thead><tbody>')
                        header_done = True
                    else:
                        t_html.append('<tr>')
                        for c in cols:
                            t_html.append(f'<td>{process_inline_markdown(c)}</td>')
                        t_html.append('</tr>')
                if header_done:
                    t_html.append('</tbody>')
                t_html.append('</table></div>')
                output.append('\n'.join(t_html))
                table_lines = []

        # Blockquote
        if stripped.startswith('>'):
            close_lists()
            quote_lines.append(stripped.lstrip('>').strip())
            i += 1
            continue
        else:
            if quote_lines:
                q_body = '<br/>'.join([process_inline_markdown(q) for q in quote_lines])
                output.append(f'<div class="quote-card">{q_body}</div>')
                quote_lines = []

        if not stripped:
            i += 1
            continue

        # Display math $$ ... $$
        if stripped.startswith('$$') and stripped.endswith('$$') and len(stripped) > 4:
            close_lists()
            output.append(format_math_display(stripped[2:-2]))
            i += 1
            continue

        # Headings
        if stripped.startswith('# '):
            close_lists()
            text = process_inline_markdown(stripped[2:].strip())
            output.append(f'<h1 class="part-header">{text}</h1>')
        elif stripped.startswith('## '):
            close_lists()
            text = process_inline_markdown(stripped[3:].strip())
            output.append(f'<h2 class="chapter-header">{text}</h2>')
        elif stripped.startswith('### '):
            close_lists()
            text = process_inline_markdown(stripped[4:].strip())
            output.append(f'<h3 class="section-header">{text}</h3>')
        elif stripped.startswith('#### '):
            close_lists()
            text = process_inline_markdown(stripped[5:].strip())
            output.append(f'<h4 class="sub-header">{text}</h4>')
        # Lists
        elif stripped.startswith('* ') or stripped.startswith('- '):
            item_text = process_inline_markdown(stripped[2:].strip())
            if 'پاسخ مدل' in item_text or 'Model Answer' in item_text or 'کلید پاسخ' in item_text:
                close_lists()
                output.append(f'<div class="model-answer-card">{item_text}</div>')
            elif 'نکته آزمون' in item_text or 'Exam Point' in item_text or 'نکته کلیدی' in item_text:
                close_lists()
                output.append(f'<div class="exam-tip-card">{item_text}</div>')
            elif 'هشدار' in item_text or 'Warning' in item_text or 'خط قرمز' in item_text:
                close_lists()
                output.append(f'<div class="warning-card">{item_text}</div>')
            else:
                if in_ol:
                    output.append('</ol>')
                    in_ol = False
                if not in_ul:
                    output.append('<ul class="bullet-list">')
                    in_ul = True
                output.append(f'  <li class="bullet-item">{item_text}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            item_text = process_inline_markdown(re.sub(r'^\d+\.\s*', '', stripped))
            if in_ul:
                output.append('</ul>')
                in_ul = False
            if not in_ol:
                output.append('<ol class="numbered-list">')
                in_ol = True
            output.append(f'  <li class="numbered-item">{item_text}</li>')
        elif stripped.startswith('---'):
            close_lists()
            output.append('<hr class="chapter-divider"/>')
        else:
            close_lists()
            p_text = process_inline_markdown(stripped)
            output.append(f'<p class="para">{p_text}</p>')
            
        i += 1

    close_lists()
    if table_lines:
        rows = [r.strip().strip('|') for r in table_lines if r.strip().strip('|')]
        t_html = ['<div class="table-wrap"><table class="styled-table">']
        header_done = False
        for r in rows:
            if re.match(r'^[\s\-\:\.\=\|]+$', r):
                continue
            cols = [c.strip() for c in r.split('|')]
            if not header_done:
                t_html.append('<thead><tr>')
                for c in cols:
                    t_html.append(f'<th>{process_inline_markdown(c)}</th>')
                t_html.append('</tr></thead><tbody>')
                header_done = True
            else:
                t_html.append('<tr>')
                for c in cols:
                    t_html.append(f'<td>{process_inline_markdown(c)}</td>')
                t_html.append('</tr>')
        if header_done:
            t_html.append('</tbody>')
        t_html.append('</table></div>')
        output.append('\n'.join(t_html))

    if quote_lines:
        q_body = '<br/>'.join([process_inline_markdown(q) for q in quote_lines])
        output.append(f'<div class="quote-card">{q_body}</div>')

    body = '\n'.join(output)
    
    full_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="fa" xml:lang="fa" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{html.escape(section_title)}</title>
  <link rel="stylesheet" type="text/css" href="style/book.css"/>
</head>
<body>
{body}
</body>
</html>"""
    return full_xhtml

def build_epub(book_id, title, subtitle, author, cover_png, manuscript_path, output_epub_path):
    print(f"--- Building EPUB: {output_epub_path} ---")
    
    with open(manuscript_path, 'r', encoding='utf-8') as f:
        full_content = f.read()

    # Strip YAML front matter if present
    if full_content.strip().startswith('---'):
        parts = full_content.strip().split('---', 2)
        if len(parts) >= 3:
            full_content = parts[2].strip()

    # Split into parts
    raw_parts = re.split(r'\n# ', full_content)
    
    chapters = []
    first_block = raw_parts[0].strip()
    first_title = first_block.split('\n')[0].replace('#', '').strip()
    if not first_title:
        first_title = "مقدمه و راهنما"
    chapters.append(('how_to_use', first_title, first_block))
    
    for idx, part_text in enumerate(raw_parts[1:], 1):
        lines = part_text.strip().split('\n')
        part_title = lines[0].strip()
        file_id = f"part_{idx:02d}"
        part_full = f"# {part_text}"
        chapters.append((file_id, part_title, part_full))

    print(f"Total parts to compile: {len(chapters)}")

    os.makedirs(os.path.dirname(output_epub_path), exist_ok=True)
    with zipfile.ZipFile(output_epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 1. mimetype (MUST be first and uncompressed)
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)

        # 2. META-INF/container.xml
        container_xml = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
        zf.writestr("META-INF/container.xml", container_xml)

        # 3. EPUB/style/book.css
        zf.writestr("EPUB/style/book.css", CSS_STYLES)

        # 4. EPUB/images/cover.png
        if os.path.exists(cover_png):
            with open(cover_png, "rb") as cf:
                zf.writestr("EPUB/images/cover.png", cf.read())
        else:
            print(f"Warning: Cover {cover_png} not found.")

        # 5. EPUB/cover.xhtml
        cover_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="fa" xml:lang="fa" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Cover</title>
  <link rel="stylesheet" type="text/css" href="style/book.css"/>
</head>
<body style="margin:0; padding:0; text-align:center;">
  <div class="cover-container">
    <img src="images/cover.png" alt="{html.escape(title)}" class="cover-image"/>
  </div>
</body>
</html>"""
        zf.writestr("EPUB/cover.xhtml", cover_xhtml)

        # 6. EPUB/title.xhtml
        title_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="fa" xml:lang="fa" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="style/book.css"/>
</head>
<body>
  <div class="title-page-wrap">
    <h1 class="title-main">{html.escape(title)}</h1>
    <h2 class="title-sub">{html.escape(subtitle)}</h2>
    <hr class="chapter-divider"/>
    <div class="title-meta-box">
      <p><strong>مرجع تدوین:</strong> {html.escape(author)}</p>
      <p><strong>حوزه عملیاتی:</strong> افغانستان — ولایت دایکندی</p>
      <p><strong>چارچوب‌های تخنیکی:</strong> MoPH / BPHS / EPHS / DHIS2 / WHO</p>
      <p><strong>تاریخ انتشار:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
      <p><strong>قالب:</strong> کتاب الکترونیک استاندارد (EPUB3 Publication)</p>
    </div>
  </div>
</body>
</html>"""
        zf.writestr("EPUB/title.xhtml", title_xhtml)

        # 7. Convert and write each chapter XHTML
        for file_id, p_title, p_md in chapters:
            xhtml_content = convert_section_to_valid_xhtml(p_md, p_title)
            try:
                ET.fromstring(xhtml_content)
            except ET.ParseError as e:
                print(f"Error in {file_id}: {e}")
                raise e
            zf.writestr(f"EPUB/{file_id}.xhtml", xhtml_content)

        # 8. EPUB/nav.xhtml (EPUB3 Navigation Document)
        nav_items = [
            '      <li><a href="cover.xhtml">جلد کتاب</a></li>',
            '      <li><a href="title.xhtml">صفحه شناسنامه و عنوان</a></li>'
        ]
        for file_id, p_title, _ in chapters:
            nav_items.append(f'      <li><a href="{file_id}.xhtml">{html.escape(p_title)}</a></li>')

        nav_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="fa" xml:lang="fa" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>فهرست مندرجات</title>
  <link rel="stylesheet" type="text/css" href="style/book.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1 class="part-header">فهرست مندرجات کتاب</h1>
    <ol class="numbered-list">
{chr(10).join(nav_items)}
    </ol>
  </nav>
  <nav epub:type="landmarks" hidden="">
    <h2>نقاط راهنما</h2>
    <ol>
      <li><a epub:type="cover" href="cover.xhtml">جلد کتاب</a></li>
      <li><a epub:type="toc" href="nav.xhtml">فهرست</a></li>
      <li><a epub:type="bodymatter" href="how_to_use.xhtml">شروع متن</a></li>
    </ol>
  </nav>
</body>
</html>"""
        zf.writestr("EPUB/nav.xhtml", nav_xhtml)

        # 9. EPUB/toc.ncx (EPUB2 backwards-compatibility NCX)
        ncx_points = [
            '    <navPoint id="np-cover" playOrder="1"><navLabel><text>جلد کتاب</text></navLabel><content src="cover.xhtml"/></navPoint>',
            '    <navPoint id="np-title" playOrder="2"><navLabel><text>شناسنامه کتاب</text></navLabel><content src="title.xhtml"/></navPoint>'
        ]
        po = 3
        for file_id, p_title, _ in chapters:
            ncx_points.append(f'    <navPoint id="np-{file_id}" playOrder="{po}"><navLabel><text>{html.escape(p_title)}</text></navLabel><content src="{file_id}.xhtml"/></navPoint>')
            po += 1

        toc_ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:{book_id}"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{html.escape(title)}</text>
  </docTitle>
  <navMap>
{chr(10).join(ncx_points)}
  </navMap>
</ncx>"""
        zf.writestr("EPUB/toc.ncx", toc_ncx)

        # 10. EPUB/content.opf (OPF Manifest & Spine)
        manifest_items = [
            '    <item id="cover-image" href="images/cover.png" media-type="image/png" properties="cover-image"/>',
            '    <item id="style" href="style/book.css" media-type="text/css"/>',
            '    <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>',
            '    <item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>',
            '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
            '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>'
        ]
        spine_items = [
            '    <itemref idref="cover"/>',
            '    <itemref idref="title"/>',
            '    <itemref idref="nav"/>'
        ]

        for file_id, _, _ in chapters:
            manifest_items.append(f'    <item id="{file_id}" href="{file_id}.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append(f'    <itemref idref="{file_id}"/>')

        content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="fa" dir="rtl">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">urn:uuid:{book_id}</dc:identifier>
    <dc:title>{html.escape(title)}</dc:title>
    <dc:creator>{html.escape(author)}</dc:creator>
    <dc:language>fa-AF</dc:language>
    <dc:date>{datetime.now().strftime('%Y-%m-%d')}</dc:date>
    <dc:publisher>مؤسسه شهدا — عملیات ساحوی دایکندی</dc:publisher>
    <dc:description>{html.escape(subtitle)}</dc:description>
    <meta property="dcterms:modified">{datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>
  </metadata>
  <manifest>
{chr(10).join(manifest_items)}
  </manifest>
  <spine toc="ncx">
{chr(10).join(spine_items)}
  </spine>
</package>"""
        zf.writestr("EPUB/content.opf", content_opf)

    print(f"Successfully generated: {output_epub_path} ({os.path.getsize(output_epub_path):,} bytes)")

if __name__ == "__main__":
    build_epub(
        book_id="shuhada-pc-daikundi-exam-2026-v1",
        title="هماهنگ‌کننده ولایتی — راهنمای جامع مدیریت ساحوی، رهبری عملیات و آمادگی آزمون",
        subtitle="راهنمای کاربردی عملیات کلینیکی، نظارت حمایوی و شبیه‌ساز آزمون استخدامی",
        author="مؤسسه شهدا — بست هماهنگ‌کننده ولایتی دایکندی",
        cover_png="build/cover_book1.png",
        manuscript_path="manuscript/master.md",
        output_epub_path="build/Provincial_Coordinator_24Hour_Exam_Master_Guide.epub"
    )

    build_epub(
        book_id="shuhada-hm-field-master-2026-v2",
        title="مدیریت صحت — راهنمای جامع یادگیری مسلکی و پرکتیک ساحوی",
        subtitle="مدیریت مراکز صحی، زنجیره تأمین ادویه، HMIS، منابع بشری و فورمول‌های اپیدمیولوژی",
        author="مؤسسه شهدا — مدیریت عملیات ساحوی صحت عامه",
        cover_png="build/cover_book2.png",
        manuscript_path="manuscript/health_management_master.md",
        output_epub_path="build/Health_Management_Master_Guide.epub"
    )
