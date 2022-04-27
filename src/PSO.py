
import pyswarms as ps
from src.Device import State, Constant
import sys
devices = None
def __fit(m, cluster):
    totalEnergy = 0.0
    totalInitEnergy = 0.0
    totaldistance = range_distance = 0.0
    devices = cluster.get_devices()
    head = cluster.get_head()
    for i in range(0, len(m)):
        if(m[i] == 0 and devices[i].get_energy() != 0.0 and devices[i].get_state() != State.SLEEP):
            totalEnergy+=devices[i].get_energy()
            range_distance += head.calculate_distance(devices[i])
        totaldistance += head.calculate_distance(devices[i])
        totalInitEnergy += devices[i].get_initial_energy()
    return 0.6*totalEnergy/(totalInitEnergy) + 0.4*(1 - range_distance/totaldistance)

def fitness(genes, cluster):
    n_particles = genes.shape[0]
    return [__fit(genes[i], cluster) for i in range(n_particles)]
class PSO:

    def __init__(self, clusters):
        self.__optimizers = []
        self.__options = {'c1': 0.5, 'c2': 0.5, 'w':0.1, 'p':2}
        for cluster in clusters:
            self.__options['k'] = len(cluster.get_devices())
            optimizer = ps.discrete.BinaryPSO(n_particles=len(
                                                cluster.get_devices()
                                              ), 
                                              dimensions=len(
                                                  cluster.get_devices()
                                              ), 
                                              options=self.__options)
            self.__optimizers.append(optimizer)
        
        self.__clusters = clusters

    def optimize(self):
        '''
        options = {
            'c1': 0.3, 'c2': 0.6, 'w':0.1, 
            'k':len(self.__clusters[i].get_devices()), 'p':2
        }
        optimizer = ps.discrete.BinaryPSO(n_particles=30, 
                                            dimensions=len(
                                                self.__clusters[i].get_devices()
                                            ), 
                                            options=options)
        '''
        for i in range(len(self.__clusters)):
            devices = self.__clusters[i].get_devices()
            _, result = self.__optimizers[i].optimize(fitness, iters=100, verbose=False, cluster=self.__clusters[i])
            for i in range(len(result)):
                if(result[i] == 0 and devices[i].get_state != State.HEAD):
                    devices[i].set_state(State.SLEEP)
                else:
                    devices[i].set_state(State.ACTIVE)

    def reset(self):
        for i in range(len(self.__clusters)):
            self.__optimizers[i].reset()