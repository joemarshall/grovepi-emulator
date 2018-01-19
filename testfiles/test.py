from __future__ import print_function

import grovepi
import grovelcd
import time

grovepi.pinMode(3,"OUTPUT")

print("time,ultra,analog,digital")
while True:
    ultra=grovepi.ultrasonicRead(2)
    ana=grovepi.analogRead(0)
    digi=grovepi.digitalRead(4)
    timestamp=time.time()
    grovepi.analogWrite(3,ultra/2)
    grovelcd.setRGB(ultra/2,200-ultra/2,0)
    txt="%d - %d - %d\n wooo yay"%(ultra,digi, ana)
    grovelcd.setText(txt,False)
    print("%f,%d,%d,%d"%(timestamp,ultra,ana,digi))
    time.sleep(0.1)
