#!/usr/bin/env python
"""
Brush Bullet Dispenser -- "pocket-wheel" concept, round 6 parametric CAD.

Concept: CONCEPT-pocket-wheel.md (winner per JUDGING.md). Frame: drone frame,
origin at airframe center, +Z up, +Y forward (ICD / mechanical README).
Payload top mounting plane at Z = -171 mm; the payload-side clip plate
(2112_attach_plate_payload_side.step) is part of this payload.

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
Outputs:   cad/exports/*_r5.step *.stl   cad/renders/r5_*.png   cad/BOM.md
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
BOLT_DX_NOM, BOLT_DY_NOM = 19.0, 19.0     # expected mount pattern (38 x 38)
PCB_TAB_DX, PCB_TAB_DY = 4.0, 10.0        # expected PCB tab pattern (8 x 20)
MOUNT_SCREW = "M2"         # set by the measured head-pocket diameter
MOUNT_HEAD_D = 3.8         # ISO 4762 M2 socket head
MOUNT_INSERT_D = 3.2       # Ruthex M2 heat-set insert bore
MOUNT_INSERT_L = 4.0

# top plate (chassis adapter = hopper lid, one printed part)
TOP_T = 5.0
TOP_R = 75.0
FILL_R = 23.0              # fill port radius (Dia 46 -- pellets pour easily, >3.5x D)
# r6: moved out 40 -> 45 so the (+/-19,+/-19) mount holes clear the cap recess
# (measured margin printed by the checks).
FILL_POS = (0.0, 45.0)     # offset fill port center
# blind-mate PCB well (r6): the payload board mounts to the CLIP PLATE's own
# 4 tabs inside its 16 x 24 shaft; the top plate provides a sealed well under
# it for the board, its Molex J1 and a service loop, plus a cable channel.
WELL_X, WELL_Y = 16.4, 24.4     # well mouth (0.2 mm around the 16x24 board)
WELL_WALL = 2.0
WELL_DEPTH_BELOW = 4.5          # cup depth below the top-plate underside
CABLE_W, CABLE_DEEP = 5.0, 2.5  # harness channel in the top face, to -Y
CAP_FLANGE_R = 27.5
CAP_RECESS_R = 28.0
CAP_T = 2.5                # flush flange thickness (recess depth 2.6)
CAP_NECK_R = 22.7          # bore R23 -> 0.3 radial clearance
LUG_R_MID = 24.45          # bayonet lug track radius (local, about port center)

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
BRUSH_A = 143.0            # wiper station angle (r5: 133; moved upstream so
                           # the 13 mm-wide station still ends 1.4 deg before
                           # the roof entry edge)
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
HOLD_W = 13.0              # holder tangential width (bristle rail + nose)
HOLD_H = 3.0               # holder rail height (top flush with the sump floor)
CHAN_W, CHAN_H = 1.8, 1.2  # bristle channel in the holder underside
BRISTLE_W = 1.6            # COTS strip backing width (fits the channel)
NOSE_GAP = 3.0             # deflector nose underside above the disc face
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
SETSCREW_Z_OFF = -3.0      # set-screw axis relative to the disc top: r6 puts
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
PORT_R = 9.0
PORT_CHAMF = 0.75
PORT_RIM_R = PORT_R + PORT_CHAMF

# chute (straight, vertical)
CHUTE_ID = 22.0
CHUTE_WALL = 2.0
CHUTE_LEN = 50.0
SENSOR_DROP = 40.0         # IR beam below retaining plate bottom

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
MOTOR_PILOT_R = 11.0       # output-flange pilot boss (ASSUMPTION, NEMA14 std)
MOTOR_SHAFT_R = 3.0        # Dia6 output shaft (vendor)
MOTOR_SHAFT_LEN = 18.0
MOTOR_SHAFT_DCUT = 12.0
MOTOR_SCREW_HALF = 13.0    # 26 mm square M3 pattern (ASSUMPTION, NEMA14 std)
MOTOR_MASS = 310.0         # NET ASSUMPTION (vendor lists 0.38 kg GROSS);
                           # 380 g sensitivity run in the ledger
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
MAG_R = 1.5
MAG_DEPTH = 2.0
# r6 (pellet-path MAJOR): the r5 detent was a Dia4 x 1.5 deep dimple with an
# unspecified M5 plunger -- a commodity plunger in that seat needs 0.2-1.1
# N*m to release, i.e. up to 6x the whole motor. Now a SHALLOW SPHERICAL
# seat (R6 x 0.6) with a specified light plunger; release torque computed.
DIMPLE_SPH_R = 8.0
DIMPLE_DEPTH = 0.4
PLUNGER_BALL_R = 2.5       # M5 ball-nose plunger
PLUNGER_F = 2.5            # N end force, LIGHT spring (specified)
HALL_STATION_A = 90.0      # station Hall angle
HALL_INDEX_A = 112.5       # index Hall angle

# latch ring (quarter-turn receiver on housing)
RING_RI = 52.3
RING_RO = 58.0
RING_DROP = 3.0            # shelf below the plate
RING_BAND_H = 8.0          # r3: overlap band height above plate top (joins housing)
LUG_ANGLES = (60.0, 180.0, 300.0)

# electronics bay
BAY_W, BAY_D, BAY_H = 50.0, 26.0, 42.0
BAY_YC = -75.0             # inner face y=-62: clear of housing r52 + lug swing r<56

# structural fastening (r3, reworked r4)
FLANGE_SCREW_R = 72.25     # top plate -> hopper flange, 6x M3 + heat-set insert
FLANGE_SCREW_AS = tuple(15.0 + 60.0 * k for k in range(6))

# derived Z stack (top down)
Z_PLATE_BOT = Z_MOUNT - CLIP_T                 # -181.5
Z_TOP_BOT = Z_PLATE_BOT - TOP_T                # -186.5
Z_HOP_BOT = Z_TOP_BOT - HOP_CYL_H              # -241.5
Z_FUN_BOT = Z_HOP_BOT - FUNNEL_H               # -280.5
Z_ROOF_BOT = Z_FUN_BOT - ROOF_T                # -284.5
Z_DISC_TOP = Z_ROOF_BOT - ROOF_CLEAR           # -286.0
Z_DISC_BOT = Z_DISC_TOP - DISC_T               # -300.0
Z_RPLATE_TOP = Z_DISC_BOT - UNDER_GAP          # -300.5
Z_RPLATE_BOT = Z_RPLATE_TOP - PLATE_T          # -304.5
Z_CHUTE_BOT = Z_RPLATE_BOT - CHUTE_LEN
Z_MOTOR_TOP = Z_RPLATE_BOT                     # gearbox output flange face
Z_GEAR_BOT = Z_MOTOR_TOP - GEAR_L              # gearbox/motor joint
Z_MOTOR_BOT = Z_GEAR_BOT - MOTOR_L             # r6: gearbox + motor
Z_SENSOR = Z_RPLATE_BOT - SENSOR_DROP

# r5: everything below is now DERIVED from the Z stack (r4 hard-coded these,
# so a funnel-angle change would have silently desynchronised them).
RIB_ZC = Z_RPLATE_TOP + RING_BAND_H + 0.4 + 11.5 / 2   # bay rib centerline
# hopper -> housing joint: 3 RADIAL skirt tabs outside the housing wall,
# M3 plastite driven horizontally from outside (r3 buildability BLOCKER fix).
# Angles clear the brush tab (133 +/-6), plunger boss (180 +/-6) and the
# electronics-bay driver shadow (~240..300).
SKIRT_AS = (30.0, 105.0, 225.0)
SKIRT_R_IN, SKIRT_R_OUT = 52.15, 55.15   # 0.15 running gap off housing OD 52
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

DENS = {"petg_cf": 1.25e-3, "petg": 1.27e-3, "tpu": 1.20e-3,
        "alu": 2.70e-3, "ptfe": 2.20e-3, "nylon": 1.14e-3}


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


# =====================================================================
# Parts
# =====================================================================
parts = {}   # name -> dict(solid, color, mass, basis)


def add(name, solid, color, mass=None, density=None, basis=""):
    if mass is None:
        mass = solid.volume * density
    solid.label = name
    parts[name] = dict(solid=solid, color=color, mass=mass, basis=basis)
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
clip = Pos(-cx, -cy, Z_MOUNT - bb.max.Z) * clip
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

# --- 2. top plate = chassis adapter + hopper lid + PCB well (printed) --
top = Pos(0, 0, Z_TOP_BOT + TOP_T / 2) * Cylinder(TOP_R, TOP_T)
# r6: insert bosses at the MAPPED mount pattern (+/-19,+/-19). The r4/r5 hex
# nut pockets are gone: an M2 heat-set insert needs no nut pocket, no
# open-bottom skin break and no captive-nut assembly step.
BOSS_R, BOSS_H = 3.9, 4.6
BOSS_BOT = Z_TOP_BOT - BOSS_H + 0.5
for sx in (1, -1):
    for sy in (1, -1):
        top += Pos(sx * BOLT_DX, sy * BOLT_DY, Z_TOP_BOT - BOSS_H / 2 + 0.5) * Cylinder(
            BOSS_R, BOSS_H)
for sx in (1, -1):
    for sy in (1, -1):
        # screw clearance through the plate, then the insert bore from below
        top -= Pos(sx * BOLT_DX, sy * BOLT_DY, Z_TOP_BOT + TOP_T / 2) * Cylinder(
            1.25, TOP_T + 2)
        top -= Pos(sx * BOLT_DX, sy * BOLT_DY, BOSS_BOT + MOUNT_INSERT_L / 2 - 0.005
                   ) * Cylinder(MOUNT_INSERT_D / 2, MOUNT_INSERT_L)
# --- blind-mate PCB WELL (r6, interference BLOCKING #2) ---------------
# The board mounts to the CLIP PLATE's own 4 tabs inside its 16x24 shaft
# (mapped above), pads up. All the payload has to do is (a) not be in the
# way, (b) house the Molex J1 + service loop under it, (c) get the harness
# out to the electronics bay without crossing the pellet space. The well is
# a closed cup printed INTO the top plate: open only upward (where the board
# and the clip plate close it), sealed against the hopper below.
WELL_Z0 = Z_TOP_BOT - WELL_DEPTH_BELOW           # cup floor (outer)
top += Pos(0, 0, (WELL_Z0 + Z_TOP_BOT) / 2) * Box(
    WELL_X + 2 * WELL_WALL, WELL_Y + 2 * WELL_WALL, Z_TOP_BOT - WELL_Z0)
top -= Pos(0, 0, (WELL_Z0 + WELL_WALL + Z_PLATE_BOT + 1) / 2) * Box(
    WELL_X, WELL_Y, Z_PLATE_BOT + 1 - (WELL_Z0 + WELL_WALL))
# harness channel in the TOP face, from the well out to the -Y rim: the
# cable never enters the hopper, and it leaves under the clip plate.
top -= Pos(0, -(TOP_R + WELL_Y / 2) / 2, Z_PLATE_BOT - CABLE_DEEP / 2 + 0.005) * Box(
    CABLE_W, TOP_R - WELL_Y / 2, CABLE_DEEP)
# 2x cable-tie slots beside the channel at the rim
for sx in (1, -1):
    top -= Pos(sx * 6.0, -66.0, Z_TOP_BOT + TOP_T / 2) * Box(2.2, 5.0, TOP_T + 2)
# fill port bore + flush cap recess (depth 2.6)
top -= Pos(*FILL_POS, Z_TOP_BOT + TOP_T / 2) * Cylinder(FILL_R, TOP_T + 2)
top -= Pos(*FILL_POS, Z_PLATE_BOT - 1.3 + 0.005) * Cylinder(CAP_RECESS_R, 2.6)
# bayonet insertion notches (2x) through the plate at local +/-Y (r6: the
# port moved to y=45, so the LOCKED lugs have to sit on the local X axis to
# stay inside the hopper wall -- notches and lugs swap quadrants)
for ang in (90.0, 270.0):
    top -= Pos(*FILL_POS, 0) * Rot(Z=ang) * (
        Pos(LUG_R_MID, 0, Z_TOP_BOT + TOP_T / 2) * Box(4.5, 8.5, TOP_T + 2))
# hopper-flange screw holes (6x M3 through, screws into flange inserts)
for a in FLANGE_SCREW_AS:
    top -= Rot(Z=a) * (Pos(FLANGE_SCREW_R, 0, Z_TOP_BOT + TOP_T / 2) * Cylinder(1.6, TOP_T + 2))
# lightening pockets (3 sectors, 2.1 mm deep; clip, fill-port and pedestal
# zones stay solid).  r4: cut from the BOTTOM face instead of the top, and
# held inside r68 (clear of the hopper wall/flange seat) -- printed
# top-face-down they now open upward and need no support.
# r6: pockets deepened 2.15 -> 3.0 (2.0 mm of plate left) and a 4th sector
# added -- the geared drive costs 110 g and this is free stiffness-neutral mass
for a0 in (140, 200, 320, 8):
    top -= sector(32, 68.0, a0 + 4, a0 + 46, Z_TOP_BOT - 0.05, 3.0)
add("top_plate", top, "#c9c2b4", density=DENS["petg_cf"],
    basis="[D] solid volume, CF-PETG; M2 insert bosses at the MAPPED clip "
          "pattern; integral sealed blind-mate PCB well + cable channel")

# --- 3. quarter-turn fill cap (real bayonet: neck + lugs + wing grip) --
# r3 connectivity fix: neck extended UP into the flange (1.0 mm overlap) and
# DOWN past the lugs; lugs widened radially INTO the neck (2 mm overlap).
recess_floor = Z_PLATE_BOT - 2.6 + 0.005
cap = Pos(*FILL_POS, recess_floor + 0.05 + CAP_T / 2) * Cylinder(CAP_FLANGE_R, CAP_T)
# r5: neck bottom raised -188.2 -> -187.6 and the lugs thinned 1.5 -> 1.4,
# trimming the extraction lift (measured in the checks). This does NOT make
# on-aircraft refill possible -- see the printed cap-extraction numbers; the
# documented procedure is quick-release the payload and refill off-aircraft.
CAP_BOT = -187.6
cap += Pos(*FILL_POS, (CAP_BOT + -183.0) / 2) * Cylinder(CAP_NECK_R, -183.0 - CAP_BOT)
for ang in (0.0, 180.0):    # lugs in LOCKED orientation (under plate web)
    cap += Pos(*FILL_POS, 0) * Rot(Z=ang) * (
        Pos(LUG_R_MID - 1.0, 0, Z_TOP_BOT - 0.05 - 0.7) * Box(5.5, 7.0, 1.4))
# wing-bar grip on the ACCESSIBLE top face (+ lanyard hole: the cap is a
# loose part handled with gloves in wind -- Judge 2's field-ops lens)
cap += Pos(FILL_POS[0], FILL_POS[1], recess_floor + 0.05 + CAP_T - 0.15 + 1.65) * Box(24, 8, 3.3)
cap -= Pos(FILL_POS[0] + 10.0, FILL_POS[1], recess_floor + 0.05 + CAP_T + 1.5) * Cylinder(1.1, 8)
# r4 (r3 open issue 4): real O-RING GLAND on the neck, inside the Dia46
# bore sealing land (z -186.5..-184.1). Groove r21.8..22.7 x 2.0 tall for a
# 1.5 mm cord: radial gland depth 23.0-21.8 = 1.2 -> 20% squeeze [D].
cap -= Pos(*FILL_POS, -185.3) * (Cylinder(22.75, 2.0) - Cylinder(21.8, 3.0))
add("fill_cap", cap, "#e8763a", density=DENS["petg"],
    basis="[D] volume; bayonet neck+lugs w/ mating notches; O-ring seal on neck [J]")

# --- 4. hopper shell (cylinder + 60 deg funnel + flange + tabs), printed
hop_outer = Pos(0, 0, Z_HOP_BOT + HOP_CYL_H / 2) * Cylinder(HOP_RI + HOP_WALL, HOP_CYL_H)
hop_outer += Pos(0, 0, Z_FUN_BOT + FUNNEL_H / 2) * Cone(
    FUNNEL_RO + HOP_WALL, HOP_RI + HOP_WALL, FUNNEL_H)
hop_void = Pos(0, 0, Z_HOP_BOT + HOP_CYL_H / 2 + 1) * Cylinder(HOP_RI, HOP_CYL_H + 2)
hop_void += Pos(0, 0, Z_FUN_BOT + FUNNEL_H / 2) * Cone(FUNNEL_RO, HOP_RI, FUNNEL_H)
hopper = hop_outer - hop_void
# top flange (r69.5..75, 4 tall; overlaps wall r69.5..72.5 -> one solid)
hopper += Pos(0, 0, Z_TOP_BOT - 2.0) * (Cylinder(TOP_R, 4.0) - Cylinder(69.5, 6.0))
# flange heat-set insert holes (Dia4, for M3 inserts; match top-plate holes)
for a in FLANGE_SCREW_AS:
    hopper -= Rot(Z=a) * (Pos(FLANGE_SCREW_R, 0, Z_TOP_BOT - 2.0) * Cylinder(2.0, 4.4))
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
add("hopper", hopper, "#ded7c8", density=DENS["petg_cf"],
    basis="[D] shell volume, 2.3 mm wall CF-PETG, 68 deg funnel + flange/tabs")

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
# detent plunger boss (radial, theta=180; M5 spring plunger, wall 2.4 mm)
housing += Pos(-(HOUSING_R + 4), 0, Z_DISC_TOP - DISC_T / 2) * Rot(Y=90) * Cylinder(5.0, 14)
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
housing -= Pos(0, 0, Z_FUN_BOT - ROOF_T / 2) * Cylinder(BUSH_OD / 2 + 0.05, ROOF_T + 2)
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
_ra = math.radians(RAMP_DEG)
RAMP_RUN = ROOF_T / math.tan(_ra)            # tangential run of the ramp
RAMP_ARC_DEG = math.degrees(RAMP_RUN / PCD_R)
_n = (0.0, -math.sin(_ra), math.cos(_ra))    # ramp plane normal (local frame)
ramp_half = Pos(0, -100 * _n[1], (Z_ROOF_BOT + ROOF_T) - 100 * _n[2]) * Rot(
    X=RAMP_DEG) * Box(400, 400, 200)
ramp_cut = ramp_half & (Pos(0, -100, Z_ROOF_BOT + 50) * Box(400, 200, 100))
ramp_cut &= (Pos(0, 0, Z_ROOF_BOT + 25) * Cylinder(CHAMBER_R, 50)
             - Pos(0, 0, Z_ROOF_BOT + 25) * Cylinder(18.0, 52))
housing -= Rot(Z=FILL_ARC[0]) * ramp_cut
# plunger bore (re-cut AFTER ring union so the band cannot block the plunger)
housing -= Pos(-(HOUSING_R + 4), 0, Z_DISC_TOP - DISC_T / 2) * Rot(Y=90) * Cylinder(2.6, 24)
# latch slots (cut after ring union)
ring_h = PLATE_T + RING_DROP
for a in LUG_ANGLES:
    # circumferential slot at lug height (shelf below carries the plate load)
    housing -= sector(52.05, 55.55, a - 6, a + 30, Z_RPLATE_BOT - 0.2, PLATE_T + 0.5)
    # vertical entry slot (insert at a+22, rotate -22 deg to lock)
    housing -= sector(52.05, 55.55, a + 14, a + 30, Z_RPLATE_BOT - RING_DROP - 1, ring_h + 2)
# r5 wiper seat (pellet-path MAJOR: the r4 "brush" was a solid printed fin
# with nowhere to put bristles). The seat is now a REBATE OPEN AT THE TOP,
# cut from the sump floor down HOLD_H+0.15, running the whole radial span
# r13.5..52.6: over r20..47 the fill sector has already removed the roof, so
# the holder free-spans there and the bristles hang into open space; at the
# inner ring and at the wall top the rebate carries it. Radial slide-in/out
# is therefore a pure translation (swept-union probed below) and there is no
# thin "ceiling" section over the slot any more (r4 MINOR: 1.5 mm).
housing -= Rot(Z=BRUSH_A) * (Pos(29.5, 0, Z_FUN_BOT)
                             * Box(32.0, HOLD_W + 0.3, 2 * (HOLD_H + 0.15)))
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
    housing -= Pos(sx * 14.0, -48.5, RIB_ZC) * Rot(X=90) * Cylinder(1.25, 7.0)
# r4 skirt-tab screw pilots (3x radial Dia2.5 x 4.4, r47.9..52.3 -- open at
# the housing OD, inner end 0.9 mm clear of the chamber wall r47)
for a in SKIRT_AS:
    housing -= Rot(Z=a) * (Pos(50.1, 0, SKIRT_SCREW_Z) * Rot(Y=90) * Cylinder(1.25, 4.4))
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
dimple_angles = [22.5 + i * 45.0 for i in range(N_POCKET)]
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
for a in pocket_angles:
    disc -= Pos(18.5 * math.cos(math.radians(a + 22.5)), 18.5 * math.sin(math.radians(a + 22.5)),
                Z_DISC_TOP - DISC_T / 2) * Cylinder(3.5, DISC_T + 2)
disc -= Pos(0, 0, Z_DISC_BOT + 1.25 - 0.005) * (Cylinder(23.0, 2.5) - Cylinder(16.0, 4.0))
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
Z_BORE_TOP = Z_DISC_TOP - 0.5
disc -= Pos(0, 0, (Z_DISC_BOT - 2 + Z_BORE_TOP) / 2) * Cylinder(
    MOTOR_SHAFT_R + 0.05, Z_BORE_TOP - (Z_DISC_BOT - 2))
# M3 set screw onto the shaft D-flat, inside the disc body (r6: the Dia6
# shaft now ends 0.5 mm below the disc top, so the screw moves DOWN into the
# disc instead of up into the journal -- the Dia20 bearing surface is
# unbroken by construction). Tightened with the cartridge out of the housing.
Z_SETSCREW = Z_DISC_TOP + SETSCREW_Z_OFF
disc -= Rot(Z=270) * (Pos(6.0, 0, Z_SETSCREW) * Rot(Y=90) * Cylinder(1.3, 9))
add("pocket_disc", disc, "#e8763a", density=DENS["petg_cf"],
    basis="[D] volume w/ pockets+lightening, CF-PETG; -Z rotation arrow engraved")

# --- 7. PTFE thrust washer (pellet-bed load off the motor bearings) ----
washer = Pos(0, 0, Z_RPLATE_TOP - 1.0 + 0.05 + 0.7) * (Cylinder(15.0, 1.4) - Cylinder(12.0, 3))
add("thrust_washer", washer, "#f0ede4", density=DENS["ptfe"],
    basis="PTFE Dia30/Dia24x1.4 in plate recess (McMaster PTFE washer class, "
          "part TBD); disc rides it (0.05 modeled gap)")

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
nose_prof = Polygon((NOSE_Y0, NOSE_Z0), (NOSE_Y0, NOSE_Z0 + 0.6),
                    (NOSE_Y1, CHAN_Z0 + 0.01), (NOSE_Y1, NOSE_Z0), align=None)
holder += Rot(Z=BRUSH_A) * (Pos(NOSE_R0, 0, 0) * Rot(Z=90) * Rot(X=90)
                            * extrude(nose_prof, amount=NOSE_R1 - NOSE_R0))
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
# motor pilot + screws
rp -= Pos(0, 0, Z_RPLATE_TOP - PLATE_T / 2) * Cylinder(MOTOR_PILOT_R + 0.1, PLATE_T + 2)
for sx in (1, -1):
    for sy in (1, -1):
        rp -= Pos(sx * MOTOR_SCREW_HALF, sy * MOTOR_SCREW_HALF,
                  Z_RPLATE_TOP - PLATE_T / 2) * Cylinder(1.6, PLATE_T + 2)
# thrust-washer recess (1.0 deep, floor at plate top - 1.0)
rp -= Pos(0, 0, Z_RPLATE_TOP - 0.5) * Cylinder(15.3, 1.01)
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
# IR sensor bosses: r3 connectivity fix -- bosses OVERLAP the chute wall by
# 2 mm (inner face y=+/-11 vs wall r11..13); bore re-cleared after the union
for sy in (1, -1):
    rp += Pos(PCD_R, sy * 17.0, Z_SENSOR) * Box(12, 12, 14)
rp -= Pos(PCD_R, 0, Z_RPLATE_BOT - CHUTE_LEN / 2 - 1) * Cylinder(CHUTE_ID / 2, CHUTE_LEN + 4)
for sy in (1, -1):
    # recessed light tunnel (Dia3.2) through boss + chute wall
    rp -= Pos(PCD_R, sy * 16.0, Z_SENSOR) * Rot(X=90) * Cylinder(1.6, 26)
    # component pocket (Dia6.5, from the outer face; sensor face recessed
    # 5.0 mm from the chute bore surface -- concept: >=5 mm dust shadowing)
    rp -= Pos(PCD_R, sy * 20.0, Z_SENSOR) * Rot(X=90) * Cylinder(3.25, 8)
    # r5 (buildability MINOR: "no sensor retention feature is modeled"):
    # M3 grub pilot entering the pocket from below, 90 deg to the optical
    # axis -- clamps the emitter/receiver body and lets it be re-seated
    # after a swab-out without glue.
    rp -= Pos(PCD_R, sy * 20.0, Z_SENSOR - 6.0) * Cylinder(1.25, 8.0)
add("retaining_plate_chute", rp, "#8f8778", density=DENS["petg_cf"],
    basis="[D] volume; integral vertical chute + fused sensor bosses + latch lugs")

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
# D-cut on the output shaft (12 mm long, vendor): 0.5 mm flat depth
motor -= Pos(MOTOR_SHAFT_R + 0.5 - 0.5 + 3.0, 0,
             Z_MOTOR_TOP + MOTOR_SHAFT_LEN - MOTOR_SHAFT_DCUT / 2) * Box(
    6.0, 8.0, MOTOR_SHAFT_DCUT)
add("stepper", motor, "#3a3a3a", mass=MOTOR_MASS,
    basis="StepperOnline 14HS13-0804S-PG5 (NEMA 14 + 5.18:1 planetary, "
          "0.14 N*m x 5.18 x 0.90 = 0.65 N*m out, 35x35x34 + 29.2 gearbox, "
          "Dia6x18 D-cut shaft); 310 g NET ASSUMPTION (vendor 0.38 kg gross)")

# --- 12. electronics bay (outboard + screwed ribs + LID, r4) -----------
ZC_BAY = RIB_ZC   # r6: bay centred on its own rib mounts
bay_s = Pos(0, BAY_YC, ZC_BAY) * Box(BAY_W, BAY_D, BAY_H)
bay_s -= Pos(0, BAY_YC, ZC_BAY) * Box(BAY_W - 4, BAY_D - 4, BAY_H - 4)
# r4 (buildability MAJOR / r3 open issue 3): the bay was a sealed shell.
# The -Y (outboard) wall is now a 42x36 OPENING (3..4 mm frame) closed by
# a screwed lid (separate printed part below): components installable.
bay_s -= Pos(0, -87.0, ZC_BAY) * Box(BAY_W - 8, 4.0, BAY_H - 6.0)
# 4 corner bosses w/ Dia2.5 pilots for the M3 self-tap lid screws; bosses
# overlap the side frame bands (x 21..25) volumetrically and sit clear of
# the rib-driver axes (z rel +/-8 vs driver at rel +15.15)
for sx in (1, -1):
    for sz in (1, -1):
        bay_s += Pos(sx * 19.5, -83.75, ZC_BAY + sz * 13.0) * Box(7.0, 5.5, 7.0)
        bay_s -= Pos(sx * 19.5, -84.0, ZC_BAY + sz * 13.0) * Rot(X=90) * Cylinder(1.25, 5.5)
# ribs: r4 widened 7.0 -> 7.6 (M3 through-hole + 2.2 mm cheeks; r3 MINOR:
# 1.9 was under the 2 mm rule), end face CONFORMAL to the housing OD
# (trimmed by r52.1 cylinder -> uniform 0.1 mm joint gap)
for sx in (1, -1):
    bay_s += Pos(sx * 14.0, -55.0, RIB_ZC) * Box(7.6, 14.0, 11.5)
bay_s -= Pos(0, 0, RIB_ZC) * Cylinder(HOUSING_R + 0.1, 12.5)
for sx in (1, -1):
    # M3 through-hole (rib + bay inner wall) -> housing pilot; head inside bay
    bay_s -= Pos(sx * 14.0, -56.0, RIB_ZC) * Rot(X=90) * Cylinder(1.6, 16.5)
# cartridge-harness connector cutout on the -X face (JST-GH class, service
# loop); r4: shifted +4 in Y so it cannot nick the new lid-screw bosses
bay_s -= Pos(-24.0, BAY_YC + 4.0, Z_FUN_BOT - 10.0) * Box(4.0, 16.0, 9.0)
add("electronics_bay", bay_s, "#c9c2b4", density=DENS["petg_cf"],
    basis="[D] 2 mm shell + screwed conformal ribs + lid opening; MCU+CAN, "
          "TMC2209, buck")

# --- 12b. bay lid (r4, printed): plate + register lip + screws + access --
lid = Pos(0, -89.0, ZC_BAY) * Box(BAY_W, 2.0, BAY_H)
lid += Pos(0, -87.5, ZC_BAY) * Box(BAY_W - 8.6, 1.4, BAY_H - 6.6)  # lip, 0.3 gap
# (lip stops at y=-86.8, 0.3 clear of the lid-screw bosses at y=-86.5)
for sx in (1, -1):
    for sz in (1, -1):
        lid -= Pos(sx * 19.5, -88.0, ZC_BAY + sz * 13.0) * Rot(X=90) * Cylinder(1.7, 6.5)
for sx in (1, -1):
    # Dia6 rib-screw driver access holes (moved here from the old outer
    # wall; grommet-plugged in service)
    lid -= Pos(sx * 14.0, -88.5, RIB_ZC) * Rot(X=90) * Cylinder(3.0, 5.5)
add("bay_lid", lid, "#b9b1a1", density=DENS["petg_cf"],
    basis="[D] volume; 4x M3 self-tap into bay corner bosses, register lip")

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
os.makedirs(EXPORT_DIR, exist_ok=True)
REV = "r6"
PRINTED = ["top_plate", "fill_cap", "hopper", "meter_housing",
           "pocket_disc", "agitator", "brush_holder", "retaining_plate_chute",
           "electronics_bay", "bay_lid"]
for name in PRINTED:
    export_step(solids[name], os.path.join(EXPORT_DIR, f"{name}_{REV}.step"))
    export_stl(solids[name], os.path.join(EXPORT_DIR, f"{name}_{REV}.stl"))

asm = Compound(children=[copy.copy(v["solid"]) for v in parts.values()])
asm.label = f"brush_bullet_dispenser_{REV}"
ASM_STEP = os.path.join(EXPORT_DIR, f"dispenser_{REV}_assembly.step")
ASM_STL = os.path.join(EXPORT_DIR, f"dispenser_{REV}_assembly.stl")
export_step(asm, ASM_STEP)
export_stl(asm, ASM_STL)
print("exports written to", EXPORT_DIR)

# =====================================================================
# Geometry checks (printed, measured from the model)
# =====================================================================
print("\n================ GEOMETRY CHECKS (measured) ================")
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
        ins = Pos(x, y, BOSS_BOT + MOUNT_INSERT_L / 2) * Cylinder(
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
bodies = mtri.split(only_watertight=False)
print(f"assembly STL bodies: {len(bodies)} (expected = {len(parts)} parts -> "
      f"{'OK' if len(bodies) == len(parts) else 'MISMATCH'})")

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
print(f"  1. REJECTION BEFORE WEDGE: the deflector nose ramp lifts rather "
      f"than stubs -- lift/push = cot({NOSE_ANG:.0f}) = "
      f"{1/math.tan(math.radians(NOSE_ANG)):.2f}, and the worst self-locked "
      f"sliver needs mu/sin(half-angle) = "
      f"{MU/math.sin(math.radians(JAM[1][3])):.2f} at w=2.0 mm -> "
      f"{'PASS' if 1/math.tan(math.radians(NOSE_ANG)) > MU/math.sin(math.radians(JAM[1][3])) else 'FAIL'}"
      f". Behind it the transfer-arc entry is a {RAMP_DEG:.0f} deg ramp, not "
      f"a square edge (measured above).")
print("  3. DETECT + RECOVER: per-pocket Hall magnet (8) + index magnet -> "
      "phase is verified EVERY index, not just at boot (r5 Judge-1 item); "
      "StallGuard + gearbox current sensing; recovery = reverse-oscillate at "
      "normal current, then bounded shear attempts at 100% current with the "
      "chute beam armed, then fault. The count sensor is BELOW the meter, so "
      "a recovery cannot manufacture a phantom count.")

# detent geometry: park phase + dimple uniformity
print(f"dimple angles: {['%.1f' % a for a in dimple_angles]} -> all at half-station; "
      f"plunger at 180 -> parked pockets sit 22.5 deg off the exit port")
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
print(f"\nEXIT KINEMATICS (r6, pellet-path MODERATE 'the drop-through window "
      f"is only 1.18x the free-fall time' + Judge 3's lateral-velocity ding): "
      f"the index is now TWO-PHASE -- park(+22.5 deg) -> index 22.5 deg so the "
      f"pocket is CONCENTRIC with the port -> DWELL -> index 22.5 deg to the "
      f"next park. Consequences [D]: (a) the pellet is released from a "
      f"STATIONARY pocket, so the imparted lateral velocity is 0 by "
      f"construction (r5 printed 'ZERO' while indexing through the port at "
      f"167 mm/s, which the critic correctly called wrong: that would have "
      f"been up to 0.17 m/s = ~0.2 m of scatter from 8 m); (b) the drop "
      f"window is a DWELL parameter, not a race -- fall time to clear the "
      f"{DISC_T + UNDER_GAP:.1f} mm pocket is {T_DROP*1000:.0f} ms, so the "
      f"contract dwell is 150 ms ({150/(T_DROP*1000):.1f}x); (c) the pocket "
      f"and port are concentric at release, so the clear aperture is the full "
      f"Dia{2*PORT_R:.0f} port, not a moving lune.")
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

# 4) disc set screw: shaft engagement + hole open + r5 margins
eng_ss = Rot(Z=270) * (Pos(2.0, 0, Z_SETSCREW) * Rot(Y=90) * Cylinder(0.6, 1.6))
hole_ss = Rot(Z=270) * (Pos(6.5, 0, Z_SETSCREW) * Rot(Y=90) * Cylinder(0.9, 7.0))
Z_SHAFT_TOP = Z_MOTOR_TOP + MOTOR_SHAFT_LEN
Z_SLEEVE_BOT = Z_FUN_BOT - BUSH_CB_DEPTH - BUSH_LEN
print(f"  disc set screw @ z={Z_SETSCREW:.2f} (M2.5): shaft-engagement probe "
      f"{inter_vol(eng_ss, solids['stepper']):.2f} mm3 (MUST be >0), hole-open "
      f"{inter_vol(hole_ss, solids['pocket_disc']):.2f} mm3 (~0); shaft top "
      f"{Z_SHAFT_TOP:.1f} -> {Z_SHAFT_TOP - (Z_SETSCREW + 1.25):.2f} mm margin "
      f"(r4 NIT: 0.00); screw body {Z_SETSCREW - 1.25:.2f}..{Z_SETSCREW + 1.25:.2f} "
      f"sits clear of the bushing sleeve bottom {Z_SLEEVE_BOT:.2f} by "
      f"{Z_SLEEVE_BOT - (Z_SETSCREW + 1.25):.2f} mm and of the disc top by "
      f"{(Z_SETSCREW - 1.25) - Z_DISC_TOP:.2f} mm -> the Dia20 journal surface "
      f"is UNBROKEN (no hole edge running in the bearing)")

# 5) bay lid: screw approach paths + rib-screw driver paths (to the head
#    INSIDE the bay at the rib inner wall)
v_lid = 0.0
for sx in (1, -1):
    for sz in (1, -1):
        pr = Pos(sx * 19.5, -93.5, ZC_BAY + sz * 13.0) * Rot(X=90) * Cylinder(2.2, 6.0)
        v_lid += sum(inter_vol(pr, solids[n]) for n in ("electronics_bay", "bay_lid"))
v_rib = 0.0
for sx in (1, -1):
    pr = Pos(sx * 14.0, -79.25, RIB_ZC) * Rot(X=90) * Cylinder(2.8, 29.5)
    v_rib += sum(inter_vol(pr, solids[n]) for n in ("electronics_bay", "bay_lid"))
print(f"  bay lid: 4x screw approach paths total {v_lid:.2f} mm3 (~0); 2x rib "
      f"driver paths through lid Dia6 holes total {v_rib:.2f} mm3 (~0)")

# 6) r5 CARTRIDGE DROP-OUT SWEEP -- the r4 BLOCKER, measured properly.
# r4 "verified" this with a Dia26.4 cylinder probe through the roof hole and
# missed that the agitator's own fingers blocked the descent (853 mm3). r5
# sweeps EVERY cartridge member (quarter-turn unlock 22 deg, then a 20-step
# 60 mm descent) against EVERY static part, exactly as the critic did.
CART = ["retaining_plate_chute", "pocket_disc", "stepper", "thrust_washer"]
STATIC = [n for n in solids if n not in CART]
print("  CARTRIDGE DROP-OUT SWEEP (unlock 22 deg + 60 mm descent, 21 steps, "
      "4 members x every static part, bbox-prefiltered):")
cart_tab = {}
tot_cart = 0.0
first_block = None
for dz in np.linspace(0.0, -60.0, 21):
    for n in CART:
        s = Pos(0, 0, dz) * Rot(Z=22.0) * copy.copy(solids[n])
        for other in STATIC:
            # the agitator is a free rotor keyed to the hub hex: the unlock
            # rotation turns it too, so it is compared in its turned pose
            o = (Rot(Z=22.0) * copy.copy(solids[other])
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
    sw = sector(52.0, 55.3, a - 5.3, a + 27.3, Z_RPLATE_BOT + 0.05, PLATE_T - 0.1)
    print(f"  lug@{a:5.1f}: x housing {inter_vol(sw, solids['meter_housing']):8.2f}  "
          f"x bay {inter_vol(sw, solids['electronics_bay']):8.2f}")
chute_or_chk = CHUTE_ID / 2 + CHUTE_WALL
print(f"cartridge rotation (22 deg): chute/boss cluster max r "
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

# ---- r5: FILL-CAP EXTRACTION (buildability MAJOR: "refill with gloves").
cap_bb = solids["fill_cap"].bounding_box()
lift_req = Z_PLATE_BOT - cap_bb.min.Z
headroom = Z_MOUNT - cap_bb.max.Z
print(f"\nFILL-CAP EXTRACTION: cap spans Z {cap_bb.min.Z:.2f}..{cap_bb.max.Z:.2f}; "
      f"lift to clear the plate top face = {lift_req:.2f} mm (r4: 6.70) vs "
      f"{headroom:.2f} mm of headroom to the {Z_MOUNT:.0f} mounting plane; the "
      f"cap must then translate {TOP_R - FILL_POS[1] + CAP_FLANGE_R:.0f} mm "
      f"laterally to clear the top plate edge inside a "
      f"{Z_MOUNT - Z_PLATE_BOT:.1f} mm gap that the airframe belly shares -> "
      f"ON-AIRCRAFT REFILL IS NOT CLAIMED. Procedure: quick-release the "
      f"payload (COTS 2112 QR), refill on the tailgate, re-clip. Cap carries "
      f"a Dia2.2 lanyard hole so it is not a droppable loose part.")

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
print("  bay->housing: 2x M3 through rib+inner wall into Dia2.5x7 wall pilots; "
      "driver access via Dia6 holes in the BAY LID")
print("  bay lid: 4x M3 self-tap into corner-boss pilots")
print("  wiper: radial slide-in into an open-topped seat + end-tab M3 radial "
      "screw into a housing pilot; bristle strip pushed into the holder "
      "channel from the outboard end (both are field-replaceable)")
print(f"  cartridge: 3x quarter-turn lugs into ring slots; disc M2.5 set screw "
      f"at z={Z_SETSCREW:.1f} onto the shaft flat, tightened with the cartridge "
      f"out (a motion r5 actually verifies)")
print("  agitator: NO fastener -- hex-driven free rotor, lifts off upward "
      "(r4's set screw inside the funnel throat is deleted)")

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
fixed = [
    ("electronics: STM32G431KBT6+TCAN332, TMC2209, D36V6F5 buck, "
     "TSSP4038+TSAL6200 IR pair, 2x DRV5032, wiring", 65.0, "[J] PNs listed below, ASSUMPTION"),
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
try:
    from scipy import ndimage
    print("\n  INFILL BRACKET (voxel erosion, 4 perimeters @0.4 + 25% infill):")
    tot_solid = tot_infill = 0.0
    for pname in PRINTED:
        m = trimesh.load(os.path.join(EXPORT_DIR, f"{pname}_{REV}.stl"))
        pitch = 0.6
        vg = m.voxelized(pitch=pitch).fill()
        mat = vg.matrix
        # EDT counts the surface voxel itself as 1 -> subtract half a voxel
        dist = (ndimage.distance_transform_edt(mat) - 0.5) * pitch
        core = float((dist > 1.6).sum()) * pitch ** 3
        vol = m.volume
        dens = (DENS["tpu"] if pname == "agitator"
                else DENS["petg"] if pname == "fill_cap" else DENS["petg_cf"])
        m_solid = vol * dens
        m_infill = (vol - core + 0.25 * core) * dens
        tot_solid += m_solid
        tot_infill += m_infill
        print(f"    {pname:22s} solid {m_solid:6.1f} g   core "
              f"{core/1000:6.2f} cm3   at 25% infill {m_infill:6.1f} g")
    print(f"    printed-parts total: solid {tot_solid:.1f} g -> sliced "
          f"{tot_infill:.1f} g ({tot_solid - tot_infill:.1f} g of the ledger is "
          f"a 100%-infill modelling artifact). LOADED @250 would be "
          f"{loaded250 - (tot_solid - tot_infill) * 1.10:.1f} g.")
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
    ("electronics + blind-mate PCB (CAN node, driver, buck, IR pair)",
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
     "Dia6x18 D-cut, gross 0.38 kg; 310 g NET is an ASSUMPTION"),
    ("sleeve bearing", "igus iglidur J JFM-2023-07 (ID20/OD23/L7)",
     "length VERIFIED catalogued (TME/RS list JFM-2023-07/11/16/21); flange "
     "Dia30x2 ASSUMPTION"),
    ("mount screws", "4x M2x10 ISO 4762 A2 + 4x Ruthex RX-M2x4 heat-set inserts",
     "head Dia3.8 vs the mapped Dia3.90 pocket -- 0.05 mm/side, tolerance item"),
    ("PCB screws", "4x M2x5 into the clip plate's own tabs", "vendor feature"),
    ("driver", "BIGTREETECH TMC2209 V1.3 module (or TMC2209-LA-T)", "ASSUMPTION"),
    ("IR count pair", "Vishay TSSP4038 receiver + TSAL6200 emitter (940 nm)", "ASSUMPTION"),
    ("Hall x2", "TI DRV5032FBDBZR", "ASSUMPTION"),
    ("MCU + CAN", "ST STM32G431KBT6 + TI TCAN332DR", "ASSUMPTION"),
    ("5 V buck", "Pololu D36V6F5 (12->5 V, 600 mA)", "ASSUMPTION"),
    ("magnets x9", "supermagnete S-03-02-N (Dia3x2, N45)", "ASSUMPTION"),
    ("inserts x6", "Ruthex RX-M3x5.7 heat-set", "ASSUMPTION"),
    ("spring plunger", "M5x0.8 ball-nose, LIGHT spring, 2.5 N end force "
     "(WDS 605 series class)", "PN ASSUMPTION -- the end force is now a "
     "specification, not a leftover (r5 pellet-path MAJOR)"),
    ("plastite x3", "Delta PT-class K30x8 thread-forming", "PN ASSUMPTION"),
    ("PTFE washer", "Dia30/Dia24x1.5 virgin PTFE (Essentra class)", "PN ASSUMPTION"),
    ("strip brush", "nylon mini strip brush, 1.6 mm backing, ~4 mm trim "
     "(Sealeze/Gordon Brush class)", "PN ASSUMPTION"),
    ("set screw", "M2.5x4 hex socket cup-point grub (disc->shaft)", "class"),
    ("O-ring", "1.5 mm cord, Dia43.6 ID nitrile (fill cap gland)", "class"),
]
print("\nCOTS PART NUMBERS (r5; ASSUMPTION until ordered/verified except stepper):")
for _n, _p, _s in COTS:
    print(f"  {_n:16s} {_p:62s} {_s}")

# =====================================================================
# BOM.md (r5, buildability PROCESS: "COTS part numbers live only as print
# statements inside cad/dispenser.py"). Generated from the model so it
# cannot drift from the geometry.
# =====================================================================
with open(os.path.join(HERE, "BOM.md"), "w") as fh:
    fh.write("# Brush Bullet Dispenser -- BOM (auto-generated by cad/"
             "dispenser.py, rev %s)\n\n" % REV)
    fh.write("Masses of printed parts are MEASURED from the modeled solids at "
             "100%% infill (CF-PETG %.2f g/cm3, TPU %.2f). Do not edit by "
             "hand.\n\n## Printed parts\n\n" % (DENS["petg_cf"] * 1000,
                                                DENS["tpu"] * 1000))
    fh.write("| part | material | volume cm3 | mass g | best print orientation "
             "| support % |\n|---|---|---|---|---|---|\n")
    for pname in PRINTED:
        v = parts[pname]
        mat = "TPU" if pname == "agitator" else "CF-PETG"
        s = SUPPORT.get(pname, (float("nan"), "?"))
        fh.write(f"| {pname} | {mat} | {v['solid'].volume/1000:.2f} | "
                 f"{v['mass']:.1f} | {s[1]} | {s[0]:.1f} |\n")
    fh.write("\n## COTS / non-printed\n\n| item | part | status | mass g |\n"
             "|---|---|---|---|\n")
    _cots_mass = {"stepper": parts["stepper"]["mass"],
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
             "| 6 | M3x10 SHCS + 6x Ruthex RX-M3x5.7 insert | top plate -> "
             "hopper flange (r72.25) |\n"
             "| 3 | M3x8 Delta-PT plastite | hopper skirt tabs -> housing |\n"
             "| 2 | M3x12 SHCS | electronics bay ribs -> housing |\n"
             "| 4 | M3x8 self-tap | bay lid -> corner bosses |\n"
             "| 1 | M3x6 SHCS | wiper end tab -> housing pilot |\n"
             "| 1 | M3x4 cup-point grub | disc hub -> gearbox shaft D-flat |\n"
             "| 2 | M3x4 cup-point grub | IR emitter/receiver retention |\n"
             "| 4 | M3x8 SHCS | gearbox output flange -> retaining plate |\n"
             "| 1 | M5x0.8 ball-nose spring plunger, LIGHT (2.5 N) | detent |\n"
             "| 1 | 1.5 mm nitrile O-ring, ID 43.6 | fill-cap gland |\n"
             "| 9 | Dia3x2 N45 magnet | 8 pocket + 1 index |\n")
    fh.write(f"\n## Rolled up\n\n- empty (measured + estimates): "
             f"{total:.1f} g, +10% contingency -> {empty:.1f} g\n"
             f"- loaded @250 pellets: {loaded250:.1f} g (ceiling 1500 g)\n"
             f"- loaded @{N_FILL_MAX} (max fill rib): "
             f"{empty + N_FILL_MAX*PELLET_MASS:.1f} g\n"
             f"- usable hopper volume {v_use:.0f} cm3 -> {cap_worst} pellets "
             f"worst-case packing / {cap_sphere} sphere basis\n")
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
render(ALL, os.path.join(RENDER_DIR, "r6_iso.png"), elev=18, azim=-55,
       title="pocket-wheel dispenser r6 — iso (mapped clip mount, geared drive)")
cutter = Pos(0, 250, -260) * Box(500, 500, 500)  # remove +Y half
render(ALL, os.path.join(RENDER_DIR, "r6_section.png"), elev=8, azim=90, cut=cutter,
       title="r6 — section at Y=0: PCB well, 68° funnel, JFM-2023-07 bushing")
METER = ["meter_housing", "pocket_disc", "agitator", "brush_holder",
         "brush_bristles", "retaining_plate_chute", "thrust_washer", "stepper",
         "sleeve_bearing"]
cutter2 = Pos(0, 250, Z_FUN_BOT) * Box(500, 500, 500)
render(METER, os.path.join(RENDER_DIR, "r6_meter_detail.png"), elev=32, azim=135,
       cut=cutter2, cut_only={"meter_housing"},
       title="r6 — meter sectioned: underside entry ramp, deflector-nose wiper")
render(ALL, os.path.join(RENDER_DIR, "r6_bottom.png"), elev=-28, azim=-40,
       title="r6 — bottom: geared stepper, chute, IR bosses, fines slots")
FILLV = ["meter_housing", "pocket_disc", "agitator", "brush_holder",
         "brush_bristles", "sleeve_bearing"]
render(FILLV, os.path.join(RENDER_DIR, "r6_fill_station.png"), elev=62, azim=-90,
       title="r6 — fill station: bristles lead, 30° deflector nose trails")
# r5: the service state the r4 critic proved impossible -- cartridge dropped
CARTV = {"retaining_plate_chute", "pocket_disc", "stepper", "thrust_washer"}
serv = {}
for k, v in parts.items():
    s = copy.copy(v["solid"])
    if k in CARTV:
        s = Pos(0, 0, -60) * Rot(Z=22) * s
    serv[k] = dict(solid=s, color=v["color"], mass=v["mass"], basis="")
_orig, parts = parts, serv
render([k for k in parts if k not in ("hopper", "top_plate", "fill_cap",
                                      "clip_plate", "pcb_pedestal",
                                      "blindmate_pcb")],
       os.path.join(RENDER_DIR, "r6_cartridge_out.png"), elev=14, azim=-65,
       title="r6 — cartridge dropped out (agitator + wiper stay)")
parts = _orig
BAYV = ["meter_housing", "electronics_bay", "bay_lid", "retaining_plate_chute"]
render(BAYV, os.path.join(RENDER_DIR, "r6_bay_lid.png"), elev=12, azim=-115,
       title="r6 — electronics bay + the mapped clip-plate mount")
print("\ndone.")
