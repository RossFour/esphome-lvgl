"""Rotate slideshow photo for ESPHome display screensaver.

Picks a random image from /config/www/photos/, crops and resizes it
to 1060x470 (center crop, no letterboxing), and saves as PNG.

Uses Pillow which ships with Home Assistant — no extra installs needed.

Place this file at: /config/scripts/rotate_slideshow.py
"""

import random
from pathlib import Path
from PIL import Image

PHOTO_DIR = Path("/config/www/photos")
OUTPUT = Path("/config/www/slideshow/current.png")
TARGET_W, TARGET_H = 1024, 600


def crop_and_resize(img: Image.Image) -> Image.Image:
    """Center-crop to target aspect ratio, then resize."""
    src_w, src_h = img.size
    target_ratio = TARGET_W / TARGET_H
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # Source is wider — crop sides
        new_w = int(src_h * target_ratio)
        offset = (src_w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, src_h))
    else:
        # Source is taller — crop top/bottom
        new_h = int(src_w / target_ratio)
        offset = (src_h - new_h) // 2
        img = img.crop((0, offset, src_w, offset + new_h))

    return img.resize((TARGET_W, TARGET_H), Image.LANCZOS)


def main():
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    photos = [
        p for p in PHOTO_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in extensions
    ]

    if not photos:
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    chosen = random.choice(photos)
    img = Image.open(chosen)
    img = img.convert("RGB")  # Strip alpha, handle palette images
    img = crop_and_resize(img)
    img.save(OUTPUT, format="PNG")


if __name__ == "__main__":
    main()
