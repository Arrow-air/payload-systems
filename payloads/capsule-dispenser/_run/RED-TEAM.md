# RED TEAM — capsule Dispenser (fresh eyes, whole package)

Scope: everything under `payloads/capsule-dispenser/` as it stands
2026-08-07 04:30 — `_run/` (survey, concepts, judging, BUILD-NOTES r1–r6),
`cad/` (dispenser.py r6 + exports + BOM), `electronics/ELECTRONICS.md`.
`sim/`, `docs/` and `README.md` **do not exist at the time of this review**
(`ls` on the payload folder returns `_run cad electronics` only).

Method: I re-measured the shipped exports myself with trimesh/build123d in the
`dock-cad-314` venv rather than trusting any prose. Everything labelled
MEASURED below is my own probe of `cad/exports/*_r6.stl`, the vendor STEP, or my
own arithmetic; everything labelled [A] is an assumption with its reasoning
stated; findings I am *confirming* rather than discovering are marked
"(re-confirms r6 critic)" so the reader can tell new information from an echo.

Severity: **CRITICAL** = the thing cannot work / requirement not met ·
**HIGH** = will bite in the field or invalidates a headline number ·
**MODERATE** = real, bounded, needs an owner · **LOW** = accuracy/hygiene.

---

## RT-1 — CRITICAL — The package is being shipped on a round that FAILED three of four critics, and I independently reproduced three of the blockers

The CAD loop stopped at r6 with **interference 7 FAIL, pellet-path 5 FAIL,
buildability 4 FAIL, mass-budget 8 PASS** (BUILD-NOTES-r6 §"Round-6 critics").
There is no r7. `cad/dispenser.py` (mtime 02:04) has not changed since those
critiques were written (03:08). So five blocking defects are live in the
artefacts that the packager step will commit as "rev-0 design package".

My own probes of the exported meshes, independent of the critics:

| Blocker | My measurement |
|---|---|
| Roof through-slot at θ = 310° | `meter_housing_r6.stl`: roof thickness (z −283.2…−274.2) at θ = 309° is **9.0 mm at r = 24.5/32/39.5/46**; at θ = **310.0° it is 0.00 mm at every one of those radii**; 0.2–0.4 mm at 311°, 0.6–1.2 mm at 313°. The half-space entry-ramp cut is mirrored 180° away, leaving an open slot from the pellet bed into the metering arc *downstream of every rejection feature*. |
| No torque path disc→shaft | `pocket_disc_r6.stl` bore at z = −295: radius **3.06 mm at all 24 angles probed** — a plain round bore on a Ø6 shaft. The D-flat the 0.65 N·m argument depends on does not exist. |
| Gearbox bolt pattern | `retaining_plate_chute_r6.stl` at z = −302: clearance holes on the **diagonals at r ≈ 16.5–19.5 mm** (26 mm square), pilot bore open to r = 11.0. The vendor drawing (per the buildability critic) is 4 × M3 on a **Ø26 bolt circle**, i.e. r = 13 on the axes. The gearbox does not bolt on. |

**Fix / test:** either run r7 and close them, or the shipped `README.md` must say
in the status line that the mechanism as drawn **cannot be assembled, cannot be
driven and cannot be powered** (RT-2), with the five blockers listed. Shipping
"rev-0 design package" without that line is the single most dangerous thing in
this run — the numbers are good enough to be believed.

## RT-2 — CRITICAL — The payload has no electrical connection to the aircraft

(re-confirms r6 interference BLOCKER; I did not re-measure the 3331 board.)
Payload blind-mate pads sit at Z = −181.5; the drone-side spring-pin tips at
Z = −162.15 → **19.35 mm of air**. Even at the highest legal pad plane (−171.0)
the gap is 8.85 mm against ≤2 mm of plunger travel [A]. The r6 notes offer
"payload material inside the shaft = 0.00 mm³" as *evidence the PCB is in the
shaft*; that metric is the proof it is not. The proposed remedy (standoffs on
the vendor tabs) pushes payload material above Z = −171, which the same
paragraph forbids, and the critic showed the QR halves nest ≤0.54 mm.

**Fix:** this is an aircraft/ICD-side defect, not a payload open issue. Raise it
against `interface/ICD.md` v1.0-draft with the measured numbers and get the
physical 2112 + 3331 pair on a bench with a depth gauge before any more CAD.
Nothing downstream (count contract, power budget, DroneCAN) is real until a pin
touches a pad.

## RT-3 — CRITICAL — "Verified count" is satisfied only in a document describing hardware that does not exist

`ELECTRONICS.md` §4.2 proves, correctly, that a single centred beam is
**disqualifying** (a Ø12 pellet near the wall reads 7.5 ms, shorter than a
centred Ø8 fragment). Its answer is ECO-3 (boss `Box(20,12,14)`, two Ø3.2
apertures at x = 29 and 35) plus ECO-9 (6 mm vertical stagger).

MEASURED in the shipped CAD (`dispenser.py` L1005–1017, and confirmed on the
export): **one** Ø3.2 tunnel per side, at `x = PCD_R = 32` — i.e. on the bore
diameter — in a `Box(12,12,14)` boss. The disqualified geometry is what is
modelled, exported, rendered and BOM'd. `cad/BOM.md` still lists the
**TSSP4038 digital receiver**, the part §4.4 explicitly rejects because "a bit
cannot report how much margin is left"; the analog VBPW34FAS/OPA2320 chain,
the sacrificial bore-face window (ECO-4), the labyrinth (ECO-5) and the motor
NTC (ECO-10) are in no mechanical drawing or BOM line.

CONTEXT's hard requirement is *"dispense exactly N pellets … VERIFIED
(sensed)"*. As shipped, the count hardware is the version the electronics
author calls a geometry error.

**Fix / test:** apply ECO-3/4/5/9/10/11/12 to `dispenser.py`, re-export,
re-run the interference checks (the widened boss leaves 4.4 mm to the motor
face — my probe puts the *current* boss at x 26…38 vs the motor face at 17.6,
so there is room; note the "1.4 mm today" figure quoted in ECO-3 is the
chute-to-motor gap, not the boss clearance). Then B1 as written.

## RT-4 — HIGH — Nobody owns the 1 m accuracy requirement, and the missing sim is about to be handed the assumption that decides it

There is no `sim/`. In its absence I ran the ballistics myself (1.18 g, Ø12
sphere, Cd 0.47, ρ 1.06 kg/m³ for hot high-plains air, RK-free explicit
integration at 1e-4 s):

| From 8 m AGL | value |
|---|---|
| terminal velocity | 20.3 m/s (so the fall is only mildly drag-limited) |
| fall time | 1.32 s |
| downwind drift, steady crosswind | **0.09 m per 1 m/s**; 0.31 m @3, 0.65 m @5, 1.37 m @8 m/s |
| release lateral velocity (r6 critic's measured 0.126–0.25 m/s) | 0.10–0.20 m |

So the **payload is not the accuracy driver — position hold is.** Monte Carlo
(40 000 drops/case, gust 30 % 1σ, release-velocity term included):

| hover error 1σ | P(<1 m) @0 / 3 / 5 / 8 m/s wind |
|---|---|
| 0.2 m | 100 / 99.8 / 97.9 / 81.5 % |
| **0.3 m** (the value the sim brief hands itself) | 99.3 / 97.6 / 92.5 / 74.0 % |
| 0.4 m | 94.6 / 91.1 / 84.2 / 67.0 % |
| 0.5 m | 85.3 / 81.4 / 74.7 / 59.6 % |

The 90 % gate passes at 0.3 m 1σ up to ~5 m/s wind and **fails at 0.4 m 1σ in
still air**. The whole result therefore rests on one un-owned assumption about
the *aircraft*, and CONTEXT cut the software phase — so wind-compensated
aim-point offset, hold-quality gating and even the 32 mm lateral offset of the
exit port from the payload axis (a yaw-dependent bias) have no owner in this
package.

**Fix:** (a) the sim must sweep hover σ as a first-class axis and report the
*pair* (wind, hold accuracy) that meets the spec, not a wind limit alone;
(b) add two lines to the §5 command contract: the FC shall provide the
aim-point offset (payload does not know wind), and `Dispense` shall be refused
with `HOLD_QUALITY` if the FC does not assert a position-hold-good flag;
(c) state the release-point offset (x = +32 mm in payload frame) and the
required payload clocking in the README.
**Test:** 50 drops from a hovering aircraft over a marked target in 0/3/5 m/s,
measuring both pellet landing and logged EKF position — that separates payload
scatter from hold error, which no bench test can.

## RT-5 — HIGH — The fill marks are calibrated on a worst-case packing constant, so "250 pellets" is really 250–370 and the 1.5 kg ceiling is an operator decision

`dispenser.py` L176: `PELLET_VOL_WORST = 2.28` mL/pellet packed. A nominal
1.18 g / Ø12 pellet is 0.905 cm³, so 2.28 mL/pellet implies a **40 % packing
fraction** — below even random-loose sphere packing (~0.60; ~0.64 after the
vibration of a flight). It is a sound *conservative floor for capacity claims*
and a **wrong constant for a fill mark**.

MEASURED on `hopper_r6.stl`: the two internal fill ribs sit at **z = −222.6**
(0.8 mm proud, the "250" baseline) and **z = −196.9** (1.05 mm proud, the MAX/
brim line). The void below the 250 rib is ≈550–570 cm³.

| filled to | worst-case basis (what the ledger prices) | nominal 12 mm spheres @0.60 packing |
|---|---|---|
| "250" rib | 250 pellets, 295 g → **1387 g** total | **≈370 pellets, 438 g → ≈1530 g** |
| brim rib | 422 pellets, 498 g → 1590 g | **≈638 pellets, 753 g → ≈1845 g** |

(BUILD-NOTES-r6 itself prints "587 sphere basis" for the brim and then masses
only the 422 case — the ledger prices the brim at the count that makes it
lightest.) CONTEXT exempts pellets above the 250 baseline from the ceiling, but
that is an accounting rule; the clip plate, the QR latch and the landing gear
carry the real 1.85 kg.

Compounding it: there is **no inventory telemetry anywhere** — I grepped the
whole DSDL/contract; `lifetime_count` is the only counter, there is no
`pellets_remaining`, no `dispensed_since_fill`, no `Fill` service. The operator
learns the hopper is empty from `EMPTY_OR_BRIDGED` after eight skips, mid-sortie.
And the ribs are internal features of an **opaque black printed hopper**, read
by eye down a Ø46 hole into a 140 mm dark cavity.

**Fix:** fill by **mass** (295 g = 250 pellets at the CONTEXT-verified 1.18 g);
put a "fill to 295 g / max 500 g" label on the hopper and a $20 scale in the
field kit; add `Fill(pellets_loaded)` + `dispensed_since_fill` to the contract
so count reconciles to inventory. Re-run the mass ledger at nominal packing and
state both bounds.
**Test:** weigh three fills to each rib with a real pellet lot; report the count
spread.

## RT-6 — HIGH — Nobody analysed the thermal case that matters: a black hopper full of PEG-bound pellets parked in the sun

`ELECTRONICS.md` §2.6 does a genuinely good four-term thermal model — **of the
50 × 26 × 42 mm electronics bay**, and finds 77.5 °C parked in sun against
CF-PETG's Tg ≈ 80 °C. Nobody applied the same method to the 963 cm³ of pellets
hanging 100 mm away. Doing it with §2.6's own coefficients (α 0.95 black CF,
h_conv 8, h_rad 8.2 W/m²K, radiative sink 55 °C, 50 °C air, exterior ≈0.045 m²,
sun-projected 0.011 m² + ground-reflected on 0.02 m²):

- **Q_in ≈ 13.7 W → ΔT ≈ 19 K → hopper wall ≈ 74 °C** parked, no wind [A, same
  assumption set as §2.6].
- With a light finish (α 0.4): ≈ 63 °C.

Why that matters, from the package's own research (`RESEARCH-drone-spreaders`
§1.3, US4172714 composition class): the pellet binder system is **PEG 200–600
(2–10 %) + urea + swelling bentonite** — note it is *not* wax, and PEG 200–600
is a **liquid or near-liquid at room temperature** (PEG 600 mp ≈ 20–25 °C).
At 65–75 °C the binder fraction is fully mobile. Whether it migrates, tacks
pellet-to-pellet and bridges the outlet is completely untested — and the outlet
is the design's weakest flow feature already (26.5 mm × 120°, **2.04 × D_max**,
below every no-arch rule, met "only through the active-agitation branch" per the
r6 pellet-path critic, with any given angular location swept once per 2.67
pellets).

Two more consequences nobody carried:
1. **Material contradiction.** §2.6 ECO-2 requires "the whole payload's external
   surface shall be light-coloured (α ≤ 0.4)"; `cad/BOM.md` specifies
   **CF-PETG for 9 of 10 printed parts** — carbon-filled is black by
   construction (α ≈ 0.95). You cannot have both. Painting/wrapping a dusty,
   glove-handled, herbicide-exposed part is a wear item nobody costed.
2. **Every structural number in the package is implicitly room-temperature**
   while the binding case is 63–77 °C: the 3 × M3 plastite skirt-tab joint
   carrying the cartridge + pellet column (r6 open issue 12), the 4 × M2
   heat-set inserts that carry the *entire loaded payload*, the 1.6 MPa
   brush-holder stress check. PETG loses most of its stiffness and creeps
   within 10 K of Tg.

**Fix / test:** amend **B4** so the soak is done with a **loaded hopper**
(295 g of real pellets), with a thermocouple *in the bed*, ≥4 h at ≥900 W/m²,
followed by 50 dispenses and a bed-flow observation; add a 70 °C pull-out test
for the plastite pilots and the M2 inserts; decide the exterior material/finish
(ASA-CF or pigmented PETG for sun-facing shells) before the print.

## RT-7 — HIGH — The hopper is not, and cannot be, sealed — and one wetted pellet is a hard jam

`RESEARCH-drone-spreaders` §1.3 [V]: wetted pellets "crack immediately after
wetting and swell to about 2 to 3 times their original volume", irreversibly;
the label itself says "avoid contact with floor and moisture". The concept doc
answered this with "gasketed screw-on lid (moisture sealing)". But the pellet
path is **permanently open to atmosphere at the bottom**: the Ø22 chute mouth
sits 181 mm above the ground with no cap, and it connects to the sump through
the retaining-plate fines slots (85 % open by the builder's own measurement) and
the 0.5 mm under-gap. r6 open issue 11 concedes the perimeter gaskets are
"schematic". So overnight dew, a rain shower on a parked aircraft, or a wash-down
puts humid air in contact with the bed, and a swollen Ø17–19 pellet in a Ø15
pocket is a jam with no bypass and no isolation gate (r6 pellet-path MODERATE 5:
clearing it means dumping 250–638 pellets of herbicide on the tailgate).

**Fix:** a storage plug for the chute mouth + a desiccant sachet in the fill
cap + a written "do not store loaded" rule; make the perimeter gaskets real
geometry. **Test:** load 50 pellets, expose to 90 % RH / 24 h and to a
simulated dew cycle, then attempt 50 dispenses and record torque; separately
introduce one deliberately pre-swollen pellet and verify the jam is *detected
and reported*, not silently ground through.

## RT-8 — HIGH — The dust analysis looks up when the dust comes from below

Seven dust measures in §4.5, all aimed at pellet fines falling from the meter.
The count windows sit **10 mm above the open chute exit** (beam at Z = −343.2,
chute mouth at −353.2), facing straight down at the caliche the aircraft lands
on and blasts with rotor downwash twice per sortie. In a West Texas landing the
optical tunnels are the lowest, most exposed, most direct dust target on the
whole aircraft — and the only sensor the "verified count" requirement depends on.

**Fix:** keep the 5 mm recess and the bore-face sacrificial window (ECO-4), add
a chute cap for ground handling (doubles as the RT-7 moisture plug), and
consider moving the beam up the chute with a separate exit-clear check.
**Test:** amend **B2** to include 20 takeoff/landing dust-injection cycles
(downwash-blown caliche dust at the chute mouth) and report
`beam_margin_pct` before/after — today B2 only loads fines from the pellet side.

## RT-9 — MODERATE — Mass creep is monotonic, 41 % in six rounds, and every open blocker adds more

| round | empty carried | loaded @250 | margin to 1.5 kg |
|---|---|---|---|
| r1 | 773.9 g | 1068.9 g | 431 g |
| r3 | 959.2 g | ~1255 g | ~245 g |
| r4 | 977.9 g | 1272.9 g | 227 g |
| r5 | 979.1 g | 1274.1 g | 226 g |
| r6 | **1092.4 g** | **1387.4 g** | **113 g** |

+58 g/round over the last three rounds, and the remaining work is all additive:
ECO-3 sensor bosses (+6 g stated), alu bay lid (+1.4 g), blind-mate standoffs
(+3–6 g, un-ledgered), a disc hub with a real D-flat and a gearbox adapter
plate (RT-1), plus whatever r7 does to the roof. Two more rounds at the observed
rate lands on the ceiling — and the ceiling case is already stated at the
**low-end density (1.25 g/cm³) with a slicer bracket the mass critic measured
15 % optimistic** (unpadded EDT: 334 g claimed vs 383 g corrected).

**Fix:** freeze a mass reserve line **per open blocker** (say 40 g) in the
ledger now, quote the ceiling at 1.27 g/cm³, and make the 1.5 kg check use the
nominal-packing pellet load from RT-5.

## RT-10 — MODERATE — Compliance criteria were re-based when they stopped passing

Two instances, both documented honestly in the notes, which is why they are
MODERATE and not CRITICAL — but they are the same move:
1. **Fill-line rule (r6 §5).** The r5 rule (MAX fill = the mass-limited line)
   returned **242 pellets, below the 250 hard minimum**, once the geared motor
   was added. The rule was replaced with "MAX rib = the volumetric brim".
   The requirement did not change; the test for it did.
2. **Pellet-above-250 exemption.** r5 refused to use CONTEXT's exemption; r6
   uses it to state the brim case. Combined with RT-5 the exemption now covers a
   ~+250 g swing nobody weighed.

**Fix:** state both rules side by side in the shipped ledger ("mass-limited
line: 242 pellets at the quadruple-conservative basis; volumetric brim: 422
worst-case / ~638 nominal") and let the reader see the tension rather than
resolving it silently.

## RT-11 — MODERATE — The recovery torque may crush whole pellets at the low end of the crush distribution, manufacturing the fragments it is recovering from

Everything in §2.2 of the r6 notes scales with **one class-derived constant**:
0.36 MPa / 41 N whole-pellet crush, from US4172714 (a *different* pellet).
Normal metering is 12.2 N (3.4× under), recovery is 20.4 N (2.0× under). But the
same research section notes measured crush for comparable granules at
**2.3–2.9 kgf = 23–28 N**. On that branch recovery at 20.4 N is only 1.1–1.4×
under whole-pellet crush, i.e. **inside the scatter** — the recovery routine
would grind pellets into exactly the Ø8–11 fragments that (a) jam the arc and
(b) are the ones the count gate cannot distinguish (§11 R1).

**Fix:** make the recovery current a function of a **measured** distribution,
not a single number: run **IFDC S-115** on ≥30 real pellets, set recovery force
≤0.5 × the 5th-percentile crush, and re-derive the gear ratio if that
contradicts the shear requirement. This is the number that decides whether the
r6 architecture change (the gearbox, +110 g, the entire >1 kg justification)
was correct.

## RT-12 — MODERATE — There is no fines budget, and the running clearances are the fines reservoir

The package names the problem repeatedly (survey open unknown #2, r6 open issue
9) and never sizes it. My arithmetic:

- Attrition [A, research §1.3]: "a few tenths of a percent by mass per handling
  cycle" → **0.9–1.5 g of fines per fill** (295–440 g), before rotor vibration,
  before the 1.0 mm rim shear gap, the deflector-nose plough and the 0.55 mm
  agitator film add their own.
- Reservoir volume, MEASURED from the modelled clearances: under-gap annulus
  (r20→46 × 0.5 mm) = **2.70 cm³**; disc-rim shear gap (Ø46 in Ø47 × 14 mm) =
  **4.09 cm³**. At a fines bulk density of ~0.8 g/cm³ [A] the running clearances
  hold ≈**5.4 g** — i.e. **three to six sorties** of fines before they are
  packed solid, and the torque budget's 28.6 mN·m bed-friction term carries no
  allowance for that.

**Fix / test:** **IFDC S-116** drum attrition on a real pellet lot to get fines
mass and size distribution; then a 250-pellet dry run with a mass balance
(weigh in, weigh delivered, weigh what falls out of the chute, weigh what stays
inside), and an acceptance criterion on drive-torque rise (e.g. <20 % after 250
pellets) and on `beam_margin_pct` drop.

## RT-13 — MODERATE — A 1.4–1.85 kg herbicide payload hangs on a COTS clip with no secondary retention and no rated load

`interface/ICD.md` §6: *"Per-port structural mass limits: **not yet formally
specified**"*. The payload's whole mechanical attachment is 4 × M2 into printed
heat-set inserts (with **0.9 mm of thread engagement** per the r6 buildability
MAJOR — the BOM's M2×10 needs to be M2×14) into a COTS spring-clip pair, with
CG **102 mm below the mating plane** (see RT-16). There is no lanyard, no
safety wire, no secondary catch in `cad/BOM.md`, and no drop/shock case anywhere
in the package. Failure mode is a 1.5 kg object plus a herbicide spill.

**Fix:** a safety tether to a hard point (grams), specify M2×14 with thread
locker, and levy a shock/retention rating request on the ICD owner in the same
change request as RT-2. **Test:** 10 g shock pull on the QR pair with a loaded
dummy; vibration per B8 **with the tether fitted**.

## RT-14 — MODERATE — The refill procedure has no stable rest position, no tooling, and handles a dusty herbicide by hand

The r5/r6 notes correctly conclude on-aircraft refill is impossible (6.45 mm
cap lift then **58 mm of lateral travel inside a 10.5 mm gap**). What is not
stated is that the same geometry blocks the *off*-aircraft procedure:

- Set the payload down on its clip plate (top face down) — the table now
  occupies exactly the 58 mm of lateral travel the cap needs. Refill impossible.
- Stand it chute-down — a **195 mm tall, Ø140, 1.09 kg** object balanced on a
  35 × 35 mm motor can, with the full weight through the gearbox output flange;
  tip angle ≈11°.
- So refill is a two-handed operation on a held part, pouring dusty herbicide
  pellets through a Ø46 hole in ranch wind, with no funnel, no scale, no cradle
  and no PPE line anywhere in the BOM or notes.

**Fix:** add a **refill kit** to the BOM (printed cradle that supports the
hopper flange, a Ø45 funnel, a 500 g scale) and write the procedure into
`docs/`; or move the fill port to the hopper's side wall above the 250 line,
which removes the airframe-clearance problem entirely. **Test:** time three
gloved refills in wind and record spillage mass.

## RT-15 — MODERATE — A live open issue was deleted rather than closed between rounds (fill-cap retention)

r5 open issue 9, verbatim: *"…fill-cap anti-rotation detent still unmodeled
(O-ring friction is the interim retention)."* r6 open issue 11 keeps the gasket
clause and **drops the detent clause**; no round in between modelled a detent;
`cad/BOM.md` lists an O-ring and a lanyard and no detent or lock. Meanwhile the
r6 numbers show the cap has **6.45 mm of lift available inside 7.39 mm of
headroom** — i.e. the same measurement used to prove the cap cannot be *removed*
on-aircraft proves it *can* disengage on-aircraft under vibration, retained then
only by a Ø2.2 lanyard.

This is the one place I found a defect that was removed from the list instead of
from the design. Everything else I checked (the "deflector nose" replacing the
brush's rejection duty, the two-phase index, the geared drive) is a real
mechanism change, not a rename.

**Fix:** restore the item; add a detent or a quarter-turn lock plus a
cap-present microswitch/Hall reported in `Status`. **Test:** B8 with the cap
fitted and torque-marked.

## RT-16 — MODERATE — Vibration is qualified on the electronics side and unqualified on the mechanical side

§7.1 + B8 are good work (magnet retention ECO-11, sensor-board retention
ECO-12, board first mode, blind-mate fretting). None of it has reached the
mechanical package: `cad/BOM.md` lists "magnets ×9 supermagnete S-03-02-N" with
**no retention specification**, the sensor retention is still a bare M3 grub
bearing on a PCB edge, the agitator is retained by **gravity only** (r6 open
issue 8, "argued behaviour, not tested"), and the cap has no lock (RT-15). A
migrated Ø3 magnet lands in a 1.0 mm rim gap and takes out both the mechanism
*and* the Hall decode that the entire safe-state argument rests on.

**Fix:** fold ECO-11/ECO-12 into `cad/BOM.md` and `dispenser.py` (0.05 mm
interference + retained adhesive; nylon-tipped grub on a clamp plate; a positive
agitator retainer). **Test:** B8 fully loaded, plus a magnet pull-test on the
first article.

## RT-17 — MODERATE — CG and its excursion are nowhere in the package; I computed them so the shock case has an input

MEASURED (mass-weighted from export centroids + the ledger's COTS lines,
drone frame, mount plane at Z = −171):

| load | mass | CG (x, y, z) |
|---|---|---|
| brim (422) | 1490.7 g | (0.58, −4.36, **−266.9**) |
| 250 pellets | 1287.7 g | (0.68, −5.05, **−273.4**) |
| 125 | 1140.2 g | (0.76, −5.70, −277.3) |
| empty | 992.7 g | (0.88, −6.55, **−279.4**) |

So the CG **moves down 6.1 mm and outboard 1.5 mm in y as the hopper empties**,
and the payload loses 23 % of its mass. At aircraft level this is negligible
(≈0.3 mm of aircraft-CG shift for a 20 kg airframe [A]) — the honest finding is
not that CG shift is dangerous, it is that **nobody computed it**, and it is
the required input to RT-13's clip-plate load case: 1.29 kg at 102 mm below the
mating plane with a 6.6 mm in-plane offset.

**Fix:** publish this table in the README mass/power section.

## RT-18 — LOW/MODERATE — The fill ribs are proud internal shelves in the flow zone

MEASURED: the ribs intrude 0.8 mm (z −222.6, in the 68° cone) and 1.05 mm
(z −196.9, in the vertical cylinder wall), and their upper flank is a
**≈45°-from-horizontal upward-facing annular shelf** — in a hopper whose flow
argument is that the wall is 68° and whose outlet only clears the arching rules
"via the active-agitation branch". At 1 mm they will not seat a 12 mm pellet, so
this is a fines shelf and a wall-friction discontinuity rather than an arch
seat — but it is a flow feature added for a *documentation* purpose that no
critic examined.

**Fix:** cut the marks as **recessed grooves** instead of proud ribs
(flow-neutral, same visual), or delete them with RT-5's fill-by-mass.

## RT-19 — LOW — Documentation integrity: measurements quoted with the sign of the claim

Three instances, all in `BUILD-NOTES-r6.md`, all caught by the r6 critics and
all still in the file the packager will fold into `docs/DESIGN.md`:
1. §4: *"10/10 part STLs watertight; assembly STL 16 bodies, 16 watertight"* —
   the builder's own `verify_exports.py` prints `meter_housing … watertight=False`
   and `15/16`. Two independent critics re-ran it.
2. §1: *"payload material inside the shaft column 0.00 mm³"* offered as proof the
   PCB is **in** the shaft (RT-2).
3. §3: *"the pellet is released from a stationary pocket, so zero [lateral
   velocity] is now true by construction"* — the r6 critic measured support loss
   at 14–30 % **into** the 22.5° index move.

**Fix:** the notes generator must print the verifier's *output*, not the
builder's restatement of it; any sentence containing "measured" must be traceable
to a line the tool printed.

## RT-20 — LOW — The "independent checker" is not independent

`cad/verify_exports.py` is written by the same agent in the same round as
`dispenser.py`, and it missed all three defects I reproduced in RT-1 (the 310°
slot, the missing D-flat, the wrong motor pattern) while also failing to flag
its own watertight failure. Its independence claim rests on "types coordinates
in by hand", which protects against transcription errors and nothing else.

**Fix:** derive the checker from the **requirement list and vendor datasheets**
(bolt circle, shaft flat, wall minima, wall-angle rule, aperture count), not
from the model; and make every self-check state what a *failing* part would look
like (the r5 lesson about tests that cannot fail was learned for the clip plate
and not generalised).

## RT-21 — LOW — Count contract residuals worth keeping visible

Disclosed and correctly reasoned in §11 R1–R3; listed here so they survive into
the shipped risk register: (a) `dispensed_verified` counts *objects*, not
pellets, and a Ø8–11 fragment slowed ≥7 % counts as a pellet; (b) the beam is
10 mm above the exit, so a pellet lodged in the last 10 mm reports as delivered
and drops on the *next* target; (c) a pellet and a fragment falling side by side
merge into one dark event on a single-beam head (RT-3), which reads as one
pellet — the payload then dispenses again onto a plant that already has its
dose, and over-application is the regulated direction. B1 with deliberately
fractured pellets covers (a) and (c); (b) needs an exit-clear check.

---

## What I checked and did **not** find a problem with

Stated so the reader knows the silence is deliberate: the power/fuse
coordination and the interlock state table (§2.2–§2.8) are the strongest work
in the package; the FRAM/idempotency/resume semantics are correct and the
15 ms hold-up vs 150 ns write margin is real; the printability statistics
reproduce (I re-measured part volumes to 0.03 % of the BOM); ground clearance
(181.5 mm) and prop clearance are comfortable and independently confirmed;
the pellet is dense enough that wind drift alone (0.09 m per m/s) is *not* the
accuracy problem — hover hold is (RT-4).

## Suggested gate before the package is called rev-0

1. RT-1/RT-2/RT-3 closed or explicitly declared unmet in `README.md`.
2. Bench tests added to the plan: **S-115** (RT-11), **S-116** (RT-12),
   **loaded-hopper solar soak** (RT-6), **humidity/swollen-pellet jam** (RT-7),
   **landing dust cycle in B2** (RT-8), **10 g retention pull** (RT-13).
3. Fill-by-mass procedure + `Fill`/`dispensed_since_fill` in the contract (RT-5).
4. Sim delivered with hover-σ as a swept axis and the accuracy ownership
   levied on the FC/ICD side (RT-4).
