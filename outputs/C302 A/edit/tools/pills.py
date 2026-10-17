"""Render caption chunks / overlays as transparent PNGs (rounded pill boxes, soft shadow)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONT = '/usr/share/fonts/truetype/montserrat/Montserrat[wght].ttf'
def font(size, weight='Bold'):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name(weight); return f
def hexrgb(h, a=255):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)
def runs(text):
    """'a *b* c' -> [('a ',False),('b',True),(' c',False)]"""
    out, hl = [], False
    for i, part in enumerate(text.split('*')):
        if part: out.append((part, hl))
        hl = not hl
    return out
def line_width(f, rs, track):
    w = 0
    for s, _ in rs:
        for ch in s: w += f.getlength(ch) + track
    return w - track
def draw_runs(d, x, y, f, rs, track, col, hcol):
    for s, hl in rs:
        for ch in s:
            d.text((x, y), ch, font=f, fill=hcol if hl else col); x += f.getlength(ch) + track
def pill(text, size=60, color='#FFF8EE', hl='#E8B54A', box='#770A08', opacity=0.88,
         padx=28, pady=14, track=1.5, shadow=True, weight='Bold', radius=None):
    f = font(size, weight); rs = runs(text)
    asc, desc = f.getmetrics()
    tw = int(round(line_width(f, rs, track))); th = asc + desc
    bw, bh = tw + 2 * padx, th + 2 * pady - 6
    S = 24  # shadow margin
    im = Image.new('RGBA', (bw + 2 * S, bh + 2 * S), (0, 0, 0, 0))
    r = bh / 2 if radius is None else radius
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((S, S + 4, S + bw, S + 4 + bh), radius=r, fill=(0, 0, 0, 90))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(7)))
    # supersampled box for smooth pill edges
    k = 4; big = Image.new('RGBA', (im.width * k, im.height * k), (0, 0, 0, 0))
    ImageDraw.Draw(big).rounded_rectangle((S * k, S * k, (S + bw) * k, (S + bh) * k), radius=r * k, fill=hexrgb(box, int(255 * opacity)))
    im = Image.alpha_composite(im, big.resize(im.size, Image.LANCZOS))
    d = ImageDraw.Draw(im)
    # vertically centre the cap-height/x-height mass
    bb = f.getbbox('Hg'); ty = S + (bh - (bb[3] - bb[1])) / 2 - bb[1]
    draw_runs(d, S + padx, ty, f, rs, track, hexrgb(color), hexrgb(hl))
    return im
def headline(lines, size=84, color='#FFF8EE', hl='#E8B54A', track=2, weight='ExtraBold'):
    """Big hook / CTA text: bold type with a soft dark glow (no box, no hard stroke)."""
    f = font(size, weight); asc, desc = f.getmetrics(); lh = int(size * 1.12)
    ws = [line_width(f, runs(l), track) for l in lines]
    W, H = int(max(ws)) + 80, lh * len(lines) + 60
    txt = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for i, (l, w) in enumerate(zip(lines, ws)):
        x, y = (W - w) / 2, 30 + i * lh
        draw_runs(ds, x, y + 4, f, runs(l), track, (0, 0, 0, 200), (0, 0, 0, 200))
        draw_runs(d, x, y, f, runs(l), track, hexrgb(color), hexrgb(hl))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    out = Image.alpha_composite(Image.alpha_composite(Image.new('RGBA', (W, H)), sh), sh)
    return Image.alpha_composite(out, txt)
