# GAP REVIEW — what everyone missed

Written 2026-08-07 ~04:30 CDT, Finish phase, in parallel with the red team.
Lens: **compare the package against the MISSION and the CONTEXT scope**, and
look *outside* the assumptions every agent in this run shared. This is not a
re-run of the critics — the CAD critics, the judges and the electronics safety
critic did their jobs well inside the box they were given. The findings below
are things **no agent in this run owned**, because they sit between documents,
between projects, or outside the mechanism entirely.

Notation: `[V]` verified against a cited file/source · `[D]` derived, arithmetic
shown · **ASSUMPTION** = my label, unverified, with the closure path stated.
Everything from `_run/CONTEXT.md` is treated as ground truth.

**Package state at the time of writing** (`ls`, 04:30): `cad/`, `electronics/`
exist. **`README.md`, `docs/`, and `sim/` do not exist yet** — the packager step
and the drop-ballistics sim gate had not landed on disk when this review ran.
Where a gap below is "the sim never happened", read it as: *as of this writing,
and here is what the sim as briefed would still not have covered.*

---

## Summary — the three that matter

| # | Gap | One-line statement | Owner today |
|---|---|---|---|
| **G1** | **Delivery accuracy is un-owned end to end** | The whole run optimised the *mechanism*; the 1 m spec is decided by ballistics, wind, canopy and bounce, and nothing in the package or in the command contract touches any of them. My own integration says the honest limit at 8 m AGL is **≈4.5 m/s (10 mph) crosswind**, and the fix that costs nothing (aim upwind / drop lower) is not in any interface | **nobody** |
| **G2** | **Nobody did the mission arithmetic** | 250 pellets vs **25–31 min endurance** [V] vs 1–3 pellets per target — targets-per-flight was never computed, so "more capacity is good" was answered with 422 pellets without knowing whether one flight can deliver 100. And the contract has **no `pellets_remaining`, no load-set, no low-hopper warning** — the planner cannot plan around inventory | **nobody** |
| **G3** | **The dock and the dispenser have never read each other** | The payload stays mounted in the dock, but it **cannot be refilled while mounted** — the dock can replenish the battery forever and the pellets never. Plus: no loaded-standby spec (unsealed hopper, days in a box), and the ICD change request the electronics doc levied (K1 state at FC boot) is exercised *by the dock*, unattended, inside a closed box, over a loaded herbicide dispenser | **nobody** (dock pkg's payload envelope is still an "OPEN Vector ask" [V]) |

Then G4–G8: hopper at 10 % full and *dispensable* vs volumetric capacity; pellet
variation beyond diameter; the missing structural load case; and the no-owner
list.

---

## G1 — Delivery accuracy: the requirement nobody owns

### What CONTEXT asked for

> "We should be able to hit a target within 1m. Expect to be flying at around 8m
> agl" … "Sim must state the honest wind limit for this." — CONTEXT §Requirements [V]

### What the package contains

Searched the entire package for `wind`, `AGL`, `drift`, `accuracy`, `bounce`,
`canopy`, `terminal`: the only hits are (a) the r6 pellet-path critic's lateral
release-velocity finding, and (b) ELECTRONICS §3.4/§5.4, which converts that
finding into a **≤90 °/s release-move speed clause** worth 0.06 m. That is one
term of a budget nobody ever wrote down. `sim/` does not exist. There is no
error budget, no wind envelope, no recommended release altitude, and no
statement anywhere of what "hit the target" physically means.

### What I computed (so the number exists somewhere)

Numerical integration, 1.18 g / 12 mm sphere, Cd 0.47, ρ = 1.06 kg/m³ (35 °C at
~800 m — ASSUMPTION), quadratic drag, steady crosswind, released from rest [D]:

| crosswind | 2 m/s | 3 | 4 | 5 | 6 | 6.6 | 8 m/s |
|---|---|---|---|---|---|---|---|
| lateral drift from 8 m | 0.19 m | 0.31 | **0.47** | 0.65 | 0.86 | **1.00** | 1.37 |

Fall time 1.32 s, impact speed **11.3 m/s**. Combining the drift bias with the
workflow brief's own stated hover-error assumption (0.3 m 1σ per axis) and the
0.06 m release spread, 200 k samples per case [D]:

| crosswind | 0 | 2 | 3 | 4 | 5 | 6 | 8 m/s |
|---|---|---|---|---|---|---|---|
| P(within 1 m) | 99.6 % | 99.0 % | 97.7 % | 93.6 % | 83.4 % | 61.7 % | 8.9 % |

**Honest wind limit for ≥90 % within 1 m at 8 m AGL: 4.46 m/s = 10.0 mph.**
Release altitude is the single strongest lever [D]:

| release altitude | 4 m | 5 m | 6 m | 8 m | 10 m |
|---|---|---|---|---|---|
| wind limit for 90 % | 7.3 m/s (16 mph) | 6.3 (14) | 5.6 (12) | **4.5 (10)** | 3.7 (8) |

**This is the gap:** a West Texas ranch routinely exceeds 10 mph. On these
numbers the mission as specified (8 m AGL, no compensation) is weather-limited
to roughly calm mornings, and **nobody in the run knows that**, because the
accuracy requirement was treated as a mechanism property ("zero imparted lateral
velocity") rather than a delivery property.

### The fix nobody proposed, and why it is missing

The drift above is a **bias**, not scatter — it is predictable from wind speed
and direction. Aiming the release point upwind cancels it, and the limit becomes
the *wind-estimate error*, not the wind [D]: at 8 m/s with a 30 % wind-estimate
error the residual bias is 0.41 m → **95.6 % within 1 m**. The same 8 m/s
uncompensated is 8.9 %.

That fix lives in the *interface*, which is explicitly in scope ("design the
electrical/command interface contract only" — CONTEXT [V]), and it is absent:
`arrow.dispenser.Dispense.Request` carries `seq`, `count`, `flags` and nothing
else (ELECTRONICS §5.2 [V]). There is no place to state a release-point offset,
no advisory of the ballistic delay the FC must hold station through relative to
the aim point, no recommended altitude, and no "wind above X → refuse/flag" gate
even though the payload refuses for eight other reasons. **Closing action:** one
sentence in the contract ("the commanding system is responsible for wind
compensation of the release point; the payload guarantees release within
±T ms of `Dispense`, at ≤0.06 m lateral, from the port at X below the belly")
plus a recommended-altitude line. Cheap, and it assigns the accuracy
responsibility to someone.

### Three terms even the *briefed* sim would have missed

The sim brief (run-workflow.js:110) covers wind, altitude, timing jitter, hover
error and downwash. It does **not** cover, and neither does any other document:

1. **Canopy interception.** The target is a mesquite/juniper — a plant with a
   canopy. A pellet dropped from 8 m onto the plant lands *in the plant*.
   Tebuthiuron pellets have to reach **soil** to work (ASSUMPTION from product
   class; CONTEXT's own research task on pellet behaviour was never closed).
   Nowhere in 5 research docs, 4 concepts, 3 judge ballots, 6 CAD rounds or the
   electronics doc does the word "canopy" appear. **"Within 1 m of the target
   coordinate" is a proxy for the real acceptance criterion, which is "on the
   ground, in the root zone, not on a branch"** — and it is a proxy that fails
   precisely on the plants we are aiming at. This may be a *good* thing (drop
   at the dripline instead of the stem, per label practice) or a fatal one; the
   point is that the run never asked, and the answer changes the target datum
   the scouting pipeline is expected to deliver.
2. **Bounce and roll.** 11.3 m/s onto caliche, rock or hardpan, on sloping
   ground, with a 12 mm sphere. Judge 3 used the phrase "bounce scatter" once,
   in passing, about the angled chute; it was never sized. A 20 % coefficient of
   restitution and a 10° slope will move a sphere further than the entire
   mechanism-side error budget (ASSUMPTION — needs a 20-drop bench test onto
   representative ground, which is a $0 test).
3. **Pellet-to-pellet aerodynamic variation** — see G5; a tumbling barrel-shaped
   pellet (Cd 0.8) drifts **0.78 m vs 0.47 m** at 4 m/s, +66 % [D].

**Recommended owner:** whoever owns the scouting/targeting pipeline, jointly
with flight ops. Not the payload — but the payload package should *state* the
budget and hand it over, and today it states nothing.

---

## G2 — The mission arithmetic: 250 pellets, one battery, and no inventory

### Nobody computed targets per flight

Verified platform fact nobody in this run pulled: **25–31 minute hover
endurance** (Tattu 14S 30 Ah) [V `/tmp/pq-main/docs/index.md:24`]. The
dispenser's own timing contract gives **634 ms per pellet, 1.9 s for N = 3, 3.2 s
for N = 3 with two skips** [V ELECTRONICS §5.4] — so *dispensing* is never the
constraint. Per-target time is transit + descend + settle + climb.

[D] with ASSUMPTION (12–20 s per target, dense mesquite spacing, no data in any
project file to check it against):

- 250 pellets ÷ 1–3 per target = **83–250 targets** per hopper load
- at 2 pellets/target (125 targets) × 12–20 s = **25–42 min of flying**
- against 25–31 min hover endurance, minus reserve and transit to/from the
  block → realistically **~15–25 min of on-task time per battery**

**So one hopper load is roughly 1–3 batteries' worth of targets, and the run
never found out which.** That matters because CONTEXT's "more brush bullets
isn't a bad thing" directive was answered by pushing the brim to 422 pellets
(498 g, BUILD-NOTES-r6 §4 [V]) — up to **203 g of pellets above the 250 baseline
carried on every flight** that, on the pessimistic branch, cannot physically be
delivered before the battery ends the flight. It also means "250 targets" as a
mission unit implies **battery swaps mid-hopper**, i.e. the aircraft lands,
gets a fresh pack, and continues on the same partly-emptied hopper — a workflow
nobody described, and the one place where a *mission-level* pellet inventory
across power cycles actually matters.

**This is not an argument to shrink the hopper.** It is an argument that the
capacity decision was made without the one number that decides it, and it is
cheap to get: `targets/flight = f(target density, cruise speed, settle time)`,
one page of arithmetic plus one flight-log check with Vector.

### The contract cannot express inventory

`arrow.dispenser.Status` publishes `lifetime_count`, `skips`, faults and rail
voltages [V ELECTRONICS §5.2]. It does **not** publish pellets remaining, and
there is **no command to declare a load**. Consequences nobody wrote down:

- The only "you are out" signal is `EMPTY_OR_BRIDGED` = **≥8 consecutive skips**
  [V §5.2 bit 4] — which is *discovered at a target*, after that plant has
  received a partial dose. There is no early **LOW** warning, no reserve
  threshold, and no rule for "refuse a target whose N exceeds what is left".
- Judge 2 already flagged that an operator "can't distinguish 'empty' from
  'bridged' without landing" — true, and the contract makes it worse by fusing
  both into one bit.
- Mission planning (fly 250 targets) has no authoritative inventory to plan
  against and cannot reconcile at end of sortie (loaded vs dispensed vs
  residue), because nothing establishes the *loaded* number in the first place.

**Closing action (cheap, in-scope, interface-only):** add `SetLoad(seq, count)`,
`pellets_remaining` (uint16, decremented on verified dispense, FRAM-backed) and
a `LOW_HOPPER` fault bit with an operator-set threshold; and state the
mission rule "do not accept `Dispense(N)` if `N > pellets_remaining`". This is
three lines of DSDL and it converts a payload that reports history into one that
supports mission planning.

---

## G3 — The dock: the payload stays mounted, and that breaks refill

The dispenser package contains **zero references to the dock** (grep `dock`:
only venv paths). The dock package (`~/projects/quiver-dock/rev1/`) contains a
payload envelope that is still an **open assumption**. They have never met.

### G3.1 The dock can replenish the battery forever and the pellets never — checked

r6 measured it: the fill cap needs **6.45 mm of lift and 58 mm of lateral travel
in a 10.5 mm gap → "on-aircraft refill is not claimed"** [V BUILD-NOTES-r6 §4],
and the buildability critic restated it: "every refill means quick-releasing a
~1.09 kg empty payload" [V].

The dock's entire value proposition is **unattended repeat sorties**: it lands,
shelters, charges to a storage SOC and tops off on tasking [V DESIGN-REV1 §1,
§2 item 8]. Therefore, with this payload:

- **pellets are the consumable the dock cannot replenish.** Sorties per human
  visit = one hopper load (83–250 targets per G2), no matter how good the dock
  is at electrons.
- the human visit is worse than a tailgate: in the PERMANENT silo the aircraft
  parks **below grade** in a ~1.15 m cavity, deck ≈450 mm below grade [V
  DESIGN-REV1 §5]. Refilling means climbing into the pit (wall rungs are
  modelled) and **unlatching a 1.1–1.6 kg herbicide payload off the belly of a
  parked aircraft in a confined space**, then handing it up. The dock's
  prototype plan trials *battery*-swap ergonomics (RT-6) and nothing else.
- **the obvious architectural answer was never considered by either project: a
  pre-filled swappable cartridge/magazine** — load the hopper on the tailgate
  and swap the *hopper*, not the payload. The r6 design already has a
  drop-out cartridge concept for the meter (`cartridge drop-out sweep 0.00 mm³`
  [V]); nobody asked whether the *hopper* should be the swappable unit. This is
  the single highest-leverage thing this gap review has to say about the design
  itself, and it is a Rev-1 architecture question, not a detail.

### G3.2 Loaded standby has no spec at all

Nothing anywhere states **how long pellets may live in the hopper**, or in what
environment. What is known:

- the payload is **not sealed**: "gasket grooves at the perimeter joints are
  still schematic (only the fill-cap O-ring gland is real geometry); … it is not
  sealed" [V BUILD-NOTES-r6 open issue 11].
- CONTEXT's own research task — "hardness numbers, **moisture swelling**" — was
  **never closed** [V CONTEXT §Pellet]. The clearances the whole mechanism rests
  on (Ø15.00 pocket vs Ø13 worst-case pellet, 1.50 mm roof clearance, 0.50 mm
  under-gap, 1.00 mm rim gap [V r6 numbers]) have **1.0–2.0 mm of total slack**.
  ASSUMPTION: a clay/urea-binder ag pellet held at high humidity swells and/or
  cakes by more than that. Nobody has bounded it.
- in the dock it sits in a closed box for days: PERM gets a dehumidifier, the
  TRANSPORTABLE skid does **not** [V DESIGN-REV1 §4.6], and both see
  condensation cycling.

**Closing action:** state a loaded-standby limit (e.g. "≤72 h loaded, or unload
before docking") until a humidity-soak test exists, and put a desiccant
provision or a real gasket on the fill path. Today this decision belongs to
nobody and will be made by whoever leaves a loaded aircraft in a dock over a
weekend.

### G3.3 The dock is the party that will exercise the un-owned ICD change request

ELECTRONICS §2.8 levies a change request on project-quiver: **K1's state at FC
boot, FC reboot, RC failsafe and parameter reset is UNSPECIFIED**, so 12VSW may
appear at the payload with no operator involvement [V]. The dock's wake circuit
**boots the FC automatically** — "FC boots and closes the SSR exactly as if a
human pressed it" [V DESIGN-REV1 §1]. So the unspecified path is not a rare
corner case: it is **the dock's normal, unattended, possibly-daily operating
sequence, executed inside a closed box, over a loaded herbicide dispenser, with
the payload's own logic rail (and therefore its `UNCOMMANDED_DROP` detection)
dark** — ELECTRONICS itself concedes "a drop while 12V_PL itself is absent
remains undetectable" [V §2.4]. Nobody has told the dock team the CR exists;
nobody owns the CR.

### G3.4 The one geometric check — I ran it, it passes, and it also finds a 13 mm datum disagreement

Dock CAD models an **assumed** payload of 320 × 320 × 180 mm and gates
`payload-clearance ≥ 50 mm`, reporting **67.9 mm** [V `dock_rev1_r9.py:2806-2816,
3127-3136`; OPEN-QUESTIONS-rev1 item 1 — "the authoritative payload keep-out is
an OPEN Vector ask (charge-B trade doc V-4)"].

Real dispenser, measured: plan **150 × 165 mm**, stack **195.4 mm** below the
mating plane, lowest point 181.5 mm above the gear ground plane [V
BUILD-NOTES-r6 §4]. Dock seat datum `AC_Z0 = 376.88`, `DECK_TOP = 500` [V
dock_rev1_r9.py:666,691]. So [D]:

- payload bottom in dock frame = 376.88 + 181.5 = **558.4** → **clearance to the
  deck ≈ 58–59 mm** (vs the dock model's 67.9): the real payload hangs **~8.5 mm
  lower** than the modelled envelope because its top is at the mating plane, not
  20 mm below it. **Still passes the ≥50 mm gate, with 9 mm instead of 18.**
- laterally the dispenser is far inside the assumed 320 × 320 — no issue.
- **the datum disagreement worth flagging:** the dock uses `AC_BELLY_CLEAR = 390`
  ("~390 mm under belly harness/connector gear", quiver CONTEXT) while the
  dispenser *derived* **376.9 mm** to the actual payload mating plane from the
  same quiver CAD. The dock's F1 payload-height budget (320 mm) and its 67.9 mm
  clearance are both computed off the looser number. Not a failure — but the
  dock's open question V-4 can be **closed today** with the dispenser's measured
  numbers, and neither project noticed the other had the answer.

---

## G4 — Hopper at 10 % full: skip storms are known; *dispensable* capacity is not

Everyone reports **volumetric** capacity (963 cm³ → 422 pellets, 1.69× the
minimum [V r6 §4]) and, separately, that draining leaves **115 cm³ ≈ 51 pellets**
of residue [V r6 §4]. **Nobody reconciled them, and nobody states how many
pellets the mechanism can actually meter out before it starves.**

Geometry at 10 % full [D, from r6 measured stack]: 42 pellets ≈ 96 cm³ spread
over the shelf annulus (r15.2–47.0, ≈6360 mm² net) = a bed only **~15 mm deep** —
about one pellet layer — sitting on what the pellet-path critic measured as a
**flat 0° shelf whose opening is a 120° × 26.5 mm window, with ~66 % of the
outlet plane dead shelf** [V r6 pellet-path critic MODERATE 4].

The only thing that moves a pellet across that dead shelf is the agitator, and
the agitator **is on the meter shaft** — it turns only when a dispense is
commanded, **22.5° per index** [V r6 §3]. So [D]: a pellet resting on the shelf
240° away from the window needs ≈ **11 index moves** to be dragged into the
window — i.e. the last pellets are recovered only by commanding dispenses you
did not want, each of which is a skip. That is the quantitative shape of Judge
2's "skip-storms at low fill", and it interacts with G2: skips cost hover time
(3.2 s for N = 3 with two skips [V §5.4]) exactly when the battery is oldest.

**What has no owner:** the number that CONTEXT's hard minimum is actually about.
"≥250 pellets" should mean **250 dispensable**, not 250 loadable. **Test (one
afternoon, zero cost):** load 250, dispense until `EMPTY_OR_BRIDGED`, count what
came out, count what is left, repeat tilted ±10°. Until then the compliance claim
is volumetric only, and the honest statement in the README should say so.

---

## G5 — Pellet-to-pellet variation: everyone converged on diameter and stopped

The whole run correctly identified the ±1 mm diameter ASSUMPTION as load-bearing
(all three judges; cross-cutting action item 1 [V JUDGING]). Three other
distributions are equally load-bearing and appear **nowhere**:

1. **Mass.** 1.18 g is a single verified value with no tolerance [V CONTEXT].
   The entire verification story counts **pellets**, and the agronomic
   requirement is **dose of active ingredient**. If molded pellet mass is ±15 %
   (ASSUMPTION, typical for extruded/molded ag granules; closure = weigh 50
   pellets on a 0.01 g scale, 10 minutes), then an N = 1 target — a large
   fraction of the mission — carries ±15 % of its dose and the payload reports
   "1 pellet, verified" either way. Also blocks any load-cell reconciliation:
   you cannot convert 295 g into a count without the distribution.
2. **Shape / tumbling, which feeds straight into G1.** CONTEXT already notes the
   pellets are "slightly irregular … barrel shape" [V]. Drift at 4 m/s
   crosswind [D]: sphere Cd 0.47 → **0.47 m**; tumbling barrel Cd 0.8 → **0.78 m**
   (+66 %). Diameter/mass variation alone is minor by comparison (0.43 m for a
   1.50 g/13 mm pellet, 0.52 m for 0.90 g/11 mm). **The aerodynamic spread is
   larger than the mechanism's whole release-velocity budget** (0.06 m), which
   the electronics doc spent a design clause on.
3. **Lot acceptance.** Every clearance in the meter is frozen against an
   unverified ±1 mm; the caliper survey is scheduled once, as a design input
   [V r6 open issue 3]. **Nothing specifies an incoming-lot check**, so a
   future drum with a different mold or a different supplier jams the fleet with
   no warning. A printed **go/no-go gauge plate** (a 13.0 mm slot the whole lot
   must pass and a 10.5 mm slot it must not) is a 20-minute CAD job and belongs
   in the shipped package next to the fill ribs. No owner today.

---

## G6 — There is no structural load case anywhere

The interference critic measured clearances; the mass critic measured mass;
**nobody multiplied mass by an acceleration.** Facts on hand [V r6]:

- loaded mass **1.39 kg** at 250 pellets, **1.59 kg** at the brim
- printed-parts centroid Z = −257.05, mating plane Z = −171 → CG hangs
  **~86–95 mm below the mount plane** (loaded, including the motor at −366 and
  the pellet column, ASSUMPTION ≈90 mm)
- the payload hangs on **4 × M2 SHCS at (±19, ±19)** with a measured **0.90 mm
  of thread engagement** into M2×4 heat-set inserts (buildability MAJOR: "M2x14
  is needed") [V]
- the quick-release's "poor unlatched-direction moment capacity" and the
  **missing per-port moment rating in the ICD** were identified by the
  *psd-escapement* advocate and died with that concept — the winner never
  carried them, and Judge 3 explicitly asked for clip-plate loads

[D] a modest 5 g lateral landing/gust case: 1.59 kg × 5 g = **78 N**, moment
about the mating plane = 78 × 0.090 = **7.0 N·m**, prying load across the 38 mm
bolt pattern ≈ **92 N per screw** — into two engaged threads of an M2 insert in
printed CF-PETG. This is almost certainly fine with the correct M2×14 screw and
almost certainly *not* fine as currently specified, and either way **it is
unanalysed**: no g-case is stated anywhere, and the ICD has no per-port
load rating to check against. **Closing action:** state a design g-case (I would
propose 10 g vertical / 5 g lateral, ASSUMPTION pending Vector), compute insert
pull-out, and raise the missing ICD per-port moment rating as a second change
request alongside the K1 one.

---

## G7 — Things with literally no owner (consolidated)

| # | Item | Where it came from | Consequence if it stays un-owned |
|---|---|---|---|
| 1 | **Caliper survey of 20+ real pellets** | r6 open issue 3, all three judges | Gates the first print; every clearance in the meter is unverified until then |
| 2 | **Pellet crush strength (0.36 MPa / 41 N)** | r6 open issue 5 — class-derived from a 1979 patent | **Every torque margin in the jam story scales with it.** IFDC S-115 bench test, no budget, no owner |
| 3 | **ICD change request: K1 state at FC boot / reset / failsafe** | ELECTRONICS §2.8 | Levied on project-quiver in a document project-quiver has not read; triggered by the dock (G3.3) |
| 4 | **ICD gap: per-port mechanical load / moment rating** | psd-escapement advocate, then dropped | G6 cannot be checked against anything |
| 5 | **DroneCAN data-type IDs** | ELECTRONICS §5.2 ("deliberately not invented here", closure = a PR to the quiver DSDL namespace) | The command contract cannot be implemented until someone opens that PR |
| 6 | **Motor on a scale** (310 g ASSUMPTION vs 380–400 g published) | mass critic MINOR | 70 g = 70 % of the entire contingency |
| 7 | **Fill / handling / PPE / decon procedure** | scope-cut "regulatory" ≠ scope-cut "handling" | A jam clear means pouring 250–422 pellets of tebuthiuron into a tub on a tailgate in wind, and the sump still spills ~51 pellets [V r6]. There is no written procedure, tool list, or spill plan — and the CONTEXT regulatory cut ("we're already handling that") does not cover the *mechanical* consequences the design chose |
| 8 | **Wear parts & interval** (brush/bristle strip, pocket disc, bearing) | Judge 2: "a scheduled field maintenance chore, not a solved problem" | No replacement interval, no wear-out criterion, no spares list in the BOM |
| 9 | **Shipped deliverables** — `README.md`, `docs/DESIGN.md`, `sim/` | absent at 04:30 | The package as it stands is `cad/` + `electronics/` + a large `_run/`; a reader outside the run has no entry point |

---

## What I checked and found already covered (so this review is honest)

- Fragment-wedge jam: covered exhaustively and correctly, and still failing on
  measured geometry (r6 pellet-path BLOCKERs) — the critics own it.
- Fuse/thermal/interlock/count-sensor integrity: ELECTRONICS is strong; the
  safety critic's findings are dispositioned in §11.
- Dust and fines: identified everywhere; attrition *rate* is an acknowledged
  open unknown, not a gap.
- Mass ceiling: measured, cross-checked, robust at every infill (mass critic).
- Ground/prop clearance: measured independently twice; 181.5 mm, 4.5× the
  requirement.
- Power-cycle safe state: the Hall decode + K1 argument is a real answer with a
  stated bounded exposure.

The gaps above are what is left when you stop looking at the mechanism.

---

## Recommended disposition (what I would do first)

1. **Write the accuracy budget and put the wind limit in the README**
   (G1) — 4.5 m/s at 8 m AGL, 7.3 m/s at 4 m, and one contract sentence assigning
   wind compensation to the commanding system. Half a day.
2. **Ask the two mission questions** (G2): targets per flight, and what "hit"
   means on a plant with a canopy. One conversation each with Thomas/flight ops.
3. **Send the dock team three numbers and one problem** (G3): the measured
   150 × 165 × 195.4 mm envelope and 58–59 mm deck clearance (closes their open
   V-4); the K1-at-boot change request; and the fact that a docked aircraft
   cannot be refilled — which should be evaluated as a **swappable hopper
   cartridge** in Rev-1, not patched.
4. **Add inventory to the contract** (G2): `SetLoad`, `pellets_remaining`,
   `LOW_HOPPER`. Three lines of DSDL.
5. **Run the two zero-cost bench tests** (G4, G5): dispense-to-starvation count,
   and weigh 50 pellets.
