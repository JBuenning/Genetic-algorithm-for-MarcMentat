import tkinter as tk
from tkinter import ttk
from algorithms import mutation_algorithms


class ToggledFrameAlgorithm(tk.Frame):

    def __init__(self, parent, algorithm, *args, **options):
        super().__init__(parent, *args, **options)

        self.algorithm = algorithm
        self.show = tk.BooleanVar()
        self.show.set(False)

        self.status = tk.BooleanVar()
        self.status.set(True)

        self.title_frame = tk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='ᐅ', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.label = tk.Label(self.title_frame, text = self.algorithm.get_name())
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

    def add_component(self, component):
        self.sub_frame = component



if __name__ == "__main__":
    root = tk.Tk()

    headline = ToggledFrameContainer(root,'Überschrift')
    headline.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    algo = mutation_algorithms.AlgorithmOne()
    t = ToggledFrameAlgorithm(headline,algo, borderwidth=1)
    #t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    headline.add_component(t)

    # t2 = ToggledFrameAlgorithm(t.sub_frame, text='Rotate', relief="raised", borderwidth=1)
    # t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
    # ttk.Label(t2.sub_frame, text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
    # ttk.Entry(t2.sub_frame).pack(side="left")

    # t2 = ToggledFrame(root, text='Resize', relief="raised", borderwidth=1)
    # t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    # for i in range(10):
    #     ttk.Label(t2.sub_frame, text='Test' + str(i)).pack()

    # t3 = ToggledFrame(root, text='Fooo', relief="raised", borderwidth=1)
    # t3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    # for i in range(10):
    #     ttk.Label(t3.sub_frame, text='Bar' + str(i)).pack()

    root.mainloop()