# Quiver Payload Attachment Interface — Interface Control Document (ICD)

**ICD version:** 1.0-draft
**Applies to:** Quiver PT3 and later
**Source of truth:** the aircraft-side hardware is owned by
[project-quiver](https://github.com/Arrow-air/project-quiver). This document is
derived from the canonical KiCad sources (`src/pcb/main_pcb/`) and CAD
(`src/quiver/supporting_structure/attachment_interface/`) and is versioned so
payload designs can declare what they were built against. If this document and
the project-quiver sources disagree, the sources win — and please file an issue.

---

## 1. Overview

Quiver carries payloads on **three hot-swappable quick-release mounting
points**: one on the belly (bottom) and one on each side of the battery
compartment. Each point provides the same mechanical mate and a blind-mate
electrical connection carrying power, Ethernet, CAN, and one PWM auxiliary
channel. Payloads require no tools to install or remove.

Platform budget: **25 kg MTOW, 5–8 kg total payload capacity** across all
mounting points. Per-port structural limits are not yet formally specified;
see §6.

## 2. Port capability matrix

The three ports are **not identical**. Design against the port you target:

| Capability | Bottom (J31) | Side 1 / Right (J29) | Side 2 / Left (J30) |
|---|---|---|---|
| **12V_PL** — main 12 V payload rail | ✓ | ✓ | ✓ |
| **12VSW** — relay-switched 12 V (2 A fused) | ✓ | — | — |
| **CAN2** (DroneCAN) | ✓ | ✓ | ✓ |
| **Ethernet** 100BASE-T | ✓ (switch 1) | ✓ (switch 1) | ✓ (switch 2) |
| **PWM aux channel** | FMU_CH1 | FMU_CH7 | FMU_CH8 |
| Suggested static IP | 192.168.144.100 | 192.168.144.101 | 192.168.144.102 |

> Historical note: pre-update Main PCB documentation showed CAN1 on the bottom
> and right ports and no Ethernet on the left port. The current Main PCB
> revision routes **CAN2 to all three ports** ("all payloads operate on CAN2")
> and Ethernet to all three ports. The Attachment Interface PCB silkscreen and
> net names still say `CAN1_P/CAN1_N`; electrically this is the CAN2 bus.

## 3. Power

### 12V_PL (all ports)
- Sourced from the Main PCB 12 V rail through two series fuses and a
  **solid-state relay (U5)** controlled by flight-controller channel
  **FMU_CH4**. Enabled by default in the standard configuration, so it behaves
  as always-on — but it is *not* hardwired. The FC can drop and restore the
  rail (e.g. to hard power-cycle a hung payload). **Payloads must tolerate
  power appearing late, being removed at any time, and repeated cycling.**
- The rail is shared by all three ports: one SSR, common fusing. Budget
  guidance: design within **~25 W per port** and verify total draw against
  Main PCB limits before exceeding.

### 12VSW (bottom port only)
- 12 V switched through mechanical relay **K1** (SPST-NO, controlled by
  **FMU_CH2**), fused at **2 A** (F1). Intended for FC-commanded on/off loads
  (originally the brush-bullet dispenser motor). Max ~24 W.

### Other voltages
- **No 5 V or 3.3 V is provided.** Payloads needing logic rails bring their own
  DC-DC (e.g. Mean Well SD-25B-05 class buck for 5 V).
- **No UART** is available at the payload connector.

## 4. Data

### Ethernet
- 100BASE-T, one TX and one RX differential pair per port, via two Ethernet
  switch modules on the Main PCB (bottom and side 1 on switch 1, side 2 on
  switch 2).
- The Quiver network is a **flat static 192.168.144.0/24 — no DHCP** (Siyi
  firmware conflicts with DHCP servers). Payloads use static IPs from the
  developer range **.100–.199**; recommended per-port assignments in §2.
- Reserved addresses (do not use): .11, .12, .20, .25, .50 (companion Pi),
  .51 (flight controller), .60. See the
  [Quiver SDK Developer Guide](https://github.com/Arrow-air/project-quiver/blob/main/docs/Develop-Attachments-Software/Quiver-SDK-Developer-Guide.md)
  for the full map and the companion-computer service architecture.

### CAN
- **CAN2 bus, DroneCAN protocol**, shared by all three ports plus the
  companion computer. A 120 Ω termination (R14) is switchable on the Main PCB
  (S2). **Payloads must not add bus termination** without coordinating with
  the airframe configuration.

### PWM auxiliary
- One direct flight-controller PWM output per port (see §2 for channel
  mapping). Note the channel differs per port — firmware/Lua that assumes
  FMU_CH1 only works on the bottom port.

## 5. Connector chain and pinouts

Main PCB (J31/J29/J30 power+CAN+PWM, 6-pos 2.50 mm; J39/J37/J38 Ethernet,
4-pos) → harness → **12-pin Molex locking connector** on the Attachment
Interface PCB → **spring-pin blind-mate** across the quick-release → payload.

### Attachment Interface PCB (the blind-mate)
- Design files: [project-quiver `0003-Attachment-Interface-PCB`](https://github.com/Arrow-air/project-quiver/tree/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB),
  current revision **V1.4** (`2026-Update/`).
- One board layout serves both sides: the **drone side populates spring-loaded
  pins (U1–U10)**; the **payload side populates only the enlarged landing pads
  (U11–U20)**. Alignment is provided by the quick-release mechanism; a
  silkscreen notch marks orientation.
- The spring-pin mate configuration is **validated** (electrically tested).
- Board: 23.5 × 15.8 mm, 1.2 mm FR4, 4× M2 mounting holes.

**10-pin blind-mate pinout** (drone-side pins → payload-side pads):

| Pin | Function |
|---|---|
| 1 | ETH_RX+ |
| 2 | 12VSW *(bottom port only; unconnected on sides)* |
| 3 | ETH_RX− |
| 4 | GND |
| 5 | ETH_TX+ |
| 6 | +12V (12V_PL) |
| 7 | ETH_TX− |
| 8 | FMU_CHx (per-port channel, §2) |
| 9 | CAN2_H *(labelled CAN1_P on board)* |
| 10 | CAN2_L *(labelled CAN1_N on board)* |

**12-pin Molex J1** (harness side, Molex 2077601281 / mate 2045231201):
doubled power and ground pins for current capacity — pinout in the
[Attachment Interface PCB README](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/README.md).

## 6. Mechanical

See [`mechanical/`](mechanical/) for the vendored STEP files, mounting-point
positions in drone coordinates, and envelope guidance. Summary:

- Quick-release plate mechanism (machined aluminum, spring press-pins) at each
  port; PETG spacers mount the plates to the airframe. Side ports sit on 3 cm
  extension adapters for body clearance; the bottom spacer has a wiring notch.
- Drone coordinate frame: **origin at airframe center, +Z up, +Y forward.**
  Bottom interface plate at Z ≈ −160.7 (payload mounting plane ≈ −171);
  side plates at X ≈ ±185.7.
- Per-port structural mass limits: **not yet formally specified** — the
  platform-level 5–8 kg budget governs. Heavy payloads (>3 kg on a single
  port) should be reviewed against the airframe before flight.

## 7. Software integration

Payloads integrate through the companion computer (Raspberry Pi, .50):
DroneCAN devices are bridged to telemetry; Ethernet payloads get REST/WebSocket
pipelines to Quiver Hub (telemetry, point cloud, camera/WebRTC, custom payload
apps). Start with the
[Quiver SDK Developer Guide](https://github.com/Arrow-air/project-quiver/blob/main/docs/Develop-Attachments-Software/Quiver-SDK-Developer-Guide.md).

## 8. Designing a payload — checklist

1. Pick your port(s) from the capability matrix (§2).
2. Mechanical: mate to the quick-release plate; stay inside the envelope
   (§6 / `mechanical/`); mind prop clearance for wide payloads.
3. Electrical: payload-side Attachment Interface PCB (pads-only population),
   own DC-DC for logic rails, tolerate 12V_PL power cycling, no CAN
   termination.
4. Network: static IP in the assigned range, or DroneCAN on CAN2.
5. Software: integrate via the SDK guide's payload pipelines.
6. Declare the ICD version your design targets in your payload README.

## Revision history

| ICD version | Date | Changes |
|---|---|---|
| 1.0-draft | 2026-08-06 | Initial ICD from verified PT3 Main PCB (current KiCad netlist), Attachment Interface PCB V1.4, and BOM 2100 CAD. |
