# -*- coding: utf-8 -*-
"""Generate Selector Casino favicon pack."""
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BG = (31, 41, 55)
ACCENT = (20, 109, 245)
ACCENT2 = (45, 140, 255)


def draw_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), BG + (255,))
    d = ImageDraw.Draw(img)
    pad = max(2, int(size * 0.08))
    box = (pad, pad, size - pad - 1, size - pad - 1)
    d.rounded_rectangle(box, radius=max(4, size // 6), fill=ACCENT2)
    inner = (pad + size // 10, pad + size // 10, size - pad - size // 10, size - pad - size // 10)
    d.rounded_rectangle(inner, radius=max(3, size // 8), fill=BG + (255,))
    try:
        font = ImageFont.truetype("segoeui.ttf", max(10, int(size * 0.52)))
    except OSError:
        try:
            font = ImageFont.truetype("arial.ttf", max(10, int(size * 0.52)))
        except OSError:
            font = ImageFont.load_default()
    text = "S"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2
    y = (size - th) // 2 - max(1, size // 32)
    d.text((x + 1, y + 1), text, fill=(0, 0, 0, 120), font=font)
    d.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    return img.convert("RGB")


def main():
    icons_dir = ROOT / "assets" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    source = draw_icon(512)
    source.save(icons_dir / "favicon-source.png", "PNG")

    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "apple-touch-icon.png": 180,
        "android-chrome-192x192.png": 192,
        "android-chrome-512x512.png": 512,
    }
    for name, s in sizes.items():
        draw_icon(s).save(ROOT / name, "PNG")

    ico_sizes = [(16, 16), (32, 32), (48, 48)]
    imgs = [draw_icon(s).convert("RGBA") for _, s in ico_sizes]
    imgs[0].save(ROOT / "favicon.ico", format="ICO", sizes=ico_sizes)
    print("Favicon pack OK:", ROOT)


if __name__ == "__main__":
    main()
