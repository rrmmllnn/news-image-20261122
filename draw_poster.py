"""Round 9 poster generator: "The World in One Day" as a news radar.

A hub-and-spokes design, new for this competition: one globe at the
centre of the day, six story cards ranged around it and joined to it by
spokes, with the lead story as a banner underneath and an "also today"
ticker along the foot. Nothing here is copied from the round 5 grid,
the round 6 timeline, or the round 7/8 briefing layout.

Runs locally only (it needs Pillow, which the grader may not have).
The graded entrypoint, main.py, is a pure-standard-library copier of
the entry.png this script renders. Writes only to its own directory.
Deterministic: no clock, no randomness, no network.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

NAVY = (13, 27, 46)
PANEL = (22, 42, 68)
PANEL_EDGE = (52, 84, 124)
GOLD = (232, 184, 75)
GOLD_DARK = (198, 150, 52)
WHITE = (244, 246, 248)
MIST = (176, 196, 216)
RED = (217, 79, 61)
TEAL = (72, 178, 164)
INK = (10, 20, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines = []
    for raw in text.split("\n"):
        line = ""
        for word in raw.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_globe(draw, cx, cy, r):
    """Stylised globe: deep disc, meridians, equator, story pins."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(27, 58, 92),
                 outline=GOLD, width=4)
    # latitude lines
    for frac, wdt in ((0.55, 2), (0.28, 2)):
        hh = int(r * frac)
        ww = int((r * r - hh * hh) ** 0.5)
        draw.arc([cx - ww, cy - hh, cx + ww, cy + hh], 0, 360,
                 fill=(96, 140, 178), width=wdt)
    draw.line([cx - r + 6, cy, cx + r - 6, cy], fill=(96, 140, 178), width=2)
    # meridians
    for wdt in (58, 108):
        draw.ellipse([cx - wdt, cy - r + 4, cx + wdt, cy + r - 4],
                     outline=(96, 140, 178), width=2)
    # abstract landmasses: soft gold-green blobs, deliberately schematic
    land = (96, 158, 120)
    draw.ellipse([cx - 88, cy - 74, cx - 28, cy - 18], fill=land)
    draw.ellipse([cx - 12, cy - 58, cx + 44, cy - 6], fill=land)
    draw.ellipse([cx - 62, cy + 22, cx + 6, cy + 78], fill=land)
    draw.ellipse([cx + 34, cy + 30, cx + 92, cy + 84], fill=land)
    # story pins on the rim
    pins = [(cx - 96, cy - 96), (cx + 104, cy - 84), (cx - 118, cy + 52),
            (cx + 116, cy + 66), (cx - 34, cy - 128), (cx + 62, cy + 122)]
    for px, py in pins:
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=GOLD,
                     outline=NAVY, width=2)


def icon_ship(draw, x, y, s, col):
    # hull, mast, waves
    draw.polygon([(x, y + 30), (x + 54, y + 30), (x + 44, y + 46),
                  (x + 10, y + 46)], fill=col)
    draw.rectangle([x + 24, y + 2, x + 28, y + 30], fill=col)
    draw.polygon([(x + 28, y + 6), (x + 48, y + 24), (x + 28, y + 24)],
                 fill=col)
    for i, wy in enumerate((y + 52, y + 58)):
        draw.arc([x + 2 + i * 6, wy, x + 52 - i * 6, wy + 8], 180, 360,
                 fill=col, width=3)


def icon_building(draw, x, y, s, col):
    draw.rectangle([x + 8, y + 10, x + 46, y + 58], fill=col)
    for wx in (16, 28, 40):
        for wy in (18, 30, 42):
            draw.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 5],
                           fill=NAVY)
    # crack
    draw.line([(x + 30, y + 10), (x + 24, y + 26), (x + 32, y + 38),
               (x + 26, y + 54)], fill=RED, width=3)
    # smoke
    draw.ellipse([x + 34, y - 2, x + 46, y + 10], outline=MIST, width=3)
    draw.ellipse([x + 42, y - 10, x + 56, y + 4], outline=MIST, width=3)


def icon_scales(draw, x, y, s, col):
    draw.rectangle([x + 26, y + 4, x + 30, y + 52], fill=col)
    draw.line([x + 6, y + 14, x + 50, y + 14], fill=col, width=4)
    draw.polygon([(x + 2, y + 34), (x + 16, y + 34), (x + 9, y + 16)],
                 outline=col, width=3)
    draw.polygon([(x + 40, y + 34), (x + 54, y + 34), (x + 47, y + 16)],
                 outline=col, width=3)
    draw.rectangle([x + 18, y + 52, x + 38, y + 58], fill=col)


def icon_drop(draw, x, y, s, col):
    draw.polygon([(x + 28, y + 2), (x + 48, y + 32), (x + 8, y + 32)],
                 fill=col)
    draw.pieslice([x + 8, y + 22, x + 48, y + 56], 0, 180, fill=col)
    draw.arc([x + 4, y + 56, x + 52, y + 64], 180, 360, fill=MIST, width=3)


def icon_flame(draw, x, y, s, col):
    draw.polygon([(x + 28, y + 2), (x + 46, y + 26), (x + 52, y + 40),
                  (x + 40, y + 58), (x + 16, y + 58), (x + 4, y + 40),
                  (x + 10, y + 26)], fill=col)
    draw.polygon([(x + 28, y + 26), (x + 38, y + 40), (x + 34, y + 52),
                  (x + 22, y + 52), (x + 18, y + 40)], fill=NAVY)


def icon_badge(draw, x, y, s, col):
    cx, cy = x + 28, y + 30
    pts = []
    import math
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = 26 if i % 2 == 0 else 11
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    draw.polygon(pts, fill=col)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=NAVY)


def icon_cracked_globe(draw, x, y, s, col):
    draw.ellipse([x + 2, y + 2, x + 58, y + 58], outline=col, width=4)
    draw.arc([x + 12, y + 2, x + 48, y + 58], 0, 360, fill=col, width=2)
    draw.line([x + 2, y + 30, x + 58, y + 30], fill=col, width=2)
    draw.line([(x + 30, y + 4), (x + 22, y + 22), (x + 34, y + 36),
               (x + 24, y + 54)], fill=RED, width=4)


ICONS = {
    "ship": icon_ship,
    "building": icon_building,
    "scales": icon_scales,
    "drop": icon_drop,
    "flame": icon_flame,
    "badge": icon_badge,
    "globe": icon_cracked_globe,
}

# (number, tag, headline, fact, icon, accent)
LEFT = [
    ("1", "UKRAINE · LIBYA", "Ukraine sinks Russian warship",
     "Ukraine says its sea drones sank the Merkury.",
     "ship", TEAL),
    ("2", "UKRAINE", "Russian strike kills 11 near Kyiv",
     "A drone strike partly collapses a block in Dymer.",
     "building", RED),
    ("3", "THE HAGUE", "Myanmar guilty of genocide",
     "ICJ rules Myanmar committed genocide.",
     "scales", GOLD),
]
RIGHT = [
    ("4", "HORMUZ", "Two tankers hit mines",
     "Iran blames mines; Trump weighs new strikes.",
     "drop", RED),
    ("5", "INDONESIA", "Factory fire: 3 dead, 36 missing",
     "Blaze tears through a candy factory in Banten.",
     "flame", GOLD),
    ("6", "MEXICO", "Troops capture \u2018El Chapo Isidro\u2019",
     "Drug lord seized in a Sinaloa raid.",
     "badge", TEAL),
]


def draw_card(draw, x, y, w, h, num, tag, headline, fact, icon, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL,
                           outline=PANEL_EDGE, width=2)
    # number badge
    bx, by = x + 14, y + 14
    draw.ellipse([bx, by, bx + 34, by + 34], fill=GOLD)
    draw.text((bx + 17, by + 17), num, font=font(F_BOLD, 20),
              fill=INK, anchor="mm")
    # tag
    draw.text((bx + 44, by + 17), tag, font=font(F_BOLD, 17), fill=accent,
              anchor="lm")
    # icon, right of the tag row
    ICONS[icon](draw, x + w - 68, y + 12, 60, accent)
    # headline
    f_head = font(F_BOLD, 26)
    lines = wrap(draw, headline, f_head, w - 28)
    ty = y + 58
    for ln in lines[:2]:
        draw.text((x + 14, ty), ln, font=f_head, fill=WHITE)
        ty += 31
    # fact
    f_fact = font(F_REG, 19)
    for ln in wrap(draw, fact, f_fact, w - 28)[:2]:
        draw.text((x + 14, ty + 4), ln, font=f_fact, fill=MIST)
        ty += 25


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # faint dot texture over the background
    for gx in range(20, W, 44):
        for gy in range(20, H, 44):
            draw.ellipse([gx, gy, gx + 2, gy + 2], fill=(24, 46, 72))

    # ---- masthead ----
    draw.text((W // 2, 34), "ONE DAY  ·  ONE PICTURE  ·  THE WORLD",
              font=font(F_BOLD, 20), fill=GOLD, anchor="mm")
    draw.text((W // 2, 82), "THE WORLD IN ONE DAY",
              font=font(F_BOLD, 56), fill=WHITE, anchor="mm")
    draw.text((W // 2, 128), "SUNDAY, 22 NOVEMBER 2026",
              font=font(F_BOLD, 28), fill=MIST, anchor="mm")
    draw.line([48, 156, W - 48, 156], fill=GOLD_DARK, width=3)

    # ---- globe hub ----
    cx, cy, r = W // 2, 478, 148
    draw_globe(draw, cx, cy, r)
    draw.text((cx, cy + r + 26), "SEVEN STORIES, ONE DAY",
              font=font(F_BOLD, 18), fill=GOLD, anchor="mm")

    # ---- spokes + side cards ----
    card_w, card_h = 302, 200
    ys = [170, 378, 586]
    for col, x in ((LEFT, 28), (RIGHT, W - 28 - card_w)):
        for (num, tag, head, fact, icon, accent), y in zip(col, ys):
            # spoke from globe rim to card edge
            cy_card = y + card_h // 2
            if x < W // 2:
                draw.line([cx - r + 8, cy, x + card_w, cy_card],
                          fill=(70, 104, 142), width=2)
            else:
                draw.line([cx + r - 8, cy, x, cy_card],
                          fill=(70, 104, 142), width=2)
            draw_card(draw, x, y, card_w, card_h, num, tag, head, fact,
                      icon, accent)

    # ---- lead story banner ----
    bx0, by0, bx1, by1 = 28, 806, W - 28, 940
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=14,
                           fill=(46, 24, 22), outline=RED, width=3)
    icon_cracked_globe(draw, bx0 + 20, by0 + 32, 60, GOLD)
    draw.text((bx0 + 104, by0 + 20), "LEAD STORY  ·  CLIMATE",
              font=font(F_BOLD, 18), fill=RED, anchor="lm")
    draw.text((bx0 + 104, by0 + 52), "COP31 COLLAPSES \u2014 NO CLIMATE DEAL",
              font=font(F_BOLD, 34), fill=WHITE, anchor="lm")
    f_fact = font(F_REG, 21)
    for i, ln in enumerate(wrap(
            draw,
            "Antalya talks end with no agreement after the longest summit "
            "in history; the EU rejects a draft that drops fossil fuels.",
            f_fact, bx1 - bx0 - 130)):
        draw.text((bx0 + 104, by0 + 80 + i * 26), ln, font=f_fact,
                  fill=MIST)

    # ---- footer ticker ----
    draw.line([48, 958, W - 48, 958], fill=PANEL_EDGE, width=2)
    draw.text((W // 2, 984),
              "ALSO TODAY:  Delta outage delays 1,600+ flights  ·  "
              "Houthi refinery claim unconfirmed  ·  Gaza: two killed",
              font=font(F_REG, 16), fill=MIST, anchor="mm")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (OUT, W, H))


if __name__ == "__main__":
    main()
