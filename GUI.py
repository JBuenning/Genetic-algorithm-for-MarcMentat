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
        right_label = tk.Label(rightbox, text='Platz für Knöpfe usw\nnatürlich nur ein\nvorläufiges Layout')
        right_label.pack()
        rightbox.pack(side=tk.RIGHT, fill=tk.Y)

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
gui.update()

for i in range(1000):
    example2 = shape.change_shape_one(example2)
    gui.draw_shape(example2, comparison_shape=example, autoscale=True)
    time.sleep(0)
    
input()
##second_example = shape.even_out_shape(example, 1)
##third_example = shape.even_out_shape(second_example)
##gui.draw_shape(third_example, comparison_shape=second_example, autoscale=True)
##gui.update()

























