BMP280 measures pressure and temperature from which values you can calculate altitude using a standard formula
I chose I2C since it requires only two lines SDA and SCL besides power and ground.
Connections between BMP280 and ESP32:
| BMP280 pin | ESP32 pin |
|------------|-----------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |
| SDO | GND (configures device address to 0x76) |
| CSB | VCC (configures I2C interface) |

(*USED AI FOR BETTER PRESENTATION OF PINS)

Register 0xD0 is Chip ID register read it returns 0x60 anytime read
It is the very first value that code will check to ensure that sensor exists and works properly anything other than 0x60 means problem prior to reading any values from the sensor
In case of not found by the sensor 
Incorrect I2C address
The sensor can have one of two possible addresses either 0x76 or 0x77, depending on the state of SDO either grounded (0x76) or powered (0x77). If the code uses 0x77, but the sensor is set to 0x76 the device won't be found should run an I2C scanner to find out what address is actually shown by the sensor.

Checking for correct readings
The standard atmospheric pressure at the sea level is 101325 Pa. The value of 97600 Pa can be expected at 300 meters altitude (which is appropriate for Hyderabad). Temperature of about 27 C also makes sense for this location.

Opening the weather app and check current temperature and pressure near my location.
The script had a Unicode encoding error on Windows because of a special character fixed it by switching to plain ASCII and setting coding to utf-8.


On real hardware I would add continuous logging to a file and a check that flags if the sensor stops responding mid-flight.
