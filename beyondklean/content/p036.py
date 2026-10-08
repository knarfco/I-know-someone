def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Convenience store remodel cleanup": dict(
 a="Convenience store remodel cleanup cleans convenience stores and fuel station stores during and after remodels, often overnight in phases, so the store can keep serving customers.",
 y="Convenience stores operate long hours and lose sales every hour they are closed. Remodels are often done in phases, with cleanup after each night's work.",
 q=[("How fast can a convenience store reopen after remodel cleaning?", "Often by the next morning when cleaning follows each night's remodel work."),
  ("Are cooler doors cleaned during convenience store remodels?", "Yes, cooler doors and frames are cleaned inside and out."),
  ("Is the food service area cleaned?", "Yes, with food-safe products, because hot food and coffee areas are inspected."),
  ("Are fuel areas cleaned during store remodels?", "Exterior canopy and fuel islands may be included, following fuel area safety rules.")]),
"Food plant post-construction cleaning": dict(
 a="Food plant post-construction cleaning prepares food processing and packaging facilities after construction or expansion, before the plant's sanitation team takes over and production starts.",
 y="Food plants are audited for sanitation and contamination. Construction dust, debris and residues must be removed before food production or audits.",
 m="Specialist crews clean top down under the plant's procedures, with food-safe products and lockout on any equipment, documenting results for the plant's quality team.",
 q=[("Who cleans food plants after construction?", "Specialist crews experienced with food facilities, working under the plant's sanitation procedures."),
  ("Do food plants have sanitation audits?", "Yes, third-party food safety audits and customer audits check sanitation, including overhead areas."),
  ("Is overhead cleaning important in food plants?", "Yes, dust and debris over production lines are common audit findings."),
  ("Are plant sanitation procedures followed by construction cleaners?", "Yes, crews follow the plant's procedures, chemicals and lockout rules.")]),
}
