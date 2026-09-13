# CONCEPT — "pocket-wheel": Rotary Pocketed Metering Wheel

Concept-development output, 2026-08-06. Advocate document for Champion A of
`MECHANISM-SURVEY.md`. Sources: `CONTEXT.md` (ground truth), `MECHANISM-SURVEY.md`
§0.1/§2A, `RESEARCH-seed-metering.md` (§3 §5 §9 §11), `RESEARCH-drone-spreaders.md`
(§1.3–1.4, M1), `RESEARCH-bulk-dispensers.md` (§1), `../../interface/ICD.md`
v1.0-draft, and the landing-gear source
`/tmp/pq-main/src/quiver/airframe_structure/landing_gear/assembly.py`.
Facts are traceable to those documents; engineering judgement is **[J]**;
unverified items **ASSUMPTION**; math shown is **[D]** (derivation).

Status: sketch-level, dimensioned in mm. No CAD yet. All pellet-facing
dimensions are parametric on `PELLET_D` (default 12, worst case 13 per
CONTEXT ASSUMPTION ±1 mm).

---

## 1. Concept in one paragraph

A stepper-indexed flat disc with 8 through-pockets rotates on a vertical axis
between the hopper sump (above) and a stationary retaining plate (below). Each
pocket holds exactly one pellet — geometry, not control, bounds output. A pocket
fills by gravity in an open fill arc where the disc top *is* the sump floor
(gumball-machine pattern, so there is no narrow throat to bridge); a compliant
Kinze-style brush wiper strips any second pellet back into the pool; the
retaining plate carries the pellet through the transfer arc; at the single exit
port the pellet falls through a short chute past a modulated through-beam IR
sensor with dark-time gating, which closes the count loop. Agitator fingers on
the same shaft stir the sump every index for free. The drive is torque-limited
an order of magnitude below the ~7.5 kgf pellet crush load and fully reversible
for jam clearing. The only intrinsic failure mode is a *skip* (empty pocket),
which the sensor converts into a harmless re-index.

---

## 2. Mechanism layout and key dimensions

### 2.1 Stack (top to bottom, below the drone belly)

```
Z=-171 mm  ═══ payload mounting plane (bottom of drone-side QR hardware) ═══
           ┌──────────────────────────────────────────┐
           │ 2112 payload-side clip plate, 50×50×10.5 │  (COTS aluminum)
           ├──────────────────────────────────────────┤
           │ chassis adapter plate, t=6               │  spreads 50×50 → hopper
           ├──────────────────────────────────────────┤
           │                                          │
           │   HOPPER  inner Ø140, cyl section h=55   │  lid on top w/ seal
           │   ╲  45° conical funnel Ø140→Ø95, h=22.5╱│
           │    ╲____________________________________╱│
           │      open fill arc over disc (~120°)     │  agitator fingers sweep here
           ├───┬──────────────────────────────────┬───┤
           │   │ POCKET DISC Ø90 × t=14, 8 pockets│   │  ← stepper shaft, vertical
           │   │ pockets Ø15 thru, on Ø60 PCD     │   │  brush wiper at fill-arc exit
           ├───┴───────────────┬──────┬───────────┴───┤
           │ retaining plate t=4, exit port Ø18 ──►│  │  fines slot 4 mm wide (arc)
           ├───────────────────┤chute ├───────────────┤
           │ NEMA-14 stepper   │ ID22 │ electronics   │  motor hangs below plate,
           │ (coaxial, below)  │ ▄▄▄▄ │ bay (side)    │  coaxial with disc
           └───────────────────┴──┼───┴───────────────┘
                    IR through-beam ┤ ← 40 mm below retaining plate
                                   ▼ pellet drops near airframe centerline
Z≈-331 mm  bottom of payload (stack ≈ 160 mm below mounting plane)
```

### 2.2 Metering disc (the counting element)

- Disc: Ø90 × 14 thick, printed PETG-CF (ASA-CF if heat testing demands),
  lightening pockets between cells.
- 8 through-pockets, **Ø15** (= `PELLET_D_MAX` 13 + 2 clearance), on a Ø60
  pitch circle. Pitch at PCD: π×60/8 = 23.6 mm → 8.6 mm web between pockets
  **[D]**. Index angle 45°/pellet.
- **Double-exclusion geometry [D]:** disc thickness 14 mm means a seated worst
  case 13 mm pellet sits ≥1 mm below the disc top surface (no shear on the
  seated pellet), while a second sphere stacked on it protrudes ≥11 mm above
  the surface and is wiped off by the brush. If the pellet is really a 12×~9 mm
  barrel (drone-spreaders §1.4 ASSUMPTION), two flat-stacked barrels = ~18 mm →
  4 mm protrusion — still wipeable but with far less margin. **Disc thickness is
  the parameter that must be re-frozen against caliper data on 20+ real pellets
  (survey open unknown #1).**
- Pocket top edge: 2 mm 45° chamfer (lead-in, anti-shear). Housing roof over
  the transfer arc: chamfered ramp entry, ≥1.5 mm clearance over the disc face.
- Disc-to-retaining-plate gap: 0.5 mm — dust falls through; nothing rubs.

### 2.3 Fill station, brush wiper, agitator

- Fill arc: ~120° of the pocket circle is open to the hopper sump; pellets rest
  directly on the disc top (the disc is the sump floor). This deliberately
  avoids any pellet-scale throat: the derived anti-bridging rule (6–8×D →
  72–96 mm orifice, seed-metering §11) says a small throat is in the clogging
  regime by design; the open-arc sump keeps the "orifice" at ~95 mm.
- Brush wiper at the fill-arc exit (Kinze brush-meter DNA, seed-metering §3):
  COTS nylon strip-brush segment, ~20 mm trim, mounted to wipe anything
  protruding >2 mm above the disc surface back into the pool. Compliant — it
  deflects rather than shearing a friable pellet. Tool-free replaceable
  (wear + dust-packing item, per Kinze Brush Meter 2.0 precedent).
- Agitator: 3 compliant TPU fingers on the disc shaft above the disc, sweeping
  the conical sump 10–15 mm above the disc face. They stir every index for
  free, and a firmware "agitation burst" (oscillate ±30°) attacks bridges on
  demand. This satisfies mandatory subsystem §0.1-1 without a second motor
  (the PSD uses a dedicated sump-agitator motor; here the meter shaft does
  double duty — see §10 for the honest downside).

### 2.4 Actuator

- **NEMA-14 stepper, direct drive** (no reduction), TMC2209-class driver,
  1/16 microstepping, sensorless stall detection (StallGuard) + Hall/magnet
  index homing (one magnet in the disc rim → absolute pocket phase after any
  power cycle).
- Why a stepper: position-indexed, reversible, silent-stall on obstruction,
  and **inherently force-limited [D]:** rated torque ~0.18 N·m at the Ø60 PCD
  (moment arm 30 mm) gives a max tangential force at the pocket lip of
  0.18/0.030 = **6 N ≈ 0.6 kgf — 12× below the ~7.5 kgf pellet crush load**
  (US4172714 class figure, drone-spreaders §1.3). A trapped pellet stalls the
  motor; it cannot be crushed into the fines we must not create. No torque
  limiter part needed — the motor *is* the torque limiter, enforced by driver
  current limit.
- Load check **[D]:** drag = pellet bed friction on the exposed disc arc
  (~2–3 N normal load from a ~400 g bed **[J]**, µ≈0.5 → ~0.04 N·m at 30 mm)
  + brush drag → well inside 0.18 N·m with >3× margin.
- Index profile: 45° in ~0.2 s, ~0.1 s settle+verify → ~3 pellets/s capability;
  requirement is ~1 Hz-class. N=3 with one skip ≈ 1.2 s **[D]**.

---

## 3. Hopper (capacity, anti-bridging)

- Geometry: inner Ø140 cylinder, 55 mm straight section, 45° conical funnel
  Ø140→Ø95 (h=22.5), terminating in the open fill arc over the disc. Printed
  PETG (2 mm wall), gasketed screw-on lid (moisture sealing — the swollen-pellet
  jam case is rain/condensation, drone-spreaders §1.3).
- Volume **[D]:** cylinder π×7²×5.5 = 846 cm³ + frustum π×2.25/3×(49+33.25+22.56)
  = 247 cm³ + sump ≈ 60 cm³ → ~1.15 L gross; **usable ≈ 0.85 L** after headspace
  and agitator swept volume.
- Capacity **[D]** (per drone-spreaders §1.4 packing numbers): barrel worst case
  2.28 mL/pellet → **~370 pellets**; sphere basis 1.64 mL/pellet → ~520.
  **Report: ≥350 pellets worst-case ≈ 1.4× the 250 hard minimum** (capacity
  above 250 is an explicit CONTEXT goal). 250-pellet baseline load fills the
  hopper ~2/3 — generous agitation headspace.
- Anti-bridging stack: (1) no pellet-scale orifice anywhere (open fill arc);
  (2) 45° funnel walls (teaching-material heuristic, seed-metering §11 —
  flagged there as unverified; here it is belt-and-braces on top of active
  agitation, not the primary defence); (3) active agitator fingers sweeping the
  sump every index + on-demand oscillation burst; (4) a swollen (2–3×) pellet
  cannot enter a Ø15 pocket — correct behaviour — and the agitator + reversible
  disc are the answer if it camps on the fill arc. No vibration motor
  (US11286119: wrong answer structurally; pollutes the IMU — survey §0.1).

---

## 4. Count-verification sensing (mandatory, §0.1-2)

- **Sensing point: the drop chute, 40 mm below the retaining plate**, i.e.
  after the pellet has irrevocably left the mechanism — this measures what
  actually left the aircraft, which is what "verified count" must mean.
- Baseline sensor: **modulated (38 kHz-class) opposed-mode IR through-beam**
  across the Ø22 chute, emitter/receiver recessed ≥5 mm in printed light
  tunnels (dust shadowing, no direct sun path), lens windows replaceable.
- **Dark-time gating [D]:** free fall from the port, v at beam =
  √(2·9.81·0.040) ≈ 0.89 m/s; a 12 mm pellet + ~3 mm effective beam width
  occludes ~17 ms. A 5 mm fragment reads ~9 ms; fines/dust puffs read shorter
  and non-square. Gate: accept ~10–35 ms as one pellet (count it); <10 ms =
  fragment (do NOT count toward N); >35 ms = hang/double → fault path. The
  2:1 pellet/fragment margin is real but not luxurious — thresholds must be
  frozen by the bench test against deliberately dusty/fragmented pellets
  (survey open unknown #7) **before** this geometry is trusted.
- Beam-clear self-test before every dispense (survey §0.1). If the beam reads
  blocked at rest → `fault: sensor_fouled`, no dispense.
- Fallback (named, not designed-in yet): capacitive/EFS ring around the chute
  — the poor-man's WaveVision (seed-metering §9); the industry abandoned
  pure optics in dust. Chute is dimensioned so a ring sensor can replace the
  optical block without touching the meter.
- Optional second observation **[J]**: a reflective IR pocket-occupancy sensor
  looking up through a small hole in the retaining plate one station before
  the exit port ("confirm-before-release"), enabling predictive skip handling
  (index straight through a known-empty pocket without waiting on the chute
  sensor). Deferred — adds a dust-facing optical surface; baseline works
  without it.
- Rejected in-flight verification: hopper load cell (1.18 g unresolvable under
  rotor vibration — seed-metering §9); retained only as pre-flight/post-sortie
  audit if a cell is ever fitted.

Dispense cycle (state machine, ICD-contract level only — no software phase):
`dispense(N)` → beam self-test → repeat {index 45°; expect one gated dark-time
event} until verified count = N → reply `dispensed(n_verified, fault_flags)`.
Skip: no event after an index → index again (free). >8 consecutive skips (one
full disc revolution with no pellet) → agitation burst → retry once → `fault:
empty_or_bridged`. Stall: reverse 15° → re-advance, 3 attempts → `fault: jam`
(Halo Z-Code pattern, survey §0.1-3). All faults leave the disc parked.

---

## 5. Mounting to the 50×50 clip plate; airframe integration

- The chassis adapter plate (6 mm, printed PETG-CF or machined 5052) bolts to
  the payload-side clip plate (`2112_attach_plate_payload_side.step`, 50×50
  ×10.5; bolt pattern to be taken off the STEP). Hopper walls carry down from
  the adapter plate; meter housing and motor hang from the hopper base ring;
  electronics bay on the side of the meter housing.
- The whole stack is coaxial with the plate center; the exit port sits at the
  30 mm pocket-circle radius and the chute angles the drop line back to ~the
  airframe centerline **[J]** — release point near CG minimizes lateral offset
  scatter for the 1 m CEP budget.
- CG: within ~5 mm of plate center by symmetry (motor mass coaxial); loaded
  mass ≈1.1 kg on the bottom port is well under even the informal >3 kg review
  threshold (ICD §6).
- **Ground clearance [D — derivation recorded per CONTEXT]:** from
  `landing_gear/assembly.py` (position constants from the PT3 master model):
  horizontal cross-tube axis Z = −527.89, foam sleeve OD 40 → ground contact
  plane Z = −527.89 − 20 = **−547.9 mm**. Payload mounting plane Z ≈ −171
  (ICD §6) → **376.9 mm available** below the mounting plane. This stack uses
  ~160 mm → **~217 mm ground clearance margin** at rest on the gear.
- Lateral: landing-gear legs sit at Y = ±123, splaying X 123→269 as they
  descend; closest leg-top approach to the payload axis ≈ √(123²+123²) =
  174 mm **[D]** vs hopper outer radius 72 mm → >100 mm clear. Prop disks are
  outboard of the side ports (X ±185) and far above/outside a Ø144 belly
  cylinder. ASSUMPTION (verify against full assembly when CAD exists): no prop
  or arm interference for this envelope.

---

## 6. Mass estimate (empty + loaded)

| Item | Mass (g) | Basis |
|---|---|---|
| Payload-side clip plate (COTS alu, 50×50×10.5) | 75 | [D] 26.3 cm³ solid alu = 71 g; machined features ±; ASSUMPTION pending weighing |
| Chassis adapter plate + standoffs | 60 | [J] printed CF-PETG 6 mm |
| Hopper Ø140 + funnel, 2 mm wall | 105 | [D] ~510 cm² wall area × 0.2 cm × 1.25 g/cm³ ≈ 128 g incl. lid; split lid out |
| Lid + gasket | 30 | [J] |
| Pocket disc Ø90×14, lightened | 60 | [D] 69 cm³ envelope − lightening, CF-PETG |
| Meter housing + retaining plate + chute | 65 | [J] |
| Brush wiper + holder | 10 | [J] COTS strip brush segment |
| Agitator fingers (TPU) + hub | 10 | [J] |
| NEMA-14 stepper | 120 | typical catalogue mass for 34 mm-stack NEMA-14 — ASSUMPTION, confirm part |
| Electronics: MCU+CAN board, TMC2209, 12→5 V buck, IR pair, Hall, wiring | 65 | [J] |
| Blind-mate PCB (pads side) + mount | 15 | ICD: 23.5×15.8 mm board + bracket [J] |
| Fasteners, misc | 35 | [J] |
| **Empty total** | **650** | |
| Contingency 15% (concept stage) | 100 | [J] |
| **Empty, carried** | **~750** | |
| + 250 pellets (baseline load) | 295 | CONTEXT verified 1.18 g × 250 |
| **Loaded @250** | **~1045** | **under the 1.5 kg ceiling with 455 g margin** |
| + full hopper ~370 pellets (worst-case packing) | 437 | [D] |
| **Loaded @370 (max)** | **~1187** | extra pellets don't count against ceiling (CONTEXT), and total stays sane |

Under 1.0 kg empty → no per-100 g justifications triggered. Heaviest single
item is the stepper; a NEMA-11 (~60 g) is the fallback if the ledger ever
tightens, at reduced torque margin.

---

## 7. Power draw vs the 2 A / ~24–25 W limits

Rails (ICD §3): 12VSW = K1 relay, **2 A fuse, ~24 W**, bottom port only,
FC-commanded — motor power. 12V_PL = shared SSR rail, ~25 W guidance — logic.
No 5 V provided → onboard buck. Split rationale: FC can hard-kill the
mechanism via 12VSW while count state, sensing and CAN reporting stay alive on
12V_PL; both tolerate cycling by design (§4 homing + §9 rest state).

| Load | Rail | Peak | Notes |
|---|---|---|---|
| Stepper via TMC2209, 0.7 A RMS/phase | 12VSW | ≤8 W (≈0.7 A @12 V) | [D] worst-case chopper input draw during index; typ. 3–4 W. ASSUMPTION: confirm on bench with chosen motor |
| Stepper hold (20% idle current) | 12VSW | ≤1 W | parked between commands |
| MCU + CAN + IR sensor + Hall (via 5 V buck, η≈0.85) | 12V_PL | ≤1.2 W | [J] |
| **Total peak (indexing)** | | **≤9.2 W, ≤0.8 A @12 V** | **2.5× under the 2 A fuse; 2.6× under 24 W** |

No inrush concern beyond buck soft-start (spec it). Duty cycle is tiny: the
meter runs ~1–2 s per target. Thermals: TMC at 0.7 A needs only a pad-size
heatsink; see §8 heat row.

---

## 8. Failure modes and honest mitigations

| Failure mode | What actually happens | Mitigation | Honest residual |
|---|---|---|---|
| **Jam — pellet wedged at pocket lip** (the gumball shear-line mode, bulk-dispensers §1) | Disc stalls against a half-seated pellet at the fill-arc exit | Brush wipes before the shear point; 2 mm chamfers; force at lip capped at ~6 N ≪ 73.5 N crush [D §2.4]; StallGuard → reverse 15° → retry ×3 → fault; reversible by design | A pellet can survive 3 retries wedged; sortie continues degraded or aborts on fault. Cannot rule out; can only make it non-destructive and reported |
| **Jam — swollen pellet** (2–3× volume, irreversible; worst case per drone-spreaders §1.3) | Cannot enter a pocket (correct); squats on the fill arc, starves filling | Sealed gasketed lid (prevention); agitator fingers + oscillation burst; skip-storm detection reports `empty_or_bridged` | A swollen pellet is not clearable in flight — it needs the tailgate. Detection is honest, removal is manual |
| **Dust film** (bentonite/urea fines + ranch dust; label itself warns of dust — drone-spreaders §1.3) | Optics attenuate → false "blocked" or missed counts; fines pack in corners | Recessed modulated optics + dark-time gating (rejects non-square/short events); beam-clear self-test each dispense fails loud, not silent; 0.5 mm under-disc gap + 4 mm fines slot passively sheds fines every index; replaceable windows | Optical sensing in this dust is the concept's biggest *bench-unproven* element. If the sensor test (open unknown #7) fails, we fit the capacitive ring fallback — cost/complexity grows |
| **Fragments** (5–12 mm, from in-hopper attrition) | Small ones exit via fines slot; mid-size ride pockets and drop; a fragment can share a pocket with a whole pellet | Dark-time gate excludes <10 ms events from the count (fragment ≠ pellet); slot geometry passes <4 mm | A pellet+fragment co-drop over-doses that target slightly, and a ~10–12 mm fragment is indistinguishable from a pellet — it will be counted. ASSUMPTION: agronomically tolerable; flag to Thomas |
| **Vibration** (multirotor + wind) | In-hopper attrition → more fines; pellet bounce at the beam → double-edge counts; bolt loosening | Meter is vibration-indifferent (positive displacement, no g-frame dependence — unlike vibratory feeders); debounce/refractory window after each counted event; thread-locker + nyloc standard | Attrition *rate* is unmeasured (open unknown #2). If fines per sortie are far above the assumed few-tenths-%, the dust row above worsens materially |
| **Heat** (West Texas ranch, payload in sun) | Printed parts creep (PETG Tg ~80 °C); driver derates; stepper heat soak | Duty cycle ~seconds per target → motor barely warms [D §7]; hold current 20%; ASA-CF for sun-facing shells if 60 °C+ soak testing demands; driver heatsunk to chassis plate | ASSUMPTION: no active cooling needed at these duty cycles — must be confirmed with a hot-soak bench run, not asserted |
| **12V_PL / 12VSW power cycling mid-command** (ICD requirement) | Motor loses power mid-index | Rest state is defined "web over exit port" (closed); a pellet can only leave via a commanded index; Hall+magnet absolute re-home on boot; chute sensor already counted anything that fell; no dispensing on boot without a fresh command | Stepper detent+friction holding the disc mid-index during the outage is assumed sufficient to prevent drift past the port — weaker than the PSD's cam-enforced safe stop (see §10) |

---

## 9. Interface contract (scope-limited per CONTEXT: no software phase)

- Power: 12VSW (motor, FC-killable master-arm), 12V_PL (logic), GND. Tolerates
  cycling of either (§8 last row).
- Command/feedback: **DroneCAN on CAN2** (no bus termination added, per ICD).
  `dispense(N)`, N ∈ 1..10 → `dispensed(n_verified, fault_flags)`;
  `status()` → {pellets_dispensed_total, last_fault, sensor_selftest}.
  FMU_CH1 PWM reserved as a dumb backup trigger (one pulse = dispense 1)
  **[J]**, optional.
- Declares ICD 1.0-draft.

---

## 10. Why this might lose (frank)

1. **The pellet may not be a sphere — and the whole guarantee is geometric.**
   The double-exclusion argument (§2.2) assumes the smallest pellet dimension
   is ~9 mm or more. If caliper data shows flatter barrels, lens shapes, or a
   wide mixed population, two pellets can co-seat with only ~2–4 mm of brush-
   wipeable protrusion, and the pocket wheel's headline claim — "doubles are
   geometrically impossible" — quietly degrades to "doubles are brush-
   improbable". Champion D's interstage airlock keeps its geometric guarantee
   under shape variance in a way this concept does not. This is the single
   most likely way pocket-wheel loses, and it is decided by a $20 caliper
   session, not by analysis.
2. **The fill interface is a rubbing interface on a friable pellet.** Every
   index drags the pellet bed across the disc face and the brush across the
   top pellet. Per-event forces are tiny, but over 250+ pellets × a sortie of
   vibration this is a fines *generator* sitting directly above the meter.
   The PSD's S-tube (Champion B) touches each pellet far less. If the
   attrition test (open unknown #2) comes back bad, this architecture is
   feeding its own worst enemy — dust — into its own sensor.
3. **Skip behaviour near empty is unproven.** The last ~15–20 pellets rattle
   on a mostly-bare disc arc; fill probability per pocket drops and N=3 may
   take many indexes, and "empty" vs "bridged" is only distinguishable by a
   skip-storm heuristic. If the requirement hardens toward guaranteed
   dispense-time per target or exact remaining-count telemetry, the buffered-
   column concepts (B/D) degrade more gracefully.
4. **Safe-state story is firmware, not mechanism.** The PSD's cam switch
   physically cannot stop in an unsafe phase; our equivalent is a detent-held
   stepper plus a Hall re-home plus a parking convention. That is three
   soft(er) things standing in for one hard thing, against an explicit ICD
   requirement (tolerate 12V_PL cycling). A reviewer who weights power-cycle
   robustness heavily should prefer B here — advocacy requires admitting that.
5. **Sensor risk is shared, not solved.** Pocket-wheel's scores lean on "the
   sensor turns skips into non-events". True — but every champion gets the
   same sensor, so if dust defeats dark-time-gated optics and forces the
   capacitive ring on everyone, pocket-wheel's relative advantage narrows to
   the mechanism alone, and C (shuttle) is simpler and lighter while D is
   more exactly-counting.
6. **It is not actually the lightest or simplest.** The mass ledger (§6) says
   ~750 g empty carried vs C's plausibly ~550–600 g **[J]**. Pocket-wheel wins
   on all-around scores, not on any single axis; a judging that maximizes one
   axis (min mass, min parts, max power-cycle safety, max shape tolerance)
   picks someone else.

## 11. Assumption register (things that must be measured before detail design)

1. Pellet axis dimensions, 20+ samples (decides disc thickness 14 mm, pocket
   Ø15, and whether claim §2.2 survives) — survey open unknown #1.
2. Fines/attrition rate under tumble test — sizes the dust load (§8 rows 3–5).
3. Actual crush load vs the 7.5 kgf class figure — confirms §2.4 margin.
4. Sensor bench test, dusty/fragmented pellets, freeze dark-time thresholds.
5. Clip-plate bolt pattern + true mass from the 2112 STEP/physical part.
6. Stepper part selection + measured indexing power on the bench (§7 numbers
   are conservative envelopes, not measurements).
7. Prop/arm clearance check against the full assembly once CAD exists (§5).
