from .tkimports import *

class CSVMappingDlg(tksd.Dialog):
    
    def __init__(self, parent,csvColumns,components,lastMapping,needsTime):
        self.needsTime=needsTime
        self.csvColumns=csvColumns
        self.components=components
        self.lastMapping=lastMapping
        self.mapping=None
        tksd.Dialog.__init__(self,parent=parent)
#        super(CSVMappingDlg, self).__init__(parent=parent) 

    def body(self,master):
        self.combos=[]
        self.mapping={}
        self.timeColumn=None
        
        if self.needsTime:
            st=tk.Label(master,text="Time column (required)",bg="black",fg="white")
            st.grid(sticky=tk.E+tk.W)
            #  need a time column
            self.timeComboVar=tk.StringVar()
            self.timeCombo=ttk.Combobox(master,state="readonly",textvariable=self.timeComboVar,values=self.csvColumns)
            self.timeCombo.grid(sticky=tk.E+tk.W)
            # for val in self.csvColumns:
                # if val=="time":
                    # self.timeComboVar.set(val)
                    # break
            if self.timeComboVar.get()=="":
                for val in self.csvColumns:
                    if val.find("time")!=-1:
                        self.timeComboVar.set(val)
                        break
        
        sensorCombo={}
        for comp in self.components:
            if hasattr(comp,"setValue"):
                st=tk.Label(master,text=comp.title(),bg="black",fg="white")
                st.grid(sticky=tk.E+tk.W)

                if hasattr(comp,"getNumAxes"):
                    for c in range(0,comp.getNumAxes()):
                        st=tk.Label(master,text=comp.getAxisName(c),bg="#7f7f7f",fg="#000000")
                        st.grid(sticky=tk.E+tk.W,padx=10)
                        comboVar=tk.StringVar()
                        compCombo=ttk.Combobox(master,state="readonly",textvariable=comboVar,values=self.csvColumns)
                        compCombo.grid(sticky=tk.E+tk.W,padx=10)

                        self.combos.append((comboVar,(comp.title(),c)))
                        sensorCombo[(comp.title(),c)]=comboVar
                else:
                    comboVar=tk.StringVar()
                    compCombo=ttk.Combobox(master,state="readonly",textvariable=comboVar,values=self.csvColumns)
                    compCombo.grid(sticky=tk.E+tk.W)
                    self.combos.append((comboVar,comp.title()))
                    sensorCombo[comp.title()]=comboVar
                    
        if self.lastMapping!=None:
            for (col,components) in self.lastMapping.items():
                if col in self.csvColumns:
                    for component in components:
                        if type(component)==list:
                            component=tuple(component)
                        if component=="TIME" and self.needsTime:
                            self.timeComboVar.set(col)
                        elif component in sensorCombo:
                            sensorCombo[component].set(col)
        if self.needsTime:
            return self.timeCombo
        else:
            return
        
    def validate(self):
        if self.needsTime and self.timeComboVar.get()=="":
            tkm.showwarning("Time column needed","You need to select a column with the time in it")
            return 0
        anySelected=False
        for box,comp in self.combos:
            if len(box.get())>0:
                anySelected=True
        if not anySelected:
            tkm.showwarning("Select a mapping","You need to select at least one mapping from CSV column to sensor")
            return 0
            
        if self.needsTime:
            self.mapping={self.timeComboVar.get():["TIME"]}
        for combo,data in self.combos:
            value=combo.get()
            if len(value)>0:
                if value in self.mapping:
                    self.mapping[value].append(data)
                else:
                    self.mapping[value]=[data]
        return 1
       
    def getAssignments(self):
        return self.mapping