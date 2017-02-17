from __future__ import absolute_import
import grovepi

from gpe_utils.tkimports import *
from . import propgrid

class GroveUltrasonic:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=tk.IntVar()
        grovepi.digValues[self.pin]=2 # tell grovepi that we are an ultrasonic ranger
        
    def title(self):
        return "D%d: Grove Ultrasonic Ranger"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Ultrasonic Ranger"

    def initSmall(self,parent):
        self.label=tk.Label(parent,text=self.title())
        self.label.grid()
        self.slider=tk.Scale(parent,from_=0,to=400,orient=tk.HORIZONTAL,command=self.OnSliderChange,variable=self.value)
        self.slider.grid()
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.valueProperty=propgrid.IntProperty("Distance (cm)",value=0)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()
        
    def OnPropGridChange(self,property,value):
        if property=="Distance (cm)":
            self.setValue(value)

    def OnSliderChange(self,event):
        self.setValue(self.value.get())
        
    def setValue(self,value):
        if value>400: value=400
        if value<0:value=0
        self.valueProperty.SetValue(value)
        self.value.set(value)
        grovepi.digValues[self.pin]=value+2

    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.ultrasonicRead(%d)"%self.pin,"variable":"ultra%d"%self.pin}

        