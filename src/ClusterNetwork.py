from src.Device import Constants
from src.PSO import PSO
from time import sleep
from src.Simulation import Simulation
from src.LEACH import LEACH
from threading import Thread

class ClusterNetwork(Simulation):

    RESET_ITERS = 2000

    def _simulation_loop(self, pso):
        
        self._reset()
        
        optimizer = PSO(self._clusters)
        leach = LEACH(self._clusters)
        for i in range(self._max_iters):
            if(self._get_total_energy() == 0.0 or not self._running):
                break
            leach.process()
            if(pso):
                optimizer.optimize()
            else:
                sleep(self.DEFAULT_TIME)
            for j in range(len(self._clusters)):
                cluster = self._clusters[j]
                ### SEND DATA
                for d in cluster.get_devices():
                    if(d is not cluster.get_head() and d.alive()):
                        if(cluster.get_head().alive()):
                            d.send_data(cluster.get_head())
                    elif(d is cluster.get_head() and d.alive()):
                        d.send_data(self._station)
                    d.stay()
            self._energy_trace.append(self._get_total_energy())
            self._nodes_trace.append(self._get_alive_nodes())
            if((i + 1) % self.RESET_ITERS == 0):
                optimizer.reset()
        self._running = False
        
    def __set_cluster_heads(self):
        for cluster in self._clusters:
            energy = 0.0
            maxEnergyDevice = None
            for device in cluster.get_devices():
                if(device is not cluster.get_head() and device.get_energy() > energy):
                    energy = device.get_energy()
                    maxEnergyDevice = device
            if(maxEnergyDevice is not None):
                cluster.set_head(maxEnergyDevice)