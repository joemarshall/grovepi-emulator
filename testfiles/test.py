import grovepi
import grovelcd
from time import sleep

grovepi.pinMode(3,"OUTPUT")



while True:
    grovepi.analogWrite(3,grovepi.ultrasonicRead(2)/2)
#    grovepi.analogWrite(3,(grovepi.digitalRead(2)*128 + grovepi.digitalRead(4)*127)|(grovepi.analogRead(0)/4))
    sleep(0.1)
    grovelcd.setRGB(grovepi.ultrasonicRead(2)/2,200-grovepi.ultrasonicRead(2)/2,0)
    grovelcd.setText("%d - %d\n wooo yay"%(grovepi.digitalRead(4), grovepi.analogRead(0)),True)
