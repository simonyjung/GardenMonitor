import datetime
from django.db import models


# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=255, blank=True)
    created_datetime = models.DateTimeField(default=datetime.datetime.now)
    is_active = models.BooleanField(default=True)
