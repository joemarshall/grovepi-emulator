import grovepi

import wx
import wx.propgrid as wxpg

class GroveButton:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=0
        
    def title(self):
        return "D%d: Grove Push Button"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Button"

    def initSmall(self,parent,sizer):
        self.button=wx.Button(parent,wx.ID_ANY,self.title())
        sizer.Add(self.button,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        self.button.Bind(wx.EVT_MOUSE_EVENTS,self.OnButtonMouseMove)
        
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

    def OnButtonMouseMove(self,event):
        cr=self.button.GetClientRect()
        pos=event.GetPosition()
        click=(self.button.HasCapture() or event.LeftDown())and (not event.LeftUp())
        if  click and cr.Contains(pos) and event.LeftIsDown():
            self.setValue(True)
        else:
            self.setValue(False)
        event.Skip()
        
    def OnButtonUp(self,event):
        self.setValue(False)
        
    def update(self):
        None
        
    def setValue(self,value):
        self.valueProperty.SetValue(value)
        if value:
            self.button.SetBackgroundColour(wx.Colour(0,255,0))
        else:
            self.button.SetBackgroundColour(wx.Colour(255,0,0))
        if value:
            grovepi.digValues[self.pin]=1
        else:
            grovepi.digValues[self.pin]=0
                