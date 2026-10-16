"""Routine and periodic cleaning tasks for recurring-contract estimates.

(task, category, unit, units per worker-hour, materials $ per unit, default frequency, what it includes)

Production rates are starting points drawn from commonly published janitorial ranges and field
experience, not from any licensed table. Every value is editable in the estimator, and contractors
should replace them with their own timed rates.
Frequencies: nightly5 (5x/week), nightly7, 3x, 2x, weekly, biweekly, monthly, quarterly, semiannual, annual.
"""

ROUTINE = [
    # Trash and recycling
    ("Empty trash and replace liner", "Trash and recycling", "each", 150, 0.06, "nightly5", "Empty desk-side and common trash, replace liner when soiled, wipe rim."),
    ("Empty recycling bins", "Trash and recycling", "each", 150, 0.02, "nightly5", "Empty recycling to the building stream, keep liners where used."),
    ("Empty large common-area trash receptacle", "Trash and recycling", "each", 40, 0.25, "nightly5", "Empty 32 to 55 gallon receptacles, replace liner, wipe lid and push plate."),
    ("Transport trash to dumpster", "Trash and recycling", "each", 6, 0, "nightly5", "Haul consolidated bags to the dumpster or compactor (per trip)."),
    ("Clean and sanitize trash receptacles", "Trash and recycling", "each", 15, 0.15, "monthly", "Wash and disinfect inside and outside of receptacles."),
    ("Dumpster enclosure sweep and wash-down", "Trash and recycling", "each", 1, 4.00, "monthly", "Sweep and rinse the dumpster pad and enclosure (per enclosure)."),
    # Restrooms
    ("Clean and disinfect toilet", "Restrooms", "fixture", 20, 0.12, "nightly5", "Bowl, seat, hinges, base and flush handle, disinfected with contact time."),
    ("Clean and disinfect urinal", "Restrooms", "fixture", 24, 0.10, "nightly5", "Bowl, flush valve, partition contact points and floor beneath."),
    ("Clean restroom sink and counter", "Restrooms", "fixture", 25, 0.06, "nightly5", "Basin, faucet, counter and backsplash, polished dry."),
    ("Clean restroom mirror", "Restrooms", "each", 60, 0.02, "nightly5", "Streak-free glass cleaning of mirrors."),
    ("Spot clean toilet partitions", "Restrooms", "each", 30, 0.03, "nightly5", "Door, latch and hand-contact areas of each stall."),
    ("Restock paper and soap", "Restrooms", "each", 60, 0, "nightly5", "Refill toilet tissue, towels and soap per dispenser (product billed separately)."),
    ("Mop and disinfect restroom floor", "Restrooms", "sqft", 900, 0.004, "nightly5", "Damp-mop with disinfectant, corners and behind fixtures."),
    ("Detail clean restroom walls and partitions", "Restrooms", "sqft", 350, 0.006, "monthly", "Wash walls, partitions and doors top to bottom."),
    ("Scrub restroom floor and grout", "Restrooms", "sqft", 250, 0.012, "monthly", "Machine or hand scrub tile and grout, rinse and extract."),
    ("Descale fixtures", "Restrooms", "fixture", 10, 0.20, "monthly", "Remove mineral scale from bowls, urinals and faucets."),
    ("Refill feminine hygiene and seat covers", "Restrooms", "each", 60, 0, "weekly", "Restock dispensers and empty sanitary receptacles."),
    # Floors, daily
    ("Vacuum carpet, open areas", "Floors", "sqft", 7000, 0.0005, "nightly5", "Backpack or upright vacuum of traffic lanes and open areas."),
    ("Vacuum carpet, offices and edges", "Floors", "sqft", 2800, 0.0005, "weekly", "Full vacuum including edges, under desks and corners."),
    ("Spot clean carpet", "Floors", "each", 12, 0.25, "weekly", "Treat spots and spills with spotter, blot and rinse."),
    ("Dust mop hard floor", "Floors", "sqft", 6000, 0.0003, "nightly5", "Treated dust mop of VCT, LVT, tile and sealed concrete."),
    ("Damp mop hard floor", "Floors", "sqft", 3000, 0.002, "nightly5", "Neutral cleaner, two-bucket or flat mop system."),
    ("Auto-scrub hard floor", "Floors", "sqft", 12000, 0.0015, "weekly", "Walk-behind or ride-on auto-scrubber pass."),
    ("Burnish floor finish", "Floors", "sqft", 8000, 0.0008, "weekly", "High-speed burnish to restore gloss on finished resilient floors."),
    ("Clean entrance mats", "Floors", "each", 20, 0.02, "nightly5", "Vacuum and spot clean walk-off mats, clean underneath weekly."),
    ("Sweep stairwells", "Floors", "flight", 6, 0.01, "weekly", "Sweep or vacuum treads and landings, damp wipe rails."),
    # Floors, periodic
    ("Strip and refinish resilient floor", "Floor care (periodic)", "sqft", 250, 0.05, "annual", "Strip old finish, rinse, apply 4 to 5 coats of finish."),
    ("Scrub and recoat resilient floor", "Floor care (periodic)", "sqft", 600, 0.025, "quarterly", "Deep scrub top coats, apply 2 coats of finish."),
    ("Hot water extraction of carpet", "Floor care (periodic)", "sqft", 500, 0.015, "semiannual", "Pre-spray, extract and groom, with drying fans."),
    ("Interim carpet encapsulation", "Floor care (periodic)", "sqft", 1200, 0.008, "quarterly", "Low-moisture encapsulation and vacuum."),
    ("Polished concrete maintenance", "Floor care (periodic)", "sqft", 3000, 0.006, "monthly", "Auto-scrub with conditioner and high-speed burnish."),
    ("Tile and grout deep clean", "Floor care (periodic)", "sqft", 200, 0.02, "quarterly", "Scrub, rinse and extract grout lines."),
    # Offices and common areas
    ("Dust horizontal surfaces", "Offices and common areas", "sqft", 6000, 0.0005, "weekly", "Microfiber dust desks (clear areas), ledges, sills and partitions."),
    ("Wipe and disinfect touch points", "Offices and common areas", "each", 300, 0.01, "nightly5", "Door handles, switches, elevator buttons, rails and push plates."),
    ("Clean desks and work surfaces", "Offices and common areas", "each", 40, 0.02, "weekly", "Wipe cleared desk surfaces, phones and keyboards where allowed."),
    ("Clean conference room", "Offices and common areas", "room", 6, 0.10, "nightly5", "Tables, chairs, whiteboard, trash and floor."),
    ("Spot clean walls, doors and switch plates", "Offices and common areas", "sqft", 2000, 0.0005, "weekly", "Remove smudges and marks from walls and doors."),
    ("Clean interior door glass and sidelights", "Offices and common areas", "each", 50, 0.02, "nightly5", "Fingerprints and smudges on door glass and sidelights."),
    ("Clean lobby and reception", "Offices and common areas", "room", 3, 0.20, "nightly5", "Furniture, glass, floors, trash and touch points."),
    ("Clean elevator cab", "Offices and common areas", "each", 4, 0.10, "nightly5", "Walls, doors, tracks, buttons and floor."),
    ("Vacuum upholstered furniture", "Offices and common areas", "each", 20, 0, "monthly", "Vacuum seats, backs and crevices."),
    ("High dust vents, ledges and fixtures", "Offices and common areas", "sqft", 2500, 0.001, "quarterly", "Above-reach dusting with extension tools or HEPA vacuum."),
    # Breakrooms and kitchens
    ("Clean breakroom", "Breakrooms", "room", 3, 0.25, "nightly5", "Counters, sink, tables, appliance exteriors, trash and floor."),
    ("Clean microwave interior", "Breakrooms", "each", 15, 0.03, "weekly", "Wipe interior, turntable and door seal."),
    ("Clean refrigerator interior", "Breakrooms", "each", 2, 0.25, "monthly", "Empty per client policy, wipe shelves and seals."),
    ("Load or run dishwasher", "Breakrooms", "each", 12, 0.15, "nightly5", "Load, run and unload break-room dishwasher."),
    # Glass
    ("Clean entrance glass", "Glass", "each", 30, 0.02, "nightly5", "Both sides of entrance doors and adjacent glass to 7 ft."),
    ("Interior window cleaning, routine", "Glass", "pane", 20, 0.03, "quarterly", "Interior panes with squeegee and detail cloth."),
    ("Exterior window cleaning, ground level", "Glass", "pane", 15, 0.04, "quarterly", "Exterior panes reachable from the ground or pole system."),
    # Exterior and site
    ("Police exterior grounds for litter", "Exterior", "sqft", 20000, 0.0001, "nightly5", "Pick up litter at entries, walks and landscaped edges."),
    ("Sweep entrances and walkways", "Exterior", "sqft", 5000, 0.0001, "nightly5", "Sweep entries, walks and smoking areas."),
    ("Pressure wash sidewalks", "Exterior", "sqft", 1000, 0.01, "quarterly", "Surface-cleaner wash with water recovery where required."),
    ("Clean exterior ash urns and benches", "Exterior", "each", 20, 0.05, "weekly", "Empty urns, wipe benches and receptacles."),
    ("Parking lot sweeping", "Exterior", "sqft", 40000, 0.0002, "weekly", "Ride-on or walk-behind sweeper pass."),
    # Industrial and specialty
    ("Warehouse floor auto-scrub", "Industrial", "sqft", 20000, 0.001, "weekly", "Ride-on scrubber through aisles and docks."),
    ("Dock and loading area sweep", "Industrial", "sqft", 8000, 0.0002, "nightly5", "Sweep docks, levelers and staging lanes."),
    ("High dusting of warehouse structure", "Industrial", "sqft", 1500, 0.002, "semiannual", "Deck, joists, pipes and lights from lifts with HEPA capture."),
    ("Clean and disinfect locker room", "Industrial", "room", 1.5, 0.80, "nightly5", "Showers, benches, lockers exteriors, fixtures and floors."),
    ("Production area wipe-down", "Industrial", "sqft", 2000, 0.002, "nightly5", "Wipe non-production surfaces per plant sanitation rules."),
    ("Clean healthcare exam room", "Healthcare", "room", 6, 0.35, "nightly5", "Disinfect surfaces and touch points, trash, floor, per facility protocol."),
    ("Terminal clean patient or procedure room", "Healthcare", "room", 1.5, 1.50, "weekly", "Top-to-bottom disinfection with documented contact times."),
    ("Clean classroom", "Education", "room", 4, 0.20, "nightly5", "Desks, boards, trash, touch points and floors."),
    ("Clean gym floor (dust mop and spot)", "Education", "sqft", 8000, 0.0003, "nightly5", "Dust mop and spot clean wood or sport floor."),
    # Multifamily and residential
    ("Common hallway vacuum and spot clean", "Multifamily", "lf", 600, 0.0005, "3x", "Vacuum corridors, spot clean walls and doors."),
    ("Amenity space clean (clubhouse, gym)", "Multifamily", "room", 1.5, 0.50, "nightly7", "Equipment wipe-down, restrooms, trash and floors."),
    ("Mail room and package area clean", "Multifamily", "room", 4, 0.10, "nightly5", "Counters, lockers exterior, trash and floor."),
    ("Pool deck sweep and furniture wipe", "Multifamily", "sqft", 4000, 0.0005, "3x", "Sweep deck, wipe loungers and tables."),
    ("Unit turnover clean (standard)", "Multifamily", "unit", 0.2, 12.00, "monthly", "Move-out clean of an occupied-ready unit (about 5 worker-hours)."),
    # Supplies and supervision
    ("Supervisor inspection", "Supervision", "hour", 1, 0, "weekly", "Quality inspection walk with checklist (per hour)."),
    ("Day porter service", "Supervision", "hour", 1, 0.50, "nightly5", "On-site porter for restrooms, spills and lobby upkeep (per hour)."),
]

FREQ = {
    "nightly7": ("7 nights a week", 30.42), "nightly5": ("5 nights a week", 21.67), "3x": ("3 times a week", 13.0),
    "2x": ("2 times a week", 8.67), "weekly": ("Weekly", 4.33), "biweekly": ("Every 2 weeks", 2.17),
    "monthly": ("Monthly", 1.0), "quarterly": ("Quarterly", 0.333), "semiannual": ("Twice a year", 0.167),
    "annual": ("Once a year", 0.083), "once": ("One time", 0.0),
}
