#!/usr/bin/env python

import numpy as np
import pandas as pd
import os

def get_pizza_df(scen):
    fname = os.path.join(".", scen + ".in")
    R, C, L, H = np.genfromtxt(fname, max_rows=1, dtype=np.int64)
    print(R, C, L, H)
    data = np.genfromtxt(fname, skip_header=1,
                         delimiter=1, dtype=None)
    assert(data.shape == (R, C))
    data2 = np.zeros(data.shape, dtype=np.uint8)
    data2[np.where(data == b'T')] = 1
    df = pd.DataFrame(data2)
    return {'pizza': df, 'L': L, 'H': H, 'source': fname}


def write_solution(slices, outfile):
    with open(outfile, 'w') as fp:
        fp.write("%d\n" % len(slices))
        for sl in slices:
            fp.write("%d %d %d %d\n" % (sl.r_min, sl.r_max, sl.c_min, sl.c_max))


def verify_solution(pizza_dict, slices):
    L = pizza_dict['L']
    H = pizza_dict['H']

    sizes = np.asarray([slice_size(sl) for sl in slices])
    tomatoes = np.asarray([np.count_nonzero(sl) for sl in slices])
    shrooms = sizes - tomatoes

    oversize = np.any(sizes > H)
    lack_tomatoes = np.any(tomatoes < L)
    lack_shrooms = np.any(shrooms < L)

    if oversize:
        raise RuntimeError("Oversized slices!")
    if lack_tomatoes:
        raise RuntimeError("Not enough tomatoes!")
    if lack_shrooms:
        raise RuntimeError("Not enough shrooms!")

    return True


def slice_size(sl):
    return abs((sl.r_max - sl.r_min) + 1) * abs((sl.c_max - sl.c_min) + 1)





if __name__ == "__main__":
    # Test
    #print(get_pizza_df("small"))
