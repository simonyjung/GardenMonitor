import board
import time
import busio
import adafruit_sht31d

from phue import Bridge
from gpiozero import MCP3008, RGBLED

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

# Philips hue
BRIDGE_IP = '192.168.2.43'
# 1, 2 Bedroom standing, 3 Study, 4 bedroom lamp
LIGHTS = [4, ]

"""
Get readings of up to 4 Capacitive soil moisture sensors, temperature (TMP36) using 
MCP3008 10bit Analog Digital Converter
"""


def get_humidity_percentage(value, min_value=MIN_HUMIDITY_VALUE, max_value=MAX_HUMIDITY_VALUE):
    """
    :param value: measured 8 bit value of analog signal
    :param min_value: calibrated value of probe when exposed to air
    :param max_value: calibrated value of probe when exposed to water
    :return: Percent humidity 0%-100%
    """
    value_range = min_value - max_value
    humidity_percentage = ((min_value - value) / value_range) * 100
    if humidity_percentage < 0:
        return 0
    elif humidity_percentage > 100:
        return 100
    else:
        return round(humidity_percentage, 1)


def get_temperature_c(voltage, round_digits=0 or None):
    """
    TMP36
    Temperature(Centigrade) = [(analog voltage in V) - .5] * 100
    :param voltage:
    :param round_digits:
    :return: Degrees C +-2
    """
    celsius = (voltage - 0.5) * 100
    if round_digits:
        return round(celsius, round_digits)
    elif round_digits == 0:
        return int(celsius)
    else:
        return celsius


def get_temperature_f(voltage, round_digits=0 or None):
    """
    TMP36
    Temperature(Fahrenheit) = ([(analog voltage in V) - .5] * 100 * ( 9 / 5)) + 32
    :param voltage:
    :param round_digits:
    :return:
    """
    celsius = get_temperature_c(voltage, round_digits=None)
    fahrenheit = (celsius * (9 / 5)) + 32
    if round_digits:
        return round(fahrenheit, round_digits)
    elif round_digits == 0:
        return int(fahrenheit)
    else:
        return fahrenheit


def main():
    # Soil moisture sensors
    moisture_sensors = {channel: MCP3008(channel=channel) for channel in MOISTURE_SENSOR_CHANNELS}
    # TMP36 Temperature Sensor
    temperature_sensor = MCP3008(channel=TEMPERATURE_SENSOR_CHANNEL)

    # SHT31D Temperature and Humidity sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_sht31d.SHT31D(i2c)

    # Hue
    bridge = Bridge(BRIDGE_IP)
    bridge.connect()
    lights = bridge.get_light_objects('id')

    while True:
        state_dict = dict()
        message = ""
        for channel in moisture_sensors:
            value = moisture_sensors[channel].value
            soil_moisture = get_humidity_percentage(value)
            state_dict['moisture_{}'.format(channel)] = {
                'voltage': moisture_sensors[channel].voltage,
                'value': value,
                'soil_moisture': soil_moisture
            }
            message += "| Plant {}: {}% ".format(channel, soil_moisture)

        temperature_voltage = temperature_sensor.voltage
        temperature = get_temperature_f(temperature_voltage, round_digits=1)
        state_dict['temperature'] = {
            'voltage': temperature_voltage,
            'fahrenheit': temperature,
        }
        temperature_message = "| TMP36 Temperature: {}F {}Fc".format(temperature,
                                                                     round(temperature - 2.5, 1))

        SHT31D_temp = round((sensor.temperature * (9 / 5)) + 32, 1)
        SHT31D_relative_humidity = int(sensor.relative_humidity)
        SHT_message = '| SHT31D Temperature: {}F {} Fc Humidity: {}% '.format(SHT31D_temp,
                                                                              round(SHT31D_temp - 7.9, 1),
                                                                            SHT31D_relative_humidity)
        print(temperature_message + SHT_message + message)
        time.sleep(.5)


if __name__ == '__main__':
    main()
