# MECHANISM SURVEY — Synthesis of all candidate metering mechanisms

Synthesis agent output, 2026-08-06. Inputs: `CONTEXT.md` (ground truth) plus all
five research domains:

- `RESEARCH-seed-metering.md` (precision-ag meters, PSD escapement, UAV carousels)
- `RESEARCH-projectile-feeders.md` (paintball/airsoft/golf-ball, escapements)
- `RESEARCH-pill-counting.md` (pharma counters, verification sensing, friability)
- `RESEARCH-bulk-dispensers.md` (gumball/fish-feeder/vending, hopper bridging)
- `RESEARCH-drone-spreaders.md` (pellet product data, IGNIS/PSD, ag spreaders)

Facts below are traceable to those docs (which carry the primary citations).
My own engineering judgement is marked **[J]**; unverified items **ASSUMPTION**.

---

## 0. Ground rules the survey scores against

From CONTEXT.md (hard requirements): dispense exactly N ∈ 1..10 (usually 1–3)
pellets of ~12 mm / 1.18 g; count **VERIFIED (sensed), not assumed**; hopper
≥ 250 pellets; ≤ 1.5 kg total loaded; 12VSW behind a **2 A fuse (24 W)**, no 5 V,
no UART; must tolerate 12V_PL power cycling; West Texas dust/heat/wind; pellets
can break/crumble in the hopper (fragments + fines guaranteed over a sortie).

Pellet facts that constrain every mechanism (RESEARCH-drone-spreaders §1):

- **[V]** Brush Bullet = hexazinone 75 % (EPA 102162-1), label-confirmed
  1.200 g/pellet vs Thomas's 1.18 g (1.7 % agreement).
- **[V, same-class US4172714]** crush strength only ~7.5 kgf; **swells 2–3×
  irreversibly when wetted** (worst-case jam article); survives 5× 3 m drops.
- **ASSUMPTION (flagged everywhere):** ±1 mm diameter, possible barrel shape
  with mold parting line — pocket/tube geometry must take a 13 mm worst case
  and must be re-checked against caliper data on real pellets.

### 0.1 Mandatory cross-cutting subsystems (mechanism-independent)

Every research domain independently converged on three non-optional elements.
These are **not** discriminators between candidates — every champion gets them —
but any concept missing one is disqualified:

1. **Active hopper agitation at the sump/throat.** The derived anti-bridging
   orifice rule (6–8×D → 72–96 mm outlet for 12 mm pellets; independently
   derived in seed-metering §11, projectile-feeders §9, bulk-dispensers §10)
   means passive gravity feed to any ~14 mm throat is deep in the clogging
   regime by design. Vibratory agitation is documented as the *wrong* answer
   (US11286119: transmits vibration, premature bearing wear — and it pollutes
   the IMU **[J]**). The proven pattern is the PSD's rotating sump agitator at
   the exit hole and paintball soft-paddle agitators; compliant (yielding)
   fingers, torque-limited below the 7.5 kgf crush load.
2. **Sensed count at the drop path, dust-discriminating.** Optical seed sensors
   are documented to count dust as seed (seed-metering §9); the industry fixes
   are mass-based sensing (WaveVision, pharma EFS/capacitive) or high-excess-
   gain **opposed-mode (through-beam) modulated IR** with **pulse-width /
   dark-time gating** (a 12 mm sphere occludes the beam ~6–12 ms at chute
   speeds; fragments read shorter, doubles/hangs read longer — pill-counting
   §4.2, drone-spreaders §M10). Baseline for all champions: modulated
   through-beam IR, recessed optics, dark-time gating, beam-clear self-test
   before each dispense; capacitive/EFS ring as the bench-tested fallback if
   optics foul. Load cell = end-of-sortie audit only (1.18 g is unresolvable
   against rotor vibration in flight — pill-counting §4.5, drone-spreaders M9).
3. **Jam state machine + safe-state stop.** Stall-detect → reverse → retry ×3 →
   fault report (Halo Z-Code pattern), torque/current limit below pellet crush,
   manual override/clearing path (Rip Drive pattern), and a mechanically
   defined rest state so 12V_PL power cycling cannot corrupt the count (PSD
   safe-stop cam / non-back-drivable index).

Control contract implied (scoped to ICD only, no software phase):
`dispense(N)` → index/cycle until verified count = N → reply
`dispensed(n_verified, fault_flags)`.

---

## 1. Candidate roster and scores

Scale 1–5 (5 best). Scores are **[J]**, anchored on the cited evidence in the
research docs. "Count" = count-accuracy *potential of the mechanism itself*
(before the mandatory sensor closes the loop — the sensor turns skips into
non-events but cannot fix a mechanism that releases uncontrolled extras).
"Jam" = resistance to dust + fragments + bridging + the swollen-pellet case.
"Build" = 3D-printability + COTS actuator fit inside 24 W. "Mass" = payload
mass economy. "Glove" = field serviceability with gloves (clear a jam, clean,
reload, swap wear parts at a tailgate).

| # | Mechanism (source sections) | Count | Jam | Build | Mass | Glove | Verdict |
|---|---|---|---|---|---|---|---|
| A | **Rotary pocketed wheel/disc** (gumball/seed-meter/carousel hybrid; seed §3 §5, proj §1, pill §2, bulk §1, drone M1) | 5 | 4 | 5 | 5 | 4 | **CHAMPION 1** |
| B | **PSD nest + flapper escapement** (S-tube queue + sump agitator + cam; seed §6, drone §2.2) | 5 | 4 | 3 | 3 | 3 | **CHAMPION 2** |
| C | **Reciprocating single-cavity shuttle** (servo slide; drone M2, pill §5 side-shuttle) | 4 | 3 | 5 | 5 | 5 | **CHAMPION 3** |
| D | **Dual-gate (airlock) escapement on short gravity column** (seed §7, proj §2, pill §5, bulk §9, drone M3) | 5 | 3 | 4 | 4 | 4 | **CHAMPION 4** |
| E | Drum meter, peripheral pockets (fish-feeder; bulk §2) | 5 | 3 | 4 | 4 | 3 | Reject — packaging variant of A |
| F | Vacuum disc + singulator (seed §1, proj §7, bulk §4, drone M6) | 4 | 2 | 2 | 2 | 2 | Reject — power/dust; named fallback |
| G | Finger pickup meter (seed §2, bulk §5) | 3 | 2 | 2 | 3 | 2 | Reject |
| H | Auger / screw (proj §6, bulk §3, drone M5) | 1 | 1 | 4 | 4 | 3 | Reject |
| I | Helical vending coil (drone M4) | 3 | 2 | 4 | 4 | 3 | Reject |
| J | Vibratory singulation + optical count (pharma; seed §8, pill §3, bulk §8, drone M7) | 5 | 3 | 2 | 2 | 3 | Reject feeder; **sensing philosophy adopted** |
| K | Slat counter (pill §1) | 5 | 3 | 1 | 1 | 2 | Reject machine; principle = A |
| L | Spring-follower magazine, full capacity (proj §3) | – | 2 | 2 | 2 | 3 | Reject as primary (3 m column); OK as 5–15 pellet buffer |
| M | Spinner/broadcast, mass-rate spreaders (drone §2.1, seed §12) | 1 | 4 | 3 | 3 | 4 | Reject — no notion of count |
| N | Pneumatic pod firing (AirSeed; seed §12) | 2 | 3 | 1 | 1 | 2 | Reject — power/friability; noted wind-drift fallback |
| O | Weight-based metering as primary (drone M9, pill §4.5) | 1 | – | 3 | 4 | – | Reject as primary; keep as audit |
| P | Kinze brush-meter compliant wiper (seed §3) | – | – | – | – | – | Not standalone: **feature folded into A/C/D** |
| Q | Paintball force-feed (Rotor/Halo; proj §5) | 1 | 5 | 2 | 2 | 3 | Reject mechanism; **jam firmware pattern adopted** |

---

## 2. Scoring notes — the four champions

### A. Rotary pocketed wheel ("celled disc") — CHAMPION 1, primary

The only mechanism ranked first or co-first by **all five** research domains
independently (seed-meter archetype + UAV briquette carousel US11370599 /
mosquito-carousel US10499628; gumball wheel; ScriptPro cell 99.70 %; drone
M1). Disc with through- or blind pockets bored for the 13 mm worst case, depth
< 2 pellet diameters so a double is geometrically impossible; stationary plate
retains the pellet until the pocket indexes over the exit port; compliant
brush wiper (Kinze brush-meter DNA — deflects instead of shearing a friable
pellet) strips a second pellet at the fill station; agitator fingers on the
same shaft break arches every index for free.

- **Count 5:** positive displacement — geometry, not control, bounds output at
  one pellet per index. Failure mode is a *skip* (empty pocket), which the
  mandatory sensor converts into "index again" — a non-event. Nearest
  quantified anchors: ScriptPro 99.70 % per pill; seed discs >99 % singulation.
- **Jam 4:** dust falls through / sits in pockets and is carried out; no spring
  stack to pack fines; fines-relief slot under the disc is free. Reversible
  stepper gives the reverse-and-retry recovery every domain recommends. The
  gumball literature's known jam (half-seated ball sheared at the pocket lip)
  is the risk — mitigated by brush wiper + chamfers + torque limit below
  7.5 kgf. Swollen pellet cannot enter a pocket (correct behaviour) but can
  bridge the throat → handled by the mandatory sump agitator.
- **Build 5:** one printed disc, one plate, one brush, one COTS stepper
  (NEMA-11/14 class) well inside 24 W. Fully parametric on `PELLET_D`.
- **Mass 5:** the mosquito-control carousel analogue was 410 g empty printed
  ABS; IGNIS proves the whole-payload envelope at 1.87 kg loaded with hardware
  we delete.
- **Glove 4:** drop the bottom plate → whole pellet path exposed; brush and
  disc are tool-free-swappable wear parts (Kinze Brush Meter 2.0 precedent).
  Small residual: pocket edges are finger-sized, not glove-sized — design the
  plate release as a quarter-turn latch **[J]**.

### B. PSD nest-and-flapper escapement — CHAMPION 2, flight-proven lineage

Aerial-ignition architecture (US10871358, productised as Drone Amplified
IGNIS III Mini) with the ignition subsystem deleted: hopper + **rotating sump
agitator at the exit hole** + S-tube single-file queue + radius-matched "nest"
+ spring-steel flapper retaining the lead sphere + one cam cycle per release,
with a **cam switch that only permits stopping in a safe post-discharge
state**. IGNIS III Mini is the existence proof at almost exactly our scale:
19 mm / 2.4 g spheres × 225, 120/min, 1.87 kg loaded — our pellet is smaller
and lighter.

- **Count 5:** structurally exact — one sphere per crank revolution; each
  pellet is physically separated in the nest before the next enters. The
  safe-stop cam is the strongest answer any candidate has to the ICD's
  "tolerate 12V_PL power cycling" requirement.
- **Jam 4:** best-defended bulk stage in the survey (sump agitator attacks
  bridging at its source), and the compliant flapper mirrors the brush-wiper
  virtue. Residual risk is real and documented: USFS names seam flash,
  out-of-round bodies, moisture clumping and brittle aged spheres as PSD jam
  causes — all present in our pellet — and a fragment wedged in the S-tube is
  a hard jam with no bypass. Mitigate with ≥1.6×D tube ID (~20 mm, Elscint
  irregular-ball rule) and a reversible drive at the nest.
- **Build 3:** cam + crank + formed spring-steel flapper + shaped S-tube is
  more parts and more tuned parts (flapper stiffness, nest radius) than A/C/D;
  still one gearmotor + one agitator motor, comfortably inside 24 W.
- **Mass 3:** two motors and a tube run; IGNIS numbers say the envelope closes
  after deleting glycol hardware, but it is the heaviest champion.
- **Glove 3:** the S-tube is the weak point — clearing a mid-tube wedge in
  gloves needs a split/hinged tube cover designed in from the start **[J]**.

### C. Servo-driven single-cavity reciprocating shuttle — CHAMPION 3, simplicity floor

Classic industrial "escapement and nest" as a linear slide: one pellet-sized
cavity shuttles between fill (under the throat) and drop (over the chute).
One stroke = at most one pellet. **Servo, not solenoid** (position feedback,
graceful reverse; a solenoid slams at full force with no retry), with a spring
(compliant) coupling so a caught pellet deflects the drive instead of being
guillotined.

- **Count 4:** exact per stroke by the same geometric argument as A; scored one
  lower because an empty cavity (partial fill at end of stroke) is more likely
  than in a continuously indexing wheel, so it leans harder on the sensor+retry
  loop.
- **Jam 3:** the slide is a shear pair with a hard end-stop — the worst pinch
  geometry of the four champions for a 7.5 kgf-crush pellet; compliant coupling
  + chamfered lips + torque-limited servo are mandatory, and its fill zone
  needs the agitator more than A does (no rotating disc to stir the sump).
- **Build 5:** fewest parts of any exact-count candidate: one printed slide,
  one hobby-class servo, one microswitch. The natural bench-comparison mule —
  it can be printed and testing pellets within a day **[J]**.
- **Mass 5:** lightest possible meter.
- **Glove 5:** everything is at the surface; the slide pulls out by hand; no
  tube, no disc stack. Best tailgate-serviceability of the survey.

### D. Dual-gate (airlock) escapement on a short buffered column — CHAMPION 4, geometric guarantee

Two gates spaced one pellet apart at the bottom of a **short (~10–15 pellet)**
single-file buffer column fed by the agitated hopper (the hybrid explicitly
recommended in seed-metering §7 — full-capacity columns are rejected: 250
pellets = 3.25 m of tube). Upper gate holds the column while the lower gate
releases exactly one; the interstage volume physically cannot hold two if
spaced < 2×D. One actuator drives both gates via rocker/cam so the gates are
mechanically interlocked (never both open) **[J]**. Golf-ball dispenser and
industrial parts-feeder art; Elscint's cast-ball feeder proves the pattern on
6–16 mm *irregular* balls released one-per-signal.

- **Count 5:** the strongest *geometric* "exactly one per cycle" of the four —
  the interstage is a physical airlock. The interstage is also a natural
  staged-pellet sensing pocket, enabling the confirm-before-release +
  confirm-after-release double observation recommended in seed-metering §9.
- **Jam 3:** the column is the liability: fragments, cocked barrel-shaped
  pellets and fines packing in a 14 mm tube are its documented failure class
  (M249 box-mag doubling; drone-spreaders M3 "attractive on paper, poor in
  dust"), and gravity can't be reversed to clear it. Short column + oversize
  ID + fragment relief slot + compliant gate faces mitigate but don't remove
  this.
- **Build 4:** one servo, two pins/one rocker, one printed tube — simple, but
  the hopper→column transition needs care (it inherits the bridging problem
  at its worst point).
- **Mass 4:** light; slightly more structure than C for the column.
- **Glove 4:** straight vertical tube with a hinged front face is easy to
  clear; gates accessible at the bottom.

### Why these four are maximally diverse

Each champion embodies a **different singulation primitive**, so their failure
modes are decorrelated and the downstream concept phase genuinely explores the
space rather than re-drawing one idea four ways:

- A: **rotary positive-displacement pocket** (continuous-path, skip-tolerant)
- B: **queue + compliant nest + cam cycle** (flight-proven, safe-state-centric)
- C: **linear positive-displacement cavity** (minimum parts, minimum mass)
- D: **static column + interlocked two-gate airlock** (pure geometric count,
  best sensing geometry)

They also diversify the actuator (stepper / gearmotor+cam / servo / servo-
rocker), the pellet path (loose sump / S-tube / sump / vertical column), and
where the "exactly one" guarantee lives (pocket geometry / cam phase / cavity
geometry / interstage volume). All four share the mandatory §0.1 stack
(agitated sump, dark-time-gated through-beam verification, stall-reverse-retry,
safe rest state), so the sensing/firmware contract work transfers no matter
which concept wins.

---

## 3. Rejections, with reasons

- **E. Drum meter (fish-feeder):** same physics as A with worse vertical
  packaging under a belly with tight ground clearance and full hopper load
  bearing on the drum surface (higher shear on a wedged pellet). Adds no
  diversity — bulk-dispensers itself ranked it "same physics, worse
  packaging". Rejected as redundant with Champion A.
- **F. Vacuum disc:** best published singulation in ag (98–99 %+), but the
  derived production design ratio (~28× seed weight, 18–21 inH₂O) puts our
  1.18 g pellet at ~Ø9 mm apertures with a blower that is marginal-to-
  impossible on the 24 W rail; a porous/molded pellet seals badly
  (ASSUMPTION, high confidence, seed-metering §1); and the aperture/dust
  hazard profile is exactly our environment's worst case. It also still needs
  the sensor we must fit anyway — it buys accuracy we get cheaper. **Status:
  named fallback** if pellet shape variance defeats all mechanical pocketing.
- **G. Finger pickup:** 94–99 %, strongly size-sensitive, explicitly
  non-adjustable, crush-prone pinch points, high part count. Its one good
  idea — the singulating brush — is already folded into Champion A.
- **H. Auger:** volumetric, not discrete; releases 0–2 uncontrolled extras
  after stop; shear line grinds a 7.5 kgf friable pellet into the fines we
  must avoid creating. Rejected by every domain that scored it.
- **I. Helical vending coil:** one-per-revolution in principle, but the
  vending "hung product" misvend recovery (keep rotating) breaks the count;
  horizontal packaging is wrong under a belly mount; strictly dominated by A.
- **J. Vibratory singulation + optical counting:** highest published counting
  accuracy (99.99 % Deitz "at optimal conditions"), but vibratory feeding
  needs a stable gravity frame a hovering multirotor doesn't provide, fights
  the airframe's own vibration, and US11286119 documents vibratory agitation
  as the wrong answer structurally. **Adopted instead:** its verification
  back-end (dark-time gating, dynamic thresholding, EFS option) — see §0.1.
- **K. Slat counter:** deterministic cavity counting, but a linear chain +
  format parts machine built for 200–300 bottles/min; and the industry bolts
  a 2000 Hz scanner on anyway (TruCount), conceding cavity counting isn't
  trusted alone. Its principle (cavities + wiper) *is* Champion A.
- **L. Full-capacity spring-follower magazine:** 250 pellets = ~3 m of column;
  cannot package; constant spring pressure on a friable stack risks attrition.
  Retained only as an optional short buffer inside Champion D.
- **M. Spinner/broadcast (DJI Agras class):** COTS spreaders are specced for
  0.5–5 mm granules (ours is 12 mm) and meter mass on a weight sensor — they
  physically cannot deliver "exactly 3". This rejection is also the product
  story: no COTS path exists.
- **N. Pneumatic pod firing (AirSeed):** would trivially beat the 1 m CEP by
  swamping wind drift, but needs stored-gas/high energy outside 24 W and
  would shatter a 7.5 kgf pellet. **Noted as the documented fallback if the
  ballistics sim kills passive drop at the honest wind limit.**
- **O. Weight-based metering/verification as primary:** 1.18 g steps are
  trivially resolvable on a bench and unresolvable under rotor vibration in
  flight. Kept as pre-flight load count + end-of-sortie audit only.
- **P. Kinze brush meter:** not rejected — *absorbed*. "Only one moving part"
  and the compliant-brush-instead-of-shear principle are load-bearing features
  of Champions A (wiper), and the compliant-face rule in C and D.
- **Q. Paintball force-feed (Rotor/Halo):** built to feed as fast as possible,
  not to stop at N; mechanically overkill at ~1 Hz. **Adopted instead:** its
  jam firmware (stall → reverse → retry ×3 → failsafe), torque-limited gentle
  drive, and manual override wheel — mandatory features for all champions.
- **Mechanical-index-only counting (US11370599 carousel as patented):** the
  patent explicitly infers count from mechanical steps with no electronic
  verification — precisely what Thomas's "verified, not assumed" requirement
  forbids. The carousel geometry survives (inside Champion A); the open-loop
  counting philosophy does not.

---

## 4. Cross-champion open unknowns (carried from research; do not invent)

1. **Pellet geometry distribution:** caliper/weigh 20+ pellets on both axes —
   sphere vs barrel changes pocket/cavity/tube geometry for A, C, D.
2. **Friability/fines rate:** USP ⟨1216⟩-style tumble test (25 rpm, 4 min) on
   real pellets; sizes the dust problem for sensing and clearances.
3. **Crush strength of the actual pellet:** confirm the US4172714-class
   7.5 kgf figure before setting torque limits.
4. **Swollen-pellet jam test:** soak-and-dry one pellet as the worst-case jam
   article for all four concepts.
5. **Buy and tear down the $650 Brush Pod** (vendor's own aerial applicator
   for this exact pellet) — retires more risk than any further web research.
6. **Contact SkySong Innovations (ASU case M23-217L)** — closest public prior
   art, anti-jamming mechanism undisclosed.
7. **Sensor bench test** against deliberately dusty/fragmented pellets before
   freezing any meter geometry (optical baseline vs capacitive/EFS ring).
