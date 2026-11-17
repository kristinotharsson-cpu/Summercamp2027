You are running unattended as a weekly maintenance job for the JQES summer camp directory
in /Users/cseries/Desktop/Claude/jqes/summer-camps-2027. Work only inside that folder.

A sweep has already run and written `build/weekly-findings.json`. Read it.

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
5. Commit the changes with git (no push; there is no remote configured).

If nothing met the bar, still append a CHANGELOG.md entry saying the check ran and found
nothing conclusive. Never invent a date. A wrong date in front of a family is far worse
than a missed update.
