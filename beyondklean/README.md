# Beyond Klean — proof-of-concept site

A static HTML site for Beyond Klean, an in-house construction and specialty cleaning company: 438 service pages, 20 family hubs, a large FAQ library, a glossary, a bid request page with a bid list, and an internal estimator. Every page is plain HTML with relative links, so the `site/` folder can be uploaded to any static host as-is.

The site is marked **noindex** and `robots.txt` blocks crawlers until launch. Forms are demo-only and do not send anything yet.

## Layout

| Path | What it is |
|---|---|
| `research/` | Task research, `tasks.csv` / `tasks.json` and the report |
| `content/families.py` | Family intros and family-level FAQs |
| `content/general.py` | Glossary, general FAQ, markets and the static pages (home, methods, GCs, quote, about) |
| `content/inhouse.py` | Rewrites applied at build time that turn referral-network wording into in-house voice |
| `content/estimator.html` | Body of the internal estimator page (`site/estimator/`) |
| `research/pricing.json` | Price book: unit and low / typical / high rate per task, with sources (`PRICING.md`) |
| `content/f*.py` | First-draft content for every task |
| `content/p*.py` | Rewrites that replace weak fields of a task (applied after `f*`) |
| `content/a*.py` | Single-answer rewrites keyed by (task, question number) |
| `build_site.py` | Generator: reads everything above and writes `site/` |
| `quality_scan.py` | Flags thin content (short answers, ledes, lists) |
| `site/` | The generated site |

## Build

```
python3 build_site.py      # writes site/, checks links and page-to-page similarity
python3 quality_scan.py -v # lists any task content that is still thin
```

## Before launch on beyondklean.com

- Remove `noindex` and replace `robots.txt`.
- Connect the bid request form to a real inbox or CRM (both owner and operator copied, with the reference number).
- Set `PHONE` and `OPERATOR` at the top of `build_site.py`.
- Keep `/estimator/` out of search (`Disallow: /estimator/`) and password-protect it in Hostinger (hPanel → Password Protect Directories).
- Add Search Console, Bing Webmaster Tools (with IndexNow) and Apple Business Connect.
- Replace the preview bar.

## Estimator

`site/estimator/index.html` is an internal quoting tool, not linked from the site. Pick services from the price book, enter quantities, add mobilization, travel, premiums, overhead and profit, discount and tax, then print to PDF or export a CSV for a spreadsheet. The Company tab sets the header of the company performing the work. Rates are starting points: edit them on the Price book tab (saved in that browser) and export or import the book as JSON to move it between computers.
