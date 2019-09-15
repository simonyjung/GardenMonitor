import adafruit_sht31d
import board
import busio
import time

from phue import Bridge
from gpiozero import MCP3008

# Base Calibration
MIN_HUMIDITY_VALUE = .860
MAX_HUMIDITY_VALUE = .483
MOISTURE_SENSOR_CHANNELS = [0]  # 0, 1, 2, 3
SENSOR_CALIBRATIONS = {
    0: {'min': .860, 'max': .483},
    1: {'min': .9648, 'max': .555},
    2: {'min': .860, 'max': .483},
    3: {'min': .860, 'max': .483},
}
TEMPERATURE_SENSOR_CHANNEL = 6  # 6
SHT31D_TEMPERATURE_CALIBRATION = -7.9  # Indoor: -7.9F, Outdoors in container:
SHT31D_HUMIDITY_CALIBRATION = None
TMP36_TEMPERATURE_CALIBRATION = -2.5  # Indoor: -2.5F, Outdoor in container


# Philips hue
BRIDGE_IP = '192.168.2.43'
# 1, 2 Bedroom standing, 3 Study, 4 bedroom lamp
LIGHTS = [4, ]

DRY_THRESHOLD = 10
"""
Get readings of up to 4 Capacitive soil moisture sensors, 
temperature and humidity (SHT31D)
redundant temperature (TMP36)
"""


def main():
    # Soil moisture sensors
    moisture_sensors = {channel: MCP3008(channel=channel) for channel in MOISTURE_SENSOR_CHANNELS}
    # TMP36 Temperature Sensor
    tmp36_sensor = MCP3008(channel=TEMPERATURE_SENSOR_CHANNEL)

    # SHT31D Temperature and Humidity sensor
    sht31d_sensor = adafruit_sht31d.SHT31D(busio.I2C(board.SCL, board.SDA))

    # Hue
    bridge = Bridge(BRIDGE_IP)
    bridge.connect()
    lights = bridge.get_light_objects('id')


if __name__ == '__main__':
    main()
