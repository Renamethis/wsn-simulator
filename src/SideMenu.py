import tkinter  as tk
from tkinter import messagebox
from matplotlib.pyplot import text
from src.Device import DeviceNetwork
from src.Generator import Generator
import os

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
        
        self.__x = tk.IntVar()
        self.__x.trace("w", lambda name, index, mode, sv=self.__x: self.__update_button(sv))
        self.__x_entry = LabelEntry(top, "Map Size X: ", textvariable=self.__x, width=3)
        self.__x_entry.pack(side=tk.TOP)
        
        self.__y = tk.IntVar()
        self.__y.trace("w", lambda name, index, mode, sv=self.__y: self.__update_button(sv))
        self.__y_entry = LabelEntry(top, "Map Size Y: ", textvariable=self.__y, width=3)
        self.__y_entry.pack(side=tk.TOP)
        
        self.__amount_devices = tk.IntVar()
        self.__amount_devices.trace("w", lambda name, index, mode, sv=self.__amount_devices: self.__update_button(sv))
        self.__amount_entry = LabelEntry(top, "Devices Amount: ", textvariable=self.__amount_devices, width=3)
        self.__amount_entry.pack(side=tk.TOP)
        self.__gen_button = tk.Button(top, text='Generate', 
                                      command=self.__generate)
        self.__gen_button["state"] = "disabled"
        self.__gen_button.pack(side=tk.LEFT, ipady=5)
        self.__create_button = tk.Button(top, text='Create', 
                                         command=self.__create)
        self.__create_button.pack(side=tk.RIGHT, ipady=5)
        self.__update_array = [0, 0, 0]
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
            elif(sv is self.__amount_devices):
                if(sv.get() > 10 and sv.get() < 500):
                    self.__update_array[2] = 1
                else:
                    self.__update_array[2] = 0
            if(sum(self.__update_array) == 3):
                self.__gen_button["state"] = "normal"
        except tk.TclError:
            return
            
    def __generate(self):
        generator = Generator((self.__x.get(), self.__y.get()), self.__amount_devices.get())
        generator.generate()
        self.__network = generator.clustering()
        self.__network.serialize('networks/net' + str(self.__current_num) + '.json')
        self.__root.load_networks()
        self.__top.destroy()

    def __create(self):
        self.__top.destroy()

    def get_network(self):
        return self.__network

class SideMenu(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.__root = root
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(fill=tk.X, side=tk.TOP)
        
        self.__load_button = tk.Button(buttons_frame, text="Load", width=5, 
                                       height=1)
        self.__load_button.pack(side=tk.LEFT, anchor=tk.W)
        
        self.__add_button = tk.Button(buttons_frame, text="+", width=1, 
                                      height=1, command=self.__add_network)
        self.__add_button.pack(side=tk.RIGHT, anchor=tk.E)
        
        self.__delete_button = tk.Button(buttons_frame, text="-", width=1, 
                                         height=1, command=self.__delete_network)
        self.__delete_button.pack(side=tk.RIGHT, anchor=tk.E)
        
        self.__list_box = tk.Listbox(self, selectmode=tk.EXTENDED, height=10, width=23)
        self.__list_box.pack(side=tk.TOP, anchor=tk.S)
        self.__list_box.bind('<<ListboxSelect>>', self.__select_network)
        self.__network = None
        self.load_networks()

    def get_network(self):
        return self.__network

    def isSelected(self):
        if(self.__list_box.curselection()):
            return True
        return False

    def __add_network(self):
        dialog = Dialog(self, self.__current_num)
        self.wait_window(dialog.top())
        self.__network = dialog.get_network()

    def __delete_network(self):
        if(self.__network is not None):
            delete = messagebox.askquestion('Delete network','Are you sure you want to delete selected network?',icon = 'warning')
            if delete == "yes":
                os.remove("networks/" + self.__list_box.get(self.__list_box.curselection()[0]) + '.json')
                self.__network = None
                self.__root.set_plotter_network(None)
                self.__list_box.delete(self.__list_box.curselection())
        else:
            messagebox.showerror("Error", "Network not selected")
            
            
    def __load_network(self):
        pass

    def load_networks(self):
        self.__list_box.delete(0, tk.END)
        directory = os.fsencode("networks")
        item = 0
        self.__current_num = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".json"): 
                self.__list_box.insert(item, filename[:filename.find(".json")])
                item += 1
                num = [s for s in filename if s.isdigit()]
                num = int(''.join(num))
                if(num > self.__current_num):
                    self.__current_num = num
        self.__current_num += 1

    def __select_network(self, evt):
        widget = evt.widget
        if(widget.curselection()):
            name = widget.get(int(widget.curselection()[0])) + '.json'
            net = DeviceNetwork(None, None, None)
            if(net.deserialize('networks/' + name)):
                self.__network = net
                self.__root.set_plotter_network(self.__network)
            else:
                messagebox.showerror("Error", "Network is unreadable")
        