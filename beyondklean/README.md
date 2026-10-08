# Beyond Klean — proof-of-concept site

A static HTML site for Beyond Klean: 438 specialty and construction cleaning service pages, 20 family hubs, a 2,397-answer FAQ library, a glossary, and quote and contractor-application pages. Every page is plain HTML with relative links, so the `site/` folder can be uploaded to any static host as-is.

The site is marked **noindex** and `robots.txt` blocks crawlers until launch. Forms are demo-only and do not send anything yet.

## Layout

| Path | What it is |
|---|---|
| `research/` | Task research, `tasks.csv` / `tasks.json` and the report |
| `content/families.py` | Family intros and family-level FAQs |
| `content/general.py` | Glossary, general FAQ and the static pages (home, methods, GCs, join, quote, about) |
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
- Connect the quote and join forms to a real inbox or CRM.
- Add Search Console, Bing Webmaster Tools (with IndexNow) and Apple Business Connect.
- Replace the preview bar.
