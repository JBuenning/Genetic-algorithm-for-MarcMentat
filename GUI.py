import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import shape
import time

class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        #self.minsize(width=500, height=300)
        self.title("Genetic MarcMentat")

        #Backroundframe, der allen Platz des Fensters einnimmt und auf den alles gezeichnet wird
        backroundframe = tk.Frame(self)
        backroundframe.pack(fill=tk.BOTH, expand=True)
        backroundframe.grid_rowconfigure(0, weight=1)
        backroundframe.grid_columnconfigure(0, weight=1)

        #alle Frames, die auf dem Backroundframe liegen
        self.pages = {}
        self.pages["marcMentat"] = MarcMentatPage(backroundframe)
        self.pages["marcMentat"].grid(row=0, column=0, sticky="nsew")
        self.pages["startpage"] = Startpage(backroundframe)
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
        settings.add_command(label="marcMentat", command=lambda: self.show_frame("marcMentat"))
        settings.master = menu
        menu.add_cascade(menu=settings, label="Settings")

        self.show_frame("startpage")

    def draw_shape(self, shape, comparison_shape=None, autoscale=True):
        #zeichnet das Polygon
        self.pages["startpage"].draw_shape(shape, comparison_shape, autoscale)

    def show_frame(self, name):
        #wechselt zwischen den Frames, die den ganzen Platz im Fenster einnehmen
        self.pages[name].tkraise()

    def open_file(self):
        filename = tk.filedialog.askopenfilename(filetypes=(("All Files", "*.*"), ("Shape", "*.shape")))#nur ein Beispiel
        if len(filename) != 0:
            print(filename)

    def save_as(self):
        print("save as")


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
        self.mentat_commandlist = Mentat_commandlist(marcMentat_commands)
        self.mentat_commandlist.pack(fill=tk.BOTH, expand=True)

    def get_mentat_commands(self):
        #gibt eine Liste (einen Tuple) aus strings zurück
        #jeder String wird als command an Mentat weitergegeben, nachdem die Form eingelesen 
        #und Kräfte angetragen wurden
        return self.mentat_commandlist.get_all_items()

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
            

class MarcMentatPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        topbox = tk.Frame(self, bg='red')
        label = tk.Label(topbox, text="hier kann man später die Marcs verbinden")
        label.pack()
        topbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        topbox.grid_rowconfigure(0, weight=1)
        topbox.grid_columnconfigure(0, weight=1)

        bottombox = tk.Frame(self)
        close = ttk.Button(bottombox, text="close", command=lambda: self.master.master.show_frame("startpage"))
        close.pack(side=tk.RIGHT, pady=4, padx=4)
        bottombox.pack(side=tk.BOTTOM, fill=tk.X)

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

def create_example_polygon():
    return shape.Shape([(0,0),(200,200),(200,100),(100,0)],holes=[[(100,50), (150,100), (125,50)]])

def second_example_polygon():
    return shape.Shape([(0,0), (20,80), (100,100), (100,0)],[[(10,10), (10,20), (20,10)]])

def complicated_polygon():
    return shape.Shape([(0,0), (3,1), (5,4), (7,4), (9,5), (6,7), (3,8), (1,7), (-1,5), (-3,3), (-2,1)])


gui = GUI()
example = shape.get_cool_example()
example2 = shape.get_cool_example()
gui.draw_shape(example, comparison_shape=example, autoscale=True)
gui.mainloop()

#for i in range(1000):
    #example2 = shape.change_shape_one(example2)
    #gui.draw_shape(example2, comparison_shape=example, autoscale=True)
    #time.sleep(0.2)
    
#input()
##second_example = shape.even_out_shape(example, 1)
##third_example = shape.even_out_shape(second_example)
##gui.draw_shape(third_example, comparison_shape=second_example, autoscale=True)
##gui.update()

























