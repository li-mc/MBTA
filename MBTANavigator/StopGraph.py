#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 20:20:30 2021

A graph that builds subway stops and contains information about which route
each stop is on.

@author: Li
"""

class StopGraph:
    def __init__(self):
        self.graphDict = {};
        
    def addStop(self, stop):
        if stop not in self.graphDict:
            self.graphDict[stop] = [];
                 
        
    def addEdge(self, stop1, stop2):
        if stop2 not in self.graphDict[stop1]:
            self.graphDict[stop1].append(stop2)
            
    def clearStop(self, stop):
        self.graphDict[stop] = [];
    
    def getGraph(self):
        return self.graphDict
        