from operator import ne
from random import random
import tkinter  as tk
from threading import Thread
from PIL import Image
from src.SideMenu import SideMenu
from src.Plotter import Plotter
class Simulator(tk.Tk):

    def __init__(self, network, iters):
        tk.Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.__close)
        self.title("WSN")
    
        self.__side_menu = SideMenu(self)
        self.__side_menu.pack(fill=tk.X, side=tk.LEFT, anchor=tk.N)
        
        self.__plotter = Plotter(network, iters, self)
        self.__plotter.get_tk_widget().pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH, padx=20)
        
        self.__simulate_button = tk.Button(text="Simulate", width=15, height=3)
        self.__simulate_button.config(command=self.simulate)
        self.__simulate_button.pack(side=tk.BOTTOM)
        
        self.__check_flag = tk.BooleanVar()
        self.__check_flag.set(1)
        self.__check_button = tk.Checkbutton(text="PSO",
                 variable=self.__check_flag,
                 onvalue=1, offvalue=0)
        self.__check_button.pack(side=tk.BOTTOM)

    def __del__(self):
        self.__close()

    def simulate(self):
        self.__plotter.simulate(self.__check_flag.get(), self.__simulate_button)

    def __close(self):
        if(self.__plotter.isRunning()):
            self.__plotter.stop()
        else:
            self.quit()