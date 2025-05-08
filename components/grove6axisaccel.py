
import grove6axis

from gpe_utils.tkimports import *
from . import propgrid



class GroveSixAxisAccelerometer:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.axisNames=["acc_x","acc_y","acc_z","mag_x","mag_y","mag_z"]
        self.formatString="{sensor:4s}: {x: 7.2f} {y: 7.2f} {z: 7.2f}"
        
    def title(self):
        return "I2C-%d: Grove Six Axis Accel/Magnetometer"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Six Axis Accel/Magnetometer"

    def initSmall(self,parent):
        self.titleLabel=ttk.Label(parent,text=self.title())
        self.titleLabel.grid()
        self.labelA=ttk.Label(parent,text=self.formatString.format(sensor="Acc",x=0,y=0,z=0),font="courier")
        self.labelM=ttk.Label(parent,text=self.formatString.format(sensor="Mag",x=0,y=0,z=0),font="courier")
        self.labelA.grid()
        self.labelM.grid()
        self.setValue(0,0.0)
        self.setValue(1,10.0)
        self.setValue(2,-5.0)
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.axProp=propgrid.FloatProperty("acc_x",value=0)
        self.ayProp=propgrid.FloatProperty("acc_y",value=0)
        self.azProp=propgrid.FloatProperty("acc_z",value=0)
        self.mxProp=propgrid.FloatProperty("mag_x",value=0)
        self.myProp=propgrid.FloatProperty("mag_y",value=0)
        self.mzProp=propgrid.FloatProperty("mag_z",value=0)
        self.propGrid.Append( self.axProp )
        self.propGrid.Append( self.ayProp )
        self.propGrid.Append( self.azProp )
        self.propGrid.Append( self.mxProp )
        self.propGrid.Append( self.myProp )
        self.propGrid.Append( self.mzProp )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack(fill=tk.X)
        
    def OnPropGridChange(self,property,value):
        axisIndex=self.axisNames.index(property)
        self.setValue(axisIndex,float(value))            
        
    def update(self):
        None
        
    def getNumAxes(self):
        return 6
        
    def getAxisName(self,num):
        return self.axisNames[num]
        
    def setValue(self,axisIndex,value):
        properties=[self.axProp,self.ayProp,self.azProp,self.mxProp,self.myProp,self.mzProp]
        if axisIndex<3:
            grove6axis.accVals[axisIndex]=value
            x,y,z=grove6axis.accVals
            self.labelA.config(text=self.formatString.format(sensor="Acc",x=x,y=y,z=z))
        else:
            grove6axis.magVals[axisIndex-3]=value
            x,y,z=grove6axis.magVals
            self.labelM.config(text=self.formatString.format(sensor="Mag",x=x,y=y,z=z))
        properties[axisIndex].SetValue(value)
        
    def getCSVCode(self):
        return {"imports":["sensors"],"pin_mappings":["\"magnetometer%d\":%d"%(self.pin,self.pin),"\"accel%d\":%d"%(self.pin,self.pin)],"reader":["sensors.magnetometer%d.get_xyz()"%self.pin,"sensors.accel%d.get_xyz()"%self.pin],"variable":["magnetometer%d_x,magnetometer%d_y,magnetometer%d_z"%(self.pin,self.pin,self.pin),"accel%d_x,accel%d_y,accel%d_z"%(self.pin,self.pin,self.pin)],"type":'%f,%f,%f'}
                