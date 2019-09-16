import adafruit_sht31d
import board
import busio
import django
import os
import smbus
import time

from gpiozero import MCP3008
from pi.sensor_calibrations import outdoor_calibrations as calibrations

os.environ['DJANGO_SETTINGS_MODULE'] = 'gardenmonitor.settings'
django.setup()

from environment import models as environment_models

TEMPERATURE_SENSOR_CHANNEL = 6

"""
Log environment values

Run every 5 minutes using cron

*/5 * * * * cd /home/pi/Code/GardenMonitor && /home/pi/.virtualenvs/GardenMonitor/bin/python -m pi.log_environment
"""


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


def main():
    # SHT31D Temperature and Humidity sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_sht31d.SHT31D(i2c)

    # TMP36 Temperature Sensor
    backup_sensor = MCP3008(channel=TEMPERATURE_SENSOR_CHANNEL)

    # SHT31D Measurements
    sht31d_temperature_c = sensor.temperature
    sht31d_temperature_f = round((sht31d_temperature_c * (9 / 5)) + 32, 1)
    sht31d_temperature_f_adj = round(sht31d_temperature_f + calibrations['SHT31D']['temperature'], 1)
    sht31d_humidity = int(sensor.relative_humidity)
    sht31d_humidity_adj = int(sht31d_humidity + calibrations['SHT31D']['humidity'])

    # TMP36 Measurements
    temperature_voltage = backup_sensor.voltage
    tmp36_temperature_c = get_temperature_c(temperature_voltage, round_digits=1)
    tmp36_temperature_f = round((tmp36_temperature_c * (9 / 5)) + 32, 1)
    tmp36_temperature_f_adj = round(tmp36_temperature_f + calibrations['TMP36']['temperature'], 1)

    # Save Measurements
    print('logging {}F, {}% Humidity '.format(sht31d_temperature_f_adj, sht31d_humidity_adj))
    environment_models.AirMeasurement.objects.create(
        sht31d_temperature_c=sht31d_temperature_c,
        sht31d_temperature_f=sht31d_temperature_f,
        sht31d_temperature_f_adj=sht31d_temperature_f_adj,
        sht31d_humidity=sht31d_humidity,
        sht31d_humidity_adj=sht31d_humidity_adj,
        tmp36_temperature_c=tmp36_temperature_c,
        tmp36_temperature_f=tmp36_temperature_f,
        tmp36_temperature_f_adj=tmp36_temperature_f_adj
    )


if __name__ == '__main__':
    main()
