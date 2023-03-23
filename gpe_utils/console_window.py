if __name__=="__main__":
    from tkimports import *
else:
    from .tkimports import *
import sys

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
        self.writes=[]
        self.timer=self.after(100,self.handle_writes)
        
    def OnClose(self,event=None):
        self.after_cancel(self.timer)
        sys.stdout=self.old_stdout
        sys.stderr.write=self.old_err_write
        return False

    def OnClear(self,event=None):
        self.text_box.delete(1.0,tk.END)

    def write(self,txt):
        if len(txt)>0:
            self.writes.append((None,txt))

    def err_write(self,txt):
        if len(txt)>0:
            self.writes.append(("stderr",txt))

    def handle_writes(self):
        fully_scrolled_down = self.text_box.yview()[1]>0.999 
        done_insert=False
        currentTag=None
        allText=""
        new_writes,self.writes=self.writes,[] # because of global interpreter lock this should be thread safe
        for (tag,txt) in new_writes:
            if currentTag!=tag:
                # change from stdout to stderr, need to insert
                if len(allText)>0:
                    self.text_box.insert('end',allText,(currentTag,))
                    done_insert=True
                allText=""
                currentTag=tag
                allText=txt
            else:
                allText+=txt
        if len(allText)!=0:
            self.text_box.insert('end',allText,(currentTag,))
            done_insert=True
        if fully_scrolled_down and done_insert:
            self.text_box.see("end")
        self.timer=self.after(50,self.handle_writes)
        
    def flush(self):
        self.old_stdout.flush()

if __name__=="__main__":
    # test performance of console window
    root =tk.Tk()                             #main window
    root.tk_setPalette(background='#fff')
    import time,threading



    class TestFrame(ttk.Frame):

        def __init__(self,parent,timestep=0.001):
            super().__init__(parent)
            self.timestep=timestep
            self.console=ConsoleWindow(self)
            self.start_time=time.time()
            self.count=0
            threading.Thread(target=self.test_fn,daemon=True).start()

        def test_fn(self):
            import timeit
            print(timeit.timeit("print('WOO')",number=1000000))
            self.after(1000,sys.exit,0)


    import cProfile
    top = TestFrame(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        top.OnClose()


