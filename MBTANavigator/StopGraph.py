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
        
    def addNode(self):
        