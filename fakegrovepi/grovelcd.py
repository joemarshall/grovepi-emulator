import math


curLCDText=[" "]*32  
curRGB=(0,0,0)

def setText(text,clear=False):
    global curLCDText
    curLCDText=[" "]*32  
    col=0
    row=0
    c=0
    while c<len(text) and row<2:
        if text[c]=='\n':
            row+=1
            col=0
        else:
            curLCDText[row*16+col]=text[c]
            col+=1
            if col>=16:
                col=0
                row+=1
        c+=1

def setRGB(r,g,b):
    global curRGB
    curRGB=(r,g,b)

_prevData=[[ord(' ')]*16,[ord(' ')]*16]        

# map 0-8 to unicode     characters 2581-2588 and space
def toChr(value):
    print(value)
    if value==0 or value==32:
        return ' '
    else:
        return chr(0x2581)


def addGraphData(data,x,y,columns,rows):
    data=list(data)
    global _prevData
    numChars=16//columns
    startChar=0
    if columns>1 and x==1:
        startChar=8
    if rows==2:
        rowIDX=1 if y==1 else 0
        thisRow=_prevData[rowIDX][:]
        for c in range(0,numChars):
            dataStart=(c*len(data))//numChars
            dataEnd=((c+1)*len(data))//numChars
            if dataEnd<=dataStart:
                dataEnd=dataStart+1
            outVal=max(data[dataStart:dataEnd])
            outVal=max(outVal,0)
            outVal=min(outVal,1)
            outVal=7-math.floor(outVal*7.5)
            thisRow[c+startChar]=outVal
    else:
        row1,row2=_prevData[0][:],_prevData[1][:]
        for c in range(0,numChars):
            dataStart=(c*len(data))//numChars
            dataEnd=((c+1)*len(data))//numChars
            if dataEnd<=dataStart:
                dataEnd=dataStart+1
            outVal=max(data[dataStart:dataEnd])
            outVal=max(outVal,0)
            outVal=min(outVal,1)
            outVal=15-math.floor(outVal*15.5)
            if outVal>=8:
                row2[c+startChar]=outVal-8
                row1[c+startChar]=ord(' ')
            else:
                row1[c+startChar]=outVal
                row2[c+startChar]=ord(' ')
        _prevData=[row1,row2]
    for c in range(32):
        curLCDText[c]=chr(_prevData[c//16][c%16])
    
