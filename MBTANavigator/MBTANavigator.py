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
        self.API = 'api-v3.mbta.com';
    
    #Load an API key from filepath if available.
    def loadKey(self, keyPath):
        if path.exists(keyPath):
            fl = open(keyPath, "r")
            self.APIKey = fl.read();
            fl.close()
            
    #Return the API Key.      
    def getKey(self):
        return self.APIKey
    
    #Connect using the API key, if available.
    def connect(self):
        conn = http.client.HTTPSConnection('api-v3.mbta.com')
        if len(self.APIKey) == 0:
            connReq = "?api_key=" + self.APIKey
        else:
            connReq = ""
        conn.request("GET", "/routes?filter[type]=0,1" + connReq)
        res = conn.getresponse()
        print(res.read().decode())
        conn.close()

        