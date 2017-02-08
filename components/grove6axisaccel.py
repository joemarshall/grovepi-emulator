from __future__ import absolute_import
import grove6axis

from gpe_utils.tkimports import *
from . import propgrid



class GroveSixAxisAccelerometer:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.axisNames=["acc_x","acc_y","acc_z","mag_x","mag_y","mag_z"]
        
    def title(self):
        return "I2C-%d: Grove Six Axis Accel/Magnetometer"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Six Axis Accel/Magnetometer"

    def initSmall(self,parent):
        self.titleLabel=tk.Label(parent,text=self.title())
        self.titleLabel.grid()
        self.labelM=tk.Label(parent,text="Mag: +00.000 +00.000 +00.000",font="Courier")
        self.labelM.grid()
        self.labelA=tk.Label(parent,text="Acc: +00.000 +00.000 +00.000",font="Courier")
        self.labelA.grid()
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
        properties=[self.axProp,self.ayProp,self.azProp,self.mxProp,self.myProp,self.mzProp]
        if axisIndex<3:
            grove6axis.accVals[axisIndex]=value
            self.labelA.config(text="Acc: {: 7.3f} {: 7.3f} {: 7.3f}".format(*grove6axis.accVals))
        else:
            grove6axis.magVals[axisIndex-3]=value
            self.labelM.config(text="Mag: {: 7.3f} {: 7.3f} {: 7.3f}".format(*grove6axis.magVals))
        properties[axisIndex].SetValue(value)
        
    def getCSVCode(self):
        return {"imports":["grove6axis"],"readall":"(acc_x,acc_y,acc_z),(mag_x,mag_y,mag_z)=grove6axis.getAccel(),grove6axis.getMag()","variables":["acc_x","acc_y","acc_z","mag_x","mag_y","mag_z"],"types":["%f","%f","%f","%f","%f","%f"]}
                