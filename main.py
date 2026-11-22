#!/usr/bin/env python3
"""news-image-20261122 entry: write the composed front page to /output/entry.png.

The image (entry.png, 1024x1024, PNG) sums up Sunday 22 November 2026's
world news in one picture. Six stories fill the front page:

1. Russia's second overnight barrage on Ukraine in three nights: 496
   drones and 53 missiles, at least 5 killed and 10 injured; four die
   in Lviv, one in Zaporizhzhia; defences down 439 drones and 39
   missiles.
2. COP31 nears a final deal on Sunday: a new package is put to nearly
   200 nations in Antalya after talks ran two days past their deadline,
   with an approval vote set for Sunday morning.
3. Iran's IRGC claims missile and drone strikes on two US Patriot
   radars at bases in Bahrain; Bahrain says it stopped the attacks.
4. Hong Kong votes for its Election Committee: 856 candidates contest
   723 seats for the committee that picks the city's next leader.
5. UN talks on autonomous weapons fall short: no enforceable rules,
   as states split over binding limits.
6. The footer carries four more: Myanmar shaken by a 4.1 quake in the
   early hours, Estonia to seal its border with Russia, Zelenskyy
   repeats his call for NATO membership, and Trump says an Iran deal
   could last 20 years.

The lead panel's night-skyline art was generated as a flat editorial
illustration; the other panels are drawn illustrations and all text is
rendered by Pillow (draw_entry.py), so the page reads as one coherent
front page instead of six unrelated pictures. The image was composed at
1024x1024 and kept under the 1 MiB cap. `main.py` copies the bundled
`entry.png` to `/output/entry.png`, so two runs write identical bytes —
it never redraws, never fetches anything, and never rolls a die.
"""
import argparse
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DEFAULT_DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# A complete PNG ends with a 12-byte IEND chunk: zero length, the ASCII
# tag "IEND", and its CRC. Checking the tail catches a truncated file
# that still has a valid header and IHDR dimensions.
PNG_IEND_TAIL = b"\x00\x00\x00\x00IEND\xaeB`\x82"

STORIES = [
    "Second overnight barrage hits Ukraine: 496 drones, 53 missiles, at least 5 killed, 10 injured; four die in Lviv, one in Zaporizhzhia",
    "COP31 nears a final deal on Sunday: new package to nearly 200 nations after two days of overtime",
    "Iran claims strikes on US Patriot radars: IRGC says missiles and drones hit two radars in Bahrain",
    "Hong Kong votes for Election Committee: 856 candidates contest 723 seats",
    "UN talks on killer robots fall short: no enforceable rules on autonomous weapons",
    "Also: Myanmar 4.1 quake, Estonia to seal border with Russia, Zelenskyy repeats NATO call, Trump says Iran deal could last 20 years",
]


def read_png(path):
    """Return the bytes of a file after checking it is a PNG."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != PNG_SIGNATURE:
        raise ValueError(f"{path} is not a PNG file")
    return data


def png_dimensions(data):
    """Read width and height from the PNG IHDR chunk."""
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def verify(data):
    """Check the bundled image against the competition's caps.

    The rules cap the image at 1 MiB and 1024 by 1024 pixels; anything
    larger is refused by the gate before judging, so this fails loudly
    here instead of silently submitting a bad file. The IEND tail check
    also rejects a truncated file whose header still looks fine.
    """
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    width, height = png_dimensions(data)
    if (width, height) != (1024, 1024):
        raise ValueError(f"entry.png is {width}x{height}, expected 1024x1024")
    if not data.endswith(PNG_IEND_TAIL):
        raise ValueError("entry.png is truncated: missing the IEND chunk")
    return width, height


def print_stories():
    """List the six stories the front page carries."""
    print("stories on the front page:")
    for i, story in enumerate(STORIES, 1):
        print(f"  {i}. {story}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=DEFAULT_DST,
                        help="where to write the copy (default: %(default)s)")
    parser.add_argument("--verify", action="store_true",
                        help="check the bundled image and exit without writing")
    parser.add_argument("--stories", action="store_true",
                        help="list the six stories and exit without writing")
    args = parser.parse_args(argv)

    if args.stories:
        print_stories()
        return 0
    data = read_png(SRC)
    width, height = verify(data)
    digest = hashlib.sha256(data).hexdigest()
    if args.verify:
        print(f"entry.png OK: {width}x{height}, {len(data)} bytes, sha256 {digest}")
        print_stories()
        return 0
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    shutil.copyfile(SRC, args.output)
    # Re-read the copy and confirm it matches the source byte for byte;
    # a short write (full disk, interrupted copy) must not pass silently.
    written = read_png(args.output)
    if hashlib.sha256(written).hexdigest() != digest:
        raise ValueError(f"{args.output} does not match the bundled image")
    print(f"wrote {args.output} {len(data)} bytes sha256 {digest}")
    print_stories()
    return 0


if __name__ == "__main__":
    sys.exit(main())
