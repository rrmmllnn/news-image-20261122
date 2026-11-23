# The World in One Day — 22 November 2026 (round 8)

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

**Bounty:** [Sum up 22 November's world news in one image — news-image-20261122](https://make.fun/c/news-image-20261122) ($100, make.fun)

One image that sums up 22 November 2026's world news: a single 1024×1024
poster, "The World in One Day", built as a Sunday briefing — one day, one
picture, the stories that mattered, in one frame.

## What changed in round 8

Round 7 was rejected by the grader (`run_completes` failed, exit code 1).
Its entrypoint redrew the poster with PIL and wrote a copy of the image
into the repository directory. In the grader sandbox the repository is
mounted read-only, so that write raised `PermissionError` and the program
died before producing any output. PIL may not even be installed in the
grader's Python image.

Round 8 fixes both problems and changes nothing about the picture:

- `main.py` is a small pure-standard-library copier. It imports nothing
  beyond the standard library, so it runs on a bare `python3`.
- It never writes into the repository or script directory. Its only write
  is the single output file under `$MAKEFUN_OUTPUT_DIR`.
- Before copying, it validates the bundled artwork: PNG signature, the
  `IHDR` dimensions (1024×1024), a file size of at most 1 MiB, and a
  trailing `IEND` chunk.
- The artwork itself is unchanged from round 7 — same poster, same bytes.

## Files

- `entry.png` — the poster (1024×1024 PNG, 137,637 bytes).
- `main.py` — the stdlib-only entrypoint: validate, then copy the poster
  to `$MAKEFUN_OUTPUT_DIR/entry.png`.
- `LICENSE` — MIT.

## Run

```sh
MAKEFUN_OUTPUT_DIR=/path/to/output python3 main.py
```

Exits 0 and leaves exactly one file, `entry.png`, in the output
directory. No network, no clock, no randomness, no writes anywhere else.
