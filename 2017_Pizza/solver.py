# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 18:58:34 2017

@author: Andreu Mora
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import iolib as iolib

def get_ordered_index (a, b):
    a = int(a)
    b = int(b)
    if a <= b:
        return range(a, b+1)
    else:
        return range(b, a+1)


class PizzaBoard:

    def __init__ (self):
        self.moves = {}
        self.moves['ur'] = pd.read_excel('moves.xlsx', sheetname='up_right')
        self.moves['ul'] = pd.read_excel('moves.xlsx', sheetname='up_left')
        self.moves['ll'] = pd.read_excel('moves.xlsx', sheetname='down_left')
        self.moves['lr'] = pd.read_excel('moves.xlsx', sheetname='down_right')
        self.slice_plan = pd.DataFrame(columns=['r_min', 'r_max', 'c_min', 'c_max'])
        self.vertices = pd.DataFrame(columns=['x', 'y', 'ul', 'ur', 'll', 'lr'])

    def load_from_scenario (self, scenario_in):
        dict_in = iolib.get_pizza_df(scenario_in)
        self.pizza = pd.DataFrame(dict_in['pizza'])
        self.L = dict_in['L']
        self.H = dict_in['H']

    def create_random_pizza (self, R, C):
        self.pizza = pd.DataFrame(np.random.randint(0, high=2, size=(R,C)))
        self.L = np.random.randint(1,5)
        self.H = np.random.randint(5,10)

    def display_pizza (self):
        plt.matshow(self.pizza)

    def get_pizza_report(self):
        df = self.pizza
        print ("Dimensions = {}".format(df.shape))
        num_tomato = df.sum().sum()
        num_mushroom = df.count().sum() - num_tomato
        print ("Number of mushrooms = {}".format(num_mushroom))
        print ("Number of tomatoes = {}".format(num_tomato))

    def check_slice_valid (self, slice_in):
        num_tomato = slice_in.sum().sum()
        num_mushroom = slice_in.count().sum() - num_tomato
        if num_tomato + num_mushroom <= self.H and num_tomato >= self.L and num_mushroom >= self.L:
            return True
        else:
            return False

    def find_slice (self, i,j):
        for dir_eval in self.moves.keys():
            i1 = (i + self.moves[dir_eval]['delta_i'])
            j1 = (j + self.moves[dir_eval]['delta_j'])
            for i_end, j_end in zip(i1, j1):
                slice_eval = self.pizza.loc[get_ordered_index(i,i_end), get_ordered_index(j,j_end)]
                if self.check_slice_valid(slice_eval):
                    return slice_eval
        return None

    def update_vertices (self, slice_in):
        df = pd.DataFrame(index=range(4), columns=['x', 'y', 'ul', 'ur', 'll', 'lr'])
        # for c in range(4):
        #     df.loc[c,'x'] = slice_in
        self.vertices.append({'x': slice_in.columns[-1], 'y': slice_in.index[-1]})
        self.vertices.append({'x': slice_in.columns[0], 'y': slice_in.index[-1]})
        self.vertices.append({'x': slice_in.columns[0], 'y': slice_in.index[0]})
        self.vertices.append({'x': slice_in.columns[-1], 'y': slice_in.index[-1]})

        pass



def main():
    board = PizzaBoard()
    board.load_from_scenario('big')
    board.get_pizza_report()
    slice_start = board.find_slice(board.pizza.shape[0]/2, board.pizza.shape[1]/2)
    print(slice_start)
    # Index the for corner os the slice in the list


if __name__ == "__main__":
    main()
