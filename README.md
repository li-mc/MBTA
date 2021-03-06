# Broad Institute Genomics Platform software enginneer take-home
Li McCarthy | Mar. 5 2021





***

Text of original tasks:
#### Problem 1  
Write a program that retrieves data representing all "subway" routes: namely, "Light Rail"(type 0)
and “Heavy Rail” (type 1). The program should output their “long names”, e.g.: Red Line,
Blue Line, Orange Line , etc.
There are two ways to obtain subway-only routes:
(1) download all results from https://api-v3.mbta.com/routes and then filter locally; or
(2) use the server via https://api-v3.mbta.com/routes?filter[type]=0,1 to filter
results.
Choose an option and briefly document your decision in the code.

#### Problem 2  
Have your program fetch stops for those routes and output summary statistics:
(1) the total number of unique stops (two routes may pass through the same stop);
(2) the name of the subway route with the most stops and the one with the fewest stops; and
(3) some other interesting statistic, completely up to you.

#### Problem 3  
Extend your program to have a mode in which the user provides any two stops on the subway
routes. Output an ordered list of routes that could be taken to get between those stops.
For example, Kendall/MIT to Kenmore might output Red Line, Green Line . We would
prefer a clear and well-documented yet inefficient solution to an unclear, efficient one. But of
course both are preferred if you can strike that balance.
Hint: It might be tempting to hardcode things in your algorithm that are specific to the MBTA
system, but we believe it will make things easier for you to generalize your solution so that it
could work for different and/or larger subway systems.

#### Problem 4  
A suspect medRxiv preprint appeared that claims any stop with a name that includes a word
starting with C, O, V, I, or D is dangerous. They are now closed and trains can’t even pass
through them. Fortunately, MBTA will run separate trains between closed stops (e.g., on a route
connecting C—A—B—D, if C and D are closed, then a train will connect A and B). Given such
closures, update your program to accept a COVID-19 mode, along with two stops, and output
whether it is still possible to ride the subway between those two stops.
