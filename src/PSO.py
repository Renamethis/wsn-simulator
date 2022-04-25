
import pyswarms as ps
from src.Device import State

class PSO:

    def __init__(self, clusters):
        self.__optimizers = []
        for cluster in clusters:
            options = {
                'c1': 0.3, 'c2': 0.6, 'w':0.4, 
                'k':len(cluster.get_devices()), 'p':2
            }
            optimizer = ps.discrete.BinaryPSO(n_particles=30, 
                                              dimensions=len(
                                                  cluster.get_devices()
                                              ), 
                                              options=options)
            self.__optimizers.append(optimizer)
        self.__clusters = clusters

    def optimize(self):
        for i in range(len(self.__optimizers)):
            self.__devices = self.__clusters[i].get_devices()
            _, result = self.__optimizers[i].optimize(self.__fitness, iters=100)
            for i in range(len(result)):
                if(result[i] == 0 and self.__devices[i].get_state != State.HEAD):
                    self.__devices[i].set_state(State.SLEEP)
                else:
                    self.__devices[i].set_state(State.ACTIVE)

    def __fit(self, m):
        total = 0.0
        for i in range(0, len(m)):
            if(m[i] == 0 and self.__devices[i].get_energy() != 0.0):
                total+=self.__devices[i].get_energy()
        return total/(2*len(m))

    def __fitness(self, genes):
        n_particles = genes.shape[0]
        return [self.__fit(genes[i]) for i in range(n_particles)]