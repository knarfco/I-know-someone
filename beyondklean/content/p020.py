def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Elevator door and sill track cleaning": dict(
 a="Elevator door and sill track cleaning vacuums the grooved door sills at every landing and in each cab and cleans the faces of hoistway and cab doors, removing grit, screws and debris that keep doors from closing properly.",
 q=[("Why are elevator sills cleaned during construction?", "Debris in the sill grooves stops elevator doors from closing smoothly, causing service calls, failed inspections and trapped-passenger complaints."),
  ("How often should elevator sills be cleaned on a jobsite?", "Regularly during construction, because every delivery fills them with grit, and thoroughly before the elevator inspection and turnover."),
  ("Can elevator sills be washed with water?", "They should be vacuumed, not washed. Water pushes debris deeper into the track and can cause corrosion."),
  ("Who adjusts elevator doors that do not close properly?", "The elevator contractor. Cleaning crews only remove debris and report problems.")]),
"Elevator pit debris removal": dict(
 a="Elevator pit debris removal clears construction debris, trash and dust from the bottom of elevator hoistways, done only under the elevator contractor's lockout, supervision and fall protection procedures.",
 q=[("Who is allowed to enter an elevator pit?", "Only authorized people working under the elevator contractor's lockout and supervision. Pits have fall, crushing and electrical hazards."),
  ("Why must elevator pits be clean for inspection?", "Debris in a pit is a fire hazard and can interfere with buffers and equipment, so elevator inspectors require pits to be clean."),
  ("What is typically found in elevator pits on construction projects?", "Construction debris, trash, dropped tools and materials, and dust that falls down the hoistway from every floor."),
  ("What if there is water in the elevator pit?", "Water must be addressed by the GC before inspection. It can indicate a waterproofing problem and damages equipment.")]),
"Escalator and moving walk cleaning": dict(
 a="Escalator and moving walk cleaning cleans the balustrades, handrails, skirt panels, decking and exterior panels of escalators and moving walks, only with the escalator contractor's lockout and approval.",
 q=[("Who cleans escalators in a new building?", "Exterior surfaces can be cleaned by trained crews with the escalator contractor's lockout and approval. Steps, comb plates and mechanisms are serviced by the escalator contractor."),
  ("Why is escalator cleaning treated as conditional work?", "Escalators are moving machinery with pinch, entanglement and fall hazards, so access and lockout are controlled by the escalator contractor."),
  ("Are escalator handrails cleaned at turnover?", "Yes, with cleaners approved by the escalator manufacturer, because some products damage handrail rubber."),
  ("Can construction debris damage escalators?", "Yes. Grit and screws in steps and comb plates can damage the machine and create trip hazards.")]),
"Stairwell cleaning top to bottom": dict(
 a="Stairwell cleaning top to bottom details stair towers from the roof landing down to the ground floor, including handrails, treads, risers, nosings, landings, walls, doors and signage, so dust always falls onto areas not yet cleaned.",
 q=[("Why are stairwells cleaned from the top down?", "Dust and debris fall down the stairs. Starting at the top means every flight below is cleaned only once."),
  ("Do fire inspectors check stairwells?", "Yes. Stairwells are exit routes, so inspectors check that they are clear, lit, signed and free of stored materials."),
  ("What is included in stairwell final cleaning?", "Handrails, treads, risers, nosings, landings, walls, doors and signage on every level."),
  ("How long does it take to clean a stair tower after construction?", "It depends on height and dirt, but a tall stair tower can take a full crew shift.")]),
"Corridor and hallway detailing": T(
 "Corridor and hallway detailing cleans corridors from ceiling to floor: light fixtures, walls, wall protection, doors and frames, signage, fire devices and floors, usually as one of the last areas cleaned because trades use corridors to reach rooms.",
 "Corridors are walked by every trade during construction and by every occupant afterward. They collect scuffs, dust and debris faster than any other space.",
 "Crews clean top down in sections, finishing walls, doors and signage before floors, and schedule corridors last so they are not re-soiled by trades finishing rooms.",
 ["Corridor length and finishes", "Doors, frames and signage", "Wall protection and corner guards", "Floor type"],
 ["Corridors re-soil quickly if trades are still working in rooms.", "Floor cleaning must leave a dry, safe path for traffic."],
 [("What is included in corridor final cleaning?", "Ceiling fixtures, walls, wall protection, doors and frames, signage, fire devices and floors, cleaned top down."),
  ("Why are corridors often cleaned last?", "Trades use them to reach rooms, so cleaning them early means cleaning them twice."),
  ("Are corner guards and wall protection cleaned?", "Yes, they collect film, adhesive and scuffs and are cleaned with suitable products."),
  ("How are corridors cleaned while people use them?", "In sections, with signs and dry paths kept open for traffic.")]),
"Lobby final detailing": T(
 "Lobby final detailing is the most detailed cleaning in the building: entry glass and doors, feature walls, stone and specialty floors, reception desks, lighting, elevator lobbies, furniture and signage.",
 "The lobby forms the first impression for owners, tenants, guests and inspectors. It usually has the most expensive finishes in the building and gets the most construction traffic.",
 "Crews detail every surface with finish-specific methods, use lifts for high glass and fixtures, finish floors last and return for a touch-up right before the owner walk.",
 ["Lobby finishes: stone, glass, metal, wood", "Feature walls and lighting", "Reception and furniture", "High areas needing lifts"],
 ["Stone floors and walls need stone-safe products.", "Lobbies re-soil quickly from traffic; schedule a touch-up."],
 [("Why does the lobby get the most detailed cleaning?", "It is the first impression of the building and usually has its most expensive finishes."),
  ("Are lobby feature walls and lighting cleaned?", "Yes, with methods suited to each material, and lifts for high elements."),
  ("When is the lobby cleaned in the closeout sequence?", "Near the very end, because construction traffic passes through it, and again as a touch-up before the owner walk."),
  ("How are stone lobby floors cleaned?", "With pH-neutral stone cleaners and soft pads, never acidic products.")]),
}
