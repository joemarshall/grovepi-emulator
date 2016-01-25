import grovepi
from genericanalog import *

class GroveLoudness(GenericAnalog):
    
    def title(self):
        return "A%d: Grove Loudness Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Loudness Sensor"

