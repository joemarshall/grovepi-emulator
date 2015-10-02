import grovenfctag
import wx
import wx.grid
import wx.propgrid as wxpg

class HexValidator(wx.PyValidator): 
   def __init__(self): 
      wx.PyValidator.__init__(self) 
      wx.EVT_CHAR(self, self.OnChar) 

   def Clone(self): 
      return HexValidator() 

   def Validate(self, win): 
      tc = wxPyTypeCast(win, "wxTextCtrl") 
      val = tc.GetValue() 
      for x in val: 
         if x not in "0123456789abcdefABCDEF": 
            return false 
      return true 

   def OnChar(self, event): 
      key = event.KeyCode
      if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255: 
         event.Skip() 
         return 
      if chr(key) in "0123456789abcdefABCDEF": 
         event.Skip() 
         return 
#      if not wxValidator_IsSilent(): 
#         wxBell() 
      return 

class HexTextCtrl(wx.TextCtrl): 
    def __init__(self,parent,id,text): 
        wx.TextCtrl.__init__(self,parent, id, text,validator = HexValidator(), 
                             style=wx.TE_PROCESS_ENTER) 
        self.SetInsertionPoint(0) 
        self.SetMaxLength(2) 
        #self.Bind(wx.EVT_TEXT, self.OnText) 
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown) 
#        self.parentgrid=parentgrid 
        self.userpressed=False 

    def OnKeyDown(self, evt): 
        self.userpressed=True 
        evt.Skip() 

    def OnText(self, evt): 
        if len(evt.GetString())>=2 and self.userpressed: 
            self.userpressed=False 
#            wx.CallAfter(self.parentgrid.advanceCursor) 

class GroveNFCTagModule:


    
    def __init__(self,pin):
        self.pin=pin
    
    def title(self):
        return "I2C-%d: Grove NFC Tag:"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove NFC Tag"
    
    def initSmall(self,parent,sizer):
        self.titleLabel=wx.StaticText(parent,wx.ID_ANY,self.title(),style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        self.blockSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.blockLabel=wx.StaticText(parent,wx.ID_ANY,"Block address: 0x")
        self.blockEdit=wx.TextCtrl(parent,wx.ID_ANY,"0",validator = HexValidator())
        self.blockSizer.Add(self.blockLabel)
        self.blockSizer.Add(self.blockEdit)
        self.dataGrid=wx.GridSizer(4,4)
        oldFont=self.blockEdit.GetFont()
        newFont=wx.Font(oldFont.PointSize,wx.FONTFAMILY_TELETYPE,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.blockEdit.SetFont(newFont)
        self.dataPoints=[]
        for c in range(0,16):
            dataPointEdit=wx.TextCtrl(parent,wx.ID_ANY,"00",validator = HexValidator())
            dataPointEdit.Bind(wx.EVT_TEXT,lambda evt, temp=c: self.OnDataPointChanged(evt, temp) )
            dataPointEdit.SetFont(newFont)
            dataPointEdit.SetMaxLength(2)
            dataPointEdit.SetMinSize((dataPointEdit.GetTextExtent("0000")[0],-1))
            self.dataGrid.Add(dataPointEdit)
            self.dataPoints.append(dataPointEdit)
        sizer.Add(self.titleLabel,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        sizer.Add(self.blockSizer,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        sizer.Add(self.dataGrid)
    
        
    def OnDataPointChanged(self,event,pos):
        try:        
            blockAddress=int(self.blockEdit.GetValue(),16)
        except ValueError:
            blockAddress=0
        grovenfctag.NFCBuffer[blockAddress+pos]=int(event.GetString(),16)
        
    def update(self):
        try:        
            blockAddress=int(self.blockEdit.GetValue(),16)
        except ValueError:
            blockAddress=0
        for c in self.dataPoints:
            if not c.HasFocus() and c.GetValue()!="%02X"%grovenfctag.NFCBuffer[blockAddress]:
                c.SetValue("%02X"%grovenfctag.NFCBuffer[blockAddress])
            blockAddress+=1
                # set text if it isn't active
