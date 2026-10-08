def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Return grille temporary filter media change": dict(
 a="Return grille temporary filter media change replaces the temporary filter material placed over return air grilles and openings when a building's HVAC system runs during construction, so construction dust does not reach ducts and coils.",
 q=[("Why are temporary filters put on return grilles during construction?", "When the HVAC runs during construction, return grilles pull dust into the system. Temporary filter media catches it before it reaches ducts and coils."),
  ("How often should temporary return filters be changed?", "Whenever they are visibly loaded or on a set schedule during dusty phases. Loaded filters reduce airflow and stop protecting the system."),
  ("What filter rating is used over return grilles?", "Many projects specify MERV 8 or higher for temporary filtration, following SMACNA and LEED guidance."),
  ("Who changes temporary HVAC filters during construction?", "The mechanical contractor or a cleaning crew assigned by the GC, with used media bagged carefully.")]),
"Final HVAC filter replacement coordination": dict(
 a="Final HVAC filter replacement coordination schedules the change from construction-period filters to new permanent filters after the final clean and before occupancy, so the owner starts with clean filtration.",
 q=[("When should HVAC filters be replaced at the end of construction?", "After the final clean and any flush-out preparation, and before the building is occupied."),
  ("Why replace HVAC filters before occupancy?", "Filters used during construction are loaded with dust and reduce airflow and air quality."),
  ("Who replaces HVAC filters at turnover?", "The mechanical contractor, coordinated with the cleaning schedule so filters are not changed too early."),
  ("Do green building standards require new filters?", "LEED construction IAQ requirements typically call for new filtration media before occupancy.")]),
"Pre-flush-out final cleaning": T(
 "Pre-flush-out final cleaning completes the building's final clean before the HVAC flush-out begins, so construction dust is removed from surfaces before large volumes of air are circulated through the building.",
 "A flush-out moves large volumes of outdoor air through the building to dilute contaminants from new finishes. If surfaces are still dusty, the flush-out spreads that dust into the HVAC system and finished rooms.",
 "Crews schedule the final clean so it finishes before flush-out starts, coordinating with the commissioning agent, mechanical contractor and filter changes.",
 ["Flush-out start date", "Final cleaning completion", "Filter change timing", "Commissioning coordination"],
 ["Starting flush-out before cleaning spreads dust through the system.", "Late trades after cleaning can re-contaminate the building."],
 [("What is a building flush-out?", "Running the HVAC system with outdoor air for a set period after construction to dilute contaminants from new finishes, often for green building credits."),
  ("Why clean before a building flush-out?", "Dust left on surfaces is stirred up and carried through the HVAC system and into finished rooms."),
  ("Who schedules the flush-out?", "The GC and commissioning agent, coordinated with the mechanical contractor."),
  ("Is a flush-out required on every project?", "No. It is common on LEED and other green building projects that pursue indoor air quality credits.")]),
"Construction IAQ photo documentation": dict(
 a="Construction IAQ photo documentation records duct protection, temporary filtration, housekeeping and cleaning with dated, located photos, organized for green building submissions and the owner's records.",
 w=["Missing or undated photos can cost the green building credit.", "Photos need to show the same measures on multiple dates."],
 q=[("Why do green building projects need IAQ photos?", "Certification reviewers require proof that construction indoor air quality measures were followed, and dated photos are the standard proof."),
  ("How many dates of IAQ photos are typically required?", "LEED IAQ documentation has commonly asked for photos on at least three separate dates during construction."),
  ("What do construction IAQ photos show?", "Capped ducts, temporary filters, protected materials, housekeeping and final cleaning."),
  ("Who submits IAQ documentation?", "The GC or the project's LEED consultant, using photos gathered by the team.")]),
"Low-VOC product log for cleaning materials": T(
 "A low-VOC product log for cleaning materials lists every cleaning product used on the project with its Safety Data Sheet, technical data and VOC content, for green building documentation and the owner's records.",
 "Green building projects and health-focused owners want to know what chemicals were used in their building. A log also supports the project's indoor air quality plan.",
 "The cleaning contractor records each product, collects current data sheets, notes VOC content and updates the log whenever a product is substituted.",
 ["Products used", "SDS and technical data", "VOC content", "Substitutions"],
 ["Product substitutions must be logged to keep the record accurate.", "Outdated data sheets do not satisfy documentation requirements."],
 [("What is a VOC?", "A volatile organic compound: a chemical that evaporates at room temperature and can affect indoor air quality."),
  ("Why keep a log of cleaning products used during construction?", "It documents what chemicals were used in the building for green building credits, safety and the owner's records."),
  ("What information goes in a cleaning product log?", "Product name, manufacturer, SDS, technical data, VOC content and where the product was used."),
  ("Who keeps the cleaning product log?", "The cleaning contractor maintains it and delivers it at closeout.")]),
}
