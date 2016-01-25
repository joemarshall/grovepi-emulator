import grovepi

import wx
import wx.propgrid as wxpg

from genericdigital import *


class GroveTilt(GenericDigital):
    
    def __init__(self,inputNum):
        GenericDigital.__init__(self,inputNum)
        
    def title(self):
        return "D%d: Grove Tilt Switch"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Tilt Switch"

    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.valueProperty=propgrid.BoolProperty("Value",value=False)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()
                