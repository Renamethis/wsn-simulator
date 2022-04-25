import tkinter  as tk

class SideMenu(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(fill=tk.X, side=tk.TOP)
        
        self.__load_button = tk.Button(buttons_frame, text="Load", width=5, height=1)
        self.__load_button.pack(side=tk.LEFT, anchor=tk.W)
        
        self.__add_button = tk.Button(buttons_frame, text="+", width=1, height=1)
        self.__add_button.pack(side=tk.RIGHT, anchor=tk.E)
        
        self.__delete_button = tk.Button(buttons_frame, text="-", width=1, height=1)
        self.__delete_button.pack(side=tk.RIGHT, anchor=tk.E)
        
        self.__list_box = tk.Listbox(self, selectmode=tk.EXTENDED, height=15)
        self.__list_box.pack(side=tk.TOP, anchor=tk.S)

    def __add_network(self):
        pass
    def __delete_network(self):
        pass
    def __load_network(self):
        pass