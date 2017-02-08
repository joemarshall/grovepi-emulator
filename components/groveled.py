from __future__ import absolute_import
import grovepi

from gpe_utils.tkimports import *
from . import propgrid


class GroveLED:
    
    def __init__(self,pin):
        self.pin=pin
        self.colour=(255,0,0)
    
    def title(self):
        return "D%d: Grove LED:"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove LED"
    
    def initSmall(self,parent):
        self.label=tk.Label(parent,text=self.title())
        self.label.grid()
    
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.valueProperty=propgrid.ColourProperty("Colour",value=self.colour)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()

    def OnPropGridChange(self,property,value):
        self.colour=value
        
    def getColourName(self,rgb):
        return "#%02x%02x%02x"%rgb
        
    def update(self):
        value=grovepi.outValues[self.pin]
        valueColour=(self.colour[0]*value / 255,self.colour[1]*value / 255,self.colour[2]*value / 255)
        self.label.config(bg=self.getColourName(valueColour))
        if value<128:
            self.label.config(fg="white")
        else:
            self.label.config(fg="black")
        self.label.config(text="%s:%3.3d"%(self.title(),value))

    def saveConfig(self):
        return {"r":self.colour[0],"g":self.colour[1],"b":self.colour[2]}
        
    def loadConfig(self,conf):
        if "r" in conf and "g" in conf and "b" in conf:
            self.colour=(conf["r"],conf["g"],conf["b"])
