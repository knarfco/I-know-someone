"""Estimator data that is not in the price book: crew roles, materials share by family,
equipment presets and starter templates. Every value is a starting point the contractor edits."""

ROLES = [  # key, label, default wage $/hr
    ("general", "General cleaner", 16.0),
    ("tech", "Floor / window tech", 20.0),
    ("lift", "Lift / high-access tech", 22.0),
    ("specialist", "Specialty / licensed tech", 26.0),
    ("lead", "Lead / supervisor", 24.0),
]

# Default crew role by service family (regulated tier always uses the specialty role)
FAMILY_ROLE = {
    "Hard Floors": "tech", "Carpet & Soft Surfaces": "tech", "Glass, Windows & Glazing": "tech",
    "Exterior, Hardscape & Building Envelope": "tech",
    "Overhead & Elevated Surfaces (Above Eye Level)": "lift",
    "Restoration & Regulated Work (Conditional)": "specialist", "Specialty & Controlled Environments": "specialist",
}

# Chemicals and consumables as a share of the typical market price, by family
MATERIAL_SHARE = {
    "Site, Debris & Waste Management": .04, "Rough Clean": .04, "Fine Dust, Drywall Dust & Controlled-Dust Cleaning": .05,
    "Overhead & Elevated Surfaces (Above Eye Level)": .04, "Walls, Ceilings & Interior Finishes": .05,
    "Doors, Hardware, Millwork & Casework": .05, "Glass, Windows & Glazing": .05, "Hard Floors": .15,
    "Carpet & Soft Surfaces": .08, "Restrooms & Plumbing Fixtures": .06, "Kitchens, Food Facilities & FRP": .07,
    "Mechanical, Electrical & Construction IAQ": .10, "Retail Fixtures & Store Opening": .05,
    "Specialty & Controlled Environments": .08, "Exterior, Hardscape & Building Envelope": .07,
    "Residue, Stain & Protective-Material Removal": .10, "Vertical Transportation & Circulation": .05,
    "Turnover, Punch & Closeout Support": .05, "Multifamily & Residential-Scale Turnover": .06,
    "Restoration & Regulated Work (Conditional)": .12,
}

EQUIPMENT = [  # name, $ per day (project) — recurring estimates treat the rate as $ per month
    ("Scissor lift (19–26 ft)", 120), ("Scissor lift (32–40 ft)", 190), ("Boom lift (45–60 ft)", 350),
    ("Auto-scrubber", 150), ("Floor burnisher", 60), ("Carpet extractor", 55), ("Pressure washer / surface cleaner", 90),
    ("HEPA vacuum", 25), ("Air scrubber (negative air)", 60), ("Water-fed pole system", 45),
    ("Lift delivery / pickup (per trip)", 150), ("Dumpster swap", 450),
]

# Templates: (name, mode, [(task, qty factor, basis, area)]) — basis "sqft" multiplies the building
# square feet by the factor; basis "fixed" uses the factor as the quantity.
TEMPLATES = [
    ("Retail store opening", "project", [
        ("Rough clean of entire building", 1, "sqft", "Rough"),
        ("Final clean of entire building", 1, "sqft", "Final"),
        ("Interior window cleaning", 1 / 250, "sqft", "Final"),
        ("VCT initial floor finish", .5, "sqft", "Final"),
        ("Restroom accessory cleaning", 4, "fixed", "Final"),
        ("Touch-up clean before owner walk", 1, "sqft", "Punch"),
        ("Store opening clean", 1, "sqft", "Punch"),
    ]),
    ("Office tenant improvement", "project", [
        ("Rough clean of entire building", 1, "sqft", "Rough"),
        ("Fine drywall dust removal from all horizontal surfaces", 1, "sqft", "Light clean"),
        ("Light clean (phase 2)", 1, "sqft", "Light clean"),
        ("Final clean of entire building", 1, "sqft", "Final"),
        ("Interior window cleaning", 1 / 300, "sqft", "Final"),
        ("Carpet extraction", .6, "sqft", "Final"),
        ("Touch-up clean before owner walk", 1, "sqft", "Punch"),
    ]),
    ("Warehouse ceiling and floor", "project", [
        ("Open ceiling deck cleaning", 1, "sqft", "Overhead"),
        ("High-bay light fixture cleaning", 1 / 1000, "sqft", "Overhead"),
        ("Warehouse floor scrubbing", 1, "sqft", "Floor"),
        ("Warehouse post-construction cleaning", 1, "sqft", "Final"),
    ]),
    ("Apartment building turnover", "project", [
        ("Apartment unit post-construction clean", 1 / 900, "sqft", "Units"),
        ("Rough clean by floor or phase", 1, "sqft", "Rough"),
        ("Final clean by phase or floor", 1, "sqft", "Final"),
        ("Touch-up clean before owner walk", 1, "sqft", "Punch"),
    ]),
    ("Office nightly janitorial", "recurring", [
        ("Empty trash and replace liner", 1 / 200, "sqft", "Nightly"),
        ("Empty recycling bins", 1 / 400, "sqft", "Nightly"),
        ("Clean and disinfect toilet", 1 / 2500, "sqft", "Restrooms"),
        ("Clean and disinfect urinal", 1 / 7500, "sqft", "Restrooms"),
        ("Clean restroom sink and counter", 1 / 2500, "sqft", "Restrooms"),
        ("Clean restroom mirror", 1 / 2500, "sqft", "Restrooms"),
        ("Restock paper and soap", 1 / 1000, "sqft", "Restrooms"),
        ("Mop and disinfect restroom floor", .03, "sqft", "Restrooms"),
        ("Vacuum carpet, open areas", .5, "sqft", "Nightly"),
        ("Damp mop hard floor", .2, "sqft", "Nightly"),
        ("Wipe and disinfect touch points", 1 / 200, "sqft", "Nightly"),
        ("Clean breakroom", 1, "fixed", "Nightly"),
        ("Clean entrance glass", 2, "fixed", "Nightly"),
        ("Dust horizontal surfaces", .5, "sqft", "Weekly"),
        ("Vacuum carpet, offices and edges", .5, "sqft", "Weekly"),
        ("Supervisor inspection", 2, "fixed", "Weekly"),
        ("Hot water extraction of carpet", .5, "sqft", "Periodic"),
        ("Strip and refinish resilient floor", .2, "sqft", "Periodic"),
    ]),
    ("Medical clinic nightly", "recurring", [
        ("Clean healthcare exam room", 1 / 400, "sqft", "Clinical"),
        ("Empty trash and replace liner", 1 / 150, "sqft", "Nightly"),
        ("Clean and disinfect toilet", 1 / 1500, "sqft", "Restrooms"),
        ("Clean restroom sink and counter", 1 / 1200, "sqft", "Restrooms"),
        ("Mop and disinfect restroom floor", .04, "sqft", "Restrooms"),
        ("Damp mop hard floor", .6, "sqft", "Nightly"),
        ("Wipe and disinfect touch points", 1 / 60, "sqft", "Nightly"),
        ("Clean lobby and reception", 1, "fixed", "Nightly"),
        ("Terminal clean patient or procedure room", 1 / 2000, "sqft", "Clinical"),
        ("Scrub and recoat resilient floor", .6, "sqft", "Periodic"),
    ]),
]
