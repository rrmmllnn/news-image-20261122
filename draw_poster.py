#!/usr/bin/env python3
"""Draw the round-4 news poster for 22 November 2026.

A newspaper front page: masthead with the date, one lead story, eight
story cards from six regions, an "also today" strip, a markets ticker
and a sport footer. Rendered with Pillow at 1024x1024.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
PAPER = (247, 243, 234)
INK = (24, 24, 26)
RED = (178, 32, 44)
NAVY = (20, 33, 61)
NAVY2 = (42, 66, 112)
GREY = (110, 108, 100)
LINE = (200, 194, 180)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = font("DejaVuSerif-Bold.ttf", 54)
SERIF_B36 = font("DejaVuSerif-Bold.ttf", 37)
SERIF_B30 = font("DejaVuSerif-Bold.ttf", 30)
SANS_B24 = font("DejaVuSans-Bold.ttf", 24)
SANS_B19 = font("DejaVuSans-Bold.ttf", 19)
SANS_B16 = font("DejaVuSans-Bold.ttf", 16)
SANS_B13 = font("DejaVuSans-Bold.ttf", 13)
SANS_B12 = font("DejaVuSans-Bold.ttf", 12)
SANS15 = font("DejaVuSans.ttf", 15)
SANS14 = font("DejaVuSans.ttf", 14)
SANS13 = font("DejaVuSans.ttf", 13)
SANS_B11 = font("DejaVuSans-Bold.ttf", 11)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, s, f, fill, x0=0, x1=W):
    w = draw.textlength(s, font=f)
    draw.text(((x0 + x1 - w) / 2, y), s, font=f, fill=fill)


def rule(draw, y, x0=MARGIN, x1=W - MARGIN, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_icon(d, kind, x, y, s, bg):
    """A small white pictogram inside a coloured square."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=bg)
    c = WHITE
    p = s / 64.0  # scale helper: coordinates are in a 64-unit box
    X = lambda u: x + u * p
    Y = lambda v: y + v * p
    if kind == "globe":
        d.ellipse([X(10), Y(10), X(54), Y(54)], outline=c, width=4)
        d.ellipse([X(24), Y(10), X(40), Y(54)], outline=c, width=3)
        d.line([X(10), Y(32), X(54), Y(32)], fill=c, width=3)
        d.arc([X(14), Y(18), X(50), Y(46)], 200, 340, fill=c, width=3)
    elif kind == "shield":
        d.polygon([(X(32), Y(8)), (X(54), Y(16)), (X(54), Y(34)),
                   (X(32), Y(56)), (X(10), Y(34)), (X(10), Y(16))],
                  outline=c, width=4)
        d.text((X(24), Y(22)), "*", font=font("DejaVuSans-Bold.ttf", int(22 * p * 1.6)), fill=c)
    elif kind == "ship":
        d.polygon([(X(8), Y(38)), (X(56), Y(38)), (X(50), Y(50)), (X(14), Y(50))], fill=c)
        d.rectangle([X(16), Y(24), X(28), Y(38)], fill=c)
        d.rectangle([X(32), Y(18), X(46), Y(38)], fill=c)
        d.line([X(40), Y(8), X(40), Y(18)], fill=c, width=3)
        d.polygon([(X(40), Y(8)), (X(52), Y(13)), (X(40), Y(16))], fill=c)
    elif kind == "rocket":
        d.polygon([(X(40), Y(6)), (X(50), Y(26)), (X(40), Y(22))], fill=c)
        d.polygon([(X(40), Y(6)), (X(30), Y(26)), (X(40), Y(22))], fill=c)
        d.polygon([(X(32), Y(10)), (X(48), Y(10)), (X(44), Y(40)), (X(36), Y(40))], fill=c)
        d.polygon([(X(36), Y(40)), (X(44), Y(40)), (X(40), Y(52))], fill=c)
        d.polygon([(X(28), Y(34)), (X(36), Y(36)), (X(34), Y(48))], fill=c)
        d.polygon([(X(52), Y(34)), (X(44), Y(36)), (X(46), Y(48))], fill=c)
    elif kind == "tent":
        d.polygon([(X(32), Y(12)), (X(56), Y(46)), (X(8), Y(46))], outline=c, width=4)
        d.line([X(32), Y(12), X(32), Y(46)], fill=c, width=3)
        d.line([X(14), Y(52), X(18), Y(58)], fill=c, width=3)
        d.line([X(32), Y(52), X(36), Y(58)], fill=c, width=3)
        d.line([X(50), Y(52), X(54), Y(58)], fill=c, width=3)
    elif kind == "scales":
        d.line([X(32), Y(10), X(32), Y(50)], fill=c, width=4)
        d.line([X(14), Y(14), X(50), Y(14)], fill=c, width=4)
        d.line([X(14), Y(14), X(10), Y(34)], fill=c, width=3)
        d.line([X(14), Y(14), X(18), Y(34)], fill=c, width=3)
        d.arc([X(6), Y(30), X(22), Y(42)], 0, 180, fill=c, width=3)
        d.line([X(50), Y(14), X(46), Y(34)], fill=c, width=3)
        d.line([X(50), Y(14), X(54), Y(34)], fill=c, width=3)
        d.arc([X(42), Y(30), X(58), Y(42)], 0, 180, fill=c, width=3)
        d.line([X(22), Y(50), X(42), Y(50)], fill=c, width=4)
    elif kind == "flame":
        d.polygon([(X(32), Y(6)), (X(44), Y(26)), (X(52), Y(36)),
                   (X(48), Y(52)), (X(32), Y(58)), (X(16), Y(52)),
                   (X(12), Y(36)), (X(22), Y(26))], fill=c)
        d.polygon([(X(32), Y(28)), (X(40), Y(38)), (X(38), Y(50)),
                   (X(26), Y(50)), (X(24), Y(38))], fill=bg)
    elif kind == "deal":
        d.rectangle([X(12), Y(12), X(52), Y(52)], outline=c, width=4)
        d.line([X(20), Y(22), X(44), Y(22)], fill=c, width=3)
        d.line([X(20), Y(32), X(38), Y(32)], fill=c, width=3)
        d.polygon([(X(40), Y(40)), (X(46), Y(34)), (X(52), Y(40)),
                   (X(46), Y(52)), (X(40), Y(46))], fill=c)


CARDS = [
    ("CLIMATE", "ANTALYA, TURKEY", "COP31 talks run into overtime",
     "Fossil-fuel wording still divides delegates as the summit enters a "
     "second day past its deadline; the draft deal omits fossil fuels.",
     "globe", (46, 125, 50)),
    ("JUSTICE", "SINALOA, MEXICO", "Cartel boss \u2018El Chapo Isidro\u2019 captured",
     "Mexican forces arrest Fausto Isidro Meza Flores; 11 killed in the "
     "raid \u2014 seven gunmen and four soldiers.",
     "shield", (30, 58, 95)),
    ("CONFLICT", "THE GULF", "Iran strikes Bahrain site; tankers hit",
     "Bahrain says a civilian industrial site was hit, and two tankers "
     "were struck in the Strait of Hormuz.",
     "ship", (14, 110, 120)),
    ("WAR", "UKRAINE", "Missile hits Zelensky\u2019s home town",
     "A Russian strike on Kryvyi Rih kills two and wounds dozens; a "
     "drone collapses flats near Kyiv.",
     "rocket", (178, 60, 44)),
    ("WAR", "GAZA", "Strikes go on as storms flood Gaza",
     "An aid vehicle is hit in Gaza City while heavy rain floods the "
     "shelters of more than a million displaced people.",
     "tent", (90, 105, 125)),
    ("JUSTICE", "THE HAGUE", "UN court: Myanmar committed genocide",
     "Rohingya welcome the verdict on Myanmar\u2019s campaign; rights "
     "groups now urge sanctions.",
     "scales", (96, 60, 130)),
    ("DISASTER", "BANTEN, INDONESIA", "Factory fire: 3 dead, 36 missing",
     "A blaze sweeps a candy factory in Cikande; rescuers search the "
     "wreckage for dozens of workers.",
     "flame", (200, 90, 20)),
    ("TRADE", "BRUSSELS \u2013 JAKARTA", "EU and Indonesia sign trade deal",
     "A decade of talks ends in a pact between the EU and Indonesia, "
     "covering some 700 million people.",
     "deal", (30, 110, 60)),
]

ALSO = [
    ("NIGERIA", "Boat capsizes on the way to a funeral \u2014 at least 24 dead."),
    ("UNITED STATES", "Trump confirms the FBI database was breached."),
    ("ESTONIA", "Tallinn to shut its border with Russia."),
    ("DENMARK", "Russian attach\u00e9 expelled over an alleged plot."),
    ("PERU", "Quake toll rises: 1 dead, 853 homeless after Friday\u2019s tremor."),
    ("ISRAEL", "Eisenkot tasked with forming the next government."),
]


def draw_lead(d):
    x0, y0, x1, y1 = MARGIN, 138, W - MARGIN, 322
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=NAVY)
    # skyline silhouette along the bottom
    sky = [(x0 + 14, y1), (x0 + 14, 292), (x0 + 60, 292), (x0 + 60, 272),
           (x0 + 96, 272), (x0 + 96, 296), (x0 + 150, 296), (x0 + 150, 278),
           (x0 + 190, 278), (x0 + 190, 300), (x0 + 240, 300), (x0 + 240, 284),
           (x0 + 280, 284), (x0 + 280, 302), (x0 + 320, 302), (x0 + 320, 288),
           (x0 + 360, 288), (x0 + 360, y1)]
    d.polygon(sky, fill=NAVY2)
    d.text((x0 + 22, y0 + 14), "DIPLOMACY  \u2014  SHENZHEN, CHINA",
           font=SANS_B13, fill=(255, 205, 90))
    d.text((x0 + 22, y0 + 42), "TRUMP, XI AND PUTIN", font=SERIF_B36, fill=WHITE)
    d.text((x0 + 22, y0 + 84), "MEET IN SHENZHEN", font=SERIF_B36, fill=WHITE)
    d.text((x0 + 22, y0 + 132),
           "The three leaders agree to open talks on reducing nuclear risk.",
           font=SANS15, fill=(210, 218, 235))
    # three flag bars, right side
    fx, fy = x1 - 200, y0 + 18
    d.rectangle([fx, fy, fx + 56, fy + 36], fill=(178, 32, 44))          # US stripes base
    for i in range(4):
        d.rectangle([fx, fy + i * 9, fx + 56, fy + i * 9 + 4], fill=WHITE)
    d.rectangle([fx, fy, fx + 24, fy + 18], fill=(30, 58, 120))
    d.rectangle([fx + 66, fy, fx + 122, fy + 36], fill=(222, 41, 16))     # China
    for sx, sy in [(8, 8), (22, 12), (26, 20), (18, 24), (8, 20)]:
        d.text((fx + 66 + sx, fy + sy), "*", font=font("DejaVuSans-Bold.ttf", 11),
               fill=(255, 222, 0))
    d.rectangle([fx + 132, fy, fx + 188, fy + 36], outline=WHITE, width=2)  # Russia
    d.rectangle([fx + 132, fy, fx + 188, fy + 12], fill=WHITE)
    d.rectangle([fx + 132, fy + 12, fx + 188, fy + 24], fill=(0, 57, 166))
    d.rectangle([fx + 132, fy + 24, fx + 188, fy + 36], fill=(213, 0, 0))
    d.text((fx, fy + 46), "USA  \u00b7  CHINA  \u00b7  RUSSIA",
           font=SANS_B11, fill=(200, 208, 225))


def draw_card(d, x, y, w, h, tag, place, headline, body, kind, color):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=WHITE,
                        outline=LINE, width=1)
    draw_icon(d, kind, x + 12, y + 12, 56, color)
    tx = x + 80
    d.text((tx, y + 10), tag + "  \u2014  " + place, font=SANS_B11, fill=RED)
    hl = wrap(d, headline, SANS_B16, w - 92)
    hy = y + 28
    for ln in hl[:2]:
        d.text((tx, hy), ln, font=SANS_B16, fill=INK)
        hy += 20
    by = hy + 2
    for ln in wrap(d, body, SANS13, w - 92)[:3]:
        d.text((tx, by), ln, font=SANS13, fill=(58, 56, 50))
        by += 17


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    center(d, 22, "THE WORLD IN ONE PAGE", SERIF_B, INK)
    rule(d, 96, width=3)
    center(d, 106, "SUNDAY,  22 NOVEMBER 2026", SANS_B24, RED)
    rule(d, 132, width=1, fill=LINE)

    draw_lead(d)

    # section line
    center(d, 336, "THE DAY\u2019S NEWS  \u2014  EIGHT STORIES FROM SIX REGIONS",
           SANS_B12, GREY)

    # story grid: 2 columns x 4 rows
    gx, gy = MARGIN, 362
    cw = (W - 2 * MARGIN - 16) // 2
    ch, gap = 102, 10
    for i, card in enumerate(CARDS):
        cx = gx + (i % 2) * (cw + 16)
        cy = gy + (i // 2) * (ch + gap)
        draw_card(d, cx, cy, cw, ch, *card)

    # also today
    ay0 = gy + 4 * ch + 3 * gap + 12
    ay1 = ay0 + 92
    d.rounded_rectangle([MARGIN, ay0, W - MARGIN, ay1], radius=8,
                        fill=(238, 233, 220), outline=LINE, width=1)
    d.text((MARGIN + 14, ay0 + 8), "ALSO TODAY", font=SANS_B13, fill=RED)
    col_w = (W - 2 * MARGIN - 28) // 2
    for i, (place, line) in enumerate(ALSO):
        cx = MARGIN + 14 + (i // 3) * (col_w + 14)
        cy = ay0 + 30 + (i % 3) * 20
        d.text((cx, cy), "\u2022  " + place + ":  ", font=SANS_B13, fill=INK)
        pw = d.textlength("\u2022  " + place + ":  ", font=SANS_B13)
        d.text((cx + pw, cy), line, font=SANS13, fill=(58, 56, 50))

    # markets ticker
    ty0, ty1 = ay1 + 12, ay1 + 50
    d.rounded_rectangle([MARGIN, ty0, W - MARGIN, ty1], radius=8, fill=NAVY)
    ticker = ("MARKETS   S&P 500  6,910  \u25bc 3.70%      FTSE 100  10,346  "
              "\u25bc 1.02%      BRENT  $89.95  \u25b2 0.57%      GTA 6: $3.79bn LAUNCH RECORD")
    center(d, ty0 + 10, ticker, SANS_B13, WHITE)

    # sport footer
    fy = ty1 + 12
    d.text((MARGIN, fy),
           "SPORT  \u2014  Wembanyama scores 50 as the Spurs beat the Pelicans 114\u201391; "
           "Leeds stun Chelsea 4\u20131 at Stamford Bridge.",
           font=SANS14, fill=INK)
    rule(d, fy + 26, width=1, fill=LINE)
    center(d, fy + 34, "THE WORLD IN ONE PAGE  \u00b7  SUNDAY 22 NOVEMBER 2026",
           SANS_B11, GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
