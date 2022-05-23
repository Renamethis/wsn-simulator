
from dijkstar import Graph, find_path

class MTE:
    def __init__(self, devices, station):
        self.__devices = devices
        self.__devices.append(station)
        
    def process(self, device):
        devices = self.__devices
        station_id = -1
        target_id = -1
        graph = Graph()
        for i in range(len(devices)):
            if(devices[i].is_station()):
                station_id = i
            if(devices[i] == device):
                target_id = i
            if(not devices[i].alive() or devices[i].is_sleep()):
                continue
            for j in range(len(devices)):
                if(i == j):
                    continue
                distance = devices[i].calculate_distance(devices[j])
                cost = distance**2 if distance < devices[i].get_coverage() else distance**4
                graph.add_edge(i, j, cost)
        if(target_id != -1 and station_id != -1):
            path = [devices[i] for i in find_path(graph, target_id, station_id).nodes]
            return path
        else:
            return None
            