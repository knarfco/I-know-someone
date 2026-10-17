"""Beyond Klean static site generator.

Reads research/tasks.json + content/*.py and writes plain HTML to site/.
Every page is a standalone .html file with relative links, so the folder can be
uploaded to any static host as-is.

    python3 build_site.py
"""
import base64, hashlib, html, importlib.util, json, os, re, shutil
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from urllib.parse import quote as quote_url
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).parent
SITE = ROOT / "site"
CONTENT = ROOT / "content"
AELC_URL = "https://aboveeyelevelcleaning.com"
SITE_URL = "https://beyondklean.com"
PHONE = ""      # business phone, e.g. "(813) 555-0100"; shows Call buttons when set
ESTIMATOR_PASSWORD = "12345"  # unlocks /estimator/ and decrypts its price book; change and rebuild to rotate
OPERATOR = ""   # company performing the work, e.g. "Acme Cleaning LLC, license #123"; shown in the footer when set

e = lambda s: html.escape(str(s), quote=True)


def load(name):
    spec = importlib.util.spec_from_file_location(name, CONTENT / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- data
rows = json.loads((ROOT / "research" / "tasks.json").read_text())
fam_mod = load("families")
gen_mod = load("general")
inhouse = load("inhouse")
company_mod = load("company")
icons_mod = load("icons")
graphics = load("graphics")
ic = icons_mod.ic
FAMILY_ICON = icons_mod.FAMILY_ICON
trust_mod = load("trust")
PHONE = company_mod.COMPANY["phone"] or PHONE
OPERATOR = company_mod.COMPANY["operator"] or OPERATOR
FAM = inhouse.deep(fam_mod.F)  # family name -> dict(slug, short, intro, faq)

# Directory expansion: categories 21-24, services added to existing families, merged names as aliases
exp = load("expansion")
hubs = load("hubs")
for _p in sorted(CONTENT.glob("famx*.py")):
    FAM.update(inhouse.deep(load(_p.stem).F))
for _fn in exp.NEW_FAMILIES:
    FAM.setdefault(_fn, dict(slug=exp.SLUG[_fn], short=exp.SHORT[_fn], intro=_fn + ".", faq=[]))
FAMILY_ICON.update(exp.ICONS)
_seq = defaultdict(int)
for _task, _fam, _grp, _phase, _tier, _al in exp.TASKS:
    _fi = 21 + exp.NEW_FAMILIES.index(_fam) if _fam in exp.NEW_FAMILIES else 25
    _seq[_fi] += 1
    _why, _how = exp.GROUPS[_grp]
    rows.append(dict(id=f"BK-{_fi:02d}{_seq[_fi]:04d}", family=_fam, group=_grp, task=_task,
                     slug=re.sub(r"[^a-z0-9]+", "-", _task.lower()).strip("-"), phase=_phase, tier=_tier, aelc_feed="",
                     aliases=_al, alias_count=len(_al.split("; ")), why_it_matters=_why, beyond_klean_method=_how,
                     overlaps_with="", merge_into="", variant_of="", bundle=""))
for _r in rows:
    if _r["task"] in exp.MERGES:
        _r["aliases"] = "; ".join(filter(None, [_r["aliases"]] + exp.MERGES[_r["task"]]))
gen_mod.GENERAL_FAQ = inhouse.deep(gen_mod.GENERAL_FAQ)

CONTENT_BY_TASK = {}
for p in sorted(CONTENT.glob("f[0-9][0-9]*.py")):
    CONTENT_BY_TASK.update(load(p.stem).C)
PATCHED = set()
for p in sorted(CONTENT.glob("p[0-9][0-9]*.py")):  # rewrites that replace weak fields
    for k, v in load(p.stem).P.items():
        CONTENT_BY_TASK[k] = {**CONTENT_BY_TASK[k], **v}
        PATCHED.add(k)
        PATCHED.add(k)
for p in sorted(CONTENT.glob("a[0-9][0-9]*.py")):  # single-answer rewrites keyed by (task, index)
    for (k, i), ans in load(p.stem).A.items():
        qs = list(CONTENT_BY_TASK[k]["q"])
        qs[i] = (qs[i][0], ans)
        CONTENT_BY_TASK[k] = {**CONTENT_BY_TASK[k], "q": qs}
CONTENT_BY_TASK = inhouse.deep(CONTENT_BY_TASK)  # referral wording -> in-house voice

for r in rows:
    r["why_it_matters"], r["beyond_klean_method"] = inhouse.fix(r["why_it_matters"]), inhouse.fix(r["beyond_klean_method"])
by_id = {r["id"]: r for r in rows}
tasks = [r for r in rows if not r["merge_into"]]
for r in rows:  # fold merged duplicates into their primary page as aliases
    if r["merge_into"]:
        p = by_id[r["merge_into"]]
        extra = [r["task"][0].lower() + r["task"][1:]] + [a for a in r["aliases"].split("; ") if a]
        p["aliases"] = "; ".join(filter(None, [p["aliases"]] + extra))
for t in tasks:
    t["alias_list"] = list(dict.fromkeys(a for a in t["aliases"].split("; ") if a))
    t["fam_slug"] = FAM[t["family"]]["slug"]
    t["c"] = CONTENT_BY_TASK.get(t["task"])

fams = list(dict.fromkeys(t["family"] for t in tasks))
TRUST = trust_mod.Trust(company_mod, {t["task"]: t["slug"] for t in tasks})
HINTS = {
    "Site, Debris & Waste Management": "Debris haul-off, daily sweeps, recycling",
    "Rough Clean": "Phase one: slabs, stud bays, plenums",
    "Fine Dust, Drywall Dust & Controlled-Dust Cleaning": "Drywall dust, silica-safe housekeeping",
    "Overhead & Elevated Surfaces (Above Eye Level)": "Decks, beams, ducts, high dusting",
    "Walls, Ceilings & Interior Finishes": "Walls, ceiling tile, grid, diffusers",
    "Doors, Hardware, Millwork & Casework": "Doors, hardware, cabinets, counters",
    "Glass, Windows & Glazing": "Construction windows, storefronts, mirrors",
    "Hard Floors": "Concrete, VCT, LVT, tile, stone, wood",
    "Carpet & Soft Surfaces": "Carpet, extraction, upholstery",
    "Restrooms & Plumbing Fixtures": "Fixtures, labels, caulk haze, drains",
    "Kitchens, Food Facilities & FRP": "Restaurants, grocery, FRP, walk-ins",
    "Mechanical, Electrical & Construction IAQ": "Equipment rooms, filters, flush-out",
    "Retail Fixtures & Store Opening": "Store openings, fixtures, remodels",
    "Specialty & Controlled Environments": "Healthcare, labs, schools, hotels",
    "Exterior, Hardscape & Building Envelope": "Pressure washing, facades, lots",
    "Residue, Stain & Protective-Material Removal": "Paint, adhesive, labels, film",
    "Vertical Transportation & Circulation": "Elevators, stairs, lobbies",
    "Turnover, Punch & Closeout Support": "Final clean, punch list, move-in",
    "Multifamily & Residential-Scale Turnover": "Apartments, condos, amenities",
    "Restoration & Regulated Work (Conditional)": "Water, mold, fire, abatement",
}
HINTS.update(exp.HINTS)
for _fn in fams:
    FAM[_fn]["hint"] = HINTS.get(_fn, "")
groups = defaultdict(list)
for t in tasks:
    groups[(t["family"], t["group"])].append(t)
clusters = defaultdict(list)
for t in tasks:
    for kind in ("bundle", "variant_of"):
        for c in filter(None, t[kind].split("; ")):
            clusters[(kind, c)].append(t)

missing = [t["task"] for t in tasks if not t["c"]]
unknown = [k for k in CONTENT_BY_TASK if k not in {t["task"] for t in tasks}]

PHASE_SPEC = {
    "Rough": "01 74 13 Progress Cleaning",
    "Progress": "01 74 13 Progress Cleaning",
    "Final": "01 74 23 Final Cleaning",
    "Touch-up / punch": "01 74 23 Final Cleaning",
    "Occupancy / turnover": "01 77 00 Closeout Procedures",
    "Any stage / specialty": "Division 01 cleaning or specialty scope",
    "Recurring maintenance": "Post-occupancy maintenance",
}
PHASE_ORDER = ["Rough", "Progress", "Final", "Touch-up / punch", "Occupancy / turnover",
               "Any stage / specialty", "Recurring maintenance"]
PHASE_KEY = {p: re.sub(r"[^a-z]+", "-", p.lower()).strip("-") for p in PHASE_ORDER}
TIER_KEY = {"Core": "core", "Adjacent specialist": "specialist", "Conditional / regulated": "conditional"}
TIER_LABEL = {"Core": "Construction cleaning crew", "Adjacent specialist": "Specialist crew",
              "Conditional / regulated": "Licensed technicians"}
TIER_NOTE = {
    "Core": "Performed by our construction cleaning crews.",
    "Adjacent specialist": "Performed by crews trained and equipped for this specialty.",
    "Conditional / regulated": "Licensed or protocol-driven work, reviewed case by case and assigned only to certified technicians.",
}

GLOSS = gen_mod.GLOSSARY  # list of (term, slug, definition)

# Price book for the estimator (research/pricing.json): unit and low / typical / high rates per task
UNIT_LABEL = {"sqft": "Square foot", "lf": "Linear foot", "each": "Each", "hour": "Crew hour", "lot": "Lump sum",
              "ton": "Ton", "cy": "Cubic yard", "load": "Load", "pane": "Pane", "opening": "Opening",
              "fixture": "Fixture", "room": "Room", "unit": "Dwelling unit", "floor": "Floor", "day": "Crew day"}
_pp = ROOT / "research" / "pricing.json"
PRICING = json.loads(_pp.read_text()) if _pp.exists() else {"meta": {}, "items": {}}
PRICEBOOK = PRICING["items"]
for _p in sorted((ROOT / "research").glob("pricing_x*.json")):  # expansion services
    PRICEBOOK.update(json.loads(_p.read_text()))


# ---------------------------------------------------------------- layout
NAV = [("services.html", "Services"), ("projects.html", "Projects"), ("government.html", "Government"),
       ("general-contractors.html", "For GCs"), ("faq.html", "FAQ"), ("about.html", "About"), ("contact.html", "Contact")]


def page(path, title, desc, body, crumbs=None, schema=None, active=None, extra_js="", robots="noindex, nofollow"):
    depth = path.count("/")
    up = "../" * depth
    nav = "".join(
        f'<a href="{up}{h}"{" aria-current=\"page\"" if active == h else ""}>{e(l)}</a>' for h, l in NAV)
    bc = ""
    if crumbs:
        items = "".join(
            f'<li><a href="{up}{h}">{e(l)}</a></li>' if h else f'<li aria-current="page">{e(l)}</li>'
            for h, l in crumbs)
        bc = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{items}</ol></nav>'
        schema = (schema or []) + [{
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": l,
                                  **({"item": f"{SITE_URL}/{h}"} if h else {})}
                                 for i, (h, l) in enumerate(crumbs)]}]
    bcw = f'<div class="wrap">{bc}</div>' if bc else ""
    tel = "".join(ch for ch in PHONE if ch.isdigit() or ch == "+")
    foot_call = f'<p><a class="foot-tel" href="tel:{tel}">{e(PHONE)}</a></p>' if PHONE else ""
    op_note = f" Services performed by {e(OPERATOR)}." if OPERATOR else ""
    mcall = f'<a class="btn btn-light mbar-call" href="tel:{tel}">{ic("phone", up)}Call</a>' if PHONE else ""
    mbar = (f'<div class="mbar">{mcall}<a class="btn" href="{up}quote.html">Request a Bid'
            f'<span class="badge" data-bidbadge hidden>0</span></a></div>')
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                 for s in (schema or []))
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{SITE_URL}/{'' if path == 'index.html' else path}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..900&family=IBM+Plex+Mono:wght@400;600&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="preview-bar">Preview build · not indexed · beyondklean.com</div>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{up}index.html" aria-label="Beyond Klean home">
      <img class="logo-l" src="{up}assets/logo.png" alt="Beyond Klean" width="634" height="243">
      <img class="logo-d" src="{up}assets/logo-dark.png" alt="" width="634" height="243">
    </a>
    <a class="btn btn-sm quote-m" href="{up}quote.html">Request a Bid</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mainnav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="mainnav" id="mainnav" aria-label="Main">{nav}<a class="bidlink" href="{up}quote.html" data-bidcount hidden>Bid list <span class="badge">0</span></a><a class="btn btn-sm" href="{up}quote.html">Request a Bid</a></nav>
  </div>
</header>
<main id="main">
{bcw}
{body}
</main>
{'' if path in ('quote.html', 'estimator.html') else mbar}
<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <img class="logo-l foot-logo" src="{up}assets/logo.png" alt="Beyond Klean" width="634" height="243">
      <img class="logo-d foot-logo" src="{up}assets/logo-dark.png" alt="" width="634" height="243">
      <p class="small">Construction and specialty cleaning for general contractors, property managers and building owners. Itemized bids, our own crews, nationwide.</p>
      {foot_call}
    </div>
    <div><h2 class="foot-h">Services</h2>
      <a href="{up}services.html">All services</a><a href="{up}faq.html">FAQ</a><a href="{up}glossary.html">Glossary</a><a href="{up}methods.html">Our methods</a></div>
    <div><h2 class="foot-h">Company</h2>
      <a href="{up}about.html">About Beyond Klean</a><a href="{up}projects.html">Projects</a><a href="{up}safety.html">Safety and compliance</a><a href="{up}capability-statement.html">Capability statement</a><a href="{up}contact.html">Contact</a></div>
    <div><h2 class="foot-h">Work with us</h2>
      <a href="{up}quote.html">Request a bid</a><a href="{up}quote.html#specs">Send your specs</a><a href="{up}general-contractors.html">For general contractors</a><a href="{up}government.html">Government contracting</a></div>
    <div><h2 class="foot-h">Browse</h2>
      <a href="{up}facilities/index.html">By facility type</a><a href="{up}phases/index.html">By project phase</a><a href="{up}where-we-work.html">Where we work</a></div>
    <div><h2 class="foot-h">Above eye level</h2>
      <a href="{up}families/{FAM[fams[3]]['slug']}.html">Overhead &amp; high dusting</a><a href="{AELC_URL}" rel="noopener">AboveEyeLevelCleaning.com</a></div>
  </div>
  <div class="wrap small foot-note">© 2026 Beyond Klean.{op_note} Regulated work such as mold remediation, abatement and hood cleaning is performed only by licensed, certified technicians where required.</div>
</footer>
{'<script src="' + up + 'assets/search-index.js"></script>' if 'data-finder' in body else ''}{extra_js}
<script src="{up}assets/site.js"></script>
</body>
</html>
"""
    dest = SITE / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out)
    return out


def link_task(t, up):
    return f'<a href="{up}tasks/{t["slug"]}.html">{e(t["task"])}</a>'


def faq_schema(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}


def qa_html(qas, prefix):
    return "".join(
        f'<details class="qa" id="{prefix}{i + 1}"><summary><h3>{e(q)}</h3></summary><p>{e(a)}</p></details>'
        for i, (q, a) in enumerate(qas))


def task_qas(t):
    c = t["c"]
    qas = list(c["q"]) if c else []
    if t["alias_list"]:
        names = t["alias_list"]
        listed = ", ".join(f'"{n}"' for n in names[:-1]) + (" and " if len(names) > 1 else "") + f'"{names[-1]}"'
        qas.append((f"What else is {t['task'].lower()} called?",
                    f"Contractors, specs and buyers also call it {listed}. On Beyond Klean, all of these names "
                    f"point to the same scope, so a bid request under any of them gets the same crew and the same line item."))
    return qas


# ---------------------------------------------------------------- task pages
def build_task(t):
    up = "../"
    c = t["c"] or {"a": "Content in progress.", "y": "", "m": "", "s": [], "w": [], "q": []}
    fam = FAM[t["family"]]
    qas = task_qas(t)
    phase_k, tier_k = PHASE_KEY[t["phase"]], TIER_KEY[t["tier"]]

    related = []
    for (kind, cname), members in clusters.items():
        if t in members:
            others = [m for m in members if m is not t]
            if others:
                label = "Often bought together" if kind == "bundle" else "Same method on other surfaces"
                related.append((f"{label}: {cname}", others))
    sib = [x for x in groups[(t["family"], t["group"])] if x is not t]
    if sib:
        related.append((f"More in {t['group']}", sib))
    rel_html = "".join(
        f'<div class="rel"><h3>{e(h)}</h3><ul class="links">{"".join(f"<li>{link_task(m, up)}</li>" for m in ms)}</ul></div>'
        for h, ms in related)

    text = " ".join([c["a"], c["y"], c["m"]] + c["s"] + c["w"] + [q + " " + a for q, a in c["q"]]).lower()
    terms = [g for g in GLOSS if re.search(r"\b" + re.escape(g[0].lower()) + r"\b", text)]
    terms_html = ("<div class='terms'><span class='eyebrow'>Terms on this page</span>" +
                  "".join(f'<a class="chip" href="{up}glossary.html#{g[1]}">{e(g[0])}</a>' for g in terms) +
                  "</div>") if terms else ""

    aelc = ""
    if t["aelc_feed"]:
        aelc = (f'<div class="aelc"><strong>Keep it clean after turnover.</strong> Overhead dust comes back. '
                f'Recurring high dusting for this surface is handled through our sister brand, '
                f'<a href="{AELC_URL}" rel="noopener">AboveEyeLevelCleaning.com</a>.</div>')

    pb = PRICEBOOK.get(t["task"])
    unit_row = (f'<div><dt>Bid by</dt><dd>{e(UNIT_LABEL.get(pb["unit"], pb["unit"]))}</dd></div>' if pb else "")
    also = ('<div class="also"><span class="eyebrow">Also called</span>' +
            "".join(f'<span class="chip chip-static">{e(a)}</span>' for a in t["alias_list"]) + "</div>"
            if t["alias_list"] else "")
    facs = [f for f in FACILITY_HUBS if t["task"] in f["tasks"]]
    fac_row = ('<div><dt>Common in</dt><dd class="fac-chips">' + "".join(
        f'<a class="chip" href="{up}facilities/{f["slug"]}.html">{e(f["name"])}</a>' for f in facs[:4]) + "</dd></div>") if facs else ""
    more = lambda txt: (f'<div class="more" data-more><p>{e(txt)}</p></div>' if len(txt) > 260 else f"<p>{e(txt)}</p>")
    body = f"""
<div class="band band-white task-top"><div class="wrap">
  <p class="eyebrow fam-eyebrow">{ic(FAMILY_ICON[t['family']], up)}<a href="{up}families/{fam['slug']}.html">{e(fam['short'])}</a> · {e(t['group'])}</p>
  <h1>{e(t['task'])}</h1>
  <p class="lede">{e(c['a'])}</p>
  <div class="task-cta">
    <button class="btn btn-lg" type="button" data-add="{e(t['task'])}">Add to bid list</button>
    <a class="btn btn-ghost" href="{up}quote.html?add={quote_url(t['task'])}">Request a bid</a>
  </div>
  {graphics.phase_strip(phase_k)}
  {also}
</div></div>
<article class="wrap task" data-phase="{phase_k}">
  <div class="task-main">
    <div class="duo">
      <section class="card"><h2>{ic("why", up)}Why it matters</h2>{more(c['y'])}</section>
      <section class="card"><h2>{ic("how", up)}How we do it</h2>{more(c['m'])}
        <p class="small"><a href="{up}methods.html">Our capture-first method</a></p></section>
    </div>
    <section class="card"><h2>{ic("list", up)}Scope checklist for your bid</h2><ul class="check check-grid">{"".join(f"<li>{e(x)}</li>" for x in c['s'])}</ul></section>
    <section class="card card-warn"><h2>{ic("warn", up)}Watch-outs</h2><ul class="warn">{"".join(f"<li>{e(x)}</li>" for x in c['w'])}</ul></section>
    {aelc}
    <section id="questions"><h2 class="qh">{ic("question", up)}Common questions</h2>{qa_html(qas, 'q')}</section>
    {terms_html}
  </div>
  <aside class="spec" aria-label="Scope summary">
    <dl>
      <div><dt>Project stage</dt><dd><a class="pill ph-{phase_k}" href="{up}phases/{phase_k}.html">{e(t['phase'])}</a></dd></div>
      <div><dt>Typical spec section</dt><dd class="mono">{e(PHASE_SPEC[t['phase']])}</dd></div>
      {unit_row}
      <div><dt>Performed by</dt><dd><span class="pill tier-{tier_k}">{e(TIER_LABEL[t['tier']])}</span><span class="small block">{e(TIER_NOTE[t['tier']])}</span></dd></div>
      {fac_row}
      <div><dt>Scope ID</dt><dd class="mono">{e(t['id'])}</dd></div>
    </dl>
    <button class="btn" type="button" data-add="{e(t['task'])}">Add to bid list</button>
    <a class="btn btn-ghost" href="{up}quote.html?add={quote_url(t['task'])}">Request a bid</a>
  </aside>
</article>
<div class="band band-soft"><section class="wrap related"><h2>Related work</h2><div class="rel-grid">{rel_html}</div></section></div>
{TRUST.for_task(t["task"], up)}
"""
    schema = [{"@context": "https://schema.org", "@type": "Service", "name": t["task"],
               "alternateName": t["alias_list"], "description": c["a"], "serviceType": t["group"],
               "category": t["family"], "provider": {"@type": "Organization", "name": "Beyond Klean", "url": SITE_URL},
               "areaServed": {"@type": "Country", "name": "United States"}}]
    if qas:
        schema.append(faq_schema(qas))
    page(f"tasks/{t['slug']}.html", f"{t['task']} | Beyond Klean", c["a"][:155], body,
         crumbs=[("index.html", "Home"), ("services.html", "Services"),
                 (f"families/{fam['slug']}.html", fam["short"]), (None, t["task"])],
         schema=schema)


# ---------------------------------------------------------------- family pages
def build_family(fname, idx):
    up = "../"
    f = FAM[fname]
    ftasks = [t for t in tasks if t["family"] == fname]
    gsec = ""
    for (fn, gname), gts in groups.items():
        if fn != fname:
            continue
        g0 = gts[0]
        items = "".join(
            f'<li><a href="{up}tasks/{t["slug"]}.html"><span>{e(t["task"])}</span>'
            f'<span class="pill ph-{PHASE_KEY[t["phase"]]}">{e(t["phase"])}</span></a></li>' for t in gts)
        gsec += f"""<section class="group"><h2>{e(gname)}</h2>
<div class="duo duo-sm">
  <div class="card"><h3>{ic("why", up)}Why it matters</h3><p>{e(g0['why_it_matters'])}</p></div>
  <div class="card"><h3>{ic("how", up)}Our method</h3><p>{e(g0['beyond_klean_method'])}</p></div>
</div>
<ul class="tasklist">{items}</ul></section>"""
    aelc = ""
    if ftasks and ftasks[0]["aelc_feed"]:
        aelc = (f'<div class="aelc wide"><strong>Above Eye Level Cleaning.</strong> Construction gets the overhead '
                f'clean once. Our sister brand keeps it clean with scheduled high dusting for stores, warehouses '
                f'and food facilities. <a href="{AELC_URL}" rel="noopener">Visit AboveEyeLevelCleaning.com</a></div>')
    prev_f, next_f = fams[idx - 1], fams[(idx + 1) % len(fams)]
    body = f"""
<div class="band band-white fam-top"><section class="wrap fam-hero">
  <div class="fam-head">{ic(FAMILY_ICON[fname], up, "ic fam-ic")}<div>
    <p class="eyebrow">Service family</p>
    <h1>{e(fname)}</h1>
  </div></div>
  <p class="lede">{e(f['intro'])}</p>
  <p class="task-cta"><a class="btn btn-lg" href="{up}quote.html">Request a Bid</a> <a class="btn btn-ghost" href="#groups">See every service</a></p>
  {aelc}
</section></div>
{'<section class="wrap mid"><h2>The order we clean in</h2>' + graphics.top_down() + '</section>' if f['slug'] == 'overhead-high-dusting' else ''}
<div class="wrap" id="groups">{gsec}</div>
<section class="wrap"><h2>Questions about {e(f['short'].lower())}</h2>{qa_html(f['faq'], 'fq')}
<p><a class="btn btn-ghost" href="{up}faq.html#{f['slug']}">See every {e(f['short'].lower())} question in the FAQ library</a></p></section>
<nav class="wrap pager" aria-label="Families">
  <a href="{up}families/{FAM[prev_f]['slug']}.html">← {e(FAM[prev_f]['short'])}</a>
  <a href="{up}families/{FAM[next_f]['slug']}.html">{e(FAM[next_f]['short'])} →</a>
</nav>
"""
    page(f"families/{f['slug']}.html", f"{fname} | Beyond Klean", f["intro"][:155], body,
         crumbs=[("index.html", "Home"), ("services.html", "Services"), (None, f["short"])],
         schema=[faq_schema(f["faq"])], active="services.html")


# ---------------------------------------------------------------- index pages
def fam_cards(up):
    return "".join(
        f'<a class="fcard" href="{up}families/{FAM[fn]["slug"]}.html">{ic(FAMILY_ICON[fn], up, "ic fc-ic")}'
        f'<strong>{e(FAM[fn]["short"])}</strong><span class="small muted">{e(FAM[fn].get("hint", ""))}</span></a>'
        for fn in fams)


def build_services():
    chips = "".join(f'<button type="button" class="chip" data-filter="{PHASE_KEY[p]}">{e(p)}</button>' for p in PHASE_ORDER)
    chips += "".join(f'<button type="button" class="chip" data-filter="{v}">{e(TIER_LABEL[k])}</button>' for k, v in TIER_KEY.items())
    items = "".join(
        f'<li data-s="{e((t["task"] + " " + t["aliases"] + " " + t["family"]).lower())}" '
        f'data-f="{PHASE_KEY[t["phase"]]} {TIER_KEY[t["tier"]]}"><a href="tasks/{t["slug"]}.html">'
        f'<span>{e(t["task"])}</span><span class="small muted">{e(FAM[t["family"]]["short"])}</span></a></li>'
        for t in sorted(tasks, key=lambda x: x["task"]))
    body = f"""
<section class="wrap">
  <p class="eyebrow">Service directory</p>
  <h1>Find the cleaning service you need</h1>
  <p class="lede">Every cleaning task a construction project can call for, from rough clean to turnover and recurring overhead care. Search by any name your spec or crew uses.</p>
  <h2 class="h3">Browse by type of work</h2>
  <div class="fgrid">{fam_cards('')}</div>
  <h2 class="h3">Browse by facility type</h2>
  <div class="chips hub-chips">{"".join(f'<a class="chip" href="facilities/{f["slug"]}.html">{e(f["name"])}</a>' for f in FACILITY_HUBS)}</div>
  <h2 class="h3">Browse by project phase</h2>
  <div class="chips hub-chips">{"".join(f'<a class="chip" href="phases/{k}.html">{e(lbl)}</a>' for k, _p, lbl, *_ in hubs.PHASES)}</div>
  <div class="filter" data-list="svc">
    <label for="q" class="eyebrow">Search services</label>
    <input id="q" type="search" placeholder="Try “grout haze”, “high dusting” or “FRP”" autocomplete="off">
    <div class="chips"><button type="button" class="chip is-on" data-filter="">All</button>{chips}</div>
    <p class="small muted" aria-live="polite" data-countline hidden><span data-count></span> services shown</p>
  </div>
  <ul class="az" id="svc">{items}</ul>
</section>"""
    page("services.html", "Specialty Cleaning Services Directory | Beyond Klean",
         "Search construction and specialty cleaning services by name, project stage or specialty.",
         body, crumbs=[("index.html", "Home"), (None, "Services")], active="services.html")


def build_faq():
    total = 0
    secs, toc = "", ""
    gen_secs = ""
    for sec, qas in gen_mod.GENERAL_FAQ:
        sid = re.sub(r"[^a-z0-9]+", "-", sec.lower()).strip("-")
        total += len(qas)
        toc += f'<a href="#{sid}">{e(sec)}</a>'
        gen_secs += f'<section class="faqsec" id="{sid}"><h2>{e(sec)}</h2>' + "".join(
            f'<details class="qa" data-s="{e((q + " " + a).lower())}"><summary><h3>{e(q)}</h3></summary><p>{e(a)}</p></details>'
            for q, a in qas) + "</section>"
    for fname in fams:
        f = FAM[fname]
        block = "".join(
            f'<details class="qa" data-s="{e((q + " " + a).lower())}"><summary><h3>{e(q)}</h3></summary><p>{e(a)}</p></details>'
            for q, a in f["faq"])
        n = len(f["faq"])
        for t in (x for x in tasks if x["family"] == fname):
            for i, (q, a) in enumerate(task_qas(t)):
                n += 1
                block += (f'<details class="qa" data-s="{e((q + " " + a + " " + t["task"]).lower())}"><summary><h3>{e(q)}</h3></summary>'
                          f'<p>{e(a)}</p><p class="small"><a href="tasks/{t["slug"]}.html#q{i + 1}">{e(t["task"])} →</a></p></details>')
        total += n
        toc += f'<a href="#{f["slug"]}">{e(f["short"])} <span class="muted">{n}</span></a>'
        secs += f'<section class="faqsec" id="{f["slug"]}"><h2>{e(fname)}</h2>{block}</section>'
    body = f"""
<section class="wrap">
  <p class="eyebrow">FAQ library</p>
  <h1>Construction cleaning questions, answered</h1>
  <p class="lede">Straight answers for general contractors, property managers and building owners. Search any question, or browse by service family. Every task answer links back to its full scope page.</p>
  <div class="filter" data-list="faqall">
    <label for="q" class="eyebrow">Search the library</label>
    <input id="q" type="search" placeholder="Ask it the way you’d say it: “who cleans the ceiling in a new store?”" autocomplete="off">
    <p class="small muted" aria-live="polite" data-countline hidden><span data-count></span> answers shown</p>
  </div>
  <nav class="toc" aria-label="FAQ sections">{toc}</nav>
  <div id="faqall">{gen_secs}{secs}</div>
</section>"""
    all_general = [qa for _, qas in gen_mod.GENERAL_FAQ for qa in qas]
    page("faq.html", "Construction Cleaning FAQ Library | Beyond Klean",
         "Answers about post-construction, overhead, floor, glass, kitchen and specialty cleaning.",
         body, crumbs=[("index.html", "Home"), (None, "FAQ")], schema=[faq_schema(all_general)], active="faq.html")
    return total


def build_glossary():
    items = "".join(
        f'<div class="gterm" id="{s}" data-s="{e((t + " " + d).lower())}"><dt>{e(t)}</dt><dd>{e(d)}</dd></div>'
        for t, s, d in sorted(GLOSS, key=lambda g: g[0].lower()))
    body = f"""<section class="wrap narrow">
<p class="eyebrow">Glossary</p><h1>Construction cleaning terms</h1>
<p class="lede">The words that show up in specs, bid packages and punch lists, defined the way crews and superintendents use them.</p>
<div class="filter" data-list="gl"><label for="q" class="eyebrow">Search terms</label><input id="q" type="search" autocomplete="off">
<p class="small muted" aria-live="polite" data-countline hidden><span data-count></span> terms shown</p></div>
<dl class="gloss" id="gl">{items}</dl></section>"""
    page("glossary.html", "Construction Cleaning Glossary | Beyond Klean",
         "Definitions of rough clean, final clean, FRP, VCT, HEPA, grout haze and other construction cleaning terms.",
         body, crumbs=[("index.html", "Home"), (None, "Glossary")],
         schema=[{"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Construction cleaning glossary",
                  "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, _, d in GLOSS]}])


def build_static(n_faq):
    pages = gen_mod.static_pages(
            n_tasks=len(tasks), n_names=sum(1 + len(t['alias_list']) for t in tasks),
            n_faq=n_faq, fam_cards=fam_cards(""), AELC_URL=AELC_URL,
            phase_counts=[(p, PHASE_KEY[p], sum(1 for t in tasks if t["phase"] == p)) for p in PHASE_ORDER],
            task_options="", phone=PHONE)
    pages += [TRUST.projects_page(), TRUST.capability_page(), TRUST.safety_page(), TRUST.contact_page()]
    gi = lambda n: ic(n, "")
    mlinks = ["facilities/multifamily.html", "facilities/office.html", "facilities/industrial.html", "facilities/education.html",
              "facilities/government.html", "families/government-military-defense.html"]
    markets = "".join(f'<a class="mcard" href="{h}">{gi(i)}<strong>{e(n)}</strong><span class="small muted">{e(d)}</span></a>'
                      for (n, d), i, h in zip(gen_mod.MARKETS, ["house", "office", "factory", "school", "capitol", "military"], mlinks))
    proof = TRUST.quotes_block() + TRUST.clients_block()
    blocks = {"<!--CRED-->": TRUST.cred_strip(), "<!--FEATURED-->": TRUST.featured(),
              "<!--PROOF-->": f'<div class="band band-white">{proof}</div>' if proof else "",
              "<!--LEADERSHIP-->": TRUST.leadership_block(),
              "<!--MARKETS-->": f'<div class="mgrid">{markets}</div>', "<!--TIMELINE-->": graphics.three_cleans(gi),
              "<!--PROCESS-->": graphics.process(gi), "<!--VERSUS-->": graphics.capture_vs_move(gi),
              "<!--TOPDOWN-->": graphics.top_down(), "<!--MISSED-->": graphics.commonly_missed(),
              "<!--CLOSEOUT-->": graphics.closeout(gi)}
    for path, title, desc, crumb, html_body, active in pages:
        for k, v in blocks.items():
            html_body = html_body.replace(k, v)
        page(path, title, desc, html_body,
             crumbs=None if path == "index.html" else [("index.html", "Home"), (None, crumb)],
             schema=[TRUST.org_schema(SITE_URL),
                     {"@context": "https://schema.org", "@type": "WebSite", "name": "Beyond Klean", "url": SITE_URL}]
             if path == "index.html" else None, active=active)


# ---------------------------------------------------------------- hub pages: facility types, phases, where we work, government
FACILITY_HUBS = []
for _slug, _name, _icon, _intro, _fams, _kw, _faq in hubs.FACILITIES:
    _rx = re.compile(_kw, re.I)
    _ts = [t["task"] for t in tasks if t["family"] in _fams or _rx.search(t["task"] + " " + t["group"])]
    _ts = list(dict.fromkeys(hubs.CORE + _ts))
    FACILITY_HUBS.append(dict(slug=_slug, name=_name, icon=_icon, intro=_intro, faq=_faq, tasks=_ts))
TASK_BY_NAME = {t["task"]: t for t in tasks}


def task_groups_html(names, up):
    by = defaultdict(list)
    for n in names:
        t = TASK_BY_NAME.get(n)
        if t:
            by[t["family"]].append(t)
    return "".join(
        f'<section class="group"><h2>{ic(FAMILY_ICON[fn], up)} <a href="{up}families/{FAM[fn]["slug"]}.html">{e(FAM[fn]["short"])}</a></h2>'
        f'<ul class="tasklist">' + "".join(
            f'<li><a href="{up}tasks/{t["slug"]}.html"><span>{e(t["task"])}</span>'
            f'<span class="pill ph-{PHASE_KEY[t["phase"]]}">{e(t["phase"])}</span></a></li>' for t in ts) + "</ul></section>"
        for fn, ts in sorted(by.items(), key=lambda kv: fams.index(kv[0])))


def build_hubs():
    up = "../"
    for d in ("facilities", "phases"):
        shutil.rmtree(SITE / d, ignore_errors=True)
    cards = ""
    for f in FACILITY_HUBS:
        cards += (f'<a class="fcard" href="{f["slug"]}.html">{ic(f["icon"], up, "ic fc-ic")}<strong>{e(f["name"])}</strong>'
                  f'<span class="small muted">{len(f["tasks"])} services</span></a>')
        body = f"""
<div class="band band-white fam-top"><section class="wrap fam-hero">
  <div class="fam-head">{ic(f['icon'], up, "ic fam-ic")}<div><p class="eyebrow">Facility type</p><h1>{e(f['name'])}</h1></div></div>
  <p class="lede">{e(f['intro'])}</p>
  <p class="task-cta"><a class="btn btn-lg" href="{up}quote.html">Request a Bid</a> <a class="btn btn-ghost" href="#services">Services for this building type</a></p>
</section></div>
<section class="wrap mid"><h2>Questions about {e(f['name'].lower())}</h2>{qa_html(f['faq'], 'fq')}</section>
<div class="wrap" id="services">{task_groups_html(f['tasks'], up)}</div>
<section class="wrap"><p><a class="btn btn-ghost" href="index.html">All facility types</a> <a class="btn btn-ghost" href="{up}phases/index.html">Browse by project phase</a></p></section>"""
        page(f"facilities/{f['slug']}.html", f"{f['name']} Construction Cleaning | Beyond Klean", f["intro"][:155], body,
             crumbs=[("index.html", "Home"), ("facilities/index.html", "Facility types"), (None, f["name"])],
             schema=[faq_schema(f["faq"])], active="services.html")
    page("facilities/index.html", "Construction Cleaning by Facility Type | Beyond Klean",
         "Construction cleaning services by building type: offices, retail, restaurants, warehouses, plants, healthcare, schools, housing, hotels, labs, government and infrastructure.",
         f"""<section class="wrap"><p class="eyebrow">Facility types</p><h1>Construction cleaning by building type</h1>
<p class="lede">Every building type has its own cleaning scope, schedule and rules. Pick yours to see the services that apply and the questions owners and contractors ask most.</p>
<div class="fgrid">{cards}</div></section>""",
         crumbs=[("index.html", "Home"), (None, "Facility types")], active="services.html")

    pcards = ""
    for k, phase, label, intro, when, spec in hubs.PHASES:
        pts = [t["task"] for t in tasks if t["phase"] == phase]
        pcards += (f'<a class="fcard" href="{k}.html"><strong>{e(label)}</strong>'
                   f'<span class="small muted">{e(when)}</span></a>')
        body = f"""
<div class="band band-white fam-top"><section class="wrap fam-hero">
  <p class="eyebrow">Project phase</p><h1>{e(label)}</h1>
  <p class="lede">{e(intro)}</p>
  {graphics.phase_strip(k)}
  <dl class="facts phase-facts"><div><dt>When it happens</dt><dd>{e(when)}</dd></div><div><dt>Typical spec section</dt><dd class="mono">{e(spec)}</dd></div></dl>
  <p class="task-cta"><a class="btn btn-lg" href="{up}quote.html">Request a Bid</a></p>
</section></div>
<section class="wrap mid"><h2>Where this fits in the schedule</h2>{graphics.three_cleans(lambda n: ic(n, up))}</section>
<div class="wrap">{task_groups_html(pts, up)}</div>
<section class="wrap"><p><a class="btn btn-ghost" href="index.html">All project phases</a> <a class="btn btn-ghost" href="{up}facilities/index.html">Browse by facility type</a></p></section>"""
        page(f"phases/{k}.html", f"{label} Services | Beyond Klean", intro[:155], body,
             crumbs=[("index.html", "Home"), ("phases/index.html", "Project phases"), (None, label)], active="services.html")
    page("phases/index.html", "Construction Cleaning by Project Phase | Beyond Klean",
         "Construction cleaning by phase: progress, rough, final, touch-up and punch, turnover, recurring and specialty.",
         f"""<section class="wrap"><p class="eyebrow">Project phases</p><h1>Construction cleaning by project phase</h1>
<p class="lede">Construction cleaning runs with the schedule. Each phase has its own scope, spec section and timing, and one bid can cover all of them.</p>
{graphics.three_cleans(lambda n: ic(n, up))}<div class="fgrid">{pcards}</div></section>""",
         crumbs=[("index.html", "Home"), (None, "Project phases")], active="services.html")

    # Where we work
    C = company_mod.COMPANY
    body = f"""
<section class="wrap"><p class="eyebrow">Where we work</p><h1>Construction cleaning nationwide</h1>
<p class="lede">We take projects anywhere in the United States. Home crews cover the Southeast, and travel crews mobilize for larger scopes in every other state. Send the city, ZIP code and size, and we confirm crew availability before we bid.</p>
<div class="split map-split"><div><h2 class="h3">Home crews and completed projects</h2>{TRUST.us_map()}</div>
<div class="panel"><h2 class="h3">How travel crews work</h2>
<ul class="check"><li>A crew lead and core team travel to the site, sized to the schedule.</li>
<li>Lodging, per diem and mobilization are shown as their own lines on the bid.</li>
<li>Local labor can be added under our supervision for very large scopes.</li>
<li>The same methods, checklists and closeout documents as our home crews.</li></ul>
<p><a class="btn" href="quote.html">Request a Bid</a></p></div></div>
<h2>Service area</h2><p>{e(C['service_area'])}</p>
<p>See the <a href="projects.html">projects</a> we have completed, or browse services by <a href="facilities/index.html">facility type</a> and <a href="phases/index.html">project phase</a>.</p>
</section>"""
    page("where-we-work.html", "Where We Work | Beyond Klean", "Construction cleaning nationwide: home crews in the Southeast and travel crews for larger projects in every state.",
         body, crumbs=[("index.html", "Home"), (None, "Where we work")])

    # Government contracting and procurement hub
    items = "".join(f'<div class="card"><h3>{ic("doc", "")}{e(h)}</h3><p>{e(d)}</p></div>' for h, d in hubs.GOV_PROCUREMENT)
    naics = "".join(f"<li><span class='mono'>{e(c)}</span> {e(d)}</li>" for c, d in C["naics"])
    gfam = "Government, Military & Defense Facility Cleaning"
    gsvc = [t for t in tasks if t["family"] == gfam]
    body = f"""
<div class="band band-white fam-top"><section class="wrap fam-hero">
  <div class="fam-head">{ic("capitol", "", "ic fam-ic")}<div><p class="eyebrow">Government contracting and procurement</p><h1>Government, military and defense facility cleaning</h1></div></div>
  <p class="lede">Construction and renovation cleaning for federal, state, municipal and military facilities, performed by our crews under the prime contractor's site plan and the facility's access rules. Send us your solicitation or bid package and we respond with an itemized bid and a capability statement.</p>
  <p class="task-cta"><a class="btn btn-lg" href="#rfp">Send us an RFP</a> <a class="btn btn-ghost" href="capability-statement.html">Capability statement</a> <a class="btn btn-ghost" href="families/government-military-defense.html">All government services</a></p>
</section></div>
<section class="wrap"><h2>How we work with government buyers</h2><div class="duo gov-grid">{items}</div></section>
<div class="band band-soft"><section class="wrap split">
  <div><h2>NAICS codes</h2><ul class="codes">{naics}</ul>
  <p class="small">Registrations such as SAM.gov UEI and CAGE are listed on the <a href="capability-statement.html">capability statement</a> once verified.</p></div>
  <div class="panel"><h2 class="h3">What we never claim</h2><p>We do not claim security clearances, facility clearances, certifications, set-aside status or contract vehicles we have not verified. Restricted-access, hazardous-material and defense-related work is performed only by appropriately qualified and authorized personnel, arranged with the prime contractor and the facility.</p></div>
</section></div>
<section class="wrap"><h2>Government and military services</h2>{task_groups_html([t["task"] for t in gsvc], "")}</section>
<section class="wrap narrow" id="rfp"><h2>Send us an RFP or bid package</h2>
<form class="form panel" data-demo>
  <div class="row"><label for="g-sol">Solicitation or project number<input id="g-sol" name="solicitation"></label>
  <label for="g-due">Bid due date<input id="g-due" type="date" name="due"></label></div>
  <div class="row"><label for="g-agency">Agency or prime contractor<input id="g-agency" name="agency"></label>
  <label for="g-loc">Location (city, state, ZIP)<input id="g-loc" name="location"></label></div>
  <div class="row"><label for="g-role">Our role<select id="g-role" name="role"><option>Subcontractor to the prime</option><option>Prime contractor</option><option>Not sure yet</option></select></label>
  <label for="g-sf">Approximate square feet<input id="g-sf" name="sqft" inputmode="numeric"></label></div>
  <label for="g-scope">Scope summary<textarea id="g-scope" name="scope" placeholder="Phases, buildings, access or security requirements, wage determination"></textarea></label>
  <label for="g-files">Solicitation documents<input id="g-files" type="file" name="files" multiple></label>
  <div class="row"><label for="g-name">Your name<input id="g-name" name="name" required></label>
  <label for="g-email">Email<input id="g-email" type="email" name="email" required></label></div>
  <button class="btn" type="submit">Send RFP</button>
  <div class="notice" tabindex="-1" hidden><p><strong>Received. Reference <span class="mono" data-ref></span>.</strong> We'll confirm availability and respond before your due date.</p><p class="small">Preview build: requests aren't sent yet.</p></div>
</form></section>"""
    page("government.html", "Government and Military Facility Cleaning | Beyond Klean",
         "Construction cleaning for federal, state, municipal and military facilities. Send an RFP, see NAICS codes and how access and security are handled.",
         body, crumbs=[("index.html", "Home"), (None, "Government")], active="government.html")


# ---------------------------------------------------------------- estimator (internal, unlinked)
def build_estimator():
    up = "../"
    est = load("est_data")
    routine_mod = load("routine")
    BILLED = {"general": 42, "tech": 55, "lift": 70, "specialist": 70, "lead": 55}
    rows_pb = []
    for t in sorted(tasks, key=lambda x: x["task"]):
        pb = PRICEBOOK.get(t["task"], {})
        role = "specialist" if t["tier"] == "Conditional / regulated" else est.FAMILY_ROLE.get(t["family"], "general")
        mid = pb.get("mid", 0)
        rate = pb.get("rate_per_hr") or (1 if pb.get("unit") == "hour" else round(BILLED[role] / (mid * .6), 3) if mid else 0)
        mat = round(mid * est.MATERIAL_SHARE.get(t["family"], .05), 4)
        scope = (t["c"] or {}).get("s", [])
        rows_pb.append([t["task"], FAM[t["family"]]["short"], pb.get("unit", "sqft"), pb.get("low", 0), mid,
                        pb.get("high", 0), pb.get("min", 0), pb.get("basis", ""), pb.get("confidence", ""),
                        t["alias_list"], t["phase"], rate, mat, role, scope])
    names = {r[0] for r in rows_pb} | {r[0] for r in routine_mod.ROUTINE}
    for name, mode, lines in est.TEMPLATES:
        bad = [l[0] for l in lines if l[0] not in names]
        assert not bad, f"template {name}: unknown tasks {bad}"
    units = {**UNIT_LABEL, "flight": "Flight of stairs", "month": "Month"}
    # The price book ships encrypted (AES-GCM, key from the password via PBKDF2), so the rates stay
    # locked even though the files sit on a plain static host. The page decrypts it after login.
    plain = json.dumps({"meta": PRICING.get("meta", {}), "units": units, "items": rows_pb,
                        "routine": [list(r) for r in routine_mod.ROUTINE], "freq": routine_mod.FREQ,
                        "roles": est.ROLES, "equipment": est.EQUIPMENT, "templates": est.TEMPLATES},
                       ensure_ascii=False, separators=(",", ":")).encode()
    salt, iv, iters = os.urandom(16), os.urandom(12), 200_000
    key = hashlib.pbkdf2_hmac("sha256", ESTIMATOR_PASSWORD.encode(), salt, iters, 32)
    ct = AESGCM(key).encrypt(iv, plain, None)
    b64 = lambda b: base64.b64encode(b).decode()
    (SITE / "estimator" / "pricebook.enc.js").parent.mkdir(parents=True, exist_ok=True)
    (SITE / "estimator" / "pricebook.enc.js").write_text(
        "window.BK_PB_ENC=" + json.dumps({"salt": b64(salt), "iv": b64(iv), "iter": iters, "ct": b64(ct)}) + ";\n")
    (SITE / "assets" / "pricebook.js").unlink(missing_ok=True)
    body = (CONTENT / "estimator.html").read_text()
    (SITE / "estimator" / "index.html").write_text(  # old address forwards to /estimator.html
        '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
        '<meta http-equiv="refresh" content="0; url=../estimator.html"><title>Estimator</title>'
        '<a href="../estimator.html">Open the estimator</a>\n')
    page("estimator.html", "Estimator | Beyond Klean", "Internal estimating tool.", body,
         extra_js='<script src="estimator/pricebook.enc.js"></script><script src="estimator/estimator.js"></script>',
         robots="noindex, nofollow, noarchive")


# ---------------------------------------------------------------- checks
def shingles(s, k=5):
    w = re.findall(r"[a-z0-9]+", s.lower())
    return {" ".join(w[i:i + k]) for i in range(max(0, len(w) - k + 1))}


def similarity_report():
    sh = {}
    for t in tasks:
        if t["c"]:
            c = t["c"]
            sh[t["task"]] = shingles(" ".join([c["a"], c["y"], c["m"]] + c["s"] + c["w"] + [q + " " + a for q, a in c["q"]]))
    worst = []
    for a, b in combinations(sh, 2):
        if sh[a] and sh[b]:
            j = len(sh[a] & sh[b]) / len(sh[a] | sh[b])
            if j > 0.05:
                worst.append((round(j, 3), a, b))
    return sorted(worst, reverse=True)[:10]


def check_links():
    bad = []
    for p in SITE.rglob("*.html"):
        for href in re.findall(r'href="([^"#?:]+\.(?:html|css|png))', p.read_text()):
            if not (p.parent / href).resolve().exists():
                bad.append((str(p.relative_to(SITE)), href))
    return bad


if __name__ == "__main__":
    for d in ("tasks", "families"):
        shutil.rmtree(SITE / d, ignore_errors=True)
    for t in tasks:
        build_task(t)
    for i, fn in enumerate(fams):
        build_family(fn, i)
    build_services()
    n_faq = build_faq()
    build_glossary()
    build_static(n_faq)
    build_hubs()
    build_estimator()
    (SITE / "assets" / "icons.svg").write_text(icons_mod.sprite())
    (SITE / "join.html").unlink(missing_ok=True)  # contractor network page retired
    # type-ahead index for the "What needs cleaning?" finder: name, other names, family, url
    POPULAR = {"Final clean of entire building": 12, "Rough clean of entire building": 10, "Open ceiling deck cleaning": 12,
               "Grout haze removal": 10, "Interior window cleaning": 8, "Exterior window cleaning": 6, "VCT initial floor finish": 8,
               "Commercial kitchen post-construction clean": 8, "Fine drywall dust removal from all horizontal surfaces": 8,
               "Touch-up clean before owner walk": 6, "Store opening clean": 6, "Warehouse post-construction cleaning": 6,
               "Sidewalk pressure washing": 6, "Carpet extraction": 6, "Quarterly high dusting program": 6, "Duct exterior cleaning": 6}
    EXTRA = {"Open ceiling deck cleaning": ["ceiling dust", "open ceiling cleaning", "high ceiling dusting"],
             "Fine drywall dust removal from all horizontal surfaces": ["construction dust cleaning", "dust removal"],
             "Final clean of entire building": ["post construction cleaning", "construction clean up"],
             "Interior window cleaning": ["window washing"], "Sidewalk pressure washing": ["power washing"]}
    TIERW = {"Core": 3, "Adjacent specialist": 1, "Conditional / regulated": 0}
    idx = [[t["task"], t["alias_list"], FAM[t["family"]]["short"], f"tasks/{t['slug']}.html",
            TIERW[t["tier"]] + POPULAR.get(t["task"], 0), EXTRA.get(t["task"], [])] for t in tasks]
    idx += [[FAM[fn]["short"], [], "Service family", f"families/{FAM[fn]['slug']}.html", 2, [fn]] for fn in fams]
    (SITE / "assets" / "search-index.js").write_text("window.BK_INDEX=" + json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (SITE / "robots.txt").write_text("# Preview build: keep out of search until launch\nUser-agent: *\nDisallow: /\n")
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE_URL}/{p.relative_to(SITE).as_posix()}</loc></url>\n"
                for p in sorted(SITE.rglob("*.html")) if p.parts[-2] != "estimator" and p.name != "estimator.html") + "</urlset>\n")
    # artifact copy of the home page: the artifact host supplies its own document skeleton
    home = (SITE / "index.html").read_text()
    head = re.search(r"<head>(.*?)</head>", home, re.S).group(1)
    head = re.sub(r'<meta (charset|name="viewport")[^>]*>\n?', "", head)
    bodyh = re.search(r"<body>(.*?)</body>", home, re.S).group(1)
    (ROOT / "artifact-index.html").write_text(head + bodyh)

    print(f"tasks: {len(tasks)}  with content: {len(tasks) - len(missing)}  missing: {len(missing)}")
    if unknown:
        print("content keys not matching a task:", unknown)
    print("FAQ answers:", n_faq)
    print("html files:", len(list(SITE.rglob("*.html"))))
    bad = check_links()
    print("broken links:", len(bad), bad[:5])
    print("most similar task pairs (5-word shingle Jaccard):")
    for row in similarity_report():
        print("  ", row)
