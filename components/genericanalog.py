from __future__ import absolute_import
import grovepi

from gpe_utils.tkimports import *
from . import propgrid

class GenericAnalog:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=tk.IntVar()
        
    def title(self):
        return "A%d: Generic Analog Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Generic Analog Sensor"

    def initSmall(self,parent):
        self.label=tk.Label(parent,text=self.title())
        self.label.grid()
        self.slider=tk.Scale(parent,from_=0,to=1024,orient=tk.HORIZONTAL,command=self.OnSliderChange,variable=self.value)
        self.slider.grid()
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.valueProperty=propgrid.IntProperty("Value",value=0)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()
        
    def OnPropGridChange(self,property,value):
        if property=="Value":
            self.setValue(value)

    def OnSliderChange(self,event):
        self.setValue(self.value.get())
        
    def setValue(self,value):
        if value>1023: value=1023
        if value<0:value=0
        self.valueProperty.SetValue(value)
        self.value.set(value)
        grovepi.anaValues[self.pin]=value
        
    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.analogRead(%d)"%self.pin,"variable":"analog%d"%self.pin}
                