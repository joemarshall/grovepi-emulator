import grovepi
import grovelcd
import time

grovepi.pinMode(3,"OUTPUT")

print "time,ultra,analog"
while True:
    ultra=grovepi.ultrasonicRead(2)
    ana=grovepi.analogRead(0)
    digi=grovepi.digitalRead(4)
    grovepi.analogWrite(3,ultra/2)
    grovelcd.setRGB(ultra/2,200-ultra/2,0)
    txt="%d - %d\n wooo yay"%(digi, ana)
    grovelcd.setText(txt,True)
    print "%f,%d,%d"%(time.time(),ultra,ana)
    time.sleep(0.1)
