#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:39:57 2021

@author: Li McCarthy
This uses the MBTA API to fetch, filter, and output subway-only routes.
If an API key is available, load from file.  
"""

import os, sys
from os import path

class MBTANavigator:
    def __init__(self):
        self.APIKey = ''
    
    #Load an API key from source "key.txt" if available.
    def loadKey(self):
        keyPath = os.path.join(sys.path[0], "key.txt")
        if path.exists(keyPath):
            fl = open(keyPath, "r")
            self.APIKey = fl.read();
            fl.close()
            
    #Return the API Key.      
    def getKey(self):
        return self.APIKey
    
    #