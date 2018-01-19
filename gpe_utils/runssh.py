from __future__ import print_function
from __future__ import absolute_import
import subprocess
import tempfile
import os, stat
import time
import threading
import sys
from .stoppablerunner import StoppableRunner

if getattr( sys, 'frozen', False ) :
        # running in an installer bundle
    _mainPath=sys._MEIPASS
        
else :
    _mainPath=os.path.dirname(__file__)


_SSH_KEY=os.path.join(_mainPath,"pikeys","openssh.key")
_PUTTY_KEY=os.path.join(_mainPath,"pikeys","putty.ppk")
_PUTTY_DIR=os.path.join(_mainPath,"pikeys")


class _ReadableTempFile:
    def __init__(self,contents):
        file,self.name=tempfile.mkstemp()
        os.write(file,contents)
        os.close(file)
        self.file=open(self.name,"rU",buffering=0)
        self.file.seek(0,2)
        
    def __del__(self):
        if self.file:
            self.file.close()
        if self.name!=None:
            os.remove(self.name)
        self.file=None
        self.name=None    

_HOST_KEY_CACHE={}
        
class RemoteRunner:
        
    def __init__(self,name,address,captureFile=None):
        self.address=address
        self.process=None
        self.captureFile=captureFile
        self.thread=self._runFile(name)

    def _runFile(self,name):
        thd=threading.Thread(target=self._runThread,args=(name,))
        thd.daemon=True
        thd.start()
        return thd

        
    def stop(self):
        while self.running():
            if self.process!=None:
                self.process.terminate()
                break
        if self.thread!=None:
            self.thread.join()
        
    def _bypassPuttyHostAuth(self,cmdCopy):
        print("Loading host key")
#        popen = subprocess.Popen(cmdCopy, universal_newlines=True,stdin=open(os.devnull),stdout=None,stderr=subprocess.PIPE,bufsize=1)
        popen = subprocess.Popen(cmdCopy, universal_newlines=True,stdin=open(os.devnull),stdout=open(os.devnull),stderr=subprocess.PIPE,bufsize=1)
        HOST_ERROR_STR="ssh-rsa "
        for line in popen.stderr:
            print (line)
            errPos=line.find(HOST_ERROR_STR)
            if errPos>=0:
                popen.stderr.close()
                popen.terminate()
                splitLine=line.split(" ")
                return splitLine[-1].strip("\n")
        sleeps=10
        while (not popen.poll()) and sleeps>0 and popen.returncode==None:
            time.sleep(0.5)
            sleeps-=1
        #print (popen.returncode)
        if sleeps==0 or popen.returncode!=0:
            print ("failed to load host key - do you have the correct IP address")
            try:
                popen.terminate()
            except OSError:
                None            
            return "FAIL"
        return None

    def _runThread(self,name):
        self._executeRemote(name)
        
    def _executeRemote(self,codeName):
        #        codeFile=_ReadableTempFile(pythonCode)
        #        codeName=codeFile.name
        print("---------------- REMOTE LAUNCH OF PYTHON ON RASPBERRY Pi ----------------")
        if self.captureFile!=None:
            print ("Running %s at %s - capture to %s"%(codeName,self.address,self.captureFile))
        else:
            print ("Running %s at %s"%(codeName,self.address))
        print("Copying python script to remote address")
        
        cmdCopyBack=None
        if os.name=="nt":
            # on windows we use plink and pscp to copy and run
            cmdCopy=_PUTTY_DIR+ os.sep+"pscp -i \"%s\" \"%s\" \"%s:%s\""%(_PUTTY_KEY,codeName,self.address,os.path.basename(codeName))
            print (cmdCopy)
            if self.address in _HOST_KEY_CACHE:
                host_key=_HOST_KEY_CACHE[self.address]
            else:
                host_key=self._bypassPuttyHostAuth(cmdCopy)
                if host_key=="FAIL":
                    return
                _HOST_KEY_CACHE[self.address]=host_key
            host_key_str=""
            if host_key!=None:
                host_key_str="-hostkey %s"%host_key
            cmdCopy=_PUTTY_DIR+ os.sep+"pscp -i \"%s\" %s \"%s\" \"%s:%s\""%(_PUTTY_KEY,host_key_str,codeName,self.address,os.path.basename(codeName))
            if self.captureFile:
                cmdRun=_PUTTY_DIR+ os.sep+'plink -i \"%s\" %s %s -t "stdbuf -o 0 python %s |tee %s"'%(_PUTTY_KEY,host_key_str   ,self.address,os.path.basename(codeName),os.path.basename(self.captureFile))
                cmdCopyBack=_PUTTY_DIR+ os.sep+"pscp -i \"%s\" %s %s:%s \"%s\""%(_PUTTY_KEY,host_key_str,self.address,os.path.basename(self.captureFile),self.captureFile)
            else:
                cmdRun=_PUTTY_DIR+ os.sep+'plink -i \"%s\" %s %s -t "python %s"'%(_PUTTY_KEY,host_key_str   ,self.address,os.path.basename(codeName))
                
        else:
            cmdCopy=["scp","-i",_SSH_KEY,"-o","UserKnownHostsFile=/dev/null","-o","StrictHostKeyChecking=no",codeName,self.address+":"+os.path.basename(codeName)]
            if self.captureFile:
                cmdRun=["ssh","-i",_SSH_KEY,self.address,"-o","UserKnownHostsFile=/dev/null","-o","StrictHostKeyChecking=no","stdbuf -o 0 python %s | tee %s"%(os.path.basename(codeName),os.path.basename(self.captureFile))]
                cmdCopyBack=["scp","-i",_SSH_KEY,"-o","UserKnownHostsFile=/dev/null","-o","StrictHostKeyChecking=no",self.address+":"+os.path.basename(self.captureFile),self.captureFile]
            else:
                cmdRun=["ssh","-i",_SSH_KEY,self.address,"-o","UserKnownHostsFile=/dev/null","-o","StrictHostKeyChecking=no","stdbuf -o 0 python %s "%os.path.basename(codeName)]
                
            # fix key permission for openssh or else it will fail to run
            os.chmod(_SSH_KEY, stat.S_IREAD)
			
        retVal=subprocess.call(cmdCopy)
           
        if retVal==0:
            print("-------------------------------- LAUNCHING -------------------------------")
            if self.captureFile!=None:
                self.process = subprocess.Popen(cmdRun,bufsize=1)
#                self.process = subprocess.Popen(cmdRun, universal_newlines=True,stdin=open(os.devnull),stdout=None,bufsize=1)
                self.return_code = self.process.wait()
                retVal=subprocess.call(cmdCopyBack)
                
#                logFile=open(self.captureFile,"wb",buffering=0)
#                self.process = subprocess.Popen(cmdRun, universal_newlines=True,stdin=open(os.devnull),stdout=subprocess.PIPE,bufsize=1)
#                for line in iter(self.process.stdout.readline,''):
#                    print(line, end=' ')                    
#                    logFile.write(line.encode("ASCII"))
#                    logFile.flush()
#         
#                logFile.close()
#                self.return_code = self.process.wait()
            else:
                self.process = subprocess.Popen(cmdRun,bufsize=0)
#                self.process = subprocess.Popen(cmdRun, universal_newlines=True,stdin=open(os.devnull),stdout=None,bufsize=1)
                self.return_code = self.process.wait()

    def running(self):
        return self.thread.is_alive()
        
    def capturing(self):
        return self.captureFile!=None


if __name__=="__main__":     
            
    pythonCode='''
import time
import sys
print 'woo'
c=0
for c in range(0,50000):
    print '%f,%d,%d'%(time.time(),0,c)
    sys.stdout.flush()
    c+=1
    c%=255
    time.sleep(.1)
    
    ''' 
    r=RemoteRunner("d:\\temp\\test.py",sys.argv[1])
#    r=RemoteRunner("d:\\temp\\test.py",sys.argv[1],captureFile="output.txt")
    try:
        while r.running():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("interrupted")
        r.stop()

