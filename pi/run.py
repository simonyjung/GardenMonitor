import board
import time
import busio
import adafruit_sht31d

from phue import Bridge
from gpiozero import MCP3008, RGBLED

from pi.sensor_calibrations import indoor_calibrations as calibrations
from pi.functions import get_humidity_percentage, get_temperature_f


# Base Calibration
MIN_HUMIDITY_VALUE = .860
MAX_HUMIDITY_VALUE = .483
MOISTURE_SENSOR_CHANNELS = [0, 1]  # 0, 1, 2, 3
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
LIGHTS = {1: 6,
          0: 5}

DRY_CUTOFF = 25

BLUE_HUE = 45808
BLUE_SATURATION = 254
NORMAL_HUE = 8402
NORMAL_SATURATION = 140

"""
Get readings of up to 2 Capacitive soil moisture sensors, temperature (TMP36) using 
MCP3008 10bit Analog Digital Converter

Turn Hue lights above plant blue if soil moisture is below DRY_CUTOFF
"""


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

            # record light status
            state_dict['light_{}'.format(channel)] = {
                'on': lights[LIGHTS[channel]].on,
                'hue': lights[LIGHTS[channel]].hue,
                'saturation': lights[LIGHTS[channel]].saturation,
                'brightness': lights[LIGHTS[channel]].brightness,
            }

            message += "|| Plant {}: {}%, Light {}: On: {} - {} H, {} S, {} B ".format(
                channel,
                soil_moisture,
                channel,
                state_dict['light_{}'.format(channel)]['on'],
                state_dict['light_{}'.format(channel)]['hue'],
                state_dict['light_{}'.format(channel)]['saturation'],
                state_dict['light_{}'.format(channel)]['brightness'],
            )

            # Blue is hue 45808 sat 254
            # normal hue 8402 sat 140
            if lights[LIGHTS[channel]].on:
                if soil_moisture < DRY_CUTOFF:
                    print("dry soil detected, turning light blue")
                    lights[LIGHTS[channel]].hue = BLUE_HUE
                    lights[LIGHTS[channel]].saturation = BLUE_SATURATION
                elif lights[LIGHTS[channel]].hue == BLUE_HUE:
                    print("Wet soil but light blue, turning back to normal")
                    #  but what is normal? Check other light
                    other_light = lights[LIGHTS[(1, 0)[channel]]]
                    if other_light.hue == BLUE_HUE:  # if blue, use preset
                        lights[LIGHTS[channel]].hue = NORMAL_HUE
                        lights[LIGHTS[channel]].saturation = NORMAL_SATURATION
                        print("normal: {} Hue, {} Saturation".format(NORMAL_HUE, NORMAL_SATURATION))
                    else:
                        lights[LIGHTS[channel]].hue = other_light.hue
                        lights[LIGHTS[channel]].saturation = other_light.saturation
                        print("normal: {} Hue, {} Saturation".format(other_light.hue, other_light.saturation))
                else:
                    pass
            # print("Sensor {}: {}".format(channel, value))

        # TMP36 reading
        temperature_voltage = temperature_sensor.voltage
        temperature = get_temperature_f(temperature_voltage, round_digits=1)
        state_dict['temperature'] = {
            'voltage': temperature_voltage,
            'fahrenheit': temperature,
        }
        temperature_message = "| TMP36 Temperature: {}F {}Fc".format(
            temperature,
            round(temperature + calibrations['TMP36']['temperature'], 1)
        )

        # SHT31D reading
        SHT31D_temp = round((sensor.temperature * (9 / 5)) + 32, 1)
        SHT31D_relative_humidity = int(sensor.relative_humidity)
        SHT_message = '|| SHT31D Temperature: {}F {} Fc Humidity: {}% '.format(
            SHT31D_temp,
            round(SHT31D_temp + calibrations['SHT31D']['temperature'], 1),
            SHT31D_relative_humidity)
        print(SHT_message + message)
        time.sleep(1)


if __name__ == '__main__':
    main()
