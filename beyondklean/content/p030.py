def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Stainless steel equipment exterior cleaning": dict(
 a="Stainless steel equipment exterior cleaning removes construction dust, fingerprints, adhesive, water spots and streaks from the outside of ranges, prep tables, refrigeration, sinks, hoods and other stainless kitchen equipment before opening.",
 q=[("How do you clean stainless steel equipment without streaks?", "Clean with a neutral or stainless-specific cleaner, rinse, dry with a clean cloth and finish by wiping in the direction of the grain."),
  ("Why does stainless steel sometimes rust?", "Chlorides from bleach or some cleaners, particles from steel wool and scratches in the surface can all cause rust spots on stainless."),
  ("Can bleach be used on stainless steel kitchen equipment?", "It should be avoided, because the chlorides in bleach can pit and stain stainless steel over time."),
  ("Does new stainless kitchen equipment need polish?", "Usually not at turnover. A clean, dry surface wiped with the grain looks right, and polish can leave residue on food areas.")]),
"Stainless steel protective film removal": dict(
 w=["Film near cooking equipment and windows bakes on quickly and leaves residue.", "Blades and abrasive pads scratch stainless and leave permanent marks."],
 q=[("When should protective film be removed from kitchen equipment?", "Before equipment is fired up or exposed to heat, as close to installation as practical. Heat bakes the adhesive on quickly."),
  ("How do you remove adhesive left by stainless steel film?", "With a stainless-safe adhesive remover and soft cloth, then a neutral cleaner, rinse and dry, wiping with the grain."),
  ("Why is old protective film so hard to remove?", "Heat, sunlight and time make the adhesive bond to the stainless, so it tears and leaves residue."),
  ("Who removes protective film from new kitchen equipment?", "The equipment installer or the cleaning crew, depending on the contract. It should be assigned clearly before startup.")]),
"Kitchen hood exterior cleaning": dict(q=[
  ("Is kitchen hood exterior cleaning the same as hood cleaning?", "No. Exterior cleaning covers the visible canopy and edges. Hood plenum and grease duct cleaning is regulated work under NFPA 96 done by certified contractors."),
  ("Can cleaning crews touch fire suppression nozzles in a kitchen hood?", "No. Suppression nozzles, links and piping are serviced only by licensed fire suppression contractors and must not be disturbed."),
  ("Should hood filters be cleaned before a restaurant opens?", "Filters should be clean and correctly installed before cooking starts. The hood contractor or kitchen staff usually handles them."),
  ("Why clean hood exteriors before opening?", "Hoods are the most visible equipment in the kitchen, and construction dust on them is noticed by inspectors and owners.")]),
"Kitchen exhaust hood and duct cleaning": dict(q=[
  ("Who is allowed to clean kitchen exhaust hoods and ducts?", "Certified hood cleaning contractors following NFPA 96 and local fire codes, who document the work with certificates and photos."),
  ("Does a new restaurant kitchen need hood cleaning before opening?", "New systems should be free of construction debris and dust before cooking begins. Inspection after installation confirms whether cleaning is needed."),
  ("What is NFPA 96?", "The fire code standard for ventilation control and fire protection of commercial cooking operations, including inspection and cleaning of exhaust systems."),
  ("How often are kitchen exhaust systems cleaned?", "It depends on cooking volume and type, from monthly for high-volume operations to annually for low-volume kitchens.")]),
"Walk-in cooler interior cleaning": dict(q=[
  ("When should a walk-in cooler be cleaned?", "Before it is started and stocked. Once the box is cold and full of product, a thorough cleaning becomes very difficult."),
  ("Can cleaning crews clean the evaporator coils in a walk-in?", "No. Coils, fans and refrigeration components are serviced by refrigeration technicians; crews clean only the housing exterior."),
  ("Why are walk-in door gaskets cleaned?", "Dirty or damaged gaskets keep the door from sealing, which wastes energy and lets moisture in. Damaged gaskets are reported for replacement."),
  ("What cleaners are used inside a walk-in cooler?", "Food-safe cleaners suitable for the panel finish, followed by rinsing and drying.")]),
}
