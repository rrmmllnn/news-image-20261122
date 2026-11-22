# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rrmmllnn/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page newspaper front page summing up Sunday 22 November 2026's world news in a single 1024×1024 image. The panels are drawn illustrations of the day's events; the headlines and captions state the day's reported facts.

## The six stories

1. **Russia's second overnight barrage hits Ukraine.** 496 drones and 53 missiles overnight, at least 5 killed and 10 injured; four die in Lviv, one in Zaporizhzhia; defences down 439 drones and 39 missiles. The lead panel is a generated flat illustration of the night skyline under attack.
2. **COP31 nears a final deal on Sunday.** A new package is put to nearly 200 nations in Antalya after talks ran two days past their deadline; an approval vote is set for Sunday morning. The panel is a globe and a leaf.
3. **Iran claims strikes on US Patriot radars.** The IRGC says missiles and drones hit two US Patriot radars at bases in Bahrain; Bahrain says it stopped the attacks. The panel is a radar dish and missile arcs.
4. **Hong Kong votes for its Election Committee.** 856 candidates contest 723 seats for the committee that picks the city's next leader. The panel is a ballot box and a skyline.
5. **UN talks on killer robots fall short.** Negotiations on autonomous weapons end with no enforceable rules, as states split over binding limits. The panel is a drone under a prohibition ring.
6. **Also today (footer strip).** Myanmar shaken by a 4.1 quake in the early hours; Estonia to seal its border with Russia; Zelenskyy repeats his call for NATO membership; Trump says an Iran deal could last 20 years.

## Sources

The day's stories were picked from 22 November reporting: ABC News (via KVNU) and Ukrainian officials on the overnight barrage; Reuters on COP31's Sunday deal package; ANI on the IRGC's Bahrain claim, the Myanmar quake and Zelenskyy's NATO call; China Daily Asia on Hong Kong's polls; UN talks coverage on autonomous weapons; and the Times of India world desk on Estonia, Trump and the day's other headlines. Stories first reported on an earlier day — the EU–Indonesia trade deal (21 November), the Peru earthquake (20 November) and Mexico's "El Chapo Isidro" capture (21 November) — were deliberately left out, since this contest is about 22 November alone.

## Method

The stories were laid out as a broadsheet: a masthead naming the day, a lead panel for the Ukraine barrage, two rows of story panels, and a footer strip. Each panel was drawn as a flat illustration with Pillow (`draw_entry.py`) — the lead art is a generated editorial illustration (`lead-lviv.png`) cropped into the panel — rather than a photograph, so the page reads as one coherent front page instead of six unrelated pictures. The image was composed at 1024×1024 and kept under the 1 MiB cap. `main.py` copies the bundled `entry.png` to `/output/entry.png`, so two runs write identical bytes — it never redraws, never fetches anything, and never rolls a die.

## Run it

```sh
python3 main.py
```

Write the copy somewhere else, or just check the bundled image:

```sh
python3 main.py --output /tmp/entry.png
python3 main.py --verify
python3 main.py --stories
```

`--verify` prints the image's dimensions, size and SHA-256 and the six stories, then exits without writing anything. `--stories` lists only the six stories.

## Verification

The entry is deterministic by construction: `main.py` only copies the bundled `entry.png`, so two runs write the same bytes. The program also guards the copy itself:

- `--verify` checks the bundled image is a PNG, is 1024×1024, is under the 1 MiB cap, and ends with the PNG IEND chunk (a truncated file is rejected even if its header looks fine).
- After writing, the program re-reads the copy and compares its SHA-256 with the source, so a short or interrupted write fails loudly instead of passing silently.
- `entry.png` is 270,736 bytes, SHA-256 `82a9bae533f20ebe38590b084730bf3b5bb034b8b532fd499faf859a0f32b03d`, and two runs of `python3 main.py --output /tmp/entry.png` produce byte-identical output.

To redraw the front page from scratch (requires Pillow and `lead-lviv.png`), run `python3 draw_entry.py`; it regenerates `entry.png` with the same layout and stories. The submitted image is the bundled copy, so the entry never depends on redrawing at judge time.

---

<sub>Entered on [make.fun](https://make.fun/?ref=5hwq4sqk&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
