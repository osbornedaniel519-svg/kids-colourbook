import math
import os
from PIL import Image, ImageDraw, ImageFont
from drawlib import (PAGE_W, PAGE_H, MARGIN, WHITE, BLACK, TW,
                      cloud, star, heart, flower, sun, moon_crescent, rainbow,
                      tree, mushroom, castle, wave, butterfly, balloon,
                      snowflake, musical_note, bird_m, ground_line, page_frame,
                      stroke_pts, circle_o, dot, ellipse_outline_rot)
import unicorn as U

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
TITLE_FONT = ImageFont.truetype(f"{FONT_DIR}/EricaOne-Regular.ttf", 58)
NUM_FONT = ImageFont.truetype(f"{FONT_DIR}/Outfit-Bold.ttf", 30)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "book", "pages")
os.makedirs(OUT_DIR, exist_ok=True)

GROUND_Y = 1860
STAND_BOTTOM = 1115
SIT_BOTTOM = 1125
LIE_BOTTOM = 1020
FLY_BOTTOM = 1050


def foot_oy(bottom_local, scale, ground_y=GROUND_Y):
    return ground_y - bottom_local * scale


def new_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), WHITE)
    return img, ImageDraw.Draw(img)


def caption(draw, text, y=None):
    if y is None:
        y = PAGE_H - 145
    bbox = draw.textbbox((0, 0), text, font=TITLE_FONT)
    w = bbox[2] - bbox[0]
    draw.text(((PAGE_W - w) / 2, y), text, font=TITLE_FONT, fill=BLACK)


def page_num(draw, n):
    text = str(n)
    bbox = draw.textbbox((0, 0), text, font=NUM_FONT)
    w = bbox[2] - bbox[0]
    draw.text(((PAGE_W - w) / 2, PAGE_H - 68), text, font=NUM_FONT, fill=BLACK)


def finish(img, draw, n, title):
    page_frame(draw)
    caption(draw, title)
    page_num(draw, n)
    img.save(os.path.join(OUT_DIR, f"page_{n:02d}.png"))


def standing(draw, x, scale, **kw):
    return U.draw_standing(draw, x, foot_oy(STAND_BOTTOM, scale), scale, **kw)


def sitting(draw, x, scale, **kw):
    return U.draw_sitting(draw, x, foot_oy(SIT_BOTTOM, scale), scale, **kw)


def rearing(draw, x, scale, **kw):
    return U.draw_rearing(draw, x, foot_oy(STAND_BOTTOM, scale), scale, **kw)


def lying(draw, x, scale, **kw):
    return U.draw_lying(draw, x, foot_oy(LIE_BOTTOM, scale), scale, **kw)


def flying(draw, x, y, scale, **kw):
    return U.draw_flying(draw, x, y, scale, **kw)


# ---------------------------------------------------------------- pages ----

def p01(draw):
    ground_line(draw, GROUND_Y)
    sun(draw, 1450, 260, 70, 10, TW)
    for x, y, r in [(230, 1550, 55), (1500, 1450, 60), (330, 1750, 45)]:
        flower(draw, x, y, r, 8, TW)
    butterfly(draw, 1350, 700, 1.0, TW)
    butterfly(draw, 300, 900, 0.8, TW)
    standing(draw, 460, 1.05)


def p02(draw):
    ground_line(draw, GROUND_Y)
    rainbow(draw, 850, 1050, 560, 6, 38, TW)
    cloud(draw, 260, 500, 1.1, TW)
    cloud(draw, 1480, 420, 1.0, TW)
    rearing(draw, 540, 0.9)


def p03(draw):
    ground_line(draw, GROUND_Y)
    castle(draw, 1180, GROUND_Y, 0.95, TW)
    for x, y, r in [(200, GROUND_Y - 30, 40), (1600, GROUND_Y - 30, 40)]:
        flower(draw, x, y, r, 7, TW)
    standing(draw, 430, 1.0)


def p04(draw):
    cloud(draw, 850, 1380, 2.5, TW)
    for x, y, r in [(230, 320, 22), (1450, 280, 28), (1550, 650, 20), (260, 850, 18), (1500, 1050, 22)]:
        star(draw, x, y, r, r * 0.45, 5, TW)
    moon_crescent(draw, 1420, 400, 85, TW)
    lying(draw, 470, 1.1)


def p05(draw):
    cloud(draw, 260, 450, 1.0, TW)
    cloud(draw, 1420, 350, 1.1, TW)
    cloud(draw, 300, 1350, 0.9, TW)
    for x, y, r in [(1500, 1150, 22), (150, 850, 18), (1300, 1600, 20)]:
        star(draw, x, y, r, r * 0.45, 5, TW)
    flying(draw, 480, 780, 1.05)


def p06(draw):
    ground_line(draw, GROUND_Y)
    cx, base_y = 1280, 1480
    tip = (cx, base_y + 260)
    stroke_pts(draw, [tip, (cx - 95, base_y), (cx + 95, base_y)], TW + 3, closed=True)
    for k in (0.32, 0.55, 0.78):
        lx = tip[0] + (cx - 95 - tip[0]) * k
        rx = tip[0] + (cx + 95 - tip[0]) * k
        ly = tip[1] + (base_y - tip[1]) * k
        stroke_pts(draw, [(lx, ly), (rx, ly)], TW * 0.55)
    circle_o(draw, (cx, base_y - 95), 110, TW + 3)
    circle_o(draw, (cx - 65, base_y - 230), 85, TW + 3)
    stroke_pts(draw, [(cx - 35, base_y - 300), (cx - 12, base_y - 360), (cx + 8, base_y - 300)], TW, closed=True)
    for dx, dy in [(-45, -60), (35, -30), (-15, -140), (55, -170)]:
        dot(draw, (cx + dx, base_y + dy), 10)
    sitting(draw, 430, 1.0)


def p07(draw):
    ground_line(draw, GROUND_Y)
    heart(draw, 850, 700, 65, TW)
    heart(draw, 950, 620, 42, TW)
    heart(draw, 760, 600, 38, TW)
    standing(draw, 320, 0.85)
    standing(draw, 1000, 0.62, flip=True)


def p08(draw):
    ground_line(draw, GROUND_Y)
    cx, base_y = 1250, GROUND_Y - 20
    tiers = [(280, 130), (210, 120), (150, 110)]
    yy = base_y
    for w, h in tiers:
        stroke_pts(draw, [(cx - w / 2, yy), (cx + w / 2, yy), (cx + w / 2, yy - h), (cx - w / 2, yy - h)],
                   TW, closed=True)
        yy -= h
    for k in range(3):
        cxk = cx - 55 + k * 55
        stroke_pts(draw, [(cxk, yy), (cxk, yy - 65)], TW)
        stroke_pts(draw, [(cxk - 11, yy - 65), (cxk, yy - 95), (cxk + 11, yy - 65)], TW, closed=True)
    for x, y, c in [(230, 420, 85), (1560, 380, 95), (1520, 780, 75)]:
        balloon(draw, x, y, c * 0.7, 130, TW)
    for x, y in [(150, 800), (1620, 1050), (400, 300), (1300, 1550)]:
        star(draw, x, y, 20, 9, 5, TW * 0.7)
    sitting(draw, 420, 0.95)


def p09(draw):
    wave(draw, MARGIN, PAGE_W - MARGIN, 1930, 24, 5, TW)
    wave(draw, MARGIN, PAGE_W - MARGIN, 2000, 20, 6, TW)
    sun(draw, 1450, 300, 75, 10, TW)
    castle(draw, 1250, 1780, 0.5, TW)
    star(draw, 300, 1800, 40, 18, 5, TW)
    circle_o(draw, (400, 1840), 20, TW)
    circle_o(draw, (440, 1860), 14, TW)
    sitting(draw, 470, 0.95)


def p10(draw):
    ground_line(draw, GROUND_Y)
    tree(draw, 260, GROUND_Y, 1.5, TW)
    tree(draw, 1520, GROUND_Y, 1.8, TW)
    mushroom(draw, 1250, GROUND_Y - 20, 1.4, TW)
    mushroom(draw, 1380, GROUND_Y + 10, 0.9, TW)
    standing(draw, 470, 1.0)


def p11(draw):
    ground_line(draw, GROUND_Y)
    for x, y, r in [(260, GROUND_Y - 30, 110), (1480, GROUND_Y - 60, 130), (1560, GROUND_Y + 20, 75),
                    (190, GROUND_Y + 30, 70)]:
        flower(draw, x, y, r, 8, TW)
    for x, y in [(700, 650), (1050, 500), (900, 850)]:
        circle_o(draw, (x, y), 16, TW)
        stroke_pts(draw, [(x - 24, y), (x + 24, y)], TW * 0.6)
    standing(draw, 500, 1.0)


def p12(draw):
    ground_line(draw, GROUND_Y)
    moon_crescent(draw, 1380, 360, 120, TW)
    for x, y, r in [(230, 300, 22), (1550, 650, 26), (260, 850, 18), (1500, 1050, 20), (900, 280, 16)]:
        star(draw, x, y, r, r * 0.45, 5, TW)
    lying(draw, 470, 1.15)


def p13(draw):
    ground_line(draw, GROUND_Y)
    for cx, cy, s in [(1330, 1560, 1.0), (1560, 1620, 0.6)]:
        stroke_pts(draw, [(cx - 85 * s, cy + 240 * s), (cx - 35 * s, cy - 220 * s), (cx + 55 * s, cy - 260 * s),
                           (cx + 105 * s, cy + 240 * s)], TW, closed=True)
    for i in range(9):
        wave(draw, 1300, 1370, 1360 + i * 45, 10, 2, TW * 0.55)
    circle_o(draw, (1400, 2000), 170, TW * 0.6)
    standing(draw, 320, 0.82)


def p14(draw):
    for i in range(10):
        a = 2 * math.pi * i / 10
        heart(draw, 850 + 760 * math.cos(a), 1100 + 900 * math.sin(a), 32, TW * 0.7)
    bx, by = 1300, 720
    stroke_pts(draw, [(bx - 65, by), (bx, by - 38), (bx - 65, by - 76)], TW, closed=True)
    stroke_pts(draw, [(bx + 65, by), (bx, by - 38), (bx + 65, by - 76)], TW, closed=True)
    circle_o(draw, (bx, by - 38), 15, TW)
    U.draw_portrait(draw, 175, 425, 1.35)


def p15(draw):
    ground_line(draw, GROUND_Y)
    musical_note(draw, 1350, 550, 1.4, TW)
    musical_note(draw, 1520, 800, 1.1, TW)
    musical_note(draw, 1250, 950, 1.0, TW)
    sitting(draw, 430, 0.95)
    fx, fy = 900, 1280
    stroke_pts(draw, [(fx, fy), (fx + 260, fy - 40)], TW + 4)
    for k in range(4):
        dot(draw, (fx + 60 + k * 55, fy - 8 - k * 7), 8)


def p16(draw):
    ground_line(draw, GROUND_Y)
    tree(draw, 280, GROUND_Y, 1.3, TW)
    for x, y, r in [(230, 320, 26), (1500, 280, 30), (1400, 650, 22), (250, 850, 20),
                    (1550, 1050, 24), (900, 230, 18)]:
        snowflake(draw, x, y, r, TW * 0.7)
    wave(draw, MARGIN, PAGE_W - MARGIN, GROUND_Y + 60, 12, 8, TW * 0.6)
    standing(draw, 480, 0.95)


def p17(draw):
    ground_line(draw, GROUND_Y)
    tree(draw, 1250, GROUND_Y, 2.2, TW)
    for x, y in [(1150, GROUND_Y - 150), (1330, GROUND_Y - 110), (1420, GROUND_Y - 210), (1080, GROUND_Y - 80)]:
        circle_o(draw, (x, y), 26, TW)
    standing(draw, 460, 1.0)


def p18(draw):
    ground_line(draw, GROUND_Y)
    for cx, cy, s in [(1200, GROUND_Y - 10, 1.3), (1400, GROUND_Y + 30, 0.9), (1050, GROUND_Y + 50, 0.7)]:
        mushroom(draw, cx, cy, s, TW)
    flower(draw, 260, GROUND_Y - 10, 55, 6, TW)
    sitting(draw, 460, 0.95)


def p19(draw):
    for x, y, r in [(230, 320, 20), (1500, 280, 24), (300, 850, 16), (1550, 950, 22),
                    (900, 230, 14), (1250, 1450, 18), (200, 1350, 16)]:
        star(draw, x, y, r, r * 0.45, 5, TW)
    sx, sy = 1500, 320
    stroke_pts(draw, [(sx, sy), (sx - 240, sy + 170)], TW)
    for k in range(3):
        stroke_pts(draw, [(sx - 55 - k * 55, sy + 40 + k * 40), (sx - 82 - k * 55, sy + 18 + k * 40)], TW * 0.5)
    ground_line(draw, GROUND_Y)
    rearing(draw, 520, 0.95)


def p20(draw):
    ground_line(draw, GROUND_Y)
    for a in range(200, 341, 20):
        rad = math.radians(a)
        flower(draw, 700 + 250 * math.cos(rad), 380 + 190 * math.sin(rad), 32, 7, TW * 0.7)
    for x in range(MARGIN + 60, PAGE_W - MARGIN, 160):
        flower(draw, x, GROUND_Y + 40, 34, 7, TW * 0.7)
    standing(draw, 480, 1.0)


def p21(draw):
    ground_line(draw, GROUND_Y)
    for x, y, c in [(220, 420, 90), (1550, 370, 95), (280, 800, 75), (1500, 800, 85), (1580, 1150, 70)]:
        balloon(draw, x, y, c * 0.7, 150, TW)
    y0 = 190
    for x in range(MARGIN + 40, PAGE_W - MARGIN, 90):
        stroke_pts(draw, [(x, y0), (x + 45, y0 + 55), (x + 90, y0)], TW * 0.7)
    standing(draw, 480, 1.0)


def p22(draw):
    ground_line(draw, GROUND_Y)
    cx = 1280
    basins = [(cx, 1830, 220, 60), (cx, 1560, 150, 44), (cx, 1360, 85, 30)]
    for i, (bx, by, r, h) in enumerate(basins):
        ellipse_outline_rot(draw, bx, by, r, h, 0, TW)
        ellipse_outline_rot(draw, bx, by - h * 0.9, r * 0.82, h * 0.65, 0, TW * 0.6)
        if i > 0:
            px, py, pr, ph = basins[i - 1]
            stroke_pts(draw, [(bx - 16, by - h), (px - 16, py + ph)], TW)
            stroke_pts(draw, [(bx + 16, by - h), (px + 16, py + ph)], TW)
    circle_o(draw, (cx, basins[-1][1] - basins[-1][3] * 2.4), 20, TW)
    for bx, by, r, h in basins:
        for k in range(3):
            stroke_pts(draw, [(bx - r * 0.45, by - h * 0.55 + k * 14), (bx + r * 0.45, by - h * 0.55 + k * 14)],
                       TW * 0.4)
    standing(draw, 380, 0.72)


def p23(draw):
    ground_line(draw, GROUND_Y)
    butterfly(draw, 1300, 550, 1.1, TW)
    butterfly(draw, 1480, 820, 0.9, TW)
    butterfly(draw, 1200, 1050, 0.8, TW)
    heart(draw, 1500, 560, 38, TW)
    heart(draw, 1050, 460, 32, TW)
    rearing(draw, 470, 0.95)


def p24(draw):
    n = int((PAGE_W - 2 * MARGIN) / 20) + 1
    stroke_pts(draw, [(MARGIN + i * 20, GROUND_Y - 40 * math.sin(math.pi * i / n)) for i in range(n)], TW)
    sun(draw, 1420, GROUND_Y + 40, 100, 14, TW)
    bird_m(draw, 300, 380, 1.2, TW)
    bird_m(draw, 420, 440, 1.0, TW)
    bird_m(draw, 1500, 330, 1.1, TW)
    standing(draw, 470, 1.05)


PAGES = [
    (p01, "In the Meadow"), (p02, "Over the Rainbow"), (p03, "Castle Friend"),
    (p04, "Cloud Nap"), (p05, "Up, Up and Away"), (p06, "Ice Cream Treat"),
    (p07, "Best Friends"), (p08, "Happy Birthday"), (p09, "Seaside Fun"),
    (p10, "Forest Walk"), (p11, "Garden Blooms"), (p12, "Starry Night"),
    (p13, "Magic Waterfall"), (p14, "Pretty and Sweet"), (p15, "Little Tune"),
    (p16, "Snowy Day"), (p17, "Apple Orchard"), (p18, "Mushroom Ring"),
    (p19, "Wish Upon a Star"), (p20, "Flower Crown"), (p21, "Carnival Time"),
    (p22, "Magic Fountain"), (p23, "Dance Party"), (p24, "Good Morning"),
]

if __name__ == "__main__":
    for i, (fn, title) in enumerate(PAGES, start=1):
        img, draw = new_page()
        fn(draw)
        finish(img, draw, i, title)
        print("saved", i, title)
