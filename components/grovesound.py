from __future__ import absolute_import
import grovepi
from .genericanalog import *

class GroveSound(GenericAnalog):
    
    def title(self):
        return "A%d: Grove Sound Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Sound Sensor"

    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.analogRead(%d)"%self.pin,"variable":"sound%d"%self.pin}
