
from src.Device import Device, DeviceNetwork, Sensors
from src.Clustering import Clustering
import numpy as np
class Generator:
    def __init__(self, map_size, devices_amount, initial_energy, coverage, station_pos):
        self.__map_size = map_size
        self.__devices_amount = devices_amount
        self.__initial_energy = initial_energy
        self.__coverage = coverage
        self.__station_position = station_pos

    def generate(self):
        self.__devices = []
        for i in range(self.__devices_amount):
            current_position = [
                np.random.uniform(0, self.__map_size[0]),
                np.random.uniform(0, self.__map_size[1])
            ]
            new_device = Device(current_position, energy=self.__initial_energy, 
                                coverage=self.__coverage)
            self.__devices.append(new_device)
        self.__baseStation = Device(self.__station_position, 
                                    sensor_type=Sensors.STATION)

    def clustering(self):
        clustering = Clustering(self.__devices)
        clusters = clustering.clustering()
        return DeviceNetwork(clusters, self.__baseStation, self.__map_size)
        