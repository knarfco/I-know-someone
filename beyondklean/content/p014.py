def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Post-IT and AV install clean": dict(a=
 "A post-IT and AV install clean removes the ceiling tile dust, cable scraps, zip ties, packaging and fingerprints left after technology, audio-visual and security installers finish, and re-cleans the rooms they worked in.",
 q=[("Why does a building need cleaning after IT installation?", "Low-voltage installers lift ceiling tiles, pull cable and mount devices after the final clean. That drops dust and debris into finished rooms right before move-in."),
  ("How are new TV screens and displays cleaned?", "With a dry or barely damp microfiber cloth wiped gently. Liquid is never sprayed onto screens, and the display manufacturer's guidance is followed."),
  ("What debris do AV installers typically leave?", "Cable scraps, zip ties, packaging, screws, ceiling tile dust and fingerprints on ceiling tiles and walls."),
  ("When is the post-IT clean scheduled?", "After the technology installers finish and before occupants move in, usually in the last days before turnover.")]),
"Model unit and show suite cleaning": T(
 "Model unit and show suite cleaning keeps model apartments, model homes and sales suites spotless during construction and lease-up, with scheduled cleaning and touch-ups before tours.",
 "Models sell the project. They are toured repeatedly while construction continues nearby, so dust settles daily and fingerprints accumulate.",
 "Crews clean models on a recurring schedule, touch up before scheduled tours and events, and care for staging furniture and decor with gentle methods.",
 ["Number of models and sales suites", "Tour and event schedule", "Staging furniture and decor", "Recurring frequency"],
 ["Construction dust from nearby work settles daily.", "Staging decor is often rented; handle with care."],
 [("Why do model units need frequent cleaning?", "They are toured constantly while construction continues nearby, so dust and fingerprints build up quickly."),
  ("How often should a model unit be cleaned?", "Commonly weekly, with touch-ups before major tours or events."),
  ("Is staging furniture cleaned?", "Yes, furniture and decor are dusted and wiped gently."),
  ("Who arranges model unit cleaning?", "The developer or the leasing and sales team.")]),
"Vacant space turnover cleaning": T(
 "Vacant space turnover cleaning cleans empty commercial suites, retail spaces and units between tenants or after renovation, so they can be shown, inspected or leased.",
 "Vacant spaces collect dust, dead insects and debris, and prospective tenants form opinions in the first minute of a showing.",
 "Crews clean the full space top down, remove leftover debris, clean restrooms and glass, and offer touch-ups before showings.",
 ["Space size and condition", "Utilities status: water and power", "Showing schedule", "Debris left by previous tenant"],
 ["Without water or power, some tasks may need workarounds.", "Spaces re-soil while vacant; plan touch-ups."],
 [("What is vacant space turnover cleaning?", "Cleaning an empty space so it is ready to show, inspect or lease."),
  ("How often should a vacant space be cleaned?", "Once thoroughly, then touched up before showings."),
  ("Do utilities need to be on for turnover cleaning?", "Water and power make it much easier; crews can work around them if needed."),
  ("Who arranges vacant space cleaning?", "Usually the property manager or landlord.")]),
"Property management turnover cleaning": T(
 "Property management turnover cleaning cleans spaces for property managers between tenants or after work orders, following the manager's checklist and timeline.",
 "Property managers need fast, consistent turnovers to keep vacancy low. Each day a unit sits dirty is lost rent.",
 "Crews follow the property manager's checklist, take photos for the file and report damage or repairs needed.",
 ["Property manager checklist", "Turnaround time", "Photo documentation", "Damage reporting"],
 ["Turnaround windows are often short.", "Damage must be reported, not cleaned over."],
 [("What is property management turnover cleaning?", "Cleaning between tenants or after work, to the property manager's standard."),
  ("Who sets the turnover checklist?", "The property manager, often with photos required."),
  ("How fast is a typical turnover?", "Often within a few days, depending on size and condition."),
  ("Do turnover crews report damage?", "Yes, damage and repair needs are reported to the manager.")]),
"Post-renovation reset clean": T(
 "A post-renovation reset clean returns an occupied building to normal after a renovation, cleaning the renovated area and the surrounding spaces where dust spread.",
 "Renovation dust travels beyond barriers through doors, HVAC and foot traffic. Occupants judge the project by how quickly their space feels clean again.",
 "Crews clean the renovated area top down, then clean adjacent rooms, corridors and HVAC grilles, coordinating with occupants' schedules.",
 ["Renovated area", "Adjacent spaces affected", "Occupant schedule", "HVAC grilles and filters"],
 ["Dust spreads further than expected.", "Occupied spaces need after-hours work."],
 [("What is a post-renovation reset clean?", "A clean that returns the renovated area and surrounding spaces to normal after work ends."),
  ("Why clean areas outside the renovation zone?", "Dust spreads through doors, HVAC and foot traffic."),
  ("Is the HVAC included in a reset clean?", "Grilles are cleaned and filters may need changing."),
  ("When is the reset clean done?", "Right after the renovation ends, often after hours.")]),
}
