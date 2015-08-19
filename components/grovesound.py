import grovepi
from genericanalog import *
import wx
import wx.propgrid as wxpg

class GroveSound(GenericAnalog):
    
    def title(self):
        return "A%d: Grove Sound Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Sound Sensor"

