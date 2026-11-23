"""Round 9 entrypoint: ship the pre-rendered poster to the output dir.

The poster (entry.png, rendered by draw_poster.py in this repository)
is bundled beside this script. This program only reads it, checks it
is a whole 1024x1024 PNG under the 1 MiB cap, and copies it to the
output directory named by MAKEFUN_OUTPUT_DIR (default /output).

It uses only the Python standard library, touches no network, clock
or randomness, and its single write is the output file itself, so it
runs identically in the grader sandbox, where the repository is
mounted read-only.
"""

import os
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SIZE_LIMIT = 1024 * 1024
WIDTH = 1024
HEIGHT = 1024
IEND = struct.pack(">I", 0) + b"IEND" + b"\xaeB`\x82"


def die(message):
    sys.stderr.write("error: %s\n" % message)
    return 1


def validate(data):
    if len(data) > SIZE_LIMIT:
        return "poster is %d bytes, over the 1 MiB cap" % len(data)
    if data[:8] != PNG_MAGIC:
        return "poster lacks the PNG signature"
    if len(data) < 33 or data[12:16] != b"IHDR":
        return "poster has no IHDR chunk"
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (WIDTH, HEIGHT):
        return "poster is %dx%d, expected %dx%d" % (
            width, height, WIDTH, HEIGHT)
    if not data.endswith(IEND):
        return "poster lacks a valid trailing IEND chunk"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        return die("bundled poster not found: %s" % source)
    with open(source, "rb") as handle:
        data = handle.read()
    problem = validate(data)
    if problem is not None:
        return die(problem)
    with open(target, "wb") as handle:
        handle.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
