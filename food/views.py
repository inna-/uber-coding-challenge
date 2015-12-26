from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.db.models import Q
from models import Truck
from datetime import datetime, date
from pytz import timezone
import operator

def getTrucks(latitude, longitude):
    current_point = GEOSGeometry('POINT(%s %s)' % (latitude, longitude), srid=4326)
    trucks = Truck.objects.filter(latlon__distance_lte=(current_point, D(km=1)))
    return trucks

weekday = {
    0: "Mo",
    1: "Tu",
    2: "We",
    3: "Th",
    4: "Fr",
    5: "Sa",
    6: "Su",
}

def index(request):
    alls = [{'val': 'all', 'chked':False, 'label':'All'}]
    foodtypes = [    
        {'val': 'openNow', 'chked':False, 'label':'Open Now'},
        {'val':'sandwiches', 'chked':False, 'label':'Sandwiches'}, 
        {'val':'burgers', 'chked':False, 'label':'Burgers'},
        {'val':'noodles', 'chked':False, 'label':'Noodles'},
        {'val':'snacks', 'chked':False, 'label':'Snacks'},
        {'val':'coffee', 'chked':False, 'label':'Coffee'},
        {'val':'pastries', 'chked':False, 'label':'Pastries'},
        {'val':'iceCream', 'chked':False, 'label':'Ice Cream'},
        {'val':'drinks', 'chked':False, 'label':'Drinks'},
        {'val':'mexican', 'chked':False, 'label':'Mexican'}
        ]

    san_fran = timezone('US/Pacific')
    sf_time = datetime.now(san_fran)
    sf_year = sf_time.year
    sf_month = sf_time.month
    sf_day = sf_time.day
    sf_dow = weekday[sf_time.weekday()]
    sf_hour = sf_time.strftime("%H:%M")

    filt = Q()

    lat = 37.773972
    lon = -122.431297
    z = 12
    qs = Truck.objects.all()

    try:
        allF = request.GET.get('all')
        a = filter(lambda x: x['val'] == 'all', alls)[0]
        a['chked'] = True
    except:
        pass

    try:
        foods = request.GET.getlist('food')
        if len(foods) != 0:
            qchk = Q()
            for food in foods:
                if food == 'openNow':
                    f = filter(lambda x: x['val'] == 'openNow', foodtypes)[0]
                    filt &= Q(schedule__start_hour__lte=sf_hour, schedule__end_hour__gte=sf_hour, schedule__day=sf_dow)
                    f['chked'] = True
                if food == 'pastries':
                    qStr = ['muffins', 'pastries', 'donuts', 'bagels']
                    for term in qStr:
                        qchk |= Q(food_item__contains=term)
                    f = filter(lambda x: x['val'] == food, foodtypes)[0]
                    f['chked'] = True
                if food == 'pastries':
                    qStr = ['muffins', 'pastries', 'donuts', 'bagels']
                    for term in qStr:
                        qchk |= Q(food_item__contains=term)
                    f = filter(lambda x: x['val'] == food, foodtypes)[0]
                    f['chked'] = True
                if food == 'mexican':
                    qStr = ['taco', 'quesadillas', 'burritos', 'mexican']
                    for term in qStr:
                        qchk |= Q(food_item__contains=term)
                    f = filter(lambda x: x['val'] == food, foodtypes)[0]
                    f['chked'] = True
                if food == 'snacks':
                    qStr = ['candy', 'candies', 'chips', 'cookies']
                    for term in qStr:
                        qchk |= Q(food_item__contains=term)
                    f = filter(lambda x: x['val'] == food, foodtypes)[0]
                    f['chked'] = True
                if food == 'drinks':
                    qStr = ['soda', 'beverages', 'juice', 'milk', 'gatorade', 'cocoa', 'water']
                    for term in qStr:
                        qchk |= Q(food_item__contains=term)
                    f = filter(lambda x: x['val'] == food, foodtypes)[0]
                    f['chked'] = True
                else:
                    f = filter(lambda x: x['val'] == food, foodtypes)[0]
                    qchk &= Q(food_item__icontains = food)
                    f['chked'] = True
            filt &= (qchk)
    except:
        pass

    try:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        current_point = GEOSGeometry('POINT(%s %s)' % (lat, lon), srid=4326)
        filt &= Q(latlon__distance_lte=(current_point, D(km=1)))
    except:
        pass

    qss = Truck.objects.filter(filt)

    z = 12
    qLen = len(qss)
    template = loader.get_template('food/index.html')
    context = RequestContext(request, {'qs': qss, 'z': z, 'len': qLen, 'foodtypes':foodtypes, 'alltypes':alls})

    return HttpResponse(template.render(context))


