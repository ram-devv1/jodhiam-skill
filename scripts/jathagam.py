#!/usr/bin/env python3
"""Tamil jathagam calculator: rasi + amsam (navamsa) charts in South Indian boxes,
Vimshottari dasa / bhukti / antaram, Maandhi, 7½ Sani and Guru transits, Chevvai
dosham, yogas, and 10-porutham + 36-guna matching.

Conventions (calibrated against a Chennai jothidar's handwritten notes, kept private): Lahiri ayanamsa, whole-sign houses from lagnam,
365.25-day dasa years, Maandhi = lagnam at the END of Saturn's portion of the day/night.

  python jathagam.py chart --name "Name" --date 2003-03-14 --time 06:40 --tz Asia/Kolkata \
      --lat 9.93 --lon 78.12 --place Madurai --out ./out
  python jathagam.py match out/girl.json out/boy.json --out ./out
  python jathagam.py selftest
"""
import argparse, datetime as dt, html, json, os, sys
import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)
FLG = swe.FLG_SIDEREAL | swe.FLG_MOSEPH  # Moshier: no ephemeris files needed, arc-second accuracy
Y = 365.25

RASI = ['Mesham', 'Rishabam', 'Mithunam', 'Kadagam', 'Simmam', 'Kanni', 'Thulam', 'Viruchigam', 'Dhanusu', 'Magaram', 'Kumbam', 'Meenam']
RASI_TA = ['மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி', 'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்']
STAR = ['Ashwini', 'Bharani', 'Karthigai', 'Rohini', 'Mirugasirisham', 'Thiruvathirai', 'Punarpoosam', 'Poosam', 'Ayilyam', 'Magam', 'Pooram', 'Uthiram', 'Hastham', 'Chithirai', 'Swathi', 'Visakam', 'Anusham', 'Kettai', 'Moolam', 'Pooradam', 'Uthiradam', 'Thiruvonam', 'Avittam', 'Sadhayam', 'Poorattathi', 'Uthirattathi', 'Revathi']
STAR_TA = ['அசுவினி', 'பரணி', 'கார்த்திகை', 'ரோகிணி', 'மிருகசீரிடம்', 'திருவாதிரை', 'புனர்பூசம்', 'பூசம்', 'ஆயில்யம்', 'மகம்', 'பூரம்', 'உத்திரம்', 'அஸ்தம்', 'சித்திரை', 'சுவாதி', 'விசாகம்', 'அனுஷம்', 'கேட்டை', 'மூலம்', 'பூராடம்', 'உத்திராடம்', 'திருவோணம்', 'அவிட்டம்', 'சதயம்', 'பூரட்டாதி', 'உத்திரட்டாதி', 'ரேவதி']
PLANETS = {'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE}
ABBR = {'Lagna': 'ல', 'Sun': 'சூரி', 'Moon': 'சந்', 'Mars': 'செவ்', 'Mercury': 'புத', 'Jupiter': 'குரு', 'Venus': 'சுக்', 'Saturn': 'சனி', 'Rahu': 'ரா', 'Ketu': 'கே', 'Maandhi': 'மா'}
LORD = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
OWN = {'Sun': [4], 'Moon': [3], 'Mars': [0, 7], 'Mercury': [2, 5], 'Jupiter': [8, 11], 'Venus': [1, 6], 'Saturn': [9, 10]}
EXALT = {'Sun': 0, 'Moon': 1, 'Mars': 9, 'Mercury': 5, 'Jupiter': 3, 'Venus': 11, 'Saturn': 6}
DASA = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
DASA_YRS = [7, 20, 6, 10, 7, 18, 16, 19, 17]
WEEK = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']  # weekday order, Sunday = 0
SPAN = 40 / 3


def rasi(lon): return int(lon / 30) % 12
def star(lon): return int(lon / SPAN) % 27
def pada(lon): return int((lon % SPAN) / (SPAN / 4)) + 1
def amsam(lon): return int(lon * 9 / 30) % 12
def tz_hours(tz, d, t):
    """Accept a UTC offset (5.5 / '-5') or an IANA zone name ('Asia/Kolkata'); the zone name gives the
    historically correct offset for that date, including DST and old offsets (e.g. India +6:30 in 1942-45)."""
    try:
        return float(tz)
    except (TypeError, ValueError):
        from zoneinfo import ZoneInfo  # stdlib; on Windows also `pip install tzdata`
        return ZoneInfo(tz).utcoffset(dt.datetime.combine(d, t)).total_seconds() / 3600


def utc_jd(d, t, tz): return swe.julday(d.year, d.month, d.day, t.hour + t.minute / 60 - tz)


def local(jd, tz):
    y, m, d, h = swe.revjul(jd + tz / 24)
    return dt.datetime(y, m, d) + dt.timedelta(hours=h)


def ascendant(jd, lat, lon): return swe.houses_ex(jd, lat, lon, b'W', FLG)[1][0]


def maandhi(jd, lat, lon, tz):
    """Lagnam at the END of Saturn's 1/8th portion (day from sunrise, night from sunset).
    The night sequence starts from the 5th lord from the weekday lord. Hindu day starts at sunrise."""
    geo = (lon, lat, 0)
    rise = lambda j: swe.rise_trans(j, swe.SUN, swe.CALC_RISE | swe.BIT_DISC_CENTER, geo, flags=FLG)[1][0]
    sset = lambda j: swe.rise_trans(j, swe.SUN, swe.CALC_SET | swe.BIT_DISC_CENTER, geo, flags=FLG)[1][0]
    r = rise(jd - 1)
    if rise(r + 0.01) <= jd: r = rise(r + 0.01)
    s = sset(r)
    wd = (local(r, tz).weekday() + 1) % 7  # python Mon=0 -> Sun=0
    if jd < s:  # day birth
        start, part, first = r, (s - r) / 8, wd
    else:       # night birth
        start, part, first = s, (rise(s) - s) / 8, (wd + 4) % 7
    k = (6 - first) % 7  # Saturn's slot in the sequence
    t = start + (k + 1) * part
    return ascendant(t, lat, lon), local(t, tz)


def ymd(years):
    y = int(years); m = (years - y) * 12; d = (m - int(m)) * (Y / 12)
    return f"{y}y {int(m)}m {int(d)}d"


def dasa_tree(jd_birth, moon_lon, tz, levels_until=None):
    """Mahadasa -> bhukti -> antaram, dates in local time. 365.25-day years."""
    s = star(moon_lon); lord = s % 9
    elapsed = (moon_lon % SPAN) / SPAN
    t = jd_birth - elapsed * DASA_YRS[lord] * Y
    tree = []
    for i in range(9):
        L = (lord + i) % 9; md_len = DASA_YRS[L] * Y
        md = {'lord': DASA[L], 'start': t, 'end': t + md_len, 'bhuktis': []}
        bt = t
        for j in range(9):
            B = (L + j) % 9; b_len = md_len * DASA_YRS[B] / 120
            bh = {'lord': DASA[B], 'start': bt, 'end': bt + b_len, 'antarams': []}
            at = bt
            for k in range(9):
                A = (B + k) % 9; a_len = b_len * DASA_YRS[A] / 120
                bh['antarams'].append({'lord': DASA[A], 'start': at, 'end': at + a_len}); at += a_len
            md['bhuktis'].append(bh); bt += b_len
        tree.append(md); t += md_len
    fmt = lambda j: local(j, tz).strftime('%d-%m-%Y')
    for md in tree:
        for x in [md] + md['bhuktis'] + [a for b in md['bhuktis'] for a in b['antarams']]:
            x['start_jd'], x['end_jd'] = x['start'], x['end']; x['start'], x['end'] = fmt(x['start']), fmt(x['end'])
    return tree, ymd((1 - elapsed) * DASA_YRS[lord]), DASA[lord]


def ingresses(body, jd_from, years):
    j = jd_from; s0 = rasi(swe.calc_ut(j, body, FLG)[0][0])
    while rasi(swe.calc_ut(j - 1, body, FLG)[0][0]) == s0: j -= 1  # back to the real ingress date
    out, prev = [], None
    while j < jd_from + years * Y:
        s = rasi(swe.calc_ut(j, body, FLG)[0][0])
        if s != prev: out.append((j, s)); prev = s
        j += 1
    return out


SANI_PHASE = {12: '7½ Sani (Viraya, 1st phase)', 1: '7½ Sani (Janma, peak)', 2: '7½ Sani (Paadha, last phase)',
              4: 'Ardhashtama Sani (4th)', 7: 'Kantaka Sani (7th)', 8: 'Ashtama Sani (8th)'}


def chart(name, date, time, tz, lat, lon, place=''):
    d = dt.date.fromisoformat(date); t = dt.time.fromisoformat(time)
    tz = tz_hours(tz, d, t)
    jd = utc_jd(d, t, tz)
    lons = {k: swe.calc_ut(jd, v, FLG)[0][0] for k, v in PLANETS.items()}
    lons['Ketu'] = (lons['Rahu'] + 180) % 360
    lons['Maandhi'], mt = maandhi(jd, lat, lon, tz)
    asc = ascendant(jd, lat, lon); lg = rasi(asc)
    house = lambda l: (rasi(l) - lg) % 12 + 1
    planets = {}
    for k, l in lons.items():
        dig = ('exalted (உச்சம்)' if EXALT.get(k) == rasi(l) else 'debilitated (நீசம்)' if k in EXALT and (EXALT[k] + 6) % 12 == rasi(l)
               else 'own sign (ஆட்சி)' if rasi(l) in OWN.get(k, []) else '')
        planets[k] = dict(lon=round(l, 3), rasi=RASI[rasi(l)], deg=round(l % 30, 2), house=house(l), star=STAR[star(l)],
                          pada=pada(l), star_lord=DASA[star(l) % 9], amsam=RASI[amsam(l)], dignity=dig)
    moon = lons['Moon']; mr = rasi(moon)
    # yogas / notes the jothidar writes in the chart summary
    signs = {}
    for k in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']: signs.setdefault(rasi(lons[k]), []).append(k)
    seven = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    exch = sorted({tuple(sorted((a, b))) for a in seven for b in seven if a != b
                   and LORD[rasi(lons[a])] == b and LORD[rasi(lons[b])] == a})
    mars = {ref: (rasi(lons['Mars']) - r) % 12 + 1 for ref, r in [('lagnam', lg), ('moon', mr), ('venus', rasi(lons['Venus']))]}
    tree, bal, bal_lord = dasa_tree(jd, moon, tz)
    now = swe.julday(*dt.date.today().timetuple()[:3], 0)
    sani = [dict(date=local(j, tz).strftime('%d-%m-%Y'), rasi=RASI[s], from_moon=(s - mr) % 12 + 1,
                 phase=SANI_PHASE.get((s - mr) % 12 + 1, '')) for j, s in ingresses(swe.SATURN, now - 3 * Y, 15)]
    guru = [dict(date=local(j, tz).strftime('%d-%m-%Y'), rasi=RASI[s], from_moon=(s - mr) % 12 + 1,
                 good=(s - mr) % 12 + 1 in (2, 5, 7, 9, 11)) for j, s in ingresses(swe.JUPITER, now - Y, 8)]
    return dict(
        name=name, date=date, time=time, tz=tz, place=place, lat=lat, lon=lon,
        star=STAR[star(moon)], star_ta=STAR_TA[star(moon)], pada=pada(moon), rasi=RASI[mr], rasi_ta=RASI_TA[mr],
        lagnam=RASI[lg], lagnam_ta=RASI_TA[lg], lagnam_deg=round(asc % 30, 2), amsa_lagnam=RASI[amsam(asc)],
        weekday=d.strftime('%A'), maandhi_time=mt.strftime('%H:%M'),
        dasa_balance=f"{bal_lord} {bal}", planets=planets,
        lagna_lord=dict(planet=LORD[lg], house=planets[LORD[lg]]['house']),
        conjunctions=[[RASI[s], v] for s, v in signs.items() if len(v) > 1],
        exchanges=[list(e) for e in exch],
        chevvai=dict(houses=mars, dosham=any(h in (2, 4, 7, 8, 12) for h in mars.values()),
                     mars_own_or_exalted=bool(planets['Mars']['dignity'])),
        star_info=dict(gana=gana(star(moon)), yoni=YONI[star(moon)], rajju=RAJJU[star(moon)], nadi=nadi(star(moon))),
        dasa=tree, sani_transits=sani, guru_transits=guru,
        _idx=dict(star=star(moon), rasi=mr, moon=moon))


def current(tree, jd=None):
    jd = jd or swe.julday(*dt.date.today().timetuple()[:3], 0)
    for md in tree:
        for b in md['bhuktis']:
            if b['start_jd'] <= jd < b['end_jd']: return md, b
    return None, None


# ---------------- matching ----------------
GANA = {0: 'Deva', 4: 'Deva', 6: 'Deva', 7: 'Deva', 12: 'Deva', 14: 'Deva', 16: 'Deva', 21: 'Deva', 26: 'Deva',
        1: 'Manushya', 3: 'Manushya', 5: 'Manushya', 10: 'Manushya', 11: 'Manushya', 19: 'Manushya', 20: 'Manushya', 24: 'Manushya', 25: 'Manushya'}
def gana(n): return GANA.get(n, 'Rakshasa')
YONI = ['Horse', 'Elephant', 'Sheep', 'Serpent', 'Serpent', 'Dog', 'Cat', 'Sheep', 'Cat', 'Rat', 'Rat', 'Cow', 'Buffalo', 'Tiger', 'Buffalo', 'Tiger', 'Deer', 'Deer', 'Dog', 'Monkey', 'Mongoose', 'Monkey', 'Lion', 'Horse', 'Lion', 'Cow', 'Elephant']
YA = ['Horse', 'Elephant', 'Sheep', 'Serpent', 'Dog', 'Cat', 'Rat', 'Cow', 'Buffalo', 'Tiger', 'Deer', 'Monkey', 'Mongoose', 'Lion']
YT = [[4,2,2,3,2,2,2,1,0,1,3,3,2,1],[2,4,3,3,2,2,2,2,3,1,2,3,2,0],[2,3,4,2,1,2,1,3,3,1,2,0,3,1],[3,3,2,4,2,1,1,1,1,2,2,2,0,2],
      [2,2,1,2,4,2,1,2,2,1,0,2,1,1],[2,2,2,1,2,4,0,2,2,1,3,3,2,1],[2,2,1,1,1,0,4,2,2,2,2,2,1,2],[1,2,3,1,2,2,2,4,3,0,3,2,2,1],
      [0,3,3,1,2,2,2,3,4,1,2,2,2,1],[1,1,1,2,1,1,2,0,1,4,1,1,2,1],[3,2,2,2,0,3,2,3,2,1,4,2,2,1],[3,3,0,2,2,3,2,2,2,1,2,4,3,2],
      [2,2,3,0,1,2,1,2,2,2,2,3,4,2],[1,0,1,2,1,1,2,1,1,1,1,2,2,4]]
ENEMY = {frozenset(x) for x in [('Horse', 'Buffalo'), ('Elephant', 'Lion'), ('Sheep', 'Monkey'), ('Serpent', 'Mongoose'), ('Dog', 'Deer'), ('Cat', 'Rat'), ('Cow', 'Tiger')]}
def nadi(n): return ['Adi', 'Madhya', 'Antya', 'Antya', 'Madhya', 'Adi'][n % 6]
RAJJU = {}
for _g, _s in [('Paadha', [0, 8, 9, 17, 18, 26]), ('Kati', [1, 7, 10, 16, 19, 25]), ('Nabhi', [2, 6, 11, 15, 20, 24]), ('Kanta', [3, 5, 12, 14, 21, 23]), ('Siro', [4, 13, 22])]:
    for _n in _s: RAJJU[_n] = _g
VEDHA = [{0, 17}, {1, 16}, {2, 15}, {3, 14}, {5, 21}, {6, 20}, {7, 19}, {8, 18}, {9, 26}, {10, 25}, {11, 24}, {12, 23}, {4, 13}, {4, 22}, {13, 22}]
FRIENDS = {'Sun': (['Moon', 'Mars', 'Jupiter'], ['Venus', 'Saturn']), 'Moon': (['Sun', 'Mercury'], []), 'Mars': (['Sun', 'Moon', 'Jupiter'], ['Mercury']),
           'Mercury': (['Sun', 'Venus'], ['Moon']), 'Jupiter': (['Sun', 'Moon', 'Mars'], ['Mercury', 'Venus']), 'Venus': (['Mercury', 'Saturn'], ['Sun', 'Moon']),
           'Saturn': (['Mercury', 'Venus'], ['Sun', 'Moon', 'Mars'])}
def rel(a, b): return 'F' if b in FRIENDS[a][0] else 'E' if b in FRIENDS[a][1] else 'N'
VASYA = {0: [4, 7], 1: [3, 6], 2: [5], 3: [7, 8], 4: [6, 9], 5: [1, 11], 6: [9, 5], 7: [3, 5], 8: [11], 9: [0, 10], 10: [0], 11: [9]}
VARNA = [1, 2, 0, 3, 1, 2, 0, 3, 1, 2, 0, 3]
def vgrp(l):
    r = rasi(l); h = (l % 30) >= 15
    return {0: 'C', 1: 'C', 2: 'H', 3: 'J', 4: 'W', 5: 'H', 6: 'H', 7: 'K', 10: 'H', 11: 'J'}.get(r, ('C' if h else 'H') if r == 8 else ('J' if h else 'C'))
VT = {'C': {'C': 2, 'H': 1, 'J': 1, 'W': .5, 'K': 1}, 'H': {'C': 1, 'H': 2, 'J': .5, 'W': 0, 'K': 1}, 'J': {'C': 1, 'H': .5, 'J': 2, 'W': 1, 'K': 1},
      'W': {'C': 0, 'H': 0, 'J': 1, 'W': 2, 'K': 0}, 'K': {'C': 1, 'H': 1, 'J': 1, 'W': 0, 'K': 2}}


def match(g, b):
    """g = girl chart dict, b = boy chart dict. Counts run from the girl's star/rasi."""
    gn, bn, gr, br = g['_idx']['star'], b['_idx']['star'], g['_idx']['rasi'], b['_idx']['rasi']
    c = (bn - gn) % 27 + 1; rc = (br - gr) % 12 + 1; rcb = (gr - br) % 12 + 1
    ga, gb = gana(gn), gana(bn); ya, yb = YONI[gn], YONI[bn]; la, lb = LORD[gr], LORD[br]
    p = {
        'Dinam': 'Yes' if c % 9 in (2, 4, 6, 8, 0) else 'No',
        'Ganam': 'Yes' if ga == gb or {ga, gb} == {'Deva', 'Manushya'} else 'No',
        'Mahendram': 'Yes' if c in (4, 7, 10, 13, 16, 19, 22, 25) else 'No',
        'Stree Deergham': 'Yes' if c > 13 else 'Average' if c > 9 else 'No',
        'Yoni': 'No' if frozenset((ya, yb)) in ENEMY else 'Yes' if ya == yb or YT[YA.index(ya)][YA.index(yb)] >= 3 else 'Average',
        'Rasi': 'No' if 6 in (rc, rcb) or 8 in (rc, rcb) else 'Average' if rc in (2, 12) else 'Yes',
        'Rasi Athipathi': 'Yes' if la == lb or (rel(la, lb) != 'E' and rel(lb, la) != 'E') else 'No',
        'Vasyam': 'Yes' if br in VASYA[gr] or gr in VASYA[br] else 'No',
        'Rajju': 'No' if RAJJU[gn] == RAJJU[bn] else 'Yes',
        'Vedhai': 'No' if {gn, bn} in VEDHA else 'Yes'}
    score = sum({'Yes': 1, 'Average': .5}.get(v, 0) for v in p.values())
    pts = {('F', 'F'): 5, ('F', 'N'): 4, ('N', 'F'): 4, ('N', 'N'): 3, ('F', 'E'): 1, ('E', 'F'): 1, ('N', 'E'): .5, ('E', 'N'): .5, ('E', 'E'): 0}
    GT = {'Deva': {'Deva': 6, 'Manushya': 5, 'Rakshasa': 1}, 'Manushya': {'Deva': 6, 'Manushya': 6, 'Rakshasa': 0}, 'Rakshasa': {'Deva': 0, 'Manushya': 0, 'Rakshasa': 6}}
    bhakoot_bad = rc != 1 and bool({rc, rcb} & {2, 12, 5, 9, 6, 8})
    k = {'Varna (1)': 1 if VARNA[br] >= VARNA[gr] else 0,
         'Vashya (2)': VT[vgrp(g['_idx']['moon'])][vgrp(b['_idx']['moon'])],
         'Tara (3)': 1.5 * (c % 9 not in (3, 5, 7)) + 1.5 * (((gn - bn) % 27 + 1) % 9 not in (3, 5, 7)),
         'Yoni (4)': YT[YA.index(ya)][YA.index(yb)],
         'Graha Maitri (5)': 5 if la == lb else pts[(rel(la, lb), rel(lb, la))],
         'Gana (6)': GT[ga][gb],
         'Bhakoot (7)': 0 if bhakoot_bad else 7,
         'Nadi (8)': 0 if nadi(gn) == nadi(bn) else 8}
    return dict(girl=g['name'], boy=b['name'], porutham=p, porutham_score=score, guna=k, guna_total=sum(k.values()),
                bhakoot_cancelled=bhakoot_bad and (la == lb or rel(la, lb) == rel(lb, la) == 'F'),
                count_girl_to_boy=c, rasi_count=rc,
                chevvai=dict(girl=g['chevvai'], boy=b['chevvai']))


# ---------------- HTML ----------------
GRID = [(0, 0, 11), (0, 1, 0), (0, 2, 1), (0, 3, 2), (1, 3, 3), (2, 3, 4), (3, 3, 5), (3, 2, 6), (3, 1, 7), (3, 0, 8), (2, 0, 9), (1, 0, 10)]
CSS = """:root{--bg:#faf8f4;--fg:#1f1d1a;--muted:#6b665e;--card:#fff;--line:#d9d2c5;--accent:#8a3b12;--lag:#fff3e6}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#161513;--fg:#ece8e1;--muted:#a39d93;--card:#1f1e1b;--line:#3b3731;--accent:#f0a46b;--lag:#2e2418}}
:root[data-theme=dark]{--bg:#161513;--fg:#ece8e1;--muted:#a39d93;--card:#1f1e1b;--line:#3b3731;--accent:#f0a46b;--lag:#2e2418}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,'Noto Sans Tamil','Latha','Tamil Sangam MN',sans-serif}
main{max-width:1000px;margin:0 auto;padding:28px 16px 60px}h1{margin:0}h2{border-bottom:1px solid var(--line);padding-bottom:4px;margin-top:34px}
.k{color:var(--muted);font-size:.85rem}.charts{display:flex;flex-wrap:wrap;gap:18px}
.chart{display:grid;grid-template:repeat(4,minmax(64px,82px))/repeat(4,minmax(64px,82px));border:2px solid var(--fg);background:var(--card)}
.cell{border:1px solid var(--line);padding:3px;font-size:.9rem;line-height:1.25;position:relative}.cell small{position:absolute;bottom:2px;right:4px;color:var(--muted);font-size:.62rem}
.cell.lag{background:var(--lag)}.cell.lag:before{content:'';position:absolute;inset:0;background:linear-gradient(to top right,transparent 49%,var(--accent) 50%,transparent 51%);opacity:.5;width:40%;height:40%}
.center{grid-area:2/2/4/4;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;border:1px solid var(--line)}
table{border-collapse:collapse;width:100%;font-size:.88rem}th,td{border-bottom:1px solid var(--line);padding:5px 6px;text-align:left}th{color:var(--muted);font-weight:600}
.scroll{overflow-x:auto}.now{background:var(--lag);font-weight:600}"""


def box(c, which, title):
    cells = {i: [] for i in range(12)}
    lag_sign = RASI.index(c['lagnam'] if which == 'rasi' else c['amsa_lagnam'])
    for k, p in c['planets'].items(): cells[RASI.index(p['rasi'] if which == 'rasi' else p['amsam'])].append(ABBR[k])
    out = [f'<div class="chart" aria-label="{title}">']
    for r, col, s in GRID:
        lag = ' lag' if s == lag_sign else ''
        txt = ('ல ' if lag else '') + ' '.join(cells[s])
        out.append(f'<div class="cell{lag}" style="grid-area:{r+1}/{col+1}">{txt}<small>{RASI_TA[s]}</small></div>')
    out.append(f'<div class="center"><b>{title}</b><span class="k">{html.escape(c["name"])}</span></div></div>')
    return ''.join(out)


def render(c):
    e = html.escape; md, bh = current(c['dasa'])
    rows = ''.join(f"<tr><td>{k} ({ABBR[k]})</td><td>{p['rasi']} {p['deg']}°</td><td>{p['house']}</td><td>{p['star']}-{p['pada']}</td><td>{p['star_lord']}</td><td>{p['amsam']}</td><td>{p['dignity']}</td></tr>" for k, p in c['planets'].items())
    mds = ''.join(f"<tr class='{'now' if m is md else ''}'><td>{m['lord']}</td><td>{m['start']}</td><td>{m['end']}</td></tr>" for m in c['dasa'])
    bhs = ''.join(f"<tr class='{'now' if b is bh else ''}'><td>{md['lord']} – {b['lord']}</td><td>{b['start']}</td><td>{b['end']}</td></tr>" for b in md['bhuktis']) if md else ''
    ants = ''
    if md:
        i = md['bhuktis'].index(bh)
        for b in md['bhuktis'][i:i + 3]:
            ants += ''.join(f"<tr><td>{md['lord']} – {b['lord']} – {a['lord']}</td><td>{a['start']}</td><td>{a['end']}</td></tr>" for a in b['antarams'])
    sani = ''.join(f"<tr><td>{s['date']}</td><td>{s['rasi']}</td><td>{s['from_moon']}</td><td>{s['phase']}</td></tr>" for s in c['sani_transits'])
    guru = ''.join(f"<tr><td>{s['date']}</td><td>{s['rasi']}</td><td>{s['from_moon']}</td><td>{'favourable' if s['good'] else ''}</td></tr>" for s in c['guru_transits'])
    ll = c['lagna_lord']; ch = c['chevvai']
    summary = [f"Lagnam ⇒ {c['lagnam']} ({c['lagnam_ta']})", f"Lagna lord ⇒ {ll['planet']} ⇒ {ll['house']}th house"]
    summary += [f"{k} ⇒ {p['dignity']} ⇒ {p['house']}th house" for k, p in c['planets'].items() if p['dignity']]
    summary += [f"{', '.join(v)} ⇒ conjunction (சேர்க்கை) in {s}" for s, v in c['conjunctions']]
    summary += [f"{a} ↔ {b} ⇒ exchange (பரிவர்த்தனை)" for a, b in c['exchanges']]
    summary += [f"Maandhi ⇒ {c['planets']['Maandhi']['house']}th house (rises {c['maandhi_time']})",
                f"Chevvai: Mars is {ch['houses']['lagnam']}th from lagnam, {ch['houses']['moon']}th from Moon, {ch['houses']['venus']}th from Venus ⇒ "
                + ('dosham' + (' (Mars own sign / exalted: traditionally cancelled)' if ch['mars_own_or_exalted'] else '') if ch['dosham'] else 'no dosham')]
    si = c['star_info']
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(c['name'])} Jathagam</title><style>{CSS}</style></head><body><main>
<h1>{e(c['name'])}</h1>
<p class="k">D.O.B {c['date']} · T.O.B {c['time']} (UTC{c['tz']:+g}) · P.O.B {e(c['place'])} · {c['weekday']}</p>
<p><b>Star (நட்சத்திரம்):</b> {c['star']} ({c['star_ta']})-{c['pada']} · <b>Rasi (ராசி):</b> {c['rasi']} ({c['rasi_ta']}) · <b>Lagnam (லக்னம்):</b> {c['lagnam']} ({c['lagnam_ta']}) {c['lagnam_deg']}°<br>
<b>Dasa balance at birth (தசா இருப்பு):</b> {c['dasa_balance']} · Gana {si['gana']} · Yoni {si['yoni']} · Rajju {si['rajju']} · Nadi {si['nadi']}</p>
<div class="charts">{box(c, 'rasi', 'இராசி · Rasi')}{box(c, 'amsam', 'அம்சம் · Navamsa')}</div>
<h2>Chart summary</h2><ul>{''.join(f'<li>{e(s)}</li>' for s in summary)}</ul>
<h2>Planets</h2><div class="scroll"><table><tr><th>Planet</th><th>Rasi</th><th>House</th><th>Star-pada</th><th>Star lord</th><th>Amsam</th><th>Dignity</th></tr>{rows}</table></div>
<h2>Dasa (மகா தசை)</h2><div class="scroll"><table><tr><th>Dasa</th><th>From</th><th>To</th></tr>{mds}</table></div>
<h2>Bhukti (புக்தி) in the current dasa</h2><div class="scroll"><table><tr><th>Dasa – Bhukti</th><th>From</th><th>To</th></tr>{bhs}</table></div>
<h2>Antaram (அந்தரம்): current and next two bhuktis</h2><div class="scroll"><table><tr><th>Dasa – Bhukti – Antaram</th><th>From</th><th>To</th></tr>{ants}</table></div>
<h2>Saturn transits from the Moon sign</h2><div class="scroll"><table><tr><th>From</th><th>Saturn in</th><th>House from Moon</th><th>Phase</th></tr>{sani}</table></div>
<h2>Jupiter transits from the Moon sign</h2><div class="scroll"><table><tr><th>From</th><th>Jupiter in</th><th>House from Moon</th><th></th></tr>{guru}</table></div>
<p class="k">Lahiri ayanamsa · whole-sign houses · Vimshottari with 365.25-day years · Maandhi at the end of Saturn's portion. Traditional astrology, not a scientific forecast.</p>
</main></body></html>"""


def strip(c):
    c = dict(c)
    c['dasa'] = [{**m, 'bhuktis': [{**b, 'antarams': [{k: v for k, v in a.items() if not k.endswith('_jd')} for a in b['antarams']]}
                                   for b in m['bhuktis']]} for m in c['dasa']]
    return c


def selftest():
    """Regression check on a made-up chart (the real calibration against a jothidar's notes is kept private)."""
    c = chart('Example', '1995-08-20', '06:40', 5.5, 9.93, 78.12, 'Madurai')
    assert (c['star'], c['pada'], c['rasi'], c['lagnam'], c['amsa_lagnam']) == ('Mirugasirisham', 1, 'Rishabam', 'Simmam', 'Mithunam'), c['star']
    assert c['dasa_balance'] == 'Mars 6y 9m 12d', c['dasa_balance']
    want = {'Sun': ('Simmam', 'Mesham'), 'Moon': ('Rishabam', 'Simmam'), 'Mars': ('Kanni', 'Simmam'), 'Mercury': ('Simmam', 'Thulam'),
            'Jupiter': ('Viruchigam', 'Thulam'), 'Venus': ('Simmam', 'Mesham'), 'Saturn': ('Kumbam', 'Mithunam'), 'Rahu': ('Thulam', 'Viruchigam'),
            'Ketu': ('Mesham', 'Rishabam'), 'Maandhi': ('Magaram', 'Meenam')}
    for k, (r, a) in want.items(): assert (c['planets'][k]['rasi'], c['planets'][k]['amsam']) == (r, a), (k, c['planets'][k])
    assert c['lagna_lord'] == {'planet': 'Sun', 'house': 1} and c['exchanges'] == []
    rahu = c['dasa'][1]; assert rahu['lord'] == 'Rahu'
    assert [(b['lord'], b['end']) for b in rahu['bhuktis']][:4] == [('Rahu', '12-02-2005'), ('Jupiter', '08-07-2007'), ('Saturn', '14-05-2010'), ('Mercury', '01-12-2012')]
    assert [a['end'] for a in rahu['bhuktis'][1]['antarams']][:3] == ['09-06-2005', '25-10-2005', '27-02-2006']
    print('selftest OK: boxes, navamsa, dasa balance, bhukti and antaram dates match the frozen example')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('chart'); c.add_argument('--name', required=True); c.add_argument('--date', required=True, help='YYYY-MM-DD')
    c.add_argument('--time', required=True, help='HH:MM local'); c.add_argument('--tz', required=True, help="UTC offset (5.5) or IANA zone ('Asia/Kolkata')")
    c.add_argument('--lat', type=float, required=True); c.add_argument('--lon', type=float, required=True); c.add_argument('--place', default='')
    c.add_argument('--out', default='.')
    m = sub.add_parser('match'); m.add_argument('girl_json'); m.add_argument('boy_json'); m.add_argument('--out', default='.')
    sub.add_parser('selftest')
    a = ap.parse_args()
    if a.cmd == 'selftest': return selftest()
    os.makedirs(a.out, exist_ok=True)
    if a.cmd == 'chart':
        ch = chart(a.name, a.date, a.time, a.tz, a.lat, a.lon, a.place)
        slug = ''.join(x if x.isalnum() else '-' for x in a.name.lower()).strip('-')
        json.dump(strip(ch), open(f'{a.out}/{slug}.json', 'w'), indent=1, ensure_ascii=False)
        open(f'{a.out}/{slug}.html', 'w').write(render(ch))
        md, bh = current(ch['dasa'])
        print(json.dumps({k: ch[k] for k in ['star', 'pada', 'rasi', 'lagnam', 'dasa_balance', 'lagna_lord', 'exchanges', 'conjunctions', 'chevvai']}, ensure_ascii=False))
        print(f"current: {md['lord']} dasa / {bh['lord']} bhukti ({bh['start']} → {bh['end']})" if md else '')
        print(f'wrote {a.out}/{slug}.json and {a.out}/{slug}.html')
    else:
        g, b = json.load(open(a.girl_json)), json.load(open(a.boy_json))
        print(json.dumps(match(g, b), indent=1, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main())
