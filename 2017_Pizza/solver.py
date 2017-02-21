# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 18:58:34 2017

@author: Andreu Mora
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import iolib as iolib

class PizzaBoard:
    
    def __init__ (self):
        pass
    
    def load_from_scenario (self, scenario_in):
        dict_in = iolib.get_pizza_df(scenario_in)
        self.pizza = pd.DataFrame(dict_in['pizza'])
        self.L = dict_in['L']
        self.H = dict_in['H']   
    
    def create_random_pizza (self, R, C):
        self.pizza = pd.DataFrame(np.random.randint(0, high=2, size=(R,C)))  
        self.L = np.random.randint(1,5)
        self.H = np.random.randint(5,10)
        
    def init_slice_plan (self, N):
        self.slice_plan = pd.DataFrame(index=range(N), columns=['r_min', 'r_max', 'c_min', 'c_max'])
        pass
            
    def display_pizza (self):
        plt.matshow(self.pizza)
        
    def get_pizza_report(self):
        df = board.pizza
        print ("Dimensions = {}".format(df.shape))
        num_tomato = df.sum().sum()
        num_mushroom = df.count().sum() - num_tomato
        print ("Number of mushrooms = {}".format(num_mushroom))
        print ("Number of tomatoes = {}".format(num_tomato))
        
    def __check_slice_valid (self, slice_in):
        num_tomato = slice_in.sum().sum()
        num_mushroom = slice_in.count().sum() - num_tomato
        if num_tomato + num_mushroom <= self.H and num_tomato >= self.H and num_mushroom >= self.H:
            return True
        else:
            return False
        
    def get_min_slice (self, i, j, origin='center'):
        if origin == 'center':
            step_d = self.L
            # start growing from here
            while i+step_d <= self.pizza.shape[0] and j+step_d <= self.pizza.shape[1]:
                slice_out = self.pizza.loc[i:i+step_d, j:j+step_d]
                if self.__check_slice_valid (slice_out):
                    return slice_out
                else:
                    step_d = step_d + 1 # increment naively
              
board = PizzaBoard()
board.load_from_scenario('small')
board.get_pizza_report()
#board.display_pizza()
board.get_min_slice(4,4)
        