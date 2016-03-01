import urllib2,socks, socket
from stem import Signal
from stem.control import Controller
import time
import json
import pandas as pd
import random
import numpy as np

#README
#download TorBrowser
#open Tor Browser\Browser\TorBrowser\Data\Tor\torrc
#comment all

#insert these 2 lines of code:
#ControlPort 9051
#HashedControlPassword 16:7FA1766AE1DC149A603309B1BF8EBBAAA3F44C237898EF82D19908BD92

#launch TorBrowser
#launch this script (TorBrowser will looks stucked, but whe it's in this state the script works) 
#/README

start = time.time()
#lenght of the calendar you want to scrape
months= 3
#ids of hosts
# ids= ["9631933", "10906"]
listing_info = pd.read_csv('OutputFile.csv')
ids = listing_info['ListingID']
calendars = dict()

#number of ids before the longer interval
longer_interval_frequency = 125
longer_interval_duration = 100
smaller_interval_duration = 4
sleep_time = []
#to randomly change user-agent
user_agent= ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30",
             "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
             "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
             "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
             "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
             "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
             "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)",
             "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
             "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"]

#not used now, but we can find a way to distribute the load
airbnb_ip= ['23.23.74.198',
'54.225.207.187',
'23.21.240.138',
'54.163.248.5',
'107.21.96.20',
'50.19.244.13',
'23.23.155.255',
'23.23.116.160']

airbnb = "www.airbnb.it"

old_socket = socket.socket
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
#socket.socket = socks.socksocket

def newIdentity():
    socket.socket = old_socket  # don't use proxy
    with Controller.from_port(port=9051) as controller:
        controller.authenticate() #this authentication bypass the password setted in the Tor configuration
        controller.signal(Signal.NEWNYM)
    # set up the proxy again
    socket.socket = socks.socksocket
    #uncomment the line below if you want to see the new changed ip
    print "changing identity. New ip:"
    print(urllib2.urlopen("http://www.ifconfig.me/ip").read())



def getCalendar(ids, months,smaller_interval_duration,longer_interval_duration,longer_interval_frequency ):
    #newIdentity()
    counter = 1
    #counter for longer interval
    cont =0
    current_user_agent= user_agent[random.randint(0, 12)]

    miniBreak = int (longer_interval_frequency * random.normalvariate(2,1))
    for s in ids:
        
        #every approximately 75 ids, take a longer break and change identity
        if cont == miniBreak:
            cont = 0
            miniBreak = int (longer_interval_frequency * random.normalvariate(2,1))
            time.sleep(random.normalvariate(longer_interval_duration,1))
            current_user_agent= user_agent[random.randint(0, 12)]
            print "longer break"
            #newIdentity()
        cont=cont+1
        hostURL= 'https://www.airbnb.it/api/v2/calendar_months?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=EUR&locale=en&listing_id='+str(s)+'&month=3&year=2016&count='+str(months)+'&_format=with_conditions'
        #print hostURL
        if counter==100:
            print counter
        req = urllib2.Request(hostURL
        #simulate a browser not to be blocked
        ,headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30" ,'Host' : airbnb})
        #comment above and uncomment below for changing user agent
        #,headers={'User-Agent' : current_user_agent})

        try:
            response = urllib2.urlopen(req)
            data = json.load(response)
            print data
        except urllib2.HTTPError, e:
            print e.fp.read()

        calendars[s] = data
        counter += 1
        time.sleep(random.normalvariate(smaller_interval_duration,1))
    with open('calendars.json', 'a') as outfile:
        json.dump(data, outfile)
    return

getCalendar(ids,months,smaller_interval_duration,longer_interval_duration,longer_interval_frequency)
#print counter
print 'Total Execution Time:', time.time() - start