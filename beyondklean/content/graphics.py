"""Infographics built as HTML and inline SVG, so they stay sharp, load fast and their words stay
readable by search engines. Each function returns an HTML fragment."""


def three_cleans(ic):
    cols = [
        ("Framing and MEP rough-in", "broom", "Progress cleaning", "Daily debris, sweeping and safe walkways while trades work. Spec 01 74 13."),
        ("Drywall and paint", "dust", "Rough clean", "Bulk debris and heavy dust out before finish trades start."),
        ("Finishes and fixtures", "glass", "Light clean", "Fixtures, glass, labels and cabinets as finishes go in."),
        ("Substantial Completion", "clipboard", "Final clean", "Every surface, top down, before the inspection. Spec 01 74 23."),
        ("Owner walk and turnover", "badge", "Touch-up and punch", "Re-clean after punch work, right before move-in."),
    ]
    items = "".join(f"""<li>
      <span class="tl-stage">{stage}</span>
      <span class="tl-dot" aria-hidden="true"></span>
      <div class="tl-card">{ic(icon)}<strong>{clean}</strong><span>{desc}</span></div>
    </li>""" for stage, icon, clean, desc in cols)
    return f"""<figure class="tl" aria-label="Where construction cleaning happens in the schedule">
  <ol class="tl-track">{items}</ol>
  <figcaption class="small muted">Construction cleaning runs with the schedule: one bid can cover every phase, each priced as its own line.</figcaption>
</figure>"""


def process(ic):
    steps = [
        ("send", "Send your scope", "Project type, location, deadline, square footage and tasks. Specs help but aren't required."),
        ("crew", "We confirm a crew", "A home crew or a travel crew, matched to the size and timing of the job."),
        ("bid", "Itemized bid", "Every task priced as its own line, by phase, with nothing buried."),
        ("truck", "We mobilize", "Rough, final and punch cleans timed to your trades and inspections."),
        ("badge", "Closeout on time", "Walkthrough, punch items re-cleaned, checklists and photos for your package."),
    ]
    li = "".join(f'<li><span class="pr-ic">{ic(i)}</span><strong>{t}</strong><span>{d}</span></li>' for i, t, d in steps)
    return f'<ol class="process">{li}</ol>'


def _building(badges, extra=""):
    """Building cross-section pictogram with numbered badges at (x, y)."""
    b = "".join(f'<g class="bdg"><circle cx="{x}" cy="{y}" r="15"/><text x="{x}" y="{y + 5}" text-anchor="middle">{n}</text></g>'
                for n, (x, y) in enumerate(badges, 1))
    joists = "".join(f'<path d="M{x} 38 L{x + 20} 58 L{x + 40} 38"/>' for x in range(50, 540, 40))
    return f"""<svg class="bldg" viewBox="0 0 600 350" role="img" aria-hidden="true">
  <g class="st">
    <rect x="30" y="26" width="540" height="12" class="deck"/>
    {joists}
    <path d="M30 58 H570"/>
    <rect x="70" y="68" width="330" height="24" rx="12" class="duct"/>
    <path d="M150 92 v10 M300 92 v10"/>
    <rect x="430" y="66" width="70" height="10" class="fixture"/><path d="M450 58 v8 M480 58 v8"/>
    <rect x="125" y="102" width="50" height="8" class="fixture"/><rect x="275" y="102" width="50" height="8" class="fixture"/>
    <path d="M40 38 V320 M560 38 V250"/>
    <rect x="60" y="140" width="110" height="90" class="win"/><path d="M115 140 v90 M60 185 h110"/>
    <rect x="370" y="236" width="150" height="16" class="top"/><rect x="380" y="252" width="130" height="68"/><path d="M445 252 v68 M395 285 h30 M460 285 h30"/>
    <path d="M560 250 h10 v70"/>
    <rect x="20" y="320" width="560" height="12" class="floor"/>
    {extra}
  </g>
  {b}
</svg>"""


def top_down():
    svg = _building([(415, 80), (115, 128), (445, 222), (290, 312), (575, 286)],
                    extra='<path class="flow" d="M250 120 V300"/><path class="flow" d="M238 286 l12 14 12-14"/>'
                          '<path class="flow" d="M500 300 h48"/><path class="flow" d="M536 290 l12 10 -12 10"/>')
    steps = [
        ("Overhead first", "Deck, joists, ducts and light fixtures, so nothing falls on clean work below."),
        ("Walls and glass", "High to low, including window frames, tracks and sills."),
        ("Fixtures and casework", "Counters, cabinets inside and out, hardware and restroom fixtures."),
        ("Floors last", "HEPA vacuum, then the floor-specific cleaning and finish."),
        ("Out the door", "Room by room toward the exits, so no one walks across a finished floor."),
    ]
    li = "".join(f"<li><strong>{t}</strong> {d}</li>" for t, d in steps)
    return f"""<figure class="graphic">
  <div class="graphic-in">{svg}<ol class="graphic-key">{li}</ol></div>
  <figcaption class="small muted">Top down, inside out: the order every Beyond Klean crew cleans in.</figcaption>
</figure>"""


def commonly_missed():
    svg = _building([(400, 46), (150, 118), (205, 186), (340, 102), (470, 226), (300, 312), (530, 300), (120, 300)],
                    extra='<rect x="310" y="150" width="48" height="26" class="hood"/><path d="M322 150 v-58 M346 150 v-58"/>')
    items = [
        ("Open deck and structure", "Dust and overspray on the deck, joists and bar joists."),
        ("Light fixture tops and lenses", "The first thing an owner sees when the lights come on."),
        ("High glass and window tracks", "Labels, overspray and debris in sills and tracks."),
        ("Ducts, diffusers and returns", "Construction dust pulled into the HVAC at startup."),
        ("Inside cabinets and drawers", "Sawdust and packaging left behind closed doors."),
        ("Floor finish and edges", "Initial finish, grout haze and dirt packed along the base."),
        ("Exit doors and thresholds", "Hardware, kick plates and the threshold under the door."),
        ("Behind and under fixtures", "Behind toilets, under sinks and around equipment."),
    ]
    li = "".join(f"<li><strong>{t}</strong> {d}</li>" for t, d in items)
    return f"""<figure class="graphic">
  <div class="graphic-in">{svg}<ol class="graphic-key">{li}</ol></div>
  <figcaption class="small muted">Write these into the cleaning scope at bid time and they never turn into change orders.</figcaption>
</figure>"""


def capture_vs_move(ic):
    return f"""<div class="versus">
  <div class="vs-card vs-bad">
    <p class="vs-h">{ic("blower")}<strong>Moves dust</strong></p>
    <ul>
      <li>Dry sweeping and dry dusting cloths</li>
      <li>Leaf blowers and compressed air</li>
      <li>Strongest chemical on the truck</li>
    </ul>
    <p class="vs-r">Result: dust resettles on new finishes, gets pulled into the HVAC and puts silica in the air.</p>
  </div>
  <div class="vs-card vs-good">
    <p class="vs-h">{ic("vacuum")}<strong>Captures dust</strong></p>
    <ul>
      <li>HEPA vacuums at the surface</li>
      <li>Damp microfiber and wet methods</li>
      <li>pH-neutral cleaners matched to the finish</li>
    </ul>
    <p class="vs-r">Result: dust leaves the building, air is cleaner at turnover and finish warranties stay intact.</p>
  </div>
</div>"""


def closeout(ic):
    docs = [("clipboard", "Room checklists", "Every room signed off"), ("photo", "Photo documentation", "Before and after, by area"),
            ("doc", "Safety Data Sheets", "Every product used"), ("shield", "Certificate of insurance", "With required endorsements"),
            ("badge", "Punch re-clean sign-off", "Items closed with the GC")]
    li = "".join(f'<li>{ic(i)}<strong>{t}</strong><span>{d}</span></li>' for i, t, d in docs)
    return f'<ul class="docstack">{li}</ul>'


PHASES = [("rough", "Rough"), ("progress", "Progress"), ("final", "Final"), ("touch-up-punch", "Touch-up"),
          ("occupancy-turnover", "Turnover"), ("recurring-maintenance", "Ongoing")]


def phase_strip(phase_key):
    anystage = phase_key == "any-stage-specialty"
    li = "".join(f'<li class="{"on" if k == phase_key or anystage else ""}">{label}</li>' for k, label in PHASES)
    note = "Any stage, as the project needs it" if anystage else "When this happens in the project"
    return f'<div class="phases" aria-label="Project stage"><span class="phases-note">{note}</span><ol>{li}</ol></div>'
