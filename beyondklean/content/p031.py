def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Walk-in freezer interior cleaning": dict(
 a="Walk-in freezer interior cleaning cleans new freezer boxes before pull-down, including wall and ceiling panels, floors, shelving, door heaters, gaskets and strip curtains, using minimal water so nothing freezes in place.",
 q=[("Why clean a walk-in freezer before it is started?", "Once the freezer is cold, any water freezes and debris freezes to surfaces, making cleaning slow and unsafe."),
  ("Can wet cleaning be used in a walk-in freezer?", "Only with minimal water, and surfaces are dried thoroughly before the box is pulled down to temperature."),
  ("Who starts up a new walk-in freezer?", "The refrigeration contractor, after cleaning is complete and the door and panels are checked."),
  ("Do freezer floors need special care during cleaning?", "Yes. Water left on the floor turns to ice, so floors are cleaned with minimal moisture and dried completely.")]),
"Kitchen ceiling cleaning": dict(
 a="Kitchen ceiling cleaning removes construction dust, overspray and residue from commercial kitchen ceilings, including washable ceiling tiles, FRP, metal panels, gypsum and light fixtures above food preparation areas.",
 q=[("Why do health inspectors check commercial kitchen ceilings?", "Dust and debris overhead can fall into food. Ceilings above food areas must be clean, intact and cleanable."),
  ("What ceiling materials are used in commercial kitchens?", "Washable vinyl-faced tiles, FRP, metal panels or painted gypsum with a washable finish."),
  ("Should kitchen ceilings be cleaned before equipment and walls?", "Yes. Cleaning top down means dust from the ceiling never lands on cleaned walls and equipment."),
  ("Can kitchen ceiling tiles be washed?", "Only tiles rated as washable. Standard mineral fiber tiles absorb water and stain, so they are cleaned dry or replaced.")]),
"Food-contact surface pre-opening cleaning": dict(q=[
  ("What is a food-contact surface?", "Any surface that food normally touches, such as prep tables, cutting boards, slicers, shelves for open food and equipment interiors."),
  ("Why must food-contact surfaces be cleaned before they are sanitized?", "Sanitizers do not work properly on dirty surfaces. Soil and residue shield microorganisms from the sanitizer."),
  ("What cleaners are used on food-contact surfaces before opening?", "Food-safe detergents that rinse clean without residue. Solvents and general-purpose chemicals are not used."),
  ("Who sanitizes food surfaces before a restaurant opens?", "Restaurant staff or a trained contractor using registered sanitizers at label concentration.")]),
"Food-contact surface sanitizing per label": dict(
 a="Food-contact surface sanitizing per label applies registered sanitizers at the concentration, contact time and rinse requirements printed on the product label to cleaned food-contact surfaces before a food facility opens.",
 q=[("What is the difference between cleaning and sanitizing food surfaces?", "Cleaning removes soil and residue. Sanitizing reduces microorganisms to safe levels using a registered product, and it only works on surfaces that are already clean."),
  ("How is sanitizer concentration checked?", "With test strips made for the specific sanitizer, so the solution is strong enough to work but not so strong it leaves harmful residue."),
  ("Do food-contact sanitizers need to be rinsed off?", "It depends on the product. The label states whether a rinse is required, and the label must be followed."),
  ("Who can sanitize food-contact surfaces?", "Trained staff or contractors using registered sanitizers exactly as the label directs.")]),
"Prep table and shelving cleaning": T(
 "Prep table and shelving cleaning cleans stainless prep tables, undershelves, wall shelves, wire racks and storage shelving in commercial kitchens before opening, including tops, undersides, legs and feet.",
 "Prep tables are food-contact surfaces and shelving holds food and supplies. Construction dust collects on undersides and wire shelving that are easy to miss.",
 "Crews clean top surfaces, undersides, legs and shelves with food-safe cleaners, rinse, dry and leave food-contact surfaces ready for sanitizing.",
 ["Number of tables and shelving units", "Stainless or wire shelving", "Food-safe products", "Sanitizing responsibility"],
 ["Sharp edges on wire shelving and table corners require gloves.", "Chlorides harm stainless; use stainless-safe products."],
 [("Are the undersides of prep tables cleaned?", "Yes. Undersides, legs and undershelves collect construction dust and are checked by inspectors."),
  ("What cleaners are used on kitchen prep tables?", "Food-safe cleaners that rinse clean, followed by sanitizing with a registered product."),
  ("Do wire shelves need cleaning before opening?", "Yes, every wire collects dust, so shelves are wiped thoroughly before food is stored."),
  ("Should prep tables be sanitized after cleaning?", "Yes, prep tables are food-contact surfaces and must be sanitized after cleaning.")]),
}
