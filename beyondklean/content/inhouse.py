"""In-house voice: rewrites applied to every content string at build time.

The first drafts described a referral network. Beyond Klean now performs the work with its own
crews (and travel crews for out-of-area projects), so referral wording is rewritten here instead
of editing hundreds of task files. Applied in order; plain strings unless marked as regex.
"""
import re

EXACT = [
    ("The cleanup contractors we match load, sort and manage the debris that goes into them.",
     "Our crews load, sort and manage the debris that goes into them."),
    ("How are specialty cleaning contractors verified?", "How are specialty crews qualified?"),
    ("By checking training, protocols, references for that facility type, and insurance that covers the work. Regulated scopes are approved case by case.",
     "By training, written protocols and experience in that facility type, with insurance that covers the work. Regulated scopes are approved case by case."),
    ("Our network handles the cleaning and documentation that supports it.",
     "Our crews handle the cleaning and documentation that supports it."),
    ("They are listed so buyers can find the right path, and they are routed only to properly licensed providers after case-by-case review.",
     "Each request is reviewed case by case and assigned only to properly licensed and certified technicians."),
    ("They are never routed automatically. Each request is reviewed, and only providers with the required licenses, training and insurance are introduced.",
     "They are never scheduled automatically. Each request is reviewed, and only technicians with the required licenses, training and insurance are assigned."),
    ("The retailer's construction team or GC, with Beyond Klean coordinating scope and verified local contractors",
     "The retailer's construction team or GC, with Beyond Klean handling the cleaning scope and crews"),
    ("Beyond Klean standardizes the scope and matches verified local contractors where coverage exists",
     "Beyond Klean standardizes the scope and staffs each site, with travel crews for out-of-area locations"),
    ("Beyond Klean confirms contractor capacity before promising a time",
     "Beyond Klean confirms crew availability before promising a time"),
    ("Requests are reviewed and routed to qualified restoration providers where coverage exists, with clear communication about capacity after major events",
     "Requests are reviewed and assigned to qualified restoration crews, with clear communication about capacity after major events"),
    ("Our partner program, Above Eye Level Cleaning,", "Our sister brand, Above Eye Level Cleaning,"),
    ("Our partner program focused on overhead cleaning", "Our sister brand focused on overhead cleaning"),
    ("route only to qualified providers", "assign only qualified technicians"),
    ("they are listed so buyers can find them, but routed only to properly licensed providers",
     "they are assigned only to properly licensed technicians"),
    ("routed only to providers with the right training", "assigned only to crews with the right training"),
    ("Contractor coverage varies by market; confirm before committing dates",
     "Crew availability varies by date and location; confirm before committing dates"),
    ("so a request under any of them reaches the same qualified contractors", "so a request under any of them reaches the same crew"),
]
REGEX = [
    (r"\brouted\b", "assigned"),
    (r"\bRouted\b", "Assigned"),
    (r"\bare introduced\b", "are assigned"),
    (r"\bqualified providers\b", "qualified technicians"),
    (r"\btrained providers\b", "trained technicians"),
    (r"\blicensed providers\b", "licensed technicians"),
]
_RX = [(re.compile(p), r) for p, r in REGEX]


def fix(s):
    if not isinstance(s, str):
        return s
    for a, b in EXACT:
        s = s.replace(a, b)
    for rx, b in _RX:
        s = rx.sub(b, s)
    return s


def deep(x):
    if isinstance(x, str):
        return fix(x)
    if isinstance(x, list):
        return [deep(v) for v in x]
    if isinstance(x, tuple):
        return tuple(deep(v) for v in x)
    if isinstance(x, dict):
        return {k: deep(v) for k, v in x.items()}
    return x
