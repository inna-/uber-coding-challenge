from __future__ import unicode_literals
from datetime import datetime, timedelta

from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models
from geopy.geocoders import GoogleV3

# Create your models here.

class Truck(models.Model):
    truck_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    facility_type = models.CharField(max_length=50)
    location_description = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    food_item = models.CharField(max_length=500, default=None)
    latlon = gis_models.PointField(srid=4326, geography=True, blank=True, null=True)
    dayhour = models.CharField(max_length=500, default=None)
    status = models.CharField(max_length=50, default='REQUESTED')
    expiration_date = models.DateTimeField(default=datetime.now() + timedelta(days=365))

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        self.latlon = "POINT(%s %s)" % (self.lat, self.lon)
        if not self.lat and not self.lon:
            address = u'%s' % (self.address)
            address = address.encode('utf-8')
            geocoder = Google()
            try:
                _, latlon = geocoder.geocode(address)
            except (URLError, ValueError):
                pass
            else:
                point = "POINT(%s %s)" % (latlon[1], latlon[0])
                self.latlon = geos.fromstr(point)
        super(Truck, self).save()

class Schedule(models.Model):
    truck = models.ForeignKey(Truck)
    day = models.CharField(max_length=2)
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    
    def __unicode__(self):
        return u'%s %s %s %s' % (self.truck, self.day, self.start_hour, self.end_hour)

class Menu(models.Model):
    truck = models.ForeignKey(Truck)
    item = models.CharField(max_length=100)

    def __unicode__(self):
        return self.item
