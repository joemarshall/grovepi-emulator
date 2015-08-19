import grovepi

import wx
import wx.propgrid as wxpg

import bisect

SHORT_LOOKUP=[]
for c in range(1,1023):
    resistance= (1023-float(c))*(10/float(c))
    lux = 10000.0 / ( pow((resistance*10.0),(4.0/3.0)));
    SHORT_LOOKUP.append(lux)
LIGHT_LOOKUP=[SHORT_LOOKUP[0]]
LIGHT_LOOKUP.extend(SHORT_LOOKUP)
LIGHT_LOOKUP.append(SHORT_LOOKUP[-1])


class GroveLight:
        
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=0
        self.needsPullup=False
        
    def title(self):
        return "A%d: Grove Light Sensor"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Light Sensor"

    def initSmall(self,parent,sizer):
        self.label=wx.StaticText(parent,wx.ID_ANY,self.title(),style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        sizer.Add(self.label,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=0)        
        self.slider=wx.Slider(parent,wx.ID_ANY,minValue=0,maxValue=1023,value=512)
        sizer.Add(self.slider,flag=wx.EXPAND|wx.CENTER,proportion=1)
        self.slider.Bind(wx.EVT_SLIDER,self.OnSliderChange)
        
    def initPropertyPage(self,parent,sizer):
        self.propGrid=wxpg.PropertyGrid(parent, wx.ID_ANY, style=wx.propgrid.PG_SPLITTER_AUTO_CENTER| wx.propgrid.PG_AUTO_SORT)        
        self.valueProperty=wxpg.FloatProperty("Lux",value=LIGHT_LOOKUP[512])
        self.propGrid.Append( self.valueProperty )
        self.rawValueProperty=wxpg.IntProperty("Raw",value=512)
        self.propGrid.Append( self.rawValueProperty )
        self.propGrid.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        sizer.Add(self.propGrid,flag=wx.EXPAND)
        
    def OnPropGridChange(self,event):
        if event.GetPropertyName()=="Raw":
            self.setValue(event.GetPropertyValue())
        else:
            self.setValueR(event.GetPropertyValue())

    def OnSliderChange(self,event):
        self.setValue(event.GetInt())
        
    def setValueR(self,cVal):
        valueSlider=bisect.bisect_left(LIGHT_LOOKUP,cVal)
        self.setValue(valueSlider)
        
    def setValue(self,value):
        if value>1023: value=1023
        if value<0:value=0
        self.valueProperty.SetValue(LIGHT_LOOKUP[value])
        self.rawValueProperty.SetValue (value)
        self.slider.SetValue (value)
        grovepi.anaValues[self.pin]=value
                