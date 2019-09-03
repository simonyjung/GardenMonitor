import django
import os
import smbus

os.environ['DJANGO_SETTINGS_MODULE'] = 'gardenmonitor.settings'
django.setup()

from plants import models as plants_models

"""
Read value of analog soil moisture sensor (up to 4) and log reading to database

Sensor: Capacitive soil moisture sensor v1.2
ADC: PCF8591 4 Channel 8 bit Analog to Digital Converter
"""

# ADC
PCF8591_ADDRESS = 0x48
CONTROL_BYTE = 0x40
CHANNELS = [0, 1]  # up to four inputs for PCF8591 Analog to Digital Converter
# Calibrated sensor values
MIN_HUMIDITY_VALUE = 220  # Value of probe when exposed to air
MAX_HUMIDITY_VALUE = 128  # Value of probe when exposed to water

PLANT_CHANNEL_TO_PK_DICT = {
    0: 1,
    1: 2
}


def read_analog(address, channel, command):
    """
    Read analog signal as 8 bit integer
    :param address:
    :param channel: Int
    :param command:
    :return: 8 bit value of analog signal
    """
    value = bus.read_byte_data(address, command + channel)
    return value


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


def main():
    """
    :return:
    """
    for channel in CHANNELS:
        value = read_analog(PCF8591_ADDRESS, channel, CONTROL_BYTE)
        soil_moisture = get_humidity_percentage(value)
        print("saving {}% moisture level for channel {}".format(soil_moisture, channel))
        measurement = plants_models.PlantSoilMoistureMeasurement.objects.create(
            plant_id=PLANT_CHANNEL_TO_PK_DICT[channel],
            measurement=soil_moisture
        )


if __name__ == '__main__':
    print("Program is starting...")
    bus = smbus.SMBus(1)
    main()
    bus.close()
