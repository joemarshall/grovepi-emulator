from __future__ import absolute_import
import grovepi
from .genericanalog import *

class GroveLoudness(GenericAnalog):
    
    def title(self):
        return "A%d: Grove Loudness Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Loudness Sensor"

    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.analogRead(%d)"%self.pin,"variable":"loudness%d"%self.pin}
