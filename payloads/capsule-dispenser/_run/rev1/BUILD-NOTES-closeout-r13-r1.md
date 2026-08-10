# Close-out r13 — build notes (2026-08-10)

Executed BY HAND in a long-lived supervised session (Hex + Thomas), not by a
spawned workflow agent: all seven spawned-agent attempts at this close-out
(2026-08-08 → 2026-08-10 morning) were killed at spawn by API content-safeguard
false positives, before and after the project rename. The work items are those
of `closeout-r13-workflow.js`, verbatim from `VERIFY.md`.

## 1. B2.2 — grub corridor to the shaft flat — CLOSED

**Source change (`cad/dispenser.py`, pocket-disc section):** the Ø2.6
thread-forming pilot was `Pos(6.0, …) * Cylinder(GRUB_PILOT_R, 6.5)` → spans
r 2.75…9.25, flooring 0.200 mm OUTBOARD of the bore flat at r = 2.55. Now
`Pos(5.85, …) * Cylinder(GRUB_PILOT_R, 6.8)` → spans **r 2.45…9.25**.

**Chosen depth r = 2.45, and why:** 0.10 mm inboard of the flat, so the pilot
breaks fully through the flat web at any ±0.05 print tolerance and the M3 cup
point lands on steel, never on CF-PETG. Inboard of the flat plane is bore void
(the D-bore removes everything outboard of r 3.05 round / x 2.55 flat in the
D-cut band), so the 0.10 mm overshoot cuts nothing structural. Outer end
unchanged (overlaps the Ø3.4 clearance channel at r 9.0…9.25, as before).

**Checker re-anchor (same file, B2 check block):** the Ø0.7 corridor ray began
at `np.arange(3.4, DISC_R, …)` — outboard of both the flat (2.55) and the old
pilot floor (2.75), which is why six rounds printed "NOWHERE — continuous
void" over a solid web. It now begins at `BORE_FLAT_R` (2.55). r13 build
output, verbatim:

```
grub corridor, Dia0.7 ray from the bore FLAT (r=2.55) to the disc OD along theta=202.5: blocked at r = NOWHERE -- continuous void (r12 anchored this ray at 3.40 and missed the 2.55..2.75 web; r6: solid 10.60..24.47)
```

**Independent verification (`cad/verify_r13_closeout.py`, OCP booleans on the
exported STEPs — not the in-session solids), verbatim:**

```
pocket_disc_r13.step (STEP volume 72.685 cm3)
  Dia0.7 corridor r=46.5 -> r=2.55 : disc material = 0.0000 mm3
  Dia1.9 corridor r=46.5 -> r=2.55 : disc material = 0.0000 mm3
  Dia2.6 corridor r=46.5 -> r=2.55 : disc material = 0.0000 mm3

pocket_disc_r12.step (STEP volume 72.686 cm3)   [FAILING CONTROL]
  Dia0.7 corridor r=46.5 -> r=2.55 : disc material = 0.0770 mm3
  Dia1.9 corridor r=46.5 -> r=2.55 : disc material = 0.5671 mm3
  Dia2.6 corridor r=46.5 -> r=2.55 : disc material = 1.0619 mm3
```

The r12 control reproduces VERIFY.md §B2.2's numbers to four decimals
(1.0619 = π·1.30²·0.200 exactly), so the probe demonstrably sees the web the
old checker missed. A probe reading 0.0000 on r12 would be broken.

**Flat-arc metric consequence (by design, not a regression):** with the pilot
correctly through the flat, the B2 bore sweep reads 0° of flat inside the grub
band (the Ø2.6 footprint at r=2.55 subtends ~61°, wider than the 50° flat).
The metric now requires ≥25° at every height OUTSIDE the band
(`|z − Z_SETSCREW| ≤ GRUB_PILOT_R`), asserts on it, and prints the in-band 0°
with its reason. r13 verbatim:

```
bore radius swept at 5 deg x 12 heights over the 13.5 mm D-cut engagement: round part 3.05 +/- 0.136 mm, FLAT part 2.63 +/- 0.076 mm over a contiguous 50 deg arc at every height OUTSIDE the grub band (need >=25 deg at r=2.55+/-0.05; r6 measured r=3.06 at ALL angles and both heights); inside the grub band (|z--341.25| <= 1.30) the flat reads 0 deg because the Dia2.6 pilot breaks through it to the shaft (close-out B2.2, by design)
```

Torque is unaffected: the flat carries it over the remaining ~10.9 mm of the
13.5 mm D-cut engagement at the full 50° arc; the grub is axial retention only.

## 2. B3.4 + BOM strings — moved into the source tables — CLOSED

All four 2026-08-08 hand-patched strings now originate in `dispenser.py`'s
COTS table, so regeneration keeps them (BOM.md regenerated this build, header
tag r13):

- **geared stepper:** 350 g NET carried with the honest caveat (vendor
  catalogue class, never on a scale; closure is to weigh one). The r12 string
  ("310 g NET is an ASSUMPTION") is gone from source.
- **gearbox output boss (NEW row):** pilot bore stated as modelled
  Ø16.20 (derived `2*MOTOR_PILOT_R + 0.20`), Ø26 bolt circle datasheet-cited,
  boss diameter explicitly ASSUMPTION → caliper-check before printing the plate.
- **count windows x4:** Ø5.90 × 0.95 (modelled size), with the note that
  ELECTRONICS ECO-4 still says Ø6 × 1.0 and needs amending.
- **PTFE washer:** Ø38 OD / Ø34 ID × 1.4, now DERIVED from `WASH_RI/WASH_RO`
  in the f-string so it cannot drift from the modelled washer again.
- **set screw:** row carries the close-out note (pilot floor r 2.75 → 2.45);
  the standing "DO NOT PRINT THE DISC YET" warning is retired with B2.2.

Adjunct found while regenerating: the COTS mass map keyed `"stepper"` against
a row named `"geared stepper"`, so the single largest COTS mass printed blank
in every generated BOM through r12. Key fixed; the 350 g now lands in the mass
column from `parts["stepper"]["mass"]`.

## 3. B7.1 — published fill/support numbers — already closed, no edit

VERIFY.md's own conclusion: the README RT row, DESIGN §fill/support and notes
§9 already state the measured plateau values (release 3.25–10.50° into the
index, separation 6.690–10.701 mm, lateral 0.126 m/s) and label it "a recorded
plateau, not a closure". Checked against the current files — still true.
Nothing to change; B7 remains a recorded plateau by punch-list rule.

## 4. B6.5/B6.6 — ground/prop clearance — UNVERIFIABLE WITHOUT INPUT (open)

Re-searched both checkouts 2026-08-10:
`~/projects/project-quiver/src/quiver/airframe_structure/landing_gear/steps/`
and `/tmp/pq-main/...` contain only `1340_tube_joint.step` and
`vendor/1330_main_adapter.step` — no full gear or airframe assembly exists to
measure against. Recorded as unverifiable-without-input per the work item;
README §clearance row already carries the "build-notes-carried until
re-checked against the real gear" caveat. Needs: real landing-gear/airframe
STEPs (or calipers on the aircraft).

## 5. Exports, integrity, renders

Full rebuild r13 (three runs: geometry, checker-metric wording, BOM mass-map
key — identical geometry throughout, verified by identical volumes). Zero
assertion failures. Export integrity, independent (trimesh + OCP on the
files): **15/15 r13 STEP/STL pairs watertight, STEP-vs-STL volume delta
≤ 0.053 %** (worst: agitator). Full table in `/tmp/r13_verify_final.log` and
reproducible via `cad/verify_r13_closeout.py`.

Renders regenerated with r13 geometry under the build's standard
`v1r6_*.png` names (the script's fixed render names; not renamed to v1r7 to
avoid diverging from the build system).

## 6. What r13 does NOT change

Mechanism, pockets, envelope, electronics, masses (except the BOM mass-column
fix above): untouched. `pocket_disc` volume 72.686 → 72.685 cm³ (−1.06 mm³ =
the corridor material removed). No other part's geometry differs from r12.
