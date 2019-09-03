import smbus
import time

"""
Read value of analog soil moisture sensor (up to 4) and continuously output reading.

Sensor: Capacitive soil moisture sensor v1.2
ADC: PCF8591 4 Channel 8 bit Analog to Digital Converter
"""

PCF8591_ADDRESS = 0x48
CONTROL_BYTE = 0x40
MIN_HUMIDITY_VALUE = 220  # Value of probe when exposed to air
MAX_HUMIDITY_VALUE = 128  # Value of probe when exposed to water
CHANNELS = [0, 1]  # up to four inputs for PCF8591 Analog to Digital Converter


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


def write_analog(address, command, value):
    """
    Write DAC value
    :param address:
    :param value: 8 bit integer
    :param command:
    :return:
    """
    bus.write_byte_data(address, command, value)


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
    Continuously print sensor readings
    :return:
    """
    while True:
        soil_readings = []
        for channel in CHANNELS:
            value = read_analog(PCF8591_ADDRESS, channel, CONTROL_BYTE)
            soil_moisture = get_humidity_percentage(value)
            soil_readings.append({'soil_moisture': soil_moisture,
                                  'channel': channel})

        # write the DAC value
        write_analog(PCF8591_ADDRESS,
                     CONTROL_BYTE,
                     int(soil_readings[0]['soil_moisture'] * 2.55))

        output_message = "Soil Moisture levels: "
        output_message += ', '.join(["Plant {} - {}%".format(x['channel'], x['soil_moisture'])
                                     for x in soil_readings])
        print(output_message)
        time.sleep(0.2)


if __name__ == '__main__':
    print("Program is starting...")
    bus = smbus.SMBus(1)
    try:
        main()
    except KeyboardInterrupt:
        bus.close()
