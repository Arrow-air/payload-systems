#!/usr/bin/env python
"""Round-3 pellet-path critic probe pass. Independent measurements against the
EXPORTED r3 STEP/STL files (not the builder's in-model claims)."""
import math
import numpy as np
import trimesh
from build123d import import_step, Sphere, Pos, Rot, Cylinder, Box

E = "/Users/hex/projects/payload-systems/payloads/capsule-dispenser/cad/exports/"
NAMES = ["top_plate", "fill_cap", "hopper", "meter_housing", "pocket_disc",
         "agitator", "brush_strip", "retaining_plate_chute", "electronics_bay"]

sol = {}
print("== reimport connectivity ==")
for n in NAMES:
    s = import_step(E + n + "_r3.step")
    sol[n] = s
    print(f"  {n:24s} solids={len(s.solids())}")

def ivol(a, b):
    """.intersect() returns None on imported solids -- use & and be loud."""
    try:
        r = a & b
        if r is None:
            return 0.0
        if hasattr(r, "volume"):
            return r.volume
        return sum(s.volume for s in r)
    except Exception:
        return float("nan")

PATH_PARTS = ["top_plate", "fill_cap", "hopper", "meter_housing", "pocket_disc",
              "agitator", "brush_strip", "retaining_plate_chute"]

def sphere_probe(label, x, y, z, d=13.0):
    sp = Pos(x, y, z) * Sphere(d / 2)
    tot = 0.0
    worst = ""
    for n in PATH_PARTS:
        v = ivol(sp, sol[n])
        if v > 0.001:
            worst += f" {n}={v:.2f}"
        tot += v
    print(f"  {label:44s} ({x:7.2f},{y:7.2f},{z:7.1f}) sum={tot:8.3f} mm3 {'CLEAR' if tot < 0.01 else 'HIT:' + worst}")
    return tot

print("\n== 13 mm worst-case pellet transit probes (0 = clear) ==")
c135 = 32 * math.cos(math.radians(135)); s135 = 32 * math.sin(math.radians(135))
c190 = 32 * math.cos(math.radians(190)); s190 = 32 * math.sin(math.radians(190))
c45 = 32 * math.cos(math.radians(45)); s45 = 32 * math.sin(math.radians(45))
probes = [
    ("fill-port drop (below cap neck)",            0, 40, -200),
    ("hopper mid",                                 0, 40, -222),
    ("hopper near wall",                           0, 55, -230),
    ("funnel cone",                                0, 44, -268),
    ("sump: resting on disc th190 r32",            c190, s190, -279.5),
    ("seated pocket th180 (on plate)",             -32, 0, -294.0),
    ("seated pocket th135 (brush plane)",          c135, s135, -294.0),
    ("seated pocket th90 (transfer arc)",          0, 32, -294.0),
    ("seated pocket th45 (transfer arc)",          c45, s45, -294.0),
    ("pocket th0 over exit hole",                  32, 0, -294.0),
    ("descending exit hole",                       32, 0, -301.0),
    ("in exit hole / chute top",                   32, 0, -308.0),
    ("chute upper",                                32, 0, -320.0),
    ("chute mid",                                  32, 0, -335.0),
    ("chute at IR beam z=-344.5",                  32, 0, -344.5),
    ("chute exit",                                 32, 0, -352.0),
]
tot_all = 0.0
for p in probes:
    tot_all += sphere_probe(*p)
print(f"  TRANSIT TOTAL: {tot_all:.3f} mm3")

print("\n== minimum channel dimensions (probe cylinders vs exports) ==")
rp = sol["retaining_plate_chute"]
disc = sol["pocket_disc"]
# exit hole (below the 1.5 chamfer): claimed Dia18
for r in (8.8, 9.2):
    pr = Pos(32, 0, -303.3) * Cylinder(r, 2.2)
    print(f"  exit-hole probe r={r}: material {ivol(pr, rp):.3f} mm3")
# chute bore: claimed Dia22
for r in (10.8, 11.2):
    pr = Pos(32, 0, -327) * Cylinder(r, 44)
    print(f"  chute-bore probe r={r}: material {ivol(pr, rp):.3f} mm3")
# pocket bore below chamfer: claimed Dia15
for r in (7.3, 7.7):
    pr = Pos(-32, 0, -295.5) * Cylinder(r, 7.0)
    print(f"  pocket probe r={r}: material {ivol(pr, disc):.3f} mm3")

print("\n== hopper funnel angle from exported STL ==")
hm = trimesh.load(E + "hopper_r3.stl")
def inner_r(z):
    sec = hm.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    v = np.asarray(sec.vertices)
    rr = np.hypot(v[:, 0], v[:, 1])
    inner = rr[rr < rr.mean()]
    return inner.max()
r1, r2 = inner_r(-270.0), inner_r(-252.0)
ang = math.degrees(math.atan2(18.0, r2 - r1))
print(f"  funnel inner r(z=-270)={r1:.2f}, r(z=-252)={r2:.2f} -> wall angle {ang:.1f} deg from horizontal")
print(f"  funnel outlet claimed r47.5: inner r extrapolated to z=-280.5: {r1 - (280.5-270.0)*(r2-r1)/18.0:.2f}")

print("\n== roof / disc / brush / agitator z-planes from exported STLs ==")
mh = trimesh.load(E + "meter_housing_r3.stl")
dm = trimesh.load(E + "pocket_disc_r3.stl")
bm = trimesh.load(E + "brush_strip_r3.stl")
am = trimesh.load(E + "agitator_r3.stl")
V = np.asarray(mh.vertices); R = np.hypot(V[:, 0], V[:, 1]); TH = np.degrees(np.arctan2(V[:, 1], V[:, 0]))
sel = (R > 21) & (R < 45) & (np.abs(TH) < 45) & (V[:, 2] < -281) & (V[:, 2] > -288)
if sel.sum():
    print(f"  roof underside over transfer arc (th +-45): min z {V[sel][:,2].min():.2f} ({sel.sum()} verts)")
else:
    print("  no housing verts in transfer-arc roof window -- widen search:")
    sel2 = (R > 21) & (R < 45) & (np.abs(TH) < 45)
    zz = np.sort(np.unique(np.round(V[sel2][:, 2], 2)))
    print("   distinct z in r21-45 th+-45:", zz[:12], "...")
Vd = np.asarray(dm.vertices); Rd = np.hypot(Vd[:, 0], Vd[:, 1])
seld = (Rd > 15) & (Rd < 44)
print(f"  disc top (r15..44): max z {Vd[seld][:,2].max():.2f}")
Vb = np.asarray(bm.vertices); Rb = np.hypot(Vb[:, 0], Vb[:, 1])
selb = Rb < 46
print(f"  brush skirt bottom (r<46): min z {Vb[selb][:,2].min():.2f}")
Va = np.asarray(am.vertices)
print(f"  agitator z range {Va[:,2].min():.2f}..{Va[:,2].max():.2f}, max r {np.hypot(Va[:,0],Va[:,1]).max():.2f}")

print("\n== roof-entry ramp spot checks (z = disc_top+2.0 band) ==")
for th, expect in ((131.0, "void"), (127.0, "material")):
    pr = Rot(Z=th) * (Pos(33.75, 0, -284.0) * Box(20, 0.4, 0.4))
    print(f"  th={th}: housing material {ivol(pr, sol['meter_housing']):.2f} mm3 (expect {expect})")

print("\n== drive coupling check: disc set screw vs motor shaft (exports) ==")
# set-screw hole: axis along -Y at (0,-6,-268) per source; probe with r1.0 cyl
pr_hole = Pos(0, -6, -268) * Rot(X=90) * Cylinder(1.0, 8)
print(f"  probe r1.0 along set-screw axis @(0,-6,-268): disc material {ivol(pr_hole, disc):.2f} mm3 (0 => hole exists)")
# is there open shaft bore at the set-screw height?
pr_bore268 = Pos(0, 0, -268) * Cylinder(2.0, 4)
pr_bore275 = Pos(0, 0, -275) * Cylinder(2.0, 4)
pr_bore283 = Pos(0, 0, -283) * Cylinder(2.0, 4)
print(f"  center-bore probe r2 @z-268: material {ivol(pr_bore268, disc):.2f} mm3 (full=50.3 => solid, no bore)")
print(f"  center-bore probe r2 @z-275: material {ivol(pr_bore275, disc):.2f} mm3 (0 => bore open)")
print(f"  center-bore probe r2 @z-283: material {ivol(pr_bore283, disc):.2f} mm3 (0 => bore open)")
# shaft top from the exported assembly STL (stepper body)
asm = trimesh.load(E + "dispenser_r3_assembly.stl")
bodies = asm.split(only_watertight=False)
print(f"  assembly STL bodies: {len(bodies)}")
for b in bodies:
    bb = b.bounds
    dx, dy = bb[1][0] - bb[0][0], bb[1][1] - bb[0][1]
    cx, cy = (bb[0][0] + bb[1][0]) / 2, (bb[0][1] + bb[1][1]) / 2
    if abs(dx - 35.2) < 1 and abs(dy - 35.2) < 1 and abs(cx) < 1 and abs(cy) < 1:
        print(f"  stepper body: z {bb[0][2]:.2f}..{bb[1][2]:.2f} -> shaft top {bb[1][2]:.2f}")

print("\n== park retention (independent recompute) ==")
d_centers = 2 * 32 * math.sin(math.radians(11.25))
print(f"  parked pocket at +-22.5deg vs exit r9: center dist {d_centers:.2f}, lens {9 + 7.5 - d_centers:.2f} mm")

print("\n== fines-slot floor coverage under rim trough ==")
cov = (245 - 135) + (345 - 265)
print(f"  slot arcs 135-245 + 265-345 = {cov} deg of 360 ({cov/3.6:.0f}%); dead floor {360-cov} deg incl. exit sector th345->135")

print("\n== rider/fragment wedge numbers (analytic, from measured planes) ==")
print("  seated 13mm pellet top = plate_top(-300.5)+13 = -287.5 (1.5 below disc top -286.0)")
print("  rigid bar z -283.25..-282.15; gap seated-pellet-top -> bar underside = 4.25 mm")
print("  rider pellet (on seated) center z -281.0; bar top 1.15 below rider center -> contact below equator")
