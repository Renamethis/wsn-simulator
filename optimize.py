from src.Device import Device, DeviceCluster
from src.WSN import WSN
from random import random
from sklearn.cluster import KMeans
import numpy as np
from kneed import KneeLocator
from sklearn.metrics import pairwise_distances

# Safety substract
def savesub(a, b):
    return  a - b if (a - b > 0) else 0

# Safety add
def saveadd(a, b, max):
    return a + b if (a + b < max) else max

map_size = (1000, 1000)
devices_amount = 50
Devices = []
max_clusters_amount = 10
points = []

### INITIALIZE MAP

delta = 10
for i in range(devices_amount):
    current_position = [int(random()*map_size[0]), int(random()*map_size[1])]
    new_device = Device(current_position)
    Devices.append(new_device)
    points.append(current_position)

### FIND BEST AMOUNT OF CLUSTERS BY DEVICES POSITION

sse = []
for k in range(1, max_clusters_amount):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(points)
    sse.append(kmeans.inertia_)
kl = KneeLocator(range(1, max_clusters_amount), sse, curve="convex", 
                 direction="decreasing")

### MAKE PREDICTIONS

kmeans = KMeans(n_clusters=kl.elbow)
kmeans.fit(points)
predictions = kmeans.predict(points)
centers = kmeans.cluster_centers_

### INITIALIZE DEVICE CLUSTERS

clusters = []
for i in range(0, len(centers)):
    clusterDevices = np.array(Devices)[np.where(predictions == i)]
    positions = [dev.get_pos() for dev in clusterDevices]
    dist = pairwise_distances(positions, [centers[i]], metric='euclidean',
                              n_jobs=None, force_all_finite=True)[:, 0]
    head = clusterDevices[np.where(dist == min(dist))][0]
    cluster = DeviceCluster(clusterDevices.tolist(), head)
    clusters.append(cluster)

### Simulate WSN network

net = WSN(clusters, 20000)
net.simulate()

