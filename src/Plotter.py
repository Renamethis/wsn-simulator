import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import gridspec as gridspec
import matplotlib.image as mpimg
from src.WSN import WSN
from src.Device import State
from threading import Thread

class Plotter(FigureCanvasTkAgg):

    def __init__(self, network, iters, root):
        self.__root = root
        self.__simulation_number = 0
        self.__network = WSN(network, iters)
        self.__clusters = network.get_clusters()
        self.__station = network.get_station()
        self.__figure = Figure()
        self.__axis = self.__figure.add_subplot(111)
        self.__gs = gridspec.GridSpec(1, 4)
        self.__energy_axis = self.__figure.add_subplot(121)
        self.__nodes_axis = self.__figure.add_subplot(131)
        self.__energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self.__exit = False
        
        FigureCanvasTkAgg.__init__(self, self.__axis.figure, master=root)
        
        self.__station_image = mpimg.imread('resources/station.webp')
        self.__img_props_full = [self.__savesub(self.__station.get_pos()[0]/network.get_map_size()[0], 0.05), 
                self.__savesub(self.__station.get_pos()[1]/network.get_map_size()[1], 0.05), 0.1, 0.1]
        self.__img_props_part = [self.__savesub(0.5*self.__station.get_pos()[0]/network.get_map_size()[0], 0), 
                self.__savesub(self.__station.get_pos()[1]/network.get_map_size()[1], 0.03), 0.06, 0.06]
        self.__image_axes = self.__axis.figure.add_axes(self.__img_props_full, anchor='NE', zorder=1)
        self.__image_axes.axis('off')

    def simulate(self, flag, button):
        self.__button = button
        self.__energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self.__draw_station(self.__img_props_full)
        self.__axis.set_position(self.__gs[0:4].get_position(self.__figure))
        self.__axis.set_subplotspec(self.__gs[0:4])
        self.__network.simulate(flag)
        draw_thread = Thread(target=self.__draw_loop)
        draw_thread.start()

    def isRunning(self):
        return self.__network.isRunning()

    def stop(self):
        self.__exit = True
        self.__network.stop()
        
    def __draw_loop(self):
        self.__button["state"] = "disabled"
        while self.__network.isRunning():
            self.__draw_devices()
        if(self.__exit):
            self.__root.quit()
            return
        self.__draw_devices()
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
        self.__draw_station(self.__img_props_part)
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
        if(self.isRunning()):
            self.draw()
            self.__root.update()

    def __draw_station(self, props):
        self.__image_axes.remove()
        self.__image_axes = self.__axis.figure.add_axes(props, anchor='NE', zorder=1)
        self.__image_axes.axis('off')
        self.__image_axes.imshow(self.__station_image)
        
    def __savesub(self, a, b):
        return a - b if a > b else 0
        