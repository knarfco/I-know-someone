def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Pre-health inspection clean": dict(a=
 "A pre-health inspection clean prepares restaurants, grocery departments, school cafeterias and other food facilities for the health department's opening inspection, focusing on overhead areas, equipment, handwash sinks, drains and food-contact surfaces."),
"Pre-fire marshal inspection clean": T(
 "A pre-fire marshal inspection clean prepares a building for the fire inspection by clearing exits and stairwells, making fire devices and equipment visible and accessible, and removing combustible debris and stored materials.",
 "Fire inspectors check that people can get out and firefighters can get in and operate equipment. Blocked exits, stored materials in riser rooms and debris near electrical equipment are common findings.",
 "Crews walk the building with the GC, clear egress paths and equipment rooms, clean fire extinguisher cabinets, alarm devices and exit signs, and remove combustible waste.",
 ["Inspection date", "Exit routes and stairwells", "Riser, pump and electrical rooms", "Fire extinguisher cabinets and exit signs"],
 ["Never move, cover or disconnect fire protection equipment.", "Storage in egress paths or equipment rooms is a common violation."],
 [("What does the fire marshal check at a new building?", "Clear exits and stairs, accessible fire equipment, working exit signs and alarms, proper storage and no combustible debris near equipment."),
  ("Are fire extinguisher cabinets cleaned before inspection?", "Yes, cabinets and glass are cleaned so extinguishers and tags are clearly visible, without moving or tampering with the extinguisher."),
  ("Why must combustible debris be removed before a fire inspection?", "Accumulated paper, cardboard and wood is fuel. Inspectors flag it, especially near electrical rooms and exits."),
  ("Can materials be stored in a sprinkler riser room?", "No. Riser and pump rooms must stay clear so firefighters can reach valves immediately.")]),
"Owner move-in clean": T(
 "An owner move-in clean is a final pass right before the owner or tenant moves in, cleaning up after furniture, equipment and IT installers so the space is ready on move-in day.",
 "Furniture, equipment and IT installers often work after the final clean and leave packaging, dust and debris behind. The owner's first day in the building shapes how they judge the whole project.",
 "Crews follow behind installers, remove packaging, vacuum and wipe new furniture, re-clean floors and glass, and check restrooms and break rooms.",
 ["Move-in date", "Installers working after the final clean", "Areas to re-clean", "Packaging volume"],
 ["Installers still working on move-in day will re-soil areas.", "Furniture and equipment must not be moved without the owner's direction."],
 [("What is an owner move-in clean?", "A final clean right before occupants arrive, done after furniture, equipment and IT installation. It removes the dust and packaging those installers leave."),
  ("Why is a building cleaned again before move-in?", "Installers who work after the final clean create new dust and debris, so a second pass is needed before people arrive."),
  ("Is packaging from furniture removed during the move-in clean?", "Yes, packaging is removed and recycled where possible, and the areas are vacuumed and wiped."),
  ("Who arranges the move-in clean?", "Usually the owner, tenant or GC, depending on who controls the furniture and equipment installation.")]),
"Tenant improvement final clean": T(
 "A tenant improvement final clean is the final clean of an interior build-out for a specific tenant, such as an office suite, retail space or medical suite, before the tenant moves in.",
 "TI projects often happen inside occupied buildings with rules about hours, elevators and common areas. The tenant and landlord both inspect the result.",
 "Crews clean the suite top down, clean any common corridors and elevator routes affected by the work and follow building rules for hours, access and protection.",
 ["Suite size and finishes", "Building rules: hours, elevator use, loading dock", "Common areas affected", "Tenant move-in date"],
 ["Building managers may limit noise and cleaning hours.", "Dust from the suite can spread to common corridors."],
 [("What is a tenant improvement project?", "An interior build-out of a leased space for a specific tenant, often shortened to TI."),
  ("Are common areas cleaned after a TI project?", "Common corridors, elevators and restrooms used by the construction crew should be cleaned so the landlord accepts them."),
  ("Do office buildings restrict cleaning hours for TI work?", "Many do, especially for noisy work or deliveries, so cleaning is often done after hours."),
  ("Who inspects a TI final clean?", "The tenant, the landlord's property manager and the GC usually walk the space together.")]),
"Phased occupancy cleaning": T(
 "Phased occupancy cleaning cleans and hands over parts of a building in stages, so finished areas can be occupied while construction continues elsewhere, and keeps occupied areas clean during the remaining work.",
 "Hospitals, schools, offices and retail centers often open in phases. Occupied areas need to stay clean even while dust and debris are being created next door.",
 "Crews final-clean each phase before handover, install protection at the boundaries, and provide recurring cleaning along shared paths until construction ends.",
 ["Phase boundaries and dates", "Shared corridors and entrances", "Protection and barriers", "Recurring cleaning schedule"],
 ["Dust migrates through doors, ceilings and HVAC into occupied areas.", "Shared paths need frequent cleaning while construction traffic continues."],
 [("What is phased occupancy in construction?", "Opening a building in stages, so some areas are used while others are still under construction."),
  ("How are occupied areas protected during phased construction?", "With barriers, closed doors, walk-off mats, negative air where needed and frequent cleaning of shared paths."),
  ("Who plans phased occupancy?", "The owner and GC, often with the architect and building officials."),
  ("Does phased occupancy need extra cleaning?", "Yes, both a final clean of each phase and ongoing cleaning of areas that construction traffic passes through.")]),
"Post-furniture install clean": T(
 "A post-furniture install clean removes packaging, cardboard, plastic wrap, dust and debris left after furniture installers finish, and cleans the new furniture and the floors around it.",
 "Furniture installation creates large volumes of packaging and leaves dust, fingerprints and scuffs. It often happens after the final clean, right before move-in.",
 "Crews remove packaging, vacuum upholstery, wipe work surfaces and storage, clean floors and check for scuffs on walls and floors caused by installation.",
 ["Furniture installation schedule", "Packaging volume and recycling", "Furniture types and finishes", "Floor and wall touch-ups"],
 ["Do not rearrange furniture placed per the plan.", "Report scuffs and damage instead of hiding them."],
 [("Why clean after furniture installation?", "Installers leave packaging, dust and scuffs, and they usually work after the final clean."),
  ("Is new furniture cleaned before occupants arrive?", "Yes, work surfaces and storage are wiped and upholstery vacuumed."),
  ("Who removes furniture packaging?", "Furniture installers sometimes take it; otherwise the cleaning crew removes and recycles it."),
  ("When should the post-furniture clean happen?", "Right after installation and before occupants move in.")]),
}
