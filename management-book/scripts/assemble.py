#!/usr/bin/env python3
"""Concatenate the manuscript parts into the single-source master file."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = sorted((ROOT / 'manuscript' / 'parts').glob('*.md'))
MASTER = ROOT / 'manuscript' / 'master.md'


def main():
    chunks = []
    for p in PARTS:
        chunks.append(p.read_text(encoding='utf-8').strip())
    MASTER.write_text('\n\n'.join(chunks) + '\n', encoding='utf-8')
    words = len(MASTER.read_text(encoding='utf-8').split())
    print(f'master.md <- {len(PARTS)} parts, {words:,} words, '
          f'{MASTER.stat().st_size / 1024:.0f} KB')
    for p in PARTS:
        print(f'   {p.name:24} {len(p.read_text(encoding="utf-8").split()):>7,} words')


if __name__ == '__main__':
    main()
