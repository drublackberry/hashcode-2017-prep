# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 18:24:46 2017

@author: Andreu Mora
"""

# This is a test.

import numpy as np
import matplotlib.pyplot as plt

print("PK test")

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()

x = np.random.random((10,10))
plt.matshow(x)
plt.show() 

