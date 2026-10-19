"""Approximate I-4 centerline (Tampa I-275 junction to Daytona I-95 junction) and corridor ZIP selection.

Waypoints are approximate interchange locations; accuracy is about a mile, which is fine for a
"15 minutes off I-4" buffer (about 10 straight-line miles from the interstate).
"""
import json, math, sys
from pathlib import Path

I4 = [  # (lat, lon, label)
    (27.9620, -82.4535, "I-275 (downtown Tampa)"), (27.9625, -82.4380, "Ybor City"),
    (27.9700, -82.4000, "50th St"), (27.9900, -82.3330, "I-75"), (28.0050, -82.2900, "Mango"),
    (28.0130, -82.2570, "McIntosh Rd"), (28.0200, -82.2000, "Branch Forbes Rd"),
    (28.0300, -82.1380, "Plant City"), (28.0480, -82.0550, "County Line Rd"),
    (28.0700, -82.0150, "Memorial Blvd"), (28.0860, -82.0000, "Kathleen Rd"),
    (28.0930, -81.9600, "US-98 (Lakeland)"), (28.1050, -81.9250, "SR-33"),
    (28.1400, -81.8600, "Polk Pkwy"), (28.1650, -81.8080, "Polk City"),
    (28.1900, -81.7500, "CR-557"), (28.2275, -81.6465, "US-27"), (28.2570, -81.6200, "ChampionsGate"),
    (28.3000, -81.5800, "World Dr"), (28.3330, -81.5400, "US-192 (Celebration)"),
    (28.3850, -81.4950, "Lake Buena Vista"), (28.4250, -81.4650, "SR-528"),
    (28.4520, -81.4450, "Sand Lake Rd"), (28.4730, -81.4520, "Universal"),
    (28.4930, -81.4300, "Turnpike"), (28.5100, -81.4100, "John Young Pkwy"),
    (28.5400, -81.3840, "Downtown Orlando"), (28.5700, -81.3860, "Princeton St"),
    (28.5980, -81.3920, "Lee Rd"), (28.6250, -81.3880, "Maitland Blvd"),
    (28.6580, -81.3920, "Altamonte Springs"), (28.6900, -81.3750, "Longwood"),
    (28.7550, -81.3500, "Lake Mary"), (28.8000, -81.3300, "Sanford (SR-46)"),
    (28.8350, -81.3200, "St. Johns River"), (28.8580, -81.2900, "US-17/92"),
    (28.8950, -81.2550, "DeBary"), (28.9270, -81.2300, "Saxon Blvd"),
    (28.9500, -81.2050, "Orange City"), (28.9900, -81.1750, "SR-44 (DeLand)"),
    (29.0600, -81.1500, "Lake Helen"), (29.1200, -81.1300, "US-92"),
    (29.1540, -81.0810, "I-95 (Daytona Beach)"),
]
MI = 3958.8


def _xy(lat, lon, lat0=28.5):
    return (math.radians(lon) * math.cos(math.radians(lat0)) * MI, math.radians(lat) * MI)


def dist_to_i4(lat, lon):
    """Miles from a point to the I-4 polyline, and the index of the nearest segment."""
    px, py = _xy(lat, lon)
    best = (1e9, 0, 0.0)
    for i in range(len(I4) - 1):
        ax, ay = _xy(*I4[i][:2]); bx, by = _xy(*I4[i + 1][:2])
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        d = math.hypot(px - ax - t * dx, py - ay - t * dy)
        if d < best[0]:
            best = (d, i, t)
    return best


def milepost(i, t):
    m = 0.0
    for k in range(i):
        ax, ay = _xy(*I4[k][:2]); bx, by = _xy(*I4[k + 1][:2]); m += math.hypot(bx - ax, by - ay)
    ax, ay = _xy(*I4[i][:2]); bx, by = _xy(*I4[i + 1][:2])
    return m + t * math.hypot(bx - ax, by - ay)


if __name__ == "__main__":
    import zipcodes
    RADIUS = 10.0  # about 15 minutes of surface-road driving
    out = []
    for z in zipcodes.filter_by(state="FL"):
        if z["zip_code_type"] != "STANDARD" or not z["active"] or not z["lat"]:
            continue
        d, i, t = dist_to_i4(float(z["lat"]), float(z["long"]))
        if d <= RADIUS:
            out.append({"zip": z["zip_code"], "city": z["city"], "county": z["county"].replace(" County", ""),
                        "lat": float(z["lat"]), "lon": float(z["long"]), "miles": round(d, 1),
                        "mp": round(milepost(i, t), 1), "near": I4[i][2] if t < .5 else I4[i + 1][2],
                        "area_codes": z["area_codes"]})
    out.sort(key=lambda r: r["mp"])
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
    from collections import Counter
    print(len(out), Counter(r["county"] for r in out))
    print(len({(r["city"], r["county"]) for r in out}), "cities")
    print(sorted({r["city"] for r in out}))
