#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 22:17:15 2021

Holds basic properties of a route: 
    longName (customer-facing name)
    rID (Internal ID)
    destinations (endpoints of the route)
    numStops (total number of stops on the route)
    
@author: Li
"""

class Route:
    def __init__(self, longName, rID, destinations, numStops):
        self.longName = longName;
        self.rID = rID;
        self.numStops = numStops
        
    def getLongName(self):
        return self.longName
    
    def getID(self):
        return self.rID
    
    def getDestinations(self):
        return self.destinations
    
    def getNumStops(self):
        return self.numStops
    