def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Drywall mud and paint removal from carpet": dict(q=[
  ("Should wet drywall mud on carpet be wiped up?", "No. Wiping spreads it into the fibers. Let it dry, break it up, vacuum the pieces and treat the remaining residue."),
  ("Can latex paint be removed from new carpet?", "Usually, if treated before it fully cures, with a latex paint spotter and blotting."),
  ("Why does drywall mud end up on new carpet?", "Carpet is often installed before final drywall and paint touch-ups, so drips land on it."),
  ("How do you prevent paint and mud on new carpet?", "By protecting carpet with film or board until painting and drywall touch-ups are finished.")]),
"Carpet seam and edge detailing": dict(q=[
  ("Why are carpet edges dirty after vacuuming?", "Most vacuums do not reach right to the wall, so dust builds up along baseboards as a visible line."),
  ("Should loose carpet threads be pulled?", "No. Pulling can unravel the carpet; loose fibers are trimmed level with the pile."),
  ("What is a carpet transition strip?", "The strip where carpet meets another flooring type, which collects dust and debris."),
  ("Is carpet edge detailing part of the final clean?", "Yes, edges, corners and transitions are detailed with crevice tools.")]),
"Upholstery and furniture vacuuming": dict(
 a="Upholstery and furniture vacuuming removes construction dust, threads and debris from new chairs, sofas, cushions, benches and fabric furniture after delivery and installation.",
 q=[("Does new furniture need cleaning after installation?", "Yes, it collects construction dust and packaging debris after delivery."),
  ("How is new upholstery vacuumed?", "With upholstery tools and gentle passes, including seams and crevices."),
  ("Is furniture cleaning part of the final clean?", "Usually it is done after furniture installation as part of the move-in clean."),
  ("Can furniture law tags be removed?", "Required law tags should stay on; promotional tags and stickers can be removed.")]),
"Upholstery extraction": dict(
 a="Upholstery extraction deep-cleans fabric furniture by injecting and extracting a cleaning solution, removing stains and embedded soil from upholstery that vacuuming cannot reach.",
 y="Stains from construction, deliveries or spills on new furniture need cleaning before occupants arrive, and the wrong method can shrink, bleed or water-mark fabric.",
 q=[("What are upholstery cleaning codes?", "Letters on furniture tags, such as W, S, WS and X, that tell which cleaning methods are safe for the fabric."),
  ("Can all upholstery be cleaned with water extraction?", "No. Fabrics coded S or X cannot be wet-cleaned and need solvent or vacuum-only methods."),
  ("How long does upholstery take to dry after extraction?", "Usually a few hours with low-moisture methods and good airflow."),
  ("Who cleans stains on new office furniture?", "Upholstery cleaning specialists or trained crews following the fabric's cleaning code.")]),
"Fabric panel and cubicle cleaning": dict(
 a="Fabric panel and cubicle cleaning vacuums and spot-cleans office workstation panels, removing construction dust, labels and marks from fabric surfaces and wiping work surfaces and trim.",
 q=[("How are cubicle panels cleaned after installation?", "Vacuumed with soft brush tools, then spot-cleaned with low-moisture methods where needed."),
  ("Do new workstations need cleaning?", "Yes, they collect dust during installation and from nearby construction."),
  ("Can fabric cubicle panels be shampooed?", "Usually only spot cleaning is recommended to avoid water rings."),
  ("Who cleans new office workstations?", "The cleaning crew after furniture installation, before move-in.")]),
"Auditorium and theater seating cleaning": dict(
 m="Crews work row by row, vacuuming seats, backs and the floor beneath each row, wiping armrests, cup holders and tablet arms, and spot-cleaning upholstery.",
 w=["Folding seat mechanisms can pinch fingers.", "The floor beneath seats is easy to miss without a row-by-row plan."],
 q=[("How are auditorium seats cleaned after construction?", "Row by row, vacuuming seats and the floor beneath each row and wiping armrests and tablet arms."),
  ("Do theater seats need upholstery extraction?", "Only where they are stained; routine turnover cleaning is vacuuming and spot cleaning."),
  ("How long does it take to clean an auditorium?", "It depends on seat count; large auditoriums can take a full crew shift or more."),
  ("Why clean under auditorium seats?", "Debris and dust collect there and are visible when seats are folded.")]),
}
