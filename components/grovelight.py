from __future__ import absolute_import
import grovepi

from .genericanalog import *

import bisect

SHORT_LOOKUP=[]
for c in range(1,1023):
    resistance= (1023-float(c))*(10/float(c))
    lux = 10000.0 / ( pow((resistance*10.0),(4.0/3.0)));
    SHORT_LOOKUP.append(lux)
LIGHT_LOOKUP=[SHORT_LOOKUP[0]]
LIGHT_LOOKUP.extend(SHORT_LOOKUP)
LIGHT_LOOKUP.append(SHORT_LOOKUP[-1])


class GroveLight(GenericAnalog):
        
    def __init__(self,inputNum):
        GenericAnalog.__init__(self,inputNum)
        self.value.set(512)
        
    def title(self):
        return "A%d: Grove Light Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Light Sensor"
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.valueProperty=propgrid.FloatProperty("Lux",value=LIGHT_LOOKUP[512])
        self.propGrid.Append( self.valueProperty )
        self.rawValueProperty=propgrid.IntProperty("Raw",value=0)
        self.propGrid.Append( self.rawValueProperty )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()
        
    def OnPropGridChange(self,property,value):
        if property=="Raw":
            self.setValue(value)
        else:
            self.setValueR(value)
        
    def OnSliderChange(self,event):
        self.setValue(self.value.get())
        
    def setValueR(self,cVal):
        valueSlider=bisect.bisect_left(LIGHT_LOOKUP,cVal)
        self.setValue(valueSlider)
        
    def setValue(self,value):
        if value>1023: value=1023
        if value<0:value=0
        self.valueProperty.SetValue(LIGHT_LOOKUP[value])
        self.rawValueProperty.SetValue (value)
        self.value.set(value)
        grovepi.anaValues[self.pin]=value
                
    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.analogRead(%d)"%self.pin,"variable":"light%d"%self.pin}
                