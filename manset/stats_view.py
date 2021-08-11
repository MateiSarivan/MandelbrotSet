import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from numpy import exp


class StatsView:
    def __init__(self, root, experiments):

        self.experiments = experiments
        top_frame = tkinter.Toplevel(root)
        top_frame.title("Experiments statistics")
        top_frame.geometry("783x484")

        time_data = []
        experiment_numbers = []
        experiment_index = 0
        experiment_strings = []
        for experiment in experiments:
            time_data.append(experiment['elapsed_time'])
            experiment_numbers.append(experiment_index)
            experiment_string = (str(experiment_index) + ": " + experiment['computation_method'] + " | " +
                                 str(int(experiment['no_points'])) + " pts" + "  |  " +
                                 experiment["number of cores"] + " cores")
            experiment_strings.append(experiment_string)
            experiment_index += 1

        plot_frame = tkinter.Frame(top_frame)
        right_frame = tkinter.Frame(top_frame)
        listbox_frame = tkinter.Frame(right_frame)
        x_frame = tkinter.Frame(right_frame)
        y_frame = tkinter.Frame(right_frame)
        range_frame = tkinter.Frame(right_frame)

        x_txt = tkinter.StringVar()
        y_txt = tkinter.StringVar()
        range_txt = tkinter.StringVar()
        self.value_x_txt = tkinter.StringVar()
        self.value_y_txt = tkinter.StringVar()
        self.value_range_txt = tkinter.StringVar()

        x_txt.set("x min | x max: ")
        y_txt.set("y min | y max: ")
        range_txt.set("Range: ")
        self.value_x_txt.set("TBD")
        self.value_y_txt.set("TBD")
        self.value_range_txt.set("TBD")

        x_label = tkinter.Label(x_frame, textvariable=x_txt, width=20)
        y_label = tkinter.Label(y_frame, textvariable=y_txt, width=20)
        range_label = tkinter.Label(range_frame, textvariable=range_txt, width=20)
        value_x_label = tkinter.Label(x_frame, textvariable=self.value_x_txt, width=20)
        value_y_label = tkinter.Label(y_frame, textvariable=self.value_y_txt, width=20)
        value_range_label = tkinter.Label(range_frame, textvariable=self.value_range_txt, width=20)

        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).bar(experiment_numbers, time_data)

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        self.listbox = tkinter.Listbox(listbox_frame, width=35, height=25)
        self.listbox.bind("<<ListboxSelect>>", self.list_select)

        scrollbar = tkinter.Scrollbar(listbox_frame)
        self.listbox.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)
        scrollbar.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        plot_frame.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False)
        listbox_frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

        x_label.pack(side=tkinter.LEFT)
        y_label.pack(side=tkinter.LEFT)
        range_label.pack(side=tkinter.LEFT)
        value_x_label.pack(side=tkinter.LEFT)
        value_y_label.pack(side=tkinter.LEFT)
        value_range_label.pack(side=tkinter.LEFT)

        x_frame.pack(side=tkinter.TOP)
        y_frame.pack(side=tkinter.TOP)
        range_frame.pack(side=tkinter.TOP)

        right_frame.pack(side=tkinter.RIGHT, expand=True)

        for string in experiment_strings:
            self.listbox.insert(tkinter.END, string)


    def list_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            experiment = self.experiments[index]

            self.value_x_txt.set(str(round(experiment['min_x'], 3)) + "  |  " + str(round(experiment['max_x'], 4)))
            self.value_y_txt.set(str(round(experiment['min_y'], 3)) + "  |  " + str(round(experiment['max_y'], 4)))
            self.value_range_txt.set(str(round(experiment['range'], 4)))
