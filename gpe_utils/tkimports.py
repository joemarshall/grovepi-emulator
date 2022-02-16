import sys
if sys.version_info.major<3:
    import tkinter as tk
    import tkinter.messagebox as tkm
    import tkinter.filedialog as tkfd
    import tkinter.simpledialog  as tksd
    import tkinter.colorchooser as tkcc
    import tkinter.ttk
    import tkinter.font as tkf 
else:
    import tkinter as tk
    import tkinter.messagebox as tkm
    import tkinter.filedialog as tkfd
    import tkinter.simpledialog  as tksd
    import tkinter.colorchooser  as tkcc
    import tkinter.ttk as ttk
    import tkinter.font as tkf 
