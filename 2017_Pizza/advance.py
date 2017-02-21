#!/usr/bin/env/python

import numpy as np
import pandas as pd


def KokouTesselation(object):

    def __init__(self, pizza):
        self.pizza = pizza
        self.validator = SliceValidator(pizza)

    def next_move(self, r0, c0, dir):
        moves = self.pizza.moves[dir]
        sl = np.column_stack([moves.delta_i + r0, moves.delta_j + c0])
        for s in sl:
            valid = self.pizza.__check_slice_valid(s)
            if valid:
                return s
        return None
