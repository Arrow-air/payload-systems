# RESEARCH — Projectile / Sphere Feed & Metering Mechanisms

Research agent output, 2026-08-06 (rev 2 — expanded with coin-hopper art,
pellet crush-strength data, clogging thresholds, and fragment-wedge prior art
per the 23:03 Thomas directive in `CONTEXT.md`).

Domain: airsoft/BB/paintball hopper and feed systems plus adjacent sphere
singulation art (seed meters, gumball wheels, escapements, coin hoppers,
tablet counters, rotary airlocks, drone dispensers).

Target problem (from `CONTEXT.md`): meter EXACTLY N pellets (N = 1..10, usually
1–3), **sensed** count, from a ≥250-pellet hopper of ~12 mm / 1.18 g molded
herbicide pellets (slightly irregular, friable, dust-shedding), mounted under a
drone, West Texas ranch conditions (dust, heat, wind, vibration).

All facts below are from the cited sources; anything marked ASSUMPTION or
INFERENCE is mine. Comparable-sphere sizes: paintball ≈ 17.3 mm (.68 cal),
airsoft BB = 6 mm, Dragon Egg = 19 mm, gumball = 16–25 mm, corn seed ≈ 8 mm,
US quarter = 24.3 mm dia × 1.75 mm. Our 12 mm pellet sits squarely inside this
envelope, so all of this art scales.

---

## 0. Pellet material data (needed to size shear/crush margins)

Our pellets are the Spike 20P / tebuthiuron class (20 % tebuthiuron pelleted
herbicide for woody brush)
([Spike 20P label, Dow/Corteva via ArborChem](https://www.arborchem.com/images/label-sds/label_Dow_Spike20P.pdf),
[Spike 20P SDS](https://www.arborchem.com/images/label-sds/sds_Dow_Spike20P.pdf)).
The governing formulation patent for compacted, swellable herbicide pellets
gives real mechanical numbers
([US4172714, "Dry compactible, swellable herbicidal compositions and pellets
produced therefrom"](https://patents.google.com/patent/US4172714A/en)):

- **Crush load:** pellets are specified to *resist* crushing at loads "less
  than about **7500 grams** or **3.7 kg/cm²**"; worked examples measured
  **6.0 – 11.5 kg** crush load (Example 1: 11 000 g; Example 4: >11.0 kg).
  Test = pellet laid horizontally between two parallel steel platens, loaded
  to failure. Sample geometry in the patent: 16 mm dia × 9–11 mm cylindrical
  pellet compacted at 1400–1450 kg/cm².
- **Impact:** "normally resist breakage for 5 drops" from **3 m onto concrete
  or steel**; better examples 5→>10 drops.
- **Moisture:** 3.5–5.0 % weight gain in 24 h at 88 % RH; on wetting the
  pellets "crack immediately… and swell to about 2 to 3 times their original
  volume", and when dried "do not rebond but remain crumbled."

**Derived design numbers (INFERENCE, flag as such downstream):**
- Take **60 N** (≈6 kg) as a conservative lower-bound crush force for an intact
  pellet, **110 N** as upper bound. A *fragment* wedged at a shear line
  presents less cross-section than a whole pellet; ASSUMPTION: design the
  actuator to deliver ≥ **150 N** equivalent at the pocket radius so shear is
  a genuine backstop with ≥1.4× margin on the worst case. This is the number
  the pocket-wheel torque budget must beat (CONTEXT.md item 2).
- Swelling on wetting is a **hard operational constraint**: a hopper that takes
  rain or dew will convert its charge into a 2–3× volume crumbled mass and
  cannot be un-jammed mechanically. Sealing/desiccant is a requirement, not a
  nicety.
- 3 m drop survival ×5 means normal drone vibration will not itself pulverise
  pellets, but repeated micro-impacts inside a hard-walled meter will generate
  dust (INFERENCE from the "attrition" behaviour implied by the label warning
  that dust irritates the respiratory tract, per the SDS).

---

## 1. Rotating metering disc / cell wheel (gumball machine, seed plate)

**How it works.** A horizontal (or inclined) disc with pellet-sized pockets
rotates under the hopper. Gravity drops one sphere into each pocket; rotation
carries the pocket over a discharge chute where the sphere falls out. Gumball
machines are exactly this: a handle drives a gear/sprocket engaging the ribs on
a wheel, the wheel indexes **120° per cycle**, and one of three apertures
aligns with the chute to release the gumball
([US6536623B1](https://patents.google.com/patent/US6536623B1/en)). That patent
also documents **agitator springs mounted on the wheel's upper surface** to
stir the ball mass above the pockets — a free anti-arching feature.

Mechanical planter seed meters are the precision version: a **flat** disc plus
a **singulator that rides on the edge of the disc and knocks off extra seeds**,
achieving >99 % singulation in corn and soybean
([Precision Planting eSet](https://www.precisionplanting.com/products/planters/eset)).
Flat-disc designs are explicitly chosen because they "eliminate variability in
seed spacing due to irregularities in seed shape or size," an improvement over
traditional cell wheels that were sensitive to seed size variation (same
source; corroborated by
[NDSU seed singulation study](https://www.ndsu.edu/sites/default/files/fileadmin/aben/SeedSingulation.pdf)).

**Count accuracy.** Highest of any surveyed family. N pellets = N pocket
indexes of a stepper/servo; count is inherently discrete and open-loop-honest.
Seed meters: >99 % singulation at field speed. Gumball wheels: 1 per cycle,
purely mechanical, no electronics.

**Jam behavior.** The classic failure is documented verbatim in the gumball
patent: problems arise from "a gumball not being properly seated in the
dispensing mechanism," either "an extra gumball becoming partially seated in a
dispensing wheel aperture, or by becoming lodged between an aperture and one of
the other parts" ([US6536623B1](https://patents.google.com/patent/US6536623B1/en)).
**This is precisely the fragment-overfill wedge jam Thomas raised on
2026-08-06 23:03** — it is a known, named failure mode of this family, not a
hypothetical. See §10 for the countermeasures the art actually uses.

**Complexity.** Low-moderate: one motor, one disc, one wiper/brush, one sensor.
Fully 3D-printable. No stored spring energy.

**Adaptability to our pellet.** Excellent, and the best fit overall. Pockets
size parametrically to `PELLET_D`. Weakness = the wedge jam, which must be
engineered against explicitly.

---

## 2. Brush plate / compliant wiper over the pocket wheel (COTS gumball art)

**How it works.** Commercial gumball wheels ship as a three-part stack —
**spacer + gum wheel + brush plate** — where the brush plate is a bristle/
elastomer plate that covers the wheel aperture directly over the hopper
opening, often with two springs
([Gumball Machine Warehouse — wheel & brush plate](https://www.gumball-machine.com/products/gumball-wheel-brush-plate),
[product wheel types](https://www.gumball-machine.com/blogs/articles/the-three-types-of-product-wheels-in-a-gumball-machine)).
Vendors state the brush plate "keeps the candy inside the machine so that it
does not come out when the machine is not in use, **reduces jams and incorrect
feeding**, and controls even dispensing together with the wheel," and that "a
wheel without a brush is useless."

**Why it matters for us.** This is the COTS, mass-produced instantiation of
"compliant overfill relief at the pocket exit." A bristle field is compliant in
the radial direction (a proud fragment pushes bristles aside or gets swept
back) but stiff enough to strip a partially-seated second sphere. Seed meters
do the same job with a spring-loaded singulator riding the disc edge (§1).

**Count accuracy contribution.** It is what turns "roughly one per pocket" into
"exactly one per pocket" by rejecting doubles/partials before the shear line.

**Jam behavior.** Failure mode is bristle wear/dust matting over a season;
ASSUMPTION: bristles hold up better than a rubber lip against abrasive
herbicide dust, but this is untested for our material.

**Complexity.** Trivially low. Brush strip is a consumable, replaceable part.

**Adaptability.** Direct. ASSUMPTION: a nylon/PBT strip brush with ~10 mm
free bristle length, interference ~2–3 mm over the disc face.

---

## 3. Coin hopper (the closest exact-count analog in existence)

**How it works.** A bulk reservoir of loose discs sits on a motor-driven
**rotating disc with pockets**; each pocket carries exactly one coin to a payout
chute. This is a pocket wheel dispensing an exact commanded count from a bulk,
dirty, unsorted mass — structurally identical to our problem
([US5516293 gaming machine coin hopper coin sensor](https://patents.google.com/patent/US5516293A/en),
[US9105140 coin hopper](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9105140),
[US7059957 coin hopper device](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7059957),
[Crane Payment Innovations H2 nano payout hopper manual](https://www.cranepi.com/en/system/files/Support/OM_h2nano_F51_EN_2-1.pdf)).

**Count accuracy — the exact pattern we should copy.** From US5516293: an
optical switch (LED source one side, detector the other) sits at the **payout
chute**; as each coin passes it momentarily blocks the beam, the detector
registers, and the counter increments. "When the number of coins detected
equals a predetermined value, the counter sends a signal to **stop the rotation
of the disc** and cease coin payout." That is: **the count sensor, not the step
count, terminates the dispense.** This is exactly the "commanded count must be
VERIFIED (sensed), not assumed" requirement in CONTEXT.md, solved in a shipping
product family for 40 years.

**Jam behavior — also directly copyable.** Two documented anti-jam strategies:
1. **Timeout-based**: rotation time from start is compared against a
   predetermined period; if exceeded, "the motor rotates in reverse direction
   during a predetermined time to break up any jam."
2. **Current-sense-based**: a current sensor "detects the effect of a jam on a
   motor and initiates a **momentary reversal** of the drive direction,
   followed by a return to normal drive."

Note that both are *reverse-oscillate recovery* and both are triggered without
a dedicated stall IC — motor current alone is sufficient. Cheap and proven.

**Complexity.** Low: one geared DC motor or stepper, one pocketed disc, one
optical gate, one current shunt. Whole COTS units are €30–€80.

**Adaptability.** Very high conceptually. Caveat: coins are hard, non-friable,
and self-lubricating; our pellets are friable and shed abrasive dust, so the
reverse-oscillate recovery must not grind a fragment into powder that packs the
clearance (INFERENCE). Also: coin hoppers accept the coin being *bent/shaved*
and simply reject-and-retry — the same tolerance philosophy applies.

---

## 4. Escapement / alternating-pawl singulator on a gravity column

**How it works.** Pellets queue single-file in a gravity tube; two fingers
alternate: the lower finger releases the bottom sphere while the upper finger
holds the column, then they swap. One cycle = exactly one part. Standard
industrial parts-feeding art; escapements "present, isolate, place, stack, or
singulate parts," with options including cross shuttles, finger releases,
linear actuators and rotary indexers
([Bellco Feeders](https://www.bellcofeeders.com/vibratory-bowl-feeders),
[Automation Devices — parts escapements and nests](https://www.autodev.com/parts-escapements-and-nests)).
The patent literature for ball dispensers is explicit: a solenoid extends "a
horizontal arm with upper and lower legs to control which ball moves down a
chute, permitting only one ball at a time to pass"
([US4575092 ball dispenser](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4575092)); a
pawl-based version uses "a pivotally mounted plate with first and second
ball-abutment pawl portions"; and a solenoid-driven scape wheel gives motion
"controlled and independent of the electrical pulse length"
([US4128949 toy clock using marbles](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4128949),
[RoyMech escapement reference](https://www.roymech.co.uk/Useful_Tables/Cams_Springs/Escapements.html)).

**Count accuracy.** Exactly one per cycle by geometry. N pellets = N cycles.
Positive-displacement, no reliance on flow rate.

**Jam behavior.** The escapement itself rarely jams, but it *displaces* the
failure upstream to the hopper→tube throat, where 12 mm spheres bridge (see
§9). The airsoft M249 box-mag is the cautionary tale: "the two inner pieces
that form the trough allow BBs to double up and jam in the opening to the
feeding mechanism," resolved in the field by *striking the magazine*
([Airsoft Society — M249 feeding problem](https://www.airsoftsociety.com/threads/help-needed-with-m249-aeg-feeding-problem.103926/),
[Airsoft Forums UK — A&K auto-winding box mag fault](https://airsoft-forums.uk/topic/45092-ak-m249-auto-winding-box-mag-fault/)).
An escapement therefore **requires** an agitated/anti-bridging throat above it.

A second, subtler risk: a fragment in the column can hold the upper pawl open
while the lower pawl releases, producing a **double-drop** — a miscount, not
just a jam (INFERENCE).

**Complexity.** Lowest of the exact-count options: one servo, a two-lobe cam,
one tube.

**Adaptability.** Good with caveats. Tube ID ~14 mm passes a 13 mm worst-case
pellet single-file (two 12 mm pellets cannot sit side by side in 14 mm) —
ASSUMPTION per the ±1 mm tolerance in CONTEXT.md. Needs a fragment/dust relief
slot along the tube.

---

## 5. Spring-follower magazine (airsoft mid-cap / hi-cap)

**How it works.** A coil spring pushes a follower that keeps a column of
spheres pressed toward the feed lips. The airsoft **hi-cap** variant adds a
wound clockwork spring driven by a knurled wheel on the base, with an
anti-reverse ratchet (the audible clicks) and a **slip clutch** that lets the
wheel skip when fully wound; the spring drives an internal gear/toothed wheel
that lifts BBs from a loose reservoir up a chute
([Pyramyd Air — how airsoft and BB gun magazines work](https://www.pyramydair.com/blog/2020/09/how-airsoft-and-bb-gun-magazines-work/),
[Airsoft Master — hi-cap vs mid-cap](https://www.airsoftmaster.com/airsoft-magazine-high-cap-vs-mid-cap/),
[JVAN beginner's guide](https://www.jvanairsoft.com/blogs/news/a-beginners-guide-to-airsoft-magazines-types-features-and-how-to-choose)).

**Count accuracy.** None inherent — it is a *presenter*, not a meter. It only
guarantees a pellet is at the exit; something else must count. Hi-caps are
documented as needing rewinding every 20–50 shots to keep the track full and
feeding consistently (Pyramyd Air, above) — i.e. the mechanism degrades
gracefully into starvation, which for us would be a silent under-count.

**Jam behavior.** Spring pressure actively fights bridging in the column
(good), but constant pressure on a stack of friable pellets under hours of
drone vibration will abrade and generate dust (INFERENCE, supported by the
attrition/dust warnings in the Spike 20P SDS). The winding mechanism itself is
cited as a common point of failure.

**Complexity.** Low mechanically, but a 250-pellet spring column is
geometrically impossible: 250 × 12 mm ≈ **3.0 m** of column (INFERENCE, simple
arithmetic). A spring follower can therefore only ever be a *sub-stage*
(5–15 pellets) buffering between a bulk hopper and the meter.

**Adaptability.** Use only as an optional buffer/anti-starvation stage. Not a
solution on its own.

---

## 6. Agitated gravity-feed hopper (paintball agitating loaders)

**How it works.** Bulk hopper with a gravity neck; a motorized paddle/impeller
stirs the ball mass to break arches at the outlet. Agitators "can take various
forms, including paddle wheels, arms, paddles, wires, fins, and vibrating
members," expressly to "increase feed rates and prevent paintball jams"
([US7694669B2 — paintball loader feed mechanism](https://patents.google.com/patent/US7694669B2/en)).

**Count accuracy.** None — it delivers availability, not count. Pair with a
break-beam gate (§8) to count what actually leaves.

**Jam behavior.** Excellent for bulk flow; this is 30 years of field experience
with dirty, slightly out-of-round 17 mm spheres in mud and dust. It fixes
arching, not wedging.

**Complexity.** Very low: one geared motor + soft paddle in the cone.

**Adaptability.** Excellent as the BULK stage: 250+ pellet hopper → steep smooth
cone → intermittently agitated throat → meter. Run agitation only on
starvation detection so pellets aren't churned (and abraded) continuously.

---

## 7. Force-feed loaders (Dye Rotor carousel; Virtue Spire drive cone)

**How it works.** Active motor-driven feeding maintaining positive pressure on
the ball stack, as opposed to gravity/agitation. Two production architectures:

- **Dye Rotor**: "the combination of the loader's constant feed carousel and
  the opposing rotation of the Rotor center arm," 30+ balls/s, plus a **patented
  spring-loaded floor tray** and **adjustable feed tension**; a manual
  **Sharkfin jam-release trigger** on the underside "releases jammed paint
  immediately… in the rare event of a ball jam caused by oversized or out of
  round paint"
  ([DYE Rotor R2](https://shop.dyepaintball.com/collections/rotor-r2),
  [ANSgear Rotor R2](https://ansgear.com/dye-rotor-r2-paintball-loader-dyecam/)).
- **Virtue Spire**: drive cone built from "a combination of nylon and flexible
  rubber," with **5 long flexible fingers** and a **9-ball raceway**; a
  **spring-loaded anti-jam drive slides underneath and pushes jams out of the
  way before they occur**; when a ball deforms, "the rubber fingers guide it
  gently, clearing potential jams." The IR2 uses **three IR sensors behind
  polycarbonate** monitoring the paint stack and feeding *proactively* rather
  than reactively
  ([Virtue Spire IR² product page](https://virtuepb.com/products/virtue-spire-ir2-loader-black),
  [ANSgear Spire IR2 + spring ramp](https://ansgear.com/virtue-spire-ir2-paintball-loader-w-speed-feed-spring-ramp-combo/)).

The underlying patent shows the compliance trick generically: rigid projections
"each connected to a drive shaft by an **elastic member**," projection length
≥ half a ball diameter, where the elastic member lets a projection "pass by
stationary or jammed paintballs **without breaking them**" — i.e. the elastic
member is a **passive torque limiter**, with no clutch or reverse required
([US7694669B2](https://patents.google.com/patent/US7694669B2/en)). The same
patent contemplates "mechanical, contact, piezoelectric, optical, or infrared"
sensors detecting ball presence/absence or stack movement under microprocessor
control.

**Count accuracy.** Not counted at the loader. Irrelevant to us directly.

**Jam behavior.** Best-in-class *philosophy*: (a) compliance everywhere the
mechanism touches a fragile sphere, (b) proactive sensing rather than
reactive, (c) a **manual mechanical override** for when electronics or torque
can't clear it (Sharkfin trigger).

**Complexity.** High: carousel/cone, torque-managed drive, control board.
Overkill for 1–10 pellets at ~1 Hz.

**Adaptability.** Don't copy the mechanism; copy four ideas — elastic-member
torque limiting on anything that touches a pellet; proactive IR stack sensing;
a manual jam-release lever accessible without tools on the flight line;
"feed the worst pellets imaginable" as the acceptance criterion.

---

## 8. Auger / screw feeder

**How it works.** A screw in a tube moves ~one flight-pitch of material per
revolution. Widely used for fish/pet pellet feeders; an ESP32 auger feeder
study established "strong linear relationships (R² > 0.997) between servo
rotation time and feed dose across three pellet sizes (1, 2, 3 mm)"
([ESP32 IoT auger-based automatic feeder for fish pellets](https://www.researchgate.net/publication/399269050_ESP32_IoT_Auger-Based_Automatic_Feeder_for_Fish_Pellets)).

**Count accuracy.** Poor for exact discrete counts — an auger meters *volume*,
not units, unless the flight pocket is sized to exactly one sphere, at which
point it has become a helical cell wheel (§1) with far more sliding contact.
Comparative field data is unfavourable for our conditions: auger feeders held
"12 % variance" with varied diets, but "consistency cratered when food sat
beyond 2 weeks — oxidation and clumping caused **35 % more missed feeds
compared to rotary systems** in longevity trials"
([Fish Feeder Sense — rotary vs auger](https://www.fishfeedersense.pro/blog/fish-feeder-reviews-comparisons/rotary-vs-auger-precision-feeding)).
Rotary disk systems by contrast "rotate to release pre-measured portions,
minimizing clumping"
([Alibaba product-insights, fish food automatic feeder](https://www.alibaba.com/product-insights/fish-food-automatic-feeder.html)).

**Jam behavior.** The shear line between flight edge and tube wall crushes
friable pellets; fines pack the screw root. Bad match for a dust-shedding
molded pellet.

**Complexity.** Low part count, high friction/wear.

**Adaptability.** **Not recommended** as the meter. Possible as a throat
agitator only.

---

## 9. Rotary airlock / star feeder (industrial pocket wheel — the wedge-jam
   engineering base case)

**How it works.** A housing with end plates containing "a multi-vane rotor with
**six or more pockets**"; the rotor indexes bulk solid from an inlet above to
an outlet below. Typical rotor-to-housing clearances are **0.004–0.006 in
(0.10–0.15 mm)** — "roughly the thickness of a strand of coarse hair"
([Powder & Bulk Solids — rotary airlock valve principles and rotor design](https://www.powderbulksolids.com/valves-gates-airlocks/rotary-airlock-valve-principles-and-rotor-design),
[Powderprocess.net — airlock rotary valve design fundamentals](https://www.powderprocess.net/Pneumatic_Transport/Airlock_Rotary_Valve.html)).

**The directly relevant fact (CONTEXT.md 23:03 directive).** The industry's
named solution to "a particle enters the rotor/housing gap and seizes the
rotor" is an **inlet moldboard**: for coarse particles such as plastic pellets,
straight-through rotary valves "feature a strategically designed inlet
moldboard that **prevents solid particles from entering the gap between the
rotor and valve housing**, thereby preventing the rotor from getting stuck or
seizing" (Powder & Bulk Solids, above). Star valves are also specifically
credited with handling "fragile and friable materials with **minimal
degradation**, with minimal shear occurring"
([DARKO — the star discharge valve](https://www.darko-tech.com/the-star-discharge-valve-the-essential-airlock-in-bulk-solids-handling/),
[BulkInside — rotary airlock feeders](https://bulkinside.com/bulk-solids-handling/valves-gates-airlocks/rotary-airlock-feeders-essential-components-in-pneumatic-transport-systems-chemical-industry-and-boiler-feed-systems/)).

**Translation to our design.** The moldboard is a **fixed relief/scraper
geometry at the inlet edge**, positioned so that any particle standing proud of
the pocket is deflected back into the hopper *before* the pocket reaches the
close-clearance arc. Combined with the gumball **brush plate** (§2) and the seed
**singulator** (§1), that is three independent industries converging on the
same answer: *reject at the inlet edge, never rely on shearing later.*

**Count accuracy.** Airlocks meter volumetric throughput, not counts — but a
6-pocket rotor with one pellet per pocket is exactly our meter.

**Jam behavior.** Seizure is the dominant failure and is designed out at the
inlet, not at the shear line.

**Complexity.** Moderate; the geometry is simple, the tolerance discipline is
the hard part. NOTE: airlock clearances (0.1–0.15 mm) are set for *air* sealing.
We do not need an air seal, so we can open the clearance substantially, which
strictly reduces wedge risk (INFERENCE — quantify against smallest credible
fragment; a clearance larger than the smallest fragment simply passes it).

**Adaptability.** High. This is the closest industrial cousin to the proposed
pocket wheel and its published failure modes should be treated as ours.

---

## 10. Anti-jam / anti-bridging geometry (cross-cutting)

**Outlet-to-particle ratio — hard numbers.**
- Classic Jenike engineering rule: circular hopper outlets should be **≥ 6×
  the largest particle diameter** to prevent mechanical arching
  ([Chemical Engineering — Facts At Your Fingertips: hopper outlet geometry and
  arching](https://www.chemengonline.com/facts-fingertips-hopper-outlet-geometry-arching/)).
- Granular-physics measurement for **spheres specifically** is more permissive:
  in 3D silo experiments the mean avalanche size diverges at an outlet of about
  **5 bead diameters**, and one analysis reports **no blockage above a ratio of
  4.94 ± 0.03**; another gives 3–5× for trouble-free glass-bead discharge
  ([Zuriguel et al., Phys. Rev. E 71, 051303 — jamming during the discharge of
  granular matter from a silo](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.71.051303),
  [Invited review: clogging of granular materials in bottlenecks (arXiv
  1412.5806)](https://arxiv.org/pdf/1412.5806)).
- Important caveat from the same literature: some authors argue **no truly
  critical size exists** — jamming probability decays but never reaches zero —
  and that grain *material* properties do not affect arch-formation probability
  (Zuriguel, above). So: treat 5–6 d as a *design floor*, not a guarantee, and
  always pair with an unjamming action.
- Vibration is a documented unjammer: "role of vibrations in the jamming and
  unjamming of grains discharging from a silo"
  ([arXiv 0907.4871](https://arxiv.org/pdf/0907.4871)). A drone airframe supplies
  vibration for free (INFERENCE — this cuts both ways: it also settles/packs).
- An **obstacle placed above the outlet** measurably reduces clogging
  ([Silo clogging reduction by placing an obstacle above the outlet](https://www.researchgate.net/publication/255484446_Silo_Clogging_Reduction_by_Placing_an_Obstacle_Above_the_Outlet))
  — a cheap, static, zero-power anti-arch feature worth adopting in the cone.

**Numbers for our pellet.** 5–6 × 12 mm ⇒ a *bulk* outlet of **60–72 mm** for
arch-free gravity flow. Any single-file throat (~14 mm, ratio 1.17) is deep in
the clogging regime **by design** — that is fine and intentional for a metering
throat, but it means the transition must be actively agitated or pocket-swept,
never relied on as free-flowing gravity.

**Compliance is the universal theme.** Every successful design in this survey
puts a compliant element where the mechanism touches a sphere: elastic-member
projections (US7694669), nylon/rubber Spire fingers, spring-loaded anti-jam
drive and spring-loaded floor tray (Spire/Rotor), spring-loaded singulator
(eSet), brush plate (gumball), agitator springs on the wheel (US6536623).

**Detect + recover.** Two proven low-cost patterns:
- **Motor current / timeout → momentary reverse**, as in coin hoppers (§3).
- **StallGuard sensorless load sensing** on a TMC2209: the driver "continuously
  monitors motor load… measures back-EMF," and asserts **DIAG** on stall
  ([TMC2209 datasheet rev 1.08, Analog Devices](https://www.analog.com/media/en/technical-documentation/data-sheets/tmc2209_datasheet_rev1.08.pdf),
  [Klipper TMC drivers doc](https://www.klipper3d.org/TMC_Drivers.html)).
  **Critical limitation for us**: StallGuard "works best at medium motor
  speeds. For very slow speeds (less than 10 RPM) the motor does not generate
  significant back EMF and the TMC cannot reliably detect motor stalls," and it
  also fails at very high speed (Klipper doc). A pocket wheel indexing at
  ~1 pellet/s is likely **below** the reliable StallGuard band — so
  **current-sense or encoder-based stall detection should be the primary**, with
  StallGuard as a secondary if the gear ratio puts motor RPM in band.
  This is a concrete correction to the CONTEXT.md item-3 suggestion.

**Manual override.** Dye's Sharkfin jam-release trigger (§7) and Empire's
Rip Drive manual wheel are the field-proven pattern: a tool-free, gloved-hand
mechanical clearing action. Cheap insurance for a ranch operation.

---

## 11. Count verification sensing (requirement: sensed, not assumed)

**Break-beam is the proven art.** Paintball anti-chop "eyes": a transmitter on
one side of the breech and receiver opposite; "when a paintball drops into the
breech, it breaks this beam, signaling to the marker's circuit board." The
system re-confirms the beam is restored after each shot before allowing the
next, which is a **state-machine, not an edge count** — it verifies both
presence and clearance
([US7765998B2 — anti-chop eyes for a paintball marker](https://patents.google.com/patent/US7765998B2/en),
[Planet Eclipse break-beam breech sensor kit](https://adrenalinepaintballairsoft.com/products/planet-eclipse-ego-etek-geo-bbbs-break-beam-breech-sensor-eye-kit-spa990007b000)).

**Dust is the known enemy, and the industry answer is documented.** Tablet
counters use photoelectric/IR "light curtains" where each pill breaks the beam
to register a count, with error rates of **0.1 % or less** per batch. But:
"dust and powder can cover the photoelectric sensors, weakening or blocking the
detection signal," so vendors ship **anti-dust optics** and, notably,
**electrostatic-field sensors that work in dusty environments and can tell
broken or half tablets apart from whole ones**
([Kenwei — pill counter machine guide](https://www.kenweigroup.com/blog/ultimate-guide-to-pill-counter-machine-2026-choosing-the-best.html),
[iPharmachine — how a tablet counting machine works](https://www.ipharmachine.com/tablet-counting-machine-principle),
[Ruida — tablet counting machine buying guide](https://ruidapacking.com/tablet-counting-machine-buying-guide/)).
Slat counters are preferred where "mechanical flow reduces bounce and
double-drops" (Ruida) — a direct argument for a pocket wheel over a free-fall
stream.

**Airsoft/consumer proof point.** COTS electric BB speed loaders count to a
commanded number and auto-stop: the GunPower unit "counts in real time the
amount of BBs being fed," reads "up to 30 rounds in 1 second," and "can be
programmed to feed exact amounts of BBs into magazines and auto stops when
round count is met"
([Airsoft Station — GunPower electric BB speed loader](https://airsoftstation.com/gunpower-high-speed-electric-automated-airsoft-bb-speed-loader-black/),
[Evike listing](https://www.evike.com/products/94026/)). Exact-count dispensing
of small spheres from a bulk reservoir is a solved consumer-price problem.

**Design notes (INFERENCE):**
- Put the beam across the **drop chute below the meter** so it counts pellets
  that actually left, and gate the dispense on sensed count (coin-hopper
  pattern, §3), not on step count.
- **Modulated/carrier IR** (as in anti-chop eyes) to reject West Texas sunlight
  through an open drop chute.
- **Recessed optics with a purge/relief geometry** and, ideally, redundant
  beams at 90° so a dust film on one lens doesn't blind the count.
- Discriminate fragments: a half pellet gives a shorter beam-break duration
  than a whole one at the same drop velocity — **beam-break duration
  thresholding** is a cheap software fragment discriminator (INFERENCE;
  analogous to the electrostatic broken-tablet detection above).
- Count must stay truthful through a reverse-oscillate recovery: only increment
  on a *complete* break→restore cycle in the forward direction, and suppress
  counting while the motor is commanded in reverse (INFERENCE).

---

## 12. Adjacent drone-dispenser art (existence proofs at our scale)

**Drone Amplified IGNIS** — the closest fielded system. IGNIS III Mini
datasheet, verified numbers
([Drone Amplified IGNIS system datasheet](https://droneamplified.com/ignis-system-datasheet/),
[IGNIS III](https://droneamplified.com/ignis-iii/)):
- Hopper capacity **225 spheres**; sphere **19 mm dia, 2.4 g**
- Drop rate **up to 120 spheres/minute**
- Payload empty weight **1.25 kg** (with camera); full UAS loaded 7.46 kg
- Reload time 2–5 minutes; each sphere is individually **punctured and injected
  with 0.2 mL** of glycol before release — i.e. the mechanism handles each
  sphere *individually and deterministically*, not as a stream.
- Larger IGNIS variants are reported at **450 Dragon Eggs (~13 lb)**
  ([Vertical Mag — controlled firepower](https://verticalmag.com/features/controlled-firepower-how-aerial-ignition-equipment-aids-the-fight-against-wildfires/amp/),
  [Popular Science](https://www.popsci.com/technology/drones-wildfires/),
  [DOI Interagency Aviation Tech Bulletin IA TB 24-01](https://www.doi.gov/sites/default/files/iatb-2024-01.pdf)).
- **Read-across to our budget**: IGNIS does 225 × 19 mm spheres, per-sphere
  processing, plus a puncture/injection system and a camera, in 1.25 kg. Our
  1.5 kg ceiling for 250 × 12 mm spheres with *no* injection stage is
  comfortably achievable (INFERENCE by comparison).
- No jam-handling or reliability claims are published in the datasheet
  (verified absence, not evidence of absence).

**UAV seed dispensers.** Academic template: a cylindrical hopper with a
**motor-driven disc** for controlled seed release; one reported configuration
had 50-seedball capacity dispensed over a 100 s flight
([Design of a Seed Dispenser for Unmanned Aerial Vehicles, IFAC-PapersOnLine
2025](https://www.sciencedirect.com/science/article/pii/S2405896325024668) —
NOTE: publisher blocks automated fetch; details taken from the indexed
abstract/summary, treat as second-hand). Review of the field:
[The mechanism of drone seeding technology: a review](https://www.researchgate.net/publication/353192140_THE_MECHANISM_OF_DRONE_SEEDING_TECHNOLOGY_A_REVIEW).

**Commercial granular spreaders** (XAG JetSeed and similar) use an "embedded
rolling feeder" to guarantee uniform output plus air-jet projection
([XAG JetSeed](https://www.xa.com/en/jetseed)). These are broadcast spreaders —
uniform *rate*, not exact *count* — so they are the wrong architecture for us,
but they confirm rolling/pocket feeders survive drone vibration and field dust.

---

## 13. Ranked synthesis for our problem

**Recommended architecture — three stages, each from proven art:**

1. **Bulk stage.** ≥250-pellet hopper (design for more; capacity is a positive
   goal per CONTEXT.md), steep smooth walls, a static anti-arch obstacle above
   the throat, and an intermittent **soft-paddle agitator** run only on
   starvation detection (paintball agitated-loader art §6, obstacle art §10).
   Sealed against moisture — non-negotiable given 2–3× swell on wetting (§0).
2. **Metering stage.** **Stepper-indexed pocketed disc** (gumball/seed-meter/
   coin-hopper/rotary-airlock art §§1,2,3,9), with:
   - an **inlet moldboard/relief chamfer** at the pocket exit from the hopper
     zone that deflects proud fragments back into the hopper *before* the
     close-clearance arc (rotary-airlock art §9) — this is countermeasure #1
     for the 23:03 wedge-jam directive;
   - a **brush plate / compliant wiper** over the pocket (§2) — the COTS,
     mass-produced version of the same idea, and countermeasure #1b;
   - housing clearance deliberately **larger** than an airlock's 0.1 mm, since
     we need no air seal — pass small fragments rather than trap them (§9);
   - actuator torque sized to exceed pellet crush force with margin as a
     **backstop only**: ≥150 N equivalent at the pocket radius against a
     60–110 N pellet crush load (§0) — countermeasure #2.
3. **Verification + recovery.** Modulated IR **break-beam in the drop chute**,
   with the sensed count (not the step count) terminating the dispense
   (coin-hopper pattern §3, anti-chop eye art §11); **motor-current stall
   detection** as primary with reverse-oscillate recovery (coin-hopper art §3),
   StallGuard only as a secondary because our indexing speed is likely below
   its reliable band (§10) — countermeasure #3; count suppressed during reverse
   so recovery cannot create phantom counts; plus a **tool-free manual
   jam-release lever** (Sharkfin pattern §7).

**Runner-up:** dual-pawl escapement on a short gravity column (§4). Fewer
parts, cleanest positive displacement, and the only option with no
close-clearance shear arc at all — so it is structurally immune to the wedge
jam. Its weaknesses are (a) it still needs an agitated throat above it, and
(b) a fragment holding a pawl open causes a *double-drop miscount*. Worth
keeping alive as the fallback if the wedge jam proves un-engineerable.

**Rejected:** auger/screw (crushes friable pellets, volumetric not discrete,
35 % more missed feeds vs rotary in longevity trials §8); vacuum singulation
(blower mass/power, dust ingestion, 1.18 g is far heavier than a corn seed);
spring-follower magazine as a primary (3 m of column for 250 pellets §5);
full force-feed loader (complexity unjustified at ~1 Hz §7).

---

## 14. Open unknowns to close by test

1. Actual crush load of *our* pellets (§0 numbers are from the formulation
   patent for a 16 mm cylindrical pellet, not our 12 mm sphere) — measure on a
   bench press with a load cell before finalising torque margin.
2. Smallest credible fragment size after a full sortie of vibration — this sets
   both the housing clearance and the beam-break duration threshold.
3. Dust accumulation rate on the IR optics over a 250-pellet sortie.
4. Diameter distribution of the real molded pellets (CONTEXT.md assumes ±1 mm).
5. Whether airframe vibration net helps (unjamming, arXiv 0907.4871) or hurts
   (packing/attrition) in our hopper — instrument and measure, don't guess.
6. Brush-plate bristle wear/matting life against abrasive herbicide dust.
