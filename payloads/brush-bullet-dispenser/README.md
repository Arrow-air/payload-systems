# Brush Bullet Dispenser

**Status:** design — **rev-1 CAD close-out, export tag `r12`, NOT cleared to print.** Two of the three rev-0 CAD blockers (RT-2's bay implication, RT-3's count hardware) are closed in geometry and reproduce under independent re-measurement. **RT-1 is not**: a fresh-eyes verifier, and then the packager, both measured a **0.200 mm closed web** across the disc's grub-screw pilot, so the disc still cannot be clamped to the motor shaft. **A dedicated close-out run (2026-08-08) failed to clear this: both fix rounds produced nothing (no `r13` exports, no source changes), so `r12` remains the shipped tag, the 0.200 mm web is still in the shipped disc (re-measured at pack time: 1.0619 mm³ of material in the Ø2.6 corridor to r = 2.55), the BOM corrections remain regeneration-fragile hand-patches, and the ground/prop clearance numbers remain unverified.** See [Open blockers](#open-blockers-read-before-building); full evidence in [`_run/rev1/VERIFY.md`](_run/rev1/VERIFY.md), [`_run/rev1/CLOSEOUT-VERIFY-r2.md`](_run/rev1/CLOSEOUT-VERIFY-r2.md) and the round-by-round record in [`_run/rev1/RUN-RESULT.md`](_run/rev1/RUN-RESULT.md).
**Target port(s):** bottom (J31 — the only port with 12VSW)
**ICD version:** 1.0
**Champion:** thomasg
**Discussion:** —

![Isometric view of the rev-1 r12 dispenser](cad/renders/v1r6_iso.png)

## What it does

Carries herbicide brush-bullet pellets (Ø12 mm, 1.18 g, tebuthiuron/Spike-20P
class) under a Quiver and drops a commanded number of them — N ∈ 1..10, usually
1–3 — onto individual target plants during targeted brush control on West Texas
rangeland. Targets arrive as coordinates from an orthophoto/scouting pipeline;
the aircraft hovers at ~8 m AGL, commands `Dispense(seq, N)` over DroneCAN, and
the payload returns a **sensed** count of how many pellets actually left the
chute. Metering is a stepper-indexed 8-pocket disc: one pocket holds exactly one
pellet, so the count is bounded by geometry rather than by control, and an IR
through-beam in the exit chute closes the loop.

## Requirements

Requirements are captured in [`_run/CONTEXT.md`](_run/CONTEXT.md) (Thomas,
2026-08-06, verbatim directives). Headline compliance:

| | |
|---|---|
| Mass | **rev-1 r12:** **1.43 kg** loaded at the 250-granule baseline on the shipped slicer-realistic basis (4 perimeters + 25 % infill), margin +68 g; **1.49 kg** with the 61 g per-open-item reserve. The 100 %-infill pessimistic bound is 1.58 kg. Dry (empty, carried) **1.28 kg**. The rev-0 1.39/1.09 kg figures are superseded |
| Power | **4.05 W peak / 0.34 A** — 3.57 W (0.298 A) from 12VSW while indexing, 0.48 W (0.040 A) from 12V_PL. Steady state, motor parked and count sensor watching: **0.40 W / 0.033 A** |
| Data | CAN2 (DroneCAN) — command + verified count. FMU_CH1 PWM — arm/disarm only. Ethernet **not used** |
| Port | bottom (J31) |
| Envelope | **rev-1 r12:** 156 × 170 mm in plan, **247.4 mm** below the mounting plane (assembly bottom Z = −418.45 against the −171.0 mount plane; the B6 stand-off neck adds ~52 mm) — **independently re-measured**. Aircraft clearances are **carried from the build notes and NOT independently reproduced**: **129.4 mm** ground clearance at rest, **103.63 mm** mesh-to-mesh to the landing gear, **152.55 mm** vertical / **232.63 mm** in-plan to the propulsion assembly. The verifier could not re-run them because the referenced airframe STEPs were not present at the cited path, and the stack moved down ~52 mm this rev — **re-check these against the real gear before flight**. The rev-0 195.4/181.5/251.1 figures are superseded |

| Requirement (CONTEXT) | Target | Achieved | Verdict |
|---|---|---|---|
| Capacity | ≥250 pellets, more is better | 962 cm³ usable → **421** at worst-case barrel packing (586 on a sphere basis), per `cad/BOM.md` at r12 — this README previously said 963 → 422 and has been aligned to the generated BOM | **PASS**, 1.68× — but see RT-5 below: the fill ribs are calibrated on a 40 % packing constant, so the "250" rib really holds ≈370 nominal pellets |
| Mass | ≤1.5 kg at the 250-pellet load | **rev-1 r12: 1432.5 g** on the shipped basis (4 perimeters at 0.4 mm + 25 % infill, padded EDT), **1493.5 g** with the 61 g per-open-item reserve; **1576.0 g** on the 100 %-infill pessimistic bound; dry 1281.0 g | **PASS on the shipped basis**, +68 g (+7 g with reserve). The per-part volumes behind the ledger were re-measured off the `r12` exports by an independent verifier and reproduce to **≤ 0.04 %** on every part. Stated, not hidden: the 100 %-infill bound is 76 g **over**, and 150.4 g of the empty subtotal is estimate rather than measured geometry (the 350 g stepper is a vendor catalogue figure that has never been on a scale — `cad/BOM.md` used to contradict the ledger here by 40 g and was corrected at packaging) |
| Count | exactly N, **verified (sensed)** | two staggered IR chord beams, 9.7–25 ms dark-time gate | **HARDWARE NOW IN THE CAD (rev-1 r10)** — 4 × Ø3.2 apertures at x = 29/35, z = −392.250/−398.250 (6.000 mm ECO-9 stagger), ECO-5 labyrinth, 4 × ECO-4 bore-face PMMA windows, bolted covers and both sensor boards, with the ordered TSAL6200 fitting at its datasheet 8.7 ± 0.3 mm height. The **claim** still waits on bench test B1 (dark-time survey). See RT-3 |
| Accuracy | within 1 m from ~8 m AGL | ballistics say the payload is not the driver — 0.09 m drift per m/s of wind; hover hold is | **UNOWNED** — no sim was delivered. See RT-4/G1 |
| Fragment jam (2026-08-06 directive) | reject before wedge; shear as backstop; detect + recover | **Re-measured on `r12`.** Entry ramp **17.83–36.12°** depending on radius (25.05° at the PCD); the model measures the nose covering **r 20.0–46.7 at 1.500 mm** and roof clearance **1.500 mm**, i.e. max(nose gap) = min(roof clearance), so **there is no blind band** (the round-5 critic probed the same solids independently on `r11` — which is byte-identical here — and read 1.500 mm at r = 20.5…47.0 and at 132 roof probes); bristle tip **1.200 mm**, i.e. the compliant element leads for every proud object below 5 mm; swept-sphere first contact has **n_z ≤ 0** for Ø5/6/7/9 fragments — the nose stubs, it never lifts. Crush at the measured section: **Ø5 → 7.07 N, Ø6 → 10.18 N, Ø7 → 13.85 N** vs 12.2 N metering / 20.4 N recovery (Ø6 = **2.00× / 1.20×**). Worst escaping fragment **Ø4.740** (round-5 critic, derived on `r11`; `pocket_disc` and `brush_holder` are md5-identical in `r12`), and it fits the exit port with +0.101 mm. Hall phase decode + bounded reverse-oscillate; guaranteed reverse free travel at the worst park (247.5°) is **12.50° at the PCD** for anything ≤5 mm proud and **2.75° at the PCD / 2.50° at r = 24.5**, of which the package publishes the conservative **2.25°** for a stacked whole granule | **MET IN GEOMETRY, bounded by test.** The 1.5–3.0 mm band and the 7.5 N / 2.7× figures were rev-0 numbers that the docs kept publishing for three rounds after the geometry changed — corrected here (rev-1 r6). **Where it runs out is now published too:** a 180° conforming shard in the worst self-locking crescent needs ≈19.3 N (1.06× recovery, 0.63× normal) and a full-ring crescent ≈38.5 N → **the drive stalls**, which is the intended failure mode (a whole granule needs 41 N and must never be milled). σ = 0.36 MPa and µ = 0.4 are **carried assumptions**; closure is bench test IFDC S-115 |
| Power ceiling | 2 A fuse on 12VSW | 0.298 A worst case, and a chopper's input current *falls* at stall | **PASS**, 6.7× |
| Scope | no software phase, no regulatory workstream | interface contract only (DSDL + semantics + timing) | honored |

## Open blockers (read before building)

This package is published with its critics' and verifiers' own findings
attached, not laundered. The rev-0 package shipped at rev-0 design maturity with
three red-team blockers declared unmet; the rev-1 run (six rounds, export tags
`r7`…`r12`) was scoped to close them in CAD. This section is the declaration of
where that landed.

### Independent verification of the final round (2026-08-08, `_run/rev1/VERIFY.md`)

A fresh-eyes verifier who had seen none of the build rounds re-measured the
`r12` exports with its own tools (OCC booleans on the STEP files, trimesh on the
STLs, never reading `dispenser.py` or the project's own checkers). **Most of the
package survived**: B1 (roof slot), B3 (bolt geometry), B4 (count sensor), B6
(reach-in), B8 (rejection band), B10 (export integrity) and B11 (mass ledger)
all reproduce independently, B4 and B6 to the third decimal. **Three things did
not**, and one of them is a hard blocker:

1. **BLOCKING — the disc still cannot be clamped to the shaft (RT-1 is not
   closed).** The grub-screw pilot dead-ends at r = 2.750 against a shaft flat
   at r = 2.550, leaving a **0.200 mm closed web of CF-PETG across the full
   Ø2.6 section**. The packager reproduced all five of the verifier's booleans
   on `pocket_disc_r12.step` exactly: Ø0.7 corridor to the flat **0.0770 mm³**,
   Ø1.9 **0.5671 mm³**, Ø2.6 **1.0619 mm³** (= π·1.30²·0.200, a full-section
   web); the same probes stopped at r = 2.75 read **0.0000**. Everything else in
   the torque path is real — D-flat r 2.550/3.050 over a 56° arc with 13.5 mm of
   axial engagement, Ø26 bolt circle on the axes with a 3.200 mm web, driver
   access 0.0000 mm³ against all seven surrounding parts — so this is a 0.2 mm
   miss, not a missing feature. **Why it was signed off six times:** round 6's
   own checker prints *"blocked at r = NOWHERE — continuous void"* and the
   round-6 assembly critic reported *"a continuous grub corridor from the disc
   OD to the shaft"*, because both start their ray at the **round** bore radius
   (3.05) or the pilot floor, both of which are outboard of the flat at 2.55.
   The probe is structurally blind to the defect it is asked to find — the same
   can't-fail-probe class as RT-19/RT-20. **Fix: deepen the pilot 0.2 mm to
   break into the bore, and re-anchor the checker ray at the flat radius.**
   Until then, do not print the disc.
2. **BOM defects, now corrected at packaging (see the `[CORRECTED 2026-08-08]`
   rows in `cad/BOM.md`).** The PTFE thrust washer was ordered **Ø30/Ø24 × 1.5**
   against a modelled solid of **Ø38/Ø34 × 1.4** — the ordered ID/OD sits on top
   of the four Ø3.4 gearbox bolt holes; the gearbox **pilot bore Ø16.20** that
   punch-list B3.4 requires the BOM to state was stated nowhere; the count
   windows are modelled **Ø5.90 × 0.95** while BOM and ECO-4 both said Ø6 × 1.0;
   and the BOM disagreed with the mass ledger on the stepper by **40 g**. All
   four are description strings, all four are fixed in `cad/BOM.md` — but
   `dispenser.py` still emits the old ones, so **the next BOM regeneration will
   re-introduce all four** unless the source tables are fixed first.
3. **Four "passes" that pass with zero margin and should be read as such:**
   sensor-boss to motor-body clearance **4.000 mm** against a ≥ 4.0 mm
   requirement (the punch list assumed 4.4 mm because it put the motor face at
   x = 17.6; the model has it at 18.0), bearing seat **Ø23.030** against
   ≤ Ø23.03, hopper insert bore depth **5.99 mm** against ≥ 6.00, and nose gap
   **1.500 mm** exactly equal to roof clearance **1.500 mm**.

The verifier also lists what it **could not** check, so nobody counts it as
checked: the harness five-volume boolean and channel-coverage numbers (B5.4/
B5.5 — they can only be reproduced inside the model), the bay gasket groove
(B5.3, below its scan resolution), the QR actuation envelope (B6.3), **ground
and prop clearance** (B6.5/B6.6 — the airframe STEPs were not at the referenced
path), the B7 release sweep, and every non-blocking item. And it found one
authoring defect in the punch list itself: B1.1's "≥ 6.0 mm of roof outside
θ = 96…131" contradicts the designed 120° sump outlet that the same document
describes in N10, so any checker written literally from B1.1 reports a permanent
false failure.

> **rev-1 update (2026-08-08, export tag `r12`, round 6).** Round 6 closed the
> two blocking findings round 5's critics raised, both by geometry, plus four
> non-blocking ones. Every number is quoted from tool output in
> `_run/rev1/BUILD-NOTES-r6.md` and independently reproduced by
> `cad/verify_r6.py`, which reads only the exports and the BOM:
>
> - **The cartridge harness duct (bay → motor, bay → both count boards) was
>   solid printed material** — r11 measured every leg 100 % solid on its axis,
>   largest conductor Ø0.0, and the part contained zero enclosed voids. Root
>   cause: the bore cylinders were fused before subtraction, and a fuse of
>   equal-radius perpendicular cylinders is topologically invalid, so OCC
>   answered the cut with an empty result and **no error**. r12: **0 of 1757
>   axis points inside material**, a **Ø4.0 mm bundle sweeps all 15 legs at
>   0.0000 mm³**, and the cut removed **8025.3368 mm³ = 10.19 g**.
> - **The M5 detent plunger had nothing to thread into** (a plain Ø5.199/Ø6.399
>   bore, and no M5 insert was ordered anywhere in the BOM, while the detent
>   carries 96.5 of the 190.7 mN·m reaction budget). r12: a modelled **Ø4.5 ×
>   13.5 mm thread-forming pilot**, measured on the export as a section that
>   steps 5.100 → 4.400 outward, insertion sweep **0.0000 mm³**.
> - **The bay screws overshot their pilot and the pilot was open into the
>   metering chamber** (27.7 % of its section, 0.144 mm of floor elsewhere).
>   r12: floor moved out, screw M3×20 → **M3×18**, pilot **0.0 % open** —
>   with r11's floor re-run as a control that comes back 33.9 % open, so the
>   probe is provably able to fail.
> - **The granule bed was open to the sky** through two 2.2 × 5.0 mm cable-tie
>   slots (22.00 mm², inside the tank) that a 12-column self-check had missed
>   for nine rounds, and — found by the 60 669-ray grid scan that replaced it —
>   through the **fill cap's lanyard hole**, which went straight through the
>   2.5 mm cap flange. Both closed: **0.00 mm² unroofed inside the fill-cap
>   seal**.
> - **Count-beam clearance** on the ECO-3 axes is now 0.0000 mm³ (r11 read
>   1.1932 mm³ because the ECO-5 labyrinth stepped the same way on both sides);
>   the BOM now carries **two** driver rows (1.5 mm for the M3 grub, 2.0 mm for
>   the countersunk gearbox screws) and orders the grommets, bay gasket cord
>   and sensor pads that three rounds had modelled seats for and never bought.
> - **Exports**: 15/15 part STLs watertight, 0 non-manifold edges, assembly 24
>   bodies / 0 open edges.
>
> **Still open after round 6** — see `_run/rev1/BUILD-NOTES-r6.md` §9: **B7**
> (release happens **3.25–10.50°** into the 22.5° index, not from a stationary
> pocket — a recorded plateau, not a closure), **N10** (sump opening
> **2.076 × D_max**),
> **N19** (external-finish α vs CF-PETG), the ECO-4 window-seat chamfer
> (attempted and withdrawn: it breaks the watertight export), the 1.262 mm
> residual under the bay-screw pilot floor, and every bench test in the plan.
>
> **rev-1 update (2026-08-07, export tag `r11`, round 5).** Round 5 closed the
> three findings round 4's critics raised, all by geometry or by BOM, and every
> number is quoted from the tool output in `_run/rev1/BUILD-NOTES-r5.md`:
> the **aircraft-harness conduit was solid at the top-plate elbow** (r10:
> largest conductor that could cross it = Ø0.0) and is now open end to end with
> an R8 swept corner — a Ø5.5 bundle sweeps the whole route at **0.0000 mm³**
> and coverage is **94.6 %** measured on the meshes, not rolled up from
> parameters; the **gearbox screws** are now specified as M3×8 ISO 10642 /
> DIN 7991 countersunk to match the seat the plate has always had (the ordered
> cap head measured 197.6 mm³ of interference with the metering disc over one
> spoke pitch); and the **plug-tether lug** no longer stands 1.000 mm inside the
> drop tube (bore r_min ≥ 10.993 mm at every height, and plate ∩ plug is now
> 83.5035 mm³ — the designed press fit and nothing else).
>
> **rev-1 history (export tag `r10`, round 4).** The rev-1 run has
> been working this list. ~~**RT-1 and RT-3 are closed in geometry**~~ **RT-3 is
> closed in geometry; the RT-1 half of this claim was wrong and is retracted —
> see the verification block above.** What round 4 did close, and what still
> holds: D-flat torque path, Ø26 bolt circle, the θ = 310° roof slot, and the
> whole ECO-3/4/5/9/12 count-sensor stack — see the rows below and
> `_run/rev1/BUILD-NOTES-r4.md`, which quotes the tool output for each. What it
> did not close, and reported as closed: the grub corridor.
> **RT-2 is out of scope by direction** (Thomas, 2026-08-07: the attachment
> interface mates electrically; treat it as a black box) — what survived of it
> is the sealed electronics bay, which is built. Still open and honestly
> unclosed: **B7** (the granule is released 3.25–10.50° into the index, not
> from a stationary pocket — geometric closure needs an architecture change),
> the sump-aperture ratio (**N10**, 2.08 × D_max), external-finish α
> (**N19**), and every bench test in the plan. The numbers in the rev-0 table
> below are rev-0 numbers and are **not** re-measured against `r10` except
> where a row says otherwise.

| # | Blocker | Measured | Owner |
|---|---|---|---|
| **RT-1** | **STILL OPEN after rev-1 — 3 of 4 legs closed, one short by 0.200 mm.** Closed and independently reproduced on `r12`: the D-flat exists (r 2.550 flat / 3.050 round, 56° contiguous arc, 13.5 mm of axial engagement, grub axis at θ = 202.5° = the flat's mid-angle), the gearbox holes are on the datasheet's Ø26 bolt circle at θ = 0/90/180/270 (Ø3.40 through a 4.000 mm flange, minimum web 3.200 mm), and the θ = 310° roof through-slot is gone (9.000 mm of roof at all 8 radii × 16 angles, largest travel-opposing roof face 1.98 mm² against a 20 mm² threshold, down from 238 mm²). **Not closed: the grub corridor is interrupted by a 0.200 mm web** — see the verification block above. The original rev-0 finding, for the record: | pocket_disc_r12.step (0.0770 / 0.5671 / 1.0619 mm³, packager-reproduced); rev-0: pocket_disc_r6.stl, retaining_plate_chute_r6.stl, meter_housing_r6.stl | round 7 CAD |
| **RT-1 (rev-0 text)** | **The mechanism cannot be assembled or driven as drawn.** Three independent geometry defects: the pocket-disc bore is a plain Ø6.12 round hole (r = 3.06 mm at all 24 probe angles) with **no D-flat**, so the gearbox D-cut transmits nothing and the grub screw is a buried blind hole with no path to the rim; the gearbox mounting holes are on a 26 mm **square** (r 16.8–19.9 on the diagonals) instead of the datasheet's Ø26 **bolt circle** (r = 13 on the axes); and the r6 entry-ramp cut was made with a half-space, mirroring a 25° undercut at θ = 310° and opening a **0.00 mm-thick through-slot** from the pellet bed into the metering arc downstream of every rejection feature | pocket_disc_r6.stl, retaining_plate_chute_r6.stl, meter_housing_r6.stl | round 7 CAD |
| **RT-2** | **There is no electrical connection to the aircraft.** Payload blind-mate pads sit at Z = −181.5 mm; the drone-side spring-pin tips are at Z = −162.15 mm → a **19.35 mm axial gap** against ≤2 mm of plunger travel. Even at the highest legal pad plane (−171.0) it is 8.85 mm. 10.5 mm of the gap is payload-controllable; the residual is aircraft/ICD-side and is **not closable in CAD**. Nothing downstream of it — count contract, power budget, DroneCAN — is real until a pin touches a pad | vendored 2112/3331 STEPs vs `dispenser_r6_assembly.step` | **escalate to the ICD owner** |
| **RT-3** | **CLOSED IN GEOMETRY (rev-1 r10).** ECO-3/ECO-9/ECO-4/ECO-5/ECO-12 are merged and measured on the export: 4 tunnels (2/side) at x = 29.000/35.000, z = −392.250/−398.250 → 6.000 mm stagger; labyrinth offset 0.800 mm; window faces at \|y\| = 11.000 with 0.000 mm³ proud of the bore; the datasheet TSAL6200 (8.7 ± 0.3 mm, Vishay 81010 rev 2.4) booleans to 0.0000 mm³ against plate and cover at its 9.0 mm max-material height. BOM lists VBPW34FAS ×2 / OPA2320 / TSAL6200 ×2 / 4 × PMMA windows and **no** TSSP4038 | `retaining_plate_chute_r10.step`, `cad/verify_r4.py` §2 | done; bench test B1 still gates the *claim* |

Two further findings are called out here because they change what an operator
may do, not just what a builder must fix:

- **RT-5 — fill by mass, not by rib.** `PELLET_VOL_WORST = 2.28 mL/pellet`
  implies ~40 % packing; real spheres pack at ~0.60 random-loose. Filling to the
  "250" rib with nominal pellets gives **≈370 pellets / 438 g → ≈1530 g all-up**,
  *over* the 1.5 kg ceiling. Until the ribs are re-cut, **fill to 295 g on a
  scale**, not to a line inside an opaque black hopper. There is also no
  inventory telemetry at all — `lifetime_count` only, no `pellets_remaining`, no
  `Fill` service — so an empty hopper is discovered at a target, after that
  plant got a partial dose.
- **RT-6 — the black hopper is a thermal problem.** Parked-in-sun wall
  temperature computes to 77.5 °C against CF-PETG's 80 °C Tg, and the pellet
  binder softens in the same band. The BOM's carbon-filled (black) material
  directly contradicts ECO-1's α ≤ 0.4 finish requirement. Every structural
  check in the package is implicitly at room temperature.

The full 21-finding red team is in [`_run/RED-TEAM.md`](_run/RED-TEAM.md); the
7-gap coverage review is in [`_run/GAP-REVIEW.md`](_run/GAP-REVIEW.md); both are
folded into the risk register in [`docs/DESIGN.md`](docs/DESIGN.md) §7.

## Folder layout

- [`README.md`](README.md) — this file.
- [`docs/DESIGN.md`](docs/DESIGN.md) — the design story end to end: mechanism
  survey → trade study → six CAD rounds → electronics and interface contract →
  the sim that was not delivered → risk register.
- [`cad/`](cad/) — parametric build123d source (`dispenser.py`, 6086 lines),
  independent export checkers (`verify_r6.py` is the current one; `verify_exports.py`, `verify_r2/r4/r5.py` are the earlier rounds'), auto-generated
  [`BOM.md`](cad/BOM.md), `exports/` (STEP + STL, per-part and assembly, rev-0 rounds
  1–6 and rev-1 rounds r7–r12) and `renders/` (69 PNGs). Mating geometry and drone coordinates:
  [`interface/mechanical/`](../../interface/mechanical/).
- [`electronics/`](electronics/) — [`ELECTRONICS.md`](electronics/ELECTRONICS.md):
  power tree, actuator drive, count sensing, the DroneCAN command contract, BOM
  with prices, ECOs and the bench-test plan. **Design document only — no KiCad
  yet.** The blind-mate board is the pads-only Attachment Interface PCB, see
  [`interface/pcb/`](../../interface/pcb/).
- `sim/` — **not delivered.** See `docs/DESIGN.md` §6.
- `software/` — out of scope by direction (CONTEXT: *"NO software phase — that
  can be a whole project on its own"*). The electrical/command **contract** it
  would implement is specified in `electronics/ELECTRONICS.md` §5.
- [`_run/`](_run/) — run docs: research, concepts, judging, six rounds of build
  notes with verbatim critic output, red team, gap review. Not part of the
  shipped design; kept because the numbers in this README are traceable to it.

## Compliance

Against the ICD §8 checklist:

| Item | Status |
|---|---|
| Port capability | bottom port only — needs 12VSW, which no side port has |
| Mechanical mate | 4 × M2 SHCS at (±19, ±19) into the COTS 2112 payload-side clip plate. ~~The BOM's M2×10 gives only 0.90 mm of thread engagement~~ — **corrected rev-1 r11:** the mount was reworked in round 1 and re-measured every round since; grip is **6.500 mm** and an M2×10 puts **3.500 mm** of thread into a 4.0 mm RX-M2×4 insert (87.5 %), against the ≥3.2 mm the punch list asks. The rev-0 0.90 mm figure is superseded |
| Envelope | within the 50 × 50 footprint above the plate face except the fill-cap wing bar (584 mm³, clears the drone-side plate underside by 7.35 mm); **0 vertices and 0.000 mm³ of payload above Z = −171.000** on `r12` (independently confirmed; r6 had 0.0397 mm³) |
| Interface reach-in (directive 3) | **PASS, independently reproduced.** Stand-off neck **h = 43.500 mm** (plan half-extent a constant **24.000 mm** from Z = −181.55 down to −225.05, where the body flares to 84–85.5 mm) — a 48 × 48 mm neck. Three of four 95 × 45 × 130 mm gloved-hand corridors are clear at **0.0000 mm³**, including **both opposing +X/−X sides**; −Y (the hopper side) reads 321.2 mm³. The fill cap tops out at Z = −228.200, 1.65 mm below the corridor floor, so it does not eat the corridor. Not verifiable from CAD: the quick-release actuation envelope (B6.3) — the release half is drone-side |
| Ground / prop clearance | **rev-1 r12, re-measured after the round-6 geometry changes — but NOT independently reproduced (the 2026-08-08 verifier found no airframe STEPs at the referenced path, and the stack dropped ~52 mm this rev; treat as build-notes-carried until re-checked against the real gear):** 129.4 mm to ground (3.2× the ≥40 mm requirement — the B6 stand-off neck costs 52.04 mm), **103.63 mm** mesh-to-mesh to the real landing gear; prop clearance against the real propulsion assembly **152.55 mm vertical, 232.63 mm in-plan**, vertex-to-vertex minimum separation 374.90 mm; zero plan overlap |
| Power | 0.298 A on 12VSW against a 2 A fuse (6.7×), cleared by the payload's own 0.60 A eFuse first; 0.040 A on 12V_PL against 25 W guidance (52×) |
| Blind-mate | **NONCOMPLIANT — see RT-2.** Pads do not reach the pins |
| CAN termination | none fitted, per ICD §4 |
| DroneCAN data-type IDs | **TBD** — must be allocated in the project-quiver DSDL registry; deliberately not invented here |
| Power cycling | tolerated by design: transaction-scoped, idempotent, resumable dispense with the count in FRAM; latched faults survive a 12V_PL cycle |
| **ICD change request raised** | **FMU_CH2 / K1 default state at FC boot is unspecified** (ELECTRONICS §2.8). The only non-firmware interlock on the rail that can release herbicide has undefined behaviour at FC boot, in-flight FC reboot, RC failsafe and parameter reset. Closure = a PR to project-quiver against ICD v1.0-draft §3. Until then the payload-side 100 kΩ EN pull-down is the sole compensation and is safety-critical |
