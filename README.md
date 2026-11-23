# Tamil jathagam skill

A [Claude](https://claude.com/claude-code) skill that reads a birth chart the way a Tamil Nadu jothidar does and turns
it into plain predictions: **what happens when**, what to do, what to avoid, and what the person is like.

Give it a name, a birth date and time, and a place. It works for one person or for a couple.

## What it does

1. **Builds the boxes:** rasi and navamsa charts in the South Indian grid, with Swiss Ephemeris and the Lahiri ayanamsa,
   the same setup Prokerala, AstroSage and most Tamil apps use. Vimshottari dasa, bhukti and antaram dates, Maandhi,
   7½ Sani, Guru and Rahu movements, Chevvai dosham, yogas, 10-porutham and 36-guna matching.
2. **Reads them:** the period quality for the lagnam, transits counted from the Moon, and topic windows (career,
   money, studies, travel and abroad, love and marriage, home).
3. **Writes it plainly:** no house numbers or jargon in the main text.

### Output format

**One person**

- Timeline (one row per real change, 1½–5 months each, Good / Mixed / Tough)
- Do's and Don'ts
- Summary
- Commonly observed behaviours and lifestyle

**Couple**

- Timeline for him, her and the couple
- Do's and don'ts
- Expectation vs reality
- Porutham and guna score

The script writes a styled HTML report (light and dark). The technical boxes go in a collapsed "Behind the reading" section.

## Install

```bash
git clone https://github.com/ram-devv1/jodhiam-skill ~/.claude/skills/tamil-jathagam
cd ~/.claude/skills/tamil-jathagam
python3 -m venv .venv && .venv/bin/pip install pyswisseph
.venv/bin/python scripts/jathagam.py selftest
.venv/bin/python scripts/predict.py selftest
.venv/bin/python scripts/twins.py selftest
```

Python 3.9+. On Windows, also run `pip install tzdata`.

## Use

Ask Claude in plain words:

- *"Predictions for Priya, born 14 March 2003, 6:40 AM, Madurai."*
- *"Check compatibility: Arjun, 2 Jan 2000, 11:15 PM, Coimbatore and Meera, 19 Aug 2002, 7:05 AM, Chennai."*
- *"When's my best time for a job change?"*, *"Why is 2028 tough?"*, *"Any remedies?"*

Or run the scripts directly:

```bash
.venv/bin/python scripts/predict.py person --name "Priya" --date 2003-03-14 --time 06:40 \
    --tz Asia/Kolkata --lat 9.93 --lon 78.12 --place Madurai --years 3 --out out/
.venv/bin/python scripts/predict.py couple out/meera.json out/arjun.json --out out/
.venv/bin/python scripts/jathagam.py chart --name "Priya" ... --out out/   # full technical sheet
```

`out/` holds personal birth data. It is git-ignored and is never published.

## How it judges a chart

Beyond "planet X in box Y", the skill uses rules that Tamil teachers apply when they read a chart. These were collected
from teaching videos and classical texts (see `references/research/`):

- **Hidden from its own house:** a ruler sitting 6th, 8th or 12th from a house it owns drops that house's results.
- **Sign edges (sandhi):** a planet in the first or last 5° of a sign is weak.
- **Combustion:** a planet close to the Sun loses strength, graded by distance. Mercury is exempt, and Jupiter's aspect
  cancels it.
- **Retrograde:** reverses results in good houses and improves them in 6, 8 and 12. A period planet that is retrograde
  now but was direct at birth stalls plans until it turns direct.
- **Sub-periods counted from the main period's planet:** 6th, 8th or 12th from it is bad.
- **Saturn's 7½-year test overrides weak periods.** Jupiter's aspect softens doshams.
- **Rahu by degree:** within 22° it affects a planet, and within 8° it hurts badly. Rahu gives the results of its sign
  lord and star lord.
- **Directional strength (dig bala), badhaka by lagna type, and the two-lord links** (5–9, 9–10, 1–10, 2–11…).

**Behaviour and lifestyle traits** are built from several layers, and only traits that two or more layers agree on are
kept:

1. Lagnam and its ruler.
2. Moon star, Moon sign and pada.
3. Planets in the lagnam or with the Moon.

An optional **chart-twins** step (`scripts/twins.py`) looks up public people born while all nine grahas sat in the
same boxes. It sends only *dates* to Wikidata. Their publicly known character traits quietly confirm or drop traits.

## Sources

**Classical texts:** Brihat Parashara Hora Shastra, Brihat Jataka and Brihat Samhita (Varahamihira), Saravali,
Phaladeepika, Jataka Parijata, Hora Sara, Uttara Kalamrita, Bhrigu Sutras. The readings are summarised with
per-claim citations in `references/planet-in-house.json`, `references/planet-in-house-sources.md` and
`references/research/traits-classical.md`.

**Tamil teaching channels (YouTube):** transcripts were read from auto-generated Tamil captions. Each rule in the notes
cites its video ID.

| Channel | Topics used |
|---|---|
| [Eshwar Gunasekaran](https://www.youtube.com/@Eshwar_Gunasekaran_Official) | Lord of each house in each house, planets in houses, lagna and nakshatra traits (36 videos) |
| Sri Mahalakshmi Jothidam (Sriramji) | Star lord, badhaka, retrograde, combustion, lagna sandhi, Thulam navamsa |
| GURUJI TV (Aditya Guruji) | Star lord, combustion, retrograde Saturn, Rahu by degree, transits |
| Dindigul P. Chinnaraj | Dasa–bhukti judgement |
| Karpaga Virucham Astro, BMKB Astro | Retrograde in transit, transit over natal |
| GK Astro System, Astro Surri Sivam | Ashtakavarga |
| Astro Whiz (KP) | KP sub-lord construction |
| Kadavul Anugraham | Weight of the star lord |
| Astrologer Gokulakannan, Jayaprakash, Life Horoscope, Rajayogam, Rajeshwari Chellaiah, Mahesh Iyer and others | Lagna, nakshatra, rasi and combination traits |

**Written:** Wikipedia (Vakri grahas, Avastha), onlinejyotish (neecha bhanga) and other pages listed in `references/sources.md`.

## Files

| Path | What |
|---|---|
| `SKILL.md` | Instructions Claude follows: inputs, output format, follow-ups, honesty rules |
| `scripts/jathagam.py` | Chart maths, dasa tree, transits, porutham, technical HTML |
| `scripts/predict.py` | Prediction engine and the person and couple HTML reports |
| `scripts/twins.py` | Chart-twins window, Wikidata lookup by date, tally |
| `references/method.md` | The prediction rules and how to write predictions |
| `references/porutham.md` | Matching rules and thresholds |
| `references/planet-in-house.json` | 9 planets × 12 boxes, classical readings with sources |
| `references/research/` | Notes from the Tamil channels and classical texts (calculation rules, traits), with video IDs |
| `references/twins-brief.md` | The research brief used for chart-twins lookups |
| `references/glossary.md`, `references/sources.md` | Tamil terms and everything consulted |

## Notes

- Charts and dates are computed. The interpretation is traditional Tamil astrology.
- The engine was calibrated against a working jothidar's handwritten chart. That calibration case is private. The
  public selftest uses a made-up chart.
- No personal birth data is included in this repository.
