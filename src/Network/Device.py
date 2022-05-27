from enum import Enum, auto
from math import sqrt, log
from random import random
from numpy import cov

# Defined constants
class Constants(float, Enum):
    # energy dissipated at the transceiver electronic
    ENERGY = 50e-10
    # energy dissipated at the power amplifier (multi-path)
    E_MP = 0.0013e-12
    # energy dissipated at the power amplifier (line-of-sight)
    E_FS = 10e-12
    # energy dissipated at the data aggregation
    E_DA = 5e-10
    # energy dissipated at other electronics
    E_ED = 50e-8
    # default message length
    MESSAGE_LENGTH = 2000

# Sensor types
class Sensors(Enum):
    DEFAULT = auto()
    STATION = auto()

# Device state
class State(Enum):
    HEAD = auto()
    ACTIVE = auto()
    SLEEP = auto()
    DEAD = auto()

# WSN node class
class Device:

    def __init__(self, pos, energy=2, sensor_type=Sensors.DEFAULT, coverage=50,
                 speed=100):
        self.__speed = speed
        self.__coverage = coverage
        self.__pos = pos
        self.__initial_energy = self.__energy = energy
        self.__sensor_type = sensor_type
        self.__state = State.ACTIVE
        self.__aggregation_size = 0

    ## SETTERS
    
    def set_speed(self, speed):
        self.__speed = speed

    def set_energy(self, energy):
        self.__energy = energy

    def set_state(self, state):
        self.__state = state

    def set_pos(self, pos):
        self.__pos = pos

    def set_coverage(self, coverage):
        self.__coverage = coverage

    def set_initial_energy(self, initial_energy):
        self.__initial_energy = initial_energy

    ## GETTERS
    def get_coverage(self):
        return self.__coverage

    def get_aggregation_size(self):
        return self.__aggregation_size

    def get_state(self):
        return self.__state

    def get_pos(self):
        return self.__pos

    def get_energy(self):
        return self.__energy

    def get_initial_energy(self):
        return self.__initial_energy

    def get_sensor_type(self):
        return self.__sensor_type

    # Check if device alive
    def alive(self):
        return self.__energy > 0.0

    def go_sleep(self):
        self.__state = State.SLEEP
    
    def go_active(self):
        self.__state = State.ACTIVE

    def go_head(self):
        self.__state = State.HEAD
    
    def set_station(self):
        self.__sensor_type = Sensors.STATION

    def set_device(self):
        self.__sensor_type = Sensors.DEFAULT
    
    def is_station(self):
        return self.__sensor_type == Sensors.STATION
    
    def is_active(self):
        return self.__state == State.ACTIVE

    def is_head(self):
        return self.__state == State.HEAD

    def is_sleep(self):
        return self.__state == State.SLEEP

    def add_data_to_aggregation(self, length):
        self.__aggregation_size += length

    # Calculate and sub transmitter energy consumption
    def send_data(self, receiver, length=Constants.MESSAGE_LENGTH):
        if(self.__state == State.SLEEP):
            return
        distance = self.calculate_distance(receiver)
        # Transmitter energy model 
        energy = Constants.ENERGY
        if(distance > self.__coverage):
            energy += Constants.E_MP*(distance**4)
        else:
            energy += Constants.E_FS*(distance**2)
        energy *= length
        self.consume(energy * self.__speed)
        receiver.receive(length)
        if(self.__sensor_type != Sensors.STATION):
            receiver.add_data_to_aggregation(length)

    # Energy spent on receive message
    def receive(self, length):
        self.consume(Constants.ENERGY * length * self.__speed)

    # Energy spent on aggregate message
    def aggregate(self):
        if(self.__aggregation_size):
            self.consume(Constants.E_DA * log(self.__aggregation_size) * self.__speed)
        self.__aggregation_size = 0

    # Energy spent on other electronics
    def stay(self):
        self.consume(Constants.E_ED * self.__speed)

    # Consume energy function
    def consume(self, energy):
        if(self.__sensor_type != Sensors.STATION):
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

    # Calculate distance between two nodes
    def calculate_distance(self, node):
        return sqrt((self.get_pos()[0] - node.get_pos()[0])**2 + (self.get_pos()[1] - 
            node.get_pos()[1])**2)

    def calculate_distance_pos(self, pos):
        return sqrt((self.get_pos()[0] - pos[0])**2 + (self.get_pos()[1] - 
            pos[1])**2)