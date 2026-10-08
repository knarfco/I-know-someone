def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Bakery department finish cleaning": dict(
 a="Bakery department finish cleaning prepares in-store and standalone bakeries for opening: oven and proofer exteriors, mixers, worktables, racks, sinks, walls, ceilings and floors.",
 y="Bakeries are inspected like any food area, and flour dust builds up quickly once production starts. Starting from a truly clean space makes daily cleaning easier.",
 m="Crews clean top down with food-safe products, detail equipment exteriors and racks, and leave oven interiors and equipment startup to vendors.",
 q=[("Who cleans bakery ovens before opening?", "Oven interiors are handled by the equipment vendor or trained staff during startup; crews clean exteriors."),
  ("Are bakery racks and pans cleaned?", "Racks are cleaned before use; pans are usually washed by bakery staff."),
  ("Why clean bakery walls and ceilings before opening?", "Flour and dust settle on every surface once production starts, so a clean start matters."),
  ("Is bakery cleaning food-safe?", "Yes, only food-safe products are used in food production areas.")]),
"Meat and seafood department finish cleaning": T(
 "Meat and seafood department finish cleaning prepares grocery cutting rooms, service cases, coolers and wrapping areas for opening, focusing on surfaces, walls, drains and equipment exteriors.",
 "Meat and seafood rooms have strict sanitation requirements and are inspected closely. Drains, walls and equipment must be clean before any product arrives.",
 "Crews clean top down with food-safe products, clear and clean floor drains, detail walls and cases, and leave equipment sanitizing to trained staff.",
 ["Cutting room and coolers", "Service cases", "Floor drains", "Equipment exteriors"],
 ["Drains must be clear before production begins.", "Saws and grinders are cleaned and sanitized by trained staff only."],
 [("Why are meat rooms cleaned so carefully before opening?", "Raw meat and seafood carry higher contamination risks, so sanitation requirements and inspections are strict."),
  ("Are meat room floor drains cleaned?", "Yes, drains are cleared of construction debris so the room can be washed down daily."),
  ("Who sanitizes meat cutting equipment?", "Trained department staff following the equipment manufacturer's procedures."),
  ("Are meat cases cleaned before stocking?", "Yes, case interiors and glass are cleaned before product is displayed.")]),
"Produce department finish cleaning": T(
 "Produce department finish cleaning prepares produce cases, wet racks, display tables, misting system exteriors, prep rooms and floors in a grocery store before opening.",
 "Produce departments use water constantly, so drains and floors must work and display cases must be clean before fresh product is set.",
 "Crews clean cases and displays with food-safe products, clear drains and leave misting system service to the vendor.",
 ["Cases and display tables", "Misting system", "Prep room and drains", "Floors"],
 ["Misting systems are installed and serviced by vendors.", "Wet produce floors are slippery; keep them dry during cleaning."],
 [("How are produce cases cleaned before opening?", "With food-safe products inside and out, including shelves, mirrors and drain pans."),
  ("Who services produce misting systems?", "The misting system vendor installs, sanitizes and maintains it."),
  ("Are produce display tables cleaned?", "Yes, tables and bins are cleaned before produce is set."),
  ("Why are produce department floors slippery?", "Water from misting and washing produce, so floors and drains must work well.")]),
"Checkstand and conveyor cleaning": T(
 "Checkstand and conveyor cleaning cleans grocery and retail checkout lanes: counters, conveyor belts, bagging areas, impulse racks and the exteriors of scanners, scales and card readers.",
 "Every customer passes through the checkstands. Construction dust and fingerprints on belts and counters are the last thing shoppers see.",
 "Crews wipe belts and counters with cleaners safe for the belt material and wipe electronics with dry or barely damp cloths, never spraying devices.",
 ["Number of checkstands", "Belt material", "Electronics", "Bagging and impulse areas"],
 ["Do not spray liquids on scanners, scales or card readers.", "Belts can be damaged by solvents."],
 [("How are checkout conveyor belts cleaned?", "With cleaners safe for the belt material and soft cloths, while the belt is stopped."),
  ("Are scanners and scales cleaned before opening?", "Exteriors are wiped gently, without spraying liquid onto the device."),
  ("Are checkstands cleaned at store opening?", "Yes, they are detailed after equipment is installed."),
  ("Who services checkstand belts and equipment?", "The fixture or equipment vendor.")]),
"Receiving and loading bay cleaning": T(
 "Receiving and loading bay cleaning cleans back-of-house receiving areas, dock plates, dock walls, receiving offices and floors in grocery stores and retail buildings before deliveries begin.",
 "Receiving areas take every delivery during construction and collect debris, pallets and mud. Food deliveries require a clean receiving area.",
 "Crews remove debris and pallets, sweep and scrub floors, wipe dock walls and doors and clear drains.",
 ["Receiving area size", "Dock equipment", "Debris and pallets", "Floor drains"],
 ["Dock edges are fall hazards.", "Drains must be protected from debris."],
 [("Why clean receiving areas before a store opens?", "Food and merchandise deliveries need a clean receiving area, and construction leaves it full of debris."),
  ("Are dock levelers cleaned?", "Exteriors and pits are cleaned only with the dock equipment locked out."),
  ("Is the receiving area inspected?", "Food facilities' receiving areas are often checked during inspection."),
  ("Who cleans receiving areas at turnover?", "The cleaning crew as part of back-of-house cleaning.")]),
}
