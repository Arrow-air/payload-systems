# Brush Bullet Dispenser — Ground Truth Pack (source of truth for ALL agents)

RULES: Never invent facts. Everything below is verified unless marked
ASSUMPTION. If you need a fact that is not here, derive it from the referenced
files and RECORD the derivation, or label it ASSUMPTION with your reasoning.
Thomas's directives are quoted verbatim and dated — they are hard requirements.

## Mission (Thomas, 2026-08-06)

> "we'll want the drone to fly to target plants and drop a specified number of
> pellets (between one and three, usually)"

Herbicide pellet dispenser for targeted brush control (mesquite/juniper class
targets, West Texas ranch conditions: dust, heat, wind). The aircraft flies to
a plant (targets arrive as coordinates from an orthophoto/scouting pipeline)
and drops N pellets, N commanded per-target, usually 1–3.

## Pellet (verified by Thomas 2026-08-06 unless noted)

- Diameter: ~12 mm (molded, slightly irregular — see photo description below)
- Mass: **1.18 g** per pellet
- Appearance: white/off-white molded sphere with a visible mold parting line /
  slight barrel shape (from Thomas's photo). ASSUMPTION: diameter tolerance
  ±1 mm; design metering to a parametric `PELLET_D` with default 12 mm and
  clearance sized for 13 mm worst case.
- Friability (Thomas, 2026-08-06): > "they do sometimes break/crumble but we
  try to filter those out before loading the dispenser" → VERIFIED: pellets
  can break/crumble; loading is pre-filtered so assume mostly-intact pellets
  at load time, BUT pellets can still break inside the hopper/meter from
  vibration and handling — the mechanism must tolerate fragments and dust
  accumulation over a full sortie without jamming or miscounting.
- ASSUMPTION (research task): hardness numbers, moisture swelling — research
  from commercial product data (tebuthiuron pellets, "Brush Bullets",
  Spike 20P class).

## Requirements (Thomas, 2026-08-06, verbatim)

- Capacity: > "250 pellets would be an ideal minimum." and (2026-08-06,
  later): > "More brush bullets isnt a bad thing, it can be more than 250
  pellets." → hopper ≥ 250 pellets HARD MINIMUM (≥ 295 g; ~12 mm spheres at
  ~60% packing ≈ 0.5 L); MORE capacity is a positive design goal — trade
  hopper size upward as long as the mass ceiling and envelope/clearance
  requirements hold. Report capacity achieved, not just compliance.
- Accuracy: > "We should be able to hit a target within 1m. Expect to be
  flying at around 8m agl" → pellet lands within 1 m of target coordinate,
  released from ~8 m AGL hover. Sim must state the honest wind limit for this.
- Count: dispense exactly N pellets per command, N ∈ 1..10 (usually 1–3).
  Commanded count must be VERIFIED (sensed), not assumed.
- SCOPE CUTS (Thomas 2026-08-06): NO software phase ("That can be a whole
  project on its own") — design the electrical/command interface contract only
  (what signal triggers a dispense of N, what feedback comes back). NO
  regulatory workstream ("we're already handling that").

## Aircraft interface (verified — ICD v1.0-draft, ../../interface/ICD.md)

- Mount: **bottom port** (J31) — the only port with 12VSW; best drop geometry.
- Mechanical: COTS quick-release clip-plate pair, BOM 2112. The payload bolts
  to the payload-side clip plate: `../../interface/mechanical/2112_attach_plate_payload_side.step`
  (50×50 mm footprint, 10.5 mm thick, "Replaceable Base"). Drone-side plate:
  `2112_attach_plate.step`. Read `../../interface/mechanical/README.md`.
- Bottom payload mounting plane sits at Z ≈ −171 mm in drone frame (origin
  airframe center, +Z up, +Y forward).
- Electrical (via spring-pin blind-mate, 10 circuits): 12V_PL (SSR-gated,
  ~25 W guidance), 12VSW (K1 relay, FMU_CH2-controlled, **2 A fuse** — this
  relay was added to the Main PCB specifically for this dispenser), CAN2
  (DroneCAN), Ethernet, FMU_CH1 PWM, GND. **No 5 V, no UART** — bring a buck
  if logic voltage is needed. Payload must tolerate 12V_PL power cycling.
- Full pinout and power rules: `../../interface/ICD.md` §3–§5.

## Airframe geometry (derive, don't guess)

Canonical Quiver CAD (origin/main worktree): `/tmp/pq-main/src/quiver/`
- Landing gear: `airframe_structure/landing_gear/` STEPs — DERIVE ground
  clearance under the bottom payload plane and record the number.
- Props/arms: `airframe_structure/motor_arm/`, `equipment/propulsion/`.
- The dispenser + full 250-pellet load hangs below the belly: it must clear
  the ground at rest on landing gear (with margin) and stay out of prop disks.
- Platform payload budget: 5–8 kg total. Dispenser target: ≤ 1.5 kg TOTAL at
  a 250-pellet load (295 g of pellets); every 100 g above 1.0 kg must be
  justified in the mass ledger. Capacity above 250 is encouraged (see
  Requirements) — extra pellet mass beyond the 250-load baseline does not
  count against the 1.5 kg ceiling, but state the full-load total and keep it
  sane against the platform budget and clip-plate loads.

## Tooling (verified working on this machine)

- Python venv with build123d, trimesh, matplotlib, numpy, PIL:
  `~/.openclaw/workspace/venvs/dock-cad-314/bin/python`
- CAD: parametric build123d in `cad/dispenser.py`; export STEP+STL to
  `cad/exports/`, renders (PNG, cream #faf7f0 background, z-sorted
  Poly3DCollection or offscreen rasterizer — see
  `~/projects/payload-systems/assets/` hero image style) to `cad/renders/`.
- Sim: plain numpy Monte Carlo; plots styled cream/black/orange like
  `~/projects/quiver-dock/rev1/sim/` outputs.
- Web research: use web search/fetch tools; cite URLs in research docs.

## Output layout (all inside payloads/brush-bullet-dispenser/)

- `_run/` — run docs (research, judging, build notes, risk register). NOT
  shipped in the eventual PR.
- `README.md` (per ../_template/), `cad/`, `electronics/`, `sim/`, `docs/` —
  the shipped package. Declare ICD version 1.0.

## Directive added mid-run (Thomas, 2026-08-06 23:03)

> "One thing I might be worried about is a possible jam if a fragment gets in
> to the pocket wheel slot, you'd have 1.5 brush bullets and it could prevent
> the wheel from turning"

HARD REQUIREMENT for the pocket-wheel design: the fragment-overfill wedge jam
(pocket holds 1 pellet + a fragment standing proud of the shear line, wedging
the disc against the housing) must be explicitly designed against and
explicitly critiqued. The design must show, with geometry and numbers:
1. **Rejection before wedge:** overfill relief at the pocket exit from the
   hopper zone (compliant wiper/brush and/or relief chamfer geometry) that
   pushes a proud fragment back into the hopper instead of carrying it into
   the close-clearance housing arc.
2. **Shear capability as backstop:** if a fragment does enter the arc, the
   actuator torque at the pocket radius must exceed the force to shear/crush a
   pellet fragment (pellets are compressed/molded herbicide — estimate crush
   strength from research data, label the assumption) with stated margin.
3. **Detect + recover:** stall detection (e.g. TMC2209 StallGuard or current
   sensing) with an automatic reverse-oscillate recovery routine, and the
   count sensor must stay truthful through a recovery (no phantom counts).
4. **Pocket geometry:** state the pocket depth/diameter vs pellet + largest
   credible fragment, and where a fragment settles (below shear line = safe).
The pellet-path critic must attempt to CONSTRUCT this jam geometrically
(worst-case fragment size/position) and pass only if the design defeats it.
