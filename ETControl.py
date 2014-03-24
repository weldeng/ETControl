# RPi-ETControl.py, written in Python version 2.7.6
# calls to Weather Underground for Opensprinkler.pi hardware
# uses API key 6123f0cccfe7fe9e


import urllib2
import json
import time
import datetime
import Solarenergy4
import ETCalc

ri = raw_input('Enter program start initial water level in root zone two days ago(range 0.0 - 1.05 inches(FC)): ')
WL = float(ri)
#WL = 1.05
irrigate = 0.00
print "day, Tmax, Tmin, RHmax, RHmin, windspd, Solar, precip, ETc, WL, irrigate"

dayold = int(datetime.date.today().strftime("%j"))-1
while True:  
    if int(datetime.date.today().strftime("%j")) > dayold:
        dayold = int(datetime.date.today().strftime("%j"))
        time.sleep(90) # allows time for personal weather stations to write/compute data before requsting that info

        ### CLOSEST WEATHER STATION DATA AQUISITION FOR HISTORICAL SOLAR ENERGY - Uses Solarenergy4 module
        for d in range (1,2): # where d in the parenthetical numbers are the range in days back in time to check
            mylist = Solarenergy4.myfunc(d)  #mylist[0] is the daily watt-hr total of solar energy from module Solarenergy4
  
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
        MAD = .50   # Management Allowable Depletion, more than this and the grass starts to wilt
        RD = 0.75  #root depth in feet


        ### CALCULATIONS ###
        ETc = ETCalc.myfunc(latitudeD, longitudeD, elev, day, Tmax, Tmin, RHmax, RHmin, meanwindspdi, Solar, Kc)
        ETc = float ("%0.3f" % (ETc))       
        FC = PAW * RD #Field Capacity, inches of water the soil is capable of holding in the root zone

        #calculate soil water level at the end of yesterday
        if  WL + float(precipi) - ETc >= FC:
            WL = FC
        if  WL + float(precipi) - ETc < FC:
            WL = WL + float(precipi) - ETc

        # run sprinklers to refill to field capacity if needed
        if WL - ETc < FC * MAD:
            irrigate = FC - WL # inches
            # insert code to wait until start time, run sprinklers to deposit irrigate amount of water
            WL = FC


        ###  OUTPUTS

        print day, Tmax, Tmin, RHmax, RHmin, meanwindspdi, Solar, precipi, ETc, WL, irrigate
        log = open('ETlog', 'a')
        log.write ("\n" + str(day) + ", " + str(Tmax)+ ", " + str(Tmin) + ", " + str(RHmax)+ ", " + str(RHmin) + ", " + str(meanwindspdi) + ", " + str(Solar)+ ", " + str(precipi) + ", " + str(format(ETc, '.3f')) + ", " + str(WL)+ ", " + str(irrigate))
        log.close()








