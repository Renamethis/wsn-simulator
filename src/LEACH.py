from random import random
import numpy as np

class LEACH:
    
    def __init__(self, clusters, station, a=0.2, b=0.4, c=0.4):
        self.__clusters = clusters
        self.__station = station
        self.__a = a
        self.__b = b
        self.__c = c
    
    def process(self):
        heads = []
        for cluster in self.__clusters:
            head = None
            devices = cluster.get_devices()
            i = 0
            while head is None and cluster.get_alive_amount() > 0:
                if(devices[i].alive()):
                    min_dist_station = 10000
                    min_dist_centroid = 10000
                    max_energy = 0
                    for d in cluster.get_devices():
                        if(d.calculate_distance(self.__station) < min_dist_station):
                            min_dist_station = d.calculate_distance(self.__station)
                        if(d.calculate_distance_pos(cluster.get_centroid()) < min_dist_centroid):
                            min_dist_centroid = d.calculate_distance_pos(cluster.get_centroid())
                        if(d.get_energy() > max_energy):
                            max_energy = d.get_energy()
                    threshold = self.__a*(devices[i].get_energy()/max_energy) + self.__b*(min_dist_centroid/devices[i].calculate_distance_pos(cluster.get_centroid()) + self.__c*(min_dist_station/devices[i].calculate_distance(self.__station)))
                    rnd = np.random.uniform(0, 1)
                    if(rnd < threshold):
                        head = devices[i]
                        break
                i = 0 if i + 1 == len(devices) else i + 1
            if(head is not None):
                heads.append(head)
        if(len(heads) > 0):
            for cluster in self.__clusters:
                for head in heads:
                    if(head in cluster.get_devices()):
                        cluster.set_head(head)
                        del head
                        break

            