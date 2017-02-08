from __future__ import print_function
import bdb
import os    
import sys,threading

class _ThreadPrinter:
    def __init__(self):
        self.saveThreads={}
        self.originalStdout=sys.stdout
        sys.stdout=self
       
    def write(self, value):
        saveThread = self.saveThreads.get(threading.currentThread().ident)
        if saveThread!=None:
            saveThread.write(value.encode("ASCII"))
        self.originalStdout.write(value)

    def add(self,id,filename):
        if filename!=None:
            self.saveThreads[id]=open(filename,"wb",buffering=0)
        
    def remove(self,id):
        if id in self.saveThreads:
            del self.saveThreads[id]
            
    def flush(self):
        self.originalStdout.flush()
        for file in self.saveThreads.values():
            file.flush()
            
_prt = _ThreadPrinter()
            
class StoppableRunner(bdb.Bdb):
    def __init__(self,name,captureFile=None):
        bdb.Bdb.__init__(self)
        self._stop=False
        self.captureFile=captureFile
        self.captureID=None
        print("---------------- LAUNCHING PYTHON SCRIPT IN EMULATOR ----------------")
        
        
        self.thread=self._runFile(name)
    
    def dispatch_line(self,frame):
        bdb.Bdb.dispatch_line(self,frame)
        if self._stop:
            raise bdb.BdbQuit
        
    def _runFile(self,name):
        thd=threading.Thread(target=self._runThread,args=(name,))
        thd.daemon=True
        thd.start()
        return thd
    
    def _runThread(self,name):
        global _prt
        sys.argv=[]
        self.captureID=threading.currentThread().ident
        _prt.add(self.captureID,self.captureFile)
        self._payload(name)
        
    def _payload(self,name):
        self.run('exec(open(\'%s\').read())'%(name.replace('\\','\\\\')))
#        self.run('execfile(\'%s\')'%(name.replace('\\','\\\\')))
        
    def stop(self):
        global _prt
        self._stop=True
        _prt.remove(self.captureID)
        
    def running(self):
        return self.thread.is_alive()
        
    def capturing(self):
        return self.captureFile!=None
        
if __name__=="__main__":        
    # this line makes it so that any loaded python files will get their grovepi from the right place where the fake grovepi bits live  
    # in preference to any that happen to be in the same directory as them
    sys.path=[os.path.join(os.path.abspath(os.path.dirname(__file__)),"fakegrovepi")]+sys.path
    a=StoppableRunner("test.py")

    import time
    time.sleep(2)
    print("yay")
    a.stop()
    print("woo\nwoo")
    time.sleep(1)
    print("second try")
    a=StoppableRunner("test.py")
    time.sleep(2)
    a.stop()
    while True:
        print(a.running())
        time.sleep(1)
