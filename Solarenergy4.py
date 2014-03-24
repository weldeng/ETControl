def myfunc(d):  # gets solar energy weather data for todays date - the number of days d

    import urllib2
    import datetime

    now = datetime.datetime.now()
    from datetime import date, timedelta
    datebefore = date.today()-timedelta(days=d)

    reportyear = datebefore.year
    YYYY = str(reportyear)
    reportmonth = datebefore.month
    MM = str(reportmonth)
    reportday = datebefore.day
    DD = str(reportday)

    # Go to weather underground on selected date to get the historical weather at Ashland, VA Weatherststion where the following
    # 1-Time,2-TemperatureF,3-DewpointF,4-PressureIn,5-WindDirection,6-WindDirectionDegrees,7-WindSpeedMPH,8-WindSpeedGustMPH,
    # 9-Humidity,10-HourlyPrecipIn,11-Conditions,12-Clouds,13-dailyrainin,14-SolarRadiationWatts/m^2,15-SoftwareType,16-DateUTC

    solartotal = 0.00
    webpage = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KVAASHLA4&month=" + MM + "&day=" + DD + "&year=" + YYYY + "&format=1"          
    for yesterdaysweather in urllib2.urlopen(webpage):
        count = 0
        for i in yesterdaysweather.split(','):
            count = count + 1            
            if count is 14:
                try:
                    solartotal = solartotal + float(i)*.25 #15 minute uniform increments at this weather station
                except:
                    pass
    return [solartotal] # watt-hours total for the day





