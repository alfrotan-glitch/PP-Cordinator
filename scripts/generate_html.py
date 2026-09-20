# -*- coding: utf-8 -*-
"""
generate_html.py
Converts manuscript/master.md into a responsive, elegant RTL HTML reader
with dark navy headers, callout styling, and full typography polish.
"""

import re
import html
import os

def markdown_to_html(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    lines = md.split('\n')
    body_html = []
    
    in_code = False
    code_lines = []
    table_lines = []
    quote_lines = []
    in_front_matter = False
    
    def process_inline(text):
        text = html.escape(text)
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        text = re.sub(r'\$\$(.*?)\$\$', r'<span class="math-formula">\1</span>', text)
        return text

    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if i == 0 and stripped == '---':
            in_front_matter = True
            continue
        if in_front_matter:
            if stripped == '---':
                in_front_matter = False
            continue

        if stripped.startswith('```'):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                block_content = html.escape("\n".join(code_lines))
                body_html.append(f'<pre class="code-box"><code>{block_content}</code></pre>')
            continue
            
        if in_code:
            code_lines.append(line)
            continue

        if stripped.startswith('|') and stripped.endswith('|'):
            table_lines.append(stripped)
            continue
        else:
            if table_lines:
                rows = []
                for tline in table_lines:
                    if set(tline.strip()).issubset({'-', '|', ':', ' '}):
                        continue
                    cells = [c.strip() for c in tline.strip('|').split('|')]
                    rows.append(cells)
                if rows:
                    tbl_html = ['<div class="table-container"><table class="data-table">']
                    for r_idx, row in enumerate(rows):
                        tbl_html.append('<tr>')
                        tag = 'th' if r_idx == 0 else 'td'
                        for cell in row:
                            formatted = process_inline(cell).replace('&lt;br&gt;', '<br>')
                            tbl_html.append(f'<{tag}>{formatted}</{tag}>')
                        tbl_html.append('</tr>')
                    tbl_html.append('</table></div>')
                    body_html.append("\n".join(tbl_html))
                table_lines = []

        if stripped.startswith('>'):
            quote_lines.append(stripped.lstrip('>').strip())
            continue
        else:
            if quote_lines:
                q_text = "<br>".join(process_inline(l) for l in quote_lines)
                box_class = "callout-info"
                if "خطر" in q_text or "هشدار" in q_text or "خطوط سرخ" in q_text:
                    box_class = "callout-danger"
                elif "طلایی" in q_text or "Memory Hook" in q_text or "فرمول" in q_text:
                    box_class = "callout-gold"
                elif "پاسخ نمونه" in q_text or "Model Answer" in q_text:
                    box_class = "callout-success"
                body_html.append(f'<div class="callout {box_class}">{q_text}</div>')
                quote_lines = []

        if not stripped:
            continue

        if stripped.startswith('# '):
            body_html.append(f'<h1 class="part-title">{process_inline(stripped[2:])}</h1>')
        elif stripped.startswith('## '):
            body_html.append(f'<h2 class="chapter-title">{process_inline(stripped[3:])}</h2>')
        elif stripped.startswith('### '):
            body_html.append(f'<h3 class="section-title">{process_inline(stripped[4:])}</h3>')
        elif stripped.startswith('#### '):
            body_html.append(f'<h4 class="sub-title">{process_inline(stripped[5:])}</h4>')
        elif stripped.startswith('* ') or stripped.startswith('- '):
            body_html.append(f'<li class="bullet-item">{process_inline(stripped[2:])}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            num = stripped.split('.')[0]
            rest = stripped[len(num)+2:]
            body_html.append(f'<div class="num-item"><span class="num-badge">{num}</span> {process_inline(rest)}</div>')
        elif stripped.startswith('---'):
            body_html.append('<hr class="divider">')
        else:
            body_html.append(f'<p class="body-p">{process_inline(stripped)}</p>')

    if quote_lines:
        q_text = "<br>".join(process_inline(l) for l in quote_lines)
        body_html.append(f'<div class="callout callout-info">{q_text}</div>')

    content_body = "\n".join(body_html)

    full_html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MASTER BLUEPRINT — PROVINCIAL COORDINATOR: 24-HOUR EXAM MASTER GUIDE</title>
    <style>
        :root {
            --primary-navy: #1B365D;
            --accent-blue: #005A9C;
            --dark-text: #222222;
            --bg-light: #F8F9FA;
            --white: #FFFFFF;
            --border-color: #E2E8F0;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: Vazirmatn, "Segoe UI", Tahoma, Arial, sans-serif;
            background-color: var(--bg-light);
            color: var(--dark-text);
            line-height: 1.8;
            direction: rtl;
            text-align: right;
            padding: 20px;
        }
        .container {
            max-width: 960px;
            margin: 0 auto;
            background-color: var(--white);
            padding: 40px 50px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.06);
            border-radius: 8px;
        }
        .part-title {
            color: var(--primary-navy);
            font-size: 26px;
            font-weight: 800;
            border-bottom: 3px solid var(--accent-blue);
            padding-bottom: 10px;
            margin-top: 50px;
            margin-bottom: 25px;
        }
        .chapter-title {
            color: var(--accent-blue);
            font-size: 21px;
            font-weight: 700;
            margin-top: 35px;
            margin-bottom: 18px;
            border-right: 4px solid var(--primary-navy);
            padding-right: 12px;
        }
        .section-title {
            color: #2D3748;
            font-size: 17px;
            font-weight: 700;
            margin-top: 25px;
            margin-bottom: 12px;
        }
        .sub-title {
            color: #4A5568;
            font-size: 15px;
            font-weight: 600;
            margin-top: 18px;
            margin-bottom: 8px;
        }
        .body-p {
            font-size: 15px;
            margin-bottom: 14px;
            color: #2D3748;
        }
        .bullet-item {
            margin-right: 25px;
            margin-bottom: 8px;
            font-size: 15px;
        }
        .num-item {
            margin-bottom: 10px;
            font-size: 15px;
        }
        .num-badge {
            display: inline-block;
            background-color: var(--primary-navy);
            color: white;
            border-radius: 50%;
            width: 22px;
            height: 22px;
            text-align: center;
            font-size: 12px;
            line-height: 22px;
            font-weight: bold;
            margin-left: 6px;
        }
        .callout {
            border-right: 5px solid var(--accent-blue);
            background-color: #F0F4F8;
            padding: 16px 20px;
            margin: 20px 0;
            border-radius: 4px;
            font-size: 14.5px;
        }
        .callout-gold {
            border-right-color: #D4AC0D;
            background-color: #FEF9E7;
        }
        .callout-danger {
            border-right-color: #C0392B;
            background-color: #FDF2E9;
        }
        .callout-success {
            border-right-color: #27AE60;
            background-color: #EAFAF1;
        }
        .math-formula {
            font-family: "Courier New", monospace;
            background-color: #FFF2F2;
            color: #900C3F;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: bold;
        }
        .code-box {
            background-color: #1A202C;
            color: #E2E8F0;
            padding: 16px;
            border-radius: 6px;
            font-family: Consolas, monospace;
            font-size: 13.5px;
            direction: ltr;
            text-align: left;
            overflow-x: auto;
            margin: 18px 0;
        }
        .table-container {
            overflow-x: auto;
            margin: 25px 0;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        .data-table th {
            background-color: var(--primary-navy);
            color: white;
            padding: 10px 14px;
            font-weight: bold;
            text-align: right;
            border: 1px solid var(--primary-navy);
        }
        .data-table td {
            padding: 9px 12px;
            border: 1px solid var(--border-color);
        }
        .data-table tr:nth-child(even) {
            background-color: #F8FAFC;
        }
        .divider {
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 35px 0;
        }
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            body {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Content Body -->
        REPLACE_ME_BODY
    </div>
</body>
</html>
""".replace("REPLACE_ME_BODY", content_body)

    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated HTML reader saved at: {html_path}")
    print(f"File size: {os.path.getsize(html_path):,} bytes")

if __name__ == "__main__":
    markdown_to_html("manuscript/master.md", "build/index.html")
