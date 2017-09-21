#!/usr/bin/python

import requests
from cothread.catools import (caget, caput)

header=open("main-status-head.html", "r")
print header.read()
header.close

beami=caget('SR:C03-BI{DCCT:1}I:Total-I')
ltime=caget('SR-BI{}BPM_lifetimeAve-I')
amphrs=caget('SR:C03-BI{DCCT:1}Dosage:1d-I_')
opmode=caget('SR-OPS{}Mode-Sts')
shutmode=caget('SR-EPS{PLC:1}Sts:MstrSh-Sts')

dateandtime=caget('OP-CT{IOC:opsum}:TOD')

opmodename=["Operations", "Setup", "Studies", "Failure", "Maintenance", "Shutdown", "Unscheduled Ops"]
opModeColor=["green", "yellow", "#92D7FF", "red", "purple", "#CCCCCC", "pink"]


shutstatus=["Shutters Disabled","Shutters Enabled"]
shutcolor=["red","green"]

print '<div class="head">Beam Current: %6.2f mA</div>' % beami 

print '<div class="subhead">Beam Lifetime: %5.2f hrs</div>' % ltime
print '<div class="subhead">Daily Amp Hours: %7.1f mAh </div>' % amphrs
print '<div class="stat-line">'
print '<div class="opmode" style="background:%s">Operating Mode: %s </div><div class="shuttermode" style="background:%s" >%s</div>' % (opModeColor[opmode], opmodename[opmode], shutcolor[shutmode], shutstatus[shutmode])
print '</div></div>'
print '<div class="history-graph"><img src="status-graph.png" alt=""> </div>'
print '<div class="message-panel">'
print '<div class="ticker">Message From Operations</div>'
print '<div class="message">'
print '##OPMESSAGE-LINE1## <br/> ##OPMESSAGE-LINE2##'
print '</div>'
print '<div class="ticker">%s</div>' % dateandtime


print '</div></div></body></html>'
