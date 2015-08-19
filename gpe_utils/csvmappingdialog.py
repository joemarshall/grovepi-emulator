import wx

class CSVMappingDlg(wx.Dialog):
    
    def __init__(self, parent,csvColumns,components,lastMapping):
        super(CSVMappingDlg, self).__init__(parent) 
        
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        #  need a time column
        self.timeCombo=wx.ComboBox(self.panel,style=wx.CB_READONLY)
        self.timeCombo.AppendItems(csvColumns)
        
        self.combos=[]
        self.mapping={}
        self.timeColumn=None
        

        st=wx.StaticText(self.panel,label="Time column (required)")
        st.SetBackgroundColour((0,0,0))
        st.SetForegroundColour((255,255,255))
        vbox.Add(st)
        vbox.Add(self.timeCombo)
        
        
        sensorCombo={}
        for comp in components:
            if hasattr(comp,"setValue"):
                st=wx.StaticText(self.panel,label=comp.title())
                st.SetBackgroundColour((0,0,0))
                st.SetForegroundColour((255,255,255))

                vbox.Add(st,flag=wx.RIGHT|wx.LEFT|wx.EXPAND,border=5)
                if hasattr(comp,"getNumAxes"):
                    for c in range(0,comp.getNumAxes()):
                        st=wx.StaticText(self.panel,label=comp.getAxisName(c))
                        vbox.Add(st,flag=wx.LEFT|wx.RIGHT|wx.EXPAND,border=10)
                        compCombo=wx.ComboBox(self.panel,style=wx.CB_READONLY)
                        compCombo.Append("")
                        compCombo.AppendItems(csvColumns)
                        self.combos.append((compCombo,(comp.title(),c)))
                        sensorCombo[(comp.title(),c)]=compCombo
                        vbox.Add(compCombo,flag=wx.EXPAND|wx.RIGHT|wx.LEFT,border=5)
                else:
                    compCombo=wx.ComboBox(self.panel,style=wx.CB_READONLY)
                    compCombo.Append("")
                    compCombo.AppendItems(csvColumns)
                    self.combos.append((compCombo,comp.title()))
                    sensorCombo[comp.title()]=compCombo
                    vbox.Add(compCombo,flag=wx.EXPAND|wx.RIGHT|wx.LEFT,border=5)
        if lastMapping!=None:
            for (col,component) in lastMapping.items():
                if type(component)==list:
                    component=tuple(component)
                if component=="TIME":
                    self.timeCombo.SetStringSelection(col)
                elif sensorCombo.has_key(component):
                    sensorCombo[component].SetStringSelection(col)
                
        # each sensor can only take one mapping
        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self.panel, wx.ID_OK)
        okButton.Bind(wx.EVT_BUTTON,self.OnOK)
        cancelButton = wx.Button(self.panel, wx.ID_CANCEL)
        hbox1.Add(okButton)
        hbox1.Add(cancelButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox1,flag=wx.ALIGN_RIGHT|wx.TOP,border=5)
        
        self.panel.SetSizer(vbox)
        self.panel.Layout()
        vbox.Fit(self)
        
    def OnOK(self,event):
        if self.timeCombo.GetSelection()!=wx.NOT_FOUND:
            anySelected=False
            for box,comp in self.combos:
                if box.GetSelection()!=wx.NOT_FOUND and len(box.GetStringSelection())>0:
                    anySelected=True
            if not anySelected:
                wx.MessageBox('You need to select at least one mapping from CSV column to sensor', 'Error', 
                    wx.OK | wx.ICON_WARNING)
                return True
        else:
            wx.MessageBox('You need to select a column with the time in it', 'Error', 
                wx.OK | wx.ICON_WARNING)
            return True
        self.mapping={self.timeCombo.GetStringSelection():"TIME"}
        for combo,data in self.combos:
            if combo.GetSelection()!=wx.NOT_FOUND and len(combo.GetStringSelection())>0:
                self.mapping[combo.GetStringSelection()]=data
        event.Skip()
        return False
       
    def getAssignments(self):
        return self.mapping