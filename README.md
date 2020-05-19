# Final Project: AI MTA Trip Planner
### By Team Wish Upon A*
### Anton Goretsky, Samantha Ngo, Daniel Rozenzaft | Hunter College
### CSCI 35000 - Artificial Intelligence 
### 2020-05-18

--- Project Description Here

_**Note:** All three of us have been working together in real time on the same code via Microsoft LiveShare. We often host on Daniel's PC, therefore most commits are in his name._

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
- The modules queue, googlemaps, datetime, and json MUST be installed(via pip or other) in order for the program to work.
- A working Google Maps API Key must be in the main directory in order for the program to work. See Dependencies for more information on where and when you will receive the API Key.

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
- Import loops resulting from current_state structure
    - current_state is not being utilized at the moment

#### For the Future:
- Have algorithm better detect which train to start/end if the user inputs stops with many available trains
    - Currently randomized
- ensure that the user does not need to enter the exact name of desired stops
    - there is presently no way to distinguish between stops with the same station name
        - Ex: "7th Av" is a stop in Brooklyn on the F/G, a different Brooklyn stop on the B/Q, and a Manhattan stop on the B/D/E
        - the current method of relating user-inputted station names to stopIDs (mta.findStop) cannot distinguish between these different stations
    - current solution: allowing keywords (algorithm accepts substrings of station names)
    - potential improvement: use a drop-down GUI?
- Continue Fine-tuning heuristic
- Integrate buses
- Integrate ai-powered walking directions
- Add Timetable
- Add Real-Time Updates
- Resolve A train issues
- Route is sometimes not picking the shortest path
    - Needs confirmation
 - Include railroads
