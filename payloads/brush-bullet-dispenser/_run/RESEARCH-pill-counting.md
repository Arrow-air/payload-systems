# RESEARCH — Pharmaceutical Pill Counting & Dispensing, Applied to Pellet Metering

Research agent output, 2026-08-06. Domain: pharmaceutical pill counting/dispensing
(rotary disc counters, channel singulators, optical count verification, friable
tablet handling), evaluated against the Brush Bullet dispenser problem.

**Target problem (from `_run/CONTEXT.md`, verified):** meter EXACTLY N pellets,
N ∈ 1..10 (usually 1–3), of ~12 mm / 1.18 g molded herbicide pellets, from a
≥250-pellet hopper, on a drone, in West Texas ranch dust/heat/wind. Count must be
SENSED, not assumed. Total payload ≤ 1.5 kg including pellets.

Every claim below is either (a) sourced with a URL, (b) a DERIVATION from
CONTEXT numbers with the arithmetic shown, or (c) explicitly labelled ASSUMPTION.

---

## 0. Derived problem parameters (arithmetic shown — not invented)

| Quantity | Derivation | Value |
|---|---|---|
| Pellet volume (as ideal sphere) | (4/3)·π·(6 mm)³ | 0.905 cm³ |
| Pellet bulk density | 1.18 g ÷ 0.905 cm³ | **1.30 g/cm³** |
| Solid volume, 250 pellets | 250 × 0.905 cm³ | 226 cm³ |
| Hopper volume @ 0.60 loose random packing | 226 ÷ 0.60 | **377 cm³ (0.38 L)** |
| Hopper volume @ 0.55 (irregular, poured) | 226 ÷ 0.55 | 411 cm³ (0.41 L) |
| Peak metering rate required | 10 pellets in a ~2 s hover-drop | **≤ 5 pellets/s** |
| Pellet transit time through a beam after 50 mm free fall | v = √(2·9.81·0.05) = 0.99 m/s; 12 mm ÷ 0.99 m/s | **~12 ms** |

CONTEXT's 0.5 L hopper estimate is conservative versus the 0.38–0.41 L derived
here; keep 0.5 L as the design allowance (headspace + agitation volume).

**The single most important framing fact:** pharma counters run at 1,000–3,000
tablets/minute (17–50 Hz)
([Deitz TC3](https://www.deitzco.com/deitz_machines/tablet-counter-tc3/),
[CVC](https://www.cvcusa.com/products/other/96-cvc-1000s-ts.html)). We need
**≤ 5 pellets/s, i.e. ~10 % of the slowest pharma machine, in bursts of ≤ 10.**
Nearly all the complexity in pharmaceutical counters exists to preserve accuracy
*at speed*. At our rate we can afford **positive mechanical metering with
per-pellet sensed verification and retry** — a design point pharma cannot use.
This is the central conclusion of this research.

---

## 1. Mechanism family A — Slat counter (mechanical cavity counting)

**How it works.** Horizontal slats, each drilled with cavities sized to accept
exactly one tablet, ride on a track beneath the bulk hopper. Product tumbles
across the slats, cavities fill by gravity, brushes/wipers sweep off excess, the
slat inverts over the drop tunnel and releases its contents. The count is set by
the *number of cavities per slat*, not by any sensor — "counting accuracy is
guaranteed by filled cavity count, independent of sensors."
([IMA HYBRID-39](https://imagroup.com/machines/slat-counter/),
[C.E. King Technocount M500](https://www.ceking.com/products/tablet-capsule-slat-counter),
[SIGMA slat counter guide](https://www.sigmaequipment.com/guide/slat-counter/))

**Count accuracy.** Deterministic *if and only if* every cavity holds exactly one
piece. "Custom slat designs fit each tablet or capsule, eliminating double-fills
and miscounts"; the failure mode is the empty cavity, not the miscount.
Modern lines therefore bolt a scanner on anyway: IMA's **TruCount®** array of
photodiodes scans "nearly 2000 times per second" *after* product leaves the slat,
verifying count before the bottle is filled
([IMA counting technologies](https://imagroup.com/pharma/brands/ima-safe/counting-technologies/)).
That is an explicit industry admission that pure mechanical cavity counting is
not trusted alone.

**Jam behaviour.** Cavity sized for one piece + brush cutoff = the classic
half-seated-part jam (see gumball wheel, §2). Optional line features listed for
slat counters include static eliminators, air filters and dust collectors —
i.e. dust is a known consequence of brushing product across cavities
([SIGMA](https://www.sigmaequipment.com/guide/slat-counter/)).

**Complexity.** High: linear slat chain, drive, brushes, and a *format part per
product* (change tablet, change slats). 200–300 bottles/min throughput we do not
need.

**Adaptability to our pellet.** Concept adapts extremely well; the machine does
not. Our pellet is a **sphere**, which is the ideal cavity-filling geometry
(orientation-independent — no "which way up" failure that plagues caplets). The
right transplant is *the principle*: a single moving element carrying N
pellet-sized pockets past a hopper port, with a wiper. Discard the linear chain
in favour of a disc (§2). **Verdict: adopt the principle, reject the machine.**

---

## 2. Mechanism family B — Rotary/indexing pocket disc ("counting disc", gumball wheel, pharmacy cell)

**How it works.** A disc with through-holes (pockets) rotates under the bulk
supply. Each pocket accepts one piece; a fixed plate below the disc keeps the
piece captive until the pocket indexes over the outlet, where it falls free.
Pharma description: "Product is fed on a rotating disc and is channeled into
guided openings as per the shape and size of the product. As per the count set in
the counting disc, the number of counts is maintained and released by the disc"
([Adinath disc-based counter](https://www.adinathpharmamachinery.com/tablet-press-machines/disc-based-tablet-counting-machine/)) —
typical discs carry ~100 holes and are product-specific. A verification variant is
described as: "The counting disc (with precisely sized holes) rotates under the
stream of tablets, and an optical sensor or laser checks that each cavity is
filled before dropping"
([N.K. Industries](https://www.nkpharmamachinery.com/products/automatic-tablet-counting-and-filling-machine.html)).

The consumer-grade ancestor is the **gumball wheel**: a wheel turned through 120°
per dispense with one bore per sector; "a plate positioned immediately below the
wheel to ensure merchandise doesn't leave a bore until properly aligned with the
chute", and "resilient members such as springs extend over the wheel in the region
immediately above the loading chute to prevent more than one capsule from passing
through a bore"
([US6536623 / US20030071049](https://patents.google.com/patent/US20030071049A1/en),
[gumball wheel adjustment](https://www.gumballs.com/how-to-adjust-gumball-machine-dispensing-wheel.html)).
Heavy-duty commercial wheels add **agitator systems and spring assemblies**
([Amazon commercial dispensing wheel](https://www.amazon.com/Gumball-Machine-Dispensing-Wheel-Replacement/dp/B0DP15T6LS)).

Pharmacy robots use the same idea as a per-drug cassette/"dispensing cell":
ScriptPro's universal cells are field-calibrated per drug and can "dispense a
specified quantity of pills from a cassette", using **no air pressure**
([ScriptPro CRS 150](https://scriptpro.com/product-information/crs-150-compact-robotic-system/),
[ScriptPro overview / Deltason](https://www.deltason.com/products/pharmacy/ScriptPro_overview.html)).

**Count accuracy.** ScriptPro publishes **99.70 % counting accuracy, based on the
number of pills counted**
([Deltason](https://www.deltason.com/products/pharmacy/ScriptPro_overview.html)) —
i.e. ~3 errors per 1,000 pieces for a calibrated pocketed dispenser *with* its
sensing. Pocket-disc patents design explicitly against the multi-release failure:
"The dimensional relationship and angular spacing between pockets in each set
prevent simultaneous dispensing of pills from multiple pockets"
([US4838453 pill dispenser](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4838453)).
A gated variant uses "a sliding gate [that] fits into a slot and blocks it in its
starting position, but is movable progressively radially outwardly, thereby
opening the slot progressively to the bottoms of pockets as the disc turns"
(same patent).

**Jam behaviour.** Documented and specific: "A somewhat common problem…is that
they have a tendency to jam during operation, often caused by a gumball not being
properly seated in the dispensing mechanism or by an extra gumball becoming
partially seated in a dispensing wheel aperture"
([gumballs.com](https://www.gumballs.com/how-to-adjust-gumball-machine-dispensing-wheel.html)).
**This is the dominant risk for our pellet**: a 12 ± 1 mm irregular molded sphere
half-entering a pocket and being sheared by the wiper. Mitigations from the
literature: compliant wiper (brush/spring, not a hard edge), generous pocket
diameter, and reverse-index recovery (§6).

**Complexity.** Low: one disc, one indexing actuator (stepper or servo), a
stationary bottom plate, a wiper. No format-change parts if we only ever handle
one pellet type. Naturally interlocks with per-pellet verification because a
single-pocket disc *emits at most one pellet per index*.

**Adaptability to our pellet.** Highest of any family. Sphere = orientation-free
pocket fill; 1.30 g/cm³ = heavy enough to seat by gravity; 1–10 count = 1–10
index steps. ASSUMPTION (design guidance, not sourced): pocket bore ≈ 14 mm and
disc thickness ≈ 13 mm so exactly one pellet occupies a pocket's depth and a
13 mm worst-case pellet still clears — must be validated on real pellets.
**Verdict: primary candidate.**

---

## 3. Mechanism family C — Vibratory channel singulation + optical counting (the mainstream pharma electronic counter)

**How it works.** Bulk from a hopper is metered onto vibratory plates/trays that
spread product into lanes: "Product starts in a hopper and moves onto vibration
panels or tracks that spread tablets into lanes. This singulation step is where
stability is won: the goal is even spacing, not aggressive shaking"
([Richpacking](https://www.richpacking020.com/tablet-counting-machine-101-how-tablet-capsule-counting-works-accuracy-factors-and-smart-selection_n347)).
Cremer uses "three vibratory plates for optimal product separation and infrared
product detection", with **separation flaps acting as buffers so the count is
verified before discharge**
([Cremer CF series / NJM](https://www.njmpackaging.com/products/cremer-cf-1220-cf-1220d-tablet-counters/),
[Cremer](https://www.cremer.com/c/tablet-counting-machine/)).
Deitz's TC3 is the cleanest small-machine description: "a variable speed vibratory
feeder chute, which regulates the flow of pills onto the rotating glass disc",
adjustable guides arrange product single-file "to ensure each tablet falls right
into the center of the counting window"
([Deitz TC3](https://www.deitzco.com/deitz_machines/tablet-counter-tc3/)).

**Count accuracy (hard numbers).**
- Deitz TC3: **99.99 % — "1 error per 10,000 pills" at optimal conditions**
  ([Deitz](https://www.deitzco.com/deitz_machines/tablet-counter-tc3/)).
  Note the qualifier "at optimal conditions" — that is a clean-room, clean-lens,
  correctly-tuned figure, not a dusty-ranch figure.
- Cremer and Countec both market **"100 % counting accuracy"**
  ([NJM/Cremer](https://www.njmpackaging.com/products/tablet-counters/),
  [Key International / Countec](https://www.keyinternational.com/packaging-equipment/tablet-counters)).
  Treat as marketing; the 99.99 % figure is the credible one.
- Throughput context: TC3 does 2,500–3,000 tablets/min (coated), 1,000–1,500
  capsules/min; size limit 0.9" (22.9 mm) width — our 12 mm pellet is inside the
  handled envelope of a commercial counter.

**Jam / fault behaviour.** Failure drivers named explicitly: dust coats sensing
windows and causes signal drift; static "causes capsules to cling to guides and
then release in bursts, creating double counts"; "fragments can be interpreted as
full pieces when overlap is present"
([Richpacking](https://www.richpacking020.com/tablet-counting-machine-101-how-tablet-capsule-counting-works-accuracy-factors-and-smart-selection_n347)).
Machines mitigate with dust extraction, perforated trays that drop fines into a
trap before the sensor, and vacuum ports
([JinLu](https://www.jinlupacking.com/blogs/pill-counting-machine-benefits/) —
page 403s to direct fetch; content summarised via search index, treat as
lower-confidence).

**Complexity.** Medium-high for us: needs a vibratory actuator (electromagnet or
piezo), tuned amplitude, a lane geometry that only works in one orientation and
at ~1 g of gravity alignment — a hovering multirotor is a **vibration source**,
which is exactly the disturbance vibratory singulation is trying to control.

**Adaptability to our pellet.** Poor as a whole system, valuable in one part.
Spheres on a vibratory tray **roll and scatter**, and once rolling they arrive at
the sensor at uncontrolled spacing. Airframe vibration is uncontrolled and
uncorrelated with the feeder drive. **Verdict: reject the vibratory front end;
adopt the counting-window/verification back end (§4).**

---

## 4. Count verification sensing — the part of pharma we should copy wholesale

This is the sub-domain where pharmaceutical practice is directly, cheaply
transplantable, and it is what satisfies CONTEXT's hard requirement that the
commanded count be *sensed*.

### 4.1 Through-beam (opposed-mode) photoelectric — recommended baseline
Banner's applications guidance is the most directly usable source:
- Opposed-mode/through-beam is "the most reliable sensing approach because these
  sensors are not affected by tablet color or reflectivity."
- **"Photoelectric sensors typically cannot accurately tell if more than one
  tablet goes through the sensing zone at a given time"** → machine singulation
  before the beam is mandatory.
- Resolution: "with the proper sensing mode and a high-resolution fiber optic
  array, Banner's photoelectric sensors can reliably and repeatedly detect 2 mm
  diameter tablets or smaller."
- Speed: DF-G2 fiber amplifier **10 µs** response; D10 plastic-fiber series also
  cited.
- Dust: "Schedule routine cleaning… Newer sensors include active optical
  monitoring to compensate gain levels or trigger maintenance alerts."
([Banner Engineering](https://www.bannerengineering.com/us/en/company/expert-insights/how-to-use-photoelectric-sensors-for-tablet-counting.html))

General through-beam suitability for our environment: "Through-beam sensing
provides the longest sensing ranges and highest excess gain, which enables
through-beam sensors to be reliably used in foggy, dusty and dirty environments…
The beam must be fully interrupted; this minimizes false triggers"
([Pepperl+Fuchs](https://www.pepperl-fuchs.com/en-us/products/industrial-sensors/photoelectric-sensors/thru-beam-sensors-gp31261),
[GTRIC guide](https://gtric.com/through-beam-photoelectric-sensor-guide/),
[OPTEX FA counting applications](https://www.optex-fa.com/tech_guide/photo_sensor/solution/purpose/counting/)).

Margin check (DERIVATION, §0): our pellet occludes the beam for ~12 ms after a
50 mm fall; a 10 µs sensor gives ~1000× timing margin, so a **software dead-time
window of e.g. 30–50 ms after each edge** cleanly rejects re-trigger from a
bouncing sphere without risking a missed second pellet at ≤ 5 pellets/s.

### 4.2 Dynamic threshold / self-compensating optics — copy this
Deitz: the sensor "dynamically regenerates the threshold level every 100 ms" and
alerts the operator when cleaning is needed
([Deitz TC3](https://www.deitzco.com/deitz_machines/tablet-counter-tc3/)).
IMA optical: **16 scans per millisecond**, counting product falling within
programmed *dark-time* limits, able to distinguish a single tablet from an
overlapping pair
([IMA](https://imagroup.com/pharma/brands/ima-safe/counting-technologies/)).
Countec: "dark-time adjustability helping detect broken or double tablets",
sensors "detect each dose on multiple planes"
([Key International](https://www.keyinternational.com/packaging-equipment/tablet-counters),
[A&J Machine](https://ajmachine2000.com/2021/01/countec-electronic-tablet-capsule-counter/)).
**Dark-time gating is free in firmware and is the single highest-value idea in
this document**: for a known 12 mm sphere at a known fall velocity, the expected
occlusion duration is known, so a too-long dark time = two pellets or a jam, and
a too-short dark time = a fragment. That converts a dumb beam into a
fragment-rejecting, double-rejecting counter.

### 4.3 Electrostatic Field Sensor (EFS) — the dust-immune option
"The technology used for the sensor is not dependent on the type of tablet being
counted, can identify an incorrect or broken tablet, and is **immune to dust**
created by movement of the tablets… There is a sufficiently wide channel so that
dust does not affect counting" — referencing US 6,504,387 and
**Sparc Systems Ltd (Malvern, UK)**
([US8141330](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8141330)).
IMA sells it as a product line: "Designed for dusty environments… discriminates
between acceptable products and damaged items by analyzing mass against reference
curves. It outperforms optical sensors at detecting half tablets, capped tablets,
empty capsules"
([IMA](https://imagroup.com/pharma/brands/ima-safe/counting-technologies/)).
Capability: single head, >1,000 pills/min; "measuring this disturbance allows the
detection of overlapping product as well as the differing mass of broken pieces"
([Sensors Portal digest — capacitive pill counting](https://www.sensorsportal.com/HTML/DIGEST/P_226.htm),
page now 404s; abstract also at
[ResearchGate](https://www.researchgate.net/publication/242321559_Pharmaceutical_Pill_Counting_and_Inspection_Using_a_Capacitive_Sensor)).
**Relevance:** this is the pharma answer to *exactly our environment* (dusty,
friable, fragment-generating). A simple capacitive/EFS ring around a 20 mm drop
tube is buildable and is immune to the lens-fouling that will otherwise define
our maintenance interval. ASSUMPTION: a DIY capacitive ring is achievable but
unproven at this pellet's dielectric properties — prototype risk, worth a bench
test against the optical baseline.

### 4.4 Vision
"Advanced vision algorithms capable of distinguishing between a single pill and
pill dust or fragments"; IMA offers camera vision as an add-on to catch
cross-contamination by colour
([IMA](https://imagroup.com/pharma/brands/ima-safe/counting-technologies/)).
**Verdict for us: reject.** Mass, power, compute, and CONTEXT explicitly cuts the
software phase.

### 4.5 Count-by-weight (checkweigh verification) — strong *secondary* check
Counting scales derive count from average piece weight, with readabilities of
0.01 g or better in precision units
([Sensors & Gauges](https://sensorsandgauges.com/blogs/latest/counting-weight-machine-efficient-and-accurate-piece-counting),
[Central Carolina Scale](https://www.centralcarolinascale.com/How-To-Buy-Counting-Scale.htm),
[Rice Lake](https://www.ricelake.com/counting-scales-resource-center/)).
DERIVATION for us: pellet = 1.18 g, so N vs N±1 differ by 1.18 g — a ±0.3 g
measurement is sufficient to resolve any N ∈ 1..10 unambiguously, which is a
*coarse* requirement by scale standards.
**But the drone kills the static case:** weighing on a multirotor requires
"vibration damping materials (silicone pads, rubber mounts) to reduce
propeller-induced noise, which can distort readings" and shielded wiring against
ESC EMI, with HX711-class conditioning
([Sensors & Gauges — drones + load cells](https://sensorsandgauges.com/blogs/latest/how-to-customise-drones-using-load-cells),
[Michigan Scientific](https://www.michsci.com/measuring-payload-release-and-landing-loads-in-drone-testing/)).
**Verdict: do not use as the primary count. Use a hopper-side load cell as a
slow, averaged *inventory* sensor** (pellets remaining, "hopper empty" warning,
and a cross-check that total dispensed over a sortie matches commanded total).
That use is tolerant of 1–2 pellet noise; per-drop counting is not.

---

## 5. Mechanism family D — Escapements (industrial parts feeding)

**How it works.** "A parts escapement is a mechanical device used in automation to
control the release of individual parts from a linear track… The escapement or
singulator stops one component and holds another. With a single stroke, one
component is released while the one behind it is then stopped."
([Bellco Feeders](https://www.bellcofeeders.com/part-escapements),
[AGI Automation feed escapements](https://www.agi-automation.com/product-category/feed-escapements/),
[Elscint pneumatic escapement](https://elscintautomation.com/index.php/2010/03/16/pneumatic-escapement/)).
Types offered commercially: motor-controlled and pneumatic **rotary**
escapements, **side-shuttle** escapements, **clamp-style** escapements
([Bellco](https://www.bellcofeeders.com/part-escapements)).
The horological **star-wheel** variant releases exactly one tooth-pitch of motion
per beat: the star "snaps forward by exactly one tooth pitch, the jumper drops
into the next notch, and the cycle repeats"
([Firgelli star-wheel escapement](https://www.firgelliauto.com/blogs/mechanisms/star-wheel-escapement)).

**The directly analogous industrial case — 6–16 mm irregular balls.** Elscint
built a bowl feeder for **cast balls 6 mm to 16 mm diameter** where "the customer
required singulation… i.e. one ball to be released on receipt of a signal, which
required highly accurate singulation mechanism", solved with a patented escapement
slide driven by a Festo cylinder. Two design notes matter for us verbatim:
"As the balls were of **irregular shapes and also having different sizes**, proper
overflow was required to ensure that the balls do not jam or get stuck in the
track. Hence, the **escapement was placed just after the bowl**", and "a 800 mm
long tube was provided which was having an **internal diameter of 20 mm so that
even the biggest ball could easily flow out**"
([Elscint cast-ball feeder](https://elscintautomation.com/index.php/2024/04/13/vibratory-bowl-feeder-for-cast-balls/)).
That is a 12 mm-class irregular sphere, singulated one-per-signal, with the
oversize-tube anti-jam rule stated explicitly. **Adopt the ≥1.6×D drop-tube rule
(≥ 20 mm ID for a 13 mm worst-case pellet).**

**Count accuracy.** Escapements are positive-displacement: one stroke = one part,
*provided* the track is fed and the part is fully seated. No accuracy percentage
is published by these vendors; accuracy is asserted structurally, same as slat
counters. Therefore an escapement still needs the §4 beam to *verify*.

**Jam behaviour.** Best-documented of any family. Jam-clearing is a designed-in
feature: "Easy part jam clearing due to internal back pressure cross port design,
this allows both rods to be retracted with the air off"
([AGI Automation](https://www.agi-automation.com/product/age-1-feed-escapement/));
and tooling "designed to guide consistent parts through efficiently while allowing
**flashed parts to recirculate rather than jam**"
([Bellco case study](https://www.bellcofeeders.com/blog/case-study-dual-bowl-system-delivers-5-part-simultaneous-escapement-at-100-ppm-for-robotic-assembly)).

**Complexity.** Low mechanically (one linear actuator, two stops) but the
canonical implementations are **pneumatic**, which we cannot have — CONTEXT gives
us 12 V only, no compressed air. A solenoid or a small servo replaces the air
cylinder at the cost of stroke force and dust tolerance. The dual-gate
("stop one, release one") arrangement needs a *filled, ordered track* upstream,
which on a drone means a gravity column — workable, since our pellets are dense
(1.30 g/cm³) and spherical, but column bridging is then the risk (§6).

**Adaptability to our pellet.** Good. A vertical gravity column of pellets in a
20 mm ID tube with a two-gate escapement at the bottom releases exactly one pellet
per cycle, orientation-free. **Verdict: strong secondary candidate; simpler than
a disc but more dependent on reliable column flow.**

---

## 6. Hopper flow, bridging and jam recovery (cross-cutting)

- **Anti-bridging by hopper geometry + agitation.** Pharma hoppers "often include
  a slow-moving agitator to prevent bridging and ensure consistent flow", with
  "angled walls and anti-clumping designs"
  ([Ruiyi](https://www.ruiyimech.com/blog/how-tablet-counting-machines-work-step-by-step-explanation),
  [Palamatic anti-bridging devices](https://www.palamaticprocess.com/en-us/bulk-handling-equipment/anti-bridging-device-conical-bottom)).
- **Reverse-drive jam clear.** Automated dispensing patents describe an explicit
  jam state machine: "Tablets may form a jam at the singulating opening or
  elsewhere, and when a tablet jam is identified by the controller, it will issue
  a 'jam clear'… the controller will drive the belt in the reverse direction, and
  the reverse driven belt may serve to dislodge any such jams **as well as to
  loosen the tablets in the hopper chamber**"
  ([US8777054](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8777054),
  [US9656794](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9656794),
  [US11594094](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11594094)).
  Pneumatic versions use a "backjet" reverse air flow for the same purpose.
- **Design consequence for us:** a pocket disc driven by a *stepper or
  bidirectional servo* gets jam recovery for free — index forward, and if the
  verification beam does not see a pellet within a timeout, reverse one step and
  retry. Reversal also stirs the pellets sitting above the disc, exactly as the
  patent describes. Report a persistent failure over the ICD feedback channel
  rather than silently under-dispensing. This directly satisfies CONTEXT's
  "commanded count must be VERIFIED (sensed), not assumed."
- **Drone-specific advantage:** the aircraft itself is an agitator. Rotor-induced
  airframe vibration, which ruins vibratory *singulation* (§3), is helpful for
  *de-bridging* a hopper. ASSUMPTION (untested): hopper bridging risk on this
  vehicle is lower than a static machine's; verify on a shaker or in hover.

---

## 7. Prior art: drone-mounted discrete-object dispensers (closest real precedent)

The mosquito-control UAS literature is the only peer-reviewed, flight-tested
precedent for dropping counted solid objects from a multirotor, and it is a very
close analogue.

**Rotary carousel dispenser** — "a servomechanism… advanced a **ratchet-and-pawl**
mechanism to rotate the carousel one position, moving a tablet over an opening in
the base of the housing." Eight chambers; 3D-printed ABS housing; **410 g empty,
730 g full**; ~1.2 kg as an installed module. The pawl "holds the position of the
ratchet and prevents it from rotating backwards."
([PLOS ONE, Case et al. 2020](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0235548) /
[PMC7500627](https://pmc.ncbi.nlm.nih.gov/articles/PMC7500627/),
[US10499628](https://patents.google.com/patent/US10499628B2/en))

**Linear shuttle dispenser** — body attaches to the landing legs; hopper, battery,
light sensor, power board, control board; "a servo swings a shuttle allowing
tablets to drop", triggered by the UAS's light signals; hopper holds up to 15
tablets ([US10499628](https://patents.google.com/patent/US10499628B2/en)).

**Measured drop accuracy** — tablets "landed an average of **1.1 m**, 95 % CI
[0.93, 1.35]" from target; **maximum spread across all drops 2.9 m**; wind
1.6–3.4 m/s "had no effect on accuracy" attributed to "the low altitude of the UAS
and **40 g weight of the tablets**"
([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0235548)).
A related programme reports "the tablet module can repeatedly deliver 40-gram
larvicide tablets within 1.1 m of the target site"
([Skyfire Consulting](https://skyfireconsulting.com/drones-for-mosquito-control/)).

**Honest read-across to our problem (important):** their 1.1 m accuracy was
achieved with a **40 g** object; ours is **1.18 g — 34× lighter**. The paper
attributes wind-insensitivity specifically to tablet weight, so **their accuracy
number does not transfer to our pellet** and CONTEXT's 1 m @ 8 m AGL requirement
must be defended by the ballistics sim, not by this citation. A 1.18 g, 12 mm,
1.30 g/cm³ sphere has a far lower ballistic coefficient and will be materially
more wind- and downwash-sensitive. This is the biggest cross-domain caveat found.

**Also note:** neither dispenser has count verification (the patent discloses
none; the operator confirms visually from the video feed) and **neither discloses
any jam-clearing mechanism**. Our design must exceed this prior art on precisely
the two axes CONTEXT calls out.

---

## 8. Friable-product handling — what pharma does about dust and fragments

- **Friability benchmark.** USP ⟨1216⟩: tablets tumble in a friabilator at
  **25 rpm for 4 minutes**, minimum 6.5 g sample, and the generally accepted limit
  is **≤ 1.0 % weight loss**; if >1.0 % the test is repeated twice and the mean of
  three used
  ([USP ⟨1216⟩ harmonised text, official 2023-08-01](https://www.usp.org/sites/default/files/usp/document/harmonization/excipients/m99935.pdf),
  [USP Tablet Friability](https://www.usp.org/harmonization-standards/pdg/excipients/tablet-friability),
  [Huanghai summary](https://drugmachines.com/blogs/news/tablet-friability-testing-guide-usp-1216)).
  **Recommendation: run exactly this test on the real herbicide pellet** — it is a
  cheap, standardised, quotable number (a jar on a rotisserie at 25 rpm for 4 min)
  and it converts CONTEXT's open friability ASSUMPTION into a measured fact that
  sizes the dust problem. Note the finding that "very dry granulations that contain
  only fractional percentages of moisture will often produce more friable tablets
  than will granules containing 2 to 4 % moisture"
  ([pharmaeducation](https://pharmaeducation.net/friability-test-of-tablets/)) —
  i.e. West Texas summer storage is the worst case for pellet dusting.
- **Mechanical dust management used in pharma:** perforated vibratory trays that
  let fines drop into a collection trap *before* product reaches the sensor, plus
  integrated vacuum ports; slat lines add static eliminators, air filters and dust
  collectors
  ([SIGMA](https://www.sigmaequipment.com/guide/slat-counter/),
  [JinLu](https://www.jinlupacking.com/blogs/pill-counting-machine-benefits/)).
  **Transplant for us:** a perforated/slotted floor under the metering disc that
  lets fines fall out of the pellet path and vent overboard in flight — free dust
  extraction, no vacuum required, since we are flying over the application site
  and the fines are the same product. (Regulatory framing is out of scope per
  CONTEXT.)
- **Fragment-tolerant sensing** is the other half: dark-time gating (§4.2) rejects
  a chip because its occlusion duration is too short, and EFS/capacitive sensing
  (§4.3) rejects it by mass. Pharma's stated approach: "Systems are programmed to
  recognize the specific dimensions of… tablets, ensuring that broken tablets or
  dust fragments do not trigger a false count"
  ([JinLu](https://www.jinlupacking.com/blogs/pill-counting-machine-benefits/));
  Countec "collects data about the wholeness of the tablet… checks if multiple
  doses are falling past at the same time", and on detecting a broken tablet
  "will trace the dose to a bottle, then reject the bottle"
  ([Key International](https://www.keyinternational.com/packaging-equipment/tablet-counters)).
  **Our equivalent of "reject the bottle" is "dispense one more pellet"** — a
  luxury pharma does not have, because our product is cheap and our tolerance is
  "N pellets on the ground", not "N pellets in a sealed bottle".

---

## 9. Comparison table

Complexity/mass columns are ASSUMPTIONS (my engineering judgement for a
drone-scale build), not sourced. Accuracy column is sourced where a number exists.

| Mechanism | Published count accuracy | Jam mode | Actuators | Adaptability to 12 mm / 1.18 g sphere |
|---|---|---|---|---|
| Slat counter (§1) | Deterministic-by-cavity; still scanned at ~2000 Hz (TruCount) | Empty cavity; part sheared by brush | Chain drive + brushes | Principle yes, machine no |
| **Rotary pocket disc (§2)** | 99.70 % (ScriptPro, per pill) | Half-seated part at wiper; recoverable by reverse index | **1** (stepper/servo) | **Best** — sphere is ideal pocket geometry |
| Vibratory channel + optics (§3) | 99.99 % = 1/10,000 (Deitz TC3, "optimal conditions"); "100 %" claimed by Cremer/Countec | Bridging, static bursts → double counts | Vibrator + feed | Poor — spheres roll; airframe vibration fights the feeder |
| **Gravity column + escapement (§5)** | none published (positive displacement) | Column bridging; flashed part wedging | 1–2 (solenoid/servo) | Good — proven on 6–16 mm irregular balls (Elscint) |
| Weigh/count-by-weight (§4.5) | Resolves N±1 easily (1.18 g steps) | n/a | 0 (load cell) | Secondary only — rotor vibration/EMI |

---

## 10. Recommendation (research agent's read; design phase owns the decision)

**Recommended architecture — "one-pocket indexing disc + verified drop tube":**

1. **Meter:** a single-pocket (or few-pocket) indexing disc under a conical
   hopper, driven by one bidirectional stepper/servo. One index = at most one
   pellet. Stationary bottom plate retains the pellet until the pocket reaches the
   outlet — the gumball-wheel/ScriptPro-cell principle (§2), with a compliant
   brush/spring wiper above the pocket to prevent a second pellet riding along
   (the spring-over-the-bore trick from US6536623).
2. **Verify:** an opposed-mode through-beam (or fiber-array) sensor across a
   ≥ 20 mm ID drop tube below the disc, with **dark-time gating** — occlusion
   shorter than the expected ~12 ms window = fragment (do not count); longer =
   two pellets or a hang-up (fault). §4.1–4.2. Add a ~30–50 ms re-trigger
   dead-time to reject a bouncing sphere.
3. **Close the loop:** index until the verified count equals N; on timeout,
   reverse-index to clear (§6) and retry a bounded number of times; report
   dispensed-count and fault status back over the ICD feedback channel.
4. **Inventory (secondary):** hopper load cell, averaged over seconds, for
   "pellets remaining" and end-of-sortie reconciliation — not per-drop counting
   (§4.5).
5. **Dust:** slotted floor around the disc so fines fall clear of the pellet path
   and vent overboard; keep the beam axis out of the fines path; rely on dynamic
   thresholding for lens drift, with a "clean me" flag (Deitz precedent, §4.2).
   If bench testing shows optical fouling within an unacceptable interval, swap
   the beam for an EFS/capacitive ring around the same tube (§4.3) — the pharma
   answer for dusty, fragment-prone product.

**Fallback if pocket-seating on real pellets proves unreliable:** gravity column
in a ≥ 20 mm ID tube with a two-gate escapement (§5), same verification stack.
Same sensor, same firmware contract — so the sensing/verification work is not
wasted if the metering element changes.

---

## 11. Open gaps / facts I could NOT establish (do not let these be invented later)

1. **Pellet friability, crush strength, moisture swelling.** No manufacturer data
   found. The Spike 20P EPA label PDF
   ([EPA 062719-121](https://www3.epa.gov/pesticides/chem_search/ppls/062719-00121-20060601.pdf))
   is a scanned image — no extractable text on pellet physicals. Brush Bullet's
   site exposes no specs
   ([brush-bullet.myshopify.com](https://brush-bullet.myshopify.com/)).
   **Action: run USP ⟨1216⟩ (25 rpm, 4 min) on real pellets in-house (§8).**
2. **Per-pellet mass distribution.** CONTEXT gives 1.18 g as a single verified
   figure; the σ is unknown. It matters for count-by-weight (§4.5) and for the
   sim. **Action: weigh 50 pellets.**
3. **Pellet-per-plant agronomy.** Spike 20P label rates found are area-based
   (3/8 oz per 100 ft² ≈ 10 lb/acre broadcast-equivalent where annual rainfall
   <20 in; 3/4 oz per 100 ft² ≈ 20 lb/acre where >20 in —
   [ArborChem](https://www.arborchem.com/product/68/spike-20p-25-lb-bag),
   [Solutions](https://www.solutionsstores.com/tebuthiuron-20p-herbicide-spike)).
   NMSU B822 covers foliar/stem/hexazinone treatments and **does not** cover
   tebuthiuron pellets ([NMSU B822](https://pubs.nmsu.edu/_b/B822/index.html)), so
   I could not verify a pellets-per-canopy-diameter rule. N ∈ 1..10 is a
   requirement from Thomas and needs no agronomic justification from me, but do
   not let anyone state a per-plant dose as fact without a label citation.
4. **Whether a DIY capacitive/EFS ring works on this pellet.** The commercial
   technology is real and dust-immune (Sparc Systems / IMA), but no low-cost
   implementation was found; treat as a prototype experiment, not a plan.
5. **Ballistics of a 1.18 g pellet from 8 m.** The only flight-tested drop
   accuracy number in this domain (1.1 m mean radial error) is for a **40 g**
   tablet and is explicitly attributed to that mass (§7). It must not be reused
   for our pellet. The sim owns this.
6. **Pocket-disc jam rate on real, irregular, dusty pellets.** No published rate
   exists for anything resembling our product; seed-metering singulation, the
   nearest quantified analogue, runs 93–97 % historically and 98–99 % for modern
   vacuum meters
   ([Precision Planting](https://www.precisionplanting.com/products/planters/precisionmeter),
   [Precision Agri Services](https://www.precisionagriservices.com/articles/what-s-the-best-seed-meter-and-drive-system)) —
   which is *far worse* than pharma and is the honest expectation band for an
   unverified mechanical metering element in field conditions. **This is the
   argument for per-pellet sensed verification with retry: it converts a ~95 %
   mechanical singulation process into a ~100 % delivered-count process, at the
   cost of a few extra index steps.**

---

## Addendum A — second research pass, 2026-08-06 (new sources only)

A follow-up sweep of pill-counting, pharmacy-automation, seed-metering and
projectile-feeder sources. Everything below is *additional* to §§0–11; nothing
above was changed. Same rules: URL-sourced, DERIVED, or ASSUMPTION.

### A.1 Baker/cassette pharmacy dispensers — the closest commercial cousin to a pocket wheel

Cassette pill dispensers (the Baker Cells lineage) use **concentric rotors**
about one axis, the outer rotor turning faster than the middle, which turns
faster than the inner, with arcuate plates forming "a stepped spiral path"
from the axis to a discharge opening. The rotors carry **radial grooves,
indentations or protrusions that prevent pills from rolling** and give
"fast and well-controlled movement of the pills"
([US4018358](https://patents.google.com/patent/US4018358A/en),
[US8794483 / RE48136 family](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8794483)).
Counting is done at the exit: "a photoelectric cell senses each pill carried to
the discharge opening via a fiber optic scanner and an electronic counter
counts the pills until the predetermined number… have passed through the
discharge opening… whereafter the machine automatically shuts down"
([US4018358](https://patents.google.com/patent/US4018358A/en)).

Two transferable details:
- **Anti-roll pocket floors.** Grooves/protrusions on the carrying surface stop
  a sphere rolling out of position. Directly applicable: our pellet is the most
  roll-prone object possible; a shallow conical or grooved pocket floor is
  cheap insurance for seating repeatability.
- **Adjustable kickoff shoe.** The cassette has "an adjustable kickoff shoe
  adjacent to the conveying wheel… such that the vacuum port of the wheel
  carries only a single pill to the discharge chute"
  ([US8794483](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8794483)).
  An *adjustable* (shimmable) doubles-rejection element at the pocket exit —
  rather than a fixed printed feature — lets the jam/doubles behaviour be tuned
  on real pellets without reprinting the disc. Recommended for the r-series
  prototype.

Architecturally this confirms the §10 recommendation: commercial pharmacy
dispensers are **positive-displacement metering with a photoelectric exit
counter**, i.e. exactly the "index + verify" loop, not sensor-only counting.

### A.2 Prior art update — a drone pellet dispenser that *does* claim anti-jamming

§7 states that the mosquito-control prior art discloses no jam-clearing. One
further precedent partially contradicts that: Arizona State University's
"Drone Deployable Automated Pellet Dispensing System" (licensing listing,
Skysong Innovations) — a lightweight, 3D-printable payload for **metered
dispensing of vaccine pellets**, integrated with the flight controller for
preprogrammed deployment of "multiple pellets", explicitly including
"an anti-jamming mechanism for a more robust operation", motivated by the fact
that traditional hoppers "frequently jam"
([Skysong Innovations](https://skysonginnovations.com/technology/drone-deployable-automated-pellet-dispensing-system/)).

Caveat, important: the public listing is a licensing abstract. It discloses
**no mechanism, no count-verification method, no capacity, and no accuracy
figure**. Its evidentiary value is limited to three things: (1) the
drone-metered-pellet niche is real and independently pursued, (2) *hopper
jamming is the acknowledged dominant failure mode* in this exact application —
supporting Thomas's 23:03 directive as the right thing to design against, and
(3) 3D-printed metering hardware is accepted practice at drone mass budgets.
**Do not cite it for any number.** Fishing-drone "bait release" products are
single-payload claw/hook releases with no metering or counting and are not
relevant prior art ([Rippton](https://www.rippton.com/blog/the-tech-behind-the-fishing-drones-with-bait-release)).

### A.3 Compliant drive elements — the projectile-feeder answer to crush-vs-jam

Paintball loaders face our exact trade (fragile spheres, a powered feed element,
jam risk). The patented answer is a **deliberately compliant driver**: "the
elastic member is formed so that it will bend when the rigid projection
encounters a jammed or stationary paintball, thus preventing paintball
breakage"; agitators appear as "paddle wheels, shaped members, arms, paddles,
wires, fins, and vibrating members" on the drive shaft, and an "auger-like
member… rotatably mounted at the bottom outlet [is] operable to clear a
paintball feed jam"
([US7694669B2](https://patents.google.com/patent/US7694669B2/en),
[bulk loader US6415781](https://patents.justia.com/patent/6415781)).

Read-across for our hopper agitator (distinct from the metering disc): make the
**agitator** compliant so it deflects rather than crushing pellets and
generating the very fragments that threaten the disc, and keep the **disc**
stiff and torque-backed so it can shear a fragment when it must (CONTEXT §2).
Compliance belongs upstream of the shear line; stiffness belongs at it. That
split is a design rule worth stating explicitly in the build notes.

### A.4 Celled disks vs flat vacuum disks — why our pocket should be a *cell*

Seed-meter patent art gives the quantitative reason to prefer a recessed pocket
over a flat-face hole: celled disks "offer the unique advantage of permitting
the meter to generally operate at **lower vacuum levels** than meters that use
flat or non-celled disks because the indentations or cells assist in holding
the seeds in place"; conversely celled disks have "a higher tendency to plant
skips and doubles in near succession when planting **flat** shaped seeds"
([US7334532](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7334532);
see also seed singulator [US7699009](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7699009)
and its reissues RE45412 / RE47447).

DERIVED read-across: the cell's known weakness (doubles) is a *flat-seed*
failure; our pellet is a near-sphere, the favourable case. The cell's known
strength — geometric retention without external holding force — is exactly what
lets us drop the vacuum system entirely (§2 of Addendum-free text already
rejects vacuum on dust grounds; this is the independent mechanical argument for
why we can afford to).

### A.5 Vibratory/optical mainstream — one more accuracy datapoint and the anti-dust menu

- Tabletop pharmacy counter datapoint: **Kirby Lester KL1** counts "almost any
  tablet or capsule… without ever needing recalibration" at up to
  **15 tablets/second** by optic sensing, versus manual counting at "only 95 %
  accurate at best"
  ([Capsa KL1](https://www.capsahealthcare.com/product/kl1-tablet-counter/),
  [KL1 operating manual PDF](https://www.capsahealthcare.com/wp-content/uploads/2024/07/KL1-Operating-Manual-5DIM-380301-OM-Rev-B.pdf)).
  Useful only as a bound: 15/s is ~3× our peak 5/s requirement, so nothing about
  our rate is demanding.
- Anti-dust options actually shipped on high-end counters: "**electrostatic
  field sensors or targeted vacuum ports**" as dedicated anti-dust features,
  and vision as a cross-check on IR counting
  ([Ruida](https://ruidapacking.com/why-need-a-vision-based-counting-machine-in-addition-to-an-ir-based-pill-counter/),
  [Ruida buying guide](https://ruidapacking.com/tablet-counting-machine-buying-guide/)).
  This corroborates §4.3's EFS fallback from a second independent vendor.
- Free-fall timing discrimination is explicitly claimed in tablet-dispenser
  patent art: "by accurately detecting On and Off signals with a time
  difference between times at which tablets fall down, the detecting sensor can
  accurately detect the number of tablets without any error, as tablets fall
  down while being separated apart by free-falling"
  ([US8386073](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8386073)).
  This is the patent-art backing for the §10.2 dark-time gating scheme.
- Positive-count practice — verifying *fill state* rather than trusting the
  cavity — is the subject of dedicated art: "positive count rotary slat
  packaging apparatus"
  ([US6505460](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6505460),
  [US6401429](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6401429)).
  Supports adding a **pocket-position encoder cross-check** ("this index should
  have produced exactly one drop") alongside the beam, so a missing drop is
  distinguishable from a missing *pellet*.

### A.6 Bulk-solids cell wheels — the granulometry warning

Rotary airlock / star feeders are the industrial-scale version of our disc:
cell wheels meter powders and granulates volumetrically from hoppers, with
rotor options including "blade, rounded type, adjusted blade type, stripper and
polyamide" chosen by material
([Sultan rotary valve](https://www.sultan.com.tr/eng_rotaryvalve.htm),
[QLAR glossary](https://www.qlar.com/glossary/rotary-airlock-feeder),
[GlobalSpec star/paddle feeders](https://www.globalspec.com/ds/2896/areaspec/type_star_paddle_rotaryvalve)).
The vendor warning is the useful part: "a single fault in design may give damage
to the material being transported… a slight change in granule size and a
different material can mean failure of such equipment"
([Sultan](https://www.sultan.com.tr/eng_rotaryvalve.htm)).

Read-across: cell-wheel performance is **granulometry-specific**, and our feed
granulometry is *not* constant — it drifts toward fragments and fines over a
sortie. That is the honest statement of the risk behind CONTEXT §1–4, and it
argues for (a) stripper/wiper hardware on the rotor (an option these vendors
sell precisely for this), and (b) validating the disc on *aged, pre-tumbled*
pellets rather than fresh ones. Add "tumble the test lot first" to the bench
protocol.

### A.7 Additional facts still NOT established in this pass

7. **Tebuthiuron pellet crush strength / hardness.** Still unfound. Product
   pages confirm only the formulation class — a "pelletized clay" carrier at
   20 % a.i. that "resists breakdown on the soil surface" until rainfall
   dissolves it
   ([Azelis](https://azelisaes-us.com/grow_your_know/tebuthiuron-invasive-brush/),
   [Solutions Stores](https://www.solutionsstores.com/tebuthiuron-20p-herbicide-spike)) —
   which tells us the pellet is engineered for *weathering* resistance, not
   *mechanical* strength, and is water-disintegrable. ASSUMPTION for design:
   treat crush force as a bench-measured unknown; do not let any downstream doc
   state a number without the bench test behind it.
8. **ASU/Skysong mechanism.** Licensing abstract only; no mechanism, count
   method, capacity or accuracy is public.
9. **Whether an adjustable kickoff shoe can be made dust-tolerant.** Pharmacy
   cassettes run in clean indoor air; no field-dust data exists for that
   element.