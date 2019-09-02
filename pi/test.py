import smbus
import time

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40

"""
Reads value of analog soil moisture sensor and continously outputs reading
"""

MIN_HUMIDITY_VALUE = 220
MAX_HUMIDITY_VALUE = 128


def read_analog(channel):
    """
    Read ADC value
    :param channel: 0, 1, 2, 3
    :return:
    """
    value = bus.read_byte_data(address, cmd + channel)
    return value


def write_analog(value):
    """
    Write DAC value
    :param value:
    :return:
    """
    bus.write_byte_data(address, cmd, value)


def get_humidity(value):
    value_range = MIN_HUMIDITY_VALUE - MAX_HUMIDITY_VALUE
    humidity_percentage = ((MIN_HUMIDITY_VALUE - value) / value_range) * 100
    if humidity_percentage < 0:
        return 0
    elif humidity_percentage > 100:
        return 100
    else:
        return round(humidity_percentage, 1)


def loop():
    while True:
        # read the ADC value of channel 0
        value = read_analog(0)
        # write the DAC value
        write_analog(value)
        # calculate the voltage value
        voltage = value / 255.0 * 3.3
        soil_moisture = get_humidity(value)
        print("Soil Moisture 1: {}%".format(soil_moisture))
        time.sleep(0.5)


def clean_up():
    bus.close()


if __name__ == '__main__':
    print("Program is starting...")
    try:
        loop()
    except KeyboardInterrupt:
        clean_up()
