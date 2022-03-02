
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
        # todo
        self.button=ttk.Button(parent,text=self.title(),style='LightUp.TButton')
        self.button.bind("<ButtonRelease-1>",self.OnButtonUp)
        self.button.bind("<Button-1>",self.OnButtonDown)
        self.button.pack()
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.valueProperty=propgrid.BoolProperty("Value",value=False)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack(fill=tk.X)
        
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
            grovepi.digValues[self.pin]=1
        else:
            grovepi.digValues[self.pin]=0

    def getCSVCode(self):
        return {"imports":["sensors"],"pin_mappings":["\"button%d\":%d"%(self.pin,self.pin)],"reader":"sensors.button%d.get_level()"%self.pin,"variable":"button%d"%self.pin}

            