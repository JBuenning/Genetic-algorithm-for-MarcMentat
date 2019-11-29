#der Frame heißt plot_box
f = matplotlib.figure.Figure()
self.plot = f.add_subplot(111)
self.plot_canvas = FigureCanvasTkAgg(f, plot_box)
self.plot_canvas.draw()
toolbar = NavigationToolbar2Tk(self.plot_canvas, plot_box)
toolbar.update()
self.plot_canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
self.plot.plot([0,1,2,3],[8,6,4,7])
