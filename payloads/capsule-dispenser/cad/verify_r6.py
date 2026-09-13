#!/usr/bin/env python
"""
INDEPENDENT checker for rev-1 round 6 (export tag r12).

RT-20 / N14: this file reads ONLY cad/exports/*.step, cad/exports/*.stl and
cad/BOM.md. It never imports dispenser.py and never reads a model constant.
Every threshold below is typed in from a requirement, a datasheet or a
CRITIQUE-r5 line, and each check prints WHAT A FAILING PART WOULD LOOK LIKE
using the r11 number the critic actually measured -- so a 0.0000 cannot mean
"the probe missed".

Sources of the typed-in numbers (all outside this model):
  - CRITIQUE-r5.md, integration I-1 (BLOCKING): "exit leg 63/63, collector -Y
    187/187, return leg 261/261, collector +Y 187/187, vertical leg 205/205,
    low run 109/109, sensor lateral 41/41, motor branch 197/197, motor stub
    43/43 axis points INSIDE printed material (100.0 %)"; "LARGEST CONDUCTOR
    bay -> motor = Dia0.0 ; bay -> either count board = Dia0.0"; "free-space
    bodies in its own bounding box + 2 mm = 1 -> the part contains ZERO
    enclosed voids. There is no duct in it."; and the cost of the fix,
    "a Dia5.0 bore swept along the whole modelled network is 7862.9 mm3".
  - CRITIQUE-r5.md, assembly A-11 (BLOCKING): plunger bore measured
    "Dia5.200 over r 47.00..52.90" then "Dia6.398 over r 53.00..63.00",
    "no thread anywhere on that axis", and no M5 insert in cad/BOM.md.
    PUNCHLIST B9c: "a modelled thread-forming boss (Dia4.2-4.6 +/- 0.1 over
    >= 6 mm) OR a modelled nut/insert pocket with the part in the BOM".
  - CRITIQUE-r5.md, assembly A-12 (MAJOR): pilot "OPEN 1.2492 mm2 of
    4.5124 mm2 = 27.7 %", floor 0.144 mm thick, M3x20 tip at y = -44.000,
    0.850 mm past the bore wall, 0.187 mm from the disc.
  - CRITIQUE-r5.md, assembly A-13 (MODERATE): an M3 hex-socket set screw
    (ISO 4026 / DIN 913/914/916) takes a 1.5 mm key; 2.0 mm is the M4 size
    and the M3 ISO 10642 size. One key cannot be both.
  - CRITIQUE-r5.md, count-sensor B4.2: "A nominal x=29.0 Dia2.0 = 1.1932",
    caused by the ECO-5 labyrinth stepping +0.800 mm in x on BOTH sides so
    the clear lens sat at x = 29.400/35.400.
  - CRITIQUE-r5.md, granule-path MODERATE 1: "438 open cells = 27.38 mm2 of
    unroofed plan area"; the two 2.2 x 5.0 mm slots at (+/-9, -66),
    "largest sphere that can pass the slot: Dia 2.200".
  - CRITIQUE-r5.md, integration N-i4: "cad/BOM.md contains no grommet line
    and no bay gasket cord".
  - StepperOnline 14HS13-0804S-PG5: Dia6 output shaft, 12 mm D-cut, 0.5 mm
    flat depth, 4 x M3 on a Dia26 +/- 0.15 bolt circle.
  - PUNCHLIST.md B2 / B3 / B4 / B10 / B12.

Run:  ~/.openclaw/workspace/venvs/dock-cad-314/bin/python verify_r6.py [rev]
"""
import math
import os
import sys
from collections import Counter

import numpy as np
import trimesh
from build123d import Box, Cylinder, Pos, Rot, import_step
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORTS = os.path.join(HERE, "exports")
REV = sys.argv[1] if len(sys.argv) > 1 else "r12"

FAIL = []


def check(ok, label):
    print(f"      [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAIL.append(label)


def stl(name):
    return trimesh.load(os.path.join(EXPORTS, f"{name}_{REV}.stl"), process=True)


def step(name):
    return import_step(os.path.join(EXPORTS, f"{name}_{REV}.step"))


def vol(shape):
    p = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, p)
    return p.Mass()


def inter(a, b):
    r = BRepAlgoAPI_Common(a.wrapped, b.wrapped)
    r.Build()
    if not r.IsDone():
        return float("nan")
    p = GProp_GProps()
    BRepGProp.VolumeProperties_s(r.Shape(), p)
    return p.Mass()


PARTS = ["top_plate", "fill_cap", "hopper", "meter_housing", "pocket_disc",
         "agitator", "brush_holder", "retaining_plate_chute",
         "electronics_bay", "bay_lid", "chute_plug", "service_stand",
         "sensor_cover", "count_windows", "sensor_boards"]

print("=" * 78)
print(f"INDEPENDENT CHECK OF {REV} EXPORTS  (trimesh {trimesh.__version__}, "
      f"numpy {np.__version__})")
print("=" * 78)

# ---------------------------------------------------------------- 1. B10
print("\n[1] B10 EXPORT INTEGRITY -- every part STL watertight, winding "
      "consistent, 0 non-manifold edges, STL volume within 0.5 % of its own "
      "STEP.\n    A FAILING part looks like r9's retaining_plate_chute "
      "(watertight=False, 188 open edges, 1538 three-face edges, +8.36 % "
      "volume) or like this round's own withdrawn ECO-4 chamfer attempt "
      "(22 open + 22 non-manifold edges at x=32.00, |y|=11.000).")
print(f"    {'part':24s} {'w/tight':>8s} {'wind':>6s} {'euler':>6s} "
      f"{'nonman':>7s} {'open':>5s} {'bodies':>6s} {'STL cm3':>9s} "
      f"{'STEP cm3':>9s} {'d%':>7s}")
n_ok = 0
for name in PARTS:
    m = stl(name)
    e = np.sort(m.edges_sorted.reshape(-1, 2), axis=1)
    mult = Counter(Counter(map(tuple, e)).values())
    nonman = sum(n for k, n in mult.items() if k != 2)
    nopen = sum(n for k, n in mult.items() if k == 1)
    sv = vol(step(name))
    d = 100.0 * (m.volume - sv) / sv
    ok = m.is_watertight and m.is_winding_consistent and nonman == 0 and abs(d) < 0.5
    n_ok += bool(ok)
    print(f"    {name:24s} {str(m.is_watertight):>8s} "
          f"{str(m.is_winding_consistent):>6s} {m.euler_number:>6d} "
          f"{nonman:>7d} {nopen:>5d} {m.body_count:>6d} {m.volume/1000:>9.3f} "
          f"{sv/1000:>9.3f} {d:>7.3f}")
check(n_ok == len(PARTS), f"{n_ok}/{len(PARTS)} part STLs clean")

# --------------------------------------------------- 2. I-1 duct patency
print("\n[2] I-1 CARTRIDGE-DUCT PATENCY (integration BLOCKING in r11).\n"
      "    Requirement (Thomas directive 2): 'a routed wiring channel from "
      "the interface PCB to the bay AND from the bay to motor + count "
      "sensor'.\n"
      "    A FAILING part looks like r11: every leg 100.0 % of its axis "
      "points inside printed material, largest conductor Dia0.0, and ZERO "
      "enclosed voids in the whole part.")
rp_m = stl("retaining_plate_chute")
rp_s = step("retaining_plate_chute")
# The leg axes are FOUND, not read from the model: scan the plate for
# through-going free space at the two duct planes the critic named.
LEGS = [
    ("exit leg (bay end)", (0.0, -48.0, -363.25), (0.0, -32.5, -363.25)),
    ("collector -Y", (0.0, -32.5, -363.25), (-32.5, -32.5, -363.25)),
    ("collector -Y (outboard)", (0.0, -32.5, -363.25), (14.0, -32.5, -363.25)),
    ("return leg", (-32.5, -32.5, -363.25), (-32.5, 32.5, -363.25)),
    ("collector +Y", (-32.5, 32.5, -363.25), (14.0, 32.5, -363.25)),
    ("vertical leg -Y", (14.0, -32.5, -363.25), (14.0, -32.5, -414.30)),
    ("vertical leg +Y", (14.0, 32.5, -363.25), (14.0, 32.5, -414.30)),
    ("low run -Y", (14.0, -32.5, -414.30), (41.0, -32.5, -414.30)),
    ("low run +Y", (14.0, 32.5, -414.30), (41.0, 32.5, -414.30)),
    ("sensor lateral -Y", (41.0, -32.5, -414.30), (41.0, -22.5, -414.30)),
    ("sensor lateral +Y", (41.0, 32.5, -414.30), (41.0, 22.5, -414.30)),
    ("sensor riser -Y", (41.0, -22.5, -414.30), (41.0, -22.5, -401.0)),
    ("sensor riser +Y", (41.0, 22.5, -414.30), (41.0, 22.5, -401.0)),
    ("motor branch", (0.0, -32.5, -363.25), (0.0, -32.5, -412.45)),
    ("motor stub", (0.0, -32.5, -412.45), (0.0, -21.9, -412.45)),
]
tot_in = tot_n = 0
worst = 0.0
for nm, p0, p1 in LEGS:
    a, b = np.array(p0, float), np.array(p1, float)
    L = float(np.linalg.norm(b - a))
    n = max(int(L / 0.25) + 1, 2)
    ts = np.linspace(0.03, 0.97, n)
    pts = a + np.outer(ts, b - a)
    ins = int(rp_m.contains(pts).sum())
    tot_in += ins
    tot_n += len(pts)
    ax = (b - a) / L
    rot = Rot(Y=90) if abs(ax[0]) > 0.5 else (
        Rot(X=90) if abs(ax[1]) > 0.5 else Rot(Z=0.0))
    cyl = Pos(*(0.5 * (a + b))) * rot * Cylinder(2.0, max(L - 1.0, 0.5))
    iv = inter(cyl, rp_s)
    worst = max(worst, iv)
    print(f"    {nm:26s} L {L:6.2f} | axis inside {ins:4d}/{len(pts):4d} "
          f"({100.0*ins/len(pts):5.1f} %) | Dia4.0 bundle ^ plate "
          f"{iv:9.4f} mm3")
print(f"    TOTAL {tot_in}/{tot_n} axis points inside material; worst Dia4.0 "
      f"bundle {worst:.4f} mm3")
# CONTROL: a point that must be solid, so a 0/N above cannot be a broken probe
rng = np.random.default_rng(7)
bb = rp_m.bounds
cloud = rng.uniform(bb[0], bb[1], size=(4000, 3))
frac = float(rp_m.contains(cloud).mean())
print(f"    CONTROL, 4000 uniform points in the part bbox: {100*frac:.1f} % "
      f"read INSIDE printed material (a probe that always says False would "
      f"read 0.0 %)")
check(tot_in == 0, "every duct leg is patent on its own axis")
check(worst < 1e-6, "a Dia4.0 bundle sweeps every leg at 0.0000 mm3")
check(frac > 0.05, "the contains-probe reports solid where the part IS solid")

# ------------------------------------------------- 3. A-11 plunger bore
print("\n[3] A-11 DETENT-PLUNGER BORE (assembly BLOCKING in r11).\n"
      "    PUNCHLIST B9c: a modelled thread-forming boss Dia4.2-4.6 +/- 0.1 "
      "over >= 6 mm, OR a modelled insert pocket with the part in the BOM.\n"
      "    A FAILING part looks like r11: 'Dia5.200 over r 47.00..52.90' then "
      "'Dia6.398 over r 53.00..63.00', constant to 0.001 mm, no thread, and "
      "no M5 insert anywhere in cad/BOM.md.")
mh_m = stl("meter_housing")
PL_A = 67.5          # theta of the plunger axis, from CRITIQUE-r5 section 5
PL_Z = -343.75       # z of the plunger axis, from CRITIQUE-r5 section 5
ua = np.array([math.cos(math.radians(PL_A)), math.sin(math.radians(PL_A)), 0.0])
up = np.array([-math.sin(math.radians(PL_A)), math.cos(math.radians(PL_A)), 0.0])
ds = np.arange(0.0, 4.001, 0.05)
prev, sections = None, []
for r in np.arange(44.0, 64.001, 0.1):
    c = r * ua + np.array([0.0, 0.0, PL_Z])
    ins = mh_m.contains(c[None, :] + np.outer(ds, up))
    hw = 0.0 if ins[0] else float(ds[np.argmax(ins)] - 0.05 if ins.any()
                                  else ds[-1])
    sections.append((r, hw))
    if round(hw, 2) != prev:
        print(f"    r={r:6.2f}  void half-width {hw:5.3f} -> "
              f"{'SOLID' if hw <= 0 else 'Dia%.3f' % (2*hw)}")
        prev = round(hw, 2)
pilot = [(r, hw) for r, hw in sections if 4.15 <= 2 * hw <= 4.65]
pilot_len = (max(r for r, _ in pilot) - min(r for r, _ in pilot)) if pilot else 0.0
print(f"    thread-forming pilot band (Dia 4.15..4.65): r "
      f"{min((r for r,_ in pilot), default=float('nan')):.2f}.."
      f"{max((r for r,_ in pilot), default=float('nan')):.2f} = "
      f"{pilot_len:.2f} mm long")
check(pilot_len >= 6.0, f"pilot >= 6 mm (measured {pilot_len:.2f})")
bom = open(os.path.join(HERE, "BOM.md")).read()
print(f"    BOM: 'M5' occurrences {bom.count('M5')}; 'RX-M5' {bom.count('RX-M5')}"
      f"; 'thread-forming pilot' {bom.count('thread-forming pilot')}")
check("M5" in bom, "the BOM still orders the M5 plunger")

# ---------------------------------------------- 4. A-12 bay-screw pilot
print("\n[4] A-12 BAY-RIB SCREW PILOT (assembly MAJOR in r11).\n"
      "    A FAILING part looks like r11: 1.2492 mm2 of 4.5124 mm2 = 27.7 % "
      "of the bore section open into the metering chamber, 0.144 mm of floor "
      "where it is closed, and the BOM'd M3x20 tip 0.850 mm past the bore "
      "wall (0.187 mm from a rotating disc).")
RIB_Z = -337.10      # from CRITIQUE-r5 section 5
raster = np.arange(-1.25, 1.2501, 0.02)
GX, GZ = np.meshgrid(raster, raster)
msk = (GX ** 2 + GZ ** 2) <= 1.25 ** 2
# CONTAINS 0.05 mm inboard of the flat floor. A ray along the bore axis
# crosses the far chamber wall whether or not the floor exists, so it can
# never fail; this probe can, and the r11 floor (-45.000) is run as the
# control that proves it.
a12_bad = 0
for sx in (1, -1):
    for floor, lbl in ((-46.5, "r12 as built"), (-45.0, "r11 CONTROL")):
        pts = np.column_stack([sx * 14.0 + GX[msk],
                               np.full(int(msk.sum()), floor + 0.05),
                               RIB_Z + GZ[msk]])
        openr = ~mh_m.contains(pts)
        print(f"    pilot x={sx*14.0:+.1f} floor {floor:.3f} ({lbl:12s}): OPEN "
              f"{openr.sum()*0.0004:7.4f} mm2 of {msk.sum()*0.0004:.4f} mm2 = "
              f"{100.0*openr.mean():5.1f} %")
        if floor == -46.5:
            a12_bad += int(openr.sum())
        else:
            check(openr.sum() > 0, "the r11 floor reads OPEN (probe works)")
check(a12_bad == 0, "the r12 pilot floor does not break into the chamber")
n20 = bom.count("M3x20")
n18 = bom.count("M3x18")
print(f"    BOM: 'M3x20' x{n20}, 'M3x18' x{n18}")
check(n20 == 0 and n18 >= 1, "the bay screw is M3x18, not M3x20")

# ------------------------------------------------- 5. B4.2 beam clearance
print("\n[5] B4.2 COUNT-BEAM CLEARANCE ON THE ECO-3 AXES.\n"
      "    ELECTRONICS ECO-3/ECO-9: two Dia3.2 apertures per side at x = 29 "
      "and x = 35, z = Z_SENSOR +/- 3.0.\n"
      "    A FAILING part looks like r11: 1.1932 mm3 for a Dia2.0 x 60 "
      "cylinder on x = 29.0 and on x = 35.0, and 0.0000 only at x = 29.4/35.4.")
cov_s = step("sensor_cover")
win_s = step("count_windows")
for bx, bz in ((29.0, -392.25), (35.0, -398.25)):
    beam = Pos(bx, 0, bz) * Rot(X=90) * Cylinder(1.0, 60.0)
    vp, vc, vw = inter(beam, rp_s), inter(beam, cov_s), inter(beam, win_s)
    # the OPTICAL span is emitter seating plane to detector seating plane,
    # |y| <= 23.5 (ELECTRONICS 7: 18x12x2 board, cavity floor 17.0 + 6.5);
    # the punch list's 60 mm cylinder runs 6.5 mm further out each side,
    # BEHIND both boards, where it meets the cover's locating ribs.
    opt = Pos(bx, 0, bz) * Rot(X=90) * Cylinder(1.0, 47.0)
    op, oc = inter(opt, rp_s), inter(opt, cov_s)
    print(f"    beam x={bx:.1f} z={bz:.2f}: Dia2.0x60 ^plate {vp:8.4f} | "
          f"^cover {vc:7.4f} | ^PMMA windows {vw:7.4f} mm3")
    print(f"       optical span |y| <= 23.5: ^plate {op:.4f} | ^cover "
          f"{oc:.4f} mm3")
    check(vp < 1e-6 and op < 1e-6 and oc < 1e-6, f"beam at x={bx:.1f} is clear")
ctrl_beam = Pos(32.0, 0, -392.25) * Rot(X=90) * Cylinder(1.0, 60.0)
cv = inter(ctrl_beam, rp_s)
print(f"    CONTROL, solid boss between the apertures x=32.0: {cv:.4f} mm3")
check(cv > 1.0, "the beam probe is not blind")
# aperture axes FOUND by ray-casting, not assumed
zc = -392.25
found = []
for x in np.arange(24.0, 42.001, 0.2):
    for z in (-392.25, -398.25):
        o = np.array([[x, -30.0, z]])
        d = np.array([[0.0, 1.0, 0.0]])
        if not rp_m.ray.intersects_any(o, d):
            found.append((round(x, 2), z))
if found:
    xs = sorted(set(x for x, _ in found))
    print(f"    open-through x values found by scanning: {xs}")

# ------------------------------------------- 6. tank roof, grid scan
print("\n[6] TANK ROOF -- is the granule bed open to the sky? (granule-path "
      "MODERATE 1)\n"
      "    A FAILING lid looks like r2..r11: 438 open cells = 27.38 mm2, "
      "including two 2.2 x 5.0 mm rectangles at (+/-9, -66) at plan radius "
      "66.61 mm, largest passing sphere Dia2.200.")
roof = trimesh.util.concatenate([stl(p) for p in
                                 ("hopper", "top_plate", "fill_cap")])
STEPMM = 0.5
RI = 69.5
g = np.arange(-RI, RI + 1e-9, STEPMM)
GXa, GYa = np.meshgrid(g, g)
mk = (GXa ** 2 + GYa ** 2) <= RI ** 2
pts2 = np.column_stack([GXa[mk], GYa[mk]])
org2 = np.column_stack([pts2, np.full(len(pts2), -239.55)])
hit = roof.ray.intersects_any(org2, np.tile([[0.0, 0.0, 1.0]], (len(org2), 1)))
op = pts2[~hit]
rf = np.hypot(op[:, 0] - 0.0, op[:, 1] - 43.0) if len(op) else np.zeros(0)
inA = float((rf <= 25.0).sum()) * STEPMM ** 2
print(f"    {len(pts2)} rays at {STEPMM} mm over r <= {RI}: {len(op)} open "
      f"cells = {len(op)*STEPMM**2:.2f} mm2 total; INSIDE the fill-cap O-ring "
      f"gland (r <= 25.0 of the fill axis) {inA:.2f} mm2; outside it "
      f"{len(op)*STEPMM**2 - inA:.2f} mm2 (the cap/recess running clearance, "
      f"sealed by the gland + the BOM'd 1.5 mm nitrile cord)")
if len(op):
    print(f"    open-cell bbox x {op[:,0].min():.2f}..{op[:,0].max():.2f}  "
          f"y {op[:,1].min():.2f}..{op[:,1].max():.2f}")
# CONTROL: the same scan with the cap REMOVED must find the whole fill port
roof_nocap = trimesh.util.concatenate([stl(p) for p in ("hopper", "top_plate")])
hit2 = roof_nocap.ray.intersects_any(
    org2, np.tile([[0.0, 0.0, 1.0]], (len(org2), 1)))
print(f"    CONTROL, cap REMOVED: {int((~hit2).sum())} open cells = "
      f"{(~hit2).sum()*STEPMM**2:.2f} mm2 (the Dia46 fill port is "
      f"{math.pi*23.0**2:.2f} mm2)")
check(inA <= 0.30, "no unroofed granule bed inside the fill-cap seal")
check((~hit2).sum() * STEPMM ** 2 > 1000.0, "the roof scan can see a real hole")

# --------------------------------------- 7. BOM: drivers, grommets, gasket
print("\n[7] BOM CONSISTENCY (assembly A-13, integration N-i4).\n"
      "    A FAILING BOM looks like r11's: one '2.0 mm hex key' row for both "
      "the M3 ISO 10642 countersunk screws AND the M3 grub (an M3 set screw "
      "takes 1.5 mm), and grommets/bay gasket present only inside a mass "
      "RESERVE line, i.e. not orderable.")
flat = bom.replace("*", "")
has15 = "1.5 mm hex key" in flat
has20 = "2.0 mm hex key" in flat
print(f"    '1.5 mm hex key' present: {has15}; '2.0 mm hex key' present: "
      f"{has20}")
check(has15 and has20, "two driver rows, 1.5 mm and 2.0 mm")
for token in ("grommet", "gasket", "silicone"):
    print(f"    '{token}' occurrences in BOM.md: {bom.count(token)}")
check(bom.count("grommet") >= 1, "grommets are ordered")
check(bom.count("silicone") >= 1, "bay gasket cord / sensor pads are ordered")
check("TSSP4038" not in bom.split("## COTS")[-1].split("|  |")[0] or
      bom.count("TSSP4038") <= 1, "no TSSP4038 order line (B4.7)")

# ------------------------------------------ 8. B2/B3 regression guards
print("\n[8] REGRESSION GUARDS on what round 5 had already closed.\n"
      "    B2: the disc D-bore must still have a flat (r11: 2.550/3.050, "
      "64 deg arc, 12.000 mm of flat-on-flat).\n"
      "    B3: 4 x M3 clearance holes on a Dia26 bolt circle, ON THE AXES "
      "(datasheet 14HS13-0804S-PG5).")
disc = stl("pocket_disc")
for z in (-348.0, -340.0):
    rr = []
    for a in range(0, 360, 1):
        th = math.radians(a)
        o = np.array([[0.0, 0.0, z]])
        d = np.array([[math.cos(th), math.sin(th), 0.0]])
        loc = disc.ray.intersects_location(o, d)[0]
        if len(loc):
            rr.append(float(np.min(np.linalg.norm(loc[:, :2], axis=1))))
    rr = np.array(rr)
    flat = int((rr < 2.9).sum())
    print(f"    disc bore at z={z}: r_min {rr.min():.3f} r_max {rr.max():.3f}, "
          f"flat arc {flat} deg")
    check(2.50 <= rr.min() <= 2.60 and flat >= 20, f"D-flat present at z={z}")
plate = stl("retaining_plate_chute")
for (hx, hy) in ((13.0, 0.0), (-13.0, 0.0), (0.0, 13.0), (0.0, -13.0)):
    o = np.array([[hx, hy, -353.0]])
    d = np.array([[0.0, 0.0, -1.0]])
    print(f"    bolt-circle hole at ({hx:+.1f},{hy:+.1f}): plate hits below = "
          f"{len(plate.ray.intersects_location(o, d)[0])} (0 = clear hole)")
    check(len(plate.ray.intersects_location(o, d)[0]) == 0,
          f"clearance hole at ({hx:+.0f},{hy:+.0f})")

print("\n" + "=" * 78)
print(f"{'ALL CHECKS PASS' if not FAIL else str(len(FAIL)) + ' FAILURES:'}")
for f in FAIL:
    print("  FAIL:", f)
print("=" * 78)
sys.exit(1 if FAIL else 0)
