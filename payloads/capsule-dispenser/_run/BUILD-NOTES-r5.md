# BUILD NOTES — Round 5 (CAD builder)

Winning concept: **pocket-wheel**. Round 5 closes the r4 critics' blocking
issues (buildability FAIL 7, pellet-path PASS 8 with four MAJORs, interference
PASS 9.5, mass-budget PASS 8.5 — `BUILD-NOTES-r4.md` §"Round 4 critics").

Every number marked *measured* is printed either by `cad/dispenser.py` itself
or by `cad/verify_exports.py`, a second script that reads **only the exported
STEP/STL**, never imports the model, and types its coordinates in by hand so a
silent parameter change shows up as a failed probe. Facts from CONTEXT are
cited; everything else is [D] (derived, math shown) or ASSUMPTION.

## Deliverables

- Model: `cad/dispenser.py` (parametric build123d; pellet-facing dims driven by
  `PELLET_D`/`PELLET_D_MAX` = 12/13; the r4 hard-coded meter Z constants are
  now all derived from the stack, which is what let the funnel angle change
  land safely)
- Independent checker: `cad/verify_exports.py` (rewritten for r5)
- Auto-generated `cad/BOM.md` (buildability PROCESS item: part numbers used to
  live only inside print statements)
- Exports (`cad/exports/`): `dispenser_r5_assembly.step/.stl` + individual
  STEP+STL for all **11 printed parts** (top_plate, pcb_pedestal, fill_cap,
  hopper, meter_housing, pocket_disc, agitator, **brush_holder**,
  retaining_plate_chute, electronics_bay, bay_lid)
- Renders (cream #faf7f0): `cad/renders/r5_iso.png`, `r5_section.png`,
  `r5_meter_detail.png`, `r5_bottom.png`, `r5_fill_station.png`,
  **`r5_cartridge_out.png`** (the service state r4 could not reach),
  `r5_bay_lid.png`

## Root cause of the r4 BLOCKER, and the structural fix

r4's blocker was not a dimension error: it was an **architecture** error.
The agitator was clamped to the disc hub, so it was a *cartridge member* whose
fingers had to pass a solid roof that the cartridge could never clear (critic:
853 mm³ of swept interference, 1077 mm³ over 12 mm of descent). r4's own
insertion/tool-path harness had been applied to screws and the brush but the
cartridge drop-out was "verified" with a Ø26.4 cylinder probe standing in for
the real part — a stand-in probe, not a swept solid.

**r5 removes the agitator from the cartridge entirely.** It is now a free
rotor that sits on the sump floor, is centred by the disc hub and driven by a
**hex spigot** on it; the cartridge slides straight out of the hex. The hub
runs in a **COTS flanged sleeve bushing** seated in the roof — which also
closes the r4 GAP "no bearings anywhere in the design".

**Harness rule adopted in r5: no stand-in probes for motion.** Every service
motion is now a swept union of the *actual exported solids*, stepped, against
every static part (cartridge drop-out 21 steps × 4 members, wiper slide-out 20
steps × 2 parts, agitator lift 16 steps, fill-cap lift, latch swing).

## Blocking issues from the r4 critics — disposition

### buildability critic (r4 score 7, FAIL)

| Issue | Disposition |
|---|---|
| **BLOCKING: cartridge service removal is kinematically impossible** (agitator fingers 0.50 mm over a solid roof; swept descent 1077 mm³, full-cartridge sweep 860 mm³) | **FIXED by re-architecting the drive.** Agitator = free rotor on the bushing flange, driven by a Ø15-AF hex spigot on the disc hub; it is no longer bolted to anything (its unreachable set screw is deleted). Measured, model **and** independently on the exports: full cartridge sweep (unlock 22°, then 60 mm descent in 21 steps, 4 members × every static part) = **0.00 mm³**. The r4 pose is reproduced in the render `r5_cartridge_out.png` |
| **BLOCKING consequence: jam access** — the only real path was "empty the hopper, undo 3 screws, lift the hopper, reach the agitator set screw inside the funnel throat"; documented nowhere | **FIXED + DOCUMENTED.** With the cartridge out, the wiper station and roof entry edge are open from below: Ø8 and Ø12 rods from below to θ=133 (wiper plane) and θ=130 (roof edge) read **0.00 mm³** on the exports. The agitator set screw no longer exists. The drain-before-service procedure is written down (below) and its residue is measured |
| MAJOR: refill with gloves — 6.70 mm of cap lift inside 7.40 mm of headroom | **PARTLY FIXED, honestly bounded.** Neck shortened and lugs thinned: lift now **6.45 mm** vs **7.39 mm** headroom — but the measured killer is stated for the first time: after lifting, the cap needs **62 mm of lateral travel** inside a 10.5 mm gap shared with the airframe belly. **On-aircraft refill is NOT claimed.** Procedure = quick-release the payload (that is what the COTS 2112 QR is for), refill on the tailgate. A Ø2.2 **lanyard hole** is modeled in the wing bar so the cap is not a droppable loose part in wind |
| MODERATE: undisclosed sub-2 mm sections; 1.0 × 4 mm annular web is the only radial section carrying the cartridge into the lugs | **FIXED + now measured every run.** Inner fines slots pulled from r44.5 to **r43.6**, rim slots from r45.4 to **r45.7** → measured web **2.1 mm** (export probe; the model's 0.1 mm-quantised scan reports 1.9). A new **inward ray-cast wall-thickness harness** (6000 rays/part, grazing hits filtered) prints min/p1/p5 and the %-under-1.95 mm for all 11 parts, every run |
| MODERATE: hopper wall cut to 1.7 mm at the two fill-line grooves | **FIXED** — the fill lines are now **raised internal ribs** (triangular, 45° both faces → support-free), rooted 0.5 mm into the wall. Measured on the export: wall material at both line heights **100%** of a full-thickness probe; rib volume 524 / 312 mm³ |
| MINOR: brush-slot ceiling 1.5 mm | **DESIGNED OUT** — the wiper seat is now an **open-topped rebate** (the sump floor is its ceiling), so there is no thin ceiling section at all; 3.80 mm of roof remains *under* the seat at the inner support |
| GAP vs brief: no bearings anywhere, no bearing PN; Ø92 disc located solely by the stepper's internal bearings | **FIXED** — igus iglidur JFM-2022-04-class flanged sleeve (ID20/OD22, flange Ø26, L4) in the roof bore; the Ø20 hub journals in it 20 mm above the pellet bed. [D] p = 3 N/(20×4) = **0.0375 MPa vs ~35 MPa** iglidur static limit (930×). Honest limit stated: **L/D = 0.20**, so it constrains disc *tilt* and takes the bed load off the motor bearings — it is not a precision journal. The set screw was moved so the journal surface is **unbroken** (measured: 97.5 of 97.5 mm³ solid in the r9.5–9.9 band over the sleeve) |
| MINOR: no sensor retention feature | **FIXED** — an M3 grub pilot enters each IR pocket from below, 90° to the optical axis, so emitter/receiver can be clamped and re-seated after a swab-out without glue |
| MINOR: orientation search only tried rot 0/180 | **FIXED** — all six axis-aligned orientations are searched; best and as-modeled are both printed and land in `BOM.md` |
| PROCESS: no BOM; part numbers only in print statements | **FIXED** — `cad/BOM.md` is generated from the model each run (volumes, masses, print orientation, support %, COTS table with status) |

### pellet-path critic (r4 score 8, PASS — MAJORs closed anyway)

| Issue | Disposition |
|---|---|
| **MAJOR: sump aperture is 3.5× smaller than documented** ("~95 mm orifice" in CONCEPT §3; really 27.0 mm) | **ACCEPTED, measured, and the number is struck.** r5 measures it every run and re-measures it on the export: open radial run containing the PCD = **r20.25…46.75 = 26.50 mm × 120°**, equivalent circular orifice **D48.7**, i.e. **2.04× the worst-case pellet**. CONCEPT-pocket-wheel §3's "~95 mm" is WRONG and must be replaced by "26.5 mm annular window, 2.04 × D". The anti-bridging defence is the agitator, not the aperture |
| **MAJOR: the wiper is a solid printed fin with no bristle retention feature** — falsifies concept §2.3 "compliant" | **FIXED** — the wiper is now **two parts**: `brush_holder` (printed, with a real **1.8 × 1.0 mm bristle channel**, measured empty at r24/32/44 on the export) and `brush_bristles` (COTS strip, 1.6 mm backing, modeled). Measured **free trim 4.25 mm** — bought by taking the roof from 4 to 6 mm, since the roof is cut away over the fill sector. Compliance [D]: one Ø0.15 nylon filament k = 0.0024 N/mm, ~30 in contact ≈ 0.07 N/mm vs the r4 CF-PETG fin at **5.7 N/mm (78× stiffer)**. Honest limit stated: this is a **short-trim** strip brush, not the 20 mm Kinze trim the concept alludes to |
| **MAJOR: the highest-probability jam site is unreachable by any straight field tool** | **FIXED** — see the buildability BLOCKING-consequence row: with the (now working) cartridge drop-out, Ø12 rods reach the wiper plane and the roof entry edge from below at 0.00 mm³ |
| **MAJOR: no isolation gate — dropping the cartridge dumps up to 507 g of pellets, and the real procedure is written down nowhere** | **REBUTTED with a measured procedure, not a gate.** A rotary shutter or slide gate in this sump means shearing friable pellets with a printed edge and ~16 g, to solve a *ground* problem. Written procedure: **quick-release the payload → invert over the tub → remove the fill cap (Ø46) → drain → re-right → quarter-turn the cartridge out.** Measured residue that can still fall: everything below the funnel outlet plus one pellet layer = **111 cm³ ≈ 49 pellets**, not 393. Open issue 2 keeps a catch-tray/《gate》decision on the bench list |
| MODERATE: BUILD-NOTES-r4 carried a stale fragment-gap number (4.25 vs the true 2.70 mm) | **FIXED** — nothing is asserted from memory any more: the gap follows `BRUSH_WIPE`, and the seated-pellet/wiper/roof clearances are printed from the model each run (seated worst-case pellet top 1.5 mm below the disc surface; wipe line disc+1.2; roof underside disc+1.5) |
| MODERATE: 60.0° funnel is at/below the printed-PETG mass-flow threshold; the agitator does not reach 78 % of the cone | **FIXED (angle) / bounded (reach).** Funnel steepened to **68.0°** (measured back off the exported hopper: 68.0), cylinder shortened 55 → 40 mm so the stack only grows 1.7 mm from this change. The agitator still only stirs the sump — that is inherent to a one-motor architecture and is now stated rather than implied; the 68° wall is the reason it no longer has to |
| MODERATE: sump floor is a 0° shelf with a 460 mm² unswept outer ring | **IMPROVED** — fingers extended to **r46.5** (chamber wall r47): unswept ring now **147 mm²** (−68 %), film under the fingers **0.55 mm** (unchanged) |
| MINOR: fines slots are 3–4 mm, not 4.0 | Accepted; r5 prints slot bands rather than a claimed width (inner 40.5–43.6, rim 45.7–46.8, mid 19.5–23.5) |
| MINOR: silent uncommanded release path for ≤4 mm fragments from a parked pocket | **ACCEPTED AND RECLASSIFIED** — the run now prints it as an **uncommanded release class** (park lens 4.01 mm) and shows it is intrinsic: closing it needs pocket_r + exit_r ≤ 12.49 mm, i.e. an exit hole smaller than a pellet |
| MINOR: chute is vertical at x = +32, contradicting CONCEPT §5's "angles the drop line back to the centreline" | **DOC FIX** — the geometry is right (Judge 3 wanted exactly this); CONCEPT §5's sentence must be struck. The run prints "straight vertical at (32, 0), ZERO imparted lateral velocity" |
| MINOR: 1.0 mm rotating shear gap around the disc | Carried into the attrition open unknown (open issue 6); unavoidable in this architecture, and the fines path out of it is the rim trough |
| NIT: set screw had 0.00 mm of top margin | **FIXED** — M2.5 grub at disc+1.4 (z −288.3): **2.85 mm** below the shaft top, engagement probe 1.45 mm³, and it now sits **below the bushing**, so the bearing surface is unbroken |

### mass-budget critic (r4 score 8.5, PASS)

| Issue | Disposition |
|---|---|
| MODERATE: the 430-pellet MAX line's rationale had <1 % margin at the optimistic density | **FIXED** — the line is **solved from a pessimistic ledger** (CF-PETG 1.31, stepper 200 g, +10 % contingency) with an explicit **20 g reserve**: **N_MAX = 393**, strict no-exemption total **1480.0 g**. And it is no longer a groove cut into the wall |
| MODERATE: every printed part priced at 100 % infill, convention never stated | **FIXED** — the convention is stated in the ledger header, and a **measured voxel infill bracket** (0.6 mm voxels, EDT erosion 1.6 mm = 4 × 0.4 walls, 25 % infill) prints per part: printed parts **519.5 g solid → 343.6 g sliced**, i.e. 176 g of the ledger is a modelling artifact (LOADED @250 would be 1080.6 g). The ledger keeps the conservative figure |
| MODERATE: the >1.0 kg justification was prose | **FIXED** — a block-by-block partition of the 274.1 g overage is printed: stepper 190.0 + capacity oversizing 61.1 (the 44 mm of cylinder wall above the 250 line, computed) + latch ring/lugs 16.5 + 6.6 of the fastening/phase-hardware block = 274.1 g, 0.0 unattributed |
| MINOR: estimate exposure understated (117 claimed, 155 real) | **FIXED** — printed: **149.3 g (16.8 %)** of the 890.1 g empty subtotal is not measured from geometry, the stepper's vendor 190 g counted separately, and it is stated that the 10 % contingency does not bound it |
| MINOR: brush_strip was both a printed part and a 10 g COTS line | **FIXED** — split: `brush_holder` printed and **measured at 1.0 g**, `brush_bristles` COTS at 3.0 g [J] |

### interference critic (r4 score 9.5, PASS)

Both NOTEs carried unchanged (blind-mate PCB position ASSUMPTION — the
pedestal is a separate shimmable part; foam-compression note irrelevant at
189.7 mm of clearance). Re-measured after the stack change.

## Measured numbers (r5)

Model run and independent export run agree on every shared figure.

- **Connectivity:** 17/17 parts single solids in-model; **11/11 exported STEPs
  re-import as 1 solid**; 11/11 part STLs watertight; assembly STL = **17
  bodies, 17 watertight**; assembly STEP = 17 solids
- **Envelope:** bbox X ±75, Y −90…+75, Z −358.2…−171.0 → stack **187.2 mm**,
  **ground clearance at rest 189.69 mm** (ground Z −547.89) vs the 40 mm
  requirement. Full-gear mesh-to-mesh clearance **83.42 mm** (unchanged; the
  governing pair is the gear adapter to the top-plate corner, and the top
  plate did not move). Props (cited, r3 critic full-assembly): vertical gap
  152.5 mm, radial 239.3 mm
- **Service (the r4 blocker):** cartridge drop-out sweep **0.00 mm³** (model)
  and **0.00 mm³** (exports, 21 steps × 4 members × every static part) vs
  r4's 860.07; agitator lift-off 30 mm vs hopper/housing **0.00/0.00**;
  Ø8/Ø12 rods from below to the wiper plane, roof edge and fill arc
  **0.00 mm³**; wiper slide-out 0–40 mm in 20 steps **0.00 mm³**
- **Bearing/drive:** iglidur ID20/OD22/flange Ø26 × L4; journal band 4.0 mm at
  z −286.90…−282.90; counterbore seat 100 % open; hub journal 99.8 % solid in
  the bore; hex engagement **5.70 mm** at 15.0 AF with 0.4 AF clearance;
  bushing flange stands 0.30 mm proud and is the agitator's thrust face
- **Wiper:** holder 4.0 × 2.0 mm with a 1.8 × 1.0 channel (channel measured
  empty at r24/32/44); **free trim 4.25 mm**; I = 10.7 mm⁴ → at the stepper's
  6 N ceiling σ = **7.6 MPa**, deflection 0.058 mm; inner seat floor 3.80 mm
  of roof (34.2 mm³ probe); outer end carried by an M3 into a wall pilot
  (40.0 mm³ of thread stock) with the end tab covering the window mouth;
  free height above the holder at the wall **0.00 mm** (the hopper cone foot
  closes the seat)
- **Meter:** pocket pitch 25.1 mm, web 10.1 mm; seated worst-case pellet
  1.5 mm below the disc top; stacked second sphere protrudes 11.5 mm (wipe
  line 1.2); restack window 3° = 1.7 mm at PCD; roof entry ramp material
  starts 129.0° @ disc+2.0 and 125.0° @ disc+5.0
- **Sump:** aperture **26.50 mm × 120°** (equivalent D48.7, 2.04 × the 13 mm
  worst case); funnel **68.0°**, cone height 55.7 mm; agitator sweeps to
  r46.5, film 0.55 mm, unswept ring 147 mm²
- **Pellet transit, Ø13 worst-case sphere, 23 stations, 0.000 mm³ everywhere**
  (fill port cap-off → hopper → funnel wall tangent at 4 angles incl. all
  three skirt-tab angles and the tab top → funnel outlet → resting on the
  sump floor at two radii → resting on the disc → **seated in a pocket with
  the disc actually indexed** at 180/133/130/90/45/0° → exit hole → chute →
  IR beam → below the aircraft); re-run independently on the exports
- **Fastening paths:** 4/4 nut pockets open (0.00 skin), 3/3 skirt screws with
  0.00 mm³ Ø8 driver corridors and 41.0 mm³ of pilot stock, 4/4 lid screws
  0.00, 2/2 rib driver paths 0.47, set screw engages the shaft (1.45 mm³)
- **Wall thickness (inward ray-cast, min/p1/p5, % under 1.95 mm):** top_plate
  0.61/1.43/2.40, 2.7 % · hopper 0.27/2.26/2.28, 0.4 % · meter_housing
  0.11/2.40/2.45, 0.7 % · pocket_disc 0.50/4.56/6.51, 0.4 % ·
  retaining_plate_chute 0.03/2.00/2.00, 0.7 % · electronics_bay
  0.25/2.00/2.00, 0.7 % · bay_lid 0.03/2.00/2.00, 0.4 % · fill_cap
  0.90/1.30/1.40, 5.5 % · agitator 1.50/1.50/1.50, 11.7 % (the socket roof) ·
  **brush_holder 0.90/0.97/1.01, 31.8 %** (deliberate — it is a 4 × 2 mm bar,
  stress-checked above) · pcb_pedestal 1.75/1.76/2.01. Sub-0.5 mm *minima* are
  single-sample chamfer/edge artifacts; p1/p5 are the load-bearing figures
- **Plate webs:** solid runs at θ=160/200/260/300 → r38.0–40.5, **r43.6–45.7**,
  r46.8–47.9 → critical web **2.1 mm** (r4: 1.0 mm over ~176°)
- **Fill cap:** lift required **6.45 mm** vs 7.39 mm of headroom; 62 mm of
  lateral travel needed to clear the plate edge → off-aircraft refill
- **Sensing:** IR beam 40 mm below the plate, v = 0.89 m/s, ~17 ms occlusion,
  faces recessed 5.0 mm, retention grub pilots added; Hall cavities 0.00 mm³
  overlap with the exit bore (margins 40.7 / 49.7 mm)
- **Capacity:** usable hopper volume **1082 cm³ → 474 pellets worst-case
  barrel packing (559 g) / 659 sphere basis — 1.90× the 250 hard minimum,
  PASS**. Molded ribs: **MAX = 393** (891 cm³ below the line, re-measured
  391), **baseline = 250** (565 cm³, re-measured 248)
- **Interference:** 136 pairs, 40 bbox-overlapping pairs boolean-checked,
  **0 collisions, 0 check-failures**; cap locked/inserted 0.00/0.00; 3 lug
  swings 0.00; agitator swept annulus 0.00 × 6; motor↔chute 1.4 mm
- **Print orientations (best of 6, as-modeled in brackets):** top_plate 2.0 %
  (42.0), pcb_pedestal 0.0 (0.8), fill_cap 4.1 (39.2), hopper 0.8 (2.5),
  meter_housing 7.8 (18.8), pocket_disc 0.6 (0.6), agitator 8.9 (11.2),
  brush_holder 1.4 (16.2), retaining_plate_chute 2.5 (24.8), electronics_bay
  7.6 (10.3), bay_lid 0.0 (2.4)
- **Mass ledger (printed parts measured from solid volumes, 100 % infill):**
  empty total **890.1 g** + 10 % contingency → **979.1 g carried empty**;
  **LOADED @250 = 1274.1 g (226 g under the 1.5 kg ceiling)**; LOADED @393
  (MAX rib) = **1442.9 g**; brim @474 = 1538.5 g (pellet mass above the 250
  baseline is exempt per CONTEXT). Sensitivities: stepper 200 g → 1285.1 g;
  CF-PETG 1.31 → 1300.3 g; steel clip plate → 1339.0 g (all pass).
  Slicer bracket: 519.5 g of printed parts → **343.6 g** at 4 walls + 25 %
  infill → LOADED @250 would be 1080.6 g

### Over-1.0 kg justification (partitioned, per the mass critic)

274.1 g over. Stepper 190.0 (it *is* the torque limiter — 6 N at the pocket
lip, 12× under the crush load, no separate clutch) + capacity oversizing 61.1
(the 44 mm of 2.5 mm cylinder wall above the 250-pellet line, 49 cm³ —
CONTEXT makes extra capacity an explicit goal) + latch ring and plate lugs
16.5 (carries the ~500 g cartridge and makes the jam path tool-free) + 6.6 of
the fastening/phase-hardware block = **274.1 g, nothing unattributed**. The
justified blocks total 443.7 g, i.e. 169.5 g more than the overage.

## Documentation corrections this round forces (into CONCEPT/README)

1. CONCEPT §3 "the open-arc sump keeps the orifice at ~95 mm" → **26.5 mm
   annular window × 120°, equivalent D48.7, 2.04 × the worst-case pellet.**
2. CONCEPT §5 "the chute angles the drop line back to ~the airframe
   centerline" → **the chute is straight and vertical at x = +32 mm**; that is
   the correct choice (Judge 3) and the concept sentence is wrong.
3. CONCEPT §2.3 "COTS nylon strip-brush segment, ~20 mm trim" → **~4.25 mm of
   free trim** is what this envelope affords; compliance is per-filament, not
   per-trim-length.
4. CONCEPT §6 mass table → superseded by the r5 ledger (979 g empty carried,
   1274 g @250).
5. Service procedure (new, must ship in the README): drain by inversion
   through the fill port before any cartridge removal; residue ≈ 49 pellets.

## Open issues for round 6 / bench

1. **Caliper survey still gates the print** — `DISC_T`, `POCKET_R`,
   `BRUSH_WIPE` must be re-frozen against 20+ real pellets (all-judges item
   #1; not closable in CAD).
2. **No isolation gate** (rebutted, not fixed): a cartridge drop with a
   *loaded* hopper still spills ~49 pellets. If the bench disagrees with the
   drain-first procedure, the cheapest addition is a catch tray on the
   cartridge, not a shearing shutter.
3. Sensor bench test with dusty/fragmented pellets freezes the dark-time
   thresholds; capacitive-ring fallback envelope preserved (chute ID 22).
4. **Min index period ≥ 150 ms is a contract requirement**, not a geometric
   guarantee — must land in the ICD command section.
5. The agitator is retained by **gravity only**. Inverting the payload to
   drain drops it off the hex; it cannot leave the hopper (OD 93 vs the Ø46
   port) and the funnel outlet limits its radial float to 1.0 mm so it
   re-seats within 30° of hand rotation on the chamfered spigot — but this is
   an argued behaviour, not a tested one.
6. Attrition/fines: the 1.0 mm disc-rim shear gap, the wiper contact and the
   0.55 mm finger film are all fines sources feeding the only count sensor.
   Unmeasured (survey open unknown #2).
7. Bristle trim of 4.25 mm is short for a "brush". If the caliper survey shows
   flat pellets, this is the first thing that needs re-engineering — probably
   by lifting the wiper into the sump on a bridge and accepting a nip with the
   agitator fingers.
8. Bushing L/D = 0.20 and a JFM-2022-**04** length is a PN ASSUMPTION; if only
   6 mm is catalogued, either machine it down or deepen the roof by 2 mm.
9. Gasket grooves at the perimeter joints are still schematic (only the fill
   cap O-ring gland is real geometry); fill-cap anti-rotation detent still
   unmodeled (O-ring friction is the interim retention).
10. Clip-plate orientation ASSUMPTION (counterbore face = drone side) and
    blind-mate PCB position ASSUMPTION remain; the pedestal is shimmable.
11. Electronics/fastener/seal estimate lines total 149.3 g (16.8 % of empty)
    and are larger than the 10 % contingency that nominally bounds them.
12. Skirt-tab joint is 3 × M3 plastite into printed pilots carrying the
    cartridge + pellet column in tension (41.0 mm³ of thread stock per pilot);
    pull-out to be verified on the printed part.
13. Near-empty skip behaviour remains bench-unproven (concept §10.3).


---

## Round-5 critics

### critic: interference

- score: 4
- pass: false

#### issues

- BLOCKING — the 4 mount bolts land in the clip plate's blind-mate window, not in plate material. I placed 2112_attach_plate_payload_side.step exactly as dispenser.py does (Rot(X=90), XY-centred, top face Z=-171.0 → occupies Z -181.50..-171.00, 50.00×50.00×10.50, 11.52 cm³) and mapped it by 0.05 mm point-containment. It is a 4.0 mm solid base slab (Z -181.5..-177.5) plus a perimeter frame above, with a THROUGH window at x -8.00..+8.00, y -12.00..+12.00 (16×24 mm, open the full 10.5 mm). The design pattern (±6.5, ±10.5) sits INSIDE that window — 1.50 mm from the x edge and 1.50 mm from the y edge. The real mounting holes are 4 × Ø2.96–3.00 at (±19.00, ±19.00), a 38×38 pattern, open through the whole thickness. dispenser.py's own 'probe' is a Ø2.4×10 cylinder at (6.5,10.5) reading 0.775 mm³ residual against a `USE_CB_PATTERN = v_cb < 5.0` threshold — a false positive on the window, not a hole: an M3-size Ø3.2×10 probe there leaves 7.66 mm³ and Ø3.4 leaves 17.52 mm³ of material. Consequence: the 1274 g loaded payload has NO verified structural attachment; the 4 M3 screws + hex nut pockets in top_plate at (±6.5,±10.5) clamp air and stand in the drone's blind-mate pocket. The error is orientation-independent (open issue 10 does not cover it) because the window is a through-window either way. Fix path exists: top_plate has 109.6–140.0 mm³ of material in an R3×5 mm column at each (±19,±19).
- BLOCKING — the blind-mate electrical interface cannot mate: 35.0 mm Y offset. The drone-side Attachment Interface PCB (3331, placed by quiver source at the bottom port, CoM (0.52,-0.14,-158.90)) measures X -8.00..+8.00, Y -12.00..+12.00, Z -163.73..-151.27 — it exactly fills the clip-plate window and matches the ICD (23.5×15.8 mm board, 'alignment is provided by the quick-release mechanism'). The r5 payload pedestal is at X ±10.00, Y -41.00..-29.00, Z -181.50..-172.60 with its PCB body at Y -42.90..-27.10, top Z -171.00. Payload material inside the 16×24×10.5 mm (4032 mm³) window column, checked across all 11 exported STEPs: 0.0 mm³. Pads sit 35.0 mm aft of the pins. BUILD-NOTES-r5 carries this as an unchanged ASSUMPTION and says the pedestal is 'shimmable' — shimming is in Z, the error is 35 mm in Y, and the closing data was in the referenced quiver files and the ICD all along.
- MAJOR — the mis-placed payload PCB is also the tightest clearance in the whole aircraft-payload pair. Full-drone clash scan (drone.stl built from quiver.assembly, 20.55 M faces, sub-meshed below Z=-100, ~2.0 M faces, KD-tree over ~494 k dispenser samples vs ~294 k drone samples): excluding the intended 50×50 QR mating block, the minimum separation is 2.14 mm — payload PCB at (7.4, -27.1, -171.5) vs the drone-side QR plate edge at (7.4, -25.0, -171.0), same Z, i.e. sitting in the clip-on approach path with no tolerance analysis behind it.
- MODERATE — the 'independent' checker does not check the interface at all. cad/verify_exports.py (288 lines) never imports the clip plate, the landing gear, the props or any quiver geometry; it types the -171.0/-181.5 stack in from the docstring. Every mount/airframe number in BUILD-NOTES-r5 traces to dispenser.py alone, so the entire mount-interface error class is invisible to the harness the notes present as the anti-self-deception mechanism.
- NOTE — payload hardware outside the 50×50 interface footprint with no published keep-out. Above the clip-bottom plane (Z > -181.5) 394 of 2982 dispenser vertices lie outside the 50×50 column: pcb_pedestal (Y -41..-29), its PCB (Y -42.9..-27.1) and the fill cap (Y 36..44, top -178.4). Measured clear of all drone hardware today (drone-side QR plate X ±25/Y ±25/Z -171..-155; spacer 2131 X ±25/Y -25..+30/Z -155..-125; release levers |X| 18..33, Y ±6.5, Z -170.0..-157.5; lower plate underside Z=-125.0), but the ICD mechanical TODO 'Formal keep-out / envelope STEP' is still open, so this is unprotected volume.

#### numbers

GROUND CLEARANCE (requirement >=40 mm): dispenser lowest Z = -358.20 (chute exit); ground plane from landing gear built from /tmp/pq-main/src/quiver/airframe_structure/landing_gear (gear STL bbox Z min = -547.88; analytic foam bottom -527.89 - 40/2 = -547.89) -> CLEARANCE = 189.68 mm, margin +149.68 mm. PASS. Builder's 189.69 confirmed.
LANDING-GEAR MESH-TO-MESH: 83.42 mm, governing pair = dispenser top-plate rim (-52.4, 53.7, -181.5) to gear main adapter (-103.4, 107.5, -143.3). Builder's 83.42 confirmed exactly.
PROPS: tip radius 305.1 mm (disk dia 610.2 mm) about axes (+-449.43, +-449.43); dispenser max radius from centreline 93.4 mm -> radial gap to swept disk 251.1 mm (builder cited 239.3, i.e. conservative). Vertical: prop lowest Z -18.50 vs dispenser top -171.00 -> 152.50 mm. Confirmed.
ENVELOPE: X -75.0..+75.0, Y -90.0..+75.0, Z -358.2..-171.0, stack 187.2 mm, 17 bodies. Matches notes.
CLIP PLATE (measured, 0.05 mm containment scan): 50.00 x 50.00 x 10.50 mm, 11.52 cm3; solid slab Z -181.5..-177.5 (4.0 mm); through-window x -8.00..+8.00, y -12.00..+12.00 open over the full 10.5 mm; real holes 4 x dia 2.96 (x) / 3.00 (y) at (+-19.00, +-19.00) = 38 x 38 pattern, through-going. Design pattern (+-6.5, +-10.5) is inside the window, 1.50 mm from both edges. Model probe dia2.4 x 10 residual 0.775 mm3 (threshold <5.0 = false pass); dia3.2 x 10 residual 7.66 mm3; dia3.4 residual 17.52 mm3. top_plate material at (+-19,+-19) in R3 x 5 mm column: 109.6 / 140.0 mm3 of 141.4.
BLIND-MATE: drone-side 3331 placed X -8.00..+8.00, Y -12.00..+12.00, Z -163.73..-151.27 (ICD board 23.5 x 15.8 mm). Payload pedestal X +-10.00, Y -41.00..-29.00, Z -181.50..-172.60; payload PCB Y -42.90..-27.10, top -171.00. Payload material inside window column (4032 mm3): 0.0 mm3. Offset 35.0 mm in Y.
FULL-DRONE CLASH: min separation excluding the QR mating block = 2.14 mm (payload PCB (7.4,-27.1,-171.5) vs drone plate edge (7.4,-25.0,-171.0)); QR mating faces touch at 0.02 mm as intended.
INTERNAL STATIC INTERFERENCE (11 exported r5 STEPs): 55 pairs, 17 bbox-overlapping, max boolean overlap 0.005 mm3 (top_plate x fill_cap), 0 check failures. Clean.
BELLY / FILL CAP: lower plate underside Z = -125.0; spacer 2131 X +-25, Y -25..+30, Z -155..-125; QR plate X +-25, Y +-25, Z -171..-155; levers |X| 18..33, Y +-6.5, Z -170.0..-157.5. Fill-cap flange (0,40) r27.5 does pass under the QR plate (overlap Y 12.5..25), plate bottom -171.0 vs cap top -178.4 -> 7.4 mm headroom; builder's 7.39 mm confirmed honest. Nearest belly equipment: camera 3270 at 45.1 mm.
FOOTPRINT: 394 of 2982 dispenser vertices above Z=-181.5 lie outside the 50x50 clip footprint (pedestal, its PCB, fill cap).

### critic: pellet-path

- score: 5
- pass: false

#### issues

- BLOCKING — the transfer-arc entry has NO relief geometry on the pellet-facing side; the claimed '45-deg lead-in ramp' is cut into the wrong face. Measured on meter_housing_r5.stl by vertical containment scans at r=24.5/28/32/36/39.5/43/45.5: the ceiling (first housing material above the disc) is None at theta=130.00 and 1.508 mm at theta=129.90 — a square step within 0.1 deg (0.056 mm of arc at PCD 32) — and then flat at 1.508 all the way to the exit at every radius. The 45-deg cut is on the roof TOP: at r=32 the housing spans disc+1.51..2.06 at 129 deg, +1.51..4.29 at 125, +1.51..7.51 at 122. Face-normal extraction confirms it: the only entry face with a tangential component has normal (-0.77,-0.64,0.00), n_z=+0.00, n.travel=-1.00 (purely horizontal, facing straight upstream). BUILD-NOTES-r5 cites its own probe ('material starts 129.0 deg @ disc+2.0 and 125.0 deg @ disc+5.0') as proof of a lead-in; that probe is measuring the top chamfer and is evidence of the opposite. Fix is one line: mirror the ramp_cut onto the roof underside so the ceiling descends from disc+7.5 to disc+1.5 over ~8 deg.
- BLOCKING — the constructed wedge jam (CONTEXT directive, Thomas 2026-08-06 23:03) is NOT defeated. Worst-case fragment built from the measured pocket: bore r7.52, top chamfer r9.42@disc-top -> r7.52@-2.0 mm, depth 14.0 + 0.5 under-gap. A ~2.0 mm thick sliver (a mold-parting-line spall of a 12 mm pellet) drops into the crescent beside a seated D13 pellet and seats at y=3.43 mm above the pellet centre (4.57 mm below the disc top) where the sphere/bore wedge half-angle is 15.9 deg — BELOW the friction angle 21.8 deg at mu=0.4, i.e. self-locked. Any such sliver >=6.08 mm tall stands proud of the 1.508 mm ceiling; its drive contact is on the CYLINDRICAL bore (below the 2 mm chamfer), so the reaction is purely horizontal — no lift. Swept check on the exports (Dia4 fragment on the seated pellet crown, 0.25 deg steps): 1.50 mm proud -> no contact anywhere; 2.50 and 3.50 mm proud -> first and only contact is the square roof edge at theta=129.9. All three defences then fail by the design's own numbers: brush 30x0.0024=0.072 N/mm -> 0.29 N at 4 mm deflection vs 5.63 N of drive (19x too weak); shear backstop explicitly '12x under the pellet crush load' (dispenser.py line 1762), i.e. CONTEXT hard requirement 2 is rebutted, not met; and reverse-oscillate cannot un-wedge a self-locked sliver — it only backs the pocket off the edge so the next forward index re-jams.
- BLOCKING/MAJOR — the rigid wiper holder leads the compliant bristles for every object more than 5.45 mm proud, so the one CONTEXT-required compliant element never gets first contact in the band that matters most. Measured: holder underside disc+5.45, top disc+7.45 (bristle channel roof at +6.44), leading face at theta=136.6 with normal n_z=-0.00, n.travel=-1.00 over 77.6 mm2 — a 2.0 mm tall square face across the whole radial span r13.5..52.6. The bristle strip (1.6 mm wide) only spans theta 131.6..134.4, i.e. 2.2 deg (1.2 mm at PCD) DOWNSTREAM. Swept confirmation: a fragment 5.50 mm proud first touches brush_holder at theta=139.25 and only reaches the housing at 133.0. A 45-deg chamfer on the holder's leading underside (or dropping the holder so the bristles lead) costs nothing.
- MAJOR — there is no torque budget anywhere in the model or the notes, and the one number quoted is not achievable. 18 N*cm at PCD 32 mm = 5.63 N, not the 6.0 N asserted in BUILD-NOTES ('6 N at the pocket lip'), before any derate for running torque. Unbudgeted parasitic loads on the same shaft: the agitator (3 fingers measured at theta 0/120/240, Dia4, r10..46.4, dragging through the bottom of a ~1073 cm3 pellet column — order 0.04-0.08 N*m by Janssen estimate, ASSUMPTION), disc-on-bed friction under the 125-deg window (order 0.03 N*m), and the M5 spring-plunger detent engaging a Dia4 x 1.5 mm deep rim dimple at r46 — a commodity M5 plunger at 8-30 N of end force needs 0.2-1.1 N*m to release, i.e. 1x to 6x the motor's ENTIRE 0.18 N*m holding torque. No plunger PN or spring rate is specified. If that number lands badly the disc does not index at all, and in every case the net force available at the pocket to reject or shear a fragment is well under the quoted 5.6-6 N.
- MODERATE — the governing bulk-flow dimension is the 26.5-28.0 mm sump window, 2.04-2.15x the 13 mm worst-case pellet, which is below every no-arch criterion (>=3xD for a slot, >=6xD for a circular outlet -> 39 mm needed), and 67% of the sump floor is a 0-deg dead shelf. Measured: funnel 68.3 deg from horizontal (claim 68.0, PASSES the >60 deg rule) down to the outlet at r47.66, but the pellets then land on a FLAT roof top and the only path to the disc is the 125-deg window (measured open 125.5..250.0 deg at r=32, radial run r20.0..48.0 at z=-282.5). Dead shelf = 4374 mm2 of the 6494 mm2 floor. CONTEXT permits this only because active agitation is present — but the agitator is hex-driven 1:1 off the disc hub, so it only turns during a dispense, and (never stated in the notes) it has ZERO relative motion over the pockets: it can stir the bed but cannot clear pocket overfill or re-level pellets above a pocket. Its fingers also sit at disc+8.06..12.05 (measured z -281.64..-277.65), so they cannot touch anything perched in a pocket.
- MODERATE — the drop-through window at the exit is only 1.18x the free-fall time, and the '>=150 ms index period' contract is not derived from it. The pellet centre is within the measured port rim (r10.5 at the plate top) for 18.89 deg of the 45 deg index = 63 ms at a 150 ms index; clearing the 14.0 mm pocket takes 50-53 ms of free fall. Below ~127 ms of index period the pellet is carried past the port, stays in the pocket (at the -22.5 deg park a D12 pellet centre is 10.99 mm from the port axis, outside the 10.5 mm rim, so it cannot drop late) and the commanded pellet is silently not delivered. Open issue 4 lists 150 ms as a contract item but never states that it is a hard kinematic floor with 18% margin.
- MODERATE — the declared uncommanded-release class is understated 1.4x because the model's own probe uses an exit radius that is not in the part. dispenser.py computes the park lens with 'exit hole r9' (lens 4.01 mm) and probes with Cylinder(9.0); the exported plate measures port radius 10.5 mm at the plate top face (-304.25), 9.75 at -305.0, 9.05 at -306.0 — a 45-deg chamfer whose TOP edge (r10.5) is the rim that actually retains. True lens = 10.5+7.5-12.486 = 5.51 mm, and the kinematic full-escape bound is Dia <= 5.56 mm. The shipped statement 'fragments >= 4.0 mm RETAINED when parked' should read 5.5 mm.
- MINOR — 'ZERO imparted lateral velocity' (printed every run, and slated for the README) is wrong. At the 150 ms minimum index the pocket is moving 167.6 mm/s at PCD when the pellet is released, so the pellet enters the Dia22 chute with up to 0.17 m/s of tangential velocity, drifts up to 8 mm over the 50 mm chute and must contact the bore (4.5 mm of clearance from the axis). The chute contains it, but the claim as written feeds the 1 m accuracy budget an unearned zero.
- MINOR — the unswept sump ring is 343 mm2, not the claimed 147 mm2. Fingers reach r46.4-46.5 (measured); the bed's outer boundary at the sump floor plane is the hopper cone foot at r47.66 (measured inner radius at z=-282.0), not the r47 chamber wall used in the claim. Dead ring = pi(47.66^2-46.5^2) = 343 mm2, 1.16 mm wide, right in the funnel-to-floor corner where fines pack.
- MINOR — park retention margin is zero at the bottom of the assumed pellet tolerance band. At the 22.5 deg detent the pocket centre is 12.486 mm from the port axis; pocket play (7.52 - r_pellet) lets the pellet centre reach 11.49 mm (D13), 10.99 (D12) and 10.486 (D11) against a 10.5 mm rim edge. D11 — the low end of CONTEXT's stated +/-1 mm ASSUMPTION — sits exactly on the chamfer edge (-0.014 mm). It is still geometrically retained (it cannot descend without moving further inward), but there is no margin, and this is the number the open-issue-1 caliper survey has to close.

#### numbers

MEASURED ON THE EXPORTS (trimesh containment/ray probes on cad/exports/*_r5.stl, independent of dispenser.py). Channel dimensions along the full path vs the 13 mm worst-case pellet: fill port clear bore Dia46.2 (3.55x) -> hopper cylinder Dia140 -> funnel 68.3 deg measured from horizontal (inner r 65.37@z-238 ... 47.66@z-282, PASSES >60 deg), outlet Dia95.3 (7.3x) -> sump window 26.5-28.0 mm radial x 125.0 deg arc (open 125.5..250.0 deg; radial run r20.0..48.0 at z-282.5) = 2.04-2.15x (FAILS the >=3xD slot criterion; relies on agitation) -> disc top 7.51 mm below the sump floor -> pocket Dia15.04 x 14.0 deep + 0.51 under-gap, top chamfer r9.42->r7.52 over 2.0 mm (1.16x) -> TRANSFER CEILING 1.508 mm (smallest dimension in the machine; square step, None at 130.00 deg / 1.508 at 129.90 deg, all radii r24.5-45.5) -> disc rim gap 1.05 mm, under-gap 0.51 mm -> exit port r10.5 at the plate top / r9.05 bore (Dia18, 1.38x) -> chute Dia22.0-22.1 (1.69x; two-body arch geometrically excluded, max centre separation 10 mm < 12 mm) -> IR tunnel clear at z-348.2. WIPER: holder underside disc+5.45, top +7.45, channel roof +6.44, leading face theta=136.6 with n_z=-0.00 / n.travel=-1.00 over 77.6 mm2; bristle band theta 131.6..134.4 only, free trim 4.25 mm, 0.072 N/mm -> 0.29 N at 4 mm vs 5.625 N drive (19x). ROOF: underside flat 1.508 at every radius from 129.9 deg to the exit; top chamfer 1.51-2.06 @129, 1.51-4.29 @125, 1.51-7.51 @122; leading-face normal (-0.77,-0.64,0.00). SWEPT FRAGMENT (Dia4 on the seated pellet crown, 0.25 deg steps): 1.00/1.50 mm proud = no contact; 2.50/3.50 = roof edge at 133.5/133.0 (edge at 129.9 + 3.58 deg half-width); 5.50/6.50/7.50 = brush_holder at 139.25/140.0/140.0. CRESCENT WEDGE: w=2.0 mm seats 4.57 below the disc top, wedge half-angle 15.9 deg < friction angle 21.8 deg (mu=0.4) = self-locking, needs h>=6.08 mm to be proud; w=3.0 -> 23.0 deg / h>=4.84; w=5.0 -> 33.6 deg / h>=3.52. AGITATOR: 3 fingers at theta 0/120/240, r10..46.4, z -281.64..-277.65 = 0.56..4.55 above the sump floor and 8.06..12.05 above the disc; hex-driven 1:1 off the disc hub -> zero relative motion over the pockets; unswept outer ring r46.5..47.66 = 343 mm2 (claim 147). SUMP FLOOR: 4374 of 6494 mm2 (67%) is 0-deg dead shelf. TORQUE: 0.18 N*m / 0.032 m = 5.625 N at PCD (claim 6.0); agitator drag est. 0.04-0.08 N*m, M5 detent release est. 0.2-1.1 N*m vs 0.18 N*m available. EXIT KINEMATICS: index v 167.6 mm/s at PCD; pellet centre inside the r10.5 rim for 18.89 deg = 63 ms of a 150 ms index vs 50-53 ms of free fall to clear the pocket (1.18x); park lens 5.51 mm (claim 4.01); park retention margins vs the r10.5 rim +0.99 (D13) / +0.49 (D12) / -0.014 mm (D11). PLATE/FINES: fines slots r19.5-23.5 and r40.5-43.6 clear the r24.5-39.5 pocket footprint by 1.0 mm each side; the r23-41 exit port spans the pocket band so dust under a seated pellet sheds once per revolution; rim slots r45.7-46.8 over 307 deg. Builder's own verify_exports.py re-run clean (11/11 STEPs 1 solid, 17/17 assembly bodies watertight, cartridge drop-out 0.00 mm3, 23-station Dia13 transit 0.000 mm3) — all confirmed, but none of those probes test the entry-relief geometry.

### critic: buildability

- score: 8.5
- pass: true

#### issues

- MODERATE (COTS): the only bearing, igus 'JFM-2022-04' (ID20/OD22/L4), could not be confirmed as a catalogued length by web search (JFM series format confirmed via JFM-1820-22, but no JFM-2022 hit); BOM flags it PN ASSUMPTION with fallbacks (machine longer bushing down, or deepen roof 2 mm) - must be resolved before ordering (open issue 8, cad/BOM.md)
- MINOR (printability/structure): top_plate has 2.9% of surface under 1.95 mm, located by critic probe at the hex-nut boss webs (0.82-1.61 mm at r10-20, a disclosed 0.9 mm web in a compression stack) and outer-rim latch detail (1.12-1.84 mm at r70-80); acceptable but the rim detail is undocumented in BUILD-NOTES
- MINOR (service/gloves): fill_cap bayonet lugs and skirt are ~1.28 mm thick and glove-handled every refill; chip/wear risk, cap is non-structural (O-ring retained, lanyard added)
- MINOR (process): cad/BOM.md omits generic fastener lines (4x M3+nyloc clip screws, 6x M3 flange screws, 2x M3 sensor grub screws) - quantities/lengths not orderable from the BOM as written
- NIT: stale stack comments in cad/dispenser.py (e.g. line 262 'Z_DISC_TOP ... -286.0' vs actual -289.7 in exports); verify_exports.py's hand-typed coordinates are correct, comments are not
- CARRIED (disclosed bench items, not CAD-closable): agitator gravity-only retention re-seat behaviour, 3x M3 plastite pull-out in printed pilots carrying the ~500 g cartridge, retaining-plate outer edge ring is a 1.1 mm land (critical web 2.1 mm passes)
- NOTED HONEST LIMIT: on-aircraft refill is impossible (62 mm lateral cap travel in a 10.5 mm gap) - procedure is quick-release + tailgate refill, acceptable since CONTEXT does not require on-aircraft refill

#### numbers

Builder's export-only checker rerun by critic: cartridge drop-out sweep 0.00 mm3 (r4: 860.07), jam-access rods Dia8/Dia12 to wiper plane and roof edge 0.00 mm3, wiper slide-out 0.00 mm3, Dia13 transit 0.000 mm3 at all 11 stations, plate webs 2.1 mm (r4: 1.0), funnel 68.0 deg, journal band 97.5/97.5 mm3 unbroken, hex engagement/socket verified, capacity 1073 cm3 analytic (claim 1082), printed mass 519.4 g. Critic's OWN independent trimesh measurements: 11/11 STLs watertight, assembly 17/17 bodies; ray-cast wall p1: hopper 2.16, meter_housing 2.38, pocket_disc 4.88, retaining_plate/e-bay/lid 1.98 (=2.0 nominal), top_plate 1.45 (2.9% <1.95 mm, localized to disclosed nut-boss webs + rim latch), brush_holder 0.99 (disclosed, stress-checked 7.6 MPa at 6 N stall); overhang at claimed best orientations 0.0-8.7% (matches builder's 0.0-8.9% per part); cap top z=-178.40 giving 7.40 mm headroom vs 6.45 mm lift; ground clearance 189.69 mm (gear tubes Z~-528 + Dia40 foam consistent). COTS: 14HS13-0804S verified real, 35x35x34 mm, ~170 g net vs 190 g carried; JFM-2022-04 length NOT confirmed catalogued (flagged in BOM). Mass: 890.1 g empty, 1274.1 g loaded @250 vs 1500 g ceiling.

### critic: mass-budget

- score: 9
- pass: true

#### issues

- MINOR: 149.3 g (16.8% of empty) is estimate lines (electronics 65 g, fasteners 57 g, seals/magnets 8 g, PCB 15 g, bushing/washer/bristles 4.3 g) not measured from geometry, and exceeds the nominal 10% contingency that carries it; margin (217-414 g) bounds a plausible 2x error, and builder discloses this honestly (open issue 11), but it stays open until a bench weigh-in.
- MINOR: MAX-fill rib labeled 393 pellets but recomputing the pessimistic ledger from measured volumes gives 391-392, and the builder's own export re-measure prints 391 - a 2-pellet (~2.4 g) label wobble; rib label should carry the export number.
- MINOR: stepper mass is a vendor 170/190 g conflict (190 carried, 200 g sensitivity passes) and clip plate material is an alu ASSUMPTION (steel sensitivity +59 g still passes at 1339 g) - both labeled, neither ceiling-critical.
- NOTE: strict no-exemption @393 on the pessimistic ledger is 1480 g with only a 20 g reserve - deliberate and legal (pellets >250 are exempt per CONTEXT), but the rib line is knife-edge if the exemption were ever revoked.

#### numbers

Independently measured from r5 exports (venv trimesh/scipy, never importing the model): 11/11 printed STLs watertight, printed volume 415.6 cm3 -> 527.5 g solid @ PETG 1.27 g/cm3, 348.9 g at realistic infill (4x0.4 mm walls via 3D voxel erosion + 25% infill); clip plate 11.52 cm3 -> 31.1 g alu (measured from 2112 STEP); stepper 190 g vendor; estimates 149.3 g. EMPTY = 719.3 g realistic / 897.9 g solid-basis; +10% contingency = 791.2 / 987.7 g; + 250 pellets = 295.0 g. TOTAL LOADED @250 = 1086.2 g realistic infill / 1282.7 g conservative 100%-infill vs 1500 g ceiling (margin 414 / 217 g). Over-1.0 kg fully attributed: stepper 190.0 + capacity oversizing 61.1 + latch/lugs 16.5 + fastening/electronics 15.1 covers the 282.7 g solid-basis overage (realistic-basis overage 86.2 g < the stepper alone). Full-load: @393 = 1254.9/1451.4 g, brim @474 = 1350.5/1547.0 g (pellets >250 exempt per CONTEXT). Assembly STL 17 bodies 17 watertight, bbox Z -358.2..-171.0. Builder ledger reproduces from components (889.9 vs claimed 890.1 g at their 1.25 CF-PETG density).
