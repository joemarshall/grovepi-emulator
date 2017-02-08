from __future__ import absolute_import
import grovepi

from .genericdigital import *

class GroveButton(GenericDigital):
    
    def __init__(self,inputNum):
        GenericDigital.__init__(self,inputNum)
        
    def title(self):
        return "D%d: Grove Push Button"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Button"

    def initSmall(self,parent):
        self.button=tk.Button(parent,text=self.title(),bg="red",activebackground="green")
        self.button.bind("<ButtonRelease-1>",self.OnButtonUp)
        self.button.bind("<Button-1>",self.OnButtonDown)
        self.button.pack()
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.valueProperty=propgrid.BoolProperty("Value",value=False)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()
        
    def OnPropGridChange(self,property,value):
        if property=="Value":
            self.setValue(value)

    def OnButtonDown(self,event):
        self.setValue(True)
            
    def OnButtonUp(self,event):
        self.setValue(False)
        
    def update(self):
        None
        
    def setValue(self,value):
        self.valueProperty.SetValue(value)
        if value:
            self.button.config(bg="green",activebackground="green")
        else:
            self.button.config(bg="red")
        if value:
            grovepi.digValues[self.pin]=1
        else:
            grovepi.digValues[self.pin]=0

    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.digitalRead(%d)"%self.pin,"variable":"button%d"%self.pin}

            