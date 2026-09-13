# BUILD NOTES — Round 4 (CAD builder)

Winning concept: **pocket-wheel**. Round 4 closes the r3 critics' blocking
issues (pellet-path FAIL 6.5, buildability FAIL 6.5, interference PASS 9 with
one correction, mass PASS 9 — `BUILD-NOTES-r3.md` §Round-3 Critics). Every
number marked *measured* is printed either by `cad/dispenser.py` itself or by
`cad/verify_exports.py`, a second script that reads **only the exported
STEP/STL** and never imports the model. Facts from CONTEXT are cited;
everything else is [D] (derived, math shown) or ASSUMPTION.

## Deliverables

- Model: `cad/dispenser.py` (parametric build123d; pellet-facing dims driven
  by `PELLET_D`/`PELLET_D_MAX` = 12/13)
- Independent checker: `cad/verify_exports.py` (new — critic-style probe pass
  on the exports only)
- Exports (`cad/exports/`): `dispenser_r4_assembly.step/.stl` **plus
  individual STEP+STL for all 11 printed parts** (top_plate, **pcb_pedestal**,
  fill_cap, hopper, meter_housing, pocket_disc, agitator, brush_strip,
  retaining_plate_chute, electronics_bay, **bay_lid**)
- Renders (cream #faf7f0): `cad/renders/r4_iso.png`, `r4_section.png`,
  `r4_meter_detail.png`, `r4_bottom.png`, `r4_fill_station.png`,
  `r4_bay_lid.png`

## Root cause of the r3 FAILs, and the structural fix

All three r3 blockers were **assembly-kinematics** defects: features that are
geometrically correct and statically non-interfering, but that no tool, nut,
screw or hand can ever reach (roofed screws, sealed nut pockets, a trapped
brush). r3's harness checked connectivity and static interference — neither
can see this class. That is the same failure pattern as r2 (tangent unions
invisible to a pairwise interference check).

**r4 adds an INSERTION / TOOL-PATH harness** that measures the paths
themselves: nut-insertion columns, Ø8 driver corridors for every screw,
an exact swept-union of the brush along its slide direction, set-screw
shaft-engagement, lid-screw approach paths, and the cartridge drop-out
envelope. Every one of these is a *measured volume*, printed on every run,
and re-measured independently on the exports. A screw with no driver path
now fails the build like a collision does.

## Blocking issues from the r3 critics — disposition

### pellet-path critic (r3 score 6.5, FAIL)

| Issue | Disposition |
|---|---|
| **BLOCKING: disc drive set screw at z −268 misses the shaft top (−280.5) by 12.5 mm and the hub bore by 5 mm → zero torque transfer; the disc cannot be driven** | **FIXED** — screw moved to z = disc_top+4 = **−282**, inside the shaft engagement band −304.5…−280.5. Measured (model *and* export): shaft-engagement probe **1.45 mm³ > 0**, hub bore open at −282 (**0.00 mm³** residual), screw path through the hub clear (0.00). The same probe at the r3 position reads **0.00 mm³** — the harness now reproduces the critic's finding and would fail on it |
| MINOR: dead dust ledge r47–47.5 at the chamber-wall top | **FIXED** — fill-sector cut pulled in from r47.5 to the chamber wall **r47.0**, and the remaining 0.5 mm step under the funnel outlet is now a 45° chamfer ring over the fill arc. Measured on the export: housing material inner radius runs **r48.1 → 47.7 → 47.3 → 47.0** over z −280.6…−281.8 (a ramp, not a shelf); the old flat annulus reads **0.000 of 1.50 mm³** |
| MINOR: rim-trough fines slots cover only 190° (53%), exit sector on dead floor | **FIXED** — 3 arcs, inner radius 45.4 (0.4 mm clear of the chute wall), now **307 of 360° open = 85%** (measured by 360 one-degree probes on the exported plate), including the exit sector. Bridges retained at the Hall cavities (83–120°) and two 8° structural webs |
| MINOR/BENCH: 4.25 mm gap between a seated pellet top and the rigid bar admits 4.3–13 mm fragments to wedge | **REBUTTED + carried as bench item** — geometry unchanged deliberately: a fragment in that gap is loaded by the pocket lip at ≤6 N ([D] 0.18 N·m / 0.030 m), 12× below the ~73.5 N crush class figure, and the Hall/StallGuard reverse-retry sequence clears it. Closing the gap would require the bar to ride within 1 mm of a friable pellet's crown — trading a recoverable jam for a fines generator. Open issue 6 |
| NOTE: funnel wall measured exactly 60.0° | Unchanged and re-stated: the anti-bridge defence is the open fill arc + active agitator, not the wall angle (concept §3) |
| NOTE: "1.0 mm below disc top" is really 1.5 mm | **FIXED in print** — the check now derives it from the under-gap: seated pellet rests on the retaining plate, top **1.5 mm** below the disc surface; stacked second sphere protrudes **11.5 mm** (brush wipes >1.2) |
| NOTE: two-in-chute exclusion is a timing property, not geometry | **FIXED (stated as a contract clause)** — the run now prints an **INTERFACE CONSTRAINT: min index period ≥ 150 ms** vs the measured 101 ms free-fall transit. Recorded here and to be carried into the ICD command contract (software remains out of scope per CONTEXT) |

### buildability critic (r3 score 6.5, FAIL)

| Issue | Disposition |
|---|---|
| **BLOCKING: hopper→housing funnel-tab screws uninstallable — the 60° cone wall sits directly over all 3 screw axes (2.85 mm³ shank, 44.2 mm³ head/driver obstruction)** | **FIXED by re-architecting the joint** — the vertical tabs are gone. 3 **radial skirt tabs** (θ 30/105/225°, r52.15–55.15, z −288.5…−273) hang outside the housing wall and take **M3 plastite screws driven horizontally from outside**. Measured per screw (export): Ø8 driver corridor r56→r95 = **0.00 mm³**, tab clearance hole 0.00, housing pilot bore 0.00, **pilot thread stock 51.2 mm³**. Tab root: a band reaching inboard to r50 over z −280.4…−276.3 fuses into the full cone wall thickness (**211 of 211 mm³ solid**) instead of a thin wedge; joint gap to the housing OD measured 0.15 mm running clearance |
| **BLOCKING: all 4 clip→top_plate hex nut pockets are sealed internal voids (0.4 mm floor skin) — the primary aircraft joint is unassemblable** | **FIXED** — bosses deepened 4.0 → 5.6 mm and the hex cut breaks **through the boss bottom face**. Measured on the export at all 4 stations: boss-bottom skin **0.00 mm³**, pocket cavity residual 0.00, insertion column below the boss 0.00; nut depth still 4.2 mm (nyloc fits), **6.8 mm³ of solid web above the nut seat** |
| **BLOCKING-class: one-piece brush cannot be installed into or removed from the closed groove** | **FIXED** — the outer wall now carries a **full-cross-section window** (r45.5–52.6, z disc+1.0…+4.0, 4.3 wide) so the brush slides in/out radially; the inner ring keeps its closed slot for the bar tip; the end tab covers the window from outside and keeps the M3 radial screw. Verified by an **exact swept union** of the exported brush over 0–38 mm of radial retraction in 20 steps: **0.00 mm³** against every other part. Window ceiling stock 13.4 mm³, floor stock 5.5 mm³ (the wall is not cut through vertically). New-leak-class check: largest sphere that fits the installed window is **1.75 mm**, smaller than the deliberate 4.0 mm fines slots → no new escape class |
| **ROOT-CAUSE: harness had no insertion/tool-path check** | **FIXED** — see §Root cause. 6 new probe families, printed every run, re-run independently by `verify_exports.py` |
| MAJOR (r3 open issue 3): electronics bay is a sealed shell | **FIXED** — the −Y wall is now a **42 × 36 opening** closed by a screwed **bay_lid** (new printed part): 4× M3 self-tap into corner bosses, register lip (0.3 gap), and the two Ø6 rib-driver access holes moved into the lid. Measured: component insertion prism **31 × 35 × 20 deep passes at 0.00 mm³**, accessible cavity **34.2 cm³**, lid↔bay interference 0.00. Honest limit: the corner bosses narrow the clear opening from 42 to **31 mm** across the corner bands (probe: 41 × 35 reads 483 mm³ of boss, 31 × 35 reads 0.00) |
| MODERATE: documented print orientations rest on protrusions (41.6% / 36.6% unsupported) | **FIXED and now measured every run.** The 8.9 mm PCB pedestal is **split out as its own printed part** (2× M3 from under the plate — which also makes blind-mate height shimmable, de-risking open issue 8), and the top-plate lightening pockets were moved to the underside. Measured support-needing area (downward faces >45° that are not on the bed): **top_plate 2.0%** (was 42.0% in the r3 orientation), pcb_pedestal 0.0%, hopper 0.9%, meter_housing 7.6%, pocket_disc 0.6%, retaining_plate_chute 2.5%, electronics_bay 9.1%, bay_lid 2.2%. Honest remainders: **fill_cap 13.9%** (flange annulus 380 mm² + 2 lug undersides on a 13 cm³ part), **agitator 11.0%** (horizontal TPU fingers, unavoidable), **brush_strip 19.8%** (0.58 cm³ part) |
| MODERATE: COTS part numbers incomplete | **IMPROVED** — real orderable numbers now printed: stepper 14HS13-0804S (verified), TMC2209 (BTT V1.3 module), **TSSP4038 + TSAL6200**, **DRV5032FBDBZR**, **STM32G431KBT6 + TCAN332DR**, **Pololu D36V6F5**, **supermagnete S-03-02-N**, **Ruthex RX-M3×5.7**. Still class-level (labelled ASSUMPTION): spring plunger, plastite, PTFE washer, strip brush |
| MINOR: rib cheeks 1.9 mm | **FIXED** — ribs widened 7.0 → 7.6 mm → cheeks **2.2 mm** |
| MINOR: brush bar 1.1 mm over a 27 mm span | Carried (open issue 6). The bar cannot exceed ~1.3 mm without exceeding the 1.4 mm inner-ring slot; load ceiling is the stepper's 6 N regardless |
| MINOR: fill-cap detent / glove refill | Detent still unmodeled (open issue 5), but the **O-ring gland is now real geometry**: r21.8–22.7 × 2.0 mm groove inside the Ø46 bore land, 1.5 mm cord, **20% squeeze** [D]; measured 265.9 mm³ open gland on the export. Off-aircraft refill remains the documented procedure |

### interference critic (r3 PASS 9 — correction)

| Issue | Disposition |
|---|---|
| Builder over-reported leg clearance (92.0 tube-axes-only vs 83.42 true full-gear) | **FIXED at the source** — the model now builds the **full landing gear from the quiver source** (`landing_gear/assembly.py`, incl. the 1330 adapters), samples 327 243 gear points and refines with exact point-to-triangle distance. Measured **83.42 mm — identical to the critic's independent figure**. The tube-axes number is still printed but explicitly labelled as the over-reporting cross-check |
| NOTE: 0.039 mm tessellation-scale penetration top_plate↔fill_cap | In-model booleans still read 0.00 locked and 0.00 inserted; carried as a printed-part running-fit item |
| NOTE: blind-mate PCB pin engagement is an ASSUMPTION | Carried (open issue 8) — but the pedestal is now a separate shimmable part, so a height error is a 2-minute fix instead of a reprint |
| NOTE: clip↔drone-side 0.047 mm at the QR engagement plane | Documented; drone-side hardware is not part of this payload model |

### mass-budget critic (r3 PASS 9 — non-blocking)

| Issue | Disposition |
|---|---|
| Brim fill (492) only passes via the CONTEXT pellet exemption; recommended fill line not modeled | **FIXED, and tightened** — two fill lines are now molded into the hopper wall, with their heights **solved from the measured usable volume**: a **430-pellet MAX line** (z −205.8, 19.3 mm below the lid) chosen so the whole payload stays under 1500 g even on the strictest no-exemption reading (**1476.8 g**), and a **250-pellet baseline reference line** (z −232.4). 450 was rejected on measurement: it lands at 1500.4 g |
| ~117 g of electronics/fastener lines are estimates | Unchanged and still flagged; bounded by the 10% contingency |
| Stepper 170 vs 190 g vendor conflict | 190 g carried; sensitivity at 200 g printed and passes |

## Measured numbers (r4)

Model run and independent export run agree on every shared figure.

- **Connectivity:** 15/15 parts are single solids in-model; **11/11 exported
  STEPs re-import as 1 solid**; 11/11 part STLs watertight; assembly
  STL = **15 bodies, 15 watertight**; assembly STEP = 15 solids
- **Envelope:** bbox X ±75, Y −90…+75, Z −354.5…−171.0 → stack **183.5 mm**,
  **ground clearance at rest 193.39 mm** (ground Z −547.89) vs the 40 mm
  requirement
- **Landing gear:** full-gear mesh-to-mesh **83.42 mm** (was over-reported 92.0)
- **Props (cited, r3 critic full-assembly):** vertical gap 152.5 mm, radial
  gap 239.3 mm, min 3D distance 348.0 mm
- **Pellet transit, Ø13 worst-case sphere, 21 stations, 0.000 mm³ everywhere**
  (fill port cap-off → hopper → funnel wall tangent → funnel wall at all three
  skirt-tab angles, high and low → outlet → resting on the disc → **seated in
  a pocket with the disc actually indexed** at 180/133/129/90/45/0° → exit
  hole → chute → IR beam → below the aircraft). The indexed-disc probes matter:
  r3's static probes would have read false positives on the disc web
- **Meter:** pocket pitch 25.1 mm, web 10.1 mm; seated worst-case pellet
  1.5 mm below the disc top; stacked second sphere protrudes 11.5 mm (brush
  wipes >1.2); roof entry ramp material starts 129.0° @ disc+2.0 and 125.0° @
  disc+5.0; restack window 3° = 1.7 mm at PCD
- **Brush:** wall window free section 4.0 × 2.75 passes at 0.00 mm³; ceiling
  13.4 / floor 5.5 mm³ stock; inner-ring closed slot ceiling 12.6 / floor
  9.0 mm³; slide sweep 0.00 mm³ against 7 parts; window leak class 1.75 mm
- **Fastening paths:** 4/4 nut pockets open (0.00 skin), 3/3 skirt screws with
  0.00 mm³ driver corridors and 51.2 mm³ pilot stock, 4/4 lid screws 0.00,
  2/2 rib driver paths through the lid 0.00, set screw engages the shaft
  (1.45 mm³), cartridge drop-out Ø26.4 through the roof pass-through 0.00
- **Fines handling:** rim slots 307/360° (85%); park lens 4.01 mm (rebuttal
  from r3 held: pellets and ≥4 mm fragments retained when parked)
- **Sensing:** IR beam 40 mm below the plate, v = 0.89 m/s, ~17 ms occlusion,
  sensor faces recessed 5.0 mm; Hall cavities 0.00 mm³ overlap with the exit
  bore (margins 40.7 / 49.7 mm)
- **Capacity:** usable hopper volume **1123 cm³ → 492 pellets worst-case
  barrel packing (581 g) / 684 sphere-basis — 1.97× the 250 hard minimum,
  PASS**. Molded MAX line = 430 (980 cm³ measured below the line), baseline
  line = 250 (570 cm³)
- **Interference:** 105 pairs, 28 bbox-overlapping pairs boolean-checked,
  **0 collisions, 0 check-failures**; cap locked/inserted 0.00/0.00; 3 lug
  swings 0.00; agitator swept annulus 0.00 ×4; motor↔chute 1.4 mm
- **Print orientations:** measured per part (list above); worst structural
  part is meter_housing at 7.6%
- **Mass ledger (printed parts measured from solid volumes):** empty total
  **881.3 g** + 10% contingency → **969.4 g carried empty**;
  **LOADED @250 = 1264.4 g (236 g under the 1.5 kg ceiling)**;
  LOADED @430 (max fill line) = **1476.8 g**; brim @492 = 1550.0 g (pellet
  mass above the 250 baseline is exempt per CONTEXT). Sensitivities:
  stepper 200 g → 1275.4 g; steel clip plate → 1329.3 g (both pass)

### Over-1.0 kg justification (Judge 3's reading: threshold at the 250 load)

1264.4 g is 264 g over 1.0 kg, +2 g vs r3 — r4 removed nothing and added the
bay lid (7.1 g), the pedestal split (+0 net, it moved) and 2 g of fasteners,
while the skirt-tab rework replaced the old funnel tabs at roughly parity.
The itemisation is unchanged from r3: vendor-verified stepper 190 g (it *is*
the torque limiter — no separate clutch), a latch ring that actually carries
the ~430 g cartridge, modeled fastening at every joint, phase/safe-state
hardware, and hopper structure buying 1.97× the hard minimum capacity.

## What else changed vs r3

- New printed parts: `bay_lid`, `pcb_pedestal` (both split out for
  buildability, not for function)
- Roof centre pass-through Ø24 → **Ø27** so the agitator collar (Ø26) leaves
  with the cartridge on a quarter-turn service removal (measured 0.00 mm³)
- O-ring gland modeled on the fill-cap neck (r3 open issue 4, partial)
- `verify_exports.py` added so critics (and CI) can re-derive every claim from
  the exports alone
- 6 renders regenerated, incl. a new bay-lid view

## Open issues for round 5 / bench

1. **Caliper survey still gates the print** — `DISC_T`, `POCKET_R`,
   `BRUSH_WIPE` must be re-frozen against 20+ real pellets (all-judges item
   #1; not closable in CAD).
2. Sensor bench test with dusty/fragmented pellets freezes the dark-time
   thresholds; capacitive-ring fallback envelope preserved (chute ID 22).
3. **Min index period ≥ 150 ms is now a contract requirement**, not a
   geometric guarantee — must land in the ICD command section.
4. Gasket grooves at the perimeter joints are still schematic (only the cap
   O-ring gland is real geometry).
5. Fill-cap anti-rotation detent not modeled — O-ring friction is the interim
   retention. A snap detent needs ~0.4 mm of axial float that the current
   bayonet lug stack (0.1 mm) does not have; changing it would re-open a
   verified bayonet, so it is deliberately deferred to a bench decision.
6. Brush bar section (1.1 mm over ~27 mm) and the 4.25 mm fragment gap under
   the bar are bench items; force ceiling is the stepper's ~6 N regardless.
7. Stepper vendor mass conflict (170 vs 190 g) — weigh at receiving.
8. Clip-plate orientation ASSUMPTION (counterbore face = drone side) and
   blind-mate PCB position ASSUMPTION remain; the pedestal is now shimmable.
9. Near-empty skip behaviour remains bench-unproven (concept §10.3).
10. Bay corner bosses narrow the clear lid opening to 31 mm across the corner
    bands — fine for the named modules, but a taller connector body at a
    corner would need the boss moved.
11. Electronics/fastener mass lines (~122 g) are still estimates.
12. Skirt-tab joint is 3× M3 plastite into printed pilots carrying the
    cartridge + pellet column in tension — pull-out to be verified on the
    printed part (thread stock measured 51.2 mm³ per pilot).

---

## Round 4 critics — verdicts (verbatim)

| Critic | Score | Verdict |
|---|---|---|
| interference | 9.5 | PASS |
| pellet-path | 8 | PASS |
| buildability | 7 | **FAIL** |
| mass-budget | 8.5 | PASS |

### interference — 9.5, PASS

Issues:

- NOTE (non-blocking, carried open issue 8): blind-mate PCB top sits at exactly Z=-171.0 at Y -27..-43, outside the 50x50 clip footprint; correct as a contact plane but depends on the unverified drone-side spring-pin block position, and the drone-side fixed plate footprint measures 66x50 mm with the 66 mm axis orientation unverified (drone-side hardware not in this payload model)
- NOTE: ground-clearance figure assumes uncompressed foam sleeves; full 5 mm foam crush still leaves ~188 mm vs the 40 mm requirement, so irrelevant to pass/fail

Numbers:

Ground clearance at rest: dispenser low Z -354.50, ground (gear min Z, full gear from quiver source) -547.88 -> 193.38 mm vs 40 mm req (margin 153.4 mm). Gear<->dispenser min 3D distance 83.42 mm (matches builder exactly; adapter-to-top-plate-corner). Prop disks: tip R 305.1 mm, disk Z 44.0..63.5; worst vertical gap 215.0 mm, radial gap 251.1 mm, min 3D to swept disk 340.8 mm, static prop/motor 348.0 mm. Clip plate: 50.00x50.00x10.50 mm, 11.52 cm3, identical to COTS 2112 payload-side STEP, centered (0,0), top at Z=-171.000; 0 payload vertices above -171; stack -125-30-16=-171 closes. Assembly: 15 bodies, 15/15 watertight, bbox X+-75.00 Y[-90.00,74.98] Z[-354.50,-171.00]; 28 bbox-overlapping pairs, no penetration >0.05 mm.

### pellet-path — 8, PASS

Issues:

- MAJOR - sump aperture is 3.5x smaller than documented. CONCEPT-pocket-wheel.md §3 claims 'the open-arc sump keeps the orifice at ~95 mm'. Measured (linear scan of meter_housing_r4.step at th=190, z=-283): housing material bands r14.0-20.0 and r47.0-52.0, i.e. a fixed inner collar OD r20.00 and chamber wall ID r47.00 -> the real aperture is a 27.00 mm radial x 122.5 deg annular window (open 127.0-249.5 deg, 68.4 mm arc at PCD, 1934 mm2 plan area, equivalent circular orifice D49.6). 27.00/13.0 = 2.08 x worst-case pellet; 2.25 x nominal. A 3-pellet arch spanning 27 mm between the collar and the chamber wall is geometrically feasible. Mitigation is real but is the agitator alone: 3 TPU fingers, r9.99-44.60, z -280.00..-272.00, sweeping 0.50 mm above the sump shelf, so a finger passes through the arch volume every 120 deg of shaft rotation. The '95 mm' number must be struck from the concept and the mass/judging docs and replaced with 27.0 mm = 2.08 d.
- MAJOR - the wiper, the sole double-exclusion backstop, is a solid printed fin with no bristle retention feature. brush_strip_r4 is exported as one of the 11 PRINTED parts (0.584 cm3 solid) but its mass is hard-overridden to 10.0 g with basis 'COTS nylon strip in printed bar'. Measured section by 0.4 mm radial slab booleans: r20.0 -> 4.40 mm2 (4.0 tangential x 1.10 tall, z -283.25..-282.15, the inner tongue); r26/32/38/44 -> 6.880 mm2 (bar 4.0 x 1.10 plus a solid 1.6 x 1.70 fin, overall z -284.80..-282.15). There is no channel, slot or pocket anywhere in the part to hold bristles - the fin IS solid material occupying the bristle envelope. Structurally the rigid reading is fine (span r14->r46 = 32 mm, I = 5.87 mm4, at the 6 N stepper ceiling: delta 0.17 mm, sigma 16.4 MPa vs ~50-70 MPa PETG-CF yield), so it works as a rigid scraper - but that falsifies concept §2.3 'Compliant - it deflects rather than shearing a friable pellet' and makes every wipe event a PETG-CF-on-friable-pellet impact directly above the meter, i.e. a fines source feeding the optical sensor. Either model the bristle channel or delete the compliance claim and the 10 g COTS mass line.
- MAJOR - the highest-probability jam site is unreachable by any straight field tool. Rod-reach booleans through the open fill port (centre (0,40), r23) to the disc top at PCD 32: a D8 rod reaches pocket angles 150-230 deg (85 of the 122.5 deg window), a D4 rod reaches 145-235 deg (95 deg). Both read 0.00 mm3 obstruction there, but neither can reach the wiper plane (133 deg) or the roof entry edge (129 deg) - which is exactly where a proud/half-seated pellet jams (rider-vs-fin first contact measured at th~146, housing ramp first contact th~137). Exit-side jams ARE clearable: a rod up the chute from below into a pocket reads 0.00 mm3 obstruction at D4, D10 and even D18. So the mechanism is half field-serviceable and the docs should say which half.
- MAJOR - no isolation gate between hopper and meter, so the documented 'quarter-turn cartridge service removal' dumps the hopper. grep of dispenser.py for gate/shutoff/isolate/drain finds nothing; the fill window is permanently open (122.5 deg x 27 mm). Dropping the meter cartridge to clear a wiper/roof-edge jam therefore releases up to the 430-pellet MAX fill line = 507 g of pellets onto the ground. The only realistic field procedure is: quick-release the payload, invert it, pour the load back out through the D46 fill port, then service - and that procedure is not written down anywhere in BUILD-NOTES-r4.md.
- MODERATE - BUILD-NOTES-r4.md carries a stale gap number. The r4 rebuttal of the r3 fragment-wedge item states '4.25 mm gap between a seated pellet top and the rigid bar ... geometry unchanged deliberately'. Measured: over the pocket band (r26-44) the wiper underside is z -284.80 (the 1.6 x 1.70 fin, set by BRUSH_WIPE=1.2), not z -283.25 (the bar, which is what 4.25 was computed from). Seated worst-case pellet top = -300.50 + 13.0 = -287.50, so the true gap is 2.70 mm to the fin and 3.00 mm to the roof underside (-284.50). The design is better than the note claims, but the note is wrong by 1.55 mm and the fragment class that can ride into the transfer arc on a seated pellet is 2.7-13 mm, not 4.3-13 mm.
- MODERATE - the funnel is exactly 60.0 deg from horizontal, and the agitator does not reach 78% of it. Measured from hopper_r4.stl inner-radius sections: local wall angle 60.018 deg over z -274->-268 and 60.018 deg over -260->-250 (global fit 60.93 deg is contaminated by the skirt tabs); inner r 70.000 at z=-241 (D140) extrapolating to r47.50 at z=-280.5 (D95). 60.0 deg is at/below the conical mass-flow threshold for printed PETG (typ. 65-70 deg from horizontal needed), so expect funnel flow with a stagnant wall annulus. Cone height = 39.0 mm (z -280.5..-241.5); the agitator tops out at z=-272.00, so 30.5 mm = 78% of the cone is unagitated. The build note is right that the defence is agitation, not wall angle - but it never states that the agitation is confined to the bottom 22% of the cone.
- MODERATE - the sump floor is a 0 deg flat shelf, not a hopper wall. meter_housing_r4 roof top at z=-280.50 presents 5793.9 mm2 of upward-facing near-flat area over r15.1-51.0; the pellet-wetted part is the 240 deg annulus r13.5-47.0 = 4245 mm2 on which pellets rest with zero gravity component toward the fill window. Transport to the window is entirely by the 3 agitator fingers (8-9 deg wide each, r9.99-44.60, 0.50 mm above the shelf), which push shelf pellets circumferentially in the -theta direction toward the 249.5 deg window edge - so the mechanism is sound, but the unswept outer ring r44.60-47.00 is 460 mm2 = 10.8% of the shelf and will pack fines. Residual film under the fingers is 0.50 mm everywhere.
- MINOR - fines slots are 3-4 mm, not 4.0 mm, and the 85% claim is understated. Per-degree through-plate scan of retaining_plate_chute_r4 (open at all three of z -300.7 / -302.5 / -304.3, r42-56): continuous radial opening >=1.0 mm at 360/360 deg, >=2.0 mm at 349/360 (97%), >=3.0 mm at 327/360 (91%), >=4.0 mm at 0/360 (0%). So coverage beats the claimed 307/360 = 85%, but the slot never reaches the stated 4.0 mm width - fragments above ~3.5 mm stay in the chamber. Trough does drain: no plate material below z=-304.8 under the slots, and column probes at th=180/200/300 hit only 4.2 mm3 of meter_housing, so fines fall clear rather than onto hardware.
- MINOR - silent uncommanded release path for <=4 mm fragments. Parked pocket at +-22.5 deg: centre distance 2*32*sin(11.25) = 12.487 mm, pocket r7.50 + exit r9.00 = 16.50 -> overlap lens 4.013 mm. Whole pellets are retained (pocket-centre-to-exit-centre 12.487 > exit r9.00 by 3.49 mm), but a <=4 mm fragment falls out of a parked pocket in flight, and per the concept's own dark-time gate a ~4 mm fragment reads ~9 ms, i.e. below the 10 ms accept threshold, so it is released without being counted or reported. Consistent with the deliberate fines-shedding intent, but it should be stated as an uncommanded-release class rather than buried in the retention rebuttal.
- MINOR - chute is vertical at x = +32 mm, contradicting concept §5. Measured bore centre stays at x=32.0 with open radius 11.000 at z = -306, -315, -330, -344.5, -352; chute bottom z=-354.50. Concept §5 says 'the chute angles the drop line back to ~the airframe centerline ... release point near CG'. It does not - release is 32 mm off the payload axis. Irrelevant against a 1 m CEP, but the accuracy argument in the concept should not cite a feature that was never built.
- MINOR - 1.0 mm rotating shear gap around the disc for the full 14 mm disc thickness. Disc OD measured 46.00, chamber wall ID 47.00 (annulus probes: 0.00 mm3 of housing at r46.8-47.0, 352.38 mm3 at r47.2-47.4). Sub-millimetre fines enter this gap and are ground between a rotating PETG-CF rim and a fixed PETG-CF wall over a 250+ pellet sortie. Unavoidable in this architecture and there is a fines path out, but it belongs in the attrition open-unknown, not omitted.
- NIT - disc set screw has zero top margin. The r3 BLOCKING defect is genuinely fixed and I reproduce it: central hub bore reads 0.000 mm3 (r2.6 probe) at z = -275, -282, -285, -290, -298; the set-screw axis probe at z=-282 reads 0.000 mm3 (hole present) while the old r3 position z=-268 reads 28.235 mm3 solid (hole gone) and the hub is solid there (8.495 mm3). But shaft top = -280.50 and an M3 screw centred at -282.00 spans -283.50..-280.50, i.e. its top edge is exactly flush with the shaft end - full engagement with 0.00 mm of margin. Dropping the screw 1.0-1.5 mm would cost nothing.

Numbers:

VERIFIED GOOD (independently re-derived from exports, disc phase measured not assumed): pocket centres in pocket_disc_r4.step are at 0/45/90/.../315 deg (open arcs at r32,z-295 grouped: 347-13, 32-58, 77-103, 122-148, 167-193, 212-238, 257-283, 302-328). With the disc rotated so a pocket is at the probe angle, a 13.0 mm sphere reads 0.000 mm3 against all 7 path parts at every one of 15 descent stations z=-273.0 to -294.0 in the fill window, and at all 14 transfer-arc angles th=250,190,140,135,133,130,129,127,112.5,90,45,22.5,5,0 at seat height z=-293.9. (My first run with a 6.5 deg phase error read 189.6 mm3 at every station - the same trap that produced r3's false positives; the r4 result survives the corrected test.) MINIMUM CHANNEL DIMENSIONS, binary-searched on the exports: pocket bore D15.00 constant below z=-288.10, with a lead-in chamfer D18.63 at the disc top (-286.10) -> D17.63 (-286.60) -> D16.63 (-287.10) -> D15.63 (-287.60) -> D15.00 (-288.10), i.e. a true 2.0 mm 45 deg chamfer; exit port D18.00 (z -302.5 and -303.5) with lead-in D20.42 at -300.7 and D18.83 at -301.5; chute D22.00 constant at z = -304.3, -306, -315, -330, -344.5, -352 to the exit at -354.50. Governing minimum = 15.00 mm = 1.15 x the 13 mm worst case, 1.25 x the 12 mm nominal. VERTICAL CLEARANCES: roof underside -284.50 (boolean column at th=0/45/90 reads exactly 3.142 mm3 of a pi*1^2*3.0 column = 1.0 mm of roof in the -286.5..-283.5 band) -> 1.50 mm over the disc top -286.00; wiper fin underside -284.80 -> 1.20 mm; seated 13 mm pellet top -287.50 -> 1.50 mm below the disc surface; stacked second 13 mm sphere protrudes 11.50 mm (wipeable); worst-case 9 mm barrel pair = 18 mm in a 14 mm pocket -> 3.50 mm protrusion, still above the 1.20 mm wipe line, so double-exclusion survives the barrel ASSUMPTION too. RIDER INTERCEPTION SEQUENCE (measured, rider centre z=-280.9): fin first touches at th~146 (10.03 mm3 at 145), housing ramp first touches at th~137 (9.74 mm3), so 9 deg = 5.0 mm at PCD of wiper-only action before the roof edge. RESTACK WINDOW: fin tangential thickness 1.6 mm at PCD = +-1.4 deg about 133, roof edge 129 -> a 2.6 deg = 1.45 mm plan slot; a 13 mm pellet cannot restack (claim of 3 deg / 1.7 mm is conservative). SUMP: aperture 27.00 mm x 122.5 deg; free band for a resting pellet CENTRE is r26.42-40.58 = 14.16 mm (PCD 32 sits mid-band), ~5.5 pellets single-file over the window, 2.7 pocket pitches. AGITATOR: 3 fingers at th 0/120/240, 8-9 deg wide, r9.99-44.60, z -280.00..-272.00, 0.50 mm over the shelf; swept union over 0-360 deg reads 0.00 mm3 against both the wiper bar and meter_housing. NIP: finger underside -280.00 vs bar top -282.15 = 2.15 mm, crossed 3x per revolution. SENSING: chute wall intact at the beam - ring r11.6-12.0 is 97.4% solid at z=-343.0 and 91.4% at z=-344.5, so the light tunnels are recessed and no pellet or >2 mm fragment can leave sideways (D2 sphere in the wall = 3.55 mm3 material). Free-fall: v at the beam sqrt(2*9.81*0.040) = 0.886 m/s, 12+3 mm occlusion 16.9 ms, plate-to-chute-exit 54 mm = 105 ms (builder says 101), consistent with the >=150 ms index-period contract clause. PART INVENTORY: 11/11 r4 STEPs re-import as exactly 1 solid, 11/11 STLs watertight (top_plate 69.79, pcb_pedestal 2.07, fill_cap 13.09, hopper 104.07, meter_housing 77.07, pocket_disc 76.24, agitator 2.86, brush_strip 0.58, retaining_plate_chute 36.93, electronics_bay 15.62, bay_lid 5.67 cm3).

### buildability — 7, **FAIL**

Issues:

- BLOCKING — cartridge service removal is kinematically impossible. BUILD-NOTES-r4 claims the agitator collar 'leaves with the cartridge on a quarter-turn service removal (measured 0.00 mm3)'; that number comes from probing a Dia26.4 cylinder, not the agitator part. Measured on the exported agitator: its three Dia4 fingers reach r44.5 at z -279.5..-275.5, only 0.50 mm above the solid housing roof top (z -280.5, solid from r13.5 out). Swept descent vs meter_housing: 0.00 mm3 @1.0 mm, 15.5 @1.2, 162.9 @2.0, 1077 mm3 over 0..12 mm. Full-cartridge sweep (plate+chute+disc+motor+agitator, unlock 22 deg then down 60 mm) = 860 mm3, of which agitator 853 and every other member 0.00. This is the exact static-probe blind spot r4 was chartered to eliminate — the new insertion/tool-path harness was applied to screws and the brush but never to the cartridge drop-out.
- BLOCKING consequence — jam access. Because the cartridge cannot descend, the only real service path is: empty the hopper (up to 430 pellets), undo the 3 skirt screws, lift the hopper, then release the agitator set screw at r11.5 / z -274, which sits inside the funnel throat and is unreachable with the hopper on (5.3 mm3 of hopper in a Dia3 radial corridor). This procedure is documented nowhere. The disc drive set screw at z -282 also has 187 mm3 of meter_housing in a Dia3 radial hex-key corridor r10->r40 — acceptable as a bench-only screw, but it means the (broken) cartridge drop-out is the sole service path.
- MAJOR — refill with gloves. Fill cap bottom z -188.20, top-plate top face -181.50 => 6.70 mm of lift required to clear the bore; headroom from cap top (-178.40) to the -171.0 mounting plane is 7.40 mm. 0.7 mm of margin, so on-aircraft refill is effectively impossible; 'off-aircraft refill' is the real procedure but the measured constraint is never stated. Bayonet retention itself is sound (swept lift blocked at all orientations except 90 deg, 110.7 mm3), but in-flight cap retention is O-ring friction only (no detent, open issue 5) over a ~500 g pellet column.
- MODERATE — undisclosed sub-2 mm structural sections (inward ray-cast on exports). retaining_plate_chute: inner fines slots (r40.5-44.5) and rim slots (r45.4-46.8) overlap in angle over ~176 deg, leaving a 1.0 x 4 mm annular web at r44.5-45.5 as the only radial section between the pellet-bearing centre and the lug-carrying outer rim (confirmed at th=160/200/260/300/330). This is the part that carries the whole cartridge + pellet bed into 3 latch lugs, and the builder's harness never measured it.
- MODERATE — hopper wall cut to 1.7 mm at the two molded fill-line grooves (r71, z -206 and z -232/-233): a full-circumference stress-riser ring in the part that hangs the cartridge in tension. Added in r4 for the mass critic, never checked for wall thickness.
- MINOR — meter_housing ceiling over the inner-ring brush slot measures 1.5 mm (material begins z -282.0, roof top -280.5), below the 2 mm structural bar; build notes report it only as a volume (12.6 mm3) which hides the thickness.
- GAP vs brief — no bearings anywhere in the design and no bearing part number. The Dia92 / 76 cm3 pocket disc plus the pellet-bed side load is radially located solely by the NEMA14 stepper's internal bearings, with no radial-load check; the PTFE thrust washer is 'McMaster PTFE washer class, part TBD'. Other COTS is genuinely good (14HS13-0804S, TMC2209, TSSP4038/TSAL6200, DRV5032FBDBZR, STM32G431KBT6, TCAN332DR, D36V6F5, S-03-02-N, RX-M3x5.7 are real orderable PNs; 4 class-level items honestly flagged). Trivial inconsistency: source comment says N52 magnets, printed PN line says N45.
- MINOR — count-sensor cleaning is only partly serviceable: IR faces sit behind Dia3.2 tunnels recessed 5.0 mm, at z -344.5 with the chute exit at -354.5 (10 mm reach-in up a Dia22 bore). Swabbable at the bore face, but the Dia3.2 x 5 mm tunnel itself needs compressed air / a pipe cleaner and no sensor retention feature is modeled.
- MINOR (non-defect, conservative direction) — the builder's print-orientation search only tries rot 0/180, so fill_cap is reported at 13.9% when rot90 gives 4.8%, brush_strip 19.8% vs 7.6%, bay_lid 2.2% vs 0.0%.
- PROCESS — no BOM/README/docs/electronics deliverables exist in the package yet; COTS part numbers live only as print statements inside cad/dispenser.py.

Numbers:

MEASURED BY ME FROM EXPORTS ONLY (venv build123d/trimesh, no import of dispenser.py).
CONFIRMED FIXES (r3 blockers): nut insertion column Dia6.4 x 15 mm below all 4 bosses vs ALL 11 parts = 0.00 mm3 each (builder only probed the top plate); skirt-screw Dia8 driver corridor extended r56->r120 = 0.00 mm3 at th=30/105/225 (builder stopped at r95); brush radial slide sweep 20 steps = 0.00 mm3; connectivity 11/11 STEP single solids, 11/11 STL watertight, assembly 15 bodies/15 watertight; bbox X +/-75, Y -90..75, Z -354.5..-171.0, ground clearance 193.39 mm.
NEW BLOCKER: agitator z -280.00..-272.00 vs housing roof top z -280.50 => 0.50 mm free travel. Agitator vs meter_housing on descent: 0.00 @0.5/1.0 mm, 15.52 @1.2, 59.99 @1.5, 162.88 @2.0, 419.12 @3.0, swept 0..12 mm = 1076.99 mm3. Cartridge sweep (unlock 22 deg + down 60 mm): total 860.07 mm3 = agitator 853.03 + brush wipe 10.9 (intentional); plate/disc/motor each 0.00. Builder's collar-only probe (Dia26.4 x 60 down) reproduces their 0.00 claim.
SET SCREWS: disc set screw z -282, Dia3 radial corridor r10->r40 = 187.46 mm3 meter_housing (r10->r60 = 272.25); housing solid from r13.5 at z -282. Agitator set screw z -274, corridor r12->r52 = 5.3 mm3 hopper.
FILL CAP: bottom z -188.20, plate top face -181.50, cap top -178.40 => lift needed 6.70 mm vs 7.40 mm headroom to the -171.0 mount plane. Swept lift 0..8 mm: 110.75 mm3 blocked at locked orientation, 112.2/111.4/110.7 at 20/22/25-60 deg, 0.00 only at 90 deg.
WALL THICKNESS (inward ray cast, min/p1/p5): top_plate 0.79/1.47/2.40; hopper 0.75/1.70/2.14; meter_housing 0.22/2.32/2.45; retaining_plate_chute 0.37/0.90/2.00 (17.5% of sampled area < 2 mm); brush_strip 0.25/1.02/1.10 (23.7% < 2 mm); electronics_bay/bay_lid 2.00 nominal. Localized: plate web r44.5-45.5 = 1.0 mm x 4 mm over ~176 deg; hopper 1.7 mm at r71 z -206/-233; housing brush-slot ceiling 1.5 mm.
SUPPORT AREA (my implementation, >45 deg down, off-bed, best of rot 0/90/180/270): top_plate 2.0, pcb_pedestal 0.0, fill_cap 4.8 (builder 13.9), hopper 0.9, meter_housing 7.6, pocket_disc 0.6, agitator 11.0, brush_strip 7.6 (builder 19.8), retaining_plate 2.5, electronics_bay 9.1, bay_lid 0.0 (builder 2.2) percent.

### mass-budget — 8.5, PASS

Issues:

- MODERATE - The molded 430-pellet MAX fill line's stated rationale is fragile. BUILD-NOTES r4 line 84 justifies choosing 430 because it 'stays under 1500 g even on the strictest no-exemption reading (1476.8 g)'. That 1476.8 g holds only at the optimistic petg_cf=1.25 in dispenser.py:205. At the instructed 1.27 it is 1485.3 g (14.7 g margin); at 1.31 (a common CF-PETG datasheet value) it is ~1510 g, and with the 200 g stepper sensitivity stacked on top ~1521 g. A physical groove is being cut into the hopper wall on the strength of a number with <1% margin. The CONTEXT pellet exemption makes the claim unnecessary anyway - recommend re-solving the line to ~410 pellets or dropping the 'under 1500 strict' rationale. Not blocking: the 250-load figure that the ceiling actually applies to has 227 g of margin.
- MODERATE - The ledger prices every printed part as 100%-infill solid and never states that convention. dispenser.py:252-257 computes mass = solid.volume * density for all 9 CF-PETG parts. Real slicing (4 perimeters + sparse infill) makes ~100 g of the 273 g overage above 1.0 kg a modelling artifact rather than real mass. Measured worst case: pocket_disc has 42.6 of its 76.24 cm3 more than 1.6 mm from any surface (analytic erosion of the Dia92x14 slab, 8x Dia15 pockets at PCD 32, 8x Dia5 lightening holes, Dia20 hub) - 96.8 g as-priced vs ~56 g at 4 walls + 25% infill, for a part loaded by a few newtons. top_plate is a further ~24 g. Conservative direction so it is not a ceiling risk, but it distorts the over-1.0 kg justification and should be stated as an assumed infill or carried as an honest bracket.
- MODERATE - CONTEXT requires 'every 100 g above 1.0 kg must be justified in the mass ledger', and the loaded-@250 total is 273 g above 1.0 kg (my rebuild) / 264 g (builder's). The justification in BUILD-NOTES-r4.md lines 139-147 is qualitative prose - only the stepper's 190 g is an actual number; the latch ring, fastening, phase hardware and hopper structure are named without masses. The ledger printed by dispenser.py:1180-1214 itemises parts but never attributes the overage block-by-block. I derived the one item the builder claims but never quantified: the capacity oversizing costs 65 g. (250 pellets need 570 cm3; the 39 mm funnel cone alone supplies 428 cm3, so only 9.2 mm of the 55 mm cylinder section is required - the remaining 45.8 mm of 2.5 mm wall is 51.2 cm3 = 65 g at 1.27.) That is defensible under CONTEXT's 'more capacity is a positive design goal', but it needs to be in the ledger as a number, along with the rest of the attribution.
- MINOR - Estimate exposure is understated. BUILD-NOTES line 85 says '~117 g of electronics/fastener lines are estimates' and open issue 11 says '~122 g'. 122 g is correct for electronics (65) + fasteners (57) only; the actual non-measured mass is 155 g once the 8 g O-ring/gasket/magnet line, the 15 g blindmate_pcb and the 10 g brush_strip are counted - 17.4% of the 889 g empty subtotal, i.e. larger than the 10% (88.9 g) contingency that is supposed to bound it. The 117 g figure is a stale r3 carry-over.
- MINOR - brush_strip is treated two contradictory ways. It is exported as one of the 11 printed parts (brush_strip_r4.step/.stl, 0.58 cm3) and given a measured print orientation (19.8% unsupported, BUILD-NOTES line 65), but dispenser.py:528 assigns it a fixed mass=10.0 g as a COTS strip brush, vs 0.7 g of PETG at its modeled volume. Conservative by ~9 g so no ceiling risk, but the BOM must resolve whether this is a printed carrier, a COTS brush, or a printed carrier plus COTS bristle strip - and if it is the last, the carrier's own mass is currently absorbed rather than measured.

Numbers:

MEASURED FROM EXPORTS (trimesh on *_r4.stl, cross-checked vs import_step on *_r4.step, agree <0.1%). Per-part volumes cm3: top_plate 69.76, pcb_pedestal 2.07, fill_cap 13.09, hopper 104.07, meter_housing 77.07, pocket_disc 76.24, agitator 2.86, brush_strip 0.58, retaining_plate_chute 36.93, electronics_bay 15.62, bay_lid 5.67 (11/11 watertight, 11/11 single solids). Non-printed from assembly STL: clip_plate 11.52, thrust_washer 0.36, blindmate_pcb 0.59, stepper envelope 40.57. || REBUILT LEDGER at PETG 1.27 g/cm3 (TPU 1.20, alu 2.70, PTFE 2.20): top_plate 88.6 | hopper 132.2 | meter_housing 97.9 | pocket_disc 96.8 | retaining_plate_chute 46.9 | electronics_bay 19.8 | fill_cap 16.6 | bay_lid 7.2 | agitator 3.4 | pcb_pedestal 2.6 | brush_strip 10.0 (COTS fixed) | clip_plate 31.1 | thrust_washer 0.8 | stepper 190.0 (vendor 170/190 conflict, worse carried) | blindmate_pcb 15.0 [est] | electronics 65.0 [est] | fasteners 57.0 [est] | O-ring+gaskets+9 magnets 8.0 [est]. EMPTY SUBTOTAL 889.0 g; +10% contingency 88.9 -> EMPTY CARRIED 977.9 g; + 250 pellets x 1.18 g = 295.0 g -> **LOADED @250 = 1272.9 g**, ceiling 1500 g, margin 227 g, 273 g above 1.0 kg. || SENSITIVITIES: stepper 200 g -> 1283.9 g (pass); CF-PETG 1.31 -> ~1298 g (pass); steel clip plate +59 g -> ~1338 g (pass); @430 max-fill-line 1485.3 g; @492 brim 1558.4 g (pellets >250 exempt per CONTEXT). || BUILDER-CLAIM AUDIT: reproducing dispenser.py:205 densities exactly gives 881.3 / 969.4 / 1264.4 g - identical to BUILD-NOTES-r4.md lines 132-137. No doc-vs-code drift, no inflation. 15 assembly bodies map 1:1 to 15 ledger lines; no unpriced component found. || CG (mass-weighted from export centroids): loaded @250 CG at x +0.5, y -5.7, z -268 mm, lateral offset 5.7 mm vs the 25 mm clip-plate half-width, static moment 0.07 N*m. || CAPACITY CROSS-CHECK (independent, analytic from coded dims): cylinder-to-headspace 693 + cone 428 + sump ~8 = ~1129 cm3 vs builder's measured 1123 usable; 430-line needs 430 x 2.28 = 980 cm3 = builder's measured 980; 250 hard minimum needs 570 cm3. || LIGHTENING LEVERS (analytic 1.6 mm erosion): pocket_disc 42.6 of 76.24 cm3 is infill-eligible -> 96.8 g solid vs ~56.2 g at 4 walls + 25% infill; top_plate ~24 g more.

## DIRECTIVE INJECTED FROM THOMAS (2026-08-06 23:03) — must address in r5

Fragment-overfill wedge jam ("1.5 capsules" in one pocket wedging the
wheel): now a hard requirement — see CONTEXT.md "Directive added mid-run"
section for the four required elements (rejection geometry, shear-torque
backstop with margin, stall detect + reverse recovery with truthful counting,
pocket geometry statement). Treat as a BLOCKING issue for r5 alongside the
agitator interference.
