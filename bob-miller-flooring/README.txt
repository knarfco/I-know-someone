BOB MILLER FLOORING — MOCK-UP WEBSITE
=====================================

Unzip and upload everything to the root (public_html / web root) of your
temporary domain, keeping the "images" folder next to the HTML files. No build step and no
server code is needed; it is plain HTML, CSS and JavaScript.

PAGES
  index.html          Home (new light "workshop" design: Bob's words, video slot,
                      before/during/after project, floor-layers explainer,
                      project wall, sample board, reviews)
  our-work.html       Portfolio: before/after sliders, filterable gallery, lightbox
  bobs-story.html     Bob's story, decade timeline, values, crew
  services.html       Floor Finder comparison tool, 6 services, FAQ
  service-areas.html  South Florida + Pittsburgh, ZIP checker, town lists
  free-quote.html     Contact / quote form with CAPTCHA

PLACEHOLDER SLOTS
  On the home page, small dashed red labels ("Bob's real photo", "Video slot",
  "Sample until interview", etc.) mark where Bob's real photos, video, quotes
  and Google rating go. Delete each label once the real item is in.

PLACEHOLDERS (made up for the mock-up)
  South Florida phone  (954) 555-0163
  Pittsburgh phone     (412) 555-0187
  Email                hello@bobmillerflooring.com
  Reviews, project stories, hours and the timeline years are samples.
  555-01xx numbers are reserved for fiction, so they won't ring anyone.
  To change the phone numbers everywhere, search-and-replace them across the files.

CAPTCHA
  The form uses Cloudflare Turnstile with Cloudflare's public TEST key
  (always passes, works on any domain). If Turnstile can't load, a simple
  "what is 3 + 4" check appears instead. A hidden honeypot field also
  catches bots.
  For go-live: create a free Turnstile site at dash.cloudflare.com and
  paste your site key into TURNSTILE_SITEKEY at the top of script.js.

FORM DELIVERY
  Right now the form shows a thank-you message but does not send anything.
  To get emails, create a free form endpoint (Formspree, Basin, etc.) and
  paste its URL into FORM_ENDPOINT at the top of script.js.

SEARCH ENGINES
  Every page has <meta name="robots" content="noindex,nofollow"> so the
  temporary domain doesn't get indexed. Remove that line when you launch on
  the real domain.
