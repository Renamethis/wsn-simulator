from src.Routing.Routing import Routing
from src.Processing.MTE import MTE
from src.Processing.PSO import PSO
from time import sleep

class DirectCommunication(Routing):

    def __init__(self, network):
        Routing.__init__(self, network)
        for d in self._devices:
            d.go_active()

    def _simulation_loop(self, **kwargs):
        
        self._reset()
        mte = MTE(self._devices, self._station)
        pso = PSO(devices=self._devices, station=self._station)
        isMTE = kwargs['isMTE']
        isPSO = kwargs['isPSO']
        for i in range(self._max_iters):
            if(self._get_total_energy() == 0.0 or not self._running):
                break
            if(isPSO):
                if(i % self.RESET_ITERS == 0):
                    pso.reset()
                pso.optimize()
            for device in self._devices:
                if(device.alive() and device.is_active()):
                    if(isMTE):
                        path = mte.process(device)
                        for j in range(len(path) - 1):
                            path[j].send_data(path[j+1])
                    else:
                        device.send_data(self._station)
                        self._station.send_data(device)
                    device.stay()

            self._energy_trace.append(self._get_total_energy())
            self._nodes_trace.append(self._get_alive_nodes())
    
            sleep(self.DEFAULT_TIME)
        self._running = False
            
        