from ast import Constant
from enum import Enum, auto
from math import sqrt, log
from random import random
from json import dump, load
from json.decoder import JSONDecodeError
# Defined constants
class Constants(float, Enum):
    # energy dissipated at the transceiver electronic
    ENERGY = 50e-10
    # energy dissipated at the power amplifier (multi-path)
    E_MP = 0.0013e-13
    # energy dissipated at the power amplifier (line-of-sight)
    E_FS = 10e-13
    # energy dissipated at the data aggregation
    E_DA = 5e-10
    # energy dissipated at other electronics
    E_ED = 50e-6
    # default message length
    MESSAGE_LENGTH = 2000
    # threshold distance value
    THRESHOLD_DIST = sqrt(E_FS/E_MP)

# Sensor types
class Sensors(Enum):
    DEFAULT = auto()
    STATION = auto()

# Device state
class State(Enum):
    HEAD = auto()
    ACTIVE = auto()
    SLEEP = auto()
    DEAD = auto()

# WSN node class
class Device:

    def __init__(self, pos, energy=2, sensor_type=Sensors.DEFAULT):
        self.__pos = pos
        self.__initial_energy = self.__energy = energy
        self.__sensor_type = sensor_type
        self.__state = State.ACTIVE

    ## SETTERS

    def set_energy(self, energy):
        self.__energy = energy

    def set_state(self, state):
        self.__state = state

    ## GETTERS 

    def get_state(self):
        return self.__state

    def get_pos(self):
        return self.__pos

    def get_energy(self):
        return self.__energy

    def get_initial_energy(self):
        return self.__initial_energy

    # Check if device alive
    def alive(self):
        return self.__energy > 0.0

    # Calculate and sub transmitter energy consumption
    def send_data(self, length, receiver):
        if(self.__state == State.SLEEP):
            return
        distance = self.calculate_distance(receiver)
        # Transmitter energy model 
        energy = Constants.ENERGY
        if(distance > Constants.THRESHOLD_DIST):
            energy += Constants.E_MP*(distance**4)
        else:
            energy += Constants.E_FS*(distance**2)
        energy *= length
        self.consume(energy)
        receiver.receive(length)
        receiver.aggregate(length)

    # Energy spent on receive message
    def receive(self, length):
        self.consume(Constants.ENERGY * length)

    # Energy spent on aggregate message
    def aggregate(self, length):
        self.consume(Constants.E_DA * log(length))

    # Energy spent on other electronics
    def stay(self):
        self.consume(Constants.E_ED)

    # Consume energy function
    def consume(self, energy):
        if(self.__sensor_type != Sensors.STATION):
            if(energy > self.__energy):
                self.__energy = 0
            else:
                self.__energy -= energy

    # Reset energy device and state
    def reset(self):
        self.__energy = self.__initial_energy
        if(self.__state == State.HEAD):
            return
        self.__state = State.ACTIVE

    # Calculate distance between two nodes
    def calculate_distance(self, node):
        return sqrt((self.get_pos()[0] - node.get_pos()[0])**2 + (self.get_pos()[1] - 
            node.get_pos()[1])**2)

    def calculate_distance_pos(self, pos):
        return sqrt((pos[0] - pos[0])**2 + (pos[1] - 
            pos[1])**2)

class DeviceCluster:

    def __init__(self, devices, head, centroid):
        self.__devices = devices
        self.__cluster_head = head
        self.__cluster_head.set_state(State.HEAD)
        self.__color = (random(), random(), random())
        self.__centroid = centroid
    
    # SETTERS

    def set_head(self, head):
        self.__cluster_head.set_state(State.ACTIVE)
        self.__cluster_head = head
        self.__cluster_head.set_state(State.HEAD)

    # GETTERS

    def get_centroid(self):
        return self.__centroid

    def get_devices(self):
        return self.__devices

    def get_head(self):
        return self.__cluster_head

    def get_color(self):
        return self.__color

    # Return remaining energy in whole cluster
    def get_cluster_energy(self):
        energy = 0
        for dev in self.__devices:
            if(dev.alive()):
                energy += dev.get_energy()
        return energy

    # Return initial energy of whole cluster
    def get_cluster_initial_energy(self):
        energy = 0
        for dev in self.__devices:
            if(dev.alive()):
                energy += dev.get_initial_energy()
        return energy

class DeviceNetwork:
    def __init__(self, clusters, station, map_size):
        self.__clusters = clusters
        self.__station = station
        self.__map_size = map_size

    def get_clusters(self):
        return self.__clusters

    def get_station(self):
        return self.__station
    
    def get_map_size(self):
        return self.__map_size

    def serialize(self, path):
        data = {}
        data['clusters'] = []
        for i in range(len(self.__clusters)):
            cluster = self.__clusters[i]
            data['map_size'] = self.__map_size
            data['clusters'].append({})
            data['clusters'][i]['centroid'] = cluster.get_centroid().tolist()
            data['clusters'][i]['head'] = {
                'pos': cluster.get_head().get_pos(),
                'initial_energy': cluster.get_head().get_initial_energy()
            }
            devices = [dev for dev in cluster.get_devices() if dev.get_state() != State.HEAD]
            data['clusters'][i]['devices'] = []
            for dev in devices:
                data['clusters'][i]['devices'].append({
                    'pos': dev.get_pos(),
                    'initial_energy': dev.get_initial_energy()
                })
        data['station'] = {}
        data['station']['pos'] = self.__station.get_pos()
        with open(path, 'w') as f:
            dump(data, f)

    def deserialize(self, path):
        with open(path, 'r') as f:
            try:
                data = load(f)
                clusters = []
                for cluster in data['clusters']:
                    devices = [Device(dev['pos'], energy=dev['initial_energy']) for dev in cluster['devices']]
                    head = Device(cluster['head']['pos'], energy=cluster['head']['initial_energy'])
                    devices.append(head)
                    centroid = cluster['centroid']
                    loaded_cluster = DeviceCluster(devices, head, centroid)
                    clusters.append(loaded_cluster)
                self.__clusters = clusters
                self.__station = Device(data['station']['pos'], 
                                        sensor_type=Sensors.STATION)
                self.__map_size = data['map_size']
                return True
            except JSONDecodeError:
                return False
            except KeyError:
                return False
            
    
    