import json, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
d = json.load(open('camps2027.json'))

# The directory's "Camp Hale" pointed at United South End Settlements' overnight camp
# on Squam Lake, NH (contact Richard Webb). JQES families mean Hale Education in
# Westwood. Keep the USES camp as its own clearly-named listing; make Hale the favorite.
uses = next(c for c in d if c['id'].startswith('camp-hale'))
uses['name'] = 'Camp Hale — overnight in New Hampshire (United South End Settlements)'
uses['favorite'] = False
uses['favoriteNote'] = None
uses['note'] = ("A different organization from Hale Education in Westwood. USES lists these session "
                "dates without a year, so they are not confirmed as 2027.")

d.append({
 "name":"Hale Day Camp (Westwood)",
 "id":"hale-day-camp-westwood",
 "status":"confirmed",
 "dates":"June 21 – August 20, 2027 · Counselor-in-Training runs June 21 – August 13, 2027",
 "hours":"8:45am – 3:45pm · Hale does not offer an extended day option",
 "cost":("$975–$2,400 depending on unit and number of sessions · Kindercamp and Lower Camp $975–$1,925 · "
         "Teen Camp $1,075–$2,075 · CIT $2,295–$2,400 · Financial aid available"),
 "ages":"4–15 · Kindercamp 4–5 · Lower 6–7 · Middle 8–10 · Teen 11–13 · CIT 14–15",
 "ageRange":[4,15],
 "description":("Hale Education's classic day camp on its own reservation in Westwood — swimming and "
   "boating in the ponds, archery, arts and crafts, field games, hiking, fishing and a low and high ropes "
   "course. Over 1,000 campers each summer, split into five age-based units by rising grade, with a 1:6 "
   "staff-to-camper ratio in Lower Camp. Middle and Teen Camp take off-site trips, and Teen Camp includes "
   "an overnight campout at Hale. Kindercampers need to be toilet-trained."),
 "registration":"Open now — enroll at hale.education · Bus sign-up is separate, after you enroll, and due by May",
 "regStatus":"open", "regDate":None,
 "extendedDay":"No",
 "categories":["Nature & Outdoor","Sports & Athletics","Arts & Creative"],
 "free":False,
 "location":"80 Carby Street, Westwood, MA 02090",
 "transport":("Free camp buses — every camper rides one. Stops in Braintree, Brookline, Dedham, Dorchester, "
   "Dover, Framingham, Jamaica Plain, Medfield, Milton, Natick, Needham, Newton, Norwood, Roslindale, Walpole, "
   "Wellesley, West Roxbury and Westwood. A staff member rides every route. Drop-off and pick-up at camp are "
   "not permitted, though there is a local bus stop in Westwood if you would rather drive."),
 "contact":"Jaclyn Ross, Director of Camp and Community Programs · 781-326-1770",
 "url":"https://hale.education/program/hale-day-camp/",
 "isNew":True,
 "favorite":True,
 "favoriteNote":("Hale's free buses do not currently stop in Chinatown or downtown — the closest are "
   "Dorchester, Roslindale, West Roxbury and Jamaica Plain. JQES is looking into a pickup at school. "
   "Email josiahquincyparentcouncil@gmail.com to let us know if you would be interested."),
 "note":None,
 "checked":"Nov 17, 2026",
})

RANK = {'open':0, 'opens':1, 'tbd':2}
d.sort(key=lambda c: (c['status'] != 'confirmed', not c.get('favorite'), RANK[c['regStatus']],
                      c['regDate'] or '9999', c['name'].lower()))
json.dump(d, open('camps2027.json','w'), ensure_ascii=False, indent=1)
print(f"total {len(d)} · confirmed {sum(1 for c in d if c['status']=='confirmed')} · "
      f"favorites {sum(1 for c in d if c.get('favorite'))}")
print("favorites:", [c['name'] for c in d if c.get('favorite')])
