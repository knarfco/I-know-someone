def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Grout haze removal": dict(q=[
  ("What is grout haze?", "A thin, cloudy film of cement-based grout left on the face of tile after grouting. It makes new tile look dull and dirty."),
  ("How do you remove grout haze from new tile?", "With a haze remover matched to the tile, stone and grout type, applied with soft pads and rinsed thoroughly."),
  ("Can vinegar remove grout haze?", "Vinegar is acidic and can etch marble, limestone and travertine and weaken some grouts, so it is not a safe general method."),
  ("When should grout haze be removed?", "After the grout has cured enough not to be damaged, but before the haze hardens completely, usually within the first days to weeks.")]),
"Grout line deep cleaning": dict(
 a="Grout line deep cleaning scrubs the joints between tiles to remove embedded soil, residue and staining, restoring grout to its original color before turnover or sealing.",
 w=["Harsh acids weaken cementitious grout.", "Unsealed grout re-soils quickly after cleaning."],
 q=[("How is dirty grout cleaned?", "With grout brushes or machines and cleaners suited to the grout, followed by extraction or rinsing."),
  ("Can grout be restored to its original color?", "Deep cleaning often restores it; grout colorant is an option for stains that will not lift."),
  ("Why does grout get dirty so fast?", "Cementitious grout is porous and absorbs dirt and spills."),
  ("Should grout be sealed after deep cleaning?", "Often yes, to slow re-soiling, once the grout is completely dry.")]),
"Grout sealing": dict(
 a="Grout sealing applies a penetrating sealer to clean, dry cementitious grout joints so they resist staining and moisture and are easier to clean, typically after the tile's initial clean.",
 y="Unsealed grout absorbs spills, grease and dirt and darkens quickly, especially in restrooms, kitchens and entries.",
 q=[("Should grout be sealed in commercial buildings?", "Cementitious grout usually benefits from sealing, especially in restrooms, kitchens and entries."),
  ("When can new grout be sealed?", "After it fully cures and is clean and dry, according to the grout and sealer manufacturers."),
  ("How long does grout sealer last?", "It varies by product and traffic, often one to a few years before resealing."),
  ("Does epoxy grout need sealing?", "Usually not, because epoxy grout is non-porous.")]),
"Quarry tile cleaning": dict(
 a="Quarry tile cleaning cleans and degreases unglazed quarry tile floors in commercial kitchens and food areas, removing construction dust, grout haze and grease so floors are clean and slip-resistant for health inspection.",
 w=["Grease left on quarry tile makes floors dangerously slippery.", "Some strong degreasers and acids damage grout."],
 q=[("What is quarry tile?", "A dense, unglazed clay tile used in commercial kitchens because it is durable and slip-resistant."),
  ("How are quarry tile floors degreased?", "With kitchen degreasers, deck brushes or floor machines, then rinsed and squeegeed to the floor drains."),
  ("Should quarry tile be sealed?", "Often yes, to help resist grease and staining, following the tile manufacturer's guidance."),
  ("Why is quarry tile used in commercial kitchens?", "It handles heavy traffic, heat and water and stays slip-resistant.")]),
"Natural stone floor initial clean": dict(
 a="Natural stone floor initial clean cleans newly installed marble, limestone, travertine, granite and slate floors with stone-safe, pH-neutral products and coordinates with sealing.",
 w=["Acids etch marble, limestone and travertine.", "Unsealed stone absorbs stains from spills and residue."],
 q=[("How are new marble floors cleaned?", "With pH-neutral stone cleaners and soft pads, never acidic or harsh alkaline products."),
  ("Can grout haze be removed from marble?", "Only with non-acidic haze removers made for calcareous stone."),
  ("Should natural stone floors be sealed?", "Many should, especially porous stones, according to the installer and stone supplier."),
  ("Who repairs etched or scratched stone?", "Stone restoration specialists, who hone and polish the surface.")]),
}
