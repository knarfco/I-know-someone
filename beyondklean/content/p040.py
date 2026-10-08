def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Toilet and urinal detailing": dict(q=[
  ("How are new toilets and urinals cleaned after construction?", "Labels and residue are removed, then fixtures are cleaned inside and out with non-acidic products safe for vitreous china and chrome, including bases, bolt caps and flush valves."),
  ("Why avoid acid bowl cleaners in a new restroom?", "Acids can damage chrome flush valves, etch some grouts and stone, and are rarely needed on new fixtures."),
  ("Do inspectors look behind toilets during an owner walk?", "Many do. Behind and under fixtures is where dust, grout and caulk residue are often missed."),
  ("Who cleans new restroom fixtures before turnover?", "The cleaning crew during the final clean, with a touch-up before the owner walk.")]),
"Sink and faucet detailing": dict(
 a="Sink and faucet detailing cleans lavatories, faucets, drains, overflows, counters around sinks and the space under each sink, removing labels, film, residue and water spots from new fixtures.",
 w=["Abrasive pads scratch chrome, brushed nickel and specialty finishes.", "Faucets and sensors should not be disassembled or adjusted."],
 q=[("How do you clean new faucets without damaging the finish?", "With non-abrasive cleaners made for the finish and soft cloths, then dry to prevent water spots."),
  ("Why are new faucets spotty right after installation?", "Water spots from plumbing tests dry on the finish and show as white marks."),
  ("Are the areas under sinks cleaned?", "Yes. Under-sink areas collect debris and packaging, and inspectors often look there."),
  ("Are specialty faucet finishes cleaned differently?", "Yes. Matte black, brushed gold and similar finishes need manufacturer-approved, gentle cleaners.")]),
"Restroom fixture sticker and label removal": dict(
 a="Restroom fixture sticker and label removal takes manufacturer labels, barcodes and adhesive off toilets, urinals, sinks, accessories and partitions without scratching vitreous china, chrome or powder-coated finishes.",
 w=["Razor blades can scratch glazed china and plated finishes.", "Solvents can damage plastic seats and partition finishes."],
 q=[("How are labels removed from new toilets and sinks?", "Peel the label slowly, then remove adhesive with a remover safe for vitreous china and chrome, wiping clean afterward."),
  ("Can razor blades be used to remove fixture labels?", "They can scratch glazes and plated finishes, so plastic scrapers and removers are preferred."),
  ("Why are fixture labels such a common punch item?", "Every fixture ships with labels, and inspectors notice any that remain."),
  ("Should fixture model information be kept?", "Ask the GC; model and warranty information may be needed for closeout, so it is often photographed before removal.")]),
"Caulk smear and silicone haze removal": dict(
 a="Caulk smear and silicone haze removal takes thin films and smears of silicone and sealant off counters, tubs, tile, glass and fixtures around new caulk joints, without cutting into the joint itself.",
 q=[("What is silicone haze?", "A thin, often invisible film of silicone left on surfaces around a caulk joint. It attracts dirt and looks smeary once grime collects."),
  ("How is silicone haze removed from tile and fixtures?", "With silicone-specific removers and plastic scrapers, working carefully away from the joint."),
  ("Can caulk smears be removed without damaging the joint?", "Yes, by working away from the bead and never cutting into it, which could cause leaks."),
  ("Who removes caulk smears at the end of construction?", "The installer should, but cleaning crews often remove remaining smears at final clean.")]),
"Shower and tub detailing": dict(
 a="Shower and tub detailing cleans new showers and tubs, including valves, heads, drains, tile walls, grout, glass and caulk lines, removing grout haze, caulk smears, labels and construction debris.",
 w=["Acrylic and fiberglass tubs scratch easily with abrasives.", "Acidic cleaners damage stone and some grouts."],
 q=[("How are new showers cleaned after construction?", "Grout haze and residue are removed with compatible products, fixtures and drains are detailed, and glass and walls are cleaned and dried."),
  ("Can acrylic tubs be scratched during cleaning?", "Yes, so only soft cloths and non-abrasive cleaners are used."),
  ("Why do new shower drains need cleaning?", "Grout, thinset and debris from tile work collect in them."),
  ("Are showers part of hotel renovation cleaning?", "Yes, they are among the most closely inspected items in a guest room.")]),
}
