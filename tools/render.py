"""Ve anh chu nen mau 1080x1350 (doc 4:5, chuan bai dang Facebook) cho Fanpage.
Dung: python3 tools/render.py "Noi dung" "#1E88E5" "#1565C0" 2026-10/20261021-1200.png
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "BeVietnamPro-Bold.ttf")

def _wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def render(text, c1, c2, out, w=1080, h=1350, pad=110):
    im = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(im)
    a = tuple(int(c1[i:i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(c2[i:i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3)))
    for fs in range(92, 30, -2):
        f = ImageFont.truetype(FONT, fs)
        lines = _wrap(d, text, f, w - 2 * pad)
        lh = int(fs * 1.35)
        if lh * len(lines) <= h - 2 * pad - 120:
            break
    y = (h - lh * len(lines)) // 2
    for line in lines:
        lw = d.textlength(line, font=f)
        d.text(((w - lw) / 2, y), line, font=f, fill="white")
        y += lh
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    im.save(out, optimize=True)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    render(*sys.argv[1:])
