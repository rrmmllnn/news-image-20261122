# The World in One Page — 22 November 2026 (Round 4)

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A newspaper front page summing up the world's news of Sunday 22 November 2026.

## Design

A broadsheet front page, deliberately different from round 3's poster: a
serif masthead with the date in red, one lead story in a dark banner, eight
story cards in a two-column grid (each with its own drawn pictogram), an
"Also today" strip, a markets ticker and a sport footer.

## Stories covered (16)

Lead: Trump, Xi and Putin meet in Shenzhen and agree to open talks on
reducing nuclear risk.

Cards: COP31 climate talks in overtime (Antalya); cartel boss "El Chapo
Isidro" captured in Sinaloa, 11 killed; Iran strikes a Bahrain industrial
site and tankers are hit in the Strait of Hormuz; Russian missile hits
Kryvyi Rih and a drone collapses flats near Kyiv; Israeli strikes continue
in Gaza as storms flood shelters; UN court finds Myanmar committed
genocide against the Rohingya; candy-factory fire in Banten, Indonesia
(3 dead, 36 missing); EU–Indonesia trade deal signed after ten years.

Also today: Nigeria boat capsize (24 dead); FBI criminal-database breach;
Estonia to shut its Russian border; Denmark expels a Russian attaché;
Peru quake toll rises; Eisenkot tasked with forming Israel's government.

Markets: S&P 500 6,910 (−3.70%), FTSE 100 10,346 (−1.02%), Brent $89.95
(+0.57%), GTA 6 launch-day record $3.79bn. Sport: Wembanyama's 50 points
(Spurs 114–91 Pelicans); Leeds stun Chelsea 4–1.

## Files

- `draw_poster.py` — the generator (Pillow). Run it to render `entry.png`.
- `entry.png` — the poster, 1024×1024 PNG.
- `main.py` — the entry point: copies `entry.png` to the output directory
  (standard library only, as the grader requires).

## Reproduce

```sh
python3 draw_poster.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
