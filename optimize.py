from Device import Device, Sensor, DeviceCluster
from random import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from kneed import KneeLocator
from sklearn.metrics import pairwise_distances
import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point

# Safety substract
def savesub(a, b):
    return  a - b if (a - b > 0) else 0

# Safety add
def saveadd(a, b, max):
    return a + b if (a + b < max) else max

# Matplotlib draw devices, sensors and clusters
def draw_devices(clusters):
    chColor = (1, 0, 0)
    for cluster in clusters:
        deviceColor = (random(), random(), random())
        sensorColor = (random(), random(), random())
        for dev in cluster.get_devices():
            devpos = dev.get_pos()
            senspos = dev.get_sensor().get_pos()
            if(dev is cluster.get_head()):
                plt.plot(devpos[0], devpos[1], marker='o', linestyle='None', markersize=7, color=chColor)
                plt.text(devpos[0] + 0.5, devpos[1] + 0.5, "CH", fontsize=7)
            else:
                plt.plot(devpos[0], devpos[1], marker='o', linestyle='None', markersize=7, color=deviceColor)
                plt.text(devpos[0] + 0.5, devpos[1] + 0.5, "Device", fontsize=7)
            plt.plot(senspos[0], senspos[1], marker='o', linestyle='None', markersize=7, color=sensorColor)
            plt.plot([devpos[0], senspos[0]], [devpos[1], senspos[1]], 'g-')
            plt.text(senspos[0] + 0.5, senspos[1] + 0.5, "Sensor", fontsize=7)
    plt.show()


map_size = (1000, 1000)
devices_amount = 50
Devices = []
max_clusters_amount = 10
points = []
### INITIALIZE MAP
delta = 10
for i in range(devices_amount):
    current_position = [int(random()*map_size[0]), int(random()*map_size[1])]
    sensor_x = savesub(current_position[0], 30) + \
                       random()*(saveadd(current_position[0], 30, map_size[0] - 1) - \
                       savesub(current_position[0], 15)) + delta
    sensor_y = savesub(current_position[1], 30) + \
                       random()*(saveadd(current_position[1], 30, map_size[1] - 1) - \
                       savesub(current_position[1], 15)) + delta
    new_delay = int(random()*10)
    new_energy = int(random()*10)
    temperature = 30 + int(random()*30)
    load = int(100*random())
    new_device = Device(current_position, new_delay, new_energy, temperature, load)
    
    new_device.set_sensor(Sensor([sensor_x, sensor_y]))
    Devices.append(new_device)
    points.append(current_position)

### FIND BEST AMOUNT OF CLUSTERS BY DEVICES POSITION
sse = []
for k in range(1, max_clusters_amount):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(points)
    sse.append(kmeans.inertia_)
kl = KneeLocator(range(1, max_clusters_amount), sse, curve="convex", direction="decreasing")
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
    dist = pairwise_distances(positions, [centers[i]], metric='euclidean', n_jobs=None, force_all_finite=True)[:, 0]
    head = clusterDevices[np.where(dist == min(dist))][0]
    cluster = DeviceCluster(clusterDevices.tolist(), head, i)
    clusters.append(cluster)
### DRAW INITIAL DATA
draw_devices(clusters)