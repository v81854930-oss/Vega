# Mission 02 - Analysis

## Sensor overview

The **BMP280** measures:
- **Temperature** (range: -40 to +85 °C, accuracy ±1.0 °C typical)
- **Pressure** (range: 300–1100 hPa, accuracy ±1 hPa relative)
- From pressure, **altitude** can be derived using the hypsometric formula

Manufacturer: Bosch Sensortec  
Datasheet: BST-BMP280-DS001-19 (available at bosch-sensortec.com)

---

## Interface

The BMP280 supports both **I2C** and **SPI**.  
I used **I2C** for this implementation because it requires fewer wires (2 vs 4)
and the VEGA-01 flight MCU already has a shared I2C bus for the pressure sensor.

**I2C address:**
- `0x76` when SDO pin is pulled LOW (to GND)
- `0x77` when SDO pin is pulled HIGH (to VCC)

Communication sequence:
1. Write configuration to `ctrl_meas` register (0xF4): set oversampling + normal mode
2. Read 6-byte burst from registers 0xF7–0xFC (raw pressure + temperature)
3. Apply two-stage compensation formula from datasheet Appendix section 4.2.3 using 12 calibration coefficients stored in the sensor's non-volatile memory at 0x88–0x9F

---

## Important hardware detail

### What is it?

**Chip ID register (0xD0)** — the BMP280 stores its chip identifier at this register.  
The expected value for BMP280 is `0x60`.

### Why does it matter?

The BMP280, BME280, and BMP180 look similar on the I2C bus and can share the same address.
Before attempting to read calibration data or configure the sensor, the code reads register 0xD0
and checks that it returns `0x60`. If the wrong value is returned (e.g., `0x60` for BME280 or `0x55` for BMP180),
the calibration byte layout and compensation formulas are different, and the readings will be wrong.
If the register returns `0x00`, the device is not responding at all.

### Where did I find it?

BMP280 datasheet section 4.2, Table 16 — "Memory map", row for address `0xD0`.

---

## Debugging

If the serial output shows `BMP280: NOT FOUND`, I would check these three things:

### 1. I2C address mismatch
**What:** The code targets `0x76` but the sensor may be wired with SDO high, making its address `0x77`.  
**Why:** SDO controls the LSB of the I2C address. If SDO is floating or pulled high, the wrong address is used.  
**How:** Run `i2cdetect -y 1` on Raspberry Pi to scan the bus and see which address responds. Change the address in code to match.

### 2. Wiring error — SDA/SCL swapped or loose connection
**What:** The I2C data and clock lines may be swapped, or a jumper wire is not fully seated.  
**Why:** I2C requires separate data (SDA) and clock (SCL) lines. Swapping them means no valid I2C frames are ever formed.  
**How:** Use a multimeter to confirm continuity from the MCU SDA/SCL pins to the correct BMP280 pins. Check with an oscilloscope or logic analyser that SCL shows a clock signal during a transaction.

### 3. CSB pin not pulled to VCC (sensor stuck in SPI mode)
**What:** The BMP280's CSB pin selects the interface. If CSB is low or floating, the sensor may be in SPI mode and will ignore I2C.  
**Why:** Even if all other wiring is correct, a floating CSB keeps the sensor in an indeterminate state.  
**How:** Use a multimeter to confirm CSB reads close to VCC (3.3 V). If not, add a 4.7 kΩ pull-up resistor from CSB to 3.3 V.

---

## Verification

Given sensor output:
```
Temperature : 26.8 °C
Pressure    : 100923 Pa
```

### Method 1 — Cross-reference with known atmospheric pressure
Standard sea-level pressure is 101325 Pa. At a typical indoor location at ~50–100 m elevation,
expected pressure is ~100800–101200 Pa. The reported 100923 Pa falls in this range, which is physically plausible.
I would compare against a local weather station barometric pressure reading (available from weather apps or airport METAR data).

### Method 2 — Cross-reference temperature with another source
26.8 °C is a plausible room temperature. I would compare against a calibrated digital thermometer placed
next to the sensor. If within ±2 °C, the sensor is working correctly.
A third option is applying the altitude formula: 100923 Pa implies ~50 m altitude above sea level.
If the actual location is known, this altitude check independently validates the pressure reading.

---

## What I learned

Before this task I had not directly read a sensor register map or implemented the BMP280 compensation
formula from scratch. The most useful thing I learned was how the 12 factory calibration coefficients
are mixed into the raw ADC output through a two-stage formula — without them, the raw pressure ADC
value alone is meaningless. Reading the datasheet appendix section to understand this was
the key step, not just calling a library.
