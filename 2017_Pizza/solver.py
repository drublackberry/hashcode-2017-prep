# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 18:58:34 2017

@author: Andreu Mora
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class PizzaBoard:
    
    def __init__ (self):
        pass
    
    def load_from_scenario (self, scenario_in):
        # TODO: fill with iolib
        self.pizza = []
        self.L = 0
        self.H = 0
        pass
    
    def create_random_pizza (self, R, C):
        self.pizza = pd.DataFrame(np.random.randint(0, high=2, size=(R,C)))
        
    def display_pizza (self):
        plt.matshow(self.pizza)
        
    def get_pizza_report(self):
        df = board.pizza
        print ("Dimensions = {}".format(df.shape))
        num_tomato = df.sum().sum()
        num_mushroom = df.count().sum() - num_tomato
        print ("Number of mushrooms = {}".format(num_mushroom))
        print ("Number of tomatoes = {}".format(num_tomato))
        
        
        
        
board = PizzaBoard()
board.create_random_pizza(15, 15)
board.get_pizza_report()
board.display_pizza()
        