def T(a, y, m, s, w, q):
    return dict(a=a, y=y, m=m, s=s, w=w, q=q)

P = {
"Mop sink and janitor closet cleaning": dict(
 a="Mop sink and janitor closet cleaning cleans custodial rooms, mop sinks, shelving, hooks and floors so the space is ready for the building's cleaning staff on day one.",
 y="Janitor closets are often used as storage and wash-up rooms by trades during construction, so they are left with paint, grout and debris in the sink.",
 q=[("Why do janitor closets need cleaning after construction?", "Trades use them for storage and to wash tools, leaving paint, grout and debris behind."),
  ("What is a mop sink?", "A low, floor-level sink used by custodial staff to fill and empty mop buckets."),
  ("Is the janitor closet part of the final clean?", "Yes, it is cleaned so custodial staff can start work immediately."),
  ("Who uses the janitor closet after turnover?", "The building's custodial staff or janitorial contractor.")]),
"Eyewash and emergency shower station cleaning": dict(
 a="Eyewash and emergency shower station cleaning cleans the exterior, bowls, covers and signage of safety stations without changing valves or interfering with their operation.",
 y="Safety stations must be clean and ready to use instantly. Construction dust on covers and bowls can get into someone's eyes during an emergency.",
 q=[("Who tests eyewash stations?", "Facility staff test them on a schedule, typically weekly activation and annual inspection."),
  ("How are eyewash stations cleaned?", "Exteriors, bowls and dust covers are wiped gently, without changing valves or removing parts."),
  ("Are eyewash stations part of the final clean?", "Their exteriors and surroundings are, along with signage."),
  ("Why keep eyewash covers clean?", "Dust on covers can be flushed into the user's eyes during an emergency.")]),
"Plumbing fixture first-flush and aerator debris check": dict(
 w=["Fixtures should not be disassembled without the plumber's approval.", "Persistent debris in aerators can mean the lines need flushing."],
 q=[("Why do new faucets sometimes have low water flow?", "Debris from new plumbing lines collects in the aerator screen at the faucet tip and restricts flow."),
  ("Who flushes new plumbing systems?", "The plumber flushes lines before turnover to clear debris from new piping."),
  ("Can cleaning crews clean faucet aerators?", "Only if the plumber allows it; otherwise slow fixtures are reported."),
  ("What is a faucet aerator?", "The small screen at the end of a faucet that shapes the water stream and catches debris.")]),
}
