#!/usr/bin/env python3
"""Sunday briefing poster: the world's news of Sunday 22 November 2026.

Draws a single 1024x1024 poster with PIL: a masthead, one large hero story
(COP31 collapse in Antalya) and five wire bands for the other stories of the
day. No network, no randomness, no clock: the same run always writes the
same bytes. Writes entry.png next to this file and into $MAKEFUN_OUTPUT_DIR
when that is set.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (28, 28, 26)
MUTED = (74, 74, 68)
NAVY = (22, 35, 63)
TEAL = (15, 61, 62)
TEAL_LT = (42, 127, 132)
CREAM = (246, 241, 231)
GOLD = (216, 180, 90)
RED = (179, 38, 30)
CRACK = (228, 87, 46)
WHITE = (255, 255, 255)
BAND_ALT = (237, 230, 211)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def chip(draw, x, y, text, fnt, fg, bg):
    pad_x, pad_y = 14, 6
    tw = draw.textlength(text, font=fnt)
    th = fnt.size
    draw.rounded_rectangle(
        [x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y],
        radius=8, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fg)


def draw_ship(draw, cx, cy, c):
    draw.polygon([(cx - 30, cy + 6), (cx + 30, cy + 6),
                  (cx + 22, cy + 22), (cx - 22, cy + 22)], fill=c)
    draw.rectangle([cx - 16, cy - 4, cx + 16, cy + 6], fill=c)
    draw.line([cx, cy - 24, cx, cy - 4], fill=c, width=3)
    draw.polygon([(cx, cy - 24), (cx + 12, cy - 20), (cx, cy - 16)], fill=c)
    draw.arc([cx - 30, cy + 24, cx - 6, cy + 36], 0, 180, fill=c, width=3)
    draw.arc([cx + 6, cy + 24, cx + 30, cy + 36], 0, 180, fill=c, width=3)


def draw_drone(draw, cx, cy, c):
    for dx, dy in ((-24, -14), (24, -14), (-24, 14), (24, 14)):
        draw.line([cx, cy, cx + dx, cy + dy], fill=c, width=3)
        draw.ellipse([cx + dx - 8, cy + dy - 4, cx + dx + 8, cy + dy + 4],
                     outline=c, width=3)
    draw.ellipse([cx - 11, cy - 9, cx + 11, cy + 9], fill=c)
    draw.ellipse([cx - 4, cy - 3, cx + 4, cy + 5], fill=PAPER)


def draw_radar(draw, cx, cy, c):
    for r in (14, 24, 34):
        draw.arc([cx - r, cy - r, cx + r, cy + r], -80, 10, fill=c, width=3)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=c)
    for dx, dy in ((16, -18), (22, -8), (12, -26)):
        draw.line([cx + 8, cy - 12, cx + dx, cy + dy], fill=c, width=3)


def draw_factory(draw, cx, cy, c):
    draw.rectangle([cx - 28, cy - 2, cx + 28, cy + 24], fill=c)
    draw.polygon([(cx - 28, cy - 2), (cx - 14, cy - 14), (cx, cy - 2),
                  (cx + 14, cy - 14), (cx + 28, cy - 2)], fill=c)
    draw.rectangle([cx + 14, cy - 26, cx + 24, cy - 2], fill=c)
    draw.polygon([(cx + 19, cy - 40), (cx + 13, cy - 26), (cx + 25, cy - 26)],
                 fill=CRACK)
    for wx in (-20, -4, 12):
        draw.rectangle([cx + wx, cy + 6, cx + wx + 8, cy + 14], fill=PAPER)


def draw_boat(draw, cx, cy, c):
    draw.polygon([(cx - 30, cy + 2), (cx + 30, cy + 2),
                  (cx + 20, cy + 18), (cx - 20, cy + 18)], fill=c)
    draw.line([cx, cy - 24, cx, cy + 2], fill=c, width=3)
    draw.polygon([(cx, cy - 24), (cx, cy - 6), (cx + 14, cy - 6)], fill=c)
    draw.arc([cx - 32, cy + 22, cx - 8, cy + 34], 0, 180, fill=c, width=3)
    draw.arc([cx + 8, cy + 22, cx + 32, cy + 34], 0, 180, fill=c, width=3)


ICONS = {"ship": draw_ship, "drone": draw_drone, "radar": draw_radar,
         "factory": draw_factory, "boat": draw_boat}

STORIES = [
    dict(num="02", place="BENGHAZI, LIBYA", icon="ship",
         accent=(179, 38, 30), tint=(243, 222, 218),
         head="Russian corvette sunk by sea drones",
         body="The Merkury capsized in port; only her bow stayed above water."),
    dict(num="03", place="DYMER, NEAR KYIV", icon="drone",
         accent=(46, 94, 140), tint=(222, 232, 242),
         head="Drone collapses apartment block",
         body="Part of a five-storey block fell in the night; rescuers dig "
              "for the missing."),
    dict(num="04", place="BAHRAIN", icon="radar",
         accent=(107, 78, 158), tint=(232, 226, 242),
         head="Iran claims strikes on US bases",
         body="Tehran claims it hit Patriot radars; Bahrain says a civilian "
              "plant burned."),
    dict(num="05", place="CIKANDE, INDONESIA", icon="factory",
         accent=(192, 94, 31), tint=(244, 228, 214),
         head="Candy factory fire kills three",
         body="36 workers missing as crews search the burned-out plant in Banten."),
    dict(num="06", place="BAYELSA, NIGERIA", icon="boat",
         accent=(47, 122, 77), tint=(220, 238, 226),
         head="Mourners' boat capsizes",
         body="At least 24 dead and 24 rescued on the way to a funeral."),
]


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL_LT,
                 outline=CREAM, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360,
             fill=CREAM, width=2)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 0, 360,
             fill=CREAM, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=CREAM, width=2)
    pts = [(cx + 12, cy - r + 10), (cx - 8, cy - 34), (cx + 16, cy - 2),
           (cx - 12, cy + 30), (cx + 6, cy + r - 8)]
    draw.line(pts, fill=CRACK, width=6, joint="curve")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 150], fill=NAVY)
    f_kick = font(SANS_B, 20)
    kick = "SIX STORIES  ·  ONE DAY  ·  AROUND THE WORLD"
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, 20), kick,
           font=f_kick, fill=GOLD)
    f_title = font(SERIF_B, 60)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 46), title,
           font=f_title, fill=WHITE)
    f_date = font(SANS_B, 26)
    date = "SUNDAY  ·  22 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 112), date,
           font=f_date, fill=GOLD)
    d.rectangle([0, 146, W, 150], fill=GOLD)

    # Hero: COP31.
    d.rounded_rectangle([24, 166, 1000, 448], radius=18, fill=TEAL)
    chip(d, 52, 188, "CLIMATE  ·  ANTALYA, TÜRKIYE", font(SANS_B, 20),
         WHITE, RED)
    f_hero = font(SERIF_B, 44)
    d.text((52, 226), "CLIMATE TALKS", font=f_hero, fill=CREAM)
    d.text((52, 274), "COLLAPSE IN ANTALYA", font=f_hero, fill=CREAM)
    f_sub = font(SANS, 22)
    sub_lines = wrap(
        d, "COP31 ends with no deal — the longest climate summit ever, "
           "and the first to fail since 2009.", f_sub, 660)
    for i, ln in enumerate(sub_lines):
        d.text((52, 330 + i * 28), ln, font=f_sub, fill=(207, 227, 222))
    f_con = font(SANS_B, 21)
    con_y = 330 + len(sub_lines) * 28 + 8
    for i, ln in enumerate(wrap(
            d, "194 nations split over fossil fuels. The EU and island states "
               "refused a text naming no coal, oil or gas.",
            f_con, 660)):
        d.text((52, con_y + i * 27), ln, font=f_con, fill=CREAM)
    draw_globe(d, 830, 298, 90)
    chip(d, 770, 400, "NO DEAL", font(SANS_B, 22), WHITE, RED)
    f_no = font(SERIF_B, 34)
    d.text((936, 182), "01", font=f_no, fill=GOLD)

    # Wire bands.
    y = 460
    for idx, s in enumerate(STORIES):
        bg = WHITE if idx % 2 == 0 else BAND_ALT
        d.rounded_rectangle([24, y, 1000, y + 96], radius=10, fill=bg)
        d.rectangle([24, y + 10, 34, y + 86], fill=s["accent"])
        cx, cy = 96, y + 48
        d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=s["tint"])
        ICONS[s["icon"]](d, cx, cy, s["accent"])
        f_place = font(SANS_B, 19)
        d.text((150, y + 12), s["place"], font=f_place, fill=s["accent"])
        f_head = font(SANS_B, 27)
        d.text((150, y + 36), s["head"], font=f_head, fill=INK)
        f_body = font(SANS, 20)
        for i, ln in enumerate(wrap(d, s["body"], f_body, 800)):
            d.text((150, y + 68 + i * 26), ln, font=f_body, fill=MUTED)
        f_num = font(SERIF_B, 34)
        num = s["num"]
        d.text((972 - d.textlength(num, font=f_num), y + 14), num,
               font=f_num, fill=s["accent"])
        y += 104

    # Footer.
    d.rectangle([0, 980, W, H], fill=NAVY)
    f_src = font(SANS, 17)
    src = ("SOURCES: REUTERS · AP · AFP · CNN · AL JAZEERA — "
           "AS REPORTED ON SUNDAY 22 NOVEMBER 2026")
    d.text(((W - d.textlength(src, font=f_src)) / 2, 998), src,
           font=f_src, fill=WHITE)
    return img


def main():
    img = build()
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(here, "out")
    targets = {os.path.join(here, "entry.png"),
               os.path.join(outdir, "entry.png")}
    for path in targets:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path, format="PNG")
    print("wrote " + ", ".join(sorted(targets)))


if __name__ == "__main__":
    main()
