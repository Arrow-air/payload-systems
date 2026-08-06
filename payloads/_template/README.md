# Payload Name

> Copy this folder to `payloads/<your-payload-name>/`, fill in this README,
> and open a PR. Delete the quoted instructions as you go.

**Status:** concept | design | prototype | flight-tested
**Target port(s):** bottom / side 1 / side 2
**ICD version:** 1.0
**Champion:** your name / Discord handle
**Discussion:** link to Discord thread

## What it does

> One paragraph. What mission does this payload fly?

## Requirements

> Link the requirement doc in project-quiver if one exists
> (`task-grant-bounty/equipment/attachment/`), or write the key requirements
> here: mass, power draw, data interfaces used, environmental limits.

| | |
|---|---|
| Mass | — kg |
| Power | — W from 12V_PL |
| Data | Ethernet / CAN2 (DroneCAN) / PWM |
| Port | bottom |

## Folder layout

- `cad/` — mechanical design (STEP exports + parametric source). See
  [`interface/mechanical/`](../../interface/mechanical/) for the mating
  geometry and drone coordinates.
- `pcb/` — payload-side electronics (KiCad). The blind-mate board is the
  pads-only Attachment Interface PCB — see
  [`interface/pcb/`](../../interface/pcb/).
- `software/` — companion-computer service / DroneCAN node code. See the
  [Quiver SDK Developer Guide](https://github.com/Arrow-air/project-quiver/blob/main/docs/Develop-Attachments-Software/Quiver-SDK-Developer-Guide.md).
- `docs/` — build guide, test results, integration notes.

## Compliance

> Run through the ICD §8 checklist and note anything nonstandard here
> (extra termination, unusual power profile, protruding envelope, etc.).
