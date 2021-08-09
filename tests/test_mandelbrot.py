import numpy as np
import pathlib
import os
from manset.mandelbrot import *


# def test_this():
#     assert 1==1

def test_naive():
    path = pathlib.Path(__file__).parent.resolve()
    test_mesh = np.load(os.path.join(path, "Mandelbrot_test_data.npy")).T
    print(np.round(test_mesh))
    x_range = np.linspace(-2.3, 0.7, 20)
    y_range = np.linspace(-1.5, 1.5, 20)
    tested_mesh = np.round(divergence_check_naive(x_range, y_range).T)
    print(test_mesh[10, 10])
    print(tested_mesh[10, 10])
    print(np.round(tested_mesh))
    test_result = test_mesh == tested_mesh
    assert test_result.all() == True
    
def test_jit():
    path = pathlib.Path(__file__).parent.resolve()
    test_mesh = np.load(os.path.join(path, "Mandelbrot_test_data.npy")).T
    print(np.round(test_mesh))
    x_range = np.linspace(-2.3, 0.7, 20)
    y_range = np.linspace(-1.5, 1.5, 20)
    tested_mesh = np.round(divergence_check_jit(x_range, y_range).T)
    print(test_mesh[10, 10])
    print(tested_mesh[10, 10])
    print(np.round(tested_mesh))
    test_result = test_mesh == tested_mesh
    assert test_result.all() == True

def test_jit_parallel():
    path = pathlib.Path(__file__).parent.resolve()
    test_mesh = np.load(os.path.join(path, "Mandelbrot_test_data.npy")).T
    print(np.round(test_mesh))
    x_range = np.linspace(-2.3, 0.7, 20)
    y_range = np.linspace(-1.5, 1.5, 20)
    tested_mesh = np.round(divergence_check_jit_parallel(x_range, y_range).T)
    print(test_mesh[10, 10])
    print(tested_mesh[10, 10])
    print(np.round(tested_mesh))
    test_result = test_mesh == tested_mesh
    assert test_result.all() == True

def test_multi():
    path = pathlib.Path(__file__).parent.resolve()
    test_mesh = np.load(os.path.join(path, "Mandelbrot_test_data.npy")).T
    print(np.round(test_mesh))
    x_range = np.linspace(-2.3, 0.7, 20)
    y_range = np.linspace(-1.5, 1.5, 20)
    tested_mesh = np.round(divergence_check_multi(x_range, y_range).T)
    print(test_mesh[10, 10])
    print(tested_mesh[10, 10])
    print(np.round(tested_mesh))
    test_result = test_mesh == tested_mesh
    assert test_result.all() == True

def test_multi_jit():
    path = pathlib.Path(__file__).parent.resolve()
    test_mesh = np.load(os.path.join(path, "Mandelbrot_test_data.npy")).T
    print(np.round(test_mesh))
    x_range = np.linspace(-2.3, 0.7, 20)
    y_range = np.linspace(-1.5, 1.5, 20)
    tested_mesh = np.round(divergence_check_multi_jit(x_range, y_range).T)
    print(test_mesh[10, 10])
    print(tested_mesh[10, 10])
    print(np.round(tested_mesh))
    test_result = test_mesh == tested_mesh
    assert test_result.all() == True