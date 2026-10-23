"""All site content for the Everglades Restorations & Land Clearing preview build.

Anything wrapped in [[double brackets]] renders as an obvious yellow placeholder.
Fill those in (or replace the brackets with real text) and rebuild.
"""

BIZ = {
    "name": "Everglades Restorations & Land Clearing Inc.",
    "short": "Everglades Restorations",
    "founded": "1992",
    "years": "35",
    "phone": "[[(XXX) XXX-XXXX]]",
    "phone_tel": "",  # e.g. "+19545551234" — leave empty until known
    "email": "[[info@XXX.com]]",
    "address": "[[Street Address XXX]]",
    "city_state": "[[City]], FL [[ZIP]]",
    "hours": "Mon–Sat [[7:00 AM – 6:00 PM]] · Storm response 24/7",
    "license": "[[FL Contractor License # XXX]]",
    "insurance": "[[General Liability $X,XXX,XXX / Auto / Workers' Comp]]",
    "bonding": "[[Bonding capacity $X,XXX,XXX single / $X,XXX,XXX aggregate]]",
    "fema": "[[FEMA Vendor / Contract # XXX]]",
    "sam_uei": "[[SAM.gov UEI XXX]]",
    "cage": "[[CAGE Code XXX]]",
    "usace": "[[Army Corps of Engineers project / permit #s XXX]]",
    "naics": "[[238910 Site Preparation · 237990 · 562119 — confirm]]",
    "youtube": "[[YouTube channel link XXX]]",
    "gbp": "[[Google Business Profile link XXX]]",
}

# ---------------------------------------------------------------- services
SERVICES = [
    {
        "slug": "land-clearing",
        "name": "Land Clearing",
        "group": "land",
        "h1": "Land Clearing in South Florida",
        "lead": "Residential lots, acreage, ranch land and commercial sites, cleared right the first time by a crew that has been doing it since 1992.",
        "aka": "lot clearing, brush clearing, underbrush removal, palmetto removal, acreage clearing, tree and stump removal, pasture clearing, right-of-way clearing",
        "intro": [
            "Whether it's a single homesite in Southwest Ranches or two hundred acres of overgrown pasture near Lake Okeechobee, land clearing in South Florida is its own kind of work. Limestone just under the surface, high water tables, protected trees and wetland edges all change how a site has to be cleared.",
            "We plan every job around what comes next: a house pad, a pond, a pasture, a solar field, or a restored wetland. That means the right machines, the right permits, and a site left ready for the next trade.",
        ],
        "includes": [
            "Residential lot clearing for new homes, pools and house pads",
            "Commercial and development site clearing",
            "Acreage, ranch and pasture clearing",
            "Right-of-way, utility and solar-field clearing",
            "Stump removal and root raking",
            "Debris hauled off, or mulched on site to save hauling costs",
        ],
        "equipment": ["Dozers [[models XXX]]", "Excavators [[models XXX]]", "Forestry mulchers [[XXX]]", "Dump trucks [[XXX]]"],
        "faqs": [
            ("How much does land clearing cost per acre?", "It depends on how thick the growth is, the size of the trees, whether there are wetlands, and whether debris is hauled away or mulched. See our full answer, with typical South Florida ranges, on the cost page.", "questions/land-clearing-cost-per-acre-south-florida/"),
            ("Do I need a permit to clear my land?", "In most of South Florida, yes — tree removal and any work near wetlands usually need a county or city permit, and sometimes state or federal approval. We help you sort it out before work starts.", "questions/do-i-need-a-permit-to-clear-land/"),
            ("Do you haul everything away?", "Your choice. We can haul and dispose of everything, or mulch it on site, which is often faster and less expensive.", None),
        ],
        "related": ["forestry-mulching", "site-prep-grading", "exotic-invasive-removal"],
    },
    {
        "slug": "forestry-mulching",
        "name": "Forestry Mulching",
        "group": "land",
        "h1": "Forestry Mulching",
        "lead": "Clear underbrush, palmetto and small trees in one pass — no burn piles, no hauling, and the topsoil stays where it belongs.",
        "aka": "brush mulching, mulching service, underbrush clearing, palmetto clearing, fire break clearing, trail cutting, fence line clearing",
        "intro": [
            "A forestry mulcher grinds brush and small trees into a layer of mulch right where they stand. It's the fastest, cleanest way to open up overgrown land without tearing up the ground.",
            "It's ideal for fence lines, trails, fire breaks, view corridors, survey lines, and lots where you want to keep the good trees and lose everything else.",
        ],
        "includes": [
            "Underbrush and palmetto clearing",
            "Selective clearing that saves the trees you want to keep",
            "Fire breaks and wildfire-risk reduction",
            "Trail, fence-line and survey-line clearing",
            "Invasive plant knock-down (Brazilian pepper and more)",
        ],
        "equipment": ["Tracked forestry mulchers [[models XXX]]", "Skid-steer mulching heads [[XXX]]"],
        "faqs": [
            ("Is forestry mulching better than regular land clearing?", "For brush, palmetto and small trees, usually yes — it's faster and leaves the soil protected. For big trees, stumps or building pads, traditional clearing is often the better fit.", "questions/forestry-mulching-vs-land-clearing/"),
            ("What happens to the mulch?", "It stays on the ground as a protective layer that holds moisture, reduces erosion and breaks down naturally.", None),
        ],
        "related": ["land-clearing", "exotic-invasive-removal", "hurricane-debris-removal"],
    },
    {
        "slug": "canal-pond-excavation",
        "name": "Canal, Lake & Pond Excavation",
        "group": "land",
        "h1": "Canal, Lake & Pond Excavation",
        "lead": "Retention ponds, lakes, canals and ditches dug, cleaned and shaped to spec — and lake banks rebuilt when erosion takes them.",
        "aka": "pond digging, retention pond construction, detention pond, lake excavation, canal dredging, canal cleaning, muck removal, lake bank erosion repair",
        "intro": [
            "South Florida runs on water management. New developments need retention and detention ponds, older neighborhoods need canals and ditches cleaned out, and HOA lake banks wash away a little more every storm season.",
            "We dig, clean and restore them — with long-reach equipment for canal work and the know-how to work around the drainage districts and permits that govern South Florida water.",
        ],
        "includes": [
            "Retention and detention pond construction",
            "Lake and pond digging for homes, ranches and developments",
            "Canal and ditch cleaning, dredging and muck removal",
            "Lake bank and canal bank erosion repair",
            "Swale and ditch excavation",
            "Fill produced from excavation, used on site or hauled",
        ],
        "equipment": ["Long-reach excavators [[XXX]]", "Amphibious excavator / marsh buggy [[confirm XXX]]", "Dozers [[XXX]]", "Dump trucks [[XXX]]"],
        "faqs": [
            ("Do I need a permit to dig a pond?", "Almost always. Ponds and canal work usually involve the county, the South Florida Water Management District, and sometimes a local drainage district. We'll walk you through it.", "questions/do-i-need-a-permit-to-clear-land/"),
            ("Can you fix our HOA's eroded lake banks?", "Yes. Lake bank restoration is one of the most common jobs we see for HOAs and property managers across Broward and Palm Beach.", None),
        ],
        "related": ["drainage-stormwater", "site-prep-grading", "wetland-restoration-mitigation"],
    },
    {
        "slug": "site-prep-grading",
        "name": "Site Prep & Grading",
        "group": "land",
        "h1": "Site Preparation & Grading",
        "lead": "From raw land to a build-ready pad: clearing, fill, rock, grading and compaction for homes, commercial sites and developments.",
        "aka": "site prep contractor, mass grading, house pad, building pad, fill dirt, rock plowing, driveway grading, laser grading",
        "intro": [
            "A good building starts with a good pad. We take a site from cleared to graded — bringing in fill and rock, setting elevations, and compacting to what the engineer and inspector want to see.",
            "In the Redland and Homestead area, that often means rock plowing: breaking up the limestone so the ground can be farmed or built on.",
        ],
        "includes": [
            "House pads and building pads",
            "Mass grading for developments",
            "Fill dirt and rock delivery and placement",
            "Rock plowing (Redland / Homestead limestone)",
            "Driveway and road base grading",
            "Compaction to spec",
        ],
        "equipment": ["Dozers [[XXX]]", "Excavators [[XXX]]", "Rollers / compactors [[XXX]]", "Dump trucks [[XXX]]"],
        "faqs": [
            ("Can you deliver fill dirt?", "Yes — fill and rock delivered, spread and compacted, or delivered only.", None),
            ("What is rock plowing?", "Rock plowing breaks up the shallow limestone common in south Miami-Dade so the land can be farmed, planted or built on.", None),
        ],
        "related": ["land-clearing", "drainage-stormwater", "canal-pond-excavation"],
    },
    {
        "slug": "wetland-restoration-mitigation",
        "name": "Wetland Restoration & Mitigation",
        "group": "env",
        "h1": "Wetland Restoration & Mitigation",
        "lead": "Earthwork that brings wetlands back: canal backfilling, road and spoil removal, re-grading to natural elevations, and mitigation-bank construction.",
        "aka": "wetland restoration contractor, wetland mitigation contractor, mitigation bank construction, hydrologic restoration, canal backfilling, spoil removal, ecosystem restoration",
        "intro": [
            "Restoration is in the name. Across South Florida, old roads, ditches and spoil piles cut wetlands off from the water they need. Putting it back takes heavy equipment run by people who understand what the finished landscape is supposed to do.",
            "We work alongside environmental consultants, engineers, agencies and prime contractors to move the earth exactly where the restoration plan calls for it.",
        ],
        "includes": [
            "Canal and ditch backfilling",
            "Old road, culvert and spoil-pile removal",
            "Re-grading to natural wetland elevations",
            "Mitigation-bank and mitigation-area construction",
            "Exotic vegetation removal ahead of restoration",
            "Work under Army Corps, state and water-management-district permits",
        ],
        "equipment": ["Amphibious excavator / marsh buggy [[confirm XXX]]", "Low-ground-pressure dozers [[XXX]]", "Long-reach excavators [[XXX]]"],
        "faqs": [
            ("Do you work as a subcontractor on large restoration projects?", "Yes. We regularly support prime contractors and agencies on earthwork and clearing scopes. See our government and agency page for capability details.", "who-we-serve/government-agencies/"),
            ("Can you clear land that has wetlands on it?", "Sometimes — with the right permits. Read our full answer on wetland clearing.", "questions/can-you-clear-land-with-wetlands/"),
        ],
        "related": ["exotic-invasive-removal", "canal-pond-excavation", "drainage-stormwater"],
    },
    {
        "slug": "exotic-invasive-removal",
        "name": "Exotic & Invasive Plant Removal",
        "group": "env",
        "h1": "Exotic & Invasive Plant Removal",
        "lead": "Melaleuca, Brazilian pepper and Australian pine removed mechanically, at scale — on preserves, conservation land, development sites and private property.",
        "aka": "melaleuca removal, Brazilian pepper removal, Australian pine removal, invasive tree removal, exotic vegetation removal, preserve maintenance",
        "intro": [
            "Invasive trees choke out native wetlands, block drainage, and are often required to be removed before a property can be developed or a preserve can be signed off.",
            "We remove them mechanically — cutting, mulching, root-raking and hauling — and coordinate follow-up treatment so they don't come back.",
        ],
        "includes": [
            "Melaleuca removal",
            "Brazilian pepper removal",
            "Australian pine removal",
            "Preserve and conservation-easement clean-up",
            "Exotic removal required for development sign-off",
            "Follow-up treatment by licensed applicators [[FDACS license # XXX or partner]]",
        ],
        "equipment": ["Forestry mulchers [[XXX]]", "Excavators with grapple / rake [[XXX]]", "Low-ground-pressure equipment [[XXX]]"],
        "faqs": [
            ("Is Brazilian pepper illegal to keep?", "Florida lists Brazilian pepper as a prohibited invasive plant, and many counties require it removed when land is developed. We can tell you what applies to your property.", None),
            ("Will the plants grow back?", "They will if the stumps aren't treated. We coordinate licensed follow-up treatment as part of the job.", None),
        ],
        "related": ["wetland-restoration-mitigation", "forestry-mulching", "land-clearing"],
    },
    {
        "slug": "drainage-stormwater",
        "name": "Drainage, Culverts & Stormwater",
        "group": "env",
        "h1": "Drainage, Culverts & Stormwater",
        "lead": "Culverts, swales, ditches, berms and outfalls that move water where it should go — on driveways, ranches, roads and developments.",
        "aka": "culvert installation, driveway culvert, swale repair, ditch work, stormwater contractor, berm and levee repair, flooding fix, headwall",
        "intro": [
            "If water sits where it shouldn't, something in the drainage is wrong — a crushed culvert, a filled-in swale, a ditch that's grown over, or a pad set too low.",
            "We find it and fix it: from a single driveway culvert to miles of roadside ditch and berm work for agencies and drainage districts.",
        ],
        "includes": [
            "Driveway and road culvert installation and replacement",
            "Swale and ditch re-grading",
            "Berm and levee repair",
            "Stormwater outfalls and headwalls",
            "Yard and property flooding fixes",
        ],
        "equipment": ["Excavators [[XXX]]", "Dozers [[XXX]]", "Dump trucks [[XXX]]"],
        "faqs": [
            ("Do you install driveway culverts?", "Yes — often the first fix for a flooded driveway or a new rural lot. Most counties require a permit, which we can help with.", None),
            ("Can you help with flooding on my property?", "Usually. We'll look at the grade, the swales and the culverts and tell you what's causing it.", None),
        ],
        "related": ["canal-pond-excavation", "site-prep-grading", "hurricane-debris-removal"],
    },
    {
        "slug": "hurricane-debris-removal",
        "name": "Hurricane & FEMA Debris Removal",
        "group": "env",
        "h1": "Hurricane & FEMA Debris Removal",
        "lead": "When a storm hits, roads, canals and properties need to be opened up fast. Our crews and equipment are ready to roll.",
        "aka": "hurricane debris removal, storm debris cleanup, FEMA debris removal contractor, emergency road clearing, vegetative debris removal, canal debris removal",
        "intro": [
            "After a hurricane, the first job is getting roads open and water flowing. Then comes the long haul of collecting, reducing and removing debris — documented the way FEMA reimbursement requires.",
            "We support cities, counties, drainage districts and prime contractors, and we help private property owners recover too.",
        ],
        "includes": [
            "Emergency road clearing (first push)",
            "Vegetative debris collection and hauling",
            "Canal and waterway debris removal",
            "Debris reduction by mulching / grinding",
            "Private property storm clean-up",
            "Documentation that supports FEMA reimbursement",
        ],
        "equipment": ["Grapple trucks / excavators [[XXX]]", "Dump trucks [[XXX]]", "Mulchers / grinders [[XXX]]"],
        "faqs": [
            ("Are you set up for FEMA-reimbursed work?", "Yes. " + "[[FEMA vendor / contract #s XXX]]" + " — see our credentials page.", "credentials/"),
            ("Can agencies pre-position you before storm season?", "Yes — we welcome pre-event contracts and standby agreements with cities, counties and districts.", "who-we-serve/government-agencies/"),
        ],
        "related": ["drainage-stormwater", "forestry-mulching", "land-clearing"],
    },
]
SVC = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- audiences
AUDIENCES = [
    {
        "slug": "government-agencies",
        "name": "Government & Agencies",
        "menu": "Government & Agencies",
        "h1": "For Government, Agencies & Prime Contractors",
        "lead": "Thirty-five years of South Florida site work, ready for public projects — as a prime on the right scope, or as the clearing and earthwork sub your team can count on.",
        "who": ["South Florida Water Management District", "Counties and cities", "FDOT and road projects", "Army Corps of Engineers prime contractors", "Drainage and water-control districts", "School districts and utilities"],
        "services": ["wetland-restoration-mitigation", "exotic-invasive-removal", "hurricane-debris-removal", "drainage-stormwater", "land-clearing", "canal-pond-excavation"],
    },
    {
        "slug": "contractors-developers",
        "name": "Contractors & Developers",
        "menu": "Contractors & Developers",
        "h1": "For General Contractors, Builders & Developers",
        "lead": "A clearing and earthwork crew that shows up when scheduled, brings its own equipment, and leaves a site ready for the next trade.",
        "who": ["General contractors", "Home builders", "Land developers", "Civil engineers", "Solar and utility developers", "Commercial property owners"],
        "services": ["land-clearing", "site-prep-grading", "canal-pond-excavation", "drainage-stormwater", "exotic-invasive-removal", "forestry-mulching"],
    },
    {
        "slug": "homeowners-ranches",
        "name": "Homeowners, Ranches & HOAs",
        "menu": "Homeowners, Ranches & HOAs",
        "h1": "For Homeowners, Ranches, Farms & HOAs",
        "lead": "Clearing a lot, opening up pasture, digging a pond, fixing a flooded driveway or rebuilding a lake bank — tell us about it and we'll get you taken care of.",
        "who": ["Homeowners and lot buyers", "Ranch and farm owners", "Equestrian properties", "HOAs and property managers", "Golf courses", "Churches, camps and land trusts"],
        "services": ["land-clearing", "forestry-mulching", "canal-pond-excavation", "drainage-stormwater", "site-prep-grading", "hurricane-debris-removal"],
    },
]
AUD = {a["slug"]: a for a in AUDIENCES}

# ---------------------------------------------------------------- areas
# Incorporated municipalities per county. Cities with a page in this build are in BUILT_CITIES.
COUNTIES = [
    {
        "slug": "broward", "name": "Broward County",
        "intro": "From the ranch and equestrian land of Southwest Ranches and Davie to the canals and lakes of Weston and Pembroke Pines, western Broward is home turf. Broward's tree-removal licenses and its Aquatic & Wetland Resources program govern much of the work here, along with local drainage districts.",
        "permit": "Broward County Tree Preservation (tree removal license) · Broward Aquatic & Wetland Resources · local drainage districts · SFWMD",
        "cities": ["Coconut Creek", "Cooper City", "Coral Springs", "Dania Beach", "Davie", "Deerfield Beach", "Fort Lauderdale", "Hallandale Beach", "Hillsboro Beach", "Hollywood", "Lauderdale-by-the-Sea", "Lauderdale Lakes", "Lauderhill", "Lazy Lake", "Lighthouse Point", "Margate", "Miramar", "North Lauderdale", "Oakland Park", "Parkland", "Pembroke Park", "Pembroke Pines", "Plantation", "Pompano Beach", "Sea Ranch Lakes", "Southwest Ranches", "Sunrise", "Tamarac", "West Park", "Weston", "Wilton Manors"],
        "unincorporated": ["Broadview Park", "Boulevard Gardens", "Roosevelt Gardens"],
    },
    {
        "slug": "miami-dade", "name": "Miami-Dade County",
        "intro": "South Miami-Dade is limestone country. In the Redland, Homestead and Florida City, clearing and site prep often mean rock plowing, and the Everglades edge brings wetland rules into play. Miami-Dade requires tree permits, a Class IV permit for work in wetlands, and Class I permits for mangroves.",
        "permit": "Miami-Dade tree removal / relocation permit · Class IV (freshwater wetlands) · Class I (coastal / mangroves) · Natural Forest Community permits · SFWMD · USACE",
        "cities": ["Aventura", "Bal Harbour", "Bay Harbor Islands", "Biscayne Park", "Coral Gables", "Cutler Bay", "Doral", "El Portal", "Florida City", "Golden Beach", "Hialeah", "Hialeah Gardens", "Homestead", "Indian Creek", "Key Biscayne", "Medley", "Miami", "Miami Beach", "Miami Gardens", "Miami Lakes", "Miami Shores", "Miami Springs", "North Bay Village", "North Miami", "North Miami Beach", "Opa-locka", "Palmetto Bay", "Pinecrest", "South Miami", "Sunny Isles Beach", "Surfside", "Sweetwater", "Virginia Gardens", "West Miami"],
        "unincorporated": ["The Redland", "Kendall", "Princeton", "Naranja", "Leisure City", "Richmond Heights"],
    },
    {
        "slug": "palm-beach", "name": "Palm Beach County",
        "intro": "Palm Beach County stretches from the coast to Lake Okeechobee. Out west, Loxahatchee, The Acreage and Wellington's equestrian estates need lot, pasture and pond work, while the Glades communities sit beside the farm land of the Everglades Agricultural Area.",
        "permit": "Palm Beach County vegetation / tree permits · ERM wetland review · local drainage districts · SFWMD",
        "cities": ["Atlantis", "Belle Glade", "Boca Raton", "Boynton Beach", "Briny Breezes", "Cloud Lake", "Delray Beach", "Glen Ridge", "Golf", "Greenacres", "Gulf Stream", "Haverhill", "Highland Beach", "Hypoluxo", "Juno Beach", "Jupiter", "Jupiter Inlet Colony", "Lake Clarke Shores", "Lake Park", "Lake Worth Beach", "Lantana", "Loxahatchee Groves", "Manalapan", "Mangonia Park", "North Palm Beach", "Ocean Ridge", "Pahokee", "Palm Beach", "Palm Beach Gardens", "Palm Beach Shores", "Palm Springs", "Riviera Beach", "Royal Palm Beach", "South Bay", "South Palm Beach", "Tequesta", "Wellington", "Westlake", "West Palm Beach"],
        "unincorporated": ["The Acreage", "Loxahatchee", "Jupiter Farms", "Canal Point"],
    },
    {
        "slug": "monroe", "name": "Monroe County (Florida Keys)",
        "intro": "Work in the Keys is careful work: thin soil over limestone, mangroves, protected habitat and limited access. Most jobs here need close coordination with county, state and federal permitting before a machine ever moves.",
        "permit": "Monroe County environmental / habitat review · FDEP · USACE · mangrove rules",
        "cities": ["Islamorada", "Key Colony Beach", "Key West", "Layton", "Marathon"],
        "unincorporated": ["Key Largo", "Tavernier", "Big Pine Key", "Cudjoe Key"],
    },
    {
        "slug": "martin", "name": "Martin County",
        "intro": "Martin County mixes coastal neighborhoods along the St. Lucie River with ranch and farm land out toward Indiantown. It is known for strict growth and environmental rules, which makes experienced, permit-aware crews especially valuable.",
        "permit": "Martin County tree / vegetation and wetland rules · SFWMD · FDEP",
        "cities": ["Indiantown", "Jupiter Island", "Ocean Breeze", "Sewall's Point", "Stuart"],
        "unincorporated": ["Palm City", "Hobe Sound", "Port Salerno", "Jensen Beach"],
    },
    {
        "slug": "lee", "name": "Lee County",
        "intro": "Lee County is one of the busiest lot-clearing markets in Florida — especially Lehigh Acres and Cape Coral, where thousands of platted lots are still waiting for homes. Canals, preserves and post-storm recovery keep the rest of the county busy.",
        "permit": "Lee County vegetation removal / development permits · city permits (Cape Coral, Fort Myers) · SFWMD",
        "cities": ["Bonita Springs", "Cape Coral", "Estero", "Fort Myers", "Fort Myers Beach", "Sanibel"],
        "unincorporated": ["Lehigh Acres", "North Fort Myers", "Alva", "Pine Island"],
    },
    {
        "slug": "collier", "name": "Collier County",
        "intro": "Collier County runs from Naples' coast to Big Cypress and the Picayune Strand, one of the largest restoration projects in Everglades history. Golden Gate Estates and Immokalee keep lot and acreage clearing steady, and Collier's rules on removing invasive plants make exotic removal part of many jobs.",
        "permit": "Collier County vegetation removal and exotic-removal requirements · SFWMD · USACE",
        "cities": ["Everglades City", "Marco Island", "Naples"],
        "unincorporated": ["Golden Gate Estates", "Immokalee", "Ave Maria", "Orangetree"],
    },
    {
        "slug": "lake-okeechobee", "name": "Lake Okeechobee Area",
        "intro": "Around the big lake — from Okeechobee and Moore Haven to Clewiston, Belle Glade and Pahokee — is farm and ranch country and the heart of Everglades water projects, including the EAA Reservoir. Ag clearing, ditch and canal work, and large restoration earthwork all happen here.",
        "permit": "Okeechobee, Glades, Hendry and Palm Beach County permits · SFWMD · USACE",
        "cities": ["Belle Glade", "Clewiston", "LaBelle", "Moore Haven", "Okeechobee", "Pahokee", "South Bay"],
        "unincorporated": ["Canal Point", "Lakeport", "Buckhead Ridge", "Port Mayaca"],
    },
]
CTY = {c["slug"]: c for c in COUNTIES}

CITIES = [
    {
        "slug": "weston", "name": "Weston", "county": "broward",
        "local": "Weston sits right on the edge of the Everglades, and its lakes and canals are a big part of what makes it work. Lake bank erosion repair, canal-side clearing and drainage fixes are the jobs we see most here.",
        "nearby": ["southwest-ranches", "davie", "pembroke-pines"],
        "focus": ["canal-pond-excavation", "drainage-stormwater", "land-clearing"],
    },
    {
        "slug": "davie", "name": "Davie", "county": "broward",
        "local": "Davie keeps its western, equestrian character — bigger lots, horse properties and open land. Lot clearing for new homes, pasture clearing and pond digging are common, and the town has its own tree rules to follow.",
        "nearby": ["southwest-ranches", "weston", "pembroke-pines"],
        "focus": ["land-clearing", "canal-pond-excavation", "site-prep-grading"],
    },
    {
        "slug": "southwest-ranches", "name": "Southwest Ranches", "county": "broward",
        "local": "Southwest Ranches is rural Broward: acre-plus lots, ranches and equestrian estates. Lot and pasture clearing, forestry mulching, ponds and driveway culverts are everyday work here.",
        "nearby": ["davie", "weston", "pembroke-pines"],
        "focus": ["land-clearing", "forestry-mulching", "drainage-stormwater"],
    },
    {
        "slug": "pembroke-pines", "name": "Pembroke Pines", "county": "broward",
        "local": "Pembroke Pines stretches west toward US-27 and the conservation areas. Commercial site work, HOA lake banks and land on the western edge keep crews busy.",
        "nearby": ["southwest-ranches", "weston", "davie"],
        "focus": ["forestry-mulching", "canal-pond-excavation", "site-prep-grading"],
    },
    {
        "slug": "homestead", "name": "Homestead", "county": "miami-dade",
        "local": "Homestead is the gateway to both Everglades and Biscayne National Parks, surrounded by the farms and nurseries of the Redland. Shallow limestone means rock plowing and careful site prep, and the Everglades edge brings wetland permitting into many jobs.",
        "nearby": [],
        "focus": ["site-prep-grading", "land-clearing", "exotic-invasive-removal"],
    },
    {
        "slug": "naples", "name": "Naples", "county": "collier",
        "local": "Naples and the surrounding Collier County communities — especially Golden Gate Estates — keep lot clearing in steady demand. Collier's rules on removing invasive plants mean exotic removal is part of many projects here.",
        "nearby": [],
        "focus": ["land-clearing", "exotic-invasive-removal", "canal-pond-excavation"],
    },
    {
        "slug": "stuart", "name": "Stuart", "county": "martin",
        "local": "Stuart is Martin County's hub, on the St. Lucie River, with Palm City, Port Salerno and Indiantown's ranch land close by. Martin County's strict environmental rules make permit-aware clearing especially important.",
        "nearby": [],
        "focus": ["land-clearing", "drainage-stormwater", "wetland-restoration-mitigation"],
    },
]
CITY = {c["slug"]: c for c in CITIES}

# ---------------------------------------------------------------- projects (sample job pages)
PROJECTS = [
    {
        "slug": "canal-excavation-weston-2024",
        "title": "Canal Excavation — Weston Property",
        "date": "2024-03-14", "date_label": "March 14, 2024",
        "city": "weston", "county": "broward",
        "service": "canal-pond-excavation",
        "summary": "Canal excavation and bank shaping on a private Weston property along the Everglades edge.",
        "youtube": "",
    },
    {
        "slug": "lot-clearing-southwest-ranches-2024",
        "title": "Lot Clearing — Southwest Ranches Site",
        "date": "2024-06-02", "date_label": "June 2, 2024",
        "city": "southwest-ranches", "county": "broward",
        "service": "land-clearing",
        "summary": "Full lot clearing and root raking to prepare a Southwest Ranches parcel for a new home.",
        "youtube": "",
    },
    {
        "slug": "retention-pond-davie-2024",
        "title": "Retention Pond Build — Davie",
        "date": "2024-11-20", "date_label": "November 20, 2024",
        "city": "davie", "county": "broward",
        "service": "canal-pond-excavation",
        "summary": "New retention pond excavated and shaped to the engineer's plan, with fill used on site.",
        "youtube": "",
    },
    {
        "slug": "forestry-mulching-pembroke-pines-2025",
        "title": "Forestry Mulching — Pembroke Pines",
        "date": "2025-02-08", "date_label": "February 8, 2025",
        "city": "pembroke-pines", "county": "broward",
        "service": "forestry-mulching",
        "summary": "Underbrush and invasive growth mulched in place across an overgrown Pembroke Pines property.",
        "youtube": "",
    },
]

# ---------------------------------------------------------------- questions
QUESTIONS = [
    {
        "slug": "land-clearing-cost-per-acre-south-florida",
        "q": "How much does land clearing cost per acre in South Florida?",
        "short": "Published Florida cost guides put land clearing at roughly $1,500 to $8,000 per acre, with dense palmetto and wetland-edge land often landing around $3,500 to $7,500. Your real number depends on how thick the growth is, tree size, access, permits and whether debris is hauled away or mulched on site.",
        "body": [
            ("What drives the price", "<ul class=\"checks\"><li><b>Density.</b> Light brush clears fast; mature hardwoods and thick Brazilian pepper take far longer.</li><li><b>Trees and stumps.</b> Big trees and stump removal add time and hauling.</li><li><b>Haul or mulch.</b> Mulching on site usually costs less than hauling everything away.</li><li><b>Ground and water.</b> Soft or wet ground needs low-ground-pressure equipment.</li><li><b>Permits and protected trees.</b> Some sites require surveys, permits or mitigation.</li><li><b>Access.</b> Tight lots, gates and neighbors all matter.</li></ul>"),
            ("Our typical ranges", "<p>Light clearing / mulching: [[$X,XXX – $X,XXX per acre]]<br>Standard lot clearing: [[$X,XXX – $X,XXX per acre]]<br>Heavy clearing with haul-off: [[$X,XXX – $X,XXX per acre]]</p><p class=\"small\">Every site is different — we give firm prices after a site visit.</p>"),
        ],
        "related_service": "land-clearing",
    },
    {
        "slug": "do-i-need-a-permit-to-clear-land",
        "q": "Do I need a permit to clear land in South Florida?",
        "short": "Usually, yes. Most South Florida counties and cities require a permit to remove trees, and any work in or near wetlands can also need state (water management district / FDEP) and federal (Army Corps) approval. In Miami-Dade, for example, wetland work requires a Class IV permit and mangrove work a Class I permit.",
        "body": [
            ("County by county", "<ul class=\"checks\"><li><b>Miami-Dade:</b> tree removal / relocation permit for non-exempt trees; Class IV permit for any work in freshwater wetlands; Class I for mangroves; special rules for Natural Forest Communities.</li><li><b>Broward:</b> tree removal license through the Tree Preservation Program (nuisance trees excepted); wetland and surface-water work through the Aquatic & Wetland Resources program.</li><li><b>Palm Beach, Martin, Lee, Collier, Monroe:</b> each has its own tree, vegetation and wetland rules, and many cities add their own.</li></ul>"),
            ("How we help", "<p>We've been working inside these rules since 1992. Before we start, we'll tell you what your property likely needs and who issues it, and coordinate with your engineer or permit expeditor when needed.</p><p class=\"small\">Rules change — always confirm with the permitting agency before work begins.</p>"),
        ],
        "related_service": "land-clearing",
    },
    {
        "slug": "can-you-clear-land-with-wetlands",
        "q": "Can you clear land that has wetlands on it?",
        "short": "Sometimes — but only with the right permits. Clearing, filling or digging in wetlands usually needs county, water-management-district and often Army Corps approval. Often the answer is to clear the upland part of the property now and permit the wetland portion separately — or to restore the wetland instead.",
        "body": [
            ("How to tell if you have wetlands", "<p>Standing water part of the year, wetland plants, or mucky soils are all signs. A wetland delineation by an environmental consultant gives the official answer.</p>"),
            ("What we do", "<p>We clear the uplands, work under wetland permits when they're issued, and do restoration and mitigation earthwork when that's the better path. [[Army Corps project history XXX]]</p>"),
        ],
        "related_service": "wetland-restoration-mitigation",
    },
    {
        "slug": "how-long-does-it-take-to-clear-an-acre",
        "q": "How long does it take to clear an acre of land?",
        "short": "With the right equipment, light brush on an acre can often be mulched in a day or less, while heavy woods with stump removal and haul-off can take several days. Permits, wet ground and access usually affect the schedule more than the clearing itself.",
        "body": [
            ("Typical timelines", "<p>Light brush / mulching: [[X hours – 1 day per acre]]<br>Standard lot clearing: [[X – X days per acre]]<br>Heavy clearing with stumps and haul-off: [[X – X days per acre]]</p>"),
            ("What slows a job down", "<ul class=\"checks\"><li>Waiting on permits</li><li>Rain and high water</li><li>Large hardwoods and stumps</li><li>Hauling distance to disposal</li></ul>"),
        ],
        "related_service": "land-clearing",
    },
    {
        "slug": "forestry-mulching-vs-land-clearing",
        "q": "Forestry mulching or traditional land clearing — which do I need?",
        "short": "Choose forestry mulching for brush, palmetto and small trees when you want a fast, clean job that protects the soil. Choose traditional clearing when you need big trees and stumps out, or a bare site ready for a pad, pond or road.",
        "body": [
            ("Side by side", "<table class=\"facts\"><tr><th></th><td><b>Forestry mulching</b></td><td><b>Traditional clearing</b></td></tr><tr><th>Best for</th><td>Brush, palmetto, small trees, fire breaks</td><td>Building pads, big trees, stumps</td></tr><tr><th>Debris</th><td>Stays as mulch</td><td>Hauled or piled</td></tr><tr><th>Soil</th><td>Protected</td><td>Exposed, ready to grade</td></tr><tr><th>Speed</th><td>Very fast</td><td>Depends on haul-off</td></tr></table>"),
        ],
        "related_service": "forestry-mulching",
    },
]
