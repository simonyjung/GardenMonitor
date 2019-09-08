import board
import time
#import Adafruit_DHT
import busio
import adafruit_sht31d

from gpiozero import MCP3008, RGBLED

# Base Calibration
MIN_HUMIDITY_VALUE = .860
MAX_HUMIDITY_VALUE = .483
MOISTURE_SENSOR_CHANNELS = [0]  # 0, 1, 2, 3
SENSOR_CALIBRATIONS = {
    0: {'min': .860, 'max': .483},
    1: {'min': .860, 'max': .483},
    2: {'min': .860, 'max': .483},
    3: {'min': .860, 'max': .483},
}
TEMPERATURE_SENSOR_CHANNEL = 4  # 4

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


def get_temperature_c(voltage, round_digits=0):
    """
    TMP36
    Temperature(Centigrade) = [(analog voltage in V) - .5] * 100
    -.02 V calibration at 22C
    :param voltage:
    :return: Degrees C +-2
    """
    celsius = (voltage - 0.5) * 100
    if round_digits or round_digits == 0:
        return round(celsius, round_digits)
    else:
        return celsius


def get_temperature_f(voltage, round_digits=0):
    """
    TMP36
    Temperature(Fahrenheit) = ([(analog voltage in V) - .5] * 100 * ( 9 / 5)) + 32
    :param voltage:
    :param round_digits:
    :return:
    """
    celsius = get_temperature_c(voltage, round_digits=None)
    fahrenheit = (celsius * (9 / 5)) + 32
    if round_digits or round_digits == 0:
        return round(fahrenheit, round_digits)
    else:
        return fahrenheit


def main():
    moisture_sensors = {channel: MCP3008(channel=channel) for channel in MOISTURE_SENSOR_CHANNELS}
    temperature_sensor = MCP3008(channel=TEMPERATURE_SENSOR_CHANNEL)
    temperature_sensor_1 = MCP3008(channel=5)

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_sht31d.SHT31D(i2c)

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
            message += "Plant {}: {}% ".format(channel, soil_moisture)

        temperature_voltage = temperature_sensor.voltage
        temperature = get_temperature_f(temperature_voltage)
        temperature_voltage_1 = temperature_sensor_1.voltage
        temperature_1 = get_temperature_f(temperature_voltage_1)
        state_dict['temperature'] = {
            'voltage': temperature_voltage,
            'fahrenheit': temperature,
        }
        temperature_message = "Temperature: {}F ".format(temperature)
        #d_humidity, d_temperature = Adafruit_DHT.read_retry(11, 4)
        #dht_message = "DHT T: {}, H: {} ".format(d_temperature, d_humidity)

        print('Humidity: {0}%'.format(sensor.relative_humidity))
        print('Temperature: {0}F'.format((sensor.temperature * (9 / 5)) + 32))

        print(temperature_message + message)
        time.sleep(.5)


if __name__ == '__main__':
    main()
