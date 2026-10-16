"""Company facts, credentials, projects and references: the trust layer of the site.

Fill these in as the operating company comes on board. Anything left empty shows as a
"Pending" marker while SHOW_SLOTS is True (preview), and is hidden when SHOW_SLOTS is False
(launch). Only put real, verifiable facts here: client names and quotes need written permission,
and government past performance must match what can be documented.
"""

SHOW_SLOTS = True  # preview: show empty slots and sample projects; set False before launch

COMPANY = {
    "name": "Beyond Klean",
    "legal_name": "",            # e.g. "Beyond Klean LLC" or the operating company's legal name
    "operator": "",              # company performing the work under the Beyond Klean brand
    "phone": "",                 # e.g. "(813) 555-0100"
    "email": "",                 # e.g. "bids@beyondklean.com"
    "address": "",               # street, city, state ZIP
    "hours": "Office Monday to Friday, 7 a.m. to 6 p.m. Crews schedule nights, weekends and shutdowns.",
    "founded": "",               # year
    "service_area": "Nationwide. Home crews in the Southeast; travel crews for larger projects anywhere in the U.S.",
    # Government identifiers
    "uei": "",                   # SAM.gov Unique Entity ID
    "cage": "",                  # CAGE code
    "sam_status": "",            # e.g. "Active, expires 2027-08-01"
    "naics": [
        ("561720", "Janitorial Services"),
        ("561790", "Other Services to Buildings and Dwellings"),
        ("562119", "Other Waste Collection"),
        ("238990", "All Other Specialty Trade Contractors"),
    ],
    "psc": [
        ("S201", "Housekeeping: Custodial Janitorial"),
        ("S205", "Housekeeping: Trash/Garbage Collection"),
        ("S214", "Housekeeping: Carpet Laying/Cleaning"),
    ],
    "set_asides": [],            # e.g. ["Small Business", "SDVOSB"] — only certifications actually held
    # Insurance, bonding and licenses: (label, value)
    "insurance": [],             # e.g. [("General liability", "$1M per occurrence / $2M aggregate"), ("Workers' compensation", "Statutory")]
    "bonding": "",               # e.g. "Single project $500K / aggregate $1M"
    "licenses": [],              # e.g. [("Florida mold remediator", "MRSR1234")]
    "safety": [],                # e.g. [("EMR", "0.82"), ("OSHA 30", "Supervisors"), ("OSHA 10", "All field staff")]
    "leadership": [],            # e.g. [("Name", "Title", "One or two lines of background")]
}

# Real clients only, with permission to show the name.
CLIENTS = []                     # e.g. ["Turner Construction", "Publix"]

# Real quotes only: (quote, name, title, company), with written permission.
TESTIMONIALS = []

# Completed projects. Photos go in site/assets/projects/ (e.g. "deck-before.jpg").
# client: shown only when client_ok is True; otherwise `client_desc` is used.
# tasks: exact service names, so the project appears on those service pages.
PROJECTS = [
    # {
    #     "slug": "distribution-center-ceiling-jacksonville",
    #     "title": "Distribution center open-ceiling cleaning",
    #     "client": "", "client_ok": False, "client_desc": "National logistics company",
    #     "type": "Industrial or warehouse", "city": "Jacksonville", "state": "FL",
    #     "sqft": 240000, "date": "2025-03", "duration": "9 nights",
    #     "summary": "Deck, joists, ducts and lights cleaned from scissor and boom lifts over live racking.",
    #     "tasks": ["Open ceiling deck cleaning", "Duct exterior cleaning"],
    #     "photos": {"before": "dc-before.jpg", "during": "dc-during.jpg", "after": "dc-after.jpg"},
    # },
]

# Preview-only sample slots, so the layout can be reviewed before real projects exist.
SAMPLE_PROJECTS = [
    {"slug": "sample-warehouse-ceiling", "title": "Warehouse open-ceiling cleaning", "client_desc": "Sample slot: distribution center",
     "type": "Industrial or warehouse", "city": "City", "state": "", "sqft": 0, "date": "", "duration": "",
     "summary": "Sample slot. Replace with a real project: deck, joists, ducts and fixtures cleaned from lifts over live operations.",
     "tasks": ["Open ceiling deck cleaning", "Duct exterior cleaning", "High-bay light fixture cleaning"]},
    {"slug": "sample-retail-final", "title": "Retail store opening clean", "client_desc": "Sample slot: national retailer",
     "type": "Retail or store opening", "city": "City", "state": "", "sqft": 0, "date": "", "duration": "",
     "summary": "Sample slot. Replace with a real project: rough, final and pre-opening touch-up clean on a new store.",
     "tasks": ["Store opening clean", "Final clean of entire building", "Interior window cleaning"]},
    {"slug": "sample-multifamily", "title": "Multifamily lease-up turnover", "client_desc": "Sample slot: apartment developer",
     "type": "Multifamily", "city": "City", "state": "", "sqft": 0, "date": "", "duration": "",
     "summary": "Sample slot. Replace with a real project: unit-by-unit final cleans released on the lease-up schedule.",
     "tasks": ["Rough clean of entire building", "Final clean of entire building"]},
    {"slug": "sample-government", "title": "Government facility renovation", "client_desc": "Sample slot: federal agency via prime contractor",
     "type": "Government", "city": "City", "state": "", "sqft": 0, "date": "", "duration": "",
     "summary": "Sample slot. Replace with a real project: phased cleaning in an occupied facility under security and access rules.",
     "tasks": ["Fine drywall dust removal from all horizontal surfaces", "Final clean of entire building"]},
    {"slug": "sample-restaurant", "title": "Restaurant kitchen turnover", "client_desc": "Sample slot: restaurant group",
     "type": "Restaurant or food service", "city": "City", "state": "", "sqft": 0, "date": "", "duration": "",
     "summary": "Sample slot. Replace with a real project: kitchen, FRP and equipment cleaned ahead of the health inspection.",
     "tasks": ["Commercial kitchen post-construction clean"]},
    {"slug": "sample-healthcare", "title": "Clinic build-out final clean", "client_desc": "Sample slot: healthcare system",
     "type": "Healthcare", "city": "City", "state": "", "sqft": 0, "date": "", "duration": "",
     "summary": "Sample slot. Replace with a real project: final clean to infection-control protocol before patient occupancy.",
     "tasks": ["Final clean of entire building"]},
]

# Home markets (true today): highlighted on the map separately from project states.
HOME_STATES = ["FL", "GA", "AL"]
