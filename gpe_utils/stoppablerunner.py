import bdb
import os    
import sys,threading

class StoppableRunner(bdb.Bdb):
    def __init__(self,name):
        bdb.Bdb.__init__(self)
        self._stop=False
        self.thread=self._runFile(name)
    
    def dispatch_line(self,frame):
        bdb.Bdb.dispatch_line(self,frame)
        if self._stop:
            raise bdb.BdbQuit
        
    def _runFile(self,name):
        thd=threading.Thread(target=self._runThread,args=(name,))
        thd.start()
        return thd
    
    def _runThread(self,name):
        sys.argv=[]
        self.run('execfile(\'%s\')'%(name.replace('\\','\\\\')))
        
    def stop(self):
        self._stop=True
        
    def running(self):
        return self.thread.is_alive()
        
if __name__=="__main__":        
    # this line I think makes it so that any loaded python files will get their grovepi from the right place where the fake grovepi bits live  
    # in preference to any that happen to be in the same directory as them
    sys.path=[os.path.join(os.path.abspath(os.path.dirname(__file__)),"fakegrovepi")]+sys.path
    a=StoppableRunner("test.py")

    import time
    time.sleep(2)
    print "yay"
    a.stop()
    print "woo\nwoo"
    time.sleep(1)
    print "second try"
    a=StoppableRunner("test.py")
    time.sleep(2)
    a.stop()
    while True:
        print a.running()
        time.sleep(1)
