#!/usr/bin/env python3
"""Weekly sweep over every camp in the directory.

Three things get surfaced, and none of them are decided here — the script only
gathers evidence, because a wrong date in front of a family is worse than a
missed update:

  link_problems  a tracked camp's URL no longer resolves. A dead link is a
                 signal that the camp moved or renamed its page, not a non-event.
  changed        a camp we already call confirmed now shows session dates that
                 are not in what we stored. Confirmed does not mean finished:
                 Minni published a second location and a full week-by-week
                 schedule after we had recorded a one-line summary.
  findings       a camp with unknown dates now shows a 2027 or registration signal.
"""
import json, re, html, os, sys, subprocess, datetime, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.chdir(ROOT)
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

MON = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)'
RANGE = re.compile(rf'({MON})[a-z]*\.?\s*(\d{{1,2}})\s*(?:[-–—]|to|through)\s*(?:({MON})[a-z]*\.?\s*)?(\d{{1,2}})', re.I)
Y27 = re.compile(r'\b2027\b')
REGOPEN = re.compile(
    r'(registration\s+(?:will\s+)?opens?|enroll(?:ment)?\s+opens?|registration\s+is\s+open|'
    r'sign[- ]ups?\s+opens?|applications?\s+open|on sale|register\s+now|opens?\s+on)\b[^.!?]{0,110}', re.I)
NUM = {m.lower(): i for i, m in enumerate(
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], 1)}

def text_of(raw):
    raw = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', raw)
    raw = re.sub(r'(?s)<[^>]+>', ' ', raw)
    return re.sub(r'[ \t\r\n\xa0]+', ' ', html.unescape(raw))

def ranges(text):
    """Normalised 'Jun 21-Jun 24' keys, so the same week written two ways matches."""
    out = set()
    for m in RANGE.finditer(text or ''):
        m1 = NUM.get(m.group(1)[:3].lower()); d1 = int(m.group(2))
        m2 = NUM.get((m.group(3) or m.group(1))[:3].lower()); d2 = int(m.group(4))
        if not m1 or not m2: continue
        if (m2, d2) < (m1, d1): continue          # reversed: not a range
        if (m2 - m1) * 31 + (d2 - d1) > 45: continue   # a season, not a session
        if not (6 <= m1 <= 9): continue                # summer only: skip winter and spring camps
        out.add(f'{m1:02d}-{d1:02d}_{m2:02d}-{d2:02d}')
    return out

def pretty(key):
    a, b = key.split('_')
    inv = {v: k for k, v in NUM.items()}
    f = lambda s: inv[int(s.split('-')[0])].title() + ' ' + str(int(s.split('-')[1]))
    return f(a) + '–' + f(b)

def fetch(url, dest):
    r = subprocess.run(['curl','-sS','-L','--max-time','30','--compressed','-A',UA,
                        '-o',dest,'-w','%{http_code}', url], capture_output=True, text=True)
    return (r.stdout or '').strip() or '000'

def main():
    camps = json.load(open('camps2027.json'))
    targets = [c for c in camps if c.get('url')]
    tmp = tempfile.mkdtemp(prefix='campcheck-')
    link_problems, changed, findings = [], [], []

    for i, c in enumerate(targets):
        dest = os.path.join(tmp, f'{i}.html')
        code = fetch(c['url'], dest)
        ok = code == '200' and os.path.exists(dest) and os.path.getsize(dest) > 500
        if not ok:
            link_problems.append({'name': c['name'], 'id': c['id'], 'url': c['url'],
                                  'http': code, 'status': c.get('status')})
            continue
        t = text_of(open(dest, encoding='utf-8', errors='replace').read())

        if c.get('status') == 'confirmed':
            fresh = ranges(t) - ranges(c.get('dates'))
            if fresh and Y27.search(t):
                changed.append({'name': c['name'], 'id': c['id'], 'url': c['url'],
                                'stored_dates': c.get('dates'),
                                'dates_on_page_we_do_not_have': sorted(pretty(k) for k in fresh)[:8]})
            continue

        regs, seen = [], set()
        for m in REGOPEN.finditer(t):
            s = ' '.join(m.group(0).split())[:150]
            if s.lower()[:50] in seen: continue
            seen.add(s.lower()[:50]); regs.append(s)
            if len(regs) >= 4: break
        date_bits, rseen = [], set()
        for m in RANGE.finditer(t):
            s = ' '.join(t[max(0, m.start()-60):m.start()+90].split())[:170]
            k = re.sub(r'\W+', '', s.lower())[:45]
            if k in rseen: continue
            rseen.add(k); date_bits.append(s)
            if len(date_bits) >= 3: break
        if Y27.search(t) or regs:
            findings.append({'name': c['name'], 'id': c['id'], 'url': c['url'],
                             'stored_status': c.get('status'), 'stored_regStatus': c.get('regStatus'),
                             'stored_dates': c.get('dates'), 'stored_registration': c.get('registration'),
                             'mentions_2027': len(Y27.findall(t)),
                             'registration_phrases': regs, 'date_ranges': date_bits})

    out = {'checked_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
           'camps_checked': len(targets),
           'link_problems': link_problems, 'changed': changed, 'findings': findings,
           'with_signals': len(findings) + len(changed) + len(link_problems)}
    json.dump(out, open(os.path.join(HERE, 'weekly-findings.json'), 'w'),
              ensure_ascii=False, indent=1)

    print(f"checked {len(targets)} camps · {len(link_problems)} link problems · "
          f"{len(changed)} confirmed camps showing new dates · {len(findings)} with a signal")
    for p in link_problems:
        print(f"\n!! LINK {p['http']}  {p['name']}\n   {p['url']}")
    for ch in changed:
        print(f"\n~~ CHANGED {ch['name']}\n   stored: {str(ch['stored_dates'])[:90]}"
              f"\n   on page, not stored: {', '.join(ch['dates_on_page_we_do_not_have'])}")
    for f_ in findings:
        print(f"\n-- {f_['name']}  ({f_['stored_regStatus']}/{f_['stored_status']}) · 2027 x{f_['mentions_2027']}")
        for r in f_['registration_phrases']: print(f"   REG   {r}")
        for r in f_['date_ranges'][:2]:      print(f"   DATES {r}")

if __name__ == '__main__':
    main()
