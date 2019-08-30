import datetime
from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=255, blank=True)
    created_datetime = models.DateTimeField(default=datetime.datetime.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "<Plant {}>".format(self.name)