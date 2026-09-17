# Quiver Multispectral Camera Mount V1 (MAPIR Survey3 RGN)

**Status:** flight-tested (prototype, see Remarks for unmet criteria)
**Target port(s):** bottom (as flown), side 1 (design intent)
**ICD version:** 1.0-draft
**Champion:** Erick Perdomo (errrks)
**Discussion:** https://dao.arrowair.com/t/bounty-v1-quiver-multispectral-camera-payload/156

# Status

`Valid, as built at Meetup 2026, flight tested 2026-08-13 (approximate). Information note for project-quiver T-11 (issue #257).`

Built by Erick Perdomo and Alperen with a camera supplied by Thomas. This README is the V1 information note. It records the hardware that flew, the flight controller configuration, the tests run and not run, and what V2 should change. The Meetup 2026 build pack is the design intent and is superseded here where they differ.

# Project Description

Fixed nadir mount for the MAPIR Survey3 RGN multispectral camera. The camera hangs in a printed saddle on four silicone damper balls under the JMRRC quick release clip plate. An LM2596 buck steps 12V_PL down for the camera's USB power input, and the flight controller drives the MAPIR HDMI PWM trigger cable directly over the port's PWM auxiliary channel. No microcontroller, no enclosure, no downlink. Images come off the microSD after flight.

Origin: DAO bounty 156, folded into an in-house meetup build charged to QGB-05. Bounty criteria (fit, stable 5 V power, trigger on each FC pulse, GPS tag, vibration isolation, IP5X dust protection) remain the evaluation baseline.

| | |
|---|---|
| Mass | Not weighed (design estimate ~300 g, built unit lighter) |
| Power | 12V_PL through an LM2596 buck at 5.3 V, ~2 W capturing |
| Data | PWM (FMU_CH1 as flown) |
| Port | bottom as flown, side 1 in design |

# Methodology

1. Parts: MAPIR Survey3 RGN (Thomas's unit), MAPIR HDMI PWM trigger cable, MAPIR USB Power+FPV cable, Zovfam LM2596 buck (Amazon B08BFKKDGD), silicone damper balls from workshop stock, Molex 204523-1201 housing with 79758-1149 leads, JMRRC male clip plate, Attach Interface PCB V1.4 payload side.
2. Printed body, damper plates, and camera saddle in PA6-CF. CAD in `CAD/`.
3. Lens swapped from the wide lens to the narrow lens: unscrew the lens retaining ring, exchange the lens body, refocus by test shots on a distant target.
4. Buck trimmed to 5.3 V at its output, unloaded, before the camera was connected.
5. Flight controller output freed from the GPIO mask, PWM verified on the bench with Mission Planner DO_SET_SERVO at 1000 and 2000 µs.
6. Flight on the bottom port with RC channel 9 triggering. Internal battery removed.

# Results and Deliverables

## Camera

- MAPIR Survey3, classic body, RGN filter, narrow lens (41° HFOV) after the swap.
- Capture mode single photo, RAW on (RAW plus JPG). MAPIR manual v3: RAW is only available in single capture mode.
- Internal battery out. The camera therefore reboots on every 12V_PL cycle.
- Firmware version, SD card model, and cable source not recorded.

## Mount

- JMRRC male clip plate with the Attach Interface PCB V1.4 payload side in its recess.
- PA6-CF body on the plate carries the buck on top and a damper plate below. A second damper plate on the camera saddle. Saddle clamps the camera body with one M3 socket head.
- Four blue silicone damper balls between the plates, hot glued. Source and durometer unknown (workshop stock).
- No enclosure, gasket, or SD door. No outboard arm (not needed on the bottom port). Single load path through the clip plate.
- Zip ties for lead strain relief.

## Electrical

Power chain: 12V_PL (J1 pin 10) → LM2596 buck IN+ → 5.3 V OUT → MAPIR USB Power+FPV cable spliced to the buck output.

Buck listing specs (2026-09-17): input 3 to 40 V, output 1.3 to 35 V, 2 A continuous, 3 A peak with heatsink, 92% peak efficiency, 65 kHz, 30 mV ripple, thermal shutdown and current limit.

The MAPIR manual v3 states "wall chargers marked output 5V 1A." It does not mention 5.3 V. The 5.3 V setting was measured at the buck output unloaded and worked. The camera end under load was not measured. USB device limit is 5.25 V, so measure the camera end and trim down if needed.

Harness on Attach Interface PCB J1:

| J1 pin | Signal | Connection |
|---|---|---|
| 8 | GND | Buck IN−, trigger cable ground |
| 10 | +12V (12V_PL) | Buck IN+ |
| 12 | FMU_CH1 | MAPIR trigger cable signal lead |

No inrush limiter, no fuse, no filtering.

## Trigger

FMU_CH1 servo PWM → J1 pin 12 → MAPIR HDMI PWM trigger cable → camera HDMI port. Trigger cable power lead unused.

MAPIR manual v3 PWM levels:

| Pulse | Camera action |
|---|---|
| 1000 µs | Neutral, camera does nothing |
| 2000 µs momentary | Capture |
| 1500 µs momentary | Enter media transfer mode, second pulse exits |

As flown the camera captured on every 2000 µs pulse from the 1000 µs idle.

**1500 µs hazard:** an output resting at trim, a three position switch center, or a slow slider puts the camera into media transfer mode and stops captures until another 1500 µs pulse. Use a two position switch and keep every failsafe path away from 1500.

## Flight controller configuration

Same channel mapping and GPIO mask procedure as the latch README (project-quiver config guide section 11.6). Camera values as flown (from recollection of a rewrite over the latch snapshot, verify on the vehicle):

```
SERVO_GPIO_MASK   12016     ; outputs 9, 15, 16 freed for PWM
SERVO9_FUNCTION   148       ; RCIN9Scaled, RC channel 9
SERVO9_MIN        1000      ; neutral
SERVO9_MAX        2000      ; capture
RELAY6_FUNCTION   1         ; 12V_PL rail (FMU_CH4, pin 53)
RELAY6_PIN        53
RELAY6_DEFAULT    0
```

Bench alternative: `SERVO16_FUNCTION = 0`, MIN/MAX 1000/2000, Servo 16 row High on the Mission Planner Servo/Relay page (side 2 port).

Not used: ArduPilot camera driver (CAM1 is already the SIYI at type 4). Mission triggering by distance is a V2 item and needs a second camera instance.

## Test record

| Test | Result |
|---|---|
| Bench trigger from Mission Planner, output 16 | Captured on every pulse, 2026-08-12 |
| Flight, bottom port, RC channel 9 | Captured on every trigger, RAW plus JPG |
| 12V_PL cycle via Relay 6 | Camera rebooted each cycle, recovered, accepted triggers |
| GPS geotag in EXIF (bounty GPS Tag) | Not checked. Camera top face points into the belly, no sky view |
| Camera end voltage under load (bounty Power) | Not measured |
| Mass (350 g budget) | Not weighed |
| IP5X (bounty Dust Protection) | Not built |

Photos and video: Arrow Discord and Twitter, meetup week of 2026-08-10.

## Deliverables

- `CAD/` STEP and STL (CERN OHL-S v2)
- This README (CC BY 4.0)
- Flight controller configuration section 11.6 in project-quiver

# Remarks

1. **Geotag unverified and probably absent.** On the bottom port the built in GPS antenna faces the 2 mm aluminum lower plate. Pull the SD and check EXIF. V2 restores sky view on a side port or feeds NMEA from the vehicle.
2. **Power criterion open.** 5.3 V set unloaded at the buck, not locked, camera end not measured. The manual's stated requirement is 5 V 1 A.
3. **1500 µs media transfer mode.** Any output parked at trim stops captures. Guard in the RC setup and in any future camera driver integration.
4. **Battery out means a reboot on every rail cycle.** Camera boot time before it accepts triggers is unrecorded. Measure and add to the ground procedure. Battery in (the original decision) survives rail cycles but needs the charge current and thermal check.
5. **Capture interval.** RAW plus JPG limits capture to roughly one per 2.5 to 3 s. Faster mission triggering drops frames silently.
6. **No enclosure, no inrush, no fuse.** IP5X criterion not attempted.
7. **Dampers.** Unknown durometer, hot glued. Vibration isolation criterion asks for a documented spec.
8. **Bottom port sharing with the latch.** SERVO9 endpoints differ (1000/2000 vs 1315/1750) and both use RC channel 9. Rewrite at every swap.
9. **Lens swap.** Filter position during the swap not recorded. Confirm with Thomas whether the RGN filter is lens mounted or sensor mounted on this unit.
10. **Print material.** All printed parts are PA6-CF (confirmed 2026-09-17), not the PETG-CF called out in the meetup build conventions. Dry the filament before printing. Heat set insert bores may creep if parts are stored humid. Filament brand and drying procedure not recorded.

# V2 Recommendations

- Side port mount with a plain PETG GPS window per the build pack, or vehicle NMEA to the camera.
- Gasketed enclosure with SD door for IP5X.
- Second ArduPilot camera instance (servo type) for mission triggering, with 1500 µs excluded from every path.
- Buck enclosure, trimmer lock, inrush NTC, local fuse.
- Measured mass, camera end voltage under load, boot time after rail power.
- Decide battery in or out. Record the damper spec.
