# REV-1 ROUND 4 — CRITIQUES

## granule-path

**Verdict: PASS with complaints — 0 blockers, 1 MAJOR, 2 MODERATE, 2 MINOR.
The rev-0 fragment-jam mandate is NOT regressed:** every geometric term of it
(overfill relief before the housing arc at full roof section, nose gap = roof
clearance = 1.500 mm, compliant-element-first contact order, shear-margin
backstop, pocket/chamfer geometry) re-measures on the r10 exports to ≤ 0.002 mm
of the r9 values, and stall-recovery motion is rotationally unobstructed
(0 penetrations at every sampled angle, agitator and disc). Round-3's BLOCKER
(export integrity on `retaining_plate_chute`) is **closed and independently
verified**. The MAJOR is new geometry this round: the plug-tether anchor lug
protrudes into the drop tube and into the fitted plug, and the model's own log
line calls the whole 206.0993 mm³ of that interference "the designed 0.3 mm
press fit" when only 83.504 mm³ of it is.

### Provenance

- Measured by me on `cad/exports/*_r10.stl` / `*_r10.step` with
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`, trimesh 5.0.0,
  numpy 2.5.1, build123d 0.11.1 (OCC booleans; trimesh has no boolean backend
  in this venv). Nothing is imported from `dispenser.py`; the only file of the
  model I read was to *name* a feature I had already measured (`TETH_X0 = 42.0`).
- md5 of the files I measured, matching `BUILD-NOTES-r4.md` §0:
  `retaining_plate_chute_r10.stl 6bb3fd144fda0f2c6cb69f3222534e33`,
  `meter_housing_r10.stl c3cbffb49753ba595dd63afb0c192db0`,
  `brush_holder_r10.stl ad2343fea8807cf4a998596e939e7308`,
  `chute_plug_r10.stl 52246a7a59f8dff1b3f84f29003f4108`;
  `pocket_disc_r10.stl d02b663b6ae5cc8086ebb3a76288762e` (not listed in §0).
- Z-stack re-measured on the exports (unchanged from r9): housing roof top
  **−326.250**, roof underside **−335.250** (9.000 mm section), **disc top
  −336.750**, disc bottom −350.750, plate top **−351.250**, port bore
  −352.000…−354.250, chute bore −354.5 → −405.25.

### Round-3 blocker: export integrity — CLOSED, verified

Independent census (vertices merged, trimesh default processing):

```
== MESH CENSUS r10 (independent) ==
agitator_r10.stl                 wt=True  wind=True  euler=     2 bodies=  1 vol_cm3=    4.288 inv=0 mult={2: 4086}
bay_lid_r10.stl                  wt=True  wind=True  euler=   -10 bodies=  1 vol_cm3=    8.598 inv=0 mult={2: 4614}
brush_holder_r10.stl             wt=True  wind=True  euler=     0 bodies=  1 vol_cm3=    3.544 inv=0 mult={2: 918}
chute_plug_r10.stl               wt=True  wind=True  euler=    -2 bodies=  1 vol_cm3=    6.874 inv=0 mult={2: 3819}
count_windows_r10.stl            wt=True  wind=True  euler=     8 bodies=  4 vol_cm3=    0.104 inv=0 mult={2: 3000}
dispenser_r10_assembly.stl       wt=True  wind=True  euler=  -167 bodies= 24 vol_cm3=  587.685 inv=0 mult={2: 191100}
electronics_bay_r10.stl          wt=True  wind=True  euler=    -8 bodies=  1 vol_cm3=   21.175 inv=0 mult={2: 15027}
fill_cap_r10.stl                 wt=True  wind=True  euler=     0 bodies=  1 vol_cm3=    7.347 inv=0 mult={2: 5325}
hopper_r10.stl                   wt=True  wind=True  euler=   -14 bodies=  1 vol_cm3=  109.423 inv=0 mult={2: 16992}
meter_housing_r10.stl            wt=True  wind=True  euler=   -12 bodies=  1 vol_cm3=  103.623 inv=0 mult={2: 17463}
pocket_disc_r10.stl              wt=True  wind=True  euler=   -30 bodies=  1 vol_cm3=   72.661 inv=0 mult={2: 36963}
retaining_plate_chute_r10.stl    wt=True  wind=True  euler=   -48 bodies=  1 vol_cm3=   71.886 inv=0 mult={2: 40974}
sensor_boards_r10.stl            wt=True  wind=True  euler=     4 bodies=  2 vol_cm3=    1.287 inv=0 mult={2: 3108}
sensor_cover_r10.stl             wt=True  wind=True  euler=    -4 bodies=  2 vol_cm3=    3.234 inv=0 mult={2: 3540}
service_stand_r10.stl            wt=True  wind=True  euler=     0 bodies=  1 vol_cm3=  103.892 inv=0 mult={2: 1656}
top_plate_r10.stl                wt=True  wind=True  euler=   -36 bodies=  1 vol_cm3=   95.755 inv=0 mult={2: 19812}
```

15/15 part STLs watertight, **0 open edges, 0 non-manifold edges, 0
inverted-normal bodies anywhere** (r9: `retaining_plate_chute` 188 open + 1538
three-face edges, 21 shells; `chute_plug` a −3930.3 mm³ inverted body). The
assembly is 24 bodies for 24 solids, watertight. Every `0.000 mm³` boolean in
this round is therefore computed on valid shells — which was the condition I set
at the end of round 3, and it is met.

**Caveat on what that census can and cannot see (relevant to the MAJOR below):**
the assembly census reads `{2: 191100}` — i.e. *no* coincident-face contact at
all between 24 parts that are supposed to seat on each other — and it did not
and cannot detect solid-solid *interpenetration*, which is what I found with an
OCC boolean.

### The full journey, hopper → pocket → exit, with every pinch point vs the Ø13 worst case

| # | station | measured on r10 | vs Ø13 worst-case granule |
|---|---|---|---|
| 1 | fill route (cap off), axis (0.00, 43.45) | Ø13 sphere dropped on that axis from z −245 to −320 in 1 mm steps: **0 obstructed stations** against `top_plate` + `hopper` | clear |
| 2 | hopper barrel | inner **r 69.978–70.000** at z −260…−270 | 10.8 × D_max |
| 3 | funnel | r 69.978 @ −270 → 67.94 @ −275 → 58.04 @ −300 → **47.99 @ −325**; slope atan(55/22) = **68.2°** from horizontal, no step at any probe | continuous |
| 4 | sump outlet (annular window) | edges bisected to 1e-3°: **θ 130.000 → 250.000 = 120.000°** at every radius; radial **r 20.050 → 47.000 = 27.00 mm** (transitions measured at θ = 190) | **27.00/13.0 = 2.077**; equivalent circular orifice **D 49.11 mm** (area 1894.4 mm²). Below every no-arch criterion for a slot (≥ 3×) — **N10 plateau, unchanged** |
| 5 | deflector nose (rigid) | underside **1.500 mm** above the disc top at r = 22.0/26/30/34/38/42/46.5, and also at r = **20.5, 21.0, 21.5, 47.0**; flat spans θ 130.40…158.45 at r 22, 133.00…154.75 at r 34, 137.10…152.90 at r 46.5 | B8.1 holds at every radius; nose covers **r 20.5…47.0** |
| 6 | bristles (compliant) | assembly body 19: 312.2 mm³, z **−335.550…−328.160** → tip **+1.200 mm** above the disc top | leads the rigid nose (1.500) ✔ |
| 7 | entry ramp (overfill relief) | ceiling 10.500 @ θ130 (= the full 9.000 roof section + 1.500 gap, i.e. **no step at the mouth**) → 10.240 @129 → 7.896 @120 → 3.989 @105 → 1.645 @96 → **1.500 @ ≤95**, matched at r = 20.5/24.5/32/39.5/45.5/46.5 to ≤ 0.06 mm | ordering correct: last fill opportunity is the window edge θ = 130.000, the ramp runs 130 → 95, nothing enters the covered arc unramped |
| 8 | transfer arc | roof underside **1.500 mm** above the disc at every probe r = 20.5/24.5/32/39.5/45.5/46.5 × θ = 95, 90, 80, 60, 45, 30, 20, 10, 0, 350, 330, 320, 313, **311, 310, 309**, 305, 300, 290, 270 | crown of a seated granule is 1.500 **below** the disc top → 3.000 mm clear |
| 9 | pocket | bore **r 7.498–7.500** from depth 2.00 to 13.50; 45° chamfer r **9.497@0.00, 9.297@0.20, 8.992@0.50, 8.489@1.00, 7.992@1.50, 7.498@2.00** | 2.00 mm diametral clearance; seated centre 8.000 below the disc top |
| 10 | exit port | bore **r 7.998–8.000** (z −352.000…−354.250), 0.75 × 45° chamfer (r 8.697 @ −351.30, 8.390 @ −351.60), **first material at the plate top r = 8.746–8.749 (mean 8.747)** over 180 azimuths | 3.00 mm diametral clearance |
| 11 | chute | **r 10.993–11.000 continuous z −354.5 → −397.9** with `count_windows` + `sensor_cover` + `sensor_boards` merged; then **r_min 10.000 over z −398.000…−404.000** (see MAJOR), then 10.997 to the mouth −405.25 | Ø13 on the axis: 0 interference. Off-axis envelope drops from ±4.500 mm to **+3.500/−4.500 mm** in the lug band |

**Seated-granule transit (B8.5).** Ø13 sphere, centre −344.750 (crown 1.500 below
the disc top), carried round the PCD:

```
   vs meter_housing         min surface distance from granule centre    9.500 mm -> clearance   +3.000 mm; centre-inside stations 0/720
   vs brush_holder          min surface distance from granule centre    9.500 mm -> clearance   +3.000 mm; centre-inside stations 0/720
   vs hopper                min surface distance from granule centre   22.722 mm -> clearance  +16.222 mm; centre-inside stations 0/720
   vs agitator              min surface distance from granule centre   19.050 mm -> clearance  +12.550 mm; centre-inside stations 0/720
   vs retaining_plate_chute min surface distance from granule centre    6.500 mm -> clearance   +0.000 mm; centre-inside stations 0/720   (the granule resting ON the plate, tangent)
   642-vertex sphere containment, 180 stations at 2 deg: 0/180 for all five parts
```

**B1 roof section** (probe down from the roof top −326.250, 120 probes at
θ = 300/305/308/309/310/311/313/316/320/330/350/0/20/45/90 × r = 20.5/24.5/30/
32/36/39.5/44/46.5): **9.000 mm at every one of the 120 probes**, worst 9.000 at
θ = 300, r = 20.5 (the r4 checker prints 8.950 there; my probe reads 9.000 —
either way B1's ≥ 6.0 mm holds, and r6's 0.000 mm slot at θ = 310 is gone).

### Adversarial fragment construction — re-derived from scratch on r10

Inputs all measured above. **σ = 0.36 MPa and µ = 0.4 are carried ASSUMPTIONS**
(US4172714-derived; closure is the IFDC S-115 bench test). Drive re-derived from
the BOM motor: 0.14 N·m × 5.18 × 0.90 = 0.6527 N·m ÷ 0.032 m = **20.4 N at the
pocket lip in recovery, 12.2 N at the 60 % normal-metering current**.

**(a) Fragment nested in the pocket chamfer on a seated granule** — solved from
the measured 45° chamfer (r = 9.4985 at depth 0) and the measured 8.000 mm seat:

```
 d_frag   D13 centred  D13 seat+1.00  D13 seat-1.00  D12 centred  D12 seat+1.50
  D 4.0     +0.638       +1.061        +0.173        +0.283       +0.892
  D 4.5     +1.221       +1.632        +0.769        +0.864       +1.454
  D 5.0     +1.800       +2.199        +1.361        +1.442       +2.013
  D 5.5     +2.376       +2.763        +1.949        +2.016       +2.569
  D 6.0     +2.948       +3.323        +2.533        +2.586       +3.122
  D 7.0     +4.083       +4.437        +3.690        +3.718       +4.220
  D 8.0     +5.207       +5.541        +4.834        +4.838       +5.310
  largest fragment that clears the 1.500 mm nose: D13 centred 4.740, D13 seat+1.00 4.384,
    D13 seat-1.00 5.118, D12 centred 5.050, D12 seat+1.50 4.541, D12 seat-1.50 5.613
  escaping-fragment outer reach vs the measured port bore r 7.999:
    D4.00 reach 7.309 (+0.690), D4.74 reach 7.647 (+0.352), D5.00 reach 7.763 (+0.236), D5.12 reach 7.817 (+0.182)
```

Identical to r7/r9 to 0.001 mm: **B8's gain over r6 is held**, the worst-case
escaping fragment is **Ø4.740 mm** (D13 centred) / **Ø5.613 mm** (D12, seat
−1.50), and every escapee still fits the exit port with **+0.182 mm** minimum
margin — the tightest clearance anywhere on the exit path.

**(b) The wedged sliver that must be sheared** — sliver of radial width w
trapped in the crescent between a seated Ø13 granule and the measured Ø14.998
bore, shear plane at the measured 1.500 mm nose/roof underside, 90°-conforming
shard on the mean crescent radius:

```
   w      y_seat   depth   height_to_shear  half-angle  self-lock  chord90(mm)  A(mm2)   F(N)   x20.4N  x12.2N
  1.000    0.114    7.886        9.386       0.50    YES       10.99    10.99    3.96    5.15x   3.08x
  1.500    2.502    5.498        6.998      11.32    YES       10.60    15.90    5.72    3.56x   2.13x
  2.000    3.466    4.534        6.034      16.11    YES       10.21    20.42    7.35    2.78x   1.66x
  2.500    4.155    3.845        5.345      19.86    YES        9.82    24.54    8.83    2.31x   1.38x
  2.793    4.484    3.516        5.016      21.81    no         9.59    26.77    9.64    2.12x   1.27x
  3.000    4.691    3.309        4.809      23.10    no         9.42    28.27   10.18    2.00x   1.20x
  4.000    5.478    2.522        4.022      28.72    no         8.64    34.55   12.44    1.64x   0.98x
  5.000    6.000    2.000        3.500      33.69    no         7.85    39.26   14.13    1.44x   0.86x

  WIDEST SELF-LOCKING SLIVER: w = 2.792 mm, seats 4.483 above the granule centre (3.517 below the disc top),
    must be >= 5.017 mm tall to reach the shear plane; A = 26.76 mm2, F_shear = 9.64 N
    -> recovery margin 2.12x (20.4 N), normal-current margin 1.27x (12.2 N)
  shearable-section bound: 56.7 mm2 at recovery, 34.0 mm2 at normal current; whole pocket bore = 176.7 mm2
  180-deg conforming shard at w=2.792: A 53.53 mm2, F 19.27 N -> 1.06x recovery, 0.63x normal
  full-ring crescent at w=2.792: A 107.06 mm2, F 38.54 N -> 0.53x recovery, 0.32x normal
  whole-granule crush 41 N (ASSUMPTION): recovery 20.4 N = 2.01x under -> a trapped whole granule stalls, it is not milled
```

**Shear-margin headline, unchanged and reproduced: the worst self-locked sliver
the pocket can hold (w = 2.792 mm, ≥ 5.017 mm tall) needs 9.64 N; the drive
delivers 20.4 N in recovery and 12.2 N at normal current → 2.12× / 1.27×.**
Where it runs out is also unchanged: a 180° conforming shard is 1.06× (0.63× at
normal current, i.e. it *needs* the recovery stroke) and a full-ring crescent
0.53× → stall. That bound must stay in the shipped notes.

Note the build notes' own §8.3 table uses a narrower crescent chord and so
reports a *less* conservative worst case (w = 3.0: A 25.5 mm², F 9.2 N vs my
28.27 mm² / 10.18 N; w = 5.0: 25.0 mm² / 9.0 N vs 39.26 / 14.13). The headline
margin is 2.0–2.2× either way, so this is a presentation difference, not a
defect — but the 180°/full-ring bounds are only in *my* table and r3's, not in
the shipped notes.

**Contact order** (the mandate's ordering clause) re-measured, not restated:
bristle tip **1.200 mm** < nose underside **1.500 mm** = roof underside
**1.500 mm** → anything the compliant element passes, the rigid elements pass.

### Stall-recovery motion has the free travel it needs — verified

**Rotational freedom is unconditional (the rev-0 agitator-clash blocker stays
closed).** Convex-hull vertices of each rotor (630 for the agitator, 1840 for
the disc — a *superset* of r3's "critical vertices", so these are the more
conservative numbers), signed-distance against each static:

```
  agitator: 1030 critical points (outermost/topmost + convex hull), 360 angles at 1 deg
     vs meter_housing            min clearance    0.550 mm at rotation   0 deg, angles with penetration 0/360
     vs hopper                   min clearance    0.933 mm at rotation  87 deg, angles with penetration 0/360
     vs brush_holder             min clearance    0.600 mm at rotation  17 deg, angles with penetration 0/360
     vs retaining_plate_chute    min clearance   25.350 mm at rotation   0 deg, angles with penetration 0/360
  pocket_disc: 2240 critical points (outermost/topmost + convex hull), 360 angles at 1 deg
     vs meter_housing            min clearance    0.973 mm at rotation 206 deg, angles with penetration 0/360
     vs hopper                   min clearance    6.639 mm at rotation 150 deg, angles with penetration 0/360
     vs brush_holder             min clearance    1.500 mm at rotation   0 deg, angles with penetration 0/360
     vs retaining_plate_chute    min clearance    0.500 mm at rotation   0 deg, angles with penetration 0/360
  agitator fingers: 3 at theta 0/120/240 deg, 4.9 deg wide at r > 44, r_max 46.743 vs the window edge 47.000
```

(r3 reported 0.778 mm agitator↔meter_housing and 2.040 mm agitator↔brush_holder
from a smaller point set; my 0.550 / 0.600 mm come from a superset of the same
kind of points and are the numbers to carry. Both agree on what matters:
**0 penetrations at 360/360 angles for both rotors against all four statics** —
the recovery stroke has unobstructed rotational freedom.)

**Reverse-stroke free travel** (recovery runs +θ), ceiling ray-cast on
`meter_housing` + `brush_holder`, 0.25° steps — I reproduce the build notes to
one sweep step, with one correction:

```
   park      ceiling@park   2.0 mm proud   5.0 mm proud  11.5 mm proud     (measured at the PCD, r = 32)
    135.0       1.500      n/a (1.50)     n/a (1.50)     n/a (1.50)
    157.5       8.640      107.50 deg     102.25 deg     n/a (8.64)
    180.0         inf       85.00 deg      79.75 deg      70.00 deg
    202.5         inf       62.50 deg      57.25 deg      47.50 deg
    225.0         inf       40.00 deg      34.75 deg      25.00 deg
    247.5         inf       17.50 deg      12.25 deg       2.50 deg
   at r = 24.5 (a stacked Dia13 granule spans r 25.5..38.5, it is not a point at the PCD):
    157.5 ceiling 7.450 -> 107.50 | 102.25 | n/a ; 180.0 -> 85.00 | 79.75 | 69.75 ; 202.5 -> 62.50 | 57.25 | 47.25
    225.0 -> 40.00 | 34.75 | 24.75 ; 247.5 -> 17.50 | 12.25 | 2.25
```

The notes' "n/a" at the 157.5° park for an 11.5 mm stack is **legitimate and I
confirm it**: the ceiling there is 8.640 mm at the PCD and 7.450 mm at r 24.5,
so an 11.5 mm stack cannot occupy that park at all — round 3's 0.25° figure was
measured for an object that cannot be there. The **guaranteed** reverse free
travel is therefore set by the 247.5° park, and it is **2.50° at the PCD but
2.25° at r 24.5**, against the **2.75°** the notes publish (they sampled only
the PCD and count the last clear step inclusive). Publish 2.25°.

### MAJOR — the r4 plug-tether anchor lug protrudes into the drop tube and into the fitted plug; 122.596 mm³ of unintended interference is logged as "the designed 0.3 mm press fit"

This is new geometry added this round to close round-3's granule-path MODERATE 3
(dispensing into a fitted plug). The fix is right in principle; the lug is 1.0 mm
too far inboard.

Measured on `retaining_plate_chute_r10.stl`, radial rays from the chute axis
(32, 0):

```
  z = -396.0 / -397.0 : r_min 10.995 (nothing intrudes)
  z = -398.0 .. -404.0: r_min 10.000, intruding angular run theta 339..21 deg (+/-21 deg about +x)
                        r(a) = 10/cos(a) exactly -> a FLAT at x = 42.000, 8.0 mm wide in y
  z = -404.5 / -405.0 : r_min 10.996 (clear again)
  first z with r = 10.0: -398.00   last z with r = 10.0: -404.00   (6.000 mm tall)
```

The chute bore is r 11.000, so the lug stands **1.000 mm proud of the bore wall
over a 6.000 × 8.000 mm patch**, 1.25–7.25 mm above the chute mouth (−405.25).
Consequences, measured:

- **The drop tube is no longer Ø22.000 continuous.** Minimum clear width across
  the bore in that band is **21.000 mm** (x 21.000…42.000); the Ø13 granule's
  free lateral envelope shrinks from **±4.500 mm to +3.500/−4.500 mm**. A Ø13
  sphere swept down at centre offset +4.0 mm — legal everywhere above −398 —
  interferes at 9 of 11 stations; at +3.5 mm it interferes at 1 station; on the
  axis, 0. It is **not** a blockage (a granule cannot arch on a 21 mm bore), but
  it is an upward-facing 1.0 × 8.0 mm ledge in the fall path and a fines shelf,
  and it is not mentioned anywhere in `BUILD-NOTES-r4.md`.
- **It collides with the plug it exists to tether.** OCC boolean, both parts as
  exported (the plug *is* exported in the fitted pose — its Ø22.3 land sits
  0.150 mm radially into the Ø22.000 bore, which is the intended press):

```
  retaining_plate_chute ^ chute_plug = 206.099 mm3   (the model's own log: "^ retaining_plate 206.0993 mm3 = the designed 0.3 mm press fit")
    body  83.504 mm3  x[20.85,43.15] y[-11.15,11.15] z[-389.000,-381.000]  <- THE PRESS FIT (2*pi*11.075*0.150*8.0 = 83.5)
    body  16.973 mm3  x[42.00,42.60] y[ -3.52, 3.52] z[-404.000,-398.000]  <- plug shank r 10.600 vs the tether lug at r 10.000: 0.600 mm radial
    body  52.811 mm3  x[29.00,40.66] y[ 11.00,14.00] z[-407.250,-405.250]  <- plug Dia28 flange vs plate structure below the chute mouth
    body  52.811 mm3  x[29.00,40.66] y[-14.00,-11.00] z[-407.250,-405.250]  <- mirror of the same
  plate material in the flange annulus (r 10.6..14.0 about the chute axis) reaches down to z = -409.750 at |y| >= 11.000
```

So **83.504 mm³ is the designed press fit and 122.596 mm³ is not** — 16.973 mm³
of shank-vs-lug (0.600 mm radial) plus 105.623 mm³ of flange-vs-plate (up to
**3.000 mm** radial, through the full 2.000 mm flange thickness). The plug is
TPU, so it will deform rather than refuse, but as modelled the flange cannot
reach its seat and the shank must be forced over a rigid 1.0 mm step.

The **documentation half of this is the RT-19/N15 failure this rule exists to
catch**: the model prints one number for three different things and labels all
of it "designed". `BUILD-NOTES-r4.md` §1 then reports the tether as closed
("the plug is captive") without any interference number at all.

Fix is one line and costs nothing: move the lug's inboard face out to the bore
wall (x = 43.0 rather than 42.0) and trim the flange or the structure below the
mouth. Then re-run the boolean and print the three bodies separately.

### MODERATE 1 — the "lift/push 1.92 vs the 1.44 self-locking requirement" credit still does not apply to the fragment class B8 exists to reject

Round 3 said the nose confronts the 1.50–7.45 mm band with an 89.6–89.8° wall.
Round 4 rebuts this with a **ray cast at the object's crown height** and
concludes that everything from 2.10 to 7.45 mm proud meets a 27.5° ramp at
lift/push 1.92. **That rebuttal is only valid for a flat-topped column.** A
rounded fragment is *wider below its crown*, so its leading surface reaches the
nose earlier and lower. Swept-sphere first contact (closest-point query against
`brush_holder_r10.stl`, 0.05° steps, fragment at the measured nested crown
height, at three radii spanning the pocket):

```
  D5.0 nested (crown +1.800)  r=26.7: contact theta 159.20, contact height +1.500, n=(+0.000,+0.000,-1.000) -> 0.0 deg from horizontal
  D5.0 nested                 r=32.0: contact theta 157.30, contact height +1.500, n=(+0.000,+0.000,-1.000)
  D6.0 nested (crown +2.948)  r=26.7: contact theta 162.20, contact height +1.500, n=(-0.530,-0.848,-0.000) -> face 90.0 deg from horizontal, lift/push 0.00
  D6.0 nested                 r=32.0: contact theta 159.80, contact height +1.500, n=(-0.530,-0.848,-0.000) -> 90.0 deg, lift/push 0.00
  D7.0 nested (crown +4.083)  r=32.0: contact theta 161.30, contact height +1.500, n=(-0.530,-0.848,-0.000) -> 90.0 deg, lift/push 0.00
  Dia9-class shard (+6.000)   r=32.0: contact theta 163.40, contact height +1.500, n=(-0.530,-0.848,-0.000) -> 90.0 deg, lift/push 0.00
  stacked 2nd granule (+11.5) r=32.0: contact theta 175.95, contact height +7.450, n=(-0.375,-0.600,+0.707) -> 45.0 deg, lift/push 1.00
```

The normal (−0.530, −0.848, 0.000) is exactly the +θ tangential direction at the
wiper station (θ = 147.63 → tangent (−0.536, −0.845)): **a vertical face whose
normal is exactly anti-travel.** For the D5.0 case the contact is on the corner
itself (the reported normal is the underside triangle at the same corner, i.e.
the fragment is pressed *down*, not lifted). Face audit on the same part
confirms the geometry:

```
  brush_holder, granule band r 18-47.5 and 0-10.5 above the disc, faces whose normal opposes travel (dot > 0.50):
    total 203.05 mm2; |n_z| < 0.05 (vertical) 80.52 mm2 (39.7 %); area-weighted n_z +0.427
    largest single vertical confronting face 21.54 mm2 at theta 154.34, r 40.75, height 8.24 above the disc
    vertical confronting faces with centroid 1.4..2.8 mm above the disc: 16.02 mm2 over 2 triangles  <- the blunt tip
  meter_housing, same band: total 75.75 mm2, largest single vertical confronting face 8.90 mm2 at theta 249.98
```

So round 4's **16.0 mm² / 0.60 mm blunt tip is real and correctly measured** —
round 3's "5.95 mm square wall" was an overstatement, the space above 2.10 mm at
that θ is empty. But the tip is still what a *rounded* fragment hits first, at
1.500 mm, with lift/push **0.00**, for every fragment size from Ø6 up. Two
consequences for the text:

1. `BUILD-NOTES-r4.md` §8.1's conclusion ("Everything from 2.10 mm to 7.45 mm
   meets the 27.5° forward ramp — lift/push 1.92") is **not true for spherical
   or blobby fragments**, which is the credible fragment shape. It is true only
   for a flat-topped column.
2. §8.3's torque-budget block still prints **"the deflector nose ramp lifts
   rather than stubs — lift/push = cot(30) = 1.73"**, which contradicts §8.1's
   own measured 27.5°/1.92 *and* the sphere result of 0.00, in the same
   document. Three different numbers for one face.

**What actually carries the requirement, and it does carry it:** the fragment is
stubbed and returned to the open sump (the nose sits inside the 120° window, so
there is somewhere for it to go), or it is crushed. Crush numbers, measured
section × the carried 0.36 MPa: Ø5.0 → 19.63 mm² → **7.07 N**, Ø6.0 → 28.27 mm²
→ **10.18 N**, Ø7.0 → 38.48 mm² → **13.85 N**, against **12.2 N** at normal
current and **20.4 N** in recovery. Everything up to Ø7 yields inside the drive's
capability, and every one of these is far under the 41 N whole-granule crush
load, so a whole granule still stalls rather than being milled. Write *that*
argument, with these numbers, instead of the ramp credit.

### MODERATE 2 — the sump outlet plateau (N10) is unchanged and should be re-stated with this round's measured numbers

`27.000 mm × 120.000°` annular window, r 20.050 → 47.000, area 1894.4 mm²,
equivalent circular orifice **D 49.11 mm**. Minimum opening dimension / D_max =
**27.000/13.0 = 2.077** (r6: 2.04, r7: 2.08, r9: 2.077) — below every no-arch
criterion (≥ 3× for a slot, ≥ 4–6× for a hopper outlet). The defence is the
agitator: **3 fingers at θ 0/120/240**, 4.9° wide at r > 44, tip r 46.743 against
the window edge 47.000, so exactly one finger is in the window at a time and each
22.5° index sweeps **18.75 %** of the window (one full sweep per 2.67 dispensed
granules). This remains a **plateau, not a pass**, and the punch list permits it
only if those numbers are printed — they are not in `BUILD-NOTES-r4.md` §11
item 2 beyond the ratio.

### MINOR 1 — the entry-ramp angle is a range, not "25°"

The relief ramp is a constant-dz/dθ surface, so the angle a granule actually
meets depends on radius:

```
   r= 20.5: ceiling 10.287 ->  1.639 = drop 8.648 mm over 11.807 mm of arc -> 36.22 deg, cot = 1.365  (< 1.44)
   r= 22.0: 10.281 -> 1.640 = 8.641 over 12.671 -> 34.29 deg, cot = 1.466
   r= 24.5: 10.270 -> 1.641 = 8.629 over 14.111 -> 31.45 deg, cot = 1.635
   r= 32.0: 10.240 -> 1.645 = 8.594 over 18.431 -> 25.00 deg, cot = 2.145   <- the published figure
   r= 39.5: 10.269 -> 1.649 = 8.620 over 22.750 -> 20.75 deg, cot = 2.639
   r= 46.5: 10.296 -> 1.653 = 8.644 over 26.782 -> 17.89 deg, cot = 3.098
```

At r ≤ 21.9 the ramp's lift/push falls **below the 1.44 self-locking criterion**
the same notes use as the pass/fail line elsewhere. **No action needed** — the
nose covers r 20.5…47.0 at 1.500 mm, so nothing more than 1.500 mm proud ever
reaches the ramp, and anything ≤ 1.500 mm proud never touches it. But the
package should publish the range, not the single PCD number.

### MINOR 2 — items I re-checked that are unchanged and correct

- **B7** (recorded plateau) re-derived analytically from the measured
  first-material radius 8.747 and PCD 32: support lost at **5.00 / 7.00 / 8.75°**
  (Ø13 at seat +1.00/0.00/−1.00), **4.25 / 7.00 / 9.50°** (Ø12), **3.25 / 7.00 /
  10.50°** (Ø11) → window **3.25…10.50°**, spread **7.25°** across Ø11–Ø13 and
  **3.75°** at Ø13 alone. This is exactly what round 4 publishes; round 3's
  MAJOR (numbers that did not reproduce) is **closed**. Park separation
  **12.4858 mm**; park retention margin vs the measured rim: D13 **+2.761**,
  D12 **+2.261**, D11 **+1.761** — none negative.
- **N6** stays closed: disc lightening voids open at r 11.0 (120/360 azimuths)
  and r 15.0 (104/360), **closed at r 15.5 (0/360)** → radial land to the window
  inner edge r 20.000 is **4.500–5.000 mm** (punch list asks ≥ 2.0).
- **B1.3 face audit**, printed as the punch list asks whatever the result: the
  largest vertical (|n_z| < 0.05) confronting face in θ 131…160 is **21.54 mm²
  at θ = 154.34, r = 40.75, n_z = 0.000** — over B1.3's 20 mm² line, but its
  centroid is **8.24 mm above the disc**, i.e. above the 7.450 mm rail underside
  where no granule or fragment can be. Not a defect; it is a number the round-4
  notes do not print.

### What I would require to pass the granule path next round

1. **Move the tether anchor lug out of the bore** (inboard face at the bore wall,
   not 1.000 mm inside it) and clear the plug flange, then print the plate ∩ plug
   boolean **decomposed by body**, with the designed press fit (83.5 mm³) named
   separately from everything else. The current "206.0993 mm³ = the designed
   0.3 mm press fit" line must not survive into the shipped notes.
2. **Restate B8.3 against a rounded fragment**: first contact for Ø5–Ø9 nested
   fragments is the nose's leading bottom corner at 1.500 mm, normal exactly
   anti-travel, **lift/push 0.00**; the mechanism that carries the requirement is
   the open-sump return path plus the crush/shear backstop (7.07 / 10.18 /
   13.85 N for Ø5 / Ø6 / Ø7 vs 12.2 N normal and 20.4 N recovery). Delete the
   `cot(30) = 1.73` line from §8.3 — it contradicts §8.1 in the same file.
3. **Publish the reverse-stroke bound as 2.25°** (r 24.5 at the 247.5° park), not
   2.75° (PCD-only).
4. **Keep** the shear table *with* its bounds (2.12× at the worst self-locking
   sliver, 1.06× at a 180° shard, 0.53× at a full ring; σ = 0.36 MPa and µ = 0.4
   are assumptions closed by IFDC S-115), and the N10 numbers (27.000 mm ×
   120.000°, 2.077 × D_max, D_eq 49.11 mm, 18.75 % of the window per index).

---

# integration

**VERDICT: FAIL (blocking).** One hard geometric defect: the aircraft-harness
conduit — the entire point of Thomas directive 2 — is **solid printed material
at the top-plate elbow**. No conductor of any diameter can get from the
attachment interface to the electronics bay. The build notes and the model's
own B5-c table say the opposite ("COVERED 18.00 mm top-plate elbow -> hopper
conduit", "95.3 % covered"), which is the RT-19 / N15 failure class this round
exists to prevent. Everything else in my scope (a, c, d, e) passes on the
exports.

Method: all numbers below are re-measured by me on `cad/exports/*_r10.step` and
`*_r10.stl` with `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`
(build123d 0.11.1 OCC booleans, trimesh 5.0.0, numpy 2.5.1, scipy). I imported
nothing from `dispenser.py`; parameter names are quoted only to name a root
cause after the geometry was measured. `[A]` marks an assumption I introduce.

---

## (a) Gloved-hand access corridor to the quick-release — **PASS**, with two caveats

### The corridor I require, and why

`[A]` **95 mm wide × 45 mm tall × 130 mm deep**, floor-to-ceiling band with its
top at the clip-plate underside, measured **from the neck face outward**:

- **95 mm wide**: 95th-percentile adult male hand breadth across the
  metacarpals ≈ 90 mm; a light mechanic's glove adds ≈ 2–3 mm per side → ≈ 95 mm.
  `[A — anthropometric figure quoted from memory, not from a table I opened
  this round; closure = a tape measure on a gloved hand or one sentence from
  Thomas.]`
- **45 mm tall**: 95th-percentile hand thickness at the metacarpals ≈ 34 mm,
  + glove + knuckle working clearance ≈ 45 mm. `[A, same closure]`
- **130 mm deep**: the hand must pass the release and the forearm follow it.
  `[A]`

These are deliberately the **same three numbers as PUNCHLIST B6.2**, so this
round is comparable with rounds 1–3.

### Measured

```
clip-plate underside Z = -181.550   (payload top face Z = -171.050)
first dispenser material OUTSIDE the 48x48 neck column at Z = -225.050
STAND-OFF HEIGHT h = 43.500 mm                    (PUNCHLIST B6.1 target h >= 40)
  the limiting part: top_plate, 552.4 mm3 in the band, X[-7.50,7.50] Y[-85.50,-24.00]
  -- the harness strain-relief boss on -Y. Everywhere else h = 52.000 mm to the
  top-plate top face (-233.550); on +Y the fill cap tops out at -230.700 (h = 48.850).
neck plan half-extent a = 24.000 mm  (48.00 x 48.00)   (B6.1 target a <= 35)

CORRIDOR BOOLEANS (from |x| or |y| = 24.0 outward 130 mm, top at Z = -181.55):
  95 x 45 x 130:   +X 0.0000   -X 0.0000   +Y 0.0000   -Y 340.2241 mm3 (top_plate)
 100 x 45 x 130:   +X 0.0000   -X 0.0000   +Y 0.0000   -Y 340.2241 mm3
  95 x 52 x 130:   +X 0.0000   -X 0.0000   +Y 536.3662 (fill_cap)   -Y 2944.2020
 110 x 50 x 130:   +X 0.0000   -X 0.0000   +Y 159.9689 (fill_cap)   -Y 2202.4049

LARGEST CLEAR CORRIDOR PER SIDE (130 mm deep, top at Z = -181.55):
  +X: 52.000 mm tall at 95 mm wide ; unlimited width at 45 mm tall
  -X: 52.000 mm tall at 95 mm wide ; unlimited width at 45 mm tall
  +Y: 49.150 mm tall at 95 mm wide ; unlimited width at 45 mm tall
  -Y: 43.500 mm tall at 95 mm wide ; <= 5 mm wide at 45 mm tall (blocked on the centreline)
```

**B6.2 is met**: two opposing sides (+X and −X) are clear at **0.0000 mm³**, and
they are clear at the *full* 52 mm stand-off, not just at 45 mm. +Y is clear at
45 mm as well; only −Y is obstructed, by the harness strain-relief boss.

### Caveat 1 — the punch-list test as literally written is unsatisfiable

B6.2 says the corridors approach "the mount axis". Run that way:

```
literal B6.2 corridor (95 x 45 x 130 reaching the mount axis):
  +X 15039.116   -X 15039.116   +Y 14857.294   -Y 15528.488 mm3   (all top_plate = the neck itself)
```

Any stand-off design fails this, because the neck occupies the axis. My
neck-face-outward reading is the only one that can distinguish a good design
from a bad one, and it is the reading I have graded against. The punch list
should be corrected rather than the geometry.

### Caveat 2 — there is no lip to hook a finger under, and B6.3 is unverifiable here

```
clip plate STEP (2112_attach_plate_payload_side.step): footprint 50.00 x 50.00 x 10.50 mm
neck 48.00 x 48.00 -> clip-plate edge proud of the neck = 1.00 mm per side, all four sides
```

The hand can get **beside** the clip plate over 130 mm of depth, which is the
big win over r6 (Ø150 disc 5.0 mm below the plate). It cannot get **under** it:
1.00 mm of overhang is not a grip feature. And the release mechanism itself is
the drone-side half (interface README: "spring press-pins … it clips into the
aircraft's fixed half by hand"), which lives **above** Z = −171 and is not in
these exports — so **B6.3 (QR actuation-envelope sweep) cannot be measured on
this package at all**. I am recording it as *not verified*, not as passed. If
the vendor release needs a squeeze on the clip half's sides, 1.00 mm of proud
edge is the number that has to be defended.

---

## (b) Electronics bay + wiring routes — **BLOCKING FAIL**

### B5.1 board fit — PASS

```
cavity centre recovered from the export: Z = -337.25 (bay box centre y = -75)
standoff free faces, 4 of 4, all at y = -69.000   (x = +/-18.0, z = -323.25 / -351.25)
BOARD ENVELOPE 42 (x) x 34 (z) x 12 (y) seated on those faces:
   ^ electronics_bay = 0.0000 mm3      ^ bay_lid = 0.0000 mm3        (B5.1 asks 0.000)
six clearance gaps (grow the envelope face by face until it touches bay+lid):
   +X               5.000 mm        (B5.1 asks >= 1.5)
   -X               5.000 mm
   +Z (up)          1.950 mm
   -Z (down)        1.850 mm
   -Y (lid)         7.600 mm
   +Y               0.000 mm  <- this face IS the standoff seat, i.e. the mounting
                                 datum, not a wall; the inboard WALL is 5.000 mm
                                 behind it (standoff height)
cavity height measured 37.80 mm (ELECTRONICS 7 asks 38); x half-walls at +/-26.0
```

### B5.2 three grommeted entries — PASS

```
(1) top riser socket (aircraft harness): x-scan at y=-81, z=-310 -> x -5.200,-3.700,3.700,5.200
    -> bore Dia7.400, grommet land (10.4-7.4)/2 = 1.500 mm      (B5.2 asks land >= 1.5)
(2) motor cable, +Y face, x=+10, z=-350.25: +Y ray sees NO material -> clean through-hole
(3) count-sensor cable, +Y face, x=-10, z=-350.25: same
    Dia 5.9 x 8 plug through the inboard wall: 0.0000 mm3
    Dia 6.0 x 8 plug:                          0.0000 mm3
    Dia 7.0 x 8 plug:                          0.0000 mm3
    Dia 9.9 x 8 plug:                          1.5894 mm3
    Dia10.0 x 8 plug:                          2.9999 mm3
    -> Dia6.000 through, Dia10.000 grommet counterbore, land 2.000 mm
```

### B5.3 gasket groove — PASS

```
60-point scan of the 26.0 x 19.5 centreline rectangle on the sealing face:
  groove-floor Y   min -89.000   max -88.800
  sealing land Y   -90.000
  -> depth 1.000 .. 1.200 mm (B5.3 asks >= 1.0)
  x-scan through the groove at y = -89.4: material x [-34.000, -26.800, 26.800, 34.000]
  -> groove width 1.600 mm (B5.3 asks >= 1.5)
  interruptions: 0 of 60 (must be 0)
  closed-loop centreline perimeter = 182.00 mm
```

### B5.6 lid removable in situ — PASS

```
bay_lid solid translated -Y by 0.5 / 1 / 2 / 4 / 8 / 12 / 16 / 20 mm
  vs EVERY other solid: 0.0000 mm3 at every station
4 x Dia6 x 25 mm driver columns on the lid screws (+/-29.0, -337.25 +/- 22.0)
  vs all solids other than bay+lid: 0.0000 / 0.0000 / 0.0000 / 0.0000 mm3
```

### Dust path tank → bay — PASS

```
24 random Dia1.2 columns from inside the tank (r<60, z -320..-250) to the -Y
conduit bore: 0 are OPEN (must be 0)
```

### **B5.5 / directive 2 — FAIL: the harness conduit is solid at the elbow**

The route the package describes is: blind-mate PCB → hollow neck → −Y exit →
top-plate horizontal conduit → **elbow** → vertical spigot → hopper conduit →
bay riser socket. The elbow does not exist as a bore.

```
Dia5.5 bundle [A, PUNCHLIST B5.4] swept along the modelled route:
  seg (0,-10,-186.00) -> (0,-10,-230.55)  len  44.55 mm : top_plate =   2.535 mm3
  seg (0,-10,-230.55) -> (0,-81,-230.55)  len  71.00 mm : top_plate = 213.825 mm3
  seg (0,-81,-230.55) -> (0,-81,-316.00)  len  85.45 mm : top_plate = 166.308 mm3

OCCUPANCY on the bore axes (trimesh.contains on top_plate_r10.stl,
1.0 mm grid, confirmed by 0.4 mm probe cubes at 0.5 mm spacing):
  vertical spigot axis  (x=0, y=-81)   : SOLID over z = -237.50 .. -225.00  (12.5 mm)
  horizontal bore axis  (x=0, z=-230.55): SOLID over y =  -84.00 ..  -72.00  (12.0 mm)

LARGEST CONDUCTOR THAT CAN CROSS THE ELBOW (coaxial column on the vertical bore
axis over z -237.5 .. -225.0, vs top_plate):
  Dia5.5 -> 295.791 mm3   Dia4.0 -> 156.451   Dia3.0 -> 88.004
  Dia2.0 ->  39.113 mm3   Dia1.0 ->   9.778   Dia0.5 ->  2.445
  -> NOTHING passes. Largest clear conductor = Dia0.0.

ROOT CAUSE, measured on the export: a rectangular strain-relief boss occupying
  x [-7.500, +7.500]  y [-85.500, -72.000]  z [-248.550, -225.050]
is unioned onto the plate AFTER both conduit bores are cut
(`dispenser.py` ~L1086-1094, added to bury a B10 tangency at the rim), so it
re-fills the junction of the two bores.
```

Consequences:

1. **Directive 2 is not met by the geometry.** There is a bay, and it is a good
   bay, but nothing can be wired into it from the aircraft side.
2. **B5.4 is vacuous.** "0.000 mm³ of harness in the pellet space" is true only
   because no harness can be installed.
3. **The build notes assert the opposite.** `logs/r10_build.log` B5-c prints
   `COVERED 18.00 mm  top-plate elbow -> hopper conduit` and a `95.3 %` headline.
   That table is computed from parameters; it is not a measurement of the
   exported solid. BUILD-NOTES-r4 §10 then lists B5 among the things a completed
   run proves "still hold". This is exactly the rev-0 failure mode (RT-19) that
   this round's own rule forbids.

The fix is small (cut the two bores **after** the boss, or bury the boss and
re-cut), but it is geometry, and B5 is a must-close-by-geometry item.

### Nonblocking findings in (b)

```
CHANNEL CROSS-SECTIONS, measured, vs 9 x 26 AWG PTFE (OD 1.05 -> 7.79 mm2):
  neck cavity at z=-200        42.70 x 42.70 mm = 1823.3 mm2 ->  0.4 % fill
  neck -Y exit / conduit bore  Dia6.000         =   28.27 mm2 -> 27.6 % fill
  hopper -Y conduit bore       Dia11.000        =   95.03 mm2 ->  8.2 % fill
  bay riser socket bore        Dia7.400         =   43.01 mm2 -> 18.1 % fill
  bay motor/sensor entries     Dia6.000 (Dia10.0 grommet counterbore, land 2.000 mm)
  cartridge duct (ret. plate)  Dia5.000         =   19.63 mm2 -> 64.0 % for two Dia4 pairs [A]
```

- **N-i1 — ELECTRONICS §6.3 is stale in a way not yet on the open list.** It
  costs the fit check against a "**5 × 2.5 mm channel**, 12.5 mm², **62 % fill**".
  That channel is not in the r10 geometry (`CABLE_W/CABLE_DEEP` are dead
  constants); the real section is **Ø6.000 = 28.27 mm² = 27.6 % fill**. The
  conclusion ("all 12 circuits would not fit") is *reversed* by the real
  section: 12 × 26 AWG = 10.4 mm² = 36.7 % of Ø6.0. A document edit, but it
  currently carries an engineering argument that the geometry no longer supports.
- **N-i2 — connector cannot follow the harness.** The aircraft-side connector is
  a Molex 12-circuit 1.25 mm-pitch shell. It does not pass a Ø6.000 bore, and
  the route contains a right-angle elbow inside a closed tube. Even after the
  elbow is opened, the harness has to be pulled un-terminated and crimped in
  situ, or the conduit made openable. Neither is modelled or written down.
- **N-i3 — the in-payload cable coverage is overstated.** Measured free-air run
  from the cartridge-duct mouth (0, −48.000, −363.25) to each bay entry
  (±10, −62, −350.25) = **21.56 mm each, 43.1 mm total**. The model's B5-c table
  calls the whole exposed run **23.71 mm**.

---

## (c) Refill workflow (directive 4 + RT-14 / B12) — **PASS**

**There is no side-wall fill port.** B12 allows "an equivalent measured
solution", and the route taken is a top-plate port plus a printed service stand.
Measured:

```
FILL PORT, on top_plate_r10 (centre x=0, y=+43):
  bore at z=-238.0: material y  20.007 .. 65.993  -> clear aperture Dia45.986
  cap recess at z=-234.0: y 15.500 .. 71.199      -> Dia55 recess
  Dia44.0 column through the plate: 37.3741 mm3 (edge slivers)
  Dia46.0 column:                   57.0541 mm3
  Dia46.1 column:                   70.1105 mm3
  Dia48.0 column:                  323.5711 mm3
  -> clear aperture Dia46.0        (B12.3's port target, Dia46 [A], is met)

FILL-CAP REMOVAL SWEEP (fill_cap_r10 vs every other solid):
  rotate to unlock, any angle 10..90 deg:      1.4338 mm3 residual
      (= the N5 anti-rotation detent, a designed elastic interference; already
       carried as BUILD-NOTES-r4 open item 3)
  pure axial lift:  0.0 -> 0.0000   0.5 -> 14.6145   1.0 -> 32.8827
                    1.5 -> 32.8827  2.0 -> 14.6145   2.5 -> 0.0000 mm3
      -> 2.5 mm of lift clears the bayonet; peak interference 32.8827 mm3
  MAX PURE-AXIAL LIFT before the cap fouls the B6 stand-off neck = 14.035 mm
      (cap is 8.85 mm tall, so it comes out; the +Y two-thirds of the cap has
       48.850 mm of headroom, only the y 16..24 sliver is limited)
  lift 10.0 mm then translate +Y 5/10/15/20/25/30 mm: 0.0000 mm3 at every station
  lift  5.0 mm then translate +Y: 1.228 / 144.841 / 220.317 / 162.569 / 136.757 /
       119.248 mm3 -> the cap must be lifted >= ~7 mm before it can be moved aside
```

```
REST POSITION (service_stand_r10, 103.892 cm3, 132.0 g printed CF-PETG):
  stand ground plane Z = -426.45 ; assembly lowest point (motor can) Z = -418.45
    -> the gearbox/motor can stands 8.00 mm OFF the ground: the load path does
       NOT pass through the gearbox output flange   (B12.1 satisfied)
  contact patch, 200 000 surface samples: 252 payload points within 1.0 mm of the
    stand, all at Z -358.25 .. -357.26 and r 52.28 .. 71.65 mm -- i.e. the
    meter-housing latch-ring underside. Printed structure, as required.
  support ring: outer r 90.0, inner r 76.0; support-polygon area 25 447 mm2
  CG rebuilt from the exports (see (e)): empty (1.58, -7.20, -329.51),
    height above the stand ground plane 96.94 mm, horizontal offset 7.37 mm
  TIP ANGLE = atan(82.63 / 96.94) = 40.44 deg empty
              39.27 deg loaded @250, 38.12 deg loaded @421
              (B12.1 asks >= 25 deg [A: 15 deg tailgate slope + margin])
```

Not re-derived: hopper capacity (directive 5 forbids re-opening it; I did not
independently reproduce the 962 cm³ / 421-granule figure, and nothing I measured
touches it).

**One thing to write down that currently isn't:** B12 passes **only because of
`service_stand`**, a 180 mm-diameter, 132 g printed part that is deliberately
outside the flight ledger. It is therefore mandatory ground-support equipment —
without it in the field kit the dispenser has no stable rest position and the
refill workflow does not close. It needs to be called out as required GSE in the
BOM/ops text, not just modelled.

---

## (d) Ground clearance and overall envelope — **PASS**

```
dispenser_r10_assembly.stl: 24 bodies, watertight, 587.685 cm3
  bbox X[-78.000, 78.000]  Y[-92.000, 78.000]  Z[-418.450, -171.050]
  plan envelope 156.00 (x) x 170.00 (y) mm; max radius from the mount axis 97.94 mm

B6.4  max Z = -171.050 -> payload material above Z = -171.000 is 0.000 mm3   PASS
      stack below the mounting plane = 247.450 mm

GROUND CLEARANCE at rest (ground plane Z = -547.89, landing_gear/assembly.py):
      -418.450 - (-547.89) = 129.440 mm      (required >= 40; r6 measured 181.484)
      -> the B6 stand-off costs 52.044 mm of ground clearance. Still 3.2x the
         requirement.
      with the storage chute_plug fitted (bbox min Z -421.250): 126.640 mm

PAYLOAD <-> LANDING GEAR, mesh-to-mesh on the REAL gear:
      quiver.airframe_structure.landing_gear.assembly.make_assembly(), meshed at
      tol 0.15 -> 77 547 vertices, bbox Z[-547.88, -124.94];
      300 000 surface samples on each body, KD-tree pre-pass, then exact
      point-to-triangle refine on the 3 000 nearest payload points:
      MINIMUM SEPARATION = 103.628 mm      (r6: 83.41 mm -- improved)
```

**Nonblocking:** prop clearance was **not re-measured** this round. The r10 log
restates the r2 figures verbatim (`vertical gap 152.5 mm`, blade disk Z +44.04,
radial gap 239.3 mm). The stand-off moves the payload *down and away* from the
disk, so there is no regression risk, but the shipped number is carried, not
measured — say so, or measure it.

---

## (e) Mass ledger, rebuilt independently from the exports — **PASS on the CONTEXT dry target; TIGHT on the package's own loaded headline**

Densities per PUNCHLIST B11.1: CF-PETG **1.27** g/cm³ (not 1.25), TPU 1.19,
PMMA 1.18. Volumes are my own `trimesh` reads of the shipped STLs (they agree
with the STEP volumes to ≤0.053 %).

```
PRINTED, FLIGHT CONFIG, SOLID BASIS
  top_plate                  95.755 cm3 x 1.27 =  121.61 g
  fill_cap                    7.347 cm3 x 1.27 =    9.33 g
  hopper                    109.423 cm3 x 1.27 =  138.97 g
  meter_housing             103.623 cm3 x 1.27 =  131.60 g
  pocket_disc                72.661 cm3 x 1.27 =   92.28 g
  agitator                    4.288 cm3 x 1.19 =    5.10 g   (TPU)
  brush_holder                3.544 cm3 x 1.27 =    4.50 g
  retaining_plate_chute      71.886 cm3 x 1.27 =   91.29 g
  electronics_bay            21.175 cm3 x 1.27 =   26.89 g
  bay_lid                     8.598 cm3 x 1.27 =   10.92 g
  sensor_cover (x2)           3.234 cm3 x 1.27 =    4.11 g
  count_windows (x4)          0.104 cm3 x 1.18 =    0.12 g
  PRINTED SUBTOTAL (solid)                       636.73 g
  (service_stand 103.892 cm3 / 132.0 g and chute_plug 6.874 cm3 / 8.3 g are
   ground-only and correctly excluded)

COTS / ESTIMATE (carried from cad/BOM.md; none of it is measured geometry)
  clip_plate (alu, STEP 11.52 cm3 x 2.70)          31.10 g
  stepper 14HS13-0804S-PG5 (vendor GROSS)         350.00 g
  blind-mate PCB + Molex J1                        15.00 g
  sensor PCBs x2                                    6.00 g
  electronics (MCU/CAN/TMC2209/buck/count chain)   65.00 g
  fasteners + inserts + plunger                    57.00 g
  O-ring + gaskets + 9 magnets                      8.00 g
  strip brush                                       3.00 g
  sleeve bearing igus JFM-2023-07                   1.70 g
  PTFE thrust washer                                0.70 g
  COTS/ESTIMATE SUBTOTAL                          537.50 g

  EMPTY (solid printed basis)                    1174.23 g   (model prints 1174.4 -- reproduces)
  + 10 % CAD contingency                          117.42 g
  EMPTY, CARRIED (= the DRY figure)              1291.65 g
  vs the CONTEXT structure target <= 1500 g DRY  -> MARGIN +208.35 g   PASS

  + 250 granules x 1.18 g                         295.00 g
  LOADED @250, 100 %-infill basis                1586.65 g   (margin -86.65 g)
  + 421 granules (max-fill rib)                   496.78 g
  LOADED @421, 100 %-infill basis                1788.43 g   (margin -288.43 g)

INDEPENDENT SLICER BRACKET (my own voxelisation, pitch 0.5 mm, 1.6 mm shell
= 4 perimeters x 0.4, 25 % infill core, PADDED distance transform):
  bay_lid                solid  10.92 g  core  1.33 cm3 (15.4 %)  sliced   9.65 g
  top_plate              solid 121.61 g  core 23.76 cm3 (24.8 %)  sliced  98.98 g
  fill_cap               solid   9.33 g  core  0.77 cm3 (10.5 %)  sliced   8.60 g
  hopper                 solid 138.97 g  core 14.11 cm3 (12.9 %)  sliced 125.53 g
  meter_housing          solid 131.60 g  core 60.09 cm3 (58.0 %)  sliced  74.36 g
  pocket_disc            solid  92.28 g  core 46.10 cm3 (63.5 %)  sliced  48.37 g
  agitator               solid   5.10 g  core  1.06 cm3 (24.8 %)  sliced   4.15 g
  brush_holder           solid   4.50 g  core  0.70 cm3 (19.7 %)  sliced   3.84 g
  retaining_plate_chute  solid  91.29 g  core 23.94 cm3 (33.3 %)  sliced  68.49 g
  electronics_bay        solid  26.89 g  core  1.17 cm3 ( 5.5 %)  sliced  25.78 g
  sensor_cover           solid   4.11 g  core  0.03 cm3 ( 1.0 %)  sliced   4.08 g
  count_windows          solid   0.12 g  core  0.00 cm3 ( 0.0 %)  sliced   0.12 g
  PRINTED SUBTOTAL sliced 471.95 g (artifact 164.78 g)
  EMPTY 1009.45 g -> +10 % 1110.40 g -> LOADED @250 = 1405.40 g (margin +94.60 g)
                                        LOADED @421 = 1607.18 g
```

Readings:

1. **The CONTEXT requirement is on DRY mass** ("Structure mass target ≤ 1500 g
   dry; report loaded mass at 250 and at max fill"). Dry, carried, is
   **1291.65 g → +208.35 g of margin**. That passes cleanly and the package
   should say so plainly; right now every headline is a *loaded* number graded
   against the dry ceiling, which is stricter than CONTEXT asks and makes the
   design look worse than it is.
2. **The model's shipped headline is the conservative one of the two slicer
   brackets.** Model: printed 494.5 g, LOADED @250 = 1435.0 g (+65 g). Mine at
   0.5 mm voxel pitch: 471.95 g, 1405.40 g (+94.6 g). My cores run 6–13
   percentage points higher than the model's (voxel resolution — my `bay_lid`
   control reads 15.4 % core where a 2 mm plate under a 1.6 mm shell should read
   ~0, and the model's N13 control correctly reads 0.0 %). So I confirm the
   direction and I do **not** dispute the shipped 1435.0 g.
3. **The reserve is the real story.** With the model's own 61.0 g of open-item
   reserve the headline is 1496.0 g against 1500 — **+4 g** — and that reserve
   does **not** contain a line for re-cutting the conduit elbow, nor for the
   grommets/harness actually being fitted through it. Any mass added by the B5
   fix comes straight out of 4 g.
4. **Estimate exposure: 537.50 g of the 1174.23 g empty subtotal is 45.8 %
   COTS/estimate**, of which 150.4 g (12.8 % of empty) is non-vendor estimate and
   350 g is a vendor *gross* catalogue figure that has never been on a scale.
   The 10 % contingency (117.4 g) does not bound that.

---

## Summary for the round

| item | verdict | headline number |
|---|---|---|
| (a) reach-in corridor, directive 3 | **PASS** | 95 × 45 × 130 clear at **0.0000 mm³** on +X, −X and +Y; h = **43.500 mm**, a = **24.000 mm** |
| (a) B6.3 QR actuation sweep | **NOT VERIFIABLE** | release mechanism is drone-side, above Z = −171; clip-plate edge proud of the neck = **1.00 mm/side** |
| (b) bay itself (B5.1/.2/.3/.6) | **PASS** | board **0.0000 mm³**, gaps 5.000/5.000/1.950/1.850/7.600 mm; entries Ø7.400 + 2 × Ø6.000 (land 2.000); gasket 1.600 × 1.000–1.200 mm, 0/60 interruptions, 182.00 mm loop; lid sweep 0.0000 mm³ |
| (b) harness route (B5.4/.5), directive 2 | **BLOCKING FAIL** | conduit **solid** over z −237.50…−225.00 and y −84.00…−72.00; largest conductor that crosses the elbow = **Ø0.0** |
| (c) refill / rest position (B12) | **PASS** | port Ø**46.0**; cap clears at 2.5 mm lift, 14.035 mm of axial room; motor can **8.00 mm** off the ground; tip angle **40.44°** empty / **38.12°** at 421 |
| (d) ground clearance / envelope | **PASS** | **129.440 mm** ground, **103.628 mm** to the real landing gear, **0.000 mm³** above Z = −171.000 |
| (e) mass ledger | **PASS (dry) / TIGHT (loaded)** | dry carried **1291.65 g** vs 1500 (+208.35); loaded @250 **1586.65 g** solid basis, **1405.4–1435.0 g** sliced; with reserve **1496.0 g (+4 g)** |

**Required to close:** re-cut the two conduit bores after the strain-relief boss
(or bury the boss and re-cut), then re-run the Ø5.5 sweep and print
`0.0000 mm³` per segment; and replace the B5-c coverage table with a
measurement of the exported solid rather than a parameter roll-up, because the
present table is what let a fully blocked conduit ship as "95.3 % covered".

---

## assembly

**Owner:** assembly-and-drive critic (rev-0 RT-1; punch-list **B2, B3-access,
B9a/b/c/d, B10, B12.2** in so far as they are assembly/torque items).
**Verdict: FAIL — 1 blocking finding (A-10).** Both round-3 blockers are
**closed** on the r10 exports: A-8 (`retaining_plate_chute_r9.stl` not a valid
mesh) and A-9 (bay screws 7.0 mm too short). Every one of round 3's five
non-blocking items is closed or answered. The assembly order still closes at
**0.0000 mm³** on 17 of 18 operations, and the torque path measures clean for
the fourth round running. What fails is new and it is in the BOM-vs-geometry
seam that B9 exists to catch: **the four screws that fasten the gearbox to the
retaining plate — the entire motor→plate attachment of the torque path — are
specified as cap-head screws, and a cap head fouls the pocket disc.**

### Provenance

- Measured on `cad/exports/*_r10.*`, mtime **2026-08-07 17:36**, and
  `cad/BOM.md`, mtime **2026-08-07 18:05** (i.e. after the exports).
  `md5(dispenser_r10_assembly.step) = 44ec8e05943a138f295583cc8f46b039`,
  `md5(dispenser_r10_assembly.stl) = d04c254b7a43859769c4ac3e43353324`,
  `md5(retaining_plate_chute_r10.step) = 286547c43efb4c6716ce941fafd44055`,
  `md5(pocket_disc_r10.step) = 6a0988b2549ddd59fff88b051d3a18f4`,
  `md5(meter_housing_r10.step) = f4e4e76a401202e7b719770614f3e12e`,
  `md5(top_plate_r10.step) = f02b23a6652ac09a5cc13c9cbfaabc9b`,
  `md5(hopper_r10.step) = 0726001a5b667fe56c24e28e0e942811`,
  `md5(electronics_bay_r10.step) = 76edd65689a6ddb50c34026dd5826eea`,
  `md5(chute_plug_r10.step) = ad2e08156bab5a8cbb05597689309292`,
  `md5(service_stand_r10.step) = 4feb744b37d77945144d6d42cac5f773`.
  The first four match the md5 table in `BUILD-NOTES-r4.md` §0, so this critique
  and the build notes are looking at the same bytes.
- All obstruction volumes are **exact OCC booleans** on the STEP bodies
  (`build123d.import_step` + `BRepAlgoAPI_Common` + `BRepGProp`), not voxel
  estimates. Profile/grip probes are trimesh ray-casts on the STLs. venv
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`, build123d 0.11.1,
  trimesh 5.0.0, numpy 2.5.1. Nothing is imported from `dispenser.py`; the two
  places I quote a source line (the countersink cut at L1752, the BOM row
  emitted at L4607) are quoted only to name the root cause after the geometry
  had already been measured.
- COTS bodies were identified in `dispenser_r10_assembly.step` by volume match
  against the part exports; the six unmatched solids (clip plate 11.5234,
  motor+gearbox 69.9363, bearing 1.4946, blind-mate PCB 1.1744, thrust washer
  0.3167, brush strip 0.3122 cm³) are identified from size and position — an
  **ASSUMPTION**, unchanged from rounds 1–3.
- Convention: "approach from +Z" means the part starts 40–60 mm above its seat
  and travels −Z. A straight-line path is reversible, so each station table is
  both the install and the removal check. Primed rows are controls: the same
  part on the opposite approach, printed so that "0.0000" cannot mean "the
  probe missed".

### 0. Part inventory, export integrity (B10 / A-8 — **CLOSED**), static interference

```
PART EXPORTS (r10), STEP volume vs an INDEPENDENT trimesh census of the shipped STL:
  part                    nsol   STEP cm3    STL cm3   d%      watertight winding euler nonman open bodies
  agitator                   1      4.291      4.288  -0.053      True     True     2     0     0    1
  bay_lid                    1      8.598      8.598  +0.001      True     True   -10     0     0    1
  brush_holder               1      3.544      3.544  +0.001      True     True     0     0     0    1
  chute_plug                 1      6.877      6.874  -0.039      True     True    -2     0     0    1
  count_windows              4      0.104      0.104  -0.041      True     True     8     0     0    4
  electronics_bay            1     21.175     21.175  +0.002      True     True    -8     0     0    1
  fill_cap                   1      7.349      7.347  -0.035      True     True     0     0     0    1
  hopper                     1    109.419    109.423  +0.004      True     True   -14     0     0    1
  meter_housing              1    103.659    103.623  -0.035      True     True   -12     0     0    1
  pocket_disc                1     72.686     72.661  -0.034      True     True   -30     0     0    1
  retaining_plate_chute      1     71.903     71.886  -0.024      True     True   -48     0     0    1
  sensor_boards              2      1.287      1.287  -0.012      True     True     4     0     0    2
  sensor_cover               2      3.234      3.234  +0.000      True     True    -4     0     0    2
  service_stand              1    103.908    103.892  -0.015      True     True     0     0     0    1
  top_plate                  1     95.780     95.755  -0.026      True     True   -36     0     0    1
  TOTAL printed STEP = 613.812 cm3      parts watertight: 15/15   (r9: 14/15)
  dispenser_r10_assembly.stl: watertight=True winding=True euler=-167 bodies=24 (for 24 solids)
                              vol=587.685 cm3  edge multiplicity {2: 191100}  open edges 0  non-manifold 0
ALL-PAIRS EXACT BOOLEAN INTERFERENCE (assembly STEP, 24 solids, 276 pairs):
  46 bbox-overlapping pairs boolean-checked, 0 with non-zero intersection
```

**A-8 is closed and I reproduce the builder's census independently.** r9 read
`watertight=False`, 188 open edges, 4817 non-manifold edges, +8.36 % STL volume
on `retaining_plate_chute`; r10 reads True / 0 / 0 / −0.024 %. The worst
STL-vs-STEP volume error across all 15 parts is 0.053 % (`agitator`), against
the 0.5 % I asked for.

### 1. Derived assembly order, with the swept-volume obstruction numbers

Each row is a 13–26-station straight approach, exact boolean against every
already-installed solid at every station; "SWEPT" is a true fused union of the
intermediate poses booleaned against those same obstacles.

| # | Operation | Approach | Station-max | Swept-union ∩ obstacles | Verdict |
|---|---|---|---|---|---|
| 1 | `meter_housing` in fixture | — | — | — | datum |
| 2 | igus JFM-2023-07 into the roof bore | **+Z**, 40 mm, 21 st | **0.0000** | **0.0000** | OK |
| 2′ | (same, from below) | −Z | 580.5963 at t = 6 | 2073.4860 | not possible |
| 3 | `brush_holder` + `brush_strip` radial slide-in | **θ = 148°, inboard**, 40 mm | **0.0000** | **0.0000** | OK |
| 4 | `pocket_disc`, hub up through the bearing | **travels +Z**, 40 mm | **0.0000** | **0.0000** | OK |
| 4′ | (same, from above) | −Z | 29564.7928 at t = 12 | 29707.9255 | not possible |
| 5 | `agitator` onto the Ø15 hex | **+Z**, 40 mm | **0.0000** | **0.0000** | OK |
| 6a | `count_windows` ×2/side, **from inside the chute bore, pushed out** | radial out, 12 mm | **0.0000** | **0.0000** | OK |
| 6a′ | (same, fitted from outside — control) | radial in | 36.6647 at t = 2 | 183.2984 | not possible (Ø5.9 window, Ø3.2 tunnel) |
| 6b | `sensor_boards` ×1/side into the cavity | **±Y inboard**, 20 mm | **0.0000** | **0.0000** | OK |
| 6c | `sensor_cover` ×1/side | **±Y inboard**, 25 mm | **0.0000** | **0.0000** | OK |
| 6d | motor+gearbox onto the plate | **travels +Z**, 40 mm | **0.0000** | **0.0000** | OK |
| 6e | PTFE thrust washer into its plate counterbore | **+Z**, 20 mm | **0.0000** | **0.0000** | OK |
| 6e′ | (washer fitted from below with the motor) | −Z | 316.6725 at t = 2.5 | 2541.2029 | not possible — the washer is **not** part of the motor sub-assembly |
| 6f | 4 × gearbox screws | +Z into the countersinks | — | — | **BLOCKING A-10** |
| 7 | drive cartridge (plate+motor+washer+2 covers+2 boards+4 windows) into the housing, 60 mm descent | **travels +Z** at −20…−24° of unlock | **0.0000 vs the housing side** | — | OK with the disc counter-indexed |
| 7′ | (same at 0 / −14 / −18 / −26°) | — | 258.7014 / 129.3507 / 33.2412 / 47.4874 | — | not possible |
| 7b | rotate the cartridge −22° → 0° to lock | rot | **0.0000 over −24.5141…+0.5141°** | — | OK |
| 8 | M3×6 stop pin, radial at θ = 51°, z = −353.25 | radial in | pin ∩ housing **4.3118** (Ø3.0 in a Ø2.6 thread-forming pilot), pin ∩ plate **0.0000** | — | OK |
| 9 | M3×4 grub, radial θ = 202.5°, z = −341.25 | radial in | continuous **Ø2.6 void r 2.75 → 52 = 0.0000** in disc, housing and every other solid | — | OK |
| 10 | `electronics_bay` onto the housing ribs | **−Y**, 40 mm | **0.0000** | **0.0000** | OK |
| 11 | `bay_lid` | **−Y**, 30 mm | **0.0000** | **0.0000** | OK, removable in situ |
| 11′ | (lid pushed inboard) | +Y | 4028.4361 at t = 27 | 18640.8270 | not possible, as designed |
| 12 | `hopper` down over the bay riser | **+Z**, 60 mm | **0.0000** | **0.0000** | OK |
| 13 | `top_plate` onto the hopper flange | **+Z**, 40 mm | **0.0000** | **0.0000** | OK |
| 14 | clip plate + blind-mate PCB | **+Z**, 30 mm | **0.0000** | **0.0000** | OK |
| 15 | `fill_cap` — rotate 90°, lift 12 mm, +Y 60 mm | 3 legs | 1.4338 / 0.0000 / 0.0000 | 25.8080 / 1.6059 / **0.0000** | OK, detent residual declared |
| 16 | `chute_plug` (ground only) | +Z | 206.0993 fitted | — | press fit; see NB-3 |
| 17 | `service_stand` (ground only) | — | ∩ every assembly solid = **0.0000** | — | OK |

All 15 exported printed parts appear in that order. Two order facts are
*forced*, not chosen, and the controls prove it: the bearing must go in from
above (2′ = 580.5963) and the disc must come up from below (4′ = 29564.7928),
so the disc can only be fitted before the drive cartridge.

**Cartridge service removal from the fully built machine** (members = plate +
motor + washer + 2 covers + 2 boards + 4 windows; obstacles = *every* other
solid, including the bay, lid, hopper, top plate and clip plate):

```
  unlock -22 deg + 60 mm descent                      : station-max 4.6955 mm3 (all of it pocket_disc, at the seat)
  same, with pocket_disc counter-indexed -22 deg      : station-max 0.0000 mm3
  same, with the machine sitting on the service_stand : cartridge ^ service_stand = 0.0000 mm3 at every station to 60 mm
```

The documented drop-out path is real, it is **0.0000 mm³** once the disc is
counter-indexed, and — new this round — it also clears the `service_stand`, so
the cartridge can be dropped with the machine in its own rest position.

### 2. Torque path — motor → gearbox → shaft → metering disc: **EXISTS and closes**

The shaft profile is a **nearest-surface** radial ray sweep at 1° (a
max-radius sweep hides a D-flat and reports a plain Ø6 shaft — printed here as
the method control, because that is exactly how r6 shipped a round bore).

```
 gearbox/motor solid            V = 69.936 cm3, bb z -418.450 .. -337.250
 shaft, nearest-surface radial ray at 1 deg:
     z -353.000 / -352.000 / -350.000 / -349.500 / -349.300 : r_min 2.998..2.999, r_max 3.000, flat arc 0 deg
     z -349.200 / -348.750 / -344.750 / -340.750 / -338.000 / -337.300 : r_min 2.500, r_max 3.000, flat arc 64 deg (171..234)
 disc D-BORE, rays from the axis outward at 1 deg:
     z -350.000 / -349.500 / -349.300 : r 3.049..3.050 round (lead-in)
     z -349.200 ... -335.800          : r_min 2.550, r_max 3.050, flat arc 64 deg (171..234)
 shaft flat starts z = -349.2500 (bisection 1e-4)   disc bore flat starts z = -349.2500 (bisection 1e-4)
 shaft top z = -337.250             disc bore ceiling z = -335.7500  -> 1.500 mm of shaft-end clearance
 FLAT-ON-FLAT ENGAGEMENT = 12.000 mm ; flat chord 2*sqrt(3.0^2 - 2.55^2) = 3.161 mm -> 37.93 mm2 of bearing
 drive torque 0.14 N*m x 5.18 x 0.90 = 0.6527 N*m -> 261.1 N at r = 2.5 mm -> 6.88 MPa on CF-PETG
 grub corridor (B2.2) continuous Dia2.6 void r 2.75 -> 52: disc 0.0000, housing 0.0000, every other solid 0.0000
 grub corridor CONTROL, disc mis-clocked +5 / +11.25 / +22.5 deg: 155.7955 / 160.0427 / 119.9572 mm3
 driver access (B2.3) Dia3.4 x 25 mm on the grub axis vs EVERY other solid: 0.0000
 bearing seat bore (meter_housing, z -330 .. -334.8): Dia 23.023 .. 23.030 on the igus JFM-2023-07 OD 23.00 (B9d <= 23.03 MET)
 thrust stack: washer top -350.800, disc bottom -350.750 -> 0.050 mm
 disc -> agitator: Dia15 hex spigot, seated 0.0000
 free-rotation scan of the seated cartridge vs meter_housing (1 deg, then bisected):
     -30..-25 : 184.787 / 150.951 / 116.919 / 82.497 / 47.487 / 11.692   -24..0 : 0.000 (free)   +1 : 11.692   +2 : 47.487
     +theta first contact +0.51415 deg ; -theta first contact -24.51415 deg ; two-sided free band 25.0283 deg
     with the M3x6 stop pin fitted: -theta free to -1.9430 deg -> bounded band 2.4573 deg (drop-out window at -20..-24 deg is blocked by 18.1 deg)
```

**B2.1, B2.2, B2.3 pass on the exports** and the reaction path (quarter-turn
latch stop in +θ after 0.5141° of lash, plus the radial stop pin in −θ) is
unchanged from r9. The grub-corridor control is the number that makes the
0.0000 meaningful: mis-clock the disc by one 22.5° station and the same ray
reads 119.9572 mm³.

### 3. Fastener grip and thread engagement, ray-measured on the r10 exports

| joint | measured | verdict |
|---|---|---|
| bay ribs → housing, **M3×20** | head bearing plane y = −64.000 (bay rib outer face; on-axis ray through the bay reads **no crossings** = clean through-bore, so the head can only bear there); first threadable housing material y = −50.080 (off-axis probe, so wall not pilot); pilot bottom y = −45.000. **GRIP 13.920 mm**, tip lands at −44.000, **ENGAGEMENT 5.080 mm** (all that is available) | **A-9 CLOSED**; r9's M3×12 reached −52.000 = 1.920 mm short, 0.000 mm of engagement |
| hopper skirt tabs → housing, **M3×8** | tab section (probed 2.5 mm off the screw axis) r 52.150…56.200 = **4.050 mm thick**; housing OD r = 52.000, pilot bottom r = **47.900** (4.100 mm deep). **GRIP 4.200 mm**, thread beyond grip **3.800 mm**, **0.300 mm of pilot to spare** | **r3 NB-2 CLOSED** (r9: 4.850 mm of thread into a 4.100 mm pilot → bottomed 0.750 mm before clamping) |
| top plate → hopper flange, **M3×10 + RX-M3×5.7** | 6 clearance holes measured at **r = 74.000, Ø3.200** (θ = 15/75/135/195/255/315); head bears at z = −233.550, insert bore top −238.550 → **GRIP 5.000 mm**; hopper insert bore Ø4.00 from −238.550 to **−244.545 = 5.995 mm deep** | B9b asks insert 5.7 + 0.3 = 6.000 → **5.995, short by 0.005 mm**. Call it met; see NB-5 for the BOM's r72.25 |
| clip plate → top plate, **4 × M2×10 + RX-M2×4** | clip-plate head pocket r = 2.000 (Ø4.000) down to the bearing shoulder z = **−177.600**, then Ø3.000; top plate Ø2.500 from −181.550 to −184.100; **insert bore Ø3.200 from −184.100 to −188.100 = 4.000 mm**. **GRIP 6.500 mm**, thread beyond grip **3.500 mm** into a 4.0 mm insert (87.5 %) | **B9a MET** (asks ≥ 3.2 mm; r6 measured 0.90 mm). N18 head clearance is now **0.100 mm/side** on the Ø3.8 M2 head (r6: 0.05) |
| gearbox flange → plate, **4 × M3×8** | hole Ø3.400 at r = 13.000 on the axes; **90° countersink, mouth Ø6.10 at z = −351.250 down to the shank hole at −352.600**; plate bottom (gearbox flange face) −355.250 | **BLOCKING A-10 — the BOM orders a cap head for a countersink** |
| bay lid, 4 × M3×8 self-tap | through-holes recovered from the export at (x, z) = (±29.000, −358.868) and (±29.000, −315.000) | OK, Ø12 driver access |
| stop pin M3×6 | pilot Ø2.60; modelled pin ∩ housing 4.3118 mm³ (thread-forming), ∩ plate 0.0000 | OK |

### 4. Tool-access corridors — largest clear driver diameter per fastener

Cylinder on the fastener axis, starting at the head-bearing plane and extending
**away** from the joint; diameters stepped 1.5/2.0/2.5/3.0/3.4/4.0/5.0/6.0/8.0/
10.0/12.0 mm; the largest with a **0.0000 mm³** exact boolean against every
other assembly solid is reported, with the first blocking size and the parts
that block it.

| ref | fastener | corridor | max clear driver | first blocking size → volume |
|---|---|---|---|---|
| F1 | 4 × M3 gearbox screws, +Z, **in situ** | 25 mm | **Ø0.0** | Ø1.5 → **15.7276** (`meter_housing` 12.7235 + `bearing` 3.0041), identical at all four holes |
| F1b | same four, **plate+motor sub-assembly** | 25 mm | **Ø8.0** | Ø10.0 → 2.1304 (thrust washer) |
| F2 | M3×4 grub, key from the disc OD (r 46 →) | 25 mm | **Ø3.4** | Ø4.0 → 11.9432 (`meter_housing`) |
| F2b | M3×4 grub, hand space outboard (r 53 →) | 40 mm | **Ø4.0** | Ø5.0 → 5.1053 (`meter_housing`) |
| F3 | M5 ball plunger, radial r = 63 → (θ = 67.5, z = −343.75) | 30 mm | **≥ Ø12.0** | — |
| F3b | M3×6 stop pin, radial r = 58.8 → (θ = 51) | 30 mm | **≥ Ø12.0** | — |
| F4 | 3 × M3×8 skirt tabs, θ = 30/105/225, radial | 25 mm | **≥ Ø12.0** each | — |
| F5 | M3×6 wiper end tab, radial r = 58.1 → (θ = 148) | 25 mm | **≥ Ø12.0** | — |
| F6 | 2 × M3×20 bay ribs, −Y from y = −64.05 | 28 mm | **Ø6.0** (lid on) / **Ø12.0** (lid off) | lid on: Ø8.0 → 74.7699 (`bay_lid`), both screws |
| F7 | 4 × M3×8 bay-lid screws, −Y from y = −92.05 | 25 mm | **≥ Ø12.0** each | — |
| F8 | 6 × M3×10 flange screws, r = 74.0, θ = 15+60k, +Z | 25 mm | **≥ Ø12.0** each | — |
| F9 | 4 × M2×10 mount screws (±19, ±19), +Z | 30 mm | **Ø4.0** each | Ø5.0 → 13.8367 (`clip_plate`'s own head pocket) |
| F10 | 4 × M2×6 sensor-cover screws, x = 34.5, z = −383.25 / −407.25, ±Y | 25 mm | **≥ Ø12.0** (upper pair) / **Ø6.0** (lower pair) | lower: Ø8.0 → 3.6757 (`retaining_plate_chute`) |

Every fastener except the in-situ gearbox screws takes at least a Ø4.0 driver.
**F1 in situ = Ø0.0 for the fourth round running**, and this round the build
notes finally say so (§6 item 1) — the motor is fastenable and removable only
as the plate+motor cartridge, which is what the quarter-turn latch is for.
With the machine on its own `service_stand`, the radial corridors are also
clear: grub Ø4.0 ∩ stand **0.0000**, stop pin Ø6.0 **0.0000**, plunger Ø6.0
**0.0000**, skirt tab Ø6.0 **0.0000**.

### BLOCKING A-10 — the four gearbox screws are specified as cap heads for a countersink, and a cap head jams the metering disc

`cad/BOM.md` fastener table: `| 4 | M3x8 SHCS | gearbox output flange ->
retaining plate |`. That is the **entire mechanical attachment of the motor to
the plate**, i.e. the first joint in the torque path. The plate does not have a
cap-head seat. Measured on `retaining_plate_chute_r10.stl`, directional radial
probes on the screw axis (13, 0), all four directions agreeing to 0.003 mm:

```
  z=-351.200  +x=   none  -x=   none  +y=   none  -y=   none      (above the plate)
  z=-351.300  +x=  3.050  -x=  3.050  +y=  3.049  -y=  3.049
  z=-351.600  +x=  2.750  -x=  2.747  +y=  2.747  -y=  2.747
  z=-351.900  +x=  2.450  -x=  2.447  +y=  2.448  -y=  2.448
  z=-352.200  +x=  2.150  -x=  2.147  +y=  2.148  -y=  2.148
  z=-352.600  +x=  1.750  -x=  1.750  +y=  1.749  -y=  1.749
  z=-353.000 .. -355.100 : 1.699..1.700 constant  (the Dia3.4 shank hole, to the flange face at -355.250)
```

That is a **90° included countersink, Ø6.10 at the mouth (z = −351.250) closing
to Ø3.40 at z = −352.600** — the seat for a 90° flat-head screw, not for a
Ø5.5 × 3.0 mm cap head. (`dispenser.py` L1752 cuts it as
`Cone(MOTOR_SCREW_CLR, 3.1, 1.4)`; the BOM row is emitted at L4607. The two
were never reconciled.) What a cap head does, measured:

```
  M3 SHCS head Dia5.5 x 3.0 bearing where the cone lets it bear (r = 2.75 -> z = -351.600, head top -348.600):
     at (+13,0) / (-13,0) / (0,+13) / (0,-13), STATIC at the assembled clocking:
        ^ pocket_disc = 8.8652 mm3 per screw   (^ retaining_plate_chute = 0.0000: the plate itself is fine)
  ONE INDEX of the disc over a static head (disc rotated, 3 deg steps):
     0 deg  8.8652 | 3  12.6219 | 6  19.8868 | 9  27.0514 | 12  33.8255 | 15  39.9987 | 18  45.3214 | 21  49.4066
    24 deg 49.4066 | 27 45.3214 | 30 39.9987 | 33 33.8255 | 36 27.0514 | 39 19.8868 | 42 12.6219 | 45  8.8652
     -> worst over one 45 deg spoke pitch: 49.4066 mm3 PER SCREW, and it never returns to zero
  the same test with an ISO 10642 M3 flat head (90 deg cone Dia6.0 -> Dia3.0, 1.5 mm, top flush at z = -351.300):
     0.0000 mm3 at (+13,0), (-13,0), (0,+13), (0,-13) against EVERY assembly solid,
     and 0.0000 mm3 at every disc angle 0..45 deg
```

Why it jams rather than merely rubs: the disc carries a **through** lightening
annulus over the bolt circle, measured by bisection at eight angles at
**r = 10.500 … 15.500** (5.000 mm wide), bridged by **8 spokes 22.5° wide**
(material at r = 13 spans θ 11.5–33.5, 56.5–78.5, 101.5–123.5, 146.5–168.5,
191.5–213.5, 236.5–258.5, 281.5–303.5, 326.5–348.5). The four screws sit in
window centres (θ = 0/90/180/270), so a proud head enters the annulus — but the
annulus is only 5.000 mm wide against a Ø5.5 head (0.25 mm of interference per
side, the 8.8652 mm³ above), and every spoke then sweeps straight into it
(49.4066 mm³). Vertically there is **0.500 mm** of air between the plate top at
the bolt circle (z = −351.250) and the disc underside (z = −350.750); a cap
head stands **2.650 mm** proud of that plane even seated as deep as the cone
allows.

So, as ordered: the machine cannot be closed up (8.8652 mm³ × 4 static
interference at the assembled clocking), and if it were forced together the
disc could not turn. **This is a one-line BOM fix** — M3×8 ISO 10642 / DIN 7991
90° countersunk, 2.0 mm hex — and the geometry already accepts it at
0.0000 mm³, which is why I am recording it as blocking-but-cheap rather than a
geometry defect. It must not be closed by narration: the fix has to re-print
the flat-head boolean at all four holes and at every disc angle.

Two smaller things fall out of the same joint and should be fixed with it:
- **Grip is 3.950 mm, not 2.900 mm.** With a flat head sunk flush at
  z = −351.300 the plate under the head is −351.300…−355.250; an M3×8
  countersunk screw (overall length includes the head) leaves **4.050 mm** of
  thread for the gearbox flange. State it in the BOM row so the next round does
  not "fix" it by lengthening the screw.
- The **F1b sub-assembly corridor is Ø8.0**, so the countersunk head is
  drivable at build time; **F1 in situ is Ø0.0** and stays that way.

### 5. Non-blocking, measured

- **NB-1 — the 4 × RX-M2×4 inserts can only be fitted from the underside of
  `top_plate`, and nothing says so.** Measured at (19, 19): Ø2.500 lead from the
  top face z = −181.550 down to −184.100, then the Ø3.200 × 4.000 mm insert
  bore (−184.100…−188.100), then a Ø4.800 relief shaft that stays open to
  z = −209.422. A Ø3.2 insert cannot pass the Ø2.500 lead, so it must go in
  from below, into a shaft **Ø4.800 × 21.3 mm**, while `top_plate` is still a
  loose part. That is a perfectly buildable sequence — it is just not written
  anywhere, and it is exactly the class of fact §6 of the build notes exists
  for. (The shoulder at −184.100 is a positive depth stop, which is good.)
- **NB-2 — `cad/BOM.md` says the flange screws are at r72.25; they are at
  r = 74.000.** Six holes, Ø3.200, θ = 15/75/135/195/255/315, clear span
  r 72.400…75.600 at every one. RT-19 class: a stated number the geometry does
  not contain.
- **NB-3 — the fitted `chute_plug` reads 206.0993 mm³ against
  `retaining_plate_chute`**, and withdrawal along −Z reads
  206.0993 / 204.1381 / 94.0070 / 92.8818 / 65.0334 / 0.0000 mm³ at
  0 / 2 / 5 / 10 / 20 / 30 mm. The plug does come out on a straight pull, so it
  is not an assembly blocker in my lane — but 206.10 mm³ is not all "the
  designed 0.3 mm press fit", and the granule-path critic's MAJOR this round
  attributes 122.596 mm³ of it to the tether anchor lug. Same defect, two
  measurements; I concur with their reading.
- **NB-4 — 0.5141° of plate-to-housing lash** at the drive-reaction stop
  (free band −24.5142…+0.5142°, bounded to 2.4573° with the stop pin). On a
  22.5° index that is 2.29 % of a station of angular error the first time the
  drive loads in each direction. Unchanged from r9, still absent from the build
  notes and from the count-contract text; one sentence, not a geometry change.
- **NB-5 — `service_stand` clearance is 8.000 mm.** Stand ground plane
  z = −426.450; lowest solid in the assembly is the **motor can at −418.450**
  (lowest *printed* material is `retaining_plate_chute` at −418.300); stand ∩
  every assembly solid = 0.0000 mm³; the support plane is the `meter_housing`
  bottom rim at z = −358.250 = the stand's top face, i.e. **printed structure,
  not the motor can** (B12.1's load-path clause). The 8.000 mm number is still
  not in the build notes.
- **NB-6 — B12.2's "0.000 mm³" is still not literally met for the fill cap.**
  Rotation leg 1.4338 mm³ instantaneous, 25.8080 mm³ over the swept union
  (station count differs from r3's 38.7708; same feature). This is N5's
  anti-rotation detent working as designed, and `BUILD-NOTES-r4.md` §11 item 3
  now declares it — accepted.
- **NB-7 — still no driver line in the BOM.** The M3×4 grub has to be pushed
  **43.00 mm** radially (housing outer r = 52 → pilot r = 9) down a Ø3.4
  channel with the disc indexed to θ = 202.5°, and there is no retrieval path
  if it is dropped in the chamber; the corridor takes a **Ø3.4** key at most.
  A ≥ 60 mm 1.5 mm hex key is still not a BOM row, and A-10 will add a 2.0 mm
  hex requirement. Carried from rounds 1, 2 and 3.
- **NB-8 — the round-3 §6 request to re-print §1/§2/§3 unchanged was answered
  by assertion, not by print.** `BUILD-NOTES-r4.md` §10 says the model asserts
  its own punch-list results and "a completed run is itself evidence". It is
  not, for a critic: the numbers that closed A-5, A-6, A-7 and the torque path
  do not appear anywhere in r4's notes, so I re-derived all of them from
  scratch (§1–§2 above). They all hold. Print them next round.

### 6. What I need to see next round to clear "assembly"

1. **A-10 closed:** `cad/BOM.md` naming a 90° countersunk M3×8 (ISO 10642 /
   DIN 7991) for the gearbox joint, with the head-fit boolean re-printed —
   **0.0000 mm³ at all four holes and at every disc angle over one 45° spoke
   pitch** — and the cap-head control (8.8652 static / 49.4066 swept) kept in
   the notes so the reason is legible. Grip stated as 3.950 mm with 4.050 mm of
   thread beyond it.
2. The insert-from-below fact (NB-1) and the r = 74.000 correction (NB-2) in
   the notes/BOM.
3. §1, §2, §3 and §4 of this critique **re-printed from the tools**, not
   asserted: 15/15 watertight, the order table's 0.0000s with their controls,
   12.000 mm of flat-on-flat, GRIP 13.920 / 4.200 / 6.500 / 5.000, and the
   F1 = Ø0.0 / F1b = Ø8.0 pair.
4. NB-4 (0.5141° of lash) and NB-5 (8.000 mm stand clearance) written into the
   service/count-contract text with those numbers.
