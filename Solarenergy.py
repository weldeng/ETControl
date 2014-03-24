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

    # Go to weather underground on selected date to get the historical weather at Hanover airport using the following
    # 1-Time,2-TemperatureF,3-DewpointF,4-PressureIn,5-WindDirection,6-WindDirectionDegrees,7-WindSpeedMPH,8-WindSpeedGustMPH,
    # 9-Humidity,10-HourlyPrecipIn,11-Conditions,12-Clouds,13-dailyrainin,14-SolarRadiationWatts/m^2,15-SoftwareType,16-DateUTC

    solartotal = 0.00
    webpage = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KVAASHLA4&month=" + MM + "&day=" + DD + "&year=" + YYYY + "&format=1"          
    for yesterdaysweather in urllib2.urlopen(webpage):

        if " 00:00" in yesterdaysweather and " 04:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:   solartotal = solartotal + float(i)                
        if " 01:00" in yesterdaysweather and " 05:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 02:00" in yesterdaysweather and " 06:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)            
        if " 03:00" in yesterdaysweather and " 07:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 04:00" in yesterdaysweather and " 08:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 05:00" in yesterdaysweather and " 09:00" in yesterdaysweather :
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)              
        if " 06:00" in yesterdaysweather and " 10:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 07:00" in yesterdaysweather and " 11:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)              
        if " 08:00" in yesterdaysweather and " 12:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 09:00" in yesterdaysweather and " 13:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)                
        if " 10:00" in yesterdaysweather and " 14:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)             
        if " 11:00" in yesterdaysweather and " 15:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)              
        if " 12:00" in yesterdaysweather and " 16:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 13:00" in yesterdaysweather and " 17:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 14:00" in yesterdaysweather and " 18:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)      
        if " 15:00" in yesterdaysweather and " 19:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 16:00" in yesterdaysweather and " 20:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 17:00" in yesterdaysweather and " 21:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 18:00" in yesterdaysweather and " 22:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)            
        if " 19:00" in yesterdaysweather and " 23:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 20:00" in yesterdaysweather and " 00:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 21:00" in yesterdaysweather and " 01:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
        if " 22:00" in yesterdaysweather and " 02:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)                
        if " 23:00" in yesterdaysweather and " 03:00" in yesterdaysweather : 
            count = 0
            for i in yesterdaysweather.split(','):
                count = count + 1            
                if count is 14:
                    solartotal = solartotal + float(i)
    return [solartotal] # watt-hours total for the day






