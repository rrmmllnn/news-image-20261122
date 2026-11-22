#!/usr/bin/env python3
"""Draw 'The World in One Day' - six illustrated frames summing up
Sunday 22 November 2026. Pure Pillow, no network, deterministic."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (15, 29, 51)
AMBER = (245, 176, 65)
PAPER = (250, 247, 240)
INK = (24, 28, 36)
GREY = (90, 96, 108)
IMG = None


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


def stamp(img, cx, cy, text, font, colour, angle=-12):
    tmp = Image.new("RGBA", (400, 90), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    tw = td.textlength(text, font=font)
    td.rounded_rectangle([4, 8, tw + 26, 56], radius=8,
                         outline=colour, width=4)
    td.text((17, 14), text, font=font, fill=colour)
    tmp = tmp.crop(tmp.getbbox())
    rot = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
    IMG.paste(rot, (int(cx - rot.width // 2), int(cy - rot.height // 2)),
              rot)


def globe(d, cx, cy, r, sea, land):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=sea,
              outline=(255, 255, 255), width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=land, width=6)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=land, width=6)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 3, cy - r // 6],
              fill=land)
    d.ellipse([cx - r // 5, cy + r // 4, cx + r // 2, cy + r // 2],
              fill=land)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=(255, 255, 255), width=2)


def scene_cop(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (18, 64, 60), (42, 110, 96))
    globe(d, x + 118, y + 66, 46, (46, 134, 120), (120, 190, 140))
    d.line([(x + 92, y + 28), (x + 112, y + 52), (x + 104, y + 70),
            (x + 128, y + 92), (x + 118, y + 108)],
           fill=(226, 62, 52), width=4)
    d.rectangle([x + 250, y + 96, x + 452, y + 108], fill=(30, 34, 40))
    d.rectangle([x + 258, y + 108, x + 266, y + h], fill=(30, 34, 40))
    d.rectangle([x + 436, y + 108, x + 444, y + h], fill=(30, 34, 40))
    for cx in (x + 280, x + 330, x + 380, x + 420):
        d.rectangle([cx, y + 70, cx + 22, y + 96], fill=(30, 34, 40))
    stamp(d, x + 352, y + 42, "NO DEAL", fnt(BOLD, 22), (226, 62, 52))


def scene_ukraine(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (58, 46, 63), (190, 110, 70))
    d.rectangle([x + 60, y + 30, x + 210, y + h], fill=(38, 38, 46))
    for row in range(4):
        for col in range(4):
            wx, wy = x + 76 + col * 34, y + 40 + row * 24
            lit = (row + col) % 3 != 0
            d.rectangle([wx, wy, wx + 18, wy + 14],
                        fill=(245, 200, 90) if lit else (20, 20, 26))
    d.polygon([(x + 210, y + 30), (x + 262, y + 58), (x + 262, y + h),
               (x + 210, y + h)], fill=(52, 48, 56))
    d.polygon([(x + 210, y + 96), (x + 262, y + 96), (x + 250, y + h),
               (x + 210, y + h)], fill=(30, 28, 34))
    for tx, ty in ((x + 222, y + 112), (x + 238, y + 120),
                   (x + 228, y + 126)):
        d.polygon([(tx, ty), (tx + 12, ty), (tx + 6, ty - 10)],
                  fill=(120, 116, 122))
    d.polygon([(x + 330, y + h), (x + 372, y + 24), (x + 388, y + 24),
               (x + 352, y + h)], fill=(245, 214, 130))
    dx, dy = x + 420, y + 26
    d.line([(dx - 16, dy - 8), (dx + 16, dy + 8)], fill=(20, 20, 26),
           width=3)
    d.line([(dx - 16, dy + 8), (dx + 16, dy - 8)], fill=(20, 20, 26),
           width=3)
    for ox, oy in ((dx - 16, dy - 8), (dx + 16, dy - 8),
                   (dx - 16, dy + 8), (dx + 16, dy + 8)):
        d.ellipse([ox - 5, oy - 5, ox + 5, oy + 5], fill=(20, 20, 26))
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(226, 62, 52))


def scene_indonesia(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (24, 30, 48), (70, 60, 66))
    d.rectangle([x + 40, y + 78, x + 300, y + h], fill=(28, 28, 34))
    for i in range(4):
        bx = x + 40 + i * 65
        d.polygon([(bx, y + 78), (bx + 32, y + 56), (bx + 65, y + 78)],
                  fill=(28, 28, 34))
    for fx in (x + 120, x + 170, x + 220):
        d.polygon([(fx - 26, y + 84), (fx, y + 30), (fx + 26, y + 84)],
                  fill=(214, 48, 32))
        d.polygon([(fx - 16, y + 84), (fx, y + 48), (fx + 16, y + 84)],
                  fill=(240, 140, 40))
        d.polygon([(fx - 8, y + 84), (fx, y + 62), (fx + 8, y + 84)],
                  fill=(250, 220, 90))
    for sx, sy, sr in ((x + 330, y + 34, 14), (x + 360, y + 22, 18),
                       (x + 392, y + 38, 12)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                  fill=(150, 148, 152))


def scene_korea(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (36, 68, 52), (74, 120, 92))
    d.rectangle([x + 40, y + 22, x + 290, y + 96], fill=(24, 52, 40),
                outline=(200, 210, 200), width=2)
    d.text((x + 165, y + 42), "CSAT", font=fnt(BOLD, 30),
           fill=(235, 240, 235), anchor="ma")
    d.line([(x + 120, y + 80), (x + 210, y + 80)], fill=(235, 240, 235),
           width=2)
    d.line([(x + 40, y + 112), (x + 440, y + 112)], fill=(40, 30, 22),
           width=4)
    d.rectangle([x + 320, y + 28, x + 404, y + 104], fill=(250, 248, 240))
    for i in range(4):
        ly = y + 46 + i * 15
        d.line([(x + 332, ly), (x + 392, ly)], fill=(150, 150, 150),
               width=2)
    d.text((x + 386, y + 32), "AI", font=fnt(BOLD, 14), fill=(200, 40, 40))
    d.polygon([(x + 292, y + 110), (x + 336, y + 82), (x + 342, y + 88),
               (x + 300, y + 114)], fill=(245, 176, 65))
    d.polygon([(x + 336, y + 82), (x + 344, y + 76), (x + 348, y + 82),
               (x + 342, y + 88)], fill=(40, 40, 48))
    d.rectangle([x + 424, y + 34, x + 440, y + 78], fill=(214, 48, 32))
    d.polygon([(x + 416, y + 78), (x + 448, y + 78), (x + 432, y + 102)],
              fill=(214, 48, 32))


def scene_bahrain(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (20, 72, 107), (90, 140, 170))
    d.ellipse([x + 36, y + 14, x + 76, y + 54], fill=(250, 226, 160))
    d.rectangle([x, y + 84, x + w, y + h], fill=(16, 58, 92))
    d.line([(x, y + 96), (x + w, y + 96)], fill=(120, 170, 205), width=2)
    d.polygon([(x + 60, y + 96), (x + 220, y + 96), (x + 208, y + 112),
               (x + 72, y + 112)], fill=(24, 26, 32))
    d.rectangle([x + 150, y + 70, x + 172, y + 96], fill=(24, 26, 32))
    d.rectangle([x + 96, y + 80, x + 110, y + 96], fill=(24, 26, 32))
    d.polygon([(x + 280, y + 100), (x + 356, y + 100), (x + 348, y + 114),
               (x + 288, y + 114)], fill=(40, 42, 50))
    d.rectangle([x + 322, y + 80, x + 336, y + 100], fill=(40, 42, 50))
    d.rectangle([x + 372, y + 100, x + 448, y + 114], fill=(40, 42, 50))
    d.pieslice([x + 378, y + 52, x + 442, y + 116], 180, 360,
               fill=(235, 238, 240))
    d.arc([x + 90, y + 8, x + 250, y + 90], 300, 20, fill=(250, 220, 90),
          width=3)
    d.ellipse([x + 240, y + 12, x + 250, y + 22], fill=(250, 220, 90))
    d.arc([x + 300, y + 30, x + 430, y + 120], 200, 300,
          fill=(250, 220, 90), width=3)
    d.ellipse([x + 296, y + 66, x + 306, y + 76], fill=(250, 220, 90))


def scene_yemen(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (74, 44, 51), (200, 120, 70))
    for bx, bw, bh in ((x + 30, 46, 46), (x + 84, 60, 62),
                       (x + 152, 40, 38), (x + 380, 56, 58),
                       (x + 444, 34, 40)):
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(30, 26, 32))
    d.line([(x + 240, y + h), (x + 240, y + 34)], fill=(30, 26, 32),
           width=5)
    d.line([(x + 240, y + 34), (x + 306, y + 34)], fill=(30, 26, 32),
           width=4)
    d.line([(x + 306, y + 34), (x + 306, y + 52)], fill=(30, 26, 32),
           width=3)
    d.rectangle([x + 302, y + 52, x + 310, y + 62], fill=(30, 26, 32))
    d.line([(x + 240, y + 34), (x + 198, y + 34)], fill=(30, 26, 32),
           width=4)
    d.rectangle([x + 194, y + 34, x + 202, y + 44], fill=(30, 26, 32))
    d.arc([x + 60, y + 6, x + 260, y + 110], 300, 30, fill=(255, 240, 180),
          width=3)
    d.ellipse([x + 248, y + 14, x + 260, y + 26], fill=(255, 240, 180))
    for sx, sy in ((x + 340, y + 30), (x + 372, y + 44), (x + 356, y + 60)):
        d.polygon([(sx, sy - 12), (sx + 4, sy - 4), (sx + 12, sy),
                   (sx + 4, sy + 4), (sx, sy + 12), (sx - 4, sy + 4),
                   (sx - 12, sy), (sx - 4, sy - 4)], fill=(255, 220, 80))


PANELS = [
    ("ANTALYA  ·  CLIMATE", "COP31 COLLAPSES",
     "No deal in Antalya: the EU rejects a pact with no mention of "
     "fossil fuels. The longest climate summit ever ends empty-handed.",
     (198, 74, 54), scene_cop),
    ("UKRAINE  ·  WAR", "DRONE HITS KYIV FLATS",
     "A Russian drone brings down part of a block in Dymer; 14 people "
     "are missing. A strike on Kryvyi Rih kills two, a boy of seven "
     "among them.", (178, 58, 48), scene_ukraine),
    ("INDONESIA  ·  DISASTER", "36 MISSING IN FACTORY FIRE",
     "Rescuers search the burnt candy factory in Cikande; three are "
     "dead and fifteen were pulled out alive.", (176, 90, 20),
     scene_indonesia),
    ("SEOUL  ·  EDUCATION", "MINISTER QUITS OVER AI CHEATING",
     "South Korea's education chief resigns after last-minute "
     "anti-cheating rules sow chaos at the college entrance exam.",
     (46, 110, 78), scene_korea),
    ("BAHRAIN  ·  THE GULF", "TWO HURT AS IRAN HITS US BASES",
     "Bahrain reports injuries after Tehran claims missile and drone "
     "strikes on US Patriot radars; a tanker convoy readies to sail.",
     (24, 92, 140), scene_bahrain),
    ("YEMEN  ·  RED SEA", "MISSILES OVER RIYADH",
     "Saudi defences intercept Houthi missiles aimed at the capital "
     "as fresh strikes hit Yemen's port of Hodeidah.",
     (150, 60, 80), scene_yemen),
]


def main():
    global IMG
    img = Image.new("RGB", (W, H), PAPER)
    IMG = img
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 116, W, 120], fill=AMBER)
    d.text((20, 16), "THE WORLD IN ONE DAY", font=fnt(BOLD, 44),
           fill=(255, 255, 255))
    d.text((20, 72), "SUNDAY  ·  22 NOVEMBER 2026",
           font=fnt(BOLD, 26), fill=AMBER)
    globe(d, 950, 58, 38, (46, 134, 120), (120, 190, 140))
    d.text((700, 78), "SIX STORIES", font=fnt(BOLD, 20),
           fill=(200, 210, 225))
    gx, gy, gap = 20, 132, 14
    pw = (W - 2 * gx - gap) // 2
    ph = (972 - gy - 2 * gap) // 3
    for i, (kick, head, body, col, scene) in enumerate(PANELS):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        d.rounded_rectangle([px, py, px + pw, py + ph], radius=10,
                            fill=(255, 255, 255),
                            outline=(210, 214, 220), width=2)
        scene(d, px + 2, py + 2, pw - 4, 128)
        d.rectangle([px + 2, py + 130, px + pw - 2, py + 132],
                    fill=(210, 214, 220))
        ty = py + 142
        d.text((px + 16, ty), kick, font=fnt(BOLD, 14), fill=col)
        ty += 24
        for line in wrap(d, head, fnt(BOLD, 21), pw - 32)[:2]:
            d.text((px + 16, ty), line, font=fnt(BOLD, 21), fill=INK)
            ty += 25
        ty += 4
        for line in wrap(d, body, fnt(REG, 15), pw - 32)[:3]:
            d.text((px + 16, ty), line, font=fnt(REG, 15), fill=(58, 64, 74))
            ty += 19
    d.rectangle([0, 978, W, H], fill=NAVY)
    d.text((W // 2, 984),
           "Sources: CNN  ·  Reuters  ·  AP  ·  Korea JoongAng Daily  ·  "
           "KBS  ·  Greenpeace",
           font=fnt(REG, 13), fill=(200, 210, 225), anchor="ma")
    d.text((W // 2, 1004),
           "Every story happened, or was first reported, on Sunday "
           "22 November 2026.",
           font=fnt(REG, 13), fill=(160, 170, 185), anchor="ma")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
