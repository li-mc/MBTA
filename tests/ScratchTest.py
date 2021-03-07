#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:55:35 2021

Just some scratch notes used to exercise the code.  
Included for transparency.

@author: Li
"""
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../MBTANavigator'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from MBTANavigator import MBTANavigator

if __name__ == "__main__":
    mb = MBTANavigator()
    keyPath = "key.txt'"
    mb.loadKeyFromPath(keyPath)
    mb.getData()
    rt = mb.getLongNames()
    mb.getUniqueStops()
    
    
    
    