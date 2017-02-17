from __future__ import absolute_import
import grovepi

from .grovebutton import *


class GrovePIR(GroveButton):
    
    def __init__(self,inputNum):
        GroveButton.__init__(self,inputNum)
        self.callbackID=None
        
    def title(self):
        return "D%d: Grove PIR"%self.pin

    def initSmall(self,parent):
        self.button=tk.Button(parent,text=self.title(),bg="red",activebackground="green")
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
        
    @classmethod
    def classDescription(cls):
        return "Grove PIR"


    def onComponentDestroy(self):
        None

    def getCSVCode(self):
        return {"imports":["grovepi"],"reader":"grovepi.digitalRead(%d)"%self.pin,"variable":"pir%d"%self.pin}
        