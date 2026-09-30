#!/usr/bin/env python3
"""Regenerate the black-and-white pixel avatar, favicon and link-preview card.

The avatar is drawn as text: '#' is black, '.' is white, ':' is a 50%
checkerboard dither. Only the left half is written out; it is mirrored to
make the face symmetric. Edit AVATAR_LEFT and re-run.
Requires Pillow: pip install pillow
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public/assets/img/avatar"

AVATAR_LEFT = """
................
................
...........#####
.........#######
........########
.......#########
......##########
......###.#.##.#
.....###........
.....##.........
....####........
...###..........
..####..........
..#::#.#########
..#::#.#..######
..#::#.#.#######
..#::#..#######.
..####..........
...##...........
.....#..........
......#.........
......#.........
.......#.....###
........##......
..........###...
............####
..........####::
......#####::::#
....##::::::::::
...#::::::::::::
..#:::::::::::::
..##############
"""


def draw_avatar():
    left = [r.ljust(16, ".")[:16] for r in AVATAR_LEFT.strip("\n").split("\n")]
    grid = [r + r[::-1] for r in left]
    grid[19] = grid[19][:15] + "##" + grid[19][17:]  # nose
    im = Image.new("RGB", (32, 32), "white")
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "#" or (c == ":" and (x + y) % 2 == 0):
                im.putpixel((x, y), (0, 0, 0))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    im = draw_avatar()
    im.resize((320, 320), Image.NEAREST).save(OUT / "avatar.png", optimize=True)
    for s in (16, 32, 48, 180, 192, 512):
        im.resize((s, s), Image.NEAREST).save(OUT / f"avatar-{s}.png", optimize=True)
    im.resize((48, 48), Image.NEAREST).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    og = Image.new("RGB", (1200, 630), "white")
    og.paste(im.resize((448, 448), Image.NEAREST), (80, 91))
    d = ImageDraw.Draw(og)
    bold = ImageFont.truetype("DejaVuSansMono-Bold.ttf", 54)
    mono = ImageFont.truetype("DejaVuSansMono.ttf", 26)
    d.rectangle((20, 20, 1179, 609), outline="black", width=4)
    d.text((590, 180), "NITHIN JAMBULA", font=bold, fill="black")
    lines = ["> robotics software", "> agentic AI systems", "> architecture & infra", "", "nithin434.github.io"]
    for i, t in enumerate(lines):
        d.text((590, 280 + i * 42), t, font=mono, fill="black")
    og.save(OUT / "og-image.jpg", quality=90)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
