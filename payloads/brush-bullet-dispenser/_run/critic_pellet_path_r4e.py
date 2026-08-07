#!/usr/bin/env python
"""Pass E: linear scans (no bad binary brackets) - chamber wall, rim fines
slots, pocket phase, and a transit test with the disc actually indexed."""
import math, numpy as np
from build123d import import_step, Sphere, Pos, Rot, Cylinder, Box

E = "/Users/hex/projects/payload-systems/payloads/brush-bullet-dispenser/cad/exports/"
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

print("== chamber wall ID over the fill sector (linear scan, th=190, z=-283) ==")
t = math.radians(190.0)
prof = [(r, mat("meter_housing", r*math.cos(t), r*math.sin(t), -283.0)) for r in np.arange(14.0, 56.0, 0.25)]
runs = []
cur = None
for r, m in prof:
    if m and cur is None: cur = r
    if not m and cur is not None: runs.append((cur, r-0.25)); cur = None
if cur is not None: runs.append((cur, prof[-1][0]))
print(f"   housing material bands at z=-283, th=190: {[(round(a,2),round(b,2)) for a,b in runs]}")
open_bands = []
prev = 14.0
for a, b in runs:
    if a - prev > 0.3: open_bands.append((prev, a))
    prev = b
print(f"   -> open radial bands: {[(round(a,2),round(b,2)) for a,b in open_bands]}")
if open_bands:
    w = max(b-a for a,b in open_bands)
    print(f"   -> widest sump aperture = {w:.2f} mm = {w/13.0:.2f} x 13 mm pellet, {w/12.0:.2f} x 12 mm")

print("\n== rim fines slots: through-plate openings, per degree ==")
rp = "retaining_plate_chute"
res = []
for thd in np.arange(0, 360, 1.0):
    t = math.radians(thd)
    best = 0.0; run = 0.0; where = None; start = None
    for r in np.arange(43.0, 54.0, 0.25):
        x, y = r*math.cos(t), r*math.sin(t)
        # through-plate: sample top, mid, bottom
        through = not (mat(rp, x, y, -300.8) or mat(rp, x, y, -302.5) or mat(rp, x, y, -304.2))
        if through:
            if start is None: start = r
            run += 0.25
            if run > best: best = run; where = (start, r)
        else:
            run = 0.0; start = None
    res.append((thd, best, where))
opened = [(t, b, w) for t, b, w in res if b >= 2.0]
print(f"   degrees with a >=2.0 mm through-slot in r43..54: {len(opened)} of 360 ({len(opened)/3.6:.0f}%)")
if opened:
    print(f"   slot radial band seen: {min(w[0] for _,_,w in opened):.2f}..{max(w[1] for _,_,w in opened):.2f}")
    ang = sorted(t for t,_,_ in opened)
    arcs=[]; st=ang[0]; pv=ang[0]
    for a in ang[1:]:
        if a-pv <= 1.5: pv=a
        else: arcs.append((st,pv)); st=a; pv=a
    arcs.append((st,pv))
    print(f"   slot arcs: {[(round(a),round(b)) for a,b in arcs]}")
wide = [(t,b) for t,b,w in res if b >= 4.0]
print(f"   degrees with a >=4.0 mm through-slot: {len(wide)} of 360 ({len(wide)/3.6:.0f}%)")

print("\n== pocket phase in the exported disc ==")
found = []
for thd in np.arange(0, 360, 1.0):
    t = math.radians(thd)
    if not mat("pocket_disc", 32*math.cos(t), 32*math.sin(t), -295.0):
        found.append(thd)
arcs=[]; st=found[0]; pv=found[0]
for a in found[1:]:
    if a-pv <= 1.5: pv=a
    else: arcs.append((st,pv)); st=a; pv=a
arcs.append((st,pv))
centers = [ (a+b)/2 for a,b in arcs ]
print(f"   open (pocket) arcs at r32,z-295: {[(round(a),round(b)) for a,b in arcs]}")
print(f"   -> pocket centres approx {[round(c,1) for c in centers]}")

print("\n== transit with the disc INDEXED (rotate the exported disc) ==")
PATH = ["top_plate","hopper","meter_housing","agitator","brush_strip","retaining_plate_chute"]
disc = sol["pocket_disc"]
p0 = centers[0] % 45.0
def probe_at(thd, z, d=13.0):
    """put a pellet at pocket angle thd; rotate the disc so a pocket is there."""
    dr = Rot(Z=(thd - p0)) * disc
    sp = Pos(32*math.cos(math.radians(thd)), 32*math.sin(math.radians(thd)), z) * Sphere(d/2)
    v = sum(ivol(sp, sol[n]) for n in PATH) + ivol(sp, dr)
    return v
print("   a) descending into a pocket at th=190 (mid fill window):")
for z in np.arange(-273.0, -295.1, -1.5):
    print(f"      z={z:8.2f}  overlap {probe_at(190.0, z):9.3f} mm3")
print("   b) seated pellet carried round the transfer arc (z=-294.0):")
for thd in (250.0, 190.0, 135.0, 133.0, 130.0, 129.0, 127.0, 125.0, 112.5, 90.0, 45.0, 22.5, 10.0, 0.0):
    print(f"      th={thd:6.1f}  overlap {probe_at(thd, -294.0):9.3f} mm3")
print("   c) 12 mm nominal pellet, same arc:")
for thd in (133.0, 129.0, 125.0, 90.0, 0.0):
    print(f"      th={thd:6.1f}  overlap {probe_at(thd, -294.0, 12.0):9.3f} mm3")

print("\n== rider pellet on a seated pellet vs the bar / roof edge ==")
# rider centre 13 mm above seated centre: seated centre z=-294.0 -> rider centre -281.0
for thd in (140.0, 135.0, 133.0, 131.0, 129.0):
    dr = Rot(Z=(thd - p0)) * disc
    sp = Pos(32*math.cos(math.radians(thd)), 32*math.sin(math.radians(thd)), -281.0) * Sphere(6.5)
    hits = {n: ivol(sp, sol[n]) for n in ("meter_housing","brush_strip","agitator")}
    print(f"   rider at th={thd:5.1f}: " + "  ".join(f"{k}={v:8.2f}" for k,v in hits.items()))
