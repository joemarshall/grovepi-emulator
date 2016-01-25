import grovepi
from genericanalog import *

class GroveSound(GenericAnalog):
    
    def title(self):
        return "A%d: Grove Sound Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Sound Sensor"

