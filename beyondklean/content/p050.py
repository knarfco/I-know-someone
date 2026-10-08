def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Stone polishing and honing": dict(
 m="Requests are reviewed and routed only to stone restoration specialists with the right diamond tooling and slurry control.",
 w=["Improper honing can leave swirl marks or uneven finishes.", "Slurry must be contained and kept out of drains and adjacent finishes."],
 q=[("What is stone honing?", "Grinding the stone surface with fine abrasives to remove etching and scratches and create a smooth, matte finish."),
  ("Can etched marble be repaired?", "Yes. Honing removes the etched layer and polishing restores the shine."),
  ("Is stone polishing a cleaning service?", "No, it is restoration work done by stone specialists."),
  ("Who polishes natural stone floors?", "Stone restoration contractors with diamond tooling and slurry control.")]),
"Terrazzo initial clean": dict(
 y="Terrazzo is a premium floor, and its first cleaning sets up its long-term appearance. Harsh acids and alkalis damage cement terrazzo and its sealer.",
 w=["Acids and high-alkaline cleaners damage cement terrazzo.", "Sealer timing should follow the terrazzo contractor's guidance."],
 q=[("What is terrazzo flooring?", "A floor made of marble, glass or other chips set in cement or epoxy and ground smooth."),
  ("How is a new terrazzo floor cleaned?", "With pH-neutral cleaners recommended for terrazzo and soft pads."),
  ("Does terrazzo need to be sealed?", "Usually yes, cement terrazzo is sealed; epoxy terrazzo may need less."),
  ("Can terrazzo be damaged by cleaners?", "Yes, by acids and strong alkalis, which can etch chips and dull the surface.")]),
"Terrazzo polishing": T(
 "Terrazzo polishing grinds and polishes cement or epoxy terrazzo floors with diamond tooling to remove scratches, etching and wear and restore the finish. It is restoration specialty work.",
 "Worn, etched or scratched terrazzo can often be restored instead of replaced, but improper grinding damages the matrix and chips.",
 "Requests are reviewed and routed only to terrazzo restoration specialists, who grind and polish in stages and control slurry.",
 ["Terrazzo type: cement or epoxy", "Condition and damage", "Area and access", "Downtime"],
 ["Improper grinding can expose voids or damage chips.", "Slurry must be controlled."],
 [("Can old terrazzo floors be restored?", "Often yes, by grinding and polishing to remove wear and etching."),
  ("Is terrazzo polishing done by cleaning crews?", "No, it is done by terrazzo restoration specialists."),
  ("How long does terrazzo polishing take?", "It depends on area and condition, often several days for large lobbies."),
  ("Does terrazzo need sealing after polishing?", "Cement terrazzo is usually sealed after polishing.")]),
"Mosaic and specialty tile detailing": dict(
 w=["Glass mosaic tile scratches easily with abrasive pads.", "Some decorative tiles and glazes are sensitive to acids."],
 q=[("How are mosaic tiles cleaned after installation?", "With soft brushes and haze removers compatible with glass, stone or ceramic mosaics, rinsing carefully."),
  ("Can glass tile be scratched during cleaning?", "Yes, abrasive pads and gritty water can scratch glass tile."),
  ("Why is grout haze harder to remove from mosaics?", "Mosaics have far more grout joints per square foot, so there is much more haze to remove."),
  ("Is mosaic detailing part of the final clean?", "Yes, especially in restrooms, lobbies and feature walls.")]),
"Thinset and mortar splatter removal": dict(
 a="Thinset and mortar splatter removal takes hardened tile setting material and mortar splatter off tile and stone faces, edges and adjacent finishes after installation.",
 w=["Scraping can scratch glazed and polished tile.", "Acidic removers can etch stone and damage grout."],
 q=[("What is thinset?", "The cement-based adhesive used to set tile and stone."),
  ("How is dried thinset removed from tile?", "Soften it, scrape carefully with plastic tools and clean with compatible removers."),
  ("Who should remove thinset from new tile?", "The tile installer, ideally while it is still fresh; cleaning crews remove what remains."),
  ("Can thinset removal damage stone?", "Yes, if acidic removers are used on marble or limestone.")]),
}
