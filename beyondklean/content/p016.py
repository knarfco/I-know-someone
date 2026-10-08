def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Paint drip and splatter removal": dict(
 a="Paint drip and splatter removal takes larger dried drops and splatters of latex, oil or epoxy paint off floors, counters, fixtures, glass, hardware and trim at final clean, without damaging the finish underneath.",
 q=[("How do you remove dried latex paint drips from a hard floor?", "Soften the drip with warm water or a latex paint remover, lift it with a plastic scraper, then clean the residue. Metal scrapers are avoided on resilient and wood floors because they gouge."),
  ("Can paint drips be removed from carpet?", "Often, especially latex paint treated before it fully cures. A spotter made for latex paint is worked in by blotting, never rubbing, and the area is rinsed."),
  ("Can paint be removed from quartz or granite countertops?", "Yes, carefully, with plastic blades and removers compatible with the stone or quartz, tested first. Strong solvents and acids can dull or etch the surface."),
  ("How can paint drips be prevented on new finishes?", "With drop cloths, floor protection and covering counters and fixtures before painting. Protection costs far less than removal and repair.")]),
"Adhesive residue removal": dict(
 a="Adhesive residue removal takes sticky residue from tape, labels, protective films, mastics and glues off finished surfaces such as glass, counters, floors, appliances and walls, using the gentlest remover that works on each surface.",
 q=[("What removes sticky residue without damaging new surfaces?", "Start with mild citrus or plant-based adhesive removers and plastic scrapers, tested on a hidden spot. Stronger solvents are used only where the surface can tolerate them."),
  ("Why does adhesive residue turn black?", "The sticky film traps dust and dirt from the air and from foot traffic. Within days it becomes a dark, obvious spot."),
  ("Does heat help remove adhesive residue?", "Gentle warming with a heat gun on low or warm water softens many adhesives so they lift more easily. Heat is kept away from plastics and fresh paint."),
  ("Do adhesive removers need to be cleaned off afterward?", "Yes. Remover residue left on a surface attracts dirt and can affect finishes, so the area is cleaned with a neutral cleaner and wiped dry.")]),
"Tape residue removal": dict(
 a="Tape residue removal cleans the adhesive left by painter's tape, duct tape, carpet tape and masking tape used during construction, from walls, floors, glass, frames and fixtures, without pulling paint or damaging finishes.",
 q=[("Why does painter's tape leave residue?", "Painter's tape is designed for short use. Left on for weeks, especially in sun or heat, its adhesive bonds to the surface and stays behind when the tape is removed."),
  ("How should old tape be removed from walls?", "Slowly, pulling back at a low angle close to the surface. Pulling fast or straight out can lift fresh paint with the tape."),
  ("How is duct tape residue removed from floors?", "With an adhesive remover compatible with the floor type, tested first, then a neutral cleaner rinse. Duct tape residue is stubborn and may need more than one pass.")]),
"Stucco and plaster splatter removal": T(
 "Stucco and plaster splatter removal takes hardened stucco, plaster, texture and skim-coat splatter off windows, frames, floors, fixtures and exterior surfaces near plastering work.",
 "Stucco and plaster bond tightly to glass and metal and contain sand that scratches surfaces when scraped dry. Splatter is common on windows and frames next to exterior stucco work.",
 "Crews soak splatter with water to soften it, lift it with plastic tools or lubricated blades on suitable glass, and rinse thoroughly so no grit is dragged across the surface.",
 ["Surfaces affected and their materials", "Extent and age of splatter", "Glass type and coatings", "Rinse water control"],
 ["Dry scraping drags sand across glass and causes scratches.", "Acidic cleaners can etch glass and damage aluminum frames."],
 [("How do you remove stucco from windows without scratching them?", "Soak the splatter until it softens, then lift it with a lubricated blade on glass that allows scraping, rinsing often so sand is not dragged across the pane."),
  ("Why does stucco scratch glass?", "Stucco contains sand. Scraping it dry drags those particles across the glass like sandpaper."),
  ("Who is responsible for stucco splatter on windows?", "Usually the stucco contractor under their protection obligations, though the cleaning crew often removes it at final clean."),
  ("Is plaster easier to remove than stucco?", "Often yes, because interior plaster softens with water more readily than cement-based stucco.")]),
"Concrete and mortar splatter removal": T(
 "Concrete and mortar splatter removal takes hardened cement-based splatter off floors, walls, frames, fixtures and hardscape throughout a project, using soaking, mechanical removal and tested cement removers.",
 "Cement bonds tightly to almost every surface and is alkaline. The acidic removers that dissolve it can also etch stone, burn aluminum and damage glass coatings if used carelessly.",
 "Crews soak and mechanically remove as much as possible first, then use cement removers only after testing, protecting nearby surfaces and rinsing thoroughly.",
 ["Surfaces and extent of splatter", "Remover testing location", "Protection of adjacent surfaces", "Rinse and disposal"],
 ["Acidic removers can etch stone, metal and glass.", "Remover left to dry on a surface causes new stains."],
 [("How do you remove dried cement splatter from finished surfaces?", "Soak it, remove what you can mechanically with plastic or appropriate tools, then use a tested cement remover only where needed and rinse thoroughly."),
  ("Can concrete removers damage surfaces?", "Yes. Many are acidic and can etch marble, burn aluminum and stain metal, so testing and rinsing are essential."),
  ("Is mortar removed the same way as concrete?", "Yes, both are cement-based, so the same soak, scrape and tested-remover approach applies."),
  ("Who removes mortar and concrete splatter at the end of a project?", "The mason or concrete contractor is often responsible, but cleaning crews frequently remove remaining splatter at final clean.")]),
}
