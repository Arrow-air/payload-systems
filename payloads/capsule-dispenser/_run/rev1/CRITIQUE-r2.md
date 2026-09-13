# REV-1 ROUND 2 — CRITIQUES

## count-sensor

**Owner:** count-sensor geometry critic (rev-0 RT-3 / rev-1 punch-list **B4**).
**Verdict: NOT CLOSED — 1 BLOCKING item.** All four of my r1 blockers are closed
by geometry and I can confirm each of them on the exports. What is still missing
is the *volume the specified emitter and receiver parts occupy*: the new ECO-12
retention fixes the sensor board **0.500 mm** off the aperture plane, and neither
the TSAL6200 nor the VBPW34FAS fits in that gap. That is spec'd-but-not-modelled
sensing hardware, which my tasking makes blocking.

**Provenance.** Every number below was measured by me on
`cad/exports/*_r8.step` / `*_r8.stl` with
`~/.openclaw/workspace/venvs/dock-cad-314/bin/python` (build123d 0.11.1 exact OCC
booleans; trimesh 5.0.0 ray casting + `contains` parity for the section scans).
I did not take any number from `BUILD-NOTES-r2.md`; where I quote it, it is to
agree or disagree with it. Export identity confirmed:

```
MD5 (retaining_plate_chute_r8.stl) = a7d64399c6dccabf46306f5ce2224296
MD5 (dispenser_r8_assembly.stl)    = 812d9a0668b7ad0276aee63d14b95733
MD5 (count_windows_r8.stl)         = 43f785bf132e7ac31e1c3b27602f7121
MD5 (sensor_cover_r8.stl)          = 187559e29170a176d5d03932110d0a71
```

The first two match `BUILD-NOTES-r2.md` §0, so the notes and I are looking at the
same geometry. Datum recovered from the exports, not from the source: chute bore
Ø22.000 on the axis **x = 32.000**, `Z_SENSOR` = mid-plane of the two beams =
**−395.250** (r7 was −385.250; the B6 neck moved the whole stack 10 mm down).

---

### PASS — ECO-3 / ECO-9 aperture geometry (re-measured, unchanged from r1)

Tunnel census by ray scan with midpoint parity, plate only:

| beam | side | inner-run centre (x, z) | Ø in x | Ø in z |
|---|---|---|---|---|
| A | +y | **29.0001, −392.2500** | 3.1998 | 3.1994 |
| A | −y | **29.0002, −392.2500** | 3.1996 | 3.1994 |
| B | +y | **35.0001, −398.2500** | 3.1998 | 3.1994 |
| B | −y | **35.0002, −398.2500** | 3.1996 | 3.1994 |

- **4 tunnels, 2 per side** ✓ (B4.1). Chord offsets from the bore axis
  **−3.000 / +3.000 mm** ✓ (ECO-3 x = 29 / 35).
- **ECO-9 stagger = |−392.250 − (−398.250)| = 6.000 mm** ✓.
- Both sides on the same x/z grid → each beam is a straight chord along y ✓.
- Exact OCC probe: a Ø1.6 × 34 coaxial cylinder on either beam axis intersects
  **0.00000 mm³** of plate; Ø2.0 × 34 intersects **1.19317 mm³** (see NB-2).

### PASS — B4.3 boss envelope and motor clearance

Boss main body measured **x 22.000…47.000, |y| 11.000…25.000, z −404.750…−385.750**
(25 × 14 × 19 mm), plus two 5 mm ear bands at z −409.750…−404.750 and
−385.750…−380.750 → 29 mm overall. Boss x-min **22.000** ≥ 22.0 ✓.

Measured on `dispenser_r8_assembly.step` (the stepper is the 69.936 cm³ solid):

```
  stepper in boss z-band       z[-409.75,-380.75]: x_max=18.0000 -> clearance to boss face x=22.000 = 4.0000 mm
  stepper in cavity z-band     z[-401.25,-389.25]: x_max=17.6000 -> clearance = 4.4000 mm
  stepper at Z_SENSOR +/-1     z[-396.25,-394.25]: x_max=17.6000 -> clearance = 4.4000 mm
  stepper material in the corridor x 18..22, |y|<25, z -409.75..-380.75 : 0.0 mm3
```

**4.000 mm worst case** (≥ 4.0 required; r6 was 1.4). Note the worst case is
4.000 exactly, not the 4.4 mm ECO-3 predicts, because a part of the stepper solid
reaches x = 18.000 in the ear band — at the beams themselves it is 4.400 mm.

### PASS — ECO-5 labyrinth (dimensionally exact)

| run | y band | tunnel centre x, beam A | beam B | Ø |
|---|---|---|---|---|
| inner | 12.000 → 14.500 | 29.0001 | 35.0001 | 3.1995…3.1999 |
| outer | 14.500 → 17.000 | **29.8001** | **35.8001** | 3.1995…3.2000 |

Offset **+0.8000 mm in x**, outer run length **2.500 mm** (14.500 → 17.000, the
cavity floor), ledge **0.800 mm** on the −x side of each tunnel (B4.5 asks
≥ 0.7) ✓. Identical on +y and −y.

### PASS — r1 BLOCKING 2 (bore lip) is genuinely fixed

The r7 seat was a flat-bottomed pocket cut against a plane at |y| = 10.6 in a
curved bore, leaving a printed wedge 0…0.610 mm thick across half of every
aperture. Re-measured on r8 (first material along +y from the bore axis, at the
beam height, compared with the exact bore radius √(121−(x−32)²)):

```
 -- beam A seat, z = -392.250 --
   x= 26.00  true bore |y|=  9.2195   first material |y|=  9.2195   recess/lip= -0.0000
   x= 26.40  true bore |y|=  9.4678   first material |y|= 12.0000   recess/lip= +2.5322
   x= 27.00  true bore |y|=  9.7980   first material |y|= 12.0000   recess/lip= +2.2020
   x= 27.50  true bore |y|= 10.0374   first material |y|= 14.5000   recess/lip= +4.4626
   x= 28.50  true bore |y|= 10.4283   first material |y|=none       (tunnel)
   x= 29.00  true bore |y|= 10.5830   first material |y|=none       (tunnel)
   x= 30.50  true bore |y|= 10.8972   first material |y|=none       (tunnel)
   x= 31.00  true bore |y|= 10.9545   first material |y|= 12.0000   recess/lip= +1.0455
   x= 32.00  true bore |y|= 11.0000   first material |y|= 11.0000   recess/lip= +0.0000
 -- beam B seat, z = -398.250 --  (mirror image, worst value +0.0000)
```

**Worst lip over both beams and both sides = 0.0000 mm** (r7: 0.610 mm). There is
no material anywhere between the true bore surface and the seat floor. The seat
mouth *is* the bore surface, as ECO-4 intends.

### PASS — clear aperture, symmetric, and the coverage proof survives

My own ray-cast map (0.02 mm grid, path |y| < 16.9 cavity-face to cavity-face,
`intersects_location` first-hit, nominal Ø3.2 area 8.0425 mm²):

```
  beam A clear area: 5.4976 mm2 (68.4 % of nominal)  centroid x=29.4002 z=-392.2500  x-range 28.220..30.600  z-range -393.790..-390.710
  beam B clear area: 5.4972 mm2 (68.4 % of nominal)  centroid x=35.4001 z=-398.2500  x-range 34.220..36.580  z-range -399.790..-396.710
```

The two channels are now **equal to 0.0004 mm²** (r7: 3.7340 / 1.3760 mm² =
2.71× asymmetry). Geometric maximum for two Ø3.2 circles offset 0.8 mm is
2r²·acos(d/2r) − (d/2)·√(4r²−d²) = **5.5094 mm²**, so the build is at **99.8 %**
of what ECO-5 permits. `beam_margin_pct` is no longer channel-dependent.

**The lateral-coverage proof (§4.3) is intact, and this is worth stating because
r1 said it was eroded.** Both apertures are displaced by the *same* +0.400 mm
(clear-aperture centroids 29.400 / 35.400), so the **chord separation is still
exactly 6.000 mm** and the guaranteed dark times are unchanged:

```
=== guaranteed (worst-lateral-position) dark time, v = 885.9 mm/s (40.0 mm free fall) ===
object     design chords -3.000/+3.000        measured centroids -2.600/+3.400
D13            13.018 ms (worst x0=+0.000)        13.018 ms (worst x0=+0.400)
D12            11.731 ms (worst x0=+0.000)        11.731 ms (worst x0=+0.400)
D11            10.407 ms (worst x0=+0.000)        10.407 ms (worst x0=+0.400)
best case, centred on a chord: D13 14.674  D12 13.546  D11 12.417  D8 9.030 ms
ECO-9 velocity solve: stagger 6.000 mm -> dt_mid = 6.536 ms at 885.9 mm/s (ELECTRONICS 4.3 quotes 6.54)
```

Ø11 guarantee **10.407 ms** vs the 9.7 ms gate = **7.3 % margin**, i.e. the full
§4.3 design margin, not r1's degraded 3.7 %. Per-beam free-fall velocities from
the retaining-plate underside (Z = −355.250) are **852.0 mm/s at beam A
(37.0 mm)** and **918.5 mm/s at beam B (43.0 mm)**.

### PASS — B4.4 nothing proud of the bore, windows are real and fit

`count_windows_r8` = **4 solids, 103.891 mm³ total**, each Ø5.900 × 0.950 at
(29.000, ±11.475, −392.250) and (35.000, ±11.475, −398.250); inner face at
**|y| = 11.0000** exactly (= the bore's maximum radius). Seat measured Ø**6.000**
in x (26.0001…32.0000) and Ø**5.9988** in z, floor at **|y| = 12.000**.

```
  minimum bore radius over z -405..-386, plate + windows, 1 deg x 0.25 mm scan = 10.9930 mm at z=-398.25 (nominal 11.000; STL facet error on a Dia22 bore is ~0.002)
  count_windows ^ retaining_plate_chute = 0.0 mm3
```

### PASS — B4.8 granule column

```
  Dia13 x 50 swept column ^ retaining_plate_chute = 0.0 mm3
  Dia13 x 50 swept column ^ count_windows         = 0.0 mm3
  Dia13 spheres at z = -389.25 / -392.25 / -395.25 / -398.25 / -401.25: 0.000000 mm3 each, plate and windows
```

### PASS — r1 BLOCKING 1 (the −y board could not be installed) is fixed

Exact OCC booleans against `retaining_plate_chute_r8`:

```
  y+1 as-built cavity centre x=34.5: 20x8x12 pocket 0.0000 | board 18x12x2 +1 mm all round (20x4x14) 0.0000 | insertion sweep 18x12x2 from |y|40->18  0.0000 mm3
  y-1 as-built cavity centre x=34.5: 20x8x12 pocket 0.0000 | board 18x12x2 +1 mm all round (20x4x14) 0.0000 | insertion sweep 18x12x2 from |y|40->18  0.0000 mm3
```

Cavity bisected on the export: **exactly 20.400 (x) × 8.000 (y) × 14.400 (z),
centred (34.500, ±21.000, −395.250)**, i.e. x 24.300…44.700, |y| 17.000…25.000,
z −402.450…−388.050. Both sides identical. r7's 203.418 mm³ duct obstruction on
−y is gone.

### PASS — r1 BLOCKING 4 (the BOM) is fixed

`cad/BOM.md` (mtime 14:00, after the 13:51 exports): **no TSSP4038 line** — the
only occurrence of the string is `"replaces the REJECTED TSSP4038"` inside the
VBPW34FAS row. Present: `count PD x2 Vishay VBPW34FAS`, `count amp TI
OPA2320AIDR`, `count emitter x2 Vishay TSAL6200`, `count windows x4 Dia6 x 1.0
cast PMMA disc … bonded`. The printed-parts table now carries `sensor_cover (x2)`
and `count_windows (x4)` (and `chute_plug`, `service_stand`). The phantom
`| 2 | M3x4 cup-point grub | IR emitter/receiver retention |` fastener line is
gone, replaced by `| 4 | M2x6 self-tap | sensor covers -> boss ears (ECO-12) |`,
which matches the modelled hardware (2 pilots per boss × 2 bosses). **B4.7 passes
on every clause.**

### PASS — r1 BLOCKING 5 / N3 / ECO-12: retention exists and is real

`sensor_cover_r8` = 2 bodies, 1689.734 mm³ each, bbox x 22.000…47.000,
|y| 19.500…27.000, z −409.750…−380.750. Measured features:

- cover plate |y| 24.600…27.000 (2.400 thick), register lip |y| 24.600…25.000
  (**0.400 mm**), lip footprint x 24.500…44.500 and z −402.250…−388.250 →
  **0.200 mm/side** clearance into the 20.400 × 14.400 cavity;
- **four 3.000 × 3.000 mm posts** at x 25.5…28.5 / 40.5…43.5 and
  z −401.75…−398.75 / −391.75…−388.75, tips at **|y| = 19.500**;
- contact area in the 0.5 mm slab just outboard of |y| = 19.500:
  **30.000 mm² over an 18 × 12 board footprint** (36.000 mm² of total post face);
  N3 asks ≥ 8 mm² ✓;
- **two M2 pilots per boss**, Ø1.600 along y at (x = 34.500, z = −407.250) and
  (x = 34.500, z = −383.250), with matching **Ø2.300** clearance holes in the
  cover — so the 4 × M2×6 in the BOM have somewhere to go;
- **Ø5.000 grommet port** in the cover at (x = 41.000, z = −406.250), on the axis
  of the plate's duct socket (plate void x 38.500…43.500, z −409.750…−402.450) —
  both sensor boards now have a covered cable exit;
- `sensor_cover ^ retaining_plate_chute = 0.0 mm³`, `sensor_cover ^ count_windows
  = 0.0 mm³`, `service_stand ^ sensor_cover = 0.0 mm³`.

---

### BLOCKING — the emitter and the receiver have no volume: the modelled retention parks the board 0.500 mm off the aperture plane

This is the one thing r1 could not see, because in r1 there was no retention
feature at all to measure. Now there is, and it puts the board at the wrong end
of the cavity.

Measured, exactly, on the exports:

```
  aperture plane (cavity floor, where all four tunnels open)   |y| = 17.000
  cover post bearing face (fixes the board's outer face)       |y| = 19.500
  -> board slot                                                      2.500 mm
  plate material in the 20.4 x 2.500 x 14.4 board slot   = 0.0000 mm3 (+y and -y)
  sensor_cover material in that slot                     = 0.0000 mm3 (+y and -y)
  cavity depth behind the board face, |y| 19.500..25.000      5.500 mm
     of which sensor_cover (posts + lip) occupies 295.600 mm3 of a 1615.7 mm3 envelope = 18.3 %
  no counterbore, no LED pocket, no component relief anywhere in the cavity floor:
     tunnel Ø at the floor (y = 16.8) = 3.200 mm, centres x = 29.800 / 35.800
```

The tunnels open **in the cavity floor**, so the emitter and the photodiode must
sit between the board and that floor — there is nowhere else for them to point.
The as-built stack gives them **2.500 mm minus the board thickness**: 0.900 mm
for a 1.6 mm PCB, 0.500 mm for the 2.0 mm board the punch list and the r1/r2
sweeps both use. Meanwhile **5.500 mm of cavity depth sits empty behind the
board**, which is exactly the space ECO-3's 8 mm depth was sized to provide
(8.0 ≈ 2 mm board + a 5 mm-class through-hole LED).

Against the parts the BOM now orders — and these package figures are
**[knowledge, not read off a datasheet file in this run; closure = the Vishay
package drawings]**:

| part | package height, aperture-facing | fits the 2.500 mm slot? |
|---|---|---|
| Vishay **TSAL6200** (5 mm radial 940 nm LED) | ≈ 5.8 mm body above the seating plane (≈ 8.6 mm with leads) | **no**, by ≈ 3.3 mm even with a zero-thickness board |
| Vishay **VBPW34FAS** (BPW34 DIL case with daylight filter) | ≈ 3.2 mm case thickness | **no**, by ≈ 0.7 mm even with a zero-thickness board |

So the count sensor as specified cannot be assembled into the count sensor as
modelled. This is the same class of defect as rev-0 RT-3 — the electronics
document describes hardware the CAD does not contain — one level down: the
apertures, tunnels, windows, labyrinth, cavity and retention are all now real,
but the two active components are not housed.

**Why the round's own checker passed it:** `cad/verify_r2.py:398-408` tests an
empty `Box(20, 8, 12)` and an 18 × 12 × 2 *bare board* insertion sweep. Neither
carries a component height, so neither can see this. (N14: a check written from
the requirement would have used the emitter's package envelope, since ELECTRONICS
§7 names the part.)

**What closes it (any one of these, measured):**
1. Shorten the cover posts so the board's outer face lands at |y| ≈ 23.0
   (board 21.0…23.0), leaving **≈ 4.0 mm** of aperture-facing component height
   and re-checking the cover screw/lip geometry; or
2. keep the board where it is and sink a component pocket into the cavity floor
   around each tunnel mouth (Ø ≥ 5.5 × ≥ 5.0 deep at x = 29.800 / 35.800,
   re-checking wall to the bore: the floor is only 17.000 − 10.583 = **6.417 mm**
   thick at the beam axis and 17.000 − 11.000 = **6.000 mm** at x = 32, so a 5 mm
   pocket leaves ~1.0–1.4 mm — probably too thin, i.e. option 1 is the real one); or
3. change the specified parts to sub-1 mm SMD emitter/detector and correct
   `ELECTRONICS.md` §4.4, §7 and the optical budget (the 182× excess gain is
   computed for TSAL6200 at 40 mW/sr).
Whichever is taken, the acceptance test is: **a solid of the emitter's package
envelope, seated on the board plane and centred on the tunnel mouth at
x = 29.800 / 35.800, booleans to 0.000 mm³ against the plate and the cover, on
both sides** — and the same for the receiver.

---

### NONBLOCKING — measured, recorded, no geometry demanded of this round

**NB-1 — the storage plug presses on the two beam-B windows.** `chute_plug_r8`'s
sealing land measures **r = 11.1500** (Ø22.300, the designed 0.300 mm diametral
interference) and runs from its top **z = −395.250** down past z = −405. The
beam-B windows span z −401.200…−395.300, so the plug lands on them:

```
  window 0 (x 26.05..31.95, y +11.00..+11.95, z -395.20..-389.30): chute_plug ^ window = 0.0000 mm3
  window 1 (x 32.05..37.95, y +11.00..+11.95, z -401.20..-395.30): chute_plug ^ window = 0.5981 mm3
  window 2 (x 26.05..31.95, y -11.95..-11.00, z -395.20..-389.30): chute_plug ^ window = 0.0000 mm3
  window 3 (x 32.05..37.95, y -11.95..-11.00, z -401.20..-395.30): chute_plug ^ window = 0.5981 mm3
  chute_plug ^ retaining_plate_chute = 200.9078 mm3   (the intended press fit)
```

Every fit/removal of the plug scrubs a bonded Ø6 × 1 mm sacrificial acrylic disc
at **0.150 mm/side** of interference. The beam-A windows clear the plug top by
**0.050 mm**. The push is radially outward (into the seat, which backs the window
0.050 mm away), so the failure mode is bond-line crush and scratching of the very
surface ECO-4 exists to keep clean, not ejection into the chute. One-line fix:
end the plug's land above z = −395.00, or relieve it to r ≤ 10.95 over
z −401.50…−395.00. Note the round's checker deliberately keeps `chute_plug` out
of the all-pairs interference sweep ("the plug's interference is a designed
0.3 mm press fit"), which is why this is not in `BUILD-NOTES-r2.md`.

**NB-2 — B4.2 as written still fails, and the build notes' arithmetic for why is
wrong (the conclusion is right).** Exact OCC, both beams identical:

```
  Dia2.0 x 60 on the beam axis: plate  1.19317 mm3   (r7: 16.1448 / 1.6675 -> the asymmetry is gone)
  Dia2.0 x 34:                  plate  1.19317 mm3
  Dia1.6 x 34:                  plate  0.00000 mm3
  Dia3.2 x 34:                  plate 12.66539 mm3
```

`BUILD-NOTES-r2.md` §2.4 says the "*inscribed coaxial* circle about the nominal
axis is Ø0.8". It is **Ø1.6** — a circle of radius r about x = 29 lies inside the
Ø3.2 circle about x = 29.8 iff 0.8 ≤ 1.6 − r, i.e. r ≤ 0.8, diameter 1.6 — and
the export agrees (Ø1.6 × 34 = 0.00000 mm³). The notes understate their own
result by 2×. Their proposed resolution (restate B4.2 as an area criterion,
≥ 5.4 mm² measured on a ray grid) is the right call and I second it; the correct
supporting numbers are **lens 5.5094 mm² theoretical, 5.4976 / 5.4972 mm²
measured, largest clear coaxial cylinder Ø1.600**.

**NB-3 — ECO-4's dimensional wording is still not met, as recorded in O-8, and
here is the size of it.** Seat depth measured **1.000 mm** from |y| = 11.000 to
the floor at |y| = 12.000; B4.4 asks 0.400 ± 0.05. The window's inner face is at
|y| = 11.000 and the bore surface under the Ø5.9 window footprint runs from
|y| = 11.000 (at x = 32) to **|y| = 9.2521** (at the window edge x = 26.05), so
the open lune in front of each window is **0.417 mm deep at the beam axis** and
**1.748 mm deep at the window's x-extremes**. It is open, undercut-free and
swab-reachable — I agree with the build notes that this is the property ECO-4
wants — but "flush at y = ±11" is still false and `ELECTRONICS.md` §4.5 has not
been edited (mtime 2026-08-07 04:13, before this round). O-7/O-8/O-9 remain open
against `electronics/`.

**NB-4 — the component grid is at x = 29.800 / 35.800, not 29 / 35, and nothing
says so.** At the cavity floor (where the parts sit) the tunnel mouths are the
*labyrinth* runs, centred **29.8001 / 35.8001**. Their 6.000 mm spacing — the
number ELECTRONICS §7 gives the board ("the two LEDs sit 6.0 mm apart in x and
6.0 mm apart in z") — is preserved, so the board layout is unaffected in *pitch*,
but its absolute datum is offset **+0.800 mm in x** from ECO-3's aperture axes.
The board itself is centred at **x = 34.500** (cavity centre), not on the chute
axis; `verify_r2.py:399` encodes this as `Pos(PCD_R + 2.5, …)` but neither the
checker's printed line ("20x8x12 pocket 0.0000 mm3") nor the build notes disclose
the offset. For the record, a 20 × 8 × 12 pocket centred on the chute axis
x = 32.000 interferes by **220.8000 mm³** on both sides; at x = 34.500 it is
0.0000. Add the 29.800 / 35.800 and 34.500 datums to the board's fabrication
note, or the first sensor board will be laid out to 29 / 35.

**NB-5 — the dark-time gate is derived for a pencil beam; the as-built aperture
is 2.38 × 3.08 mm.** The clear aperture measured above is **2.380 mm wide in x
and 3.080 mm tall in z**. Falling at 885.9 mm/s a granule takes **3.476 ms** to
traverse the aperture's own vertical extent — **33 %** of the 10.407 ms
guaranteed Ø11 dark time. §4.2/§4.3's dark-time table treats the beam as a line,
so the measured dark time depends on where the detection threshold sits between
0 % and 100 % occlusion (at 50 % the aperture height cancels; at the near-total
occlusion implied by 182× excess gain and a 1 µA threshold it is ~3.5 ms short).
This is an electronics/threshold item, not a CAD defect — ECO-3 specifies Ø3.2 —
but the 9.7 ms gate is not derivable without stating the occlusion fraction, and
nobody has. Carry it into B1.

**NB-6 — the sensor cavity is not sealed from the outside.** The cover/boss joint
is a flat land at |y| = 25.000 with **no gasket groove in either part** (y-scans
at x = 23.0 / 34.5 / 46.0 and z = −386.0 / −395.25 / −404.0 show cover material
25.000…27.000 and plate material up to 25.000, unbroken), the register lip has
**0.200 mm/side** clearance, and the two M2 screws per cover are **both on the
line x = 34.500**, leaving the cover's ends overhanging **12.500 mm** each way.
Chute-side sealing is fine — that is the window's job and it is done — but any
dust that reaches the cavity lands on the window's *inner* face and in the
tunnel, which is the one surface ECO-4 explicitly makes unserviceable
("permanently sealed"). Either add a groove/bead at the land or say plainly in
README/DESIGN that the sensor cavity is dust-resistant, not sealed (this is the
N8 rule applied to a joint N8 did not enumerate).

**NB-7 — documentation has not caught up, and one line is now false.**
`README.md` (mtime 04:51, before the r8 build) still says of the count
requirement: *"**NOT MET in this revision** — the sensing that makes the claim
true (ECO-3/ECO-9) exists only in `electronics/`, not in the CAD. See RT-3"*, and
its RT-3 row still says the ECOs "were never merged into `cad/dispenser.py`" and
"`cad/BOM.md` still lists the TSSP4038". All three statements are false against
r8. `docs/DESIGN.md` (mtime 13:50) carries the same RT-3 text at line 637. Under
the standing RT-19/N15 rule this must be corrected in the same round that changed
the geometry.

**NB-8 — BOM gaps (small).** No line for the two sensor PCBs themselves
(18 × 12 mm, 2-layer, ELECTRONICS §7) and no line for the window bonding adhesive
(the method is named inside the window row's description, but nothing is
orderable). The B11.4 reserve carries 12 g for "count-sensor boards + 2 cable
looms", so the mass is accounted for; the parts are not.

---

### What has to change for me to pass this domain

1. **House the emitter and the receiver.** Move the board plane (post tips) so
   there is ≥ 4 mm of aperture-facing component height, or pocket the cavity
   floor, or re-specify the parts. Prove it with a package-envelope boolean
   against plate **and** cover, both sides, 0.000 mm³ — not with a bare-board
   sweep.
2. Relieve `chute_plug` over the beam-B window band (or shorten its land) and
   re-print `chute_plug ^ count_windows` = 0.0000 mm³ on all four windows.
3. Publish the 29.800 / 35.800 / 34.500 board datums with the geometry.
4. Correct `README.md` line 40 and the RT-3 rows in `README.md` / `docs/DESIGN.md`
   to what r8 actually contains.
5. Carried, not mine to edit: `ELECTRONICS.md` ECO-3 boss height (14 → 19 mm),
   ECO-4 "flush at y = ±11", ECO-5 vs B4.2 (area criterion, with Ø1.600 as the
   correct inscribed-cylinder figure, not Ø0.8).

## assembly

**Verdict: FAIL — 3 blocking findings.** All four of round 1's blockers (A-1
missing chassis adapter, A-2 cartridge/housing interference, A-3 bay+lid
seating, A-4 window insertion) are **closed on the r8 exports**, and the torque
path motor→gearbox→shaft→disc still measures clean. Three parts, however,
cannot be installed or actuated on the geometry as exported — `sensor_cover`
(×2), `fill_cap` — and the drive has no reaction path: the quarter-turn latch
that is the cartridge's only retention is free to rotate 24.65° in the exact
direction the motor's stator reaction pushes it, ending in the drop-out window.

### Provenance

- Measured on `cad/exports/*_r8.*`, mtime **2026-08-07 13:51:48/49**.
  `md5(dispenser_r8_assembly.stl) = 812d9a0668b7ad0276aee63d14b95733`,
  `md5(retaining_plate_chute_r8.stl) = a7d64399c6dccabf46306f5ce2224296`,
  `md5(top_plate_r8.stl) = 85689455398cd502df462ce951209a69`,
  `md5(meter_housing_r8.stl) = 4182bfe7660018af1d1decd5ac2624de`,
  `md5(pocket_disc_r8.stl) = 57acbeca4326e2bb917933880ce6fade` — the first four
  match `BUILD-NOTES-r2.md` §0, so I am measuring the same exports the builder
  reported on.
- All obstruction volumes are **exact OCC booleans** on the STEP bodies
  (`build123d.import_step` + `Shape.intersect`), not voxel estimates. Ray probes
  are trimesh 5.0.0 on the STLs. venv
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`, build123d 0.11.1,
  trimesh 5.0.0, numpy 2.5.1.
- COTS bodies were lifted from `dispenser_r8_assembly.step` by volume rank
  (motor+gearbox+shaft 69.936, clip plate 11.523, bearing 1.495, blind-mate PCB
  1.174, thrust washer 0.317, brush strip 0.312 cm³). That identification is an
  **ASSUMPTION** from size/position, unchanged from round 1.
- Fastener axes were taken from the model's named constants (`SKIRT_AS`,
  `FLANGE_SCREW_R/AS`, `BAY_SCREW_X/Z`, `RIB_ZC`, `GRUB_A`, `PLUNGER_A`,
  `SENS_SCREW_DZ`, `BOLT_DX/DY`) and then **verified on the exports** — every
  corridor below is a boolean against the exported solids.

### 0. Part inventory and the static interference matrix

```
hopper                   nsol= 1 V=  108.849cm3 bb=[  -78.00,  -88.00, -334.250]->[   78.00,   78.00, -238.550]
meter_housing            nsol= 1 V=  103.672cm3 bb=[  -58.00,  -58.00, -358.250]->[   58.00,   60.50, -326.250]
top_plate                nsol= 1 V=   96.200cm3 bb=[  -78.00,  -85.50, -248.550]->[   78.00,   78.00, -181.550]
pocket_disc              nsol= 1 V=   72.728cm3 bb=[  -46.00,  -46.00, -350.750]->[   46.00,   46.00, -320.250]
retaining_plate_chute    nsol= 1 V=   57.995cm3 bb=[  -55.30,  -52.00, -410.250]->[   52.00,   52.00, -351.250]
electronics_bay          nsol= 1 V=   19.299cm3 bb=[  -30.00,  -90.00, -363.100]->[   30.00,  -48.96, -306.600]
fill_cap                 nsol= 1 V=   11.132cm3 bb=[  -27.50,   17.50, -240.000]->[   27.50,   72.50, -231.045]
bay_lid                  nsol= 1 V=    7.610cm3 bb=[  -29.00,  -92.00, -362.100]->[   29.00,  -88.60, -312.100]
agitator                 nsol= 1 V=    4.291cm3 bb=[  -25.08,  -41.44, -325.900]->[   46.70,   41.44, -318.350]
brush_holder             nsol= 1 V=    3.544cm3 bb=[  -51.84,    1.11, -340.550]->[  -11.22,   35.51, -326.250]
sensor_cover             nsol= 2 V=    3.379cm3 bb=[   22.00,  -27.00, -409.750]->[   47.00,   27.00, -380.750]
count_windows            nsol= 4 V=    0.104cm3 bb=[   26.05,  -11.95, -401.200]->[   37.95,   11.95, -389.300]
chute_plug               nsol= 1 V=    6.097cm3 bb=[   18.00,  -14.00, -419.250]->[   46.00,   14.00, -395.250]
service_stand            nsol= 1 V=  103.908cm3 bb=[  -90.00,  -90.00, -426.450]->[   90.00,   90.00, -358.250]

ALL-PAIRS EXACT BOOLEAN INTERFERENCE (assembly STEP, 22 solids, 231 pairs):
  40 bbox-overlapping pairs boolean-checked, 0 with non-zero intersection
```

`top_plate` is the real 96.200 cm³ chassis adapter + neck reaching the clip-plate
underside at Z = −181.550 (r7: a 0.808 cm³ Ø9 × 24 stub) — **A-1 is closed.**
`brush_holder ^ meter_housing` is now **0.0000 mm³** (r7: 3.3540 residual at the
seat, my round-1 NB-1) — closed. Export integrity, re-measured independently:

```
  14/14 part STLs watertight, 0 non-manifold edges
  (agitator euler=2, bay_lid -6, brush_holder 0, chute_plug 2, count_windows 8,
   electronics_bay -8, fill_cap 2, hopper -14, meter_housing -10, pocket_disc -30,
   retaining_plate_chute -66, sensor_cover -8, service_stand 0, top_plate -36)
```

### 1. Derived assembly order, with the swept-volume obstruction numbers

Direction = the direction the part **travels**. Each row is 21 stations of a
40–60 mm straight approach, exact boolean against every already-installed solid;
"swept" rows are a true union of the intermediate poses booleaned against the
obstacle.

| # | Operation | Travels | Obstruction along the path | Seated | Verdict |
|---|---|---|---|---|---|
| 1 | `meter_housing` in fixture | — | — | — | — |
| 2 | igus JFM-2023-07 into the roof bore | **−Z** | **0.0000** over 40 mm | 0.0000 | OK |
| 2′ | (same, from below) | +Z | peak **580.5963** at t = 6 | — | not possible |
| 3 | `brush_holder` + `brush_strip` radial/−Z | **−Z** | **0.0000** over 40 mm | **0.0000** | OK (r7: 3.3540 at the seat) |
| 3′ | (same, from below) | +Z | peak **1021.3371** at t = 18 | — | not possible |
| 4 | `pocket_disc`, hub up through the bearing | **+Z** | **0.0000** over 40 mm | 0.0000 | OK |
| 4′ | (same, from above) | −Z | peak **29564.7925** at t = 12 | — | not possible |
| 5 | `agitator` onto the Ø15 hex | **−Z** | **0.0000** over 40 mm | 0.0000 | OK |
| 6 | washer + motor onto the plate (sub-assembly) | +Z | driver corridor Ø8.0 (§3 F1b) | 0.0000 | OK, **sub-assembly only** |
| 7 | drive cartridge (plate+motor+washer) into the housing at 20–24° of unlock | **+Z**, 60 mm | **0.0000** vs housing at 20/22/24°; **swept union** plate 401756.6 mm³ ∩ housing = **0.0000**, motor 139902.9 mm³ ∩ housing = **0.0000** | 4.2552 / 4.6955 / 5.1242 vs `pocket_disc` (NB-4) | **OK — A-2 closed** |
| 7b | rotate cartridge 20–24° → 0° to lock | rot | **0.0000 mm³ over the whole 0…24° band** | 0.0000 | OK (but see BLOCKING A-7) |
| 8 | M3 grub screw, radial θ = 202.5°, z = −341.25 | radial in | continuous **Ø2.6 void r 2.75 → 52 = 0.0000** in *both* disc and housing | — | OK |
| 9 | `electronics_bay` onto the housing ribs | **+Y** | **0.0000** over 40 mm | 0.0000 | **OK — A-3 closed** |
| 10 | `bay_lid` | **+Y** | **0.0000** over 30 mm | 0.0000 | OK |
| 10′ | (same, outboard) | −Y | peak 3627.0216 | — | not possible |
| 11 | `hopper` down over the bay riser | **−Z** | **0.0000** over 60 mm | 0.0000 | OK |
| 12 | `top_plate` onto the hopper flange | **−Z** | **0.0000** over 40 mm | 0.0000 | OK |
| 13 | `fill_cap` bayonet | −Z + rot | **BLOCKED**, see A-5 | 0.0000 | **BLOCKED** |
| 14 | `sensor_cover` ×2 into the boss cavities | ±Y | **BLOCKED**, see A-6 | 0.0000 | **BLOCKED** |
| 15 | `count_windows` ×4, pushed out from the chute bore | radial out | **0.0000** over 12 mm, all four | 0.0000 | **OK — A-4 closed** |
| 15′ | (same, from the component cavity) | radial in | **18.3324** (a Ø5.90 disc cannot pass a Ø3.2 aperture) | — | not possible, as designed |
| 16 | `chute_plug` (ground only) | +Z | rises to **202.1040** at the seat | 202.1040 | designed 0.3 mm press fit |

Cartridge service removal with the whole machine built (unlock 22° + 60 mm
descent, members = plate + motor + washer + 2 covers + 4 windows, against
housing / disc / brush_holder / hopper / bay / lid / top_plate / agitator /
bearing / brush_strip): **TOTAL 4.6955 mm³**, all of it `motor ^ pocket_disc` at
the seat (NB-4). With the disc counter-indexed to the unlock angle it is
**0.0000** — the documented drop-out path is real.

The locked-pose withdrawal column is the latch working, and I read it the same
way the build notes do:

```
  t_to_go   0.0  cartridge ^ housing =     0.0000 mm3
  t_to_go   1.0  cartridge ^ housing =    73.9147 mm3
  t_to_go   2.0  cartridge ^ housing =   166.3080 mm3
  t_to_go   4.0  cartridge ^ housing =   258.7014 mm3
  t_to_go   6.0  cartridge ^ housing =    92.3933 mm3
  t_to_go  10.0  cartridge ^ housing =     0.0000 mm3
```

### 2. Torque path — motor → gearbox → shaft → metering disc: **EXISTS and closes**

Every number measured on the r8 exports:

```
 gearbox body            R=18.000  z -384.450 .. -355.250
 output flange face      z = -355.250
 output pilot boss       R= 8.000  z -355.250 .. -353.200   (Dia16.00, ASSUMPTION carried as O-5)
 output shaft            R= 3.000  z -353.200 .. -337.250   (15.900 mm exposed)
 shaft D-flat            r = 2.500 over theta 172.5..232.5 (60.5 deg), z -349.250 .. -337.250 = 11.950 mm

 disc bore               r = 3.049..3.050 round; FLAT at r = 2.550 over theta 181..224 (44 deg)
 disc bore extent        z -350.750 .. -337.250 = 13.500 mm ; D-flat z -349.250 .. -337.250 = 11.950 mm
 FLAT-ON-FLAT overlap    11.950 mm ; flat chord 2*sqrt(3.0^2-2.55^2) = 3.161 mm
 flat bearing area       37.77 mm2
 drive torque            0.14 N*m x 5.18 x 0.90 = 0.6527 N*m
 tangential force        261.1 N at r = 2.5 mm  ->  bearing stress 6.91 MPa on CF-PETG

 grub, disc channel      Dia3.4, r 9.00 -> 46.00, theta 202.5, z -341.25 : disc 0.0000, housing 0.0000
 grub, disc pilot        Dia2.6, r 2.75 -> 9.00                          : disc 0.0000
 grub, housing port      Dia3.6, r 47.00 -> 52.00                        : housing 0.0000
 B2.2 continuous void    Dia2.6 from r=2.75 (bore wall) to r=52 (outside the housing) = 0.0000 / 0.0000
 B2.3 driver access      Dia3.4 x 25 mm on the grub axis vs every other solid = 0.0000
                         (Dia4.0 -> 11.9433 mm3, meter_housing)

 disc -> agitator        Dia15 hex spigot, seated 0.0000
 bearing seat            bearing bb z -334.950..-325.950, seated 0.0000
 thrust stack            washer top -350.800, disc bottom -350.750 -> 0.050 mm
```

**B2.1, B2.2, B2.3 pass on the exports.** Torque is carried
motor → 5.18:1 planetary → Ø6 shaft flat (11.950 mm engaged, 37.77 mm²,
6.91 MPa) → disc D-bore → disc → Ø15 hex → agitator. What the *drive* is missing
is not the torque path but the **reaction** path — see A-7.

### BLOCKING A-5 — the fill cap cannot be opened (or fitted): the B6 stand-off neck traps it

`fill_cap` is a quarter-turn bayonet in the top plate's fill port at
FILL_POS = (0, 45), lugs locked on the local ±X axis, insertion notches at the
local ±Y (rotate 90° to unlock). Measured on the exports:

```
 available free lift (rot 0):  free 0.05 mm ; first fouling lift 0.10 mm -> 2.3024 mm3
 rotation at the seated height vs top_plate:  0.0000 mm3 at EVERY angle 0..180 deg
 rotation at the seated height vs hopper:
     rot   0 deg -> 0.0000    rot  45 -> 0.0000    rot  60 ->  0.9188
     rot  75 deg -> 11.5657   rot  85 -> 16.3566   rot  90 -> 16.9480  <== the UNLOCK angle
     lump V=16.948 mm3 at x[-3.50,3.50] y[69.41,71.20] z[-240.00,-238.60]
 360 deg rotation scan at a 3 mm lift (top_plate + hopper): minimum 164.7133 mm3 at 90 deg
 SWEPT union over an 8 mm lift at the 90 deg unlock angle (30486.4 mm3 of sweep):
     swept ^ top_plate =  581.7683 mm3 ;  swept ^ hopper = 17.5533 mm3
 the blocking material, at rot 90 / lift 3: V=164.713 mm3 at
     x[-17.76,17.76]  y[21.40,24.00]  z[-233.54,-231.19]
 probe of top_plate at x[-18,18] y[20,25] z[-234,-228]: V=495.633 mm3, y[20.00,24.00] solid
```

That block of material is the **B6 stand-off neck wall** (plan half-extent
a = 24.000 mm, measured by the builder and re-measured here as solid from
y = 20.00 to 24.00 above Z = −234). The fill port centre is at y = 45 with
FILL_R ≈ 27.5, so the cap's proud wing grip reaches y = 17.5 — **6.5 mm inside
the neck footprint**. The cap therefore has 0.05 mm of vertical freedom, its
lugs already foul the hopper by 16.948 mm³ before it reaches the unlock angle,
and at unlock + 3 mm of lift it is 164.713 mm³ into the neck.

Consequences: the dispenser cannot be refilled (B12.2 asks for a cap-removal
sweep of 0.000 mm³ against the ground plane *and the dispenser*), and because
the path is reversible, the cap as exported could not have been fitted either.
`BUILD-NOTES-r2.md` does not measure the cap-removal sweep anywhere; §2.12 only
measures the *stand*. This is a direct collision between directive 3 (B6 neck)
and directive 4 / B12 (refill), and it has to be resolved by geometry — move the
fill port outboard of the neck footprint, shrink the cap's proud grip inside
r < 21 about the port axis, or put the port in the hopper side wall as B12.3
already contemplates.

### BLOCKING A-6 — `sensor_cover` ×2 cannot be installed: the plate's own harness duct stands 0.50 mm outboard of it

`sensor_cover` (the ECO-12/N3 board-retention part introduced this round,
2 × 1689.711 mm³) seats with **0.0000 mm³** of interference — which is all the
build notes check ("ECO-12 cover does not foul the plate: 0.0000 mm³"). There is
no insertion sweep for it anywhere in `BUILD-NOTES-r2.md`. There is no clear
path:

```
 sensor_cover(+Y) straight-line paths, exact boolean vs plate/motor/housing/disc:
    travelling -Y (radial inboard, the only sensible sense), 25 mm : worst  151.0001 mm3 at t_to_go 4.17
    travelling +X, 30 mm                                          : worst   83.2600 mm3
    travelling -X, 30 mm                                          : worst   83.2600 mm3
    travelling +Z, 35 mm                                          : worst   85.0102 mm3
    travelling -Z, 35 mm                                          : worst  416.3533 mm3
 SWEPT-VOLUME obstruction, radial install, union of 9 stations over 12 mm:
    swept solid 10054.38 mm3 ; swept ^ retaining_plate_chute = 488.4789 mm3   (a clear path is 0.0000)
 station detail (radial inboard):
    t_to_go 12.00 -> 0.0000
    t_to_go 10.00 -> 67.8198   lump x[41.00,47.00] y[35.00,36.50] z[-409.37,-380.75]
    t_to_go  6.00 -> 113.1013  lump x[37.00,47.00] y[30.60,33.00] z[-409.75,-380.75]
    t_to_go  4.00 -> 150.1466  lump x[37.00,47.00] y[29.00,31.00] z[-409.75,-380.75]
    t_to_go  1.00 -> 12.5996
    t_to_go  0.50 -> 0.0000
 two-stage attempt (shift -X by dx, push -Y, then +X back to the seat):
    dx= 3.0 : radial push worst  67.9600 ; lateral re-entry worst  67.9600
    dx= 6.0 : radial push worst  31.0692 ; lateral re-entry worst  74.0800
    dx=10.0 : radial push worst  12.8800 ; lateral re-entry worst  58.7800
```

Cause, measured on the plate export: plate material occupies
**x 38.00…52.00, y 27.50…36.50, z −410.25…−378.00 (1073.114 mm³ inside a
14 × 22 × 34 probe box)** — the round-2 symmetric harness duct leg and its
grommet socket. The cover's outer face is at **y = 27.00**, so the duct stands
**0.50 mm** outboard of it (the model builds this deliberately:
`DUCT_SOCK_Y = SENS_BOSS_Y1 + COVER_T + 0.5 = 27.5`) and overlaps the cover's
own x-envelope (22.00…47.00) over **x 38…47**. The cover has to pass through
that wall to reach its seat.

Because the cover *is* the board retention (ECO-12) and also the cavity closure,
this re-opens count-sensor BLOCKING 5 as an assembly defect: the boards install
(that sweep is 0.0000 and I confirm it), but nothing can be fitted to hold them.
Fix directions, both cheap: pull the duct leg outboard of x = 47.5, or end the
cover at x ≤ 37.5 with its own ears.

### BLOCKING A-7 — the drive has no reaction path: the latch is free to unwind in the direction the motor pushes it

The quarter-turn latch is the cartridge's **only** attachment to the housing —
`cad/BOM.md`'s fastener table has no plate→housing screw (the M5 ball-nose
plunger is the *disc rim* detent at θ = 67.5, and the 3 × M3x8 Delta-PT are the
hopper skirt tabs). Measured free rotation of the seated cartridge
(plate + motor + washer) against `meter_housing`, exact boolean, 1° steps:

```
   -6: 184.787   -5: 150.951   -4: 116.919   -3:  82.497   -2:  47.487   -1:  11.692
   +0:   0.000   +1:   0.000  ...  +20:   0.000  +21:   0.000  +22:   0.000  +23:   0.000  +24:   0.000
  +25:  11.692  +26:  47.487  +27:  82.497  +28: 116.919  +29: 150.951  +30: 184.787
  contiguous free band about 0 deg: 0 .. 24 deg  -> 24 deg of free rotation with NO circumferential stop
```

So the locked pose has a **hard circumferential stop in −θ only** and **24.65°
of free travel in +θ**, and the far end of that free band *is* the drop-out
window: the axial insertion sweep is 0.0000 mm³ over 60 mm at +20°, +22° and
+24° of unlock (30.2908 mm³ at +18°, 53.0289 at +26°).

Which way does the drive push? Measured on the housing export, roof underside
above the disc top at r = 32:

```
  theta 95 -> gap  1.500 mm   96 -> 1.645   100 -> 2.687   110 -> 5.291
        120 -> 7.896   129 -> 10.240   130 -> 10.500   131..250 -> OPEN (fill window)
        255 -> 7.707   260 -> 4.915   266 -> 1.564   270..90 -> 1.500
```

The entry ramp descends from 10.500 mm at θ = 130 to 1.500 mm at θ ≤ 95, i.e.
pockets run **−θ (clockwise seen from +Z)** — the model's own source says the
same thing at `dispenser.py` L1404 ("the disc runs −Z / CW seen from above").
The gearbox therefore applies −θ torque to the disc and its stator reaction on
the plate is **+θ — the free direction**.

Numbers: drive torque **0.6527 N·m** (the model's own
0.14 × 5.18 × 0.90). The only restraint is lug/shelf friction:
cartridge ≈ 431 g `[A: plate 57.995 cm³ × 1.27 = 73.7 g + 350 g stepper + ~7 g
covers/windows/washer]` → 4.23 N on 3 lugs at r = 53.55 mm; at µ = 0.3 `[A]`
that is **0.068 N·m**, a **9.6× deficit**. The cartridge will index itself round
to the drop-out window and release the motor, disc drive, drop chute and both
count-sensor boards from the aircraft. Even at µ = 1.0 the restraint is
0.226 N·m, still 2.9× short.

This is not fixed by the detent: the ball plunger acts between the housing and
the **disc rim**, not between the housing and the plate. The fix is a
circumferential stop plus a positive lock — a second shelf face at +25° (so the
free band is bounded on both sides), or a screw/spring latch through a lug. Any
fix must print the two-sided free-rotation band and the holding torque.

### 3. Tool-access corridors — largest clear driver diameter per fastener

Method: a cylinder on the fastener axis starting at the head-bearing plane and
extending **away** from the joint, diameters stepped
1.5/2.0/2.5/3.0/3.4/4.0/5.0/6.0/8.0/10.0/12.0 mm; the largest diameter with a
**0.0000 mm³** exact boolean against every other assembly solid is reported.

| ref | fastener | corridor | max clear driver | first blocking size → volume |
|---|---|---|---|---|
| F1 | 4 × M3x8 gearbox screws, +Z, **in situ** | 25 mm | **Ø0.0** | Ø1.5 → **15.728 mm³** (housing 12.7235 + bearing 3.0041) |
| F1b | same four, **plate+motor sub-assembly** | 25 mm | **Ø8.0** | Ø10.0 → 2.1304 (thrust washer) |
| F2 | M3x4 grub, key from the disc OD outward | 25 mm | **Ø3.4** | Ø4.0 → 11.9433 (housing) |
| F2b | M3x4 grub, hand space outboard (r = 53 →) | 40 mm | **Ø4.0** | Ø5.0 → 5.1053 (housing) |
| F3 | M5 ball plunger, radial from r = 63 outward | 30 mm | **≥ Ø12.0** | — |
| F4 | 3 × M3x8 hopper skirt tabs, θ = 30/105/225, radial | 25 mm | **≥ Ø12.0** each | — |
| F5 | M3x6 wiper end tab, radial from r = 58.1 (θ = 148) | 25 mm | **≥ Ø12.0** | — |
| F6 | 2 × M3x12 bay ribs, −Y through the lid's Ø6 holes | 31 mm | **Ø0.0** | Ø1.5 → **0.7069 mm³ (`bay_lid` itself)** — see NB-2 |
| F7 | 4 × M3x8 bay-lid screws, −Y from y = −92.5 | 25 mm | **≥ Ø12.0** each | — |
| F8 | 6 × M3x10 flange screws, r = 74, θ = 15+60k, +Z | 25 mm | **≥ Ø12.0** each | — |
| F9 | 4 × M2x10 mount screws (±19, ±19), −Z | 30 mm | **Ø2.5** | Ø3.0 → 5.4104 (top_plate) |
| F10 | 4 × M2x6 sensor-cover ear screws, ±Y outboard | 25 mm | **Ø12.0** (upper ears) / **Ø5.0** (lower ears) | lower: Ø6.0 → 3.3686 (plate) |

Readings that matter:

- **F1 in situ = Ø0.0** — unchanged from round 1 and unchanged in kind: once the
  machine is together the four gearbox screws are buried under the disc, the
  bearing and the housing roof. The motor is fastenable and removable **only as
  the plate+motor cartridge**, where the corridor is Ø8.0. That is a legitimate
  build route (the quarter-turn latch exists precisely for it) but "the motor is
  not field-replaceable in place" must be written into the service section; it
  is not in `BUILD-NOTES-r2.md`.
- **F9 = Ø2.5 over 30 mm** for the four M2 screws that carry the whole payload —
  a bare 1.5 mm hex key, nothing with a handle.
- **F2 = Ø3.4** and the grub has to be pushed **43.00 mm** radially (housing
  outer face r = 52 → pilot r = 9) down a Ø3.4 channel, with the disc first
  indexed to θ = 202.5° so the flat, the pilot and the port line up. Both of
  those belong in the assembly procedure; neither is written down.

### 4. Non-blocking, measured

- **NB-1 — zero designed axial clearance at the shaft end.** Shaft top
  **Z = −337.250** (motor bbox max) and the disc bore's blind face
  **Z = −337.250** (axial ray up x = y = 0 through `pocket_disc` hits −337.25 and
  −320.25): **0.000 mm**. The PTFE thrust washer, which is supposed to be the
  disc's axial seat, has **0.050 mm** of gap (washer top −350.800, disc bottom
  −350.750). On any positive tolerance the shaft end, not the washer, sets the
  disc height, and the 1.500 mm roof clearance B8 depends on moves with it. Round
  1 measured 0.05 mm here; it has gone to zero.
- **NB-2 — the bay lid's rib-driver holes are closed by a 0.400 mm membrane.**
  A ray along +Y at (±14, −95, −337.10) hits `bay_lid` at **y = −89.000 and
  −88.600**: the Ø6 access hole is cut only to y = −89, while the register lip
  runs to y = −88.6. A Ø1.5 corridor reads **0.7069 mm³** of the lid's own
  material. `BUILD-NOTES-r2.md` §2.11 prints "2x rib driver paths through the
  lid's Dia6 holes total 0.00 mm3" — that check must have excluded the lid
  itself. Cut the hole through.
- **NB-3 — cartridge insertion needs the disc counter-indexed.** At the seat, an
  unlock angle of 20/22/24° reads **4.2552 / 4.6955 / 5.1242 mm³** against
  `pocket_disc` — the shaft D-flat against the disc D-bore flat at the wrong
  relative angle. It is 0.0000 with the disc pre-indexed by the same angle (the
  disc is free in the bearing), so this is a procedure item, not geometry, but
  the builder's A-2 table reports 0.0000 because it booleaned the cartridge
  against the **housing only**.
- **NB-4 — the service-stand clearance is measured against the wrong body.**
  `BUILD-NOTES-r2.md` §2.12 prints "lowest payload material −410.25 vs ground
  −426.45 → 16.20 mm of clearance". The lowest solid in the assembly is the
  **motor can at Z = −418.450**, giving **8.000 mm**, not 16.20. B12.1 still
  passes (`service_stand ^ motor = 0.0000`, `^ retaining_plate = 0.0000`), but
  the published number is not the minimum.
- **NB-5 — grub handling** (carried from round 1, unchanged): 43.00 mm of blind
  radial travel down a Ø3.4 channel, no retrieval path if the screw is dropped in
  the chamber, and a ≥ 60 mm 1.5 mm hex key is still not a BOM line.

### 5. What I need to see next round to clear "assembly"

1. `sensor_cover` with a **0.0000 mm³ swept-volume** insertion path from one
   named direction, printed per side (today: 488.4789 mm³ over 12 mm).
2. `fill_cap` removal: rotate-to-unlock **and** lift **and** lateral, each leg
   0.0000 mm³ against `top_plate` and `hopper`, with the required lift and
   lateral travel printed (today: 0.05 mm of free lift, 16.9480 mm³ at unlock,
   581.7683 mm³ swept over an 8 mm lift).
3. A **two-sided** free-rotation scan of the seated cartridge showing a bounded
   band (today 0 … +24°, open at the +θ end), plus a stated holding torque
   ≥ 0.6527 N·m from a modelled feature, not from friction.
4. The three procedure facts written into the build notes: motor is not
   field-replaceable in place (F1 = Ø0.0), the disc must be indexed to θ = 202.5°
   for the grub, and the disc must be counter-indexed to the unlock angle for
   cartridge insertion.
5. `bay_lid` Ø6 rib-driver holes cut through (today 0.7069 mm³ of the lid's own
   register lip), and the F6 corridor re-printed **including the lid**.
6. The shaft-end/bore-blind gap given a real value, and the service-stand
   clearance re-printed against the lowest solid in the assembly (8.000 mm).

Nothing above touches the torque path, which is the second round running that it
has measured clean.

## integration

**Owner:** integration / serviceability critic (Thomas directives 2, 3, 4;
punch-list **B5, B6, B11, B12**; RT-14).
**Measured on:** `cad/exports/dispenser_r8_assembly.step` (22 solids, exact OCC
booleans), the individual `*_r8.step`/`*_r8.stl` part exports, the vendor
`interface/mechanical/2112_attach_plate*.step`, and the landing gear rebuilt
from `quiver.airframe_structure.landing_gear.assembly.make_assembly()`.
venv `~/.openclaw/workspace/venvs/dock-cad-314`, build123d 0.11.1, trimesh
5.0.0. Every number below was produced by my own probes; nothing is copied from
`BUILD-NOTES-r2.md`. `[A]` marks an assumption I introduce.

**VERDICT: does not pass.** Four blocking findings, three of them created by
this round's own geometry. Directive 3 (reach-in) closes cleanly and is the
best-measured item in the round; directive 2 (electronics home) closes
structurally but the board cannot be got into the bay and the motor cable has
no route; directive 4 / RT-14 (refill) is **worse than r6** — the fill cap can
no longer be removed at all, because the directive-3 neck sits on top of it.

---

### 1. (a) Gloved-hand access corridor to the quick-release — **PASS**

**Corridor I require (all `[A]`, with justification, per B6.1's demand that the
number be argued against a hand dimension rather than asserted):**

| dimension | value | basis |
|---|---|---|
| width | **110 mm** | 95th-percentile male hand breadth across the metacarpals ≈ 97 mm (ANSUR/NASA-STD-3000-class data) + ~5 mm per side for a work glove = 107 mm, rounded up `[A]` |
| height | **45 mm** | 95th-percentile male hand thickness at the metacarpals ≈ 33 mm + glove and knuckle clearance `[A]` |
| depth | **130 mm** | payload half-width 78 mm + 52 mm so the wrist clears the body while the fingers are on the lever `[A]` |
| placement | top at the clip-plate underside **Z = −181.55**, inner face at **\|axis\| = 25.0 mm** | 25.0 mm is the measured clip-plate edge; the vendor release levers are gripped from outboard of it |
| criterion | 0.000 mm³ on **at least two opposing** sides | punch list B6.2 |

Closure for the `[A]` rows is one sentence from Thomas or a cardboard mock-up;
they are not facts.

**Measured (exact OCC boolean against all 21 payload solids, clip plate
excluded because it is the part being gripped):**

```
punch-list 95 x 45 x 130 and my 110 x 45 x 130, tops at Z=-181.55, inner face at |axis|=25.0
   W=95  +X:     0.0000 mm3  {}
   W=95  -X:     0.0000 mm3  {}
   W=95  +Y:     0.0000 mm3  {}
   W=95  -Y:   338.8337 mm3  {'top_plate': 338.834}
   W=110 +X:     0.0000 mm3  {}
   W=110 -X:     0.0000 mm3  {}
   W=110 +Y:     0.0000 mm3  {}
   W=110 -Y:   338.8337 mm3  {'top_plate': 338.834}
```

Widening the corridor from the punch list's 95 mm to my 110 mm costs nothing:
three of four sides are 0.0000 mm³ either way, including the opposing pair
±X, which is the pair the vendor levers are on.

**Free height available (bisection to 0.01 mm, 110 mm wide × 130 mm deep):**

```
   +X: max clear height = 52.00 mm ; first obstruction at Z = -233.55 -> {'top_plate': 4987.802, 'fill_cap': 13.521}
   -X: max clear height = 52.00 mm ; first obstruction at Z = -233.55 -> {'top_plate': 4987.802, 'fill_cap': 13.521}
   +Y: max clear height = 49.50 mm ; first obstruction at Z = -231.05 -> {'fill_cap': 188.199}
   -Y: max clear height = 43.50 mm ; first obstruction at Z = -225.05 -> {'top_plate': 180.0}
```

**Stand-off and neck, measured independently of the build:**

```
first material outside |x|,|y| <= 24.5 at Z -225.05..-225.55: 90.000 mm3   -> stand-off h = 43.500 mm
material OUTSIDE |x|,|y| <= 24 mm in the 45 mm band: 340.224 mm3  (all of it the -Y conduit + strain-relief boss)
material OUTSIDE |x|,|y| <= 23 mm in the 45 mm band: 8800.224 mm3         -> neck plan half-extent a = 24.000 mm
payload material above Z = -171.05: 0.000000 mm3 ; above Z = -171.00: 0.000000 mm3
```

h = **43.500 mm**, a = **24.000 mm** — both reproduce the build's figures.

**The vendor release mechanism, measured from `2112_attach_plate.step`** (this
is the thing the hand has to work, and no round has dimensioned it before):
the aircraft-side half is a 50 × 50 × 16 mm body carrying **two levers each
15.0 × 13.0 × 12.5 mm spanning \|x\| = 18.0…33.0 mm**, i.e. standing **8.0 mm
proud of the 50 mm plate on each side**. They are squeezed inward from
outboard. Payload material inside a grip envelope \|x\| 25…48, \|y\| ≤ 16.5,
45 mm deep, under the clip plate: **0.0000 mm³ on both sides**.

One honest limit: the same envelope started at \|x\| = 18.0 (the inboard end of
the lever) contains **4590.3000 mm³** of `top_plate` — the neck is a 48 × 48
column and the clip plate is 50 × 50, so there is only **1.0 mm** of undercut
at the plate edge. The operator's fingers must close on the **outer 9 mm** of
each lever; they cannot hook under the plate edge. That is acceptable for a
squeeze-release but it should be stated, not left implied by "43.5 mm of hand
space".

---

### 2. (b) Electronics bay — **structurally sound, two blocking defects**

**Interior recovered from the export by ray probing from inside the cavity
(not from the source):**

```
   +x:  23.000 mm -> wall at (  23.000, -75.000,-336.100)
   -x:  23.000 mm -> wall at ( -23.000, -75.000,-336.100)
   +y:  11.000 mm -> wall at (   0.000, -64.000,-336.100)   (inboard wall)
   -y: no hit                                               (open: the lid aperture)
   +z:  18.000 mm -> wall at (   0.000, -75.000,-318.100)
   -z:  20.000 mm -> wall at (   0.000, -75.000,-356.100)
```

Interior = **46.000 × 22.000 × 38.000 mm centred at (0, −75.0, −337.1)**,
exactly the `ELECTRONICS.md` §7 envelope. Four ECO-7 standoffs measured at
x = ±18.000, z = −323.100 / −351.100, free face **y = −69.000**, 5.000 mm tall.

**Board fit, 42 × 34 × 12 mm seated on those standoffs** (grow-the-envelope
probe, 0.1 mm steps):

```
     +x           clearance = 2.0 mm
     -x           clearance = 2.0 mm
     +z(up)       clearance = 1.0 mm      <- limited by the riser-socket boss, not the wall
     -z(down)     clearance = 2.0 mm
     +y inboard   clearance = 0.0 mm      <- seated on the standoff faces, by definition
     -y outboard  clearance = 5.0 mm
```

The material inside the true cavity is only the four standoffs (89.214 mm³
each) and **1.00 mm of the riser-socket boss** protruding at z −319.10…−318.10.
B5.1 asks for ≥ 1.5 mm to every interior wall: the walls give 2.0 mm, the riser
boss gives **1.00 mm**. Minor, but it is a miss and the build notes do not
mention it (they report a *best-fit floating* board centre `(-76.50, -338.85)`
rather than the seated position; seated is what I measured and it also fits).

**BLOCKING B5-a — the control board cannot be got into the bay.** The bay is a
closed box whose only opening is the lid aperture in the outboard wall.
Bisected to 45 iterations on `electronics_bay_r8.stl`:

```
   clear aperture WIDTH  = 42.0000 mm   (main board 42.00 mm -> clearance -0.0000 mm)
   clear aperture HEIGHT = 36.0000 mm   (main board 34.00 mm -> clearance  2.0000 mm)
```

**0.0000 mm of clearance on the 42 mm dimension.** A 42.0 mm PCB (±0.15 mm
routing tolerance) cannot pass a 42.0 mm printed aperture (FDM ±0.2 mm class,
and printed *smaller* on an internal feature). The bay houses a board it cannot
be given. Fix is trivial (aperture 42 → 45 mm, or board 42 → 40 mm) but it must
be a geometry change, not a note: directive 2 asked for a place for the
electronics.

**Gasket (B5.3) — real geometry, passes.** Sealing face measured at
y = −90.000; groove floor at y = −88.800 → **depth 1.200 mm**; the groove is
present on all four runs (top z = −317.60, bottom z = −356.60, ±x at x = ±23.0);
scanned across the top run it spans z −318.4…−316.8 → **width 1.600 mm**;
centreline half-extents 23.0 × 19.5 → closed-loop **perimeter 170.0 mm**.
B5.3 asks ≥ 1.5 × ≥ 1.0 — passes.

**Three ECO-6 entries — present, with lands.** Riser socket bore
**Ø7.400** (land 1.50 mm); the two inboard entries **Ø6.000 through** with
**Ø10.000 × 3.2 counterbores** → **2.00 mm** grommet land. A +y ray on either
inboard entry axis exits the bay with no crossings at all, which confirms both
are through-holes.

**Wiring channel cross-sections** (720-ray casts from each channel axis on the
exports; areas by 0.5·Σr²Δθ):

```
  neck interior at z=-200 (top_plate)                  area  1831.89 mm2  equiv dia  48.30 mm
  top-plate conduit horizontal leg at y=-30/-50/-70    area    28.26 mm2  equiv dia   6.00 mm
  top-plate conduit vertical spigot at z=-242/-246     area    28.26 mm2  equiv dia   6.00 mm
  hopper -Y conduit at z=-250/-270/-290/-305           area    95.00 mm2  equiv dia  11.00 mm
  bay riser socket bore at z=-314/-317                 area    42.99 mm2  equiv dia   7.40 mm
  bay +Y entry counterbore (x=+/-10)                   area    78.51 mm2  equiv dia  10.00 mm
  sensor duct vertical leg (x=48, |y|=32.5)            area    19.63 mm2  equiv dia   5.00 mm
  sensor-cover grommet port (x=41, |y|=26)             area    19.63 mm2  equiv dia   5.00 mm
```

Governing section on the aircraft-harness route is the **Ø6.00 top-plate
conduit, 28.26 mm²**. Nine 26 AWG PTFE conductors at OD 1.05 mm = 7.79 mm² →
**27.6 % fill** (B5.5 allows ≤ 70 %; this supersedes `ELECTRONICS.md` §6.3's
62 % in a 12.5 mm² channel, which no longer exists). Six-way sensor cable
5.20 mm² in 19.63 mm² = **26.5 %**.

**No wiring in the granule space — the aircraft leg genuinely clears it.**
Measured, not assumed:

```
  hopper cylindrical wall, rays from the tank axis:  inner r = 69.978, outer r = 72.278 (wall 2.300 mm)
  -Y conduit bore, inboard generator at x=0:         y = -75.502   (3.224 mm outboard of the tank OUTER wall)
  ray from (0,-75.4,z) towards the axis, z=-250..-270: first material at 5.422 mm  -> 5.42 mm of CONTINUOUS
                                                       material (web + tank wall) between bore and tank
  top plate under the neck and under the conduit:     solid Z -238.550 .. -233.550 (5.000 mm), every probe
```

**BLOCKING B5-b — the tank is not dust-tight to the harness cavity, and the
fill cap's only seal is cut through.** The two bayonet notches are
8.5 × 4.5 mm slots cut through the full 5 mm plate at (0, 20.55) and
(0, 69.45). At the O-ring gland plane:

```
   bore radius at the O-ring gland plane z=-237.35: nominal 23.000, measured min 22.993 max 27.033
   angular sectors where the sealing bore is NOT at r=23.00: [(79.5, 100.5, 21.0), (259.5, 280.5, 21.0)]
   total non-sealing arc: 42.0 deg of 360
```

A 1.5 mm cord cannot seal across a 4.5 mm-wide open slot, so **42.0° of the
fill-cap seal does not exist**. And the −Y notch does not vent to atmosphere —
it vents into the harness neck:

```
   rays UP from inside the tank (z=-245), top_plate alone vs top_plate + fitted cap:
   ( 0.00, 19.00)  top_plate alone: [-188.05, -181.55]   with cap: [-236.695, -234.195, -188.05, -181.55]
   ( 0.00, 20.55)  top_plate alone: [-188.05, -181.55]   with cap: [-236.695, -234.195, -188.05, -181.55]
   ( 0.00, 22.00)  top_plate alone: [-232.55, -181.55]   with cap: [-236.695, -234.195, -232.55, -181.55]
   ( 0.00, 69.45)  top_plate alone: []                   with cap: [-236.695, -234.195]
```

Read the first column: **over the −Y notch the plate has no material at all**
between the tank and the neck cap at Z = −188.05. The only barrier in the
assembled state is the 2.5 mm cap flange (material −236.695…−234.195), which is
a free-floating disc with **0.50 mm radial** clearance in its Ø56.000 recess and
**0.05 mm** under its face, sitting *outside* the (already broken) O-ring. The
+Y notch does the same thing to atmosphere. This is directive 2's concern in
reverse: friable herbicide dust has a modelled path out of the tank, past the
only seal, into the cavity that carries the aircraft harness to the bay.

**BLOCKING B5-c — the bay→motor cable has no modelled route.** Directive 2
names "bay to motor" explicitly; B5.5 asks for ≥ 90 % covered.

```
   count-sensor: duct exit (0,-52,-363.25) -> bay entry (-10,-62,-350.10) = 19.31 mm of free air
   motor: bay entry (10,-62,-350.10) -> nearest point of the stepper envelope (10,-18,-350.10) = 44.00 mm
   motor: bay entry -> the stepper's REAR lead exit (0,0,-418.45) [A, NEMA-14 leads exit the rear] = 92.82 mm
   material in the corridor between them: meter_housing 114.4 mm3, pocket_disc 188.0 mm3,
                                          retaining_plate 94.3 mm3   (i.e. NO conduit; and a straight
                                          run would pass through the metering chamber)
```

Motor leg coverage is **0 %**; total uncovered length is **≥ 63 mm** (19.31 +
44.00) and plausibly ~112 mm. The build notes list the 20 mm sensor service
loop honestly but do not mention the motor cable at all.

---

### 3. (c) Refill workflow / RT-14 — **BLOCKING: the fill cap cannot be opened**

**Port and fill line — pass.** Clear bore **Ø46.000** at (0, 45) (B12.3 asks
≥ Ø46), recess **Ø56.000**; port bottom edge Z = −238.550, i.e. **35.85 mm**
above the 250-pellet line (−274.4) and 10.45 mm above the 421 line (−249.0).

**Rest position — pass, with a corrected number.** `service_stand_r8`:

```
service_stand bbox X[-90.00,90.00] Y[-90.00,90.00] Z[-426.45,-358.25] vol 103.91 cm3
foot (ground) plane Z = -426.45 ; base outline convex hull r = 90.00, contact section area 7301.1 mm2
lowest FLIGHT solid Z = -418.45 (the stepper) -> clearance to the ground plane = 8.00 mm
CG (empty, my own rebuild of the modelled flight solids) = (1.63, -2.82, -326.79); 99.66 mm above the foot
minimum CG-to-tip-edge distance = 86.72 mm  ->  TIP ANGLE = 41.03 deg   (B12.1 [A] asks >= 25 deg)
loaded CG ~ (1.26, -2.19, -318.55) [A: 250-pellet column CG at Z=-290]  ->  TIP ANGLE = 39.02 deg
```

Tip angle 41.03° empty / 39.02° loaded, load path on printed structure at
r = 52 — B12.1 passes comfortably. **But `BUILD-NOTES-r2` §2.12 prints
"lowest payload material −410.25 vs ground −426.45 → 16.20 mm of clearance".
−410.25 is the retaining plate. The lowest flight solid is the stepper at
−418.450, so the real figure is 8.00 mm** — measured to the very part B12.1
exists to keep off the ground. (The assembly critic reached 8.000 mm
independently this round.) The clearance is still positive; the printed number
is wrong by 2×.

**BLOCKING B12-a — with the stand-off neck fitted, the fill cap has nowhere to
go.** The neck's +Y wall sits on the plate top face:

```
   (x=  5.0,y= 22.0): top_plate surface Z crossings above -240: [-238.55, -236.745, -233.545, -181.55]
   (x= 15.0,y= 23.0): top_plate surface Z crossings above -240: [-238.55, -236.745, -233.545, -181.55]
   (x= 18.0,y= 23.9): top_plate surface Z crossings above -240: [-238.55, -236.745, -233.545, -181.55]
```

i.e. continuous neck material from **Z = −233.545 up to −181.55** over
y = 21.4…24.0, \|x\| ≤ 24 — directly above the cap, whose flange top face is at
**Z = −234.20**. The cap flange (r 27.5 about (0,45)) reaches y = 17.5, so it
lives **6.5 mm underneath the neck wall in plan**. Lift sweep, 0.4 mm voxel
sample of the cap's −Y sliver against material above the plate top face:

```
   lift  0.50 mm: no sliver material above the plate top face yet
   lift  1.00 mm: inside neck material:   636 pts (  40.7 mm3)
   lift  2.00 mm: inside neck material:  1620 pts ( 103.7 mm3)
   lift  3.15 mm: inside neck material:  3096 pts ( 198.1 mm3)
   lift  6.45 mm: inside neck material:  4269 pts ( 273.2 mm3)
```

- **maximum clear vertical lift = 0.65 mm** (contact at −233.55 = plate top).
- lift needed to free the flange from its Ø56 recess = **3.15 mm**.
- lift needed to bring the bayonet lugs up through the plate notches =
  **6.45 mm**.
- the cap cannot translate while its flange is in the recess (0.5 mm radial
  clearance), and no (lift ≤ 6.45, +Y ≤ 40 mm) combination is clear — at
  lift 3.15 mm sliding +Y makes it worse (273 → 696 sample points at dy = 6.5).
  Only at lift ≥ 6.45 mm **and** dy ≥ 6 mm does the count reach 0, and the cap
  cannot reach that lift.

So the shipped refill workflow is: quick-release the whole dispenser (directive
4), stand it on its stand (which works), and then **fail to open it**. RT-14 is
not closed; it has been converted from "awkward" to "impossible". The r6
complaint was 6.45 mm of lift in a 10.5 mm gap; the r8 geometry gives 6.45 mm
of required lift in a **0.65 mm** gap. Directive 3's neck ate directive 4's
workflow, and no check in `verify_r2.py` looks at the cap.

Cheap fixes, in order of disruption: move `FILL_POS` outboard (the port centre
needs y ≥ 24 + 27.5 = **51.5 mm** for the flange to clear the neck footprint in
plan, against a tank inner radius of 69.978 and a port radius of 23.0 — it
does not fit, so this alone is not enough); or relieve the neck's +Y face above
the cap; or make the cap a low-profile screw plug removed without axial lift.
This needs geometry, not wording.

---

### 4. (d) Ground clearance and envelope — **PASS**

Landing gear rebuilt from the quiver source (not from a cached number):

```
LANDING GEAR built from quiver source: bbox X[-293.57,293.57] Y[-250.00,250.00] Z[-547.89,-124.94]
  lowest gear point (ground contact) Z = -547.890
PAYLOAD assembly bbox X[-78.00,78.00] Y[-92.00,78.00] Z[-418.450,-171.050]
  GROUND CLEARANCE (payload bottom - lowest gear point) = 129.440 mm  (requirement >= 40 mm)
  stack below the mounting plane (Z=-171.0): 247.45 mm
  PAYLOAD <-> LANDING GEAR minimum separation (mesh-to-mesh, 327243 gear pts, exact
    point-to-triangle refine) = 103.628 mm ; closest payload point [-60.86, -48.79, -233.55]
```

**129.440 mm** of ground clearance = 3.24× the ≥ 40 mm requirement;
**103.628 mm** payload↔gear separation. Both reproduce `BUILD-NOTES-r2` §2.10
exactly, which is the first time this round a headline number has survived an
independent rebuild unchanged. Envelope: Ø156 in X, **170.0 mm in Y** (the bay
lid reaches y = −92.0 while the body stops at +78.0 — the payload is
asymmetric in Y and that is worth stating in the README), 247.45 mm of stack
below the mount plane. Payload material above the ICD plane: **0.000000 mm³**
above both Z = −171.05 and Z = −171.00. Prop clearance I did not re-derive —
the rotor geometry is not in the exports I was given; it stays the interference
critic's number.

---

### 5. (e) Mass ledger, rebuilt from the exports — **dry target passes; the loaded reading depends on a basis this round changed**

Rebuilt from the 22 exact solid volumes in `dispenser_r8_assembly.step` at
CF-PETG **1.27 g/cm³** (TPU 1.20, PMMA 1.19, alu 2.70, PTFE 2.20, nylon 1.14),
stepper carried at **350 g** per B11.3:

```
solid                      vol cm3      basis   mass g   centroid (x,y,z)
hopper                     108.849    petg_cf    138.2   (  -0.03,  -3.55, -273.29)
meter_housing              103.672    petg_cf    131.7   (   5.78,   0.50, -339.15)
top_plate                   96.200    petg_cf    122.2   (  -0.05,  -4.38, -223.49)
pocket_disc                 72.728    petg_cf     92.4   (   0.11,   0.05, -342.89)
stepper                     69.936  [assumed]    350.0   (   0.00,   0.00, -387.40)
retaining_plate_chute       57.995    petg_cf     73.7   (  13.43,   0.39, -368.49)
electronics_bay             19.299    petg_cf     24.5   (  -0.00, -73.93, -336.41)
clip_plate                  11.523        alu     31.1   (   0.00,  -0.00, -178.13)
fill_cap                    11.132       petg     14.1   (  -0.02,  45.00, -236.45)
bay_lid                      7.610    petg_cf      9.7   (  -0.00, -90.55, -337.10)
agitator                     4.291        tpu      5.1   (  -0.00,   0.00, -322.71)
brush_holder                 3.544    petg_cf      4.5   ( -32.37,  21.67, -330.60)
sensor_cover(+Y)             1.690    petg_cf      2.1   (  34.35,  25.49, -394.99)
sensor_cover(-Y)             1.690    petg_cf      2.1   (  34.35, -25.49, -394.99)
sleeve_bearing               1.495      nylon      1.7   (   0.00,   0.00, -329.09)
blindmate_pcb                1.174  [assumed]     15.0   (   0.00,  -2.86, -183.92)
thrust_washer                0.317       ptfe      0.7   (   0.00,   0.00, -351.50)
brush_strip                  0.312  [assumed]      3.0   ( -31.27,  13.17, -331.86)
count_window x4              0.104       pmma      0.1   (  +/-29/35, +/-11.47, -392/-398)
SUBTOTAL modelled solids                        1022.0
  + electronics (STM32G431+TCAN332, TMC2209, D36V6F5, count chain, 2x DRV5032)   65.0 g  [J]
  + fasteners (M3/M2.5, 6x heat-set, 3x plastite, lid + mount screws, plunger)   57.0 g  [J]
  + O-ring + gaskets + 9x Dia3x2 magnets                                          8.0 g  [J]

  EMPTY TOTAL (my rebuild)                   1152.0 g
  contingency 10%                             115.2 g
  EMPTY carried                              1267.2 g
  LOADED @250 (1.18 g/pellet)              1562.2 g   margin vs 1500 =   -62.2 g
  LOADED @421 (1.18 g/pellet)              1764.0 g   margin vs 1500 =  -264.0 g
  CG of the modelled flight solids (empty)  (1.63, -2.82, -326.79)
```

This reproduces the build's ledger to **0.1 g**, so the arithmetic is not in
dispute. What is in dispute is which line the ≤ 1500 g rule applies to:

- `_run/rev1/CONTEXT.md` says **"Structure mass target ≤ 1500 g dry"**. On that
  reading the shipped design is **1267.2 g dry (1152.0 g before contingency) —
  a pass with 232.8 g of margin**, and there is nothing to argue about.
- Punch list **B11.2** re-reads the same rule as `LOADED @250 ≤ 1500 g`, which
  on the 100 %-infill basis is **1562.2 g, 62.2 g over**, and which the round
  then rescued by switching the shipped headline to a slicer-realistic basis.

I can independently confirm the slicer bracket is at least not optimistic. My
own voxel EDT (padded, 4 × 0.4 mm shell, 25 % infill, pitch 0.5 mm on the big
parts / 0.3–0.4 mm on the small ones):

```
  top_plate              solid  122.1 g  core  23.34 cm3 (24.3%)  sliced   99.9 g
  hopper                 solid  138.2 g  core  13.77 cm3 (12.6%)  sliced  125.1 g
  meter_housing          solid  131.6 g  core  60.09 cm3 (58.0%)  sliced   74.4 g
  pocket_disc            solid   92.3 g  core  46.16 cm3 (63.5%)  sliced   48.4 g
  retaining_plate_chute  solid   73.6 g  core  12.84 cm3 (22.1%)  sliced   61.4 g
  electronics_bay        solid   24.5 g  core   1.10 cm3 ( 5.7%)  sliced   23.5 g
  bay_lid                solid    9.7 g  core   1.19 cm3 (15.7%)  sliced    8.5 g
  fill_cap               solid   14.1 g  core   4.07 cm3 (36.6%)  sliced   10.3 g
  agitator               solid    5.1 g  core   0.84 cm3 (19.6%)  sliced    4.4 g
  brush_holder           solid    4.5 g  core   0.57 cm3 (16.0%)  sliced    4.0 g
  TOTAL printed: solid 615.9 g -> sliced 459.8 g (delta 156.1 g).
  BUILD-NOTES-r2 prints solid 615.9 -> sliced 483.9 (delta 132.1).
```

My delta is **24 g larger** than theirs, i.e. their sliced headline is the
conservative one; on my numbers LOADED @250 on the slicer basis is
**1390.5 g** against their 1416.9 g. Two caveats, both mine:

1. The bracket is strongly pitch-sensitive. At 0.9 mm pitch the same code reads
   a 307.8 g delta. Only the 100 %-infill ledger reproduces exactly; the
   slicer figure is method-dependent to ±25 g at best.
2. **The N13 control does not reproduce.** `BUILD-NOTES-r2` §2.15 prints
   "bay_lid … hollow core = 0.0 % of volume". I measure **13.9 % at 0.3 mm
   pitch and 15.7 % at 0.5 mm** — the lid is not a uniform 3.2 mm plate (its
   flange band is 3.4 mm and it carries a register lip and four screw bosses),
   so 0.0 % is the wrong answer for the wrong reason and the control does not
   actually control anything.

Recommendation for the run owner, not for me to decide: get Thomas to say
whether ≤ 1500 g is dry or loaded. On his own wording it is dry and the design
passes; B11.2's stricter reading is the punch list's invention.

---

### 6. Smaller measured items

- **Assembly STL export integrity.** `dispenser_r8_assembly.stl` is
  `watertight=False`. Split with repair off: **162 connected components — 22
  real bodies (matching the build's claim) plus 140 with \|volume\| ≤ 1e-6 mm³**,
  degenerate face strips at y = ±25.000, x 40.81…47.00, z ≈ −409.75 (on
  `sensor_cover`). Three of the 22 real bodies —
  `retaining_plate_chute` (57.980 cm³) and both `sensor_cover` halves
  (1.690 cm³ each) — are **non-watertight in the assembly STL** although the
  same parts export watertight standalone. B10 as written (part STLs + no
  inverted-normal bodies) still passes; but the assembly STL is not safe for
  volumetric booleans, which is why every number above was taken from the
  STEP.
- **−Y corridor 338.8337 mm³** is the covered harness conduit and its
  strain-relief boss. Deliberate, on the side the aircraft harness must leave
  from, and the opposing ±X pair is clear — I accept it.
- **Riser boss** costs 0.5 mm of the punch list's 1.5 mm board-to-wall
  clearance at the top-outboard corner (1.00 mm measured). Non-blocking.

---

### 7. What has to change before I can pass this

1. **Lid aperture 42.000 → ≥ 45 mm** (or board 42 → 40 mm). Print the measured
   clearance.
2. **Fill-cap extraction.** Any geometry that gives a removable cap on the
   stand: relieve the neck's +Y face over the cap footprint, or replace the
   bayonet with a zero-lift closure. Acceptance: a rigid-body extraction path
   with 0.000 mm³ of interference, printed as a sweep table, plus the same
   sweep with the payload on the service stand.
3. **Seal the bayonet notches** (lug pockets closed at the top, or a gland that
   is not interrupted). Acceptance: the sealing bore continuous over 360.0° at
   the gland plane, and 0 rays from the tank reaching the neck cavity.
4. **Model the bay→motor cable route** (and the sensor service loop), or state
   the uncovered length in the README as a deliberate exposed run. Acceptance:
   B5.5's covered fraction printed with the actual numbers, motor leg included.
5. Correct §2.12's 16.20 mm to the measured **8.00 mm**.
