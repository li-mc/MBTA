#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 20:20:30 2021

A graph that builds subway stops and contains information about which route
each stop is on.

addStop(stop) adds a unique stop to the total stops if it does not already exist.
addEdge(stop1, stop2) adds a directional edge from stop1 to stop2.
clearStop() clears the connectivity of a stop.
getGraph() returns the underlying dictionary of stop names.
getPathBetweenStops(stop1, stop2) returns a path between stops.  
This is sensitive to Covid mode, which affects closures and whether 
certain graph components are connected.
setCovidMode(bool) sets the Covid mode setting.
setClosedStops(dict) replaces the current dictionary of closed stops.

@author: Li
"""

class StopGraph:
    def __init__(self):
        self.graphDict = {}
        self.closedStops = {}
        self.covidMode = False
        
    #Add a unique stop to the total stops.
    def addStop(self, stop):
        if stop not in self.graphDict:
            self.graphDict[stop] = [];
                 
    #Add a directional edge from stop1 to stop2.
    def addEdge(self, stop1, stop2):
        if stop2 not in self.graphDict[stop1]:
            self.graphDict[stop1].append(stop2)
    
    #Clear a stop from the map.
    def clearStop(self, stop):
        self.graphDict[stop] = [];
    
    #Return the graph of stops
    def getGraph(self):
        return self.graphDict
    
    #Return a path between stops.  Check inputs then hand data to search.
    def getPathBetweenStops(self, stop1, stop2):
        if stop1 not in self.graphDict:
            raise NameError(stop1 + ' not in stops')
        if stop2 not in self.graphDict:
            raise NameError(stop2 + ' not in stops')
        return self.bfsPath(stop1, stop2)
    
    #Use breadth-first search to find a path between stop1 and stop2.
    def bfsPath(self, stop1, stop2):
        #No travel information is available for going from one stop to the same stop.
        if stop1 == stop2:
            return []
        
        #No travel information if the entry stop or exit stops are closed and we 
        #are not in Covid mode.
        if not self.covidMode and (self.closedStops[stop1] or self.closedStops[stop2]):
            return []
        
        #If we are on Covid mode, we can only travel between closed circuits of 
        #open stops and closed stops.
        if self.covidMode and not (self.closedStops[stop1] == self.closedStops[stop2]):
            return []
        
        if self.covidMode:
            circuitMode = self.closedStops[stop1]
        
        visited = []
        queue = [[stop1]]
        
        while queue:
            path = queue.pop(0)
            stop = path[-1]
            if stop not in visited:
                neighbors = self.graphDict[stop]
                for neighbor in neighbors:
                    closed = self.closedStops[neighbor]
                    if not self.covidMode and closed:
                        continue
                    if self.covidMode and not (closed == circuitMode):
                        continue
                    newPath = list(path)
                    newPath.append(neighbor)
                    queue.append(newPath)
                    if neighbor == stop2:
                        return newPath
                visited.append(stop)        
        return []
    
    #Set Covid mode true or false
    def setCovidMode(self, cv):
        self.covidMode = cv
    
    #Add a dictionary of the current stops which are closed.
    def setClosedStops(self, stops):
        self.closedStops = stops
        
        