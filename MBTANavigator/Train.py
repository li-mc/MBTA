#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 18:25:47 2021

@author: Li

Class to contain a train that will allow for easy navigation.
"""

class Train:
    def __init__(self, longName, internalName, connections):
        #Connections (other train lines)
        self.connections = []
        #External-facing name
        self.longName = ''
        #Internal name
        self.internalName = ''
        #stops
        self.stops = []
        
