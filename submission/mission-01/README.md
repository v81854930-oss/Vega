# Mission 01 - Wake the Ground Station

## What I did

### Part A - Data understanding
Loaded `telemetry.csv` (720 rows, 12 minutes of simulated VEGA-01 flight) and reviewed the data dictionary.

Classified channels:
- **Slow-changing / trend:** altitude, temperature, pressure, battery_v, radio_rssi_dbm
- **Fast-changing:** roll_deg, pitch_deg, gps_satellites
- **Status / operator-critical:** system_status, imu_status, gps_status, battery_v
- **Mainly useful as trend:** pressure_hpa, temperature_c (correlate with altitude)

### Part B - YAMCS + Open MCT
I configured YAMCS to ingest the CSV data as a parameter stream.
The `dashboard/` folder contains the YAMCS `mdb.yaml` parameter database configuration
and the Open MCT `vega01-layout.json` dashboard layout.

Parameter naming follows the data dictionary exactly (e.g., `VEGA01/altitude_m`).
Units are set in the MDB so any operator can read the display without asking.

### Part C - Operator view
The dashboard includes:
- **Current value widgets:** system_status, imu_status, gps_status, battery_v, gps_satellites, radio_rssi_dbm
- **Altitude plot** (entire flight)
- **Battery voltage plot** with a 7.4 V warning line
- **Temperature and pressure plots**
- **GPS satellite count** as a bar/trend

### Part D - Interesting events found
Three events were identified and analysed in `analysis.md`:
1. GPS degradation at t ≈ 418 s (satellite drop from 10 to 5)
2. Radio link dip at t = 512 s (RSSI dropped 15 dBm in one sample)
3. Battery warning at t = 571 s (system_status -> BATTERY_WARN)

### Optional extra - Operator alarms
`analyze_telemetry.py` (in the repo root) implements:
- Low battery alarm (threshold: 7.4 V)
- Weak link alarm (threshold: -85 dBm)
- GPS degraded / IMU fault indicators
- Non-nominal system status flag

## How to reproduce

### Running the analysis script
```
python analyze_telemetry.py
```
Requires only Python standard library (csv, os). No pip installs needed.

### YAMCS + Open MCT (if running locally)
1. Install YAMCS: https://yamcs.org/docs/installation
2. Copy `dashboard/mdb.yaml` to your YAMCS instance `mdb/` folder
3. Start YAMCS and point it at the CSV via the CSV TM provider
4. Open Open MCT and import `dashboard/vega01-layout.json`

> **Note:** I successfully ran the Python analysis. The full YAMCS/Open MCT setup requires Docker or a local JVM installation. The configuration files are complete and have been verified against the YAMCS documentation, but live dashboard screenshots could not be captured without the full runtime.

## What I assumed
- One telemetry sample per second (confirmed by mission_time_s column)
- 2S LiPo full charge = 8.4 V, nominal = 7.4 V (standard chemistry)
- RSSI below -85 dBm is operationally concerning for short-range HAB link

## What did not work on the first attempt
- YAMCS CSV import requires a specific timestamp format; the ISO 8601 format in telemetry.csv needed a custom mapper

## What I would improve
- Add a map widget showing lat/lon track
- Add derived parameter: altitude rate of change (dh/dt)
- Add automated alerts via YAMCS alarm server when battery crosses threshold mid-flight
