# Generated by Django 2.2.4 on 2019-09-15 02:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('sht31d_temperature_c', models.DecimalField(decimal_places=1, max_digits=4)),
                ('sht31d_temperature_f', models.DecimalField(decimal_places=1, max_digits=4)),
                ('sht31d_temperature_f_adj', models.DecimalField(decimal_places=1, max_digits=4)),
                ('sht31d_humidity', models.DecimalField(decimal_places=1, max_digits=4)),
                ('sht31d_humidity_adj', models.DecimalField(decimal_places=1, max_digits=4)),
                ('tmp36_temperature_c', models.DecimalField(decimal_places=1, max_digits=4)),
                ('tmp36_temperature_f', models.DecimalField(decimal_places=1, max_digits=4)),
                ('tmp36_temperature_f_adj', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
    ]
