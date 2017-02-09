#!/usr/bin/env python

import numpy as np


def read_input(fname):
    data = {}
    with open(fname, 'r') as fp:
        lines = [[int(xx) for xx in x.strip().split()] for x in fp.readlines()]
    data["T"] = lines[0][0]
    #print(data["T"])
    S = lines[1][0]
    #print(S)
    sats = np.asarray(lines[2:2 + S])
    #print(sats)
    num_imgrecords = lines[2 + S][0]
    #print("NUM", num_imgrecords)
    imgrecords = []
    idx = 3 + S
    for i in range(num_imgrecords):
        #print("VLR", lines[idx])
        V, L, R = lines[idx]
        coords = np.asarray(lines[idx:idx + L])
        tranges = np.asarray(lines[idx + L:idx + L + R])
        imgrecords.append((V, coords, tranges))
        idx += L + R + 1
    data["sats"] = sats
    data["collections"] = imgrecords
    return data


def write_output(fname, photographs):
    P = len(photographs)
    with open(fname, 'w') as fp:
        fp.write("%d\n", P)
        for p in P:
            fp.write("%d %d %d %d\n" % p)


if __name__ == "__main__":
    a = read_input("final_round_2016.in/weekend.in")
