"""Beyond Klean static site generator.

Reads research/tasks.json + content/*.py and writes plain HTML to site/.
Every page is a standalone .html file with relative links, so the folder can be
uploaded to any static host as-is.

    python3 build_site.py
"""
import html, importlib.util, json, re, shutil
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).parent
SITE = ROOT / "site"
CONTENT = ROOT / "content"
AELC_URL = "https://aboveeyelevelcleaning.com"
SITE_URL = "https://beyondklean.com"

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
FAM = fam_mod.F  # family name -> dict(slug, short, intro, faq)

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
TIER_NOTE = {
    "Core": "Routed to verified construction cleaning contractors.",
    "Adjacent specialist": "Routed only to contractors verified for this specialty and equipment.",
    "Conditional / regulated": "Licensed or protocol-driven work. Reviewed and approved case by case before any contractor is introduced.",
}

GLOSS = gen_mod.GLOSSARY  # list of (term, slug, definition)


# ---------------------------------------------------------------- layout
NAV = [("services.html", "Services"), ("faq.html", "FAQ"), ("methods.html", "Our Methods"),
       ("general-contractors.html", "For GCs"), ("join.html", "Join the Network")]


def page(path, title, desc, body, crumbs=None, schema=None, active=None):
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
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                 for s in (schema or []))
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
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
    <nav class="mainnav" aria-label="Main">{nav}<a class="btn btn-sm" href="{up}quote.html">Request a Quote</a></nav>
  </div>
</header>
<main id="main">
{bcw}
{body}
</main>
<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <img class="logo-l foot-logo" src="{up}assets/logo.png" alt="Beyond Klean" width="634" height="243">
      <img class="logo-d foot-logo" src="{up}assets/logo-dark.png" alt="" width="634" height="243">
      <p class="small">Beyond Klean helps builders and owners scope specialty cleaning and connects them with independent, verified contractors. The contractor that quotes the work performs, insures and warrants it.</p>
    </div>
    <div><h2 class="foot-h">Find work</h2>
      <a href="{up}services.html">All {len(tasks)} services</a><a href="{up}faq.html">FAQ library</a><a href="{up}glossary.html">Glossary</a><a href="{up}methods.html">Our methods</a></div>
    <div><h2 class="foot-h">Work with us</h2>
      <a href="{up}quote.html">Request a quote</a><a href="{up}quote.html#bid">Submit a bid package</a><a href="{up}join.html">Join the contractor network</a><a href="{up}general-contractors.html">For general contractors</a><a href="{up}about.html">About Beyond Klean</a></div>
    <div><h2 class="foot-h">Above eye level</h2>
      <a href="{up}families/{FAM[fams[3]]['slug']}.html">Overhead &amp; high dusting</a><a href="{AELC_URL}" rel="noopener">AboveEyeLevelCleaning.com</a></div>
  </div>
  <div class="wrap small foot-note">© 2026 Beyond Klean. Service descriptions are educational and do not represent that any single contractor performs every service. Availability depends on verified contractor coverage.</div>
</footer>
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
                    f"point to the same scope, so a request under any of them reaches the same qualified contractors."))
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
                f'Recurring high dusting for this surface is handled through our partner program at '
                f'<a href="{AELC_URL}" rel="noopener">AboveEyeLevelCleaning.com</a>.</div>')

    also = (f'<p class="also"><span class="eyebrow">Also called</span> {e("; ".join(t["alias_list"]))}</p>'
            if t["alias_list"] else "")
    body = f"""
<article class="wrap task" data-phase="{phase_k}">
  <div class="task-main">
    <p class="eyebrow"><a href="{up}families/{fam['slug']}.html">{e(t['family'])}</a> · {e(t['group'])}</p>
    <h1>{e(t['task'])}</h1>
    <p class="lede">{e(c['a'])}</p>
    {also}
    <section><h2>Why it matters</h2><p>{e(c['y'])}</p></section>
    <section><h2>How we approach it</h2><p>{e(c['m'])}</p>
      <p class="small">Methods follow our <a href="{up}methods.html">capture-first, least-aggressive-chemistry standard</a>.</p></section>
    <section><h2>Scope checklist for your bid</h2><ul class="check">{"".join(f"<li>{e(x)}</li>" for x in c['s'])}</ul></section>
    <section><h2>Watch-outs</h2><ul class="warn">{"".join(f"<li>{e(x)}</li>" for x in c['w'])}</ul></section>
    {aelc}
    <section id="questions"><h2>Questions about {e(t['task'].lower())}</h2>{qa_html(qas, 'q')}</section>
    {terms_html}
  </div>
  <aside class="spec" aria-label="Scope summary">
    <dl>
      <div><dt>Scope ID</dt><dd class="mono">{e(t['id'])}</dd></div>
      <div><dt>Project stage</dt><dd><a class="pill ph-{phase_k}" href="{up}services.html#{phase_k}">{e(t['phase'])}</a></dd></div>
      <div><dt>Typical spec section</dt><dd class="mono">{e(PHASE_SPEC[t['phase']])}</dd></div>
      <div><dt>Contractor routing</dt><dd><span class="pill tier-{tier_k}">{e(t['tier'])}</span><span class="small block">{e(TIER_NOTE[t['tier']])}</span></dd></div>
    </dl>
    <a class="btn" href="{up}quote.html?task={t['id']}">Request a scope review</a>
    <a class="btn btn-ghost" href="{up}quote.html#bid">Send a bid package</a>
  </aside>
</article>
<section class="wrap related"><h2>Related work</h2><div class="rel-grid">{rel_html}</div></section>
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
<div class="group-why"><p><strong>Why it matters.</strong> {e(g0['why_it_matters'])}</p>
<p><strong>Our method.</strong> {e(g0['beyond_klean_method'])}</p></div>
<ul class="tasklist">{items}</ul></section>"""
    aelc = ""
    if ftasks and ftasks[0]["aelc_feed"]:
        aelc = (f'<div class="aelc wide"><strong>Above Eye Level Cleaning.</strong> Construction gets the overhead '
                f'clean once. Our partner program keeps it clean with scheduled high dusting for stores, warehouses '
                f'and food facilities. <a href="{AELC_URL}" rel="noopener">Visit AboveEyeLevelCleaning.com</a></div>')
    prev_f, next_f = fams[idx - 1], fams[(idx + 1) % len(fams)]
    body = f"""
<section class="wrap fam-hero">
  <p class="eyebrow">Service family {idx + 1} of {len(fams)} · {len(ftasks)} tasks</p>
  <h1>{e(fname)}</h1>
  <p class="lede">{e(f['intro'])}</p>
  {aelc}
</section>
<div class="wrap">{gsec}</div>
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
        f'<a class="fcard" href="{up}families/{FAM[fn]["slug"]}.html"><span class="mono small">{i + 1:02d}</span>'
        f'<strong>{e(FAM[fn]["short"])}</strong><span class="small">{sum(1 for t in tasks if t["family"] == fn)} tasks</span></a>'
        for i, fn in enumerate(fams))


def build_services():
    chips = "".join(f'<button type="button" class="chip" data-filter="{PHASE_KEY[p]}">{e(p)}</button>' for p in PHASE_ORDER)
    chips += "".join(f'<button type="button" class="chip" data-filter="{v}">{e(k)}</button>' for k, v in TIER_KEY.items())
    items = "".join(
        f'<li data-s="{e((t["task"] + " " + t["aliases"] + " " + t["family"]).lower())}" '
        f'data-f="{PHASE_KEY[t["phase"]]} {TIER_KEY[t["tier"]]}"><a href="tasks/{t["slug"]}.html">'
        f'<span>{e(t["task"])}</span><span class="small muted">{e(FAM[t["family"]]["short"])}</span></a></li>'
        for t in sorted(tasks, key=lambda x: x["task"]))
    body = f"""
<section class="wrap">
  <p class="eyebrow">Service directory</p>
  <h1>All {len(tasks)} specialty cleaning services</h1>
  <p class="lede">Every cleaning task a construction project can call for, from rough clean to turnover and recurring overhead care. Search by any name your spec or crew uses. We index {sum(1 + len(t['alias_list']) for t in tasks)} of them.</p>
  <h2 class="h3">Browse by family</h2>
  <div class="fgrid">{fam_cards('')}</div>
  <div class="filter" data-list="svc">
    <label for="q" class="eyebrow">Search services</label>
    <input id="q" type="search" placeholder="Try “grout haze”, “high dusting” or “FRP”" autocomplete="off">
    <div class="chips"><button type="button" class="chip is-on" data-filter="">All</button>{chips}</div>
    <p class="small muted" aria-live="polite"><span data-count>{len(tasks)}</span> services shown</p>
  </div>
  <ul class="az" id="svc">{items}</ul>
</section>"""
    page("services.html", "Specialty Cleaning Services Directory | Beyond Klean",
         f"Search all {len(tasks)} construction and specialty cleaning services by name, stage or specialty.",
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
  <h1>{total:,} answers about construction and specialty cleaning</h1>
  <p class="lede">Straight answers for general contractors, owners, facility managers and cleaning crews. Search any question, or browse by service family. Every task answer links back to its full scope page.</p>
  <div class="filter" data-list="faqall">
    <label for="q" class="eyebrow">Search the library</label>
    <input id="q" type="search" placeholder="Ask it the way you’d say it: “who cleans the ceiling in a new store?”" autocomplete="off">
    <p class="small muted" aria-live="polite"><span data-count>{total:,}</span> answers shown</p>
  </div>
  <nav class="toc" aria-label="FAQ sections">{toc}</nav>
  <div id="faqall">{gen_secs}{secs}</div>
</section>"""
    all_general = [qa for _, qas in gen_mod.GENERAL_FAQ for qa in qas]
    page("faq.html", "Construction Cleaning FAQ Library | Beyond Klean",
         f"{total:,} answers about post-construction, overhead, floor, glass, kitchen and specialty cleaning.",
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
<p class="small muted" aria-live="polite"><span data-count>{len(GLOSS)}</span> terms shown</p></div>
<dl class="gloss" id="gl">{items}</dl></section>"""
    page("glossary.html", "Construction Cleaning Glossary | Beyond Klean",
         "Definitions of rough clean, final clean, FRP, VCT, HEPA, grout haze and other construction cleaning terms.",
         body, crumbs=[("index.html", "Home"), (None, "Glossary")],
         schema=[{"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Construction cleaning glossary",
                  "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, _, d in GLOSS]}])


def build_static(n_faq):
    for path, title, desc, crumb, html_body, active in gen_mod.static_pages(
            n_tasks=len(tasks), n_names=sum(1 + len(t['alias_list']) for t in tasks),
            n_faq=n_faq, fam_cards=fam_cards(""), AELC_URL=AELC_URL,
            phase_counts=[(p, PHASE_KEY[p], sum(1 for t in tasks if t["phase"] == p)) for p in PHASE_ORDER],
            task_options="".join(f'<option value="{t["id"]}">{e(t["task"])}</option>'
                                 for t in sorted(tasks, key=lambda x: x["task"]))):
        page(path, title, desc, html_body,
             crumbs=None if path == "index.html" else [("index.html", "Home"), (None, crumb)],
             schema=[{"@context": "https://schema.org", "@type": "Organization", "name": "Beyond Klean",
                      "url": SITE_URL, "logo": f"{SITE_URL}/assets/logo.png"},
                     {"@context": "https://schema.org", "@type": "WebSite", "name": "Beyond Klean", "url": SITE_URL}]
             if path == "index.html" else None, active=active)


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
    (SITE / "robots.txt").write_text("# Preview build: keep out of search until launch\nUser-agent: *\nDisallow: /\n")
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE_URL}/{p.relative_to(SITE).as_posix()}</loc></url>\n"
                for p in sorted(SITE.rglob("*.html"))) + "</urlset>\n")
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
