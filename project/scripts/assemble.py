#!/usr/bin/env python3
"""Assemble the single-source master manuscript from the parts (order matters)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'project/manuscript/parts'
PARTS = ['00_frontmatter.md', '10_body.md', '20_glossary.md', '30_appendices.md',
         '40_backmatter.md']
OUT = ROOT / 'project/manuscript/master.md'

chunks = []
for p in PARTS:
    f = BASE / p
    if not f.exists():
        print('  (missing, skipped):', p)
        continue
    txt = f.read_text(encoding='utf-8')
    txt = re.sub(r'^@@\s*', '', txt, flags=re.M)      # extraction marker cleanup
    chunks.append(txt.strip())

OUT.write_text('\n\n'.join(chunks) + '\n', encoding='utf-8')
body = OUT.read_text(encoding='utf-8')
print(f'master.md -> {len(body)} chars, {len(body.split(chr(10)))} lines')
print('parts:', ', '.join(PARTS))
