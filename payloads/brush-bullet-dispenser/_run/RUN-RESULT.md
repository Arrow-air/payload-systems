# RUN RESULT — Brush Bullet Dispenser, rev-0 design package

## Workflow host record (added post-run by the host process)

Run ID `wf_240e82ad-f48`, completed 2026-08-07. Return value:

```json
{"winner":"pocket-wheel","tally":{"pocket-wheel":234,"psd-escapement":195,"dual-gate-airlock":163,"servo-shuttle":198},"cadRounds":6}
```

Usage: 59 agents launched, 54 completed, 5 errored; ~5.80 M subagent tokens;
1592 tool uses; 10 h 12 m wall clock.

The 5 errored agents all died on the same terminal API error — Opus 5's
safeguards flagged the request (false positives on ballistics/dispenser
wording; see support.claude.com/en/articles/16049681):

- `research:pill-counting` (its RESEARCH doc was still delivered by a retry path)
- `sim:attempt1`, `sim:attempt2`, `cad-simfix` — **this is why `sim/` was never
  built** (Phase 7 below)
- `packager` — first packaging attempt; the package below was assembled by a
  fallback path

Per-agent return values: journal at
`~/.claude/projects/-Users-hex/ddc62c4d-b746-41ab-8eef-deda400f98e8/subagents/workflows/wf_240e82ad-f48/journal.jsonl`.

Everything below this section was written during the run by the workflow's own
packaging phase.

---

Overnight run, 2026-08-06 18:44 → 2026-08-07 04:56. Every phase below is
summarised with its key numbers. Timestamps are file mtimes in `_run/`
(research docs were expanded mid-run, so their mtimes are later than the survey
that first cited them).

**Outcome:** shipped package assembled and committed on branch
`brush-bullet-dispenser` as `c123265`, author `thomasg <thomas@arrowair.com>`,
message `brush-bullet-dispenser: rev-0 design package (overnight run)`.
**Not pushed.** 172 files, the whole `payloads/brush-bullet-dispenser/` folder.

**Bottom line:** the design story is complete and the numbers are real, but the
CAD does not close. Round 6 failed three of four critics, an independent red
team reproduced three of its blockers on the exported geometry, and `sim/` was
never built. The package ships with those declared, not hidden — which was the
red team's own stated gate for calling it rev-0.

---

## Phase 1 — Research (5 docs, ~215 kB, last written 23:53–00:01)

| Doc | Mined for |
|---|---|
| `RESEARCH-seed-metering.md` | Kinze brush meters, celled plates, vacuum discs; the anti-bridging outlet rules |
| `RESEARCH-pill-counting.md` | Slat counters, vibratory + optical count; the dark-time gating philosophy |
| `RESEARCH-projectile-feeders.md` | Paintball force-feed; the jam-detect / reverse-oscillate pattern |
| `RESEARCH-bulk-dispensers.md` | Gumball machines, fish feeders; "the disc top *is* the sump floor" |
| `RESEARCH-drone-spreaders.md` | Existing UAV granule spreaders; **§1.3 the tebuthiuron pellet property data (US4172714)** |

**Key number, and the weakest link in the package:** pellet crush strength
**0.36 MPa / 41 N per whole pellet**, **class-derived from patent literature**,
not measured on the real product. Every torque margin in the design scales with
it. Closure: IFDC S-115 on real pellets.

## Phase 2 — Mechanism survey (19:02)

**17 candidates scored 1–5** on count potential / jam resistance / buildability /
mass / glove-serviceability → **4 champions** chosen for diversity of failure
mode, not score: rotary pocketed wheel, PSD nest+flapper escapement, servo
single-cavity shuttle, dual-gate airlock.

Rejected outright: augers and spinner spreaders (**count = 1/5, no notion of
count**), vacuum singulation (power/dust), pneumatic pod firing (power/friability).
Three rejected as mechanisms but **adopted as features**: Kinze compliant brush
wiper, pharmacy optical-count sensing philosophy, paintball jam-recovery pattern.

## Phase 3 — Concepts (19:08)

Four full concept documents, ~23 kB each: `CONCEPT-pocket-wheel.md`,
`CONCEPT-psd-escapement.md`, `CONCEPT-servo-shuttle.md`,
`CONCEPT-dual-gate-airlock.md`.

## Phase 4 — Trade study / judging (19:16)

Three judges (≈ count integrity / field ops / integration):

| Concept | J1 | J2 | J3 | **Total** |
|---|---|---|---|---|
| **pocket-wheel — WINNER** | 73 | 78 | 83 | **234** |
| servo-shuttle | 52 | 68 | 78 | 198 |
| psd-escapement | 70 | 55 | 70 | 195 |
| dual-gate-airlock | 63 | 42 | 58 | 163 |

Unanimous — first on all three ballots. Sharpest disagreement: servo-shuttle
spread **26 points** (J1 last at 52, *"the right thing to BUILD first and the
wrong thing to FLY"*; J3 second at 78 for drop-path cleanliness), which pushed it
to second overall despite losing two of three ballots. All three ballots
independently flagged the **±1 mm pellet-diameter ASSUMPTION** as load-bearing.
It is still open.

## Phase 5 — CAD, six rounds (19:48 → 03:08)

`cad/dispenser.py`, 2597 lines of parametric build123d with a self-verifying
harness; `cad/verify_exports.py`, 348 lines, re-measures the exports. Four
adversarial critics per round measuring the **exported geometry**.

| Round | interference | pellet-path | buildability | mass-budget | Root cause of that round's failures |
|---|---|---|---|---|---|
| r1 | 6 FAIL | 4.5 FAIL | 6 FAIL | 8.5 PASS | first geometry |
| r2 | 9 PASS | 5.5 FAIL | 5.5 FAIL | 9 PASS | **tangent unions** — 13 parts exported as 22 solids |
| r3 | 9 PASS | 6.5 FAIL | 6.5 FAIL | 9 PASS | **assembly kinematics** — roofed screws, sealed nut pockets, trapped brush |
| r4 | 9.5 PASS | 8 PASS | 7 FAIL | 8.5 PASS | **architecture** — agitator was a cartridge member (853 mm³ swept interference) |
| r5 | **4 FAIL** | 5 FAIL | 8.5 PASS | 9 PASS | **the clip plate was never mapped** |
| **r6** | **7 FAIL** | **5 FAIL** | **4 FAIL** | **8 PASS** | **the r5 fixes created three new blockers** |

**Every round's blockers were invisible to the previous round's harness.** Each
round's real deliverable was a new class of automated check: r3 added per-part
`solids()==1` connectivity, r4 added an insertion/tool-path harness (driver
corridors, nut columns, swept brush), r5 adopted **"no stand-in probes for
motion"** — every service motion is a swept union of the *actual exported
solids*.

**r5's instructive failure.** For four rounds the payload bolted to the clip
plate at (±6.5, ±10.5), "verified" by a Ø2.4 probe reading 0.775 mm³ against a
`v_cb < 5.0` threshold. The critic mapped the vendor STEP and found that pattern
sits **inside a 16 × 24 mm through-window** — the four screws carrying a 1274 g
loaded payload clamped **air**. Real holes: 4 × Ø2.96 at **(±19, ±19)**. Same
round: blind-mate pads **35 mm out of position in Y**, with the notes calling the
pedestal "shimmable" (shimming is in Z). Rule adopted: *a check whose only
possible outcome is "pass" is not a check.*

**The 23:03 fragment-jam directive.** r6's answer: 25° entry ramp (ceiling
10.24 mm at θ=129° → 1.50 mm at the PCD), 30° rigid deflector nose, brush wiper
with 6.25 mm free trim; load budget **190.7 mN·m** at the disc vs **390 normal
(2.1×) / 650 recovery**; **20.4 N at the pocket lip vs 7.5 N to shear a Ø6
fragment**, deliberately **2.0× under** the 41 N whole-pellet crush figure. The
pellet-path critic then **constructed the jam anyway**: a Ø5.0 fragment nested in
the measured pocket chamfer sits +1.80 mm proud, Ø6.0 sits +2.95 mm — inside a
**1.50–3.00 mm blind band** between the roof clearance and the nose, where only
compliant bristles touch. Jam still defeated, but by **crushing** (defence 2),
not by **rejection** (defence 1), which is what the notes claimed. One-parameter
fix, not applied: `NOSE_GAP` 3.00 → ≤1.50 mm.

### r6 measured results

| | |
|---|---|
| Envelope | X ±75, Y −90…+75, Z −366.4…−171.0 → **195.4 mm** stack, 150 × 165 mm plan |
| Ground clearance at rest | **181.5 mm** vs ≥40 required (4.5×); 176.5 mm with the gear foam fully crushed |
| Landing gear / props | 83.41 mm min separation; 152.5 mm vertical, **251.13 mm** true in-plan prop gap, zero plan overlap |
| Interference | 120 pairs, 38 bbox-overlapping boolean-checked, **0 collisions** |
| Pellet transit (Ø13 worst case) | **23 stations, 0.000 mm³**; 11/11 re-verified on the exports |
| Tightest true channel | pocket seat 14.50 mm = **1.15×** Ø13; governing arching dimension = the 26.50 mm outlet window = **2.04×** |
| Capacity | 963 cm³ usable → **422 pellets** worst-case barrel packing (498 g) / 587 sphere basis = **1.69× the 250 minimum** |
| Mass, empty | 993.1 g → **1092.4 g** carried (+10 % contingency) |
| **Mass, loaded @250** | **1387.4 g — 113 g under the 1.5 kg ceiling** (100 %-infill basis) |
| Mass, brim @422 | 1590.4 g (pellets above the 250 baseline are CONTEXT-exempt) |
| Mass, realistic infill (critic's independent rebuild) | **1257.5–1285.1 g** — 215–243 g of margin |
| Over-1.0 kg justification | 387.4 g, fully partitioned: stepper 310.0 + capacity oversizing 46.2 + latch ring 16.5 + fastening 15.2 |
| Printability | all 10 parts fit 220 × 220 × 250; support 0.0–8.9 %; ≥2 mm rule holds except the disclosed 30° wedge and TPU fingers |
| Meshes | 10/10 STEPs re-import as 1 solid; **9/10 STLs watertight** (`meter_housing` has a non-manifold edge at r 32.50, θ = 310.0° — exactly on the ramp bug) |
| CG | printed-parts centroid (1.73, −3.24, −257.05), **3.67 mm** in-plane offset from the mount axis |

### r6's three blockers (reproduced independently by the red team)

1. **θ = 310° roof through-slot.** The entry ramp was cut with a **half-space,
   not a sector** (`dispenser.py` ~L737-750), mirroring the 25° undercut at the
   far end. Sector booleans: 138.4/138.4 mm³ of roof at θ 309–310°, **2.2/138.4
   (0.14 mm mean) at 310–311°**. Point probes: **0.000 mm roof thickness at
   θ = 310.0° at r = 20.5 / 24.5 / 30 / 32 / 36 / 39.5 / 44 / 46.5** — an open
   slot from the pellet bed into the 1.50 mm metering arc **downstream of every
   rejection feature**, plus a 238 mm² vertical face facing the direction of
   travel.
2. **No torque path to the disc.** Bore measured **r = 3.06 mm at all 36 angles,
   both heights** — no D-flat, so the gearbox's 12 mm D-cut transmits nothing.
   The backup grub screw is a **buried blind hole** (void to r = 10.60, solid
   10.60→24.47).
3. **The gearbox cannot be bolted on.** Plate holes measured at θ = 45/135/225/315°,
   r = 16.8–19.9 (a 26 mm **square**) vs the datasheet's **4 × M3 on a Ø26 bolt
   circle** (r = 13 **on the axes**) — and moving them collides with the Ø22.20
   pilot bore, leaving a 0.3 mm web.

Plus: the drop-window derivation measures a window the pellet never uses —
support is lost **3.16–6.78° into the 22.5° index move (14–30 %)**, while the
disc is still turning, giving 0.126–0.25 m/s of lateral velocity → **0.16–0.32 m
of drift** over the 1.28 s fall from 8 m.

## Phase 6 — Electronics + interface contract (04:13)

`electronics/ELECTRONICS.md`, 2129 lines. Hardware and contract only — no
firmware, per the scope cut.

| | |
|---|---|
| **Worst-case power** | **4.05 W / 0.338 A** — 12VSW 3.57 W / **0.298 A**, 12V_PL 0.48 W / 0.040 A |
| **Steady state** (parked, sensor watching) | **0.40 W / 0.033 A** |
| Fuse margin | 6.7× below the aircraft's 2 A F1; 1.9× below the payload's own 0.60 A eFuse |
| **Stall behaviour** | with a chopper, input current **falls 19 % at stall** (0.298 → 0.242 A). A brushed equivalent would stall at **4 A** and blow a fuse *inside the aircraft* |
| Torque ceiling | **R_SENSE = 0.50 Ω** makes TMC2209 full scale = 0.63 A = 20.5 N at the pocket lip, **2.0× under the 41 N crush figure**. The "pellet grinder" state is unreachable by any firmware or UART fault — moving the limit is a board change |
| Count sensing | two chord beams at x = axis ± 3.0 mm, ECO-9 staggered 6.0 mm vertically. Guarantees **10.4–14.7 ms** for any pellet at any lateral position |
| **Count gate (corrected)** | **<9.7 ms fines · 9.7–25 ms one pellet · >25 ms `OVERCOUNT`/`CHUTE_BLOCKED`**. The shipped 6 ms bound would have counted a Ø8 fragment as a whole pellet in **85 % of lateral positions** |
| Cycle timing | **634 ms/pellet**; N = 3 nominal **1.9 s**, with 2 skips **3.2 s** |
| Contract | DroneCAN primary (`Dispense`/`ClearFault`/`SetMode` + `Result`/`Status`), transaction-scoped, **idempotent**, resumable, count in FRAM. PWM = arm only, and **PWM alone cannot satisfy the verified-count requirement** |
| Two authority separations forced in review | `ACK_FAULT` removed from `Dispense` (one CAN frame could clear `JAM_UNRECOVERED` *and* re-command the mechanism that just failed); PWM armed band moved **1400–1600 → 1750–1850 µs** (1500 µs is the FC's default trim, so the payload could arm itself on an FC boot) |
| Thermal | parked-in-sun wall **77.5 °C** vs CF-PETG Tg 80 °C; motor case ~95 °C under sustained recovery → ECO-1 (α ≤ 0.4 finish), ECO-10 (motor NTC) |
| BOM | **$92.68 excluding motor, $129.45 with it**; ≈55 g, inside the ledger's 65 g line |
| Raised | **12 ECOs** against the r6 CAD, **10 bench tests** (B1–B10), **13 open issues**, and **1 ICD change request** (FMU_CH2 / K1 default state at FC boot is unspecified) |

**None of the 12 ECOs were merged back into `cad/dispenser.py`.**

## Phase 7 — Simulation: NOT DELIVERED

`sim/` does not exist. CONTEXT asked for a Monte Carlo stating the honest wind
limit for the 1 m accuracy requirement.

Two reviewers integrated the ballistics themselves so the numbers exist
somewhere (**review computations, not a delivered sim**; 1.18 g Ø12 sphere,
Cd 0.47, quadratic drag):

- Fall from 8 m: **1.28–1.32 s**, impact ~11.3 m/s.
- Crosswind drift is a **bias**: **0.09 m per 1 m/s** — 0.19 m at 2 m/s, 0.47 m
  at 4, 1.00 m at 6.6, 1.37 m at 8.
- **The payload is not the accuracy driver — hover hold is.** P(within 1 m) at
  wind 0/3/5/8 m/s: **99.3 / 97.6 / 92.5 / 74.0 %** at 0.3 m 1σ hover, but
  **94.6 / 91.1 / 84.2 / 67.0 %** at 0.4 m — **the 90 % gate fails in still air
  at 0.4 m 1σ**.
- Honest wind limit for ≥90 % at 8 m AGL: **4.46 m/s (10 mph)**; **7.3 m/s** if
  released at 4 m.
- Because the drift is a bias, **aiming upwind cancels it** — a 30 % wind-estimate
  error at 8 m/s still gives **95.6 %**. That fix is *interface-side and in
  scope*, and `Dispense.Request` has no release-offset, no altitude advisory and
  no wind/hover gate.

Missed even by the briefed sim: **canopy interception** (the target is a shrub —
"within 1 m of the coordinate" is a proxy for "on soil in the root zone"),
**bounce/roll** at 11.3 m/s onto caliche, and **tumbling-Cd spread** (0.78 m vs
0.47 m of drift at 4 m/s).

## Phase 8 — Red team (04:47)

`RED-TEAM.md` — **21 numbered findings**, severity-ranked, each with a concrete
fix and a test. All measurements are the reviewer's own probes of
`cad/exports/*_r6.stl`, not restatements of the build notes.

**3 CRITICAL:**

- **RT-1** — shipping on a CAD round that failed 3 of 4 critics; three blockers
  reproduced independently (§Phase 5). *As drawn the mechanism cannot be
  assembled or driven.*
- **RT-2** — **no electrical connection to the aircraft**: pads at Z = −181.5 vs
  pin tips at −162.15 = **19.35 mm gap**; 8.85 mm even at the highest legal pad
  plane, against ≤2 mm of plunger travel. The notes offered "0.00 mm³ of payload
  inside the shaft" as proof the PCB *is* in the shaft — that metric is the proof
  it is not. The escape route is foreclosed (the clip half nests ≤0.54 mm over 8
  tested poses). **ICD-side escalation.**
- **RT-3** — **"verified count" exists only in a document describing hardware
  that isn't in the CAD**: ECO-3/ECO-9 never entered `dispenser.py` (still one
  Ø3.2 tunnel per side), and `BOM.md` still specifies the TSSP4038 receiver
  ELECTRONICS §4.4 rejects.

**4 HIGH:** RT-4 accuracy un-owned (above) · **RT-5 fill marks on a 40 %-packing
constant** — filling to the "250" rib (z = −222.6) with nominal pellets gives
**≈370 pellets / 438 g → ≈1530 g all-up, over the ceiling**; the brim (z = −196.9)
gives ≈638 / 753 g → ≈1845 g; no inventory telemetry at all · RT-6 black hopper +
PEG-bound pellets at ~74 °C in sun, BOM material contradicts ECO-2's α ≤ 0.4 ·
RT-7 the hopper cannot be sealed against a pellet that swells 2–3× irreversibly
when wetted.

**9 MODERATE:** RT-8 dust comes from below (open chute in the downwash) · RT-9
mass creep **41 % in six rounds** · RT-10 criteria re-based when they stopped
passing · RT-11 recovery torque may crush whole pellets, manufacturing the
fragments it recovers from · RT-12 no fines budget, and the running clearances
*are* the fines reservoir · RT-13 a 1.4–1.85 kg herbicide payload on a COTS clip
with no secondary retention and no rated load · RT-14 refill has no rest
position or tooling · RT-15 a live open issue deleted rather than closed ·
RT-16 mechanical vibration unqualified · RT-17 CG absent (computed by the
reviewer).

**4 LOW:** RT-18 proud fill ribs in the flow zone · RT-19 measurements quoted
with the sign of the claim · **RT-20 the "independent checker" is not
independent** · RT-21 count-contract residuals.

**Found sound:** the power/fuse coordination and §2.2–§2.8 interlock table
(*"the strongest work in the package"*), FRAM idempotency/resume semantics,
printability statistics (part volumes reproduce to **0.03 %**), ground and prop
clearance.

## Phase 9 — Gap review (04:39)

`GAP-REVIEW.md` — 7 gaps. Top three:

- **G1** — delivery accuracy un-owned end to end (§Phase 7).
- **G2** — **nobody did the mission arithmetic.** Quiver hover endurance
  **25–31 min** [verified, `/tmp/pq-main/docs/index.md:24`, never pulled by any
  agent]. At 1–3 pellets/target, 250 pellets = **83–250 targets ≈ 25–42 min** of
  flying — one hopper load is **1–3 batteries' worth**. The run answered "more
  capacity is good" with 422 pellets (**+203 g carried every flight**) without
  ever computing targets per flight. And the contract cannot express inventory:
  no load-set command, no `pellets_remaining`, and the only empty signal is
  `EMPTY_OR_BRIDGED` at ≥8 consecutive skips — **discovered at a target, after
  that plant got a partial dose.** Fix is three lines of DSDL.
- **G3** — **the dock and the dispenser have never read each other.** On-aircraft
  refill is impossible (fill cap needs **58 mm of lateral travel in a 10.5 mm
  gap**), so a dock built for unattended repeat sorties can replenish electrons
  forever and pellets never; in the below-grade silo case refill means climbing
  into a 1.15 m cavity to unlatch a 1.1–1.6 kg herbicide payload off the belly.
  **Neither project considered a swappable pre-filled hopper cartridge.** The ICD
  change request is exercised *by the dock's wake circuit*, unattended, with
  12V_PL dark so `UNCOMMANDED_DROP` is undetectable.
  **Good news found here:** the one geometric check passes — 150 × 165 × 195.4 mm
  with ≈58–59 mm deck clearance vs the dock's ≥50 mm gate, closing the dock's
  open payload-envelope question. (The dock's model had assumed 67.9 mm; the real
  payload hangs **8.5 mm lower**.)

Also: G4 dispensable-vs-volumetric capacity never established · G5 pellet
variation converged on diameter and stopped · G6 **no structural load case
anywhere in the package** · G7 consolidated ownerless items.

## Phase 10 — Packaging (04:56, this phase)

Written: `README.md` (status **design**, port **bottom/J31**, **ICD 1.0**,
mass/power table from the measured numbers, requirement-by-requirement compliance
verdicts, folder map, ICD §8 compliance table) and `docs/DESIGN.md` (45 kB —
survey → trade → six CAD rounds → electronics → the missing sim → the full risk
register).

**Both documents declare RT-1 / RT-2 / RT-3 unmet in the README**, which was
item 1 of the red team's own gate for calling this rev-0. The README's compliance
table marks the blind-mate **NONCOMPLIANT** and the verified-count requirement
**NOT MET in this revision**, and carries the fill-by-mass warning (RT-5) as an
operator instruction rather than a future fix.

### Deliverables verified present

| Folder | Status |
|---|---|
| `cad/` | **complete** — `dispenser.py` (2597 lines), `verify_exports.py` (348), `BOM.md`, `exports/` **102 files** (per-part + assembly STEP/STL, rounds 1–6; **11 STEP + 11 STL at r6**), `renders/` **34 PNGs** (7 at r6) |
| `electronics/` | **document only** — `ELECTRONICS.md`, 2129 lines. **No KiCad, no schematic, no layout.** The template's `pcb/` folder is not populated |
| `sim/` | **ABSENT** — never created |
| `docs/` | **created this phase** — `DESIGN.md` |
| `README.md` | **created this phase** |
| `software/` | **absent by direction** (CONTEXT scope cut) |
| `_run/` | 24 documents + 8 critic scripts + workflow harness |

### Gate items still open after packaging

1. **RT-1 / RT-2 / RT-3** — declared, not closed. Round 7 needed for RT-1/RT-3;
   RT-2 needs an ICD-side answer.
2. **Bench tests not yet added to the plan:** S-115 (RT-11), S-116 (RT-12),
   loaded-hopper solar soak (RT-6), humidity/swollen-pellet jam (RT-7), landing
   dust cycle in B2 (RT-8), 10 g retention pull (RT-13).
3. **Fill-by-mass procedure** is in the README as an operator instruction, but
   `Fill` / `dispensed_since_fill` are **not** in the DSDL contract (RT-5).
4. **`sim/` not delivered**, and accuracy ownership not levied on the FC/ICD side
   (RT-4).

### Commit

```
c1232653f59bd39247a5a8f5453dbd65249048c4
branch  brush-bullet-dispenser  (NOT pushed)
author  thomasg <thomas@arrowair.com>
subject brush-bullet-dispenser: rev-0 design package (overnight run)
files   172  (payloads/brush-bullet-dispenser/ only)
```
