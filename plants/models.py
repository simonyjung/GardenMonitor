import datetime
from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=255, blank=True)
    created_datetime = models.DateTimeField(default=datetime.datetime.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "<Plant {}>".format(self.name)

    @property
    def latest_soil_moisture_measurement(self):
        return self.soil_moisture_measurements.latest()


class PlantSoilMoistureMeasurement(models.Model):
    plant = models.ForeignKey(Plant, related_name='soil_moisture_measurements', on_delete=models.SET_NULL,
                              null=True)
    created_datetime = models.DateTimeField(default=datetime.datetime.now)
    measurement = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        get_latest_by = 'created_datetime'


