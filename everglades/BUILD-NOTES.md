# Everglades build notes (internal, not uploaded, not shown to the client)

## What's here
- `build/content.py`: all copy and data (business facts, services, counties, cities, sample jobs, Q&A). `[[text]]` = yellow placeholder.
- `build/build.py`: generates `site/`. Run `python3 everglades/build/build.py`.
- `site/`: the upload. Contents go straight into Hostinger `public_html` (index.html at the top).

## Settings in build.py
| Flag | Now | At launch |
|---|---|---|
| `PREVIEW` | `True`: every page is noindex and robots.txt blocks crawling, so the temporary domain never gets indexed and can't compete with the real one later | `False` |
| `SITE_URL` | `https://www.XXX-domain.com` | real domain (sitemap and structured data use it) |
| `FRONT_DOOR_AT_ROOT` | `True`: the logo front door is `/`, the full home is `/home/` | `False`: the full home becomes `/` (best for Google), and the front door moves to `/welcome/` for QR codes, truck decals and print |

## Location-agnostic by design (client request)
No service areas, no county or city target pages, no "jobs in X" pitches. The site sells **the work, anywhere**.
Locations appear **only** where a real job was done:
- Each job in `PROJECTS` has a `place` (city / region / country; works outside the U.S. too).
- `build_place_index()` turns those into **Where We've Worked**: `/where-weve-worked/{region}/{city}/`. A place exists only once a job video exists there.
- **Projects Anywhere** (`/projects-anywhere/`) covers long-distance jobs: Matt plans it, and our crew or licensed local crews do it.
- South Florida is named once, as headquarters (footer and About), plus the GBP address. That keeps local trust signals without boxing them in.

## The web (how pages feed each other)
Job video (YouTube, short link) → **job page** `/projects/{service}-{city}-{year}/`
→ links to its **service page** and its **place pages** (city + region)
→ those list every job in them automatically
→ the home page, the "Where We Work" menu and the footer list every place.
Each new video = one new dated page, plus fresh content on its service and place pages, and possibly a brand-new place page. That's the growth engine.

### Adding a job
Add an entry to `PROJECTS` with `youtube: "VIDEO_ID"` and its `place`. That turns on the real embed (lite, click-to-load), the `VideoObject` structured data and the place pages. Rebuild.

## Scaling path toward 90k
job pages (one per video) → place pages (grow from jobs) → service × place combos where several jobs back them → Q&A + Shorts. Every page stays backed by a real job or a real answer. No empty location pages.

## Lead routing (hidden)
`request-a-bid` sets hidden `lead_lane`:
- **A**: government, utility or engineer role, OR a solicitation # is filled in, OR 20+ acres / linear work on wetland, exotic or FEMA services → straight to Matt.
- **B**: contractor, developer, HOA or commercial role, OR 5+ acres → priority quote.
- **C**: everything else → referral pool (licensed partner crews, percentage).

The form also captures `landing_page`, `referrer` and "how did you find us".
**The form isn't connected yet.** `action="#"` just jumps to the thank-you page. Before launch: point it at a PHP mail handler on Hostinger, Formspree, or a CRM, and route emails by `lead_lane`.

## Before go-live checklist
- [ ] Fill every `[[...]]` in content.py (search for `[[`)
- [ ] Real phone → `BIZ["phone_tel"]` (turns on tap-to-call everywhere)
- [ ] Videos + job list (with `place`) → `PROJECTS`; photos → before/after slots
- [ ] Form endpoint
- [ ] Flip `PREVIEW`, set `SITE_URL`, flip `FRONT_DOOR_AT_ROOT`
- [ ] GBP verified, linked in footer and `sameAs`
- [ ] Search Console + Bing Webmaster, submit sitemap
- [ ] Analytics + call tracking
- [ ] Lawyer review of the privacy page
- [ ] Optional: clean vector redraw of the logo
