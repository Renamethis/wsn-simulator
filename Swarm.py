from math import sqrt, pow
from Device import Device, Sensor, DeviceCluster
class Selection:
    def __init__(self, clusters):
        self.__clusters = clusters
    # Fitness function for energy
    def ff_energy(self):
        pass
    # Fitness function for distance
    def ff_distance(self):
        pass
    # Distance calculation
    def get_distance(self, p1, p2):
        return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - [1], 2))