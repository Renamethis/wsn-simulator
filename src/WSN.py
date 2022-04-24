from src.Device import Constants, State
import numpy as np
import pyswarms as ps
from threading import Thread

class WSN:

    def __init__(self, clusters, max_iters):
        self.__clusters = clusters
        self.__max_iters = max_iters
        self.__energy_trace = []
        self.__nodes_trace = []
    
    def simulate(self, pso):
        self.__running = True
        self.__thread = Thread(target=self.__simulation_loop, args=(pso,))
        self.__thread.start()
        
    def __simulation_loop(self, pso):
        self.__energy_trace.clear()
        self.__nodes_trace.clear()
        ### SET ENERGY
        for cluster in self.__clusters:
            for d in cluster.get_devices():
                d.set_energy(0.5)
                d.set_state(State.ACTIVE)
        for i in range(self.__max_iters):
            if(self.__get_total_energy() == 0.0 or not self.__running):
                break
            #self.__set_cluster_heads()
            for cluster in self.__clusters:
                if(pso):
                    self.__cur_devices = cluster.get_devices()
                    options = {'c1': 0.5, 'c2': 0.5, 'w':0.1, 'k':len(self.__cur_devices), 'p':2}
                    # Call instance of PSO
                    optimizer = ps.discrete.BinaryPSO(n_particles=30, dimensions=len(self.__cur_devices), options=options)
                    # Perform optimization
                    _, result = optimizer.optimize(self.__fitness, iters=100)
                    for i in range(len(result)):
                        if(result[i] == 0):
                            self.__cur_devices[i].set_state(State.SLEEP)
                        else:
                            self.__cur_devices[i].set_state(State.ACTIVE)
                ### SEND DATA
                for d in cluster.get_devices():
                    if(d is not cluster.get_head() and d.alive()):
                        if(cluster.get_head().alive()):
                            d.send_data(Constants.MESSAGE_LENGTH,
                                        cluster.get_head())
                    d.stay()
            self.__energy_trace.append(self.__get_total_energy())
            self.__nodes_trace.append(self.__get_alive_nodes())
        self.__running = False
        
    def stop(self):
        self.__running = False

    def isRunning(self):
        return self.__running

    def is_alive(self):
        return self.__get_total_energy() > 0.0

    def getTraces(self):
        return (self.__energy_trace, self.__nodes_trace)

    def __set_cluster_heads(self):
        for cluster in self.__clusters:
            energy = 0.0
            maxEnergyDevice = None
            for device in cluster.get_devices():
                if(device is not cluster.get_head() and device.get_energy() > energy):
                    energy = device.get_energy()
                    maxEnergyDevice = device
            if(maxEnergyDevice is not None):
                cluster.set_head(maxEnergyDevice)
                    
    def __get_total_energy(self):
        energy = 0.0
        for cluster in self.__clusters:
            energy += cluster.get_cluster_energy()
        return energy

    def __get_alive_nodes(self):
        nodes = 0
        for cluster in self.__clusters:
            for dev in cluster.get_devices():
                if(dev.alive()):
                    nodes += 1
        return nodes 

    def __fit(self, m):
        total = 0.0
        for i in range(0, len(m)):
            if(m[i] == 0 and self.__cur_devices[i].get_energy() != 0.0):
                total+=self.__cur_devices[i].get_energy()
        return total/(2*len(m))

    def __fitness(self, genes):
        n_particles = genes.shape[0]
        return np.array([self.__fit(genes[i]) for i in range(n_particles)])