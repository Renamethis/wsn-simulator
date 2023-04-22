import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from src.GUI.Plotter import Plotter
from src.Network.Device import Device
from src.Processing.Clustering import Clustering
from src.Network.Network import DeviceNetwork
from src.Network.Cluster import DeviceCluster
from random import random

class Creator(tk.Toplevel):
    DEFAULT_PARAMETERS = [
        "2",
        "Device",
        "15"
    ]
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.protocol("WM_DELETE_WINDOW", self.__close)
        self.title("Create Network")
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill=tk.X, side=tk.LEFT, anchor=tk.N)
        label = tk.Label(menu_frame, text="Devices: ")
        label.pack(side=tk.TOP)
        self.__list_box = tk.Listbox(menu_frame, 
                                     height=10, width=33, selectmode="single")
        self.__list_box.pack(side=tk.TOP, anchor=tk.S)
        map_size_frame = tk.Frame(menu_frame)
        map_size_frame.pack(side=tk.TOP)
        desc_label = tk.Label(map_size_frame, text="Map Size: (")
        desc_label.pack(side=tk.LEFT)
        self.__x = tk.StringVar()
        self.__x.set("300")
        self.__y = tk.StringVar()
        self.__y.set("300")
        self.__x.trace("w", self.__update_parameters)
        self.__y.trace("w", self.__update_parameters)
        vcmd = (self.register(self.__validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        x_entry = tk.Entry(map_size_frame, textvariable=self.__x, width=4, validate='key', validatecommand=vcmd)
        x_entry.pack(side=tk.LEFT)
        sep_label = tk.Label(map_size_frame, text=";")
        sep_label.pack(side=tk.LEFT)
        y_entry = tk.Entry(map_size_frame, textvariable=self.__y, width=4, validate='key', validatecommand=vcmd)
        y_entry.pack(side=tk.LEFT)
        end_label = tk.Label(map_size_frame, text=")")
        end_label.pack(side=tk.LEFT)
        device_parameters = [
            "Initial Energy",
            "Device Type",
            "Coverage"
        ]
        self.__vars = []
        self.__parameters_frame = tk.Frame(menu_frame, pady=10)
        frame = tk.Frame(self.__parameters_frame)
        frame.pack(side=tk.TOP)
        positionLabel = tk.Label(frame, text="Position: (")
        positionLabel.pack(side=tk.LEFT)
        x_var = tk.StringVar()
        x_var.trace("w", self.__update_parameters)
        y_var = tk.StringVar()
        y_var.trace("w", self.__update_parameters)
        x_entry = tk.Entry(frame, textvariable=x_var, width=4 ,validate='key', validatecommand=vcmd)
        x_entry.pack(side=tk.LEFT)
        commaLabel = tk.Label(frame, text=":")
        commaLabel.pack(side=tk.LEFT)
        y_entry = tk.Entry(frame, textvariable=y_var, width=4, validate='key', validatecommand=vcmd)
        y_entry.pack(side=tk.LEFT)
        bracketLabel = tk.Label(frame, text=")")
        bracketLabel.pack(side=tk.LEFT)
        self.__vars.append([x_var, y_var])
        for parameter in device_parameters:
            frame = tk.Frame(self.__parameters_frame)
            frame.pack(side=tk.TOP)
            label = tk.Label(frame, text=parameter + ":")
            label.pack(side=tk.LEFT)
            var = tk.StringVar()
            if(parameter is device_parameters[1]):
                menu = tk.OptionMenu(frame, var, "Device", "Station")
                menu.pack(side=tk.RIGHT)
            else:
                entry = tk.Entry(frame, textvariable=var, width=4, validate='key', validatecommand=vcmd)
                entry.pack(side=tk.RIGHT)
            var.set(self.DEFAULT_PARAMETERS[device_parameters.index(parameter)])
            var.trace("w", self.__update_parameters)
            self.__vars.append(var)
        save_button = tk.Button(menu_frame, text="Save", command=self.__save)
        save_button.pack(side=tk.BOTTOM, pady=10)
        self.__plotter = Plotter(self)
        self.__plotter.get_tk_widget().pack(side=tk.TOP, anchor=tk.N, 
                                            fill=tk.BOTH, padx=10)
        self.__plotter.get_tk_widget().bind('<Button-1>', self.__add_node)
        self.__list_box.bind('<<ListboxSelect>>', self.__select_node)
        self.__devices = []
        self.__station = None
        self.__network = None
        self.__isSetting = False
        self.__current_index = 0
        self.__colors = []

    def __validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return True

    def __save(self):
        if(self.__network is not None and self.__station is not None):
            filename = askstring("File Name", "Enter file name to save topology.")
            self.__network.save("networks/" + filename + ".json")
            self.__close()
        elif(self.__station is None):
            messagebox.showerror("Error", "No base station in network topology.")
        else:
            messagebox.showerror("Error", "Network is empty!")
            
    def __update_parameters(self, *args):
        if(self.__list_box.curselection() and not self.__isSetting):
            position = [float(self.__vars[0][0].get()), float(self.__vars[0][1].get())]
            initial_energy = float(self.__vars[1].get())
            isstation = self.__vars[2].get() == "Station"
            coverage = float(self.__vars[3].get())
            if(isstation and self.__station != None):
                self.__vars[2].set("Device")
                # show alert
            elif(isstation):
                self.__station = self.__devices[self.__list_box.curselection()[0]]
                self.__station.set_station()
                self.__station.set_pos(position)
                self.__devices[self.__list_box.curselection()[0]]
            else:
                dev = self.__devices[self.__list_box.curselection()[0]]
                if(dev.is_station()):
                    self.__station = None
                dev.set_device()
                dev.go_active()
                dev.set_pos(position)
                dev.set_initial_energy(initial_energy)
                dev.set_coverage(coverage)
        if(self.__check_vars()):
            self.__draw_network()
        
        
   
    def __add_node(self, event):
        x, y = event.x, event.y
        x = x*int(self.__x.get())/(self.__plotter.get_tk_widget().winfo_width())
        y = y*int(self.__y.get())/(self.__plotter.get_tk_widget().winfo_height())
        y = (int(self.__y.get()) - y)
        dev = Device([x, y])
        self.__set_parameters(dev)
        self.__devices.append(dev)
        self.__list_box.insert(self.__current_index, "Device" + str(self.__current_index + 1))
        self.__list_box.selection_clear(0, tk.END)
        self.__list_box.select_set(self.__current_index)
        self.__draw_network()
        self.__parameters_frame.pack(side=tk.TOP)
        self.__current_index += 1

    def __del__(self):
        self.__close()    
        
    def __close(self):
        self.destroy()

    def __select_node(self, evt):
        widget = evt.widget
        if(widget.curselection()):
            self.__parameters_frame.pack(side=tk.TOP)
            index = widget.curselection()[0]
            self.__set_parameters(self.__devices[index])
            self.__selection = widget.curselection()
        else:
            self.__parameters_frame.pack_forget()

    def __draw_network(self):
        if(not self.__x.get() or not self.__y.get()):
            return
        devices = [dev for dev in self.__devices if not dev.is_station()]
        for dev in devices:
            dev.go_active()
        if(len(self.__devices) > 5):
            clustering = Clustering(devices)
            clusters = clustering.clustering()
            for i in range(len(clusters)):
                if(i < len(self.__colors)):
                    self.__colors.append((random(), random(), random()))
                clusters[i].set_color(self.__colors[i])
            self.__network = DeviceNetwork(clusters, self.__station, 
                                           (int(self.__x.get()), 
                                            int(self.__y.get())))
            self.__plotter.set_network(self.__network, "FCM")
        elif(len(self.__devices) > 0):
            if(not self.__colors):
                self.__colors.append((random(), random(), random()))
            self.__network = DeviceNetwork(
                    [
                        DeviceCluster(devices, 
                                      self.__devices[0],
                                      self.__devices[0].get_pos(),
                                      self.__colors[0]) 
                    ], 
                    self.__station, (int(self.__x.get()), int(self.__y.get())))
            self.__plotter.set_network(self.__network, "FCM")

    def __set_parameters(self, dev):
        self.__isSetting = True
        type = "Station" if dev.is_station() else "Device"
        parameters = [[dev.get_pos()[0], dev.get_pos()[1]], str(dev.get_initial_energy()), str(type), 
                      str(dev.get_coverage())]
        for i in range(len(parameters)):
            if(i == 0):
                self.__vars[i][0].set(parameters[i][0])
                self.__vars[i][1].set(parameters[i][1])
            else:
                self.__vars[i].set(parameters[i])
        self.__isSetting = False

    def __check_vars(self):
        for var in self.__vars:
            if(isinstance(var, list)):
                for v in var:
                    if(not v.get()):
                        return False
            else:
                if(not v.get()):
                    return False
        return True