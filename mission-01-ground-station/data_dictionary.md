# VEGA-01 Telemetry Dictionary

| Field | Unit | Meaning |
|---|---|---|
| `timestamp` | UTC | Timestamp of the telemetry sample |
| `mission_time_s` | s | Seconds since simulated launch |
| `altitude_m` | m | Estimated altitude |
| `latitude_deg` | deg | Latitude |
| `longitude_deg` | deg | Longitude |
| `temperature_c` | °C | Payload temperature |
| `pressure_hpa` | hPa | Atmospheric pressure |
| `battery_v` | V | Main battery voltage |
| `roll_deg` | deg | Roll |
| `pitch_deg` | deg | Pitch |
| `gps_satellites` | count | Satellites currently tracked |
| `imu_status` | text | Basic IMU health |
| `gps_status` | text | Basic GNSS fix state |
| `radio_rssi_dbm` | dBm | Received-signal-strength indication |
| `system_status` | text | Overall system state |

The data is simulated. A single sample is not automatically ground truth. Use the other channels to investigate unusual behaviour.
