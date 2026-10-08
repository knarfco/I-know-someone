def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Fire pump and riser room cleaning": dict(q=[
  ("What is a sprinkler riser room?", "The room where the fire sprinkler system's main control valves, alarms and gauges are located, usually on the ground floor with exterior access."),
  ("Do fire inspectors check riser and pump rooms?", "Yes. They check access, clearance, labeling, signage and condition, and stored materials are a common violation."),
  ("Can cleaning crews touch sprinkler valves?", "No. Valves, gauges and controls are operated only by fire protection contractors or authorized staff."),
  ("Why must riser rooms be kept clear?", "Firefighters need immediate, unobstructed access to valves during an emergency.")]),
"Telecom and IDF/MDF room cleaning": dict(
 a="Telecom and IDF/MDF room cleaning cleans network, telecom and low-voltage rooms before and after equipment is installed, removing dust, cable scraps and packaging with HEPA and antistatic methods and with IT approval.",
 q=[("What is an IDF room?", "An intermediate distribution frame room, usually one per floor, where network cabling from that floor connects to building network equipment."),
  ("What is an MDF room?", "The main distribution frame room, where the building's main network and telecom connections come in and connect to each floor."),
  ("Why clean telecom rooms after construction?", "Dust is drawn into network switches and servers by their cooling fans, which shortens equipment life."),
  ("Who approves cleaning in telecom rooms?", "The IT team or the low-voltage contractor, who sets the rules for access and methods.")]),
"Elevator machine room cleaning": T(
 "Elevator machine room cleaning removes construction debris, dust and stored materials from elevator machine rooms and control rooms, with the elevator contractor's permission and without touching any equipment.",
 "Elevator inspectors require machine rooms to be clean, clear and used only for elevator equipment. Debris and dust can also affect controllers and machines.",
 "Crews clean floors, walls and accessible surfaces under the elevator contractor's rules, remove any non-elevator materials with the GC's approval and leave equipment untouched.",
 ["Elevator contractor permission and access", "Inspection date", "Stored materials to remove", "Floor and wall finishes"],
 ["Never touch controllers, machines or governors.", "Machine rooms must not be used for storage."],
 [("Who controls access to elevator machine rooms?", "The elevator contractor controls them until turnover, then the building owner's elevator service company."),
  ("Why must elevator machine rooms be clean?", "Elevator inspectors require it, and dust and debris can affect equipment reliability."),
  ("Can construction materials be stored in an elevator machine room?", "No. Machine rooms are for elevator equipment only, and stored materials cause inspection failures."),
  ("Can cleaners touch elevator equipment?", "No. Cleaning is limited to floors, walls and surfaces the elevator contractor approves.")]),
"Chiller and boiler exterior cleaning": T(
 "Chiller and boiler exterior cleaning cleans the outside casings, insulation jackets and surrounding floors of central plant equipment, removing construction dust and overspray without opening or adjusting the equipment.",
 "Central plant equipment is large, expensive and visible during commissioning and owner tours. Dust on casings and controls looks neglected and can affect components.",
 "Crews clean only cool, de-energized exterior surfaces with the mechanical contractor's approval, using damp microfiber and HEPA vacuums and leaving labels and controls alone.",
 ["Equipment list and approval", "Hot or energized surfaces", "Labels and controls", "Floor and housekeeping pads"],
 ["Hot boiler surfaces cause burns; clean only when cool.", "Controls and panels must not be touched."],
 [("Who cleans the inside of chillers and boilers?", "Mechanical service contractors during maintenance. Construction cleaning covers exteriors only."),
  ("Can boilers be cleaned while they are hot?", "No. Only cool surfaces are cleaned, with the mechanical contractor's approval."),
  ("Why clean central plant equipment before turnover?", "It is seen during commissioning and owner tours, and dust can affect motors and controls."),
  ("Are equipment labels left on during cleaning?", "Yes, nameplates and safety labels must stay in place.")]),
"Duct opening seal inspection and re-seal cleanup": dict(q=[
  ("Why are duct openings capped during construction?", "To keep construction dust and debris out of the HVAC system, which is far cheaper than cleaning ducts later."),
  ("What happens if duct caps tear during construction?", "Dust enters the ducts and may require duct cleaning before turnover, so torn caps should be reported immediately."),
  ("Who reseals open duct ends?", "The mechanical contractor, using plastic and tape or manufactured caps."),
  ("Is duct protection required for LEED?", "Construction IAQ credits based on SMACNA guidelines call for protecting HVAC systems, including capping ducts.")]),
}
