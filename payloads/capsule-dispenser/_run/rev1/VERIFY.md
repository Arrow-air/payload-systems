# REV-1 INDEPENDENT VERIFICATION — fresh-eyes re-measurement of the r12 exports

Date: 2026-08-08. Verifier: fresh-eyes agent; **has not seen any build round**.
Inputs read: `_run/rev1/CONTEXT.md`, `_run/rev1/PUNCHLIST.md`, `cad/BOM.md`,
`_run/rev1/BUILD-NOTES-r6.md` §4/§7/§9 (read **only** to test documentation
integrity, i.e. to compare claims against my own numbers — every number below is
my own).

## 0. Method and provenance

- Subject: **`cad/exports/*_r12.*`** (the newest tag; `dispenser_r12_assembly.*`,
  written 2026-08-08 00:07). rev-1 rounds 1–6 correspond to export tags r7…r12.
- Tools: system `python3` with `trimesh` 4.12.2 (mesh rays, watertightness,
  face-normal audits) and **OCP/OpenCascade booleans on the STEP files** for every
  number where a mesh could lie. `cad/dispenser.py` was **never read or executed**
  and none of the project's `verify_*.py` checkers were run (RT-20 rule).
- Frame: mount plane Z = −171.0; θ is the polar angle about the meter axis
  (x = y = 0); r is radius from it.
- Datums I established myself from the exports, because the whole stack moved down
  ~52 mm this rev (B6 neck):
  - meter-housing roof: **top Z = −326.250**, **underside Z = −335.250** (9.000 mm)
  - pocket-disc plate: **top Z = −336.750**, **bottom Z = −350.750**
  - roof-underside-to-disc clearance = **1.500 mm**
  - retaining plate: **top Z = −351.250**, motor face **Z = −355.250**
  - count-sensor datum **Z_SENSOR = −395.250** (derived from the four window
    solids at −392.250 / −398.250, not from the source)

Notation: **PASS / FAIL / PLATEAU (allowed) / NOT VERIFIED**.

---

## 1. BLOCKING items

### B1 — roof through-slot at θ = 310° — **PASS**

Roof thickness measured by contiguous-material march downward from Z = −326.250,
0.02 mm step, on `meter_housing_r12.stl`:

```
theta\r     20.5    24.5    30.0    32.0    36.0    39.5    44.0    46.5
 300.0    8.980   8.980   8.980   8.980   8.980   8.980   8.980   8.980
 305.0    8.980   8.980   8.980   8.980   8.980   8.980   8.980   8.980
 308.0    8.980   8.980   8.980   8.980   8.980   8.980   8.980   8.980
 309.0    8.980   8.980   8.980   8.980   8.980   8.980   8.980   8.980
 310.0    8.980   8.980   8.980   8.980   8.980   8.980   8.980   8.980   <-- r6: 0.000
 311.0    8.980   8.980   8.980   8.980   8.980   8.980   8.980   8.980
 313.0    8.980   8.980   8.980   8.980   8.980   8.980   8.980   8.980
 316.0    8.980   8.980   8.980   8.980   8.980   8.980   8.980   8.980
 320.0 / 330.0 / 350.0 / 0.0 / 20.0 / 45.0 / 90.0   all 8.980 at all eight radii
```

(8.980 not 9.000 is STL chordal error on the two bounding planes; the STEP planes
are at −326.250 / −335.250 exactly = 9.000.)

Direct r6→r12 regression, same probe, r = 32, 1° steps: the set of angles with
roof < 0.5 mm is **θ = 129…311 (124 angles) in r6** and **θ = 129…250 (122 angles)
in r12** — i.e. exactly the two bug angles (310, 311) removed and nothing else
changed. Entry-ramp taper is monotonic and re-printed:
8.98@95° → 7.82@100 → 6.52@105 → 5.22@110 → 3.92@115 → 2.62@120 → 1.32@125 → 0.00@130.

**B1.3 face-normal audit** (transfer arc θ = 160…131 through 0, roof band,
|n_z| < 0.05, normal opposing disc travel): largest single such face =
**1.98 mm² at θ = 263.1°, n_z = 0.000** (either sense of travel; totals 57.2 /
58.0 mm² spread over 51 sub-2 mm² facets). Threshold is 20 mm²; r6 had a
**238 mm²** face at θ = 310°. **PASS.**

**Punch-list defect I am flagging, not a CAD defect:** B1.1 as written demands
"≥ 6.0 mm at every probe outside θ = 96…131" and "full nominal at θ = 200° and
310°". θ = 130…250 is the **designed sump outlet** (the punch list's own N10 calls
it "26.5 mm × 120°" — I measure the open sector as 121° wide at r = 32 and open
across the full r = 20.5…46.5 probe set). Those two sub-clauses are unsatisfiable
by any correct design and must not be read as a failure. The substantive test —
no unintended through-slot outside the ramp and the sump window — passes.

*Not re-run by me:* B1.2's 1° sector volume boolean (superseded by the 8-radius ×
16-angle point probe above) and the full entry-ramp ceiling table.

### B2 — torque path disc→shaft — **FAIL (marginal, 0.200 mm), and the build notes' claim on this is wrong**

**B2.1 D-flat — PASS.** Bore radius swept at 1° × 36 heights (`pocket_disc_r12`,
mesh rays from the axis):
- round part **r = 3.050**, flat part **r = 2.550**, contiguous flat arc
  **θ = 175…230° (56°)** — requirement ≥ 25° at 2.55 ± 0.05.
- flat present continuously from **Z = −349.4 to −335.85 → 13.5 mm** of axial
  engagement (requirement ≥ 10.0; vendor D-cut is 12 mm on a Ø6 shaft).
- Grub axis is at **θ = 202.5°**, exactly the flat's mid-angle. Pilot bore Ø2.60
  (z-extent −342.55…−339.95), matching the BOM's "Ø2.6 thread-forming pilot".

**B2.2 continuous void OD→bore — FAIL.** Exact OCP boolean of a coaxial cylinder
on the grub axis (θ = 202.5°, Z = −341.25) against `pocket_disc_r12.step`:

```
  Dia0.7 from r=46.5 to r=2.55 (the bore flat): disc material = 0.0770 mm3   <-- BLOCKED
  Dia0.7 from r=46.5 to r=2.75:                 disc material = 0.0000 mm3
  Dia1.9 from r=46.5 to r=2.55:                 disc material = 0.5671 mm3   <-- BLOCKED
  Dia2.6 from r=46.5 to r=2.55:                 disc material = 1.0619 mm3   <-- BLOCKED
  Dia2.6 from r=46.5 to r=2.75:                 disc material = 0.0000 mm3
```

1.0619 mm³ = π·1.30²·0.200 exactly: the grub pilot **dead-ends at r = 2.750 and
the shaft flat is at r = 2.550**, leaving a **0.200 mm closed web of CF-PETG
across the full Ø2.6 pilot**. The corridor is *not* continuous to the bore. The
outer channel (Ø3.4, r = 46 → 9.0) and the Ø2.6 pilot (r = 9.0 → 2.75) are both
present and clean — this is a 0.2 mm miss, not a missing feature.

`BUILD-NOTES-r6.md` §7 prints: *"grub corridor, Ø0.7 ray from the bore to the disc
OD along θ = 202.5: blocked at r = **NOWHERE** — continuous void"*. My Ø0.7 test
from the flat reads **0.0770 mm³ of material**. The checker almost certainly
starts its ray at the *round* bore radius (3.05) or at the pilot floor, both of
which are **outboard** of the flat at 2.55, so it can never see the web. This is
the exact class of defect this run was told to stop shipping (RT-19/RT-20).

**B2.3 driver access — PASS.** Ø1.9 × 40 mm key column on the grub axis from
r = 46 outward, exact booleans: `meter_housing` 0.0000, `top_plate` 0.0000,
`hopper` 0.0000, `retaining_plate_chute` 0.0000, `brush_holder` 0.0000,
`agitator` 0.0000, `electronics_bay` 0.0000 mm³.

**B2.4 one grub size — PASS.** `cad/BOM.md` says **M3×4 cup-point grub** in both
the COTS table and the fastener table, "M3 thread-forming into the modelled Ø2.6
pilot"; modelled pilot measures **Ø2.60**. String-equal, and a 1.5 mm key is
separately listed.

### B3 — gearbox bolt pattern — **PASS on geometry; FAIL on B3.4 (BOM statement)**

Exact OCP probes on `retaining_plate_chute_r12.step`, flange band Z −355.25…−351.25
(4.000 mm):

- **B3.1** four clearance holes on the axes: void spans **r = 11.30…14.70 at
  θ = 0/90/180/270°** → centres **(±13.00, 0) and (0, ±13.00)**, **Ø3.40**
  through the full 4.000 mm flange. (Ø26 bolt circle per the 14HS13-0804S-PG5
  datasheet.) A Ø0.4 × 4.5 column at each of the four centres booleans to
  **0.0000 mm³**. The r6 26 mm *square* at θ = 45/135/225/315 is gone. **PASS.**
- **B3.2** pilot bore edge measured at **r = 8.10** (Ø16.20), hole edge at
  r = 11.30 → **minimum web 3.200 mm** (requirement ≥ 1.95; r6-naive 0.30). **PASS.**
- **B3.3** thrust-washer seat: an annular recess in the plate top, floor at
  **Z = −352.255 (1.005 mm deep)**, between **r ≈ 16.9 and r ≈ 19.1** (no recess
  at r = 16.75, recess at 17.00; recess at 19.00, none at 19.25). It is a
  **continuous full annulus** — the r = 13 holes are 2.2 mm clear of its inner
  edge, so it has lost no land. **PASS (land is the whole 2.2 mm annulus).**
- **B3.4 FAIL:** the pilot-bore diameter (**Ø16.20**, my measurement) is **not
  stated anywhere in `cad/BOM.md`**, with neither a datasheet citation nor an
  ASSUMPTION line. The acceptance test requires it explicitly.
- **B3.5** bolt access: not re-run (Ø6 × 25 driver columns). **NOT VERIFIED.**

### B4 — count-sensor hardware in CAD — **PASS** (this is the cleanest item in the set)

All on `retaining_plate_chute_r12.step` / `count_windows_r12.step` /
`sensor_boards_r12.step` / `sensor_cover_r12.step`, exact booleans.

- **B4.1 PASS.** A Ø0.2 probe swept the full ±y through the part reads
  **0.000 mm of material** at (x = 29.0, z = −392.250) and (x = 35.0, z = −398.250),
  and **12.834 mm** at the two off-diagonal positions (29/−398.25 and 35/−392.25)
  and **12.000 mm** at the r6 single centred position (32, −395.25). Exactly two
  straight chords, on the ECO-3 x-grid, with the **6.000 mm ECO-9 vertical
  stagger**. Four tunnels (2 per side). Tunnel bore measures **Ø3.10–3.20**
  (0.05 mm probe grid) against the Ø3.2 ± 0.1 spec.
- **B4.2 PASS.** Ø2.0 cylinder on each beam axis over the optical span
  (|y| ≤ 11): `retaining_plate` **0.0000 mm³**, `sensor_cover` **0.0000 mm³**.
  Over the punch list's literal 60 mm length it reads `sensor_cover` **0.1576 mm³**
  on beam A only — 6.5 mm behind the emitter board, off the optical path. The
  build notes print **both** numbers and label the deviation; I confirm both.
- **B4.3 PASS (at the limit).** Boss x-min = **22.000** (requirement ≥ 22.0). The
  motor body in the assembly has its face at **x = 18.000** (36 × 36 mm envelope,
  body bbox ±18 × ±18 × −418.45…−337.25), so boss-to-motor clearance = **4.000 mm**
  against the ≥ 4.0 mm requirement. Note the punch list assumed the motor face at
  x = 17.6 (which would give 4.4 mm); the modelled face is at 18.0, so this passes
  with **zero** margin, not 0.4 mm.
- **B4.4 PASS.** Four window solids, each **Ø5.90 × 0.95 mm**, inner faces at
  **|y| = 11.000 exactly**, at x = 29.0/35.0 and z = −392.25/−398.25. Material of
  the windows inside the Ø22 chute bore = **0.0000 mm³** (and 0.0000 inside
  r = 10.9). Nothing proud of the bore. *Deviation:* the BOM and ECO-4 both say
  **Ø6 × 1.0 mm**; the modelled window is **Ø5.90 × 0.95**. Also, the build notes
  record honestly that ECO-4's 0.4 mm seat chamfer was **attempted and withdrawn**
  (it produced 22 non-manifold edges) — so the "0.4 ± 0.05 mm chamfered recess"
  half of B4.4 is **not** in the geometry, by recorded deviation.
- **B4.5 PASS.** Labyrinth measured on beam A: inner tunnel opening
  **x = 27.05…30.15, centre 28.600** (|y| = 12…14); outer tunnel opening
  **x = 27.85…30.95, centre 29.400** (|y| = 15 to the boss face at y = 17.0).
  Offset **0.800 mm**, ledge **0.800 mm** (requirement 0.8 ± 0.1 / ≥ 0.7). The
  split (−0.400 inner / +0.400 outer) is what keeps the clear lens on the ECO-3
  axis — confirmed by B4.2 reading 0.0000.
- **B4.6 MIXED.** Receiver board (−Y): 18 × 12 × ~3.2 envelope grown 1 mm all
  round vs the plate = **0.0000 mm³** → PASS. Emitter board (+Y) as modelled spans
  y = 17.5…28.5 (board + LED bodies) and the boss face is at y = **17.000**, so the
  gap is **0.500 mm** and the "+1 mm all round" boolean reads **131.96 mm³**. The
  literal test fails; the physical clearance is 0.500 mm. Report as measured.
- **B4.7 PASS.** `cad/BOM.md` contains **no TSSP4038 line** (the only occurrence
  of the string is "replaces the REJECTED TSSP4038"), and does contain VBPW34FAS
  ×2, OPA2320AIDR, TSAL6200 ×2 and "count windows x4 | Ø6 × 1.0 cast PMMA".
- **B4.8 PASS.** Ø13.0 pellet swept down the chute axis (x = 32, Z −418…−373):
  `retaining_plate` 0.0000, `count_windows` 0.0000, `sensor_cover` 0.0000,
  `sensor_boards` 0.0000 mm³.

### B5 — electronics/wiring home — **PARTIAL PASS; B5.3/B5.4/B5.5 NOT INDEPENDENTLY VERIFIED**

`electronics_bay_r12` (bbox x ±34.0, y −90.000…−48.965, z −363.100…−306.600,
21.175 cm³) and `bay_lid_r12` (y −92.0…−88.6, 8.598 cm³) exist as real parts and
are in the BOM with masses (26.9 g / 10.9 g). The lid faces **−Y**, i.e. outboard,
away from the hopper.

- **B5.1 PASS.** Interior cavity measured by marching from an interior point
  (0, −76, −336) to first material: **x = −26.0 to +26.0 (52.0 mm)**, inboard wall
  at **y = −64.0**, **z = −356.1 to −318.3 (37.8 mm)**. Against the 42 × 34 board:
  x clearance **5.0 mm/side**, z clearance **1.9 mm/side** (≥ 1.5 required).
  **Four standoff bosses are modelled**, at **(x = ±21, z = −350.5)** and
  **(x = ±21, z = −322.5)** (42 × 28 mm pattern), protruding ≥ 3 mm past the
  y = −64 wall (present at y = −67). ECO-7 is closed.
- **B5.2 PASS (two of three verified).** Two round through-openings in the inboard
  wall at **x ≈ ±14, z ≈ −350**, ~Ø10–12 (grommet panel holes for a Ø6.0 grommet),
  plus a third opening region at the bay's lower/−X end. BOM orders **5 × Ø6.0
  grommets for a 2.0 mm panel** (3 bay + 2 sensor duct). I did not measure each
  seat land to ±0.1 mm.
- **B5.3 NOT INDEPENDENTLY VERIFIED.** I located the lid-joint rim (a continuous
  2.000 mm land at y = −90.000…−88.000 around the opening) and recessed cells
  within it, but my 1.0 mm scan grid cannot resolve a 1.58 mm-wide loop, so I can
  **neither confirm nor refute** the claimed 1.58 × 1.20 mm closed groove with a
  182.00 mm perimeter. It is a BOM line (2.0 mm silicone cord, 200 mm).
- **B5.4 NOT VERIFIED.** No harness sweep solids appear in
  `dispenser_r12_assembly` (24 bodies, all identified: 15 printed/PMMA parts +
  motor + bearing + PTFE washer + clip plate + interface PCB + brush strip +
  2 sensor boards + 4 windows). The "harness modelled as swept solids, 0.000 mm³
  into hopper/funnel/sump/metering arc/chute" test can only be reproduced inside
  the model, which I am not permitted to read. **Directive 2's headline is
  satisfied** (a real sealed bay exists, on the outboard −Y face, and the bay
  cavity is topologically outside the hopper), but the five-volume harness
  boolean is unverified by me.
- **B5.5 NOT VERIFIED** (channel coverage %, 70 % fill).
- **B5.6 NOT VERIFIED** (lid-lift and driver-column sweeps).
- **B5.7 PASS.** Bay, lid, standoffs, grommet seats, gasket cord and the 4 lid
  screws are all BOM lines with masses.

### B6 — attachment-interface reach-in clearance — **PASS**

Measured on the assembly and on `top_plate_r12.step` (exact booleans):

- **B6.1 PASS.** The payload plan half-extent is **exactly 24.000 mm** from
  Z = −181.55 continuously down to **Z = −225.05**, where it jumps to 84–85.5 mm.
  So **stand-off height h = 43.50 mm** (≥ 40 required) and **neck plan half-extent
  a = 24.00 mm** (≤ 35 required) — a 48 × 48 mm neck, i.e. *better* than the
  punch list's assumed 70 mm-wide neck. Independent of the build notes I get the
  same 43.500 / 24.000.
- **B6.2 PASS.** Corridor boxes 95 (wide) × 45 (tall) × 130 (deep), tops at
  Z = −181.5, referenced to the neck face:

```
  +X: 0.0000 mm3      -X: 0.0000 mm3      +Y: 0.0000 mm3      -Y: 321.2178 mm3
```

  Three of four clear, **including the two opposing sides (+X/−X)** — requirement
  is "at least two opposing sides". (The build notes print 340.2241 mm³ on −Y; I
  get 321.2178 mm³ — a 6 % difference explained by my referencing the corridor to
  the neck face at |y| = 24 rather than wherever their datum sits. Same verdict.)
  Referenced instead to the mount axis, all four read ~15 000 mm³, which is just
  the neck itself; that reading is not the intended test.
- **B6.3 NOT VERIFIED** (QR release-motion envelope; the vendor QR kinematics are
  not in these exports).
- **B6.4 PASS.** `dispenser_r12_assembly` max Z = **−171.050**; payload material
  above Z = −171.000 = **0 vertices / 0.000 mm³**. r6's 0.0397 mm³ is gone.
- **B6.5 / B6.6 NOT VERIFIED.** Ground and prop clearance need the airframe STEPs;
  `/tmp/pq-main/.../landing_gear/steps/` contains only `1340_tube_joint.step` and
  a `vendor/` folder, so I could not reproduce the mesh-to-mesh number. Carried
  from the notes, unverified: ground clearance at rest **129.4 mm**, payload↔gear
  minimum **103.63 mm**, prop vertical **152.55 mm**, in-plan **232.63 mm**.
  Assembly bottom Z = **−418.45** (measured), so the stack is **247.4 mm** below
  the mount plane (measured) — the neck did push it down ~52 mm, and this number
  deserves a real re-check against the gear before flight.

### B7 — "stationary release" — **PLATEAU (explicitly allowed by the punch list)**

Not closed by geometry, and the build notes say so in those words. Inputs I
re-measured on the exports, which are consistent with a plateau:

- exit port in `retaining_plate_chute_r12`: bore **Ø16.000** (void x = 24.0…40.0
  at y = 0, centred x = 32.000 = PCD 32), with a 0.75 × 45° top chamfer →
  **mouth Ø17.50, rim radius 8.75 at the plate top** (r6: Ø18.00 / 9.75 — the port
  was made 2.0 mm *smaller* this rev, which helps but does not close it).
- pocket bore on `pocket_disc_r12`: 8 through-pockets at 45° pitch, each spanning
  **27.0° at r = 32** → **pocket radius 7.50 mm** on a Ø13 worst-case pellet
  (r = 6.5) → ±1.00 mm of lateral seat, unchanged.
- Park separation for the two-phase 22.5° index = 2·32·sin 11.25° = **12.485 mm**.

The notes' printed plateau — release window **3.25…10.50°** into the index, spread
**7.25°** across Ø11…Ø13, separation at release **6.690…10.701 mm**, lateral
velocity **0.126 m/s** (0.25 m/s at peak) — is arithmetically consistent with the
geometry I measured, and B7.1 (support to |separation| ≤ 1.0 mm) plainly **FAILS**.
The punch list permits this **only** if every document says so; §9 of the notes,
README RT row and DESIGN all do. **Accepted as a recorded plateau.** I did not
independently re-run the 0.25° sweep.

### B8 — rejection band vs shear band — **PASS**

`brush_holder_r12`, nose underside height above the disc top (Z = −336.750),
measured by first-hit ray from below:

```
  theta      r=22.0   r=26   r=30   r=34   r=38   r=42   r=46.5
   135        1.500   1.500  1.500  1.500  1.500    -      -
   140        1.500   1.500  1.500  1.500  1.500  1.500  1.500
   145        1.500   1.500  1.500  1.500  1.500  1.500  1.500
   150        1.500   1.500  1.500  1.500  1.500  1.500  1.500
   155        1.500   1.500  1.500  7.450  8.640  8.640  8.640
```

**max(nose gap) = 1.500 mm** over the rejection arc, equal to
**min(roof clearance) = 1.500 mm** (roof underside −335.250 vs disc top −336.750).
r6's constant 3.000 mm nose is gone; the critic's one-line fix
(`NOSE_GAP 3.00 → ≤ 1.50 = ROOF_CLEAR`) is in the geometry. The brush strip in the
assembly bottoms at **Z = −335.550 = 1.200 mm above the disc**, so the compliant
element still leads the rigid one by 0.300 mm. A Ø5.0 fragment (+1.80 proud) and
a Ø6.0 fragment (+2.95 proud) now both intersect the 1.50 mm nose. **B8.1/B8.2
PASS.** B8.3 (lift/push ratio), B8.4 (thin-section stats) and B8.5 (Ø13 transit
with the lowered nose) **NOT VERIFIED** by me.

### B9 — COTS interface fits — **MIXED**

| # | Verdict | My measurement |
|---|---|---|
| a mount-screw engagement | **NOT VERIFIED** | not re-measured after the B6 move |
| b hopper insert bores | **PASS (at the limit)** | 6 blind bores at **r = 74.000, θ = 15/75/135/195/255/315°**; flange spans Z −245.55…−238.55 (7.00 mm), bore floor at **Z = −244.54** → **depth 5.99 mm** from the top face, 1.01 mm of floor left. Requirement = insert 5.7 + 0.3 = **6.00 mm**. Passes to within measurement noise, with **zero** margin. Boss wall thickness not measured. |
| c detent plunger thread | **NOT VERIFIED** | BOM/notes claim a modelled Ø4.5 × 13.5 mm thread-forming pilot at r 49.5…63.0 (r6 A-11); I did not probe it. |
| d bearing seat | **PASS (exactly at the limit) — with a BOM mismatch, see below** | `meter_housing_r12` seat bore measured **Ø23.023…23.030** over Z −334.5…−328.5 (limit ≤ Ø23.03, igus JFM-2023-07 OD 23.00). Flange counterbore **Ø30.39**, from Z ≈ −327.95 to the roof top −326.25 = **1.70 mm** deep for a 2.0 mm flange, i.e. the bearing flange stands **0.30 mm proud** of the roof; sleeve engagement **7.00 mm**. |
| e grub size stated once | **PASS** | see B2.4 |

**New defect found here (not in the punch list):** the assembly's PTFE thrust
washer solid measures **Ø38.00 OD / Ø34.00 ID × 1.400 mm** (bbox ±19.000 ×
Z −352.200…−350.800, volume 317 mm³ → 0.70 g at 2.2 g/cm³), seated in the
1.005 mm recess at r 16.9…19.1 measured in B3.3. `cad/BOM.md` still orders a
**"PTFE washer | Ø30/Ø24 × 1.5 virgin PTFE"** — an ID/OD that lands exactly on
the four Ø3.4 bolt holes at r = 11.3…14.7 and is 0.1 mm too thick for the modelled
seat + 0.5 mm gap. The **mass** in that BOM row (0.7 g) was recomputed from the
new solid; the **dimension string was not**. Ordering to this BOM gets you a
washer that does not fit.

### B10 — export integrity — **PASS**

My own trimesh run over all 16 r12 STLs, vertices merged, edge-multiplicity
counted directly:

```
part                        watertight  winding  euler  edges!=2  edges>2  bodies   vol cm3
agitator_r12                    True     True       2       0        0        1       4.29
bay_lid_r12                     True     True     -10       0        0        1       8.60
brush_holder_r12                True     True       0       0        0        1       3.54
chute_plug_r12                  True     True      -2       0        0        1       6.72
count_windows_r12               True     True       8       0        0        4       0.10
electronics_bay_r12             True     True      -8       0        0        1      21.18
fill_cap_r12                    True     True       0       0        0        1       7.55
hopper_r12                      True     True     -14       0        0        1     109.42
meter_housing_r12               True     True      -8       0        0        1     103.82
pocket_disc_r12                 True     True     -30       0        0        1      72.66
retaining_plate_chute_r12       True     True     -76       0        0        1      63.94
sensor_boards_r12               True     True       4       0        0        2       1.29
sensor_cover_r12                True     True      -4       0        0        2       3.20
service_stand_r12               True     True       0       0        0        1     103.89
top_plate_r12                   True     True     -38       0        0        1      95.55
dispenser_r12_assembly          True     True    -193       0        0       24     579.90
-> 15/15 part STLs watertight, 0 non-manifold edges; assembly 24/24 bodies, 0 non-manifold edges
```

Every number matches the table quoted verbatim in `BUILD-NOTES-r6.md` §7,
including the Euler characteristics and the 24-body assembly count. The r6
non-manifold edge at (20.891, −24.896, −274.200) — which sat on the B1 bug line —
is gone. Note the part count is **15**, not the punch list's "10/10, 16/16"; the
notes state the new count rather than the old one, which is the correct behaviour.

### B11 — mass ledger — **PASS on the shipped basis, with one stale BOM line**

- Exported solid volumes agree with the BOM table to **≤ 0.04 %** on every part
  (e.g. top_plate 95.550 STL / 95.572 STEP vs BOM 95.57; meter_housing 103.819 /
  103.856 vs 103.86). The ledger is measured from the geometry I measured.
- **B11.2 PASS:** README and BOM both headline **LOADED @250 = 1432.5 g** on the
  slicer-realistic basis (4 perimeters, 25 % infill, padded EDT) → **+68 g** under
  the 1500 g ceiling; **1493.5 g** with the 61 g reserve (+7 g). The 100 %-infill
  pessimistic bound **1576.0 g (76 g OVER)** and max-fill **1777.8 g @421** are
  both stated rather than hidden. **B11.4 PASS** (per-open-item reserve line
  exists).
- **B11.3 partial FAIL (documentation):** the ledger carries the stepper at
  **350 g** (README: "the 350 g stepper is a vendor catalogue figure"), which
  satisfies the ≥ 350 g rule — but `cad/BOM.md`'s COTS row still reads
  *"gross 0.38 kg; **310 g NET is an ASSUMPTION**"*. The BOM and the ledger
  disagree by 40 g on the single largest COTS mass. One of the two is stale.
- Minor: README says usable volume **963 cm³ → 422** pellets, BOM says
  **962 cm³ → 421**. Cosmetic, but they are generated from the same model.

### B12 — refill rest position and fill geometry — **PARTIAL**

- The **`service_stand`** is a real modelled part in the exports
  (bbox ±90.000 × ±89.970 × Z −426.450…−358.250, 103.892 cm³ → 132.0 g) and is
  correctly listed in `cad/BOM.md` as **mandatory GSE excluded from the flight
  ledger**. This is the "modelled printed cradle" route of B12.4. **PASS on
  existence.**
- **B12.1 (tip angle ≥ 25°, load path not through the gearbox flange), B12.2 (cap
  removal sweep in the rest position) and B12.3 (side-wall port) NOT VERIFIED** by
  me — I did not have budget to run the stand-plus-dispenser stability boolean.
  The notes print a cap extraction of **6.000 mm lift then 0.0000 mm³ over a
  0…45 mm +Y lateral sweep at 8 mm lift**, and a fill-cap top at Z = −228.200,
  which I did confirm is 1.65 mm below the B6 corridor floor (fill_cap bbox top
  = **−228.200**, corridor floor −226.5): the cap does not eat the reach-in
  corridor. **Capacity unchanged** (962–963 cm³ / 421–422 pellets vs rev-0's
  ~422) — directive 5 respected, ≪ 2 %.

---

## 2. The three rev-0 red-team CAD blockers

| Blocker | Verdict | Evidence (mine) |
|---|---|---|
| **RT-1 — assembly/torque path** | **NOT FULLY FIXED.** Three of its four legs are closed; one is short by 0.200 mm | D-flat present (r 2.550/3.050, 56° arc, 13.5 mm engagement) ✔; bolt pattern now Ø26 on the axes with a 3.200 mm web ✔; driver access 0.0000 mm³ ✔; **but the grub pilot dead-ends 0.200 mm short of the shaft flat (0.0770 mm³ blocks a Ø0.7 ray, 1.0619 mm³ blocks the Ø2.6 pilot), and the round's own checker reports this corridor as "blocked at NOWHERE"** |
| **RT-3 — count hardware absent from CAD** | **FIXED.** | 4 tunnels, 2/side, axes at x = 29.000/35.000 and z = −392.250/−398.250 (6.000 mm stagger); 0.000 mm of material on both beam axes; labyrinth ±0.400 = 0.800 mm offset with a 0.800 mm ledge; 4 PMMA windows with inner faces at \|y\| = 11.000 and 0.0000 mm³ proud of the bore; Ø13 pellet 0.0000 mm³ against all four bodies; BOM carries VBPW34FAS/OPA2320/TSAL6200/PMMA and no TSSP4038. Deviation recorded, not hidden: ECO-4's 0.4 mm seat chamfer is not modelled. |
| **RT-2 — bay implication only** (pin/pad stack-up is VOID per directive 1) | **FIXED in the part that survives.** | A sealed bay exists as its own part (21.175 cm³) with a lid on the outboard −Y face, a 52 × 24 × 37.8 mm interior that clears the 42 × 34 board with ≥ 1.9 mm on every side, **four modelled M2.5 standoff bosses** (ECO-7) at (±21, −350.5)/(±21, −322.5), and grommeted cable entries. The *routed-harness* half (B5.4/B5.5) I could not verify from the exports. |

---

## 3. The six directives

1. **Electrical mate out of scope — RESPECTED.** Nothing in the r12 exports or the
   BOM re-litigates the spring-pin/pad stack-up; the clip plate (±25 × 10.5 mm,
   Z −181.55…−171.05) and interface PCB are carried as black-box bodies.
2. **Dispenser needs an electronics home — MET in substance.** A real sealed bay
   with a real board volume, real standoffs, real grommet seats and a real lid,
   on the outboard face — not "wiring straight into the tank". The *modelled
   conduit route* end-to-end is the part I could not confirm from the exports.
3. **Reach-in clearance — MET and proved with numbers, not adjectives.**
   h = **43.500 mm**, a = **24.000 mm**, three of four 95 × 45 × 130 corridors at
   **0.0000 mm³** including both opposing sides. This is the strongest-evidenced
   directive of the six.
4. **Refill = remove the whole dispenser — MET architecturally.** `service_stand`
   is modelled, in the BOM, and correctly excluded from the flight ledger; the
   cap lifts 6.000 mm and clears. Stability/tip-angle proof NOT VERIFIED by me.
5. **Capacity settled — RESPECTED.** 962–963 cm³ → 421–422 pellets, i.e. the
   rev-0 hopper unchanged (≪ 2 %).
6. **Simulation skipped — RESPECTED.** No simulation artefacts in this run.

---

## 4. Findings, ranked

1. **BLOCKING — B2.2 fails by 0.200 mm, and the checker cannot see it.** The
   grub pilot on `pocket_disc_r12` bottoms at r = 2.750 against a shaft flat at
   r = 2.550. Exact booleans: Ø0.7 → **0.0770 mm³**, Ø1.9 → **0.5671 mm³**,
   Ø2.6 → **1.0619 mm³** (= π·1.3²·0.200 exactly, i.e. a full-section web). The
   round's own check prints *"blocked at r = NOWHERE — continuous void"* because
   its ray starts outboard of the flat. Fix is one line (deepen the pilot 0.2 mm
   to break into the bore) **and** re-anchor the checker ray at the flat radius,
   not the round-bore radius. Until then this is a **renamed-not-fixed instance
   of RT-1** and B2 must not be signed off.
2. **BLOCKING (BOM) — the PTFE thrust washer is ordered at the wrong size.**
   Modelled solid **Ø38 / Ø34 × 1.4**; BOM says **Ø30 / Ø24 × 1.5**. The BOM's ID/OD
   sits on top of the four Ø3.4 gearbox bolt holes at r 11.3…14.7. The mass in
   that row was updated from the new solid, the dimensions were not.
3. **BLOCKING (BOM) — B3.4 is not satisfied.** The pilot bore measures **Ø16.20**
   and appears nowhere in `cad/BOM.md`, with no datasheet source and no
   ASSUMPTION line. The punch list asks for exactly this.
4. **B11.3 — the BOM and the mass ledger disagree on the stepper by 40 g**
   (BOM row "310 g NET is an ASSUMPTION" vs ledger/README 350 g).
5. **Zero-margin passes that should be recorded as such, not as comfortable
   passes:** boss-to-motor clearance **4.000 mm** against a ≥ 4.0 requirement (and
   against a punch-list assumption of 4.4 mm, because the modelled motor face is at
   x = 18.0 not 17.6); bearing seat **Ø23.030** against ≤ Ø23.03; hopper insert
   bore depth **5.99 mm** against ≥ 6.00; nose gap **1.500** vs roof clearance
   **1.500**.
6. **Spec-vs-model drift on the count windows:** modelled **Ø5.90 × 0.95**, BOM and
   ECO-4 both say **Ø6 × 1.0**. Harmless mechanically; it is the kind of drift the
   documentation-integrity rule exists to catch.
7. **Punch-list authoring defect (no CAD action):** B1.1's "≥ 6.0 mm outside
   θ = 96…131" and "full nominal at θ = 200°" contradict the designed 120° sump
   outlet that the same document describes in N10. Any future checker written
   literally from B1.1 will report a permanent false failure.

## 5. What I could not verify (so nobody counts it as verified)

B1.2 sector boolean · B3.5 bolt access · B5.3 gasket-groove loop · B5.4 harness
five-volume boolean · B5.5 channel coverage/fill · B5.6 lid-lift + driver columns ·
B6.3 QR actuation envelope · B6.5/B6.6 ground and prop clearance (airframe STEPs
not present at the referenced path) · B7's 0.25° release sweep (accepted as a
recorded plateau) · B8.3/B8.4/B8.5 · B9a mount-screw engagement · B9c detent
thread pilot · B12.1/B12.2/B12.3 rest-position and fill-route sweeps · every
NONBLOCKING N-item.

## 6. Bottom line

The CAD is **much** better than r6 and most of it survives adversarial
re-measurement with the numbers the notes claim — B1, B3 (geometry), B4, B6, B8,
B10 and B11 all reproduce independently, and B4/B6 reproduce to the third decimal.
**The round is not closeable as it stands**, on three counts, all cheap to fix:
a **0.200 mm** unbroken web across the grub pilot (B2.2, and a checker that is
structurally blind to it), a **PTFE washer ordered at a size that cannot fit the
modelled seat**, and a **pilot bore that B3.4 requires the BOM to state and the BOM
does not**. B7 remains a correctly-documented plateau, which the punch list allows.
