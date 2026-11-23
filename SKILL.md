---
name: tamil-jathagam
description: Tamil astrology predictions in the style of a Tamil Nadu jothidar. Gives what to expect year by year and month by month (career, money, studies, travel, love, home, health) for one person, or compatibility plus a relationship timeline for a couple. Covers rasi and nakshatram, rasi and amsam charts in South Indian boxes, dasa/bhukti/antaram, 7½ Sani, Chevvai dosham, remedies and 10-porutham matching. Use when someone gives a birth date, time and place and asks for predictions, their rasi or nakshatram, jathagam, dasa, porutham or compatibility. Also use to read or translate a handwritten Tamil jathagam.
---

# Tamil jathagam: predictions first

People want **what will happen and when**, not which planet sits in which house. The chart maths is
the back end. Lead every answer with predictions, and keep the technical chart in a collapsed
appendix or a separate file.

The engine was calibrated on a real Chennai jothidar's handwritten notes. It reproduces the boxes,
dasa balance and every bhukti/antaram date to the day (the calibration notes are kept private). Readings are
traditional astrology, not science. Say that once, plainly.

## 1. Inputs: name, date of birth, time of birth, place of birth

That's all a user has to give. You resolve the rest:
- **Place → `--lat --lon`:** use the city's coordinates (city-level is enough; it only moves the
  lagnam by minutes). If the place is ambiguous ("Punjab", "Ecuador"), use the main city and tell them.
- **Timezone → `--tz`:** pass the IANA zone (`Asia/Kolkata`, `America/Toronto`, `America/Guayaquil`).
  The script gets the historically correct offset for that date, including DST and old offsets.
- **No time:** rasi is usually safe for the whole day; star and lagnam may not be. Show ranges and
  ask for the time.
- **"Around midnight":** confirm which night. Families often write the next day's date.
- **Couples:** you need both people. All matching counts run from the girl's star.
- Treat birth data as private. Don't put it into online calculators or search for the people.
  One exception: the chart-twins research (section 5) sends only birth **dates** (never the name,
  time or place) to Wikidata and the web, to find *public* people born on them.

## 2. Run it

```bash
python3 -m venv .venv && .venv/bin/pip install -q pyswisseph
.venv/bin/python scripts/jathagam.py selftest && .venv/bin/python scripts/predict.py selftest && .venv/bin/python scripts/twins.py selftest

# one person: predictions report (also writes <name>.json for later matching)
.venv/bin/python scripts/predict.py person --name "Name" --date 2003-03-14 --time 06:40 \
    --tz Asia/Kolkata --lat 9.93 --lon 78.12 --place Madurai --years 3 --out out/

# couple: girl first (all counts run from the girl's star)
.venv/bin/python scripts/predict.py couple out/girl.json out/boy.json --out out/

# optional technical sheet (all tables) for the jothidar-minded
.venv/bin/python scripts/jathagam.py chart --name "Name" ... --out out/
```

## 3. Output format: always this, in chat and in HTML

Readers want a timeline and practical advice, not astrology lessons. **Every chat answer from this
skill uses these sections, in this order.** Run `predict.py`, read the HTML/JSON, then write the
sections in your own words. Keep the engine's dates, periods and Good / Mixed / Tough verdicts.

### Chat template (couple)

```
## Timeline if they get together

| When | Him (Name) | Her (Name) | As a couple |
|---|---|---|---|
| 16 Nov 2026 → 25 Jan 2027 | 2–3 sentences: what his life feels like, why (in plain words: "his 7½-year Saturn test is in its last lap"), what it's good for. | Same for her. | **Green light / Warm / Patience / Testing / Steady.** 2–3 sentences: how they'll feel together, who's keener or under pressure, and the one thing to do in this stretch. |
(one row per engine period: usually 6–12 rows over 3 years, each 1½–5 months, cut where something actually changes)

## For him: what to do and what not to do with <her name>

**The timing:** one short paragraph on the best window and why.
**Know who she is:** one short paragraph, her nature in plain words (from her star and Moon sign).

**Do**
1. **Bold one-line instruction.** 1–3 sentences: why (tie it to her nature or the timing) and how, with a concrete example ("Something simple, like 'There's a ___ Saturday, want to go with me?'").
(6–8 items)

**Don't**
1. **Bold one-line instruction.** 1–3 sentences: why it backfires with her, and what to do instead.
(6–8 items)

**How to read her:** interested signs vs not-interested signs, and how to take a no gracefully.

## Expectation vs reality
| Expectation | Reality |   (3–4 rows: the score, the green-light window, the testing stretch, "astrology decides")

## Score
6.5/10 Tamil porutham · 26/36 North Indian guna · **Good match**. One paragraph: what the score
means, Rajju and Vedhai, best and hardest stretch, and a closing honest line.
```

Write the do's and don'ts for whoever asked (usually "for him", "for her", or "for both"). If no
one is specified, write "For both".

### Chat template (one person)

```
## Your next 3 years
| When | What to expect |   one row per engine period (1½–5 months each), each Good/Mixed/Tough + 3–4 sentences (feel, why, what it's good for, one move to make)
## Do   (6–8 numbered, bold instruction + 1–3 sentences why/how, dated where possible)
## Don't   (6–8 numbered, same style)
## Summary   (one paragraph: strongest stretch, hardest stretch, current chapter, closing line)
## Commonly observed behaviours & lifestyle   (always last; 7–10 numbered items, bold trait + 1–2 plain sentences)
```

No Expectation vs reality table and no "people born with your boxes" section in one-person readings.

**How to build "Commonly observed behaviours & lifestyle"** (method from `references/research/traits-classical.md`
and `traits-tamil-youtube.md`):
1. Lead with the lagnam (how they come across and act), read with its ruler's strength and box; if the Moon is clearly
   stronger and the lagnam ruler weak, lead with the Moon sign instead.
2. Inner side from the Moon: star first, then Moon sign, then the pada's tone (its navamsa lord).
3. Planets in the lagnam or joined to the Moon override sign traits where they clash; the ruler's strength sets how
   strong a trait is, not which trait.
4. Keep only traits **two or more layers agree on**; write a real clash as a pattern ("calm outside, flares when pushed").
5. Use the twins tally (section 5) only as quiet confirmation: prefer traits it also shows. Never mention twins,
   counts or other people in the text.
6. Cover, where supported: temperament, mind, work style, money habits, friends and family, love style, food / sleep /
   health tendencies. Plain words, no house numbers, no Sanskrit. Write the items into `summary.json` `takeaways` as
   `[bold, text]` pairs and rerun `predict.py person ... --traits <summary.json>` so the HTML matches.

### How the timeline is cut
Rows aren't fixed lengths. The engine cuts wherever something changes in day-to-day life: every
sub-sub-period (antaram) change for either person, and every Saturn, Jupiter or Rahu/Ketu sign
change. Pieces are glued into chunks of about 4 months, always breaking at a big change (sub-period
change or Saturn/Jupiter/Rahu move). A transit sentence only appears in the row where that transit
changes, so rows don't repeat. Use the engine's exact start dates in the table.

### Style rules
- Crisp and a little vivid: talk like a friend who knows astrology. Bold the key phrase in each item.
- No house numbers and no "bhukti/antaram" in the main text. "Saturn's 7½-year test" is fine; "Saturn
  transiting the 12th from natal Moon" isn't. Tamil terms only for flavour (rasi, star names).
- Keep the ups and the downs. Never sugar-coat a Testing or Tough stretch, and always pair it with what to do.
- Collapse the technical detail (charts, porutham table) into "Behind the reading" in HTML. In chat,
  leave it out unless asked.

The HTML (`predict.py`) follows the same order. Person: Timeline → Do's and don'ts → Summary → Behind the reading → Commonly observed behaviours & lifestyle. Couple: Timeline → Do's and don'ts → Expectation vs reality → Score.

## 4. Follow-up questions

People will ask more. Answer from the same run (the JSON has the full dasa tree and transits), in
the same plain style, always with dates:
- **"When will I get a job / marry / go abroad?"** Use the suggested windows for that area (top 3,
  exact dates) together with the timeline rows marked "Good for: …". Give the best window first,
  then the backup, and say it's a favourable period, not a guarantee.
- **"What about March / next year?"** Find the timeline row and the antaram covering it, and explain
  what that planet does from its box (references/planet-in-house.json, positive line; reword
  classical language into modern words).
- **"Why is this period tough?"** Name the cause in plain words (Saturn's 7½-year test, a planet
  that rules a difficult box), then give what to do and the remedy (method.md, Remedies).
- **"Are we compatible?" for a new person:** run `predict.py person` for them, then `couple`.
- **"What's my rasi / star / lagnam?"** Answer directly from the JSON; the boxes are in the HTML.
- **"Is this accurate?"** Charts and dates are computed (Swiss Ephemeris, Lahiri), the same engine
  Prokerala and AstroSage use. The interpretation is traditional astrology, not science.
- Larger horizon: rerun with `--years 5`.

## 5. Chart twins (background research, one-person readings)

On by default for every one-person reading (skip if the user says no). It finds public people born
while all nine grahas sat in the same boxes and studies their character and lifestyle. The result is
used only as quiet confirmation for the "Commonly observed behaviours & lifestyle" section (section 3).

1. Right after `predict.py person`, run `scripts/twins.py find out/<name>.json --out out/`. It writes
   `out/<name>-twins/window.json` (the exact window, usually 1–2 days because the Moon moves fast)
   and `people.tsv` (Wikidata, top 150 by fame; `--max` to change).
2. Split `people.tsv` into batches of about 30 and spawn **background** subagents, at most 6 in all
   (5 batches + 1 "extras" batch for creators/actors not on Wikidata). Each one gets
   `references/twins-brief.md`, its batch rows and the output path `out/<name>-twins/profiles-NN.json`.
   Don't wait: deliver the main reading now and say the twins study is running.
3. When they finish: `twins.py tally out/<name>-twins/` → `summary.json`. Use it to confirm or drop traits
   while building the behaviours section (section 3), write the final items into `takeaways`, then rerun
   `predict.py person ... --traits out/<name>-twins/summary.json`.
4. **Never change the reading's format** and never show the twins study itself: no window, counts, names
   or "people born with your boxes" section. If the study hasn't finished, build the behaviours section
   from the chart layers alone.

## 6. Honesty rules

- Every date comes from the script. Don't hand-compute or invent dates.
- Near a star, lagnam or dasa change (about ±30 min of birth time), flag the uncertainty.
- Conventions vary between jothidars (Chevvai houses, Maandhi, window choice). Name the convention
  you used when it matters.
- The calibration case reproduces the jothidar's **chart and dates** exactly. His **window choices**
  are only partly reproduced (see method.md, "How well the engine matches the jothidar").

## Files
- `scripts/predict.py`: prediction engine and the person and couple HTML reports (`selftest` included)
- `scripts/twins.py`: chart-twins window, Wikidata list, tally (`selftest` included)
- `references/research/`: Tamil YouTube + classical research (calculation rules, behaviour/lifestyle traits, with video ids)
- `references/twins-brief.md`: research brief and JSON format for the twins subagents
- `scripts/jathagam.py`: chart maths, dasa tree, transits, porutham, technical HTML (`selftest` included)
- `references/method.md`: the jothidar's method, the prediction rules, and how to write predictions
- `references/porutham.md`: matching rules and thresholds
- `references/planet-in-house.json`: 9 planets × 12 boxes, classical readings (Phaladeepika, Saravali, Bhrigu Sutras, AstroVed…) with source keys
- `references/planet-in-house-sources.md`: every page opened for those readings, and where they disagree
- `references/glossary.md`: Tamil abbreviations
- `references/sources.md`: everything consulted
