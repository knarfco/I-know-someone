def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Restroom accessory cleaning": dict(
 a="Restroom accessory cleaning cleans soap and towel dispensers, toilet paper holders, grab bars, sanitary bins, mirrors with shelves and baby changing stations, removing film, labels and dust.",
 y="Accessories are installed late, usually with film and labels still on, and they are touched constantly once the restroom opens.",
 q=[("What are restroom accessories?", "Soap and towel dispensers, toilet paper holders, grab bars, sanitary bins, baby changing stations and similar items."),
  ("Do new dispensers come with packaging inside?", "Often. Packaging and shipping inserts should be removed so dispensers can be loaded."),
  ("How is stainless steel restroom accessory cleaned?", "With a neutral cleaner, then wiped dry with the grain to avoid streaks."),
  ("Are grab bars cleaned during the final clean?", "Yes, they are cleaned and checked for labels and film.")]),
"Hand dryer cleaning": dict(
 a="Hand dryer cleaning cleans the exterior, air intake and outlet of electric hand dryers, removing film, labels and the construction dust that collects in intakes.",
 w=["Never spray liquid into hand dryers or their intakes.", "Units should not be opened by cleaning crews."],
 q=[("Do hand dryers need cleaning after construction?", "Yes. Dust collects in the intake and is blown at users the first time the dryer runs."),
  ("How are hand dryers cleaned?", "Exteriors are wiped with a damp cloth and intakes are vacuumed, without spraying liquid into the unit."),
  ("Can hand dryer filters be changed by cleaners?", "Filters are changed by facility staff according to the manufacturer's instructions."),
  ("Why not spray cleaner on a hand dryer?", "Liquid can enter the motor and electronics and damage the unit.")]),
"Floor drain and trap primer area cleaning": dict(
 w=["Washing debris down a floor drain moves the clog further into the line.", "Damaged or missing strainers should be reported to the plumber."],
 q=[("Why clean floor drains after construction?", "Grout, mortar and debris collect in floor drains during tile work and can clog them the first time water is used."),
  ("What is a trap primer?", "A device that adds water to a floor drain trap so it does not dry out and let sewer gas into the room."),
  ("Can construction debris be flushed down a floor drain?", "No. It should be removed by hand or vacuum, because flushing it moves the clog deeper."),
  ("Who checks that floor drains work?", "The plumber tests drain function; the cleaning crew removes debris and reports slow drains.")]),
"Restroom tile and grout detailing": T(
 "Restroom tile and grout detailing cleans restroom floor and wall tile, removing grout haze, thinset residue and dirt from tile faces and grout lines, and leaves grout ready for sealing where specified.",
 "Restroom tile is inspected closely, and grout haze makes new tile look dull. Grout absorbs dirt and moisture quickly once the restroom is used.",
 "Crews remove haze with removers compatible with the tile and grout, scrub grout lines with soft brushes, rinse thoroughly and dry before sealing.",
 ["Tile and grout types", "Haze or residue present", "Sealer plans", "Restroom count"],
 ["Acidic removers can damage cementitious grout and stone.", "Unsealed grout stains quickly."],
 [("How is restroom tile detailed after construction?", "Grout haze is removed with compatible products, grout lines are scrubbed and the floor and walls are rinsed and dried."),
  ("Should restroom grout be sealed?", "Cementitious grout often benefits from sealing to resist stains and moisture."),
  ("Why does restroom grout darken so quickly?", "Grout is porous and absorbs dirt and moisture from foot traffic and cleaning."),
  ("Is restroom tile part of the final clean?", "Yes, tile and grout are detailed as part of the restroom clean.")]),
"Drinking fountain and bottle filler cleaning": dict(
 a="Drinking fountain and bottle filler cleaning cleans the exteriors, basins, spouts, grilles and drains of drinking fountains and bottle filling stations, removing labels, film and construction dust.",
 q=[("How are drinking fountains cleaned after construction?", "Basins, spouts and exteriors are cleaned with food-safe products, and labels and film are removed."),
  ("Do bottle filling stations have filters?", "Many do. Filters are installed and changed by facility staff or the plumber."),
  ("Are drinking fountains part of the final clean?", "Yes, they are cleaned with the restrooms and corridors."),
  ("Should new drinking fountains be flushed?", "Plumbers or facility staff flush new fixtures to clear the lines before use.")]),
}
