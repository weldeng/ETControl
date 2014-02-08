# RPi-ETControl.py
# calls to Weather Underground for Opensprinkler.pi hardware
# uses API key 6123f0cccfe7fe9e

WL = 1.05 # program start initial water level (Field Capacity -inches in root zone)

import urllib2
import json
import datetime
import time
import Solarenergy
import ETCalc
from datetime import date, datetime, time, timedelta

dayold = int(datetime.date.today().strftime("%j"))-1
while True:  
    if int(datetime.date.today().strftime("%j")) > dayold:
        dayold = int(datetime.date.today().strftime("%j"))
        #time.sleep(90) # allows time for personal weather stations to write/compute data before requsting that info

        ### CLOSEST WEATHER STATION DATA AQUISITION FOR HISTORICAL SOLAR ENERGY - Uses Solarenergy module
        for d in range (1,2): # where d in the parenthetical numbers are the range in days back in time to check
            mylist = Solarenergy.myfunc(d)  #mylist[0] is the daily watt-hr total of solar energy from module Solarenergy


        ### CLOSEST WEATHER STATION DATA AQUISITION EXCEPT SOLAR ENERGY
        f = urllib2.urlopen('http://api.wunderground.com/api/6123f0cccfe7fe9e/conditions/yesterday/q/VA/Richmond_Hanover_County.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        location = 'Hanover Airport Weather Station'
        maxtempm = parsed_json['history']['dailysummary'][0]['maxtempm']
        mintempm = parsed_json['history']['dailysummary'][0]['mintempm']
        maxhumidity = parsed_json['history']['dailysummary'][0]['maxhumidity']
        minhumidity = parsed_json['history']['dailysummary'][0]['minhumidity']
        meanwindspdi = parsed_json['history']['dailysummary'][0]['meanwindspdi']
        precipi = parsed_json['history']['dailysummary'][0]['precipi']
        f.close()

        ###  INPUTS
        latitudeD = 37.753 #latitude in degrees at sprinklers
        longitudeD = -77.484 #longitude in degrees at sprinklers
        elev = 67.0 #elevation in meters at sprinklers    
        day = int(datetime.date.today().strftime("%j"))-1 #day of year (yesterday, between 1 and 365 or 366)
        Tmax = float(maxtempm) # Degrees C
        Tmin = float(mintempm)  # Degrees C
        RHmax = float(maxhumidity) # Percent
        RHmin = float(minhumidity) # Percent
        meanwindspdi = float(meanwindspdi) # MPH
        Solar = mylist[0] # watt-hours/square meter per day (sum of 24 1 hour periods)from module Solarenergy
        Kc = 0.80  #Crop coefficent for turfgrass (Meyer Zoysia , Rebel II tall fescue)
   
        PAW = 1.4   # Plant Available Water inches/foot for Sandy Loam Soil (Ref. Turfgrass irrigation Circular 660 NM State University)
        MAD = .50   # Management Allowable Depletion 
        RD = 0.75  #root depth in feet

        ### CALCULATIONS ###
        ETc = ETCalc.myfunc(latitudeD, longitudeD, elev, day, Tmax, Tmin, RHmax, RHmin, meanwindspdi, Solar, Kc)
        ETc = float ("%0.3f" % (ETc))
        
        FC = PAW * RD #Field Capacity, inches of water the soil is capable of holding in the root zone
        log = open('ETlog', 'r') # open ETlog and get the soil water level from the two days ago
        for line in log:
            oldday, oldTmax, oldTmin, oldRHmax, oldRHmin, oldmeanwindspdi, oldSolar, oldprecipi, oldETc, oldWL = line.split(",")
            print oldday, oldprecipi, oldETc, oldWL 
            if int(oldday) == day-1:
                WL= float(oldWL)
        log.close()
        #calculate soil water level at the end of yesterday
        if  WL + float(precipi) - ETc >= FC:
            WL = FC
        if  WL + float(precipi) - ETc < FC:
            WL = WL + float(precipi) - ETc        

        ###  OUTPUTS

        ##  open ET log, check if data is already there for yesterday, and if not write the line of data for yesterday
        log = open('ETlog', 'r')
        for line in log:
            lastline = line
        log.close()
        lday,ldateold,lTmax,lTmin,lRHmax,lRHmin,lmeanwindspdi,lSolar,lprecipi,lETc,lWL = lastline.split(",")
        if int(lday) != day:
            dateold = (datetime.now() + timedelta(days=-1)).strftime("%m/%d/%y")
            log = open('ETlog', 'a')
            log.write (" \n" + str(day) + ", " + str(dateold) + ", " + str(Tmax)+ ", " + str(Tmin) + ", " + str(RHmax)+ ", " + str(RHmin) + ", " + str(meanwindspdi) + ", " + str(Solar)+ ", " + str(precipi) + ", " + str(format(ETc, '.3f')) + ", " + str(WL))
            log.close()








