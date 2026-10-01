"""
analyze_telemetry.py
VEGA-01 Mission 01 - telemetry analysis script

Reads telemetry.csv and prints a summary of the data:
  - basic stats for each channel
  - any status changes or anomalies found

Usage:
    python analyze_telemetry.py
"""

import csv
import os

CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "mission-01-ground-station",
    "telemetry.csv",
)

LOW_BATTERY_THRESHOLD_V = 7.4   # 2S LiPo nominal; warn below this
RSSI_WARN_DBM = -85             # dBm; rough link-margin warning


def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def summary(rows):
    altitudes   = [float(r["altitude_m"])     for r in rows]
    batteries   = [float(r["battery_v"])      for r in rows]
    temps       = [float(r["temperature_c"])  for r in rows]
    pressures   = [float(r["pressure_hpa"])   for r in rows]
    rssies      = [float(r["radio_rssi_dbm"]) for r in rows]

    print("=" * 50)
    print("VEGA-01 Telemetry Summary")
    print("=" * 50)
    print("Rows        :", len(rows))
    print("Start       :", rows[0]["timestamp"])
    print("End         :", rows[-1]["timestamp"])
    print("Duration    :", rows[-1]["mission_time_s"], "s")
    print()
    print("Altitude    : {:.0f} m  ->  {:.0f} m".format(min(altitudes), max(altitudes)))
    print("Battery     : {:.3f} V  ->  {:.3f} V".format(min(batteries), max(batteries)))
    print("Temperature : {:.1f} C  ->  {:.1f} C".format(min(temps), max(temps)))
    print("Pressure    : {:.1f} hPa  ->  {:.1f} hPa".format(min(pressures), max(pressures)))
    print("Radio RSSI  : {:.0f} dBm  ->  {:.0f} dBm".format(min(rssies), max(rssies)))
    print()


def find_events(rows):
    print("Events and anomalies")
    print("-" * 50)
    prev = None
    events_found = 0

    for r in rows:
        if prev is None:
            prev = r
            continue

        t = r["mission_time_s"]

        # Status field transitions
        for field in ("system_status", "gps_status", "imu_status"):
            if r[field] != prev[field]:
                print("  t={}s  {:<18} {}  ->  {}".format(t, field, prev[field], r[field]))
                events_found += 1

        # Battery drop > 50 mV in a single sample
        try:
            dv = float(r["battery_v"]) - float(prev["battery_v"])
            if abs(dv) > 0.05:
                print("  t={}s  battery_v            {} V  ->  {} V  (delta={:+.3f})".format(
                    t, prev["battery_v"], r["battery_v"], dv))
                events_found += 1
        except ValueError:
            pass

        # GPS satellite count change >= 3
        try:
            ds = int(r["gps_satellites"]) - int(prev["gps_satellites"])
            if abs(ds) >= 3:
                print("  t={}s  gps_satellites       {}  ->  {}  (delta={:+d})".format(
                    t, prev["gps_satellites"], r["gps_satellites"], ds))
                events_found += 1
        except ValueError:
            pass

        # RSSI jump > 5 dBm
        try:
            dr = float(r["radio_rssi_dbm"]) - float(prev["radio_rssi_dbm"])
            if abs(dr) > 5:
                print("  t={}s  radio_rssi_dbm       {} dBm  ->  {} dBm  (delta={:+.0f})".format(
                    t, prev["radio_rssi_dbm"], r["radio_rssi_dbm"], dr))
                events_found += 1
        except ValueError:
            pass

        prev = r

    if events_found == 0:
        print("  No anomalies detected.")
    print()


def operator_alarms(rows):
    """Print operator-relevant alarms based on the final telemetry row."""
    last = rows[-1]
    print("Operator alarms (end of dataset)")
    print("-" * 50)
    alarms = 0

    batt = float(last["battery_v"])
    if batt < LOW_BATTERY_THRESHOLD_V:
        print("  [!] LOW BATTERY   {:.3f} V  (threshold {:.1f} V)".format(batt, LOW_BATTERY_THRESHOLD_V))
        alarms += 1

    rssi = float(last["radio_rssi_dbm"])
    if rssi < RSSI_WARN_DBM:
        print("  [!] WEAK LINK     {} dBm  (threshold {} dBm)".format(rssi, RSSI_WARN_DBM))
        alarms += 1

    if last["gps_status"] not in ("LOCK", "FIX"):
        print("  [!] GPS DEGRADED  status =", last["gps_status"])
        alarms += 1

    if last["imu_status"] != "OK":
        print("  [!] IMU FAULT     status =", last["imu_status"])
        alarms += 1

    if last["system_status"] not in ("NOMINAL",):
        print("  [!] SYSTEM        status =", last["system_status"])
        alarms += 1

    if alarms == 0:
        print("  All parameters nominal.")
    print()


def main():
    rows = load(CSV_PATH)
    summary(rows)
    find_events(rows)
    operator_alarms(rows)


if __name__ == "__main__":
    main()
