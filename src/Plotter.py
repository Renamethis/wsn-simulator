import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import gridspec as gridspec
import matplotlib.image as mpimg
from src.ClusterNetwork import ClusterNetwork
from src.DirectCommunication import DirectCommunication
from src.Device import State
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

        FigureCanvasTkAgg.__init__(self, self.__axis.figure, master=root)
        
        self.__station_image = mpimg.imread('resources/station.webp')
        self.__props = None
        self.__topology = False

    def simulate(self, flag):
        self.__energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self.__props = self.__img_props_full
        self.__draw_station()
        self.__axis.set_position(self.__gs[0:4].get_position(self.__figure))
        self.__axis.set_subplotspec(self.__gs[0:4])
        self.__network.simulate(flag)
        self.__is_draw_lock = True
        draw_thread = Thread(target=self.__draw_loop)
        draw_thread.start()

    def set_network(self, network, topology):
        self.__topology = topology
        if(network is None):
            self.__axis.cla()
            self.__image_axes.cla()
            self.__image_axes.axis('off')
            self.draw()
            return
        self.__clusters = network.get_clusters()
        self.__station = network.get_station()
        if(self.__props is None):
            self.__props = self.__img_props_full = [self.__savesub(network.get_station().get_pos()[0]/network.get_map_size()[0], 0.05), 
            self.__savesub(network.get_station().get_pos()[1]/network.get_map_size()[1], 0.05), 0.1, 0.1]
            self.__img_props_part = [self.__savesub(0.5*network.get_station().get_pos()[0]/network.get_map_size()[0], 0), 
        self.__savesub(network.get_station().get_pos()[1]/network.get_map_size()[1], 0.03), 0.06, 0.06]
        self.__draw_station()
        self.__draw_devices()
        self.__button['state'] = 'normal'
        if(topology):
            self.__network = ClusterNetwork(network, 50000)
        else:
            self.__network = DirectCommunication(network, 50000)

    def isRunning(self):
        try:
            return self.__network.isRunning()
        except AttributeError:
            return False

    def stop(self):
        self.__exit = True
        try:
            self.__is_draw_lock = False
            self.__network.stop()
        except AttributeError:
            return
        
    def __draw_loop(self):
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
                                label=str(self.__simulation_number))
        self.__energy_axis.legend(loc="lower left")
        self.__nodes_axis.plot(nodes_trace, color=(random(), random(), random()),
                               label=str(self.__simulation_number))
        self.__nodes_axis.legend(loc="lower left")
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
    
    # Matplotlib draw devices and clusters
    def __draw_devices(self):
        self.__axis.cla()
        self.__axis.set_title("Wireless Sensor Network")
        energy = 0.0
        for cluster in self.__clusters:
            for dev in cluster.get_devices():
                devpos = dev.get_pos()
                if(not self.__topology and dev.alive()):
                    self.__axis.plot(devpos[0], devpos[1], marker='o', 
                             linestyle='None', markersize=7, color=(0, 1, 1))
                    self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Device", 
                                     fontsize=7)
                elif(dev is cluster.get_head() and dev.alive()):
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
        