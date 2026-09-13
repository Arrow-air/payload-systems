# Capsule Dispenser — Build Guide (r13)

How to fabricate and assemble the dispenser as designed at export tag `r13`.
Read [`README.md`](README.md) first for what the machine is. Every dimension
and sequence step below is measured on the exported geometry (sources:
`cad/BOM.md`, the assembly-order proofs in `_run/rev1/`, close-out notes) —
this document collects them in build order so you don't have to.

**This machine has not been built yet.** Where a step depends on an unverified
assumption, the gate is stated inline. Do not skip §0.

---

## 0. Before you spend money or filament

1. **Caliper the gearbox output boss** on the real motor. The retaining
   plate's pilot bore is modelled **Ø16.20**; the boss diameter it must clear
   is an ASSUMPTION (not in the datasheet extract). Wrong boss = reprint the
   plate. Do this before printing `retaining_plate_chute`.
2. **Weigh the stepper.** The 350 g in the ledger is a catalogue figure. If it
   comes in heavy, the 68 g mass margin erodes first.
3. **Sweep the 19 TODO-VERIFY pins in [`cad/BOM.md`](cad/BOM.md)** while
   ordering — they are class-level part callouts that need a real orderable
   number confirmed at purchase time.
4. Count windows are **Ø5.90 × 0.95** (the modelled size). ELECTRONICS ECO-4
   still says Ø6 × 1.0 — order to the BOM, not the ECO.

## 1. Print

Ledger basis (what the mass budget assumes): **4 perimeters at 0.4 mm,
25 % infill**. CF-PETG structure, TPU for the two compliant parts. From the
generated BOM (mass at 100 % infill for reference):

| part | qty | material | mass g | orientation | support % |
|---|---|---|---|---|---|
| top_plate | 1 | CF-PETG | 121.4 | rotX+90 | 9.7 |
| fill_cap | 1 | CF-PETG | 9.6 | rotY−90 | 5.4 |
| hopper | 1 | CF-PETG | 139.0 | flipped (rotX180) | 0.9 |
| meter_housing | 1 | CF-PETG | 131.9 | flipped (rotX180) | 7.7 |
| pocket_disc | 1 | CF-PETG | 92.3 | as-modeled | 2.9 |
| agitator | 1 | TPU | 5.1 | rotX+90 | 8.9 |
| brush_holder | 1 | CF-PETG | 4.5 | rotX+90 | 5.3 |
| retaining_plate_chute | 1 | CF-PETG | 81.2 | flipped (rotX180) | 8.2 |
| electronics_bay | 1 | CF-PETG | 26.9 | rotX+90 | 11.0 |
| bay_lid | 1 | CF-PETG | 10.9 | rotX+90 | 0.0 |
| sensor_cover | 2 | CF-PETG | 4.1 | — | — |
| chute_plug | 1 | TPU | 8.1 | — | — |
| service_stand | 1 | CF-PETG | 132.0 | — | — |

`count_windows` (×4) are **laser-cut cast PMMA**, not printed.
`service_stand` and `chute_plug` are ground kit, not flight mass — but the
stand is **mandatory GSE**: without it a removed dispenser stands on its own
gearbox flange. Print one per field kit.

## 2. Order

Everything is in [`cad/BOM.md`](cad/BOM.md): COTS table (motor, bearing,
plunger, sensors, MCU, magnets, inserts, grommets, gasket cord, O-ring,
adhesive) and the fastener table with per-location quantities and lengths.
Fastener lengths are engagement-verified — **do not substitute lengths**; the
notable ones and why:

- Gearbox → plate: **4 × M3×8 countersunk (ISO 10642/DIN 7991), NOT cap
  head.** A cap head stands 2.65 mm proud into a 0.5 mm gap and jams the
  disc. Flush flat heads measure 0.0000 mm³ interference at every disc angle.
- Bay ribs → housing: **M3×18** (an M3×12 gives 0.000 mm of engagement —
  measured, not a typo).
- Hopper skirt tabs → housing: **M3×8 plastite** — 3.80 mm of thread into a
  4.10 mm pilot; longer bottoms out before clamping.

**Tools:** 2.0 mm hex (countersunk screws), **1.5 mm hex with ≥60 mm shaft**
(the disc grub — it's driven 43 mm down a Ø3.4 channel), drivers ≤ Ø8 for the
bench cartridge screws, soldering iron for heat-set inserts, UV lamp for the
window adhesive.

## 3. Bench prep (before main assembly)

1. **Heat-set inserts.** The 4 × RX-M2×4 mount inserts go into `top_plate`
   **from the underside, while it is still a loose part** — the Ø2.5 lead-in
   from the top face won't pass a Ø3.2 insert; the shoulder below is the
   depth stop. The 6 × RX-M3×5.7 flange inserts likewise while loose (flange
   holes are at **r = 74.0**).
2. **Count windows.** The 4 PMMA discs fit **from inside the chute bore,
   pushed outward** into their bore-face seats (they physically cannot enter
   from outside — Ø5.9 window, Ø3.2 tunnel). Bond with UV-cure optical
   adhesive; keep the optical faces clean.
3. **Sensor boards.** Emitter board +Y, receiver −Y, one 18×12×0.5 silicone
   pad between each board and its cover's clamp posts. Covers fix with
   4 × M2×6 self-tap into the boss ears.
4. **Drive cartridge (on the bench).** Motor+gearbox onto
   `retaining_plate_chute` with the 4 countersunk M3×8 (2.0 mm key; largest
   usable driver on the bench pose is Ø8). **QC: heads flush** — any
   proudness will jam the disc. Then the PTFE washer (Ø38/Ø34×1.4) drops into
   its plate counterbore **from above, after the motor** — it is not part of
   the motor stack and cannot be fitted from below.

## 4. Assembly (the order is forced, not chosen)

Swept-volume proofs in `_run/rev1/CRITIQUE-r4.md` §1 show each step's approach
is the *only* clear one (the controls: bearing from below = 580 mm³ of
interference; disc from above = 29,565 mm³). Sequence:

| # | step | approach / note |
|---|---|---|
| 1 | `meter_housing` in fixture | datum |
| 2 | igus JFM-2023-07 bushing into the roof bore | from **above** only |
| 3 | `brush_holder` + strip brush | radial slide-in at θ=148° |
| 4 | `pocket_disc`, hub up through the bearing | from **below** only. QC: disc spins free; roof clearance is 1.500 mm by design |
| 5 | `agitator` onto the Ø15 hex | from above |
| 6 | drive cartridge from §3.4 | descends into the housing **counter-indexed −20…−24°**, then rotates to 0° to lock. QC: free rotation band ≈ −24.5…+0.5° before the stop pin |
| 7 | M3×6 **stop pin**, radial θ=51° | bounds drive-reaction lash to 2.46°; without it the cartridge has 25° of free rotation ending in the drop-out window |
| 8 | M3×4 cup-point **grub**, radial θ=202.5° | index the disc so the bore flat faces the channel; drive the grub 43 mm down the Ø3.4 channel with the long 1.5 mm key onto the shaft D-flat. **QC — this is the r13 close-out item: the grub must seat on steel with a hard metallic stop.** If it bottoms soft/springy it is pressing on plastic — the r12 defect — stop and investigate. Residual axial play ≈ 0 |
| 9 | `electronics_bay` onto the housing ribs | −Y; 2 × M3×18. Fit the 3 grommets + 2 duct grommets and the 182 mm gasket-cord loop in the lid groove |
| 10 | `bay_lid` | −Y; 4 × M3×8 self-tap. Removable in situ |
| 11 | `hopper` down over the bay riser | +Z; 3 × M3×8 plastite at the skirt tabs; 6 × M3×10 SHCS into the flange inserts (r=74) |
| 12 | `top_plate` onto the hopper flange | +Z |
| 13 | clip plate + blind-mate PCB | +Z; 4 × M2×10 SHCS at (±19,±19) into the underside inserts — 3.5 mm engagement; 4 × M2×5 pan for the PCB |
| 14 | `fill_cap` | rotate 90°, lift, slide +Y; 1.5 mm nitrile O-ring (ID 43.6) in the gland |
| 15 | magnets | 8 pocket + 1 index, Ø3×2 N45 — set orientation consistently before gluing |
| 16 | `chute_plug` + tether | ground kit: 150 mm Dyneema, plug eye → chute anchor lug. Visibility + retention, **not** an interlock |

Cartridge service removal later: the whole drive cartridge extracts from the
built machine by reversing 6 (unlock −22°, lift) — verified clear against
every installed solid.

## 5. Electronics and first power

The electrical design is a **document, not a board** —
[`electronics/ELECTRONICS.md`](electronics/ELECTRONICS.md) has the power
tree, drive, sensing, DroneCAN contract and the priced electronics BOM; no
KiCad exists yet. Until boards exist, bench bring-up means the dev-board
harness described there. First-power gates, in order:

1. Motor indexes 22.5° steps at ≤0.30 A on 12VSW; Hall index magnet reads.
2. **B1 dark-time survey** — the bench test that turns the count hardware
   into a count *claim* (9.7–25 ms gate window against real pellet drops).
3. Detent plunger force ≈2.5 N end force (LIGHT spring — a stiffer one
   changes the fragment-recovery math).

## 6. Before anything flight-adjacent

- **Re-measure ground/gear/prop clearance against the real aircraft.** The
  package numbers (129.4 / 103.63 / 152.55 mm) are carried from build notes;
  no airframe STEPs existed to verify them. Calipers on the real gear.
- **IFDC S-115 crush test** on real pellets — σ = 0.36 MPa and µ = 0.4 are
  carried assumptions inside every jam-force margin.
- Weigh the finished unit: the ledger predicts ≈1140 g dry on the print
  settings above (1281 g is the 100 %-infill pessimistic bound). Record the
  actual against `cad/BOM.md`'s roll-up.
- The FMU_CH2/K1 boot-state ICD question must be closed (or the payload-side
  100 kΩ EN pull-down verified fitted) before the herbicide path is armed.
