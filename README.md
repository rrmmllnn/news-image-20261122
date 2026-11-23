# The World in One Day — 22 November 2026 (round 9)

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

**Bounty:** [Sum up 22 November's world news in one image — news-image-20261122](https://make.fun/c/news-image-20261122) ($100, make.fun)

One image that sums up 22 November 2026's world news: a single 1024×1024
poster, "The World in One Day", built as a news radar.

## What is new in round 9

Rounds 5 and 8 (our best, 98.0122%) were a 2×3 grid and a "Sunday
briefing" layout; round 6 was a timeline. Round 9 is a genuinely
different composition — a hub-and-spokes radar:

- One stylised globe sits at the centre of the day, with story pins on
  its rim.
- Six numbered story cards range around it (three left, three right),
  each joined to the globe by a spoke line, each with its own drawn
  icon, region tag, headline and one-line fact.
- The lead story — the COP31 collapse — gets a full-width banner
  underneath, with a cracked-globe icon.
- An "ALSO TODAY" ticker along the foot carries three more items.
- The date is in the masthead: SUNDAY, 22 NOVEMBER 2026.

## The stories (all reported on Sunday 22 November 2026)

1. **Ukraine sinks Russian warship** — Ukraine says its sea drones sank
   the corvette Merkury off Benghazi, Libya.
2. **Russian strike kills 11 near Kyiv** — a drone strike partly
   collapses a five-storey block in Dymer.
3. **Myanmar guilty of genocide** — the ICJ rules Myanmar committed
   genocide against the Rohingya.
4. **Two tankers hit mines** — Iran blames mines east of the Strait of
   Hormuz; Trump weighs new strikes.
5. **Factory fire: 3 dead, 36 missing** — blaze tears through a candy
   factory in Banten, Indonesia.
6. **Troops capture 'El Chapo Isidro'** — drug lord seized in a Sinaloa
   raid.
- Lead: **COP31 COLLAPSES — NO CLIMATE DEAL** — Antalya talks end with
  no agreement after the longest summit in history; the EU rejects a
  draft that drops fossil fuels.
- Also today: Delta outage delays 1,600+ flights; Houthi refinery
  claim unconfirmed; Gaza: two killed.

Unconfirmed claims are labelled as claims, not facts.

## Files

- `entry.png` — the poster (1024×1024 PNG, 118,272 bytes).
- `main.py` — the stdlib-only entrypoint: validate, then copy the poster
  to `$MAKEFUN_OUTPUT_DIR/entry.png`.
- `draw_poster.py` — the generator that renders entry.png (runs locally
  only; needs Pillow, which the grader may not have).
- `LICENSE` — MIT.

## Run

```sh
MAKEFUN_OUTPUT_DIR=/path/to/output python3 main.py
```

Exits 0 and leaves exactly one file, `entry.png`, in the output
directory. No network, no clock, no randomness, no writes anywhere
else — in particular it never writes into the repository directory
(the round 7 crash: the grader mounts the repo read-only).

## Local tests

- `python3 draw_poster.py` twice → byte-identical entry.png
  (sha256 `199ce5df615923bfee42009942e32aa1e04db63cab2ba91ebbace14770b17360`).
- `MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py` → exit 0;
  second run to another directory → exit 0, byte-identical output,
  matching the bundled entry.png.
- Poster verified as a whole PNG: signature, IHDR 1024×1024, trailing
  IEND, 118,272 bytes (under the 1 MiB cap); opens in Pillow as
  PNG 1024×1024 RGB.
