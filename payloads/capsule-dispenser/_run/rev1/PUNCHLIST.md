# REV-1 PUNCH LIST — Brush Bullet Dispenser CAD close-out (2026-08-07)

Synthesised from `_run/RED-TEAM.md` (RT-1…RT-21), `_run/GAP-REVIEW.md` (G1…G7),
`_run/BUILD-NOTES-r6.md` (r6 critic output + open issues 1–14),
`electronics/ELECTRONICS.md` §4.2–4.5/§6/§7 (ECO-3/4/5/6/7/9/11/12), and the six
Thomas directives in `_run/rev1/CONTEXT.md`.

Scope filter applied, per the tasking: **no simulation items, no firmware/DSDL/
software items, no electrical pin-or-pad stack-up items.** Everything below is a
geometry or a BOM/geometry-coupled item that `cad/dispenser.py` and its exports
must own.

Every acceptance test is written so it can be executed on the **exported**
STEP/STL by a checker that does not read `dispenser.py` (RT-20). "MEASURED r6"
means the number was measured on the r6 exports by a red-team or critic probe and
is the baseline the fix must move. `[A]` marks an assumption I am introducing
(with its closure path); it is not a fact from any source document.

Notation for the acceptance tests: θ is the polar angle about the meter axis, r
the radius from that axis, Z the drone-frame vertical (mount plane Z = −171.0).

---

## BLOCKING — the CAD does not close until every one of these passes

### B1 — Roof through-slot at θ = 310° (entry-ramp cut is a half-space, not a sector)
**Source:** r6 pellet-path critic BLOCKER 1; re-confirmed independently by
RT-1 (roof thickness 9.00 mm at 309°, **0.000 mm at 310.0°** at r = 20.5, 24.5,
30, 32, 36, 39.5, 44, 46.5; 0.14 mm mean over 310–311°, 0.57 mm 311–313°,
1.28 mm 313–316°). Root cause named in the critic text: `dispenser.py` ~L737-750
builds `ramp_cut` from `ramp_half & Box(400,200,100)` (half-plane y′ ≤ 0) then
`Rot(Z=130)`, so the 25° undercut is mirrored 180° away.

**What must change:** confine the entry-ramp cut to the sector that needs it
(θ ≈ 96…131°), and make the downstream boundary a *ramped* face, not a vertical
step. The roof is also the sump floor and the wall→bearing-boss structural tie,
so it must return to full section outside the ramp sector.

**Acceptance test (all on `meter_housing_r*.step/.stl` and the assembly STL):**
1. Point-probe roof thickness (Z from the roof top −274.20 down) at
   **θ = 300, 305, 308, 309, 310, 311, 313, 316, 320, 330, 350, 0, 20, 45, 90°**
   × **r = 20.5, 24.5, 30, 32, 36, 39.5, 44, 46.5** → **≥ 6.0 mm at every probe
   outside θ = 96…131°**, and full nominal (9.00 mm) at θ = 200° and 310°.
2. B-rep sector boolean, 1° sectors over θ = 295…335°: material/available
   ≥ 95 % in every sector (r6: 2.2/138.4 mm³ at 310–311°).
3. Face-normal audit of the transfer arc: **no face with |n_z| < 0.05 and area
   > 20 mm² whose normal opposes disc travel** anywhere in θ = 160…131°
   (r6: a 238 mm² vertical face at n_z = 0.000 at θ = 310°). Print the largest
   such face's area and n_z whatever the result.
4. Roof-underside clearance above the disc stays 1.50 mm over the transfer arc
   (re-measure at r = 24.5/32/39.5/45.5, θ = 250→96 and 45→0) and the entry-ramp
   ceiling table (10.24@129 … 1.50@≤95) is re-printed unchanged.

### B2 — No torque path from gearbox shaft to pocket disc; grub screw is a buried blind hole
**Source:** r6 buildability BLOCKING; re-confirmed by RT-1 (disc bore
**r = 3.06 mm at all 24–36 angles, both heights** → plain round bore on a Ø6
shaft; grub pilot void ends at r = 10.60 with solid disc material 10.60→24.47 mm,
so the screw cannot be inserted). BOM is self-contradictory on the grub: COTS
table M2.5×4, fastener table M3×4, model Ø2.6 pilot, console text M2.5.

**Acceptance test (`pocket_disc_r*.stl`, `.step`):**
1. Bore radius swept at **1° × 36 heights** over the full engagement depth: a
   **flat is present** — r = 2.55 ± 0.05 mm over a contiguous ≥ 25° arc and
   r = 3.05 ± 0.05 mm elsewhere — over an axial length **≥ 10.0 mm** (vendor
   D-cut is 12 mm long, Ø6 shaft, 0.5 mm flat depth).
2. Radial ray from the disc OD inward at the grub axis: **continuous void from
   r = disc_OD/2 to the bore**, diameter ≥ the specified grub minor diameter,
   over the full path (r6: solid 10.60→24.47).
3. Driver-access sweep: a Ø(key across-flats + 0.4) × 40 mm cylinder on the grub
   axis intersects **0.000 mm³** of every other assembly solid.
4. `cad/BOM.md` names **one** grub size, and that size matches the modelled
   pilot diameter and the fastener table (a string-equality check, printed).

### B3 — Gearbox bolt pattern does not match the vendor drawing (and the corrected pattern collides with the pilot bore)
**Source:** r6 buildability BLOCKING; re-confirmed by RT-1. MEASURED r6:
`retaining_plate_chute` holes at θ = 45/135/225/315°, r = 16.8…19.9 (a 26 mm
*square*); datasheet for 14HS13-0804S-PG5 is **4 × M3 on a Ø26 ± 0.15 bolt
circle**, i.e. r = 13.0 **on the axes**. The critic also showed the naive fix
fails: a Ø3.2 clearance hole at r = 13 has its edge at r = 11.4 against a
measured Ø22.20 pilot bore (edge r = 11.10) → a 0.30 mm web, and the Ø30/Ø24
PTFE thrust-washer seat (r 11.1…15.3) loses its inner land. `MOTOR_PILOT_R = 11.0`
is itself an unverified assumption (r6 open issue list does not carry it).

**Acceptance test (`retaining_plate_chute_r*.stl` at the motor face):**
1. Four clearance holes, centres at **(±13.0, 0) and (0, ±13.0) ± 0.15 mm**,
   diameter 3.2–3.4 mm, through the full flange thickness.
2. **Minimum web between any motor-hole edge and the pilot-bore edge ≥ 1.95 mm**,
   measured on the export by EDT/medial thickness in that plane (r6-naive: 0.30).
3. Thrust-washer seat retains a continuous annular land **≥ 1.0 mm radial** with
   the new holes present; print inner and outer land radii.
4. Pilot-bore diameter is stated in the BOM with its source (datasheet value or
   an explicit ASSUMPTION line) and matches the model to ±0.05 mm.
5. Bolt-access: Ø6 × 25 mm driver columns on all four holes intersect
   **0.000 mm³** of any other solid.

### B4 — Count-sensor hardware in CAD is the geometry the electronics doc disqualifies
**Source:** RT-3 (CRITICAL) + CONTEXT rev-1 punch-list bullet on
`ELECTRONICS.md` §4.2–4.4. MEASURED r6: **one** Ø3.2 tunnel per side at
x = PCD_R = 32 in a `Box(12,12,14)` boss (`dispenser.py` L1005-1017) — the single
centred beam §4.2 proves is disqualifying. ECO-4 (window), ECO-5 (labyrinth) and
ECO-9 (stagger) are in no geometry; `cad/BOM.md` still lists the **TSSP4038**
digital receiver that §4.4 rejects.

**What must change (verbatim ECO geometry):** boss `Box(12,12,14)` →
**`Box(20,12,14)` centred at x = 32** (spans x = 22…42); **two Ø3.2 apertures per
side at x = 29 and x = 35**, at **z = Z_SENSOR + 3.0 and Z_SENSOR − 3.0**
(ECO-9's 6.0 mm vertical stagger; both sides on the *same* x/z grid so each beam
is a straight chord along y); component pocket → **20 × 8 × 12 cavity**;
**ECO-4** Ø6 × 1 mm PMMA window seat at the **bore face y = ±11, flush**, in a
0.4 mm chamfered recess; **ECO-5** lateral labyrinth — outer 2.5 mm of each
tunnel offset **0.8 mm in x**, leaving a 0.8 mm ledge.

**Acceptance test (`retaining_plate_chute_r*.stl/.step`):**
1. Aperture count and position: **4 tunnels total** (2 per side), axes at
   (x = 29, z = Z_SENSOR + 3.0) and (x = 35, z = Z_SENSOR − 3.0), Ø3.2 ± 0.1,
   verified by ray-casting along ±y at each nominal axis.
2. **Beam clearance:** a Ø2.0 × 60 mm cylinder on each beam axis from the emitter
   window plane to the receiver window plane intersects **0.000 mm³** of printed
   material (this is the check ECO-5's withdrawn 15° slope would have failed by
   7.2 mm of drop).
3. Boss envelope x-min **≥ 22.0**; **clearance from boss face to the motor face
   at x = 17.6 measured ≥ 4.0 mm** (r6 = 1.4 mm at the chute, 4.4 mm predicted
   with ECO-3 — print the measured number, not the predicted one).
4. Window seat: Ø6.0 ± 0.1 recess, **0.4 ± 0.05 mm deep**, its floor **flush with
   the chute bore wall at |y| = 11.0 ± 0.05** (no material proud of the bore:
   probe the bore radius at the window θ before and after the seat).
5. Labyrinth: at the outer 2.5 mm of each tunnel the axis is offset **0.8 ± 0.1
   mm in x** and a ledge of ≥ 0.7 mm exists (measure tunnel centroid x in the
   inner 20 mm vs the outer 2.5 mm).
6. Sensor-board cavity clears a **20 × 8 × 12** envelope (boolean of an
   18 × 12 × 2 board body + 1 mm all round = 0.000 mm³ interference).
7. `cad/BOM.md` contains **no TSSP4038 line**, and does contain
   VBPW34FAS × 2, OPA2320, TSAL6200 × 2, and 4 × PMMA Ø6 × 1 windows.
8. Chute-bore continuity re-checked: Ø13.0 worst-case pellet swept down the
   chute axis intersects **0.000 mm³** with the new apertures/windows present.

### B5 — The dispenser has no real electronics/wiring home (Thomas directive 2)
**Source:** **Directive 2** (verbatim: "right now it looks like the wiring would
go straight into the tank") + `ELECTRONICS.md` §6.2 **ECO-6** (bay has one
modelled cable entry, needs three, grommeted), **ECO-7** (four M2.5 board
standoff bosses are not modelled), §7 (main board 42 × 34 mm, vertical, bay
interior 46 × 22 × 38), r6 open issue 11 (perimeter gaskets are schematic).
This is the *only* surviving part of RT-2 (see VOID list).

**What must change:** a sealed, dust-tight bay that actually houses the control
PCB, plus **modelled** wiring routes: interface PCB → bay, bay → motor,
bay → count-sensor boards — none of which may cross the hopper/pellet volume.
The r6 top-plate 5 × 2.5 mm channel exists but stops at the −Y rim; there is no
modelled conduit from the rim down to the bay.

**Acceptance test:**
1. **Board fits:** boolean of a 42 × 34 × 12 mm board envelope + 4 × M2.5
   standoffs (≥ 4 mm tall, bosses modelled, ECO-7) against `electronics_bay` =
   **0.000 mm³ interference**, with **≥ 1.5 mm clearance** to every interior
   wall (print the six measured gaps).
2. **Three cable entries** (ECO-6) exist as modelled openings with grommet seats:
   aircraft harness on −X, motor and sensor cables on the inboard face; each
   opening ≥ Ø6.0 for the grommet, and each has a seat land ≥ 1.5 mm wide.
3. **Gasket is real geometry, not schematic:** a continuous groove around the lid
   joint, **≥ 1.5 mm wide × ≥ 1.0 mm deep**, closed loop (verify by extracting
   the groove as a single closed sweep, and report its perimeter length).
4. **Harness never enters the pellet space:** model the harness as swept solids
   (Ø5.5 for the 9-conductor bundle [A], Ø4 for the motor and sensor pairs) along
   the modelled routes and boolean them against the hopper interior, the funnel,
   the sump, the metering arc and the chute →
   **0.000 mm³ in every one of those five volumes.**
5. **Route is continuous and covered:** the swept harness solids are contained
   within modelled channel/conduit geometry over ≥ 90 % of their length (report
   the uncovered length in mm and where it is); the top-plate channel fill stays
   ≤ 70 % (§6.3 measured 62 % for 9 × 26 AWG in 12.5 mm² — recompute for the
   final channel section and print it).
6. **Bay lid removable in situ:** 4 × screw driver columns Ø6 × 25 mm and a
   lid-lift sweep of (lid + 0.5 mm) × 20 mm outboard both intersect
   **0.000 mm³** of any other solid.
7. Bay + lid + standoffs + grommet seats appear in `cad/BOM.md` with masses, and
   the mass delta is carried in B11.

### B6 — Attachment-interface reach-in clearance (Thomas directive 3)
**Source:** **Directive 3** ("give it some more clearance from the rest of the
dispenser … Prove it with a measured access corridor, not adjectives").
Baseline r6: the Ø150 top plate face is at Z = −186.5, i.e. **5.0 mm** below the
clip plate underside (−181.5) and spans r = 75 in every direction — there is no
hand access to the quick-release at all.

**What must change:** stand the clip-plate/QR region off the dispenser body on a
neck so a gloved hand can reach the release from the side, on the aircraft.

**Acceptance test:**
1. Define in the model, and print, a **stand-off height h** (clip-plate underside
   Z = −181.5 to the topmost dispenser body material outside the neck) and a
   **neck plan half-extent a** (max |x|,|y| of payload material in the stood-off
   band). Targets: **h ≥ 40 mm** and **a ≤ 35 mm** `[A]` — a 40 mm gap and a
   70 mm-wide neck are my assumption for a gloved hand working a QR lever;
   closure = one sentence from Thomas or a mock-up. If the numbers land
   elsewhere, they must be *stated and justified against a hand dimension*, not
   adjectives.
2. **Corridor boolean:** four corridor boxes **95 (wide) × 45 (tall) × 130 (deep)
   mm** `[A: gloved hand 95 × 45, forearm reach past the QR 130]`, approaching the
   mount axis from +X, −X, +Y and −Y, their tops at Z = −181.5, intersect payload
   material in **0.000 mm³ on at least two opposing sides**; print the intersected
   volume for all four and the min distance from each corridor to the nearest
   payload material.
3. **QR actuation sweep:** the vendor quick-release's release motion envelope
   plus 10 mm intersects **0.000 mm³** of dispenser material.
4. **No regression on the aircraft side:** payload material above Z = −171.000 is
   **0.000 mm³** (r6 reported 0.0397 mm³ from the ICD's −171.047 rounding — fix
   by placing the payload top face at Z ≤ −171.05 and reporting 0.000).
5. **Ground clearance re-reported after the stand-off** (the neck pushes the
   whole stack down): mesh-to-mesh to the real landing-gear STEP
   **≥ 40 mm required**, r6 measured 181.484 mm — print the new number and the
   new payload↔landing-gear minimum separation (r6: 83.41 mm).
6. Prop clearance re-reported (r6: vertical 152.50 mm, in-plan 251.13 mm).

### B7 — "Stationary release / zero lateral velocity / full Ø18 aperture" is geometrically false
**Source:** r6 pellet-path critic BLOCKER 2; carried in RT-19 as a documentation-
integrity instance. MEASURED r6: exit port Ø18.00 at PCD 32, 0.75 × 45° top
chamfer, rim radius at the plate top **r = 9.75**; pocket bore r 7.50 vs pellet
r 6.50 → the pellet centre can sit ±1.00 mm off the pocket axis; park separation
2·32·sin 11.25° = 12.485 mm; support is lost at **8.75–10.75 mm separation =
3.16–6.78° into the 22.5° index (14–30 % of the move)**, i.e. while the disc is
moving, through a partial lune, before the 150 ms dwell begins.

**What must change:** either the geometry (port/rim/chamfer or the two-phase park
angles) so release genuinely happens with the pocket concentric and stationary,
or the claim. A geometric close is preferred; a documented plateau is acceptable
**only** if it prints the measured release angles and the resulting lateral
velocity and the README/DESIGN text is corrected in the same round.

**Acceptance test (`retaining_plate_chute` + `pocket_disc` exports):**
1. Sweep the index in **0.25° steps** and, for the worst-placed Ø13 and Ø11
   pellets (centre offset ±1.00 mm), find the separation at which the contact
   point crosses the port rim. Requirement to *close*: **support retained until
   |separation| ≤ 1.0 mm** (release inside the dwell window).
2. Print the **release-angle spread** across pellet diameter and lateral seat
   (r6: 3.62° of disc rotation) and the implied lateral velocity at the PCD for
   the stated index profile (r6: 0.126–0.25 m/s).
3. Re-print park retention against the rim with any new rim radius (r6: D13
   +1.74, D12 +1.24, D11 +0.74 mm — none may go negative).
4. Any sentence in build notes/README claiming "stationary release" must be
   traceable to check 1 passing (RT-19 rule).

### B8 — Rejection band sits above the shear band: fragments 1.50–3.00 mm proud meet only bristles
**Source:** r6 pellet-path critic MAJOR 3 (the critic states the fix in one
line: **`NOSE_GAP` 3.00 → ≤ 1.50 mm = `ROOF_CLEAR`**). MEASURED r6: roof
underside 1.50 mm above the disc; deflector-nose underside **3.00 mm** constant
over r = 22.0–46.5; bristle tip 1.20 mm. A Ø5.0 fragment nested in the pocket
chamfer sits +1.80 proud, Ø6.0 +2.95 — both pass the nose untouched. This is a
direct hit on the standing fragment-jam requirement ("reject before wedge"), so
it cannot be left to a later round.

**Acceptance test (`brush_holder` + `meter_housing` + `pocket_disc` exports):**
1. Deflector-nose underside height above the disc top measured at
   **r = 22.0, 26, 30, 34, 38, 42, 46.5** → **≤ 1.50 mm at every radius**, and
   **≥ the bristle free-trim contact height** so the compliant element still
   leads (re-print the contact-order table for 2.0 / 3.0 / 5.0 / 7.0 / 9.0 /
   11.5 mm proud objects; rigid element must not lead below 5 mm proud).
2. **No band remains uncovered:** max(nose gap) ≤ min(roof clearance) over the
   whole rejection arc; print both.
3. Re-run the wedge construction with the new gap: Ø5.0 (+1.80) and Ø6.0 (+2.95)
   fragments must now be **contacted by the nose**, and the nose lift/push ratio
   (cot 30° = 1.73) must still exceed the self-locking requirement (1.44).
4. Re-run `brush_holder` thin-section statistics after the change and re-print
   the 20.4 N stress check (r6: σ = 1.6 MPa, deflection 0.004 mm; min wall
   0.00 / p1 0.26, 28.1 % under 1.95 mm — this may get worse and must be stated).
5. Disc-transit: Ø13 worst-case pellet through all 23 stations still
   **0.000 mm³** with the lowered nose.

### B9 — COTS interface fits that make the assembly unbuildable as drawn
**Source:** r6 buildability MAJOR + MODERATEs; RT-13 (the 4 mount screws carry
the whole payload). Each sub-item has its own measured baseline:

| # | Defect | MEASURED r6 | Acceptance test |
|---|---|---|---|
| a | Mount screws get **0.90 mm** of thread engagement (BOM says M2×10; grip head-face to insert top = 4.10 + 5.00 = 9.10 mm) | 0.90 mm ≈ 2 threads at 0.4 mm pitch | Grip length measured from the vendor STEP head-bearing plane to the modelled insert top; **screw length − grip ≥ 3.2 mm** (≥ 80 % of the 4.0 mm RX-M2×4 insert). BOM + fastener table both state the same length. Re-measure after B6 moves the mount. |
| b | Hopper-flange insert holes **4.19 mm** deep vs BOM's Ruthex **RX-M3×5.7** | blind −186.50…−190.69 | Modelled bore depth **≥ insert length + 0.3 mm**, measured on `hopper_r*.stl` at all 6 positions; boss wall around each insert ≥ 1.95 mm. |
| c | Detent plunger has **nothing to thread into**: bore measured Ø5.10–5.20, a clearance hole, unthreadable for M5 | Ø5.10–5.20 | Either a modelled thread-forming boss (Ø4.2–4.6 ± 0.1 over ≥ 6 mm) or a modelled nut/insert pocket with the part in the BOM; plus a driver/adjustment access sweep of **0.000 mm³**. The detent is **96.5 of the 190.7 mN·m** load budget, so it is not optional. |
| d | Bearing seat **Ø23.100** vs igus JFM-2023-07 OD 23.00 = slip fit, no retention modelled | +0.05 mm/side | Seat bore **≤ Ø23.03** (igus asks H7) **or** a modelled retaining lip/anti-rotation feature; print the measured bore, the flange counterbore depth (1.7 mm) and the sleeve length (7.0 mm) fit. |
| e | Grub-screw size stated three different ways | M2.5×4 / M3×4 / Ø2.6 model | Covered by B2.4. |

### B10 — Export integrity: `meter_housing` is not watertight, and the notes claim it is
**Source:** r6 pellet-path MINOR 6 + buildability MINOR + mass-budget NOTE +
RT-19.1. MEASURED r6: one non-manifold edge shared by 4 faces at
(20.891, −24.896, −274.200) = r 32.50, θ = 310.0°, i.e. **on the B1 bug line**;
`verify_exports.py` prints `watertight=False` and `15/16` while
`BUILD-NOTES-r6.md` §4 says "10/10 … 16/16".

**Acceptance test:** the checker's own printed output shows **10/10 part STLs
watertight, assembly 16/16 (or the new part count), 0 non-manifold edges,
Euler characteristic as expected for each part**, and the build notes quote that
output verbatim rather than restating it (RT-19 rule; RT-20 requires the checker
be derived from requirements/datasheets, not from the model).

### B11 — Mass ledger must re-close after every fix above
**Source:** standing rev-0 rule in `_run/rev1/CONTEXT.md` ("Structure mass target
≤ 1500 g dry; report loaded mass at 250 and at max fill"); RT-9 (mass creep
+58 g/round, r6 margin **113 g** at LOADED@250 = 1387.4 g); mass-budget critic
(padded-EDT bug: 334.0 g claimed → **383.4 g** corrected at 4 walls/25 % infill).
B4 (+6 g ECO-3), B5 (bay standoffs/grommets/conduit), B6 (stand-off neck) and B3
(flange rework) are all additive.

**Acceptance test:**
1. Ledger re-printed from measured export volumes at **CF-PETG 1.27 g/cm³**
   (not the low-end 1.25) with the **padded** EDT (`np.pad(mat, 4)`) for the
   slicer bracket; both the solid and realistic-infill bases printed.
2. **LOADED @250 ≤ 1500 g** on the shipped headline basis, and **max-fill mass
   reported** (r6 brim @422 = 1590.4 g solid basis) with the exemption stated,
   not used silently (RT-10).
3. Stepper carried at **≥ 350 g** or the vendor's 0.38 kg gross until it is on a
   scale (mass critic MINOR; G7 item 6), with the sensitivity re-run.
4. A **per-open-item mass reserve line** appears in the ledger (RT-9).

### B12 — Refill has no stable rest position and no usable fill geometry
**Source:** RT-14 (MODERATE) — explicitly promoted by `_run/rev1/CONTEXT.md`
("RT-14 … should be addressed via directive 4 + a side-wall fill port above the
250-pellet line **or an equivalent measured solution**") + **directive 4**
(whole-dispenser removal is the baseline; cartridge is a stretch goal only).
MEASURED r6: fill cap needs 6.45 mm of lift then **58 mm of lateral travel in a
10.5 mm gap**; set down on the clip plate the table occupies exactly that travel;
stood chute-down it is a 195 mm tall, Ø140, 1.09 kg object on a 35 × 35 mm motor
can, tip angle ≈ 11°.

**Acceptance test — whichever route is taken, it must be measured:**
1. **Rest position:** a modelled flat ground plane supports the dispenser with a
   **tip angle ≥ 25°** `[A: 15° of ranch-tailgate slope + margin]` and the load
   path does **not** pass through the gearbox output flange (boolean: the
   support-contact patch lies on printed structure, not on the motor can); print
   the support polygon area and the CG-to-edge distances using the CG table
   (RT-17: empty CG (0.88, −6.55, −279.4)).
2. **Fill route:** with the dispenser in that rest position, the fill cap's
   removal sweep (lift + rotation + lateral) intersects **0.000 mm³** of the
   ground plane and of the dispenser; print the required lift and lateral travel.
3. If a **side-wall port** is used: its lowest edge is **above the 250-pellet
   line** (r6 rib at z = −222.6) by ≥ 5 mm, its clear opening ≥ Ø46 `[A: matches
   the existing 3.5 × pellet-diameter port]`, and a Ø13 pellet path from the port
   to the bed is **0.000 mm³** obstructed; hopper wall thickness around the port
   ≥ 1.95 mm; capacity re-measured and **unchanged within 2 %** (directive 5 —
   do not re-open capacity).
4. Refill does **not** require removing the payload from a fixture that does not
   exist: if a cradle/funnel is the answer, it is a modelled printed part in the
   BOM with the same tip-angle check.

---

## NONBLOCKING — fix if the round has room; otherwise record with measured numbers

| # | Item | Source | Acceptance test (measurable) |
|---|---|---|---|
| N1 | **Fill ribs are proud internal shelves** in the flow zone (0.8 mm at z −222.6 in the 68° cone; 1.05 mm at z −196.9) with a ≈45° upward-facing annular flank | RT-18 | Re-cut as **recessed grooves**: no feature protrudes > 0.0 mm inboard of the local wall; groove depth 0.8–1.2 mm; remaining wall ≥ 1.95 mm; capacity change < 1 % (directive 5) |
| N2 | **Magnet retention unspecified** — 9 loose Ø3 × 2 magnets; pocket modelled `MAG_R = 1.5` = Ø3.00 = zero interference | RT-16, ECO-11 | Pocket **Ø2.95 ± 0.02** (0.05 mm diametral interference) at all 9 positions, measured on `pocket_disc`/plate exports; retaining-compound bead volume modelled or a BOM line with the first-article pull test named |
| N3 | **Sensor board retained by a point-contact M3 grub** on a PCB edge | RT-16, ECO-12 | Nylon-tipped grub (BOM change) **or** a modelled clamp plate with ≥ 8 mm² of bearing area on the board edge; clamp screw driver column 0.000 mm³ |
| N4 | **Agitator retained by gravity only** | r6 open issue 8, RT-16 | A modelled positive retainer (circlip groove, screw, or snap land) with ≥ 0.4 mm of axial capture measured, and a drain-by-inversion sweep that still clears 0.000 mm³ |
| N5 | **Fill-cap anti-rotation detent deleted rather than closed** | RT-15 | Detent geometry present (bump/ramp with ≥ 0.3 mm interference or a modelled spring feature) plus measured bayonet lug engagement ≥ 3.0 mm; cap-removal torque path stated |
| N6 | **Disc lightening holes break into the sump window** over a ≈2.0 mm crescent (Ø7.0 at r 18.5 spanning r 15.0–22.0 vs window inner edge r 20.00) | r6 pellet-path NIT 8, RT-12 | Holes repositioned/resized so the **radial land from hole edge to r = 20.00 is ≥ 2.0 mm**; disc mass delta printed |
| N7 | **Chute mouth is permanently open** (Ø22 at Z = −353.2, 181.5 mm above the ground it is landed on and blasted with downwash) | RT-7, RT-8 | A printed/elastomer **storage plug** part: 0.2–0.4 mm diametral interference in the Ø22.0 bore over ≥ 8 mm, a pull tab, a BOM line, and a 0.000 mm³ interference check when fitted |
| N8 | **Perimeter gaskets outside the bay are still schematic** (only the fill-cap O-ring gland is real geometry) | r6 open issue 11 | Each claimed joint either gets a real groove (≥ 1.5 × 1.0 mm, closed loop, perimeter printed) or the README says plainly that joint is dust-resistant, not sealed |
| N9 | **Safety tether has no hard point** — 1.39–1.59 kg on 4 × M2 with CG 102 mm below the mating plane | RT-13, RT-17, G6 | A modelled tether lug: hole ≥ Ø4.0, minimum section ≥ 2.5 mm, 0.000 mm³ into the B6 access corridor and the clip-plate footprint; BOM line for the tether |
| N10 | **Sump outlet is 26.5 mm × 120° = 2.04 × D_max with ~66 % dead flat shelf**; the no-arch criterion is met "only through the active-agitation branch" | r6 pellet-path MODERATE 4 | Either improve (report new min opening / D_max ratio and the swept fraction per index, r6: 18.8 % per index, one sweep per 2.67 pellets) **or** record as an explicit plateau-with-complaint quoting those measured numbers. Capacity must not change (directive 5) |
| N11 | **No isolation gate** — any jam clear dumps the hopper (service-drain residue 115 cm³ ≈ 51 pellets) | r6 pellet-path MODERATE 5 | If a gate is added: a modelled slide/plug with a 0.000 mm³ actuation sweep and a measured shut-off area ≥ the 120° window. Otherwise: the measured consequence is written into `docs/DESIGN.md` service section |
| N12 | **Stale derived-Z-stack comments** in `dispenser.py` L384-397 (off by 5.3–23.0 mm vs the exports) | r6 pellet-path MINOR 7 | Every Z constant's comment matches the exported plane to ±0.05 mm; the checker prints both columns |
| N13 | **Slicer-bracket EDT bug** (unpadded distance transform → hollow core overstated; 334.0 → 383.4 g) | mass-budget MODERATE | `np.pad(mat, 4)` (or equivalent) applied; a flat-plate control (`bay_lid`, 3.2 mm) must report ≤ 10 % hollow core, not 83 % |
| N14 | **Checker is not independent** — `verify_exports.py` missed the 310° slot, the missing D-flat and the wrong bolt pattern, and its own watertight failure | RT-20 | Each check is written from a requirement or a datasheet value typed from the source (bolt circle Ø26, shaft flat, aperture count/positions, wall minima), and each self-check prints **what a failing part would look like** |
| N15 | **Documentation integrity rule** | RT-19, CONTEXT standing rule | Every sentence in the rev-1 notes containing "measured" is traceable to a line the tool printed; critic approvals print actual numbers |
| N16 | **CG table is not published** | RT-17 | Publish the measured CG at empty / 125 / 250 / brim in the README mass section, recomputed after B5/B6 move mass outboard and upward |
| N17 | **Fill-mark semantics** (worst-case 2.28 mL/pellet packing constant = 40 % packing; "250" rib is 250–370 real pellets) | RT-5, RT-10 | Documentation only this run (directive 5 forbids re-opening capacity): print both rules side by side — mass-limited line (242 pellets, quadruple-conservative) and volumetric brim (422 worst-case) — and add the fill-by-mass label text to the BOM |
| N18 | **M2 head clearance 0.05 mm/side** in the vendor's Ø3.90 head pocket | r6 open issue 2 | Re-measure after B6; if still < 0.10 mm/side, model the documented fallback (90° × Ø6.0 countersink + M3 flat-head) as an alternative and state which is shipped |
| N19 | **Loaded-standby / material-and-finish contradiction**: ECO-1/ECO-2 want α ≤ 0.4 external surfaces; BOM specifies CF-PETG (black, α ≈ 0.95) for 9 of 10 printed parts | RT-6, G3.2 | Not a geometry fix: the BOM must state one material/finish decision per external part (pigmented PETG / ASA-CF / coating) with its α, and the README states the loaded-standby limit |

---

## VOID for this run — findings the directives retire (with the reason)

| Finding | Status | Why |
|---|---|---|
| **RT-2** (CRITICAL, "payload has no electrical connection") — 19.35 mm pad-to-pin gap, 8.85 mm at the best legal pad plane | **VOID except its bay implication** | Directive 1: "We know that the PCBs mate electrically when the attachment interface pieces connect. You don't have to worry about that part at all." The attachment interface is a black box delivering a harness. The surviving half — *the dispenser needs an electronics home and routed wiring* — is directive 2 and is **B5** |
| r6 interference **BLOCKER** (blind-mate 19.350 mm), **MAJOR** (clip half nests ≤ 0.54 mm; standoffs would push material above −171), **MODERATE** (pin tips mis-identified at −163.73 vs −162.150, every margin 1.58 mm optimistic), **MODERATE** (PCB 16.000 in a 16.0000 shaft = 0.000 clearance) | **VOID** | All four are spring-pin/pad stack-up or blind-mate PCB placement — directive 1, and explicitly outside my tasking |
| r6 **open issue 1** (blind-mate pad plane, "not closable in CAD") | **VOID** | Same |
| **RT-4** (1 m accuracy, hover-σ Monte Carlo, wind limits) and **G1** (drift table, canopy interception, bounce/roll, aero variation) | **OUT OF SCOPE** (not "wrong") | Directive 6: simulation is skipped this run; and the ballistics/accuracy owner is the FC/targeting side, not payload CAD. Retain in the risk register, do not action here |
| **G2** (targets per flight, `SetLoad` / `pellets_remaining` / `LOW_HOPPER`) | **OUT OF SCOPE** | Contract/DSDL = software; excluded from this punch list |
| **G3.1 / G3.4** (dock refill, dock payload envelope, 58–59 mm deck clearance, AC_BELLY_CLEAR datum) | **VOID** | Directive 4: "We wouldn't be using this payload with the dock anyways" — dock compatibility is moot. (G3.2's loaded-standby limit survives as **N19**, documentation only) |
| **G3.3** (K1 state at FC boot ICD change request) | **OUT OF SCOPE** | Electrical/ICD item, and dock-triggered — both retired by directives 1 and 4 |
| **RT-5 / RT-10** *as capacity arguments* (re-base the fill marks, re-price the brim, 250 → 370 pellets) | **VOID as a design change; survives as documentation** | Directive 5: "Capacity is settled … Keep the ~422-pellet hopper as-is unless a punch-list fix forces a change. Do not re-open the capacity trade." Reduced to **N17** (state both rules) and **N1** (rib geometry) |
| **RT-14**'s dock/on-aircraft-refill framing | **Re-scoped, not void** | Directive 4 makes whole-dispenser removal the baseline and the swappable cartridge a stretch goal only; the *rest-position and fill-geometry* half is promoted to **B12** by CONTEXT |
| **RT-11** (recovery torque vs measured crush distribution, IFDC S-115), **RT-12** (fines budget, S-116), **RT-6** (loaded-hopper solar soak), **RT-7** (humidity/swollen pellet), **RT-8** (landing dust cycles), **RT-21** (count-contract residuals), **G5** (pellet mass/shape/lot acceptance), **G7** items 1, 2, 6 | **NOT VOID — bench/test-plan items, not CAD** | They stay in the shipped test plan and risk register. The only geometric hooks this run owes them are **N7** (chute plug), **N6** (fines path), **N2** (magnet retention) and the go/no-go gauge idea in G5.3, which is optional this round |

---

## Notes on how this list is meant to be used

- **BLOCKING** means the round cannot be declared closed with the item open. A
  blocking item may be closed either by geometry **or** by an explicit
  plateau-with-complaint that prints the measured number and corrects every
  document that claimed otherwise — but only where this list says so
  (**B7**, and **N10** among the nonblocking items). B1–B6 and B8–B12 must be
  closed by geometry.
- Assumptions I introduced are only in **B6** (hand/corridor dimensions), **B12**
  (tip angle, side-port size), and **B5** (harness bundle diameters). Everything
  else is traceable to a cited finding, critic line, ECO, or directive.
- The three items with no rev-0 finding behind them at all — they exist only
  because Thomas said so — are **B5** (directive 2), **B6** (directive 3) and the
  re-scoping of **B12** (directive 4).
