# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=2)),
                ('start_hour', models.TimeField()),
                ('end_hour', models.TimeField()),
                ('status', models.CharField(default='REQUESTED', max_length=50)),
                ('expiration_date', models.DateTimeField(default=datetime.datetime(2016, 12, 20, 4, 20, 56, 847617))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('truck_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('facility_type', models.CharField(max_length=50)),
                ('location_description', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('lat', models.FloatField(default=0.0)),
                ('lon', models.FloatField(default=0.0)),
                ('latlon', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='schedule',
            name='truck',
            field=models.ForeignKey(to='food.Truck'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='truck',
            field=models.ForeignKey(to='food.Truck'),
            preserve_default=True,
        ),
    ]
