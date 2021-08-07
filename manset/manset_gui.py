import tkinter
from tkinter import ttk
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

        self.XYRange = np.linspace(0.0001, 3.0, 100)
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
        compute_mode_frame = tkinter.Frame(controls_frame)
        no_cores_frame = tkinter.Frame(controls_frame)
        no_points_frame = tkinter.Frame(controls_frame)
        zoom_frame = tkinter.Frame(controls_frame)
        y_frame = tkinter.Frame(controls_frame)
        x_frame = tkinter.Frame(controls_frame)
        frame_time = tkinter.Frame(controls_frame)
        frame_min_x = tkinter.Frame(controls_frame)
        frame_max_x = tkinter.Frame(controls_frame)
        frame_min_y = tkinter.Frame(controls_frame)
        frame_max_y = tkinter.Frame(controls_frame)
        frame_range = tkinter.Frame(controls_frame)
        frame_selected_compute_mode = tkinter.Frame(controls_frame)
        frame_selected_cores = tkinter.Frame(controls_frame)
        frame_selected_no_points = tkinter.Frame(controls_frame)


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
        txt_compute_mode = tkinter.StringVar()
        txt_no_cores = tkinter.StringVar()
        txt_no_points = tkinter.StringVar()
        txt_zoom = tkinter.StringVar()
        txt_y = tkinter.StringVar()
        txt_x = tkinter.StringVar()
        txt_time = tkinter.StringVar()
        txt_min_x = tkinter.StringVar()
        txt_max_x = tkinter.StringVar()
        txt_min_y = tkinter.StringVar()
        txt_max_y = tkinter.StringVar()
        txt_range = tkinter.StringVar()
        txt_selected_compute_mode = tkinter.StringVar()
        txt_selected_cores = tkinter.StringVar()
        txt_selected_no_points =tkinter.StringVar()
        self.txt_time_value = tkinter.StringVar()
        self.txt_min_x_value = tkinter.StringVar()
        self.txt_max_x_value = tkinter.StringVar()
        self.txt_min_y_value = tkinter.StringVar()
        self.txt_max_y_value = tkinter.StringVar()
        self.txt_range_value = tkinter.StringVar()
        self.txt_selected_compute_mode_value = tkinter.StringVar()
        self.txt_selected_cores_value = tkinter.StringVar()
        self.txt_selected_no_points_value =tkinter.StringVar()

        txt_compute_mode.set("Select computational mode: ")
        txt_no_cores.set("Select number of cores: ")
        txt_no_points.set("Select number of points/axis: ")
        txt_zoom.set("Zoom:")
        txt_y.set("y axis navigation: ")
        txt_x.set("x axis navigation: ")
        txt_time.set("Elapsed generation time: ")
        txt_min_x.set("Minumum value of x: ")
        txt_max_x.set("Maximum value of x: ")
        txt_min_y.set("Minimum value of y: ")
        txt_max_y.set("Minimum value of y: ")
        txt_range.set("Range: ")
        txt_selected_compute_mode.set("Selected computation mode: ")
        txt_selected_cores.set("Number of cores selected: ")
        txt_selected_no_points.set("Number of points per axis: ")
        
        self.txt_selected_no_points_value.set(self.CurrentPointsNumber)
        self.txt_time_value.set("TBD")
        self.txt_min_x_value.set(self.XFocus[0])
        self.txt_max_x_value.set(self.XFocus[99])
        self.txt_min_y_value.set(self.YFocus[0])
        self.txt_max_y_value.set(self.YFocus[99])
        self.txt_range_value.set(self.XYRange[99])
        self.txt_selected_compute_mode_value.set("Naïve")
        self.txt_selected_cores_value.set("Default")

        
        label_compute_mode = tkinter.Label(compute_mode_frame, textvariable=txt_compute_mode, width=30)
        label_no_cores = tkinter.Label(no_cores_frame, textvariable=txt_no_cores, width=30)
        label_no_points = tkinter.Label(no_points_frame, textvariable=txt_no_points, width=30)
        label_zoom = tkinter.Label(zoom_frame, textvariable=txt_zoom, width=30)
        label_x = tkinter.Label(x_frame, textvariable=txt_x, width=30)
        label_y = tkinter.Label(y_frame, textvariable=txt_y, width=30)
        label_time = tkinter.Label(frame_time, textvariable=txt_time, width=30)
        label_min_x = tkinter.Label(frame_min_x, textvariable=txt_min_x, width=30)
        label_max_x = tkinter.Label(frame_max_x, textvariable=txt_max_x, width=30)
        label_min_y = tkinter.Label(frame_min_y, textvariable=txt_min_y, width=30)
        label_max_y = tkinter.Label(frame_max_y, textvariable=txt_max_y, width=30)
        label_range = tkinter.Label(frame_range, textvariable=txt_range, width=30)
        label_selected_compute_mode = tkinter.Label(frame_selected_compute_mode, textvariable=txt_selected_compute_mode, width=30)
        label_selected_cores = tkinter.Label(frame_selected_cores, textvariable=txt_selected_cores, width=30)
        label_selected_no_points = tkinter.Label(frame_selected_no_points, textvariable=txt_selected_no_points, width=30)
        label_time_value = tkinter.Label(frame_time, textvariable=self.txt_time_value, width=30)
        label_min_x_value = tkinter.Label(frame_min_x, textvariable=self.txt_min_x_value, width=30)
        label_max_x_value = tkinter.Label(frame_max_x, textvariable=self.txt_max_x_value, width=30)
        label_min_y_value = tkinter.Label(frame_min_y, textvariable=self.txt_min_y_value, width=30)
        label_max_y_value = tkinter.Label(frame_max_y, textvariable=self.txt_max_y_value, width=30)
        label_range_value = tkinter.Label(frame_range, textvariable=self.txt_range_value, width=30)
        label_selected_compute_mode_value = tkinter.Label(frame_selected_compute_mode, textvariable=self.txt_selected_compute_mode_value, width=30)
        label_selected_cores_value = tkinter.Label(frame_selected_cores, textvariable=self.txt_selected_cores_value, width=30)
        label_selected_no_points_value = tkinter.Label(frame_selected_no_points, textvariable=self.txt_selected_no_points_value, width=30)
        self.compute_mode = tkinter.OptionMenu(compute_mode_frame,
                                               self.variable,
                                               "Naïve", "JIT",
                                               "JIT Parallel",
                                               "MultiProc",
                                               "MultiProc JIT",
                                               command=self.updateValue)
        self.compute_mode.config(width=15)
        self.scaler_core_no = tkinter.Scale(master=no_cores_frame, from_=0,
         to=os.cpu_count(), orient=tkinter.HORIZONTAL, length=130, command=self.update_scale)
        self.scaler_x = tkinter.Scale(master=x_frame, from_=1, to=100,
                                      orient=tkinter.HORIZONTAL, command=self.update_scale)
        self.scaler_y = tkinter.Scale(master=y_frame, from_=1, to=100,
                                      orient=tkinter.VERTICAL, command=self.update_scale)
        self.scaler_range = tkinter.Scale(master=zoom_frame, from_=1,
                                          to=100, orient=tkinter.VERTICAL,
                                          command=self.update_scale)
        self.scaler_points_no = tkinter.Scale(master=no_points_frame, from_=1,
                                              to=100,
                                              orient=tkinter.HORIZONTAL,
                                              command=self.update_scale, length=130)
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

        label_compute_mode.pack(side=tkinter.LEFT)
        self.compute_mode.pack(side=tkinter.LEFT)
        label_no_cores.pack(side=tkinter.LEFT)
        self.scaler_core_no.pack(side=tkinter.LEFT)
        label_no_points.pack(side=tkinter.LEFT)
        self.scaler_points_no.pack(side=tkinter.LEFT)
        label_zoom.pack(side=tkinter.LEFT)
        self.scaler_range.pack()
        label_y.pack(side=tkinter.LEFT)
        self.scaler_y.pack()
        label_x.pack(side=tkinter.LEFT)
        self.scaler_x.pack()
        label_time.pack(side=tkinter.LEFT)
        label_min_x.pack(side=tkinter.LEFT)
        label_max_x.pack(side=tkinter.LEFT)
        label_min_y.pack(side=tkinter.LEFT)
        label_max_y.pack(side=tkinter.LEFT)
        label_range.pack(side=tkinter.LEFT)
        label_selected_compute_mode.pack(side=tkinter.LEFT)
        label_selected_cores.pack(side=tkinter.LEFT)
        label_selected_no_points.pack(side=tkinter.LEFT)
        label_time_value.pack(side=tkinter.LEFT)
        label_min_x_value.pack(side=tkinter.LEFT)
        label_max_x_value.pack(side=tkinter.LEFT)
        label_min_y_value.pack(side=tkinter.LEFT)
        label_max_y_value.pack(side=tkinter.LEFT)
        label_range_value.pack(side=tkinter.LEFT)
        label_selected_compute_mode_value.pack(side=tkinter.LEFT)
        label_selected_cores_value.pack(side=tkinter.LEFT)
        label_selected_no_points_value.pack(side=tkinter.LEFT)

        sep = ttk.Separator(controls_frame, orient="horizontal")
        sep.pack(side=tkinter.TOP, expand=True)
        frame_selected_compute_mode.pack(side=tkinter.TOP)
        frame_selected_cores.pack(side=tkinter.TOP)
        frame_selected_no_points.pack(side=tkinter.TOP)
        frame_range.pack(side=tkinter.TOP)
        frame_min_x.pack(side=tkinter.TOP)
        frame_max_x.pack(side=tkinter.TOP)
        frame_min_y.pack(side=tkinter.TOP)
        frame_max_y.pack(side=tkinter.TOP)
        frame_time.pack(side=tkinter.TOP)
        
        
        sep = ttk.Separator(controls_frame, orient="horizontal")
        sep.pack(side=tkinter.TOP, expand=True)
        
        compute_mode_frame.pack(side=tkinter.TOP)
        no_cores_frame.pack(side=tkinter.TOP)
        no_points_frame.pack(side=tkinter.TOP)
        zoom_frame.pack(side=tkinter.TOP)
        y_frame.pack(side=tkinter.TOP)
        x_frame.pack(side=tkinter.TOP)
        sep = ttk.Separator(controls_frame, orient="horizontal")
        sep.pack(side=tkinter.TOP, expand=True)
        
        
        plot_frame.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False)
        controls_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y,
                            expand=True)

    def run_gui(self):

        self.plot()
        self.root.mainloop()
        
        # plt.show()

    def update_scale(self, event):
        self.CurrentXFocus = self.XFocus[self.scaler_x.get()-1]
        self.CurrentYFocus = self.YFocus[self.scaler_y.get()-1]
        self.CurrentXYRange = self.XYRange[self.scaler_range.get()-1]
        points_no = self.PointsNumber[self.scaler_points_no.get()-1]
        self.CurrentPointsNumber = points_no
        self.core_no = self.scaler_core_no.get()
        txt_core_no = str(self.core_no)
        if self.core_no == 0:
            self.core_no = None
            txt_core_no = "Default"
        x_min = self.CurrentXFocus - self.CurrentXYRange/2
        x_max = self.CurrentXFocus + self.CurrentXYRange/2
        y_min = self.CurrentYFocus - self.CurrentXYRange/2
        y_max = self.CurrentYFocus + self.CurrentXYRange/2
        self.txt_max_x_value.set(str(round(x_max, 4)))
        self.txt_min_x_value.set(str(round(x_min, 4)))
        self.txt_max_y_value.set(str(round(y_max, 4)))
        self.txt_min_y_value.set(str(round(y_min, 4)))
        x_range = np.linspace(x_min, x_max, int(self.CurrentPointsNumber))
        y_range = np.linspace(y_min, y_max, int(self.CurrentPointsNumber))
        self.txt_range_value.set(str(round(x_range[x_range.size-1] - x_range[0], 4)))
        self.txt_selected_no_points_value.set(str(self.CurrentPointsNumber))
        self.txt_selected_cores_value.set(txt_core_no)
        self.txt_selected_compute_mode_value.set(self.variable.get())


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
        self.txt_time_value.set(str(round(end, 4)))
        self.fig.clear()
        print('Cleared')
        # time.sleep(1)
        self.fig.add_subplot(111).imshow(mesh.T, interpolation="nearest",
                                         cmap=plt.cm.hot)
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
