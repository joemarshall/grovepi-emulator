
import grovegyro

from gpe_utils.tkimports import *
from . import propgrid


class GroveGyro:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.axisNames=["acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z"]
        
    def title(self):
        return "I2C-%d: Grove Six Axis Gyro"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Six Axis Gyro/Accelerometer"

    def initSmall(self,parent):
        self.titleLabel=tk.Label(parent,text=self.title())
        self.titleLabel.grid()
        self.labelG=tk.Label(parent,text="Gyro: +00.000 +00.000 +00.000",font="Courier")
        self.labelG.grid()
        self.labelA=tk.Label(parent,text=" Acc: +00.000 +00.000 +00.000",font="Courier")
        self.labelA.grid()
        
    def initPropertyPage(self,parent):
        self.propGrid=propgrid.PropertyGrid(parent,title=self.title())        
        self.axProp=propgrid.FloatProperty("acc_x",value=0)
        self.ayProp=propgrid.FloatProperty("acc_y",value=0)
        self.azProp=propgrid.FloatProperty("acc_z",value=0)
        self.gxProp=propgrid.FloatProperty("gyro_x",value=0)
        self.gyProp=propgrid.FloatProperty("gyro_y",value=0)
        self.gzProp=propgrid.FloatProperty("gyro_z",value=0)
        self.propGrid.Append( self.axProp )
        self.propGrid.Append( self.ayProp )
        self.propGrid.Append( self.azProp )
        self.propGrid.Append( self.gxProp )
        self.propGrid.Append( self.gyProp )
        self.propGrid.Append( self.gzProp )
        self.propGrid.SetCallback(self.OnPropGridChange)
        self.propGrid.pack()
        
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
        properties=[self.axProp,self.ayProp,self.azProp,self.gxProp,self.gyProp,self.gzProp]
        if axisIndex<3:
            grovegyro.accVals[axisIndex]=value
            self.labelA.config(text="Acc: {: 7.3f} {: 7.3f} {: 7.3f}".format(*grovegyro.accVals))
        else:
            grovegyro.gyroVals[axisIndex-3]=value
            self.labelG.config(text="Gyr: {: 7.3f} {: 7.3f} {: 7.3f}".format(*grovegyro.gyroVals))
        properties[axisIndex].SetValue(value)
        
    def getCSVCode(self):
        return {"imports":["sensors"],"pin_mappings":["\"gyro%d\":%d"%(self.pin,self.pin),"\"accel%d\":%d"%(self.pin,self.pin)],"reader":["sensors.gyro%d.get_xyz()"%self.pin,"sensors.accel%d.get_xyz()"%self.pin],"variable":["gyro%d_x,gyro%d_y,gyro%d_z"%(self.pin,self.pin,self.pin),"accel%d_x,accel%d_y,accel%d_z"%(self.pin,self.pin,self.pin)],"type":'%f,%f,%f'}
                