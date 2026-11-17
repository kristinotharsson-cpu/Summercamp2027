import json, re, os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
d = json.load(open('camps2027.json'))

AREA_OF = {}
def reg(area, *names):
    for n in names: AREA_OF[n.lower()] = area
reg('Chinatown & Downtown', 'Chinatown', 'Downtown')
reg('Beacon Hill & Back Bay', 'Beacon Hill', 'Back Bay')
reg('South End & Roxbury', 'South End', 'Roxbury')
reg('Fenway & Longwood', 'Fenway', 'Longwood')
reg('Dorchester & South Boston', 'Dorchester', 'South Boston', 'Seaport')
reg('JP, Roslindale & West Roxbury', 'Jamaica Plain', 'Roslindale', 'West Roxbury', 'Hyde Park', 'Mattapan')
reg('Charlestown & East Boston', 'Charlestown', 'East Boston')
reg('Allston & Brighton', 'Allston', 'Brighton')
reg('Cambridge & Somerville', 'Cambridge', 'Somerville')
reg('Greater Boston suburbs', 'Newton', 'Brookline', 'Milton', 'Waltham', 'Westwood', 'Sharon',
    'Dover', 'Wellesley', 'Belmont', 'Beverly', 'Lexington', 'Framingham', 'Natick', 'Dedham',
    'Needham', 'Norwood', 'Walpole', 'Medfield', 'Braintree')
reg('Overnight camps', 'Poland', 'Duxbury', 'Smithfield', 'Sandwich', 'Squam Lake')

ADDR = re.compile(r'\d{1,5}[A-Za-z]?\s+[A-Z][A-Za-z.\'’-]*(?:\s+[A-Z][A-Za-z.\'’-]*){0,3}\s+'
                  r'(?:St|Street|Rd|Road|Ave|Avenue|Way|Lane|Ln|Dr|Drive|Blvd|Pl|Place|Row|Alley|Sq|Square)\b\.?'
                  r'(?:,?\s+[A-Z][a-z]+(?:\s[A-Z][a-z]+)?)?(?:,?\s*(?:MA|NH|ME))?(?:\s*\d{5})?')
TOWN = re.compile('|'.join(sorted((re.escape(k) for k in AREA_OF), key=len, reverse=True)), re.I)
TRAIL = re.compile(r'[\s,.]*(Attn|Morning|Program|Camp|Each|Campers|Students|Please|The)\b.*$', re.I)

OVERRIDE_AREA = {   # the text alone is ambiguous or misleading
 'b-safe-st-stephen-s-youth-programs':'Several locations',
 'boston-outdoor-preschool-network-bopn':'Several locations',
 'steve-kate-s-camp':'Several locations',
 'bps-5th-quarter-summer-2026':'Several locations',
 'boston-public-schools-5th-quarter':'Several locations',
 'red-sox-summer-camp':'Several locations',
 'linx-summer-camps-wellesley':'Greater Boston suburbs',
 'camp-shriver-at-umass-boston':'Dorchester & South Boston',   # UMass Boston, Columbia Point
 'new-england-base-camp-cub-scout-day-camp':'Greater Boston suburbs',
}

rows = []
for c in d:
    loc, src = c.get('location'), 'already set'
    if not loc:
        hay = ' '.join(str(c.get(k) or '') for k in ('description','registration','hours','note'))
        m = ADDR.search(hay)
        if m:
            loc = TRAIL.sub('', m.group(0)).strip(' ,.'); src = 'address in text'
        else:
            t = TOWN.search(hay)
            if t: loc = t.group(0); src = 'town in text'
    area = None
    key = c['id']
    if key in OVERRIDE_AREA:
        area = OVERRIDE_AREA[key]
    else:
        for field in (loc or '', c.get('description') or '', c.get('name') or ''):
            t = TOWN.search(field)
            if t: area = AREA_OF[t.group(0).lower()]; break
    if not area:
        area = 'Boston — area not listed' if re.search(r'\bBoston\b', ' '.join(
            str(c.get(k) or '') for k in ('description','location','name'))) else 'Location not listed'
    c['location'] = loc
    c['area'] = area
    rows.append((c['name'][:38], (loc or '—')[:40], area, src))

for n, l, a, s in sorted(rows, key=lambda r: r[2]):
    print(f'{a:31} | {n:40} | {l:42} | {s}')
from collections import Counter
print('\nAREA COUNTS:')
for a, n in Counter(r[2] for r in rows).most_common(): print(f'  {n:3}  {a}')
json.dump(d, open('camps2027.json','w'), ensure_ascii=False, indent=1)
