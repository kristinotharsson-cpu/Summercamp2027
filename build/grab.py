import re, html, sys
def text_of(p):
    raw = open(p, encoding='utf-8', errors='replace').read()
    raw = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', raw)
    raw = re.sub(r'(?s)<[^>]+>', ' ', raw)
    return re.sub(r'[ \t\r\n\xa0]+', ' ', html.unescape(raw))
p, pat = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 260
cap = int(sys.argv[4]) if len(sys.argv) > 4 else 6
t = text_of(p); seen=set(); n=0
for m in re.finditer(pat, t, re.I):
    s = t[max(0,m.start()-w//3):m.start()+w].strip()
    k = re.sub(r'\W+','',s.lower())[:60]
    if k in seen: continue
    seen.add(k); n+=1; print('--', s)
    if n>=cap: break
if not n: print('(no match)')
