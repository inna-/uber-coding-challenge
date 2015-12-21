from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from models import Truck

# Create your views here.

def getTrucks(latitude, longitude):
    current_point = GEOSGeometry('POINT(%s %s)' % (latitude, longitude), srid=4326)
    trucks = Truck.objects.filter(latlon__distance_lte=(current_point, D(km=1)))
    return trucks

def index(request):
    try:
        lat  = request.GET.get('lat')
        lon  = request.GET.get('lon')
        z = request.GET.get('zoom')
        qs = getTrucks(lat, lon) 
    except:
        lat = 37.773972
        lon = -122.431297
        z = 12
        qs = Truck.objects.all()
    template = loader.get_template('food/index.html')
    context = RequestContext(request, {'qs': qs, 'z': z})

    return HttpResponse(template.render(context))


