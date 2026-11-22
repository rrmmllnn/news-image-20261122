# news-image-20261122 — Round 3: "One Day on Earth"

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A dotted world-map poster of Sunday 22 November 2026. A dot-matrix world
map carries numbered red pins at the places where the day's stories
happened; below it, a numbered headline list matches the pins. The date is
in the masthead: **SUNDAY, 22 NOVEMBER 2026**.

## How it differs from round 2

Round 2 ("The World in One Day", 96.1059%) was a card-grid newspaper front
page: a skyline illustration on top, four story cards, an "also today"
strip. Round 3 is a different visual idea entirely — the map is the hero,
geography does the organising, and every story is located on it. It also
covers twice as many stories (12 vs 6) across six regions, with the
Europe/Gulf cluster fanned out with leader lines so every pin stays
readable.

## The 12 stories (all verified against reporting of 22 Nov 2026)

1. **COP31, Antalya** — New Sunday package put to ~200 nations after two
   days of overtime; the draft still omits fossil fuels (Reuters, CNA).
2. **Iran–Bahrain** — Tehran claims missile/drone strikes hit two US
   Patriot radars; Bahrain says an industrial site was hit (Reuters).
3. **NATO–Poland, Warsaw** — Rutte: NATO will defend "every inch" of
   Polish territory, after Poland said Russia violated its airspace
   (Reuters).
4. **EU–Indonesia, Brussels** — Landmark trade deal signed after a decade
   of talks; tariffs on 98.5% of lines to go, ~€600m a year saved
   (European Commission, Reuters).
5. **Mexico, Sinaloa** — "El Chapo Isidro" (FBI Top 10) captured in a
   military raid; 11 killed as cartel gunmen fought back (Reuters, CNN).
6. **Peru, Junín** — 6.8 quake rattles Lima; no deaths or major damage
   reported (Reuters/GFZ).
7. **Hong Kong** — Voting for the Election Committee: 856 candidates
   contest 723 seats.
8. **Baltic Sea** — Russian cargo ship ablaze after a drone strike; crew
   evacuates as it drifts into Finnish waters (Reuters).
9. **Iraq, Basra** — Fire at a power station kills 4, injures 35
   (Reuters).
10. **UN, Geneva** — States agree to negotiate rules on autonomous
    ("killer robot") weapons within two years, by 2028 (Reuters).
11. **Bangladesh, Dhaka** — Over 50 Awami League homes set ablaze ahead
    of Hasina's return.
12. **Qatar–Iran, Tehran** — Qatari delegation holds talks as diplomacy
    tries to end the Iran war (Reuters).

Fact notes: the Peru quake (6), the Mexico capture (5), the Baltic ship
(8), the Basra fire (9) and the UN talks (10) happened on 20–21 Nov and
were the lead items of the 22 Nov news cycle; the COP31 Sunday package
(1) and the Iran–Bahrain strikes (2) are the stories of 22 Nov itself.
No figures were invented: casualty counts, the 98.5% tariff figure, the
723/856 Hong Kong numbers and the 2028 target all come from the sources
above.

## Files

- `entry.png` — the final image (1024×1024, PNG, under 1 MiB)
- `draw_entry_v3.py` — the program that draws it (Pillow; run it to
  regenerate `entry.png`)
- `main.py` — the entrypoint: copies `entry.png` to the output directory
  (standard library only, deterministic across runs)

## Build / verify

```sh
python3 draw_entry_v3.py        # regenerates entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```
