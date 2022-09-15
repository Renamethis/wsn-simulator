import tkinter as tk
from src.GUI.Plotter import Plotter
from random import random
from src.Routing.ClusterNetwork import ClusterNetwork
from src.Routing.DirectCommunication import DirectCommunication
from threading import Thread
from matplotlib import gridspec as gridspec

class Simulator(Plotter):
    def __init__(self, root):
        Plotter.__init__(self, root)
        self.__gs = gridspec.GridSpec(1, 4)
        self._energy_axis = self._figure.add_subplot(121)
        self.__nodes_axis = self._figure.add_subplot(131)
        self._energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self._axis.text(0.5, 0.5, "Choose Network", bbox=dict(facecolor='red', alpha=0.5), horizontalalignment='center',
                    verticalalignment='center', transform=self._axis.transAxes, size=30)
        self._axis.figure.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.25, 
                    hspace=0.0)

    def simulate(self, iters, speed, **kwargs):
        self.__energy_axis.set_visible(False)
        self.__nodes_axis.set_visible(False)
        self._props = self._img_props_full
        self._draw_station()
        self._axis.set_position(self.__gs[0:4].get_position(self._figure))
        self._axis.set_subplotspec(self.__gs[0:4])
        self._network.simulate(iters, speed, **kwargs)
        self._is_draw_lock = True
        draw_thread = Thread(target=self.__draw_loop)
        draw_thread.start()

    def get_active(self):
        return self._active

    def stop(self):
        try:
            self._is_draw_lock = False
            self._network.stop()
            self._draw_devices()
        except AttributeError:
            return

    def __draw_loop(self):
        self._state = False
        self._active.set(True)
        while self._network.isRunning():
            self._draw_devices()
        if(self._exit):
            self._root.quit()
            return
        self._draw_devices()
        self._props = self._img_props_part
        energy_trace, nodes_trace = self._network.getTraces()
        self._simulation_number += 1
        self._energy_axis.set_visible(True)
        self._energy_axis.set_title("Energy consupmtion")
        self.__nodes_axis.set_visible(True)
        self.__nodes_axis.set_title("Number of alive nodes")
        self._energy_axis.plot(energy_trace, 
                                color=(random(), random(), random()), 
                                label=''.join([c for c in self._routing if c.isupper()]) + str(self._simulation_number))
        self._energy_axis.legend(loc="center right")
        self.__nodes_axis.plot(nodes_trace, color=(random(), random(), random()),
                               label=''.join([c for c in self._routing if c.isupper()]) + str(self._simulation_number))
        self.__nodes_axis.legend(loc="center right")
        # Replace subplots in canvas
        self._axis.set_position(self.__gs[0:2].get_position(self._figure))
        self._axis.set_subplotspec(self.__gs[0:2])
        self._energy_axis.set_position(self.__gs[2:3].get_position(self._figure))
        self._energy_axis.set_subplotspec(self.__gs[2:3])
        self.__nodes_axis.set_position(self.__gs[3:4].get_position(self._figure))
        self.__nodes_axis.set_subplotspec(self.__gs[3:4])
        self._props = self._img_props_part
        self._draw_station()
        self.draw()
        self._root.stop()
        self._state = True
        self._active.set(False)

    def _savesub(self, a, b):
        return a - b if a > b else 0