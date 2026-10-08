def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Multi-site retail rollout cleaning": dict(
 a="Multi-site retail rollout cleaning delivers the same cleaning scope, checklist and documentation across many store openings, remodels or refreshes in different locations, coordinated as a single program.",
 w=["Contractor coverage varies by market; confirm before committing dates.", "Inconsistent checklists create inconsistent stores."],
 q=[("What is a retail rollout program?", "A coordinated series of store openings, remodels or refreshes across many locations, usually on a tight schedule."),
  ("How is cleaning kept consistent across many stores?", "With one scope, one checklist and one photo documentation standard used by every local contractor."),
  ("Does Beyond Klean cover every market for rollouts?", "Coverage is being built market by market, starting in Florida, and we confirm coverage for each location before committing."),
  ("Who manages cleaning for a retail rollout?", "The retailer's construction team or GC, with Beyond Klean coordinating scope and verified local contractors.")]),
"Restaurant chain opening clean": T(
 "A restaurant chain opening clean is a standardized pre-opening clean for chain restaurants, covering the dining room, kitchen, restrooms, drive-thru and exterior to the chain's checklist and health inspection standards.",
 "Chains open many locations and need every one to look and pass inspection the same way. Kitchens must meet health code before opening, and the dining room must meet brand standards.",
 "Crews follow the chain's opening checklist, clean kitchens top down with food-safe products, detail the dining room and restrooms and clean the drive-thru and exterior last.",
 ["Chain opening checklist", "Kitchen equipment and health inspection date", "Dining room finishes", "Drive-thru and exterior"],
 ["Kitchen areas need food-safe products only.", "Specialty equipment such as fryers and ice machines is serviced by vendors."],
 [("Do restaurant chains have their own opening cleaning checklists?", "Many do, covering dining rooms, kitchens, restrooms and exteriors to brand standards."),
  ("Is the restaurant kitchen cleaned to health inspection standards?", "Yes, with food-safe products, top-down cleaning and attention to overhead areas and drains."),
  ("Is the drive-thru cleaned during a restaurant opening clean?", "Yes, windows, lanes and menu boards are included in the exterior clean."),
  ("Who provides the cleaning standard for a chain restaurant?", "The chain's construction or operations team provides the checklist.")]),
"Bank branch opening clean": T(
 "A bank branch opening clean prepares a new or remodeled branch for opening: lobby, teller line, offices, conference rooms, drive-thru, ATM exteriors and the areas around secure rooms, often under security escort.",
 "Bank branches combine customer-facing finishes with security-controlled areas. Cleaning must meet brand standards while following the bank's security procedures.",
 "Crews clean customer areas to brand standards, work in secure areas only under escort, and wipe ATM and device exteriors without touching security equipment.",
 ["Branch layout and finishes", "Security escort requirements", "ATMs and drive-thru", "Opening date"],
 ["Security equipment must not be touched or moved.", "Some areas can only be entered with bank staff present."],
 [("Are bank vaults cleaned during a branch opening clean?", "Areas around vaults and secure rooms are cleaned only under bank escort; vault interiors follow the bank's procedures."),
  ("Are ATMs cleaned before a branch opens?", "ATM exteriors and surrounds are wiped carefully, without spraying liquids into the machine."),
  ("Is a security escort required to clean a bank?", "Often, for secure areas, according to the bank's security policy."),
  ("Is the teller line cleaned?", "Yes, counters, glass and teller stations are detailed before opening.")]),
"Pharmacy and clinic retail opening clean": dict(
 a="A pharmacy and clinic retail opening clean prepares retail pharmacies and walk-in clinics for opening, including dispensing areas, medication storage, exam rooms, waiting areas and restrooms, following the operator's health requirements.",
 y="Pharmacies and clinics must meet health and licensing requirements, and medication storage areas must be clean before stock arrives. Exam rooms are used by patients from the first day.",
 m="Crews follow the operator's checklist, clean dispensing and storage areas before stocking, detail exam rooms and casework and leave any compounding areas to qualified specialists.",
 q=[("Are pharmacies cleaned differently from regular stores?", "Yes. Dispensing and medication storage areas follow the operator's health requirements, and exam rooms are detailed like medical offices."),
  ("Are clinic exam rooms cleaned before opening?", "Yes, casework, sinks, surfaces and floors are detailed, and the operator follows with its own disinfection protocol."),
  ("Is pharmacy compounding room cleaning part of the opening clean?", "Compounding rooms have special standards and are cleaned only by qualified specialists."),
  ("Who sets the cleaning requirements for a pharmacy opening?", "The pharmacy or clinic operator, based on its policies and licensing requirements.")]),
}
