from random import random
from src.Network.Device import State

class DeviceCluster:

    def __init__(self, devices, head, centroid, color=None):
        self.__devices = devices
        self.__cluster_head = head
        self.__cluster_head.set_state(State.HEAD)
        if(color is None):
            self.__color = (random(), random(), random())
        else:
            self.__color = color
        self.__centroid = centroid
    
    # SETTERS

    def set_head(self, head):
        self.__cluster_head.set_state(State.ACTIVE)
        self.__cluster_head = head
        self.__cluster_head.set_state(State.HEAD)

    def set_devices(self, devices):
        self.__devices = devices

    def set_centroid(self, centroid):
        self.__centroid = centroid

    # GETTERS

    def get_centroid(self):
        return self.__centroid

    def get_devices(self):
        return self.__devices

    def get_head(self):
        return self.__cluster_head

    def get_color(self):
        return self.__color

    def get_alive_amount(self):
        return sum([1 for device in self.get_devices() if device.alive()])

    # Return remaining energy in whole cluster
    def get_cluster_energy(self):
        energy = 0
        for dev in self.__devices:
            if(dev.alive()):
                energy += dev.get_energy()
        return energy

    # Return initial energy of whole cluster
    def get_cluster_initial_energy(self):
        energy = 0
        for dev in self.__devices:
            if(dev.alive()):
                energy += dev.get_initial_energy()
        return energy
