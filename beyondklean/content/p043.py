def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Concrete floor auto-scrubbing": dict(q=[
  ("What is an auto-scrubber?", "A walk-behind or ride-on floor machine that lays down cleaning solution, scrubs with pads or brushes and vacuums the dirty water back up in a single pass."),
  ("Is auto-scrubbing better than mopping a concrete floor?", "On large floors, yes. It cleans more thoroughly, recovers the dirty water instead of spreading it, and leaves the floor dry and safe much faster."),
  ("What pad should be used to scrub new concrete?", "It depends on the finish: more aggressive pads or brushes for raw slabs, softer pads for sealed or polished concrete to avoid scratching."),
  ("Where does auto-scrubber wastewater go?", "To a sanitary drain where the facility and local rules allow, never to a storm drain or the parking lot.")]),
"Warehouse floor scrubbing": dict(
 w=["Wet floors are slippery for forklifts and pedestrians; scrub in controlled lanes.", "Racking and stored product reduce machine access and need protection from splash."],
 q=[("How are warehouse floors cleaned after construction?", "Dry debris is swept or vacuumed first, then ride-on scrubbers clean the slab in planned lanes with marks and stains treated separately."),
  ("Should a warehouse floor be scrubbed before racking is installed?", "Yes. An empty slab is far faster to clean, and racking installers need a clean floor to lay out and anchor racks."),
  ("How often are warehouse floors scrubbed during operations?", "It varies with traffic, from daily in busy distribution centers to weekly in low-traffic storage."),
  ("Do forklift tire marks come off warehouse floors?", "Usually, with the right cleaner and pad. Non-marking tires reduce new marks.")]),
"Sealed concrete floor cleaning": dict(q=[
  ("How is sealed concrete cleaned without damaging the sealer?", "With a pH-neutral cleaner and soft pads, recovering the water with an auto-scrubber or wet vacuum."),
  ("Can cleaning remove concrete sealer?", "Strong alkaline cleaners, solvents and aggressive pads can dull or strip many sealers, so gentle methods are used."),
  ("How can you tell if a concrete floor is sealed?", "Water usually beads on a sealed floor and soaks into an unsealed one. The GC or flooring schedule confirms it."),
  ("How often does sealed concrete need resealing?", "It depends on traffic and the sealer type, often every one to three years in commercial spaces.")]),
"Polished concrete maintenance clean": dict(q=[
  ("How do you clean polished concrete floors?", "Remove grit with a dust mop or vacuum first, then auto-scrub with a pH-neutral cleaner and the maintenance pads the polishing contractor recommends."),
  ("Why does polished concrete look dull after cleaning?", "Usually from cleaner residue, the wrong pads or acidic products. Neutral cleaners and proper rinsing restore the shine."),
  ("Can polished concrete be waxed?", "Polished concrete is normally not waxed. Its shine comes from mechanical polishing and is maintained with pads and cleaners."),
  ("Do acidic cleaners damage polished concrete?", "Yes, acids etch the surface and leave dull spots that need re-polishing.")]),
"Concrete polishing": dict(q=[
  ("Is concrete polishing a cleaning service?", "No. It is a flooring specialty that grinds and polishes the slab with heavy equipment. Cleaning contractors maintain polished concrete afterward."),
  ("What is concrete densifier?", "A liquid chemical, often silicate-based, that reacts with concrete to harden the surface during polishing."),
  ("Does concrete polishing create silica dust?", "Yes. Grinders need dust collection with HEPA filtration or wet methods to comply with OSHA's silica rules."),
  ("When is concrete polished during construction?", "Often early, before walls go up, or late with heavy protection, depending on the project's sequencing.")]),
}
