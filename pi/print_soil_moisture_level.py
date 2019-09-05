import smbus
import time
from .components.PCF8574 import PCF8574_GPIO
from .components.Adafruit_LCD1602 import Adafruit_CharLCD
"""
Read value of analog soil moisture sensor (up to 4) and continuously output reading.

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
# IO expander
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.


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


def initialize_pcf8574():
    try:
        pcf8574 = PCF8574_GPIO(PCF8574_address)
        return pcf8574
    except:
        try:
            pcf8574 = PCF8574_GPIO(PCF8574A_address)
            return pcf8574
        except:
            print('I2C Address Error !')
            return None


def main(lcd_display=None):
    """
    Continuously print sensor readings
    :return:
    """
    while True:
        soil_readings = []
        soil_readings_dict = {}
        for channel in CHANNELS:
            value = read_analog(PCF8591_ADDRESS, channel, CONTROL_BYTE)
            soil_moisture = get_humidity_percentage(value)
            soil_readings.append({'soil_moisture': soil_moisture,
                                  'channel': channel})
            soil_readings_dict[channel] = soil_moisture

        # write the DAC value to light led
        write_analog(PCF8591_ADDRESS,
                     CONTROL_BYTE,
                     int(soil_readings[0]['soil_moisture'] * 2.55))

        output_message = "Soil Moisture levels: "
        output_message += ', '.join(["Plant {} - {}%".format(x['channel'], x['soil_moisture'])
                                     for x in soil_readings])
        print(output_message)
        # construct lcd message
        lcd_message = ' '.join(["{} {}%".format(x['channel'], x['soil_moisture']) for x in soil_readings])
        lcd_display.message(lcd_message)
        time.sleep(0.2)


if __name__ == '__main__':
    print("Program is starting...")
    bus = smbus.SMBus(1)

    pcf8574 = initialize_pcf8574()
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=pcf8574)
    try:
        main(lcd_display=lcd)
    except KeyboardInterrupt:
        bus.close()
