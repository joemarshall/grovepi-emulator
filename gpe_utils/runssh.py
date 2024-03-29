


import asyncio

import subprocess
import tempfile
import os, stat
import re
import time

import threading

import sys

from .stoppablerunner import StoppableRunner


class StopRunner(Exception):
    pass


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
        

class RemoteRunner:
        

    def __init__(self,name,address,captureFile=None):
        self.address=address

        self.process=None

        self.loop=None

        self.task=None

        self.wait_tasks={}

        self.captureFile=captureFile

        self.thread=self._runFile(name)


    def _runFile(self,name):

        thd=threading.Thread(target=self._runThread,args=(name,))

        thd.daemon=True
        thd.start()
        return thd


    def banner_print(self,txt):

        banner_total=80

        banner_sides=banner_total-len(txt)-2

        dash_left=banner_sides//2

        dash_right=banner_total-dash_left - len(txt)-2

        print(f"{'-'*dash_left} {txt} {'-'*dash_right}")


    async def _consume_stream_and_apply(self,strm,fn,argv,is_stderr=False):
        async for line in strm:
            if is_stderr and os.name=="nt":
                # bypass host authorisation on putty
                if line.find(b"Store key in cache?")!=-1 or line.find(b"If you trust this host")!=-1 or line.find(b"The host key does not match")!=-1:
                    self.process.stdin.write(b"y\n")

            fn(line.decode('utf-8'),**argv)


    async def _echo_subprocess_output(self,cmdRun,fn=print,argv={"end":''},override_stop=False):

#        print("launch cmd:",cmdRun)

        self.process=await asyncio.create_subprocess_exec(*cmdRun,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)

        coroutines=[self._consume_stream_and_apply(self.process.stderr,fn,argv,is_stderr=True),self._consume_stream_and_apply(self.process.stdout,fn,argv),self.process.wait()]
        if not override_stop:
            coroutines.append(self._stop_future)

        terminating=False

        for coro in asyncio.as_completed(coroutines):

            finished_result=await coro

            if self.process.returncode!=None:

                break

            if finished_result=="STOP":
                self.process.terminate()

                terminating=True

        if terminating:

            raise StopRunner

        retval=self.process.returncode

        self.process=None

        return retval
    
            

    def _stop_in_thread(self):        

        self._stop_future.set_result("STOP")
    

    def stop(self):

        if self.loop:
            self.loop.call_soon_threadsafe(self._stop_in_thread)            


    def _runThread(self,name):

        try:

            asyncio.run(self._executeRemote(name))

            self.banner_print("FINISHED")

        except StopRunner:

            self.banner_print("STOPPED")
        

    async def _executeRemote(self,codeName):

        self.loop=asyncio.get_event_loop()
        self._stop_future=self.loop.create_future()

        self.banner_print("REMOTE LAUNCH OF PYTHON ON RASPBERRY PI")

        if self.captureFile!=None:

            print ("Running %s at %s - capture to %s"%(codeName,self.address,self.captureFile))

        else:

            print ("Running %s at %s"%(codeName,self.address))

        print("Copying python script to remote address")
        

        cmdCopyBack=None

        if os.name=="nt":

            # on windows we use plink and pscp to copy and run

            cmdCopy=[_PUTTY_DIR+ os.sep+"pscp.exe","-i",_PUTTY_KEY,codeName,"%s:%s"%(self.address,os.path.basename(codeName))]
                

            if self.captureFile:

                cmdRun=[_PUTTY_DIR+ os.sep+'plink.exe','-batch','-i',_PUTTY_KEY,self.address,"-t","stdbuf -o 0 python -u %s |tee %s"%(os.path.basename(codeName),os.path.basename(self.captureFile))]

                cmdCopyBack=[_PUTTY_DIR+ os.sep+"pscp.exe","-i",_PUTTY_KEY,"%s:%s"%(self.address,os.path.basename(self.captureFile)),self.captureFile]

            else:

                cmdRun=[_PUTTY_DIR+ os.sep+'plink.exe','-batch','-i',f"{_PUTTY_KEY}",self.address,"-t","python %s"%(os.path.basename(codeName))]
                

        else:

            cmdCopy=["scp","-i",_SSH_KEY,"-o","UserKnownHostsFile=/dev/null","-o","StrictHostKeyChecking=no",codeName,self.address+":"+os.path.basename(codeName)]

            if self.captureFile:

                cmdRun=["ssh","-i",_SSH_KEY,self.address,"-o","UserKnownHostsFile=/dev/null","-o","StrictHostKeyChecking=no","stdbuf -o 0 python -u %s | tee %s"%(os.path.basename(codeName),os.path.basename(self.captureFile))]

                cmdCopyBack=["scp","-i",_SSH_KEY,"-o","UserKnownHostsFile=/dev/null","-o","StrictHostKeyChecking=no",self.address+":"+os.path.basename(self.captureFile),self.captureFile]

            else:

                cmdRun=["ssh","-i",_SSH_KEY,self.address,"-o","UserKnownHostsFile=/dev/null","-o","StrictHostKeyChecking=no","stdbuf -o 0 python -u %s "%os.path.basename(codeName)]
                

            # fix key permission for openssh or else it will fail to run

            os.chmod(_SSH_KEY, stat.S_IREAD)

			

        retVal=await self._echo_subprocess_output(cmdCopy)
           

        if retVal==0:

            self.banner_print("LAUNCHING")

            if self.captureFile!=None:

                try:

                    retVal=await self._echo_subprocess_output(cmdRun,fn=sys.stdout.write,argv={})

                    if retVal!=0:

                        print("Failed to run python")

                finally:

                    self.banner_print("COPYING OUTPUT")

                    retVal=await self._echo_subprocess_output(cmdCopyBack,override_stop=True)

                    if retVal!=0:

                        print("Failed to copy output back to PC")

            else:

                retVal=await self._echo_subprocess_output(cmdRun)

                if retVal!=0:

                    print("Failed to run python")

        else:

            print("Failed to copy python script")


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


