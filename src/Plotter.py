import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import gridspec as gridspec
import matplotlib.image as mpimg
from src.ClusterNetwork import ClusterNetwork
from src.DirectCommunication import DirectCommunication
from threading import Thread
from random import random

class Plotter(FigureCanvasTkAgg):

    def __init__(self, root, button):
        self.__button = button
        self.__root = root
        self.__simulation_number = 0
        self.__figure = Figure()
        self.__axis = self.__figure.add_subplot(111)
        self.__gs = gridspec.GridSpec(1, 4)
        self.__energy_axis = self.__figure.add_subplot(121)
        self.__nodes_axis = self.__figure.add_subplot(131)
        self.__energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self.__exit = False
        self.__is_draw_lock = True
        self.__color = None
        FigureCanvasTkAgg.__init__(self, self.__axis.figure, master=root)
        self.__state = False
        self.__station_image = mpimg.imread('resources/station.webp')
        self.__props = None
        self.__routing = None

    def simulate(self, iters, speed, **kwargs):
        self.__energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self.__props = self.__img_props_full
        self.__draw_station()
        self.__axis.set_position(self.__gs[0:4].get_position(self.__figure))
        self.__axis.set_subplotspec(self.__gs[0:4])
        self.__network.simulate(iters, speed, **kwargs)
        self.__is_draw_lock = True
        draw_thread = Thread(target=self.__draw_loop)
        draw_thread.start()

    def set_network(self, network, routing):
        if(network is None):
            self.__axis.cla()
            self.__image_axes.cla()
            self.__image_axes.axis('off')
            self.draw()
            return
        self.__clusters = network.get_clusters()
        self.__devices = sum([cluster.get_devices() for cluster in self.__clusters], [])
        self.__station = network.get_station()
        self.__img_props_full = [self.__savesub(network.get_station().get_pos()[0]/network.get_map_size()[0], 0.05), 
                                                    self.__savesub(network.get_station().get_pos()[1]/network.get_map_size()[1], 0.05), 0.1, 0.1]
        self.__img_props_part = [0.5*network.get_station().get_pos()[0]/network.get_map_size()[0] + 0.015, 
                        network.get_station().get_pos()[1]/network.get_map_size()[1] - 0.05, 0.06, 0.06]
        if(not self.__state):
            self.__props = self.__img_props_full
        else:
            self.__props = self.__img_props_part
        self.__routing = routing
        self.__button['state'] = 'normal'
        if(routing == "LEACH"):
            self.__network = ClusterNetwork(network)
        else:
            self.__network = DirectCommunication(network)
            self.__color = (random(), random(), random())
        self.__draw_station()
        self.__draw_devices()

    def isRunning(self):
        try:
            return self.__network.isRunning()
        except AttributeError:
            return False

    def clear(self):
        if(not self.isRunning()):
            self.__axis.cla()
            self.__energy_axis.cla()
            self.__nodes_axis.cla()
            self.__image_axes.cla()
            self.__image_axes.axis('off')
            self.__simulation_number = 0
            self.__energy_axis.set_visible(False)
            self.__nodes_axis.set_visible(False)
            self.__axis.set_position(self.__gs[0:4].get_position(self.__figure))
            self.__axis.set_subplotspec(self.__gs[0:4])
            self.__state = False
            self.draw()

    def stop(self):
        try:
            self.__is_draw_lock = False
            self.__network.stop()
            self.__draw_devices()
        except AttributeError:
            return

    def quit(self):
        self.__exit = True
        self.stop()

    def __draw_loop(self):
        self.__state = False
        self.__button["state"] = "disabled"
        while self.__network.isRunning():
            self.__draw_devices()
        if(self.__exit):
            self.__root.quit()
            return
        self.__draw_devices()
        self.__props = self.__img_props_part
        energy_trace, nodes_trace = self.__network.getTraces()
        self.__simulation_number += 1
        self.__energy_axis.set_visible(True)
        self.__energy_axis.set_title("Energy consupmtion")
        self.__nodes_axis.set_visible(True)
        self.__nodes_axis.set_title("Number of alive nodes")
        self.__energy_axis.plot(energy_trace, 
                                color=(random(), random(), random()), 
                                label=''.join([c for c in self.__routing if c.isupper()]) + str(self.__simulation_number))
        self.__energy_axis.legend(loc="upper right")
        self.__nodes_axis.plot(nodes_trace, color=(random(), random(), random()),
                               label=''.join([c for c in self.__routing if c.isupper()]) + str(self.__simulation_number))
        self.__nodes_axis.legend(loc="upper right")
        # Replace subplots in canvas
        self.__axis.set_position(self.__gs[0:2].get_position(self.__figure))
        self.__axis.set_subplotspec(self.__gs[0:2])
        self.__energy_axis.set_position(self.__gs[2:3].get_position(self.__figure))
        self.__energy_axis.set_subplotspec(self.__gs[2:3])
        self.__nodes_axis.set_position(self.__gs[3:4].get_position(self.__figure))
        self.__nodes_axis.set_subplotspec(self.__gs[3:4])
        self.__props = self.__img_props_part
        self.__draw_station()
        self.__button["state"] = "normal"
        self.draw()
        self.__root.stop()
        self.__state = True
    
    # Matplotlib draw devices and clusters
    def __draw_devices(self):
        self.__axis.cla()
        self.__axis.set_title("Wireless Sensor Network")
        energy = 0.0
        for dev in self.__devices:
            cluster = None
            for c in self.__clusters:
                if(dev in c.get_devices()):
                    cluster = c
                    break
            devpos = dev.get_pos()
            if(self.__routing != "LEACH" and not dev.is_sleep() and dev.alive()):
                self.__axis.plot(devpos[0], devpos[1], marker='o', 
                            linestyle='None', markersize=7, color=self.__color)
                self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Device", 
                                    fontsize=7)
            elif(dev is cluster.get_head() and dev.alive() and dev.is_head()):
                self.__axis.plot(devpos[0], devpos[1], marker='o', 
                            linestyle='None', markersize=7, color=(1, 0, 0))
                self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "CH", 
                                    fontsize=7)
            elif(not dev.alive()):
                self.__axis.plot(devpos[0], devpos[1], marker='o', 
                            linestyle='None', markersize=7, color=(0, 0, 0))
                self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Dead", 
                            fontsize=7)
            elif(dev.is_active()):
                self.__axis.plot(devpos[0], devpos[1], marker='o', 
                                    linestyle='None', markersize=7, 
                                    color=cluster.get_color())
                self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Device", 
                                    fontsize=7)
            elif(dev.is_sleep()):
                self.__axis.plot(devpos[0], devpos[1], marker='o', 
                                    linestyle='None', markersize=7, 
                                    color=(0.5, 0.5, 0.5))
                self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Sleep", 
                                    fontsize=7)
            energy += dev.get_energy()
        self.__axis.text(-0.1, -0.1, "Total energy: " + str(energy), horizontalalignment='left',
                         verticalalignment='center',
                         transform = self.__axis.transAxes)
        if(self.__is_draw_lock):
            self.draw()
        if(self.isRunning()):
            self.__root.update()

    def __draw_station(self):
        try:
            self.__image_axes.remove()
        except AttributeError:
            pass
        self.__image_axes = self.__axis.figure.add_axes(self.__props, anchor='NE', zorder=1)
        self.__image_axes.axis('off')
        self.__image_axes.imshow(self.__station_image)
        
    def __savesub(self, a, b):
        return a - b if a > b else 0
        