# BUILD NOTES — Round 6 (CAD builder)

Winning concept: **pocket-wheel**. Round 6 closes the r5 critics' blocking
issues (interference **FAIL 4** with two BLOCKERs, pellet-path **FAIL 5** with
three BLOCKERs, buildability PASS 8.5, mass-budget PASS 9 —
`BUILD-NOTES-r5.md` §"Round-5 critics").

Every number marked *measured* is printed either by `cad/dispenser.py` or by
`cad/verify_exports.py`, a second script that reads **only** the exported
STEP/STL, types its coordinates in by hand, and — new in r6 — **imports the
vendor clip-plate STEP itself**, because the r5 critic's MODERATE was exactly
that the "independent" checker never touched the interface. Facts from CONTEXT
are cited; everything else is [D] (derived, math shown) or ASSUMPTION.

Run: `~/.openclaw/workspace/venvs/dock-cad-314/bin/python cad/dispenser.py`
then `.../python cad/verify_exports.py`.

## Deliverables

- Model: `cad/dispenser.py` (parametric build123d)
- Independent checker: `cad/verify_exports.py` (rewritten; now interface-aware)
- Auto-generated `cad/BOM.md` (now including a **fastener table** — r5
  buildability MINOR)
- Exports (`cad/exports/`): `dispenser_r6_assembly.step/.stl` + individual
  STEP+STL for all **10 printed parts** (top_plate, fill_cap, hopper,
  meter_housing, pocket_disc, agitator, brush_holder, retaining_plate_chute,
  electronics_bay, bay_lid — `pcb_pedestal` is **deleted**, see below)
- Renders (cream #faf7f0): `cad/renders/r6_iso.png`, `r6_section.png`,
  `r6_meter_detail.png`, `r6_bottom.png`, `r6_fill_station.png`,
  `r6_cartridge_out.png`, `r6_bay_lid.png`

---

## 1. The two interference BLOCKERs — root cause and fix

**Root cause (one, shared):** r5 *asserted* the interface and then "verified"
it with a probe that could not fail. The clip-plate bolt test was a Ø2.4 × 10
cylinder at (±6.5, ±10.5) against a `residual < 5.0 mm³` threshold — a test a
16 × 24 mm **through-window** passes even better than a hole does. Nothing in
the model or the checker ever looked at the vendor STEP's actual features.

**r6 maps the plate instead of assuming it.** `dispenser.py` now runs a
point-containment scan (0.5 mm grid × 0.4 mm in z) of the imported
`2112_attach_plate_payload_side.step`, clusters the through-open columns, and
**derives** the mounting pattern, asserting the result. Measured, this run:

| mapped feature | measurement |
|---|---|
| through-window (blind-mate shaft) | x ±8.00, y ±12.00, open the full 10.5 mm |
| **mount holes** | 4 × **Ø2.90 at (±19.00, ±19.00)** — a 38 × 38 pattern |
| head pocket above each mount hole | **Ø3.90**, open to the mating plane |
| blind-mate PCB tabs | 4 × **Ø1.90 at (±4, ±10)** inside the shaft |
| solid bolting slab | Z −181.5…−177.4 (4.1 mm) |

- **Mount (BLOCKER 1) — FIXED.** The payload now bolts at (±19, ±19) with
  **4 × M2 SHCS** driven from the drone side; the head sits in the plate's own
  Ø3.90 pocket (measured clearance **0.05 mm/side** — a tolerance item, see
  open issues) and threads into **M2 heat-set inserts** in the top plate. The
  r4/r5 hex-nut bosses and their open-bottom skin problem are deleted.
  Measured per screw: insert-boss stock **52.8 mm³**, shank vs plate **0.00**,
  head envelope vs plate **0.00**, driver column to Z = −171 **0.00 mm³**.
  Independently on the exports: top-plate material in a Ø6.4 × 4 column at each
  (±19, ±19) = **96.8 mm³** (i.e. the screw lands in our part), and the r5
  pattern re-probed with an M3-sized probe leaves **8.54 mm³** of *nothing* —
  it is inside the shaft.
- **Blind-mate (BLOCKER 2) — FIXED, and closed with vendor geometry, not a
  shim.** The r5 pedestal at y = −35 is **deleted as a part**. The
  payload-side Attachment Interface PCB mounts where the vendor plate says it
  goes: **centred in the 16 × 24 shaft on the plate's own 4 × M2 tabs**, pads
  up. The top plate carries a **sealed PCB well** under it (16.4 × 24.4 mouth,
  cup floor 4.5 mm below the plate underside) for the board, its Molex J1 and
  a service loop, plus a **5 × 2.5 mm cable channel** in the top face running
  to the −Y rim: **the harness never enters the pellet space**.
  Measured: payload material inside the shaft column **0.00 mm³**; PCB vs every
  printed part **0.00 mm³**; shaft walls re-measured on the exports at
  **8.00 / 11.90 mm** from centre.
- **The residual, stated:** the drone-side 3331 board (built from the quiver
  source at the bottom port) has its pin tips at **Z = −163.73**, and the
  highest a payload pad can sit without breaching the QR mating plane is
  **Z = −171.0**; our pads sit at the slab underside, **Z = −181.5**. The
  vendor STEP models pin *bodies*, not plunger travel, so the pad-plane
  question is a **pin-length ASSUMPTION** — but it is now a 1-D shim question
  on vendor-owned features (standoffs at the vendor tabs), not a 35 mm
  position error. **Open issue 1.**
- MAJOR "the mis-placed PCB is the tightest clearance in the aircraft-payload
  pair (2.14 mm)" — **gone with the pedestal**: nothing of the payload is now
  outside the 50 × 50 footprint above the plate face except the fill-cap wing
  bar (**584 mm³**, top face Z = −178.4, 7.4 mm below the drone-side QR plate).
- MODERATE "the independent checker does not check the interface" — **FIXED**:
  `verify_exports.py` imports the clip-plate STEP, re-derives the pattern, the
  shaft, the head pockets and the PCB fit, and re-measures ground clearance
  from the assembly bbox.

## 2. The three pellet-path BLOCKERs

### 2.1 Transfer-arc entry relief — FIXED (the ramp is on the right face now)

r5 cut its "45° lead-in" into the roof **top**; the pellet-facing ceiling was a
square step (critic: `None` at 130.00°, 1.508 mm at 129.90°). r6 cuts the ramp
**into the underside** as an inclined plane through the radial line θ = 130°,
so the ramp starts at the same angle at every radius and has the same slope
against arc length at every radius [D]. Measured ceiling height above the disc
(mm; independent export run in brackets):

| θ | 131° | 130° | 128° | 125° | 120° | 110° | 96° | 45° |
|---|---|---|---|---|---|---|---|---|
| r = 24.5 | open | open | 10.00 | 9.25 | 8.25 | 6.25 | 4.00 | 1.50 |
| r = 32.0 (PCD) | open | 10.25 | 9.75 | 9.00 | 7.75 | 5.25 | 2.00 | 1.50 |
| r = 39.5 | open | 10.25 | 9.75 | 8.75 | 7.00 | 4.00 | 1.50 | 1.50 |
| r = 45.5 | open | 10.25 | 9.50 | 8.50 | 6.50 | 3.00 | 1.50 | 1.50 |

Ramp **25°** from horizontal, tangential run **19.3 mm = 34.6° of arc**.
Face-normal audit by the critic's own method, on the exported housing:
**598.9 mm² of upstream-facing entry faces, area-weighted n_z = −0.88, square
stub (|n_z| < 0.05) 2.7 %** (r5: one face, n_z = +0.00, i.e. 100 %).
[D] the shallow ramp is a **force multiplier**: F_vert = F/(tan25 + µ) =
**1.15 F** at µ = 0.4, so it crushes a proud fragment down into the pocket
rather than stubbing it against an edge.

### 2.2 The constructed wedge jam — now defeated with numbers, not rebutted

The r5 critic built the jam and showed all three CONTEXT defences failing. r6
changes the **mechanism**, not the argument.

**(1) Rejection before wedge — a real deflector.** The wiper is
re-architected: **compliant bristles LEAD** (channel moved to the leading
edge), and a rigid **30° DEFLECTOR NOSE** trails them, reaching down to
disc + 3.0 mm, with a 0.6 mm blunt tip. Its face is a *lifting* ramp (normal
up-and-upstream), in the **open fill sector** where a rejected fragment has an
escape path into the sump. This is the rotary-airlock "inlet shear deflector"
(RESEARCH-drone-spreaders §5, countermeasure 1) in hardware.
[D] lift/push = cot(30°) = **1.73** vs the **1.44** needed to break the worst
self-locked sliver (µ/sin(half-angle) at w = 2.0 mm) → **PASS**.
Contact order, swept at 0.25° (model **and** exports):

| fragment proud | first → second → third |
|---|---|
| 2.0 mm | bristles @153.00° |
| 3.0 mm | bristles @153.00° |
| 5.0 mm | bristles @153.00° → holder @149.00° |
| 7.0 mm | bristles @153.00° → holder @149.00° |
| 9.0 / 11.5 mm | holder @157.00° (the **lifting overhang**) → bristles → housing |

Holder face audit: **436 mm² of upstream-facing faces in the pellet band,
area-weighted n_z = +0.67 (lifting), 18.5 % square-stub** — against r5's
77.6 mm² face at n_z = −0.00 leading everything above 5.45 mm.

**(2) Shear backstop — the actuator changed.** CONTEXT requirement 2 asks the
drive to be able to shear a fragment; r5 argued the opposite ("12× under the
crush load") and the critic correctly called that a rebuttal, not compliance.
r6 replaces the direct-drive NEMA 14 with the **same motor plus a 5.18:1
planetary gearbox** (StepperOnline 14HS13-0804S-PG5). Torque is bought with
gearing, **not current**, so the 2 A / 12VSW fuse case is unchanged.

| | r5 | r6 |
|---|---|---|
| drive torque at the disc | 0.18 N·m | 0.39 N·m normal (60 % IRUN) / **0.65 N·m recovery** |
| force at the pocket lip | 5.6 N | **12.2 N normal / 20.4 N recovery** |
| vs 41 N whole-pellet crush ([D] US4172714, research §1.3) | 7.3× under | 3.4× under (normal) / 2.0× under (recovery) |
| vs worst wedged-sliver shear | 0.6× — **fails** | **2.2×** — passes |

Reconstructed wedge (worst-case D13 pellet in the Ø15.0 bore):

| sliver w | seats y above centre | its top below the shear line | wedge half-angle | self-locking? | height to reach the nose | shear area | shear force |
|---|---|---|---|---|---|---|---|
| 1.0 mm | 0.00 | 8.00 | 0.0° (parallel slot, not a wedge) | — | 11.00 mm | 6.9 mm² | 2.5 N |
| 2.0 mm | 3.46 | 4.54 | 16.1° | **yes** (µ = 0.4 → 21.8°) | 7.54 mm | 17.0 mm² | 6.1 N |
| 3.0 mm | 4.69 | 3.31 | 23.1° | no | 6.31 mm | 25.5 mm² | 9.2 N |
| 5.0 mm | 6.00 | 2.00 | 33.7° | no | 5.00 mm | 25.0 mm² | 9.0 N |

Shear-capability bound: at 20.4 N the drive shears any proud section up to
**57 mm²** (whole pocket bore = 177 mm²; worst credible wedged sliver
25 mm²). Shear stress = **0.36 MPa**, the value the US4172714 crush figure
normalises to — **ASSUMPTION**, closed by an IFDC S-115 bench test.

**(3) Detect + recover.** Per-pocket Hall magnet (8) + index magnet → phase is
verified **every index**, not only at boot (Judge 1's item); StallGuard plus
gearbox current sensing; recovery = reverse-oscillate at normal current →
bounded shear attempts at 100 % current with the chute beam armed → fault. The
count sensor is 40 mm **below** the meter, so no recovery can manufacture a
phantom count.

**(4) Pocket geometry.** Bore r7.50 × 14.0 deep + 0.5 under-gap; a seated D13
pellet's crown sits **1.50 mm below the shear line** — a whole seated pellet is
never in the shear plane. Anything that settles below that line rides through.

### 2.3 Rigid-leads-compliant — FIXED

See the contact-order table above. Additionally the rail's leading edge is now
a 45° **overhang** (bottom edge upstream of the top edge) so even an object
taller than the rail meets a lifting face, and the ramp/overhang are blunted
(0.6 mm tip face, chamfer stopped 0.6 mm short of the rail top) so the printed
part has no knife edges.

## 3. Other r5 critic items — disposition

| Issue (r5 critic) | Disposition |
|---|---|
| pellet-path MAJOR: no torque budget; an unspecified M5 plunger needs 0.2–1.1 N·m, up to 6× the whole motor | **FIXED.** Full budget printed every run (below). The detent is now a **shallow spherical seat R8 × 0.4** with a **specified light plunger (2.5 N end force)**: flank 18.2° → 2.10 N at r46 → **96.5 mN·m**, i.e. 25 % of the normal drive torque instead of 100–600 % |
| MODERATE: sump window 2.04× D, 67 % dead shelf, agitator has ZERO relative motion over the pockets | **PART-FIXED, part REBUTTED.** The zero relative motion is inherent to the one-motor architecture and is now stated plainly, not implied: the agitator stirs the *bed*, it cannot re-level a pocket. What r6 adds is a stationary element that *does* have full relative motion over the pocket band — the wiper's deflector nose sweeping at disc + 3.0 mm across r20…46.7. The 26.5 mm × 120° window is unchanged and still below every no-arch criterion; the defence remains agitation + reversibility + 68° cone |
| MODERATE: drop window only 1.18× the free-fall time; the 150 ms contract is not derived from it | **DESIGNED OUT.** The index is now **two-phase**: park (+22.5°) → index 22.5° so the pocket is **concentric** with the port → **dwell** → index 22.5° to the next park. The drop window becomes a firmware dwell (150 ms vs a **54 ms** fall to clear the pocket = 2.8×), and the clear aperture at release is the full Ø18 port instead of a moving lune |
| MINOR: "ZERO imparted lateral velocity" is wrong (167 mm/s at PCD → ~0.2 m of scatter) | **FIXED by the same change.** The pellet is released from a **stationary** pocket, so zero is now true by construction — and the claim is stated that way, with r5's error quoted |
| MODERATE: park lens understated 1.4× (probe used r9, the part has r10.5) | **FIXED.** The retaining rim is a named parameter (`PORT_RIM_R`), the top chamfer is cut **1.5 → 0.75 mm**, and the lens is **4.76 mm** (measured port radius at the plate top: 9.59 mm on the export). Park retention margins vs the rim: **D13 +1.74, D12 +1.24, D11 +0.74 mm** (r5's D11 case measured −0.014 mm) |
| MINOR: unswept sump ring is 343 mm², not 147 | **FIXED.** Fingers to r46.7 and the ring is now measured against the **real cone foot** (measured r47.40), not the chamber wall: **207 mm², 0.70 mm wide** |
| buildability MODERATE: igus JFM-2022-04 not confirmed catalogued | **FIXED.** Now **JFM-2023-07** (ID20/OD23/L7) — the 07/11/16/21 lengths are listed by distributors. Roof thickened 6 → 9 mm to seat it (counterbore 1.7 + sleeve 7.0 = 8.7 of 9.0), which also lifted the bristle trim 4.25 → **6.25 mm**. L/D 0.20 → **0.35**. Flange Ø30 × 2 remains an ASSUMPTION |
| buildability MINOR: BOM omits fasteners | **FIXED** — `cad/BOM.md` now carries a 14-line fastener table with quantities and lengths |
| buildability MINOR: top_plate 2.9 % sub-1.95 mm at the nut-boss webs | **DESIGNED OUT** with the nut pockets: top_plate now measures **min 1.13 / p1 2.00 / p5 2.05, 0.4 % under 1.95 mm** |
| buildability NIT: stale stack comments | Comments on the changed blocks rewritten; the Z stack is fully derived and the r6 values are in the `verify_exports.py` docstring |
| mass MINOR: 393-pellet rib label vs 391 measured | **SUPERSEDED** — the rib rule changed (below) and both ribs are re-measured from the exported volume each run (422 → 420, 250 → 248) |
| mass MINOR/NOTE: estimate exposure, knife-edge no-exemption line | Exposure re-printed (**150.5 g, 15.2 %**); the no-exemption line is now *reported* rather than *used* — see §5 |

## 4. Measured numbers (r6)

Model run and independent export run agree on every shared figure.

- **Connectivity:** 16/16 parts single solids in-model; 10/10 exported STEPs
  re-import as 1 solid; 10/10 part STLs watertight; assembly STL **16 bodies,
  16 watertight**
- **Envelope:** bbox X ±75, Y −90…+75, Z −366.4…−171.0 → stack **195.4 mm**,
  **ground clearance at rest 181.5 mm** (ground Z −547.89). Full-gear
  mesh-to-mesh **83.41 mm** (r5 critic independent: 83.42). Props (cited, r3
  full-assembly): vertical 152.5 mm, radial 239.3 mm
- **Interface:** mount pattern derived = (±19, ±19); Ø2.90 holes; Ø3.90 head
  pockets (M2 head Ø3.8 → 0.05 mm/side); shaft ±8.00/±12.00; payload material
  in the shaft **0.00 mm³**; payload outside the 50 × 50 footprint above the
  plate face **584 mm³** (fill-cap wing bar only)
- **Torque budget (mN·m at the disc):** bed friction 28.6 (Janssen p_sat
  1111 Pa × 1894 mm² = 2.1 N, µ = 0.4) + agitator 41.1 + deflector nose 13.1 +
  bearing/thrust 11.5 + detent 96.5 = **190.7 total**; normal drive **390**
  (2.1×), recovery **650**
- **Meter:** pocket pitch 25.1 mm, web 10.1 mm; seated worst-case pellet
  1.50 mm below the shear line; stacked second sphere protrudes 11.5 mm;
  wiper station 13 mm wide, θ = 131.4…154.6°, ending **1.4° = 0.76 mm before** the roof entry (r5 measured this from the wiper plane, which flattered it)
- **Wiper:** rail 13 × 3 mm; bristle channel 1.8 × 1.2 at the leading edge;
  free trim **6.25 mm**; deflector nose 30°, tip at disc + 3.0, blunt face
  0.6 mm; holder beam at the full 20.4 N recovery force: σ = **1.6 MPa**,
  deflection 0.004 mm
- **Bearing/drive:** JFM-2023-07 ID20/OD23/flange Ø30; journal band 7.0 mm at
  z −282.90…−275.90; **0.10 mm radial running clearance** modelled (hub Ø19.8);
  [D] p = 3 N/(20 × 7) = 0.021 MPa vs ~35 MPa (1633×); hex engagement 5.70 mm
- **Sump:** aperture **26.50 mm × 120°** (equivalent D48.7, 2.04 × D_max);
  funnel **68.1°** measured on the export (claim 68.0); agitator film 0.55 mm;
  unswept ring **207 mm²**
- **Pellet transit, Ø13 worst case, 23 stations, 0.000 mm³ everywhere**
  (in-model) and 11/11 stations 0.000 mm³ re-run independently on the exports
- **Service:** cartridge drop-out sweep **0.00 mm³** (model and exports, 21
  steps × every static part); Ø8/Ø12 rods from below to the wiper plane, roof
  edge and fill arc **0.00 mm³**; wiper slide-out **0.00 mm³**; service-drain
  residue **115 cm³ ≈ 51 pellets**
- **Fill cap:** lift 6.45 mm vs 7.39 mm headroom, then **58 mm of lateral
  travel** in a 10.5 mm gap → **on-aircraft refill is not claimed**
- **Wall thickness (min / p1 / p5, % under 1.95 mm):** top_plate
  1.13/2.00/2.05, 0.4 % · hopper 0.74/2.08/2.10, 0.3 % · meter_housing
  0.01/1.28/2.45, 1.5 % · pocket_disc 1.51/2.00/5.79, 0.9 % ·
  retaining_plate_chute 0.10/2.00/2.00, 0.7 % · electronics_bay
  0.25/2.00/2.00 · bay_lid 0.02/2.00/2.00 · fill_cap 0.90/1.30/1.40, 5.7 % ·
  agitator 1.50/1.50/1.50, 11.7 % · **brush_holder 0.00/0.26/0.60, 28.1 %**
  (open issue 4)
- **Plate webs:** solid runs r39.0–40.4, r43.6–45.6, r46.8–47.9 → critical web
  **1.90–2.00 mm**
- **Print orientations (best of 6, as-modeled in brackets):** top_plate 3.7 %
  (39.0), fill_cap 4.0 (39.2), hopper 0.9 (2.8), meter_housing 7.5 (17.8),
  pocket_disc 3.0 (3.0), agitator 8.9 (11.2), brush_holder 6.2 (30.1),
  retaining_plate_chute 2.4 (24.8), electronics_bay 7.6 (10.3), bay_lid 0.0
- **Interference:** 120 pairs, 38 bbox-overlapping pairs boolean-checked,
  **0 collisions, 0 check-failures**
- **Capacity:** usable hopper volume **963 cm³ → 422 pellets** worst-case
  barrel packing (498 g) / 587 sphere basis — **1.69 × the 250 hard minimum**
- **Mass ledger (100 % infill from measured solids):** empty **993.1 g** +
  10 % → **1092.4 g carried empty**; **LOADED @250 = 1387.4 g (113 g under the
  1.5 kg ceiling)**; brim @422 = 1590.4 g (pellets above the 250 baseline are
  exempt per CONTEXT). Sensitivities: stepper 380 g gross → 1475 g; steel clip
  plate → 1452.3 g; CF-PETG 1.31 → 1412.6 g (all pass). Slicer bracket:
  501.4 g of printed parts → **334.0 g** at 4 walls + 25 % infill → LOADED
  @250 would be **1203.3 g**

### Over-1.0 kg justification (partitioned)

387.4 g over at the 250 load. Geared stepper 310.0 (the gearbox **is** what
makes CONTEXT requirement 2 achievable — 20.4 N vs r5's 5.6 N — while the
driver current limit keeps normal metering 3.4× under the crush load) +
capacity oversizing 46.2 (the 36 mm of cylinder wall above the 250-pellet
line) + latch ring/lugs 16.5 + 15.2 of the fastening/phase-hardware block =
**387.4 g, nothing unattributed**.

## 5. The fill-line rule changed (and why that is the honest call)

r5 solved the MAX fill rib from a quadruple-conservative ledger (CF-PETG at
1.31, stepper at its heavy vendor figure, 100 % infill, +10 %) **and** refused
CONTEXT's explicit exemption for pellets above the 250 baseline. With a
+110 g geared drive that rule now returns **242 pellets — below the 250 hard
minimum**, i.e. it is infeasible, not binding. r6 therefore:

- puts the **MAX rib at the volumetric brim line (422 pellets)**, re-measured
  from the exported hopper at 420;
- keeps the 250-pellet baseline rib (re-measured 248);
- **prints both no-exemption numbers anyway**: 242 pellets on the
  quadruple-conservative ledger, ~398 on the measured-infill ledger.

The ceiling case is the 250 load at **1387.4 g**, 113 g clear.

## 6. Documentation corrections this round forces (into CONCEPT/README)

Carried from r5 (all still true): §3 "~95 mm orifice" → **26.5 mm annular
window × 120°, D48.7 equivalent, 2.04 ×**; §5 "the chute angles the drop line
back to the centreline" → **straight and vertical at x = +32**; §2.3 "~20 mm
trim" → **6.25 mm of free trim**; §6 mass table superseded. New for r6:

1. §2.4 "NEMA-14 stepper, direct drive (no reduction) … the motor *is* the
   torque limiter, 12× below the crush load" → **5.18:1 geared NEMA 14, two
   current settings: 12.2 N metering / 20.4 N recovery at the pocket lip**. The
   "12× below crush" framing was the thing that made CONTEXT requirement 2
   unachievable.
2. §2.3 "brush wiper … strips any second pellet back into the pool" → the
   brush handles the compliant band; a **30° rigid deflector nose** does the
   rejecting, and the two are one field-replaceable part.
3. §4 dispense cycle "index 45°; expect one gated dark-time event" → **two
   phase: 22.5° → dwell ≥150 ms → 22.5°**, one pellet per 45°.
4. §5/§6: the payload mounts with **4 × M2 at (±19, ±19)** and the blind-mate
   PCB sits **on the clip plate's own tabs**, not on a payload pedestal.

## 7. Open issues for round 7 / bench

1. **Blind-mate pad plane.** The drone-side pin tips are at Z = −163.73
   (measured from the quiver source); our pads are at −181.5 and the highest
   legal pad plane is −171.0. The vendor STEP does not model plunger travel.
   Resolve against the physical 2112 set and shim with standoffs on the
   vendor tabs. **Not closable in CAD.**
2. **M2 head clearance is 0.05 mm/side** in the mapped Ø3.90 pocket. If the
   physical part is tighter, the fallback (documented, not modelled) is to
   countersink the four vendor holes 90° × Ø6.0 and use M3 flat-heads.
3. **Caliper survey still gates the print** (all-judges item #1): `DISC_T`,
   `POCKET_R`, `BRUSH_WIPE`, `NOSE_GAP` must be re-frozen against 20+ real
   pellets.
4. **brush_holder thin-section statistics** (min 0.00 / p1 0.26, 28.1 % under
   1.95 mm) are dominated by the 30° wedge and the 45° overhang — wedge
   geometry, not walls; the tip is blunted to 0.6 mm and the part is
   stress-checked at 1.6 MPa under the full 20.4 N. It should still be printed
   and pulled before it is trusted.
5. **The 0.36 MPa pellet strength and the 41 N crush load are class-derived**
   (US4172714 via RESEARCH-drone-spreaders §1.3). Every torque margin in §2.2
   scales with them. IFDC S-115 on real pellets closes it.
6. **Detent plunger end force is now a specification (2.5 N)** — it must be
   bought as a light-spring part, and the release torque re-measured on the
   bench; a standard-force plunger would eat 40 % of the drive.
7. **Gearbox backlash ≤3° at the output** = 1.7 mm at the PCD. Normal indexing
   is unidirectional so it does not accumulate, and the per-pocket Hall
   verifies phase every index — but the reverse-oscillate recovery crosses it
   twice per cycle. Bench item.
8. Agitator is still retained by **gravity only**; the drain-by-inversion
   procedure drops it off the hex (argued behaviour, untested).
9. Attrition/fines: the 1.0 mm disc-rim shear gap, the wiper contact, the new
   deflector-nose plough and the 0.55 mm finger film all feed the only count
   sensor. Unmeasured (survey open unknown #2).
10. Sensor bench test with dusty/fragmented pellets freezes the dark-time
    thresholds; capacitive-ring fallback envelope preserved (chute ID 22).
11. Gasket grooves at the perimeter joints are still schematic (only the
    fill-cap O-ring gland is real geometry); the PCB well is closed by the
    board + clip plate with ~0.2 mm gaps — dust-tight enough that nothing
    reaches the hopper, but it is not sealed.
12. Skirt-tab joint is 3 × M3 plastite into printed pilots carrying the
    cartridge + pellet column; pull-out to be verified on the printed part.
13. Near-empty skip behaviour remains bench-unproven (concept §10.3).
14. Clip-plate orientation ASSUMPTION (the 4 mm solid slab is the payload-side
    bolting face) — consistent with the QR mechanism living in the frame
    cavity above it, but confirm on the physical part.

---

## Round-6 critics

Verbatim critic output, no softening.

### interference — score 7 — FAIL

**Issues**

- BLOCKER — blind-mate (r5 BLOCKER 2) reported FIXED but still open, measured 19.350 mm axial gap. The payload blind-mate PCB (assembly solid 15) sits at X ±8.000, Y ±12.000, Z −188.100…−181.500 — entirely BELOW the clip plate, with 0.000 mm³ inside the 16×24 shaft. The drone-side 3331 board's 10 spring pins (2×5 array, X −5.70…−1.38, Y −6.27…+5.67) tip at Z = −162.150. Pads at −181.500 → gap 19.350 mm; even at the notes' own stated maximum legal pad plane (−171.0) the gap is 8.850 mm, vs typical spring-pin travel ≤2 mm (ASSUMPTION). BUILD-NOTES-r6 §1 states 'the PCB mounts centred in the 16 × 24 shaft on the plate's own 4 × M2 tabs' and offers 'payload material inside the shaft column 0.00 mm³' as proof — that metric is precisely the evidence the PCB is NOT in the shaft. Same failure pattern the r5 critic named (a test that cannot fail). 10.500 mm of the gap is payload-controllable (one plate thickness); the residual 8.850 mm is aircraft/ICD-side and is correctly un-closable in CAD.
- MAJOR — the escape route the notes rely on is geometrically foreclosed, and was not tested. I swept the payload clip half upward into the drone-side 2112 channel at 0.05 mm steps in all 8 poses (Rot X ±90 × Rot Z 0/90/180/270): it collides after at most 0.54 mm. The drone-side plate is a 50×50 shell with perimeter walls solid through the entire −171.047…−155.047 range (probed solid at (0,23) and (24,24)) and an interior roof at ≈ −157.0. So face-to-face at −171 is the only arrangement the vendored geometry supports, and the notes' proposed fix ('shim with standoffs on the vendor tabs') would push payload material ~8.9 mm ABOVE Z = −171 — directly contradicting the same paragraph's constraint that −171.0 is the highest a pad may sit. This needs escalating to the ICD owner as an aircraft-side defect, not absorbing as payload Open Issue 1.
- MODERATE — a quoted 'measured' number is a mis-identified solid. BUILD-NOTES-r6 §1 and Open Issue 1 give the drone-side pin tips as Z = −163.73. That is the lowest solid on the 3331 board — a 224.5 mm³ connector housing at X +1.00…+6.08, Y −6.60…+6.10, Z −163.73…−160.25. The actual spring pins are ten 3.79 mm³ solids spanning Z −162.150…−159.940. Every margin derived from −163.73 is 1.58 mm optimistic.
- MODERATE — if the PCB were moved into the shaft as the notes claim, it is unassemblable. I bisected the vendor shaft to 1e-4 mm at three heights: it is exactly 16.0000 × 24.0000 through the full slab. The modelled payload PCB is exactly 16.000 × 24.000. That is 0.000 mm clearance per side. Round 7 must both drop the board into the shaft AND give it real clearance (or confirm the true 3331 outline).
- MINOR — 0.0397 mm³ of nominal overlap between the payload clip plate (top face Z = −171.000) and the drone-side 2112 QR plate (measured underside Z = −171.047). This is an artefact of the ICD's 'roughly Z = −171 mm' rounding, not a design error, but the r6 notes assert 'nothing of the payload is now outside/above the plate face' without reporting it.
- OBSERVATION (not blocking) — the fill-cap wing bar is the only out-of-footprint feature, 584.36 mm³ at X ±12.00, Y +41.00…+49.00, Z −181.50…−178.40. It clears the drone-side plate underside by 7.35 mm and has no plan overlap with either the ±25 body or the press-pin lugs (Y −6.46…+6.54). Confirmed clear; noted only because it is the single feature that would move first if the whole payload stack is later shifted up in Z to close the blind-mate.

**Numbers**

GROUND: gear lowest point (foam OD40 about tube axis −527.884) Z = −547.884; dispenser lowest point Z = −366.400 (X ±17.60, Y ±17.60) → ground clearance 181.484 mm vs ≥40 mm required (4.5×, 141.5 mm of margin). Foam fully crushed to bare tube OD (−542.890) → 176.490 mm. Min payload↔landing-gear separation 83.41 mm, payload (−52.1, 53.9, −181.5) to FL leg adapter (−103.3, 107.6, −143.4) — matches builder's 83.41. PROPS: 4 swept disks R = 305.04 mm (Ø610.1) at (±449.43, ±449.43), geometry Z −18.50…+63.45; payload top −171.000 → vertical 152.50 mm; disk-centre radius 635.59, inner edge 330.55, payload max plan radius 93.41 → true min in-plan gap 251.13 mm (builder's 239.3 conservative); zero plan overlap. CLIP PLATE: placed X ±25.000, Y ±25.000, Z −181.500…−171.000, vol 11523.4 mm³; payload material above Z = −171 = 0.000 mm³; material in the −181.5…−171.0 band = 584.36 mm³, 100% of it outside the 50×50 (fill-cap wing bar, X ±12.00, Y +41.00…+49.00, Z −181.50…−178.40), 7.35 mm below the drone-side plate underside −171.047. All 16 assembly solids vs 2112 / 2131 / 3331 / 1113: total overlap 0.0397 mm³ (the 0.047 mm ICD rounding only). SELF-INTERFERENCE (exported assembly STEP, independent): 16 solids, 120 pairs, 36 bbox-overlapping, 0 collisions >0.01 mm³. VENDOR PLATE RE-MAP (point containment + bisection, independent of the builder): 4 through-holes Ø2.96 at exactly (±19.00, ±19.00); head pockets Ø3.96; tab holes Ø1.96 at (±4, ±10); shaft through-open 16.0000 × 24.0000; bolting slab Z −181.50…−177.50 (4.00 mm) — all corroborate the builder's 2.90 / 3.90 / 1.90 / ±8.00 / ±12.00 / 4.1 within probe resolution. MOUNT LANDS IN PAYLOAD: top_plate = 109.04 mm³ in a Ø6.4 × 4 column at each of (±19, ±19). BLIND MATE (the failure): payload pads Z = −181.500; drone-side spring-pin tips Z = −162.150 (10 pins, 2×5, X −5.70…−1.38, Y −6.27…+5.67) → gap 19.350 mm; at the best legal pad plane (−171.0) still 8.850 mm; payload PCB 16.000 × 24.000 in a 16.0000 × 24.0000 shaft = 0.000 mm clearance; clip half nests at most 0.54 mm into the drone-side channel over 8 tested poses. CG: printed-parts centroid (1.73, −3.24, −257.05), in-plane offset 3.67 mm from the mount axis.

### pellet-path — score 5 — FAIL

**Issues**

- BLOCKER 1 — UNINTENDED ROOF THROUGH-SLOT + 238 mm2 SQUARE STEP AT theta=310deg (new in r6, created by the fix for the r5 entry-ramp blocker). The r6 entry ramp is cut with a HALF-SPACE, not a sector: dispenser.py ~L737-750 builds ramp_cut from ramp_half & Box(400,200,100) at y<=0, then Rot(Z=130). The half-plane y'<0 covers theta from 310deg all the way round through 0deg to 130deg, so the same 25deg undercut is MIRRORED at theta=310deg. MEASURED on the exported B-rep (meter_housing_r6.step, 1 solid) by boolean sector intersection: roof material in theta 309-310deg = 138.4 of 138.4 mm3 possible (9.00 mm thick, full); theta 310-311deg = 2.2 of 138.4 mm3 -> MEAN THICKNESS 0.14 mm; 311-313deg = 0.57 mm; 313-316deg = 1.28 mm; 316-322deg = 2.55 mm. Point probe on the STL and on dispenser_r6_assembly.stl: at theta=310.0deg the roof thickness is 0.000 mm at r = 20.5, 24.5, 30, 32, 36, 39.5, 44, 46.5 — an OPEN THROUGH-SLOT from the pellet bed straight into the transfer arc, ~0.86-1.7 mm of arc wide (thickness < 0.4 mm extrusion out to ~312.4deg) x 26.5 mm radial = 23-46 mm2 of aperture. Consequences: (a) fines and slivers sift out of the bed into the close-clearance (1.50 mm) metering arc DOWNSTREAM of every rejection feature — bristles, deflector nose and entry ramp are all at theta=130-155deg; (b) the boundary at theta=310.0deg is a VERTICAL face 9.00 mm tall x 26.5 mm radial = 238 mm2, n_z = 0.000, facing directly into the direction of disc travel (disc runs -theta, arrow engraved), i.e. the exact square-stub failure the r5 critic blocked at the entry, reproduced at the far end of the same cut and never audited (the r6 face-normal audit and the ceiling table only sample theta 131..45); (c) the roof is also the sump floor and the structural tie from the chamber wall to the bearing boss, and it is severed to 0.0-1.3 mm on a radial line over theta 310-315deg. This is what the builder's own 'meter_housing min wall 0.01 mm, p1 1.28, 1.5% under 1.95' statistic is reporting, mis-attributed to the entry ramp.
- BLOCKER 2 — THE DROP-WINDOW DERIVATION MEASURES A WINDOW THE PELLET NEVER USES; 'stationary release / zero lateral velocity / full Dia18 aperture' is geometrically false. MEASURED from retaining_plate_chute_r6.stl: exit port Dia18.00 (r 9.00) at PCD 32.00, 0.75x45deg top chamfer, rim radius at the plate top r = 9.75 (first material 9.66 at 0.10 below the plate top). Pocket bore r 7.50 (measured), pellet r 6.50, so the pellet centre can sit 1.00 mm either side of the pocket axis. At park the pocket-port centre separation is 2*32*sin(11.25deg) = 12.485 mm. The pellet rests on the STATIONARY retaining plate and loses support when its contact point crosses r = 9.75, i.e. at a separation of 8.75-10.75 mm = 15.72-19.34deg from concentric = 3.16-6.78deg into the 22.5deg index move (14-30% of the move). The pellet is therefore released WHILE THE DISC IS MOVING, through a partial lune, and the 150 ms dwell it is supposed to fall through has not started. BUILD-NOTES-r6 §3 claims the opposite twice ('the clear aperture at release is the full Dia18 port instead of a moving lune'; 'the pellet is released from a stationary pocket, so zero [lateral velocity] is now true by construction — with r5's error quoted'). The '150 ms dwell vs 54 ms fall = 2.8x' margin is measuring the wrong interval. Physical cost: at release the pellet is being driven by the pocket wall at v = omega*32 mm; a 22.5deg index at a modest 225 deg/s mean gives 0.126 m/s -> 0.16 m of lateral drift over the 1.28 s fall from 8 m AGL (0.32 m at a 450 deg/s trapezoid peak) against a 1 m total accuracy budget, and the release angle itself spreads 3.62deg of disc rotation depending on whether the pellet rides the leading or trailing pocket wall.
- MAJOR 3 — THE REJECTION BAND STARTS ABOVE THE SHEAR BAND: a 1.50 mm blind band that only compliant bristles touch, and the constructed wedge lands in it. MEASURED: roof underside clearance above the disc top = 1.50 mm through the whole transfer arc (theta 130->0, r 24.5/32/39.5/45.5); deflector-nose underside = 3.00 mm above the disc, constant over r = 22.0-46.5 (measured on brush_holder_r6.stl); bristle tip = 1.20 mm (assembly body 10, z -283.50). So any object whose crown is 1.50 < p <= 3.00 mm proud passes the nose untouched and meets only a 6.25 mm-trim nylon strip. Constructed cases inside the band, solved against the MEASURED pocket chamfer (bore r7.50 at 2.00 below the top, flaring 45deg to r9.50 at the disc top) with a seated Dia13 pellet (crown 1.50 below the top, centre 8.00 below): a Dia5.0 fragment nesting in the chamfer against the pellet sits +1.80 proud, a Dia6.0 fragment +2.95 proud — both inside the band; only Dia7.0 (+4.08) reaches the nose. Equivalently, a 3.00-4.50 mm chip UNDER a seated D13 pellet (4.00-5.50 under a D12) puts the crown in the band. These are carried into the arc and are defeated only by CRUSHING under the 25deg entry ramp — CONTEXT defence 2, not defence 1 ('reject before wedge'), which the notes claim. It does hold with margin: the Dia6 fragment presents 20.7 mm2 at the 1.50 mm shear plane = 7.5 N at the class 0.36 MPa, vs a ramp normal force of F/(tan25+mu) = 1.15F = 14.1 N normal / 23.4 N recovery (1.9x / 3.1x), and the ramp is 7.6 mm thick at the contact point. But the notes' own contact-order table answers 2.0 mm and 3.0 mm proud with 'bristles @153.00deg' — a compliant element that cannot reject a rigid wedged fragment. Fix is one parameter: NOSE_GAP 3.00 -> <=1.50 mm (= ROOF_CLEAR).
- MODERATE 4 — THE 68deg FUNNEL DOES NOT DISCHARGE TO A PELLET-SCALE OUTLET; the real outlet is a 0deg flat shelf with a 2.04x slot. MEASURED on hopper_r6.stl: cylinder r70.00 from z -186.5 to -218.5, then a clean cone to r47.50 at z = -274.20, wall angle 68.0deg from horizontal (r65.40@-230 to r49.20@-270 -> atan(40/16.2) = 67.9deg). But the cone foot lands on a FLAT (0deg from horizontal) shelf — the meter_housing roof top at z = -274.20, solid from r15.20 to r47.00 — whose only opening is the 120deg x 26.5 mm annular window (measured: solid bands r15.20-20.00 and r47.90-52.00 at theta=200deg, vs r15.20-18.02 / r47.02-52.00 at theta=310deg). Minimum outlet dimension / worst-case pellet = 26.50/13.0 = 2.04 (2.21 on the 12 mm nominal), below every no-arch rule (>=3x for a slot); ~66% of the outlet plane by area is dead flat shelf. The >60deg-at-outlet criterion is therefore met only through the active-agitation branch, and the agitation duty cycle is not in the notes: 3 fingers at 120deg over a 120deg window means exactly one finger is in the window at a time, and each 22.5deg index sweeps 22.5/120 = 18.8% of it, so a given angular location of the outlet is agitated once per 5.33 indexes = once per 2.67 pellets dispensed. The agitator also only moves when the meter indexes (same shaft), so an arch cannot be cleared except by commanding dispense cycles. Finger film measured 0.55 mm above the shelf, flange 0.35 mm; fingers reach r46.70 vs the measured chamber wall r47.00.
- MODERATE 5 — NO ISOLATION GATE: no jam can be cleared in the field without dumping the hopper. The pocket disc IS the sump floor (the 120deg window opens straight onto it), so the documented recovery is: QR-release the payload, invert it, remove the fill cap, pour 250-422 pellets (295-498 g of tebuthiuron) back into a tub, then drop the cartridge — which still spills a printed 115 cm3 ~= 51 pellets. dispenser.py L1806-1813 states the drain procedure but neither the notes nor the README state the operational consequence: a single mid-sortie fragment stall costs a full unload/reload cycle on the tailgate, in wind and dust, with an open herbicide hopper. Ground clearance is adequate for the work (chute bottom z = -353.20, motor bottom -366.40, 181.5 mm to the ground) and the cartridge drop-out is genuinely clean, but nothing can be touched with the hopper loaded.
- MINOR 6 — meter_housing_r6.stl is NOT watertight: one non-manifold edge shared by 4 faces at (20.891, -24.896, -274.200) — r = 32.50, theta = 310.0deg, i.e. exactly on the theta=310 ramp-bug line, on the sump-floor plane. BUILD-NOTES-r6 §4 claims '10/10 part STLs watertight' and 'assembly STL 16 bodies, 16 watertight'; measured 15/16 (assembly body 4 = meter_housing fails). The independent checker verify_exports.py does not catch it.
- MINOR 7 — the derived-Z-stack comments in dispenser.py L384-397 are still stale after r5 flagged them as fixed ('Comments on the changed blocks rewritten'): the file says Z_HOP_BOT -241.5, Z_FUN_BOT -280.5, Z_ROOF_BOT -284.5, Z_DISC_TOP -286.0, Z_DISC_BOT -300.0, Z_RPLATE_TOP -300.5, Z_RPLATE_BOT -304.5. MEASURED on the exports: -218.50, -274.20, -283.20, -284.70, -298.70, -299.20, -303.20 — off by 5.3 to 23.0 mm. Anyone reading the model to reason about the pellet path (as this critic did first) is reading the wrong stack.
- NIT 8 — second, unanalysed fines path: the disc's 8 lightening holes (Dia7.0 at r18.5, spanning r15.0-22.0) break into the sump window, whose inner edge is r20.00, over a 2.0 mm crescent. Fines and small fragments entering there land in the 0.50 mm under-gap, and the inner fines slots in the retaining plate start at r19.50, so a fragment that settles at r < 19.5 is dragged a full revolution against the plate before it can shed.

**Numbers**

MEASURED (all on cad/exports/*_r6.stl/.step, independent of dispenser.py; venv dock-cad-314, trimesh + build123d). Z STACK measured: mount -171.00, clip bot -181.50, top-plate bot -186.50, hopper cyl bot -218.50, funnel/shelf -274.20, roof bot -283.20, DISC TOP -284.70, disc bot -298.70, plate top -299.20, plate bot -303.20, chute bot -353.20, motor bot -366.40. CHANNEL DIMS vs 13.0 mm worst-case pellet: fill port Dia46 (3.5x) -> hopper Dia140 -> funnel 68.0 deg cone (measured 67.9) to Dia95 -> OUTLET = flat 0-deg shelf r15.20-47.00 with a 120 deg x 26.50 mm window (2.04x, governing for arching) -> pocket bore Dia15.00 x 14.00 deep + 0.50 under-gap = 14.50 seat (1.15x, tightest true channel) -> exit port Dia18.00 + 0.75x45 chamfer to rim r9.75 (1.38x) -> chute Dia22.0 x 50 (1.69x). PINCH POINTS: roof-underside clearance 1.50 mm (measured 1.50 at r24.5/32/39.5/45.5 over theta 250->96 and 45->0), nose underside 3.00 mm (constant r22-46.5), bristle tip 1.20, disc rim gap 1.00 (chamber r47.00 vs disc OD 46.000), under-gap 0.50, agitator finger film 0.55. SEATED D13: crown 1.50 below the disc top = 3.00 below the roof; contacts the roof only at D>16.0. ENTRY RAMP verified GOOD: true underside ramp, ceiling above disc = 10.24@129, 9.98@128, 9.20@125, 7.92@120, 5.40@110, 2.00@96, 1.50@<=95 (PCD) — matches the builder's table, 25 deg at every radius, no square step at the entry (r5 blocker genuinely fixed there). PARK RETENTION verified: separation 12.485 mm, worst-placed D13 contact at 11.485 vs rim 9.75 -> 1.735 mm margin (builder +1.74). NEW BLOCKER: roof thickness at theta=310.0 deg = 0.000 mm at r=20.5/24.5/30/32/36/39.5/44/46.5 (STL, STEP and assembly all agree); B-rep sector booleans give 138.4/138.4 mm3 (9.00 mm) at 309-310 deg but 2.2/138.4 mm3 (0.14 mm mean) at 310-311, 0.57 mm at 311-313, 1.28 at 313-316, 2.55 at 316-322 -> 23-46 mm2 open slot + a 9.00 x 26.5 = 238 mm2 vertical face at n_z=0.000 facing the direction of travel. DROP: support lost at 8.75-10.75 mm separation = 15.72-19.34 deg from concentric = 3.16-6.78 deg into the 22.5 deg index (14-30% of the move), not at the dwell; v_lat = omega*32 mm -> 0.126-0.25 m/s -> 0.16-0.32 m over a 1.28 s fall from 8 m. WEDGE CONSTRUCTION: Dia5.0 chamfer-nested fragment +1.80 proud, Dia6.0 +2.95, Dia7.0 +4.08 (nose catches only >=3.00); 3.00-4.50 mm chip under a D13 does the same; defeated by ramp crush (20.7 mm2 x 0.36 MPa = 7.5 N vs 14.1 N normal / 23.4 N recovery = 1.9x / 3.1x), not by rejection. AGITATION DUTY: 18.8% of the window per index, any location swept once per 5.33 indexes = 2.67 pellets. MESH: 15/16 assembly bodies watertight; meter_housing has 1 non-manifold (4-face) edge at r32.50, theta=310.0, z=-274.20.

### buildability — score 4 — FAIL

**Issues**

- BLOCKING - no torque path from the gearbox to the pocket disc. In /Users/hex/projects/payload-systems/payloads/capsule-dispenser/cad/dispenser.py:841 the disc bore is a plain Cylinder(MOTOR_SHAFT_R+0.05) - I measured the exported pocket_disc_r6.stl bore radius at 36 angles x 2 heights: 3.06 mm at EVERY angle (z=-295, -292). There is no D-flat pocket, so the vendor's 12 mm D-cut (the thing BUILD-NOTES-r6 credits with carrying 0.65 N*m) transmits nothing on a 0.12 mm-clearance round bore. The only remaining feature, the grub screw at dispenser.py:847, is a BURIED BLIND HOLE: radial rays at theta=265..275 deg, z=-287.2..-288.7 show void only out to r=10.60 mm and then SOLID disc material from 10.60 to 24.47 mm. No opening to the disc rim exists, so the screw cannot be inserted or driven. The builder's own self-check (dispenser.py:1944 hole_ss) probes only x=3..10 mm, i.e. inside the buried section - it is structurally the same can't-fail probe the r5 critic flagged for the clip plate.
- BLOCKING - the actuator mounting pattern does not match the vendor drawing. dispenser.py:337/971 assume a 26 mm SQUARE M3 pattern (MOTOR_SCREW_HALF=13, holes at (+/-13,+/-13)); measured on retaining_plate_chute_r6.stl at z=-302 the 4 holes sit at theta=45/135/225/315 deg, r=16.8..19.9 (centres r=18.38). The 14HS13-0804S-PG5 datasheet drawing (skysmotor/StepperOnline PDF, front view) dimensions the output flange as 35x35 REF with '4-M3' on a 'D26+/-0.15' BOLT CIRCLE, i.e. 4 holes at r=13.0 on the axes. The gearbox cannot be bolted to the retaining plate as exported, and the correction is not a parameter tweak: holes at r=13 (edge r=11.4 for a D3.2 clearance hole) collide with the measured D22.20 pilot bore (edge r=11.10), leaving a 0.3 mm web, and the D30/D24 PTFE thrust washer seat (r11.1..15.3) would lose its inner land. MOTOR_PILOT_R=11.0 (D22) is also an unverified assumption not listed in the open-issues section.
- MAJOR - the 4 mount screws that carry the entire payload get 0.90 mm of thread engagement. Measured on the vendor STEP (2112_attach_plate_payload_side.step, placed as the model places it): the mount hole at (19,19) is D2.96 through the solid slab z=-181.5..-177.4 (4.10 mm) and opens to a D3.96 head counterbore from -177.4 up to the mating plane -171.0, so the M2 socket head bears at z=-177.4. Measured on top_plate_r6.stl, the boss bore at (19,19) runs -186.6..-190.6 (Ruthex RX-M2x4 correct at D3.2 x 4.0, boss OD 7.70). Grip length head-face to insert top = 4.10 + 5.00 = 9.10 mm, so the BOM's 'M2x10 SHCS' reaches only 0.90 mm into the 4.0 mm insert (~2 threads at 0.4 mm pitch). M2x14 is needed (the bore is through, so it fits). BOM.md line 46 and the fastener table both specify M2x10.
- MODERATE - the specified heat-set inserts do not fit their bosses. dispenser.py:667 cuts the hopper-flange insert holes as Cylinder(2.0, 4.4); measured on hopper_r6.stl the hole is blind from the flange top z=-186.50 to material at z=-190.69, i.e. 4.19 mm deep, while cad/BOM.md specifies 6x 'Ruthex RX-M3x5.7' (5.7 mm long, the only M3 length Ruthex catalogues). The insert stands 1.5 mm proud, or the flange must thicken. Same check for the M2 inserts passes (4.0 mm bore, RX-M2x4).
- MODERATE - the detent spring plunger has no thread. BOM.md specifies an 'M5x0.8 ball-nose, LIGHT spring, 2.5 N' plunger, and its 96.5 mN*m release torque is 51% of the 190.7 mN*m load budget. dispenser.py:747 bores it as Cylinder(2.6, 24); measured on meter_housing_r6.stl at x=-56 the bore is D5.10-5.20 (open y -2.55..+2.55 at z=-291.25..-292.0) - a clearance hole for M5, and too large to thread-form M5 (needs ~D4.2-4.6). No nut, insert or tapping note appears in the BOM or build notes, so the plunger has nothing to screw into and no way to set its depth.
- MINOR/MODERATE - sleeve-bearing fit is a slip fit with no retention. Measured on meter_housing_r6.stl the seat bore is D23.100 (z=-276.2..-282.2) against the igus JFM-2023-07 OD of 23.00 (ID20/OD23/L7 and flange D30 both confirmed on the TME listing, so the 'flange D30 ASSUMPTION' is actually right). igus specifies an H7 housing bore press fit; +0.05 mm/side nominal is a clearance fit and nothing (adhesive, anti-rotation flat, retaining lip from below) is modelled or specified. Related unaddressed spec: the journal is a printed CF-PETG hub (measured D19.70) running in the iglidur bore - the checks compute surface pressure (0.021 MPa) but never the shaft roughness/hardness igus requires.
- MINOR - BOM internal contradiction on the disc-to-shaft grub: BOM.md COTS table says 'M2.5x4 hex socket cup-point grub (disc->shaft)', the fastener table says '1 | M3x4 cup-point grub | disc hub -> gearbox shaft D-flat', dispenser.py:847 models a D2.6 pilot and the console text at dispenser.py:2254 says M2.5. Three sizes for one fastener on the joint that is already unbuildable.
- MINOR - claim/measurement mismatch on mesh integrity. BUILD-NOTES-r6.md line 216 claims '10/10 part STLs watertight; assembly STL 16 bodies, 16 watertight'. The builder's own cad/verify_exports.py, re-run by me just now, prints 'meter_housing ... STL watertight=False' and 'assembly STL bodies=16 watertight=15/16'. Independently: meter_housing_r6.stl has 1 non-manifold/boundary edge out of 13469 (euler -9). Not a print blocker (slicers repair it) but the build notes state the opposite of the tool they cite.
- MINOR - vendor data cited as VERIFIED disagrees with the vendor drawing. BOM.md line 24 lists '0.14 N*m, 1.0 A/ph, backlash <=3 deg, max 3 N*m, gross 0.38 kg' as VERIFIED; the 14HS13-0804S-PG5 datasheet PDF gives 0.18 N*m holding w/o gearbox, 0.80 A/phase, backlash <=1 deg, max permissible 2.00 N*m, weight 0.40 kg (oyostepper lists 290 g, gearbox 28.2 vs the modelled 29.2 mm). The torque figure used is the conservative one so no margin is overstated, but the 310 g NET mass assumption now sits below every published figure (0.38-0.40 kg) and 'VERIFIED' is too strong.
- NOTE (honest, not a defect) - service limits are disclosed rather than solved: on-aircraft refill is impossible (measured fill-cap wing bar stands 3.10 mm proud of the top plate at z=-178.40 with only 7.4 mm to the drone belly, and the cap needs 58 mm of lateral travel in a 10.5 mm gap), so every refill means quick-releasing a ~1.09 kg empty payload; and with no isolation gate, dropping the cartridge for a jam spills the sump residue (their own measured 115 cm3 ~ 51 herbicide pellets, dispenser.py:1806-1811). Both are stated plainly in the build notes, which is the right call - but the shipped package (README.md, docs/, electronics/, sim/) still does not exist, so there is no written service procedure or tool list for any of it.

**Numbers**

MEASURED INDEPENDENTLY ON THE r6 EXPORTS (venv dock-cad-314, trimesh 5.0 + scipy EDT; scripts in /tmp/critic_build_r6/):

PRINTABILITY (reproduces the builder's claims exactly - this part is solid):
- support-needing area in the BOM's chosen orientation (45 deg, off-bed): top_plate 3.7% / fill_cap 4.0 / hopper 0.9 / meter_housing 7.5 / pocket_disc 3.0 / agitator 8.9 / brush_holder 6.2 / retaining_plate_chute 2.4 / electronics_bay 7.6 / bay_lid 0.0 - identical to BOM.md to 0.1%.
- support trapped under material (my added check): electronics_bay 1011 of 1161 mm2 (inside the bay, reachable through the 42x36 lid opening), retaining_plate_chute 330 of 688, others <=76 mm2. No unreachable support found.
- local (medial-axis) thickness, 0.4 mm voxels, volume-weighted - a stricter metric than the builder's ray-cast: p1 / % of volume under 2.0 mm: top_plate 2.40 / 0.6% - hopper 2.39 / 0.9% - meter_housing 2.80 / 0.5% - pocket_disc 3.12 / 0.4% - retaining_plate_chute 1.25 / 1.1% - electronics_bay 1.37 / 1.4% - bay_lid 2.40 / 0.2% - fill_cap 1.60 / 1.6% - agitator (TPU) 1.59 / 6.8% - brush_holder 0.70 / 13.1% (the disclosed 30 deg wedge). The >=2 mm structural rule holds everywhere except the disclosed wedge and the TPU agitator fingers.
- all 10 parts fit 220x220x250 (largest sorted extents 150.0 x 150.0 x 95.7, hopper).
- meshes: 10/10 STEPs re-import as 1 solid; 9/10 STLs watertight (meter_housing 1 boundary edge).

FASTENER / COTS FITS (the failures):
- clip-plate vendor STEP: mount hole D2.96 through slab z -181.5..-177.4 (4.10 mm), head counterbore D3.96 from -177.4 to -171.0. Top plate: insert bore D3.2 at -186.6..-190.6, boss OD 7.70. Grip 9.10 mm vs M2x10 -> 0.90 mm engagement (needs M2x14).
- hopper flange insert hole: blind, -186.50..-190.69 = 4.19 mm vs RX-M3x5.7 (5.7 mm).
- detent plunger bore: D5.10-5.20 (clearance, unthreadable for M5).
- bearing seat D23.100 vs igus OD 23.00 (slip fit); hub journal D19.70 vs ID 20.
- disc shaft bore: r=3.06 at all 36 angles, both heights -> no D-flat. Set-screw void ends at r=10.60 with solid material 10.60..24.47 -> uninstallable.
- retaining plate motor holes: theta 45/135/225/315, r 16.8..19.9 (26 mm square) vs the datasheet's 4-M3 on D26+/-0.15 bolt circle (r=13 on the axes). Pilot bore D22.20 (assumed).
- disc body thickness re-measured 13.95 mm (DISC_T 14 OK); park/port and pellet-transit probes in verify_exports.py all re-ran clean (0.000 mm3, 11/11 stations).

VERIFIED COTS PART NUMBERS (real, checked against vendor/distributor pages): StepperOnline 14HS13-0804S-PG5 (5.18:1, 35x35, D6x18 D-cut 12 mm) - real; igus JFM-2023-07 ID20/OD23/L7, flange D30 - real and catalogued at TME/RS; Ruthex RX-M2x4 matches the modelled D3.2x4.0 bore. The part numbers are fine; the interface geometry hung off them is not.

### mass-budget — score 8 — PASS

**Issues**

- MODERATE (measurement error, non-blocking): the slicer-realistic infill bracket in cad/dispenser.py (~line 2331, `dist = (ndimage.distance_transform_edt(mat) - 0.5) * pitch`) runs the distance transform on an UNPADDED voxel matrix. trimesh's matrix is tightly bounded, so faces coincident with the array edge have no zero voxels outside them and EDT treats them as interior -> the hollow core is overstated and sliced mass understated. Re-running with np.pad(mat,4): printed parts go from the claimed 334.0 g to 383.4 g at the same 4-wall/25%-infill assumption (15% low, 49 g). Worst offenders: bay_lid, a 3.2 mm flat plate, is reported 83% hollow core (impossible with 1.6 mm walls both sides) - 2.7 g claimed vs 6.7 g corrected; top_plate 44.1 -> 60.8 g; retaining_plate_chute 33.7 -> 40.3 g. Downstream, BUILD-NOTES-r6 §4's 'LOADED @250 would be 1203.3 g' is really ~1258 g, and §5's '~398 pellets on the measured-infill ledger' is really ~358. NOT blocking: the shipped ledger headlines the conservative 100%-infill number and the MAX fill rib is the volumetric brim line, so no shipped decision depends on the wrong figure - but it is a wrong measured number, not a modelling choice, and the same code is the basis for any future 'we can afford it, it slices lighter' argument.
- MINOR (largest single-point risk): the geared stepper's 310 g is 31% of the empty mass and 35% of the printed+COTS hardware, and it is an ASSUMPTION. I checked the vendor page independently - StepperOnline publishes only 0.38 kg GROSS for 14HS13-0804S-PG5; there is no net figure. The 70 g delta is 70% of the entire 99 g contingency. It still passes at every infill (380 g + 25% infill = 1334.5 g; 380 g + solid = 1472.8 g), so it is not blocking, but the ledger should carry 350 g until the part is on a scale, and 'weigh the motor' belongs in the r7 bench list next to the caliper survey.
- MINOR (density at the low end): 9 of the 10 printed parts are priced at CF-PETG 1.25 g/cm3. Published PETG and CF-PETG figures cluster at 1.27-1.31. Rebuilt at the directed 1.27 the printed solids go 501.4 -> 509.1 g and LOADED@250 (solid basis) 1387.4 -> 1395.8 g. The 1.31 sensitivity is already run and passes, so this is a reporting nit, but the headline number is quoted off the low-end density.
- NOTE (claim vs. tool output, hand to the buildability critic): BUILD-NOTES-r6 §4 states '10/10 part STLs watertight; assembly STL 16 bodies, 16 watertight'. I ran the builder's own cad/verify_exports.py and it prints 'meter_housing ... STL watertight=False' and 'assembly STL bodies=16 watertight=15/16'. I confirm independently: meter_housing_r6.stl has 0 open edges but non-manifold edges (euler -9). Mass impact is nil (STL integrates to 102.245 cm3 vs the STEP's 102.28, 0.03%), so the ledger is unaffected - but the notes assert the opposite of their own verifier's output, and a non-manifold STL is a slicing risk for the largest printed part.
- NIT: two small un-ledgered/mis-transcribed items. (a) Open issue 1's fix - standoffs on the vendor tabs to resolve the blind-mate pad plane - adds ~4 standoffs plus longer screws (~3-6 g) that appear nowhere in the ledger; inside contingency, but it is a known-coming mass. (b) The §'Over-1.0 kg justification' prose sums 310.0 + 46.2 + 16.5 + 15.2 = 387.9 g and states 387.4 g; the code partitions correctly with min(m, remaining), the prose transcribed the truncated last take. Cosmetic.
- FRAMING NOTE (not a misstatement): the printed 'ESTIMATE EXPOSURE: 150.5 g, 15.2%' excludes the stepper by construction (it is disclosed separately). The honest total not derived from modelled geometry is 150.5 + 310 = 460.5 g, i.e. 46% of the 1000.7 g empty subtotal. Fine given a 215-243 g margin at realistic infill, but the 15.2% figure reads friendlier than the real exposure.

**Numbers**

REBUILT LEDGER (my own measurement, not the builder's claims). Volumes read from cad/exports/*_r6.stl with trimesh, densities PETG/CF-PETG 1.27, TPU 1.20 g/cm3; clip plate from the vendor STEP (11.523 cm3 x 2.70 = 31.1 g).

Printed solids measured (cm3): top_plate 61.25, fill_cap 12.10, hopper 89.23, meter_housing 102.25, pocket_disc 70.43, agitator 4.29, brush_holder 2.51, retaining_plate_chute 37.74, electronics_bay 15.62, bay_lid 5.67 = 401.08 cm3 total (builder claims 401.1 - agrees to 0.03%).

Printed mass: 509.1 g if solid; 408.5 g at 4 walls + 40% infill; 383.4 g at 4 walls + 25% infill (my padded-EDT voxel erosion at 0.5 mm pitch).

Non-printed (491.6 g): clip plate 31.1 (measured from vendor STEP), geared stepper 310.0 (ASSUMPTION, vendor publishes 0.38 kg gross only), electronics+wiring 65.0 (est), fasteners/inserts/plunger 57.0 (est), blind-mate PCB 15.0 (est), O-ring+gaskets+9 magnets 8.0 (est), brush bristles 3.0 (est), igus JFM-2023-07 bushing 1.7, PTFE washer 0.8.

Pellets: 250 x 1.18 g = 295.0 g (CONTEXT-verified).

TOTAL AT THE 250-PELLET LOAD, realistic infill (the directed basis):
  empty 875.0 g -> 962.5 g carried (+10% CAD contingency) -> LOADED@250 = 1257.5 g @25% infill / 1285.1 g @40% infill.
  => STATE THE TOTAL: ~1.26-1.29 kg, 215-243 g under the 1.5 kg ceiling.
  If every printed part were solid (builder's shipped headline basis): 1395.8 g at 1.27 (builder prints 1387.4 at 1.25) - still 104 g clear.

Over-1.0 kg justification at realistic infill: 257.5 g over. Attributable blocks: geared stepper 310.0 g (buys 20.4 N at the pocket lip vs 5.6 N direct-drive - this is what makes CONTEXT jam-requirement #2 achievable) alone exceeds the overage; plus COTS clip plate 31.1 g (interface hardware, not ours to trade), electronics+PCB 80 g (CAN node/driver/buck/IR count sensor = the "verified count" requirement), fasteners+seals 65 g. Nothing unattributed; every 100 g block is spoken for.

Full-load statement: brim 422 pellets = 498 g -> 1460.5 g (25% infill) / 1598.8 g (solid). Pellets above the 250 baseline are ceiling-exempt per CONTEXT; sane against the 5-8 kg platform budget.

Ceiling robustness - no variant I could construct breaks it: stepper at the published 380 g gross + realistic infill = 1334.5 g; 380 g + 100% infill = 1472.8 g; quadruple-conservative (380 g + solid + CF-PETG 1.31) = 1490.2 g, 10 g under.

Cross-checks: builder's own verify_exports.py re-run by me -> printed parts 501.5 g at ledger densities (matches BOM 501.4); analytic usable volume 950 cm3 -> 417 pellets vs the model's 963 cm3 -> 422 (1.2% spread, both >>250).
