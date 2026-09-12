"""Cute pony/unicorn character in a few reusable poses, built from
drawlib primitives. Local coords: x:0-1000, y:0-1150, animal faces +x
(right). Mapped onto the page with a small affine transform (Trans)."""
import math
from drawlib import (bezier4, stroke_pts, circle_o, dot, ellipse_outline_rot,
                      leaf, BLACK)


class Trans:
    def __init__(self, ox, oy, scale, flip=False, angle=0, pivot=(500, 700)):
        self.ox, self.oy, self.scale, self.flip, self.angle, self.pivot = ox, oy, scale, flip, angle, pivot

    def __call__(self, x, y):
        if self.flip:
            x = 1000 - x
        a = math.radians(self.angle)
        ca, sa = math.cos(a), math.sin(a)
        px, py = self.pivot
        dx, dy = x - px, y - py
        rx = dx * ca - dy * sa
        ry = dx * sa + dy * ca
        x2, y2 = px + rx, py + ry
        return (self.ox + x2 * self.scale, self.oy + y2 * self.scale)

    def w(self, base):
        return max(1.5, base * self.scale)


def _bez(p0, mid, p1, n=14):
    return bezier4(p0, mid, mid, p1, n)


def _eye(draw, T, cx, cy, awake=True, fill=BLACK):
    if awake:
        circle_o(draw, T(cx, cy), 22 * T.scale, T.w(4), fill=fill)
        dot(draw, T(cx + 5, cy + 4), 7 * T.scale, fill=fill)
        for dxx in (-13, 2, 17):
            stroke_pts(draw, [T(cx + dxx, cy - 20), T(cx + dxx * 1.3, cy - 35)], T.w(3), fill=fill)
    else:
        stroke_pts(draw, _bez(T(cx - 16, cy), T(cx, cy + 6), T(cx + 16, cy)), T.w(3.5), fill=fill)


def _leg(draw, T, hip, hoof, fill=BLACK):
    knee = ((hip[0] + hoof[0]) / 2, (hip[1] + hoof[1]) / 2)
    stroke_pts(draw, _bez(T(*hip), T(*knee), T(*hoof), 12), T.w(17), fill=fill)
    ellipse_outline_rot(draw, *T(*hoof), 23 * T.scale, 14 * T.scale, T.angle, T.w(5), fill=fill)


def _hair(draw, T, pairs, fill=BLACK):
    """pairs: list of (base, tip, bulge) -> cascading leaf locks."""
    for base, tip, bulge in pairs:
        leaf(draw, T(*base), T(*tip), bulge * T.scale, T.w(6), fill=fill)


def _head(draw, T, hx, hy, hr, awake=True, fill=BLACK):
    circle_o(draw, T(hx, hy), hr * T.scale, T.w(9), fill=fill)
    mx, my = hx + hr * 1.02, hy + hr * 0.30
    ellipse_outline_rot(draw, *T(mx, my), hr * 0.36 * T.scale, hr * 0.25 * T.scale, T.angle + 12, T.w(6), fill=fill)
    dot(draw, T(mx + hr * 0.30, my + hr * 0.05), 5.5 * T.scale, fill=fill)
    _eye(draw, T, hx + hr * 0.30, hy - hr * 0.05, awake=awake, fill=fill)
    ear_a = (hx - hr * 0.35, hy - hr * 0.82)
    ear_b = (hx + hr * 0.18, hy - hr * 0.92)
    leaf(draw, T(*ear_a), T(ear_a[0] - hr * 0.28, ear_a[1] - hr * 0.55), hr * 0.16 * T.scale, T.w(6), fill=fill)
    leaf(draw, T(*ear_b), T(ear_b[0] - hr * 0.10, ear_b[1] - hr * 0.55), hr * 0.16 * T.scale, T.w(6), fill=fill)
    hb_l = (hx + hr * 0.28, hy - hr * 0.86)
    hb_r = (hx + hr * 0.62, hy - hr * 0.80)
    h_tip = (hx + hr * 0.46, hy - hr * 1.68)
    stroke_pts(draw, [T(*hb_l), T(*h_tip), T(*hb_r)], T.w(6), closed=True, fill=fill)
    for k in (0.32, 0.58):
        a1 = (hb_l[0] + (h_tip[0] - hb_l[0]) * k - hr * 0.05, hb_l[1] + (h_tip[1] - hb_l[1]) * k)
        a2 = (hb_r[0] + (h_tip[0] - hb_r[0]) * k + hr * 0.05, hb_r[1] + (h_tip[1] - hb_r[1]) * k)
        stroke_pts(draw, [T(*a1), T(*a2)], T.w(3), fill=fill)


def draw_standing(draw, ox, oy, scale, flip=False, fill=BLACK, wings=False):
    T = Trans(ox, oy, scale, flip)
    ellipse_outline_rot(draw, *T(420, 840), 235 * scale, 170 * scale, 0, T.w(9), fill=fill)
    if wings:
        _wing(draw, T, (420, 790), fill=fill)
    _leg(draw, T, (280, 985), (255, 1100), fill=fill)
    _leg(draw, T, (350, 1000), (345, 1110), fill=fill)
    _leg(draw, T, (555, 1000), (565, 1110), fill=fill)
    _leg(draw, T, (620, 985), (650, 1100), fill=fill)
    _hair(draw, T, [
        ((630, 465), (560, 400), 34), ((580, 545), (495, 500), 38), ((520, 615), (425, 585), 40),
        ((450, 675), (350, 660), 38), ((375, 715), (270, 715), 34),
    ], fill=fill)
    _hair(draw, T, [
        ((205, 745), (150, 790), 30), ((175, 810), (120, 865), 30), ((175, 875), (135, 935), 26),
    ], fill=fill)
    _head(draw, T, 700, 580, 150, awake=True, fill=fill)
    return T


def draw_sitting(draw, ox, oy, scale, flip=False, fill=BLACK):
    T = Trans(ox, oy, scale, flip)
    ellipse_outline_rot(draw, *T(450, 880), 240 * scale, 195 * scale, 0, T.w(9), fill=fill)
    _leg(draw, T, (300, 1010), (275, 1120), fill=fill)
    _leg(draw, T, (615, 1010), (645, 1120), fill=fill)
    _leg(draw, T, (250, 1040), (205, 1110), fill=fill)
    _leg(draw, T, (670, 1040), (715, 1110), fill=fill)
    _hair(draw, T, [
        ((650, 505), (580, 440), 34), ((600, 585), (515, 545), 38), ((540, 655), (445, 630), 40),
        ((470, 715), (370, 705), 38), ((395, 755), (290, 755), 34),
    ], fill=fill)
    _hair(draw, T, [
        ((225, 790), (170, 835), 30), ((195, 855), (140, 910), 30), ((195, 920), (150, 975), 26),
    ], fill=fill)
    _head(draw, T, 720, 620, 150, awake=True, fill=fill)
    return T


def draw_lying(draw, ox, oy, scale, flip=False, fill=BLACK):
    T = Trans(ox, oy, scale, flip)
    ellipse_outline_rot(draw, *T(560, 880), 300 * scale, 155 * scale, 0, T.w(9), fill=fill)
    for hip, hoof in [((350, 960), (330, 1020)), ((440, 985), (430, 1045)),
                       ((630, 985), (650, 1045)), ((720, 960), (755, 1020))]:
        stroke_pts(draw, _bez(T(*hip), T((hip[0] + hoof[0]) / 2, hip[1] + 25), T(*hoof), 10), T.w(13), fill=fill)
    _hair(draw, T, [
        ((770, 780), (830, 745), 28), ((805, 830), (865, 810), 28), ((815, 880), (875, 875), 24),
    ], fill=fill)
    _head(draw, T, 270, 730, 145, awake=False, fill=fill)
    for i, s in enumerate((1.0, 0.8, 0.62)):
        zx, zy = T(560 + i * 48 * s, 560 - i * 58 * s)
        z = 24 * s * scale
        stroke_pts(draw, [(zx, zy), (zx + z, zy), (zx, zy + z), (zx + z, zy + z)], T.w(4), fill=fill)
    return T


def _wing(draw, T, base, fill=BLACK):
    for ang, ln in [(-160, 210), (-110, 260), (-60, 215)]:
        a = math.radians(ang)
        tip = (base[0] + ln * math.cos(a), base[1] + ln * math.sin(a))
        leaf(draw, T(*base), T(*tip), 40 * T.scale, T.w(6), fill=fill)


def draw_flying(draw, ox, oy, scale, flip=False, fill=BLACK):
    T = Trans(ox, oy, scale, flip, angle=-14, pivot=(420, 840))
    ellipse_outline_rot(draw, *T(420, 840), 230 * scale, 165 * scale, T.angle, T.w(9), fill=fill)
    _wing(draw, T, (370, 810), fill=fill)
    for hip, hoof in [((300, 970), (280, 1030)), ((370, 990), (360, 1045)),
                       ((540, 990), (555, 1040)), ((605, 970), (635, 1020))]:
        stroke_pts(draw, _bez(T(*hip), T((hip[0] + hoof[0]) / 2, hip[1] + 25), T(*hoof), 10), T.w(13), fill=fill)
    _hair(draw, T, [
        ((610, 480), (545, 420), 32), ((565, 555), (485, 515), 36), ((510, 620), (420, 595), 36),
        ((445, 675), (355, 665), 32),
    ], fill=fill)
    _hair(draw, T, [
        ((215, 745), (165, 790), 28), ((190, 805), (140, 855), 26),
    ], fill=fill)
    _head(draw, T, 680, 590, 145, awake=True, fill=fill)
    return T


def draw_portrait(draw, ox, oy, scale, flip=False, fill=BLACK):
    """Close-up bust: just the head, big and centered."""
    T = Trans(ox, oy, scale, flip)
    _head(draw, T, 500, 500, 210, awake=True, fill=fill)
    return T


def draw_rearing(draw, ox, oy, scale, flip=False, fill=BLACK):
    T = Trans(ox, oy, scale, flip, angle=-9, pivot=(420, 840))
    ellipse_outline_rot(draw, *T(420, 840), 235 * scale, 170 * scale, T.angle, T.w(9), fill=fill)
    for hip, hoof, ka in [((300, 985), (410, 870), 35), ((370, 1000), (465, 900), 25)]:
        knee = ((hip[0] + hoof[0]) / 2, hip[1] + 10)
        stroke_pts(draw, _bez(T(*hip), T(*knee), T(*hoof), 12), T.w(17), fill=fill)
        ellipse_outline_rot(draw, *T(*hoof), 22 * scale, 14 * scale, T.angle + ka, T.w(5), fill=fill)
    _leg(draw, T, (555, 1000), (565, 1110), fill=fill)
    _leg(draw, T, (620, 985), (650, 1100), fill=fill)
    _hair(draw, T, [
        ((630, 465), (560, 400), 34), ((580, 545), (495, 500), 38), ((520, 615), (425, 585), 40),
        ((450, 675), (350, 660), 38), ((375, 715), (270, 715), 34),
    ], fill=fill)
    _hair(draw, T, [
        ((205, 745), (150, 790), 30), ((175, 810), (120, 865), 30), ((175, 875), (135, 935), 26),
    ], fill=fill)
    _head(draw, T, 700, 580, 150, awake=True, fill=fill)
    return T
