# RESEARCH — Bulk dispenser / metering mechanisms for exact-count pellet drop

Research agent, 2026-08-06 (rev 2 — adds rotary-valve vane-tip shear literature,
slat counters, the IGNIS drone benchmark, pellet crush-strength estimation, and
sensor-in-dust data in response to the 23:03 fragment-wedge directive).

Domain: fish/pet feeders, candy/gumball vending, bulk part singulation (bowl
feeders), plus the adjacent exact-count trades (pharmacy slat counters, aerial
ignition sphere dispensers, rotary airlock valves).

Target from CONTEXT.md: meter EXACTLY N (1–10, usually 1–3) pellets per command;
pellet ≈ 12 mm (±1 mm ASSUMPTION), 1.18 g, white molded sphere with parting
line; hopper ≥ 250 pellets; drone belly mount; dusty/hot/windy West Texas
ranch; pellets can break into fragments in the hopper.

Everything below is from the cited source unless marked **ASSUMPTION**,
**DERIVED**, or **RULE-OF-THUMB**. Nothing here is invented.

## Framing (why our problem is the easy end of singulation)

1. Spheres need no orientation — the thing bowl feeders exist to solve does not
   apply to us. Bowl-feeder tooling is ~all orientation logic
   ([Bowl feeder, Wikipedia](https://en.wikipedia.org/wiki/Bowl_feeder)).
2. N is small (1–10) and we may spend ~1 s per pellet (hovering aircraft), so
   throughput engineering is irrelevant.
3. CONTEXT.md already requires the count be **sensed**, not assumed. That
   changes the mechanism requirement from "deliver exactly N" to "deliver **at
   most one** pellet per event, and never lie about it" — the sensor closes the
   loop on exactly-N. This is the pharmacy pill-counter architecture and it is
   the single most important structural decision in this document.
4. The genuinely hard requirement is not counting. It is **not jamming on
   fragments** over a full sortie, with no operator present.

---

## 0. Benchmark: the closest existing flying machine (calibrates mass/capacity)

**Drone Amplified IGNIS** dispenses plastic ignition spheres from a bulk hopper
on a multirotor, one at a time, in smoke/dust/heat — the nearest real-world
analogue to this payload.

- IGNIS III Mini: **19 mm spheres, 2.4 g each, 225-sphere capacity, 1.87 kg
  loaded / 1.25 kg empty, up to 120 spheres/min, 2–5 min reload**
  ([IGNIS system datasheet](https://droneamplified.com/ignis-system-datasheet/)).
- Full-size IGNIS: up to 450 spheres, 10–120 spheres/min
  ([IGNIS overview](https://droneamplified.com/ignis-system-safer-faster-prescribed-burns/);
  [IFSJ interview](https://internationalfireandsafetyjournal.com/ifsj-exclusive-controlling-the-burn-with-drone-amplified/)).
- Each sphere is punctured and injected with glycol immediately before release;
  the firmware detects **bent or clogged needles** and notifies the operator
  ([Ignis II operational manual, FAA docket](https://downloads.regulations.gov/FAA-2025-0823-0001/attachment_6.pdf)).

**Read-across (DERIVED):** a 225-sphere, single-file, gravity-fed, one-at-a-time
drone sphere dispenser with agitation and injection hardware weighs 1.25 kg dry.
Our budget is ≤ 1.5 kg total at a 250-pellet (295 g) load → ~1.2 kg dry. That is
right at IGNIS-class density, and we have **no** injector, needle, pump, or
antifreeze tank to carry. The mass budget in CONTEXT.md is therefore credible
but not generous: the meter must stay simple.

## 1. Celled pocket wheel / gumball-candy dispensing wheel — POSITIVE DISPLACEMENT

**How it works.** A flat disc with through-pockets sized slightly larger than one
ball rotates between a hopper floor and a fixed base plate. Each pocket fills by
gravity under the hopper, is covered in transit by a **brush plate** (a bristle
ring that both seals the aperture against free flow and wipes back extra
product), then registers with a discharge hole and the ball drops. Classic
gumball machines index 120° with three ~1 in apertures
([US6536623B1](https://patents.google.com/patent/US6536623B1/en)).
The brush plate "keeps the candy inside the machine so it does not come out when
the machine is not in use, reduces jams and incorrect feeding, and controls even
dispensing together with the wheel"
([Gumball Machine Warehouse — wheel + brush plate](https://www.gumball-machine.com/products/gumball-wheel-brush-plate);
[adjusting the candy wheel](https://www.candymachines.com/blogs/vend-talk/adjusting-the-wheel-on-your-candy-vending-machine);
[adjusting the dispensing wheel](https://www.gumballs.com/how-to-adjust-gumball-machine-dispensing-wheel.html)).
Adjustable-aperture wheels are COTS for different ball sizes
([wheel + brush plate set](https://www.amazon.com/Dispensing-Wheel-15-Vintage-Carousel/dp/B0GQXNWY87)).

**Count accuracy.** One pocket = one ball **by geometry**, provided pocket depth
< 2 pellet diameters and the brush/wiper covers the pocket through the transit
arc. The residual error is a *skip* (unfilled pocket), not a double — the
benign direction, fully recovered by "keep indexing until the beam counts N."

**Jam behavior — this is the key literature for the 23:03 directive.** The
gumball wheel patent names our exact failure mode as the known field problem:
jams are caused by "a gumball not being properly seated in the dispensing
mechanism … **an extra gumball becoming partially seated in a dispensing wheel
aperture, or … becoming lodged between an aperture and one of the other parts**
of the gumball machine" ([US6536623B1](https://patents.google.com/patent/US6536623B1/en)).
That is precisely Thomas's "1.5 brush bullets in the pocket" wedge. Notably the
patent's fix is **aperture shape** (arcuate or peanut-shaped openings sized to
exactly two balls side-by-side, "not any larger"), i.e. geometry that gives a
partially-seated ball somewhere to go rather than a shear line to wedge on.
Field service lore adds two more causes and their remedies: debris/sticky
residue on the wheel, and **overfilling the hopper, which loads the wheel so it
cannot turn** ([Gumball.com repair guide](https://www.gumball.com/blogs/news/how-to-fix-a-gumball-machine);
[Homesteady](https://homesteady.com/12391188/how-to-repair-gumball-machines)).
→ Design consequences: (a) shape the pocket mouth, do not just bore a cylinder;
(b) **decouple hopper head-load from the wheel** (a bridge/roof or a separate
staging cavity above the disc) so a full 250-pellet column is not pressing on
the shear line.

**Complexity.** Lowest of every candidate: one motor, one disc, one fixed plate,
one brush. No vacuum, no vibration, no pneumatics, fully printable/CNC-able.

**Adaptability.** Excellent. Bore pockets for 13 mm worst case, depth
~0.8–1.0 × D so a second whole pellet cannot ride in the pocket; stepper-indexed
so it can reverse. Molded herbicide pellets are more dimensionally uniform than
candy-coated gum, which this mechanism has survived commercially for a century.
**Primary recommendation**, hardened with §2, §11, §12, §13.

## 2. Rotary airlock valve — the industrial big brother of the pocket wheel

**How it works.** A vaned rotor turns in a close-fitting housing between a bulk
inlet and a discharge; each pocket carries a fixed volume down. Same physics as
§1 with decades of hard-particle jam engineering behind it
([Rotary airlock valve principles and rotor design, Powder & Bulk Solids](https://www.powderbulksolids.com/valves-gates-airlocks/rotary-airlock-valve-principles-and-rotor-design);
[engineering guide](https://powderprocess.net/Equipments%20html/Airlock_Rotary_Valve.html)).

**Directly transferable anti-wedge design vocabulary (the most useful find of
this research pass):**
- **Shear/jam is the named failure mode:** "shearing and jamming occurs when
  hard, large particles enter the valve and pinch between the rotating rotor
  vanes and the body inlet throat, causing vibration, squealing, or even
  jamming" ([Powder & Bulk Solids](https://www.powderbulksolids.com/valves-gates-airlocks/how-to-choose-a-rotary-airlock-for-your-application)).
- **Beveled / relieved vane tips** reduce drag and smearing at the shear line —
  the standard treatment ([rotor design](https://www.powderbulksolids.com/valves-gates-airlocks/rotary-airlock-valve-principles-and-rotor-design)).
- **Flexible (rubber) tips** for gravity/low-ΔP service: "if a particle becomes
  trapped between the flexible tip and the housing, the tip either gives way" or
  guides the particle to discharge. Compliance instead of shear — this is the
  mechanical embodiment of "reject before wedge." (same source)
- **Side-entry rotors** are specified "in applications where product shearing is
  a concern," feeding the rotor from the side instead of the top so material is
  never trapped against the inlet throat. (same source)
- **Scalloped (rounded-U) pockets** discharge more completely than V-pockets;
  **reduced-volume rotors** prevent bridging above the inlet. (same source)
- **Reversing recovery is prior art:** a controller "reverses the original
  direction of rotation of the vanes … several times in momentary succession,
  and then continues rotation in its original direction," and on a hard jam the
  rotor reverses so the offending material "falls into the pocket or is cut"
  ([US5575085](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5575085)).
- Rotor-to-housing clearances of **0.004–0.006 in (0.10–0.15 mm)** are normal
  practice; note this is chosen to *prevent* particle jamming at contact points
  as much as to seal. ([rotor design](https://www.powderbulksolids.com/valves-gates-airlocks/rotary-airlock-valve-principles-and-rotor-design))

**Count accuracy.** Volumetric, not per-item — irrelevant as a product, but the
rotor-design catalogue is exactly what the pocket-wheel critic needs.

**Complexity/adaptability.** COTS units are far too heavy for a drone. Adopt the
*features*, not the part: beveled pocket lips, a compliant (TPU/silicone or
bristle) wiper at the shear line, side/relieved entry, reverse-oscillate on stall.

## 3. Slat counter (pharmaceutical exact-count by pockets)

**How it works.** A chain of grooved slats, each groove subdivided into cavities
sized to one tablet, passes under the product bed; one tablet drops into each
cavity, then the slat inverts over a chute and the tablets fall into the
container. Count = cavities passed. As the container approaches target count, a
**blocking gate** closes off all but one lane so the last few units are metered
singly ([ipharmachine — tablet counting machine principle](https://www.ipharmachine.com/tablet-counting-machine-principle);
[IMA HYBRID-39 slat counter](https://imagroup.com/machines/slat-counter/);
[Ruida buying guide](https://ruidapacking.com/tablet-counting-machine-buying-guide/)).

**Count accuracy.** Exact by geometry, not by sensing — the pharma industry
trusts it for legally-counted product. The "block all lanes but one near the
end" trick is the direct analogue of "index one pocket at a time for N ≤ 10."

**Jam behavior.** Pockets are open-topped and shallow; over-tall product is
wiped back into the bed rather than sheared into a closed housing. Complexity is
high (chain, slats, inversion) and it is a bench machine, not flight hardware.

**Adaptability.** Not as hardware. Adopt the *principle*: **exact count should
come from discrete pockets, with the sensor as verification, not the other way
round.** A pure sensor-gated continuous flow (auger, gate) is strictly worse.

## 4. Rotating drum with peripheral holes (fish-feeder class)

**How it works.** A horizontal barrel with peripheral holes turns under/inside
the hopper; product falls into a hole at the top and out at the bottom. Standard
aquaculture feeder architecture; rate set by hole count, speed and fill level
([drum-type feed metering study, Springer 2024](https://link.springer.com/article/10.1007/s44279-024-00052-z);
[hobby drum feeder](https://www.ratemyfishtank.com/blog/how-to-build-an-automatic-fish-feeder);
[Hackaday stepper drum feeder](https://hackaday.com/2025/09/23/automatic-feeder-keeps-fish-sated/)).

**Count accuracy.** Commercial drums meter *mass rate*, not count. Size the hole
to exactly one 12 mm pellet and it degenerates to §1 on a horizontal axis, with
the same per-pocket accuracy.

**Jam behavior.** Same shear-at-lip mode as §1, but the entire hopper column
bears on the drum surface, which helps filling and *hurts* wedge force — the
opposite of what the gumball overfill lore recommends.

**Complexity/adaptability.** Low complexity; poorer packaging for a belly
payload (bulkier vertically, and ground clearance under the bottom plate is
tight per CONTEXT.md). Viable fallback, not first choice.

## 5. Escapement / nest — deterministic one-per-cycle release

**How it works.** Pellets form a single-file column; two stops alternate. The
classic two-pin form: "the lever arm includes a stop pin which passes through a
hole in the tube to stop the next succeeding ball from being released, so that
only one ball is released at a time," with release and retention pins driven in
alternating cycles by one lever
([golf-ball dispenser US7506781](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7506781);
also [US4575092](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4575092),
[US5554077](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5554077)).
Industrial automation calls the two-stop form a **tic-toc escapement**; side
shuttle, rotary-actuator and blow-feed variants exist, and part-presence sensors
at the pick position are standard
([RNA Automation escapements and nests](https://www.rnaautomation.com/products/feeding-and-handling/spares-standard-equipment/escapements-and-nests/);
[Bellco part escapements](https://www.bellcofeeders.com/part-escapements);
[star-wheel escapement primer](https://www.firgelliauto.com/blogs/mechanisms/star-wheel-escapement)).

**The airborne proof case — aerial ignition PSDs.** Plastic Sphere Dispensers
feed ~32 mm incendiary spheres from a bulk hopper in a vibrating aircraft:
spheres line up in downward-sloping chutes controlled by **anti-jam slipper
blocks**, and the slipper moves each sphere onto the injection needle
([Fire Ignition Resources / Premo dispenser](https://premofireusa.com/dispenser.html);
[USFS MTDC PSD description](https://www.fs.usda.gov/t-d/aerial_ign/plsphere/describe.htm);
[USFWS PSD operator account](https://www.fws.gov/story/2023-09/aerial-ignitions-plastic-sphere-dispenser-operator)).
[US10871358B2](https://patents.google.com/patent/US10871358B2/en) is the most
instructive: a bulk hopper with a **rotating agitator in the hopper sump near
the exit hole**, an S-shaped feed tube in which spheres "line up in series," and
a **nest** — a semicircular cavity that captures exactly one sphere, retained by
a **flapper valve of thin spring steel** whose stated job is to "ensure that any
incendiary spheres that enter the nest do not over-run it." The sphere leaves
only when the injector drives it out; each sphere is fully discharged **before
the next in line is selected**, which the patent explicitly credits for avoiding
the ball-to-ball contact problems of the competing design.

**Count accuracy.** Exactly one per cycle, by geometry, *provided the column
stays fed* — the best raw accuracy of the simple mechanisms, and it gives a
positive two-state "staged / released" that a sensor can confirm.

**Jam behavior.** The escapement itself is nearly jam-proof (compliant flapper,
no closed shear arc). The weak point moves upstream to the hopper→tube funnel,
where 12–13 mm spheres bridge (see §11). Slightly-out-of-round molded pellets
force tube ID ≥ 13 mm, which permits cocking — pin placement must assume the
worst-case tilted pellet.

**Complexity/adaptability.** One servo can drive a see-saw rocker for both pins.
**Strong runner-up and an excellent final stage below a pocket wheel:** the
wheel does bulk→single-file (the hard part), the escapement does the
deterministic release and gives a clean sensing station.

## 6. Auger / screw feeder — REJECTED as the meter

**How it works.** Motor-driven screw in a tube; dispensed amount ∝ revolutions.
Ubiquitous in fish/pet feeders and noted as better than plain gravity funnels,
which clog
([ESP32 auger fish feeder](https://www.researchgate.net/publication/399269050_ESP32_IoT_Auger-Based_Automatic_Feeder_for_Fish_Pellets);
[Digi-Key auger candy dispenser](https://www.digikey.com/en/maker/projects/the-scaredy-pi-automated-candy-dispenser/fb973b3547bc4583bf9b8cecb0673a47)).
Pond-feeder vendors market augers as the "exact" option — but only in the sense
that each turn dispenses a consistent *small amount*
([Hatton Koi feeder guide](https://hattonkoi.com/blogs/koi-blog/automatic-fish-feeders-for-ponds-explained)).

**Count accuracy.** Volumetric. Zero discrete guarantee; pellets at the tube exit
are in an undefined state when the motor stops, so 0–2 extra can trail out.
Unacceptable for N = 1.

**Jam behavior.** Worst of any candidate for us: the screw *positively crushes*
anything pinched between flight and tube wall, generating exactly the fragments
and dust we are trying to survive.

**Complexity/adaptability.** Low complexity, wrong mechanism. **Rejected.**

## 7. Vacuum disc seed meter — REJECTED (dust)

Rotating holed disc, vacuum holds one seed per hole, a singulator wiper knocks
off doubles, release where vacuum is cut
([Precision Planting vSet](https://www.precisionplanting.com/products/planters/vset);
[celled-disk vacuum meter US7334532](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7334532)).
Best-in-class singulation ~98–99 %
([comparative analysis of precision seed planters](https://www.researchgate.net/publication/337736373_A_comparative_analysis_of_precision_seed_planters))
— but that is *per-seed at high rate*, still with doubles and skips, and it
needs a vacuum source, seals and power against a 2 A/12 V budget, plus a
meaningful hold force for a 1.18 g pellet. Vacuum holes clog with dust, and dust
is a design condition here. **Rejected as hardware; adopt its singulator-wiper
idea into §1.**

## 8. Finger-pickup / belt meters — REJECTED (complexity, no benefit for spheres)

Spring fingers grab one seed each and carry it to release
([Precision Planting PrecisionMeter](https://www.precisionplanting.com/products/planters/precisionmeter);
[long-belt finger-clip meter study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8831804/)).
Historically 90–95 %, improved variants 98–99 %, and sensitive to seed
size/shape ([comparative analysis](https://www.researchgate.net/publication/337736373_A_comparative_analysis_of_precision_seed_planters)).
Many tuned springs to achieve *less* than a pocket wheel gives us on uniform
spheres. **Rejected.**

## 9. Vibratory bowl feeder / step feeder — REJECTED as hardware, one idea kept

Bowl feeders vibrate parts up a spiral track past tooling that rejects
wrong-orientation parts ([Wikipedia](https://en.wikipedia.org/wiki/Bowl_feeder);
[Assembly Magazine](https://www.assemblymag.com/articles/93032-vibratory-bowl-feeders-for-automated-assembly);
[working principle](https://bbfvibratoryfeeder.com/bowl-feeder-working-principle/)).
Heavy resonant base, continuous power, fill-level sensitive — unflyable.
Worth noting for the friability problem: the industry's own answer for fragile
parts is the **step feeder**, which lifts parts on reciprocating plates with
"minimal vibration and virtually no part-on-part contact … significantly reduced
part abrasion," and is chosen where vibratory feeding causes 1–3 % scrap
([Performance Feeders step feeders](https://performancefeeders.com/products/step-feeders);
[Bellco step feeders](https://www.bellcofeeders.com/step-feeders);
[step vs vibratory comparison](https://www.hubenauto.com/blog/step-feeder-vs-vibratory-feeder)).
**Takeaway:** attrition of our pellets is driven by part-on-part rubbing and
vibration — so do *not* add a vibrator as the primary anti-bridge remedy; use a
slow compliant agitator (§11) instead. Short vibration pulses remain a legitimate
last-resort unbridging action.

## 10. Weigh-count (load cell) — viable *secondary* verification, not a meter

Counting scales derive count from total weight ÷ average piece weight; accuracy
is bounded by **piece-to-piece weight variation**, and "no counting scale will
ever work if there is significant variation in the weight of the items"
([GlobalSpec — selecting a counting scale](https://insights.globalspec.com/article/24969/how-to-select-a-counting-scale-key-factors-for-accurate-parts-counting);
[Rice Lake counting scales resource center](https://www.ricelake.com/counting-scales-resource-center/);
[Mettler counting manual PDF](https://www.dataweigh.com/media/13297/countmanual.pdf)).

**Relevance.** Our piece weight is 1.18 g. A load cell under the hopper measuring
Δmass per dispense would be an *independent* count channel immune to optical dust
fouling — but on a hovering multirotor the vibration and aero loads make a 1.18 g
resolution measurement implausible in flight (**ASSUMPTION**, not measured).
**Recommended use:** hopper load cell for *remaining-inventory* estimation and
pre-flight/post-flight audit, not per-dispense counting. Broken pellets also
violate the uniform-piece-weight premise, so treat it as coarse.

---

## 11. Bridging / arching prevention (the real hopper risk)

- Bridging = a stable arch over the outlet; ratholing = a stable vertical void.
  Remedies are steep mass-flow geometry, stirrers/agitators, internal screws,
  aeration, vibration
  ([Accendo Reliability](https://accendoreliability.com/bridging-silos-hoppers/);
  [LCI — prevent ratholing and bridging](https://www.lcicorp.com/en/_site_lci/powder-handling-equipment/circle-feeder/prevent-ratholing-and-bridging-in-your-hopper);
  [hopper stirrer US5516009](https://patents.google.com/patent/US5516009A/en);
  [feed hopper agitator US5160016](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5160016)).
- For our material class the mechanism is **mechanical interlocking**, not
  cohesive arching: hopper-design references treat coarse free-flowing solids
  (≥ ¼ in particles) as the easy funnel-flow case and compute outlet size from
  *cohesive* strength, which is ~nil for hard 12 mm spheres
  ([Chemical Engineering — hopper outlet geometry and arching](https://www.chemengonline.com/facts-fingertips-hopper-outlet-geometry-arching/);
  [Jenike & Johanson — arching/ratholing](https://jenike.com/solutions/solve-or-prevent-poor-flow/)).
  **RULE-OF-THUMB (standard bulk-solids practice; I could not source a single
  citable statement of it this pass — treat as unverified):** circular outlets
  ≥ 6–8 × particle diameter avoid interlocking arches. For 12 mm pellets that is
  72–96 mm — impractically large for a meter that must isolate one pellet.
  **Therefore: do not rely on a passive funnel.** Put a slow compliant agitator
  directly above the metering pockets (the same trick as the gumball agitator
  stack and the IGNIS/PSD hopper-sump agitator, [US10871358B2](https://patents.google.com/patent/US10871358B2/en))
  so every index cycle breaks any arch for free, at zero added actuators if it
  shares the wheel shaft.
- **Do not overfill / do not let the column bear on the shear line.** Overfilling
  a gumball globe is a documented cause of the wheel being unable to turn
  ([Gumball.com](https://www.gumball.com/blogs/news/how-to-fix-a-gumball-machine)).
  With 250+ pellets this matters: DERIVED, 250 × 1.18 g = 295 g of column load,
  and a roof/bridge over the meter converts that from a shear-line preload into
  a structural load on the housing.
- **Moisture/clumping:** the pet-feeder trade's standard mitigations are
  desiccant in the hopper, airflow/fans, stirring the product at each cycle, and
  preferring pellets over flakes
  ([Bulk Reef Supply feeder guide](https://www.bulkreefsupply.com/content/post/how-to-choose-the-right-automatic-fish-food-feeder);
  [Hatton Koi guide](https://hattonkoi.com/blogs/koi-blog/the-essential-automatic-fish-pond-feeder-guide)).
  Relevant because tebuthiuron pellets are a clay carrier that is *designed* to
  disintegrate on wetting ([Azelis on tebuthiuron](https://azelisaes-us.com/grow_your_know/tebuthiuron-invasive-brush/)):
  a sealed hopper lid plus a desiccant pocket is cheap insurance, and the hopper
  must not be left loaded through a dewy night.

## 12. Pellet crush strength — what force is actually available to shear a fragment

CONTEXT.md item 2 of the 23:03 directive demands actuator torque exceed the
force to shear a fragment. No published crush data for tebuthiuron 20P pellets
was found (searched; product listings describe only "heavy, high-density clay
pellets that stay stable on the soil surface and resist breakdown" —
[Azelis](https://azelisaes-us.com/grow_your_know/tebuthiuron-invasive-brush/);
[Spike 20P listing](https://diypestcontrol.com/spike-20p-5lb)). Nearest data:

- A dispersible granular pesticide substrate patent specifies **crush strength
  2–8 lb (≈ 9–36 N) on an 8-mesh (~2.4 mm) pellet**, with ASTM E728-91 attrition
  resistance ≥ 85–90 % ([US8404259B2](https://patents.google.com/patent/US8404259B2/en)).
- Standard test methods: **ASTM D4179** single-pellet side crush strength (SCS)
  for "spheres, short cylinders or tablets," force applied until fracture;
  **ASTM D6175** radial crush (0–65 N/mm) for 1.6–3.2 mm extrudates; **ASTM
  D7084** bulk crush, which yields **0.1–0.35 MPa for granules and 1–3.5 MPa for
  larger formed materials**
  ([Mecmesin — crush strength testing of catalyst pellets](https://www.mecmesin.com/publications/crush-strength-testing-catalyst-pellets);
  [crush strength units explainer](https://wtb-machine.com/crush-strength-units/)).
- Feed-industry practice measures **Pellet Durability Index (PDI)**, mass % of
  pellets surviving tumbling; ≥ 95 % is "high quality"
  ([Milling and Grain — PDI test device](https://millingandgrain.com/measuring-pellet-quality-pellet-durability-index-p-d-i-test-device/);
  [USDA-ARS, durability and breakage of feed pellets under repeated handling](https://www.ars.usda.gov/ARSUserFiles/30200525/372DurabilityandBreakageofFeedPelletsDuring.pdf)).
  PDI is the right metric to quote for "pellets break in the hopper from
  vibration" — repeated handling measurably degrades pellets, per the ARS study.

**DERIVED estimate (label as ASSUMPTION downstream).** For point/side loading of
a brittle sphere the Hiramatsu–Oka relation gives tensile strength
σ_t ≈ 2.8 F / (π d²), i.e. F ≈ σ_t·π·d²/2.8. For d = 12 mm: **F ≈ 162 N per MPa
of σ_t.** A weak pressed-clay pellet at σ_t ≈ 0.3–1 MPa fractures at roughly
**50–160 N**; a hard one considerably more.

**Consequence for the design — the honest number.** A NEMA-17-class stepper with
a ~5:1 gearbox delivers on the order of 2 N·m (**ASSUMPTION**, typical catalogue
value — verify against the chosen motor). At a 25 mm pocket radius that is
**80 N** tangential. That is *at or below* the estimated force to crush a whole
pellet, and only comfortably above the force to break a *fragment* loaded on an
existing fracture face. **Therefore "shear it" cannot be the primary defence.**
The design must lead with rejection-before-wedge (compliant wiper, relieved
pocket lip, side/roofed entry — §1, §2) and treat shear as a backstop only for
small fragments, with reverse-oscillate recovery (§13) as the real second line.
Any claim that the actuator "can shear a jam" must cite a measured crush force.

**ACTION for Thomas (cheap, definitive, 5 minutes):** crush 10 pellets one at a
time on a kitchen scale under a flat plate and record peak kgf (× 9.81 = N),
plus 10 halves/fragments. That single measurement replaces this whole section
and unblocks the torque-margin claim.

## 13. Stall detection and jam recovery (directive item 3)

- **Sensorless stall detection is a solved commodity.** The TMC2209 computes a
  load value (SG_RESULT) from motor back-EMF that falls as load rises; crossing a
  configurable threshold asserts the DIAG pin. StallGuard4 is the variant used
  and is optimised for StealthChop
  ([TMC2209 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/tmc2209_datasheet_rev1.08.pdf);
  [StallGuard/sensorless homing walkthrough](https://deepwiki.com/kjk25/TMC2209_ESP32/4.4-stallguard-and-sensorless-homing);
  [setup guide](https://thinkrobotics.com/blogs/tutorials/tmc2209-sensorless-homing-tutorial-complete-setup-guide)).
  Caveat from the field: StallGuard sensitivity is speed-dependent and needs
  calibration at the operating velocity ([Duet3D forum thread](https://forum.duet3d.com/topic/34501/stallguard-and-endstop-with-tmc2209);
  [SgSetup ESP32 calibration tool](https://github.com/bdring/SgSetup_ESP32)).
  Plain motor-current sensing is the fallback and is sufficient at our speeds.
- **The recovery routine is prior art, not invention:** on jam, reverse "several
  times in momentary succession, then continue in the original direction"
  ([US5575085](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5575085)).
  Adopt verbatim as the pocket-wheel recovery: reverse ~15–30° and re-advance,
  up to K attempts, escalating amplitude, then declare FAULT and report.
- **Count truthfulness through a recovery (CONTEXT.md requirement).** Two rules:
  (a) the counter must be edge-triggered on the drop-tube beam only, never on
  motor steps, so reversing cannot manufacture a phantom count; and (b) place
  the beam *below* the point of no return so a pellet that is counted can never
  be pulled back — or, if reversal can retract a staged pellet, use two beams
  (staged / released) as in escapement practice (§5), and decrement only on a
  confirmed released-beam edge. Paintball loaders already gate motors on optical
  "eyes" for the same reason ([US8210159](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8210159)).
- **Compliant drive as a torque fuse.** Dye Rotor-class loaders feed 17 mm
  fragile gelatin balls by coupling the carousel drive arms through an elastic
  member: rigid in normal feed, but against a jammed ball the spring deforms and
  the arm passes over the ball without breaking it
  ([US7694669](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7694669);
  [Dye LT-R loader](https://www.amazon.com/Dye-Paintball-Loader-Rotor-LT-R/dp/B06XB3FLH8)).
  Proof that 12–17 mm fragile spheres can be force-fed jam-free from bulk with
  a torque-limited drive plus sensor gating. Costs ~one printed flexure.

## 14. Count verification sensing in dust and sunlight

- Planter seed sensors are the proven dusty-field break-beam: LED curtain +
  photodetector across the tube, counting 1–135 seeds/s at up to 98 % accuracy
  with auto-sensitivity algorithms that discriminate seed from dust
  ([DICKEY-john Hy Rate Plus](https://dickey-john.com/products/sensors/population-sensors/hy-rate-plus-seed-sensor/);
  [announcement](https://www.farms.com/news/farm-equipment/new-dickey-john-hy-rate-plus-led-seed-sensor-accurately-counts-all-seed-sizes-and-types-80743.aspx);
  [seed counting patent US20110226939A1](https://patents.google.com/patent/US20110226939A1/en)).
- The dust failure mode is documented and specific: "dust can collect within the
  seed tube so as to prevent the sensor from functioning, **but without affecting
  the passage of seeds**" — i.e. the sensor blinds before the mechanism jams, so
  a blinded sensor must be a detectable fault state, not a silent zero
  ([US8631749, seed-tube egress-mounted sensor](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8631749);
  see also [US4950997, diagnostic testing for seed tube sensors](https://patents.google.com/patent/US4950997A/en),
  and a 2025 anti-dust seed-flow sensor design,
  [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2772375525008408)).
  **Design rule: run a beam self-test (emitter off/on) before each dispense and
  report "sensor degraded" as a distinct fault.**
- Through-beam is the right topology for dirt (emitter and receiver separated,
  highest excess gain), with air purge or recessed/shielded optics in the worst
  zones ([Banner Handbook of Photoelectric Sensing](https://info.bannerengineering.com/cs/groups/public/documents/literature/03190.pdf);
  [maintaining photoelectrics in dust](https://www.indmallautomation.com/how-to-maintain-photoelectric-sensors-in-a-dusty-environment/)).
- **Sunlight:** modulated IR (pulsed at a family-specific frequency, receiver
  tuned to it) rejects ambient light — but direct sun on the receiver can
  saturate it and defeat the modulation
  ([ifm technology overview](https://www.ifm.com/us/en/us/overview/photoelectric/technology-overview/tech-overview);
  [Fabrico troubleshooting](https://www.fabrico.io/blog/photoelectric-sensor-troubleshooting/);
  [IR sunlight interference](https://industrialmonitordirect.com/blogs/knowledgebase/ir-sensor-sunlight-interference-troubleshooting)).
  On a belly-mounted drop tube the receiver looks *up* the tube, which is
  naturally shaded — but at 8 m AGL over bright caliche, low sun can enter the
  bottom of the tube. Baffle the tube exit and/or orient the beam axis
  perpendicular to any straight sightline to the sky.
- Our sensing task is trivially easy compared to the planter case: ≤ 10 opaque
  12 mm spheres per command through a ~15 mm tube at ~1/s, versus 135 small
  seeds/s. The engineering effort belongs in fault detection, not resolution.

## 15. Prior art gap

No COTS exact-count meter for tebuthiuron-class pellets was found. Field
application is broadcast (ground spreader, helicopter, and increasingly drone
spinner/venturi spreaders at 3.75–10 lb/acre)
([Azelis on drone-applied tebuthiuron](https://azelisaes-us.com/grow_your_know/revolutionizing-invasive-brush-control);
[Azelis tebuthiuron overview](https://azelisaes-us.com/grow_your_know/tebuthiuron-invasive-brush/);
[Spike 20P](https://diypestcontrol.com/spike-20p-5lb);
[generic 20P](https://www.keystonepestsolutions.com/tebuthiuron-20p-herbicide-25-pounds-pellet-brush-killer-replaces-spike-20p-385)),
and individual-plant treatment is done by hand-thrown pellets. Drone bait
droppers are single-payload or open-gate, not counted. **ASSUMPTION: exact-count
per-plant pellet metering from a drone is genuinely novel**; the nearest flying
precedent is the aerial-ignition PSD family (§0, §5), which singulates but does
not meter a commanded N.

---

## Recommendation (ranked)

**1 — Celled pocket wheel, stepper-indexed, hardened with rotary-valve vane
practice, escapement-style staging, and a break-beam counter.** Concretely:
one disc, pockets bored for 13 mm worst case at 0.8–1.0 × D depth (a second
whole pellet cannot ride); **beveled/relieved pocket lip** and a **compliant
brush or TPU wiper** at the hopper exit so a proud fragment is pushed back into
the hopper before it reaches the close-clearance arc (§1, §2); **roofed/side
entry** so the 295 g pellet column does not preload the shear line (§1, §11);
**compliant agitator fingers on the same shaft** to break arches every index at
zero extra actuators (§11); **through-beam IR counter in the drop tube** with a
pre-dispense self-test (§14); controller indexes until N counted, and on
StallGuard/current stall runs a reverse-oscillate recovery (§13) with counts
edge-triggered from the beam only. One motor, one sensor, positive displacement,
dust-tolerant, doubles geometrically excluded, skips closed-loop recovered.

**2 — Add an escapement/nest as the final release stage** (§5) if drop-timing
repeatability turns out to matter for the 1 m accuracy budget, or if the
pellet-path critic cannot defeat the wedge case with wiper geometry alone. The
PSD nest+spring-steel-flapper (US10871358B2) is the proven airborne pattern:
capture one, retain compliantly, release positively, fully discharge before
selecting the next. Cost: one servo and ~40 mm of height.

**3 — Drum meter** (§4): same physics as 1, worse packaging and worse shear-load
geometry. Fallback only.

**4 — Rejected for exact-N drone use:** auger (§6, volumetric + crushes
pellets), vacuum disc (§7, dust + power), finger/belt meters (§8, complexity for
no gain on spheres), vibratory bowl (§9, unflyable), slat counter (§3, bench
machine). Weigh-count (§10) is kept only as coarse inventory telemetry.

## Open questions this research could not close

1. **Measured single-pellet crush force** for the actual brush bullets — blocks
   the torque-margin claim (§12). Cheap kitchen-scale test proposed.
2. **Measured pellet diameter distribution and out-of-roundness** (parting-line
   flash) — drives pocket and tube clearances; CONTEXT.md's ±1 mm is an
   assumption.
3. **Fragment size distribution after a sortie of vibration** — the PDI-style
   test (§12) applied to a shaker-table sample would define the "largest credible
   fragment" the pocket geometry must reject.
4. No citable source was found for the "outlet ≥ 6–8 × particle diameter"
   interlocking-arch rule (§11); it remains an unverified rule-of-thumb and the
   design should not lean on it quantitatively.
