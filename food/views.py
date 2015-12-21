from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import Truck

# Create your views here.

def getTrucks(longitude, latitude):
    pass

def index(request):
    qs = Truck.objects.all()[:5]
    for q in qs:
        hours = q.schedule_set.all()
        menus = q.menu_set.all()
    template = loader.get_template('food/index.html')
    context = RequestContext(request, {'qs': qs, 'hours': hours, 'menus': menus})

    return HttpResponse(template.render(context))


