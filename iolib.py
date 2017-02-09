#!/usr/bin/env python

import numpy as np
from pandas import DataFrame
import os


class Scenario(object):

    def __init__(self, data):
        self.T = data["T"]
        self.sats = DataFrame(data=data["sats"], columns=["lat0", "lon0", "v0", "w", "d"])
        self.collections = []
        for c in data["collections"]:
            self.collections.append({"value": c[0],
                                     "coords": DataFrame(data=c[1], columns=["lat", "lon"]),
                                     "trange": DataFrame(data=c[2], columns=["tmin", "tmax"])})


def read_scenario(fname):
    """
    Pretty wrapper around read_input().
    """

    return Scenario(read_input(fname))


def read_all_scenarios(basedir):
    stuff = [(f, read_scenario(os.path.join(basedir, f))) for f in os.listdir(basedir)]
    return dict(stuff)


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
        coords = np.asarray(lines[idx + 1:idx + 1 + L])
        tranges = np.asarray(lines[idx + 1 + L:idx + 1 + L + R])
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
    #a = read_input("final_round_2016.in/weekend.in")
    read_all_scenarios("final_round_2016.in")
