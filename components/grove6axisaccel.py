import grove6axis

import wx
import wx.propgrid as wxpg

class GroveSixAxisAccelerometer:
    
    def __init__(self,inputNum):
        self.pin=inputNum
        self.value=0
        self.axisNames=["acc_x","acc_y","acc_z","mag_x","mag_y","mag_z"]
        
    def title(self):
        return "I2C-%d: Grove Six Axis Accel/Magnetometer"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove Six Axis Accel/Magnetometer"

    def initSmall(self,parent,sizer):
        self.titleLabel=wx.StaticText(parent,wx.ID_ANY,self.title(),style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        sizer.Add(self.titleLabel,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        self.labelM=wx.StaticText(parent,wx.ID_ANY,"Mag: +00.000 +00.000 +00.000",style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        self.labelA=wx.StaticText(parent,wx.ID_ANY,"Acc: +00.000 +00.000 +00.000",style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
        oldFont=self.labelM.GetFont()
        newFont=wx.Font(oldFont.PointSize,wx.FONTFAMILY_TELETYPE,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.labelA.SetFont(newFont)
        self.labelM.SetFont(newFont)        
        sizer.Add(self.labelA,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        sizer.Add(self.labelM,flag=wx.EXPAND|wx.ALIGN_CENTER,proportion=1)
        self.setValue(0,0.0)
        self.setValue(1,10.0)
        self.setValue(2,-5.0)
        
    def initPropertyPage(self,parent,sizer):
        self.propGrid=wxpg.PropertyGrid(parent, wx.ID_ANY, style=wx.propgrid.PG_SPLITTER_AUTO_CENTER| wx.propgrid.PG_AUTO_SORT)        
        self.axProp=wxpg.FloatProperty("acc_x",value=0)
        self.ayProp=wxpg.FloatProperty("acc_y",value=0)
        self.azProp=wxpg.FloatProperty("acc_z",value=0)
        self.mxProp=wxpg.FloatProperty("mag_x",value=0)
        self.myProp=wxpg.FloatProperty("mag_y",value=0)
        self.mzProp=wxpg.FloatProperty("mag_z",value=0)
        self.propGrid.Append( self.axProp )
        self.propGrid.Append( self.ayProp )
        self.propGrid.Append( self.azProp )
        self.propGrid.Append( self.mxProp )
        self.propGrid.Append( self.myProp )
        self.propGrid.Append( self.mzProp )
        self.propGrid.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        sizer.Add(self.propGrid,flag=wx.EXPAND)
        
    def OnPropGridChange(self,event):
        axisIndex=self.axisNames.index(event.GetPropertyName())
        self.setValue(axisIndex,float(event.GetPropertyValue()))            
        
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
            self.labelA.SetLabel("Acc: {: 7.3f} {: 7.3f} {: 7.3f}".format(*grove6axis.accVals))
        else:
            grove6axis.magVals[axisIndex-3]=value
            self.labelM.SetLabel("Mag: {: 7.3f} {: 7.3f} {: 7.3f}".format(*grove6axis.magVals))
        properties[axisIndex].SetValue(value)
        
                