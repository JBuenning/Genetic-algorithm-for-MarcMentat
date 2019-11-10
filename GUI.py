import tkinter as tk

root = tk.Tk()
frame = tk.Frame(root, bg = 'black')
canvas = tk.Canvas(root, height=500, width=500)
canvas.pack()

root.mainloop()