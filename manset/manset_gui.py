import tkinter
from tkinter.constants import HORIZONTAL
import numpy as np
import matplotlib.pyplot as plt
from manset.clean_m import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import time
import timeit
import os

class MansetGUI:
    def __init__(self):

        self.XYRange = np.linspace(0.00001, 3.0, 100)
        self.XFocus = np.linspace(-2.3, 0.7, 100)
        self.YFocus = np.linspace(-1.5, 1.5, 100)
        self.PointsNumber = np.linspace(50, 5000, 100)
        self.CurrentXFocus = self.XFocus[49]
        self.CurrentYFocus = self.YFocus[49]
        self.CurrentXYRange = self.XYRange[99]
        self.CurrentPointsNumber = self.PointsNumber[4]
        self.core_no = None
       
        self.root = tkinter.Tk()
        self.root.geometry("1366x768")
        self.root.wm_title("Mandelbrot Set Plot")

        plot_frame = tkinter.Frame(self.root)
        controls_frame = tkinter.Frame(self.root)
        nav_frame = tkinter.Frame(controls_frame)

        self.fig = Figure(figsize=(10, 10), dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()
        toolbar.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=0)
        
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.BOTTOM,
                                         fill=tkinter.BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, self.canvas, toolbar)
        def press():
            pass
        self.variable = tkinter.StringVar(self.root)
        self.variable.set("Naïve")
        self.compute_mode = tkinter.OptionMenu(controls_frame,
                                               self.variable,
                                               "Naïve", "JIT",
                                               "JIT Parallel",
                                               "MultiProc",
                                               "MultiProc JIT",
                                               command=self.updateValue)
        self.scaler_core_no = tkinter.Scale(master=nav_frame, from_=0,
         to=os.cpu_count(), orient=tkinter.HORIZONTAL)
        self.scaler_x = tkinter.Scale(master=nav_frame, from_=1, to=100,
                                      orient=tkinter.HORIZONTAL)
        self.scaler_y = tkinter.Scale(master=nav_frame, from_=1, to=100,
                                      orient=tkinter.VERTICAL)
        self.scaler_range = tkinter.Scale(master=nav_frame, from_=1,
                                          to=100, orient=tkinter.VERTICAL,
                                          command=self.update_scale)
        self.scaler_points_no = tkinter.Scale(master=nav_frame, from_=1,
                                              to=100,
                                              orient=tkinter.HORIZONTAL,
                                              command=self.update_scale)
        self.scaler_x.set(50)
        self.scaler_y.set(50)
        self.scaler_range.set(100)
        self.scaler_points_no.set(4)
        self.scaler_core_no.set(0)
        self.scaler_core_no.bind("<ButtonRelease-1>", self.updateValue)
        self.scaler_x.bind("<ButtonRelease-1>", self.updateValue)
        self.scaler_y.bind("<ButtonRelease-1>", self.updateValue)
        self.scaler_range.bind("<ButtonRelease-1>", self.updateValue)
        self.scaler_points_no.bind("<ButtonRelease-1>", self.updateValue)
        self.canvas.mpl_connect("key_press_event", on_key_press)

        self.compute_mode.pack()
        self.scaler_core_no.pack()
        self.scaler_points_no.pack()
        self.scaler_range.pack()
        self.scaler_y.pack()
        self.scaler_x.pack()
        nav_frame.pack(side=tkinter.TOP, expand=True)
        plot_frame.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False)
        controls_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y,
                            expand=True)

    def run_gui(self):

        self.plot()
        self.root.mainloop()
        
        # plt.show()

    def plot(self):
        print(self.variable.get())
        x_min = self.CurrentXFocus - self.CurrentXYRange/2
        x_max = self.CurrentXFocus + self.CurrentXYRange/2
        y_min = self.CurrentYFocus - self.CurrentXYRange/2
        y_max = self.CurrentYFocus + self.CurrentXYRange/2

        x_range = np.linspace(x_min, x_max, int(self.CurrentPointsNumber))
        y_range = np.linspace(y_min, y_max, int(self.CurrentPointsNumber))
        mesh = np.empty((len(x_range), len(y_range)))
        start = timeit.default_timer()
        print("here   ", type(np.arange(34)))
        print("here   ", y_range.size)
        
        mesh = comp_type[self.variable.get()](x_range, y_range, self.core_no)
    
        # for index_x in range(len(x_range)):
        #     for index_y in range(len(y_range)):
        #         c_real = x_range[index_x]
        #         c_imaginary = y_range[index_y]

        #         c = complex(c_real, c_imaginary)

        #         mesh[index_x, index_y] = divergence_check(c, 100)
        end = timeit.default_timer() - start
        print(end)
        self.fig.clear()
        print('Cleared')
        # time.sleep(1)
        self.fig.add_subplot(111).imshow(mesh.T, interpolation="nearest",
                                         cmap=plt.cm.hot)
        time.sleep(0.1)
        self.fig.canvas.draw_idle()

    def updateValue(self, event):
        self.CurrentXFocus = self.XFocus[self.scaler_x.get()-1]
        self.CurrentYFocus = self.YFocus[self.scaler_y.get()-1]
        self.CurrentXYRange = self.XYRange[self.scaler_range.get()-1]
        points_no = self.PointsNumber[self.scaler_points_no.get()-1]
        self.CurrentPointsNumber = points_no
        self.core_no = self.scaler_core_no.get()
        if self.core_no == 0:
            self.core_no = None
        self.plot()

    def update_scale(self, event):
        pass

