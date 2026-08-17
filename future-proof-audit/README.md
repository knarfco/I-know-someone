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
cd future-proof-audit
npm install
npx vercel dev
```

This starts a local copy at `http://localhost:3000`.

## Deploying it so it's live on the internet

See the main project's deployment instructions from the assistant — in
short, this folder is built to deploy on [Vercel](https://vercel.com) for
free, with the "Root Directory" for the project set to `future-proof-audit`.
