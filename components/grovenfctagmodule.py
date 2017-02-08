from __future__ import absolute_import
import grovenfctag

from gpe_utils.tkimports import *
from . import propgrid


class GroveNFCTagModule:


    def __init__(self,pin):
        self.pin=pin
        self.currentDataPoint=None
        self.doValidate=True
    
    def title(self):
        return "I2C-%d: Grove NFC Tag:"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove NFC Tag"
    
    def validateHex(self,value):
        valid=True
        for char in value:
            if not char in "0123456789ABCDEFabcdef":
                valid=False
        return valid

    def validateHex2(self,value,insertPoint,actionCode,insertText,widgetFullname):
        valid=True
        index=int(widgetFullname.split(".")[-1])
        if self.doValidate:        
            self.insertPoint=None
            for char in value:
                if not char in "0123456789ABCDEFabcdef":
                    valid=False
            if len(value)>2 and valid:
                valid=False
                if actionCode=="1" and len(insertText)==1:
                    insertPoint=int(insertPoint)
                    if insertPoint<2:
                        self.doValidate=False
                        self.dataPoints[index].delete(insertPoint,insertPoint+1)
                        self.dataPoints[index].insert(insertPoint,insertText)
                        self.dataPoints[index].after_idle(lambda dp=self.dataPoints[index]: dp.config(validate='key'))
                        self.OnDataPointChanged(index)
                        self.doValidate=True
                    elif index<15:
                        self.dataPoints[index+1].focus_set()
                        self.dataPoints[index+1].insert(0,insertText)
                        self.dataPoints[index+1].icursor(1)
            if valid and len(value)>0:
                self.OnDataPointChanged(index,int(value,16))
        return valid
        

        
    def initSmall(self,parent):
        self.titleLabel=tk.Label(parent,text=self.title())
        self.titleLabel.grid(row=0,columnspan=4)

        self.vcmd=parent.register(self.validateHex)
        
        
        self.blockLabel=tk.Label(parent,text="Block address: 0x")
        self.blockLabel.grid(row=1,column=0)
        
        self.blockEdit=tk.Entry(parent,validate="key",validatecommand=(self.vcmd,'%P'))
        self.blockEdit.insert(0,"000")
        self.blockEdit.grid(row=1,column=1,columnspan=3)

        self.dataPoints=[]
        vcmd2=parent.register(self.validateHex2)

        for c in range(0,16):
            dataPointEdit=tk.Entry(parent,name="%d"%c,validate="key",width=2,font="Courier",validatecommand=(vcmd2,'%P','%i','%d','%S','%W'))
            dataPointEdit.bind("<FocusIn>",lambda event,val=c,s=self:s.OnEnterDataPoint(val) )
            dataPointEdit.bind("<FocusOut>",lambda event,val=c,s=self:s.OnLeaveDataPoint(val) )
            self.dataPoints.append(dataPointEdit)
            dataPointEdit.grid(row=2+c/4,column=c%4)
            
    def OnEnterDataPoint(self,pointNum):
        self.currentDataPoint=pointNum

    def OnLeaveDataPoint(self,pointNum):
        if self.currentDataPoint==pointNum:
            self.OnDataPointChanged(pointNum)
            self.currentDataPoint=None                
        
    def OnDataPointChanged(self,index,value=None):
        try:        
            blockAddress=int(self.blockEdit.get(),16)
        except ValueError:
            blockAddress=0
        if value==None:
            try:
                value=int(self.dataPoints[index].get(),16)
            except ValueError:
                value=0
        grovenfctag.NFCBuffer[blockAddress+index]=value
        
    def update(self):
        try:        
            blockAddress=int(self.blockEdit.get(),16)
        except ValueError:
            blockAddress=0
        for i,c in enumerate(self.dataPoints):
            thisVal="%02X"%grovenfctag.NFCBuffer[blockAddress]
            if (not i==self.currentDataPoint) and c.get()!=thisVal:
                self.doValidate=False
                c.delete(0,tk.END)
                c.insert(0,"%02X"%grovenfctag.NFCBuffer[blockAddress])
                self.doValidate=True
            blockAddress+=1
