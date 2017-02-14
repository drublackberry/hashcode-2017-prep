# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 20:35:29 2017

@author: andreu
"""

import numpy as np
import pandas as pd
import iolib as io
import matplotlib.pyplot as plt
    

class TargetBoard:
    '''Class that contains all the targets with the scores 
    '''
    
    def __init__ (self):
        pass
    
    
    def computeFromCollectionArray(self, aCA, aPickle=''):
        ''' Computes a target board table using the collections inside'''
        print 'Computing target board from collections'
        if aPickle=='':
            out_df = pd.DataFrame(columns=['tmin', 'tmax', 'lat', 'lon', 'score', 'rel_score'])
            for collec in aCA.collections:
                for time_ind in collec.trange.index:
                    temp_df = collec.coords.copy()
                    temp_df['score'] = [collec.value]*len(temp_df)
                    temp_df['rel_score'] = [collec.value/np.float(len(temp_df))]*len(temp_df)
                    temp_df['tmin'] = collec.trange.loc[time_ind, 'tmin']
                    temp_df['tmax'] = collec.trange.loc[time_ind, 'tmax']
                    out_df = out_df.append(temp_df)
            out_df = out_df.reset_index()
            out_df.__delitem__('index')
        else:
            print '-> pickle found: using pickle instead'
            out_df = pd.read_pickle(aPickle)
        self.board = out_df
                
            

class CollectionArray:
    '''Class that contains all the collections'''
    
    def __init__  (self):
        pass
    
    def loadFromScenario (self, aScenario):
        self.collections = []
        for c in aScenario.collections:
            myCollection = Collection(c['value'], c['coords'], c['trange'])
            self.collections.append(myCollection)
                
    def orderByScore(self):
        ''' Order the collections by max(score),  min(num_targets)
        '''
        scores = np.array([])
        num_targets = np.array([])
        for c in self.collections:
            scores = np.append(scores, c.value)
            num_targets = np.append(num_targets, len(c.coords))
        df = pd.DataFrame(index=range(len(self.collections)), columns=['scores', 'num_targets'])
        df['scores'] = scores
        df['num_targets'] = num_targets
        df = df.reset_index().set_index(['scores', 'num_targets'])
        df.sort_index(level=[0,1], ascending=[False, True], inplace=True)
        return df['index']


    def computeTargetBoard(self, aPickle=''):
        ''' Computes a target board table using the collections inside'''
        print 'Computing target board from collections'
        if not(aPickle==''):
            out_df = pd.read_pickle(aPickle)
            print '-> pickle found. Using pickle instead'
            return out_df
        out_df = pd.DataFrame(columns=['tmin', 'tmax', 'lat', 'lon', 'score', 'rel_score'])
        for collec in self.collections:
            for time_ind in collec.trange.index:
                temp_df = collec.coords.copy()
                temp_df['score'] = [collec.value]*len(temp_df)
                temp_df['rel_score'] = [collec.value/np.float(len(temp_df))]*len(temp_df)
                temp_df['tmin'] = collec.trange.loc[time_ind, 'tmin']
                temp_df['tmax'] = collec.trange.loc[time_ind, 'tmax']
                out_df = out_df.append(temp_df)
        return out_df
            

class Collection:
    ''' Class that encapsulates a collection of images given by the targets to 
    be acquired and the cost associated to all the collection
    '''
    
    def __init__ (self, value, coords, trange):
        self.value = value
        self.coords = coords
        self.trange = trange
        
    def printStatus (self):
        print 'Collection'
        print ' Value = ' + str(self.value) + ', ' + \
              str(len(self.coords)) + ' targets, ' + \
              str(len(self.trange)) + ' time slots'
        
class Target:
    '''Class that encapsulates a target 
    '''
    def __init__ (self, coords, trange):
        self.coords = coords
        self.trange = trange 
        
    def printStatus (self):
        print 'Target'
        print self.coords 
        print self.trange
        
    def determineVisibility(self, aConstellation, aTargetBoard):
        ''' Given a constellation checks which satellites can actually see 
        the target at the time number of time slots 
        '''
        out_df = pd.DataFrame(columns=['trange', 'sat_id', 'tmin', 'tmax'])
        # For each time range check which satellites can see it
        for time_ind in self.trange.index:
            df = aConstellation.filterByTimeRange(self.trange.loc[time_ind])
            # merge with d to get the maximum FOV
            df = df.merge(aConstellation.satellites[['sat_id', 'd']], on='sat_id')
            # Check the condition of lat-lon
            df = df[df['lat']+df['d'] >= myTarget.coords.lat]
            df = df[df['lat']-df['d'] <= myTarget.coords.lat]
            df = df[df['lon']+df['d'] >= myTarget.coords.lon]
            df = df[df['lon']-df['d'] <= myTarget.coords.lon]
            # If the dataframe is empty, then the target cannot be seen and
            # whole collection should be dropped
            if df.empty:
                return out_df
            # Check which targets are seen at each time and lat/lon
            # TODO HERE: to a merge such as tmin < time < tmax AND
            # sat_lat -d < lat < sat_lat + d AND
            # sat_lon -d < lon < sat_lon +d
            # Including the time conditio of w/d
            
            
        return out_df

                    
class Constellation:
    ''' Class that contains a number of satellites
    '''
    
    def __init__ (self):
        pass
    
    
    def loadFromScenario (self, aScenario, aPickle=''):
        ''' Loads a constellation from the scenario
        '''
        
        print 'Loading ephemeris for ' + str(len(aScenario.sats))  + ' satellites'
        self.satellites = pd.DataFrame(columns=['sat_id', 'w', 'd'])
        self.fixed_pointing = pd.DataFrame(columns=['sat_id', 'time', 'lat', 'lon'])
        if aPickle == '':
            self.ephemeris = pd.DataFrame(columns=['sat_id', 'time', 'lat', 'lon'])
            for sat_ind in aScenario.sats.index:
                mySatellite = Satellite (sat_ind, aScenario.sats.loc[sat_ind])
                self.ephemeris = self.ephemeris.append(mySatellite.orbit)
        else:
            print '-> pickle found: using precomputed ephemeris'
            self.ephemeris = pd.read_pickle(aPickle)
        self.satellites = aScenario.sats[['w', 'd']].reset_index()
        self.satellites.rename(columns={'index':'sat_id'}, inplace=True)
        
    def filterByTimeRange (self, aTrange):
        df = self.ephemeris[self.ephemeris['time']>= aTrange['tmin']]
        df = df[df['time']<=aTrange['tmax']]
        return df
        
        
    def plot (self, sat_id_to_plot):
        df = self.ephemeris.set_index('sat_id')
        for sat in sat_id_to_plot:
            plt.plot(df.loc[sat, 'lon'], df.loc[sat, 'lat'], '.', c=np.random.rand(3,1))
        plt.show()
        
        
class Satellite:
    ''' Class that encapsulates the pointing of the satellite 
    '''
    
    def __init__ (self, aId, aSatDescr):
        self.ID = aId
        self.initLat = aSatDescr['lat0']
        self.initLon = aSatDescr['lon0']
        self.v = aSatDescr['v0']
        self.w = aSatDescr['w']
        self.d = aSatDescr['d']
        ''' propagate the trajectory of the satellite '''
        self.propagateOrbit()


    def propagateOrbit(self):
        ''' Propagate the default pointing of the satellite given the
        initial conditions
        '''  
        print "Propagating orbit of satellite " + str(self.ID)
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
            if lon_vec[t+1] < -648000:
                lon_vec[t+1] = 648000 + (lon_vec[t+1]+648000)
                
        self.orbit = pd.DataFrame(index=range(T), columns=['lat', 'lon'])                    
        self.orbit['lat'] = lat_vec
        self.orbit['lon'] = lon_vec
        self.orbit['time'] = range(T)
        self.orbit['sat_id'] = [self.ID]*T

        
        
    
# Read scenario
myScenario = io.read_scenario('final_round_2016.in/weekend.in')
# Load the time
T = myScenario.T

# Load the constellation
myConstellation = Constellation()
myConstellation.loadFromScenario(myScenario, aPickle='ephemeris.pickle')
#myConstellation.plot([0.0, 1.0, 2.0, 39.0])

# Load the collection and acquire smartly
myCollectionArray = CollectionArray()
myCollectionArray.loadFromScenario(myScenario)

myTargetBoard = TargetBoard()
myTargetBoard.computeFromCollectionArray(myCollectionArray, aPickle='target_board.pickle')

myCollectionOrder = myCollectionArray.orderByScore()
for coll_ind in myCollectionOrder:
    myCollection = myCollectionArray.collections[coll_ind]
    myCollection.printStatus()
    kill_collection = False
    # Loop over the targets inside the collection
    for target_ind in myCollection.coords.index:
        if not(kill_collection):
            myTarget = Target(myCollection.coords.loc[target_ind],  myCollection.trange)
            # Check which satellites can see the current target
            mySatVis = myTarget.determineVisibility(myConstellation, myTargetBoard)
            if mySatVis.dropna().empty:
                # If target cannot be acquired, drop the collection
                print 'Target not acquirable, killing collection search'
                kill_collection = True
            
            
    
    
    
    