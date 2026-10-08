def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Hotel room post-construction cleaning": dict(
 a="Hotel room post-construction cleaning cleans guest rooms after new construction or brand-required renovations so they can return to inventory, covering bathrooms, furniture, windows, HVAC units, closets and floors to brand standards.",
 q=[("What is a hotel PIP?", "A property improvement plan, a renovation the hotel brand requires to keep the property up to standard. Rooms are renovated in blocks and cleaned before returning to service."),
  ("How are hotel rooms cleaned after renovation?", "Floor by floor with a brand checklist covering bathrooms, furniture, windows, HVAC units, closets and floors, followed by inspection."),
  ("Why does speed matter in hotel renovation cleaning?", "Every night a room is out of service is lost revenue, so rooms are cleaned and returned to inventory as fast as quality allows."),
  ("Who inspects hotel rooms after construction cleaning?", "Hotel management and housekeeping inspect each room, and brand inspectors may review rooms too.")]),
"Hotel public area post-construction cleaning": T(
 "Hotel public area post-construction cleaning cleans lobbies, corridors, ballrooms, meeting rooms, restaurants, fitness centers and pool areas after construction or renovation, to brand standards.",
 "Public areas set the guest's first impression and often have the hotel's most expensive finishes: stone, wood, chandeliers and specialty wallcoverings.",
 "Crews detail each area with finish-specific methods, coordinate lift work for high ceilings and chandeliers, and work overnight where the hotel remains open.",
 ["Areas and finishes", "Feature lighting and high ceilings", "Hotel operating status", "Opening or reopening date"],
 ["Stone floors and walls need stone-safe products.", "Chandeliers and decorative fixtures need specialists."],
 [("What are hotel public areas?", "Lobbies, corridors, ballrooms, meeting rooms, restaurants, fitness centers and pool areas used by guests."),
  ("Are hotel ballrooms cleaned after renovation?", "Yes, including high ceilings, chandeliers, wallcoverings and carpet."),
  ("Are hotel lobbies cleaned overnight?", "Often, when the hotel stays open during renovation."),
  ("Who cleans hotel chandeliers?", "Specialists with lifts and experience with decorative fixtures.")]),
"Fitness center post-construction cleaning": dict(
 a="Fitness center post-construction cleaning cleans gyms and fitness rooms after construction, including rubber and wood floors, mirrors, equipment exteriors, locker rooms, showers and group exercise studios.",
 y="Fitness centers are full of mirrors, equipment and textured rubber floors that show and trap construction dust. Members and residents use them immediately after opening.",
 m="Crews clean mirrors and equipment exteriors with approved products, vacuum and scrub rubber floors with neutral cleaners and detail locker rooms and showers.",
 q=[("Are gym mirrors cleaned after construction?", "Yes, mirror walls are cleaned carefully so no liquid runs behind the edges."),
  ("Is fitness equipment cleaned at turnover?", "Equipment exteriors are cleaned with products the equipment manufacturer allows."),
  ("How are rubber gym floors cleaned?", "Vacuumed and scrubbed with neutral cleaners approved by the flooring manufacturer, because oily products make rubber slippery."),
  ("Are locker rooms and showers included?", "Yes, they are detailed like restrooms.")]),
"Pool deck and natatorium cleaning": T(
 "Pool deck and natatorium cleaning cleans pool decks, natatorium walls, windows, bleachers and equipment areas after construction, before the pool is filled or reopened.",
 "Construction debris on pool decks blows into the pool and clogs drains and filters. Decks must be clean and slip-resistant, and natatoriums have humid conditions that affect finishes.",
 "Crews clean decks, drains and surrounding surfaces, keep debris out of the pool and coordinate with the pool contractor, who handles the pool itself.",
 ["Deck area and surface", "Pool status: empty or filled", "Deck drains", "Pool contractor coordination"],
 ["Debris that reaches the pool can damage filters and pumps.", "Wet decks are slippery; work in sections."],
 [("Who cleans the pool itself after construction?", "The pool contractor, who handles the pool shell, water and equipment."),
  ("Are pool decks cleaned before opening?", "Yes, decks, drains and surrounding areas are cleaned so debris does not enter the pool."),
  ("What is a natatorium?", "An indoor building or room that houses a swimming pool."),
  ("Why are pool deck drains cleaned?", "Construction debris clogs them and can wash into the pool.")]),
"Church and worship space post-construction cleaning": T(
 "Church and worship space post-construction cleaning cleans sanctuaries, pews, altars, choir lofts, fellowship halls, classrooms and offices after construction or renovation, with care for wood, high ceilings and feature elements.",
 "Worship spaces often have high ceilings, exposed wood, pews and decorative elements, and the congregation sees every detail on the first service.",
 "Crews clean high areas from lifts first, clean pews and wood with wood-safe products and refer stained glass and organs to specialists.",
 ["Sanctuary size and ceiling height", "Pews and wood finishes", "Stained glass and organ", "First service date"],
 ["Wood finishes on pews and paneling need gentle products.", "Stained glass and pipe organs need specialists."],
 [("How are church pews cleaned after construction?", "Vacuumed and wiped with wood-safe cleaners, including hymnal racks and kneelers."),
  ("Are sanctuary ceilings cleaned?", "Yes, high ceilings and beams are cleaned from lifts before pews and floors."),
  ("Who cleans stained glass windows?", "Stained glass specialists, because old glass and lead cames are fragile."),
  ("Is the fellowship hall cleaned too?", "Yes, fellowship halls, kitchens and classrooms are part of the clean.")]),
}
