import numpy as np
import pandas as pd
import csv
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



def bookedUnbookedInterval(cal,timeSpan, startingDate, boolean):

    #initialization
    yAxis= [0] * (timeSpan)

    #the x Axis is just the timespan right now.
    # If we want a percentage, it's enough to divide each element on x by the timeSPan
    xAxis= range(timeSpan)
    daysPerHost =105
    #for i in range (0,totalLenght):
    for i in cal.keys():
        #for each host, start the computation at the given starting date
        for j in range(0,daysPerHost-1):
            if(cal[i]['date'][j]== startingDate):
                #print "I'm HEERE"
                #print j
                ytemp=0
                #compute how many days are booked/not booked (depending on the boolean)
                #in the given timeSpan
                for internal_index in range(j,j+timeSpan-1):
                    #print "timespan" + str(internal_index)
                    if(cal[i]['availability'][internal_index]== boolean):
                        ytemp=ytemp+1

                #print "appending" + str(ytemp)

                #in the ytemp position there is the number of hosts with the ytemp number of booked houses
                #print "udating for id" + str(i)
                yAxis[ytemp] = yAxis[ytemp]+1
            #else:
                #print cal[i]['date'][j]
                #print "different from"
                #print startingDate
    #doesn't do anything: to fix
    #plt.plot(xAxis,yAxis)

    print "total number of calendars"
    x = len(cal)
    print x
    if (boolean==True):
        print "y axis: number of hosts with the number of unbooked days on the x axis"
    else:
        print "y axis: number of hosts with the number of booked days on the x axis"

    # print [i/264.0 for i in yAxis]
    print yAxis
    #print yDensity
    print "x axis: day interval"
    print xAxis


def find_orphans(cal, length):
    orphan_start = []
    orphan_end = []
    orphan_price = []

    index = 0
    while index < len(cal['availability']):
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

calendars = pd.read_json('/Users/Elena/Desktop/AirBnb/AirbnbScrape/calendars.json')
#parsed_calendars = parse_calendar(calendars[10627716.0])

all_parsed_calendars = {}
for i in calendars.keys():
    all_parsed_calendars[i] = parse_calendar(calendars[i])
print all_parsed_calendars [10627716.0]['date'][1]

#print parsed_calendars
#parsed_calendars.to_csv('Array.csv')
#print find_orphans(parsed_calendars, 1)


#bookingNearStaying
#bookedUnbookedInterval(all_parsed_calendars,4,'2016-02-28', True)

#professional hosts
# bookedUnbookedInterval(all_parsed_calendars,30,'2016-02-28', False)
print "hey"

bookedUnbookedInterval(all_parsed_calendars,4,'2016-02-28', True)
