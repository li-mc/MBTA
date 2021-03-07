#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:39:57 2021

@author: Li 
This class uses the MBTA API to fetch, filter, and output subway-only routes.
https://api-v3.mbta.com/routes

To load data, first load API key (optional but recommended) with 
loadKey(key) or loadKeyFromFile(file).  Then call getData() to generate
internal data structures.

getLongNames() returns a list of all route names.
getUniqueStops() returns a count of the total number of unique stops across
all routes.
getMostStops() returns the long name of the route with the most stops.
getFewestStops() returns the long name of the route with the fewest stops.
getMostConnectivity() returns the name of the stop that has the most 
connections to other stops.
getRoutesBetweenStops(stop1, stop2) returns a list of routes between two stops.
setCovidMode(bool) allows assignment of a mode that closes stops with 
certain names and allows connected closed stops to be travelled between.
Setting to false restores the previous state of closures and removes the
special mode.
travelIsPossible(stop1, stop2) returns whether it is possible to travel 
between two stops.

"""
from os import path
import http.client
import json
from StopGraph import StopGraph
from Route import Route
import numpy as np

class MBTANavigator:
    def __init__(self):
        self.APIKey = ''
        self.API = 'api-v3.mbta.com'
        self.routeData = ''
        self.stopData = ''
        self.covidMode = False
        #List of all routes as Route objects
        self.allRoutes = []
        #Dictionary mapping stop name to their route long name
        self.stopsLongName = {}
        #Dictionary mapping stop name to whether they are closed or not
        self.stopsClosed = {}
        #Special case for also closing a certain subset of stops.
        self.stopsClosedCovid = {}
    
    #Get a list of the long (external-facing) route names
    def getLongNames(self):
        longNames = []
        for route in self.allRoutes:
            longNames.append(route.getLongName())
        return longNames

    #Get the total count of unique stops
    def getUniqueStops(self):
        return(len(self.stopGraph.getGraph().keys()))
    
    #Return the long name of the Route with the most stops
    def getMostStops(self):
        routeInd = np.argmax(list([x.getNumStops() for x in self.allRoutes]))
        return self.allRoutes[routeInd].getLongName()
    
    #Return the long name of the Route with the fewest stops
    def getFewestStops(self):
        routeInd = np.argmin(list([x.getNumStops() for x in self.allRoutes]))
        return self.allRoutes[routeInd].getLongName()
            
    #Other interesting statistic:
    #Return the name of the stop with the most connectivity to other stops
    def getMostConnectivity(self):
        graph = self.stopGraph.getGraph();
        maxStops = 0;
        for key in graph.keys():
            if len(graph[key]) > maxStops:
                maxStops = len(graph[key])
                mostConn = key
        return mostConn            
    
    #Get the number of connections available at any stop
    def getNumConnections(self, stop):
        return len(self.stopGraph.getGraph()[stop])
    
    
    #Get list of routes between firstStop and secondStop.
    #Return empty if none.
    def getRoutesBetweenStops(self, firstStop, secondStop):
        path = self.stopGraph.getPathBetweenStops(firstStop, secondStop)
        if len(path) == 0:
            return []
        else:
            #Interpret path into routes.
            outputRoutes = []
            prevRoutes = self.stopsLongName[firstStop]
            for i in range(1, len(path)):
                routeName = self.stopsLongName[path[i]]
                routeIntersect = list(set(prevRoutes) & set(routeName))
                #Add a route if transferring to a new, unique line.
                #In most realistic subway systems this will not produce an 
                #excessive amount of transfers, but it is not optimized for 
                #transfers and does not account for journey length
                if len(outputRoutes) == 0 or \
                (routeIntersect[0] not in outputRoutes and len(routeName) == 1):
                    outputRoutes.append(routeIntersect[0])
                prevRoutes = routeName
       
        return outputRoutes    
    
    #Return whether travel between two stops is possible, without regard to
    #the actual route.
    def travelIsPossible(self, firstStop, secondStop):
        path = self.stopGraph.getPathBetweenStops(firstStop, secondStop)
        if len(path) == 0:
            return False
        else:
            return True
    
    #Set COVID Mode on or off, closing stops that contain a word starting with 
    #[C, O, V, I, D]
    #Respects case
    def setCovidMode(self, mode):
        if not isinstance(mode, bool):
            raise TypeError('Invalid input for Covid Mode')
        #Update settings to turn on covid mode
        if not mode:
            self.stopGraph.setClosedStops(self.stopsClosed)
        else:
            #Copy self.stopsClosed in case there are already stops closed.
            self.stopsClosedCovid = self.stopsClosed.copy()
            covArr = ['C', 'O', 'V', 'I', 'D']
            stopList = self.stopsClosedCovid.keys()
            for stop in stopList:
                splitStop = stop.split()
                for letter in covArr:
                    hasLetter = [x.startswith(letter) for x in splitStop]
                    if any(hasLetter):
                        self.stopsClosedCovid[stop] = True
            self.stopGraph.setCovidMode(mode)
            self.stopGraph.setClosedStops(self.stopsClosedCovid)     
                
    #Load an API key from filepath if available.
    def loadKeyFromPath(self, keyPath):
        if path.exists(keyPath):
            fl = open(keyPath, "r")
            self.APIKey = fl.read().strip();
            fl.close()

    #Load key from text
    def loadKey(self, key):
        self.APIKey = key;
            
    
    #Connect using the API key, if available and build stops graph.
    def getData(self):
        conn = http.client.HTTPSConnection('api-v3.mbta.com')
        if len(self.APIKey) == 0:
            connReq = "?"
        else:
            connReq = "?api_key=" + self.APIKey + "&";
        #Filter by type of route to avoid pulling high-density bus data.
        conn.request("GET", "/routes" + connReq + "filter[type]=0,1") 
        res = conn.getresponse().read().decode()
        self.routeData = json.loads(res)["data"]
        
        #Initialize graph
        self.stopGraph = StopGraph()
         
        prevStop = []
        for route in self.routeData:
            conn.request("GET", "/stops" + connReq 
                         + "filter[route]=" + route['id'])
            res = conn.getresponse().read().decode()
            stops = json.loads(res)['data']
                                
            for stop in stops:
                stopName = stop['attributes']['name']
                self.stopsClosed[stopName] = False
                if stopName not in self.stopsLongName:
                    self.stopsLongName[stopName] = [route['attributes']['long_name']]
                else:
                    self.stopsLongName[stopName].append(route['attributes']['long_name'])
                        
                #Build graph
                self.stopGraph.addStop(stopName)
                if len(prevStop) > 0:
                    self.stopGraph.addEdge(prevStop, stopName)
                    self.stopGraph.addEdge(stopName, prevStop)                       
                prevStop = stopName;
                #Reach the end of the line and reset.
            prevStop = []
                
            
            #Add a route to the list of routes.
            self.allRoutes.append(Route(route['attributes']['long_name'],
                                        route['id'],
                                        route['attributes']['direction_names'],
                                        len(stops)))
        #Add closures to the graph
        self.stopGraph.setClosedStops(self.stopsClosed)

        #Manually clear and reassign the southern tips of the Red Line that are
        #grouped into the Ashmont/Braintree direction
        stopsToClear = ['JFK/UMass', 'Savin Hill', 'Fields Corner',
                        'Shawmut', 'Ashmont', 'North Quincy', 'Wollaston',
                        'Quincy Center', 'Quincy Adams', 'Braintree']
        for stop in stopsToClear:
            self.stopGraph.clearStop(stop)
            
        #Reassign the tips.
        prevStop = 'Andrew';
        ashLine = ['JFK/UMass', 'Savin Hill', 'Fields Corner',
                   'Shawmut', 'Ashmont', 'Cedar Grove']
        brainLine = ['JFK/UMass', 'North Quincy', 'Wollaston', 'Quincy Center',
                     'Quincy Adams', 'Braintree']
        
        for stop in ashLine:
            self.stopGraph.addEdge(prevStop, stop)
            self.stopGraph.addEdge(stop, prevStop)
            prevStop = stop
        
        prevStop = 'Andrew';
        for stop in brainLine:
            self.stopGraph.addEdge(prevStop, stop)
            self.stopGraph.addEdge(stop, prevStop)
            prevStop = stop
                
        #Close connection
        conn.close()
        
  

    
        