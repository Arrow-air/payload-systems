#!/usr/bin/env python
"""Round-4 pellet-path critic, pass C: exact boolean probes on the exported
STEPs (build123d) -- brush bar section, pocket bore, exit/chute, clearances."""
import math, numpy as np
from build123d import import_step, Sphere, Pos, Rot, Cylinder, Box

E = "/Users/hex/projects/payload-systems/payloads/brush-bullet-dispenser/cad/exports/"
NAMES = ["top_plate", "fill_cap", "hopper", "meter_housing", "pocket_disc",
         "agitator", "brush_strip", "retaining_plate_chute"]
sol = {}
for n in NAMES:
    s = import_step(E + n + "_r4.step")
    sol[n] = s
    print(f"  {n:24s} solids={len(s.solids())} vol={s.volume/1000:8.3f} cm3")

def ivol(a, b):
    try:
        r = a & b
        if r is None: return 0.0
        if hasattr(r, "volume"): return r.volume
        return sum(x.volume for x in r)
    except Exception:
        return float("nan")

print("\n== BRUSH BAR true cross-section (tangential thickness x height) ==")
bs = sol["brush_strip"]
# bar runs radially at theta ~133 deg; probe with thin boxes normal to the bar
TH = 133.0
for rr in (20.0, 26.0, 32.0, 38.0, 44.0):
    # local frame: probe a 6 mm tangential x 6 mm vertical window, 0.2 radial
    hits_t, hits_z = [], []
    for t in np.arange(-4.0, 4.01, 0.1):     # tangential offset
        for zz in np.arange(-286.5, -279.0, 0.1):
            pass
    # cheaper: boolean a thin radial slab and take its bbox
    slab = Rot(Z=TH) * Pos(rr, 0, -283.5) * Box(0.4, 12.0, 10.0)
    inter = bs & slab
    if inter is None or (hasattr(inter, "volume") and inter.volume < 1e-9):
        print(f"   r={rr}: no bar material")
        continue
    bb = inter.bounding_box()
    # tangential extent = size along the local y
    v = inter.volume
    print(f"   r={rr}: slab vol {v:7.3f} mm3 over 0.4 radial -> section {v/0.4:6.3f} mm2 ; "
          f"bbox z {bb.min.Z:.2f}..{bb.max.Z:.2f} (h={bb.max.Z-bb.min.Z:.2f})")

print("\n== rigid-bar bending check (measured section, load = stepper ceiling) ==")
# derive section from the r=32 slab
slab = Rot(Z=TH) * Pos(32.0, 0, -283.5) * Box(0.4, 12.0, 10.0)
inter = bs & slab
A_sec = inter.volume / 0.4
bb = inter.bounding_box()
h = bb.max.Z - bb.min.Z
b = A_sec / h
print(f"   measured section at PCD: {b:.3f} (tangential) x {h:.3f} (vertical) mm, A={A_sec:.3f} mm2")
# supported span: bar tip in the inner ring slot to the outer wall window
span = 46.0 - 14.0
I = h * b**3 / 12.0
for Emod in (2000.0, 4000.0):
    for F in (2.0, 6.0):
        delta = F * span**3 / (48 * Emod * I)
        sigma = (F*span/4) * (b/2) / I
        print(f"   E={Emod:5.0f} MPa F={F:.0f} N span={span:.0f} mm: delta={delta:8.2f} mm, sigma={sigma:8.1f} MPa")

print("\n== POCKET bore: radial and tangential free width vs z (exact) ==")
disc = sol["pocket_disc"]
for z in (-286.5, -287.5, -288.5, -290.0, -294.0, -299.0):
    for rprobe in (7.0, 7.5, 8.0, 8.5, 9.0):
        cyl = Pos(32, 0, z) * Cylinder(rprobe, 0.4)
        v = ivol(cyl, disc)
        if v > 0.01:
            print(f"   z={z:7.1f}: first obstruction at probe r={rprobe:.1f} (material {v:.3f} mm3)")
            break
    else:
        print(f"   z={z:7.1f}: clear to r=9.0 (D18)")

print("\n== pocket top chamfer profile (radial half-width vs z) ==")
for z in np.arange(-286.1, -289.1, -0.5):
    lo, hi = 7.0, 12.0
    for _ in range(18):
        mid = (lo+hi)/2
        v = ivol(Pos(32,0,z)*Cylinder(mid, 0.2), disc)
        if v > 0.005: hi = mid
        else: lo = mid
    print(f"   z={z:7.2f}: open bore radius {lo:6.3f} mm (D={2*lo:.2f})")

print("\n== EXIT port + CHUTE bore (exact, retaining_plate_chute) ==")
rp = sol["retaining_plate_chute"]
for z in (-300.7, -301.5, -302.5, -303.5, -304.3, -306.0, -315.0, -330.0, -344.5, -352.0):
    lo, hi = 4.0, 14.0
    for _ in range(18):
        mid = (lo+hi)/2
        v = ivol(Pos(32,0,z)*Cylinder(mid, 0.2), rp)
        if v > 0.005: hi = mid
        else: lo = mid
    print(f"   z={z:7.1f}: open bore radius {lo:6.3f} (D={2*lo:6.2f} mm)")

print("\n== disc-to-plate and disc-to-roof gaps, disc rim gap (exact) ==")
mh = sol["meter_housing"]
# vertical gap over the transfer arc (theta 0 .. 129)
for thd in (0.0, 45.0, 90.0, 120.0, 128.0):
    th = math.radians(thd)
    col = Pos(32*math.cos(th), 32*math.sin(th), -285.0) * Cylinder(1.0, 3.0)  # z -286.5..-283.5
    vh = ivol(col, mh); vd = ivol(col, disc)
    print(f"   th={thd:5.1f}: housing material in z[-286.5,-283.5] band = {vh:7.3f} mm3, disc = {vd:7.3f} mm3")
# radial gap disc rim (r46) to chamber wall
for r in (46.2, 46.6, 47.0, 47.4):
    ring = Pos(0,0,-293.0) * Cylinder(r, 6.0) - Pos(0,0,-293.0) * Cylinder(r-0.2, 6.0)
    print(f"   annulus r={r-0.2:.1f}-{r:.1f}: disc {ivol(ring, disc):8.2f}  housing {ivol(ring, mh):8.2f} mm3")

print("\n== FIELD ACCESS: straight rod from the fill port down to the fill arc ==")
# fill port centre (0,40) radius 23; can a straight 8 mm rod reach the disc top in 130-250 deg?
parts = [sol[n] for n in NAMES if n != "fill_cap"]
def rod_clear(x0,y0,z0, x1,y1,z1, d=8.0):
    L = math.dist((x0,y0,z0),(x1,y1,z1))
    cx,cy,cz = (x0+x1)/2,(y0+y1)/2,(z0+z1)/2
    dx,dy,dz = x1-x0,y1-y0,z1-z0
    # build a cylinder along the direction
    ax = math.degrees(math.atan2(math.hypot(dx,dy), dz))
    az = math.degrees(math.atan2(dy,dx))
    rod = Pos(cx,cy,cz) * Rot(Z=az) * Rot(Y=ax) * Cylinder(d/2, L)
    tot = sum(ivol(rod, p) for p in parts)
    return tot, L
for thd in (150.0, 190.0, 250.0, 130.0):
    th = math.radians(thd)
    tx, ty = 32*math.cos(th), 32*math.sin(th)
    tot, L = rod_clear(0.0, 40.0, -181.0, tx, ty, -285.0)
    print(f"   rod fill-port -> disc top at th={thd:5.1f} ({tx:6.2f},{ty:6.2f}): obstruction {tot:9.2f} mm3 over {L:.0f} mm")
# straight rod up the chute from below
tot, L = rod_clear(32.0, 0.0, -360.0, 32.0, 0.0, -299.0)
print(f"   rod up the chute to the pocket:                       obstruction {tot:9.2f} mm3 over {L:.0f} mm")
