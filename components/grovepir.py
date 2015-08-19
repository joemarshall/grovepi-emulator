import grovepi

import wx
import wx.propgrid as wxpg

class GrovePIR:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=0
        
    def title(self):
        return "D%d: Grove PIR"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove PIR"

    def initSmall(self,parent,sizer):
        self.button=wx.Button(parent,wx.ID_ANY,self.title())
        sizer.Add(self.button,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        self.button.Bind(wx.EVT_MOUSE_EVENTS,self.OnButtonMouseMove)
        self.timer=wx.Timer(self.button)
        self.button.Bind(wx.EVT_TIMER, self.onTimerFired, self.timer)
        
        
    def initPropertyPage(self,parent,sizer):
        self.propGrid=wxpg.PropertyGrid(parent, wx.ID_ANY, style=wx.propgrid.PG_SPLITTER_AUTO_CENTER| wx.propgrid.PG_AUTO_SORT)        
        self.valueProperty=wxpg.BoolProperty("Value",value=False)
        self.propGrid.Append( self.valueProperty )
        self.propGrid.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        self.propGrid.SetPropertyAttributeAll(wxpg.PG_BOOL_USE_CHECKBOX,True);
        sizer.Add(self.propGrid,flag=wx.EXPAND)
        
    def OnPropGridChange(self,event):
        if event.GetPropertyName()=="Value":
            if event.GetPropertyValue():
                self.isDetected()
            else:                
                self.setValue(False)
                stopTimer()

    def OnButtonMouseMove(self,event):
        cr=self.button.GetClientRect()
        pos=event.GetPosition()
        click=(self.button.HasCapture() or event.LeftDown())and (not event.LeftUp())
        if  click and cr.Contains(pos) and event.LeftIsDown():
            self.isDetected()
        event.Skip()
        
    def OnButtonUp(self,event):
        self.setValue(False)
        
    def update(self):
        None
        
    def isDetected(self):
        # set value to true, timer for stop
        self.setValue(True)
        self.timer.Start(5000,True)
        
    def stopTimer(self):
        self.timer.Stop()
        
    def onTimerFired(self,event):
        self.setValue(False)
        
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
            
    def onComponentDestroy(self):
        self.timer.Stop()
                