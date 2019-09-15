import datetime
from django.db import models


class AirMeasurement(models.Model):
    measurement_datetime = models.DateTimeField(default=datetime.datetime.now)
    sht31d_temperature_c = models.DecimalField(max_digits=4, decimal_places=1)
    sht31d_temperature_f = models.DecimalField(max_digits=4, decimal_places=1)
    sht31d_temperature_f_adj = models.DecimalField(max_digits=4, decimal_places=1)
    sht31d_humidity = models.DecimalField(max_digits=4, decimal_places=1)
    sht31d_humidity_adj = models.DecimalField(max_digits=4, decimal_places=1)
    tmp36_temperature_c = models.DecimalField(max_digits=4, decimal_places=1)
    tmp36_temperature_f = models.DecimalField(max_digits=4, decimal_places=1)
    tmp36_temperature_f_adj = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return "<AirMeasurement {}>".format(self.measurement_datetime)
