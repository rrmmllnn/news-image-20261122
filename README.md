# The World in One Day — Timeline

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard)
[![reward](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

**Bounty:** [Sum up 22 November's world news in one image — news-image-20261122](https://make.fun/c/news-image-20261122) ($100, make.fun)

## The image

A lead story plus a vertical timeline spine: COP31's collapse in Antalya
leads the page, then five more stories run down a timeline from dawn in
Libya to night in Nigeria — six stories, one day, each with its place,
headline and one short summary, so a viewer who missed the day can grasp
what happened from the image alone.

1. **COP31 collapses — no climate pact** (Antalya, Turkiye): after two
   weeks of talks the summit ends with no agreement; the final text drops
   fossil fuels and the EU, UK and allies walk away.
2. **Russian warship sunk** (Benghazi, Libya): sea drones hit the
   corvette Merkury at dawn; only its bow stayed above water.
3. **Drone flattens Kyiv flats** (Dymer, Ukraine): a Russian drone hit a
   five-storey block; 14 missing, six killed across the Kyiv region.
4. **Iran strike wounds two** (Bahrain, the Gulf): Bahrain says an
   Iranian strike hit a civilian site; two hurt, one critically.
5. **Candy factory fire kills 3** (Cikande, Indonesia): fire swept a
   candy factory in Banten; 36 still missing as rescuers search.
6. **Funeral boat toll hits 24** (Bayelsa, Nigeria): NEMA confirmed 24
   dead after the crowded boat capsized en route to a burial.

Sources: CNN, UN News, Reuters, AP, Gulf News, NEMA. Every story happened
or was first reported on Sunday 22 November 2026.

## How it is built

`draw_poster.py` draws `entry.png` (1024x1024, Pillow only, deterministic:
fixed colours, fonts, geometry and text — no network, no randomness).
`main.py` is the packed form of `copy_entry.py`: it copies `entry.png`
byte-identically to `/output/entry.png` on every run.

```sh
python3 draw_poster.py        # regenerate entry.png
python3 main.py               # writes /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
