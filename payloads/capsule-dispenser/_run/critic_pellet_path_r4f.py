#!/usr/bin/env python
"""Pass F: retaining-plate rim trough / fines slot map, and the transit test
with the pocket phase fixed (pockets at 0,45,...,315 deg in the export)."""
import math, numpy as np
from build123d import import_step, Sphere, Pos, Rot, Cylinder

E = "/Users/hex/projects/payload-systems/payloads/capsule-dispenser/cad/exports/"
NAMES = ["top_plate","hopper","meter_housing","pocket_disc","agitator",
         "brush_strip","retaining_plate_chute"]
sol = {n: import_step(E + n + "_r4.step") for n in NAMES}
def ivol(a, b):
    try:
        r = a & b
        if r is None: return 0.0
        return r.volume if hasattr(r, "volume") else sum(x.volume for x in r)
    except Exception:
        return float("nan")
def mat(part, x, y, z, r=0.15, h=0.3):
    return ivol(Pos(x, y, z) * Cylinder(r, h), sol[part]) > 0.002

rp = "retaining_plate_chute"
print("== retaining plate r-z profile at selected angles (material map) ==")
for thd in (180.0, 200.0, 300.0, 20.0, 90.0):
    t = math.radians(thd)
    print(f"  theta={thd}")
    for z in (-300.7, -301.5, -302.5, -303.5, -304.3):
        row = ""
        for r in np.arange(42.0, 56.0, 0.5):
            row += "#" if mat(rp, r*math.cos(t), r*math.sin(t), z) else "."
        print(f"    z={z:8.2f} r42->55.5 : {row}")

print("\n== through-plate openings, per degree, r 42..56 (top -300.7 to bottom -304.3) ==")
res = []
for thd in np.arange(0, 360, 1.0):
    t = math.radians(thd)
    best = 0.0; run = 0.0; start = None; where = None
    for r in np.arange(42.0, 56.0, 0.25):
        x, y = r*math.cos(t), r*math.sin(t)
        through = not (mat(rp, x, y, -300.7) or mat(rp, x, y, -302.5) or mat(rp, x, y, -304.3))
        if through:
            if start is None: start = r
            run += 0.25
            if run > best: best = run; where = (start, r)
        else:
            run = 0.0; start = None
    res.append((thd, best, where))
for thr in (1.0, 2.0, 3.0, 4.0):
    n = sum(1 for _, b, _ in res if b >= thr)
    print(f"   >= {thr:.1f} mm continuous through-opening: {n} of 360 deg ({n/3.6:.0f}%)")
op = [(t,b,w) for t,b,w in res if b >= 2.0]
if op:
    ang = [t for t,_,_ in op]
    arcs=[]; st=ang[0]; pv=ang[0]
    for a in ang[1:]:
        if a-pv<=1.5: pv=a
        else: arcs.append((st,pv)); st=a; pv=a
    arcs.append((st,pv))
    print(f"   arcs with >=2 mm opening: {[(round(a),round(b)) for a,b in arcs]}")
    print(f"   radial band: {min(w[0] for _,_,w in op):.2f}..{max(w[1] for _,_,w in op):.2f}")

print("\n== does the trough drain? open volume above vs below the trough floor ==")
for thd in (180.0, 300.0):
    t = math.radians(thd)
    print(f"  theta={thd}: trough column material by z")
    for z in np.arange(-300.4, -305.6, -0.4):
        row = "".join("#" if mat(rp, r*math.cos(t), r*math.sin(t), z) else "." for r in np.arange(44.0, 56.0, 0.5))
        print(f"    z={z:8.2f} r44->55.5 : {row}")

print("\n== TRANSIT, pocket phase = 0/45/.../315 (correct) ==")
PATH = ["top_plate","hopper","meter_housing","agitator","brush_strip","retaining_plate_chute"]
disc = sol["pocket_disc"]
def probe_at(thd, z, d=13.0, dr_cache={}):
    k = round(thd % 45.0, 3)
    if k not in dr_cache: dr_cache[k] = Rot(Z=thd) * disc
    dr = Rot(Z=thd) * disc
    sp = Pos(32*math.cos(math.radians(thd)), 32*math.sin(math.radians(thd)), z) * Sphere(d/2)
    return sum(ivol(sp, sol[n]) for n in PATH) + ivol(sp, dr)
print("  a) 13 mm sphere descending into a pocket at th=190:")
for z in np.arange(-273.0, -294.6, -1.5):
    print(f"     z={z:8.2f}  overlap {probe_at(190.0, z):9.3f} mm3")
print("  b) 13 mm seated pellet round the transfer arc (centre z=-293.9):")
for thd in (250.0, 190.0, 140.0, 135.0, 133.0, 130.0, 129.0, 127.0, 112.5, 90.0, 45.0, 22.5, 5.0, 0.0):
    print(f"     th={thd:6.1f}  overlap {probe_at(thd, -293.9):9.3f} mm3")
print("  c) rider (2nd sphere) centre z=-280.9 vs the wiper/roof:")
for thd in (145.0, 140.0, 137.0, 135.0, 133.0, 131.0, 129.0):
    dr = Rot(Z=thd) * disc
    sp = Pos(32*math.cos(math.radians(thd)), 32*math.sin(math.radians(thd)), -280.9) * Sphere(6.5)
    print(f"     th={thd:6.1f}  housing={ivol(sp, sol['meter_housing']):8.2f}  bar={ivol(sp, sol['brush_strip']):8.2f}"
          f"  agitator={ivol(sp, sol['agitator']):8.2f}  disc={ivol(sp, dr):8.2f}")
