#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:55:35 2021

@author: Work
"""
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../MBTANavigator'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from MBTANavigator import MBTANavigator

if __name__ == "__main__":
    mb = MBTANavigator()
    keyPath = os.path.join(sys.path[0], 'key.txt')
    mb.loadKey(keyPath)
    mb.connect()