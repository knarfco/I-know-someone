def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Sidewalk pressure washing": dict(q=[
  ("When can new concrete sidewalks be pressure washed?", "Once the concrete has cured enough to resist surface damage. Very young concrete can be etched by high pressure, so crews follow the concrete contractor's timing and start with lower pressure and a surface cleaner."),
  ("Can pressure washing water go into the storm drain?", "Generally no. Wash water from construction sites carries concrete fines, soil and residue, so crews block inlets and vacuum the water up, or recover it with reclaim equipment, for approved disposal."),
  ("What is a surface cleaner for pressure washing?", "A rotating attachment with spinning nozzles under a hood. It cleans flat concrete evenly without the stripes a wand leaves and reduces overspray onto glass and landscaping."),
  ("Is sidewalk cleaning part of the final construction clean?", "Usually yes. Entry walks and sidewalks are cleaned before the owner walk and certificate of occupancy inspection, because mud and slurry on walks track straight into the new building.")]),
"Parking lot sweeping": T(
 "Parking lot sweeping uses truck-mounted or ride-on power sweepers to remove construction dirt, gravel, millings, debris and litter from new parking lots, drive aisles and loading areas before striping and turnover.",
 "Construction lots collect mud, stone, nails and trash that puncture tires, wash into storm drains and keep striping paint from bonding. A swept lot is also one of the first signs to an owner that the site is finished.",
 "Crews power sweep in overlapping lanes, hand-sweep islands, curb lines and corners the machine cannot reach, and lift debris off drain inlet grates instead of pushing it through.",
 ["Lot area and number of drive aisles", "Striping and seal coat schedule", "Drain inlets and inlet protection", "Day or night work and traffic control"],
 ["Fresh seal coat or asphalt needs cure time before heavy sweepers run on it.", "Sweepers working near open traffic need cones, flaggers or after-hours scheduling."],
 [("Why sweep a parking lot before striping?", "Striping paint needs a clean, dry surface to bond. Dirt and grit under the paint make new lines flake off within weeks."),
  ("How often should a construction parking lot be swept?", "During construction, as needed to control track-out, often weekly near completion. A final sweep happens right before striping and again before turnover."),
  ("Who does parking lot sweeping on a construction project?", "Power sweeping contractors with truck-mounted or ride-on sweepers, coordinated by the GC or the cleaning contractor."),
  ("Are storm drain inlets cleaned during lot sweeping?", "Debris is lifted off the inlet grates and out of inlet protection. Cleaning inside the drain structure is a separate task done with vacuum equipment.")]),
"Parking lot washing": T(
 "Parking lot washing uses pressure washing and water reclaim equipment to remove oil, rust, concrete slurry and grime stains from paved lots and garages after sweeping.",
 "Sweeping removes loose debris but not stains. Oil spots, rust from steel deliveries and concrete slurry marks make a brand-new lot look used, and wash water from lots is regulated because it carries pollutants.",
 "Crews sweep first, pre-treat stains, wash with surface cleaners and recover the water with vacuum reclaim units so nothing reaches storm drains.",
 ["Lot area and pavement type", "Stain types: oil, rust, slurry", "Water source and reclaim equipment", "Disposal location for recovered water"],
 ["Wash water with oil and degreaser must be recovered, not discharged to storm drains.", "High pressure can damage fresh seal coat and striping."],
 [("Is parking lot washing the same as sweeping?", "No. Sweeping removes loose dirt and debris; washing removes stains like oil, rust and concrete slurry using water, cleaners and reclaim equipment."),
  ("What happens to the water used to wash a parking lot?", "It should be recovered with vacuum reclaim equipment and disposed of where the local authority allows, rather than flowing into storm drains."),
  ("Can oil stains be removed from a new parking lot?", "Fresh oil stains often come out with degreasers and hot water. Old stains soaked deep into asphalt or concrete may only lighten."),
  ("When should a new parking lot be washed?", "After construction traffic ends and before the owner walk, usually after the final sweep and before or after striping depending on the paint's cure time.")]),
"Loading dock washing": T(
 "Loading dock washing cleans dock aprons, dock pits, bumpers, wall faces and leveler exteriors with pressure washing and water recovery, removing mud, oil, rubber marks and construction residue.",
 "Docks take the heaviest construction traffic on the building: every delivery, every lift and every dumpster pull. Oil and mud there spread into the warehouse once operations begin.",
 "Crews clear debris, degrease oil spots, wash from the wall out toward the apron and recover the water, protecting trench drains and dock pits.",
 ["Number of dock positions", "Leveler and pit type", "Trench drains at the apron", "Water recovery method"],
 ["Dock edges are fall hazards; work with barriers or dock locks in place.", "Leveler pits are confined spaces with moving equipment; only clean them with the dock equipment contractor's lockout."],
 [("How are loading docks cleaned after construction?", "Debris is cleared, oil spots are degreased, and the dock face, bumpers and apron are pressure washed with the water recovered."),
  ("Are dock leveler pits cleaned?", "Debris in leveler pits should be removed, but only with the leveler locked out by the dock equipment contractor."),
  ("Why do dock aprons need degreasing?", "Trucks and lifts leave oil and hydraulic fluid that becomes slippery and spreads into the building."),
  ("Can dock wash water go into the trench drain?", "Only where the drain is connected to an approved system. Many dock drains lead to storm sewers, so wash water must be recovered.")]),
"Dumpster pad degreasing": T(
 "Dumpster pad degreasing cleans the concrete pad and enclosure around dumpsters and compactors, removing grease, food waste residue, oil and stains with degreasers and recovered wash water.",
 "Dumpster pads become the smelliest, dirtiest surface on a property within weeks of opening, especially at restaurants and grocery stores. Residue attracts pests and stains run toward drains.",
 "Crews scrape solids, apply a degreaser suited to the soil, scrub, then pressure wash with hot water where possible and vacuum the wash water for approved disposal.",
 ["Pad and enclosure size", "Grease and food waste level", "Nearby drains", "Wash water disposal"],
 ["Grease-laden wash water must not reach storm drains.", "Compactors must be locked out before cleaning around them."],
 [("Why does a dumpster pad need degreasing?", "Grease and food waste build up and cause odors, pests and slippery stains that spread across the lot."),
  ("Is dumpster pad wash water recovered?", "It should be. Grease and food residue are pollutants, so the water is vacuumed up for approved disposal."),
  ("How often should a restaurant dumpster pad be cleaned?", "Often monthly or more for restaurants and grocery stores, and at turnover for new construction."),
  ("Is the dumpster enclosure cleaned too?", "Yes. Gates, walls and bollards are washed along with the pad.")]),
}
