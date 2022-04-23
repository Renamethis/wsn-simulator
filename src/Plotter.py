import matplotlib.pyplot as plt 
from src.Device import State
import sys
from random import random

class Plot:

    __colors = []

    def __init__(self, clusters):
        self.__clusters = clusters
        self.__number = 0
        self.__axis = plt.figure(self.__number).gca()
        self.__axis.figure.canvas.mpl_connect('key_press_event', self.on_press)
        plt.ion()

    # Matplotlib draw devices and clusters
    def draw_devices(self):
        plt.pause(1e-20)
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
        self.__axis.figure.show()

    def draw_traces(self, traces):
        self.__number += 1
        traceAxis = plt.figure(self.__number).gca()
        traceAxis.plot(traces, color=(random(), random(), random()))
        traceAxis.figure.show()

    def draw_energy(self, energy):
        self.__axis.text(0, 0, str(energy), fontsize=15)

    def on_press(self, event):
        if event.key == 'q':
            sys.exit(0)