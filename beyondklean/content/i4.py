"""I-4 corridor: Tampa to Daytona Beach.

ZIP codes come from research/i4_zips.json (built by research/i4_route.py): every active standard
ZIP whose center sits within about 10 straight-line miles of I-4, roughly 15 minutes of driving.
Counties and places carry short, factual descriptions; facility slugs point at the facility hubs.
"""

NAME = "I-4 Corridor"
SPAN = "Tampa to Daytona Beach"

INTRO = ("Interstate 4 runs about 132 miles across Central Florida, from downtown Tampa to I-95 at Daytona Beach. "
         "It ties together two major metros, the logistics belt of Polk County, the theme-park and convention district "
         "of Orlando and Kissimmee, the office parks of Seminole County and the coastal market of Volusia County. "
         "We cover every ZIP code within about 15 minutes of the interstate, end to end.")

# slug, name, seat, description, facility hub slugs most common in the county
COUNTIES = {
    "Hillsborough": dict(
        slug="hillsborough-county", seat="Tampa",
        desc=("Hillsborough County is the western anchor of I-4, which begins at I-275 in downtown Tampa. The county "
              "holds Tampa's office core, Port Tampa Bay, Tampa International Airport, the University of South Florida "
              "and MacDill Air Force Base, plus fast-growing suburbs east of the city in Brandon, Riverview and Plant City."),
        hubs=["office", "healthcare", "education", "multifamily", "hospitality", "warehouse", "government", "infrastructure"]),
    "Polk": dict(
        slug="polk-county", seat="Bartow",
        desc=("Polk County sits halfway between Tampa and Orlando, and its I-4 frontage has become one of Florida's busiest "
              "logistics belts. Distribution centers, industrial parks and new housing fill the corridor around Lakeland, "
              "Auburndale, Winter Haven, Haines City and Davenport."),
        hubs=["warehouse", "industrial", "retail", "multifamily", "education", "healthcare"]),
    "Osceola": dict(
        slug="osceola-county", seat="Kissimmee",
        desc=("Osceola County covers the southern edge of the theme-park district, with Kissimmee, Celebration and the "
              "US-192 corridor full of hotels, resorts, vacation homes and the retail and housing that serve them."),
        hubs=["hospitality", "multifamily", "retail", "education", "healthcare"]),
    "Orange": dict(
        slug="orange-county", seat="Orlando",
        desc=("Orange County is the center of the corridor: downtown Orlando, International Drive, the Orange County "
              "Convention Center, the theme parks and the hotel district, plus hospitals, universities and suburbs from "
              "Winter Garden and Ocoee to Winter Park and Apopka."),
        hubs=["hospitality", "office", "healthcare", "education", "retail", "multifamily", "data-labs", "government"]),
    "Seminole": dict(
        slug="seminole-county", seat="Sanford",
        desc=("Seminole County runs north of Orlando along I-4 through Altamonte Springs, Longwood, Lake Mary and Sanford. "
              "It is known for its corporate office parks, medical campuses, retail centers and Orlando Sanford "
              "International Airport."),
        hubs=["office", "healthcare", "retail", "multifamily", "education"]),
    "Volusia": dict(
        slug="volusia-county", seat="DeLand",
        desc=("Volusia County is the eastern anchor, where I-4 meets I-95 at Daytona Beach. The corridor passes DeBary, "
              "Orange City, Deltona and DeLand on the way to the coast's hotels, universities, the speedway district "
              "and the growing suburbs of Port Orange and Ormond Beach."),
        hubs=["hospitality", "education", "healthcare", "multifamily", "retail", "industrial"]),
}

# display name -> kind, description, facility hub slugs
PLACES = {
    "Tampa": ("city", "Where I-4 begins, at I-275 downtown. Office towers, hospitals, the port, the university district and Ybor City all sit a short drive from the interstate.", ["office", "healthcare", "hospitality", "education"]),
    "Seffner": ("community", "An unincorporated community east of Tampa along I-4 and US-92, with industrial sites and new neighborhoods.", ["warehouse", "multifamily"]),
    "Brandon": ("community", "A large unincorporated suburb east of Tampa with major retail, medical offices and apartment communities.", ["retail", "healthcare", "multifamily"]),
    "Valrico": ("community", "A growing residential community east of Brandon, with schools, retail centers and new subdivisions.", ["multifamily", "education", "retail"]),
    "Riverview": ("community", "One of the fastest-growing parts of Hillsborough County, south of Brandon, with new housing, schools and shopping centers.", ["multifamily", "education", "retail"]),
    "Gibsonton": ("community", "An unincorporated community on the US-41 corridor south of Tampa, with industrial and residential growth.", ["industrial", "multifamily"]),
    "Thonotosassa": ("community", "A community northeast of Tampa near I-4 and I-75, mixing rural land with new industrial and housing projects.", ["warehouse", "multifamily"]),
    "Dover": ("community", "An agricultural community between Brandon and Plant City, with new housing along the SR-60 and I-4 corridors.", ["multifamily", "warehouse"]),
    "Plant City": ("city", "Midway between Tampa and Lakeland, home of the Florida Strawberry Festival and a growing base of industrial parks and distribution centers.", ["warehouse", "industrial", "retail"]),
    "Kathleen": ("community", "An unincorporated area northwest of Lakeland, close to the I-4 and Polk Parkway interchanges.", ["warehouse", "multifamily"]),
    "Lakeland": ("city", "Polk County's largest city, home to Publix headquarters, Florida Southern College, Florida Polytechnic University and Lakeland Linder International Airport.", ["warehouse", "healthcare", "education", "office"]),
    "Polk City": ("city", "A small city at the I-4 interchange north of Lakeland, surrounded by new distribution and residential development.", ["warehouse", "multifamily"]),
    "Auburndale": ("city", "A city east of Lakeland with a large share of Polk County's distribution centers and industrial parks.", ["warehouse", "industrial"]),
    "Lake Alfred": ("city", "A small city between Auburndale and Haines City, with citrus roots and new residential growth.", ["multifamily", "industrial"]),
    "Winter Haven": ("city", "Polk County's chain-of-lakes city, with a hospital, schools, retail and the LEGOLAND Florida resort.", ["healthcare", "hospitality", "education", "retail"]),
    "Haines City": ("city", "A fast-growing city on US-27 in northeast Polk County, with new subdivisions, schools and retail.", ["multifamily", "education", "retail"]),
    "Davenport": ("city", "A city near the I-4 and US-27 interchange, at the center of northeast Polk's vacation-home and residential boom.", ["multifamily", "hospitality", "retail"]),
    "Kissimmee": ("city", "Osceola County's seat, on the US-192 tourism corridor, with hotels, vacation resorts, hospitals and new housing.", ["hospitality", "multifamily", "healthcare", "retail"]),
    "Orlando": ("city", "The center of the corridor: downtown towers, International Drive, the convention center, the theme parks, hospitals and Lake Nona.", ["hospitality", "office", "healthcare", "retail"]),
    "Windermere": ("town", "A lakeside town southwest of Orlando near the Dr. Phillips area and the theme-park district.", ["multifamily", "retail"]),
    "Gotha": ("community", "A small community between Windermere and Ocoee, surrounded by the growth of west Orange County.", ["multifamily"]),
    "Ocoee": ("city", "A west Orange County city along SR-429 and the Florida Turnpike, with retail, offices and new housing.", ["retail", "multifamily", "office"]),
    "Winter Garden": ("city", "A west Orange County city with a historic downtown and the Horizon West growth area, full of new schools, homes and shopping.", ["multifamily", "education", "retail"]),
    "Apopka": ("city", "A northwest Orange County city known for its nurseries, now growing fast with housing, retail and light industrial.", ["multifamily", "retail", "industrial"]),
    "Winter Park": ("city", "A city just north of Orlando, home to Rollins College, Park Avenue's shops and a large hospital campus.", ["retail", "healthcare", "education", "office"]),
    "Maitland": ("city", "A city along I-4 north of Winter Park with a large concentration of office parks.", ["office", "healthcare"]),
    "Altamonte Springs": ("city", "A Seminole County city at the SR-436 interchange with a regional mall, a hospital campus and dense retail.", ["retail", "healthcare", "office"]),
    "Casselberry": ("city", "A Seminole County city along US-17/92 with retail centers, apartments and neighborhood offices.", ["retail", "multifamily"]),
    "Longwood": ("city", "A Seminole County city on I-4 with light industrial parks, offices and established neighborhoods.", ["industrial", "office"]),
    "Winter Springs": ("city", "A Seminole County city with a new town center, schools and residential communities.", ["multifamily", "education", "retail"]),
    "Lake Mary": ("city", "A Seminole County city known for its corporate office campuses and regional headquarters along I-4.", ["office", "healthcare", "retail"]),
    "Sanford": ("city", "Seminole County's seat, with a historic downtown, a SunRail station and Orlando Sanford International Airport.", ["infrastructure", "industrial", "government", "multifamily"]),
    "Debary": ("city", "A Volusia County city just across the St. Johns River from Sanford, with a SunRail station and new development around it.", ["multifamily", "retail"]),
    "Orange City": ("city", "A Volusia County city with a hospital campus and the retail corridor along US-17/92 and Saxon Boulevard.", ["healthcare", "retail"]),
    "Deltona": ("city", "Volusia County's largest city by population, with schools, retail and steady residential growth.", ["multifamily", "education", "retail"]),
    "Osteen": ("community", "An unincorporated community east of Deltona on SR-415, with large new residential developments.", ["multifamily"]),
    "Deland": ("city", "Volusia County's seat, home to Stetson University and a historic downtown, with growing industrial parks near I-4.", ["education", "government", "industrial"]),
    "Lake Helen": ("city", "A small Volusia County city between DeLand and Daytona Beach, close to the I-4 interchange.", ["multifamily"]),
    "Daytona Beach": ("city", "Where I-4 ends at I-95. Home of Daytona International Speedway, Embry-Riddle Aeronautical University, beachfront hotels and new commercial development.", ["hospitality", "education", "healthcare", "retail"]),
    "Port Orange": ("city", "A city south of Daytona Beach with medical offices, retail and fast residential growth.", ["healthcare", "retail", "multifamily"]),
    "Ormond Beach": ("city", "A city north of Daytona Beach with an airport business park, medical campuses and coastal neighborhoods.", ["industrial", "healthcare", "multifamily"]),
}

# The ZIP database spells some names in title case; show them the way the cities write them.
DISPLAY = {"Debary": "DeBary", "Deland": "DeLand"}
