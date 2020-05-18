# Team Wish Upon A*
# Samantha Ngo, Daniel Rozenzaft, Anton Goretsky
# CSCI 35000 - Artificial Intelligence
# AI MTA Trip Planner: Main A* Algorithm and Driver File
# 2020-05-18

from queue import PriorityQueue
#from collections import deque
from subway_system import Subway_System
from subway_system import Current_State
import sys, math
args = sys.argv[1:]


def main():

    if len(args) != 2:
        print("Please input a starting and ending stop.")
        exit()

    directory_data, transfers_data, stop_order_data, mta = initialize_system()
    current_state = Current_State(mta.findStop(args[0]), mta.findStop(args[1]))

    output = open('route.txt', 'w')
    text = route(args[0],args[1], mta, current_state)
    output.write(text)
    print (text)

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

    #current_state = Current_State(mta.findStop(args[0]), mta.findStop(args[1]), 0)


    return directory_data, transfers_data, stop_order_data, mta


def route(start, end, mta, current_state):

    start = mta.findStop(start)
    end = mta.findStop(end)

    if not start or not end:
        return '\nNo station with the specified name was found. Please try again, or contact an administrator.'

    #This probably needs cleaning
    start.end = end
    end.end = end

    #pick best starting station
    '''minStop = ('', math.inf)
    for start_transfer in [start] + start.transfers:
        start_transfer.stopsToEnd = mta.transferStopsToEnd(start_transfer) # Facilitate heuristic calculation
        val = start_transfer.heuristic(start, end)
        print(val)
        if val  < minStop[1]:
            minStop = (start_transfer, val)

    start = minStop[0]
    start_pick = PriorityQueue()

    for start_transfer in [start] + start.transfers:
        start_transfer.startEval = True # Change definition of equality to exclude transfers for start evaluation
        start_transfer.start = start
        start_transfer.end = end # Set start and end stops

        if start_transfer.station_name != start.station_name: #Display transfer (without counting one) for differently-named starting options
            start_transfer.lastVisited = start

        if start_transfer != start:
            print (start_transfer)
            start_transfer.transferCount += 1

        start_transfer.stopsToEnd = mta.transferStopsToEnd(start_transfer) # Facilitate heuristic calculation

        start_pick.put(start_transfer) #Put into start_pick priority queue

    # Initialization

    start = start_pick.get() #Get best stop from priority queue
    #print('start: ' + str(start))'''

    frontier = PriorityQueue()
    frontier.put(start)

    explored = set()

    while not frontier.empty():
    #while frontier:

        # Pop from pqueue
        currentStop = frontier.get()

        #if currentStop.line != direc.line:

        # Pop from deque
        # #currentStop = frontier.pop()

        # Add current stop to explored
        explored.add(currentStop.stopID)

        # Can't expand transfers of last visited stop(s)
        if currentStop.lastVisited: # If it's not the starting stop
            for stop in currentStop.lastVisited.transfers: # Add all transfers of last visited stop to explored.
                explored.add(stop.stopID)

            '''#Update start if the first step is a transfer
            #This probably needs cleaning
            if currentStop == start:
                start = currentStop
                currentStop.start = start
                currentStop.lastVisited = None'''

        # Goal test
        #if end == currentStop:
        if end == currentStop and end.station_name == currentStop.station_name:
            #trace back route
            route = '\n\nArrive at: ' + end.station_name + ' (' + currentStop.line + ')\n'

            #Maybe some cleanup is needed?
            while currentStop != start:

                route = currentStop.line + ', ' + currentStop.station_name + ', ' + str(currentStop.transferCount) + ', ' + str(currentStop.heuristic(start, end)) + '\n' + route

                currentStop = currentStop.lastVisited

            start = currentStop

            route = '\n\n\nStart at: ' + start.station_name + ' (' + start.line + ')\n\n\n' + 'Intermediate Stops:\n\n' + route

            return route

        #Get neighbors: nextStop, prevStop, transfers
        neighbor_dirs = []

        if currentStop.nextStop:
            neighbor_dirs.append(currentStop.nextStop)

        if currentStop.transfers: #Already a list, so we can concatenate
            neighbor_dirs += currentStop.transfers

        if currentStop.prevStop:
            neighbor_dirs.append(currentStop.prevStop)

        #Add unexplored neighbors to frontier
        for direc in neighbor_dirs:
            if direc.stopID not in explored:# and direc not in frontier:

                #hn = direc.heuristic(end)

                #ideally we wouldn't have to set these every time, but the workaround for this (the Current_State class) is under... construction
                direc.start = start
                direc.end = end

                direc.lastVisited = currentStop #Set last visited stop for each unexplored neighbor
                #direc.startEval = False

                #update transferCount
                if currentStop.line != direc.line and direc != start and direc != end:
                    direc.transferCount = currentStop.transferCount + 1
                else:
                    #print (str(start) + ', ' + str(currentStop) + ', ' + str(direc) + ', ' + str(start.startEval))
                    direc.transferCount = currentStop.transferCount

                #update stopsToEnd if neighbor and end lines are the same
                direc.stopsToEnd = mta.transferStopsToEnd(direc)

                frontier.put(direc)
                #frontier.append(direc)

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
    print (start)
    print (end)
    return None

#def route(start, end):
#    mta = Subway_System(directory_data, transfers_data, stop_order_data)
#
#    start = mta.findStop(start)
#    end = mta.findStop(end)
#
#    if not start or not end:
#        return '\nNo station with the specified name was found. Please try again, or contact an administrator.'
#
#    # Initialization (temporarily using deque before heuristic is completed)
#    frontier = deque()
#    frontier.append(start)
#
#    #frontier = PriorityQueue()
#    #frontier.put(start)
#
#
#    explored = set()
#    #expanded = 0
#    #max_search_depth = 0
#
#
#    #while not frontier.empty():
#    while frontier:
#
#        #currentStop = frontier.get()
#        # Pop from dequq
#        currentStop = frontier.pop()
#
#        # Add current stop to explored
#        explored.add(currentStop.stopID)
#
#        # Can't expand transfers of last visited stop(s)
#        if currentStop.lastVisited: # If it's not the starting stop
#            for stop in currentStop.lastVisited.transfers: # Add all transfers of last visited stop to explored.
#                explored.add(stop.stopID)
#
#        # Goal test
#        if end.station_name in currentStop.station_name:
#            #trace back route
#            route = '\n\nArrive at: ' + end.station_name + '\n'
#
#            # tempStop = None
#            while currentStop.lastVisited != None:
#
#                #if not tempStop or currentStop.station_name != tempStop.station_name:
#                route = currentStop.line + ', ' + currentStop.station_name + '\n' + route
#
#                #tempStop = currentStop
#                currentStop = currentStop.lastVisited
#
#            route = '\n\n\nStart at: ' + start.station_name + '\n\n\n' + 'Intermediate Stops:\n\n' + route
#
#            return route
#
#        #expanded += 1
#
#        #Get neighbors: nextStop, prevStop, transfers
#        neighbor_dirs = []
#        #Prioritizes next stop on current line (LIFO)
#        if currentStop.prevStop:
#            neighbor_dirs += [currentStop.prevStop]
#        if currentStop.transfers: #(Already a list)
#            neighbor_dirs += currentStop.transfers
#        if currentStop.nextStop:
#            neighbor_dirs += [currentStop.nextStop]
#
#
#        #Add unexplored neighbors to frontier
#        for direc in neighbor_dirs:
#            if direc not in frontier and direc.stopID not in explored:
#
#                direc.lastVisited = currentStop #Set last visited stop for each unexplored neighbor
#
#                #frontier.put(direc)
#                frontier.append(direc)
#
#            '''
#            neighbor_temp = board_structure.board_state()
#            neighbor_temp.copy(new.board)
#            neighbor_temp.depth += 1
#            worked = neighbor_temp.find_neighbor(direc)
#            if worked and neighbor_temp not in explored:
#                # Heuristic Function
#                # Note: Key decrease if in frontier is not necessary, due to __lt__ in board_tuple class.
#                hn = neighbor_temp.heuristic(goal_board)
#                neighbor_temp_tuple = board_structure.board_tuple(hn, neighbor_temp)
#                frontier.put(neighbor_temp_tuple)
#                # This solution will reduce complexity to O(1) from O(n) of usual union section
#                # Changes functionality slightly of explored, but not needed in this implementation to be strict.
#                explored.add(neighbor_temp)
#                #max_search_depth = max(max_search_depth, neighbor_temp.depth)'''
#
#    #You should never get here
#    print("Impossible or Something Broke...")
#    return None



if __name__ == "__main__":
    main()
