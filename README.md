## MBTA Rail Line Exploration
Li McCarthy | Last Updated Mar. 8 2021

### Summary  
  
This is a small program that queries the open-source MBTA API (https://www.mbta.com/developers/v3-api) and uses it to answer questions about the rail lines (Light Rail and Heavy Rail). A demo program (NavigatorDemo.py) is provided that prints some sample output demonstrating how the program works. A screenshot of the output is attached at the end of this page.  

### Data  
  
The MBTA API allows for retrieval of rich data related to bus and train line scheduling, stop locations, alerts, facilities, and more. We focus on the limited scope of Light and Heavy Rail line Routes and Stops. Colloquially, a _Route_ is a train line: the Red Line, Blue Line, Orange Line, Mattapan Trolley, and Green Lines B, C, D, and E. The Green Line branches are treated as separate Routes, while the Red Line branches are referred to by the same Red Line designation. While technically contiguous with the Red Line on maps of the MBTA, the Mattapan Trolley is an independent Route that runs between Ashmont and Mattapan.
  
A _Stop_ in this representation refers to one station along each Line. A Stop is associated with one or more Routes, representing transfers that can occur at each Stop.  

### Demo
To view some sample outputs, use a command prompt/terminal to navigate to the containing folder, then run **```python NavigatorDemo.py```**. This prints some simple outputs using real data.  

### How to Use  
To answer other questions, use a python script to manually instantiate the MBTANavigator class. An API Key is optional but recommended (https://api-v3.mbta.com/register) to avoid being rate-limited. To load data, first enter the API Key or load it from a file with ```loadKey(key)``` or ```loadKeyFromFile(filename)```. Then call ```getData()``` to generate internal data structures. 

```
navi = MBTANavigator()
# navi.loadKey(key) recommended
navi.getData()
```

##### Q1
On your instance of the MBTANavigator class, you can retrieve the "Long Names" (e.g. Red Line, Orange Line, etc) of all rail lines:  
```
print(navi.getLongNames())
```

##### Q2
The following summary metrics are provided:  
(1) The total number of unique stops  
**```print(navi.getUniqueStops())  ```**  
(2) The route with the most stops  
**```print(navi.getMostStops())  ```**  
(3) The route with the fewest stops  
**```print(navi.getFewestStops())  ```**  
(4) The stop with the highest connectivity to other stops  
**```print(navi.getMostConnectivity())```**  

##### Q3  
A method is provided to take in two stops, then return a list of routes to be taken to travel from the first stop to the second stop. 
**```print(navi.getRoutesBetweenStops('Kendall/MIT', 'Kenmore'))```**  

##### Q4
A method is provided that sets a new mode for the program--one that closes stops with any word starting with ['C', 'O', 'V', 'I', 'D'], case-sensitive.  These stops are accessible from other closed stops, and open stops are accessible from other open stops, but the two cannot be moved between.  Methods are provided to set and remove this mode, to get the routes between stops, and to get whether it is possible to move between the two stops.  
  
### Interface  
  
```loadKey(String)``` stores a user-entered API key.  
  
```loadKeyFromFile(String)``` loads a key from file.  
  
```getData()``` connects to and queries the API and builds the internal representation for train routes and stops.
  
```getLongNames()``` returns a list of all long names for routes in the MBTA system (e.g. Red Line, Orange Line).  
  
```getUniqueStops()``` returns the total number of unique stops across all routes.  

```getMostStops()``` returns the long name of the route with the most stops.  
  
```getFewestStops()``` returns the long name of the route with the fewest stops.  
  
```getMostConnectivity()``` returns the name of the stop with the most connections to other stops.  
  
```getRoutesBetweenStops(String, String)``` returns a list of routes one can take to travel from the first input stop to the second input stop. If none, returns an empty list.

```setCovidMode(bool)``` sets a special mode that closes any stops that include a character in ['C', 'O', 'V', 'I', 'D'], case-sensitive. Connected closed stops can be travelled between and connected open stops can be travelled between, but closed and open stops are cut off from each other and cannot be travelled between. Setting this mode to false restores the previous state of closures and removes the special mode.
  
```travelIsPossible(String, String)``` returns whether it is possible to travel between two stops.
  
### Design  
  
MBTANavigator provides an interface for simple queries. To generate paths, it builds a directed graph of stops (StopGraph.py) that is sensitive to stop closures. Getting the list of routes between two stops first uses a breadth-first search on the graph to find the shortest path between the stops from the graph, then MBTANavigator translates the list of stops into a list of routes with a greedy selection of the first intersecting route between each pair of stops. Transfers are treated as negligible -- the MBTA has relatively low connectivity, so it would typically be unlikely to generate a labor-intensive series of transfers that has fewer stops rather than one direct path that has more stops. Realistically, generating the optimal list of routes between point A and point B would also weight transfers from one route to another.  
  
### Demo Output  
  
![Demo Output](demo_screenshot.png)
