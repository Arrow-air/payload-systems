# Brush Bullet Dispenser — Electronics Design

**Targets ICD version 1.0-draft** (`../../../interface/ICD.md`), bottom port **J31**.
Mechanism: pocket-wheel, r6 CAD (`../cad/dispenser.py`, `../_run/BUILD-NOTES-r6.md`).

**Scope (per CONTEXT.md, Thomas 2026-08-06):** *"NO software phase … design the
electrical/command interface contract only (what signal triggers a dispense of
N, what feedback comes back)."* This document therefore specifies **hardware and
the interface contract**. It contains no firmware design, no state-machine
implementation, no register maps beyond what the contract requires. Where a
behaviour is unavoidably firmware (thresholds, motion profiles), it is stated as
a **requirement on the hardware** ("the hardware shall make X measurable") plus a
**contract clause**, never as code.

**Notation.** `[V]` verified against a cited source · `[D]` derived, arithmetic
shown · `[J]` engineering judgement · **ASSUMPTION** unverified, must be closed.
Facts from `_run/CONTEXT.md`, `interface/ICD.md`, `_run/BUILD-NOTES-r6.md` and
`cad/dispenser.py` are cited inline. Nothing here is invented; where a number
could not be sourced it is labelled and given a closure path.

---

## 0. Summary of decisions

| # | Decision | Why (one line) |
|---|---|---|
| 1 | **Motor on 12VSW; all logic + all sensing on 12V_PL** | K1/FMU_CH2 becomes a true galvanic disconnect of the only actuator that can release herbicide, while the payload stays alive to report count and faults with the motive rail dead |
| 2 | **Geared stepper + current-chopping driver** (14HS13-0804S-PG5 + TMC2209) | A chopper is a *constant-current* load: worst-case 12VSW draw **0.30 A**, and it does **not rise at stall** (§2.4). A brushed alternative stalls at 4 A and blows the aircraft's 2 A F1 |
| 3 | **Driver current limits set from mechanics, not from the motor rating** — **CS = 18** metering, **CS = 31 (full scale)** recovery | Makes the driver the torque limiter: 0.39 N·m metering, 0.66 N·m recovery = 20.5 N at the pocket lip, held at exactly 2× under the 41 N pellet-crush figure. With R_SENSE = 0.50 Ω the recovery setting **is** full scale, so the ceiling is a resistor (§2.3, decision 10) |
| 4 | **Two parallel chord beams** across the exit chute at x = axis ± 3.0 mm, 940 nm, modulated, analog receivers | The r6/concept single centred pencil beam has a **5.2–14.7 ms** dark-time spread (§4.2) — the concept's "10–35 ms = one pellet" gate would reject a real pellet hugging the chute wall. Two chords guarantee **10.4–14.7 ms** for any pellet at any lateral position |
| 5 | **Hall phase sensing is the primary stall/lost-step detector**, StallGuard secondary | With a chopper, input current *falls* at stall — current sensing is a poor stall detector. The 9 magnets + 2 Halls already in the r6 CAD give a 2-bit static safe-state decode (§3.2) |
| 6 | **DroneCAN on CAN2 is the command interface; FMU_CH1 PWM is arm + degraded backup only** | PWM is FC→payload only. There is no return path on CH1, so **PWM alone cannot satisfy CONTEXT's "count must be VERIFIED (sensed)"** (§5.1) |
| 7 | **Transaction-scoped, resumable, idempotent dispense semantics** with the count in FRAM | ICD §3 requires tolerating power removal at any time. A re-sent `Dispense(seq,N)` after a mid-command power cycle must complete the *remainder*, never re-dose the plant (§5.3) |
| 8 | **Ethernet not used**; blind-mate pins 1/3/5/7 left unconnected | No data-rate need; saves a PHY, magnetics, ~1 W and 4 of the 9 conductors that must fit the 5 × 2.5 mm top-plate cable channel (§6.3) |
| 9 | **Default-safe at the pin level: 100 kΩ pull-DOWN on motor-eFuse EN, 100 kΩ pull-UP on TMC2209 ENN, external watchdog** | Both pins are pure high-impedance inputs with **no internal pull** [V TPS2595 datasheet §7.5 `IEN` = ±0.1 µA leakage only; V TMC2209 datasheet Rev 1.05 pin table — ENN is type `DI`, not `DI (pd)`]. Without external pulls the motor rail and the output stage are undefined for the whole interval between rail rise and GPIO configuration, and after every MCU reset. §2.7 gives the guaranteed state of every interlock element for every power/reset event |
| 10 | **R_SENSE = 0.50 Ω makes the torque ceiling a resistor, not a register** | The TMC2209's `IHOLD_IRUN` **reset default is IRUN = 31 = full scale** [V datasheet §5.2] and is volatile across every VM cycle. Sizing R_SENSE so that full scale *is* the 0.63 A recovery current (20.5 N, 2.0× under the 41 N crush figure) makes the "pellet grinder" state physically unreachable by any firmware or UART fault (§2.3) |
| 11 | **Both IR emitters run continuously whenever 12V_PL is present** | `UNCOMMANDED_DROP` (fault bit 9) is the top hazard; gating the emitters to the 400 ms dispense window made it undetectable for 99.9 % of the sortie. Continuous monitoring costs **0.07 W** on a 25 W-guidance rail (§2.4) |
| 12 | **PWM_ARM is mandatory in the flight configuration**, and the armed band moves to **1750–1850 µs** | 1500 µs is the near-universal FC trim/default for an unassigned channel; a 1400–1600 µs armed band let the payload arm itself as a side effect of an FC boot or parameter reset. DroneCAN gives integrity but **no authorisation** — CAN2 is shared with two other ports and the companion computer (§5.1, §5.5) |

**Worst-case power: 12VSW 0.30 A / 3.6 W (2 A fuse, 6.7× margin) · 12V_PL 0.040 A /
0.48 W (25 W guidance, 52× margin) · payload total 4.05 W, 0.34 A, GND return 0.34 A.
Steady state, motor parked and count sensor monitoring: 0.40 W / 0.033 A.**
**Electronics BOM (excluding motor) $92.68; with motor $129.45** (§8).

**§11 is a Residual Risks register.** Three findings from the safety review are
accepted-with-mitigation rather than closed, and are listed there with the
argument for acceptance and the test that would close them.

---

## 1. Architecture

```
                 ┌──── payload-side Attachment Interface PCB (pads only, ICD §5) ────┐
   AIRCRAFT      │  pad2 12VSW   pad6 12V_PL   pad4 GND   pad8 CH1   pad9/10 CAN2    │
   (blind-mate)  └──────┬────────────┬──────────┬───────────┬──────────┬─────────────┘
                        │            │          │           │          │  Molex J1 (12p)
                 ┌──────┴────────────┴──────────┴───────────┴──────────┴────┐
                 │        HARNESS  9 × 26 AWG, 300 mm, top-plate channel     │
                 └──────┬────────────┬──────────┬───────────┬──────────┬────┘
   ELECTRONICS BAY  ┌───┴────┐  ┌────┴────┐     │      ┌────┴───┐  ┌───┴────┐
   (50×26×42,       │ eFuse  │  │  eFuse  │     │      │ 1k+1nF │  │ CM     │
    y = −75)        │ 0.60 A │  │ 0.50 A  │     │      │ +3V3TVS│  │ choke  │
                    │ EN ────┼──┼──────┐  │     │      └────┬───┘  │ +TCAN  │
                    │  │     │  │ EN ← UVLO div │           │      │  1042  │
                    │ 100k   │  │ ILM ─┐  │     │           │      └───┬────┘
                    │  ▼GND  │  └───┬──┼──┘     │           │          │
                    │ ILM ───┼──► ADC  └► ADC   │           │          │
                    └───┬────┘  ┌──┴──────┴─┐   │           │          │
                   VM 12 V      │TSR 1-2450 │   │           │          │
                    ┌───┴────┐  │  5 V 1 A  │───┴─► 5 V     │          │
                    │TMC2209 │  └─────┬─────┘                │         │
                    │ ENN ◄──┼─ 100k ─► VCC_IO  (DEFAULT-SAFE, §2.8)   │
                    │ VREF ◄─┼─ 10k/10k from 5VOUT  (current ceiling)  │
                    │ R_SENSE 0.50 Ω  → 0.63 A peak MAX, §2.3          │
                    │ STEP/DIR/UART  │ AP2112K → 3V3        │          │
                    └───┬────┘       └──────────┬───────────┴──────────┘
                        │                ┌──────┴───────────────────┐
                        │                │ STM32G431KBT6 + FRAM     │
                        │                │ (count + faults + boot)  │
                        │                │  ◄── TPS3823 ext. WDT    │
                        │                └──┬───────────┬───────────┘
                   4-wire motor (PH)        │ 3× Hall   │ 2× LED drive + 2× TIA
                        │  + NTC            │ + NTC     │ (GH-6 ×2, ESD arrays)
              ┌─────────┴───────┐   ┌───────┴─────┐   ┌─┴──────────────────┐
              │ NEMA 14 + 5.18:1│   │ DRV5023 ×3  │   │ emitter bd (2 LED) │
              │  planetary      │   │ retaining   │   │ receiver bd (2 PD  │
              │  (coaxial disc) │   │ plate 42.5R │   │  + TIA), chute     │
              └─────────────────┘   └─────────────┘   └────────────────────┘
```

**Read the two eFuse EN circuits as different on purpose.** The motor eFuse EN is
a **GPIO against a 100 kΩ pull-down** — off unless the MCU is alive and asserting.
The logic eFuse EN is a conventional **IN-referenced UVLO divider** — on whenever
the aircraft supplies the rail. §2.2 and §2.8 explain why.

Three small PCBs: **main board** in the electronics bay, **emitter board** and
**receiver board** in the two chute sensor bosses. Everything else is COTS.

---

## 2. Power

### 2.1 Rail allocation and rationale

ICD §3 gives us, at the bottom port only: **12VSW** (mechanical relay **K1**,
FC channel **FMU_CH2**, **2 A fuse F1**, ~24 W max — *"originally the
brush-bullet dispenser motor"*) and **12V_PL** (SSR **U5**, FC channel
**FMU_CH4**, shared across all three ports, ~25 W per-port guidance). No 5 V, no
3.3 V, no UART. [V ICD §3]

| Load | Rail | Rationale |
|---|---|---|
| Stepper driver power stage (VM) | **12VSW** | K1 is a *mechanical* contact. When the FC opens it, the actuator is galvanically disconnected — the dispenser physically cannot turn, whatever the payload firmware believes. This is the strongest safety statement available for a herbicide release mechanism and it is exactly what the relay was added for |
| MCU, CAN node, FRAM, driver VCC_IO/logic, Hall sensors, **the whole count sensor** | **12V_PL** | (a) Count integrity survives the motor rail being cut: a pellet already in flight when K1 opens is still counted and reported. (b) The payload can run its pre-dispense sensor self-test *before* asking for motive power. (c) `MOTOR_RAIL_ABSENT` is reported as a distinct fault instead of the payload going dark — a payload that vanishes tells the operator nothing. (d) FMU_CH4 keeps its documented job (hard power-cycle a hung payload); if the logic could be fed from 12VSW that reset would not work |

**Explicitly rejected: ORing the two rails.** Diode-ORing 12VSW into the logic
rail would defeat the FMU_CH4 power-cycle. A build-time solder link **LK1**
selects the motor eFuse input as 12VSW (default) *or* 12V_PL (never both) for
bench use or a hypothetical side-port variant; fitting LK1 to 12V_PL forfeits the
hardware kill and must be marked on the unit.

### 2.2 Protection and sequencing chain (per rail)

`blind-mate pad → 26 AWG → TVS (SMAJ13A) → eFuse (TPS2595AARJER) → bulk C → load`

- **eFuse, not a fuse or PPTC.** One part gives programmable current limit,
  programmable output slew (inrush), UVLO, thermal shutdown, an **EN pin** and a
  **current-monitor output (ILM)**. A PPTC was evaluated and rejected: a 1.1 A-hold
  device derates to ~0.82 A hold at 60 °C ambient and trips in *seconds*, so it
  neither protects the aircraft fuse nor coordinates predictably in a
  West-Texas-sun payload. [J]
- **Part-number correction (defect in the earlier draft of this document).**
  The BOM previously carried "TPS2595AARJER", which is not a TPS2595 orderable
  part number. The TPS2595 is an 8-pin WSON (DSG) part and the orderable list is
  `TPS2595x0/x1/x3/x5 DSGR/DSGT` [V TI SLVSE57C orderable addendum]. **Specify
  `TPS259540DSGR`** — 13.7 V typ OV clamp, **latch-off** on thermal shutdown,
  active-high EN [V device comparison table]. Latch-off is chosen deliberately
  over the auto-retry `…41` variant: an auto-retrying eFuse on the motor rail
  would hide a real fault behind a thermal-cycling loop, and clearing the latch
  is then an explicit MCU action (drop EN, re-assert) that is visible in
  telemetry. The 13.7 V clamp sits above the 12 V rail and below the SMAJ13A's
  clamping region, so the two do not fight.

**Current limits — tightened, and bounded by what the part can actually do.**
The earlier draft set 1.2 A / 0.6 A against worst-case loads of 0.298 A / 0.039 A,
i.e. 4× and 15× oversized. In that window a partially chafed motor lead, a damaged
driver FET, or wet herbicide dust tracking across the board could dissipate up to
14.4 W indefinitely inside a plastic bay whose thermal model assumes 1.2 W —
and nothing else in the chain would trip, because the aircraft's 2 A F1 never
sees it and 12V_PL is shared across all three ports through one SSR [V ICD §3].

`I_LIMIT = 2000/R_ILM + 0.04` (A, Ω) [D from the datasheet's tabulated points:
487 Ω → 4.17 A, 1780 Ω → 1.17 A, 4420 Ω → 0.49 A; accuracy ±6 %]:

| Branch | Worst-case load | **R_ILM** | **I_LIMIT** | Margin | Note |
|---|---|---|---|---|---|
| 12VSW (motor) | 0.298 A | **3.57 kΩ** | **0.60 A** (0.56–0.64) | 1.9× over load, 3.3× under F1 | if the 1.0 A motor data set (§2.3, issue 1) is confirmed, move to 2.94 kΩ → 0.72 A |
| 12V_PL (logic) | 0.039 A | **4.42 kΩ** | **0.50 A** (0.46–0.52) | 12.8× | **this is the part's floor** — see below |

**Honest limit: the TPS2595 cannot be programmed to the ~0.15–0.2 A that the
12V_PL load would justify.** The datasheet's headline current range is
**0.5 A to 4 A** [V SLVSE57C §1 Features]; Figure 13 extends to ≈0.21 A at
R_ILM = 10 kΩ but that is outside the specified range and outside the ±6 %
accuracy characterisation. Rather than run a safety-relevant limiter out of
spec, or add a second part number for one rail, the intermediate-fault regime is
covered in a different way:

- **The ILM pin is an analog current monitor and shall be read by the MCU.**
  `I_ILM = 276 µA/A × I_OUT` [V SLVSE57C §7.5 `GIMON`, 249–304 µA/A], developed
  across the same R_ILM that programs the limit. At the 12V_PL branch's 0.039 A
  worst case, V_ILM = 0.039 × 276 µA/A × 4420 Ω = **48 mV**; full scale 0.61 V.
  On the 12VSW branch, 0.298 A → **294 mV**, full scale 0.59 V. Both go straight
  into MCU ADC channels with no amplifier.
- **This replaces the 0.05 Ω shunt** the earlier draft specified for the motor
  rail (§3.3). A 0.05 Ω shunt at 0.3 A produces 15 mV and needs a current-sense
  amplifier; ILM produces 294 mV and needs a wire. One fewer part, better
  resolution, and it is the *same* measurement the limiter acts on.
- **Firmware overcurrent thresholds are a contract item, not a suggestion:**
  12VSW > **0.45 A** for >20 ms → `OVERCURRENT` (bit 13), drop EN, latch.
  12V_PL > **0.12 A** for >100 ms → `OVERCURRENT`, latch and report (the payload
  cannot cut its own logic rail; it reports and refuses to arm).
  These are 1.5× and 3.1× over the respective worst-case loads.
- **Single-point-failure behaviour of R_ILM is defined by the part:** R_ILM open
  → 0 A limit (device off — fail-safe); R_ILM shorted to GND → 3 A circuit
  breaker [V SLVSE57C §7.5, IEC 62368-1 single-point test]. Both are acceptable
  on the motor rail; the open case is the one that matters and it fails safe.

**Sequencing and the default-safe state of the motor rail.** The motor eFuse
**EN is driven by the MCU**, which lives on 12V_PL, so VM can never reach the
TMC2209 before its VCC_IO exists whatever order the aircraft brings the rails up
in. This is a two-key arm: *the FC closes K1* **and** *the payload asserts EN*.
But an MCU-driven pin is only a key if it has a defined state when the MCU is not
driving it, and it does not by default:

- **`IEN` on the TPS2595 EN/UVLO pin is specified only as ±0.1 µA leakage
  [V SLVSE57C §7.5] — there is no internal pull-up and no internal pull-down.**
  A floating EN is genuinely undefined, and the datasheet's own typical
  application (§9.2.2.2) programs UVLO with a **resistor divider from IN**, which
  *enables the device whenever VIN is present*. That circuit must not be used on
  the motor rail.
- **Mandatory: 100 kΩ from motor-eFuse EN to payload GND**, driven high by an MCU
  GPIO. UVLO rising threshold is 1.2 V (falling 1.1 V) and EN abs-max is 6 V
  [V SLVSE57C §7.3/§7.5], so a 3.3 V push-pull GPIO drives it unambiguously and
  the 100 kΩ pull-down holds it at <1 mV against 0.1 µA of leakage. Consequence:
  **every state in which the MCU is not actively running — POR, brownout,
  watchdog reset, SWD halt, unpopulated firmware — leaves the motor rail off.**
- The **12V_PL (logic) eFuse keeps the conventional IN-referenced UVLO divider**,
  because that rail *should* come up whenever the aircraft provides it. The two
  eFuses therefore have deliberately different EN circuits and this must be
  called out on the schematic.
- **External watchdog + supervisor (`TPS3823-33DBVR`, SOT-23-5, ~$0.75).** The
  STM32G431's IWDG is on-die and shares the die's failure modes; an external part
  gives a defined POR, a brownout threshold below the LDO's dropout, and a
  ~1.6 s watchdog that pulls NRST. Because NRST tri-states every GPIO, the WDT's
  reset action *is* the motor-off action via the EN pull-down and the ENN pull-up
  (§3.1) — no additional gating logic is needed. IWDG is also enabled; the two
  are independent.
- (TMC2209 VCC_IO/VS power-up ordering is a datasheet item — ASSUMPTION that
  VIO-before-VM is the safe order; the sequencing above makes the question moot
  either way.)

- **Rail presence sensing — two dividers, not one.** The earlier draft put a
  single 100 k/10 k divider on *post*-eFuse 12VSW and called the resulting fault
  `MOTOR_RAIL_ABSENT — 12VSW not present (K1 open, or F1 blown)`. That
  measurement cannot distinguish K1 open, F1 blown, the payload's own eFuse being
  held off by its own EN, an eFuse thermal latch-off, or an eFuse failure — which
  is exactly the diagnostic §2.1 claims as a headline benefit of the split rail,
  and it is the aircraft-side cause the operator can act on. **Fit both**:
  a 100 k/10 k divider *pre*-eFuse (aircraft rail present) and a second
  *post*-eFuse (my own eFuse conducting), two ADC channels, four resistors.
  Fault bit 5 splits into `MOTOR_RAIL_ABSENT` (pre-eFuse low) and
  `MOTOR_EFUSE_OFF` (bit 12: pre-eFuse high, post-eFuse low). The post-eFuse
  divider doubles as a **readback of the safety-critical EN interlock**, which is
  worth having as telemetry in its own right.
- **Hot-plug.** ICD §1 makes payloads hot-swappable, so the blind-mate can mate
  live. The eFuse slew control bounds inrush (§2.5) and the CAN transceiver is
  specified with power-off high-impedance bus pins so mating cannot disturb CAN2
  for other nodes.
- **Bulk capacitance:** 100 µF 35 V aluminium-polymer hybrid per rail
  (Panasonic EEH-ZA1V101P class, 125 °C) + 4.7 µF X7R + 100 nF. Polymer/hybrid
  rather than wet electrolytic for life at the bay's internal temperature (§2.6).

### 2.3 Actuator current settings — derived from the mechanism, not the motor

Motor data (14HS13-0804S-PG5): 1.8° bipolar, **0.18 N·m holding, 0.8 A/phase,
6.8 Ω, 10 mH**, planetary **5.18:1 at 90 %**, backlash ≤1°, max permissible
output 2 N·m, 290 g [V oyostepper product page]. **Data conflict, must be closed
at order time:** StepperOnline's own PG5 page lists 14 N·cm / 1.0 A / 3.2 Ω /
4.5 mH / backlash ≤3° for the same part number, and the r6 BOM carries those
figures. The r6 buildability critic reached the same conclusion from the vendor
PDF. **All numbers below use the 0.18 N·m / 0.8 A / 6.8 Ω / 10 mH set**;
if the 1.0 A set is correct the currents scale but the architecture does not.

Available output torque at 100 % phase current [D]:
`0.18 × 5.18 × 0.90 = 0.839 N·m` → at the Ø64 pocket circle (r = 32 mm),
`0.839 / 0.032 = 26.2 N` at the pocket lip.

That is **more** authority than r6 assumed (0.65 N·m / 20.4 N) and it is now
close enough to the 41 N whole-pellet crush figure (US4172714 class, r6 §2.2 —
itself an ASSUMPTION) that the driver must limit it deliberately:

**The torque ceiling is set by the sense resistor, because IRUN is not a hardware
limit.** The earlier draft stated that "the IRUN ceiling (78 %) is a
hardware-configured safety limit". It is not: `IHOLD_IRUN` (0x10) is a
write-only register reached over the same single-wire UART as everything else, it
is volatile across every VM cycle, and **its reset default is `IRUN = 31`, i.e.
full scale** [V TMC2209 datasheet Rev 1.05 §5.2: "IRUN (Reset default=31)"]. So
a UART glitch, a firmware fault, or simply a VM dip that resets the driver
restores full-scale current — 26.2 N at the pocket lip, only 1.6× under the 41 N
crush figure, i.e. the drive becomes a pellet grinder and manufactures exactly
the fines the count sensor and the anti-jam geometry are fighting.

The fix costs nothing. The TMC2209's RMS current is

`I_RMS = (CS+1)/32 · V_FS/(R_SENSE + 20 mΩ) · 1/√2`, V_FS = 325 mV at the
`vsense = 0` default [V datasheet §9, "Default is 325 mV"].

Choose **R_SENSE = 0.50 Ω 1 %** — which is a tabulated standard value in the
datasheet's own sense-resistor table (0.50 Ω → 0.44 A RMS max) [V §9 "Choice of
RSENSE"]. Then `CS = 31` (the reset default) gives **0.625 A peak / 0.442 A RMS**
— *exactly the recovery current*, and the whole grinder regime is physically
unreachable:

| Mode | Requirement it satisfies | Output torque | Force at pocket lip | **IRUN (CS)** | I_rms | I_peak/phase |
|---|---|---|---|---|---|---|
| Park / idle | none (detent holds phase) | 0 | 0 | **ENN high, VM off** | 0 | 0 |
| Metering index | ≥2× the r6 measured 190.7 mN·m load budget | 0.39 N·m | 12.2 N | **18** | 0.262 A | 0.371 A |
| Jam recovery | max shear authority while staying **2.0× under** the 41 N crush load | 0.66 N·m | 20.5 N | **31 (= full scale)** | 0.442 A | 0.625 A |
| *Register-default / fault state* | — | *0.66 N·m* | *20.5 N* | *31* | *0.442 A* | *0.625 A* |

**The ceiling holds under every register state [D].** The only two registers that
can scale current upward are `CHOPCONF.vsense` and `GCONF.i_scale_analog`:
`vsense = 1` selects the *lower* 180 mV full scale, and `i_scale_analog = 1`
(the reset default) scales V_FS by `VREF/2.5 V`, capped at unity. So V_FS can
only ever be ≤325 mV **provided VREF cannot exceed 2.5 V** — therefore
**VREF is tied to a 10 k/10 k divider from the TMC2209's own 5VOUT pin**, giving
2.50 V with no possible excursion above it. With that one divider fitted,
**0.442 A RMS / 0.625 A peak is a physical bound enforced by two resistors, valid for all four
combinations of `{vsense}` × `{i_scale_analog}` and for any register content.**

- IRUN = 18 sits inside the datasheet's recommended 16–31 window for best
  microstep performance [V §5.2 hint], so nothing is given up.
- Sense-resistor dissipation: `0.442² × 0.5 = 98 mW` per phase — 0805 0.25 W,
  1 %, low-TCR (≤100 ppm/K) so the ceiling does not drift with bay temperature.
- **Contract requirement (§5.3 clause 11): the MCU shall read back
  `IHOLD_IRUN`, `GCONF` and `CHOPCONF` over the UART before every dispense and
  refuse the transaction (`REFUSED_FAULT`, bit 14 `DRIVER_CONFIG`) if they differ
  from the commanded values.** This is a detection layer on top of the physical
  bound, not a substitute for it.
- CONTEXT hard requirement 2 is still satisfied at the new ceiling: 20.5 N vs
  BUILD-NOTES-r6's 9.2 N worst-case wedged-sliver shear force = **2.2×**, and
  2.0× under the 41 N whole-pellet crush figure.
- **Zero hold current between dispenses.** The r6 detent (spherical R8 × 0.4
  seat, 2.5 N light plunger, 96.5 mN·m release torque) plus 5.18:1 gearbox
  friction holds the park position with the motor de-energised. This (a) removes
  the standby power, (b) removes a static magnetic dipole under the airframe,
  (c) makes the power-cycle rest state a *mechanical* property rather than a
  firmware one — partially answering concept §10.4's honest weakness.

### 2.4 Worked power budget, stall case, and fuse coordination

**Stepper losses** (sine microstepping, both phases, `P = 2·(I_pk/√2)²·R`, and
driver `R_DS(on)` LS+HS ≈ 0.5 Ω hot) [D]:

| Mode | I_pk | I_rms | Copper | Driver | Mech (0.19 N·m @180 °/s ÷0.9) | Input | 12VSW current |
|---|---|---|---|---|---|---|---|
| Metering index | 0.37 A | 0.26 A | 0.94 W | 0.07 W | 0.67 W | 1.73 W | **0.144 A** |
| Recovery, moving | 0.63 A | 0.44 A | 2.66 W | 0.20 W | 0.67 W | 3.57 W | **0.298 A** |
| Recovery, **stalled** | 0.63 A | 0.44 A | 2.66 W | 0.20 W | 0 | 2.91 W | **0.242 A** |
| Parked | 0 | 0 | 0 | 0 | 0 | ~0.05 W | ~0.004 A |

**The stall case is the whole argument for a stepper on this rail [D]:** with a
current-chopping driver the phase current is regulated to IRUN regardless of
rotor position, and at stall the mechanical term goes to zero, so **input current
*falls* by ~19 % at stall** (0.298 → 0.242 A). There is no stall surge to fuse
against. For contrast, a 12 V brushed gearmotor of comparable output with a 3 Ω
armature stalls at 12/3 = **4 A** — twice the aircraft's F1 rating, so a single
wedged fragment would open a fuse *inside the aircraft* and end the sortie.

**Fuse coordination [D]:**

| Element | Trip | Time to trip at a hard short |
|---|---|---|
| 12VSW firmware threshold on ILM (§2.2) | **0.45 A**, 20 ms | covers the *intermediate* fault regime the limiter is blind to |
| Payload 12VSW eFuse | 0.60 A ±6 % → 0.64 A max | fast-trip, <1 ms (TPS2595) |
| 12V_PL firmware threshold on ILM | **0.12 A**, 100 ms | report + refuse to arm |
| Payload 12V_PL eFuse | 0.50 A ±6 % → 0.52 A max | <1 ms |
| **Aircraft F1 (12VSW)** | **2 A** | a 2 A fuse does not open below ~1.35× rating; ≫100 ms at 2 A |

Selectivity margin: worst-case payload steady draw 0.30 A → **1.9×** below the
payload limiter → 6.7× below F1. Any payload-side short (chafed motor lead,
driver failure, water) is cleared by the payload's own limiter and the aircraft
fuse never sees it. **The payload never needs the aircraft's fuse to do its
job** — which matters because F1 is not field-replaceable in flight.

**The regime between the load and the limiter is covered by firmware on ILM, not
by the limiter.** A 0.60 A limit on a 0.30 A load still permits 7.2 W of
sustained fault dissipation inside the bay; the 0.45 A/20 ms firmware trip cuts
that to 5.4 W for 20 ms. On 12V_PL, where the part's 0.50 A floor is 12.8× the
load, the 0.12 A firmware threshold is the *only* thing standing between a
tracking fault and 6 W in the bay — and because the payload cannot cut its own
logic rail, its action is to latch `OVERCURRENT`, refuse to arm, and report, so
the operator (or the FC, via the FMU_CH4 SSR) can drop the rail. This is stated
plainly because it is a real asymmetry: **the motor rail can protect itself; the
logic rail can only tell you.**

**12V_PL (logic + sensing) budget [D]:**

| Load | Power |
|---|---|
| STM32G431 @64 MHz, 3V3 | 0.07 W |
| TCAN1042, 30 % dominant duty | 0.05 W |
| 3 × DRV5023 continuous-time Hall (ECO-8) | 0.03 W |
| Analog front end (2× TIA, refs) — **always on** | 0.10 W |
| IR emitters, **dispense window**: 2 × 100 mA at 50 % carrier duty | 0.14 W |
| IR emitters, **monitor mode (the other 99.9 % of the sortie)**: 2 × 50 mA at 50 % | 0.07 W |
| External watchdog/supervisor, NTC divider | <0.01 W |
| Status LEDs | 0.03 W |
| **5 V/3V3 subtotal, dispensing** | **0.42 W** |
| At 88 % buck efficiency → from 12V_PL | **0.48 W = 0.040 A** |
| **5 V/3V3 subtotal, monitoring (steady state)** | **0.35 W → 0.40 W = 0.033 A** |
| Commanded `LOW_POWER` (emitters and AFE off; ground handling only) | 0.19 W = 0.016 A |

**Why the emitters now run continuously.** The earlier draft budgeted them
"only during a dispense window" of ~400 ms per pellet. That made fault bit 9
`UNCOMMANDED_DROP` — *the single worst outcome this payload has, and the outcome
the entire interlock argument exists to prevent* — **unreachable by
construction**: a pellet shaken out in cruise by vibration, or trickling from a
port left partly open by a mid-move power loss (§3.2), would produce no event, no
telemetry and no record, because the emitters were dark. §3.2 also promises that
a `PHASE_LOST` recovery drop is reported "with the count sensor armed
throughout", which the gated budget contradicted.

**Contract requirement: both emitters and both TIAs shall be powered whenever
12V_PL is present and the payload is not in commanded `LOW_POWER`.** The cost is
**0.07 W** — 0.017 A on a rail with 25 W/port of guidance and a 0.48 W measured
payload draw. Monitor mode runs the emitters at 50 mA rather than 100 mA, which
still yields 91 µA of photocurrent, i.e. **91× excess gain** (§4.4) — ample to
detect a whole pellet, and the drive steps to 100 mA for the dispense window
where the dark-time measurement must be accurate. Standby draw is therefore
*lower* than the earlier draft's dispensing figure. A drop while 12V_PL itself is
absent remains undetectable; that is stated in §11.

**Worst-case totals:** 12VSW 3.57 W / 0.298 A · 12V_PL 0.48 W / 0.040 A ·
**payload 4.05 W, 0.338 A, all of it returning through the single blind-mate GND
pin (pin 4).** Against the ICD's 25 W/port guidance the payload uses 1.8 %.
**Steady-state (monitoring, not dispensing): 0.40 W / 0.033 A total**, because
12VSW draws ~0 with the motor parked.

**Single-GND-pin analysis [D].** Pin 4 is the only ground. At 0.34 A and an
assumed 100 mΩ spring-pin contact resistance the payload ground floats 34 mV
above aircraft ground — irrelevant for CAN (differential, ±12 V common-mode
range) and for a 3.3 V-logic PWM input. The real hazard is **loss** of that pin:
if GND opens while 12V_PL is live, return current would try to flow out through
the FMU_CH1 input's ESD structure and into the flight controller. Mitigation
(mandatory): the CH1 input is a **1 kΩ series resistor + 3.3 V TVS clamp to
payload GND**, limiting any such fault to ≈12 mA — below the FMU pin's tolerance
and non-destructive. A payload must never be able to damage the FMU.

### 2.5 Inrush [D]

`I_inrush = C · dV/dt`, set by the eFuse's slew-control capacitor:

| Bulk C | 2 ms ramp | 5 ms ramp | 10 ms ramp |
|---|---|---|---|
| 100 µF | 0.60 A | 0.24 A | 0.12 A |
| 220 µF | 1.32 A | 0.53 A | 0.26 A |

**Specified: 100 µF per rail, 5 ms ramp → 0.24 A inrush**, 5× under the eFuse
limit and 8× under F1. This matters more for **K1 contact life** than for the
fuse: a mechanical relay closing into an uncontrolled capacitive load draws tens
of amps for tens of microseconds during contact bounce, which is what welds small
relays. With slew control, K1 closes into a 0.24 A ramp. Un-slewed inrush I²t
into 100 µF through ~0.1 Ω would be ≈0.07 A²s [D] — survivable by the fuse but
not kind to the relay, and it is free to avoid.

### 2.6 Thermal — bay, with all four heat terms [D]

The earlier draft computed ΔT = 17 K from internal dissipation and natural
convection only, noted in passing that the part "also sees ground-reflected sun",
and never put a number on it. Two terms were missing — **solar gain, which is
larger than the internal load, and radiation, which is the dominant heat-rejection
path**. They partially cancel, so the old 67 °C answer was roughly right *by
luck*; neither the sign nor the size of the error was bounded. Redone with all
four terms:

Bay external 50 × 26 × 42 mm → total surface **A = 0.0090 m²**; largest
sun-facing projected area **A_sun = 50 × 42 = 0.0021 m²**; downward-facing
50 × 26 = 0.0013 m².

**Heat in:**

| Term | Value | Basis |
|---|---|---|
| Internal dissipation | **1.20 W** | driver 0.20 + buck loss 0.06 + logic 0.2 + emitters 0.14 + margin |
| Direct solar | **1.80 W** | 0.0021 m² × 900 W/m² × α = 0.95 (black carbon-filled) |
| Ground-reflected solar | **0.28 W** | 0.0013 m² × 900 × albedo 0.25 (dry caliche/grass, ASSUMPTION) × 0.95 |
| **Total in** | **3.28 W** | |

**Heat out:** `h_conv · A + h_rad · A`, with the linearised radiative coefficient
`h_rad = 4εσT_m³` = 4 × 0.92 × 5.67e-8 × 340³ = **8.2 W/m²K** [D]:

| Case | h_conv | Σ(hA) | ΔT above sink | Wall temp at 50 °C air |
|---|---|---|---|---|
| **Parked in sun, no wind** (radiative sink ≈55 °C: hot ground, hot air) | 8 | 0.146 W/K | **22.5 K** | **77.5 °C** |
| Parked in sun, 3 m/s breeze | 20 | 0.254 W/K | 12.9 K | 68 °C |
| Hovering (rotor downwash ≈5–10 m/s) | 50 | 0.524 W/K | 6.3 K | 56 °C |
| No sun (the old model) | 8 | 0.146 W/K | 8.2 K | 58 °C |

**The binding case is parked in sun with no wind: 77.5 °C against CF-PETG's
Tg ≈ 80 °C — 2.5 K of margin, which is not margin.** Note that this is the case
the old model did not consider at all, and that the hover case, which the old
model implicitly represented, is comfortable.

**The dominant lever is surface finish, not lid material.** Direct solar at
1.80 W is 55 % of the input, and it scales linearly with absorptivity:

| External finish | α | Solar in | Parked-in-sun wall temp |
|---|---|---|---|
| Black CF-PETG (baseline) | 0.95 | 2.08 W | **77.5 °C** |
| Light grey / white overprint or wrap | 0.40 | 0.88 W | **64 °C** |
| Bare aluminium lid, unanodised | ~0.4 (but ε ≈ 0.1 — *worse*, it stops radiating) | 0.88 W | see below |

1. **ECO-1 (revised): `bay_lid` in 1.5 mm 6061, light-anodised or white-painted
   on the outside** — 50 × 42 × 1.5 mm = 3.15 cm³ = 8.5 g versus 7.1 g printed,
   i.e. **+1.4 g** — with the TMC2209 thermal pad bonded to it through a 1 mm gap
   pad. The finish requirement is not cosmetic: bare aluminium has ε ≈ 0.1, and
   since radiation carries ~50 % of the heat out of this bay, a bare lid would
   *raise* the bay temperature despite the better conduction. **Specify: light
   anodise or white paint, α ≤ 0.4 and ε ≥ 0.8.**
2. **The whole payload's external surface shall be light-coloured** (α ≤ 0.4).
   This is worth more than the lid and costs nothing at print time.
3. Print `electronics_bay` in **ASA-CF or PC-CF** (Tg ≈ 105–115 °C) even if the
   rest of the payload stays CF-PETG (concept §8 already flags ASA-CF for
   sun-facing shells). With ECO-1 + a light finish this becomes optional rather
   than required.

TMC2209 junction adds ~12 K at θJA ≈ 40 K/W with a via-stitched pad; even from a
77.5 °C wall that is ~90 °C junction, far under its limit. **The plastic, not the
silicon, is the constraint.**

Electrolytics: hybrid-polymer, 125 °C, ≥2000 h — a 105 °C wet cap at 67 °C
internal has a ~5 000 h life and would become a scheduled replacement item.

**B4 is an oven test, not a sun test.** Amended: B4 shall include an outdoor or
solar-lamp soak at ≥900 W/m² with the payload parked and unshaded, because the
binding case above is driven by a term an oven cannot reproduce.

### 2.7 Thermal — the motor, which the earlier draft never analysed [D]

§2.6 carefully worried about a 1.2 W bay and then ignored the largest dissipator
in the payload. At IRUN = 31 the windings burn **2.66 W continuously whether the
rotor moves or not** — that is §2.4's own point, and it cuts both ways.

NEMA 14 body 35 × 35 × 33 mm; one end is blanked by the gearbox, so
`A ≈ 4 × 0.035 × 0.033 + 0.035² = 0.0059 m²` [D]. One end and part of the
mounting face sit against printed CF-PETG, whose surface is at bay temperature,
so the radiative sink is *not* ambient and the effective combined coefficient is
poor. Taking a deliberately conservative **h_eff = 10 W/m²K** (convection into
still bay air plus weak radiation into warm plastic):

| Condition | Dissipation | ΔT | Case temp at 50 °C ambient |
|---|---|---|---|
| Metering index (IRUN 18) | 0.94 W | 16 K | 66 °C — fine |
| **Recovery, sustained (IRUN 31)** | **2.66 W** | **45 K** | **95 °C — exceeds CF-PETG Tg 80 °C at the mount** |
| Continuous-equivalent limit for a 75 °C case | 1.48 W | 25 K | the budget to stay inside |

**But the thermal mass makes a *bounded* recovery trivially safe, and that is the
actual fix.** Motor mass 290 g, steel `c ≈ 460 J/kg·K` → thermal time constant
`τ = mc/(h_eff·A) = 133.4/0.059 = 2260 s ≈ 38 min` [D]. A 4 s recovery burst
deposits 10.6 J, i.e. an adiabatic rise of **0.08 K**. The hazard is not a
recovery attempt; **the hazard is an unbounded recovery loop**, and the earlier
draft had one: §5.3 ended recovery when "recovery exhausted" without ever
defining exhausted — no attempt count, no time limit, no cool-down — while
§5.3 clause 8 let a 12V_PL power cycle clear the latch and re-arm the payload to
try again.

**Bounded-recovery contract (§3.3, §5.3 clause 12):**

| Bound | Value | Basis |
|---|---|---|
| Max reverse-oscillate attempts per transaction | **6** | [J] |
| Max cumulative energised time per recovery episode | **4 s** | 0.08 K adiabatic rise; 2.7 % of τ |
| Max cumulative recovery duty, any 10-min window | **30 %** | 0.30 × 2.66 = 0.80 W < the 1.48 W budget |
| Mandatory cool-down after `JAM_UNRECOVERED` | ground `ClearFault` only | power-cycle-proof once faults are FRAM-persisted (§5.3 clause 8) |
| Recovery current | **lowest IRUN that meets the shear requirement**, stepped 18 → 24 → 31, not the ceiling first | reduces both fines generation and heat |

**Motor thermal sensing (ECO-10):** a 10 kΩ NTC (`NCP18XH103F03RB`, 0603,
$0.15) bonded to the motor mounting face, into an MCU ADC, reported as
`motor_temp_c` in `Status`. Threshold **>75 °C → `MOTOR_OVERTEMP` (bit 15),
refuse to arm.** This is the mount temperature, not the winding temperature; the
winding is hotter and is inferred, not measured. Fault bit 10 `OVERTEMP` remains
"driver or board", so the two are distinguishable.

**Residual:** the 2.66 W figure moves with the unresolved motor data conflict
(open issue 1). B3 shall measure winding resistance and a case-temperature rise
curve at IRUN 31 on the delivered motor. Until then the 2.66 W is derived from
the 6.8 Ω data set; the 3.2 Ω set would give **1.25 W** at the same current,
which is *better*, so the number above is the conservative branch.

### 2.8 Guaranteed interlock states — the table that was missing

The earlier draft asserted a "two-key arm" (§2.2) and "three layers" (§5.1) but
never stated what any interlock element *does* at power-up or after a reset. This
table is now normative. Every cell is a hardware property unless marked (fw).

| Event | K1 / 12VSW | Motor eFuse EN | TMC2209 ENN | Motor coils | Disc position | Exit port |
|---|---|---|---|---|---|---|
| **12V_PL rise, MCU in POR** | aircraft-determined | **LOW** (100 kΩ pull-down; GPIO Hi-Z) | **HIGH** (100 kΩ pull-up to VCC_IO; GPIO Hi-Z) | de-energised, outputs floating | unchanged (no motion on boot, §3.2) | as left |
| **12VSW rise (K1 closes) with MCU already running** | closed | LOW until firmware asserts | HIGH until firmware asserts | de-energised | unchanged | as left |
| **MCU POR / brownout / IWDG / external WDT reset** | unchanged | **LOW** (NRST tri-states all GPIO) | **HIGH** | de-energised within one chopper cycle | frozen | see §3.2 exposure bound |
| **MCU SWD halt, or unprogrammed part** | unchanged | **LOW** | **HIGH** | de-energised | frozen | as left |
| **12V_PL cycle (FMU_CH4 SSR)** | unchanged | LOW through the whole cycle | HIGH through the whole cycle | de-energised | frozen | as left |
| **12VSW cycle (FMU_CH2 / K1)** | opens | irrelevant — no VM | HIGH | de-energised | frozen | ≤1 pellet exposure (§3.2) |
| **CAN loss > 1 s** | unchanged | LOW (fw disarm) | HIGH (fw) | de-energised | parks if mid-transaction and able | closed after park |
| **PWM loss > 500 ms in PWM_ARM** | unchanged | LOW (fw disarm) | HIGH (fw) | de-energised | parks if able | closed after park |
| **eFuse thermal latch-off** | unchanged | asserted, but output off | HIGH (fw, on `MOTOR_EFUSE_OFF`) | de-energised | frozen | as left |
| **FC boot / FC reboot in flight / RC failsafe / FC param reset** | **UNSPECIFIED — see below** | LOW (MCU refuses to arm without a valid PWM arm band) | HIGH | de-energised | unchanged | as left |

**ENN polarity is verified, not assumed:** "Enable not input. The power stage
becomes switched off (all motor outputs floating) when this pin becomes driven to
a high level." [V TMC2209 datasheet Rev 1.05, pin 2 description]. And the pin
type in the same table is **`DI`** — plain digital input — whereas SPREAD,
MS1_AD0 and MS2_AD1 are **`DI (pd)`**, i.e. the datasheet distinguishes pins that
*do* have internal pull-downs and ENN is not one of them. **The 100 kΩ pull-up on
ENN is therefore mandatory, not belt-and-braces.**

**ICD change request (levied on project-quiver, ICD v1.0-draft §3).** K1 is the
only non-firmware layer in the safety chain and it is driven by **FMU_CH2 from
the flight controller**, whose state at FC power-up, at an in-flight FC reboot,
during RC failsafe, during a parameter reset, and while the FC is disarmed is
**not specified anywhere**. If FMU_CH2 floats or asserts at FC boot, 12VSW
appears at the payload with no operator involvement. The payload cannot enforce
this unilaterally — the payload-side compensation is the EN pull-down, which is
why that pull-down is treated as safety-critical. **Request: ICD §3 shall state
that K1 is commanded open at FC boot, on FC reset, and in RC failsafe, and that
FMU_CH2 defaults to the K1-open level.** The ICD is v1.0-*draft* and this relay
was added to the Main PCB specifically for this dispenser, so this is the moment
to levy it. Tracked as open issue 9.

**What this table does *not* claim.** It does not claim the disc is in a safe
*position* after every event — only that no torque can be produced. Position
safety is a separate argument with a bounded exposure, in §3.2.

---

## 3. Actuator drive and phase sensing

### 3.1 Driver

**TMC2209-LA-T, soldered to the main board** (not a plug-in "stepstick" module —
pin-header modules are a known vibration failure on airframes [J]).

- 1/16 or 1/32 microstepping, SpreadCycle for the metering and recovery moves.
- **ENN: 100 kΩ pull-up to VCC_IO, plus an MCU GPIO.** Active-low enable; high =
  power stage off, all motor outputs floating [V datasheet pin 2]. The pin has no
  internal pull (§2.8), so a dead, resetting or unprogrammed MCU must be made to
  disable the output stage by an external resistor. This is the payload's
  innermost default-safe layer and it works even with VM present.
- **Current ceiling is R_SENSE = 0.50 Ω + a VREF divider, not a register**
  (§2.3). `IHOLD_IRUN` reset default is IRUN = 31 [V datasheet §5.2], which the
  chosen R_SENSE maps onto the intended 0.63 A peak recovery current rather than
  onto 0.8 A full scale.
- Chopper frequency shall be set away from the optical carrier (§4.4).
- StallGuard4 is enabled and reported as diagnostic telemetry but is **not** the
  primary jam detector (§3.3).

**Correction to a tempting-but-false safety argument.** It would be convenient to
say that the TMC2209 has no internal motion generator, so the MCU's STEP line is
the only possible source of rotation, and to present that as the strongest
available safety claim. **It is not true.** The datasheet states: *"Even motion
without external STEP pulses is provided by an internal programmable step pulse
generator: Just set the desired motor velocity."* [V TMC2209 Rev 1.05 §1] The
register is `VACTUAL` (0x22): *"VACTUAL allows moving the motor by UART control.
… 0: Normal operation. Driver reacts to STEP input. /=0: Motor moves with the
velocity given by VACTUAL."* [V §5.2]. So a single UART write can rotate the
disc with the STEP line held static. What the part genuinely lacks is a **ramp
generator** ("However, no ramping is provided by the TMC2209" [V §1]), which is a
motion-quality property, not a safety property.

The correct hardware statement, which *is* true and is the one this design
relies on, is narrower and stronger because it does not depend on the MCU at all:

> **Rotation requires VM at the driver AND ENN low. VM requires K1 closed
> (aircraft, mechanical contact) AND the payload's eFuse EN asserted (100 kΩ
> pull-down). ENN low requires an MCU GPIO actively driving against a 100 kΩ
> pull-up. No single failure of the MCU, the firmware, the UART or the STEP line
> can satisfy all three, and none of the three is satisfied by default.**

`VACTUAL` reset default is 0. The MCU shall verify it reads back 0 before every
dispense as part of the §2.3 register-readback check.

### 3.2 Phase sensing — the r6 magnet/Hall set already gives a static safe-state decode

The r6 CAD places, at radius **42.5 mm** [V `dispenser.py` L354, L796, L810]:
8 magnets at the pocket angles (45° pitch) + 1 index magnet at 22.5°, all in the
disc underside; and two Hall cavities in the retaining plate at **θ = 90.0°
(station)** and **θ = 112.5° (index)** — i.e. **22.5° apart, at the same
radius**. [V L365-366, L993-995]

Because the two-phase index scheme parks at 22.5° offsets [V BUILD-NOTES-r6 §3
item 3], those two sensors decode the disc's *safety-relevant* state statically,
with no motion, at any time including immediately after a power cycle [D]:

| Hall @90° | Hall @112.5° | Disc state | Safe? |
|---|---|---|---|
| 0 | 1 | **PARK** — a web is over the Ø18 exit port | **yes** |
| 1 | 0 | **CONCENTRIC** — a pocket is over the exit port | no (dwell state only) |
| 1 | 1 | CONCENTRIC **and** at the once-per-rev index (φ = 90°) | no |
| 0 | 0 | mid-index, or lost phase | **unknown → `PHASE_LOST`** |

**Consequence for the ICD power-cycle clause:** the payload does **not** home on
boot. Homing motion could carry a loaded pocket across the exit port and release
an uncommanded pellet. Instead it reads the 2-bit state statically; if it is
PARK, phase is known (all eight pockets are identical, so knowing the position
modulo 45° is sufficient) and the payload can arm without moving. If it is not
PARK, the payload boots into `PHASE_LOST`, refuses to arm, and requires an
explicit ground-commanded recovery — which may drop one pellet and shall report
it as `UNCOMMANDED_DROP` with the count sensor armed throughout. This is the
concrete hardware answer to concept §10.4 ("safe-state story is firmware, not
mechanism").

**ECO-2 (verification, not a change):** confirm in CAD that the 8 pocket magnets'
angular phase puts a magnet under the 112.5° Hall exactly at park. The geometry
as written does this; it should become an asserted check in `dispenser.py`
alongside the existing `hall cavity vs exit hole` probe, and the sensors should
be **renamed** (`HALL_A`/`HALL_B`, not "station"/"index") because the 112.5°
sensor's real job is *park detection*, not revolution indexing.

**The (0,0) ambiguity is a real defect and ECO-8 closes it.** As specified, the
2-bit decode maps *"stopped mid-move, with a pocket partly over the exit port and
possibly leaking"* and *"a Hall sensor has failed"* onto the **same** code (0,0).
Those two states demand opposite responses — the first is an active release
hazard, the second is a sensor fault — and the payload cannot tell them apart.

**ECO-8: fit a third DRV5023.** The retaining plate has room at the same
r = 42.5 mm circle. A third sensor gives a 3-bit code; the angle shall be chosen
(and **asserted in `dispenser.py`, exactly as ECO-2 requires**) so that the four
safety-relevant states — PARK, mid-move-outbound, CONCENTRIC, mid-move-return —
each produce a distinct code, and so that any single stuck-at-0 or stuck-at-1
Hall produces a code that is *not* a valid motion state. The exact angle is
**deliberately not asserted here**: it depends on the pocket-magnet phase that
ECO-2 is still verifying, and inventing it would be exactly the kind of
plausible-but-unchecked number this document is supposed to avoid. Cost $1.30 +
one cavity + one conductor.

*Alternative considered and not chosen:* a direct port-occlusion sensor (a
short-range reflective head under the exit port, reading web-present vs
pocket-open). It measures the safety-relevant state directly rather than
inferring it from phase, which is better in principle, but it puts an optical
surface in the pellet path immediately above the chute — the fouling problem
§4.5 spends seven measures on, in the worst possible location. The third Hall is
outside the pellet path and reuses a qualified part.

### 3.2.1 What K1 actually guarantees, and the bounded exposure it does not

§2.1 calls the K1 galvanic disconnect "the strongest safety statement available
for a herbicide release mechanism". That is true of *torque*, and only of torque.
**K1 is a stop, not a safe state.** Opening K1 mid-move — or any 12VSW loss, or
the eFuse latching off — freezes the disc wherever it is, which can be part-way
through the 22.5° release move with a pocket partially over the Ø18 exit port and
a pellet on it. There is no stored energy to complete a return-to-park: the
return move needs ≈0.63 J and the specified 100 µF at 12 V holds **7.2 mJ**, a
factor of ~87 short [D]. The detent seat exists only *at* park; between park
positions the disc is held by gearbox friction and motor detent torque alone.

**The exposure is bounded at one pellet, and here is the geometry [D].**
`PORT_R = 9.0` at `PCD_R = 32.0`, `POCKET_R = 7.5`, `N_POCKET = 8` (45° pitch)
[V `dispenser.py` L231-235, L309]. The r6 pellet-path critic showed a pellet
loses support **3.16–6.78° into the 22.5° release move** [V BUILD-NOTES-r6
§"pellet-path"], i.e. support is lost only within ≈7° of a pocket arriving over
the port. The next pocket is **45° away — 6.4× further** — and is under the
close-clearance housing arc, not over the port. Therefore **at most one pocket
can be in the release window at any disc angle, so at most one pellet can escape
a mid-move stop.** The hopper cannot free-flow behind it: the disc web plus the
housing arc occlude the port for every other angle.

**Consequences, stated rather than implied:**

- Exposure on any mid-move power loss: **≤1 pellet**, port left partially open
  until a ground-commanded recovery.
- **The count sensor now records it** (§2.4: emitters continuous), so the drop
  produces an `UNCOMMANDED_DROP` event and an FRAM record instead of nothing.
  Under the earlier gated-emitter budget it produced neither.
- **Operating procedure (levied on the manual, not on firmware): K1 is an
  emergency kill.** Normal disarm shall wait for the `PARK` confirmation in
  `Status.disc_phase`. Opening K1 during `DISPENSING` is a deliberate,
  logged, one-pellet-exposure action.
- **Not adopted, and why:** a light torsion return spring would make PARK the
  mechanical rest state at *all* disc angles, not only at park, and would make
  §2.3's "power-cycle rest state is a mechanical property" argument true in
  general. It needs an over-centre cam so it does not fight the release move, it
  costs ≈0.05 N·m against the 0.39 N·m metering budget (13 %), and it is a
  mechanical redesign this electronics document cannot specify responsibly.
  **Recorded in §11 as an accepted residual with a named owner: the mechanical
  revision r7.**

**Magnet field [D].** N45, Br ≈ 1.32 T, Ø3 × 2 mm, on-axis
`B = Br/2 · [ (z+L)/√(R²+(z+L)²) − z/√(R²+z²) ]`. Air gap = 0.5 mm under-gap +
1.5 mm plate above the cavity + ~0.4 mm to the die ≈ **2.4 mm**:

| Gap | 1.5 mm | 2.0 mm | **2.4 mm** | 3.0 mm |
|---|---|---|---|---|
| B on axis | 140 mT | 90 mT | **65 mT** | 42 mT |

65 mT against a ~10 mT operate point is **6.5×** — enough that fouling, magnet
tolerance and a 0.5 mm build error are all absorbed. Adjacent magnets are 32.5 mm
away at 45° pitch, contributing <1 mT, so there is no cross-talk. All nine magnets
must be installed **same pole outward** (unipolar switches, not latches).

**BOM correction — this is a real defect in the r6 BOM.** It specifies
**TI DRV5032FBDBZR**. The DRV5032 is an *ultra-low-power sampled* Hall switch:
its sampling-rate options are **5 Hz / 20 Hz** class [V TI DRV5032 datasheet].
A magnet subtends ≈8.1° of significant field at r = 42.5 mm, which at the index
speeds below is **34 ms (240 °/s) to 90 ms (90 °/s)** of dwell [D] — a 20 Hz
sampler (50 ms period, up to 50 ms of latency) will miss transitions and is
useless for closed-loop index verification.
**Specify instead: TI DRV5023 (continuous-time, chopper-stabilised, 2.5–38 V,
open-drain 30 mA, reverse-supply protected).** Threshold suffix: choose the
~10 mT option; exact Bop per suffix is an **ASSUMPTION** to confirm on the
datasheet at order time — every family option is met with margin at 65 mT.

### 3.3 Stall / lost-step detection

Primary: **Hall transition timing.** Every commanded 22.5° index must produce the
expected Hall state transition within a time window derived from the motion
profile. No transition → stall or lost step, detected within one index, with no
tuning. This is deterministic, temperature-independent, and uses parts already in
the design.

Secondary: **StallGuard4** (reported, used to tune, and useful for detecting a
*soft* stall — increased load without a lost step).

Explicitly rejected: **12VSW input-current sensing as a stall detector.** §2.4
shows input current *decreases* at stall with a chopper drive. Current *is*
measured — by the eFuse **ILM** pin (§2.2), which replaces the 0.05 Ω shunt the
earlier draft specified — for power telemetry, for the `OVERCURRENT` thresholds,
and for detecting a *driver* fault. It must not be presented as jam detection.

**Recovery is bounded (§2.7).** The earlier draft ended recovery when "recovery
exhausted" and never defined exhausted. Normative: **≤6 reverse-oscillate
attempts per transaction; ≤4 s cumulative energised time per episode; ≤30 %
recovery duty in any 10-minute window; current stepped IRUN 18 → 24 → 31 rather
than starting at the ceiling; on exhaustion, park if possible, latch
`JAM_UNRECOVERED`, and require a ground `ClearFault` that a power cycle cannot
substitute for.** The thermal justification for each bound is in §2.7.

### 3.4 Speed limit at 12 V, and why it helps the accuracy budget

At 12 V the chopper must supply `V ≈ √((I·R + K·ω_m)² + (ω_e·L·I)²)`, with
`ω_e = 50·ω_m` for a 1.8° motor and a first-order `K ≈ T_h/I_rated = 0.225
V·s/rad` [D, first-order]. Allowing 0.6 V of driver drop:

| Phase current | Max motor speed | At the disc (÷5.18) |
|---|---|---|
| 0.63 A (recovery) | 208 rpm | **241 °/s** |
| 0.37 A (metering) | 305 rpm | **354 °/s** |
| 0.80 A (never used) | 160 rpm | 186 °/s |

So 12 V is adequate but not generous, and it **caps** disc speed. That cap is a
gift, because the r6 pellet-path critic showed the pellet loses support
**3.16–6.78° into the 22.5° release move**, not during the dwell, so lateral
release velocity is `ω × 32 mm` [V critic, BUILD-NOTES-r6 §"pellet-path"]:

| Release-move speed | v_lat | Lateral drift over the 1.28 s fall from 8 m AGL |
|---|---|---|
| 60 °/s | 0.034 m/s | **0.04 m** |
| 90 °/s | 0.050 m/s | **0.06 m** |
| 180 °/s | 0.101 m/s | 0.13 m |
| 240 °/s | 0.134 m/s | 0.17 m |

**Contract clause (§5.4): the release move (park → concentric) shall be executed
at ≤90 °/s and the return move (concentric → park) at ≤240 °/s.** Motion timing
[D, trapezoid]: release 22.5° at 90 °/s / 1500 °/s² = **310 ms**; dwell **150 ms**;
return 22.5° at 240 °/s / 3000 °/s² = **174 ms** → **634 ms per pellet**, N = 3 in
**1.9 s**, N = 3 with two skips in **3.2 s**. Acceleration is free: total reflected
inertia ≈4.7 × 10⁻⁶ kg·m² needs only ~5 mN·m to reach full speed in 20 ms, versus
180 mN·m available at the motor [D].

### 3.5 EMI and magnetic cleanliness

- Motor leads: 4-conductor twisted, ≤160 mm, routed away from the CAN pair;
  chopper edges kept on the board with 100 nF + ferrite at the VM entry.
- Zero hold current (§2.3) removes the static winding dipole between dispenses —
  relevant because the payload hangs 180 mm below the airframe on the same axis
  as the flight controller's compass.
- **Bonding.** The payload is almost entirely printed plastic; the only metal
  bonded to the airframe is the aluminium clip plate. The motor case sits on
  printed parts and is otherwise floating. Fit a **bonding lead from the motor
  case to payload GND** (EMI + a defined potential).

### 3.6 ESD — immunity level, and protection where the hazard actually is

The earlier draft specified protection for the two rails (SMAJ13A), CAN
(NUP2105L) and CH1 (1 kΩ + TVS) — all on the main board, all sensible — and
**nothing at all for the two sensor harnesses**, which are the nodes most exposed
to the hazard this document itself identifies: herbicide pellets
sliding on plastic are a triboelectric charge source [J], and §7 deliberately places
the OPA2320 TIA inputs *at the chute*, i.e. at the charge-generation site, for
noise reasons. The PMMA windows (ECO-4) are insulators sitting in the pellet
stream and will charge. A discharge into the LED-drive or TIA lines destroys a
$2.45 op-amp and blinds the count sensor mid-sortie, or produces a phantom event
— and under §5.3 clause 5 ("anything that plausibly left the aircraft counts") a
phantom event causes an **under-dose that is reported as a verified count**.

**Target immunity level (now stated, previously absent):**

| Interface | Level |
|---|---|
| Enclosure ports, external surfaces | **IEC 61000-4-2 ±8 kV contact / ±15 kV air**, criterion B (self-recovering, no data corruption of the FRAM count) |
| Blind-mate pads (hand-handled in the field per the ICD's hot-swap claim) | **HBM Class 2 (±2 kV)** minimum on every pad |
| Sensor harness conductors | ±8 kV contact via the enclosure path |

**Protection added:**

- **Low-capacitance ESD diode arrays at both ends of both sensor harnesses**
  (`ESD9B5.0ST5G` class, **C ≤ 5 pF**, ~$0.20 each × 6). The capacitance limit is
  the whole point: at the 6.8 kΩ transimpedance of §4.4, 5 pF is a 34 ns pole,
  i.e. 4.7 MHz — two orders of magnitude above the 38 kHz carrier, so the TIA
  bandwidth is untouched. A general-purpose 100 pF part would not be.
- **A grounded conductive bushing at the bore mouth**, tied to the bleed network,
  rather than relying on a plastic chute liner. This intercepts the charge at the
  source instead of at the amplifier.
- **Antistatic bleed at the chute:** conductive ring or liner to payload GND
  through **1 MΩ ∥ 10 nF**, giving a bleed path without a ground loop.
  Effectiveness remains an **ASSUMPTION** — and it is now a *gated* bench item
  (B9), not an unscheduled one, because it was previously the only ESD-relevant
  test in the plan and it was not in the B1–B7 gate list at all.

**Where the ESD current goes — the single-GND-pin analysis, re-run for a
transient.** §2.4 analysed pin 4 for 0.34 A of DC and correctly concluded the
34 mV offset is irrelevant. That analysis does **not** transfer to ESD. The
1 MΩ ∥ 10 nF bleed dumps the fast edge into payload GND, which is a *single*
blind-mate spring pin shared as the reference for CAN, FMU_CH1 and both rails.
A 61000-4-2 contact discharge has a 30 A peak with a ~1 ns rise; through the
~100 mΩ contact resistance and, dominantly, the **inductance of one 300 mm 26 AWG
conductor (≈0.3 µH [J])**, `V = L·di/dt` gives **≈9 kV** of payload-ground bounce
relative to aircraft ground [D, order-of-magnitude]. That is far outside CAN's
±12 V common-mode range and is the real reason the following are mandatory:

- **The NUP2105L on CAN and the 3.3 V TVS on CH1 are ESD parts, not just
  overvoltage parts** — they are what keep the transceiver and the FMU pin alive
  while payload ground moves.
- **Both GND crimps of the doubled Molex J1 ground net shall be populated**
  (§6.1 already requires this for current capacity; it halves the inductance too)
  and routed as a **twisted pair with the rails**, not as a single straight run,
  to cut the loop area.
- **The discharge shall be given a path that is not the blind-mate pin:** the
  aluminium clip plate is the only metal bonded to the airframe, so the chute
  bleed network's return shall be bonded to the clip plate as well as to payload
  GND, giving the transient a short, low-inductance path into the airframe.

**Detection:** partial. The LED-off dark-current reading (§4.6) catches a
destroyed PD, but not a transient phantom event. That residual is in §11.

---

## 4. Count sensor (the "verified count" requirement)

CONTEXT: *"Commanded count must be VERIFIED (sensed), not assumed."* The sensing
point is a through-beam across the Ø22 chute, after the granule has irrevocably
left the mechanism.

> **CORRECTION (rev-1 r12, 2026-08-08).** The sentence this section shipped —
> *"40 mm below the retaining plate (Z ≈ −343.2, 10 mm above the chute exit)"* —
> **was stale by 49.1 mm** and is struck. Measured on the shipped exports by the
> round-5 count-sensor critic and reproduced on `r12`: release plane (retaining
> plate top face) **Z = −351.250**; **beam A Z = −392.250, beam B Z = −398.250**;
> chute mouth **Z = −418.300**. So the fall is **41.000 mm to beam A and
> 47.000 mm to beam B**, and beam A is **26.050 mm** above the chute mouth, not
> 10. The two beams therefore run at **v_A = 0.8969 m/s and v_B = 0.9603 m/s**
> — 7.1 % apart — against the 0.8859 m/s this section computes from 40 mm.
>
> Consequences that must be carried into §4.2/§4.3 before the B1 dark-time
> survey freezes any threshold: §4.3 takes the **longer** dark time (beam A), so
> the Ø11 guarantee moves **10.41 → 10.28 ms** against the 9.7 ms gate and the
> stated margin drops **7 % → 6.0 %**; the Ø8 best case moves 9.03 → 8.92 ms, so
> the separator is **1.36 ms** wide, not 1.37; and **ECO-9's `Δt_mid` for the
> 6.000 mm stagger becomes 6.461 ms, not 6.54 ms**. Nothing here is
> disqualifying and B1 is what freezes the gate anyway — but the numbers in
> §4.2 and §4.3 below are still computed from 40 mm and have **not** been
> re-derived. That re-derivation is an open item (`BUILD-NOTES-r6.md` §9 item
> 10); it was not done in round 6 because round 6's scope was the CAD.

### 4.1 Existing CAD provision

Two bosses `Box(12,12,14)` at `(x=32, y=±17)`, a **Ø3.2 aperture** at y = ±16, a
**Ø6.5 × 8 component pocket** from the outer face, and an M3 grub screw for
retention — sensor faces **recessed 5.0 mm** from the bore. [V L1005-1017]

### 4.2 The problem with a single centred beam — worked, and it is disqualifying

Free-fall velocity at the beam: `v = √(2·9.81·0.040) = 0.886 m/s` [D].
A Ø12 pellet in a Ø22 bore can sit anywhere within ±5.0 mm of the axis. A pencil
beam on a diameter is occluded for `2√(r² − x₀²)/v`:

| Pellet | offset 0 | offset 2 mm | offset 5 mm |
|---|---|---|---|
| Ø11 | 12.4 ms | 11.6 ms | **5.2 ms** |
| Ø12 | 13.5 ms | 12.8 ms | **7.5 ms** |
| Ø13 | 14.7 ms | 14.0 ms | (max offset 4.5 mm) |

The concept's gate — *"accept ~10–35 ms as one pellet; <10 ms = fragment (do NOT
count)"* (concept §4) — **rejects a real Ø12 pellet that falls near the chute
wall as a fragment**, and a Ø11 pellet reads shorter than a centred Ø8 fragment.
The dark-time discriminator and the count itself both fail. This is a geometry
error in the baseline, not a threshold-tuning issue.

### 4.3 Recommended: two parallel chord beams at x = axis ± 3.0 mm

Two beams, same height, both along **y** (the only feasible axis: the motor body
occupies |x| < 17.6 mm at this Z, so no beam can pass inboard of the chute) [D
from `dispenser.py` L2095], separated by 6.0 mm and straddling the bore axis.
Count logic takes the **longer** of the two dark times. Guaranteed bounds over
every lateral position [D]:

| Object | Guaranteed dark time (worst position) | Best case |
|---|---|---|
| Ø5 fines/fragment | may pass **undetected** (correct — not a pellet) | 5.6 ms |
| Ø8 fragment | may pass undetected | 9.0 ms |
| **Ø11 pellet** | **10.4 ms** | 12.4 ms |
| **Ø12 pellet** | **11.7 ms** | 13.5 ms |
| **Ø13 pellet** | **13.0 ms** | 14.7 ms |

**A pellet is never missed** (its centre is always within 3.0 mm of at least one
beam: nearest-beam distance ≤3.0 mm ≤ r−2.5 for r ≥ 5.5) and its dark time never
falls below 10.4 ms. Allowing 18 % velocity loss to wall rubbing [J], the
**pellet band is 10.4–17.5 ms**.

**Gate — corrected. The shipped 6 ms lower bound threw away the discrimination
this geometry was built to create.** The table above says a Ø8 fragment "may pass
undetected" with a best case of 9.0 ms, and an independent check confirms it:
a Ø8 fragment (r = 4) reads **6.0 ms at its worst lateral position** (centred at
x = 0, both beams at d = 3 mm) rising to **9.03 ms** when centred on a beam, and
it can only miss *both* beams at |x| ≥ 7 mm, i.e. grazing the bore wall [D].
Meanwhile a Ø11 pellet is guaranteed ≥10.4 ms. **With the lower gate at 6 ms,
85 % of all lateral positions of a Ø8 fragment are counted as a whole pellet**
[D, see the residual table below] — and combined with §5.3 clause 5 ("anything
that plausibly left the aircraft counts toward N") the payload stops at N having
delivered N−1 pellets plus a crumb, and reports a verified count of N. CONTEXT's
hard requirement is *"dispense exactly N pellets … VERIFIED (sensed)"*; a 6 ms
gate verifies a count of **objects**, not of pellets.

Nothing justified the 6 ms bound. Velocity loss from wall rubbing only
*lengthens* dark time, so it cannot motivate lowering the lower bound.

**Gate (revised; still to be frozen by B1, not shipped as gospel):**
`<9.7 ms` = fines/fragment, **not counted** · `9.7–25 ms` = **one pellet,
counted** · `>25 ms` = double, hang or lodged pellet →
`OVERCOUNT`/`CHUTE_BLOCKED`. 9.7 ms sits in the clean separator the geometry
already provides — Ø8 best case 9.03 ms, Ø11 guaranteed 10.4 ms — with 7 %
margin on each side. **Fines below Ø8 are deliberately uncounted, and this is
stated in the contract rather than left implicit** (§5.3 clause 5a).

**Effect of the change at nominal fall velocity [D]** — the fraction of the
14 mm-wide lateral band (|x₀| ≤ 7 mm) in which a Ø8 fragment is miscounted as a
pellet, as a function of velocity loss `f` from wall rubbing:

| Velocity loss f | 6 ms gate (old) | **9.7 ms gate (new)** |
|---|---|---|
| 0 % (free fall) | 85 % | **0 %** |
| 7 % | 92 % | **0 %** (threshold of entry) |
| 10 % | 96 % | **29 %** |
| 15 % | 100 % | **47 %** |
| 18 % (the §4.3 allowance) | 100 % | **54 %** |

**The honest limit: dark time alone cannot separate size from velocity.** That is
the real defect behind the gate choice, and raising the gate reduces it without
removing it. Two beams at a common height give two chords and no velocity
information, so a Ø8 fragment slowed by ≥7 % is indistinguishable from a Ø11
pellet. **ECO-9 fixes the velocity half of the problem outright.**

**ECO-9 (CAD): stagger the two beams vertically by 6.0 mm.** Beam A at
x = +3.0 mm at the present Z; beam B at x = −3.0 mm, **6.0 mm lower**. Both
chords stay at x = ±3.0 mm, so §4.3's lateral-coverage proof is unaffected, and
the 14 mm-tall bosses have the room (`Box(20,12,14)`, ECO-3).

*Why the midpoint, not the leading edge.* The leading edge of each channel occurs
when the sphere's surface reaches that beam, which depends on the unknown chord
offset. **The midpoint of each dark interval occurs when the sphere's *centre*
crosses that beam's height — independent of radius and of lateral position.**
Therefore

`Δt_mid = t_B,mid − t_A,mid` = the time to fall exactly 6.0 mm,

and `v` follows from `6 = v·Δt + ½g·Δt²`: at the nominal 0.886 m/s,
**Δt_mid = 6.54 ms** [D]. With a 38 kHz carrier the demodulated envelope resolves
to ≈105 µs, giving `dv/v ≈ (Δz/Δt²)·δt / v` = **±1.7 %** [D]. That is a *direct,
per-event, size-independent velocity measurement*.

With `v` known, each dark time yields a true chord half-length `h = v·t/2`, and
when **both** channels fire the pair solves exactly for both unknowns [D]:

`h_A² − h_B² = 12·x₀` → `x₀ = (h_A² − h_B²)/12`, then `r² = h_A² + (x₀−3)²`.

i.e. a **velocity-independent measurement of the object's radius and of where it
was in the bore.** This also separates doubles cleanly and makes the 18 %
wall-rubbing allowance a *measured* distribution rather than a `[J]` assumption.

**What ECO-9 does not fix, stated plainly.** Both channels fire only when
|x₀| < r − 3 mm:

| Object | Lateral band with both channels | Fraction of its band |
|---|---|---|
| Ø13 pellet | ±3.5 of ±4.5 mm | 78 % |
| Ø12 pellet | ±3.0 of ±5.0 mm | 60 % |
| Ø11 pellet | ±2.5 of ±5.5 mm | 45 % |
| Ø8 fragment | ±1.0 of ±7.0 mm | **14 %** |

A Ø8 fragment that produces a *long* dark time is by definition centred near one
beam (|x₀| ≈ 3), which is exactly the single-channel case. **So the exact size
solve does not catch the dangerous fragment.** For single-channel events the
nominal-velocity gate applies and the residual in the table above stands.
ECO-9's value is real but is (a) the velocity distribution it measures on the
bench, closing the 18 % assumption that sets the residual, and (b) exact sizing
of centred objects, which confirms whole pellets and rejects doubles.

**Contract consequence (§5.3 clause 5a) and residual.** `dispensed_verified`
counts *objects passing the pellet gate*, not pellets. The residual — a fragment
between Ø8 and Ø11 that is also slowed ≥7 % by wall rubbing — is carried in §11.
Its **failure direction is under-dose, not over-dose**: the payload stops at N
having delivered fewer than N whole pellets. §5.3 clause 5's own reasoning
applies — under-dosing is recoverable by re-tasking, over-dosing is the regulated
risk — so the severity is the recoverable one. That mitigates but does not
satisfy CONTEXT's "exactly N, verified", and it is recorded as an open compliance
gap, not written off. **B1 (≥200 real-pellet drops, now including deliberately
fractured pellets) is the test that closes it.**

Bonus properties: two independent detectors (one fouled lens degrades rather than
blinds), and a coincidence test — when both fire they must overlap in time, which
rejects a dust puff or a stray-light glitch on one channel. Per-event `v`, `r`
and `x₀` (ECO-9) are logged in the transaction record so a miscount is auditable
after the sortie rather than invisible.

**ECO-3 (CAD):** widen each sensor boss from `Box(12,12,14)` to
`Box(20,12,14)` centred at x = 32 (spanning x = 22…42; motor face at x = 17.6 →
**4.4 mm clearance**, versus 1.4 mm today), and replace the single Ø3.2 aperture
with **two Ø3.2 apertures at x = 29 and x = 35** — and, per **ECO-9**, at
z = Z_SENSOR + 3.0 and Z_SENSOR − 3.0 respectively, a 6.0 mm vertical stagger that
the 14 mm boss height accommodates with 4 mm of wall left above and below each
aperture. Component pocket becomes a `20 × 8 × 12` cavity holding a small PCB.
Estimated mass +6 g for both bosses [J]. Both bosses use the *same* x/z grid, so
each beam remains a straight chord along y and §4.3's coverage proof is unchanged.

### 4.4 Signal chain

**Emitter board** (one boss): 2 × **Vishay TSAL6200** (940 nm, ±17° half-angle,
100 mA), each driven by a low-side FET + sense resistor in a current sink whose
setpoint is **MCU-programmable in at least 4 steps between 20 and 100 mA**
(this is what makes the excess-gain self-test possible, §4.6). Carrier: square
modulation, **38 kHz baseline**.

**Nominal drive currents — resolving an internal inconsistency in the earlier
draft.** §4.5 measure 3 claimed the firmware can "raise drive as windows foul
(5× of reserve from 20 to 100 mA)", while §2.4 budgeted the emitters at 100 mA
and §4.4's headline 182× excess-gain figure was computed *at* 100 mA. Both could
not be true: if nominal is 100 mA there is no upward reserve, and dust mitigation
measure 3 of 7 was overstated. **Resolved as follows:**

| Mode | Drive | Photocurrent | Excess gain | When |
|---|---|---|---|---|
| **Monitor** (continuous, §2.4) | **50 mA** | 91 µA | **91×** | whenever 12V_PL is present |
| **Dispense window** | **100 mA** | 182 µA | **182×** | the ~400 ms per pellet, where dark-time accuracy matters |
| Excess-gain sweep (§4.6) | 100 → 20 mA | 182 → 36 µA | — | pre-flight self-test only |

So the programmable range gives a **2× upward reserve from monitor to dispense
and a 5× downward sweep for measurement** — the reserve is real but it is 2×, not
5×, and **the 182× static excess gain IS the dust margin**. §4.5 measure 3 is
restated accordingly.

**Receiver board** (opposite boss): 2 × **Vishay VBPW34FAS** (BPW34 with
**daylight-blocking filter**, 7.5 mm² active, peak 950 nm) into a dual TIA
(**OPA2320**), AC-coupled, into two STM32G431 ADC channels sampled coherently
with the carrier (the G431 ADC runs to 4 MSPS; 2 channels × 250 kSPS is trivial
and DMA-driven — no hardware demodulator, no extra parts).

**Why analog rather than a digital receiver module** (e.g. TSSP4038, which the r6
BOM specifies): a digital receiver gives a bit, and a bit cannot report *how much
margin is left*. The analog level is the fouling metric (§4.6) and it costs one
op-amp. **Descope option, named:** TSSP4038 (38 kHz, light-barrier part,
$1.29 @1 [V DigiKey]) drops in on the same apertures if the analog path is
rejected — accepting that fouling is then only detectable when it has already
caused a failure.

**Optical budget [D]** (TSAL6200 Ie = 40 mW/sr at 100 mA, path 32 mm = 22 mm bore
+ 2 × 5 mm tunnel, PD 7.5 mm², responsivity ≈0.62 A/W at 940 nm):

| LED current | Irradiance at PD | PD photocurrent |
|---|---|---|
| 20 mA | 7.8 W/m² | 36 µA |
| 50 mA | 19.5 W/m² | 91 µA |
| **100 mA** | **39.1 W/m²** | **182 µA** |

**Excess gain ≈182×** against a 1 µA practical detection threshold →
**the system still counts with 99.4 % of the light lost to dust**. Shot noise from
ambient is 0.43 nA rms in a 10 kHz band [D], so the threshold is set by amplifier
drift and mechanics, not by noise.

**Ambient rejection [D]:** the tunnel's acceptance solid angle is
`π·1.6²/5² = 0.32 sr`; ground-reflected sunlight up the chute (300 W/m², NIR
fraction 0.4) puts ≈**57 µA of DC photocurrent** on the PD — comparable to the
signal at low LED current. This is why the carrier is mandatory and why the TIA
must be AC-coupled (or DC-servoed) with headroom for that DC term. Verified
sunlight immunity is then a modulation-depth question, not a shading question.

**Carrier/chopper interaction:** the optical carrier must not be harmonically
related to the TMC2209 chopper. Baseline: chopper ≈23 kHz, optical 38 kHz,
demodulation bandwidth ±2 kHz. Bench-tuning item.

**Analog front-end specification [D] — previously absent.** The earlier draft
gave the TIA no transimpedance, no AC-coupling corner and no dynamic-range
budget, while requiring it to handle the 57 µA sunlight DC term, the 182 µA
signal and a 1 µA threshold simultaneously — a ~47 dB span. "Probably fine" was
doing the work of a specification. Now specified:

| Parameter | Value | Derivation |
|---|---|---|
| Transimpedance `R_f` | **6.8 kΩ 1 %** | signal 182 µA → 1.24 V; ambient DC 57 µA → 0.39 V; sum 1.63 V, inside a 3.3 V rail with a 0.3 V mid-ref and ≥1.3 V of headroom for a brighter-than-modelled sky |
| Feedback capacitor `C_f` | **10 pF** | pole at 2.3 MHz; with PD junction + ESD-diode capacitance ≈ 80 pF the loop is stable and the closed-loop BW ≳300 kHz, i.e. ≫ the 38 kHz carrier |
| AC-coupling corner | **1.2 kHz** (100 nF into 1.3 kΩ) | ≥30× below the 38 kHz carrier so the carrier is unattenuated; ≥100× above the fastest credible sun/shadow transient, so ground-reflected sunlight is rejected as DC |
| Detection threshold | **1 µA ≡ 6.8 mV** | 8.5 LSB on the G431's 12-bit ADC at 3.3 V (0.806 mV/LSB) |
| Offset budget | **≈0.24 µA equivalent** | OPA2320 V_OS 150 µV max + 1.5 µV/K × 60 K = 90 µV → 240 µV / 6.8 kΩ. **4.2× under the threshold** |
| Ambient shot noise | **0.43 nA rms** (10 kHz BW) | 2.9 µV — 2 300× under the threshold; noise is not the limit |
| Usable dynamic range | **47 dB** (1 µA … 239 µA) | 6.8 mV … 1.63 V, all inside one ADC range with no gain switching |

The threshold is set by amplifier offset drift and by mechanics, not by noise —
and now that is a stated conclusion with the arithmetic behind it, because
`beam_margin_pct` (§4.6, "the single most valuable thing this sensor can do") is
only as trustworthy as this linear range. **B2 shall verify the linearity of the
excess-gain sweep across the full 20–100 mA drive range at 25 °C and 60 °C.**

### 4.5 Dust tolerance strategy (seven measures, in order of value)

1. **Carrier modulation + synchronous detection** — removes sunlight, removes
   slow drift from film build-up, and makes the count immune to the ambient DC
   term computed above.
2. **182× excess gain** — the design tolerates 99.4 % attenuation before it
   fails. This is the single biggest dust defence and it is bought with LED
   current, which is nearly free at a 0.7 s duty per target.
3. **Programmable emitter current** — the firmware has a **2× upward reserve**
   (monitor 50 mA → dispense 100 mA) and a **5× downward sweep** that *measures*
   fouling (§4.6). This is what turns a beam into an instrument. The earlier
   draft's claim of "5× of reserve from 20 to 100 mA" was inconsistent with its
   own power and optical budgets; see §4.4.
4. **Two beams** — independent optical paths degrade independently; one fouled
   channel is a warning, not a failure.
5. **Recessed tunnels + a replaceable window at the BORE face.** The r6 5 mm
   recess stays. **ECO-4 (revised — the original was unbuildable as described).**

   *Why the original failed.* The r6 geometry is: chute bore wall at |y| = 11;
   Ø3.2 light tunnel at y = ±16, length 26 along y; component pocket Ø6.5 × 8
   from the outer face at y = ±20, i.e. spanning **|y| = 16…24**
   [V `dispenser.py` L1005-1017]. The 5 mm recess is therefore a **Ø3.2 blind
   tunnel from y = 11 to y = 16**. Bonding a window "into the component pocket"
   puts it at y ≈ 16 — so the surface that fouls is the window's **inner** face,
   at the bottom of a sealed blind hole, *behind* the emitter/receiver board. To
   clean or swap it you would remove the grub screw, extract the sensor board and
   its GH pigtail, and debond the disc: the exact opposite of the claimed "wiped
   or swapped from outside without opening the payload". Worse, the CAD comment
   at L1013-1016 says the grub screw exists specifically so the sensor "can be
   re-seated after a swab-out without glue" — a bonded inner window makes that
   swab-out impossible, so the ECO would have **removed** the maintenance path
   the r6 CAD already provides.

   *Revised:* put the window at the **bore face, y = ±11, flush with the chute
   wall**, in a **0.4 mm-deep chamfered recess** so it is not proud of the bore
   and cannot be struck square-on by a falling pellet. Then the fouling surface
   *is* the chute wall, swabbable from the chute exit with a rod on a
   10-second maintenance action, and the 5 mm tunnel plus the sensor behind it
   are **permanently sealed** — which is strictly better than the original
   intent, because the LED/PD cavity now never sees chute air at all. The window
   is a **sacrificial Ø6 × 1 mm PMMA disc**; specify replacement whenever
   `beam_margin_pct` does not recover after a swab. Uncoated PMMA costs ~8 % of
   the light — irrelevant against 182×.

   > **CORRECTION (rev-1 r12).** Two claims in this item are not supported by
   > the geometry that was built, and are corrected rather than left standing:
   >
   > - **"Replaceable" is wrong; "swabbable" is right.** The seat is a blind
   >   counterbore that opens only into the Ø22 chute bore, **26.050 mm** (beam
   >   A) and **20.050 mm** (beam B) above the chute mouth, and the Ø3.2 tunnel
   >   behind it cannot pass a Ø6 disc; `cad/BOM.md` bonds the disc with
   >   UV-cure adhesive. Replacement means reaching 20–26 mm up a Ø22 tube or
   >   destacking `retaining_plate_chute` — a workshop job, not a field action.
   >   **Swabbing from the chute exit is supported** (the window face is flush
   >   with the bore wall and nothing is proud of it: a Ø22.0 column on the
   >   chute axis measures 0.0000 mm³ against plate, windows and boards).
   > - **The 0.4 mm chamfered recess is NOT modelled.** The seat is
   >   straight-walled: Ø6.000 mouth, 1.000 mm deep, window face at
   >   |y| = 11.000, which is 0.417 mm outside the bore surface at the aperture
   >   chord and tangent to it at x = 32. A chamfer was modelled in rev-1 round
   >   6 and **withdrawn**, because the cone's rim is tangent to the Ø22 bore at
   >   exactly that point and the part exported with 22 open + 22 non-manifold
   >   edges. See `_run/rev1/BUILD-NOTES-r6.md` §6. Either this item or the seat
   >   has to change; today the document and the part disagree.

   *Residual:* a flush window is exposed to pellet impact where a recessed one is
   not. The 0.4 mm chamfered recess and the sacrificial-part strategy are the
   mitigation; B2 (2 000-pellet fouling run) shall inspect the windows for
   impact damage as well as for film.

6. **~~ECO-5: slope the aperture tunnels up 15°~~ — WITHDRAWN AS WRITTEN. It
   physically breaks the through-beam.** Both tunnels are collinear `Rot(X=90)`
   bores along y at a common z [V `dispenser.py` L1005-1017]. "Slope each tunnel
   15° up from the bore to the window" tilts the two in **opposite senses about
   the bore**: the emitter ray leaves its window at −15° in z and, over the
   27 mm from the emitter window (y = 16) to the far bore wall (y = −11), drops
   `27·tan15° = 7.2 mm` [D] — arriving ≈5.9 mm below a ±1.6 mm receiving
   aperture. **Received signal on both channels would be zero; the count sensor
   would not work at all.** The beam-clear self-test (§4.6) would fail on first
   power-up, so this is bench-discovered rather than flight-discovered — but it
   was dust mitigation 6 of 7 and it did not exist.

   *Root cause:* an anti-fines slope can only be applied to **one** side of a
   straight through-beam. A consistent single tilt makes one side self-clearing
   and the other self-fouling.

   **ECO-5 (revised): move the anti-fines feature into the horizontal plane —
   a lateral labyrinth step in each tunnel.** Offset the outer 2.5 mm of each
   Ø3.2 tunnel by 0.8 mm in x, leaving a 0.8 mm ledge that fines must climb over
   while the ±1.6 mm aperture still passes the on-axis ray. This is symmetric,
   so it works on both sides, and it costs nothing in a printed part. Alternative
   if bench testing shows the labyrinth restricts the beam: **slope only the
   receiver tunnel** and accept the asymmetry (a self-clearing receiver and a
   self-fouling emitter), or go to a same-side retroreflective head — a larger
   redesign not taken here.

   *Residual:* fines accumulation in the emitter tunnel is now mitigated only by
   the labyrinth (unproven) and by the 182× excess gain (genuinely large, and
   measured continuously by `beam_margin_pct`). Carried in §11.

7. **Antistatic bleed at the chute** (§3.6) — triboelectrically charged fines are
   the mechanism by which dust *sticks* to a window rather than falling past it.
   ASSUMPTION; now a gated bench item (B9).

**Scorecard, honestly.** Of the seven measures, two were broken as written
(ECO-4 unbuildable, ECO-5 beam-breaking) and one was overstated (measure 3).
All three are corrected above. The two that carry the dust story — carrier
modulation and 182× excess gain — were never in doubt and are the reason the
sensor survives the corrections.

### 4.6 Self-test and health telemetry (hardware requirements, not firmware)

The hardware shall make all of the following measurable, and the contract (§5)
requires them to be reported:

- **Beam-clear check** before every dispense: both channels at their clean-baseline
  level with no LED-off residual. Blocked at rest → `SENSOR_FOULED`, refuse.
- **Excess-gain measurement:** step the emitter current down until each channel
  drops below its detection threshold; the ratio to the factory-clean value is
  reported as `beam_margin_pct` per channel. Warn <20 %, fault <5 %. This is a
  *predictive* maintenance signal — the operator learns the windows need wiping
  before a sortie miscounts, which is the single most valuable thing this sensor
  can do in a dusty ranch operation.
- **Dark-current / LED-off reading** each cycle → detects a shorted PD or stray
  light leakage.
- Per-channel event log for the transaction: dark time, peak attenuation,
  inter-channel overlap.

### 4.7 Fallback preserved

The concept's capacitive/EFS ring fallback (research §4.3, the pharma answer to
dusty counting) remains buildable: the chute ID 22 and the widened bosses give
room for a ring electrode and a capacitance-to-digital front end without touching
the meter. Not designed here; the envelope is preserved deliberately.

---

## 5. Command interface contract

**This section is the deliverable that replaces the cut software phase.** It
defines what signal triggers a dispense of N and what feedback comes back. It
defines no implementation.

### 5.1 PWM (FMU_CH1) vs DroneCAN (CAN2) — the trade

| Criterion | FMU_CH1 PWM | DroneCAN on CAN2 | Ethernet (also present) |
|---|---|---|---|
| **Direction** | **FC → payload only** | bidirectional | bidirectional |
| **Count feedback** | **impossible in-band** | native | native |
| Command richness | pulse width, ~10 distinguishable codes | typed messages, N, sequence, flags | unlimited |
| Integrity | none (no CRC, no ack); a glitch is a dispense | 15-bit CRC, transfer IDs, acks | TCP |
| Determinism | hard real-time, no stack | ~ms, shared bus | ~ms, switch |
| FC/companion integration | Lua/param plumbing on the FC | already bridged to telemetry and Quiver Hub (ICD §7); companion computer is on the same bus | REST/WebSocket pipelines (ICD §7) |
| Payload cost | 1 pin, 1 resistor | transceiver + choke + TVS ≈ $3 | PHY + magnetics ≈ $8, ~1 W, static-IP admin |
| Port portability | channel differs per port (ICD §4) — CH1 only on the bottom port | same on all ports | same |
| Bus etiquette risk | none | must not add termination (ICD §4) | none |

**Decision: DroneCAN is the command and feedback interface. FMU_CH1 is an arm
discrete and a degraded backup trigger. Ethernet is not used.**

The decisive argument is one line: **CONTEXT requires the count to be verified
and reported; FMU_CH1 has no return path; therefore a PWM-only dispenser cannot
meet the requirement.** Everything else (CRC, sequence numbers, richer status)
is supporting evidence. Ethernet would meet it but costs a PHY, magnetics, ~1 W,
four of the nine harness conductors and a static-IP allocation for a payload
whose entire telemetry need is a few dozen bytes per target.

**DroneCAN gives integrity, not authorisation — and the earlier draft conflated
them.** The trade table correctly credits DroneCAN's 15-bit CRC and transfer IDs
under *Integrity*. Integrity means "the message that arrived is the message that
was sent". It does **not** mean "the sender was allowed to send it". CAN2 is
shared by all three payload ports plus the companion computer [V ICD §4], so
**any node on the bus — a misconfigured second payload, a babbling node, a
companion-computer software defect, or anything plugged into a side port — can
emit a well-formed `Dispense` request and release herbicide.** Nothing in the
protocol rejects it; the `Result` broadcast reports the release after the fact.

The earlier draft described `PWM_ARM` as a *mode*, which implies a mode in which
a CAN message alone suffices. **That mode is withdrawn for flight.**

> **`PWM_ARM` is MANDATORY in the flight configuration.** The dispense
> precondition is always **{K1 closed by the FC}** AND **{FMU_CH1 in the armed
> band, §5.5}** AND **{a valid CAN transaction}**. CAN-only operation is a
> **bench configuration**, exactly as PWM-only is already labelled a bench mode,
> and the two bench configurations shall be mutually exclusive with flight
> configuration in the operating procedure.

This is what makes the "three layers" claim of §0 true rather than aspirational,
and it restores the layer that DroneCAN's lack of authorisation removes: FMU_CH1
is a *physically separate wire from a different FC subsystem*, so a bus-side
defect cannot assert it. Additionally, `Dispense.seq` shall be **monotonic** and
shall be rejected (`REFUSED_STALE`) if it does not follow an ARM transition
within the last 60 s — a replayed or fabricated request from a stale bus capture
is then also rejected.

**What FMU_CH1 is actually good for**, given it is one-way and hard real-time:

1. **Arm/safe discrete + heartbeat.** The payload refuses to dispense unless CH1
   is in the armed band, and disarms (drops the motor eFuse EN) if CH1 is absent
   for >500 ms. This is a second, CAN-independent, physically separate inhibit
   alongside K1 — three layers: **CAN command**, **PWM arm**, **K1 power**.
2. **A dumb bench/field trigger** with no CAN tooling: one coded pulse =
   dispense 1. Explicitly a **degraded, non-compliant mode** (no verified-count
   reporting in band) — for bring-up and hangar testing. **It is disabled at
   boot and can only be enabled by an explicit CAN command that does not persist
   across a power cycle** (§5.5), so the arm wire and the trigger wire are not
   the same wire in any flight configuration.

### 5.2 DroneCAN interface

Node: one DroneCAN node, dynamic node-ID allocation, standard
`uavcan.protocol.NodeStatus` at 1 Hz, `uavcan.protocol.GetNodeInfo`. **No bus
termination is fitted** (ICD §4). Bit rate follows the bus (500 kbit/s or
1 Mbit/s); the MCU uses a **±10 ppm crystal**, because the STM32's internal
16 MHz RC (±1 % over temperature) does not meet CAN bit-timing tolerance.

Three vendor-specific data types in the project's DSDL namespace. **Their
numeric data-type IDs must be allocated in the project-quiver DSDL registry —
they are deliberately not invented here** (ASSUMPTION/TBD, closure = a PR to the
quiver DSDL namespace).

```
# --- service: request a dispense (transaction-scoped, idempotent, resumable) ---
arrow.dispenser.Dispense.Request
    uint16 seq          # transaction id, monotonic per target, assigned by the FC/companion
    uint8  count        # N, 1..10   (CONTEXT: usually 1..3)
    uint8  flags        # bit0 DRY_RUN (cycle without arming the motor rail)
                        # bits1-7 reserved, shall be zero
                        # NOTE: ACK_FAULT deliberately REMOVED -- see below
---
arrow.dispenser.Dispense.Response
    uint16 seq          # echoed
    uint8  result       # ACCEPTED | ALREADY_COMPLETE | RESUMING | BUSY
                        # | REFUSED_NOT_ARMED | REFUSED_FAULT | REFUSED_RANGE
                        # | REFUSED_STALE   (seq non-monotonic, or no ARM in 60 s)
    uint8  already_dispensed   # for this seq, from non-volatile memory
    uint16 estimated_ms        # time to completion, so the FC knows how long to hold station

# --- service: clear a latched fault. SEPARATE SERVICE, deliberately. ---
arrow.dispenser.ClearFault.Request
    uint16 ack_flags    # bitmask of fault_flags bits the operator acknowledges
    uint32 operator_id  # attributable: who cleared it
---
arrow.dispenser.ClearFault.Response
    uint16 remaining_flags     # bits that did NOT clear (condition still present)
    uint16 faults_since_ack    # count of fault assertions since the last successful clear
    uint8  result              # CLEARED | PARTIAL | REFUSED_CONDITION_PRESENT

# --- service: bench modes. NOT persisted; off after every reset. ---
arrow.dispenser.SetMode.Request
    uint8  mode         # FLIGHT (default at every boot) | BENCH_TRIGGER | LOW_POWER
    uint32 magic        # fixed constant; makes an accidental/garbled frame ineffective
---
arrow.dispenser.SetMode.Response
    uint8  mode_now
    uint8  result       # OK | REFUSED_ARMED | REFUSED_MAGIC

# --- broadcast: completion (published on completion, repeated 3x at 10 Hz) ---
arrow.dispenser.Result
    uint16 seq
    uint8  commanded
    uint8  dispensed_verified
    uint8  skips               # empty pockets indexed through
    uint16 fault_flags
    uint32 lifetime_count

# --- broadcast: status at 2 Hz, always ---
arrow.dispenser.Status
    uint8  state               # BOOT|IDLE|ARMED|DISPENSING|RECOVERING|FAULT|LOW_POWER
    uint16 fault_flags
    uint32 lifetime_count
    uint16 seq_last
    uint8  beam_margin_pct[2]  # per channel, §4.6
    uint8  disc_phase          # 3-bit Hall decode, §3.2 + ECO-8
    uint8  motor_rail_dv       # POST-eFuse 12VSW, 100 mV units (0..25.5 V)
    uint8  aircraft_rail_dv    # PRE-eFuse 12VSW, 100 mV units -- distinguishes
                               # "K1 open / F1 blown" from "my own eFuse is off"
    int8   temperature_c       # board / driver
    int8   motor_temp_c        # motor mount NTC, ECO-10
    uint8  boot_reason         # POR|BOR|IWDG|EXT_WDT|NRST|SOFT|UNKNOWN
    uint8  stopped_mid_move    # 0 = last shutdown was at PARK; 1 = mid-move (FRAM)
    uint16 faults_since_ack    # survives 12V_PL cycling; cleared only by ClearFault
```

**`motor_rail_mv_x100` is renamed `motor_rail_dv`.** The old name was ambiguous
(`mv_x100` in a `uint8` reads as "millivolts × 100", which would saturate at
25.5 mV); the working interpretation was always 100 mV units, and the name now
says so.

**`ACK_FAULT` is removed from `Dispense.Request` and given its own service.** In
the earlier draft, `flags` bit 1 cleared a latch on the same message that
commanded a dispense — so a **single CAN frame could clear a latched
`JAM_UNRECOVERED` and immediately command a dispense of the mechanism that had
just failed**. Clearing a safety latch and commanding a herbicide release are
different authorities and now require different messages. `ClearFault` also
carries an `operator_id`, so a cleared fault is attributable in exactly the way
§5.3 already argues the dispense count must be.

`fault_flags` bit assignment (frozen here; the numbering is the contract):

| bit | flag | meaning |
|---|---|---|
| 0 | `SENSOR_FOULED` | beam-clear self-test failed, or `beam_margin_pct` <5 % |
| 1 | `SENSOR_DEGRADED` | one channel <20 % margin, or channels disagree |
| 2 | `JAM_STALL` | expected Hall transition absent; recovery attempted |
| 3 | `JAM_UNRECOVERED` | recovery bounds exhausted (§2.7); disc parked; no further dispense |
| 4 | `EMPTY_OR_BRIDGED` | ≥8 consecutive skips (one full revolution, no pellet) |
| 5 | `MOTOR_RAIL_ABSENT` | **pre**-eFuse 12VSW absent → K1 open, or F1 blown (aircraft-side) |
| 6 | `PHASE_LOST` | Hall decode ≠ PARK at boot, or lost mid-sortie |
| 7 | `OVERCOUNT` | more valid events than commanded |
| 8 | `CHUTE_BLOCKED` | dark time >25 ms, or beam still dark after the fall window |
| 9 | `UNCOMMANDED_DROP` | a valid count event outside a dispense transaction |
| 10 | `OVERTEMP` | driver or board over temperature |
| 11 | `NOT_ARMED` | dispense requested while disarmed |
| **12** | **`MOTOR_EFUSE_OFF`** | pre-eFuse present, post-eFuse absent → my own limiter is off (EN low, current limit, or thermal latch-off) — **payload-side**, distinct from bit 5 |
| **13** | **`OVERCURRENT`** | ILM exceeded the §2.2 firmware threshold on either rail |
| **14** | **`DRIVER_CONFIG`** | TMC2209 register readback ≠ commanded (`IHOLD_IRUN`, `GCONF`, `CHOPCONF`, `VACTUAL`), §2.3 |
| **15** | **`MOTOR_OVERTEMP`** | motor-mount NTC >75 °C (ECO-10), §2.7 |

Bits 5 and 12 together give the diagnostic the split-rail architecture was
supposed to deliver: **the operator learns whether the problem is on the aircraft
or in the payload**, which is the difference between "check FMU_CH2 / F1" and
"send the payload to the bench".

### 5.3 Semantics — signal → "dispense N" → count feedback

The contract that matters is not the wire format, it is the meaning:

1. **`Dispense(seq, N)` means "ensure that a total of N pellets have been
   delivered for transaction `seq`".** It is not "index N times" and not "add N".
   The payload persists `{seq, commanded, dispensed}` in **FRAM** on every
   verified count.
2. **Idempotent.** A repeat of a `seq` already complete returns
   `ALREADY_COMPLETE` and dispenses nothing. This is not optional: DroneCAN
   requests can be retried, and a retry that re-doses a plant is a regulated
   over-application.
3. **Resumable — and the two rules that governed this were incoherent, so the
   resolution is now stated.** If power is removed mid-transaction (an explicit
   ICD §3 requirement) and the FC re-sends the same `seq`, the payload returns
   `RESUMING` and delivers only the remainder. **This is why the count lives in
   FRAM and not in flash:** an FRAM write is byte-atomic in ~150 ns, whereas a
   flash page erase takes tens of milliseconds and a power loss mid-erase can
   destroy the record — precisely in the scenario the record exists for.

   *The problem.* Clause 10 and §3.2 say the disc does not move on boot and that
   a non-PARK Hall decode forces `PHASE_LOST`, refuse-to-arm, ground
   intervention. But the disc is *moving* for 484 ms of each 634 ms cycle
   (§3.4), so a power loss mid-transaction lands mid-move **76 % of the time** —
   and lands in `PHASE_LOST`, where the resume path is unreachable. Resume
   therefore worked only for a power loss at park, which is the case where resume
   is least interesting. Both clauses were individually correct and jointly
   useless, and the contract did not say which won. B5 would have surfaced it, at
   which point the *contract* would have had to change rather than the firmware.

   *Resolution — option (a), adopted.* `PHASE_LOST` permits **one bounded,
   ground-authorised creep-to-park**:

   | Rule | Value |
   |---|---|
   | Trigger | explicit `ClearFault(PHASE_LOST)` from the ground — never automatic |
   | Motion | shortest path to PARK, ≤22.5°, at ≤90 °/s, IRUN 18 |
   | Count sensor | armed throughout (guaranteed by §2.4: emitters are always on) |
   | Permitted outcome | **may drop ≤1 pellet** (bounded by §3.2.1's geometry) |
   | Mandatory reporting | any event during the creep is reported as `UNCOMMANDED_DROP` and added to `lifetime_count`, and it **counts toward the interrupted transaction's N** — a pellet that left the aircraft was delivered |
   | After the creep | Hall decode must read PARK; if not, `JAM_UNRECOVERED`, no further motion |
   | Then | the interrupted `seq` may be re-sent and returns `RESUMING` |

   So the resume path is reachable in the common case, at the price of one
   explicitly-authorised, explicitly-reported, geometrically-bounded pellet. The
   alternative — option (b), resume limited to power loss at park — was rejected
   because it makes ground intervention the *normal* outcome of a mid-sortie
   power blip, which the ICD says to expect.

   *Supporting record:* `stopped_mid_move` and the in-progress move identifier
   are written to FRAM **before** each move starts, so on restart the payload
   knows which move it was in and can compute the shortest path to PARK rather
   than guessing. `boot_reason` is reported so the ground can tell a commanded
   power cycle from a brownout.
4. **A new `seq` while a transaction is running is rejected `BUSY`.** No queue,
   no implicit abort. The aircraft is hovering over one plant at a time.
5. **What counts as "dispensed":** a beam event passing the §4.3 gate
   (**≥9.7 ms**, not ≥6 ms) on at least one channel, with the other channel
   either agreeing or reporting itself degraded. **Conservative rule: anything
   that plausibly left the aircraft counts toward N.** For a herbicide,
   over-application is the regulated risk, so an ambiguous event is counted
   (preventing a re-dispense onto an already-dosed plant) and flagged
   `SENSOR_DEGRADED`. Under-dosing is recoverable by re-tasking; over-dosing is
   not.

5a. **What "verified" means, stated rather than implied.** `dispensed_verified`
   counts **objects whose chord dwell is consistent with a sphere of D ≥ ~10.5 mm
   at the nominal fall velocity**. It is not a measurement of pellet identity.
   Specifically: fines and fragments below Ø8 are *deliberately* uncounted; a
   fragment between Ø8 and Ø11 that is additionally slowed ≥7 % by wall rubbing
   *can* be counted as a pellet (§4.3 gives the quantified window). The failure
   direction is **under-dose**, which clause 5 itself identifies as the
   recoverable one. This is an open gap against CONTEXT's "exactly N pellets …
   VERIFIED"; it is carried in §11 and closed by B1, not written off.
6. **Skips are free and invisible to the caller.** No event after an index →
   index again. Eight consecutive skips → `EMPTY_OR_BRIDGED`.
7. **A recovery can never manufacture a count.** The sensor is 40 mm below the
   meter; reverse-oscillation cannot push a pellet past it. Any event during
   recovery is a real pellet that left the aircraft and is counted (and, if
   outside a transaction, flagged `UNCOMMANDED_DROP`).
8. **Faults latch in FRAM, and a power cycle does NOT clear them.** The earlier
   draft said "clearing requires `ACK_FAULT` **or a 12V_PL power cycle**" — but
   ICD §3 states that 12V_PL exists precisely so *"the FC can drop and restore the
   rail (e.g. to hard power-cycle a hung payload)"*, and §2.1 of this document
   lists that as a design rationale. **The FC's standard recovery for an
   unresponsive payload would therefore silently erase `JAM_STALL`,
   `JAM_UNRECOVERED`, `SENSOR_FOULED` and `UNCOMMANDED_DROP`** — the operator
   would lose the evidence that a jam occurred, lose the maintenance signal that
   `beam_margin_pct` was below 5 %, and be handed a payload that faulted for a
   physical reason but presents itself as healthy. That defeats the entire point
   of latching, in exactly the hot-restart-mid-jam case.

   **Normative:** `fault_flags`, `faults_since_ack`, `boot_reason` and
   `stopped_mid_move` are persisted in the **same FRAM** that already holds the
   transaction record (one more 8-byte structure; FRAM writes are byte-atomic in
   ~150 ns and the 12V_PL bulk cap gives **15 ms** of hold-up at 0.039 A [D:
   100 µF × 6 V ÷ 0.039 A], i.e. a **10⁵× margin** over the write time — the
   record survives a contact dropout comfortably). **`ClearFault` is the only
   clear path.** A latched fault whose *condition is still present* returns
   `REFUSED_CONDITION_PRESENT` and does not clear. `JAM_UNRECOVERED` and
   `PHASE_LOST` additionally gate the §2.7 recovery bounds and the clause-3
   creep-to-park, so a power-cycle-and-retry loop is not possible.
9. **Arming** requires all of: 12VSW present (pre- *and* post-eFuse), **PWM arm
   valid — mandatory in flight configuration** (§5.1), no unacknowledged fault,
   disc phase = PARK, beam-clear self-test passed, TMC2209 register readback
   matching (§2.3), motor NTC <75 °C.
10. **On boot the disc does not move** (§3.2), and no dispense occurs without a
    fresh request. Exception: the ground-authorised creep-to-park of clause 3.
11. **Driver configuration is verified, not assumed.** Before every transaction
    the MCU reads back `IHOLD_IRUN`, `GCONF`, `CHOPCONF` and `VACTUAL` and
    refuses on mismatch (`DRIVER_CONFIG`, bit 14). §2.3 explains why this is a
    detection layer on top of the R_SENSE physical bound, not a substitute.
12. **Recovery is bounded** by the attempt, time, duty and cool-down limits of
    §2.7. "Recovery exhausted" now has a definition.

### 5.4 Timing contract

| Quantity | Value | Basis |
|---|---|---|
| Release move (park → concentric) | ≤90 °/s | §3.4 accuracy budget |
| Dwell at concentric | ≥150 ms | 2.8× the 54 ms pocket-clear fall (r6 §3) |
| Return move (concentric → park) | ≤240 °/s | §3.4 electrical limit |
| Pellet transit, port to beam | 90 ms | `√(2h/g)`, h = 40 mm |
| Event **attribution** window after release-move start | 400 ms → else skip | 310 + 90 ms + margin. **This is a bookkeeping window, not an emitter gate** — the emitters run continuously (§2.4), so a beam event *outside* the window is not missed, it is classified as `UNCOMMANDED_DROP` |
| **Cycle per pellet** | **634 ms** | §3.4 |
| **N = 3 nominal** | **1.9 s** | reported in `estimated_ms` |
| **N = 3 with 2 skips** | **3.2 s** | the FC must hold station this long |
| Emitter drive step-up before the release move | ≥20 ms | 50 → 100 mA settle before dark-time measurement (§4.4) |
| Bounded recovery, max cumulative energised time | **4 s** per episode | §2.7 |
| PWM arm-band minimum hold | **200 ms** | §5.5 |
| `Dispense.seq` must follow an ARM transition within | **60 s** | §5.1, else `REFUSED_STALE` |

### 5.5 PWM (FMU_CH1) contract — secondary

**The armed band has moved, because the old one collided with the flight
controller's default output.** The earlier draft assigned **1400–1600 µs** to
ARMED/idle. **1500 µs is the near-universal FC servo trim / default for an
unassigned or newly configured output channel**, and FMU_CH1 is a low-numbered
channel likely to be touched by a remap. The payload would therefore **arm itself
as a side effect of the flight controller booting, or of a parameter reset, with
no operator action** — and `Status.state` would show `ARMED` with nothing
flagging "armed without being asked". Compounding it, the same wire carried both
the arm heartbeat and the dispense trigger, so the "three layers" of §5.1
collapsed to two on the PWM path: **one wire at 1700 µs armed *and* dispensed.**

**Revised band plan.** The safe band is now the one adjacent to every FC default,
and the armed band is a value the FC cannot produce accidentally:

| Pulse width | State | Note |
|---|---|---|
| **No signal**, or **≤1600 µs** | **SAFE** | covers 900/1000 µs disarm defaults, 1500 µs trim, and loss of signal |
| **1750–1850 µs**, held **≥200 ms** | **ARMED / idle** (heartbeat) | 250 µs clear of 1500; requires a deliberate channel configuration |
| **>1900 µs** | **SAFE** (invalid) | a saturated or failsafe-maximum output must not arm |
| any other width | **SAFE** | fail-safe by default |

- **Minimum-hold applies to the ARM band, not only to a trigger:** the input must
  sit inside 1750–1850 µs for ≥200 ms continuously before `ARMED` is entered.
- **Loss of signal >500 ms: disarm** (drop motor eFuse EN).
- **`ARMED` is reported and is auditable:** every ARM/SAFE transition is
  timestamped into the FRAM event log with `boot_reason`, so "armed without being
  asked" is at least *visible* after the fact even though the payload cannot know
  the operator's intent.

**PWM triggering is disabled at boot.** There are **no dispense codes on CH1 in
any flight configuration**. The bench trigger (`1900 + 50·(N−1) µs`, held
≥200 ms, edge-triggered) exists only in `BENCH_TRIGGER` mode, which:

1. is **off after every reset**, including a 12V_PL cycle;
2. is enabled only by an explicit `arrow.dispenser.SetMode` CAN command;
3. **is not persisted** — there is no way to ship a unit with it on;
4. forces the bay status LED to a distinct fast blink while active.

This is what keeps the arm wire and the trigger wire separate, so a single glitch
on CH1 can arm but cannot dispense.

**Electrical — the old clamp provided no noise immunity at all.** The specified
1 kΩ series + 3.3 V TVS bounds fault current (§2.4) but does not filter: 1 kΩ
into the pin's ~5 pF is a **5 ns** time constant, i.e. no rejection whatever of
pulses induced on 300 mm of unshielded 26 AWG routed near a chopper-driven motor
pair. **Add 1 nF from the pin side of the resistor to payload GND**: `1 kΩ × 1 nF
= 1 µs`, which is 1 000× shorter than the shortest legitimate pulse edge
separation and 1 000× longer than the induced-noise timescale. Cost $0.01.

- Full input network: **1 kΩ series + 1 nF to GND + 3.3 V TVS to GND**; input
  high-Z, tolerant of the pin being driven while the payload is unpowered.
- **Residual, admitted:** PWM has no CRC and a glitch inside the arm band for
  200 ms is an arm. After the changes above, arming still requires a sustained,
  out-of-default pulse width, and **dispensing additionally requires a CRC-checked
  CAN transaction and a closed K1**. K1 remains the only true backstop and is
  correctly described as such.
- **No count feedback exists on this path.** Local indication only (bay status
  LED). Reporting still happens on CAN if CAN is present. PWM-only operation does
  not satisfy the verified-count requirement and is a bench mode.

---

## 6. Connectors and wiring through the blind-mate

### 6.1 Blind-mate pin usage (10 circuits, ICD §5)

| Pin | ICD function | This payload | Conductor |
|---|---|---|---|
| 1 | ETH_RX+ | **not used** — pad not routed on the payload board | — |
| 2 | **12VSW** | motor rail → 12VSW eFuse | 26 AWG red |
| 3 | ETH_RX− | not used | — |
| 4 | **GND** | single return for both rails, CAN and PWM reference | 26 AWG black ×2 |
| 5 | ETH_TX+ | not used | — |
| 6 | **+12V (12V_PL)** | logic + sensing → 12V_PL eFuse | 26 AWG orange |
| 7 | ETH_TX− | not used | — |
| 8 | **FMU_CH1** | arm heartbeat / backup trigger, 1 kΩ + TVS | 26 AWG white |
| 9 | **CAN2_H** *(silk CAN1_P)* | TCAN1042, **no termination** | 26 AWG yellow, twisted |
| 10 | **CAN2_L** *(silk CAN1_N)* | TCAN1042 | 26 AWG green, twisted |

Payload-side board: the same Attachment Interface PCB V1.4, **pads-only
population** (U11–U20), 23.5 × 15.8 mm, mounted on the clip plate's own four M2
tabs inside the 16 × 24 shaft [V ICD §5, BUILD-NOTES-r6 §1]. Harness leaves via
**Molex J1 (2077601281 header / 2045231201 receptacle, 1.25 mm pitch,
12 circuits)**; J1 doubles the power and ground circuits for current capacity, so
**both crimps of each doubled net shall be populated** — a 1.25 mm-pitch contact
is ~1 A class, and doubling halves the harness contact resistance. Exact J1 pin
order per the Attachment Interface PCB README (ICD §5) — not reproduced here
because it was not independently verified for this document.

### 6.2 In-payload connectors

| Link | Connector | Circuits | Note |
|---|---|---|---|
| Aircraft harness → main board | JST **GH** 1.25 mm, SM07B-GHS-TB / GHR-07V-S | 7 | positive latch; enters the bay through the modelled 4 × 16 × 9 cutout on the −X face [V L1066] |
| Main board → stepper | JST **PH** 2.0 mm, B4B-PH-K-S / PHR-4 | 4 | PH for the 0.8 A motor current (GH is 1 A class and marginal) |
| Main board → motor NTC (ECO-10) | JST GH, 2 | 2 | NTC pair; may share the PH shell only if a 6-way PH is used — **keep it separate**, the NTC is a high-impedance analog node next to the chopper leads |
| Main board → Hall set (ECO-8) | JST GH, 6 | 6 | 3V3, GND, HALL_A, HALL_B, **HALL_C**, spare — was 4 |
| Main board → emitter board | JST GH, 4 | 4 | 5 V, GND, LED1, LED2; **ESD array at both ends** (§3.6) |
| Main board → receiver board | JST GH, 6 | 6 | 5 V, GND, TIA_A, TIA_B, shield, spare; **ESD array at both ends** |

**ECO-6:** the bay has **one** modelled cable cutout. It needs three entries
(aircraft harness on −X; motor and sensor cables on the +Y inboard face) with
silicone grommet seats. Target ingress class **IP54** with a 3 mm closed-cell
gasket under the lid — *target*, not a verified rating.

### 6.3 Harness routing and the cable-channel fit check

**Corrected 2026-08-07 (rev-1 round 5, integration critic N-i1).** The
"5 × 2.5 mm channel" below was the r6 geometry and has not existed since r7;
`CABLE_W`/`CABLE_DEEP` are dead constants. The route and the fit check are
restated here against the **measured** `*_r11` exports.

Path: blind-mate PCB (Z = −181.55, centre) → hollow stand-off neck (cavity
42.70 × 42.70 mm) → Ø6.000 slot through the neck's −Y wall → **Ø6.000 closed
tube along the top plate** (y −19 → −73) → **R8.0 swept elbow** (r10's elbow
was solid printed material; measured r11: no solid point on either bore axis or
on the elbow centreline) → Ø6.000 vertical spigot → Ø11.000 hopper-side conduit
→ Ø7.400 bay riser socket. Harness coverage measured by lateral ray-casting on
the exported meshes: **94.6 % of a 484.84 mm run**, the uncovered 26.17 mm
being the two deliberate flexible joints (bay → cartridge service loop 14.76 mm,
motor flying leads 4.40 mm) plus 4.00 mm at the neck-wall slot.

**Fit [M, on the exports]:** the tightest section is the **Ø6.000 = 28.27 mm²**
top-plate conduit, not 12.5 mm². 9 × 26 AWG PTFE (OD ≈ 1.05) = 7.79 mm² =
**27.6 % fill**; all **12 circuits = 10.4 mm² = 36.8 %**, so the r6 conclusion
("all 12 circuits would not fit") is **reversed by the real section** and is no
longer an argument against Ethernet. What *is* still true, and is a shipped
assembly constraint: the **Molex 12-circuit 1.25 mm-pitch shell (≈16.7 × 5.8 mm,
diagonal 17.68 mm) does not pass a Ø6.0 bore and cannot turn the elbow**, so the
harness is pulled through as loose crimped terminals (≈2.1 × 1.0 mm each) and
J1 is populated at the neck after routing. No conduit is openable.

**Voltage drop [D]:** 26 AWG = 0.134 Ω/m; 300 mm run, 700 mm round trip;
at the 0.30 A worst case → **28 mV** on the motor rail, 14 mV on logic.
Negligible; 26 AWG is chosen for the Molex crimp range and flexibility, not for
current.

**Practices:** CAN pair twisted ≥1 turn/25 mm, run separately from the motor
pair; service loops at both ends; the harness is **internal to the payload and
never mated in the field** — the field-mated interface is the gold spring-pin
blind-mate, which needs a wipe procedure and a dust cap in the operating manual.

---

## 7. PCB set

| Board | Size | Layers | Contents | Mounting |
|---|---|---|---|---|
| **Main** | 42 × 34 mm | 4 | MCU, FRAM, CAN, TMC2209, both eFuses, buck, LDO, connectors, status LEDs, Tag-Connect SWD | vertical in the bay (interior 46 × 22 × 38), 4 × M2.5 standoffs to printed bosses (**ECO-7**: bosses are not yet modelled) |
| **Emitter** | 18 × 12 mm | 2 | 2 × TSAL6200, 2 × current sink, ESD array | in the widened +y boss (ECO-3), **clamp-retained (ECO-12)**; the two LEDs sit **6.0 mm apart in x and 6.0 mm apart in z** (ECO-3 + ECO-9) |
| **Receiver** | 18 × 12 mm | 2 | 2 × VBPW34FAS, OPA2320 dual TIA, ESD array | in the widened −y boss; PDs on the same x/z grid, so each beam stays a straight chord along y |
| **Blind-mate** | 23.5 × 15.8 | 2 | vendor design, pads-only population + J1 | clip-plate M2 tabs (vendor feature) |

Environment: all boards **conformal coated** (acrylic, e.g. MG Chemicals 422B) —
the payload's own cargo is a friable herbicide and the bay is not hermetic.
Ground: solid pour, star at the eFuse outputs, motor return routed to the bulk
cap and not through the analog section. Keep the TIA inputs <10 mm of trace and
guard-ringed (that is why the TIAs are at the chute, not in the bay).

### 7.1 Vibration and shock — four flagged items, none previously qualified

This document already knows vibration matters: §3.1 rejects plug-in stepstick
modules as "a known vibration failure on airframes". But the bench-test plan
B1–B7 contained **no vibration or shock test at all**, while four items in the
design are vibration-sensitive and unqualified. The payload hangs 180 mm below
the airframe on spring-pin blind-mate contacts, which is close to the worst
possible mounting for all four.

| # | Item | Failure mode and why it matters | Requirement added |
|---|---|---|---|
| a | **9 loose-installed disc magnets** | A migrated magnet lands in the 1.0 mm disc-rim shear gap or the pellet path → a hard jam **plus** loss of the Hall decode that the entire safe-state argument (§3.2) rests on. Retention method is not specified in this document or credited to the mechanical BOM. | **Specify retention explicitly**: 0.05 mm diametral interference in the Ø3 pocket **plus** a retained bead of Loctite 480 or equivalent, cured, with a pull-test on the first article. Levied on the mechanical BOM as **ECO-11**. |
| b | **Sensor PCBs retained by a single M3 grub screw bearing on the board** | A grub point-loading a PCB edge frets, can crack the board, and shifts the optical alignment that the ±3.0 mm chord geometry depends on. | Replace the point contact with a **nylon-tipped grub (or a 0.5 mm PTFE pad) bearing on a captured clamp plate**, so the load is distributed and the board is not the bearing surface. The re-seatable-without-glue property of the r6 design (`dispenser.py` L1013-1016) is preserved. |
| c | **Gold-on-gold spring-pin blind-mate carrying 0.34 A under continuous vibration** | A textbook fretting-corrosion site. Intermittent 12V_PL produces repeated MCU brownouts mid-dispense — precisely the scenario the FRAM resume semantics exist for, and (before §5.3 clause 3 was fixed) precisely the scenario `PHASE_LOST` blocked recovery from. | **Monitor it:** `aircraft_rail_dv` is sampled at 1 kHz and any excursion below 10 V for >1 ms is logged and counted. **Maintain it:** a wipe procedure and a dust cap in the operating manual (§6.3 already requires this) with a stated inspection interval set by B8. |
| d | **Main board, 42 × 34 mm on four M2.5 standoffs** | Unqualified first-mode frequency; a resonance coincident with rotor/blade-pass orders would fatigue the QFN solder joints and the tall bulk caps. | Resonance survey in B8; if the first mode is below 500 Hz, add a fifth central standoff or stake the tall parts. |

**B8 (new, gating): random vibration + shock.** A generic multirotor profile
(state it in the test plan; a resonance survey 20–2000 Hz plus 30 min/axis random
is enough for a first article) with the payload fully loaded to 250 pellets, plus
a landing-shock pulse. Pass criteria: no magnet migration, no change in
`beam_margin_pct` >5 %, no `aircraft_rail_dv` dropout events, no cracked joints
on X-ray or visual, and a functional dispense after each axis.

**One genuine strength worth stating, since it falls out of the same analysis.**
The 12V_PL hold-up is `100 µF × 6 V ÷ 0.039 A = 15 ms` [D] against a **150 ns**
FRAM write — a margin of 10⁵. **A blind-mate contact dropout cannot corrupt the
count record.** That is a real property of this architecture and the earlier
draft never computed it.

---

## 8. BOM with prices

Prices are **1-off** distributor prices, August 2026. `[V]` = seen on a
distributor/vendor page during this design (source in §10); `[E]` = estimate from
the same class of part, to be replaced at quote time. Motor listed separately
because it is already in the mechanical BOM (`../cad/BOM.md`).

### 8.1 Actuator

| Item | Part | Qty | Unit | Ext | Basis |
|---|---|---|---|---|---|
| Geared stepper | StepperOnline **14HS13-0804S-PG5** (NEMA 14 + 5.18:1) | 1 | $36.77 | $36.77 | [V] oyostepper listing; StepperOnline lists $34.92 |
| Driver | Analog Devices/Trinamic **TMC2209-LA-T** (QFN28) | 1 | $3.20 | $3.20 | [E]; LCSC $1.59 [V] |

### 8.2 Power

| Item | Part | Qty | Unit | Ext | Basis |
|---|---|---|---|---|---|
| eFuse (12VSW 0.60 A, 12V_PL 0.50 A) | TI **TPS259540DSGR** (part-number correction, §2.2) | 2 | $2.60 | $5.20 | [E] |
| Watchdog + supervisor | TI **TPS3823-33DBVR** | 1 | $0.75 | $0.75 | [E] |
| 5 V buck module | Traco **TSR 1-2450** (6.5–36 V in, 5 V 1 A) | 1 | $6.15 | $6.15 | [V] DigiKey |
| 3V3 LDO | Diodes **AP2112K-3.3TRG1** | 1 | $0.42 | $0.42 | [E] |
| Rail TVS | **SMAJ13A** | 2 | $0.35 | $0.70 | [E] |
| Bulk capacitor | Panasonic **EEH-ZA1V101P** 100 µF 35 V hybrid, 125 °C | 2 | $1.15 | $2.30 | [E] |

### 8.3 Digital / comms

| Item | Part | Qty | Unit | Ext | Basis |
|---|---|---|---|---|---|
| MCU | ST **STM32G431KBT6** (LQFP32, FDCAN, 4 MSPS ADC) | 1 | $5.83 | $5.83 | [V] DigiKey |
| CAN transceiver | TI **TCAN1042HGVDRQ1** (±58 V bus fault, power-off high-Z) | 1 | $1.74 | $1.74 | [V] DigiKey |
| Crystal | Abracon **ABM8-16.000MHZ-B2-T**, ±10 ppm | 1 | $0.60 | $0.60 | [E] |
| Non-volatile count | Fujitsu **MB85RC64TA** I²C FRAM | 1 | $1.35 | $1.35 | [E] |
| CAN ESD | ON **NUP2105L** | 1 | $0.45 | $0.45 | [E] |
| CAN common-mode choke | TDK **ACT45B-101-2P-TL00** | 1 | $0.85 | $0.85 | [E] |

### 8.4 Sensing

| Item | Part | Qty | Unit | Ext | Basis |
|---|---|---|---|---|---|
| Hall switch (**replaces DRV5032**, §3.2; **3rd added by ECO-8**) | TI **DRV5023BIQDBZR** continuous-time | 3 | $1.30 | $3.90 | [V] DigiKey range $1.18–1.63 |
| Motor-mount thermistor (ECO-10) | Murata **NCP18XH103F03RB** 10 kΩ NTC | 1 | $0.15 | $0.15 | [E] |
| Sensor-harness ESD arrays (§3.6) | **ESD9B5.0ST5G** class, ≤5 pF | 6 | $0.20 | $1.20 | [E] |
| Magnets | supermagnete **S-03-02-N** Ø3 × 2 N45 | 9 | $0.30 | $2.70 | [E] |
| IR emitter | Vishay **TSAL6200** 940 nm | 2 | $0.50 | $1.00 | [V] DigiKey |
| Photodiode | Vishay **VBPW34FAS** (daylight-blocking filter) | 2 | $1.50 | $3.00 | [E]; BPW34 $1.34 [V] |
| TIA | TI **OPA2320AIDR** | 1 | $2.45 | $2.45 | [E] |
| Windows (ECO-4) | PMMA Ø6 × 1 mm disc | 4 | $0.25 | $1.00 | [E] |

### 8.5 Interconnect

| Item | Part | Qty | Unit | Ext | Basis |
|---|---|---|---|---|---|
| Blind-mate PCB, payload side | project-quiver **Attachment Interface PCB V1.4**, pads-only, fab + assembly | 1 | $6.00 | $6.00 | [E] |
| Molex receptacle | **2045231201** (12 ckt, 1.25 mm) | 1 | $1.15 | $1.15 | [E]; part [V] DigiKey |
| Molex crimps, 26 AWG | 1.25 mm series | 12 | $0.12 | $1.44 | [E] |
| Aircraft harness connector | JST **SM07B-GHS-TB** + **GHR-07V-S** + crimps | 1 | $2.20 | $2.20 | [E] |
| Motor connector | JST **B4B-PH-K-S** + **PHR-4** + crimps | 1 | $1.10 | $1.10 | [E] |
| Sensor connectors | JST GH 6-ckt sets | 2 | $1.50 | $3.00 | [E] |
| Wire | 26 AWG PTFE, 7 colours, 2 m | 1 | $6.00 | $6.00 | [E] |
| Sleeving / heatshrink / RTV | — | 1 | $4.00 | $4.00 | [E] |

### 8.6 Boards and passives

| Item | Qty | Unit | Ext | Basis |
|---|---|---|---|---|
| Main PCB, 4-layer 42 × 34 (proto qty 5, per unit) | 1 | $9.00 | $9.00 | [E] |
| Emitter + receiver PCBs, 2-layer | 1 | $4.00 | $4.00 | [E] |
| Passives, 0402/0603/0805, ~75 placements | 1 | $8.35 | $8.35 | [E]; includes **2 × 0.50 Ω 1 % 0805 low-TCR sense (§2.3)**, the VREF 10 k/10 k divider, the EN pull-down and ENN pull-up, two R_ILM, four rail-divider resistors, and the CH1 1 nF. The 0.05 Ω shunt and its current-sense amplifier are **deleted** (§3.3) |
| M3 × 4 grubs, standoffs, misc hardware | 1 | $1.50 | $1.50 | [E] |

### 8.7 Totals

| | |
|---|---|
| Electronics, excluding motor | **$92.68** |
| **Total including geared stepper** | **$129.45** |
| *Delta vs the pre-review draft* | *+$4.75 — watchdog $0.75, third Hall $1.30, motor NTC $0.15, sensor ESD arrays $1.20, passives $1.35* |
| Consumables not per-unit | conformal coat ~$15/can, thermal gap pad ~$8/sheet |

**Mass [J, estimate]:** main board 16 g · sensor boards 2 × 3 g · harness +
connectors 27 g (third Hall + NTC conductors) · magnets 9 × 0.13 g ≈ 1.2 g ·
misc 5 g → **≈55 g**, inside the r6 ledger's 65 g "electronics + wiring" line,
so no mass-budget impact. ECO-1 (aluminium lid) is +1.4 g; ECO-3 (widened
bosses) +6 g; ECO-8 (third Hall cavity) ≈0 g; ECO-9 (beam stagger) 0 g; ECO-10
(NTC) ≈0 g — all fit inside the ledger's contingency. The motor's own mass
should be corrected from the ledger's 310 g ASSUMPTION to the vendor's
**290 g** [V].

---

## 9. Open issues, ECOs and bench tests

### ECOs raised against the r6 CAD

| # | Change | Why | Est. impact |
|---|---|---|---|
| **ECO-1** *(revised)* | `bay_lid` in 1.5 mm 6061, **light-anodised or white-painted (α ≤ 0.4, ε ≥ 0.8)**, driver gap-padded to it; and a light external finish on the whole payload | Parked-in-sun wall temperature is **77.5 °C** against CF-PETG Tg 80 °C once solar gain is included (§2.6). Bare aluminium (ε ≈ 0.1) would make it *worse* | +1.4 g |
| **ECO-2** | Assert in `dispenser.py` that a pocket magnet sits under the 112.5° Hall at park; rename the Halls A/B | The static safe-state decode (§3.2) depends on it and is currently incidental | 0 |
| **ECO-3** | Sensor bosses `Box(12,12,14)` → `Box(20,12,14)`; two Ø3.2 apertures at x = 29 and 35 | Single centred beam has a disqualifying 5.2–14.7 ms dark-time spread (§4.2) | +6 g, motor clearance improves 1.4 → 4.4 mm |
| **ECO-4** *(revised — original was unbuildable)* | Ø6 × 1 mm PMMA window at the **bore face (y = ±11)** in a 0.4 mm chamfered recess, **not** in the component pocket | At the pocket the fouling surface is the window's *inner* face at the bottom of a sealed blind hole behind the sensor board — the opposite of field-wipeable, and it destroys the r6 swab-out path (§4.5) | +0.5 g |
| **~~ECO-5~~** *(withdrawn as written; replaced)* | ~~Slope the aperture tunnels 15° up from the bore~~ → **lateral labyrinth step (0.8 mm offset over the outer 2.5 mm of each tunnel)** | The 15° slope tilts the two collinear tunnels in **opposite** senses and drops the ray **7.2 mm** over the 27 mm path — zero received signal on both channels (§4.5) | 0 |
| **ECO-6** | Two more grommeted cable entries (motor, sensor) on the bay's +Y face | Only one entry is modelled (§6.2) | ~0 |
| **ECO-7** | Four M2.5 board standoff bosses inside the bay | No PCB mounting is modelled | +2 g |
| **ECO-8** *(new)* | **Third DRV5023** on the r = 42.5 mm circle, angle to be chosen and asserted in CAD | The 2-bit decode maps "stopped mid-move with the port leaking" and "a Hall has failed" onto the same code (0,0) — opposite responses, indistinguishable (§3.2) | +$1.30, ≈0 g |
| **ECO-9** *(new)* | **Stagger the two chord beams 6.0 mm vertically** (A at +3.0 mm, B at −3.0 mm and 6 mm lower); x-offsets unchanged | Dark-time midpoints then give a **size- and position-independent per-event velocity** (±1.7 %), converting the count from a dwell test into a measurement and closing the 18 % wall-rubbing ASSUMPTION (§4.3) | 0 — fits the 14 mm boss height |
| **ECO-10** *(new)* | 10 kΩ NTC bonded to the motor mounting face | Sustained recovery at IRUN 31 puts the motor case at ~95 °C against CF-PETG Tg 80 °C; there was no motor thermal sensing at all (§2.7) | +$0.15 |
| **ECO-11** *(new, mechanical BOM)* | Specify disc-magnet retention: 0.05 mm interference **+** cured retaining compound, with a first-article pull test | 9 loose magnets, unqualified for vibration; a migrated magnet is a hard jam **and** loss of the safe-state decode (§7.1a) | 0 |
| **ECO-12** *(new)* | Replace the point-contact M3 grub on the sensor bosses with a nylon-tipped grub or a captured clamp plate | A grub point-loading a PCB edge frets and shifts the optical alignment the chord geometry depends on (§7.1b) | ≈0 |

### Open issues / ASSUMPTIONS to close

1. **Motor vendor data conflict** — StepperOnline's PG5 page (14 N·cm / 1.0 A /
   3.2 Ω / 4.5 mH / backlash ≤3°) vs the datasheet and oyostepper (18 N·cm /
   0.8 A / 6.8 Ω / 10 mH / ≤1°). Every current, torque and speed number in §2–3
   scales with this. **Close by measuring the delivered motor** (winding R with a
   meter, holding torque on a beam and scale).
2. **The 41 N crush / 0.36 MPa pellet strength** is class-derived (r6 §2.2,
   US4172714). The recovery ceiling (R_SENSE = 0.50 Ω → 20.5 N) is set 2.0× under
   it. IFDC S-115 on real pellets moves the limit — and because the ceiling is now
   a resistor rather than a register (§2.3), moving it is a **board change**, which
   is the intended trade: harder to get wrong in the field, harder to tune on the
   bench. B3 shall confirm 0.50 Ω is right before the boards are released.
3. **DRV5023 Bop by suffix** — confirm at order time (§3.2). All options pass at
   65 mT.
4. **DroneCAN data-type IDs** must be allocated in the project-quiver DSDL
   namespace; §5.2 defines the payloads, not the numbers.
5. **TMC2209 VCC_IO/VS power-up ordering** — mooted by MCU-controlled eFuse EN
   (§2.2), but confirm against the datasheet before layout.
6. **eFuse and several passive prices are estimates** — re-quote before ordering.
7. **Antistatic bleed effectiveness** (§3.6) is unproven — now gated by B9.
8. **IP54 is a target, not a rating.**
9. **ICD change request: FMU_CH2 / K1 default state is unspecified** (§2.8). The
   only non-firmware interlock in the chain has an undefined behaviour at FC
   boot, FC reboot in flight, RC failsafe and FC parameter reset. **Close by a PR
   to project-quiver against ICD v1.0-draft §3.** Until it is closed, the
   payload-side EN pull-down is the sole compensation and is safety-critical.
10. **ECO-8's third-Hall angle is not yet chosen.** It depends on the pocket-magnet
    phase that ECO-2 is verifying. Close by deriving it in `dispenser.py` with an
    assertion that all four motion states and every single-Hall stuck-at fault
    produce distinct codes.
11. **Ground albedo 0.25** in the §2.6 solar model is an ASSUMPTION (dry
    caliche/grass). It affects only the 0.28 W reflected term, i.e. ~2 K.
12. **`ESD9B5.0ST5G` capacitance and the OPA2320 loop stability with 80 pF of
    source capacitance** are estimates — verify the compensation on the bench
    before the sensor boards are released (B2).
13. **The TPS3823 brownout threshold must sit below the AP2112K dropout** so the
    supervisor asserts before the 3V3 rail leaves regulation — confirm at part
    selection.

### Bench tests that gate the build

| # | Test | Freezes |
|---|---|---|
| B1 | Dark-time survey: ≥200 drops of real pellets (whole, chipped, dusty) **plus ≥100 deliberately fractured Ø7–10 mm pieces**, through the ECO-9 staggered two-chord head, logging per-event `v`, `r`, `x₀` | the §4.3 gate (**now 9.7/25 ms**); the **measured** wall-rubbing velocity distribution that replaces the 18 % `[J]` allowance; and the §11-R1 residual |
| B2 | Fouling run: count 2 000 pellets with deliberate fines loading, logging `beam_margin_pct`; **plus AFE linearity across 20–100 mA at 25 °C and 60 °C, plus window impact inspection** | the maintenance interval, the warn/fault thresholds, the §4.4 front-end spec and the revised ECO-4 window |
| B3 | Motor characterisation (issue 1) + index-profile timing on the real gearbox **+ a case-temperature rise curve at IRUN 31 to steady state** | §3.4 speeds, the 634 ms cycle, and the §2.7 motor thermal model |
| B4 | Hot soak: 60 °C ambient, 100 dispenses, bay interior thermocouple **+ an outdoor or solar-lamp soak at ≥900 W/m², parked and unshaded** | ECO-1 vs ASA-CF, and the §2.6 parked-in-sun case an oven cannot reproduce |
| B5 | Power-cycle campaign: cut 12V_PL and 12VSW at every phase of a dispense, ×200 | the §5.3 clause-3 creep-to-park resolution, the FRAM record, and that **latched faults survive a 12V_PL cycle** |
| B6 | Hot-plug: mate/unmate the blind-mate 50× on a live CAN2 bus with another node talking | that the payload never corrupts the bus |
| B7 | Compass/EMI: log FC magnetometer with the dispenser cycling at 0.5 m and installed | §3.5 |
| **B8** *(new)* | **Random vibration + shock**, fully loaded to 250 pellets: resonance survey 20–2000 Hz, 30 min/axis random on a stated multirotor profile, plus a landing-shock pulse | magnet retention (ECO-11), sensor-board retention (ECO-12), main-board first mode, and blind-mate fretting — **four flagged concerns, previously unqualified** (§7.1) |
| **B9** *(new)* | **ESD**: IEC 61000-4-2 ±8 kV contact / ±15 kV air to the enclosure, chute mouth and blind-mate; plus a triboelectric run (2 000 pellets, dry, monitoring bleed current) | the §3.6 immunity claim and the antistatic-bleed ASSUMPTION (issue 7) |
| **B10** *(new)* | **Default-safe pin audit**: scope motor-eFuse EN and TMC2209 ENN through every row of the §2.8 table, including an unprogrammed MCU and a forced watchdog reset | that §2.8 is a measured property, not a schematic intention |

---

## 10. Sources

Internal (verified within this repository): `_run/CONTEXT.md` ·
`../../../interface/ICD.md` v1.0-draft §1–§6 · `_run/CONCEPT-pocket-wheel.md`
§2.4, §4, §7, §9, §10 · `_run/BUILD-NOTES-r6.md` §1–§4 and the round-6 critic
sections · `_run/RESEARCH-pill-counting.md` §4.1–§4.5 ·
`../cad/dispenser.py` (parameters and geometry cited by line) · `../cad/BOM.md`.

External (fetched during this design):

- [Vishay TSAL6200 datasheet](https://www.vishay.com/docs/81010/tsal6200.pdf) and [DigiKey listing](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/TSAL6200/1681339)
- [Vishay VBPW34FA/BPW34FA datasheet](https://www.vishay.com/docs/81127/vbpw34fa.pdf) · [BPW34 DigiKey](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/BPW34/1681149)
- [Vishay TSSP4038 (descope option) DigiKey](https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/TSSP4038/3789836)
- [TI DRV5032 datasheet](https://www.ti.com/lit/ds/symlink/drv5032.pdf) (sampled — why it is rejected) · [TI DRV5023](https://www.ti.com/product/DRV5023) · [DRV5023BIQDBZR DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/DRV5023BIQDBZR/5015732)
- [TI TPS2595 datasheet](https://www.ti.com/lit/ds/symlink/tps2595.pdf) · [TI TPS1663 (alternative)](https://www.digikey.com/en/product-highlight/t/texas-instruments/tps1663-power-limiting-efuse)
- [Traco TSR 1-2450 DigiKey](https://www.digikey.com/en/products/detail/traco-power/TSR-1-2450/9383780)
- [ST STM32G431KB](https://www.st.com/en/microcontrollers-microprocessors/stm32g431kb.html)
- [TI TCAN1042HGVDRQ1 DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/TCAN1042HGVDRQ1/5967638)
- [Trinamic TMC2209 datasheet](https://www.analog.com/en/products/tmc2209.html) · [TMC2209-LA-T DigiKey](https://www.digikey.com/en/products/detail/trinamic-motion-control-gmbh/TMC2209-LA-T/10232492)
- [StepperOnline 14HS13-0804S-PG5](https://www.omc-stepperonline.com/nema-14-stepper-motor-bipolar-l-33mm-w-gear-ratio-5-1-planetary-gearbox-14hs13-0804s-pg5) · [oyostepper listing (spec table used)](https://www.oyostepper.com/goods-283-Nema-14-Stepper-Motor-Bipolar-L=33mm-w-Gear-Ratio-5-1-Planetary-Gearbox.html)
- [Molex 2045231201 DigiKey](https://www.digikey.be/en/products/detail/molex/2045231201/12317095)
- [Banner Engineering — photoelectric tablet counting](https://www.bannerengineering.com/us/en/company/expert-insights/how-to-use-photoelectric-sensors-for-tablet-counting.html) · [Pepperl+Fuchs thru-beam in dusty environments](https://www.pepperl-fuchs.com/en-us/products/industrial-sensors/photoelectric-sensors/thru-beam-sensors-gp31261)

**Datasheet pages read directly for this revision** (the pin-level and
register-level facts in §2.2, §2.3, §2.8 and §3.1 come from these, not from
memory or from a vendor summary page):

- TI **TPS2595** SLVSE57C — §1 Features (current range 0.5–4 A), §6 pin
  functions (EN/UVLO description), §7.3 Recommended Operating Conditions,
  §7.5 Electrical Characteristics (`IEN` leakage, `GIMON`, `ILIMIT` vs `R_ILM`),
  §8.3.4 thermal shutdown, §9.2.2.1 `R_ILM` selection, device comparison table
  and orderable addendum.
- Trinamic/ADI **TMC2209** datasheet Rev 1.05 — §1 (internal step pulse
  generator; no ramp generator), §4 pin table (ENN = type `DI`, no internal
  pull; ENN-high = outputs floating), §5.2 register map (`IHOLD_IRUN` reset
  default IRUN = 31; `VACTUAL` 0x22), §9 sense-resistor selection and the
  `I_RMS` equation with `V_FS` = 325 mV default.

---

## 11. Residual risks (accepted, with mitigation)

Every blocking finding from the safety review is closed in the body of this
document except the items below. These are **accepted with mitigation**, not
deferred silently: each states what remains, why acceptance is defensible, what
detects it, and what would close it.

### 11.0 Disposition of the review findings

| Finding | Disposition | Where |
|---|---|---|
| No hardware default-safe state at the pin level | **CLOSED** — EN pull-down, ENN pull-up, external watchdog, full state table. Both pins confirmed from the datasheets to have **no internal pull** | §2.2, §2.8, §3.1 |
| ECO-5 breaks the through-beam | **CLOSED** — withdrawn as written, replaced by a lateral labyrinth | §4.5, ECO-5 |
| ECO-4 window is not field-wipeable and blocks the r6 maintenance path | **CLOSED** — window moved to the bore face | §4.5, ECO-4 |
| Top-hazard detector switched off for 99.9 % of the sortie | **CLOSED** — emitters continuous, 0.07 W | §2.4 |
| 6 ms gate discards the two-chord discrimination | **PARTIALLY CLOSED** — gate raised to 9.7 ms, ECO-9 stagger added. Residual **R1** | §4.3, R1 |
| Latched faults cleared by a routine 12V_PL cycle | **CLOSED** — FRAM-persisted, `ClearFault` split into its own service | §5.2, §5.3 cl. 8 |
| Motor thermal case never analysed; recovery unbounded | **CLOSED** — full analysis, bounded recovery, NTC. Residual **R9** on the input data | §2.7, ECO-10 |
| PWM arm band collides with the FC default | **CLOSED** — armed band 1750–1850 µs, PWM trigger disabled at boot, RC filter. Residual **R7** | §5.5 |
| K1 is a stop, not a safe state; exposure unbounded | **PARTIALLY CLOSED** — exposure bounded at ≤1 pellet with geometry, now detected and logged. Residuals **R2**, **R10** | §3.2.1 |
| Resume vs `PHASE_LOST` incoherent | **CLOSED** — bounded, ground-authorised creep-to-park adopted | §5.3 cl. 3 |
| eFuse limits 4× and 15× oversized | **PARTIALLY CLOSED** — 0.60 A / 0.50 A + ILM firmware thresholds. Residual **R5**: the part's floor is 0.5 A | §2.2, §2.4, R5 |
| IRUN "hardware limit" is a volatile register | **CLOSED** — R_SENSE 0.50 Ω + VREF divider makes the ceiling physical; readback added | §2.3 |
| No interlock requirement levied on the aircraft | **PARTIALLY CLOSED** — state table written, ICD change request raised. Residual **R6** | §2.8, issue 9 |
| DroneCAN has no authorisation; PWM_ARM optional | **CLOSED** — PWM_ARM mandatory in flight, seq monotonic + ARM-recency | §5.1 |
| Rail sense on the wrong side of the eFuse | **CLOSED** — pre- and post-eFuse dividers, bit 5 split, field renamed | §2.2, §5.2 |
| No ESD immunity level; sensor harnesses unprotected | **CLOSED** — levels stated, low-C arrays, bonding path, B9. Residual **R8** | §3.6 |
| No vibration or shock test | **CLOSED** — B8 added, four items specified (ECO-11, ECO-12) | §7.1 |
| Thermal model omits solar gain | **CLOSED** — four-term model; parked-in-sun is the binding case; finish spec added | §2.6 |
| Emitter-current reserve inconsistency; no AFE spec | **CLOSED** — 50/100 mA resolved, full front-end specification added | §4.4 |
| "TMC2209 has no motion generator" offered as the strongest safety argument | **REJECTED AS FALSE** — the part has `VACTUAL`, a UART-driven step generator. A narrower, true argument is substituted | §3.1 |

### 11.1 Register

**R1 — The count verifies objects, not pellets.** *(count integrity; severity:
under-dose, moderate)*
A fragment between Ø8 and Ø11 that is also slowed ≥7 % by wall rubbing produces a
dark time inside the pellet band. At the assumed 18 % worst-case slowing, 54 % of
Ø8 lateral positions are miscounted (§4.3). *Accepted because:* (a) the failure
direction is **under-dose**, which §5.3 clause 5 identifies as the recoverable
one — the regulated risk is over-application, and this failure does not cause it;
(b) CONTEXT states pellets are pre-filtered at load, so a Ø8 fragment requires a
pellet to break roughly in half *inside* the hopper; (c) the 6 ms → 9.7 ms change
removes the failure entirely at nominal velocity, where it was previously 85 %.
*Detected by:* per-event `v`, `r`, `x₀` logging (ECO-9) makes every miscount
auditable after the sortie. *Closed by:* **B1** with deliberately fractured
pellets — if the measured velocity distribution is tighter than 7 %, R1 vanishes.
*This remains an open gap against CONTEXT's "exactly N pellets … VERIFIED" and is
not written off.*

**R2 — Up to one pellet may be released by a mid-move stop.** *(accidental
dispense; severity: low, bounded)*
Opening K1, losing 12VSW, or an eFuse latch-off during the 484 ms of each 634 ms
cycle in which the disc is moving freezes it with a pocket possibly part-way over
the exit port. There is no stored energy to complete a return-to-park (0.63 J
needed, 7.2 mJ available). *Accepted because* the exposure is **geometrically
bounded at one pellet** — pocket pitch 45° versus a ≈7° release window means only
one pocket can ever be over the port (§3.2.1) — and the hopper cannot free-flow
behind it. *Detected by:* the count sensor is now armed continuously, so the drop
produces an `UNCOMMANDED_DROP` event and an FRAM record. *Mitigated by:* the
operating-procedure rule that K1 is an emergency kill and normal disarm waits for
`PARK`. *Closed by:* R10.

**R3 — A drop while 12V_PL is absent is undetectable.** *(accidental dispense;
severity: low)*
With the payload wholly unpowered there is no sensing of any kind. *Accepted
because* with 12V_PL absent the motor rail is also off (§2.8) and the disc is
static, so the only mechanism is vibration shaking a pellet through a port that
was already partly open — which requires R2 to have occurred first, and R2 is
recorded. *Closed by:* nothing available at reasonable cost; a mechanical
port closure (R10) removes the precondition.

**R4 — Fines in the emitter tunnel are mitigated only by the labyrinth and by
excess gain.** *(dust; severity: low)*
The withdrawn ECO-5 slope cannot be applied symmetrically to a straight
through-beam (§4.5). The replacement lateral labyrinth is unproven. *Accepted
because* the 182× excess gain tolerates 99.4 % attenuation and is *measured
continuously* as `beam_margin_pct`, so fouling is a scheduled-maintenance signal
rather than a failure; and the revised ECO-4 makes the fouling surface swabbable
from the chute exit. *Closed by:* **B2**.

**R5 — The 12V_PL rail's intermediate-fault regime is firmware-only.** *(fuse
coordination; severity: moderate)*
The TPS2595's specified current-limit range starts at **0.5 A** [V SLVSE57C §1],
which is 12.8× the 0.039 A load; the part cannot be programmed to the ~0.15 A the
load would justify. Between 0.12 A and 0.50 A the only protection is the firmware
ILM threshold, and the payload **cannot cut its own logic rail** — it can only
latch, refuse to arm and report. *Accepted because* the alternative is a second
part number and a second qualification for one rail, and because 12V_PL's own
worst case is 0.46 W in a bay budgeted for 1.2 W. *Detected by:* `OVERCURRENT`
(bit 13) plus the pre/post-eFuse dividers. *Closed by:* if a bench fault study
shows the regime matters, substitute a lower-range limiter on the logic rail —
this is a drop-in board change, not an architecture change.

**R6 — The aircraft-side default of FMU_CH2 / K1 is unspecified.** *(accidental
dispense; severity: moderate until the ICD is amended)*
K1 is the only non-firmware interlock and the payload cannot enforce its default
unilaterally (§2.8). *Accepted because* the payload-side compensation — the
100 kΩ EN pull-down, which is now treated as safety-critical and verified by B10
— means 12VSW appearing unexpectedly still does **not** energise the motor.
*Closed by:* **open issue 9**, a PR against ICD v1.0-draft §3. The ICD is a draft
and this relay was added for this payload, so the change is timely.

**R7 — PWM has no integrity check; a sustained in-band glitch arms.** *(accidental
dispense; severity: low after §5.5)*
*Accepted because* arming now requires a **sustained 200 ms pulse 250 µs away
from every FC default**, and because arming alone dispenses nothing — the trigger
codes are disabled at boot and require an explicit, non-persistent CAN command.
K1 remains the true backstop and is correctly described as such.

**R8 — An ESD-induced phantom count event is not detectable.** *(ESD / count
integrity; severity: low)*
A destroyed photodiode is caught by the LED-off dark-current reading (§4.6); a
single transient that mimics a pellet is not. *Accepted because* a phantom event
causes an under-dose (the recoverable direction, as R1), the two-channel
coincidence test rejects a transient on one channel only, and §3.6's low-C arrays
and bonding path attack the cause. *Closed by:* **B9**.

**R9 — The motor thermal numbers rest on an unresolved vendor data conflict.**
*(stall/thermal; severity: low)*
The 2.66 W figure derives from the 6.8 Ω / 0.8 A data set; the competing 3.2 Ω
set gives 1.25 W at the same current, i.e. **the quoted figure is the
conservative branch**. *Closed by:* **open issue 1** and **B3**, which now
includes a case-temperature rise curve.

**R10 — There is no mechanical return-to-park.** *(accidental dispense; severity:
low, and it is the root of R2 and R3)*
A light torsion return spring with an over-centre cam would make PARK the
mechanical rest state at *every* disc angle, and would make §2.3's "power-cycle
rest state is a mechanical property" argument true in general rather than only at
park. *Not adopted here because* it costs ≈0.05 N·m of the 0.39 N·m metering
budget and is a mechanical redesign this electronics document cannot specify
responsibly. **Owner: mechanical revision r7.** Recorded so it is a decision, not
an omission.

**R11 — IP54 is a target, not a rating**, and **R12 — the revised ECO-4 flush
window is exposed to pellet impact** where the original recessed one was not.
Both are mitigated by design (0.4 mm chamfered recess; sacrificial replaceable
disc) and both are inspection items in **B2**.
