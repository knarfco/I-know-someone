"""Line icons (24x24, stroke = currentColor), written to site/assets/icons.svg as one sprite.

Use in HTML with ic("name", up): <svg><use href="assets/icons.svg#i-name"/></svg>
"""

ICONS = {
    # service families
    "debris": '<path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 13h10l1-13"/><path d="M10 11v6M14 11v6"/>',
    "broom": '<path d="M14 3l-4 9"/><path d="M6.5 12h7l2.5 9H4z"/><path d="M8 16l-1 5M11 16v5M14 16l1 5"/>',
    "dust": '<path d="M7 17a4 4 0 0 1-.5-8 6 6 0 0 1 11.3 1.5A3.5 3.5 0 0 1 17 17z"/><circle cx="5" cy="21" r=".6"/><circle cx="10" cy="20.5" r=".6"/><circle cx="15" cy="21" r=".6"/><circle cx="20" cy="20" r=".6"/>',
    "overhead": '<path d="M2 4h20"/><path d="M5 4v3M10 4v3M15 4v3M20 4v3"/><path d="M3 7h18"/><path d="M12 21V11"/><path d="M8.5 14.5L12 11l3.5 3.5"/>',
    "walls": '<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M3 14h18M9 4v5M15 9v5M9 14v6"/>',
    "door": '<path d="M5 21V4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v17"/><path d="M3 21h18"/><circle cx="15.5" cy="12" r="1"/>',
    "glass": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M12 3v18M4 12h16"/><path d="M7 6l2.5 2.5M15 14l2.5 2.5"/>',
    "floor": '<path d="M2 20l4-8h12l4 8z"/><path d="M8 12l-2 8M12 12v8M16 12l2 8M4 16h16"/><path d="M12 3v5M9.5 5.5L12 8l2.5-2.5"/>',
    "carpet": '<rect x="3" y="7" width="13" height="12" rx="1"/><path d="M16 9h3a2 2 0 0 1 0 4h-3"/><path d="M6 10v6M9 10v6M12 10v6"/>',
    "faucet": '<path d="M4 11h9a3 3 0 0 1 3 3v1"/><path d="M4 8v6"/><path d="M8 11V7h3"/><path d="M16 18.5c0 1.2-.7 2-1.5 2s-1.5-.8-1.5-2 1.5-3 1.5-3 1.5 1.8 1.5 3z"/>',
    "kitchen": '<path d="M4 11h16v7a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3z"/><path d="M2 11h20"/><path d="M8 7c0-1.5 1-1.5 1-3M12 7c0-1.5 1-1.5 1-3M16 7c0-1.5 1-1.5 1-3"/>',
    "fan": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="1.5"/><path d="M12 10.5c0-3 1-5 3-5s2 3-1.5 5.5M13.5 12c3 0 5 1 5 3s-3 2-5.5-1.5M10.5 12c-3 0-5-1-5-3s3-2 5.5 1.5M12 13.5c0 3-1 5-3 5s-2-3 1.5-5.5"/>',
    "bag": '<path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "health": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M12 9v6M9 12h6"/>',
    "facade": '<path d="M4 21V5l8-2 8 2v16"/><path d="M2 21h20"/><path d="M8 8h2M14 8h2M8 12h2M14 12h2M8 16h2M14 16h2"/>',
    "scraper": '<path d="M4 20l7-7"/><path d="M9 11l4 4"/><path d="M11 9l6-6 4 4-6 6"/>',
    "elevator": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M12 3v18"/><path d="M6.5 10L8 8l1.5 2M14.5 14l1.5 2 1.5-2"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="17" rx="1.5"/><path d="M9 4V3h6v1"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/>',
    "apartments": '<rect x="4" y="3" width="10" height="18"/><path d="M14 9h6v12h-6"/><path d="M2 21h20M7 7h1M10 7h1M7 11h1M10 11h1M7 15h1M10 15h1M17 13h1M17 17h1"/>',
    "drop-warn": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M12 10v4M12 17h.01"/>',
    # markets
    "house": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "office": '<rect x="5" y="3" width="14" height="18"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M11 21v-3h2v3"/>',
    "factory": '<path d="M3 21V11l5 3v-3l5 3v-3l5 3V4h3v17z"/><path d="M7 18h2M12 18h2"/>',
    "school": '<path d="M3 9l9-5 9 5"/><path d="M5 9v10M9 9v10M15 9v10M19 9v10"/><path d="M3 21h18"/>',
    "capitol": '<path d="M8 9a4 4 0 0 1 8 0"/><path d="M12 3v2"/><path d="M5 9h14"/><path d="M6 11v7M10 11v7M14 11v7M18 11v7"/><path d="M3 21h18M4 18h16"/>',
    "military": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M12 8l1.2 2.5 2.8.4-2 2 .5 2.8-2.5-1.3-2.5 1.3.5-2.8-2-2 2.8-.4z"/>',
    # process
    "send": '<path d="M21 3L3 10.5l7 2.5 2.5 7z"/><path d="M21 3l-11 10"/>',
    "crew": '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2A5 5 0 0 1 21 19"/>',
    "bid": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><path d="M12.5 10.5c-.5-.6-1.2-.8-2-.6-.9.2-1.2 1.4-.2 1.8l1.6.6c1 .4.7 1.7-.3 1.9-.9.2-1.6-.1-2.1-.7M11.2 9v1M11.2 14.3v1"/>',
    "truck": '<path d="M2 6h12v10H2z"/><path d="M14 9h4l3 3v4h-7"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "badge": '<circle cx="12" cy="9" r="6"/><path d="M9.5 9l1.7 1.7L14.5 7.5"/><path d="M8.5 14l-1.5 7 5-2.5 5 2.5-1.5-7"/>',
    # page parts
    "why": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5h.01"/>',
    "how": '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L3.5 17.5l3 3 5.7-5.7a4 4 0 0 0 5.3-5.3l-2.4 2.4-2.6-.5-.5-2.6z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "warn": '<path d="M12 3.5L2.5 20h19z"/><path d="M12 10v4.5M12 17.2h.01"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 0 1 4.8 1c0 1.7-2.3 2-2.3 3.5M12 17h.01"/>',
    "leaf": '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>',
    "filter": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 9h16M4 14h16M8 4v16M12 4v16M16 4v16"/>',
    "photo": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.8"/><path d="M21 16l-5-5-8 8"/>',
    "doc": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h7"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "blower": '<path d="M3 10h9l3-3v10l-3-3H3z"/><path d="M17 9c1 .7 1 5.3 0 6M19.5 7c2 1.8 2 8.2 0 10"/>',
    "vacuum": '<rect x="4" y="9" width="9" height="11" rx="2"/><path d="M8.5 9V6a3 3 0 0 1 6 0v8h4v6"/><path d="M16 20h5"/>',
    "demo": '<path d="M14 4l6 6-3 3-6-6z"/><path d="M11 7L3.5 14.5a2 2 0 0 0 0 2.8l3.2 3.2a2 2 0 0 0 2.8 0L17 13"/><path d="M3 21h7"/>',
    "plane": '<path d="M10.5 3.5c.8-.8 2.2-.8 3 0s.8 2.2 0 3L11 9l2 9-2 2-3.5-7L4 16.5V19l-1.5 1.5L1 17l3-3-2.5-1.5L3 11l2.5.5L9 8 2 4.5 4 2.5l9 2z"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
}

FAMILY_ICON = {
    "Site, Debris & Waste Management": "debris",
    "Rough Clean": "broom",
    "Fine Dust, Drywall Dust & Controlled-Dust Cleaning": "dust",
    "Overhead & Elevated Surfaces (Above Eye Level)": "overhead",
    "Walls, Ceilings & Interior Finishes": "walls",
    "Doors, Hardware, Millwork & Casework": "door",
    "Glass, Windows & Glazing": "glass",
    "Hard Floors": "floor",
    "Carpet & Soft Surfaces": "carpet",
    "Restrooms & Plumbing Fixtures": "faucet",
    "Kitchens, Food Facilities & FRP": "kitchen",
    "Mechanical, Electrical & Construction IAQ": "fan",
    "Retail Fixtures & Store Opening": "bag",
    "Specialty & Controlled Environments": "health",
    "Exterior, Hardscape & Building Envelope": "facade",
    "Residue, Stain & Protective-Material Removal": "scraper",
    "Vertical Transportation & Circulation": "elevator",
    "Turnover, Punch & Closeout Support": "clipboard",
    "Multifamily & Residential-Scale Turnover": "apartments",
    "Restoration & Regulated Work (Conditional)": "drop-warn",
}


def sprite():
    syms = "".join(
        f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in ICONS.items())
    return f'<svg xmlns="http://www.w3.org/2000/svg">{syms}</svg>\n'


def ic(name, up="", cls="ic"):
    assert name in ICONS, name
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="{up}assets/icons.svg#i-{name}"/></svg>'
