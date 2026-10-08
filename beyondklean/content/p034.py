def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"FRP trim and seam detailing": T(
 "FRP trim and seam detailing cleans the plastic or metal division bars, inside and outside corners, cap moldings and seams between FRP panels, removing dust, adhesive and grime.",
 "Trim and seams are where dirt and adhesive collect on FRP walls. Gaps and dirty joints are a sanitation concern in food areas.",
 "Crews clean trim with soft brushes and neutral cleaner, remove adhesive at joints and report open seams or loose trim for repair.",
 ["Linear feet of trim", "Seam and joint condition", "Adhesive at trim", "Loose or missing trim"],
 ["Do not pull or pry loose trim pieces.", "Open seams should be reported for sealing."],
 [("What is FRP trim?", "Plastic or metal moldings that join FRP panels and finish corners and edges."),
  ("Why do FRP seams need detailing?", "Dirt and adhesive collect in joints and are hard to see until the wall is finished."),
  ("Are FRP seams sealed?", "In food areas, seams are often sealed so they stay cleanable."),
  ("Is FRP trim cleaned during kitchen turnover?", "Yes, as part of the wall cleaning.")]),
"Insulated metal panel wall cleaning": dict(
 a="Insulated metal panel wall cleaning cleans the metal-faced insulated panels used for coolers, freezers, food processing rooms and cold storage, removing film, dust and residue with food-safe, non-abrasive products.",
 m="Crews remove protective film, wash panels with food-safe cleaners and soft brushes, rinse and dry, paying attention to seams and corners.",
 w=["Abrasive pads scratch panel coatings and create places for bacteria to grow.", "Moisture left in seams of cold rooms can freeze."],
 q=[("Where are insulated metal panels used?", "In walk-in coolers and freezers, cold storage, food processing rooms and some clean manufacturing spaces."),
  ("How are insulated metal panels cleaned?", "With food-safe, non-abrasive cleaners and soft brushes, followed by rinsing and drying."),
  ("Can moisture damage insulated metal panels?", "Water left in seams of cold rooms can freeze and damage seals, so panels are dried."),
  ("Are insulated panels inspected in food facilities?", "Yes, inspectors and auditors check that walls are clean, intact and cleanable.")]),
"Grocery store post-construction cleaning": dict(
 a="Grocery store post-construction cleaning prepares new or remodeled supermarkets for opening: overhead structure, sales floor, refrigerated cases, departments, back room, restrooms and exterior, phased around each department's handover.",
 y="Grocery openings are complex, involve food departments with health inspections, and run on fixed dates. Dust overhead or in cases ends up on food.",
 q=[("How long does a grocery store opening clean take?", "Several days to a few weeks, phased by department as each is handed over, with a final touch-up before opening."),
  ("Is overhead cleaning part of a grocery store opening?", "It should be. Open ceilings over food areas collect construction dust that falls onto product after opening."),
  ("Who cleans grocery refrigeration cases?", "Cleaning crews clean case interiors and exteriors; refrigeration contractors handle coils and mechanical parts."),
  ("Do grocery openings require health inspection?", "Yes, food departments are inspected before the store can open.")]),
"Refrigerated case detailing": dict(
 a="Refrigerated case detailing cleans grocery and convenience store display cases, reach-ins, coffin cases and multidecks inside and out, including shelves, glass doors, frames, kick plates and drain pans, before startup and stocking.",
 y="Refrigerated cases display food directly to shoppers. Construction dust inside cases ends up on product, and dirty glass doors look neglected.",
 q=[("How are refrigerated display cases cleaned after construction?", "Shelves are removed where designed to, interiors and doors are cleaned with food-safe products and exteriors and kick plates are wiped."),
  ("When should refrigerated cases be cleaned?", "Before startup and stocking, when they are empty and warm."),
  ("Who cleans refrigerated case coils?", "Refrigeration technicians; cleaning crews do not touch coils or fans."),
  ("Are case kick plates and bumpers cleaned?", "Yes, they collect construction dust and scuffs at floor level.")]),
"Deli department finish cleaning": dict(
 a="Deli department finish cleaning prepares a grocery or standalone deli for opening, including service cases, prep areas, sinks, walls, ceilings, floors and the exteriors of slicers and equipment.",
 y="Delis handle ready-to-eat food, which carries higher food safety risk. Inspectors examine deli departments closely before a store can open.",
 w=["Slicers and food equipment are cleaned and sanitized by trained staff per the manufacturer.", "Only food-safe products may be used in food areas."],
 q=[("Who cleans deli slicers before opening?", "Trained deli staff, following the manufacturer's cleaning and sanitizing procedure."),
  ("Why is deli cleaning so important?", "Delis handle ready-to-eat food that will not be cooked again, so contamination risk is higher."),
  ("Are deli service cases cleaned inside?", "Yes, case interiors, glass and shelves are cleaned before product is displayed."),
  ("Is the deli inspected separately from the rest of the store?", "Often, food departments get specific attention during the health inspection.")]),
}
