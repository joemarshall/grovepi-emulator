from __future__ import print_function
import grovepi
import time
import os
import sys
if sys.version_info.major<3:
    import urllib2 as url
else: 
    import urllib.request as url

import json

class ServerPlayer:
    def __init__(self,name):
        self.filename=name
        resp=url.urlopen(self.filename,timeout=5)
        try:
          self.updateRate=int(resp.info()["Update-Rate"])
        except KeyError:
          self.updateRate=250
        header=resp.readline()
        self.fields=header.split(",")
        self.timestamp=0
        
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
        
    def paused(self):
        return false
        
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
        
        
    # time since start of file, time as unix time
    def getTimes(self):
        return 0,self.timestamp
        
    
    def onTimerFired(self):
        # use a short timeout as this connection should be cached now
        try:
            resp=url.urlopen(self.filename,timeout=1)
            header=resp.readline().split(",")
            srcvals=resp.readline().split(",")
            values={}
            for key,val in zip(header,srcvals):
                try:
                    values[key]=int(val)
                except ValueError:
                    values[key]=float(val)
            for (key,targets) in self.assignments.items():
                for target in targets:
                    if type(target)!=tuple:
                        target.setValue(values[key])
                    else:
                        t,channel=target
                        t.setValue(channel,values[key])
            self.timestamp=values['timestamp']
        except IOError:
            print("URL open failed")
        if self.timerFrame!=None:
            self.timerID=self.timerFrame.after(self.updateRate,self.onTimerFired)

