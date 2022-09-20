from json import dump, load
from json.decoder import JSONDecodeError
from src.Network.Device import Device, State, Sensors
from src.Network.Cluster import DeviceCluster
from random import random

class DeviceNetwork:
    def __init__(self, clusters, station, map_size, color=None):
        self.__clusters = clusters
        self.__station = station
        self.__map_size = map_size
        if(color is None):
            self.__color = (random(), random(), random())

    def get_clusters(self):
        return self.__clusters

    def get_station(self):
        return self.__station
    
    def get_map_size(self):
        return self.__map_size

    def get_color(self):
        return self.__color

    def save(self, path):
        data = {}
        data['color'] = self.__color
        data['clusters'] = []
        for i in range(len(self.__clusters)):
            cluster = self.__clusters[i]
            data['map_size'] = self.__map_size
            data['clusters'].append({})
            data['clusters'][i]['centroid'] = cluster.get_centroid().tolist()
            data['clusters'][i]['color'] = cluster.get_color()
            data['clusters'][i]['head'] = {
                'pos': cluster.get_head().get_pos(),
                'initial_energy': cluster.get_head().get_initial_energy(),
                'coverage': cluster.get_head().get_coverage()
            }
            devices = [dev for dev in cluster.get_devices() if dev.get_state() != State.HEAD]
            data['clusters'][i]['devices'] = []
            for dev in devices:
                data['clusters'][i]['devices'].append({
                    'pos': dev.get_pos(),
                    'initial_energy': dev.get_initial_energy(),
                    'coverage' : dev.get_coverage()
                })
        data['station'] = {}
        data['station']['pos'] = self.__station.get_pos()
        with open(path, 'w') as f:
            dump(data, f)

    def load(self, path):
        with open(path, 'r') as f:
            try:
                data = load(f)
                clusters = []
                self.__color = data['color']
                for cluster in data['clusters']:
                    devices = [Device(dev['pos'], energy=dev['initial_energy'], coverage=dev['coverage']) for dev in cluster['devices']]
                    head = Device(cluster['head']['pos'], energy=cluster['head']['initial_energy'], coverage=cluster['head']['coverage'])
                    devices.append(head)
                    centroid = cluster['centroid']
                    color = cluster['color']
                    loaded_cluster = DeviceCluster(devices, head, centroid, color)
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