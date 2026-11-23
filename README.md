# The World in One Day — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

**Bounty:** [Sum up 22 November's world news in one image — news-image-20261122](https://make.fun/c/news-image-20261122) ($100, make.fun)

Round 7 entry for the make.fun `news-image-20261122` competition: one image
summing up the world's news of Sunday 22 November 2026.

## Design

A "Sunday briefing" digest, not a grid, a timeline or a newspaper page:

- **Masthead** — the title and the date, Sunday 22 November 2026, so the day
  the image sums up is named at once.
- **Hero story** — the COP31 climate talks collapsing in Antalya, with a
  cracked-globe illustration and a NO DEAL stamp.
- **Five wire bands** — one story each, with a drawn pictogram, place,
  headline and consequence:
  1. COP31 collapse, Antalya, Türkiye (hero)
  2. Russian corvette *Merkury* sunk by sea drones off Benghazi, Libya
  3. Russian drone collapses an apartment block in Dymer, near Kyiv
  4. Iran claims strikes on US bases in Bahrain; Bahrain says a civilian
     plant was hit
  5. Candy factory fire in Cikande, Indonesia — three dead, 36 missing
  6. Boat carrying mourners capsizes in Bayelsa, Nigeria — at least 24 dead

Sources are named in the footer: Reuters, AP, AFP, CNN, Al Jazeera, as
reported on Sunday 22 November 2026.

## Run

```
python3 main.py
```

`main.py` draws the poster deterministically with Pillow (no network, no
clock, no randomness) and writes `entry.png` next to itself and into
`$MAKEFUN_OUTPUT_DIR` when that is set. Re-running produces identical bytes.

## Files

- `main.py` — the program that draws the poster
- `entry.png` — the rendered poster (1024 × 1024, under 1 MiB)
- `README.md` — this file
- `LICENSE` — MIT
