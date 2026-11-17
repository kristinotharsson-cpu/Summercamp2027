import re, sys, os, html

PAT = [
 (r'\bprogramm?es\b', 'programs'), (r'\bprogramme\b','program'),
 (r'\bcentres?\b','center(s)'), (r'\bfavourit', 'favorit'),
 (r'\borganis', 'organiz'), (r'\brealis','realiz'), (r'\brecognis','recogniz'),
 (r'\bapologis','apologiz'), (r'\bspecialis','specializ'), (r'\bemphasis(?:e|ed|ing)\b','emphasiz'),
 (r'\bcolour','color'), (r'\bbehaviour','behavior'), (r'\bneighbour','neighbor'),
 (r'\bhonour','honor'), (r'\blabour','labor'), (r'\bflavour','flavor'),
 (r'\bfavour(?!it)','favor'), (r'\bharbour','harbor'),
 (r'\blabelled\b','labeled'), (r'\bcancelled\b','canceled'), (r'\btravelling\b','traveling'),
 (r'\bmodelling\b','modeling'), (r'\benrolment\b','enrollment'), (r'\bfulfil\b','fulfill'),
 (r'\bwhilst\b','while'), (r'\bamongst\b','among'), (r'\blearnt\b','learned'),
 (r'\bburnt\b','burned'), (r'\bspelt\b','spelled'), (r'\btowards\b','toward'),
 (r'\bpractise','practice'), (r'\blicence\b','license'), (r'\bdefence\b','defense'),
 (r'\boffence\b','offense'), (r'\bgrey\b','gray'), (r'\bmetres?\b','meter(s)'),
 (r'\bmaths\b','math'), (r'\bpyjamas\b','pajamas'), (r'\bstorey\b','story'),
 (r'\btheatres?\b','theater(s)'),
 (r'\bcounsellors?\b','counselor(s)'), (r'\btravellers?\b','traveler(s)'),
 (r'\bcancelling\b','canceling'), (r'\bmarvellous\b','marvelous'),
 (r'\bjewellery\b','jewelry'), (r'\bskilful\b','skillful'),
 (r'\bdialled\b','dialed'), (r'\bfuelled\b','fueled'),
 (r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b','US date order'),
]
# proper nouns that keep British spelling
SKIP = [r'Wheelock Family Theatre', r'Family Theatre Camp', r'Boston Children\'s Theatre',
        r'Huntington Theatre', r'Theatre Company', r'theatre\.org', r'wheelockfamilytheatre']

def scan(path, text):
    for rx, fix in PAT:
        for m in re.finditer(rx, text, re.I):
            ctx = text[max(0,m.start()-55):m.start()+55].replace('\n',' ')
            if any(re.search(s, ctx, re.I) for s in SKIP): continue
            print(f'  {os.path.basename(path):26} {m.group(0):22} -> {fix:16} … {ctx.strip()[:95]}')

for p in sys.argv[1:]:
    t = open(p, encoding='utf-8', errors='replace').read()
    if p.endswith('.html'):
        t = re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', ' ', t)
        t = re.sub(r'(?is)<style\b.*?</style>', ' ', t)
    scan(p, t)
print('scan complete')
