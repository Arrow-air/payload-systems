# REV-1 ROUND 3 — CRITIQUES

## granule-path

**Verdict: FAIL — 1 BLOCKER (export integrity on the part that carries the exit
port and chute, a regression from r8), 1 MAJOR (documented B7 release numbers do
not reproduce), 3 MODERATEs. The rev-0 fragment-jam mandate is NOT regressed:**
every geometric term of it (overfill relief before the housing arc, nose gap =
roof clearance, shear-margin backstop, pocket/chamfer geometry) reproduces to
0.001 mm on the r9 exports, and the stall-recovery stroke has full rotational
freedom (0 penetrations at 360/360 angles).

### Provenance

- **`_run/rev1/BUILD-NOTES-r3.md` does not exist** at review time (2026-08-07
  16:2x; the directory holds only `BUILD-NOTES-r2.md`, last written 13:50). There
  are therefore **no round-3 builder claims to check text against**, and the
  RT-19/N15 traceability rule cannot be verified for this round. Everything below
  is measured by me.
- Measured on `cad/exports/*_r9.stl` / `.step` (written 15:46), venv
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`, trimesh 5.0.0,
  numpy 2.5.1, ray-casting + face audits + proximity queries, independent of
  `dispenser.py`. `cad/dispenser.py` was last modified 15:45, i.e. **before** the
  exports — consistent for once.
- **Z-stack measured on the exports** (the whole stack moved down 10.000 mm since
  r7): housing roof top **−326.250**, roof underside **−335.250** (9.000 mm
  section), **disc top −336.750**, disc bottom −350.750, plate top **−351.250**,
  port bore −352.000…−354.250, chute bore to −405, plate bottom features to
  −418.300.

### The full journey, hopper → pocket → exit, with every pinch point vs the Ø13 worst case

| # | station | measured geometry (r9) | vs Ø13 worst-case granule |
|---|---|---|---|
| 1 | fill port (cap off), axis at (0.00, 43.45) | clear throat **r = 19.999 → Ø40.00** at z = −238.0; nothing below z = −240 within r 120 | **3.08 × D_max** |
| 2 | hopper barrel | inner **r 69.978** (z −270…−262), wall reached only at r ≥ 69.5 | 10.8 × D_max |
| 3 | funnel | r 69.978 @ −270 → **r 47.585 @ −326**; slope atan(56/22.39) = **68.2°** from horizontal | continuous, no step |
| 4 | sump outlet (annular window) | **r 19.996 → 46.99 = 27.00 mm radial**, arc **θ 130.25…249.75 = 119.5°** at the disc plane | **27.00/13.0 = 2.077** — below every no-arch criterion (≥3× for a slot). **N10 plateau, unchanged** (r7: 2.08, r6: 2.04) |
| 5 | deflector nose (rigid) | underside **1.500 mm** above the disc top at r = 22, 26, 30, 34, 38, 42, 46.5 (B8 holds); flat spans θ 130.4…158.4 at r22, **132.1…155.1 at PCD**, 137.1…152.9 at r46.5 | anything > 1.50 proud is rejected |
| 6 | bristles (compliant) | tip **+1.200 mm** above the disc top (assembly body, 312.2 mm³, θ **153.63…164.98**, r 20.81…47.11) | leads the rigid nose (nose wall first material at θ 152.9–158.5) ✔ |
| 7 | entry ramp (overfill relief) | see table below — **10.50 → 1.500 mm over θ 130.25 → 95**, 25.0° | full-section start, no step |
| 8 | transfer arc | roof underside **1.500 mm** above the disc top at every probe r = 20.5/24.5/32/39.5/45.5/46.5 × θ = 95, 90, 80, 60, 45, 30, 20, 10, 0, 350, 300, 270 | granule crown sits **1.500 mm below** the disc top → 3.000 mm clear |
| 9 | pocket | bore **Ø15.000** (r 7.498–7.500) through the full 14.00 mm; 45° chamfer **r 9.497@0.00, 9.297@0.20, 8.992@0.50, 8.489@1.00, 7.992@1.50, 7.498@≥2.00** | 2.00 mm diametral clearance; seated centre 8.000 below the disc top |
| 10 | exit port | **Ø16.000** (r 7.998–8.000, z −352.000…−354.250), 0.75 × 45° chamfer, **first material at the plate top r = 8.747** | 3.00 mm diametral clearance |
| 11 | chute | **r 10.993–11.000 (Ø22.000) continuous z −354.5 → −405**, unchanged with `count_windows` + `sensor_boards` + `sensor_cover` merged (**rmin 10.994** at the beam plane) | Ø13 swept down the axis in 1 mm steps: **0 stations with any interference** |

**Seated-granule transit (the B8.5 check).** Ø13 sphere, centre −344.750 (crown
1.500 below the disc top), carried round the PCD:

- minimum surface distance from the granule centre to `meter_housing` **9.500 mm
  → clearance +3.000**, to `brush_holder` **9.500 → +3.000**, to `hopper`
  22.722 → +16.222, to `agitator` 19.050 → +12.550 (720 stations, 0.5°);
- containment test at 180 stations (2°) against `meter_housing`, `brush_holder`,
  `hopper`, `agitator`, `retaining_plate_chute`: **0 stations with any granule
  vertex inside material.**

### Overfill relief before the housing arc — verified, and in the right order

Ceiling height above the disc top, measured on `meter_housing_r9.stl`
(nan = open sump window):

| θ | r20.5 | r24.5 | r32 | r39.5 | r45.5 | r46.5 |
|---|---|---|---|---|---|---|
| 131…250 | nan | nan | nan | nan | nan | nan |
| 130 | 10.50 | 10.47 | 10.50 | — | — | — |
| 129 | 10.29 | 10.27 | 10.24 | 10.27 | 10.29 | 10.30 |
| 128 | 9.94 | 9.95 | 9.98 | 10.01 | 10.03 | 10.03 |
| 125 | 9.16 | 9.17 | 9.20 | 9.22 | 9.25 | 9.25 |
| 120 | 7.86 | 7.87 | 7.90 | 7.92 | 7.94 | 7.94 |
| 115 | 6.57 | 6.57 | 6.59 | 6.61 | 6.63 | 6.63 |
| 110 | 5.27 | 5.28 | 5.29 | 5.31 | 5.32 | 5.32 |
| 105 | 3.97 | 3.98 | 3.99 | 4.00 | 4.01 | 4.01 |
| 100 | 2.68 | 2.68 | 2.69 | 2.69 | 2.70 | 2.70 |
| 98 | 2.16 | 2.16 | 2.17 | 2.17 | 2.18 | 2.18 |
| 96 | 1.64 | 1.64 | 1.65 | 1.65 | 1.65 | 1.65 |
| ≤95 | **1.500** | **1.500** | **1.500** | **1.500** | **1.500** | **1.500** |

Slope 8.74 mm over 34° of arc at PCD 32 (18.99 mm run) → **24.7°**, matched at all
six radii (spread ≤ 0.06 mm). The ramp mouth starts at the **full 9.00 mm roof
section** (ceiling 10.50 = roof top), so there is **no step at the entrance**.
Ordering is right: last fill opportunity is the window edge at **θ = 130.25**, the
ramp runs 130.25 → 95, nothing enters the covered arc unramped.

**B1 (the r6 through-slot) is still closed.** Roof thickness probed from the roof
top −326.25 down at r = 20.5/24.5/30/32/36/39.5/44/46.5 × θ = 300, 305, 308, 309,
**310, 310.5, 311**, 313, 316, 320, 330, 350, 0, 20, 45, 90: **9.00 mm at every one
of the 128 probes** (r6: 0.000 mm at θ = 310.0). θ = 200 reads nan because that is
the sump window, as designed.

### Adversarial fragment construction — the mandate item, re-derived on r9 geometry

All inputs measured above; σ = 0.36 MPa and µ = 0.4 are **carried ASSUMPTIONS**
(US4172714-derived, closure = IFDC S-115 bench test). Drive: BOM
14HS13-0804S-PG5, 0.14 N·m × 5.18 × 0.90 = **0.65 N·m** → at PCD 32 mm
**20.3 N in recovery, 12.2 N at the 0.60 normal-metering current fraction**.

**(a) Chamfer-nested fragment against a seated granule** — proud height above the
disc top (mm), solved from the measured 45° chamfer and the measured 8.000 mm seat:

| fragment | D13 centred | D13 seat +1.00 | D12 centred | D12 seat +1.50 |
|---|---|---|---|---|
| Ø4.0 | +0.64 | +0.17 | +0.28 | −0.43 |
| Ø4.5 | +1.22 | +0.77 | +0.86 | +0.17 |
| Ø5.0 | **+1.80** | +1.36 | +1.44 | +0.77 |
| Ø5.5 | +2.38 | +1.95 | +2.02 | +1.37 |
| Ø6.0 | +2.95 | +2.53 | +2.59 | +1.95 |
| Ø7.0 | +4.08 | +3.69 | +3.72 | +3.12 |

**Largest fragment that escapes rejection entirely** (crown below the 1.500 nose):
**Ø4.74** (D13 centred), **Ø5.12** (D13 offset), **Ø5.05** (D12 centred),
**Ø5.61** (D12 offset) — identical to r7, i.e. B8's gain over r6 (Ø6.0+) is held.
Escaping fragments still fit the exit: outer reach from the pocket axis
**7.31/7.65/7.76 mm (Ø4.0/Ø4.74/Ø5.0, D13 centred) vs the port bore r 8.000 →
min margin +0.236 mm**. That is the tightest clearance anywhere on the exit and it
is now a *port-bore* margin, not the old rim margin.

**(b) The wedged sliver that must be sheared** — sliver of radial width w trapped
in the crescent between a seated Ø13 granule and the measured Ø15.000 bore, shear
plane at the measured **1.500 mm** nose/roof underside:

| w (mm) | seat y above centre | seat depth below disc top | sliver height to reach the shear line | wedge half-angle | self-locking (<21.80°) | shear area, 90° shard | F_shear | margin vs 20.3 N (normal 12.2 N) |
|---|---|---|---|---|---|---|---|---|
| 1.000 | 0.000 | 8.000 | 9.500 | 0.00° | yes | 11.00 mm² | 3.96 N | 5.13× (3.08×) |
| 1.500 | 2.500 | 5.500 | 7.000 | 11.31° | yes | 15.90 mm² | 5.73 N | 3.55× (2.13×) |
| 2.000 | 3.464 | 4.536 | 6.036 | 16.10° | yes | 20.42 mm² | 7.35 N | 2.76× (1.66×) |
| 2.500 | 4.153 | 3.847 | 5.347 | 19.86° | yes | 24.54 mm² | 8.84 N | 2.30× (1.38×) |
| **2.793 (widest self-locking)** | 4.483 | 3.517 | **5.017** | **21.80°** | limit | **26.78 mm²** | **9.64 N** | **2.11× (1.26×)** |
| 3.000 | 4.690 | 3.310 | 4.810 | 23.09° | no | 28.27 mm² | 10.18 N | 2.00× (1.20×) |
| 5.000 | 6.000 | 2.000 | 3.500 | 33.69° | no | 39.27 mm² | 14.14 N | 1.44× (0.86×) |

**Shear-margin headline (unchanged from r7, re-derived on r9): the worst
self-locked sliver the pocket can hold — w = 2.793 mm, ≥ 5.017 mm tall — needs
9.64 N; the drive delivers 20.3 N in recovery and 12.2 N at normal current →
2.11× / 1.26×.** Capability bound **20.3 N / 0.36 MPa = 56.4 mm²** of shearable
section (33.9 mm² at normal current). Where it runs out: a **180° conforming
shard** at the same width is 53.56 mm² → 19.28 N → **1.05×** (and **0.63× at
normal current**, i.e. it needs the recovery stroke); a **full-ring 2.793 mm
crescent** is 107.11 mm² → 38.56 N → **0.53×, would stall**. I do not think a
180°/360° conforming crescent is credible from a crumbled 12 mm granule, but that
is the bound and it should stay written down.

Contact order is still compliant-first: **bristle tip 1.200 < nose 1.500 = roof
1.500 mm.**

### MODERATE 1 — the rigid deflector's confronting face is *vertical* over the whole granule band; the "27.5° lifting ramp / 1.92 vs 1.44" credit does not apply where it matters

Metering runs −θ, so granules meet the nose at its **high-θ** end. Measured at
0.05° steps on `brush_holder_r9.stl`, the underside jumps **1.50 → 7.45 mm in one
0.05° step at every radius**:

| r (mm) | flat ends at θ | h = 7.45 reached at θ | arc run | local face angle |
|---|---|---|---|---|
| 22.0 | 158.45 | 158.50 | 0.019 mm | **89.8°** |
| 26.0 | 156.80 | 156.85 | 0.023 mm | **89.8°** |
| 30.0 | 155.65 | 155.70 | 0.026 mm | **89.7°** |
| 34.0 | 154.75 | 154.80 | 0.030 mm | **89.7°** |
| 38.0 | 154.00 | 154.05 | 0.033 mm | **89.7°** |
| 42.0 | 153.45 | 153.50 | 0.037 mm | **89.6°** |
| 46.5 | 152.90 | 152.95 | 0.041 mm | **89.6°** |

So for every object between **1.50 and 7.45 mm proud** — which is the entire
fragment class B8 exists to reject (a Ø5.0 nested fragment is +1.80, Ø6.0 +2.95,
Ø7.0 +4.08) — the rigid element is a **5.95 mm square wall**, not a ramp. The
27.5° face the r1 critique credited (`n_z = +0.887`, largest single forward-facing
face **154.79 mm² at θ = 142.35, r = 29.04**) is the **top** of the nose and only
engages objects ≥ 7.45 mm proud. Forward-facing area audit in the granule band
(r 18–47.5, 0–10.5 mm above the disc): `brush_holder` **554.16 mm², 122.05 mm²
(22.0 %) vertical**, area-weighted n_z +0.652 — the vertical share **grew from
84.7 mm² (16.4 %) in r7** when the r2 reverse ramp was cut. `meter_housing`
forward-facing is genuinely ramped: 702.03 mm², only 76.82 mm² (10.9 %) vertical,
area-weighted n_z **−0.807**, largest single vertical face only 8.90 mm².
This is not a new defect (r7 had it too) but the *claim* attached to it is wrong,
and B8.3 explicitly asks for the nose lift/push ratio at the fragment sizes: at
1.80–4.08 mm proud it is **cot 89.7° ≈ 0.005, not 1.92**. What saves it is that
the sump is open above the nose so a stalled granule can be pushed back into the
bed, plus the shear backstop above — that argument should be written, not the
ramp one.

### MODERATE 2 — stall-recovery: rotationally free, but the reverse lead-in is 45° (cot = 1.00 < the 1.44 self-lock criterion) and the shipped "<6° reverse stroke" bound does not fit the worst park

**Rotational free travel is unconditional** (this is the rev-0 agitator-clash
item and it is clean). Full-revolution sweep, critical vertices of each rotor
against each static, 1° steps, 360 angles:

| rotor | static | min clearance | at rotation | angles with penetration |
|---|---|---|---|---|
| agitator | meter_housing | **0.778 mm** | 277.0° | **0/360** |
| agitator | hopper | 1.473 mm | 25.0° | 0/360 |
| agitator | brush_holder | 2.040 mm | 48.0° | 0/360 |
| agitator | retaining_plate | 25.350 mm | 0.0° | 0/360 |
| pocket_disc | meter_housing | 0.973 mm | 70.0° | 0/360 |
| pocket_disc | hopper | 6.639 mm | 273.0° | 0/360 |
| pocket_disc | brush_holder | **1.500 mm** | 20.0° | 0/360 |
| pocket_disc | retaining_plate | **0.500 mm** | 0.0° | 0/360 |

Point probes: agitator lowest point **z = −325.900** at r = 14.5 (housing top at
that radius is −328.05; the roof top −326.250 begins at r = 15.20), agitator
**r_max 46.743 at z = −323.750** against the hopper funnel wall at ≈48.49 →
**1.75 mm radial** (r7 measured 0.257 mm against the old chamber wall — this is a
real improvement), disc bottom to plate top **0.500 mm**, roof underside to disc
top **1.500 mm**. Agitation duty unchanged: **3 fingers at 0/120/240°**, 5.0° wide
at r = 40, reaching r 46.743; exactly one finger in the 119.5° window at a time;
each 22.5° index sweeps **18.8 %** of the window.

**What the recovery stroke actually meets.** The r2 reverse lead-in exists and is
real: ceiling at PCD **9.94 @ 251 → 9.38 @ 252 → 6.03 @ 258 → 2.68 @ 264 →
1.56 @ 266 → 1.500 @ ≥267**, i.e. 8.38 mm over 15° of arc (8.378 mm run) =
**45.0°** (r7 had a 292.9 mm², 100 %-vertical wall at θ = 250 instead). But 45°
gives **lift/push = cot 45° = 1.00**, against the **1.44** self-locking figure the
same critique chain applies to the forward path (housing entry ramp 24.7° →
cot = 2.17; nose top 27.5° → 1.92). Reverse-facing area audit: `meter_housing`
**449.62 mm², 77.36 mm² (17.2 %) vertical**, area-weighted n_z −0.585, largest
single face only 6.75 mm² (r7: 292.9 mm², 100 % vertical, largest 121.50 mm²) —
genuinely fixed. `brush_holder` **355.36 mm², 207.76 mm² (58.5 %) vertical**,
area-weighted n_z +0.160, largest reverse-facing face 86.11 mm² at θ = 135.22 —
**unchanged from r2's own measurement; O-2 is still open** (`brush_holder_r9.stl`
is byte-identical in size to r8 and measures identically).

Free reverse travel measured for a proud object at PCD, starting from each park
(pockets at 45° pitch, park phase 22.5°), stepping +θ until the ceiling drops
below the object:

| park θ | 2.0 mm proud | 5.0 mm proud | 11.5 mm proud (stacked 2nd granule) |
|---|---|---|---|
| 157.5 | 107.75° | 102.50° | **0.25°** (hits the brush-holder/bristle overhang at 157.75) |
| 180.0 | 85.25° | 80.00° | 70.25° |
| 202.5 | 62.75° | 57.50° | 47.75° |
| 225.0 | 40.25° | 35.00° | 25.25° |
| 247.5 | 17.75° | 12.50° | **2.75°** |

The r2 mitigation shipped as text was "bound the reverse-oscillate stroke to
< 6°". Measured, **two of the eight park positions have less than 6° of reverse
free travel for a stacked second granule** (0.25° at 157.5, 2.75° at 247.5), so
the bound as written does not cover the worst park. Both contacts are lead-ins,
not square walls (θ 247.5 → the 45° helicoid at 250.25; θ 157.5 → the holder
overhang at 8.64 mm ceiling), so this is a *bound-is-wrong* finding rather than a
jam, but the number in the notes should be the measured one: **the guaranteed
reverse free travel at any park, for any object the nose lets through
(≤ 1.50 mm proud), is unlimited; for an 11.5 mm stack it is 0.25°.**

### MODERATE 3 — chute plug: the seal is right, but there is no protection against dispensing into a fitted plug

`chute_plug_r9.stl`: sealing bead at **r_chute 11.150 vs the measured bore
11.000 → 0.150 mm radial = 0.300 mm diametral interference** over the band
z ≈ −381…−389 — inside N7's 0.2–0.4 mm spec ✔. But its Ø15.0 spigot (r_chute
7.500) occupies **z −405.25 … −383.00**, i.e. straight through the count-beam
plane, and leaves only **26.75 mm of chute above it = 2.06 × D_max**. Measured
consequence: with the plug fitted, granule 1 and 2 stack in the chute and
**granule 3 cannot clear the Ø16 exit port** — it is then between the moving disc
and the fixed plate, which is the one place the design has no compliant element.
Nothing in the geometry prevents this (no interlock, no tether, no flag into the
count beam that a boot check would see). One printed tab or a BOM tether line
closes it.

### BLOCKER — export integrity regressed onto `retaining_plate_chute` again (B10)

| part | r7 | r8 | **r9** |
|---|---|---|---|
| `retaining_plate_chute` | watertight **False**, `{2: 33312, 4: 3}` | watertight **True**, `{2: 46926}` | **watertight False**, `{2: 50720, 3: 1538, 1: 188, 4: 1, 5: 1, 6: 1}` — **188 boundary edges (actual holes)**, 1538 three-face edges, **21 shells**, volume 75.315 cm³ |

Defect locations (edge midpoints): boundary edges at **z −416.799…−411.800,
r_chute 23.489…33.699**; multiplicity-3 edges at **z −416.800…−360.750, r_chute
21.734…74.466**. **Minimum r_chute over all defective edges is 21.734 mm against a
bore wall at 11.000**, so the granule bore itself measures clean by ray-casting
(Ø22.000 continuous, Ø13 sweep 0 interference) — but the exported solid is
invalid, and **every `0.000 mm³` boolean anyone computes against this part
(exit-port clearance, chute continuity, count-window intrusion, harness routing)
is computed on a broken shell.** The assembly inherits it:
`dispenser_r9_assembly.stl` watertight **False**, 44 shells, **2 inverted-normal
bodies of −137.4 mm³** at (11.5…14.0, ±30…35, z −416.8…−414.3). Separately,
`chute_plug_r9.stl` contains a **−3930.3 mm³ inverted-normal body** (its Ø15
spigot, x 24.5…39.5, y ±7.5, z −405.25…−383.00). Part STLs that *are* clean:
agitator, bay_lid, brush_holder, count_windows, electronics_bay, fill_cap,
hopper, meter_housing, pocket_disc, sensor_boards, sensor_cover, service_stand,
top_plate — **14 of 15 part STLs watertight; `retaining_plate_chute` is not, and
`chute_plug` is watertight but carries the inverted body above.** Punch list B10 requires the checker's own output to show all part STLs
watertight; it does not.

### MAJOR — B7's shipped release numbers do not reproduce

B7 may close as a documented plateau, and the plateau text in `docs/DESIGN.md`
§4.6 is honest about the *direction* of the finding. But the numbers do not
reproduce. Criterion used here: the granule is supported while its lowest point
(directly below its centre, sphere) is over **flat plate top material**, i.e.
while |pellet centre − port axis| ≥ the measured **8.747 mm** first-material
radius at z = −351.250; the 0.75 × 45° chamfer cannot hold a sphere whose radius
(6.5) is below the throat radius (8.000). Sweep at 0.25° steps on
`retaining_plate_chute_r9.stl`:

| granule | seat offset | support lost, into the 22.5° index | % of the move | pellet-centre-to-port | pocket-axis-to-port |
|---|---|---|---|---|---|
| Ø13 | +1.00 | **5.00°** | 22.2 % | 8.736 mm | 9.736 mm |
| Ø13 | 0.00 | **7.00°** | 31.1 % | 8.630 mm | 8.630 mm |
| Ø13 | −1.00 | **8.75°** | 38.9 % | 8.661 mm | 7.661 mm |
| Ø12 | +1.50 | 4.25° | 18.9 % | 8.650 mm | 10.150 mm |
| Ø12 | 0.00 | 7.00° | 31.1 % | 8.630 mm | 8.630 mm |
| Ø12 | −1.50 | 9.75° | 43.3 % | 8.606 mm | 7.106 mm |
| Ø11 | +2.00 | 3.25° | 14.4 % | 8.701 mm | 10.701 mm |
| Ø11 | 0.00 | 7.00° | 31.1 % | 8.630 mm | 8.630 mm |
| Ø11 | −2.00 | 10.50° | 46.7 % | 8.690 mm | 6.690 mm |

**Release-angle spread: 3.75° for Ø13 alone, 7.25° across Ø11–Ø13** — against the
**"1.00°"** printed in `BUILD-NOTES-r2.md` §3 and repeated in `docs/DESIGN.md`
§4.6, and against the release window **"6.75–7.75°"** there (measured
**3.25–10.50°**). B7.1 (support retained until |separation| ≤ 1.0 mm) still fails
by 5.995–10.701 mm; lateral velocity at the PCD is unchanged at **0.126 m/s**
(225 °/s mean) / **0.251 m/s** (450 °/s peak). Park retention re-printed and
unaffected: worst-placed **Ø13 +2.739 mm, Ø12 +2.239, Ø11 +1.739** against the
8.747 rim. **Fix the two numbers in DESIGN/BUILD-NOTES, or show why the seat
offset should be applied differently — as written they are the kind of
"measured" claim RT-19/N15 exists to catch.**

### Minor, for the record

- **Hopper mouth is closed** (r1 BLOCKER 1 stays closed): rays up from z = −250
  on a 5 mm grid over r ≤ 67 → **556 of 557 cells covered**. The single open cell
  at (23, 28) is a **ray-transparent tessellation seam < 0.05 mm wide** (offset
  the ray +0.05 mm in x and it hits material at −235.60/−233.55); it is not a
  granule path, but any checker probing on a grid will keep reporting it.
- **N6 stays closed**: disc lightening voids measured open at r 11.0 (120/360
  samples) through r 15.0 (104/360) and **closed at r 15.5 (0/360)**; sump window
  inner edge r = 20.00 → **radial land 4.50–5.00 mm** (punch list asks ≥ 2.0).
- **Fill route (upstream of my lane, but measured)**: Ø13 dropped on the fill axis
  in 2 mm steps from −235 to −320 touches nothing until the 68.2° funnel wall at
  z = −319, which is a roll-down surface, not an obstruction.

### What I would require to pass the granule path next round

1. `retaining_plate_chute` and `chute_plug` **watertight, 0 boundary edges, 0
   inverted-normal bodies**, and the assembly likewise — with the checker's own
   output quoted. Until then no `0.000 mm³` claim on that part is admissible.
2. Correct the B7 spread/window numbers in `BUILD-NOTES` and `docs/DESIGN.md` to
   measured values (**3.25–10.50° into the index, spread 7.25° / 3.75° at Ø13**),
   or show the alternative construction that yields 1.00°.
3. Restate B8.3 against the geometry that actually exists: the nose confronts the
   1.50–7.45 mm band with a **89.6–89.8° face**, not a 27.5° ramp; either chamfer
   that face (a 3 mm × 30° lead-in costs nothing structurally) or drop the
   lift/push credit and argue the open-sump-return path explicitly.
4. Publish the reverse-stroke bound as measured (**0.25° at the θ = 157.5 park,
   2.75° at 247.5, for an 11.5 mm stack**), not "< 6°".
5. Keep the shear table and its bound (**2.11× at the worst self-locking sliver;
   1.05× at a 180° shard; 0.53× at a full ring; σ = 0.36 MPa, µ = 0.4
   assumptions**) in the shipped notes.

## count-sensor

**Owner:** count-sensor geometry critic (rev-0 RT-3 / rev-1 punch-list **B4**).
**Verdict: NOT CLOSED — 2 BLOCKING.** Every ECO-3/ECO-4/ECO-5/ECO-9 geometry
item passes on the r9 export, the r2 chute-plug/window collision is fixed, and
the BOM is clean. What blocks: (1) the emitter that r2 asked to be *housed* is
housed against the wrong package — the Vishay drawing for the TSAL6200 the BOM
orders says **8.7 ± 0.3 mm** from the seating plane, the model uses **5.8 mm**,
and the datasheet envelope booleans to **11.2532 mm³ of interference per LED**
against the plate; (2) `retaining_plate_chute_r9.stl` — the part that carries the
whole count sensor — **is not watertight** (1729 non-manifold/open edges, STL
volume +8.36 % against its own STEP), a regression from r8.

**Provenance.** Every number below I measured myself on
`cad/exports/*_r9.step` / `*_r9.stl` with
`~/.openclaw/workspace/venvs/dock-cad-314/bin/python` (build123d 0.11.1 / OCP
exact booleans and `BRepClass3d_SolidClassifier` point classification; trimesh
5.0.0 for mesh topology only). Package dimensions are from the two Vishay PDFs
**fetched during this review** (links are in `ELECTRONICS.md` §10), not from
memory. `_run/rev1/BUILD-NOTES-r3.md` **does not exist** at review time
(16:25 CDT; `_run/rev1/` holds only BUILD-NOTES-r2.md, CRITIQUE-r1/r2,
PUNCHLIST, CONTEXT), so there are no round-3 notes to agree or disagree with —
every claim below is mine, and there is no quoted builder output for RT-19/N15
to be checked against. `cad/` also has no round-3 checker (`verify_exports.py`
01:45, `verify_r2.py` 13:44; `dispenser.py` 15:45, exports 15:46, `BOM.md` 15:55).

```
MD5 (retaining_plate_chute_r9.stl) = 5a4463f1d97608ec150ccd2438f0e2b6
MD5 (count_windows_r9.stl)         = 43f785bf132e7ac31e1c3b27602f7121   (byte-identical to r8)
MD5 (sensor_cover_r9.stl)          = 8bdb178757442d8502660ee644c4a0e2
MD5 (sensor_boards_r9.stl)         = 6454423968c6e9c305c87b2b9c50204e   (new part this round)
MD5 (chute_plug_r9.stl)            = 99675c5cdbb0a02a2ab3f409bd6ec2b2
MD5 (dispenser_r9_assembly.stl)    = 7b1395035a4e6139d1d0b6dce7e6dcbc
```

Datum recovered from the exports, not from the source: chute bore **Ø22.000** on
the axis **x = 32.000**; the Ø16.000 disc port runs z −352.000 → −354.250 and the
Ø22 bore starts at **z = −354.250**; `Z_SENSOR` (mid-plane of the two beams) =
**−395.250**; exact plate volume **69502.358 mm³** (= the 69.50 cm³ in `BOM.md`).

---

### PASS — ECO-3 / ECO-9 aperture geometry (exact OCC classification, bisected edges)

| beam | side | run | y probe | x centre | Ø in x | z centre | Ø in z |
|---|---|---|---|---|---|---|---|
| A | +y | inner | +13.0 | **29.0000** | 3.1999 | **−392.2500** | 3.1999 |
| B | +y | inner | +13.0 | **35.0000** | 3.1999 | **−398.2500** | 3.1999 |
| A | +y | outer | +16.0 | **29.8000** | 3.1999 | −392.2500 | 3.1999 |
| B | +y | outer | +16.0 | **35.8000** | 3.1999 | −398.2500 | 3.1999 |
| A | −y | inner | −13.0 | **29.0000** | 3.1999 | −392.2500 | 3.1999 |
| B | −y | inner | −13.0 | **35.0000** | 3.1999 | −398.2500 | 3.1999 |
| A | −y | outer | −16.0 | **29.8000** | 3.1999 | −392.2500 | 3.1999 |
| B | −y | outer | −16.0 | **35.8000** | 3.1999 | −398.2500 | 3.1999 |

(the 3.1999 rather than 3.2000 is my 1e-4 bisection tolerance, not the model.)

Independent confirmation from the B-rep face census (cylindrical faces of
`retaining_plate_chute_r9.step` in the boss region), which also gives the runs:

```
  centre=(  29.000, +/-13.250, -392.250)  R=1.600  y[12.000,14.500]   inner tunnel, beam A
  centre=(  29.800, +/-15.747, -392.250)  R=1.600  y[14.495,17.000]   labyrinth run, beam A
  centre=(  35.000, +/-13.250, -398.250)  R=1.600  y[12.000,14.500]   inner tunnel, beam B
  centre=(  35.800, +/-15.747, -398.250)  R=1.600  y[14.495,17.000]   labyrinth run, beam B
  centre=(  29.000, +/-10.610, -392.250)  R=3.000  y[ 9.220,12.000]   ECO-4 window seat, beam A
  centre=(  35.000, +/-10.610, -398.250)  R=3.000  y[ 9.220,12.000]   ECO-4 window seat, beam B
  centre=(  34.500, +/-25.000, -407.250)  R=0.800  y[22.500,27.500]   M2 cover pilot
  centre=(  34.500, +/-25.000, -383.250)  R=0.800  y[22.500,27.500]   M2 cover pilot
  centre=(  41.000, +/-22.500, -406.600)  R=2.500  y[20.000,25.000]   Dia5 grommet port
```

- **4 tunnels, 2 per side** (B4.1) ✓; chord offsets from the bore axis
  **−3.000 / +3.000 mm** = ECO-3's x = 29 / 35 ✓.
- **ECO-9 stagger = |−392.250 − (−398.250)| = 6.000 mm** ✓.
- Both sides on the same x/z grid → each beam is a straight chord along y ✓.
- Unchanged from r8 to 1e-4 mm. Nothing regressed.

### PASS — ECO-5 labyrinth

Outer run offset **+0.800 mm in x** (29.000 → 29.800, 35.000 → 35.800), outer run
length **2.505 mm** (|y| 14.495 → 17.000), inner run **2.500 mm** (12.000 →
14.500), ledge **0.800 mm** on the −x side of each tunnel (B4.5 asks ≥ 0.7) ✓.
Identical on +y and −y.

Clear aperture (two Ø3.2 circles offset 0.800 in x, exact):
**area 5.5094 mm², 2.400 mm wide in x, 3.098 mm tall in z**, largest clear
coaxial cylinder **Ø1.600**.

### PASS — ECO-4 windows, and nothing proud of the bore

```
  count_windows_r9: 4 solids, 103.8909 mm3 exact, each Dia5.900 x 0.950
     (26.050..31.950, |y| 11.000..11.950, z -395.200..-389.300)   beam A, both sides
     (32.050..37.950, |y| 11.000..11.950, z -401.200..-395.300)   beam B, both sides
  material inside the nominal Dia22.000 x 26 chute bore over the sensor band:
     retaining_plate_chute_r9 = 0.000000 mm3      count_windows_r9 = 0.000000 mm3
     (also 0.000000 at Dia21.99 and Dia21.9)
  count_windows ^ retaining_plate_chute = 0.000000 mm3
```

Window inner faces sit exactly on **|y| = 11.000** = the bore's maximum radius,
seat floor **|y| = 12.000**. **B4.4's "0.4 ± 0.05 mm deep" is still 1.000 mm**
(my r2 NB-3, unchanged, and `ELECTRONICS.md` §4.5 has not been edited —
mtime 2026-08-07 04:13). It is open, undercut-free and swab-reachable, which is
the property ECO-4 wants, but the dimension in the punch list is not met.

### PASS — B4.3 boss envelope and motor clearance (measured on `dispenser_r9_assembly.step`)

Boss x-min **22.000** (≥ 22.0 ✓), boss x-max 47.000, boss outer face |y| =
**27.500** (was 25.000 in r8), boss z −409.750…−380.750. Stepper = the 69.936 cm³
solid:

```
  boss z-band     z[-409.75,-380.75]: stepper x_max = 18.0000 -> clearance to boss face x=22.000 = 4.0000 mm
  cavity z-band   z[-402.46,-388.04]: stepper x_max = 17.6000 -> clearance = 4.4000 mm
  Z_SENSOR +/-1   z[-396.25,-394.25]: stepper x_max = 17.6000 -> clearance = 4.4000 mm
  beam A +/-1 mm  z[-393.25,-391.25]: stepper x_max = 17.6000 -> clearance = 4.4000 mm
  beam B +/-1 mm  z[-399.25,-397.25]: stepper x_max = 17.6000 -> clearance = 4.4000 mm
  stepper material in the corridor x 18..22, |y|<25, z -409.75..-380.75 = 0.0000 mm3
```

**4.0000 mm worst case** (B4.3 asks ≥ 4.0; r6 was 1.4). All-pairs exact boolean
of the whole sensor group (2 covers, 2 boards, 4 windows) against every one of
the 24 assembly solids: **no non-zero pair**.

### PASS — B4.6 cavity, and B4.8 granule column

```
  +y 20 x 8 x 12 pocket centred (34.5, 21.0, -395.25): plate 0.0000 mm3
  -y 20 x 8 x 12 pocket centred (34.5,-21.0, -395.25): plate 0.0000 mm3
  board 18x12x2 +1 mm all round (20 x 4 x 14), both sides: plate 0.0000 mm3
  Dia13 x 60 swept column on the chute axis ^ plate = 0.000000 mm3  ^ windows = 0.000000 mm3
  Dia13 spheres at z = -389.25 / -392.25 / -395.25 / -398.25 / -401.25: 0.000000 mm3 each, plate and windows
```

Cavity measured **20.400 (x) × 14.400 (z)**, x 24.300…44.700, z −402.460…−388.040,
open from **|y| 17.000 (aperture plane) to 27.500 (boss face)** — 10.500 mm deep,
empty (`plate ∩ cavity envelope = 0.0000 mm³` both sides).

### PASS — B4.7 BOM (`cad/BOM.md`, mtime 15:55, after the 15:46 exports)

**No TSSP4038 line**; the only occurrence of the string is
`"replaces the REJECTED TSSP4038"` inside the VBPW34FAS row. Present:
`count PD x2 Vishay VBPW34FAS`, `count amp TI OPA2320AIDR`,
`count emitter x2 Vishay TSAL6200`, `count windows x4 Dia6 x 1.0 cast PMMA disc`,
`sensor-cover screws 4x M2x6 self-tap`, plus `sensor_cover (x2)` and
`count_windows (x4)` in the printed-parts table. **B4.7 passes on every clause.**

### PASS — my r2 NB-1 (storage plug scrubbing the beam-B windows) is fixed

```
  chute_plug_r9 ^ count_windows_r9      = 0.000000 mm3   (r8: 0.5981 mm3 on each of windows 1 and 3)
  chute_plug_r9 ^ retaining_plate_chute = 189.1262 mm3   (r8: 200.9078 -- the designed press fit)
```

### PASS — ECO-12 / N3 board clamp still exists and is real

`sensor_cover_r9` = 2 bodies, 1602.988 mm³ each, bbox x 22.000…47.000,
|y| 25.500…29.500, z −409.750…−380.750. Measured by y-slabs:

- **four posts, 36.000 mm² total** (4 × 3 × 3), |y| **25.500 → 27.000**, tips
  bearing on the board's outer face; bearing on the 18 × 12 board footprint
  = **30.000 mm²** (N3 asks ≥ 8) ✓;
- **register lip 20.000 × 14.000 × 0.500** at |y| 27.000…27.500 into the
  20.400 × 14.400 cavity mouth = **0.200 mm/side**;
- flange 25 × 29 × 2.000 at |y| 27.500…29.500, 716.690 mm² section;
- **2 × M2 pilots per boss**, Ø1.600 × 5.000 deep at (34.5, ±25.0, −407.250)
  and (34.5, ±25.0, −383.250), against Ø2.300 clearance holes in the cover —
  the BOM's 4 × M2×6 have somewhere to go (r2 checked this on r8 and it survives);
- **Ø5.000 grommet port** at (41.0, ±22.5) into the duct socket, |y| 20…25.

---

### BLOCKING 1 — the ordered emitter still does not fit: the model uses a 5.8 mm TSAL6200; the Vishay drawing says 8.7 ± 0.3 mm

r2's blocker was "the emitter and the receiver have no volume". r9 answers it by
adding `sensor_boards_r9` (2 × 18 × 12 × 2 PCB + modelled device envelopes) and
by deepening the boss (|y| 25.5 → 27.5) so the aperture-facing room went from
2.500 to **6.500 mm**. Against the *modelled* envelopes everything is clean:

```
  sensor_boards_r9 ^ retaining_plate_chute_r9 = 0.0000 mm3
  sensor_boards_r9 ^ sensor_cover_r9          = 0.0000 mm3
  sensor_boards_r9 ^ count_windows_r9         = 0.0000 mm3
  modelled emitter: Dia5.9 x 1.0 rim + Dia5.0 x 4.8 body = 5.800 mm tall, axes x = 29.800 / 35.800,
                    z = -392.250 / -398.250, seating plane |y| = 23.500, nose |y| = 17.700 (0.700 mm of air)
  modelled receiver: 4.500 (x) x 3.200 (y) x 4.000 (z) box, same axes, face |y| = 20.300
```

But `dispenser.py` L505-506 / L554-555 / L2082-2085 label those envelopes
`[knowledge, not a datasheet file in this run; CLOSURE = the Vishay package
drawings]`. **I fetched the drawings.** They do not support the model:

| source | part | package figures as printed |
|---|---|---|
| Vishay doc **81010** rev 2.4, drawing 6.544-5259.06-4 | **TSAL6200** | T-1¾, **Ø5 ± 0.15** body, **Ø5.8 ± 0.15** flange, **8.7 ± 0.3 mm** seating plane → dome apex, dome **R 2.49 sphere** |
| Vishay doc **81127** rev 1.3 | **VBPW34FAS** | **surface-mount** gullwing, **L × W × H = 6.4 × 3.9 × 1.2 mm**, 7.5 mm² active |

So the emitter is **8.7 mm tall, not 5.8** — 2.900 mm more than modelled, 3.200 mm
at the max-material limit — against **6.500 mm** of aperture-facing room. Built
as a datasheet solid (Ø5.8 flange 0.7 + Ø5.0 barrel + R2.49 dome) on the modelled
seating plane |y| = 23.500 and centred on the modelled device axes:

```
  TSAL6200 (8.7 nominal) at (+y, x=29.800, z=-392.250): envelope |y| 14.800..23.500 (tip 2.200 mm past the aperture plane)
     ^ retaining_plate_chute_r9 = 11.2532 mm3     ^ sensor_cover_r9 = 0.0000 mm3
  TSAL6200 (8.7 nominal) at (+y, x=35.800, z=-398.250):
     ^ retaining_plate_chute_r9 = 11.2532 mm3     ^ sensor_cover_r9 = 0.0000 mm3
  TSAL6200 at max tolerance 9.0: ^ plate = 14.6614 mm3 per LED
  minimum seating plane at which a datasheet TSAL6200 clears the plate: |y| = 25.1175
     -> the board must retract 1.6175 mm (check at 25.1175: 0.000001 mm3; at 23.500: 11.2532 mm3)
```

The Ø5.0 barrel cannot enter the Ø3.2 tunnel; only the spherical cap of the
R2.49 dome inside Ø3.2 can, and that is **0.582 mm** deep
(`d = R − √(R² − 1.6²) = 2.49 − 1.9079`). So the LED bottoms on the printed
cavity floor **1.618 mm before the board reaches its seat**, and the whole stack
downstream of the board plane is dimensioned to 23.500/25.500: the four cover
posts (25.500…27.000), the register lip (27.000…27.500), the Ø1.6 screw pilots
(22.500…27.500) and the boss face (27.500). Retracting the board 1.618 mm puts
its outer face at 27.118 — 1.618 mm past the post tips — so the cover cannot
close and the two M2 screws cannot pull down. **The count sensor as specified
still cannot be assembled into the count sensor as modelled**; only the number
that has to change moved from 2.5 mm to 1.6 mm.

**Correction to my own r2 text, so it is not propagated a third time:** r2 said
"VBPW34FAS (BPW34 DIL case) ≈3.2 mm case … does not fit by ≈0.7 mm" and
"TSAL6200 ≈5.8 mm body above the seating plane". Both were wrong.
**VBPW34FAS is the SMD part** — 6.4 × 3.9 × **1.2** mm — and it fits with room to
spare; the model's 4.5 × 4.0 × 3.2 box is wrong in all three axes but
conservative in the axis that matters. Datasheet-envelope check:

```
  VBPW34FAS 6.4 x 3.9 x 1.2 seated on the board face |y| = 23.500, at (-y, x=29.800, z=-392.250)
     envelope |y| 22.300..23.500, x 26.600..33.000, z -394.200..-390.300
     ^ retaining_plate_chute_r9 = 0.0000 mm3   ^ sensor_cover_r9 = 0.0000 mm3
  same at (-y, x=35.800, z=-398.250):  ^ plate = 0.0000   ^ cover = 0.0000 mm3
  mutual overlap of the two datasheet PDs (6.000 x 6.000 diagonal pitch) = 0.0000 mm3
```

**The receiver side passes on the real part; the emitter side is the blocker.**
It is the emitter's 5.8 mm figure — which came from my own r2 critique, not from
a drawing — that the build was closed against.

**What closes it (any one, measured):**
1. Re-specify the emitter to a low-profile part (SMD 940 nm, e.g. a 1.6–2.5 mm
   package) and correct `ELECTRONICS.md` §4.4/§7 **and the optical budget**
   (182× is computed for TSAL6200 at 40 mW/sr and a 32 mm path).
2. Keep the TSAL6200 and give it 8.7 + clearance: seating plane |y| ≥ 25.118 →
   boss face ≥ 29.1, cover/post/pilot stack all moved out ~1.7 mm (mass and the
   x-extent of the boss are unaffected; the boss grows in |y| only).
3. Counterbore the cavity floor Ø6.0 × 1.7 deep around each tunnel mouth:
   the floor is 17.000 − 10.778 = **6.222 mm** thick at x = 29.8 and the window
   seat floor is at |y| = 12.000, so 1.7 mm leaves 3.3 mm to the seat — feasible,
   but it re-opens the ECO-4 sealed-tunnel argument, so option 2 is cleaner.
**Acceptance test either way:** the datasheet package solid (Ø5.8 flange, Ø5.0
barrel, R2.49 dome, 8.7 mm, or the replacement part's envelope + its drawing
reference) seated on the board plane and centred on the device axes booleans to
**0.000 mm³ against plate and cover on both sides**, with the *tolerance* case
(8.7 + 0.3) also printed.

### BLOCKING 2 — `retaining_plate_chute_r9.stl` is not watertight (and it is the part the count sensor lives in)

This is punch-list **B10**'s subject, but it is my part and it is a regression, so
I am recording it rather than assuming another critic owns it.

```
  r8 retaining_plate_chute.stl: watertight True   euler -66  vol 57979.528   edge multiplicity {2: 46926}
  r9 retaining_plate_chute.stl: watertight False  euler -58  vol 75314.857
      edge multiplicity {2: 50720, 3: 1538, 1: 188, 4: 1, 5: 1, 6: 1}  -> 1729 non-manifold/open edges
  r9 exact STEP volume 69502.358 mm3 -> the STL overstates by +5812.499 mm3 (+8.36 %)
  bad edges inside the sensor-boss bbox: 252 of 1729,
      all at z = -410.750, x 38.502..43.498, |y| = 25.000  (the grommet-port / duct-socket face)
  nearest bad edge to the beam-A aperture axis: 20.618 mm; to beam B: 12.879 mm (0 within 3 mm of either)
  dispenser_r9_assembly.stl: watertight False, euler -179, 1735 non-manifold/open edges
  every other r9 part STL: watertight True, 0 non-manifold edges
     (agitator, bay_lid, brush_holder, chute_plug, count_windows, electronics_bay, fill_cap, hopper,
      meter_housing, pocket_disc, sensor_boards, sensor_cover, service_stand, top_plate)
```

The optical geometry itself is clean — the defects are on the cable-port face,
not on the tunnels or the window seats — so **all my measurements above were taken
on the STEP**, and they stand. The consequence is for anyone else: an STL-based
check of this part on r9 (including the round's own checker if it loads STLs)
is measuring a mesh whose volume is 8.36 % wrong. B10's acceptance test
("10/10 part STLs watertight, assembly 16/16, 0 non-manifold edges") fails
**14/16 parts watertight, plate and assembly bad**.

---

### NONBLOCKING — measured, recorded

**NB-1 — the board is clamped in one direction only; ±1.200 mm of lateral float.**
The cavity is 20.400 × 14.400 and the board is 18.000 × 12.000, with no register
feature and no locating pin: **±1.200 mm of play in x and in z**. Axially the
posts fix the outer face at |y| = 25.500 but nothing bears on the inner face, so
the board can travel **0.700 mm inward** until the LED noses touch the cavity
floor. The chord geometry (§4.3) is set by the *apertures*, so the beam positions
do not move — but the emitter axis can be 1.2 mm off its tunnel, and ECO-12's
stated purpose is "the optical alignment that the ±3.0 mm chord geometry depends
on". A 0.5 mm register step in the cavity mouth, or two Ø1.5 locating pins in the
floor, would close it for nothing. (Same class as r8; not a regression.)

**NB-2 — B4.2 as literally written still fails; the area criterion is the right one.**

```
  Dia1.6 x 34 coaxial on the nominal beam axis (x=29 / x=35): plate 0.00000 mm3
  Dia2.0 x 34 :  1.19317 mm3      Dia2.0 x 60 :  1.19317 mm3      Dia3.2 x 34 : 12.66539 mm3
  Dia1.6 x 34 on the labyrinth axes (29.8 / 35.8): 0.00000 mm3;  Dia2.0 x 34: 1.19079 mm3
```

Identical to r8 to 1e-5 mm³. The ECO-5 labyrinth makes a Ø2.0 through-cylinder
impossible by construction; the honest criterion is the lens area,
**5.5094 mm² theoretical** (2.400 × 3.098 mm), with **Ø1.600** as the largest
clear coaxial cylinder.

**NB-3 — the sensing datum moved and `ELECTRONICS.md` §4.2/§4.3 has not been
re-based.** The doc's whole dark-time table is built on "40 mm below the
retaining plate, v = 0.886 m/s". Measured on r9 (fall from the Ø22 bore entry
z = −354.250):

```
  beam A: fall 38.000 mm -> v_A = 863.5 mm/s        beam B: fall 44.000 mm -> v_B = 929.1 mm/s
  (from the Dia16 port top z = -352.000 instead: 40.250 / 46.250 mm -> 888.7 / 952.6 mm/s)
  ECO-9 velocity solve over the measured 6.000 mm stagger: dt_mid = 6.694 ms   (ELECTRONICS 4.3 quotes 6.54 ms)
  guaranteed dark time, per-beam velocities, chords at the measured clear-aperture centroids (-2.600/+3.400):
    D13  guaranteed 12.827 ms (worst x0=+0.804)   best 15.056 ms    gate 9.7 ms -> +32.2 %
    D12  guaranteed 11.564 ms (worst x0=+0.728)   best 13.898 ms    -> +19.2 %
    D11  guaranteed 10.264 ms (worst x0=+0.658)   best 12.739 ms    -> +5.8 %
    D8   guaranteed  0.000 ms (misses both at |x0|>=7)  best  9.265 ms  -> -4.5 %
    D5   guaranteed  0.000 ms                            best  5.791 ms  -> -40.3 %
  (nominal aperture axes -3.000/+3.000 give the same times, only the worst x0 shifts)
```

The separator the 9.7 ms gate sits in is now **9.265 … 10.264 ms**, i.e. ±5 %
rather than the doc's ±7 %, purely because beam A is 2 mm higher than the doc's
assumption. Not a CAD defect — ECO-3 specifies the apertures and the CAD has
them — but the gate must be re-derived from these numbers, and it belongs in B1.

**NB-4 — optical path length is 38–40 mm, not the 32 mm in the optical budget.**
As modelled the LED nose is at |y| = 17.700 and the PD face at |y| = 20.300 →
**38.000 mm** emitter-to-detector; with the datasheet 1.2 mm SMD PD on the same
board face it is **40.000 mm**. §4.4 computes 39.1 W/m² and 182× excess gain for
a 32 mm path; at 40 mm that is (32/40)² = **0.64 → ≈25 W/m², ≈116 µA, ≈116×**.
Still a large dust margin, still fine — but the headline number in §4.4 is 1.56×
optimistic against the geometry that now exists.

**NB-5 — aperture height vs dark time (carried from r2).** The clear aperture is
**3.098 mm tall**; at v_A = 863.5 mm/s a granule takes **3.587 ms** to traverse
it, **35 %** of the 10.264 ms D11 guarantee. The 9.7 ms gate is not derivable
without stating the occlusion fraction at which the comparator fires. Carry to B1.

**NB-6 — the sensor cavity is still not sealed to the outside.** Cover/boss joint
is a flat land at |y| = 27.500 with **no groove in either part**; the register lip
has 0.200 mm/side clearance and the two M2 screws per cover are both on
x = 34.500, leaving 12.500 mm of unsupported cover each way. Chute-side sealing
is the window's job and is done (`plate ∩ windows = 0.000000`, nothing proud of
the bore). Either add a bead/groove or say plainly in README/DESIGN that the
sensor cavity is dust-resistant, not sealed (N8 applied to a joint N8 did not
enumerate). Unchanged from r2.

**NB-7 — documentation is still false, three rounds after the geometry changed.**
`README.md` (mtime 04:51, i.e. before r7/r8/r9) line 40 still says the verified
count is **"NOT MET in this revision — the sensing … exists only in
`electronics/`, not in the CAD"**, and its RT-3 row still says the ECOs "were
never merged" and "`cad/BOM.md` still lists the TSSP4038".
`docs/DESIGN.md` (mtime 13:50) line 564 **"None of the ECOs were merged into
`cad/dispenser.py`. That is RT-3."** and line 637 repeat it. All of that is false
against r9 — the apertures, stagger, labyrinth, windows, covers, boards and the
BOM are all there. This is the RT-19/N15 rule pointed the other way (the docs
under-claim what the geometry contains), and it is the third round it has been
raised. It is a one-line edit each.

**NB-8 — BOM nits.** `count windows x4` is specified **Ø6 × 1.0** but the
modelled disc is **Ø5.900 × 0.950** (seat Ø6.000, floor |y| = 12.000, so the
0.05 mm/side and 0.05 mm bond gaps are deliberate — say so). Still **no line for
the two 18 × 12 sensor PCBs themselves** and none for the window bonding
adhesive, although `sensor_boards` is now a modelled, exported part with a 6.0 g
mass in the model.

**NB-9 — device datums are now published in the source** (`dispenser.py` prints
"NB-4 DATUMS PUBLISHED: the devices sit on the LABYRINTH mouths x = 29.800 /
35.800 … board centre x = 34.500"), which answers my r2 item 3 — but with no
BUILD-NOTES-r3.md and no BOM/DESIGN line, the number is still only in the model
source. Put x = 29.800 / 35.800, z = −392.250 / −398.250, board centre
x = 34.500 into the board fabrication note.

### What has to change for me to pass this domain

1. **Fit the real emitter** (option 1/2/3 above) and prove it with the datasheet
   package solid at nominal **and** at max tolerance, plate and cover, both
   sides, 0.000 mm³ — and fix the 5.8 mm figure wherever it is written
   (`dispenser.py` L505-506, L554-555, L2082-2085, and my r2 critique's table).
2. **Re-export a watertight `retaining_plate_chute`** (and assembly) and print
   the edge-multiplicity census for it.
3. Correct `README.md` line 40 + its RT-3 row and `docs/DESIGN.md` lines 564/637.
4. Not mine to edit, carried: `ELECTRONICS.md` §4.2/§4.3 fall height (38.0/44.0 mm
   measured, not 40), §4.4 optical path (38–40 mm, not 32), §4.5 ECO-4 "flush at
   y = ±11" / 0.4 mm seat, ECO-3 boss height, and the receiver's package form
   (SMD 6.4 × 3.9 × 1.2, not a DIL case).

## assembly

**Owner:** assembly-and-drive critic (rev-0 RT-1; punch-list **B2, B3-access,
B9c/d, B10, B12.2** in so far as they are assembly/torque items).
**Verdict: FAIL — 2 blocking findings.** All three of round 2's blockers
(A-5 fill cap trapped by the B6 neck, A-6 `sensor_cover` unable to reach its
seat, A-7 no drive-reaction path) are **closed on the r9 exports**, and so are
all five of round 2's non-blocking items. The torque path measures clean for the
third round running. What fails now is (i) the largest structural part's STL is
no longer a valid mesh, and (ii) the two screws that are the electronics bay's
only attachment to the housing are 7.0 mm too short to reach the housing at all.

### Provenance

- Measured on `cad/exports/*_r9.*`, mtime **2026-08-07 15:46:23/24**.
  `md5(dispenser_r9_assembly.step) = 5b8714bfb9f5af10b3cc9ce0e23f0f92`,
  `md5(retaining_plate_chute_r9.step) = 4472b978f3e4672b2272c36ae819a11f`,
  `md5(retaining_plate_chute_r9.stl) = 5a4463f1d97608ec150ccd2438f0e2b6`,
  `md5(meter_housing_r9.step) = 072fcbc1b7dec083b7ac4a9e64bcb7b8`,
  `md5(pocket_disc_r9.step) = 08165cb66a1e51a439f0bab89a9299b1`,
  `md5(top_plate_r9.step) = d50301b2eed19e4016a83d1d20ed9406`,
  `md5(fill_cap_r9.step) = 3a7eed6e2874f94977be3a19a9a8ac7b`,
  `md5(sensor_cover_r9.step) = 66211a1a8c6392b9505fdfff06c172f6`,
  `md5(electronics_bay_r9.step) = bda844d4629b19d37518fed7b3cc2b37`.
- **`_run/rev1/BUILD-NOTES-r3.md` does not exist** at the time of writing
  (checked 15:56, 16:11 and 16:30 CDT; the directory holds only
  `BUILD-NOTES-r2.md`). I could not cross-check the builder's round-3 claims,
  so **every number below is my own probe** on the exports, which is what the
  tasking asks for in any case.
- All obstruction volumes are **exact OCC booleans** on the STEP bodies
  (`build123d.import_step` + `BRepAlgoAPI_Common` + `BRepGProp`), not voxel
  estimates. Ray probes are trimesh on the STLs. venv
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`, build123d 0.11.1,
  trimesh 5.0.0, numpy 2.5.1.
- COTS bodies were identified in `dispenser_r9_assembly.step` by volume/bbox
  match against the part exports; the six unmatched solids (clip plate 11.523,
  motor+gearbox 69.936, bearing 1.495, blind-mate PCB 1.174, thrust washer
  0.317, brush strip 0.312 cm³) are identified from size and position — an
  **ASSUMPTION**, unchanged from rounds 1–2.
- Convention: "approach from +Z" means the part starts 40–60 mm above its seat
  and **travels −Z**. Because a straight-line path is reversible, the same
  station table is both the install and the removal check.

### 0. Part inventory, static interference, export integrity

```
PART EXPORTS (r9), STEP volumes:
  agitator                nsol=1 V=  4.291cm3   bay_lid           nsol=1 V=  8.785cm3
  brush_holder            nsol=1 V=  3.544cm3   chute_plug        nsol=1 V=  7.120cm3
  count_windows           nsol=4 V=  0.104cm3   electronics_bay   nsol=1 V= 21.175cm3
  fill_cap                nsol=1 V=  7.349cm3   hopper            nsol=1 V=108.849cm3
  meter_housing           nsol=1 V=103.659cm3   pocket_disc       nsol=1 V= 72.686cm3
  retaining_plate_chute   nsol=1 V= 69.502cm3   sensor_boards     nsol=2 V=  1.222cm3
  sensor_cover            nsol=2 V=  3.206cm3   service_stand     nsol=1 V=103.908cm3
  top_plate               nsol=1 V= 95.780cm3   TOTAL printed = 611.179 cm3

ALL-PAIRS EXACT BOOLEAN INTERFERENCE (assembly STEP, 24 solids, 276 pairs):
  44 bbox-overlapping pairs boolean-checked, 0 with non-zero intersection
```

Export integrity, re-measured independently (trimesh, `process=True`):

```
  agitator              watertight=True  euler=  2 nonmanifold=0 bodies=1 V=  4.288cm3
  bay_lid               watertight=True  euler=-10 nonmanifold=0 bodies=1 V=  8.785cm3
  brush_holder          watertight=True  euler=  0 nonmanifold=0 bodies=1 V=  3.544cm3
  chute_plug            watertight=True  euler=  4 nonmanifold=0 bodies=2 V=  7.118cm3
  count_windows         watertight=True  euler=  8 nonmanifold=0 bodies=4 V=  0.104cm3
  electronics_bay       watertight=True  euler= -8 nonmanifold=0 bodies=1 V= 21.175cm3
  fill_cap              watertight=True  euler=  0 nonmanifold=0 bodies=1 V=  7.347cm3
  hopper                watertight=True  euler=-14 nonmanifold=0 bodies=1 V=108.853cm3
  meter_housing         watertight=True  euler=-12 nonmanifold=0 bodies=1 V=103.623cm3
  pocket_disc           watertight=True  euler=-30 nonmanifold=0 bodies=1 V= 72.661cm3
  retaining_plate_chute watertight=FALSE euler=-58 nonmanifold=4817 bodies=1 V= 75.315cm3
  sensor_boards         watertight=True  euler=  4 nonmanifold=0 bodies=2 V=  1.222cm3
  sensor_cover          watertight=True  euler= -4 nonmanifold=0 bodies=2 V=  3.206cm3
  service_stand         watertight=True  euler=  0 nonmanifold=0 bodies=1 V=103.892cm3
  top_plate             watertight=True  euler=-36 nonmanifold=0 bodies=1 V= 95.755cm3
  parts watertight: 14/15
  dispenser_r9_assembly.stl: watertight=False, bodies=20 (for 24 solids)
```

See **BLOCKING A-8**.

### 1. Derived assembly order, with the swept-volume obstruction numbers

Each row is a 21–26-station straight approach, exact boolean against every
already-installed solid; the "SWEPT" column is a true fused union of the
intermediate poses booleaned against those same obstacles. Primes are the
opposite approach, printed to show the order is forced rather than assumed.

| # | Operation | Approach | Station-max over the path | Swept-union ∩ obstacles | Seated | Verdict |
|---|---|---|---|---|---|---|
| 1 | `meter_housing` in fixture | — | — | — | — | datum |
| 2 | igus JFM-2023-07 into the roof bore | **+Z**, 40 mm | **0.0000** | 17202.6 mm³ ∩ = **0.0000** | 0.0000 | OK |
| 2′ | (same, from below) | −Z | 580.5963 at t = 6 | ∩ = 2073.4860 | — | not possible |
| 3 | `brush_holder` + `brush_strip` radial slide-in | **θ = 148°, inboard**, 40 mm | **0.0000** | 11147.5 ∩ = **0.0000** | 0.0000 | OK |
| 3′ | (same, on the r6 wiper angle θ = 133°) | inboard | 188.7355 at t = 24 | ∩ = 214.7502 | — | wrong angle, printed as the control |
| 4 | `pocket_disc`, hub up through the bearing | **−Z (travels +Z)**, 40 mm | **0.0000** | 276157.3 ∩ = **0.0000** | 0.0000 | OK |
| 4′ | (same, from above) | +Z | 29564.7928 at t = 12 | ∩ = 29707.9371 | — | not possible |
| 5 | `agitator` onto the Ø15 hex | **+Z**, 40 mm | **0.0000** | 43462.0 ∩ = **0.0000** | 0.0000 | OK |
| 6a | `count_windows` ×2/side, pushed **out** from the chute bore | radial out, 12 mm | **0.0000** | 675.3 ∩ = **0.0000** | 0.0000 | OK |
| 6b | `sensor_boards` ×1/side into the cavity | **±Y inboard**, 20 mm | **0.0000** | 4995.2 / 4867.2 ∩ = **0.0000** | 0.0000 | OK |
| 6c | `sensor_cover` ×1/side | **±Y inboard**, 25 mm | **0.0000** | 19520.2 ∩ = **0.0000** | 0.0000 | **OK — A-6 closed** |
| 6d | motor+gearbox onto the plate | **−Z (travels +Z)**, 40 mm | **0.0000** | 116580.7 ∩ = **0.0000** | 0.0000 | OK |
| 6e | PTFE thrust washer into its plate counterbore | **+Z**, 20 mm | **0.0000** | 4840.6 ∩ = **0.0000** | 0.0000 | OK |
| 6e′ | (washer fitted from below, with the motor) | −Z | 316.6725 at t = 3 | ∩ = 677.4530 | — | not possible — the washer is **not** part of the motor sub-assembly |
| 7 | drive cartridge (plate+motor+2 covers+2 boards+4 windows) into the housing at −20…−24° of unlock | **−Z (travels +Z)**, 60 mm | **0.0000 vs the housing**; 4.2552 / 4.6955 / 5.1242 vs `pocket_disc` at the seat (−20/−22/−24°) | — | see NB-3 | OK with the disc counter-indexed |
| 7′ | (same at 0° / −14° / −18° / −26°) | +Z | 212.5047 / 108.5068 / 30.2908 / 53.0289 | — | — | not possible |
| 7b | rotate the cartridge −22° → 0° to lock | rot | **0.0000 vs `meter_housing` over the whole −24.514…+0.514° band**; residual 5.1242 max is `pocket_disc` clocking only | — | 0.0000 | OK |
| 8 | M3×6 stop pin, radial at θ = 51°, z = −353.25 | radial in | pin ∩ plate = **0.0000**, pin ∩ housing = 4.3112 (Ø3.0 in a Ø2.6 thread-forming pilot) | — | — | OK |
| 9 | M3×4 grub, radial θ = 202.5°, z = −341.25 | radial in | continuous **Ø2.6 void r 2.75 → 52 = 0.0000** in *both* disc and housing | — | — | OK |
| 10 | `electronics_bay` onto the housing ribs | **−Y**, 40 mm | **0.0000** | 161186.8 ∩ = **0.0000** | 0.0000 | geometry OK, **fastener fails — A-9** |
| 11 | `bay_lid` | **−Y**, 30 mm | **0.0000** | 108/0.0 ∩ = **0.0000** | 0.0000 | OK, removable in situ |
| 11′ | (lid pushed inboard) | +Y | 4028.4361 at t = 27 | ∩ = 18934.7231 | — | not possible, as designed |
| 12 | `hopper` down over the bay riser | **+Z**, 60 mm | **0.0000** | 824844.9 ∩ = **0.0000** | 0.0000 | OK |
| 13 | `top_plate` onto the hopper flange | **+Z**, 40 mm | **0.0000** | 850776.8 ∩ = **0.0000** | 0.0000 | OK |
| 14 | clip plate + blind-mate PCB (COTS interface) | **+Z**, 30 mm | **0.0000** | 86869.8 ∩ = **0.0000** | 0.0000 | OK |
| 15 | `fill_cap` — rotate 90°, lift 12 mm, translate +Y 60 mm | 3 legs | see §3 | 38.7708 / 1.6059 / **0.0000** | 0.0000 | **OK — A-5 closed** |
| 16 | `chute_plug` (ground only) | +Z | 189.1262 at the seat | — | 189.1262 | designed 0.3 mm press fit |
| 17 | `service_stand` (ground only) | — | ∩ every assembly solid = **0.0000** | — | — | OK |

Every one of the 15 exported printed parts appears in that order.

**Cartridge service removal with the whole machine built** (members = plate +
motor + washer + 2 covers + 2 boards + 4 windows; obstacles = clip plate,
top plate, fill cap, hopper, housing, disc, bearing, agitator, brush holder,
brush strip, bay, lid, blind-mate PCB):

```
  unlock -20 deg + 60 mm descent : station-max 4.2552 mm3  (all of it pocket_disc, at the seat)
  with pocket_disc counter-indexed -20 deg : station-max 0.0000 mm3
```

The documented drop-out path is real and is **0.0000 mm³** once the disc is
counter-indexed (NB-3, a procedure item — the disc is free in the bearing until
the grub is torqued).

### 2. Torque path — motor → gearbox → shaft → metering disc: **EXISTS and closes**

Every number below is measured on the r9 exports; the shaft profile is a
first-hit (nearest-surface) radial ray sweep at 1°, not a max-radius sweep
(a max-radius sweep hides a D-flat and reports a plain Ø6 shaft).

```
 gearbox/motor solid       V = 69.936 cm3, bb z -418.450 .. -337.250
 motor can                 r_max = 20.846 (35 x 35 body), z -418.45 .. -384.45
 gearbox body              r = 18.000            z -384.45 .. -355.25
 output flange face        z = -355.250
 output pilot boss         r =  8.000            z -355.25 .. -353.20   (Dia16.00, ASSUMPTION)
 output shaft              r =  3.000            z -353.20 .. -337.25   (15.950 mm exposed)
 shaft D-FLAT              r =  2.500 over theta 171..234 (64 deg), z -349.250 .. -337.250 = 12.000 mm

 disc D-BORE               r = 3.049..3.050 round; FLAT r = 2.550 over theta 171..234 (64 deg)
 disc bore flat starts     z = -349.2500 (bisection to 1e-4), runs to the shaft top -337.250
 FLAT-ON-FLAT overlap      12.000 mm ; flat chord 2*sqrt(3.0^2 - 2.55^2) = 3.161 mm
 flat bearing area         12.000 x 3.161 = 37.93 mm2
 drive torque              0.14 N*m x 5.18 x 0.90 = 0.6527 N*m   (model's own constants)
 tangential force          261.1 N at r = 2.5 mm -> bearing stress 6.88 MPa on CF-PETG

 grub, disc pilot   Dia2.6, r 2.75 -> 9.00,  theta 202.5, z -341.25 : disc 0.0000
 grub, disc channel Dia3.4, r 9.00 -> 46.00                          : disc 0.0000, housing 0.0000
 grub, housing port Dia3.6, r 46.0 -> 52.0                           : housing 0.0000
 B2.2 CONTINUOUS Dia2.6 void, r 2.75 (bore wall) -> 52 (outside the housing) = 0.0000 / 0.0000
 B2.3 driver access Dia3.4 x 25 mm on the grub axis vs EVERY other solid   = 0.0000

 disc -> agitator          Dia15 hex spigot, seated 0.0000
 bearing seat bore         Dia 23.023 .. 23.030 (igus JFM-2023-07 OD 23.00) -> B9d target <= 23.03 MET
 thrust stack              washer top -350.800, disc bottom -350.750 -> 0.050 mm
 shaft end / bore blind    shaft top -337.250, disc bore ceiling -335.750 -> 1.500 mm  (r8: 0.000 — NB-1 CLOSED)
```

**B2.1, B2.2, B2.3 pass on the exports.** Torque is carried
motor → 5.18:1 planetary → Ø6 shaft flat (12.000 mm engaged, 37.93 mm²,
6.88 MPa) → disc D-bore → disc → Ø15 hex → agitator.

**The reaction path now exists too (A-7 closed).** Disc travel direction,
re-derived independently from the housing export (roof underside above the disc
land, r = 32, land plane z = −336.750):

```
  theta  85 -> 1.500   90 -> 1.500   95 -> 1.500  100 -> 2.687  105 -> 3.989  110 -> 5.291
       115 -> 6.593  120 -> 7.896  125 -> 9.198  130 -> 10.500  135..250 -> OPEN (fill window)
       255 -> 7.707  260 -> 4.915  265 -> 2.122  270..80 -> 1.500
```

The entry ramp descends 10.500 → 1.500 mm from θ = 130 to θ ≤ 95, so pockets run
**−θ** and the gearbox's stator reaction on the plate is **+θ**. Free-rotation
scan of the seated cartridge against `meter_housing` (exact boolean, 1°, then
bisected to 1e-4°):

```
  -36..-25 : 369.573 .. 11.692     -24 .. 0 : 0.000 (free)     +1 : 11.692   +2 : 47.487
  +theta first contact  +0.51416 deg   (free to +0.51410)
  -theta first contact -24.51416 deg   (free to -24.51410)
  two-sided free band = [-24.5141, +0.5141] = 25.0282 deg
  contact lump at +1.0 deg: 11.6919 mm3, bb z -355.25..-351.25 (the full 4.0 mm plate flange)
  contact lump at +2.0 deg: 47.4874 mm3
```

The handedness has been mirrored relative to r8: the hard circumferential stop
is now **in +θ, the drive-reaction direction, and engages after 0.5141° of lash**
(r8: the stop was in −θ and there were 24.65° of free travel in +θ ending in the
drop-out window). Effective stop bearing area from dV/dδ between +1° and +2°
(ΔV = 35.7955 mm³ over 0.017453 rad at r ≈ 53.8 mm → 0.939 mm of penetration):
**≈ 38.1 mm²**; the reaction force is 0.6527 N·m / 0.0538 m = **12.13 N**, i.e.
**0.32 MPa** on the lug faces. That closes with an enormous margin, against
r8's 9.6× *deficit*.

The remaining −θ freedom is closed by the new **M3×6 radial stop pin** at
θ = 51.0°, z = −353.25 (pilot verified on the export: bore radius **1.300 mm**
= Ø2.60 measured perpendicular to the axis at r = 56):

```
  modelled M3x6 pin (Dia3.0, r 52.8 .. 58.8) ^ meter_housing = 4.3112 mm3 (thread-forming into Dia2.6)
  pin ^ retaining_plate_chute, seated                        = 0.0000 mm3 (0.8 mm clear of the plate rim)
  -theta free to -1.9429 deg, first contact -1.9430 deg
  BOUNDED free band with the pin fitted = [-1.9429, +0.5141] = 2.4570 deg   (without it: 25.0282 deg)
  drop-out window (axial descent free) is at -20 .. -24 deg -> the pin blocks it by 18.1 deg
  tool access to the pin: >= Dia12.0 clear over 30 mm radially outward
```

### 3. `fill_cap` — A-5 closed

Round 2's blocker was measured about the wrong axis by the *builder's* stated
FILL_POS as well as by me; the cap's true axis is **(0, 43.000)**, recovered
from the export (plug outer radius = 22.700 constant to ±0.001 at every 1°
about that point). About the true axis the cap is a working bayonet:

```
 plug outer radius (z = -239.0, 0.5 deg sweep): 22.700 with two NOTCHES to r = 19.600
     theta  80.0 .. 100.0 deg (20.5 deg wide)   and   260.0 .. 280.0 deg (20.5 deg)
 top_plate port bore r = 23.000 with two inward TABS to r = 20.000
     theta 351 .. 9 deg (19 deg)                and   171 .. 189 deg (19 deg)
 -> unlock rotation = 90 deg; radial engagement when locked = 22.700 - 20.000 = 2.700 mm

 rotation about (0,43.0) at the seated height, cap ^ top_plate:
     rot   0 -> 0.0000      rot 15..180 -> 1.4338 CONSTANT      cap ^ hopper = 0.0000 at every angle
     (the constant 1.4338 mm3 is the anti-rotation detent boss, a 1.471 x 1.471 x 2.5 mm
      lump at x -20.167..-18.696, y 61.696..63.167, z -236.35..-233.85, r = 27.5)
 lift at rot 0 (locked): 0.0000 at 0.10 mm, 32.8827 peak at 1.00-1.50 mm (the tabs), 0.0000 from 2.50 mm
 lift at rot 90 (unlocked): 1.4338 -> 0.1721 over 0..2.5 mm, 0.0000 from 4.00 mm
 straight lift WITHOUT rotating fouls the B6 neck: 9.2987 mm3 at 16 mm rising to 613.4035 at 52 mm

 3-LEG REMOVAL / FIT:
   leg 1  rotate 0 -> 90 deg   : union 8290.7 mm3 ^ top_plate =  38.7708 ; ^ hopper 0.0000 ; ^ clip 0.0000
   leg 2  lift 12 mm at rot 90 : union 34982.1 mm3 ^ top_plate =  1.6059 ; ^ hopper 0.0000 ; ^ clip 0.0000
   leg 3  translate +Y 60 mm   : union 28638.1 mm3 ^ top_plate =  0.0000 ; ^ hopper 0.0000 ; ^ clip 0.0000
```

Required travel: **90° of rotation + 12.0 mm of lift + 60 mm of +Y translation.**
The only non-zero residual is the anti-rotation detent (peak 1.4338 mm³
instantaneous, 38.7708 mm³ over the whole rotation sweep) — that is N5's
feature working, but it means B12.2's literal "0.000 mm³" is **not** met and
the notes must say so rather than claiming zero (NB-6).

### BLOCKING A-8 — `retaining_plate_chute_r9.stl` is not a valid mesh (regression from r8)

```
  r7 : watertight=False winding_consistent=True  euler=-41 nonmanifold=  12 V=45.822 cm3 faces=22212
  r8 : watertight=True  winding_consistent=True  euler=-66 nonmanifold=   0 V=57.980 cm3 faces=31284
  r9 : watertight=False winding_consistent=FALSE euler=-58 nonmanifold=4817 V=75.315 cm3 faces=35419
       open (count-1) edges: 188
       open-edge bbox: [ 38.5, -32.5, -416.8] -> [ 43.5, -22.5, -411.8]
  STEP volume of the same part: 69.5024 cm3  ->  the STL over-reads by +5.8126 cm3 = +8.36 %
  the STEP is clean: 1 solid, and the defect box holds 250.0000 mm3 of material,
  exactly matching its +Y mirror box (250.0000 mm3) -- so this is a tessellation
  failure in the export, not a modelling error
  knock-on: dispenser_r9_assembly.stl is watertight=False with 20 bodies for 24 solids
```

B10 requires "10/10 part STLs watertight, assembly … 0 non-manifold edges". r9
reads **14/15 and 4817**. Consequences beyond B10: any mass, CG or slicer
statistic taken from that STL is 8.36 % high on the single largest structural
printed part (88.3 g at STEP volume), the assembly STL cannot be used for
mesh-to-mesh clearance work, and the region that fails is the −Y harness-duct
leg that B5 introduced. The STEP is usable, which is why every number in this
critique is a STEP boolean.

### BLOCKING A-9 — the electronics bay's only two fasteners are 7.0 mm too short to reach the housing

`cad/BOM.md` fastener table: `2 | M3x12 SHCS | electronics bay ribs -> housing`.
That is the bay's *only* attachment (the 4 × M3x8 self-tap are lid → bay, and
the 3 × M3x8 Delta-PT are the hopper skirt tabs). Measured on the exports along
the screw axis x = ±14.0, z = −337.100:

```
 electronics_bay along +Y at x=16.5 : material  y = -64.000 .. -49.415  (the rib boss)
 electronics_bay along +Y at x=18.0 : material  y = -64.000 .. -62.000  (the 2 mm bay wall)
 electronics_bay ON AXIS (x=14.0)   : NO crossings -> a clean through-bore
 radial clearance on the axis       : 1.600 mm (Dia3.200) uniformly from y = -64.0 to y = -50.0,
                                      3.699 mm at y = -49.0, open at y = -48.0
                                      -> NO counterbore anywhere: the head can only bear at y = -64.000
 meter_housing wall on the axis     : outer surface y = -50.080, inner surface y = -44.866 (r=52 / r=47 at x=14)
 meter_housing pilot                : Dia2.5, y = -52.000 .. -45.000; residual material on axis
                                      y = -45.000 .. -44.861 (0.139 mm) -> usable thread y -50.080 .. -45.000
 GRIP  (head face -64.000 to the first threadable material -50.080)  = 13.920 mm
 M3x12 tip lands at y = -52.000  ->  1.920 mm SHORT of touching the housing
 THREAD ENGAGEMENT ACHIEVED = 0.000 mm  (available if the screw were long enough: 5.080 mm)
 REQUIRED LENGTH for full engagement = 64.000 - 45.000 = 19.000 mm  -> M3x20
```

So the bay — which houses the control PCB and, per B5, is a sealed structural
enclosure — is **not attached to anything** with the hardware the BOM specifies.
Tool access is not the problem and is good: the driver corridor from the head
plane y = −64.05 outward is **≥ Ø12.0 over 28 mm with the lid off** and
**Ø6.0 with the lid fitted** (first blocking Ø8.0 → 74.7699 mm³ of `bay_lid`),
which also closes round 2's NB-2 (the r8 lid's Ø6 holes were stopped by a
0.400 mm membrane and read Ø0.0). The fix is a BOM line change plus a re-print
of this grip number; the geometry itself is fine.

### 4. Tool-access corridors — largest clear driver diameter per fastener

Method unchanged from rounds 1–2: a cylinder on the fastener axis starting at
the head-bearing plane and extending **away** from the joint, diameters stepped
1.5/2.0/2.5/3.0/3.4/4.0/5.0/6.0/8.0/10.0/12.0 mm; the largest diameter with a
**0.0000 mm³** exact boolean against every other assembly solid is reported.

| ref | fastener | corridor | max clear driver | first blocking size → volume |
|---|---|---|---|---|
| F1 | 4 × M3x8 gearbox screws, +Z, **in situ** | 25 mm | **Ø0.0** | Ø1.5 → **15.7276** (`meter_housing` 12.7235 + `bearing` 3.0041) |
| F1b | same four, **plate+motor sub-assembly** | 25 mm | **Ø8.0** | Ø10.0 → 2.1304 (thrust washer) |
| F2 | M3x4 grub, key from the disc OD outward (r 46 →) | 25 mm | **Ø3.4** | Ø4.0 → 11.9429 (`meter_housing`) |
| F2b | M3x4 grub, hand space outboard (r 53 →) | 40 mm | **Ø4.0** | Ø5.0 → 5.1053 (`meter_housing`) |
| F3 | M5 ball plunger, radial from r = 63 outward (θ = 67.5) | 30 mm | **≥ Ø12.0** | — |
| F3b | **M3x6 stop pin**, radial from r = 58.8 (θ = 51) | 30 mm | **≥ Ø12.0** | — |
| F4 | 3 × M3x8 skirt tabs, θ = 30/105/225, radial | 25 mm | **≥ Ø12.0** each | — |
| F5 | M3x6 wiper end tab, radial from r = 58.1 (θ = 148) | 25 mm | **≥ Ø12.0** | — |
| F6 | 2 × M3x12 bay ribs, −Y from the head plane y = −64.05 | 28 mm | **Ø12.0** (lid off) / **Ø6.0** (lid on) | lid on: Ø8.0 → 74.7699 (`bay_lid`) |
| F7 | 4 × M3x8 bay-lid screws, −Y from y = −92.5 | 25 mm | **≥ Ø12.0** each | — |
| F8 | 6 × M3x10 flange screws, r = 74, θ = 15+60k, +Z | 25 mm | **≥ Ø12.0** each | — |
| F9 | 4 × M2x10 mount screws (±19, ±19), +Z | 30 mm | **Ø4.0** | Ø5.0 → 12.7641 (`clip_plate`'s own head pocket) |
| F10 | 4 × M2x6 sensor-cover screws, x = 34.5, z = Z_SENSOR ± 12, ±Y | 25 mm | **≥ Ø12.0** (upper) / **Ø6.0** (lower) | lower: Ø8.0 → 10.6622 / 10.6625 (`retaining_plate_chute`) |

Readings that matter:

- **F1 in situ = Ø0.0**, third round running: once the machine is together the
  four gearbox screws are buried under the disc, the bearing and the housing
  roof. The motor is fastenable and removable **only as the plate+motor
  cartridge** (Ø8.0 there), which the quarter-turn latch exists to permit. "The
  motor is not field-replaceable in place" is a fact of this design and belongs
  in the service section; there is no round-3 build note to check it against.
- **F9 = Ø4.0 over 30 mm** for the four M2 screws that carry the whole payload
  (r8: Ø2.5) — a real improvement; a stubby driver now fits.
- **F10 ear screws exist and line up**: `sensor_cover` clearance hole radius
  **1.1496…1.1500 mm** (Ø2.30) and `retaining_plate_chute` pilot radius
  **0.79974…0.80000 mm** (Ø1.60) on the same axis x = 34.5, z = −383.250 /
  −407.250. ECO-12 retention is real hardware, not a BOM line for a hole that
  does not exist.

### 5. Non-blocking, measured

- **NB-1 (new) — the M3×6 stop pin is not in `cad/BOM.md`.** It is the entire
  positive lock for A-7: with it the free band is **2.4570°**, without it
  **25.0282°** with the far end sitting in the drop-out window. `dispenser.py`
  L1366-1379 builds its pilot and L3493-3496 prints it, but the fastener table
  in `cad/BOM.md` (checked at 15:55, rev r9) has no stop-pin row. A part that
  cannot be ordered will not be fitted.
- **NB-2 (new) — skirt-tab screws bottom out.** θ = 30° axis, z = −330.25:
  hopper skirt tab is a through-hole (no crossings on axis); housing pilot runs
  **r 52.000 → 47.900 = 4.100 mm deep**; head bears at the tab outer face
  **r = 55.150** → grip **3.150 mm**. An **M3x8** therefore presents
  **4.850 mm** of thread to a **4.100 mm** pilot and bottoms out **0.750 mm**
  before it clamps. Either deepen the pilot to ≥ 5.2 mm or specify M3x7.
- **NB-3 — clocking is a procedure fact, not geometry.** Cartridge insertion
  reads **4.2552 / 4.6955 / 5.1242 mm³** against `pocket_disc` at −20/−22/−24°
  of unlock (the shaft D-flat against the disc D-bore flat at the wrong relative
  angle) and **0.0000** with the disc counter-indexed by the same angle. Same
  for the lock rotation: 0.0000 vs the housing over the whole −24…+0.5° band,
  and a 5.1242 mm³ maximum that is entirely disc clocking.
- **NB-4 — 0.5141° of plate-to-housing lash** at the drive-reaction stop. On a
  22.5° index that is **2.29 %** of one station of angular error the first time
  the drive loads up in each direction; the magnet index has to absorb it. Worth
  one sentence in the count-contract text, not a geometry change.
- **NB-5 — service-stand clearance is 8.000 mm, not 16.20 mm.**
  `service_stand` ∩ every assembly solid = **0.0000 mm³**; stand ground plane
  Z = −426.450; **lowest solid in the assembly = the motor can at Z = −418.450**
  (the lowest *printed* material is `retaining_plate_chute` at −418.300). r8's
  published 16.20 mm was measured against the wrong body; the number to publish
  is 8.000 mm.
- **NB-6 — B12.2's "0.000 mm³" is not literally met for the fill cap.** The
  rotation leg carries the anti-rotation detent: 1.4338 mm³ instantaneous,
  38.7708 mm³ over the swept union. That is a designed elastic feature (N5) and
  I accept it, but the notes must print it rather than claim zero (RT-19).
- **NB-7 — grub handling** (carried unchanged from rounds 1–2): the M3×4 grub
  must be pushed **43.00 mm** radially (housing outer face r = 52 → pilot r = 9)
  down a Ø3.4 channel with the disc first indexed to **θ = 202.5°** so the flat,
  the pilot and the port line up; there is no retrieval path if it is dropped in
  the chamber, and a ≥ 60 mm 1.5 mm hex key is still not a BOM line.
- **NB-8 — no round-3 build notes exist**, so none of the three procedure facts
  the drive depends on (F1 = Ø0.0 sub-assembly-only motor; disc indexed to
  θ = 202.5° for the grub; disc counter-indexed to the unlock angle for
  cartridge insert/remove) is written down anywhere, and the round's own
  measurements cannot be cross-checked against a builder's claim. This was
  round 2's item 4 and it is still open.
- Outside my lane, noted in passing because I read the file: `cad/BOM.md`
  (rev r9) rolls up **"loaded @250 pellets: 1582.9 g (ceiling 1500 g)"** — B11
  is over budget by 82.9 g on the shipped headline basis.

### 6. What I need to see next round to clear "assembly"

1. `retaining_plate_chute_r9.stl` re-exported watertight: **0 open edges,
   0 non-manifold edges, winding consistent, and STL volume within 0.5 % of the
   STEP's 69.5024 cm³** (today: 188 / 4817 / False / +8.36 %), and the assembly
   STL watertight with one body per solid.
2. The bay→housing screw length corrected and the grip re-printed:
   **head plane − first threadable material = 13.920 mm, engagement ≥ 4.0 mm,
   screw length ≥ 18.0 mm** (today: M3x12 → 0.000 mm of engagement, tip 1.920 mm
   short of the housing).
3. `cad/BOM.md` fastener table carrying the **M3×6 stop pin** row, and the
   skirt-tab pilot depth or screw length reconciled (today: 4.100 mm pilot vs
   4.850 mm of thread).
4. The three procedure facts in the build notes, quoted from tool output.
5. Everything in §1, §2 and §3 re-printed unchanged — those are the numbers that
   closed A-5, A-6, A-7, NB-1 (shaft end 1.500 mm), NB-2 (lid Ø6 through) and
   the torque path, and none of them may regress.
