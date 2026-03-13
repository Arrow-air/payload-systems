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

## Platform Compatibility

| Platform | Attachment Interface | Power Available | Data Interfaces |
|---|---|---|---|
| **Quiver (PT3+)** | Quick-release, 3× mounting points (bottom + 2× side) | 12V switched, 12V always-on | Ethernet, CAN, UART, PWM (FMU_CH1) |
| **Quiver Mini** | Bottom-only, Quiver-compatible interface V1 | 6S-derived (TBD) | TBD |
| Future platforms | To be defined | — | — |

### Attachment Interface Pinout (Quiver PT3)

The standard payload connector is a **12-pin MOLEX locking header** (part #2077601281, mating #2045231201). A 10-pin 2.54mm header variant is also supported.

| Pin | Function | Notes |
|---|---|---|
| 1, 3 | ETH_RX+, ETH_RX- | 100BASE-T Ethernet |
| 5, 7 | ETH_TX+, ETH_TX- | 100BASE-T Ethernet |
| 2, 4 | 12VSW | Switched 12V (FC-controlled on/off) |
| 6 | +12V | Always-on 12V |
| 8 | FMU_CH1 | PWM output from flight controller |
| 9, 10 | CAN1_P, CAN1_N | CAN bus |
| GND | GND | Common ground |

> The Attachment Interface PCB design files (KiCAD schematic, layout, gerbers, BOM) live in the [project-quiver repo](https://github.com/Arrow-air/project-quiver/tree/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB).

**Power budget guidance:**
- 12VSW is controlled by the flight controller — payloads should handle clean enable/disable
- For payloads requiring 5V (e.g. Raspberry Pi): use an onboard buck converter (Mean Well SD-25B-05 or equivalent, rated for 60V+ input on Quiver's 14S system)
- Total payload power draw: design within ~25W per interface (conservative; verify against Main PCB limits before exceeding)

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

### ⚪ Proposed — Needs Champions

These are on the community radar but have no active development yet. The full source list (with detailed descriptions and requirements for each) is the [possible attachments document](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/equipment/attachment/0001-possible_attachment_list/information-note.md) in project-quiver.

#### UAV Logistics
| Payload | Key Requirements |
|---|---|
| **Universal Cargo Container** | Fixed or releasable; aerodynamically optimised; stackable; may include aux storage/control interface |
| **Surface Water Sourcing System** | 10–12L pump + container; shore/water-surface landing capability; instant water tester optional; extended intake arm |

#### Remote Sensing & Imaging
| Payload | Key Requirements |
|---|---|
| **Standard FPV Camera** | Fixed (non-gimbaled); ≥720p @ 45fps video TX; no image crop/timing modification; vibration damped |
| **Standard Magnification Gimbaled Camera** | 3-axis gimbal; ≥1/2" sensor @ 30fps; dual-sensor (≈24mm + ≥85mm equiv. FL); switchable video feed |
| **Multispectral Imagery System** | RGB + NIR; synchronous shutter; sunlight (downwelling) sensor on top; optional nadir 3-axis gimbal |
| **Advanced IR Optical Gas Imaging Camera** | 3-axis gimbal; ≈50mm equiv. FL; ≥25fps; sensitivity covers common industrial/petrochemical gases |
| **General Stabilized Sensor Device Carrier** | 3-axis gimbal; 1/4-20 mount; 5–8kg capacity; follow-focus + signal outlet optional |
| **Standard Geiger-Mueller Counter** | 2+ sensors for cross-reference; cosmic ray background shielding; high vibration protection; obstacle avoidance pairing |
| **Ground Target Machine Vision System** | On-board compute (RPi/Jetson); target sort by size/shape/color/spectral; raster-to-vector; KML/KMZ output |

#### UAV Geophysics
| Payload | Key Requirements |
|---|---|
| **Low Altitude Magnetic Anomaly Sensor** | Zero/minimal ferrite components; distancing pylon from airframe; multi-axis compass + fusion algorithm; stable heading during flight |
| **Compact Synthetic Aperture Radar** | High-precision GNSS + IMU + PPS timing; ≥1m resolution @ 2km; SDR-configurable frequency and scan direction |
| **General Aerial LiDAR Scanner** | High-precision GNSS + IMU + PPS; ≥32 laser channels @ ≥20Hz; ≥1cm accuracy @ 100m; optional nadir 3-axis gimbal |
| **Sentinel LiDAR (stationary full-dome)** | Mounts on top of airframe; full-dome coverage while landed; integrates Leica BLK-class scanners; GNSS integration; RGB coloured point cloud output |
| **Aerial Water Body Sampling System** | Deploys/retrieves from aircraft; surface water collection; optional in-flight analysis; close-water risk mitigation |

#### Interactive / Broadcast
| Payload | Key Requirements |
|---|---|
| **Airborne Speaker** | Directional; ≥200m range; live voice / pre-record / TTS; multi-speaker option |
| **High Capacity Flood Light** | Train-light-class brightness; 45–60° beam; 4000–4500K; flash/breathe modes |
| **General Fishing Equipment** | Buoy/water-landing system; remote-controlled gear; downward 3-axis gimbal; emergency cutoff; waterproof (storm-rated) |
| **Aerial Pellet Spreader** | Seeds/fertiliser/granules; capacity sensor; centrifugal or cyclonic dispersal; anti-blockage design; rain/moisture proof |
| **Multi-Purpose Robotic Arm** | Multi-joint, foldable; side-mountable; minimal CG shift; safety switch + emergency detach |
| **Tethering Converter** | Ground AC → stable onboard DC; backup battery for emergency landing; tether wear protection; optional signal/substance conduit |
| **Airborne Electrical Warfare System** | SDR-controlled ISM + GNSS jamming; directional PCB panel antenna; standing-wave protection; 915MHz/1.2GHz backup control link *(significant regulatory considerations)* |

#### Flight Assistance & Safety
| Payload | Key Requirements |
|---|---|
| **Arrow Airframe Parachute System (AAPS)** | 100% reliability target; ballistic/pressure-launched; ≥20m minimum deployment altitude; maintenance-free design goal |
| **Passive Propeller Defense System** | Protects propellers from horizontal/diagonal terrain and object incursion; lightweight/composite; impact shock absorbing; non-frangible |
| **Mechanical Comm-Link Extension (Antenna Tracker)** | Directional PCB panel antenna; 2-axis gimbal (aircraft + ground); slip ring connectors; dual-pair failsafe option |

---

## How to Contribute

1. **Check the discussions** — see what's already being designed before starting fresh
2. **Open a discussion** — new payload idea? Start a thread and gather input before committing to design
3. **Follow the structure** — when a payload is ready for a design brief, create a folder `payloads/<payload-name>/` with a `README.md` covering: purpose, requirements, architecture options, BOM, and open questions
4. **Interface compatibility** — any payload targeting Quiver must respect the attachment interface pinout and mechanical envelope; reference the Attachment Interface PCB docs

### Folder Structure (proposed)

```
payloads/
├── multispectral-camera/
│   ├── README.md          ← design brief
│   ├── bom/
│   ├── cad/
│   └── firmware/
├── cargo-container/
└── ...
docs/
├── attachment-interface.md
└── power-budget.md
```

---

## Community & Governance

- **Discord:** [#multi-spectral-camera](https://discord.com/channels/853833144037277726/1481622578132025364) and other payload channels in the Arrow server
- **Arrow DAO:** Payload development can be funded via Arrow grants & bounties
- **License:** Hardware and documentation in this repo is released under [CERN OHL-S v2](https://ohwr.org/cern_ohl_s_v2.txt); software under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

---

*This repo is maintained by the Arrow community. All are welcome.*
