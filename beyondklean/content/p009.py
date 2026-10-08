def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Apartment unit post-construction clean": dict(q=[
  ("What is included in an apartment final clean?", "Every surface in the unit: kitchen, appliances inside and out, bathrooms, closets, windows and blinds, fixtures, outlets, baseboards and floors. Crews follow a unit checklist so every unit matches."),
  ("How long does it take to clean a new apartment unit?", "A typical new unit takes a few crew-hours, depending on size, finishes and dust levels. Larger units and townhome-style units take longer."),
  ("Are appliance interiors cleaned in an apartment turnover?", "Yes. Packaging, protective film, labels and construction dust are removed from inside refrigerators, ovens, dishwashers and microwaves as well as the exteriors."),
  ("Do apartments need cleaning again before move-in?", "Often a light re-dust and floor touch-up is needed if units sat empty for weeks after the final clean, especially when nearby units were still under construction.")]),
"Condo unit final clean": T(
 "A condo unit final clean prepares a new condominium for the buyer's walkthrough and closing, at a higher level of detail than a typical rental turnover, covering every finish, fixture, appliance and closet.",
 "Condo buyers walk their unit with a punch list and judge every surface. Missed dust, labels or smudges become buyer complaints and delay closings.",
 "Crews detail top down with finish-specific products, pay extra attention to stone, glass and specialty fixtures, and do a touch-up pass right before the buyer walk.",
 ["Unit finishes and upgrades", "Buyer walk and closing dates", "Appliance package", "Balcony and storage"],
 ["High-end stone and specialty finishes need specific cleaners.", "Units re-soil if trades return after the clean."],
 [("Is a condo final clean different from an apartment clean?", "Yes. Buyers inspect their own unit closely, so the clean is more detailed and is usually followed by a touch-up right before the walkthrough."),
  ("When should a condo be cleaned before closing?", "After all punch work is done, with a final touch-up a day or two before the buyer walkthrough."),
  ("Are condo balconies and storage units cleaned?", "They should be, since buyers inspect everything that comes with the unit."),
  ("Who pays for the condo final clean?", "Usually the developer or GC as part of delivering the unit.")]),
"Townhome final clean": T(
 "A townhome final clean cleans multi-level townhomes from the top floor down, including stairs, garages, patios, balconies and every room, kitchen and bathroom, before closing or lease-up.",
 "Townhomes combine the detail of a home with stairs, garages and outdoor spaces that often get missed. Dust from upper floors falls onto lower floors if the order is wrong.",
 "Crews start on the top floor and work down, finish stairs last, and clean garages and outdoor spaces as separate checklist items.",
 ["Number of levels and units", "Garage and outdoor spaces", "Stair finishes", "Buyer or lease dates"],
 ["Cleaning lower floors first means re-cleaning them.", "Garage floors often have concrete and paint residue."],
 [("Why are townhomes cleaned from the top floor down?", "Dust and debris fall down stairs, so starting at the top avoids re-cleaning finished floors."),
  ("Are townhome garages included in the final clean?", "Yes. Garages usually need sweeping, residue removal and cleaning of doors and walls."),
  ("Are patios and balconies cleaned?", "Yes, outdoor spaces are cleaned along with the interior."),
  ("How long does a townhome final clean take?", "Longer than a flat of the same size because of stairs and multiple levels, often most of a crew-day.")]),
"Amenity space final clean": T(
 "An amenity space final clean prepares clubhouses, fitness centers, pool areas, lounges, coworking rooms and rooftop decks in residential communities before leasing tours or resident use.",
 "Amenities sell the property. They are often finished first so leasing can start, and they are toured repeatedly, so they need to look perfect early and stay that way.",
 "Crews detail each amenity with appropriate methods for equipment, glass, upholstery and outdoor areas, and schedule touch-ups around tour days.",
 ["Amenity spaces and finishes", "Fitness equipment and pool areas", "Leasing tour schedule", "Ongoing touch-ups"],
 ["Pool areas must stay clear of construction debris.", "Fitness equipment has manufacturer cleaning requirements."],
 [("Why are amenity spaces cleaned before the rest of a building?", "Leasing often starts from the clubhouse and amenities, so they must be tour-ready first."),
  ("Is fitness equipment cleaned at turnover?", "Yes, equipment exteriors, mirrors and floors are cleaned with approved products."),
  ("Are rooftop decks included?", "Yes, outdoor amenities are cleaned along with indoor spaces."),
  ("How are amenities kept clean during lease-up?", "With scheduled touch-up cleans before tours and events.")]),
"Leasing office final clean": T(
 "A leasing office final clean prepares the leasing center or sales office for its opening, covering the reception area, offices, model kitchen, restrooms, glass and furniture.",
 "The leasing office is the first stop for every prospective resident, and it usually opens while the rest of the property is still under construction.",
 "Crews detail the leasing office first, then schedule frequent touch-ups because construction dust from nearby work keeps settling.",
 ["Opening date", "Furniture and decor installed", "Glass and entry", "Touch-up schedule"],
 ["Construction nearby re-soils the office quickly.", "Decor and furniture need gentle cleaning."],
 [("Why is the leasing office cleaned first?", "It opens to prospects before the rest of the property is finished."),
  ("How often does a leasing office need cleaning during construction?", "Often several times a week, because dust from active construction keeps settling."),
  ("Is furniture cleaned in the leasing office?", "Yes, furniture and decor are dusted and wiped."),
  ("Is the leasing office entry cleaned?", "Yes, glass, doors and the approach are cleaned for a strong first impression.")]),
}
