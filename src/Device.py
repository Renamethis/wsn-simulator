from ast import Constant
from enum import Enum, auto
from math import sqrt
from random import random
# Defined constants
class Constants(float, Enum):
    # energy dissipated at the transceiver electronic
    ENERGY = 50e-9
    # energy dissipated at the power amplifier (multi-path)
    E_MP = 0.0013e-12
    # energy dissipated at the power amplifier (line-of-sight)
    E_FS = 10e-9
    # energy dissipated at the data aggregation
    E_DA = 5e-7
    # energy dissipated at other electronics
    E_ED = 50e-5
    # default message length
    MESSAGE_LENGTH = 2000
    # threshold distance value
    THRESHOLD_DIST = sqrt(E_FS/E_MP)

# Sensor types
class Sensors(Enum):
    DEFAULT = 0

# Device state
class State(Enum):
    HEAD = auto()
    ACTIVE = auto()
    SLEEP = auto()
    DEAD = auto()

# WSN node class
class Device:

    def __init__(self, pos, energy=0.5, sensor_type=Sensors.DEFAULT):
        self.__pos = pos
        self.__initial_energy = self.__energy = energy
        self.__sensor_type = sensor_type
        self.__state = State.ACTIVE

    ## SETTERS

    def set_energy(self, energy):
        self.__energy = energy

    def set_state(self, state):
        self.__state = state

    ## GETTERS 

    def get_state(self):
        return self.__state

    def get_pos(self):
        return self.__pos

    def get_energy(self):
        return self.__energy

    def get_initial_energy(self):
        return self.__initial_energy

    # Check if device alive
    def alive(self):
        return self.__energy > 0.0

    # Calculate and sub transmitter energy consumption
    def send_data(self, length, receiver):
        if(self.__state == State.SLEEP):
            return
        distance = self.__calculate_distance(receiver)
        # Transmitter energy model 
        energy = Constants.ENERGY
        if(distance > Constants.THRESHOLD_DIST):
            energy += Constants.E_MP*(distance**4)
        else:
            energy += Constants.E_FS*(distance**2)
        energy *= length
        self.consume(energy)
        receiver.receive(length)
        receiver.aggregate(length)

    # Energy spent on receive message
    def receive(self, length):
        self.consume(Constants.ENERGY * length)

    # Energy spent on aggregate message
    def aggregate(self, length):
        self.consume(Constants.E_DA * length)

    # Energy spent on other electronics
    def stay(self):
        self.consume(Constants.E_ED)

    # Consume energy function
    def consume(self, energy):
        if(energy > self.__energy):
            self.__energy = 0
        else:
            self.__energy -= energy

    # Reset energy device and state
    def reset(self):
        self.__energy = self.__initial_energy
        if(self.__state == State.HEAD):
            return
        self.__state = State.ACTIVE

    # Reset energy device and state 
    def reset(self, energy):
        self.__energy = energy
        if(self.__state == State.HEAD):
            return
        self.__state = State.ACTIVE

    # Calculate distance between two nodes
    def __calculate_distance(self, node):
        return sqrt((self.get_pos()[0] - node.get_pos()[0])**2 + (self.get_pos()[1] - 
            node.get_pos()[1])**2)

class DeviceCluster:

    def __init__(self, devices, head):
        self.__devices = devices
        self.__cluster_head = head
        self.__color = (random(), random(), random())
    
    # SETTERS

    def set_head(self, head):
        self.__cluster_head = head
        self.__cluster_head.set_state(State.HEAD)

    # GETTERS

    def get_devices(self):
        return self.__devices

    def get_head(self):
        return self.__cluster_head

    def get_color(self):
        return self.__color

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


