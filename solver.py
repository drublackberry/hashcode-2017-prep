# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 20:35:29 2017

@author: andreu
"""

import numpy as np
import pandas as pd

T = 250000 # REPLACE BY IO SIMULATION TIME




class Collection:
    ''' Class that encapsulates a collection of images given by the targets to 
    be acquired and the cost associated to all the collection
    '''
    
    def __init__ (self, aValue, aTargetLat, aTargetLon):
        self.value = aValue
        self.targetLat = aTargetLat
        self.targetLon = aTargetLon
        

class Satellite:
    ''' Class that encapsulates the pointing of the satellite 
    '''
    
    def __init__ (self, aID, initLat, initLon, v, w, d):
        self.ID = aID
        self.initLat = initLat
        self.initLon = initLon
        self.v = v
        self.w = w
        self.d = d
        ''' propagate the trajectory of the satellite '''
        self.propagatePointing()
        ''' create an empty matrix of fixed pointings'''
        #self.fixed_pointing = pd.DataFrame(index=self.pointing.index, columns=self.pointing.columns)


    def propagatePointing(self):
        ''' Propagate the default pointing of the satellite given the
        initial conditions
        '''    
        lat_vec = np.zeros((T,1))
        lon_vec = np.zeros((T,1))
        lat_vec[0] = self.initLat
        lon_vec[0] = self.initLon
        v = self.v
        for t in range(T-1):
            # propagation is at t+1
            new_lat = lat_vec[t] + v
            new_lon = lon_vec[t] - 15
            if new_lat > 324000:
                lat_vec[t+1] = 648000 - new_lat
                lon_vec[t+1] = -648000 + new_lon
                v = -v
            elif new_lat < -324000:
                lat_vec[t+1] = - 648000 - new_lat
                lon_vec[t+1] = -648000 + new_lon
                v = -v
            else:
                lat_vec[t+1] = new_lat
                lon_vec[t+1] = new_lon
        self.pointing = pd.DataFrame(index=range(T), columns=['lat', 'lon'])                    
        self.pointing['lat'] = lat_vec
        self.pointing['lon'] = lon_vec

    def IsTargetOnFOV (self, aTarget):
        pass


class MissionTimeline:
    ''' Class that contains which satellite will acquire which target at which 
    time , it is a matrix of features ordered by time with value the satellite
    filling the order
    '''
    def __init__ (self):
        pass
    
v = 400
w = 16
d = 4000

s = Satellite(1, 0, 0, 4, 15, 100)
print s.pointing
    
        