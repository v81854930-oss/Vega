"""
bmp280_vega01.py
VEGA-01 Mission 02 - BMP280 sensor reader

Platform : Raspberry Pi (or any Linux SBC with I2C)
Library  : smbus2   (pip install smbus2)

Wiring (I2C mode):
  BMP280 VCC  -> 3.3 V
  BMP280 GND  -> GND
  BMP280 SDA  -> SDA (GPIO 2 on RPi)
  BMP280 SCL  -> SCL (GPIO 3 on RPi)
  BMP280 SDO  -> GND  (sets I2C address to 0x76)
  BMP280 CSB  -> 3.3 V (selects I2C, not SPI)

Usage:
  python bmp280_vega01.py
"""

import struct
import time
import smbus2


BMP280_ADDR = 0x76


REG_ID          = 0xD0
REG_RESET       = 0xE0
REG_STATUS      = 0xF3
REG_CTRL_MEAS   = 0xF4
REG_CONFIG      = 0xF5
REG_PRESS_MSB   = 0xF7   
REG_CALIB_START = 0x88   


def read_calibration(bus):
    """
    Read the 24 calibration bytes from 0x88-0x9F.
    BMP280 datasheet section 4.2.2, Table 17.
    """
    raw = bus.read_i2c_block_data(BMP280_ADDR, REG_CALIB_START, 24)

  
    dig_T1 = struct.unpack_from("<H", bytes(raw), 0)[0]   
    dig_T2 = struct.unpack_from("<h", bytes(raw), 2)[0]  
    dig_T3 = struct.unpack_from("<h", bytes(raw), 4)[0]

    dig_P1 = struct.unpack_from("<H", bytes(raw), 6)[0]
    dig_P2 = struct.unpack_from("<h", bytes(raw), 8)[0]
    dig_P3 = struct.unpack_from("<h", bytes(raw), 10)[0]
    dig_P4 = struct.unpack_from("<h", bytes(raw), 12)[0]
    dig_P5 = struct.unpack_from("<h", bytes(raw), 14)[0]
    dig_P6 = struct.unpack_from("<h", bytes(raw), 16)[0]
    dig_P7 = struct.unpack_from("<h", bytes(raw), 18)[0]
    dig_P8 = struct.unpack_from("<h", bytes(raw), 20)[0]
    dig_P9 = struct.unpack_from("<h", bytes(raw), 22)[0]

    return (dig_T1, dig_T2, dig_T3,
            dig_P1, dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9)


def configure(bus):
    """
    Set oversampling and operating mode.
    ctrl_meas register (0xF4):
      bits 7-5 : osrs_t = 001 (x1 temperature oversampling)
      bits 4-2 : osrs_p = 001 (x1 pressure oversampling)
      bits 1-0 : mode   = 11  (normal / continuous mode)
    See BMP280 datasheet section 4.3.4.
    """
    ctrl_meas = (0b001 << 5) | (0b001 << 2) | 0b11
    bus.write_byte_data(BMP280_ADDR, REG_CTRL_MEAS, ctrl_meas)

  
    bus.write_byte_data(BMP280_ADDR, REG_CONFIG, 0x00)


def read_raw(bus):
    """
    Burst-read 6 bytes: press_msb, press_lsb, press_xlsb,
                        temp_msb,  temp_lsb,  temp_xlsb
    BMP280 datasheet section 4.2.2.
    """
    data = bus.read_i2c_block_data(BMP280_ADDR, REG_PRESS_MSB, 6)

    raw_press = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    raw_temp  = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    return raw_press, raw_temp


def compensate_temperature(raw_temp, calib):
    """
    BMP280 compensation formula from datasheet Appendix, section 4.2.3.
    Returns (temperature_c, t_fine) where t_fine is used by pressure comp.
    """
    dig_T1, dig_T2, dig_T3 = calib[:3]

    var1 = ((raw_temp / 16384.0) - (dig_T1 / 1024.0)) * dig_T2
    var2 = (((raw_temp / 131072.0) - (dig_T1 / 8192.0)) ** 2) * dig_T3
    t_fine = int(var1 + var2)
    temperature = (var1 + var2) / 5120.0
    return temperature, t_fine


def compensate_pressure(raw_press, t_fine, calib):
    """
    BMP280 compensation formula from datasheet Appendix, section 4.2.3.
    Returns pressure in Pa.
    """
    _, _, _, dig_P1, dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9 = calib

    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * dig_P6 / 32768.0
    var2 = var2 + var1 * dig_P5 * 2.0
    var2 = var2 / 4.0 + dig_P4 * 65536.0
    var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * dig_P1

    if var1 == 0:
        return 0 

    pressure = 1048576.0 - raw_press
    pressure = (pressure - var2 / 4096.0) * 6250.0 / var1
    var1 = dig_P9 * pressure * pressure / 2147483648.0
    var2 = pressure * dig_P8 / 32768.0
    pressure = pressure + (var1 + var2 + dig_P7) / 16.0
    return pressure


def altitude_from_pressure(pressure_pa, sea_level_pa=101325.0):
    """
    Hypsometric formula for altitude estimate.
    Reasonable for low altitudes without temperature correction.
    """
    import math
    return 44330.0 * (1.0 - (pressure_pa / sea_level_pa) ** (1.0 / 5.255))


def main():
    bus = smbus2.SMBus(1)

   
    chip_id = bus.read_byte_data(BMP280_ADDR, REG_ID)
    if chip_id != 0x60:
        print("BMP280: NOT FOUND (chip_id = 0x{:02X}, expected 0x60)".format(chip_id))
        return

    calib = read_calibration(bus)
    configure(bus)

   
    time.sleep(0.1)

    print("VEGA-01 SENSOR")
    print("-" * 25)

    for _ in range(10):
        raw_press, raw_temp = read_raw(bus)
        temperature, t_fine = compensate_temperature(raw_temp, calib)
        pressure_pa = compensate_pressure(raw_press, t_fine, calib)
        altitude_m = altitude_from_pressure(pressure_pa)

        print("Temperature : {:.2f} C".format(temperature))
        print("Pressure    : {:.0f} Pa".format(pressure_pa))
        print("Altitude    : {:.1f} m".format(altitude_m))
        print()
        time.sleep(1.0)


if __name__ == "__main__":
    main()
