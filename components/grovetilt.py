import grovepi

import wx
import wx.propgrid as wxpg

class GroveTilt:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=0
        
    def title(self):
        return "D%d: Grove Tilt Switch"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Tilt Switch"

    def initSmall(self,parent,sizer):
        self.button=wx.ToggleButton(parent,wx.ID_ANY,self.title())
        sizer.Add(self.button,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        self.button.Bind(wx.EVT_TOGGLEBUTTON,self.OnButton)
        self.button.SetBackgroundColour(wx.Colour(0,255,0))
        
    def initPropertyPage(self,parent,sizer):
        self.propGrid=wxpg.PropertyGrid(parent, wx.ID_ANY, style=wx.propgrid.PG_SPLITTER_AUTO_CENTER| wx.propgrid.PG_AUTO_SORT)        
        self.valueProperty=wxpg.BoolProperty("Value",value=False)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        self.propGrid.SetPropertyAttributeAll(wxpg.PG_BOOL_USE_CHECKBOX,True);
        sizer.Add(self.propGrid,flag=wx.EXPAND)
        
    def OnPropGridChange(self,event):
        if event.GetPropertyName()=="Value":
            self.setValue(event.GetPropertyValue())
            
    def OnButton(self,event):
        self.setValue(self.button.GetValue())
        
    def update(self):
        None
        
    def setValue(self,value):
        self.valueProperty.SetValue(value)
        self.button.SetValue(value)
        if value:
            self.button.SetBackgroundColour(wx.Colour(0,255,0))
        else:
            self.button.SetBackgroundColour(wx.Colour(255,0,0))
        if value:
            grovepi.digValues[self.pin]=1
        else:
            grovepi.digValues[self.pin]=0
                