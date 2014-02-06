# RPi-ETControl.py
# calls to Weather Underground for Opensprinkler.pi hardware
# uses API key 6123f0cccfe7fe9e

WL = 1.05 # program start initial water level (Field Capacity -inches in root zone)


import urllib2
import json
import math
import time
import datetime
import Solarenergy

dayold = int(datetime.date.today().strftime("%j"))-1
while True:  
    if int(datetime.date.today().strftime("%j")) > dayold:
        dayold = int(datetime.date.today().strftime("%j"))
        time.sleep(90) # allows time for personal weather stations to write/compute data before requsting that info

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

        #### CALCULATION OF GRASS EVAPOTRANSPIRATION BASED ON FAO-56 (USING PRIOR DAY DATA) ####

        ###CONSTANTS
        pi = math.pi
        elev = 67.0 #elevation in meters at sprinklers
        latitudeR = 37.753 * pi/180 #lattiude in radians at sprinklers
        longitudeR = -77.484 * pi/180 #longitude in radians at sprinklers


        ###  INPUTS
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
        Tmean = (Tmax + Tmin)/2 # Degrees C
        Rs = Solar/24 * 0.0864   # MJ/meter squared per day
        u2 = meanwindspdi*0.44704  # Meters/sec windspeed mean - average needed
        delta = 4098*(0.6108*math.exp((17.27*Tmean)/(Tmean+237.3)))/(Tmean +237.3)**2  # calc validated Table 2.4 FAO-56
        P = 101.3*(((293 - 0.0065*elev)/293)**5.26) # Atmospheric Pressure kPa
        Psychrometic_constant = 0.000665*P
        DT = delta/(delta + Psychrometic_constant*(1 + 0.34*u2))  # Delta term
        PT = Psychrometic_constant/(delta + Psychrometic_constant*(1 + 0.34*u2))  # Psi term
        TT = (900/(Tmean + 273))*u2  # Temperature Term
        eTmax = 0.6108*math.exp((17.27*Tmax)/(Tmax+237.3))
        eTmin = 0.6108*math.exp((17.27*Tmin)/(Tmin+237.3))
        es = (eTmax +eTmin)/2 #Mean saturation vapor pressure
        ea = (eTmin*(RHmax/100) + eTmax*(RHmin/100))/2  #actual vapor pressure
        dr = 1 + 0.033 * math.cos(2* pi * day /365)
        d = 0.409 * math.sin((2* pi * day /365) - 1.39)
        ws = math.acos(-1*math.tan(latitudeR) * math.tan(d))
        Ra = 24 * 60 / pi * 0.0820 * dr * (ws * math.sin(latitudeR) * math.sin(d) + math.cos(latitudeR)* math.cos(d) * math.sin(ws))
        Rso = (0.75 + 2*elev/100000) * Ra
        Rns = (1-.23)*Rs # Net Solar MJ/meter squared per day, grass refernce crop
        Rnl = 4.903 * 10**-9 *(((Tmax +273.16)**4 + (Tmin +273.16)**4)/2) * (0.34 -0.14 * math.sqrt(ea)) * (1.35*Rs/Rso - 0.35)
        Rn = Rns - Rnl
        ETo = (0.408 * delta * (Rn -0) + Psychrometic_constant *900 /(Tmean +273) *u2 *(es - ea))/(delta + Psychrometic_constant * (1 + 0.34 * u2))
        EToi = ETo / 25.4 # inches/day
        ETc = EToi * Kc # inches/day
        FC = PAW * RD #Field Capacity, inches of water the soil is capable of holding in the root zone

        log = open('ETlog', 'r') # open ETlog and get the soil water level from the two days ago
        for line in log:
            oldday, oldTmax, oldTmin, oldRHmax, oldRHmin, oldmeanwindspdi, oldSolar, oldprecipi, oldETc, oldWL = line.split(",")
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
        lday,lTmax,lTmin,lRHmax,lRHmin,lmeanwindspdi,lSolar,lprecipi,lETc,lWL = lastline.split(",")
        if int(lday) != day:
            log = open('ETlog', 'a')
            log.write (" \n" + str(day) + ", " + str(Tmax)+ ", " + str(Tmin) + ", " + str(RHmax)+ ", " + str(RHmin) + ", " + str(meanwindspdi) + ", " + str(Solar)+ ", " + str(precipi) + ", " + str(format(ETc, '.3f')) + ", " + str(WL))
            log.close()








