#!/usr/bin/python

import requests
from cothread.catools import (caget, caput)
import random
import csv
import matplotlib.pyplot as plt
import urllib2
from datetime import datetime as dt, timedelta
import numpy as np
import matplotlib.dates as mdates


# Set the time for the graph to one day 

dago=dt.now() - timedelta (days=1)
dago.isoformat()


# Initialize the lists for plotting

xlist=[]
ylist=[]
x1list=[]
y1list=[]


#Set up the URLs to get the data from the archiver in CSV format

beamdata='http://arcapp01.cs.nsls2.local:17668/retrieval/data/getData.csv?pv=mean_360(SR:C03-BI{DCCT:1}I:Real-I)&from=' + dago.isoformat() + 'Z'
ltdata='http://arcapp01.cs.nsls2.local:17668/retrieval/data/getData.csv?pv=mean_360(SR:OPS-BI{DCCT:1}Lifetime-I)&from=' + dago.isoformat() + 'Z'


#Get the current data - chop it up and put it into lists

response = urllib2.urlopen(beamdata)
htmlin= response.read()

datain=htmlin.rstrip()

datalines=datain.split('\n')



for dlines in datalines:
	if dlines.find(','):
		x=float(dlines.split(',')[0])
		y=(dlines.split(',')[1])
		tstamp=dt.fromtimestamp(x)
		xlist.append(tstamp)
		ylist.append(y)





response = urllib2.urlopen(ltdata)
htmlin= response.read()

datain=htmlin.rstrip()


#Get the Lifetime data - chop it up and put it into lists

datalines=datain.split('\n')


for dlines in datalines:
	if dlines.find(','):
		x=float(dlines.split(',')[0])
		y=(dlines.split(',')[1])
		tstamp=dt.fromtimestamp(x)
		x1list.append(tstamp)
		y1list.append(y)




#Begin the Matplotlib stuff


fig, ax1 = plt.subplots(figsize=(8,4))


ax1.plot(xlist,ylist,'bo')
ax1.set_xlabel('time')

# Make the y-axis label, ticks and tick labels match the line color.

ax1.set_ylabel('Current (mA)', color='b')
ax1.set_ylim([0, 400])

max_xticks = 6
xloc = plt.MaxNLocator(max_xticks)
ax1.xaxis.set_major_locator(xloc)
myFmt = mdates.DateFormatter('%H')
ax1.xaxis.set_major_formatter(myFmt)


ax2 = ax1.twinx()
ax2.plot(xlist, y1list, 'r.')
ax2.set_ylabel('Lifetime (hrs)', color='r')
ax2.tick_params('y', colors='r')
ax2.set_ylim([0, 30])

ax2.xaxis.set_major_locator(xloc)
ax2.xaxis.set_major_formatter(myFmt)

plt.savefig("status-history.png")


# Now the HTML for the page itself

# Open the HTML header and send it to STDOUT
header=open("main-status-head.html", "r")
print header.read()
header.close


#Get the PVs for the page

beami=caget('SR:C03-BI{DCCT:1}I:Total-I')
ltime=caget('SR-BI{}BPM_lifetimeAve-I')
amphrs=caget('SR:C03-BI{DCCT:1}Dosage:1d-I_')
opmode=caget('SR-OPS{}Mode-Sts')
shutmode=caget('SR-EPS{PLC:1}Sts:MstrSh-Sts')
opline1=caget('OP{1}Message')
opline2=caget('OP{2}Message')

#Intialize the Message Strings

message1=""
message2=""

#Turn the arrays of characters into Message strings

for item in opline1:
	message1=message1+chr(item)

for item in opline2:
	message2=message2+chr(item)

dateandtime=caget('OP-CT{IOC:opsum}:TOD')

#Set up the lists for the various machine states and colors

opmodename=["Operations", "Setup", "Studies", "Failure", "Maintenance", "Shutdown", "Unscheduled Ops"]
opModeColor=["green", "yellow", "#92D7FF", "red", "purple", "#CCCCCC", "pink"]


shutstatus=["Shutters Disabled","Shutters Enabled"]
shutcolor=["red","green"]

#Output the HTML to STDOUT

print '<div class="head">Beam Current: %6.2f mA</div>' % beami 

print '<div class="subhead">Beam Lifetime: %5.2f hrs</div>' % ltime
print '<div class="subhead">Daily Amp Hours: %7.1f mAh </div>' % amphrs
print '<div class="stat-line">'
print '<div class="opmode" style="background:%s">Operating Mode: %s </div><div class="shuttermode" style="background:%s" >%s</div>' % (opModeColor[opmode], opmodename[opmode], shutcolor[shutmode], shutstatus[shutmode])
print '</div></div>'
print '<div class="history-graph"><img src="status-history.png" alt=""> </div>'
print '<div class="message-panel">'
print '<div class="ticker">Message From Operations</div>'
print '<div class="message">'
print '%s <br/> %s' % (message1,message2)
print '</div>'
print '<div class="ticker">%s</div>' % dateandtime


print '</div></div></body></html>'
