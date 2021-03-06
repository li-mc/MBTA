#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:39:57 2021

@author: Li McCarthy
This uses the MBTA API to fetch, filter, and output subway-only routes.
If an API key is available, load from file.  
"""
from os import path
import http.client

class MBTANavigator:
    def __init__(self):
        self.APIKey = ''
        self.API = 'api-v3.mbta.com'
        self.data = ''
        self.covidMode = False
        
    def getLongNames(self):
        if len(self.data) == 0:
            self.getRoutes()
        print(self.data)
        return 0
    
    def getUniqueStops(self):
        return 0
    
    def getMostStops(self):
        return 0
    
    def getFewestStops(self):
        return 0
    
    #Other interesting statistic
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
    def getRoutes(self):
        conn = http.client.HTTPSConnection('api-v3.mbta.com')
        if len(self.APIKey) == 0:
            connReq = "?filter[type]=0,1"
        else:
            connReq = "?api_key=" + self.APIKey + "&filter[type]=0,1";
        conn.request("GET", "/routes" + connReq)
        res = conn.getresponse().read().decode()
        self.data = res;
        conn.close()
        return res

        