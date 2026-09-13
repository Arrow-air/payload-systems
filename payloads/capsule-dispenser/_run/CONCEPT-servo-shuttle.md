# CONCEPT — "servo-shuttle": servo-driven single-cavity reciprocating shuttle

Concept development, 2026-08-06. Champion C from `MECHANISM-SURVEY.md`
(drone-spreaders §M2, pill-counting §5 side-shuttle escapement, Elscint
irregular-ball singulation). Honest-advocate document: strengths argued hard,
weaknesses stated plainly. Labels: **[V]** verified/cited via the research docs,
**[D]** derived (derivation shown), **[A]** ASSUMPTION with reasoning.
No CAD yet — dimensioned sketch level.

---

## 1. Concept in one paragraph

One printed slide with one pellet-sized blind cavity reciprocates ~40 mm
between two stations: **FILL** (cavity open upward under the agitated hopper
throat) and **DROP** (cavity open downward over a 20 mm drop chute). The slide
is sandwiched between a fixed top plate (hopper floor, with the throat
aperture) and a fixed bottom plate (with the exit port) — the classic
industrial escapement-and-nest as a linear slide **[V, RNA
Automation/roymech]**. One stroke = at most one pellet, by geometry. A
standard-size hobby servo drives the slide through a spring-centered compliant
link so a caught friable pellet (crush ≈ 7.5 kgf **[V, US4172714 class]**)
deflects the drive instead of being sheared. A modulated through-beam IR pair
across the drop chute verifies each pellet with dark-time gating. This is the
simplicity floor of the trade space — one slide, one servo, one agitator
motor, one microswitch, one beam — and it doubles as the bench mule that can
be printed and dropping real pellets within a day.

---

## 2. Mechanism layout (dimensioned)

### 2.1 Metering stack (side view, section through stroke axis)

```
              hopper (agitated sump)
        \                         /
         \    agitator fingers   /
          \       ~ ~ ~         /
           +---[Ø16 throat]----+
  =========|====o====|============  TOP PLATE t=4 (hopper floor;
           | FILL    |              throat aperture Ø16, 3mm 45° chamfer)
   +-------+---------+----------+
   |      (o) cavity Ø14.5x13.5 |   SLIDE t=16 (blind cup, open top at FILL;
   +-------+---------+----------+     floor of cup is 2.5mm of slide material)
  =========|=========|==o=======|=  BOTTOM PLATE t=4
           |         | DROP     |     exit port Ø16 at DROP station
           |         +--v-------+
           |         | chute    |   drop chute Ø20 ID, 60 long
           |         |IR ->|<-IR|   through-beam 40 below bottom plate
           |         +--------- +
           |<-- 40 stroke ----->|
```

All dimensions mm. Cavity axis vertical; slide travel horizontal.

### 2.2 Key dimensions and why

| Feature | Value (mm) | Rationale |
|---|---|---|
| `PELLET_D` nominal / worst case | 12 / 13 | CONTEXT; ±1 mm ASSUMPTION flagged there. All metering dims parametric on this. |
| Cavity diameter | 14.5 | 13 worst-case + 1.5 clearance so seam flash / mold parting line can't bind **[A]** |
| Cavity depth (blind cup) | 13.5 | > 1 pellet, < 2× the ~9–11 mm barrel height **[D from drone-spreaders §1.4]**: a second pellet cannot fully enter; the top-plate underside wipes it off during the stroke. **Open risk:** a 9 mm-tall barrel on its side under a second barrel is the double-feed case to test — same caveat as Champion A. |
| Slide thickness | 16 | 13.5 cavity + 2.5 floor |
| Stroke (fill center → drop center) | 40 | ≥ 2.5× cavity dia so the cavity is fully closed (both plates) for ≥ 11 mm of mid-stroke travel; no open path hopper→chute at any slide position **[D]** |
| Slide plan size | 30 wide × 90 long | cavity + full overlap of both apertures at both ends |
| Throat aperture (top plate) | Ø16 | 13 worst case + flow clearance; deliberately far below the 72–96 mm anti-bridging orifice rule → **active agitation is mandatory, not optional** **[V, survey §0.1]** |
| Lip chamfers (throat edge, cavity rim, exit port) | 3 × 45° | convert the shear line into a cam that pushes a half-seated pellet up/back instead of cutting it **[A, gumball jam art]** |
| Fines relief | 1.0 wide slots along both slide guide rails + 0.5 plate-to-slide running clearance | attrition fines fall to the chute or out the slots instead of packing the sliding fit **[A — the least testable clearance in the design; see §9]** |
| Drop chute ID | 20 | ≥1.6×D oversize-tube rule proven on 6–16 mm irregular cast balls **[V, Elscint via pill-counting §5]** |
| Guide | dovetail ways printed into the plates, PTFE-loaded filament or stick-on PTFE tape on the ways | low friction without grease — grease is a dust magnet **[A]** |

### 2.3 Cycle (one pellet)

1. Rest state = FILL: cavity under throat, exit port blanked by slide body.
2. Agitator sweeps sump 0.3 s; pellet seats in cavity (gravity + agitation).
3. Servo strokes to DROP (~0.25 s). Top plate wipes off any rider; cavity
   passes fully closed mid-stroke.
4. Cavity opens over exit port; pellet falls through chute; beam reports one
   valid dark-time pulse.
5. Servo returns to FILL. Repeat N times. If the beam saw nothing by
   end-of-stroke +150 ms → empty-cavity skip → re-agitate and re-stroke
   (a non-event, costs ~1 s).

Cycle time ≈ 0.8–1.0 s/pellet **[A]** → N=3 in ~3 s, N=10 in ~10 s of hover.

---

## 3. Actuator choice and drive train

- **Shuttle drive: standard-size metal-gear digital hobby servo** (DS3218/
  DS3225 25 kg·cm class, ~60 g, 6.0–6.8 V) on a ~20 mm horn radius driving
  the slide via a short link. ~120° of horn travel = 40 mm stroke **[D]**.
- **Servo, not solenoid** (survey verdict, drone-spreaders M2 **[V]**): a
  solenoid slams at full force with no position feedback and no graceful
  reverse. The servo gives commanded-position control, slow-stroke option for
  jam-clearing, and reverse-and-retry.
- **Compliant coupling:** the link is a pushrod carrying two opposed
  compression springs in a cage (spring-centered). Preload set so the link
  transmits ≤ ~30 N before deflecting **[A, to be set on the bench]**. Context:
  25 kg·cm at a 20 mm arm could deliver ~12.5 kgf at the slide **[D]** — far
  over the ~7.5 kgf pellet crush load **[V, US4172714 class]** — so force
  limiting must live in the mechanism, not in trust of a current limit.
  30 N ≈ 3 kgf: 2.5× margin under crush, but it must also exceed worst-case
  dusty slide friction — this is the central tuning conflict of the concept
  (see §9).
- **Jam detection:** one microswitch at the DROP end of the ways (slide
  physically arrived) + commanded position + beam. Command issued, switch not
  made in 300 ms → the spring is deflected → jam: reverse at low speed,
  agitate, retry ×3, then fault (Halo Z-Code pattern, survey §0.1 **[V]**).
- **Agitator: N20-class 6 V gearmotor (~60 rpm, ~10 g)** spinning 2–3 soft
  TPU fingers that sweep the sump just above the throat — the PSD/paintball
  soft-paddle pattern **[V, survey §0.1]**. TPU fingers deflect at well below
  pellet crush load. Honest note: unlike the pocket wheel, the shuttle gets
  no agitation for free; this second actuator is part of the real parts count.

Rest state is mechanically safe: at FILL the exit port is blanked by the
slide body, and with the servo unpowered the spring-centered link plus end
detent hold the slide at FILL **[A]** — power loss at any moment strands at
most one pellet inside a closed cavity, releases none.

---

## 4. Hopper — capacity, geometry, anti-bridging

- **Geometry:** square-top wedge hopper, 110 × 110 top section 30 deep, then
  a frustum converging to a 20 × 20 sump over 80 of height. Wall angle
  ~61° from horizontal **[D:** run (110−20)/2 = 45 over rise 80 → atan(80/45)
  = 60.6°**]** — at the steep end of the ≥60° mass-flow guidance (survey M8).
  Interior faces printed smooth, seams filleted.
- **Capacity [D]:** volume = 110²×30 + (80/3)(121 + 4 + √(121·4)) cm²·mm
  = 363 + 3.94 L·… = 0.363 L + 0.392 L ≈ **0.76 L gross, ~0.70 L usable**.
  At the conservative barrel-pellet estimate (1.24 cm³ solid, 0.55 packing →
  2.25 cm³/pellet loose **[D, drone-spreaders §1.4]**): **~310 pellets**; at
  the 12 mm-sphere estimate (1.56 cm³/pellet loose): **~450 pellets**.
  **Report: ≥ 300-pellet capacity, 250 hard-minimum met with ≥20 % margin.**
  Load beyond 250 is at operator discretion; masses in §8.
- **Anti-bridging:** the Ø16 throat is ~1.3×D — deep inside the clogging
  regime by the 6–8×D orifice rule **[V, survey §0.1]**, so the agitator (§3)
  is load-bearing, runs during every fill dwell, and reverses with the jam
  state machine. Rotor-induced airframe vibration helps de-bridging for free
  (**[A]**, untested — pill-counting §6).
- **Sealing/moisture:** gasketed screw-on lid; a wetted pellet swells 2–3×
  irreversibly **[V, US4172714]** and cannot be re-dried into spec, so the
  hopper must keep condensation and rain out on the ground. Label also
  demands dry storage **[V]**.
- **Loading:** lid-off gravity pour through a coarse grate (17 mm openings)
  that catches swollen/clumped bodies at load time **[A]**, matching Thomas's
  "we filter broken ones before loading".
- **Low-pellet sensing:** none in the baseline (load cell rejected as
  in-flight counter, survey §0.1). Empty is detected honestly: repeated
  skip-retry cycles with beam silence → `hopper_empty` fault. **[A]**

---

## 5. Count-verification sensing point

Per the mandatory stack (survey §0.1, pill-counting §4, drone-spreaders M10):

- **Where:** across the Ø20 drop chute, **40 mm below the bottom plate** —
  after the last mechanical element, so what is counted is what actually left
  the aircraft. Nothing downstream of the beam can retain a pellet.
- **What:** modulated opposed-mode (through-beam) IR pair, emitter/receiver
  recessed ~8 mm behind 3 mm apertures at the ends of short tubes so dust
  cannot settle on the optics **[V, Banner opposed-mode-in-dust guidance]**.
- **Discrimination:** dark-time gating. A 12 mm pellet that has fallen 40 mm
  crosses the beam at ~0.9 m/s → ~10–14 ms occlusion **[D]**; window set
  ~5–25 ms. Shorter = fragment (count as fragment event, flag, do not count
  as a pellet); longer = hang/double → jam logic. 30–50 ms re-trigger
  dead-time rejects bounce **[V, pill-counting §4.1–4.2]**.
- **Self-test:** "beam clear?" check before every dispense; a caked beam
  reports `sensor_fault` instead of miscounting **[V, survey §0.1]**.
- **Fallback:** the chute is a straight 20 mm tube — the bench-tested
  capacitive/EFS ring (pill-counting §4.3) drops in around it with no
  mechanical change if optics foul in dust testing.
- **Audit:** end-of-sortie hopper weight check on the bench, not in flight
  (1.18 g unresolvable under rotor vibration **[V, survey §0.1]**).

Per-pellet record: commanded stroke + DROP microswitch + beam pulse. The
count reported over the interface is the **beam count**, nothing else.

---

## 6. Mounting and envelope

- **Interface:** payload-side clip half of the COTS quick-release pair (BOM
  2112, 50 × 50 mm, 10.5 mm thick **[V, mechanical README]**) bolted to the
  dispenser's aluminum-or-printed top plate; bolt pattern taken from
  `2112_attach_plate_payload_side.step`. Blind-mate pads-only Attachment
  Interface PCB (V1.4) mounted on the top plate, aligned to the silkscreen
  notch **[V, ICD §5]**. Tool-free install per ICD.
- **Port:** bottom (J31) — the only port with 12VSW; best drop geometry
  **[V, CONTEXT]**. Payload top mounting plane at Z ≈ −171 **[V]**.
- **Ground clearance [D, derivation recorded]:** from
  `/tmp/pq-main/src/quiver/airframe_structure/landing_gear/assembly.py`:
  horizontal-tube axis Z = −527.89, foam sleeve OD 40 → ground plane at rest
  ≈ Z −547.9. Budget below the payload plane: 547.9 − 171 = **377 mm**.
- **Stack height [D]:** clip+top plate ~18 + hopper 110 + meter stack 24 +
  chute 60 + beam housing ≈ **~215 mm** → **~160 mm ground clearance margin**
  at rest on gear. Comfortable.
- **Lateral:** ~140 mm max width, centered on the port. Landing-gear legs
  splay to X ≈ ±185 at Z −300 **[D from leg geometry]**; props are far above
  the belly plane. No interference **[A until STEP check against the full
  assembly — flagged for the CAD phase]**.
- **CG:** hopper is centered over the plate; the only off-axis masses are the
  servo (~60 g at ~45 mm offset) and chute. Static CG offset < 10 mm from
  port center at full load **[D, rough moments; verify in CAD]**.

---

## 7. Electrical, power vs the 2 A / ~25 W limits, interface contract

### 7.1 Architecture

- **12V_PL (≤~25 W guidance):** logic only — MCU (CAN-capable, e.g. STM32/
  RP2040-class + CAN transceiver), sensor amplifier, beam. < 1.5 W **[A]**.
  Tolerates rail cycling: verified-count events written to MCU flash/FRAM as
  they happen; after a mid-dispense power cycle the mechanism wakes at a safe
  state (§3) and reports what was verified before the cut.
- **12VSW (K1 relay, FMU_CH2, 2 A fuse = 24 W [V, ICD §3]):** actuators only,
  through a 6 V buck (no 5 V on the connector **[V]**; bring-your-own DC-DC
  per ICD §8). The FC can therefore kill actuator power independently of
  logic — a genuine safety/arming feature, and exactly what K1 was added for
  **[V, ICD: "originally the capsule dispenser motor"]**.

### 7.2 Power ledger **[A unless noted]**

| Load | Condition | @6 V | @12 V input (buck ~88 %) |
|---|---|---|---|
| Servo, normal stroke | 0.5–0.8 A | 3–5 W | 0.3–0.5 A |
| Servo, stall (buck current-limited 2.5 A) | worst case | 15 W | ~1.4 A |
| Agitator N20 | running / stalled in TPU fingers | 1–2 W | 0.1–0.2 A |
| Logic + beam (on 12V_PL) | continuous | — | ~0.1 A |
| **Worst coincident on 12VSW** | servo stall + agitator | ~17 W | **~1.6 A < 2 A fuse** |

Firmware interlock: agitator pauses during a stall-recovery stroke, so the
two worst cases never stack beyond the ledger. Buck soft-start keeps inrush
under the fuse rating. Margin is real but not lavish: ~20 % under the fuse at
the worst coincident case; the buck current limit is the enforcement, not
hope.

### 7.3 Command/feedback contract (ICD-level only; software out of scope [V])

- **Primary: DroneCAN on CAN2** (no bus termination added **[V, ICD §4]**).
  `dispense(N)`, N ∈ 1..10 → payload cycles until beam-verified count = N or
  fault → `dispensed(n_verified, n_fragment_events, fault_flags)`; 1 Hz
  heartbeat with state (idle/dispensing/jammed/hopper_empty/sensor_fault).
- **Arming:** 12VSW via FMU_CH2 = actuator enable. No actuator power, no
  pellet motion, regardless of CAN traffic.
- **Minimal fallback:** FMU_CH1 PWM pulse-count or width encodes N for
  bring-up without CAN **[A, bring-up convenience]**.

---

## 8. Mass estimate

| Item | g | Basis |
|---|---|---|
| Clip half, COTS quick-release (alu, 50×50×10.5) | 60 | [D] ≤71 g solid alu envelope; pocketed part est. — **weigh the real part** |
| Top plate + blind-mate PCB + fasteners | 45 | [A] |
| Hopper + grate + gasketed lid (PETG/ASA, 2 mm walls) | 170 | [D] ~0.11 m² shell × 2 mm × 1.27 g/cm³ ≈ 280 cm³·0.5 fill-factor printed |
| Metering plates + slide + ways | 85 | [A] printed, 16 mm slide |
| Servo (DS3225-class, metal gear) | 62 | [V-class datasheet value] |
| Link + spring cage + microswitch | 20 | [A] |
| Agitator N20 gearmotor + TPU fingers | 22 | [A] |
| Drop chute + beam housing + emitter/receiver | 35 | [A] |
| Electronics: MCU board, CAN xcvr, 6 V buck, wiring | 60 | [A] |
| Fasteners, seals, margin | 45 | [A] |
| **Empty total** | **~604** | ~40 % contingency already embedded in [A] lines |
| + 250 pellets (baseline load) | 295 | [V] 250 × 1.18 g |
| **Loaded, 250 pellets** | **~899** | |
| + full ~310-pellet barrel-case load | 366 | [D] |
| **Loaded, full hopper (~310)** | **~970** | |

**~0.90 kg at the 250-pellet baseline — well under the 1.5 kg ceiling with no
line needing justification** (ceiling applies at the 250-load per CONTEXT).
Lightest of the four champions, as scored in the survey (Mass 5).

---

## 9. Failure modes and honest mitigations

| Mode | Mechanism-specific reality | Mitigation | Honest residual |
|---|---|---|---|
| **Jam: pellet pinched at shear line** (half-seated at throat edge or exit lip mid-stroke) | This is the concept's worst geometry: a linear shear pair with a hard end-stop — survey scored it Jam 3, worst of the champions | 3 mm 45° chamfers; ≤30 N compliant link (≪ 7.5 kgf crush); microswitch detects non-arrival; reverse-slow, agitate, retry ×3, fault | Compliance is a patch, not a cure. A pellet can survive the pinch and still block the stroke; the recovery loop costs seconds and, if the pellet has wedged into the throat chamfer, may need the glove service the design is optimized for. |
| **Skip: empty cavity** | More likely than in a rotary meter — filling only happens during the dwell, and a barrel-shaped pellet may not seat in 0.3 s | Agitate during dwell; beam converts skip → re-stroke, a non-event | Leans harder on the sensor+retry loop than Champion A (survey Count 4 vs 5). At low hopper levels skip rate rises and dispense time stretches — measure skip rate vs fill level on the mule. |
| **Dust/fines** | Fines from a bentonite/urea pellet **[V, label: "until dust has settled"]** settle into the sliding fit — a slide is more dust-sensitive than a rotating disc | 0.5 mm running clearances, fines slots in the ways, no grease (PTFE surfaces), open bottom; recessed self-testing beam | The dusty-slide friction budget vs the 30 N spring limit is the concept's central unknown. If friction growth over a sortie approaches the spring limit, false "jams" appear. Bench data required (§10); if it fails, the spring limit rises and crush margin shrinks. |
| **Fragments** | A half-pellet can share the cavity with a full pellet → one stroke delivers 1 pellet + a fragment | Dark-time gating counts it as a fragment event, not a pellet; reported in feedback | **Detection, not prevention**: a fragment of herbicide lands off-count at the target. No champion prevents this; the shuttle at least reports it. Rangeland 378 pellet/acre/yr cap **[V]** makes fragment mass a real (small) compliance question for the operator. |
| **Swollen pellet (2–3× vol, irreversible [V])** | Cannot enter the Ø14.5 cavity (correct) but plugs the Ø16 throat above it | Load-time grate; TPU agitator sweeps the throat; reverse-agitate in jam loop | A fully swollen pellet mid-hopper is not clearable in flight — fault + tailgate fix. Genuinely the best concept for that fix: lid off, hand in, everything at the surface (survey Glove 5). |
| **Vibration** | Reciprocating ~30 g slide at ≤1 Hz is negligible vs rotors; airframe vibration actually aids de-bridging **[A]** | Debounce microswitch; beam is modulated (ambient/EMI immune); fasteners threadlocked | Servo gear chatter under sustained vibration is unquantified for hobby servos in this environment **[A]** — mule-on-shaker test. |
| **Heat (West Texas belly, direct sun)** | Hobby servo + printed slide at 50–60 °C surface temps | ASA or PETG-CF (no PLA); metal-gear coreless servo; duty cycle is tiny (seconds/hour); white/reflective shell | Hobby-class servo electronics are consumer-rated (~55 °C ambient max typ.) **[A]**; if soak tests fail, the upgrade is a sail-winch/robotics-grade servo at +30 g and +cost. |
| **12V_PL / 12VSW power cycling [V requirement]** | — | Rest state = FILL with exit blanked; spring-centered link + detent holds it unpowered; per-pellet count in NVM; no pellet can exit without a full powered stroke | A cycle mid-stroke can strand one pellet in a closed cavity — it is delivered as the first pellet of the next command and the NVM ledger keeps the count honest. |

---

## 10. Bench-mule plan (the concept's second job)

Printable and testing real pellets within a day **[survey [J]]**: slide +
plates + chute clamp to a bench frame; hobby servo + any MCU dev board; no
hopper needed for the first tests (hand-feed the throat). It retires, for
**every** champion: pellet both-axis dimension spread (survey unknown #1),
cavity-size vs skip/double rates (unknown #1), dusty-slide friction growth
(this concept's own #1 risk), beam dark-time distributions vs fragments
(unknown #7), crush/torque limits (unknown #3), and the soaked-pellet jam
article (unknown #4). Even if servo-shuttle loses the flight slot, this
hardware is the pocket-geometry test rig the survey says all concepts need.

---

## 11. Why this might lose (frank)

1. **It has the worst jam geometry of the four champions, in the failure
   domain that decides this product.** The survey's own scoring says it: Jam
   3, and the guillotine-with-end-stop pinch is exactly the wrong shape for a
   7.5 kgf friable pellet in dust. The compliant link converts crush into
   stall; it does not remove the stall. If the judging weights West Texas
   dust endurance above simplicity — and it probably should — Champion A wins
   this axis outright.
2. **The parts-count halo is partly an illusion.** The honest BOM is a servo
   *plus* an agitator motor *plus* the same sensing and firmware stack as
   everyone else. The rotary wheel gets agitation from its own shaft for
   free; the shuttle's headline "one moving part" is really three.
3. **Skip rate is a throughput and confidence tax.** Fill happens only in a
   short dwell instead of continuously; every skip costs ~1 s of hover and a
   retry. At N=10 with a low hopper on a windy day, dispense time could reach
   15–20 s **[A]** — hover time the accuracy requirement will not thank us
   for.
4. **The sliding fit is the single most dust-sensitive interface proposed by
   any champion**, and no research doc offers field data on a printed slide
   in hexazinone fines. The friction-vs-spring-limit conflict (§9) is a real
   tuning corner with no published anchor — it could eat the crush margin
   that justifies the compliant link in the first place.
5. **No flight-proven lineage.** Champion B descends from a fielded aerial
   dispenser (PSD/IGNIS); the closest flying shuttle relative is a 15-tablet
   mosquito-control unit with no count verification and no jam clearing
   **[V, US10499628]**. Choosing the shuttle means underwriting the pattern's
   first serious field deployment ourselves.
6. **If it loses, it should still be built** — as the §10 mule. Its cheapest
   virtue is that losing costs one day of printing and answers questions
   every other concept needs answered anyway.

---

## 12. Open items carried forward (do not invent)

- Caliper/weigh 20+ pellets both axes → freeze cavity Ø/depth (survey #1).
- Fines-vs-friction slide test, 20 min shaker with dusty pellets (own #1).
- Confirm 7.5 kgf crush on real capsules before setting the 30 N spring
  preload (survey #3).
- Soaked-pellet throat jam test (survey #4).
- Beam vs capacitive ring bench shoot-out with deliberate fines (survey #7).
- Weigh the real 2112 clip half; check lateral envelope STEP against the full
  PT3 assembly.
- Servo heat-soak at 60 °C, 500 cycles **[A threshold]**.
