# Arrow Payload Systems

Open-source payload systems for Arrow UAV platforms.

This repository is the home for community-designed payload attachments that interface with Arrow drones — starting with Quiver, and expanding to cover any Arrow platform that uses the standard attachment interface.

---

## What This Repo Is For

Arrow's drone platforms are designed from the ground up to be modular. The airframe is a carrier; the payload is the mission. This repo exists to:

- Document the **payload attachment interface standard** so anyone can design compatible payloads
- Host **design briefs, specifications, and build documentation** for community payload projects
- Coordinate development across contributors and track progress from concept to flight-ready

If you have an idea for a payload, or want to contribute to one already in progress, this is the place.

---

## The Attachment Interface

The authoritative specification is the **[Interface Control Document (ICD)](interface/ICD.md)** — per-port capabilities, pinouts, power rules, network conventions, and the mechanical mate. Payload designs declare the ICD version they target. Summary:

| Platform | Attachment Interface | Power | Data |
|---|---|---|---|
| **Quiver (PT3+)** | Quick-release, 3× hot-swap points (bottom + 2× side) | 12V_PL all ports (SSR-gated, ~25W guidance); 12VSW bottom only (2A) | Ethernet (all ports), CAN2/DroneCAN (all ports), 1× PWM aux per port |

Key facts (details and caveats in the ICD):

- **The three ports are not identical** — 12VSW and its relay exist only on the bottom port, PWM channel numbers differ per port, and the ports split across two Ethernet switch modules. Check the ICD §2 capability matrix.
- **Blind-mate electrical connection** via the Attachment Interface PCB (V1.4, validated): the aircraft carries spring-loaded pins, the payload side populates landing pads. Design files live in [project-quiver](https://github.com/Arrow-air/project-quiver/tree/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB).
- **No 5V, no UART** at the connector — payloads bring their own logic-rail DC-DC.
- **Mechanical mating geometry** (STEP) and mounting-point coordinates are vendored in [`interface/mechanical/`](interface/mechanical/).

---

## Payload Concepts

The following payload types have been identified by the Arrow community as high-value targets. They range from near-term buildable to longer-horizon R&D.

### 🟢 Active / In Progress

| Payload | Status | Thread |
|---|---|---|
| **Multispectral Camera** | Design brief complete, community discussion open | [#multi-spectral-camera](https://discord.com/channels/853833144037277726/1481622578132025364) |

### 🟡 Defined — Ready for Contributors

These payloads have detailed requirements written and are ready for someone to pick up.

| Payload | Description | Requirements Doc |
|---|---|---|
| **Universal Cargo Container** | Fixed or deployable cargo pod; stackable, manually transportable | [project-quiver](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/001-Universal_Cargo_Container_comprehensive_requirement.md) |
| **General Aerial LiDAR** | Nadir/forward LiDAR scanner; ≥32 channels, ≥20Hz, ≥1cm accuracy @ 100m | [project-quiver](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/002-General_Aerial_LiDAR_Scanning_Device_comprehensive_requirement.md) |
| **Ground Target Machine Vision** | On-board ML inference for target ID/counting; KML/KMZ output | [project-quiver](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/003-Ground_Target_Machine_Vision_System_Comprehensive_Requirement.md) |
| **Standard Magnification Camera** | 3-axis gimbaled; ≥1/2" sensor, 24mm + 85mm+ focal lengths | [project-quiver](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/004-Standard_Magnification_Camera_comprehensive_requirement.md) |
| **General Stabilized Sensor Carrier** | 3-axis gimbal; 1/4-20 mount; 5–8kg capacity; follow-focus optional | [project-quiver](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/005-General_Stabilized_Sensor_Device_Carrier_comprehensive_requirement.md) |
| **High Capacity Flood Light** | ~train-light brightness; 45–60° beam; 4000–4500K; flash/breathe modes | [project-quiver](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/006-High_Capacity_Flood_Light_comprehensive_requirement.md) |

### 💡 Your idea here

The best payload is the one *you* actually need. Quiver is a multipurpose
platform — if there is an attachment you would use, build it. Sensors,
cargo, lighting, sampling, spraying, comms, safety systems: if it fits the
interface, it can fly. A longer inventory of community-discussed concepts
lives in the [possible attachments document](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/equipment/attachment/0001-possible_attachment_list/information-note.md)
in project-quiver if you want inspiration.

Start a thread in the Arrow Discord, copy the
[payload template](payloads/_template/), and design against the
[ICD](interface/ICD.md). Payload development can be funded through Arrow
grants & bounties.

---

## How to Contribute

1. **Check the discussions** — see what's already being designed before starting fresh
2. **Open a discussion** — new payload idea? Start a thread and gather input before committing to design
3. **Start from the template** — when a payload is ready for design work, copy [`payloads/_template/`](payloads/_template/) to `payloads/<payload-name>/` and fill in its README (purpose, requirements, target port, ICD version)
4. **Design against the ICD** — any payload targeting Quiver must respect the [ICD](interface/ICD.md): port capabilities, pinout, power rules, and mechanical envelope. Run the ICD §8 checklist before requesting review.

### Repo Layout

```
interface/
├── ICD.md            ← the interface standard (versioned)
├── mechanical/       ← mating STEP files + mounting-point coordinates
└── pcb/              ← pointer to the Attachment Interface PCB in project-quiver
payloads/
├── _template/        ← copy me to start a new payload
└── <payload-name>/   ← one folder per payload: README, cad/, pcb/, software/, docs/
```

Payload folders are created when real design work starts — concepts live in the tables above until then.

---

## Community & Governance

- **Discord:** [#multi-spectral-camera](https://discord.com/channels/853833144037277726/1481622578132025364) and other payload channels in the Arrow server
- **Arrow DAO:** Payload development can be funded via Arrow grants & bounties
- **License:** Hardware and documentation in this repo is released under [CERN OHL-S v2](https://ohwr.org/cern_ohl_s_v2.txt); software under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

---

*This repo is maintained by the Arrow community. All are welcome.*
