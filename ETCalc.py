# ETCalc.py
def myfunc(latitudeR, longitudeR, elev, day, Tmax, Tmin, RHmax, RHmin, meanwindspdi, Solar, Kc):  # calculates ET with the following inputs

    #latitudeR = lattitude in degrees at sprinklers
    #longitudeR = longitude in degrees at sprinklers
    #elev = elevation in meters at sprinklers
    #day = day of year (integer between 1 and 365 or 366)
    #Tmax = Max temp Degrees C
    #Tmin = Min temp Degrees C
    #RHmax Maximum relative humidity (Percent)
    #RHmin = Minimum relative humidity (Percent)
    #meanwindspdi = mean windspead MPH
    #Solar = watt-hours/square meter per day (sum of 24 1 hour periods)
    #Kc + Crop coefficent for turfgrass (suggest 0.80 for Meyer Zoysia , Rebel II tall fescue from )  

    import math       

    #### CALCULATION OF GRASS EVAPOTRANSPIRATION BASED ON FAO-56 (USING FULL DAY DATA) ####
    pi = math.pi
    latitudeR = latitudeD * pi/180 #lattiude in radians at sprinklers
    longitudeR = longitudeD * pi/180 #longitude in radians at sprinklers         
    Tmean = (Tmax + Tmin)/2 # Degrees C
    Rs = Solar/24 * 0.0864   # MJ/meter squared per day
    u2 = meanwindspdi*0.44704  # Meters/sec windspeed mean - average needed
    delta = 4098*(0.6108*math.exp((17.27*Tmean)/(Tmean+237.3)))/(Tmean +237.3)**2  
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
    ETo = (0.408 * delta * (Rn -0) + Psychrometic_constant *900 /(Tmean +273) *u2 *(es - ea))/(delta + Psychrometic_constant * (1 + 0.34 * u2)) # Reference crop ET (mm/day)
    EToi = ETo / 25.4 # inches/day
    ETc = EToi * Kc # ET for Zoysia or Fescue inches/day

    return [ETc]








