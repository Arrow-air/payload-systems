# Brush Bullet Dispenser — Design

Design package at **rev-1** (CAD close-out run, 2026-08-07→08, export tag
`r12` — still the shipped tag: the 2026-08-08 close-out run **failed**, both fix
rounds produced nothing, and no `r13` exists; see §10.8 and
`_run/rev1/RUN-RESULT.md` "Close-out run (2026-08-08)").
This is the full story of how the design got here: what was surveyed,
what was traded, what twelve rounds of CAD found and fixed — six in rev-0
(§4.1–4.7) and six more in rev-1 (§4.8, §4.9, **§10**) — what the electronics
contract specifies, what was *not* built, and what is still wrong with it.

**If you read one section, read [§10](#10-rev-1-close-out--what-closed-what-did-not).**
It is the rev-1 close-out: what the run actually closed, what an independent
verifier could and could not reproduce on the final exports, and the one
blocker that is still open.

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

## 4. CAD — six rev-0 rounds (and six more in rev-1)

`cad/dispenser.py` is a single parametric build123d model — 2597 lines at rev-0,
**6086 lines at r12** — that exports STEP + STL for 10 parts (**15 at r12**) plus
the assembly, renders 7 PNGs per round, regenerates `cad/BOM.md` with masses
integrated from the actual solids, and **runs its own verification harness on
every execution**. `cad/verify_exports.py` re-measures the exported files
independently of the model; rev-1 replaced it round by round with
`verify_r2/r4/r5/r6.py`, of which **`verify_r6.py` is the current one**.

The table below is the **rev-0** score history. The rev-1 rounds (export tags
`r7`…`r12`) used a different four-critic panel — count-sensor, granule-path,
assembly, integration, verdicts rather than scores — and are tabulated in
[§10](#10-rev-1-close-out--what-closed-what-did-not).

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
defence 1. **The fix is one parameter: `NOSE_GAP` 3.00 → ≤1.50 mm.**

> **STATUS OF THIS SECTION — everything above the line is the r6 (rev-0)
> story and is kept as history. The `NOSE_GAP` fix WAS applied, in rev-1
> round 1, and this paragraph is the correction the round-5 granule-path
> critic required (it found the README and this section still publishing the
> pre-fix numbers three rounds after the geometry changed — an RT-19 /
> N15 documentation-integrity failure of exactly the kind this programme
> exists to catch).** Measured on the r12 exports and reproduced
> independently by the round-5 critic on r11 (`pocket_disc_r12.stl` and
> `brush_holder_r12.stl` are **byte-identical** to r10/r11 — md5
> `d02b663b…` and `ad2343fe…` — and `meter_housing` changed in r12 only at the
> detent-plunger bore and the bay-screw pilot, neither of which is on the
> granule path, so the two sets of numbers measure the same solids):
>
> - **There is no blind band.** The model's own r12 output: *"the nose covers
>   r 20.0..46.7 at 1.500 mm, so nothing more than 1.500 mm proud ever reaches
>   the ramp"*, and *"brush wipe 1.2 mm < roof clearance 1.5 mm"*. The round-5
>   critic probed the same (byte-identical) solids on r11 and read **1.500 mm
>   at r = 20.5, 22, 26, 30, 34, 38, 42, 46.5, 47.0** and **1.500 mm at 132
>   roof probes**. max(nose gap) = min(roof clearance); the 1.50–3.00 mm band
>   is closed.
> - **The bristle still leads.** Bristle tip **+1.200 mm** above the disc top
>   vs the rigid nose at 1.500 mm, so the compliant element contacts first for
>   every proud object below 5 mm.
> - **The nose stubs, it does not lift.** Swept-sphere first contact on the
>   exported `brush_holder`, 0.05° steps: Ø5.0 (+1.80 proud) contacts at
>   θ = 159.20°, Ø6.0 (+2.95) at 162.20°, Ø7.0 (+4.08) at 164.00°, Ø9.0
>   (+6.00) at 166.55° — **n_z ≤ 0 in every case**, i.e. nothing is lifted
>   over the nose. The old `cot(30°) = 1.73` ramp credit is **withdrawn**.
> - **The 7.5 N figure was wrong and flattering.** Crush force at the measured
>   section × 0.36 MPa: **Ø5.0 → 19.63 mm² → 7.07 N, Ø6.0 → 28.27 mm² →
>   10.18 N, Ø7.0 → 38.48 mm² → 13.85 N**, against 12.2 N at normal metering
>   current and 20.4 N in recovery. The Ø6 margin is **2.00× recovery /
>   1.20× normal**, not 2.7×.
> - **"25° entry ramp" is one radius of a range.** The relief is a constant
>   dz/dθ surface, so the angle is radius-dependent: **36.12° at r = 20.5,
>   34.21 at 22.0, 31.41 at 24.5, 25.05 at 32.0, 20.74 at 39.5, 17.83 at
>   46.5**. Below r ≈ 21.9 the ramp's cot falls under the 1.44 self-locking
>   line these documents use as a pass/fail criterion.
> - **Where the backstop runs out** (round-4 and round-5 MODERATE, actioned in
>   r6 and now printed by the model itself instead of only living in a
>   critique). The widest **self-locking** sliver the pocket can hold is
>   **w = 2.793 mm** by the model's bisection and **2.791 mm** by the critic's
>   independent construction — the two agree on the width and differ on the
>   crescent chord, so both sets are published:
>
>   | shard in the worst self-locking crescent | model (r12) | round-5 critic (r11) |
>   |---|---|---|
>   | 90° conforming | 20.65 mm² → 7.43 N → **2.74× / 1.64×** | 26.75 mm² → 9.63 N → **2.12× / 1.27×** |
>   | 180° conforming | 41.30 mm² → 14.87 N → **1.37× / 0.82×** | 53.51 mm² → 19.26 N → **1.06× / 0.63×** |
>   | full-ring crescent | 82.60 mm² → 29.74 N → **0.69× / 0.41× → STALLS** | 107.02 mm² → 38.53 N → **0.53× / 0.32× → STALLS** |
>
>   (margins are ×recovery 20.4 N / ×normal 12.2 N.) **Take the critic's
>   column as the shipped bound** — it is the conservative one. Both say the
>   same thing: the backstop covers a partial conforming shard, is marginal at
>   180° at normal current, and **stalls** on a full-ring crescent. Stalling is
>   the intended failure mode — a trapped whole granule needs 41 N and must
>   never be milled — but it is a bound, and it belongs next to the headline.
> - **Worst escaping fragment** (round-5 critic's construction on r11, not a
>   model print): Ø4.740 (Ø13 granule centred in its pocket) / Ø5.612 (Ø12,
>   seat −1.50 mm); every escapee still fits the exit port, tightest clearance
>   **+0.101 mm**.
>
> σ = 0.36 MPa and µ = 0.4 remain **carried assumptions** (US4172714-derived);
> the closing action is bench test IFDC S-115.

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

> **rev-1 round 4 (export tag `r10`) — B7 status: still open, and the round-2
> numbers below were WRONG in the direction that flattered the design.**
> The r8/r9 sweep applied the ±lateral seat offset **radially** (pellet centre
> at radius PCD ± e), which barely changes the distance to the port axis and
> produced an artificially tight 1.00° spread. The worst case is the offset
> lying **along the pocket→port chord** — a granule resting on the leading wall
> of its pocket reaches the port earlier by exactly e. Re-measured that way on
> `r10` at 0.25° steps (`cad/dispenser.py` B7 RELEASE SWEEP, reproduced
> independently by `cad/verify_r4.py` on the exported plate):
> **support is lost 3.25–10.50° into the 22.5° index (14.4–46.7 % of the move),
> at pellet-centre-to-port separations of 6.690–10.701 mm, with a release-angle
> spread of 7.25° across Ø11–Ø13 and 3.75° at Ø13 alone.** The independent
> round-3 critique measured 3.25–10.50° / 7.25° / 3.75° on `r9`; the model and
> the critique now agree. Everything the round-2 text said about the
> *direction* of the finding stands, and it is worse than published: the
> release is spread over 7.25° of disc rotation, not 1.00°.
>
> **rev-1 round 2 (export tag `r8`) — superseded, kept for the record.** The
> exit port was reduced Ø18 → **Ø16** (rim radius
> 8.75), which improved park retention (worst-placed Ø13 margin +2.74 mm, Ø12
> +2.24, Ø11 +1.74) but did **not** close the release. Measured on the r8
> geometry at 0.25° steps, across pellet diameter Ø11/Ø12/Ø13 and the full
> ±lateral seat offset the pocket allows: **support is lost 6.75–7.75° into the
> 22.5° index (30.0–34.4 % of the move), at a pocket-to-port centre separation
> of 8.215–8.769 mm, with a release-angle spread of 1.00°** [SUPERSEDED — the
> offset was applied radially; see the r10 block above] — against the
> punch-list requirement that support be retained until the separation is
> ≤ 1.0 mm. **The granule is therefore released while the disc is still moving,
> through a partial lune, before the 150 ms dwell begins.** Lateral velocity at
> the PCD is ω × 32 mm = **0.126 m/s** at the 225 °/s mean index rate and
> **0.25 m/s** at a 450 °/s peak [D — the index profile is an assumption carried
> from r6, not re-derived]. Any sentence anywhere in this repository claiming a
> *stationary*, *concentric*, *zero-lateral-velocity* release, or a *full-port*
> clear aperture at release, is wrong and is withdrawn; the model no longer
> prints it. What survives of the two-phase argument is the dwell: fall time to
> clear the 14.5 mm pocket is 54 ms against a 150 ms contract dwell (2.8×), so
> the granule is guaranteed clear of the disc before the second index. Closing
> B7 by geometry needs either a port smaller than the Ø13 worst-case granule
> allows, or a mechanical gate below the pocket — both are architecture changes.
> Full measured table: `_run/rev1/BUILD-NOTES-r4.md` §4 (r10, current)
> and `_run/rev1/BUILD-NOTES-r2.md` §3 (r8, superseded).

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

### 4.8 rev-1 r11 (round 5): a roll-up is not a measurement

The rev-1 rounds continued the pattern in §4 — each round's blocker was
invisible to the previous round's harness — and round 5's is the cleanest
example in the whole programme. Round 4 shipped a **harness-coverage table**
that printed `COVERED 18.00 mm top-plate elbow -> hopper conduit … 95.3 %`
while that elbow was **solid printed material**: the strain-relief boss was
unioned onto the plate after the two conduit bores were cut and re-filled the
junction, so the largest conductor that could get from the attachment interface
to the electronics bay was **Ø0.0**. The table could not see it, because the
table was a roll-up of *parameters* — a list of segment lengths with a
hand-typed COVERED flag — and no parameter changes when a boolean re-fills a
bore.

**Round 5's fix to the harness:** the route is a 3-D polyline, patency is a
contains-scan along the bore axes, and coverage is measured by casting eight
rays perpendicular to the run at every millimetre — *covered* means *laterally
enclosed by printed material*, measured on the exported mesh. Measured result:
both bore axes read no solid point, a Ø5.5 bundle sweeps every leg at
**0.0000 mm³**, and coverage is **94.6 % of a 484.84 mm run**, with the
uncovered 26.17 mm itemised and located (the bay→cartridge service loop *must*
flex, so a conduit there would be a defect). The elbow itself is now an R8.0
swept corner rather than a right angle, because a bundle cannot turn a square
one. Full numbers and the independent checker's reproduction:
`_run/rev1/BUILD-NOTES-r5.md` §2.

Two other round-4 findings closed in the same round, both in the BOM-vs-geometry
seam: the four gearbox screws were ordered as **cap heads for a 90° countersink**
(a cap head measures 197.6 mm³ of interference with the metering disc over one
spoke pitch and never returns to zero — the BOM now names M3×8 ISO 10642 /
DIN 7991), and the plug-tether anchor lug stood **1.000 mm inside the Ø22 drop
tube** while the model's log called the whole 206.0993 mm³ plate∩plug boolean
"the designed 0.3 mm press fit" when only 83.504 mm³ of it was. Both are the
same failure class as the coverage table: a number that was asserted rather
than decomposed.

### 4.9 rev-1 r12 (round 6): a boolean that silently does nothing

Round 5's fix to the *aircraft-side* harness (§4.8) was real. Round 6's blocker
was the other half of the same requirement, and its root cause is worth writing
down because it is a trap in the tool, not in the design.

The round-5 integration critic measured the **cartridge harness duct** — the
network that has to get conductors from the electronics bay to the motor and to
both count-sensor boards — and found **every leg 100 % solid on its own axis**:
`exit leg 63/63, collector 187/187, return leg 261/261, vertical leg 205/205,
motor branch 197/197` points inside printed material, largest conductor **Ø0.0**,
and `retaining_plate_chute_r11` containing **zero enclosed voids**. The model
believed it had bored that duct: it built a solid duct, built a matching set of
bore cylinders, fused them, and subtracted the fuse.

**Why the subtraction did nothing.** Every leg of the duct uses the same bore
radius, and the legs meet at right angles. A fuse of *equal-radius perpendicular
cylinders* is a degenerate-tangency case for OCC: `BRepCheck_Analyzer` reports
the fused shape **invalid**, and `BRepAlgoAPI` answers a boolean against an
invalid tool with an **empty result and no exception**. So `rp -= _bore` became
a silent no-op, `rp.intersect(_bore)` read **0.0 mm³** even though a Ø1 sphere on
the duct axis reads *inside both solids*, and every downstream number — volume,
mass, the ledger — was self-consistent with a fix that was not in the geometry.
The model's own harness metric could not see it either, because it measured
**coverage** (is the route laterally enclosed?) and a solid rod is perfectly
covered. *Coverage and patency are different questions.*

The fix is two rules, now enforced in code by `cut_each()`:

1. **Never fuse a set of cutting tools.** Keep them as primitives and cut with
   each in turn; a degenerate fuse then cannot exist.
2. **A boolean that removes nothing is a failure, not a pass.** Every tool is
   validity-checked before use and the cut asserts a volume floor.

Measured result on `r12`: **0 of 1757 axis points inside material across all 15
legs**, a **Ø4.0 mm bundle sweeps every leg at 0.0000 mm³**, and the cut removed
**8025.3368 mm³ = 10.19 g** of CF-PETG that r11 was carrying as solid. The
independent checker reproduces it with a control that proves the probe is not
blind (4000 random points in the part's bbox: 8.6 % read inside).

Three more round-5 findings closed in the same round, and one deliberately not:

- **The detent plunger had nothing to thread into** (assembly BLOCKING). Its
  bore measured Ø5.199 then Ø6.399, unthreaded, and the comment in the model
  called the counterbore a heat-set insert seat while **no M5 insert was ordered
  anywhere in the BOM**. The detent is 96.5 of the 190.7 mN·m reaction budget,
  so the latch had only the stop pin without it. It is now a **modelled Ø4.5 ×
  13.5 mm thread-forming pilot** with a Ø5.2 ball clearance to the chamber —
  measured on the export as a section that steps **5.100 → 4.400 going
  outward**, which is what a threadable boss looks like and what a clearance
  hole does not.
- **The bay screws were 1.000 mm longer than their pilot, and the pilot was
  open into the metering chamber** over 27.7 % of its section with 0.144 mm —
  one FDM layer — of floor where it was closed. Floor moved out to y = −46.5 and
  the screw dropped to M3×18; the pilot now reads **0.0 % open** with the same
  raster, and the r11 floor is run as a control that comes back **33.9 % / 35.5 %
  open**, so the probe is provably able to see the defect. The trade is stated:
  thread engagement 5.08 → **3.58 mm** (1.19 × D), and the thinnest material
  under the floor is **1.262 mm**, which is 8.8 × r11 but still under the
  1.95 mm this package uses for insert bosses. That residual is carried open.
- **Two 2.2 × 5.0 mm cable-tie slots left the granule bed open to the sky.**
  They had been there since round 2, at plan radius 66.61 mm — inside the tank —
  and the model's tank-vent self-check used **twelve hand-placed columns**, none
  within 40 mm of them, printing "0 of 12 open" for nine rounds. The check is
  now a **0.5 mm grid scan of the whole barrel bore (60 669 rays)**, the ties are
  additive bridges with no hole in the lid, and the same scan found a *second*
  defect nobody had reported: the fill cap's **lanyard hole went straight
  through the 2.5 mm cap flange into the fill bore**. Both are closed; the scan
  now reads **0.00 mm² unroofed inside the fill-cap O-ring seal**, with 7.25 mm²
  in the cap-to-recess running clearance outside the gland, which is what the
  nitrile cord seals.
- **Not closed, and recorded as such:** ECO-4 asks for a 0.4 mm chamfer at the
  count-window seat mouth. It was modelled and **withdrawn in the same round**,
  because the seat mouth plane is tangent to the Ø22 chute bore at x = 32 and the
  chamfer cone's rim is coincident with the seat cylinder there — the part came
  back with **22 open and 22 non-manifold edges**, all at x = 31.99…32.01,
  |y| = 11.000. B10 (watertight exports) is a blocking requirement and a
  degenerate tangency is not a mesh-tolerance problem, so the seat ships
  straight-walled and the deviation is written down instead.

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

**rev-1 status (r10):** the *geometry* ECOs are merged and measured on the
exports — ECO-3 (two Ø3.2 chord apertures per side at x = 29 / 35), ECO-9
(6.000 mm vertical stagger, z = −392.250 / −398.250), ECO-4 (four Ø6 PMMA
window seats cut against the bore so nothing is proud of it), ECO-5 (0.800 mm
lateral labyrinth), ECO-12 (bolted cover, four clamp posts, 30 mm² of bearing
on the board) and ECO-7/ECO-6 in the electronics bay. `cad/BOM.md` no longer
lists the TSSP4038; it lists VBPW34FAS ×2, OPA2320, TSAL6200 ×2, four PMMA
windows and the two sensor PCBs. The rev-0 sentence *"None of the ECOs were
merged into `cad/dispenser.py`"* was true at r6 and is **false at r10**.
What is **not** closed: ECO-1/ECO-2 (external finish α ≤ 0.4 vs the black
CF-PETG in the BOM — punch-list N19), ECO-8 (third Hall) and ECO-10 (motor
NTC) are electronics-side and were never in this run's scope. The optical
budget in §4.4 is still written for a 32 mm path against a measured
**43.1 mm** emitter-tip-to-detector path (≈100× excess gain, not 182×), and
§4.2/§4.3's fall heights are still the doc's 40 mm against the measured
38.0/44.0 mm — those are `ELECTRONICS.md` edits, still open.

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
| **RT-1** | **STILL OPEN after rev-1 — 3 of its 4 legs closed (§10.4).** Fixed and independently reproduced on `r12`: the θ = 310° roof through-slot is gone (9.000 mm of roof at all 8 radii × 16 angles), the gearbox holes are on the datasheet's Ø26 bolt circle (Ø3.40 at (±13, 0) and (0, ±13), 3.200 mm web), and the D-flat exists (r 2.550 flat / 3.050 round, 56° arc, 13.5 mm engagement). **Not fixed: the grub pilot dead-ends 0.200 mm short of the shaft flat** — Ø0.7 corridor 0.0770 mm³, Ø2.6 1.0619 mm³ = π·1.30²·0.200 exactly — so the disc still cannot be clamped to the shaft, and round 6's own checker *and* its assembly critic both called that corridor continuous because their ray starts outboard of the flat. Original rev-0 text: r6 failed 3 of 4 critics with disc bore r = 3.06 mm at all 24 angles (no D-flat → no torque path) and gearbox holes on a 26 mm square | Deepen the pilot 0.2 mm **and** re-anchor the probe at r = 2.55, with a control that must fail | The corridor boolean run **from the flat radius**, reading 0.0000 mm³ |
| **RT-2** | **No electrical connection to the aircraft.** 19.35 mm blind-mate gap (8.85 mm even at the highest legal pad plane) vs ≤2 mm plunger travel. The notes offered "0.00 mm³ of payload inside the shaft" as proof the PCB *is* in the shaft — that metric is the proof it is not. The escape route is foreclosed: the payload clip half nests at most 0.54 mm into the drone-side channel over 8 tested poses | **ICD-side escalation**, not a payload open issue. 10.5 mm is payload-controllable; the residual is aircraft-side | Physical mate against the real 2112 + 3331 set |
| **RT-3** | **CLOSED IN GEOMETRY at r10** (was: "verified count exists only in a document describing hardware that is not in the CAD"). Measured on `retaining_plate_chute_r10`: four Ø3.2 tunnels, two per side, axes at x = 29.000 / 35.000 and z = −392.250 / −398.250 → **6.000 mm ECO-9 stagger**; ECO-5 labyrinth offset 0.800 mm over the outer 2.505 mm; four ECO-4 window seats cut from the bore axis outward, window inner faces at \|y\| = 11.000 with **0.000 mm³ proud of the bore**; the ordered TSAL6200 now fits its cavity at its **datasheet** 8.7 ± 0.3 mm height (0.0000 mm³ against plate and cover at 9.0 mm max material — r9 buried 11.2532 mm³ per LED). BOM carries VBPW34FAS/OPA2320/TSAL6200/PMMA windows and no TSSP4038 | done in r10 | B1 dark-time survey (≥200 real drops + ≥100 fractured Ø7–10 mm pieces) still gates the **claim**; the geometry no longer blocks it |

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
   done, they are declared in [`../README.md`](../README.md). **Rev-1 update:**
   RT-3 is closed in geometry, RT-2's surviving half (the electronics bay) is
   closed and its pin/pad half is out of scope by direction, and **RT-1 is still
   declared unmet** — see [§10](#10-rev-1-close-out--what-closed-what-did-not).
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
| `../cad/dispenser.py` | Parametric build123d source, **6086 lines** at r12, with a self-verifying harness |
| `../cad/verify_r6.py` | Independent export re-measurement, **395 lines**, current (reads only `exports/` + `BOM.md`). Earlier: `verify_exports.py`, `verify_r2/r4/r5.py` (see RT-20) |
| `../cad/BOM.md` | Auto-generated from measured solids; **four COTS description strings hand-corrected at rev-1 packaging** — see §10 |
| `../cad/exports/` | **288 files** — per-part STEP + STL and full assembly, rev-0 rounds 1–6 and rev-1 `r7`…`r12`; **16 STEP + 16 STL at `r12`** |
| `../cad/renders/` | **69 PNGs** — iso, section, detail, bottom, fill station, bay lid, cartridge-out; rev-1 rounds are `v1r<N>_*` (7 at `v1r6`) |
| `../electronics/ELECTRONICS.md` | **2186 lines**: power tree, drive, sensing, DroneCAN contract, priced BOM, 12 ECOs, 10 bench tests, residual-risk register. **Stale against r12** on the count-sensor Z — see §10 |
| `sim/` | **absent** — §6 |
| `software/` | out of scope by direction |
| `../_run/` | rev-0: 5 research docs, 4 concepts, survey, judging, 6 rounds of build notes with verbatim critic output, red team, gap review |
| `../_run/rev1/` | rev-1: `CONTEXT.md` (Thomas's directives), `PUNCHLIST.md`, `CRITIQUE-r1…r6.md`, `BUILD-NOTES-r2/r4/r5/r6.md`, **`VERIFY.md`** (independent fresh-eyes re-measurement of `r12`), `RUN-RESULT.md`, `logs/` |

---

## 10. Rev-1 close-out — what closed, what did not

The rev-1 run (2026-08-07 → 08, six rounds, export tags `r7`…`r12`) had exactly
one job: **make the CAD close against the punch list**
([`../_run/rev1/PUNCHLIST.md`](../_run/rev1/PUNCHLIST.md)), under six directives
from Thomas recorded verbatim in
[`../_run/rev1/CONTEXT.md`](../_run/rev1/CONTEXT.md). No new mechanism
exploration, no trade study, no simulation, no software. Every number in this
section is either quoted from the round's tool output or was re-measured
independently; where the two disagree, both are printed.

### 10.1 The verdict in one paragraph

**Two of the three rev-0 CAD blockers are closed and survive adversarial
re-measurement. One is not.** RT-3 (the verified-count hardware that existed
only in a document) is genuinely in the geometry. RT-2's surviving half (the
electronics home — the pin/pad stack-up was ruled out of scope by directive 1)
is a real sealed bay with a real board volume, real standoffs and real grommeted
entries. **RT-1 is short by 0.200 mm**: the grub-screw pilot in the pocket disc
dead-ends before it reaches the shaft flat, so the disc still cannot be clamped
to the motor. Round 6's own checker, and the round-6 assembly critic, both
reported that corridor as continuous — because both anchor their ray outboard of
the feature they are testing. **The run therefore does not close.** It is a
0.2 mm edit plus a checker fix away from closing, and the honest reading is that
the geometry is much better than r6 and the *verification* is still the weak
member.

### 10.2 The six rounds

| Round | Tag | Critic verdicts | What the round's root cause turned out to be |
|---|---|---|---|
| 1 | `r7` | count-sensor NOT CLOSED (4 blocking) · granule-path FAIL (2 BLOCKER) · assembly FAIL (4 blocking) | first geometry for the whole rev-1 feature set; ECO-4 not as specified, one sensor board not installable, BOM untouched |
| 2 | `r8` | count-sensor NOT CLOSED (1 blocking) · assembly FAIL (3 blocking) · integration FAIL (4 blocking) | the neck/adapter and the bay landed, but three of integration's four blockers were **created by** the round's own fixes |
| 3 | `r9` | granule-path FAIL (1 BLOCKER) · count-sensor NOT CLOSED (2 blocking) · assembly FAIL (2 blocking) | **export-integrity regression on the part that carries the exit port**; documented B7 release numbers did not reproduce |
| 4 | `r10` | granule-path PASS-with-complaints · assembly FAIL (A-10) · integration BLOCKING FAIL | **RT-1 and RT-3 close in geometry here**; the gearbox screws were ordered as cap heads for a 90° countersink; the aircraft-harness conduit elbow was solid |
| 5 | `r11` | count-sensor PASS-with-complaints · granule-path PASS-with-complaints · assembly FAIL (A-11) · integration BLOCKING FAIL (I-1) | **a roll-up is not a measurement** (§4.8): a coverage table printed 95.3 % over a solid elbow; the M5 detent plunger had nothing to thread into |
| **6** | **`r12`** | **count-sensor PASS-w/c · granule-path PASS-w/c · assembly PASS · integration PASS-w/c** | **a boolean that silently does nothing** (§4.9): a degenerate fuse of equal-radius perpendicular cutting cylinders made `rp -= bore` a no-op, so the whole cartridge harness duct was solid printed material |

Round 6 is the first rev-1 round with **no blocking finding from any of the four
critics**. It is also the round the independent verifier failed — which is the
point of having one.

*Record-keeping defect, stated rather than papered over:* build notes exist for
rev-1 rounds 2, 4, 5 and 6. **Rounds 1 and 3 have critiques but no build notes**
(the round-1 count-sensor critic records that `BUILD-NOTES-r1.md` did not exist
when it ran). What those two rounds changed is recoverable only from the
following round's critique and from `logs/`.

### 10.3 What closed, with the numbers

Everything here was re-measured on the `r12` exports by a verifier who had seen
no build round and never read `dispenser.py`
([`../_run/rev1/VERIFY.md`](../_run/rev1/VERIFY.md)); B4 and B6 reproduce to the
third decimal.

- **The count-sensor hardware is real (RT-3, B4).** Four Ø3.10–3.20 tunnels, two
  per side, axes at x = 29.000/35.000 and z = −392.250/−398.250 → the **6.000 mm
  ECO-9 stagger**; a Ø0.2 probe reads **0.000 mm of material** on both beam axes
  and 12.834 mm at the two off-diagonal controls; the ECO-5 labyrinth measures a
  **0.800 mm** offset with a **0.800 mm** ledge, split ±0.400 so the clear lens
  stays on the ECO-3 axis; four PMMA windows with inner faces at |y| = 11.000 and
  **0.0000 mm³** proud of the Ø22 bore; a Ø13 granule swept down the chute
  booleans to **0.0000 mm³** against plate, windows, cover and boards. The BOM
  carries VBPW34FAS ×2 / OPA2320AIDR / TSAL6200 ×2 and **no TSSP4038**.
- **The roof through-slot is gone (B1).** 8.980 mm of roof (STL chordal error on
  a 9.000 mm STEP section) at all **8 radii × 16 angles**, including θ = 310°
  where r6 read 0.000. The largest travel-opposing roof face over the transfer
  arc is **1.98 mm²** against a 20 mm² threshold; r6 had **238 mm²**.
- **The gearbox mounts on its own bolt circle (B3).** Four Ø3.40 holes at
  (±13.00, 0) and (0, ±13.00) through a 4.000 mm flange — the datasheet Ø26 bolt
  circle, replacing r6's 26 mm *square* — with a **3.200 mm** minimum web
  (r6-naive: 0.30 mm) and a continuous 2.2 mm-wide thrust-washer annulus.
- **Reach-in clearance is proved with numbers, not adjectives (directive 3, B6).**
  Stand-off **h = 43.500 mm** on a **48 × 48 mm** neck (plan half-extent a
  constant 24.000 mm from Z = −181.55 to −225.05); three of four 95 × 45 × 130 mm
  gloved-hand corridors clear at **0.0000 mm³**, **including both opposing
  ±X sides**; **0 vertices** of payload above Z = −171.000.
- **The rejection band is no longer blind (B8).** max(nose gap) = **1.500 mm**
  over the whole rejection arc = min(roof clearance) **1.500 mm**, with the
  compliant bristle tip leading at **1.200 mm**. r6's constant 3.000 mm nose
  left a band a fragment could enter and never be stopped by.
- **The exports are clean (B10).** 15/15 part STLs watertight, **0 non-manifold
  edges**, assembly 24/24 bodies and 0 open edges — reproduced edge-by-edge,
  Euler characteristics and all, by an independent trimesh run.
- **The mass ledger is measured, not asserted (B11).** Every part volume
  reproduces to **≤ 0.04 %**. **LOADED @250 = 1432.5 g** on the shipped
  slicer-realistic basis (4 perimeters at 0.4 mm, 25 % infill, padded EDT) →
  **+68 g** under the 1500 g ceiling; **1493.5 g** with the 61 g per-open-item
  reserve; the 100 %-infill pessimistic bound **1576.0 g** is **76 g over** and
  is printed rather than hidden; max fill @421 = 1777.8 g; dry 1281.0 g.
- **Refill has a rest position (directive 4, B12).** `service_stand` is a real
  modelled part (103.892 cm³ → 132.0 g) and is correctly listed as **mandatory
  GSE excluded from the flight ledger** — without it the dispenser stands on its
  own gearbox output flange.
- **Capacity is untouched, as directed.** 962 cm³ → 421 granules, a change of
  ≪ 2 % from rev-0's ~422.

### 10.4 What did not close

**1. RT-1: a 0.200 mm web across the grub pilot — BLOCKING.** The corridor from
the disc OD to the shaft is present and clean from r = 46 down to **r = 2.750**,
and the shaft flat is at **r = 2.550**. The 0.200 mm between them is solid
CF-PETG across the full Ø2.6 section. Exact booleans on `pocket_disc_r12.step`,
first by the verifier and then reproduced digit-for-digit by the packager:

```
  Dia0.7 from r=46.5 to r=2.55 (the bore flat): disc material = 0.0770 mm3   <-- BLOCKED
  Dia0.7 from r=46.5 to r=2.75:                 disc material = 0.0000 mm3
  Dia1.9 from r=46.5 to r=2.55:                 disc material = 0.5671 mm3   <-- BLOCKED
  Dia2.6 from r=46.5 to r=2.55:                 disc material = 1.0619 mm3   <-- BLOCKED
  Dia2.6 from r=46.5 to r=2.75:                 disc material = 0.0000 mm3
```

1.0619 mm³ = π·1.30²·0.200 **exactly** — a full-section plug, not a sliver of
mesh error. Everything else in the torque path is real: the D-flat runs r 2.550
(flat) / 3.050 (round) over a **56° contiguous arc** with **13.5 mm** of axial
engagement against a 12 mm vendor D-cut, the grub axis sits at θ = 202.5° which
is the flat's exact mid-angle, and a Ø1.9 × 40 mm driver column booleans to
**0.0000 mm³** against all seven surrounding parts. This is a one-line fix.

**Why six rounds signed it off is the part worth keeping.** `BUILD-NOTES-r6.md`
§7 prints *"grub corridor, Ø0.7 ray from the bore to the disc OD along
θ = 202.5: blocked at r = **NOWHERE** — continuous void"*, and the round-6
assembly critic independently reported *"a continuous grub corridor from the disc
OD to the shaft"*. Both are wrong for the same reason: the ray is anchored at the
**round** bore radius (3.05) or at the pilot floor, both **outboard** of the flat
at 2.55, so neither probe can ever see the web. That is the third instance in
this programme of one failure class — §4.8's coverage table that scored a solid
rod as perfectly covered, §4.9's boolean that removed nothing and returned no
error, and now a probe that starts past the feature it is testing. **A check that
cannot fail is not a check**, and rev-1 shipped two rules against this
(`cut_each()`'s volume floor, and controls that must fail) without ever applying
them to the assembly probes. The fix is two lines: deepen the pilot 0.2 mm, and
re-anchor the checker ray at the flat radius.

**2. B7 — release is not from a stationary pocket. A recorded plateau, not a
closure.** The granule leaves **3.25–10.50°** into the 22.5° index (spread 7.25°
across Ø11…Ø13); separation at release **6.690–10.701 mm** against a B7.1
requirement of ≤ 1.0 mm; lateral velocity **0.126 m/s** at the mean index rate,
0.25 m/s at peak. The round-5 granule-path critic re-derived the window
analytically from the measured rim and got 3.17–10.39°, spread 7.22° —
agreement to ≤ 0.11° from a
different construction. The punch list permits B7 as a plateau **only if every
document says so**, and they do: the build notes, this section, and the README.
Geometric closure needs an architecture change, which this run was explicitly
told not to attempt.

**3. Deviations recorded in round 6, each with its trade stated.**

- **ECO-4's 0.4 mm window-seat chamfer is not modelled.** It was attempted and
  **withdrawn in the same round**: the seat mouth plane is tangent to the Ø22
  chute bore at x = 32 and the chamfer cone's rim is coincident with the seat
  cylinder there, so the part came back with 22 open and 22 non-manifold edges,
  all at x = 31.99…32.01, |y| = 11.000. Watertight exports are a blocking
  requirement and a degenerate tangency is not a mesh-tolerance problem. Either
  ELECTRONICS ECO-4 is amended or the seat is redesigned so the mouth is not
  tangent to the bore.
- **1.262 mm of material under the bay-screw pilot floor**, against the 1.95 mm
  this package uses for insert bosses. It is 8.8× better than r11's 0.144 mm and
  the pilot now reads **0.0 % open** into the metering chamber (with r11's floor
  re-run as a control that comes back 33.9 % open, so the probe is provably able
  to fail) — but it is thin, and it is carried open.
- **Bay-screw thread engagement dropped 5.080 → 3.580 mm** (1.19 × D), bought
  deliberately to close that breakthrough.
- **The Ø2.0 × 60 mm beam cylinder clips the sensor cover by 0.1576 mm³** on beam
  A, 6.5 mm behind the emitter board. Over the actual emitter-to-detector span it
  is 0.0000 mm³, so this is off the optical path — but the punch-list test as
  literally written is not satisfied, and both numbers are printed.
- **The emitter board sits 0.500 mm off the boss face**, not the 1 mm the
  punch-list test assumes; the literal "+1 mm all round" boolean reads
  131.96 mm³. The receiver board passes the same test at 0.0000 mm³.

**4. Carried open from earlier rounds, unactioned.** **N10** — the sump outlet is
26.993 mm × 120.000° = **2.076 × D_max**, below every no-arch criterion for a
slot; the defence is the agitator (one full sweep per 2.67 dispensed granules)
and this stays an explicit plateau-with-complaint. **N19** — CF-PETG (α ≈ 0.95)
on 9 of 10 external parts against ECO-1/ECO-2's α ≤ 0.4; a material decision
nobody has made, and it is the same contradiction RT-6 raises. **N11** — no
isolation gate, so clearing a jam still dumps ≈115 cm³ ≈ 51 granules. **N9/N5** —
the tether hard point and the fill-cap detent are in the 12.0 g mass reserve, not
in the geometry. **Two directive-2 complaints on the word "sealed"** — the gasket
cord is 164–169 % of its groove volume (40 % squeeze, i.e. the BOM should order
1.5 mm cord, not 2.0 mm) and there is **29.33 mm² of unsealed opening** at the
roof spigot; until one of those is fixed the bay is dust-**resistant**, not
sealed.

**5. `ELECTRONICS.md` is stale against the geometry by 49.1 mm.** §4 still places
the count sensor at Z ≈ −343.2, "10 mm above the chute exit"; it is modelled at
**−392.250/−398.250**, i.e. 41.000/47.000 mm of fall, v = 0.8969/0.9603 m/s. The
count-sensor critic asked for §4.2/§4.3 to be re-based and the Ø11 margin
restated (7 % → 6.0 %). **Not done** — this run's scope was CAD. §4.5 also still
calls window replacement "a 10-second maintenance action"; the seat is a blind
bonded counterbore 20.050–26.050 mm up a Ø22 bore, so the window is **swabbable,
not field-replaceable**.

**6. Nothing has been tested.** σ = 0.36 MPa and µ = 0.4 (IFDC S-115) are carried
assumptions, the dark-time survey that freezes the count gate (B1) is unrun, the
packing-fraction fill calibration is unrun, **150.4 g of the 1164.5 g empty
subtotal is estimate rather than measured geometry**, and the 350 g stepper has
never been on a scale.

### 10.5 The BOM defects, and a trap for whoever regenerates it

The verifier checked `cad/BOM.md` against the geometry the same file's masses
were integrated from, and found four **description strings** that would buy parts
that do not fit. All four are corrected in `cad/BOM.md` and marked
`[CORRECTED 2026-08-08]`; each correction below was re-measured by the packager
on the `r12` exports.

| Row | Said | Measures | Consequence if ordered as written |
|---|---|---|---|
| PTFE thrust washer | Ø30 / Ø24 × 1.5 | **Ø38 / Ø34 × 1.400**, 316.673 mm³, in a 1.005 mm recess at r 16.9…19.1 | the ordered ID/OD lands directly on the four Ø3.4 gearbox bolt holes at r 11.30…14.70, and is 0.1 mm too thick for the seat |
| gearbox pilot bore (B3.4) | *stated nowhere* | **Ø16.20** (no material at r ≤ 7.50, full column at r ≥ 8.50 through the 4.000 mm flange) | the punch list asks for this diameter explicitly, with a source; the vendor boss diameter it clears is still an **ASSUMPTION** and must be caliper-checked on the real motor |
| count windows ×4 | Ø6 × 1.0 | **Ø5.900 × 0.950**, 25.9727 mm³ each | the disc does not enter its seat. ECO-4 carries the same wrong number and needs amending |
| stepper net mass | "310 g NET is an ASSUMPTION" | ledger and README carry **350 g** | a 40 g disagreement on the single largest COTS mass, in the two documents that decide whether the payload is under 1500 g |

**The trap:** `cad/BOM.md` is auto-generated and says "do not edit by hand", but
`dispenser.py` still emits all four of the old strings. **The next regeneration
re-introduces every one of them** unless the source tables are fixed first. That
is written at the top of the BOM as well.

### 10.6 Four passes with zero margin

These are recorded as passes in the punch list and they are passes — but they
have no margin at all, and three of them are the kind that a real tolerance
stack turns into a failure:

- **sensor boss ↔ motor body: 4.000 mm** against a ≥ 4.0 mm requirement. The
  punch list assumed 4.4 mm because it put the motor face at x = 17.6; the
  modelled face is at x = 18.0.
- **bearing seat Ø23.023–23.030** against a ≤ Ø23.03 limit for a 23.00 mm-OD
  igus JFM-2023-07. The flange counterbore is also 1.70 mm deep for a 2.0 mm
  flange, so the bearing flange stands **0.30 mm proud** of the roof.
- **hopper insert bore depth 5.99 mm** against a required 6.00 mm (insert 5.7 +
  0.3), with 1.01 mm of floor left.
- **nose gap 1.500 mm exactly equal to roof clearance 1.500 mm** — which is the
  *intent* of the B8 fix, but it means any print variation on either part
  re-opens the blind band.

### 10.7 What nobody has verified

Stated so that no reader counts it as checked. The verifier could not reproduce:
the harness five-volume boolean and the channel coverage/fill numbers (B5.4/B5.5
— they only exist inside the model), the bay gasket groove loop (B5.3, below its
scan resolution), lid-lift and driver-column sweeps (B5.6), the quick-release
actuation envelope (B6.3 — the release half is drone-side), **ground and prop
clearance (B6.5/B6.6 — the airframe STEPs were not present at the referenced
path, and the stack moved down ~52 mm this rev)**, the B7 0.25° release sweep,
B8.3/B8.4/B8.5, mount-screw engagement, the detent thread pilot, the B12
rest-position and fill-route sweeps, and every non-blocking N-item.

One authoring defect in the punch list itself, for whoever writes the next
checker: **B1.1's "≥ 6.0 mm of roof at every probe outside θ = 96…131" and "full
nominal at θ = 200° and 310°" contradict the designed 120° sump outlet** that the
same document describes in N10. Written literally, that clause reports a
permanent false failure on a correct design.

### 10.8 What it would take to call rev-1 closed

1. Deepen the disc's grub pilot **0.200 mm** so it breaks into the bore, and
   **re-anchor the corridor probe at the flat radius (2.55), not the round bore
   radius (3.05)** — with a control that must fail. Re-export, re-verify.
2. Fix the four BOM strings **in `dispenser.py`**, so a regeneration does not
   undo §10.5.
3. Re-run ground and prop clearance against the real airframe STEPs, because the
   payload dropped ~52 mm this rev and nobody has independently confirmed the
   129.4 / 103.63 / 152.55 mm figures since.

Items 1 and 2 are hours of work. Item 3 is a path fix. **B7, N10, N19, the ECO-4
chamfer, the ELECTRONICS re-basing and every bench test remain open by design or
by scope**, and are listed above rather than folded away.

> **Close-out run result (2026-08-08): FAIL — all three items above are STILL
> OPEN.** A dedicated close-out run (two fix rounds, two independent verify
> rounds) was launched against exactly this list and produced no work product:
> zero `*r13*` files anywhere in the repo, no close-out build notes,
> `dispenser.py` / `cad/BOM.md` untouched since commit `f2a9451`, no `v1r7`
> renders. The packager re-measured B2.2 on the shipped disc at pack time
> (exact OCP boolean, `pocket_disc_r12.step`, θ = 202.5°, Z = −341.25):
> Ø2.6 corridor to r = 2.55 contains **1.0619 mm³** of disc material
> (Ø0.7: 0.0770; both controls to r = 2.75: 0.0000) — the 0.200 mm web is
> still shipped. Item 3 additionally lacks its inputs: no gear-leg solids
> exist as STEPs in either `project-quiver` checkout (only
> `1340_tube_joint.step` + `vendor/1330_main_adapter.step`). **`r12` remains
> the shipped tag and the package remains NOT cleared to print.** Full record:
> `_run/rev1/CLOSEOUT-VERIFY-r1.md`, `_run/rev1/CLOSEOUT-VERIFY-r2.md`, and
> the "Close-out run (2026-08-08)" section of `_run/rev1/RUN-RESULT.md`.
