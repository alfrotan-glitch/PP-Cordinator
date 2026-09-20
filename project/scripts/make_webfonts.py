#!/usr/bin/env python3
"""
Phase 5 (web fonts) - the font payload of the EPUB edition.

    Vazir.ttf        -> fonts/Vazir.woff2        body text (regular)
    Samim.ttf        -> fonts/Samim.woff2        headings and bold runs
    DejaVuSans.ttf   -> fonts/BookSymbols.woff2  subset: only the symbols the
                                                 two Dari fonts do not carry
                                                 (check marks, stars, arrows)
    -> fonts/LICENSE-fonts.txt                   licence notices, embedded in
                                                 the EPUB next to the fonts

Vazir and Samim are format-converted only (name tables untouched); their
licence notices are copied verbatim out of the font name tables, and the full
SIL OFL 1.1 text lives in OFL-1.1.txt.

The DejaVu subset *is* a derivative work, so per the Bitstream Vera licence it
is renamed to "BookSymbols" (no "Bitstream"/"Vera" in the name) and keeps the
original copyright/licence fields in its name table.
"""
import shutil
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / 'project/assets/fonts'
MASTER = ROOT / 'project/manuscript/master.md'
DEJAVU = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

# symbols that must survive even if a reading system has no fallback font
EXTRA_SYMBOLS = '↑↓←→✓✗★●◦▪■□◆'


def to_woff2(src: Path, dst: Path) -> None:
    font = TTFont(str(src))
    font.flavor = 'woff2'
    font.save(str(dst))
    print(f'  {src.name:>16} -> {dst.name:<20} {dst.stat().st_size / 1024:6.1f} KB')


def name_field(font: TTFont, name_id: int) -> str:
    for rec in font['name'].names:
        if rec.nameID == name_id:
            try:
                return rec.toUnicode()
            except Exception:                                  # pragma: no cover
                continue
    return ''


def symbol_codepoints() -> list:
    """Codepoints used in the book that neither Dari font can draw."""
    text = MASTER.read_text(encoding='utf-8')
    covered = set()
    for f in ('Vazir.ttf', 'Samim.ttf'):
        font = TTFont(str(FONTS / f))
        for table in font['cmap'].tables:
            covered |= set(table.cmap.keys())
    used = {ord(c) for c in text if c not in '\n\r\t '}
    missing = used - covered
    return sorted(missing | {ord(c) for c in EXTRA_SYMBOLS})


def make_symbols(dst: Path) -> None:
    if not DEJAVU.exists():
        raise SystemExit(f'missing source font: {DEJAVU}')
    options = subset.Options()
    options.layout_features = ['*']
    options.name_IDs = ['*']
    options.name_legacy = True
    options.notdef_outline = True
    options.recalc_bounds = True
    options.drop_tables += ['DSIG']
    font = subset.load_font(str(DEJAVU), options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=symbol_codepoints())
    subsetter.subset(font)

    # rename the derivative (Bitstream Vera licence, clause 2)
    name = font['name']
    for rec in list(name.names):
        if rec.nameID in (1, 4, 16, 17):
            rec.string = 'BookSymbols'
        elif rec.nameID == 3:
            rec.string = 'BookSymbols; subset of DejaVu Sans'
        elif rec.nameID == 6:
            rec.string = 'BookSymbols-Regular'
    font.flavor = 'woff2'
    subset.save_font(font, str(dst), options)
    print(f'  {"DejaVuSans.ttf":>16} -> {dst.name:<20} {dst.stat().st_size / 1024:6.1f} KB')


def write_licence(dst: Path) -> None:
    ofl = (FONTS / 'OFL-1.1.txt').read_text(encoding='utf-8')
    blocks = []
    for f, note in (('Vazir.ttf', 'body text (regular)'),
                    ('Samim.ttf', 'headings and bold runs')):
        font = TTFont(str(FONTS / f))
        blocks.append(
            f'--- {f} ({note}) ---\n'
            f'{name_field(font, 0)}\n\n{name_field(font, 13)}\n'
            f'Licence references:\n{name_field(font, 14)}\n')
    blocks.append(
        '--- DejaVu Sans -> BookSymbols.woff2 (subset, symbol fallback) ---\n'
        'Copyright (c) 2003 by Bitstream, Inc. All Rights Reserved.\n'
        'Bitstream Vera is a trademark of Bitstream, Inc.\n'
        'DejaVu changes are in public domain.\n'
        'The subset embedded in this book is renamed "BookSymbols" and carries\n'
        'only the symbol glyphs (check marks, stars, arrows, bullets) that the\n'
        'Dari text fonts do not contain.\n'
        'Full licence: https://dejavu.sourceforge.net/wiki/index.php/License\n\n'
        'Bitstream Vera Fonts Copyright\n'
        '------------------------------\n'
        'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
        'of the fonts accompanying this license ("Fonts") and associated documentation\n'
        'files (the "Font Software"), to reproduce and distribute the Font Software,\n'
        'including without limitation the rights to use, copy, merge, publish,\n'
        'distribute, and/or sell copies of the Font Software, and to permit persons to\n'
        'whom the Font Software is furnished to do so, subject to the following\n'
        'conditions:\n\n'
        'The above copyright and trademark notices and this permission notice shall be\n'
        'included in all copies of one or more of the Font Software typefaces.\n\n'
        'The Font Software may be modified, altered, or added to, and in particular the\n'
        'designs of glyphs or characters in the Fonts may be modified and additional\n'
        'glyphs or characters may be added to the Fonts, only if the fonts are renamed\n'
        'to names not containing either the words "Bitstream" or the word "Vera".\n\n'
        'This License becomes null and void to the extent applicable to Fonts or Font\n'
        'Software that has been modified and is distributed under the "Bitstream Vera"\n'
        'names.\n\n'
        'The Font Software may be sold as part of a larger software package but no copy\n'
        'of one or more of the Font Software typefaces may be sold by itself.\n\n'
        'THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
        'IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF MERCHANTABILITY,\n'
        'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF COPYRIGHT, PATENT,\n'
        'TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL BITSTREAM OR THE GNOME FOUNDATION\n'
        'BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, INCLUDING ANY GENERAL,\n'
        'SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, WHETHER IN AN ACTION\n'
        'OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF THE USE OR INABILITY TO\n'
        'USE THE FONT SOFTWARE OR FROM OTHER DEALINGS IN THE FONT SOFTWARE.\n\n'
        'Except as contained in this notice, the names of Gnome, the Gnome Foundation,\n'
        'and Bitstream Inc., shall not be used in advertising or otherwise to promote\n'
        'the sale, use or other dealings in this Font Software without prior written\n'
        'authorization from the Gnome Foundation or Bitstream Inc., respectively. For\n'
        'further information, contact: fonts at gnome dot org.\n\n'
        'Roboto / Open Sans (Latin glyphs in Vazir and Samim) are licensed under the\n'
        'Apache License, Version 2.0 - https://www.apache.org/licenses/LICENSE-2.0\n\n'
        + ofl)
    dst.write_text('\n'.join(blocks), encoding='utf-8')
    print(f'  licence notice -> {dst.name} ({dst.stat().st_size / 1024:.1f} KB)')


def main() -> None:
    print('web fonts:')
    to_woff2(FONTS / 'Vazir.ttf', FONTS / 'Vazir.woff2')
    to_woff2(FONTS / 'Samim.ttf', FONTS / 'Samim.woff2')
    make_symbols(FONTS / 'BookSymbols.woff2')
    write_licence(FONTS / 'LICENSE-fonts.txt')


if __name__ == '__main__':
    main()
