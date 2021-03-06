from queue import PriorityQueue
from collections import deque
from subway_system import Subway_System
import sys
args = sys.argv[1:]

# Stop Directory
#stop_order: connects line names to routes
directory_data = open('stop_directory.csv','r').read().split('\n')

# Transfers Directory
transfers_data = open('stop_transfers.csv', 'r').read().split('\n')

#Stop Order Directory
stop_order_data = open('stop_order.csv', 'r').read().split('\n')


def route(start, end):
    mta = Subway_System(directory_data, transfers_data, stop_order_data)

    start = mta.findStop(start)
    end = mta.findStop(end)

    if not start or not end:
        return '\nNo station with the specified name was found. Please try again, or contact an administrator.'
    
    # Initialization (temporarily using deque before heuristic is completed)
    frontier = deque()
    frontier.append(start)

    #frontier = PriorityQueue()
    #frontier.put(start)
    
    
    explored = set()
    #expanded = 0
    #max_search_depth = 0


    #while not frontier.empty():
    while frontier:

        #currentStop = frontier.get()
        # Pop from dequq
        currentStop = frontier.pop()

        # Add current stop to explored
        explored.add(currentStop.stopID)

        # Can't expand transfers of last visited stop(s)
        if currentStop.lastVisited: # If it's not the starting stop
            for stop in currentStop.lastVisited.transfers: # Add all transfers of last visited stop to explored.
                explored.add(stop.stopID)

        # Goal test
        if end.station_name in currentStop.station_name:
            #trace back route
            route = '\n\nArrive at: ' + end.station_name + '\n'
            
            # tempStop = None
            while currentStop.lastVisited != None:

                #if not tempStop or currentStop.station_name != tempStop.station_name:
                route = currentStop.line + ', ' + currentStop.station_name + '\n' + route
                
                #tempStop = currentStop
                currentStop = currentStop.lastVisited

            route = '\n\n\nStart at: ' + start.station_name + '\n\n\n' + 'Intermediate Stops:\n\n' + route
            
            return route

        #expanded += 1

        #Get neighbors: nextStop, prevStop, transfers
        neighbor_dirs = []
        #Prioritizes next stop on current line (LIFO)
        if currentStop.prevStop:
            neighbor_dirs += [currentStop.prevStop]
        if currentStop.transfers: #(Already a list)
            neighbor_dirs += currentStop.transfers
        if currentStop.nextStop: 
            neighbor_dirs += [currentStop.nextStop]
        
        
        #Add unexplored neighbors to frontier
        for direc in neighbor_dirs:
            if direc not in frontier and direc.stopID not in explored:

                direc.lastVisited = currentStop #Set last visited stop for each unexplored neighbor

                #frontier.put(direc)
                frontier.append(direc)

            '''
            neighbor_temp = board_structure.board_state()
            neighbor_temp.copy(new.board)
            neighbor_temp.depth += 1
            worked = neighbor_temp.find_neighbor(direc)
            if worked and neighbor_temp not in explored:
                # Heuristic Function
                # Note: Key decrease if in frontier is not necessary, due to __lt__ in board_tuple class.
                hn = neighbor_temp.heuristic(goal_board)
                neighbor_temp_tuple = board_structure.board_tuple(hn, neighbor_temp)
                frontier.put(neighbor_temp_tuple)
                # This solution will reduce complexity to O(1) from O(n) of usual union section
                # Changes functionality slightly of explored, but not needed in this implementation to be strict.
                explored.add(neighbor_temp)
                #max_search_depth = max(max_search_depth, neighbor_temp.depth)'''

    #You should never get here
    print("Impossible or Something Broke...")
    return None

#transfer-less test [WORKING!]

output = open('route.txt', 'w')
if len(args) > 1:
    text = route(args[0],args[1])
    output.write(text)

else:
    text = route('Neck Rd', 'Av H')
    
print (text)