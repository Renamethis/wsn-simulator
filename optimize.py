from Device import Device, Sensor
from random import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from kneed import KneeLocator
# Safety substract
def savesub(a, b):
    return  a - b if (a - b > 0) else 0
# Safety add
def saveadd(a, b, max):
    return a + b if (a + b < max) else max

# Matplotlib draw devices, sensors and clusters
def draw_devices(Devices, centers, predictions, map_size):
    points1 = []
    points2 = []
    for device in Devices:
        pos1 = device.get_pos()
        #plt.plot(pos1[0], pos1[1], marker='o', markersize=7, color="red")
        pos2 = device.get_sensor().get_pos()
        #plt.plot(pos2[0], pos2[1], marker='x', markersize=7, color="blue")
        plt.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 'g-')
        plt.text(pos1[0] + 0.5, pos1[1]+0.5, "Device", fontsize=5)
        plt.text(pos2[0] + 0.5, pos2[1]+0.5, "Sensor", fontsize=5)
        points1.append(pos1)
        points2.append(pos2)
    points1_np = np.array(points1)
    points2_np = np.array(points2)
    plt.scatter(points1_np[:, 0], points1_np[:, 1], c=predictions, s=len(points1), cmap='cividis')
    plt.scatter(points2_np[:, 0], points2_np[:, 1], c=predictions, s=len(points2), cmap='cool')
    code = ord('A')
    for center in centers:
        plt.scatter(center[0], center[1],  c='b', s=200, alpha=0.6)
        plt.text(center[0] - 5, center[1] - 5, chr(code) , fontsize=10)
        code+=1
    #plt.scatter(centers[:, 0], centers[:, 1], c='b', s=200, alpha=0.6)
    plt.show()


map_size = (500, 500)
devices_amount = 20
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
predictions = kmeans.predict(points)
### DRAW DATA
draw_devices(Devices, centers, predictions, map_size)

