import grovepi
import time
import os
import sys
if sys.version_info.major<3:
    import urllib2 as url
else: 
    import urllib.request as url
import json

class JSONPlayer:
    def __init__(self,name):
        self.filename=name

        resp=url.urlopen(self.filename,timeout=5)
        values=json.load(resp)
        self.fields=values.keys()
        temp=[]
        for c in self.fields:
            temp.append("%s-TIME_SINCE_PRESSED"%c)
        self.fields.extend(temp)
        
        self.assignments={}
        self.timerFrame=None
            
    def getName(self):
        return self.filename
        
    def getFieldNames(self):
        return self.fields

    # assignments = dictionary with key=field name, value = (target sensor,channelnum) or targetSensor (for non-i2c values)
    def setFieldAssignments(self,assignments):
        self.assignments=assignments
        
    def startPlaying(self,frame,loop):
        if len(self.assignments)==0:
            return
        # this takes account that we may have paused before
        self.timerFrame=frame
        self.timerID=self.timerFrame.after(10,self.onTimerFired)
        
        
    def stopPlaying(self):
        self.pausePlaying()
        self.curPos=0
            
    def pausePlaying(self):
        if self.timerFrame!=None:
            if self.timerID!=None:
                self.timerFrame.after_cancel(self.timerID)
            self.timerFrame=None
            self.timerID=None
        
    def playing(self):
        return (self.timerFrame!=None)
        
    def unload(self):
        self.stopPlaying()
        
    def paused(self):
        return false
    
    # time since start of file, time as unix time
    def getTimes(self):
        return 0,0
        
    
    def onTimerFired(self):
        # use a short timeout as this connection should be cached now
        resp=url.urlopen(self.filename,timeout=1)
        line=json.load(resp)
        values={}
        for key,val in line.items():
            try:
                values[key]=float(val)
                if values[key].is_integer():
                    values[key]=int(val)
                if values[key]==0:
                    values[key+"-TIME_SINCE_PRESSED"]=1
                else:
                    values[key+"-TIME_SINCE_PRESSED"]=0
            except ValueError:
                None
        for (key,targets) in self.assignments.items():
            for target in targets:
                if type(target)!=tuple:
                    target.setValue(values[key])
                else:
                    t,channel=target
                    t.setValue(channel,values[key])
        if self.timerFrame!=None:
            self.timerID=self.timerFrame.after(self.updateRate,self.onTimerFired)

