def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Medical office post-construction clean": dict(q=[
  ("Is a medical office cleaned differently from a regular office?", "Yes. Exam rooms, sinks, casework and waiting areas need detailed cleaning, and the practice usually follows with its own disinfection protocol before seeing patients."),
  ("Who disinfects a new medical office before it opens?", "The practice's cleaning provider or staff, using EPA-registered disinfectants according to the label. Construction cleaning prepares the surfaces first."),
  ("When should a new medical office be cleaned?", "After all trades and furniture installation are complete, close to the practice's move-in date, with a touch-up before patients arrive."),
  ("Are exam room cabinets and drawers cleaned inside?", "Yes. Cabinets and drawers are vacuumed and wiped because staff stock them with supplies immediately.")]),
"Dental office post-construction clean": dict(q=[
  ("Who cleans dental equipment after installation?", "The dental equipment vendor handles internal components and waterlines. Cleaning crews handle external surfaces, cabinetry and the room itself."),
  ("What is a dental operatory?", "A treatment room with a dental chair, delivery unit, light and cabinetry. Most dental offices have several."),
  ("Are dental sterilization rooms cleaned at turnover?", "Yes, surfaces, sinks and cabinetry are cleaned before the practice sets up its sterilization equipment and process."),
  ("Do dental offices require special cleaning products?", "Practices often specify products compatible with their chairs and equipment, so crews confirm before using anything on equipment surfaces.")]),
"Operating room post-construction clean": dict(
 a="An operating room post-construction clean is a specialized, protocol-driven clean of new or renovated operating rooms and procedure rooms before air balancing verification, environmental testing and clinical use.",
 w=["Air and surface testing may be required before the room can be used.", "Only hospital-approved products and procedures may be used."],
 q=[("Who cleans operating rooms after construction?", "Specialized healthcare cleaning crews working under the hospital's infection prevention and environmental services teams."),
  ("Are operating rooms tested after construction cleaning?", "Often. Hospitals may require air particle counts, pressure verification and sometimes surface testing before clinical use."),
  ("Why is operating room cleaning so strict?", "Operating rooms have the highest infection control requirements in a hospital, and contamination can lead to surgical site infections."),
  ("Can a general construction cleaning crew clean an operating room?", "No. It requires crews trained in healthcare construction protocols and approved by the hospital.")]),
"Laboratory post-construction clean": dict(
 a="A laboratory post-construction clean cleans new research, clinical or teaching labs, including casework, benches, sinks, fume hood exteriors, shelving and floors, following the lab's safety requirements and the safety officer's direction.",
 m="Reviewed crews clean under the safety officer's direction, wipe casework and benches with approved products, and leave instruments, chemicals and hood interiors alone unless procedures allow.",
 w=["Never touch lab instruments, chemicals or biological materials.", "Lab safety rules and PPE requirements apply to cleaning crews too."],
 q=[("Who approves cleaning in a new laboratory?", "The lab's safety officer or facilities manager, who sets the products, areas and rules crews must follow."),
  ("Are lab benches cleaned after construction?", "Yes, with approved products, because new benches and casework carry construction dust that can contaminate experiments."),
  ("Why is laboratory cleaning conditional work?", "Labs can contain chemical, biological or sensitive instrument hazards, so access and methods are controlled."),
  ("Are fume hood interiors cleaned during construction cleanup?", "Only according to the lab's procedures; exteriors are cleaned more routinely.")]),
"Fume hood exterior cleaning": dict(
 a="Fume hood exterior cleaning cleans the outside surfaces, sashes, airfoils and work surface edges of laboratory fume hoods without disturbing airflow monitors, sash settings or certification labels.",
 y="Fume hoods are certified for airflow before use. Cleaning that moves sashes, blocks airfoils or removes labels can affect certification and safety.",
 w=["Do not change sash positions or airflow monitor settings.", "Certification labels must remain in place."],
 q=[("What is a laboratory fume hood?", "A ventilated enclosure that pulls fumes away from the user when working with hazardous chemicals."),
  ("Can cleaning crews clean inside a fume hood?", "Only according to the lab's procedures, because interiors may contain chemical residue."),
  ("Are fume hood sashes cleaned?", "Yes, sash glass is cleaned carefully without changing its position."),
  ("Why must fume hood certification labels stay on?", "They show the hood passed airflow testing and when it was certified.")]),
}
