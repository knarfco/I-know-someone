def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Rust stain removal from concrete": dict(
 w=["Strong acids can etch and discolor concrete; test first.", "Deep rust stains in porous concrete may not come out completely."],
 q=[("What causes rust stains on new concrete?", "Steel materials, rebar, tools or fertilizer left on the slab, and iron-rich irrigation water on exterior concrete."),
  ("Can rust stains be removed from concrete?", "Usually, with rust removers formulated for concrete, applied carefully and rinsed well."),
  ("Do rust removers damage concrete?", "Strong acid-based removers can etch the surface, so products made for concrete are tested first."),
  ("How can rust stains on concrete be prevented?", "By keeping steel off finished concrete and redirecting sprinklers that use iron-rich water.")]),
"Paint and coating drip removal from concrete": dict(
 y="Drips on exposed concrete look unfinished, and on polished or stained concrete they are very visible. Under future flooring, they cause bumps and adhesion problems.",
 q=[("How do you remove paint drips from a concrete floor?", "Scrape carefully with a floor scraper and use removers suited to the paint type and the floor's finish, tested first."),
  ("Can epoxy drips be removed from concrete?", "Yes, but cured epoxy is tough and often needs careful scraping or light grinding."),
  ("Who is responsible for paint drips on concrete floors?", "Usually the painter, under their protection obligations, although cleaning crews often remove them at final clean."),
  ("Do paint drips matter if the floor will be covered?", "Yes. Drips under flooring create bumps and can prevent adhesives from bonding.")]),
"Joint and crack debris vacuuming": dict(
 y="Debris in control joints keeps releasing dust long after cleaning and prevents joint fillers and sealants from bonding properly.",
 q=[("Why clean concrete control joints?", "Debris in joints keeps releasing dust and prevents joint fillers from bonding to the joint walls."),
  ("What is a concrete control joint?", "A planned groove or cut in a slab that controls where cracks form as the concrete shrinks."),
  ("How are concrete joints cleaned?", "With crevice tools and HEPA vacuums, sometimes after blowing debris loose in controlled conditions."),
  ("When is joint cleaning done?", "Before joints are filled and before the final floor clean.")]),
"Densifier and guard application support": dict(q=[
  ("What is a concrete guard?", "A topical protective treatment applied to polished concrete to resist stains and improve shine."),
  ("Why must the floor be cleaned before densifier is applied?", "Dirt and residue block absorption and cause uneven, blotchy results."),
  ("Who applies concrete densifier and guard?", "Usually the flooring or concrete polishing contractor, with cleaning support before and after."),
  ("Can densifier residue be removed?", "Usually, if it is addressed promptly before it hardens on the surface.")]),
"Epoxy floor preparation cleaning": dict(
 a="Epoxy floor preparation cleaning removes dust, oil, grease and contaminants from concrete slabs before epoxy, urethane or other resinous coatings are applied, so the coating bonds properly.",
 q=[("Why is surface preparation so important for epoxy floors?", "Epoxy only bonds to clean, sound concrete. Dust, oil and residues are the main causes of coating failure."),
  ("What contaminants cause epoxy floors to fail?", "Dust, oil, grease, curing compounds, old sealers and moisture coming up through the slab."),
  ("Who prepares concrete floors for epoxy coatings?", "The coating contractor is responsible for preparation, often with cleaning support beforehand."),
  ("Can epoxy be applied over sealed concrete?", "Usually only after the sealer is removed by grinding or blasting.")]),
}
