import smbus
import time

"""
Reads value of analog soil moisture sensor and continuously outputs reading
"""

PCF8591_ADDRESS = 0x48
bus = smbus.SMBus(1)
cmd = 0x40
MIN_HUMIDITY_VALUE = 220  # Value of probe when exposed to air
MAX_HUMIDITY_VALUE = 128  # Value of probe when exposed to water
CHANNELS = [0, 1]  # up to four inputs for PCF8591 Analog to Digital Converter


def read_analog(address, channel, command):
    """
    Read ADC value
    :param address:
    :param channel: Int
    :param command:
    :return:
    """
    value = bus.read_byte_data(address, command + channel)
    return value


def write_analog(address, command, value):
    """
    Write DAC value
    :param value:
    :return:
    """
    bus.write_byte_data(address, command, value)


def get_humidity(value):
    value_range = MIN_HUMIDITY_VALUE - MAX_HUMIDITY_VALUE
    humidity_percentage = ((MIN_HUMIDITY_VALUE - value) / value_range) * 100
    if humidity_percentage < 0:
        return 0
    elif humidity_percentage > 100:
        return 100
    else:
        return round(humidity_percentage, 1)


def clean_up():
    bus.close()


def main():
    while True:
        soil_readings = []
        for channel in CHANNELS:
            value = read_analog(PCF8591_ADDRESS, channel, cmd)
            soil_moisture = get_humidity(value)
            soil_readings.append({'soil_moisture': soil_moisture,
                                  'channel': channel})

        # write the DAC value
        write_analog(PCF8591_ADDRESS,
                     cmd,
                     int(soil_readings[0]['soil_moisture'] * 2.55))

        output_message = "Soil Moisture levels: "
        output_message += ', '.join(["Plant {} - {}%".format(x['channel'], x['soil_moisture'])
                                     for x in soil_readings])
        print(output_message)
        time.sleep(0.2)


if __name__ == '__main__':
    print("Program is starting...")
    try:
        main()
    except KeyboardInterrupt:
        clean_up()
