import grovepi

import wx
import wx.propgrid as wxpg

class GenericDigital:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=0
        self.needsPullup=False
        
    def title(self):
        return "D%d: Generic Digital Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Generic Digital Sensor"

    def initSmall(self,parent,sizer):
        self.checkBox=wx.CheckBox(parent,wx.ID_ANY,self.title())
        sizer.Add(self.checkBox,flag=wx.EXPAND|wx.CENTER,proportion=1)
        self.checkBox.Bind(wx.EVT_CHECKBOX,self.OnCheckBoxChange)
        
    def initPropertyPage(self,parent,sizer):
        self.propGrid=wxpg.PropertyGrid(parent, wx.ID_ANY, style=wx.propgrid.PG_SPLITTER_AUTO_CENTER| wx.propgrid.PG_AUTO_SORT)        
        self.valueProperty=wxpg.BoolProperty("Value",value=False)
        self.needsPullupProp=wxpg.BoolProperty("Needs Pullup",value=False)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.Append( self.needsPullupProp )
        self.propGrid.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        self.propGrid.SetPropertyAttributeAll(wxpg.PG_BOOL_USE_CHECKBOX,True);
        sizer.Add(self.propGrid,flag=wx.EXPAND)
        
    def OnPropGridChange(self,event):
        if event.GetPropertyName()=="Value":
            self.setValue(event.GetPropertyValue())
        else:
            self.needsPullup=event.GetPropertyValue()

    def OnCheckBoxChange(self,event):
        self.setValue(event.IsChecked())
        
    def setValue(self,value):
        self.valueProperty.SetValue(value)
        self.checkBox.SetValue (value)
        if value:
            if not self.needsPullup or grovepi.outValues[self.pin]!=0:
                grovepi.digValues[self.pin]=1
        else:
            grovepi.digValues[self.pin]=0
            
    def saveConfig(self):
        return {"pullup":self.needsPullup}
        
    def loadConfig(self,conf):
        if conf.has_key("pullup"):
            self.needsPullup=conf["pullup"]
                