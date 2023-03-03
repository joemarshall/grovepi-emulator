from .tkimports import *
import sys
import queue


class ConsoleWindow(tk.Toplevel):
    def __init__(self,parent):
        self.old_stdout=sys.stdout
        self.old_err_write=sys.stderr.write
        tk.Toplevel.__init__(self)
        if sys.platform=="win32":
            self.attributes('-toolwindow', True)
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
        self.writes=queue.Queue()
        self.waiting_write=True
        self.timer=self.after(100,self.handle_writes)
        
    def OnClose(self,event=None):
        self.after_cancel(self.timer)
        sys.stdout=self.old_stdout
        sys.stderr.write=self.old_err_write
        return False

    def OnClear(self,event=None):
        self.text_box.delete(1.0,tk.END)

    def write(self,txt):
        self.writes.put(("stdout",txt))

    def err_write(self,txt):
        self.writes.put(("stderr",txt))

    def handle_writes(self):
        fully_scrolled_down = self.text_box.yview()[1]>0.999 
        done_insert=False
        currentTag=None
        allText=""
        while not self.writes.empty():
            (stream,txt)=self.writes.get()
            if currentTag!=stream:
                # change from stdout to stderr, need to insert
                if len(allText)>0:
                    self.text_box.insert('end',allText,(currentTag,))
                    done_insert=True
                allText=""
                currentTag=stream
                allText=txt
            else:
                allText+=txt
        if len(allText)!=0:
            self.text_box.insert('end',allText,(currentTag,))
            done_insert=True
        if fully_scrolled_down and done_insert:
            self.text_box.see("end")
        self.timer=self.after(100,self.handle_writes)
        
    def flush(self):
        self.old_stdout.flush()
        pass

