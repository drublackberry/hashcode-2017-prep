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
    
    
    def compute_from_collection_array(self, collection_array, in_pickle=''):
        ''' Computes a target board table using the collections inside'''
        print 'Computing target board from collections'
        if in_pickle=='':
            out_df = pd.DataFrame(columns=['tmin', 'tmax', 'lat', 'lon', 'score', 'rel_score'])
            for collec in collection_array.collections:
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
            out_df = pd.read_pickle(in_pickle)
        self.board = out_df
        
    def compute_opportunity_cost (self, in_vis):
        ''' Adds the opportunity cost of using a certain satellite at a certain 
        time by checking which potential is there in using such satellite
        '''
        # Merge the target board with the visibility with time
        in_vis['max_lat'] = in_vis['lat'] + in_vis['d']
        in_vis['min_lat'] = in_vis['lat'] - in_vis['d']
        in_vis['max_lon'] = in_vis['lon'] + in_vis['d']
        in_vis['min_lon'] = in_vis['lon'] - in_vis['d']
        out_df = in_vis[['sat_id', 'max_lat', 'min_lat', 'max_lon', 'min_lon', 'time']]
        
                
            

class CollectionArray:
    '''Class that contains all the collections'''
    
    def __init__  (self):
        pass
    
    def load_from_scenario (self, scenario):
        self.collections = []
        for c in scenario.collections:
            my_collection = Collection(c['value'], c['coords'], c['trange'])
            self.collections.append(my_collection)
                
    def order_by_score(self):
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


    def compute_target_board(self, in_pickle=''):
        ''' Computes a target board table using the collections inside'''
        print 'Computing target board from collections'
        if not(in_pickle==''):
            out_df = pd.read_pickle(in_pickle)
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
        
    def print_status (self):
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
        
    def print_status (self):
        print 'Target'
        print self.coords 
        print self.trange
        
    def determine_visibility(self, in_constellation):
        ''' Given a constellation checks which satellites can actually see 
        the target at the time number of time slots 
        Returns a dataframe with id, lat, lon, time
        '''
        out_df = pd.DataFrame(columns=['sat_id', 'lat', 'lon', 'time', 'd'])
        # For each time range check which satellites can see it
        for time_ind in self.trange.index:
            df = in_constellation.filter_by_time_range(self.trange.loc[time_ind])
            # merge with d to get the maximum FOV
            df = df.merge(in_constellation.satellites[['sat_id', 'd']], on='sat_id')
            # Check the condition of lat-lon
            df = df[df['lat']+df['d'] >= self.coords.lat]
            df = df[df['lat']-df['d'] <= self.coords.lat]
            df = df[df['lon']+df['d'] >= self.coords.lon]
            df = df[df['lon']-df['d'] <= self.coords.lon]
            out_df = out_df.append(df[['sat_id', 'lat', 'lon', 'time', 'd']])
        return out_df

                    
class Constellation:
    ''' Class that contains a number of satellites
    '''
    
    def __init__ (self):
        pass
    
    
    def load_from_scenario (self, in_scenario, in_pickle=''):
        ''' Loads a constellation from the scenario
        '''
        
        print 'Loading ephemeris for ' + str(len(in_scenario.sats))  + ' satellites'
        self.satellites = pd.DataFrame(columns=['sat_id', 'w', 'd'])
        self.fixed_pointing = pd.DataFrame(columns=['sat_id', 'time', 'lat', 'lon'])
        if in_pickle == '':
            self.ephemeris = pd.DataFrame(columns=['sat_id', 'time', 'lat', 'lon'])
            for sat_ind in in_scenario.sats.index:
                mySatellite = Satellite (sat_ind, in_scenario.sats.loc[sat_ind])
                self.ephemeris = self.ephemeris.append(mySatellite.orbit)
        else:
            print '-> pickle found: using precomputed ephemeris'
            self.ephemeris = pd.read_pickle(in_pickle)
        self.satellites = in_scenario.sats[['w', 'd']].reset_index()
        self.satellites.rename(columns={'index':'sat_id'}, inplace=True)
        
    def filter_by_time_range (self, in_trange):
        df = self.ephemeris[self.ephemeris['time']>= in_trange['tmin']]
        df = df[df['time']<=in_trange['tmax']]
        return df
        
        
    def plot (self, sat_id_to_plot):
        df = self.ephemeris.set_index('sat_id')
        for sat in sat_id_to_plot:
            plt.plot(df.loc[sat, 'lon'], df.loc[sat, 'lat'], '.', c=np.random.rand(3,1))
        plt.show()
        
        
class Satellite:
    ''' Class that encapsulates the pointing of the satellite 
    '''
    
    def __init__ (self, in_Id, in_sat_descr):
        self.id = in_Id
        self.init_lat = in_sat_descr['lat0']
        self.init_lon = in_sat_descr['lon0']
        self.v = in_sat_descr['v0']
        self.w = in_sat_descr['w']
        self.d = in_sat_descr['d']
        ''' propagate the trajectory of the satellite '''
        self.propagate_orbit()


    def propagate_orbit(self):
        ''' Propagate the default pointing of the satellite given the
        initial conditions
        '''  
        print "Propagating orbit of satellite " + str(self.ID)
        lat_vec = np.zeros((T,1))
        lon_vec = np.zeros((T,1))
        lat_vec[0] = self.init_lat
        lon_vec[0] = self.init_lon
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
        self.orbit['sat_id'] = [self.id]*T

        
        
    
# Read scenario
scenario = io.read_scenario('final_round_2016.in/weekend.in')
# Load the time
T = scenario.T

# Load the constellation
constellation = Constellation()
constellation.load_from_scenario(scenario, in_pickle='ephemeris.pickle')
#constellation.plot([0.0, 1.0, 2.0, 39.0])

# Load the collection and acquire smartly
collection_array = CollectionArray()
collection_array.load_from_scenario(scenario)

target_board = TargetBoard()
target_board.compute_from_collection_array(collection_array, in_pickle='target_board.pickle')

collection_order = collection_array.order_by_score()
for coll_ind in collection_order:
    collection = collection_array.collections[coll_ind]
    collection.print_status()
    kill_collection = False
    # Loop over the targets inside the collection
    for target_ind in collection.coords.index:
        if not(kill_collection):
            target = Target(collection.coords.loc[target_ind],  collection.trange)
            # Check which satellites can see the current target
            sat_vis = target.determine_visibility(constellation)
            if sat_vis.dropna().empty:
                # If target cannot be acquired, drop the collection
                print 'Target not acquirable, killing collection search'
                kill_collection = True
            # Check how much do we lose by using the satellite
            sat_vis_with_cost = target_board.compute_opportunity_cost(sat_vis)
            
            
            
    
    
    
    