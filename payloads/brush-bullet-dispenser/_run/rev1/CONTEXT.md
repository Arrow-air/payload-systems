# REV-1 CONTEXT — Brush Bullet Dispenser CAD completion run (2026-08-07)

Read this whole file before doing anything. Never invent facts; label every
assumption as an assumption. This file supersedes `_run/CONTEXT.md` where they
conflict; otherwise rev-0 context still applies (pellet = 1.18 g, Ø12 mm
agricultural herbicide granule; ≥250 pellet capacity floor; bottom port;
payload mounts on the payload-side clip plate STEP).

## What this run is

Rev-0 (run `wf_240e82ad-f48`, 2026-08-06→07) produced a complete design story
for the pocket-wheel metering dispenser but the CAD does not close: an
independent red team confirmed blockers on the exported geometry. This run's
ONLY job is to make the CAD close against the punch list. No new mechanism
exploration, no trade study, no simulation, no software. The pocket-wheel
concept as judged (`_run/CONCEPT-pocket-wheel.md`, `_run/JUDGING.md`) stays.

## Thomas's directives (2026-08-07 morning, verbatim, HARD RULES)

1. **Electrical mate is SOLVED — out of scope.** "We know that the PCBs mate
   electrically when the attachment interface pieces connect. You don't have
   to worry about that part at all." Do NOT model, measure, or re-litigate
   spring-pin/pad stack-up (rev-0's RT-2 pin-gap finding is void). Treat the
   payload-side attachment interface (clip plate + pads-only interface PCB)
   as a black box that delivers a wiring harness at its location.
2. **The dispenser DOES need an electronics home:** "We do need a place for
   the wiring and electronics on the dispenser side of it though, right now
   it looks like the wiring would go straight into the tank." → A sealed,
   dust-tight electronics bay housing the control PCB (STM32G431 + TMC2209 +
   count-sensor analog chain per `electronics/ELECTRONICS.md`), plus a
   routed wiring channel from the interface PCB to the bay and from the bay
   to motor + count sensor. Wiring must NOT pass through the hopper volume.
3. **Interface reach-in clearance:** "the way the attachment interface is
   integrated may make it difficult to reach in and connect/disconnect it
   from the drone. Maybe it would help to give it some more clearance from
   the rest of the dispenser." → Stand the attachment-interface region off
   from the dispenser body so a gloved hand can reach the quick-release and
   work the connect/disconnect on the aircraft. Prove it with a measured
   access corridor, not adjectives.
4. **Refill workflow = remove the whole dispenser from the drone.** Dock
   compatibility is moot ("We wouldn't be using this payload with the dock
   anyways"). Whole-dispenser swap is the baseline; a swappable pre-filled
   cartridge is a stretch goal ONLY if it falls out easily — do not redesign
   the architecture around it in this run.
5. **Capacity is settled.** 1–3 batteries of pellets per hopper is fine
   ("we only need to reload the dispenser every other flight"). Keep the
   ~422-pellet hopper as-is unless a punch-list fix forces a change. Do not
   re-open the capacity trade.
6. **Simulation is skipped** for this run, per Thomas.

## Punch list sources (read in this order)

- `_run/RED-TEAM.md` — 21 findings; RT-1 (assembly/torque path) and RT-3
  (count-sensor hardware absent from CAD) are the confirmed CRITICAL CAD
  blockers. RT-2 is void per directive 1 EXCEPT its electronics-bay
  implication (directive 2). RT-14 (refill has no stable rest position /
  fill-port geometry) should be addressed via directive 4 + a side-wall fill
  port above the 250-pellet line or an equivalent measured solution.
- `_run/GAP-REVIEW.md`, `_run/BUILD-NOTES-r6.md` (r6 open issues list).
- `electronics/ELECTRONICS.md` §4.2–4.4 — the count sensor the CAD must
  actually contain: ECO-3 dual staggered Ø3.2 beam apertures + ECO-9 6 mm
  vertical stagger, analog VBPW34FAS/OPA2320 receive chain (BOM must drop the
  rejected TSSP4038), sacrificial bore-face window (ECO-4), labyrinth (ECO-5).

## Standing rev-0 rules that still bind

- Parametric build123d model at `cad/dispenser.py`, venv python per rev-0
  CONTEXT. Exports (STEP+STL) to `cad/exports/`, renders to `cad/renders/`
  (rev-1 rounds: `v1r<N>_*.png`, cream background).
- Structure mass target ≤1500 g dry; report loaded mass at 250 and at max
  fill. Ground clearance on the real landing-gear STEPs ≥ stated margin.
- Fragment-jam requirement (Thomas, 2026-08-06): overfill relief before the
  housing arc, shear-margin backstop, stall-detect + reverse-oscillate
  recovery that keeps the count truthful, pocket geometry stated vs worst
  credible fragment. Rev-1 must not regress any of this.
- Critic approvals must print the actual measured numbers. Builders' notes
  must quote tool output, not restate it (rev-0 RT-19: narrated "fixes" the
  geometry didn't contain).
- Wording: this is an agricultural granule dispenser for herbicide pellets.
  Describe it that way (granule singulation, metering, drop tube). Avoid
  weapons-adjacent framing (no "projectile", "ballistics", "BB", "airsoft").

## Deliverables

Closed CAD (all critics pass or plateau-with-complaints explicitly recorded),
updated `cad/BOM.md`, updated `README.md` + `docs/DESIGN.md` rev-1 section
(honest: what closed, what remains), `_run/rev1/RUN-RESULT.md`. Commit on
branch `brush-bullet-dispenser`, author `thomasg <thomas@arrowair.com>`.
Do NOT push.
