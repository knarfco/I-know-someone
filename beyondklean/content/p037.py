def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Air handler exterior cleaning": dict(q=[
  ("Is air handler exterior cleaning the same as cleaning the inside?", "No. Exterior cleaning covers only the outer casing and access doors. Coils, drain pans and internal sections are cleaned by mechanical or HVAC hygiene specialists."),
  ("Why clean the outside of a new air handler?", "Dust on the casing is pulled inside whenever access doors are opened for service, and a dusty unit looks neglected at turnover."),
  ("When should air handler exteriors be cleaned?", "Near the end of construction, after dusty work in that area is finished and before filters are changed for occupancy."),
  ("Do air handler labels need to stay on during cleaning?", "Yes. Nameplates, electrical warnings and service labels must remain in place and readable.")]),
"Air handler interior cleaning": dict(q=[
  ("When does a new air handler need internal cleaning?", "When construction dust or debris got inside, usually because the unit ran without proper filtration or was left open during dusty work."),
  ("Who cleans the inside of air handlers?", "Qualified HVAC cleaning contractors, coordinated with the mechanical contractor so warranties and settings are protected."),
  ("Can coil cleaning damage HVAC equipment?", "Yes. Excessive pressure bends coil fins and the wrong chemicals corrode them, which is why this is specialist work."),
  ("Is air handler interior cleaning documented?", "It should be, with before-and-after photos and a written report for the owner's records.")]),
"HVAC duct interior cleaning": dict(q=[
  ("Do new buildings need duct cleaning?", "Only when ducts were contaminated during construction, for example when ends were left uncapped or the system ran without filters. Well-protected systems usually do not."),
  ("What is NADCA?", "The National Air Duct Cleaners Association, which publishes standards for assessing, cleaning and restoring HVAC systems."),
  ("How can duct contamination be prevented during construction?", "By capping open duct ends, storing ductwork clean and covered, and not running the HVAC without temporary filtration."),
  ("Who verifies that duct cleaning was done properly?", "The duct contractor documents the work with photos, and some owners hire independent inspectors to verify cleanliness.")]),
"Rooftop unit exterior and curb cleaning": dict(q=[
  ("Why clean around rooftop HVAC units after construction?", "Debris left on the roof can be pulled into unit intakes, block condensate drains or puncture the roof membrane around the curb."),
  ("Who cleans rooftop unit coils?", "The mechanical contractor or HVAC service company. Cleaning crews only clean cabinet exteriors and the area around the unit."),
  ("Is cleaning on a roof dangerous?", "It can be. Crews need roof access plans, fall protection near edges and care around skylights and openings."),
  ("Can cleaning crews walk anywhere on the roof?", "Only on approved paths or walk pads, so the roof membrane is not damaged.")]),
"Generator and switchgear exterior cleaning": dict(
 w=["Generators can start automatically during a power event, so lockout is essential.", "Arc-flash boundaries around switchgear must be respected at all times."],
 q=[("Can a cleaning crew clean an emergency generator?", "Only the exterior enclosure and surrounding area, with the responsible trade's approval and the generator locked out against automatic start."),
  ("Why is switchgear cleaning treated as conditional work?", "Switchgear is energized, high-voltage equipment with arc-flash hazards, so only work approved by the electrical contractor is allowed."),
  ("Who cleans inside switchgear?", "Qualified electrical workers during de-energized maintenance. It is never part of construction cleaning."),
  ("Why are generators dangerous to clean around?", "They can start automatically when utility power drops, so lockout and coordination are required before anyone approaches.")]),
}
