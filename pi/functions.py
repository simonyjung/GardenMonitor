MIN_HUMIDITY_VALUE = .860
MAX_HUMIDITY_VALUE = .483


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