def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Store opening clean": dict(q=[
  ("When should a new store be cleaned before opening?", "In stages: overhead cleaning before fixtures go in, fixture cleaning before merchandise is set, and floors, glass and the entrance right before opening day."),
  ("What is included in a retail store opening clean?", "Overhead structure, light fixtures, fixtures and shelving, glass and storefront, fitting rooms, cash wrap, stockroom, restrooms and floors, plus the entrance and sidewalk."),
  ("How long does a store opening clean take?", "From one day for a small shop to several days or overnight shifts for a big-box store, usually split around fixture and merchandise delivery."),
  ("Who coordinates the cleaning for a store opening?", "Usually the GC, working with the retailer's opening or construction manager so cleaning stays ahead of merchandise.")]),
"Gondola shelving detailing": dict(
 a="Gondola shelving detailing cleans freestanding, double-sided retail aisle shelving top to bottom: shelves, uprights, back panels, base decks, kick plates and price channels, before products are stocked.",
 q=[("What is gondola shelving?", "Freestanding, double-sided shelving units that form the aisles in grocery, pharmacy and big-box stores. They are assembled on site late in construction."),
  ("When should gondolas be cleaned in a new store?", "After the fixture installers finish and before stocking begins. Once products are on the shelves, a thorough cleaning is nearly impossible."),
  ("Are price channels cleaned during gondola detailing?", "Yes. Price channels and shelf edges trap dust and debris that show clearly once price labels are installed."),
  ("Why does new store shelving need cleaning?", "Shelving is assembled while the store is still dusty, and it arrives with packaging debris, fingerprints and labels.")]),
"Wall fixture and slatwall cleaning": T(
 "Wall fixture and slatwall cleaning cleans slatwall panels, grid walls, wall standards, brackets and wall-mounted display fixtures in retail stores, including the grooves and inserts that trap dust.",
 "Wall fixtures sit at eye level along the store perimeter where shoppers look first. Slatwall grooves collect drywall dust that falls onto merchandise once hooks and shelves are loaded.",
 "Crews vacuum each groove with crevice tools from top to bottom, wipe faces and inserts with damp microfiber, and clean standards and brackets before merchandise is hung.",
 ["Linear feet of slatwall and grid wall", "Metal or plastic groove inserts", "Accessories already installed", "Merchandising schedule"],
 ["Plastic groove inserts scratch with abrasive pads.", "Removing accessories set by the visual team can disrupt the layout."],
 [("How is slatwall cleaned in a new store?", "Each groove is vacuumed with a crevice tool, then the faces and inserts are wiped with damp microfiber, working top to bottom."),
  ("Why does slatwall get so dusty during construction?", "Its horizontal grooves act like shelves that collect drywall and ceiling dust."),
  ("Should wall fixtures be cleaned before merchandise is hung?", "Yes, because dust in the grooves falls onto merchandise and packaging once it is loaded."),
  ("What is grid wall?", "A wire grid panel system used to hang hooks, baskets and shelves in retail displays.")]),
"Display fixture and mannequin cleaning": T(
 "Display fixture and mannequin cleaning cleans freestanding tables, racks, rounders, display platforms, acrylic risers and mannequins on the sales floor before the store opens.",
 "Display fixtures are where shoppers look and touch first. Dust, fingerprints and labels on them undermine the store's presentation, and mannequin finishes are easily damaged.",
 "Crews clean each fixture by material, using mild cleaners and soft cloths on mannequins and acrylic, and coordinate with the visual merchandising team before moving anything.",
 ["Fixture types and finishes", "Mannequin finishes", "Acrylic and glass displays", "Visual merchandising schedule"],
 ["Solvents can damage mannequin finishes and acrylic.", "Moving placed fixtures without the visual team's approval disrupts the layout."],
 [("How are store mannequins cleaned?", "Gently, with a mild cleaner and soft cloth, because many mannequin finishes are damaged by solvents and abrasives."),
  ("Are display tables cleaned before merchandise is set?", "Yes, so dust and packaging debris do not end up on the first products shoppers see."),
  ("Do acrylic displays scratch easily?", "Yes. Acrylic is cleaned with mild soap or acrylic cleaners and soft cloths only."),
  ("Who places mannequins and display fixtures?", "The retailer's visual merchandising team, so cleaning is coordinated with them.")]),
"Fitting room cleaning": T(
 "Fitting room cleaning details each fitting room before a store opens: doors or curtains, mirrors, benches, hooks, walls, lighting and floors, plus the fitting room lounge area.",
 "Fitting rooms are small, brightly lit and mirrored, so every speck of dust and fingerprint shows. Shoppers spend time in them and judge the store by them.",
 "Crews clean top down in each room, clean mirrors by spraying onto cloths instead of the mirror, wipe hooks and benches and vacuum or mop floors last.",
 ["Number of fitting rooms", "Mirrors and lighting", "Doors, curtains and hooks", "Floor type"],
 ["Liquid behind mirror edges damages the silvering.", "Curtain fabrics may need dry cleaning methods only."],
 [("Are fitting rooms cleaned before a store opens?", "Yes, each room is detailed because shoppers spend time in them and notice everything."),
  ("How are fitting room mirrors cleaned?", "Cleaner is sprayed onto a cloth, not the mirror, so liquid does not run behind the edges."),
  ("Are fitting room hooks and benches cleaned?", "Yes, they collect dust and fingerprints from installation."),
  ("Why are fitting rooms a focus at opening?", "They are small, mirrored and brightly lit, so dirt is very visible.")]),
}
