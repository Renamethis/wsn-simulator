import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
from src.Routing.ClusterNetwork import ClusterNetwork
from src.Routing.DirectCommunication import DirectCommunication
from random import random

class Plotter(FigureCanvasTkAgg):

    def __init__(self, root):
        #self._button = button
        self._root = root
        self._simulation_number = 0
        self._figure = Figure()
        self._axis = self._figure.add_subplot(111)
        #self._axis.axis('off')
        self._exit = False
        self.__is_draw_lock = True
        self._color = None
        FigureCanvasTkAgg.__init__(self, self._axis.figure, master=root)
        self._state = False
        self._station_image = mpimg.imread('resources/station.webp')
        self._props = None
        self._routing = None
        self._active = tk.BooleanVar()
        self._axis.set_xlim([0, 300])
        self._axis.set_ylim([0, 300])
        self._active.set(False)
        self._image_axes = None
        self._axis.figure.subplots_adjust(left=0.00,
                    bottom=0.00, 
                    right=1.0, 
                    top=1.0, 
                    wspace=0.25, 
                    hspace=0.0)
        self._axis.axis('off')
        

    def set_network(self, network, routing):
        self._active.set(True)
        if(network is None):
            self._axis.cla()
            self._image_axes.cla()
            self._image_axes.axis('off')
            self.draw()
            return
        self._clusters = network.get_clusters()
        self._devices = sum([cluster.get_devices() for cluster in self._clusters], [])
        self._station = network.get_station()
        self.__map_size = network.get_map_size()
        self._axis.set_xlim([0, self.__map_size[0]])
        self._axis.set_ylim([0, self.__map_size[1]])
        if(self._station is not None):
            self._img_props_full = [self._savesub(network.get_station().get_pos()[0]/self.__map_size[0], 0.05), 
                                                        self._savesub(network.get_station().get_pos()[1]/self.__map_size[1], 0.05), 0.1, 0.1]
            self._img_props_part = [0.5*network.get_station().get_pos()[0]/self.__map_size[0] + 0.015, 
                            network.get_station().get_pos()[1]/self.__map_size[1] - 0.05, 0.06, 0.06]
            if(not self._state):
                self._props = self._img_props_full
            else:
                self._props = self._img_props_part
        self._routing = routing
        if(routing == "LEACH" or routing == "FCM"):
            self._network = ClusterNetwork(network)
        else:
            self._network = DirectCommunication(network)
            self._color = network.get_color()
        self._draw_station()
        self._draw_devices()

    def clear(self):
        if(not self.isRunning()):
            self._axis.cla()
            self._energy_axis.cla()
            self._nodes_axis.cla()
            self._image_axes.cla()
            self._image_axes.axis('off')
            self._simulation_number = 0
            self._energy_axis.set_visible(False)
            self._nodes_axis.set_visible(False)
            self._axis.set_position(self._gs[0:4].get_position(self._figure))
            self._axis.set_subplotspec(self._gs[0:4])
            self._state = False
            self.draw()

    def isRunning(self):
        try:
            return self._network.isRunning()
        except AttributeError:
            return False

    '''    def set_size(self, size):    
        l = self._axis.figure.subplotpars.left
        r = self._axis.figure.subplotpars.right
        t = self._axis.figure.subplotpars.top
        b = self._axis.figure.subplotpars.bottom
        figw = float(size[0])/(r-l)
        figh = float(size[1])/(t-b)
        print(figw, figh)
        self._axis.figure.set_size_inches(figw, figh)
    '''

    def quit(self):
        self._exit = True
        self.stop()
    
    # Matplotlib draw devices and clusters
    def _draw_devices(self):
        self._axis.cla()
        self._axis.set_title("Wireless Sensor Network")
        self._axis.axis('off')
        self._axis.set_xlim([0, self.__map_size[0]])
        self._axis.set_ylim([0, self.__map_size[1]])
        energy = 0.0
        for dev in self._devices:
            cluster = None
            for c in self._clusters:
                if(dev in c.get_devices()):
                    cluster = c
                    break
            if(cluster is not None):
                devpos = dev.get_pos()
                if(self._routing != "LEACH" and self._routing != "FCM" and not dev.is_sleep() and dev.alive()):
                    self._axis.plot(devpos[0], devpos[1], marker='o', 
                                linestyle='None', markersize=7, color=self._color)
                    self._axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Device", 
                                        fontsize=7)
                elif(dev is cluster.get_head() and dev.alive() and dev.is_head()):
                    self._axis.plot(devpos[0], devpos[1], marker='o', 
                                linestyle='None', markersize=7, color=(1, 0, 0))
                    self._axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "CH", 
                                        fontsize=7)
                elif(not dev.alive()):
                    self._axis.plot(devpos[0], devpos[1], marker='o', 
                                linestyle='None', markersize=7, color=(0, 0, 0))
                    self._axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Dead", 
                                fontsize=7)
                elif(dev.is_active()):
                    self._axis.plot(devpos[0], devpos[1], marker='o', 
                                        linestyle='None', markersize=7, 
                                        color=cluster.get_color())
                    self._axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Device", 
                                        fontsize=7)
                elif(dev.is_sleep()):
                    self._axis.plot(devpos[0], devpos[1], marker='o', 
                                        linestyle='None', markersize=7, 
                                        color=(0.5, 0.5, 0.5))
                    self._axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Sleep", 
                                        fontsize=7)
                energy += dev.get_energy()
        self._axis.text(-0.1, -0.1, "Total energy: " + str(energy), horizontalalignment='left',
                         verticalalignment='center',
                         transform = self._axis.transAxes)
        if(self.__is_draw_lock):
            self.draw()
        if(self.isRunning()):
            self._root.update()

    def _draw_station(self):
        if(self._station is not None):
            try:
                self._image_axes.remove()
            except AttributeError:
                pass
            self._image_axes = self._axis.figure.add_axes(self._props, anchor='NE', zorder=1)
            self._image_axes.axis('off')
            self._image_axes.imshow(self._station_image)
            self._image_axes.set_visible(True)
        elif(self._image_axes is not None):
            self._image_axes.set_visible(False)

    def _savesub(self, a, b):
        return a - b if a > b else 0
        