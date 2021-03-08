#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 12:14:41 2021

This is a demo program for the MBTA Navigator that answers explicit questions.
@author: Li

"""

from MBTANavigator import MBTANavigator

if __name__ == "__main__":
    print('Starting MBTA Navigator Demo\n')
    mb = MBTANavigator()
    
    #I recommend entering an API key here through loadKey() or loadKeyFromFile()
    #to avoid rate limitations.
    
    mb.getData()
    print("The long names of all the MBTA routes are: " 
          + str(mb.getLongNames()) + "\n")
    print("Here are some interesting metrics:")
    print("Out of the MBTA Light and Heavy Rail lines, there are " 
          + str(mb.getUniqueStops()) + " unique stops.\n")
    print("Out of the MBTA Light Rail and Heavy Rail lines, "
          + mb.getMostStops() + " has the most stops and " 
          + mb.getFewestStops() + " has the fewest stops.\n")
    mc = mb.getMostConnectivity()
    numConns = mb.getNumConnections(mc)
    print("The best-connected stop is " + mc + ", which has a total of "
          + str(numConns) + " connections\n")
    print("Here are a few samples of transfers we can take to get around: \n")
    print("To get from the Broad Institute (Kendall/MIT) to the Museum of Fine Arts: ")
    print(mb.getRoutesBetweenStops("Kendall/MIT", "Museum of Fine Arts"))
    print("Then to go from the MFA to the aquarium: ")
    print(str(mb.getRoutesBetweenStops("Museum of Fine Arts", "Aquarium")) + "\n")
    
    print("Unfortunately, we have to closed service for any station that has a"
          + " name starting with a letter in COVID")
    print("We could previously ride from Tufts Medical Center to Sullivan Square: ")
    print(str(mb.getRoutesBetweenStops("Tufts Medical Center", "Sullivan Square")) + "\n")
    
    mb.setCovidMode(True)
    print("Now with the mode enabled, our route is: " 
          + str(mb.getRoutesBetweenStops("Tufts Medical Center", "Sullivan Square")) + "\n")
    print("However, trains are still running on a closed loop between closed and "
          + "non-closed stations.")
    print("We can take the train from Tufts Medical Center to Downtown Crossing: "
          + (str(mb.getRoutesBetweenStops("Tufts Medical Center", "Downtown Crossing")) + "\n"))
    print("We can also take the train between State and North Station: "
          + str(mb.getRoutesBetweenStops("State", "North Station")))
    print("But we can't reach Community College, which is one stop away: " 
          + str(mb.getRoutesBetweenStops("State", "Community College")) + "\n")
    print("We can ask if travel is possible between two stops. For State to North Station,"
          + " the answer is: " + str(mb.travelIsPossible("State", "North Station")))
    print("And for State and Community College, the answer is: " 
          + str(mb.travelIsPossible("State", "Community College")) + "\n")
    mb.setCovidMode(False)
    print("Finally, if we turn off COVID Mode, we can ask about State to "
          + "North Station again, and the answer is: " 
          + str(mb.travelIsPossible("State", "North Station")))

    
