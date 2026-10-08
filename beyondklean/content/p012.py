def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Final clean by phase or floor": dict(
 w=["Trades working in adjacent phases will re-soil finished areas unless access is controlled.", "Each extra mobilization adds cost, so agree on phase pricing before work starts."],
 q=[("Why do a final clean in phases instead of all at once?", "Large buildings and phased occupancies finish one area at a time. Cleaning each area as it is released lets it be inspected, handed over or occupied without waiting for the whole building."),
  ("How is a finished phase kept clean while work continues next door?", "With floor protection, closed doors or barriers, walk-off mats and controlled access, plus a scheduled touch-up right before handover."),
  ("Does a phased final clean cost more?", "Often somewhat more, because crews mobilize several times and some touch-up is repeated. It is usually offset by earlier occupancy and fewer delays."),
  ("Who decides the phases for final cleaning?", "The GC and owner set them based on the occupancy plan, inspections and the construction schedule.")]),
"Light clean (phase 2)": dict(q=[
  ("What is a light clean in construction?", "The light clean, also called the phase 2 or detail clean, is the middle cleaning phase. It removes dust from surfaces, fixtures and glass after most finishes are installed and before the final clean."),
  ("Does every construction project need a light clean?", "No. Small projects often skip it and go from rough clean to final clean. Larger projects use it to keep finishes protected and make the final clean faster."),
  ("What is cleaned during the light clean?", "Surfaces, cabinets, fixtures, window frames and glass get a first detail pass. Floors are often still protected, and final detailing waits for the last phase."),
  ("When does the light clean happen?", "After drywall, paint, cabinets and most fixtures are in, but before final trim-out and punch work are complete.")]),
"Touch-up clean before owner walk": dict(q=[
  ("What is a touch-up clean before the owner walk?", "A fast, focused pass right before the owner or architect inspection. It re-cleans glass, fixtures, floors and anything that got dirty since the final clean."),
  ("When should the touch-up clean be scheduled?", "The day before or the morning of the owner walk, after the last trades have left the inspected areas."),
  ("What areas get the most attention in a touch-up?", "Entries, glass, restroom fixtures, floors along the walk route, and anything an inspector will touch or open."),
  ("Is touch-up cleaning included in the final clean price?", "Usually not. It is often priced as a separate item or allowance, so it should be agreed in the cleaning contract.")]),
"Punch-list cleaning": T(
 "Punch-list cleaning works through the cleaning items recorded on the architect's or owner's punch list, such as smudges, labels, residue, dust and missed areas, and documents each item as complete so the list can close.",
 "Projects cannot reach final completion and release retainage until punch items are closed. Cleaning items are often the most numerous and the easiest to close quickly when someone owns them.",
 "Crews sort the punch list by room, complete cleaning items in a single organized pass, photograph completed items when required, and return the list to the GC with items marked off.",
 ["Punch list format and owner", "Rooms and item count", "Documentation requirements", "Deadline for closeout"],
 ["Some items listed as cleaning are actually damage that needs the responsible trade.", "Items must be documented; verbal completion is not enough."],
 [("What is a punch list in construction?", "A list of incomplete or defective items recorded during the pre-completion walk. All items must be fixed before final completion."),
  ("What cleaning items are typically on a punch list?", "Fingerprints, labels, paint and caulk smears, dust on fixtures, dirty glass and missed areas inside cabinets or behind fixtures."),
  ("How are punch-list cleaning items closed out?", "By completing each item, marking it on the list and often photographing it, then returning the list to the GC for verification."),
  ("Who assigns punch list items to the cleaning crew?", "The GC reviews the list and assigns cleaning items to the cleaning contractor and other items to the responsible trades.")]),
"Pre-certificate of occupancy clean": T(
 "A pre-certificate of occupancy clean prepares a building for the building official's final inspection: clearing exits, cleaning fire and life-safety equipment, opening access to equipment rooms and making inspected areas presentable.",
 "The certificate of occupancy inspection focuses on life safety. Blocked exits, debris in equipment rooms and dirty or covered devices can delay the certificate, which delays move-in and often payment.",
 "Crews walk the inspection route with the GC, clear exits and stairs, clean equipment rooms, make sure fire devices are visible and finish with a general clean of public areas.",
 ["Inspection date and route", "Exits, stairs and corridors", "Fire and life-safety devices", "Equipment rooms"],
 ["Some labels, such as energy labels, may need to remain until the inspector sees them.", "Never cover or block fire devices while cleaning."],
 [("What is a certificate of occupancy?", "The document from the local building authority that allows a building or space to be legally occupied. It follows a final inspection."),
  ("Can a dirty building fail a certificate of occupancy inspection?", "Debris in exits, blocked equipment and obstructed fire devices can cause failures or delays, even when construction is complete."),
  ("What should be cleaned before the CO inspection?", "Exit routes, stairs, equipment rooms, fire and life-safety devices, and the public areas on the inspection route."),
  ("Who schedules the certificate of occupancy inspection?", "The GC schedules it with the building department once the project is ready.")]),
}
