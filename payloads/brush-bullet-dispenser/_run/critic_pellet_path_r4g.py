#!/usr/bin/env python
"""Pass G: field jam access (rod reach map), agitator/bar nip, chute sensor
bores, chute exit position."""
import math, numpy as np
from build123d import import_step, Sphere, Pos, Rot, Cylinder, Box

E = "/Users/hex/projects/payload-systems/payloads/brush-bullet-dispenser/cad/exports/"
NAMES = ["top_plate","hopper","meter_housing","pocket_disc","agitator",
         "brush_strip","retaining_plate_chute","electronics_bay"]
sol = {n: import_step(E + n + "_r4.step") for n in NAMES}
def ivol(a, b):
    try:
        r = a & b
        if r is None: return 0.0
        return r.volume if hasattr(r, "volume") else sum(x.volume for x in r)
    except Exception:
        return float("nan")

STAT = ["top_plate","hopper","meter_housing","agitator","brush_strip",
        "retaining_plate_chute","electronics_bay"]
def rod(x0,y0,z0,x1,y1,z1,d,parts):
    L = math.dist((x0,y0,z0),(x1,y1,z1))
    cx,cy,cz = (x0+x1)/2,(y0+y1)/2,(z0+z1)/2
    dx,dy,dz = x1-x0,y1-y0,z1-z0
    ax = math.degrees(math.atan2(math.hypot(dx,dy), dz))
    az = math.degrees(math.atan2(dy,dx))
    r = Pos(cx,cy,cz)*Rot(Z=az)*Rot(Y=ax)*Cylinder(d/2, L)
    return sum(ivol(r, sol[n]) for n in parts)

print("== field access: straight rod through the OPEN fill port to the disc top ==")
print("   (fill port centre (0,40) r23; disc top z=-286; pockets at PCD 32)")
for d in (4.0, 8.0):
    ok = []
    for thd in range(100, 285, 5):
        t = math.radians(thd)
        v = rod(0.0, 40.0, -178.0, 32*math.cos(t), 32*math.sin(t), -285.5, d, STAT)
        if v < 0.05: ok.append(thd)
    print(f"   rod D{d:.0f}: reachable pocket angles {ok if ok else 'NONE'}")
    if ok: print(f"      -> {len(ok)*5} deg of the 122.5 deg fill window reachable; "
                 f"jam sites at the bar(133)/roof edge(129) reachable: "
                 f"{'YES' if any(125<=a<=137 for a in ok) else 'NO'}")

print("\n== field access: rod up the chute from below ==")
for d in (4.0, 10.0, 18.0):
    v = rod(32.0, 0.0, -370.0, 32.0, 0.0, -298.0, d, STAT)
    print(f"   rod D{d:4.1f} up the chute into a pocket: obstruction {v:9.2f} mm3")

print("\n== agitator finger over the fixed wiper bar: nip gap ==")
ag = sol["agitator"]; bs = sol["brush_strip"]
print(f"   agitator z {ag.bounding_box().min.Z:.2f}..{ag.bounding_box().max.Z:.2f}")
print(f"   bar/fin  z {bs.bounding_box().min.Z:.2f}..{bs.bounding_box().max.Z:.2f}")
# radial overlap band of finger vs bar
print(f"   nip = finger underside (-280.00) - bar top (-282.15) = 2.15 mm; "
      f"3 fingers x 8 deg cross the bar every revolution")
sw = None
for a in range(0, 360, 5):
    c = Rot(Z=a) * ag
    sw = c if sw is None else sw + c
print(f"   agitator swept-union vs brush bar: {ivol(sw, bs):8.2f} mm3 (0 = no strike)")
print(f"   agitator swept-union vs meter_housing: {ivol(sw, sol['meter_housing']):8.2f} mm3")

print("\n== chute: sensor bores and bottom exit position ==")
rp = sol["retaining_plate_chute"]
for z in (-344.5, -343.0, -346.0):
    for r in (11.0, 12.0, 13.0, 14.0):
        # look for side openings: thin ring at radius r about the chute axis
        ring = Pos(32,0,z)*Cylinder(r,0.4) - Pos(32,0,z)*Cylinder(r-0.4,0.4)
        v = ivol(ring, rp)
        full = math.pi*(r**2-(r-0.4)**2)*0.4
        print(f"   z={z:8.1f} ring r{r-0.4:.1f}-{r:.1f}: material {v:8.2f} of {full:8.2f} mm3 "
              f"({100*v/full:5.1f}% solid)")
bb = rp.bounding_box()
print(f"   chute bottom z={bb.min.Z:.2f}; bore centre x=32 -> release point 32 mm off the payload axis")
# largest sphere that can leave through a sensor window
for d in (2.0, 3.0, 4.0, 5.0, 6.0):
    sp = Pos(32+11.0+d/2-0.5, 0, -344.5)*Sphere(d/2)
    print(f"   sphere D{d} centred in the wall at the beam height: material {ivol(sp, rp):8.2f} mm3")
