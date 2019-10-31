import datetime

date1 = "20150625"
#date2 = "2018-01-01"

datetime_object = datetime.datetime.strptime(date1, "%Y%m%d")
#datetime_object2 = datetime.datetime.strptime(date2, "%Y-%m-%d")

image_date = datetime_object.strftime("%Y-%m-%d")
#print datetime_object2.strftime("%Y-%m-%d")

print(image_date)
