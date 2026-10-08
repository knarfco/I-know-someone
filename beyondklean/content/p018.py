def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Rust stain removal from finishes": dict(q=[
  ("What causes rust stains on new finishes?", "Steel tools, paint cans, fasteners and metal debris left on damp surfaces leave orange rings and spots. Tile, stone, concrete and painted surfaces are most affected."),
  ("Can rust stains be removed from marble?", "Sometimes, with stone-safe rust poultices applied patiently. Acidic rust removers will etch marble, so they are not used on it."),
  ("What is a rust poultice?", "A paste of absorbent material and a rust-dissolving agent that is spread on porous stone, covered and left to draw the stain out as it dries."),
  ("Who removes rust stains from finished surfaces?", "Cleaning crews handle most rust spots, and stone restoration specialists handle stains on delicate or expensive natural stone.")]),
"Water spot and mineral deposit removal": dict(
 a="Water spot and mineral deposit removal cleans hard water spots, mineral rings and scale from faucets, fixtures, glass, stainless steel and counters that appear after plumbing is tested or surfaces are washed.",
 y="Water spots appear as soon as fixtures are run for testing and as soon as surfaces are washed and left to air-dry. They make brand-new chrome and glass look dirty and get harder to remove as they build up.",
 q=[("How do you remove water spots from new faucets?", "With a mild descaler or a cleaner made for the fixture's finish, followed by rinsing and drying with a soft cloth. Abrasives scratch chrome and specialty finishes."),
  ("Why do water spots appear on new fixtures?", "Minerals in tap water stay behind when droplets evaporate. Plumbing tests and wet cleaning leave plenty of droplets."),
  ("Can vinegar remove hard water spots?", "Vinegar works on some surfaces, but it is acidic and can damage natural stone, some grout and certain metal finishes, so it is not used everywhere."),
  ("How are water spots prevented after cleaning?", "By drying fixtures, glass and stainless with a clean cloth instead of letting them air-dry.")]),
"Tar and roofing material removal": dict(
 a="Tar and roofing material removal cleans asphalt, roofing cement, mastic, sealant and tar from walls, walkways, windows, fixtures and floors near roofing and waterproofing work, including tar tracked inside on boots.",
 y="Roofing tar is sticky, black and spreads easily. It is tracked from roofs and waterproofing areas onto walkways and new floors, where it stains and is hard to remove.",
 w=["Solvent-based tar removers can damage paint, plastics and resilient flooring.", "Tar tracked onto new floors spreads quickly; stop the source with mats and boot cleaning."],
 q=[("How is roofing tar removed from concrete walkways?", "Bulk material is scraped off when cool and hard, then a tar remover suited to concrete is applied, agitated and rinsed with the water recovered."),
  ("Can tar be removed from windows and frames?", "Usually, with careful scraping on glass and tar removers that are safe for the frame finish, tested first."),
  ("How does tar get onto new floors inside a building?", "Workers track it on boots from roofs and waterproofing areas. Walk-off mats and boot cleaning stations reduce it."),
  ("Who removes roofing tar at the end of a project?", "The roofer is often responsible for tar outside their work area, with the cleaning crew handling remaining spots.")]),
"Floor protection installation": dict(
 a="Floor protection installation lays temporary board, rolled protection or adhesive film over finished floors after they are installed, so tools, lifts, debris and foot traffic do not damage them during the rest of construction.",
 y="New floors are installed while many trades are still working. Without protection, finished floors get scratched, gouged and stained, and repairs or replacement are expensive and slow.",
 w=["Debris trapped under protection acts like sandpaper and scratches the floor.", "Some tapes and films damage floor finishes or leave residue."],
 q=[("Why should floors be cleaned before protection goes down?", "Debris trapped under protection grinds into the floor under foot traffic and scratches it. A clean floor under protection stays undamaged."),
  ("What kinds of floor protection are used in construction?", "Heavy-duty paper-based boards, corrugated plastic sheets, adhesive films for carpet and hard floors, and plywood in heavy traffic or lift areas."),
  ("Can floor protection damage new floors?", "It can if the wrong tape is used, if moisture is trapped underneath or if debris is left under it."),
  ("Who installs floor protection?", "The GC, the flooring contractor or the cleaning crew, depending on the contract and schedule.")]),
"Floor protection removal and disposal": dict(
 a="Floor protection removal and disposal takes up temporary floor protection near the end of the project, captures the dust and debris trapped on and beneath it, disposes of it properly and leaves the floor ready for final cleaning.",
 y="Floor protection holds weeks of construction dust on its surface. Ripping it up quickly releases that dust into clean areas and drags debris across the finished floor.",
 w=["Dragging protection across floors scratches them with trapped debris.", "Tape residue left behind must be removed with floor-safe products."],
 q=[("When is floor protection removed at the end of construction?", "Near the final clean, after the heaviest trades and lifts are done in that area and before the owner walk."),
  ("What happens to the dust on top of floor protection?", "It is HEPA vacuumed off first, and the protection is rolled or folded inward so the dust stays trapped as it is removed."),
  ("Is used floor protection recyclable?", "Some board products can be recycled or reused if they are clean and dry, depending on local recycling options."),
  ("Who removes floor protection?", "The cleaning crew or the GC, coordinated so the final floor clean happens right after.")]),
"Adhesive under floor protection cleanup": T(
 "Adhesive under floor protection cleanup removes the tape lines and adhesive residue left on finished floors after temporary protection is taken up, using removers that are safe for each floor type.",
 "Tape seams and adhesive films used to hold protection in place leave sticky lines that trap dirt within days and show up as dark strips across new floors.",
 "Crews identify the floor type, use the gentlest compatible remover with soft pads, and follow with a neutral cleaner so no remover residue is left behind.",
 ["Floor types under protection", "Tape and film types used", "Remover compatibility", "Final floor clean timing"],
 ["Solvents can soften vinyl, rubber and floor finishes.", "Residue that is not fully removed turns black under traffic."],
 [("Does floor protection tape leave residue on new floors?", "Often, especially when tape was left on for weeks or exposed to heat. The residue shows up as sticky lines along seams."),
  ("How is tape residue removed from vinyl or LVT floors?", "With a remover the flooring manufacturer allows, applied with a soft pad and followed by a neutral cleaner."),
  ("Can adhesive removers damage new floors?", "Some can, especially strong solvents on vinyl, rubber and finished wood, which is why products are tested first."),
  ("Who cleans tape residue after protection is removed?", "The cleaning crew during the final floor clean.")]),
}
