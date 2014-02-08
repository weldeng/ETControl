import datetime
print datetime.date.today().strftime("%m/%d/%y")
from datetime import date, datetime, time, timedelta

olddate = (datetime.now() + timedelta(days=-1)).strftime("%m/%d/%y")
print olddate
#print olddate.strftime("%m/%d/%y")
