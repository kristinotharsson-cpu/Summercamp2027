# Rebuilding the 2027 camp page

The page is one self-contained HTML file. Two ways to change it:

**Small edit (one camp):** open `../summercamp2027.html`, find the `let camps = [` array,
edit that camp's line. Nothing to rebuild.

**Bigger update (new dates land in the new year):**
1. Edit `../camps2027.json` — set `status` to `"confirmed"`, fill in `dates`,
   and set `regStatus` (`open` / `opens` / `tbd`) plus `regDate` (`YYYY-MM-DD`).
2. From this folder: `python3 build_page.py`
3. It rewrites `summercamp2027.html` in the scratch folder — copy it up one level.

`build_page.py` works by patching `live-summercamp2026.html` (last year's page, kept here
as the base) and injecting `inject.css` + `inject.js`. Every patch is checked: if the base
file changes and a patch no longer matches, the build stops and names the step rather than
producing a half-edited page.

## Re-checking camp websites
- `fetch.sh <index> <url>` downloads one camp page into `dl/`
- `digest.py <indices…>` prints the date-shaped lines from those pages
- `grab.py dl/<n>.html "<regex>" [width] [count]` digs into one page

## Fields on a camp
`status` confirmed|tbc · `dates` · `regStatus` open|opens|tbd · `regDate` · `note`
(why it's flagged) · `ref2026` (last year's dates, shown small on flagged cards) ·
`checked` (date stamp shown on every card) · `location` · `id` (used by the saved list)
