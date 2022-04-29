from src.Simulation import Simulation
from time import sleep

class DirectCommunication(Simulation):

    def __init__(self, network, max_iters):
        Simulation.__init__(self, network, max_iters)
        self.___devices = sum([cluster.get_devices() for cluster in self._clusters], [])

    def _simulation_loop(self, pso=False):
        
        self._reset()
        
        for i in range(self._max_iters):
            if(self._get_total_energy() == 0.0 or not self._running):
                break
            for device in self.___devices:
                if(device.alive()):
                    device.send_data(self._station)
                self._station.send_data(device)
            self._energy_trace.append(self._get_total_energy())
            self._nodes_trace.append(self._get_alive_nodes())
    
            sleep(self.DEFAULT_TIME)
        self._running = False
            
        