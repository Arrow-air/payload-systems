#!/usr/bin/env python
"""Round-4 pellet-path critic, pass A: geometry inventory measured from the
EXPORTED r4 STL/STEP only. No import of dispenser.py."""
import math, numpy as np, trimesh

E = "/Users/hex/projects/payload-systems/payloads/capsule-dispenser/cad/exports/"
NAMES = ["top_plate", "pcb_pedestal", "fill_cap", "hopper", "meter_housing",
         "pocket_disc", "agitator", "brush_strip", "retaining_plate_chute",
         "electronics_bay", "bay_lid"]
M = {n: trimesh.load(E + n + "_r4.stl") for n in NAMES}

print("== part inventory (exported STL) ==")
for n, m in M.items():
    b = m.bounds
    print(f"  {n:24s} wt={m.is_watertight!s:5s} vol={m.volume/1000:8.2f} cm3 "
          f"bbox x[{b[0][0]:7.2f},{b[1][0]:7.2f}] y[{b[0][1]:7.2f},{b[1][1]:7.2f}] z[{b[0][2]:8.2f},{b[1][2]:8.2f}]")

def sect_radii(m, z, tol=None):
    s = m.section(plane_origin=[0,0,z], plane_normal=[0,0,1])
    if s is None: return None
    v = np.asarray(s.vertices)
    return np.hypot(v[:,0], v[:,1])

print("\n== hopper funnel wall: inner radius vs z (exported hopper STL) ==")
h = M["hopper"]
rows = []
for z in np.arange(-279.0, -240.0, 2.0):
    rr = sect_radii(h, z)
    if rr is None: continue
    inner = rr[rr < (rr.min()+rr.max())/2].max()
    rows.append((z, inner))
    print(f"   z={z:8.2f}  inner_r={inner:7.3f}  outer_r={rr.max():7.3f}")
zs = np.array([r[0] for r in rows]); ri = np.array([r[1] for r in rows])
sel = (zs > -279) & (zs < -243)
A = np.polyfit(ri[sel], zs[sel], 1)
print(f"   linear fit dz/dr = {A[0]:.4f} -> wall angle from horizontal = {math.degrees(math.atan(abs(A[0]))):.3f} deg")
# local angle at the outlet (bottom 6 mm of the cone)
for zlo, zhi in ((-280.4,-274.0), (-274.0,-268.0), (-260.0,-250.0)):
    r1 = sect_radii(h, zlo); r2 = sect_radii(h, zhi)
    i1 = r1[r1 < (r1.min()+r1.max())/2].max(); i2 = r2[r2 < (r2.min()+r2.max())/2].max()
    print(f"   local {zlo}->{zhi}: r {i1:.3f}->{i2:.3f}  angle {math.degrees(math.atan((zhi-zlo)/(i2-i1))):.3f} deg")

print("\n== hopper outlet plane / bottom of hopper part ==")
print(f"   hopper z min {h.bounds[0][2]:.2f}  z max {h.bounds[1][2]:.2f}")
rr = sect_radii(h, h.bounds[0][2]+0.2)
print(f"   at z={h.bounds[0][2]+0.2:.2f}: r range {rr.min():.2f}..{rr.max():.2f}")

print("\n== key z-planes measured from exports ==")
d = M["pocket_disc"]; mh = M["meter_housing"]; rp = M["retaining_plate_chute"]
Vd = np.asarray(d.vertices); Rd = np.hypot(Vd[:,0],Vd[:,1])
print(f"   pocket_disc  z {d.bounds[0][2]:.2f}..{d.bounds[1][2]:.2f}; disc plate top(r15-44) {Vd[(Rd>15)&(Rd<44)][:,2].max():.2f}, bot {Vd[(Rd>15)&(Rd<44)][:,2].min():.2f}")
Vr = np.asarray(rp.vertices); Rr = np.hypot(Vr[:,0],Vr[:,1])
print(f"   retain plate z {rp.bounds[0][2]:.2f}..{rp.bounds[1][2]:.2f}; plate top (r<50) {Vr[Rr<50][:,2].max():.2f}")
print(f"   meter_housing z {mh.bounds[0][2]:.2f}..{mh.bounds[1][2]:.2f}")
b = M["brush_strip"]; Vb=np.asarray(b.vertices); Rb=np.hypot(Vb[:,0],Vb[:,1])
th_b = np.degrees(np.arctan2(Vb[:,1],Vb[:,0]))%360
print(f"   brush_strip  z {b.bounds[0][2]:.2f}..{b.bounds[1][2]:.2f}; r {Rb.min():.2f}..{Rb.max():.2f}; theta {th_b.min():.1f}..{th_b.max():.1f}")
a = M["agitator"]; Va=np.asarray(a.vertices); Ra=np.hypot(Va[:,0],Va[:,1])
print(f"   agitator     z {a.bounds[0][2]:.2f}..{a.bounds[1][2]:.2f}; r max {Ra.max():.2f}")
for zlo,zhi in ((-286,-282),(-282,-278),(-278,-274),(-274,-270),(-270,-260),(-260,-240)):
    s = (Va[:,2]>=zlo)&(Va[:,2]<zhi)
    if s.sum(): print(f"     agitator band z[{zlo},{zhi}): rmax={Ra[s].max():.2f} n={s.sum()}")

print("\n== fill window: what is open above the disc, by angle (meter_housing) ==")
# ray-free approach: at a given z and radius, is there housing material at angle th?
from trimesh.proximity import ProximityQuery
def occupied(mesh, pts):
    return mesh.contains(pts)
for z in (-285.0, -283.0, -281.0):
    open_deg = []
    for thd in range(0,360,1):
        th = math.radians(thd)
        pts = np.array([[r*math.cos(th), r*math.sin(th), z] for r in (20,26,32,38,44,46.5)])
        inside = mh.contains(pts)
        open_deg.append((thd, (~inside).sum(), inside.sum()))
    fully = [t for t,o,i in open_deg if i==0]
    def arcs(lst):
        out=[];
        if not lst: return out
        st=lst[0]; pv=lst[0]
        for t in lst[1:]:
            if t==pv+1: pv=t
            else: out.append((st,pv)); st=t; pv=t
        out.append((st,pv)); return out
    print(f"   z={z}: angles with NO housing material at r=20..46.5: {arcs(fully)}  total {len(fully)} deg")

print("\n== roof / shelf: horizontal upward-facing area over the sump ==")
for name in ("meter_housing","hopper","retaining_plate_chute","pocket_disc"):
    m = M[name]
    nz = m.face_normals[:,2]
    ar = m.area_faces
    ctr = m.triangles_center
    R = np.hypot(ctr[:,0],ctr[:,1])
    # upward-facing (>70 deg from horizontal normal => within 20 deg of flat) in the pellet region
    up = (nz > math.cos(math.radians(20)))
    reg = up & (R < 70) & (ctr[:,2] > -305) & (ctr[:,2] < -240)
    print(f"   {name:24s} upward near-flat area in sump/meter region: {ar[reg].sum():9.1f} mm2")
    if reg.sum():
        zs2 = np.round(ctr[reg][:,2],1)
        uz = {}
        for zz,aa in zip(zs2, ar[reg]): uz[zz]=uz.get(zz,0)+aa
        top = sorted(uz.items(), key=lambda kv:-kv[1])[:6]
        for zz,aa in top:
            sel2 = reg & (np.round(ctr[:,2],1)==zz)
            print(f"        z={zz:8.2f}  area={aa:8.1f} mm2  r range {R[sel2].min():.1f}..{R[sel2].max():.1f}")
