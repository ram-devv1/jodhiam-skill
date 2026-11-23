# Reading method

This is how the calibration jothidar (a working Tamil Nadu jothidar) builds a reading, and how to
reproduce it with `jathagam.py`. Anything marked **(observed)** was inferred from the notes, not
stated by the jothidar.

## How popular calculators do it (and how this skill matches)

Prokerala, AstroSage, Astro-Vision, Jagannatha Hora and most Tamil jathagam apps use **Swiss
Ephemeris** (or equivalent) with **Lahiri (Chitrapaksha) ayanamsa** by default, houses counted
sign by sign from the lagnam, and the **South Indian fixed grid** with Rasi (D-1) and Navamsa (D-9)
charts. Lahiri has been the Indian government's standard since 1956. KP, Raman and Fagan-Bradley
are the alternatives. Fagan-Bradley is about 0.5° away from Lahiri, which can move a star or lagnam
near a boundary. Traditional Vakya panchangams use older formulas and can differ from these
(Thirukanitha) calculations by a few hours on star changes. When a user's printed jathagam
disagrees near a boundary, that's usually why.

This skill uses the same defaults (Swiss Ephemeris/Moshier + Lahiri + whole sign + South Indian
grid), plus the calibration jothidar's conventions below.

## Calculation conventions (verified against the notes)

| Item | Convention | How it was verified |
|---|---|---|
| Zodiac | Sidereal, **Lahiri** ayanamsa | All planets land in the jothidar's boxes |
| Houses | Whole sign from lagnam | "Mars 2nd" and "Maandhi 5th" match |
| Amsam | Navamsa = floor(longitude × 9 / 30) mod 12 | All ten planets and the amsa lagnam match |
| Dasa | Vimshottari from the Moon's nakshatra, **365.25-day years** | Balance "Venus 8y 8m 8d" and every bhukti end matches to the day (360 days was months off) |
| Antaram | bhukti length × planet years / 120 | All 5 antaram dates match (one is 1 day off at a midnight boundary) |
| Maandhi | Lagnam at the **end** of Saturn's 1/8 portion (day from sunrise, night from sunset; night sequence starts from the 5th lord from the weekday lord) | Only "end" puts Maandhi in Kadagam in both boxes. "Start" and "middle" give Mithunam |
| Box layout | South Indian, fixed signs: Meenam top-left, then clockwise | Matches the hand-drawn boxes |

## Page order of a reading

1. **Header:** name, D.O.B, T.O.B, P.O.B, star-pada, rasi, lagnam.
2. **Rasi box and amsam box.** The lagnam is marked with a diagonal line and ல. Abbreviations are in glossary.md.
3. **தசா இருப்பு (dasa balance at birth)** in years, months and days.
4. **Chart summary in arrow shorthand**, one fact per line:
   - `லக்னம் ⇒ மீனம்`
   - `லக்னாதிபதி ⇒ குரு ⇒ 8-ல்` (lagna lord and its house)
   - `செவ் ⇒ ஆட்சி ⇒ 2-ல்` (own-sign or exalted planets and their house)
   - `சூரி, புத ⇒ சேர்க்கை` (conjunctions worth noting: benefic/malefic pairs and house lords)
   - `குரு, சுக் ⇒ பரிவர்த்தனை` (sign exchanges)
   - `மாந்தி ⇒ 5-ல்`
   - a boxed `7½ சனி` when Saturn is in the 12th, 1st or 2nd from the Moon sign
5. **Current dasa–bhukti and its antarams with dates**, then the next bhukti.
6. **Event windows** (see below).
7. **Character line(s)**, short. Example from the notes: "Technically sound person. Hard worker."
8. **Predictions:** short imperative lines, mixing Tamil and English.
9. **பரிகாரம் (remedies)**, numbered, specific (day, time, count), ending with சுபம்.

## House significations

| House | Main meanings |
|---|---|
| 1 | Self, body, health, temperament |
| 2 | Family, money, speech, food, early education |
| 3 | Courage, siblings, short travel, communication, skills |
| 4 | Mother, home, vehicles, basic education, peace of mind |
| 5 | Intelligence, studies, children, romance, mantra and devotion |
| 6 | Service jobs, competition, debts, illness, enemies |
| 7 | Spouse, partnership, business, public dealings |
| 8 | Obstacles, sudden events, research, hidden matters, longevity |
| 9 | Fortune, father, guru, higher studies, long-distance travel |
| 10 | Career, status, actions |
| 11 | Gains, income, friends, fulfilment of desires |
| 12 | Expenses, foreign lands, sleep, losses, liberation |

| Topic | Houses to read |
|---|---|
| Job / job change | 2, 6, 10, 11 (the jothidar wrote **6, 10 & 9** in the notes) |
| Higher studies / Masters | 4, 5, 9, 11 |
| Abroad | 9 and 12 (3 for short trips) |
| Marriage | 2, 7, 11 (7th lord, Venus, and Jupiter for a woman's chart) |
| Health caution | 1, 6, 8, 12, and the 7½ / ashtama Sani periods |

## Picking event windows

1. List the antarams for the current and next two bhuktis (in the JSON under `dasa`).
2. A planet **signifies** a house if it owns the house, sits in it, or its star lord owns or sits in
   it. Rahu and Ketu also give the results of their sign lord.
3. Candidates are antarams whose lord signifies the topic's houses, inside a bhukti whose lord also
   connects to the topic.
4. Merge neighbouring candidates into a window. **Always start and end windows on exact antaram
   boundaries.** The jothidar's windows all do.
5. Trim with transits. Avoid starting a window in the middle of a harsh Saturn phase if Jupiter is
   unfavourable from the Moon.
6. Give two windows (① and ②) when there's a gap. That's the jothidar's habit.

**(Observed) The selection isn't fully mechanical.** In the worked example, job window ① =
Moon–Mercury–**Saturn** antaram (Saturn rules the 11th, gains) through the end of Moon–Ketu–**Moon**.
It skips the Mars and Rahu antarams, even though Mars scores high on job houses. Window ② starts at
Moon–Ketu–**Jupiter** (Jupiter rules the 10th, career) and ends after Moon–Venus–**Rahu**. Masters
windows started on Jupiter or Moon (5th lord) antarams. So the rule of thumb is to start a window
on the antaram of a key house lord (10th or 11th for jobs, 5th or 9th for studies) and run it until
the next run of malefic antarams. State that the window is a judgement call.

The jothidar also revised windows between two visits a year apart ( ① end 13-03-2028 → 31-03-2028,
② end 21-03-2029 → 20-06-2029). Windows are soft. Present them as "favourable periods", not deadlines.

## Transits (from the Moon sign)

| Saturn from Moon | Name | Traditional reading |
|---|---|---|
| 12, 1, 2 | **7½ Sani** (Ezharai Sani) | Stress, pressure, anxiety, delays, sleeplessness, health (stomach), expenses. The jothidar's advice: proper food and sleep, don't rush, don't over-trust |
| 4 | Ardhashtama Sani | Home and mother worries, moving, mental unrest |
| 7 | Kantaka Sani | Partner and relationship strain, business friction |
| 8 | Ashtama Sani | Hardest: health, obstacles, sudden setbacks |
| 3, 6, 11 | Good | Effort pays, enemies weaken, gains |

| Jupiter from Moon | Reading |
|---|---|
| 2, 5, 7, 9, 11 | Favourable: money, studies, marriage, fortune, gains. Jupiter in the 7th is the classic marriage trigger |
| others | Neutral to weak; 8th and 12th bring expenses or detachment |

## Prediction style (from the notes)

The jothidar writes short, practical, imperative lines. Each one ties to a placement or period:
- "உடல் நலத்தில் கவனம் அவசியம்." Take care of health (7½ Sani).
- "அவசரப்படாமல் நிதானமாகச் செயல்படவும்." Don't rush; act calmly (Mars in the 2nd, Moon–Mars in Mesham).
- "யாரையும் முழுமையாக நம்பி personal விஷயத்தை share பண்ணக்கூடாது." Don't share personal matters with anyone you can't fully trust.
- "உணவில் கட்டுப்பாடு." Control your diet (stomach, 2nd house, Saturn).
- "Night travel-ஐத் தவிர்க்கவும்." Avoid night travel (Saturn period).
- "உன் skill-ஐ prove பண்ணும் நேரம்." A time to prove your skills (Mercury bhukti, 3rd/11th).

Keep it to about 6–10 lines. Each line should be useful advice rather than a fate statement.

## Remedies (பரிகாரம்)

Match the remedy to the planet causing the trouble. These are traditional practices. Present them
as optional devotional practices, never as paid rituals someone must buy.

| Planet / period | Remedy used by the jothidar or commonly given |
|---|---|
| Saturn, 7½ Sani | Hanuman Chalisa daily (the jothidar: listen 3× a day); Saneeswara abhishekam on a Saturday; feed crows; charity on Saturdays |
| Moon (Moon dasa, weak Moon) | **Every Monday, 8–9 pm, light 2 ghee lamps at the house entrance** (the jothidar); Monday fasting; Ambal/Parvati worship |
| Mars / Chevvai dosham | Murugan worship on Tuesdays, Kanda Sashti Kavasam |
| Rahu / Ketu | Durga (Rahu) or Vinayagar (Ketu) worship, Rahu kalam lamp |
| Jupiter | Thursday Dakshinamurthy worship |

## Prediction engine (`predict.py`)

**Period quality:** each antaram gets a score from the functional nature of the dasa, bhukti and
antaram lords for this lagnam (Parashara):
- Lords of the 1st, 5th and 9th houses give good results. A planet owning both a kendra and a trikona is a yogakaraka (best).
- Lords of the 3rd, 6th, 8th, 11th and 12th give trouble, unless they also own a trikona.
- Kendra lords (4, 7, 10) go neutral.
- Adjustments: placed in the 6th/8th/12th −; own sign or exalted +; debilitated −; in a sign exchange (parivartanai) + (it acts as if in its own sign).
- Rahu and Ketu act like their sign lord; they're good in the 3rd, 6th and 11th.

The transit score is added on top (Saturn, Jupiter and Rahu from the Moon sign: Jupiter good in
2/5/7/9/11; Saturn and Rahu good in 3/6/11; Saturn 12/1/2/4/7/8 hard). Tone: Good / Mixed / Tough.

**Wording:** lines come from the houses the bhukti and antaram lords own or occupy (the HOUSE_TXT
table), in the positive or cautionary version to match the tone, plus the planet's natural meaning
(KARAKA).

**Areas and windows:** an area is "on" when the bhukti lord signifies its houses (own, occupy, or via
star lord), the antaram lord owns or occupies one of them, a key house is involved, and the tone
isn't Tough. Neighbouring active antarams merge (gaps ≤ 31 days). Windows under 21 days are dropped.
The top 3 are kept, ranked by mean score plus an area-specific transit bonus (for example, Jupiter
5/7/11 from the Moon for love).

| Area | Houses | Key house |
|---|---|---|
| Career / job | 2, 6, 10, 11 | 10, 6 |
| Money / gains | 2, 11 | 11, 2 |
| Studies | 4, 5, 9 | 4, 5, 9 |
| Travel / abroad | 3, 9, 12 | 12, 9 |
| Love / marriage | 2, 5, 7, 11 (+ Venus) | 7, 5 |
| Home / property | 4, 11 | 4 |

**Report periods:** cut at every antaram change (either person) and every Saturn, Jupiter and
Rahu/Ketu sign change. Pieces are glued into ~120-day chunks, always breaking at a major cut
(bhukti change or Saturn/Jupiter/Rahu ingress) once a chunk is ≥45 days; the maximum is ~185 days.
Each person's line = the headline for the planet running most of those months (its antaram), by tone
+ that planet's natal-box reading (references/planet-in-house.json) + the Saturn / Jupiter / Rahu
transit line, shown only when it changed since the previous row (Saturn by its main sign, ignoring
retrograde blips).

**Couple column**, sampled monthly: love signals (each person's love area on, Jupiter 5/7/11 from
either Moon) vs strain signals (Saturn 7th/8th from either Moon, either person Tough).
Green light = 2+ love and no strain · Testing = 2+ strain · Patience = exactly one strain · Warm = love only · Steady = neither.

### How well the engine matches the jothidar

- **Exact:** boxes, dasa balance, bhukti and antaram dates, 7½ Sani dates, summary facts.
- **Chapters:** for the calibration chart, Moon–Mercury (Aug 2026 → Jan 2028) reads as gains,
  studies and skills. That's in line with the jothidar's "time to prove your skills, appreciation,
  knowledge increases".
- **Job windows: not reproduced.** The jothidar gave ① 24-10-2027 → 31-03-2028 and
  ② 14-05-2028 → 20-06-2029. Almost every antaram in this chart touches a job house, so house logic
  can't separate them; he chooses at the bhukti level (the late Mercury, Ketu and early Venus
  sub-periods). When you present windows, lean on the chapters and say the exact windows are a
  judgement call.

## Character notes for the 27 stars

Keep this short and balanced: one strength and one weakness per star, and connect it to the chart
(for example, Bharani-3 plus a strong Mars gives "decisive, but act calmly").
