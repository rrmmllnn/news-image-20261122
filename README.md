[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard)
[![reward](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

# The World in One Day — Sunday 22 November 2026

Round 5 entry for [Sum up 22 November's world news in one image](https://make.fun/bounty/news-image-20261122) ($100, make.fun).

## The image

A poster, **"The World in One Day"**, that sums up Sunday 22 November 2026 in six illustrated frames — a different design from the newspaper front page of round 4. Each frame is a flat-illustration scene with a place tag, a headline, and a two-line summary, so a viewer who missed the day can tell what happened from the image alone.

1. **Antalya · Climate — COP31 collapses.** The UN climate summit in Antalya ends with no deal after the EU rejects a pact with no mention of fossil fuels; the longest COP ever.
2. **Ukraine · War — Drone hits Kyiv flats.** A Russian drone brings down part of a five-storey block in Dymer, Kyiv region; 14 people are missing. A strike on Kryvyi Rih kills two, a boy of seven among them.
3. **Indonesia · Disaster — 36 missing in factory fire.** Rescuers search the burnt candy factory in Cikande; three are dead and fifteen were pulled out alive.
4. **Seoul · Education — Minister quits over AI cheating.** South Korea's education chief resigns after last-minute anti-cheating rules sow chaos at the college entrance exam (CSAT).
5. **Bahrain · The Gulf — Two hurt as Iran hits US bases.** Bahrain reports injuries after Tehran claims missile and drone strikes on US Patriot radars; a tanker convoy readies to sail.
6. **Yemen · Red Sea — Missiles over Riyadh.** Saudi defences intercept Houthi missiles aimed at the capital as fresh strikes hit Yemen's port of Hodeidah.

Every story happened, or was first reported, on Sunday 22 November 2026. Sources: CNN, Reuters, AP, Korea JoongAng Daily, KBS, Greenpeace.

## How it is built

`draw_poster.py` draws the poster with Pillow (no network, deterministic) and writes `entry.png` (1024×1024, under 1 MiB). `main.py` is the entry program: it copies `entry.png` to `/output/entry.png`, byte-identically, on every run.

```sh
python3 draw_poster.py   # regenerate entry.png
python3 main.py          # write /output/entry.png
```

## License

MIT — see `LICENSE`.
