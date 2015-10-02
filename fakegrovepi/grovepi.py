import threading
import math

digValues={}# digital input values (or 2 ---> 300 for ultrasonic distances)
anaValues={} 
# 0 = input
pinModes={}
# what is written to it (or pull up if in input mode) - in 0 - 255 form
outValues={}


# check for this if your code has to know whether it is in the emulator
IS_EMULATOR=True

def digitalWrite(pin, value):
  outValues[pin]=value*255
  
def analogWrite(pin,value):
    if pinModes[pin]=="INPUT":
        print "Error, trying to analog write to pin set as INPUT"
    if pin!=3 and pin!=5 and pin!=6:
        print "Can't analog write on pins other than 3,5 or 6"
    else:
        outValues[pin]=value
  
def digitalRead(pin):
  if pinModes[pin]=="INPUT":  
    if digValues[pin]>1:
        print "Error, trying to digital read from ultrasonic transducer"
        return 0
    return digValues[pin]
  else:
    print "Error, trying to read from pin set to output: %d"%pin
    print "Pinmodes:",pinModes
    return 0

def analogRead(pin):
  return anaValues[pin]

def ultrasonicRead(pin):
    if digValues[pin]<=1:
        print "Error, trying to ultrasonic read from normal digital sensor"
        return 0
    return digValues[pin]-2
  
def temp(pin):
    a=analogRead(pin)
    resistance=(float)(1023-a)*10000/a
    t=(float)(1/(math.log(resistance/10000)/3975+1/298.15)-273.15) 
    return t
  
  
def pinMode(pin,mode):
  pinModes[pin]=mode
  
for c in range(0,9):
  digValues[c]=0
  anaValues[c]=0
  pinModes[c]="INPUT"
  outValues[c]=0
              