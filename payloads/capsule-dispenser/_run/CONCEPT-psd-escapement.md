# CONCEPT — psd-escapement: PSD Nest-and-Flapper Escapement (ignition deleted)

Concept-development output, 2026-08-06. Champion B from `MECHANISM-SURVEY.md`.
Lineage: US 10,871,358 B2 (aerial-ignition PSD) → Drone Amplified IGNIS III
Mini, with the entire ignition subsystem (needle, pump, glycol reservoir,
injection dwell) deleted. Sources: `CONTEXT.md`, `MECHANISM-SURVEY.md`,
`RESEARCH-seed-metering.md` §6 §9 §11, `RESEARCH-drone-spreaders.md` §1 §2.2
§M10, `../../interface/ICD.md` v1.0-draft, `../../interface/mechanical/README.md`.

Labels: **[V]** verified (cited in the research docs), **[D]** derived
(arithmetic shown), **[A]** assumption, **[J]** engineering judgement.

I am the honest advocate for this concept. The case *for* it is §1; the case
against it is §9 and I have not softened it.

---

## 0. Why this architecture, in three sentences

IGNIS III Mini is the only **flight-proven** device that does almost exactly
our job at almost exactly our scale: singulate molded ~2 g spheres from a
~225-unit hopper, one per crank revolution, on a drone, in the field, at
1.87 kg loaded **[V]**. Our pellet is smaller and lighter (12 mm / 1.18 g vs
19 mm / 2.4 g) and we get to delete the glycol injection hardware, which is
most of the IGNIS parts count. What remains — agitated sump, S-tube queue,
radius-matched nest, spring flapper, one cam cycle per release, safe-stop cam
switch — is the strongest structural answer in the survey to the two hardest
requirements: *exactly one per cycle* and *12V_PL power cycling must not
corrupt the count*.

---

## 1. Mechanism layout

### 1.1 Pellet path (top to bottom)

```
        ┌───────────────────────────────┐   ← lid, gasketed (moisture seal)
        │        HOPPER  ~0.65 L        │
        │   floor slopes 30° → sump     │
        │        ┌────┐                 │
        │  sump  │agit│◄─ N20 gearmotor │   3 compliant TPU fingers sweep
        │  well  │ator│   (vertical)    │   directly over the exit hole
        └───┬────┴────┴─────────────────┘
            │ exit hole Ø20                ← swollen pellet cannot enter (good)
           ╱                               ← S-TUBE, ID 20, single-file,
          ╱   queue of 5–7 pellets            S-bend decouples hopper head
          ╲                                   pressure from the nest
           ╲
        ┌───▼──────────────┐
        │  NEST  R6.5      │◄─ cam/crank + pusher (25D-class 12 V gearmotor)
        │  [pellet]        │   one revolution = one release
        │  ═flapper═       │◄─ spring-steel flapper, hall sensor on root
        └───┬──────────────┘   cam-switch: motor can stop ONLY post-discharge
            │ drop chute Ø20
        ────┼────  ← modulated through-beam IR, recessed, 30 below flapper
            ▼  free fall from ~8 m AGL
```

### 1.2 The release cycle (one crank revolution)

The original PSD cam cycle is: needle down → inject → retract → sphere forced
past the flapper and discharged **[V, US10871358]**. With ignition deleted,
the needle becomes a plain **pusher finger**: a cam-driven plunger with
~16 mm stroke that pushes the nested pellet down through the flapper. The
flapper's preload holds the rest of the queue back; only the pushed pellet
passes; the queue then advances one and the lead pellet settles into the nest
under gravity + agitator feed. **[J]** Pusher tip is a compliant TPU pad,
14 mm diameter cup, so the load on the pellet is distributed, not a point.

- One revolution = at most one pellet, structurally (the nest holds one; the
  flapper separates it from the queue before the pusher ever moves) **[V]**.
- Cycle rate: design 1 rev/s, capability 2 rev/s (IGNIS does 120/min **[V]**).
  N=3 dispensed and verified in ~3 s. We are nowhere near the mechanism's
  rate limit — that headroom is wasted capability, noted honestly in §9.

### 1.3 Safe-stop cam switch (the power-cycling answer)

A second cam track closes a microswitch only in the **safe window**: pusher
fully retracted, pellet discharged, next pellet not yet loaded into a
committed position **[V, pattern from US10871358]**. Control rule: the motor
is only ever de-energised inside the safe window. On power-up (12V_PL or
12VSW restored after a cycle), the controller reads the switch; if the
mechanism is *outside* the safe window (power died mid-rev), it completes the
revolution to the safe stop **before accepting any command**, and reports
whether the drop-beam saw a pellet during that completion. The count can
therefore never be ambiguous by more than one pellet, and that one pellet is
independently observed by two sensors (§4). Dispensed-count per command-ID is
stored in the controller's nonvolatile memory **[J]**.

### 1.4 Actuator choices

| Function | Actuator | Sizing basis |
|---|---|---|
| Crank/cam/pusher | 12 V brushed gearmotor, 25 mm class (Pololu 25D style), ~100:1, ~60–120 rpm out | **[D]** Pusher force budget: flapper pass-through preload ≤ 0.4 kgf (§1.5) + friction ≈ ≤ 10 N at ~10 mm cam radius ≈ 0.1 N·m working; spec ≥ 0.3 N·m continuous for margin. Any 25 mm-class gearmotor clears this. Current-limited so pusher force stays < 3 kgf — 2.5× margin under the ~7.5 kgf pellet crush load **[V, US4172714-class]** |
| Sump agitator | 12 V N20 gearmotor, ~45 rpm, vertical shaft, 3 TPU fingers | **[J]** Torque-limited (current sense) so a finger stalls/deflects rather than crushing a pellet; runs only during a dispense window ±2 s |

Brushed DC + cam switch (not a stepper) is the deliberate IGNIS-pattern
choice **[V]**: indexing is enforced by the cam switch, not by open-loop
steps, so a stall is detected by current + switch timeout, and the drive is
reversible for the back-off-and-retry recovery. Both motors on **12VSW** so
the FC can hard-kill all mechanism power via K1 relay independently of the
logic (§5).

### 1.5 Key dimensions (sketch-level, mm — parametric on `PELLET_D` = 12)

| Feature | Value | Basis |
|---|---|---|
| Pellet design range | Ø12 nominal, 13 worst case | CONTEXT.md ASSUMPTION carried |
| Sump exit hole / S-tube / chute ID | **20** | **[D]** ≥1.6× worst-case D (Elscint irregular-ball rule, survey §B) = 20.8 → 20 chosen; re-check after caliper campaign |
| S-tube queue length | ~110 along path (5–7 pellets) | **[J]** short queue: fewer bodies at risk in the tube |
| S-tube bend radii | ≥ 40 centreline | **[J]** ≥2×ID to prevent cocked barrels wedging in bends |
| Nest interior radius | **6.5** (cup, radius-matched) | **[V]** patent pattern; sized to worst case, compliant liner takes up nominal |
| Flapper | spring steel 0.25 thick × 12 wide, ~18 free length; pass-through preload 0.2–0.4 kgf, set-screw adjustable | **[A]** tuning range — must be set empirically against real pellets; crush margin ≈ 20–35× below 7.5 kgf |
| Pusher stroke | 16 | **[J]** nest depth + flapper travel + 3 clearance |
| Through-beam station | 30 below flapper, optics recessed 8 behind Ø3 apertures | survey §0.1 baseline |
| Hopper internal | ~150 × 110 × 65 box, floor 30° to Ø40 sump well | §2 |
| Overall envelope below clip plate | ~150 × 115 wide, **~195 tall** | **[D]** hopper+lid 85 + tube/nest/cam section 85 + chute exit 25 |

**[A] Height risk flagged:** bottom payload plane is at Z ≈ −171 **[V]**;
ground clearance under a ~195 mm-tall payload at rest on landing gear is
**not yet derived** — it must be measured from the landing-gear STEPs
(`/tmp/pq-main/src/quiver/airframe_structure/landing_gear/`) before this
layout is frozen. If clearance fails, the S-tube can be re-routed sideways
(the S becomes a C) to trade height for width; the hopper cannot get much
shorter without losing capacity.

---

## 2. Hopper — 250+ pellets, anti-bridging

- **Volume: ~0.65 L usable.** **[D]** From CONTEXT/drone-spreaders §1.4:
  barrel-shaped worst case ≈ 1.94–2.26 cm³/pellet loose → 0.65 L holds
  **287–335 barrel-case pellets**; sphere case 1.41–1.65 cm³ → **394–460**.
  Conservative declared capacity: **≥ 285 pellets** (margin over the 250 hard
  minimum); best case ~460. Report actual after the caliper campaign.
- **Anti-bridging is active, not geometric.** The 6–8×D orifice rule demands
  a 72–96 mm outlet for free flow **[D, survey §0.1]** — impossible at a
  20 mm throat. So, per the PSD pattern **[V]**, a rotating agitator sweeps
  *directly over the exit hole* — attacking bridging at its source rather
  than hoping wall slope prevents it. This is exactly why the hopper can be a
  squat 65 mm-deep box with a modest 30° floor instead of an un-packageable
  86 mm-tall 60° cone **[D]**: the agitator substitutes for steepness.
- Agitator: 3 flexible TPU fingers (shore ~85A), swept radius ~35, tips
  passing 2–3 above the exit hole, ~45 rpm, torque-limited **[J]**. Compliant
  fingers deflect around a jammed/swollen body instead of grinding it
  (US11286119 explicitly damns vibratory agitation: bearing wear, IMU
  pollution **[V]** — we do not add a vibration motor).
- Lid: gasketed, quarter-turn latches. The pellet **swells 2–3× irreversibly
  when wetted** **[V, US4172714-class]** — moisture sealing is a jam-rate
  feature, not a nicety. Interior surfaces ≥ 30° slope or vertical; no
  horizontal ledges where fines can pack.
- Free agitation bonus **[J]**: rotor-induced airframe vibration mildly
  fluidises the hopper for free; the flip side (attrition → fines) is
  accounted in §7.

---

## 3. Mounting to the 50×50 clip plate

- The payload bolts to the COTS payload-side clip plate (BOM 2112
  "Replaceable Base", 50×50×10.5 alu) **[V]**; the blind-mate pads PCB
  (23.5×15.8, 4× M2) aligns with the drone-side spring pins **[V]**.
- Structure: a printed (ASA, 40 %+ infill) or 2 mm-alu **spine plate** bolts
  under the clip plate on a 4-bolt M4 pattern; hopper and mechanism housing
  hang from the spine. The hopper (the mass) sits centred on the port axis so
  the loaded CG stays within ~10 of the clip-plate centre **[J]** — the
  quick-release carries moment poorly in the unlatched direction
  (ASSUMPTION: per-port structural limits are not yet specified in the ICD
  **[V]**; keep CG offset minimal and verify against the flying aircraft).
- **[D]** Loaded moment sanity: ~1.2 kg at CG ~100 below the plate ≈ 1.2 N·m
  static; a 3 g manoeuvre triples it. Well within what a 50×50 bolted alu
  plate takes; the open question is the clip mechanism's rating, flagged
  above.
- Full pellet path (S-tube cover, nest, chute) faces one side of the spine
  behind a single hinged cover — see glove-serviceability mitigation, §7.

---

## 4. Count-verification sensing (sensed, not assumed)

Three independent observations per pellet; the count reported to the aircraft
uses the first two, the third is bookkeeping:

1. **Flapper deflection (primary, dust-immune).** The pellet physically bends
   the flapper to exit; a magnet on the flapper root + hall sensor turns each
   pass-through into a discrete mechanical event **[J]**. Dust cannot fake
   it, and a fines puff cannot trigger it — it takes ~0.2–0.4 kgf of real
   body to open the flapper. Debounced and *validated against cam phase*: a
   flapper event only counts if it occurs during the pusher's discharge arc
   (rejects queue-rattle chatter under vibration).
2. **Modulated through-beam IR at the drop chute (confirm-after-release).**
   Opposed-mode for maximum excess gain in dust **[V]**; optics recessed 8 mm
   behind Ø3 apertures; **dark-time gating** — a 12 mm body at chute speed
   occludes 6–12 ms **[D, survey §0.1]**; shorter = fragment (logged, not
   counted), longer = hang (fault). **Beam-clear self-test before every
   dispense**; a caked beam is a reported fault, never a miscount.
3. **Cam index switch** — commanded-cycle count and stall/timeout detection.
   Necessary, not sufficient (an empty nest still cycles the cam).

Count rule **[J]**: `verified = flapper AND beam agree`; disagreement →
retry logic (§6 contract) and a fault flag. An empty-nest cycle (cam turned,
no flapper event, no beam event) is a **skip** — a non-event, retried
automatically. Load-cell audit: end-of-sortie only, per survey (1.18 g is
unresolvable in flight **[V/D]**).

---

## 5. Electrical & power vs the 2 A / 25 W limits

Rail split (deliberate, per ICD §3 **[V]**):

- **12V_PL (~25 W guidance)** → buck (SD-25B-05 class) → logic 5 V/3.3 V:
  controller MCU, CAN transceiver, sensors. Draw < 1.5 W **[A]**. Must
  tolerate cycling: safe-stop cam + NV count storage (§1.3).
- **12VSW (K1 relay, 2 A fuse, ~24 W)** → both motors, through the
  controller's drivers with current sensing. The FC can hard-kill all moving
  parts (FMU_CH2) without killing the brain — a runaway mechanism and a hung
  controller have independent kill paths **[J]**.

| Load | Typical | Limit (enforced) |
|---|---|---|
| Crank gearmotor (25D class) | 0.3–0.6 A while cycling **[A]** | 1.2 A current limit (≈ pusher < 3 kgf) |
| Agitator N20 | 0.1–0.2 A **[A]** | 0.4 A current limit |
| Logic (via 12V_PL) | ~0.1 A eq. | — |
| **Worst simultaneous on 12VSW** | ~0.8 A (≈ 10 W) | **1.6 A < 2 A fuse** |

Soft-start PWM ramps on both motors so stall-recovery reversals never see the
2 A fuse **[J]**. Duty cycle is tiny: motors run only during a dispense
window (~3–10 s per target); thermal load is negligible (§7 heat).

### 5.1 Command contract (ICD scope only — no software phase)

DroneCAN on CAN2 **[V, ICD §4]**:
- `dispense(N, command_id)` with N ∈ 1..10.
- Behaviour: cycle until `verified == N`, max N+3 cam cycles, then stop.
- Reply: `dispensed(command_id, n_verified, fault_flags)` where fault bits =
  {jam_sump, jam_tube, jam_nest, beam_blocked, sensor_disagree, low_hopper,
  unsafe_stop_recovered}.
- Fallback trigger: FMU_CH1 PWM pulse-count = N for a CAN-less bring-up mode
  **[J]**; feedback still requires CAN.

---

## 6. Jam state machine

Halo Z-Code pattern, mandatory per survey §0.1: on cam stall or cycle timeout
→ reverse crank ~30° → re-advance → retry ×3 → declare fault, stop in safe
window, report `dispensed(n_so_far, fault)`. Agitator has its own
stall→reverse→retry. Manual override: crank end carries an external knurled
thumb-wheel (Rip Drive pattern) so a gloved operator can hand-cycle the
mechanism with the payload powered off **[J]**.

---

## 7. Failure modes — honest assessment

| Failure | Likelihood **[A]** | Effect | Mitigation | Honest residual |
|---|---|---|---|---|
| **Bridging over sump exit** | High if passive; low with agitator | No feed; skips | Agitator sweeping the exit hole itself **[V pattern]**; skip detected as empty-nest cycle → retry | Agitator motor is a single point of failure for feeding; its failure = mission over (report + RTB). |
| **Fragment/half-pellet wedged in S-tube** | Medium over a season | **Hard jam, no bypass** — gravity can't be reversed | 20 ID (1.6× worst case); ≥40 bend radii; fines-relief slots at both tube low points; **full-length hinged tube cover** for tailgate clearing; pusher reverse only clears the nest end | **This is the concept's worst weakness.** A mid-tube wedge cannot be cleared in flight, only detected (nest never refills → timeout fault). The USFS jam list (seam flash, out-of-round, clumping, brittle aged bodies **[V]**) maps 1:1 onto our pellet — and ours is *more* friable than an injection-molded sphere. |
| **Swollen pellet (wetted, 2–3× vol)** | Low if lid sealed; certain if rained into | Plugs sump exit | Cannot enter Ø20 hole (correct rejection); compliant fingers deflect around it; timeout fault; gasketed lid is the real defence | No in-flight clearance. Operator opens lid and picks it out. |
| **Dust/fines** | Certain (bentonite/urea pellet, label admits dust **[V]**) | False counts; caked optics; packed fines | Primary count is *mechanical* (flapper-hall — dust-immune); beam is dark-time-gated + self-tested; relief slots; no horizontal ledges | Fines will still accumulate; cleaning is a between-sortie chore. Beam self-test converts "silent miscount" into "reported fault" — that is the honest best achievable. |
| **Flapper mis-tune / pellet variance** | Medium until pellets are measured | Too stiff → skips/chipped pellets; too soft → doubles under vibration | Set-screw preload; cam-phase validation of counts; doubles *are* detected (two beam events in one cycle → over-count flagged, next command compensates) **[J]** | A barrel-shaped pellet seats in the sphere-matched nest in ≥2 orientations with different pass-through force. Tuning may chase pellet-lot variance. Must caliper 20+ pellets before freezing nest/flapper geometry (survey open unknown #1). |
| **Vibration** | Constant | Queue rattle → flapper chatter; attrition → fines | Cam-phase gating on hall counts; TPU nest liner; short queue | Attrition rate is unmeasured (open unknown #2) — fines budget is a guess until the tumble test is done. |
| **Heat (West Texas cab/sun)** | Seasonal certainty | Printed-part creep; sticky pellets | ASA/PETG (no PLA); white/reflective hopper; motors near-zero duty | **[A]** PEG-bearing pellet behaviour at 60 °C+ (softening/stickiness) is unverified — a soak test is required; if pellets get tacky, every candidate suffers, but a queue+flapper suffers more than an open disc. |
| **12V_PL / 12VSW power cycling** | By design (FC may cycle rails **[V]**) | Mid-cycle stop | Safe-stop cam window + completion-on-repower + NV count + dual-sensor observation of the in-flight pellet (§1.3) | Strongest story of any champion; residual is a single pellet released during a dying-power revolution, which is still observed by beam+hall and reported. |

---

## 8. Mass estimate

**[A]** — component-class estimates, PETG/ASA prints at 2–2.5 mm wall:

| Item | g |
|---|---|
| Clip plate, payload side (COTS alu, 50×50×10.5, pocketed) | 55 |
| Spine plate + housing frame | 80 |
| Hopper + gasketed lid (~0.65 L, printed) | 180 |
| Sump agitator (fingers, shaft, bushing) + N20 motor | 25 |
| S-tube + hinged cover + nest block + TPU liner | 95 |
| Flapper (spring steel) + preload hardware + hall | 10 |
| Cam/crank/pusher + bearings + thumb-wheel | 70 |
| Crank gearmotor (25D class) + mount | 110 |
| Electronics: MCU board, buck, CAN, drivers, current sense | 40 |
| Sensors: through-beam pair, cam switch, wiring | 20 |
| Blind-mate pads PCB + harness | 25 |
| Chute + sensor shrouds + fasteners | 40 |
| **Empty total** | **750** |
| Contingency 15 % (printed-part reality, TBD brackets) | 110 |
| **Empty, with margin** | **~860** |
| + 250 pellets (250 × 1.18 g **[V]**) | 295 |
| **Loaded, 250-pellet baseline** | **~1.16 kg** ✓ ≤ 1.5 kg |
| + full hopper best case (~460 pellets, 543 g) | **~1.40 kg** (still ≤ 1.5) |

Justification of the ~160 g above 1.0 kg (per CONTEXT mass rule): ~110 g is
the second motor + cam/crank assembly relative to a single-actuator concept —
that is the price of the safe-stop cam and the flight-proven release
primitive; ~50 g is the gasketed lid + hinged tube cover, bought directly
against the swelling-jam and glove-serviceability failure modes. IGNIS
comparison **[D]**: 1.25 kg empty *with* injection hardware → 0.86 kg empty
with it deleted and a smaller pellet is consistent, not optimistic.

---

## 9. Why this might lose (frank)

1. **Its pedigree is for a different projectile.** The flight-proven claim
   rests on injection-molded plastic spheres: round, hard, dimensionally
   controlled. Our pellet is a friable, dusty, moisture-swelling molded
   barrel with ±1 mm tolerance. Every geometry-tuned element here — nest
   radius, flapper preload, tube ID — inherits that mismatch, and the USFS
   jam literature says even the *good* spheres jam PSDs constantly in the
   field **[V]**. "Flight-proven architecture" is honestly only
   "flight-proven for a friendlier article."
2. **It is the heaviest and most-parts champion.** Two motors, a cam, a
   crank, a formed spring, a shaped tube — versus Champion A's one disc, one
   motor, one brush. If A's pocket wheel passes the pellet-variance test, it
   does the same job with ~150–200 g less and half the tuned parts.
3. **The S-tube is a jam trap with no bypass.** A wedged fragment mid-tube is
   undetectable until the nest starves, unclearable in flight, and the
   worst-in-survey glove-serviceability item even with the hinged cover.
   Champion A has no equivalent single-file confinement at all.
4. **Two empirically tuned parts (flapper, nest) against an unmeasured
   pellet.** Until the caliper/friability campaign (survey open unknowns
   1–3) runs, flapper preload is a guess with a failure mode on both sides
   (skips vs doubles). Concepts whose "exactly one" lives in rigid pocket
   geometry don't have a tuning knob to get wrong.
5. **Its killer feature may not be decisive.** The safe-stop cam is the best
   power-cycle answer — but a detented stepper or worm-driven pocket wheel
   (Champion A) is *also* non-backdrivable and stops in a defined index. If
   judges score power-cycle robustness as "adequate everywhere," this
   concept paid two motors and 150 g for a differentiator that didn't
   discriminate.
6. **Rate capability is wasted.** The cam architecture's 120/min heritage is
   irrelevant at 1–3 pellets per target with a hover between targets. We
   carry crank-and-cam complexity sized for a duty cycle we will never use.

**When it wins anyway [J]:** if the pellet-measurement campaign shows shape
variance bad enough that rigid pockets double-load or shear (killing A and
C), the compliant flapper + oversized tube is the architecture that degrades
gracefully instead of binding — and it is the only concept with field hours
behind its exact bulk-feed (agitated sump) and its exact power-loss story.

---

## 10. Open items this concept needs before CAD freeze

1. Ground-clearance derivation from landing-gear STEPs vs the ~195 mm stack
   (§1.5) — layout-blocking.
2. Caliper/weigh 20+ pellets, both axes → freeze nest radius, tube ID,
   flapper range (survey unknown #1).
3. Flapper-preload bench rig with real pellets, including a pre-swollen and
   a fragmented article (survey unknowns #3–4).
4. Tumble-test fines rate → sizes relief slots and cleaning interval
   (survey unknown #2).
5. Clip-plate structural rating for a ~1.2–1.4 kg cantilevered payload
   (ICD §6 gap **[V]**).
6. Brush Pod teardown ($650) — if the vendor's own applicator uses a queue
   architecture, that is direct evidence for (or against) this concept on
   this exact pellet.
