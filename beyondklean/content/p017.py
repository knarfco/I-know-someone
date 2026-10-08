def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Spray foam overspray removal": dict(
 a="Spray foam overspray removal takes cured or partly cured polyurethane spray foam insulation off framing, windows, floors, equipment and fixtures near areas that were insulated, without damaging the surfaces underneath.",
 q=[("Can cured spray foam be removed from windows?", "Usually yes, by careful mechanical removal with plastic tools and, on suitable glass, a lubricated blade. Cured foam does not dissolve easily, so solvents rarely help."),
  ("Why is spray foam overspray so hard to remove?", "Spray foam bonds aggressively and cures within minutes. Once cured, it is tough and has to be cut or scraped off rather than wiped."),
  ("Who is responsible for spray foam overspray?", "Typically the insulation contractor, who should mask nearby surfaces. Remaining overspray is often removed at final clean and back-charged."),
  ("Is protective equipment needed around spray foam?", "Yes, especially around uncured foam, which can irritate skin and lungs. Crews follow the foam manufacturer's re-entry and PPE guidance.")]),
"Fireproofing overspray removal": dict(q=[
  ("Can spray-applied fireproofing overspray be removed?", "Yes, from surfaces where it does not belong, such as ducts, conduit or glass. It must be done by qualified crews with approval so required fireproofing is not damaged."),
  ("Why is fireproofing removal treated as conditional work?", "Fireproofing is a life-safety system, and older materials may contain asbestos. Work near it needs testing, approval and a defined procedure."),
  ("Who repairs fireproofing damaged during cleanup?", "The fireproofing contractor repairs it, and the area is typically re-inspected before ceilings close."),
  ("Is fireproofing dust hazardous?", "It can irritate lungs and may contain hazardous fibers in older buildings, so dust controls and testing are required before disturbance.")]),
"Joint compound film removal": dict(
 a="Joint compound film removal takes the thin white film of drywall mud off floors, window frames, glass, doors and other finishes where it was smeared, splashed or tracked during taping and finishing.",
 y="Mud film looks chalky and dull, shows clearly on dark finishes and floors, and spreads into a wider haze if it is wiped with a wet rag. It is one of the most common residues at final clean.",
 q=[("How do you remove drywall mud film from floors?", "Dry-remove and HEPA vacuum the loose material first, then clean with fresh water and microfiber in small sections, changing water often so the gypsum is lifted instead of spread."),
  ("Why does drywall mud film come back after mopping?", "Dirty mop water redeposits the dissolved gypsum as the floor dries. Fresh water and frequent rinsing prevent the haze."),
  ("Is joint compound film a common punch list item?", "Yes. White haze on floors, frames and dark finishes shows up on most punch lists in drywall-heavy projects."),
  ("Who is responsible for joint compound residue?", "The drywall contractor should clean up after themselves, but the cleaning crew usually removes remaining film at final clean.")]),
"Pencil, marker and layout line removal": dict(
 a="Pencil, marker and layout line removal cleans the layout marks, chalk lines, measurements, pencil notes and permanent marker that trades leave on walls, floors, ceilings and exposed concrete that remain visible in the finished space.",
 w=["Permanent marker can bleed through paint, so it should be removed or sealed before painting.", "Solvent-based marker removers can damage paint, vinyl and some plastics."],
 q=[("How do you remove permanent marker from exposed concrete?", "With a marker or graffiti remover made for concrete, tested first, and a stiff brush. Several light applications work better than one aggressive one."),
  ("Can chalk layout lines be removed from floors?", "Usually yes, with dry brushing or vacuuming first and then a mild cleaner. Colored chalk can stain porous concrete, so act early."),
  ("Do layout marks bleed through new paint?", "Permanent marker and some crayons can bleed through paint. They should be removed or primed with a stain-blocking primer before painting."),
  ("Who removes layout marks before turnover?", "The cleaning crew removes them at final clean, or the responsible trade if the marks are on finished surfaces they installed.")]),
"Label, sticker and UPC removal": dict(
 a="Label, sticker and UPC removal takes manufacturer labels, barcodes, shipping stickers and promotional decals off fixtures, doors, equipment, glass and appliances throughout a building, while leaving required safety and rating labels in place.",
 w=["Fire rating labels, nameplates, warning labels and inspection tags must stay in place.", "Razor blades scratch soft plastics, painted metal and coated surfaces."],
 q=[("Which labels should not be removed during final cleaning?", "Fire rating labels on doors and frames, equipment nameplates, electrical warning labels and inspection tags. Removing them can fail an inspection."),
  ("How is sticker residue removed without scratching?", "Peel the label slowly, then use a surface-safe adhesive remover and a plastic scraper. Blades are only used on glass that allows it."),
  ("Why are leftover labels such a common punch item?", "Almost every item delivered to a jobsite has labels, and every one left behind looks unfinished to the owner."),
  ("Who removes labels at the end of construction?", "The cleaning crew at final clean, working room by room so nothing is missed.")]),
"Protective film removal from appliances and fixtures": dict(
 a="Protective film removal from appliances and fixtures peels the plastic film shipped on stainless appliances, plumbing fixtures, glass, metal trim and plastic surfaces, and removes the adhesive left behind.",
 m="Crews peel film slowly from a corner, warm stubborn film gently, remove adhesive with surface-safe products and finish stainless with a clean wipe along the grain.",
 w=["Film left on for months, especially near windows, bakes on and leaves residue.", "Blades and abrasive pads scratch stainless and plastic finishes."],
 q=[("When should protective film be removed from new appliances?", "At final clean, as close to turnover as practical but before heat and sun bake the adhesive on. Film near windows and cooking equipment should come off sooner."),
  ("Why does protective film leave residue?", "Heat, sunlight and time make the film's adhesive bond to the surface, so it stays behind when the film is peeled."),
  ("How is film residue removed from stainless steel?", "With a stainless-safe adhesive remover and a soft cloth, then a neutral cleaner wiped along the grain and dried."),
  ("Who removes protective film from fixtures and appliances?", "The installer or the cleaning crew, depending on the contract. Most often it happens during the final clean.")]),
}
