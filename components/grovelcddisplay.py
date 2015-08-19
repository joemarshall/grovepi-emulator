import grovelcd
import wx
import wx.propgrid as wxpg

class GroveLCDDisplay:
    
    def __init__(self,pin):
        self.pin=pin
        self.colour=wx.Colour(255,0,0)
    
    def title(self):
        return "I2C-%d: Grove LCD 2 line RGB:"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove LCD 2 line (RGB)"
    
    def initSmall(self,parent,sizer):
        self.titleLabel=wx.StaticText(parent,wx.ID_ANY,self.title(),style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        self.label=wx.StaticText(parent,wx.ID_ANY,"                \n                ",style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        oldFont=self.label.GetFont()
        newFont=wx.Font(oldFont.PointSize,wx.FONTFAMILY_TELETYPE,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.label.SetFont(newFont)
        sizer.Add(self.titleLabel,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        sizer.Add(self.label,flag=wx.ALIGN_CENTER,proportion=1)
    
#    def initPropertyPage(self,parent,sizer):
#        self.propGrid=wxpg.PropertyGrid(parent, wx.ID_ANY, style=wxpg.PG_SPLITTER_AUTO_CENTER| wxpg.PG_AUTO_SORT)        
#        self.valueProperty=wxpg.ColourProperty("Colour",value=self.colour)
#        self.propGrid.Append( self.valueProperty )
#        sizer.Add(self.propGrid,flag=wx.EXPAND)
#        self.propGrid.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )

    def OnPropGridChange(self,event):
        self.colour=event.GetPropertyValue()
        
    def update(self):
        text=grovelcd.curLCDText
        colour=grovelcd.curRGB
        line1="".join(text[0:16])
        line2="".join(text[16:32])
        self.label.SetBackgroundColour(wx.Colour(*colour))
        self.label.SetLabel("%s\n%s"%(line1,line2))
