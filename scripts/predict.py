#!/usr/bin/env python3
"""Prediction reports (what happens when) on top of jathagam.py.

  python predict.py person --name "Name" --date 2003-03-14 --time 06:40 --tz Asia/Kolkata \
      --lat 9.93 --lon 78.12 --place Madurai [--years 5] --out ./out
  python predict.py couple girl.json boy.json [--years 5] --out ./out   # JSONs from `person` or `jathagam.py chart`

Rules (sources in references/sources.md):
- Period quality: Parashari functional nature of dasa / bhukti / antaram lords for the lagnam
  (lords of 1,5,9 good; 6,8,12 and 3,11 troublesome; kendra lords neutral), plus placement and dignity.
- Transits (gochara) from the Moon sign: Jupiter good in 2,5,7,9,11; Saturn and Rahu good in 3,6,11;
  Saturn in 12,1,2 (7½ Sani), 4, 7 and 8 are hard.
- Topic timing: a topic is "on" when both the bhukti and the antaram lords signify its houses
  (own, occupy, or via their star lord). Windows snap to antaram boundaries, as the jothidar's do.
The engine writes plain-language lines. Claude should still read them, merge and polish.
"""
import argparse, datetime as dt, html, json, os, sys
import swisseph as swe
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jathagam as J

HOUSE_TXT = {
    1: ("Confidence and health are strong; a good time for personal fresh starts.", "Low energy or health niggles; don't overcommit."),
    2: ("Money and family support improve; good for savings.", "Watch spending, food habits and harsh words at home."),
    3: ("Courage, skills, short trips and networking pay off.", "Restless; avoid impulsive moves and arguments with siblings or friends."),
    4: ("Home comforts, vehicle or property matters and studies go well.", "Worries at home or about mother; a move or disruption is possible."),
    5: ("Studies, creativity and romance flourish; your thinking is clear.", "Overthinking; romance or studies need patience."),
    6: ("You beat competition: good for job applications, interviews, exams and clearing debts.", "Work stress, minor illness or disputes; keep a steady routine."),
    7: ("Relationships, partnerships and deals move forward.", "Friction with a partner or associates; listen more than you talk."),
    8: ("Deep research, hidden or sudden gains, inheritance/insurance matters.", "Sudden obstacles, delays or health scares; avoid risky decisions."),
    9: ("Luck, mentors, higher studies and long-distance travel are favoured.", "Plans abroad or with mentors get delayed; stay patient."),
    10: ("Career moves, promotion and recognition at work.", "Pressure at work; don't quit on impulse."),
    11: ("Gains, income and help from friends; wishes get fulfilled.", "Gains slower than hoped; don't lend money."),
    12: ("Foreign travel or relocation, spiritual growth, good rest.", "Expenses, sleeplessness and losses; avoid night travel."),
}
KARAKA = {'Sun': 'authority, father, government and recognition', 'Moon': 'mind, mother, emotions and travel',
          'Mars': 'energy, property, siblings and drive', 'Mercury': 'studies, skills, communication and business',
          'Jupiter': 'growth, teachers, wisdom and blessings', 'Venus': 'love, comforts, vehicles and art',
          'Saturn': 'hard work, discipline and slow-but-solid results', 'Rahu': 'ambition, foreign links and sudden change',
          'Ketu': 'detachment, spirituality and research'}
TOPICS = {'Career / job': {2, 6, 10, 11}, 'Money / gains': {2, 11}, 'Studies': {4, 5, 9}, 'Travel / abroad': {3, 9, 12},
          'Love / marriage': {2, 5, 7, 11}, 'Home / property': {4, 11}}
TOPIC_KEY = {'Career / job': {10, 6}, 'Money / gains': {11, 2}, 'Studies': {4, 5, 9}, 'Travel / abroad': {12, 9},
             'Love / marriage': {7, 5}, 'Home / property': {4}}
TONE = {1: ('Good', '#1f7a4d'), 0: ('Mixed', '#8a6100'), -1: ('Tough', '#b3261e')}


def load(path_or_args):
    d = json.load(open(path_or_args)) if isinstance(path_or_args, str) else path_or_args
    return J.chart(d['name'], d['date'], d['time'], d['tz'], d['lat'], d['lon'], d.get('place', ''))


def houses(c, p):
    lg = J.RASI.index(c['lagnam'])
    h = {c['planets'][p]['house']} | {(s - lg) % 12 + 1 for s in range(12) if J.LORD[s] == p}
    if p in ('Rahu', 'Ketu'): h |= houses(c, J.LORD[J.RASI.index(c['planets'][p]['rasi'])])
    return h


def signifies(c, p): return houses(c, p) | houses(c, c['planets'][p]['star_lord'])


def nature(c, p):
    lg = J.RASI.index(c['lagnam']); own = {(s - lg) % 12 + 1 for s in range(12) if J.LORD[s] == p}
    pl = c['planets'][p]
    if p in ('Rahu', 'Ketu'):
        s = nature(c, J.LORD[J.RASI.index(pl['rasi'])]) * 0.6 + (0.5 if pl['house'] in (3, 6, 11) else -0.3)
    else:
        s = (1.0 if own & {1, 5, 9} else 0) + (0.5 if own & {4, 7, 10} and own & {5, 9} else 0)
        s -= 0.8 if (own & {6, 8, 3, 11, 12}) and not own & {1, 5, 9} else 0
        s += 0.2 if p in ('Jupiter', 'Venus', 'Mercury', 'Moon') else -0.1
    if pl['house'] in (6, 8, 12) and not own & {6, 8, 12}: s -= 0.4
    s += 0.4 if ('exalted' in pl['dignity'] or 'own' in pl['dignity']) else -0.4 if 'debilitated' in pl['dignity'] else 0
    s += 0.6 if any(p in x for x in c['exchanges']) else 0  # parivartanai: acts as if in its own sign
    return s


def sign_at(body, jd): return J.rasi(swe.calc_ut(jd, body, J.FLG)[0][0])


def gochara(c, jd):
    mr = c['_idx']['rasi']; sa = (sign_at(swe.SATURN, jd) - mr) % 12 + 1; gu = (sign_at(swe.JUPITER, jd) - mr) % 12 + 1
    ra = (sign_at(swe.MEAN_NODE, jd) - mr) % 12 + 1
    s = {3: 1, 6: 1, 11: 1, 12: -1, 1: -1, 2: -.8, 8: -1.5, 4: -.8, 7: -.8}.get(sa, 0)
    s += 1 if gu in (2, 5, 7, 9, 11) else -.5 if gu in (8, 12) else 0
    s += .4 if ra in (3, 6, 11) else -.3 if ra in (1, 8, 12) else 0
    return s, sa, gu


def timeline(c, years=5):
    today = swe.julday(*dt.date.today().timetuple()[:3], 0); end = today + years * J.Y
    out = []
    for md in c['dasa']:
        for b in md['bhuktis']:
            for a in b['antarams']:
                if a['end_jd'] <= today or a['start_jd'] >= end: continue
                mid = (a['start_jd'] + a['end_jd']) / 2
                g, sa, gu = gochara(c, mid)
                nb, na, nd = nature(c, b['lord']), nature(c, a['lord']), nature(c, md['lord'])
                score = .5 * nd + nb + .6 * na + .7 * g
                tone = 1 if score >= 1.0 else -1 if score <= -.6 else 0
                hb, ha = houses(c, b['lord']), houses(c, a['lord'])
                focus = sorted(hb & ha) or sorted(ha)[:2]
                pos = tone == 1 or (tone == 0 and na + nb >= 0)
                lines = [HOUSE_TXT[h][0 if pos else 1] for h in focus[:2]]
                lines.append(f"Theme of the period: {KARAKA[a['lord']]} (inside a {b['lord']} sub-period about {KARAKA[b['lord']].split(',')[0]}).")
                sb, sa_ = signifies(c, b['lord']), signifies(c, a['lord'])
                key_hit = lambda t: (ha | hb) & TOPIC_KEY[t] or (t == 'Love / marriage' and 'Venus' in (a['lord'], b['lord']))
                topics = [t for t, hs in TOPICS.items() if sb & hs and ha & hs and key_hit(t) and tone >= 0]
                out.append(dict(start=a['start'], end=a['end'], s_jd=a['start_jd'], e_jd=a['end_jd'], dasa=md['lord'], bhukti=b['lord'],
                                antaram=a['lord'], tone=tone, score=round(score, 2), lines=lines, topics=topics, sani=sa, guru=gu))
    return out


TRANSIT_BONUS = {'Career / job': lambda e: .5 * (e['sani'] in (3, 6, 11)) + .5 * (e['guru'] in (2, 9, 11)),
                 'Money / gains': lambda e: .7 * (e['guru'] in (2, 11)) + .3 * (e['sani'] in (3, 6, 11)),
                 'Studies': lambda e: .7 * (e['guru'] in (5, 9)), 'Travel / abroad': lambda e: .5 * (e['guru'] in (9, 12)),
                 'Love / marriage': lambda e: 1.0 * (e['guru'] in (5, 7, 11)) - .5 * (e['sani'] in (7, 8)),
                 'Home / property': lambda e: .7 * (e['guru'] in (4, 11))}


def windows(tl, gap=31, min_len=21, top=3):
    """Per topic: merge active antarams (bridge gaps <= gap days), drop windows < min_len days,
    rank by mean period score + topic transit bonus, keep the best `top`, return them in date order."""
    res = {}
    for t in TOPICS:
        runs = []
        for e in (x for x in tl if t in x['topics']):
            sc = e['score'] + TRANSIT_BONUS[t](e)
            if runs and e['s_jd'] - runs[-1][1] <= gap:
                r = runs[-1]; r[1] = e['e_jd']; r[3] = e['end']; r[4].append(sc)
            else: runs.append([e['s_jd'], e['e_jd'], e['start'], e['end'], [sc]])
        runs = [r for r in runs if r[1] - r[0] >= min_len]
        best = sorted(runs, key=lambda r: -sum(r[4]) / len(r[4]))[:top]
        res[t] = [(r[2], r[3]) for r in sorted(best)]
    return res


def chapters(c, tl):
    """One chapter per bhukti in range: headline from the bhukti lord's occupied/owned houses + karaka, tone = mean score."""
    out = []
    for key in dict.fromkeys((e['dasa'], e['bhukti']) for e in tl):
        es = [e for e in tl if (e['dasa'], e['bhukti']) == key]; lord = key[1]
        pl = c['planets'][lord]; nat = nature(c, lord)
        hs = [pl['house']] + sorted(houses(c, lord) - {pl['house']})
        mean = sum(e['score'] for e in es) / len(es)
        b = next(b for m in c['dasa'] if m['lord'] == key[0] for b in m['bhuktis'] if b['lord'] == lord)
        tone = 1 if mean >= .8 else -1 if mean <= -.4 else 0
        pos = tone == 1 or (tone == 0 and nat >= 0)  # wording follows the chapter verdict
        out.append(dict(dasa=key[0], bhukti=lord, start=b['start'], end=b['end'], tone=tone,
                        lines=[HOUSE_TXT[h][0 if pos else 1] for h in hs[:3]], theme=KARAKA[lord]))
    return out


# ---------------- plain-language tables ----------------
HEAD = {  # bhukti lord -> (good, mixed, tough) headline
    'Venus': ("Love, comfort and good times", "Wants love and comfort, and spends on it", "Relationship confusion and overspending"),
    'Saturn': ("Slow but solid progress; effort pays", "Head-down, grinding phase", "Heavy duties, delays, tiredness"),
    'Jupiter': ("Growth, luck and good mentors", "Learning and planning; results come later", "Over-optimism; watch money and weight"),
    'Rahu': ("Big ambition, sudden breaks, foreign links", "Restless and searching", "Confused and unsettled; avoid shortcuts"),
    'Ketu': ("Inner clarity; good for research and letting go", "Detached, rethinking direction", "Low motivation, losing interest"),
    'Sun': ("In the spotlight: career and recognition", "Ego and authority get tested", "Clashes with bosses or father; energy dips"),
    'Moon': ("Emotionally warm; family and travel go well", "Moody and home-focused", "Anxious; sleep and mood swings"),
    'Mars': ("High energy; wins battles, property moves", "Driven but short-tempered", "Anger, arguments, accident-prone"),
    'Mercury': ("Learning, deals and networking pay off", "Busy mind, too many plans", "Overthinking and miscommunication")}
SANI_PLAIN = {12: "Saturn's 7½-year test begins: money leaks, poor sleep.", 1: "Peak of the 7½-year Saturn test: heavy and tiring, but character-building.",
              2: "Last lap of the 7½-year Saturn test: family and money strain.", 3: "Saturn's pressure lifts; confidence and drive return.",
              4: "Home and family stress; a move is possible.", 6: "Beats obstacles and competition.", 7: "Saturn puts strain on relationships; patience needed.",
              8: "Hardest Saturn stretch: health and setbacks, so no big risks.", 11: "Steady gains."}
JUP_PLAIN = [(7, "Jupiter lights up love and partnership."), (5, "Jupiter boosts romance and studies."), (11, "Jupiter brings gains."),
             (9, "Jupiter brings luck and travel."), (2, "Jupiter helps money and family.")]
STAR_NEED = ['action and quick decisions', 'loyalty and total honesty', 'respect, and never being criticised in public', 'affection and stability',
             'variety and good conversation', 'patience during emotional storms', 'a calm home and second chances', 'to feel needed and appreciated',
             'trust that is earned slowly', 'respect and a sense of pride', 'fun and appreciation', 'reliability in return', 'order and humour',
             'admiration and room to create', 'freedom; never feeling caged', 'clarity, commitment and shared goals', 'deep friendship first',
             'to feel like the priority', 'blunt honesty and nothing fake', 'to be heard', 'integrity', 'to be listened to and respected',
             'shared ambition', 'space and alone time', 'meaning and passion', 'calm and depth', 'gentleness and care']
TOPIC_PLAIN = {'Career / job': 'career moves', 'Money / gains': 'money', 'Studies': 'studies', 'Travel / abroad': 'travel or moving abroad',
               'Love / marriage': 'love', 'Home / property': 'home or property'}
COUPLE_TXT = {'commit': ('Green light', "Best stretch for big steps: defining the relationship, meeting families, planning ahead. Make the clear move here; plan real dates, not just chats."),
              'warm': ('Warm', "Easy, supportive stretch. Build trust and shared routines: trips, small traditions, meeting each other's friends."),
              'test': ('Testing', "Friction and pressure. Expect more arguments and misread moods. Give each other space, talk things out, and avoid big decisions until it passes."),
              'patience': ('Patience', "Good feelings, but one of you is under pressure (work, family, health). Keep promises, don't take moods personally, and be the calm one."),
              'steady': ('Steady', "Ordinary stretch. Small, consistent effort matters most.")}
TONE_WORD = {1: 'Good', 0: 'Mixed', -1: 'Tough'}


def jd_of(s): d, m, y = map(int, s.split('-')); return swe.julday(y, m, d, 0)
def fmt(j): return J.local(j, 0).strftime('%d %b %Y').lstrip('0')
def today_jd(): return swe.julday(*dt.date.today().timetuple()[:3], 0)


RAHU_PLAIN = {1: "Rahu sits on the Moon: a restless, foggy mind.", 3: "Rahu boosts courage and initiative.", 6: "Rahu helps beat rivals.",
              7: "Rahu stirs confusion in relationships.", 8: "Rahu brings sudden shake-ups.", 11: "Rahu brings sudden gains.",
              12: "Rahu brings expenses or a pull towards abroad."}
PIH = {}  # planet-in-house readings (references/planet-in-house.json), optional
try:
    PIH = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references', 'planet-in-house.json')))['readings']
except (OSError, ValueError, KeyError):
    pass


def segments(people, years, target=120, min_days=45, max_days=185):
    """Cut wherever life changes: every antaram change (either person) and every Saturn / Jupiter / Rahu
    sign change. Then glue pieces into chunks of ~`target` days, always breaking at a 'major' cut
    (bhukti change or Saturn/Jupiter/Rahu ingress) once a chunk is >= min_days."""
    t0 = today_jd(); t1 = t0 + years * J.Y; minor, major = set(), set()
    for c in people:
        for m in c['dasa']:
            for b in m['bhuktis']:
                if t0 < b['start_jd'] < t1: major.add(b['start_jd'])
                minor |= {a['start_jd'] for a in b['antarams'] if t0 < a['start_jd'] < t1}
    for body in (swe.SATURN, swe.JUPITER, swe.MEAN_NODE):
        major |= {j for j, _ in J.ingresses(body, t0, years + .1) if t0 < j < t1}
    cuts = sorted(minor | major | {t1}); chunks, start = [], t0
    for cut in cuts:
        ln = cut - start
        if cut == t1 or (cut in major and ln >= min_days) or ln >= target or (ln >= min_days and cut - start + 30 > max_days):
            chunks.append([start, cut]); start = cut
    if len(chunks) > 1 and chunks[-1][1] - chunks[-1][0] < min_days:
        last = chunks.pop(); chunks[-1][1] = last[1]
    return chunks


def samples(a, b, step=15): return [a + i * step for i in range(max(1, int((b - a) / step)))]
def months(a, b): return samples(a, b, 30)
def at(tl, j): return next((x for x in tl if x['s_jd'] <= j < x['e_jd']), None)


def read_person(c, tl, a, b, prev=None):
    """Plain sentences for one person over [a, b). Transit lines only when they change vs `prev`."""
    pts = [p for p in (at(tl, j) for j in samples(a, b)) if p]
    mean = sum(p['score'] for p in pts) / len(pts); tone = 1 if mean >= .8 else -1 if mean <= -.4 else 0
    lord = max(set(p['antaram'] for p in pts), key=[p['antaram'] for p in pts].count)  # the planet running these months
    gs = [gochara(c, j) for j in samples(a, b)]
    sa = max(set(x[1] for x in gs), key=[x[1] for x in gs].count)  # Saturn's main sign (ignores retro blips)
    gu = max(set(x[2] for x in gs), key=[x[2] for x in gs].count)
    ra = (sign_at(swe.MEAN_NODE, (a + b) / 2) - c['_idx']['rasi']) % 12 + 1
    txt = [HEAD[lord][{1: 0, 0: 1, -1: 2}[tone]] + '.']
    h = str(c['planets'][lord]['house'])
    # classical box reading: positive line only (classical cautions are too fatalistic to print raw)
    pg = PIH.get(lord, {}).get(h, {}).get('good', '')
    if tone >= 0 and len(pg.split()) >= 4 and 'some texts' not in pg.lower(): txt.append(pg)
    if sa in SANI_PLAIN and (not prev or prev['sani'] != sa): txt.append(SANI_PLAIN[sa])
    jt = dict(JUP_PLAIN).get(gu)
    if jt and (not prev or prev['guru'] != gu): txt.append(jt)
    if ra in RAHU_PLAIN and (not prev or prev['rahu'] != ra): txt.append(RAHU_PLAIN[ra])
    days = {}
    for p in pts:
        for t in p['topics']: days[t] = days.get(t, 0) + 1
    good_for = [TOPIC_PLAIN[t] for t, _ in sorted(days.items(), key=lambda kv: -kv[1])[:2]] if tone >= 0 else []
    return dict(tone=tone, text=' '.join(txt), good_for=good_for, sani=sa, guru=gu, rahu=ra, lord=lord)


def read_all(c, tl, segs):
    out = []
    for a, b in segs: out.append(read_person(c, tl, a, b, out[-1] if out else None))
    return out


def couple_state(g, b, tg, tb, j):
    x, y = at(tg, j), at(tb, j)
    _, sg, gg = gochara(g, j); _, sb, gb = gochara(b, j)
    love = ('Love / marriage' in x['topics']) + ('Love / marriage' in y['topics']) + (gg in (5, 7, 11)) + (gb in (5, 7, 11))
    strain = (sg in (7, 8)) + (sb in (7, 8)) + (x['tone'] < 0) + (y['tone'] < 0)
    return ('commit' if love >= 2 and strain == 0 else 'test' if strain >= 2
            else 'patience' if strain == 1 else 'warm' if love >= 1 else 'steady')


def couple_seg(g, b, tg, tb, a, z):
    st = [couple_state(g, b, tg, tb, j) for j in samples(a, z)]
    if st.count('test') / len(st) >= .4: return 'test'
    if 'commit' in st and st.count('patience') / len(st) < .5: return 'commit'
    if st.count('patience') / len(st) >= .4: return 'patience'
    return 'warm' if st.count('warm') / len(st) >= .5 else 'steady'


# ---------------- HTML ----------------
CSS = J.CSS + """
.badge{display:inline-block;padding:1px 8px;border-radius:99px;color:#fff;font-size:.75rem;font-weight:600;margin-left:4px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:10px 0}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
td{vertical-align:top;line-height:1.45}td:first-child{font-weight:700;white-space:nowrap}
.do li,.dont li{margin:8px 0;line-height:1.5}.do li::marker{color:#1f7a4d;font-weight:700}.dont li::marker{color:#b3261e;font-weight:700}
details{margin-top:30px}summary{cursor:pointer;color:var(--muted)}.big{font-size:2rem;font-weight:700}.k2{color:var(--muted);font-size:.8rem}"""


def page(title, body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head><body><main>{body}
<p class="k" style="margin-top:30px">Based on traditional Tamil astrology. It's a reading, not a guarantee.</p></main></body></html>"""


def badge(t): n, col = TONE[t]; return f'<span class="badge" style="background:{col}">{n}</span>'
def ul(cls, items):
    li = lambda i: f'<b>{html.escape(i[0])}</b> {html.escape(i[1])}' if isinstance(i, tuple) else html.escape(i)
    return f"<ol class='{cls}'>" + ''.join(f'<li>{li(i)}</li>' for i in items) + '</ol>'
def table(head, rows): return "<div class='scroll'><table><tr>" + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table></div>'
def span(a, b): return f"{fmt(a)} → {fmt(b)}"


def runs_of(segs, labels, want):
    return [span(a, b) for (a, b), l in zip(segs, labels) if l == want]


def behaviours_section(s):
    """'Commonly observed behaviours & lifestyle' from summary.json 'takeaways' (Claude writes them from the trait research
    and the twins tally). Items are [bold, text] pairs or plain strings; ul() escapes them."""
    items = [tuple(map(str, t[:2])) if isinstance(t, list) and len(t) >= 2 else str(t) for t in (s.get('takeaways') or [])]
    return f"<h2>Commonly observed behaviours &amp; lifestyle</h2><div class='card'>{ul('do', items)}</div>" if items else ''


def person_report(c, years, traits=None):
    e = html.escape; tl = timeline(c, years); segs = segments([c], years); first = c['name'].split()[0]
    rs = read_all(c, tl, segs)
    rows = [[span(a, b), f"{badge(r['tone'])}<br>{e(r['text'])}" + (f"<br><span class='k2'>Good for: {', '.join(r['good_for'])}</span>" if r['good_for'] else '')]
            for (a, b), r in zip(segs, rs)]
    good = [span(a, b) for (a, b), r in zip(segs, rs) if r['tone'] == 1]
    tough = [span(a, b) for (a, b), r in zip(segs, rs) if r['tone'] == -1]
    heavy = [span(a, b) for (a, b), r in zip(segs, rs) if r['sani'] in (12, 1, 2, 8)]
    need = STAR_NEED[c['_idx']['star']]
    dos = ([("Push hardest in your strongest stretch.", f"{good[0]} is when effort pays off fastest. Apply, ask, launch, move then.")] if good else []) + [
        ("Protect what you need most.", f"Your star needs {need}. Build your life so you get it, and tell the people close to you."),
        ("Keep sleep, food and exercise regular.", "It's the cheapest remedy there is, and it matters most in the pressured stretches.")] + \
        ([("Do the Saturn remedy.", f"During {heavy[0]}, listen to the Hanuman Chalisa daily and help older people or workers on Saturdays. It keeps you patient when Saturn slows things down.")] if heavy else []) + \
        ([("Do the Moon remedy.", "Every Monday, 8–9 pm, light 2 ghee lamps at the entrance. It's a traditional remedy for the Moon period you're in.")] if J.current(c['dasa'])[0]['lord'] == 'Moon' else [])
    donts = ([("Don't take big risks in the tough stretch.", f"During {tough[0]}, avoid quitting on impulse, big loans or big moves. Wait for the next good stretch.")] if tough else []) + \
            ([("Don't mistake slow for stuck.", f"The Saturn-heavy stretch ({heavy[0]}) brings delays and tiredness. It's slow, not failure; keep going.")] if heavy else []) + \
            [("Don't wait for a 'good period' to start working.", "Good periods reward effort that's already happening. Start now so there's something to reward."),
             ("Don't over-share plans.", "Keep personal plans to people you fully trust until they're done.")]
    best = good[0] if good else 'the steadier stretches'
    summary = (f"{e(c['name'])} is {c['rasi']} rasi, {c['star']} star. Over the next {years} years, the strongest stretch is {best}"
               + (f" and the hardest is {tough[0]}" if tough else '') + ". "
               + f"The current chapter runs to {J.current(c['dasa'])[1]['end']}. Use the timeline to plan the big moves, and the do's and don'ts to get through the rest.")
    tech = f"<details><summary>Behind the reading</summary><div class='charts'>{J.box(c, 'rasi', 'Rasi')}{J.box(c, 'amsam', 'Navamsa')}</div><p class='k'>{c['star']}-{c['pada']} · {c['rasi']} rasi · {c['lagnam']} lagnam · dasa balance {c['dasa_balance']}</p></details>"
    return (f"<h1>{e(c['name'])}: the next {years} years</h1>"
            + "<h2>Timeline</h2>" + table(['When', 'What to expect'], rows)
            + f"<h2>Do's and don'ts</h2><div class='grid'><div class='card'><h3>Do</h3>{ul('do', dos)}</div><div class='card'><h3>Don't</h3>{ul('dont', donts)}</div></div>"
            + f"<h2>Summary</h2><div class='card'><p>{summary}</p></div>" + tech
            + (behaviours_section(traits) if traits else ''))  # behaviours always last


def couple_report(g, b, years):
    e = html.escape; m = J.match(g, b); tg, tb = timeline(g, years), timeline(b, years)
    s, k = m['porutham_score'], m['guna_total']; p = m['porutham']
    gn, bn = g['name'].split()[0], b['name'].split()[0]
    verdict = ('Not recommended' if 'No' in (p['Rajju'], p['Vedhai']) else 'Good match' if s >= 6 and k >= 18
               else 'Average match' if s >= 5 or k >= 18 else 'Weak match')
    segs = segments([g, b], years)
    rb, rg = read_all(b, tb, segs), read_all(g, tg, segs)
    labs = [couple_seg(g, b, tg, tb, x, y) for x, y in segs]
    rows = []
    for (x, y), hb, hg, l in zip(segs, rb, rg, labs):
        name, txt = COUPLE_TXT[l]; extra = ''
        if hb['tone'] - hg['tone'] == 2: extra = f" {bn} is up while {gn} is down: support her, don't pressure her."
        if hg['tone'] - hb['tone'] == 2: extra = f" {gn} is up while {bn} is down: support him, don't pressure him."
        if l == 'patience':
            who = [n for n, r, pr in ((bn, hb, 'him'), (gn, hg, 'her')) if r['sani'] in (7, 8, 1)]
            if who: extra = f" {who[0]} is carrying Saturn pressure here: be patient with {'him' if who[0] == bn else 'her'}."
        if not extra and l == 'commit' and hb['tone'] > hg['tone']: extra = f" {bn} is keener than {gn} right now: don't rush her."
        if not extra and l == 'commit' and hg['tone'] > hb['tone']: extra = f" {gn} is keener than {bn} right now: don't rush him."
        cell = lambda r: f"{badge(r['tone'])}<br>{e(r['text'])}" + (f"<br><span class='k2'>Good for: {', '.join(r['good_for'])}</span>" if r['good_for'] else '')
        rows.append([span(x, y), cell(hb), cell(hg), f"<b>{name}.</b> {e(txt + extra)}"])
    commit, test = runs_of(segs, labs, 'commit'), runs_of(segs, labs, 'test')
    he, she = (bn, 'he', 'him'), (gn, 'she', 'her')
    dos = [(f"Give {bn} what he needs: {STAR_NEED[b['_idx']['star']]}.", "Your star says this is non-negotiable for him. Respect it and he relaxes; ignore it and he pulls away."),
           (f"Give {gn} what she needs: {STAR_NEED[g['_idx']['star']]}.", "This is what makes her feel safe. Show it through actions over weeks, not one big gesture.")]
    donts = []
    if commit: dos.append(("Make the move in the green-light window.", f"{commit[0]} is the easiest stretch for big steps: defining the relationship, meeting families, planning ahead. Ask clearly, once. Something simple and specific beats hinting."))
    if test: donts.append(("Don't force big decisions in the testing stretch.", f"During {test[0]} pressure runs high. No ultimatums, no moving in or breaking up on impulse. Talk it out and wait for calmer months."))
    if p['Vasyam'] == 'No': dos.append(("Be friends for real first.", "There's no instant 'pull' between these charts. The spark grows from talking, joking, debating and doing things together."))
    if p['Yoni'] != 'Yes': dos.append(("Let closeness build naturally.", "Physical and emotional chemistry here grows with time and trust. Rushing it backfires."))
    if p['Dinam'] == 'No': dos.append(("Build small shared routines.", "A regular call, a weekly plan, a shared ritual. Your daily rhythms differ, so routines keep you in sync."))
    if p['Rasi Athipathi'] == 'No': dos.append(("Talk about values early.", "Money, family, religion, where to live. Your core values differ, so surface them before they become fights."))
    dos.append(("Be consistent.", "Show up when you say you will and reply like a normal person. Reliability wins more than intensity, especially with a partner who's still deciding."))
    dos.append(("Keep your own life full.", "Work, friends, gym, plans. Someone with direction is attractive; someone whose world revolves around the other person isn't."))
    if J.gana(g['_idx']['star']) == J.gana(b['_idx']['star']) == 'Rakshasa':
        donts.append(("Don't compete to win arguments.", "You're both strong-willed. When it turns into who's right, both lose. Agree to pause and come back to it."))
    elif p['Ganam'] == 'No': donts.append(("Don't take reactions personally.", "You're wired differently: one reacts fast, one slow. Ask what they meant before reacting."))
    if p['Rasi'] != 'Yes': donts.append(("Don't read silence as rejection.", "Your moods run on different clocks. Quiet days happen; check in gently instead of assuming the worst."))
    if p['Rajju'] == 'No' or p['Vedhai'] == 'No': donts.append(("Don't ignore the dosham if families follow porutham.", "Rajju or Vedhai failing is a dealbreaker for many families. Get a jothidar's view early instead of being surprised later."))
    if g['chevvai']['dosham'] != b['chevvai']['dosham']: donts.append(("Don't panic over Chevvai dosham.", f"Only {'she' if g['chevvai']['dosham'] else 'he'} shows it, and it depends on the exact birth time and is often cancelled. Don't let it decide anything on its own."))
    donts.append(("Don't chase or smother.", "No flooding with texts, no double or triple texting, no constant check-ins. Intensity reads as pressure."))
    donts.append(("Don't go cold and mysterious either.", "When overwhelmed, say 'busy week, talk soon' instead of disappearing. Silence gets read as 'not interested'."))
    donts.append(("Don't play games.", "No trying to make the other jealous. With these stars, jealousy doesn't spark interest; it shuts the door."))
    reality = [(f"{s:g}/10 means it's written in the stars", "The score measures temperament fit, not effort. High scores still fail without communication, and lower ones work with it."),
               ((f"{commit[0]} is when they'll get together" if commit else "There's a perfect moment coming"), "A green-light window is when it's easier, not when it happens. Someone still has to make the move."),
               ((f"The testing time ({test[0]}) means a breakup" if test else "No testing time means no fights"), "Testing stretches bring friction and pressure. Couples who talk through them come out stronger."),
               ("Astrology decides it", "How they treat each other, their families, culture and distance decide far more.")]
    ups = [n for n, v in p.items() if v == 'Yes']; key = 'both pass' if 'No' not in (p['Rajju'], p['Vedhai']) else 'do not both pass'
    summary = (f"On the stars, {e(gn)} and {e(bn)} score <b>{s:g}/10</b> on the Tamil porutham and <b>{k:g}/36</b> on the North Indian guna: a "
               f"<b>{verdict.lower()}</b>. The two checks families care most about (Rajju and Vedhai) {key}. "
               + (f"Best stretch for big steps: {commit[0]}. " if commit else '') + (f"Hardest stretch: {test[0]}. " if test else '')
               + "The score says they can work. The timeline says when it's easier and when it's harder.")
    ptab = ''.join(f"<tr><td>{n}</td><td>{badge({'Yes': 1, 'Average': 0, 'No': -1}[v])}</td><td>{e(PORUTHAM_TXT[n][0 if v == 'Yes' else 1])}</td></tr>" for n, v in p.items())
    tech = (f"<details><summary>Behind the reading</summary><div class='charts'>{J.box(b, 'rasi', bn)}{J.box(g, 'rasi', gn)}</div>"
            f"<p class='k'>{e(bn)}: {b['star']}-{b['pada']}, {b['rasi']} · {e(gn)}: {g['star']}-{g['pada']}, {g['rasi']}</p><table>{ptab}</table></details>")
    return (f"<h1>{e(bn)} & {e(gn)}</h1><h2>Timeline</h2>" + table(['When', f'Him ({e(bn)})', f'Her ({e(gn)})', 'As a couple'], rows)
            + f"<h2>Do's and don'ts</h2><div class='grid'><div class='card'><h3>Do</h3>{ul('do', dos[:7])}</div><div class='card'><h3>Don't</h3>{ul('dont', donts[:7])}</div></div>"
            + "<h2>Expectation vs reality</h2>" + table(['Expectation', 'Reality'], [[e(a), e(z)] for a, z in reality])
            + f"<h2>Score</h2><div class='grid'><div class='card'><div class='big'>{s:g}/10</div>Tamil porutham (pass: 6)</div>"
            + f"<div class='card'><div class='big'>{k:g}/36</div>North Indian guna (pass: 18)</div><div class='card'><div class='big' style='font-size:1.4rem'>{verdict}</div></div></div>"
            + f"<div class='card'><p>{summary}</p></div>" + tech)


PORUTHAM_TXT = {
    'Dinam': ("Day-to-day harmony and good health together.", "Daily routines and moods may clash."),
    'Ganam': ("Similar temperament.", "Different temperaments."),
    'Mahendram': ("Supports family growth and children.", "Family growth needs planning."),
    'Stree Deergham': ("Supports her wellbeing and prosperity.", "She needs her own space and support."),
    'Yoni': ("Natural chemistry.", "Chemistry needs time."),
    'Rasi': ("Moon signs support each other.", "Moon signs in tension."),
    'Rasi Athipathi': ("Core values line up.", "Different values."),
    'Vasyam': ("Strong mutual pull.", "No special pull; grows through friendship."),
    'Rajju': ("No Rajju dosham.", "Rajju dosham: most jothidars advise against."),
    'Vedhai': ("No obstruction between the stars.", "Vedhai dosham: traditionally serious.")}


def selftest():
    """Windows must sit on exact antaram boundaries; chapters must equal real bhuktis."""
    c = J.chart('Example', '1995-08-20', '06:40', 5.5, 9.93, 78.12, 'Madurai'); tl = timeline(c, 5)
    edges = {a['start'] for m in c['dasa'] for b in m['bhuktis'] for a in b['antarams']} | {a['end'] for m in c['dasa'] for b in m['bhuktis'] for a in b['antarams']}
    for t, ws in windows(tl).items():
        for a, b in ws: assert a in edges and b in edges, (t, a, b)
    bh = {(b['start'], b['end']) for m in c['dasa'] for b in m['bhuktis']}
    assert all((x['start'], x['end']) in bh for x in chapters(c, tl))
    assert all(e['tone'] in (-1, 0, 1) and e['lines'] for e in tl)
    segs = segments([c], 3)
    assert all(x[1] == y[0] for x, y in zip(segs, segs[1:])) and all(20 <= b - a <= 200 for a, b in segs), segs
    print('predict selftest OK: windows on antaram boundaries, chapters = bhuktis, timeline rows contiguous (20-200 days)')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('person')
    for a in ('name', 'date', 'time', 'place'): p.add_argument('--' + a, required=a != 'place', default='')
    p.add_argument('--tz', required=True, help="UTC offset (5.5) or IANA zone ('Asia/Kolkata', 'America/Toronto')")
    for a in ('lat', 'lon'): p.add_argument('--' + a, type=float, required=True)
    p.add_argument('--traits', '--twins', dest='traits', help='summary.json (twins.py tally + takeaways): adds the behaviours & lifestyle section')
    q = sub.add_parser('couple'); q.add_argument('girl_json'); q.add_argument('boy_json'); sub.add_parser('selftest')
    for x in (p, q): x.add_argument('--years', type=int, default=3); x.add_argument('--out', default='.')
    a = ap.parse_args()
    if a.cmd == 'selftest': return selftest()
    os.makedirs(a.out, exist_ok=True)
    slug = lambda n: ''.join(x if x.isalnum() else '-' for x in n.lower()).strip('-')
    if a.cmd == 'person':
        inp = dict(name=a.name, date=a.date, time=a.time, tz=a.tz, lat=a.lat, lon=a.lon, place=a.place)
        c = load(inp)
        json.dump(inp, open(f'{a.out}/{slug(a.name)}.json', 'w'), indent=1)
        open(f'{a.out}/{slug(a.name)}-predictions.html', 'w').write(page(a.name + ' Predictions', person_report(c, a.years, json.load(open(a.traits)) if a.traits else None)))
        print(f'wrote {a.out}/{slug(a.name)}-predictions.html')
    else:
        g, b = load(a.girl_json), load(a.boy_json)
        f = f"{a.out}/{slug(g['name'])}-and-{slug(b['name'])}-compatibility.html"
        open(f, 'w').write(page(f"{b['name']} and {g['name']}", couple_report(g, b, a.years)))
        print(f'wrote {f}')


if __name__ == '__main__':
    main()
