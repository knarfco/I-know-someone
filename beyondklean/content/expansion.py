"""Service directory expansion: four new primary categories (21-24), new services added to existing
families, and new names merged into existing services as aliases.

Rows: (task, family, group, phase, tier, aliases). Group-level why / method strings follow in GROUPS.
Content for each task lives in content/f21.py ... f25.py; family intros and FAQs in content/fam_x.py.
"""

NEW_FAMILIES = [
    "Post-Demolition & Reconstruction Cleaning",
    "Industrial & Technical Commissioning Cleaning",
    "Infrastructure & Transportation Cleaning",
    "Government, Military & Defense Facility Cleaning",
]

C, SP, CR = "Core", "Adjacent specialist", "Conditional / regulated"
ANY, RO, FI, TU, OC = "Any stage / specialty", "Rough", "Final", "Touch-up / punch", "Occupancy / turnover"

D21, D22, D23, D24 = NEW_FAMILIES

TASKS = [
    # 21. Post-Demolition & Reconstruction
    ("Selective demolition cleanup", D21, "Demolition cleanup", RO, C, "selective demo cleanup; partial demolition cleanup"),
    ("Interior gut-out cleanup", D21, "Demolition cleanup", RO, C, "gut job cleanup; interior strip-out cleanup; tear-out cleanup"),
    ("Post-demolition dust and debris removal", D21, "Demolition cleanup", RO, C, "demo dust cleanup; after-demo cleaning"),
    ("Fire and flood reconstruction cleanup", D21, "Disaster reconstruction", ANY, SP, "fire rebuild cleanup; flood rebuild cleanup; reconstruction cleaning after fire or flood"),
    ("Hurricane and storm reconstruction cleanup", D21, "Disaster reconstruction", ANY, SP, "hurricane rebuild cleanup; storm damage reconstruction cleaning"),
    ("Post-abatement cleaning", D21, "Regulated and historic work", ANY, CR, "after abatement cleaning; post-abatement clean"),
    ("Historic building restoration cleanup", D21, "Regulated and historic work", ANY, SP, "historic renovation cleanup; preservation project cleaning"),
    # 22. Industrial & Technical Commissioning
    ("Pre-commissioning facility cleaning", D22, "Commissioning and startup", FI, SP, "commissioning clean; pre-startup cleaning"),
    ("Production line and machinery cleaning", D22, "Commissioning and startup", FI, SP, "machinery cleaning after install; production equipment cleaning"),
    ("Abrasive blasting residue cleanup", D22, "Commissioning and startup", ANY, SP, "sandblast cleanup; blast media cleanup; media blasting residue removal"),
    ("Semiconductor facility final cleaning", D22, "Advanced manufacturing", FI, SP, "fab cleaning; semiconductor fab final clean"),
    ("Pharmaceutical and biotechnology facility cleaning", D22, "Advanced manufacturing", FI, SP, "pharma facility cleaning; biotech lab construction cleaning; GMP facility cleaning"),
    ("Battery energy storage facility cleaning", D22, "Energy facilities", FI, SP, "BESS cleaning; battery storage installation cleanup; battery plant cleaning"),
    ("Solar installation construction cleanup", D22, "Energy facilities", FI, C, "solar farm construction cleanup; solar project cleanup"),
    ("Renewable energy facility turnover cleaning", D22, "Energy facilities", OC, C, "wind and solar facility turnover; renewable plant final clean"),
    # 23. Infrastructure & Transportation
    ("Airport and terminal construction cleaning", D23, "Aviation and transit", FI, SP, "airport terminal cleaning; airport construction cleanup"),
    ("Railway and transit station cleaning", D23, "Aviation and transit", FI, SP, "train station construction cleaning; transit station final clean"),
    ("Cruise terminal construction cleanup", D23, "Aviation and transit", FI, C, "port terminal cleaning; cruise port construction cleaning"),
    ("Parking garage construction cleanup", D23, "Parking and vehicles", FI, C, "parking structure cleaning; new garage cleanup"),
    ("EV charging facility construction cleaning", D23, "Parking and vehicles", FI, C, "EV charger site cleanup; charging station construction cleaning"),
    ("Transportation maintenance facility cleaning", D23, "Parking and vehicles", FI, C, "bus garage cleaning; fleet maintenance facility cleaning"),
    ("Marine and marina construction cleaning", D23, "Marine and public works", FI, SP, "marina cleanup; dock construction cleaning"),
    ("Public infrastructure project cleaning", D23, "Marine and public works", ANY, C, "public works construction cleaning; municipal infrastructure cleanup"),
    # 24. Government, Military & Defense
    ("Federal government building construction cleaning", D24, "Federal, state and municipal", FI, C, "federal building cleaning; GSA building construction cleaning"),
    ("State and municipal government facility cleaning", D24, "Federal, state and municipal", FI, C, "city hall cleaning; county building construction cleaning"),
    ("Federal courthouse and administrative building cleaning", D24, "Federal, state and municipal", FI, C, "courthouse construction cleaning; administrative building final clean"),
    ("Police, fire and emergency services facility cleaning", D24, "Federal, state and municipal", FI, C, "fire station construction cleaning; police station cleaning; EMS station cleaning"),
    ("Correctional and detention facility cleaning", D24, "Federal, state and municipal", FI, SP, "jail construction cleaning; prison cleaning; detention center cleaning"),
    ("Disaster response and emergency operations facility cleaning", D24, "Federal, state and municipal", ANY, SP, "EOC cleaning; emergency operations center cleaning"),
    ("Government building decommissioning cleanup", D24, "Federal, state and municipal", ANY, SP, "decommissioning cleaning; facility closeout cleaning"),
    ("Government historic preservation project cleaning", D24, "Federal, state and municipal", ANY, SP, "historic government building cleaning; landmark restoration cleanup"),
    ("Government infrastructure construction cleanup", D24, "Federal, state and municipal", ANY, C, "public infrastructure construction cleanup; government construction site cleanup"),
    ("Military base construction and renovation cleaning", D24, "Military installations", FI, SP,
     "military installation cleaning; Army base cleaning; Navy base cleaning; Air Force base cleaning; Marine Corps base cleaning; Space Force facility cleaning; Coast Guard station cleaning; DoD facility construction cleaning"),
    ("Military barracks and housing turnover cleaning", D24, "Military installations", OC, C, "barracks cleaning; military housing turnover; dormitory turnover on base"),
    ("Military hangar and aircraft maintenance facility cleaning", D24, "Military installations", FI, SP, "hangar cleaning; aircraft maintenance hangar construction cleaning"),
    ("Naval shipyard and dockside facility cleaning", D24, "Military installations", ANY, SP, "shipyard facility cleaning; dockside building cleaning"),
    ("Military vehicle maintenance facility cleaning", D24, "Military installations", FI, C, "motor pool cleaning; vehicle maintenance bay cleaning"),
    ("Military training and simulation facility cleaning", D24, "Military installations", FI, SP, "simulator facility cleaning; training center cleaning"),
    ("Military warehouse and logistics facility cleaning", D24, "Military installations", FI, C, "military warehouse cleaning; logistics center cleaning"),
    ("Military installation environmental cleaning", D24, "Military installations", ANY, CR, "environmental cleanup on base; installation environmental cleaning"),
    ("Defense contractor manufacturing facility cleaning", D24, "Secure, research and medical", FI, SP, "defense manufacturing cleaning; aerospace and defense plant cleaning"),
    ("Government research laboratory cleaning", D24, "Secure, research and medical", FI, SP, "federal lab cleaning; national lab construction cleaning"),
    ("Secure and restricted-access facility cleaning", D24, "Secure, research and medical", ANY, SP, "secure facility cleaning; restricted area cleaning; SCIF construction cleaning"),
    ("Government data center and communications facility cleaning", D24, "Secure, research and medical", FI, SP, "government data center cleaning; communications facility cleaning"),
    ("Government hospital and VA medical facility cleaning", D24, "Secure, research and medical", FI, SP, "VA hospital cleaning; military hospital cleaning; VA clinic construction cleaning"),
    # Additions to existing families
    ("Post-construction duct cleaning", "Mechanical, Electrical & Construction IAQ", "Duct and air system cleaning", FI, SP, "construction duct cleaning; NADCA duct cleaning after construction"),
    ("Ventilation commissioning cleaning", "Mechanical, Electrical & Construction IAQ", "Duct and air system cleaning", FI, SP, "HVAC commissioning cleaning; air system startup cleaning"),
    ("Indoor air quality testing coordination", "Mechanical, Electrical & Construction IAQ", "Duct and air system cleaning", TU, C, "IAQ testing coordination; air test coordination"),
    ("Elevator shaft and hoistway cleanup", "Vertical Transportation & Circulation", "Hoistways and shafts", RO, SP, "hoistway cleaning; elevator pit and shaft cleanup"),
    ("Controlled-environment final decontamination", "Specialty & Controlled Environments", "Decontamination and verification", FI, CR, "final decon; controlled environment decontamination"),
    ("Post-construction odor removal", "Specialty & Controlled Environments", "Decontamination and verification", TU, C, "new construction odor removal; paint and adhesive odor removal"),
    ("Environmental verification preparation", "Specialty & Controlled Environments", "Decontamination and verification", TU, SP, "pre-test cleaning; verification readiness cleaning"),
    ("Precast concrete cleaning", "Exterior, Hardscape & Building Envelope", "Architectural surfaces", FI, SP, "precast panel cleaning; architectural precast cleaning"),
    ("Architectural metal cleaning", "Exterior, Hardscape & Building Envelope", "Architectural surfaces", FI, SP, "metal panel and storefront metal cleaning; anodized and stainless facade cleaning"),
    ("Sensitive historic masonry cleaning", "Exterior, Hardscape & Building Envelope", "Architectural surfaces", ANY, SP, "historic brick cleaning; gentle masonry cleaning"),
]

GROUPS = {
    "Demolition cleanup": ("Demolition leaves the heaviest debris and dust load of any phase, and the new work starts on top of whatever is left.",
                           "Wet methods and HEPA capture hold demolition dust down, and debris is separated for recycling before it is hauled."),
    "Disaster reconstruction": ("Rebuilding after fire, flood or storms means residue, moisture and debris hiding in places new work will seal in.",
                                "Crews clean behind the restoration contractor, working with moisture readings and documentation so rebuild trades start clean."),
    "Regulated and historic work": ("Post-abatement areas and historic fabric both punish the wrong method: one with exposure risk, the other with irreversible damage.",
                                    "Regulated work follows the abatement plan and clearance results; historic surfaces get the gentlest method that works, tested first."),
    "Commissioning and startup": ("Equipment cannot be started, tested or validated until construction dust, metal fines and blast media are out of it.",
                                  "Crews clean to the commissioning agent's checklist with lockout coordination, HEPA capture and documented sign-off."),
    "Advanced manufacturing": ("Semiconductor, pharmaceutical and biotech spaces have contamination limits that ordinary construction cleaning will not meet.",
                               "Protocol-driven cleaning with specified garments, wipes and sequences, coordinated with the owner's validation and certification teams."),
    "Energy facilities": ("Battery, solar and renewable sites combine electrical hazards, remote locations and owner turnover requirements.",
                          "Crews work under the site's electrical safety rules, clean without water near energized equipment and document turnover condition."),
    "Aviation and transit": ("Terminals and stations open to the public on fixed dates and are judged by travelers the first day.",
                             "Phased cleaning that follows security rules, airside or trackside access requirements and the opening schedule."),
    "Parking and vehicles": ("Garages and maintenance facilities are concrete-heavy, dusty and full of slurry, oil and coating residue at turnover.",
                             "Sweeping, scrubbing and washing with water recovery, timed around striping, sealers and equipment installation."),
    "Marine and public works": ("Waterfront and public projects carry environmental rules on wash water and debris that ordinary jobs do not.",
                                "Debris containment and water recovery near waterways, with cleaning documented for the public owner."),
    "Federal, state and municipal": ("Government buildings close out under strict inspection, documentation and access rules set by the owner agency.",
                                     "Crews follow the prime contractor's site rules, wage and reporting requirements and the agency's closeout checklist."),
    "Military installations": ("Base projects add installation access, security rules and mission schedules to every cleaning scope.",
                               "Access is arranged through the prime contractor and the installation's process, and crews follow base safety and environmental rules."),
    "Secure, research and medical": ("Secure, research and medical facilities restrict who enters, what is touched and how cleaning is documented.",
                                     "Escorted or credentialed access as the facility requires, protocol-matched products and documented sequences."),
    "Duct and air system cleaning": ("Construction dust in ducts and air handlers spreads through the whole building the day the system starts.",
                                     "Source removal with HEPA-filtered negative air to industry standards, coordinated with the mechanical contractor and commissioning."),
    "Hoistways and shafts": ("Debris in elevator pits and hoistways is a fire and equipment hazard and fails elevator inspections.",
                             "Work only under the elevator contractor's lockout and access control, top down, with debris removed from the pit last."),
    "Decontamination and verification": ("Controlled spaces are tested before use, and a failed test or lingering odor delays occupancy.",
                                         "Final cleaning in the sequence the testing firm and owner protocol require, so the space passes the first time."),
    "Architectural surfaces": ("Precast, metal and historic masonry are expensive finishes that the wrong cleaner can stain, etch or strip.",
                               "Manufacturer and preservation guidance first, test panels before full cleaning and the least aggressive method that works."),
}

# New names that duplicate an existing service: folded into that service as searchable aliases.
MERGES = {
    "Post-equipment installation cleaning": ["manufacturing equipment installation cleanup"],
    "Fireproofing overspray removal": ["post-fireproofing cleanup"],
    "Curtain wall cleaning": ["curtain wall and facade detailing"],
    "Sprinkler pipe exterior dusting": ["fire protection piping exterior cleaning"],
}

ICONS = {D21: "demo", D22: "factory", D23: "plane", D24: "capitol"}
HINTS = {D21: "Demo, gut-outs, disaster rebuilds", D22: "Commissioning, fabs, pharma, energy",
         D23: "Airports, transit, garages, marinas", D24: "Federal, military, secure sites"}
SHORT = {D21: "Demolition & Reconstruction", D22: "Industrial Commissioning", D23: "Infrastructure & Transportation", D24: "Government & Military"}
SLUG = {D21: "post-demolition-reconstruction", D22: "industrial-commissioning", D23: "infrastructure-transportation", D24: "government-military-defense"}
