from __future__ import absolute_import
import grovepi

from gpe_utils.tkimports import *

from . import propgrid

class GenericDigital:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=tk.IntVar()
        self.needsPullup=False
        
    def title(self):
        return "D%d: Generic Digital Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Generic Digital Sensor"

    def initSmall(self,parent):    
        self.checkBox=tk.Checkbutton(parent,text=self.title(),command=self.OnCheckBoxChange,variable=self.value)
        self.checkBox.grid()
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.valueProperty=propgrid.BoolProperty("Value",value=False)
        self.needsPullupProp=propgrid.BoolProperty("Needs Pullup",value=False)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.Append( self.needsPullupProp )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()
        
    def OnPropGridChange(self,property,value):
        if property=="Value":
            self.setValue(value)
        else:
            self.needsPullup=value

    def OnCheckBoxChange(self):
        self.setValue(self.value.get())        
        
    def setValue(self,value):
        self.valueProperty.SetValue(value)
        self.value.set(value)
        if value:
            if not self.needsPullup or grovepi.outValues[self.pin]!=0:
                grovepi.digValues[self.pin]=1
        else:
            grovepi.digValues[self.pin]=0
            
    def saveConfig(self):
        return {"pullup":self.needsPullup}
        
    def loadConfig(self,conf):
        if "pullup" in conf:
            self.needsPullup=conf["pullup"]

    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.digitalRead(%d)"%self.pin,"variable":"digital%d"%self.pin}
            