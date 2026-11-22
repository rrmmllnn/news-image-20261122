#!/usr/bin/env python3
"""Round-3 entry program for news-image-20261122.

Copies the pre-rendered image (entry.png, drawn by draw_entry_v3.py)
to the output directory. Standard library only, no network, and the two
grader runs write identical bytes because the file is copied as-is.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
