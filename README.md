# Future-Proof Audit V2

A small web tool that checks one webpage's raw HTML against the 9 mechanical
criteria defined in the "Future-Proof Audit — V2" spec. Every result is
**PASS**, **FAIL**, **NOT VERIFIABLE**, or (for the one conditional
criterion) **SKIPPED** — there is no AI model involved in producing a
verdict. The tool fetches the page's raw HTML on the server, parses the
actual tags, and applies the exact conditions written in the spec.

## What it checks

1. H1 Present & Unique
2. Heading Hierarchy Logical
3. Canonical Tag Present
4. Meta Description Present
5. Structured Data (Schema) Present & Valid
6. Crawlability Baseline (meta robots + HTTP status)
7. AI Crawler Access (robots.txt vs. GPTBot, ClaudeBot, PerplexityBot, Google-Extended, OAI-SearchBot)
8. Organization/LocalBusiness Schema Completeness
9. FAQPage Schema (conditional — skipped if the page has no FAQ-style content)

## How it works

- `index.html` — the page you open in a browser. It has a box to type a URL
  and a button to run the audit. It shows the results in a table.
- `api/audit.js` — the "brain." When you submit a URL, your browser asks
  this code to fetch that page's HTML directly (server to server, not
  through your browser, so there are no CORS/browser restrictions), read
  the tags, and check each of the 9 rules. It also fetches `robots.txt`
  from the site for criterion 7.

This only reads the HTML delivered by the very first server response. It
does not run the page's JavaScript. Per the spec's own implementation
notes, all 9 criteria check elements that are expected to already be
present in that first HTML response, so this is the correct approach — but
if a site builds these elements entirely with client-side JavaScript, a
FAIL here reflects what's in the raw source, not necessarily what a user's
browser eventually renders.

## One page, one report

Per the spec, each run checks exactly one URL. To check a whole site, run
it once per page — don't assume one page's result applies to any other page.

## Running it locally (optional — for testing before it's live)

You need [Node.js](https://nodejs.org) installed (v18+), and the free
[Vercel CLI](https://vercel.com/docs/cli):

```
npm install
npx vercel dev
```

This starts a local copy at `http://localhost:3000`.

## Deploying it so it's live on the internet

This tool lives at the root of this repository on purpose, so it deploys
on [Vercel](https://vercel.com) with zero configuration — just import this
repository and deploy, no settings need to be changed.

## MediaIn360 Super Intelligence Readiness Check ($1.99)

The paid, MediaIn360-branded version of this audit. The page lives on
mediain360.com (`readiness-check.html`); the engine is these three endpoints:

- `api/readiness-checkout.js` — validates the form and starts a $6.97
  Stripe Checkout session (website, business name and city are stored in
  the session's metadata).
- `api/readiness-report.js` — runs only for a *paid* Checkout session:
  the 9 website checks from `api/audit.js`, plus a YouTube video-presence
  check, and emails the report once.
- `api/readiness-config.js` — a small public endpoint the static page
  reads on load to find out whether Turnstile is configured (and its
  site key, which is meant to be public). Lets the site pick up Turnstile
  the moment it's turned on, with no redeploy of mediain360.com itself.

Nothing turns on until these are set in Vercel → Project → Settings →
Environment Variables (then redeploy):

| Variable | What it does |
|---|---|
| `STRIPE_SECRET_KEY` | **Required.** Turns on checkout. Until it's set, the page falls back to "email us to run your check." |
| `YOUTUBE_API_KEY` | Turns on the YouTube check (Google Cloud → YouTube Data API v3). Without it, that check reads "Can't verify." |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `REPORT_FROM_EMAIL` | Turns on emailing the report. For Zoho Mail: `smtp.zoho.com`, port `465`, the mailbox address and an app password. |
| `REPORT_BCC_EMAIL` | Optional: a copy of every report (e.g. `info@mediain360.com`) — every buyer becomes a lead. |
| `READINESS_SITE_URL` | Optional; defaults to `https://mediain360.com`. |
| `TURNSTILE_SITE_KEY`, `TURNSTILE_SECRET_KEY` | Turns on Cloudflare Turnstile (a free, non-Google bot check) on checkout. Get both from a free Cloudflare account → Turnstile → add a site for `mediain360.com`. Until both are set, checkout runs with no bot check at all rather than silently blocking every submission. |

In Stripe, turn on Radar (fraud screening) — small charges attract
card-testing bots. The three lead forms (`demo.html`, `self-shoot.html`,
`signup.html`) each also carry a honeypot field (`#hp_field`) as a
no-account-needed first layer: a bot that fills every field on the page
fills that one too, and the form quietly pretends to succeed without
actually sending anything.

## Accessibility check (internal only)

`api/_accessibility.js` runs a real WCAG 2.2 AA scan (axe-core, against the
actually-rendered page via a real headless browser) on one public URL.
Deliberately has no linked public page — not meant for prospects or the
public to self-serve, only for in-house use and for `api/prospector.js`'s
own `check_accessibility` tool. Never issues a pass/fail "compliance"
verdict; reports concrete, verifiable findings and states plainly that
manual review is still required.

- `api/accessibility.js` — plain internal HTTP endpoint:
  `GET /api/accessibility?url=...`
- `api/prospector.js` — once it has found and fetched a business's real
  homepage, it can call the same check as a tool and fold a real finding
  into the outreach email, alongside the existing V8-F2 rubric findings.

Blocks requests to private/internal IP ranges (localhost, 10.x, 192.168.x,
link-local/cloud-metadata addresses, etc.) — re-validated on every
sub-request the target page itself makes, not just the URL typed in.

## CAN-SPAM footer on prospector outreach emails

Every email `api/prospector.js` drafts closes with a required footer: a
real business mailing address and an opt-out instruction pointing back to
the prospector's own inbox (they send it, so they're the one who sees and
honors a reply). This is a legal requirement on any commercial email
regardless of who hits send or how personalized it is — not something to
shorten or remove.

| Variable | What it does |
|---|---|
| `CORXIT_MAILING_ADDRESS` | **Required before sending anything.** The real physical business mailing address, used verbatim in every drafted email's footer. Until it's set, drafts contain an obvious placeholder instead of a real address — don't send those. |
