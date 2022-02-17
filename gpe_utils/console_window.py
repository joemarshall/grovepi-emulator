from .tkimports import *
import sys
import os

class ConsoleWindow(tk.Toplevel):
    def __init__(self,parent):
        self.old_stdout=sys.stdout
        tk.Toplevel.__init__(self)
        #self.frame=ttk.Frame(self)
        if sys.platform=="win32":
            self.attributes('-toolwindow', True)
#        self.iconbitmap(os.path.join(_mainPath,"main.ico"))
        self.title("GrovePI Python Output")
        sb = tk.Scrollbar(self)
        sb.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.text_box=tk.Text(self,width=80,wrap='char')
        self.text_box.pack(side=tk.LEFT,expand=True)
        self.text_box.config(yscrollcommand=sb.set)
        sb.config(command=self.text_box.yview)        
        sys.stdout=self
        self.protocol("WM_DELETE_WINDOW", self.OnClose)
        
    def OnClose(self,event=None):
        return False

        
    def write(self,txt):
        self.text_box.insert('end',txt)
        
    def flush(self):
        pass

