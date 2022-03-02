
import grovepi

from .grovebutton import *


class GrovePIR(GroveButton):
    
    def __init__(self,inputNum):
        GroveButton.__init__(self,inputNum)
        self.value=tk.IntVar()
        self.callbackID=None
        
    def title(self):
        return "D%d: Grove PIR"%self.pin

    def initSmall(self,parent):
    #todo
        self.button=ttk.Checkbutton(parent, text=self.title(), style='Toggle.TButton',variable=self.value)
        self.button.bind("<Button-1>",self.OnButtonDown)
        self.button.bind("<ButtonRelease-1>",self.OnButtonUp)
        self.button.pack()

    def OnButtonDown(self,event):
        if self.callbackID!=None:
            self.button.after_cancel(self.callbackID)
        self.setValue(True)

    def OnButtonUp(self,event):
        self.callbackID=self.button.after(5000,self.release)

        
    def release(self):
        self.callbackID=None
        self.setValue(False)
        self.value.set(False)
        
    @classmethod
    def classDescription(cls):
        return "Grove PIR"


    def onComponentDestroy(self):
        None

    def getCSVCode(self):
        return {"imports":["sensors"],"pin_mappings":["\"pir%d\":%d"%(self.pin,self.pin)],"reader":"sensors.pir%d.get_level()"%self.pin,"variable":"pir%d"%self.pin}
        