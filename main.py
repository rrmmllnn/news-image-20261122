"""Sunday front page, 22 November 2026.

This entry is a single-page newspaper front page that sums up the
world news of Sunday 22 November 2026. The artwork itself lives in
entry.png next to this script: a 1024 by 1024 PNG, kept under one
mebibyte. This program never draws anything. It only hands out an
exact copy of that bundled picture, so every run produces the very
same bytes. Use --verify to inspect the bundled file, --stories to
see what the page covers, or run it plain to write the copy out.
"""

import argparse
import hashlib
import struct
import sys
from pathlib import Path


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IEND_TAIL = b"\x00\x00\x00\x00IEND\xaeB`\x82"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
SIZE_LIMIT = 1024 * 1024

HEADLINES = [
    (
        "Overnight barrage over Ukraine",
        "Russia launched its second overnight barrage on Ukraine in "
        "three nights, firing 496 drones and 53 missiles. At least "
        "5 people were killed and 10 injured; four died in Lviv and "
        "one in Zaporizhzhia. Ukrainian defences brought down 439 "
        "drones and 39 missiles.",
    ),
    (
        "COP31 in Antalya closes in on a deal",
        "Climate talks in Antalya are nearing a final deal on Sunday. "
        "Negotiators put a new package to nearly 200 nations after "
        "the talks ran two days past their deadline, with an approval "
        "vote set for Sunday morning.",
    ),
    (
        "IRGC claim over Bahrain bases",
        "Iran's IRGC claims it carried out missile and drone strikes "
        "on two US Patriot radars at bases in Bahrain, while Bahrain "
        "says it stopped the attacks.",
    ),
    (
        "Hong Kong picks its Election Committee",
        "Hong Kong is voting for its Election Committee, with 856 "
        "candidates contesting 723 seats on the committee that picks "
        "the city's next leader.",
    ),
    (
        "UN talks on autonomous weapons fall short",
        "United Nations talks on autonomous weapons, the so-called "
        "\"killer robots\", ended without any enforceable rules, with "
        "states split over binding limits.",
    ),
    (
        "Also on the page",
        "Myanmar was shaken by a 4.1 quake in the early hours; "
        "Estonia is to seal its border with Russia; Zelenskyy repeats "
        "his call for NATO membership; and Trump says an Iran deal "
        "could last 20 years.",
    ),
]


def bundled_picture() -> Path:
    """Return the path of the picture shipped beside this script."""
    return Path(__file__).resolve().parent / "entry.png"


def fingerprint(data: bytes) -> str:
    """Return the hex SHA-256 digest of some bytes."""
    return hashlib.sha256(data).hexdigest()


def read_dimensions(blob: bytes) -> tuple[int, int]:
    """Pull width and height out of the PNG IHDR chunk."""
    if len(blob) < 24:
        raise ValueError("file is too short to hold a PNG header")
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def inspect_bundle(blob: bytes) -> tuple[int, int, int, str]:
    """Check the bundled picture and return width, height, size, digest."""
    if not blob.startswith(PNG_SIGNATURE):
        raise ValueError("bundled file does not start with the PNG magic bytes")
    if len(blob) > SIZE_LIMIT:
        raise ValueError(f"bundled file is over the 1 MiB limit ({len(blob)} bytes)")
    # The first chunk after the 8-byte signature must be IHDR; without
    # it the width/height bytes at offset 16 would be meaningless.
    if blob[12:16] != b"IHDR":
        raise ValueError("bundled file's first chunk is not IHDR")
    width, height = read_dimensions(blob)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"expected a {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} image, "
            f"found {width}x{height}"
        )
    if not blob.endswith(IEND_TAIL):
        raise ValueError("bundled file does not end with a valid PNG IEND chunk")
    return width, height, len(blob), fingerprint(blob)


def show_stories() -> None:
    """Print the six stories the front page covers."""
    for index, (title, body) in enumerate(HEADLINES, start=1):
        print(f"{index}. {title}")
        print(f"   {body}")


def verify_only() -> int:
    """Run the checks, report the findings, and write nothing."""
    blob = bundled_picture().read_bytes()
    width, height, size, digest = inspect_bundle(blob)
    print(f"image: {bundled_picture().name}")
    print(f"dimensions: {width}x{height}")
    print(f"size: {size} bytes")
    print(f"sha256: {digest}")
    print("checks passed: PNG signature, 1024x1024, <= 1 MiB, IEND present")
    print()
    print("Stories on the front page:")
    show_stories()
    return 0


def hand_out_copy(destination: Path) -> int:
    """Copy the bundled picture to destination and confirm it matches."""
    source = bundled_picture()
    blob = source.read_bytes()
    inspect_bundle(blob)
    source_digest = fingerprint(blob)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(blob)
    written = destination.read_bytes()
    if fingerprint(written) != source_digest:
        raise ValueError(
            f"copy mismatch: wrote {destination} but its SHA-256 "
            "does not match the bundled image; refusing to claim success"
        )
    print(f"wrote {destination} ({len(written)} bytes, sha256 {source_digest})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Hand out a copy of the 22 November 2026 front page."
    )
    parser.add_argument(
        "--output",
        default="/output/entry.png",
        help="where to write the copy (default: /output/entry.png)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="check the bundled image and list its stories, without writing",
    )
    parser.add_argument(
        "--stories",
        action="store_true",
        help="print the six stories covered and exit",
    )
    return parser


def main(argv=None) -> int:
    options = build_parser().parse_args(argv)
    if options.stories:
        show_stories()
        return 0
    if options.verify:
        return verify_only()
    return hand_out_copy(Path(options.output))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as problem:
        print(f"error: {problem}", file=sys.stderr)
        sys.exit(1)
