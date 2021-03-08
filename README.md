## MBTA Rail Line Exploration
Li McCarthy | Last Updated Mar. 7 2021

This is a small program that retrieves data from the open-source MBTA API (https://www.mbta.com/developers/v3-api) and uses it to answer questions
about the rail lines.  A demo program (NavigatorDemo.py) is provided that prints some sample output demonstrating how the program works.  A screenshot of the output is attached at the end of this section.  

The program can also be run manually by instantiating MBTANavigator.py.  To load data, first load API key (optional but recommended) with loadKey(key) or loadKeyFromFile(file).  Then call getData() to generate internal data structures.  

* getLongNames() returns a list of all route names.  
* getUniqueStops() returns a count of the total number of unique stops across
all routes.  
* getMostStops() returns the long name of the route with the most stops.  
* getFewestStops() returns the long name of the route with the fewest stops.  
* getMostConnectivity() returns the name of the stop that has the most connections to other stops.  
* getRoutesBetweenStops(stop1, stop2) returns a list of routes between two stops.  
* setCovidMode(bool) allows assignment of a mode that closes any stops with names that include a character in ['C', 'O', 'V', 'I', 'D'] and allows connected closed stops to be travelled between. Setting to false restores the previous state of closures and removes the special mode.  
* travelIsPossible(stop1, stop2) returns whether it is possible to travel between two stops.  

![Demo Output](demo_screenshot.png)
