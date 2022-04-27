
from src.Device import Device, DeviceNetwork, Sensors
from src.Clustering import Clustering
import numpy as np
class Generator:
    def __init__(self, map_size, devices_amount):
        self.__map_size = map_size
        self.__devices_amount = devices_amount

    def generate(self):
        self.__devices = []
        for i in range(self.__devices_amount):
            current_position = [
                np.random.uniform(0, self.__map_size[0]),
                np.random.uniform(0, self.__map_size[1])
            ]
            new_device = Device(current_position)
            self.__devices.append(new_device)
        self.__baseStation = Device((self.__map_size[0]/2, self.__map_size[1]/2), 
                     sensor_type=Sensors.STATION)

    def clustering(self):
        clustering = Clustering(self.__devices)
        clusters = clustering.clustering()
        return DeviceNetwork(clusters, self.__baseStation, self.__map_size)
        