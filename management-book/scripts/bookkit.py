#!/usr/bin/env python3
"""
bookkit - text shaping and layout kit used for the cover, the diagrams and the
page proofs.

HarfBuzz does the shaping (Arabic letter-joining, Latin kerning), FreeType
rasterises each glyph with real anti-aliasing, Pillow is the canvas. The small
bidi model is sufficient for this book's text pattern: Dari paragraphs that
embed Latin words, figures and parenthesised English terms.
"""
from __future__ import annotations

import re
from pathlib import Path

import freetype
import uharfbuzz as hb
from PIL import Image, ImageDraw

FONTS = Path(__file__).resolve().parents[1] / 'assets' / 'fonts'
BODY_TTF = FONTS / 'Vazir.ttf'
DISPLAY_TTF = FONTS / 'Samim.ttf'
SYMBOL_TTF = FONTS / 'BookSymbols.ttf'

AR = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')
LAT = re.compile(r'[A-Za-z0-9]')

_cache: dict = {}
_faces: dict = {}


# ------------------------------------------------------------------- fonts ----

class FaceFont:
    def __init__(self, path: Path, size: float, embolden: bool = False):
        self.path = str(path)
        self.size = float(size)
        self.embolden = embolden
        self.ft = freetype.Face(self.path)
        self.ft.set_char_size(int(round(self.size * 64)))
        self.hb = hb.Font(hb.Face(Path(self.path).read_bytes()))
        self.upem = self.hb.face.upem
        self.hb.scale = (self.upem, self.upem)
        self.ascender = self.ft.size.ascender / 64.0
        self.descender = self.ft.size.descender / 64.0
        self.line_height = self.ft.size.height / 64.0
        self.cmap = {c[0] if isinstance(c, tuple) else c
                      for c in self.ft.get_chars()}
        self.space = self.advance(' ')

    def advance(self, text: str) -> float:
        return sum(adv for _, adv, _, _ in shape(text, self, 'ltr')) * self.size / self.upem

    def has(self, ch: str) -> bool:
        return ord(ch) in self.cmap

    def tile(self, gid: int, colour):
        """RGBA tile of one glyph, cached per (font, size, gid, colour)."""
        key = (self.path, self.size, self.embolden, gid, colour)
        hit = _cache.get(key)
        if hit is not None:
            return hit
        flags = (freetype.FT_LOAD_DEFAULT | freetype.FT_LOAD_RENDER
                 | freetype.FT_LOAD_TARGET_NORMAL)
        if self.embolden and hasattr(freetype, 'FT_LOAD_EMBOLDEN'):
            flags |= freetype.FT_LOAD_EMBOLDEN
        self.ft.load_glyph(gid, flags)
        g = self.ft.glyph
        bm = g.bitmap
        w, h, pitch = bm.width, bm.rows, bm.pitch
        out = (None, 0, 0)
        if w and h:
            raw = bytes(bm.buffer)
            if bm.pixel_mode == freetype.FT_PIXEL_MODE_MONO:
                data = bytearray(w * h)
                for y in range(h):
                    row = raw[y * abs(pitch):y * abs(pitch) + (w + 7) // 8]
                    for x in range(w):
                        if (row[x // 8] >> (7 - (x % 8))) & 1:
                            data[y * w + x] = 255
                mask = Image.frombytes('L', (w, h), bytes(data))
            else:
                step = abs(pitch)
                mask = Image.frombytes('L', (w, h),
                                       b''.join(raw[y * step:y * step + w] for y in range(h)))
            tile = Image.new('RGBA', (w, h), colour)
            tile.putalpha(mask)
            out = (tile, g.bitmap_left, g.bitmap_top)
        _cache[key] = out
        return out


def font(size: float, kind: str = 'body', bold: bool = False):
    path = {'body': BODY_TTF, 'display': DISPLAY_TTF, 'symbol': SYMBOL_TTF}[kind]
    embolden = bool(bold) and kind == 'body'
    key = (str(path), round(size, 2), embolden)
    if key not in _faces:
        _faces[key] = FaceFont(path, size, embolden)
    return _faces[key]


# ------------------------------------------------------------------ shaping ---

def shape(text: str, f: FaceFont, direction: str = 'ltr'):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = direction
    buf.guess_segment_properties()
    buf.direction = direction
    hb.shape(f.hb, buf, {'kern': True, 'liga': True})
    return [(i.codepoint, p.x_advance, p.x_offset, p.y_offset)
            for i, p in zip(buf.glyph_infos, buf.glyph_positions)]


OPENERS = '([{\u00ab\u2039'


def segments(text: str):
    out = []
    for i, ch in enumerate(text):
        kind = 'ar' if AR.match(ch) else ('lat' if LAT.match(ch) else 'neutral')
        if ch in OPENERS and out:
            # an opening bracket binds to what follows it, the way a bidi
            # renderer keeps "(Manager)" visually intact inside Dari text
            nxt = text[i + 1] if i + 1 < len(text) else ''
            nxt_kind = 'ar' if AR.match(nxt) else ('lat' if LAT.match(nxt) else 'neutral')
            if nxt_kind in ('ar', 'lat') and out[-1][0] != nxt_kind:
                out.append([nxt_kind, ch])
                continue
        if out and (out[-1][0] == kind or kind == 'neutral'):
            out[-1][1] += ch
        elif out and out[-1][0] == 'neutral':
            out[-1][0] = kind
            out[-1][1] += ch
        else:
            out.append([kind, ch])
    for i in range(1, len(out) - 1):
        if out[i][0] == 'neutral' and out[i - 1][0] == 'lat' and out[i + 1][0] == 'lat':
            out[i][0] = 'lat'
    return [tuple(x) for x in out]


def pick(size: float, ch: str, primary: FaceFont):
    """Fall back to the symbol face when the text face has no glyph, scaled a
    little larger so arrows and ticks match the visual weight of Dari letters."""
    if primary.has(ch) or not SYMBOL_TTF.exists():
        return primary
    sym = font(size * 1.16, 'symbol')
    return sym if sym.has(ch) else primary


def runs(text: str, base: str, primary: FaceFont):
    """Visual left-to-right runs: [(font, text, harfbuzz_direction)]."""
    items = []
    for kind, chunk in segments(text):
        direction = 'ltr' if kind == 'lat' else ('rtl' if base == 'rtl' else 'ltr')
        cur_font, cur = None, ''
        for ch in chunk:
            f = pick(primary.size, ch, primary)
            if cur_font is not None and f is cur_font:
                cur += ch
            else:
                if cur:
                    items.append((cur_font, cur, direction))
                cur_font, cur = f, ch
        if cur:
            items.append((cur_font, cur, direction))
    return list(reversed(items)) if base == 'rtl' else items


def measure(text: str, base: str, primary: FaceFont) -> float:
    total = 0.0
    for f, chunk, direction in runs(text, base, primary):
        total += sum(adv for _, adv, _, _ in shape(chunk, f, direction)) * f.size / f.upem
    return total


# ------------------------------------------------------------------ drawing ---

def draw_line(img: Image.Image, x: float, baseline: float, text: str,
              primary: FaceFont, colour, base: str = 'rtl',
              letter_space: float = 0.0) -> float:
    """Draw one line. For base='rtl' the line ends at x (x = right edge)."""
    width = measure(text, base, primary)
    pen = x if base == 'rtl' else x
    if base == 'rtl':
        pen = x - width
    for f, chunk, direction in runs(text, base, primary):
        for gid, adv, xo, yo in shape(chunk, f, direction):
            px_adv = adv * f.size / f.upem
            tile, left, top = f.tile(gid, colour)
            if tile is not None:
                gx = pen + xo * f.size / f.upem
                gy = baseline - top - yo * f.size / f.upem
                img.paste(tile, (int(round(gx + left)), int(round(gy))), tile)
            pen += px_adv + letter_space
    return width


def draw_block(img, x_right, y_top, width, text, primary, colour, base='rtl',
               align='justify', line_height=None, first_line_indent=0.0):
    """Wrapped paragraph. Returns the y after the paragraph."""
    lh = line_height or primary.line_height * 1.62
    lines = wrap(text, primary, width - first_line_indent, base)
    baseline = y_top + primary.ascender * 1.06
    for i, line in enumerate(lines):
        words = line.split(' ')
        line_w = measure(line, base, primary)
        right = x_right
        if i == 0 and first_line_indent:
            right -= first_line_indent
        if align == 'justify' and i < len(lines) - 1 and len(words) > 1:
            space = primary.space
            extra = (width - line_w) / (len(words) - 1)
            pen = right
            for w in words:
                ww = measure(w, base, primary)
                draw_line(img, pen, baseline, w, primary, colour, base)
                pen -= ww + space + extra
        elif align == 'center':
            draw_line(img, right - (width - line_w) / 2, baseline, line, primary, colour, base)
        elif align == 'left':
            draw_line(img, right - width + line_w, baseline, line, primary, colour, base)
        else:
            draw_line(img, right, baseline, line, primary, colour, base)
        baseline += lh
    return y_top + lh * len(lines)


def wrap(text: str, primary: FaceFont, max_width: float, base: str = 'rtl'):
    lines, cur = [], ''
    for w in text.split(' '):
        trial = (cur + ' ' + w) if cur else w
        if not cur or measure(trial, base, primary) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_flow(img, x_right, y_top, width, steps, primary, colour):
    text = ('  \u2192  ').join(steps)
    f = font(primary.size * 0.9, 'body')
    baseline = y_top + f.ascender * 1.15
    for ln in wrap(text, f, width, 'rtl'):
        w = measure(ln, 'rtl', f)
        draw_line(img, x_right - (width - w) / 2 + w, baseline, ln, f, colour, 'rtl')
        baseline += f.line_height * 1.55
    return baseline - f.line_height * 1.55 + 4


def row_height(row, primary, width, base='rtl', ncols=None):
    """Estimated height of one table row, using the table's own cell sizing."""
    cell_font = font(max(9.5, primary.size * 0.86), 'body')
    ncols = ncols or len(row)
    col = width / max(ncols, 1)
    lines = max(len(wrap(cell, cell_font, col - 16, base)) for cell in row)
    return lines * cell_font.line_height * 1.45 + 12


def table(img, x_right, y_top, width, rows, primary, colours, base='rtl'):
    """Render a table; returns the y after it."""
    if not rows:
        return y_top
    ncols = max(len(r) for r in rows)
    rows = [r + [''] * (ncols - len(r)) for r in rows]
    cell_font = font(max(9.5, primary.size * 0.86), 'body')
    pad = 8.0
    natural = []
    for c in range(ncols):
        w = max(measure(r[c], base, cell_font) for r in rows)
        natural.append(min(max(w + 2 * pad, 60), width * 0.6))
    total = sum(natural)
    scale = width / total if total > width else 1.0
    widths = [w * scale for w in natural]
    # wrap each cell
    lines = [[wrap(row[c], cell_font, widths[c] - 2 * pad, base) for c in range(ncols)]
             for row in rows]
    row_h = [max(len(lines[r][c]) for c in range(ncols)) * cell_font.line_height * 1.45 + 12
             for r in range(len(rows))]
    draw = ImageDraw.Draw(img)
    y = y_top
    x_left = x_right - width
    for r, row in enumerate(rows):
        h = row_h[r]
        if r == 0:
            draw.rectangle([x_left, y, x_right, y + h], fill=colours['table_head'])
        elif r % 2 == 0:
            draw.rectangle([x_left, y, x_right, y + h], fill=colours['table_alt'])
        draw.line([x_left, y, x_right, y], fill=colours['rule'], width=1)
        x = x_right
        for c in range(ncols):
            cw = widths[c]
            draw.line([x - cw, y, x - cw, y + h], fill=colours['rule'], width=1)
            ty = y + 7
            for ln in lines[r][c]:
                draw_line(img, x - pad, ty + cell_font.ascender, ln, cell_font,
                          colours['ink'], base)
                ty += cell_font.line_height * 1.45
            x -= cw
        y += h
    draw.line([x_left, y, x_right, y], fill=colours['rule'], width=1)
    return y + 10


def rounded_panel(img, x_right, y_top, width, height, colours, fill, accent,
                  radius=10, accent_side='right'):
    draw = ImageDraw.Draw(img)
    x_left = x_right - width
    draw.rounded_rectangle([x_left, y_top, x_right, y_top + height], radius=radius,
                           fill=fill, outline=colours['rule'], width=1)
    if accent_side == 'right':
        draw.rectangle([x_right - 4, y_top + 1, x_right, y_top + height - 1], fill=accent)
    else:
        draw.rectangle([x_left, y_top + 1, x_left + 4, y_top + height - 1], fill=accent)
