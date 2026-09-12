import os
import shutil
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
PAGES_DIR = os.path.join(ROOT, "book", "pages")
COVER_DIR = os.path.join(ROOT, "book", "cover")
OUT_DIR = os.path.join(ROOT, "output")
os.makedirs(OUT_DIR, exist_ok=True)

DPI = 200


def load(path):
    return Image.open(path).convert("RGB")


def build_interior():
    title = Image.new("RGB", (1700, 2200), "white")
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(title)
    font_dir = "/mnt/skills/examples/canvas-design/canvas-fonts"
    big = ImageFont.truetype(f"{font_dir}/EricaOne-Regular.ttf", 110)
    small = ImageFont.truetype(f"{font_dir}/EricaOne-Regular.ttf", 48)
    tiny = ImageFont.truetype(f"{font_dir}/Outfit-Regular.ttf", 34)
    d.text((850, 900), "Unicorn Party", font=big, fill="black", anchor="mm")
    d.text((850, 1030), "A Coloring Book", font=small, fill="black", anchor="mm")
    d.text((850, 1150), "24 Magical Pages", font=tiny, fill="black", anchor="mm")

    pages = [title]
    blank = Image.new("RGB", (1700, 2200), "white")
    for i in range(1, 25):
        pages.append(load(os.path.join(PAGES_DIR, f"page_{i:02d}.png")))
        pages.append(blank.copy())

    out_path = os.path.join(OUT_DIR, "Unicorn-Coloring-Book-Interior.pdf")
    pages[0].save(out_path, save_all=True, append_images=pages[1:], resolution=DPI)
    print("wrote", out_path, "pages:", len(pages))
    return len(pages)


def build_cover_preview():
    front = load(os.path.join(COVER_DIR, "front_cover.png"))
    back = load(os.path.join(COVER_DIR, "back_cover.png"))
    out_path = os.path.join(OUT_DIR, "Unicorn-Coloring-Book-Cover-Preview.pdf")
    back.save(out_path, save_all=True, append_images=[front], resolution=DPI)
    print("wrote", out_path)
    shutil.copy(os.path.join(COVER_DIR, "front_cover.png"),
                os.path.join(OUT_DIR, "Unicorn-Coloring-Book-FrontCover.png"))
    shutil.copy(os.path.join(COVER_DIR, "back_cover.png"),
                os.path.join(OUT_DIR, "Unicorn-Coloring-Book-BackCover.png"))


if __name__ == "__main__":
    n = build_interior()
    build_cover_preview()
    with open(os.path.join(OUT_DIR, "PAGE_COUNT.txt"), "w") as f:
        f.write(str(n))
    print("done, interior page count:", n)
