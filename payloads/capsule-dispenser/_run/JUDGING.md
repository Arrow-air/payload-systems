# JUDGING — Brush Bullet Dispenser Concept Trade Study

Scribe record of the judging round. Three judges scored four champion concepts.
All per-concept arguments below are VERBATIM from the judges' JSON output.
Judge names were not provided in the source data; they are labeled Judge 1–3 in
JSON order. Inferred lens per judge (labeled as inference, not fact):
Judge 1 ≈ count integrity ("exactly N, every time, 5000 cycles in dust"),
Judge 2 ≈ field operations / serviceability ("the Ubaldo test"),
Judge 3 ≈ integration (envelope, power, mass, drop-path geometry).

## Result

| Concept | Judge 1 | Judge 2 | Judge 3 | Total |
|---|---|---|---|---|
| **pocket-wheel (WINNER)** | 73 | 78 | 83 | **234** |
| servo-shuttle | 52 | 68 | 78 | 198 |
| psd-escapement | 70 | 55 | 70 | 195 |
| dual-gate-airlock | 63 | 42 | 58 | 163 |

Winner: **pocket-wheel**, 234 points — first with every judge.

## Dissent and disagreement (scribe notes)

- **Unanimity on the winner:** pocket-wheel ranked #1 on all three ballots —
  no dissent on the outcome, but each judge carried substantive reservations
  (Judge 1: three count-integrity holes; Judge 2: glove-hostile lid, brush wear
  item, fines self-generation, near-empty skip-storms; Judge 3: the angled
  drop chute is "an accuracy liability" and the power-cycle rest state is the
  softest answer to a hard ICD clause).
- **Sharpest disagreement — servo-shuttle:** Judge 1 scored it last (52,
  "the right thing to BUILD first and the wrong thing to FLY"), while Judge 3
  had it second (78, praising the cleanest drop-path of the four alongside
  dual-gate). Judge 2 was in between (68). This 26-point spread made
  servo-shuttle edge psd-escapement for second overall (198 vs 195) despite
  psd-escapement beating it on two of three ballots.
- **psd-escapement split:** Judge 1 rated it a close second (70, best
  count-verification integrity of the four); Judge 2 rated it a distant third
  (55, "a hangar-queen architecture with two great handles bolted on").
- **dual-gate-airlock:** unanimously ranked 3rd–4th; all three judges credited
  its count purity/sensing geometry and honesty while faulting feed
  reliability, jam recovery, ground clearance (~62 mm), and fuse margin.
- **Shared cross-judge theme:** all three ballots flag the unverified ±1 mm
  pellet-diameter ASSUMPTION (CONTEXT.md) as load-bearing — it underwrites
  pocket-wheel's double-exclusion claim and dual-gate-airlock's entire
  20.8–22 mm tube-ID window.

---

## Judge 1 — per-concept arguments (verbatim)

### pocket-wheel — 73

> Best jam-mode profile of the four for the lens: no single-file confinement anywhere, so no unrecoverable pellet path; skips are non-events (re-index) and the reversible stepper gives a real mid-mission back-off-and-retry. But advocates soft-pedaled three count-integrity holes. (1) The 'doubles are geometrically impossible' claim quietly rests on the ±1 mm sphere ASSUMPTION; the doc itself admits a 12x9 mm barrel stack leaves only ~4 mm of brush-wipeable protrusion, degrading the guarantee to 'brush-improbable' — a co-seated double exits as one long/ambiguous dark-time event, and the pellets are gone (overdose detected at best, miscounted at worst). (2) Verification is a SINGLE optical point in dust, and §10.2 concedes the fill interface is a fines generator sitting directly above that sensor — over 5000 cycles the mechanism degrades its own only witness; the self-test fails loud, but a fouled beam is still a mission stop, and a 10–12 mm fragment is counted as a pellet. (3) Phase integrity is open-loop: StallGuard sensorless stall detection is notoriously flaky at low speed with dust-variable friction, and the single rim magnet only re-homes at boot — lost steps mid-sortie can misalign pocket/port with no detection until a pellet hangs or shears. Safe-state under the ICD power-cycle requirement is detent + Hall + convention (three soft things), admitted weaker than B's cam. Net: strongest availability and recovery, middling verification integrity, shape-contingent exactness.

### psd-escapement — 70

> Best count-verification integrity of the four over 5000 dusty cycles: the primary counter is mechanical (flapper-hall, ~0.2–0.4 kgf to trigger — dust cannot fake it and dust cannot blind it), cross-checked against a dark-time-gated beam and cam phase, with the strongest power-cycle story (safe-stop cam window, NV count, at most one ambiguous pellet and it is dual-observed). Structurally one pellet per revolution. Adversarial findings the advocate under-weighted: (1) 'completion-on-repower' is an UNCOMMANDED release path — if power dies pre-discharge mid-rev, the recovery revolution drops a pellet wherever the aircraft happens to be; observed and reported, but delivered off-target. (2) 'Doubles are detected... next command compensates' is soft-pedaling: you cannot recall a pellet; compensating on the next command mis-doses a different plant. (3) The exactness lives in a hand-tuned spring (flapper preload) against an unmeasured, ±1 mm, multi-orientation barrel pellet — the failure is double-sided (too stiff = skips + chipped pellets feeding the fines problem; too soft = vibration doubles from queue pressure), and tuning may chase pellet lots for the life of the product. (4) The S-tube keeps 5–7 pellets permanently in the worst confinement geometry; a mid-tube fragment wedge is undetectable until nest starvation, unclearable in flight (only the nest end is reversible), and its probability integrates over 5000 cycles. Count integrity stays honest through all of this — it fails loud, not silently — but 'exactly N, every time' degrades to 'exactly N or an honest abort'.

### dual-gate-airlock — 63

> Purest per-cycle count guarantee in the portfolio — a static 18 mm interstage that cannot hold two pellets regardless of wear, backlash, or missed steps — plus the best sensing geometry (S1 confirm-staged + S2 confirm-released, two independent observations per pellet, fragment co-release logged rather than counted). If a pellet reaches the gates, this concept miscounts less than anyone. But the lens asks 'exactly N, EVERY time, for 5000 cycles in dust,' and this architecture deliberately routes every pellet through the worst documented dust geometry in the survey: a ~21 mm single-file throat fed directly from bulk (~1.75xD, deep in the interlocking-arch regime), with only probabilistic agitation against it. Persistent rathole = N not delivered — honestly reported, but a failed drop is a failed drop. Worse for mid-mission recovery: gravity cannot be reversed, so a hard-wedged shard anywhere in the 130 mm column is unrecoverable until landing — the only champion with a completely dead-end jam in its primary path. The advocate's own §10.2 is the killer: the entire tube-ID design window is 20.8–22 mm, existing only if the unverified ±1 mm diameter ASSUMPTION holds; ±1.5 mm makes single-file and anti-jam mutually exclusive and voids the concept. Additional soft spots: the upper-gate gap-finding step retries against cocked pellets (0.5 s each, detected but rate-degrading); 1.8 A worst case against a 2 A fuse is ~10% margin with firmware interlocks doing the enforcement, and a blown fuse mid-sortie is mission over. Superb count purity bolted onto the weakest availability and the worst jam recovery.

### servo-shuttle — 52

> Weakest on this lens, and the survey's own scoring agrees (Jam 3, Count 4 — worst of the champions in exactly the domains the lens weighs). The core problem: a linear shear pair with a hard end-stop, in dust, on a 7.5 kgf-class friable pellet, for 5000 cycles. The sliding fit is the most dust-sensitive interface any champion proposes, with no published anchor for printed-slide friction growth in hexazinone fines; the central tuning conflict (30 N compliant-link limit must exceed worst-case dusty friction yet stay 2.5x under crush) means late-sortie fines accumulation manifests as false-jam storms — mission aborts even when the count logic is honest. Soft-pedaled points: (1) the anti-double wiper is the RIGID top-plate underside, not a compliant brush — wiping a protruding second barrel off a friable pellet is a chamfered shear that can crush the rider into exactly the fines and fragments the count system must then discriminate; (2) double-exclusion shares A's unverified shape assumption (a 9 mm barrel on its side under a second is the admitted open double-feed case) but with less wipe compliance; (3) verification is a single optical point, and a jam wedged into the throat chamfer 'may need the glove service' — i.e., no in-flight recovery for its own signature jam; (4) skip-prone fill (dwell-only, no continuous stirring) stretches N=10 to 15–20 s at low hopper, multiplying exposure to every per-cycle failure mode. Power-cycle rest state (exit blanked, stranded pellet delivered next command with NVM ledger) is genuinely decent, and everything fails loud. But 'exactly N, every time, in dust' is precisely the axis this concept trades away for simplicity and mule value — it is the right thing to BUILD first and the wrong thing to FLY.

---

## Judge 2 — per-concept arguments (verbatim)

### pocket-wheel — 78

> Best field-ops package, but not for the reason the advocate leads with. What matters to Ubaldo: ONE motor total (agitator rides the meter shaft — every other concept needs two actuators), a meter that is vibration-indifferent, and dust management that is passive and self-shedding (0.5 mm under-disc gap + fines slot dumps fines every index; no sliding fit, no spring stack to pack). Jam clearing is genuinely tailgate-grade: drop the bottom plate, whole pellet path exposed, brush and disc tool-free-swappable — provided the quarter-turn plate latch the survey demands actually gets designed in; the concept doc itself never commits to it. Adversarial finds the advocate soft-pedaled: (1) 'gasketed screw-on lid' is glove-hostile — threading a gasketed lid in 20 mph wind with dusty gloves cross-threads and drops seals; needs quarter-turn latches like B specifies. (2) The brush wiper is a known dust-packing wear item (the Kinze precedent they cite is precisely why Kinze made it replaceable) — that's a scheduled field maintenance chore, not a solved problem. (3) Its own §10.2 admits the fill interface is a fines GENERATOR — every index drags the pellet bed across the disc, feeding dust into its own sensor over a 250-pellet sortie. (4) Near-empty behavior is skip-storms: the last ~15-20 pellets mean long hovers and an operator who can't distinguish 'empty' from 'bridged' without landing. Still: 160 mm stack (217 mm ground clearance), ~1.05 kg loaded, PETG/ASA with a stepper that barely warms, and the fewest field-adjustable tuning knobs of the four. If the caliper survey kills the double-exclusion geometry it degrades to 'brush-improbable' doubles — an occasional over-dose a rancher tolerates, not a jam. Fails least, clears easiest, needs the least fiddling.

### servo-shuttle — 68

> The survey's Glove 5 is real — everything at the surface, slide pulls out by hand, no tube, no disc stack, and the loading grate (17 mm) is the only concept that designed the gloved-pour-in-wind case at all. It's also the lightest (~0.9 kg loaded) and the honest advocate says plainly it should be built as the mule regardless. But on the survive-dust half of the Ubaldo test it is the WORST of the four, by its own admission: a printed sliding fit with 0.5 mm running clearance is the single most dust-sensitive interface proposed by any champion, in bentonite/urea fines plus ranch dust. The field failure mode isn't dramatic — it's insidious: dust friction creeps up over a sortie toward the 30 N compliant-link limit and the payload starts throwing FALSE jams, which to Ubaldo is a machine that 'randomly quits' and gets parked. The 30 N spring preload is a bench-set tuning knob squeezed between crush margin and dirty-slide friction — the advocate calls this 'the central tuning conflict' and has no data. More soft-pedaling: (1) the hobby servo is consumer-rated ~55 °C ambient, hanging in a belly pod in West Texas sun — the 'upgrade path' is an admission, not a mitigation; (2) the 'one moving part' halo is three (servo + agitator motor + slide), so it is NOT simpler in actuator count than pocket-wheel's one motor; (3) another gasketed screw-on lid — glove-hostile; (4) the DROP microswitch is a dust-exposed mechanical contact in the dirtiest zone of the payload; (5) skip-storms at low fill mean 15-20 s hovers on windy days per its own §11.3. Superb to service when it stops; too likely to stop. If the dusty-slide friction bench test comes back clean, it closes the gap to pocket-wheel; the lens can't award unproven clearances.

### psd-escapement — 55

> Two field-ops gems the others lack, buried under the most field-hostile parts count of the four. The gems: the external knurled thumb-wheel (Rip Drive pattern) lets a gloved operator hand-cycle the whole mechanism with power OFF — the single best jam-clearing affordance in the trade study — and the quarter-turn latched lid is the only glove-correct refill closure specified by anyone. The safe-stop cam is also mechanism, not firmware. But the Ubaldo test fails on the middle of the machine: (1) The S-tube is, per its own §9.3, 'the worst-in-survey glove-serviceability item even WITH the hinged cover' — clearing a wedged fragment from a 110 mm run of 20 mm tube with gloved fingers at a tailgate means a poke stick and profanity, and a mid-tube wedge is undetectable until the nest starves. (2) The set-screw-adjustable flapper preload is a field tuning knob with failure modes on BOTH sides (too stiff = skips and chipped pellets, too soft = doubles under vibration), and the advocate concedes tuning 'may chase pellet-lot variance' — a mechanism that needs re-tuning per pellet batch is a mechanism ranch crews will mis-tune or abandon. (3) Heaviest (1.16 kg loaded, ~860 g empty), most parts, two motors, a cam, a crank, a formed spring — every one a thing that heat, dust, and vibration get a vote on. (4) The 'flight-proven' pedigree is for hard injection-molded spheres; the advocate admits USFS jam literature says even those jam PSDs constantly in the field, and our pellet is worse. (5) Ground clearance for the ~195 mm stack was never derived — flagged as layout-blocking, i.e., the packaging story is unfinished. Wins only if pellet shape variance kills the rigid-pocket concepts; on its own field merits it's a hangar-queen architecture with two great handles bolted on.

### dual-gate-airlock — 42

> The purest count guarantee and the best sensing geometry — and nearly everything the field-ops lens cares about cuts against it. (1) Ground clearance: ~62 mm at rest BEFORE foam compression, the tightest of the four by a factor of ~2.5-3.5, hanging as the tallest, thinnest structure (~315 mm) under the belly. West Texas ranch landing zones are caliche, rock, grass clumps, and mesquite stubble — the drop chute and sensor housings at the bottom of that snout are the first casualty of one firm landing, and the advocate defers the foam-compression check. Ground handling and truck transport snag it too. (2) Feed reliability: it deliberately routes bulk pellets into a 21 mm single-file throat — 'the worst documented dust/bridging geometry in the survey' per its own §10.1 — and mitigates with a second motor whose agitation is 'probabilistic, not geometric.' In the field that reads as routine starvation faults: the drone comes home having skipped targets, and Ubaldo learns to distrust it. (3) Jam clearing: gravity cannot be reversed; a wedged shard mid-column is unrecoverable in flight and the tailgate fix is fishing fragments out of a 130 mm × 21 mm tube through a hinged face with gloved hands — worse than it sounds and the advocate knows it. (4) Simplicity is a mirage: the advocate's own §10.6 admits four coupled tuning parameters (rocker overlap, wedge-nose angle, blade force limit, interstage height) against an unmeasured irregular pellet, plus a serial-bus servo, a torsion spring, an agitator motor, and firmware current limits — versus one disc and one brush. (5) The entire architecture stands on a ~1 mm-wide tube-ID design window (20.8-22 mm) resting on the unverified ±1 mm diameter ASSUMPTION; if calipers say ±1.5 mm, single-file and anti-jam become mutually exclusive and the concept collapses into pocket-wheel with extra steps. Credit for the most honest self-assessment of the four and for the sealed hinged lid (glove-correct); but this is a lab instrument's answer to a ranch problem.

---

## Judge 3 — per-concept arguments (verbatim)

### pocket-wheel — 83

> Best integration package overall, with one soft-pedaled accuracy flaw. Envelope: 160 mm stack gives ~217 mm derived ground clearance (I verified the derivation: ground plane Z=-547.9, 376.9 mm available) and correct lateral math (leg-top radial 174 mm vs hopper r=72) — most comfortable envelope of the four. Power: best margin by far, <=0.8 A worst-case on the 2 A 12VSW fuse (2.5x), with the stepper driver current limit as hardware enforcement; clean 12V_PL/12VSW split per ICD. Mass ledger: most complete of the four — explicit 15% contingency, shown volume derivations (clip plate 71 g solid-alu check is correct), 1.045 kg loaded at 250; realistic. Dings: (1) DROP-PATH: the chute that 'angles the drop line back to the airframe centerline' is advocated as an accuracy feature but is an accuracy liability — a ~17 deg guided exit at ~1.4 m/s imparts up to ~0.4 m/s lateral velocity, i.e. up to ~0.5 m of displacement plus bounce scatter over the 1.28 s fall from 8 m, against a 1 m budget, to fix a 30 mm offset that is negligible if dropped straight. Unmodeled and mis-sold. (2) Misreads the CONTEXT mass rule as applying to empty mass ('under 1.0 kg empty, no justification') when the 1.0 kg threshold reads against the 250-load total (1.045 kg) — immaterial in grams, sloppy in compliance. (3) Weakest power-cycle rest state (detent+re-home firmware convention vs ICD's explicit cycling requirement) — admitted, but it is the softest answer of the four to a hard ICD clause. (4) NEMA-14 mass (120 g, heaviest single item) and stepper draw are catalog-class assumptions, not selections.

### servo-shuttle — 78

> Light, flat, and geometrically clean, but the ledger's realism claim is unauditable and the clip/power treatments are thin. Envelope: 215 mm stack -> ~162 mm clearance (derivation correct; I verified legs at X~185 at Z=-300 and Y inner clearance 108 mm vs 70 mm half-width) — comfortable. Drop path: the cleanest of the four alongside dual-gate — pellet falls vertically from the cavity through a straight 20 mm chute at ~40 mm from port center; no angled surfaces adding lateral velocity; beam placed after the last mechanical element, which is the right definition of released count. Mass: lightest loaded (899 g at 250), and the servo (62 g) and clip-plate numbers check out — but '~40% contingency already embedded in [A] lines' is an assertion, not a ledger line; it is the only concept with neither an explicit contingency row nor an external cross-check (PSD has IGNIS, pocket-wheel has volume math), so its headline lightness is the least defended number in the run. Power: 1.6 A worst coincident on the 2 A fuse (~20% margin) is acceptable and, credibly, enforced by the buck's 2.5 A hardware current limit rather than firmware hope — better engineering than dual-gate's identical-looking number — but the no-stacking claim depends on a firmware interlock between servo stall recovery and agitator. Clip-plate loads get one rough-moments sentence (CG <10 mm, 'verify in CAD') with no moment or dynamic-factor estimate — thinnest structural treatment of the four. Integration-relevant residual honestly carried: skip-retry stretches hover time (15-20 s at N=10 low-hopper), which spends the accuracy budget in wind exposure rather than geometry.

### psd-escapement — 70

> Structurally the most careful mounting story, undermined by skipping the one envelope derivation my lens is about. Clip-plate loads: best of the four — actual static moment computed (1.2 N.m, 3x under maneuver), the quick-release's poor unlatched-direction moment capacity flagged, and the missing per-port rating logged as an ICD gap; no other concept did this. Mass: heaviest (860 g empty w/ contingency, 1.16 kg at 250), but the only ledger with an external anchor (IGNIS 1.25 kg empty WITH injection hardware makes 860 g without it consistent, not optimistic) and the only concept that actually performed the CONTEXT-required >1.0 kg justification correctly (160 g itemized against the safe-stop cam and sealed lid). Power: 1.6 A worst on the fuse, honest current limits, clean kill-path split — fine. The failure: ground clearance for the ~195 mm stack was left underived — an explicit CONTEXT violation ('DERIVE ground clearance... and record the number') on the layout-blocking item, in a run where three other advocates did the derivation from the same file. My own derivation says it passes comfortably (~182 mm), so the physics is benign but the process miss is real and it means the '[A] Height risk flagged' hedge (offering an S-to-C re-route) is solving a problem it never bothered to size. Secondary dings: the claimed <10 mm loaded CG offset is marginal — ~275 g of S-tube/cam/gearmotor hangs on one side of the spine, which back-of-envelopes to ~12 mm at 1.16 kg, against their own warning that the clip carries moment poorly; and at best-case full load (1.40 kg) it is the only concept crowding the 1.5 kg ceiling, buying rate capability (120/min heritage) the 1 Hz mission never uses — mass spent on a non-requirement.

### dual-gate-airlock — 58

> The best-documented envelope math in the run arrives at the worst envelope, and the power story is the only one that can plausibly blow the fuse. Ground clearance: derivation is correct (I verified: 315 mm stack -> Z -486 -> 61.9 mm at rest; lateral 242/108 mm inner clearances also check out) — but 62 mm BEFORE foam compression, on West Texas ranch fields with stubble, rocks, and non-flat touchdowns, is marginal-to-unacceptable for a fielded product; the 40 mm-OD foam sleeves compressing even 10-15 mm under a firm landing plus any grass eats most of it, and a chute ground-strike acts on the clip plate through a 315 mm lever arm — the worst clip-plate load case of any concept, dismissed in one deferred sentence ('dynamic factor check deferred'). The advocate flags the clearance honestly but then freezes a 130 mm column anyway; the mitigation (shorten the column) attacks the concept's own buffer-depth rationale. Power: worst of the four — 1.8 A worst honest case on a 2 A fuse (10% margin) where the servo cap is FIRMWARE-only; an uncapped STS3215 stall (~2.7 A @6 V -> ~1.6 A @12 V through the buck) plus the 0.5 A agitator is ~2.1 A, over the fuse, so a single firmware fault mode converts a jam into a blown F1 and a dead 12VSW for the sortie. The 'stagger in firmware' mitigation is a scheduling promise, not a circuit. Mass: lightest empty (600 g) but the only ledger carrying NO contingency line despite self-declaring +/-30% at sketch level — at +30% it is ~780 g empty, still compliant, so the omission is presentational optimism rather than a ceiling risk. Credits: drop-path geometry is the best of the four (static vertical column and straight chute within 15 mm of plate center, zero lateral velocity imparted; S2 after release), and every geometric claim it makes survived independent check — this concept loses on physical margins, not on honesty or math.

---

## Cross-cutting action items surfaced by the judges

1. Caliper survey of actual pellet lots — the ±1 mm diameter ASSUMPTION is
   load-bearing for pocket-wheel's double-exclusion claim (flagged by Judges 1
   and 2; also what voids dual-gate-airlock).
2. Pocket-wheel drop chute: judge 3 argues the angled chute should be dropped
   for a straight vertical exit; model in sim before freezing geometry.
3. Power-cycle safe-state: pocket-wheel's detent+Hall+firmware-convention
   answer to the ICD power-cycling clause is the weakest of the four — needs
   hardening (flagged by Judges 1 and 3).
4. Replace the gasketed screw-on lid with quarter-turn latches (Judge 2), and
   commit to the tool-free quarter-turn bottom-plate latch the survey demands.
5. Dust protection for the single optical count sensor beneath a
   fines-generating fill interface (Judges 1 and 2); consider a second sensing
   modality.
6. StallGuard low-speed reliability and mid-sortie re-homing (single boot-time
   rim magnet is insufficient per Judge 1).
