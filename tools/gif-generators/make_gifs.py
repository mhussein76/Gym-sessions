import math, sys
from PIL import Image, ImageDraw

W = 360          # final size
SS = 2           # supersampling
FL = 318         # floor y
X0 = 150         # grounded ankle x
LT = LS = 60     # thigh, shin
LTOR, LU, LF = 70, 42, 40

BG = (26, 36, 49)
FLOORC = (70, 88, 110)
BODY = (255, 255, 255)
BODY2 = (170, 184, 200)
ACC = (255, 122, 47)
DARK = (34, 34, 34)


def r(d):
    return math.radians(d)


def pt(o, L, a):
    # direction measured from straight-down, forward(+x) positive
    return (o[0] + L * math.sin(r(a)), o[1] + L * math.cos(r(a)))


def up(o, L, a):
    # direction measured from straight-up, forward positive
    return (o[0] + L * math.sin(r(a)), o[1] - L * math.cos(r(a)))


def ease(t):
    return t * t * (3 - 2 * t)


def lerp_pose(a, b, t):
    t = ease(t)
    return {k: a[k] + (b[k] - a[k]) * t for k in a}


def seq(keys, per=14, hold=5):
    """keys: list of dicts (same keys). returns list of poses, looping back to first."""
    frames = []
    n = len(keys)
    for i in range(n):
        a, b = keys[i], keys[(i + 1) % n]
        frames += [dict(a)] * hold
        for j in range(1, per):
            frames.append(lerp_pose(a, b, j / per))
    return frames


def line(d, p, q, w, c):
    d.line([p, q], fill=c, width=int(w * SS), joint="curve")
    for z in (p, q):
        d.ellipse([z[0] - w * SS / 2, z[1] - w * SS / 2, z[0] + w * SS / 2, z[1] + w * SS / 2], fill=c)


def S(p):
    return (p[0] * SS, p[1] * SS)


def draw_person(d, P, mode, extra=None):
    """P: pose dict. Returns key points."""
    tt = P.get("tt", 0)
    if mode == "ground":
        ankle = (X0, FL - 6)
        knee = pt(ankle, LS, -P["s"] + 180) if False else (ankle[0] + LS * math.sin(r(P["s"])), ankle[1] - LS * math.cos(r(P["s"])))
        hip = (knee[0] - LT * math.sin(r(P["t"])), knee[1] - LT * math.cos(r(P["t"])))
        legs = [(hip, knee, ankle, BODY)]
        if P.get("phi") is not None and P.get("use2", 0) > 0.5:
            k2 = pt(hip, LT, P["phi"])
            a2 = pt(k2, LS, P["psi"])
            legs.insert(0, (hip, k2, a2, BODY2))
        sh = up(hip, LTOR, tt)
    elif mode == "run":
        hip = (X0 + 10, FL - 6 - 118 + P["by"])
        legs = []
        for ph, ps, col in ((P["p1"], P["q1"], BODY), (P["p2"], P["q2"], BODY2)):
            k = pt(hip, LT, ph)
            a = pt(k, LS, ps)
            legs.insert(0 if col == BODY2 else len(legs), (hip, k, a, col))
        sh = up(hip, LTOR, tt)
    else:  # hang
        sh = (X0, 128)
        hip = (sh[0], sh[1] + LTOR)
        legs = []
        k2 = pt(hip, LT, P["phi"] - 6)
        a2 = pt(k2, LS, P["psi"])
        legs.append((hip, k2, a2, BODY2))
        k1 = pt(hip, LT, P["phi"])
        a1 = pt(k1, LS, P["psi"])
        legs.append((hip, k1, a1, BODY))
    # legs
    for h, k, a, c in legs:
        line(d, S(h), S(k), 11, c)
        line(d, S(k), S(a), 10, c)
        line(d, S(a), S((a[0] + 16, a[1] + 2)), 8, c)
    # torso + head
    line(d, S(hip), S(sh), 14, BODY)
    head = up(sh, 26, tt * 0.6)
    d.ellipse([ (head[0]-14)*SS, (head[1]-14)*SS, (head[0]+14)*SS, (head[1]+14)*SS ], fill=BODY)
    # arm
    el = pt(sh, LU, P["a"])
    wr = pt(el, LF, P["f"])
    line(d, S(sh), S(el), 9, ACC)
    line(d, S(el), S(wr), 8, ACC)
    return dict(hip=hip, sh=sh, el=el, wr=wr)


def new_img():
    im = Image.new("RGB", (W * SS, W * SS), BG)
    d = ImageDraw.Draw(im)
    d.line([(0, FL * SS), (W * SS, FL * SS)], fill=FLOORC, width=3 * SS)
    return im, d


def kettlebell(d, c):
    x, y = c
    d.ellipse([(x - 15) * SS, (y - 15) * SS, (x + 15) * SS, (y + 15) * SS], fill=DARK, outline=(200, 200, 200), width=2 * SS)
    d.arc([(x - 10) * SS, (y - 30) * SS, (x + 10) * SS, (y - 6) * SS], 180, 360, fill=(200, 200, 200), width=3 * SS)


def bag(d, c, rot=0):
    x, y = c
    d.rounded_rectangle([(x - 30) * SS, (y - 13) * SS, (x + 30) * SS, (y + 13) * SS], radius=10 * SS, fill=(60, 66, 78), outline=(210, 210, 210), width=2 * SS)
    d.line([((x - 14) * SS, (y - 13) * SS), ((x - 14) * SS, (y + 13) * SS)], fill=(150, 150, 150), width=2 * SS)
    d.line([((x + 14) * SS, (y - 13) * SS), ((x + 14) * SS, (y + 13) * SS)], fill=(150, 150, 150), width=2 * SS)


def plate(d, c):
    x, y = c
    d.ellipse([(x - 24) * SS, (y - 24) * SS, (x + 24) * SS, (y + 24) * SS], fill=(40, 40, 46), outline=(190, 190, 190), width=2 * SS)
    d.ellipse([(x - 5) * SS, (y - 5) * SS, (x + 5) * SS, (y + 5) * SS], fill=(190, 190, 190))


def save(name, imgs, ms=45):
    out = [i.resize((W, W), Image.LANCZOS) for i in imgs]
    out[0].save(f"img/{name}.gif", save_all=True, append_images=out[1:], duration=ms, loop=0, optimize=True)
    out[len(out) // 3].save(f"/tmp/prev_{name}.png")
    print(name, len(out))


# ---------- exercises ----------
def kp(**k):
    base = dict(s=3, t=3, tt=0, a=0, f=0, phi=-3, psi=-3, use2=0, bx=0, by=0)
    base.update(k)
    return base


def swing():
    top = kp(s=3, t=3, tt=3, a=88, f=88)
    bot = kp(s=18, t=55, tt=62, a=-12, f=-12)
    out = []
    for P in seq([top, bot], per=16, hold=4):
        im, d = new_img()
        pts = draw_person(d, P, "ground")
        kettlebell(d, pt(pts["wr"], 18, P["f"]))
        out.append(im)
    save("swing", out)


def snatch():
    bot = kp(s=38, t=72, tt=35, a=5, f=5)
    mid = kp(s=5, t=5, tt=0, a=75, f=170)
    top = kp(s=3, t=3, tt=0, a=175, f=178)
    out = []
    for P in seq([bot, mid, top, mid], per=10, hold=4):
        im, d = new_img()
        pts = draw_person(d, P, "ground")
        if P["f"] > 120:
            c = (pts["wr"][0], pts["wr"][1] - 16)
        else:
            c = pt(pts["wr"], 18, P["f"])
        kettlebell(d, c)
        out.append(im)
    save("snatch", out)


def lift():
    bot = kp(s=40, t=75, tt=50, a=15, f=15, bx=0, by=18)
    top = kp(s=3, t=3, tt=-3, a=40, f=165, bx=-20, by=-8)
    out = []
    for P in seq([bot, top], per=16, hold=5):
        im, d = new_img()
        pts = draw_person(d, P, "ground")
        bag(d, (pts["wr"][0] + P["bx"], pts["wr"][1] + P["by"]))
        out.append(im)
    save("sandbag-lift", out)


def run():
    out = []
    N = 24
    for i in range(N):
        th = 2 * math.pi * i / N
        P = dict(by=5 * abs(math.sin(th)), tt=10, a=45, f=165,
                 p1=38 * math.sin(th), q1=38 * math.sin(th) - (12 + 70 * max(0, math.cos(th))),
                 p2=-38 * math.sin(th), q2=-38 * math.sin(th) - (12 + 70 * max(0, -math.cos(th))))
        im, d = new_img()
        # moving ground ticks
        for k in range(-1, 12):
            x = (k * 40 - (i * 40 / N * 2)) % (W + 40) - 20
            d.line([(x * SS, (FL + 8) * SS), ((x + 16) * SS, (FL + 8) * SS)], fill=FLOORC, width=3 * SS)
        pts = draw_person(d, P, "run")
        bag(d, (pts["wr"][0] - 18, pts["wr"][1] - 4))
        out.append(im)
    save("sandbag-run", out, ms=55)


def lunge():
    st = kp(s=0, t=0, tt=0, phi=-3, psi=-3, use2=1, a=-35, f=-170)
    dn = kp(s=0, t=88, tt=0, phi=-10, psi=-85, use2=1, a=-35, f=-170)
    out = []
    for P in seq([st, dn], per=16, hold=5):
        im, d = new_img()
        pts = draw_person(d, P, "ground")
        plate(d, (pts["sh"][0] - 4, pts["sh"][1] - 2))
        out.append(im)
    save("lunge", out)


def squat():
    st = kp(s=3, t=3, tt=2, a=-35, f=-170)
    dn = kp(s=40, t=75, tt=42, a=-35, f=-170)
    out = []
    for P in seq([st, dn], per=16, hold=5):
        im, d = new_img()
        pts = draw_person(d, P, "ground")
        plate(d, (pts["sh"][0] - 4, pts["sh"][1] - 2))
        out.append(im)
    save("squat", out)


def knee():
    dn = dict(phi=3, psi=3, tt=0, a=172, f=178)
    upk = dict(phi=95, psi=8, tt=0, a=172, f=178)
    out = []
    for P in seq([dn, upk], per=14, hold=5):
        im, d = new_img()
        # bar + straps
        d.line([(60 * SS, 40 * SS), (260 * SS, 40 * SS)], fill=(190, 190, 190), width=5 * SS)
        pts = draw_person(d, P, "hang")
        el = pts["el"]
        line(d, S((el[0] + 2, 40)), S((el[0] + 2, el[1] + 8)), 12, DARK)
        out.append(im)
    save("knee-raise", out)


for f in (swing, snatch, lift, run, lunge, squat, knee):
    f()
