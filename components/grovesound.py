
import grovepi
from .genericanalog import *

class GroveSound(GenericAnalog):
    
    def title(self):
        return "A%d: Grove Sound Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Sound Sensor"

    def getCSVCode(self):
        return {"imports":["sensors"],"pin_mappings":["\"sound%d\":%d"%(self.pin,self.pin)],"reader":"sensors.sound%d.get_level()"%self.pin,"variable":"sound%d"%self.pin}
