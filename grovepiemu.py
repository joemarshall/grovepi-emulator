3
# Todo: RFID module, RFID tag module
#
# 


import os    
import sys
from idlelib.tooltip import Hovertip

if getattr( sys, 'frozen', False ) :
        # running in an installer bundle
    _mainPath=sys._MEIPASS
        
else :
        _mainPath=os.path.dirname(__file__)
        # running live
        # this line I think makes it so that any loaded python files will get their grovepi from the right place where the fake grovepi bits live  
        # in preference to any that happen to be in the same directory as them
        sys.path=[os.path.join(os.path.abspath(os.path.dirname(__file__)),"fakegrovepi")]+sys.path

import gpe_utils
from gpe_utils.tkimports import *
import components
import threading
import time
import json
import sensors 
import graphs 

DIGI_PINS=[2,3,4,5,6,7,8]
ANA_PINS=[0,1,2]
I2CPINS=[1,2,3]

class AllPropertyFrame(tk.Toplevel):
    def __init__(self,parent):
        tk.Toplevel.__init__(self)
        if sys.platform=="win32":
            self.attributes('-toolwindow', True)
        self.iconbitmap(os.path.join(_mainPath,"main.ico"))
        self.title("Properties")
        self.componentSizers={}
        self.protocol("WM_DELETE_WINDOW", self.OnClose)
        
    def addSensorObject(self,sensorObject,type):
        posBefore=0
        pin=sensorObject.pin
        if type=="D":
            rowNum= DIGI_PINS.index(pin)
        elif type=="A":
            rowNum=len(DIGI_PINS)+ANA_PINS.index(pin)
        elif type=="I":
            rowNum=len(DIGI_PINS)+len(ANA_PINS)+I2CPINS.index(pin)
            
        newFrame=tk.Frame(self)
        sensorObject.initPropertyPage(newFrame)
        self.componentSizers[sensorObject]=newFrame
        newFrame.grid(row=rowNum)
        
    def removeSensorObject(self,sensorObject):
        if sensorObject in self.componentSizers:
            sizer=self.componentSizers[sensorObject]
            for child in sizer.winfo_children():
                child.destroy()
            self.componentSizers[sensorObject].destroy()    
            del self.componentSizers[sensorObject]

    def OnClose(self,event=None):
        return False


def _make_button(parent,imageOrText,fn):
    if type(imageOrText)==tuple:
        img=tk.PhotoImage(file=imageOrText[1])
        button=tk.Button(parent,image=img,text=imageOrText[0],command=fn)
        button.img=img
        return button,imageOrText[0]
    else:
        button=tk.Button(parent,text=imageOrText,command=fn)
        return button,imageOrText


class Frame(tk.Frame):

    def __init__(self, root,title):
        tk.Frame.__init__(self, master=root,width=640,height=480)
        
        self.root=root
        self.root.wm_title(title)
        
        self.componentList={}
        self.properties=AllPropertyFrame(self)

        root.protocol("WM_DELETE_WINDOW", self.OnClose)
        
        menuBar = tk.Menu(root)
        fileMenu=tk.Menu(menuBar,tearoff=0)
        m_new=fileMenu.add_command(label="New",command=self.OnNew,underline=0,accelerator="Ctrl+N")
        m_open=fileMenu.add_command(label="Open", underline=0,accelerator="Ctrl+O",command=self.OnOpen)
        m_save=fileMenu.add_command(label="Save", underline=0,accelerator="Ctrl+S",command=self.OnSave)
        m_saveas=fileMenu.add_command(label="Save As",underline=5,accelerator="Ctrl+Shift+S", command=self.OnSaveAs)
        fileMenu.add_separator()
        m_writePython=fileMenu.add_command(label="Write Python for Current Sensors",command=self.OnWritePython,underline=6,accelerator="Ctrl+P")
        fileMenu.add_separator()      
        m_exit = fileMenu.add_command(label="Exit",underline=2,accelerator="Ctrl+X", command=self.OnClose)

        root.bind_all("<Control-n>", self.OnNew)
        root.bind_all("<Control-o>", self.OnOpen)
        root.bind_all("<Control-s>", self.OnSave)
        root.bind_all("<Control-S>", self.OnSaveAs)
        root.bind_all("<Control-x>", self.OnClose)
        root.bind_all("<Control-p>", self.OnWritePython)
        
        menuBar.add_cascade(label="File",menu=fileMenu,underline=0)
        
        helpMenu=tk.Menu(menuBar,tearoff=0)
        helpMenu.add_command(label="About",command=self.OnAbout,underline=0)
        menuBar.add_cascade(label="Help",menu=helpMenu,underline=0)
        
        root.config(menu=menuBar)

        
        defaultFont=tkf.nametofont('TkDefaultFont').actual()
        self.labelFrameFont=(defaultFont['family'],defaultFont['size'],'bold')
        
        self.subSizers={}
        self.containerSizers={}
        
        #column 0 = digital
        for row,pinNum in enumerate(DIGI_PINS):
            allBox=tk.LabelFrame(root,text="D%d"%pinNum,bd=0,bg='#eff',padx=4,pady=4,font=self.labelFrameFont)
            containerBox=tk.Frame(allBox)
            containerBox.grid(row=0)

            dummy=tk.Label(containerBox,text="Right click to connect sensor")
            dummy.pack()

            allBox.grid(row=row,column=0,sticky=tk.W+tk.E+tk.N+tk.S,pady=2,padx=2 )
            
            self.containerSizers[(pinNum,"D")]=allBox
            self.subSizers[(pinNum,"D")]=containerBox
            
        #column 1 = analog
        for row,pinNum in enumerate(ANA_PINS):
            allBox=tk.LabelFrame(root,text="A%d"%pinNum,bd=0,bg='#fef',padx=4,pady=4,font=self.labelFrameFont)
            containerBox=tk.Frame(allBox)
            containerBox.grid(row=0)

            dummy=tk.Label(containerBox,text="Right click to connect sensor")
            dummy.pack()

            allBox.grid(row=row*2,rowspan=2,column=1,sticky=tk.W+tk.E+tk.N+tk.S,pady=2,padx=2 )
            
            self.containerSizers[(pinNum,"A")]=allBox
            self.subSizers[(pinNum,"A")]=containerBox

        #column 2 = i2c
        for row,pinNum in enumerate(I2CPINS):
            allBox=tk.LabelFrame(root,text="I2C-%d"%pinNum,bd=0,bg='#ffe',padx=4,pady=4,font=self.labelFrameFont)
            containerBox=tk.Frame(allBox)
            containerBox.grid(row=0)

            dummy=tk.Label(containerBox,text="Right click to connect sensor")
            dummy.pack()

            allBox.grid(row=row*2,rowspan=2,column=2,sticky=tk.W+tk.E+tk.N+tk.S,pady=2,padx=2 )
            
            self.containerSizers[(pinNum,"I")]=allBox
            self.subSizers[(pinNum,"I")]=containerBox
            
        # CSV file transport, chooser, mapper
        bg='#fee'
        csvBox=tk.LabelFrame(root,text="CSV Playback of sensor data",bd=0,bg=bg,padx=4,pady=4,font=self.labelFrameFont)
        transportBox=tk.Frame(csvBox,bg=bg)
        transportBox2=tk.Frame(csvBox,bg=bg)
        timeBox=tk.Frame(csvBox,bg=bg)
        self.csvName=tk.Label(csvBox,text="Replay CSV: ",bg=bg)
        transportButtons=[("File..",self.OnLoadCSV),("Server...",self.OnServerConnect),("Clear..",self.OnUnloadCSV)]
        transportButtons2=[(("[]","stopcsv.png"),self.OnStopCSV),(("||","pausecsv.png"),self.OnPauseCSV),((">","startcsv.png"),self.OnPlayCSV),("Map Fields...",self.OnMapCSV)]
        self.csvButtons={}
        for col,(label,fn) in enumerate(transportButtons):
            button,button_id=_make_button(transportBox,label,fn)
            self.csvButtons[button_id]=button
            transportBox.columnconfigure(col,weight=1)
            button.grid(row=0,column=col,sticky=tk.W+tk.E+tk.N+tk.S)
        for col,(label,fn) in enumerate(transportButtons2):
            button,button_id=_make_button(transportBox2,label,fn)
            self.csvButtons[button_id]=button
            transportBox2.columnconfigure(col,weight=1)
            button.grid(row=0,column=col,sticky=tk.W+tk.E+tk.N+tk.S)
        
        self.csvTimeReal=tk.Label(timeBox,text="00:00:00 (12/12/2012)",font="Courier",bg=bg)
        self.csvTimeStart=tk.Label(timeBox,text="00:00:00",font="Courier",bg=bg)
        tk.Label(timeBox,text="Time from start:",bg=bg).grid(row=0,column=0,sticky=tk.E)
        tk.Label(timeBox,text="File Time:",bg=bg).grid(row=1,column=0,sticky=tk.E)
        self.csvTimeStart.grid(row=0,column=1,sticky=tk.W)
        self.csvTimeReal.grid(row=1,column=1,sticky=tk.W)
        
        self.csvName.grid(row=0,sticky=tk.W)
        transportBox.grid(row=1,sticky=tk.W+tk.E)
        transportBox2.grid(row=2,sticky=tk.W+tk.E)
        timeBox.grid(row=3,sticky=tk.W)
        
        csvBox.grid(row=7,column=2,sticky=tk.W+tk.E+tk.N+tk.S)            
        
        # buttons to run python scripts
        bg='#eef'
        scriptBox=tk.LabelFrame(root,text="Run python scripts",bd=0,bg=bg,padx=4,pady=4,font=self.labelFrameFont)
        self.scriptNameLabel=tk.Label(scriptBox,text="GrovePi Python Script:",bg=bg)
        self.scriptStatus=tk.Label(scriptBox,text="",bg=bg)
        
        self.captureScriptButton=tk.Button(scriptBox,text="Capture script to file",command=self.OnCaptureToFile)
        self.runRemoteButton=tk.Button(scriptBox,text="Run on real PI via SSH",command=self.OnRunRemote)
        self.runLocalButton=tk.Button(scriptBox,text="Run in emulator",command=self.OnRunLocal)
        self.setAddressButton=tk.Button(scriptBox,text="Set remote address",command=self.OnSetRemote)
        

        pyButtonBox=tk.Frame(scriptBox)
        pyButtons=[(("Load...","loadscript.png"),self.OnLoadPY),(("Clear","clearscript.png"),self.OnClearPY),(("[]","stopscript.png"),self.OnStopPY),((">","startscript.png"),self.OnRunPY)]
        self.scriptButtons={}
        for col,(label,fn) in enumerate(pyButtons):
            button,button_id=_make_button(pyButtonBox,label,fn)
            pyButtonBox.columnconfigure(col,weight=1)            
            button.grid(row=0,column=col,sticky="EW")
            self.scriptButtons[button_id]=button

        self.scriptNameLabel.grid(sticky=tk.E+tk.W)
        self.scriptStatus.grid(sticky=tk.E+tk.W)
        pyButtonBox.grid(sticky=tk.E+tk.W)
        self.captureScriptButton.grid(sticky=tk.E+tk.W)
        self.runLocalButton.grid(pady=(10,0),sticky=tk.E+tk.W)
        self.runRemoteButton.grid(sticky=tk.E+tk.W)
        self.setAddressButton.grid(sticky=tk.E+tk.W)
        scriptBox.columnconfigure(0,weight=1)        
        scriptBox.grid(row=7,columnspan=2,sticky=tk.E+tk.W,padx=(0,10))
        
        if sys.platform == "darwin": 
            root.bind("<Button-2>", self.OnContextMenu)
        else:
            root.bind("<Button-3>", self.OnContextMenu)
        
        self.player=None
        self.scriptPath=None
        self.scriptRunner=None
        self.remoteScript=False
        self.remoteAddress=""
        self.lastAssignments={}
        self.settingsFile=None
        self.csvPath=None
        self.nextCaptureFile=None
        if len(sys.argv)>1:
            self.settingsFile=sys.argv[1]
            self.loadSettingsIni(sys.argv[1])
            if self.settingsFile!=None:
               self.root.wm_title("GrovePi Emulator - %s"%self.settingsFile)
        else:
            self.loadSettingsIni(os.path.join(_mainPath,"grovepiemu.ini"),True)
        self.root.after(50,self.update)
        
    def OnWritePython(self,event=None):
        options={}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('Python script', '.py')]
        options['parent'] = self.root
        options['title'] = 'Generate a python script to capture current sensor setup'    
        filename=tkfd.asksaveasfilename(**options)
        if not filename:
            return
        pythonText=gpe_utils.generatePython(list(self.componentList.values()))
        file=open(filename,"wb")
        file.write(pythonText.encode("ASCII"))
        file.close()
        self.scriptPath=filename
            

        
    def OnSetRemote(self):
        oldAddress="dis@"
        if self.remoteAddress!=None:
            oldAddress=self.remoteAddress
        newAddress= tksd.askstring(parent=self.root,prompt="Enter the username and host of the Raspberry Pi to run the script on\nin the format: username@192.168.1.1",title="Run script remotely",initialvalue=oldAddress)
        if newAddress==None:
            return
        if newAddress.find("@")<0:
            tkm.showwarning("Bad address",message="Address should be in the format username@address\nOn the lab Raspberry Pis, username is usually dis, and address looks like 10.N.N.N")
            return
        self.remoteAddress=newAddress
        
    def OnRunRemote(self):
        if self.remoteAddress==None or len(self.remoteAddress)==0:
            self.OnSetRemote()
        if self.remoteAddress!=None and len(self.remoteAddress)>0:
            self.remoteScript=True
            self.OnRunPY()

    def OnRunLocal(self):
        self.remoteScript=False
        self.OnRunPY()
        
            
    def OnCaptureToFile(self):
        if self.scriptRunner!=None and self.scriptRunner.capturing() and self.scriptRunner.running():
            self.OnStopPY()
        else:
            options={}
            options['defaultextension'] = '.csv'
            options['filetypes'] = [('CSV file', '.csv')]
            options['parent'] = self.root
            options['title'] = 'Save script output to file'    
            filename=tkfd.asksaveasfilename(**options)
            if not filename:
                return
            self.nextCaptureFile=filename
            self.OnRunPY()
            
    def OnClearPY(self):
        self.scriptPath=None
        self.OnRunPY()
            
    def OnLoadPY(self,reloadCurrent=False,start=True):
        if not reloadCurrent:
            options={}
            options['defaultextension'] = '.py'
            options['filetypes'] = [('Python file', '.py')]
            options['parent'] = self.root
            options['title'] = 'Open python script to run'    
            filename=tkfd.askopenfilename(**options)
            if not filename:
                return
            self.scriptPath=filename
        if self.scriptPath==None:
            self.scriptNameLabel.config(text="No python script loaded")
        else:
            self.scriptNameLabel.config(text="Python script: %s"%os.path.basename(self.scriptPath))
        if start:
            self.OnRunPY()
        
    def OnRunPY(self):
        if self.scriptRunner!=None and self.scriptRunner.running():
            self.scriptRunner.stop()            
        if self.scriptPath==None:
            self.scriptNameLabel.config(text="No python script loaded")
        else:
            if self.remoteScript:
                self.scriptNameLabel.config(text="Python script: %s"%os.path.basename(self.scriptPath))
                self.scriptRunner=gpe_utils.RemoteRunner(self.scriptPath,self.remoteAddress,captureFile=self.nextCaptureFile)
            else:
                self.scriptNameLabel.config(text="Python script: %s"%os.path.basename(self.scriptPath))
                self.scriptRunner=gpe_utils.StoppableRunner(self.scriptPath,captureFile=self.nextCaptureFile)
            self.nextCaptureFile=None
    
    def OnStopPY(self):
        if self.scriptRunner!=None and self.scriptRunner.running():
            self.scriptRunner.stop()
        
    def OnServerConnect(self,reloadCurrent=False):
        if not reloadCurrent:
            oldPath="http://www.cs.nott.ac.uk/~pszjm2/sensordata/?id=1"
            if self.csvPath!=None and self.csvPath.lower().startswith("http://"):
                oldPath=self.csvPath
            csvPath= tksd.askstring(parent=self.root,prompt="Enter a URL to remote sensor data",title="Connect to sensor server",initialvalue=oldPath)
            if csvPath==None:
                return
            self.csvPath=csvPath
            if not self.csvPath.lower().startswith("http://"):
                self.csvPath="http://"+self.csvPath
        if self.player!=None:
            self.player.unload()
            self.player=None
            self.csvName.config(text="Replay data: ")
        if self.csvPath!=None:
            try:
                self.player=gpe_utils.ServerPlayer(self.csvPath)
                self.csvName.config(text="Replay url: %s (need to set mapping)"%(self.player.getName()))
                self.OnMapCSV(reloadCurrent=reloadCurrent)
            except IOError:
                self.player=None
                self.csvName.config(text="Replay data: ")
                self.csvPath=None

    def OnJSONConnect(self,reloadCurrent=False):
        if not reloadCurrent:
            oldPath="http://www.cs.nott.ac.uk/~jqm/sensorvalues.php?id=2"
            if self.csvPath.lower().startswith("http://"):
                oldPath=self.csvPath
            csvPath= tksd.askstring(parent=self.root,prompt="Enter a URL to remote sensor data",title="Connect to JSON Sensor Server",initialvalue=oldPath)
            if csvPath==None:
                return
            self.csvPath=csvPath
            if not self.csvPath.lower().startswith("http://"):
                self.csvPath="http://"+self.csvPath
        if self.player!=None:
            self.player.unload()
            self.player=None
            self.csvName.config(text="Replay data: ")
        if self.csvPath!=None:
            self.player=gpe_utils.JSONPlayer(self.csvPath)
            self.csvName.config(text="Replay url: %s (need to set mapping)"%(self.player.getName()))
            self.OnMapCSV(reloadCurrent=reloadCurrent)
            
            
    def OnUnloadCSV(self):
        if self.player!=None:
            self.player.unload()       
            self.player=None
            self.csvName.config(text="Replay data: ")
            self.csvPath=""
        
        
    def OnLoadCSV(self,reloadCurrent=False):
        if not reloadCurrent:
            options={}
            options['defaultextension'] = '.csv'
            options['filetypes'] = [('CSV file', '.csv')]
            options['parent'] = self.root
            options['title'] = 'Open CSV file for data playback'    
        
            filename=tkfd.askopenfilename(**options)
            if not filename:
                return
            self.csvPath=filename
        if self.player!=None:
            self.player.unload()       
            self.player=None
            self.csvName.config(text="Replay data: ")
        if self.csvPath!=None:
            self.player=gpe_utils.CSVPlayer(self.csvPath)
            self.csvName.config(text="Replay data: %s (need to set mapping)"%(self.player.getName()))
            self.OnMapCSV(reloadCurrent=reloadCurrent)

    def findComponentByName(self,name):
        for c in list(self.componentList.values()):
            if c.title()==name:
                return c
        return None
        
    def OnMapCSV(self,reloadCurrent=False):
        if self.player==None:
            return
        if not reloadCurrent:        
            mapdlg=gpe_utils.CSVMappingDlg(self.root,self.player.getFieldNames(),list(self.componentList.values()),self.lastAssignments,isinstance(self.player,gpe_utils.CSVPlayer))
            assignments=mapdlg.getAssignments()
            if assignments==None:
                return
            self.lastAssignments=assignments
        assignmentsFixed={}
        timeColumn=None
        for (col,dests) in list(self.lastAssignments.items()):
            assignmentsFixed[col]=[]
            for dest in dests:
                if type(dest)==tuple or type(dest)==list:
                    colDesc=(self.findComponentByName(dest[0]),dest[1])
                    if colDesc[0]!=None:
                        assignmentsFixed[col].append(colDesc)
                elif dest=="TIME":
                    timeColumn=col
                else:
                    colDesc=self.findComponentByName(dest)
                    if colDesc!=None:
                        assignmentsFixed[col].append(colDesc)
        if isinstance(self.player,gpe_utils.ServerPlayer):
            if len(assignmentsFixed)>0:
                self.player.setFieldAssignments(assignmentsFixed)
                self.csvName.config(text="Replay data: %s"%(self.player.getName()))
                self.player.startPlaying(self.root,False)
        else:
            if timeColumn!=None and len(assignmentsFixed)>0:
                self.player.setFieldAssignments(timeColumn,assignmentsFixed)
                self.csvName.config(text="Replay data: %s"%(self.player.getName()))
        
    def OnStopCSV(self):
        if self.player!=None:
            self.player.stopPlaying()
        
    def OnPauseCSV(self):
        if self.player!=None:
            self.player.pausePlaying()
        
    def OnPlayCSV(self):
        if self.remoteScript:
            tkm.showwarning("CSV Playback only works locally",message="You can only play CSV files back in the emulator,\nthe PI always uses real sensors.\nSwitching to emulated script.")
            if self.scriptRunner!=None and self.scriptRunner.running():            
                self.scriptRunner.stop()               
                self.OnRunLocal()
        if self.player!=None:
            if self.player.playing():
                self.player.stopPlaying()
            self.player.startPlaying(self.root,False)
            
    def OnSave(self,event=None):
        if self.settingsFile==None:
            self.OnSaveAs()
        else:
            self.saveSettingsIni(self.settingsFile)

    def OnNew(self,event=None):
        removals=[]
        for (pin,type) in list(self.componentList.keys()):
            removals.append((pin,type))
        for (pin,type) in removals:
            self.removeComponent(pin,type)
        if self.player!=None:
            self.player.unload()       
            self.player=None
            self.csvName.config(text="Replay data: ")
        if self.scriptRunner!=None and self.scriptRunner.running():
            self.scriptRunner.stop()
        self.scriptPath=None
        self.scriptNameLabel.config(text="GrovePi Python Script: ")
        self.csvPath=None
            
    def OnSaveAs(self,event=None):
        options={}
        options['defaultextension'] = '.gpi'
        options['filetypes'] = [('GrovePI emulator settings file', '.gpi')]
        options['parent'] = self.root
        options['title'] = 'Save GrovePI emulator settings'    
        filename= tkfd.asksaveasfilename(**options)
        if not filename:
            return
        self.settingsFile=filename
        self.root.wm_title("GrovePi Emulator - %s"%self.settingsFile)
        self.saveSettingsIni(self.settingsFile)
    
    
    def OnOpen(self,event=None):
        options={}
        options['defaultextension'] = '.gpi'
        options['filetypes'] = [('GrovePI emulator settings file', '.gpi')]
        options['parent'] = self.root
        options['title'] = 'Save GrovePI emulator settings'    
        filename= tkfd.askopenfilename(**options)
        if not filename:
            return
        self.settingsFile=filename
        self.root.wm_title("GrovePi Emulator - %s"%self.settingsFile)
        self.loadSettingsIni(self.settingsFile)
        
    def OnAbout(self):
        description="""Emulation environment for running python programs developed for the GrovePI sensor board.
Currently has support for the following sensors:

"""
        for c in components.allSensors:
            description+=c.classDescription()+"\n"
        description+="\nBy Joe Marshall\nhttp://www.cs.nott.ac.uk/~pszjm2\n\nDo what you want with the code. Any questions, email joe.marshall@nottingham.ac.uk "
        tkm.showinfo("Grove PI Emulation Environment 3.1",message=description)

    
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
                for (pinType,(moduleName,config)) in list(modules.items()):
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
                        self.OnServerConnect(reloadCurrent=True)
                    else:
                        self.OnLoadCSV(True)
                else:
                    self.OnUnloadCSV()
                if fromIni:
                    self.remoteAddress=None
                    self.remoteScript=False
                else:
                    self.remoteScript=allConfig["remoteScript"]
                    self.remoteAddress=allConfig["remoteAddress"]
                self.OnLoadPY(reloadCurrent=True,start=False)

 #               if fromIni:
 #                   self.settingsFile=self.fullPath(allConfig["currentFileOpen"],name) 
 #                   if self.settingsFile!=None:
 #                       self.SetTitle("GrovePi Emulator - %s"%self.settingsFile)

        except IOError:
            print( "Couldn't load config ",name)
        except KeyError:
            print("Key missing")
        except ValueError:
            print("JSON config object bad")

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
            allConfig={}
            modules={}
            for (pin,type),component in list(self.componentList.items()):
                modConfig=None
                if hasattr(component,"saveConfig"):
                    modConfig=component.saveConfig()
                modules["%d%s"%(pin,type)]=[component.classDescription(),modConfig]
            allConfig["modules"]=modules
            
            allConfig["pythonScript"]=self.relPath(self.scriptPath,name)
            allConfig["sensorAssignments"]=self.lastAssignments
            if self.csvPath!=None and len(self.csvPath)>0:
                allConfig["csvPath"]=self.relPath(self.csvPath,name)
            else:
                allConfig["csvPath"]=""
            allConfig["remoteScript"]=self.remoteScript
            allConfig["remoteAddress"]=self.remoteAddress
#            allConfig["currentFileOpen"]=self.relPath(self.settingsFile,name)
            with open(name,'w') as file:
                json.dump(allConfig,file)
        except IOError:
            print("Couldn't save settings file")
    
    # a)which things are connected 
# b)any config settings on them e.g.LED colour, generic digital pullup (and what?). Most modules won't have any config I think
# c)the name/path of the currently loaded python script
# d)the (last)mapping for playback
# e)currently loaded csv file
        None
        
    def OnContextMenu(self,event):
        x,y=event.x_root,event.y_root
        for (pin,type),sizer in list(self.containerSizers.items()):
            wx=sizer.winfo_rootx()
            wy=sizer.winfo_rooty()
            ww=sizer.winfo_width()
            wh=sizer.winfo_height()
            menu = tk.Menu(self.root, tearoff=0)
            
            if x>=wx and x<wx+ww and y>=wy and y<wy+wh:                
                if type=="D":                
                    for index,classObj in enumerate(components.digitalSensors):
                        menu.add_command(label=classObj.classDescription(),command=lambda i=index,p=pin: self.OnSelectDig(i+1,p))
                    menu.add_separator()
                    for index,classObj in enumerate(components.digitalOutputs):
                        menu.add_command(label=classObj.classDescription(),command=lambda i=index,p=pin: self.OnSelectDig(i+1000,p))
                elif type=="A":
                    for index,classObj in enumerate(components.analogSensors):
                        menu.add_command(label=classObj.classDescription(),command=lambda i=index,p=pin: self.OnSelectAna(i+1,p))
                elif type=="I":
                    for index,classObj in enumerate(components.i2cConnections):
                        menu.add_command(label=classObj.classDescription(),command=lambda i=index,p=pin: self.OnSelectI2c(i+1,p))

                if (pin,type) in self.componentList:
                    menu.add_separator()
                    self.selectedComponent=(pin,type)
                    menu.add_command(label="Disconnect "+self.componentList[(pin,type)].title(),command=self.OnDeleteComponent)
                    
                self.menuSelection=None
                menu.tk_popup(x,y,0)

    def OnSelectDig(self,index,pin):
        if index<1000:
            self.addComponent(components.digitalSensors[index-1](pin),"D")
        else:
            self.addComponent(components.digitalOutputs[index-1000](pin),"D")
        
    def OnSelectAna(self,index,pin):
        self.addComponent(components.analogSensors[index-1](pin),"A")

    def OnSelectI2c(self,index,pin):
        self.addComponent(components.i2cConnections[index-1](pin),"I")
        
    def OnDeleteComponent(self):
        self.removeComponent(*self.selectedComponent)

        
    def addComponent(self,component,type):
        pin=component.pin
        self.removeComponent(pin,type,replacing=True)
        self.componentList[(pin,type)]=component
        if hasattr(component,"initPropertyPage"):
            self.properties.addSensorObject(component,type)
        sizer=self.subSizers[(pin,type)]
        component.initSmall(sizer)
                
    def removeComponent(self,pin,type,replacing=False):
        if (pin,type) in self.componentList:
            component=self.componentList[(pin,type)]
            if hasattr(component,"onComponentDestroy"):
                component.onComponentDestroy()
            del(self.componentList[(pin,type)])
            self.properties.removeSensorObject(component)
        sizer=self.subSizers[(pin,type)]
        for child in sizer.winfo_children():
            child.destroy()
        if not replacing:
            dummy=tk.Label(sizer,text="Right click to connect sensor")
            dummy.pack()
        
        
            
    def update(self):
        for component in list(self.componentList.values()):
            if hasattr(component,"update"):
                component.update()
        if self.player!=None:
            ofsTime,realTime=self.player.getTimes()
            self.csvTimeStart.config(text=time.strftime("%H:%M:%S",time.gmtime(ofsTime)))
            self.csvTimeReal.config(text=time.strftime("%H:%M:%S (%d/%m/%Y)",time.gmtime(realTime)))
        if self.player==None or not self.player.playing():
            self.csvButtons[">"].config(bg="pale green",relief=tk.RAISED)
            if self.player!=None and self.player.paused():
                self.csvButtons["[]"].config(bg="#ff9f9f",relief=tk.RAISED)
                self.csvButtons["||"].config(bg="red",relief=tk.SUNKEN)           
            else:
                self.csvButtons["[]"].config(bg="red",relief=tk.SUNKEN)
                self.csvButtons["||"].config(bg="#ff9f9f",relief=tk.RAISED)
        else:
            self.csvButtons[">"].config(bg="#00ff00",relief=tk.SUNKEN)
            self.csvButtons["[]"].config(bg="#ff9f9f",relief=tk.RAISED)
            self.csvButtons["||"].config(bg="#ff9f9f",relief=tk.RAISED)
        self.captureScriptButton.config(bg="gray80")
        self.captureScriptButton.config(text="Capture script to file")
        if self.remoteScript:
            self.runRemoteButton.config(bg="#7fff7f")
            self.runLocalButton.config(bg="gray80")
        else:
            self.runRemoteButton.config(bg="gray80")
            self.runLocalButton.config(bg="#7f7fff")

        
        if self.scriptRunner!=None:
            if self.scriptRunner.running():
                self.scriptStatus.config(text="Running")
                if self.remoteScript:
                    self.scriptStatus.config(text="Run at: %s"%self.remoteAddress)                
                else:
                    self.scriptStatus.config(text="Running in emulator")                
                if self.scriptRunner.capturing():
                    self.captureScriptButton.config(bg="#ff7f7f")
                    self.captureScriptButton.config(text="Stop capturing")                
            else:
                self.scriptStatus.config(text="Stopped")                
        else:
            self.scriptStatus.config(text="Stopped")
        self.root.after(50,self.update)
        
        
    def OnClose(self,event=None):
        if self.scriptRunner!=None and self.scriptRunner.running():
            self.scriptRunner.stop()
        self.saveSettingsIni(os.path.join(_mainPath,"grovepiemu.ini"))
        self.root.quit()



        
root =tk.Tk()                             #main window
root.tk_setPalette(background='#fff')
root.iconbitmap(os.path.join(_mainPath,"main.ico"))
top = Frame(root,"GrovePi Emulator - <untitled>")
root.geometry('800x700')#'%dx%d+0+0'%(root.winfo_width()+1, root.winfo_height()+1))
#top.Show()

try:
    root.mainloop()
except KeyboardInterrupt:
    top.OnClose()
    
