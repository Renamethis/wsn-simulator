import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.Device import State
from src.WSN import WSN
import sys
from random import random
import tkinter  as tk
from threading import Thread
from matplotlib.figure import Figure
from matplotlib import gridspec as gridspec

class Simulator(tk.Tk):

    __colors = []

    def __init__(self, clusters, iters):
        tk.Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.__close)
        self.__clusters = clusters
        self.__network = WSN(clusters, iters)
        self.__exit = False
        self.title("WSN")
        self.__figure = Figure()
        self.__axis = self.__figure.add_subplot(111)
        self.__gs = gridspec.GridSpec(1, 4)
        self.__energy_axis = self.__figure.add_subplot(121)
        self.__nodes_axis = self.__figure.add_subplot(131)
        self.__energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self.__canvas = FigureCanvasTkAgg(self.__axis.figure, master=self)
        self.__canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=2)
        self.__simulate_button = tk.Button(text="Simulate", width=15, height=3)
        self.__simulate_button.config(command=self.__simulate)
        self.__simulate_button.pack()

    def __del__(self):
        self.__network.stop()
        self.__exit = True

    def __close(self):
        self.__network.stop()
        self.__exit = True

    def __simulate(self):
        self.__energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self.__axis.set_position(self.__gs[0:4].get_position(self.__figure))
        self.__axis.set_subplotspec(self.__gs[0:4])
        self.__network.simulate(True)
        draw_thread = Thread(target=self.__draw_loop)
        draw_thread.start()

    def __draw_loop(self):
        self.__simulate_button["state"] = "disabled"
        while self.__network.isRunning():
            self.__draw_devices()
        if(self.__exit):
            self.quit()
            return
        self.__draw_devices()
        energy_trace, nodes_trace = self.__network.getTraces()
        self.__energy_axis.set_visible(True)
        self.__energy_axis.set_title("Energy consupmtion")
        self.__nodes_axis.set_visible(True)
        self.__nodes_axis.set_title("Number of alive nodes")
        self.__energy_axis.plot(energy_trace, color=(random(), random(), random()))
        self.__nodes_axis.plot(nodes_trace, color=(random(), random(), random()))
        # Replace subplots in canvas
        self.__axis.set_position(self.__gs[0:2].get_position(self.__figure))
        self.__axis.set_subplotspec(self.__gs[0:2])
        self.__energy_axis.set_position(self.__gs[2:3].get_position(self.__figure))
        self.__energy_axis.set_subplotspec(self.__gs[2:3])
        self.__nodes_axis.set_position(self.__gs[3:4].get_position(self.__figure))
        self.__nodes_axis.set_subplotspec(self.__gs[3:4])
        self.__simulate_button["state"] = "normal"
        self.__canvas.draw()
        #self.__draw_devices()
        
    # Matplotlib draw devices and clusters
    def __draw_devices(self):
        self.__axis.cla()
        self.__axis.set_title("Wireless Sensor Network")
        energy = 0.0
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
                energy += dev.get_energy()
        self.__axis.text(0, 0, str(energy), fontsize=15)
        self.__canvas.draw()
        self.update()