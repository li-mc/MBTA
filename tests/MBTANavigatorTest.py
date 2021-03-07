#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 20:23:47 2021

@author: Li

Test cases for MBTA Navigator.
This information is easily available so it can be tested directly.  
Tests that build the underlying graph are in StopGraphTest.py

Covers the following:
* Retrieve a text list of each route "Long Name"
* Get the total number of unique stops
* Get the name of the route with the most stops and the route with the fewest
* Get the route with the highest connectivity with other routes
* Get a list of routes between two stops
* Get a list of routes between two stops after COVID blockages that block 
certain stops.

"""
import unittest
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../MBTANavigator'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from MBTANavigator import MBTANavigator

class MBTANavigatorTest(unittest.TestCase):
    
    def setUp(self):
        self.routeNames = ['Red Line', 'Mattapan Trolley', 'Orange Line', 
                           'Green Line B', 'Green Line C', 'Green Line D',
                           'Green Line E', 'Blue Line'];
        self.navi = MBTANavigator()
        self.navi.loadKey("7c2ebb9b2cd74b62905201d54a8258ab")
        self.navi.getData()
     
    
    #Test that the "Long Names" for each route are identical.
    #Ordering of return is not specified.
    def testNames(self):
        nm = self.navi.getLongNames()
        self.assertEqual(nm.sort(), self.routeNames.sort())
        
    #Test the count 
    def testTotalUnique(self):
        nm = self.navi.getUniqueStops();
        self.assertEqual(nm, 118)
        
    #Test that the return for the MBTA route with the most stops is correct.
    def testMostStops(self):
        nm = self.navi.getMostStops()
        self.assertEqual(nm, 'Green Line B')
        
    #Test that the return for the MBTA route with the fewest stops is correct.
    def testFewestStops(self):
        nm = self.navi.getFewestStops()
        self.assertEqual(nm, 'Mattapan Trolley')
    
    #Test that the return for the stop with the most transfers is correct.
    def testConnectedStop(self):
        nm = self.navi.getMostConnectivity()
        self.assertEqual(nm, 'Park Street')
    
    #Test entering invalid inputs for ordered routes.
    @unittest.expectedFailure
    def testOrderedRoutesEmpty(self):
        self.navi.getRoutesBetweenStops([])
        
    @unittest.expectedFailure
    def testOrderedRoutesFirstFail(self):
        self.navi.getRoutesBetweenStops([], 'North Quincy')
        
    @unittest.expectedFailure 
    def testOrderedRoutesSecondFail(self):
        self.navi.getRoutesBetweenStops('North Quincy', [])
        
    #Test edge case where we go from one stop to the same stop.
    def testOrderedRoutesSame(self):
        ans = self.navi.getRoutesBetweenStops('North Quincy', 'North Quincy')
        self.assertEqual(ans, [])
        
    #Test that route to same route path is handled
    def testSingleRoute(self):
        ans = self.navi.getRoutesBetweenStops('Stony Brook', 'Downtown Crossing')
        self.assertEqual(ans, ['Orange Line'])
    
    #Test that route to different route transition is handled
    def testDiffRoute(self):
        ans = self.navi.getRoutesBetweenStops('Stony Brook', 'Central')
        self.assertEqual(ans, ['Orange Line', 'Red Line'])
    
    #Test that directionality is respected
    def testDiffDirectional(self):
        ans = self.navi.getRoutesBetweenStops('Central', 'Stony Brook')
        self.assertEqual(ans, ['Red Line', 'Orange Line'])
        
    #Test expected failure for setting Covid mode
    @unittest.expectedFailure
    def testCovidClosureFailure(self):
        self.navi.setCovidMode('foo')
     
    #Test navigation failure after Covid closure
    def testCovidClosure(self):
        self.navi.setCovidMode(True)
        ans = self.navi.getRoutesBetweenStops('Stony Brook', 'Downtown Crossing')
        self.assertEqual(ans, [])
        
    #Test Covid closure being turned on and off.'
    def testTurnOffCovidClosure(self):
       self.navi.setCovidMode(True)
       ans = self.navi.getRoutesBetweenStops('Stony Brook', 'Downtown Crossing')
       self.assertEqual(ans, [])
       self.navi.setCovidMode(False)
       ans = self.navi.getRoutesBetweenStops('Stony Brook', 'Downtown Crossing')
       self.assertEqual(ans, ['Orange Line'])
          
if __name__ == "__main__":
    unittest.main()