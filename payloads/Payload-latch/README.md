# Quiver Actuated Payload Latch V1

**Status:** flight-tested (prototype, see Remarks for unmet criteria)
**Target port(s):** bottom
**ICD version:** 1.0-draft
**Champion:** Erick Perdomo (errrks)
**Discussion:** https://dao.arrowair.com/t/bounty-v1-quiver-actuated-payload-latch/155

# Status

`Valid, as built at Meetup 2026, flight tested 2026-08-13 (approximate). Information note for project-quiver T-11 (issue #257).`

Built by Erick Perdomo and Alperen. This README is the V1 information note. It records the hardware that flew, the flight controller configuration that drove it, the tests that were and were not run, and what V2 should change. The design intent lives in the Meetup 2026 build pack and is superseded here where they differ.

# Project Description

Servo actuated cargo hook for slung loads on the Quiver bottom port. An off the shelf aluminum sliding pin release block, driven by a standard size servo, is carried on a printed PA6-CF bracket bolted to the JMRRC quick release clip plate. The flight controller drives the servo directly over the port's PWM auxiliary channel. There is no microcontroller and no return spring in V1.

Origin: DAO bounty 155 ($500 USDC, unclaimed), folded into an in-house meetup build charged to QGB-05. The bounty requirements (2 kg safe working load, under 250 g, 3.3 V GPIO trigger, mechanically closed on power loss, 20 cycle reliability) remain the evaluation baseline. See Remarks for which are met.

| | |
|---|---|
| Mass | Not weighed (design estimate ~240 g) |
| Power | 12V_PL through an LM2596 buck at 6 V. Idle under 1 W, servo stall bound ~15 W for under 1 s |
| Data | PWM (FMU_CH1) |
| Port | bottom |

# Methodology

1. Parts per the meetup build pack BOM: powerday 995 alloy release unit (Amazon B07HKF6C5P), Deegoo-FPV MG995 servo (Amazon B07NQJ1VZ2), Zovfam LM2596 buck 10 pack (Amazon B08BFKKDGD), Molex 204523-1201 housing with 79758-1149 pre-crimped leads, JMRRC male clip plate, Attach Interface PCB V1.4 payload side.
2. Bracket modeled and printed in PA6-CF, heat set M3 inserts for the servo frame. CAD in `CAD/V1-Servo-Payload-Mount.step`.
3. Servo endpoints measured at linkage fitting with the servo on a bench PWM source: 1315 µs pin home, 1750 µs pin retracted.
4. Buck trimmed to 6 V at its output with a DMM, unloaded, before the servo was connected.
5. Flight controller outputs freed from the GPIO mask and configured for RC passthrough (see Results, FC configuration).
6. Bench cycles from Mission Planner on outputs 9, 15, and 16, then two flights with a 370 g load and one 1 kg drop.

# Results and Deliverables

## Mechanism

- powerday 995 aluminum pin block with its servo frame. MG995 with a blue 25T aluminum horn. M3 bolt and nyloc nut as the linkage pivot.
- **No return spring.** The servo drives and holds the pin in both positions. With power removed the pin is retained by gear friction only.
- One L shaped PA6-CF bracket. Four M3 socket heads into heat set inserts hold the servo frame. The buck sits exposed on the bracket top face. The bracket bolts to the JMRRC male clip plate, which carries the Attach Interface PCB V1.4 payload side (10 pads) on 4× M2.
- Printed zip tie saddle on the bracket side for lead strain relief.
- Single structural path through the clip plate. No secondary strap.

## Electrical

Power chain: 12V_PL (J1 pin 10) → LM2596 buck IN+ → 6 V OUT → servo. Servo power leads soldered to the buck output pads.

Buck listing specs (2026-09-17): input 3 to 40 V, output 1.3 to 35 V, 2 A continuous, 3 A peak with heatsink recommended above 2 A or 15 W, 92% peak efficiency, 65 kHz, thermal shutdown and current limit, 43 × 21 × 14 mm.

Harness on Attach Interface PCB J1:

| J1 pin | Signal | Connection |
|---|---|---|
| 8 | GND | Buck IN−, servo ground via buck OUT− |
| 10 | +12V (12V_PL) | Buck IN+ |
| 12 | FMU_CH1 | Servo signal lead, solder heat shrink joint |

No inrush limiter, no fuse, no series resistor, no pulldown, no bulk capacitor beyond the buck's own output cap.

## Flight controller configuration

Confirmed on the second Dev-Kit, 2026-08-12. Full procedure in project-quiver `docs/Operations/Initial-Configuration-Guide.md` section 11.6.

| Port | FC pin | ArduPilot output |
|---|---|---|
| Bottom | FMU_CH1 | SERVO9 |
| Side 1 | FMU_CH7 | SERVO15 |
| Side 2 | FMU_CH8 | SERVO16 |

The HOU baseline ships `SERVO_GPIO_MASK = 65520`, claiming outputs 5 through 16 as GPIO. A masked output produces no PWM. Clear the bit for the port in use (bottom only: 65264, all three payload channels: 16112), write, reboot. The flown unit used 12016.

Latch parameters as flown (from a work in progress snapshot, verify on the vehicle):

```
SERVO_GPIO_MASK   12016     ; outputs 9, 13, 15, 16 freed for PWM
SERVO9_FUNCTION   148       ; RCIN9Scaled, RC channel 9 scaled into MIN/MAX
SERVO9_MIN        1315      ; locked
SERVO9_MAX        1750      ; released
RELAY6_FUNCTION   1         ; 12V_PL rail (FMU_CH4, pin 53)
RELAY6_PIN        53
RELAY6_DEFAULT    0
```

Bench alternative: `SERVO9_FUNCTION = 0` and drive the Servo 9 row on the Mission Planner Flight Data → Servo/Relay page with Low/High typed as 1315/1750.

Transmitter: any radio with channel 9 on a two position switch. Low is locked. The switch is the operator's choice.

Ground procedure: Relay 6 on, confirm the pin is home, load the ring or loop onto the pin, arm. Any Relay 6 toggle in flight power cycles the latch.

## Test record

| Test | Result |
|---|---|
| Bench, no load, repeated cycles from outputs 9, 15, 16 | Passed |
| Two flights, 370 g bottle on a zip tie loop, drops at 10 m and 5 m, RC channel 9 | Released cleanly both times, mechanism unaffected |
| 1 kg first aid kit drop | Released cleanly |
| 2 kg static load, 20 cycles (bounty reliability) | Not run |
| Power loss with load hanging (bounty failsafe) | Not run |
| RC failsafe behavior | Not run |
| Mass, current, buck under load | Not measured |

Photos and drop videos: Arrow Discord and the Arrow Twitter account, meetup week of 2026-08-10.

## Deliverables

- `CAD/V1-Servo-Payload-Mount.step`, `.stl` (CERN OHL-S v2)
- This README (CC BY 4.0)
- Flight controller configuration section 11.6 in project-quiver

# Remarks

1. **Failsafe criterion not met.** No spring. An unpowered servo holds the pin by friction only, and 12V_PL drops on every Relay 6 cycle and reboot. Untested with load. V2 needs a mechanical lock on power loss.
2. **Reliability criterion not run.** 20 cycles at 2 kg still owed. Flown loads were 370 g and 1 kg.
3. **Structure.** Single load path through the clip plate. The ICD and the requirement docs ask for two rigid connections or a rated tether.
4. **Electrical protection.** No inrush limiting (AB-1), no local fuse, exposed buck and trimmer, trim set unloaded and not locked. A stalled MG995 (~2.5 A at 6 V) exceeds the buck's 2 A continuous rating and relies on the module's thermal shutdown.
5. **Signal loss.** No pulldown. Servo behavior with a floating signal is the retention path when the FC output stops. Characterize it.
6. **Bottom port sharing.** The V1 multispectral camera also flies on the bottom port with SERVO9 at 1000/2000. Swapping payloads means rewriting SERVO9_MIN/MAX. A stale 1000 µs low endpoint drives the latch servo past its lock stop.
7. **Parameter snapshot.** The saved WT file is work in progress and also carries `SERVO13_FUNCTION = 148`, presumed a leftover. Verify against the live vehicle.
8. **Print material.** All printed parts are PA6-CF (confirmed 2026-09-17), not the PETG-CF called out in the meetup build conventions. Dry the filament before printing. Heat set insert bores may creep if parts are stored humid. Filament brand and drying procedure not recorded.

# V2 Recommendations

- Mechanical lock on power loss: return spring or over center pin geometry.
- Enclosed electronics: buck in a printed pocket, trimmer locked, leads captive.
- Inrush NTC and local fuse on the 12 V input.
- Second structural path.
- Larger packages with a different loading and unloading mechanism (Erick).
- Measured mass, servo hold and stall current at 6 V, buck temperature.
- Keep FC only PWM or reintroduce an MCU for debounce, stall guard, and signal loss lock. Decide from the signal loss test.
- Per payload parameter file for bottom port hot swaps, or dedicate ports.
