# REV-1 ROUND 5 — CRITIQUE (exports `r11`)

## count-sensor

**Verdict: PASS WITH COMPLAINTS.** RT-3 is closed in geometry — the counting
hardware ELECTRONICS §4.2–4.4 requires is physically in `retaining_plate_chute_r11`
plus three new part files (`count_windows_r11`, `sensor_boards_r11`,
`sensor_cover_r11`). Nothing on my list is spec'd-but-not-modelled. Two real
defects survive, both non-blocking and both cheap to fix: the ECO-5 labyrinth is
offset in the **same** x-sense on both sides, which walks the effective optical
chord 0.400 mm off the ECO-3 axis and fails PUNCHLIST B4.2 as written
(1.1932 mm³, not 0.0000); and the count-sensor Z in `ELECTRONICS.md` §4 is stale
by 49.1 mm, which shifts every dark-time number in §4.2/§4.3.

Method: measured by me on the shipped exports, not read from `BUILD-NOTES-r5.md`
or from `dispenser.py`. Tools: `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`,
trimesh 5.0.0 (mesh sectioning + ray casting on the STLs), build123d 0.11.1 /
OCC (exact booleans on the STEPs), numpy 2.5.1. Every number below is tool
stdout. Files measured:
`retaining_plate_chute_r11.stl/.step` (vol 71849.9259 mm³ STL / 71867.2529 mm³ STEP,
watertight True), `count_windows_r11`, `sensor_boards_r11`, `sensor_cover_r11`,
`dispenser_r11_assembly.stl` (24 bodies), `cad/BOM.md`.

---

### B4.1 — aperture count and position: **PASS**

Four tunnels, two per side, found by ray-casting along ±y over a 0.20 mm (x,z)
grid across x 20…46, z −406…−385 and by planar sectioning; I did not tell the
probe where to look.

Zero-crossing (open end-to-end) clusters over that grid — only two, plus one
artefact below the boss:

```
 cluster 2: cells 135  x 34.40..36.40 (c 35.400, span 2.20)  z -399.60..-396.80 (c -398.200, span 3.00)
 cluster 3: cells 135  x 28.40..30.40 (c 29.400, span 2.20)  z -393.60..-390.80 (c -392.200, span 3.00)
```

Inner-segment tunnel cross-sections (mesh sections, both sides):

```
  y= +13.0 beam A: x 27.400..30.600 (c 29.000, w 3.200)  z -393.850..-390.650 (c -392.250, h 3.199)
  y= +13.0 beam B: x 33.400..36.600 (c 35.000, w 3.200)  z -399.850..-396.650 (c -398.250, h 3.199)
  y= -13.0 beam A: x 27.400..30.600 (c 29.000, w 3.200)  z -393.850..-390.650 (c -392.250, h 3.199)
  y= -13.0 beam B: x 33.400..36.600 (c 35.000, w 3.200)  z -399.850..-396.650 (c -398.250, h 3.199)
```

Axis rays, and the controls that prove the probe is not simply missing:

```
  beam A nominal axis        x= 29.00 z= -392.250: NO SOLID POINT (clear end to end)
  beam B nominal axis        x= 35.00 z= -398.250: NO SOLID POINT (clear end to end)
  CONTROL boss between apertures  x= 32.00 z= -392.250:  -17.000 -12.000 -11.000  11.000  12.000  17.000
  CONTROL A-x at B-height         x= 29.00 z= -398.250:  -17.000 -10.582  10.582  17.000
  CONTROL B-x at A-height         x= 35.00 z= -392.250:  -17.000 -10.583  10.583  17.000
```

| ECO-3/ECO-9 spec | measured (r11) | verdict |
|---|---|---|
| 2 apertures/side, 4 total | 4 (2/side, 2 collinear pairs) | PASS |
| axes x = 29 and x = 35 | 29.000 and 35.000 (inner segment) | PASS |
| Ø3.2 ± 0.1 | 3.200 × 3.199–3.200 | PASS |
| z = Z_SENSOR + 3.0 / − 3.0 | −392.250 / −398.250 | PASS |
| **ECO-9 vertical stagger 6.0 mm** | **6.000 mm exactly** | PASS |

### B4.2 — Ø2.0 × 60 mm beam-clearance cylinder: **FAIL as written** (non-blocking)

Exact OCC intersection against `retaining_plate_chute_r11.step`:

```
  A nominal x=29.0     Dia2.0=   1.1932  Dia2.2=   2.3085  Dia2.4=   3.7347  Dia2.6=   5.4739  Dia2.8=   7.5340  Dia3.0=   9.9265  Dia3.2=  12.6654
  B nominal x=35.0     Dia2.0=   1.1932  Dia2.2=   2.3085  Dia2.4=   3.7347  Dia2.6=   5.4739  Dia2.8=   7.5340  Dia3.0=   9.9265  Dia3.2=  12.6654
  A lens ctr x=29.4    Dia2.0=   0.0000  Dia2.2=   0.0000  Dia2.4=   0.0000  Dia2.6=   1.3728  Dia2.8=   4.0819  Dia3.0=   7.8809  Dia3.2=  12.7540
  B lens ctr x=35.4    Dia2.0=   0.0000  Dia2.2=   0.0000  Dia2.4=   0.0000  Dia2.6=   1.3728  Dia2.8=   4.0819  Dia3.0=   7.8809  Dia3.2=  12.7540
CONTROL solid boss x=32   Dia2.0: 32.9966
CONTROL A-x at B-height   Dia2.0: 40.3982
```

Against every other solid on the path:

```
  A x=29.0   Dia2.0x60: plate   1.1932  cover   0.2364  boards  44.6106  windows(PMMA, transparent)   5.9690
  B x=35.0   Dia2.0x60: plate   1.1932  cover   0.0000  boards  44.6106  windows(PMMA, transparent)   5.9690
  A x=29.4   Dia2.0x60: plate   0.0000  cover   0.0000  boards  44.6106  windows(PMMA, transparent)   5.9690
  B x=35.4   Dia2.0x60: plate   0.0000  cover   0.0000  boards  44.6106  windows(PMMA, transparent)   5.9690
  A x=29.8   Dia2.0x60: plate   1.1908  cover   0.0000  boards  44.6106  windows(PMMA, transparent)   5.9690
```

(the 44.6106 mm³ against `sensor_boards` is the emitter/detector bodies
themselves sitting on the beam — that is correct, not interference. The
5.9690 mm³ against `count_windows` is the PMMA, which is transparent.)

**Root cause, measured.** ECO-5's labyrinth offsets the outer 2.5 mm of the
tunnel **+0.800 mm in x on BOTH the +Y and the −Y boss** (see B4.5). Two Ø3.200
circles offset 0.800 mm intersect in a lens, so the straight-through aperture is
**not Ø3.2 centred on 29.000** — it is a 2.4 mm × 3.2 mm lens centred on
**x = 29.400 / 35.400**:

```
  A dx=-1.00  x= 28.00 z= -392.250:  -17.000  -14.500   14.500   17.000
  A dx=-0.75  x= 28.25 z= -392.250: NO SOLID POINT (clear end to end)
  A dx=+1.50  x= 30.50 z= -392.250: NO SOLID POINT (clear end to end)
  A dx=+1.75  x= 30.75 z= -392.250:  -14.495  -12.000   12.000   14.495
clear lens area (two Dia3.200 circles offset 0.800) = 5.5094 mm2 vs full circle 8.0425 mm2 -> 68.5 %
```

The model itself agrees with my reading, not with the punch list: the modelled
TSAL6200 bodies are centred at **x = 29.800 / 35.800**, i.e. on the *outer*
(offset) tunnel axis, not on ECO-3's 29/35.

**Consequences, quantified** (so this is a complaint with a size, not an adjective):

```
  as-built effective chords x = 29.400 / 35.400 -> -2.600 / +3.400 mm from the bore axis (doc: -3.000/+3.000); separation 6.000 mm
  worst nearest-beam distance for a centre anywhere between the chords = 3.000 mm (unchanged) -> the 4.3 no-miss proof survives
```

1. **§4.3's "a pellet is never missed" proof survives** — it depends on the
   6.000 mm beam *separation*, which is exact, not on symmetry about the bore
   axis. Worst nearest-beam distance is still 3.000 mm.
2. **ECO-9's published size solve is wrong for the as-built chords.** §4.3 gives
   `x₀ = (h_A² − h_B²)/12` for chords at ±3.0. With chords at −2.600/+3.400 it
   becomes `x₀ = (4.800 − (h_A² − h_B²))/12`, and the doc also has beam A on the
   +x side where the geometry puts it on −x. Firmware/document constant, not
   geometry — but it must be corrected or the per-event `r`/`x₀` telemetry is
   biased.
3. **Optical budget is 68.5 % of the modelled aperture** (5.5094 vs 8.0425 mm²),
   i.e. −1.64 dB on §4.4's 182× excess gain. Irrelevant against a 1 µA
   threshold; the §4.4 number is nonetheless optimistic as printed.

**Fix is internal and free:** offset the *inner* segment −0.400 mm and the outer
+0.400 mm (identical 0.800 mm ledge), and the lens re-centres on 29.000/35.000,
B4.2 reads 0.0000 at Ø2.0, and ECO-9's constants become true again.

### B4.3 — boss envelope and motor clearance: **PASS**

```
 z=-392.25: x 19.001..47.000  y -30.500..30.500
    +Y boss verts: x 22.000..47.000  y 12.000..30.500
    -Y boss verts: x 22.000..47.000  y -30.500..-12.000
assembly body 12 (motor/gearbox envelope): x -18.00..18.00  y -18.00..18.00  z -418.45..-337.25
```

- boss x-min = **22.000** (B4.3 asks ≥ 22.0) → **4.000 mm** to the *modelled*
  motor body face at x = 18.000, **4.400 mm** to ECO-3's quoted motor face at
  x = 17.6. B4.3 asks ≥ 4.0; I print the measured number, not the predicted one.
- boss x-max = **47.000**, so the boss is 25.0 mm wide, not ECO-3's
  `Box(20,12,14)` (x 22…42). The extra 5 mm is the sensor cable duct merged into
  the boss and it grows *away* from the motor, so it costs nothing here.
- **Printed anyway (not a count-sensor defect, but it is the real minimum):** the
  chute tube OD at this Z reaches **x = 19.001**, i.e. **1.001 mm** from the
  modelled motor body at x = 18.000. The 4.4 mm ECO-3 headline describes the
  boss, not the closest payload-to-motor pair at that height.

### B4.4 — ECO-4 window seat: **PASS on the requirement, deviates from the literal dimension**

```
count_windows_r11.stl  4 bodies, vol 103.848 mm3 total, watertight True
  body 0 bbox [26.05, 11.00, -395.1991]..[31.95, 11.95, -389.3009] vol 25.9619 centroid [29.000, 11.475, -392.250]
  body 1 bbox [32.05, 11.00, -401.1991]..[37.95, 11.95, -395.3009] vol 25.9619 centroid [35.000, 11.475, -398.250]
  body 2 (mirror, y -11.95..-11.00) ; body 3 (mirror)
seat section: y=11.20 -> Dia5.999 ; y=11.60 -> Dia6.000 ; y=12.00 -> tunnel only (Dia3.200)
ray x=31.00 z=-392.250: -14.495 -12.000 12.000 14.495   (seat floor plane |y| = 12.000)
```

- Window discs **Ø5.900 × 0.950**, seated in a **Ø6.000** counterbore whose mouth
  is the plane **|y| = 11.000** and whose floor is **|y| = 12.000** →
  0.050 mm/side bond gap, 0.050 mm back clearance. Window inner face is the plane
  |y| = 11.000.
- **Nothing proud of the bore**, which is the requirement that matters:

```
  Dia22.0 x 45 column on the chute axis: ^plate 0.0000  ^windows 0.0000  ^boards 0.0000 mm3
  Dia21.0 column:                        ^plate 0.0000  ^windows 0.0000  ^boards 0.0000 mm3
  Dia13.0 column:                        ^plate 0.0000  ^windows 0.0000  ^boards 0.0000 mm3
```

- The seat depth is **1.000 mm**, not B4.4's literal "0.4 ± 0.05 mm". B4.4 as
  written is self-contradictory — a Ø6 × 1 mm disc in a 0.4 mm seat stands
  0.6 mm proud of the bore, which the same test forbids — and the model resolved
  it the only way that keeps nothing proud. What *is* 0.4 mm is the recession of
  the flat window face below the curved bore: at the aperture centre x = 29 the
  Ø22 bore surface is at |y| = 10.583, so the window face at |y| = 11.000 sits
  **0.417 mm** outside it, tangent to the bore at exactly x = 32. Record the
  deviation; do not re-cut the seat to 0.4 mm.
- **No chamfer.** ECO-4 asks for a "0.4 mm **chamfered** recess"; the seat mouth
  measures Ø5.999 at y = 11.20 and Ø6.000 at y = 11.60 — straight-walled, so the
  seat presents a sharp Ø6 edge in the bore wall. Minor; the granule column check
  above is unaffected.
- **The "sacrificial, replaceable" claim is not supported by geometry.** The seat
  is a blind counterbore opening only into the Ø22 chute bore, **26.050 mm**
  (beam A) and **20.050 mm** (beam B) above the chute mouth at Z = −418.300, and
  the Ø3.200 tunnel behind it cannot pass a Ø6 disc. `cad/BOM.md` bonds the disc
  with UV-cure adhesive. So replacement means reaching 20–26 mm up a Ø22 tube or
  destacking `retaining_plate_chute` — a workshop job, not the "10-second
  maintenance action" §4.5 measure 5 describes. **Swabbing** the window from the
  chute exit *is* supported (the face is flush and in the bore wall); only
  *replacement* is not. ELECTRONICS §4.5/ECO-4 should say so.

### B4.5 — ECO-5 labyrinth: **PASS on every dimension, wrong in sense**

```
+Y labyrinth step plane (inner->outer) bisected: y = 14.4950
-Y labyrinth step plane bisected:                y = -14.4950
boss outer face (x=32, z=-392.25) bisected:      y = 17.0000  -> outer segment length = 2.5000 mm
  y=  14.40: A tunnel cx  29.000 w 3.200  cz  -392.250 h 3.200
  y=  14.80: A tunnel cx  29.800 w 3.200  cz  -392.250 h 3.200
  y= -14.40: A tunnel cx  29.000 w 3.200  cz  -392.250 h 3.200
  y= -14.80: A tunnel cx  29.800 w 3.200  cz  -392.250 h 3.200
  (beam B identical: 35.000 -> 35.800 at the same y planes)
```

Outer segment **2.5000 mm** (spec: outer 2.5 mm); offset **0.800 mm**
(spec 0.8 ± 0.1); ledge **0.800 mm** (B4.5 asks ≥ 0.7); present on all four
tunnels. The defect is only that both sides step in **+x**, which is what causes
B4.2 — see above.

### B4.6 — sensor-board cavity: **PASS in function, FAIL as a 20 × 8 × 12 box at x = 32**

```
  20x8x12 at x= 32.0 y= +22.0: ^plate  220.8000  ^cover    0.0000 mm3
  20x8x12 at x= 33.0 y= +22.0: ^plate  124.8000  ^cover    0.0000 mm3
  20x8x12 at x= 34.0 y= +22.0: ^plate   28.8000  ^cover    0.0000 mm3
  20x8x12 at x= 34.5 y= +22.0: ^plate    0.0000  ^cover    0.0000 mm3
  20x8x12 at x= 35.0 y= +22.0: ^plate   28.8000  ^cover    0.0000 mm3
  (identical at y = -22.0)
obstruction decomposed:  220.8000 mm3  x[22.000,24.300] y[19.000,27.000] z[-401.250,-389.250]
```

A clear 20 × 8 × 12 cavity **does** exist — centred at **x = 34.500**, not at
ECO-3's x = 32; at x = 32 it is blocked by the inboard cable-duct wall at
x 22.000…24.300. The as-built architecture is not ECO-3's "component pocket in
the boss" at all: the boards sit **outboard of the boss face (|y| = 17.000)**
under a printed `sensor_cover`. The real hardware fits with zero interference:

```
  board 0 (+Y emitter):  bbox x 25.50..43.50  y 17.50..28.50  z -401.25..-389.25  vol 794.93  ^ plate = 0.0000 mm3
  board 1 (-Y receiver): bbox x 25.50..43.50  y -28.50..-25.30 z -401.25..-389.25  vol 491.90  ^ plate = 0.0000 mm3
  cover ^ plate  : 0.0   cover ^ boards : 0.0   boards ^ plate : 0.0   windows ^ plate: 0.0
```

Board is 18.00 × 12.00 (matching the BOM's `18 x 12 x 2.0 mm 2-layer sensor
PCB`), z-centred on Z_SENSOR = −395.250. Emitter LED bodies measure **Ø5.000 ×
9.000 mm** (y 17.5…26.5), centred (29.800, −392.250) and (35.800, −398.250) —
the Vishay TSAL6200 max-material height, so the r9 "LED buried in the wall"
defect stays closed.

### B4.7 — BOM: **PASS**

`cad/BOM.md` orders no TSSP4038. The string occurs exactly once, in the status
column of the PD row, as the record of the rejection:

```
| count PD x2 | Vishay VBPW34FAS (940 nm filtered PIN, 7.5 mm2) | ELECTRONICS 4.4 ASSUMPTION -- replaces the REJECTED TSSP4038 |  |
| count amp | TI OPA2320AIDR (dual, rail-to-rail, transimpedance) | ELECTRONICS 4.4 ASSUMPTION |  |
| count emitter x2 | Vishay TSAL6200 (940 nm, 34 deg) | ASSUMPTION |  |
| count windows x4 | Dia6 x 1.0 cast PMMA disc, sacrificial, bonded (UV-acrylic or CA) | ECO-4; laser-cut, PN ASSUMPTION |  |
| sensor-cover screws | 4x M2x6 self-tap into the boss ears | ECO-12 retention (r7 ordered 2x M3 grubs for a hole that did not exist) |  |
| sensor_cover (x2) | CF-PETG | 3.23 | 4.1 |
| count_windows (x4) | PMMA | 0.10 | 0.1 |
| 2 | 18 x 12 x 2.0 mm 2-layer sensor PCB | count emitter board (+Y) and receiver board (-Y), ECO-12 |
| 1 | UV-cure optical adhesive, 2 g | bonds the 4 PMMA windows into their bore-face seats (ECO-4) |
```

All five B4.7 items present (VBPW34FAS ×2, OPA2320, TSAL6200 ×2, 4 × PMMA
Ø6 × 1 windows), no TSSP4038 order line.

### B4.8 — chute-bore continuity with the new features: **PASS**

Printed under B4.4: Ø22.0 / Ø21.0 / Ø13.0 × 45 mm columns on the chute axis all
read **0.0000 mm³** against plate, windows and boards. The worst-case Ø13
granule has the full bore.

### ECO-12 / N3 sensor-board retention: **CLOSED, with one nit**

```
cover +Y: 2 through-holes, Dia~2.2, at (x 34.500, z -407.250) and (x 34.500, z -383.250)
plate pilot at the same axes: Dia1.600 blind, mouth |y| = 30.500, floor |y| = 25.500 -> 5.000 mm deep
side 0: min gap board->cover = 0.0000 mm ; min gap board->plate = 0.5000 mm
side 1: min gap board->cover = 0.0000 mm ; min gap board->plate = 1.2000 mm
```

The point-contact M3 grub is gone; the board is captured by a face on the
`sensor_cover` pocket floor bearing on the full 18 × 12 = **216 mm²** board face
(N3 asks ≥ 8 mm²), retained by 2 × M2×6 self-tap per side into Ø1.600 × 5.000 mm
thread-forming pilots. **Nit:** the board→cover gap is **0.0000 mm nominal** with
no compliant element modelled, so on a printed part it is either loose or
interfering; a 0.3–0.5 mm foam/elastomer pad (or a modelled 0.2 mm crush rib) is
the honest way to make "clamped" true.

### Cross-document defect: `ELECTRONICS.md` §4 sensing Z is stale by 49.1 mm

§4 states the beam is at "Z ≈ −343.2, 40 mm below the retaining plate, 10 mm
above the chute exit". Measured on r11:

```
release plane (retaining-plate top face) Z = -351.250; beam A Z = -392.250; beam B Z = -398.250; chute mouth Z = -418.300
drop to beam A = 41.000 mm -> v_A = 0.8969 m/s ; drop to beam B = 47.000 mm -> v_B = 0.9603 m/s ; ELECTRONICS 4.2 nominal (40 mm) = 0.8859 m/s
beam A is 26.050 mm above the chute mouth (ELECTRONICS 4 says 10 mm); doc stale by 49.1 mm
  Dia11: guaranteed worst-position chord = 9.2195 mm -> 10.41 ms @0.886, 10.28 ms @v_A, 9.60 ms @v_B
  Dia12: guaranteed worst-position chord = 10.3923 mm -> 11.73 ms @0.886, 11.59 ms @v_A, 10.82 ms @v_B
  Dia13: guaranteed worst-position chord = 11.5326 mm -> 13.02 ms @0.886, 12.86 ms @v_A, 12.01 ms @v_B
  Dia8 : best case (on-beam) chord 8.000 mm -> 9.03 ms @0.886, 8.92 ms @v_A, 8.33 ms @v_B
  ECO-9 dt_mid for 6.000 mm at v=0.8859 (doc) = 6.536 ms ; at v=0.8969 (as-built v_A) = 6.461 ms
```

Because the two beams are now at **different fall heights** (41.000 vs
47.000 mm), they run at **0.8969 and 0.9603 m/s** — 7.1 % apart. §4.3's count
logic takes the **longer** dark time, i.e. beam A, so the Ø11 guarantee moves
10.41 → **10.28 ms** against the 9.7 ms gate: margin drops from the stated 7 % to
**6.0 %**. The Ø8 best case moves 9.03 → **8.92 ms**, so the separator still
exists but is **1.36 ms** wide, not 1.37. Nothing here is disqualifying, and
B1 (the ≥200-drop survey) is what freezes the gate anyway — but §4 must be
re-based on Z = −392.250/−398.250 before B1's thresholds are cut, and ECO-9's
`Δt_mid = 6.54 ms` becomes **6.461 ms**.

### Ledger of what I asked for and what I got

| item | required | measured r11 | verdict |
|---|---|---|---|
| B4.1 aperture count/pos/dia | 4 × Ø3.2 ± 0.1 at (29, Z+3) / (35, Z−3) | 4 × Ø3.200 at (29.000, −392.250) / (35.000, −398.250) | PASS |
| ECO-9 stagger | 6.0 mm | **6.000** | PASS |
| B4.2 Ø2.0 × 60 beam clear | 0.000 mm³ on each beam axis | **1.1932 mm³** at x = 29.0/35.0; 0.0000 at 29.4/35.4 | **FAIL as written** |
| B4.3 boss x-min | ≥ 22.0 | **22.000** | PASS |
| B4.3 boss → motor face | ≥ 4.0 mm | **4.000** (modelled motor at x = 18.000) / 4.400 (ECO's 17.6) | PASS |
| B4.4 window flush, nothing proud | 0.000 mm³ proud | Ø22.0 column **0.0000 mm³** | PASS |
| B4.4 seat Ø6.0, 0.4 mm deep | Ø6.0 ± 0.1, 0.4 ± 0.05 deep | Ø6.000, **1.000 mm** deep (face recession 0.417 mm) | PASS in intent, deviates |
| B4.5 labyrinth offset / ledge | 0.8 ± 0.1 over the outer 2.5 mm, ledge ≥ 0.7 | **0.800 / 2.5000 / 0.800**, all 4 tunnels | PASS (wrong sense) |
| B4.6 20 × 8 × 12 cavity | 0.000 mm³ interference | **220.8000** at x = 32; **0.0000** at x = 34.5; real boards 0.0000 | PASS in function |
| B4.7 BOM | no TSSP4038; VBPW34FAS ×2 / OPA2320 / TSAL6200 ×2 / 4 × PMMA | all present, no order line | PASS |
| B4.8 Ø13 chute column | 0.000 mm³ | **0.0000** (also at Ø21.0 and Ø22.0) | PASS |

### What I am asking for in r12 (none of it blocking)

1. **Re-centre the labyrinth lens** (inner segment −0.400, outer +0.400) so B4.2
   reads 0.0000 at Ø2.0 on x = 29.000/35.000 and ECO-9's `x₀` solve stays valid;
   move the modelled TSAL6200 bodies back to 29.000/35.000 with it. If instead
   the offset chords are kept, **correct ELECTRONICS §4.3** to chords at
   −2.600/+3.400 with the re-derived `x₀ = (4.800 − (h_A² − h_B²))/12`, and
   restate the §4.4 excess gain against the 5.5094 mm² lens.
2. **Re-base ELECTRONICS §4** on the measured Z (−392.250/−398.250, 41.000/
   47.000 mm of fall, v = 0.8969/0.9603 m/s) and re-print the §4.2/§4.3 dark-time
   tables and `Δt_mid`. Delete "Z ≈ −343.2 … 10 mm above the chute exit".
3. **Say plainly in §4.5/ECO-4 that the window is swabbable but not field-
   replaceable** (20.050–26.050 mm up a Ø22 bore, bonded), or model a removal
   path.
4. Add the missing **0.4 mm chamfer** at the window-seat mouth, and a modelled
   compliant element (or crush rib) behind the sensor board so "clamped" is more
   than a 0.0000 mm tangency.

---

## granule-path

**Verdict: PASS with complaints — 0 blockers on the granule path, 1 MAJOR
(documentation of the fragment-jam requirement itself), 2 MODERATE, 3 MINOR.
The rev-0 fragment-jam mandate is NOT regressed.** Round 4's granule-path MAJOR
(the plug-tether anchor lug 1.000 mm inside the Ø22 drop tube, and 122.596 mm³
of unintended interference logged as "the designed 0.3 mm press fit") is
**closed and independently verified**: the bore re-measures ≥ 10.994 mm at every
height and `retaining_plate_chute ∩ chute_plug` is **83.5035 mm³ in exactly one
body** = the designed press fit and nothing else. Every geometric term of the
mandate (overfill relief before the housing arc at full roof section, nose gap =
roof clearance = 1.500 mm, compliant-element-first contact order, shear-margin
backstop, pocket/chamfer geometry) re-measures **byte-identically** to r10 —
`pocket_disc`, `meter_housing`, `brush_holder`, `agitator` and `hopper` are
md5-identical — and stall-recovery motion is rotationally unobstructed by a
method that is exact over **all** rotation angles, not a 1° sample.

The MAJOR is not geometry: the shipped `README.md` requirement table and
`docs/DESIGN.md` §4.5 still publish the **pre-B8** fragment-jam story (3.00 mm
nose, a 1.5–3.0 mm blind band, "7.5 N to shear a Ø6 fragment", verdict
"PARTIAL") — which the r11 geometry and the model's own r11 stdout both
contradict.

### Provenance

- Measured by me on `cad/exports/*_r11.stl` / `*_r11.step` with
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`, trimesh 5.0.0,
  numpy 2.5.1, scipy 1.18.0, build123d 0.11.1 (OCC booleans). Nothing was
  imported from `dispenser.py`; I read that file only to *name* a self-check
  after I had already measured the geometry it misses (§ MODERATE 1).
- md5 of the files every number below was measured on:
  `retaining_plate_chute_r11.stl 4946222b630217a46a669c1fd290820e`,
  `chute_plug_r11.stl 88c344f8264272d216eb82f5bbb3c59e`,
  `top_plate_r11.stl 27489119d3ac7e0fcefa382b91743c09`,
  `pocket_disc_r11.stl d02b663b6ae5cc8086ebb3a76288762e`,
  `meter_housing_r11.stl c3cbffb49753ba595dd63afb0c192db0`,
  `brush_holder_r11.stl ad2343fea8807cf4a998596e939e7308`,
  `hopper_r11.stl fdc1ab2e84884b5df4fa562ce9715331`,
  `agitator_r11.stl 8cb2f51f1358fd2b3ecdf8f49abbea3e`,
  `count_windows_r11.stl dfe57d4da5504b302f71422427f90918`,
  `sensor_cover_r11.stl 322b06d5ab237f8762f4c53ac447a9f2`,
  `sensor_boards_r11.stl 05f1c46fbcda261ef1377b2da10725d9`,
  `fill_cap_r11.stl 6c91283e1e336d0ebfec3e6c7e7ec415`,
  `dispenser_r11_assembly.stl 08b63f8a1f1a7b5605fbdd8720623c33`.
- **BUILD-NOTES-r5 §0 claim "the last two md5s are identical to the r10 files"
  is true and understated.** I checked all eight parts on the granule path:
  `pocket_disc`, `meter_housing`, `brush_holder`, `hopper` **and** `agitator`
  are byte-identical r10 → r11; `retaining_plate_chute`, `chute_plug` and
  `top_plate` changed. So every metering measurement below that reproduces r4
  reproduces it *because the bytes did not change*, and the only places a
  granule-path regression could hide this round are the chute, the plug and the
  tank lid — which is where I spent the scan budget.
- Z-stack re-measured on the exports by vertical ray crossings (not carried):
  housing roof top **−326.250**, roof underside **−335.250** (9.000 mm section),
  disc top **−336.750**, disc bottom **−350.750**, plate top **−351.250**, port
  bore **−352.000…−354.250**, chute bore **−354.500 → −405.250**.

### Independent mesh census (r11)

```
== MESH CENSUS r11 (independent) ==
agitator_r11.stl                   wt=True wind=True euler=     2 bodies=  1 vol_cm3=    4.288 inv=0 mult={2: 4086}
bay_lid_r11.stl                    wt=True wind=True euler=   -10 bodies=  1 vol_cm3=    8.598 inv=0 mult={2: 4614}
brush_holder_r11.stl               wt=True wind=True euler=     0 bodies=  1 vol_cm3=    3.544 inv=0 mult={2: 918}
chute_plug_r11.stl                 wt=True wind=True euler=    -2 bodies=  1 vol_cm3=    6.718 inv=0 mult={2: 3507}
count_windows_r11.stl              wt=True wind=True euler=     8 bodies=  4 vol_cm3=    0.104 inv=0 mult={2: 3000}
dispenser_r11_assembly.stl         wt=True wind=True euler=  -169 bodies= 24 vol_cm3=  587.193 inv=0 mult={2: 204780}
electronics_bay_r11.stl            wt=True wind=True euler=    -8 bodies=  1 vol_cm3=   21.175 inv=0 mult={2: 15027}
fill_cap_r11.stl                   wt=True wind=True euler=     0 bodies=  1 vol_cm3=    7.347 inv=0 mult={2: 5325}
hopper_r11.stl                     wt=True wind=True euler=   -14 bodies=  1 vol_cm3=  109.423 inv=0 mult={2: 16992}
meter_housing_r11.stl              wt=True wind=True euler=   -12 bodies=  1 vol_cm3=  103.623 inv=0 mult={2: 17463}
pocket_disc_r11.stl                wt=True wind=True euler=   -30 bodies=  1 vol_cm3=   72.661 inv=0 mult={2: 36963}
retaining_plate_chute_r11.stl      wt=True wind=True euler=   -48 bodies=  1 vol_cm3=   71.850 inv=0 mult={2: 40860}
sensor_boards_r11.stl              wt=True wind=True euler=     4 bodies=  2 vol_cm3=    1.287 inv=0 mult={2: 3108}
sensor_cover_r11.stl               wt=True wind=True euler=    -4 bodies=  2 vol_cm3=    3.234 inv=0 mult={2: 3540}
service_stand_r11.stl              wt=True wind=True euler=     0 bodies=  1 vol_cm3=  103.892 inv=0 mult={2: 1656}
top_plate_r11.stl                  wt=True wind=True euler=   -38 bodies=  1 vol_cm3=   95.299 inv=0 mult={2: 33606}
```

**15/15 part STLs watertight, every edge shared by exactly 2 faces (`mult={2: …}`
with no other key = 0 non-manifold and 0 open edges), 0 inverted bodies,
assembly 24 bodies.** B10 holds. This is the checker's claim reproduced, not
quoted.

### The full journey, hopper → pocket → exit, with every pinch point vs the Ø13 worst case

Travel direction re-derived from the geometry, not assumed: 8 pockets at 45°
pitch (open at r = 32 over θ ≈ 0/45/…/315, material 14…30° between them), index
22.5° = half a pitch, so **two indexes per dispensed granule**; the pocket fills
in the 120° sump window, leaves it at θ = 130.000 and runs to the exit port at
θ = 0.

| # | station | measured on r11 | vs the Ø13 worst-case granule |
|---|---|---|---|
| 1 | fill route, axis (0.00, 43.45) | Ø13 sphere dropped z −245 → −320 at 1 mm vs `hopper` + `top_plate`: **74/76 stations clear**; first contact at **z = −319** — that is the 68° funnel wall, not an obstruction (granule centre r 43.45 + 6.5 = 49.95 vs the measured wall r 49.983 at z = −320) | clear, then rolls |
| 2 | hopper barrel | inner **r 69.978** at z −255…−270 (69.478 at −245, the lid land) | 10.8 × D_max |
| 3 | funnel | r 69.978 @ −270 → 67.941 @ −275 → 64.089 @ −285 → 58.034 @ −300 → 53.999 @ −310 → **47.986 @ −325**; slope atan(55/21.99) = **68.2°**, no step at any probe | continuous |
| 4 | sump outlet (annular window) | edges bisected: **θ 130.0000 → 250.0000 = 120.0000°**; radial **r 20.0000 → 46.9926 = 26.9926 mm** at θ = 190; area **1893.7 mm²** → equivalent circular orifice **D 49.10 mm** | **26.993/13.0 = 2.076** — below every no-arch criterion for a slot (≥ 3×). **N10 plateau, unchanged** |
| 5 | deflector nose (rigid) | underside **1.500 mm** above the disc top at r = 20.5, 22, 26, 30, 34, 38, 42, 46.5, **47.0**; nose absent at r = 20.0 and 47.5 (7.450 mm rail there) | B8.1 holds at every radius; nose covers **r 20.5…47.0** |
| 6 | bristles (compliant) | assembly body 10: **312.2 mm³**, z −335.550…−328.160 → tip **+1.200 mm** above the disc top | leads the rigid nose (1.500 mm) ✔ |
| 7 | entry ramp (overfill relief) | ceiling **10.500 @ θ 130** (= 9.000 roof section + 1.500 gap, i.e. no step at the mouth) → 10.287/10.270/10.240/10.269/10.292/10.296 @ 129 → 9.158…9.249 @ 125 → 7.861…7.939 @ 120 → 3.972…4.010 @ 105 → 1.639…1.653 @ 96 → **1.500 @ ≤ 95**, at r = 20.5/24.5/32/39.5/45.5/46.5 | ordering correct: last fill opportunity is the window edge θ = 130.000, the relief runs 130 → 95, **nothing enters the covered arc unramped** |
| 8 | transfer arc | roof underside **1.500 mm** at every one of 6 radii × 22 angles (θ = 95, 90, 80, 60, 45, 30, 20, 10, 0, 350, 330, 320, 316, 313, 311, **310**, 309, 308, 305, 300, 290, 270); the window ramps back open at 255 (7.589–7.801) and 251 (9.941–10.071) | crown of a seated granule is 1.500 **below** the disc top → 3.000 mm clear |
| 9 | pocket | bore **r 7.498** from depth 2.00 to 13.90; 45° chamfer **9.497 @ 0.00, 9.297 @ 0.20, 8.992 @ 0.50, 8.489 @ 1.00, 7.992 @ 1.50, 7.498 @ 2.00** (180/180 azimuths at every depth) | 2.00 mm diametral clearance; seated centre 8.000 mm below the disc top |
| 10 | exit port | bore **r 7.998** (z −352.000…−354.200), 0.75 × 45° chamfer (8.697 @ −351.30, 8.390 @ −351.60), **first material at the plate top r = 8.747** | 3.00 mm diametral clearance |
| 11 | chute | **r_min 10.994 mm at z = −401.00**, ≥ 10.994 over the whole run z −355 → −405 with `count_windows` + `sensor_cover` + `sensor_boards` merged (180 azimuths × 51 heights) → **Ø21.989 continuous**; window inner faces sit at r 11.000, nothing proud | Ø13 free lateral envelope **±4.49 mm, symmetric** (r10: +3.500/−4.500) |

**Ø13 free-fall envelope in the parallel chute** (signed distance from the
granule centre to the merged plate + windows + cover + boards, z −362…−403 at
0.5 mm):

```
   centre offset +0.00 mm in +x: worst centre-to-surface 10.993 mm at z  -398.50 -> clearance +4.493 mm; centre inside material 0/83 stations
   centre offset +3.50 mm in +x: worst centre-to-surface  7.498 mm at z  -362.00 -> clearance +0.998 mm; centre inside material 0/83 stations
   centre offset +4.49 mm in +x: worst centre-to-surface  6.508 mm at z  -362.00 -> clearance +0.008 mm; centre inside material 0/83 stations
   centre offset +4.60 mm in +x: worst centre-to-surface  6.398 mm at z  -362.00 -> clearance -0.102 mm
   centre offset -4.49 mm in +x: worst centre-to-surface  6.507 mm at z  -403.00 -> clearance +0.007 mm; centre inside material 0/83 stations
```

**Seated-granule transit (B8.5).** Ø13 sphere, centre z −344.750 (crown 1.500 mm
below the disc top), carried round the PCD:

```
   vs meter_housing            min surface distance from the granule centre   9.500 mm -> clearance  +3.000 mm; centre-inside stations 0/360
   vs brush_holder             min surface distance from the granule centre   9.500 mm -> clearance  +3.000 mm; centre-inside stations 0/360
   vs hopper                   min surface distance from the granule centre  22.722 mm -> clearance +16.222 mm; centre-inside stations 0/360
   vs agitator                 min surface distance from the granule centre  19.050 mm -> clearance +12.550 mm; centre-inside stations 0/360
   vs retaining_plate_chute    min surface distance from the granule centre   6.500 mm -> clearance  +0.000 mm; centre-inside stations 0/360   (the granule resting ON the plate, tangent)
   642-vertex Dia13 sphere containment, 180 stations at 2 deg: 0/180 for all five parts
```

**B1 roof section**, 120 probes (θ = 300/305/308/309/310/311/313/316/320/330/
350/0/20/45/90 × r = 20.5/24.5/30/32/36/39.5/44/46.5): **9.000 mm at every one
of the 120 probes**, worst 9.000 at θ = 300, r = 20.5. (`verify_r5.py` prints
8.950 for the same worst probe; the 0.050 mm is its probe step, and either
number passes B1's ≥ 6.0 mm. r6's 0.000 mm slot at θ = 310 stays gone.)

**B1.3 face audit, printed whatever the result** (faces whose outward normal
opposes disc travel, granule band r 18…47.5 and 0…10.5 mm above the disc):

```
   brush_holder : confronting faces  203.05 mm2; vertical (|n_z|<0.05)  80.52 mm2; area-weighted n_z +0.427
      largest single vertical confronting face  21.54 mm2 at theta 154.34, r 40.75, height  8.24 above the disc
      vertical confronting faces with centroid 1.4..2.8 mm above the disc: 16.02 mm2 over 2 triangles (the blunt leading tip)
      COVERED TRANSFER ARC (theta 250..360..131): NO vertical confronting face at all
   meter_housing: confronting faces   75.75 mm2; vertical  75.75 mm2
      largest single vertical confronting face   8.90 mm2 at theta 249.98, r 19.33, height 7.43 above the disc
      COVERED TRANSFER ARC (theta 250..360..131): largest vertical confronting face 1.98 mm2 at theta 263.07, r 42.00, height 3.20
```

The only face over B1.3's 20 mm² line is the 21.54 mm² one at θ = 154.34 — its
centroid is **8.24 mm above the disc**, i.e. above the 7.450 mm rail underside
where no granule or fragment can be, and it is in the wiper sector, not the
covered arc. Over the covered transfer arc the worst is **1.98 mm²**. Not a
defect; it is a number the r5 notes do not print.

### Round-4 granule-path MAJOR — closed, verified two ways

Radial-ray sweep about the chute axis (32, 0), 180 azimuths per height:

```
   z  -396.000: r_min 10.995      z  -401.500: r_min 10.994      z  -404.500: r_min 10.996
   z  -398.000: r_min 10.995      z  -403.000: r_min 10.995      z  -405.000: r_min 10.997
   z  -399.000: r_min 10.995      z  -404.000: r_min 10.996      z  -405.200: r_min 10.997
   MINIMUM bore radius over z -355..-405 (1 mm x 180 azimuths, merged with count_windows + sensor_cover + sensor_boards): 10.994 mm at z = -401.00
```

r10 read **10.000 mm over z −398.00…−404.00** (a 6.0 × 8.0 mm ledge in the fall
path). It is gone. OCC boolean, both parts as exported in the fitted pose:

```
   retaining_plate_chute ^ chute_plug = 83.5035 mm3 in 1 bodies:
         83.5035 mm3  x[  20.85,  43.15] y[ -11.15,  11.15] z[ -389.000, -381.000]
   designed press fit = the Dia22.3 land in the Dia22.0 bore over 8.0 mm = 2*pi*11.075*0.150*8.0 = 83.504 mm3
```

**One body, and it is the press fit.** r10's 206.0993 mm³ / three bodies is
resolved; the shank-vs-lug (16.973) and flange-vs-plate (2 × 52.811) terms are
gone, not re-labelled. The build notes' §4 numbers reproduce exactly.

### Adversarial fragment construction — re-derived from scratch on r11

All inputs are my own r11 probes: chamfer first-material r 9.497 at depth 0
(45°, verified against the 6-depth table), bore r 7.498, seat depth 8.000, nose
1.500, port bore 7.998. **σ = 0.36 MPa and µ = 0.4 remain carried ASSUMPTIONS**
(US4172714-derived; closure = IFDC S-115). Drive re-derived from the BOM motor:
`0.14 N·m × 5.18 × 0.90 = 0.6527 N·m ÷ 0.032 m` = **20.4 N at the pocket lip in
recovery, 12.2 N at the 60 % metering current**.

**(a) Fragment nested in the pocket chamfer on a seated granule** (crown height
above the disc top; the nose is at 1.500):

```
   d_frag |  D13 centred | D13 seat+1.00 | D13 seat-1.00 |  D12 centred | D12 seat+1.50
    D 4.0  | +0.639 | +1.062 | +0.174 | +0.283 | +0.893
    D 4.5  | +1.222 | +1.632 | +0.770 | +0.865 | +1.455
    D 5.0  | +1.801 | +2.199 | +1.362 | +1.443 | +2.013
    D 5.5  | +2.376 | +2.763 | +1.950 | +2.017 | +2.569
    D 6.0  | +2.949 | +3.324 | +2.533 | +2.587 | +3.122
    D 7.0  | +4.083 | +4.438 | +3.690 | +3.718 | +4.221
    D 8.0  | +5.207 | +5.542 | +4.835 | +4.838 | +5.310
   largest fragment that clears the 1.500 mm nose, D13 centred   : D 4.740 ; outer reach 7.646 vs port bore 7.998 -> margin +0.352 mm
   largest fragment that clears the 1.500 mm nose, D13 seat+1.00 : D 4.384 ; outer reach 7.897 vs port bore 7.998 -> margin +0.101 mm
   largest fragment that clears the 1.500 mm nose, D13 seat-1.00 : D 5.117 ; outer reach 7.379 -> +0.619 mm
   largest fragment that clears the 1.500 mm nose, D12 centred   : D 5.050 ; outer reach 7.426 -> +0.572 mm
   largest fragment that clears the 1.500 mm nose, D12 seat+1.50 : D 4.541 ; outer reach 7.786 -> +0.212 mm
   largest fragment that clears the 1.500 mm nose, D12 seat-1.50 : D 5.612 ; outer reach 7.028 -> +0.970 mm
```

Identical to r7/r9/r10 to ≤ 0.001 mm: **B8's gain over r6 is held.** The
worst-case escaping fragment is **Ø4.740** (D13 centred) / **Ø5.612** (D12, seat
−1.50), and every escapee still fits the exit port, with **+0.101 mm** the
tightest clearance anywhere on the exit path (D13 seat +1.00).

**(b) The wedged sliver that must be sheared** — sliver of radial width w in the
crescent between a seated Ø13 granule and the measured Ø14.996 bore, shear plane
at the measured 1.500 mm nose/roof underside, 90°-conforming shard on the mean
crescent radius:

```
      w     x_inner  y_seat   depth   height_to_shear  half-angle  self-lock  arc90(mm)  A(mm2)   F(N)   x20.4N  x12.2N
    1.000    6.498    0.161   7.839         9.339        0.71      YES      10.99    10.99    3.96    5.16x   3.08x
    1.500    5.998    2.505   5.495         6.995       11.33      YES      10.60    15.90    5.72    3.56x   2.13x
    2.000    5.498    3.467   4.533         6.033       16.12      YES      10.21    20.41    7.35    2.78x   1.66x
    2.500    4.998    4.156   3.844         5.344       19.87      YES       9.81    24.54    8.83    2.31x   1.38x
    2.793    4.705    4.485   3.515         5.015       21.81       no       9.58    26.77    9.64    2.12x   1.27x
    3.000    4.498    4.692   3.308         4.808       23.11       no       9.42    28.26   10.18    2.00x   1.20x
    4.000    3.498    5.479   2.521         4.021       28.72       no       8.64    34.54   12.44    1.64x   0.98x
    5.000    2.498    6.001   1.999         3.499       33.70       no       7.85    39.25   14.13    1.44x   0.86x
   WIDEST SELF-LOCKING SLIVER: w = 2.791 mm, seats 4.483 above the granule centre (3.517 below the disc top),
     must be >= 5.017 mm tall to reach the shear plane; A = 26.75 mm2, F_shear = 9.63 N
     -> recovery margin 2.12x (20.4 N), normal-current margin 1.27x (12.2 N)
   shearable-section bound: 56.7 mm2 at recovery, 33.9 mm2 at normal current; whole pocket bore = 176.6 mm2
   180-deg conforming shard at w=2.791: A 53.51 mm2, F 19.26 N -> 1.06x recovery, 0.63x normal
   full-ring crescent at w=2.791: A 107.02 mm2, F 38.53 N -> 0.53x recovery, 0.32x normal
   whole-granule crush 41 N [ASSUMPTION]: recovery 20.4 N = 2.01x under -> a trapped whole granule STALLS, it is not milled
```

**Shear-margin headline, reproduced on r11: the worst self-locked sliver the
pocket can hold (w = 2.791 mm, ≥ 5.017 mm tall) needs 9.63 N; the drive delivers
20.4 N in recovery and 12.2 N at normal current → 2.12× / 1.27×.** Where it runs
out is unchanged and is still only in *my* table: a 180° conforming shard is
**1.06×** recovery / **0.63×** normal, a full-ring crescent **0.53× / 0.32×** →
stall (MODERATE 2 below).

**(c) Does the nose actually stub a rounded fragment?** Swept-sphere first
contact (closest-point query on the exported `brush_holder`, 0.05° steps,
reaction taken as contact-point → sphere-centre, which is the direction a sphere
is actually pushed):

```
   D 5.0 crown + 1.80, r= 26.7: first contact theta 159.20, contact height +1.500 mm, n=(-0.252,-0.403,-0.880) -> |n_z|/|n_tang| = 1.85 (pressed DOWN)
   D 5.0 crown + 1.80, r= 32.0: first contact theta 157.30, contact height +1.500 mm, n=(-0.249,-0.399,-0.883) -> 1.88 (pressed DOWN)
   D 6.0 crown + 2.95, r= 26.7: first contact theta 162.20, contact height +1.500 mm, n=(-0.453,-0.725,-0.520) -> 0.61 (pressed DOWN)
   D 6.0 crown + 2.95, r= 32.0: first contact theta 159.80, contact height +1.500 mm, n=(-0.452,-0.724,-0.521) -> 0.61 (pressed DOWN)
   D 7.0 crown + 4.08, r= 26.7: first contact theta 164.00, contact height +1.500 mm, n=(-0.511,-0.818,-0.263) -> 0.27 (pressed DOWN)
   D 7.0 crown + 4.08, r= 32.0: first contact theta 161.30, contact height +1.500 mm, n=(-0.511,-0.818,-0.263) -> 0.27 (pressed DOWN)
   D 9.0 crown + 6.00, r= 26.7: first contact theta 166.55, contact height +1.500 mm, n=(-0.530,-0.848,+0.000) -> 0.00 (pure anti-travel STUB)
   D 9.0 crown + 6.00, r= 32.0: first contact theta 163.40, contact height +1.500 mm, n=(-0.530,-0.848,+0.000) -> 0.00 (pure anti-travel STUB)
   D13.0 crown +11.50, r= 26.7: first contact theta 180.00, contact height +7.450 mm, n=(-0.479,-0.766,-0.430) -> 0.48 (pressed DOWN)
   D13.0 crown +11.50, r= 32.0: first contact theta 175.95, contact height +7.450 mm, n=(-0.491,-0.785,-0.378) -> 0.41 (pressed DOWN)
```

**This reproduces BUILD-NOTES-r5 §5 to ≤ 0.05 in every ratio and to 0.00° in
every contact angle except the stacked Ø13 case**, where I read first contact at
**180.00° at r 26.7 / 175.95° at r 32.0** against their 175.00° at both radii —
a scan-start artefact on their side, and immaterial (contact height +7.450 mm
and the sign of n_z agree). **n_z ≤ 0 in every case: nothing is lifted over the
nose.** The withdrawal of the `cot(30) = 1.73` ramp credit (r4 MODERATE 1) is
therefore correct and is confirmed on the geometry; the crush numbers now
carrying the argument reproduce exactly (Ø5.0 → 19.63 mm² → **7.07 N**, Ø6.0 →
28.27 mm² → **10.18 N**, Ø7.0 → 38.48 mm² → **13.85 N** vs 12.2 N normal /
20.4 N recovery).

### Stall-recovery motion has the free travel it needs — verified, and by a stronger method than r4

The rev-0 agitator-clash blocker stays closed. Rather than sample 360 angles, I
reduced the problem exactly: for rotation about the meter axis, the minimum
distance between a revolved rotor point and a static surface is a **2-D (r, z)
distance**, so a KD-tree over the static's surface cloud gives the minimum
clearance over **all** angles, not a sample. Statics sampled at 300 k points +
vertices, rotors at 120 k + vertices:

```
   agitator     vs meter_housing         : MIN CLEARANCE OVER ALL ROTATION ANGLES =   0.550 mm  (at r= 46.70, z= -325.70); assembled-pose containment 0/4000 rotor points inside
   agitator     vs hopper                : MIN CLEARANCE OVER ALL ROTATION ANGLES =   0.934 mm  (at r= 46.70, z= -325.70); 0/4000
   agitator     vs brush_holder          : MIN CLEARANCE OVER ALL ROTATION ANGLES =   0.600 mm  (at r= 46.70, z= -325.70); 0/4000
   agitator     vs retaining_plate_chute : MIN CLEARANCE OVER ALL ROTATION ANGLES =  25.350 mm; 0/4000
   pocket_disc  vs meter_housing         : MIN CLEARANCE OVER ALL ROTATION ANGLES =   0.973 mm  (at r= 46.00, z= -345.85); 0/4000
   pocket_disc  vs hopper                : MIN CLEARANCE OVER ALL ROTATION ANGLES =   6.646 mm; 0/4000
   pocket_disc  vs brush_holder          : MIN CLEARANCE OVER ALL ROTATION ANGLES =   1.500 mm  (at r= 31.88, z= -336.75); 0/4000
   pocket_disc  vs retaining_plate_chute : MIN CLEARANCE OVER ALL ROTATION ANGLES =   0.500 mm  (at r= 41.22, z= -350.75); 0/4000
```

Since the rotors start outside every static (0/4000 containment at the assembled
pose) and the revolved clearance never reaches 0, **penetration is impossible at
any rotation angle, forward or reverse** — a stronger statement than r4's
"0/360 sampled angles". The binding numbers are the same as r4's (0.550 / 0.934
/ 0.600 / 25.350 and 0.973 / 6.646 / 1.500 / 0.500), because the geometry is
byte-identical.

**Reverse-stroke free travel** (recovery runs +θ; ceiling ray-cast on
`meter_housing` + `brush_holder`, 0.25° steps), measured at three radii because
a stacked Ø13 granule spans r 25.5…38.5 and is not a point at the PCD:

```
   at r = 24.5:  park 157.5 ceiling  7.450 | 2.0 mm 107.50 | 5.0 mm 102.25 | 11.5 mm n/a
                 park 180.0 ceiling    inf | 85.00 | 79.75 | 69.75
                 park 202.5 ceiling    inf | 62.50 | 57.25 | 47.25
                 park 225.0 ceiling    inf | 40.00 | 34.75 | 24.75
                 park 247.5 ceiling    inf | 17.50 | 12.25 |  2.25   <- the binding case
   at r = 32.0:  park 247.5           inf | 17.50 | 12.25 |  2.50
   at r = 39.5:  park 247.5           inf | 17.75 | 12.25 |  2.50
   park 135.0 at r 24.5 / 32.0: ceiling 1.500 -> n/a for every proud class (such an object cannot be at that park at all)
```

**The published 2.25° is correct and is the number I measure independently** at
r = 24.5, the binding radius. BUILD-NOTES-r5 §6 measures 2.50° there and
*publishes* 2.25° anyway; that is the right call and it is stated. For every
fragment class the recovery actually has to clear (≤ 5.0 mm proud) the
guaranteed free travel is **12.25°** = 6.84 mm of arc at the PCD, which is
2.4 × the 2.791 mm widest self-locking sliver — the recovery stroke has room to
back a wedged fragment out. The 2.25° bound applies only to a *stacked whole
granule* (11.5 mm proud) at the 247.5° park, where it is 1.26 mm of arc; that is
tight, it is published, and it is the one recovery case that is arc-limited
rather than torque-limited.

**N10 agitation defence re-measured** (the plateau is only allowed if these are
printed): agitator **r_max 46.743** vs the measured window outer edge 46.993 →
**+0.250 mm**; **3 fingers** at θ ≈ 0/120/240, 4.8–4.9° wide at r > 44, so
exactly one is in the 120.000° window at a time; each 22.5° index sweeps
**18.75 %** of the window → one full sweep per **5.33 indexes = 2.67 dispensed
granules**. Reproduces the notes exactly.

**N6** stays closed on r11: disc lightening voids read 120/360 azimuths open at
r = 11.0, 104/360 at r = 15.0, **2/360 at r = 15.5, 0/360 at r = 16.0** → radial
land to the sump-window inner edge r = 20.000 is **≥ 4.000 mm** (punch list asks
≥ 2.0).

**B7 release** re-derived analytically from my measured rim (first material
r = 8.747 at the plate top) and PCD 32, park separation `2·32·sin 11.25° =
12.4858 mm`:

```
   D13 seat +max (+0.998): contact crosses the rim at pocket separation  9.745 mm =  4.98 deg into the 22.5 deg index
   D13 centred           : 8.747 mm =  6.79 deg          D13 seat -max (-0.998): 7.749 mm =  8.59 deg
   D12 seat +max (+1.498): 10.245 mm =  4.08 deg         D12 seat -max (-1.498): 7.249 mm =  9.49 deg
   D11 seat +max (+1.998): 10.745 mm =  3.17 deg         D11 seat -max (-1.998): 6.749 mm = 10.39 deg
   -> release window 3.17 .. 10.39 deg into the index; spread across D11-D13 = 7.22 deg; spread at D13 alone = 3.61 deg
   park retention: the contact point is +3.739 mm outboard of the rim when centred, +2.741 mm at the worst D13 seat -> retained at park
```

That is the shipped 3.25–10.50° / 7.25° window reproduced to ≤ 0.11° from a
different construction. **B7 remains a recorded plateau** (release happens
12.1–19.3° of disc rotation before the dwell begins, i.e. while the disc is
moving), which the package states.

---

### MAJOR — the shipped README and DESIGN still publish the *pre-B8* fragment-jam story, and a shear force the model's own r11 output contradicts

This is my requirement, so I own the complaint. `README.md` line 42, the
headline requirement table:

> | Fragment jam (2026-08-06 directive) | reject before wedge; shear as backstop; detect + recover | 25° entry ramp + 30° deflector nose + brush wiper; **20.4 N recovery vs 7.5 N to shear a Ø6 fragment (2.7×)**; Hall phase decode + bounded reverse-oscillate | **PARTIAL** — the r6 pellet-path critic constructed a fragment that lands in a **1.5–3.0 mm blind band** and is defeated by *crushing*, not by rejection |

Three of those clauses are false on `r11`:

1. **"1.5–3.0 mm blind band"** — measured nose underside is **1.500 mm at
   r = 20.5, 22, 26, 30, 34, 38, 42, 46.5, 47.0** and roof clearance is
   **1.500 mm** at 132 probes. max(nose gap) = min(roof clearance) = 1.500;
   **there is no band**. B8 closed this and the README still reports it open.
2. **"7.5 N to shear a Ø6 fragment (2.7×)"** — the model's own r11 stdout prints
   **Ø6.0 → 28.27 mm² → 10.18 N** (2.00× at recovery, 1.20× at normal current),
   and my independent derivation gives the same 10.18 N. `docs/DESIGN.md`
   carries the same stale 7.5 N at lines 253, 273 and 289. A shipped
   requirement-table margin that is 36 % optimistic against the package's own
   log is exactly the RT-19 / N15 failure class this run exists to prevent.
3. **"25° entry ramp"** — the ramp is a constant-dz/dθ surface, so the angle is
   radius-dependent. Measured on r11 (ceiling 10.500 → 1.500 over the modelled
   arc): **36.12° at r 20.5, 34.21 @ 22.0, 31.41 @ 24.5, 25.05 @ 32.0, 20.74 @
   39.5, 17.83 @ 46.5**. 25° is one radius of a 17.8–36.1° range, and at
   r ≤ 21.9 the ramp's cot falls below the 1.44 self-locking line the same
   documents use as a pass/fail criterion. BUILD-NOTES-r5 publishes the range;
   README does not.

`docs/DESIGN.md` §4.5 is worse in one respect: it still ends "**The fix is one
parameter: `NOSE_GAP` 3.00 → ≤1.50 mm.** It is not applied in this revision" —
which is now untrue of the CAD, and no rev-1 section corrects it (§4.8 covers
only the harness elbow, the screw head and the tether lug). CONTEXT's
deliverables require an honest rev-1 section in both documents; the fragment-jam
requirement is the one thing in this package that Thomas asked for by name, and
it is the one requirement row that has not been re-written against the geometry
that now exists.

**What closes it:** rewrite the README row and add a DESIGN rev-1 paragraph
using the measured numbers — nose 1.500 mm at r 20.5…47.0 = roof clearance,
bristle tip 1.200 mm leading, entry-ramp angle range 17.83–36.12°, worst
escaping fragment Ø4.740 (D13 centred) / Ø5.612 (D12 seat −1.50), widest
self-locking sliver w = 2.791 mm → 9.63 N → 2.12× recovery / 1.27× normal,
Ø6 crush 10.18 N (2.00× / 1.20×), whole-granule crush 41 N = 2.01× above
recovery so a granule stalls rather than being milled — and state the verdict
that follows from *those* numbers rather than the r6 ones.

### MODERATE 1 — two 2.2 × 5.0 mm slots leave the granule bed open to the sky, and the model's own tank-vent check cannot see them

New finding; **not a regression** (identical in r10 and r11, so it predates this
round), and not previously reported by any critic. Upward-ray scan from inside
the barrel at z = −239.5 against `hopper` + `top_plate` + `fill_cap` (cap
**fitted**), 0.25 mm plan grid:

```
   r10: 10653 probes over x -25..25, y -72..-59 at 0.25 mm -> OPEN 438 = 27.38 mm2 of unroofed plan area
      patch: x -20.75.. -17.75  y -72.00..-70.00  area   6.00 mm2      (outside the barrel bore, over the flange -- not tank)
      patch: x -10.00..  -8.00  y -68.25..-63.75  area  10.69 mm2
      patch: x   8.00..  10.00  y -68.25..-63.75  area  10.69 mm2
   r11: identical, 438 probes / 27.38 mm2, same three patches
   edges bisected: +x slot x 7.9000..10.1000 = 2.2000 mm, y -63.5000..-68.5000 = 5.0000 mm -> clear opening 11.00 mm2 (mirror at x -10.1..-7.9)
   lid section there z -235.60..-233.55 = 2.05 mm; no material at ANY z above the funnel in those columns
   plan radius of the slot centre = 66.61 mm, inside the measured barrel bore r 69.978 -> it is over the granule bed
   largest sphere that can pass the slot: Dia 2.200 mm
```

Cross-checked with downward rays from z = −200 against the **whole assembly**:
at (9, −66) and (−9, −66) the first material below is the funnel cone at
**−278.88 / −284.52** — i.e. nothing at all between the granule bed and the sky.
For comparison (0, −66) reads `[-226.05, -227.55, -233.55, -235.60, …]` and
(9, −72) reads `[-233.55, -238.55, …]`, so the neighbouring columns *are* roofed
and this is a local 2.2 × 5.0 mm hole, twice.

Consequence for the granule path: a Ø11–13 granule cannot pass (Ø2.200), but
**fines, dust and water can, in both directions**, straight onto the top of the
granule bed — and dust and swollen granules are precisely the mechanisms behind
the fragment-jam requirement I am reviewing (RT-7 humidity/swelling, RT-8
landing dust). It also means the tank has an uncontrolled upward-facing vent,
which nobody has decided to have.

The reason this survived nine rounds is a checker-coverage defect worth naming
(N14 class): `dispenser.py` L3985-3993 tests "tank → NECK CAVITY" with **12
hand-placed Ø1.2 columns** at `(0,0), (0,8), (0,14), (0,18), (0,20), (0,22),
(5,20), (-5,20), (10,10), (0,-10), (12,18), (-12,18)` — none of them is within
40 mm of (±9, −66), so the check prints `0 of 12 … open` while 22.0 mm² of the
lid is missing. A 12-point sample cannot certify a 15 000 mm² lid; the scan
should be a grid (mine is 0.25 mm and takes seconds).

### MODERATE 2 — the shear backstop's failure bound is still not in any shipped document

Repeat of round 4's item 4, unactioned. The model prints the *capability*
(`at 20.4 N the drive can shear any proud section up to 57 mm²`,
`r11_build.log:211`) but never the *bound*: at the widest self-locking sliver
(w = 2.791 mm) a **180° conforming shard is 53.51 mm² → 19.26 N → 1.06×
recovery and 0.63× at normal current**, and a **full-ring crescent is
107.02 mm² → 38.53 N → 0.53× / 0.32× → stall**. That is where "shear as
backstop" stops working, it is one line, and it belongs in
`docs/DESIGN.md` §4.5 and the test plan alongside the 2.12× headline. The
shipped shear table (`r11_build.log:195-199`) also uses a narrower crescent
chord than mine and so reports a *less* conservative worst case (w = 3.0:
25.5 mm² / 9.2 N vs my 28.26 / 10.18) and picks its "worst" row from a
**non-self-locking** width; the headline margin is 2.0–2.2× either way, so this
is presentation, not a defect — but the self-locking limit (w = 2.791) is the
row that matters and it is not in the table.

### MINOR 1 — the r5 notes' stacked-Ø13 contact angle

BUILD-NOTES-r5 §5 prints `Dia13.0 crown +11.50, r=26.7: first contact theta
175.00` and `r=32.0: 175.00`. I measure **180.00° at r 26.7** and **175.95° at
r 32.0** on the same mesh with the same 0.05° step; the flat 175.00 at both
radii looks like the scan starting at 175°. Conclusion is unaffected (contact
height +7.450 mm, n_z < 0 both ways).

### MINOR 2 — the fill-drop "obstruction" needs one word of explanation in the notes

A Ø13 granule dropped on the fill axis (0.00, 43.45) reads **2 obstructed
stations of 76** at z = −319 and −320. That is not a blockage: it is the
granule reaching the 68.2° funnel wall (centre radius 43.45 + 6.5 = 49.95 mm
against the measured wall at r 49.983 @ z −320) and rolling. Any future checker
that prints this as a failure count will re-raise it; label it.

### MINOR 3 — the assembly census still shows no seated contact

`dispenser_r11_assembly.stl` reads `mult={2: 204780}` — every edge shared by
exactly two faces, i.e. **no coincident-face contact anywhere between 24 parts
that seat on each other**, and the census cannot see interpenetration either
(the r10 tether lug passed this census while sitting 1.000 mm inside the bore).
The census is a *manifoldness* test, not an *assembly* test; the OCC boolean is
the one that finds interference. Keep both, and stop citing the census as
evidence about fit.

### What I require to pass the granule path next round

1. **Rewrite the `README.md` fragment-jam requirement row and add the DESIGN
   rev-1 paragraph** against the measured r11 numbers (MAJOR above). The
   "1.5–3.0 mm blind band", the "7.5 N to shear a Ø6 fragment (2.7×)" and the
   bare "25° entry ramp" must all go; `docs/DESIGN.md` §4.5's closing sentence
   ("It is not applied in this revision") must be corrected or explicitly dated
   as r6 history.
2. **Close or consciously accept the two 2.2 × 5.0 mm lid slots** (22.00 mm²
   total, Ø2.200 pass-through, over the granule bed, open to atmosphere), and
   **replace the 12-column tank-vent self-check with a grid scan** that would
   have found them. If they are a deliberate vent, say so in the BOM/README with
   a filter and the ingress consequence stated.
3. **Publish the shear-backstop bound** (180° shard 1.06× recovery / 0.63×
   normal; full ring 0.53× / 0.32×) next to the 2.12× headline, and add the
   w = 2.791 mm self-locking row to the model's own shear table.
4. **Keep** everything that closed: the Ø21.989 continuous drop tube, the
   single-body 83.5035 mm³ press fit, the 1.500 mm nose at r 20.5…47.0, the
   1.200 mm bristle lead, the 130 → 95° overfill relief at full 9.000 mm roof
   section, the 2.25° published reverse bound, and the N10 plateau with its
   measured 120.000° / 26.993 mm / 2.076 × D_max / 18.75 %-per-index numbers.

## assembly

**Owner:** assembly-and-drive critic (rev-0 RT-1; punch-list **B2, B3-access,
B9a/b/c/d, B10, B12.2** in so far as they are assembly/torque items).
**Verdict: FAIL — 1 blocking finding (A-11).** Round-4's blocker **A-10 is
closed** and I reproduce the closing numbers independently. The assembly order
closes at **0.0000 mm³ on every one of the 24 straight-line operations** with
their opposite-approach controls all non-zero, and the torque path
motor→gearbox→shaft→disc measures clean for the fifth round running
(**12.000 mm of flat-on-flat, 37.93 mm² of bearing**). What fails is in the same
BOM-vs-geometry seam that A-10 was in, and it was in the punch list from the
start: **B9c — the M5 detent plunger has nothing to thread into. Its bore is a
plain Ø5.199/Ø6.399 hole, no thread and no insert is modelled, and no M5 insert
appears anywhere in `cad/BOM.md`, so the part cannot be installed at all.** The
detent is 96.5 of the 190.7 mN·m reaction budget, so this is not cosmetic.

### Provenance

- Measured on `cad/exports/*_r11.*`, mtime **2026-08-07 20:33**, and
  `cad/BOM.md`, mtime **2026-08-07 20:51** (i.e. after the exports).
  `md5(dispenser_r11_assembly.step) = ed5d4fe2e822c4d9f86b5e734df5d677`,
  `md5(dispenser_r11_assembly.stl) = 08b63f8a1f1a7b5605fbdd8720623c33`,
  `md5(retaining_plate_chute_r11.step) = 57b491fd98175bd57cc6b4b80fbdfbde`,
  `md5(pocket_disc_r11.step) = 1a03d84c9ee00e4d3875dcb64aeeeb56`,
  `md5(meter_housing_r11.step) = e2015b6d3a11ee1a677dba278e45cbee`,
  `md5(top_plate_r11.step) = e07e01a701cbd18fd1be676f8ec0c1ca`,
  `md5(hopper_r11.step) = 3fe2cc48a80518e37253ddb2a608f5d7`,
  `md5(electronics_bay_r11.step) = 8990bb9e7bc376760e2807130ac9d370`,
  `md5(chute_plug_r11.step) = cec04fc635be64b813846c25f3b78089`,
  `md5(service_stand_r11.step) = 3654e9e37401689b2f3fb69d456e186d`.
  The STL md5s in `BUILD-NOTES-r5.md` §0 match my own reads, and the notes'
  central claim that **`pocket_disc_r11.stl` and `meter_housing_r11.stl` are
  byte-identical to r10** is true — I checked it rather than believed it:
  `pocket_disc r10=d02b663b6ae5cc8086ebb3a76288762e r11=d02b663b6ae5cc8086ebb3a76288762e`,
  `meter_housing r10=c3cbffb49753ba595dd63afb0c192db0 r11=c3cbffb49753ba595dd63afb0c192db0`.
  `hopper` and `electronics_bay` are also byte-identical to r10; `top_plate`,
  `retaining_plate_chute` and `chute_plug` changed, as the notes say.
- All obstruction volumes are **exact OCC booleans** on the STEP bodies
  (`build123d.import_step` + `BRepAlgoAPI_Common` + `BRepGProp`), not voxel
  estimates. Profile/grip probes are trimesh ray-casts on the STLs. venv
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`, build123d 0.11.1,
  trimesh 5.0.0, numpy 2.5.1. Nothing is imported from `dispenser.py` and no
  number is taken from `BUILD-NOTES-r5.md`; where I quote the notes it is to
  agree or disagree with a number I measured first.
- COTS bodies were identified in `dispenser_r11_assembly.step` by volume match
  against the part exports; the six unmatched solids (clip plate 11.5234,
  motor+gearbox 69.9363, bearing 1.4946, blind-mate PCB 1.1744, thrust washer
  0.3167, brush strip 0.3122 cm³) are identified from size and position — an
  **ASSUMPTION**, unchanged from rounds 1–4.
- Convention: a straight-line approach is described by where the part **starts**
  ("from +Z" = the part starts 40–60 mm above its seat and travels −Z). A
  straight-line path is reversible, so each row is both the install and the
  removal check. Primed rows are controls: the same part on the opposite
  approach, printed so that "0.0000" cannot mean "the probe missed".

### 0. Part inventory, export integrity (B10), static interference — **all pass**

```
PART EXPORTS (r11) STEP volume vs independent trimesh census of the shipped STL
part                     nsol   STEP cm3    STL cm3      d%  watertight winding euler nonman open bodies
agitator                    1      4.291      4.288  -0.053      True    True      2     0     0     1
bay_lid                     1      8.598      8.598  +0.001      True    True    -10     0     0     1
brush_holder                1      3.544      3.544  +0.001      True    True      0     0     0     1
chute_plug                  1      6.721      6.718  -0.037      True    True     -2     0     0     1
count_windows               4      0.104      0.104  -0.041      True    True      8     0     0     4
electronics_bay             1     21.175     21.175  +0.002      True    True     -8     0     0     1
fill_cap                    1      7.349      7.347  -0.035      True    True      0     0     0     1
hopper                      1    109.419    109.423  +0.004      True    True    -14     0     0     1
meter_housing               1    103.659    103.623  -0.035      True    True    -12     0     0     1
pocket_disc                 1     72.686     72.661  -0.034      True    True    -30     0     0     1
retaining_plate_chute       1     71.867     71.850  -0.024      True    True    -48     0     0     1
sensor_boards               2      1.287      1.287  -0.012      True    True      4     0     0     2
sensor_cover                2      3.234      3.234  +0.000      True    True     -4     0     0     2
service_stand               1    103.908    103.892  -0.015      True    True      0     0     0     1
top_plate                   1     95.322     95.299  -0.023      True    True    -38     0     0     1
TOTAL printed STEP = 613.161 cm3
dispenser_r11_assembly.stl: watertight=True winding=True euler=-169 bodies=24 vol=587.193 cm3 nonmanifold_edges=0 open_edges=0
assembly STEP solids = 24
ALL-PAIRS EXACT BOOLEAN INTERFERENCE (assembly STEP, 24 solids, 276 pairs):
  44 bbox-overlapping pairs boolean-checked, 0 with non-zero intersection
```

The build notes' §10 claim — "15/15 part STLs watertight, 0 non-manifold edges,
0 open edges, assembly 24 bodies for 24 solids, worst STL-vs-STEP volume error
0.053 %" — **reproduces exactly**, including which part carries the worst error
(`agitator`, −0.053 %). B10 stays closed.

### 1. Derived assembly order, with swept-volume obstruction numbers

Exact boolean against every already-installed solid at every station; "SWEPT" is
a true fused union of the intermediate poses booleaned against those same
obstacles (printed where the member is small enough for the union to converge;
where it is not, the station count is doubled to 41–42 instead and that is said).

| # | Operation | Starts from | Stations | Station-max | Swept-union | Verdict |
|---|---|---|---|---|---|---|
| 1 | `meter_housing` in fixture | — | — | — | — | datum |
| 2 | igus JFM-2023-07 into the roof bore | **+Z**, 40 mm | 42 | **0.0000** | **0.0000** | OK |
| 2′ | (same, from below) | −Z | 42 | 580.5963 @ t = 6.83 | 2073.4860 | not possible |
| 3 | `brush_holder` + `brush_strip` radial slide-in | **θ = 148°, outboard** | 42 | **0.0000** | **0.0000** | OK |
| 4 | `pocket_disc`, hub up through the bearing | **−Z (travels +Z)**, 40 mm | 42 | **0.0000** | (n/a) | OK |
| 4′ | (same, from above) | +Z | 42 | 29600.4275 @ t = 12.68 | (n/a) | not possible |
| 5 | `agitator` onto the Ø15 hex | **+Z**, 40 mm | 42 | **0.0000** | **0.0000** | OK |
| 6a | `count_windows` ×2/side, from inside the chute bore, pushed out | radial out, 12 mm | 26 | **0.0000** (+Y and −Y) | **0.0000** | OK |
| 6a′ | (same, fitted from outside — control) | radial in | 26 | 36.6647 @ t = 2.40 | 192.9470 | not possible |
| 6b | `sensor_boards` ×1/side into the cavity | **±Y outboard**, 20 mm | 22 | **0.0000** | **0.0000** | OK |
| 6c | `sensor_cover` ×1/side | **±Y outboard**, 25 mm | 22 | **0.0000** | **0.0000** | OK |
| 6d | motor+gearbox onto the plate | **from below**, 40 mm | 22 | **0.0000** | (n/a) | OK |
| 6d′ | (same, from above) | +Z | 22 | 3287.5698 | (n/a) | not possible |
| 6e | PTFE thrust washer into its plate counterbore | **+Z**, 20 mm | 22 | **0.0000** | **0.0000** | OK |
| 6e′ | (washer fitted from below with the motor) | −Z | 22 | 316.6725 @ t = 2.86 | 2541.2029 | not possible — the washer is **not** part of the motor sub-assembly |
| 6f | 4 × gearbox screws | +Z into the countersinks | — | **0.0000** (flat head) | — | **A-10 CLOSED**, §3 |
| 7 | drive cartridge (plate+motor+washer+2 covers+2 boards+4 windows) into the housing, 60 mm ascent, at −22° of unlock, disc counter-indexed −22° | **from below** | 26 | **0.0000 vs every installed solid** | (n/a) | OK |
| 7′ | (same at 0 / −14 / −18 / −26° vs the housing alone) | — | 26 | 203.2654 / 101.6327 / 26.1181 / 47.4874 | — | not possible |
| 7b | rotate the cartridge −22° → 0° to lock | rot, 1° | 28 | **0.0000 over −24…0°**; 11.692 at −25 and at +1 | — | OK |
| 10 | `electronics_bay` onto the housing ribs | **−Y**, 40 mm | 22 | **0.0000** | (n/a) | OK |
| 11 | `bay_lid` | **−Y**, 30 mm | 22 | **0.0000** | **0.0000** | OK, removable in situ |
| 11′ | (lid pushed inboard) | +Y | 22 | 4087.6681 @ t = 27.14 | 18640.8270 | not possible, as designed |
| 12 | `hopper` down over the bay riser | **+Z**, 60 mm | 26 | **0.0000** | (n/a) | OK |
| 13 | `top_plate` onto the hopper flange **(NEW r11 geometry: R8 elbow + −Y spigot to z = −248.55)** | **+Z**, 40 mm | 26 | **0.0000** | (n/a) | OK |
| 14 | clip plate + blind-mate PCB | **+Z**, 30 mm | 22 | **0.0000** | **0.0000** | OK |
| 15 | `fill_cap` — rotate 90°, lift 12 mm, +Y 60 mm | 3 legs | 19/25/25 | 11.6387 / 14.9239 / **0.0000** | — | see NB-11 |
| 16 | `chute_plug` (ground only) | +Z | — | **83.5035 fitted, in 1 body** | — | press fit, §4 |
| 17 | `service_stand` (ground only) | — | ∩ every assembly solid = **0.0000** | — | — | OK |

All 15 exported printed parts appear in that order. The **new r11 geometry does
not break the order**: `top_plate`, whose bottom now reaches z = −248.55 because
of the −Y conduit spigot, still drops straight onto the hopper flange at
**0.0000 mm³ over 26 stations of a 40 mm descent**, and `hopper` still drops over
the bay riser at 0.0000 over 60 mm. Two order facts remain *forced*, not chosen:
the bearing cannot go in from below (**580.5963**) and the disc cannot go in from
above (**29600.4275**), so the disc can only be fitted before the drive cartridge.

**Cartridge service removal from the fully built machine** (members = plate +
motor + washer + 2 covers + 2 boards + 4 windows; obstacles = *every* other
solid, including bay, lid, hopper, top plate and clip plate):

```
  unlock -22 deg + 60 mm descent, disc as assembled     : station-max 4.6955 mm3 at dz=-0.00
  same, with pocket_disc counter-indexed -22 deg        : station-max 0.0000 mm3
  cartridge ^ service_stand at every station to 60 mm   : 0.0000 mm3
```

That reproduces r4's 4.6955 / 0.0000 / 0.0000 to four decimals. The documented
drop-out path is real and it clears the `service_stand`, so the cartridge can be
dropped with the machine in its own rest position.

### 2. Torque path — motor → gearbox → shaft → metering disc: **EXISTS and closes**

The shaft profile is a **nearest-surface** radial ray sweep at 1°, taking the
**first** surface along the inward ray. Printed here as a method control,
because taking the far-side exit instead (which I did first, by mistake) reports
`flat arc 0 deg` at every height — i.e. it hides the D-flat and reports a plain
Ø6 shaft, which is exactly the artefact that let r6 ship a round bore:

```
 motor/gearbox solid V = 69.926 cm3, bb z -418.450 .. -337.250
 SHAFT, first surface along the inward ray, 1 deg:
   z -353.000 / -352.000 / -350.000 / -349.500 / -349.300 : r_min 2.998..2.999  r_max 3.000  flat arc   0 deg
   z -349.200 / -348.750 / -344.750 / -340.750 / -338.000 / -337.300 : r_min 2.500  r_max 3.000  flat arc  64 deg (171..234)
 DISC D-BORE, rays from the axis outward at 1 deg:
   z -350.000 / -349.500 / -349.300 : r 3.049..3.050 round (lead-in)
   z -349.200 / -348.000 / -344.000 / -340.000 / -337.000 / -335.800 : r_min 2.550  r_max 3.050  flat arc 64 deg (171..234)
 shaft flat starts z = -349.2500 (bisected to 1e-4)   disc bore flat starts z = -349.2500 (bisected to 1e-4)
 shaft top z = -337.250    disc bore ceiling z = -335.7500  -> shaft-end clearance 1.500 mm
 FLAT-ON-FLAT ENGAGEMENT = 12.000 mm ; flat chord 2*sqrt(3.0^2-2.55^2) = 3.161 mm -> 37.93 mm2 of bearing
 grub corridor (B2.2), continuous void on the grub axis r 2.75 -> 52.0 vs EVERY assembly solid:
     Dia2.6 -> 0.0000 mm3 ;  Dia3.0 -> pocket_disc 10.9956 ;  Dia3.4 -> pocket_disc 23.5619 ;  Dia4.0 -> meter_housing 11.9431 + pocket_disc 174.3174
 grub corridor CONTROL, disc mis-clocked +5 / +11.25 / +22.5 deg: 155.5630 / 160.1463 / 119.9557 mm3
 grub hole section along its own axis (probed laterally and vertically inside pocket_disc):
     r  3.0 ..  9.0 : lateral half-width 1.300  -> Dia2.600 thread-forming pilot
     r 10.0 .. 45.0 : lateral half-width 1.699..1.700 -> Dia3.400 clearance channel to the disc OD
     (the step falls between r 9.0 and r 10.0; at r 9.0 the vertical probe already reads 1.700)
 free-rotation bisection of the seated cartridge vs meter_housing:
     +theta first contact +0.51401 deg ; -theta first contact -24.51402 deg ; two-sided free band 25.0280 deg
 bearing seat bore (meter_housing, z -330.0 / -331.5 / -333.0 / -334.8): Dia 23.023 .. 23.030 (B9d asks <= 23.03: MET)
```

**B2.1, B2.2 and B2.3 pass on the exports.** The grub-corridor control is what
makes the 0.0000 meaningful: mis-clock the disc by one 22.5° station and the same
ray reads 119.9557 mm³.

**On the notes' open issue 6 (flat-on-flat 11.850 vs 12.000):** the notes are
right that the difference is probe resolution, and the resolved number is
**12.000 mm**. My shaft-flat start is found by ray-cast bisection to 1e-4
(−349.2500) rather than with a 0.3 mm probe cube, and it lands on the disc-side
flat start to the fourth decimal. The package should publish 12.000 mm.

### 3. A-10 — **CLOSED**, and I reproduce the closing numbers

`cad/BOM.md` line 70 now reads
`M3x8 ISO 10642 / DIN 7991 90 deg COUNTERSUNK, 2.0 mm hex`. The plate geometry
did not change, and it is the seat for exactly that head — re-probed
directionally on the screw axis (13, 0), all four directions agreeing to
0.003 mm:

```
  z=-351.200  +x=  none -x=  none +y=  none -y=  none      (above the plate)
  z=-351.300  +x= 3.050 -x= 3.050 +y= 3.049 -y= 3.049
  z=-351.600  +x= 2.750 -x= 2.747 +y= 2.747 -y= 2.747
  z=-351.900  +x= 2.450 -x= 2.447 +y= 2.448 -y= 2.448
  z=-352.200  +x= 2.150 -x= 2.147 +y= 2.148 -y= 2.148
  z=-352.600  +x= 1.750 -x= 1.750 +y= 1.749 -y= 1.749
  z=-353.000 / -354.000 / -355.100 : 1.699..1.700 constant  (the Dia3.40 shank hole, to the flange face at -355.250)
  vertical ray down at (13.0, 3.5), off the screw axis: plate top face z=-351.250, gearbox flange face z=-355.250 -> 4.000 mm of plate
```

The head-fit boolean the round-4 critique demanded, with its control:

```
  ISO 10642 flush FLAT HEAD x4 ^ EVERY other assembly solid (static, assembled clocking) = 0.0000 mm3
  ISO 10642 flush FLAT HEAD x4 ^ its own countersink in retaining_plate_chute        = 0.0000 mm3 (seat contact)
  Dia5.5x3.0 CAP-HEAD CONTROL x4 ^ pocket_disc (static)                              = 35.4607 mm3
  disc swept over one 45 deg spoke pitch, heads static (3 deg steps):
     0:  flat 0.0000 / cap  35.4607      3:  0.0000 /  50.4874      6:  0.0000 /  79.5471      9:  0.0000 / 108.2056
    12:  0.0000 / 135.3019     15:  0.0000 / 159.9948     18:  0.0000 / 181.2857     21:  0.0000 / 197.6265
    24:  0.0000 / 197.6265     27:  0.0000 / 181.2857     30:  0.0000 / 159.9948     33:  0.0000 / 135.3019
    36:  0.0000 / 108.2056     39:  0.0000 /  79.5471     42:  0.0000 /  50.4874     45:  0.0000 /  35.4607
```

**Flat head 0.0000 mm³ at all four holes and at every disc angle over one 45°
spoke pitch; the cap-head control never returns to zero.** A-10 is closed by the
BOM row and the geometry accepts it. My cap-head control reproduces the notes'
35.4607 / 197.6265 exactly because I model the head the same way they do (full
Ø5.5 × 3.0 seated where the cone lets it bear); the round-4 figures (8.8652 /
49.4066) are the same conclusion measured with the head allowed to sit deeper.
**The disagreement the notes declare in their §3 is real, it is a modelling
convention, and both readings say the same thing.** The grip statement in the
BOM row (4.000 mm plate, 4.000 mm of thread beyond it, "do NOT lengthen the
screw") matches my ray measurement of the plate at the bolt circle.

### 4. `chute_plug` — the r11 tether-lug fix, checked in my lane

```
  retaining_plate_chute ^ chute_plug (fitted pose) = 83.5035 mm3 in 1 bodies:
       83.5035 mm3  x[  20.85,  43.15] y[ -11.15,  11.15] z[ -389.000, -381.000]
  the DESIGNED press fit is the Dia22.3 land in the Dia22.0 bore over 8.0 mm = 2*pi*11.075*0.150*8.0 = 83.504 mm3
  chute_plug ^ EVERY OTHER assembly solid = 0.0000 mm3
  withdrawal along -Z: dz=0 -> 83.5035 | -2 -> 81.5416 | -5 -> 77.0340 | -10 -> 72.7172 | -20 -> 46.9729 | -30 -> 0.0000 mm3
```

**Round-4's NB-3 is closed.** r10 read 206.0993 mm³ in three body classes and
called all of it "the designed press fit"; r11 reads **one** body and it *is* the
press fit, to 0.0005 mm³ of the closed-form value. The plug still comes off on a
straight pull.

### 5. Fastener grip and thread engagement, ray-measured on the r11 exports

| joint | measured | verdict |
|---|---|---|
| gearbox flange → plate, **4 × M3×8 countersunk** | plate top face at the bolt circle z = **−351.250**, gearbox flange face **−355.250** → **4.000 mm** of plate; 90° countersink mouth Ø6.10 → shank Ø3.40 at −352.600 | **A-10 closed** |
| clip plate → top plate, **4 × M2×10 + RX-M2×4** | `top_plate` top face −181.550; **Ø2.500 lead −181.55…−184.10**, then **Ø3.200 insert bore −184.10…−188.10 = 4.000 mm**, then a Ø4.800 relief shaft open to −209.422. Grip (clip-plate head shoulder −177.600 → insert top −184.100) = **6.500 mm**, thread beyond grip **3.500 mm** = 87.5 % of the 4.0 mm insert | **B9a MET** (asks ≥ 3.2 mm) |
| top plate → hopper flange, **6 × M3×10 + RX-M3×5.7** | 6 clearance holes measured at **r = 74.000, Ø3.200** (θ = 15/75/135/195/255/315); hopper insert bore **Ø4.000 from −238.550 to −244.545 = 5.995 mm** | B9b asks 5.7 + 0.3 = 6.000 → **short by 0.005 mm**; call it met (NB-10) |
| hopper skirt tabs → housing, **M3×8** | housing OD r = 51.993…51.999, pilot bottom r = 46.988…46.999 at θ = 30/105/225 → **pilot 5.00 mm deep** | OK, unchanged from r10 |
| bay ribs → housing, **M3×20** | bay through-bore **Ø3.100 at (x = ±14.000, z = −337.100)**; head bears on the bay rib outer face **y = −64.000**; housing outer face **y = −50.080**; pilot floor **y = −45.000**. **GRIP 13.920 mm, ENGAGEMENT 5.080 mm** — but the screw tip lands at **y = −44.000** | **A-12**, below |
| bay lid, 4 × M3×8 | corridors clear at Ø12.0 on all four | OK |
| M5 ball plunger | bore **Ø5.199 over r 47.00…52.90 and Ø6.399 over r 53.00…63.00, unthreaded** | **BLOCKING A-11** |

### 6. Tool-access corridors — largest clear driver diameter per fastener

Cylinder on the fastener axis, starting at the head-bearing plane and extending
**away** from the joint; diameters stepped 1.5/2.0/2.5/3.0/3.4/4.0/5.0/6.0/8.0/
10.0/12.0 mm; the largest with a **0.0000 mm³** exact boolean against every other
assembly solid is reported, with the first blocking size and the parts that block
it.

```
  F1  4xM3 gearbox screws (13,0) +Z, IN SITU            max clear Dia 0.0 | Dia1.5 -> 15.7276 mm3 (meter_housing 12.7235, bearing 3.0041)
  F1  same at (0,13)                                    max clear Dia 0.0 | Dia1.5 -> 15.7276 mm3 (identical)
  F1b same, plate+motor+washer BENCH sub-assembly       max clear Dia 8.0 | Dia10.0 -> 2.1304 (thrust_washer)
  F2  M3x4 grub, key from the disc OD r46 outward       max clear Dia 3.4 | Dia4.0 -> 11.9432 (meter_housing)
  F2b M3x4 grub, hand space outboard r53                max clear Dia 4.0 | Dia5.0 ->  5.1053 (meter_housing)
  F3  M5 ball plunger, radial r63 (th=67.5)             max clear Dia12.0 | -
  F3b M3x6 stop pin, radial r58.8 (th=51)               max clear Dia12.0 | -
  F4  M3x8 skirt tabs th=30 / 105 / 225, radial         max clear Dia10.0 each | Dia12.0 -> 4.3712 (meter_housing)
  F5  M3x6 wiper end tab, radial r58.1 (th=148)         max clear Dia12.0 | -
  F6  M3x20 bay rib screws x=+/-14, -Y (LID ON)         max clear Dia 6.0 | Dia8.0 -> 74.7699 (bay_lid), both screws
  F6  same (LID OFF)                                    max clear Dia12.0 | -
  F7  4x M3x8 bay-lid screws (+/-29, z=-358.868/-315.0) max clear Dia12.0 each | -
  F8  6x M3x10 flange screws r74, th=15+60k, +Z         max clear Dia12.0 each | -
  F9  4x M2x10 mount screws (+/-19,+/-19), +Z           max clear Dia 4.0 each | Dia5.0 -> 13.9439 (clip_plate's own head pocket)
  F10 4x M2x6 sensor-cover screws x=34.5, +/-Y          upper pair Dia12.0 | lower pair Dia 6.0, Dia8.0 -> 3.6757 (retaining_plate_chute)
```

Every fastener except the in-situ gearbox screws takes at least a Ø4.0 driver.
**F1 in situ = Ø0.0 for the fifth round running and F1b on the bench = Ø8.0** —
this reproduces the notes' §8 pair exactly, and it is the reason the motor is
fastenable and removable only as the plate+motor cartridge, which is what the
quarter-turn latch is for.

### BLOCKING A-11 — the M5 detent plunger has no thread and no insert; it cannot be installed

`cad/BOM.md` orders `M5x0.8 ball-nose spring plunger, LIGHT (2.5 N)` (COTS table
line 48, fastener table line 72). Measured on `meter_housing_r11.stl` along the
plunger axis (θ = 67.5°, z = −343.75), lateral half-width vs radius at 0.1 mm
steps, transitions only:

```
   r= 46.90: half-width 2.984      <- entering the bore from the chamber side
   r= 47.00: half-width 2.600      -> Dia5.200 over r 47.00 .. 52.90
   r= 53.00: half-width 3.199      -> Dia6.398 over r 53.00 .. 63.00 (housing OD)
   r= 63.00: none                  (breaks out of the housing OD)
   perpendicular vertical probe agrees to 0.001 mm at every radius: this is a round hole, not a thread form
```

There is **no thread anywhere on that axis** — the section is constant to
0.001 mm over both steps, which is what a plain bore looks like and is not what
a modelled thread looks like. And there is **no M5 insert in `cad/BOM.md`**:
grepping the whole file for `Ruthex|insert|RX-M` returns only
`RX-M2x4` (×4, mount bosses) and `RX-M3x5.7` (×6, hopper flange). So an
M5×0.8 threaded plunger, whose major diameter is 5.000 mm, is being asked to
retain itself in a **Ø5.199** hole that opens into a **Ø6.398** counterbore. It
drops straight through. On the alternative reading — that the plunger is meant to
be a smooth-body press fit — a Ø5.199 bore on a Ø5.000 body is a 0.199 mm slip
fit and it still drops through.

This is punch-list **B9c verbatim**, still open: *"Detent plunger has nothing to
thread into: bore measured Ø5.10–5.20, a clearance hole, unthreadable for M5 …
Either a modelled thread-forming boss (Ø4.2–4.6 ± 0.1 over ≥ 6 mm) or a modelled
nut/insert pocket with the part in the BOM."* Neither exists on the r11 export.
B9 is a **BLOCKING** punch-list item that the list says must be closed by
geometry, and the detent is **96.5 of the 190.7 mN·m** reaction budget, so it is
not optional: without it the quarter-turn latch has only the 2.4573° stop-pin
band and 25.0280° of free rotation to hold the cartridge against drive reaction.

**The cheapest close is probably already half-modelled.** The Ø6.398 × 10.00 mm
outer section is very close to a Ruthex **RX-M5×9.5** seat (OD 6.4 mm, length
9.5 mm) — 0.5 mm over-length and 0.002 mm under on diameter. If that is the
intent, the fix is (a) an M5 insert line in the BOM and (b) trimming the seat to
the insert length; if it is not, the fix is a Ø4.2–4.6 thread-forming boss over
≥ 6 mm. Either way it must be **printed, not narrated**: the closing evidence is
the bore section re-measured on the export plus an insertion sweep, and the F3
corridor is already Ø12.0 clear so tool access is not the problem.

### MAJOR A-12 (non-blocking) — the M3×20 bay screw is 1.000 mm longer than its pilot, and the pilot is already open into the metering chamber

Two separate defects on the same axis, both measured on `meter_housing_r11.stl`
(which is byte-identical to r10, so this is a pre-existing miss of mine from
round 4, not an r11 regression — round 4 measured the grip and stopped at the
pilot bottom).

**(a) The pilot floor is not there.** The pilot is bored from −Y into a wall
whose inner face is *curved*, so the flat-bottomed bore breaks out over part of
its section. Rastering the bore cross-section at 0.02 mm and casting a +Y ray at
every sample:

```
pilot at x=+14.0, z=-337.100, measured bore radius 1.20 mm, 0.02 mm raster:
   OPEN (ray passes straight through the housing wall)   1.2492 mm2 of   4.5124 mm2 =  27.7 %
   pilot-floor y over the closed part: -45.000 (flat)    chamber wall inner face at this x: y = -44.856
pilot at x=-14.0 : OPEN 1.2480 mm2 of 4.5124 mm2 = 27.7 %
```

So each of the two bay screws sits in a hole that is **27.7 % open into the
metering chamber** before the screw goes in, and where it is closed the floor is
only **0.144 mm** thick — one FDM layer. Total open area chamber→outside
**2.4972 mm²**. The bay-rib boss around the bore is solid (`electronics_bay`
material runs y −64.000…−50.18 all round the bore), so this does **not** open
into the sealed bay interior — but it is an unsealed path from the granule
chamber to the outside air under the screw head, and B5's "sealed, dust-tight"
language should not be read as covering it.

**(b) The specified screw is 1.000 mm too long.** Grip 13.920 mm + pilot
5.080 mm = **19.000 mm of usable length**; the BOM (line 64) orders **M3×20**:

```
  head bearing plane y=-64.000 (bay rib outer face) -> tip lands at y=-44.000
  pilot floor y=-45.000 ; chamber wall inner face at the screw axis y=-44.850 (bore R 46.984 at x=14)
  -> the tip protrudes 0.850 mm past the bore wall, into the disc running clearance
  meter_housing bore radius at z=-337.100: min 46.984 max 47.000 (180 azimuths)
  pocket_disc OD           at z=-337.100: min 45.984 max 46.000
  running clearance disc OD -> housing bore = 0.984 mm
  screw tip radius from the meter axis = 46.174 mm -> radial clearance to the disc = 0.174 mm
  modelled M3x20 (Dia3.0 shank + 60 deg point) ^ pocket_disc = 0.0000 mm3 at the assembled clocking
                                                and 0.0000 mm3 worst over a 22.5 deg index (3 deg steps), both screws
  5280 sample points on the protruding cone, signed distance to pocket_disc: closest approach 0.1867 mm
  control, M3x18 (tip at y=-46.000, inside the pilot): ^ meter_housing 6.2089 mm3/screw vs M3x20's 10.9561 mm3/screw
```

**It does not jam** — 0.0000 mm³ against the disc at every clocking, closest
approach 0.187 mm — which is why this is a MAJOR and not a blocker. But 0.187 mm
is the clearance between a rotating disc and the point of a *thread-forming*
screw that has been driven through a 0.144 mm membrane, i.e. through the exact
condition that raises a breakthrough burr, and the printed radial tolerance on
an FDM CF-PETG part is not 0.187 mm. **M3×18 keeps the tip inside the pilot
(4.080 mm of engagement, 1.36 × D) and costs nothing.** The BOM row's parenthesis
("this gives 5.08 mm") is true and incomplete: it does not say what the other
1.000 mm of the screw does.

### MODERATE A-13 (non-blocking) — the one driver row in the BOM cannot drive the grub it names

`cad/BOM.md` line 71: `| 1 | 2.0 mm hex key, >= 60 mm shaft | gearbox
countersunk screws (A-10) AND the M3x4 grub, which has to be pushed 43.00 mm
radially down a Dia3.4 channel …`. An M3 hex-socket set screw (ISO 4026 /
DIN 913/914/916) takes a **1.5 mm** key across flats; 2.0 mm is the M4 size, and
it is also the correct size for the M3 ISO 10642 countersunk screw. **One key
cannot be both.** Round-4's NB-7 asked for a ≥ 60 mm **1.5 mm** key and noted that
A-10 would add a 2.0 mm requirement — two rows, not one. Geometry is fine either
way (the grub channel takes Ø3.4 and the Ø2.6 pilot takes a 1.5 mm key shaft
easily), so this is a BOM line, but as written the shipped tool list cannot build
the machine. NB-7 is **not** closed.

For the record, the grub joint itself measures correct and is buildable: the disc
carries a **Ø3.400 clearance channel from the OD (r 45) in to r ≈ 9.5** and a
**Ø2.600 thread-forming pilot from r ≈ 9.5 in to r 2.75**, landing on the shaft
flat at r 2.550; the M3×4 grub therefore ends up fully inside the pilot with
2.75 mm of empty pilot behind it, and the key must reach r ≈ 6.75, i.e.
**45.25 mm** of radial travel from the housing OD at r 52. That is the retrieval
hazard round 4 named, and it is unchanged.

### Non-blocking, measured

- **NB-9 — B9b is 0.005 mm short and has been for four rounds.** Hopper flange
  insert bore Ø4.000 from −238.550 to **−244.545 = 5.995 mm** against
  RX-M3×5.7 + 0.3 = 6.000 mm. Met for practical purposes; say so once in the BOM
  instead of leaving a reader to find the 0.005.
- **NB-10 — the notes carry round-4's lash figure; I re-derived it and it holds.**
  `BUILD-NOTES-r5.md` §8 states 0.5141° and says it is carried, not re-measured.
  Bisected independently on the r11 exports: **+θ first contact +0.51401°, −θ
  first contact −24.51402°, two-sided free band 25.0280°**. The carried number is
  correct to 1.4 × 10⁻⁴ degrees. It is still not in the count-contract text.
- **NB-11 — the fill-cap removal residual is unchanged geometry, and my numbers
  differ from round 4's for a stated reason.** With the cap axis taken as the
  bbox centre (0, 43.45) — an **ASSUMPTION**, the cap bbox is 54.9 mm in y
  against a 54 mm circle, so a lug skews it — the rotation leg reads 11.6387 mm³
  at 90° and 1.02–1.59 mm³ over 5–60°, and the lift leg 14.9239 mm³, against
  round 4's 1.4338 / 0.0000. The residual is **entirely against `top_plate`**, and
  running the identical sweep against `top_plate_r10` gives **the same value to
  four decimals at every angle** (0.0000 / 1.4209 / 1.3560 / 1.1351 / 1.0191 /
  1.5947 / 4.2559 / 11.6387 at 0/5/15/30/45/60/75/90°). So the r11 elbow and
  strain-relief boss did **not** touch this, and the difference from round 4 is my
  assumed rotation axis, not a regression. N5's detent residual stays declared.
- **NB-12 — `service_stand` clearance re-measured: 8.000 mm.** Stand ground plane
  z = **−426.450**; lowest solid in the assembly is the **motor can at −418.450**
  (lowest *printed* material −418.300); stand ∩ every assembly solid =
  **0.0000 mm³**. Reproduces the notes' §8 figure.
- **NB-13 — B9d re-measured: bearing seat Ø23.023…23.030** at z = −330.0 / −331.5
  / −333.0 / −334.8 against the igus JFM-2023-07 OD 23.00 and the punch list's
  ≤ Ø23.03. Met, with 0.000–0.007 mm to spare; it is a tolerance item, not a
  margin.
- **NB-14 — the stop-pin pilot was not re-derived this round.** My radial probe at
  the stated axis (θ = 51°, z = −353.25) did not land in the bore, so I have no
  independent number for it; round 4's `pin ∩ housing 4.3118 mm³ (Ø3.0 in a Ø2.6
  thread-forming pilot), pin ∩ plate 0.0000` is **carried, not re-measured**, and
  is labelled as such. The half of the reaction path I *did* re-derive this round
  is the latch free band (25.0280°), above.

### What I need to see next round to clear "assembly"

1. **A-11 closed by geometry:** either a modelled thread-forming boss
   (Ø4.2–4.6 ± 0.1 over ≥ 6 mm) or a modelled M5 insert seat **with the insert in
   `cad/BOM.md`**, with the bore section re-printed from the export at 0.1 mm
   steps (a failing part looks like the Ø5.199/Ø6.398 pair above) and a plunger
   insertion sweep at 0.0000 mm³.
2. **A-12:** the bay screws re-specified at **M3×18** with the tip-vs-disc
   boolean and the closest-approach distance re-printed, and the pilot floor
   either closed (wall thickened / bore shortened) or the open **2.4972 mm²**
   written into the sealing text so no document claims that joint is dust-tight.
3. **A-13:** two driver rows in the BOM — a **1.5 mm** hex key ≥ 60 mm for the
   M3×4 grub and a **2.0 mm** hex key for the countersunk gearbox screws.
4. §1, §2, §5 and §6 of this critique re-printed from the tools, not asserted:
   the order table's 0.0000s with their controls, **12.000 mm** of flat-on-flat
   (not 11.850 — the probe artefact is resolved), the F1 = Ø0.0 / F1b = Ø8.0 pair,
   and the grip figures 13.920 / 4.200 / 6.500 / 5.000 / 4.000.
5. NB-10 (0.51401° of lash) and NB-12 (8.000 mm stand clearance) written into the
   service and count-contract text with those numbers.

---

## integration

**Owner:** integration-and-serviceability critic (directives 2, 3, 4; punch-list
**B5, B6, B11, B12**, plus ground clearance / envelope).
**Verdict: BLOCKING FAIL — 1 blocking finding (I-1).**
(a) reach-in corridor **PASS**, (c) refill workflow **PASS**, (d) ground
clearance / envelope **PASS**, (e) mass ledger **PASS on the CONTEXT dry
target, TIGHT on the package's own loaded headline**.
(b) electronics bay **PASS on the bay itself and on the interface→bay leg
(the round-4 blocker is genuinely closed), FAIL on the bay→motor and
bay→count-sensor legs**, which are solid printed material.

**Method.** Everything below is my own measurement on the shipped `*_r11`
exports, made without importing `dispenser.py`: OCC solid classification and
exact booleans on the STEP files (`build123d` 0.11.1 / OCP), `trimesh` 5.0.0 on
the STLs, `scipy` KD-trees for mesh-to-mesh separations. Bores and cavities are
**found** by enumerating the analytic surfaces of the exported B-rep and by
scanning, not by being told where they are. `[A]` marks an assumption I
introduce. Where I disagree with round-4 or with `BUILD-NOTES-r5.md`, both
numbers are printed.

---

### I-1 — BLOCKING: the cartridge harness duct (bay → motor, bay → both count boards) is solid printed material

Directive 2 requires "a routed wiring channel from the interface PCB to the bay
**and from the bay to motor + count sensor**". The first half is now real (see
(b)). The second half is not: every leg of the modelled duct network in
`retaining_plate_chute_r11` is **solid on its own axis**. This is the same class
of defect as the round-4 elbow blocker, in the segment round 5 did not re-test.

Axis occupancy, `retaining_plate_chute_r11.step`, OCC solid classifier at 0.25 mm
steps (a passing part reads 0/N):

```
exit leg     (0,y,-363.25)      y -48.0 -> -32.5        63/  63 axis points INSIDE printed material (100.0 %)
collector -Y (x,-32.5,-363.25)  x -32.5 -> 14          187/ 187 axis points INSIDE printed material (100.0 %)
return leg   (-32.5,y,-363.25)  y -32.5 -> 32.5        261/ 261 axis points INSIDE printed material (100.0 %)
collector +Y (x,+32.5,-363.25)  x -32.5 -> 14          187/ 187 axis points INSIDE printed material (100.0 %)
vertical leg (14,-32.5,z)       z -363.25 -> -414.30   205/ 205 axis points INSIDE printed material (100.0 %)
vertical leg (14,+32.5,z)       z -363.25 -> -414.30   205/ 205 axis points INSIDE printed material (100.0 %)
low run  -Y  (x,-32.5,-414.30)  x 14 -> 41             109/ 109 axis points INSIDE printed material (100.0 %)
low run  +Y  (x,+32.5,-414.30)  x 14 -> 41             109/ 109 axis points INSIDE printed material (100.0 %)
sensor lateral -Y (41,y,-414.30) y -32.5 -> -22.5       41/  41 axis points INSIDE printed material (100.0 %)
sensor riser -Y  (41,-22.5,z)   z -414.30 -> -389       15/ 102 axis points INSIDE printed material ( 14.7 %)
sensor riser +Y  (41,+22.5,z)   z -414.30 -> -389       15/ 102 axis points INSIDE printed material ( 14.7 %)
motor branch (0,-32.5,z)        z -363.25 -> -412.45   197/ 197 axis points INSIDE printed material (100.0 %)
motor stub   (0,y,-412.45)      y -32.5 -> -22.0        43/  43 axis points INSIDE printed material (100.0 %)
```

Largest conductor that can traverse each leg (cylinder swept on the leg axis,
exact boolean vs the plate; a clear leg reads 0.000 mm³):

```
exit leg         Dia1.0:    12.174 mm3   Dia2.0:    48.695 mm3   Dia4.0:   194.779 mm3
collector -Y     Dia1.0:    36.521 mm3   Dia2.0:   146.084 mm3   Dia4.0:   584.336 mm3
vertical leg -Y  Dia1.0:    40.095 mm3   Dia2.0:   160.378 mm3   Dia4.0:   641.513 mm3
motor branch     Dia1.0:    38.642 mm3   Dia2.0:   154.566 mm3   Dia4.0:   618.265 mm3
sensor riser +Y  Dia1.0:     2.788 mm3   Dia2.0:    11.153 mm3   Dia4.0:    44.611 mm3
-> LARGEST CONDUCTOR bay -> motor = Dia0.0 ; bay -> either count board = Dia0.0
```

A Ø1.0 cylinder 15.5 mm long is 12.17 mm³ = 100 % of its own volume inside the
part: there is no bore at all, not a small one.

Three independent methods agree, point by point (OCC classifier on the STEP,
`trimesh.contains` on the STL, and a Ø1.0 sphere boolean whose full volume is
0.5236 mm³):

```
point                     OCC-inside  trimesh-contains  sphereØ1∩rp(mm3)
  (0, -40, -363.25)          True       True               0.5236
  (0, -32.5, -380.0)         True       True               0.5236
  (0, -32.5, -400.0)         True       True               0.5236
  (-32.5, 0, -363.25)        True       True               0.5236
  (14, 32.5, -390.0)         True       True               0.5236
  (30, 32.5, -414.3)         True       True               0.5236
  (41, 22.5, -400.0)         False      False              0.0000   <- the sensor CAVITY, the only free point on the list
```

Cross-sections through the duct confirm it is a solid rod, not a tube:

```
z= -380.00 x-scan at y=-32.5: material [-4.00,4.00] [10.00,18.00]     (motor branch Dia8 solid, vertical leg Dia8 solid)
z= -363.25 x-scan at y=-32.5: material [-36.50,18.00]                 (collector run, 54.5 mm of continuous material)
z= -363.25 y-scan at x=14:   material [-36.50,-28.50] [28.50,36.50]
```

And the count boards cannot even leave their own cavity: the Ø5 cable port under
each board is open from the cavity floor down to z = −410.750 and then runs into
the solid duct stub, i.e. it is a **blind pocket**:

```
z-scan (41,+22.5): plate material [-385.00,-388.05] [-410.75,-418.30]
z-scan (41,-22.5): plate material [-385.00,-388.05] [-410.75,-418.30]
```

Free-space topology of the part as a whole, which is the one-line version of all
of the above:

```
retaining_plate_chute_r11: free-space bodies in its own bounding box + 2 mm = 1
   OUTSIDE AIR  782182.165 mm3   X[-57.30,54.00] Y[-54.00,54.00] Z[-420.30,-349.25]
-> the part contains ZERO enclosed voids. There is no duct in it.
```

**Why this got through.** `BUILD-NOTES-r5.md` §2 measures **coverage** of the
route (8 lateral rays per millimetre) and prints `100.0 % covered … cartridge
duct, bay end -> x=0 collector`, `100.0 % … sensor duct +Y`, `93.9 % … motor
branch`. A solid rod scores 100 % on a lateral-enclosure test — enclosure and
**patency** are different questions, and only the top-plate legs got the patency
test (§2's Ø5.5 sweep and checker §8 both stop at the bay riser). The model's own
B5.4 line even calls the object "duct **solid**". Round 4's blocker was closed by
adding a patency test to one leg; the same test was never extended to the other
nine.

**Cost of the fix is negative in mass** (measured): a Ø5.0 bore swept along the
whole modelled network is 7862.9 mm³, of which **7861.0 mm³ is printed material**
= **9.98 g of CF-PETG** that comes out when the bore is actually cut.

**What I need to see to clear I-1:** the same axis-occupancy table above reading
0/N on every leg, a Ø4.0 bundle swept bay→motor and bay→each count board at
**0.0000 mm³**, the sensor port opening into a through duct (not a blind pocket),
and the duct-bore volume re-printed with the plate volume dropping ≈7.9 cm³.

---

### (a) Gloved-hand access corridor to the quick-release (directive 3 / B6) — **PASS**

**The corridor I require, and why.** `[A]` **95 mm wide × 45 mm tall × 130 mm
deep**, top at the clip-plate underside, measured **from the neck face outward**:

- **95 mm wide** — 95th-percentile adult male hand breadth across the metacarpals
  ≈ 90 mm, plus a light mechanic's glove ≈ 2–3 mm per side. `[A: anthropometric
  figure quoted from memory, not from a table I opened; closure = a tape measure
  on a gloved hand, or one sentence from Thomas.]`
- **45 mm tall** — 95th-percentile hand thickness at the metacarpals ≈ 34 mm plus
  glove and knuckle working clearance. `[A, same closure]`
- **130 mm deep** — the hand must pass the release and the forearm follow it. `[A]`

These are deliberately the same three numbers as PUNCHLIST B6.2 and as rounds
1–4, so the series is comparable.

```
payload top face Z = -181.550   (clip-plate underside; clip plate 50.00 x 50.00 x 10.50 from
                                 interface/mechanical/2112_attach_plate_payload_side.step)
material OUTSIDE the 48.0 x 48.0 neck column tops out at:
    top_plate  Z = -225.050        <- limiting (the -Y harness strain-relief boss)
    fill_cap   Z = -230.700
    hopper     Z = -238.550
STAND-OFF HEIGHT h = 43.500 mm                (B6.1 target h >= 40)
neck plan half-extent a = 24.000 mm (48.00 x 48.00 outer, 2.5 mm walls, cavity 42.80 x 42.80)
                                              (B6.1 target a <= 35)

CORRIDOR BOOLEANS (from the neck face outward, top at Z = -181.550, vs all flight solids)
    95 x  45 x 130 mm: +X 0.0000   -X 0.0000   +Y 0.0000   -Y 340.2241 (top_plate)
    95 x  52 x 130 mm: +X 0.0000   -X 0.0000   +Y 536.3662 (fill_cap)   -Y 2627.7999 (top_plate)
   100 x  50 x 130 mm: +X 0.0000   -X 0.0000   +Y 159.9689 (fill_cap)   -Y 2007.7415 (top_plate)
   110 x  45 x 130 mm: +X 0.0000   -X 0.0000   +Y 0.0000   -Y 340.2241 (top_plate)

LARGEST CLEAR CORRIDOR PER SIDE (130 mm deep, top at Z = -181.550, bisected to 0.01 mm)
   +X: 52.00 mm tall at 95 mm wide ; >= 300 mm wide at 45 mm tall
   -X: 52.00 mm tall at 95 mm wide ; >= 300 mm wide at 45 mm tall
   +Y: 49.15 mm tall at 95 mm wide ; >= 300 mm wide at 45 mm tall
   -Y: 43.50 mm tall at 95 mm wide ;    0.00 mm wide at 45 mm tall (blocked on the centreline)
```

**B6.2 is met**: three sides — including the two opposing sides +X and −X — are
clear at **0.0000 mm³**, and +X/−X are clear at the full 52 mm, 7 mm more than my
requirement. Only −Y is obstructed, by the strain-relief boss, and even there
43.50 mm is clear. This reproduces round 4 exactly (0.0000/0.0000/0.0000/340.2241
and h = 43.500, a = 24.000); round 5 did not regress it.

**B6.3 (QR actuation sweep) remains NOT VERIFIABLE on this package.** The release
mechanism is the drone-side half (`interface/mechanical/README.md`: "it clips
into the aircraft's fixed half by hand"), which lives above Z = −171 and is not
in these exports. Clip plate 50.00 × 50.00 on a 48.00 × 48.00 neck leaves
**1.00 mm of proud edge per side** — enough to see, not a finger grip. Recorded
as not verified, not as passed.

**B6.4 no regression on the aircraft side:** `dispenser_r11_assembly.stl` max
Z = **−171.0500**, **0 vertices above Z = −171.000**.

---

### (b) Electronics bay and wiring routes (directive 2 / B5)

#### B5.1 board fit — **PASS**

Bay interior recovered by scanning (no model constant used): inboard wall
y −64.000…−62.000, lid inner face y = −88.600, side walls |x| 26.000…28.000,
floor z −358.100…−356.100; four M2.5 standoff bosses at (±18.0, z = −323.100 /
−351.100) whose seat faces are at **y = −69.000, i.e. 5.000 mm proud of the
inboard wall** (ECO-7 asks ≥ 4).

```
BOARD ENVELOPE 42 (x) x 34 (z) x 12 (y) seated on those faces, X[-21,21] Y[-81,-69] Z[-354.10,-320.10]
   ^ electronics_bay = 0.0000 mm3     ^ bay_lid = 0.0000 mm3        (B5.1 asks 0.000)
six clearance gaps (grow one face at a time to first contact, bisected 0.01 mm):
   +X  5.000 mm   -X  5.000 mm   +Z (up) 1.800 mm   -Z (down) 2.000 mm   -Y (lid) 7.600 mm
   +Y  0.000 mm  <- this face IS the standoff seat (mounting datum); the inboard WALL is 5.000 mm behind it
cavity 52.0 (x) x 24.6 (y) x 37.8 (z) mm   (ELECTRONICS 7 asks 46 x 22 x 38)
```

(Round 4 read +Z 1.950 / −Z 1.850 because they centred the board on z = −337.25;
I centre it on the midpoint of the two standoff rows, z = −337.100. Same
geometry, 0.150 mm of convention.)

#### B5.2 three cable entries — **PASS on count and size, with two corrections to round 4**

```
(1) top riser socket (aircraft harness): x-scan at y=-81, z=-310 -> material [-5.200,-3.700] [3.700,5.200]
    -> bore Dia7.400, land (10.4-7.4)/2 = 1.500 mm             (B5.2 asks land >= 1.5)
(2) motor entry, inboard (+Y) face: x-scan at y=-63, z=-350.1 -> material [-20,-15] [-5,5] [15,19.98]
    -> a 10.000 mm clear opening centred on x = +10
(3) count-sensor entry: the mirror opening centred on x = -10
    plug tests through the 2.000 mm inboard wall at x = +10:
       Dia 5.9 -> 0.0000   Dia 6.0 -> 0.0000   Dia 7.0 -> 0.0000
       Dia 9.9 -> 0.0000   Dia10.0 -> 0.0000   Dia11.0 -> 33.0785 mm3
    -> the entries are PLAIN Dia10.000 holes through a 2.000 mm wall
-X face of the bay, x-scans at y=-78, z=-320/-330/-340/-350: material [-28,-26] [26,28] only
    -> there is NO opening on -X
```

Two corrections: round 4 reported these entries as "Ø6.000 through, Ø10.000
grommet counterbore, land 2.000 mm" — measured on r11 there is **no Ø6 through
section**, the hole is Ø10.000 for the full 2.000 mm wall, so the grommet's
retaining land is the wall thickness itself. And `ELECTRONICS.md` §6.2 ECO-6 (and
PUNCHLIST B5.2) put the aircraft harness on **−X**; the geometry puts it on the
**top riser**. Three entries exist and the route works, but the document and the
part disagree about which face.

#### B5.3 gasket groove — **PASS**

```
bay sealing land y = -90.000; groove floor y = -88.800  -> DEPTH 1.200 mm   (B5.3 asks >= 1.0)
fine x-scans across the groove at z = -337.25 / -320.0 / -355.0:
   open from x 25.210 to 26.790 -> WIDTH 1.580 mm at all three (B5.3 asks >= 1.5)
mid-groove slab (y -89.60..-89.40) decomposed into free bodies:
   291.200 mm2 plan area  X[-26.80,26.80] Z[-357.40,-316.80]   <- ONE closed rectangular ring
   1656.000 mm2 cavity mouth (46.0 x 36.0), 4 x 4.909 mm2 lid-screw holes OUTSIDE the ring
-> closed loop, no interruptions; centreline perimeter 2*(52.0+39.0) = 182.00 mm
```

#### B5.6 lid removable in situ — **PASS**

```
bay_lid translated -Y by 0.5 / 1 / 2 / 4 / 8 / 12 / 16 / 20 mm vs every other flight solid: 0.0000 mm3 at every station
4 x Dia6 x 25 mm driver columns at (+/-29.0, z -315.10 / -359.10) vs all solids except bay+lid:
   0.0000  0.0000  0.0000  0.0000 mm3
```

#### B5.5 interface → bay: the round-4 blocker is **CLOSED**, independently confirmed

The two bores are found as analytic faces of the exported B-rep (r = 3.000 along
−Y at z = −230.550 spanning y −81…−21; r = 3.000 along Z at x = 0, y = −81
spanning z −248.6…−230.5), and both are open:

```
HORIZONTAL BORE AXIS (x=0, z=-230.550), y -19 -> -85 at 0.25 mm: NO SOLID POINT before y=-81 (the turn)
VERTICAL BORE AXIS   (x=0, y=-81.000), z -230.55 -> -249 at 0.25 mm: NO SOLID POINT
ELBOW CENTRELINE ARC R8.0, centre (0,-73.000,-238.550), 91 points 0..90 deg: NO SOLID POINT
Dia5.5 bundle swept along the discovered route, exact OCC boolean:
   horizontal leg y -21..-73 (top-plate conduit)        ^top_plate 0.0000  ^hopper 0.0000  ^bay 0.0000 mm3
   R8.0 elbow quarter turn                              ^top_plate 0.0000  ^hopper 0.0000  ^bay 0.0000 mm3
   vertical spigot -> hopper conduit -> bay riser       ^top_plate 0.0000  ^hopper 0.0000  ^bay 0.0000 mm3
   TOTAL 0.0000 mm3          (r10, measured by me last round: 2.535 / 213.825 / 166.308)
   Dia6.0 whole route 4.5893 mm3 ; Dia6.5 332.9175 ; Dia7.0 691.5442
-> largest conductor bundle that crosses the elbow = Dia5.5   (r10: Dia0.0)
```

#### B5.4 no wiring in the granule space (interface→bay leg) — **PASS, and it is structural, not incidental**

```
CONDUIT LATERAL CLOSURE (36 probes per station on a ring just outside the bore):
   top-plate horizontal conduit, y -22..-80 at 1 mm: 36/36 closed at every station except
       y -75..-80, where the ring opens into the elbow's own vertical bore (by design)
   vertical spigot, z -239..-248.5 (top_plate):      ALL 36/36 CLOSED
   hopper conduit, z -241..-310 (hopper):            ALL 36/36 CLOSED
   bay riser socket, z -307..-318 (bay):             ALL 36/36 CLOSED
WALL BETWEEN THE HOPPER-SIDE CONDUIT AND THE TANK (y-scan inward from the bore wall):
   z=-245: hopper material y [-75.50,-69.50]  = 6.00 mm      z=-275: [-75.50,-68.00]  = 7.50 mm
   z=-260: [-75.50,-70.00] = 5.50 mm                          z=-290: [-75.50,-62.15] = 13.35 mm
   z=-305: [-75.50,-60.05] = 15.45 mm
FLOOR BETWEEN THE TOP-PLATE CONDUIT AND THE TANK (z-scan below the bore, x=0):
   y=-35 / -50 / -65: top_plate material [-233.55,-235.60] = 2.05 mm of continuous plate
JOINT: at z=-244 the top_plate spigot occupies y -85.50..-76.50 (Dia9) inside the hopper socket
   y -88.00..-70.02 -> a telescoping, covered handover, not a butt joint
```

The conduit is outside the tank by construction — it runs on top of the plate and
then down a spigot at y = −81.000, which is outboard of the Ø156 tank — so the
interface→bay harness cannot enter the granule volume.

#### Channel cross-sections, measured (B5.5 asks for these)

Fill fractions are for 9 × 26 AWG PTFE, OD ≈ 1.05 mm → 7.79 mm² `[A: bundle
composition from ELECTRONICS §6.3]`.

| segment | measured section | area | 9-cond. fill |
|---|---|---|---|
| neck cavity (blind-mate PCB → neck base) | 42.80 × 42.80 mm | 1831.8 mm² | 0.4 % |
| neck −Y wall exit slot | 6.000 (x) × 6.020 (z) mm | 36.1 mm² | 21.6 % |
| top-plate conduit + R8.0 elbow + spigot | Ø6.000 | 28.27 mm² | 27.6 % (12 cond. 36.8 %) |
| hopper-side conduit | Ø11.000 | 95.03 mm² | 8.2 % |
| bay riser socket | Ø7.400 | 43.01 mm² | 18.1 % |
| bay motor entry / sensor entry | Ø10.000 through a 2.000 mm wall | 78.54 mm² | 9.9 % |
| cartridge duct, bay → motor / count boards | nominal Ø5.000 = 19.63 mm² | **0.00 mm² (solid, I-1)** | **n/a** |

#### Non-blocking in (b)

- **N-i4 — the grommets and the bay gasket are not orderable.** The groove is
  real geometry (1.580 × 1.200 mm, 182.00 mm loop) and the three entries are real
  openings, but `cad/BOM.md` contains **no grommet line and no bay gasket cord**
  (grep: the only sealing parts are the fill-cap O-ring, ID 43.6, and the
  chute-plug Dyneema tether). Both appear only inside the **mass reserve**
  ("grommets ×5 + bay gasket cord, 6.0 g"), which is by definition not in the
  ledger and not in the BOM. As shipped, the "dust-tight bay" is a groove with
  nothing in it and three Ø10 holes with nothing in them. PUNCHLIST B5.7 asks for
  the grommet seats *and their masses* in the BOM.
- **N-i5 — ECO-6 vs the part.** ELECTRONICS §6.2 says the aircraft harness enters
  "through the modelled 4 × 16 × 9 cutout on the −X face"; measured, the −X face
  is unbroken and the harness enters through the Ø7.400 top riser. One of the two
  documents is wrong.
- **N-i6 — the coverage metric cannot see a blocked route.** §2 of the build
  notes replaced a parameter roll-up with a lateral-ray measurement, which was the
  right fix for the *coverage* claim, but coverage is 100 % for a solid rod (I-1).
  Coverage and patency must be printed as a pair, per leg, for every leg.

---

### (c) Refill workflow (directive 4 + RT-14 / B12) — **PASS**

**There is no side-wall fill port** — I checked rather than assumed:

```
hopper_r11, azimuth sweep at 2 deg x r 60..78 for a gap in the tank wall:
   z=-250: 0 of 180 azimuths open    z=-280: 0 of 180
   z=-260: 0 of 180                  z=-290: 0 of 180
   z=-270: 0 of 180
```

B12 allows "an equivalent measured solution", and the route taken is the
top-plate port plus the printed `service_stand`:

```
FILL PORT on top_plate_r11 (axis x=0, y=+43):
   y-scan x=0, z=-238.00: material [10.000,20.000] [66.000,78.000] -> clear aperture 46.000 mm in y
   x-scan y=43, z=-238.00: material [-34.820,-20.000] [20.000,32.400] -> 40.000 mm across the bayonet lugs
   largest column with 0.0000 mm3 (bisected) = Dia40.000
   Dia46.0 column -> 57.0541 mm3   <- round 4 called this "clear aperture Dia46.0"; it is not clear, the lugs are in it
   -> Dia40.000 clear = 3.33 x the Dia12 granule
FILL-CAP REMOVAL (fill_cap_r11 vs every other flight solid):
   pure axial lift 0.0 -> 0.0000 | 0.5 -> 14.6145 | 1.0 -> 32.8827 | 1.5 -> 32.8827 | 2.0 -> 14.6145
                   2.5 -> 0.0000 | 3.0 -> 0.0000 | 5.0 -> 0.0000 | 8.0 -> 0.0000 | 10.0 -> 0.0000
                  14.0 -> 0.0000 | 14.5 -> 0.2573 (the cap reaches the stand-off neck)
   lift 10 mm then translate +Y 5/10/15/20/25/30 mm: 0.0000 mm3 at every station
```

So the cap comes off with a **snap-over of 32.8827 mm³ peak elastic interference
across 0.5–2.0 mm of lift**, then 11.5 mm of free axial travel and unlimited +Y
travel. That is a workable one-handed refill; it is **not** the "pure-axial
extraction" the BOM row implies, and the 32.9 mm³ should be named as a designed
snap, with its insertion/extraction force, in the ops text.

```
REST POSITION on service_stand_r11 (103.892 cm3, 132.0 g, ground-support equipment):
   stand ground plane Z = -426.450 ; assembly lowest point Z = -418.450
   -> the gearbox can stands 8.000 mm OFF the ground: the load path does NOT pass through the
      gearbox output flange                                            (B12.1 satisfied)
   contact patch (300 000 surface samples each body, KD-tree at 1.0 mm):
      406 payload samples, all at Z -358.25..-357.27, r 52.28..71.83 -> the meter-housing latch-ring underside
      contact azimuths present: 50-60, 170-180, 290-300 deg -> THREE pads, support polygon = a triangle, area 6740 mm2
   stand ground footprint: annulus r 75.98..90.00, hull area 25 436 mm2
   EMPTY CG rebuilt from the exports (see (e)) = (1.67, -7.37, -327.96)
   TIP ANGLE, dispenser + stand tipping as a unit  (pivot = stand footprint edge 82.41 mm, CG 98.49 mm up)
      EMPTY 39.92 deg | @250 38.48 deg | @421 36.35 deg
   TIP ANGLE, dispenser tipping off the three pads (pivot = pad-triangle edge 33.49 mm, CG 29.31 mm up)
      EMPTY 48.81 deg | @250 44.15 deg | @421 38.03 deg
   (B12.1 asks >= 25 deg [A: 15 deg of ranch-tailgate slope + margin])
```

A note on method, because round 4's 40.44° was right for the wrong reason: it
took the support polygon from the **stand's own ring** (r 76–90) while measuring
the contact patch at r 52–72. Those are two different pivots and they must not be
mixed — with h taken from the ground plane and d from the contact patch the
answer would be 19.07°, which is not a real failure mode either. Both consistent
readings are printed above and both pass.

**Still true and still worth writing down:** B12 closes **only** because of
`service_stand`. It is now correctly called out as mandatory GSE in `cad/BOM.md`.

---

### (d) Ground clearance and overall envelope — **PASS**

```
dispenser_r11_assembly.stl: 136 520 faces, watertight=True, 24 bodies, 587.193 cm3
   bbox X[-78.000,78.000] Y[-92.000,78.000] Z[-418.450,-171.050]
   plan envelope 156.00 (x) x 170.00 (y) mm ; max radius from the mount axis 97.944 mm
   stack below the mounting plane = 247.450 mm
   B6.4: 0 vertices above Z = -171.000 (max Z = -171.0500)

GROUND CLEARANCE, on the real landing gear
   quiver.airframe_structure.landing_gear.assembly.make_assembly()
   gear bbox X[-293.57,293.57] Y[-250.00,250.00] Z[-547.89,-124.94] -> ground plane Z = -547.890
   ground clearance at rest = -418.450 - (-547.890) = 129.440 mm        (required >= 40; 3.2x)
   PAYLOAD <-> LANDING GEAR minimum separation, mesh-to-mesh
      (gear tessellated at 0.2 mm -> 155 758 faces / 135 367 vertices; 200 000 surface samples per
       body, KD-tree) = 103.659 mm                                      (r6: 83.41; round 4: 103.628)
```

Prop clearance: I did not re-measure it this round; `BUILD-NOTES-r5.md` §9
measures it for the first time (vertical 152.55 mm, in-plan 232.63 mm,
vertex-to-vertex 374.90 mm) and corrects the carried in-plan figure by 6.7 mm.
Carried, not independently reproduced.

---

### (e) Mass ledger, rebuilt from the exports — **PASS on the CONTEXT dry target; TIGHT on the package's own loaded headline**

Volumes are my own `trimesh` reads of the shipped r11 STLs; densities per
PUNCHLIST B11.1 (CF-PETG **1.27**, TPU 1.19, PMMA 1.18). COTS masses are carried
from `cad/BOM.md` / the r11 ledger and are **not** measurements — each is placed
at the centroid of its own body in the assembly where one exists.

```
PRINTED, FLIGHT CONFIG, 100 %-INFILL BASIS
   top_plate                  95.299 cm3 x 1.27 =  121.03 g   centroid ( -0.05,  -4.07, -223.45)
   fill_cap                    7.347 cm3 x 1.27 =    9.33 g   centroid ( -0.16,  42.79, -235.42)
   hopper                    109.423 cm3 x 1.27 =  138.97 g   centroid ( -0.04,  -3.46, -273.57)
   meter_housing             103.623 cm3 x 1.27 =  131.60 g   centroid (  5.77,   0.49, -339.15)
   pocket_disc                72.661 cm3 x 1.27 =   92.28 g   centroid (  0.11,   0.05, -342.89)
   agitator                    4.288 cm3 x 1.19 =    5.10 g   (TPU)
   brush_holder                3.544 cm3 x 1.27 =    4.50 g
   retaining_plate_chute      71.850 cm3 x 1.27 =   91.25 g   centroid ( 11.98,  -1.03, -373.88)
   electronics_bay            21.175 cm3 x 1.27 =   26.89 g
   bay_lid                     8.598 cm3 x 1.27 =   10.92 g
   sensor_cover (x2)           3.234 cm3 x 1.27 =    4.11 g
   count_windows (x4)          0.104 cm3 x 1.18 =    0.12 g
   PRINTED FLIGHT SUBTOTAL                        636.10 g
   (service_stand 103.892 cm3 / 132.0 g and chute_plug 6.718 cm3 are ground-only and correctly excluded)

COTS / ESTIMATE (carried from cad/BOM.md; none of it is measured geometry)
   clip_plate (alu, STEP 11.523 cm3 x 2.70)   31.10 g      stepper (vendor GROSS)      350.00 g
   blind-mate PCB + Molex J1                  15.00 g      sensor PCBs x2                6.00 g
   electronics (MCU/CAN/TMC2209/buck/count)   65.00 g      fasteners + inserts + plunger 57.00 g
   O-ring + gaskets + 9 magnets                8.00 g      strip brush                   3.00 g
   sleeve bearing igus JFM-2023-07             1.70 g      PTFE thrust washer            0.70 g
   COTS/ESTIMATE SUBTOTAL                     537.50 g

   EMPTY (solid printed basis)               1173.60 g     (model prints 1173.8 -- reproduces to 0.2 g)
   + 10 % CAD contingency                     117.36 g
   EMPTY, CARRIED (= the DRY figure)         1290.96 g   vs CONTEXT <= 1500 g DRY -> MARGIN +209.04 g   PASS
   + 250 granules x 1.18 g                    295.00 g
   LOADED @250, 100 %-infill basis           1585.96 g   (margin  -85.96 g)
   + 421 granules (max-fill rib)              496.78 g
   LOADED @421, 100 %-infill basis           1787.74 g   (margin -287.74 g)
   EMPTY CG (mass-weighted, measured centroids) = (1.67, -7.37, -327.96)
```

Readings:

1. **The CONTEXT requirement is on dry mass** and it passes with **+209.04 g**.
   The package's headline is a *loaded* number graded against the dry ceiling,
   which is stricter than CONTEXT asks.
2. I reproduce the model's 100 %-infill ledger to **0.2 g** and do **not** dispute
   the shipped slicer-realistic headline (1435.1 g, +65 g; with the 61.0 g reserve
   1496.1 g, **+4 g**). Round 5 is genuinely mass-neutral: my `top_plate` reads
   95.299 cm³ against r10's 95.755 (the elbow), `retaining_plate_chute` 71.850
   against 71.886 (the lug).
3. **I-1 is the only item in this critique that moves mass, and it moves it the
   right way:** cutting the duct bores removes **7861.0 mm³ = 9.98 g**. That is
   2.5× the whole +4 g headline-with-reserve margin, so the fix pays for itself.
4. Estimate exposure is unchanged and large: **537.50 g of the 1173.60 g empty
   subtotal (45.8 %) is COTS/estimate**, of which 350 g is a vendor *gross*
   catalogue figure that has never been on a scale. The 10 % contingency
   (117.36 g) does not bound that.

---

### Summary for the round

| item | verdict | headline number |
|---|---|---|
| (a) reach-in corridor (directive 3 / B6) | **PASS** | 95 × 45 × 130 clear at **0.0000 mm³** on +X, −X and +Y; h = **43.500 mm**, a = **24.000 mm** |
| (a) B6.3 QR actuation sweep | **NOT VERIFIABLE** | release half is drone-side, above Z = −171; clip-plate edge proud of the neck = **1.00 mm/side** |
| (b) the bay itself (B5.1/.2/.3/.6) | **PASS** | board **0.0000 mm³**, gaps 5.000/5.000/1.800/2.000/7.600; entries Ø7.400 + 2 × Ø10.000; gasket **1.580 × 1.200 mm**, closed loop, 182.00 mm; lid sweep 0.0000 mm³ |
| (b) interface → bay (round-4 blocker) | **CLOSED** | elbow arc, both bore axes: **NO SOLID POINT**; Ø5.5 sweep **0.0000 mm³** on all three legs; largest bundle **Ø5.5** |
| (b) bay → motor / count sensors | **BLOCKING FAIL (I-1)** | every duct leg **100 % solid on its axis**; largest conductor **Ø0.0**; sensor cable port is a **blind pocket** ending at z = −410.750 |
| (b) harness vs granule space | **PASS (upper leg)** | conduit closed 36/36 at every station; ≥ **5.50 mm** of hopper wall and **2.05 mm** of plate floor between the bore and the tank |
| (c) refill / rest position (B12) | **PASS** | clear port **Ø40.000** (Ø46.000 between lugs); cap free above **2.5 mm** of lift; can **8.000 mm** off the ground; tip angle **39.92°** empty / **36.35°** at 421 |
| (d) ground clearance / envelope | **PASS** | **129.440 mm** ground, **103.659 mm** to the real landing gear, **0** vertices above Z = −171.000 |
| (e) mass ledger | **PASS (dry) / TIGHT (loaded)** | dry carried **1290.96 g** vs 1500 (**+209.04**); loaded @250 **1585.96 g** solid basis; shipped headline 1435.1 g, with reserve 1496.1 g (**+4 g**) |

**Required to close the round on integration:** cut the cartridge duct bores so a
conductor can actually reach the motor and both count boards, and re-print the
axis-occupancy table, a Ø4.0 bundle sweep at 0.0000 mm³ per leg, and the
7.9 cm³ volume drop. Add the grommets and the bay gasket cord to `cad/BOM.md`
(N-i4) — as shipped, nothing seals the bay that this round proved is sealable.
