# Team Wish Upon A*
# Samantha Ngo, Daniel Rozenzaft, Anton Goretsky
# CSCI 35000 - Artificial Intelligence
# AI MTA Trip Planner: Main A* Algorithm and Driver File
# 2020-05-18

from queue import PriorityQueue
from subway_system import Subway_System
import sys, math

args = sys.argv[1:]

def main():
    if len(args) != 2:
        sys.exit("---Incorrect usage. Must be 'python main.py <origin_str> <destination_str>'")

    directory_data, transfers_data, stop_order_data, mta = initialize_system()

    output = open('route.txt', 'w')
    text = route(args[0],args[1], mta)
    output.write(text)
    print(text)
    # # Start to Station Usage:
    # print(mta.startToStation("Knapp Street Pizza"))
    # print()
    # # Station to End Usage:
    # print(mta.stationToEnd("Kinkun Books"))

def initialize_system():
    # Stop Directory
    #stop_order: connects line names to routes
    directory_data = open('stop_directory.csv','r').read().split('\n')
    # Transfers Directory
    transfers_data = open('stop_transfers.csv', 'r').read().split('\n')
    #Stop Order Directory
    stop_order_data = open('stop_order.csv', 'r').read().split('\n')

    mta = Subway_System(directory_data, transfers_data, stop_order_data)

    return directory_data, transfers_data, stop_order_data, mta

def route(start, end, mta):
    start = mta.findStop(start)
    end = mta.findStop(end)

    if not start or not end:
        sys.exit("\nNo station with the specified name was found. Please try again, or contact an administrator.'")

    start.end = end
    end.end = end

    # Initialize Frontier and Explored History
    frontier = PriorityQueue()
    frontier.put(start)
    explored = set()

    while not frontier.empty():
        # Pop from pqueue
        currentStop = frontier.get()

        # Might be used to not double print transfer stations
        # if currentStop.line != direc.line

        # Add current stop to explored
        explored.add(currentStop.stopID)

        # If it's not the starting stop
        if currentStop.lastVisited:  
            # Add all transfers of last visited stop to explored.
            for stop in currentStop.lastVisited.transfers:
                explored.add(stop.stopID) # Isn't allowed to expand transfers of last visited stop(s)

        # Goal Test, also traces back the route
        if end == currentStop and end.station_name == currentStop.station_name:
            #trace back route
            route = '\n\nArrive at: ' + end.station_name + ' (' + currentStop.line + ')\n'
            while currentStop != start:
                route = currentStop.line + ', ' + currentStop.station_name + ', ' + str(currentStop.transferCount) + ', ' + str(currentStop.heuristic(start, end)) + '\n' + route
                currentStop = currentStop.lastVisited
            start = currentStop
            route = '\n\n\nStart at: ' + start.station_name + ' (' + start.line + ')\n\n\n' + 'Intermediate Stops:\n\n' + route
            return route

        # Get neighbors: nextStop, prevStop, transfers
        neighbor_dirs = []
        if currentStop.nextStop:
            neighbor_dirs.append(currentStop.nextStop)
        if currentStop.transfers: #Already a list, so we can concatenate
            neighbor_dirs += currentStop.transfers
            #for transfer in currentStop.transfers:
                # if accessibility == 'DOWNTOWN' and transfer.prevStop.heuristic(start, end) < transfer.nextStop.heuristic(start,end):
                    #add it to the frontier, since you can transfer as a disabled person
                # if accessibility == 'UPTOWN' and transfer.prevStop.heuristic(start, end) > transfer.nextStop.heuristic(start,end):
                    #add it to the frontier, since you can transfer as a disabled person
                # if accessibility == 'BOTH':
                    #add it to the frontier, no questions asked
                #else: don't add it, it's not accessible in your direction
        if currentStop.prevStop:
            neighbor_dirs.append(currentStop.prevStop)

        #Add unexplored neighbors to frontier
        for direc in neighbor_dirs:
            if direc.stopID not in explored:
                direc.start = start
                direc.end = end
                direc.lastVisited = currentStop #Set last visited stop for each unexplored neighbor
                #update transferCount
                if currentStop.line != direc.line and direc != start and direc != end:
                    direc.transferCount = currentStop.transferCount + 1
                else:
                    #print (str(start) + ', ' + str(currentStop) + ', ' + str(direc))
                    direc.transferCount = currentStop.transferCount
                #update stopsToEnd if neighbor and end lines are the same
                direc.stopsToEnd = mta.transferStopsToEnd(direc)
                frontier.put(direc)

    #You should never get here
    print("Impossible or Something Broke...")
    print (start)
    print (end)
    return None

if __name__ == "__main__":
    main()