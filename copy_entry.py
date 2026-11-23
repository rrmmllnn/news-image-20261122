"""Copy the rendered poster into the make.fun output directory.

Entrypoint for the news-image-20261122 round 7 submission. It copies
entry.png (rendered beside this file) into $MAKEFUN_OUTPUT_DIR
(default /output) and prints what it wrote.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, dest)
    size = os.path.getsize(dest)
    print("wrote {} ({} bytes)".format(dest, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
