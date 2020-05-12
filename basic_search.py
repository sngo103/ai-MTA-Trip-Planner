from queue import PriorityQueue
from subway_system import Subway_System
import sys


# Stop Directory
#stop_order: connects line names to routes
directory_data = open('stop_directory.csv','r').read().split('\n')

# Transfers Directory
transfers_data = open('stop_transfers.csv', 'r').read().split('\n')

#Stop Order Directory
stop_order_data = open('stop_order.csv', 'r').read().split('\n')

#startStop = sys.argv[1]
#endStop = sys.argv[2]

def route(start, end):
    mta = Subway_System(directory_data, transfers_data, stop_order_data)

    start = mta.findStop(start)
    end = mta.findStop(end)
    if not start or not end:
        return '\nNo station with the specified name was found. Please try again, or contact an administrator.'
    
    # Initialization
    frontier = PriorityQueue()
    frontier.put(start)
    explored = set()
    #expanded = 0
    #max_search_depth = 0


    while not frontier.empty():

        currentStop = frontier.get()
        explored.add(currentStop.stopID)

        if currentStop.stopID == end.stopID:
            route = '\n\nArrive at: ' + end.station_name + '\n'
            #trace back route
            while currentStop.lastStop != None:
                currentStop = currentStop.lastStop
                route = currentStop.station_name + '\n' + route

            route = '\nStart at: ' + start.station_name + '\n\n\n' + 'Intermediate Stops:\n\n' + route
            return route

        #expanded += 1
        neighbor_dirs = [currentStop.nextStop] #+ currentStop.transfers
        #print (currentStop.transfers)
        
        #=======NEXT FIX: MAKE TRANSFER LIST CONSIST OF STOPS, NOT STOP_IDS=======
        
        for direc in neighbor_dirs:
            direc.lastStop = currentStop
            if direc.stopID not in explored:
                frontier.put(direc)

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

    print("Impossible or Something Broke...")
    return None, None, None

#transfer-less test [WORKING!]
print (route('Neck Rd', 'Av H'))

#transfer test [not working: see notes]
#print (route('Brighton Beach', '68th St - Hunter College'))