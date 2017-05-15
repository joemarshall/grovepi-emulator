from __future__ import absolute_import
import grovelcd


from gpe_utils.tkimports import *
from . import propgrid


class GroveLCDDisplay:
    
    def __init__(self,pin):
        self.pin=pin
        self.colour=(255,0,0)
    
    def title(self):
        return "I2C-%d: Grove LCD 2 line RGB:"%self.pin
        
    @classmethod
    def classDescription(cls):
        return "Grove LCD 2 line (RGB)"
    
    def initSmall(self,parent):
        self.titleLabel=tk.Label(parent,text=self.title())
        self.titleLabel.grid()

        self.label=tk.Label(parent,text="                \n                ",font="Courier")
        self.label.grid()
    
    def update(self):
        text=grovelcd.curLCDText
        colour=grovelcd.curRGB
        line1="".join(text[0:16])
        line2="".join(text[16:32])
        thisColour=(int(128+colour[0]*0.5),int(128+colour[1]*0.5),int(128+colour[2]*0.5))
        self.label.config(bg="#%02x%02x%02x"%thisColour)
        self.label.config(text="%s\n%s"%(line1,line2))
