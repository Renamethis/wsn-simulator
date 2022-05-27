
from sklearn.cluster import KMeans
import numpy as np
from kneed import KneeLocator
from sklearn.metrics import pairwise_distances
from src.Network.Cluster import DeviceCluster

MAX_CLUSTER_AMOUNT = 10

class Clustering:
    def __init__(self, devices):
        self.__devices = devices
        points = [dev.get_pos() for dev in devices]
        sse = []
        max_clusters = MAX_CLUSTER_AMOUNT if len(devices) >= MAX_CLUSTER_AMOUNT else len(devices)
        for k in range(1, max_clusters):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(points)
            sse.append(kmeans.inertia_)
        kl = KneeLocator(range(1, max_clusters), sse, curve="convex", 
                        direction="decreasing")
        kmeans = KMeans(n_clusters=kl.elbow)
        kmeans.fit(points)
        self.__predictions = kmeans.predict(points)
        self.__centers = kmeans.cluster_centers_


    def clustering(self):
        clusters = []
        for i in range(0, len(self.__centers)):
            clusterDevices = np.array(self.__devices)[np.where(self.__predictions == i)]
            positions = [dev.get_pos() for dev in clusterDevices]
            dist = pairwise_distances(positions, [self.__centers[i]], metric='euclidean',
                                    n_jobs=None, force_all_finite=True)[:, 0]
            head = clusterDevices[np.where(dist == min(dist))][0]
            cluster = DeviceCluster(clusterDevices.tolist(), head, self.__centers[i])
            clusters.append(cluster)
        return clusters
        