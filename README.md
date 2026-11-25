# Tuesday 24 November 2026 world news in one image

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/taozhupipi/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/taozhupipi/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

An entry for the make.fun bounty
[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124):
one 1024×1024 infographic of the day's world news, drawn with Pillow.

## The image

Eight stories from Tuesday 24 November 2026, each verified against
reporting published that day (Reuters, BBC, CBS, FT, Just Security):

1. **Nvidia rally fades** — shares slide 6% a day after Huang's return;
   the CEO admits a conduct breach.
2. **New US tariffs loom** — Trump poised to unveil duties after a probe
   of excess capacity in 16 trading partners.
3. **Strike kills 2 in Zaporizhzhia** — overnight Russian attack hits
   flats; 40 wounded, among them four children.
4. **Hamas security chief killed** — Israeli strikes kill Naeem Abu
   Nahel in Gaza; six others also dead.
5. **CIA hit by cyberattack** — the CIA and another US spy agency
   breached; officials say key systems are safe.
6. **UK energy bills to jump 26%** — household bills forecast to rise
   about £443 a year from January.
7. **175 migrants missing off Senegal** — contact lost with a
   Europe-bound boat that left Dakar two weeks ago.
8. **Huawei convicted in US trial** — a jury finds corporate espionage
   and sanctions evasion.

## How it is built

`draw.py` draws `entry.png` (1024×1024, under 1 MiB) with Pillow:
a dated header plus a two-by-four grid of stories, each with a tag,
a headline, a one-line summary and a small pictogram. `main.ts` is the
entrypoint the harness runs: it copies the pre-drawn image to
`/output/entry.png`, so two runs write byte-identical output.

```sh
python3 draw.py        # renders entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Verification

- `entry.png` is 1024×1024 and under the 1 MiB limit.
- `main.ts` performs a plain byte copy, so repeated runs produce
  byte-identical output.
- Every fact on the image was checked against reporting published
  on 24 November 2026; no story is carried over from an earlier day.
