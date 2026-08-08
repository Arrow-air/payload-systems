# CLOSE-OUT VERIFY — round 2 (2026-08-08)

Fresh-eyes verifier; has not seen any close-out build round. Every number below is
the printed output of my own OCP/trimesh code run against files in `cad/exports/`.
I did not read or run `cad/dispenser.py` or any project `verify_*.py`.

## 0. Headline: the round-2 Fix phase ALSO produced nothing — there is still no r13

- `find /Users/hex/projects/payload-systems -name "*r13*"` → **zero files**.
  `cad/exports/` ends at tag **r12** (newest 2026-08-08 00:07).
- No `BUILD-NOTES-closeout-r1.md` or `BUILD-NOTES-closeout-r2.md` exists in
  `_run/rev1/` — there are no builder claims for me to test at all.
- `git status` on `brush-bullet-dispenser`: clean except three untracked run
  artifacts (`CLOSEOUT-VERIFY-r1.md`, `closeout-watchdog.sh`,
  `closeout-workflow.js`).
  `git diff --stat HEAD -- README.md docs/DESIGN.md cad/BOM.md cad/dispenser.py`
  → **empty**. `cad/dispenser.py` mtime 2026-08-08 00:07 (the r12 export run).
- No `v1r7_*.png` renders (`cad/renders/` newest: `v1r6_*.png`, 00:27).
- `find <package> -newer closeout-workflow.js` outside `_run/rev1/` → **nothing**.

So neither close-out fix round ran (or both died before writing a single byte).
Everything below is my own measurement of the shipped **r12 baseline**, run so the
open/closed state is established by measurement rather than carried forward.

## 1. B2.2 — grub corridor to the shaft flat — **STILL OPEN (blocking)**

My exact OCP booleans on `cad/exports/pocket_disc_r12.step` (no r13 disc exists);
coaxial corridor on the grub axis θ = 202.5°, Z = −341.25, from r = 46.5 inward.
Verbatim output:

```
disc volume = 72.686 cm3
  Dia0.7 corridor r=46.5 -> r=2.55 : disc material = 0.0770 mm3
  Dia1.9 corridor r=46.5 -> r=2.55 : disc material = 0.5671 mm3
  Dia2.6 corridor r=46.5 -> r=2.55 : disc material = 1.0619 mm3
  Dia2.6 corridor r=46.5 -> r=2.75 : disc material = 0.0000 mm3
```

Requirement: **0.0000 mm³ at Ø2.6 down to the flat at r = 2.55**. Measured
1.0619 mm³ = π·1.30²·0.200 — the full-section 0.200 mm web between the pilot
floor (r = 2.750) and the shaft flat (r = 2.550) is still in the shipped disc,
identical to VERIFY.md §B2.2 and CLOSEOUT-VERIFY-r1 §1 to four decimals. The
checker re-anchor (probe at the flat, r12 disc as failing control) was also not
done — `dispenser.py` and the verify scripts are untouched per git. **NOT CLOSED.**

## 2. B3.4 + BOM strings — strings verified correct against my geometry, but they
are the pre-existing packaging hand-patches; the source-table fix was NOT done

`cad/BOM.md` is unmodified since commit `f2a9451` and its own header still warns:
*"`cad/dispenser.py` still emits the old strings — the next regeneration will
re-introduce all four unless the source tables are fixed first."* The close-out
work item was to reconcile the source; git shows `dispenser.py` unmodified.
**NOT CLOSED** as a work item. String-by-string against my own r12 measurements:

- **Pilot bore (B3.4):** BOM row 36 states **Ø16.20** with the Ø26 bolt circle
  cited to the 14HS13-0804S-PG5 datasheet and the boss diameter flagged as an
  ASSUMPTION to be caliper-checked. My Ø0.2 OCP columns through the flange band
  Z −355.25…−351.25 on `retaining_plate_chute_r12.step` (full column = 0.1257 mm³),
  all four angles θ = 0/90/180/270° equal:

  ```
  r=7.50 : 0.0000   r=8.00 : 0.0000   r=8.05 : 0.0247   r=8.10 : 0.0630
  r=8.15 : 0.1012   r=8.20 : 0.1257   r=8.50 : 0.1257
  ```

  Half-material at r = 8.10 → bore edge r = 8.10 → **Ø16.20 confirmed**. Bonus
  regression: Ø0.4 × 4.5 columns at the four gearbox bolt centres (±13,0)/(0,±13)
  all read **0.0000 mm³** — the Ø26-on-axes bolt pattern is intact.
- **Count windows:** BOM says **Ø5.90 × 0.95**. My per-body extents on
  `count_windows_r12.stl`: 4 bodies, each **5.900 × 0.950 × 5.898**, centres
  (29.00, ±11.475, −392.25) and (35.00, ±11.475, −398.25), inner faces
  **|y| = 11.000**. Matches.
- **PTFE washer:** BOM says **Ø38 OD / Ø34 ID × 1.4**. My extraction of the washer
  body from `dispenser_r12_assembly.stl`: bbox ±19.000, Z −352.200…−350.800
  (**1.400 thick**), volume **316.5 mm³**; radial material scan at Z = −351.50
  from r = 17.05 to 18.95 → **ID Ø34.10 / OD Ø37.90** on the faceted mesh
  (STEP nominal Ø34/Ø38). Matches; the old unbuildable Ø30/Ø24 × 1.5 is gone.
- **Stepper mass:** BOM row 35 carries **350 g** matching the ledger/README, with
  the "never been on a scale" caveat. Reconciled.
- **Grub:** one **M3×4 cup-point** grub, stated once in each table, 1.5 mm key,
  and an explicit **"DO NOT PRINT THE DISC YET"** warning quoting the same
  0.0770/0.5671/1.0619 mm³ numbers I measured. Honest.

Verdict: all corrected strings are true of the r12 geometry (my measurement), but
this was already the state at commit `f2a9451`; the close-out round contributed
nothing, and the corrections remain regeneration-fragile.

## 3. B7.1 — published fill/support numbers — docs match my measured geometry
(also pre-existing state; no r13 to re-check)

README lines 150–151/182 and DESIGN lines 406/419–422/439/1100–1107 state the
plateau with measured numbers: release **3.25–10.50°** into the 22.5° index,
separation **6.690–10.701 mm** vs the ≤ 1.0 mm requirement, lateral **0.126 m/s**,
labelled "a recorded plateau, not a closure". My own r12 geometry inputs are
consistent with those numbers:

```
exit-port void scan on retaining_plate_chute_r12 (y=0):
  z=-351.45 : void x = 23.50 .. 40.55  (dia 17.05, centre 32.03)   [chamfer mouth]
  z=-352.50 : void x = 24.00 .. 40.00  (dia 16.00, centre 32.00)   [port bore]
  z=-354.50 / -360.00 / -365.00 : void x = 21.05 .. 43.00 (dia 21.95, centre 32.03)
pocket_disc_r12 void arcs at r=32, z=-343.75: 8 pockets, each 26.9-27.0 deg
park separation 2*32*sin(11.25 deg) = 12.486 mm
```

Exit port Ø16.00 at PCD 32, chute bore Ø21.95, 8 × 27° pockets, 12.49 mm park
separation — the same inputs VERIFY.md derived the plateau from. Docs are honest
against geometry I measured; unmodified since HEAD; **no r13 fill/support
geometry exists to verify**.

## 4. B6.5/B6.6 — ground/prop clearance — **STILL NOT VERIFIED (blocking)**

There are no build notes, so the builder cites no airframe STEPs. I searched both
plausible checkouts myself:

- `/Users/hex/projects/project-quiver/src/quiver/airframe_structure/landing_gear/steps/`
  → only `1340_tube_joint.step` + `vendor/1330_main_adapter.step`
- `/tmp/pq-main/src/quiver/airframe_structure/landing_gear/steps/` → identical two files
- `find /tmp/pq-main /Users/hex/projects/project-quiver -iname "13*.step"` → those
  same four paths only; the assembly-guide model folder
  (`/tmp/pq-main/docs/Manufacturing/Assembly-Guides/assets/models/structural/`)
  has no 13xx gear parts either.

No gear-leg solids exist as STEPs, so a mesh-to-mesh clearance measurement is not
reproducible from exported geometry. The carried numbers (ground 129.4 mm,
payload↔gear 103.63 mm, prop vertical 152.55 mm, in-plan 232.63 mm) remain
**unverified**; my own measured assembly bottom is **Z = −418.450** (247.400 mm
below the mount plane, max Z = −171.050 — from `dispenser_r12_assembly.stl`).

## 5. Regression gate — cannot run on r13 (no files); r12 baseline re-measured intact

My trimesh watertightness + my OCP STEP volumes, all 15 part exports of the
newest tag (r12), verbatim:

```
part                         watertight   bodies     STLcm3    STEPcm3   diff%
agitator_r12                       True        1      4.288      4.291  0.053%
bay_lid_r12                        True        1      8.598      8.598  0.001%
brush_holder_r12                   True        1      3.544      3.544  0.001%
chute_plug_r12                     True        1      6.718      6.721  0.037%
count_windows_r12                  True        4      0.104      0.104  0.041%
electronics_bay_r12                True        1     21.175     21.175  0.002%
fill_cap_r12                       True        1      7.545      7.548  0.034%
hopper_r12                         True        1    109.423    109.419  0.004%
meter_housing_r12                  True        1    103.819    103.856  0.035%
pocket_disc_r12                    True        1     72.661     72.686  0.034%
retaining_plate_chute_r12          True        1     63.945     63.960  0.023%
sensor_boards_r12                  True        2      1.287      1.287  0.012%
sensor_cover_r12                   True        2      3.198      3.198  0.000%
service_stand_r12                  True        1    103.892    103.908  0.015%
top_plate_r12                      True        1     95.550     95.572  0.023%
gate: PASS        (assembly: 24 bodies, 579.90 cm3, maxZ -171.050, minZ -418.450)
```

15/15 watertight, STEP-vs-STL ≤ 0.053 % (limit 1 %). Roof-slot march at the old
bug angle, `meter_housing_r12.stl`, 0.02 mm steps down from Z = −326.25:

```
theta=310 : 9.000 mm at all 8 radii (20.5, 24.5, 30, 32, 36, 39.5, 44, 46.5)
theta=305 / 315 : 9.000 mm at all 8 radii
```

Fragment-jam spot term — brush nose underside above disc top (Z = −336.75),
first-hit rays on `brush_holder_r12.stl`:

```
theta=140/145/150, r=22..46.5 (7 radii): 1.500 mm everywhere
```

Nose gap 1.500 mm = min roof clearance 1.500 mm — B8 baseline intact. No
regression anywhere, because nothing changed.

## 6. Verdict — **FAIL**

Blocking (all four are the same items round 1 flagged, untouched):

1. **No r13 exports exist** — the round-2 Fix phase, like round 1's, produced no
   exports, no build notes, no source changes, no renders. There is nothing to
   verify against the close-out acceptance tests.
2. **B2.2 open by my measurement**: 0.200 mm full-section web across the Ø2.6 grub
   pilot on the shipped disc (0.0770 / 0.5671 / 1.0619 mm³ at Ø0.7/Ø1.9/Ø2.6 to
   r = 2.55; 0.0000 at r = 2.75). Checker re-anchor not done.
3. **BOM/doc corrections remain hand-patches**: `dispenser.py` source tables not
   reconciled (git-clean since `f2a9451`); the BOM's own header says regeneration
   will re-introduce all four bad strings.
4. **B6.5/B6.6 still unverified**: no builder citation exists; no gear-leg solids
   exist as STEPs in either project-quiver checkout (only `1340_tube_joint.step`
   and `vendor/1330_main_adapter.step`).

Closed by my measurement, on the r12 baseline (state inherited from the packaging
commit, not from any close-out builder): BOM strings vs geometry (Ø16.20 pilot
bore, Ø5.90 × 0.95 windows, Ø38/Ø34 × 1.4 washer, 350 g stepper, single M3×4
grub), B7.1 doc numbers vs geometry, and the full regression gate on r12
(watertightness, volume agreement, roof at θ = 310, nose gap). **r12 stays the
shipped tag.** The fix work itself — pilot depth, checker anchor, source tables,
clearance study, r13 export — has not been started; the close-out cannot close
until a builder actually runs.
