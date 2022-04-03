from src.Plotter import Plot
from src.Device import Constants

class WSN:

    def __init__(self, clusters, max_iters):
        self.__clusters = clusters
        self.__max_iters = max_iters
        self.__colors = []

    def simulate(self):
        plotter = Plot(self.__clusters)
        for i in range(self.__max_iters):
            ### CALCULATE CLUSTER HEADS

            ### SEND DATA
            for cluster in self.__clusters:
                for d in cluster.get_devices():
                    if(d is not cluster.get_head() and d.alive()):
                        if(cluster.get_head().alive()):
                            d.send_data(Constants.MESSAGE_LENGTH,
                                        cluster.get_head())
                    d.consume()
            plotter.draw_devices()
            plotter.draw_energy(self.__get_total_energy())
    
    def __get_total_energy(self):
        energy = 0.0
        for cluster in self.__clusters:
            energy += cluster.get_cluster_energy()
        return energy