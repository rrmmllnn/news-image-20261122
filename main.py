#!/usr/bin/env python3
"""Entry point for the news-image-20261122 round-4 poster.

Copies the poster rendered by draw_poster.py (entry.png, in this
repository) to the grader's output directory. Standard library only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
# The grader runs the program twice; both runs must write identical bytes,
# so this copies the pre-rendered poster byte for byte.

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT, "entry.png"))
