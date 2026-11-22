#!/usr/bin/env python3
"""Round 3 entry for news-image-20261122: "One Day on Earth".

Concept: a dotted world map poster. The whole day is shown as geography:
a dot-matrix world map with numbered red pins at the places where the
day's stories happened, and below it a numbered headline list that matches
the pins. Genuinely different from round 2's card-grid front page: the map
is the hero, the stories are located on it, and the list reads as a legend.

Stories verified against Reuters / AP / EU Commission reporting of
22 November 2026 (see README.md for the fact notes).
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

NAVY = (16, 32, 60)
GOLD = (217, 164, 65)
PAPER = (246, 241, 227)
LAND = (51, 80, 110)
RED = (192, 57, 43)
INK = (20, 36, 60)
DECKC = (74, 85, 104)
RULE = (216, 210, 192)
OCEAN_TXT = (147, 160, 176)
MUTED = (122, 134, 152)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 46)
F_SUB = font("DejaVuSans.ttf", 16)
F_SIDE_BIG = font("DejaVuSans-Bold.ttf", 22)
F_SIDE_SMALL = font("DejaVuSans.ttf", 15)
F_SECT = font("DejaVuSans-Bold.ttf", 20)
F_SECT_NOTE = font("DejaVuSans.ttf", 14)
F_HEAD = font("DejaVuSans-Bold.ttf", 20)
F_DECK = font("DejaVuSans.ttf", 15)
F_NUM = font("DejaVuSans-Bold.ttf", 13)
F_NUM_BIG = font("DejaVuSans-Bold.ttf", 14)
F_OCEAN = font("DejaVuSans.ttf", 14)
F_CAP = font("DejaVuSans.ttf", 13)

# --- dotted world map -------------------------------------------------------
# Equirectangular grid, 96 columns (lon -180..180) x 40 rows (lat 90..-60).
# Each row lists inclusive column ranges that are land. Built from the
# coastlines as I know them; verified visually after the first render.
LAND_ROWS = [
    [],
    [(25, 30), (33, 42)],
    [(14, 18), (20, 24), (26, 33), (35, 43), (52, 53), (62, 65)],
    [(3, 10), (12, 33), (34, 43), (52, 53), (60, 66)],
    [(2, 12), (13, 34), (35, 44), (50, 53), (55, 75)],
    [(2, 11), (13, 34), (32, 42), (49, 54), (55, 80)],
    [(3, 10), (14, 23), (28, 33), (37, 43), (42, 44), (49, 55), (56, 88)],
    [(4, 9), (14, 24), (28, 33), (40, 42), (46, 48), (50, 57), (58, 90)],
    [(15, 24), (28, 34), (46, 48), (50, 50), (52, 54), (55, 57), (58, 92)],
    [(15, 24), (28, 35), (47, 47), (50, 55), (56, 92), (89, 91)],
    [(12, 35), (47, 52), (53, 90)],
    [(11, 34), (45, 46), (49, 51), (52, 55), (63, 88), (85, 86)],
    [(11, 33), (44, 46), (49, 53), (54, 58), (63, 87), (85, 86)],
    [(11, 32), (44, 46), (50, 50), (53, 53), (54, 58), (63, 86), (82, 83)],
    [(11, 32), (44, 50), (52, 55), (55, 56), (57, 59), (60, 64),
     (65, 67), (68, 72), (73, 85)],
    [(11, 32), (44, 56), (55, 59), (60, 63), (64, 66), (67, 71),
     (73, 76), (77, 84)],
    [(12, 20), (30, 31), (43, 56), (56, 60), (67, 71), (73, 78), (80, 80)],
    [(13, 21), (43, 57), (56, 60), (67, 70), (73, 77)],
    [(14, 21), (21, 24), (43, 58), (57, 61), (67, 70), (73, 76), (80, 81)],
    [(22, 25), (43, 48), (48, 58), (58, 60), (68, 69), (73, 76), (81, 81)],
    [(23, 26), (43, 47), (48, 57), (68, 68), (74, 76), (81, 81)],
    [(24, 27), (27, 31), (45, 50), (50, 58), (75, 76)],
    [(27, 36), (46, 50), (50, 59), (73, 76), (77, 79), (83, 85)],
    [(27, 37), (50, 55), (56, 60), (73, 75), (77, 79), (83, 87)],
    [(27, 38), (50, 58), (74, 75), (78, 79), (83, 86)],
    [(27, 39), (51, 57), (76, 78), (84, 85)],
    [(28, 39), (51, 59), (59, 61)],
    [(28, 39), (51, 59), (59, 61), (82, 86)],
    [(28, 38), (51, 58), (59, 61), (78, 87)],
    [(29, 37), (51, 57), (59, 60), (78, 87)],
    [(29, 36), (51, 56), (78, 86)],
    [(29, 35), (52, 55), (79, 85)],
    [(29, 34), (52, 54), (79, 85)],
    [(29, 33), (52, 54), (80, 84), (93, 94)],
    [(29, 32), (80, 82), (93, 94)],
    [(29, 31), (87, 87), (93, 93)],
    [(29, 30)],
    [(29, 29)],
    [(29, 29)],
    [],
]

MAP_X0, MAP_Y0, CELL = 32, 98, 10.0
MAP_W = 96 * CELL
MAP_H = 40 * CELL


def project(lon, lat):
    """Equirectangular projection into the map area."""
    px = MAP_X0 + (lon + 180.0) / 360.0 * MAP_W
    py = MAP_Y0 + (90.0 - lat) / 3.75 * CELL
    return px, py


# --- the day's stories ------------------------------------------------------
# num, lon, lat, badge offset (dx, dy) from the true pin (0,0 = badge on pin),
# headline, deck (deck starts with a dateline).
STORIES = [
    (1, 30.7, 36.9, (-9, 28),
     "COP31 CLOSE TO A DEAL — FOSSIL FUELS STILL UNNAMED",
     "ANTALYA — New package put to ~200 nations in overtime."),
    (2, 50.6, 26.2, (-5, 28),
     "IRAN SAYS IT HIT TWO US PATRIOT RADARS IN BAHRAIN",
     "Tehran claims strikes on US bases; Bahrain reports a site hit."),
    (3, 21.0, 52.2, (27, -13),
     "NATO VOWS TO DEFEND 'EVERY INCH' OF POLAND",
     "WARSAW — Rutte speaks after a Russian airspace violation."),
    (4, 4.35, 50.85, (-34, -7),
     "EU AND INDONESIA SIGN LANDMARK TRADE DEAL",
     "BRUSSELS — After a decade of talks, tariffs on 98.5% of lines to go."),
    (5, -108.5, 25.6, (0, 0),
     "MEXICO CAPTURES FBI 'TOP 10' KINGPIN",
     "SINALOA — 'El Chapo Isidro' seized in a raid; 11 killed as gunmen fought back."),
    (6, -75.3, -11.2, (0, 0),
     "6.8 QUAKE SHAKES CENTRAL PERU",
     "JUNÍN — Tremor rattles Lima; no deaths or major damage reported."),
    (7, 114.2, 22.3, (0, 0),
     "HONG KONG VOTES FOR ELECTION COMMITTEE",
     "856 candidates contest 723 seats on the leader panel."),
    (8, 24.5, 59.8, (25, -25),
     "RUSSIAN CARGO SHIP ABLAZE AFTER DRONE STRIKE",
     "Crew evacuates as the vessel drifts into Finnish waters."),
    (9, 47.8, 30.5, (29, 16),
     "FIRE AT BASRA POWER STATION KILLS FOUR",
     "Blaze in southern Iraq injures 35; the toll is expected to rise."),
    (10, 6.1, 46.2, (-29, 22),
     "UN TALKS AIM TO CURB 'KILLER ROBOTS' BY 2028",
     "GENEVA — States to negotiate 'killer robot' rules by 2028."),
    (11, 90.4, 23.8, (0, 0),
     "DOZENS OF AWAMI LEAGUE HOMES TORCHED",
     "DHAKA — Over 50 houses set ablaze ahead of Hasina's return."),
    (12, 51.4, 35.7, (29, -7),
     "QATAR IN TEHRAN AS MEDIATION GOES ON",
     "Doha delegation holds talks as diplomacy tries to end the Iran war."),
]

OCEAN_LABELS = [
    ("ATLANTIC OCEAN", -15.0, -30.0),
    ("PACIFIC OCEAN", -140.0, -12.0),
    ("INDIAN OCEAN", 75.0, -28.0),
]


# --- text helpers -----------------------------------------------------------
def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_block(draw, headline, deck, max_w, max_h):
    """Wrap headline + deck to fit max_h, shrinking fonts if needed."""
    for hs, ds in ((20, 15), (19, 14), (18, 13)):
        hf = font("DejaVuSans-Bold.ttf", hs)
        df = font("DejaVuSans.ttf", ds)
        hl = wrap(draw, headline, hf, max_w)
        dl = wrap(draw, deck, df, max_w)
        total = len(hl) * (hs + 4) + len(dl) * (ds + 4)
        if total <= max_h or (hs, ds) == (18, 13):
            while total > max_h and dl:
                dl = dl[:-1]
                if dl:
                    dl[-1] = dl[-1].rstrip(".") + "…"
                total = len(hl) * (hs + 4) + len(dl) * (ds + 4)
            return hl, dl, hf, df, hs + 4, ds + 4
    raise AssertionError("unreachable")


def text_center(draw, cx, cy, s, fnt, fill):
    box = draw.textbbox((0, 0), s, font=fnt)
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text((cx - w / 2 - box[0], cy - h / 2 - box[1]), s, font=fnt, fill=fill)


# --- drawing ---------------------------------------------------------------
def draw_header(draw):
    draw.rectangle([0, 0, W, 92], fill=NAVY)
    draw.text((24, 12), "ONE DAY ON EARTH", font=F_TITLE, fill=(255, 255, 255))
    draw.text((26, 66), "SUNDAY, 22 NOVEMBER 2026  •  THE WORLD'S NEWS, MAPPED",
              font=F_SUB, fill=GOLD)
    draw.text((1000, 14), "12 STORIES", font=F_SIDE_BIG, fill=GOLD, anchor="ra")
    draw.text((1000, 46), "FROM 6 REGIONS", font=F_SIDE_SMALL,
              fill=(199, 208, 221), anchor="ra")
    draw.rectangle([0, 92, W, 95], fill=GOLD)


def draw_map(draw):
    draw.rectangle([0, 95, W, 500], fill=PAPER)
    for r, ranges in enumerate(LAND_ROWS):
        for a, b in ranges:
            for c in range(a, b + 1):
                cx = MAP_X0 + (c + 0.5) * CELL
                cy = MAP_Y0 + (r + 0.5) * CELL
                draw.ellipse([cx - 3.1, cy - 3.1, cx + 3.1, cy + 3.1], fill=LAND)
    for label, lon, lat in OCEAN_LABELS:
        x, y = project(lon, lat)
        draw.text((x, y), label, font=F_OCEAN, fill=OCEAN_TXT, anchor="mm")
    caption = "Red dots mark where today's stories happened — numbers match the list below."
    tw = draw.textlength(caption, font=F_CAP)
    draw.rectangle([28, 474, 28 + tw + 12, 494], fill=PAPER)
    draw.text((34, 478), caption, font=F_CAP, fill=MUTED)


def draw_pins(draw):
    for num, lon, lat, (dx, dy), _h, _d in STORIES:
        px, py = project(lon, lat)
        bx, by = px + dx, py + dy
        if dx or dy:
            draw.line([px, py, bx, by], fill=RED, width=2)
        draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=RED,
                     outline=(255, 255, 255), width=2)
        text_center(draw, bx, by + 0.5, str(num), F_NUM, (255, 255, 255))
        if dx or dy:
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                         outline=(255, 255, 255), width=2)


def draw_list(draw):
    draw.text((16, 508), "THE STORIES", font=F_SECT, fill=INK)
    note = "Numbers on the map match the numbers below"
    draw.text((1008, 514), note, font=F_SECT_NOTE, fill=MUTED, anchor="ra")
    draw.rectangle([16, 538, 1008, 540], fill=RED)
    col_x = [16, 520]
    col_w = 488
    row_y0, row_h = 548, 79
    for i, (num, _lon, _lat, _off, headline, deck) in enumerate(STORIES):
        col = i // 6
        row = i % 6
        x = col_x[col]
        y = row_y0 + row * row_h
        if row:
            draw.line([x, y - 6, x + col_w, y - 6], fill=RULE, width=1)
        draw.ellipse([x, y + 2, x + 26, y + 28], fill=RED)
        text_center(draw, x + 13, y + 15.5, str(num), F_NUM_BIG, (255, 255, 255))
        hl, dl, hf, df, lh, ld = fit_block(draw, headline, deck, col_w - 36, 74)
        ty = y
        for line in hl:
            draw.text((x + 36, ty), line, font=hf, fill=INK)
            ty += lh
        for line in dl:
            draw.text((x + 36, ty), line, font=df, fill=DECKC)
            ty += ld


def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_map(draw)
    draw_pins(draw)
    draw_list(draw)
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
