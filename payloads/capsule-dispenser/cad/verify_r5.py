#!/usr/bin/env python
"""
INDEPENDENT checker for rev-1 round 5 (export tag r11).

RT-20 / N14: this file reads ONLY cad/exports/*.step, cad/exports/*.stl and
cad/BOM.md. It never imports dispenser.py and never reads a model constant.
Every threshold below is typed in from a requirement, a datasheet or a
critique line, and each check prints what a FAILING part would look like.

Sources of the typed-in numbers:
  - Vishay doc 81010 rev 2.4 (TSAL6200): Dia5.0 +/-0.15 body, Dia5.8 +/-0.15
    flange, 8.7 +/- 0.3 mm seating plane -> dome apex, dome R2.49 sphere.
  - Vishay doc 81127 rev 1.3 (VBPW34FAS): SMD gullwing 6.4 x 3.9 x 1.2 mm.
  - StepperOnline 14HS13-0804S-PG5: Dia6 output shaft, 12 mm D-cut, 0.5 mm
    flat depth, 4 x M3 on a Dia26 +/- 0.15 bolt circle.
  - _run/rev1/PUNCHLIST.md B1/B2/B4/B7/B8/B10.
  - _run/rev1/CRITIQUE-r3.md: the r9 numbers each check has to move.
  - _run/rev1/CRITIQUE-r4.md: the r10 numbers ROUND 5 has to move --
    integration BLOCKING (conduit elbow solid: vertical bore axis solid over
    z -237.50..-225.00, horizontal over y -84.00..-72.00, largest conductor
    Dia0.0), assembly BLOCKING A-10 (M3x8 SHCS ordered for a 90 deg
    countersink; cap head 8.8652 mm3 static / 49.4066 mm3 swept vs the disc),
    granule-path MAJOR (tether lug r_min 10.000 in an r11.000 bore over
    z -398.00..-404.00; plate ^ plug 206.0993 mm3 of which only 83.504 is the
    designed press fit).
  - Thomas directive 2: the dispenser needs an electronics home AND a routed
    harness -- so a conductor must be able to get from the interface to the
    bay. That requirement, not a model constant, is what section [8] tests.

Run:  ~/.openclaw/workspace/venvs/dock-cad-314/bin/python verify_r4.py
"""
import math
import os
import sys
from collections import Counter

import numpy as np
import trimesh
from build123d import (Box, Cylinder, Pos, Rot, Sphere, import_step)
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORTS = os.path.join(HERE, "exports")
REV = sys.argv[1] if len(sys.argv) > 1 else "r11"

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
      "STEP.\n    A FAILING part looks like r9's retaining_plate_chute: "
      "watertight=False, 188 open edges, 1538 three-face edges, +8.36 % "
      "volume.")
print(f"    {'part':24s} {'w/tight':>8s} {'wind':>6s} {'euler':>6s} "
      f"{'nonman':>7s} {'open':>5s} {'bodies':>6s} {'STL cm3':>9s} "
      f"{'STEP cm3':>9s} {'d%':>7s}  multiplicity")
n_ok = 0
for name in PARTS:
    m = stl(name)
    e = np.sort(m.edges_sorted.reshape(-1, 2), axis=1)
    mult = Counter(Counter(map(tuple, e)).values())
    nonman = sum(n for k, n in mult.items() if k != 2)
    sv = vol(step(name))
    d = 100.0 * (m.volume - sv) / sv
    ok = m.is_watertight and m.is_winding_consistent and nonman == 0 and abs(d) < 0.5
    n_ok += bool(ok)
    print(f"    {name:24s} {str(m.is_watertight):>8s} "
          f"{str(m.is_winding_consistent):>6s} {m.euler_number:6d} "
          f"{nonman:7d} {mult.get(1, 0):5d} "
          f"{len(trimesh.graph.connected_components(m.face_adjacency, nodes=np.arange(len(m.faces)))):6d} "
          f"{m.volume/1000:9.3f} {sv/1000:9.3f} {d:+7.3f}  {dict(sorted(mult.items()))}")
check(n_ok == len(PARTS), f"{n_ok}/{len(PARTS)} part STLs clean (r9: 14/15)")

asm = trimesh.load(os.path.join(EXPORTS, f"dispenser_{REV}_assembly.stl"),
                   process=True)
ae = np.sort(asm.edges_sorted.reshape(-1, 2), axis=1)
amult = Counter(Counter(map(tuple, ae)).values())
abodies = len(trimesh.graph.connected_components(
    asm.face_adjacency, nodes=np.arange(len(asm.faces))))
print(f"    assembly: bodies={abodies}  open edges={amult.get(1, 0)}  "
      f"multiplicity={dict(sorted(amult.items()))}  vol="
      f"{asm.volume/1000:.3f} cm3  winding={asm.is_winding_consistent}")
check(amult.get(1, 0) == 0 and asm.is_winding_consistent,
      "assembly STL has 0 open edges and consistent winding (r9: 188 open, "
      "winding False, 2 inverted bodies)")

# ------------------------------------------------- 2. count sensor / emitter
print("\n[2] COUNT SENSOR -- the ORDERED emitter has to fit. Datasheet solid "
      "(Dia5.8 x 0.7 flange + Dia5.0 barrel + R2.49 dome) seated on the board "
      "plane recovered FROM THE EXPORT, at 8.7 nominal and 9.0 max.\n"
      "    A FAILING part looks like r9: 11.2532 mm3 per LED into the plate "
      "at nominal, 14.6614 at max.")
plate = step("retaining_plate_chute")
cover = step("sensor_cover")
boards = step("sensor_boards")
bb = boards.bounding_box()
print(f"    sensor_boards bbox x[{bb.min.X:.3f},{bb.max.X:.3f}] "
      f"y[{bb.min.Y:.3f},{bb.max.Y:.3f}] z[{bb.min.Z:.3f},{bb.max.Z:.3f}]")
pbb = plate.bounding_box()
# recover the board seating plane from the exported cover: the clamp posts
# stop on it.  Probe the cover for its innermost |y| material on a post axis.
cbb = cover.bounding_box()
BOSS_FACE = float(min(abs(cbb.min.Y), abs(cbb.max.Y)))
print(f"    boss/cover interface |y| = {BOSS_FACE:.3f} (r9: 27.500)")


def led(x, z, sy, h, seat):
    s = Pos(x, sy * (seat - 0.35), z) * Rot(X=90) * Cylinder(2.9, 0.7)
    barrel = (h - 2.49) - 0.7
    s += Pos(x, sy * (seat - 0.7 - barrel / 2), z) * Rot(X=90) * \
        Cylinder(2.5, barrel)
    s += Pos(x, sy * (seat - (h - 2.49)), z) * Sphere(2.49)
    return s


# the seating plane is the board's inner face: measured off the exported
# sensor_boards solid as the innermost face of the 2 mm PCB slab.
# probe at a corner of the board where no device sits (devices are at
# x = 29.8 / 35.8, z = -392.25 / -398.25): ray-cast the +Y board slab
bm = stl("sensor_boards")
_loc, _, _ = bm.ray.intersects_location(
    ray_origins=np.array([[42.0, 0.0, -395.25]]),
    ray_directions=np.array([[0.0, 1.0, 0.0]]))
seat = float(min(p[1] for p in _loc))
print(f"    board seating plane recovered from the export: |y| = {seat:.3f} "
      f"(r9: 23.500)")
DEV_X = [29.8, 35.8]
DEV_Z = [-392.25, -398.25]
for h, lbl in ((8.7, "nominal"), (9.0, "max tolerance")):
    vp = vc = 0.0
    for sy in (1, -1):
        for x, z in zip(DEV_X, DEV_Z):
            L = led(x, z, sy, h, seat)
            vp += inter(L, plate)
            vc += inter(L, cover)
    print(f"    TSAL6200 {h:.1f} mm ({lbl}), 4 placements: ^plate = "
          f"{vp:.4f} mm3   ^cover = {vc:.4f} mm3")
    check(vp < 1e-3 and vc < 1e-3, f"emitter fits at {lbl}")
vpd = 0.0
for x, z in zip(DEV_X, DEV_Z):
    pd = Pos(x, -(seat - 0.6), z) * Box(6.4, 1.2, 3.9)
    vpd += inter(pd, plate)
print(f"    VBPW34FAS 6.4 x 3.9 x 1.2 SMD, 2 placements: ^plate = "
      f"{vpd:.4f} mm3")
check(vpd < 1e-3, "receiver fits")

# ECO-3/ECO-9/ECO-5 aperture geometry, by ray-casting the plate mesh
print("\n    ECO-3/9/5 aperture audit (ray-cast on the plate STL along +/-y).")
print("    A CLEAR beam axis shows ZERO crossings -- the ray never touches "
      "material.\n    A BLOCKED axis shows 4 (plate, bore, bore, plate): the "
      "mismatched x/z pairs\n    printed underneath are exactly that control, "
      "so 'zero crossings' cannot mean\n    'the ray missed the part'.")
pm = stl("retaining_plate_chute")
BEAM_AX = [(29.0, -392.25), (35.0, -398.25), (29.8, -392.25), (35.8, -398.25)]
CTRL_AX = [(35.0, -392.25), (29.0, -398.25), (35.8, -392.25), (29.8, -398.25)]


def ycrossings(x, z):
    loc, _, _ = pm.ray.intersects_location(
        ray_origins=np.array([[x, -40.0, z]]),
        ray_directions=np.array([[0.0, 1.0, 0.0]]))
    return sorted(float(p[1]) for p in loc)


clear = True
for (x, z) in BEAM_AX:
    ys = ycrossings(x, z)
    clear &= (len(ys) == 0)
    print(f"      BEAM    x={x:5.1f} z={z:9.3f}: {len(ys)} crossings "
          + " ".join(f"{v:.3f}" for v in ys))
for (x, z) in CTRL_AX:
    ys = ycrossings(x, z)
    print(f"      control x={x:5.1f} z={z:9.3f}: {len(ys)} crossings "
          + " ".join(f"{v:.3f}" for v in ys))
check(clear, "all 4 beam/labyrinth axes are clear through the plate")

# aperture centres and diameters, measured in the inner and outer runs
for ylev, lbl in ((13.0, "inner run"), (16.0, "labyrinth run")):
    for zc in (-392.25, -398.25):
        xs = np.arange(24.0, 42.0, 0.005)
        P = np.stack([xs, np.full_like(xs, ylev), np.full_like(xs, zc)], axis=1)
        solid = pm.contains(P)
        holes = []
        s0 = None
        for i, v in enumerate(solid):
            if not v and s0 is None:
                s0 = xs[i]
            if v and s0 is not None:
                holes.append((float(s0), float(xs[i - 1])))
                s0 = None
        holes = [h for h in holes if h[1] - h[0] > 0.5]
        print(f"      {lbl} at |y|={ylev:.1f}, z={zc:.3f}: open x runs "
              + ", ".join(f"[{a:.3f},{b:.3f}] -> centre {(a+b)/2:.3f} "
                          f"width {b-a:.3f}" for a, b in holes))
zs_a, zs_b = None, None
for zc, xc in ((-392.25, 29.0), (-398.25, 35.0)):
    zz = np.arange(zc - 4.0, zc + 4.0, 0.005)
    P = np.stack([np.full_like(zz, xc), np.full_like(zz, 13.0), zz], axis=1)
    solid = pm.contains(P)
    open_z = zz[~solid]
    print(f"      aperture z-extent at x={xc:.1f}: [{open_z.min():.3f},"
          f"{open_z.max():.3f}] -> centre {(open_z.min()+open_z.max())/2:.3f} "
          f"height {open_z.max()-open_z.min():.3f}")
    if xc == 29.0:
        zs_a = (open_z.min() + open_z.max()) / 2
    else:
        zs_b = (open_z.min() + open_z.max()) / 2
print(f"      ECO-9 vertical stagger = {abs(zs_a - zs_b):.3f} mm "
      f"(spec 6.000; a FAILING part reads 0.000 -- one centred beam)")
check(abs(abs(zs_a - zs_b) - 6.0) < 0.05, "ECO-9 6.000 mm stagger")

# --------------------------------------------------------------- 3. B7
print("\n[3] B7 RELEASE SWEEP, measured on the exported plate. Criterion: the "
      "granule is supported while its contact point is over flat plate-top "
      "material, i.e. while |pellet centre - port axis| >= the FIRST-MATERIAL "
      "radius at the plate top. Seat offset applied along the pocket->port "
      "chord (worst case).\n    r9 published 6.75..7.75 deg / 1.00 deg "
      "spread; the r3 critic measured 3.25..10.50 / 7.25.")
# plate top plane and the first-material radius at that plane, both by
# ray-cast (fast, and independent of any model constant)
_loc, _, _ = pm.ray.intersects_location(
    ray_origins=np.array([[42.0, 0.0, -300.0]]),
    ray_directions=np.array([[0.0, 0.0, -1.0]]))
PLATE_TOP = float(max(p[2] for p in _loc))
# first material radius at the plate top: one horizontal ray from the port
# axis outward, 2 um below the top plane (point-in-solid sampling in a plane
# parallel to a face is pathologically slow in trimesh and is not needed)
_loc, _, _ = pm.ray.intersects_location(
    ray_origins=np.array([[32.0, 0.0, PLATE_TOP - 0.002]]),
    ray_directions=np.array([[1.0, 0.0, 0.0]]))
rim = float(min(p[0] for p in _loc)) - 32.0 if len(_loc) else float("nan")
print(f"    plate top z = {PLATE_TOP:.3f}; first material at r = {rim:.3f} "
      f"from the port axis (r9 critic: 8.747)")
rows = []
for D in (13.0, 12.0, 11.0):
    for e in (7.5 - D / 2, 0.0, -(7.5 - D / 2)):
        a = 22.5
        while a > 0:
            chord = 2 * 32.0 * math.sin(math.radians(a) / 2)
            if chord - e <= rim:
                break
            a -= 0.25
        rows.append((D, e, 22.5 - a, chord, chord - e))
        print(f"      D{D:4.1f} seat {e:+5.2f}: support lost "
              f"{22.5 - a:5.2f} deg into the index, pocket-axis-to-port "
              f"{chord:6.3f}, pellet-centre-to-port {chord - e:6.3f}")
angs = [r[2] for r in rows]
a13 = [r[2] for r in rows if r[0] == 13.0]
print(f"    -> window {min(angs):.2f}..{max(angs):.2f} deg into the 22.5 deg "
      f"index; spread {max(angs)-min(angs):.2f} deg over D11..D13, "
      f"{max(a13)-min(a13):.2f} deg at D13")
check(abs((max(angs) - min(angs)) - 7.25) < 0.6,
      "release spread reproduces the r3 critic's 7.25 deg (r9 claimed 1.00)")

# --------------------------------------------------------------- 4. B8
print("\n[4] B8 -- deflector nose gap and FIRST CONTACT. B8.1 asks for a nose "
      "underside <= 1.50 mm above the disc at r = 22..46.5. Then: what does a "
      "proud fragment actually strike? Ray along the travel direction at its "
      "crown height.\n    r3 MODERATE 1 asserted 'a 5.95 mm square wall, "
      "lift/push 0.005, over the whole 1.50-7.45 band'.")
hm = stl("brush_holder")
dm = stl("pocket_disc")
# the disc TOP LAND, not the bbox (the hub stands proud of it): ray down at
# the PCD, away from a pocket
# theta = 22.5 deg is exactly between two pockets (pockets are on 45 deg
# centres, half-width ~13.4 deg at the PCD), so this ray lands on the top land
_loc, _, _ = dm.ray.intersects_location(
    ray_origins=np.array([[32.0 * math.cos(math.radians(22.5)),
                           32.0 * math.sin(math.radians(22.5)), -300.0]]),
    ray_directions=np.array([[0.0, 0.0, -1.0]]))
DISC_TOP = float(max(p[2] for p in _loc))
print(f"    disc top land z = {DISC_TOP:.3f} (bbox max is the hub at "
      f"{dm.bounds[1][2]:.3f})")
BRUSH_A = None
# recover the wiper station angle from the holder centroid
c = hm.centroid
BRUSH_A = math.degrees(math.atan2(c[1], c[0])) % 360
print(f"    wiper station recovered from the export: theta = {BRUSH_A:.2f} deg")
ca, sa = math.cos(math.radians(BRUSH_A)), math.sin(math.radians(BRUSH_A))


def loc2w(x, y, z):
    return np.array([x * ca - y * sa, x * sa + y * ca, z])


gaps = []
for r in (22.0, 26.0, 30.0, 34.0, 38.0, 42.0, 46.5):
    o = loc2w(r, 0.0, DISC_TOP + 0.02)
    loc, _, _ = hm.ray.intersects_location(
        ray_origins=o[None, :], ray_directions=np.array([[0.0, 0.0, 1.0]]))
    g = float(loc[:, 2].min()) - DISC_TOP if len(loc) else float("nan")
    gaps.append(g)
    print(f"      r={r:5.1f}: nose underside {g:.3f} mm above the disc top")
check(max(gaps) <= 1.501, "nose gap <= 1.50 mm at every radius")

for pr, lbl in ((1.80, "Dia5.0 fragment nested in the chamfer"),
                (2.95, "Dia6.0 fragment"),
                (4.08, "Dia7.0 fragment"),
                (6.00, "Dia9.0-class shard")):
    for r in (22.0, 32.0, 46.5):
        o = loc2w(r, 14.0, DISC_TOP + pr)
        d = loc2w(0, -1, 0) - loc2w(0, 0, 0)
        loc, _, tri = hm.ray.intersects_location(
            ray_origins=o[None, :], ray_directions=d[None, :],
            multiple_hits=False)
        if not len(loc):
            print(f"      {pr:4.2f} mm proud, r={r:4.1f}: NO CONTACT")
            continue
        n = hm.face_normals[tri[0]]
        ny = float(n[0] * -sa + n[1] * ca)
        nz = float(n[2])
        yl = float(-loc[0][0] * sa + loc[0][1] * ca)
        ang = math.degrees(math.atan2(abs(ny), abs(nz)))
        print(f"      {pr:4.2f} mm proud, r={r:4.1f}: first contact at local "
              f"y={yl:+6.2f}, normal (ny={ny:+.3f}, nz={nz:+.3f}) -> face "
              f"{ang:5.1f} deg from horizontal, lift/push "
              f"{abs(nz)/max(abs(ny), 1e-9):5.2f}")

# ------------------------------------------------------- 5. torque path
print("\n[5] TORQUE PATH (B2) -- the disc bore must carry a D-flat on the "
      "vendor's Dia6 shaft with a 0.5 mm flat, over >= 10 mm.\n"
      "    A FAILING part reads r = 3.05 at every angle (a plain round bore, "
      "which is what r6 shipped).")
disc = stl("pocket_disc")
# the D-cut engagement is the top 12 mm of the disc bore, measured UP from the
# disc bottom face (the bbox max is the hub, which is a different feature -- a
# probe referenced to it reads r = 2.000 at every angle and would pass a plain
# round bore by accident)
DISC_BOT = float(disc.bounds[0][2])
for zoff in (2.0, 6.0, 10.0):
    z = DISC_BOT + zoff
    ths = np.arange(0, 360, 5.0)
    rs = np.arange(2.0, 4.0, 0.01)
    P = np.stack([np.outer(rs, np.cos(np.radians(ths))).ravel(),
                  np.outer(rs, np.sin(np.radians(ths))).ravel(),
                  np.full(len(rs) * len(ths), z)], axis=1)
    inside = disc.contains(P).reshape(len(rs), len(ths))
    rr = np.array([rs[inside[:, j]].min() if inside[:, j].any() else np.nan
                   for j in range(len(ths))])
    flat = np.nansum(rr < 2.9) * 5
    print(f"      z={z:9.3f}: bore radius min {np.nanmin(rr):.3f} max "
          f"{np.nanmax(rr):.3f}; arc with r < 2.90 = {flat} deg")
    check(np.nanmin(rr) < 2.60 and flat >= 24, f"D-flat present at z={z:.2f}")

# ------------------------------------------------------ 6. fasteners
print("\n[6] FASTENER GRIP (A-9 / NB-2), ray-measured on the exports.\n"
      "    A FAILING bay screw looks like r9's M3x12: grip 13.920 mm, "
      "engagement 0.000, tip 1.920 mm short of the housing.")
bay = stl("electronics_bay")
hou = stl("meter_housing")


def ycross(mesh, x, z):
    loc, _, _ = mesh.ray.intersects_location(
        ray_origins=np.array([[x, -95.0, z]]),
        ray_directions=np.array([[0.0, 1.0, 0.0]]))
    return sorted(float(p[1]) for p in loc)


RIB_Z = None
for z in np.arange(-330.0, -345.0, -0.05):
    if len(ycross(bay, 14.0, z)) >= 2:
        RIB_Z = float(z)
        break
print(f"    bay rib axis found at z = {RIB_Z:.3f}")
head = min(ycross(bay, 14.0, RIB_Z))
wall = min(ycross(hou, 15.4, RIB_Z))
print(f"    head bearing plane y = {head:.3f}; housing wall (off-axis ray) "
      f"y = {wall:.3f}; GRIP = {wall - head:.3f} mm")
for L in (12.0, 20.0):
    print(f"      M3x{L:.0f}: tip at y = {head + L:.3f} -> "
          f"{'engages ' + format(head + L - wall, '.3f') + ' mm' if head + L > wall else 'MISSES the housing by ' + format(wall - (head + L), '.3f') + ' mm'}")
bom = open(os.path.join(HERE, "BOM.md")).read()
check("M3x20" in bom and "M3x12 SHCS | electronics bay" not in bom,
      "BOM specifies the bay screw that actually reaches (M3x20)")
check("STOP PIN" in bom.upper(), "BOM carries the cartridge stop pin (NB-1)")
check("TSSP4038" not in bom.replace("REJECTED TSSP4038", ""),
      "BOM has no live TSSP4038 line (B4.7)")
for s in ("VBPW34FAS", "OPA2320", "TSAL6200", "PMMA"):
    check(s in bom, f"BOM contains {s}")
check("sensor PCB" in bom, "BOM carries the two sensor PCBs (NB-8)")

# ------------------------------------------------- 7. granule path spot checks
print("\n[7] GRANULE PATH spot checks on the exports.")
ch = stl("retaining_plate_chute")
_zs = np.arange(-356.0, -404.0, -1.0)
_ths = np.arange(0, 360, 30.0)
P = np.array([[32.0 + 6.5 * math.cos(math.radians(t)),
               6.5 * math.sin(math.radians(t)), z]
              for z in _zs for t in _ths])
bad = int(ch.contains(P).sum())
print(f"    Dia13 column swept down the chute axis, 48 z-stations x 12 "
      f"points: {bad} points inside material (must be 0)")
check(bad == 0, "Dia13 granule column is clear of the chute (B4.8)")

roof = stl("meter_housing")
th_probe = [300, 305, 308, 309, 310, 311, 313, 316, 320, 330, 350, 0, 20, 45, 90]
r_probe = [20.5, 24.5, 30, 32, 36, 39.5, 44, 46.5]
ROOF_TOP = float(roof.bounds[1][2])
worst = (9e9, None)
for th in th_probe:
    for r in r_probe:
        o = np.array([[r * math.cos(math.radians(th)),
                       r * math.sin(math.radians(th)), ROOF_TOP - 0.05]])
        loc, _, _ = roof.ray.intersects_location(
            ray_origins=o, ray_directions=np.array([[0.0, 0.0, -1.0]]))
        if not len(loc):
            continue
        t = (ROOF_TOP - 0.05) - float(loc[:, 2].max())
        zs = sorted(float(p[2]) for p in loc)
        thick = (ROOF_TOP - 0.05) - zs[-1] if len(zs) else 0.0
        if thick < worst[0]:
            worst = (thick, (th, r))
print(f"    B1 roof thickness, worst of {len(th_probe)*len(r_probe)} probes "
      f"outside the ramp sector: {worst[0]:.3f} mm at theta={worst[1][0]}, "
      f"r={worst[1][1]} (r9: 9.00 everywhere; r6: 0.000 at theta=310)")
check(worst[0] >= 6.0, "B1: roof >= 6.0 mm at every probe")

# ------------------------------------------------- 8. harness conduit (r5)
print("\n[8] DIRECTIVE 2 -- A CONDUCTOR MUST BE ABLE TO GET FROM THE "
      "ATTACHMENT INTERFACE TO THE ELECTRONICS BAY.\n"
      "    Measured on top_plate only, with no model constant: the conduit "
      "bores are FOUND by scanning the exported mesh, then walked.\n"
      "    A FAILING part is r10: the vertical bore axis is SOLID over "
      "z -237.50..-225.00 and the horizontal bore axis over y -84.00..-72.00, "
      "so the largest conductor that crosses the elbow is Dia0.0.")
tp = stl("top_plate")


def _solid_runs_on(mesh, pts):
    inside = mesh.contains(np.array(pts))
    runs, s0 = [], None
    for i, v in enumerate(inside):
        if v and s0 is None:
            s0 = i
        if (not v) and s0 is not None:
            runs.append((s0, i - 1))
            s0 = None
    if s0 is not None:
        runs.append((s0, len(inside) - 1))
    return runs


# the -Y spigot: 4 y-crossings on x = 0 below the plate -> the bore is the
# gap between the middle pair
_loc, _, _ = tp.ray.intersects_location(
    ray_origins=np.array([[0.0, -200.0, -244.0]]),
    ray_directions=np.array([[0.0, 1.0, 0.0]]))
spig_y = sorted(float(p[1]) for p in _loc)
print(f"    -Y spigot found at z=-244.0: y crossings "
      + " ".join(f"{v:.3f}" for v in spig_y))
SPIG_Y = (spig_y[1] + spig_y[2]) / 2 if len(spig_y) >= 4 else -81.0
SPIG_D = (spig_y[2] - spig_y[1]) if len(spig_y) >= 4 else float("nan")
print(f"    spigot axis y = {SPIG_Y:.3f}, bore Dia{SPIG_D:.3f}")
# the horizontal bore height: on the tube's mid-run (y = -50) find the open
# z-run that has material on BOTH sides -- that is a bore, not free air
zz = np.arange(-242.0, -220.0, 0.05)
P = np.stack([np.zeros_like(zz), np.full_like(zz, -50.0), zz], axis=1)
inside = tp.contains(P)
ZH, ZH_D = None, float("nan")
i = 0
while i < len(zz):
    if not inside[i]:
        j = i
        while j < len(zz) and not inside[j]:
            j += 1
        if i > 0 and j < len(zz):          # material on both sides = a bore
            ZH = float((zz[i] + zz[j - 1]) / 2)
            ZH_D = float(zz[j - 1] - zz[i])
            break
        i = j
    i += 1
print(f"    horizontal bore recovered on the mid-run (x=0, y=-50): axis "
      f"z = {ZH:.3f}, bore height {ZH_D:.3f} mm")
# (1) the horizontal bore must be open from the spigot to the neck wall
yy = np.arange(SPIG_Y, -18.0, 0.25)
P = np.stack([np.zeros_like(yy), yy, np.full_like(yy, ZH)], axis=1)
runs = _solid_runs_on(tp, P)
print(f"    HORIZONTAL BORE AXIS (x=0, z={ZH:.3f}) over y {SPIG_Y:.1f}..-18 at "
      f"0.25 mm: " + ("NO SOLID POINT" if not runs else "SOLID over " +
                      ", ".join(f"y {yy[a]:.2f}..{yy[b]:.2f}" for a, b in runs)))
check(not runs, "horizontal conduit bore is open end to end (r10: solid over "
                "y -84.00..-72.00)")
# (2) the vertical bore must be open from the elbow tangent DOWN to the tip
zv = np.arange(ZH - 8.0, float(tp.bounds[0][2]) + 0.5, -0.25)
P = np.stack([np.zeros_like(zv), np.full_like(zv, SPIG_Y), zv], axis=1)
runs = _solid_runs_on(tp, P)
print(f"    VERTICAL BORE AXIS (x=0, y={SPIG_Y:.3f}) from the elbow tangent "
      f"z={ZH - 8.0:.2f} DOWN to the spigot tip {zv[-1]:.2f} at 0.25 mm: "
      + ("NO SOLID POINT" if not runs else "SOLID over " +
         ", ".join(f"z {zv[a]:.2f}..{zv[b]:.2f}" for a, b in runs)))
check(not runs, "vertical conduit bore is open from the elbow to the tip "
                "(r10: solid over z -237.50..-225.00)")
# (3) walk a bundle round the corner between the two bores
tp_step = step("top_plate")
best = 0.0
for dia in (3.0, 4.0, 5.0, 5.5, 6.0, 7.0):
    vv = 0.0
    for k in range(17):
        a_ = math.radians(90.0 * k / 16.0)
        R = 8.0
        cy = (SPIG_Y + R) - R * math.cos(a_)
        cz = (ZH - R) + R * math.sin(a_)
        vv += inter(Pos(0.0, cy, cz) * Sphere(dia / 2), tp_step)
    print(f"      Dia{dia:.1f} bundle walked round the R8 corner from the "
          f"horizontal bore to the vertical bore: {vv:.4f} mm3")
    if vv < 1e-3:
        best = dia
print(f"    -> largest conductor bundle that crosses the elbow = "
      f"Dia{best:.1f} (r10: Dia0.0)")
check(best >= 5.5, "a Dia5.5 9-conductor bundle can cross the elbow")

# ------------------------------------------- 9. A-10 gearbox screw head
print("\n[9] A-10 -- THE GEARBOX SCREW HEAD MUST FIT THE SEAT THE PLATE HAS.\n"
      "    The seat is measured on the export; then the ORDERED head is "
      "tested against the disc.\n    A FAILING BOM is r10's: `M3x8 SHCS` for "
      "a 90 deg countersink -> 8.8652 mm3 static and 49.4066 mm3 swept.")
pl = stl("retaining_plate_chute")
PLATE_TOP2 = None
_loc, _, _ = pl.ray.intersects_location(
    ray_origins=np.array([[13.0, 6.0, -300.0]]),
    ray_directions=np.array([[0.0, 0.0, -1.0]]))
PLATE_TOP2 = float(max(p[2] for p in _loc))
prof = []
for dz in np.arange(0.05, 2.0, 0.1):
    z = PLATE_TOP2 - dz
    _loc, _, _ = pl.ray.intersects_location(
        ray_origins=np.array([[13.0, 0.0, z]]),
        ray_directions=np.array([[1.0, 0.0, 0.0]]))
    if len(_loc):
        prof.append((z, float(min(p[0] for p in _loc)) - 13.0))
print(f"    plate top z = {PLATE_TOP2:.3f}; hole profile on the (13,0) axis:")
for z, r in prof:
    print(f"      z={z:9.3f}  r={r:6.3f}")
cs_mouth = 2 * max(r for _, r in prof)
cs_shank = 2 * min(r for _, r in prof)
print(f"    -> countersink mouth Dia{cs_mouth:.3f}, shank Dia{cs_shank:.3f} "
      f"(a plain cap-head seat would read a CONSTANT r over the whole depth)")
check(cs_mouth > 5.0 and cs_shank < 3.6,
      "the plate has a countersunk seat, not a cap-head counterbore")
plate_s = step("retaining_plate_chute")
disc_s = step("pocket_disc")
cap = None
flat = None
for (hx, hy) in ((13.0, 0.0), (-13.0, 0.0), (0.0, 13.0), (0.0, -13.0)):
    c = Pos(hx, hy, PLATE_TOP2 - 1.35 + 1.05 + 1.5) * Cylinder(2.75, 3.0)
    f = Pos(hx, hy, PLATE_TOP2 - 0.675) * Cylinder(3.05, 1.35)
    cap = c if cap is None else cap + c
    flat = f if flat is None else flat + f
print(f"    ISO 10642 flat head (flush, Dia6.1 -> Dia3.0) ^ pocket_disc = "
      f"{inter(flat, disc_s):.4f} mm3")
print(f"    Dia5.5 x 3.0 CAP HEAD control      ^ pocket_disc = "
      f"{inter(cap, disc_s):.4f} mm3   (r10 assembly critic: 8.8652)")
check(inter(flat, disc_s) < 1e-3, "flush countersunk head clears the disc")
check(inter(cap, disc_s) > 1.0,
      "the cap-head control DOES foul (so the flat-head 0.0000 is meaningful)")
bom2 = open(os.path.join(HERE, "BOM.md")).read()
check("M3x8 SHCS | gearbox" not in bom2.replace("**", ""),
      "BOM no longer orders a cap head for the gearbox joint")
check(("10642" in bom2) or ("7991" in bom2),
      "BOM names a 90 deg countersunk screw (ISO 10642 / DIN 7991)")

# ------------------------------------- 10. tether lug in the drop tube
print("\n[10] GRANULE-PATH MAJOR -- NOTHING MAY STAND PROUD OF THE DROP-TUBE "
      "BORE.\n     A FAILING part is r10: r_min 10.000 in an r11.000 bore "
      "over z -398.00..-404.00 (a 6.0 x 8.0 mm ledge in the fall path).")
CH_X = 32.0
worst_r = (99.0, None)
for z in np.arange(-390.0, -405.1, -0.5):
    org, dirs = [], []
    for a in range(0, 360, 2):
        ra = math.radians(a)
        org.append([CH_X, 0.0, float(z)])
        dirs.append([math.cos(ra), math.sin(ra), 0.0])
    loc, ir, _ = pl.ray.intersects_location(ray_origins=np.array(org),
                                            ray_directions=np.array(dirs))
    if not len(loc):
        continue
    d = np.linalg.norm(loc - np.array([CH_X, 0.0, float(z)]), axis=1)
    if float(d.min()) < worst_r[0]:
        worst_r = (float(d.min()), float(z))
print(f"     minimum bore radius over z -390..-405 (2 deg x 31 heights): "
      f"{worst_r[0]:.3f} mm at z = {worst_r[1]:.2f}")
check(worst_r[0] >= 10.95, "the drop tube is Dia22 continuous to the mouth")
plug_s = step("chute_plug")
_res = plate_s & plug_s
_bodies = [] if _res is None else list(_res.solids())
_tot = sum(b.volume for b in _bodies)
print(f"     retaining_plate_chute ^ chute_plug = {_tot:.4f} mm3 in "
      f"{len(_bodies)} bodies:")
for b in sorted(_bodies, key=lambda s: -s.volume):
    bb2 = b.bounding_box()
    print(f"        {b.volume:9.4f} mm3  x[{bb2.min.X:7.2f},{bb2.max.X:7.2f}] "
          f"y[{bb2.min.Y:7.2f},{bb2.max.Y:7.2f}] "
          f"z[{bb2.min.Z:9.3f},{bb2.max.Z:9.3f}]")
print(f"     the ONLY designed interference is the Dia22.3 land in the Dia22.0 "
      f"bore over 8 mm = 2*pi*11.075*0.15*8 = 83.5 mm3 (r10 logged all "
      f"206.0993 mm3 as 'the designed 0.3 mm press fit')")
check(_tot < 95.0, "plate ^ plug is the press fit and nothing else "
                   "(r10: 206.0993)")

print("\n" + "=" * 78)
if FAIL:
    print(f"{len(FAIL)} CHECK(S) FAILED:")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
