def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Point-of-sale counter detailing": T(
 "Point-of-sale counter detailing cleans checkout counters and cash wraps: counter surfaces, display cases, shelves, bag wells, cable openings and the outside of registers, card readers and screens.",
 "The cash wrap is where every shopper finishes their visit. It combines millwork, glass, stone or laminate and electronics, each with different cleaning needs.",
 "Crews clean surfaces by material, vacuum cable grommets and bag wells, wipe electronics with dry or barely damp cloths and never spray liquid onto devices.",
 ["Counter materials", "Electronics installed", "Glass display cases", "Bag wells and storage"],
 ["Liquid sprayed on card readers and screens can damage them.", "Stone counters need stone-safe cleaners."],
 [("What is a cash wrap?", "The checkout counter in a store, where purchases are rung up and wrapped."),
  ("How are point-of-sale devices cleaned?", "With a dry or barely damp microfiber cloth, never spraying cleaner directly on the device."),
  ("Is the cash wrap cleaned before opening?", "Yes, it is detailed after registers and devices are installed and before opening day."),
  ("Why clean cable openings and bag wells?", "They collect dust, cable scraps and packaging debris from installation.")]),
"Merchandise set support cleaning": dict(
 a="Merchandise set support cleaning keeps a new store clean while the retailer's team unpacks and stocks merchandise, continuously removing cardboard, plastic and debris and cleaning areas as they are finished.",
 m="Crews work alongside the merchandising team, breaking down and removing cardboard, pulling plastic and hangers, and cleaning floors and fixtures as each department is completed.",
 w=["Merchandise and fixtures must never be removed or moved without the retailer's direction.", "Cardboard volume during stocking is large; plan recycling containers ahead."],
 q=[("What is a merchandise set in a new store?", "The period when the retailer's team unpacks and places all merchandise on the shelves and fixtures before opening."),
  ("Why is cleaning needed during merchandise set?", "Stocking produces huge volumes of cardboard, plastic and hangers, and the store fills with debris right before opening if it is not cleared continuously."),
  ("Is cardboard from merchandise set recycled?", "Usually. Cardboard is broken down and baled or placed in recycling containers."),
  ("Who stocks the store during merchandise set?", "The retailer's own team or a merchandising contractor, with the cleaning crew supporting them.")]),
"Stockroom and backroom cleaning": dict(
 a="Stockroom and backroom cleaning cleans storage rooms, receiving areas, break rooms, offices and restrooms behind the sales floor, which are often used for construction storage and left dirty at opening.",
 m="Crews clear construction debris and leftover materials with the GC's approval, clean shelving top down, scrub floors, and detail break rooms and staff restrooms.",
 q=[("Are stockrooms cleaned before a store opens?", "Yes, they are cleaned so merchandise and supplies can be stored on clean shelving and floors."),
  ("Why are back rooms so dirty at the end of a store build?", "Trades use them to store tools and materials and they are often the last areas finished."),
  ("Are staff break rooms included in the opening clean?", "Yes, break rooms, offices and staff restrooms are part of the back-of-house clean."),
  ("Is stockroom shelving cleaned?", "Yes, shelving is cleaned top down before merchandise and supplies are stored.")]),
"Retail remodel overnight cleaning": dict(
 a="Retail remodel overnight cleaning cleans an operating store after each night of remodel work, so construction areas are safe and the sales floor is clean when the store opens the next morning.",
 y="Most remodels happen while the store stays open. Every morning the store must be safe, presentable and free of dust on merchandise, or sales and customer trust suffer.",
 w=["Crews must finish and clear the floor before the store opens.", "Merchandise near work areas must be covered and uncovered every night."],
 q=[("How does overnight remodel cleaning work?", "After construction crews finish each night, cleaners clean work zones, uncover merchandise, scrub floors and remove debris before the store opens."),
  ("Do stores stay open during remodels?", "Most retail remodels happen while the store stays open, with work done at night or in sections."),
  ("How is merchandise protected during overnight remodel work?", "It is covered with plastic before work starts and uncovered and cleaned around after the night's work."),
  ("Who coordinates overnight remodel cleaning?", "The GC and the store manager, so cleaning matches each night's construction scope.")]),
"Phased store remodel cleaning": dict(
 a="Phased store remodel cleaning cleans each section of a remodeled store as it is completed and turned back to the retailer, so finished departments can reopen to shoppers while work moves to the next area.",
 m="Crews final-clean each finished phase, install barriers or protection at the boundary with active work, and touch up as needed until the next phase is complete.",
 w=["Adjacent active work can re-soil a cleaned phase.", "Phase dates often shift, so cleaning needs flexible scheduling."],
 q=[("What is a phased store remodel?", "A remodel done one section or department at a time so the store can keep operating."),
  ("How is each phase of a remodel cleaned?", "It gets a complete final clean when finished, then is protected from the next phase's dust."),
  ("Does phased remodel cleaning cost more?", "It can, because crews mobilize several times, but it keeps the store trading throughout."),
  ("Who decides the phases of a store remodel?", "The retailer and GC, based on sales, schedule and logistics.")]),
}
