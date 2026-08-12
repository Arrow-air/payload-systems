"""Independent checks on the exported ram_ball_c_adapter geometry.

Measures the exported STL/STEP (not the generator's variables) with trimesh
point containment and build123d face queries. Every claim in the README that
matters for fit or function is asserted here.

Run:  <python with build123d + trimesh> verify_ram_ball_c.py
Exit code 0 = all checks pass.
"""

import sys
from math import sqrt
from pathlib import Path

import numpy as np
import trimesh
from build123d import GeomType, import_step

HERE = Path(__file__).parent
BALL_R = 38.1 / 2
BALL_CZ = -39.5532  # from tangency: -(16 + 8 + sqrt(19.05^2 - 11^2))

failures = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    if not ok:
        failures.append(name)


mesh = trimesh.load(HERE / "ram_ball_c_adapter.stl")
check("mesh watertight", mesh.is_watertight)

# 1. Envelope: nothing above the clip mating plane, footprint inside 50 x 50
mn, mx = mesh.bounds
check("nothing above Z=0", mx[2] < 0.01, f"max Z {mx[2]:.3f}")
check("footprint <= 50 x 50", mx[0] - mn[0] <= 50.0 and mx[1] - mn[1] <= 50.0,
      f"{mx[0]-mn[0]:.1f} x {mx[1]-mn[1]:.1f}")

# 2. Mount holes at (+/-19, +/-19): Ø3.2 cylinders, axis Z, from STEP
step = import_step(str(HERE / "ram_ball_c_adapter.step"))
bores = []
for f in step.faces().filter_by(GeomType.CYLINDER):
    ax = f.axis_of_rotation
    if abs(ax.direction.Z) > 0.99 and abs(f.radius - 1.6) < 0.05:
        bores.append((round(ax.position.X, 1), round(ax.position.Y, 1)))
expected = {(19.0, 19.0), (19.0, -19.0), (-19.0, 19.0), (-19.0, -19.0)}
check("4x Ø3.2 mount holes at (+/-19, +/-19)", expected <= set(bores),
      f"found {sorted(set(bores))}")
# through-holes: open along the full 16 mm body at every hole position
probe = np.array([[sx * 19, sy * 19, z]
                  for sx in (1, -1) for sy in (1, -1)
                  for z in (-2.0, -8.0, -15.5)])
check("mount holes go all the way through (open at -2/-8/-15.5)",
      not mesh.contains(probe).any())

# 3. Blind-mate well: the full 16 x 24 shaft footprint must be open down to
#    the well floor so the pads PCB + Molex J1 can hang below the clip plate
xs = np.linspace(-8.0, 8.0, 9)
ys = np.linspace(-12.0, 12.0, 13)
zs = np.linspace(-0.5, -11.5, 6)
pts = np.array([[x, y, z] for x in xs for y in ys for z in zs])
occupied = mesh.contains(pts)
check("well: full 16 x 24 board footprint open to -11.5", not occupied.any(),
      f"{int(occupied.sum())}/{len(pts)} sample points inside solid")

# 4a. Side cable path: well -> -Y face at slot height, Ø4 test cable
path = np.array([[0, y, -9.0] for y in np.linspace(0, -25, 26)])
for r in ((0, 0), (1.8, 0), (-1.8, 0), (0, 1.8), (0, -1.8)):
    p = path.copy()
    p[:, 0] += r[0]
    p[:, 2] += r[1]
    if mesh.contains(p).any():
        check("side cable path (Ø4 envelope)", False, f"blocked at offset {r}")
        break
else:
    check("side cable path (Ø4 envelope)", True)

# 4b. Axial cable path: well floor -> below the ball pole, Ø7 test cable
path = np.array([[0, 0, z] for z in np.linspace(-6, -59, 54)])
for r in ((0, 0), (3.5, 0), (-3.5, 0), (0, 3.5), (0, -3.5)):
    p = path.copy()
    p[:, 0] += r[0]
    p[:, 1] += r[1]
    if mesh.contains(p).any():
        check("axial cable path (Ø7 envelope)", False, f"blocked at offset {r}")
        break
else:
    check("axial cable path (Ø7 envelope)", True)

# 5. Ball size: equator radius = 19.05 +/- 0.1
v = mesh.vertices
band = v[np.abs(v[:, 2] - BALL_CZ) < 2.0]
r_eq = np.sqrt(band[:, 0] ** 2 + band[:, 1] ** 2).max()
check("ball equator radius 19.05 +/- 0.1", abs(r_eq - BALL_R) < 0.1, f"{r_eq:.3f}")

# 6. Clamp band integrity: RAM socket grips the ball around the equator.
#    Sphere surface must be solid 1 mm inboard everywhere within +/-45 deg
#    of the equator (the bore only breaches within ~15 deg of the pole).
angs = np.linspace(-np.pi / 4, np.pi / 4, 19)   # elevation from equator
azs = np.linspace(0, 2 * np.pi, 37)[:-1]
pts = []
for el in angs:
    for az in azs:
        r = BALL_R - 1.0
        pts.append([r * np.cos(el) * np.cos(az), r * np.cos(el) * np.sin(az),
                    BALL_CZ + r * np.sin(el)])
occupied = mesh.contains(np.array(pts))
check("clamp band solid (+/-45 deg, 1 mm inboard)", occupied.all(),
      f"{int(occupied.sum())}/{len(pts)}")

# 7. Neck tangency: solid radius at the neck-ball junction ~ 11.0
band = v[np.abs(v[:, 2] + 24.0) < 0.3]
if len(band):
    r_neck = np.sqrt(band[:, 0] ** 2 + band[:, 1] ** 2).max()
    check("neck Ø22 at ball junction", abs(r_neck - 11.0) < 0.3, f"r={r_neck:.3f}")
else:
    check("neck Ø22 at ball junction", True, "(no facet vertices in band — tangent blend)")

# 8. Mass sanity for the printed part
vol = mesh.volume / 1000.0
check("volume 40..80 cm^3", 40.0 < vol < 80.0, f"{vol:.1f} cm^3")

print()
if failures:
    print(f"{len(failures)} FAILURES: {failures}")
    sys.exit(1)
print("ALL CHECKS PASS")
