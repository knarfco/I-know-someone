def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Dish area and dish machine exterior cleaning": dict(
 a="Dish area and dish machine exterior cleaning cleans dish tables, pre-rinse sinks, dish machine exteriors, racks, walls and floors in the dish room, and clears construction debris from floor drains before the dish machine is started.",
 w=["Do not run or open the dish machine until the vendor completes startup.", "Construction debris in dish room drains causes immediate backups."],
 q=[("Who starts up a new dish machine?", "The dish machine vendor or chemical service company, who also sets chemical dispensers and temperatures."),
  ("Is the dish machine interior cleaned at turnover?", "Usually the vendor handles interior cleaning and setup at startup. Crews clean exteriors and the surrounding area."),
  ("Why are dish area drains cleaned before opening?", "Grout, mortar and debris from construction collect in floor drains and cause backups when the dish room starts running."),
  ("Is the dish area part of the kitchen turnover clean?", "Yes, dish tables, sinks, walls, floors and drains are all included.")]),
"Grease trap area cleaning": dict(
 a="Grease trap area cleaning cleans around grease interceptors and under-sink grease traps, including lids, access covers and surrounding floors, and reports construction debris inside them. Pumping and interior servicing are done by licensed grease haulers.",
 q=[("Who pumps and services grease traps?", "Licensed grease haulers or plumbers pump interceptors and service traps, following local wastewater rules."),
  ("Why clean the grease trap area before a restaurant opens?", "Inspectors check that traps are accessible and clean, and construction debris in a trap can cause clogs from the first day."),
  ("Can construction debris end up in grease traps?", "Yes. Grout, mortar and debris washed down kitchen drains collect in traps and interceptors."),
  ("Are grease traps inspected before opening?", "Often. Many local wastewater authorities inspect grease interceptors before or soon after opening.")]),
"Bar and beverage station cleaning": dict(
 a="Bar and beverage station cleaning cleans bar tops, back bars, bar sinks, under-bar equipment, beverage dispensers, glass racks and shelving before a restaurant or bar opens, with food-safe products and finish-appropriate methods.",
 q=[("Who cleans beverage lines in a new bar?", "The beverage vendor or a line cleaning service cleans and sanitizes draft and soda lines during setup."),
  ("How are bar tops cleaned after construction?", "With cleaners matched to the material, such as stone-safe products for granite or wood-safe products for wood bar tops."),
  ("Is the back bar cleaned before opening?", "Yes. Back bar shelving, mirrors and lighting are cleaned before bottles and glassware are set."),
  ("Are bar surfaces sanitized before opening?", "Food-contact surfaces are cleaned and then sanitized with registered products before service begins.")]),
"Ice machine exterior cleaning": T(
 "Ice machine exterior cleaning cleans the outside of ice machines and bins, including cabinet panels, vent grilles, bin doors and the surrounding floor and wall, before the machine is started.",
 "Construction dust drawn into ice machine vents affects condenser performance, and dirty exteriors near ice are noticed by inspectors.",
 "Crews wipe cabinets and bin exteriors with food-safe cleaners and vacuum vent grilles, leaving interior cleaning and sanitizing to service technicians.",
 ["Number of machines and bins", "Vent grille locations", "Service technician schedule", "Floor and wall around the unit"],
 ["Interior cleaning requires the manufacturer's procedure and approved chemicals.", "Blocking or bending vent grilles reduces airflow."],
 [("Who cleans the inside of a new ice machine?", "Service technicians, using the manufacturer's procedure and approved chemicals."),
  ("Why clean ice machine vent grilles?", "Dust drawn into the vents coats the condenser and reduces ice production and efficiency."),
  ("Is the ice bin exterior cleaned?", "Yes, bin doors and exteriors are cleaned with food-safe products."),
  ("Do health inspectors check ice machines?", "Yes, ice is food, and inspectors check machines and bins for cleanliness.")]),
"Ice machine interior cleaning and sanitizing": dict(
 a="Ice machine interior cleaning and sanitizing descales and sanitizes the inside of ice machines and bins using the manufacturer's procedure and approved chemicals, before first use and on a regular schedule after.",
 m="Requests are routed only to qualified service technicians after review, who follow the model's cleaning cycle and document the service.",
 w=["Using the wrong chemicals can damage the machine and void the warranty.", "Procedures differ by model; the manufacturer's manual controls."],
 q=[("How often should an ice machine be cleaned and sanitized?", "According to the manufacturer, commonly about every six months, and more often in dusty or high-yeast environments like bakeries and breweries."),
  ("Who cleans the inside of ice machines?", "Qualified service technicians following the manufacturer's procedure."),
  ("Why is ice machine sanitizing important?", "Ice is food, and dirty machines can grow slime, mold and bacteria that contaminate drinks."),
  ("Does a new ice machine need sanitizing before use?", "Yes, manufacturers typically call for cleaning and sanitizing before the first batch of ice is used.")]),
}
