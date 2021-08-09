import tkinter
from tkinter import ttk
from tkinter.constants import HORIZONTAL
import numpy as np
import matplotlib.pyplot as plt
from manset.mandelbrot import *
from manset.stats_view import StatsView
from manset.plotting import plot_experiments
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import time
import timeit
import os
from datetime import date, datetime
from manset.pdf_gen import generate_pdf
from manset.pdf_merge import merge_pdfs
from threading import Thread

class MansetGUI:
    def __init__(self):

        self.XYRange=np.empty(100)
        range_start = np.double(3)
        for index in np.arange(100):
            self.XYRange[99-index] = range_start
            range_start = range_start/1.1
        #self.XYRange = np.linspace(0.0001, 3.0, 100)

        self.XFocus = np.linspace(-2.3, 0.7, 200)
        self.YFocus = np.linspace(-1.5, 1.5, 200)
        self.PointsNumber = np.linspace(20, 10000, 100)
        self.CurrentXFocus = self.XFocus[99]
        self.CurrentYFocus = self.YFocus[99]
        self.CurrentXYRange = self.XYRange[99]
        self.CurrentPointsNumber = self.PointsNumber[0]
        self.core_no = None
        self.experiments = []
       
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
        frame_saved_experiments = tkinter.Frame(controls_frame)
        frame_buttons = tkinter.Frame(controls_frame)


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
        txt_saved_experiments = tkinter.StringVar()
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
        self.txt_saved_experiments_value = tkinter.StringVar()
        self.txt_status = tkinter.StringVar()

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
        txt_saved_experiments.set("Number of saved experiments: ")
        self.txt_status.set("Ready")
        
        self.txt_selected_no_points_value.set(self.CurrentPointsNumber)
        self.txt_time_value.set("TBD")
        self.txt_min_x_value.set(self.XFocus[0])
        self.txt_max_x_value.set(self.XFocus[99])
        self.txt_min_y_value.set(self.YFocus[0])
        self.txt_max_y_value.set(self.YFocus[99])
        self.txt_range_value.set(self.XYRange[99])
        self.txt_selected_compute_mode_value.set("Naïve")
        self.txt_selected_cores_value.set("Default")
        self.txt_saved_experiments_value.set("0")

        
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
        label_saved_experiments = tkinter.Label(frame_saved_experiments, textvariable=txt_saved_experiments, width=30)
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
        label_saved_experiments_value = tkinter.Label(frame_saved_experiments, textvariable=self.txt_saved_experiments_value, width=30)
        label_status = tkinter.Label(controls_frame, textvariable=self.txt_status, width=60)
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
        self.scaler_x = tkinter.Scale(master=x_frame, from_=1, to=200,
                                      orient=tkinter.HORIZONTAL, command=self.update_scale, length=200)
        self.scaler_y = tkinter.Scale(master=y_frame, from_=1, to=200,
                                      orient=tkinter.VERTICAL, command=self.update_scale)
        self.scaler_range = tkinter.Scale(master=zoom_frame, from_=1,
                                          to=100, orient=tkinter.VERTICAL,
                                          command=self.update_scale)
        self.scaler_points_no = tkinter.Scale(master=no_points_frame, from_=1,
                                              to=100,
                                              orient=tkinter.HORIZONTAL,
                                              command=self.update_scale, length=130)
        self.scaler_x.set(100)
        self.scaler_y.set(100)
        self.scaler_range.set(100)
        self.scaler_points_no.set(0)
        self.scaler_core_no.set(0)
        self.scaler_core_no.bind("<ButtonRelease-1>", self.updateValue)
        self.scaler_x.bind("<ButtonRelease-1>", self.updateValue)
        self.scaler_y.bind("<ButtonRelease-1>", self.updateValue)
        self.scaler_range.bind("<ButtonRelease-1>", self.updateValue)
        self.scaler_points_no.bind("<ButtonRelease-1>", self.updateValue)
        self.canvas.mpl_connect("key_press_event", on_key_press)

        button_stats = tkinter.Button(frame_buttons, text="Show Statistics",  command=self.stats)
        button_save = tkinter.Button(frame_buttons, text="Save experiments",  command=self.save)

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
        label_saved_experiments.pack(side=tkinter.LEFT)
        label_time_value.pack(side=tkinter.LEFT)
        label_min_x_value.pack(side=tkinter.LEFT)
        label_max_x_value.pack(side=tkinter.LEFT)
        label_min_y_value.pack(side=tkinter.LEFT)
        label_max_y_value.pack(side=tkinter.LEFT)
        label_range_value.pack(side=tkinter.LEFT)
        label_selected_compute_mode_value.pack(side=tkinter.LEFT)
        label_selected_cores_value.pack(side=tkinter.LEFT)
        label_selected_no_points_value.pack(side=tkinter.LEFT)
        label_saved_experiments_value.pack(side=tkinter.LEFT)

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
        frame_saved_experiments.pack(side=tkinter.TOP)
        self.var1 = tkinter.IntVar()
        self.chbox = tkinter.Checkbutton(controls_frame, text='Save Experiment',variable=self.var1, onvalue=1, offvalue=0)
        self.chbox.pack(side=tkinter.TOP)
        button_stats.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X)
        button_save.pack(side=tkinter.LEFT, expand = True, fill=tkinter.X)
        self.button_save = button_save
        
        
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
        frame_buttons.pack(side=tkinter.TOP, expand=True, fill=tkinter.X)
        label_status.pack(side=tkinter.TOP, expand=True, fill=tkinter.X)
        
        plot_frame.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False)
        controls_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y,
                            expand=True)

    def run_gui(self):

        self.plot()
        self.var1.set(1)
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
        self.txt_max_x_value.set(str(round(x_max, 6)))
        self.txt_min_x_value.set(str(round(x_min, 6)))
        self.txt_max_y_value.set(str(round(y_max, 6)))
        self.txt_min_y_value.set(str(round(y_min, 6)))
        x_range = np.linspace(x_min, x_max, int(self.CurrentPointsNumber))
        y_range = np.linspace(y_min, y_max, int(self.CurrentPointsNumber))
        self.txt_range_value.set(str(round(x_range[x_range.size-1] - x_range[0], 6)))
        self.txt_selected_no_points_value.set(str(self.CurrentPointsNumber))
        self.txt_selected_cores_value.set(txt_core_no)
        self.txt_selected_compute_mode_value.set(self.variable.get())

    def stats(self):
        print("stats")
        StatsView(self.root, self.experiments)

    def save(self):
        self.txt_status.set("Saving experiments... Wait!")
        self.button_save['state'] = tkinter.DISABLED
        dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        name = "Mandelbrot " + dt_string
        file_address = tkinter.filedialog.askdirectory()
        if name not in file_address and len(file_address):
            file_address = os.path.join(file_address, name)
            if not os.path.exists(file_address):
                os.makedirs(file_address)
        np.save(os.path.join(file_address, "Mandelbrot_data.npy"), self.experiments)
        def save_thread():
        
            plot_experiments(file_address, self.experiments)
            generate_pdf(file_address, self.experiments)
            merge_pdfs(file_address, "Mandelbrot set experiments.pdf")
            self.txt_status.set("Ready")
            self.button_save['state'] = tkinter.NORMAL
        
        thr = Thread(target=save_thread)
        thr.start()

        
    def plot(self):

        x_min = self.CurrentXFocus - self.CurrentXYRange/2
        x_max = self.CurrentXFocus + self.CurrentXYRange/2
        y_min = self.CurrentYFocus - self.CurrentXYRange/2
        y_max = self.CurrentYFocus + self.CurrentXYRange/2
        x_range = np.linspace(x_min, x_max, int(self.CurrentPointsNumber))
        y_range = np.linspace(y_min, y_max, int(self.CurrentPointsNumber))
        mesh = np.empty((len(x_range), len(y_range)))
        start = timeit.default_timer()
 
        mesh = comp_type[self.variable.get()](x_range, y_range, self.core_no)
    
        end = timeit.default_timer() - start

        self.txt_time_value.set(str(round(end, 6)))
        self.fig.clear()

 
        self.fig.add_subplot(111).imshow(mesh.T, interpolation="nearest",
                                         cmap=plt.cm.hot, extent=[x_min, x_max, y_min, y_max])

        self.fig.canvas.draw_idle()
        self.core_no = self.scaler_core_no.get()
        txt_core_no = str(self.core_no)
        if self.core_no == 0:
            self.core_no = None
            txt_core_no = "Default"
        experiment = {
            "elapsed_time": end,
            "computation_method": self.variable.get(),
            "number of cores": txt_core_no,
            "range": x_range[x_range.size-1] - x_range[0],
            "min_x": x_min,
            "max_x": x_max,
            "min_y": y_min,
            "max_y": y_max,
            "no_points": self.CurrentPointsNumber,
            "result": mesh
        }

        if self.var1.get():
            if len(self.experiments) < 20:
                self.experiments.append(experiment)
                self.txt_saved_experiments_value.set(str(len(self.experiments)))
            else:
                self.txt_status.set("Reached maximum allowed experiments. Start a new session.")
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
