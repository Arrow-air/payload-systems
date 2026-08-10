#!/usr/bin/env python3
"""rev-1 close-out r13 verification (independent of dispenser.py's own checks).

Measures the exported STEP/STL files directly:
  1. B2.2 -- grub corridor booleans on pocket_disc_r13.step: coaxial corridors
     at Dia0.7 / Dia1.9 / Dia2.6 on the grub axis (theta=202.5, Z=-341.25)
     from r=46.5 inward to the shaft FLAT at r=2.55. Requirement: 0.0000 mm3
     of disc material in all three. The same probes are run against
     pocket_disc_r12.step as a FAILING CONTROL (expected ~1.0619 mm3 at
     Dia2.6) -- a probe that reads 0.0000 on r12 is broken.
  2. Export integrity -- every *_r13.step/.stl pair: STL watertight, and
     STEP-vs-STL volume delta < 1 %.
Every number printed is measured here, not quoted.
"""
import glob
import math
import os

import trimesh
from build123d import Cylinder, Pos, Rot, import_step

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORTS = os.path.join(HERE, "exports")
GRUB_A = 202.5
Z_SETSCREW = -341.25
FLAT_R = 2.55
OUTER_R = 46.5

def vol_of(x):
    """ShapeList-safe volume (same idiom as dispenser.py's helper)."""
    if x is None:
        return 0.0
    if hasattr(x, "volume"):
        return x.volume
    return sum(vol_of(i) for i in x)

def corridor_material(disc_shape, dia, r_in):
    """mm3 of disc material inside a coaxial corridor from OUTER_R to r_in."""
    length = OUTER_R - r_in
    corr = Rot(Z=GRUB_A) * (Pos((r_in + OUTER_R) / 2.0, 0, Z_SETSCREW)
                            * Rot(Y=90) * Cylinder(dia / 2.0, length))
    return vol_of(corr.intersect(disc_shape))

def check_disc(tag):
    path = os.path.join(EXPORTS, f"pocket_disc_{tag}.step")
    shape = import_step(path)
    print(f"\n  {os.path.basename(path)} (STEP volume {shape.volume/1000:.3f} cm3)")
    results = {}
    for dia in (0.7, 1.9, 2.6):
        v = corridor_material(shape, dia, FLAT_R)
        results[dia] = v
        print(f"    Dia{dia:.1f} corridor r={OUTER_R} -> r={FLAT_R} : "
              f"disc material = {v:.4f} mm3")
    return results

print("=== B2.2 grub corridor to the shaft flat "
      f"(theta={GRUB_A}, Z={Z_SETSCREW}, flat r={FLAT_R}) ===")
r13 = check_disc("r13")
r12 = check_disc("r12")

ok_r13 = all(v < 1e-4 for v in r13.values())
ctrl = r12[2.6]
ok_ctrl = 0.9 < ctrl < 1.3
print(f"\n  r13 corridors clear: {'PASS' if ok_r13 else 'FAIL'}")
print(f"  r12 failing control at Dia2.6: {ctrl:.4f} mm3 "
      f"(expected ~1.0619 = pi*1.30^2*0.200) -> "
      f"{'CONTROL VALID' if ok_ctrl else 'CONTROL BROKEN -- probe suspect'}")

print("\n=== r13 export integrity (watertight + STEP-vs-STL volume) ===")
fails = []
for step_path in sorted(glob.glob(os.path.join(EXPORTS, "*_r13.step"))):
    base = os.path.basename(step_path)[:-5]
    stl_path = os.path.join(EXPORTS, base + ".stl")
    shape = import_step(step_path)
    mesh = trimesh.load(stl_path)
    delta = abs(mesh.volume - shape.volume) / shape.volume * 100.0
    wt = mesh.is_watertight
    status = "ok" if (wt and delta < 1.0) else "FAIL"
    if status == "FAIL":
        fails.append(base)
    print(f"  {base:32s} watertight={wt}  STEP {shape.volume/1000:9.3f} cm3  "
          f"STL {mesh.volume/1000:9.3f} cm3  delta {delta:.3f}%  {status}")

print(f"\n=== VERDICT: B2.2 {'CLOSED' if ok_r13 and ok_ctrl else 'OPEN'}; "
      f"export integrity {'PASS' if not fails else 'FAIL: ' + ', '.join(fails)} ===")
