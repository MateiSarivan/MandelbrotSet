import os
from reportlab.lib.colors import blue, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
import datetime
import time
import psutil
import platform as pfm
import json
import numpy as np

def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def generate_pdf(file_address, experiments):
    """
    pdf generator

    Parameters
    -------
    
    file_address : Path
        Directory for file creation
    x_0 : List of float
        Initial value of x.
    y_0 : List of float
        Initial value of y.
    z_0 : List of float
        Initial value of z.
    dt: Float
        Iteration step.
    N: Float
        Length of iteration.
    elapsed_time : Float
        Time elapsed for parametric analysis
    """
    names = {"Naïve": "Naïve implementation",
    "JIT": "Numba just-in-time compiling",
    "JIT Parallel": "Numba just-in-time compiling with parallel processing",
    "MultiProc": "Multiprocessing",
    "MultiProc JIT": "Multiprocessing with Numba just-in-time compiling"
    }

    #experiments = np.load("Mandelbrot_data.npy", allow_pickle=True)
    canvas = Canvas(os.path.join(file_address, "AA.pdf"), pagesize=A4)
    canvas.setFont("Times-Roman", 28)
    canvas.drawString(5 * cm, 27 * cm, "Mandelbrot Set Experiments")
    canvas.setFont("Times-Roman", 20)
    canvas.drawString(2 * cm, 26 * cm, "Study of processing time using various computation methods")
    canvas.setFont("Times-Roman", 14)
    canvas.drawString(2.5 * cm, (27-3.5) * cm, "Experiments conducted on ")
    day_today = datetime.datetime.now().strftime("%A")
    date_today = datetime.datetime.now().strftime("%d")
    month_today = datetime.datetime.now().strftime("%B")
    year_today = datetime.datetime.now().strftime("%Y")
    time_hms = time.strftime('%H:%M:%S')

    time_string = ' '.join([day_today + ',',
        "the " + ord(int(date_today)),
        "of " + month_today,
        year_today + ",",
        "at",
        str(time_hms)    
    ])

    canvas.drawString(7.7 * cm, (27-3.5) * cm, time_string)

    canvas.setFillColor(black)
    canvas.drawString(2.5 * cm, (27-4.5) * cm, str(len(experiments)) + " experiments were conducted by using the following computation methods: ")
    methods = []
    index = 5.5
    for experiment in experiments:
        if experiment['computation_method'] not in methods:
            methods.append(experiment['computation_method'])
            canvas.drawString(3.5 *cm, cm*(27-index), "→ " + names[experiment['computation_method']])
            index += 1.0
    #canvas.drawString(3.5 * cm, (27-5.5)* cm, methods[0])

    canvas.drawString(2.5 * cm, (27-12.5) * cm, "Experiments conducted using a computer with: " )
    canvas.drawString(3.5 * cm, (27-13.5) * cm, "Python version: " + pfm.python_version())
    canvas.drawString(3.5 * cm, (27-14.5) * cm, "Python build: " + pfm.python_build()[1])
    canvas.drawString(3.5 * cm, (27-15.5) * cm, "Operating system: " + pfm.system())
    canvas.drawString(3.5 * cm, (27-16.5) * cm, "Operating platform: " + pfm.platform())
    canvas.drawString(3.5 * cm, (27-17.5) * cm, "Processor: " + pfm.processor())
    total_ram = psutil.virtual_memory().total/10**9
    total_ram = str(round(total_ram, 2)) + " GB"
    canvas.drawString(3.5 * cm, (27-18.5) * cm, "RAM installed: " + total_ram)

    canvas.drawString(2.5 * cm, (27-20.5) * cm, "In the pages below, time statistics are presented for all the experiments, together with")
    canvas.drawString(2.5 * cm, (27-21.5) * cm, "Mandelbrot set plots for each experiment:")


    canvas.save()