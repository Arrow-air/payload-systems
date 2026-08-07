#!/usr/bin/env python
"""Round-4 pellet-path critic, pass D: sump aperture, fines paths, agitator
coverage, continuous worst-case transit. Exports only."""
import math, numpy as np, trimesh
from build123d import import_step, Sphere, Pos, Rot, Cylinder, Box

E = "/Users/hex/projects/payload-systems/payloads/brush-bullet-dispenser/cad/exports/"
NAMES = ["top_plate", "fill_cap", "hopper", "meter_housing", "pocket_disc",
         "agitator", "brush_strip", "retaining_plate_chute", "electronics_bay"]
sol = {n: import_step(E + n + "_r4.step") for n in NAMES}
def ivol(a, b):
    try:
        r = a & b
        if r is None: return 0.0
        return r.volume if hasattr(r, "volume") else sum(x.volume for x in r)
    except Exception:
        return float("nan")

mh = sol["meter_housing"]

print("== sump aperture at the roof plane (theta 190 deg, mid fill sector) ==")
th = math.radians(190.0)
for z in (-284.0, -282.5, -281.0):
    # inner collar outer radius
    lo, hi = 10.0, 30.0
    for _ in range(20):
        mid=(lo+hi)/2
        v = ivol(Pos(mid*math.cos(th), mid*math.sin(th), z)*Cylinder(0.15,0.3), mh)
        if v > 0.002: lo = mid
        else: hi = mid
    collar = hi
    lo2, hi2 = 30.0, 60.0
    for _ in range(20):
        mid=(lo2+hi2)/2
        v = ivol(Pos(mid*math.cos(th), mid*math.sin(th), z)*Cylinder(0.15,0.3), mh)
        if v > 0.002: hi2 = mid
        else: lo2 = mid
    wall = hi2
    print(f"   z={z}: collar OD r={collar:6.3f}  chamber wall ID r={wall:6.3f}  ->"
          f" radial aperture {wall-collar:6.3f} mm = {(wall-collar)/13.0:.2f} x 13 mm pellet")

print("\n== angular extent of the sump aperture at z=-282.5 (r=32) ==")
open_th = []
for thd in np.arange(120.0, 262.0, 0.5):
    t = math.radians(thd)
    v = ivol(Pos(32*math.cos(t), 32*math.sin(t), -282.5)*Cylinder(0.2,0.3), mh)
    if v < 0.002: open_th.append(thd)
print(f"   open from {min(open_th):.1f} to {max(open_th):.1f} deg = {max(open_th)-min(open_th):.1f} deg;"
      f" arc length at r32 = {math.radians(max(open_th)-min(open_th))*32:.1f} mm")

print("\n== agitator finger geometry (count, angular width, radial reach) ==")
ag = sol["agitator"]
for z in (-279.0, -276.0):
    hits = []
    for thd in np.arange(0, 360, 1.0):
        t = math.radians(thd)
        v = sum(ivol(Pos(r*math.cos(t), r*math.sin(t), z)*Cylinder(0.2,0.3), ag) for r in (20,30,40,44))
        hits.append((thd, v > 0.002))
    runs=[]; cur=None
    for thd, h in hits:
        if h and cur is None: cur=thd
        if not h and cur is not None: runs.append((cur, thd-1)); cur=None
    if cur is not None: runs.append((cur, 359))
    print(f"   z={z}: {len(runs)} finger(s): {runs}")
# radial reach at a finger
t = math.radians(0.0)
for thd in np.arange(0,360,1.0):
    t = math.radians(thd)
    if ivol(Pos(40*math.cos(t),40*math.sin(t),-278.0)*Cylinder(0.2,0.3), ag) > 0.002:
        break
lo, hi = 0.0, 20.0
for _ in range(18):
    mid=(lo+hi)/2
    v = ivol(Pos(mid*math.cos(t), mid*math.sin(t), -278.0)*Cylinder(0.15,0.3), ag)
    if v > 0.002: hi = mid
    else: lo = mid
print(f"   finger at th={thd:.0f}: inner radius {hi:.2f}")
lo, hi = 40.0, 50.0
for _ in range(18):
    mid=(lo+hi)/2
    v = ivol(Pos(mid*math.cos(t), mid*math.sin(t), -278.0)*Cylinder(0.15,0.3), ag)
    if v > 0.002: lo = mid
    else: hi = mid
print(f"   finger at th={thd:.0f}: outer radius {lo:.2f}   (sump shelf runs r13.5..47.0)")
bb = ag.bounding_box(); print(f"   agitator z {bb.min.Z:.2f}..{bb.max.Z:.2f}; shelf top z=-280.50 -> under-finger gap {abs(-280.5-bb.min.Z):.2f} mm")

print("\n== retaining plate: through-openings at mid-plate z=-302.5 (angle x radius) ==")
rp = sol["retaining_plate_chute"]
rows = []
for thd in np.arange(0, 360, 1.0):
    t = math.radians(thd)
    openr = []
    for r in np.arange(42.0, 54.0, 0.5):
        v = ivol(Pos(r*math.cos(t), r*math.sin(t), -302.5)*Cylinder(0.2,0.3), rp)
        if v < 0.002: openr.append(r)
    rows.append((thd, openr))
cov = [t for t, o in rows if len(o) >= 6]   # >=3 mm of continuous open radius
print(f"   degrees with >=3.0 mm open radial band in r42..54: {len(cov)} of 360 ({len(cov)/3.6:.0f}%)")
if cov:
    o = [r for t, orr in rows for r in orr]
    print(f"   open radii seen {min(o):.1f}..{max(o):.1f}")

print("\n== what is under the rim fines slots (does dust land on hardware)? ==")
for thd in (180.0, 200.0, 300.0):
    t = math.radians(thd)
    col = Pos(47.5*math.cos(t), 47.5*math.sin(t), -320.0) * Cylinder(2.0, 40.0)  # z -340..-300
    for n in NAMES:
        v = ivol(col, sol[n])
        if v > 0.01:
            print(f"   th={thd}: column below slot hits {n} = {v:.1f} mm3")
    print(f"   th={thd}: column scan done")

print("\n== continuous worst-case 13 mm sphere transit (fine steps) ==")
PATH = ["top_plate","hopper","meter_housing","pocket_disc","agitator","brush_strip","retaining_plate_chute"]
def probe(x,y,z,d=13.0):
    sp = Pos(x,y,z)*Sphere(d/2)
    return sum(ivol(sp, sol[n]) for n in PATH)
worst = []
# a) descent through the sump aperture into a pocket at theta 190 (mid window)
t = math.radians(190.0)
for z in np.arange(-273.0, -294.1, -1.0):
    v = probe(32*math.cos(t), 32*math.sin(t), z)
    worst.append((f"fill th190 z={z:.1f}", v))
# b) seated pellet carried round the transfer arc (indexed positions)
for thd in (133.0, 129.0, 125.0, 112.5, 90.0, 67.5, 45.0, 22.5, 5.0, 0.0):
    t = math.radians(thd)
    v = probe(32*math.cos(t), 32*math.sin(t), -294.0)
    worst.append((f"seated th={thd}", v))
# c) drop through exit and chute
for z in np.arange(-297.0, -356.0, -3.0):
    worst.append((f"chute z={z:.1f}", probe(32.0, 0.0, z)))
bad = [(k, v) for k, v in worst if v > 0.01]
print(f"   {len(worst)} probes, {len(bad)} with material overlap")
for k, v in bad: print(f"     HIT {k}: {v:.3f} mm3")

print("\n== vertical gaps over a seated worst-case pellet (top at z=-287.50) ==")
for name, zref in (("bar underside (r26-44)", -284.80), ("roof underside", -284.50), ("disc top", -286.00)):
    print(f"   {name:26s} z={zref:8.2f} -> gap above seated pellet {zref-(-287.50):6.2f} mm")
print("   stacked 2nd 13 mm sphere: bottom -287.50, top -274.50 -> protrudes 11.50 mm above disc top")
print("   stacked 2nd 9 mm barrel on a 9 mm seated barrel: top = -300.50+18 = -282.50 -> protrudes 3.50 mm")
print("   seated 9 mm barrel alone: top -291.50 -> 5.50 mm BELOW disc top (bar cannot touch it)")
