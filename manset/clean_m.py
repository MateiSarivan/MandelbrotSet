from concurrent.futures.process import ProcessPoolExecutor
import numpy as np
from concurrent.futures import ThreadPoolExecutor
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


def div_check(y_range, c_real):
    result = np.empty(y_range.size)
    for index_y in range(y_range.size):
        c_imaginary = y_range[index_y]
        c = complex(c_real, c_imaginary)
        z = complex(0, 0)

        for iteration_number in range(100):
            z = z * z + c
            if abs(z) > 4:
                result[index_y] = iteration_number
                break
        else:
            result[index_y] = iteration_number

    # print(result)
    return result


def divergence_check_multi(x_range=np.array([1, 2, 3, 4]), y_range=np.array([5, 6, 7, 8])):
    len_x = len(x_range)
    len_y = len(y_range)
    mesh = np.empty((len_x, len_y))
    partial_div_check = functools.partial(div_check, y_range)
    pool = ProcessPoolExecutor(max_workers=8)
    future = pool.map(partial_div_check, y_range)
    pool.shutdown()


    index = 0
    for result in future:
        mesh[index, :] = result
        index += 1

    return mesh
    

divergence_check_multi()