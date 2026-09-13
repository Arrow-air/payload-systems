# RESEARCH — Drone spreading/dispensing systems + capsule pellet product data

Research agent output, **2026-08-06 (rev B)**. Supersedes rev A of the same
filename; rev A's product facts were **re-verified from the primary source in
this pass** (the EPA label PDF was downloaded and text-extracted locally, not
taken on trust), and this revision adds three bodies of work rev A did not have:

1. **The fragment-overfill wedge jam** (Thomas's 23:03 directive) attacked with
   the *rotary-airlock / bulk-solids* design literature, which has named,
   commercially proven solutions for exactly this failure — plus derived
   force/torque numbers (§5).
2. **New primary prior art**: two UAS pellet-dispenser patents and an aerial
   ignition sphere-dispenser patent that actually describe their singulators
   (§3.3, §3.4) — rev A only had marketing pages for this class.
3. **Fragment-discriminating count sensing** (electrostatic-field sensors used
   in pharma), which changes the sensing recommendation (§6).

Scope as tasked: (a) existing drone spreading/dispensing systems, (b) commercial
capsule / tebuthiuron-class pellet product data (hardness, moisture, dust,
dimensions), (c) mechanism catalogue for metering **exactly N ∈ 1..10** of a
12 mm / 1.18 g molded pellet from a ≥250-pellet hopper, on a drone, in dust.

Labelling convention (used on every claim):
- **[V]** verified by this agent from a cited primary source (label PDF, patent,
  datasheet, manufacturer spec page)
- **[V2]** verified from a secondary/trade source (trade press, vendor blog) —
  credible but not primary
- **[D]** derived by arithmetic from a **[V]** number; the derivation is shown
- **[A]** ASSUMPTION / engineering judgement — not sourced, must be tested

---

## 1. THE PELLET — what the product actually is

### 1.1 The product is **hexazinone**, not tebuthiuron

The research prompt (and CONTEXT.md §Pellet) hypothesised "tebuthiuron pellet
products, Spike 20P class". **That is the wrong chemistry for the named product.**

**[V]** EPA label, *CAPSULE HERBICIDE*, EPA Reg. No. 102162-1, stamped
2023-04-05, manufactured by/for **capsule Manufacturing, LLC** —
https://www3.epa.gov/pesticides/chem_search/ppls/102162-00001-20230405.pdf
(this agent downloaded the PDF and ran `pdftotext -layout`; quotes below are
literal lines from that extraction):

| Label field | Literal text |
|---|---|
| Header | `HEXAZINONE GROUP 5 HERBICIDE` |
| Active | `Hexazinone: 3-cyclohexyl-6-(dimethylamino)-1-methyl-1,3,5-triazine-2,4-(1H,3H)-dione)..... 75%` / `0.75 lb active/lb product` |
| Signal word | `DANGER  PELIGRO` |
| Net weight | `Net Weight: 3 oz., 1 lb., 6 oz. or 5.5 lb.` |
| **Pellet count** | `Approx. 378 pellets per lb of product. 1 pellet = approx. 0.0026 lb of product / 0.00198 lb of active` |
| Application method | `Apply CAPSULE HERBICIDE by hand or with an exact delivery handgun applicator or other exact delivery device to the soil around specific plants or in a grid pattern for area control.` |
| Dust | `persons out of treated area until dust has settled.` |
| Storage | `Store out of the weather.` / `PESTICIDE STORAGE: Avoid contact with floor and moisture.` |

Note **[A]**: the net-weight line is ambiguously punctuated — it is almost
certainly the three SKUs **3 oz / 1 lb 6 oz (22 oz) / 5.5 lb** (matching the
sibling product's SKUs, §1.2), not four sizes.

**[D] The single most useful number in this document:** 453.592 g/lb ÷ 378
pellets = **1.200 g/pellet**. Thomas measured **1.18 g** → agreement to **1.7 %**.
Thomas's pellet *is* the registered capsule pellet, and the manufacturer's
own declared nominal implies a tolerance band of roughly ±2 %.
→ Design to **1.18 g nominal, 1.10–1.30 g range [A]**.

**[D]** SKU → pellet count: 3 oz ≈ **71**; 22 oz ≈ **520**; 5.5 lb ≈ **2 079**.
**A 250-pellet hopper is about half a 22 oz jug; a 500-pellet hopper is one jug.**
That is an operationally meaningful capacity target — sizing the hopper to
**one full retail jug (≈520 pellets, 614 g)** makes field reloading a
pour-one-container operation with no counting or partial containers.
**Recommend 500+ pellets as the capacity goal**, consistent with Thomas's
"more capsules isn't a bad thing".

### 1.2 Sibling product for physical-property inference

**[V2]** *Pronone Power Pellet* (Pro-Serve Inc., EPA Reg. 33560-41) is also
**75 % hexazinone**, sold in the **same three SKUs**, with near-identical label
directions (same "1–2 pellets per inch of stem diameter", same mesquite /
red-berry-cedar language, no license required, no grazing restriction under
600 pellets/acre).
- 22 oz package = **975 pellets** —
  https://www.pro-serveinc.com/product-page/pronone-power-pellets-22-ounce-package-975-pellets ,
  https://www.pro-serveinc.com/pronone-power-pellets
- Label/MSDS — https://www.forestry-suppliers.com/Documents/138_msds.pdf
- **[D]** 623.7 g ÷ 975 = **0.64 g/pellet** (≈709 pellets/lb).
  **capsule's pellet is ~1.9× the mass of a Pronone pellet** — same
  chemistry and dose logic, deliberately bigger body.
- **[D] Consequence:** any COTS hand/pod applicator built around the Pronone
  pellet (~9–10 mm class) will **not** pass our 12 mm pellet. Do not assume
  existing applicator hardware transfers. Conversely, our design should be
  parametric enough (`PELLET_D`) to *also* run Pronone pellets — that doubles
  the addressable market for the same mechanism. Note the doubles risk: two
  0.64 g pellets fit where one 1.18 g pellet does, so a Pronone-configured
  pocket is a different part, not a different setting **[A]**.

### 1.3 Hardness / crush / moisture / dust — best available data

No hardness or friability figure is published for capsule itself
(confirmed again this pass; the vendor site exposes an SDS link but no physical
property sheet). The authoritative datum for this *class* of pellet (compacted
bentonite-carrier herbicide pellet designed for aerial grid application) remains
DuPont's Velpar Gridball patent:

**[V] US 4,172,714**, "Dry compactible, swellable herbicidal compositions and
pellets produced therefrom" — https://patents.google.com/patent/US4172714A/en
- Composition class: active 5–25 %, **swelling bentonite 20–60 %**, anhydrous
  sodium sulfate 5–15 %, urea 10–25 %, PEG 200–600 2–10 %, water 1–12 %.
- Example geometry: **16 mm dia × 9–11 mm long**, 0.75–2.0 cm³, apparent density
  **≥1 g/mL**, example briquettes ≈**2.1 g**.
- **Crush strength: pellets "resist crushing with loads less than about 7500
  grams, or 3.7 kg/cm²"** → **7.5 kgf ≈ 74 N**, normalised **0.36 MPa**.
- **Impact: "normally resist breakage for 5 drops" from 3 m onto hard surfaces.**
- **Moisture: on wetting "pellets will crack immediately after wetting and swell
  to about 2 to 3 times their original volume"** in 2–5 h; once crumbled, dried
  pellets **"do not rebond but remain crumbled."**
- Design intent quoted: strength exists specifically so pellets "can be better
  controlled during aerial application to achieve the desired grid pattern".

**[D] Scaling the crush number to our pellet.** 7500 gf ÷ 3.7 kg/cm² = 2.03 cm²
= 203 mm², which is the projected area of a 16 mm disc (π·8² = 201 mm²) — i.e.
the patent normalised crush force by **projected pellet area**. Applying
0.36 MPa to our 12 mm pellet's projected area (π·6² = 113 mm²):

> **Whole-pellet crush load for a 12 mm capsule-class pellet ≈ 41 N ≈ 4.2 kgf [D]**

This is the anchor number for §5 (jam shear) and for torque limiting. It is a
**derived, class-level estimate — it must be measured** (§8, test plan).

**Standard test methods to measure it properly [V2]:** granular-fertiliser
practice uses **IFDC S-115 crush strength** (single granule crushed between flat
platens, mean of 10, reported kgf) and **IFDC S-116 abrasion resistance**
(100 g sample tumbled in a rotary drum with fifty 5/16" ball bearings at 30 rpm
for 5 min, then sieved for fines) —
https://feeco.com/physical-specifications-for-granular-fertilizer-and-soil-amendment-products/ ,
https://www.sciencedirect.com/science/article/abs/pii/S0032591001004168 .
**These are exactly the two bench tests we need** (crush load for §5 torque
margin; drum attrition for the fines-per-sortie budget), and they are cheap.
Context for expectations: accepted crush limit for fertiliser granules is
~2 MPa; micronized sulphur-urea granules test 2.3–2.9 kgf/granule
(https://link.springer.com/article/10.1023/A:1009714306464). **Our class-derived
4.2 kgf is in the same order — this is a *weak* solid by machine-design
standards, and every pinch point must be treated as a fines generator [D].**

**Design consequences (all [D] from the above):**
1. **~41 N crushes a pellet.** A geared stepper at a 20 mm pocket radius reaches
   that at **0.8 N·m** — trivially attainable. The metering drive will *crush*
   before it stalls unless current-limited. **Two-stage torque policy required**
   (§5.4).
2. **5× 3 m drops survive** → an 8 m free drop onto ranch soil is inside the
   pellet's designed impact envelope. Landing fracture is not a failure (the
   pellet only has to dissolve).
3. **Swelling 2–3×, irreversible** → one rained-on/condensation-wetted pellet
   becomes an oversize plug that cannot be dried back into spec. **The hopper
   must be sealed (gasketed lid, drain-free floor) and "one swollen pellet" is
   a design jam case.** The label's own storage line — *"Avoid contact with
   floor and moisture"* **[V]** — is the manufacturer conceding this.
4. **The label admits the product is dusty** (*"until dust has settled"* **[V]**),
   and it is 75 % active on a bentonite/urea carrier. Assume a **dust film on
   every internal surface and every optical window** by end of sortie.
5. **[A]** Attrition estimate: a few tenths of a percent by mass per handling
   cycle; visible fines at the hopper base after a 20-min sortie under rotor
   vibration. **Measure with the S-116 drum test before freezing clearances.**

### 1.4 Geometry / density derivation

**[D]** True 12 mm sphere: V = 0.905 cm³ → ρ = 1.18/0.905 = **1.30 g/cm³**
(consistent with the "≥1 g/mL" class figure, on the high side).
**[D]** 12 mm-dia barrel (Thomas's photo shows a mold parting line and a slight
barrel): for ρ = 1.0/1.1/1.2/1.3 the implied length is 10.4/9.5/8.7/8.0 mm.
**[A]** Most likely: **12 mm dia × 9–10 mm tall barrel, ρ ≈ 1.1–1.25**.
**This shape anisotropy is a metering risk**: a barrel can lie flat *or* stand on
edge, so a pocket sized on the sphere assumption may admit a second pellet
edge-on. **Caliper 20 pellets on both axes before freezing pocket geometry.**

**[D]** Hopper volume: 250 spheres = 226 cm³ solid → at packing 0.55/0.60/0.64 =
**0.41/0.38/0.35 L**; bulk density 0.72–0.84 g/cm³. As 12×11 mm barrels
(1.24 cm³): 250 → 311 cm³ → **0.48–0.57 L**. For the recommended **520-pellet
(one-jug) capacity**: 0.8–1.2 L loose, **614 g of pellets [D]**.

### 1.5 Label-driven dose — why N is 1–10 and why scatter is *good*

**[V]** literal label directions:
- Single-stem: `apply 1-2 pellets for every inch of stem diameter`.
- Multi-stem incl. **Mesquite**, huisache, multiflora rose, 2–3 ft:
  `1-2 pellets at the base`; 3–6 ft: `2-4 pellets at the base`.
- **Red Berry Cedar (Juniper)**: `1-2 pellets for every 3ft of plant height or
  every 3ft of canopy diameter, whichever is greater`.
- Fence line: `1 pellet ... every 3ft of fence length`, heavy: `every 1.5ft`.
- Placement: `distribute the pellets uniformly around the stem out approximately
  half way between the stem and canopy edge` → **the label wants N≥2 pellets
  spread around the plant, not stacked.** A burst dropped from an 8 m hover
  naturally scatters ~0.3–0.8 m **[A]** — that is label-*favourable*. State this
  in the design rationale; it converts a dispersion "error" into compliance.
- **Rangeland/pasture cap [V]:** `DO NOT exceed 1 pound of product per acre
  (0.75 lb ai) per year`, `Maximum Applications: 1/yr` = **378 pellets/acre/yr**.
  Forestry/non-crop allow far more (10–11.5 lb/acre = 3 780–4 347 pellets/acre).
- **[V]** `by hand or with an exact delivery handgun applicator or other exact
  delivery device` — **"other exact delivery device" is the label category our
  counted dispenser falls in.** The label contains **no aerial broadcast
  directions**. Regulatory is out of scope per Thomas, but the framing matters:
  we are building an *exact delivery device*, not an aerial spreader.
- **[V]** Activation: `¼ to ½ inch of rainfall ... within 2 weeks`; response
  `3 to 6 weeks`.

### 1.6 The incumbent applicator: the "Brush Pod"

- **[V]** capsule Manufacturing sells an **Applicator Pod**, **$650**,
  **battery powered**, mounted by **1" ball mount or 1/4-20 thread**, described
  as a "Multi-Equipment capsule applicator" —
  https://capsule.myshopify.com/products/applicator-pod
  (re-fetched this pass: **the page still publishes no capacity, mass, rate,
  count-control or mechanism data**; it showed "9 units remaining").
- **[V2]** Vendor claims aerial use "by helicopter or other aerial platforms"
  via the Brush Pod — https://capsule.myshopify.com/
- **[V]** Internal prior art: Arrow DAO thread "capsule Applicator (aka.
  Brush Pod) Reverse Modeling" — Onshape assembly from photos, explicitly *"for
  aircraft layout reference only"*, several mm deviation, **no mechanism data** —
  https://dao.arrowair.com/t/capsule-applicator-aka-brush-pod-reverse-modeling/88
- **[V2]** Vendor video, applicator in use — https://www.youtube.com/watch?v=8JXTMeRnTko
- **HIGHEST-VALUE ACTION, unchanged from rev A and still not done:** **buy one
  ($650) and tear it down.** It is the only device in the world known to meter
  *this exact pellet*. Contact: info@brushbullet.com, +1 (806) 323-9921.

### 1.7 Tebuthiuron (Spike 20P) — checked, and it is a dead end for us

**[V2]** Spike 20P is **20 % tebuthiuron** pellets applied at **3.75–20 lb/acre**
broadcast (https://www.arborchem.com/product/68/spike-20p-25-lb-bag ,
https://www.domyown.com/spike-20p-herbicide-p-20850.html). Searched this pass
for per-pellet dimensions/mass/pellets-per-lb: **no manufacturer publishes them.**
Spike's pellet is a broadcast-rate product (small pellet, high pounds/acre) and
is **not per-plant counted** — the opposite of our dose model. **Conclusion: the
tebuthiuron line of products contributes nothing to pellet geometry or metering
requirements. Drop it from the requirement set** (CONTEXT.md §Pellet's
"tebuthiuron / Spike 20P class" reference should be corrected to hexazinone).

---

## 2. EXISTING DRONE SPREADING SYSTEMS — and why none of them can do this

### 2.1 COTS agricultural spreaders (DJI Agras, XAG, CFR)

| System | Key spec | Source |
|---|---|---|
| **DJI Agras T100 Spreading System 4.0** (current flagship, 2026) | 150 L / **100 kg**; **screw-feeder discharge**; **400 kg/min**; auger options: XL **0.5–10 mm**, large **4–10 mm**, medium **4–6 mm**, small **0.5–4 mm** | https://ag.dji.com/t100/specs |
| DJI Agras T70P | granules **0.5–10 mm** | https://www.dji.com/newsroom/news/dji-release-agras-t100-t70p-t25p |
| DJI Agras T40/T50 (prior gen) | 50 kg, 0.5–5 mm granules, spinner disc, weighing sensor closes the rate loop | https://www.dji.com/t40 , https://www.dslrpros.com/products/dji-agras-t50-spreading-system |
| CFR-Innovations UGS-2G / UGS-4G (drone-specific spreader) | **8 L / 16 L**, "adjustable spreading rate" set *before flight*, up to 30 m throw; **no counted-dose capability published** | https://www.cfr-innovations.com/ |
| XAG P150 / RevoSpray (Texas brush work, Gonzales County) | liquid, 30 L/min — cited because it is the current *commercial* answer to Texas brush | https://www.prnewswire.com/news-releases/for-texas-ranchers-fighting-invasive-brush-xag-drones-are-changing-the-odds-302715576.html |

**Findings:**
- **[V] Even the newest, largest COTS spreader tops out at 10 mm granules.** Our
  pellet is **12 mm — still above the top of the accepted range**, on an
  *auger* ("Screw Feeder Feeding") that would grind a 4.2 kgf pellet (§1.3) into
  fines. Rev A said "0.5–5 mm"; the 2026 hardware has moved to 0.5–10 mm and
  **still does not reach us**.
- **[V/D] Their metering is mass-rate closed on a weighing sensor, not count.**
  Minimum resolvable dose is orders of magnitude above 1.18 g. **A broadcast
  spreader physically cannot deliver "exactly 3".**
- **Conclusion: no COTS agricultural spreader is adaptable — not by tuning, not
  by an auger swap.** This is a purpose-built problem, and that is now a
  *citable* justification for building rather than buying.

### 2.2 Rate-based drone dispersal in the same mission space (context, not candidates)

- **[V2] AgAbove LLC (SE Arizona)** commercially applies **Spike 20P by drone**
  for rangeland brush at 3.75–10 lb/acre — broadcast rates, not counts —
  https://azelisaes-us.com/grow_your_know/revolutionizing-invasive-brush-control
- **[V2] Envico** production island-eradication baiting by drone; "full swath,
  directional swath, trickle and cluster baiting" — rate-based —
  https://www.envicotech.co.nz/drone-baiting
- **[V2] AirSeed Technologies** fires ~1 g carbon seed pods at **2 pods/second**,
  GPS-targeted, ~40 000/day — same mass class, same cadence, mechanism not
  disclosed — https://www.airseedtech.com/our-technology ,
  https://dronelife.com/2022/08/26/planting-trees-with-drones-airseed-delivers-seed-pods-for-drone-reforestation-initiative/
- **[V2] Historical baseline** for the grid application our pellet descends from:
  helicopter bucket spreader with Velpar Gridball, 27 m effective swath,
  19 ± 5 kg/ha against a 20 kg/ha target (**±26 % rate error**) —
  https://www.srs.fs.usda.gov/pubs/rn/rn_so255.pdf
  → **[D] The bar we are asked to clear (±0 pellets on a 1–3 pellet dose, within
  1 m) is ~2 orders of magnitude finer than incumbent aerial practice. That gap
  is the product.**
- **Prior *counted* capsule drone attempts: none found in the public
  record** (searched forums — TexasBowhunter, TexAgs, AR15.com — plus trade
  press; ranchers discuss the pellet and speculate about drones, and the vendor
  claims helicopter use, but **no published counted-pellet drone applicator for
  this product exists**). **This is greenfield.**

---

## 3. THE REAL ANALOGS — aircraft-mounted discrete-object dispensers

These are the systems that actually solve our problem shape: singulate a molded
body out of a bulk store, on an aircraft, in the field.

### 3.1 Drone Amplified IGNIS — the mass/capacity benchmark

**[V]** IGNIS III Mini: **max payload 225 spheres**, **sphere 19 mm dia / 2.4 g**,
**max drop rate 120/min**, glycol injection 0.2 mL per sphere, **loaded weight
1.87 kg**, empty payload 1.25 kg, reload 2–5 min, smart dovetail electro-
mechanical mount — https://droneamplified.com/ignis-system-datasheet/ ,
https://droneamplified.com/ignis-iii/ ; IGNIS II: 450 spheres, 120/min —
https://droneamplified.com/ignis/ . Mechanism, marketing level **[V2]**: hopper →
spheres forced down a feed path → each injected with glycol immediately before
release — https://droneamplified.com/ignis-system-safer-faster-prescribed-burns/

**[D] Why this is the benchmark:** a **1.87 kg loaded, 225-sphere,
one-at-a-time, drone-mounted, field-serviceable singulator exists and is
type-accepted for US federal fire operations.** Our pellet is *smaller and
lighter* (12 mm/1.18 g vs 19 mm/2.4 g) and we can delete the glycol pump,
needle, reservoir and injection dwell entirely. **Our ≤1.5 kg target with 295 g
of pellets is comfortably inside a proven envelope**, and IGNIS's 120/min rate
shows the cadence is not the hard part.

### 3.2 Premo / SEI Plastic Sphere Dispenser — the jam-reality benchmark

- **[V2] Mechanism:** *"The spheres are fed into **four chutes** which are
  controlled by **anti-jam slipper blocks**. The slipper mechanism moves the
  spheres into the glycol injection needle."* 45–130 drops/min, 24 V,
  3.25 L water reservoir plumbed to flood the injection area if a jam ignites —
  https://premofireusa.com/dispenser.html ,
  https://dartaerospace.com/products/premo%C2%AE-plastic-sphere-dispenser ,
  https://www.sei-ind.com/accessories/premo-plastic-sphere-dispenser/
- **[V] Jam reality**, PSD operator quoted by USFWS: *"The PSD has a tendency to
  jam, so you're constantly filling it with spheres and fixing jams."* —
  https://www.fws.gov/story/2023-09/aerial-ignitions-plastic-sphere-dispenser-operator
- **[V] Root causes**, USFS MTDC 1151-2312P *Better Performance of Aerial
  Ignition Spheres Through Proper Storage and Handling* —
  https://www.fs.usda.gov/t-d/pubs/htmlpubs/htm11512312/ : jams are caused by
  **misaligned sphere halves; excess plastic protrusions at the seams;
  misshapen/non-round spheres; clumped chemical; humidity-driven clumping;**
  and **aged, brittle spheres that "make PSD equipment dirty and cause jams"**.
  Mitigations: FIFO stock rotation, agitate stock 1–2×/yr, **cull defective
  units before loading**, protect from temperature swings and UV, clean often.
- **[D] Every failure mode the USFS documents is present in our pellet and
  mostly worse**: our pellet has a **mold parting line** (seam flash), is
  **moisture-swelling and irreversibly crumbling**, is **friable** (4.2 kgf),
  and **sheds dust by label admission**. Thomas's stated practice — *"we try to
  filter those out before loading"* — is exactly the USFS "cull before loading"
  mitigation, independently arrived at. **Cite this: pre-load culling is
  established best practice, not a workaround.**

### 3.3 US 9,199,735 — a *documented* aircraft sphere singulator (new this pass)

**[V]** "Apparatus for processing and dispensing incendiary capsules" —
https://patents.google.com/patent/US9199735B2/en (also
https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9199735).
This is the most mechanically detailed public description of an aircraft-mounted
sphere singulator, and it validates our architecture almost element for element:

- **Hopper (64)** *"can typically contain up to several hundred spheres"*, with a
  dedicated **agitator motor (64a)**: *"A certain amount of agitation is required
  to shake the spheres out of the hopper and in to the tube."*
  → **[V] Agitation is not optional in this class of machine.**
- **Feeding tube (64c)**: spheres *"line up in series within feeding tube"*, and
  *"when the lowest incendiary in line becomes presented with an empty cavity of
  the rotary feeder, that incendiary falls by gravity into that empty cavity."*
- **Rotary feeder (46) with five semi-circular cavities (46b)** — a **pocket
  wheel**, exactly our M1. Spheres *"settle one by one into semi-circular
  cavities."*
- **Dwell matters**: *"the feeder is stationary for about 83 % of the time"* —
  gravity fill is given a long dwell rather than being asked to fill on the fly.
  **[D] Design rule for us: index the wheel in discrete steps with a fill dwell
  of ≥60–80 % of the cycle, not continuous rotation.** This is a concrete,
  sourced parameter that rev A did not have.
- **Geneva drive (48/49/50)** with five radial notches gives exact 72° indexing
  — **the count is guaranteed by kinematics**, no controller involved.
- **Explicitly no electronics**: *"no electric pumps, no on-off valves, no
  solenoids, and no other non-mechanical inputs"* — and correspondingly
  **no jam detection and no count verification**. **[D] That is precisely the
  gap we are being asked to fill:** the mechanical art has the singulator; the
  *verified count* and *automatic jam recovery* are our contribution.

### 3.4 UAS pellet/briquette dispenser patents (new this pass)

- **[V] US 11,370,599 / US 10,499,628**, "Dispensers and methods of use thereof
  for dispensing solid mosquito larvicides and other materials of interest" —
  https://patents.google.com/patent/US11370599B2/en :
  UAS-mounted, **carousel (60) of eight chambers (65)**, one briquette per
  chamber, **lightening holes between chambers** to cut mass, manual loading
  through a loading port, **servo (35) drives an arm (55) → ratchet (50), with a
  pawl (30) preventing back-rotation**, one signal = one index = one release
  through the **exit port (22)**. *"The number, size and shape of the chambers
  can be scaled to accommodate various types of solid mosquito control
  products."* **No jam detection, no count verification, capacity 8.**
- **[V] US 2018/0016007 A1**, "Dispenser for unmanned aerial vehicles, platforms
  and systems" — https://patents.google.com/patent/US20180016007A1/en :
  compartmentalised carrier, per-compartment release (spring/smart-lock/magnet),
  and notably a **release-path optical counter**: *"the slide may also have a
  sensor, like a laser sensor, to account for every article that has moved down
  its surface, towards the target location."*
- **[V2] ASU / Skysong Innovations, "Drone Deployable Automated Pellet
  Dispensing System"** (Das, Keating, Brauer): 3D-printed drone payload for
  **metered** vaccine-pellet dispensing with an explicit **"anti-jamming
  mechanism"**, motivated because **"traditional [hopper-based] delivery means
  frequently jam"** —
  https://skysonginnovations.com/technology/drone-deployable-automated-pellet-dispensing-system/
- **[V2] USFWS/USGS sylvatic-plague-vaccine drone**: a **modified Lithuanian
  carp-bait machine** ("gumball machine" class) dropping **one bait at a time**,
  >1 M baits over 5 000 acres —
  https://www.fws.gov/media/drone-drops-plague-vaccine-baits-prairie-dog-habitat-ul-bend-refuge ,
  https://www.upi.com/Science_News/2016/07/12/FWS-to-use-drones-to-deliver-vaccine-laced-MMs-to-save-endangered-ferrets/2921468354747

**[D] Pattern across all four:** *every* fielded UAS discrete dispenser is either
(a) a **small fixed-capacity magazine** (8 chambers) with a geometric count and
no sensing, or (b) a **hopper machine that everyone admits jams**. **Nobody has
shipped hopper-fed + high-capacity + verified count.** Our differentiator is
exactly the intersection: **250–520 pellet hopper + geometric singulation +
sensed count + automatic jam recovery.** No public prior art blocks that; the
Skysong "anti-jamming mechanism" is the only IP worth a clearance check.

---

## 4. MECHANISM CATALOGUE

For each: **how it works · count accuracy · jam behaviour · complexity ·
adaptability to our 12 mm / 1.18 g / friable / dusty pellet.**
Scores are **[A]** engineering judgement anchored on the cited art.

### M1 — Rotary pocket wheel / cavity disc (indexed escapement) ★ RECOMMENDED
**How it works.** A disc or drum carrying one-pellet blind pockets indexes under
a hopper throat. In the load zone a pocket fills by gravity (dwell-limited); a
close-clearance housing arc closes the pocket through the transfer; the pocket
opens over the drop chute. **One index = one pellet.** Direct precedent:
US 9,199,735's five-cavity rotary feeder on an aircraft **[V]** (§3.3);
US 11,370,599's eight-chamber carousel on a UAS **[V]** (§3.4); mechanical
cell-wheel seed plates (https://www.kinze.com/which-seed-meter-is-right-for-you/);
and pharma **slat counters**, whose whole selling proposition is that *"counting
accuracy is guaranteed by filled cavity count, independent of sensors"* **[V2]**
(https://ipsnj.com/tablet-counting/ , https://imagroup.com/machines/slat-counter/).
- **Count accuracy [A]:** *geometric, not statistical* — a pocket that can hold
  one and only one pellet cannot deliver two. This is the entire reason to
  prefer it. Realistic **≥99 %** per index with exit-sensor confirmation and
  retry-on-miss; **effectively 100 % on the commanded N** because a miss is
  detectable and retryable, and an over-count is geometrically impossible.
  (Compare: vacuum discs 98–99 %+, mechanical finger meters 94–99 % —
  https://www.precisionplanting.com/products/planters/vset .)
- **Jam behaviour [A]:** the dominant risk is **the fragment-overfill wedge**
  (Thomas's directive) — see §5, which is now the longest section of this doc
  and gives sourced, named, commercially proven countermeasures (inlet shear
  deflector, trailing-edge bevel, flexible tip, side-entry V-throat, scalloped
  pocket) plus derived forces. Secondary risks: swollen pellet bridging the
  throat (M8 agitation required), fines packing the pocket floor (needs a fines
  escape slot).
- **Complexity [A]:** LOW–MEDIUM. One rotating part, one motor, one sensor. No
  vacuum, no air, no liquid. Fully printable/machinable; parametric on `PELLET_D`.
- **Adaptability [A]:** HIGH. Pocket depth/diameter is the only pellet-specific
  dimension; a Pronone variant is a swapped disc. **Caveat:** must verify a
  12 mm *barrel* cannot enter a pocket edge-on beside a first pellet — that is a
  measurement (§1.4), not an assumption.

### M2 — Reciprocating slide / shuttle escapement (single cavity)
**How it works.** A linear slide with one pellet-sized cavity shuttles between
"under the hopper" (fill) and "over the chute" (drop). One stroke = one pellet.
Classic industrial escapement-and-nest
(https://www.rnaautomation.com/products/feeding-and-handling/spares-standard-equipment/escapements-and-nests/ ,
https://www.roymech.co.uk/Useful_Tables/Cams_Springs/Escapements.html);
stop-gate/dispense-gate patent art https://patents.google.com/patent/US6064921A .
- **Count accuracy [A]:** exact per stroke by the same geometric argument;
  slightly worse than M1 in practice because an end-of-stroke partial fill is
  more likely than in a dwelling rotary pocket. Needs the exit sensor + retry.
- **Jam behaviour [A]:** **worse than M1.** A guillotine slide is a shear pair
  with a hard end stop; a fragment caught mid-stroke is crushed (fines) or
  stalls at full current. There is no "next pocket" for a wedged fragment to
  fall into, and no rotary-airlock trick applies. **If chosen, use a servo (not
  a solenoid)** so you get position feedback and reverse-retry, and put a spring
  in the drive train.
- **Complexity [A]:** LOWEST — a printed slide, a hobby servo, a microswitch.
- **Adaptability [A]:** HIGH (one critical dimension).
- **Verdict:** best *simplicity fallback / bench comparison*; inferior jam
  ergonomics. Keep as the risk-reduction backup build.

### M3 — Dual-gate airlock on a single-file column
**How it works.** Pellets queue single-file in a ~13 mm ID tube; two gates one
pellet apart alternate: upper closes → lower opens (one pellet falls) → lower
closes → upper opens (column advances). N cycles = N pellets. Same family as
ball-diverter/stop-gate art (https://patents.justia.com/patent/5474292).
Note US 9,199,735 **[V]** uses a feeding tube *feeding a pocket wheel* — the
column is a supply device there, not the meter.
- **Count accuracy [A]:** exact **iff** the column is truly single file and the
  inter-gate volume holds exactly one. With ±1 mm diameter tolerance, seam flash
  and a barrel that can cock, that condition is fragile → **95–99 %** unsensed;
  ~100 % with sensor + retry.
- **Jam behaviour [A]:** **the tube is the jam.** Columns of irregular dusty
  bodies bridge and cock; fines pack the wall; recovery would require reversing
  gravity. **Highest jam risk of the mechanical options.**
- **Complexity [A]:** LOW mechanically, but you must add a reliable single-filing
  stage between hopper and tube, which re-imports M1's complexity.
- **Adaptability [A]:** MEDIUM — the ID must bracket 11–13 mm bodies *and* be
  loose enough to clear seam flash; those requirements fight.
- **Verdict:** viable only as a **short magazine (≤10 pellets) refilled by an
  M1 pre-wheel** — which is a useful packaging trick if the belly envelope
  forces a thin dispenser.

### M4 — Helical coil / vending spiral
**How it works.** A wire helix in a tube; one revolution advances the column one
pitch and ejects one item. Standard snack-vending mechanism.
- **Count accuracy [A]:** one per revolution by geometry, but the vending
  industry's signature failure is the **"hung product" misvend** — the exact
  failure we cannot tolerate. **97–99 %** unsensed.
- **Jam behaviour [A]:** hangs at the coil exit; the standard recovery (keep
  turning) **breaks the count** — you get 0 then 2.
- **Complexity [A]:** LOW, but wants a horizontal coil gravity-fed from a
  magazine: bad packaging under a belly, and it needs single-filing first.
- **Adaptability [A]:** MEDIUM. Pitch must exceed pellet dia + clearance; a
  barrel can rotate within a turn and double up.
- **Verdict:** strictly dominated by M1.

### M5 — Auger / screw feeder
**How it works.** A screw carries material forward; metered by revolutions. This
is what **DJI's T100 actually uses** ("Screw Feeder Feeding") **[V]**.
- **Count accuracy [A]:** POOR. Augers meter volume/mass. One-pellet-per-turn
  pitch degenerates into M4. **Cannot do N=1.**
- **Jam behaviour [A]:** an auger is a **compaction device** — it will grind a
  4.2 kgf pellet (§1.3) against the barrel wall into fines and pack them.
- **Complexity [A]:** MEDIUM. **Adaptability:** LOW. **REJECT.**

### M6 — Vacuum pickup disc (precision planter)
**How it works.** Vacuum plenum behind a perforated disc picks one seed per hole
from a pool; a **brush singulator** knocks off doubles; vacuum is cut at drop.
- **Count accuracy [V2]:** the best-documented singulation in existence —
  98–99 %+, >99 % with an edge singulator
  (https://www.precisionplanting.com/products/planters/eset ,
  https://www.kinze.com/why-upgrade-to-vacuum-seed-meters/).
- **Jam behaviour [A]:** fatal for us — **vacuum meters inhale dust**. The
  orifice must be smaller than the pellet, so a 2–4 mm orifice pulling ranch
  dust plus hexazinone fines clogs within a sortie, and clogging degrades
  *silently* (skips, no stall to detect). Seed-treatment dust is already
  documented as degrading entrainment
  (https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7334532).
- **Complexity [A]:** HIGH — pump (5–15 W), plumbing, filter, regulation, on a
  **2 A/12 V = 24 W** rail.
- **Adaptability [A]:** LOW–MEDIUM (1.18 g is ~4× a maize kernel; holding it
  pushes pump size up).
- **Verdict:** right accuracy, wrong environment. **REJECT — but steal its brush
  singulator** (§5.2).

### M7 — Vibratory bowl / linear feeder + gate + optical count
**How it works.** Vibration walks pellets into single file past a counter/gate;
the pharma tablet-counting architecture (https://ipsnj.com/tablet-counting/).
- **Count accuracy [V2]:** >99.7 % photoelectric, >99.98 % with vision; modern
  heads discriminate tablet from tablet dust and fragments.
- **Jam behaviour [A]:** good — vibration is self-clearing, no shear pairs. But
  the *count* is open-loop against a moving stream: the gate must close between
  pellet 3 and 4 while the feed is still running. Pharma solves this by
  weight-verifying a batch afterwards; we cannot.
- **Complexity [A]:** HIGH on a drone — bowl mass, driver, and a vibration source
  rigidly coupled to an airframe that already has four rotors exciting it.
- **Adaptability [A]:** MEDIUM.
- **Verdict:** **reject the feeder, steal the sensor** (§6).

### M8 — Hopper agitation / anti-bridging (companion, not a meter)
**How it works.** Slow paddle, star agitator, wobble plate, or a flexed
compliant hopper wall breaks arches over the throat. **[V]** US 9,199,735 fits a
dedicated **agitator motor** and states agitation *"is required"*; **[V]**
USFS MTDC recommends agitating sphere stock to prevent clumping.
- **Necessity — now quantified [D]:** bulk-solids practice sizes an outlet to
  avoid *mechanical arching* of coarse particles at **≥6× the largest particle
  dimension** for a circular outlet (Jenike-derived rule of thumb; see
  https://jenike.com/solutions/solve-or-prevent-poor-flow/ ,
  https://www.chemengonline.com/facts-fingertips-hopper-outlet-geometry-arching/ ,
  and the "7–9× characteristic particle dimension" variant in the same
  literature). **For a 12 mm pellet that is a ≥72 mm free outlet** — which is
  wider than the entire pocket-wheel throat we can afford under a 50×50 mm clip
  plate. **Therefore our throat is, by construction, in the arching regime, and
  positive agitation is MANDATORY, not a nice-to-have.** This is the cleanest
  sourced argument in the whole document for why the agitator is not optional,
  and it should be quoted in the design rationale.
- **Complexity [A]:** LOW if the agitator is driven off the metering motor
  through a reduction or a crank; a compliant hopper wall excited by airframe
  vibration gives partial agitation for free (a genuine advantage of mounting
  under a multirotor).

### M9 — Load-cell verification (companion, not the primary count)
**How it works.** Weigh the hopper before/after: ΔM ÷ 1.18 g = pellets out. This
is how COTS spreaders close their loop (https://www.dji.com/t40).
- **Accuracy [D]:** resolving 1 pellet (1.18 g) out of a 614 g full load needs
  ~0.2 % of full scale — trivial on a bench (0.02 % FS cells are standard), but
  **rotor-induced vibration and aero loads at an 8 m hover will swamp a 1.18 g
  step [A]**, and the averaging needed fights a ~1 s dispense window.
- **Verdict [A]:** **not** a per-pellet in-flight verifier. **Excellent as
  (i) hopper-low/empty warning, (ii) end-of-sortie audit (total dispensed vs
  total commanded), (iii) pre-flight load count.** Cheap; recommend as a
  supplement.

### M10 — Ruled out, in writing
- **Spinner/broadcast disc** — cannot count; 0.5–10 mm particle spec **[V]** §2.1.
- **Auger** — §M5, and it makes fines.
- **Vacuum** — §M6, dust.
- **Pneumatic/blower ejection** — adds a blower, aerosolises a DANGER-signal-word
  dust (label: keep persons out until dust settles **[V]**), and gains nothing:
  an 8 m free drop is already ballistically adequate.
- **Paintball-loader force feed** — designed to feed as fast as possible, not to
  stop at N; its agitator paddles would abrade a 4.2 kgf pellet.

---

## 5. THE FRAGMENT-OVERFILL WEDGE JAM (Thomas 2026-08-06 23:03)

> *"a possible jam if a fragment gets in to the pocket wheel slot, you'd have 1.5
> capsules and it could prevent the wheel from turning"*

This is a **known, named, solved-in-industry problem**. The industry is **rotary
airlock / rotary valve** design, where a rotor with pockets turns inside a
close-clearance housing and hard lumps wedge at the "shear point" between vane
tip and housing. The vocabulary and the fixes transfer 1:1 to our pocket wheel.

### 5.1 The failure, in the source industry's own words
**[V2]** *"Shearing and jamming occurs when hard, large particles are introduced
and pinch between the rotating rotor vanes as they turn into the housing"*, and
jamming also occurs when a lump is *"larger than the size of the rotor pocket in
the valve"* —
https://www.powderbulksolids.com/valves-gates-airlocks/how-to-prevent-jamming-of-rotary-airlocks
This is exactly Thomas's "1.5 capsules" case: a proud fragment carried out
of the fill zone into the close-clearance arc.

### 5.2 Countermeasures — five named, commercially proven mechanisms
All **[V2]** from rotary-valve practice, with the mapping to our design **[D/A]**:

| # | Industry fix (quoted) | Source | Our implementation |
|---|---|---|---|
| 1 | **Inlet shear deflector** — *"fitted to the inlet of the rotary airlock and enables the material to avoid contact between the rotor vanes and the valve inlet"* | powderbulksolids (above) | A fixed deflector lip over the trailing edge of the hopper throat so the pocket edge never closes *against* the pellet column — the column is shadowed before the shear line arrives. **This is requirement #1 of the directive ("rejection before wedge") in hardware.** |
| 2 | **Side-entry throat with a V** — *"the inlet throat has a 'V' shape where the rotor enters the housing, which minimizes the pinch point"*, and *"the product is caught on the upswing of the rotor vanes so that the product is constantly falling away from the shear point"* | powderbulksolids | Feed the wheel on the **rising** side of its rotation with a V-relieved throat; gravity then continuously unloads the shear line instead of pressing pellets into it. |
| 3 | **Trailing-edge bevel** — *"A chamfer is made on the trailing edge of each vane, blade, or tip, which allows product particles to fall away."* | https://www.rotolok.co.uk/different-rotor-options-inside-rotary-valves | Chamfer the pocket's trailing lip (≥1×, suggest 2 mm × 45° **[A]**) so a proud fragment is cammed back into the hopper rather than pinched. |
| 4 | **Flexible tip** — *"if a particle becomes trapped between the flexible tip and the housing, the tip either gives way allowing it to fall into the next pocket or drags it around to the outlet where it falls out"*; tips in *"polyurethane or Teflon"*, adjustable/replaceable | powderbulksolids; Rotolok | **The single highest-value idea in this section.** Make the *housing shoe* over the fill-to-drop arc a compliant elastomer/PTFE wiper rather than rigid aluminium. A wedge then loads a **spring**, not a structure (see §5.3 numbers), and the fragment is either released back or carried to the chute. |
| 5 | **Scalloped / reduced-capacity pocket** — scalloping *"puts a radius in the bottom of each pocket to minimise clumping, which can stop the product falling out"*; reduced capacity gives *"throughput of a larger valve when a smaller valve would be a restriction for the particle size"* | Rotolok | Radiused pocket floor so a pellet always seats to the bottom (no fragment trapped underneath holding the pellet proud), and a deliberately **oversize wheel with small pockets** so the pocket-to-wheel size ratio is generous. |

Complementary from the seed industry **[V]**: the **adjustable singulating brush**
— nylon bristles (0.008 in dia, 340 per assembly) in tufts with a *"bristle
diverting rib"* that *"diverts a portion of the bristles to each side"* to reduce
stiffness and allow greater deflection on seed contact, adjustable in detented
increments from outside the housing without disassembly —
https://patents.google.com/patent/US7798080B2/en (see also
https://patents.google.com/patent/US10785904B2/en ,
https://patents.google.com/patent/EP2901833A1). **A compliant brush wiper at the
pocket exit is the proven "reject the overfill before it reaches the shear line"
device, and the patent gives us real bristle parameters and the design trick
(the diverting rib) for making a brush soft enough not to abrade a friable
pellet while still sweeping proud material.**

### 5.3 Why compliance beats strength — the numbers **[D]**
Model the wedge: a fragment standing **δ** proud of the shear line is squeezed
between disc face and housing. Normal force **N = k·δ**, where **k** is the
stiffness of whichever member yields. Drag torque **T = µ·N·r**.

- **Rigid aluminium housing:** k ~ 10⁴ N/mm ⇒ a δ = 0.3 mm fragment develops
  N ~ 3 000 N (limited only by the fragment failing) ⇒ with µ ≈ 0.4 and
  r = 20 mm, **T ≈ 24 N·m**. No sane drone actuator turns that. **Guaranteed
  hard lock.**
- **Elastomer wiper shoe, k ≈ 20 N/mm [A]:** the same δ = 0.3 mm gives N = 6 N;
  a gross δ = 1 mm gives N = 20 N ⇒ **T = µ·N·r = 0.4 × 20 N × 0.02 m
  = 0.16 N·m.** Comfortably inside a small geared stepper's capability.
- **Conclusion [D]: the wedge jam is a *stiffness* problem, not a strength
  problem.** Adding motor torque to defeat a rigid wedge is futile (24 N·m);
  adding 1–2 mm of designed compliance in the housing shoe reduces the same
  event to a 0.16 N·m speed bump — a **~150× reduction** for a few grams of
  polyurethane. **This should be the headline of the pocket-wheel jam defence.**

### 5.4 Shear-through as backstop, and the torque paradox **[D]**
Directive item 2 wants the actuator to be able to **shear a fragment** as a
backstop. But §1.3 says ~41 N crushes a whole pellet — so a drive strong enough
to shear is also strong enough to mill pellets into fines during normal running.
**Resolution: a two-stage torque policy** (this is the design answer to the
apparent contradiction):

| Mode | Current/torque | Intent |
|---|---|---|
| **Normal metering** | limited to ≈ **0.15 N·m at the wheel** ( ≈ 7.5 N at r = 20 mm — *well below* the ~41 N pellet crush load) | A trapped pellet **stalls**; it is never crushed. Stall is a *detection event*, not damage. |
| **Recovery (after stall detected)** | reverse-oscillate at the same low torque first; only if 2–3 oscillations fail, escalate to ≈ **1.0 N·m** ( ≈ 50 N at r = 20 mm, **> the 41 N crush load with ≈ 20 % margin**) for a bounded number of shear attempts, then declare a fault | Guarantees a fragment can be crushed/sheared through as a last resort, on purpose, with the count sensor armed. |

**[D] Sizing check:** 1.0 N·m at the wheel from a NEMA-11 stepper (0.06–0.09 N·m
holding) needs ≈ **15:1** reduction; from a NEMA-14 (0.14 N·m) ≈ **8:1**. Both
are small planetary or printed-cycloid ratios and are compatible with the
≤1.5 kg budget. Note the reduction also multiplies the *normal* torque, hence
current limiting — not gearing — must set the 0.15 N·m normal ceiling.
**[A] The 41 N crush figure is class-derived (§1.3) and must be replaced with an
IFDC S-115 measurement on real pellets before this margin is claimed as final.**

### 5.5 Detect and recover
- **Stall detection.** **[V2]** TMC2209 integrates **StallGuard4**, which
  measures the difference between electrical energy in and out to infer
  mechanical load, and is used for sensorless homing/stall detection —
  https://www.analog.com/media/en/technical-documentation/data-sheets/tmc2209_datasheet_rev1.08.pdf ,
  https://www.analog.com/en/resources/app-notes/an-002.html . **Caveats that
  matter for us [V2]:** StallGuard4 on the TMC2209 is **intended for StealthChop
  mode**, and the threshold (SGTHRS) is **speed- and current-dependent — any
  change to current or velocity requires recalibration**
  (https://thinkrobotics.com/blogs/tutorials/tmc2209-sensorless-homing-tutorial-complete-setup-guide ,
  https://deepwiki.com/kjk25/TMC2209_ESP32/4.4-stallguard-and-sensorless-homing).
  **[D] Design implication: run the metering index at ONE fixed speed and ONE
  fixed current so a single SGTHRS calibration is valid; do stall detection only
  in that regime, and use plain current/encoder-deviation sensing during the
  high-torque recovery mode** (where StallGuard is out of calibration by
  definition). A cheap independent backstop: a magnetic encoder (e.g. AS5600)
  on the wheel — commanded-vs-actual angle deviation is a speed-independent,
  driver-independent stall detector and also gives the "did the index complete"
  answer the count logic needs **[A]**.
- **Recovery routine [A]:** reverse 15–30°, re-advance; up to 3 cycles at normal
  torque; then up to 2 shear attempts at recovery torque; then fault.
- **Truthful counting through recovery [A]:** the count must be **owned by the
  exit sensor, never by the step count**. Rule: increment only on a validated
  exit-sensor pulse (§6), and **disarm/ignore the sensor during reverse motion**
  so a pellet rocking in the beam cannot produce phantom counts. On fault,
  report `commanded N`, `verified n`, and a jam bit — the interface contract
  must carry all three (this is inside Thomas's "electrical/command interface
  contract" scope).
- **Pocket geometry rule [A]:** pocket depth ≥ pellet major dimension + largest
  credible fragment thickness, so that **a fragment sharing the pocket with a
  pellet still settles below the shear line**. With a 12 mm pellet, a **14 mm
  deep, 13.5 mm dia radiused-floor pocket** leaves ~2 mm of sub-shear-line
  volume — enough for the fines and small chips that dominate the fragment size
  distribution, while a *large* fragment (>2 mm proud) is rejected by fixes
  1/3/4 above rather than carried. **The credible fragment size distribution is
  unmeasured — get it from the S-116 drum test (§8).**

---

## 6. COUNT VERIFICATION SENSING (Thomas: "VERIFIED (sensed), not assumed")

**Change from rev A: the primary recommendation is now a fragment-discriminating
sensor, with through-beam IR as the proven fallback.**

- **Electrostatic-field / capacitive counting — NEW RECOMMENDATION [V2].**
  Pharma uses **electrostatic field sensors (EFS, Sparc Systems Ltd)** instead
  of photoeyes precisely because of dust: *"the falling product disturbs the
  electrostatic field, and measuring this disturbance allows the detection of
  overlapping product as well as the differing mass of broken pieces so bottles
  containing fragments can be rejected"*, and they *"increase uptime because
  there's no need to stop the line mid-run to clean the sensor when handling
  extremely dusty products"* —
  https://www.pharmtech.com/view/ensuring-correct-tablet-count (this agent got a
  403 on direct fetch; text corroborated via
  https://www.sensorsportal.com/HTML/DIGEST/P_226.htm and
  https://www.researchgate.net/publication/242321559_Pharmaceutical_Pill_Counting_and_Inspection_Using_a_Capacitive_Sensor).
  **[D] Why this matters to us specifically:** it is the only sensing modality
  found that **(a) is immune to the dust film our label-admitted dusty pellet
  creates and (b) can tell a whole pellet from a fragment by its mass/field
  disturbance.** Both are direct requirements here — a fragment falling down the
  chute must NOT be counted as a pellet, or a "3 pellets delivered" report is a
  lie. **[A] Risk:** our pellet is a low-permittivity bentonite/urea solid, not a
  pharma tablet; sensitivity must be characterised on a bench with real pellets
  and real fragments before this is baselined. Implementation can be a simple
  guard-ring capacitive electrode pair around the chute plus a charge amplifier —
  no COTS drone part exists.
- **Through-beam (opposed-mode) IR — proven fallback [V2].** Opposed mode
  *"offers much higher excess gain than any other mode, making it ideal in dusty,
  smoky, foggy, misty or oily environments"* and is *"most reliable for accurate
  parts counting, as long as the diameter of the effective beam is no larger than
  the part"* —
  https://www.bannerengineering.com/my/en/company/expert-insights/3-photoelectric-sensing-modes-how-to-choose.html ,
  https://www.ttco.com/sensors/fundamentals . Banner's tablet-counting note adds
  the two constraints we must respect **[V2]**: through-beam is preferred because
  it is *"not affected by tablet color or reflectivity"*; response speeds of
  ~10 µs are available; newer sensors have *"active optical monitoring... to
  track the optical level"* and can *"compensate gain level... or output an alarm
  signal for maintenance, before the sensor becomes inaccurate"*; **and crucially
  *"the machine singulates individual tablets before they enter the sensing
  region"* because photoelectrics *"typically cannot accurately tell if more than
  one tablet goes through the sensing zone"*** —
  https://www.bannerengineering.com/us/en/company/expert-insights/how-to-use-photoelectric-sensors-for-tablet-counting.html
  **[D] This validates the architecture:** an optical counter is only trustworthy
  *downstream of a geometric singulator* (M1). It also means **the sensor cannot
  rescue a mechanism that can pass two at once** — another reason M1 over M7.
  Design notes **[A]**: recess emitter/receiver behind short tubes or an air gap;
  run high excess gain so a dust film costs margin not function; discriminate
  pellet from fines puff by **pulse width** (a 12 mm body at ~1–2 m/s occupies
  the beam ~6–12 ms; dust is shorter and noisier); self-test "beam clear" before
  each dispense so a caked beam faults instead of miscounting.
- **Motor position/current (encoder + StallGuard):** free, necessary for jam
  detection and index confirmation, **but it does not prove a pellet was in the
  pocket.** Necessary, not sufficient.
- **Load cell:** audit only (§M9).
- **Recommended stack [A]:** *index count (commanded)* + *chute sensor pulse,
  fragment-discriminating if characterisation succeeds, through-beam otherwise
  (verified)* + *load cell (audited)*. The interface contract returns
  **commanded N, verified n, fault/jam bits, hopper-low bit**.

---

## 7. RANKED RECOMMENDATION

1. **M1 indexed rotary pocket wheel** — geometric count, one moving part, and
   the only candidate with a *documented aircraft precedent* for singulating
   molded spheres from a hopper (US 9,199,735 **[V]**). Build it with the five
   rotary-airlock anti-wedge features (§5.2), a **compliant housing shoe** as the
   primary jam defence (§5.3, ~150× drag reduction), a **two-stage torque
   policy** (§5.4), **mandatory agitation** (§M8 — our throat is provably inside
   the arching regime), and a **fragment-discriminating chute counter** (§6).
   Index with a long fill dwell (≥60–80 % of cycle, per US 9,199,735's 83 %).
2. **M2 servo single-cavity slide** — the simplicity fallback and the bench
   A/B comparison. Same count logic, fewer parts, worse jam ergonomics.
3. **M3 short magazine (≤10) refilled by an M1 pre-wheel** — only if the belly
   envelope forces a very thin package.
4. Everything else: rejected with cited reasons (§M4–M7, §M10).

**Highest-value next actions, in order:**
1. **Buy the $650 Brush Pod and tear it down** (§1.6). Only device known to meter
   this pellet. Retires more risk than any further web research.
2. **Caliper 20+ pellets on both axes, weigh individually** — settle
   sphere-vs-barrel and the true tolerance before freezing pocket geometry (§1.4).
3. **IFDC S-115 crush test** on real pellets — replaces the derived 41 N with a
   measured number and validates the §5.4 torque margins.
4. **IFDC S-116 drum attrition test** — gives the **fragment size distribution**
   that §5.5's pocket-depth rule currently assumes, plus the fines-per-sortie
   budget.
5. **Deliberate-jam test** with (a) a pre-swollen pellet and (b) a machined
   worst-case fragment placed proud in a pocket — the critic's constructed jam,
   run on hardware.
6. **Bench-characterise a capacitive chute sensor** on real pellets and real
   fragments before committing to it over through-beam.

---

## 8. KNOWN GAPS / WHAT COULD NOT BE VERIFIED

- **No published dimension, hardness, friability or moisture spec for Brush
  Bullet specifically.** All §1.3 mechanical numbers derive from US 4,172,714, a
  same-class but **different** pellet (16 × 9–11 mm, ~2.1 g). The 41 N figure is
  **[D]**, not measured. The vendor's SDS was not retrievable in this pass
  either (site exposes SDS links; content not reachable) — **request it from
  info@brushbullet.com**.
- **Brush Pod mechanism, capacity, count accuracy: still not public**
  (re-checked this pass). Our internal reverse-model captures outer geometry only.
- **IGNIS singulator internals: not published** (marketing level only). The
  PSD's "four chutes + anti-jam slipper blocks" and US 9,199,735's rotary
  feeder + Geneva drive are the most detailed public descriptions in this class.
- **ASU/Skysong "anti-jamming mechanism": named, never described**; no patent
  number surfaced in two passes. Worth an IP clearance check before filing.
- **No public per-pellet count-accuracy figure exists for ANY drone pellet
  dispenser.** The 94–99 % / 98–99 % figures cited are ground precision planters
  and pharma counters — the nearest quantitative anchors available.
- **The "6× largest particle" hopper-outlet rule** is well attested as a rule of
  thumb across bulk-solids sources but the exact Jenike chart/threshold was not
  retrieved from a primary text in this pass (chemengonline's primer is
  paywall-limited; variants of 6× and 7–9× both appear). Treat 6× as
  order-of-magnitude — it is used here only to establish that our throat is in
  the arching regime by a wide margin, a conclusion robust to the exact factor.
- **Spike 20P / tebuthiuron per-pellet geometry: not published by anyone.**

---

## 9. SOURCE LIST

**Pellet / product**
- EPA label, capsule Herbicide, Reg. 102162-1 (downloaded + text-extracted this pass) — https://www3.epa.gov/pesticides/chem_search/ppls/102162-00001-20230405.pdf
- capsule vendor site / Applicator Pod — https://capsule.myshopify.com/ , https://capsule.myshopify.com/products/applicator-pod
- Brush Pod in use (video) — https://www.youtube.com/watch?v=8JXTMeRnTko
- Arrow DAO Brush Pod reverse model — https://dao.arrowair.com/t/capsule-applicator-aka-brush-pod-reverse-modeling/88
- Pronone Power Pellets (counts, label) — https://www.pro-serveinc.com/pronone-power-pellets , https://www.pro-serveinc.com/product-page/pronone-power-pellets-22-ounce-package-975-pellets , https://www.forestry-suppliers.com/Documents/138_msds.pdf
- US 4,172,714 — pellet composition, 7500 g crush, 3 m drop, 2–3× swelling — https://patents.google.com/patent/US4172714A/en
- Gridball helicopter swath/deposition — https://www.srs.fs.usda.gov/pubs/rn/rn_so255.pdf
- Spike 20P (tebuthiuron) — https://www.arborchem.com/product/68/spike-20p-25-lb-bag , https://www.domyown.com/spike-20p-herbicide-p-20850.html
- Granule crush/abrasion test standards (IFDC S-115 / S-116) — https://feeco.com/physical-specifications-for-granular-fertilizer-and-soil-amendment-products/ ; attrition sieve-shaker method — https://www.sciencedirect.com/science/article/abs/pii/S0032591001004168 ; NPK compression testing — https://link.springer.com/article/10.1023/A:1009714306464

**Drone spreading / dispensing**
- DJI Agras T100 specs (150 L, screw feeder, 0.5–10 mm augers) — https://ag.dji.com/t100/specs ; T100/T70P/T25P launch — https://www.dji.com/newsroom/news/dji-release-agras-t100-t70p-t25p
- DJI Agras T40 / T50 spreaders — https://www.dji.com/t40 , https://www.dslrpros.com/products/dji-agras-t50-spreading-system
- CFR-Innovations UGS drone granule spreader — https://www.cfr-innovations.com/
- XAG P150 Texas brush work — https://www.prnewswire.com/news-releases/for-texas-ranchers-fighting-invasive-brush-xag-drones-are-changing-the-odds-302715576.html
- Drone Amplified IGNIS III / datasheet / IGNIS II — https://droneamplified.com/ignis-iii/ , https://droneamplified.com/ignis-system-datasheet/ , https://droneamplified.com/ignis/ , https://droneamplified.com/ignis-system-safer-faster-prescribed-burns/
- Premo PSD (four chutes, anti-jam slipper blocks) — https://premofireusa.com/dispenser.html , https://dartaerospace.com/products/premo%C2%AE-plastic-sphere-dispenser , https://www.sei-ind.com/accessories/premo-plastic-sphere-dispenser/
- PSD jams, operator account — https://www.fws.gov/story/2023-09/aerial-ignitions-plastic-sphere-dispenser-operator
- USFS MTDC 1151-2312P sphere storage/handling & jam causes — https://www.fs.usda.gov/t-d/pubs/htmlpubs/htm11512312/
- **US 9,199,735** incendiary capsule processing/dispensing (hopper + agitator + 5-cavity rotary feeder + Geneva drive, 83 % dwell) — https://patents.google.com/patent/US9199735B2/en
- **US 11,370,599 / US 10,499,628** UAS larvicide briquette dispenser (8-chamber carousel, servo + ratchet + pawl) — https://patents.google.com/patent/US11370599B2/en
- **US 2018/0016007 A1** UAV dispenser (compartments + laser counting sensor) — https://patents.google.com/patent/US20180016007A1/en
- ASU/Skysong drone pellet dispensing system ("anti-jamming mechanism") — https://skysonginnovations.com/technology/drone-deployable-automated-pellet-dispensing-system/
- SPV bait drone (carp-bait "gumball" machine) — https://www.fws.gov/media/drone-drops-plague-vaccine-baits-prairie-dog-habitat-ul-bend-refuge , https://www.upi.com/Science_News/2016/07/12/FWS-to-use-drones-to-deliver-vaccine-laced-MMs-to-save-endangered-ferrets/2921468354747
- Envico drone baiting — https://www.envicotech.co.nz/drone-baiting
- AirSeed — https://www.airseedtech.com/our-technology , https://dronelife.com/2022/08/26/planting-trees-with-drones-airseed-delivers-seed-pods-for-drone-reforestation-initiative/
- AgAbove / Spike 20P by drone — https://azelisaes-us.com/grow_your_know/revolutionizing-invasive-brush-control

**Jam / metering / bulk solids**
- Rotary airlock jamming (inlet shear deflector, flexible tips, side-entry V-throat) — https://www.powderbulksolids.com/valves-gates-airlocks/how-to-prevent-jamming-of-rotary-airlocks
- Rotor options (bevelling, scalloped, reduced capacity, flexible/wood-waste blades) — https://www.rotolok.co.uk/different-rotor-options-inside-rotary-valves
- Rotary airlock principles/rotor design — https://www.powderbulksolids.com/valves-gates-airlocks/rotary-airlock-valve-principles-and-rotor-design
- Hopper arching / outlet sizing — https://jenike.com/solutions/solve-or-prevent-poor-flow/ , https://www.chemengonline.com/facts-fingertips-hopper-outlet-geometry-arching/ , https://www.powderprocess.net/Silo_discharge.html
- Adjustable singulating brush (bristle spec + diverting rib) — https://patents.google.com/patent/US7798080B2/en ; air seed meter adjustable singulator — https://patents.google.com/patent/US10785904B2/en ; seed-double eliminator — https://patents.google.com/patent/EP2901833A1
- Vacuum meter singulation & dust effects — https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7334532 , https://www.precisionplanting.com/products/planters/eset , https://www.kinze.com/why-upgrade-to-vacuum-seed-meters/ , https://www.kinze.com/which-seed-meter-is-right-for-you/ , https://www.precisionplanting.com/products/planters/vset
- Escapements — https://www.roymech.co.uk/Useful_Tables/Cams_Springs/Escapements.html , https://www.rnaautomation.com/products/feeding-and-handling/spares-standard-equipment/escapements-and-nests/ , https://patents.google.com/patent/US6064921A , https://patents.justia.com/patent/5474292
- Slat counters (cavity-guaranteed count) — https://ipsnj.com/tablet-counting/ , https://imagroup.com/machines/slat-counter/ , https://www.packingmachineinc.com/blogs/slat-counter-vs-electronic-counter-which-one-is-better-for-tablet-counting/

**Sensing**
- Electrostatic-field tablet counting (dust-immune, fragment discrimination) — https://www.pharmtech.com/view/ensuring-correct-tablet-count , https://www.sensorsportal.com/HTML/DIGEST/P_226.htm , https://www.researchgate.net/publication/242321559_Pharmaceutical_Pill_Counting_and_Inspection_Using_a_Capacitive_Sensor
- Vision-based broken-tablet detection — https://data-technologies.com/tablet-counter/ , https://raupack.co.uk/machinery/tablet-counting-inspection-system.aspx
- Banner: photoelectric tablet counting (singulate before sensing) — https://www.bannerengineering.com/us/en/company/expert-insights/how-to-use-photoelectric-sensors-for-tablet-counting.html ; sensing modes / excess gain in dust — https://www.bannerengineering.com/my/en/company/expert-insights/3-photoelectric-sensing-modes-how-to-choose.html , https://www.ttco.com/sensors/fundamentals
- TMC2209 StallGuard4 — https://www.analog.com/media/en/technical-documentation/data-sheets/tmc2209_datasheet_rev1.08.pdf , https://www.analog.com/en/resources/app-notes/an-002.html , https://thinkrobotics.com/blogs/tutorials/tmc2209-sensorless-homing-tutorial-complete-setup-guide , https://deepwiki.com/kjk25/TMC2209_ESP32/4.4-stallguard-and-sensorless-homing
