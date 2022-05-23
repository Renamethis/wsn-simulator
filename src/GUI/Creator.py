import tkinter as tk
from src.GUI.Plotter import Plotter

class Creator(tk.Toplevel):
    
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.protocol("WM_DELETE_WINDOW", self.__close)
        self.title("Create Network")
        self.__plotter = Plotter(self)
        self.__plotter.get_tk_widget().pack(side=tk.TOP, anchor=tk.N, 
                                  fill=tk.BOTH, padx=10)
    def __del__(self):
        self.__close()    
        
    def __close(self):
        self.destroy()