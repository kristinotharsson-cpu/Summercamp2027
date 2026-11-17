# Uploading to jqesscc.netlify.app

## Read this first
Netlify's drag-and-drop deploy **replaces the whole site with whatever you drop**.
Drop `summercamp2027.html` on its own and the homepage and the 2026 page disappear.

So drop the **folder**, not the file.

## What to do
1. Log in to the Netlify account that owns `jqesscc` (it is not the account logged in
   on this Mac — that one has 8 other sites and jqesscc is not among them).
2. Open the site → **Deploys**.
3. Drag the whole **`deploy-folder`** onto the drop zone.
4. Check these three afterwards:
   - https://jqesscc.netlify.app/ (homepage)
   - https://jqesscc.netlify.app/summercamp2026.html (last year, kept as archive)
   - https://jqesscc.netlify.app/summercamp2027.html (new)

**If the site is connected to GitHub instead**, don't drag anything — the drop zone
will be disabled. Add `summercamp2027.html` to the repo and push.

## What's in deploy-folder
| File | What it is |
|---|---|
| `index.html` | your homepage, as published, **plus one fix** (see below) |
| `summercamp2026.html` | last summer's page, downloaded from the live site, untouched |
| `summercamp2027.html` | the new page |

## The homepage fix
The footer "Email us" link on the live homepage is broken right now. The HTML carries a
Cloudflare email-obfuscation stub (`/cdn-cgi/l/email-protection#...`) that needs a decoder
script at `/cdn-cgi/scripts/.../email-decode.min.js`. That path 404s on Netlify, so the
decoder never runs: the link reads **"[email protected]"** instead of the address, and
clicking it goes to a 404.

It got baked in when the page was saved from somewhere that sat behind Cloudflare.

`index.html` in the folder has the real `mailto:josiahquincyparentcouncil@gmail.com` put
back, the placeholder text replaced with the address, and the dead decoder script removed.
Nothing else is changed. The address was already public on the camp page, so this exposes
nothing new.

The untouched original is one level up as `index.homepage-before-email-fix.html` — if you
would rather not touch the homepage at this point, swap it back in before you deploy.

---

## After you deploy: repoint the Google Site

The SCC Google Site at `sites.google.com/view/jqes-school-community-council` has a
**Resources** nav item that currently links to:

    https://jqesscc.netlify.app/summercamp2026.html

Families clicking "Resources" will land on last summer's page until that link is changed to
`summercamp2027.html`. Edit it in Google Sites → Resources nav item → change the URL.

The same Google Site also links out to `getinvolvedatjqes.netlify.app` and
`roomparentsjqes.netlify.app`, both of which *are* on the Netlify login on this Mac —
only `jqesscc` is on a different account.

## Does the countdown keep working after upload?

Yes. "Registration opens Wed, Dec 9, 2026 — in 22 days" is calculated in each visitor's
browser every time the page loads, from the opening dates stored in the page. Nothing is
frozen at upload time, so:

- the day count ticks down on its own
- a camp flips from blue to orange once it is within 30 days
- once the date passes, the card says "Registration should now be open"

What does *not* update by itself is the underlying research — whether a camp has posted its
2027 dates, and the camps currently marked "open now". The header shows how long ago the page
was checked, and after 45 days it turns that line into an amber warning telling families to
confirm with the camp. Re-run the research (see `build/README.md`) when that appears.
