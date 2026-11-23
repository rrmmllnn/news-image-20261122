"""Round 8 entrypoint: validate the bundled poster and copy it out.

The poster is pre-rendered and shipped next to this script as entry.png.
This program only checks that file and copies it to the output directory
named by MAKEFUN_OUTPUT_DIR. It never writes into the repository, it
imports only the standard library, and it performs no network, clock or
random access, so it runs identically on every deterministic run.
"""

import os
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_FILE_BYTES = 1024 * 1024
IEND_TAIL = struct.pack(">I", 0) + b"IEND" + b"\xaeB`\x82"


def fail(message):
    sys.stderr.write("error: %s\n" % message)
    return 1


def read_poster(path):
    with open(path, "rb") as handle:
        return handle.read()


def check_poster(data):
    if len(data) > MAX_FILE_BYTES:
        return "poster is %d bytes, over the 1 MiB limit" % len(data)
    if data[:8] != PNG_SIGNATURE:
        return "poster does not start with the PNG signature"
    if len(data) < 33:
        return "poster is too short to hold an IHDR chunk"
    if data[12:16] != b"IHDR":
        return "first chunk is not IHDR"
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return "poster is %dx%d, expected %dx%d" % (
            width,
            height,
            EXPECTED_WIDTH,
            EXPECTED_HEIGHT,
        )
    if not data.endswith(IEND_TAIL):
        return "poster does not end with a valid IEND chunk"
    return None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target_path = os.path.join(output_dir, "entry.png")

    if not os.path.isfile(source_path):
        return fail("bundled poster missing: %s" % source_path)

    data = read_poster(source_path)
    problem = check_poster(data)
    if problem is not None:
        return fail(problem)

    os.makedirs(output_dir, exist_ok=True)
    with open(target_path, "wb") as handle:
        handle.write(data)

    print("wrote %s (%d bytes)" % (target_path, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
