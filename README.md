# Final Project: AI MTA Trip Planner
### By Team Wish Upon A*
### Anton Goretsky, Samantha Ngo, Daniel Rozenzaft | Hunter College
### CSCI 35000 - Artificial Intelligence 
### 2020-05-18

_**Note:** All three of us have been working together in real time on the same code via Microsoft LiveShare. We often host on Daniel's PC, therefore most commits are in his name._

#### Project Description
This project is a trip planner application that services four boroughs of NYC. Given a start and a destination, either an address or subway station, this application will generate the an optimal or sub-optimal route to the destination. If the user needs wheelchair accessibility, the application will provide a route with only accessible stations in mind. The directions provided will include the NYC subway, and walking directions to and from start and end addresses, if specified. This project uses the A* informed search algorithm with various heuristic metrics, from transfers counts to express train bias. Walking directions are provided via the Google Maps API. Data was generated using one pre-made dataset which we heavily modified by hand and by custom script to include all stops and more information. Evalutation was done manually and subjectively due to the various service changes around the coronavirus providing conflicting routes, and select lines being no longer in service. A several thousand route test file was generated and evaluated manually for "optimality."

#### Dependencies:
- Python version: >3.6.0
- Outside Modules Used: sys, math, random, **queue**, json, **googlemaps**, **datetime**
- **Google Maps API Key**: *An API KEY will be emailed to Professor Raja by the Blackboard submission deadline. The API Key is to be placed in the main directory as "api_key.txt". It is not uploaded to the repo and is included in the .gitignore for security reasons.

#### Our Environment Specifics(conditions under which we wrote and ran our code):
- Python Version: 3.7.4
- Operating System: Windows 10
- IDE: Atom, Microsoft Visual Studio 2019, Microsoft LiveShare

#### Usage Instructions: ```python main.py```

#### Important Notes:
- The modules queue, googlemaps, datetime, and json MUST be installed (via pip or other) in order for the program to work.
- A working Google Maps API Key must be in the main directory in order for the program to work. See Dependencies for more information on where and when you will receive the API Key.
- We didn't not focus on the user interface as much as we did the algorithms and structure, so there is little protection against incorrectly formatted input. Please try to follow the input specifications provided closely to avoid any unexpected and irrelevant errors.

#### Task Breakdown:
- Anton: Wrote enhanced A* algorithm, fine-tuned heuristics, conducted testing, researched state-of-the-art and potential algorithms
- Samantha: Designed and built search space structure, wrote api functions, created dataset, fine-tuned heuristics, wrote terminal feedback
- Daniel: Designed and built search space algorithm facilitation functions, wrote basic A* algorithm and DFS algorithm, worked on enhanced A* algorithm, created dataset, fine-tuned heuristics, conducted testing, debugged terminal feedback structure

#### Accomplishments:
- Much improved A* search, supporting transfers and routes in both directions
- Smarter, heuristic-based train selection for starting stations with multiple line options
- Heuristic takes into account total stops to destination, including transfers
- Heuristic that takes into account latitude/longitude-based distance to the end stop, number of transfers made, and distance to the end stop (now including transfers!)
- Designed and built efficient search space for traversal
- Created four-borough dataset
- Standardized station names in stop_directory 
- Fixed issues related to null pointers in data files
- Resolved issue in Stop class \_\_eq\_\_ method

#### Unresolved Issues:
- The A train splits off into 3 types in the Rockaways
    - Transfers between A trains were treated as negligible
    - Printing only shows a single version
    - Must be split back into its 3 types for optimal use.
- At "Aqueduct," there exists the only instance of a "split stop"
    - North and South directions are independent stops on single line: our structure cannot handle that.
    - Currently handled by combining "Aqueduct - North Conduit Av' and "Aqueduct Racetrack" into a single stop, "Aqueduct."
- The heuristic balance between choosing an express train or local train is very sensisitve
    - Some routes will favor express routes as desired
    - Some will switch to an express train at a seemingly odd point
    - Currently favors express slightly
    - May need to do more stern evaluation and implement heuristic adjustments per cases
- Accessibility constraint may crash on certain routes.
    - There exists an issue in adding some stations to the priority queue when feature is on
    - Priority queue empties before destination is reached
    - Seems to be caused by the A train divergences
    - Need to adjust station adding under accessibility constraint to make sure this never happens, otherwise, results appear       optimal.
- Walking directions are limited to picking the closest station to interpreted input address
    - No multiple starting point selection
    - No address interpretation options
- Printing walking directions has a slight formatting issue.
- Staten Island is not included.


#### For the Future:
- Continue fine-tuning heuristic
- Integrate buses
- Integrate ai-powered walking directions
- Add Timetable
- Add Real-Time Updates
- Resolve A train issues
- Route is sometimes not picking the shortest path
    - Not always choosing available express options when they are optimal
 - Include commuter rail
