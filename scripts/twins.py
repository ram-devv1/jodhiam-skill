#!/usr/bin/env python3
"""Chart twins: public people born while all nine grahas sat in the same boxes as this person.

  python twins.py find out/name.json [--max 150] --out out/   # window + Wikidata list -> out/<slug>-twins/
  python twins.py tally out/<slug>-twins/                      # profiles-*.json -> summary.json
  python twins.py selftest

Only birth DATES go to Wikidata, never the person's name, time or place. Lagnam isn't matched
(twins' birth times are almost never public). Research brief for subagents: references/twins-brief.md.
"""
import argparse, collections as C, datetime as dt, glob, json, os, re, sys, time, urllib.parse, urllib.request
import swisseph as swe
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jathagam as J

STEP = 1 / 24  # one hour
CATS = ['temperament', 'social_style', 'intellect_learning', 'spiritual_religious', 'aesthetics_luxury', 'family', 'money_lifestyle']


def signs(jd): return {k: J.rasi(swe.calc_ut(jd, v, J.FLG)[0][0]) for k, v in J.PLANETS.items()}


def window(d):
    """UT julian-day span around birth where Sun..Saturn and Rahu (so Ketu too) keep the birth signs."""
    day, t = dt.date.fromisoformat(d['date']), dt.time.fromisoformat(d['time'])
    jd = J.utc_jd(day, t, J.tz_hours(d['tz'], day, t)); want = signs(jd)
    a = b = jd
    while a > jd - 4 and signs(a - STEP) == want: a -= STEP
    while b < jd + 4 and signs(b + STEP) == want: b += STEP
    return a, b + STEP, want  # [a, b) at hourly resolution


def ut(jd): y, m, d, h = swe.revjul(jd); return dt.datetime(y, m, d) + dt.timedelta(hours=h)


def wikidata(day):
    q = (f'SELECT ?p ?pLabel ?sl ?desc ?placeLabel WHERE {{ ?p wdt:P569 "{day}T00:00:00Z"^^xsd:dateTime; wdt:P31 wd:Q5; '
         'wikibase:sitelinks ?sl. OPTIONAL{?p wdt:P19 ?place} OPTIONAL{?p schema:description ?desc FILTER(lang(?desc)="en")} '
         'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } }')
    req = urllib.request.Request('https://query.wikidata.org/sparql?' + urllib.parse.urlencode({'query': q, 'format': 'json'}),
                                 headers={'User-Agent': 'jathagam-twins/0.1 (research script)'})
    rows = json.load(urllib.request.urlopen(req, timeout=60))['results']['bindings']
    g = lambda r, k: r.get(k, {}).get('value', '')
    return [dict(date=day, name=g(r, 'pLabel'), sitelinks=int(g(r, 'sl') or 0), desc=g(r, 'desc'), place=g(r, 'placeLabel'))
            for r in rows]


def retry(f, x, n=3):
    for i in range(n):  # Wikidata often answers 502/timeout under load
        try: return f(x)
        except Exception:
            if i == n - 1: raise
            time.sleep(5 * (i + 1))


def find(path, out, cap):
    d = json.load(open(path)); a, b, want = window(d)
    slug = os.path.splitext(os.path.basename(path))[0]; od = f'{out}/{slug}-twins'; os.makedirs(od, exist_ok=True)
    d0, d1 = ut(a).date(), ut(b - 1e-6).date()
    days = [(d0 + dt.timedelta(days=i)).isoformat() for i in range((d1 - d0).days + 1)]  # UTC dates the window touches
    people, failed = {}, []
    for day in days:
        try:
            for r in retry(wikidata, day):
                # skip genealogy-only / no-description entries (usually private individuals)
                if r['desc'] and not r['desc'].startswith('(born') and not re.fullmatch(r'Q\d+', r['name']):  # unlabeled item
                    people.setdefault((r['name'], day), r)
        except Exception as e:  # keep partial results; report which dates failed
            failed.append(day); print(f'wikidata {day} failed: {e}', file=sys.stderr)
        time.sleep(1)
    keep = sorted(people.values(), key=lambda r: -r['sitelinks'])[:cap]
    with open(f'{od}/people.tsv', 'w') as f:
        f.write('date\tname\tsitelinks\tdescription\tbirthplace\n')
        for r in keep: f.write('\t'.join(str(r[k]).replace('\t', ' ') for k in ('date', 'name', 'sitelinks', 'desc', 'place')) + '\n')
    w = dict(start_ut=ut(a).strftime('%Y-%m-%d %H:%M'), end_ut=ut(b).strftime('%Y-%m-%d %H:%M'), hours=round((b - a) * 24),
             signs={k: J.RASI[v] for k, v in want.items()}, dates=days, failed_dates=failed, found=len(people), kept=len(keep))
    json.dump(w, open(f'{od}/window.json', 'w'), indent=1)
    print(f"window {w['start_ut']} -> {w['end_ut']} UT ({w['hours']} h), {len(people)} people, kept {len(keep)} -> {od}/people.tsv")
    return w


def tally(od):
    P = []
    for f in sorted(glob.glob(f'{od}/profiles-*.json')):
        try: x = json.load(open(f))
        except Exception as e: print(f'skip {f}: {e}', file=sys.stderr); continue
        P += [p for p in (x if isinstance(x, list) else []) if isinstance(p, dict)]  # subagent output: shape not guaranteed
    o = lambda p, k: p.get(k) if isinstance(p.get(k), dict) else {}
    l = lambda v: v if isinstance(v, list) else []
    V = [p for p in P if p.get('dob_verified') is not False]
    D = [p for p in V if p.get('data') in ('rich', 'some')]
    tags = {k: C.Counter(str(t).lower() for p in D for t in l(o(p, k).get('tags')) if t).most_common(8) for k in CATS}
    ab = [o(p, 'abroad') for p in V]
    years = C.Counter()
    for p in V:
        for s in l(p.get('setbacks')):
            y = str(s.get('year') or '')[:4] if isinstance(s, dict) else ''
            if y.isdigit(): years[int(y)] += 1
    details = [(str(p.get('name', '?')), str(q)) for p in D for q in l(p.get('quirks_rituals'))][:15]
    try: old = json.load(open(f'{od}/summary.json'))
    except Exception: old = {}
    s = dict(profiled=len(P), verified=len(V), with_personal_data=len(D), tags=tags,
             ever_moved=sum(bool(a.get('moved_countries')) for a in ab), nationality_switch=sum(bool(a.get('nationality_switch')) for a in ab),
             abroad_now=sum(a.get('lives_abroad_now') is True for a in ab), abroad_known=sum(a.get('lives_abroad_now') in (True, False) for a in ab),
             public_partner=sum(bool(o(p, 'love').get('public_partner')) for p in V), married=sum(o(p, 'love').get('married') is True for p in V),
             setback_years=dict(sorted(years.items())),
             hobbies=C.Counter(str(h).lower() for p in D for h in l(p.get('hobbies'))).most_common(10),
             pets=[str(x) for p in D for x in l(p.get('pets'))], details=details,
             takeaways=old.get('takeaways', []) if isinstance(old, dict) else [])  # Claude writes takeaways; keep them across re-tallies
    if os.path.exists(f'{od}/window.json'): s['window'] = json.load(open(f'{od}/window.json'))
    json.dump(s, open(f'{od}/summary.json', 'w'), indent=1)
    print(f"{od}/summary.json: {len(P)} profiled, {len(V)} verified, {len(D)} with personal data")
    return s


def selftest():
    import tempfile
    d = dict(date='1995-08-20', time='06:40', tz=5.5)
    a, b, want = window(d)
    day, t = dt.date(1995, 8, 20), dt.time(6, 40); jd = J.utc_jd(day, t, 5.5)
    assert a <= jd < b and all(signs(x) == want for x in (a, (a + b) / 2, b - STEP)), (a, b, jd)
    assert signs(a - STEP) != want and signs(b) != want, 'window should stop where a sign changes'
    tmp = tempfile.mkdtemp()
    sample = [dict(name='A', dob_verified=True, data='rich', temperament={'tags': ['Funny', 'shy']}, abroad={'lives_abroad_now': True, 'moved_countries': ['X'], 'nationality_switch': True},
                   love={'public_partner': 'B', 'married': False}, setbacks=[{'year': 2022, 'what': 'x'}, {'year': '2024-05', 'what': 'y'}], quirks_rituals=['naps'], hobbies=['Golf'], pets=['dog']),
              dict(name='C', dob_verified=False, data='rich', temperament={'tags': ['funny']}),
              dict(name='D', data='thin', abroad={'lives_abroad_now': False})]
    sample[0]['pets'].append('<script>x</script>'); sample.append(dict(name='E', data='some', temperament={'tags': [None]}, setbacks=['oops'], love=['x']))
    json.dump(sample, open(f'{tmp}/profiles-00.json', 'w')); open(f'{tmp}/profiles-01.json', 'w').write('{broken')
    json.dump({'not': 'a list'}, open(f'{tmp}/profiles-02.json', 'w'))
    s = tally(tmp)
    assert (s['profiled'], s['verified'], s['with_personal_data']) == (4, 3, 2), s
    assert s['tags']['temperament'] == [('funny', 1), ('shy', 1)] and s['abroad_now'] == 1 and s['abroad_known'] == 2
    assert s['setback_years'] == {2022: 1, 2024: 1} and s['details'] == [('A', 'naps')] and s['public_partner'] == 1
    import predict
    h = predict.behaviours_section({'takeaways': [['<b>Bold</b>', 'x<script>'], 'plain']}) + predict.behaviours_section({})
    assert '<script>' not in h and '&lt;script&gt;' in h and 'Commonly observed' in h, 'section must render escaped; empty summary renders nothing'
    print('twins selftest OK: window holds all signs and contains birth; tally counts, skips unverified and broken files')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    f = sub.add_parser('find'); f.add_argument('person_json'); f.add_argument('--out', default='.'); f.add_argument('--max', type=int, default=150)
    t = sub.add_parser('tally'); t.add_argument('dir'); sub.add_parser('selftest')
    a = ap.parse_args()
    if a.cmd == 'find': find(a.person_json, a.out, a.max)
    elif a.cmd == 'tally': tally(a.dir)
    else: selftest()


if __name__ == '__main__':
    main()
