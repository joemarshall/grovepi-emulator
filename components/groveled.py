import grovepi
import wx
import wx.propgrid as wxpg

class GroveLED:
    
    def __init__(self,pin):
        self.pin=pin
        self.colour=wx.Colour(255,0,0)
    
    def title(self):
        return "D%d: Grove LED:"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove LED"
    
    def initSmall(self,parent,sizer):
        self.label=wx.StaticText(parent,wx.ID_ANY,self.title(),style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        sizer.Add(self.label,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
    
    def initPropertyPage(self,parent,sizer):
        self.propGrid=wxpg.PropertyGrid(parent, wx.ID_ANY, style=wxpg.PG_SPLITTER_AUTO_CENTER| wxpg.PG_AUTO_SORT)        
        self.valueProperty=wxpg.ColourProperty("Colour",value=self.colour)
        self.propGrid.Append( self.valueProperty )
        sizer.Add(self.propGrid,flag=wx.EXPAND)
        self.propGrid.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )

    def OnPropGridChange(self,event):
        self.colour=event.GetPropertyValue()
        
    def update(self):
        value=grovepi.outValues[self.pin]
        valueColour=wx.Colour(self.colour.Red()*value / 255,self.colour.Green()*value / 255,self.colour.Blue()*value / 255)
        self.label.SetBackgroundColour(valueColour)
        if value<128:
            self.label.SetForegroundColour(wx.Colour(255,255,255))
        else:
             self.label.SetForegroundColour(wx.Colour(0,0,0))
        self.label.SetLabel("%s:%3.3d"%(self.title(),value))

    def saveConfig(self):
        return {"r":self.colour.Red(),"g":self.colour.Green(),"b":self.colour.Blue()}
        
    def loadConfig(self,conf):
        if conf.has_key("r") and conf.has_key("g") and conf.has_key("b"):
            self.colour=wx.Colour(conf["r"],conf["g"],conf["b"])
