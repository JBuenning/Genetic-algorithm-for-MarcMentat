from tkinter import *

class Fenster(Tk):
    def __init__(self):
        super().__init__()
        self.minsize(width=500, height=300)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        f = Canvas(self, bg='red')
        f.grid(sticky="nsew")
        f.grid_columnconfigure(0, weight=1)
        f.grid_rowconfigure(0, weight=1)

        c = Canvas(f, bg='blue')
        c.grid(sticky="nsew")

        c.create_line(0, 0, 200, 100)

f = Fenster()
f.mainloop()
