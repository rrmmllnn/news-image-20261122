#!/usr/bin/env python3
"""Round 6 poster: 'The World in One Day' - a lead story plus a vertical
timeline spine. Draws Sunday 22 November 2026 world news with Pillow only.
Deterministic: fixed colours, fonts, geometry and text; no randomness,
no network, no timestamps in the image."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 242, 232)
INK = (27, 38, 63)
NAVY = (20, 38, 63)
NAVY2 = (28, 52, 84)
GOLD = (201, 162, 61)
GOLD_LT = (232, 196, 106)
RED = (178, 44, 36)
RED_LT = (226, 93, 76)
TEAL = (43, 122, 120)
TEAL_LT = (120, 190, 186)
CARD = (255, 255, 255)
GREY = (92, 102, 118)
LINE = (214, 205, 188)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL, outline=INK, width=4)
    draw.ellipse([cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9], outline=GOLD, width=3)
    draw.ellipse([cx - 52, cy - 48, cx - 6, cy - 8], fill=(86, 158, 110))
    draw.ellipse([cx + 4, cy + 6, cx + 56, cy + 44], fill=(86, 158, 110))
    draw.ellipse([cx - 30, cy + 34, cx + 8, cy + 62], fill=(86, 158, 110))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=TEAL_LT, width=3)
    crack = [(cx - 58, cy - 62), (cx - 30, cy - 28), (cx - 52, cy - 2),
             (cx - 14, cy + 22), (cx - 38, cy + 48), (cx - 6, cy + 70)]
    draw.line(crack, fill=RED, width=6, joint="curve")
    draw.line(crack, fill=(255, 255, 255), width=2, joint="curve")


def draw_icon(draw, kind, cx, cy, accent):
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=accent, outline=INK, width=2)
    if kind == "ship":
        draw.polygon([(cx - 16, cy + 4), (cx + 16, cy + 4), (cx + 10, cy + 14),
                      (cx - 10, cy + 14)], fill=(255, 255, 255))
        draw.line([(cx, cy + 4), (cx, cy - 14)], fill=(255, 255, 255), width=3)
        draw.polygon([(cx, cy - 14), (cx + 11, cy - 6), (cx, cy - 6)], fill=GOLD_LT)
        draw.ellipse([cx - 14, cy - 18, cx - 8, cy - 12], fill=(255, 255, 255))
        draw.ellipse([cx + 6, cy - 20, cx + 12, cy - 14], fill=(255, 255, 255))
    elif kind == "flats":
        draw.rectangle([cx - 15, cy - 12, cx - 1, cy + 14], fill=(255, 255, 255))
        draw.rectangle([cx + 2, cy - 16, cx + 15, cy + 14], fill=(233, 230, 220))
        draw.polygon([(cx - 15, cy - 12), (cx - 1, cy - 12), (cx - 8, cy - 20)],
                     fill=RED_LT)
        for bx in (-11, -4, 6, 11):
            for by in (-6, 2, 9):
                draw.rectangle([cx + bx, cy + by, cx + bx + 3, cy + by + 3],
                               fill=INK)
    elif kind == "burst":
        pts = []
        import math
        for i in range(16):
            ang = math.pi * i / 8
            rad = 17 if i % 2 == 0 else 7
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        draw.polygon(pts, fill=GOLD_LT, outline=INK)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    elif kind == "flame":
        draw.polygon([(cx, cy - 18), (cx + 9, cy - 4), (cx + 13, cy + 6),
                      (cx + 6, cy + 15), (cx - 6, cy + 15), (cx - 13, cy + 6),
                      (cx - 9, cy - 4)], fill=(240, 120, 40))
        draw.polygon([(cx, cy - 6), (cx + 6, cy + 4), (cx + 3, cy + 12),
                      (cx - 3, cy + 12), (cx - 6, cy + 4)], fill=GOLD_LT)
    elif kind == "boat":
        draw.polygon([(cx - 17, cy + 2), (cx + 17, cy + 2), (cx + 11, cy + 13),
                      (cx - 11, cy + 13)], fill=(255, 255, 255))
        draw.line([(cx, cy + 2), (cx, cy - 13)], fill=(255, 255, 255), width=3)
        draw.polygon([(cx, cy - 13), (cx + 10, cy - 5), (cx, cy - 5)], fill=GOLD_LT)
        draw.arc([cx - 20, cy + 12, cx - 2, cy + 24], 0, 180, fill=TEAL_LT, width=3)
        draw.arc([cx + 2, cy + 12, cx + 20, cy + 24], 0, 180, fill=TEAL_LT, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_title = font(FB, 52)
    f_date = font(FB, 25)
    f_kick = font(FB, 19)
    f_hero = font(FB, 41)
    f_hero2 = font(FB, 30)
    f_body = font(FR, 20)
    f_tag = font(FB, 19)
    f_head = font(FB, 22)
    f_sum = font(FR, 16)
    f_foot = font(FR, 15)
    f_sec = font(FB, 20)

    # ---- banner ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 124], fill=GOLD)
    d.text((36, 18), "THE WORLD IN ONE DAY", font=f_title, fill=(255, 255, 255))
    d.rounded_rectangle([36, 76, 36 + 470, 76 + 32], radius=16,
                        fill=GOLD, outline=None)
    d.text((52, 80), "SUNDAY  •  22 NOVEMBER 2026", font=f_date, fill=NAVY)
    d.text((560, 80), "6 STORIES  •  1 DAY", font=f_date, fill=GOLD_LT)

    # ---- hero: COP31 ----
    d.rounded_rectangle([28, 140, 996, 340], radius=14, fill=CARD,
                        outline=RED, width=3)
    d.rectangle([28, 140, 40, 340], fill=RED)
    draw_globe(d, 175, 240, 64)
    d.rounded_rectangle([108, 292, 242, 320], radius=6, fill=RED)
    d.text((122, 297), "NO DEAL", font=font(FB, 20), fill=(255, 255, 255))
    d.text((288, 152), "CLIMATE  •  ANTALYA, TURKIYE", font=f_kick, fill=RED)
    d.text((288, 176), "COP31 COLLAPSES", font=f_hero, fill=INK)
    d.text((288, 220), "— NO CLIMATE PACT", font=f_hero2, fill=INK)
    hero_lines = wrap(d, "Two weeks of talks end with no agreement: the final "
                      "text drops fossil fuels, and the EU, UK and allies "
                      "walk away.", f_body, 660)
    text_block(d, 288, 260, hero_lines, f_body, (58, 66, 84), 26)

    # ---- timeline section header ----
    d.text((36, 356), "THE DAY, IN ORDER", font=f_sec, fill=INK)
    d.line([(36, 388), (988, 388)], fill=LINE, width=2)
    d.text((640, 356), "from dawn in Libya to night in Nigeria", font=f_foot,
           fill=GREY)

    # ---- timeline spine ----
    spine_x = 512
    d.line([(spine_x, 404), (spine_x, 962)], fill=INK, width=4)
    d.ellipse([spine_x - 9, 404 - 9, spine_x + 9, 404 + 9], fill=GOLD,
              outline=INK, width=2)

    stories = [
        ("BENGHAZI, LIBYA", "Russian warship sunk",
         "Sea drones hit the corvette Merkury at dawn; only its bow stayed "
         "above water.", "ship", NAVY2, "left"),
        ("DYMER, UKRAINE", "Drone flattens Kyiv flats",
         "A Russian drone hit a five-storey block; 14 missing, six killed "
         "across the Kyiv region.", "flats", RED, "right"),
        ("BAHRAIN, THE GULF", "Iran strike wounds two",
         "Bahrain says an Iranian strike hit a civilian site; two hurt, "
         "one critically.", "burst", (122, 84, 20), "left"),
        ("CIKANDE, INDONESIA", "Candy factory fire kills 3",
         "Fire swept a candy factory in Banten; 36 still missing as "
         "rescuers search.", "flame", (176, 92, 20), "right"),
        ("BAYELSA, NIGERIA", "Funeral boat toll hits 24",
         "NEMA confirmed 24 dead after the crowded boat capsized en route "
         "to a burial.", "boat", TEAL, "left"),
    ]
    y = 400
    card_h = 110
    gap = 4
    for idx, (place, head, summ, kind, accent, side) in enumerate(stories, 2):
        if side == "left":
            x0, x1 = 28, 486
            node_x = 486
        else:
            x0, x1 = 538, 996
            node_x = 538
        d.rounded_rectangle([x0, y, x1, y + card_h], radius=10, fill=CARD,
                            outline=LINE, width=2)
        d.rectangle([x0, y + 8, x0 + 7, y + card_h - 8], fill=accent)
        d.ellipse([spine_x - 11, y + card_h // 2 - 11, spine_x + 11,
                   y + card_h // 2 + 11], fill=accent, outline=INK, width=2)
        d.text((spine_x - 5, y + card_h // 2 - 10), str(idx), font=font(FB, 14),
               fill=(255, 255, 255))
        icon_cx = node_x + (-34 if side == "left" else 34)
        draw_icon(d, kind, icon_cx, y + card_h // 2, accent)
        tx = x0 + 20 if side == "left" else x0 + 76
        tw = (x1 - x0) - (20 + 58) if side == "left" else (x1 - x0) - (76 + 16)
        d.text((tx, y + 8), place, font=f_tag, fill=accent)
        head_lines = wrap(d, head, f_head, tw)
        yy = text_block(d, tx, y + 31, head_lines[:1], f_head, INK, 26)
        sum_lines = wrap(d, summ, f_sum, tw)
        text_block(d, tx, yy + 2, sum_lines[:2], f_sum, (58, 66, 84), 20)
        y += card_h + gap

    # ---- footer ----
    d.line([(36, 978), (988, 978)], fill=LINE, width=2)
    d.text((36, 986), "Sources: CNN, UN News, Reuters, AP, Gulf News, NEMA  •  "
           "Every story happened or was first reported on 22 Nov 2026",
           font=f_foot, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
