#!/usr/bin/env python3
"""Weekly sweep: re-fetch every camp that has no 2027 registration date (or no 2027
dates at all) and report anything that looks newly posted. Writes findings for review —
it never edits camps2027.json itself, because a wrong date misleads a family."""
import json, re, html, os, sys, subprocess, datetime, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.chdir(ROOT)
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

MON = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*'
Y27   = re.compile(r'\b2027\b')
RANGE = re.compile(rf'{MON}\.?\s*\d{{1,2}}\s*(?:[-–—]|to|through)\s*(?:{MON}\.?\s*)?\d{{1,2}}', re.I)
REGOPEN = re.compile(
    r'(registration\s+(?:will\s+)?opens?|enroll(?:ment)?\s+opens?|registration\s+is\s+open|'
    r'sign[- ]ups?\s+opens?|applications?\s+open|on sale|register\s+now|opens?\s+on)\b[^.!?]{0,110}', re.I)

def text_of(raw):
    raw = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', raw)
    raw = re.sub(r'(?s)<[^>]+>', ' ', raw)
    return re.sub(r'[ \t\r\n\xa0]+', ' ', html.unescape(raw))

def fetch(url, dest):
    r = subprocess.run(['curl','-sS','-L','--max-time','30','--compressed','-A',UA,'-o',dest,
                        '-w','%{http_code}', url], capture_output=True, text=True)
    return r.stdout.strip()

def main():
    camps = json.load(open('camps2027.json'))
    targets = [c for c in camps if (c.get('regStatus') == 'tbd' or c.get('status') != 'confirmed') and c.get('url')]
    tmp = tempfile.mkdtemp(prefix='campcheck-')
    findings, errors = [], []
    for i, c in enumerate(targets):
        dest = os.path.join(tmp, f'{i}.html')
        code = fetch(c['url'], dest)
        if code != '200' or not os.path.exists(dest) or os.path.getsize(dest) < 500:
            errors.append({'name': c['name'], 'url': c['url'], 'http': code})
            continue
        t = text_of(open(dest, encoding='utf-8', errors='replace').read())
        y27 = Y27.findall(t)
        regs, seen = [], set()
        for m in REGOPEN.finditer(t):
            s = ' '.join(m.group(0).split())[:150]
            k = s.lower()[:50]
            if k not in seen:
                seen.add(k); regs.append(s)
            if len(regs) >= 4: break
        ranges, rseen = [], set()
        for m in RANGE.finditer(t):
            s = t[max(0, m.start()-60):m.start()+90].strip()
            k = re.sub(r'\W+','',s.lower())[:45]
            if k not in rseen:
                rseen.add(k); ranges.append(' '.join(s.split())[:170])
            if len(ranges) >= 3: break
        # only worth a human's attention if 2027 shows up, or registration language does
        if y27 or regs:
            findings.append({
                'name': c['name'], 'id': c['id'], 'url': c['url'],
                'stored_status': c.get('status'), 'stored_regStatus': c.get('regStatus'),
                'stored_dates': c.get('dates'), 'stored_registration': c.get('registration'),
                'mentions_2027': len(y27),
                'registration_phrases': regs,
                'date_ranges': ranges,
            })
    out = {
        'checked_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'camps_checked': len(targets),
        'with_signals': len(findings),
        'unreachable': errors,
        'findings': findings,
    }
    with open(os.path.join(HERE, 'weekly-findings.json'), 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"checked {len(targets)} camps · {len(findings)} show a 2027 or registration signal "
          f"· {len(errors)} unreachable")
    for f_ in findings:
        print(f"\n--- {f_['name']}  (stored: {f_['stored_regStatus']}/{f_['stored_status']})")
        print(f"    {f_['url']}  · 2027 mentions: {f_['mentions_2027']}")
        for r in f_['registration_phrases']: print(f"    REG   {r}")
        for r in f_['date_ranges'][:2]:      print(f"    DATES {r}")
    if errors:
        print('\nUnreachable: ' + ', '.join(f"{e['name']} ({e['http']})" for e in errors))

if __name__ == '__main__':
    main()
