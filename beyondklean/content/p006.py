def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Balcony and terrace cleaning": T(
 "Balcony and terrace cleaning cleans outdoor balconies, roof terraces and patios at turnover: decking or pavers, railings, glass panels, drains and door thresholds.",
 "Balconies collect debris from facade work, sealant and paint, and their drains clog easily. Residents and tenants step onto them on day one.",
 "Crews remove debris, clean drains, wash decks with methods suited to the surface, and clean railings and glass from safe positions.",
 ["Number and size of balconies", "Deck material", "Railings and glass", "Drains"],
 ["Work near open edges requires fall protection rules.", "Wash water should not run down the facade."],
 [("Are balcony drains cleaned at turnover?", "Yes, they clog easily with construction debris."),
  ("How are glass balcony railings cleaned?", "Both sides of each panel are cleaned from safe positions."),
  ("Can balconies be pressure washed?", "Depending on the deck surface, with care so water does not run down the facade."),
  ("Who cleans balconies in a new apartment building?", "The cleaning crew as part of unit turnover.")]),
"Solar array cleaning": T(
 "Solar array cleaning removes construction dust and residue from solar panels following the panel manufacturer's instructions and electrical safety requirements. It is conditional work.",
 "Construction dust on new panels reduces output, but panels are energized whenever there is light, and improper cleaning can damage coatings and void warranties.",
 "Requests are reviewed and routed only to crews qualified for solar work, using deionized water and soft brushes and following electrical safety and fall protection rules.",
 ["Array size and location", "Manufacturer cleaning guidance", "Electrical safety and fall protection", "Water quality"],
 ["Panels produce voltage whenever light is present.", "Hard water and abrasives damage panel glass and coatings."],
 [("Does dust reduce solar panel output?", "Yes, dust and residue block light and reduce output."),
  ("Why is solar cleaning conditional work?", "Panels are energized in daylight and are often on roofs, so electrical and fall hazards apply."),
  ("What water is used to clean solar panels?", "Often deionized or purified water to avoid mineral spots."),
  ("Who should clean solar panels?", "Crews trained for solar work following the manufacturer's instructions.")]),
}
