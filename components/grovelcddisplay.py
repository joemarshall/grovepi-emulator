
import grovelcd


from gpe_utils.tkimports import *
from . import propgrid


class GroveLCDDisplay:
    
    def __init__(self,pin):
        self.pin=pin
        self.colour=(255,0,0)
        self.graph_lines=[]    
        
    def title(self):
        return "I2C-%d: Grove LCD 2 line RGB:"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove LCD 2 line (RGB)"
    
    def initSmall(self,parent):
        self.titleLabel=ttk.Label(parent,text=self.title())
        self.titleLabel.grid()
        font=tkf.Font(font="courier")
        self.line_height=font.metrics('linespace')
        self.line_width=font.measure("XXXXXXXXXXXXXXXX")
        self.canvas=tk.Canvas(parent,bg="red",width=self.line_width+4,height=self.line_height*2+4)
        self.label=self.canvas.create_text(4,4,text="                \n                ",font="Courier",justify="left",anchor=tk.NW)
        self.canvas.grid(sticky=tk.NSEW)

#        self.label=ttk.Label(parent,text="                \n                ",font="Courier")
#        self.label.grid()
    
    def cleanText(self,chrs,x0,y0):
        retVal=""
        cleaned=False
        for count,c in enumerate(chrs):
            if ord(c)<16:
                retVal+=" "
                cleaned=True
                startX=(count*self.line_width)//16+x0
                endX=((count+1)*self.line_width)//16+x0
                y=(self.line_height*ord(c))//8+y0
                line=self.canvas.create_line(startX,y,endX,y)
                self.graph_lines.append(line)
            else:
                retVal+=c
        return retVal,cleaned
    
    def update(self):
        text=grovelcd.curLCDText
        colour=grovelcd.curRGB        
        for l in self.graph_lines:
            self.canvas.delete(l)
        self.graph_lines=[]
        line1,cleaned1=self.cleanText(text[0:16],4,4)
        line2,cleaned2=self.cleanText(text[16:32],4,self.line_height+4)

        thisColour=(int(128+colour[0]*0.5),int(128+colour[1]*0.5),int(128+colour[2]*0.5))
        hexColour="#%02x%02x%02x"%(thisColour)
        self.canvas.itemconfig(self.label,text="%s\n%s"%(line1,line2))
        self.canvas.config(bg=hexColour)
        
