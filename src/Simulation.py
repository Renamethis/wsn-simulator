from threading import Thread

class Simulation():

    DEFAULT_TIME = 0.0001
    RESET_ITERS = 250

    def __init__(self, network):
        self._clusters = network.get_clusters()
        self._station = network.get_station()
        self._energy_trace = []
        self._nodes_trace = []
        self._running = False
    
    def simulate(self, max_iters, speed, **kwargs):
        for cluster in self._clusters:
            for dev in cluster.get_devices():
                dev.set_speed(speed)
        self._max_iters = max_iters
        self._running = True
        self.__thread = Thread(target=self._simulation_loop, kwargs=kwargs)
        self.__thread.start()

    def _simulation__loop(self, **args):
        pass

    def _reset(self):
        self._energy_trace.clear()
        self._nodes_trace.clear()
        
        for cluster in self._clusters:
            for d in cluster.get_devices():
                d.reset()

    def stop(self):
        self._running = False

    def isRunning(self):
        return self._running

    def is_alive(self):
        return self._get_total_energy() > 0.0

    def getTraces(self):
        return (self._energy_trace, self._nodes_trace)
                    
    def _get_total_energy(self):
        energy = 0.0
        for cluster in self._clusters:
            energy += cluster.get_cluster_energy()
        return energy

    def _get_alive_nodes(self):
        nodes = 0
        for cluster in self._clusters:
            for dev in cluster.get_devices():
                if(dev.alive()):
                    nodes += 1
        return nodes 