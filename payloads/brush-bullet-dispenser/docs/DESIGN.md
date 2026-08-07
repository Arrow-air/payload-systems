# Brush Bullet Dispenser — Design

Rev-0 design package. This is the full story of how the design got here: what
was surveyed, what was traded, what six rounds of CAD found and fixed, what the
electronics contract specifies, what was *not* built, and what is still wrong
with it.

**Reading rule used throughout.** Numbers are labelled by provenance:
**[V]** verified against a cited source · **[D]** derived, arithmetic shown ·
**[M]** measured on exported geometry · **[J]** engineering judgement ·
**ASSUMPTION** unverified with a stated closure path. Requirements come from
[`../_run/CONTEXT.md`](../_run/CONTEXT.md), which quotes Thomas verbatim and
dated; the aircraft interface comes from [`../../../interface/ICD.md`](../../../interface/ICD.md)
v1.0-draft and the vendored quiver CAD.

---

## 1. The problem

Fly to a mesquite or juniper, hover at ~8 m AGL, drop 1–3 herbicide pellets
within 1 m of a scouted coordinate, fly to the next one. Do it in West Texas
dust, heat and wind, from a hopper holding at least 250 pellets, on a payload
that weighs no more than 1.5 kg loaded, powered from a 2 A switched rail, and
report a count that was **sensed**, not assumed.

The pellet is the hard part of the problem statement. Ø12 mm nominal
(ASSUMPTION ±1 mm tolerance, design to Ø13 worst case), **1.18 g** [V], molded
with a parting line and a slight barrel shape, and — Thomas, 2026-08-06 —
*"they do sometimes break/crumble but we try to filter those out before loading
the dispenser."* Pre-filtered at load time, but they keep breaking inside the
hopper from vibration. Every mechanism in this package is judged first on what
it does with a fragment.

A directive arrived mid-run (2026-08-06 23:03) that became the hardest single
requirement:

> "One thing I might be worried about is a possible jam if a fragment gets in
> to the pocket wheel slot, you'd have 1.5 brush bullets and it could prevent
> the wheel from turning"

That fragment-overfill wedge jam had to be designed against **and** explicitly
attacked by a critic that tries to construct it geometrically. §4.5 is what
happened when it did.

**Out of scope by direction:** no software phase (*"That can be a whole project
on its own"*) — the electrical/command **contract** only; no regulatory
workstream (*"we're already handling that"*).

---

## 2. Research

Five research passes, all with cited URLs, in `../_run/`:

| Doc | What it was mined for |
|---|---|
| [`RESEARCH-seed-metering.md`](../_run/RESEARCH-seed-metering.md) | Agricultural singulation: finger meters, vacuum discs, Kinze brush meters, celled plates. Source of the compliant-wiper pattern and of the anti-bridging outlet rules |
| [`RESEARCH-pill-counting.md`](../_run/RESEARCH-pill-counting.md) | Pharmacy counters: slat counters, vibratory singulation + optical count. Source of the dark-time gating philosophy for the count sensor |
| [`RESEARCH-projectile-feeders.md`](../_run/RESEARCH-projectile-feeders.md) | Paintball/airsoft force-feed hoppers. Source of the jam-detect / reverse-oscillate firmware pattern |
| [`RESEARCH-bulk-dispensers.md`](../_run/RESEARCH-bulk-dispensers.md) | Gumball machines, fish feeders, vending coils. Source of the "the disc top *is* the sump floor" trick that eliminates the throat |
| [`RESEARCH-drone-spreaders.md`](../_run/RESEARCH-drone-spreaders.md) | Existing UAV granule spreaders, and §1.3 the tebuthiuron pellet property data (US4172714) that every crush-strength margin in the package rests on |

The pellet mechanical properties are the weakest link in the whole evidence
chain and are flagged as such everywhere they are used: **0.36 MPa crush
strength / 41 N to crush a whole pellet** is **class-derived** from patent
literature for compressed herbicide pellets, not measured on the actual
product. Closure is an IFDC S-115 crush test on real pellets.

---

## 3. Mechanism survey and trade study

### 3.1 Survey — 17 candidates to 4

[`MECHANISM-SURVEY.md`](../_run/MECHANISM-SURVEY.md) scored 17 mechanisms 1–5
on count-accuracy potential, jam resistance (dust + fragments + bridging +
swollen pellets), buildability (3D-printable, COTS actuator inside the power
budget), mass economy, and glove-serviceability at a tailgate. Four champions
were carried forward, chosen for maximum diversity of failure mode rather than
for score alone:

| Champion | Principle |
|---|---|
| **A — rotary pocketed wheel** | one pocket = one pellet; count bounded by geometry |
| **B — PSD nest + flapper escapement** | flight-proven lineage (precision seed drills) |
| **C — servo single-cavity shuttle** | simplicity floor; one moving part |
| **D — dual-gate airlock** | geometric guarantee: two gates never open together |

Notable rejections and what survived them: augers and spinner spreaders were
rejected outright (**no notion of count** — 1/5), vacuum singulation on power
and dust, pneumatic pod firing on power and friability. Three things were
rejected as *mechanisms* but adopted as *features*: the Kinze compliant brush
wiper (folded into A/C/D), pharmacy vibratory-count **sensing philosophy**, and
the paintball **jam-recovery firmware pattern**.

### 3.2 Trade — three judges, four concepts

Each champion got a full concept document (`../_run/CONCEPT-*.md`, ~23 k each).
Three judges with different lenses scored them ([`JUDGING.md`](../_run/JUDGING.md)):
Judge 1 ≈ count integrity, Judge 2 ≈ field operations, Judge 3 ≈ integration.

| Concept | J1 | J2 | J3 | Total |
|---|---|---|---|---|
| **pocket-wheel (WINNER)** | 73 | 78 | 83 | **234** |
| servo-shuttle | 52 | 68 | 78 | 198 |
| psd-escapement | 70 | 55 | 70 | 195 |
| dual-gate-airlock | 63 | 42 | 58 | 163 |

Unanimous winner — first on all three ballots — but nobody was uncritical. The
dissent is worth keeping because it predicted most of what went wrong later:

- **Judge 1** carried three count-integrity holes against the winner.
- **Judge 2** flagged a glove-hostile lid, brush wear, fines self-generation,
  and near-empty skip storms. All four are still open (§7).
- **Judge 3** called the angled drop chute *"an accuracy liability"* and the
  power-cycle rest state *"the softest answer to a hard ICD clause."* The chute
  was straightened in a later round; the rest state became the §2.8 interlock
  table and an ICD change request.
- **The sharpest disagreement** was servo-shuttle: J1 ranked it last (*"the
  right thing to BUILD first and the wrong thing to FLY"*), J3 ranked it second
  for having the cleanest drop path. That 26-point spread is what pushed it to
  second overall despite losing two of three ballots.
- **All three ballots** independently flagged the unverified ±1 mm pellet
  diameter ASSUMPTION as load-bearing. It still is.

### 3.3 The winning concept in one paragraph

A stepper-indexed flat disc, 8 through-pockets on a Ø60 PCD, rotating on a
vertical axis between the hopper sump above and a stationary retaining plate
below. The **disc top *is* the sump floor**, so pellets fill pockets by gravity
across an open ~120° fill arc with no narrow throat to bridge (the
gumball-machine trick). A compliant brush wiper plus a rigid deflector nose
strips any second pellet or proud fragment back into the pool at the arc exit.
The retaining plate carries the pellet through a closed transfer arc to a single
Ø18 exit port, where it falls down a short chute past a modulated IR through-beam
that closes the count loop. Agitator fingers on the same shaft stir the sump on
every index for free. The only intrinsic failure mode is a **skip** — an empty
pocket — which the sensor converts into a harmless re-index rather than a
miscount.

---

## 4. CAD — six rounds

`cad/dispenser.py` is a single parametric build123d model, 2597 lines, that
exports STEP + STL for 10 parts plus the assembly, renders 7 PNGs, regenerates
`cad/BOM.md` with masses integrated from the actual solids, and **runs its own
verification harness on every execution**. `cad/verify_exports.py` re-measures
the exported files independently of the model.

Each round was attacked by four adversarial critics — interference,
pellet-path, buildability, mass-budget — who measure the **exported geometry**,
not the build notes. The score history is the interesting part of this project:

| Round | interference | pellet-path | buildability | mass-budget | What the round's root cause turned out to be |
|---|---|---|---|---|---|
| r1 | 6 FAIL | 4.5 FAIL | 6 FAIL | 8.5 PASS | first geometry; everything |
| r2 | 9 PASS | 5.5 FAIL | 5.5 FAIL | 9 PASS | **tangent unions** — parts built from zero-overlap primitives export as floating lumps |
| r3 | 9 PASS | 6.5 FAIL | 6.5 FAIL | 9 PASS | **assembly kinematics** — screws under roofs, sealed nut pockets, a trapped brush |
| r4 | 9.5 PASS | 8 PASS | 7 FAIL | 8.5 PASS | **architecture** — the agitator was a cartridge member that could never clear the roof |
| r5 | 4 FAIL | 5 FAIL | 8.5 PASS | 9 PASS | **the clip plate was never mapped** — 4 mount bolts landed in the blind-mate window |
| **r6** | **7 FAIL** | **5 FAIL** | **4 FAIL** | **8 PASS** | **the fixes for r5 created three new blockers** (§4.6) |

The pattern that matters: **every round's blockers were invisible to the
previous round's harness**, and each round's real deliverable was a new class of
automated check.

### 4.1 r1 → r2: the harness cannot see what it does not check

r1 built the stack. r2's critics found that 13 parts exported as 22 solids: the
agitator fingers were line-tangent to their collar (0.00 mm overlap), the latch
receiver ring floated 0.30 mm off the housing body, both IR sensor bosses were
tangent to the chute wall, and the fill cap exported as four disconnected lumps
with a 0.055 mm axial gap. A pairwise interference harness checks *different*
parts for overlap; it is structurally incapable of noticing that a *single*
part is not connected to itself.

**r3's fix was to the harness:** per-part `solids() == 1` connectivity plus an
assembly STL body count. Result: 13/13 parts single solids, 9/9 STEPs re-import
as one solid, assembly STL exactly 13 bodies. *"This class of defect is now
mechanically detected, not reviewer-detected."*

### 4.2 r3 → r4: geometry that no hand can reach

r3's blockers were all assembly-kinematics: features geometrically correct and
statically non-interfering that no tool, nut, screw or hand can ever reach.
Neither connectivity nor static interference can see this.

**r4 added an insertion / tool-path harness:** nut-insertion columns, Ø8 driver
corridors for every screw, an exact swept union of the brush along its slide
direction, set-screw shaft engagement, lid-screw approach paths, cartridge
drop-out envelope. Every one is a measured volume, printed on every run. A screw
with no driver path now fails the build the same way a collision does.

### 4.3 r4 → r5: no stand-in probes for motion

r4's remaining blocker was not a dimension error but an architecture error: the
agitator was clamped to the disc hub, making it a cartridge member whose fingers
had to pass a solid roof the cartridge could never clear — 853 mm³ of swept
interference over 12 mm of descent. r4's own tool-path harness had "verified"
the cartridge drop-out with a **Ø26.4 cylinder standing in for the real part**.

**r5 removed the agitator from the cartridge entirely** — it is now a free rotor
sitting on the sump floor, centred by the disc hub and driven by a hex spigot,
so the cartridge slides straight out of the hex. The hub runs in a COTS flanged
sleeve bushing (igus JFM-2023-07, ID20/OD23/L7) seated in the roof, which also
closed r4's *"no bearings anywhere in the design"* gap.

**Harness rule adopted in r5: no stand-in probes for motion.** Every service
motion is now a swept union of the *actual exported solids*, stepped, against
every static part — cartridge drop-out 21 steps × 4 members, wiper slide-out 20
steps × 2 parts, agitator lift 16 steps, fill-cap lift, latch swing.

### 4.4 r5's humiliation: the interface nobody had measured

r5 scored **4** on interference. The reason is the most instructive failure in
the run. Every round up to r5 had bolted the payload to the clip plate at
(±6.5, ±10.5) — a pattern that dispenser.py "verified" with a Ø2.4 × 10 probe
reading 0.775 mm³ of residual material against a `USE_CB_PATTERN = v_cb < 5.0`
threshold.

The critic mapped the vendor STEP by 0.05 mm point containment. The clip plate
is a 4.0 mm solid slab plus a perimeter frame with a **16 × 24 mm through-window**
at x ±8, y ±12 — and the (±6.5, ±10.5) pattern sits **inside that window**,
1.50 mm from each edge. The four mount screws carrying a 1274 g loaded payload
clamped **air**. The probe had returned a false positive on a window, not a
hole. The real mounting holes are 4 × Ø2.96 at **(±19, ±19)**.

The same round found the blind-mate pads **35 mm out of position in Y**, with
the build notes calling the pedestal "shimmable" — shimming is in Z; the error
was 35 mm in Y; and the closing data had been in the referenced quiver files and
the ICD the whole time.

**The lesson generalised into a rule the red team later re-applied:** a check
whose only possible outcome is "pass" is not a check. `verify_exports.py` still
contains probes of this shape (§7, RT-20).

### 4.5 The fragment wedge jam — the directive, and what the critic did to it

Thomas's 23:03 directive demanded four things with geometry and numbers:
rejection before wedge, shear capability as backstop, detect + recover, and
stated pocket geometry. r6's answer:

1. **Rejection before wedge.** A 25° entry ramp on the roof underside, ceiling
   falling 10.24 mm at θ = 129° to 1.50 mm at the PCD [M], plus a 30° rigid
   deflector nose with a 0.6 mm blunt face at disc + 3.0 mm, plus a nylon strip
   brush with 6.25 mm of free trim at tip = disc + 1.20 mm. Nose and brush are
   one field-replaceable part.
2. **Shear as backstop.** Load budget at the disc **190.7 mN·m** [D] — bed
   friction 28.6 (Janssen p_sat 1111 Pa × 1894 mm² = 2.1 N at µ 0.4) + agitator
   41.1 + deflector nose 13.1 + bearing/thrust 11.5 + detent 96.5. Normal drive
   **390 mN·m (2.1×)**, recovery **650 mN·m**. At the pocket lip that is 12.2 N
   metering / **20.4 N recovery** against **7.5 N** to shear a Ø6 fragment at
   the class 0.36 MPa — and deliberately **2.0× under** the 41 N whole-pellet
   crush figure, so the driver cannot become a pellet grinder.
3. **Detect + recover.** Hall phase decode (9 magnets, 2 → 3 Halls) as primary
   stall detection with bounded reverse-oscillate recovery; the count sensor
   stays armed throughout so recovery cannot manufacture a phantom count.
4. **Pocket geometry.** Bore Ø15.00 × 14.00 deep + 0.50 mm under-gap = 14.50 mm
   seat [M]. A worst-case Ø13 pellet seats **1.50 mm below the shear line**; a
   stacked second sphere protrudes 11.5 mm and is unmissable.

**Then the pellet-path critic constructed the jam anyway.** Solving against the
*measured* pocket chamfer (bore r7.50 at 2.00 below the top, flaring 45° to
r9.50) with a seated Ø13 pellet: a **Ø5.0 fragment nested in the chamfer sits
+1.80 mm proud; a Ø6.0 fragment +2.95 mm**. The roof clearance is 1.50 mm and
the deflector nose sits at 3.00 mm — so there is a **1.50–3.00 mm blind band**
where an object passes the nose untouched and meets only compliant bristles,
which cannot reject a rigid wedged fragment. Only Ø7.0 (+4.08 mm) reaches the
nose.

The jam is still defeated — but by **crushing under the entry ramp** (14.1 N
normal at metering current vs 7.5 N to shear, 1.9×; 23.4 N at recovery, 3.1×),
which is CONTEXT defence **2**, not defence **1**. The build notes claimed
defence 1. **The fix is one parameter: `NOSE_GAP` 3.00 → ≤1.50 mm.** It is not
applied in this revision.

This is the single best argument for the adversarial-critic structure: the
directive asked for a critic that would *try to build the jam*, and it built one
that the design's own documentation said was impossible.

### 4.6 r6 — what it fixed, and the three blockers it created

r6 fixed r5's real blockers: the mount pattern moved to the verified (±19, ±19),
the entry-ramp geometry became a true underside ramp with no square step, the
brush holder became rigid-plus-compliant, and the drive became a **5.18:1 geared
NEMA 14** — because the previous "the motor *is* the torque limiter, 12× below
crush" framing made the directive's shear requirement *unachievable* (5.6 N
available vs a fragment needing 7.5 N).

It then failed three of four critics on new ground:

- **The entry ramp was cut with a half-space, not a sector.** `dispenser.py`
  ~L737-750 builds the ramp from `ramp_half & Box(400,200,100)` at y ≤ 0, then
  rotates 130°. The half-plane covers θ = 310° through 0° to 130°, so the same
  25° undercut is **mirrored at θ = 310°**. Measured on the exported B-rep by
  sector boolean: roof material is 138.4 / 138.4 mm³ (full 9.00 mm) at
  θ 309–310°, and **2.2 / 138.4 mm³ (0.14 mm mean) at 310–311°** [M]. Point
  probes read **0.000 mm roof thickness at θ = 310.0° at r = 20.5, 24.5, 30, 32,
  36, 39.5, 44, 46.5** — an open through-slot from the pellet bed straight into
  the 1.50 mm metering arc, **downstream of every rejection feature**, plus a
  9.00 × 26.5 = 238 mm² vertical face facing directly into the direction of disc
  travel. This is exactly the square-stub failure r5 blocked at the entry,
  reproduced at the far end of the same cut and never audited. It is also what
  the builder's own "meter_housing min wall 0.01 mm" statistic was reporting,
  mis-attributed to the entry ramp.
- **No torque path to the disc.** `dispenser.py:841` cuts the disc bore as a
  plain `Cylinder(MOTOR_SHAFT_R+0.05)`. Measured bore radius: **3.06 mm at every
  one of 36 angles at both heights** [M] — no D-flat, so the vendor's 12 mm
  D-cut transmits nothing across a 0.12 mm-clearance round bore. The backup grub
  screw (`dispenser.py:847`) is a **buried blind hole**: radial rays show void
  to r = 10.60 mm and then solid disc material out to r = 24.47 mm, so the screw
  cannot be inserted or driven. The builder's self-check probes only x = 3–10 mm
  — inside the buried section. Another can't-fail probe.
- **The gearbox cannot be bolted on.** `dispenser.py:337/971` assume a 26 mm
  **square** M3 pattern; the exported plate has its 4 holes at θ = 45/135/225/315°,
  r = 16.8–19.9 [M]. The 14HS13-0804S-PG5 datasheet dimensions the output flange
  as **4 × M3 on a Ø26 ± 0.15 bolt circle** — r = 13.0 **on the axes**. And the
  correction is not a parameter tweak: holes at r = 13 (edge r = 11.4 for a Ø3.2
  clearance hole) collide with the Ø22.20 pilot bore (edge r = 11.10), leaving a
  0.3 mm web, and the PTFE thrust-washer seat loses its inner land.

Round 6 also produced a fourth finding worth carrying: the drop-window
derivation measures a window the pellet never uses. The pellet rests on the
*stationary* retaining plate and loses support when its contact crosses r = 9.75,
i.e. **3.16–6.78° into the 22.5° index move (14–30 % of the move)** [M] — while
the disc is still turning, not during the 150 ms dwell the "2.8× fall margin"
was computed against. At release the pellet carries ω × 32 mm of lateral
velocity: **0.126 m/s at 225 °/s → 0.16 m of drift** over the 1.28 s fall from
8 m, against a 1 m total budget. This is why the electronics §3.4 release-speed
clause (≤90 °/s) exists.

### 4.7 Where r6 actually landed — measured

Everything below is **[M]** on `cad/exports/*_r6.*`, reproduced independently by
the critics.

**Envelope and integration**

| | |
|---|---|
| Bounding box | X ±75, Y −90…+75, Z −366.4…−171.0 → **195.4 mm** stack |
| Ground clearance at rest | **181.5 mm** (gear lowest point Z −547.884) vs ≥40 mm required — 4.5× |
| Ground clearance, foam fully crushed | 176.5 mm |
| Min payload ↔ landing gear | **83.41 mm** (independently 83.42) |
| Prop clearance | 152.5 mm vertical; true min in-plan gap **251.13 mm**; zero plan overlap |
| Mount pattern | 4 × M2 at (±19, ±19); Ø2.90 holes, Ø3.90 head pockets |
| CG | printed-parts centroid (1.73, −3.24, −257.05); **3.67 mm** in-plane offset from the mount axis |

**Pellet channel**, worst-case Ø13 pellet, every ratio stated:

Ø46 fill port (3.5×) → Ø140 hopper → 68.0° cone to Ø95 → **120° × 26.50 mm
annular outlet window (2.04×, the governing arching dimension)** → pocket bore
Ø15.00 × 14.00 + 0.50 under-gap = 14.50 mm seat (**1.15×, the tightest true
channel**) → Ø18.00 exit port + 0.75 × 45° chamfer (1.38×) → Ø22.0 × 50 chute
(1.69×). Pinch points: roof underside 1.50 mm, nose underside 3.00 mm, bristle
tip 1.20 mm, disc rim gap 1.00 mm, under-gap 0.50 mm, agitator film 0.55 mm.
**Pellet transit verified at 23 stations, 0.000 mm³ everywhere** in-model and
11/11 stations re-run independently on the exports.

**Capacity**

963 cm³ usable → **422 pellets** at worst-case barrel packing (498 g), 587 on a
sphere basis. **1.69× the 250-pellet hard minimum.** Fill ribs measured at 248
("250" line) and 420 (brim). See RT-5 in §7 — the packing constant behind these
ribs is wrong in the conservative direction for volume and the *dangerous*
direction for mass.

**Mass ledger** (100 % infill from measured solids, CF-PETG 1.25 g/cm³)

| | |
|---|---|
| Printed parts (10) | 401.1 cm³ → 501.4 g |
| Geared stepper | 310.0 g (**ASSUMPTION** — vendor publishes only 0.38 kg gross; electronics §8.7 corrects to 290 g [V]) |
| Clip plate, electronics, fasteners, PCB, magnets, brush, bearing | 181.7 g |
| **Empty** | **993.1 g** → +10 % contingency → **1092.4 g carried** |
| **Loaded @ 250 pellets (295 g)** | **1387.4 g — 113 g under the 1.5 kg ceiling** |
| Brim @ 422 pellets | 1590.4 g (pellets above the 250 baseline are exempt per CONTEXT) |

Sensitivities all pass: stepper at 380 g gross → 1475 g; steel clip plate →
1452.3 g; CF-PETG at 1.31 g/cm³ → 1412.6 g. The mass-budget critic rebuilt the
ledger independently at realistic slicing (4 walls + 25–40 % infill, with a
padded-EDT correction to the builder's voxel erosion) and got **1257.5–1285.1 g
loaded @250**, i.e. 215–243 g of margin. The package headlines the conservative
number.

**Over-1.0 kg justification, partitioned** (CONTEXT requires every 100 g above
1.0 kg be justified): 387.4 g over, all attributed — geared stepper **310.0 g**
(the gearbox *is* what makes the fragment-shear requirement achievable: 20.4 N
vs r5's 5.6 N, while the driver current limit keeps normal metering 3.4× under
the crush load) + capacity oversizing 46.2 g (the 36 mm of cylinder wall above
the 250-pellet line) + latch ring/lugs 16.5 g + fastening/phase hardware 15.2 g.
Nothing unattributed.

**Manufacturing**

All 10 parts fit a 220 × 220 × 250 mm bed (largest sorted extents 150.0 × 150.0
× 95.7, the hopper). Support-needing area in the BOM's chosen orientations
ranges 0.0–8.9 % and reproduces to 0.1 % under independent medial-axis
measurement. No unreachable support found. The ≥2 mm structural rule holds
everywhere except the disclosed 30° deflector wedge (`brush_holder`, 13.1 % of
volume under 2 mm) and the TPU agitator fingers. 10/10 STEPs re-import as one
solid; **9/10 STLs watertight** — `meter_housing_r6.stl` has one non-manifold
edge at exactly r 32.50, θ = 310.0°, z = −274.20, i.e. precisely on the ramp-bug
line. The build notes claim 10/10, which is the opposite of what their own
`verify_exports.py` prints.

---

## 5. Electronics and the interface contract

Full document: [`../electronics/ELECTRONICS.md`](../electronics/ELECTRONICS.md)
(2129 lines). It is hardware and contract only — no firmware design, per the
scope cut. Where behaviour is unavoidably firmware, it is stated as a
*requirement on the hardware* ("the hardware shall make X measurable") plus a
contract clause.

### 5.1 The architecture decisions that carry weight

**Motor on 12VSW, everything else on 12V_PL.** K1 (the relay added to the Main
PCB specifically for this dispenser) becomes a true galvanic disconnect of the
only actuator that can release herbicide — while the payload stays alive to
report count and faults with the motive rail dead.

**A current-chopping stepper driver, and why that decides the whole power
argument.** A chopper is a constant-current load, so worst-case 12VSW draw is
**0.30 A** and — the key property — **input current *falls* ~19 % at stall**
(0.298 → 0.242 A), because the mechanical term goes to zero while phase current
stays regulated. There is no stall surge to fuse against. A comparable 12 V
brushed gearmotor with a 3 Ω armature stalls at **4 A**, twice the aircraft's F1
rating: a single wedged fragment would open a fuse *inside the aircraft* and end
the sortie.

| Mode | I_pk | Input | 12VSW current |
|---|---|---|---|
| Metering index | 0.37 A | 1.73 W | 0.144 A |
| Recovery, moving | 0.63 A | 3.57 W | **0.298 A** |
| Recovery, **stalled** | 0.63 A | 2.91 W | 0.242 A |
| Parked | 0 | ~0.05 W | ~0.004 A |

Fuse coordination: payload eFuse 0.60 A trips first (<1 ms), firmware trips on
the ILM pin at 0.45 A/20 ms to cover the intermediate regime the limiter is
blind to, aircraft F1 at 2 A never sees it — **1.9× below the payload limiter,
6.7× below F1**. Stated honestly: *the motor rail can protect itself; the logic
rail can only tell you* — the payload cannot cut its own 12V_PL, so its only
action on `OVERCURRENT` is to latch, refuse to arm, and report.

**The torque ceiling is a resistor, not a register.** The TMC2209's
`IHOLD_IRUN` reset default is IRUN = 31 = full scale, and it is volatile across
every VM cycle. Sizing **R_SENSE = 0.50 Ω** so that full scale *is* the 0.63 A
recovery current (20.5 N at the pocket lip, exactly 2.0× under the 41 N crush
figure) makes the "pellet grinder" state **physically unreachable by any
firmware or UART fault**. Moving the limit is a board change. That is the
intended trade: harder to get wrong in the field, harder to tune on the bench.

**Default-safe at the pin level.** Both the motor-eFuse EN (TPS2595) and the
TMC2209 ENN are pure high-impedance inputs with no internal pull [V, both
datasheets]. Without external pulls, the motor rail and the output stage are
undefined for the entire interval between rail rise and GPIO configuration, and
after every MCU reset. Hence 100 kΩ pull-**down** on eFuse EN, 100 kΩ pull-**up**
on ENN, plus an external watchdog — and §2.8 tabulates the guaranteed state of
every interlock element for every power and reset event.

**Count sensing — two staggered chord beams.** The single centred pencil beam in
the concept and the r6 CAD has a **5.2–14.7 ms dark-time spread** depending on
where the pellet passes, which is disqualifying: the concept's "10–35 ms = one
pellet" gate would reject a real pellet hugging the chute wall. Two beams at
x = axis ± 3.0 mm, counting the *longer* dark time, guarantee **10.4–14.7 ms for
any pellet at any lateral position** (a pellet's centre is always within 3.0 mm
of at least one beam). ECO-9 additionally staggers them 6.0 mm vertically, which
converts the count from a dwell test into a **per-event velocity measurement**
(±1.7 %, size- and position-independent) and closes the 18 % wall-rubbing
allowance.

The gate itself was corrected during review and the correction is instructive:
the shipped 6 ms lower bound meant **85 % of lateral positions of a Ø8 fragment
would be counted as a whole pellet** — the payload stops at N having delivered
N−1 pellets and a crumb, and reports a verified count of N. CONTEXT says
*"dispense exactly N **pellets**"*; a 6 ms gate verifies a count of *objects*.
Revised gate: **<9.7 ms = fines, not counted · 9.7–25 ms = one pellet · >25 ms =
double/hang/lodged → `OVERCOUNT`/`CHUTE_BLOCKED`**, sitting in the clean
separator the geometry provides (Ø8 best case 9.03 ms, Ø11 guaranteed 10.4 ms)
with 7 % margin each side.

**Emitters run continuously.** Gating them to the 400 ms dispense window made
`UNCOMMANDED_DROP` — *the worst outcome this payload has* — unreachable by
construction: a pellet shaken out in cruise would produce no event, no telemetry
and no record. Continuous monitoring costs **0.07 W** on a 25 W rail. Standby
draw is now lower than the earlier draft's *dispensing* figure.

### 5.2 The command contract

**DroneCAN on CAN2 is the command interface; FMU_CH1 PWM is arm-only.** PWM is
FC→payload with no return path, so **PWM alone cannot satisfy CONTEXT's
"count must be VERIFIED (sensed)"**. Three vendor-specific DSDL types
(`Dispense`, `ClearFault`, `SetMode`) plus `Result` and `Status` broadcasts.
Data-type IDs are deliberately **not invented** — they must be allocated in the
project-quiver DSDL registry.

The semantics are the actual deliverable:

1. **`Dispense(seq, N)` means "ensure a total of N pellets have been delivered
   for transaction `seq`."** Not "index N times", not "add N". `{seq, commanded,
   dispensed}` is persisted in **FRAM** on every verified count.
2. **Idempotent.** A repeat of a completed `seq` returns `ALREADY_COMPLETE` and
   dispenses nothing — because DroneCAN requests get retried, and a retry that
   re-doses a plant is a regulated over-application.
3. **Resumable.** ICD §3 requires tolerating power removal at any time; a
   re-sent `Dispense` after a mid-command power cycle completes the *remainder*.

Two authority separations were forced during review and both are worth naming.
`ACK_FAULT` was **removed from `Dispense.Request` and given its own service**:
in the earlier draft a single CAN frame could clear a latched `JAM_UNRECOVERED`
*and* command a dispense of the mechanism that had just failed. `ClearFault` now
carries an `operator_id`, so a cleared fault is attributable. And the PWM armed
band **moved from 1400–1600 µs to 1750–1850 µs**, because 1500 µs is the
near-universal FC trim for an unassigned channel — the payload could arm itself
as a side effect of an FC boot or a parameter reset, with no operator action.

Timing contract: release move ≤90 °/s (this is the accuracy clause — it buys
0.06 m), dwell ≥150 ms, return ≤240 °/s, **634 ms per pellet**, N = 3 nominal
**1.9 s**, N = 3 with two skips 3.2 s (the FC must hold station that long).
16 fault flags are frozen by bit number, with bits 5 and 12 deliberately split
so the operator learns whether the problem is on the **aircraft** (K1 open, F1
blown) or in the **payload** (own eFuse off) — the difference between "check
FMU_CH2" and "send it to the bench".

### 5.3 What electronics raised against the rest of the package

Twelve ECOs against the r6 CAD, of which the load-bearing ones are **ECO-3**
(two sensor apertures at x = 29/35, replacing the single centred beam),
**ECO-9** (6 mm beam stagger), **ECO-1** (aluminium bay lid, light-anodised,
α ≤ 0.4 — because parked-in-sun wall temperature computes to **77.5 °C** against
CF-PETG's 80 °C Tg), **ECO-8** (third Hall, because the 2-bit decode maps
"stopped mid-move with the port leaking" and "a Hall has failed" onto the same
code with opposite correct responses), **ECO-10** (motor NTC — sustained
recovery puts the motor case at ~95 °C), and **ECO-11** (magnet retention: 9
loose magnets unqualified for vibration, where a migrated magnet is *both* a
hard jam and loss of the safe-state decode).

**None of the ECOs were merged into `cad/dispenser.py`.** That is RT-3.

Ten bench tests gate the build (B1–B10), and one **ICD change request** is
levied: **FMU_CH2 / K1 default state at FC boot is unspecified** — the only
non-firmware interlock in the chain has undefined behaviour at FC boot, in-flight
FC reboot, RC failsafe and parameter reset.

Electronics BOM: **$92.68 excluding the motor, $129.45 with it.** Electronics
mass ≈55 g, inside the ledger's 65 g line.

---

## 6. Simulation — not delivered

**`sim/` does not exist.** CONTEXT asked for a Monte Carlo that states the
honest wind limit for the 1 m accuracy requirement. The run did not produce it,
and this package does not pretend otherwise.

What that means is worse than a missing folder, and the gap review is blunt
about it: **the 1 m accuracy requirement has no owner anywhere in the package.**
The entire run optimised the *mechanism*. The words wind, drift, AGL, canopy and
bounce appear nowhere in the design documents in the sense that matters. The
only accuracy work in the whole package is the electronics §3.4 release-speed
clause, worth 0.06 m.

Two reviewers integrated the ballistics themselves so that the numbers exist
somewhere. **These are review computations, not a delivered simulation, and they
have not been cross-checked against each other or against a validated model.**
Both used the verified pellet (1.18 g, Ø12 mm) with quadratic drag at Cd 0.47:

- Fall time from 8 m AGL: **1.28–1.32 s**; impact velocity ~11.3 m/s.
- Crosswind drift is a **bias**, not a scatter: **0.09 m per 1 m/s** — drift
  from 8 m is 0.19 m at 2 m/s, 0.47 m at 4, 1.00 m at 6.6, 1.37 m at 8.
- **The payload is therefore not the accuracy driver — hover hold is.** Monte
  Carlo P(land within 1 m) at wind 0/3/5/8 m/s: **99.3 / 97.6 / 92.5 / 74.0 %**
  at 0.3 m 1σ hover error, but **94.6 / 91.1 / 84.2 / 67.0 %** at 0.4 m — i.e.
  the 90 % gate **fails in still air** if hover hold is 0.4 m 1σ.
- Honest limit for ≥90 % within 1 m at 8 m AGL with 0.3 m 1σ hover:
  **4.46 m/s (10 mph)**; **7.3 m/s** if you release at 4 m instead.
- Because the drift is a bias, **aiming upwind cancels it** — a 30 % wind-estimate
  error at 8 m/s still yields 95.6 %. This is the cheap fix, and it is an
  *interface* fix, squarely in scope: `Dispense.Request` has no release-offset
  field, no altitude advisory and no wind/hover-quality gate.

Three terms even the briefed sim would have missed, all noted for whoever builds
it: **canopy interception** (the target is a shrub; "within 1 m of the
coordinate" is a proxy for "on soil in the root zone", and the word canopy
appears nowhere in the package), **bounce and roll** at 11.3 m/s onto caliche,
and **tumbling-Cd spread** (0.78 m vs 0.47 m of drift at 4 m/s depending on
attitude).

**What a delivered sim must do:** sweep hover σ as a first-class axis, not a
fixed assumption; state the wind limit at 8 m and at 4 m; and produce the two
contract changes the accuracy requirement actually needs — an FC-provided aim-point
offset, and a `HOLD_QUALITY` refusal so the payload declines to dispense when the
aircraft is not holding well enough for the drop to count.

---

## 7. Risk register

Sources: [`../_run/RED-TEAM.md`](../_run/RED-TEAM.md) (21 numbered findings,
severity-ranked, each with a fix and a test) and
[`../_run/GAP-REVIEW.md`](../_run/GAP-REVIEW.md) (7 coverage gaps). Nothing here
is downgraded from how the reviewers wrote it. Both reviewers measured the
exported geometry themselves rather than restating the build notes.

### 7.1 Critical — must close or the package cannot be built

| ID | Risk | Fix | Test that closes it |
|---|---|---|---|
| **RT-1** | r6 failed 3 of 4 critics and `dispenser.py` has not changed since. Three blockers reproduced independently: θ = 310° roof through-slot (0.00 mm at all 8 probe radii), disc bore r = 3.06 mm at all 24 angles (no D-flat → no torque path), gearbox holes on a 26 mm square vs the datasheet's Ø26 bolt circle | Run round 7 | The existing four-critic harness, re-run to PASS |
| **RT-2** | **No electrical connection to the aircraft.** 19.35 mm blind-mate gap (8.85 mm even at the highest legal pad plane) vs ≤2 mm plunger travel. The notes offered "0.00 mm³ of payload inside the shaft" as proof the PCB *is* in the shaft — that metric is the proof it is not. The escape route is foreclosed: the payload clip half nests at most 0.54 mm into the drone-side channel over 8 tested poses | **ICD-side escalation**, not a payload open issue. 10.5 mm is payload-controllable; the residual is aircraft-side | Physical mate against the real 2112 + 3331 set |
| **RT-3** | **"Verified count" exists only in a document describing hardware that is not in the CAD.** ECO-3 and ECO-9 never entered `dispenser.py` (L1005-1017 still cuts one Ø3.2 tunnel per side on the bore diameter in a 12 mm boss); `cad/BOM.md` still specifies the TSSP4038 receiver that ELECTRONICS §4.4 rejects | Merge ECO-3/ECO-9/ECO-4 into r7; update BOM | B1 dark-time survey (≥200 real drops + ≥100 fractured Ø7–10 mm pieces) |

### 7.2 High

| ID | Risk | Fix | Test |
|---|---|---|---|
| **RT-4 / G1** | **The 1 m accuracy spec has no owner**, and the un-written sim was about to be handed the assumption that decides it (§6). The 90 % gate fails in still air at 0.4 m 1σ hover | Sweep hover σ as a first-class sim axis; add an FC aim-point offset and a `HOLD_QUALITY` refusal to the §5 contract | Deliver `sim/`; flight-test hover hold |
| **RT-5** | **Fill marks are calibrated on a 40 %-packing constant** (`PELLET_VOL_WORST = 2.28 mL/pellet`) vs ~0.60 random-loose for real spheres, so "250 pellets" is really 250–370. Filling to the "250" rib (z = −222.6) with nominal pellets gives **≈370 pellets / 438 g → ≈1530 g all-up, over the ceiling**; the brim (z = −196.9) gives ≈638 pellets / 753 g → ≈1845 g. The 1.5 kg ceiling is currently an operator decision made by eye, inside an opaque black hopper | **Fill by mass (295 g).** Add `Fill` / `dispensed_since_fill` to the contract. Restate the ledger at nominal packing | Weigh 20 fills; measure real packing fraction |
| **RT-6** | **Black hopper + PEG-bound pellets at ~74 °C parked in sun.** The BOM's carbon-filled (black) material directly contradicts ECO-2/ECO-1's α ≤ 0.4 requirement; every structural check is implicitly at room temperature | Light external finish on the whole payload, not just the lid | **Loaded-hopper solar soak** (added to B4) |
| **RT-7** | **The hopper cannot be sealed** — the chute is permanently open — against a pellet that swells 2–3× **irreversibly** when wetted. One wetted pellet is a hard jam | Chute closure or a desiccant path; specify loaded-standby limits | Humidity / swollen-pellet jam test |
| **RT-8** | The dust analysis looks *up* when the dust comes from *below* — the permanently open chute faces the rotor downwash and the landing plume | — | Landing dust cycle added to B2 |
| **G2** | **Nobody did the mission arithmetic.** Quiver hover endurance is **25–31 min** [V, `/tmp/pq-main/docs/index.md:24`]. At 1–3 pellets/target, 250 pellets = 83–250 targets ≈ 25–42 min of flying (ASSUMPTION 12–20 s/target) — so one hopper load is **1–3 batteries' worth**, and the run answered "more capacity is good" with 422 pellets (+203 g carried every flight) without ever computing targets per flight. The contract cannot express inventory: no load-set command, no `pellets_remaining`, and the only empty signal is `EMPTY_OR_BRIDGED` at ≥8 consecutive skips — **discovered at a target, after that plant got a partial dose** | Three lines of DSDL | — |
| **G3** | **The dock and the dispenser have never read each other.** On-aircraft refill is impossible (measured: the fill cap needs 58 mm of lateral travel in a 10.5 mm gap), so a dock built for unattended repeat sorties can replenish electrons forever and pellets never — and in the below-grade silo case, refill means climbing into a 1.15 m cavity to unlatch a 1.1–1.6 kg herbicide payload off the belly. **Neither project considered a swappable pre-filled hopper cartridge.** Also un-owned: loaded-standby spec, and the fact that the ICD change request (K1 state at FC boot) is exercised *by the dock's wake circuit*, unattended, in a closed box, with 12V_PL dark so `UNCOMMANDED_DROP` is undetectable | Swappable cartridge; close the ICD CR | — |

*One G3 sub-item is good news and is recorded because nobody had noticed it:*
the payload is 150 × 165 × 195.4 mm with ≈58–59 mm of deck clearance against the
dock's ≥50 mm gate — **it passes**, and it closes the dock's open payload-envelope
question. The dock's own model had assumed 67.9 mm; the real payload hangs 8.5 mm
lower.

### 7.3 Moderate

| ID | Risk |
|---|---|
| **RT-9** | Mass creep is monotonic — **41 % in six rounds** — and every open blocker adds more |
| **RT-10** | Compliance criteria were re-based when they stopped passing. Specifically, the MAX fill rib moved to the volumetric brim once the quadruple-conservative rule returned 242 pellets, *below the 250 hard minimum*. The build notes argue this is honest (the rule became infeasible, not binding) and print both no-exemption numbers anyway — but the pattern is named here so a reader can judge it |
| **RT-11** | The recovery torque may crush **whole** pellets at the low end of the crush distribution, manufacturing the fragments it is recovering from. Closure: **S-115** |
| **RT-12** | **No fines budget anywhere**, and the running clearances (1.0 mm rim shear gap, 0.50 mm under-gap, 0.55 mm agitator film, the wiper contact, the new deflector plough) *are* the fines reservoir — and they all feed the only count sensor. Closure: **S-116** |
| **RT-13** | A 1.4–1.85 kg herbicide payload hangs on a COTS clip with **no secondary retention and no rated load**. Closure: 10 g retention pull test |
| **RT-14** | The refill procedure has no stable rest position, no tooling, and handles a dusty herbicide by hand |
| **RT-15** | A live open issue (fill-cap retention) was **deleted rather than closed** between rounds |
| **RT-16** | Vibration is qualified on the electronics side (B8) and **unqualified on the mechanical side** |
| **RT-17** | CG and its excursion are nowhere in the package; the red team computed them so the shock case has an input (3.67 mm in-plane offset from the mount axis) |
| **G4** | Hopper at 10 % full: skip storms are a known issue, but **dispensable** capacity — as opposed to volumetric capacity — was never established |
| **G5** | Pellet-to-pellet variation: everyone converged on *diameter* and stopped. Mass, density, crush strength and sphericity distributions are all unmeasured |
| **G6** | **There is no structural load case anywhere in the package.** No landing shock, no gust, no clip-plate load path analysis |

### 7.4 Low

| ID | Risk |
|---|---|
| **RT-18** | The fill ribs are proud internal shelves sitting in the flow zone |
| **RT-19** | Documentation integrity: measurements are repeatedly quoted with the sign of the claim (e.g. "10/10 STLs watertight" against the verifier's own 9/10; drone-side pin tips quoted from a mis-identified connector housing, making every derived margin 1.58 mm optimistic) |
| **RT-20** | **The "independent checker" is not independent.** `verify_exports.py` shares the builder's assumptions and missed the non-manifold edge its sibling tool reports. This is the same can't-fail-probe pattern that hid the clip-plate blunder for four rounds (§4.4) |
| **RT-21** | Residual count-contract items worth keeping visible |

### 7.5 What the reviewers checked and found sound

Recorded so the silence above is legible as deliberate: the **power and fuse
coordination and the §2.2–§2.8 interlock state table are the strongest work in
the package**; the FRAM idempotency/resume semantics are correct and the 15 ms
hold-up vs 150 ns write margin is real; the printability statistics reproduce
(part volumes re-measured to 0.03 %); ground clearance (181.5 mm) and prop
clearance are comfortable and independently confirmed; and the pellet is dense
enough that **wind drift alone is not the accuracy problem** — hover hold is.

---

## 8. What closes what

The red team's stated gate for calling this package rev-0:

1. RT-1 / RT-2 / RT-3 **closed or explicitly declared unmet in `README.md`** —
   done, they are declared unmet in [`../README.md`](../README.md).
2. Bench tests added: **S-115** (pellet crush distribution, RT-11), **S-116**
   (fines generation rate, RT-12), **loaded-hopper solar soak** (RT-6),
   **humidity / swollen-pellet jam** (RT-7), **landing dust cycle** into B2
   (RT-8), **10 g retention pull** (RT-13).
3. **Fill-by-mass procedure** plus `Fill` / `dispensed_since_fill` in the
   contract (RT-5).
4. **Sim delivered** with hover-σ as a swept axis, and accuracy ownership levied
   on the FC/ICD side (RT-4).

Plus the pre-existing bench plan from electronics §9 (B1–B10) and the CAD open
issues from `_run/BUILD-NOTES-r6.md` §7, of which the two that gate the print
are the **caliper survey on 20+ real pellets** (`DISC_T`, `POCKET_R`,
`BRUSH_WIPE`, `NOSE_GAP` must be re-frozen against measured pellets — an
all-judges item since the trade study) and **weighing the actual motor**.

## 9. Deliverables in this package

| Path | What |
|---|---|
| `../README.md` | Status, compliance, declared-unmet blockers |
| `DESIGN.md` | This document |
| `../cad/dispenser.py` | Parametric build123d source, 2597 lines, with a self-verifying harness |
| `../cad/verify_exports.py` | Independent export re-measurement, 348 lines (see RT-20) |
| `../cad/BOM.md` | Auto-generated from measured solids |
| `../cad/exports/` | 102 files — per-part STEP + STL and full assembly, rounds 1–6; **11 STEP + 11 STL at r6** |
| `../cad/renders/` | 34 PNGs — iso, section, bottom, meter detail, fill station, bay lid, cartridge-out, rounds 1–6 |
| `../electronics/ELECTRONICS.md` | 2129 lines: power tree, drive, sensing, DroneCAN contract, priced BOM, 12 ECOs, 10 bench tests, residual-risk register |
| `sim/` | **absent** — §6 |
| `software/` | out of scope by direction |
| `../_run/` | 5 research docs, 4 concepts, survey, judging, 6 rounds of build notes with verbatim critic output, red team, gap review |
