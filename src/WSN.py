from src.Device import Constants
from src.PSO import PSO
from threading import Thread
from time import sleep

DEFAULT_TIME = 0.0001

class WSN:

    def __init__(self, network, max_iters):
        self.__clusters = network.get_clusters()
        self.__station = network.get_station()
        self.__max_iters = max_iters
        self.__energy_trace = []
        self.__nodes_trace = []
        self.__running = False
    
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
                d.reset()
        pso = PSO(self.__clusters)
        for i in range(self.__max_iters):
            if(self.__get_total_energy() == 0.0 or not self.__running):
                break
            self.__set_cluster_heads()
            for cluster in self.__clusters:
                if(pso):
                    pso.optimize()
                else:
                   sleep(DEFAULT_TIME) 
                ### SEND DATA
                for d in cluster.get_devices():
                    if(d is not cluster.get_head() and d.alive()):
                        if(cluster.get_head().alive()):
                            d.send_data(Constants.MESSAGE_LENGTH,
                                        cluster.get_head())
                    elif(d is cluster.get_head() and d.alive()):
                        d.send_data(Constants.MESSAGE_LENGTH * \
                            (len(cluster.get_devices()) - 1), self.__station)
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