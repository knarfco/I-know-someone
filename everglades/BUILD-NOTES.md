# Everglades build notes (internal, not uploaded, not shown to the client)

## What's here
- `build/content.py`: all copy and data (business facts, services, counties, cities, sample jobs, Q&A). `[[text]]` = yellow placeholder.
- `build/build.py`: generates `site/`. Run `python3 everglades/build/build.py`.
- `site/`: the upload. Contents go straight into Hostinger `public_html` (index.html at the top).

## Standing rule: MediaIn360 credit on every page
- "Produced and Powered by MediaIn360" sits small in the **bottom-right of every page**, linking to https://mediain360.com (new tab).
- `credit(cur, light_bg=False)` in build.py. `footer()` adds it automatically, so **every new page that uses the standard layout gets it for free**. Pages with their own layout (front door, capability statement, QR sheet, 404) call it directly; any new custom-layout page must too.
- Files: `assets/img/mediain360-credit-light.png` (white + orange, for dark backgrounds) and `mediain360-credit.png` (original colors, for light backgrounds / print).
- The client owns the site; the credit stays as the design attribution.
- Size is locked **on the image tag itself** (80 px, inline style), so it stays tiny even if a stale or missing stylesheet loads.

## Cache-proof uploads
- Every build copies CSS/JS to content-hashed names (`site.<hash>.css`, `site.<hash>.js`, `qrcode.<hash>.js`) and rewrites every page to point at them (`fingerprint_assets()`). Edit `site.css` / `site.js` as usual; the hashed copies regenerate.
- `.htaccess` marks HTML/PHP as no-cache, so each upload shows immediately; hashed CSS/JS can be cached safely.
- Background: the first live upload showed new pages with an OLD stylesheet (Hostinger server/CDN copy). Hashed names make that impossible. If anything still looks stale, hPanel → Performance → Cache Manager / CDN → Purge all.

## Legal, compliance & accessibility
- `build/legal.py`: Privacy, Terms, Accessibility Statement, Compliance & Certifications (Drug-Free Workplace, E-Verify, EEO, safety, ethics, public records), Text Messaging Terms. Linked in every footer and on the front door. `[[...]]` = facts to confirm (effective date, testing policy, OSHA/EMR, E-Verify ID, venue county, analytics). Attorney review before launch.
- Bid form has an unchecked SMS opt-in (carrier/TCPA language) linking Text Terms and Privacy.
- Accessibility: every page audited with axe-core (WCAG 2.1 A/AA + best-practice), desktop and mobile: 0 issues as of `AUDIT_DATE` in build.py. Re-run after adding pages and update `AUDIT_DATE` (shown on the Accessibility Statement). Add captions to every YouTube job video.

## Final sweep layout (Oct 24, 2026)
- **Home hero:** "Built in the Everglades. Ready for Anywhere." + buyer line, [Request a Bid] [Capability Statement], "Since 1992 · Licensed · Bonded · Insured", Procurement Card (UEI, CAGE, license, FEMA, bonding, E-Verify), which becomes chips on phones.
- **Hero video:** set `BIZ["hero_video"]` in content.py (`mp4`, optional `mp4_mobile`, `webm`, `poster`) and put files in `site/assets/video/`. Silent, looped, autoplay, dark overlay, pause button (WCAG 2.2.2), hidden for reduce-motion. Empty = placeholder. Target 10–20 s, 1080p ≈3–6 MB MP4 (H.264) + WebM, 720p mobile version, poster JPG.
- **Home = short landing page:** hero → "At a Glance" (one-line 'who we are' + 9 teasers, each 1–2 sentences with a varied info link: capabilities, government & primes, job videos, core services, projects anywhere, where we've worked, property owners, compliance, Q&A) → closing band. Everything else lives on its own page; inner pages link back via breadcrumbs. Informational tone, not salesy.
- **Accordions:** home "At a Glance" = 9 collapsed headers (two independent columns on desktop, one on phones), each opening to 1–2 sentences + links to the supporting pages. Footer Licenses / Capabilities / Company = `<details data-desktop-open>`: shipped open, collapsed on phones by site.js. Front door, Government & Primes, Credentials and the capability statement stay fully open.
- **Proof linking:** `proof_card()` ("Backed by") on service, capability-category and job pages links each claim to credentials, compliance, job videos, the capability statement and the matching capability or government page; government and credentials pages carry "Related" link rows.
- **Menu:** Capabilities (mega: 7 areas + 8 core services) · Government & Primes · Projects ▾ · Company ▾ · [Request a Bid]. Phones: full-screen panel with Request a Bid + Call on top; 📞 button in the header. Pinned bottom call bar removed.
- **Footer (every page):** logo + one-line contact → full Licenses & Registrations grid (`CREDS`) → Capabilities / Company links → legal + MediaIn360 credit.

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
- Sample jobs have `place: None`: their location shows as `[[City, State / Country]]` and no place pages are made. Until real places exist, Where We've Worked shows an any-state / any-country preview.
- Headquarters is a placeholder (`BIZ['hq']`) in the footer, About and capability statement. Fill it in at launch; Google trusts a real home base.

## Front door = digital business card (built for procurement offices)
- `/` → logo · **Call · Email · See the Website** · all of `CREDS` above the fold · QR (auto-points at whatever domain it's on) · Capability Statement · Save Contact (`assets/everglades-contact.vcf`).
- `CREDS` in content.py drives the front door, home hero (first 6), government page, credentials page and capability statement. Rename or delete rows to match what they actually hold.
- `/capability-statement/` prints on one Letter page (browser → Save as PDF).
- `phone_tel` is `+1XXXXXXXXXX` for now. Set the real number and every Call button and the vCard update.
- Future: a 60–90s narrated reel from their footage for agencies (front door / government page).

## Capability map + Matt's checklist
- `build/taxonomy.py`: 38 categories in 7 sections, 395 public services (Matt's 30-category list, duplicates removed, plus gaps added in review: trucking, materials, debris reduction, maintenance contracts, erosion control and revegetation, species and tree relocation, recreation sites, site documentation).
- Pages: `/capabilities/` hub → 7 section pages → 38 category pages (service list with each future URL, "How Buyers Find This": Google / YouTube / AI / bid portals) → 7 sample service pages (one per section).
- High-hazard categories (11, 12, 13, 14, 29) are worded publicly as earthwork / support with qualified partners. Contaminant lists, radiological/munitions items and the internal #30 items (referral routing, sub qualification) live in `private` and show **only** on the checklist.
- `/plan/checklist/` (noindex): 418 items, each We do it / Sub-team / Not for us. Saved in that browser's localStorage; Email / Copy / Print send the answers back.
- **Send to us** posts the answers to `send-checklist.php` (PHP on Hostinger), which emails them to `CHECKLIST_TO` (knarfco@yahoo.com, set in build.py) and **always saves a copy** in `public_html/submissions/` (web access blocked by `.htaccess`). If email lands in spam or fails, the copy is still there in File Manager. A backup **Email** button opens his mail app pre-addressed.
- After Matt answers: delete the "Not for us" items from taxonomy.py, rebuild, and build out real service pages for the rest as jobs come in. Every service already has a reserved URL.

## Video Log + YouTube Playbook
- Video links come in on a spreadsheet: `docs/presentation/Everglades_Video_Log.xlsx` (one row per video; client fills it in and emails it, re-sending the updated file as they add videos). The old `/plan/videos/` web page + `send-video.php` are still in the build but no longer used: remove them at the next site upload.
- `docs/presentation/youtube-playbook.html` → `Everglades_YouTube_Playbook.pdf` (14 slides): channel setup, name/handle, upload, title format, short link, Video Log, best clips for the hero (originals via WeTransfer, stored on the MediaIn360 server), filming tips, privacy, checklist. No channel access needed; optional later: YouTube **Editor** role for captions and description links.
- Each logged link → add to `PROJECTS` with `youtube: "VIDEO_ID"` and its `place`, rebuild.

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

## Go-live phase (not yet built)
- **Switches:** real domain → `SITE_URL`; `PREVIEW=False`; `FRONT_DOOR_AT_ROOT=False`; submit sitemap to Google Search Console + Bing Webmaster.
- **SEO:** titles/descriptions pass, deeper internal linking, page speed, Google Business Profile, consistent name/address/phone across directories (citations).
- **AEO:** build Question Bank answers as short-answer-first pages (40–60 word answer, then detail, then proof), structured data on each.
- **GEO:** captioned YouTube job videos, strong About / company-facts page, directory and industry listings so AI tools can cite them.
- **Content & wiring:** real photos/videos/licenses, Matt's answers, hero video files, bid-form endpoint, analytics + call tracking, attorney review.

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

## Bid Finder app (internal, proposed)
- Pitched in `docs/presentation/TerraAll_Strategy_Presentation_v3.pdf` (one slide + the "TerraAll Digital Findability Network" slide) and `TerraAll_Bid_Finder_App.pdf` (8 slides).
- Plan: nightly search of public procurement sources (SAM.gov, state/county portals, water districts, CPRA, prime sub lists) filtered by Matt's dials (size, area, work type, role) → morning list on his phone → Take it / Team it / Route it / 86 it.
- Back end: Supabase (cheap to run); phone-friendly web app on top. Never named in client docs.
- Bid support (additional service): plain-English bid summary, then drafting and production. Matt sets prices, checks facts and signs. No dollar amounts in any client doc; terms in person.
