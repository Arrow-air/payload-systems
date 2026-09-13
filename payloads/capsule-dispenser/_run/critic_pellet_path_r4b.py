#!/usr/bin/env python
"""Round-4 pellet-path critic, pass B: channel dimensions, fill-window
obstructions, brush geometry, pocket/exit/chute bores. Exports only."""
import math, numpy as np, trimesh
from trimesh.proximity import ProximityQuery

E = "/Users/hex/projects/payload-systems/payloads/capsule-dispenser/cad/exports/"
NAMES = ["top_plate", "fill_cap", "hopper", "meter_housing", "pocket_disc",
         "agitator", "brush_strip", "retaining_plate_chute"]
M = {n: trimesh.load(E + n + "_r4.stl") for n in NAMES}

# ---------------------------------------------------------------- fill window
print("== meter_housing material inside the nominal fill sector (130-250 deg) ==")
mh = M["meter_housing"]
zs = [-285.5, -284.0, -282.5, -281.0]
for z in zs:
    hits = []
    for thd in np.arange(126.0, 254.0, 0.5):
        th = math.radians(thd)
        rs = np.arange(14.0, 47.0, 1.0)
        pts = np.stack([rs*math.cos(th), rs*math.sin(th), np.full_like(rs, z)], axis=1)
        ins = mh.contains(pts)
        if ins.any():
            hits.append((thd, rs[ins].min(), rs[ins].max(), ins.sum()))
    if hits:
        print(f"  z={z}: {len(hits)} of 256 half-degree rays hit housing material")
        # group
        grp=[]; cur=[hits[0]]
        for hh in hits[1:]:
            if hh[0]-cur[-1][0] <= 0.75: cur.append(hh)
            else: grp.append(cur); cur=[hh]
        grp.append(cur)
        for g in grp:
            print(f"     theta {g[0][0]:6.1f}..{g[-1][0]:6.1f} ({g[-1][0]-g[0][0]+0.5:4.1f} deg wide)  r {min(x[1] for x in g):5.1f}..{max(x[2] for x in g):5.1f}")
    else:
        print(f"  z={z}: clear across 130-250 at r14..46")

print("\n== what are the obstructions? radial/vertical extent probe at theta=150,170,210 ==")
for thd in (150.0, 170.0, 210.0):
    th = math.radians(thd)
    for z in np.arange(-286.0, -280.0, 0.5):
        rs = np.arange(14.0, 47.5, 0.5)
        pts = np.stack([rs*math.cos(th), rs*math.sin(th), np.full_like(rs, z)], axis=1)
        ins = mh.contains(pts)
        if ins.any():
            print(f"   th={thd} z={z:7.2f}: material at r {rs[ins].min():.1f}..{rs[ins].max():.1f} ({ins.sum()} samples)")

# ---------------------------------------------------------------- brush
print("\n== brush_strip profile: bottom z vs radius (must clear disc top -286.0) ==")
b = M["brush_strip"]
Vb = np.asarray(b.vertices); Rb = np.hypot(Vb[:,0], Vb[:,1])
for r0 in range(12, 60, 3):
    s = (Rb >= r0) & (Rb < r0+3)
    if s.sum():
        print(f"   r {r0:2d}-{r0+3:2d}: z {Vb[s][:,2].min():8.2f} .. {Vb[s][:,2].max():8.2f}  ({s.sum()} verts)")
# does brush overlap the disc solid?
print("   brush volume below z=-286.0 (would foul the disc if at r12..46):")
sl = b.slice_plane([0,0,-286.0], [0,0,-1])
if sl is not None:
    Vs = np.asarray(sl.vertices); Rs = np.hypot(Vs[:,0], Vs[:,1])
    print(f"     brush geometry below -286: r {Rs.min():.2f}..{Rs.max():.2f}, z min {Vs[:,2].min():.2f}")
else:
    print("     none")

# ---------------------------------------------------------------- agitator
print("\n== agitator finger coverage (angular + radial), z-band -280..-274 ==")
a = M["agitator"]
for z in (-279.5, -277.0, -274.5):
    cov = 0; radial = []
    for thd in range(0, 360, 2):
        th = math.radians(thd)
        rs = np.arange(6.0, 46.0, 1.0)
        pts = np.stack([rs*math.cos(th), rs*math.sin(th), np.full_like(rs, z)], axis=1)
        ins = a.contains(pts)
        if ins.any():
            cov += 2
            radial.append((rs[ins].min(), rs[ins].max()))
    if radial:
        print(f"   z={z}: {cov} deg of 360 has finger material; r {min(x[0] for x in radial):.1f}..{max(x[1] for x in radial):.1f}")
    else:
        print(f"   z={z}: no material")

# ---------------------------------------------------------------- pocket bore
print("\n== pocket bore geometry (pocket_disc, PCD 32, theta 0) ==")
d = M["pocket_disc"]
for z in (-286.2, -287.0, -288.0, -289.0, -292.0, -296.0, -299.5):
    # scan a line across the pocket at theta=0 along the radial direction
    xs = np.arange(20.0, 44.0, 0.1)
    pts = np.stack([xs, np.zeros_like(xs), np.full_like(xs, z)], axis=1)
    ins = d.contains(pts)
    free = xs[~ins]
    free = free[(free > 22) & (free < 42)]
    if len(free):
        # contiguous free span containing r=32
        w = free.max()-free.min()
        print(f"   z={z:8.2f}: radial free span {free.min():.2f}..{free.max():.2f} = {w:.2f} mm")
    else:
        print(f"   z={z:8.2f}: no free span (solid)")
print("   tangential width at PCD:")
for z in (-286.2, -288.0, -292.0, -299.5):
    ys = np.arange(-10.0, 10.0, 0.1)
    pts = np.stack([np.full_like(ys, 32.0), ys, np.full_like(ys, z)], axis=1)
    ins = d.contains(pts)
    free = ys[~ins]
    if len(free): print(f"   z={z:8.2f}: tangential free {free.min():.2f}..{free.max():.2f} = {free.max()-free.min():.2f} mm")

# ---------------------------------------------------------------- exit + chute
print("\n== exit port + chute bore (retaining_plate_chute) ==")
rp = M["retaining_plate_chute"]
for z in (-300.6, -301.5, -302.5, -303.5, -304.4, -306.0, -312.0, -325.0, -340.0, -344.5, -350.0, -354.0):
    xs = np.arange(18.0, 48.0, 0.1)
    pts = np.stack([xs, np.zeros_like(xs), np.full_like(xs, z)], axis=1)
    ins = rp.contains(pts)
    free = xs[~ins]
    if len(free):
        # keep the span around x=32
        f2 = free[(free>20)&(free<46)]
        if len(f2):
            print(f"   z={z:8.2f}: free x {f2.min():6.2f}..{f2.max():6.2f} = {f2.max()-f2.min():5.2f} mm")
            continue
    print(f"   z={z:8.2f}: solid across x20..46")

print("\n== max inscribed sphere along the drop path (all parts, unsigned distance) ==")
allmesh = trimesh.util.concatenate([M[n] for n in NAMES])
pq = ProximityQuery(allmesh)
def clearance(pts):
    _, dist, _ = pq.on_surface(pts)
    inside = allmesh.contains(pts)
    d = dist.copy(); d[inside] = -d[inside]
    return d
stations = []
for z in np.arange(-186.0, -280.0, -6.0):   # hopper column above the fill port
    stations.append(("hopper col", 0.0, 40.0, z))
for z in np.arange(-281.0, -286.5, -1.0):
    stations.append(("fill window th190", 32*math.cos(math.radians(190)), 32*math.sin(math.radians(190)), z))
for z in np.arange(-287.0, -300.0, -1.5):
    stations.append(("in pocket th180", -32.0, 0.0, z))
for z in np.arange(-300.5, -355.0, -3.0):
    stations.append(("exit/chute th0", 32.0, 0.0, z))
best = {}
for lab, x, y, z in stations:
    # local optimisation: sample a small xy grid around the nominal centre
    g = np.arange(-3.0, 3.01, 0.75)
    P = np.array([[x+dx, y+dy, z] for dx in g for dy in g])
    c = clearance(P)
    i = int(np.argmax(c))
    key = (lab, round(z,1))
    best[key] = (c[i], P[i])
for (lab, z), (c, p) in best.items():
    flag = "  << under 13 mm" if 2*c < 13.0 else ""
    print(f"   {lab:20s} z={z:8.1f}  max inscribed sphere D = {2*c:7.2f} mm at ({p[0]:6.2f},{p[1]:6.2f}){flag}")
