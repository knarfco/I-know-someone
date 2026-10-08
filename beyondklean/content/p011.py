def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Mailroom and package room cleaning": T(
 "Mailroom and package room cleaning cleans mailbox banks, parcel lockers, shelving, counters and floors in residential and commercial mail areas, removing film, labels and construction dust.",
 "Residents use the mailroom daily from the first day of occupancy. Mailbox banks and smart lockers arrive with film and labels and collect dust from nearby work.",
 "Crews remove film and labels, clean metal finishes with the grain, wipe locker screens dry and clean shelving and floors.",
 ["Mailbox and locker count", "Finishes and screens", "Film and labels", "Shelving"],
 ["Locker screens and keypads should not be sprayed.", "Postal locks must not be forced."],
 [("Are mailboxes cleaned before residents move in?", "Yes, mailbox banks are cleaned and film and labels are removed."),
  ("How are smart package lockers cleaned?", "Exteriors are wiped and screens cleaned with dry or barely damp cloths."),
  ("Is the mailroom part of the final clean?", "Yes, it is a common-area space that residents use daily."),
  ("Who removes mailbox film?", "The cleaning crew at final clean.")]),
"Trash room and chute room cleaning": T(
 "Trash room and chute room cleaning cleans trash and recycling rooms, chute doors, compactor areas and floors in residential and mixed-use buildings before occupancy.",
 "Trash rooms collect construction debris and odors, and chute doors on every floor are seen by residents. A dirty trash room causes complaints from day one.",
 "Crews remove debris, degrease floors and walls, clean chute doors floor by floor and leave compactor equipment to its service provider.",
 ["Rooms and floors with chute doors", "Compactor equipment", "Floor drains", "Odor control"],
 ["Compactors must be locked out.", "Chute interiors need specialist cleaning."],
 [("Are trash chutes cleaned in new buildings?", "Chute doors and rooms are cleaned; chute interiors are cleaned by specialists if needed."),
  ("Why do trash rooms smell in new buildings?", "Construction debris and food waste from workers can leave odors before residents arrive."),
  ("Is the compactor cleaned?", "Exteriors around it are; the compactor itself is serviced by its provider."),
  ("When are trash rooms cleaned?", "Before residents move in, as part of common-area turnover.")]),
}
