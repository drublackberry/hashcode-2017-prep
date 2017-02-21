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

if __name__ == "__main__":
    # Test
    print(get_pizza_df("small"))
