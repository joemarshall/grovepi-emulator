from __future__ import print_function
import csv
import grovepi
import time
import os

from .tkimports import *

class CSVPlayer:
    def __init__(self,name):
        self.filename=name
        self.csvfile=open(name)
        self.reader = csv.DictReader(self.csvfile)
        self.assignments={}
        self.allLines=[]
        for line in self.reader:
            for key,val in line.items():
                try:
                    line[key]=float(val)
                    if line[key].is_integer():
                        line[key]=int(val)
                except ValueError:
                    None
            self.allLines.append(line)
        self.timeColumn=None
        self.curPos=0
        self.startTime=0
        self.timerFrame=None
            
    def getName(self):
        return os.path.basename(self.filename)
        
    def getFieldNames(self):
        if self.reader!=None:
            return self.reader.fieldnames

    # assignments = dictionary with key=field name, value = (target sensor,channelnum) or targetSensor (for non-i2c values)
    def setFieldAssignments(self,timeColumn,assignments):
        self.assignments=assignments
        self.timeColumn=timeColumn
        if len(self.allLines)>0:
            self.startTime=float(self.allLines[0][timeColumn])
        
    def setReplayTime(self,theTime):
        theTime+=self.startTime
        print(theTime)
        if self.timeColumn!=None and len(self.assignments)>0:
            while theTime>self.allLines[self.curPos][self.timeColumn] and self.curPos<(len(self.allLines)-1):
                self.curPos+=1
            while self.curPos>0 and theTime<self.allLines[self.curPos-1][self.timeColumn]:
                self.curPos-=1

    def startPlaying(self,frame,loop):
        if self.timeColumn==None or len(self.assignments)==0 or len(self.allLines)==0:
            return
        self.loop=loop
        # this takes account that we may have paused before
        self.playStartRealTime=time.time() - (self.allLines[self.curPos][self.timeColumn]-self.startTime)
        self.timerFrame=frame
        self.timerID=self.timerFrame.after(0,self.onTimerFired)
        
        
    def stopPlaying(self):
        if self.timerFrame!=None:
            if self.timerID!=None:
                self.timerFrame.after_cancel(self.timerID)
            self.timerFrame=None
            self.timerID=None
        self.curPos=0
            
    def pausePlaying(self):
        if self.timerFrame!=None:
            if self.timerID!=None:
                self.timerFrame.after_cancel(self.timerID)
            self.timerFrame=None
            self.timerID=None
        
    def playing(self):
        return (self.timerFrame!=None)
        
    def paused(self):
        return (self.timerFrame==None and self.curPos!=0)

    def unload(self):
        self.stopPlaying()
    
    # time since start of file, time as unix time
    def getTimes(self):
        if self.timeColumn!=None:
            return (self.allLines[self.curPos][self.timeColumn]-self.startTime,self.allLines[self.curPos][self.timeColumn])
        else:
            return 0,0
        
    
    def onTimerFired(self):
        timeSinceStart=time.time()-self.playStartRealTime
        for (key,targets) in self.assignments.items():
            for target in targets:
                if type(target)!=tuple:
                    target.setValue(self.allLines[self.curPos][key])
                else:
                    t,channel=target
                    t.setValue(channel,self.allLines[self.curPos][key])
        if self.curPos+1 < len(self.allLines):
            nextTime=self.allLines[self.curPos+1][self.timeColumn]-self.startTime
            if self.timerFrame!=None:
                if nextTime>0:
                    self.timerID=self.timerFrame.after(int(1000*(nextTime-timeSinceStart)),self.onTimerFired)
                else:
                    self.timerID=self.timerFrame.after(10,self.onTimerFired)
            self.curPos+=1
        else:
            if self.loop:
                self.curPos=0
                self.playStartRealTime=time.time()
                if self.timerFrame!=None:
                    self.timerID=self.timerFrame.after(10,self.onTimerFired)
            else:
                self.stopPlaying()

