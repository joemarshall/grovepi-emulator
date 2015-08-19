import grovepi

import wx
import wx.propgrid as wxpg

class GroveUltrasonic:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=0
        grovepi.digValues[self.pin]=2 # tell grovepi that we are an ultrasonic ranger
        
    def title(self):
        return "D%d: Grove Ultrasonic Ranger"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Ultrasonic Ranger"

    def initSmall(self,parent,sizer):
        self.label=wx.StaticText(parent,wx.ID_ANY,self.title(),style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        sizer.Add(self.label,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=0)
        self.slider=wx.Slider(parent,wx.ID_ANY,minValue=0,maxValue=400,value=0)
        sizer.Add(self.slider,flag=wx.EXPAND|wx.CENTER,proportion=1)
        self.slider.Bind(wx.EVT_SLIDER,self.OnSliderChange)
        
    def initPropertyPage(self,parent,sizer):
        self.propGrid=wxpg.PropertyGrid(parent, wx.ID_ANY, style=wx.propgrid.PG_SPLITTER_AUTO_CENTER| wx.propgrid.PG_AUTO_SORT)        
        self.valueProperty=wxpg.IntProperty("Value",value=False)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        sizer.Add(self.propGrid,flag=wx.EXPAND)
        
    def OnPropGridChange(self,event):
        if event.GetPropertyName()=="Value":
            self.setValue(event.GetPropertyValue())

    def OnSliderChange(self,event):
        self.setValue(event.GetInt())
        
    def setValue(self,value):
        if value>400: value=400
        if value<0:value=0
        self.valueProperty.SetValue(value)
        self.slider.SetValue (value)
        grovepi.digValues[self.pin]=value+2
                