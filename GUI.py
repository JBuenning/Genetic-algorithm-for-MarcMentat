import tkinter as tk
from tkinter import ttk
import matplotlib
import core
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import shape
import examples
import time
from mentat_connection import HEADERSIZE, Task, Test_connection
import socket
import pickle
from algorithms import mutation_algorithms


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.core = core.Core()
        #self.minsize(width=500, height=300)
        self.title("Genetic MarcMentat")

        #Backroundframe, der allen Platz des Fensters einnimmt und auf den alles gezeichnet wird
        backroundframe = tk.Frame(self)
        backroundframe.pack(fill=tk.BOTH, expand=True)
        backroundframe.grid_rowconfigure(0, weight=1)
        backroundframe.grid_columnconfigure(0, weight=1)

        #alle Frames, die auf dem Backroundframe liegen
        self.pages = {}
        self.pages["marcMentat"] = MarcMentatPage(backroundframe, self.core)
        self.pages["marcMentat"].grid(row=0, column=0, sticky="nsew")
        self.pages["startpage"] = Startpage(backroundframe)
        self.pages["startpage"].grid(row=0, column=0, sticky="nsew")
        self.pages["mergingpage"] = Mergingpage(backroundframe)
        self.pages["mergingpage"].grid(row=0, column=0, sticky="nsew")

        #menubar
        menu = tk.Menu(self)
        self.config(menu=menu)

        #file-dropdown
        file_dropdown = tk.Menu()
        file_dropdown.add_command(label="Open", command=self.open_file)
        file_dropdown.add_command(label="Save as", command=self.save_as)
        file_dropdown.master = menu
        menu.add_cascade(menu=file_dropdown, label="File")

        #settings
        settings = tk.Menu()
        settings.add_command(label="marcMentat", command=lambda: self.show_frame("marcMentat"))
        settings.add_command(label="mergingpage", command=lambda: self.show_frame("mergingpage"))
        settings.master = menu
        menu.add_cascade(menu=settings, label="Settings")

        self.show_frame("startpage")

    def draw_shape(self, shape, comparison_shape=None, autoscale=True):
        #zeichnet das Polygon
        self.pages["startpage"].draw_shape(shape, comparison_shape, autoscale)
    
    def draw_shape_merge(self, shape1,shape2, comparison_shape=None, autoscale=True):
        #zeichnet das Polygon
        self.pages["mergingpage"].draw_shapes(shape1,shape2, comparison_shape, autoscale)

    def get_mentat_connections(self):
        return self.pages['marcMentat'].get_connections()

    def show_frame(self, name):
        #wechselt zwischen den Frames, die den ganzen Platz im Fenster einnehmen
        self.pages[name].tkraise()

    def open_file(self):
        filename = tk.filedialog.askopenfilename(filetypes=(("All Files", "*.*"), ("Shape", "*.shape")))#nur ein Beispiel
        if len(filename) != 0:
            print(filename)

    def save_as(self):
        print("save as")

    def test_exampleshape(self):
        for connection in self.get_mentat_connections():
            HOST = connection[0]
            PORT = connection[1]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                try:
                    s.connect((HOST, PORT))
                    example_shape = examples.get_cool_example()
                    obj_send = Task(list(example_shape.exterior.coords[:-1]), '','')#2. und 3. Argument muss natürlich noch gefüllt werden
                    obj_bytes = pickle.dumps(obj_send)

                    if len(str(len(obj_bytes)))>HEADERSIZE:
                        raise Exception('Length of the object to send exceeds header size')
                    
                    header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
                    s.sendall(header + obj_bytes)

                    obj_recv = bytearray()
                    data = s.recv(64)
                    obj_length = int(data[:HEADERSIZE].decode('utf-8'))
                    obj_recv.extend(data[HEADERSIZE:])
                    while len(obj_recv) < obj_length:
                        data = s.recv(64)
                        obj_recv.extend(data)

                    obj_recv = pickle.loads(obj_recv)
                    print(obj_recv)#obj_recv ist später der Wert, der von Mentat berechnet wurde
                except socket.error as e:
                    print('exception!!!')


class Startpage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        topbox = tk.Frame(self)
        topbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        f = matplotlib.figure.Figure()
        self.plot = f.add_subplot(111)
        self.plot.set_aspect('equal', adjustable='datalim')#x- und y- achse gleich skaliert
        
        #um die Zahlen an den Achsen unsichtbar zu machen
##        self.plot.xaxis.set_major_locator(matplotlib.pyplot.NullLocator())
##        self.plot.yaxis.set_major_locator(matplotlib.pyplot.NullLocator())
        
        self.canvas = FigureCanvasTkAgg(f, topbox)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, topbox)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        rightbox = tk.Frame(self, bg='red')
        rightbox.pack(side=tk.RIGHT, fill=tk.Y)

        frame_random_shape_settings = ttk.Labelframe(rightbox, text='irgendwelche Settings')
        frame_random_shape_settings.pack(fill=tk.BOTH, expand=True)
        marcMentat_commands = ttk.Labelframe(rightbox, text='MarcMentat commands')
        marcMentat_commands.pack(fill=tk.BOTH, expand=True)
        right_label = tk.Label(frame_random_shape_settings, text='\nwelcher Algorithmus,\nwie oft,\nvielleicht auch\nAnzahl formen pro Generation usw')
        right_label.pack()
        test_shape = ttk.Button(frame_random_shape_settings, text='Beispielshape einlesen', command=self.master.master.test_exampleshape)
        test_shape.pack()
        self.mentat_commandlist = Mentat_commandlist(marcMentat_commands)
        self.mentat_commandlist.pack(fill=tk.BOTH, expand=True)

    def draw_shape(self, shape, comparison_shape, autoscale):
        
        self.plot.clear()
        self.plot.autoscale(autoscale)#funktioniert noch nicht

        #um die Zahlen an den Achsen unsichtbar zu machen
##        self.plot.xaxis.set_major_locator(matplotlib.pyplot.NullLocator())
##        self.plot.yaxis.set_major_locator(matplotlib.pyplot.NullLocator())
        
        if comparison_shape is not None:
            self.plot.plot(*comparison_shape.exterior.xy, color='red')

            interiors = comparison_shape.interiors
            for interior in interiors:
                self.plot.plot(*interior.xy, color='red')

        markercolors = []
        for restriction in shape.move_restrictions:
            if restriction:
                if type(restriction) is tuple:
                    markercolors.append('yellow')
                else:
                    markercolors.append('red')
            else:
                markercolors.append('black')
        markercolors.append(markercolors[0])
        
        self.plot.fill(*shape.exterior.xy, color='black', alpha=0.1)
        self.plot.plot(*shape.exterior.xy, color='black')
        self.plot.scatter(*shape.exterior.xy, color=markercolors)

        interiors = shape.interiors
        for interior in interiors:
            self.plot.fill(*interior.xy, color='white')
            self.plot.plot(*interior.xy, marker = 'o', color='black')

        self.canvas.draw()

class Mergingpage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        topbox = tk.Frame(self)
        topbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        f = matplotlib.figure.Figure()
        self.plot = f.add_subplot(111)
        self.plot.set_aspect('equal', adjustable='datalim')#x- und y- achse gleich skaliert
        
        #um die Zahlen an den Achsen unsichtbar zu machen
##        self.plot.xaxis.set_major_locator(matplotlib.pyplot.NullLocator())
##        self.plot.yaxis.set_major_locator(matplotlib.pyplot.NullLocator())
        
        self.canvas = FigureCanvasTkAgg(f, topbox)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, topbox)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        rightbox = tk.Frame(self, bg='red')
        right_label = tk.Label(rightbox, text='Platz für Knöpfe usw\nnatürlich nur ein\nvorläufiges Layout')
        right_label.pack()
        rightbox.pack(side=tk.RIGHT, fill=tk.Y)

    def draw_shapes(self, shape1, shape2, merged_shape, autoscale):
        
        self.plot.clear()
        self.plot.autoscale(autoscale)#funktioniert noch nicht

        #um die Zahlen an den Achsen unsichtbar zu machen
##        self.plot.xaxis.set_major_locator(matplotlib.pyplot.NullLocator())
##        self.plot.yaxis.set_major_locator(matplotlib.pyplot.NullLocator())
        ### Merged_shape
        if merged_shape is not None:
            self.plot.plot(*merged_shape.exterior.xy, color='red')
            self.plot.scatter(*merged_shape.exterior.xy, color='red')
            interiors = merged_shape.interiors
            for interior in interiors:
                self.plot.plot(*interior.xy, color='red')

        ### Shape 1 and 2
        for shape in [shape1,shape2]:
            markercolors = []
            for restriction in shape.move_restrictions:
                if restriction:
                    if type(restriction) is tuple:
                        markercolors.append('yellow')
                    else:
                        markercolors.append('red')
                else:
                    markercolors.append('black')
            markercolors.append(markercolors[0])
            
            self.plot.fill(*shape.exterior.xy, color='black', alpha=0.1)
            self.plot.plot(*shape.exterior.xy, color='black')
            self.plot.scatter(*shape.exterior.xy, color=markercolors)

            interiors = shape.interiors
            for interior in interiors:
                self.plot.fill(*interior.xy, color='white')
                self.plot.plot(*interior.xy, marker = 'o', color='black')
        self.canvas.draw()        

class MarcMentatPage(tk.Frame):

    def __init__(self, parent, core):
        super().__init__(parent)
        self.core = core

        self.listbox = tk.Listbox(self)
        #label = tk.Label(topbox, text="hier kann man später die Marcs verbinden")
        #label.pack()
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #topbox.grid_rowconfigure(0, weight=1)
        #topbox.grid_columnconfigure(0, weight=1)

        bottombox = tk.Frame(self)
        close = ttk.Button(bottombox, text="close", command=lambda: self.master.master.show_frame("startpage"))
        close.pack(side=tk.RIGHT, pady=4, padx=4)
        test_all = ttk.Button(bottombox, text='test all', command=self.test_all)
        test_all.pack(side=tk.LEFT, pady=4, padx=4)
        bottombox.pack(side=tk.BOTTOM, fill=tk.X)

        middlebox = tk.Frame(self)
        middlebox.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(middlebox, text='Host').grid(row=0, sticky=tk.W)
        self.entry_host = tk.Entry(middlebox)
        self.entry_host.grid(row=1)
        tk.Label(middlebox, text='Port').grid(row=0, column=1, sticky=tk.W)
        self.entry_port = tk.Entry(middlebox)
        self.entry_port.grid(row=1, column=1)
        add_item = ttk.Button(middlebox, text='add connection', command=self.add_item)
        add_item.grid(row=1, column=2, padx=4)

    def add_item(self):
        host = self.entry_host.get()
        port = self.entry_port.get()
        if host:
            try:
                int(port)
                self.listbox.insert(tk.END, 'HOST "{}", PORT {}'.format(host, port))
                self.core.mentat_connections.append((host,int(port)))
                #self.entry_host.delete(0,'end')
                self.entry_port.delete(0,'end')
            except:
                pass

    def test_all(self):
        i = 0
        while i < len(self.core.mentat_connections):
            HOST = self.core.mentat_connections[i][0]
            PORT = self.core.mentat_connections[i][1]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                try:
                    s.connect((HOST, PORT))
                    test_obj = 'Hello World!'
                    obj_send = Test_connection(test_obj)
                    obj_bytes = pickle.dumps(obj_send)

                    if len(str(len(obj_bytes)))>HEADERSIZE:
                        raise Exception('Length of the object to send exceeds header size')
                    
                    header = bytes('{message:<{width}}'.format(message=len(obj_bytes), width=HEADERSIZE), encoding='utf-8')
                    s.sendall(header + obj_bytes)

                    obj_recv = bytearray()
                    data = s.recv(64)
                    obj_length = int(data[:HEADERSIZE].decode('utf-8'))
                    obj_recv.extend(data[HEADERSIZE:])
                    while len(obj_recv) < obj_length:
                        data = s.recv(64)
                        obj_recv.extend(data)

                    obj_recv = pickle.loads(obj_recv)
                    if test_obj==obj_recv:
                        i += 1
                    else:
                        self.remove_connection(i)
                except socket.error as e:
                    self.remove_connection(i)

    def remove_connection(self, index):
        self.core.mentat_connections.pop(index)
        self.listbox.delete(index)

    #def get_connections(self):
        #return self.connections.copy()

class Mentat_commandlist(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        topbox = tk.Frame(self)
        topbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scroll_y = tk.Scrollbar(topbox, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(topbox, orient=tk.HORIZONTAL)
        self.listbox = tk.Listbox(topbox, selectmode=tk.SINGLE, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.listbox.yview)
        scroll_x.config(command=self.listbox.xview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Button-1>', self.setCurrent)
        self.listbox.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None
        self.listbox.insert(tk.END, '*af_planar_trimesh')
        self.listbox.insert(tk.END, '*new_geometry *geometry_type mech_planar_pstress')

        bottombox = tk.Frame(self)
        bottombox.pack(side=tk.BOTTOM, fill=tk.X)
        delete = ttk.Button(bottombox, text="delete", command=self.delete)
        delete.pack(side=tk.LEFT, pady=4, padx=4)
        add_item = ttk.Button(bottombox, text="add command", command=self.add_item)
        add_item.pack(side=tk.LEFT, pady=4, padx=0)
        self.entry = tk.Entry(bottombox)
        self.entry.pack(side=tk.LEFT, pady=4, padx=0)
        
    def delete(self):
        item = self.listbox.curselection()
        if item:
            self.listbox.delete(item)

    def get_all_items(self):
        all_items = self.listbox.get(0,'end')
        return all_items

    def add_item(self):
        entry = self.entry.get()
        if entry:
            self.listbox.insert(tk.END, entry)
            self.entry.delete(0,'end')
            
    def setCurrent(self, event):
        self.curIndex = self.listbox.nearest(event.y)

    def shiftSelection(self, event):
        i = self.listbox.nearest(event.y)
        if i < self.curIndex:
            x = self.listbox.get(i)
            self.listbox.delete(i)
            self.listbox.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.listbox.get(i)
            self.listbox.delete(i)
            self.listbox.insert(i-1, x)
            self.curIndex = i
gui = GUI()
# c = core.Core()
# c.inital_shape = examples.get_realisticreate_example_polygonc_example()
# c.generate_first_generation()
# gen = c.generations[0]
# for shp in gen:
#     gui.draw_shape(shp, comparison_shape=c.inital_shape, autoscale=True)
#     time.sleep(0)
# gui.draw_shape(example, comparison_shape=example, autoscale=True)
# example2 = examples.get_cool_example()
# mutation_algorithm = mutation_algorithms.AlgorithmOne()
# for i in range(1000):
#     gui.draw_shape(example2, comparison_shape=example, autoscale=True)
#     example2 = mutation_algorithm.change_shape(example2)
#     time.sleep(0)
#print(shape.join_shapes(examples.merge_example_1(),examples.merge_example_2()).exterior.coords)
#gui.draw_shape_merge(examples.merge_example_1(),examples.merge_example_2(),shape.join_shapes(examples.merge_example_1(),examples.merge_example_2()))
gui.mainloop()