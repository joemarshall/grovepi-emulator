
import grovepi


from gpe_utils.tkimports import *
from . import propgrid



class GroveDHT:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.axisNames=["temperature","humidity"]
        self.valueH=tk.DoubleVar()
        self.valueT=tk.DoubleVar()

    def title(self):
        return "D-%d: Grove Humidity & Temperature"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Digital Humidity & Temperature"

    def initSmall(self,parent):
        self.titleLabel=tk.Label(parent,text=self.title())
        self.titleLabel.grid(columnspan=2)
        self.tLabel=tk.Label(parent,text="Temp:")
        self.tLabel.grid(column=0,row=1)
        self.hLabel=tk.Label(parent,text="Humidity:")
        self.hLabel.grid(column=0,row=2)

        self.sliderT=tk.Scale(parent,from_=0,to=100,resolution=0.1,orient=tk.HORIZONTAL,command=self.OnSliderChange,variable=self.valueT)
        self.sliderH=tk.Scale(parent,from_=0,to=100,resolution=0.1,orient=tk.HORIZONTAL,command=self.OnSliderChange,variable=self.valueH)
        self.sliderT.grid(column=1,row=1,sticky=tk.W+tk.E)
        self.sliderH.grid(column=1,row=2,sticky=tk.W+tk.E)
 

#    self.label=tk.Label(parent,text="T: 0.00 H:0.00",font="Courier")
#        self.label.grid()
    def OnSliderChange(self,event):
        self.setValue(0,self.valueT.get())
        self.setValue(1,self.valueH.get())
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.tProp=propgrid.FloatProperty("temperature",value=0)
        self.hProp=propgrid.FloatProperty("humidity",value=0)
        self.propGrid.Append( self.tProp )
        self.propGrid.Append( self.hProp )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()
        
    def OnPropGridChange(self,property,value):
        axisIndex=self.axisNames.index(property)
        self.setValue(axisIndex,float(value))
        
    def update(self):
        None
        
    def getNumAxes(self):
        return 2
        
    def getAxisName(self,num):
        return self.axisNames[num]
        
    def setValue(self,axisIndex,value):
        properties=[self.tProp,self.hProp]
        if axisIndex<2:
            grovepi.DHTVals[self.pin][axisIndex]=value
            t,h=grovepi.DHTVals[self.pin]
        properties[axisIndex].SetValue(value)
        [self.valueT,self.valueH][axisIndex].set(value)
        
    def getCSVCode(self):
        return {"imports":["sensors"],"pin_mappings":["\"dht%d\":%d"%(self.pin,self.pin)],"reader":"sensors.dht%d.get_level()"%self.pin,"variable":"temp%d,humidity%d"%(self.pin,self.pin),"type":'%f,%f'}
                