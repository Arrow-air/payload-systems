# Mechanical Interface — Quick-Release Mounting Points

Vendored from project-quiver (BOM 2100, `src/quiver/supporting_structure/attachment_interface/`).
These files are copies for payload-design convenience; the originals in
project-quiver are the source of truth.

## Files

| File | Part | Used |
|---|---|---|
| `2112_attach_plate.step` | Quick-release interface plate (aluminum) — the drone-side mechanism your payload clips into | 3× (all ports) |
| `2111_attach_spacer.step` | Side-port spacer (PETG) | 2× (left/right) |
| `2131_attach_spacer_bottom.step` | Bottom-port spacer with wiring notch (PETG) | 1× (bottom) |

The plate STEP contains the drone side of the quick-release mechanism
(fixed top, press pins, springs). Your payload provides the mating side.

## Mounting-point positions (drone coordinates)

Frame: origin at airframe center, **+Z up, +Y forward**. Positions are
interface-plate center-of-mass values from the PT3 master model (confirmed
accurate to the flying aircraft, 2026-08).

| Port | Plate position (x, y, z) mm | Mechanism faces |
|---|---|---|
| Bottom | (0, 0, −160.7) | −Z (down) |
| Side 1 / Right | (+185.65, −0.02, −71.0) | +X (outboard) |
| Side 2 / Left | (−185.65, +0.02, −71.0) | −X (outboard) |

The drone-side plate hardware is ~10 mm thick, so a bottom payload's top
mounting plane sits at roughly **Z = −171 mm**. Side ports include a 3 cm
extension adapter for clearance from the airframe body; cable ports face
sideways to prevent abrasion and water ingress.

## Designing the payload side

- Start from the parametric example in project-quiver:
  [`src/quiver/attachments/designs/example_plate/`](https://github.com/Arrow-air/project-quiver/tree/main/src/quiver/attachments/designs/example_plate)
  — it builds a placeholder plate positioned on the bottom interface and can
  render your design in place on the full drone CAD
  (`python -m quiver.attachments.designs.example_plate.assembly --show`).
- Envelope: no formal keep-out volumes are published yet. Practical limits:
  propeller disk clearance for anything wide, ground clearance on landing
  gear for bottom payloads, and the battery-slider travel for side payloads.
  When in doubt, load your STEP against the full drone assembly.

## TODO (tracked)

- [ ] Formal keep-out / envelope STEP exported from the full PT3 assembly
- [ ] Payload-side mating geometry reference (the clip-in counterpart)
- [ ] Per-port structural mass limits
