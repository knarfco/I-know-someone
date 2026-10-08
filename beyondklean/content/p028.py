def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Theater and auditorium post-construction cleaning": T(
 "Theater and auditorium post-construction cleaning cleans seating, aisles, stages, orchestra pits, lobbies and control booths in performing arts venues and school auditoriums after construction.",
 "Auditoriums have hundreds of seats, high ceilings and stage equipment. Construction dust settles on seats and lighting and is visible under stage lights.",
 "Crews clean high areas first, clean seating row by row, clean stage floors with care for their finish and leave rigging and stage equipment to stage contractors.",
 ["Seat count and type", "Stage floor finish", "Ceiling height and lighting", "Rigging and stage equipment"],
 ["Stage rigging and lighting are handled only by stage contractors.", "Stage floors often have special finishes that cleaners must not damage."],
 [("Are theater stages cleaned after construction?", "Stage floors are cleaned with methods suited to their finish; rigging and equipment are left to stage contractors."),
  ("Who handles stage rigging during cleanup?", "Stage and rigging contractors. Cleaners do not touch rigging, curtains or lighting."),
  ("How are auditorium seats cleaned?", "Row by row, vacuuming seats and floors and wiping armrests and tablet arms."),
  ("Is the auditorium lobby cleaned too?", "Yes, lobbies, concessions and restrooms are part of the clean.")]),
"Arena and stadium post-construction cleaning": T(
 "Arena and stadium post-construction cleaning cleans seating bowls, concourses, suites, clubs, locker rooms, concessions and press areas in large venues after construction or renovation, before the first event.",
 "Venues have tens of thousands of seats and open on fixed event dates. The scale requires large crews, equipment and careful planning.",
 "Specialist contractors with large crews and equipment are routed, cleaning seating bowls by section and concessions to food service standards.",
 ["Venue size and seat count", "First event date", "Suites and club areas", "Concessions and kitchens"],
 ["The scale requires large, well-coordinated crews.", "Concessions need food-safe cleaning for health inspection."],
 [("How is a new stadium cleaned before the first event?", "By section, with large crews cleaning seats, concourses, suites, concessions and restrooms on a tight schedule."),
  ("Are stadium suites cleaned separately?", "Yes, suites and club areas are detailed like hospitality spaces."),
  ("Are stadium concessions cleaned for health inspection?", "Yes, kitchens and stands are cleaned to food service standards."),
  ("Why is arena cleaning a specialist service?", "The size, schedule and number of spaces require large crews and specialized equipment.")]),
"Library stack and shelving cleaning": T(
 "Library stack and shelving cleaning cleans library shelving, stacks, reading rooms and study areas after construction, before the collection is moved in.",
 "Dust on shelves transfers to books and archives and can damage them. Once books are shelved, cleaning shelves becomes slow and risky.",
 "Crews vacuum and wipe shelves top down before the collection arrives, and clean reading rooms, study carrels and service desks.",
 ["Shelving extent", "Collection move date", "Reading and study areas", "Special collections rooms"],
 ["Cleaning around shelved books needs the library's approval.", "Tall stacks may need ladders or lifts."],
 [("Why clean library shelves before books are moved in?", "Construction dust transfers to books and can damage them, and cleaning around shelved books is slow."),
  ("When are library shelves cleaned?", "After construction and before the collection move."),
  ("Are reading rooms cleaned?", "Yes, reading rooms, study carrels and service desks are cleaned."),
  ("Who moves library collections?", "Specialized library movers, coordinated with the library staff.")]),
"Warehouse post-construction cleaning": dict(
 a="Warehouse post-construction cleaning prepares new distribution centers and warehouses for tenants: overhead dusting, slab sweeping and scrubbing, dock cleaning, office and restroom detailing and exterior truck court sweeping.",
 q=[("What is included in warehouse post-construction cleaning?", "Overhead dusting, slab sweeping and scrubbing, dock and leveler cleaning, office and restroom detailing, and exterior truck court sweeping."),
  ("How long does it take to clean a new warehouse?", "It depends on size and clear height; large distribution centers can take several days with multiple ride-on machines and lifts."),
  ("Should a warehouse be cleaned before racking is installed?", "Yes. An empty building is far faster and easier to clean, especially overhead."),
  ("Who sweeps warehouse truck courts?", "The cleaning contractor or a power sweeping subcontractor with truck-mounted sweepers.")]),
"Pallet rack cleaning": dict(
 a="Pallet rack cleaning removes dust and debris from racking uprights, beams, wire decking and rack tops in warehouses, distribution centers and big-box stores, from lifts and with product protected below.",
 w=["Never climb racking; use lifts with spotters.", "Loaded racks need product covered before overhead dust is disturbed."],
 q=[("How is pallet racking cleaned?", "From lifts, vacuuming rack tops and decking and wiping beams and uprights, with product below covered."),
  ("Can workers climb racking to clean it?", "No. Racking is not designed to be climbed; crews use lifts with spotters."),
  ("Why clean the tops of pallet racks?", "Dust collects there and falls onto stored product, which is an audit finding in food and pharmaceutical warehouses."),
  ("Is rack cleaning part of high dusting?", "Often yes, rack tops are included in scheduled high dusting programs.")]),
}
