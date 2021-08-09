from concurrent.futures.process import ProcessPoolExecutor
import numba as nb
from numba import core
import numpy as np
import functools

def divergence_check_naive(x_range, y_range, core_no=None):
    len_x = len(x_range)
    len_y = len(y_range)
    mesh = np.empty((len_x, len_y))
    for index_x in range(len_x):
        for index_y in range(len_y):
            c_real = x_range[index_x]
            c_imaginary = y_range[index_y]
            
            c = complex(c_real, c_imaginary)

            z = complex(0, 0)

            for iteration_number in range(100):
                z = z*z+c
                if np.abs(z) > 4:
                    mesh[index_x, index_y] = iteration_number
                    break
            # else:
            #     mesh[index_x, index_y] = 0

    return mesh


def divergence_check_naive2(x_range, y_range, core_no=None):
    len_x = x_range.size
    len_y = y_range.size
    mesh = np.empty((len_x, len_y))
    for index_x in np.arange(len_x):
        for index_y in np.arange(len_y):
            c_real = np.double(x_range[index_x])
            c_imaginary = np.double(y_range[index_y])
            c_x = c_real
            c_y = c_imaginary

            for iteration_number in np.arange(100):
                c_real_squared = c_real * c_real - c_imaginary * c_imaginary
                c_imaginary_squared = 2*c_real*c_imaginary
                c_real = c_x + c_real_squared
                c_imaginary = c_y + c_imaginary_squared

                if np.abs(c_real + c_imaginary) > 4:
                    mesh[index_x, index_y] = iteration_number
                    break

    return mesh


@nb.jit(nopython=True)
def divergence_check_jit(x_range, y_range, core_no=None):

    mesh = np.empty((x_range.size, y_range.size))
    for index_x in np.arange(x_range.size):
        c_real = x_range[index_x]
        for index_y in np.arange(y_range.size):

            c_imaginary = y_range[index_y]
            
            c = complex(c_real, c_imaginary)

            z = complex(0, 0)

            for iteration_number in np.arange(100):
                z = z*z+c
                if np.abs(z) > 4:
                    mesh[index_x, index_y] = iteration_number
                    break
            else:
                mesh[index_x, index_y] = 0

    return mesh

@nb.jit(nopython=True)
def div_check_jit_parallel(c_real, c_imaginary):
    c = complex(c_real, c_imaginary)
    z = complex(0, 0)
    for iteration_number in np.arange(100):
        z = z*z+c
        if np.abs(z) > 4:
            return iteration_number
    else:
        return 0

@nb.jit(nopython = True, parallel = True)
def divergence_check_jit_parallel(x_range, y_range, core_no=None):
    mesh = np.empty((x_range.size, y_range.size))
    for index_x in nb.prange(x_range.size):
        c_real = x_range[index_x]
        for index_y in nb.prange(x_range.size):
            c_imaginary = y_range[index_y]
            mesh[index_x, index_y] = div_check_jit_parallel(c_real, c_imaginary)

    return mesh

@nb.jit(nopython=True, parallel = True)
def divergence_check_jit3(x_range, y_range, core_no=None):

    mesh = np.empty((x_range.size, y_range.size))
    for index_x in np.arange(x_range.size):
        c_real = x_range[index_x]
        for index_y in np.arange(y_range.size):

            c_imaginary = y_range[index_y]
            
            c = complex(c_real, c_imaginary)

            z = complex(0, 0)

            for iteration_number in np.arange(100):
                z = z*z+c
                if np.abs(z) > 4:
                    mesh[index_x, index_y] = iteration_number
                    break
            else:
                mesh[index_x, index_y] = 0

    return mesh

def div_check(y_range, c_real, core_no=None):
    result = np.empty(y_range.size)
    for index_y in range(y_range.size):
        c_imaginary = y_range[index_y]
        c = complex(c_real, c_imaginary)
        z = complex(0, 0)

        for iteration_number in range(100):
            z = z * z + c
            if np.abs(z) > 4:
                result[index_y] = iteration_number
                break
        else:
            result[index_y] = 0

    # print(result)
    return result

@nb.jit(nopython=True)
def div_check_jit(y_range, c_real):
    result = np.empty(y_range.size)
    for index_y in range(y_range.size):
        c_imaginary = y_range[index_y]
        c = complex(c_real, c_imaginary)
        z = complex(0, 0)

        for iteration_number in range(100):
            z = z * z + c
            if np.abs(z) > 4:
                result[index_y] = iteration_number
                break
        else:
            result[index_y] = 0

    # print(result)
    return result


def divergence_check_multi(x_range=np.array([1, 2, 3, 4]), y_range=np.array([5, 6, 7, 8]), core_no=None):
    len_x = len(x_range)
    len_y = len(y_range)
    mesh = np.empty((len_x, len_y))
    #div_check(0, [0, 1])
    partial_div_check = functools.partial(div_check, y_range)
    print("core_no ", core_no)
    pool = ProcessPoolExecutor(max_workers=core_no)
    future = pool.map(partial_div_check, x_range)
    pool.shutdown()


    index = 0
    for result in future:
        mesh[index, :] = result
        index += 1

    return mesh


def divergence_check_multi_jit(x_range=np.array([1, 2, 3, 4]), y_range=np.array([5, 6, 7, 8]), core_no=None):
    len_x = len(x_range)
    len_y = len(y_range)
    mesh = np.empty((len_x, len_y))
    partial_div_check = functools.partial(div_check_jit, y_range)
    print("core_no  ", core_no)
    pool = ProcessPoolExecutor(max_workers=core_no)
    future = pool.map(partial_div_check, x_range)
    pool.shutdown()


    index = 0
    print(type(future))
    for result in future:
        mesh[index, :] = result
        index += 1

    return mesh
    

comp_type = {
    "Naïve": divergence_check_naive,
    "JIT": divergence_check_jit,
    "JIT Parallel": divergence_check_jit_parallel,
    "MultiProc": divergence_check_multi,
    "MultiProc JIT": divergence_check_multi_jit
    }

#divergence_check_multi()