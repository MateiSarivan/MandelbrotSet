import numba as nb
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import itertools
import functools



def divergence_check(x_range, y_range):
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
                if abs(z) > 16:
                    mesh[index_x, index_y] = iteration_number
                    break
            # else:
            #     mesh[index_x, index_y] = 0

    return mesh
            

# def divergence_check(c, divergence_condition):
#     z = complex(0, 0)

#     for iteration_number in range(divergence_condition):
#         z = z * z + c

#         if abs(z*z) > 4:
#             break
    
#     if iteration_number == 99:
#         return 0
#     else:
#         return iteration_number


@nb.jit(nopython=True)
def divergence_check_jit(x_range, y_range):
    len_x = len(x_range)
    len_y = len(y_range)
    mesh = np.empty((len_x, len_y))
    for index_x in np.arange(len_x):
        for index_y in np.arange(len_y):
            c_real = np.double(x_range[index_x])
            c_imaginary = np.double(y_range[index_y])
            c_x = c_real
            c_y = c_imaginary

            for iteration_number in range(100):
                c_real_squared = c_real * c_real - c_imaginary * c_imaginary
                c_imaginary_squared = 2*c_real*c_imaginary
                c_real = c_x + c_real_squared
                c_imaginary = c_y + c_imaginary_squared

                if np.abs(c_real + c_imaginary) > 4:
                    mesh[index_x, index_y] = iteration_number
                    break

    return mesh


@nb.jit(nopython=True)
def divergence_check_jit2(x_range, y_range):

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


def divergence_check_part1(x_range, y_range):
    mesh = np.empty((x_range.size, y_range.size))
    for index_x in np.arange(x_range.size):
        for index_y in np.arange(y_range.size):
            c_real = x_range[index_x]
            c_imaginary = y_range[index_y]
            
            c = complex(c_real, c_imaginary)

            mesh[index_x, index_y] = divergence_check_part2(c)

    return mesh

@nb.jit(nopython=True)
def divergence_check_part2(c):
    z = complex(0, 0)

    for iteration_number in np.arange(100):
        z = z*z+c
        if np.abs(z) > 4:
            return iteration_number
    else:
        return 0

@nb.jit(nopython=True)
def divergence_check_part4(c_real, c_imaginary):
    c = complex(c_real, c_imaginary)
    z = complex(0, 0)
    for iteration_number in np.arange(100):
        z = z*z+c
        if np.abs(z) > 4:
            return iteration_number
    else:
        return 0

@nb.jit(nopython = True, parallel = True)
def divergence_check_part3(x_range, y_range):
    mesh = np.empty((x_range.size, y_range.size))
    for index_x in nb.prange(x_range.size):
        c_real = x_range[index_x]
        for index_y in nb.prange(x_range.size):
            c_imaginary = y_range[index_y]
            mesh[index_x, index_y] = divergence_check_part4(c_real, c_imaginary)

    return mesh


def divergence_check_multiproc(x_range, y_range):
    with ThreadPoolExecutor(16) as ex:
        result = ex.map(divergence_check_jit2, x_range, y_range)

        print(type(result))

        print(len(list(result)))
            

def divergence_check_prc(c_real, c_imaginary):
    with ThreadPoolExecutor(16) as ex:
        results = np.array(list(ex.map(divergence_check_part4, c_real, c_imaginary)))


    return results
            

def div_check(y_range, c_real):
    result = np.empty(y_range.size)
    for index_y in np.arange(y_range.size):
        c_imaginary = y_range[index_y]
        c = complex(c_real, c_imaginary)
        z = complex(0, 0)
        for iteration_number in np.arange(100):
            z = z*z+c
            if np.abs(z) > 4:
                result[index_y] = iteration_number
        else:
            result[index_y] = 0
    return result
        
def divergence_check_multi(x_range, y_range):
    partial_div_check = functools.partial(div_check, y_range)
    mesh = np.empty((len(x_range), len(y_range)))
    with ThreadPoolExecutor() as ex:
        results = list(ex.map(partial_div_check, x_range))
    
    len(results)
    return mesh


def divergence_check_multis(x_range, y_range):
    mesh = np.empty((x_range.size, y_range.size))
    #for x in np.arange(x_range.size):
    results = []
    for y in y_range:
        result = div_check(x_range[0], y)
        results.append(result)
    mesh[0, :] = results

    return mesh



            