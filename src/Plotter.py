import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.Device import State
import sys
from random import random
import tkinter  as tk
import threading
from matplotlib.figure import Figure
class Plot:

    __colors = []

    def __init__(self, clusters):
        self.__clusters = clusters
        self.__number = 0
        self.__root = tk.Tk()
        self.__root.title("WSN")
        self.__figure = Figure()
        self.__axis = self.__figure.add_subplot(1,1,1)
        self.__canvas = FigureCanvasTkAgg(self.__axis.figure, master=self.__root)
        self.__canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.__mainloop = threading.Thread(target=self.__run_gui)

    def __del__(self):
        self.__root.quit()
        self.__root.destroy()

    # Matplotlib draw devices and clusters
    def draw_devices(self):
        self.__axis.cla()
        for cluster in self.__clusters:
            for dev in cluster.get_devices():
                devpos = dev.get_pos()
                if(dev is cluster.get_head() and dev.alive()):
                    self.__axis.plot(devpos[0], devpos[1], marker='o', 
                             linestyle='None', markersize=7, color=(1, 0, 0))
                    self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "CH", 
                                     fontsize=7)
                elif(not dev.alive()):
                    self.__axis.plot(devpos[0], devpos[1], marker='o', 
                             linestyle='None', markersize=7, color=(0, 0, 0))
                    self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Dead", 
                             fontsize=7)
                elif(dev.get_state() == State.ACTIVE):
                    self.__axis.plot(devpos[0], devpos[1], marker='o', 
                                     linestyle='None', markersize=7, 
                                     color=cluster.get_color())
                    self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Device", 
                                     fontsize=7)
                else:
                    self.__axis.plot(devpos[0], devpos[1], marker='o', 
                                     linestyle='None', markersize=7, 
                                     color=(0.5, 0.5, 0.5))
                    self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Sleep", 
                                     fontsize=7)
        self.__canvas.draw()
        self.__root.update()
        
    def draw_traces(self, traces):
        self.__number += 1
        traceAxis = self.__figure.add_subplot(1,self.__number,1)
        traceAxis.plot(traces, color=(random(), random(), random()))
        traceAxis.figure.show()
        self.__canvas.draw()
        self.__root.update()
        
    def __run_gui(self):
        self.__root.mainloop()

    def draw_energy(self, energy):
        self.__axis.text(0, 0, str(energy), fontsize=15)
        self.__canvas.draw()
        self.__root.update()