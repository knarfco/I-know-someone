#!/usr/bin/env python3
"""Builds the Everglades Restorations & Land Clearing static site into ../site/.

Run:  python3 everglades/build/build.py
Output is plain HTML/CSS/JS that can be uploaded to any host (Hostinger, etc.).
"""
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import BIZ, CREDS, SERVICES, SVC, AUDIENCES, PROJECTS, QUESTIONS  # noqa: E402
from taxonomy import SECTIONS, CATEGORIES, EXAMPLES  # noqa: E402
from legal import LEGAL, EFFECTIVE  # noqa: E402

CAT = {c["slug"]: c for c in CATEGORIES}
N_SERVICES = sum(len(c["services"]) for c in CATEGORIES)

# ---------------------------------------------------------------- settings
# PREVIEW keeps the temporary domain out of Google (noindex + robots.txt block).
# Set to False only when the site is on its real, permanent domain.
PREVIEW = True
# Final domain (used for sitemap, canonical-ready structured data). Placeholder until known.
SITE_URL = "https://www.XXX-domain.com"
# The logo "front door" sits at the root for the presentation; the full home page is /home/.
# At launch, set False to make the full home page the root (best for Google) and move
# the front door to /welcome/ for QR codes and print.
FRONT_DOOR_AT_ROOT = True
# Where "Send to us" on Matt's service checklist delivers (send-checklist.php, server-side).
CHECKLIST_TO = "knarfco@yahoo.com"
# Date of the most recent accessibility (axe-core) audit, shown on the Accessibility Statement.
AUDIT_DATE = "October 24, 2026"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "site")
HOME = "home/" if FRONT_DOOR_AT_ROOT else ""
DOOR = "" if FRONT_DOOR_AT_ROOT else "welcome/"

PAGES = {}       # path -> html
PLACES = {}      # filled in main() from PROJECTS
SITEMAP = []     # indexable paths


def ph(s):
    """[[text]] -> visible placeholder span."""
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="ph">\1</span>', s)


def plain(s):
    """[[text]] -> text (for JSON-LD / meta)."""
    return re.sub(r"\[\[(.+?)\]\]", r"\1", s)


def rel(cur, target):
    depth = cur.count("/")
    prefix = "../" * depth
    if not target:
        return prefix or "./"
    return prefix + target


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def tel_href(cur):
    return f"tel:{BIZ['phone_tel']}" if BIZ["phone_tel"] else rel(cur, "request-a-bid/")


def place_label(pl):
    if not pl:
        return "[[City, State / Country]]"
    return f"{pl['city']}, {pl['region'] or pl['region_name']}"


def region_path(pl):
    return f"where-weve-worked/{slugify(pl['region_name'])}/"


def place_path(pl):
    return region_path(pl) + slugify(pl["city"]) + "/"


def build_place_index():
    """Regions -> cities -> jobs, built only from real job pages."""
    regions = {}
    for p in sorted(PROJECTS, key=lambda p: p["date"], reverse=True):
        pl = p["place"]
        if not pl:
            continue
        r = regions.setdefault(slugify(pl["region_name"]), {"name": pl["region_name"], "country": pl["country"],
                                                            "path": region_path(pl), "cities": {}, "projects": []})
        r["projects"].append(p)
        c = r["cities"].setdefault(slugify(pl["city"]), {"name": pl["city"], "label": place_label(pl),
                                                        "path": place_path(pl), "projects": []})
        c["projects"].append(p)
    return dict(sorted(regions.items(), key=lambda kv: -len(kv[1]["projects"])))


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace("'", "")).strip("-")


# ---------------------------------------------------------------- schema
ORG_ID = SITE_URL + "/#business"


def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": ["GeneralContractor", "LocalBusiness"],
        "@id": ORG_ID,
        "name": BIZ["name"],
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/assets/img/everglades-logo.png",
        "image": SITE_URL + "/assets/img/everglades-logo.png",
        "foundingDate": BIZ["founded"],
        "telephone": plain(BIZ["phone"]),
        "email": plain(BIZ["email"]),
        "address": {"@type": "PostalAddress", "streetAddress": plain(BIZ["address"]),
                    "addressCountry": "US"},
        "knowsAbout": [s["name"] for s in SERVICES],
        "sameAs": [plain(BIZ["youtube"]), plain(BIZ["gbp"])],
    }


def crumbs_schema(trail):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE_URL + "/" + path}
            for i, (name, path) in enumerate(trail)
        ],
    }


def faq_schema(pairs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": plain(re.sub("<[^>]+>", "", a))}}
                       for q, a in pairs],
    }


# ---------------------------------------------------------------- layout pieces
CREDIT_URL = "https://mediain360.com"


def credit(cur, light_bg=False):
    """MediaIn360 design credit. Goes bottom-right on EVERY page (footer() adds it automatically)."""
    img = "assets/img/mediain360-credit.png" if light_bg else "assets/img/mediain360-credit-light.png"
    return (f'<a class="credit" href="{CREDIT_URL}" target="_blank" rel="noopener" title="Produced and Powered by MediaIn360">'
            f'<img src="{rel(cur, img)}" alt="Produced and Powered by MediaIn360" width="80" height="21" style="width:80px;max-width:80px;height:auto;display:block"></a>')


def header(cur):
    L = lambda p: rel(cur, p)  # noqa: E731
    areas = "".join(f'<a href="{L("capabilities/" + k + "/")}"><b>{n}</b><span>{d}</span></a>' for k, n, d in SECTIONS)
    core = "".join(f'<a href="{L("services/" + x["slug"] + "/")}">{x["name"]}</a>' for x in SERVICES)
    return f"""
<a class="skip" href="#main">Skip to content</a>
<div class="topbar" role="region" aria-label="Contact"><div class="wrap">
  <span class="since">Land Clearing · Excavation · Restoration</span>
  <span>Call <a href="{tel_href(cur)}">{ph(BIZ['phone'])}</a> · Storm response 24/7</span>
</div></div>
<header class="header"><div class="wrap">
  <a class="brand" href="{L(HOME)}" aria-label="{esc(BIZ['name'])} home">
    <img src="{L('assets/img/everglades-mark.png')}" alt="" width="54" height="54">
    <span class="brand-name">EVERGLADES<small>RESTORATIONS &amp; LAND CLEARING INC.</small></span>
  </a>
  <a class="hdr-call" href="{tel_href(cur)}" aria-label="Call {esc(plain(BIZ['phone']))}">📞</a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="nav">☰ Menu</button>
  <nav class="nav" id="nav" aria-label="Main">
    <div class="nav-quick">
      <a class="btn btn-yellow" href="{L('request-a-bid/')}">Request a Bid</a>
      <a class="btn btn-ghost" href="{tel_href(cur)}">📞 Call</a>
    </div>
    <ul>
      <li><details><summary>Capabilities</summary><div class="menu mega">
        <div class="mega-areas"><div class="menu-head">Areas of expertise</div>{areas}</div>
        <div class="mega-core"><div class="menu-head">Core services</div>{core}
        <a class="mega-all" href="{L('capabilities/')}">All capabilities →</a></div>
      </div></details></li>
      <li><a class="top" href="{L('who-we-serve/government-agencies/')}">Government &amp; Primes</a></li>
      <li><details><summary>Projects</summary><div class="menu">
        <a href="{L('projects/')}">Job Videos</a>
        <a href="{L('where-weve-worked/')}">Where We've Worked</a>
        <a href="{L('projects-anywhere/')}">Projects Anywhere</a>
      </div></details></li>
      <li><details><summary>Company</summary><div class="menu">
        <a href="{L('about/')}">About Us</a>
        <a href="{L('credentials/')}">Licenses &amp; Credentials</a>
        <a href="{L('compliance/')}">Compliance</a>
        <a href="{L('questions/')}">Questions &amp; Answers</a>
        <a href="{L('reviews/')}">Reviews</a>
      </div></details></li>
    </ul>
    <a class="btn btn-yellow btn-sm nav-bid" href="{L('request-a-bid/')}">Request a Bid</a>
  </nav>
</div></header>"""


def footer(cur):
    L = lambda p: rel(cur, p)  # noqa: E731
    caps = "".join(f'<li><a href="{L("capabilities/" + k + "/")}">{n}</a></li>' for k, n, _ in SECTIONS)
    return f"""
<footer class="footer"><div class="wrap">
  <div class="foot-top">
    <div class="logo-plate footer-logo"><img src="{L('assets/img/everglades-logo-640.webp')}" alt="{esc(BIZ['name'])}" width="640" height="289" loading="lazy"></div>
    <p class="foot-contact"><a href="{tel_href(cur)}">{ph(BIZ['phone'])}</a> · {ph(BIZ['email'])} · Headquartered in {ph(BIZ['hq'])} · {ph(BIZ['hours'])}</p>
  </div>
  <section class="foot-creds" aria-label="Licenses and registrations">
    <h2 class="foot-h">Licenses &amp; Registrations</h2>
    {creds_grid()}
  </section>
  <div class="foot-links">
    <div><h2 class="foot-h">Capabilities</h2><ul>{caps}<li><a href="{L('capabilities/')}">All capabilities</a></li></ul></div>
    <div><h2 class="foot-h">Company</h2><ul>
      <li><a href="{L('who-we-serve/government-agencies/')}">Government &amp; Primes</a></li>
      <li><a href="{L('who-we-serve/contractors-developers/')}">Contractors &amp; Developers</a></li>
      <li><a href="{L('who-we-serve/homeowners-ranches/')}">Homeowners, Ranches &amp; HOAs</a></li>
      <li><a href="{L('projects/')}">Job Videos</a></li>
      <li><a href="{L('projects-anywhere/')}">Projects Anywhere</a></li>
      <li><a href="{L('about/')}">About Us</a></li>
      <li><a href="{L('capability-statement/')}">Capability Statement</a></li>
      <li><a href="{L('questions/')}">Questions &amp; Answers</a></li>
      <li><a href="{L('request-a-bid/')}">Request a Bid</a></li>
    </ul></div>
  </div>
  <div class="legal">
    <span>© <span data-current-year>2026</span> {BIZ['name']} · Since {BIZ['founded']}</span>
    <span class="legal-right"><nav class="legal-links" aria-label="Legal"><a href="{L('privacy/')}">Privacy</a><a href="{L('terms/')}">Terms</a><a href="{L('accessibility/')}">Accessibility</a><a href="{L('compliance/')}">Compliance</a><a href="{L('text-terms/')}">Text Terms</a></nav>{credit(cur)}</span>
  </div>
</div></footer>"""


def page(cur, title, desc, body, schema=None, crumbs=None, noindex=False, chrome=True, extra_head=""):
    L = lambda p: rel(cur, p)  # noqa: E731
    robots = "noindex, nofollow" if (PREVIEW or noindex) else "index, follow"
    blocks = [org_schema()] + (schema or [])
    if crumbs:
        blocks.append(crumbs_schema(crumbs))
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks)
    body_html = (header(cur) + f'<main id="main">{body}</main>' + footer(cur)) if chrome else body
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(plain(title))}</title>
<meta name="description" content="{esc(plain(desc))}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#06381A">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(plain(title))}">
<meta property="og:description" content="{esc(plain(desc))}">
<meta property="og:image" content="{L('assets/img/everglades-logo.png')}">
<link rel="icon" href="{L('assets/img/icon-32.png')}" sizes="32x32">
<link rel="apple-touch-icon" href="{L('assets/img/icon-180.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{L('assets/css/site.css')}">
{extra_head}
{ld}
</head>
<body>
{ph(body_html)}
<script src="{L('assets/js/qrcode.js')}" defer></script>
<script src="{L('assets/js/site.js')}" defer></script>
</body>
</html>
"""
    PAGES[cur] = html
    if not noindex:
        SITEMAP.append(cur)


def crumb_html(cur, trail):
    L = lambda p: rel(cur, p)  # noqa: E731
    parts = [f'<a href="{L(p)}">{esc(n)}</a>' for n, p in trail[:-1]]
    parts.append(f'<span aria-current="page" style="margin:0;opacity:1">{esc(trail[-1][0])}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>›</span>".join(parts) + "</nav>"


def page_hero(cur, trail, h1, lead, ctas=True, eyebrow=""):
    L = lambda p: rel(cur, p)  # noqa: E731
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    c = (f'<div class="ctas"><a class="btn btn-yellow" href="{L("request-a-bid/")}">Request a Bid</a>'
         f'<a class="btn btn-ghost" href="{tel_href(cur)}">Call {BIZ["phone"]}</a></div>') if ctas else ""
    return f"""<section class="page-hero"><div class="wrap">{crumb_html(cur, trail)}{eb}<h1>{h1}</h1><p class="lead">{lead}</p>{c}</div></section>"""


def video(label, sub="YouTube link goes here", yt="", title=""):
    return (f'<div class="video" data-yt="{yt}" data-title="{esc(title or label)}">'
            f'<div><div class="play"></div><div class="vlabel">{label}</div><div class="vsub">{sub}</div></div></div>')


def before_after(caption="Before / after photos go here"):
    return f"""<div class="ba">
  <div class="ba-img ba-before"><span>Before photo</span></div>
  <div class="ba-img ba-after"><span>After photo</span></div>
  <span class="tag l">BEFORE</span><span class="tag r">AFTER</span>
  <div class="ba-handle"></div>
  <input type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">
</div><p class="video-caption">{caption}</p>"""


def cta_band(cur, h="Got a job? We'll go where it is.", p="Big or small, near or far — tell us about it and we'll get back to you fast."):
    L = lambda p_: rel(cur, p_)  # noqa: E731
    return f"""<section class="cta-band"><div class="wrap">
  <div><h2>{h}</h2><p>{p}</p></div>
  <div class="ctas"><a class="btn btn-yellow" href="{L('request-a-bid/')}">Request a Bid</a>
  <a class="btn btn-ghost" href="{tel_href(cur)}">Call {BIZ['phone']}</a></div>
</div></section>"""


def service_cards(cur, slugs, cls="g3"):
    L = lambda p: rel(cur, p)  # noqa: E731
    out = []
    for s in slugs:
        sv = SVC[s]
        out.append(f'<a class="card" href="{L("services/" + s + "/")}"><h3>{sv["name"]}</h3>'
                   f'<p>{sv["lead"]}</p><span class="more">Learn more</span></a>')
    return f'<div class="grid {cls}">' + "".join(out) + "</div>"


def project_card(cur, p):
    L = lambda x: rel(cur, x)  # noqa: E731
    return (f'<a class="card proj" href="{L("projects/" + p["slug"] + "/")}" data-service="{p["service"]}" '
            f'data-region="{slugify(p["place"]["region_name"]) if p["place"] else ""}" data-year="{p["date"][:4]}">'
            f'<div class="thumb"><span class="date">{p["date_label"]}</span></div>'
            f'<div class="body"><div class="meta">{SVC[p["service"]]["name"]} · {place_label(p["place"])}</div>'
            f'<h3>{p["title"]}</h3><p>{p["summary"]}</p><span class="more">See the job</span></div></a>')


def project_grid(cur, projects, empty_text, next_text="Next job video goes here"):
    if not projects:
        return f'<div class="empty-slot">{empty_text}</div>'
    return '<div class="grid g3">' + "".join(project_card(cur, p) for p in projects) + \
        f'<div class="empty-slot">{next_text}</div></div>'


def faq_html(cur, faqs):
    L = lambda p: rel(cur, p)  # noqa: E731
    out = []
    for q, a, link in faqs:
        more = f' <a href="{L(link)}">Read more →</a>' if link else ""
        out.append(f"<details><summary>{q}</summary><div><p>{a}{more}</p></div></details>")
    return '<div class="faq">' + "".join(out) + "</div>"


def creds_grid(compact=False):
    rows = CREDS[:6] if compact else CREDS
    return '<dl class="creds">' + "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows) + "</dl>"


def places_preview():
    """Shown until real job locations exist: makes 'any state, any country' obvious."""
    groups = [("[[State]]", 3), ("[[Another State]]", 2), ("[[Country]]", 1)]
    return "".join(f'<h3 class="mt">{g}</h3><ul class="pill-list">' +
                   "".join('<li><span class="soon">[[City]]</span></li>' for _ in range(n)) + "</ul>"
                   for g, n in groups) + \
        '<p class="note mt"><b>Any state. Any country.</b> Every place we work lands here automatically, with the job video to prove it.</p>'


def places_block(cur):
    if not PLACES:
        return places_preview()
    return "".join(f'<h3 class="mt">{r["name"]}</h3>' + place_pills(cur, r["cities"].values()) for r in PLACES.values())


def place_pills(cur, places):
    L = lambda p: rel(cur, p)  # noqa: E731
    return '<ul class="pill-list">' + "".join(
        f'<li><a href="{L(c["path"])}">{c["label"]} <small>· {len(c["projects"])}</small></a></li>' for c in places) + "</ul>"


def anywhere_teaser(cur):
    L = lambda p: rel(cur, p)  # noqa: E731
    return f"""<div class="card lane-card"><span class="eyebrow" style="color:var(--green)">Projects Anywhere</span>
<h3>Big job far from home?</h3><p>We plan it, manage it and put the right crew and equipment on the ground — wherever it is.</p>
<a class="more" href="{L('projects-anywhere/')}">How it works</a></div>"""


# ---------------------------------------------------------------- pages
def build_front_door():
    """Digital business card: call, email, website, every credential, QR. Built for procurement offices."""
    cur = DOOR
    L = lambda p: rel(cur, p)  # noqa: E731
    style = """<style>
body{background:radial-gradient(ellipse at 50% 20%,#13692e 0%,#06381A 45%,#031d0d 100%);color:#fff;min-height:100vh}
.door{max-width:1180px;margin:0 auto;padding:32px 20px 24px}
.door-top{text-align:center}
.door-logo{position:relative;max-width:540px;margin:0 auto}
.door-logo img{width:100%}
.door-tag{color:#fff;font-family:var(--head);font-weight:800;font-size:clamp(1.2rem,2.2vw,1.6rem);letter-spacing:-.01em;margin:16px 0 4px}
.door-sub{color:#bfe0c6;margin:0 0 20px;letter-spacing:.04em}
.door-btns{display:grid;grid-template-columns:repeat(3,minmax(0,220px));gap:12px;justify-content:center}
.door-btns .btn{font-size:1.05rem;padding:15px 18px}
.door-main{display:grid;grid-template-columns:1fr 270px;gap:24px;margin-top:28px;align-items:start}
.door-creds{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:18px 20px}
.door-creds h2{font-size:1.05rem;color:#b9d9bf;margin:0 0 12px;letter-spacing:.06em}
.door-side{display:flex;flex-direction:column;gap:12px}
.qr-panel{background:#fff;color:var(--ink);border-radius:14px;padding:18px;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.4)}
.qr-panel .qr{width:180px;height:180px;margin:0 auto}
.qr-panel .qr svg{width:100%;height:100%}
.qr-panel b{display:block;font-family:var(--head);font-weight:800;font-size:1rem;color:var(--green-deep);margin-top:8px}
.qr-panel small{display:block;color:var(--ink-soft);word-break:break-all;margin-top:2px}
.door-side .btn{width:100%}
.door-foot{text-align:center;padding:14px 20px 8px;color:#8fbf99;font-size:.88rem}
.door-legal{margin-top:8px;font-size:.82rem}
.door-legal a{color:#cfe8d4}
@media (max-width:900px){.door-main{grid-template-columns:1fr}.door-side{max-width:420px;margin:0 auto;width:100%}}
@media (max-width:620px){.door-btns{grid-template-columns:1fr}.door{padding-top:22px}.door-creds{padding:14px}.door-creds .creds{grid-template-columns:1fr 1fr;gap:6px}.door-creds .creds div{padding:7px 9px}.door-creds .creds dt{font-size:.62rem;letter-spacing:.03em}.door-creds .creds dd{font-size:.85rem}}
</style>"""
    email = plain(BIZ["email"])
    body = f"""
<main class="door" id="main">
  <div class="door-top">
    <div class="door-logo logo-plate"><img src="{L('assets/img/everglades-logo.webp')}" alt="{esc(BIZ['name'])}" width="1400" height="632"></div>
    <h1 class="door-tag">Land Clearing · Excavation · Restoration</h1>
    <p class="door-sub">Any state · Any country</p>
    <div class="door-btns">
      <a class="btn btn-ghost" href="tel:{BIZ['phone_tel']}">📞 Call Now</a>
      <a class="btn btn-ghost" href="mailto:{email}">✉️ Email Us</a>
      <a class="btn btn-yellow" href="{L(HOME)}">🌐 See the Website</a>
    </div>
  </div>
  <div class="door-main">
    <section class="door-creds" aria-label="Licenses and registrations">
      <h2>Licenses &amp; Registrations</h2>
      {creds_grid()}
    </section>
    <div class="door-side">
      <div class="qr-panel">
        <div class="qr" id="qr-door" data-qr="/" role="img" aria-label="QR code to open this website on a phone"></div>
        <b>Scan to open on your phone</b>
        <small data-qr-url="qr-door"></small>
      </div>
      <a class="btn btn-yellow" href="{L('capability-statement/')}">📄 Capability Statement</a>
      <a class="btn btn-ghost" href="{L('assets/everglades-contact.vcf')}" download>👤 Save Contact</a>
    </div>
  </div>
</main>
<footer class="door-footer"><div class="door-foot">W-9 and certificate of insurance on request · Storm response 24/7<br>{BIZ['name']} · {BIZ['phone']} · {BIZ['email']}
<nav class="door-legal" aria-label="Legal"><a href="{L('privacy/')}">Privacy</a> · <a href="{L('terms/')}">Terms</a> · <a href="{L('accessibility/')}">Accessibility</a> · <a href="{L('compliance/')}">Compliance</a> · <a href="{L('text-terms/')}">Text Terms</a></nav></div>
<div class="credit-row">{credit(cur)}</div></footer>"""
    page(cur, f"{BIZ['name']} | Land Clearing, Excavation & Restoration",
         f"{BIZ['name']}: land clearing, excavation, wetland restoration and storm response since {BIZ['founded']}. Licensed, bonded and registered for public work.",
         ph(body), chrome=False, extra_head=style, noindex=FRONT_DOOR_AT_ROOT is False)


def hero_media(cur):
    """Silent looping background video (self-hosted). Empty HERO_VIDEO = placeholder, no motion."""
    v = BIZ["hero_video"]
    if not v["mp4"]:
        return ('<div class="hero-media" aria-hidden="true"></div>'
                '<span class="hero-video-tag">[[Background video: 10–20 sec loop of their best job footage]]</span>')
    L = lambda p: rel(cur, p)  # noqa: E731
    small = f'<source src="{L(v["mp4_mobile"])}" type="video/mp4" media="(max-width: 760px)">' if v.get("mp4_mobile") else ""
    poster = f' poster="{L(v["poster"])}"' if v.get("poster") else ""
    webm = f'<source src="{L(v["webm"])}" type="video/webm">' if v.get("webm") else ""
    return (f'<div class="hero-media" aria-hidden="true"><video class="hero-vid" muted loop playsinline autoplay preload="metadata"{poster}>'
            f'{small}{webm}<source src="{L(v["mp4"])}" type="video/mp4"></video></div>'
            '<button type="button" class="hero-pause" aria-label="Pause background video" aria-pressed="false">⏸</button>')


def build_home():
    cur = HOME
    L = lambda p: rel(cur, p)  # noqa: E731
    card_rows = [c for c in CREDS if c[0] in ("SAM.gov UEI", "CAGE Code", "Bonding Capacity", "FEMA Vendor #", "E-Verify Company ID", "Certified Contractor License #")]
    pcard = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in card_rows)
    glance = [
        ("Capabilities", "Land, water, cleanup, infrastructure, disaster and rural work — seven areas of expertise, one accountable team.", "capabilities/", "Explore capabilities"),
        ("Government &amp; Primes", "Registrations, bonding, compliance and past performance for agencies and the prime contractors who win their work.", "who-we-serve/government-agencies/", "View the capability snapshot"),
        ("Job Videos", "Real, dated jobs on video — the place, the equipment and the before-and-after.", "projects/", "Watch the work"),
        ("Core Services", "Land clearing, mulching, ponds and canals, site prep, wetlands, invasive removal, drainage and storm debris.", "services/", "See core services"),
        ("Projects Anywhere", "A big job far from home? We plan it, manage it and put the right crew on the ground.", "projects-anywhere/", "How it works"),
        ("Where We've Worked", "Every place listed is backed by a real job video. The list grows with every job.", "where-weve-worked/", "See the places"),
        ("Developers &amp; Property Owners", "Builders, developers, ranches, HOAs and landowners — jobs of every size.", "who-we-serve/", "Find your fit"),
        ("Compliance", "Drug-Free Workplace, E-Verify, safety, equal opportunity and ethics, in plain view.", "compliance/", "Read our policies"),
        ("Questions &amp; Answers", "Straight answers on cost, permits, wetlands and timing.", "questions/", "Read the answers"),
    ]
    glance_html = "".join(f'<div class="glance-item"><h3>{t}</h3><p>{d}</p><a href="{L(u)}">{c} <span aria-hidden="true">→</span></a></div>' for t, d, u, c in glance)
    body = f"""
<section class="hero hero-video">
  {hero_media(cur)}
  <div class="wrap hero-grid">
    <div>
      <h1>Built in the Everglades. Ready for Anywhere.</h1>
      <p class="lead">Land clearing, earthwork and environmental restoration for public agencies, prime contractors and major developers. If we can work the Everglades, we can work your site.</p>
      <div class="ctas">
        <a class="btn btn-yellow" href="{L('request-a-bid/')}">Request a Bid</a>
        <a class="btn btn-ghost" href="{L('capability-statement/')}">📄 Capability Statement</a>
      </div>
      <p class="hero-proof">Since {BIZ['founded']} · Licensed · Bonded · Insured</p>
    </div>
    <aside class="pcard" aria-label="Procurement card">
      <div class="pcard-head">Procurement Card</div>
      <dl>{pcard}</dl>
      <a href="{L('credentials/')}">All licenses &amp; registrations →</a>
    </aside>
  </div>
</section>

<section class="section glance"><div class="wrap">
  <div class="section-head"><span class="eyebrow">At a glance</span><h2>Who We Are</h2>
  <p>{BIZ['name']} clears, digs and restores land and water for public agencies, prime contractors, developers and property owners — since {BIZ['founded']}, in any state or country.</p></div>
  <div class="glance-grid">{glance_html}</div>
</div></section>

<section class="cta-band"><div class="wrap">
  <div><h2>Have a project or solicitation?</h2><p>Send it over, or take our capability statement with you.</p></div>
  <div class="ctas"><a class="btn btn-yellow" href="{L('request-a-bid/')}">Request a Bid</a>
  <a class="btn btn-ghost" href="{L('capability-statement/')}">📄 Capability Statement</a></div>
</div></section>"""
    page(cur, f"Land Clearing, Earthwork & Environmental Restoration Contractor | {BIZ['short']}",
         f"Built in the Everglades. Ready for anywhere. Land clearing, earthwork and environmental restoration for public agencies, prime contractors and major developers. Since {BIZ['founded']}.",
         body)


def build_services():
    cur = "services/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Services", cur)]
    land = [s["slug"] for s in SERVICES if s["group"] == "land"]
    env = [s["slug"] for s in SERVICES if s["group"] == "env"]
    body = page_hero(cur, trail, "Our Services", "Everything from clearing a single lot to restoring wetlands and opening roads after a hurricane.") + f"""
<section class="section"><div class="wrap">
  <h2>Land &amp; Site Work</h2>{service_cards(cur, land, 'g4')}
  <h2 class="mt">Environmental &amp; Storm</h2>{service_cards(cur, env, 'g4')}
  <div class="note mt"><b>Don't see your job?</b> If it involves land, water or heavy equipment, ask us — wherever it is. <a href="{L('request-a-bid/')}">Tell us about it →</a></div>
</div></section>{cta_band(cur)}"""
    page(cur, f"Services | Land Clearing, Excavation & Restoration | {BIZ['short']}",
         "Land clearing, forestry mulching, excavation, site prep, wetland restoration, invasive plant removal, drainage and hurricane debris removal.",
         body, crumbs=trail)

    for s in SERVICES:
        cur = f"services/{s['slug']}/"
        L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
        trail = [("Home", HOME), ("Services", "services/"), (s["name"], cur)]
        projs = [p for p in PROJECTS if p["service"] == s["slug"]]
        places = []
        for p in projs:
            if not p["place"]:
                continue
            if place_path(p["place"]) not in [x[0] for x in places]:
                places.append((place_path(p["place"]), place_label(p["place"])))
        place_links = "".join(f'<li><a href="{L(a)}">{b}</a></li>' for a, b in places) or "<li>Listed here as job videos are added</li>"
        includes = "".join(f"<li>{i}</li>" for i in s["includes"])
        equip = "".join(f"<li>{e}</li>" for e in s["equipment"])
        intro = "".join(f"<p>{p}</p>" for p in s["intro"])
        body = page_hero(cur, trail, s["h1"], s["lead"]) + f"""
<section class="section"><div class="wrap split">
  <div>
    {intro}
    <h2>What's Included</h2><ul class="checks">{includes}</ul>
    <p class="small"><b>Also called:</b> {s['aka']}.</p>
  </div>
  <div>
    {video(s['name'] + ' video', 'Job video for this service goes here')}
    <div class="card mt"><h3>Equipment</h3><ul class="checks">{equip}</ul>
    <a class="btn btn-yellow" href="{L('request-a-bid/?service=' + s['slug'])}">Request a Bid</a></div>
  </div>
</div></section>
<section class="section alt"><div class="wrap">
  <div class="section-head"><h2>Before &amp; After</h2></div>
  <div class="grid g2">{before_after()}{before_after('Second before / after pair')}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>Recent {s['name']} Jobs</h2><p>Real, dated jobs from our project library.</p></div>
  {project_grid(cur, projs, 'Job videos for this service will appear here as they are added.')}
</div></section>
<section class="section sand"><div class="wrap split">
  <div><h2>Questions</h2>{faq_html(cur, s['faqs'])}</div>
  <div><h3>Where we've done this</h3><ul class="checks">{place_links}</ul><div class="mt">{anywhere_teaser(cur)}</div></div>
</div></section>
<section class="section"><div class="wrap"><h2>Related Services</h2>{service_cards(cur, s['related'])}</div></section>
{cta_band(cur, f"Need {s['name'].lower()}?")}"""
        schema = [{
            "@context": "https://schema.org", "@type": "Service", "name": s["name"],
            "serviceType": s["name"], "provider": {"@id": ORG_ID},
            "description": s["lead"],
        }, faq_schema([(q, a) for q, a, _ in s["faqs"]])]
        page(cur, f"{s['name']} Contractor | {BIZ['short']}",
             f"{s['lead']} Licensed and insured — wherever the job is.",
             body, schema=schema, crumbs=trail)


def build_audiences():
    cur = "who-we-serve/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Who We Serve", cur)]
    cards = "".join(f'<a class="card lane-card" href="{L("who-we-serve/" + a["slug"] + "/")}"><h3>{a["name"]}</h3><p>{a["lead"]}</p><span class="more">Learn more</span></a>' for a in AUDIENCES)
    body = page_hero(cur, trail, "Who We Serve", "Agencies, builders and landowners — every one gets a crew that shows up and does the job right.") + \
        f'<section class="section"><div class="wrap"><h2 class="sr">Who we serve</h2><div class="grid g3">{cards}</div></div></section>{cta_band(cur)}'
    page(cur, f"Who We Serve | {BIZ['short']}", "Land clearing and earthwork for government agencies, prime contractors, developers, homeowners, ranches and HOAs.", body, crumbs=trail)

    for a in AUDIENCES:
        cur = f"who-we-serve/{a['slug']}/"
        L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
        trail = [("Home", HOME), ("Who We Serve", "who-we-serve/"), (a["name"], cur)]
        who = "".join(f"<li>{w}</li>" for w in a["who"])
        extra = ""
        if a["slug"] == "government-agencies":
            extra = f"""
<section class="section alt"><div class="wrap split">
  <div>
    <h2>Capability Snapshot</h2>
    <p>{BIZ['name']} · In business since {BIZ['founded']} · Registered bid portals: [[DemandStar · state / county portals XXX]]</p>
    {creds_grid()}
    <p class="mt"><a class="btn btn-green" href="{L('capability-statement/')}">Capability Statement (print / PDF)</a></p>
  </div>
  <div>
    <h3>Past Performance</h3>
    <div class="empty-slot">Project name · agency / prime · year · scope · value<br>[[XXX]]</div>
    <div class="empty-slot mt">Project name · agency / prime · year · scope · value<br>[[XXX]]</div>
    <div class="empty-slot mt">Project name · agency / prime · year · scope · value<br>[[XXX]]</div>
  </div>
</div></section><!--split-->
<section class="section"><div class="wrap prose">
  <h2>Teaming With Prime Contractors</h2>
  <p>Large restoration and water projects need dependable clearing, exotic-removal and earthwork subcontractors who know wet, difficult ground. We know that ground — and we're ready to team on the next one, wherever it's let.</p>
  <p><a class="btn btn-yellow" href="{L('request-a-bid/')}">Send us a scope or solicitation</a></p>
</div></section>"""
        top, rest = (extra.split("<!--split-->") + [""])[:2] if extra else ("", "")
        body = page_hero(cur, trail, a["h1"], a["lead"]) + f"""{top}
<section class="section"><div class="wrap split">
  <div><h2>Who We Work With</h2><ul class="checks">{who}</ul></div>
  <div>{video(a['name'] + ' video', 'A job video for this kind of client goes here')}</div>
</div></section>
{rest}
<section class="section sand"><div class="wrap"><h2>Services for {a['name']}</h2>{service_cards(cur, a['services'])}</div></section>
{cta_band(cur)}"""
        page(cur, f"{a['h1']} | {BIZ['short']}", a["lead"], body, crumbs=trail)


def build_places():
    cur = "where-weve-worked/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Where We've Worked", cur)]
    blocks = "".join(f"""
<div class="card"><h3><a href="{L(r['path'])}">{r['name']}</a></h3>
<p>{len(r['projects'])} job{'s' if len(r['projects']) != 1 else ''} on video</p>{place_pills(cur, r['cities'].values())}</div>""" for r in PLACES.values())
    body = page_hero(cur, trail, "Where We've Worked", "Every place on this page is here because we did a real job there — and there's a dated video to prove it. Any state, any country: the list grows with every job.") + f"""
<section class="section"><div class="wrap"><h2 class="sr">Places</h2>
  {('<div class="grid g2">' + blocks + '<div class="empty-slot">The next place shows up here automatically when its first job video is added.</div></div>') if PLACES else '<div class="prose">' + places_preview() + '</div>'}
</div></section>
<section class="section alt"><div class="wrap">{anywhere_teaser(cur)}</div></section>
{cta_band(cur)}"""
    page(cur, f"Where We've Worked | Job Locations | {BIZ['short']}",
         "Every place we've done land clearing, excavation and restoration work — each backed by a real, dated job video.",
         body, crumbs=trail)

    for r in PLACES.values():
        cur = r["path"]
        L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
        trail = [("Home", HOME), ("Where We've Worked", "where-weve-worked/"), (r["name"], cur)]
        done = sorted({p["service"] for p in r["projects"]})
        body = page_hero(cur, trail, f"Our Work in {r['name']}", f"Real, dated jobs we've done in {r['name']}. Each one has its own page with video, photos and the details.") + f"""
<section class="section"><div class="wrap">
  <h2>Places in {r['name']}</h2>{place_pills(cur, r['cities'].values())}
</div></section>
<section class="section alt"><div class="wrap">
  <div class="section-head"><h2>Jobs in {r['name']}</h2></div>
  {project_grid(cur, r['projects'], '')}
</div></section>
<section class="section sand"><div class="wrap"><h2>What We've Done Here</h2>{service_cards(cur, done)}</div></section>
{cta_band(cur)}"""
        page(cur, f"Our Work in {r['name']} | {BIZ['short']}",
             f"Land clearing, excavation and restoration jobs we've completed in {r['name']} — with video.", body, crumbs=trail)

        for c in r["cities"].values():
            cur = c["path"]
            L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
            trail = [("Home", HOME), ("Where We've Worked", "where-weve-worked/"), (r["name"], r["path"]), (c["name"], cur)]
            done = sorted({p["service"] for p in c["projects"]})
            others = [x for x in r["cities"].values() if x["path"] != c["path"]]
            body = page_hero(cur, trail, f"Our Work in {c['label']}", f"Real jobs we've done in {c['name']}, with video and before-and-after photos. Got one nearby — or anywhere else? We'll go where it is.") + f"""
<section class="section"><div class="wrap split">
  <div>
    <h2>Jobs in {c['name']}</h2>
    {project_grid(cur, c['projects'], '', 'Next ' + c['name'] + ' job video goes here')}
  </div>
  <div>{video(c['name'] + ' job reel', 'Video from our jobs here goes here')}
  <div class="mt">{before_after(c['name'] + ' before / after photos go here')}</div></div>
</div></section>
<section class="section sand"><div class="wrap split">
  <div><h2>What We Did Here</h2>{service_cards(cur, done, 'g2')}</div>
  <div><h3>Other places in {r['name']}</h3>{place_pills(cur, others) if others else '<p>More coming as jobs are added.</p>'}
  <div class="mt">{anywhere_teaser(cur)}</div></div>
</div></section>
{cta_band(cur)}"""
            page(cur, f"Our Work in {c['label']} | {BIZ['short']}",
                 f"Land clearing and excavation jobs we've completed in {c['label']}, with video and photos.", body, crumbs=trail)


def build_anywhere():
    cur = "projects-anywhere/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Projects Anywhere", cur)]
    body = page_hero(cur, trail, "Projects Anywhere", f"Big job far from home? We plan it, manage it and get it done — wherever it is.", eyebrow="Any state · any country") + f"""
<section class="section"><div class="wrap split">
  <div>
    <h2>How It Works</h2>
    <ol class="timeline">
      <li><b>1 · Send the job</b>Plans, photos, video, a solicitation — whatever you have. We review it fast.</li>
      <li><b>2 · We size it up</b>Remote review, then a site visit when the job calls for one.</li>
      <li><b>3 · We plan it</b>Equipment, sequence, permits, schedule and budget — the way we'd run it ourselves.</li>
      <li><b>4 · We put crews on the ground</b>Our own crew and equipment, or licensed local crews working to our plan and under our oversight.</li>
      <li><b>5 · You see it all</b>Progress video and photos from start to finish, so you always know where the job stands.</li>
    </ol>
  </div>
  <div>{video('Projects Anywhere', 'Walkthrough of a long-distance job goes here')}
  <div class="card mt"><h3>Send us a scope</h3><p>Tell us where it is and what it needs.</p>
  <a class="btn btn-yellow" href="{L('request-a-bid/')}">Request a Bid</a></div></div>
</div></section>
<section class="section alt"><div class="wrap">
  <div class="section-head"><h2>What We Take On</h2><p>The work where experience matters most — and where the right plan saves the most money.</p></div>
  <div class="grid g4">
    <div class="card"><h3>Restoration Projects</h3><p>Wetland restoration, mitigation banks, canal backfilling and exotic removal.</p></div>
    <div class="card"><h3>Large Clearing</h3><p>Hundreds of acres for development, agriculture, solar or utility corridors.</p></div>
    <div class="card"><h3>Storm Response</h3><p>Debris removal and road clearing wherever the storm hits.</p></div>
    <div class="card"><h3>Agency &amp; Prime Teaming</h3><p>Clearing and earthwork scopes on public projects, anywhere they're let.</p></div>
  </div>
</div></section>
<section class="section"><div class="wrap split">
  <div><h2>Why It Works</h2><ul class="checks">
    <li>Deep experience planning and running heavy site work</li>
    <li>Experience on Army Corps, agency and FEMA-reimbursed work</li>
    <li>One point of contact from bid to finish</li>
    <li>Every job documented on video</li>
  </ul></div>
  <div><h2>See Where We've Been</h2><p>Every place we've worked, backed by a real job video.</p>
  <a class="btn btn-green" href="{L('where-weve-worked/')}">Where We've Worked</a></div>
</div></section>
{cta_band(cur, "Wherever it is, let's talk.")}"""
    schema = [{"@context": "https://schema.org", "@type": "Service", "name": "Long-distance land clearing, earthwork and restoration project management",
               "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Place", "name": "Worldwide"}}]
    page(cur, f"Projects Anywhere | Land Clearing & Restoration Project Management | {BIZ['short']}",
         "Big land clearing, earthwork or restoration job far from home? We plan it, manage it and get it done — anywhere.", body, schema=schema, crumbs=trail)


def build_projects():
    cur = "projects/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Job Videos", cur)]
    svc_opts = "".join(f'<option value="{s["slug"]}">{s["name"]}</option>' for s in SERVICES)
    cty_opts = "".join(f'<option value="{k}">{r["name"]}</option>' for k, r in PLACES.items())
    yr_opts = ""
    cards = "".join(project_card(cur, p) for p in sorted(PROJECTS, key=lambda p: p["date"], reverse=True))
    body = page_hero(cur, trail, "Job Videos", "Every job we film: the date, the place, the equipment and the result. Filter by service, location or year.") + f"""
<section class="section"><div class="wrap">
  <h2 class="sr">All job videos</h2>
  <div class="filters">
    <label>Service<select data-filter="service"><option value="">All services</option>{svc_opts}</select></label>
    {f'<label>Location<select data-filter="region"><option value="">All locations</option>{cty_opts}</select></label>' if PLACES else ''}
    {f'<label>Year<select data-filter="year"><option value="">All years</option>{yr_opts}</select></label>' if yr_opts else ''}
  </div>
  <div class="grid g3" id="project-grid">{cards}
    <div class="empty-slot">Job #5 — next uploaded video becomes a page here</div>
    <div class="empty-slot">Job #6</div>
  </div>
  <p id="no-results" style="display:none" class="note">No jobs match those filters yet — more are being added.</p>
  <p class="mt small">Watch every job on our YouTube channel: {BIZ['youtube']}</p>
</div></section>{cta_band(cur)}"""
    page(cur, f"Job Videos | Land Clearing & Excavation Projects | {BIZ['short']}",
         "Real, dated land clearing, excavation and restoration jobs — with video and before/after photos.",
         body, crumbs=trail)

    for p in PROJECTS:
        cur = f"projects/{p['slug']}/"
        L = lambda x, cur=cur: rel(cur, x)  # noqa: E731
        pl = p["place"]
        sv = SVC[p["service"]]
        trail = [("Home", HOME), ("Job Videos", "projects/"), (p["title"], cur)]
        others = [o for o in PROJECTS if o["slug"] != p["slug"]][:3]
        body = page_hero(cur, trail, p["title"], p["summary"], ctas=False, eyebrow=f"{p['date_label']} · {place_label(pl)}") + f"""
<section class="section"><div class="wrap split">
  <div>
    {video('Job video', 'YouTube link for this job goes here', yt=p['youtube'], title=p['title'])}
    <h2 class="mt">The Job</h2>
    <h3>The challenge</h3><p>[[What the customer needed and what made this site difficult — XXX]]</p>
    <h3>How we did it</h3><p>[[Equipment, approach, permits and crew — XXX]]</p>
    <h3>The result</h3><p>[[Finished outcome, timeline and what came next for the property — XXX]]</p>
    <h2 class="mt">Before &amp; After</h2>
    {before_after()}
    <div class="grid g3 mt"><div class="photo">Job photo 1</div><div class="photo">Job photo 2</div><div class="photo">Job photo 3</div></div>
  </div>
  <div>
    <table class="facts">
      <tr><th>Date</th><td>{p['date_label']}</td></tr>
      <tr><th>Location</th><td>{(f'<a href="{L(place_path(pl))}">{pl["city"]}</a>, <a href="{L(region_path(pl))}">{pl["region_name"]}</a>') if pl else place_label(pl)}</td></tr>
      <tr><th>Service</th><td><a href="{L('services/' + sv['slug'] + '/')}">{sv['name']}</a></td></tr>
      <tr><th>Size</th><td>[[X acres / X linear ft]]</td></tr>
      <tr><th>Equipment</th><td>[[XXX]]</td></tr>
      <tr><th>Duration</th><td>[[X days]]</td></tr>
      <tr><th>Client type</th><td>[[Homeowner / GC / Agency]]</td></tr>
    </table>
    <div class="card mt"><h3>Need something like this?</h3><p>Tell us about your site and we'll get back to you fast.</p>
    <a class="btn btn-yellow" href="{L('request-a-bid/?service=' + sv['slug'])}">Request a Bid</a></div>
  </div>
</div></section>
<section class="section alt"><div class="wrap"><h2>More Jobs</h2>
<div class="grid g3">{''.join(project_card(cur, o) for o in others)}</div></div></section>
{cta_band(cur)}"""
        schema = [{
            "@context": "https://schema.org", "@type": "CreativeWork", "name": p["title"],
            "dateCreated": p["date"], "about": sv["name"], "creator": {"@id": ORG_ID},
        }]
        if pl:
            schema[0]["locationCreated"] = {"@type": "Place", "name": f"{pl['city']}, {pl['region_name']}"}
        if p["youtube"]:
            schema.append({"@context": "https://schema.org", "@type": "VideoObject", "name": p["title"],
                           "description": p["summary"], "uploadDate": p["date"],
                           "thumbnailUrl": f"https://i.ytimg.com/vi/{p['youtube']}/hqdefault.jpg",
                           "embedUrl": f"https://www.youtube.com/embed/{p['youtube']}"})
        page(cur, f"{p['title']} | Job Video | {BIZ['short']}",
             plain(f"{p['summary']} {place_label(pl)} — {p['date_label']}."), body, schema=schema, crumbs=trail)


def build_questions():
    cur = "questions/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Questions", cur)]
    cards = "".join(f'<a class="card" href="{L("questions/" + q["slug"] + "/")}"><h3>{q["q"]}</h3><p>{q["short"][:150]}…</p><span class="more">Read the answer</span></a>' for q in QUESTIONS)
    body = page_hero(cur, trail, "Questions &amp; Answers", "Straight answers about land clearing, permits, wetlands, timing and cost — from a crew that does this every day.") + f"""
<section class="section"><div class="wrap"><h2 class="sr">All questions</h2><div class="grid g2">{cards}
<div class="empty-slot">Next question + short video answer goes here</div></div></div></section>{cta_band(cur, "Have a question we didn't answer?")}"""
    page(cur, f"Land Clearing Questions & Answers | {BIZ['short']}",
         "Answers about land clearing costs, permits, wetlands, timelines and forestry mulching.", body, crumbs=trail)

    for q in QUESTIONS:
        cur = f"questions/{q['slug']}/"
        L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
        trail = [("Home", HOME), ("Questions", "questions/"), (q["q"], cur)]
        sections = "".join(f"<h2>{h}</h2>{b}" for h, b in q["body"])
        others = "".join(f'<li><a href="{L("questions/" + o["slug"] + "/")}">{o["q"]}</a></li>' for o in QUESTIONS if o["slug"] != q["slug"])
        sv = SVC[q["related_service"]]
        body = page_hero(cur, trail, q["q"], "", ctas=False) + f"""
<section class="section"><div class="wrap split">
  <div class="prose">
    <div class="answer-box"><b>Short answer</b>{q['short']}</div>
    {video('Short video answer', 'A 60-second YouTube Short answering this goes here')}
    {sections}
  </div>
  <div>
    <div class="card"><h3>Related service</h3><p>{sv['lead']}</p><a class="more" href="{L('services/' + sv['slug'] + '/')}">{sv['name']}</a></div>
    <div class="card mt"><h3>More questions</h3><ul class="checks">{others}</ul></div>
  </div>
</div></section>{cta_band(cur)}"""
        page(cur, f"{q['q']} | {BIZ['short']}", q["short"][:155], body,
             schema=[faq_schema([(q["q"], q["short"])])], crumbs=trail)


def build_about():
    cur = "about/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("About", cur)]
    body = page_hero(cur, trail, f"Clearing Land Since {BIZ['founded']}", f"Hard-won knowledge about land and water. Headquartered in [[City, State]] — working anywhere.", eyebrow="Our history") + f"""
<section class="section"><div class="wrap split">
  <div class="prose">
    <h2>Our Story</h2>
    <p>[[How the company started in {BIZ['founded']} — who, where and the first machine. XXX]]</p>
    <p>[[How it grew: the jobs, the equipment, the people. XXX]]</p>
    <p>[[What makes the crew different today. XXX]]</p>
    <h2>The People</h2>
    <div class="grid g2"><div class="card"><div class="photo">Photo — Matt</div><h3 class="mt">Matt [[Last name]]</h3><p>[[Title · years in the field]]</p></div>
    <div class="card"><div class="photo">Photo — Sam</div><h3 class="mt">Sam [[Last name]]</h3><p>[[Title · years in the field]]</p></div></div>
  </div>
  <div>
    <ol class="timeline">
      <li><b>{BIZ['founded']}</b>[[Company founded — XXX]]</li>
      <li><b>[[Year]]</b>[[First big project / first major machine — XXX]]</li>
      <li><b>[[Year]]</b>[[Army Corps / agency work begins — XXX]]</li>
      <li><b>[[Year]]</b>[[Hurricane response milestone — XXX]]</li>
      <li><b>2026</b>Our project library and new website go live.</li>
    </ol>
    <div class="photo mt">Old job photo from the '90s</div>
  </div>
</div></section>
{cta_band(cur)}"""
    page(cur, f"About Us | Land Clearing & Restoration Since {BIZ['founded']} | {BIZ['short']}",
         f"{BIZ['name']} has cleared, dug and restored land since {BIZ['founded']}.", body, crumbs=trail)


def build_credentials():
    cur = "credentials/"
    trail = [("Home", HOME), ("Credentials", cur)]
    rows = CREDS + [("State / federal contract numbers", "[[XXX]]"), ("W-9 · Certificate of insurance", "Available on request")]
    table = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows)
    body = page_hero(cur, trail, "Licenses, Insurance &amp; Credentials", "Everything an owner, engineer or contracting officer needs to check us out — in one place.") + f"""
<section class="section"><div class="wrap split">
  <div><table class="facts">{table}</table>
  <p class="small mt">Copies of certificates available on request.</p>
  <p><a class="btn btn-green" href="{rel(cur, 'capability-statement/')}">Capability Statement (print / PDF)</a></p></div>
  <div><div class="photo">License certificate image</div><div class="photo mt">Insurance certificate image</div></div>
</div></section>{cta_band(cur)}"""
    page(cur, f"Licenses & Credentials | {BIZ['short']}", "Licensed, insured and bonded land clearing and earthwork contractor with FEMA and Army Corps experience.", body, crumbs=trail)


def build_bid():
    cur = "request-a-bid/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Request a Bid", cur)]
    svc_boxes = "".join(f'<label><input type="checkbox" name="services" value="{s["slug"]}"> {s["name"]}</label>' for s in SERVICES) + \
        '<label><input type="checkbox" name="services" value="other"> Something else</label>'
    body = page_hero(cur, trail, "Request a Bid", "Tell us about the job. The more we know, the faster we can get you a real number.", ctas=False) + f"""
<section class="section"><div class="wrap split">
  <!-- FORM ENDPOINT: [[XXX]] — set action="..." (email handler / CRM) before going live -->
  <form class="form" id="bid-form" action="#" method="post" data-thanks="{L('thank-you/')}">
    <fieldset><legend>About you</legend>
      <div class="row"><div><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
      <div><label for="f-company">Company / agency <span class="hint">(if any)</span></label><input id="f-company" name="company" type="text" autocomplete="organization"></div></div>
      <div class="row"><div><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
      <div><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div></div>
      <div class="full"><label for="f-role">I am a…</label><select id="f-role" name="role" required>
        <option value="">Choose one</option>
        <option value="homeowner">Homeowner / lot owner</option>
        <option value="ranch">Ranch or farm owner</option>
        <option value="hoa">HOA / property manager</option>
        <option value="commercial">Commercial property owner</option>
        <option value="contractor">General contractor / builder</option>
        <option value="developer">Developer</option>
        <option value="engineer">Engineer / environmental consultant</option>
        <option value="government">Government agency / prime contractor</option>
        <option value="utility">Utility / solar</option>
      </select></div>
    </fieldset>
    <fieldset><legend>The job</legend>
      <div class="full"><label>What do you need? <span class="hint">(check all that apply)</span></label><div class="checks-grid">{svc_boxes}</div></div>
      <div class="full"><label for="f-loc">Where is the job? <span class="hint">(city, state or country — anywhere)</span></label><input id="f-loc" name="location" type="text" required></div>
      <div class="row"><div><label for="f-size">About how big?</label><select id="f-size" name="size">
        <option value="">Not sure</option><option value="under-1">Under 1 acre</option><option value="1-5">1–5 acres</option>
        <option value="5-20">5–20 acres</option><option value="20-100">20–100 acres</option><option value="100+">100+ acres</option>
        <option value="linear">Linear (miles of canal, ditch or road)</option></select></div>
      <div><label for="f-when">When?</label><select id="f-when" name="timeline">
        <option value="">Choose</option><option value="asap">As soon as possible</option><option value="1-3mo">1–3 months</option>
        <option value="3mo+">3+ months</option><option value="bid">Bidding / budgeting</option><option value="storm">Storm emergency</option></select></div></div>
      <div class="row"><div><label for="f-permit">Permits</label><select id="f-permit" name="permits">
        <option value="">Not sure</option><option value="have">We have permits</option><option value="in-progress">In progress</option><option value="need-help">Need help with permits</option></select></div>
      <div><label for="f-sol">Bid / solicitation # <span class="hint">(agencies)</span></label><input id="f-sol" name="solicitation" type="text"></div></div>
      <div class="full"><label for="f-desc">Tell us about it</label><textarea id="f-desc" name="description" placeholder="What's there now, what you want it to look like, access, anything else"></textarea></div>
      <div class="full"><label for="f-src">How did you find us?</label><select id="f-src" name="source">
        <option value="">Choose</option><option>Google search</option><option>Google Maps</option><option>YouTube</option>
        <option>AI assistant (ChatGPT, Gemini, etc.)</option><option>Referral</option><option>Truck / sign / QR code</option><option>Other</option></select></div>
    </fieldset>
    <div class="full sms-consent"><label><input type="checkbox" name="sms_consent" value="yes"> Yes, you may text me about my request. Message frequency varies. Message &amp; data rates may apply. Reply STOP to opt out, HELP for help. Consent is not required to get a bid. <a href="{L('text-terms/')}">Text Terms</a> · <a href="{L('privacy/')}">Privacy</a></label></div>
    <input type="hidden" name="lead_lane"><input type="hidden" name="landing_page"><input type="hidden" name="referrer">
    <button class="btn btn-yellow" type="submit" style="width:100%">Send My Request</button>
    <p class="small mt">We never sell your information. <a href="{L('privacy/')}">Privacy Policy</a> · <a href="{L('terms/')}">Terms</a></p>
  </form>
  <div>
    <h2 class="sr">Other ways to reach us</h2>
    <div class="card"><h3>Rather talk?</h3><p>Call <a href="{tel_href(cur)}">{BIZ['phone']}</a><br>{BIZ['hours']}</p></div>
    <div class="card mt"><h3>Agencies &amp; primes</h3><p>Send solicitations and scopes to {BIZ['email']}. See our <a href="{L('who-we-serve/government-agencies/')}">capability snapshot</a>.</p></div>
    <div class="card mt"><h3>Send photos or video</h3><p>[[Text photos to (XXX) XXX-XXXX]] — it's the fastest way to get an accurate price.</p></div>
  </div>
</div></section>"""
    page(cur, f"Request a Bid | {BIZ['short']}", "Request a bid for land clearing, excavation, site prep, restoration or storm debris removal — anywhere.", body, crumbs=trail)

    cur = "thank-you/"
    L = lambda p: rel(cur, p)  # noqa: E731
    body = f"""<section class="page-hero"><div class="wrap"><h1>Thank You — We've Got It</h1>
<p class="lead">Your request is in. We'll be in touch [[within one business day]]. For anything urgent, call {BIZ['phone']}.</p>
<div class="ctas"><a class="btn btn-yellow" href="{L('projects/')}">Watch Our Work</a><a class="btn btn-ghost" href="{L(HOME)}">Back to Home</a></div></div></section>"""
    page(cur, f"Thank You | {BIZ['short']}", "Thanks for your request.", body, noindex=True)


def build_reviews():
    cur = "reviews/"
    trail = [("Home", HOME), ("Reviews", cur)]
    body = page_hero(cur, trail, "Worked With Us? Tell Others.", f"Word of mouth built this company. A quick Google review helps the next customer find us.", ctas=False) + f"""
<section class="section"><div class="wrap split">
  <div>
    <a class="btn btn-yellow" href="#">[[Leave a Google Review — link XXX]]</a>
    <h2 class="mt">What Customers Say</h2>
    <div class="grid g2">
      <div class="card"><p>“[[Customer review text XXX]]”</p><b>[[Name · City]]</b></div>
      <div class="card"><p>“[[Customer review text XXX]]”</p><b>[[Name · City]]</b></div>
      <div class="card"><p>“[[Customer review text XXX]]”</p><b>[[Name · City]]</b></div>
      <div class="card"><p>“[[Customer review text XXX]]”</p><b>[[Name · City]]</b></div>
    </div>
  </div>
  <div class="card"><h3>It takes one minute</h3><ol><li>Tap the button</li><li>Pick the stars</li><li>Say what we did and where</li></ol>
  <p class="small">Mentioning the job and the city ("cleared 3 acres for a new home") helps the most.</p></div>
</div></section>"""
    page(cur, f"Reviews | {BIZ['short']}", f"Reviews of {BIZ['name']}.", body, crumbs=trail)


def build_legal():
    fill = {"name": BIZ["name"], "address": BIZ["address"], "city_state": BIZ["city_state"],
            "phone": BIZ["phone"], "email": BIZ["email"], "audit_date": AUDIT_DATE}
    others_all = [(d["slug"], d["title"]) for d in LEGAL]
    for d in LEGAL:
        cur = d["slug"] + "/"
        L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
        links = dict(fill, privacy=L("privacy/"), text_terms=L("text-terms/"), credentials=L("credentials/"),
                     capability=L("capability-statement/"))
        trail = [("Home", HOME), (d["title"], cur)]
        toc = "".join(f'<li><a href="#s{i}">{h}</a></li>' for i, (h, _) in enumerate(d["sections"], 1))
        secs = "".join(f'<h2 id="s{i}">{h}</h2>{t.format(**links)}' for i, (h, t) in enumerate(d["sections"], 1))
        others = "".join(f'<li><a href="{L(sl + "/")}">{t}</a></li>' for sl, t in others_all if sl != d["slug"])
        body = page_hero(cur, trail, d["title"], d["lead"], ctas=False) + f"""
<section class="section"><div class="wrap split legal">
  <article class="prose">
    <p class="small">Effective: {EFFECTIVE}</p>
    {secs}
    <p class="small mt">Effective: {EFFECTIVE} · {BIZ['name']}</p>
  </article>
  <div class="legal-side">
    <div class="card"><h3>On this page</h3><ul class="checks">{toc}</ul></div>
    <div class="card mt"><h3>Policies</h3><ul class="checks">{others}</ul></div>
  </div>
</div></section>"""
        page(cur, f"{d['title']} | {BIZ['short']}", f"{d['title']} for {BIZ['name']}. {d['lead']}", body, crumbs=trail)


def build_plan():
    """Client-facing plan page for Matt & Sam (hidden from search)."""
    cur = "plan/"
    L = lambda p: rel(cur, p)  # noqa: E731
    n_pages_hint = "{PAGE_COUNT}"
    body = f"""
<section class="hero"><div class="wrap hero-grid">
  <div><span class="eyebrow">Prepared for Matt &amp; Sam</span>
  <h1>Your New Home Online</h1>
  <p class="lead">Great work — now built so the people who need it can find it. Here's what's built, how it works, and what comes next.</p>
  <div class="ctas"><a class="btn btn-yellow" href="{L('plan/checklist/')}">Open the Service Checklist</a><a class="btn btn-ghost" href="{L(HOME)}">Tour the Website</a><a class="btn btn-ghost" href="{L('capabilities/')}">Capability Map</a></div></div>
  <div class="logo-plate"><img src="{L('assets/img/everglades-logo.webp')}" alt="" width="1400" height="632"></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>What It Does For You</h2></div>
  <div class="grid g3">
    <div class="card lane-card"><h3>Gets You Found</h3><p>On Google, Google Maps, YouTube, and the AI assistants people now ask for recommendations. Every service, every county and every city gets its own page.</p></div>
    <div class="card lane-card"><h3>Earns Trust Fast</h3><p>Your real job videos, before-and-after photos, licenses, insurance, FEMA and Army Corps work — all in plain view.</p></div>
    <div class="card lane-card"><h3>Makes the Phone Ring</h3><p>Call buttons on every page, and a bid form that asks the right questions — so the big jobs get to you first.</p></div>
  </div>
</div></section>

<section class="section alt"><div class="wrap split">
  <div>
    <h2>Your Videos Do the Heavy Lifting</h2>
    <p>Every job you film becomes its own page — with the date, the city, the equipment and the before-and-after. Those pages show up in search, and they prove you do the work. A hundred real, dated jobs across dozens of cities is something almost nobody in your trade has.</p>
    <p>You've already got the footage. We'll turn it into your biggest advantage.</p>
    <a class="btn btn-green" href="{L('projects/' + PROJECTS[0]['slug'] + '/')}">See a sample job page</a>
  </div>
  <div>{video('Your job video here', 'Sample — shows where each job video plays')}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>What's Built So Far</h2><p>This preview is the full skeleton. The tagged spots are where your real details go.</p></div>
  <div class="grid g4">
    <a class="card" href="{L(HOME)}"><h3>Home</h3><p>Your front page with video, before/after and credentials.</p></a>
    <a class="card" href="{L('services/')}"><h3>Services</h3><p>A full page for each type of work.</p></a>
    <a class="card" href="{L('where-weve-worked/')}"><h3>Where We've Worked</h3><p>Built only from your real jobs — every video puts a new place on the map.</p></a>
    <a class="card" href="{L('projects-anywhere/')}"><h3>Projects Anywhere</h3><p>Big job far from home? Matt plans it, the right crew does it.</p></a>
    <a class="card" href="{L('projects/')}"><h3>Job Videos</h3><p>Filterable job videos — {len(PROJECTS)} samples built from your example list.</p></a>
    <a class="card" href="{L('who-we-serve/government-agencies/')}"><h3>Government Page</h3><p>Capability snapshot for agencies and prime contractors.</p></a>
    <a class="card" href="{L('questions/')}"><h3>Questions</h3><p>Straight answers on cost, permits and wetlands.</p></a>
    <a class="card" href="{L('request-a-bid/')}"><h3>Request a Bid</h3><p>The form every inquiry comes through.</p></a>
    <a class="card" href="{L('about/')}"><h3>About</h3><p>Your history, your people, your numbers.</p></a>
    <a class="card lane-card" href="{L('capabilities/')}"><h3>Capability Map</h3><p>Every capability, each with its own page and the searches it's built to win.</p></a>
    <a class="card lane-card" href="{L('plan/checklist/')}"><h3>Service Checklist</h3><p>Tap through every service: we do it, we sub it, or not for us. Your answers decide what goes live.</p></a>
    <a class="card" href="{L(DOOR)}"><h3>Front Door</h3><p>Your digital business card: call, email, website, every license, QR code.</p></a>
    <a class="card" href="{L('capability-statement/')}"><h3>Capability Statement</h3><p>The one page every procurement office asks for, ready to print.</p></a>
    <a class="card" href="{L('credentials/')}"><h3>Credentials</h3><p>Every license and registration in one place.</p></a>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>How Buyers Find Each Service</h2><p>Behind every capability page is a plan for the searches, videos, AI questions and bid keywords it's built to win. Here's one example — every category has its own.</p></div>
  <h3>{CAT['land-clearing-vegetation-management']['name']}</h3>
  {cat_find(CAT['land-clearing-vegetation-management'])}
</div></section>

<section class="section dark"><div class="wrap">
  <div class="section-head"><h2>How It Grows</h2><p>No boundaries. Wherever you've worked — and wherever you work next — shows up on its own.</p></div>
  <div class="grid g4">
    <div class="stat"><b>Every job</b><span>gets its own page with video, date and place</span></div>
    <div class="stat"><b>Every place</b><span>you've worked goes on the map automatically</span></div>
    <div class="stat"><b>Every week</b><span>new videos, new pages, more ways to be found</span></div>
    <div class="stat"><b>Anywhere</b><span>Projects Anywhere brings in the big jobs far from home</span></div>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    <h2>What We Need From You</h2>
    <ul class="checks">
      <li>Domain name (your web address)</li>
      <li>YouTube channel in the company name — and your job videos uploaded</li>
      <li>A simple list for each video: job name, date, city</li>
      <li>Google Business Profile set up and verified</li>
      <li>Job photos, especially before-and-afters (old ones too)</li>
      <li>Founding year, phone, email, address, hours</li>
      <li>Every license and registration: contractor, SAM.gov UEI / CAGE, NAICS, FEMA, Army Corps, FDOT, bonding, insurance, certifications</li>
      <li>Past government and agency projects for the capability statement</li>
      <li>Your equipment list</li>
      <li>A few past customers who'd leave a Google review</li>
    </ul>
  </div>
  <div>
    <h2>Next Steps</h2>
    <ol class="timeline">
      <li><b>1</b>Look it over — tell us what you like and what to change.</li>
      <li><b>2</b>Send the details and videos above.</li>
      <li><b>3</b>We fill in every yellow spot and connect your videos.</li>
      <li><b>4</b>Point your domain here and go live.</li>
    </ol>
  </div>
</div></section>"""
    page(cur, f"Your Website Plan | {BIZ['short']}", "Website plan preview.", body, noindex=True)


def build_capability():
    """One-page capability statement, print / save as PDF from the browser."""
    cur = "capability-statement/"
    L = lambda p: rel(cur, p)  # noqa: E731
    style = """<style>
body{background:#e9e5da}
.cap{max-width:8.5in;margin:24px auto;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.15)}
.cap-head{background:var(--green-deep);color:#fff;display:grid;grid-template-columns:1fr auto;gap:18px;align-items:center;padding:22px 28px}
.cap-head img{max-width:300px}.cap-head .logo-plate{padding:10px 14px;max-width:320px}
.cap-head h1{color:#fff;font-size:1.6rem;margin:0}
.cap-head p{margin:2px 0;color:#d7eadb;font-size:.9rem;text-align:right}
.cap-body{display:grid;grid-template-columns:1fr 1fr;gap:22px;padding:22px 28px}
.cap h2{font-size:1rem;color:var(--green);border-bottom:2px solid var(--green);padding-bottom:4px;margin:14px 0 8px;letter-spacing:.05em}
.cap h2:first-child{margin-top:0}
.cap ul{margin:0;padding-left:1.1em;font-size:.9rem}
.cap li{margin-bottom:3px}
.cap p{font-size:.9rem;margin:0 0 6px}
.cap .creds{grid-template-columns:1fr 1fr;gap:5px}
.cap .creds div{padding:5px 8px}
.cap .creds dt{font-size:.6rem;letter-spacing:.03em}
.cap .creds dd{font-size:.82rem}
.cap .creds div{background:#f6f3ea;border-color:#e2dccb}
.cap .creds dt{color:var(--ink-soft)}
.cap .creds dd{color:var(--ink)}
.cap-foot{background:var(--sand);padding:12px 28px;font-size:.85rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.printbar{text-align:center;margin:18px 0 30px}
@media screen and (max-width:760px){.cap-head,.cap-body{grid-template-columns:1fr}.cap-head p{text-align:left}}
@media print{body{background:#fff}.printbar{display:none}.cap{box-shadow:none;margin:0;max-width:none}@page{size:letter;margin:.35in}
.cap-head{padding:12px 18px}.cap-head img{max-width:230px}.cap-head h1{font-size:1.5rem}.cap-head p{font-size:.8rem}
.cap-body{padding:12px 18px;gap:16px}.cap h2{margin:8px 0 5px;font-size:.88rem}.cap p,.cap ul{font-size:.76rem}.cap li{margin-bottom:1px}
.cap .creds div{padding:3px 7px}.cap .creds dd{font-size:.74rem}.cap .creds dt{font-size:.55rem}.cap-foot{padding:7px 18px;font-size:.75rem}
.cap-head,.cap-foot,.cap .creds div{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style>"""
    comp = "".join(f"<li>{x['name']}</li>" for x in SERVICES) + "<li>Projects Anywhere: long-distance planning and management</li>"
    body = f"""
<main id="main"><article class="cap">
  <header class="cap-head">
    <div class="logo-plate"><img src="{L('assets/img/everglades-logo.webp')}" alt="{esc(BIZ['name'])}" width="1400" height="632"></div>
    <div><h1>Capability Statement</h1><p>{BIZ['phone']}</p><p>{BIZ['email']}</p><p>Website: [[www.XXX.com]]</p></div>
  </header>
  <div class="cap-body">
    <div>
      <h2>Company Overview</h2>
      <p>{BIZ['name']} has delivered land clearing, excavation and environmental restoration since {BIZ['founded']}. We self-perform with our own crews and equipment, support agencies and prime contractors, and take on projects in any state or country. [[One-sentence differentiator XXX]]</p>
      <h2>Core Competencies</h2><ul>{comp}</ul>
      <h2>Differentiators</h2><ul>
        <li>Heavy site work on wet, difficult ground since {BIZ['founded']}</li>
        <li>Army Corps, agency and FEMA-reimbursed project experience</li>
        <li>Own equipment fleet: [[XX machines — key types XXX]]</li>
        <li>Every job documented on video</li></ul>
      <h2>Past Performance</h2><ul>
        <li>[[Project · Agency / prime · Year · Scope · Value]]</li>
        <li>[[Project · Agency / prime · Year · Scope · Value]]</li>
        <li>[[Project · Agency / prime · Year · Scope · Value]]</li></ul>
    </div>
    <div>
      <h2>Company Data</h2>{creds_grid()}
    </div>
  </div>
  <footer class="cap-foot"><span>Headquartered in [[City, State]] · Working anywhere</span><span>W-9 and COI on request</span><span class="cap-credit">{credit(cur, light_bg=True)}</span></footer>
</article>
<div class="printbar"><button class="btn btn-yellow" onclick="window.print()">Print / Save as PDF</button>
<a class="btn btn-outline" href="{L(DOOR)}">Back</a></div>
</main>"""
    page(cur, f"Capability Statement | {BIZ['short']}", f"Capability statement for {BIZ['name']}.",
         body, chrome=False, extra_head=style, noindex=True)


# ---------------------------------------------------------------- capability hub
STATUS_LABEL = {"EXISTING": "Planned", "EXPAND": "Expanded", "NEW": "New", "ADDED": "Added in review"}


def cap_path(c, svc=None):
    return f"capabilities/{c['slug']}/" + (slugify(svc) + "/" if svc else "")


def sec_cats(sec):
    return [c for c in CATEGORIES if c["sec"] == sec]


def svc_grid(cur, c):
    L = lambda p: rel(cur, p)  # noqa: E731
    items = []
    for svc in c["services"]:
        path = cap_path(c, svc)
        if (c["slug"], svc) in EXAMPLES:
            items.append(f'<li class="svc live"><a href="{L(path)}">{svc}</a></li>')
        else:
            items.append(f'<li class="svc"><span>{svc}</span></li>')
    return '<ul class="svc-grid">' + "".join(items) + "</ul>"


def find_panel(name, google, bids, yt, ai):
    g = "".join(f"<li>“{q}”</li>" for q in google)
    b = "".join(f"<li>“{q}”</li>" for q in bids) + "<li>NAICS [[XXX]]</li>"
    y = "".join(f"<li>{q}</li>" for q in yt)
    return f"""<div class="find-grid">
  <div class="find"><b>Google &amp; Maps</b><ul>{g}</ul></div>
  <div class="find"><b>YouTube</b><ul>{y}</ul></div>
  <div class="find"><b>AI assistants</b><ul><li>{ai}</li></ul></div>
  <div class="find"><b>Bid portals &amp; procurement</b><ul>{b}</ul></div>
</div>
<p class="small mt">Every {name.lower()} job video gets its own page that links back here, so this page grows stronger with every job.</p>"""


def cat_find(c):
    first = c["services"][0]
    return find_panel(c["name"], c["find"] + [f"{first.lower()} near me"], c["bid"],
                      [f"“{first} — Before &amp; After”", f"“How we handle {c['services'][1].lower()}”"],
                      f"“Who can handle {first.lower()} for a [[project type]]?”")


def sensitive_note():
    return ('<div class="note"><b>Delivered with qualified partners.</b> On high-hazard projects we provide the earthwork, '
            'hauling, containment and restoration — working under the remediation prime and with licensed specialists. '
            'Crew training and certifications: [[HAZWOPER / OSHA / other XXX]].</div>')


def build_capabilities():
    cur = "capabilities/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Capability Map", cur)]
    blocks = ""
    for i, (sk, sname, sdesc) in enumerate(SECTIONS):
        cards = "".join(f'<a class="card" href="{L(cap_path(c))}"><h3>{c["name"]}</h3><p>{c["blurb"]}</p>'
                        f'<span class="more">View services</span></a>' for c in sec_cats(sk))
        blocks += f"""<section class="section{' alt' if i % 2 else ''}" id="{sk}"><div class="wrap">
  <div class="section-head"><h2><a href="{L('capabilities/' + sk + '/')}" style="text-decoration:none;color:inherit">{sname}</a></h2><p>{sdesc}</p></div>
  <div class="grid g3">{cards}</div></div></section>"""
    jump = "".join(f'<li><a href="#{sk}">{sname}</a></li>' for sk, sname, _ in SECTIONS)
    body = page_hero(cur, trail, "The Full Capability Map", "From a single lot to Superfund-scale earthwork. One accountable team, our own crews and a nationwide partner network.", eyebrow="Any state · Any country") + f"""
<section class="section jumpbar"><div class="wrap"><ul class="pill-list">{jump}</ul></div></section>
{blocks}
{cta_band(cur, "Don't see it? Ask.", "If it involves land, water or heavy equipment, we do it, team it or know who does.")}"""
    page(cur, f"Capabilities | Land, Water & Site Work | {BIZ['short']}",
         f"Land clearing, earthwork, wetlands, stormwater, dredging, remediation earthwork, energy sites, disaster recovery and more.",
         body, crumbs=trail)

    for sk, sname, sdesc in SECTIONS:
        cur = f"capabilities/{sk}/"
        L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
        trail = [("Home", HOME), ("Capability Map", "capabilities/"), (sname, cur)]
        cats = sec_cats(sk)
        cards = "".join(f'<a class="card" href="{L(cap_path(c))}"><h3>{c["name"]}</h3><p>{c["blurb"]}</p>'
                        f'<p class="small">{", ".join(c["services"][:5])}…</p><span class="more">View services</span></a>' for c in cats)
        others = "".join(f'<li><a href="{L("capabilities/" + k + "/")}">{n}</a></li>' for k, n, _ in SECTIONS if k != sk)
        body = page_hero(cur, trail, sname, sdesc) + f"""
<section class="section"><div class="wrap"><h2 class="sr">Categories in {sname}</h2><div class="grid g3">{cards}</div></div></section>
<section class="section alt"><div class="wrap"><h2>Other Areas of Expertise</h2><ul class="pill-list">{others}</ul></div></section>
{cta_band(cur)}"""
        page(cur, f"{sname} | Capabilities | {BIZ['short']}", f"{sname}: {sdesc}", body, crumbs=trail)

    for c in CATEGORIES:
        cur = cap_path(c)
        L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
        sname = dict((k, n) for k, n, _ in SECTIONS)[c["sec"]]
        trail = [("Home", HOME), ("Capability Map", "capabilities/"), (sname, f"capabilities/{c['sec']}/"), (c["name"], cur)]
        related = c.get("related")
        rel_card = (f'<div class="card mt"><h3>In depth</h3><p>{SVC[related]["lead"]}</p>'
                    f'<a class="more" href="{L("services/" + related + "/")}">{SVC[related]["name"]}</a></div>') if related else ""
        siblings = "".join(f'<li><a href="{L(cap_path(o))}">{o["name"]}</a></li>' for o in sec_cats(c["sec"]) if o is not c)
        body = page_hero(cur, trail, c["name"], c["blurb"], eyebrow=sname) + f"""
<section class="section"><div class="wrap split">
  <div>
    <h2>Services</h2>
    {svc_grid(cur, c)}
    {sensitive_note() if c.get('sensitive') else ''}
  </div>
  <div>
    {video(c['name'] + ' video', 'Job video for this category goes here')}
    {rel_card}
    <div class="card mt"><h3>Have a job like this?</h3><p>Any size, any state, any country.</p>
    <a class="btn btn-yellow" href="{L('request-a-bid/')}">Request a Bid</a></div>
  </div>
</div></section>
<section class="section"><div class="wrap split">
  <div><h2>Before &amp; After</h2>{before_after()}</div>
  <div><h3>More in {sname}</h3><ul class="pill-list">{siblings}</ul>
  <p class="mt"><a href="{L('capabilities/')}">Full capability map →</a></p></div>
</div></section>
{cta_band(cur)}"""
        schema = [{"@context": "https://schema.org", "@type": "Service", "name": c["name"], "serviceType": c["name"],
                   "provider": {"@id": ORG_ID}, "description": c["blurb"],
                   "hasOfferCatalog": {"@type": "OfferCatalog", "name": c["name"],
                                       "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": x}} for x in c["services"]]}}]
        page(cur, f"{c['name']} | {BIZ['short']}", f"{c['blurb']} {', '.join(c['services'][:6])} and more.",
             body, schema=schema, crumbs=trail)

    for (cslug, svc), desc in EXAMPLES.items():
        c = CAT[cslug]
        cur = cap_path(c, svc)
        L = lambda p, cur=cur: rel(cur, p)  # noqa: E731
        sname = dict((k, n) for k, n, _ in SECTIONS)[c["sec"]]
        trail = [("Home", HOME), ("Capability Map", "capabilities/"), (c["name"], cap_path(c)), (svc, cur)]
        siblings = "".join(f'<li><a href="{L(cap_path(c, o))}">{o}</a></li>' if (cslug, o) in EXAMPLES
                           else f'<li><span>{o}</span></li>' for o in c["services"] if o != svc)
        low = svc.lower()
        body = page_hero(cur, trail, svc, desc, eyebrow=c["name"]) + f"""
<section class="section"><div class="wrap split">
  <div class="prose">
    <h2>What's Included</h2>
    <ul class="checks"><li>[[Scope item XXX]]</li><li>[[Scope item XXX]]</li><li>[[Scope item XXX]]</li><li>[[Scope item XXX]]</li></ul>
    <h2>How We Do It</h2>
    <ol class="timeline">
      <li><b>1 · Review</b>[[Plans, permits and site conditions XXX]]</li>
      <li><b>2 · Mobilize</b>[[Equipment and crew XXX]]</li>
      <li><b>3 · Build</b>[[Method and quality checks XXX]]</li>
      <li><b>4 · Document</b>Video and photos from start to finish.</li>
    </ol>
  </div>
  <div>{video(svc + ' video', 'Job video for this service goes here')}
  <table class="facts mt"><tr><th>Typical equipment</th><td>[[XXX]]</td></tr><tr><th>Typical timeline</th><td>[[XXX]]</td></tr>
  <tr><th>Self-perform or team</th><td>[[Self-perform / with partners]]</td></tr></table>
  <div class="card mt"><h3>Need {low}?</h3><p>Anywhere in the country — tell us about it.</p>
  <a class="btn btn-yellow" href="{L('request-a-bid/')}">Request a Bid</a></div></div>
</div></section>
<section class="section"><div class="wrap split">
  <div><h2>Before &amp; After</h2>{before_after()}</div>
  <div><h3>Also in {c['name']}</h3><ul class="pill-list">{siblings}</ul></div>
</div></section>
{cta_band(cur)}"""
        schema = [{"@context": "https://schema.org", "@type": "Service", "name": svc, "serviceType": svc,
                   "provider": {"@id": ORG_ID}, "description": desc, "category": c["name"]}]
        page(cur, f"{svc} | {c['name']} | {BIZ['short']}", desc, body, schema=schema, crumbs=trail)


def build_checklist():
    """Matt's yes / sub / no checklist. Choices are saved on his device; he can print or send them."""
    cur = "plan/checklist/"
    L = lambda p: rel(cur, p)  # noqa: E731
    total = 0
    blocks = ""
    for sk, sname, _ in SECTIONS:
        cats = ""
        for c in sec_cats(sk):
            rows = ""
            for svc in c["services"] + c.get("private", []):
                total += 1
                priv = ' <small class="priv">checklist only</small>' if svc in c.get("private", []) else ""
                rows += (f'<div class="ck-row" data-key="{c["slug"]}::{esc(svc)}"><span class="ck-name">{svc}{priv}</span>'
                         f'<span class="ck-opts"><button type="button" data-v="do">We do it</button>'
                         f'<button type="button" data-v="sub">Sub / team</button><button type="button" data-v="no">Not for us</button></span></div>')
            cats += f"""<div class="ck-cat" data-cat="{c['slug']}">
  <div class="ck-head"><div><span class="ck-num">{c['n']:02d}</span> <b>{c['name']}</b> <span class="ck-status s-{c['status'].lower()}">{STATUS_LABEL[c['status']]}</span>
  <a class="small" href="{L(cap_path(c))}">view page →</a></div>
  <span class="ck-all">All: <button type="button" data-all="do">Do</button><button type="button" data-all="sub">Sub</button><button type="button" data-all="no">No</button></span></div>
  {rows}</div>"""
        blocks += f'<section class="ck-sec"><h2>{sname}</h2>{cats}</section>'
    body = f"""
<section class="page-hero"><div class="wrap">
  <span class="eyebrow">For Matt &amp; Sam</span><h1>Service Checklist</h1>
  <p class="lead">Tap one choice for each service: <b>We do it</b>, <b>Sub / team</b> (we take it and bring in a partner), or <b>Not for us</b>. Your choices save on this device, so you can stop and come back. When you're done, tap <b>Send to us</b> — your answers come straight to us.</p>
</div></section>
<div class="ck-bar"><div class="wrap">
  <span>✅ <b id="c-do">0</b> do</span><span>🤝 <b id="c-sub">0</b> sub</span><span>❌ <b id="c-no">0</b> no</span><span>⬜ <b id="c-open">{total}</b> open</span>
  <span class="ck-actions"><button type="button" class="btn btn-yellow btn-sm" data-send>Send to us</button>
  <button type="button" class="btn btn-outline btn-sm" id="ck-send">Email</button>
  <button type="button" class="btn btn-outline btn-sm" onclick="window.print()">Print</button>
  <button type="button" class="btn btn-outline btn-sm" id="ck-reset">Reset</button></span>
</div></div>
<section class="section"><div class="wrap">{blocks}
<div class="ck-done" id="ck-done">
  <h2>All Done? Send It.</h2>
  <p>Your answers go straight to us. You can send again later if you change anything.</p>
  <label for="ck-name">Your name</label>
  <input type="text" id="ck-name" autocomplete="name" placeholder="Matt">
  <input type="text" name="website" id="ck-hp" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
  <div class="ck-done-btns"><button type="button" class="btn btn-yellow" data-send>Send to us</button>
  <button type="button" class="btn btn-outline" id="ck-copy">Copy answers</button></div>
  <p class="ck-msg" id="ck-msg" role="status"></p>
</div>
<p class="small">Status tags: <span class="ck-status s-existing">Planned</span> already in the plan · <span class="ck-status s-expand">Expanded</span> broadened · <span class="ck-status s-new">New</span> proposed · <span class="ck-status s-added">Added in review</span> gaps we filled. Items marked <small class="priv">checklist only</small> stay off the public site.</p>
</div></section>
<script>
(function () {{
  var KEY = "eg-service-checklist", state = {{}};
  try {{ state = JSON.parse(localStorage.getItem(KEY) || "{{}}"); }} catch (e) {{}}
  var rows = document.querySelectorAll(".ck-row");
  function save() {{ try {{ localStorage.setItem(KEY, JSON.stringify(state)); }} catch (e) {{}} }}
  function paint() {{
    var n = {{do: 0, sub: 0, no: 0}};
    rows.forEach(function (r) {{
      var v = state[r.getAttribute("data-key")];
      r.setAttribute("data-v", v || "");
      r.querySelectorAll("[data-v]").forEach(function (b) {{ b.setAttribute("aria-pressed", b.getAttribute("data-v") === v ? "true" : "false"); }});
      if (v) n[v]++;
    }});
    document.getElementById("c-do").textContent = n.do;
    document.getElementById("c-sub").textContent = n.sub;
    document.getElementById("c-no").textContent = n.no;
    document.getElementById("c-open").textContent = rows.length - n.do - n.sub - n.no;
  }}
  rows.forEach(function (r) {{
    r.querySelectorAll("[data-v]").forEach(function (b) {{
      b.addEventListener("click", function () {{
        var k = r.getAttribute("data-key"), v = b.getAttribute("data-v");
        if (state[k] === v) delete state[k]; else state[k] = v;
        save(); paint();
      }});
    }});
  }});
  document.querySelectorAll(".ck-cat").forEach(function (c) {{
    c.querySelectorAll("[data-all]").forEach(function (b) {{
      b.addEventListener("click", function () {{
        c.querySelectorAll(".ck-row").forEach(function (r) {{ state[r.getAttribute("data-key")] = b.getAttribute("data-all"); }});
        save(); paint();
      }});
    }});
  }});
  function summary() {{
    var label = {{do: "WE DO IT", sub: "SUB / TEAM", no: "NOT FOR US"}}, out = ["Everglades service checklist", ""];
    document.querySelectorAll(".ck-cat").forEach(function (c) {{
      out.push(c.querySelector(".ck-head b").textContent);
      c.querySelectorAll(".ck-row").forEach(function (r) {{
        var v = state[r.getAttribute("data-key")];
        out.push("  - " + r.querySelector(".ck-name").childNodes[0].textContent.trim() + ": " + (v ? label[v] : "(open)"));
      }});
      out.push("");
    }});
    return out.join("\\n");
  }}
  document.getElementById("ck-copy").addEventListener("click", function () {{
    var t = summary();
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(function () {{ alert("Copied. Paste it into a text or email."); }});
  }});
  function counts() {{
    var n = {{}};
    ["do", "sub", "no", "open"].forEach(function (k) {{ n[k] = +document.getElementById("c-" + k).textContent; }});
    return n;
  }}
  var msg = document.getElementById("ck-msg"), nameBox = document.getElementById("ck-name");
  try {{ nameBox.value = localStorage.getItem(KEY + "-name") || ""; }} catch (e) {{}}
  nameBox.addEventListener("input", function () {{ try {{ localStorage.setItem(KEY + "-name", nameBox.value); }} catch (e) {{}} }});
  function say(text, ok) {{ msg.textContent = text; msg.className = "ck-msg " + (ok ? "good" : "bad"); }}
  document.querySelectorAll("[data-send]").forEach(function (btn) {{
    btn.addEventListener("click", function () {{
      var c = counts();
      if (c.open === rows.length && !confirm("Nothing is marked yet. Send anyway?")) return;
      document.getElementById("ck-done").scrollIntoView({{behavior: "smooth", block: "center"}});
      say("Sending…", true);
      fetch("{L('send-checklist.php')}", {{
        method: "POST",
        headers: {{"Content-Type": "application/json"}},
        body: JSON.stringify({{name: nameBox.value, summary: summary(), counts: c, website: document.getElementById("ck-hp").value}})
      }}).then(function (r) {{ return r.json(); }}).then(function (d) {{
        if (d && d.ok) say("Sent — thank you! We have your answers.", true);
        else throw new Error("not ok");
      }}).catch(function () {{
        say("Couldn't send from here. Tap Email instead — it opens your email with the answers ready.", false);
      }});
    }});
  }});
  document.getElementById("ck-send").addEventListener("click", function () {{
    var t = summary(), to = "{CHECKLIST_TO}", subj = encodeURIComponent("Everglades service checklist" + (nameBox.value ? " from " + nameBox.value : ""));
    if (t.length > 1800) {{
      if (navigator.clipboard) navigator.clipboard.writeText(t);
      alert("Your full answers are copied. Paste them into the email that opens next.");
      location.href = "mailto:" + to + "?subject=" + subj + "&body=" + encodeURIComponent("(Paste my answers here)\\n\\n");
    }} else {{
      location.href = "mailto:" + to + "?subject=" + subj + "&body=" + encodeURIComponent(t);
    }}
  }});
  document.getElementById("ck-reset").addEventListener("click", function () {{
    if (confirm("Clear all choices?")) {{ state = {{}}; save(); paint(); }}
  }});
  paint();
}})();
</script>"""
    page(cur, f"Service Checklist | {BIZ['short']}", "Service checklist.", body, noindex=True)


def build_qr_sheet():
    cur = "qr/"
    L = lambda p: rel(cur, p)  # noqa: E731
    style = """<style>
body{background:#fff}
.sheet{max-width:780px;margin:0 auto;padding:40px 24px;text-align:center}
.sheet img{max-width:560px;margin:0 auto 18px;width:100%}
.sheet h1{font-size:2.4rem;margin-bottom:.2em}
.sheet .qr{width:320px;height:320px;margin:24px auto 8px;border:10px solid var(--green-deep);border-radius:18px;padding:8px;background:#fff}
.sheet .qr svg{width:100%;height:100%}
.sheet .url{font-weight:700;color:var(--green);word-break:break-all}
.sheet .tag{font-family:var(--head);font-size:1.4rem;text-transform:uppercase;color:var(--green-deep);margin-top:24px}
.printbar{margin-top:28px}
@media print{.printbar{display:none}.sheet{padding:0}@page{size:letter;margin:.6in}}
</style>"""
    body = f"""<main class="sheet" id="main">
  <img src="{L('assets/img/everglades-logo.png')}" alt="{esc(BIZ['name'])}" width="1400" height="632">
  <h1>See Our New Website</h1>
  <p>Point your phone's camera at the code.</p>
  <div class="qr" id="qr-sheet" data-qr="/" role="img" aria-label="QR code to the website"></div>
  <p class="url" data-qr-url="qr-sheet"></p>
  <p class="tag">Land Clearing · Excavation · Restoration</p>
  <p>{BIZ['phone']}</p>
  <div class="printbar"><button class="btn btn-yellow" onclick="window.print()">Print this page</button>
  <a class="btn btn-outline" href="{L(DOOR)}">Back</a></div>
</main>
<footer class="credit-row">{credit(cur, light_bg=True)}</footer>"""
    page(cur, f"QR Code | {BIZ['short']}", "Printable QR code.", body, chrome=False, extra_head=style, noindex=True)


def build_404():
    # Served from any depth, so it uses root-absolute paths.
    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page Not Found | {BIZ['short']}</title><meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css"><link rel="icon" href="/assets/img/icon-32.png"></head>
<body><main id="main"><section class="hero" style="min-height:100vh;display:flex;align-items:center"><div class="wrap center">
<img src="/assets/img/everglades-logo-640.webp" alt="{esc(BIZ['name'])}" style="margin:0 auto 24px;max-width:420px">
<h1>This Page Got Cleared</h1><p class="lead" style="margin:0 auto 24px">We couldn't find that page. Try one of these:</p>
<div class="ctas" style="justify-content:center"><a class="btn btn-yellow" href="/{HOME}">Home</a><a class="btn btn-ghost" href="/services/">Services</a><a class="btn btn-ghost" href="/request-a-bid/">Request a Bid</a></div>
</div></section></main>
<footer class="credit-row" style="position:fixed;right:0;bottom:0"><a class="credit" href="{CREDIT_URL}" target="_blank" rel="noopener"><img src="/assets/img/mediain360-credit-light.png" alt="Produced and Powered by MediaIn360" width="80" height="21" style="width:80px;max-width:80px;height:auto;display:block"></a></footer></body></html>"""
    PAGES["404.html"] = body


# ---------------------------------------------------------------- write
def fingerprint_assets():
    """Copy CSS/JS to content-hashed names (site.<hash>.css) so no host or CDN cache can serve a stale copy."""
    mapping = {}
    for rel_path in ("assets/css/site.css", "assets/js/site.js", "assets/js/qrcode.js"):
        src = os.path.join(OUT, rel_path)
        base, ext = os.path.splitext(src)
        with open(src, "rb") as f:
            data = f.read()
        digest = hashlib.md5(data).hexdigest()[:10]
        folder = os.path.dirname(src)
        stem = os.path.basename(base)
        for old in os.listdir(folder):
            if re.fullmatch(re.escape(stem) + r"\.[0-9a-f]{10}" + re.escape(ext), old):
                os.remove(os.path.join(folder, old))
        with open(f"{base}.{digest}{ext}", "wb") as f:
            f.write(data)
        mapping[rel_path] = rel_path[: -len(ext)] + f".{digest}{ext}"
    return mapping


def write_all():
    for d in os.listdir(OUT):
        if d in ("assets",):
            continue
        p = os.path.join(OUT, d)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    hashed = fingerprint_assets()
    count = sum(1 for k in PAGES if k != "404.html")
    for path, html in PAGES.items():
        html = html.replace("{PAGE_COUNT}", str(count))
        for old, new in hashed.items():
            html = html.replace(old, new)
        target = os.path.join(OUT, path) if path.endswith(".html") else os.path.join(OUT, path, "index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(html)
    robots = "User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(robots)
    urls = "".join(f"  <url><loc>{SITE_URL}/{p}</loc></url>\n" for p in SITEMAP)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    vcard = "\r\n".join([
        "BEGIN:VCARD", "VERSION:3.0", f"FN:{BIZ['name']}", f"ORG:{BIZ['name']}",
        f"TEL;TYPE=WORK,VOICE:{BIZ['phone_tel']}", f"EMAIL;TYPE=WORK:{plain(BIZ['email'])}",
        f"URL:{SITE_URL}/", "NOTE:Land clearing · excavation · restoration · since " + BIZ["founded"], "END:VCARD", ""])
    with open(os.path.join(OUT, "assets", "everglades-contact.vcf"), "w") as f:
        f.write(vcard)
    with open(os.path.join(HERE, "send-checklist.php")) as f:
        php = f.read().replace("__CHECKLIST_TO__", CHECKLIST_TO)
    with open(os.path.join(OUT, "send-checklist.php"), "w") as f:
        f.write(php)
    os.makedirs(os.path.join(OUT, "submissions"), exist_ok=True)
    with open(os.path.join(OUT, "submissions", ".htaccess"), "w") as f:
        f.write("# Saved checklist answers: never served to the web\nRequire all denied\n<IfModule !mod_authz_core.c>\nDeny from all\n</IfModule>\n")
    with open(os.path.join(OUT, ".htaccess"), "w") as f:
        f.write("# Hostinger / Apache\nDirectoryIndex index.html\nErrorDocument 404 /404.html\nOptions -Indexes\nAddType text/vcard .vcf\n\n"
                "<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType image/webp \"access plus 1 year\"\n"
                "ExpiresByType image/png \"access plus 1 year\"\nExpiresByType text/css \"access plus 1 month\"\n"
                "ExpiresByType application/javascript \"access plus 1 month\"\n</IfModule>\n\n"
                "# Pages are never cached, so every upload shows immediately (CSS/JS have hashed names).\n"
                "<IfModule mod_headers.c>\n<FilesMatch \"\\.(html|php)$\">\nHeader set Cache-Control \"no-cache, no-store, must-revalidate\"\n</FilesMatch>\n</IfModule>\n")
    return count


def main():
    PLACES.update(build_place_index())
    build_front_door()
    build_home()
    build_services()
    build_audiences()
    build_places()
    build_anywhere()
    build_capability()
    build_capabilities()
    build_checklist()
    build_projects()
    build_questions()
    build_about()
    build_credentials()
    build_bid()
    build_reviews()
    build_legal()
    build_plan()
    build_qr_sheet()
    build_404()
    n = write_all()
    print(f"Built {n} pages (+404) into {OUT}")


if __name__ == "__main__":
    main()
