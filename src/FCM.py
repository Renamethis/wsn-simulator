import skfuzzy
import numpy as np
from sklearn.metrics import max_error
from src.Device import Device
from sys import maxsize

class FCM:
    def __init__(self, clusters):
        self.__clusters = clusters
        self.__size = len(clusters)

    def process(self):
        devices = sum([cluster.get_devices() for cluster in self.__clusters if cluster is not None], [])
        data = np.array([dev.get_pos() for dev in devices]).transpose()
        centroids, membership = skfuzzy.cluster.cmeans(data, len(self.__clusters),
                                                       2, error=0.005,
                                                       maxiter=1000, 
                                                       init=None)[0:2]
        heads = []
        reorganized = []
        for i in range(len(centroids)):
            centroid = centroids[i]
            min_dist = maxsize
            nearest = None
            for dev in devices:
                if(dev.alive() and not dev.is_sleep()):
                    distance = dev.calculate_distance_pos(centroid)
                    if(distance < min_dist):
                        min_dist = distance
                    nearest = dev
            if(nearest is not None):
                heads.append(nearest)
                reorganized.append([])
        new_clusters = [None for _ in self.__clusters]

        ccopy = centroids.copy().tolist()
        
        for i in range(len(ccopy)):
            if(self.__clusters[i] is None):
                continue
            centroid_node = Device(self.__clusters[i].get_centroid())
            index_source = index_copy = -1
            min_dist = maxsize
            for j in range(len(ccopy)):
                distance = centroid_node.calculate_distance_pos(ccopy[j])
                if(distance < min_dist):
                    min_dist = distance
                    index_source = centroids.tolist().index(ccopy[j])
                    index_copy = j
            new_clusters[index_source] = self.__clusters[i]
            del ccopy[index_copy]

        self.__clusters = new_clusters
        
        for i in range(len(devices)):
            dev = devices[i]
            id = np.argmax(membership[:, i])
            reorganized[id].append(dev)
    
        for i in range(len(reorganized)):
            self.__clusters[i].set_devices(reorganized[i])
            self.__clusters[i].set_centroid(centroids[i])
            self.__clusters[i].set_head(heads[i])

        self.head_rotation()

    def head_rotation(self):
        for i in range(len(self.__clusters)):
            if(self.__clusters[i] is None):
                continue
            max_energy = 0
            if(self.__clusters[i].get_alive_amount() <= 1):
                continue
            head = None
            for dev in self.__clusters[i].get_devices():
                if(dev.alive() and dev.get_energy() > max_energy):
                    max_energy = dev.get_energy()
                    head = dev
            self.__clusters[i].set_head(head)

    def get_clusters_amount(self):
        energy = sum([cluster.get_cluster_energy() for cluster in self.__clusters if cluster is not None])
        initial_energy = sum([cluster.get_cluster_initial_energy() for cluster in self.__clusters if cluster is not None])
        return int(0.5*self.__size*energy/initial_energy + 0.5*self.__size)
            