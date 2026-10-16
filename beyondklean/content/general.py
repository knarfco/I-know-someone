"""Site-wide content: glossary, general FAQ, markets and the static pages (home, methods, GCs, quote, about)."""
from html import escape as e

GLOSSARY = [(t, s, d) for t, s, d in [
 ("Rough clean", "rough-clean", "The first phase of construction cleaning, after framing, drywall and MEP rough-in. Removes bulk debris and heavy dust before finish trades start."),
 ("Light clean", "light-clean", "The middle phase of construction cleaning, also called the detail clean. Cleans surfaces, fixtures and glass after most finishes are installed."),
 ("Final clean", "final-clean", "The complete, detailed cleaning of a space before the Substantial Completion inspection and owner turnover."),
 ("Touch-up clean", "touch-up-clean", "A quick pass after punch work or right before an owner walk to re-clean areas that got dirty again."),
 ("Sparkle clean", "sparkle-clean", "An informal name for the last detailed touch-up before an owner walk or grand opening."),
 ("Punch list", "punch-list", "The list of incomplete or defective items recorded during the pre-completion walk. Cleaning items such as smudges, labels and residue are common entries."),
 ("Substantial Completion", "substantial-completion", "The point when the work is complete enough for the owner to occupy and use it. Most specs require final cleaning before the inspection for it."),
 ("Certificate of occupancy", "certificate-of-occupancy", "The document issued by the local building authority allowing a building or space to be occupied. Often abbreviated CO."),
 ("Progress cleaning", "progress-cleaning", "Ongoing cleaning during construction to keep the site safe and orderly. Often specified under section 01 74 13."),
 ("Tenant improvement", "tenant-improvement", "Interior build-out of a leased space for a specific tenant. Often abbreviated TI."),
 ("FRP", "frp", "Fiberglass reinforced plastic. Textured, washable wall panels used in kitchens, restrooms and food areas."),
 ("VCT", "vct", "Vinyl composition tile. A resilient floor tile that needs initial preparation and floor finish after installation."),
 ("LVT", "lvt", "Luxury vinyl tile. A resilient floor with a factory wear layer, usually maintained without floor finish according to the manufacturer's guide."),
 ("ACT", "act", "Acoustical ceiling tile. Lay-in ceiling panels supported by a metal grid."),
 ("HEPA", "hepa", "High-efficiency particulate air. A HEPA filter captures at least 99.97 percent of particles at 0.3 microns, so fine construction dust is held instead of exhausted."),
 ("Microfiber", "microfiber", "Synthetic cleaning cloth with very fine fibers that trap dust and soil mechanically, reducing the need for chemicals."),
 ("pH-neutral cleaner", "ph-neutral-cleaner", "A cleaner with a pH near 7. Gentler on new finishes, stone, grout and floor coatings than acids or strong alkalis."),
 ("VOC", "voc", "Volatile organic compound. Chemicals that evaporate from products and finishes and affect indoor air. Low-VOC cleaners release less."),
 ("IAQ", "iaq", "Indoor air quality. Construction IAQ management keeps dust and contaminants out of the HVAC system and occupied space."),
 ("IEQ", "ieq", "Indoor environmental quality. A broader measure of indoor air, lighting, acoustics and comfort used in green building standards."),
 ("SDS", "sds", "Safety Data Sheet. The manufacturer's document describing a chemical's hazards, handling and first aid."),
 ("TDS", "tds", "Technical Data Sheet. The manufacturer's document describing how a product performs and how to use it."),
 ("Crystalline silica", "crystalline-silica", "A mineral in concrete, masonry, stone and some joint compounds. Its respirable dust is regulated by OSHA."),
 ("Silica-aware housekeeping", "silica-aware-housekeeping", "Cleaning that avoids dry sweeping, dry brushing and compressed air where silica dust is present, using wet methods and HEPA vacuums instead."),
 ("Wet sweeping", "wet-sweeping", "Sweeping with water or a damp compound to keep dust from becoming airborne."),
 ("Sweeping compound", "sweeping-compound", "A granular material spread on floors before sweeping to hold dust down."),
 ("Negative air machine", "negative-air-machine", "A HEPA-filtered fan unit that pulls air out of a contained work area so dust does not escape into occupied space."),
 ("Containment", "containment", "Temporary barriers, often plastic sheeting with zipper doors, that isolate a dusty work area."),
 ("Grout haze", "grout-haze", "A thin film of cement-based grout left on the face of tile after grouting."),
 ("Efflorescence", "efflorescence", "White, powdery salt deposits left when water moves through concrete, masonry or grout and evaporates."),
 ("Overspray", "overspray", "Paint, coating or texture that lands outside the intended surface."),
 ("Mastic", "mastic", "A thick adhesive used for flooring, tile and panels."),
 ("Floor finish", "floor-finish", "The polymer coating applied to resilient floors such as VCT. Often called wax."),
 ("Strip and refinish", "strip-and-refinish", "Removing old floor finish chemically and applying new coats."),
 ("Scrub and recoat", "scrub-and-recoat", "Deep-scrubbing the top layers of floor finish and applying fresh coats without a full strip."),
 ("Burnishing", "burnishing", "High-speed polishing of floor finish to restore gloss."),
 ("Auto-scrubber", "auto-scrubber", "A floor machine that applies cleaning solution, scrubs and vacuums it back up in one pass."),
 ("Extraction", "extraction", "Carpet cleaning that injects a cleaning solution and vacuums it out, often called hot water extraction."),
 ("Wicking", "wicking", "When soil or residue deep in carpet rises to the surface as it dries, making stains reappear."),
 ("High dusting", "high-dusting", "Cleaning surfaces out of normal reach, such as decks, beams, ducts, pipes and fixtures."),
 ("Open ceiling", "open-ceiling", "A design with no finished ceiling, leaving the deck, structure and MEP exposed."),
 ("Bar joist", "bar-joist", "An open-web steel joist that supports roof or floor decks."),
 ("Cable tray", "cable-tray", "An open metal support system for electrical and data cables, usually overhead."),
 ("HVLS fan", "hvls-fan", "High-volume, low-speed ceiling fan used in warehouses, gyms and large spaces."),
 ("MEP", "mep", "Mechanical, electrical and plumbing systems."),
 ("AHU", "ahu", "Air handling unit. The equipment that moves and conditions air through ductwork."),
 ("RTU", "rtu", "Rooftop unit. A packaged heating and cooling unit installed on the roof."),
 ("NADCA", "nadca", "National Air Duct Cleaners Association. Publishes standards for HVAC system cleaning."),
 ("NFPA 96", "nfpa-96", "The fire code standard for ventilation control and fire protection of commercial cooking operations, including hood and duct cleaning."),
 ("LEED", "leed", "Leadership in Energy and Environmental Design. A green building rating system that includes construction IAQ and waste diversion credits."),
 ("Flush-out", "flush-out", "Running a building's HVAC with outdoor air after construction to dilute contaminants before or during early occupancy."),
 ("Low-E coating", "low-e-coating", "A thin metallic coating on glass that controls heat transfer. Some coated surfaces cannot be scraped."),
 ("Glass scratch waiver", "glass-scratch-waiver", "A contract clause addressing liability for scratches that can occur when construction debris is removed from glass."),
 ("Pure-water cleaning", "pure-water-cleaning", "Window cleaning with deionized or reverse-osmosis water that dries spot-free without detergent."),
 ("Soft washing", "soft-washing", "Exterior cleaning with low pressure and cleaning solutions instead of high pressure."),
 ("EIFS", "eifs", "Exterior insulation and finish system. A synthetic stucco cladding that can be damaged by high-pressure washing."),
 ("Attic stock", "attic-stock", "Spare finish materials left for the owner for future repairs."),
 ("Floor protection", "floor-protection", "Temporary board or film laid over finished floors during construction."),
 ("Back-charge", "back-charge", "A cost the GC charges to a subcontractor for work, such as cleanup, that the sub was responsible for."),
 ("CSI MasterFormat", "csi-masterformat", "The standard numbering system for construction specifications. Cleaning is usually in Division 01."),
 ("Food-contact surface", "food-contact-surface", "A surface that food normally touches, which must be cleaned and then sanitized."),
 ("Sanitizing", "sanitizing", "Reducing microorganisms on a surface to safe levels with a registered sanitizer used at label concentration."),
 ("Disinfecting", "disinfecting", "Killing specified microorganisms on surfaces with an EPA-registered disinfectant used according to its label."),
 ("Safer Choice", "safer-choice", "An EPA program that certifies cleaning products meeting criteria for human health and environmental safety."),
 ("Green Seal GS-42", "green-seal-gs-42", "A certification standard for commercial and institutional cleaning services covering procedures, purchasing and training."),
 ("Raised access floor", "raised-access-floor", "Removable floor panels over a plenum, common in data centers."),
 ("Static-dissipative floor", "static-dissipative-floor", "A floor designed to safely drain static electricity, used around electronics. Needs specific cleaners."),
 ("Curtain wall", "curtain-wall", "A non-structural exterior glass and metal wall system on larger buildings."),
 ("Storefront", "storefront", "Ground-level aluminum and glass framing system used for retail and building entries."),
 ("Gondola", "gondola", "Freestanding retail shelving unit used in aisles."),
 ("Walk-off mat", "walk-off-mat", "Entrance matting that captures soil and moisture before it is tracked inside."),
]]

GENERAL_FAQ = [
 ("About Beyond Klean", [
  ("What is Beyond Klean?", "Beyond Klean is a construction and specialty cleaning company. Our crews handle every cleaning scope a building project can call for, from debris and rough clean through final clean, glass, floors, kitchens, overhead and closeout."),
  ("Does Beyond Klean do the cleaning itself?", "Yes. Our own crews perform the work, and your bid names the company that performs and insures it. Regulated scopes such as mold, abatement and hood cleaning are assigned only to licensed, certified technicians."),
  ("Where does Beyond Klean work?", "We take projects nationwide. Home crews cover the Southeast, and travel crews mobilize for larger scopes anywhere in the country. Tell us the city and ZIP code and we will confirm crew availability before we bid."),
  ("What kinds of buildings do you clean?", "Residential, multifamily, commercial, retail, restaurant, industrial, warehouse, institutional, healthcare, education, government and military facilities, from tenant improvements to ground-up construction."),
  ("What kinds of cleaning do you handle?", "Everything a construction project can need cleaned, from debris and rough clean through final clean, glass, floors, kitchens, overhead high dusting and closeout, searchable by the names contractors, specs and buyers actually use."),
  ("Is there a cost to request a bid?", "No. Bids are free for general contractors, property managers and building owners."),
  ("What do you need from me to bid?", "Five things: the type of project, when it needs to be done, the city and ZIP code, the approximate square footage and the tasks you need. Plans and specs help but are not required."),
  ("What is the relationship with Above Eye Level Cleaning?", "Above Eye Level Cleaning is our sister brand for recurring overhead and high-dusting work. Beyond Klean handles construction turnover, and AELC keeps overhead surfaces clean after the building opens."),
 ]),
 ("For general contractors", [
  ("How do I get a cleaning crew on my project?", "Request a bid or send your specs. We review the scope, phases, schedule and site, confirm crew availability and send an itemized bid."),
  ("Can you price from my drawings and specs?", "Yes. Send drawings, the Division 01 cleaning section and any finish schedules. We price from them and point out anything commonly missed, such as overhead cleaning, glass or floor finish."),
  ("Can one bid cover rough, final and touch-up cleaning?", "Yes. Most construction cleaning is bid by phase. One bid can cover every phase, with each phase priced as its own line."),
  ("What if I need a cleaning crew tomorrow?", "Tell us the deadline. We only commit to a date after a crew is confirmed, and we will tell you plainly if we cannot make it."),
  ("Do your crews carry insurance?", "Yes. A certificate of insurance is provided with the bid or on award, and additional insured or waiver requirements are confirmed before mobilization."),
  ("Who do I contract with and pay?", "The company named on your bid, which is the company performing the work."),
  ("Can you handle multi-site rollouts?", "Yes. National and regional programs use one scope and checklist across every site, with travel crews for locations outside our home markets."),
  ("What documentation do I get at closeout?", "Room checklists, photo documentation and product data sheets for the cleaners used, ready for your closeout package and any LEED or IAQ requirements."),
 ]),
 ("For owners and property managers", [
  ("When should cleaning be planned on a construction project?", "Early. Overhead cleaning, glass, floors and kitchen equipment are often missed in scopes. Writing them in during bidding prevents change orders at the end."),
  ("Why is my new building still dusty after the final clean?", "Usually because overhead surfaces were not in scope, or dust was moved instead of captured. HEPA capture and overhead cleaning fix the cause, not just the symptom."),
  ("Can Beyond Klean help after we open?", "Yes. Recurring overhead and high dusting goes through Above Eye Level Cleaning, and floor, glass and specialty services can be scheduled as needed."),
  ("Is construction cleaning the same as janitorial service?", "No. Construction cleaning removes construction residue from new finishes: dust, labels, adhesive, grout haze and debris. Janitorial service maintains an occupied building."),
  ("How do I know the cleaning was done right?", "Ask for room checklists and before-and-after photos, and walk the space with the punch list. Our crews provide both and re-clean punch items before sign-off."),
  ("Can cleaning be scheduled around our operations?", "Yes. Remodels in operating stores, offices and healthcare facilities are commonly cleaned overnight or in phases."),
  ("What should I check at the owner walk?", "Look up at ceilings and fixtures, open drawers, check glass in daylight, look behind toilets and under sinks, and check floor edges and corners."),
  ("Who is responsible if something is damaged during cleaning?", "The company performing the work, under its contract and insurance. That is why we test products in a hidden spot and follow manufacturer care guides on new finishes."),
 ]),
 ("Government, military and institutional work", [
  ("Do you work on government and military projects?", "Yes. Federal, state, municipal and military facility work follows the contract's requirements, including wage determinations, site access rules and documentation."),
  ("Can your crews get onto a military installation?", "Yes, by following the installation's access process, such as background checks, base credentials or escorts, arranged with the prime contractor before mobilization."),
  ("Do you work in occupied schools, hospitals and courthouses?", "Yes, with scheduling, containment and infection-control or security rules set by the facility, and crews briefed on them before work starts."),
  ("Can you work as a subcontractor to the prime contractor?", "Yes. Most institutional and government cleaning scopes are subcontracted under the prime, and we follow the prime's safety plan and submittal process."),
 ]),
 ("Green and safer cleaning", [
  ("What makes Beyond Klean's approach greener?", "Methods first: capture dust with HEPA instead of blowing it around, use microfiber and water before chemicals, pick pH-neutral and low-VOC products matched to the surface, and recover wash water instead of sending it to storm drains."),
  ("Do you use non-toxic cleaning products?", "We avoid blanket claims like non-toxic. We describe the specific methods and products used and provide their data sheets, because every product has handling requirements."),
  ("What is capture-first cleaning?", "Removing dust and soil from the building, with HEPA vacuums and microfiber, instead of moving it into the air or onto other surfaces."),
  ("Why does least-aggressive chemistry matter on new buildings?", "New finishes are at their most vulnerable. Harsh acids and solvents can etch stone, dull coatings, damage grout and void warranties."),
  ("Are green cleaning products less effective?", "Not when they are matched to the job. Many construction residues come off with mechanical methods and neutral products; stronger chemistry is reserved for when it is truly needed."),
  ("Do you follow green building requirements?", "Yes. Our crews follow the project IAQ plan, document products and methods, and support LEED documentation for cleaning-related credits."),
  ("What certifications matter for green cleaning?", "EPA Safer Choice certifies products, and Green Seal GS-42 certifies cleaning service providers. Project specs may name others."),
  ("How is wash water handled?", "Exterior washing uses recovery equipment or drain protection so dirty water does not enter storm drains."),
 ]),
 ("Pricing and scheduling", [
  ("How is construction cleaning priced?", "By square foot, by phase, by crew-day or by line item, depending on scope. Overhead work, glass and floor care are usually separate lines on the bid."),
  ("What affects the price most?", "Square footage, ceiling height and access, number of phases, finish types, the amount of residue, schedule pressure, travel and night or weekend work."),
  ("Why don't you publish prices?", "Prices depend on location, access and scope. We price after seeing the project type, size, location, deadline and task list, and every line is itemized."),
  ("How far in advance should cleaning be booked?", "As early as the bid phase. Final cleaning is scheduled around inspection dates, and crews book up near quarter-end and holiday openings."),
  ("Is night work more expensive?", "Usually, because of labor premiums. It is often worth it for operating stores and occupied buildings."),
  ("Are re-cleans extra?", "That depends on the contract. Clear re-clean terms in the scope avoid disputes at the end of the job."),
  ("How long does a final clean take?", "From one day for a small tenant space to several weeks for large buildings cleaned in phases."),
  ("Do you charge for travel on out-of-area projects?", "Travel crews carry mobilization and lodging costs, shown as their own line on the bid so you can compare it fairly."),
 ]),
]

MARKETS = [
    ("Residential & multifamily", "Apartments, condos, townhomes and amenity spaces, unit turns and lease-up."),
    ("Commercial", "Offices, retail, restaurants, hotels and tenant improvements, including store openings."),
    ("Industrial", "Warehouses, distribution centers, plants and cold storage, with lift work at any height."),
    ("Institutional", "Schools, universities, hospitals, clinics and labs, cleaned to facility protocol."),
    ("Government", "Federal, state and municipal buildings, courthouses and public works."),
    ("Military", "Barracks, hangars, admin and support facilities, under installation access rules."),
]


def static_pages(n_tasks, n_names, n_faq, fam_cards, AELC_URL, phase_counts, task_options, phone=""):
    tel = "".join(c for c in phone if c.isdigit() or c == "+")
    call = f'<a class="btn btn-light" href="tel:{tel}">Call {e(phone)}</a>' if phone else ""
    markets = "".join(f'<div class="mcard"><strong>{e(n)}</strong><span class="small muted">{e(d)}</span></div>'
                      for n, d in MARKETS)
    need = """<ol class="need">
      <li><strong>Project type</strong><span>Residential, commercial, industrial, institutional, government or military</span></li>
      <li><strong>Needed by</strong><span>The date it has to be done</span></li>
      <li><strong>Location</strong><span>City and ZIP code</span></li>
      <li><strong>Size</strong><span>Approximate square footage</span></li>
      <li><strong>Tasks</strong><span>What needs cleaning</span></li>
    </ol>"""
    home = f"""
<section class="hero">
  <div class="wrap hero-in">
    <p class="eyebrow">Construction &amp; specialty cleaning · Nationwide</p>
    <h1>Construction cleaning, done to spec and on schedule.</h1>
    <form class="finder" data-finder role="search" action="services.html">
      <label for="finder-q" class="finder-label">What needs cleaning?</label>
      <div class="finder-box">
        <input id="finder-q" name="q" type="text" autocomplete="off" spellcheck="false" placeholder="Try “ceiling dust”, “grout haze” or “final clean”" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="finder-list">
        <button class="btn" type="submit">Find it</button>
      </div>
      <ul class="finder-list" id="finder-list" role="listbox" hidden></ul>
    </form>
    <p class="lede">Our crews handle every cleaning scope a building project calls for, from rough clean to final turnover, for general contractors, property managers and building owners. Home crews cover the Southeast. Travel crews mobilize nationwide for larger projects.</p>
    <div class="hero-cta">
      <a class="btn" href="quote.html">Request a Bid</a>
      <a class="btn btn-light" href="quote.html#specs">Send Your Specs</a>
      {call}
    </div>
  </div>
</section>
<!--CRED-->

<section class="wrap">
  <p class="eyebrow">Markets we serve</p>
  <h2>Any building type. Any stage of construction.</h2>
  <div class="mgrid">{markets}</div>
</section>
<!--FEATURED-->

<section class="wrap">
  <p class="eyebrow">Services</p>
  <h2>Browse by type of work</h2>
  <div class="fgrid">{fam_cards}</div>
  <p><a class="btn btn-ghost" href="services.html">Search our services</a></p>
</section>

<section class="wrap">
  <p class="eyebrow">How it works</p>
  <h2>From your scope to a signed-off building</h2>
  <ol class="steps">
    <li><strong>Send your scope.</strong> Project type, location, deadline, square footage and the tasks you need. Specs and plans help but aren't required.</li>
    <li><strong>We confirm crew availability.</strong> A home crew or a travel crew, matched to the size and timing of the job.</li>
    <li><strong>You get an itemized bid.</strong> Every task priced as its own line, by phase, with nothing buried.</li>
    <li><strong>We mobilize on your schedule.</strong> Rough, final and punch cleans timed to your trades and inspections.</li>
    <li><strong>Closeout on time.</strong> Walkthrough, punch items re-cleaned, checklists and photos for your closeout package.</li>
  </ol>
</section>

<section class="wrap bidstrip">
  <div>
    <p class="eyebrow">What we need to bid</p>
    <h2>Five answers get you a bid</h2>
    {need}
  </div>
  <div class="bidstrip-cta">
    <a class="btn" href="quote.html">Request a Bid</a>
    <a class="btn btn-ghost" href="quote.html#specs">Send Your Specs</a>
  </div>
</section>

<!--PROOF-->

<section class="wrap split">
  <div class="panel">
    <p class="eyebrow">Our methods</p>
    <h2>Capture it. Don't move it.</h2>
    <p>Construction dust that is swept or blown just lands somewhere else. Our crews capture it with HEPA vacuums and microfiber, use water and pH-neutral products before stronger chemistry, and keep wash water out of storm drains.</p>
    <p><a href="methods.html">How we clean differently</a></p>
  </div>
  <div class="panel">
    <p class="eyebrow">Above Eye Level Cleaning</p>
    <h2>The ceiling gets cleaned once. Then it gets dusty again.</h2>
    <p>Open decks, beams, ducts and fixtures collect dust long after turnover. Our sister brand schedules recurring high dusting for stores, warehouses and food facilities.</p>
    <p><a href="families/overhead-high-dusting.html">Overhead services</a> · <a href="{AELC_URL}" rel="noopener">AboveEyeLevelCleaning.com</a></p>
  </div>
</section>
"""

    methods = """
<section class="wrap narrow">
  <p class="eyebrow">Our methods</p>
  <h1>How Beyond Klean cleans differently</h1>
  <p class="lede">Construction cleaning has a habit of moving dirt around: blowing dust off ledges, sweeping it into the air and attacking residue with the strongest chemical on the truck. Our standard is the opposite.</p>

  <h2>1. Capture first</h2>
  <p>Dust is removed from the building, not relocated. Our crews use sealed HEPA vacuums at the surface, damp microfiber and wet methods. OSHA's construction silica standard already restricts dry sweeping, dry brushing and compressed-air cleaning where silica dust is present; we treat that as the baseline everywhere.</p>

  <h2>2. Top down, inside out</h2>
  <p>Overhead surfaces are cleaned before walls, walls before floors, and rooms toward exits, so nothing falls onto a surface that is already clean.</p>

  <h2>3. Least-aggressive chemistry</h2>
  <p>Mechanical removal and water come first, then pH-neutral cleaners, then targeted products only where needed, tested in a hidden spot. New stone, grout, floor finishes, coatings and glass are at their most vulnerable right after installation.</p>

  <h2>4. Products matched to the surface and the warranty</h2>
  <p>Floor, countertop, glass and fixture manufacturers publish care requirements. Following them protects the owner's warranty and avoids etching, hazing and dulling.</p>

  <h2>5. Water stays out of storm drains</h2>
  <p>Exterior washing uses recovery equipment or drain protection, so wash water carrying concrete fines, oils and detergents is collected instead of discharged.</p>

  <h2>6. Clean air at turnover</h2>
  <p>Ductwork protection, temporary return filters, final filter replacement and a thorough final clean support the project's construction indoor air quality plan before flush-out and occupancy.</p>

  <h2>7. Documented, not promised</h2>
  <p>We provide the Safety Data Sheets and technical data for the products we use, along with room checklists and photos. We describe methods specifically instead of making blanket claims like "non-toxic" or "eco-friendly."</p>

  <h2>Standards we reference</h2>
  <ul>
    <li>OSHA 29 CFR 1926.1153, respirable crystalline silica in construction</li>
    <li>SMACNA IAQ Guidelines for Occupied Buildings Under Construction, used by LEED construction IAQ credits</li>
    <li>EPA Safer Choice for cleaning products and Green Seal GS-42 for cleaning services</li>
    <li>FTC Green Guides for environmental marketing claims</li>
    <li>IWCA and glass industry guidance on construction glass protection and cleaning</li>
  </ul>
  <p><a class="btn" href="quote.html">Request a Bid</a></p>
</section>"""

    gcs = f"""
<section class="wrap narrow">
  <p class="eyebrow">For general contractors</p>
  <h1>One crew for every cleaning scope on your job</h1>
  <p class="lede">Rough clean, final clean, glass, floors, overhead, kitchens and the touch-up before the owner walk. Send us the scope and we bid it line by line, then show up when your schedule says.</p>
  <h2>What we keep off your punch list</h2>
  <ul class="check">
    <li>Final cleaning scopes that leave out overhead structure, glass or floor finish, then turn into change orders.</li>
    <li>Dust swept into the air that settles back on finishes a week later.</li>
    <li>Residue removal that etches stone, scratches glass or voids a floor warranty.</li>
    <li>Missing insurance certificates and unclear re-clean terms at the end of the job.</li>
    <li>A failed Substantial Completion walk because the building was not inspection-clean.</li>
  </ul>
  <h2>What we need to bid</h2>
  {need}
  <h2>What helps us sharpen the number</h2>
  <ul class="check">
    <li>Drawings and the finish schedule</li>
    <li>Your Division 01 cleaning section (often 01 74 13, 01 74 23 or 01 77 00)</li>
    <li>Phase dates, inspection dates and the owner walk date</li>
    <li>Site access rules, working hours and who provides water, power and lifts</li>
  </ul>
  <p><a class="btn" href="quote.html">Request a Bid</a> <a class="btn btn-ghost" href="quote.html#specs">Send Your Specs</a></p>
</section>"""

    types = ["Residential", "Multifamily", "Commercial office", "Retail or store opening", "Restaurant or food service",
             "Hospitality", "Industrial or warehouse", "Healthcare", "Education or institutional", "Government",
             "Military", "Other"]
    type_opts = "".join(f"<option>{e(t)}</option>" for t in types)
    quote = f"""
<section class="wrap narrow">
  <p class="eyebrow">Request a bid</p>
  <h1>Send us your scope</h1>
  <p class="lede">Five answers get you a bid: what kind of project, when it has to be done, where it is, how big it is and what needs cleaning. Specs and plans help but aren't required.</p>
  <form class="form panel" data-demo data-bidform>
    <fieldset class="bidbox">
      <legend>What needs cleaning</legend>
      <ul class="bidlist" data-bidlist><li class="empty">Nothing on your list yet. Add services below or from any service page.</li></ul>
      <div class="finder finder-add" data-finder data-mode="add">
        <label for="add-q" class="small">Add a service</label>
        <div class="finder-box">
          <input id="add-q" type="text" autocomplete="off" spellcheck="false" placeholder="Start typing: “final clean”, “windows”, “VCT”" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="add-list">
          <button class="btn btn-sm" type="button" data-add-typed>Add</button>
        </div>
        <ul class="finder-list" id="add-list" role="listbox" hidden></ul>
      </div>
      <input type="hidden" name="tasks" data-bidfield>
    </fieldset>
    <div class="row">
      <label for="r-type">Project type<select id="r-type" name="project_type" required><option value="">Choose one</option>{type_opts}</select></label>
      <label for="r-date">Needed by<input id="r-date" type="date" name="needed_by" required></label>
    </div>
    <div class="row">
      <label for="r-city">City and state<input id="r-city" name="city" placeholder="Tampa, FL" required></label>
      <label for="r-zip">ZIP code<input id="r-zip" name="zip" inputmode="numeric" maxlength="10" required></label>
    </div>
    <label for="r-sf">Approximate square feet<input id="r-sf" name="sqft" inputmode="numeric" placeholder="25,000"></label>
    <label for="r-desc">Anything else we should know<textarea id="r-desc" name="details" placeholder="Phases, ceiling heights, inspection dates, access rules"></textarea></label>
    <label for="r-files" id="specs">Specs, plans or photos (optional)<input id="r-files" type="file" name="files" multiple></label>
    <div class="row">
      <label for="r-name">Your name<input id="r-name" name="name" required></label>
      <label for="r-co">Company<input id="r-co" name="company"></label>
    </div>
    <div class="row">
      <label for="r-phone">Phone<input id="r-phone" type="tel" name="phone" required></label>
      <label for="r-email">Email<input id="r-email" type="email" name="email" required></label>
    </div>
    <button class="btn" type="submit">Request my bid</button>
    <div class="notice" tabindex="-1" hidden>
      <p><strong>Got it. Your reference is <span class="mono" data-ref></span>.</strong> We'll confirm crew availability and send an itemized bid.</p>
      <p class="small">Preview build: requests aren't sent yet.</p>
    </div>
  </form>
</section>"""

    about = f"""
<section class="wrap narrow">
  <p class="eyebrow">About</p>
  <h1>About Beyond Klean</h1>
  <p class="lede">Beyond Klean is a construction and specialty cleaning company. We clean new and renovated buildings of every type, from a single apartment turn to a full campus, with methods built for new finishes.</p>
  <h2>What we do</h2>
  <p>Our crews handle rough, final and touch-up cleaning, glass, floors, kitchens, overhead structure, exteriors and closeout for general contractors, property managers and building owners. Every bid is itemized, and every job closes out with checklists and photos.</p>
  <h2>Where we work</h2>
  <p>Home crews cover the Southeast. Travel crews mobilize nationwide for larger projects. Send the city and ZIP code and we'll confirm availability before we bid.</p>
  <h2>How we work</h2>
  <p>Capture dust instead of moving it. Use the least aggressive chemistry that does the job. Follow the manufacturer's care guide on every new finish. Assign regulated work only to licensed, certified technicians.</p>
<!--LEADERSHIP-->
  <h2>Proof and paperwork</h2>
  <p>See our <a href="projects.html">projects</a>, how our crews work under our <a href="safety.html">safety and compliance</a> program, our <a href="methods.html">cleaning methods</a>, and the <a href="capability-statement.html">capability statement</a> for government and institutional buyers.</p>
  <h2>Our sister brand</h2>
  <p>Recurring overhead and high dusting is handled through <a href="{AELC_URL}" rel="noopener">Above Eye Level Cleaning</a>, which keeps open ceilings, structure and fixtures clean after the building opens.</p>
  <p><a class="btn" href="quote.html">Request a Bid</a></p>
</section>"""

    return [
        ("index.html", "Beyond Klean | Construction & Specialty Cleaning",
         "Post-construction and specialty cleaning for general contractors, property managers and building owners. Itemized bids, our own crews, nationwide.",
         None, home, None),
        ("methods.html", "Our Cleaning Methods | Beyond Klean",
         "Capture-first dust removal, least-aggressive chemistry, warranty-safe products and documented results.",
         "Our Methods", methods, "methods.html"),
        ("general-contractors.html", "Construction Cleaning for General Contractors | Beyond Klean",
         "One crew for rough, final, overhead, glass, floor and kitchen cleaning scopes, bid line by line.",
         "For General Contractors", gcs, "general-contractors.html"),
        ("quote.html", "Request a Bid | Beyond Klean",
         "Request an itemized bid for construction or specialty cleaning. Project type, deadline, location, size and tasks.",
         "Request a Bid", quote, "quote.html"),
        ("about.html", "About Beyond Klean", "Beyond Klean is a construction and specialty cleaning company working nationwide.",
         "About", about, "about.html"),
    ]
