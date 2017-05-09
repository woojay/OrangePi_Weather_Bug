#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 15:35:28 2017

@author: woojay
#echo 1 > /sys/class/leds/red_led/brightness
"""

from forecastiopy import *
from datetime import datetime
from subprocess import call
from time import sleep

delaySec = 5
blinkPerMinute = int(60 / (delaySec+1))
checkPeriodMinutes = 10

precipCount = 0
oPi = False

fio = ForecastIO.ForecastIO('YOUR DARK SKY API KEY HERE', latitude=16.775833, longitude=-3.009444)
currently = FIOCurrently.FIOCurrently(fio)

print('Latitude '+str(fio.latitude)+' Longitude '+str(fio.longitude))
print('Timezone '+str(fio.timezone)+' Offset '+str(fio.offset))

timeNow = datetime.fromtimestamp(int(currently.time)).strftime('%Y-%m-%d %H:%M:%S')
hourNow = int(timeNow[11:13])
print('Time now: '+str(timeNow))

while True:
    for mainLoop in range(0, checkPeriodMinutes):
        if fio.has_hourly() is True:
            hourly = FIOHourly.FIOHourly(fio)
            print(hourly.summary)
            print('\nToday')
            
            #for hour in range(0, hourly.hours()):
            for hour in range(0, 12):
                tempHour = int(hourNow + hour )
                tempPrecip = hourly.get_hour(hour)['precipProbability']
                
                if (tempHour == 24):
                    print('Tomorrow')
                elif (tempHour == 48):
                    print('Day after Tomorrow')
                    
                print('Hour '+'{:2d}'.format(tempHour % 24)+ ' %: '+'{:.2f}'.format(tempPrecip)+' '+str(hourly.get_hour(hour)['summary']))
                if ((hour <= 12) and (tempPrecip >= 0.1)):
                    precipCount += 1
        
            print('\nNo. of recipitable hour blocks: '+str(precipCount))
            
            if (oPi):
                call("echo 0 > /sys/class/leds/red_led/brightness", shell=True)
            
                for i in range(0, blinkPerMinute * checkPeriodMinutes):
                    for each in range(0, precipCount):
                        call("echo 1 > /sys/class/leds/red_led/brightness", shell=True)
                        sleep(0.1)
                        call("echo 0 > /sys/class/leds/red_led/brightness", shell=True)
                        sleep(0.1)
                   
                    sleep(delaySec)
            else:
                sleep(checkPeriodMinutes * 60)
        else:
            print('No Hourly data')
            if (oPi):
                call("echo 1 > /sys/class/leds/red_led/brightness", shell=True)
    
        fio = ForecastIO.ForecastIO('YOUR DARK SKY API KEY HERE', latitude=16.775833, longitude=-3.009444)
        currently = FIOCurrently.FIOCurrently(fio)
        timeNow = datetime.fromtimestamp(int(currently.time)).strftime('%Y-%m-%d %H:%M:%S')
        hourNow = int(timeNow[11:13])
        precipCount = 0
        print('New Time now: '+str(timeNow))
