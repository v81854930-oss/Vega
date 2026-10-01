# VEGA-01 Mission 01 - Telemetry Analysis

## Dataset overview

| Item | Value |
|---|---|
| Rows | 720 |
| Start | 2026-09-25T10:00:00Z |
| End | 2026-09-25T10:11:59Z |
| Duration | 719 s (~12 minutes) |
| Altitude range | 120 m → 3,227 m |
| Battery range | 6.99 V → 8.22 V |
| Temperature range | ~5.2 °C → 26.8 °C |
| Pressure range | ~689 hPa → 996 hPa |
| Radio RSSI range | -88 dBm → -73 dBm |

---

## Event 1 — GPS degradation at t ≈ 418 s

### What changed?

At **t = 418 s**, `gps_status` transitioned from `LOCK` to `DEGRADED`
and `gps_satellites` dropped from **10 → 5**.  
The fix was partially restored at t = 421 s (status back to LOCK, 5 satellites),
then another DEGRADED event occurred at t = 426 s before full recovery at t = 429 s (10 satellites).

### Why did it catch my attention?

A halving of the tracked-satellite count in a single telemetry sample is unusual for a clean sky view at altitude.  
The status field independently corroborated the satellite drop, making this a two-channel alarm rather than a single noisy field.  
The double dip (418–421 s, then 426–429 s) suggests something intermittent rather than a one-time glitch.

### Two possible explanations

1. **Multipath or obscuration from the balloon envelope / payload structure** — as the balloon rotates and pitches, the GNSS antenna briefly points toward the balloon canopy. This blocks part of the sky, causing satellites to drop out. The oscillation fits this: balloon rotates, antenna dips below the canopy shadow, recovers, dips again.

2. **Interference from the radio transmitter or IMU SPI bus** — a burst of RF or EMI at that moment could cause the GNSS receiver to lose lock on weaker satellites temporarily. High-altitude balloons operate in a congested ISM environment and short bursts of interference are common near the transmit schedule of the radio.

### What I would check next

- **Attitude data (roll, pitch)** around t = 418–429 s — if roll/pitch shows a rotation event coinciding with the satellite drop, that points to antenna obscuration.
- **Radio transmission schedule** — if the radio fires a burst every N seconds and the drops correlate, EMI is likely.
- **Satellite PRN logs** (if available) — persistent loss of the same satellite IDs across events suggests geometry, not interference.
- **GNSS receiver power rail** — a voltage droop on the 3.3 V rail could momentarily reset the receiver. Cross-check battery_v at those timestamps.

---

## Event 2 — Radio link dip at t = 512 s

### What changed?

At **t = 512 s**, `system_status` changed from `NOMINAL` to `LINK_MARGIN_LOW`
and `radio_rssi_dbm` jumped from **-71 → -86 dBm** (a 15 dBm drop in one sample).  
Both recovered at t = 521 s.

### Why did it catch my attention?

A 15 dBm step drop is extremely large for a link that had been slowly degrading by 1 dBm per ~100 m of altitude gain. A gradual fade follows range; a sudden step suggests an attitude-induced null in the antenna pattern or brief RF blockage.

### Two possible explanations

1. **Antenna pattern null** — the balloon rotated so that the payload antenna briefly pointed its null toward the ground station. A dipole or patch antenna can easily show a 15+ dB difference between bore-sight and null.
2. **Ground-station antenna tracking error** — if the ground station uses a directional antenna, a pointing lag could create a momentary deep fade.

### What I would check next

- **Attitude at t = 512 s** — a coincident roll/pitch spike would confirm antenna-null hypothesis.
- **Link budget** — check expected RSSI vs range at that altitude to see if -86 dBm is within the receiver sensitivity margin.
- **Ground station azimuth/elevation logs** — tracking error would appear here.

---

## Event 3 — Battery warning at t = 571 s

### What changed?

At **t = 571 s**, `system_status` transitions to `BATTERY_WARN`.  
Inspecting battery_v at the end of the dataset shows it at **~6.99 V** (below the 7.4 V 2S LiPo nominal).

### Why did it catch my attention?

The battery started at 8.22 V (near full for a 2S LiPo, fully charged ≈ 8.4 V). A steady discharge is expected with altitude/time, but the BATTERY_WARN trigger is the flight computer flagging that it has crossed an internal threshold. This is the most operationally critical event in the dataset.

### Two possible explanations

1. **Normal discharge** — the 2S pack simply depleted over 570 s of flight with radio, MCU, and sensor loads. At altitude, lower temperatures can also reduce effective capacity, causing the voltage to sag faster than at room temperature.
2. **Elevated current draw from thermal effects** — as temperature dropped with altitude, the battery's internal resistance increased, causing a larger voltage sag under the same current, triggering the threshold earlier than expected.

### What I would check next

- **Battery current sensor** (if fitted) — to distinguish high-drain vs low-capacity scenarios.
- **Temperature vs battery_v correlation** — plot both on the same axis; if voltage sag tracks temperature drop, thermal derating is the cause.
- **Mission power budget** — compare projected discharge rate at launch vs observed to identify whether load was higher than expected.
