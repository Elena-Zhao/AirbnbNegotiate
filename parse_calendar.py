import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def parse_calendar(list_calendar):
    date = []
    price_USD = []
    availability = []
    for month in list_calendar['calendar_months']:
        for day in month['days']:
            date.append(day['date'])
            price_USD.append(day['price']['native_price'])
            availability.append(day['available'])
    return pd.DataFrame({'date':date, 'price_USD': price_USD, 'availability':availability})

def find_orphans(cal, length):
    orphan_start = []
    orphan_end = []
    orphan_price = []

    index = 0
    while index < len(cal['availability']) - 2:
        count = 0
        start = index
        while cal['availability'][index] == True and count < length:
            count += 1
            if count >= length and cal['availability'][index + 1] == False:
                orphan_start.append(cal['date'][start])
                orphan_end.append(cal['date'][index])
                if length == 1:
                    orphan_price.append(cal['price_USD'][start])
                else:
                    orphan_price.append(np.mean(cal['price_USD'][start: index]))
                break
            index += 1
        index += 1

    return pd.DataFrame({'Start': orphan_start, 'End': orphan_end, 'Price': orphan_price})

def listings_price_var(calendars):
    listings_var = {}
    for i in calendars.keys():
        listings_var[i] = np.var(parse_calendar(calendars[i])['price_USD'])
    return listings_var


calendars = pd.read_json('/Users/Elena/Desktop/AirBnb/Codes/calendars/1456693184.99.json')
parsed_calendars = {}
for i in calendars.keys():
    parsed_calendars[i] = parse_calendar(calendars[i])

num_1d = 0
num_2d = 0
num_3d = 0
for i in parsed_calendars.values()[5:]:
    num_1d += len(find_orphans(i, 1))
    num_2d += len(find_orphans(i, 2))
    num_3d += len(find_orphans(i, 3))

print num_1d, num_2d, num_3d