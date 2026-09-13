# RESEARCH — Precision-Ag Seed Metering & Discrete Singulation Mechanisms

Scope: mechanisms capable of dispensing **exactly N (1–10) 12 mm / 1.18 g molded
pellets** from a **≥250-pellet hopper**, on a **drone**, in **dusty West Texas
ranch conditions**, within the ICD budget (12VSW behind a **2 A fuse = 24 W max**,
no 5 V, no UART; ≤1.5 kg total incl. 295 g of pellets).

Method: web research on production planter meters (John Deere, Kinze, Precision
Planting), drone/aerial discrete-object dispensers (aerial ignition PSDs, UAV
bait/briquette dispensers), and adjacent counting industries (pharma tablet
counters, lab seed counters). Every fact is cited. Anything not cited is marked
**DERIVATION** (with the math shown) or **ASSUMPTION** (with reasoning).

---

## 0. Pellet physical baseline (DERIVATION from CONTEXT.md ground truth)

- Sphere volume: V = (4/3)π(6 mm)³ = **904.8 mm³ = 0.905 cm³**
- Bulk density of pellet material: ρ = 1.18 g / 0.905 cm³ = **1.30 g/cm³**
  (consistent with a clay/mineral-carrier pelleted herbicide — plausible, not verified)
- Weight force per pellet: W = 1.18e-3 kg × 9.81 = **0.0116 N**
- Hopper volume for 250 pellets: 250 × 0.905 cm³ = 226 cm³ of solid.
  At random-loose sphere packing (~0.55–0.60): **0.38–0.41 L**. CONTEXT's
  "≥0.5 L" is conservative and safe; use 0.5 L with headspace for agitation.
- Single-file column length for 250 pellets at 13 mm pitch: **3.25 m**
  (drives the helical-magazine concept in §7).

**Key scaling fact for everything below:** a corn kernel is ~0.30–0.35 g. Our
pellet is **~3.5–4× the mass and ~2.5× the diameter** of the seed that every
production planter meter is optimized for. No production meter takes this
pellet without a redesigned disc/cell — all "adaptability" ratings below are
about whether the *principle* scales, not the hardware.

---

## 1. Vacuum disc meter (Kinze True Rate/EdgeVac, JD ProMAX/vSet, PP eSet)

**How it works.** A vacuum plenum sits behind a rotating disc pierced with a ring
of apertures. Vacuum pulls one seed onto each aperture as the disc passes through
the seed pool; the seed rides up out of the pool; at the discharge point the
vacuum is cut off by a seal and the seed drops. Two disc styles: **celled discs**
(indentation around each hole, holds seed at lower vacuum) and **flat discs** with
a **singulator** — a spring-loaded brush/blade riding the disc face that knocks
extra seeds off. ([USPTO 7,334,532](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7334532),
[Precision Planting eSet](https://www.precisionplanting.com/products/planters/eset),
[Kinze — Why upgrade to vacuum meters](https://www.kinze.com/why-upgrade-to-vacuum-seed-meters/))

**Count accuracy.** Best-in-class of all ag meters. Flat disc + singulator: **>99%**
singulation in corn and soybeans; vacuum meters "consistently 98–99%" when properly
adjusted; Kinze True Rate claims **>99% at up to 8 mph**.
([Kinze](https://www.kinze.com/why-upgrade-to-vacuum-seed-meters/),
[Kinze meter comparison](https://www.kinze.com/which-seed-meter-is-right-for-you/))
Note what 99% means: **~1 error per 100 seeds**. For a 3-pellet drop that is a
~3% chance of a wrong-count drop — *not* good enough on its own for a
"verified exactly N" requirement. Sensing (§9) is mandatory regardless of meter.

**Jam behaviour.** Does not jam mechanically (no pinch points); it **fails soft**
as *skips*. Failure modes are aperture plugging and coating/dust buildup: seed
treatment dust "makes it more difficult to entrain the seed over the apertures"
([USPTO 7,334,532](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7334532));
field practice is to add talc/graphite lubricant and to clean discs when
"seed treatment is building up on the disc"
([Sloan seed lubricant guidelines](https://sloansupport.com/2023/04/10/seed-lubricant-guidelines/)).
Talc/graphite themselves are abrasive and are being replaced by synthetic
lubricants that cut dust-off by up to 90%
([Seed World](https://www.seedworld.com/us/2018/02/15/new-day-dust-reduction/),
[BW Fusion](https://bwfusion.com/proof/blog/the-good-the-bad-the-ugly-of-seed-talc-and-graphite)).
**This is the exact hazard profile of a friable herbicide pellet in ranch dust.**

**Complexity / power.** Requires a vacuum source. Production planters run
**18–21 inH₂O** water column for large seed (Kinze EdgeVac: 19–21 inH₂O for
35–70 lb corn units; Bayer: 18–20 inH₂O, higher for larger seed)
([Bayer large corn seed recommendations](https://www.cropscience.bayer.us/articles/bayer/large-corn-seed-planting-recommendations),
[Wolfe Ag rate charts](https://www.wolfeagsales.com/siteart/Rate%20Charts%20Operators%20Manual.pdf)).

**DERIVATION — can vacuum lift our pellet inside our power budget?**
20 inH₂O = 20 × 249.09 Pa = **4982 Pa**.
- *Theoretical minimum*: with a perfect seal and 2× margin, A = 2W/ΔP =
  0.0232/4982 = 4.65 mm² → **Ø2.4 mm hole**. Looks trivially easy.
- *But production practice is not near theory*: corn (0.35 g, W = 0.0034 N) uses
  ~Ø5 mm apertures → A = 19.6 mm² → hold force at 4982 Pa = **0.098 N ≈ 28× seed
  weight**. Real meters design to ~28× seed weight to survive leakage, seed
  irregularity, disc acceleration and pool drag.
- *Scaling that ratio to our pellet*: F = 28 × 0.0116 = 0.325 N → A = 65 mm² →
  **Ø9.1 mm aperture**, under a 12 mm sphere. Geometrically it just fits, but
  flow through Ø9 mm holes is ~3.3× the area per hole of a corn meter.
- **ASSUMPTION (high confidence):** a molded, mold-parting-line, possibly porous
  herbicide pellet seals far worse than a waxy seed coat, so effective ΔP at the
  pellet collapses and leakage flow rises further. Achieving 5 kPa at that flow
  from a **24 W** budget (2 A × 12 V, and that rail also has to run the motor and
  logic) is at best marginal. **ASSUMPTION: vacuum is not the right primitive for
  this payload** — it buys ag-grade 99% accuracy that we still have to verify with
  a sensor anyway, at a large and dust-vulnerable power/complexity cost.

**Adaptability to our pellet.** Principle scales (vacuum meters are explicitly
run across corn, soybeans, cotton, edible beans, sugarbeets, sunflowers by
swapping discs — [eSet](https://www.precisionplanting.com/products/planters/eset)),
but the hardware does not: a bespoke large-aperture disc plus a blower is a
whole subsystem. **Verdict: reject for v1; strongest *fallback* if a purely
mechanical escapement proves unable to handle pellet shape variance.**

---

## 2. Finger pickup meter (John Deere / Kinze)

**How it works.** A rotating finger wheel carries spring-loaded, cam-operated
fingers with "seed trapping spoons" against a stationary backing plate. Fingers
open by cam as they pass through the seed puddle, close to trap a single kernel
against the plate, and carry it up out of the puddle to a seed outlet, where it
transfers to a flat belt conveyor and then the seed tube. A **singulating brush**
immediately upstream of the outlet knocks off any extra trapped seed back into
the puddle. ([USPTO 6,273,010 singulating brush assembly](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6273010),
[Kinze finger pick-up](https://www.kinze.com/planter-performance/meters/finger-pick-up-meter/),
[Sloan JD finger meters](https://www.sloanex.com/planter-parts/corn-meter/john-deere.html))

**Count accuracy.** Worse than vacuum and **strongly seed-size dependent**:
**94–99%** depending on seed size, vs 98–99% for a properly set vacuum meter;
a cited head-to-head test stand gave 99.6% (vacuum) vs 97.6% (finger)
([Kinze](https://www.kinze.com/why-upgrade-to-vacuum-seed-meters/)). Critically,
"a finger meter has no adjustability" for seed size — you cannot tune it the way
you tune a vacuum singulator. Rated for mid-size corn at 4–6 mph only.

**Jam behaviour.** Mechanical pinch points between finger, spoon and backing
plate. A hard 12 mm pellet caught mid-close would either be crushed (creating the
fragments and dust we must not create) or stall the drive. Spring-and-cam parts
are wear items; these meters are a known rebuild item.

**Complexity.** High part count (12 sprung fingers, cams, backing plate, belt
conveyor) for a mechanism whose whole job is one seed at a time.

**Adaptability.** Poor. It is a *corn-and-sunflower* mechanism, sized to
kernel geometry, and it is the least size-tolerant meter in the industry.
**Verdict: reject.** The one idea worth stealing is the **wiper/singulating brush
that returns excess pellets to the pool** — that pattern (a compliant brush as the
"only one extra pellet gets rejected, gently" element) is reusable in any design.

---

## 3. Kinze Brush Meter / Brush Meter 2.0

**How it works.** A mechanical disc meter with pockets, where a brush retains and
singulates the seed. Introduced 1990; the marketing claim is **"only one moving
part"**, with a tool-free seed disc and brush swap in 2.0. Target crops:
soybeans, milo/grain sorghum, cotton, wheat — i.e. **small, round, hard, dry
seeds**, which is the closest morphology class to a molded pellet in the
production line-up. ([Kinze meter comparison](https://www.kinze.com/which-seed-meter-is-right-for-you/))

**Count accuracy.** Kinze does not publish a singulation number for the brush
meter (they publish >99% for True Rate vacuum). **ASSUMPTION: brush meter
singulation is below vacuum**, since Kinze positions vacuum as the upgrade path
for accuracy. Treat as unquantified.

**Jam behaviour.** Bristles are compliant, so an oversize/irregular pellet
deflects the brush rather than stalling the drive — **the single most attractive
property of this family for a friable pellet.** Brushes wear and pack with dust
(hence tool-free replacement in 2.0).

**Complexity.** Lowest of any production meter: one rotating disc, one brush,
no vacuum, no fan, no cams. Directly drivable by one small motor within our 24 W
rail.

**Adaptability.** **High.** Pocket size is just disc geometry — scale a pocket to
13 mm and the principle is unchanged. Brush pressure is the tuning knob that
finger meters lack. **Verdict: strong candidate — this is the mechanical
archetype to build from (rotating pocketed disc + compliant brush wiper).**

---

## 4. Brush belt delivery (John Deere ExactEmerge) — *delivery, not metering*

**How it works.** After singulation, seeds are handed from the meter into a
moving belt with bristles on its exterior. The brush "expands as it comes around
the pulley" to accept the seed, then closes around it, "controls all four sides
of the seed and tightens around it" so it cannot move during transport; at the
bottom the belt wraps a small-diameter idler which opens the pocket and releases
the seed at a point where the belt is transitioning from downward to slightly
upward, aiding clean separation. A **blocking member** guarantees the seed enters
the belt centred rather than at a random width position.
([Cross Implement — ExactEmerge/BrushBelt](https://crossimplement.com/news/article/2015/06/john-deere-exactemerge-planter-trench-delivery-system-and-brushbelttm-delivery-system),
[USPTO 9,345,188 blocking member](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9345188),
[USPTO RE48,572](https://patents.justia.com/patent/RE48572))

**Relevance.** This does **not** count — it transports what the meter already
singulated. But two ideas transfer directly to a drone dispenser:
1. **Bristle capture controls the object on all sides** — this is exactly what we
   want between "counted" and "released" so the pellet cannot rattle, double-feed,
   or be re-counted while the aircraft manoeuvres.
2. **A geometric release point** (small-radius wrap + direction change) gives a
   deterministic, repeatable release instant — relevant to the 1 m CEP-from-8 m
   drop requirement, where release-time jitter maps directly to landing scatter.

**Verdict: not a metering candidate; borrow the "controlled hold, then geometric
release" pattern for the drop stage.**

---

## 5. Pocketed carousel + servo/ratchet indexing (UAV bait & briquette dispensers)

**How it works.** The clearest documented UAV analogue. A carousel with **eight
chambers** holds briquettes above a base plate with a single **exit port**; on
command a servo drives a **ratchet-and-pawl** (servo rotary motion → linear arm
motion → advance ratchet one cog, pawl prevents back-rotation), advancing the
carousel exactly one chamber and dropping exactly one briquette through the port.
Lightening holes between chambers cut mass; the number/size/shape of chambers is
explicitly scalable to the product. Mounts to the UAS by an integrated **dovetail
quick-attach**.
([US 11,370,599 B2](https://patents.google.com/patent/US11370599B2/en),
[US 10,499,628](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10499628))

Arizona State University has a parallel, licensable design for **drone-deployable
automated vaccine-pellet dispensing "in a metered fashion"** that explicitly
"includes an anti-jamming system to enable robust operation" and supports 3D
printed components — but the public page gives no mechanism detail, pellet size,
or accuracy numbers (case ID M23-217L)
([SkySong Innovations](https://skysonginnovations.com/technology/drone-deployable-automated-pellet-dispensing-system/)).
**ASSUMPTION: worth a direct licensing/technical enquiry — it is the closest
publicly known prior art to our exact problem.**

**Count accuracy.** *Mechanically* exact: N servo strokes = N indexes = N pellets,
**provided every chamber was filled**. The patent explicitly notes there is **no
electronic verification** — quantity is "predictable through mechanical steps
rather than electronic verification". That is precisely the gap our requirement
("commanded count must be VERIFIED (sensed), not assumed") forbids. The real
error mode is **empty-chamber skips** from bridging over the fill point.

**Jam behaviour.** Not addressed in the patent. Pinch risk exists at the chamber
edge / base plate shear line — a pellet half-entering a chamber gets sheared by
the rotating carousel. Mitigations: chamber depth ≥ pellet dia so a pellet either
seats fully or is pushed aside; a chamfered/compliant (brush) lead-in at the fill
station (steal from §3); stall-current detection and **reverse-and-retry** on the
drive.

**Complexity.** Very low. One rotor, one indexing actuator, one exit port. Fully
within 24 W. Ratchet-and-pawl gives a positive, non-back-drivable index that
survives power cycling of 12V_PL (an explicit ICD requirement) — the mechanism
cannot lose its place when de-energised mid-command.

**Adaptability.** Excellent — chamber geometry is a parameter, exactly what our
parametric `PELLET_D` approach wants. **Verdict: strongest primary candidate.**

---

## 6. Single-file queue + nest + flapper escapement (aerial ignition PSD)

**How it works.** The most directly transferable *proven-in-the-field* discrete
sphere handler, from drone aerial-ignition Plastic Sphere Dispensers. Bulk
spheres sit in a hopper with a **rotating agitator in the hopper sump near the
exit hole**, driven by its own motor. Spheres drop into an **S-shaped feed tube**
where they "line up in series". The lead sphere lodges in a **"nest"** — a
semicircular cavity whose **interior radius matches the sphere's outside radius**
— and is retained by a **spring-steel flapper valve** across the nest exit. A
crankshaft-cam cycle then: (1) drives the injector needle down to pierce the
sphere, (2) injects reactant, (3) retracts, (4) the ball falls through the
discharge. A **cam-driven switch synchronises stopping** so the machine can only
halt in a "safe position": after one sphere has been discharged but before the
next is punctured. The hopper agitator motor runs at constant speed while the main
motor's RPM varies. ([US 10,871,358 B2](https://patents.google.com/patent/US10871358B2/en);
background: [USFS PSD description](https://www.fs.usda.gov/t-d/aerial_ign/plsphere/describe.htm),
[Vertical Mag on aerial ignition](https://verticalmag.com/features/controlled-firepower-how-aerial-ignition-equipment-aids-the-fight-against-wildfires/amp/))

Field-proven scale, from the productised version (Drone Amplified IGNIS III Mini):
**19 mm spheres, 2.4 g each, 225-sphere payload, 120 spheres/min drop rate,
1.87 kg loaded / 1.25 kg empty payload weight**
([IGNIS system datasheet](https://droneamplified.com/ignis-system-datasheet/),
[IGNIS III](https://droneamplified.com/ignis-iii/); larger IGNIS II variants
carry up to 450 spheres). Note how close this is to our envelope: **19 mm/2.4 g
× 225 vs our 12 mm/1.18 g × 250, at 1.87 kg loaded vs our ≤1.5 kg target.**
This is the single best existence proof that a drone-mounted, hopper-fed,
one-at-a-time discrete sphere dispenser at our scale is a solved problem.

**Count accuracy.** Structurally exact: **one sphere per crank revolution**, with
the cam switch enforcing a known rest state. The patent's own claim is that
processing spheres individually "avoids traditional jamming issues" because each
sphere is physically separated before the next enters the nest.

**Jam behaviour.** Two designed-in defences worth copying verbatim:
- **Sump agitator at the exit hole** (attacks bridging at its source, not from
  the top of the hopper).
- **Safe-stop cam switch** (the mechanism always halts in a defined,
  known-count state — invaluable when 12V_PL can be cycled mid-cycle).
The residual risk is the S-tube: a **fragment or half-pellet** wedging in the
single-file queue is a hard jam with no bypass. Mitigation: size the tube for the
13 mm worst-case pellet plus clearance, and add a reversible drive at the nest.

**Complexity.** Moderate — but note that most of the IGNIS complexity (needle,
pump, glycol) is the *ignition* function, which we delete entirely. Strip it and
what remains is: hopper + sump agitator + S-tube + nest + flapper + one cam.

**Adaptability.** High. The nest radius, tube ID and flapper stiffness are all
single parameters that scale to a 12 mm pellet.
**Verdict: strongest primary candidate alongside §5. The nest-and-flapper is
the highest-confidence "exactly one" primitive found in this research, and it has
flight hours behind it.**

---

## 7. Gravity single-file magazine + dual-gate escapement (DERIVED concept)

Not a product — a synthesis of §6's queue with a classic two-gate (airlock)
escapement: two independently actuated gates spaced one pellet apart in a
single-file tube. Upper gate open + lower closed = load one pellet into the
interstage; upper closed + lower open = release exactly one. Count = number of
gate cycles.

**Count accuracy.** Exact by construction, *and* the interstage volume physically
cannot hold two pellets if spaced < 2× pellet dia — a **geometric** guarantee, not
a probabilistic one. This is the property vacuum/finger meters cannot offer.

**Jam behaviour.** Gates are the pinch points; a shear across a friable pellet is
the failure. Mitigate with compliant (spring/brush) gate faces that deflect rather
than shear, plus stall detection and retry.

**DERIVATION — magazine sizing.** 250 pellets single-file at 13 mm pitch = 3.25 m
of tube. As a helix of mean diameter 140 mm: 440 mm/turn → 7.4 turns; at 18 mm
pitch → **~133 mm tall, ~158 mm outer envelope**. That is a plausible drone-belly
package (the bottom port plate is 50×50 mm; the payload hangs below Z ≈ −171 mm —
ground clearance must be derived from the landing-gear STEPs before committing).
Trade-off: a helical magazine occupies ~2 L of envelope to store 0.4 L of pellets
— **~5× the volumetric efficiency penalty vs a bulk hopper**, bought in exchange
for eliminating bridging entirely. **ASSUMPTION: probably not worth the volume for
250 pellets; but a *hybrid* — bulk hopper feeding a short 10–15 pellet single-file
buffer — gets most of the benefit at ~5% of the volume cost.** Recommend the
hybrid.

---

## 8. Vibratory single-file feed + optical gate (pharma tablet & lab seed counters)

**How it works.** Bulk product is fed onto vibrating channelled plates; controlled
vibration both **aligns** items into single file and **separates** items that are
stuck together, then each item falls past a photoelectric/IR "light curtain" or
laser and is counted as it breaks the beam. High-end machines exceed **99.8%
accuracy**, achieved through controlled feeding + separation + advanced (including
anti-dust and vision) sensors + automatic rejection of incorrect counts.
([Jinlu — how pill counting machines work](https://www.jinlupacking.com/blogs/pill-counting-machine-benefits/),
[Makwell](https://makwell.com/how-does-pill-counting-machine-work/),
[Kenwei pill counter guide](https://www.kenweigroup.com/blog/ultimate-guide-to-pill-counter-machine-2026-choosing-the-best.html))
The lab-seed equivalent (elmor C3) counts parts from **0.1 mm to 15 mm**,
including "extremely small and irregular" shapes, and logs every operation
([elmor C3](https://elmor.com/project/elmor-c3-seed-counter/)). Our 12 mm pellet
is inside the C3's stated range.

**Count accuracy.** Highest of any family surveyed (>99.8%), *because* counting is
done by a sensor on singulated flow rather than inferred from mechanism position.

**Jam behaviour.** Benign — a stuck item just stops flowing; the count simply
doesn't advance and the controller can keep vibrating.

**Complexity / suitability to a drone.** **Poor.** Vibratory bowl/plate feeders
depend on gravity direction and a stable reference frame; a hovering drone in West
Texas wind supplies neither, and the feeder's own vibration is a structural and
sensor-noise problem (the hopper patent in §11 explicitly flags vibratory agitation
as transmitting vibration into surrounding structure and causing premature bearing
failure). Counting rate is also throughput-oriented, not "stop exactly at N".
**Verdict: reject the feeder; adopt the *philosophy* — singulate mechanically,
then count with a sensor, and reject/retry on a bad count.**

---

## 9. Count verification / sensing (mandatory for our requirement)

Our requirement is "commanded count must be VERIFIED (sensed), not assumed", and
§5's carousel patent is explicit that mechanical indexing alone does **not** verify.
The ag industry's counting infrastructure:

- **Definition of the metric.** % singulation = 100% properly-timed single drops
  − % multiples − % skips; a *multiple* is the sensor seeing two where one is due,
  a *skip* is the sensor seeing nothing where one is due
  ([Precision Planting — should I calibrate my meters](https://www.precisionplanting.com/resources/articles/should-i-calibrate-my-seed-meters)).
  Adopt this exact vocabulary in our sim and test plan.
- **Optical seed-tube sensors fail in dust.** "Traditional sensors can be fooled
  by dust — if the dust is thick enough to break the beam of light, it gets counted
  as seed", giving inaccurate population counts.
- **The industry fix is non-optical:** Precision Planting **WaveVision** uses
  **high-frequency radio waves to measure mass rather than shape**, taking a
  3-D view of anything passing the tube; because a seed, a double, a triple, and
  dust each register a different mass, it distinguishes them and **"sees through
  dust"** ([WaveVision](https://www.precisionplanting.com/products/planters/wavevision),
  [Key Cooperative](https://www.keycoop.com/agronomy/centrol-precision-ag/precision-ag-products/precision-planting/precision-planting-products/wavevision-seed-sensor)).
  **This is the most important single finding for our dusty-ranch requirement:
  the exact sensing failure we face (dust false-counts) has a productised,
  mass-based solution in this industry, and a friable herbicide pellet in a dusty
  hopper is a *worse* dust environment than treated corn.**
- **ASSUMPTION (design guidance):** a plain IR through-beam at our drop chute is
  the cheap default, but must be validated against pellet dust and pellet
  *fragments* (a fragment breaking the beam reads as a pellet → overcount, which
  under-doses the target and, worse, silently drains the hopper). Candidate
  mitigations to trade: (a) dual-beam time-of-flight gating to reject
  slow/partial obstructions, (b) a short-range ToF/optical sensor looking at the
  nest to confirm *presence before release* as well as *passage after*, (c) a
  capacitive/impedance gate as a poor-man's WaveVision. Prefer **confirm-before-
  release + confirm-after-release** (two independent observations per pellet) over
  a single beam.
- **ASSUMPTION (rejected option):** hopper load-cell weighing at 1.18 g resolution
  against a ~300 g tare, on a vibrating airframe in wind, is ~0.4% full-scale
  resolution under heavy dynamic noise — not viable in flight. Possibly viable as
  a *pre-flight* self-check of remaining count.

---

## 10. Electric per-row drives — precedent for commanded discrete metering

Precision Planting **vDrive** puts an individual electric motor on each vSet meter,
"making that row a single-row planter because that row is controlled individually",
enabling **seeds-on-demand** (row-by-row shutoff at boundaries/overlap) and
**turn compensation** (each meter runs at the speed matching that row's ground
speed through a curve). It replaced chain drives and hex shafts.
([vDrive](https://www.precisionplanting.com/products/planters/vdrive),
[Alabama Extension on electric planter drives](https://www.aces.edu/blog/topics/farming/electric-drives-for-seed-metering-on-row-crop-planters/),
[Farm Progress](https://www.farmprogress.com/technology/vdrive-from-precision-planting-solves-many-problems),
[USPTO 8,850,997 individual meter control](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8850997))

**Relevance.** Validates the architecture we want: **a single small electric motor
directly driving one meter, commanded digitally, dispensing on demand at a
commanded rate/position.** A closed-loop stepper or a servo with a position
encoder driving the §5 carousel or §6 cam is exactly this pattern at 1/12th the
scale, and maps cleanly onto the ICD's "what signal triggers a dispense of N,
what feedback comes back" contract (no software phase required — the contract is
`dispense(N)` → `dispensed(n_verified, fault_flags)`).

---

## 11. Cross-cutting: hopper bridging with pellet-shaped articles

Independent of meter choice, the hopper is where a 250-pellet load fails.

- **Bridging mechanism**, stated precisely for pellet-shaped articles: a bulk
  quantity of pellets "randomly orient themselves such that the shape of the
  pellet-shaped articles, as well as the friction forces between adjacent
  pellet-shaped articles and with surfaces of the hopper, cause the pellet-shaped
  articles to bind" above the feed point. Worst for **oblong or complex geometry**
  and **rough or sticky surfaces** — our pellet has a mold parting line and a
  slight barrel shape, i.e. it is explicitly in the bad category.
  ([US 11,286,119 B2](https://patents.google.com/patent/US11286119B2/en))
- **Why vibratory agitation is not the answer**: hard to control without ejecting
  material from the hopper; transmits vibration through the equipment causing
  **premature bearing wear**; still inadequate for difficult geometries (same
  patent). This is a direct warning against the "just add a vibration motor"
  reflex on a drone, where that vibration also pollutes the IMU.
- **Air-assist alternative**: pressurised air jets into the hopper, **5–50 PSI**,
  continuous or pulsed, **angled 8–14° downward**, directed below the bulk material
  but above the feed mechanism, triggered by sensors that detect articles present
  in the hopper but not reaching the conveyor. Claimed to let machines run ~2× the
  speed of prior art with the same hopper (same patent). **ASSUMPTION: a compressed-
  air subsystem is out of budget for a 24 W drone payload, but a *small pulsed* jet
  from a micro-blower, or simply the §6 sump agitator, captures the useful part.**
- **Mechanical hopper rules** from the ag literature: steep wall slope (reported as
  **≥45°**) combined with a mechanical agitator for high-flakiness material; the
  classic agitator is "a simple shaft equipped with a curved plate"; a rotary
  agitator prevents choking at the hopper orifice.
  ([NPTEL Design of Farm Machinery, Raheman — seed metering lecture](http://elearn.psgcas.ac.in/nptel/courses/video/126105547/lec26.pdf),
  [Seed metering devices overview](https://www.slideshare.net/slideshow/seed-metering-devices/249874473),
  [Scientific Reports — cylindrical hopper + metering device performance](https://www.nature.com/articles/s41598-022-25798-8))
  *Note: the ≥45° figure comes from teaching material, not a peer-reviewed source
  — treat as a design heuristic to validate, not a verified constant.*
- **DERIVATION:** with 12 mm pellets, the standard anti-bridging orifice rule of
  thumb (outlet ≥ 6–8× particle diameter for free flow of near-spherical solids)
  implies a **72–96 mm outlet** — larger than our whole meter. **This is the
  quantitative reason a passive gravity hopper alone will not feed reliably and
  why an active sump agitator (§6) is non-optional.**

---

## 12. Non-candidates, recorded for completeness

- **Pneumatic pod firing (AirSeed "Podder").** Fires carbon seed pods into the
  ground at **150–300 m/s, 2 pods/second**, >40,000 pods/day/drone
  ([DroneLife](https://dronelife.com/2022/08/26/planting-trees-with-drones-airseed-delivers-seed-pods-for-drone-reforestation-initiative/),
  [UST](https://www.unmannedsystemstechnology.com/2022/08/using-drone-technology-to-plant-100-million-trees-by-2024/),
  [Euronews](https://www.euronews.com/2022/05/20/this-australian-start-up-wants-to-fight-deforestation-with-an-army-of-drones)).
  Interesting for the **accuracy** requirement (muzzle velocity swamps wind drift,
  which would trivially beat 1 m CEP from 8 m), but it is a rate-based firing
  mechanism, needs a compressed-gas or high-energy launcher well outside 24 W,
  and would shatter a friable herbicide pellet. **Reject for v1; note as the
  answer if wind-drift analysis later kills the passive-drop approach.**
- **Auger / spiral pay-off / spreader disc.** UAV broadcast seeders use a spiral
  pay-off mechanism or spinner plate for "steady and controlled release... spread
  evenly", with motor speed driven proportional to ground speed from the flight
  controller ([Saiwa overview](https://saiwa.ai/sairone/blog/drone-cover-crop-seeding/),
  [Payload manipulation for seed-sowing UAV](https://www.researchgate.net/publication/343755970_Payload_Manipulation_for_Seed_Sowing_Unmanned_Aerial_Vehicle_through_interface_with_Pixhawk_Flight_Controller)).
  These are **mass-flow-rate** devices with no notion of an exact count.
  **Reject:** fundamentally incompatible with "exactly N, verified".
- **Belt/cell-belt and vibrating cell-belt precision meters** (research-grade, e.g.
  long-belt finger-clip corn meters and vibrating cell-belt rice meters —
  [PMC8831804](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8831804/),
  [ScienceDirect cell-belt rice meter](https://www.sciencedirect.com/science/article/abs/pii/S1537511025000728)).
  Same singulation principle as §3/§5 in a belt form factor; adds belt tension and
  tracking failure modes for no benefit at our scale. **Reject.**

---

## 13. Comparison table

| # | Mechanism | Count accuracy | Jam behaviour | Complexity | Fits 24 W | Adapt to 12 mm/1.18 g pellet | Verdict |
|---|-----------|---------------|---------------|------------|-----------|------------------------------|---------|
| 1 | Vacuum disc + singulator | 98–99%, >99% best case (cited) | Soft-fails as skips; apertures plug with dust | High (blower + plenum + seals) | Marginal→No (derived Ø9 mm apertures) | Principle yes, hardware no | Fallback only |
| 2 | Finger pickup | 94–99%, size-sensitive, non-adjustable | Pinch/crush; wear item | High | Yes | Poor | Reject |
| 3 | Kinze brush meter | Unpublished (< vacuum) | **Compliant — deflects, doesn't shear** | **Lowest ("one moving part")** | Yes | **High** | **Core archetype** |
| 4 | Brush belt (ExactEmerge) | n/a (delivery) | n/a | Medium | Yes | Borrow hold+release pattern | Drop-stage idea |
| 5 | Pocketed carousel + ratchet servo | Exact *if* chambers fill; **no verification** | Undocumented; shear risk at base plate | **Very low** | Yes | **Excellent (chamber = parameter)** | **Primary candidate** |
| 6 | Nest + flapper escapement (PSD) | **Exact, one per crank rev, safe-stop cam** | Best-defended (sump agitator, individual processing) | Medium (minus ignition hardware: low) | Yes | High; **flight-proven at 19 mm/2.4 g × 225** | **Primary candidate** |
| 7 | Single-file magazine + dual gate | **Geometrically exact** | Gate shear risk | Low | Yes | High, but ~5× volume penalty | Hybrid buffer only |
| 8 | Vibratory + optical gate | **>99.8%** | Benign | High; needs stable g-frame | No | Range covers 12 mm | Reject device, adopt philosophy |
| 9 | Sensing (WaveVision-class) | Turns any of the above into "verified" | n/a | Low–medium | Yes | Mass-based sensing **sees through dust** | **Mandatory** |

---

## 14. Recommendation

**Architecture: mechanically-guaranteed singulation + independent sensed
verification + reversible drive.** Concretely, the highest-confidence v1 is a
**§5/§6 hybrid**: a bulk hopper with a **§6-style rotating sump agitator at the
exit** feeding a **short single-file buffer (§7 hybrid, ~10 pellets)** into a
**pocketed indexing rotor (§5)** whose fill station uses a **compliant brush
wiper (§3)** to reject the second pellet, releasing through a **geometric release
point (§4)** past a **dust-tolerant, non-purely-optical count sensor (§9)** —
driven by **one small electric motor with position feedback and stall/reverse
retry (§10)**, halting only in a **cam/index-defined safe state (§6)** so that
12V_PL power cycling cannot corrupt the count.

Every element above is drawn from a cited, fielded design. The three things this
research says will actually kill the payload if ignored, in order:
1. **Hopper bridging of 12 mm irregular pellets** (§11 — the 6–8×D orifice
   derivation says passive gravity will not work; agitation at the sump is
   non-optional, and vibratory agitation is documented as the wrong answer).
2. **Dust/fragment false counts on an optical sensor** (§9 — the industry's own
   answer was to abandon optical for mass-based sensing).
3. **Shear of a friable pellet at any mechanical pinch point**, which converts one
   fault into a permanent dust/fragment source (§2, §5, §7 — hence compliant
   brush/spring faces everywhere a pellet can be caught, plus reverse-and-retry).

**Open items for the next phase:** (a) contact SkySong Innovations re case
M23-217L (§5) — closest known prior art; (b) obtain real pellet friability,
sphericity spread and dust-shed data (CONTEXT flags these as unknown) — every
clearance and brush-pressure number depends on them; (c) derive landing-gear
ground clearance from the Quiver STEPs before fixing the hopper aspect ratio;
(d) bench-test the count sensor against deliberately dusty/fragmented pellets
before committing to any meter geometry.

---

# ADDENDUM (research pass 2026-08-06, added after Thomas's 23:03 fragment-wedge
# directive) — prior art aimed specifically at the pocket-wheel wedge jam

Sections 1–14 above stand. This addendum adds material that is specific to the
HARD REQUIREMENT in CONTEXT.md: *"a possible jam if a fragment gets in to the
pocket wheel slot, you'd have 1.5 capsules and it could prevent the wheel
from turning."* Each item below maps to one of the four sub-requirements
(reject-before-wedge / shear backstop / detect+recover / pocket geometry).

## A1. Compliant torque decoupling — paintball loader drives (→ shear backstop, detect+recover)

The paintball industry solved "rigid rotor vs fragile sphere" explicitly.
US 7,694,669 B2 mounts the rigid feed projections on the drive shaft **through an
elastic member**, sized so it stays rigid in normal feeding and yields only on a
genuine jam. Verbatim from the patent:

> "When a paintball stack is moving or when an individual paintball is capable of
> movement … the elastic member should not bend or flex, so that the rotational
> force F applied by the motor is translated by the projections to the paintballs
> being moved."

> "Upon encountering a stationary or jammed paintball represented by the opposing
> force F′, the elastic member should deform sufficiently to allow a projection to
> pass the jammed or stationary paintball, without breaking or rupturing of the
> paintball."

The spring is specified to "flex only when F′ > F", with preferred elastic
modulus **0.01–10 GPa**
([US7694669B2](https://patents.google.com/patent/US7694669B2/en)). A companion
patent decouples the feeder from the drive shaft entirely with a torsion spring
that "maintains constant tension on the feeder when the drive shaft rotates"
([US8459245B1](https://patents.google.com/patent/US8459245B1/en); see also
US 8,047,191 / US 7,343,909 "mechanical drive assist for active feed paintball
loader", https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8047191).
Production loaders pair this with **electronic jam detection that automatically
reverses and resets**, and use a constant-pressure carousel with opposing
rotation arms for jam-free feed at 40+ balls/s
([DYE Rotor R2](https://www.estrategopaintball.com/en/loaders/580-dye-rotor-r2-loader-se.html)).

**Design read-across (label: DERIVED recommendation, not a verified number).**
Our fragment-wedge requirement asks for two *opposite* behaviours — yield gently
on a fragile whole pellet, but deliver enough torque to shear a wedged fragment.
The paintball art shows the resolution: an elastic element with a **defined
break-over threshold** F′ > F. Set the compliance threshold *above* the
fragment-shear force and *below* the housing-damage force, so the sequence on a
wedge is: (1) brush relief rejects it (§3/A2), (2) if carried in, drive torque
rises to the threshold and shears the fragment, (3) if it still doesn't clear,
the elastic element absorbs the overload while stall detection fires the
reverse-oscillate routine. This is a three-stage defence, all of it fielded prior
art, and it directly answers directive items 1–3.

## A2. Brush/sprung plate as the overfill relief — Kinze brush meter + gumball wheels (→ reject-before-wedge)

The Kinze brush meter is the ag-side proof that a *compliant retainer* is the
right element at the pocket exit: a disc with peripheral seed pockets rotates
through the pool and "a retainer brush retains the measured quantity of seeds in
the seed pockets until the belt reaches the release point, thereby providing an
accurately measured and accurately released stream of seed", explicitly claimed
to improve release accuracy and reduce seed bounce
([US6581535](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6581535),
[Kinze Brush Meter 2.0](https://www.kinze.com/planter-performance/meters/brush-meter-2-0/),
[Kinze innovation history](https://www.kinze.com/great-kinze-innovations-the-brush-type-seed-meter/)).
Air-seeder meters use the same trick — see "Brush for air seeder metering system"
([US5826523](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5826523)).
The consumer analogue is the gumball wheel's **brush plate**, a sprung element
that "aligns the springs to cover the triangular opening" over the dispensing
aperture, with a notched wing giving discrete portion-control settings
([Gumball Machine Warehouse](https://www.gumball-machine.com/blogs/articles/how-to-adjust-the-candy-dispensing-wheel-of-your-candy-vending-machine)).
Gumball wheel geometry also documents the **aperture-margin rule**: apertures
"slightly larger than one inch" for 1-inch balls, indexed 120° per vend, and
replacement wheels with 39 mm holes rated for 25–33 mm product — i.e. roughly
**1.05–1.2 × object diameter** hole sizing for reliable one-at-a-time vending
([US6536623 / US20030071049A1](https://patents.google.com/patent/US20030071049A1/en),
[replacement dispensing wheel](https://www.amazon.com/Gumball-Machine-Dispensing-Wheel-Replacement/dp/B0DP15T6LS)).

**DERIVED for our pocket:** at 1.05–1.2 × the 13 mm worst-case pellet, the pocket
mouth lands at **13.7–15.6 mm**. Note the tension with the wedge requirement: a
larger mouth reduces fill jams but increases the chance a fragment shares the
pocket with a whole pellet. The brush relief is what buys back that margin — it
is the element that decides *what leaves the fill zone*, and it must be the last
thing the pocket passes before entering the close-clearance housing arc.

## A3. Sensor-side handling of broken product — pharma counters (→ detect + truthful count)

Disc-cavity tablet counters index one tablet per cavity and verify optically at
the exit; **electronic sensors verify each cavity is filled before dispensing**,
and if a cavity is empty (a "miss") or a tablet is broken the system rejects that
bottle rather than shipping a wrong count
([Busch Machinery](https://www.busch-machinery.com/tablet-and-pill-counting-machines/),
[Pharmaceutical Technology — Ensuring Correct Tablet Count](https://www.pharmtech.com/view/ensuring-correct-tablet-count),
[Allpack counting line](https://www.allpackchina.com/capsule-tablet-counting-line/)).
Fetched figures: the BMT-C3 class claims **99.99% accuracy** using a proprietary
photoelectric sensor that recognises opaque, translucent and transparent product
including odd/elongated shapes; other units advertise "upstream problem detection
stops process" and "no-bottle-no-count" interlocks (Busch, fetched 2026-08-06).

**Read-across:** the industry that actually has to hit exact counts (a) counts
per-object at the exit rather than trusting the index, (b) **verifies fill before
release**, and (c) treats a broken unit as a *reject-the-batch* event, not
something to count. Our analogue: on a suspected fragment, do not silently keep
dispensing — increment a fault flag in the `dispensed(n_verified, fault_flags)`
return so the aircraft knows the target was under-dosed. §9's dust caveat still
governs the sensor choice; a pharma-style photoelectric gate is a clean-room
sensor and must not be adopted uncritically into a West Texas dust environment.

## A4. Pellet crush strength — the number the shear backstop needs (ASSUMPTION, flagged)

No manufacturer publishes a crush strength for tebuthiuron pellets. What the
sources do give:
- Spike 20P is described as **"heavy, high-density clay pellets that stay stable
  on the soil surface and resist breakdown"**, 20% tebuthiuron, applied by
  handheld/broadcast/push spreader or aerially at 3.75–10 lb/acre
  ([Azelis](https://azelisaes-us.com/grow_your_know/tebuthiuron-invasive-brush/),
  [ArborChem Spike 20P](https://www.arborchem.com/product/68/spike-20p-25-lb-bag)).
  "Resist breakdown" refers to *weathering*, not mechanical strength — do not
  over-read it.
- The nearest measurable analogue is pharmaceutical **breaking force** (misleadingly
  called "hardness"), measured by diametral compression between rigid platens
  (Stokes/Monsanto, Schleuniger, Erweka, Varian VK200 testers)
  ([USP <1217> Tablet Breaking Force](http://www.uspbpep.com/usp32/pub/data/v32270/usp32nf27s0_c1217.html)).
  A large compressed tablet is typically specified **≥ ~30 N**
  ([US9756869](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9756869));
  see also break-force ↔ tensile-strength relationships for curved-face tablets
  ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0378517312008708)).

**ASSUMPTION (must be bench-verified before the design is trusted):** treat the
whole-pellet diametral crush force as **30–100 N**, and design the shear backstop
to **≥ 150 N at the pocket radius** (1.5× the upper bound). Reasoning: Thomas
reports the pellets "sometimes break/crumble", which places them at the weak end
of the molded-compact range; a *fragment* — already fractured, with a smaller
load-bearing cross-section and existing crack front — will shear well below the
whole-pellet figure, so a backstop sized against a whole pellet is conservative
for the fragment case. A cheap bench test (kitchen scale + flat platen, press a
pellet to failure, n≈20) converts this whole assumption into a measured
distribution and should be run before CDR.

## A5. Additional pocket/cell prior art at our exact size class

- **Sutton Ag AA-12 metering wheels**: large-seed cells at **12 mm (0.47")**, 12
  cells per wheel, for beans/chard/peas/spinach — i.e. rigid cell wheels are
  routinely built at *exactly our pellet diameter*
  (https://suttonag.com/products/aa-12-seed-metering-wheel — note: page returned
  404 on direct fetch 2026-08-06; figures are from the search index snippet,
  treat as UNVERIFIED pending a working source).
- **Monosem MS**: plants "raw, encrusted, and pelleted seeds accurately"
  ([Monosem MS](https://monosemusa.com/ms-mini-seed-planters/)) — pelleted product
  is a supported class for cell/vacuum meters, not an exotic case.
- **Belted pocket meters**: US 6,237,514 / US 5,992,338 describe conveyors whose
  material is flexible enough to wrap the sprockets yet firm enough not to "pinch
  around seeds in the containment pockets"
  ([US6237514](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6237514))
  — an explicit statement of the compliance/pinch trade our pocket wheel faces.
- **UAV precedent for drop-one-on-command**: Mast Reforestation (ex-DroneSeed)
  pucks are "loaded in a special puck-dispenser which, closely coordinating with
  the drone, spits one out at the exact moment and speed needed"
  ([TechCrunch](https://techcrunch.com/2018/11/26/that-night-a-forest-flew-droneseed-is-planting-trees-from-the-air/));
  academic UAV dispensers use a cylindrical hopper + motor-driven disc with servo
  release ([ScienceDirect, IFAC 2025](https://www.sciencedirect.com/science/article/pii/S2405896325024668),
  [Eur. J. Forest Eng.](https://dergipark.org.tr/en/pub/ejfe/article/1802823)).
  These confirm the form factor flies; none publish count accuracy.

## A6. What the addendum changes in the §14 recommendation

Nothing is retracted. Three additions:
1. **Add an elastic/torque-limited coupling between motor and pocket rotor** with
   a defined break-over threshold (A1) — this is the piece §14 was missing to
   satisfy directive item 2 without also crushing good pellets.
2. **Specify the pocket mouth at ~1.05–1.2 × worst-case pellet diameter**
   (13.7–15.6 mm for a 13 mm pellet) and make the compliant brush the *last*
   element before the close-clearance arc (A2) — directive items 1 and 4.
3. **Verify fill before release as well as passage after release** (A3), and
   surface a fault flag rather than silently under-dosing — directive item 3,
   and it keeps the count truthful through a reverse-oscillate recovery if the
   sensor logic is made direction-aware.
