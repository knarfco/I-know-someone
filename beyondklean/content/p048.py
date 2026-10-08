def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Static-dissipative floor cleaning": dict(
 y="Static-control floors protect sensitive electronics from static discharge. Wax and residue-forming cleaners can insulate the surface and stop the floor from working.",
 w=["Wax and residue-leaving cleaners can block static dissipation.", "Only manufacturer-approved cleaners should be used."],
 q=[("What is a static-dissipative floor?", "A floor designed to safely drain static electricity to ground, protecting sensitive electronics."),
  ("Can ESD floors be waxed?", "Usually not, unless a special conductive or dissipative finish is specified by the manufacturer."),
  ("Where are static-dissipative floors used?", "In electronics manufacturing, labs, data centers, hospital imaging rooms and control rooms."),
  ("How is static-dissipative floor performance checked?", "With electrical resistance testing according to the manufacturer and project specifications.")]),
"Adhesive residue removal from resilient floors": dict(q=[
  ("How do you remove flooring adhesive from the face of vinyl tile?", "With the adhesive manufacturer's recommended remover or a mild option, tested first, using soft pads and wiping clean afterward."),
  ("Why does flooring adhesive turn black on new floors?", "Sticky adhesive left on the surface traps dirt from foot traffic within days."),
  ("Who is responsible for adhesive on new resilient floors?", "The installer should clean adhesive as they work, but cleaning crews often remove the rest at final clean."),
  ("Can cured flooring adhesive still be removed?", "It is harder, but often possible with the right remover and patience.")]),
"Scuff and heel mark removal": dict(
 y="Scuffs from carts, ladders and shoes appear during the last weeks of construction and stand out on new floors during the owner walk.",
 w=["Aggressive pads and solvents can damage floor finish.", "Deep scuffs through the finish may need recoating."],
 q=[("How are scuff marks removed from new floors?", "With soft pads, a tennis-ball tool or a mild cleaner, followed by light buffing on finished floors."),
  ("Do scuff marks damage floor finish?", "Light scuffs sit on the surface; heavy scuffs can cut into the finish and need recoating."),
  ("Why are new floors scuffed at the end of construction?", "Carts, ladders, furniture moves and shoes all mark floors in the final weeks."),
  ("Is scuff removal part of the final clean?", "Yes, it is a standard final floor clean item.")]),
"Burnishing": dict(
 a="Burnishing polishes finished resilient floors, such as VCT with floor finish, using a high-speed machine to restore gloss and a wet look between scrub-and-recoat and strip cycles.",
 q=[("What is burnishing a floor?", "Polishing floor finish with a high-speed machine and pad to restore gloss."),
  ("How often should floors be burnished?", "It depends on traffic, from daily in busy retail to monthly in low-traffic areas."),
  ("Can luxury vinyl tile be burnished?", "Only if the manufacturer allows it; many LVT products should not be."),
  ("Does burnishing create dust?", "It can, so dust-control burnishers and a clean floor beforehand are recommended.")]),
"Ceramic and porcelain tile initial clean": dict(q=[
  ("How are new ceramic and porcelain tile floors cleaned?", "Grout haze and residue are removed first with compatible products, then the floor is cleaned with a neutral cleaner and rinsed."),
  ("Is porcelain tile easy to clean after construction?", "Smooth porcelain is easy, but textured and matte porcelain holds residue and needs brush scrubbing."),
  ("Can acidic cleaners be used on new tile?", "Only if both the tile and the grout can tolerate them; many grouts and stone accents cannot."),
  ("How soon can new tile be cleaned?", "After the grout has cured enough per the grout manufacturer, usually at least a day or more.")]),
}
