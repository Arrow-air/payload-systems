#!/usr/bin/env python
"""
Capsule Dispenser -- "pocket-wheel" concept, rev-1 round 6 (export tag r12).

REV-1 ROUND-6 changes (against _run/rev1/CRITIQUE-r5.md; mechanism unchanged):
  integration BLOCKING I-1  the cartridge harness duct (bay -> motor, bay ->
      both count boards) was SOLID PRINTED MATERIAL on every leg -- 63/63,
      187/187, 261/261, 205/205, 109/109, 197/197, 43/43 axis points inside
      material, largest conductor Dia0.0, and the part contained ZERO
      enclosed voids. ROOT CAUSE, found this round: the bores were FUSED
      into one solid `_bore` before `rp -= _bore`, and every leg of that
      fuse is an equal-radius cylinder meeting another equal-radius cylinder
      at 90 deg. BRepCheck_Analyzer reports the fused shape INVALID, and OCC
      answers a boolean against an invalid tool with an EMPTY result and no
      exception -- so the cut was a silent no-op, `rp.intersect(_bore)` read
      0.0 mm3, and the model's own coverage metric read 100 % (a solid rod is
      perfectly covered). Fixed by cut_each(): the bores are a LIST of
      primitives, each validity-checked and cut in turn, with a hard volume
      floor. A per-leg PATENCY test now runs on the exported mesh.
  assembly BLOCKING A-11  the M5 detent plunger had nothing to thread into
      (plain Dia5.199/Dia6.399 bore, no M5 insert anywhere in cad/BOM.md).
      Now a modelled Dia4.5 x 13.5 mm thread-forming pilot + Dia5.2 ball
      clearance, per punch-list B9c branch 1.
  assembly MAJOR A-12  bay-rib pilot floor was 27.7 % open into the metering
      chamber with 0.144 mm of floor where it was closed; the BOM'd M3x20 tip
      landed 0.850 mm past the bore wall, 0.187 mm from the rotating disc.
      Pilot floor -45.0 -> -46.5, screw M3x20 -> M3x18.
  granule-path MODERATE 1  two 2.2 x 5.0 mm cable-tie slots left 22.00 mm2 of
      the granule bed open to the sky at (+/-9, -66). Replaced with additive
      tie-down bridges; the 12-column tank-vent self-check is replaced by a
      0.5 mm grid scan over the whole barrel bore.
  count-sensor B4.2  the ECO-5 labyrinth stepped +0.800 mm in x on BOTH
      sides, so the clear lens sat at x = 29.400/35.400 and B4.2 read
      1.1932 mm3 on the ECO-3 axes. The step is now split -0.400 / +0.400.
  assembly MODERATE A-13 / integration N-i4  two driver rows (1.5 mm for the
      M3 grub, 2.0 mm for the countersunk gearbox screws); grommets, bay
      gasket cord and sensor pads are now ordered, not just reserved.

REV-1 ROUND-5 changes (against _run/rev1/CRITIQUE-r4.md; mechanism unchanged):
  integration BLOCKING  the aircraft-harness conduit was SOLID at the
      top-plate elbow: the r2 strain-relief boss was unioned on AFTER both
      conduit bores were cut, so it re-filled the junction (measured on
      top_plate_r10.stl: vertical bore axis solid over z -237.50..-225.00,
      horizontal bore axis solid over y -84.00..-72.00, largest conductor
      that could cross = Dia0.0). The boss is now unioned BEFORE the bores,
      and the square corner is replaced by an R8.0 swept elbow. Patency and
      coverage are MEASURED on the exported mesh, not rolled up from
      parameters -- the r10 "95.3 % covered" table is deleted, because a
      parameter roll-up is exactly what let a fully blocked conduit ship.
  assembly BLOCKING A-10  the BOM ordered `M3x8 SHCS` for a joint the plate
      countersinks (90 deg, mouth Dia6.10 -> Dia3.40). A Dia5.5x3.0 cap head
      measures 8.8652 mm3/screw static and 49.4066 mm3 swept against the
      pocket disc; the BOM now names M3x8 ISO 10642 / DIN 7991 with the
      measured grip, and the flat-head boolean is printed at all four holes
      and at every disc angle over a 45 deg spoke pitch.
  granule-path MAJOR  the r4 plug-tether anchor lug stood 1.000 mm INSIDE
      the Dia22 chute bore over a 6.0 x 8.0 mm patch and fouled the plug
      shank; the plug's Dia28 flange also drove 2 x 52.811 mm3 into the
      count-sensor boss below the chute mouth. Lug inboard face moved to the
      bore wall, flange clipped to |y| <= 10.8, and the plate ^ plug boolean
      is now printed DECOMPOSED BY BODY with the designed press fit named
      separately (r10 logged all 206.0993 mm3 as "the designed press fit").
  granule-path MODERATE 1  the "lift/push = cot(30) = 1.73" ramp credit is
      DELETED from the torque budget: for a rounded fragment first contact is
      the nose's leading bottom corner at 1.500 mm with lift/push 0.00. The
      argument that actually carries the requirement (stub + open-sump return
      + crush/shear backstop, with the crush forces) is printed instead.
  granule-path  reverse-stroke bound re-measured at r=24.5, not only at the
      PCD; entry-ramp angle published as a RANGE over radius, not "25 deg".
  N10  the sump-outlet plateau is re-measured (window edges bisected, area,
      equivalent orifice, agitator sweep fraction) and re-stated as a
      plateau, not a pass.
  integration nonblocking  prop clearance MEASURED against the real
      propulsion assembly instead of restating the r2 figures; N-i2
      (connector cannot follow the harness) answered with numbers and a
      stated assembly workflow; service_stand called out as required GSE.
  assembly nonblocking  NB-1 (inserts go in from below), NB-2 (flange screws
      are at r74.000, the BOM said r72.25), NB-4 (0.5141 deg of lash), NB-5
      (8.000 mm stand clearance), NB-7 (hex-key BOM row) all written down.

REV-1 ROUND-4 changes (against _run/rev1/CRITIQUE-r3.md; mechanism unchanged):
  B10 / A-8  every STL is now tessellated from the SHIPPED STEP (export_step ->
      import_step -> export_stl). r9 meshed the in-session OCC shape and put
      188 OPEN edges + 1538 three-face edges into retaining_plate_chute_r9.stl
      (+8.36 % volume) and into the assembly. A full edge-multiplicity census
      of every exported STL is printed and asserted.
  count-sensor BLOCKING 1  the emitter now fits the DRAWING, not a critique:
      TSAL6200 is 8.7 +/- 0.3 mm seating-plane-to-apex (Vishay 81010 rev 2.4),
      not 5.8. Board plane |y| 23.5 -> 26.5, boss face 27.5 -> 30.5; the
      datasheet package solid is booleaned at nominal AND at 9.0 mm.
      VBPW34FAS re-modelled as the SMD 6.4 x 3.9 x 1.2 part it is.
  A-9  bay->housing screws M3x12 -> M3x20: measured grip 13.9 mm gave 0.000 mm
      of engagement. Grip and engagement are now ray-measured on the exports.
  NB-2  hopper skirt tabs thickened 3.00 -> 4.05 mm so an M3x8 stops clamping
      instead of bottoming in a 4.1 mm pilot.
  B7  release sweep corrected: the seat offset is applied along the pocket->
      port CHORD (worst case), which reproduces the r3 critic's 3.25..10.50
      deg window and 7.25 deg spread instead of r9's 1.00 deg.
  B8.3  first-contact ray audit added: what a proud fragment actually strikes,
      with the face normal, instead of a silhouette measurement.
  granule-path M3  chute plug is tethered (Dia4 eye + printed anchor lug) and
      its sealed internal void is opened out.
  NB-1  4 board-locating ribs on the sensor cover (float +/-1.20 -> +/-0.20 mm).
  BOM  stop pin, sensor PCBs, window adhesive and the tether are orderable;
      the rolled-up mass leads with the shipped (slicer-realistic) basis.

REV-1 ROUND-2 changes (against _run/rev1/CRITIQUE-r1.md; mechanism unchanged):
  BUILD  three parts had been silently EATEN by booleans across r7/r7+ (top
      plate, then brush_holder via SEAT_KEEP/HOLD_KEEP built at z=0, 116 mm
      off station). Every part now passes _guard(): null shape or a volume
      below its floor is a hard failure, not a 0.81 cm3 export.
  A-2 harness duct rerouted X-first and dropped below the latch ring, so
      meter_housing ^ retaining_plate_chute = 0.0000 mm3 seated and 0.0000
      over a 60 mm descent at 20-24 deg of unlock.
  A-3 the bay's top entry is now a RISER SOCKET that the hopper conduit plugs
      down over (r7 left the conduit 3 mm short and fouling the lid flange by
      6.0 mm3 along the whole insertion path).
  A-4/B4  the ECO-4 window seat is cut from the BORE AXIS outward, so its
      mouth IS the bore surface: lip 0.0000 mm (r7: 0.610), clear aperture
      5.4972 mm2 = 68.4 % on BOTH beams (r7: 46.4 / 17.1), window insertion
      from the bore 0.0000 mm3 (r7: 5.2219).
  B4/B5  the duct is SYMMETRIC (both count boards routed, r7 routed one) and
      is built BEFORE the sensor cavities, so it can never refill them; both
      board insertion sweeps are 0.0000 mm3.
  ECO-12 new printed sensor_cover x2: 4 posts, 36 mm2 of clamp bearing, 2x M2
      into new boss ears, Dia5 grommeted cable port. r7 had NO retention.
  B10 14/14 part STLs watertight, 0 non-manifold edges, 0 inverted-normal
      bodies in the assembly (r7: plate not watertight, 4 bad bodies).
  MOD1 mirrored 45 deg recovery ramp at the sump window's theta=250 edge;
      nose trailing face ramped as far as the holder width allows (PARTIAL).
  B7  the "stationary release / zero lateral velocity / full port aperture"
      claim is WITHDRAWN and replaced by a measured release sweep.
  B12 the service stand's ground plane was ABOVE the motor can (the payload
      would have stood on its own gearbox); now 16.20 mm of clearance.
  N12 the Z-stack comments were 10.0 mm stale after r1 took NECK_H 42 -> 52;
      the audit is printed and asserted. N13 padded EDT + flat-plate control.
  B2.4 one grub size everywhere, string-equality asserted against BOM.md.

Concept: CONCEPT-pocket-wheel.md (winner per JUDGING.md). Frame: drone frame,
origin at airframe center, +Z up, +Y forward (ICD / mechanical README).
Payload top mounting plane at Z = -171 mm; the payload-side clip plate
(2112_attach_plate_payload_side.step) is part of this payload.

REV-1 ROUND-1 changes (against _run/rev1/PUNCHLIST.md; the mechanism is
unchanged -- pocket wheel as judged):
  B1  entry-ramp cut was a HALF-SPACE (`ramp_half & Box(400,200,100)` then
      Rot(Z=130)), so the 25 deg undercut was mirrored 180 deg away and cut a
      through-slot in the roof at theta=310 (RT-1: 0.000 mm roof there). The
      ramp is now a discretised HELICOID confined to theta 95.4..130: the
      ceiling height is a function of ANGLE (not of tangential distance), so
      the roof returns to full 9.00 mm section at every radius outside the
      ramp sector.
  B2  disc bore is now a D-BORE (flat at r=2.55 over the vendor's 12 mm
      D-cut) so the flat, not the grub, carries torque; and the grub screw
      has a modelled radial CORRIDOR from the disc OD to the bore plus a
      plugged access port through the chamber wall at theta=202.5.
  B3  motor pattern corrected to the datasheet 4 x M3 on a Dia26 bolt CIRCLE
      (+/-13,0),(0,+/-13); the pilot bore is reduced to Dia16.1 (explicit
      ASSUMPTION, see MOTOR_PILOT_R) so the web to the bolt holes is real,
      and the PTFE thrust washer moves outboard of the bolt circle.
  B4  count sensor rebuilt to ELECTRONICS.md 4.2-4.5: ECO-3 wide bosses, two
      Dia3.2 apertures per side at x=29/35, ECO-9 6 mm vertical stagger,
      ECO-4 bore-face PMMA window seats, ECO-5 lateral labyrinth.
  B5  electronics/wiring home (Thomas directive 2): board standoffs, three
      grommeted entries, a real lid gasket groove, and a MODELLED conduit
      run (neck -> top-plate tube -> hopper-side tube -> bay, plus a
      cartridge duct) with the harness swept as solids and booleaned against
      the pellet space.
  B6  attachment-interface reach-in (Thomas directive 3): the clip plate now
      stands off on a 42 mm hollow NECK (48 x 48 plan) integral with the top
      plate; corridor boxes are measured, not asserted.
  B7  exit port reduced Dia18 -> Dia16 (later release, better park margin);
      the release sweep is measured and the "stationary release" claim is
      corrected -- see the RELEASE SWEEP block.
  B8  deflector nose gap 3.00 -> 1.50 mm (= ROOF_CLEAR) so the rejection band
      covers the shear band; holder widened 13 -> 18 mm and moved to 148 deg
      to keep the 30 deg ramp inside the holder and clear of the roof entry.
  B9  mount-screw grip, hopper insert depth, detent thread (M5 heat-set
      insert boss) and bearing seat fit all reworked.
  B12 printed SERVICE STAND so the dispenser has a stable refill rest
      position off the aircraft; fill-cap removal measured in that pose.
  N2/N6/N7/N12/N13/N16/N17 folded in (see the checks).

Round-6 changes (fixing the r5 critics' BLOCKING issues, BUILD-NOTES-r5.md
"Round-5 critics"):
  interference BLOCKING -- "the 4 mount bolts land in the clip plate's
  blind-mate window, not in plate material":
    - the clip plate is now MAPPED, not assumed: a containment scan of the
      imported STEP finds the 4 real through-holes at (+/-19,+/-19) (Dia2.90),
      the 16 x 24 blind-mate shaft, the 4 PCB tabs at (+/-4,+/-10) (Dia1.90)
      and the Dia3.90 head-clearance column above each mount hole. The
      mounting pattern is DERIVED from that scan and asserted; the screws are
      M2 (the measured head pocket is Dia3.90) into heat-set inserts.
  interference BLOCKING -- "the blind-mate electrical interface cannot mate:
  35.0 mm Y offset":
    - the r5 pedestal at y=-35 is DELETED. The blind-mate PCB now sits where
      the vendor plate says it goes: centred in the 16 x 24 shaft on the
      plate's own 4x M2 tabs. The top plate carries a sealed PCB WELL under
      it (connector + service loop) and a cable channel out to the bay.
    - the fill port moved (0,40) -> (0,45) so the new mount holes clear the
      cap recess.
  pellet-path BLOCKING -- "the transfer-arc entry has NO relief geometry on
  the pellet-facing side; the 45-deg lead-in is cut into the wrong face":
    - the ramp is now cut into the roof UNDERSIDE as a true inclined plane
      (RAMP_DEG from horizontal, measured by a ceiling-profile probe at 7
      radii): the ceiling descends from the roof top to disc+ROOF_CLEAR over
      ~35 deg of arc. No square step anywhere on the entry.
  pellet-path BLOCKING -- "the constructed wedge jam is NOT defeated":
    - REJECTION: the wiper is re-architected -- compliant bristles LEAD, and
      a rigid 45-deg DEFLECTOR NOSE (the rotary-airlock "inlet shear
      deflector") trails them, reaching down to disc+NOSE_GAP so anything
      standing proud is pushed UP into the sump where there is an escape
      path, not into a close-clearance arc.
    - SHEAR BACKSTOP: the drive is now a 5.18:1 planetary-geared stepper.
      Two current settings give 0.20 N*m normal (6.2 N at the pocket lip,
      6.6x under the 41 N whole-pellet crush load, RESEARCH-drone-spreaders
      1.3) and 0.65 N*m recovery (20.3 N, 2.5x over the estimated worst
      wedged-sliver shear force, still 2x under whole-pellet crush).
    - the full torque budget (bed drag, agitator, detent, bearing) is printed.
  pellet-path BLOCKING/MAJOR -- "the rigid wiper holder leads the compliant
  bristles": bristle channel moved to the LEADING edge; contact order is
  measured by a swept probe at 5 fragment heights.
  pellet-path MAJOR -- "no torque budget, and the M5 detent needs 1-6x the
  motor's entire holding torque": the rim dimples are now shallow spherical
  seats (R6 x 0.6) with a specified light plunger; release torque computed.
  pellet-path MODERATE -- drop-window margin: the index is now TWO-PHASE
  (22.5 deg to the port, DWELL, 22.5 deg to park), so the pellet is released
  from a STATIONARY pocket -- zero tangential velocity, and the drop window
  is a dwell parameter instead of a kinematic race.
  buildability MODERATE -- the bushing PN could not be confirmed: replaced by
  igus JFM-2023-07 (ID20/OD23/L7), a catalogued length; roof thickened to
  suit (which also buys 3 mm of bristle trim).

Round-5 changes (fixing the r4 critics' blocking issues, BUILD-NOTES-r4.md
"Round 4 critics"):
  buildability BLOCKER -- "cartridge service removal is kinematically
  impossible" (agitator fingers 0.5 mm above a solid roof; swept descent
  1077 mm3):
    - the agitator NO LONGER RIDES ON THE CARTRIDGE. It is now a separate
      rotor that sits on the sump floor (housing roof), radially located by
      the disc hub and driven by a HEX SPIGOT on that hub. The cartridge
      (plate+chute+disc+motor+washer) drops straight out of the hex; the
      agitator stays in the hopper. Its set screw -- which r4 buried inside
      the funnel throat, unreachable with the hopper on -- is DELETED.
    - a real BEARING closes the "no bearings anywhere" GAP: an iglidur-class
      flanged sleeve bushing (ID20/OD22, flange Dia26) is seated in the roof
      bore, so the Dia92 disc is radially located 20 mm above the pellet bed
      instead of cantilevered off the stepper's internal bearings.
    - new harness family: FULL CARTRIDGE DROP-OUT SWEEP (unlock 22 deg, then
      20-step descent) of every cartridge member against every static part --
      the exact check r4 replaced with a Dia26.4 cylinder probe.
  pellet-path MAJOR -- "the wiper is a solid printed fin with no bristle
  retention feature", falsifying the compliance claim:
    - the wiper is now TWO parts: a printed holder with a real 1.8 x 1.0 mm
      bristle channel, and a COTS strip-brush insert (modeled). Measured
      free trim length and a [D] contact-stiffness comparison vs the r4
      solid fin are printed by the run.
  pellet-path MAJOR -- jam site unreachable / cartridge removal dumps the
  hopper: the wiper station is now exposed by the (working) cartridge
  drop-out, probed with rods from below; the drain-before-service procedure
  is measured (residual sump load) and written into BUILD-NOTES-r5.
  buildability MODERATE -- undisclosed sub-2 mm sections: rim/inner fines
  slots re-spaced (measured web), hopper fill-line GROOVES replaced by
  raised internal RIBS (wall no longer thinned), and an INWARD RAY-CAST WALL
  THICKNESS harness now measures min/p1/p5 wall on every exported part.
  pellet-path MODERATE -- 60 deg funnel is at/below the printed-PETG
  mass-flow threshold: funnel steepened to 68 deg (cylinder shortened so the
  stack barely moves); the agitator now sweeps the full sump floor.
  mass MODERATE -- ledger prices every part as 100% infill and the fill-line
  rationale had <1% margin: a measured VOXEL INFILL BRACKET (4 walls + 25%
  infill) is printed alongside the solid figure, the max fill line is
  re-solved against the pessimistic density AND the heavy-stepper case, and
  the >1.0 kg overage is attributed block-by-block.

Round-4 changes (fixing the r3 critics' blocking issues,
BUILD-NOTES-r3.md "Round-3 Critics"):
  pellet-path BLOCKER:
    - disc drive set screw moved from z=-268 (12.5 mm above the shaft top,
      5 mm above the hub bore -- zero torque transfer) to z = disc_top+4
      (-282), where the 5 mm motor shaft (-304.5..-280.5) is present.
      Engagement PROBED against the stepper solid, hole-open probed too.
  buildability BLOCKERS:
    - hopper->housing joint reworked: the 3 vertical funnel-tab screws sat
      directly under the 60 deg cone wall (no driver path, measured 44 mm3
      head-envelope obstruction). Replaced by 3 RADIAL skirt tabs hanging
      outside the housing wall (theta 30/105/225), M3 plastite driven
      HORIZONTALLY from outside; driver-path envelopes probed empty.
    - clip->top_plate hex nut pockets were sealed voids (0.4 mm floor
      skin). Bosses deepened to 5.6 and the hex cut now breaks through the
      boss bottom face: open-bottom insertion probed (skin band ~0 mm3),
      4.2 mm nut depth retained, >=5.9 mm web above the nut.
    - brush strip had no install/removal path (skirt below the closed-slot
      floor; 7 mm tab vs 1.4 mm slot). Outer wall now has a full-cross-
      section WINDOW (3.0 tall vs 2.65 brush section) at theta=133; the
      inner-ring groove stays a closed slot for the bar tip; the end tab
      seals the window from outside + keeps the radial M3 screw. The whole
      radial slide path is verified by a swept-union probe (brush is
      prismatic along the slide direction, so the union is exact).
    - electronics bay lid MODELED (r3 open issue 3 / MAJOR): -Y wall
      replaced by a 42x36 opening + screwed lid (4x M3 self-tap into
      corner-boss pilots, lip register, 2x Dia6 rib-driver access holes
      moved into the lid). Bay rib cheeks widened 1.9 -> 2.2 mm.
    - NEW HARNESS CHECKS (r3 root-cause: no insertion/tool-path checks):
      nut-insertion probes, screw driver-path envelope probes, brush
      slide-sweep probe, set-screw shaft-engagement probe.
  other r3 critic items:
    - leg clearance now measured mesh-to-mesh against the FULL landing
      gear built from the quiver source (incl. 1330 adapters), not just
      the tube axes (r3 over-report: 92.0 vs true 83.4).
    - dead dust ledge at chamber-wall top removed: fill-sector cut now
      stops at the chamber wall r47 and the 0.5 mm step under the funnel
      outlet gets a 45 deg chamfer ring (dust slides to the rim trough).
    - rim-trough fines slots extended to 3 arcs / ~85% of the circle
      (incl. the exit sector); bridges kept at the Hall cavities.
    - roof center pass-through opened Dia24->Dia27 so the agitator collar
      (Dia26) can drop out with the cartridge.
    - 450-pellet fill-line groove molded into the hopper wall (mass critic
      recommendation; z solved from the measured usable volume).
    - COTS candidates now carry real part numbers (ASSUMPTION-labeled).
    - two-in-chute exclusion printed as an explicit INTERFACE CONSTRAINT
      (min index period), per the pellet-path critic's NOTE.

Run with:  ~/.openclaw/workspace/venvs/dock-cad-314/bin/python dispenser.py
Outputs:   cad/exports/*_r12.step *.stl  cad/renders/v1r6_*.png  cad/BOM.md
Checker:   cad/verify_r4.py (INDEPENDENT: reads only the exports)
Prints:    geometry checks + mass ledger (measured from solids)
"""

import math
import os

import numpy as np
from build123d import (
    Axis, Box, Compound, Cone, Cylinder, Location, Polygon, Pos, Sphere,
    RegularPolygon, Rot, export_step, export_stl, extrude, import_step,
)

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR = os.path.join(HERE, "exports")
RENDER_DIR = os.path.join(HERE, "renders")
IFACE = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "interface", "mechanical"))
CLIP_PLATE_STEP = os.path.join(IFACE, "2112_attach_plate_payload_side.step")

# =====================================================================
# Parameters (mm, g).  All pellet-facing dims parametric on PELLET_D.
# =====================================================================
PELLET_D = 12.0            # verified ~12 mm (CONTEXT)
PELLET_D_MAX = 13.0        # ASSUMPTION +/-1 mm (CONTEXT)
PELLET_MASS = 1.18         # g, verified (CONTEXT)
PELLET_VOL_WORST = 2.28    # mL/pellet packed, barrel worst case (concept 3)
PELLET_VOL_SPHERE = 1.64   # mL/pellet packed, sphere basis (concept 3)

Z_MOUNT = -171.0           # payload top mounting plane (ICD / README)
Z_GROUND = -547.89         # tube axis -527.89 - foam 40/2 (landing_gear/assembly.py)

# clip plate (from STEP: 50 x 50 x 10.5).  r6: NOTHING here is assumed any
# more -- the four numbers below are the SEARCH SEED for the containment scan
# that maps the imported STEP (see "clip-plate map" further down). The r5
# model bolted to (+/-6.5,+/-10.5), which the r5 interference critic proved
# is inside the blind-mate window: those screws clamped air.
CLIP_T = 10.5
# B6.4: the ICD plane is -171.047 and r6 placed the clip face at exactly
# -171.000, leaving 0.0397 mm3 of payload above it. The whole payload is now
# dropped 0.05 mm so nothing is above Z = -171.05.
Z_CLIP_TOP = Z_MOUNT - 0.05
BOLT_DX_NOM, BOLT_DY_NOM = 19.0, 19.0     # expected mount pattern (38 x 38)
PCB_TAB_DX, PCB_TAB_DY = 4.0, 10.0        # expected PCB tab pattern (8 x 20)
MOUNT_SCREW = "M2"         # set by the measured head-pocket diameter
MOUNT_SCREW_LEN = 10.0     # B9a: length is now SOLVED against the measured
                           # grip (r6 shipped M2x10 into a 9.10 mm grip =
                           # 0.90 mm of thread, ~2 threads)
MOUNT_HEAD_D = 3.8         # ISO 4762 M2 socket head
MOUNT_INSERT_D = 3.2       # Ruthex M2 heat-set insert bore
MOUNT_INSERT_L = 4.0

# --- B6 STAND-OFF NECK (Thomas directive 3) ---------------------------
# The clip plate / quick-release used to sit 5.0 mm above a Dia150 disc that
# spanned r=75 in every direction: no hand could reach the release. The clip
# plate now stands off on a hollow neck, integral with the top plate.
# NECK_A is the plan HALF-extent: it must contain the 4 mount bosses
# (+/-19 +/- BOSS_R) and stay inside the 50 x 50 clip footprint so the
# reach-in corridors (which start at the footprint edge) are clear.
# NECK_H is set by the B6 reach-in corridor, not by taste: the corridor boxes
# are 45 mm tall with their tops at the clip underside, so the top-plate face
# has to sit clear of Z = Z_PLATE_BOT - 45 with room for the harness conduit
# that runs on it. 52 mm leaves 7 mm under the corridor floor.
NECK_H = 52.0              # clip underside -> top-plate top face
NECK_A = 24.0              # plan half-extent (48 x 48)
NECK_WALL = 2.6
# r3 (assembly A-5 / integration B12-a): the r8 neck stood as a full 48 x 48
# column straight off the plate face, and its +Y wall (y = 21.4..24.0) sat
# DIRECTLY on top of the fill cap's flange, which reaches y = 17.5. Measured
# by two independent critics: 0.65 mm of free lift against a 6.45 mm
# requirement -> the cap could neither be removed nor have been fitted. The
# neck's +Y face is now STEPPED BACK to NECK_YP0 at the base and flares out
# to the full NECK_A at NECK_FLARE_ANG, so the section stays a closed box
# (not a notch) and the cap footprint is clear of it in PLAN -- the lift is
# then unbounded, which is the only robust close. Wall thickness is kept
# NORMAL to the flare (the inner flare plane is offset along the normal).
NECK_YP0 = 15.0            # +Y face at the neck base (fill-cap plan relief)
NECK_YP_H = 12.0           # height of the relieved band (>= the cap's 6.0 mm
                           # extraction lift, measured, with 2x margin)
NECK_FLARE_ANG = 60.0      # deg from horizontal (30 deg from vertical: printable)
NECK_CAP_T = 6.5           # solid cap under the clip plate (carries inserts)
NECK_CABLE_W, NECK_CABLE_H = 8.0, 4.0     # harness slot out of the neck (-Y)

# top plate (chassis adapter = hopper lid, one printed part, now incl. neck)
TOP_T = 5.0
# rev1 B9b: 75.0 -> 78.0. The hopper flange OD follows the plate, and the
# 6x M3 heat-set inserts have to sit in it with >=1.95 mm of material on BOTH
# sides (r6: the bore was 4.19 mm deep for a 5.7 mm insert and had 0.75 mm of
# flange outboard of it).
TOP_R = 78.0
FILL_R = 23.0              # fill port radius (Dia 46 -- pellets pour easily, >3.5x D)
# r6: moved out 40 -> 45 so the (+/-19,+/-19) mount holes clear the cap recess
# (measured margin printed by the checks).
# r3: 45.0 -> 43.0. The cap's recess must clear the stepped neck base in PLAN
# (43.0 - 27.5 = 15.5 vs NECK_YP0 15.0 = 0.5 mm of land) while the Dia46 bore
# stays inside the tank (43.0 + 23.0 = 66.0 vs HOP_RI 70.0). Both measured.
FILL_POS = (0.0, 43.0)     # offset fill port center
# blind-mate PCB well (r6): the payload board mounts to the CLIP PLATE's own
# 4 tabs inside its 16 x 24 shaft; the top plate provides a sealed well under
# it for the board, its Molex J1 and a service loop, plus a cable channel.
WELL_X, WELL_Y = 16.4, 24.4     # well mouth (0.2 mm around the 16x24 board)
WELL_WALL = 2.0
WELL_DEPTH_BELOW = 4.5          # cup depth below the top-plate underside
CABLE_W, CABLE_DEEP = 5.0, 2.5  # harness channel in the top face, to -Y
CAP_FLANGE_R = 27.0
CAP_RECESS_R = 27.5
CAP_T = 2.5                # flush flange thickness
CAP_RECESS_DEEP = 3.2      # rev1: deepened 2.6 -> 3.2 so the cap flange top
                           # sits 0.65 mm BELOW the top-plate face, clear of
                           # the neck footprint that now stands on it
CAP_NECK_R = 22.7          # bore R23 -> 0.3 radial clearance
# --- r3: INVERTED BAYONET + CONTINUOUS SEALING SKIRT ------------------
# r8 cut two 4.5 x 8.5 insertion NOTCHES straight through the top plate at
# r 22.2..26.7 local, i.e. through the very bore the cap's O-ring sealed
# against: the integration critic measured 42.0 deg of 360 where the sealing
# bore does not exist, and rays from inside the tank reaching the harness
# neck through the -Y notch (B5-b). The bayonet is now INVERTED -- the PLATE
# carries two lugs that protrude INWARD from the bore wall and the CAP
# carries the slots and the circumferential groove. Consequences:
#   * NOTHING is cut radially outboard of r = FILL_R at any z, so the plate's
#     top face is unbroken and the seal becomes a FACE seal on the recess
#     floor: a closed 360 deg gland, and no path at all from the tank to the
#     neck cavity (both re-measured on the export);
#   * nothing has to sit outboard of r = CAP_RECESS_R, which is what lets the
#     cap clear the stepped neck in plan and makes the lift unbounded;
#   * the lugs are coplanar with the plate's bottom face, so they are in-plane
#     first-layer geometry, not an unsupported overhang into the bore.
LUG_RI = 20.0              # plate lug inner radius -> 3.0 mm engagement (N5)
LUG_T = 1.4                # lug thickness (z)
LUG_W = 7.0                # lug tangential width
LUG_AS = (0.0, 180.0)      # local azimuths of the two plate lugs
CAP_SEAL_R = 25.0          # face-gland centreline radius (local)
CAP_SEAL_W = 2.0           # gland width for a 1.5 mm cord
CAP_SEAL_D = 0.8           # gland depth; flange rides CAP_SEAL_GAP proud
CAP_SEAL_GAP = 0.4         # -> compressed cord 1.2 mm = 20 % squeeze [D]
# N5 anti-rotation detent, as a MODELLED SPRING FEATURE (which is what N5
# asks for as the alternative to a >=0.3 mm rigid interference: a rigid bump
# on a circular flange interferes at EVERY angle, so it is a jam, not a
# detent). The cap flange carries a tangential cantilever tab, freed by an
# arc slot and a radial slot; its tip stands CAP_DET_PROUD proud of the
# nominal flange OD and drops into a dimple in the recess wall at the locked
# angle. Turning out deflects the tab by CAP_DET_PROUD.
CAP_DET_A = 90.0           # locked angle of the detent (local, about the port)
CAP_DET_ARC = 70.0         # tab arc length (deg) -> ~33 mm of cantilever
CAP_DET_SLOT_W = 1.0       # slot width
CAP_DET_TAB_T = 1.7        # tab radial thickness
CAP_DET_PROUD = 0.40       # bump stands this far outside CAP_FLANGE_R
CAP_DET_D = 3.0            # bump / dimple diameter

# hopper.  r5 (pellet-path MODERATE): the r4 funnel was exactly 60.0 deg from
# horizontal, at/below the conical mass-flow threshold quoted for printed
# PETG (typ. 65-70 deg) -> funnel wall STEEPENED to 68 deg and the straight
# cylinder shortened 55 -> 40 so the stack barely moves (+1.7 mm) while the
# cone (which is the part that has to flow) gets 16.7 mm taller.
HOP_RI = 70.0              # inner radius (Dia 140)
HOP_WALL = 2.3
# r6: cylinder shortened 40 -> 32 mm. The geared drive (below) costs ~110 g;
# capacity at 32 mm is still 1.6x the CONTEXT hard minimum and well above the
# MASS-limited fill line, so the cheapest gram is hopper wall we cannot fill.
HOP_CYL_H = 32.0
FUNNEL_ANGLE = 68.0        # deg from horizontal (r4: 60.0)
FUNNEL_RO = 47.5           # funnel outlet radius (open sump, no pellet-scale throat)
FUNNEL_H = round((HOP_RI - FUNNEL_RO) * math.tan(math.radians(FUNNEL_ANGLE)), 1)  # 55.7

# meter
DISC_R = 46.0
DISC_T = PELLET_D_MAX + 1.0        # 14: worst-case pellet sits >=1 mm below top
POCKET_R = (PELLET_D_MAX + 2.0) / 2  # Dia 15 pockets
PCD_R = 32.0               # pocket pitch circle radius
N_POCKET = 8
CHAMBER_R = DISC_R + 1.0   # radial clearance
# r5: roof 4.0 -> 6.0. Two reasons, both from the r4 critics: it gives the
# new sleeve bushing a real seat (buildability GAP "no bearings anywhere"),
# and because the roof is cut away over the fill sector it buys 2 mm of
# BRISTLE TRIM for the wiper without touching the 1.5 mm transfer clearance.
# r6: roof 6.0 -> 9.0. Driven by the bushing PN fix (buildability MODERATE):
# the only catalogued short iglidur J flange bushing at ID20 is JFM-2023-07
# (L=7), so the seat must be 1.7 (flange counterbore) + 7.0 = 8.7 deep. The
# spare 3 mm also goes straight into bristle trim (r5 open issue 7).
ROOF_T = 9.0
ROOF_CLEAR = 1.5           # roof underside to disc top (transfer arc)
RAMP_DEG = 25.0            # r6: TRUE underside lead-in ramp at the entry edge
BRUSH_WIPE = 1.2           # bristle tip height above the disc
UNDER_GAP = 0.5            # disc to retaining plate (fines shed)
HOUSING_R = 52.0
FILL_ARC = (130.0, 250.0)  # open fill sector, deg (angle 0 = +X, exit port at 0)
BRUSH_A = 148.0            # wiper station angle (r5: 133, r6: 143). rev1 B8
                           # widens the holder 13 -> 18 mm (the 1.5 mm nose
                           # gap needs a longer 30 deg ramp), so the station
                           # moves upstream again to keep its downstream edge
                           # clear of the roof entry at 130 deg.
PLATE_T = 4.0              # retaining plate

# r6 wiper (pellet-path BLOCKING/MAJOR: "the rigid holder leads the compliant
# bristles for every object more than 5.45 mm proud"). Now:
#   - the bristle channel is at the LEADING edge, so bristles touch first at
#     every fragment height (measured by a swept contact-order probe);
#   - a rigid 45-deg DEFLECTOR NOSE trails them, reaching down to
#     disc+NOSE_GAP: the rotary-airlock "inlet shear deflector"
#     (RESEARCH-drone-spreaders 5, countermeasure #1) in hardware. Its face
#     is inclined, so a proud fragment is pushed UP into the sump (escape
#     path) instead of into a close-clearance arc.
HOLD_W = 18.0              # holder tangential width (bristle rail + nose).
                           # rev1 B8: 13 -> 18. The nose gap drops to 1.50 mm,
                           # so the 30 deg ramp run grows to ~10.3 mm and the
                           # 13 mm holder could not contain it (the r6 assert
                           # "deflector ramp overruns the holder" fires).
HOLD_H = 3.0               # holder rail height (top flush with the sump floor)
CHAN_W, CHAN_H = 1.8, 1.2  # bristle channel in the holder underside
BRISTLE_W = 1.6            # COTS strip backing width (fits the channel)
# rev1 B8 (r6 pellet-path MAJOR 3): the r6 nose sat 3.00 mm above the disc
# while the roof underside is at 1.50 -- so anything standing 1.50..3.00 mm
# proud (a Dia5 fragment nested in the pocket chamfer is +1.80, a Dia6 is
# +2.95) passed the rigid rejector untouched and met only 1.2 mm bristles
# before entering the close-clearance arc. The rejection band must cover the
# shear band: NOSE_GAP == ROOF_CLEAR.
NOSE_GAP = 1.5             # deflector nose underside above the disc face
# r6 [D]: the nose must LIFT a proud fragment, so its ramp reaction must beat
# the wedge friction. Ramp at NOSE_ANG from horizontal gives lift/push =
# cot(NOSE_ANG); the worst self-locked sliver needs mu/sin(wedge half-angle).
# 30 deg (cot = 1.73) clears the 1.46 needed at mu=0.4 for the critic's
# constructed 2.0 mm sliver -- see the WEDGE JAM block in the checks.
NOSE_ANG = 30.0            # deflector ramp angle from horizontal

# r5 disc hub / agitator drive / bearing (buildability BLOCKER fix).
# The agitator no longer clamps to the hub: the hub carries a HEX SPIGOT that
# drives an agitator rotor sitting on the sump floor, and the cartridge pulls
# straight down out of it. A COTS flanged sleeve bushing in the roof bore
# gives the disc a real radial bearing (r4 GAP: "no bearings anywhere").
# r6: the r5 PN (JFM-2022-04) could not be confirmed as catalogued
# (buildability MODERATE). Distributor listings DO carry JFM-2023-xx at
# ID20/OD23 in lengths 07/11/16/21 -> take the L=7 part. L/D = 0.35 (r5: 0.20).
HUB_R = 9.9                # Dia19.8 journal -> 0.1 mm radial
                           # running clearance in the Dia20 bushing ID
BUSH_ID, BUSH_OD = 20.0, 23.0
BUSH_FL_OD, BUSH_FL_T = 30.0, 2.0    # flange OD / thickness (ASSUMPTION)
BUSH_CB_DEPTH = 1.7        # roof-top counterbore: flange stands 0.3 proud and
                           # becomes the agitator's thrust face (iglidur, not
                           # TPU-on-PETG)
BUSH_LEN = 7.0             # sleeve length below the flange (JFM-2023-07)
SETSCREW_Z_OFF = -4.5      # set-screw axis relative to the disc top: r6 puts
                           # it INSIDE the disc body (the Dia6 gearbox shaft
                           # ends 0.5 mm below the disc top), so the Dia20
                           # journal surface stays unbroken
HEX_AF = 15.0              # hub drive spigot across-flats
HEX_LEN = 6.5              # spigot length above the bushing
AGIT_FL_R = 14.5           # agitator flange (rides on the bushing flange)
AGIT_COL_R = 11.8
AGIT_FINGER_R = 2.0
AGIT_FINGER_RO = 46.7      # fingers sweep to 0.3 mm off the chamber wall

# exit port. r6 (pellet-path MODERATE: "the model's own probe uses an exit
# radius that is not in the part"): the retaining rim is the TOP of the
# chamfer, so it is a named parameter now and the chamfer is reduced 1.5 ->
# 0.75 mm, which shrinks the park-lens uncommanded-release class.
# rev1 B7: bore Dia18 -> Dia16. The release separation scales with the rim
# radius (support is lost when the pellet centre crosses the rim), so a
# smaller port releases LATER in the index and improves park retention. It is
# still 1.23x the worst-case Dia13 pellet and 2.4 mm larger than the pellet's
# maximum lateral freedom in the pocket.
PORT_R = 8.0
PORT_CHAMF = 0.75
PORT_RIM_R = PORT_R + PORT_CHAMF

# chute (straight, vertical)
CHUTE_ID = 22.0
CHUTE_WALL = 2.0
CHUTE_LEN = 50.0
SENSOR_DROP = 40.0         # IR beam below retaining plate bottom

# --- rev1 B4: COUNT SENSOR, rebuilt to ELECTRONICS.md 4.2-4.5 ----------
# r6 had ONE centred Dia3.2 tunnel per side in a Box(12,12,14) boss, which
# 4.2 shows is disqualifying (a Dia12 pellet near the wall reads 7.5 ms and
# is thrown away as a fragment). ECO-3 + ECO-9: TWO chord beams at
# x = 32 -/+ 3 and z = Z_SENSOR +/- 3 (6.0 mm vertical stagger, which also
# gives a per-event velocity). ECO-4: the window moves to the BORE FACE.
# ECO-5 (revised): lateral labyrinth instead of the withdrawn 15 deg slope.
SENS_BOSS_X0 = 22.0        # inboard face (motor face is at x = 17.6)
SENS_BOSS_X1 = 47.0        # outboard face
SENS_BOSS_Y0 = 11.0        # chute bore wall
# r3 (count-sensor critic BLOCKING): 25.0 -> 27.5. The r8 stack parked the
# board's inner face 0.500 mm off the aperture plane, so neither the ordered
# TSAL6200 (5 mm radial LED, ~5.8 mm body above its seating plane) nor the
# VBPW34FAS (~3.2 mm case) could be fitted -- the electronics doc again
# described hardware the CAD did not contain. The cavity is deepened by
# 2.5 mm and the board plane moved out, so the aperture-facing component
# height is SENS_COMP_H; the package envelopes are booleaned in the checks.
# r4 (count-sensor critic BLOCKING 1): 27.5 -> 30.5. The r9 stack was built
# against a 5.8 mm TSAL6200 body height that came out of a CRITIQUE, not out
# of a drawing. Vishay doc 81010 rev 2.4 (drawing 6.544-5259.06-4) gives the
# T-1 3/4 package as Dia5.0 +/-0.15 body, Dia5.8 +/-0.15 flange and
# 8.7 +/- 0.3 mm from the SEATING PLANE to the dome apex (dome R2.49). At the
# r9 board plane |y| = 23.5 a datasheet LED buried 11.2532 mm3 in the plate
# (14.6614 at the 9.0 mm tolerance limit). The board plane moves out 3.0 mm
# to |y| = 26.5, which clears the 9.0 mm worst case with 0.5 mm to spare, and
# the boss/cover/post/ear stack moves with it. The boss grows in |y| ONLY --
# x stays 22.0..47.0, so B4.3's 4.0000 mm motor clearance is untouched.
SENS_BOSS_Y1 = 30.5        # outer face
SENS_BOSS_H = 19.0         # 4.4 mm of wall above/below the outer apertures
SENS_BEAM_DX = 3.0         # chord offset from the bore axis (4.3)
SENS_BEAM_DZ = 3.0         # ECO-9 half-stagger -> 6.0 mm apart
SENS_APER_R = 1.6          # Dia3.2 aperture
SENS_LAB_OFF = 0.8         # ECO-5 lateral labyrinth offset, outer 2.5 mm
SENS_LAB_LEN = 2.5
SENS_WIN_R = 3.0           # ECO-4 Dia6 PMMA window
SENS_WIN_T = 1.0           # 1 mm thick -> the seat is 1.0 deep, not 0.4
SENS_WIN_CHAMF = 0.4       # chamfer at the bore mouth
SENS_CAV = (20.4, 13.5, 14.4)  # component cavity (x, y, z): 9.5 mm of
                               # component height + a 2 mm board + 2 mm of
                               # cover post (r8 was 8.0 deep and 0.5 short;
                               # r9 was 10.5 and 1.6 short of a datasheet LED)
SENS_CAV_Y0 = 17.0         # cavity inner face -> 6.0 mm of tunnel
# --- rev1 r2: BOARD RETENTION + CABLE PORT (ECO-12 / punch-list N3) ----
# r1 modelled no retention at all ("carried as an open issue") while the BOM
# ordered 2x M3 grubs for a hole that does not exist -- the count-sensor
# critic escalated that documentation/geometry disagreement to blocking.
# The 2.3 mm cavity walls cannot take an M2 pilot, so the boss grows two
# local EARS in z and a bolted COVER closes the cavity, clamps the board on
# 4 posts and carries the grommeted cable port.
SENS_EAR_H = 5.0           # ear height (z), one above and one below
SENS_EAR_X = 18.0          # ear width (x)
SENS_EAR_XC = 38.0         # ear centre (x): covers both the screw pilots and
                           # the cable port/duct socket
SENS_SCREW_DZ = SENS_BOSS_H / 2 + SENS_EAR_H / 2       # 12.0, pilot axis
SENS_PORT_R = 2.5          # Dia5 cable port, cavity -> lower ear -> duct
SENS_PORT_X = 41.0         # OFF the beam chords x=29/35 (a port on the boss
                           # centreline x=34.5 breaks into aperture B)
# r3 (assembly A-6): the r8 cable port exited SIDEWAYS through the cover into
# a duct socket at |y| = 27.5..32.5, x 37..45 -- i.e. the duct stood 0.5 mm
# outboard of the cover it had to receive, and the cover's swept insertion
# path was 488.4789 mm3 into the plate. The port now leaves the cavity floor
# BEHIND the board and drops out of the lower ear's BOTTOM face, so nothing
# of the harness is outboard of the cover at all and the cover has no hole.
SENS_PORT_Y = 22.5         # riser axis |y| (behind the components,
                           # and the duct stub below it stays inboard of the
                           # cover face at |y| = 27.5)
# r2 run 3: the port/socket also has to sit OUTSIDE the 18 x 12 board's own
# straight-line insertion corridor (board z-envelope +/-6). At the beam
# height the 5 mm socket stub obstructed that sweep by 57.27 mm3, so the port
# drops into the LOWER EAR band and the cavity feeds it through a short
# vertical riser.
SENS_PORT_DZ = -11.0       # port axis, relative to Z_SENSOR
# r4: 6.5 -> 9.5. TSAL6200 seating-plane-to-apex 8.7 +0.3 (Vishay 81010 rev
# 2.4) + 0.5 mm of air at the max-material limit. The Dia5.0 barrel CANNOT
# enter the Dia3.2 aperture, so the LED tip must clear the cavity floor
# outright: 17.0 (floor) + 9.0 (max) + 0.5 = 26.5 = the board seating plane.
SENS_COMP_H = 9.5          # aperture-facing component height
LED_H_NOM, LED_H_MAX = 8.7, 9.0        # Vishay 81010 rev 2.4, drawing
LED_BODY_D, LED_FLANGE_D = 5.0, 5.8    # 6.544-5259.06-4 (fetched by the r3
LED_FLANGE_T, LED_DOME_R = 0.7, 2.49   # count-sensor critic)
PD_L, PD_W, PD_H = 6.4, 3.9, 1.2       # VBPW34FAS SMD gullwing, Vishay 81127
SENS_BOARD_T = 2.0         # sensor PCB thickness (ELECTRONICS 7)
SENS_BOARD_Y0 = SENS_CAV_Y0 + SENS_COMP_H          # 23.5, board inner face
SENS_BOARD_Y1 = SENS_BOARD_Y0 + SENS_BOARD_T       # 25.5, board outer face
COVER_T = 2.0              # sensor-cover plate thickness
SENS_PAD_T = 0.5           # r6: compliant silicone pad between the cover
                           # posts and the board's outer face (BOM line)
# r4 (B10 mesh hygiene): the r9 cover flange was EXACTLY as wide as the boss,
# so its perimeter edge was coincident with the boss edge and the assembly
# mesh carried 4-face edges there. It is inset 0.4 mm/side.
COVER_X = SENS_BOSS_X1 - SENS_BOSS_X0 - 0.8      # 24.2
COVER_Z = SENS_BOSS_H + 2 * SENS_EAR_H - 0.8     # 28.2
# r4 (count-sensor NB-1): board-locating ribs on the cover, in the 1.200 mm
# gap between the 18 x 12 board and the 20.4 x 14.4 cavity wall.
SENS_RIB_T, SENS_RIB_D = 0.8, 3.5      # 0.8 thick, 3.5 deep in |y|
SENS_RIB_X, SENS_RIB_Z = 9.6, 6.6      # rib centres -> 0.200 mm/side on the
                                       # board, 0.200 mm/side in the cavity

# r6 ACTUATOR CHANGE (pellet-path BLOCKING "the constructed wedge jam is not
# defeated" + MAJOR "no torque budget"). CONTEXT hard requirement 2 wants the
# actuator to be able to SHEAR a fragment; r5's direct-drive NEMA 14 gave
# 5.6 N at the pocket lip and the builder argued the opposite case. Fix:
# StepperOnline 14HS13-0804S-PG5 -- the same NEMA 14 with a 5.18:1 planetary
# gearbox (vendor page: 0.14 N*m motor holding torque, ratio 5.18, efficiency
# 90%, backlash <=3 deg, max permissible output 3 N*m, frame 35x35, motor
# L=34, gearbox L=29.2, output shaft Dia6 x 18 with a 12 mm D-cut, gross
# 0.38 kg). Torque is bought with GEARING, not current: the phase current --
# and therefore the 2 A / 12VSW fuse case -- is unchanged.
MOTOR_W = 35.2             # motor frame
GEAR_OD = 36.0             # gearbox body (round, worst case) -- ASSUMPTION
MOTOR_L = 34.0             # motor body length
GEAR_L = 29.2              # gearbox length (vendor)
# rev1 B3. The r6 model used a 26 mm SQUARE pattern at 45/135/225/315 deg,
# which is not what the datasheet says: 14HS13-0804S-PG5 is 4 x M3 on a
# Dia26 +/- 0.15 BOLT CIRCLE, i.e. r = 13.0 ON THE AXES. With M3 clearance
# holes at r=13 the hole edge is at r=11.30, so the r6 Dia22.2 pilot bore
# (edge 11.10) would have left a 0.20 mm web.
# MOTOR_PILOT_R is an explicit ASSUMPTION: the datasheet does not give the
# gearbox output-flange pilot. Dia22 (the plain NEMA-14 motor-face pilot) is
# geometrically impossible against a Dia26 M3 bolt circle -- no vendor ships
# a 0.3 mm land -- so the pilot is taken as Dia16, the largest round number
# that leaves the printed plate a >=1.95 mm web AND a continuous thrust-
# washer land. CLOSURE: measure the delivered gearbox flange.
MOTOR_PILOT_R = 8.0        # Dia16 output-flange pilot boss (ASSUMPTION)
MOTOR_SHAFT_R = 3.0        # Dia6 output shaft (vendor)
MOTOR_SHAFT_LEN = 18.0
MOTOR_SHAFT_DCUT = 12.0
MOTOR_SHAFT_FLAT = 0.5     # vendor D-cut depth -> flat at r = 2.5
MOTOR_BC_R = 13.0          # Dia26 +/- 0.15 bolt CIRCLE (datasheet)
MOTOR_SCREW_CLR = 1.7      # Dia3.4 clearance for M3
MOTOR_MASS = 350.0         # rev1 B11.3: carried at >=350 g until it is on a
                           # scale (vendor lists 0.38 kg GROSS; r6 carried a
                           # 310 g NET ASSUMPTION and the mass critic called
                           # it optimistic). 380 g sensitivity in the ledger.
GEAR_RATIO = 5.18
GEAR_EFF = 0.90
MOTOR_T_HOLD = 0.14        # N*m at rated phase current (vendor)
DRIVE_T_MAX = MOTOR_T_HOLD * GEAR_RATIO * GEAR_EFF        # 0.65 N*m output
DRIVE_I_NORMAL = 0.60      # normal-metering current fraction (TMC2209 IRUN)
# pellet strength anchor: US4172714 "resist crushing with loads less than
# about 7500 g, or 3.7 kg/cm2" -> 0.36 MPa on projected area; scaled to a
# 12 mm pellet that is ~41 N whole-pellet crush (RESEARCH-drone-spreaders
# 1.3, [D]). Both numbers are class-derived ASSUMPTIONS pending an IFDC
# S-115 bench test on real pellets.
PELLET_CRUSH_N = 41.0
PELLET_STRENGTH_MPA = 0.36

# magnets / hall / detent (phase hardening)
MAG_R_POS = 42.5           # magnet track radius (Dia3x2 N52, supermagnete S-03-02-N class)
MAG_R = 1.475              # rev1 N2 / ECO-11: Dia2.95 = 0.05 mm diametral
                           # INTERFERENCE on a Dia3.00 magnet (r6 modelled
                           # Dia3.00 = zero retention) + retaining compound
MAG_DEPTH = 2.0
# r6 (pellet-path MAJOR): the r5 detent was a Dia4 x 1.5 deep dimple with an
# unspecified M5 plunger -- a commodity plunger in that seat needs 0.2-1.1
# N*m to release, i.e. up to 6x the whole motor. Now a SHALLOW SPHERICAL
# seat (R6 x 0.6) with a specified light plunger; release torque computed.
DIMPLE_SPH_R = 8.0
DIMPLE_DEPTH = 0.4
PLUNGER_BALL_R = 2.5       # M5 ball-nose plunger
PLUNGER_F = 2.5            # N end force, LIGHT spring (specified)
# rev1 B2: the detent DIMPLES move from the half-station angles to the POCKET
# angles and the plunger boss moves from theta=180 to theta=157.5 (also a
# half-station). The park phase is IDENTICAL either way -- engagement needs
# dimple+phi = plunger, so phi = 22.5 deg (mod 45) in both schemes, i.e.
# pockets park at 22.5+45k, 22.5 deg off the exit port, and a pocket magnet
# still sits under the 112.5 deg index Hall (ECO-2, asserted below).
# What it buys: the half-station radii are now free of dimples, which is the
# only place a radial grub-screw corridor can run between the pockets.
# r2 (all-pairs COLLISION, 3.4 mm3): the detent plunger boss at theta=157.5
# (radius 6, i.e. +/-6.3 deg at r=54.5) overlapped the WIPER END TAB, which
# spans theta 142.8..153.2 at that radius. 67.5 is the same half-station
# modulo 45 deg, so the park phase (22.5 deg off the port) is unchanged, and
# it is 37.5 deg from both neighbouring skirt tabs (30/105).
PLUNGER_A = 67.5
GRUB_A = 202.5             # grub corridor / access-port angle (half-station)
GRUB_SIZE = "M3x4"         # rev1 B2.4: ONE grub size, used by the BOM, the
                           # fastener table and the console text alike
GRUB_PILOT_R = 1.3         # Dia2.6 thread-forming pilot for the M3 grub
GRUB_CLEAR_R = 1.7         # Dia3.4 clearance channel out to the disc OD
GRUB_KEY_AF = 1.5          # M3 grub hex key across flats
HALL_STATION_A = 90.0      # station Hall angle
HALL_INDEX_A = 112.5       # index Hall angle

# latch ring (quarter-turn receiver on housing)
RING_RI = 52.3
RING_RO = 58.0
RING_DROP = 3.0            # shelf below the plate
RING_BAND_H = 8.0          # r3: overlap band height above plate top (joins housing)
LUG_ANGLES = (60.0, 180.0, 300.0)

# electronics bay.
# r3 (integration BLOCKING B5-a): the lid aperture measured 42.0000 mm clear
# against a 42.0 mm board -> 0.0000 mm of clearance, i.e. the bay housed a
# board it could not be given. The bay grows 50 -> 56 wide (interior 52) so
# the aperture can open to 46.0 with the gasket groove and the lid screws
# still outside it; board clearance is re-measured on the export.
BAY_W, BAY_D, BAY_H = 56.0, 26.0, 42.0
BAY_FL_W, BAY_FL_H = 68.0, 50.0          # lid flange (screws outside the seal)
BAY_YC = -75.0             # inner face y=-62: clear of housing r52 + lug swing r<56

# structural fastening (r3, reworked r4)
FLANGE_SCREW_R = 74.0      # top plate -> hopper flange, 6x M3 + heat-set insert
FLANGE_SCREW_AS = tuple(15.0 + 60.0 * k for k in range(6))
FLANGE_T = 7.0             # rev1 B9b: 4.0 -> 7.0 so a Ruthex RX-M3x5.7 gets
                           # a 6.0 mm bore with 1.0 mm of floor under it
FLANGE_INSERT_DEEP = 6.0

# derived Z stack (top down).  rev1 N12: the r6 comments here were stale by
# 5.3-23.0 mm (they still described the r4 funnel), so every value is now
# printed against its comment by the Z-STACK AUDIT in the checks and the
# comments are the CURRENT derived numbers.
# rev1 r2 (N12 again): r1 took NECK_H from 42 to 52 mm and did NOT update
# these comments or the audit table, so every Z below the clip plate was
# quoted 10.0 mm high in the source while the exports were 10.0 mm lower.
# The values below are the CURRENT derived numbers and the audit asserts them.
Z_PLATE_BOT = Z_CLIP_TOP - CLIP_T              # -181.55  clip underside
Z_TOP_TOP = Z_PLATE_BOT - NECK_H               # -233.55  top-plate top face
Z_TOP_BOT = Z_TOP_TOP - TOP_T                  # -238.55
Z_HOP_BOT = Z_TOP_BOT - HOP_CYL_H              # -270.55
Z_FUN_BOT = Z_HOP_BOT - FUNNEL_H               # -326.25  sump floor
Z_ROOF_BOT = Z_FUN_BOT - ROOF_T                # -335.25
Z_DISC_TOP = Z_ROOF_BOT - ROOF_CLEAR           # -336.75
Z_DISC_BOT = Z_DISC_TOP - DISC_T               # -350.75
Z_RPLATE_TOP = Z_DISC_BOT - UNDER_GAP          # -351.25
Z_RPLATE_BOT = Z_RPLATE_TOP - PLATE_T          # -355.25
Z_CHUTE_BOT = Z_RPLATE_BOT - CHUTE_LEN         # -405.25
Z_MOTOR_TOP = Z_RPLATE_BOT                     # gearbox output flange face
Z_GEAR_BOT = Z_MOTOR_TOP - GEAR_L              # -384.45
Z_MOTOR_BOT = Z_GEAR_BOT - MOTOR_L             # -418.45
Z_SENSOR = Z_RPLATE_BOT - SENSOR_DROP          # -395.25  count-beam datum
Z_STACK_AUDIT = [
    ("Z_MOUNT", Z_MOUNT, -171.0), ("Z_CLIP_TOP", Z_CLIP_TOP, -171.05),
    ("Z_PLATE_BOT", Z_PLATE_BOT, -181.55), ("Z_TOP_TOP", Z_TOP_TOP, -233.55),
    ("Z_TOP_BOT", Z_TOP_BOT, -238.55), ("Z_HOP_BOT", Z_HOP_BOT, -270.55),
    ("Z_FUN_BOT", Z_FUN_BOT, -326.25), ("Z_ROOF_BOT", Z_ROOF_BOT, -335.25),
    ("Z_DISC_TOP", Z_DISC_TOP, -336.75), ("Z_DISC_BOT", Z_DISC_BOT, -350.75),
    ("Z_RPLATE_TOP", Z_RPLATE_TOP, -351.25),
    ("Z_RPLATE_BOT", Z_RPLATE_BOT, -355.25),
    ("Z_SENSOR", Z_SENSOR, -395.25), ("Z_CHUTE_BOT", Z_CHUTE_BOT, -405.25),
    ("Z_GEAR_BOT", Z_GEAR_BOT, -384.45), ("Z_MOTOR_BOT", Z_MOTOR_BOT, -418.45),
]

# r5: everything below is now DERIVED from the Z stack (r4 hard-coded these,
# so a funnel-angle change would have silently desynchronised them).
RIB_ZC = Z_RPLATE_TOP + RING_BAND_H + 0.4 + 11.5 / 2   # bay rib centerline
# hopper -> housing joint: 3 RADIAL skirt tabs outside the housing wall,
# M3 plastite driven horizontally from outside (r3 buildability BLOCKER fix).
# Angles clear the brush tab (133 +/-6), plunger boss (180 +/-6) and the
# electronics-bay driver shadow (~240..300).
SKIRT_AS = (30.0, 105.0, 225.0)
# r4 (assembly NB-2): the r9 tab was 3.00 mm thick -> grip 3.150 mm, so an
# M3x8 presented 4.850 mm of thread to a 4.100 mm pilot and bottomed out
# 0.750 mm before it clamped. The pilot CANNOT go deeper: at theta = 225 that
# tab sits on the open sump window, where the housing is only the r 47.0..52.0
# wall and the modelled pilot already stops 0.900 mm short of breaking into
# the pellet space. So the TAB grows instead, 3.00 -> 4.05 mm: grip 4.200 mm,
# thread beyond the grip 3.800 mm against a 4.100 mm pilot -> the screw
# clamps with 0.300 mm to spare and 3.800 mm (1.27 x D) of engagement.
SKIRT_R_IN, SKIRT_R_OUT = 52.15, 56.20   # 0.15 running gap off housing OD 52
SKIRT_PILOT_L = 4.4                      # r 47.9 .. 52.3, unchanged
SKIRT_SCREW, SKIRT_SCREW_L = "M3x8", 8.0
# r4 (assembly A-9): the bay's only two fasteners were BOM'd M3x12 against a
# measured 13.920 mm grip -- 0.000 mm of engagement, tip 1.920 mm short of
# the housing. The pilot bottoms at y = -45.0, so full engagement needs
# 64.0 - 45.0 = 19.0 mm; the next standard length up was M3x20.
# r6 (assembly MAJOR A-12, both halves): M3x20 put the screw TIP at y =
# -44.000, i.e. 0.850 mm PAST the chamber bore wall and 0.187 mm from a
# rotating disc; and the flat-bottomed Dia2.5 pilot at y = -45.000 broke
# through the CURVED chamber wall (inner face -44.856 at x = 14) over
# 1.2492 mm2 = 27.7 % of its own section, leaving 0.144 mm -- one FDM layer --
# where it was closed at all, i.e. an unsealed granule-chamber-to-atmosphere
# path under each screw head. The pilot floor moves out to -46.5 (>= 1.95 mm
# of wall under the whole bore section, printed below) and the screw drops to
# M3x18, whose tip lands at y = -46.000: 0.500 mm short of the floor, 4.080 mm
# of engagement (1.36 x D), and 2.560 mm of material still under the tip.
BAY_SCREW, BAY_SCREW_L = "M3x18", 18.0
BAY_RIB_PILOT_Y0, BAY_RIB_PILOT_Y1 = -52.0, -46.5
SKIRT_SCREW_Z = Z_FUN_BOT - 4.0          # radial screw axis (wall solid there)
SKIRT_Z0 = Z_FUN_BOT - 8.0
# tab top: r5 raised to Z_FUN_BOT+11.0 so the steeper (68 deg) cone still
# overlaps the tab by >2 mm; asserted against the hopper VOID below.
SKIRT_Z1 = Z_FUN_BOT + 11.0
SKIRT_ROOT_Z0, SKIRT_ROOT_Z1 = Z_FUN_BOT + 0.1, Z_FUN_BOT + 4.2
# cone surfaces: inner r(z) = FUNNEL_RO + dz/tan(A), outer = inner + HOP_WALL
_tanA = math.tan(math.radians(FUNNEL_ANGLE))
assert FUNNEL_RO + (SKIRT_Z1 - Z_FUN_BOT) / _tanA < SKIRT_R_IN, \
    "skirt tab breaches the hopper void"
assert FUNNEL_RO + HOP_WALL + (SKIRT_Z1 - Z_FUN_BOT) / _tanA > SKIRT_R_IN + 2.0, \
    "skirt tab not fused into the cone wall"

# rev1 B11.1: CF-PETG carried at 1.27 g/cm3 (r6 used the low-end 1.25).
DENS = {"petg_cf": 1.27e-3, "petg": 1.27e-3, "tpu": 1.20e-3,
        "alu": 2.70e-3, "ptfe": 2.20e-3, "nylon": 1.14e-3, "pmma": 1.19e-3}


def sector(r_in, r_out, a0_deg, a1_deg, z_bot, height):
    """Annular sector solid, angles CCW from +X."""
    ring = Cylinder(r_out, height) - Cylinder(max(r_in, 0.01), height + 2)
    pts = [(0.0, 0.0)]
    for a in np.linspace(math.radians(a0_deg), math.radians(a1_deg), 24):
        pts.append((2 * r_out * math.cos(a), 2 * r_out * math.sin(a)))
    wedge = extrude(Polygon(*pts, align=None), amount=height + 4)
    wedge = Pos(0, 0, -(height + 4) / 2) * wedge
    return Pos(0, 0, z_bot + height / 2) * (ring & wedge)


def vol_of(x):
    """ShapeList-safe volume (never swallow to 0.0)."""
    if x is None:
        return 0.0
    if hasattr(x, "volume"):
        return x.volume
    return sum(vol_of(i) for i in x)  # ShapeList / iterable of shapes


def inter_vol(a, b):
    try:
        return vol_of(a.intersect(b))
    except Exception:
        try:
            return vol_of(a & b)
        except Exception:
            return float("nan")   # loud, not silent


def bb_disjoint(a, b, margin=0.05):
    A, B = a.bounding_box(), b.bounding_box()
    return (A.max.X < B.min.X - margin or B.max.X < A.min.X - margin or
            A.max.Y < B.min.Y - margin or B.max.Y < A.min.Y - margin or
            A.max.Z < B.min.Z - margin or B.max.Z < A.min.Z - margin)


def is_valid(s):
    """OCC topological validity of a shape.

    r6 ROOT CAUSE of integration BLOCKING I-1 ("the cartridge harness duct is
    solid printed material"). BRepAlgoAPI returns an EMPTY result, with no
    exception, when a TOOL shape is topologically invalid -- so `a -= b`
    silently becomes a no-op and every downstream volume/mass number is
    consistent with a fix that is not in the geometry. r11's `_bore` was a
    FUSE of EQUAL-RADIUS PERPENDICULAR cylinders (DUCT_RI = 2.5 on every leg),
    which is the classic OCC degenerate-tangency case; BRepCheck_Analyzer
    reports IsValid() = False on it, and rp.intersect(_bore) then reads
    0.0 mm3 even though a Dia1 sphere on the duct axis reads INSIDE both.
    """
    from OCP.BRepCheck import BRepCheck_Analyzer
    return bool(BRepCheck_Analyzer(s.wrapped).IsValid())


def cut_each(part, tools, name="", floor=None):
    """Subtract a LIST of tools ONE AT A TIME and PROVE material came out.

    Two rules, both learned from I-1: (1) never fuse a set of cutting tools
    before using them -- cut with each valid primitive in turn, so a
    degenerate fuse can never exist; (2) a boolean that removes nothing is a
    hard failure, not a silent pass.
    """
    v0 = vol_of(part)
    for i, t in enumerate(tools):
        if not is_valid(t):
            raise AssertionError(
                f"cut_each('{name}'): tool {i} is an INVALID solid -- OCC "
                f"would silently no-op this cut (I-1 class)")
        part = part - t
    removed = v0 - vol_of(part)
    print(f"  cut_each({name}): {len(tools)} tools, removed {removed:.4f} mm3 "
          f"from {v0:.4f} mm3 -> {vol_of(part):.4f} mm3")
    if floor is not None and removed < floor:
        raise AssertionError(
            f"cut_each('{name}'): removed {removed:.4f} mm3 < floor "
            f"{floor:.4f} mm3 -- the boolean did NOT bite (I-1 class)")
    return part


# =====================================================================
# Parts
# =====================================================================
parts = {}   # name -> dict(solid, color, mass, basis)


# rev1 r2: the round-1 assembly critic's requirement #1 -- "an assertion in
# the build that fails the export if any named part's volume drops below a
# floor -- this failure mode has now bitten twice in the same file". It has
# now bitten three times (top_plate at r7, brush_holder at the r7+ source).
# Floors are order-of-magnitude sanity numbers, not tolerances.
VOL_FLOOR_CM3 = {
    "clip_plate": 8.0, "top_plate": 80.0, "fill_cap": 6.0, "hopper": 90.0,
    "meter_housing": 80.0, "pocket_disc": 60.0, "thrust_washer": 0.2,
    "sleeve_bearing": 1.0, "agitator": 3.0, "brush_holder": 2.0,
    "brush_bristles": 0.2, "retaining_plate_chute": 35.0, "stepper": 50.0,
    "electronics_bay": 14.0, "bay_lid": 5.0, "blindmate_pcb": 0.8,
    "count_windows": 0.05, "chute_plug": 3.0, "service_stand": 50.0,
    "sensor_cover": 1.0,
}


def _guard(name, solid):
    """Fail LOUDLY if a boolean ate a part (null shape or below its floor)."""
    if solid is None or getattr(solid, "_wrapped", None) is None:
        raise AssertionError(f"PART EATEN: '{name}' is a NULL shape")
    v = solid.volume / 1000.0
    floor = VOL_FLOOR_CM3.get(name)
    if floor is not None and v < floor:
        raise AssertionError(
            f"PART EATEN: '{name}' = {v:.3f} cm3 < floor {floor:.1f} cm3")
    return v


def add(name, solid, color, mass=None, density=None, basis=""):
    _guard(name, solid)
    if mass is None:
        mass = solid.volume * density
    solid.label = name
    parts[name] = dict(solid=solid, color=color, mass=mass, basis=basis)
    return solid


# rev1: AUX parts are shipped hardware that is NOT part of the flight
# assembly's all-pairs interference model -- the bonded count windows (which
# sit in their seats by design), the ground-only chute plug (0.3 mm
# interference by design) and the off-aircraft service stand. They are
# exported, massed and BOM'd, and checked by their own probes.
aux = {}


def add_aux(name, solid, color, mass=None, density=None, basis=""):
    _guard(name, solid)
    if mass is None:
        mass = solid.volume * density
    solid.label = name
    aux[name] = dict(solid=solid, color=color, mass=mass, basis=basis)
    return solid


# --- 1. payload-side clip plate (imported COTS STEP) -------------------
clip = import_step(CLIP_PLATE_STEP)
bb = clip.bounding_box()
# STEP thickness axis is Y (-2.5..8.0). Rotate +90 about X -> thickness on Z,
# STEP +Y face becomes +Z (drone-facing side, ASSUMPTION on orientation).
clip = Rot(X=90) * clip
bb = clip.bounding_box()
cx = (bb.min.X + bb.max.X) / 2
cy = (bb.min.Y + bb.max.Y) / 2
clip = Pos(-cx, -cy, Z_CLIP_TOP - bb.max.Z) * clip   # B6.4: top face -171.05
clip_vol = clip.volume
add("clip_plate", clip, "#9aa0a6", density=DENS["alu"],
    basis="COTS 2112; [D] STEP vol %.1f cm3 x 2.70 (alu ASSUMPTION)" % (clip_vol / 1000))

# ---- r6 CLIP-PLATE MAP (interference BLOCKING #1) ---------------------
# r5 "probed" the pattern with a Dia2.4 cylinder against a `v < 5.0 mm3`
# threshold -- which passes just as happily inside a 16x24 through-WINDOW as
# in a hole. r6 maps the plate by point containment (the method the critic
# used) and DERIVES the pattern, then asserts it.
from OCP.BRepClass3d import BRepClass3d_SolidClassifier   # noqa: E402
from OCP.gp import gp_Pnt                                  # noqa: E402
from OCP.TopAbs import TopAbs_OUT                          # noqa: E402

_clip_cls = BRepClass3d_SolidClassifier(clip.wrapped)


def clip_solid(x, y, z):
    _clip_cls.Perform(gp_Pnt(x, y, z), 1e-6)
    return _clip_cls.State() != TopAbs_OUT


def clip_open_dia(x, y, z, rmax=5.0):
    """Largest concentric clear diameter about (x,y) at height z."""
    best = 0.0
    for r in np.arange(0.0, rmax, 0.05):
        if all(not clip_solid(x + r * math.cos(t), y + r * math.sin(t), z)
               for t in np.linspace(0, 2 * math.pi, 25)):
            best = r
        else:
            break
    return 2 * best


_zs = np.arange(Z_PLATE_BOT + 0.2, Z_MOUNT - 0.1, 0.4)
_through = [(x, y) for x in np.arange(-24.5, 24.6, 0.5)
            for y in np.arange(-24.5, 24.6, 0.5)
            if not any(clip_solid(x, y, z) for z in _zs)]
_T = np.array(_through)
# cluster the through-open columns
_used = np.zeros(len(_T), bool)
CLIP_OPENINGS = []
for _i in range(len(_T)):
    if _used[_i]:
        continue
    _st, _comp, _used[_i] = [_i], [_i], True
    while _st:
        _k = _st.pop()
        _d = np.linalg.norm(_T - _T[_k], axis=1)
        for _j in np.where((_d < 0.75) & (~_used))[0]:
            _used[_j] = True
            _st.append(_j)
            _comp.append(_j)
    _c = _T[_comp]
    CLIP_OPENINGS.append(dict(n=len(_c), cx=_c[:, 0].mean(), cy=_c[:, 1].mean(),
                              x0=_c[:, 0].min(), x1=_c[:, 0].max(),
                              y0=_c[:, 1].min(), y1=_c[:, 1].max()))
# the 4 mount holes = small openings nearest the expected 38x38 pattern
_mount = [o for o in CLIP_OPENINGS
          if abs(abs(o["cx"]) - BOLT_DX_NOM) < 1.5 and abs(abs(o["cy"]) - BOLT_DY_NOM) < 1.5]
_tabs = [o for o in CLIP_OPENINGS
         if abs(abs(o["cx"]) - PCB_TAB_DX) < 1.0 and abs(abs(o["cy"]) - PCB_TAB_DY) < 1.0]
_shaft = max(CLIP_OPENINGS, key=lambda o: o["n"])
assert len(_mount) == 4, f"expected 4 mount holes, mapped {len(_mount)}"
assert len(_tabs) == 4, f"expected 4 blind-mate PCB tabs, mapped {len(_tabs)}"
BOLT_DX = round(float(np.mean([abs(o["cx"]) for o in _mount])), 2)
BOLT_DY = round(float(np.mean([abs(o["cy"]) for o in _mount])), 2)
MOUNT_HOLE_D = clip_open_dia(BOLT_DX, BOLT_DY, Z_PLATE_BOT + 2.0, 3.0)
MOUNT_POCKET_D = clip_open_dia(BOLT_DX, BOLT_DY, Z_MOUNT - 2.0, 5.0)
TAB_HOLE_D = clip_open_dia(PCB_TAB_DX, PCB_TAB_DY, Z_PLATE_BOT + 2.0, 3.0)
# blind-mate shaft: the big through-opening (walls found by scanning out)
SHAFT_X = round(float(max(abs(_shaft["x0"]), abs(_shaft["x1"]))) + 0.25, 2)
SHAFT_Y = round(float(max(abs(_shaft["y0"]), abs(_shaft["y1"]))) + 0.25, 2)
# slab (solid bolting face) thickness under the cavity
SLAB_TOP = Z_PLATE_BOT
for _z in np.arange(Z_PLATE_BOT, Z_MOUNT, 0.1):
    if not clip_solid(23.5, 0.0, _z) or not clip_solid(0.0, 23.5, _z):
        pass
    if not clip_solid(12.0, 12.0, _z):     # first z with no slab material
        SLAB_TOP = _z
        break
assert MOUNT_HOLE_D > 2.5, "mapped mount hole is not screw-sized"
assert MOUNT_POCKET_D >= MOUNT_HEAD_D, (
    f"M2 head {MOUNT_HEAD_D} does not fit the mapped {MOUNT_POCKET_D:.2f} pocket")

# --- 2. top plate = chassis adapter + STAND-OFF NECK + hopper lid ------
# rev1 B6 (Thomas: "the way the attachment interface is integrated may make it
# difficult to reach in and connect/disconnect it ... give it some more
# clearance from the rest of the dispenser"). The r6 top plate put a Dia150
# disc 5.0 mm under the clip plate, so there was no hand access to the
# quick-release at all. The clip plate now stands off on a hollow 48 x 48
# neck, integral with the plate (no new joint, no new leak path), and the
# neck doubles as the covered first leg of the harness route (B5).
top = Pos(0, 0, Z_TOP_BOT + TOP_T / 2) * Cylinder(TOP_R, TOP_T)
NECK_Z0, NECK_Z1 = Z_TOP_TOP, Z_PLATE_BOT
NECK_CAP_BOT = Z_PLATE_BOT - NECK_CAP_T
# r3: the neck's +Y face is stepped back to NECK_YP0 at the base and flares
# out to NECK_A at NECK_FLARE_ANG (see the parameter block: this is what
# frees the fill cap). The flare half-space is built once and offset along
# its own NORMAL for the inner face, so the wall stays NECK_WALL thick
# measured perpendicular to the sloped face (2.6 mm, not 2.6*sin = 1.84).
_fa = math.radians(NECK_FLARE_ANG)
_fn = (math.sin(_fa), -math.cos(_fa))          # (y, z) unit normal, outward
NECK_FLARE_Z = NECK_Z0 + NECK_YP_H             # where the flare starts
NECK_FLARE_H = (NECK_A - NECK_YP0) / math.tan(_fa)


def _relief_cut(y0, zf):
    """Material to remove: a vertical face at y0 up to zf, then a FLARE at
    NECK_FLARE_ANG out to the full section."""
    L = 300.0
    half = Pos(0, y0 + _fn[0] * L / 2, zf + _fn[1] * L / 2) * Rot(
        X=-(180.0 - NECK_FLARE_ANG)) * Box(600, 600, L)
    half &= Pos(0, 0, zf + 150.0) * Box(600, 600, 300)          # keep z >= zf
    slab = Pos(0, y0 + 150.0, (NECK_Z0 - 2.0 + zf) / 2) * Box(
        600, 300, zf - NECK_Z0 + 2.0)
    return half + slab


_neck_o = Pos(0, 0, (NECK_Z0 + NECK_Z1) / 2) * Box(2 * NECK_A, 2 * NECK_A, NECK_H)
_neck_o -= _relief_cut(NECK_YP0, NECK_FLARE_Z)
top += _neck_o
_neck_i = Pos(0, 0, (NECK_Z0 + NECK_CAP_BOT) / 2) * Box(
    2 * (NECK_A - NECK_WALL), 2 * (NECK_A - NECK_WALL), NECK_CAP_BOT - NECK_Z0)
# inner boundary = outer boundary offset NECK_WALL along its own normal, so
# the wall is NECK_WALL thick measured PERPENDICULAR to the sloped face (a
# naive y-offset would leave 2.6*sin60 = 2.25 there).
_neck_i -= _relief_cut(NECK_YP0 - NECK_WALL,
                       NECK_FLARE_Z - _fn[1] * NECK_WALL
                       - (NECK_WALL - _fn[0] * NECK_WALL) * math.tan(_fa))
top -= _neck_i
# mount inserts: bores open DOWNWARD out of the cap underside (heat-set from
# inside the neck), screws come down from the drone side through the mapped
# vendor holes. B9a: grip and thread engagement are printed in the checks.
BOSS_R = 3.9
INSERT_TOP = NECK_CAP_BOT + MOUNT_INSERT_L
for sx in (1, -1):
    for sy in (1, -1):
        top -= Pos(sx * BOLT_DX, sy * BOLT_DY, (INSERT_TOP + Z_PLATE_BOT) / 2
                   ) * Cylinder(1.25, Z_PLATE_BOT - INSERT_TOP + 2)
        top -= Pos(sx * BOLT_DX, sy * BOLT_DY,
                   NECK_CAP_BOT + MOUNT_INSERT_L / 2 - 0.005) * Cylinder(
            MOUNT_INSERT_D / 2, MOUNT_INSERT_L)
# --- blind-mate PCB WELL (r6, interference BLOCKING #2; now in the cap) --
# The board mounts to the CLIP PLATE's own 4 tabs inside its 16x24 shaft
# (mapped above), pads up. The payload has to (a) not be in the way, (b)
# house the Molex J1 + service loop under it, (c) get the harness out to the
# electronics bay without crossing the pellet space. The well is now a
# through-window in the neck cap: the board closes it from above and the
# connector hangs into the neck, which is the harness conduit.
top -= Pos(0, 0, (Z_PLATE_BOT + 1 + NECK_CAP_BOT - 0.5) / 2) * Box(
    WELL_X, WELL_Y, (Z_PLATE_BOT + 1) - (NECK_CAP_BOT - 0.5))
# harness exit slot at the base of the neck's -Y wall, on the conduit axis
CONDUIT_R_O, CONDUIT_R_I = 4.5, 3.0
# the tube is sunk 1.5 mm INTO the plate face: a tangent union is a degenerate
# boolean (it silently ate the whole part on the first attempt).
CONDUIT_ZC = Z_TOP_TOP + CONDUIT_R_O - 1.5
# r2 (B10): -(TOP_R + CONDUIT_R_O) put the Dia9 spigot EXACTLY tangent to
# the Dia156 plate rim -- two vertical cylinders touching along a line, which
# is what left top_plate_r8.stl with a 4-face edge at (0, -78, -238.55).
# 1.5 mm inboard makes it a proper transversal intersection.
CONDUIT_Y = -(TOP_R + CONDUIT_R_O - 1.5)         # -81.0, overlapping the rim
CONDUIT_Y_IN = -21.0                             # inside the neck -Y wall
CONDUIT_Z_BOT = Z_TOP_BOT - 10.0                 # spigot tip (into the hopper)
top -= Pos(0, -NECK_A, CONDUIT_ZC) * Box(NECK_CABLE_W, 3 * NECK_WALL,
                                         2 * CONDUIT_R_I)
# top-plate conduit: a CLOSED tube on the top face from the neck wall to the
# rim, then an elbow down to a spigot that plugs into the hopper conduit.
# B5.5: the harness is covered, not lying in an open channel.
top += Pos(0, (CONDUIT_Y + CONDUIT_Y_IN) / 2, CONDUIT_ZC) * Rot(X=90) * Cylinder(
    CONDUIT_R_O, CONDUIT_Y_IN - CONDUIT_Y)
top += Pos(0, CONDUIT_Y, (CONDUIT_ZC + CONDUIT_R_O + CONDUIT_Z_BOT) / 2
           ) * Cylinder(CONDUIT_R_O, CONDUIT_ZC + CONDUIT_R_O - CONDUIT_Z_BOT)
# r2 (B10): the horizontal conduit tube crossed the plate's OUTER RIM
# cylinder at exactly x = 0, y = -TOP_R, where the tube's bottom generator is
# horizontal and the rim's is vertical -- OCC emitted a degenerate edge there
# and top_plate_r8.stl came out with 1 non-manifold (4-face) edge at
# (0.000, -78.000, -238.550..-235.050). A rectangular STRAIN-RELIEF BOSS now
# buries that crossing, so the rim is cut by flat faces, transversally.
# r5 (integration BLOCKING FAIL): this boss used to be unioned on AFTER both
# conduit bores were cut, so it re-filled the elbow -- measured on
# top_plate_r10.stl the vertical bore axis was SOLID over z -237.50..-225.00
# and the horizontal bore axis SOLID over y -84.00..-72.00, i.e. the largest
# conductor that could cross the elbow was Dia0.0 and directive 2's harness
# route did not exist. The boss is now unioned BEFORE the bores, so the bores
# are cut THROUGH it; the tangency it exists to bury is still buried.
top += Pos(0, -TOP_R, (Z_TOP_BOT + 1.0 + CONDUIT_ZC + CONDUIT_R_O + 1.0) / 2
           ) * Box(15.0, 12.0,
                   (CONDUIT_ZC + CONDUIT_R_O + 1.0) - (Z_TOP_BOT + 1.0))
top -= Pos(0, (CONDUIT_Y + CONDUIT_Y_IN + 2.0) / 2, CONDUIT_ZC) * Rot(X=90) * \
    Cylinder(CONDUIT_R_I, CONDUIT_Y_IN + 2.0 - CONDUIT_Y)
top -= Pos(0, CONDUIT_Y, (CONDUIT_ZC + CONDUIT_Z_BOT - 0.5) / 2) * Cylinder(
    CONDUIT_R_I, CONDUIT_ZC - CONDUIT_Z_BOT + 0.5)
# r5: the elbow itself -- the two bores meet at (0, CONDUIT_Y, CONDUIT_ZC) at
# a right angle, and a bundle cannot turn a square corner. A quarter-torus
# fillet of the same Dia6.0 section is swept between them so the inside of
# the corner is a radius, not a step. Swept as 16 overlapping cylinders
# (an OCC sweep on a circular path is a degenerate-prone operation here).
ELB_R = 8.0                                   # elbow centreline radius
_ec_y, _ec_z = CONDUIT_Y + ELB_R, CONDUIT_ZC - ELB_R
for _i in range(17):
    _a = math.radians(90.0 * _i / 16.0)
    _py = _ec_y - ELB_R * math.cos(_a)
    _pz = _ec_z + ELB_R * math.sin(_a)
    top -= Pos(0, _py, _pz) * Sphere(CONDUIT_R_I)
# 2x cable-tie anchors beside the conduit at the rim.
# r6 (granule-path MODERATE 1): r2-r11 cut these as THROUGH slots --
# Box(2.2, 5.0, TOP_T + 2) at (+/-9, -66) -- and an upward-ray grid scan from
# inside the barrel found them: 2 x 11.00 mm2 of clear opening at plan radius
# 66.61 mm, i.e. INSIDE the measured barrel bore r 69.978, with no material
# at any z above them. The granule bed was open to the sky through 22.00 mm2
# (largest passing sphere Dia2.200): granules could not fall out, but fines,
# dust and water went both ways, straight onto the bed -- against the two
# mechanisms (RT-7 swelling, RT-8 landing dust) the fragment-jam requirement
# exists for. The model's own tank-vent self-check used 12 HAND-PLACED
# columns, none within 40 mm of (+/-9, -66), and printed "0 of 12 open" for
# nine rounds; it is a grid scan from this round on.
# The tie function is kept as ADDITIVE bridges on the top face: two 2.0 mm
# legs and a 2.2 mm bar over a 4.0 (y) x 2.4 (z) tunnel running in x. No hole
# is made in the lid at all.
for sx in (1, -1):
    top += Pos(sx * 9.0, -66.0, Z_TOP_TOP + 2.3) * Box(3.0, 9.0, 4.6)
    top -= Pos(sx * 9.0, -66.0, Z_TOP_TOP + 1.2) * Box(5.0, 4.0, 2.4)
# fill port: bore + cap recess + FACE GLAND + the two INWARD bayonet lugs.
# Nothing is cut radially outboard of FILL_R at any z, so the plate's top
# face is unbroken and the gland is a closed 360 deg loop (B5-b) -- both
# asserted on the export below.
top -= Pos(*FILL_POS, Z_TOP_BOT + TOP_T / 2) * Cylinder(FILL_R, TOP_T + 2)
CAP_RECESS_FLOOR = Z_TOP_TOP - CAP_RECESS_DEEP
top -= Pos(*FILL_POS, Z_TOP_TOP - CAP_RECESS_DEEP / 2 + 0.005) * Cylinder(
    CAP_RECESS_R, CAP_RECESS_DEEP)
# B5-b / N8: the fill joint's seal is now REAL geometry on an unbroken face
top -= Pos(*FILL_POS, CAP_RECESS_FLOOR - CAP_SEAL_D / 2 + 0.005) * (
    Cylinder(CAP_SEAL_R + CAP_SEAL_W / 2, CAP_SEAL_D)
    - Cylinder(CAP_SEAL_R - CAP_SEAL_W / 2, CAP_SEAL_D + 2))
# the two lugs: coplanar with the plate's bottom face (in-plane first-layer
# geometry), rooted 0.5 mm into the bore wall so the union cannot be
# degenerate, protruding to LUG_RI -> FILL_R - LUG_RI = 3.0 mm of engagement.
LUG_Z0, LUG_Z1 = Z_TOP_BOT, Z_TOP_BOT + LUG_T
for ang in LUG_AS:
    top += Pos(*FILL_POS, 0) * Rot(Z=ang) * (
        Pos((LUG_RI + FILL_R + 0.5) / 2, 0, (LUG_Z0 + LUG_Z1) / 2)
        * Box(FILL_R + 0.5 - LUG_RI, LUG_W, LUG_T))
# N5 anti-rotation detent: the DIMPLE half, cut into the recess wall at the
# locked angle. The cap's sprung tab drops into it (the spring half is on the
# cap); both halves and the deflection are measured in the checks.
CAP_DET_BUMP_R = CAP_RECESS_R + CAP_DET_PROUD          # 27.90, tab tip reach
CAP_DET_RC = CAP_DET_BUMP_R + 0.3 - (CAP_DET_D / 2 + 0.2)
top -= Pos(*FILL_POS, 0) * Rot(Z=CAP_DET_A) * (
    Pos(CAP_DET_RC, 0, (CAP_RECESS_FLOOR + Z_TOP_TOP) / 2)
    * Cylinder(CAP_DET_D / 2 + 0.2, CAP_RECESS_DEEP + 0.4))
# hopper-flange screw holes (6x M3 through, screws into flange inserts)
for a in FLANGE_SCREW_AS:
    top -= Rot(Z=a) * (Pos(FLANGE_SCREW_R, 0, Z_TOP_BOT + TOP_T / 2) * Cylinder(1.6, TOP_T + 2))
# lightening pockets (3 sectors, 2.1 mm deep; clip, fill-port and pedestal
# zones stay solid).  r4: cut from the BOTTOM face instead of the top, and
# held inside r68 (clear of the hopper wall/flange seat) -- printed
# top-face-down they now open upward and need no support.
# r6: pockets deepened 2.15 -> 3.0 (2.0 mm of plate left) and a 4th sector
# added -- the geared drive costs 110 g and this is free stiffness-neutral mass
# r2 (B11): the round-2 additions (symmetric harness duct, sensor covers +
# ears, bay riser, thicker hopper conduit) are all additive, and B11.3 forces
# the stepper to >= 350 g, so the ledger has to be paid for somewhere. The
# lightening pattern goes from 4 x 42 deg (168 deg) to 6 x 46 deg (276 deg),
# keeping theta 53..129 solid for the fill port / cap recess and leaving
# 2.0 mm of plate everywhere. Measured saving is printed in the ledger.
for (a0, a1) in ((129, 175), (177, 223), (225, 271), (273, 319),
                 (321, 367), (9, 53)):
    top -= sector(32, 68.0, a0, a1, Z_TOP_BOT - 0.05, 3.0)
add("top_plate", top, "#c9c2b4", density=DENS["petg_cf"],
    basis="[D] solid volume, CF-PETG; integral 42 mm stand-off NECK (B6) "
          "carrying the M2 inserts at the MAPPED clip pattern, the blind-mate "
          "PCB well and the covered harness conduit to the -Y rim")

# --- 3. quarter-turn fill cap (real bayonet: neck + lugs + wing grip) --
# r3 connectivity fix: neck extended UP into the flange (1.0 mm overlap) and
# DOWN past the lugs; lugs widened radially INTO the neck (2 mm overlap).
recess_floor = CAP_RECESS_FLOOR
CAP_FL_BOT = recess_floor + CAP_SEAL_GAP     # rides on the compressed cord
cap = Pos(*FILL_POS, CAP_FL_BOT + CAP_T / 2) * Cylinder(CAP_FLANGE_R, CAP_T)
# r3: the cap is now the SLOTTED half of the bayonet. Its spigot is a downward
# -open cup (wall 2.6+ at the groove root) that reaches into the plate's
# sealing skirt; the O-ring gland sits on the continuous part of that skirt
# bore, BELOW the lugs, so the seal is a full 360 deg (r8: 42 deg of the
# gland plane was open slot). Extraction is a pure axial lift of CAP_LIFT mm
# with NO lateral travel and NO obstruction above it -- measured below.
CAP_BOT = Z_TOP_BOT - 1.0                           # 1.0 mm below the lugs
CAP_NECK_TOP = CAP_FL_BOT + 1.5                     # buried in the flange
CAP_GRV_ZC = (LUG_Z0 + LUG_Z1) / 2
CAP_GRV_H = LUG_T + 0.2                             # 0.1 mm axial play/side
CAP_GRV_RI = LUG_RI - 0.4                           # groove root
CAP_BORE_R = 17.0                                   # spigot cored out
cap += Pos(*FILL_POS, (CAP_BOT + CAP_NECK_TOP) / 2) * Cylinder(
    CAP_NECK_R, CAP_NECK_TOP - CAP_BOT)
cap -= Pos(*FILL_POS, (CAP_BOT - 1.0 + CAP_FL_BOT + 0.5) / 2) * Cylinder(
    CAP_BORE_R, (CAP_FL_BOT + 0.5) - (CAP_BOT - 1.0))
# circumferential lug groove (the lugs run in this when locked)
cap -= Pos(*FILL_POS, CAP_GRV_ZC) * (Cylinder(CAP_NECK_R + 1.0, CAP_GRV_H)
                                     - Cylinder(CAP_GRV_RI, CAP_GRV_H + 2))
# axial entry slots, from the spigot's bottom end up to the groove: the cap
# is modelled LOCKED (turned 90 deg from insert), so the slots sit on the
# local +/-Y axis here while the plate lugs are on +/-X.
for ang in (90.0, 270.0):
    cap -= Pos(*FILL_POS, 0) * Rot(Z=ang) * (
        Pos((CAP_GRV_RI + CAP_NECK_R + 1.0) / 2, 0,
            (CAP_BOT - 1.0 + CAP_GRV_ZC + CAP_GRV_H / 2) / 2)
        * Box(CAP_NECK_R + 1.0 - CAP_GRV_RI, LUG_W + 1.0,
              (CAP_GRV_ZC + CAP_GRV_H / 2) - (CAP_BOT - 1.0)))
# wing-bar grip on the ACCESSIBLE top face. The cap is a loose part handled
# with gloves in wind (Judge 2's field-ops lens), so it needs a lanyard.
# r6 (found by this round's new tank-roof GRID SCAN, granule-path MODERATE 1
# class): rounds 1-5 made the lanyard hole a VERTICAL Dia2.2 x 8 cylinder at
# local (+10, 0) -- which went through the wing bar AND the CAP_T = 2.5 mm
# flange, i.e. straight into the fill bore. Measured on fill_cap_r12 before
# the fix: a vertical ray at (10.0, 43.0) hit NO cap material at all, and 13
# grid cells = 3.25 mm2 of granule bed were open to the sky at radius
# 9.0..11.0 mm from the fill axis -- INSIDE the O-ring gland at r = 25.0, so
# nothing seals it. The bar is now raised on two legs instead: the lanyard
# passes UNDER it, through a 16 x 8 x 2.5 mm tunnel, and the cap has no
# through-hole anywhere.
CAP_BAR_LIFT = 2.5
_bar_z0 = CAP_FL_BOT + CAP_T - 0.15 + CAP_BAR_LIFT
cap += Pos(FILL_POS[0], FILL_POS[1], _bar_z0 + 1.65) * Box(24, 8, 3.3)
for _sx in (1, -1):
    cap += Pos(FILL_POS[0] + _sx * 10.0, FILL_POS[1],
               CAP_FL_BOT + CAP_T - 0.15 + CAP_BAR_LIFT / 2) * Box(
        4, 8, CAP_BAR_LIFT)
# N5 detent, spring half: a tangential cantilever tab in the flange rim, its
# tip standing CAP_DET_PROUD proud of the recess wall and dropping into the
# plate's dimple at the locked angle. Freed by an arc slot behind it and a
# radial slot at its free end.
CAP_DET_RI = CAP_FLANGE_R - CAP_DET_TAB_T                      # 25.30
_dz = CAP_FL_BOT + CAP_T / 2
cap -= Pos(*FILL_POS, 0) * (sector(CAP_DET_RI - CAP_DET_SLOT_W, CAP_DET_RI,
                                   CAP_DET_A - CAP_DET_ARC, CAP_DET_A + 4.0,
                                   CAP_FL_BOT - 1.0, CAP_T + 2.0))
cap -= Pos(*FILL_POS, 0) * (sector(CAP_DET_RI - CAP_DET_SLOT_W, CAP_FLANGE_R + 2.0,
                                   CAP_DET_A + 4.0, CAP_DET_A + 4.0 + math.degrees(
                                       CAP_DET_SLOT_W / CAP_FLANGE_R),
                                   CAP_FL_BOT - 1.0, CAP_T + 2.0))
cap += Pos(*FILL_POS, 0) * Rot(Z=CAP_DET_A) * (
    Pos(CAP_DET_BUMP_R - 1.5, 0, _dz) * Cylinder(1.5, CAP_T))
add("fill_cap", cap, "#e8763a", density=DENS["petg"],
    basis="[D] volume; r3 INVERTED bayonet (slotted spigot + circumferential "
          "groove over the plate's inward lugs); face O-ring on an unbroken "
          "360 deg gland; N5 detent scallop; pure-axial extraction")

# --- 4. hopper shell (cylinder + 60 deg funnel + flange + tabs), printed
hop_outer = Pos(0, 0, Z_HOP_BOT + HOP_CYL_H / 2) * Cylinder(HOP_RI + HOP_WALL, HOP_CYL_H)
hop_outer += Pos(0, 0, Z_FUN_BOT + FUNNEL_H / 2) * Cone(
    FUNNEL_RO + HOP_WALL, HOP_RI + HOP_WALL, FUNNEL_H)
hop_void = Pos(0, 0, Z_HOP_BOT + HOP_CYL_H / 2 + 1) * Cylinder(HOP_RI, HOP_CYL_H + 2)
hop_void += Pos(0, 0, Z_FUN_BOT + FUNNEL_H / 2) * Cone(FUNNEL_RO, HOP_RI, FUNNEL_H)
hopper = hop_outer - hop_void
# top flange (r69.5..TOP_R, FLANGE_T tall; overlaps the wall -> one solid)
hopper += Pos(0, 0, Z_TOP_BOT - FLANGE_T / 2) * (
    Cylinder(TOP_R, FLANGE_T) - Cylinder(69.5, FLANGE_T + 2))
# flange heat-set insert holes (Dia4 x 6.0 deep, Ruthex RX-M3x5.7 + 0.3)
for a in FLANGE_SCREW_AS:
    hopper -= Rot(Z=a) * (Pos(FLANGE_SCREW_R, 0,
                              Z_TOP_BOT - FLANGE_INSERT_DEEP / 2 + 0.005)
                          * Cylinder(2.0, FLANGE_INSERT_DEEP))
# r4 skirt tabs (replace the un-fastenable funnel tabs): 3 vertical plates
# hanging outside the housing wall (r52.15..55.15, 10 wide, z -288.5..-273);
# the plate top overlaps the funnel cone wall volumetrically for z >-276.8
# (cone outer reaches r52.15 there) and never enters the hopper void (void
# inner surface stays < r52.15 below z=-272.4). Radial M3 clearance holes.
for a in SKIRT_AS:
    hopper += Rot(Z=a) * (Pos((SKIRT_R_IN + SKIRT_R_OUT) / 2, 0,
                              (SKIRT_Z0 + SKIRT_Z1) / 2)
                          * Box(SKIRT_R_OUT - SKIRT_R_IN, 10.0, SKIRT_Z1 - SKIRT_Z0))
    # root band: reaches inboard to the cone outer surface over
    # SKIRT_ROOT_Z0..Z1, so the tab roots into full wall thickness instead
    # of a thin wedge (the band stays outside the hopper VOID -- asserted).
    hopper += Rot(Z=a) * (Pos((FUNNEL_RO + HOP_WALL + SKIRT_R_OUT) / 2, 0,
                              (SKIRT_ROOT_Z0 + SKIRT_ROOT_Z1) / 2)
                          * Box(SKIRT_R_OUT - (FUNNEL_RO + HOP_WALL), 10.0,
                                SKIRT_ROOT_Z1 - SKIRT_ROOT_Z0))
    hopper -= Rot(Z=a) * (Pos((SKIRT_R_IN + SKIRT_R_OUT) / 2, 0, SKIRT_SCREW_Z)
                          * Rot(Y=90) * Cylinder(1.7, SKIRT_R_OUT - SKIRT_R_IN + 0.4))
# --- rev1 B5: HARNESS CONDUIT down the -Y outside of the tank -----------
# Thomas: "right now it looks like the wiring would go straight into the
# tank". This is the second covered leg of the route: a closed Dia12/Dia9.2
# tube from the top-plate spigot down to the electronics-bay lid... top face,
# webbed to the cone. Everything is OUTSIDE hop_void by construction (the web
# has the hopper void subtracted from it), which the B5.4 boolean re-proves.
# r2: Dia12/Dia9.2 -> Dia14/Dia11 so the bay's riser spigot can plug INTO
# it (the joint used to be a 3 mm air gap that also fouled the lid flange).
HOP_COND_RO, HOP_COND_RI = 7.0, 5.5
BAY_TOP = RIB_ZC + BAY_H / 2
# r2 (assembly critic BLOCKING A-3): the r1 conduit foot stopped 3.0 mm above
# the bay's TOP FACE, but the bay's LID FLANGE stands 4 mm proud of that face
# (BAY_FL_H = 50 vs BAY_H = 42) and reaches y = -88, so the Dia12 conduit
# (y -88.5..-76.5) overlapped it by 6.0000 mm3 -- and the obstruction was
# CONSTANT along the whole +Y insertion sweep, so neither the bay nor its lid
# could be seated at all. The foot now clears the flange top, and a riser
# SOCKET on the bay top face closes the gap so the harness stays covered.
HOP_COND_Z0 = RIB_ZC + BAY_FL_H / 2 + 1.5
HOP_COND_Z1 = Z_TOP_BOT - 2.0
# r2: CONDUIT_Y moved 1.5 mm inboard (B10 tangency fix), which brings the
# top plate's Dia9 conduit SPIGOT inside the hopper flange OD -- clearance
# bore for it, or the two rigid parts share 6.8 mm3.
hopper -= Pos(0, CONDUIT_Y, Z_TOP_BOT - FLANGE_T / 2) * Cylinder(
    CONDUIT_R_O + 0.6, FLANGE_T + 4)
hopper += Pos(0, CONDUIT_Y, (HOP_COND_Z0 + HOP_COND_Z1) / 2) * Cylinder(
    HOP_COND_RO, HOP_COND_Z1 - HOP_COND_Z0)
_web = Pos(0, (CONDUIT_Y + 30.0) / 2, (HOP_COND_Z0 + HOP_COND_Z1) / 2) * Box(
    3.0, 30.0 - CONDUIT_Y, HOP_COND_Z1 - HOP_COND_Z0)
hopper += _web - hop_void
hopper -= Pos(0, CONDUIT_Y, (HOP_COND_Z0 - 1 + HOP_COND_Z1 + 1) / 2) * Cylinder(
    HOP_COND_RI, HOP_COND_Z1 - HOP_COND_Z0 + 2)
add("hopper", hopper, "#ded7c8", density=DENS["petg_cf"],
    basis="[D] shell volume, 2.3 mm wall CF-PETG, 68 deg funnel + flange/tabs "
          "+ integral -Y harness conduit (B5)")

# --- 5. meter housing (roof + chamber wall + latch ring), printed ------
# r3: ring merged FIRST via an overlap band, then all cuts re-applied.
housing = Pos(0, 0, Z_RPLATE_TOP + (Z_FUN_BOT - Z_RPLATE_TOP) / 2) * Cylinder(
    HOUSING_R, Z_FUN_BOT - Z_RPLATE_TOP)
# quarter-turn latch RECEIVER ring + overlap band (joins housing wall r47..52)
ring_bot = Z_RPLATE_BOT - RING_DROP
band_top = Z_RPLATE_TOP + RING_BAND_H
ring = Pos(0, 0, (ring_bot + band_top) / 2) * Cylinder(RING_RO, band_top - ring_bot)
ring -= Pos(0, 0, ((ring_bot - 1) + (Z_RPLATE_TOP + 0.2)) / 2) * Cylinder(
    RING_RI, (Z_RPLATE_TOP + 0.2) - (ring_bot - 1))
ring -= Pos(0, 0, ((Z_RPLATE_TOP + 0.2) + (band_top + 1)) / 2) * Cylinder(
    50.0, (band_top + 1) - (Z_RPLATE_TOP + 0.2))
housing += ring
# detent plunger boss (radial, theta=PLUNGER_A). rev1 B9c / r5 assembly
# BLOCKING A-11: r6 bored a plain Dia5.10-5.20 clearance hole, and r7-r11
# added an outer Dia6.4 x 10 counterbore whose comment CALLED it a heat-set
# insert seat -- but no M5 insert was ever ordered in cad/BOM.md, so the
# measured part was still "Dia5.199 over r 47.00..52.90 and Dia6.399 over
# r 53.00..63.00, unthreaded" and an M5x0.8 plunger dropped straight through.
# The detent is 96.5 of the 190.7 mN*m reaction budget, so it is not optional.
# r6 takes B9c's FIRST branch (a modelled thread-forming boss), because it
# needs no COTS part whose bore spec I cannot verify from a datasheet I have
# actually read: PLUNGER_PILOT_D over PLUNGER_PILOT_L, with a short Dia5.2
# NOSE clearance at the inboard end (the Dia5.0 ball cannot pass a Dia4.5
# thread pilot, so the ball has to have its own bore to reach the disc-rim
# dimples at r = DISC_R).
PLUNGER_ZC = Z_DISC_TOP - DISC_T / 2
PLUNGER_BOSS_R = 6.0
PLUNGER_OUT_R = HOUSING_R + 11.0        # outer face of the boss
PLUNGER_PILOT_D = 4.5      # [A] thread-forming pilot for M5x0.8 in CF-PETG
                           # (0.90 x D). B9c asks Dia4.2-4.6 +/- 0.1.
PLUNGER_NOSE_D = 5.2       # ball clearance, chamber wall -> pilot mouth
PLUNGER_NOSE_R0 = CHAMBER_R           # 47.0, opens into the disc chamber
PLUNGER_NOSE_R1 = CHAMBER_R + 2.5     # 49.5, pilot starts here
PLUNGER_PILOT_L = PLUNGER_OUT_R - PLUNGER_NOSE_R1     # 13.5 mm (B9c: >= 6)
PLUNGER_BODY_L = 16.0      # BOM body length; ball tip reaches r = 47.0 with
                           # the body flush at r = 63.0, and screws in to the
                           # DIMPLE_DEPTH seat at r = DISC_R from there
housing += Rot(Z=PLUNGER_A) * (Pos(HOUSING_R + 4, 0, PLUNGER_ZC) * Rot(Y=90)
                               * Cylinder(PLUNGER_BOSS_R, 14))
# disc chamber
housing -= Pos(0, 0, Z_RPLATE_TOP + (Z_ROOF_BOT - Z_RPLATE_TOP) / 2) * Cylinder(
    CHAMBER_R, Z_ROOF_BOT - Z_RPLATE_TOP)
# open fill sector through the roof (sump floor IS the disc).
# r4 (pellet-path MINOR): cut outer radius reduced 47.5 -> 47.0 (chamber
# wall) -- the old cut left a 1 mm deep dead dust ledge at r47..47.5.
housing -= sector(20.0, CHAMBER_R, FILL_ARC[0], FILL_ARC[1], Z_ROOF_BOT - 1, ROOF_T + 2)
# ...and the remaining 0.5 mm step under the funnel outlet (r47..47.5 at
# roof top) gets a 45 deg chamfer ring over the fill arc: dust slides down
# funnel -> chamfer -> vertical wall -> rim trough instead of camping.
chamf = sector(46.7, 48.25, FILL_ARC[0], FILL_ARC[1], Z_FUN_BOT - 1.25, 1.30)
chamf &= Pos(0, 0, Z_FUN_BOT - 0.625) * Cone(46.95, 48.2, 1.25)
housing -= chamf
# r5 (buildability BLOCKER + GAP "no bearings"): the roof centre is now a
# BEARING SEAT, not a clearance hole. Bore Dia22 for an iglidur-class
# flanged sleeve bushing + a Dia26.4 x 0.7 counterbore in the sump floor so
# the flange stands 0.3 mm proud and carries the agitator's thrust load.
# The disc hub (Dia20) journals in it -> the Dia92 disc is no longer
# radially located by the stepper's internal bearings alone, and the
# agitator (which sits ON the floor, driven by the hub hex) does not have to
# come out with the cartridge.
# rev1 B9d: seat bore 23.100 -> 23.030 (igus asks H7 on the housing bore;
# +0.05/side was a slip fit with no retention modelled).
housing -= Pos(0, 0, Z_FUN_BOT - ROOF_T / 2) * Cylinder(BUSH_OD / 2 + 0.015, ROOF_T + 2)
housing -= Pos(0, 0, Z_FUN_BOT - BUSH_CB_DEPTH / 2 - 0.05) * Cylinder(
    BUSH_FL_OD / 2 + 0.2, BUSH_CB_DEPTH + 0.1)
# --- r6: TRUE UNDERSIDE LEAD-IN RAMP at the transfer-arc entry ---------
# r5 BLOCKING (pellet-path): the r5 "ramp" was cut into the roof TOP; the
# pellet-facing ceiling was a square step (None at 130.00 deg, 1.508 mm at
# 129.90). r6 cuts the RAMP INTO THE UNDERSIDE as an inclined plane through
# the radial line theta = FILL_ARC[0]: the ceiling starts at the roof TOP at
# the entry and descends at RAMP_DEG to disc+ROOF_CLEAR. Because the plane
# contains that radial line, the ramp starts at exactly the same angle at
# every radius and the slope along the arc is RAMP_DEG at every radius [D].
# rev1 B1 -- THE ROOF THROUGH-SLOT AT theta=310.
# r6 built the cut as `ramp_half & Box(400,200,100)` (a half-plane y' <= 0)
# and then Rot(Z=130). The half-plane runs 180 deg away from the entry, and
# on the -x' axis -- theta = 310 -- the inclined plane has descended below the
# roof, so the boolean removed the ENTIRE roof section there: RT-1 measured
# 0.000 mm of roof at theta=310.0 at every radius, on the same edge that made
# meter_housing non-manifold (B10). Two errors compounded: (a) the cut was
# not confined to a sector, and (b) a PLANE makes the ceiling a function of
# TANGENTIAL DISTANCE, so at r=20.5 the same plane is still 5.7 mm into the
# roof 34 deg downstream, which no acceptance test could pass.
# rev1 builds the ramp as a discretised HELICOID instead: the ceiling height
# is a function of ANGLE alone, so the ramp starts and ENDS at the same angle
# at every radius. Each 1 deg slice is cut by a plane tangent to the helicoid
# at the slice mid-angle (matched at the PCD), so the ceiling is a genuinely
# inclined face, not a staircase; the residual step between slices is
# +/-(dz/dtheta)*(dtheta/2)*(r/PCD - 1) <= 0.06 mm.
_ra = math.radians(RAMP_DEG)
RAMP_DZDTH = math.tan(_ra) * PCD_R           # mm of ceiling per radian
RAMP_ARC_DEG = math.degrees(ROOF_T / RAMP_DZDTH)   # 34.6 deg
RAMP_A1 = FILL_ARC[0]                        # entry edge, fully open
RAMP_A0 = FILL_ARC[0] - RAMP_ARC_DEG         # ramp foot, full roof again
RAMP_RUN = math.radians(RAMP_ARC_DEG) * PCD_R      # tangential run at PCD
_NSLICE = int(round(RAMP_ARC_DEG))
ramp_cut = None
for _i in range(_NSLICE):
    _a_hi = RAMP_A1 - _i * RAMP_ARC_DEG / _NSLICE
    _a_lo = RAMP_A1 - (_i + 1) * RAMP_ARC_DEG / _NSLICE
    _amid = (_a_hi + _a_lo) / 2
    # ceiling height (above Z_ROOF_BOT) at the slice mid-angle
    _zc = Z_ROOF_BOT + ROOF_T * (_amid - RAMP_A0) / RAMP_ARC_DEG
    # half-space BELOW the tangent plane, in the slice's own frame
    _hs = Pos(0, 100 * math.sin(_ra), _zc - 100 * math.cos(_ra)) * Rot(
        X=RAMP_DEG) * Box(400, 400, 200)
    _sl = sector(18.0, CHAMBER_R, _a_lo - 0.02, _a_hi + 0.02,
                 Z_ROOF_BOT - 1.0, ROOF_T + 2.0)
    _piece = _sl & (Rot(Z=_amid) * _hs)
    ramp_cut = _piece if ramp_cut is None else ramp_cut + _piece
housing -= ramp_cut
# --- r2: REVERSE-DIRECTION relief at the sump window's other edge -------
# granule-path MODERATE 1: "the whole rejection train is one-directional; the
# stall-recovery stroke drives fragments into square walls". Measured on the
# r7 export: the roof edge at theta = 250.00 presents 292.9 mm2 of face to a
# reverse-oscillating pocket, 100 % of it vertical (|n_z| = 0.000), the
# largest single face 121.50 mm2 spanning h = 1.50..10.50. Recovery is
# exactly the motion that runs after a fragment stall, so that wall can
# create the second jam.
# The fix is the same helicoid, mirrored: the roof underside now ramps DOWN
# from the window edge at 250 deg into the covered arc at REV_RAMP_DEG. The
# pockets in this sector are EMPTY on the forward stroke (they have just
# passed the exit port at theta = 0 and have not reached the fill window
# yet), so removing roof section here cannot affect the granule path
# forwards; it only turns the reverse-facing wall into a lifting ramp.
REV_RAMP_DEG = 45.0
REV_DZDTH = math.tan(math.radians(REV_RAMP_DEG)) * PCD_R
REV_ARC_DEG = math.degrees(ROOF_T / REV_DZDTH)          # 16.1 deg
REV_A0 = FILL_ARC[1]                                    # 250, fully open
REV_A1 = FILL_ARC[1] + REV_ARC_DEG                      # full roof again
_NR = max(8, int(round(REV_ARC_DEG)))
rev_cut = None
for _i in range(_NR):
    _a_lo = REV_A0 + _i * REV_ARC_DEG / _NR
    _a_hi = REV_A0 + (_i + 1) * REV_ARC_DEG / _NR
    _amid = (_a_hi + _a_lo) / 2
    _zc = Z_ROOF_BOT + ROOF_T * (REV_A1 - _amid) / REV_ARC_DEG
    _hs = Pos(0, -100 * math.sin(math.radians(REV_RAMP_DEG)),
              _zc - 100 * math.cos(math.radians(REV_RAMP_DEG))) * Rot(
        X=-REV_RAMP_DEG) * Box(400, 400, 200)
    _sl = sector(18.0, CHAMBER_R, _a_lo - 0.02, _a_hi + 0.02,
                 Z_ROOF_BOT - 1.0, ROOF_T + 2.0)
    _piece = _sl & (Rot(Z=_amid) * _hs)
    rev_cut = _piece if rev_cut is None else rev_cut + _piece
housing -= rev_cut
# plunger bore (re-cut AFTER ring union so the band cannot block the plunger):
# r6 (A-11): Dia5.2 BALL clearance from the chamber wall out to r 49.5, then
# a Dia4.5 THREAD-FORMING PILOT for 13.5 mm to the boss face at r 63.0.
# A failing part looks like r11 did: one constant Dia5.2 section straight
# through into a Dia6.4 counterbore, with the section constant to 0.001 mm
# over both steps. The r6 section has to step DOWN, 5.2 -> 4.5, going out.
housing -= Rot(Z=PLUNGER_A) * (
    Pos((PLUNGER_NOSE_R0 - 3.0 + PLUNGER_NOSE_R1) / 2, 0, PLUNGER_ZC)
    * Rot(Y=90) * Cylinder(PLUNGER_NOSE_D / 2,
                           PLUNGER_NOSE_R1 - PLUNGER_NOSE_R0 + 3.0))
housing -= Rot(Z=PLUNGER_A) * (
    Pos((PLUNGER_NOSE_R1 + PLUNGER_OUT_R + 0.5) / 2, 0, PLUNGER_ZC)
    * Rot(Y=90) * Cylinder(PLUNGER_PILOT_D / 2, PLUNGER_PILOT_L + 0.5))
# rev1 B2: GRUB ACCESS PORT through the chamber wall on the grub axis, so the
# disc's shaft grub can be reached with a straight key without pulling the
# cartridge. Plugged with an M4 nylon set screw (BOM).
housing -= Rot(Z=GRUB_A) * (Pos(DISC_R + 4.0, 0, Z_DISC_TOP + SETSCREW_Z_OFF)
                            * Rot(Y=90) * Cylinder(1.8, 16.0))
# latch slots (cut after ring union).
# rev1 r3 -- ASSEMBLY BLOCKING A-7, "the drive has no reaction path". The r8
# slots ran a-6..a+30 with the entry at a+14..a+30, so the seated cartridge
# had a hard circumferential stop in -theta ONLY and 24.65 deg of FREE travel
# in +theta -- and +theta is exactly the direction the gearbox's stator
# reaction pushes the plate (the disc runs -theta), with the far end of that
# free band being the drop-out window. Restraint was lug friction, 0.068 N*m
# against 0.6527 N*m of drive torque: a 9.6x deficit.
# The handedness is now MIRRORED: entry at a-30..a-14, circumferential slot
# a-30..a+6. The cartridge is inserted at -22 deg and turned +22 deg to lock,
# so the motor's reaction drives it INTO the hard stop instead of out of the
# latch. The two-sided free-rotation band is scanned in the checks.
ring_h = PLATE_T + RING_DROP
for a in LUG_ANGLES:
    # circumferential slot at lug height (shelf below carries the plate load)
    housing -= sector(52.05, 55.55, a - 30, a + 6, Z_RPLATE_BOT - 0.2, PLATE_T + 0.5)
    # vertical entry slot (insert at a-22, rotate +22 deg to lock)
    housing -= sector(52.05, 55.55, a - 30, a - 14, Z_RPLATE_BOT - RING_DROP - 1, ring_h + 2)
# ...and a POSITIVE LOCK (A-7, second half). The mirrored latch takes the
# drive reaction on a hard shelf, but nothing stopped the cartridge walking
# BACK towards the entry slot under vibration, so a radial M3 thread-forming
# STOP PIN is driven through the ring wall into the empty part of the
# circumferential slot behind the seated lug. With it fitted the free band is
# bounded on both sides; both bands are scanned and printed in the checks.
LOCK_LUG_A = LUG_ANGLES[0]
LOCK_PIN_A = LOCK_LUG_A - 9.0              # 2.05 deg behind the locked lug's
                                           # trailing face (measured below)
LOCK_PIN_Z = Z_RPLATE_TOP - PLATE_T / 2
LOCK_PIN_LEN = 6.0                         # M3x6 -> tip at r = 52.8, i.e.
LOCK_PIN_TIP = 52.8                        # 0.8 mm clear of the plate rim
                                           # and 3.5 mm into the lug's path
housing -= Rot(Z=LOCK_PIN_A) * (Pos(56.8, 0, LOCK_PIN_Z) * Rot(Y=90)
                                * Cylinder(1.3, 4.0))
# r5 wiper seat (pellet-path MAJOR: the r4 "brush" was a solid printed fin
# with nowhere to put bristles). The seat is now a REBATE OPEN AT THE TOP,
# cut from the sump floor down HOLD_H+0.15, running the whole radial span
# r13.5..52.6: over r20..47 the fill sector has already removed the roof, so
# the holder free-spans there and the bristles hang into open space; at the
# inner ring and at the wall top the rebate carries it. Radial slide-in/out
# is therefore a pure translation (swept-union probed below) and there is no
# thin "ceiling" section over the slot any more (r4 MINOR: 1.5 mm).
# rev1: the rebate is a BOX, so at small radii its tangential half-width is a
# large ANGLE: at r=24.5 an 18.3 mm box spans +/-21.4 deg, i.e. down to
# theta=126.6, which is 3.4 deg PAST the roof entry. Combined with the entry
# ramp that removed the whole roof there and opened a hole from the sump into
# the transfer arc DOWNSTREAM of the wiper -- a restack path straight into the
# descending ceiling. Both the seat and the holder are therefore clipped by a
# radial plane at the roof entry angle (seat at FILL_ARC[0], holder 0.4 deg
# inside it), which is still a pure radial slide, so the wiper still pulls out.
# r2 BUGFIX (round-1 assembly critic could not see this because the r7 export
# predated it): both keep-boxes were built at z = -200..+200, i.e. 116 mm
# ABOVE the wiper station (z ~ -316..-330). `housing -= (seat & SEAT_KEEP)`
# therefore subtracted NOTHING (the wiper seat rebate was silently missing)
# and `holder &= HOLD_KEEP` returned an EMPTY solid -- brush_holder came out
# 0.000 cm3 and export_step asserted. The keep half-spaces are now centred on
# the wiper station in Z, and both parts are volume-floor asserted below.
SEAT_KEEP = Rot(Z=FILL_ARC[0]) * (Pos(0, 200, Z_FUN_BOT) * Box(800, 400, 400))
HOLD_KEEP = Rot(Z=FILL_ARC[0] + 0.4) * (Pos(0, 200, Z_FUN_BOT) * Box(800, 400, 400))
housing -= (Rot(Z=BRUSH_A) * (Pos(29.5, 0, Z_FUN_BOT)
                              * Box(32.0, HOLD_W + 0.3, 2 * (HOLD_H + 0.15)))
            & SEAT_KEEP)
# ...and a full-height WINDOW through the chamber wall (r45.5..52.6) so the
# BRISTLES clear the wall on the way out: without it the strip drags through
# 13.8 mm3 of wall on retraction (measured before this was added).
WIN_Z0 = Z_DISC_TOP + BRUSH_WIPE - 0.3
housing -= Rot(Z=BRUSH_A) * (Pos(49.05, 0, (WIN_Z0 + Z_FUN_BOT + 2.15) / 2)
                             * Box(7.1, HOLD_W + 0.3, Z_FUN_BOT + 2.15 - WIN_Z0))
# wiper end-tab retention screw pilot (radial M3, in solid wall BELOW the
# window; the tab reaches down to meet it and stops 0.1 above the latch ring)
BRUSH_SCREW_Z = WIN_Z0 - 2.2
housing -= Rot(Z=BRUSH_A) * (Pos(49.9, 0, BRUSH_SCREW_Z) * Rot(Y=90) * Cylinder(1.25, 4.4))
# electronics-bay rib screw pilots (2x, M3 into wall, 5+ mm engagement)
for sx in (1, -1):
    housing -= Pos(sx * 14.0, (BAY_RIB_PILOT_Y0 + BAY_RIB_PILOT_Y1) / 2,
                   RIB_ZC) * Rot(X=90) * Cylinder(
        1.25, BAY_RIB_PILOT_Y1 - BAY_RIB_PILOT_Y0)
# r4 skirt-tab screw pilots (3x radial Dia2.5 x 4.4, r47.9..52.3 -- open at
# the housing OD, inner end 0.9 mm clear of the chamber wall r47)
for a in SKIRT_AS:
    housing -= Rot(Z=a) * (Pos(52.3 - SKIRT_PILOT_L / 2, 0, SKIRT_SCREW_Z)
                           * Rot(Y=90) * Cylinder(1.25, SKIRT_PILOT_L))
add("meter_housing", housing, "#8f8778", density=DENS["petg_cf"],
    basis="[D] volume, CF-PETG; latch ring merged via band; ramp; brush wall "
          "window + inner closed slot; radial skirt-screw pilots")

# --- 6. pocket disc ----------------------------------------------------
disc = Pos(0, 0, Z_DISC_TOP - DISC_T / 2) * Cylinder(DISC_R, DISC_T)
pocket_angles = [i * 360.0 / N_POCKET for i in range(N_POCKET)]
for a in pocket_angles:
    x = PCD_R * math.cos(math.radians(a))
    y = PCD_R * math.sin(math.radians(a))
    disc -= Pos(x, y, Z_DISC_TOP - DISC_T / 2) * Cylinder(POCKET_R, DISC_T + 2)
    # 2 mm x 45 deg top-edge chamfer (lead-in, anti-shear)
    disc -= Pos(x, y, Z_DISC_TOP - 1.0) * Cone(POCKET_R, POCKET_R + 2.0, 2.0)
    # per-pocket magnet (bottom face) -- phase verified EVERY index
    mx = MAG_R_POS * math.cos(math.radians(a))
    my = MAG_R_POS * math.sin(math.radians(a))
    disc -= Pos(mx, my, Z_DISC_BOT + MAG_DEPTH / 2 - 0.01) * Cylinder(MAG_R, MAG_DEPTH)
# rim detent dimples: HALF-STATION angles, RADIAL axes.
# r6 (pellet-path MAJOR: an unspecified M5 plunger in the r5 Dia4 x 1.5 deep
# dimple needs 0.2-1.1 N*m to release, up to 6x the whole r5 motor): the seat
# is now a SHALLOW SPHERICAL dimple, R6 x 0.6 deep, and the plunger is
# specified (PLUNGER_F). Release torque is computed in the checks.
# rev1 B2: dimples move to the POCKET angles and the plunger to 157.5 deg (see
# PLUNGER_A). Engagement needs dimple + phi = plunger, so phi = 22.5 deg
# (mod 45) in BOTH schemes -- the park phase, the 22.5 deg port offset and the
# ECO-2 magnet-under-the-112.5-Hall property are all unchanged (asserted).
dimple_angles = list(pocket_angles)
PARK_PHI = (PLUNGER_A - dimple_angles[0]) % 45.0
assert abs(PARK_PHI - 22.5) < 1e-9, "park phase moved: pockets no longer 22.5 off the port"
assert any(abs(((a + PARK_PHI) % 360.0) - HALL_INDEX_A) < 1e-6 for a in pocket_angles), \
    "ECO-2: no pocket magnet under the 112.5 deg index Hall at park"
for a in dimple_angles:
    disc -= Rot(Z=a) * (Pos(DISC_R + DIMPLE_SPH_R - DIMPLE_DEPTH, 0,
                            Z_DISC_TOP - DISC_T / 2) * Sphere(DIMPLE_SPH_R))
# index magnet (half-station offset -> absolute phase within half a station)
ia = 22.5
disc -= Pos(MAG_R_POS * math.cos(math.radians(ia)), MAG_R_POS * math.sin(math.radians(ia)),
            Z_DISC_BOT + MAG_DEPTH / 2 - 0.01) * Cylinder(MAG_R, MAG_DEPTH)
# lightening holes (r=18.5 band, clear of the r12-15 thrust-washer track).
# r6: Dia5 -> Dia7 + a 2.5 mm annular relief in the UNDERSIDE between the
# washer track and the pocket footprint (mass trim for the geared drive).
# rev1 N6: the r6 holes were Dia7 at r=18.5, spanning r 15.0..22.0 -- they
# broke through the sump window's inner edge (r=20.00) over a ~2 mm crescent,
# so pellet fines dropped straight into the under-plate space. They move to
# r=13.0 / Dia5.0 (span 10.5..15.5): the radial land to r=20.00 is 4.5 mm, and
# they clear the relocated thrust-washer track (r 16..19, B3) by 0.5 mm.
# They also move to the POCKET angles, which frees the half-station radii for
# the B2 grub corridor.
LIGHT_R, LIGHT_HOLE_R = 13.0, 2.5
for a in pocket_angles:
    disc -= Pos(LIGHT_R * math.cos(math.radians(a)), LIGHT_R * math.sin(math.radians(a)),
                Z_DISC_TOP - DISC_T / 2) * Cylinder(LIGHT_HOLE_R, DISC_T + 2)
disc -= Pos(0, 0, Z_DISC_BOT + 1.0 - 0.005) * (Cylinder(23.5, 2.0) - Cylinder(20.0, 4.0))
# rotation-direction arrow engraved on the disc top (points -theta = CW from
# above = direction of motion; r2 critic NOTE: direction was not asserted)
arrow = extrude(Polygon((0, -4.5), (2.4, 0), (-2.4, 0), align=None), amount=1.2)
disc -= Rot(Z=157.5) * (Pos(25.5, 0, Z_DISC_TOP - 0.8) * arrow)
# r5 hub: Dia20 JOURNAL (rides in the roof bushing) + HEX DRIVE SPIGOT for
# the agitator. The hex is what lets the whole cartridge drop straight out
# while the agitator stays in the hopper (r4 buildability BLOCKER).
Z_JOURNAL_TOP = Z_FUN_BOT - 0.5
disc += Pos(0, 0, (Z_DISC_TOP + Z_JOURNAL_TOP) / 2) * Cylinder(
    HUB_R, Z_JOURNAL_TOP - Z_DISC_TOP)
hex_spigot = extrude(RegularPolygon(HEX_AF / math.sqrt(3), 6), amount=HEX_LEN)
disc += Pos(0, 0, Z_JOURNAL_TOP) * hex_spigot
# 45 deg lead-in chamfer on the spigot top (blind hex re-entry by feel)
_hz = Z_JOURNAL_TOP + HEX_LEN - 0.6
disc -= Pos(0, 0, _hz) * (Cylinder(12.0, 1.2)
                          - Cone(HEX_AF / math.sqrt(3), HEX_AF / math.sqrt(3) - 1.2, 1.2))
# r6: BLIND Dia6.1 bore for the GEARBOX output shaft (Dia6 x 18 with a 12 mm
# D-cut). The D-flat -- not the set screw -- carries the 0.65 N*m recovery
# torque: bearing stress is computed in the checks. Bore stops 0.5 mm below
# the disc top so the journal/hex above stays solid material.
# rev1 B2 -- THE TORQUE PATH. r6 bored a plain Dia6.1 ROUND hole on a Dia6
# D-cut shaft (RT-1 measured r = 3.06 at all 24-36 angles and both heights),
# so nothing but a grub screw could transmit 0.65 N*m, and the grub pilot was
# a BLIND void ending at r=10.60 inside solid disc material -- the screw could
# not be inserted at all. The bore is now a real D-BORE: round at Dia6.10
# below the vendor's D-cut, and flat at r = 2.55 (0.05 mm off the shaft's
# 0.5 mm flat) over the full 12 mm of the D-cut. The FLAT carries the torque;
# the grub is axial retention only.
# r3 (assembly NB-1): the r8 blind bore face landed at exactly Z = -337.250,
# which is also the modelled shaft top -- 0.000 mm of designed axial
# clearance, so on any positive tolerance the SHAFT, not the PTFE thrust
# washer, would set the disc height and with it the 1.500 mm roof clearance.
# The bore now runs 1.0 mm past the shaft end into the solid hub journal.
Z_BORE_TOP = Z_DISC_TOP + 1.0
Z_DCUT_BOT = Z_MOTOR_TOP + MOTOR_SHAFT_LEN - MOTOR_SHAFT_DCUT
BORE_FLAT_R = MOTOR_SHAFT_R - MOTOR_SHAFT_FLAT + 0.05      # 2.55
_bore = Pos(0, 0, (Z_DISC_BOT - 2 + Z_BORE_TOP) / 2) * Cylinder(
    MOTOR_SHAFT_R + 0.05, Z_BORE_TOP - (Z_DISC_BOT - 2))
_flat_keep = Rot(Z=GRUB_A) * (Pos(BORE_FLAT_R + 25.0, 0,
                                  (Z_DCUT_BOT + Z_BORE_TOP + 1) / 2)
                              * Box(50.0, 50.0, Z_BORE_TOP + 1 - Z_DCUT_BOT))
disc -= (_bore - _flat_keep)
# M3 cup-point grub onto the shaft D-flat, on the SAME axis as the flat so it
# presses square on it. The corridor is continuous from the disc OD to the
# bore: Dia3.4 clearance r 9..47, then a Dia2.6 thread-forming pilot from
# r 9.25 down to a floor at r = 2.45 -- 0.10 mm INBOARD of the 2.55 bore
# flat, so the pilot breaks fully through the flat web and the cup point can
# reach the shaft at any +/-0.05 print tolerance. (rev1 close-out B2.2: the
# r12 pilot floored at r = 2.75 and left a full-section 0.200 mm CF-PETG web
# over the flat -- 1.0619 mm3 in the Dia2.6 corridor -- so the grub could
# never touch the shaft. Inboard of the flat plane is bore void; 0.10 mm of
# overshoot cuts nothing structural.)
# GRUB_A = 202.5 deg is a half-station: with the dimples moved to the pocket
# angles (above) it clears the pockets by 12.2 mm, the dimples by 17.6 mm and
# the lightening holes by 5.7 mm -- all measured in the checks.
Z_SETSCREW = Z_DISC_TOP + SETSCREW_Z_OFF
disc -= Rot(Z=GRUB_A) * (Pos(5.85, 0, Z_SETSCREW) * Rot(Y=90)
                         * Cylinder(GRUB_PILOT_R, 6.8))
disc -= Rot(Z=GRUB_A) * (Pos((9.0 + DISC_R + 1.0) / 2, 0, Z_SETSCREW)
                         * Rot(Y=90) * Cylinder(GRUB_CLEAR_R, DISC_R + 1.0 - 9.0))
add("pocket_disc", disc, "#e8763a", density=DENS["petg_cf"],
    basis="[D] volume w/ pockets+lightening, CF-PETG; -Z rotation arrow engraved")

# --- 7. PTFE thrust washer (pellet-bed load off the motor bearings) ----
# rev1 B3: the r6 washer (Dia30/Dia24, r 12..15) sat exactly where the
# corrected Dia26 bolt circle puts the 4 clearance holes (r 11.3..14.7), so it
# would have been supported on four holes. It moves OUTBOARD of the bolt
# circle to r 17..19 and the plate recess follows it.
WASH_RI, WASH_RO = 17.0, 19.0
WASH_SEAT_RI, WASH_SEAT_RO = 16.7, 19.3
washer = Pos(0, 0, Z_RPLATE_TOP - 1.0 + 0.05 + 0.7) * (
    Cylinder(WASH_RO, 1.4) - Cylinder(WASH_RI, 3))
add("thrust_washer", washer, "#f0ede4", density=DENS["ptfe"],
    basis="PTFE Dia38/Dia34x1.4 in plate recess (McMaster PTFE washer class, "
          "part TBD); disc rides it (0.05 modeled gap); OUTBOARD of the "
          "Dia26 motor bolt circle (B3)")

# --- 7b. sleeve bearing (COTS, r6: catalogued PN) ----------------------
# igus iglidur J flanged sleeve JFM-2023-07: ID20 / OD23 / L7 (r5's
# JFM-2022-04 could not be confirmed as a catalogued length -- buildability
# MODERATE). Seated in the roof-top counterbore; the flange stands 0.3 mm
# proud and is the agitator's thrust face. L/D = 0.35 (r5: 0.20).
Z_BUSH_FL_TOP = Z_FUN_BOT - BUSH_CB_DEPTH + BUSH_FL_T
bush = Pos(0, 0, Z_BUSH_FL_TOP - BUSH_FL_T / 2) * (
    Cylinder(BUSH_FL_OD / 2, BUSH_FL_T) - Cylinder(BUSH_ID / 2, BUSH_FL_T + 2))
bush += Pos(0, 0, Z_FUN_BOT - BUSH_CB_DEPTH - BUSH_LEN / 2) * (
    Cylinder(BUSH_OD / 2, BUSH_LEN) - Cylinder(BUSH_ID / 2, BUSH_LEN + 2))
add("sleeve_bearing", bush, "#d9a441", density=DENS["nylon"],
    basis="COTS igus iglidur J JFM-2023-07 (ID20/OD23/L7; flange Dia30x2 "
          "ASSUMPTION) -- length confirmed catalogued at distributors")

# --- 8. agitator (r5: independent rotor, hex-driven, sits on the floor) -
# r4 BLOCKER: the agitator was clamped to the disc hub, its fingers passed
# 0.5 mm over a solid roof, and the cartridge therefore could not descend
# (swept 1077 mm3 of housing). It is now a free rotor: it rests on the
# bushing flange, is centred by the hub journal/hex, and is driven by the
# HEX SPIGOT, which the cartridge simply slides out of. No set screw (r4's
# was unreachable inside the funnel throat with the hopper on).
AG_Z0 = Z_FUN_BOT + (BUSH_FL_T - BUSH_CB_DEPTH) + 0.05   # 0.05 over the flange
agit = Pos(0, 0, AG_Z0 + 2.275) * Cylinder(AGIT_FL_R, 4.55)
agit += Pos(0, 0, AG_Z0 + 4.55 + 1.5) * Cylinder(AGIT_COL_R, 3.0)
for a in (0, 120, 240):
    agit += Rot(Z=a) * (Pos((10.0 + AGIT_FINGER_RO) / 2, 0, AG_Z0 + 2.2)
                        * Rot(Y=90) * Cylinder(AGIT_FINGER_R, AGIT_FINGER_RO - 10.0))
# hex socket (open at the bottom, 0.4 mm across-flats clearance)
agit -= Pos(0, 0, AG_Z0 - 0.05) * extrude(
    RegularPolygon((HEX_AF + 0.4) / math.sqrt(3), 6), amount=6.1)
add("agitator", agit, "#4a4a4a", density=DENS["tpu"],
    basis="[D] volume, TPU; hex-driven free rotor on the bushing flange; "
          "fingers sweep to r46.7; unswept ring measured against the real "
          "cone foot, not the chamber wall (r5 pellet-path MINOR)")

# --- 9. wiper: printed HOLDER with a real bristle channel + COTS strip ---
# r4 pellet-path MAJOR: "the wiper is a solid printed fin with no bristle
# retention feature ... that falsifies concept 2.3 'compliant'". r5 splits
# it: brush_holder (printed, channelled) + brush_bristles (COTS strip).
hold_zc = Z_FUN_BOT - HOLD_H / 2 - 0.05
holder = Rot(Z=BRUSH_A) * (Pos(34.55, 0, hold_zc) * Box(36.1, HOLD_W, HOLD_H))
# end tab outside the housing OD (grip + RADIAL retention screw); it also
# closes the wall window from outside
TAB_Z0, TAB_Z1 = BRUSH_SCREW_Z - 2.5, Z_FUN_BOT
holder += Rot(Z=BRUSH_A) * (Pos(55.15, 0, (TAB_Z0 + TAB_Z1) / 2)
                            * Box(5.7, 10.0, TAB_Z1 - TAB_Z0))
holder -= Rot(Z=BRUSH_A) * (Pos(55.5, 0, BRUSH_SCREW_Z) * Rot(Y=90) * Cylinder(1.6, 9))
# r6: bristle channel at the LEADING edge (leading = +theta side = local +Y,
# because the disc runs -Z / CW seen from above), so the compliant element
# gets first contact at EVERY fragment height (r5 BLOCKING/MAJOR: the rigid
# holder led the bristles for everything more than 5.45 mm proud).
CHAN_Z0 = hold_zc - HOLD_H / 2                     # holder rail underside
CHAN_YC = HOLD_W / 2 - CHAN_W / 2 - 2.7   # r6: room for the rail chamfer
                                          # AND >=1.5 mm of web under it
holder -= Rot(Z=BRUSH_A) * (Pos(34.55, CHAN_YC, CHAN_Z0 + CHAN_H / 2 - 0.01)
                            * Box(36.3, CHAN_W, CHAN_H))
# r6: 45-deg chamfer on the RAIL's leading bottom edge, so even an object
# taller than the rail underside meets an inclined face (the r5 rigid face
# had n_z = 0.00: a pure square stub across the whole radial span).
# It is cut as an OVERHANG (bottom edge upstream of the top edge) so the
# face normal is up-and-upstream, i.e. it LIFTS: n = (0, +0.71, +0.71).
_c = math.sqrt(0.5)
# ...stopped 0.6 mm short of the rail top so the chamfer does not run out to
# a feather edge (printability: the wall-thickness harness sees it).
holder -= Rot(Z=BRUSH_A) * ((Pos(0, HOLD_W / 2 + 100 * _c, CHAN_Z0 + 100 * _c)
                             * Rot(X=-45) * Box(400, 400, 200))
                            & (Pos(0, 0, CHAN_Z0 + (HOLD_H - 0.6) / 2)
                               * Box(400, 400, HOLD_H - 0.6)))
# r6 DEFLECTOR NOSE on the TRAILING half: prism whose UPSTREAM face is a
# NOSE_ANG ramp reaching down to disc+NOSE_GAP. This is the rotary-airlock
# "inlet shear deflector" (RESEARCH-drone-spreaders 5, countermeasure 1) and
# it is CONTEXT requirement 1 ("rejection before wedge") in hardware: a
# proud fragment meets an inclined face in the OPEN FILL SECTOR, where the
# reaction has an upward component and there is an escape path into the sump.
NOSE_Z0 = Z_DISC_TOP + NOSE_GAP
NOSE_H = CHAN_Z0 - NOSE_Z0
NOSE_RUN = NOSE_H / math.tan(math.radians(NOSE_ANG))
NOSE_Y0 = CHAN_YC - CHAN_W / 2 - 0.5               # LOW TIP, upstream side
NOSE_Y1 = NOSE_Y0 - NOSE_RUN                       # top of the ramp, downstream
assert NOSE_Y1 > -HOLD_W / 2, "deflector ramp overruns the holder"
NOSE_R0, NOSE_R1 = 20.0, AGIT_FINGER_RO
# tip (y0, low) -> ramp up to (y1, rail underside) -> vertical downstream face
# 0.6 mm blunt vertical tip (a printed knife edge is not a design feature)
# r2 (granule-path MODERATE 1): the nose's TRAILING face was vertical too --
# 79.43 mm2 at theta ~ 136.7, n_z = 0.000, h 1.50..7.45 -- so a pocket parked
# in the 6.4 deg band between the ramp mouth and the nose met a square wall
# on the reverse (recovery) stroke. All of the holder width left downstream
# of the nose top is now spent on a reverse ramp. It is steeper than the
# forward 30 deg (there is only NOSE_REV_RUN of width left), so this is a
# PARTIAL fix and the residual vertical height is measured and published.
NOSE_REV_RUN = NOSE_Y1 + HOLD_W / 2 - 0.2
assert NOSE_REV_RUN > 1.5, "no width left for the reverse ramp"
NOSE_Y2 = NOSE_Y1 - NOSE_REV_RUN
NOSE_REV_DEG = math.degrees(math.atan2(NOSE_H, NOSE_REV_RUN))
nose_prof = Polygon((NOSE_Y0, NOSE_Z0), (NOSE_Y0, NOSE_Z0 + 0.6),
                    (NOSE_Y1, CHAN_Z0 + 0.01), (NOSE_Y2, NOSE_Z0), align=None)
holder += Rot(Z=BRUSH_A) * (Pos(NOSE_R0, 0, 0) * Rot(Z=90) * Rot(X=90)
                            * extrude(nose_prof, amount=NOSE_R1 - NOSE_R0))
# clip to the same radial plane as its seat (see SEAT_KEEP above)
holder &= HOLD_KEEP
add("brush_holder", holder, "#c9c2b4", density=DENS["petg_cf"],
    basis="[D] volume, CF-PETG; LEADING bristle channel + 45 deg deflector "
          "nose; slides out radially; M3 retention screw through the end tab")

# COTS strip brush: 1.6 mm backing in the channel + free trim to the wipe
# line. Trim length is measured and printed by the checks below.
BRIS_TIP = Z_DISC_TOP + BRUSH_WIPE
BRIS_TOP = CHAN_Z0 + CHAN_H - 0.06                 # 0.05 gap to the channel roof
bristles = Rot(Z=BRUSH_A) * (Pos((20.3 + AGIT_FINGER_RO) / 2, CHAN_YC,
                                 (BRIS_TOP + BRIS_TIP) / 2)
                             * Box(AGIT_FINGER_RO - 20.3, BRISTLE_W,
                                   BRIS_TOP - BRIS_TIP))
add("brush_bristles", bristles, "#2b2b2b", mass=3.0,
    basis="COTS nylon strip brush, 1.6 mm backing, short trim (Sealeze/Gordon "
          "class, PN ASSUMPTION); 3.0 g [J] -- r4 charged 10 g to a solid "
          "printed fin, which is what the pellet-path critic flagged")

# --- 10. retaining plate + integral chute (one printed part) -----------
rp = Pos(0, 0, Z_RPLATE_TOP - PLATE_T / 2) * Cylinder(HOUSING_R, PLATE_T)
# exit port with top chamfer, at theta=0, r=PCD
rp -= Pos(PCD_R, 0, Z_RPLATE_TOP - PLATE_T / 2) * Cylinder(PORT_R, PLATE_T + 2)
rp -= Pos(PCD_R, 0, Z_RPLATE_TOP - PORT_CHAMF / 2) * Cone(
    PORT_R, PORT_RIM_R, PORT_CHAMF)
# motor pilot + screws. rev1 B3: 4 x M3 on the datasheet Dia26 BOLT CIRCLE,
# i.e. ON THE AXES, not the r6 26 mm square at 45/135/225/315. Heads are
# COUNTERSUNK (DIN 7991) because the disc runs 0.5 mm above this face and a
# socket head would stand 3 mm into it.
rp -= Pos(0, 0, Z_RPLATE_TOP - PLATE_T / 2) * Cylinder(MOTOR_PILOT_R + 0.1, PLATE_T + 2)
MOTOR_HOLES = [(MOTOR_BC_R, 0.0), (-MOTOR_BC_R, 0.0),
               (0.0, MOTOR_BC_R), (0.0, -MOTOR_BC_R)]
for hx, hy in MOTOR_HOLES:
    rp -= Pos(hx, hy, Z_RPLATE_TOP - PLATE_T / 2) * Cylinder(
        MOTOR_SCREW_CLR, PLATE_T + 2)
    rp -= Pos(hx, hy, Z_RPLATE_TOP - 0.7) * Cone(MOTOR_SCREW_CLR, 3.1, 1.4)
# thrust-washer recess: an ANNULAR seat outboard of the bolt circle (B3.3)
rp -= Pos(0, 0, Z_RPLATE_TOP - 0.5) * (Cylinder(WASH_SEAT_RO, 1.01)
                                       - Cylinder(WASH_SEAT_RI, 3.0))
# fines slots: TWO arc pairs (shed twice per revolution)
# r5 (buildability MODERATE): the r4 inner slots (r40.5..44.5) and rim slots
# (r45.4..46.8) overlapped in angle, leaving a 1.0 mm annular web as the only
# radial section carrying the cartridge into the latch lugs. Inner slots
# pulled in to r43.6 -> measured web 2.1 mm (harness now measures it).
for (s0, s1) in ((FILL_ARC[0] + 10, FILL_ARC[1] - 20), (255, 345)):
    rp -= sector(19.5, 23.5, s0, s1, Z_RPLATE_BOT - 1, PLATE_T + 2)
    rp -= sector(40.5, 43.6, s0, s1, Z_RPLATE_BOT - 1, PLATE_T + 2)
# fines slots UNDER the rim dust trough (disc OD r46 .. chamber r47).
# r4 (pellet-path MINOR): coverage extended 190 -> 307 deg (85%) in 3 arcs
# INCLUDING the exit sector (r3: rim dust sheared most of a revolution
# before shedding). Bridges kept at the Hall cavities (83..120), plus two
# 8 deg structural bridges. Inner radius 45.4: 0.4 mm clear of the chute
# outer wall (which reaches r45 at theta=0); fines at r45.4+ fall clear of
# the motor (half-width 17.6) and chute below.
for (s0, s1) in ((352.0, 443.0), (120.0, 250.0), (258.0, 344.0)):
    rp -= sector(45.7, 46.8, s0, s1, Z_RPLATE_BOT - 1, PLATE_T + 2)
# hall sensor cavities: theta=90 (station) + 112.5 (index)
for ha in (HALL_STATION_A, HALL_INDEX_A):
    rp -= Pos(MAG_R_POS * math.cos(math.radians(ha)), MAG_R_POS * math.sin(math.radians(ha)),
              Z_RPLATE_BOT + 1.25) * Box(5, 5, 2.5)
# quarter-turn latch lugs (3x), sized to the receiver slots (r52..55.3)
for a in LUG_ANGLES:
    rp += Rot(Z=a) * (Pos(53.55, 0, Z_RPLATE_TOP - PLATE_T / 2) * Box(3.5, 10, PLATE_T))
# integral chute, straight + vertical
chute_or = CHUTE_ID / 2 + CHUTE_WALL
rp += Pos(PCD_R, 0, Z_RPLATE_BOT - CHUTE_LEN / 2) * Cylinder(chute_or, CHUTE_LEN)
# --- rev1 B4: COUNT-SENSOR BOSSES, rebuilt to ELECTRONICS.md 4.2-4.5 -----
# r6: ONE centred Dia3.2 tunnel per side in a Box(12,12,14) boss. 4.2 works
# the consequence: a Dia12 pellet falling 5 mm off the bore axis is occluded
# for 7.5 ms against a 10-35 ms "one pellet" gate, i.e. a real pellet is
# thrown away as a fragment and the verified count is wrong. That is a
# geometry defect, not a threshold. rev1 builds what the doc actually
# specifies: TWO chord beams per side at x = 32 -/+ 3 (ECO-3) with a 6.0 mm
# VERTICAL STAGGER (ECO-9, which makes the per-event velocity measurable),
# a bore-face PMMA window seat (ECO-4) and a lateral labyrinth (ECO-5).
SENS_BOSS_XC = (SENS_BOSS_X0 + SENS_BOSS_X1) / 2
SENS_BOSS_YC = (SENS_BOSS_Y0 + SENS_BOSS_Y1) / 2
SENS_CAV_YC = (SENS_CAV_Y0 + SENS_BOSS_Y1) / 2
BEAMS = [(PCD_R - SENS_BEAM_DX, Z_SENSOR + SENS_BEAM_DZ),
         (PCD_R + SENS_BEAM_DX, Z_SENSOR - SENS_BEAM_DZ)]
for sy in (1, -1):
    rp += Pos(SENS_BOSS_XC, sy * SENS_BOSS_YC, Z_SENSOR) * Box(
        SENS_BOSS_X1 - SENS_BOSS_X0, SENS_BOSS_Y1 - SENS_BOSS_Y0, SENS_BOSS_H)
    # r2 (count-sensor critic BLOCKING 5 / N3 / ECO-12): the boss had no
    # board-retention feature anywhere and the BOM ordered 2x M3 grubs for a
    # hole that did not exist. The cavity walls (2.3 mm in x, 2.3 mm in z)
    # cannot take an M2 pilot, so the boss grows two LOCAL EARS in z that can.
    for sz in (1, -1):
        rp += Pos(SENS_EAR_XC, sy * SENS_BOSS_YC,
                  Z_SENSOR + sz * (SENS_BOSS_H / 2 + SENS_EAR_H / 2)) * Box(
            SENS_EAR_X, SENS_BOSS_Y1 - SENS_BOSS_Y0, SENS_EAR_H)
rp -= Pos(PCD_R, 0, Z_RPLATE_BOT - CHUTE_LEN / 2 - 1) * Cylinder(CHUTE_ID / 2, CHUTE_LEN + 4)

# --- rev1 B5: CARTRIDGE HARNESS DUCT (motor + BOTH count-sensor boards) ---
# Closed printed duct network under the retaining plate. It is built BEFORE
# the sensor cavities are cut, because r1 built it after and it re-filled the
# mouth of the -Y component cavity (count-sensor critic BLOCKING 1: 93.245
# mm3 of intrusion, insertion sweep 203.418 mm3 -> one of the two boards
# could not be installed). Cut order is now: bosses -> chute bore -> DUCT ->
# cavities/tunnels/window seats/cable ports, so a cavity can never be
# re-filled by a later union.
# Three further r1 defects fixed here:
#  - r1 had ONE duct, on -Y only: the +Y board's cable had no modelled route
#    at all (critic: "cable path length unrouted ~74 mm"). The network is now
#    symmetric and both boards feed one exit.
#  - r1's duct crossed the plate's rim fines slot tangentially at theta=270,
#    which is exactly where retaining_plate_chute_r7.stl had its 3
#    non-manifold 4-face edges (B10). The collector now runs 1.75 mm BELOW
#    the deepest slot cut (slot floor -346.25, duct crown -347.00), so no
#    slot cut can graze the duct at all, and the duct is tied to the plate by
#    6 discrete WEBS placed at radii inside the clear annuli.
#  - the route is X-first then Y: running -Y at x=32 first would put the
#    elbow at (32,-48), r=57.7, straight through the quarter-turn latch ring
#    (r52.3) and the cartridge would not come out.
DUCT_RO, DUCT_RI = 4.0, 2.5
# r3 (assembly A-6): the r8 vertical leg at x=48 and its grommet socket at
# x 37..45, |y| 27.5..32.5 stood OUTBOARD of the sensor cover and inside its
# only insertion corridor (swept obstruction 488.4789 mm3). The whole sensor
# branch now leaves the boss through the LOWER EAR'S BOTTOM FACE and runs
# BELOW the cover, then inboard to a vertical leg at x = DUCT_LEG_X, which is
# clear of both the cover envelope (x 22..47) and the board's own insertion
# corridor (x 25.5..43.5).
DUCT_LEG_X = 14.0
DUCT_LEG_Y = 32.5                  # clear of the cover face (|y| = 29.5)
DUCT_Z = Z_RPLATE_BOT - 8.0        # -363.25 axis -> crown -359.25, which is
                                   # 1.00 mm BELOW the latch ring's bottom
                                   # face and below the deepest fines slot
DUCT_LOW_Z = Z_SENSOR - 19.05      # -414.30: the run under the sensor
                                   # covers. Dia8 OD -> crown -410.30 (0.55 mm
                                   # under the cover bottom -409.75) and floor
                                   # -418.30 (0.15 mm above the motor can)
DUCT_XW = -32.5                    # +Y branch return leg
DUCT_END_Y = -48.0
# r6 (integration BLOCKING I-1): r11 accumulated the bores into ONE fused
# solid `_bore` and did `rp -= _bore`. Every leg of that fuse is an
# equal-radius (DUCT_RI = 2.5) cylinder meeting another equal-radius cylinder
# at 90 deg, which is a degenerate-tangency fuse: BRepCheck_Analyzer reports
# the fused shape INVALID, and OCC then answers `rp - _bore` with rp itself
# and `rp.intersect(_bore)` with 0.0 mm3 -- no exception, no warning. The
# printed part shipped with 100 % solid material on every duct axis while the
# model's own coverage metric read 100 % (a solid rod is perfectly "covered").
# The bores are now kept as a LIST of primitives and cut one at a time by
# cut_each(), which refuses an invalid tool and asserts a volume floor.
_duct, _bores = None, []


def _du(s, b):
    global _duct
    _duct = s if _duct is None else _duct + s
    _bores.append(b)


SENS_EAR_Z0 = Z_SENSOR - SENS_SCREW_DZ - SENS_EAR_H / 2      # ear bottom face
for sy in (1, -1):
    # (a) stub DOWN out of the lower ear's bottom face, on the port axis
    _du(Pos(SENS_PORT_X, sy * SENS_PORT_Y, (DUCT_LOW_Z + SENS_EAR_Z0) / 2)
        * Cylinder(DUCT_RO, SENS_EAR_Z0 - DUCT_LOW_Z),
        Pos(SENS_PORT_X, sy * SENS_PORT_Y,
            (DUCT_LOW_Z + SENS_EAR_Z0 + 2.0) / 2)
        * Cylinder(DUCT_RI, SENS_EAR_Z0 + 2.0 - DUCT_LOW_Z))
    # (b) low run in Y, underneath the cover, out to the collector plane
    _du(Pos(SENS_PORT_X, sy * (SENS_PORT_Y + DUCT_LEG_Y) / 2, DUCT_LOW_Z)
        * Rot(X=90) * Cylinder(DUCT_RO, DUCT_LEG_Y - SENS_PORT_Y),
        Pos(SENS_PORT_X, sy * (SENS_PORT_Y + DUCT_LEG_Y) / 2, DUCT_LOW_Z)
        * Rot(X=90) * Cylinder(DUCT_RI, DUCT_LEG_Y - SENS_PORT_Y + 2))
    # (c) low run in X, inboard to the vertical leg
    _du(Pos((DUCT_LEG_X + SENS_PORT_X) / 2, sy * DUCT_LEG_Y, DUCT_LOW_Z)
        * Rot(Y=90) * Cylinder(DUCT_RO, SENS_PORT_X - DUCT_LEG_X),
        Pos((DUCT_LEG_X + SENS_PORT_X) / 2, sy * DUCT_LEG_Y, DUCT_LOW_Z)
        * Rot(Y=90) * Cylinder(DUCT_RI, SENS_PORT_X - DUCT_LEG_X + 2))
    # (d) vertical leg up to the collector
    _du(Pos(DUCT_LEG_X, sy * DUCT_LEG_Y, (DUCT_LOW_Z + DUCT_Z) / 2)
        * Cylinder(DUCT_RO, DUCT_Z - DUCT_LOW_Z),
        Pos(DUCT_LEG_X, sy * DUCT_LEG_Y, (DUCT_LOW_Z + DUCT_Z + 2.0) / 2)
        * Cylinder(DUCT_RI, DUCT_Z - DUCT_LOW_Z + 2.0))
    # (e) collector run in X at |y| = DUCT_LEG_Y
    _du(Pos((DUCT_XW + DUCT_LEG_X) / 2, sy * DUCT_LEG_Y, DUCT_Z) * Rot(Y=90)
        * Cylinder(DUCT_RO, DUCT_LEG_X - DUCT_XW),
        Pos((DUCT_XW + DUCT_LEG_X) / 2, sy * DUCT_LEG_Y, DUCT_Z) * Rot(Y=90)
        * Cylinder(DUCT_RI, DUCT_LEG_X - DUCT_XW + 2))
# (f) rev1 r3 -- B5-c, "the bay->motor cable has no modelled route" (0 % of
# that leg was covered in r8, >=63 mm of it in free air). A branch drops from
# the collector at x=0 to the motor's rear plane and turns inboard to a
# grommet socket facing the can, 4.4 mm off the motor's -Y face.
MOT_BR_Y = -DUCT_LEG_Y
MOT_SOCK_Y = -(MOTOR_W / 2 + 4.4)
MOT_BR_Z = Z_MOTOR_BOT + 6.0
_du(Pos(0.0, MOT_BR_Y, (MOT_BR_Z + DUCT_Z) / 2) * Cylinder(
    DUCT_RO, DUCT_Z - MOT_BR_Z),
    Pos(0.0, MOT_BR_Y, (MOT_BR_Z + DUCT_Z + 2.0) / 2) * Cylinder(
    DUCT_RI, DUCT_Z - MOT_BR_Z + 2.0))
_du(Pos(0.0, (MOT_BR_Y + MOT_SOCK_Y) / 2, MOT_BR_Z) * Rot(X=90) * Cylinder(
    DUCT_RO, MOT_SOCK_Y - MOT_BR_Y),
    Pos(0.0, (MOT_BR_Y + MOT_SOCK_Y) / 2, MOT_BR_Z) * Rot(X=90) * Cylinder(
    DUCT_RI + 0.25, MOT_SOCK_Y - MOT_BR_Y + 2.0))
MOTOR_LEAD_SOCKET = (0.0, MOT_SOCK_Y, MOT_BR_Z)
# +Y branch return leg (x = DUCT_XW) and the single exit leg (x = 0)
_du(Pos(DUCT_XW, 0.0, DUCT_Z) * Rot(X=90) * Cylinder(DUCT_RO, 2 * DUCT_LEG_Y),
    Pos(DUCT_XW, 0.0, DUCT_Z) * Rot(X=90) * Cylinder(DUCT_RI, 2 * DUCT_LEG_Y + 2))
_du(Pos(0.0, (-DUCT_LEG_Y + DUCT_END_Y) / 2, DUCT_Z) * Rot(X=90)
    * Cylinder(DUCT_RO, -DUCT_END_Y - DUCT_LEG_Y),
    Pos(0.0, (-DUCT_LEG_Y + DUCT_END_Y) / 2, DUCT_Z) * Rot(X=90)
    * Cylinder(DUCT_RI, -DUCT_END_Y - DUCT_LEG_Y + 4))
rp += _duct
# webs tying the duct crown to the plate underside, at radii inside the
# CLEAR annuli of the fines-slot pattern (r 23.5..40.5 and r > 46.8)
DUCT_WEBS = [(10.0, DUCT_LEG_Y), (-15.0, DUCT_LEG_Y), (10.0, -DUCT_LEG_Y),
             (-15.0, -DUCT_LEG_Y), (0.0, -38.0), (DUCT_XW, 0.0)]
for (wx, wy) in DUCT_WEBS:
    rp += Pos(wx, wy, (DUCT_Z + 1.0 + Z_RPLATE_BOT + 1.25) / 2) * Box(
        3.0, 3.0, (Z_RPLATE_BOT + 1.25) - (DUCT_Z + 1.0))
# I-1: the cut that r11 believed it had made. The closed-form lower bound is
# the volume of the SHORTEST leg alone (the motor stub, Dia5.5 x 10.5 =
# 249 mm3); the floor below is set at 7000 mm3, i.e. ~88 % of the closed-form
# network volume, so a single silently-dropped leg fails the build.
_rp_v0 = vol_of(rp)
rp = cut_each(rp, _bores, "cartridge harness duct bores (B5 / I-1)",
              floor=7000.0)
DUCT_BORE_CUT = _rp_v0 - vol_of(rp)
DUCT_EXIT = (0.0, DUCT_END_Y - DUCT_RO, DUCT_Z)
# I-1 needs a PATENCY test, not a coverage test (a solid rod is 100 %
# "covered"). The axis of every leg is registered here, in world coords, and
# the checks below classify points on it and sweep a Dia4.0 bundle down it.
DUCT_LEGS = []
for sy in (1, -1):
    _t = "+Y" if sy > 0 else "-Y"
    DUCT_LEGS += [
        (f"sensor cavity riser {_t}",
         (SENS_PORT_X, sy * SENS_PORT_Y, Z_SENSOR - SENS_CAV[2] / 2 + 0.5),
         (SENS_PORT_X, sy * SENS_PORT_Y, DUCT_LOW_Z)),
        (f"low run in Y {_t}",
         (SENS_PORT_X, sy * SENS_PORT_Y, DUCT_LOW_Z),
         (SENS_PORT_X, sy * DUCT_LEG_Y, DUCT_LOW_Z)),
        (f"low run in X {_t}",
         (SENS_PORT_X, sy * DUCT_LEG_Y, DUCT_LOW_Z),
         (DUCT_LEG_X, sy * DUCT_LEG_Y, DUCT_LOW_Z)),
        (f"vertical leg {_t}",
         (DUCT_LEG_X, sy * DUCT_LEG_Y, DUCT_LOW_Z),
         (DUCT_LEG_X, sy * DUCT_LEG_Y, DUCT_Z)),
        (f"collector run {_t}",
         (DUCT_LEG_X, sy * DUCT_LEG_Y, DUCT_Z),
         (DUCT_XW, sy * DUCT_LEG_Y, DUCT_Z)),
    ]
DUCT_LEGS += [
    ("return leg (+Y -> -Y)", (DUCT_XW, DUCT_LEG_Y, DUCT_Z),
     (DUCT_XW, -DUCT_LEG_Y, DUCT_Z)),
    ("motor branch", (0.0, MOT_BR_Y, DUCT_Z), (0.0, MOT_BR_Y, MOT_BR_Z)),
    ("motor stub", (0.0, MOT_BR_Y, MOT_BR_Z), (0.0, MOT_SOCK_Y, MOT_BR_Z)),
    ("exit leg (-> bay)", (0.0, -DUCT_LEG_Y, DUCT_Z),
     (0.0, DUCT_END_Y, DUCT_Z)),
]

# --- sensor cavities, tunnels, ECO-4 window seats, cable ports ---------
for sy in (1, -1):
    # component cavity: clears an 18 x 12 x 2 board + 1 mm all round; it now
    # ends flush with the boss face (|y| = 25) because a bolted COVER closes
    # it (r1 left it open to free air and unretained).
    rp -= Pos(SENS_BOSS_XC, sy * (SENS_CAV_Y0 + SENS_BOSS_Y1) / 2, Z_SENSOR) * Box(
        SENS_CAV[0], SENS_BOSS_Y1 - SENS_CAV_Y0, SENS_CAV[2])
    for (bx, bz) in BEAMS:
        # ECO-4 window seat. r1 cut this as a blind Dia6 x 1.0 pocket whose
        # mouth was a FLAT plane at |y| = 11.0 while the Dia22 bore wall at
        # the aperture chord is at |y| = 10.583 -- leaving a printed wedge up
        # to 0.610 mm thick standing across half of every aperture (critic
        # BLOCKING 2), which cost beam B 83 % of its clear area (BLOCKING 3)
        # and blocked the window insertion path (assembly A-4, 5.2219 mm3).
        # The seat is now cut from the BORE AXIS outward, so its mouth IS the
        # bore surface and no lip can exist by construction. A flat Dia6
        # window cannot be geometrically flush with a Dia22 cylinder (the
        # sagitta across the footprint is measured and printed); the window
        # face is placed at |y| = 11.000 = the bore's own maximum radius, so
        # nothing is ever proud of the bore.
        rp -= Pos(bx, sy * (SENS_BOSS_Y0 + SENS_WIN_T) / 2, bz) * Rot(X=90) * \
            Cylinder(SENS_WIN_R, SENS_BOSS_Y0 + SENS_WIN_T)
        # r6, ECO-4's "0.4 mm chamfered recess" (count-sensor r5 ask 4):
        # ATTEMPTED AND WITHDRAWN, with the measurement that withdrew it.
        # A Cone(3.0 -> 3.4) over |y| 10.6..11.0 was cut on this axis and the
        # part came back NOT WATERTIGHT: retaining_plate_chute_r12 exported
        # with 22 open + 22 non-manifold edges, all of them at x = 31.99..
        # 32.01, |y| = 11.000, z = -391.96..-398.47 -- i.e. exactly where the
        # cone's narrow rim (r = 3.000 at |y| = 11.000) is coincident with the
        # seat cylinder AND the seat-mouth plane |y| = 11.000 is tangent to
        # the Dia22 chute bore at x = 32.000. That is a degenerate tangency,
        # not a mesh-tolerance artefact, and B10 is a blocking punch-list
        # item. The seat is therefore shipped straight-walled again and the
        # deviation from ECO-4 is RECORDED, not narrated away.
        # r6 (count-sensor r5 ask 1, B4.2): the ECO-5 labyrinth stepped the
        # outer 2.5 mm +0.800 mm in x on BOTH sides, so the straight-through
        # aperture was the LENS of two Dia3.2 circles offset 0.800 -- 2.4 x
        # 3.2 mm, centred on x = 29.400/35.400, not on ECO-3's 29/35. B4.2's
        # Dia2.0 x 60 beam cylinder read 1.1932 mm3 on the nominal axis and
        # ECO-9's published x0 solve (chords at +/-3.0) was false for the
        # as-built chords (-2.600/+3.400). The step is now SPLIT: inner
        # segment -SENS_LAB_OFF/2, outer +SENS_LAB_OFF/2. The ledge is the
        # same 0.800 mm ECO-5 asks for, but the lens re-centres on 29.000 /
        # 35.000 and the chords are symmetric about the bore axis again.
        _t0 = SENS_BOSS_Y0 + SENS_WIN_T
        _t1 = SENS_CAV_Y0 - SENS_LAB_LEN
        rp -= Pos(bx - SENS_LAB_OFF / 2, sy * (_t0 + _t1) / 2, bz) * \
            Rot(X=90) * Cylinder(SENS_APER_R, _t1 - _t0)
        rp -= Pos(bx + SENS_LAB_OFF / 2, sy * (_t1 + SENS_CAV_Y0) / 2, bz) * \
            Rot(X=90) * Cylinder(SENS_APER_R, SENS_CAV_Y0 - _t1 + 0.01)
    # r3 (assembly A-6): cable port is now a single VERTICAL riser from the
    # cavity floor, behind the board plane, straight out of the lower ear's
    # bottom face into the duct stub -- nothing of the harness is outboard of
    # the cover any more, and the cover itself has no hole in it.
    rp -= Pos(SENS_PORT_X, sy * SENS_PORT_Y,
              (Z_SENSOR - SENS_CAV[2] / 2 + SENS_EAR_Z0 - 1.0) / 2) * Cylinder(
        SENS_PORT_R, Z_SENSOR - SENS_CAV[2] / 2 - SENS_EAR_Z0 + 1.0)
    # 2 x M2 self-tap pilots in the ears, for the sensor cover
    for sz in (1, -1):
        rp -= Pos(SENS_BOSS_XC, sy * (SENS_BOSS_Y1 - 2.5),
                  Z_SENSOR + sz * SENS_SCREW_DZ) * Rot(X=90) * Cylinder(
            0.8, 5.0)
# --- r4 (granule-path MODERATE 3): PLUG TETHER ANCHOR -----------------
# "with the plug fitted, granule 1 and 2 stack in the chute and granule 3
# cannot clear the Dia16 exit port ... nothing in the geometry prevents this.
# One printed tab or a BOM tether line closes it." The plug now carries a
# Dia4 eye and the chute carries this anchor lug, so the plug is captive and
# hangs below the chute mouth in plain sight when it is out.
# r5 (granule-path MAJOR): TETH_X0 was 42.0, i.e. 1.000 mm INSIDE the r11.0
# chute bore -- measured on retaining_plate_chute_r10.stl as r_min 10.000 over
# z -398.00..-404.00, a 6.000 x 8.000 mm ledge in the fall path that also
# fouled the plug shank by 0.600 mm radially (16.973 mm3 of the 206.099 mm3
# the r10 log called "the designed 0.3 mm press fit"). The lug's inboard face
# is now ON the bore wall, so the drop tube is Dia22.000 continuous.
TETH_X0, TETH_X1 = PCD_R + CHUTE_ID / 2, 51.0   # 43.0 = the bore wall
TETH_W, TETH_H = 8.0, 6.0
# the chute tube ENDS at Z_CHUTE_BOT: a lug below that plane is a floating
# body (which is exactly what the first r10 attempt exported -- a
# disconnected 283.5 mm3 solid). It sits on the tube, 4.25 mm above the mouth.
TETH_ZC = Z_CHUTE_BOT + 4.25
TETH_EYE_D = 4.0
rp += Pos((TETH_X0 + TETH_X1) / 2, 0.0, TETH_ZC) * Box(
    TETH_X1 - TETH_X0, TETH_W, TETH_H)
rp -= Pos(TETH_X1 - 3.0, 0.0, TETH_ZC) * Rot(X=90) * Cylinder(
    TETH_EYE_D / 2, TETH_W + 2.0)
add("retaining_plate_chute", rp, "#8f8778", density=DENS["petg_cf"],
    basis="[D] volume; integral vertical chute + ECO-3/4/5/9 count-sensor "
          "bosses + latch lugs + cartridge harness duct (B5) + plug tether "
          "anchor (r4)")

# --- 11. geared stepper (14HS13-0804S-PG5 envelope, r6) ----------------
# gearbox body first (round Dia36 worst case), then the NEMA 14 motor.
motor = Pos(0, 0, (Z_MOTOR_TOP + Z_GEAR_BOT) / 2) * Cylinder(GEAR_OD / 2, GEAR_L)
motor += Pos(0, 0, Z_GEAR_BOT - MOTOR_L / 2) * Box(MOTOR_W, MOTOR_W, MOTOR_L)
for sx in (1, -1):
    for sy in (1, -1):
        motor -= Pos(sx * MOTOR_W / 2, sy * MOTOR_W / 2, Z_GEAR_BOT - MOTOR_L / 2) * Rot(
            Z=45 if sx * sy > 0 else -45) * Box(9, 9, MOTOR_L + 2)
motor += Pos(0, 0, Z_MOTOR_TOP + 1.0) * Cylinder(MOTOR_PILOT_R, 2.0)
motor += Pos(0, 0, Z_MOTOR_TOP + MOTOR_SHAFT_LEN / 2) * Cylinder(MOTOR_SHAFT_R, MOTOR_SHAFT_LEN)
# D-cut on the output shaft (12 mm long, vendor): 0.5 mm flat depth.
# rev1: the r6 cutter was centred at x=+6.0 with width 6, i.e. it spanned
# x 3.0..9.0 and removed NOTHING from a Dia6 shaft -- the modelled shaft was
# plain round, which is exactly why the disc bore could be round too and no
# check caught it. The flat is now real and CLOCKED to GRUB_A so it faces the
# disc's D-bore flat and the grub screw.
motor -= Rot(Z=GRUB_A) * (
    Pos(MOTOR_SHAFT_R - MOTOR_SHAFT_FLAT + 3.0, 0,
        Z_MOTOR_TOP + MOTOR_SHAFT_LEN - MOTOR_SHAFT_DCUT / 2)
    * Box(6.0, 8.0, MOTOR_SHAFT_DCUT))
add("stepper", motor, "#3a3a3a", mass=MOTOR_MASS,
    basis="StepperOnline 14HS13-0804S-PG5 (NEMA 14 + 5.18:1 planetary, "
          "0.14 N*m x 5.18 x 0.90 = 0.65 N*m out, 35x35x34 + 29.2 gearbox, "
          "Dia6x18 D-cut shaft); 310 g NET ASSUMPTION (vendor 0.38 kg gross)")

# --- 12. electronics bay (rev1 B5: a REAL electronics home) ------------
# Thomas, directive 2: "We do need a place for the wiring and electronics on
# the dispenser side of it though, right now it looks like the wiring would go
# straight into the tank." r6 had a box with a lid and nothing in it: no board
# mounting (ECO-7), one cable entry instead of three (ECO-6), and a "gasket"
# that was a note rather than geometry. rev1 adds all three, plus the modelled
# conduit runs that get the harness here without crossing the pellet space.
ZC_BAY = RIB_ZC   # bay centred on its own rib mounts
BAY_Y_IN = BAY_YC + BAY_D / 2            # -62, inboard face
BAY_Y_OUT = BAY_YC - BAY_D / 2           # -88, outboard (lid) face
BAY_LAND_T = 2.0                         # extra thickness at the lid joint
BAY_FLANGE_Y = BAY_Y_OUT - BAY_LAND_T    # -90, sealing face
BAY_TOP_Z = ZC_BAY + BAY_H / 2
BAY_RISER_RO, BAY_RISER_RI = 5.2, 3.7   # r2: top-face riser SOCKET; the
                           # hopper conduit (ID 11.0) plugs down over it
bay_s = Pos(0, BAY_YC, ZC_BAY) * Box(BAY_W, BAY_D, BAY_H)
bay_s += Pos(0, BAY_FLANGE_Y + BAY_LAND_T / 2, ZC_BAY) * Box(
    BAY_FL_W, BAY_LAND_T, BAY_FL_H)
bay_s -= Pos(0, BAY_YC, ZC_BAY) * Box(BAY_W - 4, BAY_D - 4, BAY_H - 4)
# lid opening through the land + outboard wall.
# r3 (B5-a): BAY_W - 8 gave a 42.0000 mm clear aperture for a 42.0 mm board
# (0.0000 mm of clearance, measured by the integration critic on the r8
# export). The bay is 6 mm wider and the aperture is now BAY_W - 10 = 46.0.
BAY_APER_W = BAY_W - 10.0
bay_s -= Pos(0, BAY_FLANGE_Y + 3.0, ZC_BAY) * Box(BAY_APER_W, 8.0, BAY_H - 6.0)
# --- B5.3 GASKET GROOVE: real geometry, closed loop, 1.6 x 1.2 ---------
GASK_W, GASK_D = 1.6, 1.2
GASK_X, GASK_Z = 26.0, 19.5              # groove centreline half-extents
_g_out = Pos(0, BAY_FLANGE_Y + GASK_D / 2, ZC_BAY) * Box(
    2 * GASK_X + GASK_W, GASK_D, 2 * GASK_Z + GASK_W)
_g_in = Pos(0, BAY_FLANGE_Y + GASK_D / 2, ZC_BAY) * Box(
    2 * GASK_X - GASK_W, GASK_D + 1.0, 2 * GASK_Z - GASK_W)
BAY_GASKET_PERIM = 4 * (GASK_X + GASK_Z)     # closed-loop centreline length
bay_s -= (_g_out - _g_in)
# 4 lid screws OUTSIDE the gasket, in bosses behind the flange
BAY_SCREW_X, BAY_SCREW_Z = 29.0, 22.0
for sx in (1, -1):
    for sz in (1, -1):
        bay_s += Pos(sx * BAY_SCREW_X, BAY_FLANGE_Y + 5.0,
                     ZC_BAY + sz * BAY_SCREW_Z) * Box(8.0, 8.0, 8.0)
        bay_s -= Pos(sx * BAY_SCREW_X, BAY_FLANGE_Y + 3.5,
                     ZC_BAY + sz * BAY_SCREW_Z) * Rot(X=90) * Cylinder(1.25, 7.5)
# ribs (unchanged): conformal end face, M3 into housing wall pilots
for sx in (1, -1):
    bay_s += Pos(sx * 14.0, -55.0, RIB_ZC) * Box(7.6, 14.0, 11.5)
bay_s -= Pos(0, 0, RIB_ZC) * Cylinder(HOUSING_R + 0.1, 12.5)
for sx in (1, -1):
    bay_s -= Pos(sx * 14.0, -56.0, RIB_ZC) * Rot(X=90) * Cylinder(1.6, 16.5)
# --- ECO-7: four M2.5 board standoffs on the inboard wall --------------
STANDOFF_H, STANDOFF_R = 5.0, 2.6
BOARD_X, BOARD_Z = 42.0, 34.0            # main board (ELECTRONICS 7)
BOARD_ENV_Y = 12.0                       # board + tallest component
STANDOFF_XS = (18.0, -18.0)
STANDOFF_ZS = (14.0, -14.0)
BOARD_Y0 = BAY_Y_IN - 2.0 - STANDOFF_H   # board underside plane
for sx in STANDOFF_XS:
    for sz in STANDOFF_ZS:
        # r2: the standoff end face used to be COPLANAR with the inner wall
        # face (y = BAY_Y_IN - 2.0). That tangent union is what put 4
        # inverted-normal bodies (-15.9 mm3 each) into dispenser_r7_assembly
        # .stl (granule-path MAJOR / assembly export-integrity). The boss now
        # buries 0.4 mm into the wall.
        bay_s += Pos(sx, BAY_Y_IN - 1.8 - STANDOFF_H / 2, ZC_BAY + sz) * Rot(
            X=90) * Cylinder(STANDOFF_R, STANDOFF_H + 0.4)
        # r2: this pilot used to be a SEALED internal void (0.3 mm of skin
        # over its outer end), which is what produced the 4 inverted-normal
        # bodies of -15.926 mm3 each in the assembly STL. It now opens at the
        # standoff's free face, where the M2.5 screw actually enters.
        bay_s -= Pos(sx, BAY_Y_IN - 1.8 - STANDOFF_H / 2 - 0.5,
                     ZC_BAY + sz) * Rot(X=90) * Cylinder(
            1.05, STANDOFF_H + 0.4)
# --- ECO-6: THREE grommeted cable entries -----------------------------
# (1) aircraft harness, from the hopper conduit, into the bay TOP face
BAY_ENTRIES = []
# r2: the r1 entry was a Dia11 x 3.2 counterbore + a Dia7 through-hole in a
# flat face, with the hopper conduit ending 3 mm above it in mid-air. The
# entry is now the RISER SOCKET itself (built below): its bore is the cable
# hole and its wall is the grommet land, and the hopper conduit plugs down
# over the outside of it, so the route is continuous and covered.
BAY_ENTRIES.append(("aircraft harness (top riser socket)",
                    (0.0, CONDUIT_Y, BAY_TOP_Z), 2 * BAY_RISER_RI,
                    BAY_RISER_RO - BAY_RISER_RI))
# (2)+(3) motor and count-sensor cables, inboard (+Y) face
for sx, lbl in ((10.0, "motor cable (+Y face)"), (-10.0, "count-sensor cable (+Y face)")):
    bay_s -= Pos(sx, BAY_Y_IN - 1.0, ZC_BAY - 13.0) * Rot(X=90) * Cylinder(5.0, 3.2)
    bay_s -= Pos(sx, BAY_Y_IN - 3.0, ZC_BAY - 13.0) * Rot(X=90) * Cylinder(3.0, 8.0)
    BAY_ENTRIES.append((lbl, (sx, BAY_Y_IN, ZC_BAY - 13.0), 6.0, 2.0))
# r2: riser SOCKET on the bay top face that receives the hopper conduit foot,
# so the aircraft harness is covered from the neck all the way into the bay
# (the r1 geometry left the conduit foot floating 3 mm above a flat face and
# fouling the lid flange -- see HOP_COND_Z0).
BAY_RISER_Z1 = HOP_COND_Z0 + 4.0           # conduit bore -> 4.0 mm engagement
# the riser must bury itself in the bay's top wall: a cylinder whose end
# face is COPLANAR with that wall is a tangent union and came out as a
# second, disconnected solid.
# r3 (integration): at -3.0 the riser dipped 1.0 mm into the cavity and cost
# the board 0.5 mm of the 1.5 mm wall clearance B5.1 asks for. It now buries
# only 0.2 mm past the inner face of the 2 mm top wall (still a transversal
# intersection, not a tangent union).
BAY_RISER_Z0 = BAY_TOP_Z - 2.2
bay_s += Pos(0, CONDUIT_Y, (BAY_RISER_Z0 + BAY_RISER_Z1) / 2) * Cylinder(
    BAY_RISER_RO, BAY_RISER_Z1 - BAY_RISER_Z0)
bay_s -= Pos(0, CONDUIT_Y, (BAY_RISER_Z0 - 6.0 + BAY_RISER_Z1 + 1) / 2) * Cylinder(
    BAY_RISER_RI, BAY_RISER_Z1 + 1 - (BAY_RISER_Z0 - 6.0))
add("electronics_bay", bay_s, "#c9c2b4", density=DENS["petg_cf"],
    basis="[D] 2 mm shell + screwed conformal ribs + gasketed lid flange + "
          "4x M2.5 board standoffs (ECO-7) + 3 grommeted entries (ECO-6)")

# --- 12b. bay lid (printed): flange + register lip + screws + access ----
# r4 (B10 mesh hygiene): the r9 lid plate was exactly as big as the bay
# flange, so its 4 perimeter edges at the sealing plane y = -90 were
# coincident with the bay's and the assembly mesh carried 4-face edges there.
# The lid is inset 0.4 mm/side; the gasket groove is at |x| <= 26.8, so the
# seal is unaffected.
lid = Pos(0, BAY_FLANGE_Y - 1.0, ZC_BAY) * Box(BAY_FL_W - 0.8, 2.0,
                                               BAY_FL_H - 0.8)
lid += Pos(0, BAY_FLANGE_Y + 0.7, ZC_BAY) * Box(
    BAY_APER_W - 0.6, 1.4, BAY_H - 6.6)  # register lip, 0.3 gap
for sx in (1, -1):
    for sz in (1, -1):
        lid -= Pos(sx * BAY_SCREW_X, BAY_FLANGE_Y - 1.0,
                   ZC_BAY + sz * BAY_SCREW_Z) * Rot(X=90) * Cylinder(1.7, 4.0)
for sx in (1, -1):
    # Dia6 rib-screw driver access holes (grommet-plugged in service).
    # r3 (assembly NB-2): the r8 cut was 4.0 long and centred on the flange,
    # so it stopped at y = -89.0 and left a 0.400 mm membrane of the lid's
    # own register lip across the hole (0.7069 mm3 in a Dia1.5 corridor).
    lid -= Pos(sx * 14.0, BAY_FLANGE_Y, RIB_ZC) * Rot(X=90) * Cylinder(3.0, 10.0)
add("bay_lid", lid, "#b9b1a1", density=DENS["petg_cf"],
    basis="[D] volume; 4x M3 self-tap OUTSIDE the gasket line, register lip, "
          "Dia6 rib-driver access")

# --- 13. blind-mate PCB, positioned FROM the vendor plate (r6) ---------
# The payload-side Attachment Interface PCB (ICD 5: same layout as the drone
# side, pads U11-U20 instead of pins) bolts to the clip plate's own 4 tabs
# at (+/-4,+/-10) with M2 screws through the mapped Dia1.9 tab holes, pads up
# through the 16 x 24 shaft. Board outline taken from the vendor 3331 STEP
# (16.0 x 24.0 placed footprint; ICD quotes the 23.5 x 15.8 copper outline).
PCB_X, PCB_Y, PCB_T = 16.0, 24.0, 1.6
pcb = Pos(0, 0, Z_PLATE_BOT - PCB_T / 2) * Box(PCB_X, PCB_Y, PCB_T)
# Molex J1 (12-pin, harness side) + service loop live in the well below
pcb += Pos(0, -6.0, Z_PLATE_BOT - PCB_T - 2.5) * Box(14.0, 8.0, 5.0)
add("blindmate_pcb", pcb, "#1f6f43", mass=15.0,
    basis="ICD 5 board + Molex J1 mock; POSITION IS NOW DERIVED from the "
          "clip-plate map (shaft centre, tabs at +/-4/+/-10), not assumed")

# --- 14. ECO-4 sacrificial PMMA count windows (4 off, COTS/laser-cut) ---
# r2: the window's INNER face is now placed at exactly |y| = SENS_BOSS_Y0 =
# 11.000 = the Dia22 bore's own maximum radius, so nothing is ever proud of
# the bore, and the 0.05 mm that used to sit proud (r1 put the face at
# 11.025) becomes the bond line at the BACK of the seat.
WIN_FACE_Y = SENS_BOSS_Y0
win = None
for sy in (1, -1):
    for (bx, bz) in BEAMS:
        w = Pos(bx, sy * (WIN_FACE_Y + (SENS_WIN_T - 0.05) / 2), bz) * \
            Rot(X=90) * Cylinder(SENS_WIN_R - 0.05, SENS_WIN_T - 0.05)
        win = w if win is None else win + w
add_aux("count_windows", win, "#cfe3ee", density=DENS["pmma"],
        basis="ECO-4: 4x sacrificial Dia6 x 1.0 PMMA disc, bonded in a seat "
              "cut against the bore cylinder (no lip); inner face tangent to "
              "the Dia22 bore; swabbable from the chute exit, replaceable")

# --- 14a2. count-sensor BOARDS with their optoelectronics (2 off, COTS) --
# rev1 r3 (count-sensor critic BLOCKING): "the emitter and the receiver have
# no volume". r3 modelled them from PACKAGE KNOWLEDGE (LED 5.8 mm tall, PD a
# 4.5 x 4.0 x 3.2 DIL case) and the r3 critic then fetched the two Vishay
# drawings and showed both were wrong: TSAL6200 is 8.7 +/- 0.3 mm from the
# seating plane to the dome apex (Dia5.0 barrel, Dia5.8 x 0.7 flange, R2.49
# dome; doc 81010 rev 2.4, drawing 6.544-5259.06-4) and VBPW34FAS is a
# SURFACE-MOUNT gullwing 6.4 x 3.9 x 1.2 (doc 81127 rev 1.3), not a DIL case.
# r4 models the DRAWING solids, and the emitter is modelled at its MAXIMUM
# height (9.0 mm) so the shipped assembly boolean is the worst-material case.
# r6: with the labyrinth step SPLIT (-0.400 inner / +0.400 outer) the clear
# lens is back on the ECO-3 axes, so the devices go back on them too. r11 put
# them at 29.800/35.800 because that was where the r11 outer tunnel was.
SENS_DEV_X = [bx for (bx, bz) in BEAMS]
SENS_DEV_Z = [bz for (bx, bz) in BEAMS]
SENS_BOARD_XC = SENS_BOSS_XC


def led_solid(x, z, sy, h):
    """Vishay TSAL6200 datasheet envelope, seated on the board plane.

    The dome is modelled as the MAX-MATERIAL CYLINDRICAL envelope: a Dia5.0
    barrel run all the way to the apex at h. That solid strictly CONTAINS the
    drawing's R2.49 spherical cap, so every interference number it produces is
    conservative. It is done this way because build123d's Sphere primitive
    tessellates with degenerate pole triangles -- measured: a lone
    Sphere(2.55) exports with 2 open + 2 four-face edges at every tolerance
    from 5e-4 to 0.05 -- and B10 now asserts a clean census on every exported
    STL, so a sphere anywhere in an exported part would fail this round's own
    integrity test. cad/verify_r4.py booleans the TRUE domed solid (exact OCC,
    nothing exported), so the sphere case is measured too.
    """
    y0 = SENS_BOARD_Y0                    # seating plane, |y|
    s = Pos(x, sy * (y0 - LED_FLANGE_T / 2), z) * Rot(X=90) * Cylinder(
        LED_FLANGE_D / 2, LED_FLANGE_T)
    barrel = h - LED_FLANGE_T                         # flange top -> apex
    s += Pos(x, sy * (y0 - LED_FLANGE_T - barrel / 2), z) * Rot(X=90) * \
        Cylinder(LED_BODY_D / 2, barrel)
    return s


def pd_solid(x, z, sy):
    """Vishay VBPW34FAS datasheet envelope (SMD gullwing)."""
    return Pos(x, sy * (SENS_BOARD_Y0 - PD_H / 2), z) * Box(PD_L, PD_H, PD_W)


sb = None
for sy in (1, -1):
    b = Pos(SENS_BOARD_XC, sy * (SENS_BOARD_Y0 + SENS_BOARD_Y1) / 2, Z_SENSOR) \
        * Box(18.0, SENS_BOARD_T, 12.0)
    for (dx, dz) in zip(SENS_DEV_X, SENS_DEV_Z):
        b += led_solid(dx, dz, sy, LED_H_MAX) if sy > 0 else pd_solid(dx, dz, sy)
    sb = b if sb is None else sb + b
add_aux("sensor_boards", sb, "#1f6f43", mass=6.0,
        basis="ELECTRONICS 7: 2x 18x12x2 sensor PCB; +Y 2x TSAL6200 at the "
              "9.0 mm max-material height, -Y 2x VBPW34FAS SMD. Envelopes are "
              "the two Vishay package drawings (81010 rev 2.4 / 81127 rev 1.3)")

# --- 14b. count-sensor covers (2 off, printed) -- ECO-12 / N3 ----------
# Closes the component cavity (dust), clamps the board on four posts and
# carries the grommeted cable port into the harness duct socket. One printed
# part, used on both sides (it is symmetric in x and z).
cov = None
for sy in (1, -1):
    c = Pos(SENS_BOSS_XC, sy * (SENS_BOSS_Y1 + COVER_T / 2), Z_SENSOR) * Box(
        COVER_X, COVER_T, COVER_Z)
    # 0.4 mm register lip into the cavity mouth (0.2 mm clearance all round)
    c += Pos(SENS_BOSS_XC, sy * (SENS_BOSS_Y1 - 0.2), Z_SENSOR) * Box(
        SENS_CAV[0] - 0.4, 0.4, SENS_CAV[2] - 0.4)
    # 4 clamp posts onto the board's outer face (4 x 3x3 = 36 mm2 bearing)
    # r6 (count-sensor r5 ask 4 / NIT): r11's posts landed EXACTLY on the
    # board's outer face -- "min gap board->cover = 0.0000 mm" with no
    # compliant element modelled, so on a printed part the board is either
    # loose or crushed. The posts now stop SENS_PAD_T short and a silicone
    # pad of that thickness is a BOM line, so "clamped" is a real stack-up.
    for px in (-7.5, 7.5):
        for pz in (-5.0, 5.0):
            c += Pos(SENS_BOSS_XC + px,
                     sy * (SENS_BOSS_Y1 + SENS_BOARD_Y1 + SENS_PAD_T) / 2,
                     Z_SENSOR + pz) \
                * Box(3.0, SENS_BOSS_Y1 - SENS_BOARD_Y1 - SENS_PAD_T, 3.0)
    # r4 (count-sensor NB-1): the board had +/-1.200 mm of lateral float in a
    # 20.4 x 14.4 cavity, and ECO-12 exists because the +/-3.0 mm chord
    # geometry depends on the emitter sitting on its tunnel. Four LOCATING
    # RIBS on the COVER nest the board to +/-0.200 mm. They live in the
    # 1.200 mm gap beside the board, so the PLATE cavity is untouched and
    # B4.6 (board + 1 mm all round vs the plate) still measures 0.000 mm3.
    for px in (-SENS_RIB_X, SENS_RIB_X):
        c += Pos(SENS_BOSS_XC + px, sy * (SENS_BOSS_Y1 - SENS_RIB_D / 2),
                 Z_SENSOR) * Box(SENS_RIB_T, SENS_RIB_D, 8.0)
    for pz in (-SENS_RIB_Z, SENS_RIB_Z):
        c += Pos(SENS_BOSS_XC, sy * (SENS_BOSS_Y1 - SENS_RIB_D / 2),
                 Z_SENSOR + pz) * Box(12.0, SENS_RIB_D, SENS_RIB_T)
    # 2 x M2 clearance holes into the boss ears
    for sz in (1, -1):
        c -= Pos(SENS_BOSS_XC, sy * (SENS_BOSS_Y1 + COVER_T / 2),
                 Z_SENSOR + sz * SENS_SCREW_DZ) * Rot(X=90) * Cylinder(
            1.15, COVER_T + 2)
    # r3: the r8 cover carried a Dia5 grommet port on the duct-socket axis.
    # The cable now leaves through the ear's bottom face inside the plate, so
    # the cover is UNBROKEN -- one fewer dust path into the cavity.
    cov = c if cov is None else cov + c
add_aux("sensor_cover", cov, "#b9b1a1", density=DENS["petg_cf"],
        basis="ECO-12 / N3: 2x printed cover, 2x M2 self-tap into the boss "
              "ears; 4 posts clamp the 18x12x2 board (36 mm2 bearing area, "
              "vs r1's ZERO retention); Dia5 grommeted cable port")

# --- 15. chute storage plug (rev1 N7) ----------------------------------
# RT-7/RT-8: the Dia22 chute mouth is permanently open 181 mm above the
# ground it lands on and is blasted with downwash. A press-fit plug with a
# pull tab closes it in storage and transport.
# r3 (count-sensor NB-1): the r8 plug's sealing land ran from the chute mouth
# up to z = -395.25 and pressed on the two beam-B windows (0.5981 mm3 each),
# scrubbing the bonded sacrificial acrylic at 0.150 mm/side on every fit. The
# four windows occupy z -401.20..-389.30 continuously, so there is no 8 mm
# band of clean bore below them (N7 asks for >= 8 mm): the land moves ABOVE
# the windows and the shank is relieved to Dia21.2 across the window band.
PLUG_INTERF = 0.3
PLUG_LAND_Z0 = Z_SENSOR + 6.25            # -389.00: 0.30 above window A's top
PLUG_LAND_H = 8.0
PLUG_SHANK_R = 10.6                       # 0.40 mm off the window faces
plug = Pos(PCD_R, 0, PLUG_LAND_Z0 + PLUG_LAND_H / 2) * Cylinder(
    (CHUTE_ID + PLUG_INTERF) / 2, PLUG_LAND_H)
plug += Pos(PCD_R, 0, (Z_CHUTE_BOT + PLUG_LAND_Z0) / 2) * Cylinder(
    PLUG_SHANK_R, PLUG_LAND_Z0 - Z_CHUTE_BOT)
# r5 (granule-path MAJOR): the Dia28 flange was a full disc, and the plate's
# count-sensor boss reaches BELOW the chute mouth at |y| >= 11.000 -- measured
# as 2 x 52.811 mm3 of flange-vs-plate interference (x 29.00..40.66,
# |y| 11.00..14.00, z -407.25..-405.25) through the flange's full 2.000 mm
# thickness, so the flange could not reach its seat. The flange is now
# clipped to |y| <= PLUG_FLANGE_HY and keeps its full Dia28 reach in x, which
# is where the stop face is wanted (the bore is Dia22).
PLUG_FLANGE_HY = 10.8
plug += Pos(PCD_R, 0, Z_CHUTE_BOT - 1.0) * (
    Cylinder(14.0, 2.0) & Box(28.0, 2 * PLUG_FLANGE_HY, 2.0))
plug += Pos(PCD_R, 0, Z_CHUTE_BOT - 9.0) * Box(4.0, 20.0, 14.0)
# r4 (granule-path critic: "chute_plug_r9 contains a -3930.3 mm3
# inverted-normal body"): the r9 weight-saving bore was cut BEFORE the flange
# was added, so the flange sealed it back up -- a trapped-air pocket in a TPU
# print and an inverted shell in the STL. The bore is cut LAST now and runs
# out through the bottom face of the flange (z = Z_CHUTE_BOT - 2.0), which
# also lets the plug be squeezed to break the seal on removal.
plug -= Pos(PCD_R, 0, (Z_CHUTE_BOT - 2.0 + PLUG_LAND_Z0 + PLUG_LAND_H - 2.0) / 2
            ) * Cylinder(7.5, (PLUG_LAND_Z0 + PLUG_LAND_H - 2.0) - (Z_CHUTE_BOT - 2.0))
# r4 (granule-path MODERATE 3): "nothing in the geometry prevents dispensing
# into a fitted plug ... one printed tab or a BOM tether line closes it".
# The pull tab gets a Dia4.0 TETHER EYE and the retaining plate gets a
# matching anchor lug (built with the plate, below), so the plug stays
# captive on the payload and hangs in view of the operator when it is out.
PLUG_EYE_D = 4.0
PLUG_EYE_Z = Z_CHUTE_BOT - 11.0
plug -= Pos(PCD_R, 0, PLUG_EYE_Z) * Rot(Y=90) * Cylinder(PLUG_EYE_D / 2, 10.0)
add_aux("chute_plug", plug, "#e8763a", density=DENS["tpu"],
        basis="rev1 N7/r3: TPU storage plug, 0.3 mm diametral interference "
              "over 8 mm of clean Dia22 bore ABOVE the count windows, shank "
              "relieved to Dia21.2 past them; flange + pull tab; ground-only")

# --- 16. service stand (rev1 B12) --------------------------------------
# RT-14 / directive 4: refill = take the whole dispenser off the aircraft.
# Stood chute-down the payload is a 195 mm tall Dia150 object balanced on a
# 35 x 35 mm motor can (tip angle ~11 deg) and the load path runs through the
# gearbox output flange. The stand is a printed tripod cradle: the housing's
# latch-ring underside lands on three pads, the motor and chute hang free in
# the middle, and the support polygon is 3 x r90.
STAND_TOP_Z = Z_RPLATE_BOT - RING_DROP        # the ring underside it carries
STAND_PAD_R = 60.0
STAND_FOOT_R = 90.0
# r2: the r1 ground plane was Z_CHUTE_BOT - 6 = -401.25, but the motor can
# bottoms at Z_MOTOR_BOT = -408.45 -- the payload stood on the stand would
# have had its gearbox/motor 7.20 mm THROUGH the ground, i.e. the stand did
# not actually hold the load path off the motor (B12.1). The plane is now
# below the lowest payload solid, and the clearance is measured.
STAND_GROUND_Z = Z_MOTOR_BOT - 8.0            # flat ground plane
stand = Pos(0, 0, (STAND_GROUND_Z + STAND_GROUND_Z + 4.0) / 2) * (
    Cylinder(STAND_FOOT_R, 4.0) - Cylinder(STAND_FOOT_R - 14.0, 6.0))
# r2: pads moved off 90/210/330 to 60/180/300 so they clear the new
# symmetric harness duct (its outermost material sits at r 56.3, theta
# +/-38.4, z -357.25..-349.25).
for a in (60.0, 180.0, 300.0):
    stand += Rot(Z=a) * (Pos((STAND_PAD_R + STAND_FOOT_R - 7.0) / 2, 0,
                             (STAND_GROUND_Z + 2.0 + STAND_TOP_Z) / 2)
                         * Box(STAND_FOOT_R - 7.0 - STAND_PAD_R, 16.0,
                               STAND_TOP_Z - STAND_GROUND_Z - 2.0))
    # r2: pads pulled in from r46 to r52 so they land on the LATCH-RING
    # footprint (r 52.3..58) only -- at r46 a pad corner clipped the harness
    # duct by 1.0585 mm3 per side.
    stand += Rot(Z=a) * (Pos((STAND_PAD_R + 52.0) / 2, 0, STAND_TOP_Z - 3.0)
                         * Box(STAND_PAD_R - 52.0, 16.0, 6.0))
add_aux("service_stand", stand, "#8f8778", density=DENS["petg_cf"],
        basis="rev1 B12: printed refill cradle; carries the latch-ring "
              "underside on 3 pads at r46..60, feet on a Dia180 circle, motor "
              "+ chute hang clear (tip angle measured in the checks)")

# =====================================================================
# Fill lines molded into the hopper wall. r5 changes both the FEATURE and
# the NUMBER:
#  - mass critic MODERATE ("a physical groove cut into the wall on the
#    strength of a number with <1% margin", and buildability MODERATE
#    "hopper wall cut to 1.7 mm at the two fill-line grooves"): the lines
#    are now RAISED INTERNAL RIBS (triangular section, 45 deg both faces =
#    printable, no support) -- the 2.5 mm wall is not thinned at all.
#  - the MAX line is SOLVED against the pessimistic ledger (CF-PETG at
#    1.31 g/cm3, stepper at 200 g, +10% contingency), not the nominal one,
#    so the strict no-exemption reading survives the density spread.
# =====================================================================
FILL_LINE = Z_TOP_BOT - 10.0   # brim reference (10 mm headspace)


def usable_void(to_z):
    """Usable pellet volume (mm3) from the disc-top sump up to z=to_z."""
    v = sector(20.0, CHAMBER_R, FILL_ARC[0], FILL_ARC[1],
               Z_DISC_TOP, Z_FUN_BOT - Z_DISC_TOP)
    if to_z > Z_FUN_BOT:
        cone = Pos(0, 0, Z_FUN_BOT + FUNNEL_H / 2) * Cone(FUNNEL_RO, HOP_RI, FUNNEL_H)
        if to_z < Z_HOP_BOT:
            cone &= Pos(0, 0, (Z_FUN_BOT + to_z) / 2 - 50) * Box(300, 300,
                                                                 100 + to_z - Z_FUN_BOT)
        v += cone
    if to_z > Z_HOP_BOT:
        v += Pos(0, 0, (Z_HOP_BOT + to_z) / 2) * Cylinder(HOP_RI, to_z - Z_HOP_BOT)
    for k in ("agitator", "pocket_disc", "brush_holder", "brush_bristles",
              "sleeve_bearing", "top_plate"):
        v -= parts[k]["solid"]
    return vol_of(v)


v_use_pre = usable_void(FILL_LINE) / 1000.0        # cm3 at the brim
# --- pessimistic empty mass (drives the MAX line) ---------------------
PESS_DENS = 1.31e-3        # CF-PETG datasheet high end (mass critic)
PESS_MOTOR = 380.0         # vendor GROSS figure for the geared unit
_est_fixed = 65.0 + 57.0 + 8.0 + 15.0 + 3.0   # electronics/fasteners/seals/pcb/bristles
_pess = _est_fixed
for _k, _v in parts.items():
    if _k in ("stepper",):
        _pess += PESS_MOTOR
    elif _k in ("blindmate_pcb", "brush_bristles"):
        continue                      # already in _est_fixed
    elif _k in ("clip_plate", "thrust_washer", "sleeve_bearing"):
        _pess += _v["mass"]
    else:
        _pess += _v["solid"].volume * PESS_DENS
EMPTY_PESS = _pess * 1.10
MASS_RESERVE = 20.0        # explicit reserve so the rib is not knife-edge
# r6: the geared drive costs ~110 g, so the r5 rule (solve the rib from the
# quadruple-conservative ledger AND refuse CONTEXT's exemption for pellets
# above the 250 baseline) now returns a line BELOW the 250 hard minimum --
# i.e. that reading is infeasible, not binding. The shipped MAX rib is
# therefore the VOLUMETRIC brim line, and both strict-reading numbers are
# printed next to it so nothing is hidden.
N_MASS_STRICT = int((1500.0 - EMPTY_PESS - MASS_RESERVE) / PELLET_MASS)
N_FILL_MAX = int(v_use_pre / PELLET_VOL_WORST)


def wall_r(z):
    """Hopper INNER radius at height z (cone below Z_HOP_BOT)."""
    if z >= Z_HOP_BOT:
        return HOP_RI
    return FUNNEL_RO + (z - Z_FUN_BOT) / _tanA


V_SUMP = usable_void(Z_FUN_BOT) / 1000.0   # cm3 below the funnel outlet


def z_for_volume(v_cm3):
    """Fill height for a target usable volume (analytic, cone + cylinder)."""
    def vol(z):
        if z <= Z_FUN_BOT:
            return V_SUMP
        h = min(z, Z_HOP_BOT) - Z_FUN_BOT
        r1 = wall_r(min(z, Z_HOP_BOT))
        v = math.pi * h / 3 * (FUNNEL_RO ** 2 + FUNNEL_RO * r1 + r1 ** 2)
        if z > Z_HOP_BOT:
            v += math.pi * HOP_RI ** 2 * (z - Z_HOP_BOT)
        return V_SUMP + v / 1000.0
    lo, hi = Z_FUN_BOT, FILL_LINE
    for _ in range(60):
        mid = (lo + hi) / 2
        if vol(mid) < v_cm3:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def fill_rib(z, proud):
    """Triangular internal rib (45 deg faces -> support-free), following the
    local wall (cone or cylinder). Rooted 0.5 mm INTO the wall: a
    face-coincident union is the r2 disconnected-solid failure class."""
    def frustum(r0, r1, hh):
        return Cylinder(r0, hh) if abs(r0 - r1) < 1e-6 else Cone(r0, r1, hh)

    h = proud + 0.5
    rA, rB, rC = wall_r(z - h), wall_r(z), wall_r(z + h)
    r = Pos(0, 0, z - h / 2) * (frustum(rA + 0.5, rB + 0.5, h)
                                - frustum(rA + 0.5, rB - proud, h))
    r += Pos(0, 0, z + h / 2) * (frustum(rB + 0.5, rC + 0.5, h)
                                 - frustum(rB - proud, rC + 0.5, h))
    return r


Z_FILL_MAX = z_for_volume(N_FILL_MAX * PELLET_VOL_WORST)
assert Z_FUN_BOT + 5 < Z_FILL_MAX < FILL_LINE, "max-line outside the hopper"
ribs = fill_rib(Z_FILL_MAX, 1.2)
# ...plus a 250-pellet BASELINE reference rib (CONTEXT hard minimum load)
Z_FILL250 = z_for_volume(250 * PELLET_VOL_WORST)
assert Z_FUN_BOT + 5 < Z_FILL250 < FILL_LINE, "250-line outside the hopper"
ribs += fill_rib(Z_FILL250, 0.8)
add("hopper", parts["hopper"]["solid"] + ribs, "#ded7c8",
    density=DENS["petg_cf"],
    basis="[D] shell volume, 2.5 mm wall CF-PETG, %.0f deg funnel + flange/"
          "skirt tabs + raised max/baseline fill-line ribs" % FUNNEL_ANGLE)

# =====================================================================
# Assembly + exports (ALL printed parts individually)
# =====================================================================
import copy

solids = {k: v["solid"] for k, v in parts.items()}
aux_solids = {k: v["solid"] for k, v in aux.items()}
os.makedirs(EXPORT_DIR, exist_ok=True)
REV = "r13"         # rev-1 close-out (r12 = round 6, r11 = round 5, r10 = round 4)
PRINTED = ["top_plate", "fill_cap", "hopper", "meter_housing",
           "pocket_disc", "agitator", "brush_holder", "retaining_plate_chute",
           "electronics_bay", "bay_lid"]
PRINTED_AUX = ["chute_plug", "service_stand", "sensor_cover"]
EXPORT_AUX = ["count_windows", "sensor_boards"]

# --- rev1 r4 (B10; assembly A-8, count-sensor BLOCKING 2) --------------
# r9 shipped retaining_plate_chute_r9.stl with 188 OPEN edges, 1538 three-face
# edges and a volume 8.36 % above its own STEP, and the assembly STL inherited
# it. The STEP was clean, so the defect was in the tessellation of the
# IN-SESSION OCC shape, not in the model. Measured on the r9 STEP with this
# venv: re-importing that same STEP and meshing it gives watertight=True,
# winding=True, 0 non-manifold edges at every tolerance from 5e-4 to 0.1.
# So every STL is now tessellated from the SHIPPED STEP, not from the session
# shape: the two files cannot disagree, and the census below is asserted.
import trimesh as _tm
from collections import Counter as _Counter

MESH_CENSUS = []


def _mesh_census(path, ref_vol):
    """Edge-multiplicity census of an exported STL (B10 / RT-20)."""
    m = _tm.load(path, process=True)
    e = np.sort(m.edges_sorted.reshape(-1, 2), axis=1)
    mult = _Counter(_Counter(map(tuple, e)).values())
    nonman = sum(n for k, n in mult.items() if k not in (2,))
    openedge = mult.get(1, 0)
    comps = _tm.graph.connected_components(m.face_adjacency,
                                           nodes=np.arange(len(m.faces)))
    return dict(path=os.path.basename(path), watertight=bool(m.is_watertight),
                winding=bool(m.is_winding_consistent), euler=int(m.euler_number),
                nonman=int(nonman), openedge=int(openedge),
                bodies=len(comps), faces=len(m.faces), vol=float(m.volume),
                ref=float(ref_vol),
                dvol=100.0 * (float(m.volume) - ref_vol) / max(ref_vol, 1e-9),
                mult={int(k): int(v) for k, v in sorted(mult.items())})


def export_part(solid, name):
    sp = os.path.join(EXPORT_DIR, f"{name}_{REV}.step")
    st = os.path.join(EXPORT_DIR, f"{name}_{REV}.stl")
    export_step(solid, sp)
    export_stl(import_step(sp), st)          # mesh the SHIPPED STEP
    MESH_CENSUS.append(_mesh_census(st, solid.volume))


for name in PRINTED:
    export_part(solids[name], name)
for name in PRINTED_AUX + EXPORT_AUX:
    export_part(aux_solids[name], name)

# r2 (assembly + count-sensor critics): count_windows / sensor_cover are
# FLIGHT hardware and were exported but never entered the assembly compound,
# so no assembly-level interference check could see them. They are in it now.
# chute_plug and service_stand stay out on purpose: both are ground-only and
# the plug's interference (0.3 mm diametral) is a designed press fit.
ASM_AUX = ["count_windows", "sensor_cover", "sensor_boards"]
asm = Compound(children=[copy.copy(v["solid"]) for v in parts.values()]
               + [copy.copy(aux[k]["solid"]) for k in ASM_AUX])
asm.label = f"capsule_dispenser_{REV}"
ASM_STEP = os.path.join(EXPORT_DIR, f"dispenser_{REV}_assembly.step")
ASM_STL = os.path.join(EXPORT_DIR, f"dispenser_{REV}_assembly.stl")
export_step(asm, ASM_STEP)
export_stl(import_step(ASM_STEP), ASM_STL)
_asm_vol = sum(v["solid"].volume for v in parts.values()) + \
    sum(aux[k]["solid"].volume for k in ASM_AUX)
MESH_CENSUS.append(_mesh_census(ASM_STL, _asm_vol))
print("exports written to", EXPORT_DIR)

# ---- B10 EXPORT-INTEGRITY CENSUS (quoted verbatim in BUILD-NOTES-r4) ---
print("\n================ B10 EXPORT INTEGRITY (mesh census of the shipped "
      "STLs; r9: retaining_plate_chute 188 open + 1538 three-face edges, "
      "+8.36 % volume) ================")
print(f"  {'part':26s} {'watertight':>10s} {'winding':>8s} {'euler':>6s} "
      f"{'nonman':>7s} {'open':>5s} {'bodies':>6s} {'faces':>7s} "
      f"{'STL cm3':>9s} {'STEP cm3':>9s} {'delta %':>8s}  edge-multiplicity")
_bad_parts = 0
for c in MESH_CENSUS:
    _isasm = "assembly" in c["path"]
    if not (c["watertight"] and c["winding"] and c["nonman"] == 0) and not _isasm:
        _bad_parts += 1
    print(f"  {c['path'][:-4]:26s} {str(c['watertight']):>10s} "
          f"{str(c['winding']):>8s} {c['euler']:6d} {c['nonman']:7d} "
          f"{c['openedge']:5d} {c['bodies']:6d} {c['faces']:7d} "
          f"{c['vol']/1000:9.3f} {c['ref']/1000:9.3f} {c['dvol']:+8.3f}  "
          f"{c['mult']}")
_parts_ct = len(MESH_CENSUS) - 1
_wt = sum(1 for c in MESH_CENSUS[:-1] if c["watertight"] and c["nonman"] == 0)
_a = MESH_CENSUS[-1]
print(f"  -> PART STLs watertight with 0 non-manifold edges: {_wt}/{_parts_ct} "
      f"(r9: 14/15, and the one failure was the part that carries the count "
      f"sensor, the exit port and the chute)")
_asm_nsol = len(asm.solids())
print(f"  -> assembly: {_a['bodies']} mesh bodies for "
      f"{_asm_nsol} solids, {_a['openedge']} open edges, "
      f"{_a['nonman']} non-manifold edges, volume {_a['vol']/1000:.3f} cm3 vs "
      f"{_a['ref']/1000:.3f} cm3 of source solids ({_a['dvol']:+.3f} %). "
      f"NOTE the assembly is a COMPOUND of separate closed shells: trimesh "
      f"merges coincident vertices across bodies, so any face-to-face contact "
      f"between two parts shows up as a 4-face edge. Non-zero here means "
      f"'two parts touch', not 'the mesh is broken' -- r9 had 188 genuinely "
      f"OPEN edges, which is a different failure.")
EXPECTED_BODIES = {"count_windows": 4, "sensor_cover": 2, "sensor_boards": 2}
_bodybad = [(c["path"], c["bodies"]) for c in MESH_CENSUS[:-1]
            if c["bodies"] != EXPECTED_BODIES.get(c["path"][:-4].rsplit(
                "_", 1)[0], 1)]
print(f"  -> mesh-body count vs expected (a DISCONNECTED lug or a sealed "
      f"internal void shows up here): "
      f"{'all as expected' if not _bodybad else _bodybad}")
assert _bad_parts == 0, f"{_bad_parts} part STLs are not watertight (B10)"
assert _a["openedge"] == 0, "assembly STL has open edges (B10)"
assert not _bodybad, f"unexpected mesh bodies: {_bodybad}"

# =====================================================================
# Geometry checks (printed, measured from the model)
# =====================================================================
print("\n================ GEOMETRY CHECKS (measured) ================")
# ---- rev1 N12: Z-STACK AUDIT. The table existed in r7 but was never
# printed or asserted, which is exactly how the comments came to be 10.0 mm
# stale after NECK_H went 42 -> 52. Both columns are printed now and any
# mismatch > 0.05 mm is a hard failure.
print("Z-STACK AUDIT (derived vs the value written in the source comment; "
      "N12 asks for both columns and +/-0.05 mm):")
_zbad = 0
for _n, _v, _c in Z_STACK_AUDIT:
    _d = _v - _c
    if abs(_d) > 0.05:
        _zbad += 1
    print(f"  {_n:14s} derived {_v:10.3f}   comment {_c:10.3f}   "
          f"delta {_d:+7.3f}  {'**STALE**' if abs(_d) > 0.05 else 'ok'}")
assert _zbad == 0, f"{_zbad} stale Z-stack comments (N12)"

# ---- r6 INTERFACE BLOCK (both r5 interference BLOCKERs) ---------------
print("CLIP-PLATE MAP (containment scan of the imported vendor STEP, 0.5 mm "
      "grid x 0.4 mm z; r5 used a Dia2.4 cylinder + a <5 mm3 threshold and "
      "read a through-WINDOW as a bolt hole):")
for o in sorted(CLIP_OPENINGS, key=lambda o: -o["n"]):
    print(f"  through-opening n={o['n']:5d}  centre ({o['cx']:7.2f},{o['cy']:7.2f})"
          f"  x [{o['x0']:6.2f},{o['x1']:6.2f}]  y [{o['y0']:6.2f},{o['y1']:6.2f}]")
print(f"  -> MOUNT pattern DERIVED: (+/-{BOLT_DX:.2f}, +/-{BOLT_DY:.2f}) = "
      f"{2*BOLT_DX:.0f} x {2*BOLT_DY:.0f}; hole dia {MOUNT_HOLE_D:.2f} through "
      f"the {SLAB_TOP - Z_PLATE_BOT:.1f} mm bolting slab; head pocket above it "
      f"dia {MOUNT_POCKET_D:.2f} -> {MOUNT_SCREW} socket head "
      f"(dia {MOUNT_HEAD_D}) fits with {(MOUNT_POCKET_D - MOUNT_HEAD_D)/2:.2f} mm "
      f"radial clearance. r5 bolted to (+/-6.5,+/-10.5), which this scan shows "
      f"is INSIDE the blind-mate shaft.")
print(f"  -> BLIND-MATE shaft mapped at x +/-{SHAFT_X:.2f}, y +/-{SHAFT_Y:.2f} "
      f"(through); 4 PCB tabs at (+/-{PCB_TAB_DX:.0f},+/-{PCB_TAB_DY:.0f}) with "
      f"dia {TAB_HOLE_D:.2f} holes = the vendor's own board mounts. The payload "
      f"board is placed THERE (r5 put it at y=-35, 35 mm off the pins).")
_pcb_bb = solids["blindmate_pcb"].bounding_box()
print(f"  payload PCB now spans x [{_pcb_bb.min.X:.2f},{_pcb_bb.max.X:.2f}] "
      f"y [{_pcb_bb.min.Y:.2f},{_pcb_bb.max.Y:.2f}] z [{_pcb_bb.min.Z:.2f},"
      f"{_pcb_bb.max.Z:.2f}]; pad face at Z={_pcb_bb.max.Z:.2f} directly under "
      f"the shaft. Fit in the mapped shaft: {SHAFT_X*2 - PCB_X:+.2f} mm in X, "
      f"{SHAFT_Y*2 - PCB_Y:+.2f} mm in Y (vendor board = vendor shaft).")
# nothing of the payload may sit inside the shaft column above the plate face
_shaft_col = Pos(0, 0, (Z_PLATE_BOT + Z_MOUNT) / 2) * Box(2 * SHAFT_X, 2 * SHAFT_Y,
                                                          CLIP_T)
_v_shaft = sum(inter_vol(_shaft_col, s) for k, s in solids.items()
               if k not in ("clip_plate", "blindmate_pcb"))
print(f"  payload material inside the blind-mate shaft column: {_v_shaft:.2f} mm3 "
      f"(must be 0; r5 had 0.0 here too -- and 0.0 pads, which was the bug)")
# mount screws: insert stock, head envelope in the plate cavity, driver path
for sx in (1, -1):
    for sy in (1, -1):
        x, y = sx * BOLT_DX, sy * BOLT_DY
        ins = Pos(x, y, NECK_CAP_BOT + MOUNT_INSERT_L / 2) * Cylinder(
            MOUNT_INSERT_D / 2 + 1.0, MOUNT_INSERT_L)
        stock = inter_vol(ins, solids["top_plate"])
        head = Pos(x, y, SLAB_TOP + 1.1) * Cylinder(MOUNT_HEAD_D / 2, 2.0)
        drv = Pos(x, y, (SLAB_TOP + Z_MOUNT) / 2) * Cylinder(
            MOUNT_HEAD_D / 2, Z_MOUNT - SLAB_TOP)
        shank = Pos(x, y, Z_PLATE_BOT + 2.0) * Cylinder(1.0, 4.0)
        print(f"  mount ({x:+5.1f},{y:+5.1f}): insert-boss stock {stock:6.1f} mm3, "
              f"screw shank vs plate {inter_vol(shank, clip):5.2f} (~0), head "
              f"envelope vs plate {inter_vol(head, clip):5.2f} (~0), driver "
              f"column to Z=-171 {inter_vol(drv, clip):5.2f} (~0)")
# B9a: mount-screw GRIP and thread engagement (r6: 0.90 mm of engagement)
GRIP = SLAB_TOP - INSERT_TOP
print(f"  B9a MOUNT SCREW: head-bearing plane (measured on the vendor STEP) "
      f"Z={SLAB_TOP:.2f}; insert top Z={INSERT_TOP:.2f} -> GRIP {GRIP:.2f} mm; "
      f"{MOUNT_SCREW}x{MOUNT_SCREW_LEN:.0f} -> thread engagement "
      f"{MOUNT_SCREW_LEN - GRIP:.2f} mm into a {MOUNT_INSERT_L:.1f} mm insert "
      f"({'PASS' if 3.2 <= MOUNT_SCREW_LEN - GRIP <= MOUNT_INSERT_L else 'FAIL'}"
      f"; need >=3.2 and <= insert length so it cannot bottom out). r6: grip "
      f"9.10, M2x10 -> 0.90 mm.")
_out_foot = 0.0
for k, s in solids.items():
    if k in ("clip_plate",):
        continue
    bbk = s.bounding_box()
    if bbk.max.Z > Z_PLATE_BOT + 0.01:
        col = Pos(0, 0, (Z_PLATE_BOT + Z_MOUNT) / 2) * Box(50, 50, CLIP_T)
        _out_foot += max(0.0, vol_of(s & Pos(0, 0, (Z_PLATE_BOT + Z_MOUNT) / 2)
                                     * Box(400, 400, CLIP_T)) - inter_vol(s, col))
print(f"  payload volume above the plate face and OUTSIDE the 50x50 clip "
      f"footprint: {_out_foot:.0f} mm3 (fill cap wing bar; ICD keep-out STEP "
      f"is still an open ICD TODO -- carried as a NOTE, re-measured each run)")

# ---- NEW r3: per-part connectivity (the r2 blocker class, now mechanical)
print("\nPER-PART CONNECTIVITY (must be 1 solid each -- r2 root-cause check):")
n_disconnected = 0
for k, v in parts.items():
    ns = len(v["solid"].solids())
    ok = ns == 1
    if not ok:
        n_disconnected += 1
    print(f"  {k:24s} {ns} solid(s)  {'OK' if ok else '**DISCONNECTED**'}")
print(f"  summary: {n_disconnected} disconnected parts")

import trimesh

mtri = trimesh.load(ASM_STL)


def _split_components(mesh):
    """Connected-component split that never calls fill_holes (this venv has
    no networkx, and trimesh's split() reaches for it on any non-watertight
    body -- which is exactly the case we are trying to MEASURE)."""
    comps = trimesh.graph.connected_components(mesh.face_adjacency)
    out = []
    for c in comps:
        sub = trimesh.Trimesh(vertices=mesh.vertices, faces=mesh.faces[c],
                              process=False)
        sub.remove_unreferenced_vertices()
        out.append(sub)
    return out


bodies = _split_components(mtri)
# r2: the expectation has to count SOLIDS, not part names -- count_windows is
# 4 discs and sensor_cover is 2 covers. r7's assembly STL also carried 4
# INVERTED-NORMAL bodies (-15.9 mm3 each) from the tangent standoff union;
# any body with volume <= 0 is a tessellation defect and is now named.
n_expected = len(parts) + sum(
    len(aux[k]["solid"].solids()) for k in ASM_AUX)
print(f"assembly STL bodies: {len(bodies)} (expected = {n_expected} solids -> "
      f"{'OK' if len(bodies) == n_expected else 'MISMATCH'})")
_bad = [b for b in bodies if b.volume <= 0.0]
print(f"  bodies with non-positive volume (inverted normals): {len(_bad)} "
      f"(r7: 4)")
for b in _bad[:8]:
    print(f"    V={b.volume:9.3f} mm3  bbox {np.round(b.bounds, 3).tolist()}")

# ---- r4 (buildability MODERATE): PRINT ORIENTATION support-area check.
# r3 documented orientations that rested on 8.9 mm protrusions; the critic
# measured 41.6% / 36.6% unsupported area. Metric here: fraction of surface
# area on downward faces steeper than 45 deg from horizontal that is NOT on
# the bed plane (i.e. genuinely needs support), per candidate orientation.
# r5 (buildability MINOR: "the builder's search only tries rot 0/180"):
# the search is now over all six axis-aligned orientations, and the
# as-modeled figure is printed alongside the best one.
ORIENT_SET = [("as-modeled", (0, 0)), ("flipped (rotX180)", (180, 0)),
              ("rotX+90", (90, 0)), ("rotX-90", (-90, 0)),
              ("rotY+90", (0, 90)), ("rotY-90", (0, -90))]
SUPPORT = {}
print("\nPRINT ORIENTATIONS (support-needing area, measured on exported STLs;"
      " r5: 6 orientations searched):")
for pname in PRINTED:
    m0 = trimesh.load(os.path.join(EXPORT_DIR, f"{pname}_{REV}.stl"))
    res = []
    for lbl, (rx, ry) in ORIENT_SET:
        mm = m0.copy()
        mm.apply_transform(trimesh.transformations.rotation_matrix(
            math.radians(rx), [1, 0, 0]))
        mm.apply_transform(trimesh.transformations.rotation_matrix(
            math.radians(ry), [0, 1, 0]))
        nz = mm.face_normals[:, 2]
        ar = mm.area_faces
        zc = mm.triangles_center[:, 2]
        zmin = mm.bounds[0][2]
        need = ar[(nz < -math.cos(math.radians(45))) & (zc > zmin + 0.3)].sum()
        res.append((100 * need / ar.sum(), lbl))
    asmod = res[0][0]
    res.sort()
    SUPPORT[pname] = (res[0][0], res[0][1])
    print(f"  {pname:22s} best: {res[0][1]:18s} {res[0][0]:5.1f}% needs support"
          f"   (as-modeled {asmod:.1f}%)")

abb = asm.bounding_box()
print(f"\nassembly bbox X [{abb.min.X:.1f}, {abb.max.X:.1f}]  "
      f"Y [{abb.min.Y:.1f}, {abb.max.Y:.1f}]  Z [{abb.min.Z:.1f}, {abb.max.Z:.1f}]")
stack = Z_MOUNT - abb.min.Z
clearance = abb.min.Z - Z_GROUND
print(f"stack below mounting plane: {stack:.1f} mm (bottom Z = {abb.min.Z:.1f})")
print(f"ground clearance at rest:   {clearance:.1f} mm (ground Z = {Z_GROUND})")

# ---- leg clearance. r4 (r3 interference critic): the tube-axes-only
# method over-reported (92.0 vs true 83.42) because the 1330 aluminum
# adapters sit higher and closer than the tubes. Now measured MESH-TO-MESH
# against the FULL landing gear built from the quiver source (adapters,
# joints, tubes, foam), with the axis method kept as a cross-check.
V = np.asarray(mtri.vertices)
tilt = math.atan2(145.84, 376.47)   # landing_gear/assembly.py
d_leg = 1e9
for sx in (1, -1):
    for sy in (1, -1):
        C = np.array([sx * 194.56, sy * 123.0, -322.5])
        D = np.array([sx * math.sin(tilt), 0.0, -math.cos(tilt)])
        W = V - C
        t = np.clip(W @ D, -200.0, 200.0)   # 400 mm tube
        P = C + t[:, None] * D[None, :]
        d_leg = min(d_leg, float(np.linalg.norm(V - P, axis=1).min()) - 15.0)
print(f"cross-check, assembly-mesh -> leg TUBE axes only: {d_leg:.1f} mm "
      f"(known to over-report; not the carried figure)")

d_gear = None
try:
    import sys as _sys
    import tempfile as _tf
    _sys.path.insert(0, "/tmp/pq-main/src")
    from quiver.airframe_structure.landing_gear.assembly import make_assembly
    gear = make_assembly()
    with _tf.NamedTemporaryFile(suffix=".stl", delete=False) as tf:
        gear_stl = tf.name
    export_stl(gear, gear_stl, tolerance=0.2)
    gm = trimesh.load(gear_stl)
    os.unlink(gear_stl)
    from scipy.spatial import cKDTree
    gs, _ = trimesh.sample.sample_surface(gm, 250000)
    gp = np.vstack([np.asarray(gm.vertices), gs])
    ds, _ = trimesh.sample.sample_surface(mtri, 250000)
    dp = np.vstack([V, ds])
    dvv = cKDTree(gp).query(dp)[0]
    dmin_vv = dvv.min()
    # refine: exact point-to-triangle for the dispenser points nearest gear
    near = dp[np.argsort(dvv)[:2000]]
    _, dexact, _ = trimesh.proximity.closest_point(gm, near)
    d_gear = float(dexact.min())
    print(f"FULL-GEAR clearance (mesh-to-mesh, {len(gp)} gear pts, exact "
          f"point-to-triangle refine): {d_gear:.2f} mm "
          f"(r3 critic independent: 83.42 mm)")
except Exception as e:
    print(f"FULL-GEAR measurement unavailable ({e}); carrying the r3 "
          f"interference critic's independent figure: 83.42 mm")
print("prop clearance (r2 interference critic, full-assembly measurement): "
      "lowest propulsion solid Z -18.50 -> vertical gap 152.5 mm; blade disk "
      "Z +44.04, tip r 304.8 at hubs (+/-449.4,+/-449.4) -> radial gap 239.3 mm")

# pocket geometry
pitch = math.pi * 2 * PCD_R / N_POCKET
print(f"\npocket pitch at PCD {pitch:.1f} mm; web between pockets {pitch - 2*POCKET_R:.1f} mm")
print(f"disc t {DISC_T} vs worst pellet {PELLET_D_MAX}: seated pellet rests on "
      f"the retaining plate (through the {UNDER_GAP} under-gap) -> top "
      f"{DISC_T + UNDER_GAP - PELLET_D_MAX:.1f} mm below disc surface (r3 critic "
      f"correction; conservative); stacked 2nd sphere protrudes "
      f"{2*PELLET_D_MAX - DISC_T - UNDER_GAP:.1f} mm (brush wipes >{BRUSH_WIPE} mm)")
print(f"fragment window: brush wipe {BRUSH_WIPE} mm < roof clearance {ROOF_CLEAR} mm -> "
      f"anything passing the brush passes the roof")
# r6: the restack window is measured from the DOWNSTREAM EDGE of the 13 mm
# wiper station (r5 measured it from the wiper plane, which flattered it).
_wiper_out = BRUSH_A - math.degrees((HOLD_W / 2) / PCD_R)
restack_arc = (_wiper_out - FILL_ARC[0]) * math.pi / 180 * PCD_R
print(f"restack window: wiper station spans theta "
      f"{_wiper_out:.1f}..{BRUSH_A + math.degrees((HOLD_W/2)/PCD_R):.1f} deg "
      f"({HOLD_W:.0f} mm at PCD); from its downstream edge to the roof entry "
      f"({FILL_ARC[0]:.0f} deg) is {_wiper_out - FILL_ARC[0]:.1f} deg = "
      f"{restack_arc:.2f} mm at PCD (<< pellet radius {PELLET_D/2:.0f} mm -> "
      f"nothing can restack into a pocket after the wiper)")
print(f"funnel angle {FUNNEL_ANGLE:.0f} deg (r4: 60.0, at/below the printed-PETG "
      f"mass-flow threshold), h={FUNNEL_H} mm; rotation direction -Z (CW from "
      f"above): pockets pass wiper {BRUSH_A:.0f}deg then roof edge "
      f"{FILL_ARC[0]:.0f}deg; arrow engraved at theta=157.5 r25.5")

# ---- r5 WIPER: the r4 critic's MAJOR was that the wiper was a solid
# printed fin with nowhere to put bristles. Measure the real thing.
bb_bris = solids["brush_bristles"].bounding_box()
trim = (CHAN_Z0 + CHAN_H) - BRIS_TIP - CHAN_H
print(f"\nWIPER (r6, 2 parts): holder {HOLD_W} x {HOLD_H} mm, bristle channel "
      f"{CHAN_W} x {CHAN_H} mm; COTS strip backing {BRISTLE_W} mm; measured "
      f"free trim {trim:.2f} mm (bristle bbox z {bb_bris.min.Z:.2f}..{bb_bris.max.Z:.2f}, "
      f"tip at disc+{bb_bris.min.Z - Z_DISC_TOP:.2f} = wipe line)")
_E_N, _E_P = 2500.0, 4000.0          # MPa, nylon 6.6 filament / CF-PETG [J]
_d_fil = 0.15                        # mm filament ASSUMPTION
_k_fil = 3 * _E_N * (math.pi * _d_fil ** 4 / 64) / trim ** 3
_k_fin = 48 * _E_P * (1.7 * 1.6 ** 3 / 12) / 27.0 ** 3   # r4 fin, both ends held
print(f"  compliance [D]: single Dia{_d_fil} nylon filament k = {_k_fil:.4f} N/mm; "
      f"~30 filaments in contact -> ~{30*_k_fil:.2f} N/mm, vs the r4 solid "
      f"CF-PETG fin at {_k_fin:.0f} N/mm ({_k_fin/(30*_k_fil):.0f}x stiffer). "
      f"Concept 2.3's 'compliant' claim is restored in the sense that matters "
      f"(contact force on a friable pellet), NOT as a 20 mm Kinze trim.")
# seat floor stock: the rebate is open at the TOP (no thin ceiling any more,
# r4 MINOR 1.5 mm) but there must be roof material UNDER the holder at both
# supports, and the holder must not touch the disc.
pr_f = Rot(Z=BRUSH_A) * (Pos(16.0, 0, (Z_ROOF_BOT + CHAN_Z0 - 0.15) / 2)
                         * Box(3, 3, CHAN_Z0 - 0.15 - Z_ROOF_BOT))
print(f"  INNER support: seat floor stock under the holder at r16 "
      f"{inter_vol(pr_f, solids['meter_housing']):.1f} mm3 ("
      f"{CHAN_Z0 - 0.15 - Z_ROOF_BOT:.2f} mm of roof below the rebate)")
pilot = Rot(Z=BRUSH_A) * (Pos(50.1, 0, BRUSH_SCREW_Z) * Rot(Y=90)
                          * Cylinder(2.2, 4.0))
print(f"  OUTER support: the wall window is open below the holder (the "
      f"bristles pass through it), so the outer end is carried by the end tab "
      f"M3 into the wall pilot at z={BRUSH_SCREW_Z:.1f}: pilot thread stock "
      f"{inter_vol(pilot, solids['meter_housing']):.1f} mm3, tab spans z "
      f"{TAB_Z0:.1f}..{TAB_Z1:.1f} and covers the window mouth")
_I = HOLD_H * HOLD_W ** 3 / 12
_F_LIP = DRIVE_T_MAX / (PCD_R / 1000)     # recovery force at the pocket lip
print(f"  holder beam check [D]: 27 mm free span, tangential load, "
      f"I = {_I:.1f} mm4; at the r6 RECOVERY force {_F_LIP:.1f} N (the whole "
      f"drive, applied at the nose) sigma = "
      f"{(_F_LIP*27/4)*(HOLD_W/2)/_I:.1f} MPa and deflection "
      f"{_F_LIP*27**3/(48*4000*_I):.3f} mm (CF-PETG ~50-70 MPa yield)")
# the open-topped seat must not become a NEW leak class. The escape route
# would be outboard along the top of the seat at the wall (r47..52.6); the
# hopper cone foot sits on that face and closes it. Measured as the free
# height between the holder top and the hopper underside at r=49.
free_h = 0.0
for h in np.arange(0.1, 6.0, 0.1):
    slab = Rot(Z=BRUSH_A) * (Pos(49.0, 0, Z_FUN_BOT - HOLD_H / 2 - 0.05 + HOLD_H / 2 + h / 2)
                             * Box(3.0, 3.0, h))
    if sum(inter_vol(slab, solids[n]) for n in
           ("meter_housing", "hopper", "brush_holder")) > 0.05:
        break
    free_h = h
print(f"  wiper-seat leak class: free height above the holder at the wall "
      f"(r49) = {free_h:.2f} mm, tangential clearance 2 x 0.15 mm -> nothing "
      f"of pellet or fines class (>=3 mm) escapes outboard; the hopper cone "
      f"foot closes the seat top and the end tab closes its outer mouth")

# ---- r6 CONTACT ORDER at the wiper station (r5 BLOCKING/MAJOR: "the rigid
# wiper holder leads the compliant bristles for every object more than
# 5.45 mm proud"). Sweep a Dia4 fragment standing PROUD of the disc face
# around the station and report which part it touches FIRST.
print("  CONTACT ORDER (Dia4 fragment on the disc face, swept 0.25 deg; the "
      "compliant element must be first at every height):")
for proud in (2.0, 3.0, 5.0, 7.0, 9.0, 11.5):
    frag = Pos(PCD_R, 0, Z_DISC_TOP + proud / 2) * Cylinder(2.0, proud)
    first = {}
    for th in np.arange(BRUSH_A + 14.0, FILL_ARC[0] - 6.0, -0.25):
        f = Rot(Z=th) * copy.copy(frag)
        for k in ("brush_bristles", "brush_holder", "meter_housing"):
            if k not in first and inter_vol(f, solids[k]) > 0.02:
                first[k] = th
        if len(first) == 3:
            break
    order = sorted(first.items(), key=lambda kv: -kv[1])
    if not order:
        verdict = "   no contact"
    elif order[0][0] == "brush_bristles":
        verdict = "   OK (compliant first)"
    elif proud >= (CHAN_Z0 - Z_DISC_TOP) - 0.01:
        verdict = "   OK (taller than the rail: the LIFTING overhang takes it)"
    else:
        verdict = "   **RIGID FIRST**"
    print(f"    proud {proud:5.1f} mm: " + " -> ".join(
        f"{k}@{v:.2f}deg" for k, v in order) + verdict)
# face-normal audit, the r5 critic's own method, on the EXPORTED solids:
# every upstream-facing face at the wiper station and at the transfer entry
# must be INCLINED (r5: "the only entry face with a tangential component has
# normal (-0.77,-0.64,0.00), n_z=+0.00" -- a pure square stub).
_d = np.array([math.sin(math.radians(BRUSH_A)), -math.cos(math.radians(BRUSH_A)), 0.0])
for pname, lo, hi in (("brush_holder", Z_DISC_TOP, Z_DISC_TOP + ROOF_T + 2),
                      ("meter_housing", Z_DISC_TOP + 1.0, Z_DISC_TOP + ROOF_T)):
    m = trimesh.load(os.path.join(EXPORT_DIR, f"{pname}_{REV}.stl"))
    n, ar, c = m.face_normals, m.area_faces, m.triangles_center
    sel = (n @ _d) < -0.3
    if lo is not None:
        rr = np.hypot(c[:, 0], c[:, 1])
        th = np.degrees(np.arctan2(c[:, 1], c[:, 0])) % 360
        sel &= (c[:, 2] > lo) & (c[:, 2] < hi) & (rr > 20) & (rr < 47)
        if pname == "meter_housing":
            sel &= (th > FILL_ARC[0] - 40) & (th < FILL_ARC[0] + 1)
    A = ar[sel].sum()
    if A <= 0:
        print(f"    {pname:14s}: no upstream-facing faces in the window")
        continue
    nz = n[sel][:, 2]
    flat = ar[sel][np.abs(nz) < 0.05].sum()
    print(f"    {pname:14s}: {A:7.1f} mm2 of upstream-facing faces, "
          f"area-weighted n_z {float((nz*ar[sel]).sum()/A):+.2f}, "
          f"square-stub area (|n_z|<0.05) {flat:.2f} mm2 = {100*flat/A:.1f}% "
          f"(r5's entry: 100%)")

# ---- r4: B8.3 FIRST-CONTACT AUDIT -- what a proud fragment ACTUALLY hits --
# The r3 granule-path critique (MODERATE 1) measured the nose UNDERSIDE as a
# function of theta, saw it jump 1.50 -> 7.45 mm in one 0.05 deg step and
# concluded "for every object between 1.50 and 7.45 mm proud the rigid
# element is a 5.95 mm square wall, lift/push = cot 89.7 = 0.005". That is a
# silhouette measurement, not a contact measurement: the step it found is the
# END of the nose prism, past which there is no nose at all. What a proud
# object meets is measured here by casting a ray ALONG THE TRAVEL DIRECTION
# at the object's crown height and reading the first face it hits, on the
# exported mesh. Travel is -theta, so the ray runs local -y.
print("\nB8.3 FIRST-CONTACT AUDIT (ray along the travel direction at the "
      "crown height of a proud object; r3 MODERATE 1 claimed a 89.6-89.8 deg "
      "wall over the whole 1.50-7.45 mm band):")
_hm = trimesh.load(os.path.join(EXPORT_DIR, f"brush_holder_{REV}.stl"))
_ca, _sa = math.cos(math.radians(BRUSH_A)), math.sin(math.radians(BRUSH_A))


def _loc2w(x, y, z):
    return np.array([x * _ca - y * _sa, x * _sa + y * _ca, z])


_dirw = _loc2w(0.0, -1.0, 0.0) - _loc2w(0.0, 0.0, 0.0)
for _pr, _lbl in ((1.80, "Dia5.0 fragment, D13 seat, centred"),
                  (2.95, "Dia6.0 fragment, D13 seat, centred"),
                  (4.08, "Dia7.0 fragment, D13 seat, centred"),
                  (6.00, "Dia9.0-class shard"),
                  (7.60, "above the nose top (7.45)")):
    _row = []
    for _r in (22.0, 32.0, 46.5):
        _o = _loc2w(_r, 14.0, Z_DISC_TOP + _pr)
        _loc, _idx, _tri = _hm.ray.intersects_location(
            ray_origins=_o[None, :], ray_directions=_dirw[None, :],
            multiple_hits=False)
        if len(_loc) == 0:
            _row.append(f"r{_r:.0f}: no contact")
            continue
        _n = _hm.face_normals[_tri[0]]
        _ny = float(_n[0] * -_sa + _n[1] * _ca)       # local +y component
        _nz = float(_n[2])
        _yl = float(-_loc[0][0] * _sa + _loc[0][1] * _ca)   # local tangential
        _ang_h = math.degrees(math.atan2(abs(_nz), abs(_ny))) if abs(_ny) > 1e-9 \
            else 90.0
        _row.append(f"r{_r:4.1f}: y={_yl:+6.2f} n=({_ny:+.3f},{_nz:+.3f}) "
                    f"face {90 - _ang_h:5.1f} deg from horiz, lift/push "
                    f"{abs(_nz)/max(abs(_ny), 1e-9):5.2f}")
    print(f"    {_pr:5.2f} mm proud ({_lbl}):")
    for _t in _row:
        print(f"        {_t}")
# ---- r5 (granule-path MODERATE 1): the ray above is a FLAT-TOPPED COLUMN
# test. A rounded fragment is WIDER BELOW ITS CROWN, so it reaches the nose
# earlier and lower. This is the r4 critic's method: sweep the fragment as a
# SPHERE and take first contact from a closest-point query, then read the
# contact normal as the direction from the contact point to the sphere centre
# (that is the direction the reaction pushes the fragment).
print("\nB8.3b SWEPT-SPHERE FIRST CONTACT (rounded fragment, 0.05 deg steps, "
      "closest-point query on the exported brush_holder; the r4 critic showed "
      "the crown-height ray above is only valid for a flat-topped column):")
print("     sign convention: n_z < 0 means the reaction presses the fragment "
      "DOWN into the pocket; n_z > 0 would mean it is LIFTED over the nose")
for _d, _crown in ((5.0, 1.80), (6.0, 2.95), (7.0, 4.08), (9.0, 6.00),
                   (13.0, 11.50)):
    for _r in (26.7, PCD_R):
        _zc = Z_DISC_TOP + _crown - _d / 2.0
        _hit = None
        for _th in np.arange(175.0, 129.9, -0.05):
            _a = math.radians(_th)
            _c = np.array([[_r * math.cos(_a), _r * math.sin(_a), _zc]])
            _cp, _dist, _tri = trimesh.proximity.closest_point(_hm, _c)
            if _dist[0] <= _d / 2.0:
                _v = _c[0] - _cp[0]
                _n = _v / np.linalg.norm(_v)
                _tg = np.array([-math.sin(_a), math.cos(_a), 0.0])
                _nt = abs(float(np.dot(_n, _tg)))
                _hit = (_th, float(_cp[0][2]) - Z_DISC_TOP, _n,
                        abs(float(_n[2])) / max(_nt, 1e-9))
                break
        if _hit:
            print(f"     Dia{_d:4.1f} crown +{_crown:5.2f}, r={_r:4.1f}: first "
                  f"contact theta {_hit[0]:7.2f}, contact height "
                  f"{_hit[1]:+.3f} mm above the disc, n=({_hit[2][0]:+.3f},"
                  f"{_hit[2][1]:+.3f},{_hit[2][2]:+.3f}) -> |n_z|/|n_tang| = "
                  f"{_hit[3]:5.2f} "
                  + ("(pressed DOWN)" if _hit[2][2] < -1e-6 else
                     "(pure anti-travel STUB, no vertical component)"
                     if abs(_hit[2][2]) <= 1e-6 else "(LIFTED)"))
        else:
            print(f"     Dia{_d:4.1f} crown +{_crown:5.2f}, r={_r:4.1f}: NO "
                  f"CONTACT over theta 175..130")
print(f"    nose geometry for reference: flat underside at {NOSE_GAP:.2f} mm "
      f"spans local y {NOSE_Y2:+.2f}..{NOSE_Y0:+.2f}; the LEADING end face is "
      f"a blunt vertical tip only {0.6:.2f} mm tall (y = {NOSE_Y0:+.2f}, "
      f"z = {NOSE_GAP:.2f}..{NOSE_GAP + 0.6:.2f} above the disc, "
      f"{(NOSE_R1-NOSE_R0)*0.6:.1f} mm2 total); above it the confronting face "
      f"is the {math.degrees(math.atan2(NOSE_H, NOSE_RUN)):.1f} deg forward "
      f"ramp running to the rail underside at "
      f"{CHAN_Z0 - Z_DISC_TOP:.2f} mm.")

# ---- r6: TRANSFER-ARC CEILING PROFILE (pellet-path BLOCKING #1) -------
# The r5 critic measured the ceiling as "None at 130.00 deg and 1.508 mm at
# 129.90 -- a square step within 0.1 deg", because r5's ramp was cut into the
# roof TOP. Measure the ceiling the way a pellet meets it: for each radius
# and angle, find the lowest housing material above the disc.
print("\nTRANSFER-ARC CEILING PROFILE (lowest housing material above the disc "
      "face, mm above disc top; r5: a square step from open to 1.508):")
CEIL = {}


def ceiling_at(th, r):
    for h in np.arange(ROOF_CLEAR, ROOF_T + ROOF_CLEAR + 0.51, 0.25):
        p = Rot(Z=th) * (Pos(r, 0, Z_DISC_TOP + h) * Box(0.6, 0.6, 0.4))
        if inter_vol(p, solids["meter_housing"]) > 1e-4:
            return h
    return None


_ths = [FILL_ARC[0] + 1, FILL_ARC[0], FILL_ARC[0] - 2, FILL_ARC[0] - 5,
        FILL_ARC[0] - 10, FILL_ARC[0] - 20, FILL_ARC[0] - 34, 90.0, 45.0, 5.0]
print("      theta:" + "".join(f"{t:8.1f}" for t in _ths))
for r in (24.5, 32.0, 39.5, 45.5):
    row = [ceiling_at(t, r) for t in _ths]
    CEIL[r] = row
    print(f"  r={r:5.1f}   " + "".join(
        (f"{v:8.2f}" if v is not None else "    open") for v in row))
_ramp_ok = all(row[1] is None or row[1] > ROOF_T for row in CEIL.values())
print(f"  ramp: {RAMP_DEG:.0f} deg from horizontal cut into the roof "
      f"UNDERSIDE, tangential run {RAMP_RUN:.1f} mm = {RAMP_ARC_DEG:.1f} deg "
      f"of arc at the PCD; the ceiling is open at the entry edge at every "
      f"radius ({'PASS' if _ramp_ok else 'FAIL'}) and descends to "
      f"{ROOF_CLEAR:.1f} mm. Mechanical advantage on a proud fragment [D]: a "
      f"drive force F normal to the ramp gives F_vert = F/(tan{RAMP_DEG:.0f} "
      f"+ mu) = {1/(math.tan(math.radians(RAMP_DEG)) + 0.4):.2f} F at mu=0.4 "
      f"-- the ramp CRUSHES a proud fragment down into the pocket instead of "
      f"stubbing it against a square edge.")
# r5 (granule-path MINOR 1): the ramp is a constant dz/dtheta surface, so the
# angle a granule meets is a FUNCTION OF RADIUS and the single PCD number is
# not the whole story. Publish the range, and note where it falls below the
# 1.44 self-locking line the same notes use elsewhere.
print(f"  ENTRY-RAMP ANGLE IS A RANGE, NOT '{RAMP_DEG:.0f} deg' (constant "
      f"dz/dtheta -> the arc length, hence the angle, scales with r):")
_A_HI, _A_LO = FILL_ARC[0] - 1.0, FILL_ARC[0] - RAMP_ARC_DEG + 1.0
for _r in (20.5, 22.0, 24.5, PCD_R, 39.5, 46.5):
    _c_hi, _c_lo = ceiling_at(_A_HI, _r), ceiling_at(_A_LO, _r)
    if _c_hi is None or _c_lo is None:
        print(f"     r={_r:5.1f}: ceiling open at one end "
              f"({_c_hi}, {_c_lo}) -- not on the ramp")
        continue
    _arc = math.radians(_A_HI - _A_LO) * _r
    _ang = math.degrees(math.atan2(_c_hi - _c_lo, _arc))
    print(f"     r={_r:5.1f}: ceiling {_c_hi:6.3f} -> {_c_lo:5.3f} = drop "
          f"{_c_hi - _c_lo:5.3f} mm over {_arc:6.3f} mm of arc -> "
          f"{_ang:5.2f} deg, cot = {1 / math.tan(math.radians(_ang)):5.3f}"
          + ("   <- below the 1.44 self-locking line"
             if 1 / math.tan(math.radians(_ang)) < 1.44 else ""))
print(f"     no action: the nose covers r {NOSE_R0:.1f}..{NOSE_R1:.1f} at "
      f"{NOSE_GAP:.3f} mm, so nothing more than {NOSE_GAP:.3f} mm proud ever "
      f"reaches the ramp and anything less never touches it.")

# ---- r4: REVERSE (RECOVERY) FREE TRAVEL, MEASURED ---------------------
# r2 shipped the mitigation as text -- "bound the reverse-oscillate stroke to
# < 6 deg" -- and the r3 granule-path critic measured two parks with less
# than that for a stacked second granule (0.25 deg at 157.5, 2.75 at 247.5).
# The bound is now MEASURED here, at 0.25 deg, by ray-casting the ceiling
# above the disc on the exported housing + holder meshes, and it is the
# measured number that goes into the notes.
print("\nREVERSE-STROKE FREE TRAVEL (recovery runs +theta; ceiling ray-cast "
      "at the PCD on meter_housing + brush_holder, 0.25 deg steps; r2's "
      "shipped '< 6 deg' bound is SUPERSEDED by these numbers):")
_rev_m = trimesh.util.concatenate([
    trimesh.load(os.path.join(EXPORT_DIR, f"meter_housing_{REV}.stl")),
    trimesh.load(os.path.join(EXPORT_DIR, f"brush_holder_{REV}.stl"))])


def _ceiling_ray(th, r=PCD_R):
    o = np.array([[r * math.cos(math.radians(th)), r * math.sin(math.radians(th)),
                   Z_DISC_TOP + 0.02]])
    loc, _, _ = _rev_m.ray.intersects_location(
        ray_origins=o, ray_directions=np.array([[0.0, 0.0, 1.0]]))
    if len(loc) == 0:
        return None
    return float(loc[:, 2].min()) - Z_DISC_TOP


# the parks that can hold a proud object at all: those in the OPEN sump
# window. Under the roof the ceiling is ROOF_CLEAR = 1.50 mm, so an object
# 2.0 mm or more proud cannot be parked there in the first place.
_PARKS = sorted(p for p in {(157.5 + 22.5 * k) % 360 for k in range(16)}
                if FILL_ARC[0] <= p <= FILL_ARC[1])
_OBJ = (2.0, 5.0, 11.5)
print("     park theta   " + "".join(f"{h:>10.1f} mm proud" for h in _OBJ))
_worst = {h: 9e9 for h in _OBJ}
for _p in _PARKS:
    _cells = []
    _c0 = _ceiling_ray(_p)
    for _h in _OBJ:
        if _c0 is not None and _c0 < _h - 1e-6:
            # the object cannot be parked here in the first place (the wiper
            # or the roof is already lower than the object is tall)
            _cells.append(f"  n/a ({_c0:5.2f} mm)")
            continue
        _t, _free = 0.0, None
        while _t <= 120.0:
            _c = _ceiling_ray(_p + _t)
            if _c is not None and _c < _h - 1e-6:
                _free = _t
                break
            _t += 0.25
        if _free is None:
            _free = 120.0
        _worst[_h] = min(_worst[_h], _free)
        _cells.append(f"{_free:13.2f} deg")
    print(f"     {_p:8.1f}   " + "".join(_cells))
print("     -> GUARANTEED reverse free travel at ANY park the object can "
      "actually occupy: "
      + ", ".join(f"{h:.1f} mm proud -> {_worst[h]:.2f} deg" for h in _OBJ)
      + f". Anything the nose lets through is <= {NOSE_GAP:.2f} mm proud and "
      f"has the full stroke; an 11.5 mm STACK (a second granule sitting on a "
      f"seated one) is the case that is bounded, and the bound is the "
      f"measured number above, not '< 6 deg'.")

# =====================================================================
# r6: WEDGE-JAM CONSTRUCTION, TORQUE BUDGET, CONTACT ORDER
# (CONTEXT directive, Thomas 2026-08-06 23:03, items 1-4; and the r5
# pellet-path BLOCKING "the constructed wedge jam is NOT defeated" +
# MAJOR "there is no torque budget anywhere in the model or the notes")
# =====================================================================
print("\n================ WEDGE-JAM (CONTEXT directive) ================")
MU = 0.4                      # pellet/PETG friction ASSUMPTION (friction
                              # angle 21.8 deg) -- the critic's own value
R_PEL = PELLET_D_MAX / 2
DEPTH_BELOW_TOP = DISC_T + UNDER_GAP - 2 * R_PEL     # crown below shear line
print(f"4. POCKET GEOMETRY: bore r{POCKET_R:.2f}, depth {DISC_T:.1f} + "
      f"{UNDER_GAP:.1f} under-gap; a seated Dia{PELLET_D_MAX:.0f} pellet's "
      f"crown sits {DEPTH_BELOW_TOP:.2f} mm BELOW the disc top (the shear "
      f"line), so a whole seated pellet is never in the shear plane. Anything "
      f"that settles below the shear line is safe by construction.")
print("   worst-case wedged sliver (the r5 critic's construction), rebuilt:")
print("     w mm  seats(y) mm  below-top mm  wedge half-angle  self-lock?  "
      "proud-of-nose height  shear area mm2  shear force N")
JAM = []
for w in (1.0, 2.0, 3.0, 5.0):
    if w >= POCKET_R:
        continue
    y = math.sqrt(max(R_PEL ** 2 - (POCKET_R - w) ** 2, 1e-9))   # seat height
    below = DEPTH_BELOW_TOP + (R_PEL - y)                        # top of seat
    half = math.degrees(math.asin(min(y / R_PEL, 1.0))) / 2
    lock = half < math.degrees(math.atan(MU))
    h_nose = below + NOSE_GAP                                    # to reach the nose
    # chord of the crescent at the seat plane, pellet pushed hard against the
    # bore on the leading side: gap opens to 2*(POCKET_R - r_s) on the far side
    r_s = math.sqrt(max(R_PEL ** 2 - y ** 2, 1e-9))
    e = POCKET_R - r_s
    chord = 2 * math.sqrt(max(r_s ** 2 - max(r_s - w, 0) ** 2, 1e-9))
    area = w * chord
    force = area * PELLET_STRENGTH_MPA
    JAM.append((w, area, force, half, lock))
    print(f"    {w:4.1f}  {y:9.2f}  {below:11.2f}  {half:14.1f}  "
          f"{'YES':>10}" if lock else f"    {w:4.1f}  {y:9.2f}  {below:11.2f}  "
          f"{half:14.1f}  {'no':>10}", end="")
    print(f"  {h_nose:19.2f}  {area:14.1f}  {force:12.1f}")
W_SHEAR = max(f for _, _, f, _, _ in JAM)
print(f"   (shear area = sliver thickness x the measured crescent chord; "
      f"shear stress taken as the {PELLET_STRENGTH_MPA} MPa the US4172714 "
      f"crush figure normalises to -- ASSUMPTION, IFDC S-115 bench test is "
      f"the closing action)")
# r6 (granule-path MODERATE 2, raised in round 4 and again in round 5 and
# never actioned): the table above prints the drive's CAPABILITY but not the
# BOUND. The row that decides the argument is the WIDEST SELF-LOCKING sliver
# -- wider than that and the wedge is not self-locking, so it is pushed out
# rather than held -- and the three shard geometries that can sit in that
# crescent. Bisected on the same construction the table uses.
_wlo, _whi = 0.5, POCKET_R - 0.01
for _ in range(60):
    _wm = 0.5 * (_wlo + _whi)
    _ym = math.sqrt(max(R_PEL ** 2 - (POCKET_R - _wm) ** 2, 1e-9))
    if math.degrees(math.asin(min(_ym / R_PEL, 1.0))) / 2 < math.degrees(
            math.atan(MU)):
        _wlo = _wm
    else:
        _whi = _wm
W_LOCK = _wlo
_ylk = math.sqrt(max(R_PEL ** 2 - (POCKET_R - W_LOCK) ** 2, 1e-9))
_rslk = math.sqrt(max(R_PEL ** 2 - _ylk ** 2, 1e-9))
print(f"   SHEAR-BACKSTOP BOUND (this is where 'shear as backstop' stops "
      f"working; construction: conforming shard of radial width w on the "
      f"crescent radius r_s, sheared at the {NOSE_GAP:.3f} mm nose/roof "
      f"plane):")
print(f"     widest SELF-LOCKING sliver w = {W_LOCK:.3f} mm (half-angle = "
      f"atan(mu={MU}) = {math.degrees(math.atan(MU)):.2f} deg), seats "
      f"{_ylk:.3f} mm above the granule centre, crescent radius r_s = "
      f"{_rslk:.3f} mm")
for _ang, _lbl in ((90.0, "90 deg conforming shard"),
                   (180.0, "180 deg conforming shard"),
                   (360.0, "full-ring crescent")):
    _arc = math.radians(_ang) * _rslk
    _A = W_LOCK * _arc
    _F = _A * PELLET_STRENGTH_MPA
    print(f"     {_lbl:24s} arc {_arc:6.2f} mm  A {_A:7.2f} mm2  F "
          f"{_F:7.2f} N  -> {20.4/_F:5.2f}x at recovery (20.4 N), "
          f"{12.2/_F:5.2f}x at normal current (12.2 N)"
          f"{'  <- STALLS' if _F > 20.4 else ''}")
print(f"     (the round-5 granule-path critic derived the same bound "
      f"independently on the r11 exports and got w = 2.791 mm -> 9.63 N "
      f"(2.12x / 1.27x), 180 deg shard 19.26 N (1.06x / 0.63x), full ring "
      f"38.53 N (0.53x / 0.32x). Both constructions say the same thing: the "
      f"backstop covers a partial shard and runs out at a full-ring crescent, "
      f"where the drive STALLS rather than shears -- which is the intended "
      f"failure mode, and it is now printed instead of implied.)")

# --- torque budget ---------------------------------------------------
print("\nTORQUE BUDGET at the disc (r5 MAJOR: 'there is no torque budget "
      "anywhere in the model or the notes'):")
RHO_BULK = PELLET_MASS / PELLET_VOL_WORST * 1e3        # kg/m3 from the packing
K_JAN, MU_W = 0.4, 0.4
P_SAT = RHO_BULK * 9.81 * (2 * HOP_RI / 1000) / (4 * K_JAN * MU_W)   # Pa
A_WIN = math.pi * (CHAMBER_R ** 2 - 20.0 ** 2) * (FILL_ARC[1] - FILL_ARC[0]) / 360
N_BED = P_SAT * A_WIN * 1e-6                            # N on the disc face
T_BED = MU * N_BED * 0.034
A_FIN = 3 * 2 * AGIT_FINGER_R * (AGIT_FINGER_RO - 10.0)
T_AGIT = 3.0 * P_SAT * A_FIN * 1e-6 * 0.028             # passive coeff ~3 [J]
A_NOSE = (NOSE_R1 - NOSE_R0) * (CHAN_Z0 - NOSE_Z0)
T_NOSE = 3.0 * P_SAT * A_NOSE * 1e-6 * 0.033
T_BEAR = 0.2 * 3.0 * (BUSH_ID / 2 / 1000) + 0.15 * (N_BED + 0.6) * 0.0135
# detent: ball rides out of a spherical seat; max flank angle from geometry
_rim = math.sqrt(max(DIMPLE_SPH_R ** 2 - (DIMPLE_SPH_R - DIMPLE_DEPTH) ** 2, 0))
_beta = math.degrees(math.asin(min(_rim * (DIMPLE_SPH_R - PLUNGER_BALL_R)
                                   / DIMPLE_SPH_R / (DIMPLE_SPH_R - PLUNGER_BALL_R), 1)))
_tb = math.tan(math.radians(_beta))
F_DET = PLUNGER_F * (_tb + MU) / max(1 - MU * _tb, 1e-3)
T_DET = F_DET * DISC_R / 1000
T_LOAD = T_BED + T_AGIT + T_NOSE + T_BEAR + T_DET
T_NORMAL = DRIVE_T_MAX * DRIVE_I_NORMAL
for lbl, t in (("pellet-bed friction on the exposed disc face "
                f"(Janssen p_sat {P_SAT:.0f} Pa x {A_WIN:.0f} mm2 = "
                f"{N_BED:.1f} N, mu={MU})", T_BED),
               (f"agitator fingers ploughing the sump ({A_FIN:.0f} mm2 "
                f"frontal, passive x3)", T_AGIT),
               (f"wiper deflector nose ({A_NOSE:.0f} mm2 frontal)", T_NOSE),
               ("sleeve bearing + PTFE thrust washer", T_BEAR),
               (f"detent plunger release ({PLUNGER_F:.1f} N end force, "
                f"R{DIMPLE_SPH_R:.0f} x {DIMPLE_DEPTH:.1f} seat -> flank "
                f"{_beta:.1f} deg -> {F_DET:.2f} N at r{DISC_R:.0f})", T_DET)):
    print(f"  {t*1000:7.1f} mN*m  {lbl}")
print(f"  {T_LOAD*1000:7.1f} mN*m  TOTAL worst-case running load")
print(f"  DRIVE: 14HS13-0804S-PG5, {MOTOR_T_HOLD:.2f} N*m x {GEAR_RATIO} x "
      f"{GEAR_EFF} = {DRIVE_T_MAX:.2f} N*m available; normal metering at "
      f"{DRIVE_I_NORMAL*100:.0f}% current = {T_NORMAL:.2f} N*m "
      f"({T_NORMAL/T_LOAD:.1f}x the budget), recovery at 100% = "
      f"{DRIVE_T_MAX:.2f} N*m")
F_NORMAL = T_NORMAL / (PCD_R / 1000)
F_RECOV = DRIVE_T_MAX / (PCD_R / 1000)
print(f"  -> force at the pocket lip (r={PCD_R:.0f}): normal "
      f"{F_NORMAL:.1f} N ({PELLET_CRUSH_N/F_NORMAL:.1f}x UNDER the "
      f"{PELLET_CRUSH_N:.0f} N whole-pellet crush load -- a trapped whole "
      f"pellet stalls, it is never milled), recovery {F_RECOV:.1f} N "
      f"({F_RECOV/W_SHEAR:.1f}x OVER the {W_SHEAR:.1f} N worst wedged-sliver "
      f"shear force, still {PELLET_CRUSH_N/F_RECOV:.1f}x under whole-pellet "
      f"crush). r5 had 5.6 N and rebutted CONTEXT requirement 2; r6 meets it.")
print(f"  2. SHEAR BACKSTOP bound: at {F_RECOV:.1f} N the drive can shear any "
      f"proud section up to {F_RECOV/PELLET_STRENGTH_MPA:.0f} mm2 "
      f"(the whole pocket bore is {math.pi*POCKET_R**2:.0f} mm2, the worst "
      f"credible wedged sliver {max(a for _, a, _, _, _ in JAM):.0f} mm2)")
# r5 (granule-path MODERATE 1): this line used to claim "the deflector nose
# ramp lifts rather than stubs -- lift/push = cot(30) = 1.73", which
# contradicted the same file's own measured 27.5 deg / 1.92 AND the r4
# first-contact ray audit, which shows that a ROUNDED fragment (the credible
# shape) hits the nose's leading bottom corner at 1.500 mm with a normal
# exactly anti-travel, lift/push 0.00, for every size from Dia6 up. The ramp
# credit is DELETED. What carries the requirement is stated instead, with
# the numbers: the fragment is stubbed and returned to the OPEN sump (the
# nose sits inside the window, so there is somewhere for it to go), or it is
# crushed at a force the drive has.
print(f"  1. REJECTION BEFORE WEDGE (restated for a ROUNDED fragment; the "
      f"cot({NOSE_ANG:.0f}) = {1/math.tan(math.radians(NOSE_ANG)):.2f} ramp "
      f"credit is WITHDRAWN -- see B8.3b above: for every fragment class up to "
      f"Dia9 the swept-sphere first contact is the nose's leading bottom "
      f"corner at {NOSE_GAP:.3f} mm (a stacked Dia13 granule meets the rail "
      f"underside higher up instead), and the reaction normal has n_z <= 0 in "
      f"every case, so NOTHING is lifted over the nose): the nose STUBS the "
      f"fragment "
      f"and it is returned to the open {FILL_ARC[1] - FILL_ARC[0]:.0f} deg "
      f"sump window, or it yields. Crush force at the measured section x "
      f"{PELLET_STRENGTH_MPA:.2f} MPa [A, US4172714-derived; CLOSURE = IFDC "
      f"S-115]: "
      + ", ".join(f"Dia{_d:.1f} -> {math.pi * (_d / 2) ** 2:.2f} mm2 -> "
                  f"{math.pi * (_d / 2) ** 2 * PELLET_STRENGTH_MPA:.2f} N"
                  for _d in (5.0, 6.0, 7.0))
      + f", against {F_NORMAL:.1f} N at normal current and {F_RECOV:.1f} N in "
      f"recovery -- everything up to Dia7 yields inside the drive's "
      f"capability, and every one of these is far under the "
      f"{PELLET_CRUSH_N:.0f} N whole-granule crush load, so a whole granule "
      f"still STALLS rather than being milled. Behind the nose the "
      f"transfer-arc entry is a {RAMP_DEG:.0f} deg ramp at the PCD, not a "
      f"square edge, but that angle is radius-dependent (measured above).")
print("  3. DETECT + RECOVER: per-pocket Hall magnet (8) + index magnet -> "
      "phase is verified EVERY index, not just at boot (r5 Judge-1 item); "
      "StallGuard + gearbox current sensing; recovery = reverse-oscillate at "
      "normal current, then bounded shear attempts at 100% current with the "
      "chute beam armed, then fault. The count sensor is BELOW the meter, so "
      "a recovery cannot manufacture a phantom count.")

# detent geometry: park phase + dimple uniformity
print(f"dimple angles: {['%.1f' % a for a in dimple_angles]} (rev1: at the "
      f"POCKET angles), plunger at {PLUNGER_A:.1f} -> park phase "
      f"{PARK_PHI:.1f} deg, i.e. parked pockets sit 22.5 deg off the exit "
      f"port, unchanged from r6, and a pocket magnet sits under the "
      f"{HALL_INDEX_A:.1f} deg Hall at park (ECO-2, asserted)")
stock = Pos(0, 0, Z_DISC_TOP - DISC_T / 2) * Cylinder(DISC_R, DISC_T)
dvols = []
for a in dimple_angles:
    pr = Rot(Z=a) * (Pos(DISC_R - 0.5, 0, Z_DISC_TOP - DISC_T / 2) * Box(3.5, 4.5, 4.5))
    dvols.append(inter_vol(pr, stock) - inter_vol(pr, solids["pocket_disc"]))
print("dimple cavity volumes (mm3, uniform => radial axes ok): "
      + " ".join(f"{v:.2f}" for v in dvols)
      + f"   spread {max(dvols)-min(dvols):.2f}")

# park-position exit lens. r6 (pellet-path MODERATE: "the model's own probe
# uses an exit radius that is not in the part"): the retaining edge is the TOP
# of the port chamfer, so the lens is computed from PORT_RIM_R, re-measured on
# the exported plate, and the chamfer was cut 1.5 -> 0.75 to shrink it.
d_centers = 2 * PCD_R * math.sin(math.radians(22.5 / 2))
lens_w = (PORT_RIM_R + POCKET_R) - d_centers
print(f"PARK LENS: pocket at +/-22.5 deg vs the port RIM r{PORT_RIM_R:.2f} "
      f"(bore r{PORT_R:.1f} + {PORT_CHAMF:.2f} chamfer) -> centre distance "
      f"{d_centers:.2f} mm, lens {lens_w:.2f} mm (r5 quoted 4.01 using r9, "
      f"which is not the retaining edge; the r5 critic measured 5.51). "
      f"Pellets and fragments >= {lens_w:.2f} mm are RETAINED when parked; "
      f"smaller ones are an UNCOMMANDED RELEASE CLASS -- intrinsic (closing "
      f"it needs port_rim + pocket_r <= {d_centers:.2f} mm, i.e. a port "
      f"smaller than a pellet). Park retention margin vs the rim for "
      + ", ".join(f"D{d:.0f}: {(d_centers - (POCKET_R - d/2)) - PORT_RIM_R:+.2f} mm"
                  for d in (13.0, 12.0, 11.0)) + " (D11 = the bottom of the "
      "CONTEXT +/-1 mm band; the r5 critic measured -0.014 mm there and r6's "
      "smaller chamfer is what buys it back).")

# hall cavities vs exit port
exit_probe = Pos(PCD_R, 0, Z_RPLATE_TOP - PLATE_T / 2) * Cylinder(9.0, PLATE_T + 4)
for ha in (HALL_STATION_A, HALL_INDEX_A):
    hx = MAG_R_POS * math.cos(math.radians(ha))
    hy = MAG_R_POS * math.sin(math.radians(ha))
    hall_probe = Pos(hx, hy, Z_RPLATE_BOT + 1.25) * Box(5, 5, 2.5)
    d = math.hypot(hx - PCD_R, hy) - 9.0 - 2.5 * math.sqrt(2)
    print(f"hall cavity @{ha} deg vs exit hole: overlap "
          f"{inter_vol(hall_probe, exit_probe):.2f} mm3, planar margin ~{d:.1f} mm")

T_DROP = math.sqrt(2 * (DISC_T + UNDER_GAP) / 9810)      # s, pocket clear
_arc_in = 2 * math.degrees(math.acos(min(1.0, (d_centers ** 2 + 0) / 1)))  # unused
# ---- rev1 B7 RELEASE SWEEP (measured, replaces the r6/r7 CLAIM) --------
# Punch-list B7 and the r1 granule-path critic: "stationary release / zero
# lateral velocity / full Dia18 aperture" is geometrically FALSE, and RT-19
# says every such sentence has to be traceable to a passing check. It is
# measured here instead of asserted. Model: the seated pellet is a sphere of
# radius R resting on the retaining plate, its centre offset e from the
# pocket axis (the pocket bore is POCKET_R = 7.5, so |e| <= POCKET_R - R);
# support is lost when the sphere's plate contact point (directly under its
# centre) crosses the port RIM radius PORT_RIM_R.
#
# r4 CORRECTION (r3 granule-path MAJOR, "B7's shipped release numbers do not
# reproduce"): r9 applied the seat offset RADIALLY (centre = (PCD_R + e) at
# angle a), which barely changes the distance to the port axis and gave a
# release spread of 1.00 deg. The worst case is the offset lying ALONG THE
# CHORD from the pocket axis to the port axis -- a pellet resting on the
# leading wall of its pocket reaches the port earlier by exactly e. That is
# the construction the r3 critic used, and it is what is measured here: it
# reproduces 3.25..10.50 deg into the index (spread 7.25 deg overall,
# 3.75 deg at D13 alone) against r9's published 6.75..7.75 / 1.00 deg.
print("\nB7 RELEASE SWEEP (measured on the modelled port + pocket geometry; "
      "the r6/r7 'STATIONARY RELEASE / zero lateral velocity / full port "
      "aperture' claim is WITHDRAWN; r9's 1.00 deg spread is SUPERSEDED):")
_IDX = 22.5
_rel = []
for _D in (PELLET_D_MAX, PELLET_D, PELLET_D_MAX - 2.0):
    _R = _D / 2
    for _e in (POCKET_R - _R, 0.0, -(POCKET_R - _R)):
        _lost = None
        _a = _IDX
        while _a >= -0.0001:                     # 0.25 deg steps toward park
            # chord from the pocket axis (at _a) to the port axis (at 0)
            _s = 2 * PCD_R * math.sin(math.radians(_a) / 2)
            _d = _s - _e                         # contact point to port axis
            if _d <= PORT_RIM_R:
                _lost = (_a, _d)
                break
            _a -= 0.25
        _rel.append((_D, _e, _lost))
_ang = [r[2][0] for r in _rel if r[2]]
_sep = []
for (_D, _e, _l) in _rel:
    _R = _D / 2
    if _l is None:
        print(f"    D{_D:4.1f} seat {_e:+5.2f}: NEVER supported-to-park "
              f"(no release inside the index)")
        continue
    _a, _d = _l
    _th = math.radians(_a)
    _s = math.hypot(PCD_R * math.cos(_th) - PCD_R, PCD_R * math.sin(_th))
    _sep.append(_s)
    print(f"    D{_D:4.1f} seat {_e:+5.2f} mm: support lost at "
          f"{_IDX - _a:6.2f} deg into the {_IDX} deg index "
          f"({100*(_IDX-_a)/_IDX:4.1f} % of the move), pocket-axis-to-port "
          f"{_s:6.3f} mm, pellet-centre-to-port {_d:6.3f} mm "
          f"(B7.1 asks <= 1.0 mm)")
_d13 = [r[2][0] for r in _rel if r[2] and abs(r[0] - PELLET_D_MAX) < 1e-9]
print(f"  -> release window {_IDX - max(_ang):.2f}..{_IDX - min(_ang):.2f} deg "
      f"into the index; spread {max(_ang)-min(_ang):.2f} deg across D11..D13, "
      f"{max(_d13)-min(_d13):.2f} deg at D13 alone (r9 published 1.00 deg from "
      f"a radial-offset construction and the r3 critic measured 7.25/3.75 "
      f"independently -- these now agree). Separation at release "
      f"{min(_sep):.3f}..{max(_sep):.3f} mm. "
      f"B7.1 (support retained until |separation| <= 1.0 mm) FAILS: the "
      f"pellet leaves while the disc is still moving. Lateral velocity at "
      f"the PCD = omega x {PCD_R:.0f} mm = 0.126 m/s at the 225 deg/s mean "
      f"index rate and 0.25 m/s at a 450 deg/s peak [D, profile assumption "
      f"carried from r6, not re-derived]. THIS IS A RECORDED PLATEAU, not a "
      f"closure -- see BUILD-NOTES-r4 B7 and the corrected README/DESIGN "
      f"text. Park retention is unaffected and is re-printed above.")
print(f"\nEXIT KINEMATICS: the index is TWO-PHASE -- park(+22.5 deg) -> index "
      f"22.5 deg to the port -> DWELL -> index 22.5 deg to the next park. "
      f"(a) release happens {_IDX - max(_ang):.2f}..{_IDX - min(_ang):.2f} deg "
      f"INTO the first index, i.e. before the dwell begins, through a partial "
      f"lune -- NOT from a stationary, concentric pocket (measured above); "
      f"(b) the drop window is still a DWELL parameter, not a race -- fall "
      f"time to clear the {DISC_T + UNDER_GAP:.1f} mm pocket is "
      f"{T_DROP*1000:.0f} ms, so the contract dwell is 150 ms "
      f"({150/(T_DROP*1000):.1f}x); (c) the dwell is what guarantees the "
      f"pellet is clear of the disc before the second index, and that part of "
      f"the r6 argument survives.")
print(f"exit drop line: straight vertical at ({PCD_R:.0f}, 0) -> {PCD_R:.0f} mm "
      f"from the airframe centreline; chute bore Dia{CHUTE_ID:.0f} gives "
      f"{CHUTE_ID/2 - PELLET_D_MAX/2:.1f} mm of radial clearance around a "
      f"worst-case pellet")
v_beam = math.sqrt(2 * 9.81 * SENSOR_DROP / 1000)
print(f"IR beam at Z={Z_SENSOR:.1f} ({SENSOR_DROP:.0f} mm below plate); "
      f"v at beam = {v_beam:.2f} m/s; occlusion ~{(PELLET_D+3)/1000/v_beam*1000:.0f} ms "
      f"(12 mm pellet + 3 mm beam); sensor faces recessed 5.0 mm from bore")
print(f"chute ID {CHUTE_ID} < 2xD: two-body arch needs two pellets in the chute; "
      f"free-fall transit {math.sqrt(2*CHUTE_LEN/9810)*1000:.0f} ms << the "
      f"two-phase cycle -> temporally excluded (rebuttal held from r2)")
print("INTERFACE CONSTRAINT (r6, replaces r4's '>=150 ms index period'): the "
      "ICD command contract is INDEX 22.5 deg -> DWELL >= 150 ms -> INDEX "
      "22.5 deg -> park; one pellet per 45 deg, <= 3 pellets/s. The dwell is "
      "the only timing the count loop depends on and it is a firmware "
      "constant, not a kinematic race.")

# hopper usable volume: void from disc top (sump floor) to fill line 10 mm
# below the top plate, minus agitator + hub + brush intrusions
v_use = usable_void(FILL_LINE) / 1000.0  # cm3
cap_worst = int(v_use / PELLET_VOL_WORST)
cap_sphere = int(v_use / PELLET_VOL_SPHERE)
print(f"usable hopper volume (to fill line {FILL_LINE:.1f}): {v_use:.0f} cm3")
print(f"capacity: worst-case barrel packing {cap_worst} pellets "
      f"({cap_worst*PELLET_MASS:.0f} g); sphere basis {cap_sphere} "
      f"({cap_sphere*PELLET_MASS:.0f} g); requirement >=250 -> "
      f"{'PASS' if cap_worst >= 250 else 'FAIL'} ({cap_worst/250:.2f}x)")
for zl, tgt in ((Z_FILL_MAX, N_FILL_MAX), (Z_FILL250, 250)):
    vchk = usable_void(zl) / 1000.0
    print(f"{tgt}-pellet fill line (raised rib) at Z={zl:.1f} "
          f"({-(zl - Z_TOP_BOT):.1f} mm below the lid): volume below the line "
          f"{vchk:.0f} cm3 = {vchk / PELLET_VOL_WORST:.0f} pellets worst-case "
          f"(target {tgt}) / {vchk / PELLET_VOL_SPHERE:.0f} sphere-basis")
print(f"FILL-LINE RULE (r6): the MAX rib is the VOLUMETRIC brim line "
      f"({N_FILL_MAX} pellets, {N_FILL_MAX*PELLET_MASS:.0f} g). CONTEXT "
      f"exempts pellet mass above the 250 baseline from the 1.5 kg ceiling, "
      f"and the ceiling case is therefore the 250 load. For transparency the "
      f"NO-EXEMPTION limits are printed too: on the quadruple-conservative "
      f"ledger (CF-PETG {PESS_DENS*1000:.2f} g/cm3, stepper {PESS_MOTOR:.0f} g "
      f"gross, 100% infill, +10%) empty = {EMPTY_PESS:.1f} g -> only "
      f"{N_MASS_STRICT} pellets, which is BELOW the 250 hard minimum: that "
      f"reading is infeasible with a geared drive and r6 says so instead of "
      f"quietly moving a rib. On the measured-infill ledger the same strict "
      f"rule gives ~{int((1500.0 - (EMPTY_PESS - 167.5*1.10) - MASS_RESERVE)/PELLET_MASS)} "
      f"pellets. r5's rib was 393 on a 190 g direct drive.")
# r5: sump residual = what actually falls out when the cartridge is dropped
# after a drain-by-inversion (pellet-path MAJOR: "no isolation gate").
v_sump = usable_void(Z_FUN_BOT + PELLET_D_MAX) / 1000.0
print(f"SERVICE DRAIN: pellets below the funnel outlet + one pellet layer "
      f"(z<{Z_FUN_BOT + PELLET_D_MAX:.1f}) = {v_sump:.0f} cm3 = "
      f"~{v_sump/PELLET_VOL_WORST:.0f} pellets. That is the residue that can "
      f"fall when the cartridge is dropped AFTER the documented drain "
      f"(QR the payload, invert, remove the fill cap, pour back into the "
      f"tub) -- not the {N_FILL_MAX}-pellet load.")

# ---------------- PELLET TRANSIT PROBES (worst-case Dia13) -------------
# A worst-case pellet is swept through the whole path as a Dia13 sphere;
# every station must read 0 mm3 against EVERY part of the assembly.
# (r3 ran these in a separate probe pass; r4 folds them into the model.)
print("\nPELLET TRANSIT (Dia13 sphere vs all parts; every station must be 0):")


def at(x, y, z):
    return Pos(x, y, z) * Sphere(PELLET_D_MAX / 2)


def pol(r, a_deg, z):
    return at(r * math.cos(math.radians(a_deg)), r * math.sin(math.radians(a_deg)), z)


Z_SEAT = Z_RPLATE_TOP + PELLET_D_MAX / 2   # seated pellet rests on the plate
# funnel-wall contact point: a sphere tangent to a wall inclined A from
# horizontal sits R/sin(A) inside the wall radius [D]
_off = PELLET_D_MAX / 2 / math.sin(math.radians(FUNNEL_ANGLE))
z_fw = Z_FUN_BOT + 12.0
r_fw = (FUNNEL_RO + (z_fw - Z_FUN_BOT) / math.tan(math.radians(FUNNEL_ANGLE))) - _off

# Stations at a pocket angle are checked with the DISC (+ agitator, same
# shaft) INDEXED so a pocket really is under the probe -- otherwise the
# probe just reads the disc web, which is not a pellet-path finding.
def at_station(theta, z):
    rot = theta - 45.0 * round(theta / 45.0)
    moving = {"pocket_disc", "agitator"}
    sset = {k: (Rot(Z=rot) * copy.copy(v) if k in moving else v)
            for k, v in solids.items()}
    return pol(PCD_R, theta, z), sset


stations = [
    ("fill port (cap off)", at(FILL_POS[0], FILL_POS[1], Z_PLATE_BOT - 2.0),
     {"fill_cap"}),
    ("hopper cylinder mid", at(0.0, 30.0, Z_HOP_BOT + HOP_CYL_H / 2), set()),
    ("funnel wall tangent", pol(r_fw, 200.0, z_fw), set()),
    # the r4 skirt tabs bolt on OUTSIDE the funnel: prove they never
    # intrude into the pellet space at their own angles, high and low
    ("funnel wall @skirt 30", pol(r_fw, SKIRT_AS[0], z_fw), set()),
    ("funnel wall @skirt 105", pol(r_fw, SKIRT_AS[1], z_fw), set()),
    ("funnel wall @skirt 225", pol(r_fw, SKIRT_AS[2], z_fw), set()),
    # lowest station a pellet can reach on the funnel wall WITHOUT the roof
    # being under it; spans z -278.5..-265.5, i.e. straight through the
    # tab-root band and the tab/void crossover height (-272.45) [D]
    ("funnel wall @skirt 30, low",
     pol((FUNNEL_RO + 8.5 / math.tan(math.radians(FUNNEL_ANGLE))) - _off,
         SKIRT_AS[0], Z_FUN_BOT + 8.5), set()),
    # r5: the skirt tab top moved up with the steeper cone -- check the
    # pellet space right at the tab/void crossover height too
    ("funnel wall @skirt 105, tab top",
     pol((FUNNEL_RO + (SKIRT_Z1 - Z_FUN_BOT) / math.tan(math.radians(FUNNEL_ANGLE)))
         - _off, SKIRT_AS[1], SKIRT_Z1), set()),
    ("funnel outlet", pol(40.0, 190.0, Z_FUN_BOT + 3.0), set()),
    ("resting on disc, fill arc", pol(PCD_R, 190.0, Z_DISC_TOP + PELLET_D_MAX / 2),
     set()),
    # r5: the sump floor is a shelf (closed sector) -- a pellet resting on
    # it must clear the new bushing collar and the agitator flange
    ("resting on sump floor @60", pol(30.0, 60.0, Z_FUN_BOT + PELLET_D_MAX / 2),
     set()),
    ("resting on sump floor @300, inboard",
     pol(21.0, 300.0, Z_FUN_BOT + PELLET_D_MAX / 2), set()),
    ("in exit hole", at(PCD_R, 0.0, Z_RPLATE_TOP - PLATE_T / 2), set()),
    ("chute top", at(PCD_R, 0.0, Z_RPLATE_BOT - 8.0), set()),
    ("at IR beam", at(PCD_R, 0.0, Z_SENSOR), set()),
    ("chute exit", at(PCD_R, 0.0, Z_CHUTE_BOT + 4.0), set()),
    ("below aircraft", at(PCD_R, 0.0, Z_CHUTE_BOT - 15.0), set()),
]
worst_station = ("", 0.0)
for lbl, pr, skip in stations:
    _per = {k: inter_vol(pr, s) for k, s in solids.items() if k not in skip}
    v = sum(_per.values())
    if v > 0.05:
        lbl = lbl + " <- " + ",".join(f"{k}:{x:.2f}" for k, x in _per.items() if x > 0.01)
    if v > worst_station[1]:
        worst_station = (lbl, v)
    print(f"  {lbl:30s} {v:8.3f} mm3  {'OK' if v < 0.05 else '**BLOCKED**'}")
# indexed-disc stations (pocket really present under the probe)
for theta, lbl in ((180.0, "seated in pocket th=180"),
                   (BRUSH_A, "seated under brush th=133"),
                   (129.0, "seated at roof edge th=129"),
                   (90.0, "seated, transfer th=90"),
                   (45.0, "seated, transfer th=45"),
                   (0.0, "seated over exit port th=0")):
    pr, sset = at_station(theta, Z_SEAT)
    v = sum(inter_vol(pr, s) for s in sset.values())
    if v > worst_station[1]:
        worst_station = (lbl, v)
    print(f"  {lbl:30s} {v:8.3f} mm3  {'OK' if v < 0.05 else '**BLOCKED**'} "
          f"(disc indexed {theta - 45.0 * round(theta / 45.0):+.1f} deg)")
print(f"  worst station: {worst_station[0] or 'none'} {worst_station[1]:.3f} mm3")

# ---------------- r4: INSERTION / TOOL-PATH HARNESS --------------------
# r3 root cause: connectivity + interference checks could not see assembly-
# kinematics defects (sealed nut pockets, roofed screws, trapped brush).
# These probes measure the actual insertion and tool paths on the model.
print("\nINSERTION / TOOL-PATH CHECKS (r4 harness additions):")

# 1) mount screws: covered by the r6 INTERFACE BLOCK above.
# 2) skirt-tab screws: shank path + Dia8 driver envelope (radial, r56->r95)
#    + pilot thread stock
for a in SKIRT_AS:
    shank = Rot(Z=a) * (Pos(53.65, 0, SKIRT_SCREW_Z) * Rot(Y=90) * Cylinder(1.2, 3.0))
    drv = Rot(Z=a) * (Pos(75.5, 0, SKIRT_SCREW_Z) * Rot(Y=90) * Cylinder(4.0, 39.0))
    eng = Rot(Z=a) * (Pos(50.0, 0, SKIRT_SCREW_Z) * Rot(Y=90) * Cylinder(2.2, 4.0))
    v_sh = sum(inter_vol(shank, solids[n]) for n in ("hopper", "meter_housing"))
    v_dr = sum(inter_vol(drv, solids[n]) for n in solids)
    v_en = inter_vol(eng, solids["meter_housing"])
    print(f"  skirt screw @theta={a:5.1f}: shank path {v_sh:5.2f} mm3 (~0), driver "
          f"envelope {v_dr:5.2f} mm3 (~0; r3 BLOCKER: 44.2), pilot stock "
          f"{v_en:5.1f} mm3 (>0)")

# 3) wiper radial slide sweep (exact: holder + bristles are prismatic along
#    the slide direction, so a union of translated copies is the true sweep)
dirx, diry = math.cos(math.radians(BRUSH_A)), math.sin(math.radians(BRUSH_A))
sweep = copy.copy(solids["brush_holder"]) + copy.copy(solids["brush_bristles"])
for d in np.arange(2.0, 40.1, 2.0):
    sweep += Pos(d * dirx, d * diry, 0) * (copy.copy(solids["brush_holder"])
                                           + copy.copy(solids["brush_bristles"]))
print("  wiper slide sweep (0..40 mm radial retraction, 20 steps, holder+"
      "bristles) vs statics (~0 = OK):")
for other in ("meter_housing", "hopper", "pocket_disc", "agitator",
              "electronics_bay", "top_plate", "retaining_plate_chute",
              "sleeve_bearing"):
    print(f"    sweep x {other:22s} {inter_vol(sweep, solids[other]):9.2f}")

# 4) rev1 B2: D-BORE + GRUB CORRIDOR + DRIVER ACCESS
Z_SHAFT_TOP = Z_MOTOR_TOP + MOTOR_SHAFT_LEN
Z_SLEEVE_BOT = Z_FUN_BOT - BUSH_CB_DEPTH - BUSH_LEN
print("\n  B2 DISC->SHAFT TORQUE PATH (r6: a plain round bore on a D-cut "
      "shaft, and a grub pilot that dead-ended at r=10.60 in solid material):")
_disc_mesh = trimesh.load(os.path.join(EXPORT_DIR, f"pocket_disc_{REV}.stl"))
_zs_bore = np.linspace(Z_DCUT_BOT + 0.5, Z_BORE_TOP - 0.5, 12)
_flat_arc, _rr_all = [], []
for _z in _zs_bore:
    _row = []
    for _th in range(0, 360, 5):
        _t = math.radians(_th)
        _rr = 0.0
        for _r in np.arange(1.0, 4.0, 0.01):
            if not _disc_mesh.contains(np.array(
                    [[_r * math.cos(_t), _r * math.sin(_t), _z]]))[0]:
                _rr = _r
            else:
                break
        _row.append(_rr)
    _rr_all.append(_row)
_rr_all = np.array(_rr_all)
_flat_mask = _rr_all < 2.80
# The >=25 deg flat-arc requirement applies OUTSIDE the grub band: at heights
# within +/-GRUB_PILOT_R of the setscrew axis the Dia2.6 pilot occupies the
# middle of the flat BY DESIGN (close-out B2.2 -- the corridor must break
# through to the shaft there; its ~61 deg footprint at r=2.55 is wider than
# the 50 deg flat, so the flat reads 0 deg inside the band and that is the
# fixed geometry, not a regression).
_pilot_band = np.abs(_zs_bore - Z_SETSCREW) <= GRUB_PILOT_R + 0.05
_arc_deg = 5.0 * _flat_mask[~_pilot_band].sum(axis=1).min()
_arc_band = (5.0 * _flat_mask[_pilot_band].sum(axis=1).min()
             if _pilot_band.any() else float("nan"))
print(f"    bore radius swept at 5 deg x {len(_zs_bore)} heights over the "
      f"{Z_BORE_TOP - Z_DCUT_BOT:.1f} mm D-cut engagement: round part "
      f"{_rr_all[~_flat_mask].mean():.2f} +/- {_rr_all[~_flat_mask].std():.3f} mm, "
      f"FLAT part {_rr_all[_flat_mask].mean():.2f} +/- "
      f"{_rr_all[_flat_mask].std():.3f} mm over a contiguous {_arc_deg:.0f} deg "
      f"arc at every height OUTSIDE the grub band (need >=25 deg at "
      f"r=2.55+/-0.05; r6 measured r=3.06 at ALL angles and both heights); "
      f"inside the grub band (|z-{Z_SETSCREW:.2f}| <= {GRUB_PILOT_R:.2f}) the "
      f"flat reads {_arc_band:.0f} deg because the Dia{2*GRUB_PILOT_R:.1f} "
      f"pilot breaks through it to the shaft (close-out B2.2, by design)")
assert _arc_deg >= 25.0, "B2: flat arc lost outside the grub band"
_ray_blocked = []
# The ray MUST anchor at the bore FLAT (r = 2.55), not the round-bore radius:
# anchoring at 3.4 is how six rounds missed a 0.200 mm web sitting at
# r 2.55..2.75 (rev1 close-out B2.2 -- the independent verifier measured
# 1.0619 mm3 of disc material there while this check printed "NOWHERE").
for _r in np.arange(BORE_FLAT_R, DISC_R, 0.25):
    _p = Rot(Z=GRUB_A) * (Pos(_r, 0, Z_SETSCREW) * Sphere(0.35))
    if inter_vol(_p, solids["pocket_disc"]) > 1e-4:
        _ray_blocked.append(_r)
print(f"    grub corridor, Dia0.7 ray from the bore FLAT (r={BORE_FLAT_R:.2f}) "
      f"to the disc OD along theta={GRUB_A:.1f}: blocked at r = "
      f"{('%.2f..%.2f' % (min(_ray_blocked), max(_ray_blocked))) if _ray_blocked else 'NOWHERE -- continuous void'} "
      f"(r12 anchored this ray at 3.40 and missed the 2.55..2.75 web; r6: solid 10.60..24.47)")
_key = Rot(Z=GRUB_A) * (Pos(DISC_R + 20.0, 0, Z_SETSCREW) * Rot(Y=90)
                        * Cylinder((GRUB_KEY_AF + 0.4) / 2, 40.0))
_key_tab = {k: inter_vol(_key, s) for k, s in solids.items()
            if k != "pocket_disc" and not bb_disjoint(_key, s)}
print(f"    driver access, Dia{GRUB_KEY_AF + 0.4:.1f} x 40 mm key column on the "
      f"grub axis from r={DISC_R:.0f} outward vs every other solid: "
      + (", ".join(f"{k} {v:.3f}" for k, v in _key_tab.items()) if _key_tab
         else "no bbox-overlapping solid")
      + f" -> total {sum(_key_tab.values()):.3f} mm3 (the wall access port at "
      f"theta={GRUB_A:.1f} is what makes this 0)")
print(f"    grub axis z={Z_SETSCREW:.2f}; shaft top {Z_SHAFT_TOP:.1f}; screw "
      f"body {Z_SETSCREW - 1.5:.2f}..{Z_SETSCREW + 1.5:.2f} clears the bushing "
      f"sleeve bottom {Z_SLEEVE_BOT:.2f} by "
      f"{Z_SLEEVE_BOT - (Z_SETSCREW + 1.5):.2f} mm -> the Dia20 journal "
      f"surface is UNBROKEN")

# 5) bay lid: screw approach paths + rib-screw driver paths (to the head
#    INSIDE the bay at the rib inner wall)
v_lid = 0.0
for sx in (1, -1):
    for sz in (1, -1):
        pr = Pos(sx * BAY_SCREW_X, BAY_FLANGE_Y - 14.0,
                 ZC_BAY + sz * BAY_SCREW_Z) * Rot(X=90) * Cylinder(3.0, 25.0)
        v_lid += sum(inter_vol(pr, solids[n]) for n in solids
                     if n not in ("electronics_bay", "bay_lid"))
v_rib = 0.0
for sx in (1, -1):
    pr = Pos(sx * 14.0, (BAY_FLANGE_Y - 12.0 + BAY_Y_IN) / 2, RIB_ZC) * Rot(X=90) \
        * Cylinder(2.8, BAY_Y_IN - BAY_FLANGE_Y + 12.0)
    v_rib += sum(inter_vol(pr, solids[n]) for n in solids
                 if n not in ("electronics_bay", "bay_lid"))
print(f"  bay lid (B5.6): 4x Dia6 x 25 mm driver columns total {v_lid:.2f} mm3 "
      f"vs every OTHER solid (~0); 2x rib driver paths through the lid's Dia6 "
      f"holes total {v_rib:.2f} mm3 (~0)")
_lidsw = None
for _dy in np.linspace(0.0, -20.0, 11):
    _s = Pos(0, _dy, 0) * copy.copy(solids["bay_lid"])
    _lidsw = _s if _lidsw is None else _lidsw + _s
print(f"  bay lid REMOVAL sweep (20 mm outboard, 11 steps) vs every other "
      f"solid: {sum(inter_vol(_lidsw, s) for k, s in solids.items() if k != 'bay_lid'):.2f} mm3")

# 6) r5 CARTRIDGE DROP-OUT SWEEP -- the r4 BLOCKER, measured properly.
# r4 "verified" this with a Dia26.4 cylinder probe through the roof hole and
# missed that the agitator's own fingers blocked the descent (853 mm3). r5
# sweeps EVERY cartridge member (quarter-turn unlock 22 deg, then a 20-step
# 60 mm descent) against EVERY static part, exactly as the critic did.
CART = ["retaining_plate_chute", "pocket_disc", "stepper", "thrust_washer"]
CART_UNLOCK = -22.0        # r3: latch handedness mirrored (A-7)
STATIC = [n for n in solids if n not in CART]
print("  CARTRIDGE DROP-OUT SWEEP (unlock -22 deg + 60 mm descent, 21 steps, "
      "4 members x every static part, bbox-prefiltered; r3 REVERSED the latch "
      "handedness, so the unlock rotation is now -22, not +22):")
cart_tab = {}
tot_cart = 0.0
first_block = None
for dz in np.linspace(0.0, -60.0, 21):
    for n in CART:
        s = Pos(0, 0, dz) * Rot(Z=CART_UNLOCK) * copy.copy(solids[n])
        for other in STATIC:
            # the agitator is a free rotor keyed to the hub hex: the unlock
            # rotation turns it too, so it is compared in its turned pose
            o = (Rot(Z=CART_UNLOCK) * copy.copy(solids[other])
                 if other == "agitator" else solids[other])
            if bb_disjoint(s, o, margin=0.0):
                continue
            v = inter_vol(s, o)
            if v > 0.02:
                cart_tab[(n, other)] = cart_tab.get((n, other), 0.0) + v
                tot_cart += v
                if v > 0.5 and first_block is None:
                    first_block = (dz, n, other, v)
for (n, other), v in sorted(cart_tab.items(), key=lambda kv: -kv[1]):
    print(f"    {n:22s} x {other:20s} {v:9.2f} mm3 summed over the descent")
print(f"    TOTAL {tot_cart:.2f} mm3, first blocking step: {first_block} "
      f"(r4 measured 860.07 mm3 here, 853 of it the agitator -> the "
      f"documented service path did not exist)")
# and the agitator must STAY: lift it 30 mm and show it clears the funnel
ag_up = None
for dz in np.linspace(0.0, 30.0, 16):
    s = Pos(0, 0, dz) * copy.copy(solids["agitator"])
    ag_up = s if ag_up is None else ag_up + s
print(f"  agitator removal (lift 30 mm up into the funnel, 16 steps) vs hopper "
      f"{inter_vol(ag_up, solids['hopper']):.2f} / housing "
      f"{inter_vol(ag_up, solids['meter_housing']):.2f} mm3 -- it comes off the "
      f"hex upward with the hopper removed (bench item, not a field item)")
# 7) r5 JAM ACCESS with the cartridge removed: straight rods from below to
# the wiper station and the roof entry edge (r4 pellet-path MAJOR: "the
# highest-probability jam site is unreachable by any straight field tool")
STATIC_NOCART = [solids[n] for n in STATIC]
for th, lbl in ((BRUSH_A, "wiper plane 133"), (FILL_ARC[0], "roof edge 129"),
                (180.0, "fill arc 180")):
    for dia in (8.0, 12.0):
        rod = Rot(Z=th) * (Pos(PCD_R, 0, (Z_DISC_TOP + 1.0 + Z_CHUTE_BOT - 40) / 2)
                           * Cylinder(dia / 2, (Z_DISC_TOP + 1.0) - (Z_CHUTE_BOT - 40)))
        v = sum(inter_vol(rod, s) for s in STATIC_NOCART)
        print(f"  jam access, cartridge OUT: Dia{dia:.0f} rod from below to the "
              f"{lbl:16s} {v:8.2f} mm3 (~0 = reachable)")

# ---------------- ALL-PAIRS interference (ShapeList-safe) --------------
names = list(parts.keys())
print(f"\nALL-PAIRS interference ({len(names)*(len(names)-1)//2} pairs, "
      "bbox-prefiltered, ShapeList-safe; >0.5 mm3 flagged):")
n_bad = n_nan = n_checked = 0
worst_pair = ("", 0.0)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = names[i], names[j]
        if bb_disjoint(solids[a], solids[b]):
            continue
        v = inter_vol(solids[a], solids[b])
        n_checked += 1
        if math.isnan(v):
            n_nan += 1
            print(f"  {a:24s} x {b:24s}   CHECK-FAILED (boolean exception)")
        elif v > 0.5:
            n_bad += 1
            if v > worst_pair[1]:
                worst_pair = (f"{a} x {b}", v)
            print(f"  {a:24s} x {b:24s} {v:9.1f}  **COLLISION**")
        else:
            print(f"  {a:24s} x {b:24s} {v:9.2f}  OK")
print(f"  summary: {n_checked} bbox-overlapping pairs boolean-checked, "
      f"{n_bad} collisions, {n_nan} check-failures")

# fill cap: locked AND inserted orientations must both be clear
cap_ins = Pos(*FILL_POS, 0) * Rot(Z=90) * Pos(-FILL_POS[0], -FILL_POS[1], 0) * copy.copy(solids["fill_cap"])
print(f"fill cap vs top plate: locked {inter_vol(solids['fill_cap'], solids['top_plate']):.2f} mm3, "
      f"inserted(+90deg) {inter_vol(cap_ins, solids['top_plate']):.2f} mm3 (both must be ~0)")

# latch swing path: each lug sweeps entry->lock inside its slots
print("latch-lug swing sweep (r52..55.3, th a-5.3..a+27.3, z inset 0.05) vs "
      "housing / bay (must be ~0):")
for a in LUG_ANGLES:
    sw = sector(52.0, 55.3, a - 27.3, a + 5.3, Z_RPLATE_BOT + 0.05, PLATE_T - 0.1)
    print(f"  lug@{a:5.1f}: x housing {inter_vol(sw, solids['meter_housing']):8.2f}  "
          f"x bay {inter_vol(sw, solids['electronics_bay']):8.2f}")
chute_or_chk = CHUTE_ID / 2 + CHUTE_WALL
print(f"cartridge rotation ({CART_UNLOCK:.0f} deg): chute/boss cluster max r "
      f"{math.hypot(PCD_R + 6, 23.0):.1f} mm < ring bore r{RING_RI} -> inserts/rotates clear")

# rotating agitator swept annulus vs statics (exact: revolve the modeled
# rotor rather than an assumed envelope)
ag_bb = solids["agitator"].bounding_box()
swept = Pos(0, 0, (ag_bb.min.Z + ag_bb.max.Z) / 2) * (
    Cylinder(AGIT_FINGER_RO + 0.2, ag_bb.max.Z - ag_bb.min.Z)
    - Cylinder(HEX_AF / 2 - 0.4, ag_bb.max.Z - ag_bb.min.Z + 2))
print(f"agitator swept annulus (r<={AGIT_FINGER_RO + 0.2}, z {ag_bb.min.Z:.2f}.."
      f"{ag_bb.max.Z:.2f}) vs statics (~0 = OK):")
for other in ("brush_holder", "brush_bristles", "hopper", "meter_housing",
              "top_plate", "sleeve_bearing"):
    print(f"  swept x {other:18s} {inter_vol(swept, solids[other]):9.2f}")
_foot = None
for r in np.arange(CHAMBER_R + 3.0, 40.0, -0.1):
    if inter_vol(Pos(r, 0, Z_FUN_BOT + 0.6) * Sphere(0.25), solids["hopper"]) < 1e-5:
        _foot = r
        break
print(f"  sump-floor film under the fingers "
      f"{ag_bb.min.Z - Z_FUN_BOT + 0.2:.2f} mm; the bed's outer boundary at "
      f"the sump-floor plane is the hopper CONE FOOT, measured at "
      f"r{_foot:.2f} (r5 claimed the chamber wall r{CHAMBER_R:.0f} and the "
      f"critic corrected it) -> unswept ring r{AGIT_FINGER_RO}..{_foot:.2f} = "
      f"{math.pi*(_foot**2 - AGIT_FINGER_RO**2):.0f} mm2 "
      f"({_foot - AGIT_FINGER_RO:.2f} mm wide; r5 claimed 147, the critic "
      f"measured 343)")

# motor <-> chute lateral clearance (the tight spot)
chute_inner_x = PCD_R - chute_or_chk
print(f"\nmotor face x={MOTOR_W/2:.1f} vs chute outer wall x={chute_inner_x:.1f} -> "
      f"clearance {chute_inner_x - MOTOR_W/2:.1f} mm (14HS13-0804S flat face; "
      "leads clocked -X)")

# ---- rev1 r3: FILL-CAP EXTRACTION, MEASURED (assembly A-5 / integration
# B12-a). The r8 build printed a NARRATIVE here ("the cap lifts and swings
# OUTBOARD, away from the neck") and never booleaned it; two critics then
# measured 0.65 mm of free lift against a 6.45 mm requirement, i.e. the cap
# could not be removed OR fitted. Every number below is a boolean.
CAP_STATIC = ("top_plate", "hopper", "clip_plate", "blindmate_pcb")


def _cap_at(deg, lift=0.0, dy=0.0):
    return Pos(0, dy, lift) * (Pos(*FILL_POS, 0) * Rot(Z=deg)
                               * Pos(-FILL_POS[0], -FILL_POS[1], 0)
                               * copy.copy(solids["fill_cap"]))


def _cap_obst(sol):
    return sum(inter_vol(sol, solids[k]) for k in CAP_STATIC)


_cap_bb = solids["fill_cap"].bounding_box()
CAP_LIFT_REQ = Z_TOP_TOP - _cap_bb.min.Z
print(f"\nFILL-CAP EXTRACTION (B12.2 / A-5), measured on the model, not "
      f"narrated:")
print(f"  cap spans Z {_cap_bb.min.Z:.3f}..{_cap_bb.max.Z:.3f}; lift to clear "
      f"the plate top face ({Z_TOP_TOP:.2f}) = {CAP_LIFT_REQ:.3f} mm "
      f"(r8: 6.45 mm required against 0.65 mm available)")
print(f"  cap near edge y={FILL_POS[1] - CAP_RECESS_R:.2f} (recess) / "
      f"{FILL_POS[1] - CAP_FLANGE_R:.2f} (flange) vs the neck's relieved +Y "
      f"face y={NECK_YP0:.2f} over Z {Z_TOP_TOP:.2f}..{NECK_FLARE_Z:.2f} "
      f"-> {FILL_POS[1] - CAP_RECESS_R - NECK_YP0:.2f} mm of plan land, and "
      f"{NECK_YP_H:.1f} mm of relieved height for a {CAP_LIFT_REQ:.2f} mm lift")
_leg1 = None
for _d in np.linspace(0.0, 90.0, 19):
    _p = _cap_at(_d)
    _leg1 = _p if _leg1 is None else _leg1 + _p
_det_v = _cap_obst(_cap_at(5.0))
print(f"  LEG 1 turn to unlock, swept union 0..90 deg at the seat: "
      f"{_cap_obst(_leg1):.4f} mm3, ALL of it the N5 detent tab riding the "
      f"recess wall ({_det_v:.4f} mm3 at every angle off the dimple; the "
      f"tab is a modelled cantilever spring, deflection "
      f"{CAP_DET_PROUD:.2f} mm)")
_leg2 = None
for _L in np.linspace(0.0, 12.0, 25):
    _p = _cap_at(90.0, _L)
    _leg2 = _p if _leg2 is None else _leg2 + _p
print(f"  LEG 2 axial lift 0..12 mm at the unlock angle, swept union: "
      f"{_cap_obst(_leg2) - _det_v:.4f} mm3 above the detent term "
      f"({_cap_obst(_leg2):.4f} total)")
for _L in (2.0, 4.0, 6.0, 8.0, 10.0, 12.0):
    print(f"     lift {_L:5.1f} mm -> {_cap_obst(_cap_at(90.0, _L)):9.4f} mm3")
_leg3 = None
for _dy in np.linspace(0.0, 45.0, 16):
    _p = _cap_at(90.0, 8.0, _dy)
    _leg3 = _p if _leg3 is None else _leg3 + _p
print(f"  LEG 3 lateral +Y 0..45 mm at lift 8.0: {_cap_obst(_leg3):.4f} mm3")
print(f"  -> the shipped extraction is: turn 90 deg, lift {CAP_LIFT_REQ:.1f} mm, "
      f"lift again/withdraw +Y. No leg needs the cap to pass under the neck.")
# B5-b: the gland is a closed 360 deg loop and nothing vents the tank
_bad_gland = []
for _i in range(720):
    _th = _i * 0.5
    _x = FILL_POS[0] + CAP_SEAL_R * math.cos(math.radians(_th))
    _y = FILL_POS[1] + CAP_SEAL_R * math.sin(math.radians(_th))
    if inter_vol(Pos(_x, _y, CAP_RECESS_FLOOR - CAP_SEAL_D - 0.25) * Sphere(0.2),
                 solids["top_plate"]) < 1e-6:
        _bad_gland.append(_th)
print(f"  B5-b FACE GLAND: {CAP_SEAL_W:.1f} x {CAP_SEAL_D:.1f} mm groove at "
      f"r={CAP_SEAL_R:.1f}, centreline perimeter "
      f"{2 * math.pi * CAP_SEAL_R:.2f} mm; 720-point scan of the material "
      f"UNDER the groove floor -> "
      f"{'sectors with no backing: ' + str(_bad_gland) if _bad_gland else 'CLOSED 360.0 deg, no interruption'} "
      f"(r8: 42.0 deg of the sealing bore did not exist -- two through-notches)")
print(f"     seal stack: cord 1.5, gland depth {CAP_SEAL_D:.1f}, flange rides "
      f"{CAP_SEAL_GAP:.1f} proud -> compressed {CAP_SEAL_D + CAP_SEAL_GAP:.1f} "
      f"= {(1.5 - CAP_SEAL_D - CAP_SEAL_GAP) / 1.5 * 100:.0f}% squeeze [D]")
_open_cols = 0
for (_px, _py) in ((0, 0), (0, 8), (0, 14), (0, 18), (0, 20), (0, 22), (5, 20),
                   (-5, 20), (10, 10), (0, -10), (12, 18), (-12, 18)):
    _col = Pos(_px, _py, (Z_TOP_BOT + Z_PLATE_BOT) / 2) * Cylinder(
        0.6, Z_PLATE_BOT - Z_TOP_BOT)
    if inter_vol(_col, solids["top_plate"]) < 0.02 * math.pi * 0.36 * (
            Z_PLATE_BOT - Z_TOP_BOT):
        _open_cols += 1
print(f"  B5-b tank -> NECK CAVITY: {_open_cols} of 12 Dia1.2 columns from "
      f"inside the tank to the clip-plate underside are open (must be 0; r8's "
      f"-Y bayonet notch vented the tank straight into the harness neck).")
print("     ^ THIS CHECK IS NOT SUFFICIENT AND IS KEPT ONLY AS HISTORY: 12 "
      "hand-placed columns cannot certify a ~15 000 mm2 lid, and it printed "
      "'0 of 12 open' for nine rounds while 22.00 mm2 of the lid was missing "
      "(granule-path MODERATE 1). The grid scan below is the real test.")

# ---- r6 (granule-path MODERATE 1 / N14): TANK ROOF, GRID SCAN ---------
# Upward rays from just under the lid, on a 0.5 mm plan grid over the whole
# barrel bore, against hopper + top_plate + fill_cap with the CAP FITTED.
# A failing part looks like r2..r11 did: two 2.2 x 5.0 mm rectangles of open
# cells at (+/-9.0, -66.0), i.e. 22.00 mm2 with a Dia2.200 pass-through, at
# plan radius 66.61 mm which is INSIDE the barrel bore.
_roofm = trimesh.util.concatenate([
    trimesh.load(os.path.join(EXPORT_DIR, f"{_p}_{REV}.stl"))
    for _p in ("hopper", "top_plate", "fill_cap")])
_ROOF_STEP = 0.5
_BARREL_RI = HOP_RI - 0.5               # 69.5, inside the measured bore 69.978
Z_SCAN_ROOF = Z_TOP_BOT - 1.0           # -239.55, just under the lid
_gg = np.arange(-_BARREL_RI, _BARREL_RI + 1e-9, _ROOF_STEP)
_GX, _GY = np.meshgrid(_gg, _gg)
_msk = (_GX ** 2 + _GY ** 2) <= _BARREL_RI ** 2
_pts = np.column_stack([_GX[_msk], _GY[_msk]])
_org = np.column_stack([_pts, np.full(len(_pts), Z_SCAN_ROOF)])
_dirs = np.tile(np.array([[0.0, 0.0, 1.0]]), (len(_org), 1))
_hit = _roofm.ray.intersects_any(_org, _dirs)
_openpts = _pts[~_hit]
_openA = len(_openpts) * _ROOF_STEP ** 2
print(f"  r6 TANK-ROOF GRID SCAN: {len(_pts)} upward rays at "
      f"{_ROOF_STEP:.2f} mm over the barrel bore r <= {_BARREL_RI:.3f} from "
      f"z = {Z_SCAN_ROOF:.1f} vs hopper+top_plate+fill_cap (cap FITTED): "
      f"{len(_openpts)} open cells = {_openA:.2f} mm2 of UNROOFED granule bed")
# Split by radius from the FILL axis: anything inside the O-ring gland has
# nothing sealing it and must be zero; the cap-to-recess running clearance
# OUTSIDE the gland is a designed removable joint whose seal is the modelled
# gland + the BOM'd 1.5 mm nitrile cord (a cord is not modelled as a solid,
# so those rays get through the CAD and not through the machine).
_rf = np.hypot(_openpts[:, 0] - FILL_POS[0],
               _openpts[:, 1] - FILL_POS[1]) if len(_openpts) else np.zeros(0)
_inA = float((_rf <= CAP_SEAL_R).sum()) * _ROOF_STEP ** 2
_outA = _openA - _inA
print(f"     INSIDE the fill-cap O-ring gland (r <= {CAP_SEAL_R:.1f} from the "
      f"fill axis, nothing seals it): {_inA:.2f} mm2   <- must be 0.00")
print(f"     OUTSIDE it (cap flange r{CAP_FLANGE_R:.1f} in the r"
      f"{CAP_RECESS_R:.1f} recess = the designed running clearance, sealed by "
      f"the {CAP_SEAL_W:.1f} x {CAP_SEAL_D:.1f} mm gland + the 1.5 mm nitrile "
      f"cord, which is a BOM line and not a modelled solid): {_outA:.2f} mm2")
if len(_openpts):
    print("     open-cell bbox: x "
          f"{_openpts[:, 0].min():.2f}..{_openpts[:, 0].max():.2f}  y "
          f"{_openpts[:, 1].min():.2f}..{_openpts[:, 1].max():.2f}; radius "
          f"from the fill axis {_rf.min():.2f}..{_rf.max():.2f} mm")
print("     (a failing part looks like r2..r11: 438 open cells / 27.38 mm2, "
      "including two 2.2 x 5.0 mm rectangles at (+/-9, -66) at plan radius "
      "66.61 mm, and 13 cells at r 9.0..11.0 from the fill axis where the "
      "lanyard hole went through the cap)")
assert _inA <= 0.30, (
    f"r6: {_inA:.2f} mm2 of the granule bed is open to the sky inside the "
    f"fill-cap seal")
print(f"  N5 bayonet engagement: plate lugs r {LUG_RI:.1f}..{FILL_R:.1f} = "
      f"{FILL_R - LUG_RI:.2f} mm radial x {LUG_W:.1f} mm x2 = "
      f"{2 * (FILL_R - LUG_RI) * LUG_W:.1f} mm2 of retaining face; groove play "
      f"{CAP_GRV_H - LUG_T:.2f} mm")

# =====================================================================
# rev1 ROUND-3 CHECKS -- one block per round-2 critic BLOCKING finding.
# Every line is a boolean or a scan on the modelled solids; verify_r3.py
# re-measures the same claims on the EXPORTED files without reading this file.
# =====================================================================
print("\n============ REV-1 r3: ROUND-2 BLOCKING FINDINGS ============")

# --- A-7: the drive's reaction path ---------------------------------
print("A-7 CARTRIDGE FREE ROTATION (r8: hard stop in -theta only, 24.65 deg "
      "free in +theta = the direction the stator reaction pushes, ending in "
      "the drop-out window):")
_rot_tab = []
for _d in range(-32, 15):
    _v = sum(inter_vol(Rot(Z=float(_d)) * copy.copy(solids[n]),
                       solids["meter_housing"]) for n in CART[:1] + ["stepper"])
    _rot_tab.append((_d, _v))
_free = [d for d, v in _rot_tab if v < 0.5]
print(f"  free band WITHOUT the lock pin: {min(_free):+.0f} .. {max(_free):+.0f} deg "
      f"(1 deg steps, exact booleans vs meter_housing)")
for _d in (min(_free) - 2, min(_free) - 1, min(_free), 0, max(_free),
           max(_free) + 1, max(_free) + 2):
    _v = dict(_rot_tab).get(_d)
    if _v is not None:
        print(f"     {_d:+3d} deg -> {_v:9.3f} mm3")
_pin = Rot(Z=LOCK_PIN_A) * (Pos(LOCK_PIN_TIP + LOCK_PIN_LEN / 2, 0, LOCK_PIN_Z)
                            * Rot(Y=90) * Cylinder(1.5, LOCK_PIN_LEN))
print(f"  M3x{LOCK_PIN_LEN:.0f} STOP PIN at theta={LOCK_PIN_A:.1f} "
      f"(r {LOCK_PIN_TIP:.1f}..{LOCK_PIN_TIP + LOCK_PIN_LEN:.1f}): "
      f"^ retaining_plate {inter_vol(_pin, solids['retaining_plate_chute']):.4f} "
      f"mm3 seated, ^ meter_housing {inter_vol(_pin, solids['meter_housing']):.4f} "
      f"mm3 (= the thread-forming interference in the Dia2.6 pilot)")
_pin_stop = None
for _d in (0, -1, -2, -3, -5):
    _v = inter_vol(Rot(Z=float(_d)) * copy.copy(solids["retaining_plate_chute"]), _pin)
    print(f"     back-rotation {_d:+3d} deg -> lug ^ pin {_v:8.3f} mm3")
    if _v > 0.5 and _pin_stop is None:
        _pin_stop = _d
print(f"  -> two-sided band WITH the pin fitted: {_pin_stop + 1:+.0f} .. "
      f"{max(_free):+.0f} deg. Drive torque {DRIVE_T_MAX:.4f} N*m reacts on "
      f"the +theta shelf faces: 3 lugs x {(55.55 - 52.05) * PLATE_T:.1f} mm2 = "
      f"{3 * (55.55 - 52.05) * PLATE_T:.1f} mm2 at r=53.55 -> "
      f"{DRIVE_T_MAX / 0.05355:.1f} N -> "
      f"{DRIVE_T_MAX / 0.05355 / (3 * (55.55 - 52.05) * PLATE_T):.3f} MPa on "
      f"CF-PETG (r8 relied on {0.068:.3f} N*m of lug friction: a 9.6x deficit)")
_drv_pin = Rot(Z=LOCK_PIN_A) * (Pos(75.0, 0, LOCK_PIN_Z) * Rot(Y=90)
                                * Cylinder(4.0, 30.0))
print(f"  pin driver access, Dia8 x 30 mm radial from r=60: "
      f"{sum(inter_vol(_drv_pin, s) for s in solids.values()):.4f} mm3")

# --- count-sensor BLOCKING: the emitter and the receiver now have volume --
print("\nCOUNT-SENSOR: the DATASHEET optoelectronics fit (r9 was built against "
      "a 5.8 mm TSAL6200 that came from a critique, not a drawing; the "
      "datasheet part is 8.7 +/- 0.3 mm and buried 11.2532 mm3 per LED in the "
      "r9 plate):")
print(f"  aperture plane |y|={SENS_CAV_Y0:.1f}; board inner face "
      f"|y|={SENS_BOARD_Y0:.1f}; outer face |y|={SENS_BOARD_Y1:.1f}; cavity "
      f"floor |y|={SENS_BOSS_Y1:.1f} -> component height "
      f"{SENS_BOARD_Y0 - SENS_CAV_Y0:.2f} mm, post length "
      f"{SENS_BOSS_Y1 - SENS_BOARD_Y1:.2f} mm")
print(f"  sensor_boards (2x PCB + 2x TSAL6200 + 2x VBPW34FAS, modelled "
      f"envelopes) ^ retaining_plate_chute = "
      f"{inter_vol(aux_solids['sensor_boards'], solids['retaining_plate_chute']):.4f} mm3")
print(f"  sensor_boards ^ sensor_cover = "
      f"{inter_vol(aux_solids['sensor_boards'], aux_solids['sensor_cover']):.4f} mm3")
print(f"  sensor_boards ^ count_windows = "
      f"{inter_vol(aux_solids['sensor_boards'], aux_solids['count_windows']):.4f} mm3")
# r4: the acceptance test the r3 critic wrote -- the DATASHEET package solid,
# at nominal AND at the max-material limit, on both sides, vs plate and cover.
for _hh, _lbl in ((LED_H_NOM, "nominal 8.7"), (LED_H_MAX, "max 9.0")):
    _vp = _vc = 0.0
    for _sy in (1, -1):
        for (_dx, _dz) in zip(SENS_DEV_X, SENS_DEV_Z):
            _led = led_solid(_dx, _dz, _sy, _hh)
            _vp += inter_vol(_led, solids["retaining_plate_chute"])
            _vc += inter_vol(_led, aux_solids["sensor_cover"])
    print(f"  TSAL6200 max-material envelope ({_lbl} mm, Dia5.8x0.7 flange + "
          f"Dia5.0 barrel run FLAT to the apex, which contains the R2.49 "
          f"dome), 4 placements: ^ plate = {_vp:.4f} mm3, "
          f"^ cover = {_vc:.4f} mm3  (r9 at 8.7: 11.2532 per LED)")
_vpd = sum(inter_vol(pd_solid(_dx, _dz, -1), solids["retaining_plate_chute"])
           for (_dx, _dz) in zip(SENS_DEV_X, SENS_DEV_Z))
print(f"  VBPW34FAS datasheet solid ({PD_L}x{PD_W}x{PD_H} SMD), both "
      f"placements: ^ plate = {_vpd:.4f} mm3")
print(f"  LED tip |y| = {SENS_BOARD_Y0 - LED_H_MAX:.2f} at the 9.0 mm "
      f"worst case vs the cavity floor {SENS_CAV_Y0:.2f} -> "
      f"{SENS_BOARD_Y0 - LED_H_MAX - SENS_CAV_Y0:.2f} mm of air "
      f"({SENS_BOARD_Y0 - LED_H_NOM - SENS_CAV_Y0:.2f} mm at nominal). The "
      f"Dia5.0 barrel cannot enter the Dia3.2 aperture, so this clearance is "
      f"what the fit depends on.")
_OPT_PATH = (SENS_BOARD_Y0 - LED_H_NOM) + (SENS_BOARD_Y0 - PD_H)
print(f"  optical path, emitter tip |y|={SENS_BOARD_Y0 - LED_H_NOM:.1f} to PD "
      f"face |y|={SENS_BOARD_Y0 - PD_H:.1f} = {_OPT_PATH:.1f} mm "
      f"(r9 geometry: 38-40 mm). ELECTRONICS 4.4 computes 182x excess gain "
      f"over a 32 mm path; inverse-square at {_OPT_PATH:.1f} mm gives "
      f"{182 * (32.0 / _OPT_PATH) ** 2:.0f}x. Still a large dust margin, but "
      f"4.4's headline is {(_OPT_PATH / 32.0) ** 2:.2f}x optimistic against "
      f"the geometry that exists -- carried as an open ELECTRONICS edit, not "
      f"silently kept.")
print(f"  NB-1 BOARD LOCATION: cavity {SENS_CAV[0]:.3f} (x) x {SENS_CAV[2]:.3f} "
      f"(z) around an 18.000 x 12.000 board = +/-{(SENS_CAV[0]-18)/2:.3f} / "
      f"+/-{(SENS_CAV[2]-12)/2:.3f} mm of float in r9. The cover now carries 4 "
      f"locating ribs {SENS_RIB_T:.1f} mm thick at x +/-{SENS_RIB_X:.1f}, "
      f"z +/-{SENS_RIB_Z:.1f}, {SENS_RIB_D:.1f} mm deep -> board float "
      f"+/-{SENS_RIB_X - SENS_RIB_T/2 - 9.0:.3f} mm in x and "
      f"+/-{SENS_RIB_Z - SENS_RIB_T/2 - 6.0:.3f} mm in z, with "
      f"{10.2 - SENS_RIB_X - SENS_RIB_T/2:.3f} mm of rib-to-cavity clearance; "
      f"lateral capture over the board edge = "
      f"{SENS_RIB_D - (SENS_BOSS_Y1 - SENS_BOARD_Y1):.3f} mm")
print(f"  NB-4 DATUMS PUBLISHED: the devices sit on the LABYRINTH mouths "
      f"x = {SENS_DEV_X[0]:.3f} / {SENS_DEV_X[1]:.3f} (not the ECO-3 aperture "
      f"axes 29/35), z = {SENS_DEV_Z[0]:.3f} / {SENS_DEV_Z[1]:.3f}, board "
      f"centre x = {SENS_BOARD_XC:.3f}; pitch 6.000 x 6.000 mm unchanged")

# --- A-6: the sensor cover can be installed -------------------------
print("\nA-6 SENSOR-COVER INSERTION (r8: 488.4789 mm3 swept, no clear "
      "direction; the harness duct stood 0.50 mm outboard of the cover):")
_cov_bodies = aux_solids["sensor_cover"].solids()
for _cb in _cov_bodies:
    _bb = _cb.bounding_box()
    _side = "+Y" if _bb.min.Y > 0 else "-Y"
    _vec = (0.0, -1.0, 0.0) if _side == "+Y" else (0.0, 1.0, 0.0)
    _sw = None
    for _t in np.linspace(0.0, 30.0, 16):
        _p = Pos(-_vec[0] * _t, -_vec[1] * _t, 0) * copy.copy(_cb)
        _sw = _p if _sw is None else _sw + _p
    _v = (inter_vol(_sw, solids["retaining_plate_chute"])
          + inter_vol(_sw, solids["stepper"])
          + inter_vol(_sw, aux_solids["count_windows"]))
    print(f"  cover {_side}: radial swept union over 30 mm (16 stations) vs "
          f"plate+stepper+windows = {_v:.4f} mm3; seated "
          f"{inter_vol(_cb, solids['retaining_plate_chute']):.4f} mm3")
print(f"  harness material outboard of the cover face |y|={SENS_BOSS_Y1 + COVER_T:.1f} "
      f"in the cover's own x/z envelope: the duct's lowest run is at "
      f"z={DUCT_LOW_Z:.2f} (crown {DUCT_LOW_Z + DUCT_RO:.2f}), "
      f"{abs(DUCT_LOW_Z + DUCT_RO - (Z_SENSOR - SENS_SCREW_DZ - SENS_EAR_H / 2)):.2f} mm "
      f"below the cover's bottom face")

# --- B5-a / B5.1: the board fits AND can be got in ------------------
print("\nB5-a ELECTRONICS BAY (r8: 42.0000 mm clear aperture for a 42.0 mm "
      "board = 0.0000 mm of clearance):")


def _aperture(axis):
    _a, _b = 1.0, 60.0
    for _ in range(40):
        _m = (_a + _b) / 2
        _box = (Pos(0, BAY_FLANGE_Y + 3.0, ZC_BAY) * Box(_m, 10.0, 20.0)
                if axis == "x" else
                Pos(0, BAY_FLANGE_Y + 3.0, ZC_BAY) * Box(20.0, 10.0, _m))
        if inter_vol(_box, solids["electronics_bay"]) > 1e-6:
            _b = _m
        else:
            _a = _m
    return _a


_apw, _aph = _aperture("x"), _aperture("z")
print(f"  clear aperture {_apw:.4f} (w) x {_aph:.4f} (h) mm -> a "
      f"{BOARD_X:.1f} x {BOARD_Z:.1f} board passes with "
      f"{_apw - BOARD_X:.4f} / {_aph - BOARD_Z:.4f} mm of clearance")
_board = Pos(0, BOARD_Y0 - BOARD_ENV_Y / 2, ZC_BAY) * Box(
    BOARD_X, BOARD_ENV_Y, BOARD_Z)
print(f"  {BOARD_X:.0f} x {BOARD_Z:.0f} x {BOARD_ENV_Y:.0f} board seated on the "
      f"ECO-7 standoffs ^ bay = {inter_vol(_board, solids['electronics_bay']):.4f} mm3")
for _lbl, _vec in (("+x", (1, 0, 0)), ("-x", (-1, 0, 0)), ("+z", (0, 0, 1)),
                   ("-z", (0, 0, -1)), ("-y (outboard)", (0, -1, 0))):
    _gap = 0.0
    for _t in np.arange(0.0, 6.05, 0.1):
        if inter_vol(Pos(_vec[0] * _t, _vec[1] * _t, _vec[2] * _t) * copy.copy(_board),
                     solids["electronics_bay"]) > 1e-6:
            break
        _gap = _t
    print(f"     board clearance {_lbl:14s} {_gap:4.1f} mm (B5.1 asks >= 1.5)")
_bins = None
for _t in np.linspace(0.0, 30.0, 16):
    _p = Pos(0, -_t, 0) * copy.copy(_board)
    _bins = _p if _bins is None else _bins + _p
print(f"  board insertion sweep through the aperture (-Y, 30 mm): "
      f"{inter_vol(_bins, solids['electronics_bay']):.4f} mm3")

# --- r6 (integration BLOCKING I-1): CARTRIDGE-DUCT PATENCY -----------
# Coverage and patency are DIFFERENT questions and r11 only asked the first:
# a solid rod is 100 % laterally enclosed. This block asks the second, on the
# EXPORTED mesh, per leg, and it is the check that would have failed r11.
# A failing part looks like r11 did: 63/63, 187/187, 261/261, 205/205,
# 109/109, 197/197, 43/43 axis points INSIDE printed material, and a Dia1.0
# cylinder scoring 100 % of its own volume against the plate.
print("\nI-1 CARTRIDGE-DUCT PATENCY (bay -> motor, bay -> both count boards). "
      "r11: every leg 100.0 % SOLID on its own axis; largest conductor Dia0.0")
_rpm = trimesh.load(os.path.join(EXPORT_DIR,
                                 f"retaining_plate_chute_{REV}.stl"))
_rps = solids["retaining_plate_chute"]
_tot_in, _tot_pts, _worst = 0, 0, 0.0
for (_nm, _p0, _p1) in DUCT_LEGS:
    _p0a, _p1a = np.array(_p0, float), np.array(_p1, float)
    _L = float(np.linalg.norm(_p1a - _p0a))
    _n = max(int(_L / 0.25) + 1, 2)
    _ts = np.linspace(0.02, 0.98, _n)          # skip the exact end faces
    _pp = _p0a + np.outer(_ts, _p1a - _p0a)
    _ins = int(_rpm.contains(_pp).sum())
    _tot_in += _ins
    _tot_pts += len(_pp)
    # Dia4.0 bundle swept down the leg axis, exact OCC boolean vs the plate
    _d = _p1a - _p0a
    _ax = _d / _L
    _rotb = Rot(Y=90) if abs(_ax[0]) > 0.5 else (
        Rot(X=90) if abs(_ax[1]) > 0.5 else Rot(Z=0.0))
    _cyl = Pos(*(0.5 * (_p0a + _p1a))) * _rotb * Cylinder(2.0, _L - 0.5)
    _iv = inter_vol(_cyl, _rps)
    _worst = max(_worst, _iv)
    print(f"    {_nm:<28s} L {_L:6.2f} mm | axis points inside material "
          f"{_ins:4d}/{len(_pp):4d} ({100.0*_ins/len(_pp):5.1f} %) | "
          f"Dia4.0 bundle ^ plate = {_iv:9.4f} mm3")
print(f"    TOTAL {_tot_in}/{_tot_pts} axis points inside material; worst "
      f"Dia4.0 bundle intersection {_worst:.4f} mm3")
print(f"    duct-bore material actually removed by cut_each = "
      f"{DUCT_BORE_CUT:.4f} mm3 = {DUCT_BORE_CUT*DENS['petg_cf']:.2f} g of "
      f"CF-PETG at 100 % infill (r11 removed 0.0000)")
assert _tot_in == 0 and _worst < 1e-6, "I-1: the cartridge duct is not patent"

# --- B5-c: harness coverage, MEASURED ON THE EXPORTED SOLIDS ---------
# r5 (integration BLOCKING FAIL): this table used to be a parameter roll-up
# -- a list of segment lengths with a hand-typed COVERED/exposed flag. It
# printed "COVERED 18.00 mm top-plate elbow -> hopper conduit ... 95.3 %"
# while the elbow was SOLID PRINTED MATERIAL and no conductor of any diameter
# could cross it. A roll-up cannot see that, so it is replaced: the route is
# now a POLYLINE of 3-D points, and both patency and coverage are measured on
# the exported meshes by ray-casting.
print("\nB5-c HARNESS ROUTE, MEASURED ON THE EXPORTS (r10 shipped a PARAMETER "
      "roll-up that read 95.3 % covered while the elbow was solid; this block "
      "reads the meshes):")
_ROUTE = []                       # (name, [pts], covered_expected)


def _arc_pts(cy, cz, rr, a0, a1, n=16):
    return [(0.0, cy - rr * math.cos(math.radians(a)),
             cz + rr * math.sin(math.radians(a)))
            for a in np.linspace(a0, a1, n + 1)]


_ROUTE.append(("neck cavity (blind-mate PCB -> neck base)",
               [(0.0, -8.0, Z_PLATE_BOT - 3.0),
                (0.0, -8.0, CONDUIT_ZC)], True))
_ROUTE.append(("neck -Y wall exit slot -> top-plate conduit",
               [(0.0, -8.0, CONDUIT_ZC), (0.0, -19.0, CONDUIT_ZC)], True))
_ROUTE.append(("top-plate conduit, neck wall -> elbow tangent",
               [(0.0, -19.0, CONDUIT_ZC), (0.0, _ec_y, CONDUIT_ZC)], True))
_ROUTE.append(("top-plate ELBOW (R%.1f quarter turn)" % ELB_R,
               _arc_pts(_ec_y, _ec_z, ELB_R, 90.0, 0.0), True))
_ROUTE.append(("vertical spigot -> hopper conduit -> bay riser",
               [(0.0, CONDUIT_Y, _ec_z), (0.0, CONDUIT_Y, BAY_RISER_Z0)], True))
_ROUTE.append(("bay -> cartridge duct SERVICE LOOP (must flex: the cartridge "
               "drops out)",
               [(10.0, BAY_Y_IN, RIB_ZC - BAY_H / 2 + 4.0),
                (10.0, DUCT_END_Y, DUCT_Z)], False))
_ROUTE.append(("cartridge duct, bay end -> x=0 collector",
               [(0.0, DUCT_END_Y, DUCT_Z), (0.0, -DUCT_LEG_Y, DUCT_Z)], True))
_ROUTE.append(("motor branch, collector -> motor rear plane",
               [(0.0, MOT_BR_Y, DUCT_Z), (0.0, MOT_BR_Y, MOT_BR_Z)], True))
_ROUTE.append(("motor branch, inboard to the lead socket",
               [(0.0, MOT_BR_Y, MOT_BR_Z), (0.0, MOT_SOCK_Y, MOT_BR_Z)], True))
_ROUTE.append(("motor flying leads, socket -> can face",
               [(0.0, MOT_SOCK_Y, MOT_BR_Z),
                (0.0, -MOTOR_W / 2, MOT_BR_Z)], False))
for _sy in (1, -1):
    _tag = "+Y" if _sy > 0 else "-Y"
    _ROUTE.append((f"sensor duct {_tag}: collector -> vertical leg",
                   [(DUCT_LEG_X, _sy * DUCT_LEG_Y, DUCT_Z),
                    (DUCT_LEG_X, _sy * DUCT_LEG_Y, DUCT_LOW_Z)], True))
    _ROUTE.append((f"sensor duct {_tag}: low run in X",
                   [(DUCT_LEG_X, _sy * DUCT_LEG_Y, DUCT_LOW_Z),
                    (SENS_PORT_X, _sy * DUCT_LEG_Y, DUCT_LOW_Z)], True))
    _ROUTE.append((f"sensor duct {_tag}: low run in Y -> ear bottom",
                   [(SENS_PORT_X, _sy * DUCT_LEG_Y, DUCT_LOW_Z),
                    (SENS_PORT_X, _sy * SENS_PORT_Y, DUCT_LOW_Z)], True))
    _ROUTE.append((f"sensor riser {_tag} inside the boss",
                   [(SENS_PORT_X, _sy * SENS_PORT_Y, DUCT_LOW_Z),
                    (SENS_PORT_X, _sy * SENS_PORT_Y, SENS_EAR_Z0)], True))

# one mesh of every FLIGHT printed part, straight off disc
_FLIGHT_STL = [n for n in parts
               if os.path.exists(os.path.join(EXPORT_DIR, f"{n}_{REV}.stl"))]
_allm = trimesh.util.concatenate(
    [trimesh.load(os.path.join(EXPORT_DIR, f"{n}_{REV}.stl"))
     for n in _FLIGHT_STL])
print(f"     mesh under test: {len(_FLIGHT_STL)} exported part STLs "
      f"({', '.join(sorted(_FLIGHT_STL))}), {len(_allm.faces)} faces")
# COVERED = laterally ENCLOSED: all 8 rays perpendicular to the run hit
# printed material. A free-air leg fails it (measured: the bay->cartridge
# service loop reads 3/8, the motor flying leads 7/8), a conduit passes it
# (8/8). The enclosure DISTANCE is printed too, so "covered" cannot mean
# "there is a wall somewhere in the same county".
COVER_RAY_MAX = 1e9
COVER_MIN_HITS = 8


def _covered_pt(p, d):
    """8 perpendicular rays from p -> (hits, worst enclosing distance mm)."""
    d = np.array(d, dtype=float)          # COPY: np.asarray would alias the
    d = d / max(np.linalg.norm(d), 1e-9)  # caller's direction and /= in place
    _u = np.cross(d, [0, 0, 1.0])
    if np.linalg.norm(_u) < 1e-6:
        _u = np.cross(d, [1.0, 0, 0])
    _u /= np.linalg.norm(_u)
    _v = np.cross(d, _u)
    dirs, origins = [], []
    for _k in range(8):
        _a = math.radians(45.0 * _k)
        dirs.append(math.cos(_a) * _u + math.sin(_a) * _v)
        origins.append(p)
    loc, idx_ray, _ = _allm.ray.intersects_location(
        ray_origins=np.array(origins), ray_directions=np.array(dirs))
    hits, worst = 0, 0.0
    for _k in range(8):
        _sel = loc[idx_ray == _k]
        if len(_sel):
            _dm = float(np.min(np.linalg.norm(_sel - np.array(p), axis=1)))
            if _dm <= COVER_RAY_MAX:
                hits += 1
                worst = max(worst, _dm)
    return hits, worst


_cov = _unc = 0.0
_unc_where = []
for _name, _pts, _exp in _ROUTE:
    _L = _lc = 0.0
    _encl = 0.0
    for _i in range(len(_pts) - 1):
        _p0, _p1 = np.array(_pts[_i], float), np.array(_pts[_i + 1], float)
        _d = _p1 - _p0
        _seg = float(np.linalg.norm(_d))
        _n = max(2, int(round(_seg)))
        for _j in range(_n):
            _t0, _t1 = _j / _n, (_j + 1) / _n
            _mid = _p0 + _d * (_t0 + _t1) / 2
            _dl = _seg / _n
            _L += _dl
            _h, _w = _covered_pt(tuple(_mid), _d)
            if _h >= COVER_MIN_HITS:
                _lc += _dl
                _encl = max(_encl, _w)
    _cov += _lc
    _unc += _L - _lc
    if _L - _lc > 0.5:
        _unc_where.append((_name, _L - _lc))
    print(f"     {_lc / _L * 100:5.1f} % covered  {_L:7.2f} mm  (worst "
          f"enclosing wall {_encl:5.2f} mm)  {_name}"
          + ("" if (_lc / _L > 0.9) == _exp else "   <- NOT as the route "
             "description assumes"))
print(f"  total modelled harness run {_cov + _unc:.2f} mm; MEASURED covered "
      f"{_cov:.2f} mm = {_cov / (_cov + _unc) * 100:.1f} % (B5.5 asks >= 90 %); "
      f"uncovered {_unc:.2f} mm")
for _n, _u in _unc_where:
    print(f"     uncovered {_u:6.2f} mm at: {_n}")
_mot_socket = Pos(*MOTOR_LEAD_SOCKET) * Sphere(1.0)
print(f"  motor lead socket at {MOTOR_LEAD_SOCKET} -> gap to the motor can "
      f"face (|y|={MOTOR_W / 2:.1f}) = {abs(MOT_SOCK_Y) - MOTOR_W / 2:.2f} mm "
      f"[A: NEMA-14 leads exit the can; CLOSURE = the delivered motor]")
_pel = [("hopper", solids["hopper"]), ("top_plate", solids["top_plate"])]
_duct_all = _duct
print(f"  B5.4 the cartridge duct never enters the granule space: duct solid "
      f"^ hopper {inter_vol(_duct_all, solids['hopper']):.4f}, ^ meter_housing "
      f"{inter_vol(_duct_all, solids['meter_housing']):.4f}, ^ pocket_disc "
      f"{inter_vol(_duct_all, solids['pocket_disc']):.4f} mm3")

# --- NB-1 / NB-2 / NB-4 from the round-2 critics ---------------------
print("\nROUND-2 NON-BLOCKING items closed by geometry:")
print(f"  NB-1 chute_plug ^ count_windows = "
      f"{inter_vol(aux_solids['chute_plug'], aux_solids['count_windows']):.4f} mm3 "
      f"(r8: 0.5981 mm3 on each beam-B window); plug land now z "
      f"{PLUG_LAND_Z0:.2f}..{PLUG_LAND_Z0 + PLUG_LAND_H:.2f} = "
      f"{PLUG_LAND_H:.1f} mm ABOVE the windows (top window edge "
      f"{-389.30:.2f}), shank relieved to Dia{2 * PLUG_SHANK_R:.1f}; "
      f"^ retaining_plate {inter_vol(aux_solids['chute_plug'], solids['retaining_plate_chute']):.4f} "
      f"mm3 = the designed 0.3 mm press fit")
_ribdrv = 0.0
for _sx in (1, -1):
    _pr = Pos(_sx * 14.0, (BAY_FLANGE_Y - 12.0 + BAY_Y_IN) / 2, RIB_ZC) * Rot(
        X=90) * Cylinder(2.8, BAY_Y_IN - BAY_FLANGE_Y + 12.0)
    _ribdrv += sum(inter_vol(_pr, solids[n]) for n in solids
                   if n != "electronics_bay")
print(f"  NB-2 bay-lid rib-driver corridor INCLUDING the lid itself: "
      f"{_ribdrv:.4f} mm3 (r8: 0.7069 mm3 of the lid's own register lip -- the "
      f"r8 check excluded bay_lid from its own corridor test)")
print(f"  NB-1(assembly) shaft-end clearance: bore blind face "
      f"Z={Z_BORE_TOP:.3f}, shaft top Z={Z_MOTOR_TOP + MOTOR_SHAFT_LEN:.3f} -> "
      f"{Z_BORE_TOP - (Z_MOTOR_TOP + MOTOR_SHAFT_LEN):.3f} mm (r8: 0.000, so "
      f"the shaft, not the PTFE washer, set the disc height)")
_lowest = min((s.bounding_box().min.Z, k) for k, s in solids.items())
print(f"  NB-4(assembly)/B12.1 the LOWEST FLIGHT SOLID is {_lowest[1]} at "
      f"Z={_lowest[0]:.3f}; service-stand ground plane Z={STAND_GROUND_Z:.2f} "
      f"-> clearance {_lowest[0] - STAND_GROUND_Z:.3f} mm (BUILD-NOTES-r2 "
      f"printed 16.20 mm by measuring the retaining plate, not the motor)")

# ---- r5: WALL THICKNESS by inward ray-cast (buildability MODERATE:
# "undisclosed sub-2 mm structural sections ... the builder's harness never
# measured it"). Same method the critic used: sample surface points, cast
# along -normal, take the distance to the next surface.
print("\nWALL THICKNESS (inward ray-cast on the exported STLs, mm):")
rng = np.random.default_rng(7)
WALL = {}
for pname in PRINTED:
    m = trimesh.load(os.path.join(EXPORT_DIR, f"{pname}_{REV}.stl"))
    pts, fidx = trimesh.sample.sample_surface(m, 6000, seed=7)
    nrm = m.face_normals[fidx]
    org = pts - nrm * 1e-3
    loc, ray_i, tri_i = m.ray.intersects_location(org, -nrm, multiple_hits=False)
    if len(loc) == 0:
        continue
    d = np.linalg.norm(loc - org[ray_i], axis=1)
    # drop GRAZING hits (ray nearly parallel to the far face): those measure
    # chamfer/edge slivers, not wall sections, and are what produces the
    # 0.03 mm "min wall" artifacts
    keep = np.abs((m.face_normals[tri_i] * -nrm[ray_i]).sum(1)) > 0.5
    d = d[keep]
    WALL[pname] = (d.min(), np.percentile(d, 1), np.percentile(d, 5),
                   100.0 * (d < 1.95).mean())
    if pname == "brush_holder":
        zk = pts[ray_i][keep][:, 2]
        thin = d < 1.0
        band = np.abs(zk[thin] - (Z_DISC_TOP + NOSE_GAP)) < 2.0
        _WH_TIP = 100.0 * band.mean() if thin.sum() else 0.0
        _WH_THIN = 100.0 * thin.mean()
    print(f"  {pname:22s} min {d.min():5.2f}  p1 {np.percentile(d,1):5.2f}  "
          f"p5 {np.percentile(d,5):5.2f}   {100*(d<1.95).mean():5.1f}% of sampled "
          f"area under 1.95 mm  ({100*(~keep).mean():.0f}% grazing rays dropped)")
    if pname == "brush_holder":
        print(f"      -> {_WH_THIN:.1f}% of samples read under 1.0 mm and "
              f"{_WH_TIP:.0f}% of THOSE lie within 2 mm of the deflector tip "
              f"plane z={Z_DISC_TOP + NOSE_GAP:.1f}: they are the 30 deg WEDGE "
              f"(blunted to a 0.6 mm tip face), not a wall. The rail section "
              f"is {HOLD_W:.0f} x {HOLD_H:.0f} mm and the thinnest real wall is "
              f"the bristle-channel outer web at 0.9 mm (stress-checked above).")
# the specific r4 findings, re-measured as targeted sections
rp_mesh = trimesh.load(os.path.join(EXPORT_DIR, f"retaining_plate_chute_{REV}.stl"))
web_min = 9e9
for th in (160, 200, 260, 300, 330):
    ok_r = []
    for r in np.arange(39.0, 48.0, 0.1):
        p = np.array([[r * math.cos(math.radians(th)), r * math.sin(math.radians(th)),
                       Z_RPLATE_TOP - PLATE_T / 2]])
        if rp_mesh.contains(p)[0]:
            ok_r.append(r)
    if ok_r:
        runs, start = [], ok_r[0]
        for a, b in zip(ok_r, ok_r[1:]):
            if b - a > 0.15:
                runs.append((start, a))
                start = b
        runs.append((start, ok_r[-1]))
        widest = max(w[1] - w[0] for w in runs)
        web_min = min(web_min, widest)
        print(f"  plate radial web @theta={th}: solid runs "
              f"{[f'{a:.1f}-{b:.1f}' for a, b in runs]} -> widest "
              f"{widest:.2f} mm")
print(f"  -> min radial web between the inner slots and the rim slots "
      f"{web_min:.2f} mm (r4 critic measured 1.0 mm over ~176 deg)")

# ---- r5: SUMP APERTURE, measured (pellet-path MAJOR: concept 3 claims a
# "~95 mm orifice"; the r4 critic measured 27.0 mm and demanded the number
# be struck). Measure it again here so the doc cannot drift.
z_ap = Z_FUN_BOT - 1.0
open_r = []
for r in np.arange(8.0, 52.0, 0.25):
    p = Pos(r * math.cos(math.radians(190)), r * math.sin(math.radians(190)),
            z_ap) * Sphere(0.2)
    if inter_vol(p, solids["meter_housing"]) < 1e-4:
        open_r.append(r)
runs, start = [], open_r[0]           # contiguous open runs, not min..max
for a, b in zip(open_r, open_r[1:]):
    if b - a > 0.3:
        runs.append((start, a))
        start = b
runs.append((start, open_r[-1]))
ap_lo, ap_hi = [rr for rr in runs if rr[0] <= PCD_R <= rr[1]][0]
print(f"\nSUMP APERTURE (measured at theta=190, z={z_ap:.1f}): open radial runs "
      f"{[f'{a:.2f}-{b:.2f}' for a, b in runs]}; the pellet window (the run "
      f"containing the PCD) is r{ap_lo:.2f}..{ap_hi:.2f} = {ap_hi - ap_lo:.2f} mm x "
      f"{FILL_ARC[1] - FILL_ARC[0]:.1f} deg annular window; equivalent "
      f"circular orifice D{2*math.sqrt((ap_hi**2 - ap_lo**2)*(FILL_ARC[1]-FILL_ARC[0])/360):.1f}. "
      f"That is {(ap_hi - ap_lo)/PELLET_D_MAX:.2f}x the worst-case pellet -- "
      f"CONCEPT-pocket-wheel 3's '~95 mm orifice' is WRONG and is struck in "
      f"BUILD-NOTES-r5; the anti-bridging defence is the agitator, not the "
      f"aperture size.")

# ---- r5: BEARING checks (buildability GAP "no bearings anywhere")
jrnl_len = (Z_FUN_BOT - BUSH_CB_DEPTH) - (Z_FUN_BOT - BUSH_CB_DEPTH - BUSH_LEN)
side_load = 3.0    # N, pellet-bed drag on the disc [J]
print(f"\nBEARING: iglidur-class flanged sleeve ID{BUSH_ID}/OD{BUSH_OD}, flange "
      f"Dia{BUSH_FL_OD}, journal length {jrnl_len:.1f} mm at z "
      f"{Z_FUN_BOT - BUSH_CB_DEPTH - BUSH_LEN:.2f}..{Z_FUN_BOT - BUSH_CB_DEPTH:.2f}; "
      f"seat probe (bushing vs housing counterbore) "
      f"{inter_vol(solids['sleeve_bearing'], solids['meter_housing']):.2f} mm3, "
      f"hub-in-bore radial clearance {BUSH_ID/2 - HUB_R:.2f} mm modeled. "
      f"[D] p = {side_load:.0f} N / ({BUSH_ID:.0f} x {jrnl_len:.0f}) = "
      f"{side_load/(BUSH_ID*jrnl_len):.4f} MPa vs iglidur J ~35 MPa static -> "
      f"{35/(side_load/(BUSH_ID*jrnl_len)):.0f}x margin; L/D = "
      f"{jrnl_len/BUSH_ID:.2f} is short, so it constrains disc TILT and takes "
      f"the bed load off the stepper bearings rather than acting as a "
      f"precision journal (stated, not hidden).")
print(f"  agitator self-capture: it is held by gravity alone, so inverting the "
      f"payload for the service drain drops it off the hex. It cannot leave "
      f"the hopper (OD {2*AGIT_FINGER_RO:.0f} vs the Dia46 fill port) and the "
      f"funnel outlet r{FUNNEL_RO} limits its radial float to "
      f"{FUNNEL_RO - AGIT_FINGER_RO:.1f} mm, so on re-righting it lands "
      f"concentric within {FUNNEL_RO - AGIT_FINGER_RO:.1f} mm and drops onto "
      f"the hex within 30 deg of hand rotation (45 deg lead-in chamfer "
      f"modeled on the spigot top).")
print(f"  agitator thrust face: rides on the bushing flange standing "
      f"{BUSH_FL_T - BUSH_CB_DEPTH:.2f} mm proud of the sump floor "
      f"(iglidur-on-TPU, not PETG-on-TPU); hex drive engagement "
      f"{(Z_JOURNAL_TOP + HEX_LEN) - (AG_Z0 - 0.05):.2f} mm, "
      f"{HEX_AF} mm across flats, 0.4 mm AF clearance")

# modeled fastening summary (every joint fastenable AND tool-reachable)
print("\nMODELED FASTENING (r5):")
print(f"  clip->top_plate: 4x {MOUNT_SCREW} SHCS from the drone side, through "
      f"the MAPPED vendor holes at (+/-{BOLT_DX:.0f},+/-{BOLT_DY:.0f}) "
      f"(dia {MOUNT_HOLE_D:.2f}), heads in the plate's own dia "
      f"{MOUNT_POCKET_D:.2f} pockets, into {MOUNT_SCREW} heat-set inserts in "
      f"the top plate (r5 bolted into a through-window: BLOCKING)")
print("  blind-mate PCB: 4x M2 into the CLIP PLATE's own tabs at "
      "(+/-4,+/-10); the payload only provides the sealed well + cable route")
print(f"  top_plate->hopper: 6x M3 at r{FLANGE_SCREW_R} into Dia4 heat-set "
      f"inserts in the hopper flange (both hole sets modeled)")
print(f"  hopper->housing: 3x RADIAL M3 plastite through skirt tabs at theta "
      f"{SKIRT_AS}, z={SKIRT_SCREW_Z:.1f}, into Dia2.5x4.4 wall pilots -- "
      f"driver comes in horizontally from outside")
print(f"  bay->housing: 2x {BAY_SCREW} through rib+inner wall into Dia2.5x7 "
      f"wall pilots; driver access via Dia6 holes in the BAY LID")

# ---- r4 (assembly A-9): FASTENER GRIP / ENGAGEMENT, MEASURED ----------
# "the electronics bay's only two fasteners are 7.0 mm too short to reach the
# housing": M3x12 gave 0.000 mm of thread engagement, tip 1.920 mm short of
# the housing. Grip and engagement are measured on the exported meshes here
# (off-axis rays, so the pilot bore does not hide the wall), and the BOM
# length is derived from the measurement instead of being asserted.
# ---- r4 (assembly NB-8): the three PROCEDURE FACTS the drive depends on ---
# "none of the three procedure facts is written down anywhere" -- they are
# measured and printed here so the build notes can quote them.
print("\nSERVICE PROCEDURE FACTS (measured, not narrated -- assembly NB-8):")
_f1 = {}
for _dia in (1.5, 3.4, 6.0, 8.0):
    _v = 0.0
    for (_bx, _by) in ((MOTOR_BC_R, 0), (-MOTOR_BC_R, 0), (0, MOTOR_BC_R),
                       (0, -MOTOR_BC_R)):
        _col = Pos(_bx, _by, Z_RPLATE_TOP + 12.5) * Cylinder(_dia / 2, 25.0)
        _v += sum(inter_vol(_col, s) for k, s in solids.items()
                  if k not in ("retaining_plate_chute", "stepper"))
    _f1[_dia] = _v
_f1_ok = [d for d, v in _f1.items() if v < 1e-3]
print(f"  1. MOTOR IS NOT FIELD-REPLACEABLE IN PLACE. Driver columns on the "
      f"4 gearbox screws (r={MOTOR_BC_R:.0f} bolt circle), +Z, 25 mm, vs "
      f"every OTHER assembled solid: "
      + ", ".join(f"Dia{d:.1f} -> {v:.4f} mm3" for d, v in _f1.items())
      + f" -> largest clear driver in situ = "
      f"{('Dia%.1f' % max(_f1_ok)) if _f1_ok else 'Dia0.0'}. The motor is "
      f"fastened and removed ONLY as the plate+motor cartridge (that is what "
      f"the quarter-turn latch is for).")
print(f"  2. THE DISC MUST BE INDEXED TO theta = {GRUB_A:.1f} deg before the "
      f"grub can be fitted: the disc's grub pilot, the housing access port "
      f"and the shaft flat only line up there (the continuous "
      f"Dia{2*GRUB_PILOT_R:.1f} void measured above is measured at that "
      f"clocking). The grub must be pushed "
      f"{HOUSING_R - GRUB_PILOT_R * 0 - 9.0:.2f} mm radially down the "
      f"Dia{2*GRUB_CLEAR_R:.1f} channel; there is no retrieval path if it is "
      f"dropped in the chamber.")
print(f"  2b. THE 4 x RX-M2x4 MOUNT INSERTS GO IN FROM THE UNDERSIDE of "
      f"top_plate, while it is still a loose part (assembly r4 NB-1: "
      f"'a perfectly buildable sequence -- it is just not written anywhere'). "
      f"Measured at ({BOLT_DX:.0f}, {BOLT_DY:.0f}): Dia2.500 lead from the "
      f"top face z={Z_PLATE_BOT:.3f} down to {NECK_CAP_BOT:.3f}, then the "
      f"Dia{MOUNT_INSERT_D:.3f} x {MOUNT_INSERT_L:.3f} mm insert bore, then a "
      f"Dia4.800 relief shaft. A Dia3.2 insert cannot pass the Dia2.5 lead, "
      f"so it is heat-set from below; the shoulder is a positive depth stop.")
print(f"  4. LASH AT THE DRIVE-REACTION STOP is {0.5141:.4f} deg (assembly "
      f"NB-4, measured on the r10 exports; free band -24.5142..+0.5142 deg, "
      f"bounded to 2.4573 deg with the stop pin fitted). On a "
      f"{360.0 / N_POCKET / 2:.1f} deg index that is "
      f"{0.5141 / (360.0 / N_POCKET / 2) * 100:.2f} % of a station of angular "
      f"error the FIRST time the drive loads in each direction, and it must "
      f"be in the count-contract text: the count is taken at the chute beam, "
      f"not from the commanded angle, so lash cannot manufacture a count.")
print(f"  5. SERVICE-STAND CLEARANCE is "
      f"{Z_MOTOR_BOT - STAND_GROUND_Z:.3f} mm (assembly NB-5): stand ground "
      f"plane z={STAND_GROUND_Z:.2f}, lowest assembly solid = the motor can "
      f"at z={Z_MOTOR_BOT:.2f}. The load path is the meter_housing latch-ring "
      f"underside on the stand's 3 pads -- printed structure, not the can.")
print(f"  3. THE DISC MUST BE COUNTER-INDEXED BY THE UNLOCK ANGLE "
      f"({CART_UNLOCK:+.0f} deg) when the cartridge goes in or out: the shaft "
      f"D-flat and the disc D-bore flat are a keyed pair, so at the wrong "
      f"relative angle the cartridge fouls the disc (the r3 critic measured "
      f"4.2552/4.6955/5.1242 mm3 at -20/-22/-24 deg and 0.0000 with the disc "
      f"counter-indexed). The disc is free in the bearing until the grub is "
      f"torqued, so this is a hand motion, not a fixture.")

print("\nFASTENER GRIP / ENGAGEMENT (measured by ray-cast on the exported "
      "STLs; r9: bay screw engagement 0.000 mm):")
_bay_m = trimesh.load(os.path.join(EXPORT_DIR, f"electronics_bay_{REV}.stl"))
_hou_m = trimesh.load(os.path.join(EXPORT_DIR, f"meter_housing_{REV}.stl"))


def _ycross(mesh, x, z, y0=-95.0):
    o = np.array([[x, y0, z]])
    loc, _, _ = mesh.ray.intersects_location(
        ray_origins=o, ray_directions=np.array([[0.0, 1.0, 0.0]]))
    return sorted(float(p[1]) for p in loc)


# the screw axis is a clean through-bore in the bay (a ray down it never
# touches the bay), so the HEAD plane is probed 2.2 mm off the axis, on the
# rib boss; the housing wall is probed on the SAME x but 2.0 mm off in z, so
# the Dia2.5 pilot is missed while the wall radius is identical (the housing
# OD is a cylinder about Z, so its y depends only on x).
_bay_y = _ycross(_bay_m, 14.0 + 2.2, RIB_ZC)
_hou_y = _ycross(_hou_m, 14.0, RIB_ZC - 2.0)
_head = min(_bay_y) if _bay_y else float("nan")
# the first HOUSING crossing inboard of the pilot mouth (the latch-ring band
# further out is not what the screw threads into)
_hou_in = [y for y in _hou_y if y > BAY_RIB_PILOT_Y0]
_wall = min(_hou_in) if _hou_in else float("nan")
print(f"  ray crossings: bay rib boss y {['%.3f' % v for v in _bay_y]}; "
      f"housing y {['%.3f' % v for v in _hou_y]}")
_pilot_end = BAY_RIB_PILOT_Y1
_grip = _wall - _head
_eng = min(BAY_SCREW_L - _grip, _pilot_end - _wall)
print(f"  bay->housing: head bearing plane y={_head:.3f} (bay rib outer "
      f"face), first threadable housing material y={_wall:.3f} (off-axis ray, "
      f"so this is wall, not pilot), pilot bottom y={_pilot_end:.3f}")
print(f"    GRIP = {_grip:.3f} mm; {BAY_SCREW} tip lands at "
      f"{_head + BAY_SCREW_L:.3f}; THREAD ENGAGEMENT = {_eng:.3f} mm "
      f"(available {_pilot_end - _wall:.3f} mm; r9's M3x12 achieved 0.000 and "
      f"stopped {_wall - (_head + 12.0):.3f} mm short of the housing)")
print(f"    r6 TRADE, stated not hidden (assembly A-12): r11 bought "
      f"5.080 mm of engagement by bottoming the pilot at y = -45.000, which "
      f"broke through the CURVED chamber wall over 27.7 % of the bore "
      f"section and left 0.144 mm of floor where it did not. Moving the floor "
      f"to {BAY_RIB_PILOT_Y1:.3f} closes it with "
      f"{abs(BAY_RIB_PILOT_Y1) - math.sqrt(CHAMBER_R**2 - 15.25**2):.3f} mm "
      f"of material under the WORST point of the bore section, and costs "
      f"{5.080 - _eng:.3f} mm of thread. {_eng:.3f} mm = "
      f"{_eng / 3.0:.2f} x D of thread-forming engagement in CF-PETG on a "
      f"2-screw joint that carries no drive reaction (the bay hangs off the "
      f"housing rib; the reaction path is the latch + stop pin + detent).")
assert _eng >= 3.5, "bay screw does not engage (A-9/A-12)"
_skirt_grip = SKIRT_R_OUT - HOUSING_R
_skirt_thread = SKIRT_SCREW_L - _skirt_grip
print(f"  hopper skirt tabs: head bearing r={SKIRT_R_OUT:.2f}, housing OD "
      f"r={HOUSING_R:.2f} -> GRIP {_skirt_grip:.3f} mm; {SKIRT_SCREW} presents "
      f"{_skirt_thread:.3f} mm of thread to a {HOUSING_R - (52.3 - SKIRT_PILOT_L):.3f} mm "
      f"pilot -> ENGAGEMENT {_skirt_thread:.3f} mm "
      f"({_skirt_thread / 3.0:.2f} x D), "
      f"{HOUSING_R - (52.3 - SKIRT_PILOT_L) - _skirt_thread:.3f} mm of pilot "
      f"left before the screw bottoms (r9: 4.850 mm of thread into a 4.100 mm "
      f"pilot -> bottomed out 0.750 mm before clamping)")
assert _skirt_thread < HOUSING_R - (52.3 - SKIRT_PILOT_L), \
    "skirt screw bottoms out (assembly NB-2)"
print("  bay lid: 4x M3 self-tap into corner-boss pilots")
print("  wiper: radial slide-in into an open-topped seat + end-tab M3 radial "
      "screw into a housing pilot; bristle strip pushed into the holder "
      "channel from the outboard end (both are field-replaceable)")
print(f"  cartridge: 3x quarter-turn lugs into ring slots; disc {GRUB_SIZE} set screw "
      f"at z={Z_SETSCREW:.1f} onto the shaft flat, tightened with the cartridge "
      f"out (a motion r5 actually verifies)")
print("  agitator: NO fastener -- hex-driven free rotor, lifts off upward "
      "(r4's set screw inside the funnel throat is deleted)")

# =====================================================================
# rev1 ROUND-5 CHECKS -- one block per round-4 critic BLOCKING/MAJOR
# finding (_run/rev1/CRITIQUE-r4.md). Each block prints the r10 number the
# fix has to move, then the r11 measurement.
# =====================================================================
print("\n============ REV-1 r5: ROUND-4 CRITIC FINDINGS ============")

# --- integration BLOCKING FAIL: the conduit elbow was solid -----------
print("R5-1 CONDUIT ELBOW PATENCY (r10, measured by the integration critic on "
      "top_plate_r10.stl: vertical bore axis SOLID over z -237.50..-225.00, "
      "horizontal bore axis SOLID over y -84.00..-72.00, largest conductor "
      "that could cross the elbow = Dia0.0):")
_tp_m = trimesh.load(os.path.join(EXPORT_DIR, f"top_plate_{REV}.stl"))


def _solid_runs(pts):
    """contiguous runs of points INSIDE the exported top_plate mesh"""
    _in = _tp_m.contains(np.array(pts))
    runs, s = [], None
    for _i, _f in enumerate(_in):
        if _f and s is None:
            s = _i
        if (not _f) and s is not None:
            runs.append((s, _i - 1))
            s = None
    if s is not None:
        runs.append((s, len(_in) - 1))
    return runs


_zs = np.arange(CONDUIT_Z_BOT, CONDUIT_ZC + 0.001, 0.25)
_vpts = [(0.0, CONDUIT_Y, float(z)) for z in _zs]
_vr = _solid_runs(_vpts)
print(f"     vertical spigot axis (x=0, y={CONDUIT_Y:.1f}), z "
      f"{_zs[0]:.2f}..{_zs[-1]:.2f} at 0.25 mm: "
      + ("NO SOLID POINT (bore is open end to end)" if not _vr else
         "SOLID over " + ", ".join(f"z {_zs[a]:.2f}..{_zs[b]:.2f}" for a, b in _vr)))
_ys = np.arange(CONDUIT_Y, -19.0 + 0.001, 0.25)
_hpts = [(0.0, float(y), CONDUIT_ZC) for y in _ys]
_hr = _solid_runs(_hpts)
print(f"     horizontal bore axis (x=0, z={CONDUIT_ZC:.2f}), y "
      f"{_ys[0]:.2f}..{_ys[-1]:.2f} at 0.25 mm: "
      + ("NO SOLID POINT (bore is open end to end)" if not _hr else
         "SOLID over " + ", ".join(f"y {_ys[a]:.2f}..{_ys[b]:.2f}" for a, b in _hr)))
_apts = [tuple(p) for p in _arc_pts(_ec_y, _ec_z, ELB_R, 90.0, 0.0, 64)]
_ar = _solid_runs(_apts)
print(f"     elbow centreline arc (R{ELB_R:.1f}, 65 points): "
      + ("NO SOLID POINT (the corner is a radius, not a step)" if not _ar else
         f"SOLID at {len(_ar)} runs"))
assert not _vr and not _hr and not _ar, \
    "conduit elbow is blocked (integration BLOCKING, r10)"
# swept bundle, per leg, against the exported-equivalent solids
_TOP_ROUTE = [r for r in _ROUTE[:5]]


def _sweep_solid(pts, dia, n_extra=0):
    s = None
    for _i in range(len(pts) - 1):
        _p0, _p1 = np.array(pts[_i], float), np.array(pts[_i + 1], float)
        _seg = float(np.linalg.norm(_p1 - _p0))
        _k = max(2, int(round(_seg / 1.0)))
        for _j in range(_k + 1):
            _p = _p0 + (_p1 - _p0) * (_j / _k)
            _b = Pos(*_p) * Sphere(dia / 2)
            s = _b if s is None else s + _b
    return s


print(f"  Dia5.5 bundle [A: 9-conductor 26 AWG PTFE] swept along each leg of "
      f"the modelled route, exact boolean vs top_plate + hopper + "
      f"electronics_bay:")
_bund_tot = 0.0
for _name, _pts, _exp in _TOP_ROUTE:
    _sw = _sweep_solid(_pts, 5.5)
    _v = (inter_vol(_sw, solids["top_plate"]) + inter_vol(_sw, solids["hopper"])
          + inter_vol(_sw, solids["electronics_bay"]))
    _bund_tot += _v
    print(f"     {_v:9.4f} mm3   {_name}")
print(f"     -> total {_bund_tot:.4f} mm3 (r10: the same sweep read 2.535 / "
      f"213.825 / 166.308 mm3 on three legs)")
assert _bund_tot < 1e-6, "harness bundle does not fit its own conduit"
_big = None
for _d in (5.5, 6.0, 7.0, 8.0):
    _sw = _sweep_solid([p for _, ps, _e in _TOP_ROUTE for p in ps], _d)
    _v = inter_vol(_sw, solids["top_plate"])
    print(f"     largest-bundle probe: Dia{_d:.1f} over the WHOLE top-plate "
          f"route ^ top_plate = {_v:.4f} mm3")
    if _v < 1e-6:
        _big = _d
print(f"     -> largest conductor bundle that crosses the elbow = "
      f"Dia{_big:.1f} (r10: Dia0.0)")
# N-i2: the connector cannot follow the harness; say so with numbers
print(f"  N-i2 CONNECTOR vs BORE: the aircraft-side shell is a Molex 12-circuit "
      f"1.25 mm-pitch housing, ~16.7 x 5.8 mm envelope [A: catalogue figure "
      f"from memory, CLOSURE = the ordered PN drawing]. Its diagonal 17.68 mm "
      f"does NOT pass the measured Dia{2 * CONDUIT_R_I:.1f} conduit bore and "
      f"cannot turn the R{ELB_R:.1f} elbow. SHIPPED WORKFLOW, stated as an "
      f"assembly constraint: the harness is routed as 12 LOOSE CRIMPED "
      f"terminals (each ~2.1 x 1.0 mm, bundle 10.4 mm2 = "
      f"{10.4 / (math.pi * CONDUIT_R_I ** 2) * 100:.1f} % of the "
      f"{math.pi * CONDUIT_R_I ** 2:.2f} mm2 bore) and the J1 housing is "
      f"populated at the neck AFTER routing. No conduit is openable.")

# --- assembly BLOCKING A-10: cap head vs the modelled countersink -----
print("\nR5-2 A-10 GEARBOX SCREW HEAD (r10 BOM ordered `M3x8 SHCS` for a 90 "
      "deg countersink; measured by the assembly critic: 8.8652 mm3 per screw "
      "static and 49.4066 mm3 over one 45 deg spoke pitch, and it never "
      "returns to zero):")
_CS_TOP_Z = Z_RPLATE_TOP
_CS_BOT_Z = Z_RPLATE_TOP - 1.4          # modelled cone: r1.7 -> r3.1 over 1.4
_flat_heads = None
_cap_heads = None
for _hx, _hy in MOTOR_HOLES:
    _fh = Pos(_hx, _hy, (_CS_TOP_Z + _CS_BOT_Z) / 2) * Cone(
        MOTOR_SCREW_CLR, 3.05, _CS_TOP_Z - _CS_BOT_Z)
    _flat_heads = _fh if _flat_heads is None else _flat_heads + _fh
    _zb = _CS_BOT_Z + (2.75 - MOTOR_SCREW_CLR)     # where a Dia5.5 head bears
    _ch = Pos(_hx, _hy, _zb + 1.5) * Cylinder(2.75, 3.0)
    _cap_heads = _ch if _cap_heads is None else _cap_heads + _ch
print(f"     countersink as modelled: cone r{MOTOR_SCREW_CLR:.2f} at "
      f"z={_CS_BOT_Z:.3f} -> r3.05 at z={_CS_TOP_Z:.3f} (90 deg included), "
      f"shank Dia{2 * MOTOR_SCREW_CLR:.2f} to the gearbox face "
      f"z={Z_RPLATE_BOT:.3f}")
_a10_grip = _CS_TOP_Z - Z_RPLATE_BOT
_a10_thread = 8.0 - _a10_grip
print(f"     FLUSH FLAT HEAD (ISO 10642 / DIN 7991): GRIP {_a10_grip:.3f} mm "
      f"(plate TOP FACE z={_CS_TOP_Z:.3f} to the gearbox flange face "
      f"z={Z_RPLATE_BOT:.3f}), M3x8 leaves {_a10_thread:.3f} mm of thread "
      f"beyond the grip -- the screw must NOT be lengthened. The assembly "
      f"critic printed 3.950/4.050 for the same joint because they seated "
      f"the head 0.050 mm below the top face; the difference is the head "
      f"clearance, not a geometry change.")
_a10_flat_static = sum(inter_vol(_flat_heads, s) for n, s in solids.items()
                       if n != "retaining_plate_chute")
_a10_flat_plate = inter_vol(_flat_heads, solids["retaining_plate_chute"])
print(f"     flat head x4 ^ EVERY other assembly solid (static, assembled "
      f"clocking) = {_a10_flat_static:.4f} mm3; ^ its own countersink in "
      f"retaining_plate_chute = {_a10_flat_plate:.4f} mm3 (it seats IN the "
      f"cone, so this is the seat contact, not interference)")
_a10_worst_flat = 0.0
_a10_worst_cap = 0.0
_cap_static = inter_vol(_cap_heads, solids["pocket_disc"])
print("     disc swept over one 45 deg spoke pitch (3 deg steps), heads "
      "static:")
for _ang in range(0, 46, 3):
    _dr = Rot(Z=float(_ang)) * copy.copy(solids["pocket_disc"])
    _vf = inter_vol(_flat_heads, _dr)
    _vc = inter_vol(_cap_heads, _dr)
    _a10_worst_flat = max(_a10_worst_flat, _vf)
    _a10_worst_cap = max(_a10_worst_cap, _vc)
    print(f"        disc {_ang:3d} deg: flat head {_vf:8.4f} mm3   "
          f"Dia5.5x3.0 CAP HEAD CONTROL {_vc:8.4f} mm3")
print(f"     -> flat head worst over the pitch {_a10_worst_flat:.4f} mm3 "
      f"(must be 0.0000); cap-head control worst {_a10_worst_cap:.4f} mm3, "
      f"static {_cap_static:.4f} mm3 (assembly critic: 49.4066 / 8.8652). "
      f"Vertical air between the plate top at the bolt circle "
      f"({Z_RPLATE_TOP:.3f}) and the disc underside ({Z_DISC_BOT:.3f}) = "
      f"{Z_DISC_BOT - Z_RPLATE_TOP:.3f} mm; a cap head stands "
      f"{3.0 - (2.75 - MOTOR_SCREW_CLR):.3f} mm proud of it")
assert _a10_worst_flat < 1e-6 and _a10_flat_static < 1e-6, \
    "countersunk gearbox screw fouls something (A-10)"

# --- granule-path MAJOR: the plug tether lug in the drop tube ---------
print("\nR5-3 PLUG TETHER LUG + PLUG FLANGE (r10: lug inboard face 1.000 mm "
      "INSIDE the r11.000 bore -> r_min 10.000 over z -398.00..-404.00; "
      "plate ^ plug 206.0993 mm3 logged as 'the designed 0.3 mm press fit' "
      "when only 83.504 mm3 of it was):")
_rp_m = trimesh.load(os.path.join(EXPORT_DIR, f"retaining_plate_chute_{REV}.stl"))
print("     radial ray sweep from the chute axis, 1 deg x 13 heights:")
for _z in np.arange(-396.0, -405.01, -0.75):
    _rmin = 99.0
    _org, _dirs = [], []
    for _a in range(0, 360):
        _ra = math.radians(_a)
        _org.append([PCD_R, 0.0, float(_z)])
        _dirs.append([math.cos(_ra), math.sin(_ra), 0.0])
    _loc, _ir, _ = _rp_m.ray.intersects_location(
        ray_origins=np.array(_org), ray_directions=np.array(_dirs))
    if len(_loc):
        _d = np.linalg.norm(_loc - np.array([PCD_R, 0.0, float(_z)]), axis=1)
        _rmin = float(_d.min())
    print(f"        z={_z:8.2f}: r_min {_rmin:7.3f} mm"
          + ("   <- BORE WALL, nothing proud" if _rmin >= CHUTE_ID / 2 - 0.01
             else "   <- INTRUSION"))
_pp = solids["retaining_plate_chute"] & aux_solids["chute_plug"]
_bodies = [] if _pp is None else sorted(_pp.solids(), key=lambda s: -s.volume)
print(f"     retaining_plate_chute ^ chute_plug (fitted pose) = "
      f"{sum(b.volume for b in _bodies):.4f} mm3 in {len(_bodies)} bodies, "
      f"decomposed:")
for _b in _bodies:
    _bb = _b.bounding_box()
    print(f"        {_b.volume:9.4f} mm3  x[{_bb.min.X:7.2f},{_bb.max.X:7.2f}] "
          f"y[{_bb.min.Y:7.2f},{_bb.max.Y:7.2f}] "
          f"z[{_bb.min.Z:9.3f},{_bb.max.Z:9.3f}]")
_press_nom = 2 * math.pi * (CHUTE_ID + PLUG_INTERF / 2) / 2 * (PLUG_INTERF / 2) * PLUG_LAND_H
print(f"     the DESIGNED press fit is the Dia{CHUTE_ID + PLUG_INTERF:.1f} land "
      f"in the Dia{CHUTE_ID:.1f} bore over {PLUG_LAND_H:.1f} mm = "
      f"2*pi*{(CHUTE_ID + PLUG_INTERF / 2) / 2:.3f}*{PLUG_INTERF / 2:.3f}*"
      f"{PLUG_LAND_H:.1f} = {_press_nom:.3f} mm3. Anything else in the list "
      f"above is NOT designed.")

# --- granule-path: reverse free travel at r=24.5, not just the PCD ----
print("\nR5-4 REVERSE-STROKE BOUND AT r=24.5 (the critic: 'a stacked Dia13 "
      "granule spans r 25.5..38.5, it is not a point at the PCD'; publish "
      "2.25 deg, not the PCD-only 2.75):")
for _rr in (24.5, PCD_R, 39.5):
    _w = 9e9
    for _p in _PARKS:
        _c0 = _ceiling_ray(_p, _rr)
        if _c0 is None or _c0 >= 11.5 - 1e-6:
            _t, _free = 0.0, None
            while _t <= 120.0:
                _c = _ceiling_ray(_p + _t, _rr)
                if _c is not None and _c < 11.5 - 1e-6:
                    _free = _t
                    break
                _t += 0.25
            _w = min(_w, 120.0 if _free is None else _free)
    print(f"     r={_rr:5.1f}: guaranteed reverse free travel for an 11.5 mm "
          f"stack = {_w:.2f} deg")

# --- granule-path / N10: the sump-outlet plateau, measured ------------
print("\nR5-5 N10 SUMP OUTLET, re-measured on meter_housing_%s.stl (recorded "
      "PLATEAU, not a pass):" % REV)


_hous_only = trimesh.load(os.path.join(EXPORT_DIR, f"meter_housing_{REV}.stl"))


def _open_at(th, rr):
    """open = NO meter_housing material above the disc face at (th, rr).
    r11b measured this with brush_holder in the ceiling mesh too, which is
    the WIPER, not the sump roof, and it read a 115.000 deg span."""
    o = np.array([[rr * math.cos(math.radians(th)),
                   rr * math.sin(math.radians(th)), Z_DISC_TOP + 0.02]])
    loc, _, _ = _hous_only.ray.intersects_location(
        ray_origins=o, ray_directions=np.array([[0.0, 0.0, 1.0]]))
    return len(loc) == 0


_lo, _hi = FILL_ARC[0] - 5.0, FILL_ARC[0] + 5.0
for _ in range(40):
    _m = (_lo + _hi) / 2
    if _open_at(_m, PCD_R):
        _hi = _m
    else:
        _lo = _m
_edge0 = (_lo + _hi) / 2
_lo, _hi = FILL_ARC[1] - 5.0, FILL_ARC[1] + 5.0
for _ in range(40):
    _m = (_lo + _hi) / 2
    if _open_at(_m, PCD_R):
        _lo = _m
    else:
        _hi = _m
_edge1 = (_lo + _hi) / 2
_lo, _hi = 17.0, 25.0     # 17 is inside the bearing-boss material, 25 is open
for _ in range(40):
    _m = (_lo + _hi) / 2
    if _open_at(190.0, _m):
        _hi = _m
    else:
        _lo = _m
_r_in = (_lo + _hi) / 2
_lo, _hi = 40.0, 52.0
for _ in range(40):
    _m = (_lo + _hi) / 2
    if _open_at(190.0, _m):
        _lo = _m
    else:
        _hi = _m
_r_out = (_lo + _hi) / 2
_span = _edge1 - _edge0
_area = math.pi * (_r_out ** 2 - _r_in ** 2) * _span / 360.0
print(f"     window edges bisected to 1e-4 deg at the PCD: theta "
      f"{_edge0:.3f} -> {_edge1:.3f} = {_span:.3f} deg; radial span at "
      f"theta=190: r {_r_in:.3f} -> {_r_out:.3f} = {_r_out - _r_in:.3f} mm")
print(f"     area {_area:.1f} mm2 -> equivalent circular orifice D "
      f"{2 * math.sqrt(_area / math.pi):.2f} mm; min opening / D_max = "
      f"{(_r_out - _r_in) / PELLET_D_MAX:.3f} (a slot wants >= 3, a hopper "
      f"outlet 4-6) -> the no-arch criterion is met ONLY through the active "
      f"agitation branch")
print(f"     agitator defence: 3 fingers at theta 0/120/240, so exactly one "
      f"is in the {_span:.1f} deg window at a time; each {360.0 / N_POCKET / 2:.1f} deg "
      f"index sweeps {360.0 / N_POCKET / 2 / _span * 100:.2f} % of the window = one full "
      f"sweep per {_span / (360.0 / N_POCKET / 2):.2f} INDEXES = "
      f"{_span / (360.0 / N_POCKET):.2f} dispensed granules (the cycle is "
      f"TWO 22.5 deg indexes per granule)")

# --- assembly item 3: the order table and the torque path, RE-PRINTED --
print("\nR5-7 ASSEMBLY ORDER RE-PRINTED FROM THE TOOLS (assembly critic item "
      "3: 'not asserted'). Each row is a straight approach; primed rows are "
      "CONTROLS -- the same part on the opposite approach, printed so that "
      "0.0000 cannot mean 'the probe missed'.")
_ASM_SOL = dict(solids)
_ASM_SOL.update(aux_solids)
_ASM = [
    ("2  igus JFM-2023-07 into the roof bore", ["sleeve_bearing"], (0, 0, 1),
     40.0, ["meter_housing"]),
    ("2' (same, from below) CONTROL", ["sleeve_bearing"], (0, 0, -1),
     40.0, ["meter_housing"]),
    ("4  pocket_disc, hub up through the bearing", ["pocket_disc"], (0, 0, -1),
     40.0, ["meter_housing", "sleeve_bearing", "brush_holder"]),
    ("4' (same, from above) CONTROL", ["pocket_disc"], (0, 0, 1),
     40.0, ["meter_housing", "sleeve_bearing", "brush_holder"]),
    ("5  agitator onto the Dia15 hex", ["agitator"], (0, 0, 1), 40.0,
     ["meter_housing", "sleeve_bearing", "brush_holder", "pocket_disc"]),
    ("10 electronics_bay onto the housing ribs", ["electronics_bay"],
     (0, -1, 0), 40.0, ["meter_housing", "pocket_disc",
                        "retaining_plate_chute"]),
    ("12 hopper down over the bay riser", ["hopper"], (0, 0, 1), 60.0,
     ["meter_housing", "electronics_bay", "pocket_disc", "agitator",
      "retaining_plate_chute"]),
    ("13 top_plate onto the hopper flange", ["top_plate"], (0, 0, 1), 40.0,
     ["hopper", "electronics_bay", "meter_housing"]),
    ("14 clip plate + blind-mate PCB", ["clip_plate", "blindmate_pcb"],
     (0, 0, 1), 30.0, ["top_plate", "hopper"]),
]
for _nm, _mem, _vec, _dist, _obs in _ASM:
    _stmax, _swept, _sw_un = 0.0, None, 0.0
    for _t in np.linspace(_dist, 0.0, 11):
        _v = 0.0
        for _m in _mem:
            _s = Pos(_vec[0] * _t, _vec[1] * _t, _vec[2] * _t) * copy.copy(
                _ASM_SOL[_m])
            _swept = _s if _swept is None else _swept + _s
            for _o in _obs:
                if bb_disjoint(_s, _ASM_SOL[_o]):
                    continue
                _v += inter_vol(_s, _ASM_SOL[_o])
        _stmax = max(_stmax, _v)
    for _o in _obs:
        if not bb_disjoint(_swept, _ASM_SOL[_o]):
            _sw_un += inter_vol(_swept, _ASM_SOL[_o])
    print(f"     station-max {_stmax:12.4f} | swept-union {_sw_un:12.4f} mm3  "
          f"{_nm}")
# torque path: flat-on-flat engagement, measured on the export + the model
print("  TORQUE PATH, flat-on-flat engagement re-measured (assembly critic: "
      "12.000 mm):")
_disc_m = trimesh.load(os.path.join(EXPORT_DIR, f"pocket_disc_{REV}.stl"))
_fa = math.radians(GRUB_A)


def _bore_r(z, a):
    _loc, _ir, _ = _disc_m.ray.intersects_location(
        ray_origins=np.array([[0.0, 0.0, float(z)]]),
        ray_directions=np.array([[math.cos(a), math.sin(a), 0.0]]))
    if not len(_loc):
        return None
    return float(np.linalg.norm(_loc[:, :2], axis=1).min())


_lo, _hi = Z_DISC_BOT, Z_DISC_TOP
for _ in range(30):
    _m = (_lo + _hi) / 2
    _r = _bore_r(_m, _fa)
    if _r is not None and _r < 2.8:
        _hi = _m
    else:
        _lo = _m
_disc_flat_z0 = (_lo + _hi) / 2
print(f"     disc D-bore: r at the flat azimuth = "
      f"{_bore_r(Z_DISC_TOP - 1.0, _fa):.3f} mm, round azimuth = "
      f"{_bore_r(Z_DISC_TOP - 1.0, _fa + math.pi / 2):.3f} mm; the flat "
      f"STARTS at z = {_disc_flat_z0:.4f} (bisected 1e-4)")


def _shaft_solid_at(z, r=2.8):
    _p = Pos(r * math.cos(_fa), r * math.sin(_fa), z) * Box(0.3, 0.3, 0.3)
    return inter_vol(_p, solids["stepper"]) > 1e-6


_lo, _hi = Z_MOTOR_TOP, Z_MOTOR_TOP + MOTOR_SHAFT_LEN
for _ in range(24):
    _m = (_lo + _hi) / 2
    if _shaft_solid_at(_m):
        _lo = _m
    else:
        _hi = _m
_shaft_flat_z0 = (_lo + _hi) / 2
_shaft_top = Z_MOTOR_TOP + MOTOR_SHAFT_LEN
_engage = min(_shaft_top, Z_DISC_TOP) - max(_shaft_flat_z0, _disc_flat_z0)
print(f"     shaft flat starts at z = {_shaft_flat_z0:.4f}, shaft top "
      f"{_shaft_top:.3f}; FLAT-ON-FLAT ENGAGEMENT = {_engage:.3f} mm "
      f"(vendor D-cut is 12 mm)")
# F1 / F1b driver corridor pair
_f1b = {}
for _dia in (6.0, 8.0, 10.0, 12.0):
    _v = 0.0
    for (_bx, _by) in MOTOR_HOLES:
        _col = Pos(_bx, _by, Z_RPLATE_TOP + 12.5) * Cylinder(_dia / 2, 25.0)
        _v += sum(inter_vol(_col, _ASM_SOL[k]) for k in ("thrust_washer",)
                  if not bb_disjoint(_col, _ASM_SOL[k]))
    _f1b[_dia] = _v
_ok = [d for d, v in _f1b.items() if v < 1e-3]
print(f"     F1b (plate+motor+washer SUB-ASSEMBLY on the bench, i.e. the "
      f"pose the screws are actually driven in; the disc is NOT part of it): "
      + ", ".join(f"Dia{d:.1f} -> {v:.4f}" for d, v in _f1b.items())
      + f" -> largest clear driver = Dia{max(_ok) if _ok else 0.0:.1f} "
      f"(F1 in situ is Dia0.0, printed above)")

# --- integration nonblocking: prop clearance, MEASURED not carried ----
# r5: the first attempt did this IN PROCESS and the kernel killed the run
# (exit 137): the propulsion assembly meshes to 1.57 M faces even at 1.0 mm
# tolerance and needs ~1.8 GB on its own. It is measured in a SUBPROCESS so
# the memory is reclaimed, and the subprocess output is quoted below.
print("\nR5-6 PROP CLEARANCE, MEASURED (r10 restated the r2 figures verbatim; "
      "the critic asked for a measurement or an admission):")
_PROP_SRC = r'''
import sys, os, tempfile
sys.path.insert(0, "/tmp/pq-main/src")
import numpy as np, trimesh
from build123d import export_stl
from scipy.spatial import cKDTree
from quiver.equipment.propulsion.assembly import make_assembly
asm = trimesh.load(sys.argv[1])
p = make_assembly()
f = tempfile.NamedTemporaryFile(suffix=".stl", delete=False).name
export_stl(p, f, tolerance=1.0)
pm = trimesh.load(f, process=False)
os.unlink(f)
pv = np.asarray(pm.vertices)
av = np.asarray(asm.vertices)
d = cKDTree(pv).query(av)[0]
print("     propulsion assembly: %d faces at 1.0 mm tolerance, bbox "
      "Z [%.2f, %.2f], plan radius %.1f mm"
      % (len(pm.faces), pm.bounds[0][2], pm.bounds[1][2],
         float(np.linalg.norm(pv[:, :2], axis=1).max())))
print("     payload assembly:    bbox Z [%.3f, %.3f], plan radius %.2f mm"
      % (asm.bounds[0][2], asm.bounds[1][2],
         float(np.linalg.norm(av[:, :2], axis=1).max())))
print("     VERTICAL gap, lowest propulsion material to payload top = "
      "%.2f mm  (r2 carried: 152.5)" % (pm.bounds[0][2] - asm.bounds[1][2]))
print("     IN-PLAN gap, payload max radius to the nearest propulsion "
      "material radius = %.2f mm  (r2 carried: 239.3)"
      % (float(np.linalg.norm(pv[:, :2], axis=1).min())
         - float(np.linalg.norm(av[:, :2], axis=1).max())))
print("     VERTEX-TO-VERTEX minimum separation (KD-tree, %d propulsion "
      "vertices x %d payload vertices) = %.2f mm  [method: vertex-level, so "
      "it over-reports by at most one 1.0 mm chord]"
      % (len(pv), len(av), float(d.min())))
'''
import subprocess as _sp
import sys as _sysp
_r = _sp.run([_sysp.executable, "-c", _PROP_SRC, ASM_STL], capture_output=True,
             text=True, timeout=900)
if _r.returncode == 0:
    print(_r.stdout.rstrip())
else:
    print(f"     NOT MEASURED (subprocess rc={_r.returncode}): "
          f"{_r.stderr.strip().splitlines()[-1] if _r.stderr.strip() else ''}")
    print("     the r2 figures (vertical 152.5 mm, radial 239.3 mm) are "
          "CARRIED, not measured; the B6 stand-off only moves the payload "
          "further from the disk, so there is no regression risk -- but the "
          "shipped number is carried and this line says so.")

# =====================================================================
# Mass ledger (printed part masses MEASURED from solid volumes)
# =====================================================================
print("\n================ MASS LEDGER ================")
print("  (printed parts priced at 100% INFILL from the measured solid volume "
      "-- stated explicitly per the r4 mass critic; the slicer-realistic "
      "bracket is measured below and is LIGHTER, so the ceiling case here is "
      "the conservative one.)")
total = 0.0
ESTIMATED = {"blindmate_pcb", "brush_bristles", "stepper"}
for k, v in parts.items():
    print(f"  {k:24s} {v['mass']:7.1f} g   {v['basis']}")
    total += v["mass"]
# r2: the FLIGHT aux parts were exported and BOM'd but never entered the
# ledger. They do now (ground-only chute_plug / service_stand still do not).
for k in ASM_AUX:
    print(f"  {k:24s} {aux[k]['mass']:7.1f} g   {aux[k]['basis']}")
    total += aux[k]["mass"]
fixed = [
    ("electronics: STM32G431KBT6+TCAN332, TMC2209, D36V6F5 buck, 2x "
     "VBPW34FAS + OPA2320 + 2x TSAL6200 analog count chain, 2x DRV5032, "
     "wiring", 65.0, "[J] PNs listed below, ASSUMPTION"),
    ("fasteners: M3/M2.5 screws/nuts, 6x heat-set inserts, 3x plastite, "
     "4x lid screws, 4x M2 mount screws + M2 inserts, M5 spring plunger, "
     "thread-locker", 57.0, "[J]"),
    ("O-ring + gaskets + 9x Dia3x2 magnets (S-03-02-N)", 8.0, "[J]"),
]
for name, m, basis in fixed:
    print(f"  {name:60s} {m:6.1f} g  {basis}")
    total += m
print(f"  EMPTY TOTAL (measured+estimates)      {total:7.1f} g")
cont = 0.10 * total
print(f"  contingency 10% (CAD stage)           {cont:7.1f} g")
empty = total + cont
print(f"  EMPTY, carried                        {empty:7.1f} g")
print(f"  + 250 pellets                         {250*PELLET_MASS:7.1f} g")
loaded250 = empty + 250 * PELLET_MASS
print(f"  LOADED @250                           {loaded250:7.1f} g  "
      f"(ceiling 1500 g -> margin {1500 - loaded250:.0f} g)")
print(f"  sensitivity: stepper at 200 g -> LOADED @250 = "
      f"{loaded250 + (200 - MOTOR_MASS) * 1.10:7.1f} g; steel clip plate (+59 g) "
      f"-> {loaded250 + 59 * 1.10:7.1f} g; CF-PETG at 1.31 g/cm3 -> "
      f"{EMPTY_PESS - (PESS_MOTOR - MOTOR_MASS) * 1.10 + 250 * PELLET_MASS:7.1f} g "
      f"(all pass)")
print(f"  + {N_FILL_MAX} pellets (MAX fill rib)        {N_FILL_MAX*PELLET_MASS:7.1f} g")
print(f"  LOADED @{N_FILL_MAX} (max fill line)          {empty + N_FILL_MAX*PELLET_MASS:7.1f} g  "
      f"({'under' if empty + N_FILL_MAX*PELLET_MASS < 1500 else 'OVER'} the 1500 g "
      f"ceiling on the strict no-exemption reading; worst-case ledger "
      f"{EMPTY_PESS + N_FILL_MAX*PELLET_MASS:.1f} g)")
print(f"  + full hopper ({cap_worst} worst-case)     {cap_worst*PELLET_MASS:7.1f} g")
print(f"  LOADED @{cap_worst} (brim, max)            {empty + cap_worst*PELLET_MASS:7.1f} g  "
      f"(pellet mass >250 exempt per CONTEXT; sane vs 5-8 kg platform)")

# ---- r5 (mass MINOR): estimate exposure, stated honestly
est_mass = sum(v["mass"] for k, v in parts.items() if k in ESTIMATED
               and k != "stepper") \
    + sum(m for _, m, _ in fixed) + parts["sleeve_bearing"]["mass"] \
    + parts["thrust_washer"]["mass"]
print(f"\n  ESTIMATE EXPOSURE: {est_mass:.1f} g of the {total:.1f} g empty "
      f"subtotal ({100*est_mass/total:.1f}%) is NOT measured from modeled "
      f"geometry (blind-mate PCB, bristle strip, bushing, washer, "
      f"electronics, fasteners, seals+magnets; the stepper's 190 g is a "
      f"vendor catalogue figure, counted separately). The 10% contingency "
      f"({cont:.1f} g) does NOT bound it -- r4 claimed ~117 g and the true "
      f"figure was 155 g. Nothing here is ceiling-critical (margin "
      f"{1500-loaded250:.0f} g), but the number is now printed, not asserted.")

# ---- r5 (mass MODERATE): slicer-realistic INFILL BRACKET, measured by
# voxelising each printed part and eroding 1.6 mm (4 x 0.4 mm walls).
_sliced250 = loaded250          # falls back to the pessimistic basis
try:
    from scipy import ndimage
    print("\n  INFILL BRACKET (voxel erosion, 4 perimeters @0.4 + 25% infill):")
    tot_solid = tot_infill = 0.0
    for pname in PRINTED:
        m = trimesh.load(os.path.join(EXPORT_DIR, f"{pname}_{REV}.stl"))
        pitch = 0.6
        vg = m.voxelized(pitch=pitch).fill()
        # rev1 N13 (mass-budget MODERATE): the r5/r6/r7 code ran the EDT on
        # the UNPADDED occupancy array, so every voxel touching the array
        # boundary was treated as interior and the hollow core was grossly
        # overstated (334.0 -> 383.4 g on the slicer bracket; the flat-plate
        # control below read 68 % core on a 3.2 mm plate). Padded now.
        mat = np.pad(vg.matrix, 4)
        # EDT counts the surface voxel itself as 1 -> subtract half a voxel
        dist = (ndimage.distance_transform_edt(mat) - 0.5) * pitch
        core = float((dist > 1.6).sum()) * pitch ** 3
        if pname == "bay_lid":                    # N13 flat-plate control
            _ctl = 100.0 * core / m.volume
        vol = m.volume
        dens = (DENS["tpu"] if pname == "agitator"
                else DENS["petg"] if pname == "fill_cap" else DENS["petg_cf"])
        m_solid = vol * dens
        m_infill = (vol - core + 0.25 * core) * dens
        tot_solid += m_solid
        tot_infill += m_infill
        print(f"    {pname:22s} solid {m_solid:6.1f} g   core "
              f"{core/1000:6.2f} cm3   at 25% infill {m_infill:6.1f} g")
    print(f"    N13 CONTROL (bay_lid, a 3.2 mm flat plate: 4x0.4 walls = "
          f"1.6 mm/side leaves ~0 core): hollow core = {_ctl:.1f} % of volume "
          f"(requirement <= 10 %; the unpadded r7 code read 68.6 %)")
    print(f"    printed-parts total: solid {tot_solid:.1f} g -> sliced "
          f"{tot_infill:.1f} g ({tot_solid - tot_infill:.1f} g of the ledger is "
          f"a 100%-infill modelling artifact). LOADED @250 would be "
          f"{loaded250 - (tot_solid - tot_infill) * 1.10:.1f} g.")
    # ---- rev1 B11.2 / B11.4: SHIPPED HEADLINE BASIS + RESERVE ---------
    _sliced250 = loaded250 - (tot_solid - tot_infill) * 1.10
    print(f"\n  B11.2 SHIPPED HEADLINE BASIS = the SLICER-REALISTIC ledger "
          f"(4 perimeters at 0.4 mm + 25 % infill, padded EDT): "
          f"LOADED @250 = {_sliced250:.1f} g vs the 1500 g ceiling -> margin "
          f"{1500 - _sliced250:+.0f} g. This is the basis chosen because it "
          f"is what actually gets printed; the 100 %-INFILL figure "
          f"({loaded250:.1f} g, margin {1500 - loaded250:+.0f} g) is carried "
          f"as the PESSIMISTIC BOUND and is stated, not hidden. rev-0 shipped "
          f"the 100 %-infill basis at 1387.4 g; the delta since then is "
          f"almost entirely B11.3 (stepper 310 -> 350 g) plus the B4/B5/B6 "
          f"geometry the punch list required.")
    print(f"  B11.4 PER-OPEN-ITEM MASS RESERVE (each is a known-open item "
          f"that will add mass when it closes; none is in the ledger above):")
    _res = [("count-sensor boards + 2 cable looms (ELECTRONICS 7)", 12.0),
            ("4 x PMMA windows + bonding, 8 x M2 cover screws", 3.0),
            ("wiring harness itself (9 x 26 AWG, ~250 mm) [A]", 18.0),
            ("grommets x5 + bay gasket cord", 6.0),
            ("delivered gearbox flange pilot may force a plate rework (B3.4)",
             10.0),
            ("fill-cap detent / N5 and tether lug / N9, both still open",
             12.0)]
    for _l, _m in _res:
        print(f"    {_m:5.1f} g  {_l}")
    print(f"    {sum(m for _, m in _res):5.1f} g  TOTAL RESERVE -> headline "
          f"basis with reserve = {_sliced250 + sum(m for _, m in _res):.1f} g "
          f"(margin {1500 - _sliced250 - sum(m for _, m in _res):+.0f} g)")
except Exception as e:
    print("  INFILL BRACKET unavailable:", e)

# ---- r5 (mass MODERATE): block-by-block attribution of the >1.0 kg overage
over = loaded250 - 1000.0
cap_extra_h = Z_TOP_BOT - Z_FILL250          # cylinder above the 250 line
cyl_wall_cm3 = math.pi * ((HOP_RI + HOP_WALL) ** 2 - HOP_RI ** 2) * cap_extra_h / 1000
print(f"\n  OVER-1.0 kg ATTRIBUTION (CONTEXT: every 100 g above 1.0 kg must be "
      f"justified). LOADED @250 = {loaded250:.1f} g -> {over:.1f} g over.")
_att = [
    ("geared stepper 14HS13-0804S-PG5: the gearbox is what makes CONTEXT "
     "requirement 2 (shear a fragment) achievable at all -- 20.4 N recovery "
     "at the pocket lip vs 5.6 N in r5 -- while the driver current limit "
     "keeps normal metering at 12.2 N, 3.4x under the pellet crush load",
     parts["stepper"]["mass"]),
    ("capacity oversizing: the straight cylinder above the 250-pellet line, "
     f"{cap_extra_h:.0f} mm of 2.5 mm wall = {cyl_wall_cm3:.0f} cm3 "
     f"(CONTEXT: more capacity is an explicit design goal)",
     cyl_wall_cm3 * DENS["petg_cf"] * 1000),
    ("quarter-turn latch ring + retaining plate lugs: carries the ~500 g "
     "cartridge + pellet column and makes the jam-clear path tool-free",
     parts["retaining_plate_chute"]["mass"] * 0.35),
    ("modeled fastening at every joint (inserts, plastites, nut bosses, "
     "skirt tabs) + phase/safe-state hardware (9 magnets, 2 Hall pockets, "
     "detent plunger boss)", 57.0 + 8.0),
    ("electronics + blind-mate PCB (CAN node, driver, buck, count chain)",
     65.0 + 15.0),
    ("clip plate (COTS, not ours to trade)", parts["clip_plate"]["mass"]),
]
_rem = over
for lbl, m in _att:                     # partition the overage, largest first
    take = min(m, _rem)
    _rem -= take
    print(f"    {take:6.1f} g of {m:5.1f} g  {lbl}")
    if _rem <= 0.05:
        break
print(f"    {_rem:6.1f} g  unattributed")
print(f"    (the justified blocks total {sum(m for _, m in _att):.1f} g, i.e. "
      f"{sum(m for _, m in _att) - over:.1f} g MORE than the overage: every "
      f"gram above 1.0 kg is spoken for by hardware that cannot be deleted "
      f"without deleting a requirement. Deleting the capacity oversizing "
      f"alone would put the 250-load at {loaded250 - 61.1:.0f} g.)")

# COTS part numbers (r3 buildability MODERATE: named at class level only)
COTS = [
    ("geared stepper", "StepperOnline 14HS13-0804S-PG5 (5.18:1 planetary)",
     "VERIFIED vendor page: 0.14 N*m, 1.0 A/ph, backlash <=3 deg, max 3 N*m, "
     "Dia6x18 D-cut, gross 0.38 kg; 350 g NET carried (rev1 B11.3: same "
     "figure as the ledger/README, vendor catalogue class -- never on a "
     "scale; closure is to weigh one)"),
    # rev1 close-out B3.4: this row exists so the Dia16.20 pilot bore the
    # retaining plate models for the gearbox output boss is stated WHERE THE
    # ORDER HAPPENS, next to the part it must clear. Bore edge measured at
    # r=8.10 through the 4.000 mm flange band; Dia26 bolt circle is datasheet;
    # the BOSS diameter itself is not in the datasheet extract -> ASSUMPTION.
    ("gearbox output boss", "(feature of the stepper above)",
     "rev1 B3.4: retaining plate pilot bore modelled Dia%.2f for this boss; "
     "Dia%.0f bolt circle VERIFIED (datasheet); the boss diameter the bore "
     "must clear is an ASSUMPTION -- caliper-check the real motor before "
     "printing the plate" % (2 * MOTOR_PILOT_R + 0.20, 2 * MOTOR_BC_R)),
    ("sleeve bearing", "igus iglidur J JFM-2023-07 (ID20/OD23/L7)",
     "length VERIFIED catalogued (TME/RS list JFM-2023-07/11/16/21); flange "
     "Dia30x2 ASSUMPTION"),
    ("mount screws", "4x M2x10 ISO 4762 A2 + 4x Ruthex RX-M2x4 heat-set inserts",
     "head Dia3.8 vs the mapped Dia3.90 pocket -- 0.05 mm/side, tolerance item"),
    ("PCB screws", "4x M2x5 into the clip plate's own tabs", "vendor feature"),
    ("driver", "BIGTREETECH TMC2209 V1.3 module (or TMC2209-LA-T)", "ASSUMPTION"),
    # rev1 B4.7 / ELECTRONICS 4.4: the TSSP4038 is a 38 kHz DIGITAL burst
    # receiver with AGC -- 4.4 disqualifies it for a 10-35 ms single-pellet
    # occlusion gate. r7's BOM still ordered it. Deleted; the ANALOG receive
    # chain the doc actually specifies is listed instead.
    ("count PD x2", "Vishay VBPW34FAS (940 nm filtered PIN, 7.5 mm2)",
     "ELECTRONICS 4.4 ASSUMPTION -- replaces the REJECTED TSSP4038"),
    ("count amp", "TI OPA2320AIDR (dual, rail-to-rail, transimpedance)",
     "ELECTRONICS 4.4 ASSUMPTION"),
    ("count emitter x2", "Vishay TSAL6200 (940 nm, 34 deg)", "ASSUMPTION"),
    ("count windows x4", "Dia5.90 x 0.95 cast PMMA disc, sacrificial, bonded "
     "(UV-acrylic or CA)", "ECO-4; laser-cut, PN ASSUMPTION -- rev1 B4.4: "
     "order to the MODELLED size (window solids 5.900 x 0.950, seats at "
     "x=29.0/35.0) or the disc will not enter its seat; ELECTRONICS ECO-4 "
     "still says Dia6 x 1.0 and needs amending"),
    ("sensor-cover screws", "4x M2x6 self-tap into the boss ears",
     "ECO-12 retention (r7 ordered 2x M3 grubs for a hole that did not exist)"),
    ("Hall x2", "TI DRV5032FBDBZR", "ASSUMPTION"),
    ("MCU + CAN", "ST STM32G431KBT6 + TI TCAN332DR", "ASSUMPTION"),
    ("5 V buck", "Pololu D36V6F5 (12->5 V, 600 mA)", "ASSUMPTION"),
    ("magnets x9", "supermagnete S-03-02-N (Dia3x2, N45)", "ASSUMPTION"),
    ("inserts x6", "Ruthex RX-M3x5.7 heat-set", "ASSUMPTION"),
    ("spring plunger", "M5x0.8 ball-nose, LIGHT spring, 2.5 N end force, "
     "16 mm body (WDS 605 series class)", "PN ASSUMPTION -- end force is a "
     "specification; r6 A-11: threads into a modelled Dia4.5 x 13.5 mm "
     "thread-forming pilot, NOT an insert (no M5 insert is ordered)"),
    ("grommets x5", "Dia6.0 cable grommet for a 2.0 mm panel", "ECO-6 / N-i4 "
     "PN ASSUMPTION -- r1-r5 modelled the seats and ordered nothing"),
    ("bay gasket", "2.0 mm silicone cord, 200 mm (182.00 mm loop)",
     "N-i4 PN ASSUMPTION"),
    ("sensor pads x2", "18 x 12 x 0.5 mm silicone pad", "PN ASSUMPTION"),
    ("plastite x3", "Delta PT-class K30x8 thread-forming", "PN ASSUMPTION"),
    ("PTFE washer", "Dia%.0f OD / Dia%.0f ID x 1.4 virgin PTFE (Essentra "
     "class)" % (2 * WASH_RO, 2 * WASH_RI),
     "PN ASSUMPTION -- rev1 B9d: sized from WASH_RI/RO so this string cannot "
     "drift from the modelled washer again (the r12 string said Dia30/Dia24 "
     "x1.5, which sat on the Dia26-circle bolt holes and was 0.1 mm too "
     "thick for the seat)"),
    ("strip brush", "nylon mini strip brush, 1.6 mm backing, ~4 mm trim "
     "(Sealeze/Gordon Brush class)", "PN ASSUMPTION"),
    # rev1 B2.4: r7 stated this THREE different ways (COTS M2.5x4, fastener
    # table M3x4, model pilot Dia2.6 = M3 thread-forming). It is an M3, and
    # the string-equality check below asserts that the BOM says so.
    ("set screw", GRUB_SIZE + " hex socket cup-point grub (disc->shaft)",
     "M3 thread-forming into the modelled Dia%.1f pilot; close-out r13 "
     "(B2.2): pilot floor moved r=2.75 -> r=2.45, 0.10 mm inboard of the "
     "2.55 bore flat -- the r12 disc had a 0.200 mm closed CF-PETG web here "
     "and its grub could never touch the shaft; corridor now measured "
     "continuous (corridor check, anchored at the flat)" % (2 * GRUB_PILOT_R)),
    ("O-ring", "1.5 mm cord, Dia43.6 ID nitrile (fill cap gland)", "class"),
]
# =====================================================================
# REV-1 r6 CHECKS -- one block per round-5 critic BLOCKING/MAJOR finding.
# Each one prints WHAT A FAILING PART LOOKS LIKE (punch-list N14) using the
# r11 number the critic actually measured, so a pass cannot be a probe that
# missed.
# =====================================================================
print("\n============ REV-1 r6: ROUND-5 BLOCKING / MAJOR FINDINGS ============")

# --- A-11: the M5 detent plunger now has something to thread into ----
print("\nA-11 DETENT-PLUNGER BORE SECTION (assembly BLOCKING; r11 measured "
      "'Dia5.199 over r 47.00..52.90 and Dia6.399 over r 53.00..63.00, "
      "unthreaded' -> an M5x0.8 plunger drops straight through).")
_mhm = trimesh.load(os.path.join(EXPORT_DIR, f"meter_housing_{REV}.stl"))
_pa = math.radians(PLUNGER_A)
_ua = np.array([math.cos(_pa), math.sin(_pa), 0.0])
_up = np.array([-math.sin(_pa), math.cos(_pa), 0.0])
_ds = np.arange(0.0, 4.001, 0.05)
_prev = None
print("    r (mm)   void half-width (mm)   -> section")
for _r in np.arange(44.0, 64.001, 0.1):
    _c = _r * _ua + np.array([0.0, 0.0, PLUNGER_ZC])
    _pts3 = _c[None, :] + np.outer(_ds, _up)
    _in = _mhm.contains(_pts3)
    _hw = 0.0 if _in[0] else float(_ds[np.argmax(_in)] - 0.05
                                   if _in.any() else _ds[-1])
    _key = round(_hw, 2)
    if _key != _prev:
        print(f"    r={_r:6.2f}   half-width {_hw:5.3f}   -> "
              f"{'SOLID' if _hw <= 0.0 else 'Dia%.3f' % (2 * _hw)}")
        _prev = _key
print(f"    REQUIRED (B9c): a thread-forming pilot Dia4.2-4.6 +/- 0.1 over "
      f">= 6 mm. MODELLED: Dia{PLUNGER_PILOT_D:.1f} over "
      f"r {PLUNGER_NOSE_R1:.1f}..{PLUNGER_OUT_R:.1f} = "
      f"{PLUNGER_PILOT_L:.1f} mm, with a Dia{PLUNGER_NOSE_D:.1f} ball "
      f"clearance r {PLUNGER_NOSE_R0:.1f}..{PLUNGER_NOSE_R1:.1f}")
# insertion sweep: a Dia4.5 body (the pilot's own diameter) must reach its
# seat against EVERY other solid; the Dia5.0 MAJOR diameter's overlap with
# the pilot is the designed thread-forming interference and is printed too.
_plunger_body = Rot(Z=PLUNGER_A) * (
    Pos((PLUNGER_NOSE_R0 + PLUNGER_OUT_R) / 2, 0, PLUNGER_ZC) * Rot(Y=90)
    * Cylinder(PLUNGER_PILOT_D / 2, PLUNGER_OUT_R - PLUNGER_NOSE_R0))
_pl_obst = 0.0
for _dr in (0.0, 2.0, 5.0, 10.0, 20.0, 40.0):
    _sw = Rot(Z=PLUNGER_A) * (Pos(_dr, 0, 0) * (Rot(Z=-PLUNGER_A) * _plunger_body))
    for _k, _s in solids.items():
        if _k == "meter_housing":
            continue
        _pl_obst = max(_pl_obst, inter_vol(_sw, _s))
_maj = Rot(Z=PLUNGER_A) * (
    Pos((PLUNGER_NOSE_R1 + PLUNGER_OUT_R) / 2, 0, PLUNGER_ZC) * Rot(Y=90)
    * Cylinder(2.5, PLUNGER_PILOT_L))
_maj_int = inter_vol(_maj, solids["meter_housing"])
_maj_cf = math.pi / 4 * (5.0 ** 2 - PLUNGER_PILOT_D ** 2) * PLUNGER_PILOT_L
print(f"    insertion sweep, Dia{PLUNGER_PILOT_D:.1f} body pulled out to "
      f"+40 mm radially, vs EVERY other flight solid: {_pl_obst:.4f} mm3")
print(f"    designed thread-forming interference (Dia5.0 major in the "
      f"Dia{PLUNGER_PILOT_D:.1f} pilot over {PLUNGER_PILOT_L:.1f} mm): "
      f"measured {_maj_int:.4f} mm3 vs closed form {_maj_cf:.4f} mm3")
assert _pl_obst < 1e-6, "A-11: plunger cannot be installed"

# --- A-12: bay-rib screw pilot -- floor closed, tip inside the pilot --
print("\nA-12 BAY-RIB SCREW PILOT (assembly MAJOR; r11: the flat-bottomed "
      "pilot at y = -45.000 was OPEN 1.2492 mm2 of 4.5124 mm2 = 27.7 % into "
      "the metering chamber, 0.144 mm of floor where it was closed at all, "
      "and the BOM'd M3x20 tip landed 0.850 mm PAST the bore wall, 0.187 mm "
      "from the rotating disc).")
# The test is a CONTAINS probe 0.05 mm INBOARD of the flat bore floor, not a
# ray: a ray fired along the bore axis crosses the far chamber wall whether or
# not the floor is there, so it can never fail. Every raster is run twice --
# once at the r6 floor and once at r11's -45.000, which MUST come back open --
# so the probe is proved able to see the defect it is testing for.
_ras = np.arange(-1.25, 1.2501, 0.02)
_gxs, _gzs = np.meshgrid(_ras, _ras)
_m2 = (_gxs ** 2 + _gzs ** 2) <= 1.25 ** 2
_cell = 0.02 ** 2
_a12_open = 0.0
for _sx in (1, -1):
    _cx = _sx * 14.0
    for (_floor, _lbl) in ((BAY_RIB_PILOT_Y1, "r6 as built"),
                           (-45.0, "r11 CONTROL, must be OPEN")):
        _pts2 = np.column_stack([_cx + _gxs[_m2],
                                 np.full(int(_m2.sum()), _floor + 0.05),
                                 RIB_ZC + _gzs[_m2]])
        _openr = ~_mhm.contains(_pts2)
        if _floor == BAY_RIB_PILOT_Y1:
            _a12_open = max(_a12_open, float(_openr.sum()) * _cell)
        print(f"    pilot x={_cx:+.1f}, floor y={_floor:.3f} ({_lbl:<26s}): "
              f"OPEN {_openr.sum()*_cell:7.4f} mm2 of {_m2.sum()*_cell:.4f} "
              f"mm2 = {100.0*_openr.mean():5.1f} %")
assert _a12_open < 1e-6, "A-12: the pilot still breaks into the chamber"
# min material under the floor, and the M3x18 tip
_thk = []
for _sx in (1, -1):
    for _dx in np.arange(-1.25, 1.2501, 0.05):
        _xx = _sx * 14.0 + _dx
        if abs(_xx) < CHAMBER_R:
            _thk.append(abs(BAY_RIB_PILOT_Y1) - math.sqrt(
                max(CHAMBER_R ** 2 - _xx ** 2, 0.0)))
print(f"    material under the pilot floor across the whole bore section: "
      f"min {min(_thk):.3f} mm (r11: 0.144), at the chamber wall r="
      f"{CHAMBER_R:.1f}")
_tip_y = -64.0 + BAY_SCREW_L
print(f"    {BAY_SCREW} tip lands at y = {_tip_y:+.3f} vs pilot floor "
      f"{BAY_RIB_PILOT_Y1:+.3f} -> {_tip_y - BAY_RIB_PILOT_Y1:+.3f} mm of "
      f"clear pilot ahead of the tip (r11's M3x20 tip was at -44.000, i.e. "
      f"1.000 mm PAST the floor and 0.850 mm past the bore wall); the tip is "
      f"{abs(_tip_y) - math.sqrt(CHAMBER_R**2 - 14.0**2):.3f} mm of material "
      f"short of the chamber bore on its own axis (r11: -0.850)")
print(f"    RESIDUAL, stated: the thinnest material under the pilot floor is "
      f"{min(_thk):.3f} mm, at the point of the bore section NEAREST the "
      f"chamber axis. That is 8.8 x r11's 0.144 mm and the raster above says "
      f"0.0 % open, but it is still below the 1.95 mm the punch list uses for "
      f"insert bosses -- carried as an open issue, not claimed closed.")
assert _tip_y >= BAY_RIB_PILOT_Y1 - 1e-9, \
    "A-12: the bay screw tip is past the pilot floor"

# --- B4.2: beam clearance on the ECO-3 NOMINAL axes -------------------
print("\nB4.2 COUNT-BEAM CLEARANCE ON THE ECO-3 AXES (count-sensor critic: "
      "r11 read 1.1932 mm3 at x = 29.0/35.0 because the labyrinth stepped "
      "+0.800 on BOTH sides, walking the clear lens to x = 29.400/35.400):")
for (_bx, _bz) in BEAMS:
    _beam = Pos(_bx, 0, _bz) * Rot(X=90) * Cylinder(1.0, 60.0)
    _vp = inter_vol(_beam, solids["retaining_plate_chute"])
    _vc = inter_vol(_beam, aux_solids["sensor_cover"])
    _vw = inter_vol(_beam, aux_solids["count_windows"])
    # the OPTICAL path is emitter seating plane to detector seating plane,
    # |y| <= SENS_BOARD_Y0; the punch list's 60 mm cylinder runs 6.5 mm
    # further out each side, i.e. BEHIND both boards, where it meets the
    # cover's own locating ribs. Both numbers are printed.
    _opt = Pos(_bx, 0, _bz) * Rot(X=90) * Cylinder(1.0, 2 * SENS_BOARD_Y0)
    _op, _oc = (inter_vol(_opt, solids["retaining_plate_chute"]),
                inter_vol(_opt, aux_solids["sensor_cover"]))
    print(f"    beam x={_bx:.3f} z={_bz:.3f}  Dia2.0x60 ^ plate {_vp:8.4f} "
          f"| ^ cover {_vc:7.4f} | ^ PMMA windows (transparent) {_vw:7.4f} mm3")
    print(f"       optical span |y| <= {SENS_BOARD_Y0:.1f} (emitter seating "
          f"plane to detector seating plane): ^ plate {_op:.4f} | ^ cover "
          f"{_oc:.4f} mm3")
    assert _vp < 1e-6 and _op < 1e-6 and _oc < 1e-6, \
        "B4.2: the beam is obstructed"
_ctrl = Pos(SENS_BOSS_XC, 0, BEAMS[0][1]) * Rot(X=90) * Cylinder(1.0, 60.0)
print(f"    CONTROL, solid boss between the apertures x={SENS_BOSS_XC:.1f}: "
      f"{inter_vol(_ctrl, solids['retaining_plate_chute']):.4f} mm3 "
      f"(a probe that reads 0.0000 here is broken)")

print("\nCOTS PART NUMBERS (r6; ASSUMPTION until ordered/verified except stepper):")
for _n, _p, _s in COTS:
    print(f"  {_n:16s} {_p:62s} {_s}")

# =====================================================================
# BOM.md (r5, buildability PROCESS: "COTS part numbers live only as print
# statements inside cad/dispenser.py"). Generated from the model so it
# cannot drift from the geometry.
# =====================================================================
with open(os.path.join(HERE, "BOM.md"), "w") as fh:
    fh.write("# Capsule Dispenser -- BOM (auto-generated by cad/"
             "dispenser.py, rev %s)\n\n" % REV)
    fh.write("Masses of printed parts are MEASURED from the modeled solids at "
             "100%% infill (CF-PETG %.2f g/cm3, TPU %.2f). Do not edit by "
             "hand.\n\n## Printed parts\n\n" % (DENS["petg_cf"] * 1000,
                                                DENS["tpu"] * 1000))
    fh.write("| part | material | volume cm3 | mass g | best print orientation "
             "| support % |\n|---|---|---|---|---|---|\n")
    # rev1 B4.7: the r7 table had 10 rows and silently omitted the three
    # exported aux parts (count_windows, chute_plug, service_stand) -- and
    # sensor_cover did not exist. Every exported printed part is listed now,
    # with its quantity.
    _QTY = {"count_windows": 4, "sensor_cover": 2}
    for pname in PRINTED + PRINTED_AUX + ["count_windows"]:
        v = parts.get(pname) or aux[pname]
        mat = ("TPU" if pname in ("agitator", "chute_plug")
               else "PMMA" if pname == "count_windows" else "CF-PETG")
        st = SUPPORT.get(pname, (float("nan"), "?"))
        q = _QTY.get(pname, 1)
        fh.write(f"| {pname} (x{q}) | {mat} | {v['solid'].volume/1000:.2f} | "
                 f"{v['mass']:.1f} | {st[1]} | {st[0]:.1f} |\n")
    fh.write("\n### Required ground-support equipment (NOT flight mass)\n\n"
             "- **`service_stand` is mandatory GSE, not an accessory** (r4 "
             "integration critic). Refill (directive 4) is 'take the whole "
             "dispenser off the aircraft', and B12 closes **only** with this "
             "part in the field kit: without it the dispenser stands on its "
             "own gearbox output flange. Print one per field kit; it is "
             "excluded from the flight ledger on purpose.\n"
             "- `chute_plug` is ground-only storage kit (fitted between "
             "flights, removed before flight).\n\n"
             "## COTS / non-printed\n\n| item | part | status | mass g |\n"
             "|---|---|---|---|\n")
    # keys must match the COTS row NAMES exactly -- "stepper" here vs the
    # "geared stepper" row left the largest COTS mass blank in every BOM
    # through r12 (close-out B11.3 adjunct, found regenerating r13)
    _cots_mass = {"geared stepper": parts["stepper"]["mass"],
                  "sleeve bearing": parts["sleeve_bearing"]["mass"],
                  "PTFE washer": parts["thrust_washer"]["mass"],
                  "strip brush": parts["brush_bristles"]["mass"]}
    for _n, _p, _s in COTS:
        _m = _cots_mass.get(_n)
        fh.write(f"| {_n} | {_p} | {_s} | {('%.1f' % _m) if _m else ''} |\n")
    fh.write("\n## Fasteners (r6: the r5 BOM omitted these -- buildability "
             "MINOR 'quantities/lengths not orderable from the BOM')\n\n"
             "| qty | item | where |\n|---|---|---|\n"
             f"| 4 | {MOUNT_SCREW}x10 SHCS A2 | clip plate -> top plate "
             f"(+/-{BOLT_DX:.0f},+/-{BOLT_DY:.0f}) |\n"
             f"| 4 | Ruthex RX-M2x4 heat-set insert | top plate mount bosses |\n"
             "| 4 | M2x5 pan | blind-mate PCB -> clip-plate tabs |\n"
             f"| 6 | M3x10 SHCS + 6x Ruthex RX-M3x5.7 insert | top plate -> "
             f"hopper flange, 6 holes at r{FLANGE_SCREW_R:.3f} (r4 assembly "
             f"NB-2: the BOM said r72.25, the geometry has always been "
             f"r{FLANGE_SCREW_R:.3f}) |\n"
             f"| 3 | {SKIRT_SCREW} Delta-PT plastite | hopper skirt tabs -> "
             f"housing (r4: tab thickened to 4.05 mm -> grip "
             f"{SKIRT_R_OUT - HOUSING_R:.2f} mm, engagement "
             f"{SKIRT_SCREW_L - (SKIRT_R_OUT - HOUSING_R):.2f} mm in a "
             f"{HOUSING_R - (52.3 - SKIRT_PILOT_L):.2f} mm pilot) |\n"
             f"| 2 | {BAY_SCREW} SHCS | electronics bay ribs -> housing "
             f"(r4: r9's M3x12 gave 0.000 mm of engagement against a "
             f"{_grip:.2f} mm grip; this gives {_eng:.2f} mm) |\n"
             "| 4 | M3x8 self-tap | bay lid -> corner bosses |\n"
             "| 1 | M3x6 SHCS | wiper end tab -> housing pilot |\n"
             f"| 1 | M3x{LOCK_PIN_LEN:.0f} SHCS | cartridge STOP PIN, radial at theta "
             f"{LOCK_PIN_A:.0f} deg into a Dia2.6 thread-forming pilot "
             f"(r4: assembly NB-1 -- without it the cartridge has "
             f"25.03 deg of free rotation ending in the drop-out window) |\n"
             f"| 1 | {GRUB_SIZE} cup-point grub | disc hub -> gearbox shaft D-flat |\n"
             "| 4 | M2x6 self-tap | sensor covers -> boss ears (ECO-12) |\n"
             f"| 4 | **M3x8 ISO 10642 / DIN 7991 90 deg COUNTERSUNK**, 2.0 mm "
             f"hex | gearbox output flange -> retaining plate. r4 assembly "
             f"A-10 BLOCKING: the row used to say `M3x8 SHCS` and the plate "
             f"has a 90 deg countersink (mouth Dia6.10 at z=-351.250 closing "
             f"to Dia3.40 at -352.600) -- a Dia5.5x3.0 cap head stands 2.650 "
             f"mm proud of a 0.500 mm gap and jams the disc (measured: "
             f"8.8652 mm3/screw static, 49.4066 mm3/screw over one 45 deg "
             f"spoke pitch). Flush flat head measures 0.0000 mm3 at all four "
             f"holes and at every disc angle (measured this run: flat "
             f"{_a10_worst_flat:.4f} mm3 worst over the pitch, cap-head "
             f"control {_a10_worst_cap:.4f}). GRIP {_a10_grip:.3f} mm (head "
             f"seat plane to the gearbox flange face), thread beyond grip "
             f"{_a10_thread:.3f} mm -- do NOT lengthen the screw |\n"
             f"| 1 | **2.0 mm** hex key | gearbox countersunk screws (M3 ISO "
             f"10642 takes a 2.0 mm key) |\n"
             f"| 1 | **1.5 mm** hex key, >= 60 mm shaft | the {GRUB_SIZE} disc "
             f"grub. r6 (assembly MODERATE A-13): rounds 1-5 listed "
             f"ONE 2.0 mm key for both jobs, and 2.0 mm is the M4 size -- an "
             f"M3 hex-socket set screw (ISO 4026 / DIN 913-916) takes 1.5 mm, "
             f"so the shipped tool list could not build the machine. The grub "
             f"has to be pushed 43.00 mm radially down a Dia3.4 channel with "
             f"the disc indexed to theta=202.5 (assembly NB-7, rounds 1-5) |\n"
             f"| 1 | M5x0.8 ball-nose spring plunger, LIGHT (2.5 N), "
             f"{PLUNGER_BODY_L:.0f} mm body | cartridge detent. r6 (assembly "
             f"BLOCKING A-11): it now threads into a modelled "
             f"Dia{PLUNGER_PILOT_D:.1f} thread-forming pilot "
             f"{PLUNGER_PILOT_L:.1f} mm long (r 49.5..63.0), with a "
             f"Dia{PLUNGER_NOSE_D:.1f} ball clearance to the chamber wall. "
             f"r11 had a plain Dia5.199/Dia6.399 bore and NO M5 insert "
             f"anywhere in this file, so the plunger dropped through |\n"
             f"| 5 | Dia6.0 cable grommet, 2.0 mm panel | 3 x electronics-bay "
             f"entries + 2 x sensor-duct sockets (ECO-6). r6 (integration "
             f"N-i4): rounds 1-5 modelled the seats and ordered nothing, so "
             f"the 'dust-tight' bay was three open Dia10 holes |\n"
             f"| 1 | 2.0 mm silicone cord, 200 mm | electronics-bay lid "
             f"gasket, into the modelled 1.58 x 1.20 mm groove (182.00 mm "
             f"centreline loop). N-i4: also never ordered before |\n"
             f"| 2 | 18 x 12 x {SENS_PAD_T:.1f} mm silicone pad | between the "
             f"sensor-cover clamp posts and the board (count-sensor NIT: r11 "
             f"had a 0.0000 mm nominal tangency with no compliant element) |\n"
             "| 1 | 1.5 mm nitrile O-ring, ID 43.6 | fill-cap gland |\n"
             "| 9 | Dia3x2 N45 magnet | 8 pocket + 1 index |\n"
             "| 1 | 150 mm x Dia1.5 Dyneema cord + swage | chute-plug tether: "
             "plug eye Dia4.0 -> chute anchor lug Dia4.0 (r4: the plug is "
             "captive and hanging in sight below the chute mouth; it is a "
             "visibility+retention feature, NOT an interlock -- see "
             "BUILD-NOTES-r4 section 11 item 4) |\n"
             "| 2 | 18 x 12 x 2.0 mm 2-layer sensor PCB | count emitter board "
             "(+Y) and receiver board (-Y), ECO-12 |\n"
             "| 1 | UV-cure optical adhesive, 2 g | bonds the 4 PMMA windows "
             "into their bore-face seats (ECO-4) |\n")
    fh.write(f"\n## Rolled up\n\n"
             f"- **SHIPPED HEADLINE BASIS (B11.2): slicer-realistic, 4 "
             f"perimeters at 0.4 mm + 25 % infill, padded EDT -- LOADED @250 "
             f"pellets = {_sliced250:.1f} g against the 1500 g ceiling, margin "
             f"{1500 - _sliced250:+.0f} g.** This is what actually gets "
             f"printed. (r9's BOM rolled up only the 100 %-infill number and "
             f"the assembly critic correctly read it as 82.9 g over budget.)\n"
             f"- PESSIMISTIC BOUND, 100 % infill: empty (measured + "
             f"estimates) {total:.1f} g, +10% contingency -> {empty:.1f} g; "
             f"loaded @250 pellets {loaded250:.1f} g "
             f"({'under' if loaded250 <= 1500 else 'OVER'} the 1500 g "
             f"ceiling by {abs(1500 - loaded250):.0f} g). Nothing is printed "
             f"at 100 % infill; this is the bound, not the plan.\n"
             f"- loaded @{N_FILL_MAX} (max fill rib), 100 % infill basis: "
             f"{empty + N_FILL_MAX*PELLET_MASS:.1f} g\n"
             f"- usable hopper volume {v_use:.0f} cm3 -> {cap_worst} pellets "
             f"worst-case packing / {cap_sphere} sphere basis\n")
_bom = open(os.path.join(HERE, "BOM.md")).read()
_n_grub = _bom.count(GRUB_SIZE + " cup-point grub") + _bom.count(
    GRUB_SIZE + " hex socket cup-point grub")
print(f"B2.4 GRUB-SIZE STRING EQUALITY: BOM.md mentions '{GRUB_SIZE}' as the "
      f"disc grub {_n_grub} times; occurrences of any OTHER grub size "
      f"(M2.5/M4/M2): "
      f"{sum(_bom.count(x + ' cup-point') for x in ('M2.5', 'M4', 'M2'))}; "
      f"modelled pilot Dia{2*GRUB_PILOT_R:.1f}, clearance channel "
      f"Dia{2*GRUB_CLEAR_R:.1f}, key A/F {GRUB_KEY_AF:.1f}")
assert _n_grub == 2 and sum(
    _bom.count(x + " cup-point") for x in ("M2.5", "M4")) == 0, \
    "B2.4: BOM names more than one grub size"
print("BOM -> ", os.path.join(HERE, "BOM.md"))

# =====================================================================
# Renders (matplotlib painter's algorithm, cream background)
# =====================================================================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

CREAM = "#faf7f0"

import tempfile


def mesh_of(solid, tol=0.35):
    with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tf:
        tmp = tf.name
    export_stl(solid, tmp, tolerance=tol)
    m = trimesh.load(tmp)
    os.unlink(tmp)
    return np.asarray(m.vertices), np.asarray(m.faces)


def hex2rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i+2], 16) / 255 for i in (0, 2, 4)])


def render(sel, path, elev=22, azim=-60, cut=None, cut_only=None, zoom=1.0, title=""):
    tris_all, cols_all = [], []
    light = np.array([0.35, -0.5, 0.8])
    light = light / np.linalg.norm(light)
    for name in sel:
        s = parts[name]["solid"]
        if cut is not None and (cut_only is None or name in cut_only):
            s = s - cut
            if s is None or vol_of(s) < 1:
                continue
        v, f = mesh_of(s)
        base = hex2rgb(parts[name]["color"])
        tri = v[f]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        nn = np.linalg.norm(n, axis=1, keepdims=True)
        nn[nn == 0] = 1
        n = n / nn
        shade = 0.45 + 0.55 * np.clip(n @ light, 0, 1)
        cols = np.clip(base[None, :] * shade[:, None], 0, 1)
        tris_all.append(tri)
        cols_all.append(cols)
    T = np.concatenate(tris_all)
    C = np.concatenate(cols_all)
    e, a = math.radians(elev), math.radians(azim)
    view = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    depth = T.mean(axis=1) @ view
    order = np.argsort(depth)
    T, C = T[order], C[order]

    fig = plt.figure(figsize=(9, 9), dpi=140)
    fig.patch.set_facecolor(CREAM)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(CREAM)
    pc = Poly3DCollection(T, facecolors=C, edgecolors="none")
    ax.add_collection3d(pc)
    allv = T.reshape(-1, 3)
    c = (allv.max(0) + allv.min(0)) / 2
    r = (allv.max(0) - allv.min(0)).max() / 2 / zoom
    ax.set_xlim(c[0] - r, c[0] + r)
    ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_proj_type("ortho")
    ax.axis("off")
    if title:
        ax.set_title(title, color="#2b2b2b", fontsize=11, pad=0)
    fig.tight_layout()
    fig.savefig(path, facecolor=CREAM, bbox_inches="tight")
    plt.close(fig)
    print("render ->", path)


os.makedirs(RENDER_DIR, exist_ok=True)
ALL = list(parts.keys())
render(ALL, os.path.join(RENDER_DIR, "v1r6_iso.png"), elev=18, azim=-55,
       title="pocket-wheel granule dispenser — rev-1 r6 (r12): relieved reach-in neck, "
             "inverted-bayonet fill cap, sealed bay, reversed latch")
cutter = Pos(0, 250, -260) * Box(500, 500, 500)  # remove +Y half
render(ALL, os.path.join(RENDER_DIR, "v1r6_section.png"), elev=8, azim=90, cut=cutter,
       title="rev-1 r6 (r12) — section at Y=0: relieved neck + PCB well, fill cap\n"
             "inverted bayonet + face gland, 68° funnel, metering disc, chute")
METER = ["meter_housing", "pocket_disc", "agitator", "brush_holder",
         "brush_bristles", "retaining_plate_chute", "thrust_washer", "stepper",
         "sleeve_bearing"]
cutter2 = Pos(0, 250, Z_FUN_BOT) * Box(500, 500, 500)
render(METER, os.path.join(RENDER_DIR, "v1r6_detail.png"), elev=32, azim=135,
       cut=cutter2, cut_only={"meter_housing"},
       title="rev-1 r6 (r12) — meter detail: 25° entry ramp, 1.50 mm deflector nose,\n"
             "45° reverse-recovery ramp, mirrored latch slots + M3 stop pin")
render(ALL, os.path.join(RENDER_DIR, "v1r6_bottom.png"), elev=-28, azim=-40,
       title="rev-1 r6 (r12) — bottom: geared stepper, chute, deepened ECO-3 count\n"
             "bosses + covers, re-routed duct incl. the bay→motor branch")
FILLV = ["meter_housing", "pocket_disc", "agitator", "brush_holder",
         "brush_bristles", "sleeve_bearing"]
render(FILLV, os.path.join(RENDER_DIR, "v1r6_fill_station.png"), elev=62, azim=-90,
       title="rev-1 r6 (r12) — fill station: bristles lead, deflector nose trails")
# r5: the service state the r4 critic proved impossible -- cartridge dropped
CARTV = {"retaining_plate_chute", "pocket_disc", "stepper", "thrust_washer"}
serv = {}
for k, v in parts.items():
    s = copy.copy(v["solid"])
    if k in CARTV:
        s = Pos(0, 0, -60) * Rot(Z=CART_UNLOCK) * s
    serv[k] = dict(solid=s, color=v["color"], mass=v["mass"], basis="")
_orig, parts = parts, serv
render([k for k in parts if k not in ("hopper", "top_plate", "fill_cap",
                                      "clip_plate", "pcb_pedestal",
                                      "blindmate_pcb")],
       os.path.join(RENDER_DIR, "v1r6_cartridge_out.png"), elev=14, azim=-65,
       title="rev-1 r6 (r12) — cartridge dropped out at the −22° unlock angle")
parts = _orig
BAYV = ["meter_housing", "electronics_bay", "bay_lid", "retaining_plate_chute"]
render(BAYV, os.path.join(RENDER_DIR, "v1r6_bay_lid.png"), elev=12, azim=-115,
       title="rev-1 r6 (r12) — electronics bay: 46 mm lid aperture, gasket groove")
print("\ndone.")
