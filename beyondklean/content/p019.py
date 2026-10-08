def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Elevator cab protection install and removal": dict(q=[
  ("Why are elevator cabs protected during construction?", "Construction traffic, carts and materials scratch and dent cab finishes quickly. Pads and floor protection keep the cab presentable for turnover."),
  ("Who approves elevator cab protection?", "The elevator contractor or GC, since pads must not interfere with doors, sensors or the cab's operation."),
  ("When is elevator cab protection removed?", "Near the end of construction, after heavy deliveries and furniture moves are complete. The cab is detailed right after removal."),
  ("What happens if the cab is damaged under the pads?", "Damage is documented and reported to the GC so the responsible party can arrange repair by a finish specialist.")]),
"Door and frame protection removal": T(
 "Door and frame protection removal takes off temporary corner guards, film, cardboard and tape that protected doors and frames during construction, and cleans the residue left behind.",
 "Door protection prevents dents and scratches during construction, but the tape and film often stay on too long and leave residue or pull paint.",
 "Crews remove protection slowly at a low angle, clean adhesive with finish-safe removers and touch up the door and frame faces.",
 ["Number of doors and frames protected", "Protection type and tape", "Door and frame finishes", "Paint cure status"],
 ["Pulling tape quickly can lift fresh paint from frames.", "Adhesive left on wood doors can damage the finish if removed with solvents."],
 [("Why are doors protected during construction?", "Doors and frames are installed early and are easily dented and scratched by carts and materials."),
  ("Does door protection leave residue?", "Often, especially tape left on for weeks. Residue is removed with finish-safe products."),
  ("When is door protection removed?", "At final clean, after heavy traffic and deliveries are finished in that area."),
  ("Who removes door protection?", "The cleaning crew or the trade that installed it, depending on the contract.")]),
"Countertop and fixture protection removal": T(
 "Countertop and fixture protection removal takes protective coverings off counters, vanities, sinks, tubs and fixtures, and cleans the dust and residue trapped underneath.",
 "Counters and fixtures are protected because they are installed before painting and trim work finishes. Debris trapped under protection can scratch them when it is removed.",
 "Crews lift protection carefully instead of dragging it, vacuum trapped debris, remove adhesive and clean the surface with material-specific products.",
 ["Counters, sinks and fixtures protected", "Protection type", "Surface materials", "Residue"],
 ["Dragging protection drags debris across stone and quartz.", "Tape residue on stone needs stone-safe removers."],
 [("Why protect countertops during construction?", "They are installed before painting and trim work, so they are exposed to tools, paint and debris."),
  ("How is debris under countertop protection handled?", "Protection is lifted, not dragged, and debris is vacuumed off before the surface is wiped."),
  ("Can tape residue damage stone countertops?", "The residue itself rarely damages stone, but harsh removers can, so stone-safe products are used."),
  ("When is fixture protection removed?", "During the final clean, after trades finish in the room.")]),
"Carpet protection film removal": T(
 "Carpet protection film removal peels the adhesive plastic film laid over new carpet during construction and vacuums the carpet afterward.",
 "Carpet film protects new carpet from foot traffic and spills, but left too long or exposed to heat, its adhesive can leave residue and crush or distort the pile.",
 "Crews peel film slowly in the direction of the pile, remove any residue with carpet-safe spotters and HEPA vacuum the carpet to lift the pile.",
 ["Carpet area under film", "How long film has been down", "Residue", "Vacuuming after removal"],
 ["Film left down for weeks can leave adhesive residue in the pile.", "Pulling film too fast can distort carpet fibers."],
 [("How long can carpet protection film stay down?", "Manufacturers usually recommend limited periods, often a few weeks. Longer exposure, heat and sun increase the risk of residue."),
  ("Does carpet protection film leave residue?", "It can, especially after long periods or in heat. Carpet-safe spotters remove most residue."),
  ("Is carpet vacuumed after the film is removed?", "Yes, vacuuming lifts the pile and removes dust that got under the film edges."),
  ("Who removes carpet protection film?", "The cleaning crew during the final clean.")]),
"Temporary walk-off mat placement and removal": T(
 "Temporary walk-off mat placement and removal places heavy-duty mats at entrances and transitions during construction to trap dirt before it reaches finished floors, keeps them clean, and removes them at the end.",
 "Most dirt on a building's floors comes in on shoes and wheels. Mats at entrances and between dirty and clean areas protect finishes and reduce cleaning time.",
 "Crews place mats at entrances and transitions, vacuum or replace them when they are saturated, and remove and clean under them before the final clean.",
 ["Entrance and transition locations", "Mat type and size", "Cleaning and replacement schedule", "Removal timing"],
 ["Curled or wrinkled mats are trip hazards.", "Saturated mats stop working and start spreading dirt."],
 [("Why use temporary walk-off mats during construction?", "They trap dirt and moisture from shoes and wheels before it reaches finished floors."),
  ("How often should construction walk-off mats be cleaned?", "Whenever they look saturated, often daily at busy entrances, and replaced when they stop trapping dirt."),
  ("Are walk-off mats a trip hazard?", "They can be if curled or wrinkled, so they need to lie flat and be secured."),
  ("When are temporary mats removed?", "Just before the final clean, with the floor underneath cleaned right away.")]),
}
