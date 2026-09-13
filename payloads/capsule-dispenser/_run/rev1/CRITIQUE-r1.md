# REV-1 ROUND 1 — CRITIQUES

## count-sensor

**Owner:** count-sensor geometry critic (rev-0 RT-3 / rev-1 punch-list **B4**).
**Verdict: NOT CLOSED — 4 blocking items.** The ECO-3/ECO-9 aperture geometry is
genuinely in the exports for the first time (r6 had none of it), but ECO-4 is not
achieved as specified, one of the two sensor boards cannot be installed, and the
BOM has not been touched.

**Provenance of every number below:** measured by me on
`cad/exports/*_r7.step` / `*_r7.stl` with
`~/.openclaw/workspace/venvs/dock-cad-314/bin/python` (build123d 0.11.1 exact
B-rep booleans; trimesh 5.0.0 ray casting for the aperture maps). I did not read
build notes for these numbers — `_run/rev1/BUILD-NOTES-r1.md` **does not exist**
at the time of this critique (only the rev-0 `_run/BUILD-NOTES-r1..r6.md`).
Note also `cad/dispenser.py` mtime **10:16:37** > `cad/BOM.md` **10:08:04** >
`cad/exports/*_r7` **10:04:37** — the source has been edited since the exports I
measured, so the source may already differ from what is checked here.

Datum: `Z_SENSOR` measured on the export as the mid-plane of the two beams =
**−385.250**; chute bore Ø22.000 on the axis **x = 32.000** (= PCD_R).

---

### PASS — what is actually in the geometry (measured)

**ECO-3 aperture count and position — PASS.** Aperture census by exact B-rep
slab boolean (0.2 mm slab through each boss, 25 × 19 mm boss section = 475.000 mm²
if solid):

| slab | material area | missing | = n × Ø3.2 (8.042 mm²) |
|---|---|---|---|
| +y, inner tunnel run (y = 13.0) | 458.915 mm² | 16.085 mm² | **2.00** |
| +y, labyrinth run (y = 15.75) | 458.915 mm² | 16.085 mm² | **2.00** |
| +y, at the cavity floor (y = 16.9) | 458.915 mm² | 16.085 mm² | **2.00** |
| −y, inner tunnel run | 458.915 mm² | 16.085 mm² | **2.00** |
| −y, labyrinth run | 458.915 mm² | 16.085 mm² | **2.00** |
| −y, at the cavity floor | 458.915 mm² | 16.085 mm² | **2.00** |

→ **4 tunnels total, 2 per side.** Axes measured by 40-step bisection on the STL:

| beam | side | tunnel centre (x, z) | Ø_x | Ø_z |
|---|---|---|---|---|
| A | +y | **29.0001, −382.2500** | 3.1998 | 3.1994 |
| A | −y | **29.0001, −382.2500** | 3.1998 | 3.1994 |
| B | +y | **35.0001, −388.2500** | 3.1998 | 3.1994 |
| B | −y | **35.0001, −388.2500** | 3.1998 | 3.1994 |

Exact diameter on the STEP: a Ø3.20 coaxial probe in the inner run gives
**0.00000 mm³**, Ø3.25 gives 0.53191 mm³ → the tunnels are exactly **Ø3.200**
(spec Ø3.2 ± 0.1 ✓).

- **Chord offsets from the bore axis: −3.000 / +3.000 mm** ✓ (ECO-3 x = 29 / 35).
- **ECO-9 vertical stagger = |−382.250 − (−388.250)| = 6.000 mm** ✓.
- Both sides on the **same x/z grid**, so each beam is a straight chord along y ✓.
- The r6 single centred aperture is **gone**: a ray along y at (x = 32.000,
  z = −385.250) finds solid material from the bore wall |y| = 11.000 out to the
  cavity floor |y| = 17.000 on both sides.
- Boss walls (measured, from boss z-extent −394.750…−375.750 and the bisected
  aperture edges): **4.900 mm above beam A, 2.801 mm between A and B, 4.900 mm
  below beam B.**

**B4.3 boss envelope / motor clearance — PASS.** Boss material bbox measured on
the STEP: **x 22.000…47.000, |y| 11.000…25.000, z −394.750…−375.750**.
Boss x-min = **22.000** ≥ 22.0 ✓. On the assembly STEP the `stepper` solid in
that z-band measures **x_max = 17.600** → **measured clearance = 4.400 mm**
(required ≥ 4.0; r6 was 1.4). Corridor check: stepper material in
x 17.8…22.0, |y| 11…25, z Z_S ± 9.5 = **0.0000 mm³**.

**ECO-5 labyrinth — PRESENT and dimensionally correct.** Outer run of every
tunnel measured at y = ±15.8: centre **x = 29.8001 / 35.8001**, i.e. offset
**+0.800 mm in x** over the outer **2.5 mm** (y 14.500…17.000, read off the ray
hits), leaving a **0.800 mm ledge** (punch list asks ≥ 0.7) ✓.

**Windows exist as a part.** `count_windows_r7.step` = **4 solids**, each
Ø5.900 × 0.950 PMMA at (29.000, ±11.500, −382.250) and (35.000, ±11.500,
−388.250), total 0.104 cm³ = 0.12 g @ 1.18 g/cm³. Interference with
`retaining_plate_chute_r7` = **0.000000 mm³**. Nothing is proud of the bore
(closest window point to the bore axis = 11.025 > 11.000).

**B4.8 chute continuity — PASS.** Against `retaining_plate_chute_r7 +
count_windows_r7`: Ø13.0 sphere on the chute axis at z = −381.00 / −382.25 /
−385.25 / −388.25 / −390.00 → **0.00000 mm³** each; Ø13.0 × 50 swept column
(z −395.25…−345.25) → **0.00000 mm³**.

**B4.6 board envelope, +y side — PASS.** ECO-3 nominal 20 × 8 × 12 pocket:
**0.0000 mm³**. 18 × 12 × 2 board + 1 mm all round (20 × 4 × 14): **0.0000 mm³**.

**Mass.** `retaining_plate_chute` 37.747 → **45.833 cm³** (47.9 → **58.2 g** @
CF-PETG 1.27). Sensor bosses alone: r6 2 × 1724.8 = 3449.6 mm³ → r7 4159.8 +
4221.8 = **8381.6 mm³**, i.e. **+6.26 g** — ECO-3's "+6 g [J]" estimate holds.

**Recorded deviation, judged acceptable:** the boss is **25 × 14 × 19 mm**, not
ECO-3's verbatim `Box(20,12,14)`. ECO-3's own arithmetic does not close — a 6.0 mm
stagger plus Ø3.2 apertures plus the "4 mm of wall above and below" it claims
needs ≥ 17.2 mm of height, not 14. The built 19 mm delivers the measured 4.900 mm
walls above/below. **ELECTRONICS.md §4.3/ECO-3 should be corrected to 19 mm**, and
the mass line updated from +6 g (which happens to still be right, measured 6.26 g,
because the boss is hollowed by the 20.4 × 9.0 × 14.4 cavity).

---

### BLOCKING 1 — the −Y sensor board cannot be installed: the B5 harness duct runs through its cavity

The B5 wiring duct (OD 8.0 / ID 5.0 at x = 32.0, y = −27.0, z −385.25…−345.25) was
added to the solid **after** the sensor cavity was cut, so it re-fills the mouth of
the −y component cavity.

| check (exact STEP boolean) | +y side | −y side |
|---|---|---|
| material intruding into the modelled cavity (x 24.3…44.7, \|y\| 17…26, z −392.45…−378.05) | **0.000 mm³** | **93.245 mm³** (3.53 % of the 2643.8 mm³ pocket), bbox x 28.127…35.873, y −26.000…−23.000, z −385.250…−378.050 |
| ECO-3 nominal 20 × 8 × 12 pocket | 0.0000 mm³ | **53.8523 mm³** |
| 18 × 12 × 2 board + 1 mm all round, seated | 0.0000 mm³ | **62.6574 mm³** |
| **insertion sweep**: 18 × 12 × 2 board swept along y from \|y\| = 40 to \|y\| = 18 | **0.000 mm³** | **203.418 mm³**, bbox x 28.000…36.000, y −31.000…−23.000, z −385.250…−379.250 |

Board-plane sweep on the −y side (2 mm board, 18 × 12): clear at |y| = 18.5, 19.5,
20.5, 21.5 (0.0000 mm³), then **7.8483 mm³ at 22.5**, **39.1463 mm³ at 23.5**,
**53.8523 mm³ at 24.0**. Point map of the cavity mouth at y = −24.5 (x = 25…43,
`X` = material): clear at z = −391.0/−388.0/−385.5, **blocked x ≈ 29…35 at
z = −384.0/−381.0/−379.0**.

So a rigid 18 × 12 board physically cannot be passed into the −y boss: the free
mouth is L-shaped (full 20.4 mm width only below z = −385.25, and 24.3…28.1 /
35.9…44.7 above it). One of the two count-sensor boards has nowhere to go.
**Fix direction:** cut the duct after the cavity, or move the duct's vertical leg
off x = 32 / to |y| > 26, or make the duct's lower leg the cavity's own cable exit
with a proper grommeted port. Whatever is done, re-run the insertion sweep.

### BLOCKING 2 — ECO-4 is not achieved: the windows sit behind an unswabbable printed lip, not flush with the bore

ECO-4 (§4.5 measure 5, and the ECO table) requires the window at the **bore face,
y = ±11, flush with the chute wall**, so "the fouling surface *is* the chute wall,
swabbable from the chute exit". Punch-list B4.4 restates it as "floor **flush with
the chute bore wall at |y| = 11.0 ± 0.05**".

Measured on the export:

- Window seat is **Ø6.000** ✓ but its floor is at **|y| = 12.000** — the seat is
  **1.000 mm deep, not 0.4 ± 0.05** (the model comment says this is deliberate,
  because the window is 1 mm thick; ECO-4's "0.4 mm chamfered recess" is genuinely
  ambiguous and the built 45° chamfer is 0.800 × 0.800 mm, y = 10.600…11.400,
  radius 3.800 → 3.000). **Recorded as a spec-vs-model conflict that ELECTRONICS.md
  and the punch list must resolve — not the blocking part.**
- The blocking part: the seat is a **flat-bottomed pocket cut in a curved wall**,
  and it does not break through to the bore. The bore wall at the *aperture axes*
  (x = 29 / 35, i.e. 3.0 mm off the bore axis) is at **|y| = 10.583**, but the
  chamfer mouth only starts at **|y| = 10.600**. Measured lip thickness along y
  between the true bore wall and the seat mouth, at the beam-A height
  z = −382.250, +y side:

| x | true bore wall \|y\| | ray hits | **lip thickness** |
|---|---|---|---|
| 27.40 | 9.9920 | 9.990 / 10.600 | **0.6100 mm** |
| 27.80 | 10.1666 | 10.1632 / 10.600 | **0.4368 mm** |
| 28.20 | 10.3228 | 10.3192 / 10.600 | **0.2808 mm** |
| 28.60 | 10.4614 | 10.4589 / 10.600 | **0.1411 mm** |
| **29.00 (beam axis)** | 10.5830 | 10.5814 / 10.600 | **0.0186 mm** |
| 29.40 | 10.6883 | — | 0.0000 |
| 29.80 | 10.7778 | — | 0.0000 |
| 30.60 | 10.9105 | — | 0.0000 |

i.e. a printed wedge 0…0.610 mm thick stands across roughly **half** of every
aperture, and the PMMA window's inner face (|y| = 11.025) is **0.442 mm behind the
local bore surface** in a re-entrant annular pocket. That pocket is exactly where
fines will sit, and a swab rod run down the Ø22 bore cannot reach into it — the
ECO-4 maintenance path the whole revision was written to create is not there.
The lip is real B-rep geometry, not STL faceting (STL bore facet error is
0.0016 mm; the lip is up to 0.610 mm).

### BLOCKING 3 — consequence of 2: the beams are obstructed, and the two channels are not equal

**Punch-list B4.2 (Ø2.0 cylinder on each beam axis → 0.000 mm³): FAILS.**
Exact STEP booleans:

| cylinder | beam A | beam B |
|---|---|---|
| Ø3.20 × 34 (cavity face to cavity face, y ±17) | 14.6249 mm³ | 14.6250 mm³ |
| **Ø2.00 × 34** | **1.6675 mm³** | **1.6675 mm³** |
| Ø1.60 × 34 | 0.2460 mm³ | 0.2460 mm³ |
| Ø0.80 × 34 | 0.0346 mm³ | 0.0346 mm³ |
| Ø3.20 × 24 (window plane to window plane, y ±12) | 1.9595 mm³ | 1.9596 mm³ |
| Ø2.00 × 24 | 0.4743 mm³ | 0.4743 mm³ |
| Ø2.00 × **60** (the literal B4.2 test) | **16.1448 mm³** | **1.6675 mm³** |

The Ø2.0 × 60 breakdown names the culprits and the asymmetry exactly:

- beam A: 14.4774 mm³ at y −30.000…−23.536 = **the B5 harness duct** (outside the
  optical path, but it is on the beam line); 2 × 0.2371 mm³ at |y| 10.247…10.600,
  **x 28.000…29.061** = the bore lip; 2 × 0.5966 mm³ at |y| 14.500…17.000,
  **x 28.000…28.425** = the ECO-5 labyrinth ledge — **both on the −x side of the
  axis, so they overlap.**
- beam B: 2 × 0.2371 mm³ lip at **x 34.939…36.000 (+x side)**; 2 × 0.5966 mm³
  labyrinth ledge at **x 34.000…34.425 (−x side)** — **opposite sides, so they eat
  the aperture from both directions.** The labyrinth is offset +0.8 mm in absolute
  x on both beams, but the lip is mirror-symmetric about the bore axis, so the two
  features cooperate on beam A and fight on beam B.

Ray-cast clear-aperture map (0.02 mm grid over the nominal Ø3.2 aperture, path
from cavity face to cavity face, |y| < 16.9; nominal area 8.0425 mm²):

| | beam A | beam B |
|---|---|---|
| clear area, zero material in the path | **3.7340 mm² (46.4 %)** | **1.3760 mm² (17.1 %)** |
| clear area allowing ≤ 0.05 mm of material | 4.0128 mm² (49.9 %) | 1.6508 mm² (20.5 %) |
| clear-area centroid x | **29.7246** | **34.6324** |
| largest fully clear circle in the aperture | Ø2.2804 at (30.580, −382.390) | **Ø0.8400** at (34.620, −388.370) |
| largest clear coaxial cylinder, exact STEP | Ø1.5 at x = 29.72 → 0.0009 mm³ | Ø0.8 at x = 34.63 → 0.0006 mm³ (Ø1.0 → 0.1473 mm³) |
| material on the nominal beam axis (r < 0.03) | 0.0494 mm | 0.0489 mm |
| max material in the path inside r ≤ 1.6 | 1.2007 mm | 1.2007 mm |

Two consequences, both **[my calculation, from the measured clear apertures;
the modelling assumption that the effective chord sits at the clear-aperture
centroid is mine and is not in any source document]**:

1. **The two channels are not equivalent.** Aperture-limited coupling ratio
   3.7340 / 1.3760 = **2.71×**. §4.4's 182× excess gain becomes ≈ **84× (A)** and
   ≈ **31× (B)** if flux scales with clear aperture area (the PD is 7.5 mm², larger
   than the aperture, so it is aperture-limited). Still workable, but `beam_margin_pct`
   is now channel-dependent and the "two independent detectors degrade gracefully"
   argument is asymmetric by 2.7× before any dust lands.
2. **§4.3's lateral-coverage proof shifts.** Effective chord offsets from the bore
   axis become **−2.275 / +2.632 mm** instead of ±3.000. At the free-fall velocity
   measured from the geometry (40.0 mm drop → **885.9 mm/s**), guaranteed worst-case
   dark times:

| pellet | ECO-3 design chords ±3.000 | measured clear-aperture chords |
|---|---|---|
| Ø11 | **10.407 ms** (worst x₀ = 0.00) | **10.059 ms** (worst x₀ = −5.50, nearest chord 3.225 mm) |
| Ø12 | 11.731 ms | 12.069 ms |
| Ø13 | 13.018 ms | 13.590 ms |

   Against the §4.3 gate of 9.7 ms the Ø11 guarantee margin falls from **7.3 % to
   3.7 %**. Not fatal, but it erodes the separator the whole ECO-3 rework exists to
   create, and it is not written down anywhere.

**Note on B4.2 as written:** a Ø2.0 clear cylinder is *unachievable* with ECO-5 as
specified — two Ø3.2 bores offset 0.8 mm leave a lens of
2r²·acos(d/2r) − (d/2)·√(4r²−d²) = **5.51 mm² (68.5 % of nominal)**, whose
inscribed coaxial circle is Ø1.6 at best and Ø0.8 about the nominal axis. So the
punch list's B4.2 threshold and ELECTRONICS.md ECO-5 contradict each other and one
of them must be corrected. **That is not what fails here** — what fails is that
beam B is at **17.1 %** rather than the 68.5 % the labyrinth alone would cost,
because of the bore lip of Blocking 2. Fix the lip (cut the window seat through to
the bore surface) and both beams return to the symmetric 68.5 %.

### BLOCKING 4 — the BOM still specifies the rejected digital receiver, and the analog chain is absent

`cad/BOM.md` (header says "rev r7", written 10:08:04, after the r7 exports):

- line 29: `| IR count pair | Vishay TSSP4038 receiver + TSAL6200 emitter (940 nm) | ASSUMPTION |` — **the TSSP4038 §4.4 rejects is still there.** Source:
  `cad/dispenser.py:2959` (COTS table) and `cad/dispenser.py:2831`
  (`"TSSP4038+TSAL6200 IR pair, 2x DRV5032, wiring", 65.0`).
- **No `VBPW34FAS` line** (required ×2). **No `OPA2320` line.** **No PMMA
  Ø6 × 1 window line** (required ×4) — the `count_windows` part is exported and has
  a `basis` string in the model, but never reaches the BOM. **`TSAL6200` is not
  quantified ×2.**
- The printed-parts table has **10 rows** and omits **`count_windows`,
  `chute_plug`, `service_stand`**, all three of which are exported at r7
  (`PRINTED_AUX` at `dispenser.py:1715-1721` is exported but not tabulated).
- The fastener table still lists `| 2 | M3x4 cup-point grub | IR emitter/receiver
  retention |` — **that feature is not in the geometry** (see Blocking 5). The BOM
  orders a part for a hole that does not exist.

B4.7 therefore fails on every clause.

### BLOCKING 5 (same defect family as N3/ECO-12) — no board retention, either side

Measured: the top 2 mm slab of each boss (x 22…47, |y| 11…25, z −377.75…−375.75)
is **700.0 / 700.0 mm³ solid on +y** and **698.0 / 700.0 mm³ on −y** (the 2 mm³
is the duct outside the boss) — i.e. **no grub pilot, no clamp screw, no boss, no
retention feature of any kind** in either sensor boss. `dispenser.py:1376-1380`
says so explicitly ("no board-retention feature is modelled here… carried as an
open issue"). Two Ø6 × 1 mm windows per side are likewise unbonded/unretained (no
adhesive or retainer in the BOM). With the BOM simultaneously ordering two M3
grubs for retention, the shipped documentation and the shipped geometry disagree.
This is punch-list **N3** (nonblocking) by letter, but combined with Blocking 4 it
is a *documentation-integrity* failure (RT-19) and I am recording it as blocking
for this domain: either model the clamp or delete the grub line, and say which.

---

### Other measured facts the round must carry

- **The +y sensor board has no modelled cable route.** The duct exists only on −y;
  the −y cavity connects to the duct bore over **30.716 mm³** (x 29.709…34.291,
  y −26.000…−24.500, z −384.250…−378.050), so that board has an exit. The +y
  cavity opens only to free air at y = +25.000 and there is no channel, conduit or
  grommet seat between it and the electronics bay (bay bbox y −90.00…−48.96).
  Cable path length unrouted ≈ 74 mm. (Feeds B5, whose owner should confirm.)
- **`count_windows` is not in the assembly.** `dispenser_r7_assembly.step` has
  **16 solids**: clip_plate, top_plate, fill_cap, hopper, meter_housing,
  pocket_disc, thrust_washer, sleeve_bearing, agitator, brush_holder,
  brush_bristles, retaining_plate_chute, stepper, electronics_bay, bay_lid,
  blindmate_pcb. The windows, chute plug and service stand are exported but never
  enter the assembly compound (`dispenser.py:1723`), so no assembly-level
  interference check can see them.
- **`retaining_plate_chute_r7.stl` is NOT watertight** (r6 was). 22 212 faces,
  **3 non-manifold edges shared by 4 faces each**, all at
  **(0.284, −45.684, −345.246)** — the B5 duct / plate-underside junction, not the
  sensor bosses (which are clean). Euler characteristic −41 (r6: −28), 1 body.
  This is B10's item but it lands on the part the count sensor lives on.

---

### What has to change for me to pass this domain

1. Get the −y sensor board in: re-order the duct/cavity booleans or move the duct.
   Re-run the insertion sweep → 0.000 mm³ **both sides**.
2. Break the window seat through to the bore surface (cut the seat/chamfer against
   the Ø22 cylinder, not against a flat |y| = 11 plane) so the lip goes to 0.000 mm
   across the full Ø3.2 aperture on both beams. Re-print the lip table and the
   clear-aperture areas; target the symmetric labyrinth-limited 5.51 mm² / 68.5 %
   on both beams, and re-print the effective chord offsets.
3. Reconcile B4.2 (Ø2.0 clear) with ECO-5 (0.8 mm offset) in writing, with the
   measured lens area, and pick one.
4. BOM: delete TSSP4038; add VBPW34FAS ×2, OPA2320 ×1, TSAL6200 ×2,
   PMMA Ø6 × 1 window ×4 (+ bonding method); add `count_windows`, `chute_plug`,
   `service_stand` to the printed table; delete or model the 2 × M3×4 retention
   grubs.
5. Model board retention (ECO-12) or state plainly in README/DESIGN that the
   sensor boards are unretained, with the consequence.
6. Correct ELECTRONICS.md §4.3/ECO-3's boss height (14 → 19 mm; the doc's own
   4 mm-wall claim does not fit 14 mm) and its "flush at y = ±11" wording so it
   describes a seat cut against the bore cylinder.

## granule-path

**Verdict: FAIL — 2 BLOCKERs, 1 MAJOR, 3 MODERATEs, 1 MINOR.** The rev-0 pellet-path
mandate is *not* regressed on the fragment-jam requirement — B1 (roof through-slot)
and B8 (nose gap) are genuinely closed in the geometry, with numbers below — but the
r7 exports contain a new, worse containment failure: **the hopper has no lid**.

Scope note / provenance: `_run/rev1/BUILD-NOTES-r1.md` **does not exist** at review
time (2026-08-07 ~10:40), so there are no builder claims to check text against. All
numbers below are measured by me on `cad/exports/*_r7.stl` / `.step`
(timestamps 10:04:37), venv `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`,
trimesh ray-casting + face audits, independent of `dispenser.py`. Note
`cad/dispenser.py` was modified at **10:16:37, i.e. AFTER the exports were written** —
if the source has since changed, re-export before re-reading these numbers.
Z-stack measured on the exports: funnel/shelf −316.25, roof bottom −325.25,
**disc top −326.750**, disc bottom −340.750, plate top −341.250, plate bottom
−345.250, chute bottom −395.250.

### BLOCKER 1 — the hopper is open to the sky: `top_plate` (= hopper lid + B6 neck) is a 0.81 cm³ stub in the exports

`dispenser.py:259` calls the top plate "chassis adapter = hopper lid, one printed
part, now incl. neck" (48 × 48 × 52 mm neck, `NECK_H = 52`, `NECK_A = 24`). What was
exported is not that part:

- `top_plate_r7.stl`: **volume 0.81 cm³**, bbox **x −4.50…4.50, y −87.00…−78.00,
  z −238.55…−214.55** — a 9 × 9 × 24 mm tube (the top-plate harness conduit,
  `dispenser.py:792`). No Ø150 lid, no neck. (r6: `top_plate_r6.stl` = 61.25 cm³.)
- `hopper_r7.stl` has no top closure: vertical ray probes hit **nothing** at
  (0, 0), (0, 45), (0, −40); section at z = −232 contains material only at
  r ≥ 69.48.
- Whole-assembly test (`dispenser_r7_assembly.stl`, ray up from z = −240 on a 5 mm
  grid over the mouth, r ≤ 67): **368 of 561 cells have zero material above them.**
  The only covered region is x ∈ [−25, 25], y ≥ −25 (the fill cap, Ø55 at (0, 45),
  and the clip plate) — i.e. roughly **two thirds of the Ø140 hopper mouth is open**.

Granule-path consequences, in my lane: the 422-pellet column is not contained
(pellets leave in flight/handling), there is no overfill datum above the bed, the
fill cap has nothing to seal against (B12 fill route is unverifiable), and the whole
dust/water exclusion story for the bed is void. Everything B5/B6/B12 hang on this
part too. **Must be re-built and re-exported before any other granule-path number in
this round can be trusted as final.**

### BLOCKER 2 — B7 not closed: release still happens while the disc is moving (measured on the exports)

Exit port re-cut Ø18.00 → **Ø16.000** (measured r = 7.998–8.000 through the 4.00 mm
plate, 0.75 × 45° top chamfer, **first material at the plate top r = 8.747**).
Release sweep on `retaining_plate_chute_r7.stl` at 0.25° steps, pocket approaching
θ = 0 from the 22.5° park:

| pellet | lateral seat offset | support lost at | centre–port separation |
|---|---|---|---|
| Ø13 | 0.00 | **7.00°** into the 22.5° index | 8.630 mm |
| Ø13 | +1.00 | **8.75°** (38.9 % of the move) | 8.655 mm |
| Ø13 | −1.00 | **5.25°** (23.3 % of the move) | 8.610 mm |
| Ø11 | 0.00 / ±1.00 | 7.00 / 8.75 / 5.25° | 8.630 / 8.655 / 8.610 mm |

Release-angle spread **3.50°** of disc rotation (r6: 3.62°). Punch-list B7.1 asks for
support retained until |separation| ≤ 1.0 mm; measured **8.61–8.66 mm**. Lateral
velocity at release is still ω·32 mm — on the r6 profile assumptions (carried, not
re-derived here) **0.126 m/s at 225 °/s mean, 0.25 m/s at a 450 °/s peak**. The
smaller port *did* buy park retention: worst-placed Ø13 contact at 12.486 − 1.000 =
**11.486 mm vs rim 8.747 → +2.739 mm** (r6: +1.735). But note release now occurs
*later* in the index (23–39 % vs r6's 14–30 %), i.e. deeper into the accelerating
part of the move, so the lateral-velocity number does not improve. B7 may close as a
documented plateau **only** if these measured numbers and the corrected README/DESIGN
text ship in the same round; there is no build note yet to check.

### MAJOR — export integrity regressed onto the plate (B10)

- `meter_housing_r7.stl`: **watertight True, 0 non-manifold edges** — the r6
  4-face edge at θ = 310° is gone. ✔
- `retaining_plate_chute_r7.stl`: **watertight False** — edge-multiplicity histogram
  `{2: 33312, 4: 3}`, i.e. **3 non-manifold (4-face) edges** at
  **r = 45.668–45.700, θ = 270.00°, z = −345.250** (plate bottom, outer rim). Same
  failure mode as r6, moved to the part that carries the exit port, the chute and the
  count apertures. Containment/volume queries on this part are unreliable until fixed.
- `dispenser_r7_assembly.stl`: 4 bodies with **negative volume (−15.9 mm³ each)**
  (inverted normals) at (±16.95…±19.05, −68.50…−63.90, z −342.15…−340.05 and
  −314.15…−312.05).

### What is genuinely closed (with the numbers)

**B1 — roof through-slot fixed.** Roof thickness probed on `meter_housing_r7.stl`
(z from the roof top −316.25 down) at r = 20.5/24.5/30/32/36/39.5/44/46.5:
**9.00 mm at every probe at θ = 300, 305, 308, 309, 310, 310.5, 311, 313, 316, 320,
330, 350, 0, 20, 45, 90°** (r6: 0.000 mm at θ = 310.0). The 25° undercut is now
confined to the sector that needs it; open roof arc at r = 32 measured **θ = 130.25…
249.75 (119.5°)**, which is the sump window, plus the ramp band 96…130.25.
Face-normal audit over the pellet band (z −326.75…−316.25, r 18…47.5), faces opposing
disc travel (disc runs −θ): **largest vertical face 13.23 mm² at r = 47.00,
θ = 130.93, n_z = 0.000** — under the 20 mm² limit (r6: a 238 mm² face at θ = 310°).
Housing upstream-facing entry faces total **641.2 mm², area-weighted n_z = −0.849**
(a genuine downward-crushing 25° ramp), only **40.7 mm² (6.3 %) vertical**, largest
single vertical 1.82 mm².

**Overfill relief before the housing arc — verified, true underside ramp at every
radius.** Ceiling height above the disc top (r = 20.5 / 24.5 / 32 / 39.5 / 45.5 /
46.5): 10.50 @130° (r = 32), 10.24–10.30 @129°, 9.98–10.03 @128°, 9.17–9.25 @125°,
7.86–7.94 @120°, 6.57–6.63 @115°, 5.27–5.32 @110°, 3.97–4.01 @105°, 2.68–2.70 @100°,
2.16–2.18 @98°, 1.64–1.65 @96°, **1.500 @ ≤95° and at every θ in 250…95 (transfer
arc)**. Slope 8.60 mm over 33° of arc at PCD 32 = 18.43 mm run → **25.0°**, matched at
all six radii (spread ≤ 0.08 mm). The ramp cuts the full 9.00 mm roof section at its
entrance (ceiling starts at the roof top), so there is **no step at the ramp mouth**.
Ordering is right: last fill opportunity is the window edge at θ = 130.25, the ramp
runs 130.25 → 96, nothing enters the covered arc unrampled.

**B8 — nose gap closed to 1.500 mm.** `brush_holder_r7.stl` underside above the disc
top: **1.500 mm at r = 22, 26, 30, 34, 38, 42, 46.5** (r6: 3.00 constant). Nose flat
angular extent (0.1° sweep): r 22 → θ 131.4…158.4, r 32 → **136.7…155.1**,
r 46.5 → 140.3…152.9. Cross-section on the holder axis: flat underside at h = 1.50
from c = −4.0 to +6.3, **0.6 mm blunt tip (h 1.50 → 2.10)**, then the lifting ramp.
Ramp angle measured from the face normal **n_z = +0.887 → 27.5° from horizontal**
(source says `NOSE_ANG = 30.0`; the export is shallower, i.e. better):
**lift/push = cot 27.5° = 1.92 vs the 1.44 requirement** (µ/sin 16.1° at the worst
self-locked sliver) → PASS. Holder upstream-facing faces in the pellet band
**516.8 mm², area-weighted n_z = +0.699 (lifting), 84.7 mm² (16.4 %) vertical**; by
height band: 0–1.5 mm **nothing**, 1.5–3.0 mm **16.0 mm² all vertical (the blunt
tip)**, 3.0–6.0 mm 309.6 mm² at n_z = +0.887, 6.0–9.0 mm 107.5 mm² at +0.403.

Contact order measured at r = 32 (scan from θ = 249.5 downward, exports only):

| object proud | first → second → third |
|---|---|---|
| 1.20 mm | **no contact — passes** |
| 1.30 / 1.50 mm | bristles @159.00° |
| 1.60 / 2.00 / 2.10 mm | bristles @159.00° → holder @155.00° → housing ramp @95.75–97.50° |
| 3.00 / 5.00 / 7.00 mm | bristles @159.00° → holder @155.00° → housing @101.00 / 108.75 / 116.50° |
| 9.00 / 11.50 mm | holder overhang @164.25° → bristles @159.00° → housing @124.00 / 130.00° |

Compliant element leads for everything below 9 mm proud (B8.1 asks the rigid element
not to lead below 5 mm) ✔. Bristle tip measured **1.200 mm** above the disc top
(assembly body, vol 312.2 mm³, z −325.55…−318.16) — below the 1.500 nose, so the
compliant element still leads ✔.

**Worst-case seated pellet is untouched.** Ø13 seated pellet centre −334.750
(crown 1.500 below the disc top), swept at 0.5° through all 720 stations: minimum
surface distance from the pellet centre to `meter_housing` **9.500 mm (clearance
3.000)**, to `brush_holder` **9.500 (3.000)**, to bristles **9.200 (2.700)**, resting
on the plate (0.000 by construction). **0.000 mm³ interference over the full
revolution.**

**Chute is clear with the new count hardware.** `retaining_plate_chute_r7`: bore
**r = 10.997–11.000 (Ø22.000) continuous from z = −345.25 to −395.25**, including at
the sensor plane z = −385.25; merging `count_windows_r7.stl` (4 bodies, 0.104 cm³)
leaves **rmin = 10.997** at z = −382…−388, i.e. **no window or aperture protrudes into
the bore** (B4.8 ✔).

**N6 closed.** Disc lightening voids measured at **r 10.50…15.50** (8 groups, ±11°
about each pocket angle); sump window inner edge r = 20.00 → **radial land 4.50 mm**
(punch list asked ≥ 2.0; r6 broke through by a 2.0 mm crescent).

### Adversarial fragment construction, on the measured geometry

Measured pocket: bore **Ø15.000 (r 7.498–7.500) through the full 14.00 mm**, chamfer
**45° from r 7.500 at 2.00 below the disc top flaring to r 9.500 at the top**
(probe: r 9.497@0.00, 9.297@0.20, 8.992@0.50, 8.489@1.00, 7.992@1.50, 7.498@≥2.00).
Seated Ø13 pellet: centre 8.000 below the disc top, crown **1.500 below** it.

**(a) Chamfer-nested fragment against a seated pellet** (my reconstruction reproduces
the r6 critic's numbers exactly: Ø5.0 → +1.80, Ø6.0 → +2.95, Ø7.0 → +4.08 for a
centred Ø13):

| fragment | D13 centred | D13 at max ±1.00 seat offset | D12 centred | D12 offset |
|---|---|---|---|---|
| Ø4.0 | +0.64 | +0.17 | — | — |
| Ø5.0 | **+1.80** | +1.36 | +1.14 | +0.73 |
| Ø6.0 | +2.95 | +2.53 | +2.28 | +1.89 |
| Ø7.0 | +4.08 | +3.69 | +3.40 | +3.03 |

With the nose at 1.500 the **largest fragment that escapes rejection entirely** is
**Ø4.74 (D13 centred), Ø5.11 (D13 offset), Ø5.31 (D12 centred), Ø5.66 (D12 offset)** —
against **Ø6.0+ in r6**, so the blind band shrank as intended. Ø5.0 (+1.80) now lands
on the **0.6 mm blunt tip**, Ø6.0 (+2.95) on the **27.5° lifting ramp**. Escaping
fragments still leave with the pellet: outer reach from the pocket axis
**7.65 / 7.38 / 7.24 / 6.99 mm vs the Ø16 port radius 8.000** → min margin
**0.35 mm** (it was 1.35 mm on the r6 Ø18 port — worth watching, it is now the
tightest clearance on the exit).

**(b) The wedged sliver that must be sheared** — sliver of radial width w trapped in
the crescent between a seated Ø13 pellet and the bore, shear plane at the measured
nose/roof underside 1.500 above the disc top; σ = 0.36 MPa and µ = 0.4 are carried
**ASSUMPTIONS** (US4172714-derived, closed by IFDC S-115); drive force from
`DRIVE_T_MAX = 0.14 × 5.18 × η = 0.65 N·m` at PCD 32 = **20.3 N recovery /
12.2 N normal** (BOM r7 still carries the 14HS13-0804S-PG5, verified):

| w (mm) | seats y above pellet centre | seat depth below disc top | sliver height needed to reach the shear line | wedge half-angle | self-locking (< 21.8°) | shear area, 90° conforming shard | F_shear | margin vs 20.3 N |
|---|---|---|---|---|---|---|---|---|
| 1.000 | 0.000 | 8.000 | 9.500 | 0.00° | yes (parallel slot) | 11.00 mm² | 3.96 N | 5.13× |
| 1.500 | 2.500 | 5.500 | 7.000 | 11.31° | yes | 15.90 mm² | 5.73 N | 3.55× |
| 2.000 | 3.464 | 4.536 | 6.036 | 16.10° | yes | 20.42 mm² | 7.35 N | 2.76× |
| 2.500 | 4.153 | 3.847 | 5.347 | 19.86° | yes | 24.54 mm² | 8.84 N | 2.30× |
| **2.793 (widest self-locking)** | 4.483 | 3.517 | **5.017** | 21.80° | limit | **26.79 mm²** | **9.65 N** | **2.11×** |
| 3.000 | 4.690 | 3.310 | 4.810 | 23.09° | no (squeezes down) | 28.27 mm² | 10.18 N | 2.00× |
| 5.000 | 6.000 | 2.000 | 3.500 | 33.69° | no | 39.27 mm² | 14.14 N | 1.44× |

**Shear-margin headline: the worst self-locked sliver the pocket can hold (w = 2.793,
≥ 5.02 mm tall) needs 9.65 N; the drive delivers 20.3 N in recovery and 12.2 N
normal → 2.11× / 1.26×.** Capability bound: **20.3 N / 0.36 MPa = 56.4 mm²** of
shearable section (normal 33.9 mm²). Where it stops passing: a **180°** conforming
shard at the same width is 53.6 mm² → 19.3 N → **1.05×** (i.e. it only just shears,
and **fails at normal current**), and a full-ring 2.793 mm crescent (107.2 mm²,
38.6 N) is **0.53× — would stall**. I do not think a 180°/360° conforming crescent
shard is credible from a crumbled 12 mm pellet, but that is where the margin runs out
and it should be written down as the bound, not left implicit.

Lowering the nose to 1.500 raised the height a sliver must have before anything
engages it (5.02 mm at w = 2.79, was 3.52 mm with the 3.00 nose). Net effect is still
favourable — the escaping *nested-fragment* size dropped from Ø6.0+ to Ø4.74–5.66 —
but note the trade explicitly: the rejection band is wider, the shear band is
narrower.

### MODERATE 1 — the whole rejection train is one-directional; **the stall-recovery stroke drives fragments into square walls**

The reverse (recovery) direction has no lead-in anywhere. Downstream-facing faces in
the pellet band (r 18…46.5, z −326.75…−316.25), i.e. the faces a reverse-oscillate
pushes material into:

| part | area opposing REVERSE travel | area-weighted n_z | vertical (|n_z| < 0.05) | largest single face |
|---|---|---|---|---|
| `meter_housing` | 292.9 mm² | **+0.000** | **292.9 mm² (100 %)** | **121.50 mm² at θ = 250.00°, h 1.50–10.50** |
| `brush_holder` | 310.2 mm² | **+0.000** | **310.2 mm² (100 %)** | **79.43 mm² at θ ≈ 136.7° (PCD), h 1.50–7.45** |

(For comparison the forward direction is 641.2 mm² at n_z = −0.849 and 516.8 mm² at
n_z = +0.699.) Concretely: a pocket sits at θ = 135° at park — **inside the 6.4° band
(130.25…136.7 at PCD) between the ramp mouth and the nose's trailing wall**. Anything
proud > 1.50 mm in that freshly-loaded pocket (a stacked second pellet is 11.5 mm
proud) has **≤ 6.4° of reverse free travel before it hits a 5.95 mm tall square wall**;
elsewhere in the window it has up to 113° before the 9.00 mm roof edge at θ = 250.00.
The recovery motion is exactly the motion that runs after a fragment stall, so the
recovery stroke can create the second jam. Fix is cheap and symmetric: chamfer/ramp
the nose trailing face and the roof edge at θ = 250 the same way the leading edges
already are, or bound the reverse stroke to < 6° in firmware and say so.

### MODERATE 2 — rotational free travel is fine; the axial films are thin (numbers for the record)

Full-revolution clash check of the rotating group (`pocket_disc_r7` + `agitator_r7`)
against the swept-solid profile of `meter_housing`, `hopper`, `brush_holder`,
`retaining_plate_chute` and the bristles (0.2 mm (r, z) occupancy grid, 800 k surface
samples): **no contact at any angle**, so reverse-oscillate has unlimited rotational
free travel. Minimum clearances (exact probes, not grid): agitator lowest point
**z = −315.900 vs roof top −316.250 → 0.350 mm film** (r4's blocker was 0.50 mm),
agitator tip **r = 46.743 vs chamber wall r = 47.000 → 0.257 mm**, disc bottom to
plate top **0.500 mm**, roof underside to disc top **1.500 mm**, bristle tip
**1.200 mm**, disc rim (r 46.000) to chamber wall (r 47.000) **1.000 mm**. Nothing
here blocks recovery; the 0.257/0.350 mm agitator films are below any sensible
printed-part tolerance and should be stated as a fit note, not left as a number that
only exists in nominal CAD.

### MODERATE 3 — N10 unchanged, still the governing arching risk

Sump outlet measured on `meter_housing_r7`: annular window **r 20.00 → 47.00 at the
disc plane (27.00 mm), r 20.00 → 48.14 at the roof top (chamfered lead-in), arc
θ 130.25…249.75 = 119.5°**. **Minimum outlet dimension / worst-case pellet =
27.00 / 13.0 = 2.08** (r6: 2.04) — still below every no-arch criterion (≥ 3× for a
slot). Funnel measured 68.0° from horizontal (r 66.15 @ z −270 → r 48.00 @ z −315 =
atan(45/18.15) = **68.03°**), landing on a **0° flat shelf** (housing roof top,
solid r 15.20…20.00 inboard). Agitation duty unchanged: **3 fingers at 0/120/240°**
(5–7° wide at r = 30–40, reaching r 46.743), exactly **one finger in the 119.5°
window at a time**, each 22.5° index sweeps **18.8 %** of the window, so a given
angular location is agitated **once per 5.33 indexes ≈ once per 2.67 pellets**, and
only when a dispense is commanded. Carry as the recorded plateau-with-complaint with
these numbers, per punch-list N10.

### MINOR — probe artefact worth knowing about

Radial rays cast at exactly θ = 0.000° miss `hopper_r7.stl` (STL seam); θ = 1° and
θ = 359° both report the wall at r = 49.99/52.32 etc. Not a hole — but any checker
that probes on the axes will report a phantom opening.

### What I would require to pass this round on the granule path

1. Re-build and re-export `top_plate` (lid + neck). Re-run: mouth-coverage probe
   → 0 open cells over r ≤ 67; fill-port bore ≥ Ø46 with the Ø13 path to the bed
   0.000 mm³ obstructed; hopper containment.
2. `retaining_plate_chute` watertight, 0 non-manifold edges; assembly with no
   negative-volume bodies.
3. B7: either geometry that releases inside the dwell, or the plateau written with
   **5.25–8.75° into the index / 8.61–8.66 mm separation / 3.50° spread** and every
   "stationary release / zero lateral velocity" sentence corrected in the same round.
4. Ramp/chamfer the two reverse-direction square walls (121.50 mm² at θ = 250.00,
   79.43 mm² at θ ≈ 136.7) **or** publish the bounded reverse stroke (< 6°).
5. Keep and publish the shear table above with its explicit bound (2.11× at the worst
   self-locking sliver; 1.05× at a 180° shard; assumptions σ = 0.36 MPa, µ = 0.4).

## assembly

**Verdict: FAIL — 4 blocking findings.** The exported r7 geometry cannot be built:
the chassis adapter / stand-off neck is missing from the export, the retaining
plate (which carries the motor, the disc thrust face, the chute and the count
sensor) hard-interferes with the meter housing in *every* rotational and axial
position, and the electronics bay and its lid cannot be seated. The **torque
path itself is sound** — motor → gearbox → Ø6 D-shaft → disc D-bore → disc →
Ø15 hex → agitator is present and dimensionally consistent, and the grub-screw
corridor closes B2.1/B2.2/B2.3. It just has nothing to mount to.

### Provenance and caveats

- Measured on `cad/exports/*_r7.*`, mtime **2026-08-07 10:04:37**.
  `md5(retaining_plate_chute_r7.stl) = 5cd5b0c82ff4e760ce353f8416ac2ca1`,
  `md5(meter_housing_r7.stl) = 98f0f3038a670f04304d1db63f60505a`,
  `md5(top_plate_r7.stl) = 3e85b203279a9327fc62add8d16e942f` (unchanged over the
  whole measurement run).
- `cad/dispenser.py` mtime **10:16:37** — 12 min *after* the exports. If the
  source has moved on, these numbers describe the exports, which is what the
  tasking asks for.
- `_run/rev1/BUILD-NOTES-r1.md` **does not exist** at the time of writing (only
  the rev-0 `_run/BUILD-NOTES-r1..r6.md`), so no builder claim could be
  cross-checked. `_run/rev1/CONTEXT.md` and `_run/rev1/PUNCHLIST.md` were read.
- All obstruction volumes are **exact OCC booleans** on the STEP bodies
  (`build123d.import_step` + `Shape.intersect`), not voxel estimates — the venv
  has no `manifold3d`/blender backend for trimesh booleans. Ray/section probes
  are trimesh 5.0.0 on the STLs. venv:
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`.
- COTS bodies (motor+gearbox+shaft, igus bearing, thrust washer, clip plate,
  blind-mate PCB, brush strip) were lifted from `dispenser_r7_assembly.step` by
  volume rank; that identification is an **ASSUMPTION** from size/position.

### 0. Part inventory (exact STEP volumes)

```
hopper                   nsol= 1 V=  114.153cm3 bb=[  -78.00, -112.50, -324.250]->[   78.00,   78.00, -228.550]
meter_housing            nsol= 1 V=  104.807cm3 bb=[  -60.50,  -58.00, -348.250]->[   58.00,   58.00, -316.250]
pocket_disc              nsol= 1 V=   72.728cm3 bb=[  -46.00,  -46.00, -340.750]->[   46.00,   46.00, -310.250]
retaining_plate_chute    nsol= 1 V=   45.833cm3 bb=[  -55.30,  -52.00, -395.250]->[   52.00,   52.00, -341.250]
electronics_bay          nsol= 1 V=   18.748cm3 bb=[  -30.00,  -90.00, -353.100]->[   30.00,  -48.96, -301.100]
fill_cap                 nsol= 1 V=   11.132cm3 bb=[  -27.50,   17.50, -230.000]->[   27.50,   72.50, -221.045]
bay_lid                  nsol= 1 V=    7.610cm3 bb=[  -29.00,  -92.00, -352.100]->[   29.00,  -88.60, -302.100]
agitator                 nsol= 1 V=    4.291cm3 bb=[  -25.08,  -41.44, -315.900]->[   46.70,   41.44, -308.350]
brush_holder             nsol= 1 V=    3.431cm3 bb=[  -51.84,    1.11, -330.550]->[   -9.22,   35.51, -316.250]
top_plate                nsol= 1 V=    0.808cm3 bb=[   -4.50,  -87.00, -238.550]->[    4.50,  -78.00, -214.550]   <-- see A-1
count_windows            nsol= 4 V=    0.104cm3 bb=[   26.05,  -11.97, -391.200]->[   37.95,   11.97, -379.300]
chute_plug               nsol= 1 V=    6.097cm3 bb=[   18.00,  -14.00, -409.250]->[   46.00,   14.00, -385.250]
service_stand            nsol= 1 V=   88.855cm3 bb=[  -90.00,  -90.00, -401.250]->[   90.00,   90.00, -348.250]
motor_gearbox_shaft      nsol= 1 V=   69.936cm3 bb=[  -18.00,  -18.00, -408.450]->[   18.00,   18.00, -327.250]
clip_plate_COTS          nsol= 1 V=   11.523cm3 bb=[  -25.00,  -25.00, -181.550]->[   25.00,   25.00, -171.050]
blindmate_pcb            nsol= 1 V=    1.174cm3 bb=[   -8.00,  -12.00, -188.150]->[    8.00,   12.00, -181.550]
bearing_JFM2023          nsol= 1 V=    1.495cm3 bb=[  -15.00,  -15.00, -324.950]->[   15.00,   15.00, -315.950]
thrust_washer            nsol= 1 V=    0.317cm3 bb=[  -19.00,  -19.00, -342.200]->[   19.00,   19.00, -340.800]
brush_strip              nsol= 1 V=    0.312cm3 bb=[  -42.89,    5.50, -325.550]->[  -19.65,   20.85, -318.160]
```

Static interference matrix (exact boolean; every pair not listed is 0.0000 mm³):

```
   hopper                ^ electronics_bay       =       6.3017 mm^3
   hopper                ^ bay_lid               =       6.0000 mm^3
   meter_housing         ^ retaining_plate_chute =     186.4134 mm^3
   meter_housing         ^ brush_holder          =       3.3540 mm^3
   (chute_plug ^ retaining_plate_chute           =      98.3738 mm^3  <- intended press fit)
```

---

### BLOCKING A-1 — the chassis adapter / stand-off neck is not in the export; the payload is not attached to anything

`top_plate_r7.step/.stl` is **0.808 cm³**, bb `[-4.50, -87.00, -238.550] → [+4.50, -78.00, -214.550]` —
a Ø9 × 24 mm vertical conduit spigot and nothing else. The model's own ledger
string for that part reads *"integral 42 mm stand-off NECK (B6) carrying the M2
inserts at the MAPPED clip pattern, the blind-mate PCB well and the covered
harness conduit to the -Y rim"*; the Ø150 plate, the 48 × 48 × 52 neck, the
6.5 mm cap, the four M2 insert bores and the elbow are all absent from the
exported solid (the source comment at that point in `dispenser.py` warns that a
tangent union there *"silently ate the whole part on the first attempt"* — it ate
it again, and nothing caught it).

Measured consequences, on the assembly export:

| quantity | measured |
|---|---|
| highest payload material anywhere | **Z = −214.550** (the conduit spigot) |
| clip-plate underside | Z = −181.550 |
| vertical void between them | **33.000 mm** |
| min 3-D distance `clip_plate_COTS` ↔ nearest payload solid | **58.8325 mm** |
| min 3-D distance `blindmate_pcb` ↔ `top_plate` | **72.9449 mm** |
| solids in `dispenser_r7_assembly.step` | 16, **none** in the band Z −214.55 … −188.15 |
| `fill_cap` ↔ nearest payload solid (`hopper`) | **1.8000 mm** (bayonet counterpart absent) |

Orphaned fasteners this creates:

- **6 × M3 hopper-flange screws.** The hopper side is fine and measures well:
  vertical probe at r = 74.0, θ = 15/75/135/195/255/315° gives material only
  from **Z −234.545 to −235.550**, i.e. a **5.995 mm** deep insert bore under a
  **1.005 mm** floor in a **7.000 mm** flange (θ = 45° control probe: solid
  −228.550 → −235.550). Tool corridor Ø6 × 25 above each bore = **0.0000 mm³**.
  There is simply no mating part to screw to.
- **4 × M2 mount screws** at the mapped clip pattern (±19, ±19): **no payload-side
  threaded feature within 58.83 mm** of the clip plate. Driver column Ø5 × 30
  downward from Z = −171.05 meets only the vendor clip plate (64.2094 mm³ — its
  own hole is smaller than the probe).
- The **harness route** loses its first covered leg (the neck) and the
  interface-PCB well.

Nothing in the shipped assembly transmits the 1.39–1.59 kg payload load to the
aircraft. This is the single largest defect in the round.

### BLOCKING A-2 — the retaining plate hard-interferes with the meter housing in every pose; the whole drive cannot be mounted

As-exported (seated) pose: **186.4134 mm³** in one lump, θ = **298.86°**,
r **52.30 … 58.00**, z **−348.250 … −344.500**.

Full 360° rotation scan (10° steps, exact boolean, plate about Z vs housing):

```
   0:186.4134   10:150.1185   20:124.6997   30:321.5484   40:545.4243   50:573.2653
  60:573.3643   70:573.8984   80:573.8981   90:573.9006  100:573.8993  110:515.6929
 120:186.4134  130:150.1185  140:124.6997  150:321.5484  160:545.4243  170:573.2655
 180:573.9006  190:573.8993  200:573.9012  210:573.9006  220:573.9006  230:515.6923
 240:186.4134  250:150.1185  260:124.6997  270:321.5484  280:545.4243  290:573.2655
 300:573.9006  310:573.8993  320:573.9012  330:573.9006  340:573.9006  350:515.6923
   MINIMUM over 360 deg = 124.6997 mm^3 at 20/140/260 deg   (needs 0.0000 somewhere)
```

Axial approach of the plate+motor+washer sub-assembly, travelling +Z into the
housing (disc, brush holder and bearing already fitted):

```
   t_to_go      meter_housing   pocket_disc  brush_holder  brush_strip  bearing
     40.00           0.0000        0.0000        0.0000       0.0000     0.0000
      6.00          92.3933        0.0000        0.0000       0.0000     0.0000
      4.00         258.7014        0.0000        0.0000       0.0000     0.0000
      2.00         276.2538        0.0000        0.0000       0.0000     0.0000
      0.00         186.4134        0.0000        0.0000       0.0000     0.0000
```

Bayonet anatomy (material-presence bands at fixed radius, 0.5° steps):

```
 z=-343.25  housing @r=54.0 : 0.0-54.0, 90.5-173.5, 210.0-293.5, 330.5-359.5   (3 slots ~36.5 deg)
 z=-343.25  plate   @r=54.0 : 55.0-65.0, 175.0-185.0, 295.0-305.0              (3 lugs 10 deg)
 z=-343.25  housing @r=56.5 : 0.0-359.5  (solid ring, no relief anywhere)
 z=-346.50  plate   @r=56.5 : 294.5-298.5, 306.5-308.5   <- plate boss inside the ring
 z=-346.50  plate outer loop reaches r=60.602 at theta=301.9 and r=59.679 at 306.5
```

Two independent defects here:

1. The exported pose is the **unlocked/insert** orientation (all three lugs sit
   inside the housing slots). Rotating them under the ring — which is what a
   quarter-turn latch has to do — drives the interference to **573.9 mm³**
   (unlocked-pose lumps at −40°: 327.5189 mm³ @ θ 259.5 z −348.25…−341.25, plus
   123.1911 mm³ each @ θ 20 and 140, r 52.30…55.53, z −345.25…−341.25). There is
   **no locked position**: the housing bore above the lug band is r = 52.29 and
   the lugs are r = 55.526, so there is no shelf to slide under.
2. A plate boss at θ ≈ 295–309°, reaching **r = 60.602** at z = −346.5, passes
   straight through the housing skirt (solid at r = 56.5 over the full 360°).
   That is the residual 124.70–186.41 mm³ that survives *every* rotation.

Because this plate carries the gearbox, the disc thrust face, the drop chute and
the count-sensor boss, A-2 makes the entire drive unassemblable.

### BLOCKING A-3 — the electronics bay and its lid cannot be seated

Straight-line insertion sweeps (exact boolean, 20 stations):

```
 electronics_bay, travel +Y (inboard) 40 mm:
   t_to_go 24 -> hopper 1.5000 ; 22..2 -> hopper 6.0000 (constant) ; 0 -> hopper 6.3017
 electronics_bay, travel -Y (outboard): max 3656.0355 (housing) - wrong sense, blocked
 electronics_bay, travel -Z 60 mm:      max 1611.0334 (hopper) at t=45 - blocked
 bay_lid, travel +Y 30 mm:
   t_to_go 21 -> hopper 4.5000 ; 19.5..0 -> hopper 6.0000 (constant)
```

The obstruction is **constant along the whole approach and non-zero at the seat**,
so no straight-line insertion clears it: 6.3017 mm³ at
(±2.398, −90.00…−88.00, −303.100…−302.100) for the bay and 6.0000 mm³ at
(±1.500, −92.00…−90.00, −303.100…−302.100) for the lid — both at θ = 270°, on the
hopper's −Y arm. Two rigid CF-PETG parts share that volume.

### BLOCKING A-4 — the four count-sensor windows have no clear path into their seats

`count_windows_r7` = 4 × Ø5.90 × 1.00 discs at (x 29/35, y ±11.5, z −382.25 /
−388.25). Seated clearance is fine (min distance to plate **0.0250 mm**), but:

```
 from the component-cavity side (travel inboard, 15 mm):  MAX 18.3324 mm^3
     (t=5..1 constant 18.3324) - a Dia5.90 window cannot pass the Dia3.20 aperture
 from inside the Dia22 chute bore (travel outboard, 20 mm): MAX 5.2219 mm^3
     (t=2 -> 1.2493 ; t=1 -> 5.2219 ; t=0 -> 0.0000)
 Dia18 x 13.0 mm rod up the chute to z=-382.25 : 0.0000 mm^3
 Dia18 x  7.0 mm rod up the chute to z=-388.25 : 0.0000 mm^3
```

So the bore route physically exists (0.0000 mm³ of rod obstruction), but a
straight push still gouges **5.2219 mm³** — that is the **0.404 mm** sagitta of a
flat-bottomed Ø6.0 seat mouth cut into the Ø22 curved bore wall
(11 − √(11² − 2.95²) = 0.404). Either relieve the seat mouth to the full bore
chord, or prove the tilt-in (a Ø5.90 disc in a Ø6.00 pocket has ≈4° of tilt,
which is marginal against the required 3.9°). B4.4's "floor flush with the bore
wall" and a flat pocket are geometrically in tension; that has to be resolved.

---

### 1. Derived assembly order, with the swept-volume numbers that prove it

Directions are the direction the part **travels** while being installed.
"0.0000" means the exact boolean against every already-installed solid is zero at
all 21 stations of a 40–60 mm approach.

| # | Operation | Direction | Obstruction along the path | Verdict |
|---|---|---|---|---|
| 1 | `meter_housing` in fixture | — | — | — |
| 2 | igus JFM-2023-07 sleeve bearing into the roof bore | **−Z, from above** | **0.0000 mm³** over 40 mm | OK |
| 2′ | (same, from below) | +Z | 377.3876 / 580.5963 / 580.5963 / 533.7285 at t = 8/6/4/2 | **not possible** — bearing must go in from above |
| 3 | `brush_holder` (+`brush_strip`) into the metering chamber | **−Z, from above** | 0.0000 over 40 mm, **3.3540 mm³ residual at the seat** | seats only with an interference (see NB-1) |
| 3′ | (same, from below) | +Z | max **1002.4383 mm³** at t = 18 | not possible |
| 4 | `pocket_disc` into the chamber, hub up through the bearing | **+Z, from below** | **0.0000 mm³** vs housing / bearing / brush_holder / brush_strip over 40 mm | OK |
| 4′ | (same, from above) | −Z | max **27555.6197** vs housing, **1037.6697** vs bearing at t = 12 | not possible — the Ø92 disc cannot pass the Ø23.02 roof bore |
| 5 | `thrust_washer` into the plate seat; motor+gearbox onto the plate underside | +Z | **0.0000 mm³** over 40 mm | OK |
| 5b | 4 × M3 gearbox screws driven +Z through the plate | +Z | max clear driver **Ø8.0 mm** (Ø10.0 first touches the washer, 2.1304 mm³) | OK **at sub-assembly only** |
| 6 | plate + motor + washer up into the housing | +Z | **92.3933 / 258.7014 / 276.2538 / 186.4134 mm³** at t = 6/4/2/0 | **BLOCKED (A-2)** |
| 7 | M3 grub screw, radial θ = 202.5°, z = −331.250 | radial in | Ø1.9 × 50 key column = **0.0000 mm³** against all 18 solids | OK |
| 8 | `agitator` onto the Ø15 hex | −Z | **0.0000 mm³** over 40 mm | OK |
| 9 | `hopper` onto the housing | −Z | **0.0000 mm³** vs housing / agitator / disc / brush_holder over 60 mm | OK |
| 10 | `top_plate` (chassis adapter + neck) | −Z | **part not present in the export** | **BLOCKED (A-1)** |
| 11 | `fill_cap` bayonet | −Z + rotate | 0.0000 vs hopper and the conduit; but the mating flange/notches live on the missing top plate | **BLOCKED (A-1)** |
| 12 | `electronics_bay` | +Y | constant **6.0000 mm³**, 6.3017 at seat | **BLOCKED (A-3)** |
| 13 | `bay_lid` | +Y | constant **6.0000 mm³** | **BLOCKED (A-3)** |
| 14 | 4 × `count_windows` | ±Y | 18.3324 (cavity side) / 5.2219 (bore side) | **BLOCKED (A-4)** |
| 15 | `chute_plug` | +Z from below | rises to **98.3738 mm³** at the seat | OK — that is the *designed* interference (≈0.28 mm diametral over the Ø22.0 × 10 mm engagement); N7 asked for 0.2–0.4 mm |

`service_stand` contacts the retaining plate (min distance **0.0000 mm**) and
clears the motor can by **28.0000 mm**, so the B12.1 "load path not through the
gearbox flange" condition is satisfied by the stand as drawn.

### 2. Torque path — motor → gearbox → shaft → metering disc: **EXISTS and closes**

Measured chain, every number from the exports:

```
 gearbox body            R=18.000  z -374.450 .. -345.250
 output flange face      plane n=(0,0,1) at z=-345.250, area 816.81 mm^2
 output pilot boss       R= 8.000  z -345.250 .. -343.250   (Dia16.00, ASSUMPTION in the model)
 output shaft            R= 3.000  z -343.250 .. -327.250   (16.000 mm exposed)
 shaft D-flat            plane n=(-0.924,-0.383,0) = theta 202.5 deg, at r=2.500,
                         z -339.250 .. -327.250  =  12.000 mm  (vendor D-cut 12 mm)

 plate pilot bore        R= 8.100  (Dia16.20 on a Dia16.00 boss = 0.100 mm/side)
 plate motor holes       4 x R=1.700 at (+/-13.000, 0) and (0, +/-13.000), through
                         z -345.250 .. -341.250, with Dia5.700 counterbores from the top
 web hole-edge -> pilot-edge = 11.300 - 8.100 = 3.200 mm   (B3.2 wanted >= 1.95)

 disc bore               r = 3.049 .. 3.050 round; FLAT at r = 2.550 over
                         theta 181.0 .. 224.0 deg (44 deg), z -339.20 .. -327.30 = 11.90 mm
                         (B2.1 wanted a >=25 deg arc over >= 10.0 mm)
 bore blind top          z = -327.20 ; disc bottom -340.750 -> 13.55 mm of bore,
                         13.50 mm of shaft engaged, shaft top -327.250 (0.05 mm to the blind face)
 flat overlap            11.90 mm ; flat width 2*sqrt(3.0^2-2.5^2) = 3.317 mm
 flat bearing area       39.47 mm^2
 drive torque            0.14 N*m x 5.18 x 0.90 = 0.6527 N*m
 tangential force        261.1 N at r = 2.5 mm  ->  bearing stress 6.61 MPa on CF-PETG

 grub, disc side         clearance R=1.700 (Dia3.400), face area 395.04 mm^2 -> 36.98 mm long,
                         r 9.00 -> 46.00 ; pilot R=1.300 (Dia2.600), area 51.05 -> 6.25 mm,
                         r 2.75 -> 9.00 ; axis theta = 202.5 deg, z = -331.250
 grub, housing port      R=1.800 (Dia3.600), area 56.57 -> 5.00 mm long, r 47.00 -> 52.00,
                         SAME axis and height  (B2.2: continuous void OD -> bore, PASS)
 driver access           Dia1.9 x 50 on the grub axis = 0.0000 mm^3 vs all 18 solids (B2.3 PASS)

 disc -> agitator        hex across-flats 15.000 mm (disc) into 15.400 mm (agitator) = 0.200/side
 bearing seat            Dia23.024 vs igus JFM-2023-07 Dia23.00 (0.012 mm/side);
                         bearing<->housing min distance 0.0150 mm
 disc journal            Dia19.796 in the Dia20 bearing bore -> min distance 0.1000 mm
 disc axial              disc bottom -340.750, washer top -340.800 (0.050),
                         washer -> plate seat floor 0.0550, roof underside -> disc top 1.500
```

Torque is carried motor → planetary gearbox → Ø6 shaft flat (12.000 mm) → disc
D-bore flat (11.90 mm engaged, 39.47 mm², 6.61 MPa) → disc → Ø15 hex → agitator,
with the grub screw taking axial retention against the flat. **B2.1, B2.2, B2.3
all pass on the exports.** The only thing wrong with the drive is that the plate
carrying it cannot be installed (A-2).

### 3. Tool-access corridors — largest clear driver diameter per fastener

Method: a cylinder on the fastener axis, starting at the head-bearing plane and
extending away from the joint, diameter stepped 1.5/2.0/2.5/3.0/3.4/4.0/5.0/6.0/
8.0/10.0/12.0 mm; largest diameter with a **0.0000 mm³** exact boolean against
every other assembly solid is reported.

| ref | fastener | corridor | max clear driver | first blocking size / volume |
|---|---|---|---|---|
| F1 | 4 × M3 gearbox screws, +Z, **in situ** | 25 mm | **0.0 mm** | Ø1.5 → 15.7276 mm³ (housing 12.72 + bearing 3.00) |
| F1b | same four, **plate+motor sub-assembly** | 25 mm | **Ø8.0 mm** | Ø10.0 → 2.1304 mm³ (thrust washer) |
| F2 | M3 grub, key from the disc OD outward | 25 mm | **Ø3.4 mm** | Ø4.0 → 11.9433 mm³ (housing) |
| F2b | M3 grub, hand space outboard of the housing (r = 53 →) | 40 mm | **Ø4.0 mm** | Ø5.0 → 5.1053 mm³ (housing) |
| F3 | M5 detent plunger, outboard of its boss (r = 57.2 →) | 25 mm | **Ø6.0 mm** | Ø8.0 → 104.9543 mm³ (housing) |
| F4 | hopper→housing M3, θ = 30° | 25 mm | **Ø3.4 mm** | Ø4.0 → 0.5231 mm³ (hopper) |
| F4 | hopper→housing M3, θ = 45° | 25 mm | **≥ Ø12.0 mm** | — |
| F4 | hopper→housing M3, θ = 105° | 25 mm | **Ø3.4 mm** | Ø4.0 → 0.5231 mm³ (hopper) |
| F5 | brush-holder screw, θ = 148° | 25 mm | **Ø3.0 mm** | Ø3.4 → 1.0366 mm³ (brush holder) |
| F6 | 2 × bay→housing screws, driver through the lid opening | 40 mm | **Ø2.5 mm** | Ø3.0 → 3.1741 mm³ (housing) |
| F7 | 4 × bay-lid screws, −Y from y = −92 | 25 mm | **≥ Ø12.0 mm** | — (B5.6 passes) |
| F8 | 6 × hopper-flange M3, +Z above the flange | 25 mm | **≥ Ø6.0 mm** | — but **no mating part** (A-1) |
| F9 | 4 × M2 mount screws | 30 mm | n/a | **no payload thread within 58.83 mm** (A-1) |

Readings that matter:

- **F1 in situ = 0.0 mm.** Once the machine is together the gearbox screws are
  buried under the disc, the bearing and the housing roof; a Ø1.5 probe already
  hits 15.7276 mm³. The motor is only fastenable (and only removable) as a
  plate+motor sub-assembly, where the corridor is a healthy **Ø8.0 mm**. That is
  an acceptable *build* route but means no motor swap without a full teardown —
  and today that teardown is impossible in the other direction because of A-2.
- **F6 = Ø2.5 mm over 40 mm.** The two screws holding the electronics bay to the
  housing sit at the bottom of a Ø3.2 × 13.8 mm tube in the bay's inboard wall,
  40 mm from the lid opening. A bare 2.0 mm hex key fits; nothing with a handle
  or a bit-holder does.
- **F4 (θ = 30° and 105°) = Ø3.4 mm**, F5 = **Ø3.0 mm**: bare-key access only.
  θ = 45° is the one screw with real access (≥ Ø12).
- **F3 = Ø6.0 mm** is fine for a hex-socket ball plunger and **not** fine for a
  hex-body M5 plunger needing an 8 mm A/F wrench. State which one is bought.

### 4. Export integrity (feeds B10)

```
 agitator_r7.stl               watertight=True   0 non-manifold edges
 bay_lid_r7.stl                watertight=True   0
 brush_holder_r7.stl           watertight=True   0
 chute_plug_r7.stl             watertight=True   0
 count_windows_r7.stl          watertight=True   0
 electronics_bay_r7.stl        watertight=True   0
 fill_cap_r7.stl               watertight=True   0
 hopper_r7.stl                 watertight=True   0
 meter_housing_r7.stl          watertight=True   0     <- r6's 310 deg defect is gone
 pocket_disc_r7.stl            watertight=True   0
 retaining_plate_chute_r7.stl  watertight=FALSE  3 non-manifold (4-face) edges, Euler -41
 service_stand_r7.stl          watertight=True   0
 top_plate_r7.stl              watertight=True   0
 dispenser_r7_assembly.stl     watertight=FALSE  (4 inverted-normal bodies, V = -0.02 cm^3 each,
                                                  at x = +/-18, y -68.5..-63.9, z -342.15 and -314.15)
```

The three bad edges are all at `(x ≈ 0.000, y = −45.668 / −45.700, z = −345.250)`,
i.e. on the retaining plate's motor-face plane at θ = 270°. **12/13 part STLs
watertight, not 13/13** — B10 is still open, just relocated from the housing to
the plate.

### 5. Non-blocking, measured

- **NB-1 `brush_holder` seats with 3.3540 mm³ of interference** into the housing
  at θ = 152.87°, r ≈ 54.5, z −330.550 … −329.027. Its approach is otherwise
  clean (0.0000 over 40 mm from above). If this is meant as a snap/press land it
  must be stated; as drawn it is an unannotated overlap of two rigid parts.
- **NB-2 count-window seat mouth** — see A-4; the 0.404 mm curved-wall sagitta is
  the whole of the residual 5.2219 mm³.
- **NB-3 motor serviceability** — F1 in situ = 0.0 mm clear (above).
- **NB-4 grub-screw handling.** The screw has to be pushed **36.98 mm** down a
  Ø3.400 channel from the housing port (r 47.00 → 52.00) to reach the Ø2.600
  pilot; the key corridor is clear (0.0000 mm³) but only Ø3.4, and outboard hand
  space is Ø4.0 over 40 mm. A ≥ 60 mm long 1.5 mm hex key is a BOM item, and the
  screw cannot be retrieved if dropped in the chamber. Also: the disc must be
  indexed to θ = 202.5° before the port lines up — that indexing step belongs in
  the assembly procedure.
- **NB-5 `chute_plug`** interference is **98.3738 mm³** ≈ 0.28 mm diametral over
  Ø22.0 × 10 mm — inside N7's 0.2–0.4 mm window. Recorded as a pass.

### 6. What I need to see next round to clear "assembly"

1. `top_plate_r7+` exporting the actual plate + neck (volume in the 90–110 cm³
   class, bb spanning Z −228.55 … −181.55, four M2 insert bores), and an
   assertion in the build that fails the export if any named part's volume drops
   below a floor — this failure mode has now bitten twice in the same file.
2. `retaining_plate_chute ∩ meter_housing = 0.0000 mm³` in the seated pose **and**
   a rotation angle where it is 0.0000 during insertion, i.e. a real slot for the
   θ ≈ 295–309° boss and a real locked shelf for the lugs. Print the 360° scan.
3. `electronics_bay ∩ hopper` and `bay_lid ∩ hopper` = 0.0000 mm³, with the +Y
   approach sweep printed.
4. A window insertion path with 0.0000 mm³ from one named side, printed per
   window.
5. F6 corridor ≥ Ø4.0 mm (or a stated 2.0 mm-key-only procedure), and F1's in-situ
   0.0 mm recorded explicitly as "motor is not field-replaceable".
6. `retaining_plate_chute_r7+.stl` watertight with 0 non-manifold edges.

Nothing above touches the torque path, which is the one part of this round that
measured clean.
