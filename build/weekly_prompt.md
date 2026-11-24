You are the weekly maintenance job for the JQES summer camp directory, a public resource
for families at Josiah Quincy Elementary School in Boston. Work only inside this repository.

`camps2027.json` holds 61 camps. Each has `status` ("confirmed" once the camp has published
its summer 2027 dates, otherwise "tbc") and `regStatus` ("open", or "opens" with a `regDate`
of YYYY-MM-DD, or "tbd"). `summercamp2027.html` is a single self-contained page built from
that JSON. Families read it; a wrong date in front of them is far worse than a missed update.

Start by running: python3 -I build/weekly_check.py

That sweep writes `build/weekly-findings.json` and edits nothing itself. Read it. It
separates what it found into three lists, and each needs a different response.

**`link_problems`** — a camp whose URL no longer resolves. Treat this as a real finding,
not a skipped row. A dead link usually means the camp renamed or moved its page, and the
new page often carries the dates we are waiting for. Open the site's root, look for the
current summer page, and if you find a clear replacement, update that camp's `url` and say
so. If you cannot find one, leave the url alone and list the camp as needing a person.
These links are also broken for every family reading the page, so never pass over them.

**`changed`** — a camp we already mark `confirmed` whose page now shows session dates we
have not stored. Confirmed does not mean finished. A camp can add a location, publish a
week-by-week schedule where we stored a one-line span, or drop a week. Compare what we hold
against the page and update `dates` when the page is clearly more specific or more current.
If the page merely says the same thing in other words, change nothing.

**`findings`** — a camp whose 2027 dates or registration date were unknown and whose page
now shows a 2027 or registration signal. These are the ones to judge strictly, below.

Each finding is a camp whose stored record says its 2027 dates or registration date are
NOT yet known, together with text scraped from its website this morning.

For each finding, decide whether the site now states something unambiguous:
  - a registration opening date for summer 2027, or
  - summer 2027 session dates.

Apply an update to `camps2027.json` ONLY when the page says it plainly. Be strict:
  - "Register Now" or "Registration is open" next to 2026 sessions is NOT a 2027 signal.
  - "Registration closed for summer 2026" is NOT a 2027 signal.
  - A date with no year attached is NOT confirmation. Check the weekday if you must:
    a Mon-Fri camp starting "June 21" fits 2027, not 2026.
  - A year appearing only in a page footer, a copyright line or site navigation is NOT a signal.
If you are unsure, leave the record alone and note it as needing a human.

When you do update a camp, set the fields consistently:
  - dates + status:"confirmed" when 2027 session dates are published
  - regStatus:"open" when registration is open now
  - regStatus:"opens" plus regDate:"YYYY-MM-DD" when a future opening date is given
  - registration: a short human sentence, US spelling, month-day-year order
  - checked: today's date as "Mon D, YYYY"
  - clear `note` if it no longer applies

Then:
1. Run `python3 -I build/build_page.py` to rebuild summercamp2027.html.
2. Run `python3 -I build/gen_notes.py` to refresh RESEARCH-NOTES.md.
3. Run `python3 -I build/britcheck.py summercamp2027.html camps2027.json` and fix any
   British spellings or day-month-year dates it reports, except the proper noun
   "Wheelock Family Theatre" and its course name "Theatre Design & Tech".
4. Append a dated section to CHANGELOG.md listing every camp you changed, with the exact
   sentence from the website that justified it, and separately list camps that looked
   promising but were too ambiguous to act on.
5. Commit the changes. If a git remote named `origin` exists, push to `main` so the
   rebuilt page is available to download; if there is no remote, just commit.

If nothing met the bar, still append a CHANGELOG.md entry saying the check ran and found
nothing conclusive. Never invent a date. A wrong date in front of a family is far worse
than a missed update.

Finish by stating plainly, in your final message: how many camps you changed and which,
how many you left alone as too ambiguous, and whether anything needs a person to phone or
email the camp. If you changed nothing, say so.
