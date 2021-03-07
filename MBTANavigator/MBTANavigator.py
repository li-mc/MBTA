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

class MBTANavigator:
    def __init__(self):
        self.APIKey = ''
        self.API = 'api-v3.mbta.com'
        self.routeData = ''
        self.stopData = ''
        self.covidMode = False
        self.stopGraph = {};
        
    def getLongNames(self):
        routes = []
        for i in self.routeData:
            routes.append(i['attributes']['long_name'])
        return routes

    def getUniqueStops(self):
        print(self.stopGraph)
        return 0
    
    def getMostStops(self):
        return 0
    
    def getFewestStops(self):
        return 0
    
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
    def loadKey(self, keyPath):
        if path.exists(keyPath):
            fl = open(keyPath, "r")
            self.APIKey = fl.read().strip();
            fl.close()
            
    
    #Connect using the API key, if available.
    def getData(self):
        conn = http.client.HTTPSConnection('api-v3.mbta.com')
        if len(self.APIKey) == 0:
            connReq = "?"
        else:
            connReq = "?api_key=" + self.APIKey + "&";
        conn.request("GET", "/routes" + connReq + "filter[type]=0,1") 
        res = conn.getresponse().read().decode()
        self.routeData = json.loads(res)["data"]
                
        conn.request("GET", "/stops" + connReq + "filter[route_type]=0,1")
        res = conn.getresponse().read().decode()
        self.stopData = json.loads(res)["data"];
        
        print(self.stopData)
        
        #Build a graph of stops
        #self.stopGraph = StopGraph();
        #for stop in self.stopData:
            #self.stopGraph[stop["attributes"]["name"]] = []     

             
        conn.close()

        