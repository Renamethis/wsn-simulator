from ast import Constant
from enum import Enum
from math import sqrt
from random import random
# Defined constants
class Constants(float, Enum):
    # energy dissipated at the transceiver electronic
    ENERGY = 50e-9
    # energy dissipated at the power amplifier (multi-path)
    E_MP = 0.0013e-12 
    # energy dissipated at the power amplifier (line-of-sight)
    E_FS = 10e-12 
    # energy dissipated at the data aggregation
    E_DA = 5e-9
    # energy dissipated at other electronics
    E_ED = 50e-5
    # default message length
    MESSAGE_LENGTH = 2000
    # threshold distance value
    THRESHOLD_DIST = sqrt(E_FS/E_MP)

# Sensor types
class Sensors(Enum):
    DEFAULT = 0

# WSN node class
class Device:

    def __init__(self, pos, energy=2.0, sensor_type=Sensors.DEFAULT):
        self._pos = pos
        self._energy = energy
        self._sensor_type = sensor_type

    def alive(self):
        return self._energy > 0.0

    # Calculate and sub transmitter energy consumption
    def send_data(self, length, receiver):
        distance = self.__calculate_distance(self, receiver)
        # Transmitter energy model 
        energy = Constants.ENERGY
        if(distance > Constants.THRESHOLD_DIST):
            energy += Constants.E_MP*(distance**4)
        else:
            energy += Constants.E_FS*(distance**2)
        energy *= length

        self._energy -= energy
        receiver.receive(length)
        receiver.aggregate(length)

    # Energy spent on receive message
    def receive(self, length):
        self._energy -= Constants.ENERGY * length

    # Energy spent on aggregate message
    def aggregate(self, length):
        self._energy -= Constants.E_DA * length

    # Energy spent on other electronics
    def consume(self):
        self._energy -= Constants.E_ED

    def get_pos(self):
        return self._pos

    def get_energy(self):
        return self._energy

    # Calculate distance between two nodes
    def __calculate_distance(self, n1, n2):
        return sqrt((n1.get_pos()[0] - n2.get_pos()[0])**2 + (n1.get_pos()[1] - 
            n2.get_pos()[1])**2)

class DeviceCluster:

    def __init__(self, devices, head):
        self.__devices = devices
        self.__cluster_head = head
        self.__color = (random(), random(), random())

    # Return remaining energy in whole cluster
    def get_cluster_energy(self):
        energy = 0
        for dev in self.__devices:
            if(dev.alive()):
                energy += dev.get_energy()
        return energy

    # Getters

    def get_devices(self):
        return self.__devices

    def get_head(self):
        return self.__cluster_head

    def get_color(self):
        return self.__color


