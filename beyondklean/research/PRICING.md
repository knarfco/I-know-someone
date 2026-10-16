# Beyond Klean price book - research notes

As of 2026-10 | US national, FL/GA/AL calibrated | 438 priced tasks (68 sourced, 370 derived)

Machine-readable data: `research/pricing.json`. This report explains how the numbers were built and where they are weakest.

> **These are starting points for an editable price book, not quotes.** Every line should be checked against
> the job's access, soil load, schedule, local wage and disposal costs before a bid goes out.

## 1. Method

1. **Scope.** Every non-merged task in `research/tasks.json` (438) gets one bidding unit and a low / mid / high unit price.
   Units used: sqft 218, each 111, lf 43, hour 17, cy 9, fixture 8, pane 6, room 6, lot 5, unit 5, floor 4, opening 4, load 2.
2. **Anchors first.** Where a published number exists we used it: public bid tabulations and awarded unit-price
   contracts (school districts, counties, cities, a state contract), then cost guides (Fixr, HomeAdvisor/Angi,
   Homewyse, Thumbtack, Housecall Pro), then trade publications and contractor forums. These lines are marked
   `sourced`.
3. **Derived lines.** Where no direct price exists, the price comes from the nearest sourced analog, checked with
   labor math: *production rate (units per worker-hour) x billed labor rate + materials/equipment*. These are marked
   `derived` and cite the analog and labor sources they lean on.
4. **What low / mid / high mean.** `low` is a competitive public-bid or large-volume price; `mid` is a typical
   FL/GA/AL bid to a GC or property manager; `high` covers small jobs, rush or night work, heavy soil, or hard access.
   `min` is a typical minimum charge when the line is bid alone. `rate_per_hr` is units per **worker**-hour.
5. **Exclusions unless the basis says otherwise:** lift and scaffold rental, dumpsters and tipping fees, permits, and
   licensed-subcontract work (hood/duct NFPA 96, NADCA duct work, abatement, mold, rope access, elevator mechanic).

## 2. Labor-rate assumptions (FL / GA / AL)

| Role | Billed $/worker-hr (low / mid / high) |
|---|---|
| General construction cleaner | $35 / $42 / $50 |
| Lead, floor tech, window tech | $45 / $55 / $65 |
| Specialty tech (lift work, restoration, controlled environments) | $55 / $70 / $90 |
| Nights, weekends, short-notice turnarounds | x1.5 |

- **Wages.** The BLS OEWS May 2024 median for janitors and cleaners (37-2011) is $17.27/hr nationally. State medians
  are FL $15.16, GA $15.93 and AL $14.00 (S46). The federal SCA wage determination for Polk County, FL lists Janitor
  (11150) at $15.63 plus $5.55/hr health and welfare (S47).
- **From wage to billed rate.** A ~$16-18 wage x ~1.30-1.35 burden (FICA, FUTA/SUTA, workers comp, GL) gives a
  loaded cost of ~$21-24/hr. Adding overhead, supervision, supplies and profit (x1.5-1.7) gives ~$35-45 billed.
  Contractor guides quote $35-60 per cleaner-hour for rough and light phases (S72) and $30-50 per employee-hour (S2).
- **Floor of the market.** Public janitorial bids in the region go as low as $15-20 per man-hour: Leon County
  Schools custodial $15-35/hr (S11), City of Pensacola $18-20 (S48). Those prices are routine custodial work with
  little overhead. Do not use them for construction cleaning.

## 3. Regional notes

- FL/GA/AL wages run about 8-19% below the national janitor median. Suggested factors vs national: FL 0.90,
  GA 0.93, AL 0.85, high-cost Northeast/West metros ~1.25.
- Disposal is cheap compared with the national picture. C&D tipping is $55/ton in Highlands Co., FL and $40.97/ton in
  Dougherty Co., GA (S42), against $90/ton in Fairfax, VA. A 30-yd roll-off with its weight allowance runs
  $530-740 in FL (S43).
- Florida humidity makes construction dust stick and slows final cleans (S6). Hurricane-season restoration work
  briefly drives up labor rates and lift rentals. Exterior washing has to handle wastewater properly (stormwater/NPDES).
- In Florida, mold assessment and remediation need a state license, and asbestos and lead work need certified
  contractors. Keep those lines as pass-through subcontract items.

## 4. Strongest anchors

| Anchor | Value | Source |
|---|---|---|
| Rough / final / touch-up clean | $0.10-0.15 / $0.15-0.30 / $0.06-0.12 per sf | Cleaner Match via ThePricer (S2) |
| Phase ranges, cost guide | rough $0.15-0.40, final $0.20-0.60 per sf | Fixr (S1) |
| Commercial post-construction | $0.15-0.75/sf; large commercial final $0.20-0.50 | ServiceMaster (S3), 2026 guides (S72) |
| Trade press baseline | 13-20 cents/sf commercial, to 35 cents restaurants (2011) | CMM Online (S4) |
| Production rates | commercial final 70-100 sf/worker-hr, rough 150-200, medical 50-80 | S8 |
| VCT strip & wax (FL bids) | $0.20-0.25/sf (Leon Co. Schools); $0.28-0.45/sf (Town of Davie) | S9, S10 |
| Carpet extraction (bids) | $0.09-0.40/sf (Leon Co. Schools), $0.05-0.15/sf (MoDOT) | S11, S12 |
| Gym floor screen & recoat | $0.26-0.95/sf bid tab; $0.40-0.80 typical | S14, S15 |
| Kitchen hood (NFPA 96) | $138-450 per hood system (Cobb Co. Schools GA), $200-395 (Jefferson Co. AL) | S16, S17 |
| HVAC duct cleaning (state contract) | $3.50-4.50/lf easy, $9.50-10.25/lf difficult; AHU $68.50-98.50/hr | S19 |
| Sidewalk pressure washing (FL county bid) | $0.075-0.20/sf | S20 |
| Graffiti removal (municipal bids) | $0.30-0.70/sf large areas; to $4.25 full service | S21, S22 |
| Wall/ceiling washing | $0.45-0.65/sf | S29 |
| Data center deep clean | ~$1/sf | S54 |
| Floor protection material | Ram Board ~$0.19-0.26/sf | S44 |
| Lift rental FL | 19 ft $97/day, 26 ft $121/day | S45 |
| Debris haul | full truck (13-17 cy) $600-800 | S41 |
| Multifamily per unit | construction-clean calculators assume $300-400 per unit | S7, S64 |

## 5. Most common tasks (~50)

| Task | Unit | Low | Mid | High | Min | Confidence | Sources |
|---|---|---|---|---|---|---|---|
| Rough clean of entire building | sqft | $0.08 | $0.13 | $0.22 | $750 | sourced | S1, S2, S72, S4 |
| Light clean (phase 2) | sqft | $0.06 | $0.10 | $0.16 | $400 | sourced | S2, S72 |
| Final clean of entire building | sqft | $0.15 | $0.25 | $0.40 | $1,000 | sourced | S1, S2, S3, S72, S4 |
| Final clean by phase or floor | sqft | $0.17 | $0.28 | $0.45 | $750 | sourced | S1, S2, S72 |
| Touch-up clean before owner walk | sqft | $0.05 | $0.08 | $0.15 | $350 | sourced | S2, S72 |
| Tenant improvement final clean | sqft | $0.18 | $0.30 | $0.50 | $600 | sourced | S1, S3, S72 |
| Store opening clean | sqft | $0.20 | $0.32 | $0.55 | $1,200 | sourced | S3, S4 |
| Restaurant chain opening clean | sqft | $0.30 | $0.50 | $0.85 | $1,500 | sourced | S4, S65 |
| Commercial kitchen post-construction clean | sqft | $0.35 | $0.60 | $1.00 | $750 | sourced | S4, S65, S70 |
| School post-construction cleaning | sqft | $0.15 | $0.25 | $0.40 | $2,000 | sourced | S1, S2, S4 |
| Warehouse post-construction cleaning | sqft | $0.06 | $0.11 | $0.20 | $1,500 | sourced | S77, S1 |
| Healthcare post-construction terminal-style clean | sqft | $0.40 | $0.70 | $1.20 | $1,500 | derived | S8, S65 |
| Data center post-construction cleaning | sqft | $0.50 | $1.00 | $1.75 | $3,000 | sourced | S54 |
| Apartment unit post-construction clean | unit | $225 | $350 | $550 |  | sourced | S7, S64, S2 |
| Condo unit final clean | unit | $275 | $425 | $700 |  | sourced | S7, S5 |
| Property management turnover cleaning | unit | $175 | $275 | $450 |  | sourced | S64 |
| Hotel room post-construction cleaning | room | $60.00 | $95.00 | $160 |  | derived | S2, S1 |
| Punch-list cleaning | hour | $40.00 | $48.00 | $60.00 | $200 | derived | S46, S48 |
| Final haul-off of remaining debris | load | $350 | $550 | $850 | $350 | sourced | S41, S42 |
| Construction dumpster loading | load | $250 | $400 | $650 | $250 | derived | S41, S43 |
| Daily jobsite sweep | sqft | $0.004 | $0.008 | $0.015 | $175 | derived | S49, S46 |
| Weekly jobsite clean | sqft | $0.01 | $0.02 | $0.035 | $300 | derived | S49, S46 |
| HEPA vacuuming of work areas | sqft | $0.015 | $0.025 | $0.045 | $200 | derived | S49, S46 |
| Fine drywall dust removal from all horizontal surfaces | sqft | $0.03 | $0.05 | $0.09 | $300 | derived | S1, S2, S46 |
| Open ceiling deck cleaning | sqft | $0.12 | $0.22 | $0.40 | $1,000 | sourced | S77, S45 |
| Warehouse ceiling dust removal | sqft | $0.08 | $0.15 | $0.28 | $1,200 | sourced | S77, S45 |
| High-bay light fixture cleaning | fixture | $12.00 | $22.00 | $40.00 | $300 | derived | S45, S77 |
| Full wall washing | sqft | $0.25 | $0.45 | $0.65 | $300 | sourced | S29 |
| Interior window cleaning | pane | $2.50 | $4.00 | $7.00 | $200 | sourced | S26, S27 |
| Exterior window cleaning | pane | $3.00 | $5.00 | $9.00 | $250 | sourced | S26, S27 |
| Storefront glass cleaning | sqft | $0.15 | $0.30 | $0.55 | $150 | sourced | S26 |
| Construction debris removal from glass | pane | $3.00 | $6.00 | $10.00 | $200 | sourced | S27 |
| Concrete and mortar splatter removal from glass | pane | $6.00 | $12.00 | $25.00 | $200 | sourced | S27 |
| Hard water stain removal from glass | sqft | $4.00 | $7.00 | $12.00 | $150 | sourced | S28 |
| Concrete floor auto-scrubbing | sqft | $0.03 | $0.05 | $0.09 | $350 | derived | S74, S49 |
| VCT initial floor finish | sqft | $0.20 | $0.32 | $0.50 | $350 | sourced | S9, S10 |
| VCT strip and refinish | sqft | $0.20 | $0.30 | $0.45 | $350 | sourced | S9, S10 |
| Burnishing | sqft | $0.02 | $0.035 | $0.06 | $150 | derived | S75 |
| Grout haze removal | sqft | $0.20 | $0.40 | $0.80 | $250 | derived | S32 |
| Grout line deep cleaning | sqft | $0.40 | $0.75 | $1.50 | $250 | sourced | S32 |
| Concrete polishing | sqft | $2.00 | $3.50 | $6.00 | $2,500 | sourced | S34 |
| Construction carpet vacuuming | sqft | $0.01 | $0.02 | $0.035 | $150 | derived | S49 |
| Carpet extraction | sqft | $0.12 | $0.22 | $0.40 | $250 | sourced | S11, S12, S13, S33 |
| Toilet and urinal detailing | fixture | $8.00 | $14.00 | $22.00 | $75.00 | derived | S49 |
| Kitchen exhaust hood and duct cleaning | each | $250 | $450 | $900 | $350 | sourced | S16, S17, S18 |
| HVAC duct interior cleaning | lf | $3.00 | $4.50 | $10.00 | $1,500 | sourced | S19 |
| Sidewalk pressure washing | sqft | $0.08 | $0.15 | $0.30 | $300 | sourced | S20, S23, S24 |
| Parking lot sweeping | hour | $95.00 | $125 | $175 | $250 | sourced | S58 |
| Building facade washing | sqft | $0.15 | $0.30 | $0.60 | $1,000 | sourced | S69 |
| Floor protection installation | sqft | $0.35 | $0.50 | $0.75 | $300 | sourced | S44 |
| Floor protection removal and disposal | sqft | $0.03 | $0.06 | $0.10 | $150 | derived | S44 |
| Stairwell cleaning top to bottom | floor | $35.00 | $60.00 | $100 | $150 | derived | S46 |
| Graffiti removal | sqft | $0.50 | $1.50 | $4.00 | $150 | sourced | S21, S22 |

## 6. Caveats and gaps

- **Source quality varies.** Public bid tabs are the best anchors, but many are old (Collier 2007, CMM 2011) or
  only list lump sums (Garland ISD windows, University of Kentucky final cleans). Consumer cost guides lean
  residential and run high per sf on small jobs. A few figures come from low-quality aggregator pages (marked in
  the source list). Treat them as directional only.
- **370 of 438 lines are derived.** Weakest areas, with no published unit price found:
  - overhead structure cleaning by lf (beams, joists, pipe, cable tray)
  - most door, millwork and casework detail items
  - FRP, kitchen detail and grocery department lines
  - residue removal (overspray, spray foam, fireproofing, tar)
  - controlled environments (OR, cleanroom, USP 797/800, vivarium)
  - escalators, pallet racks, HVLS fans, high-rise and curtain-wall glass
  - debris collection per cy (labor only)

  Calibrate these lines first against your own job-cost history.
- **High-variance lines.**
  - Window and glass work depends on pane size, access and scraping risk. Post-construction work is commonly
    priced at 2-3x routine (S27).
  - High dusting depends on lift access.
  - Restoration and regulated work depends on the specialist subcontractor.
- **Bundles.** A three-phase package (rough + light + final) adds up to about $0.29-0.78/sf at low/high and ~$0.48 at mid from
  these lines. A typical three-phase commercial bid lands at $0.25-0.60/sf, because a single contract shares
  mobilization and supervision. Discount 10-20% when bundling.
- **Public-sector work** may require SCA or Davis-Bacon wages, extra insurance, and bonding. Add these explicitly.

## 7. Sources

- **S1** [Fixr - Post-construction cleaning cost](https://www.fixr.com/costs/post-construction-cleaning) - Phase ranges: rough $0.15-0.40/sf, final $0.20-0.60/sf; renovation low end, new construction high end
- **S2** [ThePricer - Post construction clean up cost (cites Cleaner Match)](https://thepricer.org/post-construction-clean-up-cost) - Rough $0.10-0.15/sf, final $0.15-0.30/sf, touch-up $0.06-0.12/sf; $30-50 per employee-hour
- **S3** [ServiceMaster Clean - Post-construction cleaning cost factors](https://www.servicemasterclean.com/clean-blog/post-construction-cleaning/post-construction-cleaning-cost-factors/) - Commercial post-construction cleaning $0.15-0.75/sf by detail level
- **S4** [CMM Online - Tuesday's Ask the Experts: Post-construction cleaning (2011)](https://cmmonline.com/articles/tuesdays-ask-the-experts-post-construction-cleaning) - Trade Q&A: 13-20 cents/sf for commercial jobs, up to 35 cents for restaurants; windows, carpet, VCT refinish extra
- **S5** [HomeAdvisor - Post-construction cleaning cost](https://www.homeadvisor.com/cost/cleaning-services/clean-construction-site) - About $0.25/sf average for a new home
- **S7** [Construction Clean Partners - Calculator pricing assumptions](https://final-clean.com/calculator-pricing-assumptions/) - Construction-clean calculator prices residential living units at a flat ~$300-400 per unit; rates vary by state/project type
- **S8** [EngineersViews - Post construction cleaning calculator (2025 US reference)](https://engineersviews.com/tools/post-construction-cleaning-calculator/) - Production: commercial rough 150-200 sf/hr, standard 100-150, final 70-100, medical final 50-80 sf/worker-hr
- **S9** [Leon County Schools (FL) - Lincoln HS stripping bid tab & award (2018)](https://www.leonschools.net/cms/lib/FL01903265/Centricity/Domain/195/CURRENTBIDS/BID55272018LINCOLNHSSTRIPPING/AwardRecommendationandBidTab.pdf) - VCT strip and wax bids $0.20-0.25/sf
- **S10** [Town of Davie (FL) - ITB EL-21-61 janitorial bid tabulation (2021)](https://davie-fl.gov/DocumentCenter/View/15592/ITB-EL-21-61_Bid-Tabulation) - Optional as-needed strip & wax and tile/grout per SF; six vendors roughly $0.23-0.75/sf (strip & wax ~$0.28-0.45)
- **S11** [Leon County Schools (FL) - ITB 1001-2026 Supplemental Custodial Services bid tab](https://www.leonschools.net/cms/lib/FL01903265/Centricity/Domain/195/ITB%201001-2026%20Bid%20Tabulation.pdf) - Custodian $15-35/hr billed; carpet deep cleaning $0.09-0.40/sf across bidders
- **S12** [Missouri DOT - CD-15-001B janitorial services bid tabulation](https://www.modot.org/sites/default/files/documents/general_services/central_district_bidding/cd-15-001bjanitorialservices-bidtabulation.pdf) - Carpet deep clean/water extraction $0.05-0.15/sf; construction clean-up priced per person-hour
- **S13** [Collin County (TX) - Bid 2022-260 tabulation](https://eagenda.collincountytx.gov/docs/2022/CC/20221205_2806/53264%5FBid%20Tabulation%202022%2D260%2Epdf) - Wet-extraction carpet cleaning $0.34-1.75/sf (small, travel-loaded sites)
- **S14** [Cobb County School District (GA) - Gym floor resurfacing bid tab B1922](https://media.cobbk12.org/media/WWWCobb/medialib/gymfloorresurfacingrefinishing_b1922_tabsheet.d5ca0346913.pdf) - Screen and recoat bids about $0.26-0.95/sf
- **S15** [Sports Venue Calculator - gym floor maintenance Q&A (sports flooring manufacturer rep)](https://sportsvenuecalculator.com/knowledge/news/gym-floor-maintenance-best-practices-interview/) - Screen and recoat typically $0.40-0.80/sf
- **S16** [Cobb County School District (GA) - Hood cleaning bid tab B2115](https://media.cobbk12.org/media/WWWCobb/medialib/fnshoodclnsrv-b2115_tabsht.e5bcc246889.pdf) - Per single/double hood system: $137.90-350 single, $154.85-450 double
- **S17** [Jefferson County Commission (AL) - Kitchen exhaust hood cleaning bid tabs 31-20 / 30-24](https://paca.jccal.org/Sites/PACA/AppData/DocLib/Main/30-24%20Kitchen%20Commerical%20Food%20Areas%20Exhaust%20Hoods%20Cleaning%20Services%20-%20Bid%20Tabulation.pdf) - $200-395 per hood per location
- **S18** [HoodMart / Angi - commercial kitchen hood cleaning cost guides](https://www.hoodmart.com/blog/post/the-average-cost-of-a-commercial-exhaust-hood-cleaning) - Vendor rate cards by system length ~$475-1,100; HomeAdvisor flat fee ~$400-430, $140-180/hr
- **S19** [State of Iowa - HVAC duct cleaning task order unit rates](https://bidopportunities.iowa.gov/Home/ShowContractDocument/c53743de-1446-4cdf-b2c2-c98f2af5d25b) - Duct cleaning $3.50-4.50/lf easy access, $9.50-10.25/lf difficult; air handler work $68.50-98.50/hr
- **S20** [Collier County (FL) - Pressure washing bid 08-5002 tabulation (2007)](https://colliercountyfl.gov/home/showpublisheddocument/15932/635883137282070000) - Sidewalk/walkway pressure washing $0.075-0.20/sf
- **S21** [Dallas County (TX) - Bid 2022-002-6917 Power Washing Services tabulation](https://www.dallascounty.org/Assets/uploads/docs/purchasing/bidtabs/2022/Bid%20Tabulation-%202022-002-6917%20Power%20Washing%20Services.pdf) - Emergency power washing $0.15/sf; graffiti abatement $0.35-10.00/sf across bidders
- **S22** [Town of Apple Valley (CA) - Graffiti removal bid results](https://applevalley.org/home/showpublisheddocument/3395/635611242901270000) - Graffiti removal $0.30-0.70/sf over minimum areas
- **S23** [Housecall Pro - How to price pressure washing jobs](https://housecallpro.com/resources/how-to-price-pressure-washing-jobs) - Commercial flatwork $0.08-0.40/sf
- **S24** [Thumbtack - Power washing prices](https://www.thumbtack.com/p/power-washing-prices) - National $0.08-0.47/sf; $65-99/hr; average job $368
- **S26** [Housecall Pro / Jobber - commercial window cleaning pricing guides](https://www.housecallpro.com/resources/how-to-price-window-cleaning-guide/) - Commercial ~$2-8/pane, $50-100/hr, $0.10-0.50/sf of glass
- **S27** [Window cleaner trade forum + Angi - post-construction window pricing](https://community.windowcleaner.com/t/post-construction-cleanup/5930) - Post-construction priced 2-3x routine; overspray bids $5.50-10+/pane; Angi $12-20/window post-construction
- **S28** [Window cleaner trade forum - hard water stain removal pricing](https://community.windowcleaner.com/t/what-to-charge-for-glass-restoration-stain-removal/53202) - Glass restoration averages $5-10/sf incl. sealing
- **S29** [HomeAdvisor - Wall and ceiling washing cost](https://www.homeadvisor.com/cost/cleaning-services/clean-walls-and-ceilings) - $0.45-0.65/sf by wall material
- **S30** [Homewyse - Cost to clean ceiling tile (Jan 2026)](https://www.homewyse.com/maintenance_costs/cost_to_clean_ceiling_tile.html) - $0.63-0.78/sf
- **S31** [Homewyse - Cost to clean ceiling fan (Jan 2026)](https://www.homewyse.com/maintenance_costs/cost_to_clean_ceiling_fan.html) - $117-144 per fan (residential, incl. minimums)
- **S32** [HomeAdvisor / Fixr - Tile and grout cleaning and sealing](https://www.fixr.com/costs/tile-and-grout-cleaning) - Cleaning $0.50-3/sf; sealing $0.25-0.50 (HomeAdvisor) to $0.90-1.73 (Fixr)
- **S33** [Angi / HomeAdvisor - Carpet cleaning prices](https://www.angi.com/articles/what-are-average-carpet-cleaning-prices.htm) - Hot water extraction $0.20-0.90/sf; commercial carpet $0.15-0.25/sf (HomeAdvisor)
- **S34** [HomeAdvisor / This Old House - Polished concrete cost](https://www.homeadvisor.com/cost/flooring/polished-concrete-floor-cost) - Polish $2-16/sf; basic polish $2-6/sf
- **S35** [EngineerFix and cost guides - Terrazzo restoration cost](https://engineerfix.com/how-much-does-terrazzo-floor-restoration-cost/) - Finishing/polish $2.50-8.00/sf; full restoration $6-14/sf
- **S36** [Fixr - Mold remediation cost](https://www.fixr.com/costs/mold-remediation) - $10-30/sf of affected area
- **S37** [Fixr / HomeServe - Lead paint removal](https://www.fixr.com/costs/lead-paint-removal) - Removal $8-17/sf; encapsulation $1-4/sf
- **S38** [Asbestos removal cost guides (homeowner oriented)](https://partner.kurlon.com/news/asbestos-removal-cost-guide-2026-8211-adnan-painting-and-remodeling.html) - $8-25/sf incl. containment and disposal (low-quality source; verify locally)
- **S39** [LawnStarter / Angi - Fire and smoke damage restoration cost](https://www.lawnstarter.com/blog/cost/fire-and-smoke-restoration-price) - Standard fire/smoke cleanup $4-7/sf
- **S40** [Fixr / BioRecovery - Biohazard cleanup cost](https://fixr.com/costs/biohazard-cleanup) - $60-140/hr typical; $4-12 (to $20)/sf
- **S41** [HomeAdvisor - Junk / construction debris removal cost (2025)](https://www.homeadvisor.com/cost/cleaning-services/remove-waste/) - Construction debris $100-800/truckload; full truck 13-17 cy $600-800; per-cy $50-80 typical
- **S42** [Highlands County FL FY2025-26 landfill fees; Dougherty County GA tipping fees (2025)](https://highlandsfl.gov/departments/solid_waste/landfill/fee_schedule.php) - C&D disposal $55/ton (FL), $40.97/ton (GA)
- **S43** [ZTERS dumpster rental pricing, Tampa / Fort Myers FL (2025)](https://zters.com/dumpster-rental/tampa-fl) - 30-yd roll-off $677-740 incl. weight allowance; Orlando guides $530-650
- **S44** [Ram Board 38in x 100ft retail listings](https://www.runyonsurfaceprep.com/product/ram-board-38x100/) - $61.68-81.25 per 317 sf roll = ~$0.19-0.26/sf material
- **S45** [BigRentz - Florida scissor lift rental rates](https://www.bigrentz.com/rental-locations/florida/lakeland/scissor-lifts) - 19 ft electric $97/day, $230/wk; 26 ft $121/day, $338/wk
- **S46** [BLS OOH / OEWS - Janitors and building cleaners (May 2024)](https://www.bls.gov/ooh/building-and-grounds-cleaning/janitors-and-building-cleaners.htm) - National median $17.27/hr; FL $15.16, GA $15.93, AL $14.00 (OEWS 37-2011 state medians); basis for derived labor math
- **S48** [City of Pensacola (FL) - janitorial bids 24-045 / 24-046 (2024)](https://www.cityofpensacola.com/DocumentCenter/View/27050) - Low bids $18-20 per man-hour labor / extraction (low end of FL market)
- **S49** [ISSA - How to calculate cleaning times (612 production rates)](https://www.issa.com/articles/how-to-calculate-cleaning-times/) - Mopping 5,355 sf/hr; restroom ~3 min/fixture; vacuum 20-30 min per 1,000 sf
- **S50** [Cooperator News / Florida Community Association Journal - trash chute cleaning](https://sofl.cooperatornews.com/article/a-breath-of-fresh-air) - $30-40 per floor (Cooperator); $50-100 per floor (FCAJ 2024)
- **S51** [Commercial gutter cleaning price guides (2026)](https://cleanproguttercleaning.com/guides/commercial-gutter-cleaning-prices) - $0.75-2.75 per lf for commercial/multi-unit
- **S52** [Angi - Dryer vent cleaning cost](https://www.angi.com/articles/how-much-does-dryer-vent-cleaning-cost/dc/washington) - $90-250 per vent, by run length
- **S53** [Ice machine and grease trap service cost guides (ThePricer et al.)](https://www.thepricer.org/?p=19032) - Ice machine $120-350/unit (avg ~$200); interceptor service $130-250
- **S54** [Uptime Institute Journal - data center cleaning and sanitization](https://journal.uptimeinstitute.com/data_center_cleaning_sanitization_covid19/) - Up to ~$100,000 per deep clean of a 100,000 sf facility (~$1/sf); sanitization +20%
- **S55** [Window cleaner trade forum - chandelier cleaning pricing](https://community.windowcleaner.com/t/chandelier-cleaning-and-pricing/15495) - $80-125 and up per chandelier; guides $60-250 per fixture
- **S56** [HomeServe / Thumbtack - Solar panel cleaning cost](https://www.homeserve.com/blog/cost-guide/solar-panel-cleaning-service-cost) - $10-25 per panel small arrays; $3-8 per panel larger arrays; ~$100 minimums
- **S57** [Karcher know-how - cleaning escalators; escalator cleaning business model](https://www.kaercher.com/int/professional/know-how/cleaning-escalators-and-moving-walkways.html) - Maintenance clean ~20 min per 50-step escalator; restorative jobs planned at $800-2,500 per unit
- **S58** [City of Tulsa sweeping bid summary; World Sweeper contractor bidding guidance](https://www.cityoftulsa.org/media/16491/bid-summary-tac-308e.pdf) - Sweeper bids $125-195/hr; contractor bids typically $115-135/hr
- **S59** [HomeServe (citing Homewyse) - Efflorescence / brick cleaning cost](https://www.homeserve.com/blog/home-improvement/efflorescence-remover) - Brick cleaning $0.54-0.68/sf; acid/chemical efflorescence $1.00-3.50/sf
- **S60** [Paver cleaning and sealing cost guides](https://new.risingsunartscentre.org/news/paver-cleaning-and-sealing-cost-guide-2026.html) - Cleaning + sealing bundled $0.75-1.45/sf (low-quality source)
- **S61** [Epoxy floor cost guides - surface preparation tiers](https://dna.strongeru.com/how-much-is-it-cost-to-epoxy-sf-floor/) - Light prep $0.50-1.50, medium $1-3, heavy grind/shot blast $2-5/sf (low-quality source)
- **S64** [CMM Online - Tackling the condo and apartment market](https://cmmonline.com/articles/tackling-the-condo-and-apartment-market) - Multifamily flat rates $125 (studio/1BR) to $300+ (3BR+)
- **S65** [Housecall Pro - Commercial cleaning price guide 2025](https://www.housecallpro.com/?p=49928) - Restaurant/kitchen $0.15-0.25/sf; medical $0.25-0.35/sf recurring
- **S67** [Move-out / deep cleaning add-on guides](https://new.risingsunartscentre.org/news/move-out-deep-cleaning-cost-2026.html) - Appliance add-ons $40-150 each (low-quality source)
- **S68** [Clean Group - Cost to clean blinds](https://www.clean-group.com.au/cost-to-clean-blinds) - Commercial contracts 50+ blinds ~$8-15 each (vendor page, AUD market)
- **S69** [Fixr siding cleaning; commercial soft wash pricing guides](https://www.fixr.com/costs/siding-cleaning) - Residential $0.30-0.80/sf; commercial wall wash $0.20-1.00, soft wash $0.15-0.60/sf
- **S70** [Airtasker - Commercial kitchen cleaning prices](https://www.airtasker.com/us/commercial-cleaning/commercial-kitchen-cleaning/price/commercial-kitchen-cleaning-cost) - Commercial kitchen deep cleaning $50-150/hr
- **S72** [Contractor 2026 construction-cleaning price guides (FlexCrew, Brye A Plus, Housefly)](https://flexcrewusa.com/blog/post-construction-cleaning-cost-per-square-foot/) - Rough $0.10-0.30/sf, final $0.30-0.75 (homes) / $0.20-0.50 (large commercial), touch-up $0.10-0.20/sf or $150-500/visit; rough/light phases $35-60 per cleaner-hour
- **S74** [Auto-scrubber productivity specs (Elite Metal Tools) and manufacturer guidance](https://www.elitemetaltools.com/tool-shop/janitorial/automatic-scrubbers) - Practical productivity ~22,770 sf/hr for 32-in machine; 10,000-40,000 sf/hr by model
- **S75** [ContractorPlus - strip and wax rates](https://contractorplus.app/blog/set-profitable-strip-and-wax-rates-this-winter) - ~3-5 labor hours per 1,000 sf strip and wax (200-330 sf/labor-hr)
- **S77** [HomeStars - Industrial cleaning cost](https://www.homestars.com/demolition-disposal/price-guides/industrial-cleaning-cost) - Industrial cleaning ~$0.20/sf average; high dusting with lifts +20-40%
- **S79** [Parking lot / garage pressure washing guides and contractor forum](https://pressurewashingresource.com/community/t/indoor-parking-garage-quote-help/40130) - Lots $0.08-0.25/sf basic; enclosed garage bid at $0.20/sf
- **S80** [Water damage restoration cost guides](https://new.risingsunartscentre.org/news/mold-and-water-damage-repair-cost-2026.html) - $2-12/sf extraction through drying (low-quality source; verify with licensed restorers)
