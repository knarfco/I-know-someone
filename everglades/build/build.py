#!/usr/bin/env python3
"""Builds the Everglades Restorations & Land Clearing static site into ../site/.

Run:  python3 everglades/build/build.py
Output is plain HTML/CSS/JS that can be uploaded to any host (Hostinger, etc.).
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import BIZ, SERVICES, SVC, AUDIENCES, PROJECTS, QUESTIONS  # noqa: E402

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
                    "addressRegion": "FL", "addressCountry": "US"},
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
def header(cur):
    L = lambda p: rel(cur, p)  # noqa: E731
    land = "".join(f'<a href="{L("services/" + s["slug"] + "/")}">{s["name"]}</a>' for s in SERVICES if s["group"] == "land")
    env = "".join(f'<a href="{L("services/" + s["slug"] + "/")}">{s["name"]}</a>' for s in SERVICES if s["group"] == "env")
    aud = "".join(f'<a href="{L("who-we-serve/" + a["slug"] + "/")}">{a["menu"]}</a>' for a in AUDIENCES)
    regions = "".join(f'<a href="{L(r["path"])}">{r["name"]} ({len(r["projects"])} jobs)</a>' for r in PLACES.values())
    return f"""
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span class="since">Land Clearing · Excavation · Restoration · Since {BIZ['founded']}</span>
  <span>Call <a href="{tel_href(cur)}">{ph(BIZ['phone'])}</a> · Storm response 24/7</span>
</div></div>
<header class="header"><div class="wrap">
  <a class="brand" href="{L(HOME)}" aria-label="{esc(BIZ['name'])} home">
    <img src="{L('assets/img/everglades-mark.png')}" alt="" width="54" height="54">
    <span class="brand-name">EVERGLADES<small>RESTORATIONS &amp; LAND CLEARING INC.</small></span>
  </a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="nav">☰ Menu</button>
  <nav class="nav" id="nav" aria-label="Main">
    <ul>
      <li><details><summary>Services</summary><div class="menu wide">
        <div><div class="menu-head">Land &amp; Site Work</div>{land}</div>
        <div><div class="menu-head">Environmental &amp; Storm</div>{env}</div>
        <div><a href="{L('services/')}"><b>All services →</b></a></div>
      </div></details></li>
      <li><details><summary>Who We Serve</summary><div class="menu">{aud}<a href="{L('who-we-serve/')}"><b>Overview →</b></a></div></details></li>
      <li><details><summary>Where We Work</summary><div class="menu">
        <a href="{L('projects-anywhere/')}"><b>Projects Anywhere</b></a>
        <div class="menu-head">Where we've worked</div>{regions}
        <a href="{L('where-weve-worked/')}"><b>All places →</b></a>
      </div></details></li>
      <li><a class="top" href="{L('projects/')}">Job Videos</a></li>
      <li><a class="top" href="{L('questions/')}">Questions</a></li>
      <li><details><summary>About</summary><div class="menu">
        <a href="{L('about/')}">Our History (Since {BIZ['founded']})</a>
        <a href="{L('credentials/')}">Licenses &amp; Credentials</a>
        <a href="{L('reviews/')}">Reviews</a>
      </div></details></li>
    </ul>
    <a class="btn btn-yellow btn-sm" href="{L('request-a-bid/')}">Request a Bid</a>
  </nav>
</div></header>"""


def footer(cur):
    L = lambda p: rel(cur, p)  # noqa: E731
    svc = "".join(f'<li><a href="{L("services/" + s["slug"] + "/")}">{s["name"]}</a></li>' for s in SERVICES)
    regions = "".join(f'<li><a href="{L(r["path"])}">{r["name"]}</a></li>' for r in PLACES.values())
    return f"""
<footer class="footer"><div class="wrap">
  <div class="footer-grid">
    <div>
      <img class="footer-logo" src="{L('assets/img/everglades-logo-640.webp')}" alt="{esc(BIZ['name'])}" width="640" height="289" loading="lazy">
      <p>Land clearing, excavation and environmental restoration since {BIZ['founded']}. Headquartered in South Florida — working wherever the job is.</p>
      <p>{ph(BIZ['address'])}<br>{ph(BIZ['city_state'])}<br>
      <a href="{tel_href(cur)}">{ph(BIZ['phone'])}</a><br>{ph(BIZ['email'])}<br>{ph(BIZ['hours'])}</p>
      <p>{ph(BIZ['license'])}</p>
    </div>
    <div><h4>Services</h4><ul>{svc}</ul></div>
    <div><h4>Where We Work</h4><ul>
      <li><a href="{L('projects-anywhere/')}">Projects Anywhere</a></li>
      <li><a href="{L('where-weve-worked/')}">Where We've Worked</a></li>{regions}
      <li><a href="{L('projects/')}">Job Videos</a></li>
    </ul></div>
    <div><h4>Company</h4><ul>
      <li><a href="{L('about/')}">About &amp; History</a></li>
      <li><a href="{L('credentials/')}">Licenses &amp; Credentials</a></li>
      <li><a href="{L('questions/')}">Questions &amp; Answers</a></li>
      <li><a href="{L('who-we-serve/government-agencies/')}">Government &amp; Agencies</a></li>
      <li><a href="{L('reviews/')}">Leave a Review</a></li>
      <li><a href="{L('request-a-bid/')}">Request a Bid</a></li>
      <li>YouTube: {ph(BIZ['youtube'])}</li>
      <li>Google: {ph(BIZ['gbp'])}</li>
    </ul></div>
  </div>
  <div class="legal">
    <span>© <span data-current-year>2026</span> {BIZ['name']} All rights reserved.</span>
    <span><a href="{L('privacy/')}">Privacy</a></span>
  </div>
</div></footer>
<div class="callbar"><a class="c1" href="{tel_href(cur)}">📞 Call Now</a><a class="c2" href="{L('request-a-bid/')}">Request a Bid</a></div>"""


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


def trust_strip():
    return f"""<div class="trust"><div class="wrap"><ul>
<li>{BIZ['years']} years in business · Since {BIZ['founded']}</li>
<li>Licensed &amp; insured · {BIZ['license']}</li>
<li>Army Corps project experience</li>
<li>FEMA-ready storm response</li>
<li>Our own equipment &amp; crews</li>
</ul></div></div>"""


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
            f'data-region="{slugify(p["place"]["region_name"])}" data-year="{p["date"][:4]}">'
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
    cur = DOOR
    L = lambda p: rel(cur, p)  # noqa: E731
    style = """<style>
body{background:radial-gradient(ellipse at 50% 35%,#13692e 0%,#06381A 45%,#031d0d 100%);color:#fff;min-height:100vh;display:flex;flex-direction:column}
.door{flex:1;display:flex;align-items:center;justify-content:center;padding:40px 20px}
.door-grid{display:grid;grid-template-columns:1fr auto;gap:56px;align-items:center;max-width:1180px;width:100%}
.door-logo{position:relative}
.door-logo::before{content:"";position:absolute;left:4%;top:-6%;width:46%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(255,200,40,.55),rgba(255,160,0,.18) 45%,transparent 70%);filter:blur(10px);animation:glow 5s ease-in-out infinite alternate;pointer-events:none}
@keyframes glow{from{opacity:.55;transform:scale(.92)}to{opacity:1;transform:scale(1.08)}}
@media (prefers-reduced-motion:reduce){.door-logo::before{animation:none}}
.door-logo img{position:relative;width:100%;filter:drop-shadow(0 0 1px rgba(255,255,255,.95)) drop-shadow(0 0 5px rgba(255,255,255,.35)) drop-shadow(0 14px 34px rgba(0,0,0,.55))}
.door-tag{font-family:var(--head);font-size:clamp(1.3rem,2.6vw,2rem);letter-spacing:.06em;text-transform:uppercase;text-align:center;margin:26px 0 6px;color:#fff}
.door-sub{text-align:center;color:#bfe0c6;margin:0 0 26px}
.door-ctas{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.door-ctas .btn{font-size:1.1rem;padding:16px 30px}
.qr-panel{background:#fff;color:var(--ink);border-radius:16px;padding:22px;text-align:center;width:250px;box-shadow:0 20px 50px rgba(0,0,0,.4)}
.qr-panel .qr{width:200px;height:200px;margin:0 auto}
.qr-panel .qr svg{width:100%;height:100%}
.qr-panel b{display:block;font-family:var(--head);font-weight:400;font-size:1.25rem;text-transform:uppercase;color:var(--green-deep);margin-top:10px}
.qr-panel small{display:block;color:var(--ink-soft);word-break:break-all;margin-top:4px}
.door-foot{text-align:center;padding:18px;color:#8fbf99;font-size:.85rem}
.door-foot a{color:#cfe8d4}
@media (max-width:860px){.door-grid{grid-template-columns:1fr;gap:34px}.qr-panel{margin:0 auto}}
</style>"""
    body = f"""
<div class="door"><div class="door-grid">
  <div>
    <div class="door-logo"><img src="{L('assets/img/everglades-logo.webp')}" alt="{esc(BIZ['name'])}" width="1400" height="632"></div>
    <p class="door-tag">Land Clearing, Excavation &amp; Restoration</p>
    <p class="door-sub">Since {BIZ['founded']} · Wherever the job is</p>
    <div class="door-ctas">
      <a class="btn btn-yellow" href="{L(HOME)}">Enter Site →</a>
      <a class="btn btn-ghost" href="{L('request-a-bid/')}">Request a Bid</a>
    </div>
  </div>
  <div class="qr-panel">
    <div class="qr" id="qr-door" data-qr="/" role="img" aria-label="QR code to open this website on a phone"></div>
    <b>Scan to open on your phone</b>
    <small data-qr-url="qr-door"></small>
  </div>
</div></div>
<div class="door-foot">{ph(BIZ['phone'])} · {BIZ['name']}</div>"""
    page(cur, f"{BIZ['name']} | Land Clearing, Excavation & Restoration Since {BIZ['founded']}",
         f"{BIZ['name']}: land clearing, excavation, wetland restoration and storm response since {BIZ['founded']}.",
         body, chrome=False, extra_head=style, noindex=FRONT_DOOR_AT_ROOT is False)


def build_home():
    cur = HOME
    L = lambda p: rel(cur, p)  # noqa: E731
    lanes = f"""
<div class="grid g3">
  <a class="card lane-card" href="{L('who-we-serve/government-agencies/')}"><h3>Government &amp; Agencies</h3><p>Restoration earthwork, exotic removal, drainage and FEMA storm response for agencies and prime contractors.</p><span class="more">Capabilities</span></a>
  <a class="card lane-card" href="{L('who-we-serve/contractors-developers/')}"><h3>Contractors &amp; Developers</h3><p>Clearing, site prep, ponds and grading — on schedule, with our own equipment and crews.</p><span class="more">Work with us</span></a>
  <a class="card lane-card" href="{L('who-we-serve/homeowners-ranches/')}"><h3>Homeowners, Ranches &amp; HOAs</h3><p>Lots, pasture, ponds, culverts and lake banks. Tell us what you need and we'll take care of it.</p><span class="more">Get started</span></a>
</div>"""
    places_html = "".join(f'<h3 class="mt">{r["name"]}</h3>' + place_pills(cur, r["cities"].values()) for r in PLACES.values())
    qlinks = "".join(f'<li><a href="{L("questions/" + q["slug"] + "/")}">{q["q"]}</a></li>' for q in QUESTIONS)
    body = f"""
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">Since {BIZ['founded']} · {BIZ['years']} years of site work</span>
    <h1>Land Clearing, Excavation &amp; Restoration — Wherever the Job Is</h1>
    <p class="lead">From a single homesite to thousands of acres of wetland restoration — our own crews, our own equipment, and {BIZ['years']} years of knowing how land and water really work.</p>
    <div class="ctas">
      <a class="btn btn-yellow" href="{L('request-a-bid/')}">Request a Bid</a>
      <a class="btn btn-ghost" href="{tel_href(cur)}">Call {BIZ['phone']}</a>
      <a class="btn btn-ghost" href="{L('projects/')}">Watch Our Work</a>
    </div>
  </div>
  <div><img class="hero-logo" src="{L('assets/img/everglades-logo.webp')}" alt="{esc(BIZ['name'])} logo" width="1400" height="632"></div>
</div></section>
{trust_strip()}

<section class="section"><div class="wrap">
  <div class="section-head"><span class="eyebrow" style="color:var(--green)">What we do</span><h2>Services</h2>
  <p>Land and site work for every kind of property, plus the environmental and storm work communities depend on.</p></div>
  {service_cards(cur, [s['slug'] for s in SERVICES], 'g4')}
</div></section>

<section class="section alt"><div class="wrap split">
  <div>
    <span class="eyebrow" style="color:var(--green)">See it for yourself</span>
    <h2>Real Jobs. Real Video.</h2>
    <p>Every job we film gets its own page — the date, the place, the equipment and the result. No stock photos.</p>
    {video('Featured job video', 'Latest YouTube job video plays here')}
    <p class="mt"><a class="btn btn-green" href="{L('projects/')}">Browse All Job Videos</a></p>
  </div>
  <div>
    <h3>Before &amp; After</h3>
    {before_after('Drag the slider — before and after photos from a real job go here')}
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>Who We Work For</h2><p>Agencies, builders and landowners all get the same thing: a crew that shows up and does it right.</p></div>
  {lanes}
</div></section>

<section class="section dark"><div class="wrap">
  <div class="stats">
    <div class="stat"><b>{BIZ['years']}</b><span>years in business</span></div>
    <div class="stat"><b>[[XXX]]</b><span>jobs completed</span></div>
    <div class="stat"><b>[[XX,XXX]]</b><span>acres cleared</span></div>
    <div class="stat"><b>[[XX]]</b><span>states &amp; places worked</span></div>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div><div class="section-head"><h2>Where We've Worked</h2><p>Every place here has a real, dated job video behind it — and the list grows with every job.</p></div>
  {places_html}
  <p class="mt"><a href="{L('where-weve-worked/')}">All places →</a></p></div>
  <div>{anywhere_teaser(cur)}</div>
</div></section>

<section class="section alt"><div class="wrap split">
  <div>
    <h2>Licensed, Insured &amp; Proven</h2>
    <ul class="checks">
      <li>{BIZ['license']}</li>
      <li>{BIZ['insurance']}</li>
      <li>{BIZ['usace']}</li>
      <li>{BIZ['fema']}</li>
      <li>{BIZ['sam_uei']}</li>
    </ul>
    <a class="btn btn-outline" href="{L('credentials/')}">See all credentials</a>
  </div>
  <div>
    <h3>Common Questions</h3>
    <ul class="checks">{qlinks}</ul>
    <a href="{L('questions/')}">All questions →</a>
  </div>
</div></section>
{cta_band(cur)}"""
    page(cur, f"Land Clearing, Excavation & Restoration Contractor | {BIZ['short']} Since {BIZ['founded']}",
         f"Land clearing, forestry mulching, excavation, wetland restoration and storm debris removal — wherever the job is. Licensed and insured, since {BIZ['founded']}.",
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
            if place_path(p["place"]) not in [x[0] for x in places]:
                places.append((place_path(p["place"]), place_label(p["place"])))
        place_links = "".join(f'<li><a href="{L(a)}">{b}</a></li>' for a, b in places) or "<li>Listed here as job videos are added</li>"
        includes = "".join(f"<li>{i}</li>" for i in s["includes"])
        equip = "".join(f"<li>{e}</li>" for e in s["equipment"])
        intro = "".join(f"<p>{p}</p>" for p in s["intro"])
        body = page_hero(cur, trail, s["h1"], s["lead"], eyebrow=f"Since {BIZ['founded']}") + f"""
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
        page(cur, f"{s['name']} Contractor | {BIZ['short']} Since {BIZ['founded']}",
             f"{s['lead']} Licensed and insured, since {BIZ['founded']} — wherever the job is.",
             body, schema=schema, crumbs=trail)


def build_audiences():
    cur = "who-we-serve/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Who We Serve", cur)]
    cards = "".join(f'<a class="card lane-card" href="{L("who-we-serve/" + a["slug"] + "/")}"><h3>{a["name"]}</h3><p>{a["lead"]}</p><span class="more">Learn more</span></a>' for a in AUDIENCES)
    body = page_hero(cur, trail, "Who We Serve", "Agencies, builders and landowners — every one gets a crew that shows up and does the job right.") + \
        f'<section class="section"><div class="wrap"><div class="grid g3">{cards}</div></div></section>{cta_band(cur)}'
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
    <table class="facts">
      <tr><th>Company</th><td>{BIZ['name']}</td></tr>
      <tr><th>In business since</th><td>{BIZ['founded']}</td></tr>
      <tr><th>SAM.gov UEI / CAGE</th><td>{BIZ['sam_uei']} · {BIZ['cage']}</td></tr>
      <tr><th>NAICS</th><td>{BIZ['naics']}</td></tr>
      <tr><th>State license</th><td>{BIZ['license']}</td></tr>
      <tr><th>Bonding</th><td>{BIZ['bonding']}</td></tr>
      <tr><th>Insurance</th><td>{BIZ['insurance']}</td></tr>
      <tr><th>FEMA</th><td>{BIZ['fema']}</td></tr>
      <tr><th>Army Corps</th><td>{BIZ['usace']}</td></tr>
      <tr><th>Certifications</th><td>[[Small business / DBE / other certifications XXX]]</td></tr>
      <tr><th>Registered bid portals</th><td>[[MyFloridaMarketPlace · DemandStar · county portals XXX]]</td></tr>
    </table>
    <p class="mt"><a class="btn btn-green" href="#">[[Download Capability Statement (PDF) XXX]]</a></p>
  </div>
  <div>
    <h3>Past Performance</h3>
    <div class="empty-slot">Project name · agency / prime · year · scope · value<br>[[XXX]]</div>
    <div class="empty-slot mt">Project name · agency / prime · year · scope · value<br>[[XXX]]</div>
    <div class="empty-slot mt">Project name · agency / prime · year · scope · value<br>[[XXX]]</div>
  </div>
</div></section>
<section class="section"><div class="wrap prose">
  <h2>Teaming With Prime Contractors</h2>
  <p>Large restoration and water projects need dependable clearing, exotic-removal and earthwork subcontractors who know wet, difficult ground. We've spent {BIZ['years']} years working it — and we're ready to team on the next one, wherever it's let.</p>
  <p><a class="btn btn-yellow" href="{L('request-a-bid/')}">Send us a scope or solicitation</a></p>
</div></section>"""
        body = page_hero(cur, trail, a["h1"], a["lead"]) + f"""
<section class="section"><div class="wrap split">
  <div><h2>Who We Work With</h2><ul class="checks">{who}</ul></div>
  <div>{video(a['name'] + ' video', 'A job video for this kind of client goes here')}</div>
</div></section>
{extra}
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
    body = page_hero(cur, trail, "Where We've Worked", "Every place on this page is here because we did a real job there — and there's a dated video to prove it. The list grows with every job.") + f"""
<section class="section"><div class="wrap">
  <div class="grid g2">{blocks}
  <div class="empty-slot">The next place shows up here automatically when its first job video is added.</div></div>
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
    body = page_hero(cur, trail, "Projects Anywhere", f"Big job far from home? We plan it, manage it and get it done — wherever it is. {BIZ['years']} years of know-how, on your site.", eyebrow="Any state · any country") + f"""
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
    <li>{BIZ['years']} years of planning and running heavy site work</li>
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
    years = sorted({p["date"][:4] for p in PROJECTS}, reverse=True)
    yr_opts = "".join(f'<option value="{y}">{y}</option>' for y in years)
    cards = "".join(project_card(cur, p) for p in sorted(PROJECTS, key=lambda p: p["date"], reverse=True))
    body = page_hero(cur, trail, "Job Videos", "Every job we film: the date, the place, the equipment and the result. Filter by service, location or year.") + f"""
<section class="section"><div class="wrap">
  <div class="filters">
    <label>Service<select data-filter="service"><option value="">All services</option>{svc_opts}</select></label>
    <label>Location<select data-filter="region"><option value="">All locations</option>{cty_opts}</select></label>
    <label>Year<select data-filter="year"><option value="">All years</option>{yr_opts}</select></label>
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
      <tr><th>Location</th><td><a href="{L(place_path(pl))}">{pl['city']}</a>, <a href="{L(region_path(pl))}">{pl['region_name']}</a></td></tr>
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
            "locationCreated": {"@type": "Place", "name": f"{pl['city']}, {pl['region_name']}"},
        }]
        if p["youtube"]:
            schema.append({"@context": "https://schema.org", "@type": "VideoObject", "name": p["title"],
                           "description": p["summary"], "uploadDate": p["date"],
                           "thumbnailUrl": f"https://i.ytimg.com/vi/{p['youtube']}/hqdefault.jpg",
                           "embedUrl": f"https://www.youtube.com/embed/{p['youtube']}"})
        page(cur, f"{p['title']} ({p['date'][:4]}) | {BIZ['short']}",
             f"{p['summary']} {place_label(pl)} — {p['date_label']}.", body, schema=schema, crumbs=trail)


def build_questions():
    cur = "questions/"
    L = lambda p: rel(cur, p)  # noqa: E731
    trail = [("Home", HOME), ("Questions", cur)]
    cards = "".join(f'<a class="card" href="{L("questions/" + q["slug"] + "/")}"><h3>{q["q"]}</h3><p>{q["short"][:150]}…</p><span class="more">Read the answer</span></a>' for q in QUESTIONS)
    body = page_hero(cur, trail, "Questions &amp; Answers", "Straight answers about land clearing, permits, wetlands, timing and cost — from a crew that's been doing it since 1992.") + f"""
<section class="section"><div class="wrap"><div class="grid g2">{cards}
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
    body = page_hero(cur, trail, f"Clearing Land Since {BIZ['founded']}", f"{BIZ['years']} years, [[XXX]] jobs and a lot of hard-won knowledge about land and water. Headquartered in South Florida — working wherever the job is.", eyebrow="Our history") + f"""
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
<section class="section dark"><div class="wrap"><div class="stats">
  <div class="stat"><b>{BIZ['years']}</b><span>years in business</span></div>
  <div class="stat"><b>[[XXX]]</b><span>jobs completed</span></div>
  <div class="stat"><b>[[XX]]</b><span>machines in our fleet</span></div>
  <div class="stat"><b>[[XX]]</b><span>crew members</span></div>
</div></div></section>
{cta_band(cur)}"""
    page(cur, f"About Us | Land Clearing & Restoration Since {BIZ['founded']} | {BIZ['short']}",
         f"{BIZ['name']} has cleared, dug and restored land since {BIZ['founded']}.", body, crumbs=trail)


def build_credentials():
    cur = "credentials/"
    trail = [("Home", HOME), ("Credentials", cur)]
    rows = [
        ("State contractor license", BIZ["license"]), ("Local business tax receipts", "[[County / city BTR #s XXX]]"),
        ("Insurance", BIZ["insurance"]), ("Bonding", BIZ["bonding"]), ("FEMA", BIZ["fema"]),
        ("Army Corps of Engineers", BIZ["usace"]), ("SAM.gov", BIZ["sam_uei"] + " · " + BIZ["cage"]),
        ("NAICS codes", BIZ["naics"]), ("State / federal contract numbers", "[[XXX]]"),
        ("Herbicide / applicator license", "[[FDACS license # XXX or licensed partner]]"),
        ("Certifications", "[[Small business / DBE / other XXX]]"),
    ]
    table = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows)
    body = page_hero(cur, trail, "Licenses, Insurance &amp; Credentials", "Everything an owner, engineer or contracting officer needs to check us out — in one place.") + f"""
<section class="section"><div class="wrap split">
  <div><table class="facts">{table}</table>
  <p class="small mt">Copies of certificates available on request.</p></div>
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
    <input type="hidden" name="lead_lane"><input type="hidden" name="landing_page"><input type="hidden" name="referrer">
    <button class="btn btn-yellow" type="submit" style="width:100%">Send My Request</button>
    <p class="small mt">We never share your information. <a href="{L('privacy/')}">Privacy</a></p>
  </form>
  <div>
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
    body = page_hero(cur, trail, "Worked With Us? Tell Others.", f"After {BIZ['years']} years, word of mouth built this company. A quick Google review helps the next customer find us.", ctas=False) + f"""
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
  <p class="small">Mentioning the job and the city ("cleared 3 acres in Davie") helps the most.</p></div>
</div></section>"""
    page(cur, f"Reviews | {BIZ['short']}", f"Reviews of {BIZ['name']}.", body, crumbs=trail)


def build_privacy():
    cur = "privacy/"
    trail = [("Home", HOME), ("Privacy", cur)]
    body = page_hero(cur, trail, "Privacy", "How we handle the information you send us.", ctas=False) + f"""
<section class="section"><div class="wrap prose">
<p>When you request a bid or contact us, we use your information only to respond to you and to provide the work you ask about. We do not sell your information.</p>
<p>This site may use basic analytics to understand how visitors find us. [[Analytics provider XXX]]</p>
<p>Questions: {BIZ['email']}</p>
<p class="small">[[Have counsel review before launch.]]</p>
</div></section>"""
    page(cur, f"Privacy | {BIZ['short']}", "Privacy policy.", body, crumbs=trail, noindex=True)


def build_plan():
    """Client-facing plan page for Matt & Sam (hidden from search)."""
    cur = "plan/"
    L = lambda p: rel(cur, p)  # noqa: E731
    n_pages_hint = "{PAGE_COUNT}"
    body = f"""
<section class="hero"><div class="wrap hero-grid">
  <div><span class="eyebrow">Prepared for Matt &amp; Sam</span>
  <h1>Your New Home Online</h1>
  <p class="lead">{BIZ['years']} years of great work — now built so the people who need it can find it. Here's what's built, how it works, and what comes next.</p>
  <div class="ctas"><a class="btn btn-yellow" href="{L(HOME)}">Tour the Website</a><a class="btn btn-ghost" href="{L('qr/')}">Printable QR Sheet</a></div></div>
  <div><img class="hero-logo" src="{L('assets/img/everglades-logo.webp')}" alt="" width="1400" height="632"></div>
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
  <div class="section-head"><h2>What's Built So Far</h2><p>This preview is the full skeleton — {n_pages_hint} pages. The yellow highlighted spots are where your real details go.</p></div>
  <div class="grid g4">
    <a class="card" href="{L(HOME)}"><h3>Home</h3><p>Your front page with video, before/after and credentials.</p></a>
    <a class="card" href="{L('services/')}"><h3>{len(SERVICES)} Services</h3><p>A full page for each type of work.</p></a>
    <a class="card" href="{L('where-weve-worked/')}"><h3>Where We've Worked</h3><p>Built only from your real jobs — every video puts a new place on the map.</p></a>
    <a class="card" href="{L('projects-anywhere/')}"><h3>Projects Anywhere</h3><p>Big job far from home? Matt plans it, the right crew does it.</p></a>
    <a class="card" href="{L('projects/')}"><h3>Job Videos</h3><p>Filterable job videos — {len(PROJECTS)} samples built from your example list.</p></a>
    <a class="card" href="{L('who-we-serve/government-agencies/')}"><h3>Government Page</h3><p>Capability snapshot for agencies and prime contractors.</p></a>
    <a class="card" href="{L('questions/')}"><h3>Questions</h3><p>Straight answers on cost, permits and wetlands.</p></a>
    <a class="card" href="{L('request-a-bid/')}"><h3>Request a Bid</h3><p>The form every inquiry comes through.</p></a>
    <a class="card" href="{L('about/')}"><h3>About · Since {BIZ['founded']}</h3><p>Your history, your people, your numbers.</p></a>
  </div>
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
      <li>License, insurance, bonding, FEMA, Army Corps and SAM.gov numbers</li>
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
    body = f"""<div class="sheet">
  <img src="{L('assets/img/everglades-logo.png')}" alt="{esc(BIZ['name'])}" width="1400" height="632">
  <h1>See Our New Website</h1>
  <p>Point your phone's camera at the code.</p>
  <div class="qr" id="qr-sheet" data-qr="/" role="img" aria-label="QR code to the website"></div>
  <p class="url" data-qr-url="qr-sheet"></p>
  <p class="tag">Land Clearing · Excavation · Restoration · Since {BIZ['founded']}</p>
  <p>{BIZ['phone']}</p>
  <div class="printbar"><button class="btn btn-yellow" onclick="window.print()">Print this page</button>
  <a class="btn btn-outline" href="{L(DOOR)}">Back</a></div>
</div>"""
    page(cur, f"QR Code | {BIZ['short']}", "Printable QR code.", body, chrome=False, extra_head=style, noindex=True)


def build_404():
    # Served from any depth, so it uses root-absolute paths.
    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page Not Found | {BIZ['short']}</title><meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css"><link rel="icon" href="/assets/img/icon-32.png"></head>
<body><section class="hero" style="min-height:100vh;display:flex;align-items:center"><div class="wrap center">
<img src="/assets/img/everglades-logo-640.webp" alt="{esc(BIZ['name'])}" style="margin:0 auto 24px;max-width:420px">
<h1>This Page Got Cleared</h1><p class="lead" style="margin:0 auto 24px">We couldn't find that page. Try one of these:</p>
<div class="ctas" style="justify-content:center"><a class="btn btn-yellow" href="/{HOME}">Home</a><a class="btn btn-ghost" href="/services/">Services</a><a class="btn btn-ghost" href="/request-a-bid/">Request a Bid</a></div>
</div></section></body></html>"""
    PAGES["404.html"] = body


# ---------------------------------------------------------------- write
def write_all():
    for d in os.listdir(OUT):
        if d in ("assets",):
            continue
        p = os.path.join(OUT, d)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    count = sum(1 for k in PAGES if k != "404.html")
    for path, html in PAGES.items():
        html = html.replace("{PAGE_COUNT}", str(count))
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
    with open(os.path.join(OUT, ".htaccess"), "w") as f:
        f.write("# Hostinger / Apache\nDirectoryIndex index.html\nErrorDocument 404 /404.html\nOptions -Indexes\n\n"
                "<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType image/webp \"access plus 1 year\"\n"
                "ExpiresByType image/png \"access plus 1 year\"\nExpiresByType text/css \"access plus 1 month\"\n"
                "ExpiresByType application/javascript \"access plus 1 month\"\n</IfModule>\n")
    return count


def main():
    PLACES.update(build_place_index())
    build_front_door()
    build_home()
    build_services()
    build_audiences()
    build_places()
    build_anywhere()
    build_projects()
    build_questions()
    build_about()
    build_credentials()
    build_bid()
    build_reviews()
    build_privacy()
    build_plan()
    build_qr_sheet()
    build_404()
    n = write_all()
    print(f"Built {n} pages (+404) into {OUT}")


if __name__ == "__main__":
    main()
