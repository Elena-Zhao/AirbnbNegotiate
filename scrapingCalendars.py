import urllib2
import time
import json
import pandas as pd
import random
import numpy as np
start = time.time()
#lenght of the calendar you want to scrape
months= 3
#ids of hosts
listing_info = pd.read_csv('listings 2.csv')
ids = listing_info['id']
calendars = dict()
# ids = [66288, 9887215, 10906, 3049206, 591248, 5791244, 6676364, 251657, 4549374, 4359160, 1695275, 7954270, 6554785, 4849808, 1143563, 8694786, 6742905, 8555943, 1811776, 10627716]
# ids = [1811776]
sleep_time = []
def getCalendar(ids, months):
    counter = 1
    lost_ids = []
    for s in ids:
        hostURL= 'https://www.airbnb.it/api/v2/calendar_months?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=EUR&locale=en&listing_id='+str(s)+'&month=3&year=2016&count='+str(months)+'&_format=with_conditions'
        print counter
        req = urllib2.Request(hostURL
        #simulate a browser not to be blocked
        ,headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
        # response = urllib2.urlopen(req)
        # data = json.load(response)
        # calendars[s] = data
        # counter += 1
        try:
            response = urllib2.urlopen(req)
            data = json.load(response)
            calendars[s] = data
            counter += 1
        except urllib2.HTTPError, e:
            lost_ids.append(s)
            print e.fp.read()
            time.sleep(15)
        time.sleep(random.uniform(0.5, 8))

        if(counter % 3 == 0):
            # with open('calendars/' + str(time.time())+'.json', 'w') as outfile:
            with open('calendars/cal.json', 'w') as outfile:
                json.dump(calendars, outfile)
            with open('calendars/failed_ids.json', 'w') as outfile:
                json.dump(lost_ids, outfile)
    return

getCalendar(ids,months)

print 'Total Execution Time:', time.time() - start