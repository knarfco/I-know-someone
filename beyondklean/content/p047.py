def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"LVT and LVP manufacturer-approved cleaning": dict(q=[
  ("Can luxury vinyl tile be waxed?", "Most LVT and LVP products are designed to be maintained without wax or floor finish. Applying it can void the warranty, so the manufacturer's guide controls."),
  ("What cleaner is safe for LVT floors?", "A pH-neutral cleaner approved by the flooring manufacturer, used with microfiber or a soft pad."),
  ("Can cleaning void a luxury vinyl floor warranty?", "Yes. Unapproved strippers, finishes, steam or harsh chemicals can void it."),
  ("What is the difference between LVT and LVP?", "LVT is luxury vinyl tile in square or rectangular tiles; LVP is the plank format that imitates wood boards.")]),
"Sheet vinyl initial clean": dict(
 a="Sheet vinyl initial clean cleans newly installed sheet vinyl flooring in healthcare, food service and education spaces, removing adhesive, seam sealer residue and construction dust and following the manufacturer's initial maintenance.",
 w=["Solvents can soften heat-welded or chemically welded seams.", "Some sheet vinyls are designed to be used with no floor finish."],
 q=[("How is new sheet vinyl cleaned after installation?", "Adhesive and seam residue are removed with approved products, then the floor is scrubbed with a neutral cleaner and rinsed."),
  ("Does sheet vinyl need floor finish?", "It depends on the product. Many modern sheet vinyls have factory coatings and need no finish."),
  ("Where is sheet vinyl flooring used?", "In healthcare, schools, labs and food areas where seamless, cleanable floors are needed."),
  ("Can cleaning damage sheet vinyl seams?", "Yes, solvents and aggressive scrubbing can damage welded seams.")]),
"Rubber floor initial cleaning": dict(
 w=["Solvents and oily cleaners damage rubber and make it slippery.", "Some rubber floors should never receive floor finish."],
 q=[("Why does new rubber flooring look blotchy?", "Rubber floors often have factory release agents and installation residue that need an initial cleaning to even out the appearance."),
  ("Can rubber floors be waxed?", "Follow the manufacturer. Many rubber floors are designed to be maintained without finish."),
  ("What cleaner is safe for rubber flooring?", "A pH-neutral cleaner recommended by the rubber flooring manufacturer."),
  ("Where are rubber floors commonly used?", "In healthcare, schools, gyms, labs and stair treads, because they are durable and comfortable.")]),
"Sports and gym floor rubber cleaning": dict(
 m="Crews vacuum the textured surface, then scrub with neutral cleaners approved by the flooring manufacturer, rinse and dry, avoiding oily products that make rubber slippery.",
 q=[("How are rubber gym floors cleaned after construction?", "Vacuumed to remove grit and dust, then scrubbed with neutral, manufacturer-approved cleaners and rinsed."),
  ("Why do rubber gym floors get slippery?", "Oily or residue-leaving cleaners make rubber slick, which is dangerous during workouts."),
  ("Are rubber gym floors cleaned before equipment is installed?", "Ideally yes, so the floor under heavy equipment is clean."),
  ("Do rubber athletic floors need a finish?", "Usually not. Most are maintained with cleaning alone.")]),
"Linoleum and marmoleum initial care": dict(
 w=["High-pH cleaners and strippers can damage linoleum.", "Excess water at seams can affect the backing."],
 q=[("Is linoleum the same as vinyl flooring?", "No. Linoleum is made from natural materials like linseed oil, wood flour and jute, while vinyl is a plastic."),
  ("What cleaner is safe for linoleum floors?", "A pH-neutral cleaner recommended by the linoleum manufacturer."),
  ("Why avoid strong alkaline cleaners on linoleum?", "High-pH products can damage the linseed binder and dull or discolor the surface."),
  ("Does new linoleum need a floor finish?", "Follow the manufacturer; many products have factory finishes and specific initial maintenance steps.")]),
}
