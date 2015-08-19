import grovepi
from genericanalog import *
import wx
import wx.propgrid as wxpg

class GroveLoudness(GenericAnalog):
    
    def title(self):
        return "A%d: Grove Loudness Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Loudness Sensor"

