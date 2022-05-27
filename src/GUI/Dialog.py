import tkinter  as tk
from src.Processing.Generator import Generator
from src.GUI.Creator import Creator

class LabelEntry(tk.Frame):
    def __init__(self, root, label, textvariable, width):
        tk.Frame.__init__(self, root)
        self.__label = tk.Label(self, text=label)
        self.__label.pack(side=tk.LEFT)
        self.__entry = tk.Entry(self, textvariable=textvariable, width=width)
        self.__entry.pack(side=tk.RIGHT)

class Dialog(object):
    def __init__(self, parent, current_num):
        self.__root = parent
        top = self.__top = tk.Toplevel(parent)
        self.__current_num = current_num
        
        self.myLabel = tk.Label(top, text='Create or generate network?')
        self.myLabel.pack(ipady=10)
        
        self.__x = tk.IntVar(value=300)
        self.__x.trace("w", lambda name, index, mode, sv=self.__x: \
            self.__update_button(sv))
        self.__x_entry = LabelEntry(top, "Map Size X: ", 
                                    textvariable=self.__x, width=4)
        self.__x_entry.pack(side=tk.TOP)
        
        self.__y = tk.IntVar(value=300)
        self.__y.trace("w", lambda name, index, mode, sv=self.__y: \
            self.__update_button(sv))
        self.__y_entry = LabelEntry(top, "Map Size Y: ", 
                                    textvariable=self.__y, width=4)
        self.__y_entry.pack(side=tk.TOP)
        
        self.__bs_x = tk.IntVar(value=150)
        self.__bs_x.trace("w", lambda name, index, mode, sv=self.__bs_x: \
            self.__update_button(sv))
        self.__bs_x_entry = LabelEntry(top, "Base Station Position X: ", 
                                       textvariable=self.__bs_x, width=4)
        self.__bs_x_entry.pack(side=tk.TOP)
        
        self.__bs_y = tk.IntVar(value=150)
        self.__bs_y.trace("w", lambda name, index, mode, sv=self.__bs_y: \
            self.__update_button(sv))
        self.__bs_y_entry = LabelEntry(top, "Base Station Position Y: ", 
                                       textvariable=self.__bs_y, width=4)
        self.__bs_y_entry.pack(side=tk.TOP)
        
        self.__amount_devices = tk.IntVar(value=30)
        self.__amount_devices.trace("w", lambda name, index, mode, 
                                    sv=self.__amount_devices: \
                                        self.__update_button(sv))
        self.__amount_entry = LabelEntry(top, "Devices Amount: ", 
                                         textvariable=self.__amount_devices, 
                                         width=4)
        self.__amount_entry.pack(side=tk.TOP)
        
        self.__initial_energy = tk.DoubleVar(value=2.0)
        self.__initial_energy.trace("w", lambda name, index, mode, 
                                    sv=self.__initial_energy: \
                                        self.__update_button(sv))
        self.__initial_entry = LabelEntry(top, "Device Initial Energy: ", 
                                          textvariable=self.__initial_energy, 
                                          width=4)
        self.__initial_entry.pack(side=tk.TOP)
        
        self.__coverage = tk.DoubleVar(value=25.0)
        self.__coverage.trace("w", lambda name, index, mode, 
                              sv=self.__coverage: self.__update_button(sv))
        self.__coverage_entry = LabelEntry(top, "Device Coverage: ", 
                                           textvariable=self.__coverage, 
                                           width=4)
        self.__coverage_entry.pack(side=tk.TOP)
        
        self.__gen_button = tk.Button(top, text='Generate', 
                                      command=self.__generate)
        self.__gen_button.pack(side=tk.LEFT, ipady=5)
        self.__create_button = tk.Button(top, text='Create', 
                                         command=self.__create)
        self.__create_button.pack(side=tk.RIGHT, ipady=5)
        self.__update_array = [1, 1, 1, 1, 1, 1, 1]
        self.__network = None


    def top(self):
        return self.__top

    def __update_button(self, sv):
        try:
            if(sv is self.__x):
                if(sv.get() > 10 and sv.get() < 2000):
                    self.__update_array[0] = 1
                else:
                    self.__update_array[0] = 0
            elif(sv is self.__y):
                if(sv.get() > 10 and sv.get() < 2000):
                    self.__update_array[1] = 1
                else:
                    self.__update_array[1] = 0
            elif(sv is self.__bs_x):
                if(sv.get() > 0.0 and sv.get() < self.__x.get()):
                    self.__update_array[5] = 1
                else:
                    self.__update_array[5] = 0
            elif(sv is self.__bs_x):
                if(sv.get() > 0.0 and sv.get() < self.__x.get()):
                    self.__update_array[6] = 1
                else:
                    self.__update_array[6] = 0
            elif(sv is self.__amount_devices):
                if(sv.get() > 10 and sv.get() < 500):
                    self.__update_array[2] = 1
                else:
                    self.__update_array[2] = 0
            elif(sv is self.__initial_energy):
                if(sv.get() > 0.0 and sv.get() < 100):
                    self.__update_array[3]= 1
                else:
                    self.__update_array[3]= 0
            elif(sv is self.__coverage):
                if(sv.get() > 0.0 and sv.get() < 500):
                    self.__update_array[4]= 1
                else:
                    self.__update_array[4]= 0
            if(sum(self.__update_array) == 7):
                self.__gen_button["state"] = "normal"
            else:
                self.__gen_button["state"] = "disabled"
        except tk.TclError:
            return
            
    def __generate(self):
        generator = Generator((self.__x.get(), self.__y.get()), 
                               self.__amount_devices.get(), 
                               self.__initial_energy.get(), 
                               self.__coverage.get(), (self.__bs_x.get(), 
                                                       self.__bs_y.get()))
        generator.generate()
        self.__network = generator.clustering()
        self.__network.serialize('networks/net' + str(self.__current_num) + '.json')
        self.__root.load_networks()
        self.__top.destroy()

    def __create(self):
        self.__root.get_root().withdraw()
        self.__top.withdraw()
        creator = Creator(self.__top)
        self.__top.wait_window(creator)
        self.__root.get_root().deiconify()
        self.__top.deiconify()
        self.__top.destroy()
        self.__root.load_networks()

    def get_network(self):
        return self.__network
