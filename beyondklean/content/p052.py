def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Entrance mat and grate cleaning": T(
 "Entrance mat and grate cleaning cleans recessed walk-off mats, metal or aluminum grates, roll-up entrance systems and the pits beneath them, removing construction dirt, debris and water.",
 "Entrance systems are designed to trap most of the dirt entering a building. Construction fills their pits with debris long before the building opens, so they stop working.",
 "Crews lift grates and roll-up mats where designed to be lifted, vacuum and clean the pits, clean the mats or inserts and reinstall everything level.",
 ["Entrance systems and sizes", "Removable grates or roll-up mats", "Pit debris and water", "Drainage in pits"],
 ["Grates are heavy; use proper lifting technique.", "Pits can hold standing water and sharp debris."],
 [("What is a walk-off mat system?", "A recessed entrance matting system that traps soil and moisture from shoes before it reaches interior floors."),
  ("Why clean entrance mats after construction?", "Construction fills mat pits with debris and dirt, so they stop trapping soil."),
  ("Can entrance grates be lifted for cleaning?", "Many recessed systems are designed to be lifted or rolled up for cleaning."),
  ("How often should entrance mats be cleaned?", "At turnover, then regularly during operation, often daily vacuuming.")]),
"Stair tread and nosing cleaning": dict(
 m="Crews clean from the top step down, remove adhesive and residue from treads and nosings with compatible products and scrub textured nosings so the contrast strip stays visible.",
 w=["Wet stairs are slippery; clean in sections and keep a dry path.", "Nosing contrast strips must stay clean and visible for safety."],
 q=[("How are stairs cleaned after construction?", "From the top step down, tread by tread, finishing with risers and landings."),
  ("What is a stair nosing?", "The front edge of a stair tread, often with a contrasting or anti-slip strip."),
  ("Why are stair nosings important to clean?", "They help people see the edge of each step, so contrast and grip must stay clear."),
  ("Are stairs part of the final clean?", "Yes, stairs and landings are cleaned in every stair tower and feature stair.")]),
"Carpet extraction": dict(q=[
  ("What is carpet extraction?", "Cleaning that injects a cleaning solution into the carpet and immediately vacuums it back out, often called hot water extraction or steam cleaning."),
  ("How long does carpet take to dry after extraction?", "Usually a few hours with low-moisture methods and air movers, longer if humidity is high."),
  ("Can extraction damage new carpet?", "Over-wetting or harsh chemicals can, which is why the carpet manufacturer's cleaning guidance is followed."),
  ("Why do stains come back after carpet extraction?", "Soil or residue deep in the backing wicks back up to the surface as the carpet dries.")]),
"Carpet tile cleaning": dict(q=[
  ("Is carpet tile cleaned differently from broadloom carpet?", "The methods are similar, but damaged carpet tiles can be replaced individually instead of cleaned."),
  ("Can carpet tiles be lifted to clean underneath?", "They can be lifted for replacement, but routine cleaning does not require lifting them."),
  ("Why keep spare carpet tiles from the installation?", "Spare tiles from the same dye lot allow invisible replacements later."),
  ("Does moisture affect carpet tiles?", "Excess water can loosen tile adhesive and affect the backing, so low-moisture methods are used.")]),
"Carpet spot and stain treatment": dict(q=[
  ("How do you remove paint from new carpet?", "Treat it quickly with a spotter made for the paint type, blotting from the outside in rather than rubbing."),
  ("Why shouldn't carpet stains be rubbed?", "Rubbing spreads the stain, pushes it deeper and frays the carpet fibers."),
  ("Can every carpet stain be removed?", "Many can, but some, like bleach spots or dye stains, are permanent and need patching or replacement."),
  ("Should carpet spotters be tested first?", "Yes, on a hidden area, to check for color loss or texture change.")]),
}
