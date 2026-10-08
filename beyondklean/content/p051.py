def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Hardwood floor initial clean": dict(
 y="New wood floor finishes are sensitive to water and chemicals and need time to cure. Construction grit tracked across them scratches the finish before the owner ever moves in.",
 w=["Water and wet mops can cup and damage wood floors.", "Cleaning or covering before the finish cures can damage it."],
 q=[("How are new hardwood floors cleaned after construction?", "Dust mopped and vacuumed first, then cleaned with a wood floor cleaner and barely damp microfiber."),
  ("When can new hardwood floor finish be cleaned?", "After it cures according to the finish manufacturer, often days for light cleaning and longer for full cure."),
  ("Can hardwood floors be mopped?", "Only with a barely damp microfiber mop; standing water damages wood."),
  ("When can rugs go on newly finished wood floors?", "After the finish fully cures, which can take a few weeks for some finishes.")]),
"Engineered wood floor cleaning": dict(
 a="Engineered wood floor cleaning cleans engineered hardwood floors with methods and products that protect the factory finish and the thin real-wood wear layer.",
 m="Crews use dry methods first, then the manufacturer's recommended cleaner with barely damp microfiber, keeping water away from seams.",
 w=["Water at seams can swell the core and edges.", "Some cleaners leave residue that dulls the factory finish."],
 q=[("What is engineered wood flooring?", "Flooring with a real wood top layer bonded to plywood or fiberboard layers."),
  ("How is engineered wood cleaned?", "With dry methods and the manufacturer's recommended cleaner on barely damp microfiber."),
  ("Can engineered wood floors be refinished?", "Sometimes, depending on the thickness of the wear layer."),
  ("Is engineered wood sensitive to water?", "Yes, especially at seams and edges.")]),
"Gym and athletic hardwood floor cleaning": dict(
 m="Crews dust mop with treated or microfiber mops, then clean with approved gym floor cleaners and minimal moisture, keeping game lines and the finish intact.",
 w=["Wrong cleaners make gym floors slippery and dangerous.", "Water damages maple sport floors."],
 q=[("How are gym floors cleaned after construction?", "With dust mops and gym floor cleaners approved by the floor system manufacturer, using minimal moisture."),
  ("Can a gym floor be wet mopped?", "Only with minimal moisture from an approved system; standing water damages maple."),
  ("Why do gym floors become slippery?", "Residue from improper cleaners and dust on the surface reduce traction."),
  ("Who recoats a gym floor?", "Sport floor finishing contractors, usually during screen-and-recoat maintenance.")]),
"Bamboo and cork floor cleaning": dict(
 a="Bamboo and cork floor cleaning cleans these natural flooring materials with dry methods, low moisture and pH-neutral products recommended by the manufacturer.",
 y="Bamboo and cork are sensitive to water and harsh chemicals. Water can swell cork and bamboo, and strong cleaners damage their finishes.",
 w=["Excess water can swell cork and bamboo.", "Harsh or oily cleaners damage finishes."],
 q=[("How is cork flooring cleaned?", "With dust mopping and barely damp microfiber using a neutral cleaner the manufacturer recommends."),
  ("Is bamboo flooring cleaned like hardwood?", "Mostly yes, with dry methods and minimal moisture."),
  ("Can cork floors get wet?", "Moisture should be limited, because cork can swell and its finish can be damaged."),
  ("Do cork floors need to be sealed?", "Many cork floors are factory-finished or site-sealed; follow the manufacturer.")]),
"Raised access floor cleaning": dict(
 y="Dust on and under raised access floors is distributed through cooling air into equipment, which affects reliability in data centers and control rooms.",
 w=["Removing too many panels at once weakens the grid.", "Cabling under the floor must not be disturbed."],
 q=[("What is a raised access floor?", "A floor of removable panels on pedestals, creating a plenum for cables and air."),
  ("Why clean raised access floors after construction?", "Dust on and under the floor is distributed by cooling air into equipment."),
  ("Who cleans raised access floors?", "Trained critical-environment crews with HEPA and antistatic methods."),
  ("How are raised floor panels lifted for cleaning?", "With suction-cup panel lifters, a few panels at a time.")]),
}
