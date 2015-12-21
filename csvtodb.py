import psycopg2
import csv
import itertools
from datetime import datetime, timedelta
from urllib2 import URLError
from geopy.geocoders.googlev3 import GoogleV3

try:
    conn = psycopg2.connect("dbname='foodtruck_db' user='inna'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

def timeParser(time):
    abbrDays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    parsedDays = []
    time = time.split(":")
    days = time[0]
    if '-' in days:
        days = days.split('-')
        idx_1 = abbrDays.index(days[0])
        idx_2 = abbrDays.index(days[1])
        days = abbrDays[idx_1:idx_2+1]
        parsedDays.extend(days)
    elif '/' in days:
        days = days.split('/')
        parsedDays.extend(days)
    else:
        parsedDays.append(days)
    hours = time[1]
    if '/' in hours:
        hours = hours.split('/')
    else:
        hours = [hours]
    parsedDays = sorted(set(parsedDays), key=lambda x: parsedDays.index(x))
    permu = list(itertools.product(parsedDays, hours))
    newPermu = []
    for p in permu:
        newHours = []
        hours = p[1].split('-')
        for hour in hours:
            if 'PM' in hour:
                if '12' in hour:
                    nhour = int(hour[:-2])
                else:
                    nhour = (int(hour[:-2]) + 12) % 24
                newHours.append(nhour)
            if 'AM' in hour:
                if '12' in hour:
                    nhour = 0
                else:
                    nhour = int(hour[:-2])
                newHours.append(nhour)
        if newHours[0] > newHours[1] and newHours[1] != 0:
            idx = abbrDays.index(p[0])
            hour1 = p[0], [newHours[0], 0]
            hour2 = abbrDays[(idx+1)%7], [0, newHours[1]]
            newPermu.append(hour1)
            newPermu.append(hour2)
        else:
            newHours = p[0], newHours
            newPermu.append(newHours)
    return newPermu

def foodParser(food):
    if ':' in food:
        food = food.split(':')
    return food


def truncate(entry):
    if len(entry) < 100:
        return entry
    return entry[:97] + "..."

##########################################################
############ SQL INSERTION FUNCTIONS #####################
##########################################################

def scheduleSQL(schedule, applicant, status, expirationDate):
    if len(expirationDate) != 22:
        expirationDate = datetime.now() + timedelta(days=365)
    for s in schedule:
        day = s[0]
        start_hour = "%s:00" % s[1][0]
        end_hour = "%s:00" % s[1][1]
        print locationId, s[0], s[1][0], s[1][1]
        cur.execute('INSERT INTO food_schedule (truck_id, day, start_hour, end_hour, status, expiration_date) VALUES (%s, %s, %s, %s, %s, %s)', (locationId, day, start_hour, end_hour, status, expirationDate))

def truckSQL(locationId, applicant, facilityType, locationDescription, address, latitude, longitude):
    if not latitude or not longitude:
        address = '%s, San Francisco' % (address)
        geocoder = GoogleV3(timeout=None)
        try:
            _, latlon = geocoder.geocode(address)
            latitude, longitude = latlon[0], latlon[1]
        except (URLError, ValueError):
            latitude = 0.0
            longitude = 0.0
    latlon = "POINT(%s %s)" % (latitude, longitude)
    print locationId, applicant, facilityType, locationDescription, address, latlon, latitude, longitude

    cur.execute('INSERT INTO food_truck (truck_id, name, facility_type, location_description, address, latlon, lat, lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (locationId, applicant, facilityType, locationDescription, address, latlon, latitude, longitude))

def foodSQL(locationId, food):
    if type(food) == list:
        for f in food:
            print locationId, f
            cur.execute('INSERT INTO food_menu (truck_id, item) VALUES (%s, %s)', (locationId, f))
    else:
        f = truncate(food)
        cur.execute('INSERT INTO food_menu (truck_id, item) VALUES (%s, %s)', (locationId, f))

def data():
    truckData = []
    with open('food.csv') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        print headers
        for line in reader:
            truckData.append(line)
    return truckData


def main():
    data = data()
    for line in data:
        locationId = line[0]
        applicant = line[1]
        facilityType = line[2]
        locationDescription = truncate(line[4])
        address = line[5]
        status = line[10]
        foodItems = line[11]
        latitude = line[14]
        longitude = line[15]
        dayshours = line[17]
        expirationDate = line[22]
        truckSQL(locationId, applicant, facilityType, locationDescription, address, latitude, longitude)
        if dayshours:
            schedule = timeParser(dayshours)
            scheduleSQL(schedule, applicant, status, expirationDate)
        food = foodParser(foodItems)
        if food:
            foodSQL(locationId, food)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()




