import math
import os
from PIL import Image, ImageDraw, ImageFont
from drawlib import bezier4, arc_pts, PAGE_W, PAGE_H, MARGIN

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
TITLE_FONT = ImageFont.truetype(f"{FONT_DIR}/EricaOne-Regular.ttf", 150)
SUB_FONT = ImageFont.truetype(f"{FONT_DIR}/EricaOne-Regular.ttf", 62)
BADGE_FONT = ImageFont.truetype(f"{FONT_DIR}/Outfit-Bold.ttf", 34)
BLURB_FONT = ImageFont.truetype(f"{FONT_DIR}/Outfit-Regular.ttf", 40)
BLURB_BOLD = ImageFont.truetype(f"{FONT_DIR}/Outfit-Bold.ttf", 46)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "book", "cover")
os.makedirs(OUT_DIR, exist_ok=True)

SKY = (191, 227, 255)
GRASS = (196, 232, 172)
INK = (46, 40, 74)
CREAM = (255, 250, 240)
GOLD = (250, 200, 60)
PASTELS = [(255, 179, 186), (255, 223, 186), (255, 255, 186), (186, 255, 201), (186, 225, 255), (216, 186, 255)]


def leaf_fill(draw, p0, p1, bulge, color, outline=INK, width=5):
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    nx, ny = -dy, dx
    ln = math.hypot(nx, ny) or 1
    nx, ny = nx / ln, ny / ln
    c1 = (mx + nx * bulge, my + ny * bulge)
    c2 = (mx - nx * bulge, my - ny * bulge)
    pts = bezier4(p0, c1, c1, p1, 16) + bezier4(p1, c2, c2, p0, 16)
    draw.polygon(pts, fill=color, outline=outline, width=width)


def flower_fill(draw, cx, cy, r, petals, petal_color, center_color=GOLD):
    for i in range(petals):
        a = 2 * math.pi * i / petals
        tip = (cx + r * math.cos(a), cy + r * math.sin(a))
        leaf_fill(draw, (cx, cy), tip, r * 0.45, petal_color, outline=INK, width=3)
    draw.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3], fill=center_color, outline=INK, width=3)


def cloud_fill(draw, cx, cy, scale):
    r = scale * 55
    for dx, dy, k in [(-1.1, 0.1, 0.55), (-0.5, -0.35, 0.72), (0.15, -0.45, 0.78), (0.85, -0.15, 0.62), (1.25, 0.15, 0.48)]:
        draw.ellipse([cx + dx * r * 2 - k * r, cy + dy * r * 2 - k * r, cx + dx * r * 2 + k * r, cy + dy * r * 2 + k * r],
                     fill="white", outline=INK, width=4)


def rainbow_fill(draw, cx, cy, r_out, band_w):
    for i, col in enumerate(PASTELS):
        r = r_out - i * band_w
        bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.pieslice(bbox, 180, 360, fill=col, outline=None)
    draw.arc([cx - r_out, cy - r_out, cx + r_out, cy + r_out], 180, 360, fill=INK, width=5)
    inner = r_out - len(PASTELS) * band_w
    draw.arc([cx - inner, cy - inner, cx + inner, cy + inner], 180, 360, fill=INK, width=5)
    draw.line([(cx - r_out, cy), (cx - inner, cy)], fill=INK, width=5)
    draw.line([(cx + r_out, cy), (cx + inner, cy)], fill=INK, width=5)


def unicorn_color(draw, cx, cy, scale, mirror=1):
    def P(x, y):
        return (cx + mirror * x * scale, cy + y * scale)

    bx0, by0 = P(-235, -170)
    bx1, by1 = P(235, 170)
    draw.ellipse([min(bx0, bx1), min(by0, by1), max(bx0, bx1), max(by0, by1)], fill=CREAM, outline=INK, width=7)
    for hip, hoof in [(P(-160, 145), P(-175, 260)), (P(-90, 160), P(-95, 270)),
                      (P(115, 160), P(125, 270)), (P(180, 145), P(210, 260))]:
        draw.line([hip, hoof], fill=CREAM, width=int(34 * scale))
        draw.line([hip, hoof], fill=INK, width=int(34 * scale) + 6)
        draw.line([hip, hoof], fill=CREAM, width=int(34 * scale))
        draw.ellipse([hoof[0] - 24 * scale, hoof[1] - 15 * scale, hoof[0] + 24 * scale, hoof[1] + 15 * scale],
                     fill=(90, 70, 60), outline=INK, width=4)
    hx, hy, hr = 190, -220, 150 * scale
    head_c = (cx + mirror * hx * scale, cy + hy * scale)
    for i, (dx, dy) in enumerate([(-40, -145), (0, -95), (45, -35), (85, 25), (110, 90), (100, 150)]):
        col = PASTELS[i % len(PASTELS)]
        pcx, pcy = head_c[0] + mirror * dx * scale, head_c[1] + dy * scale
        draw.ellipse([pcx - 46 * scale, pcy - 46 * scale, pcx + 46 * scale, pcy + 46 * scale],
                     fill=col, outline=INK, width=4)
    for i, (dx, dy) in enumerate([(-260, 120), (-300, 190), (-290, 260)]):
        col = PASTELS[(i + 2) % len(PASTELS)]
        pcx, pcy = cx + mirror * dx * scale, cy + dy * scale
        draw.ellipse([pcx - 38 * scale, pcy - 38 * scale, pcx + 38 * scale, pcy + 38 * scale],
                     fill=col, outline=INK, width=4)
    draw.ellipse([head_c[0] - hr, head_c[1] - hr, head_c[0] + hr, head_c[1] + hr], fill=CREAM, outline=INK, width=7)
    mx, my = head_c[0] + mirror * hr * 1.0, head_c[1] + hr * 0.3
    draw.ellipse([mx - 54 * scale, my - 38 * scale, mx + 54 * scale, my + 38 * scale], fill=CREAM, outline=INK, width=5)
    draw.ellipse([mx + mirror * 26 * scale - 6 * scale, my - 6 * scale, mx + mirror * 26 * scale + 6 * scale, my + 6 * scale],
                 fill=INK)
    ex, ey = head_c[0] + mirror * hr * 0.3, head_c[1] - hr * 0.05
    draw.ellipse([ex - 22 * scale, ey - 22 * scale, ex + 22 * scale, ey + 22 * scale], fill="white", outline=INK, width=5)
    draw.ellipse([ex + mirror * 5 * scale - 12 * scale, ey + 4 * scale - 12 * scale,
                  ex + mirror * 5 * scale + 12 * scale, ey + 4 * scale + 12 * scale], fill=INK)
    for dxx in (-13, 2, 17):
        p0 = (ex + mirror * dxx * scale, ey - 20 * scale)
        p1 = (ex + mirror * dxx * 1.3 * scale, ey - 34 * scale)
        draw.line([p0, p1], fill=INK, width=4)
    ear_a = (head_c[0] - mirror * hr * 0.35, head_c[1] - hr * 0.82)
    leaf_fill(draw, ear_a, (ear_a[0] - mirror * hr * 0.28, ear_a[1] - hr * 0.55), hr * 0.16, CREAM)
    ear_b = (head_c[0] + mirror * hr * 0.18, head_c[1] - hr * 0.92)
    leaf_fill(draw, ear_b, (ear_b[0] - mirror * hr * 0.10, ear_b[1] - hr * 0.55), hr * 0.16, CREAM)
    hb_l = (head_c[0] + mirror * hr * 0.28, head_c[1] - hr * 0.86)
    hb_r = (head_c[0] + mirror * hr * 0.62, head_c[1] - hr * 0.80)
    h_tip = (head_c[0] + mirror * hr * 0.46, head_c[1] - hr * 1.68)
    draw.polygon([hb_l, h_tip, hb_r], fill=GOLD, outline=INK, width=6)
    for k in (0.32, 0.58):
        a1 = (hb_l[0] + (h_tip[0] - hb_l[0]) * k - mirror * hr * 0.05, hb_l[1] + (h_tip[1] - hb_l[1]) * k)
        a2 = (hb_r[0] + (h_tip[0] - hb_r[0]) * k + mirror * hr * 0.05, hb_r[1] + (h_tip[1] - hb_r[1]) * k)
        draw.line([a1, a2], fill="white", width=5)


def text_with_outline(draw, xy, text, font, fill, outline, width, anchor=None):
    draw.text(xy, text, font=font, fill=fill, stroke_width=width, stroke_fill=outline, anchor=anchor)


def front_cover():
    img = Image.new("RGB", (PAGE_W, PAGE_H), SKY)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 1620, PAGE_W, PAGE_H], fill=GRASS)
    draw.ellipse([-180, 1550, 220, 1700], fill=(170, 218, 148))
    draw.ellipse([1450, 1600, 1900, 1780], fill=(170, 218, 148))
    draw.ellipse([1420, -120, 1680, 140], fill=(255, 232, 150))
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        p0 = (1550 + 160 * math.cos(a), 10 + 160 * math.sin(a))
        p1 = (1550 + 210 * math.cos(a), 10 + 210 * math.sin(a))
        draw.line([p0, p1], fill=(255, 232, 150), width=10)
    cloud_fill(draw, 230, 260, 1.1)
    cloud_fill(draw, 1500, 430, 0.85)
    rainbow_fill(draw, 850, 1120, 560, 34)
    for x, y, r, col in [(150, 1780, 42, PASTELS[0]), (1560, 1750, 46, PASTELS[3]),
                          (1500, 2020, 36, PASTELS[5]), (120, 2020, 40, PASTELS[2]),
                          (1640, 1900, 30, PASTELS[1])]:
        flower_fill(draw, x, y, r, 6, col)
    unicorn_color(draw, 850, 1520, 1.55)
    text_with_outline(draw, (850, 210), "UNICORN", TITLE_FONT, (140, 60, 150), "white", 14, anchor="mm")
    text_with_outline(draw, (850, 345), "COLORING BOOK", SUB_FONT, INK, "white", 10, anchor="mm")
    badge_c = (1470, 940)
    draw.ellipse([badge_c[0] - 130, badge_c[1] - 130, badge_c[0] + 130, badge_c[1] + 130],
                 fill=(255, 235, 140), outline=INK, width=6)
    draw.text((badge_c[0], badge_c[1] - 26), "24 PAGES", font=BADGE_FONT, fill=INK, anchor="mm")
    draw.text((badge_c[0], badge_c[1] + 22), "AGES 4-8", font=BADGE_FONT, fill=INK, anchor="mm")
    img.save(os.path.join(OUT_DIR, "front_cover.png"))
    return img


def back_cover():
    img = Image.new("RGB", (PAGE_W, PAGE_H), SKY)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 1780, PAGE_W, PAGE_H], fill=GRASS)
    cloud_fill(draw, 220, 220, 0.75)
    cloud_fill(draw, 1480, 260, 0.65)
    for x, y, r, col in [(140, 1900, 30, PASTELS[4]), (1560, 1900, 34, PASTELS[0])]:
        flower_fill(draw, x, y, r, 6, col)
    unicorn_color(draw, 300, 1780, 0.62, mirror=-1)

    text_with_outline(draw, (850, 260), "A Magical Coloring Adventure", SUB_FONT, (140, 60, 150), "white", 8, anchor="mm")

    blurb = [
        "Twenty-four sweet, single-sided unicorn designs —",
        "rainbows, castles, clouds, and more — made for",
        "little hands and big imaginations.",
        "",
        "Bold, simple lines are perfect for crayons,",
        "markers, or colored pencils.",
    ]
    y = 480
    for line in blurb:
        draw.text((850, y), line, font=BLURB_FONT, fill=INK, anchor="mm")
        y += 66

    y += 30
    for label in ["24 original designs", "Printed single-sided", "Ages 4-8"]:
        draw.ellipse([560, y - 14, 588, y + 14], fill=(140, 60, 150))
        draw.text((615, y), label, font=BLURB_BOLD, fill=INK, anchor="lm")
        y += 70

    # Reserved quiet zone for the KDP-generated ISBN barcode (leave blank).
    img.save(os.path.join(OUT_DIR, "back_cover.png"))
    return img


if __name__ == "__main__":
    front_cover()
    back_cover()
    print("cover saved")
