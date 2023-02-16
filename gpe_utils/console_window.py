from .tkimports import *
import sys
import os

class ConsoleWindow(tk.Toplevel):
    def __init__(self,parent):
        self.old_stdout=sys.stdout
        self.old_err_write=sys.stderr.write
        tk.Toplevel.__init__(self)
        if sys.platform=="win32":
            self.attributes('-toolwindow', True)
#        self.iconbitmap(os.path.join(_mainPath,"main.ico"))
        self.title("GrovePI Python Output")
        sb = ttk.Scrollbar(self)
        sb.grid(row=0,column=1,sticky=tk.NSEW)
        clear_button=ttk.Button(self,text='clear',command=self.OnClear)
        clear_button.grid(row=1,column=0)
        self.text_box=tk.Text(self,width=80,wrap='char',font=("courier",10))
        self.text_box.tag_config("stderr", background="white", foreground="red")
        self.text_box.grid(row=0,column=0)
        self.text_box.config(yscrollcommand=sb.set)
        sb.config(command=self.text_box.yview)        
        sys.stdout=self
        sys.stderr.write=self.err_write
        self.protocol("WM_DELETE_WINDOW", self.OnClose)
        
    def OnClose(self,event=None):
        sys.stdout=self.old_stdout
        sys.stderr.write=self.old_err_write
        return False

    def OnClear(self,event=None):
        self.text_box.delete(1.0,tk.END)

    def write(self,txt):
        fully_scrolled_down = self.text_box.yview()[1] == 1.0
        self.text_box.insert('end',txt)
        if fully_scrolled_down:
            self.text_box.see("end")

    def err_write(self,txt):
        fully_scrolled_down = self.text_box.yview()[1] == 1.0
        self.text_box.insert('end',txt,("stderr",))
        if fully_scrolled_down:
            self.text_box.see("end")
        
    def flush(self):
        pass

