# VEGA-01 - Mission Brief

VEGA-01 is a high-altitude balloon payload carrying scientific instruments and a small avionics stack.

During flight, the avionics system needs to collect measurements, keep track of vehicle health, transmit useful telemetry, and give the ground team enough information to understand what is happening.

For this recruitment challenge, the real system is simplified so that you can focus on engineering decisions rather than solving the whole aerospace problem at once.

## Simplified system

```text
                       2S LiPo
                          |
                    +-----+-----+
                    |   Power   |
                    | Regulation|
                    +-----+-----+
                          | 3.3 V
                    +-----+-----+
                    | Flight MCU|
                    +--+--+--+--+
                       |  |  |
                 I2C --+  |  +-- UART -- GNSS
                       |  |
                   SPI |  |
                       |  |
                       +--+--> IMU

                    MCU ------- Radio
                     |
                     +--------- ADC -- Battery Monitor
```

## Available devices

| Device | Interface | Simplified notes |
|---|---|---|
| Flight MCU | - | 3.3 V logic |
| Pressure sensor | I2C | 3.3 V |
| IMU | SPI | 3.3 V |
| GNSS receiver | UART | 3.3 V logic assumed |
| Radio | UART/SPI | RF section out of scope |
| Battery monitor | ADC | MCU ADC range 0-3.3 V |
| Main battery | - | 2S LiPo, 7.4 V nominal, 8.4 V full |

## Recruitment missions

The avionics challenge is split into two small missions.

### Mission 01 - Wake the Ground Station

Work with the supplied telemetry data and starter material for YAMCS and Open MCT.

The goal is to turn raw flight data into a ground-station view that an operator can actually use.

You will work with:

- telemetry
- data interpretation
- ground-station software
- plots and status information
- basic fault investigation

### Mission 02 - Bring a Sensor to Life

Work with a BMP280 pressure and temperature sensor and a suitable microcontroller.

The goal is to figure out how the sensor should be connected, how the controller communicates with it, and how to check that the measurements make sense.

You will work with:

- datasheets
- power and wiring
- I2C
- basic embedded code
- hardware troubleshooting

You do not need to already know these things. The task is designed so that the documentation is part of the problem.

## Telemetry

The ground team cares about mission time, position, altitude, temperature, pressure, battery voltage, attitude, GPS health, IMU health, and radio-link quality.

The exact packet format is intentionally not fixed in advance.

## What we are looking for

This is a recruitment challenge, so the final result is only part of what we care about.

We want to see how you approach something you do not already know:

**learn -> build -> test -> break -> debug -> explain**

Using documentation, search, compilers, CAD tools, and AI is allowed.

What matters is that you understand what you submit and can explain the decisions you made.

## Scope

This is a recruitment challenge, not a flight-qualification review. You are not expected to solve full thermal qualification, EMC qualification, RF regulatory compliance, mechanical analysis, radiation effects, or complete flight redundancy.

The electronics task also does not require PCB design, soldering, or a physical sensor. A simulation, schematic, or software-only demonstration is acceptable where the task allows it.
