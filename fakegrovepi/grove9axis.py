from math import *
import time

gyroVals=[0,0,0]
accVals=[0,0,0]
magVals=[0,0,0]

def getAccel():
    time.sleep(0.0054553399086) # simulate sensor delay
    return tuple(accVals)

def getGyro():
    time.sleep(0.0054553399086) # simulate sensor delay
    return tuple(gyroVals)

def getMag():
    time.sleep(0.0054553399086) # simulate sensor delay
    return tuple(magVals)
