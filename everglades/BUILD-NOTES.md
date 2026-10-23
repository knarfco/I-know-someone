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

## The web (how pages feed each other)
Job video (YouTube, short link) → **job page** `/projects/{service}-{city}-{year}/`
→ links up to its **service page**, **city page**, **county page**
→ those list every job in them (auto-generated from `PROJECTS`)
→ the home page and footer link to every service and county.
Each new video = one new dated page plus fresh content on 3 existing pages. That's the growth engine.

### Adding a job
Add an entry to `PROJECTS` with `youtube: "VIDEO_ID"`. That turns on the real embed (lite, click-to-load) and the `VideoObject` structured data. Rebuild.

### Adding a city
Add it to `CITIES` (it's already listed under its county). It gets a page and automatically switches from "soon" to a link everywhere. **Only publish a city once it has a real job or real local substance.** Thin city/ZIP pages = doorway-page risk under Google's scaled-content rules.

## Scaling path toward 90k
service × county → service × city (with proof) → job pages (one per video) → Q&A + Shorts → statewide → national. Keep every page backed by a real job, real local facts, or a real answer.

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
- [ ] Videos + job list → `PROJECTS`; photos → before/after slots
- [ ] Form endpoint
- [ ] Flip `PREVIEW`, set `SITE_URL`, flip `FRONT_DOOR_AT_ROOT`
- [ ] GBP verified, linked in footer and `sameAs`
- [ ] Search Console + Bing Webmaster, submit sitemap
- [ ] Analytics + call tracking
- [ ] Lawyer review of the privacy page
- [ ] Optional: clean vector redraw of the logo
