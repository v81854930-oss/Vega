# Mission 02 - Bring a Sensor to Life

## Setup

**Sensor:** BMP280 (Bosch Sensortec)  
**Platform:** Raspberry Pi (or any Linux SBC with I2C) — no physical hardware required  
**Interface:** I2C at address 0x76 (SDO pulled to GND)  
**Language:** Python 3

## Requirements

```
pip install smbus2
```

## How to run

```
python firmware/bmp280_vega01.py
```

Expected output:
```
VEGA-01 SENSOR
-------------------------
Temperature : 27.42 C
Pressure    : 100812 Pa
Altitude    : 46.1 m
```

## Wiring

| BMP280 Pin | Connect to         | Notes                                |
|------------|--------------------|--------------------------------------|
| VCC        | 3.3 V              | Do NOT connect to 5 V                |
| GND        | GND                |                                      |
| SDA        | SDA (GPIO 2 RPi)   | I2C data                             |
| SCL        | SCL (GPIO 3 RPi)   | I2C clock                            |
| SDO        | GND                | Sets address to 0x76                 |
| CSB        | 3.3 V              | Selects I2C mode (not SPI)           |

See `hardware/connection-diagram.png` for the visual diagram.

## What I assumed

- No physical hardware available; code verified against BMP280 datasheet formulas
- Raspberry Pi I2C bus 1 (default for GPIO 2/3)
- Sea-level pressure for altitude formula: 101325 Pa (standard atmosphere)

## What I tried

- Read the BMP280 datasheet completely before writing code
- Implemented compensation formula directly from datasheet Appendix section 4.2.3
- Verified the formula numerically against known values from the datasheet example

## What did not work on first attempt

- Initial struct.unpack used wrong signed/unsigned mix for P2–P9 coefficients (all signed int16)
  Corrected after re-reading Table 17 of the datasheet

## What I would improve

- Add I2C error handling and retry logic (important for flight environment with vibration)
- Implement BMP280 filter coefficient to smooth out pressure spikes (register 0xF5 bits 4-2)
- Add configurable sea-level pressure reference for accurate altitude at any ground elevation
- Port to MicroPython for the actual flight MCU
