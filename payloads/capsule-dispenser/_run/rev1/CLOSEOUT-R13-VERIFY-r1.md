GRANULE-METERING DISPENSER — CLOSEOUT R13, fresh-eyes verification round 1
Date: 2026-08-10. Verifier: fresh-eyes agent, round 1; has NOT read any r13 build round.

================================================================================
0. BLOCKING PRECONDITION — THE r13 EXPORTS DO NOT EXIST
================================================================================
This run is defined as: measure cad/exports/*_r13.* directly with my own OCP /
trimesh code and close each VERIFY item against MY numbers. There are no r13
export files. No item can be verified, because the subject of verification is
absent. I did not fabricate numbers, did not substitute the r12 baseline for r13,
and did not narrate build-note claims as measurements.

Evidence (my own commands):

  $ ls cad/exports/*_r13.*
  zsh: no matches found: cad/exports/*_r13.*        (exit 1)

  $ ls cad/exports/ | grep -c r13
  0

  $ ls cad/exports/ | grep -oE 'r[0-9]+' | sort -t r -k2 -n | uniq | tail -5
  r8
  r9
  r10
  r11
  r12          <-- newest export tag physically present is r12

  $ find /Users/hex/projects/payload-systems -name '*r13*'
  .../_run/rev1/r13-watchdog.sh
  .../_run/rev1/closeout-r13-workflow.js   <-- only orchestration scripts carry
                                               the r13 tag; NO geometry files

The only r13-named artifacts in the whole repo are the two orchestration scripts
(r13-watchdog.sh, closeout-r13-workflow.js, both dated 2026-08-10). No STEP, no
STL. The r13 build / regeneration round this verification is meant to close never
wrote any exports. The shipped baseline remains r12 (dispenser_r12_assembly.*,
written 2026-08-08 00:07).

My toolchain IS working (so the obstruction is the missing files, not me):

  python3 -> /Library/Developer/CommandLineTools/usr/bin/python3
  trimesh 4.12.2
  OCP ok

OCP/OpenCascade booleans and trimesh watertightness/volume checks import and run
cleanly. The instant r13 exports exist, every item below can be measured. Until
then, none can — and per this run's rules I may not read/run cad/dispenser.py or
the project verify scripts to synthesise a substitute (I did not).

================================================================================
1. PER-ITEM STATUS — EVERY CLOSE-OUT ITEM IS OPEN / BLOCKING (NO r13 GEOMETRY)
================================================================================
Each item needs an r13 export that is not on disk. I record the exact check thenext round should run once r13 exists, plus the r12-baseline result (from the
prior fresh-eyes pass in VERIFY.md, which was measured on r12) for comparison.

B2.2 — grub corridor void. NOT RUN (pocket_disc_r13.step absent). BLOCKING.
  Planned: OCP exact boolean of a coaxial Ø2.6 corridor on the grub axis
  (θ=202.5°) from r=46.5 to the shaft FLAT at r=2.55 vs pocket_disc_r13.step —
  disc material must be 0.0000 mm³; also sweep Ø0.7 and Ø1.9. r12 baseline
  FAILED (Ø2.6 -> 1.0619 mm³, a 0.200 mm closed CF-PETG web; Ø0.7 -> 0.0770;
  Ø1.9 -> 0.5671 mm³). This is the headline blocker r13 was meant to fix.

B3.4 + BOM strings. NOT RUN (no r13 geometry to anchor strings to). BLOCKING.
  Planned: measure r13 gearbox pilot-bore diameter; confirm cad/BOM.md states it
  with a source/ASSUMPTION line and that the corrected strings (PTFE washer
  size, grub size, pilot-bore) match r13 geometry AND originate in dispenser.py
  source tables (the one permitted dispenser.py read, only after numbers lock).
  r12 baseline: pilot bore Ø16.20 not stated in BOM (FAIL); PTFE washer BOM
  Ø30/Ø24×1.5 vs modelled Ø38/Ø34×1.4 (FAIL). Cannot re-check without r13.

B7.1 — README/docs fill & support numbers. NOT RUN (no r13 fill/support geom). BLOCKING.
  Planned: measure r13 hopper usable volume / pellet count and the support
  (release-window) geometry, compare to published README/DESIGN numbers. r12
  baseline: README 963 cm³ -> 422 pellets vs BOM 962 cm³ -> 421 (cosmetic drift);
  B7 support was a recorded plateau. Cannot re-check without r13.

B6.5 / B6.6 — ground & propeller clearance vs airframe STEPs. NOT RUN. BLOCKING
  (but of the confirmed-absent-input kind: open-but-nonblocking-for-this-run per
  the task rule, IF the airframe STEPs are genuinely absent). Two-part status:
   (a) r13 assembly geometry absent -> cannot place the payload stack.
   (b) The airframe STEPs the r12 verifier cited were already absent: the prior
       pass recorded that .../landing_gear/steps/ held only 1340_tube_joint.step
       plus a vendor/ folder, no full gear/pr