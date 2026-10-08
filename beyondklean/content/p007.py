def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Water damage cleanup": dict(q=[
  ("What should be done first after water damage on a jobsite?", "Stop the water source, make the area electrically safe and photograph the damage. Then get a qualified restoration contractor drying the structure quickly, because wet materials start growing mold within days."),
  ("How quickly can mold grow after water damage?", "Mold can begin growing on wet drywall, wood and insulation within roughly 24 to 48 hours in warm conditions. That is why fast extraction and monitored drying matter so much."),
  ("Who handles water damage restoration on a construction project?", "A restoration contractor trained in water damage drying. They extract water, set dehumidifiers and air movers, and track moisture readings until materials are dry."),
  ("Does water damage on a new building need insurance documentation?", "Usually yes. Photos, moisture readings and drying logs support builder's risk or property insurance claims and protect the owner's warranty position.")]),
"Mold remediation": dict(q=[
  ("Can a regular cleaning company remove mold?", "Very small surface spots may be cleaned in some situations, but anything larger should go to a qualified remediation contractor. Disturbing mold without containment spreads spores through the building."),
  ("Does Florida license mold remediation?", "Yes. Florida licenses mold assessors and mold remediators under state law, with limited exemptions, so remediation there should be done by a properly licensed provider."),
  ("What is clearance testing after mold remediation?", "An independent assessment after remediation to confirm the area is acceptable before reconstruction or occupancy. It is often required by owners, lenders or insurers."),
  ("Why must the moisture source be fixed before mold remediation?", "Mold needs moisture to grow. If the leak or humidity problem continues, mold comes back no matter how well the area was cleaned.")]),
"Fire and smoke residue cleaning": T(
 "Fire and smoke residue cleaning removes soot, smoke film and odor from building surfaces and contents after a fire, using restoration methods matched to the type of residue. It is specialty restoration work.",
 "Soot is acidic and oily and can permanently stain finishes if it is wiped incorrectly. Smoke odor penetrates porous materials and HVAC systems and returns unless it is treated at the source.",
 "Requests are reviewed and routed only to qualified fire restoration contractors, who test residue types, use dry sponges and specialty cleaners, and treat odor with methods such as thermal fogging or hydroxyl generators.",
 ["Extent of fire and smoke damage", "Residue type: dry, wet or protein", "Odor treatment needs", "Insurance adjuster coordination"],
 ["Wiping soot with water or the wrong cleaner smears it deeper into surfaces.", "HVAC systems can spread smoke odor and residue unless they are cleaned too."],
 [("Who cleans up after a fire in a building?", "Fire restoration contractors trained to identify soot types and use the right removal and deodorizing methods. Cleaning crews without that training can make stains permanent."),
  ("Is soot harmful to people?", "Soot contains fine particles and combustion byproducts that can irritate lungs and skin. Cleanup crews use respiratory protection and containment."),
  ("Can smoke odor be removed completely?", "Usually, when residue is removed and odor is treated at the source, including HVAC systems. Odor that persists often means residue was missed."),
  ("Is fire restoration covered by insurance?", "Often, under builder's risk or property insurance. Restoration contractors typically document the work for the adjuster.")]),
"Asbestos abatement": T(
 "Asbestos abatement is the removal, encapsulation or enclosure of asbestos-containing materials by licensed abatement contractors under federal, state and local regulations, usually during renovation or demolition of older buildings.",
 "Disturbing asbestos releases fibers that cause serious lung disease. Federal rules require inspection before renovation or demolition of many buildings, notifications and licensed workers for removal.",
 "This work is never routed to cleaning crews. Requests go only to licensed abatement contractors after review, and cleaning crews stop work immediately if suspect material is found.",
 ["Asbestos survey results", "Licensing and notification requirements", "Containment and air monitoring", "Clearance testing"],
 ["Stop work and isolate the area if suspect material is found during cleaning.", "Notifications to regulators may be required before work starts."],
 [("What should a crew do if they find possible asbestos during construction cleaning?", "Stop work in that area, keep people out and notify the GC. Only an inspection and, if needed, a licensed abatement contractor should handle it."),
  ("Is asbestos still found in commercial buildings?", "Yes, in many buildings built before the 1980s, in flooring, mastic, pipe insulation, fireproofing and ceiling materials."),
  ("Can a cleaning company remove asbestos?", "No. Asbestos removal requires licensed abatement contractors, trained workers, containment and air monitoring."),
  ("Is clearance testing required after asbestos abatement?", "Clearance air testing is commonly required before the area can be reoccupied, depending on the project and jurisdiction.")]),
"Lead paint abatement": T(
 "Lead paint abatement permanently removes or controls lead-based paint hazards using certified contractors and lead-safe work practices under EPA and OSHA rules, followed by cleaning and clearance testing.",
 "Lead dust from sanding, scraping or demolition of old paint is toxic, especially to children. Renovation in older buildings can create lead hazards that ordinary cleaning spreads instead of removing.",
 "Requests are routed only to certified lead contractors after review. Cleanup uses HEPA vacuums and wet wiping in a specific sequence, followed by verification or clearance.",
 ["Lead testing results", "Certification requirements", "Work practices and containment", "Clearance or cleaning verification"],
 ["Dry sweeping and ordinary vacuums spread lead dust.", "Child-occupied facilities have stricter rules."],
 [("Who can remove lead paint from a building?", "EPA-certified renovators for renovation work and certified abatement contractors for abatement. Requirements depend on the building and type of work."),
  ("Why is lead dust dangerous?", "Lead is toxic, and fine dust from old paint is easily ingested or inhaled. Children are especially vulnerable."),
  ("How is lead dust cleaned up after renovation?", "With HEPA vacuuming and wet wiping in a defined sequence, followed by cleaning verification or clearance testing."),
  ("Which buildings may have lead paint?", "Many buildings built before 1978 may contain lead-based paint, which should be tested before renovation.")]),
}
