"""Renders the README figures in assets/: cover.png, demo.gif, clicks.png.

usage:
  python tools/record_web.py <file:///.../do_you_love_me/index.html> frames --size 960x640 \
      --steps "wait:1.4;click:#noBtn;wait:0.9;click:#noBtn;wait:0.9;click:#noBtn;wait:0.9;click:#noBtn;wait:1.1;click:#yesBtn;wait:5.2"
  python tools/render_figures.py frames
Inputs: assets/screen-question.png and assets/screen-success.png (2x screenshots of the real page).
Needs Pillow. Fonts (OFL) in tools/fonts/: Fredoka and Nunito. Colours are the page's own CSS variables.
"""
import os, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "tools", "fonts")
OUT = os.path.join(ROOT, "assets")

# style.css :root
PRIMARY, SECONDARY, DARK, LIGHT = "#ff4d6d", "#ff758f", "#590d22", "#fff0f3"
ROSE, ROSE_DK = (255, 179, 193), (255, 143, 163)  # --bg-gradient
GREY_BTN, GREY_TXT, WHITE, MUTED = "#e9ecef", "#495057", "#ffffff", "#9b6b78"

def font(name, size, *axes):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    f.set_variation_by_axes(list(axes))
    return f

DISPLAY = lambda s: font("Fredoka.ttf", s, 650, 100)
ROUND = lambda s: font("Fredoka.ttf", s, 500, 100)
BODY = lambda s: font("Nunito.ttf", s, 500)
BODY_B = lambda s: font("Nunito.ttf", s, 800)

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]

def glow(im, xy, r, rgb, alpha):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=rgb + (alpha,))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(r // 2)))

def shadow(im, box, r, offset=16, blur=26, alpha=60):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(layer).rounded_rectangle([x0, y0 + offset, x1, y1 + offset], r, fill=(89, 13, 34, alpha))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))

def pill(d, xy, text, f, fill, color, pad=(18, 9)):
    x, y = xy
    w = d.textlength(text, font=f)
    h = f.size + 2 * pad[1]
    d.rounded_rectangle([x, y, x + w + 2 * pad[0], y + h], h // 2, fill=fill)
    d.text((x + pad[0], y + pad[1] - 2), text, font=f, fill=color)
    return x + w + 2 * pad[0]

def heart(d, cx, cy, s, fill):
    """A simple heart: two circles and a triangle."""
    r = s * 0.28
    d.ellipse([cx - 2 * r, cy - r, cx, cy + r], fill=fill)
    d.ellipse([cx, cy - r, cx + 2 * r, cy + r], fill=fill)
    d.polygon([(cx - 1.95 * r, cy + 0.25 * r), (cx + 1.95 * r, cy + 0.25 * r), (cx, cy + 2.3 * r)], fill=fill)

def browser(im, box, shot, url="do_you_love_me/index.html"):
    x0, y0, x1, y1 = box
    shadow(im, box, 20)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, 20, fill=WHITE, outline="#f3d3da", width=2)
    bar = 54
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        cx = x0 + 28 + i * 24
        d.ellipse([cx - 7, y0 + bar // 2 - 7, cx + 7, y0 + bar // 2 + 7], fill=c)
    d.rounded_rectangle([x0 + 110, y0 + 12, x1 - 30, y0 + bar - 12], 15, fill=LIGHT)
    d.text((x0 + 130, y0 + 16), url, font=BODY(18), fill=MUTED)
    s = shot.resize((x1 - x0 - 4, y1 - y0 - bar - 2), Image.LANCZOS)
    mask = Image.new("L", s.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, -30, s.width, s.height], 18, fill=255)
    im.paste(s.convert("RGB"), (x0 + 2, y0 + bar), mask)
    return bar

def cover():
    W, H = 1800, 860
    im = Image.new("RGBA", (W, H), LIGHT)
    glow(im, (1450, 140), 430, ROSE, 150)
    glow(im, (950, 860), 380, ROSE_DK, 90)
    d = ImageDraw.Draw(im)
    x, nx = 100, 100
    for t in ["HTML", "CSS", "JavaScript"]:
        nx = pill(d, (nx, 130), t, ROUND(20), WHITE, DARK) + 10
    d.text((x - 4, 196), "Benimle", font=DISPLAY(104), fill=DARK)
    d.text((x - 4, 306), "Çıkar Mısın?", font=DISPLAY(104), fill=PRIMARY)
    d.text((x, 438), "Will you go out with me?", font=ROUND(36), fill=DARK)
    y = 506
    for line in wrap(d, "A tiny web page that asks one question. Every \"Hayır\" makes the No button run "
                        "and the Yes button grow, until there is only one answer left.", BODY(25), 600):
        d.text((x, y), line, font=BODY(25), fill="#7a3b4c"); y += 38
    heart(d, x + 14, y + 52, 40, PRIMARY)
    d.text((x + 44, y + 38), "Hüseyin Baran Işık", font=BODY_B(20), fill=DARK)

    q = Image.open(os.path.join(OUT, "screen-question.png"))  # the whole 960 x 640 viewport, 2x
    browser(im, (840, 100, 1720, 100 + 54 + int(876 * q.height / q.width) + 2), q)
    # floating card: the success screen, over the page's empty left margin
    s = Image.open(os.path.join(OUT, "screen-success.png")).crop((420, 180, 1500, 1110))
    cw = 300
    ch = int(cw * s.height / s.width)
    cx0, cy0 = 760, 470
    shadow(im, (cx0, cy0, cx0 + cw + 24, cy0 + ch + 70), 22, offset=12, blur=20, alpha=80)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([cx0, cy0, cx0 + cw + 24, cy0 + ch + 70], 22, fill=WHITE, outline="#f3d3da", width=2)
    d.text((cx0 + 22, cy0 + 16), "after \"Evet\"", font=ROUND(22), fill=PRIMARY)
    im.paste(s.resize((cw, ch), Image.LANCZOS).convert("RGB"), (cx0 + 12, cy0 + 56))
    return im.convert("RGB")

def caption(d, x, y, fig, title):
    nx = pill(d, (x, y), f"Fig. {fig}", ROUND(18), PRIMARY, WHITE)
    d.text((nx + 16, y + 1), title, font=DISPLAY(28), fill=DARK)

def frames_of(frames_dir):
    files = sorted(f for f in os.listdir(frames_dir) if f.endswith(".png"))
    return [os.path.join(frames_dir, f) for f in files]

def demo(frames_dir):
    files = frames_of(frames_dir)
    fw, fh = 960, 640
    W, H = fw + 140, fh + 54 + 2 + 150
    base = Image.new("RGBA", (W, H), LIGHT)  # flat: gradients band in a GIF palette
    caption(ImageDraw.Draw(base), 70, 36, 2, "Real recording: four times \"Hayır\", then \"Evet\"")
    blank = Image.new("RGB", (fw, fh), LIGHT)
    browser(base, (70, 100, 70 + fw + 4, 100 + 54 + fh + 2), blank)
    base = base.convert("RGB")
    out = []
    for f in files:
        p = base.copy()
        fr = Image.open(f).convert("RGB")
        mask = Image.new("L", fr.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, -30, fw, fh], 18, fill=255)
        p.paste(fr, (72, 154), mask)
        out.append(p.quantize(colors=192, method=Image.Quantize.FASTOCTREE))
    out[0].save(os.path.join(OUT, "demo.gif"), save_all=True, append_images=out[1:] + [out[-1]] * 10,
                duration=100, loop=0, optimize=True)

def clicks(frames_dir):
    """Fig. 3: real frames after each "Hayır" click, then the loader and the answer."""
    files = frames_of(frames_dir)
    # find each click: the first frame of a burst of change; the frame before it shows the settled state
    small = [Image.open(f).convert("L").resize((96, 64)) for f in files]
    diff = [0.0] + [ImageStat.Stat(ImageChops.difference(a, b)).mean[0] for a, b in zip(small, small[1:])]
    starts = [i for i in range(1, len(diff)) if diff[i] > 4 and diff[i - 1] <= 4]
    no_clicks, yes_click, answer = starts[:4], starts[4], starts[5]
    picks = [(no_clicks[0] - 1, "start")] + [(s - 1, f"Hayır × {k}") for k, s in enumerate(no_clicks[1:] + [yes_click], 1)]
    picks += [((yes_click + answer) // 2, "Evet: loader"), (len(files) - 1, "the answer")]
    tw, th = 300, 200
    W, H = 70 * 2 + 4 * tw + 3 * 24, 120 + 2 * (th + 70)
    im = Image.new("RGBA", (W, H), LIGHT)
    d = ImageDraw.Draw(im)
    caption(d, 70, 36, 3, "What each click does (real frames)")
    for i, (idx, label) in enumerate(picks):
        col, row = i % 4, i // 4
        x0, y0 = 70 + col * (tw + 24), 110 + row * (th + 70)
        fr = Image.open(files[idx]).convert("RGB").resize((tw, th), Image.LANCZOS)
        shadow(im, (x0, y0, x0 + tw, y0 + th), 14, offset=8, blur=12, alpha=45)
        d = ImageDraw.Draw(im)
        mask = Image.new("L", fr.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw - 1, th - 1], 14, fill=255)
        im.paste(fr, (x0, y0), mask)
        d.rounded_rectangle([x0, y0, x0 + tw, y0 + th], 14, outline="#f3d3da", width=2)
        d.text((x0 + 4, y0 + th + 14), label, font=BODY_B(21), fill=DARK)
    return im.convert("RGB")

if __name__ == "__main__":
    cover().save(os.path.join(OUT, "cover.png"), optimize=True)
    if len(sys.argv) > 1:
        demo(sys.argv[1])
        clicks(sys.argv[1]).save(os.path.join(OUT, "clicks.png"), optimize=True)
    print("figures ->", OUT)
