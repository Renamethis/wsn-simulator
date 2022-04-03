import matplotlib.pyplot as plt 
import sys

class Plot:
    __colors = []
    def __init__(self, clusters):
        self.__clusters = clusters
        self.__axis = plt.subplot(1, 1, 1)
        self.__axis.figure.canvas.mpl_connect('key_press_event', self.on_press)
        plt.ion()

    # Matplotlib draw devices, sensors and clusters
    def draw_devices(self):
        plt.pause(0.000001)
        self.__axis.cla()
        for cluster in self.__clusters:
            for dev in cluster.get_devices():
                devpos = dev.get_pos()
                if(dev is cluster.get_head()):
                    self.__axis.plot(devpos[0], devpos[1], marker='o', 
                             linestyle='None', markersize=7, color=(1, 0, 0))
                    self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "CH", 
                                     fontsize=7)
                elif(not dev.alive()):
                    self.__axis.plot(devpos[0], devpos[1], marker='o', 
                             linestyle='None', markersize=7, color=(0, 0, 0))
                    self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Dead", 
                             fontsize=7)
                else:
                    self.__axis.plot(devpos[0], devpos[1], marker='o', 
                                     linestyle='None', markersize=7, 
                                     color=cluster.get_color())
                    self.__axis.text(devpos[0] + 0.5, devpos[1] + 0.5, "Device", 
                                     fontsize=7)
        self.__axis.figure.show()

    def draw_energy(self, energy):
        self.__axis.text(0, 0, str(energy), fontsize=15)

    def on_press(self, event):
        if event.key == 'q':
            sys.exit(0)