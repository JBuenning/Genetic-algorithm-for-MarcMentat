import tkinter as tk

class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        #self.core = core.Core()
        #self.minsize(width=500, height=300)
        self.title("Genetic MarcMentat")

        #Backroundframe, der allen Platz des Fensters einnimmt und auf den alles gezeichnet wird
        backroundframe = tk.Frame(self, bg='green')
        backroundframe.pack(fill=tk.BOTH, expand=True)
        backroundframe.columnconfigure(0, weight=1)
        backroundframe.rowconfigure(0, weight=1)

        #alle Frames, die auf dem Backroundframe liegen
        self.pages = {}
        #self.pages["marcMentat"] = MarcMentatPage(backroundframe, self.core)
        #self.pages["marcMentat"].grid(row=0, column=0, sticky="nsew")
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

    def show_frame(self, name):
        #wechselt zwischen den Frames, die den ganzen Platz im Fenster einnehmen
        self.pages[name].tkraise()

    def open_file(self):
        filename = tk.filedialog.askopenfilename(filetypes=(("All Files", "*.*"), ("Shape", "*.shape")))#nur ein Beispiel
        if len(filename) != 0:
            print(filename)

    def save_as(self):
        print("save as")
class Startpage(tk.PanedWindow):

    def __init__(self, parent):
        super().__init__(parent)

        leftbox = tk.Frame(self, bg='yellow')
        self.add(leftbox)
        label = tk.Label(leftbox, text='sldkfj')
        label.pack()
        rightbox = tk.Frame(self, bg='red')
        self.add(rightbox)

root = GUI()
root.mainloop()