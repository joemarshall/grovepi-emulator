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
