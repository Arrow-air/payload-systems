# REV-1 ROUND 6 — CRITIQUE (exports `r12`)

## count-sensor

**Verdict: PASS WITH COMPLAINTS. No blocking count-sensor item.** Every piece of
hardware `ELECTRONICS.md` §4.2–4.4 specifies is physically present in the r12
exports — ECO-3's four Ø3.2 apertures, ECO-9's 6.000 mm stagger, ECO-4's four
PMMA windows in bore-face seats, ECO-5's labyrinth ledge, and the emitter/
receiver board + cover + fastener features — and `cad/BOM.md` orders the analog
VBPW34FAS/OPA2320 chain with no TSSP4038 order line. **Nothing on my list is
spec'd-but-not-modelled.** Round 5's one FAIL (B4.2, the labyrinth walking the
clear lens 0.400 mm off the ECO-3 axis) is **closed by geometry**: I measure
0.0000 mm³ on both nominal beam axes with controls that fire.

Three complaints survive, all non-blocking, one of them new and not previously
reported by any critic: the **receiver photodiode sits 8.300 mm behind its tunnel
exit** while the emitter LED tip sits 0.500 mm in front of its own, so the
as-built LED→PD span is **42.800 mm** against §4.4's **32 mm** optical budget and
the headline **182× excess gain is optimistic by ≈2.6× before the ECO-5 vignette
and ≈3.6× after it**; ECO-9's A/B channels are **mirrored** relative to the
document, which inverts the sign of the published `x₀` solve (BUILD-NOTES-r6 §4
claims that solve is now "valid as written" — the magnitude is, the sign is not);
and ECO-4's window face is a flat chord plane recessed **0.000–1.748 mm** below
the curved Ø22 bore, not "flush", though nothing is proud of the bore.

### Method

Every number below is stdout from my own probes on the shipped `*_r12` exports.
I did not read `dispenser.py` and I did not take any number from
`BUILD-NOTES-r6.md`. Tools: `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`,
trimesh 5.0.0 (grid ray-casting + `contains` on the STLs), build123d 0.11.1 / OCC
(exact booleans on the STEPs), numpy 2.5.1, scipy 1.18.0.

```
retaining_plate_chute_r12: watertight True vol 63944.7284 bbox [[-55.3, -51.999, -418.3], [51.984, 51.999, -351.25]]
count_windows_r12   watertight True vol  103.8478 bodies 4 bbox [[26.05, -11.95, -401.199], [37.95, 11.95, -389.301]]
sensor_boards_r12   watertight True vol 1286.6835 bodies 2 bbox [[25.5, -28.5, -401.25], [43.5, 28.5, -389.25]]
sensor_cover_r12    watertight True vol 3198.1348 bodies 2 bbox [[22.4, -32.5, -409.35], [46.6, 32.5, -381.15]]
volumes from the STEPs: plate 63959.7322  cover 3198.1219  boards 1286.8333  windows 103.8909
dispenser_r12_assembly.stl: 24 bodies; bodies 16-19 = the 4 windows, 20-21 = the 2 covers, 22-23 = the 2 boards
```

Probe control (proves `contains` is not answering False to everything):

```
CONTROL: 8.1 % of 4000 uniform bbox points read INSIDE printed material (a probe that always says False reads 0.0 %)
```

### B4.1 — aperture count, position, diameter: **PASS**

I did not tell the probe where to look. 8 925 rays fired along +y over an
0.25 mm (x, z) grid spanning x 20…46, z −406…−385, then connected-component
labelled:

```
rays 8925  hits 46035
fully-clear cells (no material anywhere along +/-y): 287   clusters: 3
  cluster 1: cells  109  x 20.000..28.750 (c 24.375, span 9.000)  z -406.000..-405.250 (c -405.625, span 1.000)  area 6.8125 mm2   <- below the boss, not an aperture
  cluster 2: cells   89  x 28.000..30.000 (c 29.000, span 2.250)  z -393.750..-390.750 (c -392.250, span 3.250)  area 5.5625 mm2
  cluster 3: cells   89  x 34.000..36.000 (c 35.000, span 2.250)  z -399.750..-396.750 (c -398.250, span 3.250)  area 5.5625 mm2
```

Tunnel cross-sections, by x-ray crossings at fixed y (inner segment and outer
segment, both sides):

```
  beam A y=+13.000  crossings [22.0, 27.0, 30.2, 47.0]  tunnel x 27.000..30.200 (c 28.600, w 3.200)
  beam A y=+14.450  crossings [22.0, 27.0, 30.2, 47.0]  tunnel x 27.000..30.200 (c 28.600, w 3.200)
  beam A y=+14.550  crossings [22.0, 27.8, 31.0, 47.0]  tunnel x 27.800..31.000 (c 29.400, w 3.200)
  beam A y=+16.900  crossings [22.0, 27.8, 31.0, 47.0]  tunnel x 27.800..31.000 (c 29.400, w 3.200)
  beam A y=-13.000 / -14.400 : c 28.600 w 3.200   ;  y=-14.600 / -16.900 : c 29.400 w 3.200
  beam B y=+13.000 / +14.450 : c 34.600 w 3.200   ;  y=+14.550 / +16.900 : c 35.400 w 3.200
  beam B y=-13.000 / -14.400 : c 34.600 w 3.200   ;  y=-14.600 / -16.900 : c 35.400 w 3.200
aperture heights (z-rays at each segment axis):
  A inner x=28.6 y=+13.0: gap z -393.850..-390.650 (c -392.250, h 3.199)
  A outer x=29.4 y=+16.0: gap z -393.850..-390.650 (c -392.250, h 3.199)
  B inner x=34.6 y=+13.0: gap z -399.850..-396.650 (c -398.250, h 3.199)
  B outer x=35.4 y=+16.0: gap z -399.850..-396.650 (c -398.250, h 3.199)
  (chord at 0.800 off a segment axis reads h 2.771 = 2*sqrt(1.6^2-0.8^2) -> the tunnels are true circles)
```

| ECO-3 / ECO-9 spec | measured on `retaining_plate_chute_r12` | verdict |
|---|---|---|
| 2 apertures per side, 4 total | 4 (2 per side, 2 collinear pairs) | PASS |
| aperture axes x = 29 and x = 35 | straight-through lens centres **29.000 / 35.000**; segment axes 28.600 (inner) / 29.400 (outer) and 34.600 / 35.400 | PASS |
| Ø3.2 ± 0.1 | **3.200 × 3.199** every segment, all four tunnels | PASS |
| z = Z_SENSOR + 3.0 / Z_SENSOR − 3.0 | **−392.250 / −398.250** | PASS |
| **ECO-9 vertical stagger 6.0 mm** | **6.000 mm exactly** | PASS |
| chords symmetric about the bore axis (x = 32) | **−3.000 / +3.000** (r11 was −2.600 / +3.400) | PASS |

Web audit for the stagger: aperture A z −393.850…−390.650, aperture B
−399.850…−396.650, so the **web between the two apertures is 2.800 mm** and the
boss carries 9.900 mm of material above A and 12.139 mm below B (the boss+ears
span z −411.989…−380.750 = 31.239 mm, not ECO-3's 14 mm — it grew to carry the
board pocket and the cover ears).

### B4.2 — Ø2.0 × 60 mm beam clearance: **PASS (round-5 FAIL closed)**

Exact OCC booleans against the STEPs:

```
  beam A x= 29.000 z= -392.250  Dia2.0x60  ^plate    0.0000 | ^cover    0.1576 | ^boards   44.6106 | ^windows(PMMA)    5.9690 mm3
      optical span |y|<=26.5:                 ^plate    0.0000 | ^cover    0.0000 mm3
  beam B x= 35.000 z= -398.250  Dia2.0x60  ^plate    0.0000 | ^cover    0.0000 | ^boards   44.6106 | ^windows(PMMA)    5.9690 mm3
      optical span |y|<=26.5:                 ^plate    0.0000 | ^cover    0.0000 mm3
  aperture sweep on the nominal axes (^plate):
   A x= 29.0  Dia2.0=  0.0000  Dia2.2=  0.0000  Dia2.4=  0.0000  Dia2.6=  1.3728  Dia2.8=  4.0819  Dia3.0=  7.8809  Dia3.2= 12.7540
   B x= 35.0  Dia2.0=  0.0000  Dia2.2=  0.0000  Dia2.4=  0.0000  Dia2.6=  1.3728  Dia2.8=  4.0819  Dia3.0=  7.8809  Dia3.2= 12.7540
  CONTROLS:
    solid boss x=32, beam-A height     Dia2.0x60 ^plate   34.8162 mm3
    beam-A x at beam-B height          Dia2.0x60 ^plate   40.3992 mm3
    beam-B x at beam-A height          Dia2.0x60 ^plate   40.3989 mm3
    off-lens x=29.8 beam A             Dia2.0x60 ^plate    4.9576 mm3
    off-lens x=28.2 beam A             Dia2.0x60 ^plate    4.9675 mm3
```

r11 read **1.1932 mm³** on these axes and 0.0000 at x = 29.4/35.4. r12 reads
**0.0000 on the axes** and the two off-lens probes at ±0.8 mm read **4.9675 /
4.9576 mm³ — equal to 0.1 %**, which is the direct evidence that the lens is now
*symmetric* about 29.000 rather than displaced. The 0.1576 mm³ against
`sensor_cover` on beam A is 6.5 mm behind the emitter board (the punch list's
60 mm cylinder overruns both boards); over the emitter-to-detector span it is
0.0000, and I reproduce both numbers exactly as the build notes printed them.

**Complaint carried, unchanged:** the straight-through clear aperture is a **lens,
not a circle** — two Ø3.200 circles offset 0.800 mm:

```
   straight-through clear lens area = 5.5094 mm2 vs full Dia3.2 circle 8.0425 mm2 -> 68.5 % (-1.64 dB)
   (grid measurement above: 5.5625 mm2 at 0.25 mm quantisation, consistent)
   clear width in x = 2.400 mm, in z = 3.200 mm
```

So the optical aperture ECO-5 leaves is 68.5 % of the one §4.4 budgets, and the
"beam" is a 2.4 × 3.2 mm lens rather than the pencil §4.2/§4.3's chord arithmetic
assumes. Neither is disqualifying; both should be stated where 182× is stated.

### B4.5 — ECO-5 labyrinth: **PASS, and the sense defect is fixed**

```
   +Y step plane bisected: y =  14.4950
   -Y step plane bisected: y = -14.4950
   boss faces at x=32 (solid), y-crossings: [-17.0, -12.0, -11.0, 11.0, 12.0, 17.0]   -> boss face |y| = 17.000
   outer segment length = 17.000 - 14.500 = 2.5000 mm          (spec: outer 2.5 mm)
   inner segment centre 28.600 / outer 29.400 -> offset 0.800 mm; each ledge = 0.800 mm   (spec 0.8 +/- 0.1, B4.5 asks ledge >= 0.7)
```

Present on all four tunnels, both sides, both beams. The r11 defect (both sides
stepping **+x**, walking the lens to 29.400/35.400) is gone: the step is now
split −0.400 inner / +0.400 outer, so the ledge is unchanged at 0.800 mm and the
lens re-centres on the ECO-3 axis. **Note for the ECO text:** neither tunnel
segment is centred on x = 29.000 — 29.000 is the *midpoint* of the two segment
axes. ECO-5 as written ("offset the outer 2.5 mm by 0.8 mm") would put the inner
segment on 29.000 and the outer on 29.800; the built part is the better
interpretation, but ECO-5 should be amended to say so.

### B4.4 — ECO-4 window seat and discs: **PASS on the requirement that matters; two literal deviations**

```
  window body 0: bbox [26.05, 11.0, -395.1991]..[31.95, 11.95, -389.3009]  dia_x 5.9000 dia_z 5.8982 thickness_y 0.9500 vol 25.9619 centroid [29.0, 11.475, -392.25]
  window body 1: bbox [32.05, 11.0, -401.1991]..[37.95, 11.95, -395.3009]  ... centroid [35.0, 11.475, -398.25]
  window bodies 2, 3 = the -Y mirrors.   4 discs, total 103.8478 mm3
  seat section, x-crossings at fixed y (beam A, z = -392.25):
    y= 11.05 .. 11.95 : plate x 22.0, 26.0, 32.0, 47.0   -> seat void x 26.000..32.000 = Dia6.000 centred 29.000
    y= 12.05          : plate x 22.0, 27.0, 30.2, 47.0   -> the Dia3.200 inner tunnel takes over
  => seat Dia6.000, mouth plane |y| = 11.000, floor plane |y| = 12.000, DEPTH 1.000 mm
     disc Dia5.900 x 0.950 thick, inner face on |y| = 11.000 -> 0.050 mm/side bond gap, 0.050 mm back clearance
```

Nothing is proud of the bore — the check that actually protects the granule path:

```
   Dia 22.0 x 50 column on the chute axis: ^plate 0.0000 | ^windows 0.0000 | ^boards 0.0000 | ^cover 0.0000 mm3
   Dia 21.0 x 50 column:                   ^plate 0.0000 | ^windows 0.0000 | ^boards 0.0000 | ^cover 0.0000 mm3
   Dia 13.0 x 50 column:                   ^plate 0.0000 | ^windows 0.0000 | ^boards 0.0000 | ^cover 0.0000 mm3
   CONTROL Dia24 column (must eat the bore wall): 2842.5333 mm3
   bore-radius rays, 180 azimuths per plane: z=-388.0 min 10.9960 max 11.0000 | z=-395.25 min 10.9950 max 11.0000 | z=-402.0 min 10.9946 max 11.0000
   (the 10.995 is the inscribed-facet radius of the tessellated Dia22 cylinder, not a proud feature)
```

**Deviation 1 — seat depth.** B4.4 asks Ø6.0 × **0.4 ± 0.05 mm** deep; measured
**Ø6.000 × 1.000 mm**. B4.4 as written is self-contradictory (a Ø6 × 1 mm disc in
a 0.4 mm seat stands 0.6 mm proud, which the same test forbids). The part is
right and the punch-list line is wrong; record it, do not re-cut the seat.

**Deviation 2 — the 0.4 mm chamfer is still not modelled** (BUILD-NOTES-r6 §6
records it as attempted and withdrawn; `ELECTRONICS.md` §4.5 now carries a
matching CORRECTION block). I confirm it on the export: the seat is
straight-walled Ø5.999–6.000 through its full 1.000 mm depth. I also confirm
*why* it is hard — the seat mouth plane |y| = 11.000 is exactly tangent to the
Ø22 bore at x = 32, and my ray probe at x = 32 shows the doubled surface that
tangency produces:

```
   x= 32.00: plate y-crossings [-17.0, -12.0, -11.0, 11.0, 12.0, 17.0]     <- the +/-11.000 pair is the tangency
   x= 32.20: plate y-crossings [-17.0, -10.9971, 10.9971, 17.0]            <- clean bore wall 0.2 mm away
   contains() at (32, 0, -392.25) = False, (32, -11.5, -392.25) = False, (32, -13, -392.25) = True
```

The part is watertight with 0 non-manifold edges as shipped, so this is a
modelling hazard, not a defect in r12. **ECO-4 or the seat has to move**; my
recommendation is to sink the seat plane to |y| = 11.4 (0.4 mm outboard of the
tangent point) so a chamfer stops being tangent to anything.

**Deviation 3 (new, mine) — "flush with the chute wall" is only true at one
point.** The window face is a flat plane at |y| = 11.000; the bore is a Ø22
cylinder about x = 32. Over the Ø5.900 disc footprint the face is recessed below
the bore surface by:

```
   at x = 31.95 (disc edge nearest the bore crown): 11.000 - sqrt(11^2 - 0.05^2) = 0.0001 mm
   at x = 29.00 (aperture centre):                  11.000 - 10.5830           = 0.4170 mm
   at x = 26.05 (far disc edge):                    11.000 -  9.2521           = 1.7479 mm
```

So each window sits at the bottom of a Ø6 scallop up to **1.748 mm** deep, not
flush. Nothing is proud (checked above) so ECO-4's swab claim survives and the
granule path is untouched, but §4.5 measure 5's argument — "the fouling surface
*is* the chute wall" — is weakened: a 1.75 mm-deep pocket in the wall is a fines
trap that a rod-and-swab will not scour as cleanly as a flush face. Round 5
printed only the 0.417 mm figure at the aperture centre; the full range is above.

### B4.3 — boss envelope and motor clearance: **PASS**

```
  +Y boss verts (z -406..-385, y>=12): x 22.000..44.700  y 12.000..30.500  z -405.250..-385.750  (1414 verts)
  -Y boss verts:                        x 22.000..44.700  y -30.500..-12.000  z -405.250..-385.750
  boss+ear extent (x>=20, |y|>=12, z -412..-380): x 22.000..47.000
  boss x-min = 22.000  (B4.3 asks >= 22.0)
  min |SENSOR-BOSS vertex -> motor-body surface| = 8.4347 mm  at boss [26.0, 12.0, -392.25] -> motor [17.6, 11.236, -392.25]
  motor body surface, ray +x at y=0: x = 17.600 at z = -392.25, -398.25, -405.25 and -410.00
  boss x-min 22.000 vs the motor face at x = 17.600 -> CLEARANCE 4.400 mm   (B4.3 asks >= 4.0; this is measured, not predicted)
```

**Printed anyway, because it is the real minimum and it is not the boss:** the
chute tube outer wall, not the sensor boss, is the closest payload material to
the motor in this band.

```
  plate: ray -x at y=0, z=-392.25: crossings [19.001, 21.003, 43.0, 45.0] -> chute-tube OD reaches x = 19.001, wall thickness 2.002 mm
  min |any plate vertex in z -412..-380 -> motor surface| = 1.4000 mm at plate [19.0, 0.0, -405.25] -> motor [17.6, 0.0, -405.25]
```

**1.400 mm**, at the chute tube. (Round 5 reported 1.001 mm against a motor face
assumed at x = 18.000; the modelled motor can is actually at x = 17.600
throughout this band, so the correct number is 1.400.) ECO-3's "4.4 mm
clearance" headline describes the boss only.

### B4.6 — sensor-board cavity and the real boards: **PASS in function, still not ECO-3's pocket at x = 32**

```
   20x8x12 at x= 32.0 y= +22.0: ^plate  220.8000 | ^cover 0.0000 mm3
   20x8x12 at x= 33.0 y= +22.0: ^plate  124.8000 | 20x8x12 at x= 34.0: 28.8000 | at x= 34.5: 0.0000 | at x= 35.0: 28.8000 | at x= 36.0: 124.8000
   (identical at y = -22.0)
   pocket walls, ray +x at y=+22, z=-395.25: plate crossings [22.0, 24.3, 44.7, 47.0]  -> clear pocket x 24.300..44.700 = 20.400 mm wide
   pocket depth in y: boss face 17.000 -> cover inner face 27.000 = 10.000 mm ; pocket z -404.750..-385.750 = 19.000 mm
   boards ^ plate 0.0000 | boards ^ cover 0.0000 | windows ^ plate 0.0000 | cover ^ plate 0.0000 mm3
   board 0 (+Y emitter):  bbox x 25.500..43.500  y 17.500..28.500  z -401.250..-389.250  vol 794.929
   board 1 (-Y receiver): bbox x 25.500..43.500  y -28.500..-25.300 z -401.250..-389.250  vol 491.904
```

A clear 20 × 8 × 12 envelope exists, centred at **x = 34.500**, not ECO-3's
x = 32 (the obstruction at x = 22.000…24.300 is the inboard pocket wall). The
as-built architecture is a pocket in the plate closed by a printed
`sensor_cover`, which is better than ECO-3's "component pocket in the boss";
ECO-3 should be amended to the built geometry rather than the reverse.

Retention (ECO-12 / N3), measured:

```
   cover +Y through-holes found by grid ray-cast: hole 1 x 33.50..35.50 (c 34.500) z -408.00..-406.50 (c -407.250)
                                                  hole 2 x 33.50..35.50 (c 34.500) z -384.00..-382.50 (c -383.250)
   plate pilot behind each: ray -y at x=34.5, z=-407.25 -> first plate hit y = 25.500 (mouth |y| = 30.500) -> Dia1.6 blind pilot 5.000 mm deep
   min |board vertex -> cover surface| = 0.5000 mm ; cover clamp-post face at |y| = 29.000 vs board face 28.500
```

BOM orders `2 | 18 x 12 x 0.5 mm silicone pad`. **Nit:** a 0.5 mm pad in a
0.5000 mm modelled gap is **zero designed compression** — the pad closes r11's
0.0000 mm tangency complaint on paper but still gives no preload; 0.3–0.4 mm of
modelled crush (or a 0.8 mm pad) is what makes "clamped" true.

### B4.7 — BOM: **PASS**

```
$ grep -c TSSP4038 cad/BOM.md
1
| count PD x2 | Vishay VBPW34FAS (940 nm filtered PIN, 7.5 mm2) | ELECTRONICS 4.4 ASSUMPTION -- replaces the REJECTED TSSP4038 |  |
| count amp | TI OPA2320AIDR (dual, rail-to-rail, transimpedance) | ELECTRONICS 4.4 ASSUMPTION |  |
| count emitter x2 | Vishay TSAL6200 (940 nm, 34 deg) | ASSUMPTION |  |
| count windows x4 | Dia6 x 1.0 cast PMMA disc, sacrificial, bonded (UV-acrylic or CA) | ECO-4; laser-cut, PN ASSUMPTION |  |
| sensor-cover screws | 4x M2x6 self-tap into the boss ears | ECO-12 retention |  |
| 2 | 18 x 12 x 2.0 mm 2-layer sensor PCB | count emitter board (+Y) and receiver board (-Y), ECO-12 |
| 1 | UV-cure optical adhesive, 2 g | bonds the 4 PMMA windows into their bore-face seats (ECO-4) |
| 2 | 18 x 12 x 0.5 mm silicone pad | between the sensor-cover clamp posts and the board |
| sensor_cover (x2) | CF-PETG | 3.20 | 4.1 | ; | count_windows (x4) | PMMA | 0.10 | 0.1 |
```

The single TSSP4038 occurrence is in the *status* column recording the rejection,
not an order line. All five B4.7 items present.

### B4.8 — chute-bore continuity: **PASS** (printed under B4.4)

Ø22.0 / Ø21.0 / Ø13.0 × 50 mm columns on the chute axis all read **0.0000 mm³**
against plate, windows, boards and cover, with a Ø24 control at 2842.5333 mm³.

---

### NEW MAJOR COMPLAINT (non-blocking) — the receiver sits 8.3 mm behind its aperture, and §4.4's 182× does not survive it

No previous critic measured the *axial* position of the optical parts relative to
the tunnel mouths. Measured on `sensor_boards_r12`:

```
  emitter LED at beam A: x-extent at y=+18.0, z=-392.25: [26.5, 31.5] -> Dia5.000 centred x 29.000 ; z-extent [-394.749, -389.751]
  receiver PD  at beam A: x-extent at y=-25.8, z=-392.25: [25.8, 32.2] -> 6.400 mm wide centred x 29.000 ; z-extent [-394.200, -390.300] = 3.900 mm
  board 0 distinct y planes: 17.5, 25.8, 26.5, 28.5   -> PCB y 26.500..28.500 (2.0 mm), LED body y 17.500..26.500 (9.000 mm)
  board 1 distinct y planes: -28.5, -26.5, -25.3      -> PCB y -28.500..-26.500 (2.0 mm), PD package y -26.500..-25.300 (1.200 mm)
  boss outer face |y| = 17.000
  emitter LED tip plane |y| = 17.500 -> 0.500 mm air gap in front of the tunnel mouth
  receiver PD face plane |y| = 25.300 -> PD sits 8.300 mm BEHIND the tunnel exit
  as-built LED-tip -> PD-face span = 42.800 mm ; ELECTRONICS 4.4 budgets 32 mm (22 bore + 2 x 5 tunnel)
  as-built window-face -> window-face span = 22.000 mm ; tunnel |y| 11.000..17.000 = 6.000 mm per side (doc says 5 mm)
```

Good news first: the LED bodies are now centred on **x = 29.000 / 35.000**, i.e.
on the ECO-3 axes and on the re-centred lens (r11 had them at 29.800/35.800, on
the offset outer-tunnel axis). That defect is closed.

The problem is the asymmetry. The emitter is a 9 mm through-hole part that
reaches to within 0.500 mm of its tunnel; the receiver is a 1.200 mm SMD part on
a PCB at the same nominal depth, so its face is **8.300 mm** from the tunnel
exit. Two independent bounds on the cost, both mine:

```
  1) doc's own free-space method: (32/42.8)^2 = 0.5590 -> 182x becomes 102x ; x 0.685 for the ECO-5 lens -> 70x
  2) geometric capture: bundle half-slope bounded by the two Dia3.2 tunnel mouths 34.000 mm apart = 0.0941 rad (5.38 deg)
     -> spot diameter at the PD face 8.300 mm past the exit mouth = 4.762 mm (area 17.81 mm2)
     vs VBPW34FAS active 7.5 mm2 -> capture <= 42 %
```

Both land in the same place: the delivered photocurrent is of order **1/3 of
§4.4's number**, so the excess gain is ≈**50–70×**, not 182×, and the dust
tolerance §4.5 measure 2 advertises is ≈**98.0–98.6 % of light lost**, not
99.4 %. This is **not disqualifying** — 50× is still enormous against a 1 µA
threshold, and §4.4's own conclusion ("the threshold is set by amplifier offset
drift and by mechanics, not by noise") is unaffected. But 182× is quoted three
times as "the single biggest dust defence", it is the headline of §4.4's optical
budget, and it is the number the `beam_margin_pct` warn/fault thresholds
(<20 %/<5 %) are implicitly scaled against. **Fix it in one of two ways:** move
the PD forward (a through-hole PD or a 8 mm standoff/light-pipe puts the face at
the tunnel mouth and recovers most of it), or re-derive §4.4's table at the
as-built 42.800 mm and restate measure 2. Either way the CAD and the doc must
stop disagreeing about where the detector is.

### NEW MINOR — ECO-9's channels are mirrored, so the published `x₀` solve has the wrong sign

```
  ECO-9 text: "Beam A at x = +3.0 mm at the present Z; beam B at x = -3.0 mm, 6.0 mm lower"
  AS BUILT:   upper beam (Z -392.250) at x = 29.000 = bore axis -3.000
              lower beam (Z -398.250) at x = 35.000 = bore axis +3.000     -> MIRRORED
  => x0 = (h_A^2 - h_B^2)/12 returns -x0_true with the as-built A/B assignment
     r^2 = h_A^2 + (x0-3)^2 still returns r_true (the two sign errors cancel in the radius solve)
```

`BUILD-NOTES-r6.md` §4 states: *"The ECO-3 chords are now symmetric about the
bore axis again, so ECO-9's published `x₀ = (h_A² − h_B²)/12` solve is valid as
written."* The symmetry claim is true and I confirm it (−3.000/+3.000). The
"valid as written" claim is **half true**: the magnitude is right, the sign is
not, because the upper beam is on the −x side and the ECO puts beam A on +x.
Per-event `x₀` telemetry would be mirrored about the bore axis; the radius solve
is unaffected. Firmware/document constant, not geometry — but under RT-19/N15
that sentence in the build notes has to be corrected in the same round it is
written.

### Cross-document status: §4's stale sensing Z is now *recorded*, not yet *re-derived*

Re-measured by me on r12 (identical to r11, as expected — the beams did not
move):

```
  retaining-plate top face (release plane) Z = -351.250 ; chute mouth Z = -418.300
  beam A: Z -392.250 -> fall 41.000 mm -> v = 0.8969 m/s ; 26.050 mm above the chute mouth
  beam B: Z -398.250 -> fall 47.000 mm -> v = 0.9603 m/s ; 20.050 mm above the chute mouth
  ELECTRONICS 4.2 nominal (40 mm) v = 0.8859 m/s
  Dia 8: guaranteed worst-position chord  0.0000 mm (can miss both beams at |x0| >= 7) | best chord  8.000 ->  8.92 ms @v_A
  Dia11: guaranteed worst-position chord  9.2195 mm -> 10.41 ms @doc, 10.28 ms @v_A, 9.60 ms @v_B | best 11.000 -> 12.26 ms @v_A
  Dia12: guaranteed worst-position chord 10.3923 mm -> 11.73 ms @doc, 11.59 ms @v_A, 10.82 ms @v_B | best 12.000 -> 13.38 ms @v_A
  Dia13: guaranteed worst-position chord 11.5326 mm -> 13.02 ms @doc, 12.86 ms @v_A, 12.01 ms @v_B | best 13.000 -> 14.49 ms @v_A
  ECO-9 dt_mid for the measured 6.000 mm stagger: 6.536 ms @doc v, 6.461 ms @v_A (doc prints 6.54 ms)
```

`ELECTRONICS.md` §4 now carries a CORRECTION block (dated rev-1 r12) that states
the 49.1 mm error, the 41.000/47.000 mm falls, v_A/v_B, the Ø11 margin moving
7 % → 6.0 % and Δt_mid 6.54 → 6.461 ms. That is the honest half. **The §4.2 and
§4.3 tables themselves are still computed from 40 mm** and the correction block
says so. Acceptable for a CAD round; it must be closed before B1 freezes any
threshold, and it is the one item where the shipped document still contains
numbers it knows are wrong.

### Ledger

| item | required | measured on r12 | verdict |
|---|---|---|---|
| B4.1 aperture count / position / Ø | 4 × Ø3.2 ± 0.1 at (29, Z+3) and (35, Z−3) | 4 × Ø3.200/3.199, lens axes **29.000 / 35.000**, z **−392.250 / −398.250** | PASS |
| ECO-9 stagger | 6.0 mm | **6.000** | PASS |
| chord symmetry about the bore axis | ±3.0 | **−3.000 / +3.000** | PASS (r11 was −2.600/+3.400) |
| B4.2 Ø2.0 × 60 beam clear | 0.000 mm³ | **0.0000** both axes, controls 34.8162 / 40.3992 / 40.3989 | PASS (r11 FAIL 1.1932 closed) |
| B4.3 boss x-min | ≥ 22.0 | **22.000** | PASS |
| B4.3 boss → motor face | ≥ 4.0 mm | **4.400** (motor face measured at x = 17.600) | PASS |
| B4.4 nothing proud of the bore | 0.000 mm³ | Ø22/Ø21/Ø13 columns **0.0000**, Ø24 control 2842.5333 | PASS |
| B4.4 seat Ø6.0 | Ø6.0 ± 0.1 | **Ø6.000**, disc Ø5.900 × 0.950 | PASS |
| B4.4 seat 0.4 mm deep + chamfer | 0.4 ± 0.05, chamfered | **1.000 mm, straight-walled** | deviation, recorded in 3 places |
| B4.4 face flush at \|y\| = 11.0 | ± 0.05 | plane **11.000**; recess below the curved bore **0.0001…1.7479 mm** | PASS on the plane, "flush" overstated |
| B4.5 labyrinth offset / ledge / outer length | 0.8 ± 0.1 / ≥ 0.7 / 2.5 | **0.800 / 0.800 / 2.5000**, all four tunnels, split ±0.400 | PASS |
| B4.6 20 × 8 × 12 cavity | 0.000 mm³ | **0.0000 at x = 34.5**; 220.8000 at x = 32; real boards 0.0000 | PASS in function |
| B4.7 BOM | no TSSP4038 order; VBPW34FAS ×2, OPA2320, TSAL6200 ×2, 4 × PMMA | all present, 1 TSSP4038 string in a status cell | PASS |
| B4.8 chute continuity | 0.000 mm³ | **0.0000** | PASS |
| ECO-12 / N3 board retention | ≥ 8 mm² bearing, driver access | 18 × 12 board face, 2 × Ø1.6 × 5.000 mm pilots per side, 0.5000 mm pad gap | PASS, nit on preload |
| §4.4 optical span | 32 mm | **42.800 mm** LED tip → PD face; PD **8.300 mm** behind its aperture | **MAJOR complaint, non-blocking** |
| §4.4 excess gain | 182× | **≈102×** by the doc's own method, **≈70×** with the ECO-5 lens, ≤42 % geometric capture | complaint |
| ECO-9 channel assignment | beam A at +3.0 | upper beam at **−3.000** — mirrored; `x₀` sign inverted | minor, doc/firmware |

### What I am asking for in round 7

1. **Reconcile the detector depth with §4.4** — either move the PD face to the
   tunnel mouth (through-hole PD, standoff or light pipe) or re-derive §4.4's
   optical budget and §4.5 measure 2 at the as-built **42.800 mm** and print the
   corrected excess gain. Non-blocking either way; do not ship 182× unqualified.
2. **Correct the ECO-9 sign** in `ELECTRONICS.md` §4.3 (and the build-notes
   sentence that calls the solve "valid as written"): the upper beam is at
   bore-axis **−3.000**.
3. **Amend ECO-3/ECO-5 to the built geometry** — boss/pocket at x = 34.500 under
   a cover, not a pocket in the boss at x = 32; labyrinth split ±0.400 about the
   nominal axis, not +0.800 on the outer segment; and state the **68.5 %** lens.
4. **Decide ECO-4's seat**: either sink the seat plane to |y| ≈ 11.4 so the
   chamfer is no longer tangent to the Ø22 bore, or delete the chamfer from the
   ECO. State the **0.000–1.748 mm** scallop where §4.5 measure 5 says "flush".
5. Give the sensor-board pad **real crush** (0.3–0.4 mm), or say in the BOM that
   the joint is a locating pad, not a clamp.

None of the five blocks the round. **RT-3 stays closed.**

## granule-path

**Verdict: PASS with complaints — 0 blockers, 0 regressions on the rev-0
fragment-jam mandate, 3 MINOR + 2 NITs.** Both round-5 granule-path findings are
closed and I reproduce the closures independently: the **MAJOR** (README /
`docs/DESIGN.md` §4.5 still publishing the pre-B8 fragment-jam story) is
rewritten against measured numbers with the r6-era text kept as dated history,
and **MODERATE 1** (22.00 mm² of granule bed open to the sky through two
2.2 × 5.0 mm cable-tie slots, plus a 12-column self-check that could not see
them) is closed by geometry and by a grid scan — my own 0.25 mm scan reads
**32.50 mm² unroofed on r11 → 7.31 mm² on r12**, largest passing sphere
**Ø2.500 → Ø0.707 mm**. **MODERATE 2** (publish the shear-backstop bound) is
also actioned: both constructions are now in `docs/DESIGN.md` §4.5 with the
conservative one declared as the shipped bound. One genuine granule-path
*improvement* this round was booked as an assembly item and nobody credited it
here: the r11 bay-screw pilots opened **2.79 mm² into the granule transit gap**
(z −338.20…−336.00); on r12 that is **0.00 mm²**.

### Provenance

- Measured by me on `cad/exports/*_r12.stl` / `*_r12.step` with
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`, trimesh 5.0.0,
  numpy 2.5.1, scipy 1.18.0, build123d 0.11.1. Nothing imported from
  `dispenser.py`; I read that file only to *name* two features after I had
  already measured them (`PLUNGER_A = 67.5`, `GRUB_A = 202.5`, `CAP_SEAL_R =
  25.0`).
- md5 of the r12 STLs I measured (mine, computed here, matching BUILD-NOTES-r6
  §0 where it lists them):

```
agitator_r12.stl              8cb2f51f1358fd2b3ecdf8f49abbea3e
bay_lid_r12.stl               5216bd4550f20cc7d3c33e5bfdf1b086
brush_holder_r12.stl          ad2343fea8807cf4a998596e939e7308
chute_plug_r12.stl            88c344f8264272d216eb82f5bbb3c59e
count_windows_r12.stl         dfe57d4da5504b302f71422427f90918
electronics_bay_r12.stl       5b32d7d66710be69a135b3b3e9a21b60
fill_cap_r12.stl              0978d874b3b6fbea40ca9c16615c50b7
hopper_r12.stl                fdc1ab2e84884b5df4fa562ce9715331
meter_housing_r12.stl         eda2945b79fc4ad6a05e97c048beac14
pocket_disc_r12.stl           d02b663b6ae5cc8086ebb3a76288762e
retaining_plate_chute_r12.stl 88ab8264f05d1e2a6e9f7b6ab00fc328
sensor_boards_r12.stl         27bf20d7769c8ad5fca603b20b97637c
sensor_cover_r12.stl          bf43d5c8cdb35fa231988491fba56072
service_stand_r12.stl         2c88381d257cba8afe2d6c74baa7fae8
top_plate_r12.stl             695a6ebb534c178bbd0765b9b05b083f
```

- **BUILD-NOTES-r6 §0's byte-identity claim is true and understated.** Nine of
  fifteen parts are byte-identical r11 → r12: `pocket_disc`, `brush_holder`,
  `hopper` (the three it names) **and** `agitator`, `chute_plug`,
  `count_windows`, `bay_lid`, `electronics_bay`, `service_stand`. The six that
  changed are `meter_housing`, `retaining_plate_chute`, `top_plate`,
  `fill_cap`, `sensor_cover`, `sensor_boards` — four of which are on or beside
  the granule path, so that is where I spent the scan budget.
- **Where the changed parts changed** (vertex-set diff, r11 vs r12, my probe):

```
meter_housing: 103.623 -> 103.819 cm3
   NEW  630 verts  z -346.350..-335.850  r 48.216..63.040  theta 64.5..288.2
   GONE 648 verts  z -346.950..-335.850  r 46.999..63.082  theta 64.0..288.7
retaining_plate_chute: 71.850 -> 63.945 cm3
   NEW 5467 verts  z -416.800..-360.750 x -34.999..43.500 y -48.000..35.000
   GONE 2276 verts z -410.750..-390.650 x  27.400..43.500 y -24.999..24.999
top_plate: 95.299 -> 95.550 cm3   NEW 96 verts z -238.550..-228.950, y -70.5..-47.0
fill_cap: 7.347 -> 7.545 cm3      NEW 12 verts z -233.850..-228.200
sensor_boards / sensor_cover: the ECO-5 lens split, x -0.800 mm, |y| >= 17.5
```

  The r11 `GONE` set for `meter_housing` reaches **r = 46.999**, i.e. r11 had
  material cut at the chamber bore; the r12 `NEW` set stops at **r = 48.216**.
  That is the A-12 pilot moving out of the chamber wall, and it is the only
  granule-path-relevant part of that part's delta (see the aperture census
  below). The `retaining_plate_chute` delta is entirely at z ≤ −360.75, i.e.
  **9.5 mm below the plate top face and 6.25 mm below the exit-port bottom** —
  the duct network never comes up into the metering plane.

### Independent mesh census (r12)

```
agitator_r12.stl                    wt=True wind=True euler=     2 bodies=  1 vol_cm3=     4.288 mult={2: 4086}
bay_lid_r12.stl                     wt=True wind=True euler=   -10 bodies=  1 vol_cm3=     8.598 mult={2: 4614}
brush_holder_r12.stl                wt=True wind=True euler=     0 bodies=  1 vol_cm3=     3.544 mult={2: 918}
chute_plug_r12.stl                  wt=True wind=True euler=    -2 bodies=  1 vol_cm3=     6.718 mult={2: 3507}
count_windows_r12.stl               wt=True wind=True euler=     8 bodies=  4 vol_cm3=     0.104 mult={2: 3000}
electronics_bay_r12.stl             wt=True wind=True euler=    -8 bodies=  1 vol_cm3=    21.175 mult={2: 15027}
fill_cap_r12.stl                    wt=True wind=True euler=     0 bodies=  1 vol_cm3=     7.545 mult={2: 4593}
hopper_r12.stl                      wt=True wind=True euler=   -14 bodies=  1 vol_cm3=   109.423 mult={2: 16992}
meter_housing_r12.stl               wt=True wind=True euler=    -8 bodies=  1 vol_cm3=   103.819 mult={2: 17397}
pocket_disc_r12.stl                 wt=True wind=True euler=   -30 bodies=  1 vol_cm3=    72.661 mult={2: 36963}
retaining_plate_chute_r12.stl       wt=True wind=True euler=   -76 bodies=  1 vol_cm3=    63.945 mult={2: 50517}
sensor_boards_r12.stl               wt=True wind=True euler=     4 bodies=  2 vol_cm3=     1.287 mult={2: 3108}
sensor_cover_r12.stl                wt=True wind=True euler=    -4 bodies=  2 vol_cm3=     3.198 mult={2: 3540}
service_stand_r12.stl               wt=True wind=True euler=     0 bodies=  1 vol_cm3=   103.892 mult={2: 1656}
top_plate_r12.stl                   wt=True wind=True euler=   -38 bodies=  1 vol_cm3=    95.550 mult={2: 33630}
dispenser_r12_assembly.stl          wt=True wind=True euler=  -193 bodies= 24 vol_cm3=   579.898 mult={2: 213663}
```

**15/15 part STLs watertight, every edge shared by exactly two faces (no key
other than `2` in any multiplicity dict = 0 non-manifold and 0 open edges),
assembly 24 bodies watertight.** B10 holds on the shipped exports, reproduced,
not quoted. (`meter_housing` euler −12 → −8 and `retaining_plate_chute` −48 →
−76 are the detent/pilot rework and the 14 duct bores.)

### The full journey, hopper → pocket → exit, re-measured on r12 vs the Ø13 worst case

| # | station | measured on r12 | vs the Ø13 worst-case granule |
|---|---|---|---|
| 1 | fill route (cap removed), axis (0.00, 43.45) | Ø13 sphere dropped z −245 → −320 at 1 mm vs `hopper` + `top_plate`: **74/76 stations clear**; first contact z = −319 (centre-to-surface 6.463) and −320 (6.088) = the 68° funnel wall, not an obstruction | unchanged by the new tie bridges |
| 2 | barrel / funnel | funnel wall reached at centre radius 49.95 vs measured wall; no step | 10.8 × D_max at the barrel |
| 3 | sump outlet | edges bisected on r12: **θ 130.0000 → 250.0000 = 120.0000°**, radial **r 20.0000 → 46.9926 = 26.9926 mm**, area **1893.7 mm²** → equivalent circular orifice **D 49.10 mm** | **26.9926/13.0 = 2.076 × D_max** — N10 plateau, unchanged |
| 4 | deflector nose (rigid) | underside **1.500 mm** above the disc top at r = 20.25, 20.4, 20.5, 21, 22, 26, 30, 34, 38, 42, 46.0, 46.5, **46.70**; rail 7.450 at r ≤ 20.00 and r ≥ 46.90 | covers r **20.25…46.70** (see NIT 1) |
| 5 | bristles (compliant) | assembly body 10: **312.153 mm³**, z −335.550…−328.160 → tip **+1.200 mm** above the disc top | leads the rigid nose by 0.300 mm ✔ |
| 6 | entry ramp (overfill relief) | ceiling **10.500 @ θ 130** → 10.240…10.296 @ 129 → 9.158…9.249 @ 125 → 7.861…7.939 @ 120 → 5.269…5.320 @ 110 → 3.972…4.010 @ 105 → 2.676…2.700 @ 100 → 1.639…1.653 @ 96 → **1.500 @ ≤ 95**, at r = 20.5/24.5/32/39.5/45.5/46.5 | relief runs 130 → 95 **before** the covered arc; nothing enters unramped |
| 7 | transfer arc | roof underside **1.500 mm** at every one of 6 radii × 22 angles (θ = 95, 90, 80, 60, 45, 30, 20, 10, 0, 350, 330, 320, 316, 313, 311, **310**, 309, 308, 305, 300, 290, 270); window ramps back open at 255 (7.589–7.801) and 251 (9.941–10.071), fully open at 250 | seated crown is 1.500 **below** the disc top → 3.000 mm clear |
| 8 | pocket | bore **r 7.498** at depths 2.00/4.00/8.00/12.00/13.90/13.99 (180/180 azimuths each); 45° chamfer **9.497 @ 0.00, 9.297 @ 0.20, 8.992 @ 0.50, 8.489 @ 1.00, 7.992 @ 1.50, 7.498 @ 2.00**; 8 pockets, ~26° of open arc each at the PCD | 2.00 mm diametral clearance |
| 9 | exit port | bore **r 7.998** over z −352.000…−354.200, chamfer 8.697 @ −351.30 / 8.390 @ −351.60, **first plate material at the top face r = 8.747** | 3.00 mm diametral clearance |
| 10 | drop tube | **r_min 10.994 mm at z = −401.00** over z −355…−405 (180 azimuths × 51 heights, `retaining_plate_chute` + `count_windows` + `sensor_cover` + `sensor_boards` merged) → **Ø21.989 continuous** | Ø13 lateral envelope **±4.49 mm, symmetric** |

**B1 roof section on r12**, 120 probes (θ = 300/305/308/309/310/311/313/316/320/
330/350/0/20/45/90 × r = 20.5/24.5/30/32/36/39.5/44/46.5): **9.000 mm at every
one of the 120 probes; worst = 9.000 mm at θ = 300, r = 20.5.** The r6-era
0.000 mm slot at θ = 310 stays gone.

**Ø13 free-fall envelope in the parallel chute** (signed distance, z −362…−403
at 0.5 mm, merged plate + windows + cover + boards):

```
   centre offset +0.00 mm in +x: worst centre-to-surface 10.993 mm at z  -398.50 -> clearance +4.493 mm; centre inside material 0/83
   centre offset +3.50 mm in +x: worst centre-to-surface  7.498 mm at z  -362.00 -> clearance +0.998 mm; 0/83
   centre offset +4.49 mm in +x: worst centre-to-surface  6.508 mm at z  -362.00 -> clearance +0.008 mm; 0/83
   centre offset +4.60 mm in +x: worst centre-to-surface  6.398 mm at z  -362.00 -> clearance -0.102 mm
   centre offset -4.49 mm in +x: worst centre-to-surface  6.507 mm at z  -403.00 -> clearance +0.007 mm; 0/83
```

Identical to r11 — the ECO-5 lens split (boards and cover moved 0.800 mm in −x)
did not touch the fall envelope, because both parts stay at |y| ≥ 17.5 where the
bore only needs 11.0.

**Seated-granule transit (B8.5), Ø13 sphere at centre z = −344.750 carried round
the PCD, 360 stations, r12 parts:**

```
   vs meter_housing         min surface distance from the granule centre  9.500 mm -> clearance  +3.000 mm; centre-inside 0/360
   vs brush_holder          min surface distance from the granule centre  9.500 mm -> clearance  +3.000 mm; centre-inside 0/360
   vs hopper                min surface distance from the granule centre 22.722 mm -> clearance +16.222 mm; centre-inside 0/360
   vs agitator              min surface distance from the granule centre 19.050 mm -> clearance +12.550 mm; centre-inside 0/360
   vs retaining_plate_chute min surface distance from the granule centre  6.500 mm -> clearance  +0.000 mm; centre-inside 0/360  (the granule resting ON the plate, tangent)
```

**New check this round — the duct network never breaks into the granule path.**
`retaining_plate_chute` lost 7.905 cm³ to 14 duct bores, so I re-scanned the two
surfaces a granule touches:

```
   plate-top through-scan (0.25 mm plan grid, r 12..48, rays from z = -340 downward):
      r12: 868.06 mm2 open in 21 patches   r11: 868.06 mm2 open in 21 patches   -- IDENTICAL, patch for patch
      largest patch = 200.31 mm2 at 0.00..7.99 mm from the chute axis (the Dia16 exit port = 201.06 mm2)
      the two arc patches under the disc (134.88 + 119.38 mm2) sit at r 19.50..23.50, covered by solid disc
      annulus (disc voids close at r = 15.5, pockets start at r = 24.5)
   thinnest wall from the Dia22 drop-tube bore to the nearest void: 1.995 mm at z = -378.5, theta = 236.0
      (bore r 10.997 -> next void at r 12.993)
```

Zero new openings in the plate top face, and the duct leaves **1.995 mm** of
wall around the drop tube — on this package's own 1.95 mm minimum, not under it.

### Adversarial fragment construction — re-derived from scratch on r12

All inputs are my own r12 probes: bore r 7.498, chamfer 45° from (7.498, −2.000)
to (9.497, 0.000), plate top **14.500 mm** below the disc top, nose/roof plane
**+1.500**, port bore 7.998. **σ = 0.36 MPa and µ = 0.4 remain carried
ASSUMPTIONS** (US4172714-derived; closure = IFDC S-115). Drive re-derived from
the BOM motor: `0.14 N·m × 5.18 × 0.90 = 0.6527 N·m ÷ 0.032 m` = **20.4 N at the
pocket lip in recovery, 12.2 N at the 60 % metering current**.

**(a) Fragment nested on a seated granule, settled against the measured pocket
wall** (my construction rolls the fragment outboard on the granule until it
touches the bore/chamfer polyline and takes the lowest feasible seat — a
stricter statement than r5's tangent-line solve, which is why the mid-size
crowns come out 0.05–0.6 mm lower):

```
   crown height above the disc top (nose/roof plane = +1.500)
   d_frag |   D13 centred | D13 seat+1.00 | D13 seat-1.00 |   D12 centred | D12 seat+1.50 | D12 seat-1.50
    D 2.0  |        -3.255 |        -1.901 |        -6.755 |        -4.897 |        -2.601 |        -7.500
    D 3.0  |        -1.206 |        -0.269 |        -2.620 |        -2.497 |        -1.000 |        -6.755
    D 4.0  |        +0.440 |        +1.026 |        -0.518 |        -0.689 |        +0.404 |        -2.620
    D 4.5  |        +1.118 |        +1.621 |        +0.374 |        +0.116 |        +1.026 |        -1.501
    D 5.0  |        +1.750 |        +2.197 |        +1.137 |        +0.857 |        +1.621 |        -0.518
    D 5.5  |        +2.355 |        +2.762 |        +1.821 |        +1.526 |        +2.197 |        +0.378
    D 6.0  |        +2.943 |        +3.323 |        +2.464 |        +2.157 |        +2.761 |        +1.205
    D 7.0  |        +4.083 |        +4.437 |        +3.677 |        +3.352 |        +3.864 |        +2.616
    D 8.0  |        +5.207 |        +5.541 |        +4.835 |        +4.494 |        +4.944 |        +3.876
   largest fragment that clears the 1.500 mm nose, D13 centred   : D 4.799 ; outer reach 7.765 vs port bore 7.998 -> margin +0.233 mm ; centre (u 5.366, z -0.900), roll 37.1 deg
   largest fragment that clears the 1.500 mm nose, D13 seat+1.00 : D 4.397 ; outer reach 7.925 -> +0.073 mm ; roll 32.9 deg
   largest fragment that clears the 1.500 mm nose, D13 seat-1.00 : D 5.260 ; outer reach 7.646 -> +0.352 mm
   largest fragment that clears the 1.500 mm nose, D12 centred   : D 5.480 ; outer reach 7.606 -> +0.392 mm
   largest fragment that clears the 1.500 mm nose, D12 seat+1.50 : D 4.897 ; outer reach 7.735 -> +0.263 mm
   largest fragment that clears the 1.500 mm nose, D12 seat-1.50 : D 6.194 ; outer reach 7.524 -> +0.474 mm
```

This agrees with the r5 table to **≤ 0.001 mm at D7.0 and D8.0** and to
0.05–0.06 mm at D5.0/D6.0; the escape thresholds land at **Ø4.799 (D13 centred)
/ Ø4.397 (D13 seat +1.00)** against r5's 4.740 / 4.384 — same answer from a
different construction. **Every escapee still fits the exit port**, the tightest
anywhere on the exit path being **+0.073 mm** (D13 seat +1.00). B8's gain over
r6 is held: a Ø5.0 fragment (crown +1.750 centred, +2.197 at the worst seat) and
a Ø6.0 (+2.943 / +3.323) are both **above** the 1.500 mm nose, i.e. contacted,
not passed.

**(b) The wedged sliver that must be sheared** — sliver of radial width w in the
crescent between a seated Ø13 granule and the measured Ø14.996 bore, sheared at
the measured 1.500 mm nose/roof plane, 90° conforming shard on the **mean**
crescent radius:

```
      w     x_inner  y_seat   depth   height_to_shear  half-angle  self-lock  arc90(mm)  A(mm2)   F(N)   x20.4N  x12.2N
    1.000    6.498   0.161   7.839       9.339        0.71   YES       10.99    10.99    3.96    5.16x   3.08x
    1.500    5.998   2.505   5.495       6.995       11.33   YES       10.60    15.90    5.72    3.56x   2.13x
    2.000    5.498   3.467   4.533       6.033       16.12   YES       10.21    20.41    7.35    2.78x   1.66x
    2.500    4.998   4.156   3.844       5.344       19.87   YES        9.81    24.54    8.83    2.31x   1.38x
    2.793    4.705   4.485   3.515       5.015       21.81    no        9.58    26.77    9.64    2.12x   1.27x
    3.000    4.498   4.692   3.308       4.808       23.11    no        9.42    28.26   10.18    2.00x   1.20x
    4.000    3.498   5.479   2.521       4.021       28.72    no        8.64    34.54   12.44    1.64x   0.98x
    5.000    2.498   6.001   1.999       3.499       33.70    no        7.85    39.25   14.13    1.44x   0.86x
   WIDEST SELF-LOCKING SLIVER: w = 2.791 mm, seats 4.483 above the granule centre (3.517 below the disc top),
     must be >= 5.017 mm tall to reach the shear plane; A = 26.75 mm2, F_shear = 9.63 N -> 2.12x recovery, 1.27x normal
   shearable-section bound: 56.7 mm2 at recovery, 33.9 mm2 at normal current; whole pocket bore = 176.6 mm2
   180 deg conforming shard   at w=2.791: A  53.51 mm2, F 19.26 N -> 1.06x recovery, 0.63x normal
   full-ring crescent         at w=2.791: A 107.02 mm2, F 38.53 N -> 0.53x recovery, 0.32x normal
   MODEL's own crescent convention (arc on the INNER radius, not the mean): arc90 7.39 mm, A 20.64 mm2, F 7.43 N -> 2.75x / 1.64x
   crush at the measured section: D5.0 19.63 mm2 -> 7.07 N (2.89x/1.73x); D6.0 28.27 -> 10.18 N (2.00x/1.20x);
                                  D7.0 38.48 -> 13.85 N (1.47x/0.88x); whole D13 granule 132.73 -> 47.78 N (0.43x/0.26x)
```

**Shear-margin headline, reproduced on r12: the worst self-locked sliver the
pocket can hold (w = 2.791 mm, ≥ 5.017 mm tall) needs 9.63 N; the drive delivers
20.4 N in recovery and 12.2 N at normal current → 2.12× / 1.27×.** My
independent recomputation of the *model's* own convention (inner-radius chord)
gives **7.43 N → 2.75× / 1.64×**, i.e. `r12_build.log`'s 7.43 N / 2.74× is
arithmetically right and simply less conservative; §8 of the build notes says so,
and `docs/DESIGN.md` §4.5 publishes both columns and names the critic's as the
shipped bound. That closes round-5 MODERATE 2.

**(c) Does the nose stub a rounded fragment, or lift it?** Swept-sphere first
contact on the exported `brush_holder` (closest-point query, 0.05° steps,
reaction taken contact-point → sphere-centre):

```
   D 5.0 crown + 1.75, r= 26.7: first contact theta 158.95, contact height +1.500, n=(-0.228,-0.365,-0.903) -> |n_z|/|n_tang| = 2.10 (pressed DOWN)
   D 5.0 crown + 1.75, r= 32.0: first contact theta 157.15, contact height +1.500, n=(-0.231,-0.369,-0.900) -> 2.07 (pressed DOWN)
   D 6.0 crown + 2.94, r= 26.7: 162.20, +1.500, n=(-0.452,-0.724,-0.521) -> 0.61 (pressed DOWN)
   D 6.0 crown + 2.94, r= 32.0: 159.80, +1.500, n=(-0.452,-0.723,-0.522) -> 0.61 (pressed DOWN)
   D 7.0 crown + 4.08, r= 26.7: 164.00, +1.500, n=(-0.511,-0.818,-0.263) -> 0.27 (pressed DOWN)
   D 9.0 crown + 6.00, r= 26.7: 166.55, +1.500, n=(-0.530,-0.848,+0.000) -> 0.00 (pure anti-travel STUB)
   D13.0 crown +11.50, r= 26.7: 182.20, +7.450, n=(-0.491,-0.785,-0.378) -> 0.41 (pressed DOWN)
   D13.0 crown +11.50, r= 32.0: 175.95, +7.450, n=(-0.491,-0.785,-0.378) -> 0.41 (pressed DOWN)
```

**n_z ≤ 0 in every case: nothing is lifted over the nose**, and every contact is
at the 1.500 mm nose plane. Bristle tip **+1.200 mm** vs nose **1.500 mm** →
compliant-first for every proud class below 5 mm. The withdrawal of the
`cot(30°) = 1.73` ramp credit remains correct on the geometry.

### Stall-recovery motion still has the free travel it needs

Exact over **all** rotation angles (revolved (r, z) KD-tree, statics sampled at
300 k surface points + vertices, rotors at 120 k + vertices), re-run against the
**r12** statics because `meter_housing` changed:

```
   agitator     vs meter_housing         : MIN CLEARANCE OVER ALL ROTATION ANGLES =  0.550 mm (at r=46.70, z=-325.70); assembled-pose containment 0/4000
   agitator     vs hopper                : 0.934 mm (r=46.70, z=-325.70); 0/4000
   agitator     vs brush_holder          : 0.600 mm (r=46.70, z=-325.70); 0/4000
   agitator     vs retaining_plate_chute : 25.350 mm; 0/4000
   pocket_disc  vs meter_housing         : 0.974 mm (r=46.00, z=-345.77); 0/4000
   pocket_disc  vs hopper                : 6.650 mm; 0/4000
   pocket_disc  vs brush_holder          : 1.500 mm (r=41.83, z=-336.75); 0/4000
   pocket_disc  vs retaining_plate_chute : 0.500 mm (r=27.86, z=-350.75); 0/4000
```

Rotors start outside every static and the revolved clearance never reaches zero
→ **penetration is impossible at any rotation angle, forward or reverse.** The
rev-0 agitator-clash blocker stays closed, and the detent-bore rework did not
move the binding disc↔housing number (0.973 → 0.974 mm, which is mesh faceting
on the 46.993 wall vs the 46.000 disc OD).

**Reverse-stroke free travel** (recovery runs +θ; ceiling ray-cast on
`meter_housing` + `brush_holder`, 0.25° steps, three radii because a stacked Ø13
granule spans r 25.5…38.5):

```
   at r = 24.5:  park 135.0 ceiling 1.500 -> n/a for every proud class
                 park 157.5 ceiling 7.450 | 2.0 mm 107.75 | 5.0 mm 102.50 | 11.5 mm n/a
                 park 180.0 ceiling   inf |  85.25 |  80.00 |  70.00
                 park 202.5 ceiling   inf |  62.75 |  57.50 |  47.50
                 park 225.0 ceiling   inf |  40.25 |  35.00 |  25.00
                 park 247.5 ceiling   inf |  17.75 |  12.50 |   2.50   <- the binding case
   at r = 32.0:  park 247.5           inf |  17.75 |  12.50 |   2.75
   at r = 39.5:  park 247.5           inf |  18.00 |  12.50 |   2.75
```

The package's published **2.25°** stays conservative against my 2.50° at the
binding radius. For every fragment class recovery actually has to clear
(≤ 5.0 mm proud) the guaranteed free travel is **12.50° = 6.98 mm of arc at the
PCD = 2.5 × the 2.791 mm widest self-locking sliver.** The 2.25° bound applies
only to a stacked *whole* granule at the 247.5° park (1.26 mm of arc); unchanged,
published, and still the one arc-limited recovery case.

### Round-5 MODERATE 1 — closed, and measured two ways

```
   r11 TANK-ROOF GRID SCAN (242761 rays at 0.25 mm, r <= 69.5, from z = -239.6, cap FITTED):
      520 open cells = 32.50 mm2 unroofed granule bed, in 5 patches
        2.00 mm2  x[-23.75,-20.25] y[24.75,29.25]     (cap-flange clearance)
       10.69 mm2  x[-10.00, -8.00] y[-68.25,-63.75]   <- cable-tie slot
       10.69 mm2  x[  8.00, 10.00] y[-68.25,-63.75]   <- cable-tie slot
        3.81 mm2  x[  9.00, 11.00] y[ 42.00, 44.00]   <- INSIDE the O-ring gland (the cap lanyard hole)
        5.31 mm2  x[ 20.25, 26.00] y[24.75,34.50]     (cap-flange clearance)
      largest passing sphere: Dia 2.500 mm
   r12 TANK-ROOF GRID SCAN (same probe):
      117 open cells = 7.31 mm2, in 2 patches, both at r_fill 27.19..27.77
      INSIDE the fill-cap O-ring gland (r <= 25.0 from the fill axis): 0.00 mm2
      largest passing sphere: Dia 0.707 mm
      CONTROL, cap REMOVED: 24944 open cells = 1559.00 mm2 (the Dia46 fill port is 1661.90 mm2) -- the probe can see a real hole
   the tie slots, column by column:
      (x +9.0, y -66.0) top_plate z-crossings  r11: []   r12: [-235.60 -233.55 -231.15 -228.95]
      (x -9.0, y -66.0) top_plate z-crossings  r11: []   r12: [-235.60 -233.55 -231.15 -228.95]
      (x +9.0, y -72.0)                        r11: [-238.55 -233.55]  r12: [-238.55 -233.55]  (unchanged control)
```

The lid is now continuous at the tie locations (2.05 mm of lid, then a 2.40 mm
tunnel, then the 2.20 mm bridge bar), **nothing protrudes below the lid
underside** (−235.60, same plane as the neighbouring columns), and the cap has no
through-hole anywhere. 22.00 mm² of open granule bed and a Ø2.200 pass-through
are gone; the newly-found cap lanyard hole (3.81 mm², inside the seal) is gone.

### MINOR 1 — the residual 7.31 mm² is *not* sealed by the gland, and the notes say it is

BUILD-NOTES-r6 §4 attributes the residual to "the designed running clearance,
sealed by the 2.0 × 0.8 mm gland + the 1.5 mm nitrile cord". Measured, the
residual is **outside** that seal:

```
   all 117 open cells: azimuth about the fill axis 210.9..341.0 deg in two clusters, r_fill 27.19..27.77 mm
   model CAP_SEAL_R = 25.0 mm (face gland, closed 360 deg) -> every open cell is 2.19..2.77 mm OUTBOARD of the seal line
   sample columns, all three parts probed vertically:
      (+25.50,+33.00) r_fill 27.56: top_plate [] | fill_cap [] | hopper []
      (+21.75,+26.50) r_fill 27.57: top_plate [] | fill_cap [] | hopper []
      (-23.00,+28.25) r_fill 27.57: top_plate [] | fill_cap [] | hopper []
      (+20.50,+24.75) r_fill 27.75: top_plate [] | fill_cap [] | hopper []
   (for comparison, a column that IS roofed: (+24.00,+32.00) r_fill 26.59 -> top_plate [-238.550 -236.745], fill_cap [-236.35 -233.85])
```

These are **full-depth slots through the tank roof** at the two bayonet-lug
entries, not a lateral joint the face gland closes: the plate has *no* material
anywhere in those columns, so a vertical path from the granule bed to atmosphere
exists that the cord at r = 25.0 is nowhere near. The consequence is small and
should be stated as what it is: **7.31 mm² of vent passing at most a Ø0.707 mm
sphere** — fines, dust and water in both directions, no granule loss (Ø11–13
cannot pass, and neither can any fragment the metering path cares about). Fix is
one sentence in the notes/README (an accepted 7.31 mm² labyrinth vent at the
bayonet slots, ingress consequence stated) or a lug-slot roof; do not leave it
claimed as sealed. **Not a regression** — r11 had the same two patches plus
25.19 mm² more.

### MINOR 2 — two unplugged apertures in the metering-chamber wall, still only ordered in the BOM

Full-resolution census of the chamber wall (rays from the meter axis, θ at 0.1°
× z at 0.1 mm, restricted to the chamber z −351.0…−335.5, "open" = no material
inside r = 47.6):

```
   r12 detent-plunger bore (PLUNGER_A = 67.5): OPEN z -346.30..-341.20 (5.20 mm) x theta 64.4..70.6 (5.17 mm arc) -> 21.03 mm2
   r11 detent-plunger bore                   : identical, 21.03 mm2
   r12 grub access port (GRUB_A = 202.5)     : OPEN z -343.00..-339.50 (3.60 mm) x theta 200.4..204.6 (3.53 mm arc) -> 10.07 mm2
   r11 grub access port                      : identical, 10.07 mm2
   r12 bay-screw pilots (theta 253.2 / 286.8): NO aperture into the chamber
   r11 bay-screw pilots                      : OPEN z -338.20..-336.00 (2.30 mm), 2.79 mm2 total
```

Two observations, in order of importance:

1. **The r12 bay-pilot closure is a granule-path win nobody booked here.** In
   r11 those two pilots opened **2.79 mm² directly into the band a proud granule
   crown travels through** (disc top −336.750, roof underside −335.250; the
   apertures spanned −338.20…−336.00). On r12 the same probe reads **0.00 mm²**,
   with the r11 planes as the control that proves the probe fires.
2. **The two surviving apertures are open in the geometry and closed only in the
   BOM.** The Ø5.2 plunger nose bore (21.03 mm²) is filled by the COTS ball
   plunger — which no STL contains, so no clash or ingress check in this package
   can see it — and the Ø3.6 grub access port (10.07 mm²) is "plugged with an M4
   nylon set screw (BOM)" that is likewise not modelled. Both sit at disc
   mid-height facing the 0.993 mm disc-OD-to-wall gap (disc OD 46.000 measured,
   45.600 at the dimples; chamber wall 46.993), so **no granule can reach them**
   and this is a fines/dust path, not a jam path. It is pre-existing (identical
   in r11), so it is a NIT for the granule path and a note for whoever owns
   dust-tightness: state the two plugs as *required at assembly*, or model them.

### MINOR 3 — B7 and N10 remain plateaus, with the same numbers

Re-derived on r12 from my own measured rim (first plate material r = 8.747 at the
port top face) and PCD 32:

```
   park separation 2*32*sin(11.25 deg) = 12.4858 mm
   D13 seat +max : support lost at pocket separation  9.745 mm =  4.98 deg into the 22.5 deg index
   D13 centred   : 8.747 mm =  6.79 deg     D13 seat -max : 7.749 mm =  8.59 deg
   D12 seat +max : 10.245 mm = 4.08 deg     D12 seat -max : 7.249 mm =  9.49 deg
   D11 seat +max : 10.745 mm = 3.17 deg     D11 seat -max : 6.749 mm = 10.39 deg
   -> release window 3.17..10.39 deg into the index; spread D11-D13 = 7.22 deg; at D13 alone 3.61 deg
   separation at release 6.749..10.745 mm (B7.1 asks <= 1.0 mm) -> B7.1 FAILS, as recorded
   park retention: +3.739 mm outboard of the rim centred, +2.741 (D13 worst seat), +2.241 (D12), +1.741 (D11) -- none negative
   lateral velocity at the PCD: 0.126 m/s at 225 deg/s mean, 0.251 m/s at 450 deg/s peak
```

That is the shipped 3.25–10.50° / 7.25° window reproduced to ≤ 0.11° from a
different construction, and it matches my own r11 derivation to 0.00°. **B7 is
still a recorded plateau, correctly labelled in the notes.** N10 likewise:
window **120.0000° × 26.9926 mm = 2.076 × D_max**, agitator **r_max 46.743**
(0.250 mm inboard of the 46.9926 window edge), **3 fingers** ~6° wide at r > 44
at θ ≈ 0/120/240, one 22.5° index sweeps **18.75 %** of the window → one full
sweep per **5.33 indexes = 2.67 dispensed granules**. Unchanged, still an
explicit plateau-with-complaint.

### NIT 1 — "the nose covers r 20.0..46.7" is 0.25 mm optimistic at the inner end

Fine scan (0.25° over θ 145…180, `brush_holder`):

```
   r=19.50 min ceiling 7.450 | r=20.00 7.450 | r=20.25 1.500 | r=20.40 1.500 | r=20.50 1.500
   r=46.00 1.500 | r=46.50 1.500 | r=46.70 1.500 | r=46.90 7.450 | r=47.00 7.450 | r=47.20 7.450
```

The nose underside is at 1.500 mm over **r 20.25…46.70**; at r = 20.00 the first
material above the disc is the 7.450 mm rail. The model's string (quoted in
README and `docs/DESIGN.md` §4.5 as "the nose covers r 20.0..46.7 at 1.500 mm")
is therefore 0.25 mm generous at the inner end — and the r5 critic, probing r11,
reported the mirror error at the outer end (1.500 at r = 47.0, where I read
7.450). Immaterial mechanically: the uncovered inner sliver is 0.25 mm wide at a
radius where a seated granule's footprint (r ≥ 24.5) cannot be. It is worth one
character in the string because this package's standing rule is that every
"measured" sentence is traceable.

### NIT 2 — N6 improves slightly on the published number

Disc through-scan, 360 azimuths per radius: **120/360 open at r = 11.0, 104/360
at r = 15.0, 0/360 at r = 15.5, 16.0, 17.0, 18.0.** Radial land from the
lightening voids to the sump-window inner edge (measured r = 20.0000) is
**≥ 4.500 mm** against N6's ≥ 2.0 requirement (r5 measured 2/360 open at 15.5 and
published ≥ 4.000).

### What I checked and found unchanged, deliberately

`pocket_disc`, `brush_holder`, `hopper`, `agitator` and `chute_plug` are
byte-identical r11 → r12, so every number above that reproduces r11 reproduces it
because the bytes did not change; I re-ran the probes anyway rather than cite the
md5s alone, and the changed parts (`meter_housing`, `retaining_plate_chute`,
`top_plate`, `fill_cap`, `sensor_cover`, `sensor_boards`) got the scan budget.

### What I require to pass the granule path next round

1. **Label the 7.31 mm² correctly** (MINOR 1) — it is a vent at the two bayonet
   slots, outboard of the r = 25.0 face gland, passing Ø0.707 mm; not a joint the
   cord seals. One sentence in BUILD-NOTES/README, or roof the lug slots.
2. **Say that the Ø5.2 plunger nose bore (21.03 mm²) and the Ø3.6 grub port
   (10.07 mm²) are open in the shipped geometry** and closed only by COTS parts
   the exports do not contain (MINOR 2), and book the r11→r12 bay-pilot closure
   (2.79 → 0.00 mm² into the transit gap) where a reader can see it.
3. **Fix the nose-coverage string** to r 20.25…46.70 (NIT 1).
4. **Keep** everything that closed: Ø21.989 continuous drop tube with ≥ 1.995 mm
   of wall to the new duct, the 1.500 mm nose = 1.500 mm roof clearance with the
   1.200 mm bristle lead, the 130 → 95° overfill relief at full 9.000 mm roof
   section, 9.000 mm roof at all 120 B1 probes, the w = 2.791 mm / 9.63 N /
   2.12× shear headline with its 1.06× and 0.53× bounds now published, the
   2.25° published reverse bound, and the N10 plateau with its 120.0000° /
   26.9926 mm / 2.076 × D_max / 18.75 %-per-index numbers.

---

## assembly

**Owner:** assembly-and-drive critic (rev-0 RT-1; punch-list **B2**, **B3**-access,
**B9a/b/c/d/e**, **B10**, **B12.2** in so far as they are assembly/torque items).
**Verdict: PASS — no blocking assembly finding on the `r12` exports.** Round-5's
blocker **A-11 (the M5 detent plunger had nothing to thread into) is closed by
geometry** and I reproduce the closing section independently; **A-12** (bay-screw
pilot open into the metering chamber + a screw 1.000 mm longer than its pilot)
and **A-13** (one driver row for two different keys) are also closed. The
assembly order closes at **0.0000 mm³ on every one of the 26 straight-line
operations**, each with an opposite-approach control that is non-zero, and the
torque path motor→gearbox→shaft→disc measures **12.000 mm of flat-on-flat over a
64° flat arc, 39.80 mm² of bearing, and a continuous grub corridor from the disc
OD to the shaft**. Two new non-blocking findings: **A-14** (nobody has tested
whether the harness can be *threaded* through the internal duct — the r6 patency
test is a straight-line-per-leg test and cannot see a corner) and **A-15** (the
stop-pin thread engagement is **2.40 mm = 0.80 × D**, measured here for the first
time).

### Provenance

- Measured on `cad/exports/*_r12.*`, mtime **2026-08-08 00:07**, and
  `cad/BOM.md`, mtime 2026-08-08 00:27 (i.e. after the exports).
  `md5(dispenser_r12_assembly.stl) = 8465eddc5c541b45ca3035ab9cda772d`,
  `md5(dispenser_r12_assembly.step) = 92f58f640cd2fa940c664c719e685f8d`,
  `md5(retaining_plate_chute_r12.stl) = 88ab8264f05d1e2a6e9f7b6ab00fc328`,
  `md5(meter_housing_r12.stl) = eda2945b79fc4ad6a05e97c048beac14`,
  `md5(pocket_disc_r12.stl) = d02b663b6ae5cc8086ebb3a76288762e`,
  `md5(top_plate_r12.stl) = 695a6ebb534c178bbd0765b9b05b083f`,
  `md5(hopper_r12.stl) = fdc1ab2e84884b5df4fa562ce9715331`,
  `md5(fill_cap_r12.stl) = 0978d874b3b6fbea40ca9c16615c50b7`,
  `md5(brush_holder_r12.stl) = ad2343fea8807cf4a998596e939e7308`.
  **All nine match `BUILD-NOTES-r6.md` §0**, which I checked rather than believed;
  so does the notes' claim that `pocket_disc`, `brush_holder` and `hopper` are
  byte-identical to r10/r11.
- Obstruction volumes are **exact OCC booleans** on the STEP bodies
  (`build123d.import_step` + `BRepAlgoAPI_Common` + `BRepGProp`), never voxel
  estimates. Profile/section/grip probes are trimesh ray-casts and containment
  tests on the STLs. venv `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`,
  build123d 0.11.1, trimesh 5.0.0, numpy 2.5.1, scipy 1.18.0. **Nothing is
  imported from `dispenser.py`, nothing is read from `cad/verify_r6.py`, and no
  number below is taken from the build notes** — where I quote them it is to
  agree or disagree with a figure I measured first.
- COTS bodies in `dispenser_r12_assembly.step` were identified by volume +
  bounding-box match against the part exports; the six unmatched solids
  (clip plate 11.5234, motor+gearbox 69.9363, bearing 1.4946, blind-mate PCB
  1.1744, thrust washer 0.3167, brush strip 0.3122 cm³) are identified from size
  and position — an **ASSUMPTION**, unchanged from rounds 1–5.
- Convention: an approach is named by where the part **starts** ("from +Z" = the
  part starts 30–60 mm above its seat and travels −Z). Straight-line paths are
  reversible, so each row is both the install and the removal check. Primed rows
  are controls — the same member on the opposite approach — printed so that
  "0.0000" cannot mean "the probe missed".

### 0. Part inventory, export integrity (B10), static interference — all pass

```
PART EXPORTS (r12): STEP volume vs independent trimesh census of the shipped STL
part                       nsol   STEP cm3    STL cm3      d%  water  wind  euler nonman  open bodies   faces
agitator                      1      4.291      4.288  -0.053   True  True      2      0     0      1    2724
bay_lid                       1      8.598      8.598   0.001   True  True    -10      0     0      1    3076
brush_holder                  1      3.544      3.544   0.001   True  True      0      0     0      1     612
chute_plug                    1      6.721      6.718  -0.037   True  True     -2      0     0      1    2338
count_windows                 4      0.104      0.104  -0.041   True  True      8      0     0      4    2000
electronics_bay               1     21.175     21.175   0.002   True  True     -8      0     0      1   10018
fill_cap                      1      7.548      7.545  -0.034   True  True      0      0     0      1    3062
hopper                        1    109.419    109.423   0.004   True  True    -14      0     0      1   11328
meter_housing                 1    103.856    103.819  -0.035   True  True     -8      0     0      1   11598
pocket_disc                   1     72.686     72.661  -0.034   True  True    -30      0     0      1   24642
retaining_plate_chute         1     63.960     63.945  -0.023   True  True    -76      0     0      1   33678
sensor_boards                 2      1.287      1.287  -0.012   True  True      4      0     0      2    2072
sensor_cover                  2      3.198      3.198   0.000   True  True     -4      0     0      2    2360
service_stand                 1    103.908    103.892  -0.015   True  True      0      0     0      1    1104
top_plate                     1     95.572     95.550  -0.023   True  True    -38      0     0      1   22420
TOTAL printed STEP = 605.864 cm3
assembly STL: watertight=True winding=True euler=-193 bodies=24 vol=579.898 cm3 nonmanifold=0 open=0
ALL-PAIRS EXACT BOOLEAN INTERFERENCE (assembly STEP, 24 solids, 276 pairs): 44 bbox-overlapping pairs checked, 0 non-zero
```

**B10 holds: 15/15 part STLs watertight, 0 non-manifold edges, 0 open edges,
assembly 24 mesh bodies for 24 STEP solids, worst STL-vs-STEP volume error
−0.053 % (`agitator`).** This reproduces the notes' §7 table row for row,
including which part carries the worst error. The withdrawn ECO-4 chamfer (§6 of
the notes) is genuinely absent: `retaining_plate_chute_r12` reads
`watertight True, nonman 0, open 0`, not the `False / 22 / 22` of the aborted
run 1.

### 1. Derived assembly order, with swept-volume obstruction numbers

Exact boolean at every station against every already-installed solid. Stations
are 22–42 per operation over the stated travel.

| # | Operation | Starts from | Stations | Station-max | Verdict |
|---|---|---|---|---|---|
| 1 | `meter_housing` in fixture | — | — | — | datum |
| 2 | igus JFM-2023-07 into the roof bore | **+Z**, 40 mm | 42 | **0.0000** | OK |
| 2′ | (control, from below) | −Z | 42 | 580.5963 @ t = 0.833 | not possible |
| 3 | `brush_holder` + `brush_strip` radial slide-in | **θ = 148°, outboard** | 42 | **0.0000** | OK |
| 3′ | (control, opposite radial) | θ = 328° | 42 | 3000.1251 | not possible |
| 4 | `pocket_disc`, hub up through the bearing | **−Z (travels +Z)**, 40 mm | 42 | **0.0000** | OK |
| 4′ | (control, from above) | +Z | 42 | 29600.4103 @ t = 0.667 | not possible |
| 5 | `agitator` onto the Ø15 hex | **+Z**, 40 mm | 42 | **0.0000** | OK |
| 5′ | (control, from below) | −Z | 42 | 3537.3721 | not possible |
| 6a | 4 × `count_windows`, from inside the chute bore pushed out | radial out, 12 mm | 26 | **0.0000** (all four) | OK |
| 6a′ | (control, fitted from outside) | radial in | 26 | 18.3324 each | not possible |
| 6b | 2 × `sensor_boards` into the cavity | **±Y outboard**, 20 mm | 22 | **0.0000** | OK |
| 6c | 2 × `sensor_cover` | **±Y outboard**, 25 mm | 22 | **0.0000** | OK |
| 6d | motor+gearbox onto the plate | **from below**, 40 mm | 22 | **0.0000** | OK |
| 6d′ | (control, from above) | +Z | 22 | 3287.5698 | not possible |
| 6e | PTFE thrust washer into its plate counterbore | **+Z**, 20 mm | 22 | **0.0000** | OK |
| 6e′ | (control, fitted from below with the motor) | −Z | 22 | 316.6725 @ t = 0.864 | washer is **not** part of the motor sub-assembly |
| 6f | 4 × M3×8 ISO 10642 gearbox screws | +Z into the countersinks | — | flat head 0.0000 | §7, bench only |
| 7 | drive cartridge (plate + motor + washer + 2 covers + 2 boards + 4 windows) into the housing, 60 mm ascent, at −22° of unlock, disc counter-indexed −22° | **from below** | 26 | **0.0000 vs every installed solid** | OK |
| 7′ | (same at 0 / −14 / −18 / −26°, vs the housing alone) | — | 26 | 220.3226 / 110.1613 / 28.3098 / 47.4874 | not possible |
| 7b | rotate the cartridge −22° → 0° to lock | rot, 1° | 31 | **0.0000 over −24…0°**; 11.6919 at −25 and at +1; 47.4874 at −26/+2; 82.4972 at −27/+3 | OK |
| 10 | `electronics_bay` onto the housing ribs | **−Y**, 40 mm | 22 | **0.0000** | OK |
| 10′ | (control, from +Y) | +Y | 22 | 5620.7408 | not possible |
| 11 | `bay_lid` | **−Y**, 30 mm | 22 | **0.0000** | OK, removable in situ |
| 11′ | (control, pushed inboard) | +Y | 22 | 4141.5154 | not possible, as designed |
| 12 | `hopper` down over the bay riser | **+Z**, 60 mm | 26 | **0.0000** | OK |
| 12′ | (control, from below) | −Z | 26 | 11617.1463 | not possible |
| 13 | `top_plate` onto the hopper flange | **+Z**, 40 mm | 26 | **0.0000** | OK |
| 13′ | (control, from below) | −Z | 26 | 19349.5069 | not possible |
| 14 | clip plate + blind-mate PCB | **+Z**, 30 mm | 22 | **0.0000** | OK |
| 15 | `fill_cap` — rotate 90°, lift, +Y | 3 legs | 8/7/5 | 11.6387 / 0.0000 at lift ≥ 4.0 mm / 0.0000 | see NB-4 |
| 16 | `chute_plug` (ground only) | +Z | — | 83.5035 fitted, 1 body | press fit, §8 |
| 17 | `service_stand` (ground only) | — | ∩ every assembly solid = **0.0000** | — | OK |

All **15** exported printed parts are placed by that order (`chute_plug` and
`service_stand` are ground-only). Two order facts remain *forced*, not chosen:
the bearing cannot go in from below (580.5963) and the disc cannot go in from
above (29600.4103), so the disc must precede the drive cartridge. The r6 changes
— the raised fill-cap wing bar, the additive tie bridges, the duct bore, the new
detent pilot — **break nothing**: `top_plate` still drops on at 0.0000 over 26
stations, `hopper` still drops over the bay riser at 0.0000 over 60 mm.

**Cartridge service removal from the fully built machine** (members = plate +
motor + washer + 2 covers + 2 boards + 4 windows; obstacles = *every* other
solid, bay, lid, hopper, top plate and clip plate included):

```
  unlock -22 deg + 60 mm descent, disc AS ASSEMBLED     : station-max 4.6955 mm3 at dz = 0.00
  same, pocket_disc counter-indexed -22 deg             : station-max 0.0000 mm3
  service_stand ^ every assembly solid                  : 0.0000 mm3
```

That reproduces rounds 4 and 5 to four decimals. The documented drop-out path is
real, and it clears the `service_stand`, so the cartridge can be dropped with the
machine standing in its own rest position.

### 2. Torque path — motor → gearbox → shaft → metering disc: EXISTS and closes

The shaft profile is a **nearest-surface** radial ray sweep (first surface along
the inward ray); the disc bore is rays from the axis outward. Both at 1° × 13
heights spanning the whole engagement depth. "FLAT arc" counts azimuths whose
radius is below the full round radius.

```
 motor/gearbox solid V = 69.926 cm3, bbox z -418.450 .. -337.250
 DISC D-BORE   z -349.200 / -348.250 / -347.250 / -346.250 / -345.250 / -344.250 / -343.250
               / -342.250 / -341.250 / -340.250 / -339.250 / -338.250 / -337.300
               : r_min 2.550  r_max 3.050  FLAT arc 64 deg starting 171 deg  (all 13 heights)
 SHAFT D-CUT   same 13 heights : r_min 2.500  r_max 3.000  FLAT arc 64 deg starting 171 deg
 SHAFT round-only heights -353.000 / -352.000 / -350.000 / -349.500 / -349.300 : r 2.998..3.000, no flat
 DISC round-only heights  -350.000 / -349.500 / -349.300 : r 3.049..3.050, no flat (lead-in)
 shaft flat starts z = -349.2500 (bisected) ; disc bore flat starts z = -349.2500 (bisected)
 shaft top z = -337.250 ; disc hub bore ceiling z = -335.750 -> shaft-end clearance 1.500 mm
 FLAT-ON-FLAT ENGAGEMENT = 12.000 mm ; shaft flat chord 2*sqrt(3.0^2-2.5^2) = 3.317 mm
   -> 39.80 mm2 of bearing (disc-side chord 2*sqrt(3.05^2-2.55^2) = 3.347 mm)
 GRUB BORE in pocket_disc, theta = 202.5 deg (mid-flat), axis z = -341.250 (void on the r=6.0 ray
   spans z -342.500..-340.000 = 2.500 mm):
     r  2.80 ..  9.10 : lateral half-width 1.300, vertical 1.300 -> Dia2.599 thread-forming pilot
     r  9.10 .. 46.00 : lateral half-width 1.699, vertical 1.700 -> Dia3.399 clearance channel to the disc OD
     blocked radii on the grub axis: NONE - continuous void (r6 baseline: solid 10.60..24.47)
 DRIVER ACCESS on the grub axis, key across-flats 1.5 + 0.4 = Dia1.9 x 40 mm vs every other solid: 0.0000 mm3
   (largest clear driver from the disc OD r46 outward = Dia3.4; first block Dia4.0 -> meter_housing 11.9429 mm3)
 BEARING SEAT bore in meter_housing, z -330.0 / -331.5 / -333.0 / -334.8 : Dia 23.023 .. 23.030
 GEARBOX BOLT CIRCLE in retaining_plate_chute at z = -353.0, ray-located:
   (+1,0) open r 11.30..14.70 -> centre r 13.000, Dia3.400 | (0,+1) centre r 13.000, Dia3.380
   (-1,0) centre r 13.000, Dia3.400                        | (0,-1) centre r 13.000, Dia3.380
```

**B2.1, B2.2, B2.3 and B2.4 all pass on the exports**, and so does the B3
bolt-circle geometry (four clearance holes centred at r = 13.000 ± 0.000 on the
axes, Ø3.38–3.40, through the flange). **B9d** passes: seat Ø23.023–23.030
against igus JFM-2023-07 OD 23.00 and the punch list's ≤ Ø23.03 — met with
0.000–0.007 mm to spare, i.e. a tolerance item, not a margin.

**Method control, printed because it is the artefact that let r6 ship a round
bore:** taking the *far-side* exit of the same ray instead of the first surface
reports `flat arc 0 deg` at every height and hides the D-flat entirely.

**On flat-on-flat length:** the shipped figure should be **12.000 mm**, not
11.850 — 11.850 is a 0.3 mm probe-cube artefact. My flat-start planes are found
by ray-cast bisection to 1e-4 and the shaft and the disc bore land on the same
plane, −349.2500, to the fourth decimal.

### 3. A-11 — CLOSED by geometry, and I reproduce the closing section

Round-5's blocker was that the M5 detent bore was a plain Ø5.199/Ø6.399 hole with
no thread and no insert, so the plunger dropped through. Re-measured on
`meter_housing_r12.stl` along the plunger axis (θ = 67.5°, z = −343.750), lateral
half-width vs radius at 0.1 mm, transitions only, with a perpendicular vertical
probe at every step:

```
   r= 46.90   lateral half-width 2.982 -> Dia5.963   (chamber-side lead-in)
   r= 47.00   lateral half-width 2.599 -> Dia5.199   (vertical half-width 2.599)  <- Dia5.0 ball clearance
   r= 49.50   lateral half-width 2.249 -> Dia4.499   (vertical half-width 2.250)  <- thread-forming pilot
   r= 63.10   no lateral surface (outside the housing OD)
```

**The section now steps 5.199 → 4.499 going outward**, over a pilot band
**r 49.50 → 63.00 = 13.500 mm**. r11's section stepped the other way
(5.199 → 6.398) and was constant to 0.001 mm across both steps, which is what a
clearance hole looks like. B9c asks for Ø4.2–4.6 ± 0.1 over ≥ 6 mm: **Ø4.499 over
13.500 mm, met with 7.5 mm to spare.** Insertion:

```
   Dia4.5 x 16 body, r0 = 49.5, pulled radially out 0..40 mm vs EVERY assembly solid : 0.0000 mm3
   Dia5.0 x 16 body, r0 = 47.0, same sweep                                           : 50.3637 mm3 (meter_housing)
   closed form, annulus Dia5.000 in the Dia4.499 pilot over 13.500 mm                : 50.4591 mm3
```

The 50.3637 mm³ is the **designed thread-forming interference**, not an
obstruction — the Ø4.5 body path is otherwise clear at 0.0000 mm³, and the F3
corridor is Ø12.0 clear, so the plunger can be driven. This is the same
50.3637 mm³ the model prints, arrived at from the export.
`cad/BOM.md` orders one M5 part (`M5x0.8 ball-nose spring plunger, LIGHT (2.5 N),
16 mm body`) and no M5 insert (`RX-M5` count = 0), which now matches the
geometry. **A-11 is closed.**

### 4. A-12 — CLOSED, with the residual restated

Two defects on one axis. Re-measured on `meter_housing_r12.stl`, bore Ø2.500 at
(x = ±14.000, z = −337.100), 0.02 mm raster of the bore section, +Y ray per
sample. A ray is OPEN if it reaches r = 46.90 from the meter axis (inside the
Ø94 chamber bore) without crossing printed material:

```
   pilot x=+14.0 floor y=-46.500 (r12 as built) OPEN 0.0000 mm2 of 4.9024 mm2 =   0.0 %
       material floor->chamber: min 1.270 mm at (x=12.77 z=-337.31), max 2.039 mm
   pilot x=-14.0 floor y=-46.500 (r12 as built) OPEN 0.0000 mm2 of 4.9024 mm2 =   0.0 %
       material floor->chamber: min 1.268 mm at (x=-12.77 z=-337.31), max 2.037 mm
   CONTROL x=+14.0 floor y=-45.000 (r11)        OPEN 1.2832 mm2 of 4.9024 mm2 =  26.2 %
   CONTROL x=-14.0 floor y=-45.000 (r11)        OPEN 1.3368 mm2 of 4.9024 mm2 =  27.3 %
```

**The control is what makes the 0.0 % a measurement.** Re-run at r11's floor
plane the identical probe reads 26.2 % / 27.3 % open with a min material
thickness of 0.000 mm. (The notes and `verify_r6.py` print 33.9 % / 35.5 % for
the same control; the difference is the open criterion — they count a ray as open
if it reaches the far side of the chamber, I stop at the near bore wall. Both say
the same thing about r11 and about r12.) I record my own earlier construction of
this probe **failed as a can't-fail probe** — starting the ray on the floor plane
put the origin inside material and made every ray read OPEN, including the r12
one; the control caught it, which is exactly what controls are for.

The residual the notes carry as 1.262 mm I measure as **1.270 / 1.268 mm** at the
point of the bore section nearest the chamber axis. It is 8.8 × r11's 0.144 mm
and it is closed, but it is **below the 1.95 mm this package uses for insert
bosses** and it stays on the open list (notes §9 item 3 — correct as written).

Screw length, second half of A-12:

```
   bay rib outer face (head bearing plane)  y = -64.000 ; bay through-bore Dia3.200
   housing outer face at the bore edge      y = -49.601 (x=+15.6) / -50.489 (x=-12.4)
   pilot floor                              y = -46.500
   chamber bore wall on the screw axis      y = -sqrt(47.0^2 - 14^2) = -44.866
   M3x18 tip lands at y = -46.000 -> 0.500 mm of clear pilot ahead of the tip,
       and 1.134 mm of material short of the chamber bore on its own axis
   pocket_disc OD at z=-337.100: r 45.984..46.000 ; housing bore r 47.000 -> running clearance 1.000 mm
```

**`cad/BOM.md` line 67 now orders `2 × M3x18 SHCS`; `M3x20` occurs 0 times in the
file.** GRIP = 64.000 − 50.080 = **13.920 mm**, THREAD ENGAGEMENT = 50.080 −
46.500 = **3.580 mm = 1.19 × D**. My independent bracket on the housing face at
the bore edge (−49.601 … −50.489) contains the model's −50.080, so the 3.580 mm
is right. The trade (5.080 → 3.580 mm of thread bought to close the
breakthrough) is stated in the notes rather than buried, which is the correct
call on a 2-screw joint that carries no drive reaction. **A-12 is closed**, with
the 1.270 mm floor and the 1.19 × D engagement both on the record.

### 5. A-13 — CLOSED

`cad/BOM.md` now carries **two** driver rows: `**2.0 mm** hex key` (M3 ISO 10642
countersunk gearbox screws) and `**1.5 mm** hex key, >= 60 mm shaft` (the M3×4
disc grub). An M3 hex-socket set screw (ISO 4026 / DIN 913-916) takes 1.5 mm;
2.0 mm is the M4 size and the M3 countersunk size. The shipped tool list can now
build the machine. **B2.4 string check:** the only grub sizes named anywhere in
the file are `M3x4 hex socket cup-point grub` (COTS) and `M3x4 cup-point grub`
(fasteners) — **one size, stated twice, matching the modelled Ø2.599 pilot**;
`M2.5x4` occurs 0 times.

### 6. Fastener grip and thread engagement, ray-measured on the r12 exports

| joint | measured on the export | verdict |
|---|---|---|
| gearbox flange → plate, **4 × M3×8 countersunk** | 4 clearance holes at r = **13.000**, Ø3.380–3.400; motor flange face z = **−355.255**, plate top **−351.250** → **4.005 mm** of plate | B3 pattern met |
| clip plate → top plate, **4 × M2×10 + RX-M2×4** | clip-plate through-hole Ø2.999 −181.550…−177.600, head pocket **Ø4.000** −177.600…−171.050; top plate Ø2.500 lead −181.550…**−184.055**, **Ø3.200 insert bore −184.055…−188.050 = 3.995 mm**, Ø4.800 relief to −209.425. GRIP **6.455 mm**, thread beyond grip **3.545 mm = 88.7 %** of the 3.995 mm insert | **B9a MET** (asks ≥ 3.2 mm) |
| top plate → hopper flange, **6 × M3×10 + RX-M3×5.7** | 6 bores at r = 74.000, θ = 15/75/135/195/255/315, **Ø4.000 from −238.550 to −244.545 = 5.995 mm**, 1.005 mm of floor below | B9b asks 6.000 → **short by 0.005 mm**, call it met (NB-2) |
| bay ribs → housing, **2 × M3×18** | head plane −64.000, housing face −50.080, pilot Ø2.500 floor −46.500. **GRIP 13.920, ENGAGEMENT 3.580 mm** | **A-12 closed** |
| cartridge detent, **M5×0.8 plunger** | Ø5.199 ball clearance r 47.00–49.50, **Ø4.499 pilot r 49.50–63.00 = 13.500 mm** | **A-11 closed** |
| cartridge stop pin, **M3×6** | **Ø2.600 pilot r 55.600 → 58.000 = 2.400 mm** at θ = 51.0°, z = −353.250 | **A-15**, below |
| disc → shaft, **M3×4 grub** | Ø2.599 pilot r 2.80–9.10 behind a Ø3.399 channel to the OD | met |
| bay lid, 4 × M3×8 | corridors clear at Ø12.0 on all four | OK |

### 7. Tool-access corridors — largest clear driver diameter per fastener

Cylinder on the fastener axis starting at the head-bearing plane and extending
**away** from the joint; diameters stepped 1.5/2.0/2.5/3.0/3.4/4.0/5.0/6.0/8.0/
10.0/12.0 mm; the largest with a **0.0000 mm³** exact boolean against every other
assembly solid is reported, with the first blocking size and what blocks it.

```
  F1  4xM3 gearbox screws (13,0) +Z, IN SITU            max clear Dia 0.0 | Dia1.5 -> 15.7276 mm3 (meter_housing 12.7235, bearing 3.0041)
  F1  same at (0,13)                                    max clear Dia 0.0 | Dia1.5 -> 15.7276 mm3 (identical)
  F1b same, plate+motor+washer BENCH sub-assembly       max clear Dia 8.0 | Dia10.0 -> 2.1304 (thrust_washer)
  F2  M3x4 grub, key from the disc OD r46 outward       max clear Dia 3.4 | Dia4.0 -> 11.9429 (meter_housing)
  F2b M3x4 grub, hand space outboard r53                max clear Dia 4.0 | Dia5.0 ->  5.1053 (meter_housing)
  F3  M5 ball plunger, radial r63 (th=67.5)             max clear Dia12.0 | -
  F3b M3x6 stop pin, radial r58.8 (th=51)               max clear Dia12.0 | -
  F4  M3x8 skirt tabs th=30 / 105 / 225, radial         max clear Dia12.0 each | -
  F5  M3x6 wiper end tab, radial r58.1 (th=148)         max clear Dia12.0 | -
  F6  M3x18 bay rib screws x=+/-14, -Y (LID ON)         max clear Dia 6.0 | Dia8.0 -> 74.7699 (bay_lid), both screws
  F6  same (LID OFF)                                    max clear Dia12.0 | -
  F7  4x M3x8 bay-lid screws (+/-29, z=-358.868/-315.0) max clear Dia12.0 each | -
  F8  6x M3x10 flange screws r74, th=15+60k, +Z         max clear Dia12.0 each | -
  F9  4x M2x10 mount screws (+/-19,+/-19), +Z           max clear Dia 3.0 each | Dia3.4 -> 0.1005 (clip_plate's own Dia4.000 head pocket)
  F10 4x M2x6 sensor-cover screws x=34.5, +/-Y          upper pair Dia12.0 | lower pair Dia10.0, Dia12.0 -> 2.3330 (retaining_plate_chute)
```

Every fastener except the in-situ gearbox screws takes at least a Ø3.0 driver and
most take Ø12.0. **F1 in situ = Ø0.0 for the sixth round running, F1b on the
bench = Ø8.0.** Punch-list **B3.5 asks for Ø6 × 25 mm driver columns on all four
motor holes at 0.000 mm³** — that is **literally FAILED in situ and PASSED on the
plate+motor+washer bench sub-assembly**, which is the only state in which the
joint is ever made or broken. This is the design intent (the quarter-turn latch
exists so the motor is only ever handled as the drive cartridge), the cartridge
drop-out path is proven at 0.0000 mm³ above, and I record it as a stated
deviation rather than a pass — as I have in every round.

**B2.3 literal:** Ø(1.5 + 0.4) = **Ø1.9 × 40 mm on the grub axis = 0.0000 mm³**
against every other assembly solid. **B5.6 literal:** all four bay-lid driver
columns clear at Ø12.0, and the lid-lift sweep is 0.0000 mm³ over 30 mm of −Y
travel. Met.

### MAJOR A-14 (non-blocking) — nothing in the package tests whether the harness can be *threaded* through the duct; the r6 patency test cannot see a corner

This is the one place where "can it be assembled" is still unanswered, and it is
new because the duct itself is new this round.

What r6 proved is real and I do not dispute it: the I-1 boolean now removes
material (`cut_each … removed 8025.3368 mm3`), and every leg is patent **on its
own axis**. What that test does *not* do is test the *joins*. Each printed line
is a **straight** cylinder swept along **one** leg:

```
    sensor cavity riser +Y  L 12.35 | low run in Y +Y  L 10.00 | low run in X +Y  L 27.00
    vertical leg +Y  L 51.05 | collector run +Y  L 46.50 | return leg  L 65.00
    motor branch L 49.20 | motor stub L 10.50 | exit leg (-> bay) L 15.50   (x2 for -Y)
```

Fourteen legs, ~383.6 mm of total run, in a **single monolithic printed part**,
which means the conductors are not laid in — they must be pulled through after
printing. A bundle turning from "low run in Y" into "low run in X" is turning
**90° inside a ~Ø5 bore with no bend relief**: the geometric radius available at
such a junction is **0 mm**, against a minimum bend radius for a Ø4 multi-
conductor bundle of roughly **20 mm (5 × OD)** `[A: standard cable rule of thumb,
not a datasheet figure for the specific bundle — closure = the wire spec, or a
physical fish test on the printed part]`. A fish tape cannot turn that corner
either.

What I could establish independently on the export, and what I could not:

```
  complement of the plate bounding box minus retaining_plate_chute_r12.step:
      1 solid, 790089.692 mm3  -> the part contains NO fully enclosed void,
      i.e. every duct leg communicates with the outside surface somewhere
  what I could NOT extract in this round: the duct's connectivity graph, the
      number and location of its mouths, and the radius available at each junction
```

So I am **not** claiming the harness cannot be installed — I am recording that
**no test in the package supports the claim that it can**, and that the one test
that exists (a straight cylinder per leg) is structurally incapable of finding
the failure. This sits on the B5 boundary between me and the integration critic;
the *routing* is theirs, the *installability* is mine. It is non-blocking because
I could not demonstrate a failure, and because the plausible fixes are cheap
(split the duct into per-leg jumpers with both ends in accessible pockets; add
radiused junction pockets; or make the run a surface channel closed by a cover).

**Required next round:** a **fish test** printed from the export — for each
conductor run, a swept-solid bundle of the stated diameter following a path with
a bend radius ≥ the specified minimum, booleaned against the plate, plus a
statement of how many mouths the duct has and where each conductor is terminated.
A failing part looks like a 90° join with 0 mm of relief.

### MODERATE A-15 (non-blocking) — the stop-pin thread engagement is 2.40 mm, and no document says so

Round-5's NB-14 said the stop pin was carried, not re-measured, because my probe
missed the bore. I found it this round. On `meter_housing_r12.stl`, radial
section at θ = 51.0°, z = −353.250, 0.1 mm steps:

```
   r 52.0 .. 55.5 : vertical half-width 2.200 (the Dia4.4 relief/clearance pocket)
   r 55.6 .. 58.0 : lateral half-width 1.300, vertical 1.300 -> Dia2.600 thread-forming pilot
   r 58.0         : outside the housing OD
   retaining_plate_chute on the same ray: SOLID r 46.8..52.0, void beyond r 52.0
```

So the M3×6 pin threads into **Ø2.600 over 2.400 mm = 0.80 × D**, and its tip
lands at r = 52.0, exactly the plate OD it has to stop. Round 4's carried figure
(`pin ∩ housing 4.3118 mm³` for Ø3.0 in a Ø2.6 pilot) back-solves to
**2.451 mm** of engaged length — so the carried number and my direct section
agree to 0.05 mm, and NB-14 is now closed as a measurement.

The load is small (the pin sees roughly 94.2 of the 190.7 mN·m reaction at
r = 52 mm ≈ **1.81 N**, once the detent's 96.5 mN·m is subtracted), so this is not
a strength blocker. But 0.80 × D of thread-formed engagement in CF-PETG on the
part that keeps the cartridge from unlocking is worth **one sentence somewhere**,
and right now it appears in no document. Either deepen the pilot (there is
housing wall available inboard of r = 55.6 — the Ø4.4 pocket is what is eating
it) or state the 2.400 mm with its 1.81 N duty.

### Non-blocking, measured

- **NB-1 — cartridge lash re-derived: 25.0280°.** Bisected on the r12 exports:
  **+θ first contact +0.51401°, −θ first contact −24.51402°, two-sided free band
  25.0280°.** Identical to r11 to 1.4 × 10⁻⁴ degrees. Still not in the
  count-contract text, four rounds after it was first asked for.
- **NB-2 — B9b is 0.005 mm short and has been for five rounds.** Hopper flange
  insert bore **Ø4.000 from −238.550 to −244.545 = 5.995 mm** at all six
  positions, against RX-M3×5.7 + 0.3 = 6.000. Say so once in the BOM instead of
  leaving a reader to find the 0.005.
- **NB-3 — N18 / r6 open issue 2 is better than the record says.** I measure the
  clip-plate head pocket at (19, 19) as **Ø4.000** (half-width 2.000 in +x and
  +y at z = −175.0), head-bearing step at **−177.600**. Against a Ø3.80 M2 socket
  head that is **0.100 mm/side**, not the 0.05 mm/side the open-issue list
  carries against an assumed Ø3.90 pocket. The clip plate is a COTS solid and has
  not changed (11.5234 cm³, same as r11), so this is a measurement disagreement,
  not a geometry change. N18's own threshold ("if still < 0.10 mm/side, model the
  fallback") is **exactly met**; the fallback is not required. Print the Ø4.000.
- **NB-4 — the fill-cap removal residual is unchanged geometry.** With the cap
  axis taken as the bbox centre (0.000, 43.450) — an **ASSUMPTION**; the cap bbox
  is 54.9 mm in y against a 54 mm circle, so a lug skews it — leg 1 reads
  **11.6387 mm³ at 90°** and 1.02–4.26 mm³ over 5–75°, **entirely against
  `top_plate`**, exactly as in r11 (0.0000 / 1.4209 / 1.3560 / 1.1351 / 1.0191 /
  1.5947 / 4.2559 / 11.6387 at 0/5/15/30/45/60/75/90°). Leg 2 clears at a
  **4.0 mm lift** (0.0000 mm³ at 4/6/8/10/12 mm) and leg 3 at **0.0000 mm³ out to
  +45 mm**. The r6 raised wing bar did **not** touch this. N5's detent residual
  stays declared.
- **NB-5 — `chute_plug` press fit is exactly the designed interference.**
  `retaining_plate_chute ∩ chute_plug = 83.5035 mm³ in 1 body`, against the
  closed form 2π·11.075·0.150·8.0 = **83.5035 mm³**; ∩ every other solid
  = 0.0000; withdrawal along −Z: 83.5035 / 81.5416 / 77.0340 / 72.7172 / 46.9729
  / **0.0000** at dz = 0 / −2 / −5 / −10 / −20 / −30. Comes off on a straight pull.
- **NB-6 — `service_stand` clearance 8.000 mm.** Stand ground plane z =
  **−426.450**; lowest solid in the assembly is the motor can at **−418.450**
  (lowest *printed* material −418.300); stand ∩ every assembly solid =
  **0.0000 mm³**. B12.2's "load path does not pass through the gearbox output
  flange" is met in the only sense I can check: nothing touches the motor.
- **NB-7 — the detent thread form is at the loose end.** Ø4.499 pilot on an
  M5×0.8 major diameter is a radial interference of **0.251 mm = 57.9 % of the
  0.433 mm ISO thread height (H1 = 0.541 P)**. That is a legitimate
  thread-forming hole for a plastic, but it is nearer 0.90 × D than the 0.80 × D
  that is usual for thermoplastics, and the plunger is a *machine*-thread part,
  not a thread-forming screw. First-article pull/retention on the printed part is
  the closure, and it is not in the test plan.
- **NB-8 — the grub retrieval hazard is unchanged.** The M3×4 grub seats at
  r 2.80–6.80 with 2.30 mm of empty Ø2.599 pilot behind it and a **Ø3.399 channel
  running 39.2 mm out to the disc OD**; the 1.5 mm key must travel **≈ 45 mm**
  from outside the housing OD. Dropped, the grub falls down the channel. Named in
  rounds 4–5, still true, still only a note.
- **NB-9 — the BOM's TSSP4038 occurrence is historical, not an order line.**
  `cad/BOM.md` contains the string once, inside
  `Vishay VBPW34FAS … replaces the REJECTED TSSP4038`. B4.7 is substantively met.
  For the record, `verify_r6.py`'s own hex-key check works only because it does
  `bom.replace("*","")` first — the literal substrings `1.5 mm hex key` and
  `2.0 mm hex key` do **not** appear in `BOM.md` (they are `**1.5 mm** hex key`).
  That is fine, but it is the kind of thing that makes a checker look like it
  passed something it did not read.

### What I need to see next round to keep "assembly" passing

1. **A-14: a fish test, not a patency test.** Swept bundles on paths with a real
   bend radius, per conductor run, booleaned against `retaining_plate_chute`;
   the duct's mouth count and locations; and a statement of how the harness is
   physically installed. A failing part looks like a 90° join with 0 mm of relief.
2. **A-15: the stop pin's 2.400 mm / 0.80 × D engagement written down**, or the
   pilot deepened, with the section re-printed from the export.
3. **The residuals restated, not quietly dropped:** 1.270 mm under the bay-screw
   pilot floor, 3.580 mm (1.19 × D) of bay-screw thread, 5.995 vs 6.000 mm on the
   hopper insert bores, and F1 = Ø0.0 in situ / Ø8.0 on the bench against B3.5's
   literal Ø6.
4. **NB-1 (0.51401° / 25.0280° of lash) and NB-6 (8.000 mm stand clearance)**
   written into the service and count-contract text with those numbers — asked
   for in rounds 4 and 5, still not done.
5. §1, §2, §6 and §7 of this critique re-printed from the tools rather than
   asserted: the order table's 0.0000s **with their controls**, **12.000 mm** of
   flat-on-flat with the 64° flat arc, the Ø2.599/Ø3.399 grub section, and the
   grip figures 13.920 / 6.455 / 4.005 / 5.995 / 3.580 / 13.500 / 2.400.

---

## integration

**Owner:** integration-and-serviceability critic (directives 2, 3, 4; punch-list
**B5, B6, B11, B12**, plus ground clearance / envelope).
**Verdict: PASS WITH COMPLAINTS — 0 blocking findings, 6 recorded (N-i5 … N-i10).**
(a) reach-in corridor **PASS** · (b) electronics bay + wiring **PASS on every
punch-list test, including the round-5 blocker I-1, which is genuinely closed in
geometry** — with two real complaints about what *seals* it · (c) refill workflow
**PASS** · (d) ground clearance / envelope **PASS** · (e) mass ledger **PASS on
the CONTEXT dry target, over on the 100 %-infill loaded bound**.

**Method.** Every number below is my own measurement on the shipped `*_r12`
exports, made without importing `dispenser.py`: OCC solid classification and
exact B-rep booleans on the STEP files (build123d 0.11.1 / OCP), `trimesh` 5.0.0
on the STLs, `scipy` KD-trees and convex hulls for separations and support
polygons, venv `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`. **Bores,
bosses, grooves and cavities are *found* by enumerating the analytic surfaces of
the exported B-rep and by scanning — never by being told where they are**; the
duct-leg axes below were re-derived from the Ø5.000/Ø5.500 *inner* cylindrical
faces of `retaining_plate_chute_r12.step`, which is how I can check them without
trusting `BUILD-NOTES-r6.md`. `[A]` marks an assumption I introduce. Where I
disagree with the build notes, both numbers are printed.

---

### I-1 (round-5 BLOCKING) — CLOSED, and closed harder than the notes claim

The round-5 blocker was that every leg of the cartridge harness duct was **solid
printed material** (largest conductor Ø0.0, part contained zero enclosed voids).
`BUILD-NOTES-r6.md` §2 tests the fix against `retaining_plate_chute` only. I ran
the same test **against all 13 flight solids at once**, so a leg that is patent
in the plate but blocked by the housing, the bay or the disc would still fail:

```
B5 DUCT PATENCY — axis occupancy vs ALL 13 FLIGHT SOLIDS (a patent leg reads 0/N)
   leg axes derived from the Dia5.0/5.5 INNER cylindrical faces enumerated on retaining_plate_chute_r12.step
   exit leg (bay end -> collector)    L  15.50 mm     0/  63 axis points INSIDE material (  0.0 %)
   collector run -Y                   L  32.50 mm     0/ 131 axis points INSIDE material (  0.0 %)
   collector run -Y (east)            L  14.00 mm     0/  57 axis points INSIDE material (  0.0 %)
   return leg (-Y -> +Y)              L  65.00 mm     0/ 261 axis points INSIDE material (  0.0 %)
   collector run +Y                   L  46.50 mm     0/ 187 axis points INSIDE material (  0.0 %)
   vertical leg +Y                    L  51.05 mm     0/ 205 axis points INSIDE material (  0.0 %)
   vertical leg -Y                    L  51.05 mm     0/ 205 axis points INSIDE material (  0.0 %)
   low run in X +Y                    L  27.00 mm     0/ 109 axis points INSIDE material (  0.0 %)
   low run in X -Y                    L  27.00 mm     0/ 109 axis points INSIDE material (  0.0 %)
   low run in Y +Y                    L  10.00 mm     0/  41 axis points INSIDE material (  0.0 %)
   low run in Y -Y                    L  10.00 mm     0/  41 axis points INSIDE material (  0.0 %)
   sensor cavity riser +Y             L  11.85 mm     0/  48 axis points INSIDE material (  0.0 %)
   sensor cavity riser -Y             L  11.85 mm     0/  48 axis points INSIDE material (  0.0 %)
   motor branch (vertical)            L  49.20 mm     0/ 197 axis points INSIDE material (  0.0 %)
   motor stub                         L  10.50 mm     0/  43 axis points INSIDE material (  0.0 %)
   TOTAL 0/1745 axis points inside printed material

   CONTROL: 4000 uniform points in the retaining_plate_chute bbox
   10.2 % read INSIDE printed material (a probe that always says False reads 0.0 %)
```

Conductor sweeps, exact booleans vs all 13 solids (r11: **Ø0.0** everywhere):

```
B5.4 CONDUCTOR SWEEP: cylinder on each leg axis vs ALL 13 flight solids (clear = 0.0000 mm3)
   exit leg (bay end -> collector)      Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   collector run -Y                     Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   return leg (-Y -> +Y)                Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   collector run +Y                     Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   vertical leg +Y                      Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   vertical leg -Y                      Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   low run in X +Y                      Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   low run in X -Y                      Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   sensor cavity riser +Y               Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   sensor cavity riser -Y               Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   motor branch (vertical)              Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3
   motor stub                           Dia4.0    0.0000 mm3  Dia4.5    0.0000 mm3

   LARGEST CLEAR CONDUCTOR PER LEG (bisect 0.01 mm, vs all flight solids)
   every cartridge leg                  Dia  5.00 mm
   motor stub                           Dia  5.50 mm
```

`retaining_plate_chute` 71.850 → **63.945 cm³** on the shipped STL (my own
trimesh read), i.e. the 7.9 cm³ I asked for in round 5 actually came out.
**I-1 is closed.**

---

### (a) Gloved-hand access corridor to the quick-release (directive 3 / B6) — **PASS**

**The corridor I require, and why.** `[A]` **95 mm wide × 45 mm tall × 130 mm
deep**, top at the clip-plate underside, measured **from the neck face outward**.
Same three numbers as PUNCHLIST B6.2 and as rounds 1–5, so the series is
comparable:

- **95 mm wide** — 95th-percentile adult male hand breadth across the
  metacarpals ≈ 90 mm, plus a light mechanic's glove ≈ 2–3 mm per side.
  `[A: anthropometric figure quoted from memory, not from a table I opened;
  closure = a tape measure on a gloved hand, or one sentence from Thomas.]`
- **45 mm tall** — 95th-percentile hand thickness at the metacarpals ≈ 34 mm
  plus glove and knuckle working clearance. `[A, same closure]`
- **130 mm deep** — the hand must pass the release and the forearm follow it.
  `[A, same closure]`

Stand-off geometry, recovered by 0.5 mm slab intersections on the exported
B-rep (no model constant used):

```
PLAN EXTENT OF PAYLOAD MATERIAL BY Z (0.5 mm slab intersections, exact B-rep)
   -181.600  top_plate    X[  -24.00,   24.00] Y[  -24.00,   24.00]  a=  24.00
   -200.000  top_plate    X[  -24.00,   24.00] Y[  -24.00,   24.00]  a=  24.00
   -224.000  top_plate    X[  -24.00,   24.00] Y[  -24.00,   15.00]  a=  24.00
   -225.000  top_plate    X[  -24.00,   24.00] Y[  -84.00,   15.00]  a=  84.00   <- the -Y strain-relief boss
   -228.300  fill_cap     X[  -12.00,   12.00] Y[   39.00,   47.00]  a=  47.00
payload top face (clip-plate underside)  Z = -181.550
first material outside the 48 x 48 neck  Z = -225.050
STAND-OFF HEIGHT h = 43.500 mm      (B6.1 target h >= 40)
NECK PLAN HALF-EXTENT a = 24.000 mm (48.000 x 48.000 outer, cavity 42.800 x 42.800)  (B6.1 target a <= 35)
```

```
B6 REACH-IN CORRIDOR, r12 exports, exact B-rep booleans vs ALL flight solids
corridor near face at |x| or |y| = 24.000 (neck outer face), top at Z = -181.550
   95.0 x  45.0 x 130.0 mm:  +X     0.0000  -X     0.0000  +Y     0.0000  -Y   340.2241 (top_plate)
   95.0 x  52.0 x 130.0 mm:  +X     0.0000  -X     0.0000  +Y   764.8000 (fill_cap)  -Y  2818.5999 (top_plate)
  100.0 x  50.0 x 130.0 mm:  +X     0.0000  -X     0.0000  +Y   636.8000 (fill_cap)  -Y  2138.5415 (top_plate)
  110.0 x  45.0 x 130.0 mm:  +X     0.0000  -X     0.0000  +Y     0.0000  -Y   340.2241 (top_plate)
   95.0 x  45.0 x 150.0 mm:  +X     0.0000  -X     0.0000  +Y     0.0000  -Y   340.2241 (top_plate)

LARGEST CLEAR CORRIDOR PER SIDE (D=130, top at Z=-181.550, bisect 0.01 mm)
   +X:  52.00 mm tall at 95 mm wide ;  >=300.00 mm wide at 45 mm tall
   -X:  52.00 mm tall at 95 mm wide ;  >=300.00 mm wide at 45 mm tall
   +Y:  46.65 mm tall at 95 mm wide ;  >=300.00 mm wide at 45 mm tall
   -Y:  43.50 mm tall at 95 mm wide ;     0.00 mm wide at 45 mm tall (blocked on the centreline)
```

**B6.2 is met:** three sides clear at **0.0000 mm³**, including the two opposing
sides +X and −X, and those two are clear at **52.00 mm** — 7.00 mm more than my
requirement. Widening the corridor to 110 mm costs nothing (still 0.0000 on
+X/−X/+Y). Only −Y is obstructed, by the harness strain-relief boss whose top is
at Z = −225.050, i.e. **1.500 mm** into a corridor floored at −226.550
(340.2241 mm³ / 1.500 mm ≈ 226.8 mm² of footprint).

**B6.3 (QR actuation sweep) remains NOT VERIFIABLE on this package**, unchanged
from rounds 4 and 5: `interface/mechanical/README.md` puts the release on the
**drone-side** half ("Fixed half (spring press-pins) — mounted on the aircraft …
it clips into the aircraft's fixed half by hand"), which lives above Z = −171 and
is not in these exports. Measured on the assembly: the clip plate is
**50.000 × 50.000 × 10.500** (component 8 of the assembly STL, bbox X[−25,25]
Y[−25,25] Z[−181.6,−171.1]) on a 48.000 × 48.000 neck = **1.000 mm of proud edge
per side** — enough to index the halves, not a finger grip. Recorded as not
verified, not as passed.

**B6.4 no regression on the aircraft side:** `dispenser_r12_assembly.stl` max
Z = **−171.0500**, **0 vertices above Z = −171.000**.

---

### (b) Electronics bay, PCB envelope, dust-tightness and wiring routes (directive 2 / B5) — **PASS on every test, with two complaints about the seals**

#### B5.1 the bay exists and the control PCB fits — **PASS**

Bay interior recovered by scanning (no model constant used): inboard wall
y −64.000…−62.000, lid inner face y = −88.600, side walls |x| 26.000…28.000,
floor z −358.100…−356.100, roof z −318.100…−316.100 → **interior 52.000 (x) ×
24.600 (y) × 38.000 (z) mm**. (ELECTRONICS §7 says "interior 46 × 22 × 38"; the
built bay is larger — see N-i10.)

**ECO-7 standoff bosses are real geometry**, found by mapping bay material 2 mm
inboard of the wall and clustering:

```
MAP of bay material at y = -66.0 (0.5 mm grid): four clusters
   x  15.50.. 20.50  z -353.50..-348.50      x -20.50..-15.50  z -353.50..-348.50
   x  15.50.. 20.50  z -325.50..-320.50      x -20.50..-15.50  z -325.50..-320.50
BOSS AXIAL EXTENT (y-scan off the boss axis): material [-69.000,-62.000]
   -> boss OD Dia5.200, seat face y = -69.000 = 5.000 mm PROUD of the wall (ECO-7 asks >= 4)
   -> M2.5 thread-forming pilot Dia2.100, blind, y -69.000..-64.100 = 4.900 mm deep
```

```
B5.1 BOARD FIT: 42(x) x 34(z) x 12(y) envelope seated on the boss seat faces
   board envelope X[-21,21] Y[-81.0,-69.0] Z[-354.100,-320.100]
   vs ALL flight solids = 0.0000 mm3                                   (B5.1 asks 0.000)
   six clearance gaps (grow one face at a time to first contact, bisect 0.01):
      +X            5.000 mm      -X            5.000 mm
      +Y(inboard)   0.000 mm  <- this face IS the standoff seat (the mounting datum);
                                  the inboard WALL is 5.000 mm behind it
      -Y(lid)       7.600 mm
      +Z(up)        1.800 mm      -Z(down)      2.000 mm
```

Every real gap is **≥ 1.500 mm** as B5.1 asks (1.800 is the tightest).

#### B5.2 three cable entries — **PASS as written**

Enumerated from the bay's own analytic surfaces:

```
electronics_bay_r12: cylindrical faces (entries only)
   Dia 10.400 axis Z  X[-5.20,5.20]  Y[-86.20,-75.80] Z[-316.10,-306.60]  (spigot OD; ID Dia7.400)
   Dia  7.400 axis Z  X[-3.70,3.70]  Y[-84.70,-77.30] Z[-318.30,-306.60]  (through the bay roof)
   Dia 10.000 axis Y  X[-15.00,-5.00] Y[-64.00,-62.00] Z[-355.10,-345.10] (inboard face, 2.000 mm panel)
   Dia 10.000 axis Y  X[  5.00,15.00] Y[-64.00,-62.00] Z[-355.10,-345.10] (inboard face, 2.000 mm panel)
```

Three entries, each ≥ Ø6.0, each with a land ≥ 1.500 mm (the two inboard ones
are 2.000 mm panels; the roof one is a 1.500 mm spigot wall). B5.2 passes on the
letter. What it does not prove is that any of them **seals** — see **N-i6**.

#### B5.3 the lid gasket is real geometry — **PASS**

The groove is cut into the bay rim face at y = −90.000. Edges bisected to 1e-5 mm
on the exported B-rep:

```
B5.3 GASKET GROOVE
   +x rail, z=-337.0/-350.0/-322.0: groove x[25.2000,26.8000]  width 1.6000 mm  depth 1.2000 mm
   -x rail, same three z:           groove x[-26.8000,-25.2000] width 1.6000 mm depth 1.2000 mm
   bottom rail, x=+24/-24:          groove z[-357.350,-355.850] width 1.550 mm  depth 1.200 mm
   top rail,    x=+24/-24:          groove z[-318.350,-316.850] width 1.550 mm  depth 1.200 mm
   centreline loop |x| = 26.000, z = -356.600 .. -317.600 -> 52.000 x 39.000 mm
   PERIMETER = 182.000 mm
   CONTINUITY: 120 of 120 stations on the loop show the groove; misses []
```

≥ 1.5 mm wide × ≥ 1.0 mm deep, closed loop, perimeter printed. **B5.3 passes.**
(The r5 figure "1.580 × 1.200" was the model's nominal; measured on the export
the loop is 1.550–1.600 wide depending on rail. The **cord ordered against it is
wrong** — N-i5.)

#### B5.4 the harness never enters the granule space — **PASS, 0.0000 mm³**

I built the granule space as a deliberate **superset** of the real void from
measured bounds, so a miss is a strong pass, and I ran controls that must hit:

```
GRANULE-SPACE SUPERSET
   tank+funnel  r70.0  z[-334.30,-238.00]   (real barrel bore r<=69.5; tank ceiling z=-235.60/-238.55)
   metering     r48.0  z[-351.25,-334.30]   (pocket disc OD r46.0 z[-350.75,-320.25]; plate top face z=-351.25)
   exit chute   Dia22.0 at (x=32,y=0) z[-418.40,-351.25]

B5.4 HARNESS vs GRANULE SPACE (swept solid on each modelled route, exact boolean)
   neck cavity drop            Dia5.5   tank 0.0000 | metering 0.0000 | chute 0.0000
   top-plate conduit           Dia5.5   tank 0.0000 | metering 0.0000 | chute 0.0000
   elbow + vertical spigot     Dia5.5   tank 0.0000 | metering 0.0000 | chute 0.0000
   bay riser                   Dia5.5   tank 0.0000 | metering 0.0000 | chute 0.0000
   bay -> cartridge exit leg   Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   collector run -Y            Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   return leg                  Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   collector run +Y            Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   vertical leg +Y / -Y        Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   low run +Y / -Y             Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   sensor riser +Y / -Y        Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   motor branch                Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   motor stub                  Dia4.0   tank 0.0000 | metering 0.0000 | chute 0.0000
   TOTAL harness volume inside the granule-space superset = 0.0000 mm3

   CONTROL through the tank               tank  879.6459 | metering    0.0000 | chute   0.0000
   CONTROL through the chute              tank    0.0000 | metering    0.0000 | chute 628.3185
   CONTROL through the metering chamber   tank    0.0000 | metering 1005.3096 | chute   0.0000
      (a broken probe reads 0.0000 on all three)
```

Directive 2's "the wiring would go straight into the tank" is fixed and stays
fixed. The thinnest barrier between harness and granules is printed in N-i9.

#### B5.5 route continuity, coverage and **channel cross-sections** — **PASS (92.9 % covered)**

The upper route is a genuine closed conduit, and the R8.0 elbow that
ELECTRONICS §6.3 claims **is actually in the geometry** (a swept-ball elbow: a
chain of 15 spherical patches of r = 3.000 running from y = −73.30 to −80.98):

```
ELBOW CENTRELINE (tangent arc joining the horizontal conduit axis z=-230.55 to the vertical axis y=-81)
   R= 4.00:   0/181 centreline points inside top_plate material
   R= 8.00:   0/181 centreline points inside top_plate material
   R=10.00:   0/181 centreline points inside top_plate material
   local clear half-width across the R8.00 arc (0.02 mm probe):
     arc 0 deg   free out 2.98 / in 2.98 / lateral x 2.98 mm
     arc 30 deg  free out 2.98 / in 4.70 / lateral x 2.98 mm
     arc 60 deg  free out 2.98 / in 4.70 / lateral x 2.98 mm
     arc 90 deg  free out 2.98 / in 2.98 / lateral x 2.98 mm
   -> Dia5.96 clear all the way round the bend
```

**Channel cross-sections, as asked, measured by bisecting the largest clear
cylinder on each axis against all flight solids:**

| segment | measured clear section | area | fill with its own bundle |
|---|---|---|---|
| neck cavity (blind-mate PCB → conduit mouth) | 42.800 × 42.800 mm | 1831.84 mm² | 9 × 26 AWG = 7.79 mm² → **0.4 %** |
| top-plate conduit (0, y, −230.55), y −22…−80 | **Ø6.750** (nominal bore Ø6.000) | 35.781 mm² | 7.79 mm² → **21.8 %** |
| R8.00 swept elbow | **Ø5.960** | 27.898 mm² | 7.79 mm² → **27.9 %** ← tightest on the aircraft harness |
| vertical spigot / hopper-side conduit, z −232…−309 | **Ø6.122** | 29.433 mm² | 7.79 mm² → **26.5 %** |
| bay riser socket, z −311…−317 | **Ø7.400** | 43.004 mm² | 7.79 mm² → **18.1 %** |
| cartridge duct, every leg | **Ø5.001** | 19.643 mm² | motor 4 × 26 AWG = 3.46 mm² → **17.6 %**; sensor 6 × 26 AWG = 5.20 mm² → **26.5 %** |
| cartridge duct, motor stub | **Ø5.500** | 23.758 mm² | 3.46 mm² → **14.6 %** |

Every section is far under B5.5's **≤ 70 %** ceiling; the worst is **27.9 %**.
(ELECTRONICS §6.3's "tightest section is the Ø6.000 = 28.27 mm² top-plate
conduit" is right in spirit; measured, the pinch is the elbow at Ø5.960.)

Coverage:

```
covered route length (measured legs)  = 195.30 mm (upper: neck 47.55 + conduit 60.00 + spigot/conduit 80.05 + riser 7.70)
                                      + 433.00 mm (15 cartridge duct legs)
                                      = 628.30 mm
uncovered                             = 2 x 21.655 mm bay -> cartridge service loop = 43.309 mm
                                      + 4.40 mm motor flying leads [carried from ELECTRONICS 6.3, not re-measured]
                                      = 47.709 mm
COVERAGE = 628.30 / 676.01 = 92.94 %          (B5.5 asks >= 90 %)
```

The uncovered length and where it is: **21.655 mm per cable**, straight line from
the bay's inboard entry face (x = ±10, y = −62.000, z = −350.100) to the
cartridge duct mouth (0, −48.000, −363.250) — two cables (motor + count sensor),
**43.309 mm total**. This is the deliberate service loop that lets the cartridge
come off; it is outside the granule space and outside the bay, on the −Y flank of
the housing. Recorded as **N-i7**, not as a failure.

#### B5.6 lid removable in situ — **PASS**

```
   driver column Dia6 x 25 on the lid screw at (-29.0,-359.1): 0.0000 mm3
   driver column Dia6 x 25 on the lid screw at (+29.0,-359.1): 0.0000 mm3
   driver column Dia6 x 25 on the lid screw at (-29.0,-315.1): 0.0000 mm3
   driver column Dia6 x 25 on the lid screw at (+29.0,-315.1): 0.0000 mm3
   lid-lift sweep (lid translated 0..20 mm outboard in -Y, 21 stations) vs every other flight solid: 0.0000 mm3
```

#### Dust-tightness to the hopper — **PASS on the tank side; the leaks are on the harness side**

There is **no shared opening between the bay interior and the granule space**:
the pairwise interference matrix is clean and the only structure the bay shares
with the tank side is the telescoping conduit:

```
PAIRWISE INTERFERENCE OF THE 13 FLIGHT SOLIDS (exact B-rep boolean)
   pairs with interference: 0
```

```
BAY RISER <-> HOPPER CONDUIT TELESCOPING JOINT (the only bay/tank-side shared boundary)
   z=-308.00 .. -310.50:  bay material y[-86.200,-84.700] and [-77.300,-75.800]  -> spigot OD Dia10.400, ID Dia7.400, wall 1.500
                          hopper conduit bore Dia11.000
   radial clearance 0.300 mm/side ; engagement z -310.600 .. -306.600 = 4.000 mm
   unsealed annulus area = pi/4 (11.000^2 - 10.400^2) = 10.0844 mm2
   the Dia7.400 bore itself = 43.0084 mm2 gross; a Dia5.5 bundle fills 23.7583 -> 19.2501 mm2 free
```

Both of those paths lead to the **neck cavity**, not to the tank, so no granule
or granule dust can reach the board through them; but they are the reason the
word "sealed" in directive 2 is not yet earned — see **N-i6**.

---

### (c) Side-wall fill port / refill workflow (directive 4 + RT-14 / B12) — **PASS**

The package takes B12's "**or an equivalent measured solution**" branch: a
roof-mounted bayonet port plus a mandatory printed `service_stand`, not a
side-wall port. Measured, in that order:

**B12.3-equivalent, the port itself** (cap removed, min clear radius about the
fill axis (0.0, 43.0), 2° angular sampling, bisected):

```
   z=  -233.60: clear Dia 54.999 mm
   z=  -235.60: clear Dia 54.999 mm
   z=  -237.10: clear Dia 52.000 mm
   z=  -237.60: clear Dia 46.000 mm   <- WORST (the bayonet-lug band), azimuth 14 deg
   z=  -238.10: clear Dia 46.000 mm
   z=  -238.60: clear Dia 62.618 mm
   granule Dia13.0 worst-case drop path from the port to the bed (vertical Dia13 on the fill axis): 0.0000 mm3
```

**Ø46.000 mm** clear through the whole port depth — exactly B12.3's
`[A: >= Dia46]`. The port is in the tank **roof**, so it is trivially above any
fill line. **Capacity is untouched (directive 5): `hopper_r12.stl` is
byte-identical to r10 and r11** (`md5 fdc1ab2e84884b5df4fa562ce9715331` for all
three), so the measured change in usable volume is **0.000 %**.

**B12.1 rest position** — the load path does **not** run through the gearbox:

```
   ground plane (service_stand underside) Z = -426.450
   stand footprint radius 76.000..90.000 mm, ground-hull area 25436.4 mm2
   CONTACT PATCH (assembly samples within 1.0 mm of the stand, 300 000 samples/body):
      407 samples, Z -358.250..-357.265, r 52.29..71.55 -> the meter-housing latch-ring underside
      contact azimuth bins (10 deg): 50, 60, 170, 180, 290, 300  -> THREE pads
      contact support polygon (convex hull in plan) = 6784.4 mm2
   lowest dispenser material Z = -418.450 (the gearbox can) vs ground -426.450
      -> the can stands 8.000 mm OFF the ground; the load path is on printed structure
   dispenser EMPTY CG = (1.66, -7.08, -329.45) at 1164.3 g ; service_stand 131.9 g at (0.00,0.00,-399.77)
   UNIT (dispenser + stand) CG = (1.49, -6.36, -336.61)
   TIP ANGLE, tipping as a unit on the stand footprint (d = 83.445, h = 89.841)  = 42.89 deg  EMPTY
   TIP ANGLE, tipping off the three pads   (d = 34.217, h = 28.675)              = 50.04 deg  EMPTY
                                                    (B12.1 asks >= 25 deg [A: 15 deg tailgate slope + margin])
```

Both consistent pivots pass with ≥ 17.9° of margin. The loaded tip angles are
**carried** from round 5 (unit 38.48° @250, 36.35° @421) — `hopper`,
`meter_housing`'s latch ring and `service_stand` are unchanged, so the geometry
behind them is the same, but I did not re-derive the granule-bed CG this round
and say so rather than restating it as measured.

**B12.2 fill route**, measured on the exports (the neck and clip plate stay
bolted to the dispenser when it comes off the aircraft, so they are in the way
whether or not you are on the aircraft):

```
   fill_cap bbox Z -239.550..-228.200 ; top-plate top face Z = -233.550 ; neck column (|x|,|y|<=24) starts at Z = -225.050
   PURE AXIAL LIFT, cap translated +Z, vs every other flight solid:
      lift  2.00 mm ->    14.6145 mm3 top_plate     <- bayonet still engaged; you must unlock first
      lift  3.00 mm ->     0.0000 mm3
      lift  6.00 mm ->     0.0000 mm3
      lift 12.00 mm ->     0.0000 mm3
   LATERAL +Y at lift 6.00 mm:
      +Y  0 / 10 / 20 / 30 / 40 / 50 / 60 mm ->  0.0000 mm3 at every station
```

Required lift **3.000 mm** to break the lugs free, **6.000 mm** to clear the
plate top face, then an unobstructed lateral run to **+60 mm** — against r6's
"6.45 mm of lift then 58 mm of lateral travel in a 10.5 mm gap". The raised
lanyard wing bar (cap top −230.700 → −228.200) does not touch it: the cap flange
at a 12 mm lift still tops out at −225.550, below the neck at −225.050.

---

### (d) Ground clearance and overall envelope — **PASS**

```
dispenser_r12_assembly.stl: 142 442 faces, watertight=True, 24 connected components (all watertight), 579.898 cm3
   bbox X[-78.000,78.000] Y[-92.000,78.000] Z[-418.450,-171.050]
   plan envelope 156.00 (x) x 170.00 (y) mm ; max radius from the mount axis 97.944 mm
   stack below the mounting plane = 247.450 mm
   B6.4: 0 vertices above Z = -171.000 (max Z = -171.0500)

GROUND CLEARANCE, on the real landing gear
   quiver.airframe_structure.landing_gear.assembly.make_assembly()
   gear bbox X[-293.57,293.57] Y[-250.00,250.00] Z[-547.89,-124.94]
   my tessellation (0.2 mm) puts the ground plane at Z = -547.834
   GROUND CLEARANCE AT REST = -418.450 - (-547.834) = 129.384 mm     (required >= 40; 3.2x)
   PAYLOAD <-> LANDING GEAR minimum separation, mesh-to-mesh
      (200 000 surface samples per body, KD-tree, then exact point-to-triangle on the 200 closest)
      = 103.673 mm KD / 103.664 mm exact          (r6: 83.41; round 4: 103.628; r12 notes: 103.63)
      closest payload point (-59.79, 50.04, -233.55)

PROP CLEARANCE, re-measured this round (quiver.equipment.propulsion.assembly)
   propulsion bbox X[-673.63,673.63] Y[-664.52,673.63] Z[-18.50,63.54]
   VERTICAL gap, lowest propulsion material (-18.501) to payload top (-171.050) = 152.549 mm
   IN-PLAN gap, nearest propulsion radius 330.576 - payload max radius 97.944   = 232.632 mm
   VERTEX-TO-VERTEX minimum separation (306 070 x 71 028 vertices, KD-tree)     = 374.901 mm
```

This is the first round I have reproduced the prop numbers independently: they
match `BUILD-NOTES-r6.md` §7 to **0.001 / 0.002 / 0.001 mm**.

Also checked and clean, because the notes' body count was the one number I could
not reproduce with `trimesh.body_count`: splitting the assembly STL into
connected components gives **24 components, every one watertight**, matching
"24 mesh bodies for 24 solids". (`Trimesh.body_count` reads 23 because it welds
coincident vertices; the split is the right test. No finding.)

---

### (e) Mass ledger, rebuilt independently from the exports — **PASS on the CONTEXT dry target**

Volumes are my own `trimesh` reads of the shipped r12 STLs; densities per
PUNCHLIST B11.1 (CF-PETG **1.27**, TPU 1.19, PMMA 1.18). COTS masses are carried
from `cad/BOM.md` and are **not** measurements.

```
PRINTED, FLIGHT CONFIG, 100 %-INFILL BASIS
   top_plate                   95.550 cm3 x 1.27 =   121.35 g   centroid (  -0.05,  -4.24,  -223.47)
   fill_cap                     7.545 cm3 x 1.27 =     9.58 g   centroid (  -0.13,  42.79,  -235.15)
   hopper                     109.423 cm3 x 1.27 =   138.97 g   centroid (  -0.04,  -3.46,  -273.57)
   meter_housing              103.819 cm3 x 1.27 =   131.85 g   centroid (   5.80,   0.58,  -339.15)
   pocket_disc                 72.661 cm3 x 1.27 =    92.28 g   centroid (   0.11,   0.05,  -342.89)
   agitator                     4.288 cm3 x 1.19 =     5.10 g   (TPU)
   brush_holder                 3.544 cm3 x 1.27 =     4.50 g
   retaining_plate_chute       63.945 cm3 x 1.27 =    81.21 g   centroid (  13.19,  -0.43,  -372.68)
   electronics_bay             21.175 cm3 x 1.27 =    26.89 g
   bay_lid                      8.598 cm3 x 1.27 =    10.92 g
   sensor_cover (x2 bodies)     3.198 cm3 x 1.27 =     4.06 g
   count_windows (x4 bodies)    0.104 cm3 x 1.18 =     0.12 g
   PRINTED FLIGHT SUBTOTAL                          626.84 g
   (GSE, correctly excluded: service_stand 103.892 cm3 = 131.9 g ; chute_plug 6.718 cm3 = 8.5 g)

COTS / ESTIMATE (carried from cad/BOM.md; none of it is measured geometry)
   clip_plate (alu, interface STEP 11.523 cm3 x 2.70)      31.10 g
   stepper (vendor GROSS 0.38 kg -> carried 350 g)        350.00 g
   blind-mate PCB + Molex J1                               15.00 g
   sensor PCBs x2                                           6.00 g
   electronics (MCU/CAN/TMC2209/buck/count board)          65.00 g
   fasteners + inserts + plunger                           57.00 g
   O-ring + gaskets + 9 magnets                             8.00 g
   strip brush                                              3.00 g
   sleeve bearing igus JFM-2023-07                          1.70 g
   PTFE thrust washer                                       0.70 g
   COTS/ESTIMATE SUBTOTAL                                537.50 g

   EMPTY (solid printed basis)                          1164.34 g   (cad/BOM.md prints 1164.5 -- reproduces to 0.16 g)
   + 10 % CAD contingency                                116.43 g
   EMPTY, CARRIED (= the DRY figure)                    1280.77 g   vs CONTEXT <= 1500 g DRY -> MARGIN  +219.23 g   PASS
   + 250 granules x 1.18 g                               295.00 g
   LOADED @250, 100 %-infill basis                      1575.77 g   (margin  -75.77 g)
   + 421 granules (max-fill rib)                         496.78 g
   LOADED @421, 100 %-infill basis                      1777.55 g   (margin -277.55 g)
   EMPTY CG (mass-weighted, measured centroids + placed COTS) = (1.66, -7.08, -329.45)
   ESTIMATE EXPOSURE: 537.50 g of 1164.34 g = 46.2 % is COTS/estimate, of which 350 g is a vendor GROSS
                      catalogue figure that has never been on a scale
```

Readings, unchanged in substance from round 5:

1. **The CONTEXT requirement is on dry mass** and it passes with **+219.23 g**
   (round 5: +209.04 g — the round is 10.19 g *lighter* because the I-1 duct
   bore finally removed material; my independent number is +10.19 g, the notes'
   is +10.19 g, they agree).
2. I reproduce the package's 100 %-infill empty subtotal to **0.16 g** and do
   **not** dispute the shipped slicer-realistic headline (1432.5 g, +68 g; with
   the 61.0 g reserve 1493.5 g, **+7 g**). I did not re-derive the padded-EDT
   infill model this round; the 100 %-infill column above is my own and is the
   pessimistic bound, which is **1575.77 g @250, i.e. 75.77 g over** — stated,
   as B11.2 requires, not hidden.
3. The margin on the shipped basis is **+7 g with reserve**. Two of my findings
   below (N-i5, N-i6) are seal changes with essentially zero mass, so they do not
   move it; but there is no room left for anything that does.

---

### Findings — none blocking

**N-i5 (MAJOR, BOM one-liner) — the bay gasket cord cannot fit the groove it is
ordered for, so the "dust-tight bay" is not sealable as shipped.**
Measured groove: **1.550–1.600 mm wide × 1.200 mm deep**, section
**1.860–1.920 mm²**. `cad/BOM.md` orders **"2.0 mm silicone cord, 200 mm
(182.00 mm loop)"**: section **π/4 × 2.0² = 3.1416 mm²** = **164–169 % of the
groove volume**, and the squeeze against a flat lid is **(2.000 − 1.200)/2.000 =
40.0 %**. Static face seals want 15–30 % squeeze and ≥ 100 % groove volume; at
169 % fill the cord has nowhere to go and holds the joint open by
(3.1416 − 1.896)/1.58 ≈ **0.79 mm**, which is more than the whole groove depth.
**Fix is one character:** a **1.5 mm** cord gives **1.7671 mm² = 92–95 % fill and
20.0 % squeeze** — and is the cord this same BOM already orders for the fill-cap
gland. Nothing in the geometry needs to change.

**N-i6 (MODERATE) — the third bay entry is not a grommeted panel hole, and
nothing seals it.** `cad/BOM.md` orders **5 × "Ø6.0 cable grommet for a 2.0 mm
panel"** for "3 × electronics-bay entries + 2 × sensor-duct sockets". Measured,
only **two** of the bay's three entries are 2.000 mm panels (the Ø10.000 inboard
pair). The third is the **Ø10.400 OD / Ø7.400 ID spigot** through the bay roof,
which telescopes 4.000 mm into the hopper-side conduit's Ø11.000 bore with
**0.300 mm/side radial clearance = 10.0844 mm² of unsealed annulus**, and whose
own Ø7.400 bore leaves **19.2501 mm² free** around the Ø5.5 aircraft bundle. Both
paths run to the neck cavity and the open mate interface, so **43.0084 mm² gross
/ 29.33 mm² free of unsealed opening** stands between the outside world and the
control PCB. IP54 (ELECTRONICS §6.2's target) is not achievable through that.
Either order a grommet/boot sized to the Ø7.400 bore and say so, or model a
gland at the telescoping joint, or stop calling the bay sealed and call it
dust-**resistant** (N8's fallback).

**N-i7 (MINOR, record) — 43.309 mm of harness is deliberately uncovered**
(2 × 21.655 mm, motor and count-sensor cables, bay inboard face (±10, −62.000,
−350.100) → cartridge duct mouth (0, −48.000, −363.250)). Coverage
**92.94 %** clears B5.5's 90 %, and the loop is what makes the cartridge
removable, but it sits on the outside of the housing at Z ≈ −350…−363 — in the
downwash and landing-dust zone that RT-8 is about. It should be named in the
service section as "two service loops, sleeve them", not left implicit.

**N-i8 (MINOR, correction to `BUILD-NOTES-r6.md` §7) — the +Y reach-in headroom
did regress 2.50 mm.** The notes say the raised cap bar "tops out at −228.200,
i.e. 1.65 mm below the corridor floor, so it costs nothing", and the 95 × 45 ×
130 boolean is indeed still 0.0000. But the **largest clear corridor** on +Y
went **49.15 → 46.65 mm** at 95 mm width, exactly the 2.50 mm the cap top rose
(−230.700 → −228.200). "Costs nothing" is true against the 45 mm requirement and
false against the measured margin; the series number should be carried.

**N-i9 (MINOR) — thinnest dust barriers between the harness and the granules,
and on the conduit skin, are below the 1.95 mm this package uses elsewhere.**

```
downward z-scan at x=0 from the top-plate conduit bore floor (z=-233.55):
   y=-25.0 floor 4.95 mm | y=-30.0 4.95 | y=-40.0 2.00 | y=-50.0 2.00 | y=-60.0 2.00 | y=-69.0 4.95
radial wall between the Dia11.0 hopper-side conduit and the tank interior:
   z=-245  6.00 mm | z=-260  5.50 mm | z=-275  7.50 mm | z=-290 13.35 mm | z=-305 15.45 mm
outer skin of the hopper-side conduit: 1.500 mm at every z probed
```

**2.000 mm** of plate floor over the tank at y = −40…−60 and a **1.500 mm** outer
conduit skin. Both are printable (4 perimeters at 0.4 mm), neither is a
structural member, and both are unchanged from r11 — so this is a record, not a
demand. It is the number to quote if anyone asks how well the wiring is isolated
from the granule bed.

**N-i10 (documentation) — ELECTRONICS §7 states the bay interior as
46 × 22 × 38 mm; measured on `electronics_bay_r12.step` it is
52.000 × 24.600 × 38.000 mm** (walls |x| 26.000…28.000, inboard wall
−64.000…−62.000, lid inner face −88.600, floor −358.100…−356.100, roof
−318.100…−316.100). The doc is conservative, not wrong in a dangerous direction,
but §7 and §6.3 (which still describes the y −19 → −73 conduit; measured
y −21.000 → −81.000) should be re-based in the same pass as open issue 10.

---

### Summary for the round

| item | verdict | headline number |
|---|---|---|
| I-1 (round-5 BLOCKING) | **CLOSED** | **0/1745** axis points inside material vs **all 13** flight solids; Ø4.0 and Ø4.5 bundles **0.0000 mm³** on every leg; largest clear conductor **Ø5.00** (Ø5.50 motor stub); plate 71.850 → **63.945 cm³** |
| (a) reach-in corridor (directive 3 / B6) | **PASS** | 95 × 45 × 130 clear at **0.0000 mm³** on +X, −X and +Y; h = **43.500 mm**, a = **24.000 mm**; +X/−X clear to **52.00 mm** tall |
| (a) B6.3 QR actuation sweep | **NOT VERIFIABLE** | release half is drone-side, above Z = −171; clip plate **50.000 × 50.000 × 10.500** on a 48 × 48 neck = **1.000 mm/side** proud |
| (b) bay + PCB envelope | **PASS** | interior **52.000 × 24.600 × 38.000**; 42 × 34 × 12 board **0.0000 mm³**; gaps 5.000/5.000/1.800/2.000/7.600; ECO-7 bosses **Ø5.200, seat 5.000 mm proud, Ø2.100 × 4.900 pilot** |
| (b) entries / gasket / lid | **PASS** | 3 entries (Ø7.400 + 2 × Ø10.000), lands ≥ 1.500; groove **1.550–1.600 × 1.200**, closed loop **52.000 × 39.000**, perimeter **182.000 mm**, 120/120 stations; lid sweep and 4 driver columns **0.0000 mm³** |
| (b) harness vs granule space | **PASS** | **0.0000 mm³** in tank, metering chamber and chute, with three controls that hit (879.6459 / 1005.3096 / 628.3185 mm³) |
| (b) route coverage + sections | **PASS** | **92.94 %** covered; tightest section **Ø5.960** (the R8.00 elbow) at **27.9 %** fill; every section ≤ 27.9 % vs the 70 % ceiling |
| (b) "sealed / dust-tight" | **COMPLAINT** | **N-i5** cord 164–169 % of groove volume, 40.0 % squeeze; **N-i6** **29.33 mm² free** of unsealed opening at the roof spigot (10.0844 mm² annulus + 19.2501 mm² bore) |
| (c) refill / rest position (B12) | **PASS** | clear port **Ø46.000**; Ø13 drop path **0.0000 mm³**; lift **3.000 mm** to unlock, **6.000 mm** to clear, lateral to **+60 mm** at **0.0000 mm³**; can **8.000 mm** off the ground; tip **42.89°** / **50.04°** empty; capacity change **0.000 %** (hopper STL byte-identical to r10/r11) |
| (d) ground clearance / envelope | **PASS** | **129.384 mm** ground, **103.664 mm** to the real landing gear, prop **152.549 / 232.632 / 374.901 mm**, **0** vertices above Z = −171.000, 24/24 components watertight |
| (e) mass ledger | **PASS (dry) / over on the 100 % bound** | dry carried **1280.77 g** vs 1500 (**+219.23**); loaded @250 **1575.77 g** on the 100 %-infill bound (**−75.77**); shipped headline 1432.5 g, with reserve 1493.5 g (**+7 g**); estimate exposure **46.2 %** |

**Nothing on this list blocks the round.** To retire the two complaints that
touch directive 2's word "sealed", one BOM line has to change (**1.5 mm** cord,
not 2.0 mm) and one of three things has to happen at the roof spigot: a boot
sized to the Ø7.400 bore in the BOM, a modelled gland at the telescoping joint,
or the README saying plainly that the bay is dust-**resistant**, not sealed.
