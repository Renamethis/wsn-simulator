
import pyswarms as ps
from copy import copy 

devices = None
def __fit_cluster(m, cluster):
    active_energy = total_energy = 0.0
    cluster_energy = cluster_init_energy = 0.0
    totaldistance = range_distance = 0.0
    devices = cluster.get_devices()
    for i in range(0, len(m)):
        if(m[i] == 0 and devices[i].alive() and devices[i].is_active()):
            active_energy += devices[i].get_energy()
            range_distance += devices[i].calculate_distance_pos(cluster.get_centroid())
        cluster_init_energy += devices[i].get_initial_energy()
        totaldistance += devices[i].calculate_distance_pos(cluster.get_centroid())
        total_energy += devices[i].get_energy()
    if(total_energy > 0.0):
        return 0.4*active_energy/(total_energy)+ 0.2*cluster_energy/cluster_init_energy + 0.4*(1 - range_distance/totaldistance)
    return 0

def __fit_dc(m, devices, station):
    active_energy = total_energy = 0.0
    range_distance = total_distance = 0.0
    for i in range(len(devices)):
        if(m[i] == 0 and devices[i].alive() and devices[i].is_active()):
            active_energy += devices[i].get_energy()
            range_distance += devices[i].calculate_distance(station)
        if(devices[i].alive()):
            total_energy += devices[i].get_energy()
            total_distance += devices[i].calculate_distance(station)
    if(total_energy > 0.0 and total_distance > 0.0):
        return 0.7*(active_energy/total_energy) + 0.3*(1 - range_distance/total_distance)
    return 0
                
def fitness(genes, **args):
    n_particles = genes.shape[0]
    try:
        return [__fit_cluster(genes[i], args['cluster']) for i in range(n_particles)]
    except KeyError:
        return [__fit_dc(genes[i], args['devices'], args['station']) for i in range(n_particles)]

class PSO:

    def __init__(self, **kwargs):
        self.__optimizers = []
        self.__optimizer = None
        self.__options = {'c1': 0.5, 'c2': 0.5, 'w':0.1, 'p':2}
        try:
            self.__devices = kwargs['devices']
            self.__station = kwargs['station']
            self.__options['k'] = len(self.__devices)
            self.__optimizer = ps.discrete.BinaryPSO(n_particles=4*len(
                                                    self.__devices
                                                ), 
                                                dimensions=len(
                                                    self.__devices
                                                ), 
                                                options=self.__options)
        except KeyError:
            for cluster in kwargs['clusters']:
                self.__options['k'] = len(cluster.get_devices())
                optimizer = ps.discrete.BinaryPSO(n_particles=4*len(
                                                    cluster.get_devices()
                                                ), 
                                                dimensions=len(
                                                    cluster.get_devices()
                                                ), 
                                                options=self.__options)
                self.__optimizers.append(optimizer)
        
            self.__clusters = kwargs['clusters']

    def optimize(self):
        if(self.__optimizer is None):
                for i in range(len(self.__clusters)):
                    devices = self.__clusters[i].get_devices()
                    if(len(devices) == 0):
                        continue
                    self.__options['k'] = len(devices)
                    optimizer = ps.discrete.BinaryPSO(n_particles=2*len(
                                                        devices
                                                    ), 
                                                    dimensions=len(
                                                        devices
                                                    ), 
                                                    options=self.__options)
                    _, result = optimizer.optimize(fitness, iters=300,
                                                            verbose=False, 
                                                            cluster=self.__clusters[i])
                    for i in range(len(result)):
                        if(result[i] == 0 and not devices[i].is_head()):
                            devices[i].go_sleep()
                        elif(result[i] == 1 and not devices[i].is_head()):
                            devices[i].go_active()
        else:
            _, result = self.__optimizer.optimize(fitness, iters=500,
                                                        verbose=False, 
                                                        devices=self.__devices,
                                                        station=self.__station)
            for i in range(len(result)):
                    if(result[i] == 0):
                        self.__devices[i].go_sleep()
                    else:
                        self.__devices[i].go_active()

    def reset(self):
        if(self.__optimizer is None):
            for i in range(len(self.__clusters)):
                self.__optimizers[i].reset()
        else:
            self.__optimizer.reset()