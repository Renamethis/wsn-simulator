import tkinter  as tk
from src.SideMenu import SideMenu
from src.Plotter import Plotter

class MainWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.__close)
        self.title("WSN")
    
        self.__side_menu = SideMenu(self)
        self.__side_menu.pack(fill=tk.X, side=tk.LEFT, anchor=tk.N)
        
        top_frame = tk.Frame(self.__side_menu)
        top_frame.pack(side=tk.TOP)
        
        self.__routing = tk.StringVar()
        self.__routing.trace("w", self.__switch_routing)
        routings = ("Direct Communication", "MTE", "LEACH")
        self.__routing.set(routings[0])
        self.__routing_menu = tk.OptionMenu(top_frame, self.__routing, 
                                            *routings)
        self.__routing_menu.pack(side=tk.LEFT)
        
        self.__clear_button = tk.Button(top_frame, text="Clear",
                                        width=6, height=1, command=self.__clear)

        iters_frame = tk.Frame(self.__side_menu)
        iters_frame.pack(side=tk.TOP)
        
        label = tk.Label(iters_frame, text="MAX Iters: ")
        label.pack(side=tk.LEFT)
        
        self.__iters = tk.IntVar(value=20000)
        self.__iters_slider = tk.Scale(iters_frame, from_=100, to=200000, orient=tk.HORIZONTAL, length=130, variable=self.__iters)
        self.__iters_slider.pack(side=tk.LEFT, ipady=10)
        
        speed_frame = tk.Frame(self.__side_menu)
        speed_frame.pack(side=tk.TOP)
        
        label = tk.Label(speed_frame, text="Energy Consumption: ")
        label.pack(side=tk.LEFT)
        
        self.__speed = tk.IntVar(value=50)
        self.__speed_slider = tk.Scale(speed_frame, from_=1, to=100, orient=tk.HORIZONTAL, length=130, variable=self.__speed)
        self.__speed_slider.pack(side=tk.LEFT, ipady=10)
        
        buttons_frame = tk.Frame(self.__side_menu)
        self.__simulate_button = tk.Button(buttons_frame, text="Simulate",
                                           width=6, height=1)
        self.__plotter = Plotter(self, self.__simulate_button)
        self.__plotter.get_tk_widget().pack(side=tk.TOP, anchor=tk.N, 
                                            fill=tk.BOTH, padx=10)
        self.__check_flag = tk.BooleanVar()
        self.__check_flag.set(1)
        self.__check_button = tk.Checkbutton(self.__side_menu, 
                                             text="Sleep Scheduling",
                                             variable=self.__check_flag,
                                             onvalue=1, offvalue=0)
        self.__check_button.pack(side=tk.TOP)
        buttons_frame.pack(side=tk.TOP)
        self.__simulate_button.config(command=self.simulate)
        self.__simulate_button.pack(side=tk.LEFT)
        self.__simulate_button["state"] = "disabled"
        self.__stop_button = tk.Button(buttons_frame, text="Stop",
                                           width=4, height=1)
        self.__stop_button.config(command=self.stop)

    def set_plotter_network(self, network):
        self.__network = network
        self.__plotter.set_network(network, 
                                   self.__routing.get())
    def __del__(self):
        self.__close()
            
    def simulate(self):
        self.__clear_button.pack_forget()
        self.__stop_button.pack(side=tk.RIGHT)
        if(self.__routing.get() == "LEACH"):
            self.__plotter.simulate(self.__iters.get(), self.__speed.get(),
                                    isPSO=self.__check_flag.get())
        else:
            self.__plotter.simulate(self.__iters.get(), self.__speed.get(), 
                                    isPSO=self.__check_flag.get(), 
                                    isMTE=self.__routing.get() == "MTE")

    def stop(self):
        self.__clear_button.pack(side=tk.RIGHT)
        if(self.__plotter.isRunning()):
            self.__plotter.stop()
        self.__stop_button.pack_forget()

    def __switch_routing(self, *args):
        if(self.__side_menu.isSelected()):
            self.__plotter.set_network(self.__network, self.__routing.get())

    def __clear(self):
        self.__side_menu.unselect()
        self.__plotter.clear()

    def __close(self):
        if(self.__plotter.isRunning()):
            self.__plotter.quit()
        else:
            self.quit()