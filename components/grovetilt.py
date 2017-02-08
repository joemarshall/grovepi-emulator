from __future__ import absolute_import
import grovepi

from . import propgrid

from .genericdigital import *


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

    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.digitalRead(%d)"%self.pin,"variable":"tilt%d"%self.pin}
        