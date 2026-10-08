def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Epoxy and resinous floor cleaning": dict(
 m="Crews dust mop or vacuum grit, then scrub with neutral or manufacturer-approved cleaners and soft pads, recovering the water and rinsing so no residue makes the floor slippery.",
 w=["Aggressive pads wear down anti-slip textures and gloss.", "Some solvents soften or stain resinous coatings."],
 q=[("How are epoxy floors cleaned?", "With neutral or manufacturer-approved cleaners and soft pads, followed by rinsing so no residue remains."),
  ("Can epoxy floors be scratched?", "Yes, by grit dragged under traffic and by aggressive pads, so grit is removed first."),
  ("Do epoxy floors need wax?", "Usually not. Most resinous floors are maintained with cleaning alone."),
  ("Where are epoxy and resinous floors used?", "In garages, commercial kitchens, labs, healthcare, warehouses and industrial spaces.")]),
"Parking garage floor scrubbing": dict(q=[
  ("How are parking garages cleaned after construction?", "Dry debris is swept first, then decks are scrubbed or pressure washed with the water recovered instead of flowing to drains."),
  ("Can parking garage wash water go into the drains?", "Garage drains often connect to storm sewers or oil separators, so wash water is generally recovered."),
  ("Do garage traffic coatings need special care?", "Yes. High pressure and harsh chemicals can damage traffic coatings and waterproofing membranes."),
  ("How often are parking garages cleaned?", "At turnover, then typically once or twice a year with regular sweeping in between.")]),
"VCT initial floor finish": dict(q=[
  ("Why does new VCT need an initial floor finish?", "New vinyl composition tile has a factory coating that floor finish does not bond to well. It must be prepared and then built up with several coats."),
  ("How many coats of finish go on new VCT?", "Commonly four to six thin coats, depending on the specification and traffic."),
  ("When can people walk on new floor finish?", "After it cures per the product, usually light traffic after a few hours and full traffic after a day or more."),
  ("Is floor finish the same as wax?", "Floor finish is a polymer coating, but people commonly call it wax.")]),
"VCT strip and refinish": dict(q=[
  ("What does stripping a VCT floor mean?", "Removing all the old floor finish with a chemical stripper and scrubbing, down to the bare tile, before applying new coats."),
  ("How often do VCT floors need stripping?", "Depending on traffic and maintenance, often once a year or less with good scrub-and-recoat maintenance."),
  ("Can stripping damage VCT?", "Overly strong stripper, too much water or aggressive pads can damage tiles and seams."),
  ("How long does a VCT strip and refinish take?", "Usually overnight or a day for a typical area, including drying time between coats.")]),
"VCT scrub and recoat": T(
 "VCT scrub and recoat deep-scrubs the worn top layers of floor finish on vinyl composition tile and applies fresh coats of finish, without stripping the floor down to bare tile.",
 "Scrub and recoat restores appearance at a fraction of the cost, chemicals and downtime of a full strip, and keeps the finish from wearing through to the tile.",
 "Crews scrub with a pad and cleaner that remove only the top coats, rinse, let the floor dry and apply two or more fresh coats.",
 ["Area and traffic level", "Condition of existing finish", "Compatible finish product", "Downtime available"],
 ["Too many recoats without stripping build up and yellow the finish.", "Edges and corners need hand detailing."],
 [("What is scrub and recoat on a VCT floor?", "Scrubbing off the worn top layers of finish and applying new coats without stripping to bare tile."),
  ("Is scrub and recoat cheaper than stripping?", "Usually yes, with less chemical use and less downtime."),
  ("When is a full strip needed instead?", "When the finish is worn through, heavily built up, yellowed or damaged."),
  ("How often is scrub and recoat done?", "In busy areas, often a few times a year between annual strips.")]),
}
