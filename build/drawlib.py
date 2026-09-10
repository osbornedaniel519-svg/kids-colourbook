"""
Reusable vector-style drawing primitives for the coloring book generator.
Everything is stroke-only (outline), pure black on white, so pages print
cleanly as line art. Filled shapes are only used for tiny details (pupils,
confetti dots) or for the color cover.
"""
import math
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PAGE_W, PAGE_H = 1700, 2200          # 8.5 x 11 in @ 200dpi
MARGIN = 80
BW = 9   # base stroke width (main outlines)
TW = 5   # thin stroke width (details)


# ---------- low level ----------

def bezier4(p0, c0, c1, p1, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * c0[0] + 3 * mt * (t**2) * c1[0] + (t**3) * p1[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * c0[1] + 3 * mt * (t**2) * c1[1] + (t**3) * p1[1]
        pts.append((x, y))
    return pts


def stroke_pts(draw, pts, width, closed=False, fill=BLACK):
    if len(pts) < 2:
        return
    seq = list(pts) + ([pts[0]] if closed else [])
    draw.line(seq, fill=fill, width=max(1, int(round(width))), joint="curve")
    r = width / 2
    for (x, y) in seq:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def circle_o(draw, c, r, width, fill=BLACK):
    x, y = c
    draw.ellipse([x - r, y - r, x + r, y + r], outline=fill, width=max(1, int(round(width))))


def dot(draw, c, r, fill=BLACK):
    x, y = c
    draw.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def ellipse_pts(cx, cy, rx, ry, rot=0, n=40):
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        ex, ey = rx * math.cos(t), ry * math.sin(t)
        x = cx + ex * ca - ey * sa
        y = cy + ex * sa + ey * ca
        pts.append((x, y))
    return pts


def ellipse_outline_rot(draw, cx, cy, rx, ry, rot, width, fill=BLACK):
    stroke_pts(draw, ellipse_pts(cx, cy, rx, ry, rot), width, closed=True, fill=fill)


def arc_pts(cx, cy, r, a0, a1, n=30):
    pts = []
    for i in range(n + 1):
        t = a0 + (a1 - a0) * i / n
        a = math.radians(t)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def leaf(draw, p0, p1, bulge, width, fill=BLACK):
    """Closed pointed petal/leaf shape between p0 and p1."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    nx, ny = -dy, dx
    ln = math.hypot(nx, ny) or 1
    nx, ny = nx / ln, ny / ln
    c1 = (mx + nx * bulge, my + ny * bulge)
    c2 = (mx - nx * bulge, my - ny * bulge)
    top = bezier4(p0, c1, c1, p1, 16)
    bot = bezier4(p1, c2, c2, p0, 16)
    stroke_pts(draw, top + bot, width, closed=False, fill=fill)


def puff_row(draw, path, radii, width, fill=BLACK):
    """Row of overlapping outline circles along a path -> fluffy mane/tail/cloud look."""
    for (x, y), r in zip(path, radii):
        circle_o(draw, (x, y), r, width, fill=fill)


def star_pts(cx, cy, r_out, r_in, points, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * (360 / (points * 2)))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def star(draw, cx, cy, r_out, r_in, points, width, rot=-90, fill=BLACK):
    stroke_pts(draw, star_pts(cx, cy, r_out, r_in, points, rot), width, closed=True, fill=fill)


def heart(draw, cx, cy, size, width, fill=BLACK):
    s = size
    top = (cx, cy - s * 0.35)
    left_top = (cx - s, cy - s * 0.7)
    left_bot = (cx - s * 0.05, cy + s * 0.55)
    right_top = (cx + s, cy - s * 0.7)
    right_bot = (cx + s * 0.05, cy + s * 0.55)
    a = bezier4(top, (cx - s * 0.3, cy - s * 1.15), (cx - s * 1.15, cy - s * 0.9), left_top, 16)
    b = bezier4(left_top, (cx - s * 1.1, cy - s * 0.15), (cx - s * 0.5, cy + s * 0.15), left_bot, 16)
    c = bezier4(left_bot, (cx - s * 0.05, cy + s * 0.95), (cx + s * 0.05, cy + s * 0.95), right_bot, 16)
    d = bezier4(right_bot, (cx + s * 0.5, cy + s * 0.15), (cx + s * 1.1, cy - s * 0.15), right_top, 16)
    e = bezier4(right_top, (cx + s * 1.15, cy - s * 0.9), (cx + s * 0.3, cy - s * 1.15), top, 16)
    stroke_pts(draw, a + b + c + d + e, width, closed=False, fill=fill)


def flower(draw, cx, cy, r, petals, width, fill=BLACK):
    for i in range(petals):
        a = 2 * math.pi * i / petals
        tip = (cx + r * math.cos(a), cy + r * math.sin(a))
        leaf(draw, (cx, cy), tip, r * 0.42, width, fill=fill)
    circle_o(draw, (cx, cy), r * 0.32, width, fill=fill)


def cloud(draw, cx, cy, scale, width, fill=BLACK):
    puffs = [(-1.1, 0.15, 0.55), (-0.5, -0.35, 0.7), (0.15, -0.45, 0.75),
             (0.85, -0.15, 0.62), (1.25, 0.2, 0.5)]
    for dx, dy, r in puffs:
        circle_o(draw, (cx + dx * scale * 60, cy + dy * scale * 60), r * scale * 60, width, fill=fill)
    base = [(cx - 1.5 * scale * 60, cy + 0.35 * scale * 60), (cx + 1.6 * scale * 60, cy + 0.35 * scale * 60)]
    stroke_pts(draw, arc_pts(cx, cy + 0.1 * scale * 60, 1.55 * scale * 60, 10, 170, 24), width, fill=fill)


def sun(draw, cx, cy, r, rays, width, fill=BLACK):
    circle_o(draw, (cx, cy), r, width, fill=fill)
    for i in range(rays):
        a = 2 * math.pi * i / rays
        p0 = (cx + (r * 1.25) * math.cos(a), cy + (r * 1.25) * math.sin(a))
        p1 = (cx + (r * 1.7) * math.cos(a), cy + (r * 1.7) * math.sin(a))
        stroke_pts(draw, [p0, p1], width * 0.8, fill=fill)


def moon_crescent(draw, cx, cy, r, width, fill=BLACK):
    outer = arc_pts(cx, cy, r, 100, 440, 30)
    inner = arc_pts(cx + r * 0.55, cy - r * 0.05, r * 0.92, 260, -60, 30)
    stroke_pts(draw, outer + inner, width, closed=True, fill=fill)


def rainbow(draw, cx, cy, r_out, n_bands, band_w, width, fill=BLACK):
    for i in range(n_bands):
        r = r_out - i * band_w
        stroke_pts(draw, arc_pts(cx, cy, r, 180, 360, 40), width, fill=fill)


def tree(draw, cx, cy, scale, width, fill=BLACK):
    trunk_top = (cx, cy - 40 * scale)
    trunk_bot = (cx, cy + 60 * scale)
    stroke_pts(draw, [trunk_bot, trunk_top], 14 * scale, fill=fill)
    puff_row(draw, [(cx - 55 * scale, cy - 80 * scale), (cx + 10 * scale, cy - 130 * scale),
                    (cx + 70 * scale, cy - 70 * scale), (cx - 5 * scale, cy - 55 * scale)],
             [42 * scale, 50 * scale, 44 * scale, 46 * scale], width, fill=fill)


def mushroom(draw, cx, cy, scale, width, spotted=True, fill=BLACK):
    r = 60 * scale
    cap = arc_pts(cx, cy, r, 180, 360, 30)
    stroke_pts(draw, cap, width, fill=fill)
    stroke_pts(draw, [(cx - r, cy), (cx + r, cy)], width, fill=fill)
    stroke_pts(draw, [(cx - 22 * scale, cy), (cx - 18 * scale, cy + 70 * scale),
                       (cx + 18 * scale, cy + 70 * scale), (cx + 22 * scale, cy)], width, closed=True, fill=fill)
    if spotted:
        dot(draw, (cx - r * 0.35, cy - r * 0.55), 8 * scale, fill=fill)
        dot(draw, (cx + r * 0.4, cy - r * 0.4), 7 * scale, fill=fill)
        dot(draw, (cx, cy - r * 0.85), 6 * scale, fill=fill)


def castle(draw, cx, cy, scale, width, fill=BLACK):
    w, h = 340 * scale, 220 * scale
    x0, y0 = cx - w / 2, cy - h
    x1, y1 = cx + w / 2, cy
    stroke_pts(draw, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], width, closed=True, fill=fill)
    for tx in (x0, cx, x1):
        tw = 70 * scale
        stroke_pts(draw, [(tx - tw / 2, y0 + 10 * scale), (tx - tw / 2, y0 - 90 * scale),
                           (tx + tw / 2, y0 - 90 * scale), (tx + tw / 2, y0 + 10 * scale)],
                    width, closed=False, fill=fill)
        stroke_pts(draw, [(tx - tw / 2 - 6 * scale, y0 - 90 * scale), (tx, y0 - 150 * scale),
                           (tx + tw / 2 + 6 * scale, y0 - 90 * scale)], width, closed=True, fill=fill)
    stroke_pts(draw, [(tx, y0 - 150 * scale), (tx, y0 - 190 * scale)], width, fill=fill)
    flag = [(tx, y0 - 190 * scale), (tx + 34 * scale, y0 - 178 * scale), (tx, y0 - 166 * scale)]
    stroke_pts(draw, flag, width, closed=True, fill=fill)
    door_w, door_h = 60 * scale, 100 * scale
    stroke_pts(draw, arc_pts(cx, y1 - door_h, door_w / 2, 180, 360, 20) + [(cx + door_w / 2, y1)] +
               [(cx - door_w / 2, y1)], width, closed=True, fill=fill)


def wave(draw, x0, x1, y, amp, cycles, width, fill=BLACK):
    pts = []
    n = 60
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        yy = y + amp * math.sin(2 * math.pi * cycles * t)
        pts.append((x, yy))
    stroke_pts(draw, pts, width, fill=fill)


def butterfly(draw, cx, cy, scale, width, fill=BLACK):
    leaf(draw, (cx, cy), (cx - 46 * scale, cy - 46 * scale), 30 * scale, width, fill=fill)
    leaf(draw, (cx, cy), (cx - 34 * scale, cy + 40 * scale), 22 * scale, width, fill=fill)
    leaf(draw, (cx, cy), (cx + 46 * scale, cy - 46 * scale), 30 * scale, width, fill=fill)
    leaf(draw, (cx, cy), (cx + 34 * scale, cy + 40 * scale), 22 * scale, width, fill=fill)
    stroke_pts(draw, [(cx, cy - 30 * scale), (cx, cy + 30 * scale)], width, fill=fill)
    stroke_pts(draw, [(cx, cy - 28 * scale), (cx - 16 * scale, cy - 46 * scale)], width * 0.7, fill=fill)
    stroke_pts(draw, [(cx, cy - 28 * scale), (cx + 16 * scale, cy - 46 * scale)], width * 0.7, fill=fill)


def balloon(draw, cx, cy, r, string_len, width, fill=BLACK):
    ellipse_outline_rot(draw, cx, cy, r * 0.85, r, 0, width, fill=fill)
    tip = (cx, cy + r)
    knot = (cx, cy + r + 14)
    stroke_pts(draw, [tip, knot], width, fill=fill)
    pts = []
    n = 20
    for i in range(n + 1):
        t = i / n
        pts.append((cx + 14 * math.sin(t * 5), cy + r + 14 + string_len * t))
    stroke_pts(draw, pts, width * 0.6, fill=fill)


def snowflake(draw, cx, cy, r, width, fill=BLACK):
    for i in range(6):
        a = math.radians(i * 60)
        p1 = (cx + r * math.cos(a), cy + r * math.sin(a))
        stroke_pts(draw, [(cx, cy), p1], width * 0.7, fill=fill)
        base = (cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a))
        for s in (-1, 1):
            aa = a + s * math.radians(35)
            p2 = (base[0] + r * 0.28 * math.cos(aa), base[1] + r * 0.28 * math.sin(aa))
            stroke_pts(draw, [base, p2], width * 0.6, fill=fill)


def musical_note(draw, cx, cy, scale, width, fill=BLACK):
    stroke_pts(draw, [(cx, cy), (cx, cy - 90 * scale)], width, fill=fill)
    ellipse_outline_rot(draw, cx - 14 * scale, cy + 6 * scale, 16 * scale, 11 * scale, -20, width, fill=fill)
    stroke_pts(draw, [(cx, cy - 90 * scale), (cx + 30 * scale, cy - 80 * scale),
                       (cx + 28 * scale, cy - 55 * scale), (cx, cy - 65 * scale)], width, closed=True, fill=fill)


def bird_m(draw, cx, cy, scale, width, fill=BLACK):
    stroke_pts(draw, [(cx - 22 * scale, cy), (cx - 6 * scale, cy - 14 * scale), (cx, cy),
                       (cx + 6 * scale, cy - 14 * scale), (cx + 22 * scale, cy)], width, fill=fill)


def ground_line(draw, y, width=TW, fill=BLACK):
    stroke_pts(draw, [(MARGIN, y), (PAGE_W - MARGIN, y)], width, fill=fill)


def page_frame(draw, fill=BLACK):
    inset = 40
    stroke_pts(draw, [(inset, inset), (PAGE_W - inset, inset), (PAGE_W - inset, PAGE_H - inset),
                       (inset, PAGE_H - inset)], 6, closed=True, fill=fill)
    for cx, cy in [(inset, inset), (PAGE_W - inset, inset), (inset, PAGE_H - inset), (PAGE_W - inset, PAGE_H - inset)]:
        flower(draw, cx, cy, 22, 5, 4, fill=fill)
