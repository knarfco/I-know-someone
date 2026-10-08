def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Concrete grinding preparation": dict(q=[
  ("Why is concrete ground before coatings are applied?", "Grinding removes weak surface material, old coatings and contaminants and creates a texture the new coating can bond to."),
  ("Does concrete grinding create silica dust?", "Yes. Grinding concrete releases respirable crystalline silica, so dust collection or wet methods are required."),
  ("Who grinds concrete floors?", "Flooring, coating or concrete polishing contractors with specialized grinders and dust collectors."),
  ("Is concrete grinding a cleaning task?", "No. It is surface preparation. Cleaning crews remove the remaining dust and residue afterward.")]),
"Curing compound residue removal": dict(
 y="Curing compound residue can block flooring adhesives and coatings, causing flooring failures, and it looks patchy and uneven on exposed or polished concrete.",
 q=[("What is a concrete curing compound?", "A liquid sprayed on fresh concrete to slow evaporation so the concrete cures properly."),
  ("Why does curing compound need to be removed?", "It can stop flooring adhesives and coatings from bonding and leaves patchy color on exposed concrete."),
  ("How is curing compound removed from concrete?", "With chemical strippers and scrubbing, or by grinding when the compound is stubborn or a coating will follow."),
  ("Does every curing compound need to be removed?", "No. Some are compatible with certain floor finishes. The flooring or coating manufacturer decides.")]),
"Tire mark and forklift mark removal": dict(q=[
  ("How are forklift tire marks removed from concrete?", "With a cleaner made for rubber marks and a scrubbing pad matched to the floor finish, tested first on sealed or polished concrete."),
  ("Do non-marking tires prevent floor marks?", "They greatly reduce them, which is why many owners require them on lifts used over finished floors."),
  ("Can tire marks be removed from polished concrete?", "Usually yes, with gentle cleaners and maintenance pads that will not dull the polish."),
  ("Who removes tire marks at the end of construction?", "The cleaning crew during the final floor clean.")]),
"Concrete stain and oil spot treatment": dict(
 a="Concrete stain and oil spot treatment removes oil, grease, hydraulic fluid, food and other stains from concrete floors and slabs using absorbents, degreasers and poultices suited to the stain and floor finish.",
 w=["Some old or deep stains will lighten but not fully disappear.", "Degreaser rinse water must not go to storm drains."],
 q=[("How are oil stains removed from concrete floors?", "Fresh spills are absorbed first, then degreasers and poultices draw the oil out of the pores, followed by scrubbing and rinsing."),
  ("Can old oil stains be removed from concrete?", "Often partly. Oil that has soaked in for months may only lighten, especially on unsealed concrete."),
  ("What is a poultice for concrete stains?", "A paste of absorbent material and cleaner that pulls stains out of porous concrete as it dries."),
  ("Are oil stains on concrete a safety concern?", "Yes, they can be slippery, especially when wet.")]),
"Concrete efflorescence removal": dict(
 y="Efflorescence looks like white haze or powder on new concrete and makes floors and walls look stained. It comes back if the moisture source is not addressed, and the wrong cleaner can etch or discolor the concrete.",
 q=[("What causes efflorescence on concrete?", "Water moving through the concrete carries dissolved salts to the surface, where they remain as white deposits when the water evaporates."),
  ("Will efflorescence come back after cleaning?", "It can if moisture keeps moving through the concrete. New slabs often stop once they dry out."),
  ("How is efflorescence removed from concrete floors?", "Dry brushing and vacuuming first, then efflorescence cleaners tested on the surface if needed."),
  ("Is efflorescence harmful to concrete?", "It is mostly cosmetic, but it signals moisture movement that can affect floor coverings.")]),
}
