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
from algorithms import mutation_algorithms, read_in_algorithms, evaluation_algorithms, pairing_algorithms
import os

import threading


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.core = core.Core()
        #self.minsize(width=500, height=300)
        self.title("Genetic MarcMentat")

        #Backroundframe, der allen Platz des Fensters einnimmt und auf den alles gezeichnet wird
        backroundframe = tk.Frame(self)
        backroundframe.pack(fill=tk.BOTH, expand=True)
        backroundframe.columnconfigure(0, weight=1)
        backroundframe.rowconfigure(0, weight=1)

        #alle Frames, die auf dem Backroundframe liegen
        self.pages = {}
        self.pages["marcMentat"] = MarcMentatPage(backroundframe, self.core)
        self.pages["marcMentat"].grid(row=0, column=0, sticky="nsew")
        self.pages["startpage"] = Startpage(backroundframe, self.core)
        self.pages["startpage"].grid(row=0, column=0, sticky="nsew")

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
        settings.master = menu
        menu.add_cascade(menu=settings, label="Settings")

        self.show_frame("startpage")

    # def draw_shape(self, shape, comparison_shape=None, autoscale=True):
    #     #zeichnet das Polygon
    #     self.pages["startpage"].draw_shape(shape, comparison_shape, autoscale)
    
    # def draw_shape_merge(self, shape1,shape2, comparison_shape=None, autoscale=True):
    #     #zeichnet das Polygon
    #     self.pages["mergingpage"].draw_shapes(shape1,shape2, comparison_shape, autoscale)

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

    def _test(self):
        self.core.generate_first_generation()
        self.core.evaluate_shapes(self.core.generations[0])

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


class Startpage(tk.PanedWindow):

    def __init__(self, parent, core):
        super().__init__(parent, borderwidth=0, sashwidth=4, sashrelief='sunken')

        self.core = core

        #some help-widgets (not so important)
        leftpane = tk.PanedWindow(self, orient='vertical', borderwidth=0, sashwidth=4, sashrelief='sunken')
        self.add(leftpane)
        rightbox = tk.Frame(self)
        self.add(rightbox)
        scrollbox = tk.Frame(rightbox)
        scrollbox.pack(side='top', fill='both', expand=True)
        scrolly = tk.Scrollbar(scrollbox, orient='vertical')
        scrollx = tk.Scrollbar(scrollbox, orient='horizontal')
        scrolly.pack(side='right', fill='y')
        scrollx.pack(side='bottom', fill='x')
        scroll_canvas = tk.Canvas(scrollbox, yscrollcommand = scrolly.set, xscrollcommand = scrollx.set)
        scroll_canvas.pack(side='top', fill='both', expand=True)
        
        #the basic layout
        settings_box = tk.Frame(scroll_canvas)
        important_box = tk.Frame(rightbox)#box on the bottom right
        shape_box = tk.Frame(leftpane)
        plot_box = tk.Frame(leftpane)

        settings_box.pack(side='top', fill='both', expand=True)
        important_box.pack(side='bottom', fill='x')
        leftpane.add(shape_box)
        leftpane.add(plot_box)

        #important box
        mentat_button = ttk.Button(important_box, text='MarcMentat instances', command=lambda: parent.master.show_frame('marcMentat'))
        mentat_button.pack(side='right', padx=4, pady=4)
        self.start_optimization_button = ttk.Button(important_box, text='start optimaization', command=self.optimization_button_pressed)
        self.start_optimization_button.pack(side='left', padx=4, pady=4)

        #shape box
        f = matplotlib.figure.Figure()
        self.shape_plot = f.add_subplot(111)
        self.shape_plot.set_aspect('equal', adjustable='datalim')#scale of x- and y- axis equal
        #to hide numbers and ticks of the axes
        #self.shape_plot.xaxis.set_major_locator(matplotlib.pyplot.NullLocator())
        #self.shape_plot.yaxis.set_major_locator(matplotlib.pyplot.NullLocator())
        self.shape_canvas = FigureCanvasTkAgg(f, shape_box)
        self.shape_canvas.draw()
        toolbar = NavigationToolbar2Tk(self.shape_canvas, shape_box)
        toolbar.update()
        self.shape_canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        #plot box
        f = matplotlib.figure.Figure()
        self.graph_plot = f.add_subplot(111)
        self.plot_canvas = FigureCanvasTkAgg(f, plot_box)
        self.plot_canvas.draw()
        toolbar = NavigationToolbar2Tk(self.plot_canvas, plot_box)
        toolbar.update()
        self.plot_canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        #settings box
        container_mutation_algorithms = ToggledFrameContainer(settings_box, 'mutation algorithm')
        container_mutation_algorithms.pack(fill='x', pady=3)
        for algo in self.core.mutation_algorithms:
            ToggledFrameAlgorithm(container_mutation_algorithms.sub_frame, algo).pack(fill='x', pady=3)
        
        container_pairing_algorithms = ToggledFrameContainer(settings_box, 'pairing algorithm')
        container_pairing_algorithms.pack(fill='x', pady=3)
        for algo in self.core.pairing_algorithms:
            ToggledFrameAlgorithm(container_pairing_algorithms.sub_frame, algo).pack(fill='x', pady=3)

        container_read_in_algorithms = ToggledFrameContainer(settings_box, 'read in method')
        container_read_in_algorithms.pack(fill='x', pady=3)
        all_read_in_algorithms = list(core.all_read_in_algorithms.keys())
        read_in_list = ttk.Combobox(container_read_in_algorithms.sub_frame, values=all_read_in_algorithms, state='readonly')
        read_in_list.bind('<<ComboboxSelected>>', lambda _ : self.core.set_read_in_algorithm(read_in_list.get()))
        if len(core.all_read_in_algorithms) > 0:
            read_in_list.set(core.read_in_algorithm)
        read_in_list.pack()

        container_evaluation_algorithms = ToggledFrameContainer(settings_box, 'calculation of fittness value')
        container_evaluation_algorithms.pack(fill='x', pady=3)
        all_evaluation_algorithms = list(core.all_evaluation_algorithms.keys())
        evaluation_algo_list = ttk.Combobox(container_evaluation_algorithms.sub_frame, values=all_evaluation_algorithms, state='readonly')
        evaluation_algo_list.bind('<<ComboboxSelected>>', lambda _ : self.core.set_evaluation_algorithm(evaluation_algo_list.get()))
        if len(core.all_evaluation_algorithms) > 0:
            evaluation_algo_list.set(core.evaluation_algorithm)
        evaluation_algo_list.pack()

        #....
        container_tests = ToggledFrameContainer(settings_box, 'tests')
        container_tests.pack(fill='x', pady=3)
        test_shape = ttk.Button(container_tests.sub_frame, text='test', command=self.master.master._test)
        test_shape.pack()
#         self.mentat_commandlist = Mentat_commandlist(marcMentat_commands)
#         self.mentat_commandlist.pack(fill=tk.BOTH, expand=True)

    def update_progress(self):
        while self.core.optimization_running:
            time.sleep(1)
            self.show_improvement_history(self.core.improvement_history)
            self.draw_shape_foreground(self.core.find_best_shape)


    def optimization_button_pressed(self):
        #self.core.set_optimization_running(not self.core.get_optimization_running())
        if not self.core.get_optimization_running():
            thread1 = threading.Thread(target=self.core.start_optimization)
            thread2 = threading.Thread(target=lambda: self.listen_for_optimization_loop_terminating(thread1))
            thread1.start()
            thread2.start()

            # thread3 = threading.Thread(target=self.update_progress)
            # thread3.start()
            self.start_optimization_button.config(text='stop optimization')
        else:
            self.core.terminate_optimization()
            self.start_optimization_button.config(state='disabled', text='stopping optimization...')
            self.show_improvement_history(self.core.improvement_history)
            #self.start_optimization_button.config(text='start optimization')

    def listen_for_optimization_loop_terminating(self, loop_thread):
        loop_thread.join()
        self.start_optimization_button.config(text='start optimization', state='normal')


    def draw_shape_background(self,shp,markers=False,color='red'):
        self.shape_plot.plot(*shp.exterior.xy, color=color)
        if markers:
            self.shape_plot.scatter(*shp.exterior.xy,color=color)
        for interior in shp.interiors:
            self.shape_plot.plot(*interior.xy, color=color)
    def draw_shape_foreground(self,shp,fill_color='black'):
        self.shape_plot.fill(*shp.exterior.xy, color=fill_color, alpha=0.1)
        self.shape_plot.plot(*shp.exterior.xy, color='black')
        self.shape_plot.scatter(*shp.exterior.xy, color=self.restrictions_to_markercolors(shp))

        for interior in shp.interiors:
            self.shape_plot.fill(*interior.xy, color='white')
            self.shape_plot.plot(*interior.xy, marker = 'o', color='black')

    def restrictions_to_markercolors(self,shp):
        markercolors = []
        for restriction in shp.move_restrictions:
            if restriction:
                if type(restriction) is tuple:
                    markercolors.append('yellow')
                else:
                    markercolors.append('red')
            else:
                markercolors.append('black')
        markercolors.append(markercolors[0])
        return markercolors
    
    def show_improvement_history(self,improvement_history):
        inital_fittness = self.core.inital_shape.fittness
        generation_nums = [line[0] for line in improvement_history]
        fittness_means = [line[2] for line in improvement_history]
        fittness_min = [line[4]for line in improvement_history]
        fittness_max = [line[3]for line in improvement_history]
        self.graph_plot.clear()
        self.graph_plot.hlines(inital_fittness,0,len(self.core.generations)-1)
        self.graph_plot.plot(generation_nums,fittness_means)
        self.graph_plot.fill_between(generation_nums,fittness_min,fittness_max,color='blue',alpha=0.2)
        self.plot_canvas.draw()
        
    def draw_shape_comparison(self, shp, comparison_shape, autoscale):
        
        self.shape_plot.clear()
        self.shape_plot.autoscale(autoscale)#funktioniert noch nicht

        #um die Zahlen an den Achsen unsichtbar zu machen
##        self.plot.xaxis.set_major_locator(matplotlib.pyplot.NullLocator())
##        self.plot.yaxis.set_major_locator(matplotlib.pyplot.NullLocator())
        
        if comparison_shape:
            self.draw_shape_background(comparison_shape)
        
        self.draw_shape_foreground(shp)

        self.shape_canvas.draw()

    def draw_shape_pairing(self, shp1, shp2, merged_shape, autoscale):
        self.shape_plot.clear()
        self.shape_plot.autoscale(autoscale)
        if merged_shape is not None:
            self.draw_shape_background(merged_shape,markers=True)
        self.draw_shape_foreground(shp1,fill_color='yellow')
        self.draw_shape_foreground(shp2,fill_color='green')
        self.shape_canvas.draw()
  
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
        self.entry_host.bind('<Return>',lambda event: self.add_item())
        self.entry_host.grid(row=1)
        tk.Label(middlebox, text='Port').grid(row=0, column=1, sticky=tk.W)
        self.entry_port = tk.Entry(middlebox)
        self.entry_port.bind('<Return>',lambda event: self.add_item())
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

class ToggledFrameAlgorithm(tk.Frame):

    '''
    example usage:
    headline = ToggledFrameContainer(root,'headline')
    headline.pack(fill="x")

    subheadline1 = ToggledFrameContainer(headline.sub_frame,'subheadline 1')
    subheadline1.pack(fill="x")

    subheadline2 = ToggledFrameContainer(headline.sub_frame,'subheadline 2')
    subheadline2.pack(fill="x")

    algo = mutation_algorithms.AlgorithmOne()
    t = ToggledFrameAlgorithm(subheadline1.sub_frame,algo, borderwidth=1)
    t.pack(fill='both')

    algo2 = mutation_algorithms.AlgorithmOne()
    t2 = ToggledFrameAlgorithm(subheadline1.sub_frame,algo2, borderwidth=1)
    t2.pack(fill='both')
    '''

    def __init__(self, parent, algorithm, *args, **options):
        super().__init__(parent, *args, **options)

        self.algorithm = algorithm
        self.show = tk.BooleanVar()
        self.show.set(False)

        self.status = tk.BooleanVar()
        self.status.set(True)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='ᐅ', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.label = ttk.Label(self.title_frame, text = self.algorithm.get_name())
        self.label.pack(side='left')

        self.checkbox = ttk.Checkbutton(self.title_frame,command= self.cb, variable = self.status)
        self.checkbox.pack(side="right", expand=0)

        self.sub_frame = self.algorithm.get_settings_frame(self)

    def cb(self):
        self.algorithm.activated = self.status.get()

    def toggle(self):
        if self.show.get():
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='ᐁ')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='ᐅ')

class ToggledFrameContainer(tk.Frame):

    def __init__(self, parent, name, *args, **options):
        super().__init__(parent, *args, **options)

        self.show = tk.BooleanVar()
        self.show.set(False)

        self.title_frame = tk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='ᐅ', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.label = ttk.Label(self.title_frame, text = name)
        self.label.pack(side='left')

        self.sub_frame = tk.Frame(self)

    def toggle(self):
        if self.show.get():
            self.sub_frame.pack(fill="x", expand=1, padx=(15,0))
            self.toggle_button.configure(text='ᐁ')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='ᐅ')

if __name__=='__main__':
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    gui = GUI()
    gui.core.inital_shape=shape.csv_to_shape('wuerfel.csv')

    # gui.core.inital_shape = examples.get_realisticreate_example_polygonc_example()
    # gui.core.generate_first_generation()
    # gen = gui.core.generations[0]
    # gui.pages['startpage'].draw_shape_pairing(gen[0],gen[1],gui.core.pairing_algorithms[0].pair_shapes(gen[0],gen[1]),True)
    # merged_shape=shape.join_shapes(gui.core.generations[0][0],gui.core.generations[0][1])
    # # gui.pages['startpage'].draw_shape_comparison(gui.core.generations[0][0],gui.core.inital_shape,True)
    # gui.pages['startpage'].draw_shape_pairing(gui.core.generations[0][0],gui.core.generations[0][1],merged_shape,True)
    # for shp in gen:
    #gui.draw_shape(c.generations[0][0], comparison_shape=c.inital_shape, autoscale=True)
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