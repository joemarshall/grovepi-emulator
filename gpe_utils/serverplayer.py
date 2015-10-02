import grovepi
import time
import wx
import os
import urllib2
import json

class ServerPlayer:
    def __init__(self,name):
        self.filename=name

        resp=urllib2.urlopen(self.filename,timeout=5)
        header=resp.readline()
        self.fields=header.split(",")
        self.timestamp=0
        
        self.assignments={}
        self.timer=None
            
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
        self.timer=wx.Timer(frame)
        frame.Bind(wx.EVT_TIMER, self.onTimerFired, self.timer)
        self.timer.Start(0,True)
        
    def stopPlaying(self):
        if self.timer!=None:
            self.timer.Stop()
            self.timer=None
        self.curPos=0
            
    def pausePlaying(self):
        if self.timer!=None:
            self.timer.Stop()
            self.timer=None
        
    def unload(self):
        self.stopPlaying()
        
    def playing(self):
        return (self.timer!=None)

        
    # time since start of file, time as unix time
    def getTimes(self):
        return 0,self.timestamp
        
    
    def onTimerFired(self,event):
        # use a short timeout as this connection should be cached now
        resp=urllib2.urlopen(self.filename,timeout=1)
        header=resp.readline().split(",")
        srcvals=resp.readline().split(",")
        values={}
        for key,val in zip(header,srcvals):
            try:
                values[key]=int(val)
            except ValueError:
                values[key]=float(val)
        for (key,target) in self.assignments.iteritems():
            if type(target)!=tuple:
                target.setValue(values[key])
            else:
                t,channel=target
                t.setValue(channel,values[key])
        self.timer.Start(250,True)
        self.timestamp=values['timestamp']

