#!/usr/bin/python3
# -*- coding: ascii -*-
"""
    Writes and reads to the eeprom of the Grove NFC Tag module
    http://www.seeedstudio.com/wiki/Grove_-_NFC_Tag

    example usage:
        print (grovenfctag.readNFCData(0,16)) # display the first 16 bytes of the NFC tag
        
        time.sleep(0.1)# good idea to pause between read and writes
        grovenfctag.writeNFCData(0,[11,12,13,14,15,16,17,18,19])# write data to position 0
        
        print (grovenfctag.readNFCData(0,16)) # display the first 16 bytes of the NFC tag

"""
from __future__ import print_function

import time,sys

NFCBuffer=[0]*8192
        
def readNFCData(addr,length):
    """ Read some data from eeprom of the Grove NFC Tag module 
    
        Args:
            addr:
                Address to read data from
            
            length:
                Number of bytes to read
                
        Returns:
            Array of bytes
    """
    global NFCBuffer
    if addr<0 or addr+length>len(NFCBuffer):
        print("Trying to read NFC tag outside data area")
        raise IOError
    return NFCBuffer[addr:(addr+length)]

def writeNFCData(addr,data):
    """ Write some data to the eeprom of the Grove NFC Tag module
    
        Args:
            addr:
                address to write data to
                
            data:
                Array of bytes to write
    """
    if addr<0 or addr+len(data)>len(NFCBuffer):
        print("Trying to write NFC tag outside data area")
        raise IOError
    for byte in data:
        NFCBuffer[addr]=byte
        addr+=1
        time.sleep(0.01)

      
class NFCTagBuffer:
    def __init__(self):
        self.writePosition=1
        self.bytes=[]
    
    # write data to the tag at current position and increment write position if needed
    def writeData(self, bytes):
        print("write:"+str(bytes))
        self.bytes.extend(bytes)
        self.flush(False)
        
    # if we have more than 4 bytes, actually write blocks out
    # if partialBuffer is true, then we write a partial buffer if we
    # have >1 and <4 bytes
    # buffer space 1 takes the current position
    def flush(self, partialBuffer=True):
        self.posAtStart=self.writePosition
        while len(self.bytes)>3:
            writeNFCData(self.writePosition*4,self.bytes[0:4])
            self.bytes=self.bytes[4:]
            self.writePosition+=1
            if self.writePosition>=2048:
                self.writePosition=1
        if partialBuffer and len(self.bytes)>0:
            self.bytes.extend([0]*(4-len(self.bytes)))
            writeNFCData(self.writePosition*4,self.bytes)
            self.bytes=[]
            self.writePosition+=1
            if self.writePosition>=2048:
                self.writePosition=1
        if self.posAtStart<self.writePosition:
            writeNFCData(0,[self.writePosition>>8,self.writePosition&0xff,0,0])

if __name__=="__main__":
    print (readNFCData(0,16))
    time.sleep(0.1)
    writeNFCData(0,[11,12,13,14,15,16,17,18,19])
    time.sleep(0.1)
    print( readNFCData(0,16))

writeNFCData(0,[11,12,13,14,15,16,17,18,19])
