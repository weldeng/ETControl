import ETCalc

#grasset = ETCalc.myfunc(latitudeR, longitudeR, elev, day, Tmax, Tmin, RHmax, RHmin, meanwindspdi, Solar, Kc)
grasset = ETCalc.myfunc(latitudeR, longitudeR, 67.0, day, Tmax, Tmin, RHmax, RHmin, meanwindspdi, Solar, Kc)
print grasset
