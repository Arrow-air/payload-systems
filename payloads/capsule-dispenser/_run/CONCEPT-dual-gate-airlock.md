# CONCEPT — "dual-gate-airlock": Dual-Gate (Airlock) Escapement on a Short Buffered Column

Concept-development agent output, 2026-08-06. Advocate document for Champion D
(MECHANISM-SURVEY §2.D). Sources: CONTEXT.md (ground truth), MECHANISM-SURVEY.md,
RESEARCH-projectile-feeders.md §2 §4 §8 §9 (primary domain), RESEARCH-seed-metering.md
§7 §9 §11, RESEARCH-bulk-dispensers.md §9 §10, RESEARCH-pill-counting.md §4 §5,
RESEARCH-drone-spreaders.md §1 M3 M10. Everything derived is marked **[D]** with the
arithmetic shown; unverified items are **ASSUMPTION**. No CAD yet — sketch level.

## 1. Claim (what this concept is betting on)

One servo cycles two mechanically interlocked gates at the bottom of a short
single-file buffer column. The interstage volume between the gates physically
cannot contain two pellets, so each cycle releases exactly one — the count
guarantee is **static geometry**, not a moving pocket or a cam phase. The
interstage doubles as a staged-pellet sensing pocket, giving **two independent
observations per pellet** (confirm-before-release + confirm-after-release), the
best sensing geometry of any champion (seed-metering §9 recommendation,
implemented literally). Prior art: golf-ball dispenser pin escapements
(US6523718, US5529307), industrial two-finger escapements (Hoosier/Bellco/AGI),
and Elscint's cast-ball feeder — 6–16 mm *irregular* balls singulated
one-per-signal (pill-counting §5).

The honest bet: the count core is nearly unbeatable; the **availability** of a
pellet at that core (hopper → column throat) is this concept's weakest link,
and everything in §4 and §9 below is about that.

---

## 2. Architecture and layout

Vertical stack, drop point near the airframe centerline for drop accuracy.
The buffer column hangs from the hopper sump; gates and chute below it.

```
        ┌────────────────────────┐  ← payload-side clip plate (BOM 2112,
        │   50×50 clip plate     │     50×50×10.5) + blind-mate PCB
   ┌────┴────────────────────────┴────┐   adapter frame, 6 mm
   │                                  │  ─ 0 (payload top plane, Z ≈ −171 drone)
   │        HOPPER  ~0.72 L usable    │
   │   interior 135 × 115, walls ≥55° │   hopper section ~120 mm tall
   │  ┌sealed hinged lid on top face┐ │
   │   \                            / │
   │    \      wedge sump          /  │
   │     \   [agitator shaft ⊙]   /   │  ← GA12/N20 gearmotor, TPU fingers
   │      \______  ______________/    │     sweeping the column mouth
   └─────────────││────────────── ────┘  ─ ~126 mm
                 ││  ← throat / column mouth (the risk zone)
                 ││
                 ││   buffer column: Ø21 mm ID × 130 mm
                 ││   ≈ 10 pellets nominal          ─ hinged front cover
                 ││
              ═══╪═══  UPPER GATE (wedge blade, TPU face)
                 |○|   INTERSTAGE: 18 mm clear height
                 |○|←— S1: modulated IR through-beam (staged-pellet sensor)
              ═══╪═══  LOWER GATE (blade + seat)          ─ ~286 mm
                 ││
                 ││   drop chute Ø22 mm × ~25 mm
                 |·|←— S2: modulated IR through-beam, dark-time gated
                 \/                                       ─ ~311 mm
              (free fall, ~8 m AGL)
```

Key dimensions (all mm, parametric on `PELLET_D = 12`, worst case 13,
best case 11 per CONTEXT ASSUMPTION ±1):

| Item | Value | Basis |
|---|---|---|
| Column ID | **21** | ≥1.6×D_max = 20.8 (Elscint oversize anti-jam rule, pill §5) AND < 2×D_min = 22 (single-file guarantee). **[D]** The window is 20.8–22 mm — see §9. |
| Column length | 130 (≈10 pellets) | survey mandate: short buffer, not full column (250 pellets = 3.25 m, seed §7) |
| Interstage clear height (upper blade plane → lower gate seat) | **18** | holds one 13 mm pellet + 5 mm clearance; two smallest pellets need ≥ 2×11 = 22 > 18 → geometrically excluded **[D]** |
| Gate blades | 8 wide, wedge nose, 2 mm TPU face, 12 stroke | compliant-face rule (Kinze/eSet lineage, survey §0.1) |
| Gate vertical spacing (blade planes) | 18 | = interstage height |
| Chute ID / length | 22 / 25 | ≥ column ID, no step to catch fragments |
| Hopper interior | 135 × 115 × ~105, walls ≥ 55° from horizontal | ≥45° heuristic (seed §11) + margin; steep walls reduce clogging (proj §9) |
| Overall envelope | ~150 W × 130 D × ~315 H below mounting plane | see §6 ground-clearance derivation |

---

## 3. Metering mechanism and actuator

**Gate pair + rocker.** Two horizontal wedge-nosed blades enter the column
through wall slots, driven by one see-saw rocker from a single servo horn.
Rocker geometry gives a **mechanical interlock**: the two stable ends of travel
are FILL (lower blade in / upper out) and RELEASE (upper in / lower out), and
mid-travel both blades are partially inserted (**both-closed overlap**). There
is no rocker position with both gates open — the "never both open" property is
kinematic, not firmware.

**Cycle** (one pellet):

1. Rest = FILL: column stands on the lower gate; bottom pellet occupies the
   interstage; S1 dark = staged confirmed.
2. Servo sweeps to RELEASE: upper blade wedges into the gap above the staged
   pellet (separating it from pellet 2 and taking the column weight), then the
   lower blade retracts → staged pellet falls through the chute past S2.
3. Servo returns to FILL: lower closes first (overlap), upper opens, column
   advances one pitch, next pellet seats in the interstage → S1 dark again.

The upper blade's job — entering a gap whose position varies with pellet
diameter and cocking — is the mechanically fragile step; the wedge nose is
angled so it cams pellet 2 *upward* (against a ~18 g column, trivial force)
rather than shearing the staged pellet. See §9.

**Timing [D].** Servo travel ~60° each way at ~0.15 s + settle ≈ 0.5 s per
pellet → N = 10 in ≈ 5 s plus verification retries. Requirement is ~1 Hz-class
per-target drops — comfortable.

**Actuator choice: serial-bus servo** (Feetech STS3215 class, ~60 g, run at
6 V from a buck; position + current telemetry over its serial bus to the
payload MCU). Rationale:

- Position feedback + current sensing implement the mandatory stall-detect →
  reverse → retry ×3 → fault state machine (Halo Z-Code pattern, survey §0.1)
  with no extra sensors. A dumb PWM hobby servo hides stalls; a solenoid slams
  at full force with no retry (survey §2.C note applies equally here).
- **Force limiting below pellet crush:** class-datum crush load ≈ 7.5 kgf
  (US4172714, drone-spreaders §1.3 — pellet-specific value is an open unknown,
  survey §4.3). At the chosen horn/rocker lever ratio a 15–19 kg·cm servo can
  exceed that at the blade **[D]**, so the firmware current limit is set to cap
  blade force at ≤ 4 kgf, and the 2 mm TPU face + wedge geometry sheds point
  loads. The gate must *never* be the thing that makes fines.
- **Defined rest state:** a light torsion spring biases the rocker to FILL, so
  loss of servo power (12VSW dropped, or 12V_PL cycling per ICD §3) leaves the
  lower gate closed and the column retained. See §9 power-cycle case.

**Agitator actuator:** 12 V brushed gearmotor (GA12/N20 class, ~30–60 rpm at
the paddle shaft), current-limited in firmware, driving a hub of compliant TPU
fingers that sweep directly across the column mouth (§4).

---

## 4. Hopper: capacity, anti-bridging, agitation

**Capacity [D].** Usable interior ≈ 0.72 L (prismatic 135×115×40 section +
converging wedge; minus sump hardware — sketch-level estimate, ±15%). Using the
derived bulk densities (drone-spreaders §1.4): barrel-shaped worst case
250 pellets ≈ 0.57 L → capacity ≈ **315 pellets worst-case** (~440 if pellets
are true spheres). Hard minimum 250 is met with ≥25% margin, and per CONTEXT
extra capacity is reported as a positive: **≈315–440 pellets** depending on
true pellet shape (open unknown §4.1 of survey).

**Why agitation is non-optional here.** The anti-bridging orifice rule
(6–8×D → 72–96 mm; derived independently in three research domains) puts our
~21 mm column mouth deep in the interlocking-arch regime *by design*. This
concept feeds a single-file throat directly from bulk — it inherits the
bridging problem at its worst point (survey §2.D "Build" note). Passive
geometry cannot fix that; the mitigations are:

- **Steep smooth walls** (≥55° from horizontal, printed then smoothed or lined)
  converging to a slot directly over the column mouth.
- **Powered sump agitator at the throat**: horizontal shaft, compliant TPU
  fingers passing within ~2 mm of the column mouth each revolution — the
  PSD-sump / paintball-soft-paddle pattern (proj §4, US7694669, soft impeller
  US2004/0074489). NOT a vibration motor: US11286119 documents vibratory
  agitation as causing bearing wear and poor performance, and it would pollute
  the IMU (survey §0.1).
- **Demand-driven duty**: the agitator runs only when S1 reports "interstage
  empty after a column advance" (starvation) plus a short stir before each
  commanded dispense. Torque-limited below crush; reversible for retry.
- **Sealed hinged lid with gasket**: the pellet swells 2–3× irreversibly when
  wetted (US4172714) — moisture exclusion is a hopper *requirement*, not a
  finish detail.
- **Fines management**: wall fillets ≥ 3 mm everywhere in the sump; a fines
  relief slot (3 mm) at the column mouth lip and at each gate seat lets dust
  fall through instead of packing (proj §2 INFERENCE adopted).

**ASSUMPTION:** a single-slot throat with one agitator singulates adequately.
If bench tests show rathole/starve behaviour, the documented fallback is a
small rotary pre-feeder fin at the mouth — which starts reintroducing Champion
A's complexity and is called out honestly in §10.

---

## 5. Count verification (sensed, not assumed)

Two sensing points, two independent observations per pellet — the
confirm-before-release + confirm-after-release scheme recommended in
seed-metering §9, which this geometry gets almost for free:

**S1 — interstage staged-pellet sensor.** Modulated IR through-beam across the
interstage, emitter/detector recessed behind 2 mm apertures (dust film
mitigation, pill §4.1–4.2). Beam axis 6 mm above the lower gate seat **[D]**:
a seated pellet (11–13 mm) always blocks it, while flat-lying fragments and
fines below ~5 mm sit under the beam and cannot false-confirm. Functions:
confirm-staged before each release; detect column starvation (drive agitator);
detect "still dark after release" = pellet hung in interstage → retry.

**S2 — drop-chute passage sensor.** Modulated IR through-beam across the 22 mm
chute, ~40 mm below the interstage centre, **dark-time gated** (pill §4.2 —
"the single highest-value idea"): fall from rest through ~40 mm gives
v ≈ √(2·9.81·0.040) ≈ 0.89 m/s → a 12 mm pellet occludes ≈ 13.5 ms **[D]**
(consistent with the 6–12 ms figure at chute speeds, survey §0.1). Accept
window ≈ 8–25 ms = one pellet; shorter = fragment (logged, **not** counted);
longer = hang or double → fault path. Beam-clear self-test before every
dispense (survey §0.1 baseline).

**Fallback sensing:** capacitive/EFS ring around the chute (pharma dust-immune
option, US8141330 / Sparc; pill §4.3) is the bench-tested alternate if optics
foul faster than the cleaning interval — the chute geometry accepts a ring
electrode with no mechanical change. Load-cell = pre-flight inventory and
end-of-sortie audit only (unresolvable in flight, survey §0.1).

**Count logic / ICD contract** (contract only — software phase is out of scope
per Thomas 2026-08-06):

- Command: `dispense(N)`, N ∈ 1..10, over **CAN2 (DroneCAN)**. FMU_CH1 PWM
  reserved as an optional discrete "dispense 1" backup trigger (bottom port
  only, ICD §4).
- Per pellet: S1 staged? → cycle gates → S2 valid pulse? → increment
  `n_verified`. Any miss → retry state machine: re-cycle, pulse/reverse
  agitator, ×3, then stop safe and set fault.
- Reply: `dispensed(n_verified, fault_flags)`; flags include `jam_column`,
  `jam_gate`, `starved`, `fragment_seen`, `sensor_selftest_fail`,
  `possible_uncounted_release` (§9 power case), `hopper_low` (inventory
  estimate from load audit + running count).

---

## 6. Mounting and envelope (clip plate, ground clearance)

- Bolts to the payload-side clip plate (BOM 2112 clip half, 50×50×10.5,
  `2112_attach_plate_payload_side.step`) via a 6 mm adapter frame that spreads
  the 50×50 interface into the hopper lid perimeter; blind-mate PCB aligned to
  the silkscreen notch (mechanical README). Column + chute axis placed within
  ~15 mm of plate centre so the release point is near the airframe centreline
  and the loaded CG stays under the clip plate (pellet mass sits in the hopper,
  which is centred; ASSUMPTION: CG offset < 10 mm loaded, verify in CAD).
- **Ground clearance [D]** (derived from `/tmp/pq-main/src/quiver/airframe_structure/landing_gear/assembly.py`):
  horizontal cross-tube axis Z = −527.89, foam sleeve OD 40 → uncompressed
  ground contact plane Z ≈ −547.9. Bottom payload mounting plane Z ≈ −171
  (mechanical README) → **377 mm available**. This payload extends ~315 mm
  below the mounting plane → lowest point Z ≈ −486, **~62 mm ground clearance
  at rest** before foam compression. Adequate but not generous; foam
  compression under landing loads must be checked before freezing the column
  length (recorded as open item).
- Lateral: leg axis splays outward; at Z = −486 the inner clear half-width is
  ≈ 242 mm in X (leg axis 257 − tube radius 15) and 108 mm in Y **[D]** — our
  75 mm half-width clears both. Prop disks are far above the belly plane.

---

## 7. Power vs the 2 A / 25 W limits

Split across the two rails deliberately:

- **12V_PL (~25 W budget, SSR, can cycle):** MCU (STM32 + CAN transceiver),
  sensors, buck to 3.3 V logic — **< 1.5 W**. Keeping brains + sensors on
  12V_PL means an FC-commanded 12VSW kill does not blind the counter.
- **12VSW (relay K1, 2 A fuse, ~24 W):** actuation only, so the FC can
  hard-kill motion (its designed purpose per ICD §3). Buck 12→6 V for the bus
  servo: peak 2 A @ 6 V = 12 W ≈ 1.2 A @ 12 V at 85% **[D]**; firmware current
  limit holds it below this. Agitator: current-limited to 0.5 A @ 12 V = 6 W
  stall, ~0.2 A running.

Worst honest simultaneous case **[D]**: servo peak 1.2 A + agitator limit
0.5 A + conversion overhead ≈ **1.8 A (≈21 W) on 12VSW** — inside the 2 A fuse
but with only ~10% margin, so firmware additionally staggers full-torque servo
retries against agitator pulses (they are never required simultaneously: the
agitator fills the column, the servo empties it). Buck soft-start and servo
power via a load switch keep inrush under the fuse rating. No 5 V from the
aircraft — both bucks are ours (ICD §3, "bring a buck").

Duty-cycle energy is trivial: ~0.5 s of servo + occasional agitator per pellet,
tens of joules per sortie.

---

## 8. Mass estimate

Printed parts ASA (heat, §9), ±30% at sketch level; COTS masses are catalog
class figures (ASSUMPTION until weighed).

| Item | g |
|---|---|
| Hopper shell + sealed hinged lid (ASA, 2.0–2.4 mm + ribs) | 190 |
| Sump/throat insert + agitator mounts | 35 |
| Buffer column + hinged front cover + latches | 45 |
| Gate blades ×2, rocker, pivots, torsion spring, TPU faces | 30 |
| Bus servo (STS3215 class) | 60 |
| Agitator gearmotor + finger hub | 35 |
| Electronics: MCU/CAN board, 2× buck, driver, S1/S2, harness | 65 |
| Drop chute + sensor housings | 30 |
| Payload-side clip plate (aluminum, ASSUMPTION — weigh actual) | 55 |
| Adapter frame + fasteners | 55 |
| **Empty total** | **≈ 600** |
| + 250 pellets (baseline load, 250 × 1.18 g) | 295 |
| **Loaded (250)** | **≈ 895** |
| + full hopper ≈ 315 pellets worst-case shape | 372 |
| **Loaded (full, ~315)** | **≈ 972** |

Comfortably under the 1.5 kg ceiling (~500 g margin at the 250-load baseline;
no >1.0 kg justification needed). Clip-plate static load < 1 kg is benign;
dynamic factor check deferred to CAD phase.

---

## 9. Failure modes and honest mitigations

| Failure | Mechanism | Mitigation | Residual truth |
|---|---|---|---|
| **Bridging / starvation at column mouth** | 21 mm throat is ~1.75×D — deep inside the clogging regime by the 6–8×D rule | steep smooth sump, TPU-finger agitator sweeping the mouth, demand-driven + pre-dispense stir, starvation detected by S1, retry loop | **Biggest liability of the concept.** Agitation is probabilistic, not geometric; a persistent rathole = missed drop and a fault report, not a silent miscount |
| **Fragment / half-pellet in column** | friable pellet (crush ~7.5 kgf class); fragments cock and wedge; the M249 doubling failure class is documented for exactly this geometry | 21 mm oversize ID (Elscint rule) passes most fragments; fines slots at gate seats; S2 dark-time rejects fragments from the count; interstage excludes two *pellets* but **not** pellet+fragment | a co-released fragment adds an unquantified partial dose (logged via `fragment_seen`); a hard-wedged shard mid-column **cannot be cleared in flight — gravity does not reverse** (M3 verdict). Hinged column face = tailgate fix only |
| **Cocked barrel pellet defeats upper gate** | inter-pellet gap position varies ±2–3 mm with ±1 mm dia + cocking in the oversize tube | wedge-nosed compliant blade cams pellet 2 upward against trivial (~18 g) column weight; miss → detected by S1/S2 mismatch → re-cycle retry ×3 | every retry costs ~0.5 s; a bad pellet batch degrades rate; pellet-shape caliper survey (survey §4.1) is a gating unknown |
| **Swollen pellet (wetted, 2–3×, irreversible)** | worst-case jam article (US4172714) — a ~25–30 mm body cannot enter the column and cannot be crushed within torque limits | gasketed lid (prevention is primary); throat shaped so agitator fingers push an oversize body aside into the sump rather than wedging it; fault after retries | a swollen pellet *in the sump slot* is a mission-ending jam until ground service; we mitigate exposure, not the physics |
| **Dust film on optics** | bentonite/urea fines + ranch dust; "dust counted as seed" is the documented optical failure | recessed 2 mm apertures, modulated IR, beam-clear self-test each dispense, dark-time gating; EFS ring fallback if bench tests fail optics | maintenance interval set by dust, unknown until the tumble-test fines rate (survey §4.2) is measured |
| **Gate pinch crushes pellet** | servo can exceed 7.5 kgf-class crush at the blade | firmware current limit ⇒ ≤ 4 kgf blade force, TPU faces, chamfers; stall → reverse → retry ×3 → fault | limit is set against a *class* datum; real crush strength unmeasured (survey §4.3) |
| **Vibration** | rotor vibration grinds column stack; false sensor triggers | short column ⇒ ~18 g stack load (an order gentler than any spring-follower); TPU gate faces; modulated beams ignore vibration; no vibratory agitation anywhere | vibration-driven attrition *rate* unknown — feeds the dust problem above |
| **Heat (West Texas, dark belly)** | printed creep, servo derating; pellet binder (PEG/urea) may soften/stick (ASSUMPTION — untested) | ASA/PC prints, light-colored hopper, motors rated ≥ 60 °C, current limits derated with temperature | pellet hot-tack behaviour is an open unknown; a sticky pellet column defeats gravity feed and there is no in-flight recovery |
| **12V power cycling (ICD requirement)** | 12V_PL and/or 12VSW can drop at any time | torsion spring biases rocker to FILL (lower gate closed) — mechanically defined rest state; MCU+sensors on 12V_PL keep counting through a 12VSW kill; count state persisted to NV memory each cycle | if power drops in the ~150 ms release dwell, at most **one** pellet may fall uncounted → reported as `possible_uncounted_release`, never silently absorbed |

---

## 10. Why this might lose

Stated plainly, as the advocate:

1. **The count guarantee and the availability problem live in different
   places.** Our "exactly one" is the purest of the four champions — but it
   sits under a single-file throat that is the *worst* documented dust/bridging
   geometry in the survey (M3: "attractive on paper, poor in dust"). Champion A
   breaks arches every index for free with the same motor that meters; we pay
   a second actuator and still only get probabilistic feeding. If the judge
   weights feed reliability over count purity, A beats us on our own margin.
2. **The tube-ID design window is ~1 mm wide and rests on an assumption.**
   Single-file requires ID < 2×D_min = 22 mm; the Elscint anti-jam rule wants
   ID ≥ 1.6×D_max ≈ 20.8 mm. That 20.8–22 window exists only if the ±1 mm
   diameter ASSUMPTION holds. If the caliper survey shows ±1.5 mm or a strong
   barrel aspect, single-file and anti-jam become **mutually exclusive** and
   the concept needs a pre-orienting feeder — at which point it has quietly
   become Champion A with extra steps.
3. **Gravity cannot be reversed.** A, B and C can all back-drive their meter to
   clear a wedge; a hard jam in our column is unrecoverable until landing. Our
   jam state machine can only report it honestly.
4. **The sensing advantage may not be decisive.** Every champion already
   carries the mandatory dark-time-gated chute beam (survey §0.1). Our second
   observation (S1) buys earlier fault detection and starvation sensing —
   real margin, but margin on a requirement everyone already meets.
5. **Tallest thin structure, tightest ground clearance.** ~62 mm derived rest
   clearance is the least comfortable packaging of the four (C in particular
   is flat); foam compression or rough-field landings eat directly into it.
6. **More tuned than it looks.** The rocker overlap timing, wedge-nose angle,
   blade force limit and interstage height are four coupled tuning parameters
   around an irregular pellet; C has essentially one. "Simple" here describes
   the part count, not the tuning burden.

What would win it anyway: if the pellet survey confirms ≤ ±1 mm and modest
barrel aspect, this is the only design whose per-pellet guarantee needs *no
moving part to be anywhere in particular* — a static 18 mm gap either can or
cannot hold two pellets, forever, regardless of wear, backlash, or missed
steps. Decorrelated failure modes are exactly what a four-concept portfolio is
for (survey §2, "why these four").

## 11. Open items this concept needs before CAD

Inherited from survey §4, ranked by lethality to *this* concept:
1. Caliper/weigh 20+ pellets both axes → sets column ID window viability (§10.2).
2. Tumble-test fines rate → sizes dust load on S1/S2 and fines slots.
3. Crush strength of the real pellet → sets the blade force limit.
4. Soak-and-dry swollen pellet → sump rejection geometry test article.
5. Bench: hopper+throat+agitator mule (printable in a day) → starvation rate
   in dust before any gate hardware exists.
6. Landing-gear foam compression under landing loads → confirms the 62 mm rest
   clearance is real margin.
