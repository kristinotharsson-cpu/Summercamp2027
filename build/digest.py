import re, html, json, os, sys

MON = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*'
RANGE = re.compile(rf'{MON}\.?\s*\d{{1,2}}\s*(?:[-–—]|to|through)\s*(?:{MON}\.?\s*)?\d{{1,2}}', re.I)
Y27   = re.compile(r'\b2027\b')
Y26   = re.compile(r'\b2026\b')
REG   = re.compile(r'(registration|register|enroll|opens?\s+(on|in)|sign[- ]up|waitlist|sold out|closed)', re.I)

def text_of(p):
    raw = open(p, encoding='utf-8', errors='replace').read()
    raw = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', raw)
    raw = re.sub(r'(?s)<[^>]+>', ' ', raw)
    t = html.unescape(raw)
    return re.sub(r'[ \t\r\n\xa0]+', ' ', t)

def snips(t, rx, w=105, cap=6):
    out, seen = [], set()
    for m in rx.finditer(t):
        s = t[max(0, m.start()-w):m.start()+w].strip()
        k = re.sub(r'\W+', '', s.lower())[:60]
        if k in seen: continue
        seen.add(k); out.append(s)
        if len(out) >= cap: break
    return out

camps = json.load(open('camps.json'))
sel = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else range(len(camps))
for i in sel:
    c = camps[i] if i < len(camps) else None
    if not c: continue
    p = f'dl/{i}.html'
    print(f'\n### [{i}] {c["name"]}')
    print(f'    OLD dates: {str(c.get("dates",""))[:120]}')
    if not os.path.exists(p):
        print('    !! NO PAGE FETCHED'); continue
    t = text_of(p)
    n27, n26 = len(Y27.findall(t)), len(Y26.findall(t))
    print(f'    year hits: 2027={n27}  2026={n26}')
    for s in snips(t, Y27, cap=5): print('    27|', s[:215])
    if n27 == 0:
        for s in snips(t, RANGE, cap=3): print('    R |', s[:215])
    for s in snips(t, REG, cap=2): print('    RG|', s[:180])
