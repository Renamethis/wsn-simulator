from src.Device import Constants
from src.PSO import PSO
from time import sleep
from src.Simulation import Simulation
from src.LEACH import LEACH
class ClusterNetwork(Simulation):

    LEACH_ITERS = 1
    def _simulation_loop(self, **kwargs):
        
        self._reset()
        isPSO = kwargs['isPSO']
        optimizer = PSO(clusters=self._clusters)
        leach = LEACH(self._clusters, self._station)
        for i in range(self._max_iters):
            if(self._get_total_energy() == 0.0 or not self._running):
                break
            if(i%self.LEACH_ITERS == 0):
                leach.process()
            if(isPSO):
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
                        if(d.get_aggregation_size() > 0):
                            d.send_data(self._station)
                            d.aggregate()
                        self._station.send_data(d)
                    d.stay()
            self._energy_trace.append(self._get_total_energy())
            self._nodes_trace.append(self._get_alive_nodes())
            if((i + 1) % self.RESET_ITERS == 0):
                optimizer.reset()
        self._running = False