#!/usr/bin/env python3
"""Make web-sized copies of gallery photos.

Reads full-size images from public/assets/img/photos/originals/ and writes
800px (longest side) JPEGs to public/assets/img/photos/. Files that are
already up to date are skipped. Requires Pillow: pip install pillow
"""
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public/assets/img/photos/originals"
DST = ROOT / "public/assets/img/photos"
MAX_SIDE = 800
EXTS = {".jpg", ".jpeg", ".png", ".webp"}

for src in sorted(SRC.iterdir()):
    if src.suffix.lower() not in EXTS or src.stem.startswith("profile-image"):
        continue
    dst = DST / f"{src.stem}.jpg"
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        continue
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((MAX_SIDE, MAX_SIDE))
    im.save(dst, quality=82, optimize=True)
    print(f"{dst.relative_to(ROOT)}  {im.width}x{im.height}  (use these as width/height in the <img> tag)")
