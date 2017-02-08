import sys
if sys.version_info.major<3:
    import Tkinter as tk
    import tkMessageBox as tkm
    import tkFileDialog as tkfd
    import tkSimpleDialog  as tksd
    import tkColorChooser as tkcc
    import ttk
else:
    import tkinter as tk
    import tkinter.messagebox as tkm
    import tkinter.filedialog as tkfd
    import tkinter.simpledialog  as tksd
    import tkinter.colorchooser  as tkcc
    import tkinter.ttk as ttk
