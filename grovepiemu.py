# Todo: RFID module, RFID tag module
#
# 

import wx
import wx.propgrid as wxpg

import os    
import sys
# this line I think makes it so that any loaded python files will get their grovepi from the right place where the fake grovepi bits live  
# in preference to any that happen to be in the same directory as them
sys.path=[os.path.join(os.path.abspath(os.path.dirname(__file__)),"fakegrovepi")]+sys.path

import components
import threading
import time
import json
import gpe_utils
import urllib2

class PropertyFrame(wx.Frame):
    def __init__(self, sensorObject):
        wx.Frame.__init__(self, None, title=sensorObject.title(), size=(200,200))
        panel = wx.Panel(self)
        box = wx.GridSizer(1,1,0,0)
        sensorObject.initPropertyPage(panel,box)        
        panel.SetSizer(box)
        panel.Layout()

class AllPropertyFrame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, title="Properties",style=wx.CAPTION |wx.FRAME_FLOAT_ON_PARENT| wx.FRAME_TOOL_WINDOW)
        self.panel = wx.Panel(self)
        self.masterSizer = wx.BoxSizer(wx.VERTICAL)        
        self.panel.SetSizer(self.masterSizer)
        self.panel.Layout()
        self.componentSizers={}
        
    def addSensorObject(self,sensorObject,type):
        posBefore=0
        pin=sensorObject.pin
        typeOrdering=["D","A","I"]
        typeIndex=typeOrdering.index(type)        
        for c in self.masterSizer.GetChildren():
            (ignore,otherPin,otherType)=c.GetUserData()
            otherTypeIndex=typeOrdering.index(otherType)
            if (otherTypeIndex,otherPin)<(typeIndex,pin):
                posBefore+=1
   
        sizer1=wx.BoxSizer(wx.VERTICAL)
        sizer1.Add( wx.StaticText(self.panel,label=sensorObject.title()))
        sizer2=wx.BoxSizer(wx.VERTICAL)
        sensorObject.initPropertyPage(self.panel,sizer2)
        self.fixPropertyPageLength(sizer2)
        sizer1.Add(sizer2,proportion=0,flag=wx.EXPAND)
        self.masterSizer.Insert(posBefore,sizer1,proportion=0,flag=wx.EXPAND,userData=(sensorObject,sensorObject.pin,type))
        self.componentSizers[sensorObject]=sizer1
        self.panel.Layout()
        self.masterSizer.Fit(self)
    
    def fixPropertyPageLength(self,ownerSizer):
        for c in ownerSizer.GetChildren():
            if c.GetWindow()!=None and isinstance(c.GetWindow(),wxpg.PropertyGrid):
                pg=c.GetWindow()
                rows=pg.GetRoot().GetChildCount()
                pg.SetMinSize(wx.Size(pg.GetMinWidth(),pg.GetRowHeight()*rows+ pg.GetVerticalSpacing()*(rows+1)))
        
    def removeSensorObject(self,sensorObject):
        if self.componentSizers.has_key(sensorObject):
            self.componentSizers[sensorObject].DeleteWindows()




class Frame(wx.Frame):


    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(640,480))

        self.componentList={}
        self.propertyFrames={}
        self.properties=AllPropertyFrame(self)
        self.properties.Show()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_new=menu.Append(wx.ID_NEW, "&New\tCtrl+N", "Clear everything")
        m_open=menu.Append(wx.ID_OPEN, "&Open\tCtrl+O", "Open settings file")
        m_save=menu.Append(wx.ID_SAVE, "&Save\tCtrl+S", "Save settings file")
        m_saveas=menu.Append(wx.ID_SAVEAS, "Save &As\tCtrl+Shift+S", "Save as new settings file")
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tCtrl+X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        self.Bind(wx.EVT_MENU, self.OnSave, m_save)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, m_saveas)
        self.Bind(wx.EVT_MENU, self.OnOpen, m_open)
        self.Bind(wx.EVT_MENU, self.OnNew, m_new)
        menuBar.Append(menu, "&File")
        
        menu=wx.Menu()
        m_about=menu.Append(wx.ID_ABOUT,"&About","Information about the program")
        self.Bind(wx.EVT_MENU,self.OnAbout,m_about)
        menuBar.Append(menu,"&Help")
#        menu = wx.Menu()
#        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
#        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
#        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        
#        self.statusbar = self.CreateStatusBar()

        self.panel = wx.Panel(self)
        self.sizer=wx.GridBagSizer()
        self.subSizers={}
        self.digiPins=[2,3,4,5,6,7,8]
        self.anaPins=[0,1,2]
        self.i2cPins=[1,2,3]
        self.containerSizers={}
        
        
        
        for row,pinNum in enumerate(self.digiPins):
            allBox=wx.BoxSizer(wx.VERTICAL)
            newSizer=wx.BoxSizer(wx.VERTICAL)
            self.subSizers[(pinNum,"D")]=newSizer
            self.containerSizers[(pinNum,"D")]=allBox
            self.sizer.Add(allBox,(row,0),flag=wx.EXPAND)
            allBox.Add( wx.StaticText(self.panel,label="D%d"%pinNum))
            allBox.Add(newSizer,flag=wx.EXPAND)
            newSizer.Add( wx.StaticText(self.panel,label="Right click to connect sensor"))
            
        for row,pinNum in enumerate(self.anaPins):
            allBox=wx.BoxSizer(wx.VERTICAL)
            newSizer=wx.BoxSizer(wx.VERTICAL)
            self.subSizers[(pinNum,"A")]=newSizer
            self.containerSizers[(pinNum,"A")]=allBox
            self.sizer.Add(allBox,(row*2,1),span=(2,1),flag=wx.EXPAND)
            allBox.Add( wx.StaticText(self.panel,label="A%d"%pinNum))
            allBox.Add(newSizer,flag=wx.EXPAND)
            newSizer.Add( wx.StaticText(self.panel,label="Right click to connect sensor"))

        for row,pinNum in enumerate(self.i2cPins):
            allBox=wx.BoxSizer(wx.VERTICAL)
            newSizer=wx.BoxSizer(wx.VERTICAL)
            self.subSizers[(pinNum,"I")]=newSizer
            self.containerSizers[(pinNum,"I")]=allBox
            allBox.Add( wx.StaticText(self.panel,label="I2C-%d"%pinNum))
            allBox.Add(newSizer,flag=wx.EXPAND)
            self.sizer.Add(allBox,(row*2,2),span=(2,1),flag=wx.EXPAND)
            newSizer.Add( wx.StaticText(self.panel,label="Right click to connect sensor"))

        # CSV file transport, chooser, mapper
        csvBox=wx.BoxSizer(wx.VERTICAL)
        transportBox=wx.BoxSizer(wx.HORIZONTAL)
        transportBox2=wx.BoxSizer(wx.HORIZONTAL)
        timeBox=wx.FlexGridSizer(2,2)
        self.csvName=wx.StaticText(self.panel,label="Replay: ")
        transportButtons=[("Unload..",self.OnUnloadCSV),("File..",self.OnLoadCSV),("Server...",self.OnServerConnect)]
        transportButtons2=[("[]",self.OnStopCSV),("||",self.OnPauseCSV),(">",self.OnPlayCSV),("Map Fields...",self.OnMapCSV)]
        self.csvButtons={}
        for(label,fn) in transportButtons:
            button=wx.Button(self.panel,wx.ID_ANY,label,style=wx.BU_EXACTFIT)
            transportBox.Add(button)
            self.csvButtons[label]=button
            button.Bind(wx.EVT_BUTTON,fn)
        for(label,fn) in transportButtons2:
            button=wx.Button(self.panel,wx.ID_ANY,label,style=wx.BU_EXACTFIT)
            transportBox2.Add(button)
            self.csvButtons[label]=button
            button.Bind(wx.EVT_BUTTON,fn)
        
        self.csvTimeReal=wx.StaticText(self.panel,label="00:00:00 (12/12/2012)",style=wx.ST_NO_AUTORESIZE)
        self.csvTimeStart=wx.StaticText(self.panel,label="00:00:00",style=wx.ST_NO_AUTORESIZE)
        oldFont=self.csvTimeReal.GetFont()
        newFont=wx.Font(oldFont.PointSize,wx.FONTFAMILY_TELETYPE,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.csvTimeReal.SetFont(newFont)
        self.csvTimeStart.SetFont(newFont)

        timeBox.Add(wx.StaticText(self.panel,label="Time from start: "),flag=wx.ALIGN_RIGHT)
        timeBox.Add(self.csvTimeStart)
        timeBox.Add(wx.StaticText(self.panel,label="File Time: "),flag=wx.ALIGN_RIGHT)
        timeBox.Add(self.csvTimeReal)
            
        csvBox.Add(self.csvName)
        csvBox.Add(transportBox)
        csvBox.Add(transportBox2)
        csvBox.Add(timeBox)
        self.sizer.Add(csvBox,(7,2),flag=wx.EXPAND)
        
        # script loader, stopper, starter
        scriptBox=wx.BoxSizer(wx.VERTICAL)
        self.scriptNameLabel=wx.StaticText(self.panel,label="GrovePi Python Script:")
        self.scriptStatus=wx.StaticText(self.panel,label="")
        
        pyButtonBox=wx.BoxSizer(wx.HORIZONTAL)
        pyButtons=[("Load...",self.OnLoadPY),("Clear",self.OnClearPY),("[]",self.OnStopPY),(">",self.OnRunPY)]
        self.scriptButtons={}
        for(label,fn) in pyButtons:
            button=wx.Button(self.panel,wx.ID_ANY,label,style=wx.BU_EXACTFIT)
            pyButtonBox.Add(button)
            self.scriptButtons[label]=button
            button.Bind(wx.EVT_BUTTON,fn)
        
        scriptBox.Add(self.scriptNameLabel)
        scriptBox.Add(self.scriptStatus)
        scriptBox.Add(pyButtonBox)
        
        self.sizer.Add(scriptBox,(7,1),flag=wx.EXPAND)            
            
        for i in range(3):
            self.sizer.AddGrowableCol(i)
            
        for i in range(7):
            self.sizer.AddGrowableRow(i)
            
 
 
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()

        self.panel.Bind(wx.EVT_RIGHT_DOWN, self.OnContextMenu)
        

        
        self.updateTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.updateTimer)
        self.updateTimer.Start(50)
        self.BindRightClick(self)
        self.player=None
        self.scriptPath=None
        self.scriptRunner=None
        self.lastAssignments={}
        self.settingsFile=None
        self.csvPath=None
        if len(sys.argv)>1:
            self.settingsFile=sys.argv[1]
            self.loadSettingsIni(sys.argv[1])
            if self.settingsFile!=None:
               self.SetTitle("GrovePi Emulator - %s"%self.settingsFile)
        else:
            self.loadSettingsIni(os.path.join(os.path.dirname(__file__),"grovepiemu.ini"),True)

    def OnClearPY(self,event):
        self.scriptPath=None
        self.OnRunPY(event)
            
    def OnLoadPY(self,event,reloadCurrent=False):
        if not reloadCurrent:
            openFileDialog = wx.FileDialog(self, "Open Python script to run", "", "",
                                           "Python files (*.py)|*.py", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.scriptPath=openFileDialog.GetPath()
        self.OnRunPY(event)
        
    def OnRunPY(self,event):
        if self.scriptRunner!=None and self.scriptRunner.running():
            self.scriptRunner.stop()
        if self.scriptPath==None:
            self.scriptNameLabel.SetLabel("GrovePi Python Script: ")
        else:
            self.scriptNameLabel.SetLabel("GrovePi Python Script: %s"%os.path.basename(self.scriptPath))
            self.scriptRunner=gpe_utils.StoppableRunner(self.scriptPath)
    
    def OnStopPY(self,event):
        if self.scriptRunner!=None and self.scriptRunner.running():
            self.scriptRunner.stop()
        
    def OnServerConnect(self,event,reloadCurrent=False):
        if not reloadCurrent:
            oldPath="http://www.cs.nott.ac.uk/~pszjm2/sensordata/?id=1"
            if self.csvPath!=None and self.csvPath.lower().startswith("http://"):
                oldPath=self.csvPath
            selectURLDialog= wx.TextEntryDialog(self,"Enter a URL to remote sensor data","Connect to sensor server",defaultValue=oldPath)
            if selectURLDialog.ShowModal()==wx.ID_CANCEL:
                return
            self.csvPath=selectURLDialog.GetValue()
            if not self.csvPath.lower().startswith("http://"):
                self.csvPath="http://"+self.csvPath
        if self.player!=None:
            self.player.unload()
            self.player=None
            self.csvName.SetLabel("Replay data: ")
        if self.csvPath!=None:
            try:
                self.player=gpe_utils.ServerPlayer(self.csvPath)
                self.csvName.SetLabel("Replay url: %s (need to set mapping)"%(self.player.getName()))
                self.OnMapCSV(None,reloadCurrent)
            except IOError:
                self.player=None
                self.csvName.SetLabel("Replay data: ")
                self.csvPath=None

    def OnJSONConnect(self,event,reloadCurrent=False):
        if not reloadCurrent:
            oldPath="http://www.cs.nott.ac.uk/~jqm/sensorvalues.php?id=2"
            if self.csvPath.lower().startswith("http://"):
                oldPath=self.csvPath
            selectURLDialog= wx.TextEntryDialog(self,"Enter a URL to remote sensor data JSON","Connect to JSON Sensor Server",defaultValue=oldPath)
            if selectURLDialog.ShowModal()==wx.ID_CANCEL:
                return
            self.csvPath=selectURLDialog.GetValue()
            if not self.csvPath.lower().startswith("http://"):
                self.csvPath="http://"+self.csvPath
        if self.player!=None:
            self.player.unload()
            self.player=None
            self.csvName.SetLabel("Replay data: ")
        if self.csvPath!=None:
            self.player=gpe_utils.JSONPlayer(self.csvPath)
            self.csvName.SetLabel("Replay url: %s (need to set mapping)"%(self.player.getName()))
            self.OnMapCSV(None,reloadCurrent)
            
            
    def OnUnloadCSV(self,event):
        if self.player!=None:
            self.player.unload()       
            self.player=None
            self.csvName.SetLabel("Replay data: ")
            self.csvPath=""
        
        
    def OnLoadCSV(self,event,reloadCurrent=False):
        if not reloadCurrent:
            openFileDialog = wx.FileDialog(self, "Open CSV file for data playback", "", "",
                                           "CSV files (*.csv)|*.csv", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.csvPath=openFileDialog.GetPath()
        if self.player!=None:
            self.player.unload()       
            self.player=None
            self.csvName.SetLabel("Replay data: ")
        if self.csvPath!=None:
            self.player=gpe_utils.CSVPlayer(self.csvPath)
            self.csvName.SetLabel("Replay data: %s (need to set mapping)"%(self.player.getName()))
            self.OnMapCSV(None,reloadCurrent)

    def findComponentByName(self,name):
        for c in self.componentList.values():
            if c.title()==name:
                return c
        return None
        
    def OnMapCSV(self,event,reloadCurrent=False):
        if self.player==None:
            return
        if not reloadCurrent:        
            mapdlg=gpe_utils.CSVMappingDlg(self,self.player.getFieldNames(),self.componentList.values(),self.lastAssignments,isinstance(self.player,gpe_utils.CSVPlayer))
            if mapdlg.ShowModal()!=wx.ID_OK:
                return
            self.lastAssignments=mapdlg.getAssignments()
        assignmentsFixed={}
        timeColumn=None
        for (col,dest) in self.lastAssignments.items():
            if type(dest)==tuple or type(dest)==list:
                colDesc=(self.findComponentByName(dest[0]),dest[1])
                if colDesc[0]!=None:
                    assignmentsFixed[col]=colDesc
            elif dest=="TIME":
                timeColumn=col
            else:
                colDesc=self.findComponentByName(dest)
                if colDesc!=None:
                    assignmentsFixed[col]=colDesc
        if isinstance(self.player,gpe_utils.ServerPlayer):
            if len(assignmentsFixed)>0:
                self.player.setFieldAssignments(assignmentsFixed)
                self.csvName.SetLabel("Replay data: %s"%(self.player.getName()))
                self.player.startPlaying(self,True)
        else:
            if timeColumn!=None and len(assignmentsFixed)>0:
                self.player.setFieldAssignments(timeColumn,assignmentsFixed)
                self.csvName.SetLabel("Replay data: %s"%(self.player.getName()))
        
    def OnStopCSV(self,event):
        if self.player!=None:
            self.player.stopPlaying()
        
    def OnPauseCSV(self,event):
        if self.player!=None:
            self.player.pausePlaying()
        
    def OnPlayCSV(self,event):
        if self.player!=None:
            self.player.startPlaying(self,True)                       
            
    def OnSave(self,event):
        if self.settingsFile==None:
            self.OnSaveAs(event)
        else:
            self.saveSettingsIni(self.settingsFile)

    def OnNew(self,event):
        removals=[]
        for (pin,type) in self.componentList.keys():
            removals.append((pin,type))
        for (pin,type) in removals:
            self.removeComponent(pin,type)
        if self.player!=None:
            self.player.unload()       
            self.player=None
            self.csvName.SetLabel("Replay data: ")
        if self.scriptRunner!=None and self.scriptRunner.running():
            self.scriptRunner.stop()
        self.scriptPath=None
        self.scriptNameLabel.SetLabel("GrovePi Python Script: ")
            
    def OnSaveAs(self,event):
        openFileDialog = wx.FileDialog(self, "Save GrovePI emulator settings", "", "",
                                       "Grove PI emulator settings files (*.gpi)|*.gpi", wx.FD_SAVE)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        self.settingsFile=openFileDialog.GetPath()
        self.SetTitle("GrovePi Emulator - %s"%self.settingsFile)
        self.saveSettingsIni(self.settingsFile)
    
    
    def OnOpen(self,event):
        openFileDialog = wx.FileDialog(self, "Open GrovePI emulator settings", "", "",
                                       "Grove PI emulator settings files (*.gpi)|*.gpi", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        self.settingsFile=openFileDialog.GetPath()
        self.SetTitle("GrovePi Emulator - %s"%self.settingsFile)
        self.loadSettingsIni(self.settingsFile)
        
    def OnAbout(self,event):
        info = wx.AboutDialogInfo()
        description="""Emulation environment for running python programs developed for the GrovePI sensor board.
Currently has support for the following sensors:

"""
        for c in components.allSensors:
            description+=c.classDescription()+"\n"
        info.SetName('Grove PI Emulation Environment')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2015 Joe Marshall')
        info.SetWebSite('http://www.cs.nott.ac.uk/~jqm')
        info.SetLicence(""" Do what you want with the code. Any questions, email joe.marshall@nottingham.ac.uk """)
        info.AddDeveloper('Joe Marshall')

        wx.AboutBox(info)

    
    def loadSettingsIni(self,name,fromIni=False):
# a)which things are connected 
# b)any config settings on them e.g.LED colour, generic digital pullup (and what?). Most modules won't have any config I think
# c)the name/path of the currently loaded python script
# d)the (last)mapping for playback
# e)currently loaded csv file
        try:
            with open(name,'r') as file:
                allConfig=json.load(file)
                modules=allConfig["modules"]
                for (pinType,(moduleName,config)) in modules.items():
                    thisComponent=None
                    for sensorClass in components.allSensors:
                        if sensorClass.classDescription()==moduleName:
                            thisComponent=sensorClass(int(pinType[0]))
                            break
                    if thisComponent!=None:
                        if config!=None and hasattr(thisComponent,"loadConfig"):
                            thisComponent.loadConfig(config)
                        self.addComponent(thisComponent,pinType[1])
                # go through each module, a)creating it, b)setting the config if there is any
                self.scriptPath=self.fullPath(allConfig["pythonScript"],name)
                self.lastAssignments=allConfig["sensorAssignments"]
                if allConfig["csvPath"] and len(allConfig["csvPath"])>0:
                    self.csvPath=self.fullPath(allConfig["csvPath"],name)
                    # reload the CSV file and sensor assignments
                    if self.csvPath.lower().startswith("http://"):
                        self.OnServerConnect(None,True)
                    else:
                        self.OnLoadCSV(None,True)
                else:
                    self.OnUnloadCSV(None)
                self.OnLoadPY(None,True)
 #               if fromIni:
 #                   self.settingsFile=self.fullPath(allConfig["currentFileOpen"],name) 
 #                   if self.settingsFile!=None:
 #                       self.SetTitle("GrovePi Emulator - %s"%self.settingsFile)

 #       except IOError:
 #           print "Couldn't load config ",name
        except KeyError:
            print "Key missing"

    def fullPath(self,file,name):
        if file==None:
            return None
        if file.lower().startswith("http://"):
            return file
        return os.path.abspath(os.path.join(os.path.dirname(name),file))
            
    def relPath(self,file,name):
        if file==None:
            return None
        if file.lower().startswith("http://"):
            return file
        return os.path.relpath(file,os.path.dirname(os.path.abspath(name)))
            
    def saveSettingsIni(self,name):
        try:
            with open(name,'w') as file:
                allConfig={}
                modules={}
                for (pin,type),component in self.componentList.items():
                    modConfig=None
                    if hasattr(component,"saveConfig"):
                        modConfig=component.saveConfig()
                    modules["%d%s"%(pin,type)]=[component.classDescription(),modConfig]
                allConfig["modules"]=modules
                
                allConfig["pythonScript"]=self.relPath(self.scriptPath,name)
                allConfig["sensorAssignments"]=self.lastAssignments
                allConfig["csvPath"]=self.relPath(self.csvPath,name)
    #            allConfig["currentFileOpen"]=self.relPath(self.settingsFile,name)
                json.dump(allConfig,file)
        except IOError:
            print "Couldn't save settings file"
    
    # a)which things are connected 
# b)any config settings on them e.g.LED colour, generic digital pullup (and what?). Most modules won't have any config I think
# c)the name/path of the currently loaded python script
# d)the (last)mapping for playback
# e)currently loaded csv file
        None
        
    def BindRightClick(self,wnd):
        wnd.Bind(wx.EVT_RIGHT_DOWN,self.OnContextMenu)
        for item in wnd.GetChildren():
            self.BindRightClick(item)

        
    def OnContextMenu(self,event):
        fromWindow=event.GetEventObject()
        posHere=self.ScreenToClient(fromWindow.ClientToScreen(event.GetPosition()))
        for (pin,type),sizer in self.containerSizers.items():
            sp=sizer.GetPosition()
            ss=sizer.GetSize()
            rect = wx.Rect(sp.x,sp.y,ss.width,ss.height)
            if rect.Contains(posHere):
                if type=="D":
                    menu = wx.Menu()
                    for index,classObj in enumerate(components.digitalSensors):
                        menu.Append(index+1,classObj.classDescription())
                        wx.EVT_MENU(menu,index+1,self.OnSelectDig)
                    menu.AppendSeparator()
                    for index,classObj in enumerate(components.digitalOutputs):
                        menu.Append(index+1000,classObj.classDescription())
                        wx.EVT_MENU(menu,index+1000,self.OnSelectDig)
                elif type=="A":
                    menu = wx.Menu()
                    for index,classObj in enumerate(components.analogSensors):
                        menu.Append(index+1,classObj.classDescription())
                        wx.EVT_MENU(menu,index+1,self.OnSelectAna)
                elif type=="I":
                    menu = wx.Menu()
                    for index,classObj in enumerate(components.i2cConnections):
                        menu.Append(index+1,classObj.classDescription())
                        wx.EVT_MENU(menu,index+1,self.OnSelectI2c)
                self.menuSelection=None
                if self.componentList.has_key((pin,type)):
                    menu.AppendSeparator()
                    menu.Append(999,"Disconnect "+self.componentList[(pin,type)].title())
                    wx.EVT_MENU(menu,999,self.OnDeleteComponent)
                    self.selectedComponent=(pin,type)
                    
                if self.PopupMenu( menu, posHere ) and self.menuSelection!=None:
                    wx.CallAfter(self.addComponent, self.menuSelection(pin),type)

    def OnSelectDig(self,event):
        if event.GetId()<1000:
            self.menuSelection= components.digitalSensors[event.GetId()-1]
        else:
            self.menuSelection= components.digitalOutputs[event.GetId()-1000]
        
    def OnSelectAna(self,event):
        self.menuSelection= components.analogSensors[event.GetId()-1]

    def OnSelectI2c(self,event):
        self.menuSelection= components.i2cConnections[event.GetId()-1]
        
    def OnDeleteComponent(self,event):
        self.removeComponent(*self.selectedComponent)

        
    def addComponent(self,component,type):
        pin=component.pin
        self.removeComponent(pin,type)
        self.componentList[(pin,type)]=component
        if hasattr(component,"initPropertyPage"):
            self.properties.addSensorObject(component,type)
            #pf=PropertyFrame(component)
            #pf.Show()
            #self.propertyFrames[(pin,type)]=pf
        sizer=self.subSizers[(pin,type)]
        component.initSmall(self.panel,sizer)
        for item in sizer.GetChildren():
            if item.GetWindow()!=None:
                item.GetWindow().Bind(wx.EVT_RIGHT_DOWN,self.OnContextMenu)
        self.panel.Layout()
                
    def removeComponent(self,pin,type):
        if self.componentList.has_key((pin,type)):
            component=self.componentList[(pin,type)]
            if hasattr(component,"onComponentDestroy"):
                component.onComponentDestroy()
            del(self.componentList[(pin,type)])
            self.properties.removeSensorObject(component)
        sizer=self.subSizers[(pin,type)]
        sizer.DeleteWindows()
        
            
    def update(self,event):
        for component in self.componentList.values():
            if hasattr(component,"update"):
                component.update()
        if self.player!=None:
            ofsTime,realTime=self.player.getTimes()
            self.csvTimeStart.SetLabel(time.strftime("%H:%M:%S",time.gmtime(ofsTime)))
            self.csvTimeReal.SetLabel(time.strftime("%H:%M:%S (%d/%m/%Y)",time.gmtime(realTime)))
        if self.player==None or not self.player.playing():
            self.csvButtons[">"].SetBackgroundColour((128,150,128))
            self.csvButtons["[]"].SetBackgroundColour((255,0,0))
            self.csvButtons["||"].SetBackgroundColour((255,0,0))
        else:
            self.csvButtons[">"].SetBackgroundColour((0,255,0))
            self.csvButtons["[]"].SetBackgroundColour((150,128,128))
            self.csvButtons["||"].SetBackgroundColour((150,128,128))
        if self.scriptRunner!=None:
            if self.scriptRunner.running():
                self.scriptStatus.SetLabel("Running")
            else:
                self.scriptStatus.SetLabel("Stopped")
        else:
            self.scriptStatus.SetLabel("No script loaded")
        
    def OnClose(self, event):
        if self.scriptRunner!=None and self.scriptRunner.running():
            self.scriptRunner.stop()
        self.saveSettingsIni(os.path.join(os.path.dirname(__file__),"grovepiemu.ini"))
        self.Destroy()
#        dlg = wx.MessageDialog(self, 
#            "Do you really want to close this application?",
#            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
 #       result = dlg.ShowModal()
  #      dlg.Destroy()
   #     if result == wx.ID_OK:
    #        self.Destroy()

    
app = wx.App()   # Error messages go to popup window
top = Frame("GrovePi Emulator - <untitled>")
top.Show()
app.MainLoop()
