import json, sys
p = 'camps2027.json'
d = json.load(open(p))
by = {c['name']: c for c in d}

FAVS = ["BMP Summer Strings (Boston Music Project)",
        "Minni Summer Program – Beacon Hill",
        "Minni × Urbanity Dance – South End",
        "Camp Hale (United South End Settlements)",
        "Nike Tennis Camp at MIT",
        "New England Base Camp – Cub Scout Day Camp (JQES Pack 617 Bus)"]

TRANSPORT = {
 "Everwood Day Camp":"Camp buses with pick-up and drop-off across Greater Boston, staffed by trained bus counsellors. Seatbelts on every bus, licensed school-year drivers. Optional add-on priced by stop; dropping off at camp yourself is free.",
 "Summer at BB&N (Buckingham Browne & Nichols)":"Two bus routes run every camp week on BB&N's own buses with their own drivers. First pick-up around 8:00am, all campers on campus by 8:30am; buses leave at about 3:15pm with the last drop-off by 4:00pm.",
 "Nike Tennis Camp at MIT":"No transport provided — the camp states it does not run transport to or from the airport, train stations or bus depots.",
 "Camp Hale (United South End Settlements)":"USES runs pick-up and drop-off in Boston so families don't have to drive to New Hampshire.",
 "Red Sox Summer Camp":"No camp-run transport. Sessions are spread across six venues, so pick the week nearest you.",
 "Experience Camps (Grief Camp, Maine)":"Overnight camp in Maine. Arrival and departure arrangements are shared closer to the session.",
 "Minni Summer Program – Beacon Hill":"No camp-run transport — drop-off and pick-up at 125 Charles St.",
 "Hill House Day Camp":"No camp-run transport — drop-off and pick-up at 127 Mt. Vernon St.",
 "Hill House Kiddie Kamp":"No camp-run transport — drop-off 8:30–9:00am and pick-up 1:00–1:30pm at 127 Mt. Vernon St.",
 "Warrior Ice Arena (Boston Bruins Practice Facility)":"No camp-run transport — 90 Guest St, Brighton.",
 "BMP Summer Strings (Boston Music Project)":"No camp-run transport — 80 Boylston St, Boston.",
}

LOCATION = {
 "Everwood Day Camp":"125 Lakeview Street, Sharon, MA 02067 (on Lake Massapoag)",
 "Summer at BB&N (Buckingham Browne & Nichols)":"80 Gerry's Landing Road, Cambridge, MA 02138",
 "BMP Summer Strings (Boston Music Project)":"80 Boylston St, Boston, MA 02116",
 "Warrior Ice Arena (Boston Bruins Practice Facility)":"90 Guest Street, Brighton, MA 02135",
 "Experience Camps (Grief Camp, Maine)":"Camp Somerset, 11 Somerset Lane, Smithfield, ME",
 "Red Sox Summer Camp":"Six venues: Belmont Hill School, Newton South HS, Danehy Park (Cambridge), Beverly HS, Beverly (TBD), Lexington (TBD)",
 "Camp Hale (United South End Settlements)":"Sleepaway camp on Squam Lake, Sandwich, NH · Boston office and Meet the Staff Day at USES, 48 Rutland St, Boston, MA 02118",
}

CATS = {
 "Everwood Day Camp":["Nature & Outdoor","Sports & Athletics","Arts & Creative"],
 "Hill House Day Camp":["Sports & Athletics","Arts & Creative"],
 "Hill House Kiddie Kamp":["Arts & Creative"],
}

for c in d:
    c.setdefault('transport', None)
    c.setdefault('favorite', False)
    c.setdefault('favoriteNote', None)
    n = c['name']
    if n in FAVS: c['favorite'] = True
    if n in TRANSPORT: c['transport'] = TRANSPORT[n]
    if n in LOCATION:  c['location']  = LOCATION[n]
    if n in CATS:      c['categories'] = CATS[n]

# ── Camp Hale, refreshed from uses.org ──
h = by["Camp Hale (United South End Settlements)"]
h['description'] = ("Sleepaway camp on Squam Lake in Sandwich, New Hampshire, run by United South End "
  "Settlements. Serves 300+ Boston boys and girls each summer in the White Mountains, with archery, "
  "gardening, swimming and time outdoors at its centre. Cabins offer modern amenities a few steps from "
  "the lake. 74% of families served are low-income and 80% of campers identify as BIPOC.")
h['dates'] = ("Boys Session 1: June 21 – July 5 · Boys Session 2: July 6 – July 19 · Family Camp: July 23–26 · "
  "Girls Session 3: July 26 – August 8 · Girls Session 4: August 9–23 · All-Gender Session 5: August 26 – September 2 (7 days)")
h['hours'] = "Overnight (sleepaway) · 2-week sessions, plus a 7-day all-gender session and a 4-day Family Camp"
h['registration'] = "Register at camphale.campmanagement.com · Meet the Staff Day June 14 at USES, 48 Rutland St"
h['note'] = ("USES lists these session dates without a year, so they are not confirmed as 2027 — worth checking "
  "before you plan around them. Everything else here is current from uses.org.")
h['favoriteNote'] = ("JQES is looking into a bus pick-up at school for Camp Hale. "
  "Email josiahquincyparentcouncil@gmail.com to let us know if you'd be interested.")

# ── Boston Ballet — not previously in the directory ──
d.append({
 "name":"Boston Ballet School Summer Camps",
 "id":"boston-ballet-school-summer-camps",
 "cost":"Check website · Financial aid available",
 "ages":"2–9 (age as of August 31)", "ageRange":[2,9],
 "description":("Boston Ballet School's summer programmes for young dancers — co-ed, and new students are "
   "welcome. Ages 2–6 Summer Sessions blend the school-year curriculum with summer fun, building musical, "
   "body and spatial awareness through storytelling and movement. Ages 5–6 Preparatory Workshop explores "
   "preparatory ballet technique and creative dance. Ages 7–9 Foundations Workshop focuses on technique, "
   "conditioning and stretching alongside enrichments such as modern dance, ballet history and ballet mime."),
 "dates":"2027 dates not yet posted",
 "registration":"Not yet open for 2027",
 "hours":"Check website — varies by programme",
 "extendedDay":"—",
 "categories":["Dance & Movement","Performing Arts","Arts & Creative"],
 "free":False,
 "location":"Boston, Brookline and Newton studios",
 "url":"https://www.bostonballet.org/education-artical/summer-camps/",
 "isNew":True, "status":"tbc",
 "note":"The summer camp pages still describe the 2026 season (ages are given as of 31 August 2026).",
 "transport":"No camp-run transport listed.",
 "favorite":True, "favoriteNote":None,
 "regStatus":"tbd", "regDate":None,
 "checked":"Nov 17, 2026",
})

RANK = {'open':0, 'opens':1, 'tbd':2}
d.sort(key=lambda c: (c['status'] != 'confirmed', not c.get('favorite'), RANK[c['regStatus']],
                      c['regDate'] or '9999', c['name'].lower()))
json.dump(d, open(p,'w'), ensure_ascii=False, indent=1)

print(f"total {len(d)} · favourites {sum(1 for c in d if c.get('favorite'))} · "
      f"with transport info {sum(1 for c in d if c.get('transport'))}")
print("favourites:", [c['name'] for c in d if c.get('favorite')])
missing = [c['name'] for c in d if c['status']=='confirmed' and not c.get('categories')]
print("confirmed camps still without a category:", missing or "none")
