import json, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
d = json.load(open('camps2027.json'))
conf  = [c for c in d if c['status']=='confirmed']
tbc   = [c for c in d if c['status']!='confirmed']
op    = [c for c in d if c['regStatus']=='open']
dated = sorted([c for c in d if c['regStatus']=='opens'], key=lambda c: c['regDate'])
favs  = [c for c in d if c.get('favorite')]

L = ["# Summer 2027 camp research — JQES SCC\n",
     "Every program checked against its own website on **November 17, 2026**.\n",
     f"- **{len(d)} programs** total — {len(conf)} have published 2027 dates, {len(tbc)} have not yet",
     f"- **{len(op)} open for registration now**, {len(dated)} with a dated opening",
     f"- **{len(favs)} marked as JQES fan favorites**\n"]

L.append("\n## Registration diary\n")
for c in dated:
    L.append(f"- **{c['regDate']}** — {c['name']}  \n  {c['registration']}")
L.append("\n**Open right now:** " + ", ".join(c['name'] for c in op) + "\n")

L.append("\n## JQES fan favorites\n")
for c in favs:
    L.append(f"- **{c['name']}** — {'2027 dates published' if c['status']=='confirmed' else 'dates not yet posted'}")
    if c.get('favoriteNote'): L.append(f"  - {c['favoriteNote']}")
L.append("")

L.append("\n## Published their 2027 dates\n")
for c in conf:
    L.append(f"### {c['name']}")
    L.append(f"- **Dates:** {c['dates']}")
    L.append(f"- **Hours:** {c['hours']}")
    L.append(f"- **Cost:** {c['cost']}")
    L.append(f"- **Ages:** {c['ages']}")
    L.append(f"- **Registration:** {c['registration']}")
    if c.get('location'):  L.append(f"- **Location:** {c['location']}")
    if c.get('transport'): L.append(f"- **Getting there:** {c['transport']}")
    if c.get('contact'):   L.append(f"- **Contact:** {c['contact']}")
    L.append(f"- {c['url']}\n")

L.append("\n## Still to come — chase list\n")
L.append("| Program | What their site says now | Link |")
L.append("|---|---|---|")
for c in sorted(tbc, key=lambda c: c['name'].lower()):
    L.append(f"| {c['name']} | {(c.get('note') or '').replace('|','/')} | {c.get('url') or ''} |")

L.append("\n## Worth a phone call or email\n")
for c in tbc:
    n = (c.get('note') or '').lower()
    if any(k in n for k in ('out of date','unavailable','blocked','no dates posted','no summer schedule','not listed on the site')):
        L.append(f"- **{c['name']}** — {c['note']} ({c.get('url') or 'no link'})")
L.append("\nNory and Ivy Seed were emailed on November 17, 2026 and have not replied yet.\n")

L.append("\n## Fixed or corrected along the way\n")
L.append("- **Camp Hale was the wrong organization.** The directory listed United South End Settlements' "
         "overnight camp on Squam Lake, NH (contact Richard Webb, rwebb@uses.org). JQES families mean "
         "**Hale Education in Westwood**. Hale Day Camp is now its own listing with 2027 dates, free bus "
         "routes and Jaclyn Ross as the contact. The USES camp is kept as a separate, clearly-named entry.")
L.append("- **Boston Ballet** was not in the directory at all and has been added.")
L.append("- Five dead links now point at working pages: Wheelock Family Theatre, Mass Audubon Blue Hills, "
         "Agassiz Village, and both BCYF entries.")
L.append("- The 2026 page's camp list had six stray commas, so it counted 60 programs when only 54 existed.")
L.append("- B-SAFE was listed as July 7 – August 8, 2026; their own site said July 6 – August 7, 2026.")
L.append("- Everwood, Hill House Day Camp and Hill House Kiddie Kamp had no category at all, so they were "
         "invisible to every category filter.")

INFERRED = [
 ("Camp Shriver at UMass Boston", "Dorchester & South Boston", "UMass Boston is on Columbia Point"),
 ("BMP Summer Strings", "Chinatown & Downtown", "80 Boylston St"),
 ("MFA Summer Art Camp", "Fenway & Longwood", "465 Huntington Ave"),
 ("Boston Children's Museum", "Dorchester & South Boston", "308 Congress St, Fort Point"),
 ("Nory", "Beacon Hill & Back Bay", "60 Commonwealth Ave"),
 ("Ivy Seed", "Fenway & Longwood", "BU campus"),
 ("BCYF Camp Joy", "South End & Roxbury", "1483 Tremont St"),
 ("Community Boat Building", "Dorchester & South Boston", "21 Liberty Drive, Seaport"),
 ("Wang YMCA Day Camp / YMCA Summer Camps", "Chinatown & Downtown", "the Wang Y is the Chinatown branch"),
 ("Piers Park Sailing Center", "Charlestown & East Boston", "Piers Park is in East Boston"),
 ("Northeastern — Math Masters", "Fenway & Longwood", "Northeastern campus"),
 ("BCYF Leahy-Holloran @ Perry School", "Dorchester & South Boston", "Leahy-Holloran is in Dorchester"),
 ("Tenacity", "Several locations", "runs at sites across the city"),
]
L.append("\n## Neighborhoods — which ones I inferred\n")
L.append("Most came straight from an address on the camp's own site or in the brief. These I worked out "
         "from a known address rather than the camp saying so — worth a glance:\n")
L.append("| Camp | Placed in | Why |")
L.append("|---|---|---|")
for n, a, why in INFERRED:
    L.append(f"| {n} | {a} | {why} |")
unplaced = [c['name'] for c in d if c.get('area','').startswith(('Boston —','Location not'))]
L.append("\nStill without a neighborhood: " + ", ".join(unplaced) + ".\n")
L.append("\n**Corrected:** Minni x Urbanity had been given Nory's address (60 Commonwealth Ave) by mistake; "
         "it now just says South End. Tenacity, B-SAFE and BCYF Camp Joy were showing 2026 registration dates "
         "as though they were upcoming, and now read as last year's dates.\n")

open('RESEARCH-NOTES.md','w',encoding='utf-8').write('\n'.join(L))
print('RESEARCH-NOTES.md regenerated')
