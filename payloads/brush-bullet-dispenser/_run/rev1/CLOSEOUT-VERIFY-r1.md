# CLOSE-OUT VERIFY — round 1 (2026-08-08)

Fresh-eyes verifier; has not seen any close-out build round. Every number below is
from my own OCP/trimesh code run against files in `cad/exports/` — I did not read
or run `cad/dispenser.py` or any project `verify_*.py`.

## 0. Headline: THE FIX PHASE PRODUCED NOTHING — there is no r13 to verify

The round fails before any geometry question is reached:

- `find /Users/hex/projects/payload-systems -name "*r13*"` returns **zero files**.
  `cad/exports/` ends at tag **r12** (newest files 2026-08-08 00:07).
- No `BUILD-NOTES-closeout-r1.md` exists in `_run/rev1/`.
- `git status` on branch `brush-bullet-dispenser` shows a clean tree except the
  two workflow scripts themselves (`closeout-watchdog.sh`, `closeout-workflow.js`,
  both untracked). `cad/dispenser.py`, `cad/BOM.md`, `README.md`, `docs/DESIGN.md`
  are all unmodified since commit `f2a9451` (2026-08-08 02:13, the rev-1 packaging
  commit). No renders `v1r7_*.png` were produced.

So no builder ran (or it died without writing anything). Everything below is my
measurement of the **shipped r12 baseline**, to state precisely what remains open.

## 1. B2.2 — grub corridor to the shaft flat — **STILL OPEN (blocking)**

My own exact OCP booleans on `cad/exports/pocket_disc_r12.step` (grub axis
θ = 202.5°, Z = −341.25; corridor from r = 46.5 inward), verbatim output:

```
disc volume = 72.686 cm3
  Dia0.7 corridor r=46.5 -> r=2.55 (flat): disc material = 0.0770 mm3
  Dia1.9 corridor r=46.5 -> r=2.55 (flat): disc material = 0.5671 mm3
  Dia2.6 corridor r=46.5 -> r=2.55 (flat): disc material = 1.0619 mm3
  Dia2.6 corridor r=46.5 -> r=2.75:        disc material = 0.0000 mm3
```

Identical to VERIFY.md §B2.2 to four decimals (1.0619 mm³ = π·1.30²·0.200: a
full-section 0.200 mm web between the pilot floor at r = 2.750 and the shaft flat
at r = 2.550). Requirement is 0.0000 mm³ at Ø2.6 down to r = 2.55. **Not fixed;
no r13 disc exists.** The checker re-anchor (probe ray at the flat r = 2.55, with
the r12 disc as a failing control) was also not done — `cad/dispenser.py` and the
verify scripts are untouched per git.

## 2. B3.4 + BOM strings — **strings are correct on r12, but this was already true
before this run; the source-table fix was NOT done**

`cad/BOM.md` was hand-corrected at rev-1 *packaging* (commit `f2a9451`, before
this close-out run), and its own header warns: *"`cad/dispenser.py` still emits
the old strings — the next regeneration will re-introduce all four unless the
source tables are fixed first."* The close-out work item was to reconcile the
source; git shows `dispenser.py` unmodified, so the corrections remain
regeneration-fragile hand-patches. I spot-checked each corrected string against
my own r12 measurements:

- **Pilot bore (B3.4):** BOM row 36 states Ø16.20 (with the boss-diameter
  ASSUMPTION flagged). My probe — Ø0.2 vertical columns through the flange band
  Z −355.25…−351.25 on `retaining_plate_chute_r12.step`, at θ = 0/90/180/270°
  (full column = 0.1257 mm³):

  ```
  r=7.50 : 0.0000   r=8.00 : 0.0000   r=8.05 : 0.0247   r=8.10 : 0.0630
  r=8.15 : 0.1012   r=8.20 : 0.1257   r=8.50 : 0.1257     (all four angles equal)
  ```

  Half-material at r = 8.10 → bore edge r = 8.10 → **Ø16.20 confirmed**. String
  matches geometry.
- **Count windows:** BOM says Ø5.90 × 0.95. My per-body extents on
  `count_windows_r12.stl`: 4 bodies, each **5.900 × 0.950 × 5.898**, centres
  (29.00, ±11.47, −392.25) and (35.00, ±11.47, −398.25) → inner faces
  |y| = 11.000. String matches geometry.
- **PTFE washer:** BOM now Ø38/Ø34 × 1.4 (was Ø30/Ø24 × 1.5). Consistent with the
  assembly washer solid VERIFY.md measured; I did not re-extract it this round.
- **Stepper mass:** BOM row now 350 g, matching ledger/README. String reconciled.

Verdict: the four strings are true of r12, but the close-out item (fix the source
so regeneration doesn't undo them) is **not closed**, and there is no r13 BOM
regeneration to test.

## 3. B7.1 — published fill/support numbers — **docs match measured geometry
(also already true at packaging); no r13 to re-check**

README lines 150–151/182 and DESIGN lines 406/419–422/1101–1103 state the
plateau with the original verifier's measured numbers: release **3.25–10.50°**
into the 22.5° index, separation **6.690–10.701 mm** vs the ≤ 1.0 mm requirement,
lateral **0.126 m/s**, explicitly labelled "a recorded plateau, not a closure".
My own r12 geometry inputs agree: exit-port void at y = 0, Z = −352.5 spans
**x = 24.00…40.00 (Ø16.00, centre x = 32.00)**; chute bore below it
**x = 21.05…43.00 (Ø21.95 ≈ 22.0)** at Z = −354.5/−360/−365. The docs are
honest against geometry I measured. But this was the state of commit `f2a9451`;
the close-out round added nothing and there is no r13 fill/support geometry.

## 4. B6.5/B6.6 — ground/prop clearance — **STILL NOT VERIFIED (blocking)**

The builder cited no airframe STEPs (no build notes exist), so there is nothing
for me to re-measure against. I checked the plausible source myself:
`/Users/hex/projects/project-quiver/src/quiver/airframe_structure/landing_gear/steps/`
contains only `1340_tube_joint.step` and `vendor/1330_main_adapter.step` — no
gear-leg/tube solids as STEPs (the legs appear to be generated by
`landing_gear/assembly.py`, which is outside what I can independently measure
without placement transforms). Propulsion vendor STEPs exist
(`equipment/propulsion/steps/vendor/3111_motor.step`, `3112_propeller.step`,
`3122_propeller.step`). The item remains exactly where VERIFY.md left it:
carried numbers (129.4 / 103.63 / 152.55 / 232.63 mm) are **unverified**, and the
stack bottom at Z = −418.45 (247.4 mm below the mount plane) still deserves a
real gear check before flight.

## 5. Regression gate — **cannot run (no r13); r12 baseline re-confirmed intact**

- Watertightness + STEP-vs-STL volume on r13: **no files**. (Baseline reference:
  VERIFY.md §B10's 15/15 + assembly, which I did not re-run this round.)
- Roof-slot march at θ = 310°, `meter_housing_r12.stl`, march down from
  Z = −326.25 in 0.02 mm steps:

  ```
  r=20.5..46.5 (8 radii): 9.000 mm at every radius
  ```

  Full-thickness roof at the old bug angle — baseline intact.
- Fragment-jam spot term — brush nose gap above disc top (Z = −336.75), first-hit
  ray from below on `brush_holder_r12.stl`:

  ```
  theta=140/145/150, r=22..46.5 (7 radii): 1.500 mm everywhere
  ```

  Equals min roof clearance 1.500 mm — baseline B8 intact.

## 6. Verdict — **FAIL**

Blocking:

1. **No r13 exports exist** — the Fix phase produced no artifacts at all (no
   exports, no build notes, no source changes, no renders). Nothing to verify.
2. **B2.2 open**: the 0.200 mm web across the grub pilot is still in the shipped
   disc (my booleans: 0.0770 / 0.5671 / 1.0619 mm³ at Ø0.7/Ø1.9/Ø2.6 to r = 2.55);
   the checker re-anchor was not done.
3. **BOM/doc corrections are hand-patches only**: `dispenser.py` source tables
   were not reconciled, so regeneration re-introduces the four bad strings
   (BOM's own header says so).
4. **B6.5/B6.6 still unverified**: no builder citation of airframe STEPs; gear-leg
   solids not present as STEPs at the project-quiver path I checked.

Closed by my measurement (state carried from the r12 packaging commit, not from
this round's builder): BOM strings vs geometry (Ø16.20 pilot bore, Ø5.90 × 0.95
windows, washer, 350 g stepper) and B7.1 doc numbers vs geometry. Round 2 must
start with an actual build: fix the pilot depth + checker anchor + source tables
in `dispenser.py`, export r13, and run the clearance study, then I can verify.
