#!/usr/bin/env python3
"""Draw the news-image-20261122 front page (1024x1024) with Pillow.

Layout: navy masthead naming Sunday 22 November 2026, a lead panel on
Russia's second overnight barrage of Ukraine in three nights (art
generated with the media pipeline, no text in it), two rows of two
story panels (COP31 nearing a final deal on Sunday, Iran's claim of
strikes on US Patriot radars in Bahrain, Hong Kong's Election
Committee vote, UN talks on autonomous weapons falling short), and a
footer strip with four more stories. All text is rendered by Pillow
so it stays legible; the lead art is the generated illustration
cropped into the panel.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LEAD_ART = os.path.join(HERE, "lead-lviv.png")

W, H = 1024, 1024
NAVY = (20, 38, 74)
GOLD = (201, 162, 39)
PAPER = (250, 248, 242)
INK = (24, 24, 24)
GREY = (90, 90, 90)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width in pixels, word by word."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def panel(draw, x, y, w, h, accent):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=(255, 255, 255), outline=(200, 200, 200), width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)


def headline_block(draw, x, y, w, title, caption, title_size=25, cap_size=17):
    tf, cf = font(FB, title_size), font(FR, cap_size)
    ty = y
    for line in wrap(draw, title, tf, w):
        draw.text((x, ty), line, font=tf, fill=INK)
        ty += title_size + 6
    ty += 2
    for line in wrap(draw, caption, cf, w):
        draw.text((x, ty), line, font=cf, fill=(60, 60, 60))
        ty += cap_size + 5
    return ty


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 118], fill=GOLD)
    d.text((512, 18), "THE WORLD IN ONE DAY", font=font(FB, 52),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 80), "SUNDAY 22 NOVEMBER 2026  •  THE DAY IN SIX STORIES",
           font=font(FB, 20), fill=(214, 226, 240), anchor="ma")

    # --- lead panel: Russia's second overnight barrage on Ukraine ---
    px, py, pw, ph = 20, 130, 984, 300
    panel(d, px, py, pw, ph, GOLD)
    art = Image.open(LEAD_ART).convert("RGB")
    aw, ah = pw - 4, 130
    scale = max(aw / art.width, ah / art.height)
    art = art.resize((int(art.width * scale), int(art.height * scale)),
                     Image.LANCZOS)
    left = (art.width - aw) // 2
    # Crop the band with the skyline and explosions, not the empty sky.
    top = int(art.height * 0.42)
    top = min(top, art.height - ah)
    img.paste(art.crop((left, top, left + aw, top + ah)),
              (px + 2, py + 10))
    d.text((px + 24, py + 150), "LVIV  •  KYIV  •  ZAPORIZHZHIA", font=font(FB, 16), fill=GREY)
    headline_block(d, px + 24, py + 172, pw - 48,
                   "SECOND OVERNIGHT BARRAGE HITS UKRAINE",
                   "Russia fires 496 drones and 53 missiles overnight; at least 5 killed, 10 injured. "
                   "Four die in Lviv, one in Zaporizhzhia; defences down 439 drones and 39 missiles.",
                   title_size=27, cap_size=17)

    # --- row 2 (y 442, h 236) ---
    y, w, h = 442, 484, 236
    # COP31 panel
    x = 20
    panel(d, x, y, w, h, (0, 110, 70))
    d.rectangle([x + 2, y + 10, x + w - 2, y + 100], fill=(214, 238, 222))
    # globe
    cx, cy, r = x + 90, y + 55, 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 120, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.line([cx, cy - r, cx, cy + r], fill=(255, 255, 255), width=2)
    # leaf
    d.pieslice([x + 170, y + 20, x + 250, y + 90], 180, 360, fill=(60, 160, 80))
    d.line([x + 170, y + 55, x + 250, y + 55], fill=(30, 110, 60), width=3)
    d.text((x + 270, y + 52), "COP31", font=font(FB, 34),
           fill=(0, 110, 70), anchor="lm")
    d.text((x + 24, y + 108), "ANTALYA  •  CLIMATE", font=font(FB, 16), fill=GREY)
    headline_block(d, x + 24, y + 126, w - 48,
                   "COP31 NEARS A FINAL DEAL ON SUNDAY",
                   "New package put to nearly 200 nations after two days of overtime; vote set for Sunday.",
                   title_size=24, cap_size=16)

    # Gulf / Bahrain panel
    x = 520
    panel(d, x, y, w, h, (150, 40, 40))
    d.rectangle([x + 2, y + 10, x + w - 2, y + 100], fill=(238, 220, 220))
    # radar dish
    cx, cy = x + 90, y + 78
    d.pieslice([cx - 52, cy - 52, cx + 52, cy + 52], 180, 360, fill=(170, 30, 30))
    d.line([cx, cy, cx + 30, y + 96], fill=(170, 30, 30), width=5)
    for ang in (200, 230, 260, 290, 320):
        a = math.radians(ang)
        d.line([cx + 58 * math.cos(a), cy + 58 * math.sin(a),
                cx + 78 * math.cos(a), cy + 78 * math.sin(a)],
               fill=(170, 30, 30), width=3)
    # missile arcs
    d.arc([x + 220, y + 10, x + 420, y + 130], 200, 330, fill=(120, 30, 30), width=4)
    d.polygon([(x + 396, y + 34), (x + 420, y + 22), (x + 408, y + 48)], fill=(120, 30, 30))
    d.arc([x + 260, y + 30, x + 440, y + 140], 200, 330, fill=(120, 30, 30), width=3)
    d.text((x + 24, y + 108), "BAHRAIN  •  THE GULF", font=font(FB, 16), fill=GREY)
    headline_block(d, x + 24, y + 126, w - 48,
                   "IRAN CLAIMS STRIKES ON US PATRIOT RADARS",
                   "IRGC says missiles and drones hit two US Patriot radars; Bahrain says it stopped them.",
                   title_size=24, cap_size=16)

    # --- row 3 (y 690, h 236) ---
    y = 690
    # Hong Kong panel
    x = 20
    panel(d, x, y, w, h, (0, 70, 140))
    d.rectangle([x + 2, y + 10, x + w - 2, y + 100], fill=(214, 226, 240))
    # ballot box
    bx, by = x + 60, y + 28
    d.rectangle([bx, by + 22, bx + 110, by + 66], fill=(0, 70, 140))
    d.rectangle([bx - 8, by + 14, bx + 118, by + 26], fill=(0, 50, 110))
    d.rectangle([bx + 42, by, bx + 68, by + 16], fill=(250, 248, 242))
    d.text((bx + 55, by + 44), "✓", font=font(FB, 34),
           fill=(255, 255, 255), anchor="mm")
    d.rectangle([x + 200, y + 40, x + 236, y + 94], fill=(0, 70, 140))
    d.rectangle([x + 244, y + 26, x + 280, y + 94], fill=(0, 90, 170))
    d.rectangle([x + 288, y + 52, x + 324, y + 94], fill=(0, 70, 140))
    d.text((x + 340, y + 66), "723 seats", font=font(FB, 22),
           fill=(0, 70, 140), anchor="lm")
    d.text((x + 24, y + 108), "HONG KONG  •  POLITICS", font=font(FB, 16), fill=GREY)
    headline_block(d, x + 24, y + 126, w - 48,
                   "HONG KONG VOTES FOR ELECTION COMMITTEE",
                   "856 candidates contest 723 seats for the committee that picks the city's next leader.",
                   title_size=24, cap_size=16)

    # UN autonomous weapons panel
    x = 520
    panel(d, x, y, w, h, (120, 60, 160))
    d.rectangle([x + 2, y + 10, x + w - 2, y + 100], fill=(232, 222, 242))
    # drone with a prohibition ring
    cx, cy = x + 110, y + 55
    d.ellipse([cx - 16, cy - 10, cx + 16, cy + 10], fill=(60, 30, 90))
    for dx, dy in ((-34, -22), (34, -22), (-34, 22), (34, 22)):
        d.line([cx, cy, cx + dx, cy + dy], fill=(60, 30, 90), width=3)
        d.ellipse([cx + dx - 12, cy + dy - 4, cx + dx + 12, cy + dy + 4],
                  outline=(60, 30, 90), width=3)
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=(200, 30, 30), width=6)
    d.line([cx - 37, cy + 37, cx + 37, cy - 37], fill=(200, 30, 30), width=6)
    d.text((x + 200, y + 52), "NO RULES", font=font(FB, 30),
           fill=(120, 60, 160), anchor="lm")
    d.text((x + 24, y + 108), "UNITED NATIONS  •  DISARMAMENT", font=font(FB, 16), fill=GREY)
    headline_block(d, x + 24, y + 126, w - 48,
                   "UN TALKS ON KILLER ROBOTS FALL SHORT",
                   "Autonomous-weapons talks end with no enforceable rules; states split over limits.",
                   title_size=24, cap_size=16)

    # --- footer strip ---
    d.rectangle([0, 944, W, H], fill=NAVY)
    d.text((512, 954), "ALSO TODAY", font=font(FB, 15), fill=GOLD, anchor="ma")
    footer = ("MYANMAR shaken by a 4.1 quake in the early hours  •  ESTONIA to seal its border "
              "with Russia  •  ZELENSKYY repeats call for NATO membership  •  TRUMP says an Iran "
              "deal could last 20 years")
    for i, line in enumerate(wrap(d, footer, font(FR, 16), W - 48)):
        d.text((512, 976 + i * 20), line, font=font(FR, 16),
               fill=(220, 228, 240), anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
