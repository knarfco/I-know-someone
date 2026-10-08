def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Controlled contamination cleaning": T(
 "Controlled contamination cleaning cleans manufacturing and assembly environments that have defined contamination limits, such as electronics assembly, aerospace, optics and precision manufacturing, following the site's written protocol.",
 "These environments are not always formal cleanrooms, but particles, fibers and residues can still ruin products. Construction contamination must be removed before production starts.",
 "Requests are routed only to specialists after review, who use the site's approved materials, garments and sequence and document results for the owner's quality team.",
 ["Site contamination protocol", "Approved materials and garments", "Areas and equipment", "Verification method"],
 ["Wrong wipes, mops or chemicals introduce new contamination.", "Production equipment must not be touched without approval."],
 [("What is controlled contamination cleaning?", "Cleaning to defined limits for particles, fibers or residues in sensitive manufacturing areas, following a written protocol."),
  ("Where is controlled contamination cleaning used?", "Electronics and aerospace assembly, optics, precision machining and similar manufacturing spaces."),
  ("Who performs controlled contamination cleaning?", "Specialist crews trained in the site's protocol and materials."),
  ("Is the cleaning verified?", "Often, through particle counts, surface tests or the owner's quality inspections.")]),
"Vivarium and animal facility cleaning": T(
 "Vivarium and animal facility cleaning cleans research animal facilities after construction, including holding rooms, procedure rooms, cage wash areas and corridors, following the institution's facility and regulatory requirements before animals arrive.",
 "Animal facilities are regulated, and animal health and research integrity depend on clean, controlled environments. Products and methods must be approved by the facility.",
 "Requests are routed only to specialists after review, working under the facility manager's direction with approved products and documented procedures.",
 ["Facility requirements and approvals", "Approved products", "Room types and sequence", "Documentation"],
 ["Only facility-approved products may be used.", "Access is controlled and may require training."],
 [("What is a vivarium?", "A facility that houses research animals under controlled conditions."),
  ("Who cleans a new vivarium after construction?", "Specialist crews working under the facility manager's direction."),
  ("Why is vivarium cleaning conditional work?", "Regulatory requirements and animal health require approved products, procedures and documentation."),
  ("Are cleaning products restricted in animal facilities?", "Yes, only products approved by the facility may be used.")]),
"School post-construction cleaning": dict(q=[
  ("When should a new school be cleaned before opening?", "After trades finish and before furniture and staff move in, with a touch-up pass in the days before students arrive."),
  ("Do school cleaning crews need background checks?", "Many school districts require background checks for anyone working on school property, so crews are screened before they are assigned."),
  ("Why do schools ask for low-odor cleaning products?", "Students and staff arrive soon after cleaning, and strong odors cause complaints and can affect sensitive students."),
  ("Is the school cafeteria kitchen cleaned for health inspection?", "Yes. Cafeteria kitchens are cleaned to food service standards before the health department's opening inspection.")]),
"Classroom turnover cleaning": dict(
 a="Classroom turnover cleaning cleans individual classrooms after construction or summer renovation, including boards, casework, sinks, windows, floors, desks and technology mounts, so teachers can set up their rooms.",
 w=["Interactive boards and projectors must not be sprayed or moved.", "Whiteboards need manufacturer-approved cleaners to avoid ghosting."],
 q=[("What does classroom turnover cleaning include?", "Boards, casework, sinks, windows, light fixtures, furniture and floors, cleaned top down to a classroom checklist."),
  ("How long does it take to clean a classroom after construction?", "Usually a few crew-hours per room, depending on how much construction dust and furniture are present."),
  ("Are interactive classroom boards cleaned?", "Yes, gently with approved cleaners applied to a cloth, never sprayed onto the board or projector."),
  ("When can teachers set up their classrooms?", "After the turnover clean is done and the room has been signed off by the school or GC.")]),
"Dormitory and student housing turnover": dict(
 a="Dormitory and student housing turnover cleans residence hall rooms, suites, shared bathrooms, lounges, kitchens and corridors after construction or summer renovations, before students move in.",
 w=["Move-in day is fixed; crews must finish every room on time.", "Shared bathrooms need detailed cleaning and inspection."],
 q=[("When are dormitories cleaned after construction?", "Before move-in, usually in summer, on a schedule that finishes every room before students arrive."),
  ("Are shared dorm bathrooms cleaned during turnover?", "Yes, shared bathrooms are a focus because they get the most use and the closest inspection."),
  ("How long does dormitory turnover cleaning take?", "It depends on the number of rooms; large halls need multiple crews working floor by floor."),
  ("Who sets the cleaning standard for student housing?", "The university's housing or facilities department, often with its own checklist.")]),
}
