from __future__ import print_function
from gpe_utils.tkimports import *


class PropertyGrid(tk.Frame):

    def __init__(self,parent,title):
        tk.Frame.__init__(self,parent)
        title=tk.Label(self,text=title,bg="black",fg="white")        
        title.grid(row=0,column=0,columnspan=2)
        self.properties=[]
        self.callback=None
        
    def Append(self,property):
        self.properties.append(property)        
        property._makeRow(self,len(self.properties))
        
    def SetCallback(self,callback):
        self.callback=callback
        
    def OnPropertyChange(self,prop,value=None):
        if self.callback!=None:
            if value==None:
                self.callback(prop.title,prop.GetValue())
            else:
                self.callback(prop.title,value)

class BoolProperty:
    def __init__(self,title,value):
        self.value=tk.BooleanVar()
        self.value.set(value)
        self.title=title

    def SetValue(self,value):
        self.value.set(value)
        
    def GetValue(self):
        return self.value.get()
       
    def _makeRow(self,rowParent,rowNum):
        label=tk.Label(rowParent,text=self.title)
        label.grid(row=rowNum,column=0)
        checkBox=tk.Checkbutton(rowParent,command=lambda s=self:rowParent.OnPropertyChange(s),variable=self.value)
        checkBox.grid(row=rowNum,column=1)
        
class IntProperty:
    def __init__(self,title,value,minVal=0,maxVal=1023):
        self.value=tk.StringVar()
        self.value.set(value)
        self.title=title
        self.minVal=minVal
        self.maxVal=maxVal
        self.inValidate=False

    def SetValue(self,value):
        if self.inValidate:
            # avoid recursing through setters & validation
            return
        self.value.set("%d"%value)

    def GetValue(self):
        return int(self.value.get())
        
    def validate(self,value):
        valid=True
        self.inValidate=True
        try:
            self.rowParent.OnPropertyChange(self,int(value))
        except ValueError:
            if value!="":
                valid=False
        self.inValidate=False
        return valid
       
    def _makeRow(self,rowParent,rowNum):
    
        self.vcmd=rowParent.register(self.validate)
    
        self.rowParent=rowParent
        label=tk.Label(rowParent,text=self.title)
        label.grid(row=rowNum,column=0)        

        self.spinBox=tk.Spinbox(rowParent,from_=self.minVal,to=self.maxVal,validate="key",validatecommand=(self.vcmd,'%P'),textvariable=self.value)

        self.spinBox.grid(row=rowNum,column=1)
        
        
class FloatProperty:
    def __init__(self,title,value,minVal=0.0,maxVal=1023.0):
        self.value=tk.StringVar()
        self.value.set(value)
        self.title=title
        self.minVal=minVal
        self.maxVal=maxVal
        self.inValidate=False

    def SetValue(self,value):
        if self.inValidate:
            # avoid recursing through setters & validation
            return
        self.value.set("%.1f"%value)

    def GetValue(self):
        return float(self.value.get())
        
    def validate(self,value):
        valid=True
        self.inValidate=True
        try:
            self.rowParent.OnPropertyChange(self,float(value))
        except ValueError:
            if value!="" and value!="." and value!="-" and value!="-.":
                valid=False
        self.inValidate=False
        return valid
       
    def _makeRow(self,rowParent,rowNum):
    
        self.vcmd=rowParent.register(self.validate)
    
        self.rowParent=rowParent
        label=tk.Label(rowParent,text=self.title)
        label.grid(row=rowNum,column=0)        

        self.spinBox=tk.Entry(rowParent,validate="key",validatecommand=(self.vcmd,'%P'),textvariable=self.value)
        self.spinBox.grid(row=rowNum,column=1)
                
                
class ColourProperty:
    def __init__(self,title,value):
        self.value=value
        self.title=title

    def SetValue(self,value):
        self.value=value
        
    def GetValue(self):
        return self.value
       
    def _ChooseColour(self):
        newColour=tkcc.askcolor(initialcolor=self.value)
        if newColour!=None and newColour[0]!=None:
            print(newColour)
            self.value=newColour[0]
            self.rowParent.OnPropertyChange(self,self.value)
       
    def _makeRow(self,rowParent,rowNum):
        self.rowParent=rowParent
        label=tk.Label(rowParent,text=self.title)
        label.grid(row=rowNum,column=0)
        button=tk.Button(rowParent,text="    ",command=self._ChooseColour)
        button.grid(row=rowNum,column=1)
                