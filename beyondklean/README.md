# Beyond Klean — proof-of-concept site

A static HTML site for Beyond Klean, an in-house construction and specialty cleaning company: 438 service pages, 20 family hubs, a large FAQ library, a glossary, a bid request page with a bid list, and an internal estimator. Every page is plain HTML with relative links, so the `site/` folder can be uploaded to any static host as-is.

The site is marked **noindex** and `robots.txt` blocks crawlers until launch. Forms are demo-only and do not send anything yet.

## Layout

| Path | What it is |
|---|---|
| `research/` | Task research, `tasks.csv` / `tasks.json` and the report |
| `content/families.py` | Family intros and family-level FAQs |
| `content/general.py` | Glossary, general FAQ, markets and the static pages (home, methods, GCs, quote, about) |
| `content/company.py` | Company facts, credentials, projects, clients and quotes. Empty values show as Pending in preview; set `SHOW_SLOTS = False` at launch |
| `content/trust.py` | Projects, capability statement, safety and contact pages, and the proof blocks on home and service pages |
| `content/expansion.py` | Categories 21-24, services added to existing families, merged names; content in `f21`-`f25`, family intros in `famx*.py`, prices in `research/pricing_x*.json` |
| `content/hubs.py` | Facility-type and project-phase hubs and the government procurement hub |
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
- Fill in `content/company.py` (phone, email, address, credentials, projects with photos in `site/assets/projects/`), then set `SHOW_SLOTS = False`.
- Keep `/estimator/` out of search (`Disallow: /estimator/`). It is locked by its own password (`ESTIMATOR_PASSWORD` in `build_site.py`); Hostinger's Password Protect Directories can add a server login on top.
- Add Search Console, Bing Webmaster Tools (with IndexNow) and Apple Business Connect.
- Replace the preview bar.

## Estimator

`site/estimator.html` is the in-house estimating program (its scripts and encrypted data live in `site/estimator/`, and `/estimator/` forwards to it), not linked from the site and opened with a password (`ESTIMATOR_PASSWORD` in `build_site.py`, default `12345`). Its data ships encrypted in `estimator/pricebook.enc.js` and is decrypted in the browser on unlock (https or localhost only).

- **Your costs:** wages by crew role with payroll burden, supervision, crew size and shift, night premium, local or travel crew (mileage, lodging, per diem), equipment by the day, disposal, overhead and target margin.
- **The job:** any number of line items from the 438 construction tasks or 70 routine janitorial tasks, each with its own quantity, unit, height, soil level and crew. Hours come from production rates; labor, materials, cost, price and margin are calculated per line. Lines price at market rates (low, typical, high) or at cost plus target margin.
- **Recurring contracts:** tasks by frequency, giving monthly hours, cleaners per night, monthly price, price per square foot per month and annual value.
- **Summary:** days on site, cost breakdown, profit, margin against target, profit per crew-hour, a market check and a what-if price slider.
- **Outputs:** internal estimate PDF, customer quote PDF (no internal numbers), estimate CSV, and a bids list with status tracking, win rate and a CRM-ready CSV export. Company defaults, templates and the price book are editable and saved in the browser.

Data lives in `research/pricing.json`, `content/routine.py` and `content/est_data.py`. Production rates and material costs are starting points to be replaced with each contractor's own numbers.
