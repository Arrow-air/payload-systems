"""Independent probe pass on the EXPORTED r6 files (critic method).

Run:  ~/.openclaw/workspace/venvs/dock-cad-314/bin/python verify_exports.py

This re-measures every r6 fix from the exported STEP/STL only -- it never
imports dispenser.py, so a builder-side modelling error cannot hide here.
All coordinates below are typed in from the r6 stack, not read from the
model, so a silent parameter change shows up as a failed probe.

r5 interference critic MODERATE: "the 'independent' checker does not check
the interface at all ... so the entire mount-interface error class is
invisible to the harness the notes present as the anti-self-deception
mechanism." r6 therefore ALSO imports the vendor clip-plate STEP and (when
available) builds the landing gear from the quiver source, and re-derives the
mount pattern, the blind-mate position and the ground clearance here.

r6 stack (mm, drone frame): mount -171.0 | clip bottom -181.5 | top plate
-186.5 | hopper cyl bottom -218.5 | funnel/sump floor -274.2 | roof under
-283.2 | disc top -284.7 | disc bottom -298.7 | plate top -299.2 | plate
bottom -303.2 | IR beam -343.2 | chute exit -353.2 | motor bottom -366.4.
"""
import copy
import math
import os

import numpy as np
import trimesh
from build123d import Box, Cylinder, Pos, Rot, Sphere, import_step

HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(HERE, "exports")
IFACE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "interface",
                                      "mechanical"))
REV = "r6"
PRINTED = ["top_plate", "fill_cap", "hopper", "meter_housing", "pocket_disc",
           "agitator", "brush_holder", "retaining_plate_chute",
           "electronics_bay", "bay_lid"]

Z_MOUNT, Z_PLATE_BOT, Z_TOP_BOT = -171.0, -181.5, -186.5
Z_FUN_BOT, Z_ROOF_BOT = -274.2, -283.2
Z_DISC_TOP, Z_DISC_BOT = -284.7, -298.7
Z_RPLATE_TOP, Z_RPLATE_BOT = -299.2, -303.2
BRUSH_A, PCD, ENTRY_A = 143.0, 32.0, 130.0
POCKET_R, PORT_R, PORT_RIM_R = 7.5, 9.0, 9.75


def vol(x):
    if x is None:
        return 0.0
    if hasattr(x, "volume"):
        return x.volume
    return sum(vol(i) for i in x)


def ivol(a, b):
    try:
        return vol(a.intersect(b))
    except Exception:
        return float("nan")


print("=== EXPORTED STEP CONNECTIVITY + STL INTEGRITY ===")
S = {}
for n in PRINTED:
    s = import_step(os.path.join(EX, f"{n}_{REV}.step"))
    S[n] = s
    m = trimesh.load(os.path.join(EX, f"{n}_{REV}.stl"))
    print(f"  {n:24s} STEP solids={len(s.solids())}  vol={s.volume/1000:7.2f} cm3  "
          f"STL watertight={m.is_watertight}  bodies={len(m.split(only_watertight=False))}")

asm = trimesh.load(os.path.join(EX, f"dispenser_{REV}_assembly.stl"))
bodies = asm.split(only_watertight=False)
print(f"  assembly STL bodies={len(bodies)}  watertight="
      f"{sum(b.is_watertight for b in bodies)}/{len(bodies)}")
b = asm.bounds
print(f"  assembly bbox X[{b[0][0]:.1f},{b[1][0]:.1f}] Y[{b[0][1]:.1f},{b[1][1]:.1f}] "
      f"Z[{b[0][2]:.1f},{b[1][2]:.1f}]  -> stack {Z_MOUNT - b[0][2]:.1f} mm, "
      f"ground clearance {b[0][2] + 547.89:.2f} mm (ground plane from the "
      f"landing-gear tube axis -527.89 - 40/2 foam)")

# =====================================================================
print("\n=== r5 INTERFERENCE BLOCKER 1+2: THE MOUNT, RE-DERIVED HERE ===")
clip = import_step(os.path.join(IFACE, "2112_attach_plate_payload_side.step"))
clip = Rot(X=90) * clip
cb = clip.bounding_box()
clip = Pos(-(cb.min.X + cb.max.X) / 2, -(cb.min.Y + cb.max.Y) / 2,
           Z_MOUNT - cb.max.Z) * clip
cb = clip.bounding_box()
print(f"  clip plate placed: {cb.max.X - cb.min.X:.1f} x {cb.max.Y - cb.min.Y:.1f} "
      f"x {cb.max.Z - cb.min.Z:.1f} mm, {clip.volume/1000:.2f} cm3, top face "
      f"Z={cb.max.Z:.1f}")
# through-column scan (independent of the model's own scan)
zs = np.arange(Z_PLATE_BOT + 0.2, Z_MOUNT - 0.1, 0.5)
opens = []
for x in np.arange(-24.0, 24.1, 1.0):
    for y in np.arange(-24.0, 24.1, 1.0):
        col = Pos(x, y, (Z_PLATE_BOT + Z_MOUNT) / 2) * Cylinder(0.2, 10.4)
        if ivol(col, clip) < 1e-3:
            opens.append((x, y))
A = np.array(opens)
print(f"  through-open columns on a 1 mm grid: {len(opens)}; corners at "
      f"|x|,|y| >= 18: {sorted(set((abs(x), abs(y)) for x, y in opens if abs(x) >= 18 and abs(y) >= 18))}")
for (x, y) in ((19.0, 19.0), (-19.0, 19.0), (19.0, -19.0), (-19.0, -19.0)):
    hole = Pos(x, y, Z_PLATE_BOT + 2.0) * Cylinder(1.45, 3.5)
    head = Pos(x, y, Z_PLATE_BOT + 5.1) * Cylinder(1.9, 2.0)
    drv = Pos(x, y, (Z_PLATE_BOT + 4.1 + Z_MOUNT) / 2) * Cylinder(
        1.9, Z_MOUNT - (Z_PLATE_BOT + 4.1))
    print(f"  ({x:+5.1f},{y:+5.1f}) Dia2.9 hole residual {ivol(hole, clip):5.2f} mm3, "
          f"M2 head pocket (Dia3.8x2) {ivol(head, clip):5.2f}, driver column to "
          f"the mating plane {ivol(drv, clip):5.2f} (all ~0)")
    boss = Pos(x, y, Z_TOP_BOT - 2.0) * Cylinder(3.2, 4.0)
    print(f"          top-plate material at the same xy: "
          f"{ivol(boss, S['top_plate']):6.1f} mm3 (>0 = the screw lands in "
          f"OUR plate; r5's (+/-6.5,+/-10.5) landed in the vendor window)")
# r5's pattern, re-tested with an M3-sized probe
for (x, y) in ((6.5, 10.5), (-6.5, 10.5)):
    p32 = Pos(x, y, (Z_PLATE_BOT + Z_MOUNT) / 2) * Cylinder(1.6, 10.4)
    print(f"  r5 pattern ({x:+5.1f},{y:+5.1f}) with an M3 probe: residual "
          f"{ivol(p32, clip):.2f} mm3 -> it is INSIDE the blind-mate shaft "
          f"(a hole would read 0 for any probe up to the hole size; the shaft "
          f"reads 0 for probes far larger, which is how r5's test passed)")
# blind-mate shaft walls, measured by bisection
for axis in ("x", "y"):
    lo, hi = 5.0, 15.0
    for _ in range(40):
        mid = (lo + hi) / 2
        p = (Pos(mid, 0, Z_PLATE_BOT + 2.0) if axis == "x"
             else Pos(0, mid, Z_PLATE_BOT + 2.0)) * Sphere(0.1)
        if ivol(p, clip) < 1e-6:
            lo = mid
        else:
            hi = mid
    print(f"  blind-mate shaft wall on {axis}: {lo:.2f} mm from centre "
          f"(-> {'16.0 mm' if axis == 'x' else '24.0 mm'} nominal opening)")
pcb_box = Pos(0, 0, Z_PLATE_BOT - 0.8) * Box(16.0, 24.0, 1.6)
v_pcb = sum(ivol(pcb_box, S[n]) for n in PRINTED)
print(f"  payload PCB volume (16 x 24 x 1.6, pads at Z={Z_PLATE_BOT}) vs every "
      f"printed part: {v_pcb:.2f} mm3 (~0 = the well clears it)")
shaft_col = Pos(0, 0, (Z_PLATE_BOT + Z_MOUNT) / 2) * Box(16.0, 24.0, 10.5)
print(f"  payload material inside the shaft column: "
      f"{sum(ivol(shaft_col, S[n]) for n in PRINTED):.2f} mm3 (must be 0)")

# =====================================================================
print("\n=== r5 PELLET-PATH BLOCKER 1: TRANSFER-ARC CEILING (underside) ===")
hou = S["meter_housing"]


def ceiling(th, r):
    for h in np.arange(1.4, 11.0, 0.25):
        p = Rot(Z=th) * (Pos(r, 0, Z_DISC_TOP + h) * Box(0.6, 0.6, 0.4))
        if ivol(p, hou) > 1e-4:
            return h
    return None


print("      theta:" + "".join(f"{t:8.1f}" for t in
                               (131, 130, 128, 125, 120, 110, 96, 45)))
for r in (24.5, 32.0, 39.5, 45.5):
    row = [ceiling(t, r) for t in (131, 130, 128, 125, 120, 110, 96, 45)]
    print(f"  r={r:5.1f}   " + "".join(
        (f"{v:8.2f}" if v is not None else "    open") for v in row))
print("  (r5 measured None at 130.00 deg and 1.508 mm at 129.90 -- a square "
      "step within 0.056 mm of arc, because the 45 deg cut was on the roof TOP)")
# face-normal audit at the entry, the critic's own method
hm = trimesh.load(os.path.join(EX, f"meter_housing_{REV}.stl"))
d = np.array([math.sin(math.radians(ENTRY_A)), -math.cos(math.radians(ENTRY_A)), 0.0])
n, ar, c = hm.face_normals, hm.area_faces, hm.triangles_center
rr = np.hypot(c[:, 0], c[:, 1])
th = np.degrees(np.arctan2(c[:, 1], c[:, 0])) % 360
sel = ((n @ d) < -0.3) & (c[:, 2] > Z_DISC_TOP + 1.0) & (c[:, 2] < Z_DISC_TOP + 10.5) \
    & (rr > 20) & (rr < 47) & (th > ENTRY_A - 40) & (th < ENTRY_A + 1)
if sel.sum():
    nz = n[sel][:, 2]
    print(f"  upstream-facing entry faces: {ar[sel].sum():.1f} mm2, "
          f"area-weighted n_z {float((nz*ar[sel]).sum()/ar[sel].sum()):+.2f}, "
          f"square-stub area (|n_z|<0.05) "
          f"{100*ar[sel][np.abs(nz) < 0.05].sum()/ar[sel].sum():.1f}% "
          f"(r5: one face, n_z = +0.00, i.e. 100%)")

# =====================================================================
print("\n=== r5 PELLET-PATH BLOCKER 3: WIPER CONTACT ORDER ===")
hold = S["brush_holder"]
hb = hold.bounding_box()
print(f"  brush_holder bbox z {hb.min.Z:.2f}..{hb.max.Z:.2f} (rail underside "
      f"should be disc+7.5 = {Z_DISC_TOP + 7.5:.1f}, nose tip disc+3.0 = "
      f"{Z_DISC_TOP + 3.0:.1f})")
bris = Rot(Z=BRUSH_A) * (Pos(33.5, 3.5, (Z_DISC_TOP + 1.2 + Z_DISC_TOP + 8.64) / 2)
                         * Box(26.4, 1.6, 7.44))
for proud in (2.0, 3.0, 5.0, 7.0, 11.5):
    frag = Pos(PCD, 0, Z_DISC_TOP + proud / 2) * Cylinder(2.0, proud)
    first = {}
    for t in np.arange(BRUSH_A + 14.0, ENTRY_A - 6.0, -0.25):
        f = Rot(Z=t) * copy.copy(frag)
        if "bristles" not in first and ivol(f, bris) > 0.02:
            first["bristles"] = t
        if "holder" not in first and ivol(f, hold) > 0.02:
            first["holder"] = t
        if "housing" not in first and ivol(f, hou) > 0.02:
            first["housing"] = t
        if len(first) == 3:
            break
    order = sorted(first.items(), key=lambda kv: -kv[1])
    print(f"  fragment {proud:5.1f} mm proud: " +
          " -> ".join(f"{k}@{v:.2f}" for k, v in order))
hmesh = trimesh.load(os.path.join(EX, f"brush_holder_{REV}.stl"))
dw = np.array([math.sin(math.radians(BRUSH_A)), -math.cos(math.radians(BRUSH_A)), 0.0])
n, ar, c = hmesh.face_normals, hmesh.area_faces, hmesh.triangles_center
rr = np.hypot(c[:, 0], c[:, 1])
sel = ((n @ dw) < -0.3) & (rr > 20) & (rr < 47)
nz = n[sel][:, 2]
print(f"  upstream-facing holder faces in the pellet band: {ar[sel].sum():.1f} mm2, "
      f"area-weighted n_z {float((nz*ar[sel]).sum()/ar[sel].sum()):+.2f} "
      f"(>0 = LIFTS the fragment back into the sump), square-stub area "
      f"{100*ar[sel][np.abs(nz) < 0.05].sum()/ar[sel].sum():.1f}% "
      f"(r5: a 77.6 mm2 face with n_z = -0.00 leading everything)")

# =====================================================================
print("\n=== POCKET / PARK / PORT GEOMETRY ===")
rp = S["retaining_plate_chute"]
for z, lbl in ((Z_RPLATE_TOP - 0.05, "plate top"), (Z_RPLATE_TOP - 1.0, "-1.0 mm"),
               (Z_RPLATE_TOP - 2.5, "-2.5 mm")):
    lo, hi = 5.0, 14.0
    for _ in range(40):
        mid = (lo + hi) / 2
        p = Pos(PCD + mid, 0, z) * Sphere(0.08)
        if ivol(p, rp) < 1e-6:
            lo = mid
        else:
            hi = mid
    print(f"  exit port radius at {lbl:10s}: {lo:.2f} mm")
d_c = 2 * PCD * math.sin(math.radians(22.5 / 2))
print(f"  park lens = rim {PORT_RIM_R:.2f} + pocket {POCKET_R:.2f} - centre "
      f"distance {d_c:.2f} = {PORT_RIM_R + POCKET_R - d_c:.2f} mm "
      f"(r5 printed 4.01 from an r9 that is not in the part; the critic "
      f"measured 5.51 on the r5 export)")
disc = S["pocket_disc"]
for r in (POCKET_R - 0.2, POCKET_R + 0.2):
    p = Pos(PCD + r, 0, Z_DISC_TOP - 7.0) * Sphere(0.1)
    print(f"  pocket bore at r={r:.1f} from the pocket axis: "
          f"{'OPEN' if ivol(p, disc) < 1e-6 else 'SOLID'}")

# =====================================================================
print("\n=== CARTRIDGE DROP-OUT + JAM ACCESS (re-run on r6 exports) ===")
motor = Pos(0, 0, Z_RPLATE_BOT - 14.6) * Cylinder(18.0, 29.2)
motor += Pos(0, 0, Z_RPLATE_BOT - 29.2 - 17.0) * Box(35.2, 35.2, 34.0)
CART = {"retaining_plate_chute": S["retaining_plate_chute"],
        "pocket_disc": S["pocket_disc"], "geared_stepper_envelope": motor}
STATIC = {n: S[n] for n in PRINTED if n not in CART}
tot, worst = 0.0, ("", 0.0, 0.0)
for dz in np.linspace(0.0, -60.0, 21):
    for cn, cs in CART.items():
        moved = Pos(0, 0, dz) * Rot(Z=22.0) * copy.copy(cs)
        for sn, ss in STATIC.items():
            s2 = Rot(Z=22.0) * copy.copy(ss) if sn == "agitator" else ss
            v = ivol(moved, s2)
            if v > 0.02:
                tot += v
                if v > worst[2]:
                    worst = (f"{cn} x {sn}", dz, v)
print(f"  swept obstruction over the 21-step descent: {tot:.2f} mm3  worst {worst}")
for t, lbl in ((BRUSH_A, "wiper plane"), (ENTRY_A, "roof entry edge")):
    for dia in (8.0, 12.0):
        rod = Rot(Z=t) * (Pos(PCD, 0, (Z_DISC_TOP + 1.0 - 398.0) / 2)
                          * Cylinder(dia / 2, (Z_DISC_TOP + 1.0) + 398.0))
        v = sum(ivol(rod, S[n]) for n in PRINTED
                if n not in ("pocket_disc", "retaining_plate_chute"))
        print(f"  Dia{dia:.0f} rod from below to the {lbl:16s}: {v:.2f} mm3 (~0)")

# =====================================================================
print("\n=== Dia13 TRANSIT ON EXPORTS ===")


def sph(x, y, z):
    return Pos(x, y, z) * Sphere(6.5)


def polar(r, a, z):
    return sph(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), z)


Z_SEAT = Z_RPLATE_TOP + 6.5
tests = [
    ("hopper cyl mid", sph(0, 30, Z_TOP_BOT - 16.0), None),
    # tangent radius for a Dia13 sphere on a 68 deg wall at +12 mm:
    # 47.5 + 12/tan68 - 6.5/sin68 = 45.3 (typed, not read from the model)
    ("funnel wall tangent", polar(45.3, 200, Z_FUN_BOT + 12.0), None),
    ("sump floor @60", polar(30, 60, Z_FUN_BOT + 6.5), None),
    ("on disc, fill arc", polar(32, 190, Z_DISC_TOP + 6.5), None),
    ("seated pocket th=180", polar(32, 180, Z_SEAT), 0.0),
    ("seated under wiper th=143", polar(32, 143, Z_SEAT), 8.0),
    ("seated roof edge th=130", polar(32, 130, Z_SEAT), -5.0),
    ("seated th=90", polar(32, 90, Z_SEAT), 0.0),
    ("exit hole", sph(32, 0, Z_RPLATE_TOP - 2.0), 0.0),
    ("IR beam", sph(32, 0, -343.2), None),
    ("chute exit", sph(32, 0, -349.2), None),
]
for lbl, pr, rot in tests:
    tot = 0.0
    for n in PRINTED:
        s = S[n]
        if rot is not None and n in ("pocket_disc", "agitator"):
            s = Rot(Z=rot) * copy.copy(s)
        tot += ivol(pr, s)
    tot += ivol(pr, motor)
    print(f"  {lbl:26s} {tot:7.3f} mm3  {'OK' if tot < 0.05 else '**BLOCKED**'}")

# =====================================================================
print("\n=== SUMP APERTURE + FUNNEL + MASS CROSS-CHECK ===")
open_r = []
for r in np.arange(8.0, 52.0, 0.25):
    p = Pos(r * math.cos(math.radians(190)), r * math.sin(math.radians(190)),
            Z_FUN_BOT - 1.0) * Sphere(0.2)
    if ivol(p, hou) < 1e-4:
        open_r.append(r)
runs, start = [], open_r[0]
for a, c2 in zip(open_r, open_r[1:]):
    if c2 - a > 0.3:
        runs.append((start, a))
        start = c2
runs.append((start, open_r[-1]))
lo, hi = [rr2 for rr2 in runs if rr2[0] <= PCD <= rr2[1]][0]
print(f"  sump pellet window r{lo:.2f}..{hi:.2f} = {hi-lo:.2f} mm x 120 deg "
      f"-> equivalent orifice D{2*math.sqrt((hi**2-lo**2)*120/360):.1f}, "
      f"{(hi-lo)/13.0:.2f}x the worst-case pellet")
hopm = trimesh.load(os.path.join(EX, f"hopper_{REV}.stl"))
pts = []
for z in (-272.0, -262.0, -252.0, -242.0, -232.0):
    for rr2 in np.arange(45.0, 72.0, 0.1):
        if hopm.contains(np.array([[rr2 * math.cos(math.radians(190)),
                                    rr2 * math.sin(math.radians(190)), z]]))[0]:
            pts.append((z, rr2))
            break
(z0, r0), (z1, r1) = pts[0], pts[-1]
print(f"  funnel wall angle {math.degrees(math.atan2(z1 - z0, r1 - r0)):.1f} deg "
      f"from horizontal (claim 68.0)")
DENS = {"petg_cf": 1.25e-3, "tpu": 1.20e-3, "petg": 1.27e-3}
tot_m = 0.0
for n in PRINTED:
    dd = DENS["tpu"] if n == "agitator" else (
        DENS["petg"] if n == "fill_cap" else DENS["petg_cf"])
    tot_m += S[n].volume * dd
print(f"  printed parts ({len(PRINTED)}) total {tot_m:.1f} g at the ledger "
      f"densities, 100% infill")
cyl = math.pi * 70.0 ** 2 * (Z_TOP_BOT - 10.0 - Z_HOP_BOT if False else 22.0)
cone = math.pi * 55.7 / 3 * (47.5 ** 2 + 47.5 * 70 + 70 ** 2)
print(f"  analytic usable volume to the -196.5 fill line: "
      f"{(cyl + cone)/1000:.0f} cm3 (+ sump) -> "
      f"{(cyl + cone)/1000/2.28:.0f} pellets at worst-case barrel packing")
