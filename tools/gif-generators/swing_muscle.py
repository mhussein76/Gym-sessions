import math
from PIL import Image, ImageDraw, ImageFont

W, H = 420, 400
SS = 2
FL = 372
X0 = 215
LT = LS = 66
LTOR, LU, LF = 78, 46, 44
BG = (20, 28, 40)
FLOORC = (70, 88, 110)
SKIN = (200, 208, 220)
SKIN2 = (168, 178, 192)
RED = (235, 52, 64)
ACC = (255, 122, 47)

try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15 * SS)
    FONT_S = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14 * SS)
except Exception:
    FONT = FONT_S = ImageFont.load_default()

rad = math.radians


def pt(o, L, a):
    return (o[0] + L * math.sin(rad(a)), o[1] + L * math.cos(rad(a)))


def up(o, L, a):
    return (o[0] + L * math.sin(rad(a)), o[1] - L * math.cos(rad(a)))


def ease(t):
    return t * t * (3 - 2 * t)


def S(p):
    return (p[0] * SS, p[1] * SS)


def capsule(d, p, q, w1, w2, col):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    poly = [(p[0] + nx * w1 / 2, p[1] + ny * w1 / 2), (q[0] + nx * w2 / 2, q[1] + ny * w2 / 2),
            (q[0] - nx * w2 / 2, q[1] - ny * w2 / 2), (p[0] - nx * w1 / 2, p[1] - ny * w1 / 2)]
    d.polygon([S(z) for z in poly], fill=col)
    for c, w in ((p, w1), (q, w2)):
        d.ellipse([(c[0] - w / 2) * SS, (c[1] - w / 2) * SS, (c[0] + w / 2) * SS, (c[1] + w / 2) * SS], fill=col)


def norm(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy) or 1
    return (-dy / L, dx / L), L


def blob(d, p, q, f, off, lenf, wid, inten):
    n, L = norm(p, q)
    cx = p[0] + (q[0] - p[0]) * f + n[0] * off
    cy = p[1] + (q[1] - p[1]) * f + n[1] * off
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    a, b = L * lenf / 2, wid / 2
    pts = []
    for i in range(28):
        t = 2 * math.pi * i / 28
        x, y = a * math.cos(t), b * math.sin(t)
        pts.append(S((cx + x * ux + y * n[0], cy + x * uy + y * n[1])))
    alpha = int(40 + 215 * max(0, min(1, inten)))
    d.polygon(pts, fill=RED + (alpha,))
    return (cx, cy)


def frame(P, label, bell=True):
    base = Image.new("RGBA", (W * SS, H * SS), BG + (255,))
    d = ImageDraw.Draw(base)
    d.line([(0, FL * SS), (W * SS, FL * SS)], fill=FLOORC, width=3 * SS)

    ankle = (X0, FL - 6)
    knee = (ankle[0] + LS * math.sin(rad(P["s"])), ankle[1] - LS * math.cos(rad(P["s"])))
    hip = (knee[0] - LT * math.sin(rad(P["t"])), knee[1] - LT * math.cos(rad(P["t"])))
    sh = up(hip, LTOR, P["tt"])
    head = up(sh, 30, P["tt"] * 0.6)
    el = pt(sh, LU, P["a"])
    wr = pt(el, LF, P["f"])

    # far arm (slightly behind) then body
    capsule(d, sh, pt(sh, LU, P["a"] - 4), 12, 9, SKIN2)
    capsule(d, hip, knee, 26, 18, SKIN)
    capsule(d, knee, ankle, 17, 11, SKIN)
    capsule(d, ankle, (ankle[0] + 22, ankle[1] + 3), 10, 8, SKIN)
    capsule(d, hip, sh, 32, 38, SKIN)
    capsule(d, sh, up(sh, 14, P["tt"] * 0.6), 13, 13, SKIN)
    d.ellipse([(head[0] - 15) * SS, (head[1] - 15) * SS, (head[0] + 15) * SS, (head[1] + 15) * SS], fill=SKIN)
    capsule(d, sh, el, 14, 10, SKIN)
    capsule(d, el, wr, 10, 8, SKIN)

    # kettlebell
    c = pt(wr, 20, P["f"])
    d.ellipse([(c[0] - 17) * SS, (c[1] - 17) * SS, (c[0] + 17) * SS, (c[1] + 17) * SS], fill=(30, 30, 34), outline=(210, 210, 210), width=2 * SS)
    d.arc([(c[0] - 11) * SS, (c[1] - 33) * SS, (c[0] + 11) * SS, (c[1] - 8) * SS], 180, 360, fill=(210, 210, 210), width=3 * SS)

    # muscles (translucent overlay)
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    o = ImageDraw.Draw(ov)
    g = P["g"]; h = P["h"]; q = P["q"]; b = P["b"]; dl = P["d"]
    tp = {}
    tp["Glutes"] = blob(o, sh, hip, 1.0, 10, 0.4, 28, g)
    tp["Hamstrings"] = blob(o, hip, knee, 0.5, 9, 0.8, 15, h)
    tp["Quads"] = blob(o, hip, knee, 0.5, -9, 0.7, 14, q)
    tp["Calves"] = blob(o, knee, ankle, 0.35, 6, 0.5, 11, 0.35 + 0.2 * q)
    tp["Lower back"] = blob(o, hip, sh, 0.32, -12, 0.5, 14, b)
    tp["Shoulders"] = blob(o, sh, el, 0.18, 0, 0.5, 18, dl)
    tp["Core"] = blob(o, hip, sh, 0.5, 12, 0.5, 14, 0.25 + 0.5 * b)
    base = Image.alpha_composite(base, ov)
    d = ImageDraw.Draw(base)

    # labels with leader lines (left column)
    order = ["Shoulders", "Lower back", "Glutes", "Hamstrings", "Quads", "Calves"]
    y = 58
    for nme in order:
        inten = {"Glutes": g, "Hamstrings": h, "Quads": q, "Calves": 0.4, "Lower back": b, "Shoulders": dl}[nme]
        col = (255, 255, 255) if inten > 0.5 else (150, 165, 185)
        d.text((14 * SS, y * SS), nme, font=FONT_S, fill=col)
        tx, ty = tp[nme]
        d.line([(100 * SS, (y + 9) * SS), (tx * SS, ty * SS)], fill=(255, 122, 47, 255) if inten > 0.5 else (90, 105, 125, 255), width=1 * SS)
        d.ellipse([(tx - 3) * SS, (ty - 3) * SS, (tx + 3) * SS, (ty + 3) * SS], fill=ACC if inten > 0.5 else (90, 105, 125))
        y += 36
    d.text((14 * SS, 14 * SS), "Kettlebell Swing", font=FONT, fill=(255, 255, 255))
    d.text((14 * SS, 36 * SS), label, font=FONT_S, fill=ACC)
    return base.convert("RGB").resize((W, H), Image.LANCZOS)


def kp(**k):
    base = dict(s=3, t=3, tt=3, a=88, f=88, g=0, h=0, q=0, b=0, d=0)
    base.update(k)
    return base


top = kp(s=3, t=3, tt=3, a=88, f=88, g=1.0, h=0.7, q=0.7, b=0.35, d=0.7)
bot = kp(s=18, t=58, tt=64, a=-12, f=-12, g=0.35, h=0.9, q=0.2, b=0.8, d=0.15)


def lerp(a, b, t):
    t = ease(t)
    return {k: a[k] + (b[k] - a[k]) * t for k in a}


frames = []
hold, per = 5, 16
for _ in range(hold):
    frames.append((top, "Stand tall: squeeze glutes"))
for j in range(1, per):
    frames.append((lerp(top, bot, j / per), "1. Hips back, back flat"))
for _ in range(hold):
    frames.append((bot, "Hamstrings + back loaded"))
for j in range(1, per):
    frames.append((lerp(bot, top, j / per), "2. Snap hips forward!"))

imgs = [frame(P, lab) for P, lab in frames]
imgs[0].save("img/swing-muscle.gif", save_all=True, append_images=imgs[1:], duration=55, loop=0, optimize=True)
imgs[0].save("/tmp/m_top.png")
imgs[hold + per // 2].save("/tmp/m_mid.png")
imgs[hold + per - 1 + hold - 1].save("/tmp/m_bot.png")
print(len(imgs))
