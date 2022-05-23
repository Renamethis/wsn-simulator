import tkinter  as tk
from tkinter import messagebox
from matplotlib.pyplot import text
from src.Network.Network import DeviceNetwork
from src.GUI.Dialog import Dialog
import os

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
        
        self.__list_box = tk.Listbox(self, selectmode=tk.EXTENDED, height=10, width=33)
        self.__list_box.pack(side=tk.TOP, anchor=tk.S)
        self.__list_box.bind('<<ListboxSelect>>', self.__select_network)
        self.__network = None
        self.load_networks()

    def get_network(self):
        return self.__network

    def unselect(self):
        self.__list_box.selection_clear(0, tk.END)

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

    def get_root(self):
        return self.__root

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
        