"""Site-wide content: glossary, general FAQ and the static pages (home, methods, GCs, join, quote, about)."""
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
  ("What is Beyond Klean?", "Beyond Klean is a specialty cleaning procurement platform for construction and commercial buildings. We help builders and owners define the cleaning scope and connect them with independent, verified contractors who quote and perform the work."),
  ("Does Beyond Klean do the cleaning itself?", "No. Independent, verified contractors perform the work. Beyond Klean handles scoping, matching, coordination and documentation, and the contractor that quotes the job performs, insures and warrants it."),
  ("How is Beyond Klean different from a lead-selling directory?", "We do not sell your request to a list of companies. Each request is scoped and qualified, then matched to contractors verified for that specific work, with capacity confirmed before an introduction."),
  ("What areas does Beyond Klean serve?", "The service library is national. Contractor coverage is being built market by market, starting in Florida, and we tell you plainly whether a verified contractor covers your location."),
  ("What kinds of buildings does Beyond Klean cover?", "Commercial, retail, grocery, restaurant, warehouse, industrial, office, healthcare, education, hospitality and multifamily projects, from tenant improvements to ground-up construction."),
  ("How many cleaning services does Beyond Klean list?", "438 distinct services across 20 service families, searchable under nearly a thousand names that contractors, specs and buyers use for them."),
  ("Is there a cost to request a quote?", "No. Requesting a scope review and quote is free for project owners and general contractors."),
  ("What is the relationship with Above Eye Level Cleaning?", "Above Eye Level Cleaning is our partner program for recurring overhead and high-dusting work. Beyond Klean covers construction turnover, and AELC keeps overhead surfaces clean after the building opens."),
 ]),
 ("For general contractors", [
  ("How do I get a cleaning sub for my project?", "Request a quote or send your bid package. We review the scope, phases, schedule and site details, then introduce a verified contractor who prices the work directly with you."),
  ("Can you price from my drawings and specs?", "Yes. Send drawings, the Division 01 cleaning section and any finish schedules. The matched contractor prices the scope; we help make sure nothing is missing, such as overhead cleaning or glass."),
  ("Can one request cover rough, final and touch-up cleaning?", "Yes. Most construction cleaning is bid by phase. One request can cover every phase, with each priced separately."),
  ("What if I need a cleaning crew tomorrow?", "Tell us the deadline. We only promise a response after a contractor confirms capacity, and we will tell you plainly if we cannot cover it in time."),
  ("Do your contractors carry insurance?", "Contractors must provide current insurance certificates before they are routed work, and expired documents pause routing automatically. Project-specific requirements such as additional insured status are confirmed by the contractor."),
  ("Who do I pay?", "You contract with and pay the cleaning contractor that performs the work, under the terms you agree with them."),
  ("Can you help with multi-site rollouts?", "Yes. National and regional programs can use one scope and checklist across many sites, with local verified contractors where coverage exists."),
  ("What documentation do I get at closeout?", "Contractors can provide photo documentation, room checklists and product data sheets for the cleaners used, which help with closeout packages and LEED or IAQ requirements."),
 ]),
 ("For owners and facility managers", [
  ("When should cleaning be planned on a construction project?", "Early. Overhead cleaning, glass, floors and kitchen equipment are often missed in scopes. Writing them in during bidding prevents change orders at the end."),
  ("Why is my new building still dusty after the final clean?", "Usually because overhead surfaces were not in scope, or dust was moved instead of captured. HEPA capture and overhead cleaning fix the cause, not just the symptom."),
  ("Can Beyond Klean help after we open?", "Yes. Recurring overhead and high dusting goes through Above Eye Level Cleaning, and floor, glass and specialty services can be arranged as needed."),
  ("Is construction cleaning the same as janitorial service?", "No. Construction cleaning removes construction residue from new finishes: dust, labels, adhesive, grout haze and debris. Janitorial service maintains an occupied building."),
  ("How do I know the cleaning was done right?", "Ask for room checklists and before-and-after photos, and walk the space with the punch list. We track complaints so performance is visible."),
  ("Can cleaning be scheduled around our operations?", "Yes. Remodels in operating stores, offices and healthcare facilities are commonly cleaned overnight or in phases."),
  ("What should I check at the owner walk?", "Look up at ceilings and fixtures, open drawers, check glass in daylight, look behind toilets and under sinks, and check floor edges and corners."),
  ("Who is responsible if something is damaged during cleaning?", "The contractor performing the work is responsible under its contract and insurance. That is one reason we verify insurance before routing."),
 ]),
 ("For cleaning contractors", [
  ("How do I join the Beyond Klean network?", "Apply through the Join the Network page with your company details, services, coverage area, insurance and references. We verify before any project is routed."),
  ("Does Beyond Klean sell leads?", "No. Requests are scoped and matched to verified contractors with capacity, not sold to a list."),
  ("What are the network tiers?", "Applicant, verified generalist, verified specialist and conditional specialist. Your tier determines which scopes are routed to you."),
  ("Do I set my own prices?", "Yes. The executing contractor prices and approves every proposal. Beyond Klean does not set your price."),
  ("Can specialty contractors join?", "Yes. Floor care, glass, high dusting, kitchen, pressure washing and other specialists are needed, and regulated specialties are reviewed case by case."),
  ("What documents are required?", "Legal business information, insurance certificates, relevant licenses, safety program information, references and your service area and capacity."),
  ("Is there a cost to join?", "Commercial terms are discussed during onboarding and agreed in writing before any work is routed."),
  ("Can I serve only part of a state?", "Yes. You set your service area and the scopes you want, and routing follows them."),
 ]),
 ("Green and safer cleaning", [
  ("What makes Beyond Klean's approach greener?", "Methods first: capture dust with HEPA instead of blowing it around, use microfiber and water before chemicals, pick pH-neutral and low-VOC products matched to the surface, and recover wash water instead of sending it to storm drains."),
  ("Do you use non-toxic cleaning products?", "We avoid blanket claims like non-toxic. We describe the specific methods and products used and provide their data sheets, because every product has handling requirements."),
  ("What is capture-first cleaning?", "Removing dust and soil from the building, with HEPA vacuums and microfiber, instead of moving it into the air or onto other surfaces."),
  ("Why does least-aggressive chemistry matter on new buildings?", "New finishes are at their most vulnerable. Harsh acids and solvents can etch stone, dull coatings, damage grout and void warranties."),
  ("Are green cleaning products less effective?", "Not when they are matched to the job. Many construction residues come off with mechanical methods and neutral products; stronger chemistry is reserved for when it is truly needed."),
  ("Do you follow green building requirements?", "Contractors can follow project IAQ plans, document products and methods, and support LEED documentation for cleaning-related credits."),
  ("What certifications matter for green cleaning?", "EPA Safer Choice certifies products, and Green Seal GS-42 certifies cleaning service providers. Project specs may name others."),
  ("How is wash water handled?", "Exterior washing uses recovery equipment or drain protection so dirty water does not enter storm drains."),
 ]),
 ("Pricing and scheduling", [
  ("How is construction cleaning priced?", "By square foot, by phase, by crew-day or by line item, depending on scope. Overhead work, glass and floor care are often priced separately."),
  ("What affects the price most?", "Square footage, ceiling height and access, number of phases, finish types, the amount of residue, schedule pressure and night or weekend work."),
  ("Why do you not publish prices?", "Prices depend on local labor, access and scope. We provide pricing factors, and the contractor prices after reviewing the actual project."),
  ("How far in advance should cleaning be booked?", "As early as the bid phase. Final cleaning is scheduled around inspection dates, and crews book up near quarter-end and holiday openings."),
  ("Is night work more expensive?", "Usually, because of labor premiums. It is often worth it for operating stores and occupied buildings."),
  ("Are re-cleans extra?", "That depends on the contract. Clear re-clean terms in the scope avoid disputes at the end of the job."),
  ("How long does a final clean take?", "From one day for a small tenant space to several weeks for large buildings cleaned in phases."),
  ("Can cleaning be split between phases of occupancy?", "Yes. Each area can be final-cleaned and protected as it is handed over."),
 ]),
]


def static_pages(n_tasks, n_names, n_faq, fam_cards, AELC_URL, phase_counts, task_options):
    phase_bar = "".join(
        f'<a href="services.html#{k}"><span class="eyebrow">{e(p)}</span><strong>{n}</strong><span class="small muted">tasks</span></a>'
        for p, k, n in phase_counts)
    home = f"""
<section class="hero">
  <div class="wrap hero-in">
    <p class="eyebrow">Specialty construction cleaning · procurement network</p>
    <h1>Every cleaning task your project needs. One place to get it done.</h1>
    <p class="lede">Beyond Klean scopes specialty and post-construction cleaning for general contractors and owners, then matches it to verified contractors who use capture-first, safer-chemistry methods.</p>
    <div class="hero-cta">
      <a class="btn" href="quote.html">Request a Quote</a>
      <a class="btn btn-light" href="quote.html#bid">Submit a Bid Package</a>
      <a class="btn btn-light" href="join.html">Join the Network</a>
    </div>
    <div class="statrow" role="list">
      <div role="listitem"><strong>{n_tasks}</strong><span>distinct services</span></div>
      <div role="listitem"><strong>{n_names:,}</strong><span>names we answer to</span></div>
      <div role="listitem"><strong>{n_faq:,}</strong><span>answered questions</span></div>
      <div role="listitem"><strong>20</strong><span>service families</span></div>
    </div>
  </div>
</section>

<section class="wrap">
  <p class="eyebrow">By project stage</p>
  <h2>From rough clean to recurring overhead care</h2>
  <p class="lede">Most construction cleaning scopes stop at what you can reach. Ours follow the whole project: debris during construction, the final clean before Substantial Completion, the touch-up before the owner walk, and the high dusting that keeps it clean after opening.</p>
  <div class="phasebar">{phase_bar}</div>
</section>

<section class="wrap">
  <p class="eyebrow">Service families</p>
  <h2>Twenty families. Every surface, every stage.</h2>
  <div class="fgrid">{fam_cards}</div>
  <p><a class="btn btn-ghost" href="services.html">Search all {n_tasks} services</a></p>
</section>

<section class="wrap">
  <p class="eyebrow">How it works</p>
  <h2>Scoped first. Matched second. Quoted by the contractor who does the work.</h2>
  <ol class="steps">
    <li><strong>Describe the work.</strong> Facility type, project stage, square footage, heights, surfaces, deadline, plans and photos.</li>
    <li><strong>We qualify the scope.</strong> We check for missing items like overhead, glass and floor care, and flag regulated work.</li>
    <li><strong>We match a verified contractor.</strong> Insurance, specialty and current capacity are confirmed before any introduction.</li>
    <li><strong>The contractor quotes.</strong> The company performing the work prices it, signs it and warrants it.</li>
    <li><strong>Work is documented.</strong> Checklists, photos and product data sheets for your closeout package.</li>
  </ol>
</section>

<section class="wrap split">
  <div class="panel">
    <p class="eyebrow">Our methods</p>
    <h2>Capture it. Don't move it.</h2>
    <p>Construction dust that is swept or blown just lands somewhere else. Our network captures it with HEPA vacuums and microfiber, uses water and pH-neutral products before stronger chemistry, and keeps wash water out of storm drains.</p>
    <p><a href="methods.html">How we clean differently</a></p>
  </div>
  <div class="panel">
    <p class="eyebrow">Above Eye Level Cleaning</p>
    <h2>The ceiling gets cleaned once. Then it gets dusty again.</h2>
    <p>Open decks, beams, ducts and fixtures collect dust long after turnover. Our partner program schedules recurring high dusting for stores, warehouses and food facilities.</p>
    <p><a href="families/overhead-high-dusting.html">Overhead services</a> · <a href="{AELC_URL}" rel="noopener">AboveEyeLevelCleaning.com</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <p class="eyebrow" style="color:inherit">FAQ library</p>
    <h2>{n_faq:,} straight answers.</h2>
    <p class="lede">Who cleans the ceiling in a new grocery store? Can LVT be waxed? How do you get grout haze off porcelain? Ask it the way you'd say it.</p>
    <p><a class="btn" href="faq.html">Search the FAQ library</a></p>
  </div>
</section>
"""

    methods = """
<section class="wrap narrow">
  <p class="eyebrow">Our methods</p>
  <h1>How Beyond Klean cleans differently</h1>
  <p class="lede">Construction cleaning has a habit of moving dirt around: blowing dust off ledges, sweeping it into the air and attacking residue with the strongest chemical on the truck. Our standard is the opposite.</p>

  <h2>1. Capture first</h2>
  <p>Dust is removed from the building, not relocated. Crews use sealed HEPA vacuums at the surface, damp microfiber and wet methods. OSHA's construction silica standard already restricts dry sweeping, dry brushing and compressed-air cleaning where silica dust is present; we treat that as the baseline everywhere.</p>

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
  <p>Contractors provide the Safety Data Sheets and technical data for the products they use, along with checklists and photos. We describe methods specifically instead of making blanket claims like "non-toxic" or "eco-friendly."</p>

  <h2>Standards we reference</h2>
  <ul>
    <li>OSHA 29 CFR 1926.1153, respirable crystalline silica in construction</li>
    <li>SMACNA IAQ Guidelines for Occupied Buildings Under Construction, used by LEED construction IAQ credits</li>
    <li>EPA Safer Choice for cleaning products and Green Seal GS-42 for cleaning services</li>
    <li>FTC Green Guides for environmental marketing claims</li>
    <li>IWCA and glass industry guidance on construction glass protection and cleaning</li>
  </ul>
  <p><a class="btn" href="quote.html">Request a scope review</a></p>
</section>"""

    gcs = f"""
<section class="wrap narrow">
  <p class="eyebrow">For general contractors</p>
  <h1>One call for every cleaning scope on your job</h1>
  <p class="lede">Rough clean, final clean, glass, floors, overhead, kitchens and the touch-up before the owner walk. Beyond Klean scopes it with you and brings in verified contractors who price it directly.</p>
  <h2>What we help you avoid</h2>
  <ul class="check">
    <li>Final cleaning scopes that leave out overhead structure, glass or floor finish, then turn into change orders.</li>
    <li>Crews that sweep dust into the air and leave the building dusty a week later.</li>
    <li>Residue removal that etches stone, scratches glass or voids a floor warranty.</li>
    <li>Missing insurance certificates and unclear re-clean terms at the end of the job.</li>
    <li>A failed Substantial Completion walk because the building was not inspection-clean.</li>
  </ul>
  <h2>What to send us</h2>
  <ul class="check">
    <li>Drawings and the finish schedule</li>
    <li>Your Division 01 cleaning section (often 01 74 13, 01 74 23 or 01 77 00)</li>
    <li>Phase dates, inspection dates and the owner walk date</li>
    <li>Site access rules, working hours and who provides water, power and lifts</li>
  </ul>
  <p><a class="btn" href="quote.html#bid">Submit a bid package</a> <a class="btn btn-ghost" href="services.html">Browse {n_tasks} services</a></p>
</section>"""

    join = """
<section class="wrap narrow">
  <p class="eyebrow">Join the network</p>
  <h1>Specialty cleaning contractors: get matched to real projects</h1>
  <p class="lede">Beyond Klean doesn't sell leads. We scope projects, qualify them and route them to verified contractors with the right specialty and capacity. You price and perform the work.</p>
  <h2>Network tiers</h2>
  <ul class="check">
    <li><strong>Applicant.</strong> Information received, not yet verified. No project routing.</li>
    <li><strong>Verified generalist.</strong> Identity, insurance and experience verified. Routed general construction cleaning scopes.</li>
    <li><strong>Verified specialist.</strong> Additional technical qualifications and references. Routed matching specialty scopes.</li>
    <li><strong>Conditional specialist.</strong> Regulated or higher-risk capabilities, reviewed case by case. Manual approval only.</li>
  </ul>
  <form class="form panel" data-demo>
    <div class="row">
      <label for="j-co">Company name<input id="j-co" name="company" required></label>
      <label for="j-name">Contact name<input id="j-name" name="name" required></label>
    </div>
    <div class="row">
      <label for="j-email">Email<input id="j-email" type="email" name="email" required></label>
      <label for="j-phone">Phone<input id="j-phone" type="tel" name="phone"></label>
    </div>
    <div class="row">
      <label for="j-area">Service area<input id="j-area" name="area" placeholder="Cities, counties or state"></label>
      <label for="j-crew">Crew capacity<input id="j-crew" name="crew" placeholder="Crews and people available"></label>
    </div>
    <label for="j-svc">Services and specialties<textarea id="j-svc" name="services" placeholder="Rough and final clean, high dusting, floor care, glass, pressure washing…"></textarea></label>
    <label for="j-ins">Insurance and licenses<textarea id="j-ins" name="insurance" placeholder="General liability, workers' compensation, licenses held"></textarea></label>
    <button class="btn" type="submit">Apply to join</button>
    <p class="notice" tabindex="-1" hidden>This is a preview build, so applications aren't sent yet. On the live site this goes to the Beyond Klean network team for verification.</p>
  </form>
</section>"""

    quote = f"""
<section class="wrap narrow">
  <p class="eyebrow">Request a quote</p>
  <h1>Tell us about the project</h1>
  <p class="lede">The more we know about stage, size, heights and surfaces, the faster we can match a verified contractor. Plans and photos help.</p>
  <form class="form panel" data-demo>
    <div class="row">
      <label for="r-name">Your name<input id="r-name" name="name" required></label>
      <label for="r-co">Company<input id="r-co" name="company"></label>
    </div>
    <div class="row">
      <label for="r-email">Email<input id="r-email" type="email" name="email" required></label>
      <label for="r-role">Your role<select id="r-role" name="role"><option>General contractor</option><option>Owner or developer</option><option>Facility or property manager</option><option>Architect or designer</option><option>Other</option></select></label>
    </div>
    <label for="r-task">Main service needed<select id="r-task" name="task"><option value="">Choose a service</option>{task_options}</select></label>
    <div class="row">
      <label for="r-fac">Facility type<select id="r-fac" name="facility"><option>Retail</option><option>Grocery</option><option>Restaurant</option><option>Warehouse or industrial</option><option>Office</option><option>Healthcare</option><option>Education</option><option>Hospitality</option><option>Multifamily</option><option>Other</option></select></label>
      <label for="r-stage">Project stage<select id="r-stage" name="stage"><option>Bidding</option><option>Under construction</option><option>Near completion</option><option>Occupied or operating</option></select></label>
    </div>
    <div class="row">
      <label for="r-sf">Approx. square feet<input id="r-sf" name="sqft" inputmode="numeric"></label>
      <label for="r-ht">Highest ceiling (ft)<input id="r-ht" name="height" inputmode="numeric"></label>
    </div>
    <div class="row">
      <label for="r-loc">City and state<input id="r-loc" name="location"></label>
      <label for="r-date">Needed by<input id="r-date" type="date" name="date"></label>
    </div>
    <label for="r-desc" id="bid">Scope or bid package details<textarea id="r-desc" name="details" placeholder="Phases, surfaces, inspection dates, access constraints, links to plans"></textarea></label>
    <label for="r-files">Plans and photos<input id="r-files" type="file" name="files" multiple></label>
    <button class="btn" type="submit">Request a scope review</button>
    <p class="notice" tabindex="-1" hidden>This is a preview build, so requests aren't sent yet. On the live site this goes to the Beyond Klean intake team, and you get an acknowledgment right away.</p>
  </form>
</section>"""

    about = f"""
<section class="wrap narrow">
  <p class="eyebrow">About</p>
  <h1>About Beyond Klean</h1>
  <p class="lede">Beyond Klean is a national specialty cleaning procurement platform. We built the most complete library of construction and specialty cleaning services we know of, {n_tasks} services and {n_faq:,} answers, so buyers can specify the work correctly and find the right contractor to do it.</p>
  <h2>What we do</h2>
  <p>We help general contractors, developers, property owners and facility managers scope specialty cleaning, then connect them with independent, verified contractors. We handle coordination and documentation. The contractor that quotes the job performs it, insures it and warrants it.</p>
  <h2>What we don't do</h2>
  <p>We don't sell your request to a list of companies, invent local offices, or claim capabilities our network doesn't have. Where we don't yet have verified coverage, we say so.</p>
  <h2>Our partner program</h2>
  <p>Recurring overhead and high dusting is handled through <a href="{AELC_URL}" rel="noopener">Above Eye Level Cleaning</a>, which keeps open ceilings, structure and fixtures clean after the building opens.</p>
  <p><a class="btn" href="quote.html">Request a quote</a> <a class="btn btn-ghost" href="join.html">Join the network</a></p>
</section>"""

    return [
        ("index.html", "Beyond Klean | Specialty Construction Cleaning Network",
         f"Scope and source {n_tasks} specialty and post-construction cleaning services, matched to verified contractors using capture-first, safer-chemistry methods.",
         None, home, None),
        ("methods.html", "Our Cleaning Methods | Beyond Klean",
         "Capture-first dust removal, least-aggressive chemistry, warranty-safe products and documented results.",
         "Our Methods", methods, "methods.html"),
        ("general-contractors.html", "Construction Cleaning for General Contractors | Beyond Klean",
         "One source for rough, final, overhead, glass, floor and kitchen cleaning scopes, priced by verified contractors.",
         "For General Contractors", gcs, "general-contractors.html"),
        ("join.html", "Join the Contractor Network | Beyond Klean",
         "Specialty cleaning contractors: apply to be verified and matched to qualified construction and commercial projects.",
         "Join the Network", join, "join.html"),
        ("quote.html", "Request a Quote | Beyond Klean",
         "Request a scope review and quote for construction or specialty cleaning.", "Request a Quote", quote, None),
        ("about.html", "About Beyond Klean", "Beyond Klean is a national specialty cleaning procurement platform.",
         "About", about, None),
    ]
