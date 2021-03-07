#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:39:57 2021

@author: Li 
This class uses the MBTA API to fetch, filter, and output subway-only routes.

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
        
    def getLongNames(self):
        longNames = []
        for route in self.allRoutes:
            longNames.append(route.getLongName())
        return longNames

    #Get the total count of unique stops
    def getUniqueStops(self):
        return(len(self.allStops))
    
    #Return the long name of the Route with the most stops
    def getMostStops(self):
        routeInd = np.argmax(list([x.getNumStops() for x in self.allRoutes]))
        return self.allRoutes[routeInd].getLongName()
    
    #Return the long name of the Route with the fewest stops
    def getFewestStops(self):
        routeInd = np.argmin(list([x.getNumStops() for x in self.allRoutes]))
        return self.allRoutes[routeInd].getLongName()
            
    #Other interesting statistic:
    #Return the long name of the route with the most connections to other routes.
    def getMostConnectivity(self):
        return 0
    
    
    #Get list of routes between firstStop and secondStop.
    def getRoutesBetweenStops(self, firstStop, secondStop):
        return 0
        
    def setCovidMode(self, mode):
        if isinstance(mode, bool):
            self.covidMode = mode
    
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
        
        #Create graph
        self.stopGraph = StopGraph()
         
        prevStop = []
        for route in self.routeData:
            for direction in route['attributes']['direction_names']:
                conn.request("GET", "/stops" + connReq 
                         + "filter[route]=" + route['id']
                         + "&filter[direction_id]=" + direction)
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
                    
                #Reach the end of the line.
                prevStop = []
                
            
            
            
            #Add a route to the list of routes
            self.allRoutes.append(Route(route['attributes']['long_name'],
                                        route['id'],
                                        route['attributes']['direction_names'],
                                        len(stops)))

        #Close connection
        print(self.stopGraph.getGraph())
        conn.close()
        
  
if __name__ == "__main__":
    mb = MBTANavigator()
    keyPath = "key.txt"
    mb.loadKeyFromPath(keyPath)
    mb.getData()
    rt = mb.getLongNames()
    print(mb.getMostStops())
    print(mb.getFewestStops())
    
        