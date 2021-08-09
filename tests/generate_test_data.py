import numpy as np
from manset.mandelbrot import divergence_check_naive

x_range = np.linspace(-2.3, 0.7, 20)
y_range = np.linspace(-1.5, 1.5, 20)

mesh = divergence_check_naive(x_range, y_range)
mesh = np.round(mesh)

np.save("Mandelbrot_test_data.npy", mesh)