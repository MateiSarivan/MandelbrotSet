import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os


def plot_experiments(file_address, experiments):

    recorded_time = []
    indexes = []
    index = 0
    strings = 'Experiments:\n\n'
    for experiment in experiments:
        index += 1
        indexes.append(index)
        recorded_time.append(experiment['elapsed_time'])
        strings = (strings + str(index) + ": " + experiment["computation_method"] +
                   ", " + str(experiment['number of cores']) +
                   " cores, " + str(int(experiment['no_points'])) + " points per axis, " +
                   "ET: " + str(round(experiment['elapsed_time'], 6)) + " seconds" + "\n")

        font = {'family': 'Arial',
                'size': '11'}

        plt.rc('font', **font)
        fig = plt.figure(figsize=(10, 11))
        cmap = plt.cm.hot
        plot = fig.add_subplot(111)
        plot.imshow(experiment['result'].T, interpolation="nearest",
                    cmap=plt.cm.hot, extent=[experiment['min_x'],
                    experiment['max_x'], experiment['min_y'], experiment['max_y']])
        plot.set_xlabel("x\n\nValue range: " + str(experiment['range']) +
                        "\nx min | x max: " + str(experiment['min_x']) + ' | ' + str(experiment['max_x']) +
                        "\ny min | y max: " + str(experiment['min_y']) + ' | ' + str(experiment['max_y']))
        plot.set_ylabel("y")
        fig.suptitle("Mandelbrot Set\n\nComputation Method: " + experiment["computation_method"] +
                     "\nNumber of cores: " + str(experiment["number of cores"]) +
                     "\nNumber of points per axis: " + str(experiment["no_points"]) +
                     "\nElapsed computation time: " + str(experiment['elapsed_time']) + " seconds")
        address = os.path.join(file_address, "Experiment " + str(index) + ".png")
        plt.savefig(address, dpi=240)
        address = os.path.join(file_address, "Experiment " + str(index) + ".pdf")
        plt.savefig(address, dpi=240)
        if index == 20:
            break

    font = {'family': 'Arial',
            'size': '11'}

    plt.rc('font', **font)
    fig = plt.figure(figsize=(10, 11))
    plot = fig.add_subplot(111)
    plot.bar(indexes, recorded_time)
    plot.set_ylabel("Seconds")
    plot.set_xlabel("Experiment number")
    fig.suptitle("Mandelbrot experiments time statistics")
    plt.subplots_adjust(top=0.53)
    print(strings)
    plt.gcf().text(0.12, 0.55, strings, fontsize=12)
    address = os.path.join(file_address, "Time Statistics.png")
    plt.savefig(address, dpi=240)
    address = os.path.join(file_address, "AATime Statistics.pdf")
    plt.savefig(address, dpi=240)
