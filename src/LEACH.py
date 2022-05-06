from random import random
from re import L
from xmlrpc.client import MAXINT
import numpy as np
from sys import maxsize
from random import shuffle

class LEACH:
    
    def __init__(self, clusters, station, a=0.4, b=0.4, c=0.6):
        self.__clusters = clusters
        self.__station = station
        self.__devices = sum([cluster.get_devices() for cluster in self.__clusters], [])
        shuffle(self.__devices)
        self.__a = a
        self.__b = b
        self.__c = c
    
    def process(self):
        heads = []
        i = 0
        shuffle(self.__devices)
        while len(heads) != len(self.__clusters):
            device = self.__devices[i]
            if(not device.alive() or device.is_sleep()):
                i = 0 if i + 1 == len(self.__devices) else i + 1
                continue
            max_energy = 0.0
            min_dist_station = maxsize
            for dev in self.__devices:
                if(dev.get_energy() > max_energy):
                    max_energy = dev.get_energy()
                if(dev.calculate_distance(self.__station) < min_dist_station):
                    min_dist_station = dev.calculate_distance(self.__station)
            if(max_energy != 0):
                threshold = self.__a*(device.get_energy()/max_energy) + self.__c*(min_dist_station/device.calculate_distance(self.__station))
            else:
                threshold = 0
            rnd = np.random.uniform(0, 1)
            if(rnd < threshold):
                heads.append(device)
            i = 0 if i + 1 == len(self.__devices) else i + 1

        reorganized = []
        for head in heads:
            reorganized.append([])
        for dev in self.__devices:
            min_dist = maxsize
            k = -1
            for i in range(len(heads)):
                head = heads[i]
                if(head.calculate_distance(dev) < min_dist):
                    min_dist = head.calculate_distance(dev)
                    k = i
            if(k != -1 and dev not in sum(reorganized, [])):
                reorganized[k].append(dev)
        if(reorganized):
            for i in range(len(heads)):
                self.__clusters[i].set_head(heads[i])
                devices = reorganized[i]
                self.__clusters[i].set_devices(devices)
            
            