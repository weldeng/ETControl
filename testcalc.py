import ETCalc

#ETc = ETCalc.myfunc(latitudeR, longitudeR, elev, day, Tmax, Tmin, RHmax, RHmin, meanwindspdi, Solar, Kc)
ETc = ETCalc.myfunc(37.753, -77.484, 67.0, 37, 8.0, 0.0, 100.0, 57.0, 4.0, 2452.0, 0.80)
print ETc, " inches evapotranspiration occurred"
