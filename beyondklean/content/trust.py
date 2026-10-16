"""Trust pages and blocks: projects, capability statement, safety and compliance, contact.

All facts come from content/company.py. Empty facts render as a "Pending" marker in preview
(SHOW_SLOTS) and disappear at launch, so nothing unverified is ever stated as fact.
"""
from html import escape
import re

e = lambda s: escape(str(s), quote=True)

# Tile-grid map of the U.S.: state -> (column, row)
TILES = {
    "AK": (0, 0), "ME": (11, 0), "VT": (10, 1), "NH": (11, 1),
    "WA": (1, 2), "ID": (2, 2), "MT": (3, 2), "ND": (4, 2), "MN": (5, 2), "IL": (6, 2), "WI": (7, 2), "MI": (8, 2), "NY": (9, 2), "RI": (10, 2), "MA": (11, 2),
    "OR": (1, 3), "NV": (2, 3), "WY": (3, 3), "SD": (4, 3), "IA": (5, 3), "IN": (6, 3), "OH": (7, 3), "PA": (8, 3), "NJ": (9, 3), "CT": (10, 3),
    "CA": (1, 4), "UT": (2, 4), "CO": (3, 4), "NE": (4, 4), "MO": (5, 4), "KY": (6, 4), "WV": (7, 4), "VA": (8, 4), "MD": (9, 4), "DE": (10, 4),
    "AZ": (2, 5), "NM": (3, 5), "KS": (4, 5), "AR": (5, 5), "TN": (6, 5), "NC": (7, 5), "SC": (8, 5), "DC": (9, 5),
    "OK": (4, 6), "LA": (5, 6), "MS": (6, 6), "AL": (7, 6), "GA": (8, 6),
    "HI": (0, 7), "TX": (4, 7), "FL": (9, 7),
}


class Trust:
    def __init__(self, company_mod, task_slug):
        self.m = company_mod
        self.C = company_mod.COMPANY
        self.slots = company_mod.SHOW_SLOTS
        self.task_slug = task_slug  # task name -> slug
        real = [dict(p, sample=False) for p in company_mod.PROJECTS]
        samples = [dict(p, sample=True) for p in company_mod.SAMPLE_PROJECTS] if self.slots else []
        self.projects = real + samples
        for p in self.projects:
            bad = [t for t in p.get("tasks", []) if t not in task_slug]
            if bad:
                print(f"project {p['slug']}: unknown service names {bad}")
            p["tasks"] = [t for t in p.get("tasks", []) if t in task_slug]

    # ------------------------------------------------------------ helpers
    def pending(self, label="Pending"):
        return f'<span class="pending">{e(label)}</span>' if self.slots else ""

    def fact(self, value, label="Pending"):
        return e(value) if value else self.pending(label)

    def rows(self, pairs):
        """(label, value) rows; empty values become Pending (preview) or are dropped (launch)."""
        out = ""
        for k, v in pairs:
            if v or self.slots:
                out += f"<div><dt>{e(k)}</dt><dd>{self.fact(v)}</dd></div>"
        return out

    def phone_link(self, cls=""):
        ph = self.C["phone"]
        if not ph:
            return self.pending("Phone pending")
        tel = "".join(c for c in ph if c.isdigit() or c == "+")
        return f'<a class="{cls}" href="tel:{tel}">{e(ph)}</a>'

    def email_link(self):
        em = self.C["email"]
        return f'<a href="mailto:{e(em)}">{e(em)}</a>' if em else self.pending("Email pending")

    # ------------------------------------------------------------ before / after slider
    def slider(self, p, up):
        ph = p.get("photos") or {}
        def img(stage, alt):
            if ph.get(stage):
                return f'<img src="{up}assets/projects/{e(ph[stage])}" alt="{e(alt)}" loading="lazy">'
            return f'<div class="ph ph-{stage}"><span>{stage.title()} photo</span></div>'
        during = ""
        if ph.get("during") or p.get("sample"):
            during = (f'<div class="ba-during" hidden>{img("during", p["title"] + ", during")}</div>'
                      f'<div class="ba-tabs"><button type="button" class="chip is-on" data-ba-view="compare">Before / after</button>'
                      f'<button type="button" class="chip" data-ba-view="during">During</button></div>')
        return f"""<div class="ba" data-ba>
  <div class="ba-stage" style="--pos:50%">
    <div class="ba-img">{img("before", p["title"] + ", before")}</div>
    <div class="ba-img ba-after">{img("after", p["title"] + ", after")}</div>
    <span class="ba-tag ba-tag-l">Before</span><span class="ba-tag ba-tag-r">After</span>
    <span class="ba-handle" aria-hidden="true"></span>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Slide to compare before and after">
  </div>{during}
</div>"""

    # ------------------------------------------------------------ project card
    def where(self, p):
        return ", ".join(x for x in (p.get("city"), p.get("state")) if x and x != "City") or ("Location pending" if p.get("sample") else "")

    def card(self, p, up, heading="h3"):
        who = p["client"] if p.get("client") and p.get("client_ok") else p.get("client_desc", "")
        facts = []
        if p.get("sqft"):
            facts.append(("Size", f'{p["sqft"]:,} sq ft'))
        if p.get("date"):
            facts.append(("Completed", p["date"]))
        if p.get("duration"):
            facts.append(("Duration", p["duration"]))
        if p.get("sample"):
            facts = [("Size", ""), ("Completed", ""), ("Duration", "")]
        fhtml = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v) if v else self.pending()}</dd></div>" for k, v in facts)
        tags = "".join(f'<li><a href="{up}tasks/{self.task_slug[t]}.html">{e(t)}</a></li>' for t in p["tasks"])
        badge = '<span class="sample-badge">Sample slot</span>' if p.get("sample") else ""
        key = re.sub(r"[^a-z]+", "-", p.get("type", "").lower()).strip("-")
        hay = " ".join([p["title"], p.get("type", ""), self.where(p), who, p.get("summary", "")] + p["tasks"]).lower()
        return f"""<article class="proj{' is-sample' if p.get('sample') else ''}" id="{e(p['slug'])}" data-s="{e(hay)}" data-f="{key}">
  {self.slider(p, up)}
  <div class="proj-body">
    {badge}<p class="eyebrow">{e(p.get('type', ''))} · {e(self.where(p))}</p>
    <{heading}>{e(p['title'])}</{heading}>
    <p class="small muted">{e(who)}</p>
    <dl class="proj-facts">{fhtml}</dl>
    <p>{e(p.get('summary', ''))}</p>
    <ul class="proj-tags">{tags}</ul>
  </div>
</article>"""

    def for_task(self, task, up):
        ps = [p for p in self.projects if task in p["tasks"]]
        if not ps:
            return ""
        return (f'<section class="wrap related"><h2>Projects featuring {e(task.lower())}</h2>'
                f'<div class="proj-grid proj-grid-sm">{"".join(self.card(p, up) for p in ps[:3])}</div>'
                f'<p><a class="btn btn-ghost" href="{up}projects.html">See all projects</a></p></section>')

    # ------------------------------------------------------------ map
    def us_map(self):
        done = {p.get("state") for p in self.projects if not p.get("sample") and p.get("state")}
        home = set(self.m.HOME_STATES)
        cells = ""
        for st, (c, r) in TILES.items():
            cls = "done" if st in done else "home" if st in home else ""
            cells += f'<span class="tile {cls}" style="grid-column:{c + 1};grid-row:{r + 1}" title="{st}">{st}</span>'
        legend = ('<span><i class="tile home"></i>Home crews</span><span><i class="tile done"></i>Completed projects</span>'
                  '<span><i class="tile"></i>Travel crews on request</span>')
        return f'<div class="usmap" role="img" aria-label="Map of states we work in">{cells}</div><p class="map-legend small">{legend}</p>'

    # ------------------------------------------------------------ home-page blocks
    def cred_strip(self):
        C = self.C
        items = []
        ins = dict(C["insurance"])
        items.append(("Insured", ins.get("General liability", "")))
        items.append(("Bonded", C["bonding"]))
        items.append(("SAM.gov registered", f'UEI {C["uei"]}' if C["uei"] else ""))
        safety = dict(C["safety"])
        items.append(("OSHA-trained crews", safety.get("OSHA 10", "")))
        shown = [(k, v) for k, v in items if v or self.slots]
        if not shown:
            return ""
        li = "".join(f"<li><strong>{e(k)}</strong><span>{e(v) if v else self.pending()}</span></li>" for k, v in shown)
        return f'<section class="credstrip" aria-label="Credentials"><ul class="wrap">{li}</ul></section>'

    def featured(self):
        ps = self.projects[:3]
        if not ps:
            return ""
        return f"""<div class="band band-white"><section class="wrap">
  <p class="eyebrow">Recent work</p>
  <h2>Before, during and after</h2>
  <div class="proj-grid">{"".join(self.card(p, "") for p in ps)}</div>
  <p><a class="btn btn-ghost" href="projects.html">See all projects</a></p>
</section></div>"""

    def clients_block(self):
        if self.m.CLIENTS:
            li = "".join(f"<li>{e(c)}</li>" for c in self.m.CLIENTS)
        elif self.slots:
            li = "".join(f'<li class="logo-slot">{self.pending("Client logo")}</li>' for _ in range(6))
        else:
            return ""
        return f'<section class="wrap"><p class="eyebrow">Trusted by</p><ul class="clients">{li}</ul></section>'

    def quotes_block(self):
        ts = self.m.TESTIMONIALS
        if not ts and not self.slots:
            return ""
        if ts:
            body = "".join(f'<figure class="tq"><blockquote>“{e(q)}”</blockquote><figcaption><strong>{e(n)}</strong>, {e(t)}, {e(c)}</figcaption></figure>'
                           for q, n, t, c in ts[:3])
        else:
            body = "".join(f'<figure class="tq is-sample"><blockquote>Client quote goes here, with written permission.</blockquote>'
                           f'<figcaption>{self.pending("Name, title, company")}</figcaption></figure>' for _ in range(3))
        return f'<section class="wrap"><p class="eyebrow">What clients say</p><div class="tq-grid">{body}</div></section>'

    # ------------------------------------------------------------ pages
    def projects_page(self):
        types = []
        for p in self.projects:
            if p.get("type") and p["type"] not in types:
                types.append(p["type"])
        chips = "".join(f'<button type="button" class="chip" data-filter="{re.sub(r"[^a-z]+", "-", t.lower()).strip("-")}">{e(t)}</button>' for t in types)
        cards = "".join(self.card(p, "", "h2") for p in self.projects)
        empty = "" if self.projects else '<p class="muted">Projects are being added.</p>'
        body = f"""
<section class="wrap">
  <p class="eyebrow">Projects</p>
  <h1>Construction cleaning projects, before and after</h1>
  <p class="lede">Real jobs, real photos. Slide each image to compare before and after, and filter by building type or search by city, state or service.</p>
  <div class="split map-split">
    <div>
      <h2 class="h3">Where we work</h2>
      {self.us_map()}
    </div>
    <div class="panel">
      <h2 class="h3">Your project, anywhere in the U.S.</h2>
      <p>Home crews cover the Southeast. Travel crews mobilize for larger scopes in any state. Send the city, ZIP and size and we'll confirm availability before we bid.</p>
      <p><a class="btn" href="quote.html">Request a Bid</a></p>
    </div>
  </div>
  <div class="filter" data-list="projlist">
    <label for="q" class="eyebrow">Search projects</label>
    <input id="q" type="search" placeholder="Try “warehouse”, “Florida” or “ceiling”" autocomplete="off">
    <div class="chips"><button type="button" class="chip is-on" data-filter="">All</button>{chips}</div>
    <p class="small muted" aria-live="polite" data-countline hidden><span data-count></span> projects shown</p>
  </div>
  <div class="proj-grid" id="projlist">{cards}</div>{empty}
</section>
{self.quotes_block()}
{self.clients_block()}"""
        return ("projects.html", "Construction Cleaning Projects | Beyond Klean",
                "Before and after construction cleaning projects: warehouses, retail, multifamily, healthcare, government and more.",
                "Projects", body, "projects.html")

    def capability_page(self):
        C = self.C
        naics = "".join(f"<li><span class='mono'>{e(c)}</span> {e(d)}</li>" for c, d in C["naics"])
        psc = "".join(f"<li><span class='mono'>{e(c)}</span> {e(d)}</li>" for c, d in C["psc"])
        gov = [p for p in self.projects if p.get("type") in ("Government", "Military", "Education or institutional", "Healthcare")]
        gov = gov or self.projects
        past = "".join(
            f"<li><strong>{e(p['title'])}</strong> · {e(p['client'] if p.get('client') and p.get('client_ok') else p.get('client_desc', ''))}"
            f" · {e(self.where(p))}{' · ' + e(p['date']) if p.get('date') else ''}</li>" for p in gov[:5]) or f"<li>{self.pending()}</li>"
        ins = self.rows(C["insurance"] or [("General liability", ""), ("Workers' compensation", ""), ("Auto liability", ""), ("Umbrella", "")])
        body = f"""
<section class="wrap capdoc">
  <div class="cap-head">
    <div>
      <p class="eyebrow">Capability statement</p>
      <h1>{e(C['legal_name'] or C['name'])}</h1>
      <p class="lede">Construction and specialty cleaning for federal, state, municipal, military and institutional facilities. Rough, final and touch-up cleaning, overhead and high dusting, floors, glass, kitchens and closeout, performed by our own crews.</p>
    </div>
    <dl class="cap-contact">
      {self.rows([("Phone", C['phone']), ("Email", C['email']), ("Address", C['address'])])}
      <div><dt>Web</dt><dd>beyondklean.com</dd></div>
    </dl>
  </div>
  <div class="cap-grid">
    <section class="panel">
      <h2 class="h3">Core competencies</h2>
      <ul class="check">
        <li>Post-construction cleaning by phase: rough, final, touch-up and punch</li>
        <li>Overhead and high-structure cleaning from lifts: decks, joists, ducts, fixtures</li>
        <li>Construction indoor air quality support: HEPA capture, filter changes, flush-out readiness</li>
        <li>Initial floor care: VCT finish, sealed concrete, tile and grout haze, carpet extraction</li>
        <li>Construction glass and window cleaning, film and label removal</li>
        <li>Commercial kitchen, FRP and food-facility turnover cleaning</li>
        <li>Occupied-facility and phased cleaning under security and infection-control rules</li>
        <li>Debris management, recycling separation and closeout documentation</li>
      </ul>
    </section>
    <section class="panel">
      <h2 class="h3">Differentiators</h2>
      <ul class="check">
        <li>Itemized, phase-by-phase bids priced from a documented unit-price book</li>
        <li>Capture-first methods: HEPA vacuums and wet methods aligned with OSHA 1926.1153 silica rules</li>
        <li>Least-aggressive chemistry matched to manufacturer care guides, protecting finish warranties</li>
        <li>Closeout package: room checklists, photo documentation and product SDS</li>
        <li>Home crews in the Southeast, travel crews nationwide</li>
      </ul>
    </section>
    <section class="panel">
      <h2 class="h3">Company data</h2>
      <dl class="facts">
        {self.rows([("UEI", C['uei']), ("CAGE code", C['cage']), ("SAM.gov status", C['sam_status']), ("Year founded", C['founded'])])}
        {self.rows([("Socioeconomic status", ", ".join(C['set_asides']))])}
        {self.rows([("Bonding capacity", C['bonding'])])}
      </dl>
      <h3 class="h3 sub">NAICS codes</h3><ul class="codes">{naics}</ul>
      <h3 class="h3 sub">PSC codes</h3><ul class="codes">{psc}</ul>
    </section>
    <section class="panel">
      <h2 class="h3">Insurance</h2>
      <dl class="facts">{ins}</dl>
      <h2 class="h3 sub">Past performance</h2>
      <ul class="past">{past}</ul>
      <p class="small"><a href="projects.html">Project photos and details</a></p>
    </section>
  </div>
  <p class="noprint"><button type="button" class="btn" data-print>Print / Save as PDF</button> <a class="btn btn-ghost" href="quote.html">Request a Bid</a></p>
</section>"""
        return ("capability-statement.html", "Capability Statement | Beyond Klean",
                "Beyond Klean capability statement: core competencies, NAICS and PSC codes, company data and past performance for government and institutional buyers.",
                "Capability Statement", body, "capability-statement.html")

    def safety_page(self):
        C = self.C
        lic = self.rows(C["licenses"] or [("State licenses and registrations", "")])
        saf = self.rows(C["safety"] or [("Experience modification rate (EMR)", ""), ("OSHA 30", ""), ("OSHA 10", ""), ("Aerial lift training", "")])
        ins = self.rows(C["insurance"] or [("General liability", ""), ("Workers' compensation", ""), ("Auto liability", ""), ("Umbrella", "")])
        body = f"""
<section class="wrap narrow">
  <p class="eyebrow">Safety and compliance</p>
  <h1>Safe crews, clean paperwork</h1>
  <p class="lede">General contractors and owners need more than a clean building. They need a crew that follows the site safety plan and hands over the documents at the start and the end of the job.</p>

  <h2>How our crews work safely</h2>
  <ul class="check">
    <li><strong>Silica-aware housekeeping.</strong> No dry sweeping or compressed air where silica dust is present. HEPA vacuums and wet methods, per OSHA 29 CFR 1926.1153.</li>
    <li><strong>Work at height.</strong> Trained lift operators, fall protection in boom lifts and site-specific lift plans for overhead cleaning.</li>
    <li><strong>Hazard communication.</strong> Safety Data Sheets on site for every product, labeled containers and trained crews.</li>
    <li><strong>Coordination with other trades.</strong> Lockout and equipment-start coordination with the electrical and mechanical contractors before cleaning equipment rooms.</li>
    <li><strong>Site rules.</strong> We follow the GC's safety plan, attend orientation and toolbox talks, and report incidents and near misses the same day.</li>
    <li><strong>Regulated work.</strong> Mold, abatement, biohazard and hood cleaning go only to licensed, certified technicians, with the required notifications.</li>
  </ul>

  <h2>Insurance and bonding</h2>
  <dl class="facts">{ins}{self.rows([("Bonding capacity", C['bonding'])])}</dl>
  <p class="small">Certificates of insurance are issued with the bid or on award, with additional insured and waiver of subrogation endorsements as the contract requires.</p>

  <h2>Licenses and registrations</h2>
  <dl class="facts">{lic}{self.rows([("SAM.gov UEI", C['uei']), ("CAGE code", C['cage'])])}</dl>

  <h2>Safety record and training</h2>
  <dl class="facts">{saf}</dl>

  <h2>Secure, government and military sites</h2>
  <p>Crews complete the access process each site requires, such as background checks, base credentials or escorts, arranged with the prime contractor before mobilization. Federal work follows the contract's wage determination and reporting requirements.</p>

  <h2>Documents we provide</h2>
  <ul class="check">
    <li>Certificate of insurance and W-9 with the bid or on award</li>
    <li>Site-specific safety plan and job hazard analysis before mobilization</li>
    <li>Training records for crew members on site</li>
  </ul>
  <h3>At closeout</h3>
  <!--CLOSEOUT-->
  <p><a class="btn" href="quote.html">Request a Bid</a> <a class="btn btn-ghost" href="capability-statement.html">Capability statement</a></p>
</section>"""
        return ("safety.html", "Safety and Compliance | Beyond Klean",
                "How Beyond Klean crews work safely: silica-aware cleaning, lift safety, hazard communication, insurance, licensing and the documents we provide.",
                "Safety and Compliance", body, "safety.html")

    def contact_page(self):
        C = self.C
        body = f"""
<section class="wrap">
  <p class="eyebrow">Contact</p>
  <h1>Talk to an estimator</h1>
  <p class="lede">Call for anything, send your specs, or request a bid online. Every request gets a reference number and an answer on crew availability.</p>
  <div class="contact-grid">
    <div class="panel contact-card">
      <h2 class="h3">Call</h2><p class="big">{self.phone_link()}</p>
      <h2 class="h3">Email</h2><p>{self.email_link()}</p>
      <h2 class="h3">Office</h2><p>{self.fact(C['address'], 'Address pending')}</p>
      <h2 class="h3">Hours</h2><p>{e(C['hours'])}</p>
    </div>
    <div class="panel">
      <h2 class="h3">Fastest way to a bid</h2>
      <ol class="need">
        <li><strong>Project type</strong><span>Residential, commercial, industrial, institutional, government or military</span></li>
        <li><strong>Needed by</strong><span>The date it has to be done</span></li>
        <li><strong>Location</strong><span>City and ZIP code</span></li>
        <li><strong>Size</strong><span>Approximate square footage</span></li>
        <li><strong>Tasks</strong><span>What needs cleaning</span></li>
      </ol>
      <p><a class="btn" href="quote.html">Request a Bid</a> <a class="btn btn-ghost" href="quote.html#specs">Send Your Specs</a></p>
      <h2 class="h3">Service area</h2><p>{e(C['service_area'])}</p>
    </div>
  </div>
</section>"""
        return ("contact.html", "Contact | Beyond Klean",
                "Call, email or request a bid for construction and specialty cleaning anywhere in the U.S.",
                "Contact", body, "contact.html")

    def leadership_block(self):
        L = self.C["leadership"]
        if L:
            cards = "".join(f'<div class="lead-card"><strong>{e(n)}</strong><span class="small muted">{e(t)}</span><p class="small">{e(b)}</p></div>' for n, t, b in L)
        elif self.slots:
            cards = "".join(f'<div class="lead-card is-sample"><strong>{self.pending("Name")}</strong><span class="small muted">{r}</span>'
                            f'<p class="small">One or two lines of background.</p></div>' for r in ("Owner / President", "Operations Manager", "Estimating"))
        else:
            return ""
        return f'<h2>Leadership</h2><div class="lead-grid">{cards}</div>'

    def org_schema(self, site_url):
        C = self.C
        s = {"@context": "https://schema.org", "@type": "Organization", "name": C["name"], "url": site_url,
             "logo": f"{site_url}/assets/logo.png", "areaServed": {"@type": "Country", "name": "United States"}}
        if C["legal_name"]:
            s["legalName"] = C["legal_name"]
        if C["phone"]:
            s["telephone"] = C["phone"]
        if C["email"]:
            s["email"] = C["email"]
        if C["address"]:
            s["address"] = C["address"]
        if C["naics"]:
            s["naics"] = C["naics"][0][0]
        return s
