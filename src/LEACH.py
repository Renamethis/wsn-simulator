from random import random
import numpy as np

class LEACH:
    
    def __init__(self, clusters, a=0.5, b=0.0, c=0.5):
        self.__a = a
        self.__b = b
        self.__c = c
        self.__clusters = clusters
        self.__devices = sum([cluster.get_devices() for cluster in self.__clusters], [])
    
    def process(self):
        heads = []
        
        for cluster in self.__clusters:
            head = None
            devices = cluster.get_devices()
            i = 0
            while head is None and cluster.get_alive_amount() > 0:
                if(devices[i].alive()):
                    max_dist = 0
                    for d in cluster.get_devices():
                        if(d.calculate_distance_pos(cluster.get_centroid()) > max_dist):
                            max_dist = d.calculate_distance_pos(cluster.get_centroid())
                    threshold = self.__a*(devices[i].get_energy()/devices[i].get_initial_energy()) + self.__b*(cluster.get_cluster_energy()/cluster.get_cluster_initial_energy() + self.__c*(devices[i].calculate_distance_pos(cluster.get_centroid())/max_dist))
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

            